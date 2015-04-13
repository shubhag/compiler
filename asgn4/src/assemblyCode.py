import pprint
class AssemblyCode:
	def __init__(self, symbolTable, threeAddressCode):
		self.code = {}
		self.string = []
		self.ST =symbolTable
		self.TAC = threeAddressCode
		self.currFunction = ''
		self.registerCount = 1
		self.label = 0
		self.resetReg()

	def addCommand(self, command):
		self.code[self.currFunction].append(command)

	def addNewFunc(self, funcName):
		self.currFunction = funcName
		self.code[funcName] = []

	def resetReg(self):
		self.regDetail = {
			'$t0' : None
		}
		self.freeRegister = []
		self.usedRegister = []
		for register in self.regDetail:
			self.freeRegister.append(register)

	def printAssemblyCode(self):
		pprint.pprint(self.code)

	def printToFile(self):
		f = open('code.s','w')
		f.write('.section .data\n')
		for line in self.string:
			if line[1]:
				f.write(str(line[0]) + ' ' + str(line[1]) +'\n')
			else:
				f.write(str(line[0])+'\n')

		f.write('.section .text\n')
		f.write('.globl _start\n')
		for function in self.code:
			if len(self.code[function]) :
				for line in self.code[function]:
					if line[2]:
						f.write(str(line[0]) + ' ' + str(line[1]) + ', ' + str(line[2]) +'\n')
					else:
						f.write(str(line[0]) + ' ' + str(line[1]) + '\n')
		f.write('exit:\n')
		f.write('\tmovl $1, %eax\n')
		f.write('\tmovl $0, %ebx\n')
		f.write('\tint $0x80\n')

	def newLabel(self):
		self.label += 1
		return self.label