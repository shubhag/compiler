import pprint

class symbTbl:

	def __init__(self):
		mainSymbTbl = {
				'scope' :	'main',
				'type'	:	'function',	
				'pscope':	'main',		#parent scope
				'retype':	'undefined'
			}

		self.scopeList = [mainSymbTbl]

	#for error handling
	def printSymbTbl(self):
		pprint.pprint(self.symbTbl)

	#to get the current scope name 
	def getCurrScopeName(self):
		return self.scopeList[-1]['scope']		#get the last element of the array by -1

	def lookup_for_identifier(self, identifier):
		return self.checkscope_id(identifier, len(self.scope) - 1)

	#error in scope
	def checkscope_id(self, identifier, scopeLen):
		if scopeLen == -1 :
			return None

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
			'pscope': tempScope['scope']
			'retype': 'undefined'
		}

		self.scopeList.append(newSymbTbl)

	def addNewIdentifier(self, identifier,type):
		tempScope = self.scopeList[-1]
		width = 0 
		
		if type in ['BOOLEAN', 'CHAR']:
			width = 1
		elif type == 'INTEGER':
			width = 4
		elif type in ['FLOAT', 'DOUBLE']:
			width = 8
		elif type in ['FUNCTION', 'CALLBACK', 'STRING']:
			width = 4					#address size
		else:
			width = -1

		if tempScope.has_key(identifier):
			tempScope[identifier] = {
				'width'	:	width,
				'type'	:	type
			}	

	