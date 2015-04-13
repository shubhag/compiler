import pprint
class threeAddressCode:
	def __init__(self, ST):
		self.code = {'Main': []}
		self.instr = {'Main': -2}
		self.nextInstr = {'Main': -1}
		self.ST = ST

	def printTAC(self):
		# pprint.pprint(self.code)
		for function in self.code:
			if len(self.code[function]) :
				pprint.pprint(function + " :")
				lineno = -1
				for taccode in self.code[function]:
					print(str(lineno) + ":\t"+str(taccode[0]) + '\t' + str(taccode[1]) + '\t' + str(taccode[2]) + '\t' + str(taccode[3]) )
					lineno += 1

	def printSymbTbl(self):
		self.ST.printSymbTbl()

	def addendAtStart(self):
		offset = self.ST.mainSymbTbl[self.ST.currScope]['offset']
		currScope = self.ST.currFunc
		self.incInstr()
		self.code[currScope].insert(0, ['','',offset,'BeginFunc'])

	def getNextInstr(self):
		return self.nextInstr[self.ST.currFunc]

	def incInstr(self):
		currScope = self.ST.currFunc
		self.instr[currScope] = self.nextInstr[currScope]
		self.nextInstr[currScope] += 1 ;

	def getLengthInstr(self, funcName):
		return self.instr[funcName]

	#emit code for an instruction
	def emit(self, destReg, srcReg1, srcReg2, op):
		currScope = self.ST.currFunc
		self.incInstr()
		self.code[currScope].append([destReg, srcReg1, srcReg2, op])

	def genNewTacFunc(self, funcName):
		self.instr[funcName] = -2
		self.nextInstr[funcName] = -1
		self.code[funcName] = []

	def merge(self, list1, list2):
		list2.extend(list1)
		return list2

	def backPatch(self, lList, loc):
		currScope = self.ST.currFunc
		for pos in lList:
			self.code[currScope][pos][2] = loc

	def generateFuncTac(self,funcName):
		self.code[funcName] =  []
		self.instr[funcName] =  -1
		self.nextInstr[funcName] = 0 