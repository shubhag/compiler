import pprint

class symbTbl:

	def __init__(self):
		self.mainSymbTbl = {
			'Main' :	{
				'scope' :	'Main',
				'type'	:	'function',	
				'pscope':	None,		#parent scope
				'retype':	'undefined',
				'functions': {} ,
				'identifier' : {}
			}
		}
		self.tempCount = 0 
		self.currScope = 'Main'
		self.switchList = []
		self.currFunc = 'Main'
		self.currClass = ''

	def chgClass(self, name):
		self.currClass = "Main." + name

	def checkNumArgs(self, funcName, numArgs):
		function = self.mainSymbTbl[self.currClass]['functions']
		if function.has_key(funcName):
			if len(function[funcName]['arglist']) != numArgs :
				raise Exception('Number of arguments passed in '+ funcName +' call not equal to that in its declration')

	def checkRetType(self, typeId, scope):
		funcName = self.mainSymbTbl[scope]['name']
		function = self.mainSymbTbl[self.currClass]['functions']
		if function.has_key(funcName):
			if function[funcName]['returnType'] != typeId :
				raise Exception("Type check error in return type of function")

	def checkType(self, funcName, typeId, index):
		function = self.mainSymbTbl[self.currClass]['functions']
		if function.has_key(funcName):
			if function[funcName]['arglist'][index]['type'] != typeId :
				raise Exception('TypeCheck Error')

	#for error handling
	def printSymbTbl(self):
		pprint.pprint(self.mainSymbTbl)

	def getFuncName(self,funcName):
		function = self.mainSymbTbl[self.currClass]['functions']
		if function.has_key(funcName):
			return function[funcName]['name']

	def addArgList(self, funcName, arguments):
		function = self.mainSymbTbl[self.currClass]['functions']
		if function.has_key(funcName):
			if arguments == None:
				function[funcName]['arglist'] = {}
			else:
				function[funcName]['arglist'] = arguments

	def addReturntype(self, funcName, returnType):
		function = self.mainSymbTbl[self.currClass]['functions']
		if function.has_key(funcName):
			function[funcName]['returnType'] = returnType

	def getReturntype(self, funcName):
		function = self.mainSymbTbl[self.currClass]['functions']
		if function.has_key(funcName):
			return function[funcName]['returnType']

	#to get the current scope name 
	def getCurrScopeName(self):
		return self.currScope

	def lookup_for_identifier(self, identifier):
		currScope = self.currScope
		idEntry = self.checkscope_id(identifier, currScope)
		if idEntry!= None : 
			return True
		else:
			return False

	def lookup_for_id(self, identifier):
		currScope =  self.currScope
		idEntry = self.checkscope_id(identifier, currScope)
		return idEntry

	#error in scope
	def checkscope_id(self, identifier, currScope):
		print currScope
		if currScope == 'Main' or currScope == None:
			return None
		tempScope = self.mainSymbTbl[currScope]['identifier']
		if tempScope.has_key(identifier):
			return tempScope[identifier]
		else:
			return self.checkscope_id(identifier, self.mainSymbTbl[currScope]['pscope'])

	def addNewScope(self, funcName,functype):
		pScope = self.currScope
		newSymbTbl = {
			'scope'	: pScope + "." + funcName,
			'type'	: functype,
			'pscope' : pScope,
			'retype' : 'undefined',
			'identifier' : {},
			'functions' : {},
			'offset' : 0,
			'name' : funcName
		}
		# print newSymbTbl, "115"
		self.mainSymbTbl[pScope + "." + funcName] = newSymbTbl
		self.currScope = pScope + "." + funcName
		if functype == 'function' or functype =='constructor':
			self.currFunc = pScope + "." + funcName
			self.mainSymbTbl[self.currClass]['functions'][funcName] = { 'name' : pScope + "." + funcName }
		return self.currScope
		# TAC.generateFuncTac(self.currFunc)

	def addNewIdentifier(self, identifier,type):
		tempScope = self.mainSymbTbl[self.currScope]['identifier']
		width = 0 
		
		if type in ['boolean', 'char']:
			width = 1
		elif type == 'int':
			width = 4
		elif type in ['float', 'double']:
			width = 8
		elif type in ['FUNCTION', 'CALLBACK', 'String']:
			width = 4					#address size
		else:
			width = 0
		self.mainSymbTbl[self.currScope]['offset'] +=  width
		
		if not tempScope.has_key(identifier):
			tempScope[identifier] = {}
		tempScope[identifier] = {
				'width'	:	width,
				'type'	:	type,
				'offset' : self.mainSymbTbl[self.currScope]['offset']
			}	

	#insert attributes in the symbol table
	#galat hai baad mein karenege
	#\n
	#\n
	# def addAttrId(self, identifier, attrName, attrVal):
	# 	temp = self.lookup_for_id(identifier)
	# 	temp[attrName] = attrVal
	#\n
	#\n

	#get width of identifier
	def getWidth(self,type):
		if type in ['boolean', 'char']:
			width = 1
		elif type == 'int':
			width = 4
		elif type in ['float', 'double']:
			width = 8
		elif type in ['FUNCTION', 'CALLBACK', 'String']:
			width = 4					#address size
		else:
			width = 0
		return width
	#add attributes to the current scopeLen
	def addAttrScope(self, attrName, attrVal):
		self.mainSymbTbl[self.currScope][attrName] = attrVal

	def getAttrScope(self, attrName):
		tempScope = self.mainSymbTbl[self.currScope]
		return tempScope[attrName]

	def getIdAttr(self, identifier, attrName):
		idEntry = self.lookup_for_id(identifier)
		if not idEntry :
			raise Exception("Variable "+identifier+" not declared before use")
			return None
		elif idEntry.has_key(attrName):
			return idEntry[attrName]
		else:
			raise Exception("Variable "+identifier+" not declared before use")
			return None

	#check for existence of an identifier in current scope
	def existCurrScope(self, identifier):
		existence = self.mainSymbTbl[self.currScope]['identifier'].get(identifier, 0)
		return existence

	def change_scope(self):
		# print self.currScope, self.currFunc, True 
		# if self.currScope == self.currFunc :
		self.currScope = self.mainSymbTbl[self.currScope]['pscope']
		return self.currScope

	def getTemp(self):
		temp = "_t" + str(self.tempCount)
		self.tempCount += 1
		return temp

	#switch

	def addbrkVar(self, variable):
		temp = {
			'val' : variable,
			'brklist' : [],
			'caselist': []
		}
		self.switchList.append(temp)
	
	def addInbrklist(self, address):
		self.switchList[-1]['brklist'].append(address)

	def addIncaselist(self,address):
		self.switchList[-1]['caselist'].append(address)

	def getLastCaseAddr(self):
		if len(self.switchList[-1]['caselist']) :
			return self.switchList[-1]['caselist'][-1]
		else:
			return None
	def remLastCAse(self):
		if len(self.switchList[-1]['caselist']) :
			del self.switchList[-1]['caselist'][-1]

	def getbrkList(self):
		return self.switchList[-1]['brklist']

	def getListVar(self):
		return self.switchList[-1]['val']

	def printswitch(self):
		pprint.pprint(self.switchList)