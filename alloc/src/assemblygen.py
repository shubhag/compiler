#! /usr/bin/python
import assemblyCode as AssemblyCode
from parser_yacc import runParser
import sys
import pprint

def getRegister(temporary, function, ST, AC):
	if temporary in AC.regDetail.values():
		register = AC.addrDescriptor[temporary]
	else:
		offset = getOffset(temporary, function, ST)
		if len(AC.freeRegister):
			register = AC.freeRegister.pop()
		else:
			register = AC.usedRegister.pop(0)
			temp = AC.regDetail[register] 
			offTemp = getOffset(temp, function, ST)
			AC.addCommand(['movl', '%'+register ,str(offTemp)+'(%esp)'])
			AC.addrDescriptor[temp] = None

		AC.addCommand(['movl', str(offset)+'(%esp)' , '%'+register])
		AC.addrDescriptor[temporary] = register
		AC.usedRegister.append(register)
		AC.regDetail[register] = temporary
	return register

def getRegisterWithoutTemp(function, ST, AC):
	if len(AC.freeRegister):
		register = AC.freeRegister.pop()
	else:
		register = AC.usedRegister.pop(0)
		temp = AC.regDetail[register] 
		offTemp = getOffset(temp, function, ST)
		AC.addCommand(['movl', '%'+register ,str(offTemp)+'(%esp)'])
		AC.addrDescriptor[temp] = None
	return register

def flushReg(temporary, function, ST, AC):
	if temporary in AC.regDetail.values():
		register = AC.addrDescriptor[temporary]
		offTemp = getOffset(temp, function, ST)
		AC.addCommand(['movl', '%'+register ,str(offTemp)+'(%esp)'])
		AC.addrDescriptor[temp] = None
		AC.freeRegister.append(register)
		del AC.usedRegister[AC.usedRegister.index(register)]
		AC.regDetail[register] = None

def flushAll(function, ST, AC):
	for register in AC.regDetail:
		temporary = AC.regDetail[register]
		if temporary!= None:
			flushReg(temporary, function, ST, TAC)

def getOffset(temp, Function, ST):
	global count
	# print temp,'8'
	if temp[0] == '_' or temp[0] == '*':
		# print '\n', temp,'\n'
		# print ST.mainSymbTbl[Function]['temp'], "9"
		offset = ST.mainSymbTbl[Function]['temp'][temp]['offset'] + count * 4
	else:
		offset = ST.mainSymbTbl[Function]['identifier'][temp]['offset'] + count * 4
	return offset

def insertLabel(ST, TAC):
	labelCount = 0;
	label = {}
	for function in TAC.code :
		label[function] = {}
		for line in TAC.code[function]:
			if line[3] == 'GOTO':
				if not label[function].has_key(line[2]):
					label[function][line[2]] = 'LabelGoto'+str(labelCount)
					labelCount += 1
	return label

def genCode(inputfile):
	global count
	ST, TAC = runParser(inputfile)
	AC = AssemblyCode.AssemblyCode(ST,TAC)
	ST.printSymbTbl()
	TAC.printTAC()
	label = insertLabel(ST,TAC)

	mainClass = inputfile.split('/')[-1].split('.')[0]
	mainFunction = 'Main.'+mainClass + '.main'

	for function in TAC.code:
		if (function == mainFunction):
			AC.addNewFunc(mainFunction)
			AC.addCommand(['\n','',''])
			AC.addCommand(['_start:','',''])

		elif(len(function.split('.')) == 3):
			AC.addNewFunc(function)
			# funcName = function.split('.')[-1]
			AC.addCommand(['\n','',''])
			AC.addCommand([function+':','',''])
			# AC.addCommand(['jmp','exit',''])
			# continue

		else:
			continue


		lineno = -1
		count = 0
		for line in TAC.code[function]:
			# if line[0]:
			# 	offset = getOffset(line[0], function, ST)
			if label[function].has_key(lineno):
				AC.addCommand([label[function][lineno]+':', '', ''])
			lineno += 1

			if line[3] == 'BeginFunc':
				# if function != mainFunction:
				AC.addCommand(['pushl', '%ebp' , ''])
				AC.addCommand(['movl', '%esp','%ebp'])
				# count += 1
	
				AC.addCommand(['subl', '$'+ str(line[2]) , '%esp'])

			if line[3] == 'EndFunc':
				AC.addCommand(['popl', '%ebp' , ''])
				AC.addCommand(['jmp', 'exit' , ''])
				# count -= 	1

			if line[3] == '=':
				offset = getOffset(line[0], function, ST)
				if line[2]:

					if str(line[2]).isdigit():
						AC.addCommand(['movl', '$'+ str(line[2]) , '%eax'])
					else:
						AC.addCommand(['movl', '$'+ str(line[2]) , '%eax'])
				else:
					offset1 = getOffset(line[1], function, ST)
					if line[1][0] == '*':
						register = getRegister(line[1], function, ST, AC)
						# AC.addCommand(['movl', str(offset1)+'(%esp)' , '%'+register])
						AC.addCommand(['movl', '(%'+register+')' , '%eax'])
					else:	
						AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				if line[0][0] == '*':
					register = getRegister(line[0], function, ST, AC)
					# AC.addCommand(['movl', str(offset)+'(%esp)', '%ebx'])
					AC.addCommand(['movl', '%eax' , '(%'+register+')'])
				else:
					AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			
			if line[3] == 'PRINT':
				offset = getOffset(line[0], function, ST)
				if line[2] == 'int':
					if (line[0][0] == '*'):
						register = getRegister(line[0], function, ST, AC)
						# AC.addCommand(['movl', str(offset)+'(%esp)' , '%ebx'])
						AC.addCommand(['pushl', '(%'+register+')' , ''])
					else:
						AC.addCommand(['pushl', str(offset)+'(%esp)' , ''])
					AC.addCommand(['call','print_int',''])		
					AC.addCommand(['popl','%eax',''])	

			if line[3] == '+':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				if not line[2]:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
					AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				else:
					offset2 = getOffset(line[2], function, ST)
					if line[1][0] == '*':
						register1 = getRegister(line[1], function, ST, AC)
						# AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
						AC.addCommand(['movl', '(%'+register1+')' , '%eax'])
					else:
						AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])

					if line[2][0] == '*': 
						register2 = getRegister(line[2], function, ST, AC)
						# AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
						AC.addCommand(['addl', '(%'+register2+')' , '%eax'])
					else:
						AC.addCommand(['addl', str(offset2)+'(%esp)' , '%eax'])
					
					if line[0][0] == '*':
						register = getRegister(line[0], function, ST, AC)
						# AC.addCommand(['movl', str(offset)+'(%esp)', '%ebx'])
						AC.addCommand(['movl', '%eax' , '(%'+register+')'])					
					else:
						AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			if line[3] == '-':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				if not line[2]:
					register1 = getRegister(line[1], function, ST, AC)
					# AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
					AC.addCommand(['negl', '%'+register1,''])
					AC.addCommand(['movl', '%'+register1 , str(offset)+'(%esp)'])
				else:
					offset2 = getOffset(line[2], function, ST)
					if line[1][0] == '*':
						register1 = getRegister(line[1], function, ST, AC)
						# AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
						AC.addCommand(['movl', '(%'+register1+')' , '%eax'])
					else:
						AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])

					if line[2][0] == '*': 
						AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
						AC.addCommand(['subl', '(%ebx)' , '%eax'])
					else:
						AC.addCommand(['subl', str(offset2)+'(%esp)' , '%eax'])
					
					if line[0][0] == '*':
						AC.addCommand(['movl', str(offset)+'(%esp)', '%ebx'])
						AC.addCommand(['movl', '%eax' , '(%ebx)'])					
					else:
						AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			if line[3] == '*':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				if line[1][0] == '*':
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
					AC.addCommand(['movl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])

				if str(line[2]).isdigit():
					AC.addCommand(['imull', '$'+str(line[2]) , '%eax'])
				else:
					offset2 = getOffset(line[2], function, ST)
					if line[2][0] == '*': 
						AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
						AC.addCommand(['mull', '(%ebx)' , ''])
					else:
						AC.addCommand(['mull', str(offset2)+'(%esp)' , ''])

				if line[0][0] == '*':
					AC.addCommand(['movl', str(offset)+'(%esp)', '%ebx'])
					AC.addCommand(['movl', '%eax' , '(%ebx)'])					
				else:
					AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			if line[3] == '/':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				AC.addCommand(['movl', '$0', '%edx'])
				
				if line[1][0] == '*':
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
					AC.addCommand(['movl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				
				if line[2][0] == '*': 
					AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
					AC.addCommand(['divl', '(%ebx)' , ''])
				else:
					AC.addCommand(['divl', str(offset2)+'(%esp)' , ''])

				if line[0][0] == '*':
					AC.addCommand(['movl', str(offset)+'(%esp)', '%ebx'])
					AC.addCommand(['movl', '%eax' , '(%ebx)'])					
				else:
					AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			if line[3] == '%':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				AC.addCommand(['movl', '$0', '%edx'])

				if line[1][0] == '*':
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
					AC.addCommand(['movl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				
				if line[2][0] == '*': 
					AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
					AC.addCommand(['divl', '(%ebx)' , ''])
				else:
					AC.addCommand(['divl', str(offset2)+'(%esp)' , ''])

				if line[0][0] == '*':
					AC.addCommand(['movl', str(offset)+'(%esp)', '%ebx'])
					AC.addCommand(['movl', '%edx' , '(%ebx)'])					
				else:
					AC.addCommand(['movl', '%edx' , str(offset)+'(%esp)'])

			if line[3] == '<=':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
				AC.addCommand(['movl', '$1' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				if line[1][0] == '*':
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
					AC.addCommand(['movl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])

				if line[2][0] == '*': 
					AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
					AC.addCommand(['cmpl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
				tempLabel = AC.newLabel()
				AC.addCommand(['jle', 'Label'+str(tempLabel) , ''])
				AC.addCommand(['movl', '$0' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				AC.addCommand(['Label'+str(tempLabel)+':','',''])

			if line[3] == '>=':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
				AC.addCommand(['movl', '$1' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				if line[1][0] == '*':
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
					AC.addCommand(['movl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])

				if line[2][0] == '*': 
					AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
					AC.addCommand(['cmpl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
				tempLabel = AC.newLabel()
				AC.addCommand(['jge', 'Label'+str(tempLabel) , ''])
				AC.addCommand(['movl', '$0' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				AC.addCommand(['Label'+str(tempLabel)+':','',''])

			if line[3] == '==':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
				AC.addCommand(['movl', '$1' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				if line[1][0] == '*':
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
					AC.addCommand(['movl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])

				if line[2][0] == '*': 
					AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
					AC.addCommand(['cmpl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
				tempLabel = AC.newLabel()
				AC.addCommand(['je', 'Label'+str(tempLabel) , ''])
				AC.addCommand(['movl', '$0' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				AC.addCommand(['Label'+str(tempLabel)+':','',''])

			if line[3] == '>':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
				AC.addCommand(['movl', '$1' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				if line[1][0] == '*':
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
					AC.addCommand(['movl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])

				if line[2][0] == '*': 
					AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
					AC.addCommand(['cmpl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
				tempLabel = AC.newLabel()
				AC.addCommand(['jg', 'Label'+str(tempLabel) , ''])
				AC.addCommand(['movl', '$0' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				AC.addCommand(['Label'+str(tempLabel)+':','',''])

			if line[3] == '<':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
				AC.addCommand(['movl', '$1' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				if line[1][0] == '*':
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
					AC.addCommand(['movl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])

				if line[2][0] == '*': 
					AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
					AC.addCommand(['cmpl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
				tempLabel = AC.newLabel()
				AC.addCommand(['jl', 'Label'+str(tempLabel) , ''])
				AC.addCommand(['movl', '$0' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				AC.addCommand(['Label'+str(tempLabel)+':','',''])

			if line[3] == '!=':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
				AC.addCommand(['movl', '$1' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				if line[1][0] == '*':
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%ebx'])
					AC.addCommand(['movl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])

				if line[2][0] == '*': 
					AC.addCommand(['movl', str(offset2)+'(%esp)' , '%ebx'])
					AC.addCommand(['cmpl', '(%ebx)' , '%eax'])
				else:
					AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
				tempLabel = AC.newLabel()
				AC.addCommand(['jne', 'Label'+str(tempLabel) , ''])
				AC.addCommand(['movl', '$0' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				AC.addCommand(['Label'+str(tempLabel)+':','',''])

			if line[3] == 'GOTO':
				if not line[1]:
					AC.addCommand(['jmp',label[function][line[2]],''])
				elif line[0] == 'IF':
					offset1 = getOffset(line[1], function, ST)
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
					AC.addCommand(['cmpl', '$1' , '%eax'])
					AC.addCommand(['je',label[function][line[2]] , ''])
			
			if line[3] == 'PARAM':
				offset = getOffset(line[0], function, ST)
				typeId = ST.getTypeAssembly(line[0], function)
				if line[0][0] == '*' or ST.ifClassArray(typeId):
					# AC.addCommand(['movl', str(offset)+'(%esp)', '%ebx'])
					# AC.addCommand(['pushl','(%ebx)','']) 
					if function == mainFunction:
						AC.addCommand(['movl', '%esp', '%eax'])
						AC.addCommand(['addl', '$'+str(offset),'%eax'])	
						AC.addCommand(['pushl','%eax',''])
					else:
						AC.addCommand(['pushl', str(offset)+'(%esp)',''])
				else:
					AC.addCommand(['pushl', str(offset)+'(%esp)',''])
				count += 1

			if line[3] == 'CALL':
				if line[0] != '_ALLOC':
					# AC.addCommand(['pushl', '$'+str(line[1]),''])
					AC.addCommand(['call', line[0] ,''])
					AC.addCommand(['addl', '$'+ str(line[1]) , '%esp'])
					count -= int(line[1])/4
					offset2 = getOffset(line[2], function, ST)
					AC.addCommand(['movl', '%eax' ,str(offset2)+'(%esp)' ])

			if line[3] == 'RETURN':
				offset = getOffset(line[0], function, ST)
				AC.addCommand(['movl', str(offset)+'(%esp)', '%eax' ])
				if line[0][0] == '*':
					AC.addCommand(['movl','(%eax)','%eax'])	
				
				AC.addCommand(['addl', '$'+ str(TAC.code[function][0][2]), '%esp'])
				AC.addCommand(['popl', '%ebp', '' ])
				AC.addCommand(['ret', '', '' ])
				# count -= 1
				# count -= int(TAC.code[function][0][2])/4

			if line[3] == '+*':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				AC.addCommand(['movl','$'+str(offset1), '%eax'])
				AC.addCommand(['subl',str(offset2)+'(%esp)', '%eax'])
				AC.addCommand(['addl','%esp', '%eax'])
				AC.addCommand(['movl','%eax', str(offset)+'(%esp)'])

			if line[3] == '_*':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				AC.addCommand(['movl',str(offset1)+'(%esp)', '%eax'])
				AC.addCommand(['subl', '$'+str(line[2]), '%eax'])
				AC.addCommand(['movl','%eax', str(offset)+'(%esp)'])

			if line[3] == '-*':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				AC.addCommand(['movl','$'+str(offset1), '%eax'])
				AC.addCommand(['subl','$'+str(line[2]), '%eax'])
				AC.addCommand(['addl','%esp', '%eax'])
				AC.addCommand(['movl','%eax', str(offset)+'(%esp)'])

			if line[3] == '*.':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				AC.addCommand(['movl',str(offset1)+'(%esp)', '%eax'])
				AC.addCommand(['subl',str(offset2)+'(%esp)', '%eax'])
				AC.addCommand(['movl','%eax', str(offset)+'(%esp)'])




	# AC.printAssemblyCode()
	AC.printToFile()

if __name__ == '__main__':
	count = 0
	genCode(sys.argv[1])
