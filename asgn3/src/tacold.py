import pprint
class threeAddressCode:
	def __init__(self, ST):
		self.code = {'Main': []}
		self.instr = {'Main': -1}
		self.nextInstr = {'Main': 0}
		self.ST = ST

	def printTAC(self):
		pprint.pprint(self.code)

	def printSymbTbl(self):
		self.ST.printSymbTbl()

	def getNextInstr(self):
		return self.nextInstr[self.ST.getCurrScopeName()]

	def incInstr(self):
		currScope = self.ST.getCurrScopeName()
		self.instr[currScope] = self.nextInstr[currScope]
		self.nextInstr[currScope] += 1 ;

	def getLengthInstr(self, funcName):
		return self.instr[funcName]

	#emit code for an instruction
	def emit(self, destReg, srcReg1, srcReg2, op):
		currScope = self.ST.getCurrScopeName()
		self.incInstr()
		self.code[currScope].append([destReg, srcReg1, srcReg2, op])

	def genNewTacFunc(self, funcName):
		self.instr[funcName] = -1
		self.nextInstr[funcName] = 0
		self.code[funcName] = []

	def merge(self, list1, list2):
		list2.extend(list1)
		return list2

	# def backPatch(self, locList, location):
	# 	currScope = self.ST.getCurrScopeName()
 #        for variable in locList:
 #            self.code[currScope][variable][2] = location
	def backPatch(self, lList, loc):
		currScope = self.ST.getCurrScopeName()
		for pos in lList:
			self.code[currScope][pos][2] = loc
