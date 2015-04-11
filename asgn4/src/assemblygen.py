#! /usr/bin/python
import assemblyCode as AssemblyCode
from parser_yacc import runParser
import sys
import pprint

def getOffset(temp, Function, ST):
	if temp[0] == '_':
		offset = ST.mainSymbTbl[Function]['temp'][temp]['offset']
	else:
		offset = ST.mainSymbTbl[Function]['identifier'][temp]['offset']
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
	ST, TAC = runParser(inputfile)
	AC = AssemblyCode.AssemblyCode(ST,TAC)
	# ST.printSymbTbl()
	TAC.printTAC()
	label = insertLabel(ST,TAC)

	mainClass = inputfile.split('/')[-1].split('.')[0]
	mainFunction = 'Main.'+mainClass + '.main'

	AC.addNewFunc(mainFunction)
	AC.addCommand(['_start:','',''])
	lineno = -1
	for line in TAC.code[mainFunction]:
		# if line[0]:
		# 	offset = getOffset(line[0], mainFunction, ST)
		if label[mainFunction].has_key(lineno):
			AC.addCommand([label[mainFunction][lineno]+':', '', ''])
		lineno += 1

		if line[3] == 'BeginFunc':
			AC.addCommand(['subl', '$'+ str(line[2]) , '%esp'])

		if line[3] == '=':
			offset = getOffset(line[0], mainFunction, ST)
			if line[2]:
				# print line[2],'48'
				if str(line[2]).isdigit():
					AC.addCommand(['movl', '$'+ str(line[2]) , '%eax'])
			else:
				offset1 = getOffset(line[1], mainFunction, ST)
				AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
		
		if line[3] == 'PRINT':
			offset = getOffset(line[0], mainFunction, ST)
			AC.addCommand(['pushl', str(offset)+'(%esp)' , ''])
			if line[2] == 'int':
				AC.addCommand(['call','print_int',''])		
				AC.addCommand(['popl','%eax',''])	

		if line[3] == '+':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			if not line[2]:
				AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			else:
				offset2 = getOffset(line[2], mainFunction, ST)
				AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				AC.addCommand(['addl', str(offset2)+'(%esp)' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

		if line[3] == '-':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			if not line[2]:
				AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				AC.addCommand(['negl', '%eax',''])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			else:
				offset2 = getOffset(line[2], mainFunction, ST)
				AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				AC.addCommand(['subl', str(offset2)+'(%esp)' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

		if line[3] == '*':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			offset2 = getOffset(line[2], mainFunction, ST)
			AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
			AC.addCommand(['mull', str(offset2)+'(%esp)' , ''])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

		if line[3] == '/':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			offset2 = getOffset(line[2], mainFunction, ST)
			AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
			AC.addCommand(['divl', str(offset2)+'(%esp)' , ''])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

		if line[3] == '%':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			offset2 = getOffset(line[2], mainFunction, ST)
			AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
			AC.addCommand(['divl', str(offset2)+'(%esp)' , ''])
			AC.addCommand(['movl', '%edx' , str(offset)+'(%esp)'])

		if line[3] == '<=':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			offset2 = getOffset(line[2], mainFunction, ST)
			
			AC.addCommand(['movl', '$1' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
			AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
			tempLabel = AC.newLabel()
			AC.addCommand(['jle', 'Label'+str(tempLabel) , ''])
			AC.addCommand(['movl', '$0' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			AC.addCommand(['Label'+str(tempLabel)+':','',''])

		if line[3] == '>=':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			offset2 = getOffset(line[2], mainFunction, ST)
			
			AC.addCommand(['movl', '$1' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
			AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
			tempLabel = AC.newLabel()
			AC.addCommand(['jge', 'Label'+str(tempLabel) , ''])
			AC.addCommand(['movl', '$0' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			AC.addCommand(['Label'+str(tempLabel)+':','',''])

		if line[3] == '==':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			offset2 = getOffset(line[2], mainFunction, ST)
			
			AC.addCommand(['movl', '$1' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
			AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
			tempLabel = AC.newLabel()
			AC.addCommand(['je', 'Label'+str(tempLabel) , ''])
			AC.addCommand(['movl', '$0' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			AC.addCommand(['Label'+str(tempLabel)+':','',''])

		if line[3] == '>':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			offset2 = getOffset(line[2], mainFunction, ST)
			
			AC.addCommand(['movl', '$1' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
			AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
			tempLabel = AC.newLabel()
			AC.addCommand(['jg', 'Label'+str(tempLabel) , ''])
			AC.addCommand(['movl', '$0' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			AC.addCommand(['Label'+str(tempLabel)+':','',''])

		if line[3] == '<':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			offset2 = getOffset(line[2], mainFunction, ST)
			
			AC.addCommand(['movl', '$1' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
			AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
			tempLabel = AC.newLabel()
			AC.addCommand(['jl', 'Label'+str(tempLabel) , ''])
			AC.addCommand(['movl', '$0' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			AC.addCommand(['Label'+str(tempLabel)+':','',''])

		if line[3] == '!=':
			offset = getOffset(line[0], mainFunction, ST)
			offset1 = getOffset(line[1], mainFunction, ST)
			offset2 = getOffset(line[2], mainFunction, ST)
			
			AC.addCommand(['movl', '$1' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
			AC.addCommand(['cmpl', str(offset2)+'(%esp)' , '%eax'])
			tempLabel = AC.newLabel()
			AC.addCommand(['jne', 'Label'+str(tempLabel) , ''])
			AC.addCommand(['movl', '$0' , '%eax'])
			AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			AC.addCommand(['Label'+str(tempLabel)+':','',''])

		if line[3] == 'GOTO':
			if not line[1]:
				AC.addCommand(['jmp',label[mainFunction][line[2]],''])
			elif line[0] == 'IF':
				offset1 = getOffset(line[1], mainFunction, ST)
				AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				AC.addCommand(['cmpl', '$1' , '%eax'])
				AC.addCommand(['je',label[mainFunction][line[2]] , ''])
		


	# AC.printAssemblyCode()
	AC.printToFile()

if __name__ == '__main__':
	genCode(sys.argv[1])
