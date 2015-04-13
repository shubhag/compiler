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
				'identifier' : {},
				'temp' : {}
			}
		}
		self.tempCount = 0 
		self.currScope = 'Main'
		self.switchList = []
		self.currFunc = 'Main'
		self.currClass = ''
		self.prevScope = -1
		self.mainClass = False

	def notLocalnotMainClass(self, identifier):
		tempScope = self.mainSymbTbl[self.currScope]['identifier']
		if self.mainClass == True:
			return False
		elif tempScope.has_key(identifier):
			return False
		else:
			scopename = self.mainSymbTbl[self.currScope]['pscope']
			tempScope = self.mainSymbTbl[scopename]['identifier']
			if tempScope.has_key(identifier):
				return True
			else:
				return False

	def getTypeOffset(self, identifier):
		scopename = self.mainSymbTbl[self.currScope]['pscope']
		tempScope = self.mainSymbTbl[scopename]['identifier']
		if tempScope.has_key(identifier):
			return tempScope[identifier]['type'], tempScope[identifier]['offset']
		else:
			raise Exception("Something went wrong with classes")
	def setMain(self, value):
		self.mainClass = value

	def getMain(self, value):
		return self.mainClass

	def checkExistFuncClass(self, className, funcName):
		function = self.mainSymbTbl['Main.'+className]['functions']
		if function.has_key(funcName):
			return True
		else:
			raise Exception("Invalid function call")

	def checkNumClassArgs(self,className, funcName, numArgs):
		function = self.mainSymbTbl['Main.'+className]['functions']
		if function.has_key(funcName):
			if len(function[funcName]['arglist']) != numArgs :
				raise Exception('Number of arguments passed in '+ funcName +' call not equal to that in its declration')

	def checkClassType(self,className, funcName, typeId, index):
		function = self.mainSymbTbl['Main.'+className]['functions']
		if function.has_key(funcName):
			if function[funcName]['arglist'][index]['type'] != typeId :
				raise Exception('TypeCheck Error')

	def checkClassId(self, className, identifier):
		idEntry = self.mainSymbTbl['Main.'+className]['identifier']
		if idEntry.has_key(identifier):
			return idEntry[identifier]['type'], idEntry[identifier]['offset']
		else:
			raise Exception('Variable not defined in respective class')

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

	def getReturntypeClass(self, funcName, className):
		function = self.mainSymbTbl[className]['functions']
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
			'temp' : {},
			'offset' : 0,
			'name' : funcName
		}
		self.mainSymbTbl[pScope + "." + funcName] = newSymbTbl
		self.currScope = pScope + "." + funcName
		if functype == 'function' or functype =='constructor':
			self.currFunc = pScope + "." + funcName
			self.mainSymbTbl[self.currClass]['functions'][funcName] = { 'name' : pScope + "." + funcName }
		return self.currScope

	def changeOffsetArgList(self):
		offsetFunction = self.mainSymbTbl[self.currFunc]['offset']
		pscope = self.mainSymbTbl[self.currFunc]['pscope']
		argList = self.mainSymbTbl[pscope]['functions'][self.currFunc.split('.')[-1]]['arglist']
		for arguments in reversed(argList):
			width = self.mainSymbTbl[self.currFunc]['identifier'][arguments['name']]['width']
			offsetFunction = offsetFunction + width
			self.mainSymbTbl[self.currFunc]['identifier'][arguments['name']]['offset'] = offsetFunction + 4

		if self.mainSymbTbl[self.currFunc]['temp'].has_key('_this'):
			offsetFunction = offsetFunction + 4
			# print offsetFunction , '189'
			self.mainSymbTbl[self.currFunc]['temp']['_this']['offset'] = offsetFunction + 4


	def searchForArrayArg(self, identifier ):
		pscope = self.mainSymbTbl[self.currFunc]['pscope']
		funcName = self.currFunc.split('.')[-1]
		if funcName == 'main':
			return False
		else: 
			argList = self.mainSymbTbl[pscope]['functions'][self.currFunc.split('.')[-1]]['arglist']
			for arguments in argList:
				if arguments['name'] == identifier :
					return True
			return False

	def addNewIdentifier(self, identifier,type):
		tempScope = self.mainSymbTbl[self.currScope]['identifier']
		width = 0 
		
		if type in ['boolean', 'char']:
			width = 1
		elif type in ['int','pointer']:
			width = 4
		elif type in ['float', 'double']:
			width = 8
		elif type in ['FUNCTION', 'CALLBACK', 'String']:
			width = 4					#address size
		else:
			if type.split('_')[0] == 'array':
				width = 4
			else:
				width = 0
			# width = 0
		self.mainSymbTbl[self.currScope]['offset'] +=  width
		
		if not tempScope.has_key(identifier):
			tempScope[identifier] = {}
		tempScope[identifier] = {
				'width'	:	width,
				'type'	:	type,
				'offset' : self.mainSymbTbl[self.currScope]['offset']
			}	
	def addIdentifierAttr(self, identifier, attr, val):
		tempScope = self.mainSymbTbl[self.currScope]['identifier']
		if tempScope.has_key(identifier):
			tempScope[identifier][attr] = val

	def addClassIdentifier(self, identifier, type, width):
		tempScope = self.mainSymbTbl[self.currScope]['identifier']
		self.mainSymbTbl[self.currScope]['offset'] +=  width
		if not tempScope.has_key(identifier):
			tempScope[identifier] = {}
		tempScope[identifier] = {
				'width'	:	width,
				'type'	:	type,
				'offset' : self.mainSymbTbl[self.currScope]['offset']
			}	

	def ifClass(self, className):
		cname = 'Main.'+ className;
		if not self.mainSymbTbl.has_key(cname):
			return False
		else:
			return True

	def checkForClass(self, className):
		cname = 'Main.'+ className;
		if not self.mainSymbTbl.has_key(cname):
			raise Exception("Class not defined before use")
		else:
			return self.mainSymbTbl[cname]['offset']
	#get width of identifier
	def getWidth(self,type):
		if type in ['boolean', 'char']:
			width = 1
		elif type in ['int','pointer']:
			width = 4
		elif type in ['float', 'double']:
			width = 8
		elif type in ['FUNCTION', 'CALLBACK', 'String']:
			width = 4					#address size
		else:
			if type.split('_')[0] == 'array':
				width = 4
			else:
				width = 0
		return width
	#add attributes to the current scopeLen
	def addAttrScope(self, attrName, attrVal):
		self.mainSymbTbl[self.currScope][attrName] = attrVal

	def getAttrScope(self, attrName):
		tempScope = self.mainSymbTbl[self.currScope]
		return tempScope[attrName]

	def getTypeAssembly(self, identifier, function):
		if identifier[0] == '_':
			return self.mainSymbTbl[function]['temp'][identifier]['type']
		else:	
			return self.mainSymbTbl[function]['identifier'][identifier]['type']

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
		# if self.currScope == self.currFunc :
		self.currScope = self.mainSymbTbl[self.currScope]['pscope']
		return self.currScope

	def getTemp(self):
		temp = "_t" + str(self.tempCount)
		self.tempCount += 1
		return temp

	def addTempAttr(self, temporary, type):
		tempScope = self.mainSymbTbl[self.currFunc]['temp']
		width = 0 
		
		if type in ['boolean', 'char']:
			width = 1
		elif type in ['int','pointer']:
			width = 4
		elif type in ['float', 'double']:
			width = 8
		elif type in ['FUNCTION', 'CALLBACK', 'String']:
			width = 4					#address size
		else:
			if type.split('_')[0] == 'array':
				width = 4
			else:
				width = 0

		self.mainSymbTbl[self.currFunc]['offset'] +=  width
		
		if not tempScope.has_key(temporary):
			tempScope[temporary] = {}
		tempScope[temporary] = {
				'width'	:	width,
				'type'	:	type,
				'offset' : self.mainSymbTbl[self.currFunc]['offset']
			}	

	def changeWidth(self, identifier, arrWidth):
		tempScope = self.mainSymbTbl[self.currScope]['identifier']
		self.mainSymbTbl[self.currScope]['offset'] +=  arrWidth
		if tempScope.has_key(identifier):
			tempScope[identifier]['width'] = arrWidth
			tempScope[identifier]['offset'] = self.mainSymbTbl[self.currScope]['offset']

	def addTempArrayAttr(self, temporary, arrWidth, type):
		tempScope = self.mainSymbTbl[self.currFunc]['temp']
		width = arrWidth

		self.mainSymbTbl[self.currFunc]['offset'] +=  width
		
		if not tempScope.has_key(temporary):
			tempScope[temporary] = {}
		tempScope[temporary] = {
				'width'	:	width,
				'type'	:	type,
				'offset' : self.mainSymbTbl[self.currFunc]['offset']
			}	
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

	def getcaseList(self):
		return self.switchList[-1]['caselist']

	def getListVar(self):
		return self.switchList[-1]['val']

	def printswitch(self):
		pprint.pprint(self.switchList)

	def deleteList(self):
		del self.switchList[-1]