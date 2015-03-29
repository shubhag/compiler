class threeAddressCode:
	def __init__(self, ST):
		self.code = {'main': []}
		self.instr = {'main': -1}
		self.nextInstr = {'main': 0}

	def printSymbTbl(self):
		ST.printSymbTbl()

	def getNextInstr(self):
		return self.nextInstr[ST.getCurrScopeName()]

	def incInstr(self):
		currScope = ST.getCurrScopeName()
		self.instr[currScope] = self.nextInstr[currScope]
		self.nextInstr[currScope] += 1 ;

	def getLengthInstr(self, funcName):
		return self.instr[funcName]

	#emit code for an instruction
	def emit(self, destReg, srcReg1, srcReg2, op):
		currScope = ST.getCurrScopeName()
		self.incInstr()
		self.code[currScope].append([destReg, srcReg1, srcReg2, op])

	def genNewTacFunc(self, funcName):
		self.instr[funcName] = -1
		self.nextInstr[funcName] = 0
		self.code[funcName] = []

	def mergeLists(self, list1, list2):
		list2.extend(list1)
		return list2

	


