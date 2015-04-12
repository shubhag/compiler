#! /usr/bin/python
import assemblyCode as AssemblyCode
from parser_yacc import runParser
import sys
import pprint

def getOffset(temp, Function, ST):
	# print temp,'8'
	if temp[0] == '_':
		# print '\n', temp,'\n'
		# print ST.mainSymbTbl[Function]['temp'], "9"
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
		for line in TAC.code[function]:
			# if line[0]:
			# 	offset = getOffset(line[0], function, ST)
			if label[function].has_key(lineno):
				AC.addCommand([label[function][lineno]+':', '', ''])
			lineno += 1

			if line[3] == 'BeginFunc':
				if function != mainFunction:
					AC.addCommand(['pushl', '%ebp' , ''])
					AC.addCommand(['movl', '%esp','%ebp'])

	
				AC.addCommand(['subl', '$'+ str(line[2]) , '%esp'])

			if line[3] == 'EndFunc':
				AC.addCommand(['jmp', 'exit' , ''])

			if line[3] == '=':
				offset = getOffset(line[0], function, ST)
				if line[2]:
					if str(line[2]).isdigit():
						AC.addCommand(['movl', '$'+ str(line[2]) , '%eax'])
					else:
						AC.addCommand(['movl', '$'+ str(line[2]) , '%eax'])
				else:
					offset1 = getOffset(line[1], function, ST)
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
			
			if line[3] == 'PRINT':
				offset = getOffset(line[0], function, ST)
				if line[2] == 'int':
					AC.addCommand(['pushl', str(offset)+'(%esp)' , ''])
					AC.addCommand(['call','print_int',''])		
					AC.addCommand(['popl','%eax',''])	
				elif line[2] == 'pointer':
					AC.addCommand(['movl', str(offset)+'(%esp)' , '%eax'])
					AC.addCommand(['pushl', '(%eax)' , ''])
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
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
					AC.addCommand(['addl', str(offset2)+'(%esp)' , '%eax'])
					AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			if line[3] == '-':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				if not line[2]:
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
					AC.addCommand(['negl', '%eax',''])
					AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])
				else:
					offset2 = getOffset(line[2], function, ST)
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
					AC.addCommand(['subl', str(offset2)+'(%esp)' , '%eax'])
					AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			if line[3] == '*':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				if str(line[2]).isdigit():
					AC.addCommand(['imull', '$'+str(line[2]) , '%eax'])
				else:
					offset2 = getOffset(line[2], function, ST)
					AC.addCommand(['mull', str(offset2)+'(%esp)' , ''])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			if line[3] == '/':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				AC.addCommand(['divl', str(offset2)+'(%esp)' , ''])
				AC.addCommand(['movl', '%eax' , str(offset)+'(%esp)'])

			if line[3] == '%':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
				AC.addCommand(['divl', str(offset2)+'(%esp)' , ''])
				AC.addCommand(['movl', '%edx' , str(offset)+'(%esp)'])

			if line[3] == '<=':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
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
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
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
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
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
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
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
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
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
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				
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
					AC.addCommand(['jmp',label[function][line[2]],''])
				elif line[0] == 'IF':
					offset1 = getOffset(line[1], function, ST)
					AC.addCommand(['movl', str(offset1)+'(%esp)' , '%eax'])
					AC.addCommand(['cmpl', '$1' , '%eax'])
					AC.addCommand(['je',label[function][line[2]] , ''])
			
			if line[3] == 'PARAM':
				offset = getOffset(line[0], function, ST)
				AC.addCommand(['pushl', str(offset)+'(%esp)',''])

			if line[3] == 'CALL':
				if line[0] != '_ALLOC':
					# AC.addCommand(['pushl', '$'+str(line[1]),''])
					AC.addCommand(['call', line[0] ,''])
					offset2 = getOffset(line[2], function, ST)
					AC.addCommand(['addl', '$'+ str(line[1]) , '%esp'])
					AC.addCommand(['movl', '%eax' ,str(offset2)+'(%esp)' ])

			if line[3] == 'RETURN':
				offset = getOffset(line[0], function, ST)
				AC.addCommand(['movl', str(offset)+'(%esp)', '%eax' ])
				
				AC.addCommand(['addl', '$'+ str(TAC.code[function][0][2]), '%esp'])
				AC.addCommand(['popl', '%ebp', '' ])
				AC.addCommand(['ret', '', '' ])

			if line[3] == '+*':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				offset2 = getOffset(line[2], function, ST)
				AC.addCommand(['movl','$'+str(offset1), '%eax'])
				AC.addCommand(['subl',str(offset2)+'(%esp)', '%eax'])
				AC.addCommand(['addl','%esp', '%eax'])
				AC.addCommand(['movl','%eax', str(offset)+'(%esp)'])

			if line[3] == '=*':
				offset = getOffset(line[0], function, ST)
				offset1 = getOffset(line[1], function, ST)
				AC.addCommand(['movl',str(offset)+'(%esp)', '%ebx'])
				AC.addCommand(['movl','%eax', '(%ebx)'])




	# AC.printAssemblyCode()
	AC.printToFile()

if __name__ == '__main__':
	genCode(sys.argv[1])
