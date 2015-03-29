import pprint

class symbTbl:

	def __init__(self):
		mainSymbTbl = {
				'scope' :	'Main',
				'type'	:	'function',	
				'pscope':	'Main',		#parent scope
				'retype':	'undefined'
			}
		self.tempCount = 0 
		self.scopeList = [mainSymbTbl]

	#for error handling
	def printSymbTbl(self):
		pprint.pprint(self.scopeList)

	#to get the current scope name 
	def getCurrScopeName(self):
		return self.scopeList[-1]['scope']		#get the last element of the array by -1

	def lookup_for_identifier(self, identifier):
		idEntry = self.checkscope_id(identifier, len(self.scopeList) - 1)
		if idEntry!= None : 
			return True
		else:
			return False

	def lookup_for_id(self, identifier):
		idEntry = self.checkscope_id(identifier, len(self.scopeList) - 1)
		return idEntry

	#error in scope
	def checkscope_id(self, identifier, scopeLen):
		if scopeLen == -1 :
			return None
		print identifier
		# print self.scopeList[scopeLen][identifier]
		tempScope = self.scopeList[scopeLen]
		if tempScope.has_key(identifier):
			return tempScope[identifier]
		else:
			return self.checkscope_id(identifier, tempScope - 1)

	def addNewScope(self, funcName):
		tempScope = self.scopeList[-1]

		newSymbTbl = {
			'scope'	: funcName,
			'type'	: 'function',
			'pscope' : tempScope['scope'],
			'retype' : 'undefined'
		}

		self.scopeList.append(newSymbTbl)

	def addNewIdentifier(self, identifier,type):
		tempScope = self.scopeList[-1]
		width = 0 
		
		if type in ['bool', 'char']:
			width = 1
		elif type == 'int':
			width = 4
		elif type in ['float', 'double']:
			width = 8
		elif type in ['FUNCTION', 'CALLBACK', 'String']:
			width = 4					#address size
		else:
			width = -1

		if not tempScope.has_key(identifier):
			tempScope[identifier] = {}
		tempScope[identifier] = {
				'width'	:	width,
				'type'	:	type
			}	

	#insert attributes in the symbol table
	def addAttrId(self, identifier, attrName, attrVal):
		temp = self.lookup_for_identifier(identifier)
		temp[attrName] = attrVal

	#add attributes to the current scopeLen
	def addAttrScope(self, attrName, attrVal):
		tempScope = self.scopeList[-1]
		tempScope[attrName] = attrVal

	def getAttrScope(self, attrName):
		tempScope = self.scopeList[-1]
		return tempScope[attrName]

	def getIdAttr(self, identifier, attrName):
		idEntry = self.lookup_for_id(identifier)
		if idEntry.has_key(attrName):
			return idEntry[attrName]
		else:
			return None

	#check for existence of an identifier in current scope
	def existCurrScope(self, identifier):
		existence = self.scopeList[-1].get(identifier, 0)
		return existence

	def getTemp(self):
		temp = "_t" + str(self.tempCount)
		self.tempCount += 1
		return temp

	def delScope(self, function):
		del self.scopeList[-1]

	def addNewScope(self, name, scopeType):
		tempSymbTbl = {
				'scope' :	name,
				'type'	:	scopeType,	
				'pscope':	self.scopeList[-1]['scope'],		#parent scope
				'retype':	'undefined'
			}
		self.scopeList.append(tempSymbTbl)