import pprint
class AssemblyCode:
	def __init__(self, symbolTable, threeAddressCode):
		self.code = {}
		self.ST =symbolTable
		self.TAC = threeAddressCode
		self.currFunction = ''
		self.registerCount = 4
		self.label = 0
		self.addrDescriptor = {}
		self.resetReg()

	def addCommand(self, command):
		self.code[self.currFunction].append(command)

	def addNewFunc(self, funcName):
		self.currFunction = funcName
		self.code[funcName] = []


	def printAssemblyCode(self):
		pprint.pprint(self.code)

	def printToFile(self):
		f = open('code.s','w')
		f.write('.section .data\n')
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
	
	def resetReg(self):
		self.regDetail = {
			# 'eax' : None,
			'ebx' : None,
			'ecx' : None,
			'edx' : None,
			'esi' : None,
			'edi' : None
		}
		self.freeRegister = []
		self.usedRegister = []
		for register in self.regDetail:
			self.freeRegister.append(register)

	def addInAddrDescriptor(self, function, ST):
		self.addrDescriptor = {}
		temporary = ST.getIdentifiers(function)
		for identifier in temporary:
			self.addrDescriptor[identifier] = None

		print self.addrDescriptor

	# def getRegister(self, temporary):
	# 	if temporary in self.regDetail.values():
	# 		register = self.addrDescriptor[temporary]
	# 		return register
	# 	else:
	# 		if len(self.freeRegister):
	# 			register = self.freeRegister.pop()

			
