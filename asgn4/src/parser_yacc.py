import ply.yacc as yacc, sys
import symbol as symbolTbl
import tac as tac
# Get the token map from the lexer.  This is required.
from lexer_yacc import tokens


ST = symbolTbl.symbTbl()
TAC = tac.threeAddressCode(ST)

def p_compilationunit(p):
	'''CompilationUnit : ProgramFile '''
	# ST.printSymbTbl()
	# TAC.printTAC()
	# TAC.emit('','',-1,'END')


def p_typespeciifier(p):
	'''TypeSpecifier : TypeName
					| TypeName Dims '''

	if len(p) == 2 :
		p[0] = p[1]
	else:
		p[0] = 'array_'+p[1]+'_' +str(p[2])


def p_typename(p):
	'''TypeName : PrimitiveType 
				| QualifiedName '''

	p[0] = p[1]

def p_primitivetype(p):
	'''PrimitiveType : BOOLEAN 
					| CHAR
					| BYTE
					| SHORT
					| INT
					| LONG
					| FLOAT
					| DOUBLE
					| VOID '''

	p[0] = p[1]

def p_semicolons(p):
	''' SemiColons : ';'
					| SemiColons ';' '''
	p[0] = {}

def p_programfile(p):
	'''ProgramFile : PackageStatement ImportStatements TypeDeclarations
					| PackageStatement TypeDeclarations
					| ImportStatements TypeDeclarations
					| TypeDeclarations '''


def p_packagestatement(p):
	''' PackageStatement : PACKAGE QualifiedName SemiColons'''

def p_typedeclarations(p):
	''' TypeDeclarations : TypeDeclarationOptSemi
						| TypeDeclarations TypeDeclarationOptSemi '''

def p_typedeclarationoptsemi(p):
	''' TypeDeclarationOptSemi : TypeDeclaration
    							| TypeDeclaration SemiColons '''

def p_importstms(p):
	''' ImportStatements : ImportStatement
						| ImportStatements ImportStatement '''

def p_importstatement(p):
	''' ImportStatement : IMPORT QualifiedName SemiColons
						| IMPORT QualifiedName '.' '*' SemiColons '''

def p_qualifiedname(p):
	''' QualifiedName : IDENTIFIER
					| QualifiedName '.' IDENTIFIER '''

	if len(p) == 4 :
		p[0] = p[1] + '.' + p[3]
	else:
		p[0] = p[1]
		if ST.notLocalnotMainClass(p[0]) :
			typeId, offset = ST.getTypeOffset(p[0])
			temp = ST.getTemp()
			temp = '*' + temp 
			ST.addTempAttr(temp, typeId)
			temp1 = '_this'
			ST.addTempAttr(temp1, 'int')
			TAC.emit(temp, temp1, offset, '_*')
			p[0] = {'type': typeId, 'tempVar' : temp}


def p_typedeclaration(p):
	'''TypeDeclaration : ClassHeader '{' FieldDeclarations Rparen
						| ClassHeader '{' Rparen '''


def p_classheader(p):
	'''ClassHeader :	Modifiers ClassWord IDENTIFIER
					|           ClassWord IDENTIFIER '''

	if len(p) == 3 :
		p[0] = {'mod': [], 'id': p[2] , 'class': p[1] }
	else:
		p[0] = {'mod': p[1], 'id':p[3], 'class': p[2] }

	global MainClass
	if p[0]['id'] == MainClass:
		ST.setMain(True)
	else:
		ST.setMain(False)
	funcName = ST.addNewScope(p[0]['id'], 'class')
	TAC.generateFuncTac(funcName)
	ST.chgClass(p[0]['id'])
	# TAC.genNewTacFunc()
def p_modifiers(p):
	''' Modifiers : Modifier
					| Modifiers Modifier '''

	if len(p) == 3 :
		p[1].append(p[2])
		p[0] = p[1]
	else:
		p[0] = list(p[1])

def p_modifier(p):
	'''Modifier : PUBLIC
				| PRIVATE
				| STATIC'''

	p[0] = p[1]

def p_classword(p):
	''' ClassWord : CLASS
					| INTERFACE '''
	p[0] = p[1]
# def p_interfaces(p):
# 	'''Interfaces : IMPLEMENTS ClassNameList '''

def p_fielddeclarartions(p):
	''' FieldDeclarations : FieldDeclarationOptSemi
        					| FieldDeclarations FieldDeclarationOptSemi '''

	if len(p) == 2:
		p[0] = p[1]

def p_fielddeclarationoptsemi(p):
	''' FieldDeclarationOptSemi : FieldDeclaration
        						| FieldDeclaration SemiColons '''
	
	p[0] = p[1]

def p_fielddeclaration(p):
	''' FieldDeclaration : FieldVariableDeclaration ';'
						| MethodDeclaration
						| ConstructorDeclaration
						| StaticInitializer
					    | NonStaticInitializer
				        | TypeDeclaration '''

	p[0] = p[1]

def p_fieldvariabledeclaration(p):
	'''FieldVariableDeclaration : Modifiers TypeSpecifier VariableDeclarators
								| TypeSpecifier VariableDeclarators '''

def p_variabledeclarators(p):
	'''VariableDeclarators : VariableDeclarator
							| VariableDeclarators ',' VariableDeclarator'''

	p[0] = {'type': p[-1]}

def p_variabledeclarator(p):
	''' VariableDeclarator : DeclaratorName
							| DeclaratorName '=' VariableInitializer '''

	exist = ST.existCurrScope(p[1])
	if ST.ifClass(p[-1]) :
		p[0] = {'type': p[-1], 'name': p[1]}
		if exist == 0:
			ST.addClassIdentifier(p[1],p[0]['type'], ST.checkForClass(p[-1]))
		else:
			raise Exception("Error: " + p[1] + " Redeclared")
	else:
		if p[-1] != ',':
			p[0] = {'type': p[-1], 'name': p[1]} 
		else:
			p[0] = {'type': p[-2]['type'], 'name': p[1]}
	
		if exist == 0:
			ST.addNewIdentifier(p[1],p[0]['type'])
		else:
			raise Exception("Error: " + p[1] + " Redeclared")

	if len(p) == 4:
		if type(p[3]) is not dict:
			type1 = ST.getIdAttr(p[3], 'type')
			tempVar1 = p[1]
			if type1 == 'None':
				raise Exception("Variable declared before use")
		else:
			type1 = p[3]['type']
			tempVar1 = p[3]['tempVar']

		if p[0]['type'] == type1 :
			TAC.emit(p[1],tempVar1,'','=')
			if type1.split('_')[0] == 'array':
				ST.addIdentifierAttr(p[1], 'dimension', p[3]['dimension'] )
				ST.changeWidth(p[1], p[3]['width'])
		else:
			raise Exception("Type Check in variable declaration of " + p[1])

def p_variableinitializer(p):
	'''VariableInitializer : Expression '''
							# | '{' '}'
       #  					| '{' ArrayInitializers '}' '''
  	if len(p) == 2:
  		p[0] = p[1]

def p_arrayinitializers(p):
	''' ArrayInitializers : VariableInitializer
							| ArrayInitializers ',' VariableInitializer
							| ArrayInitializers ',' '''

def p_methoddeclaration(p):
	''' MethodDeclaration : Modifiers TypeSpecifier MethodDeclarator        MethodBody
						|           TypeSpecifier MethodDeclarator        MethodBody '''

	if len(p) == 4 : 
		p[0] = {'mod': [], 'type': p[1], 'method': p[2]}
	else :
		p[0] = {'mod': p[1], 'type':p[2], 'method':p[3]}
	ST.changeOffsetArgList()

def p_methoddeclarator(p):
	'''MethodDeclarator : DeclaratorName '(' ParameterList ')'
						| DeclaratorName '(' ')' '''
	funcName = ST.addNewScope(p[1], 'function' )
	TAC.generateFuncTac(funcName)
	if len(p) == 4 : 
		p[0] = { 'name': p[1], 'plist': [] }
		ST.addArgList(p[1], None )
	else:
		p[0] = {'name': p[1], 'plist': p[3]}
		ST.addArgList(p[1], p[3] )
		for parameter in p[3] :
			ST.addNewIdentifier(parameter['name'], parameter['type'])
			if parameter['type'].split('_')[0] == 'array':
				print parameter['type']
				dimension = [0] * int(parameter['type'].split('_')[2])
				ST.addIdentifierAttr(parameter['name'], 'dimension', dimension)
	ST.addReturntype(p[1], p[-1])
	

def p_parameterlist(p):
	''' ParameterList : Parameter
						| ParameterList ',' Parameter '''

	if len(p) == 4 : 
		p[1].append(p[3])
		p[0] = p[1] 
	else:
		p[0] =[ p[1] ]

def p_parameter(p):
	'''Parameter : TypeSpecifier DeclaratorName'''

	p[0] = {'type': p[1], 'name': p[2]}

def p_declaratorname(p):
	''' DeclaratorName : IDENTIFIER
						| DeclaratorName OP_DIM '''

	if len(p) == 2:
		p[0] = p[1] 


def p_methodbody(p):
	'''MethodBody : '{' LocalVariableDeclarationsAndStatements '}'
				| '{' '}' 
					| ';' '''
	if len(p) == 3 :
		p[0] = {}
	elif len(p) == 4 :
		p[0] = p[2]
	else :
		p[0] = {}
	TAC.addendAtStart()
	TAC.emit('','','','EndFunc')
	ST.change_scope()
	


def p_constructdeclarator(p):
	''' ConstructorDeclaration : Modifiers ConstructorDeclarator '{' LocalVariableDeclarationsAndStatements '}'
								| Modifiers ConstructorDeclarator '{' '}'
								|           ConstructorDeclarator  '{' LocalVariableDeclarationsAndStatements '}'
								| ConstructorDeclarator '{' '}' '''

	TAC.addendAtStart()
	TAC.emit('','','','EndFunc')
	ST.change_scope()
	# if len(p) == 4 : 
	# 	p[0] = {'mod': p[1],  'constructor': p[2]}
	# else :
	# 	p[0] = { 'constructor':p[1]}

def p_constructordeclarator(p):
	'''ConstructorDeclarator : IDENTIFIER '(' ParameterList ')'
							| IDENTIFIER '(' ')' '''

	funcName = ST.addNewScope(p[1], 'constructor' )
	TAC.generateFuncTac(funcName)
	if len(p) == 4 : 
		p[0] = { 'name': p[1], 'plist': [] }
		ST.addArgList(p[1], None )
	else:
		p[0] = {'name': p[1], 'plist': p[3]}
		ST.addArgList(p[1], p[3] )
		for parameter in p[3] :
			ST.addNewIdentifier(parameter['name'], parameter['type'])
	# ST.addReturntype(p[1], p[-1])

def p_staticinitializer(p):
	'''StaticInitializer : STATIC Block '''

def p_nonstaticini(p):
	'''NonStaticInitializer : Block '''


def p_block(p):
	'''Block : Lparen LocalVariableDeclarationsAndStatements Rparen
				| Lparen Rparen '''

	if len(p) == 3 :
		p[0] = {}
	else:
		p[0] = p[2]
	# ST.change_scope()

def p_lparen(p):
	''' Lparen : '{' '''
	temp = ST.getTemp()
	ST.addNewScope(temp, 'if')

def p_rparen(p):
	''' Rparen : '}' '''
	ST.change_scope()

def p_LocalVariableDeclarationsAndStatements(p):
	'''LocalVariableDeclarationsAndStatements : LocalVariableDeclarationOrStatement 
											| LocalVariableDeclarationsAndStatements LocalVariableDeclarationOrStatement '''

	if len(p) == 2:
		p[0] = {
			'endOfLoop' : p[1].get('endOfLoop', []),
			'beginLoop' : p[1].get('beginLoop', [])
		}

	else:
		p[0] = {
			'endOfLoop' : TAC.merge(p[1].get('endOfLoop', []), p[2].get('endOfLoop', [])),
			'beginLoop' : TAC.merge(p[1].get('beginLoop',[]), p[2].get('beginLoop',[]))
		}
def p_LocalVariableDeclarationOrStatement(p):
	'''LocalVariableDeclarationOrStatement : LocalVariableDeclarationStatement
											| Statement '''
	p[0] = p[1]


def p_LocalVariableDeclarationStatement(p):
	''' LocalVariableDeclarationStatement : TypeSpecifier VariableDeclarators ';' M_instr '''

	p[0] = {
		# 'endOfLoop' : p[4].get('endOfLoop')
	}
	
def p_statement(p):
	'''	Statement :  EmptyStatement M_instr
				| LabelStatement M_instr
				| ExpressionStatement  ';' M_instr
			    | SelectionStatement M_instr
			   	| IterationStatement M_instr
				| JumpStatement M_instr
				| Block M_instr '''

	if type(p[1]) is not dict:
		p[1] = {}

	p[0] = {
		'endOfLoop' : p[1].get('endOfLoop', []), 
		'beginLoop': p[1].get('beginLoop', [])
	}
	nList = p[1].get('nList', [])
	if len(p) == 3:
		TAC.backPatch(nList, p[2]['instr'])
	else:
		TAC.backPatch(nList, p[3]['instr'])
	

def p_next_instr(p):
	'''M_instr : '''
	p[0] = {'instr': TAC.getNextInstr() }

def p_EmptyStatement(p):
	'''EmptyStatement : ';' '''

def p_LabelStatement(p):
	'''LabelStatement : IDENTIFIER ':'
				    | Marker_case CASE ConstantExpression ':'
					| DEFAULT ':' '''

	if p[2] == 'case':
		if type(p[3]) is dict:
			p3 = p[3]['tempVar']
		else:
			p3 = p[3]
		temp = ST.getTemp()
		ST.addTempAttr(temp,'int')
		t = ST.getListVar()
		TAC.emit(temp,t,p3,'!=')
		ST.addIncaselist(TAC.getNextInstr())
		TAC.emit('IF',temp,'','GOTO')
	elif p[1] == 'default' :
		addr = ST.getLastCaseAddr()
		if addr != None :
			caseAdrr = [ ST.getLastCaseAddr() ]
			ST.remLastCAse()
			TAC.backPatch(caseAdrr, TAC.getNextInstr())

def p_markerase(p):
	'''Marker_case : '''
	addr = ST.getLastCaseAddr()
	if addr != None :
		caseAdrr = [ ST.getLastCaseAddr() ]
		ST.remLastCAse()
		TAC.backPatch(caseAdrr, TAC.getNextInstr())

def p_ExpressionStatement(p):
	'''ExpressionStatement : Expression '''
	p[0] = p[1]	

def p_SelectionStatement(p):
	'''SelectionStatement : IF '(' Expression ')' M_instr_branch Statement
							|	IF '(' Expression ')' M_instr_branch Statement  ELSE N_instr M_instr_branch Statement
					        | SWITCH '(' Expression Mark_switch ')' Block '''

	if len(p) == 7 :
		if p[1] == 'if':
			p[0] = {
				'nList' : TAC.merge(p[3].get('falseList',[]), p[6].get('nList',[])),
				'endOfLoop' : p[6].get('endOfLoop' , [] ),
				'beginLoop' : p[6].get('beginLoop' , [] )
			}
			TAC.backPatch(p[3].get('trueList', []), p[5].get('instr',[]))
		else:
			addr = ST.getLastCaseAddr()
			if addr != None :
				caseAdrr = [ ST.getLastCaseAddr() ]
				ST.remLastCAse()
				TAC.backPatch(caseAdrr, TAC.getNextInstr())
			brkList = ST.getbrkList()
			for addr in brkList:
				TAC.backPatch([ addr ], TAC.getNextInstr())
			ST.deleteList()
	
	elif len(p) == 11 :
		TAC.backPatch(p[3].get('trueList',[]), p[5].get('instr',[]) )
		TAC.backPatch(p[3].get('falseList',[]),p[9].get('instr',[]) )
		temp = TAC.merge(p[6].get('nList',[]),p[8].get('nList',[]))
		p[0]= {
			'nList' : TAC.merge(temp, p[10].get('nList',[])),
			'endOfLoop': TAC.merge(p[10].get('endOfLoop',[]), p[6].get('endOfLoop',[])),
			'beginLoop': TAC.merge(p[10].get('loopBeginList', []), p[6].get('loopBeginList', []))
		}

def p_Mark_switch(p):
	''' Mark_switch : '''
	ST.addbrkVar(p[-1])

def p_N_instr(p):
	'''N_instr : '''
	p[0] = {
		'nList' : [TAC.getNextInstr()]
	}
	TAC.emit('','','','GOTO')


def p_branch_if(p):
	'''M_instr_branch : '''
	p[0] = {
		'instr' : TAC.getNextInstr()
	}

def p_IterationStatement(p):
	'''IterationStatement : WHILE M_instr_branch '(' Expression Mark_switch ')' M_instr_branch Statement
							| DO Mark_switch M_instr_branch Statement WHILE M_instr_branch '(' Expression ')' ';'
							| FOR '(' Mark_switch ForInit M_instr ForExpr M_instr ForIncr ')' M_instr Statement '''
							# | FOR '(' ForInit ForExpr         ')' Statement '''

	if len(p) == 9:
		TAC.backPatch(p[8].get('nList',[]), p[2].get('instr',[]))
		TAC.backPatch(p[4].get('trueList',[]), p[7].get('instr', []))
		p[0] = {
			'nList' : p[4].get('falseList',[])
		}
		TAC.emit('','',p[2]['instr'],'GOTO')
		brkList = ST.getbrkList()
		contList = ST.getcaseList()
		for addr in brkList:
			TAC.backPatch([ addr ], TAC.getNextInstr())
		for addr in contList:
			TAC.backPatch([ addr ],p[2].get('instr',[]))
		ST.deleteList()

	elif len(p) == 11:
		TAC.backPatch(p[4].get('nList',[]), p[6].get('instr',[]))
		TAC.backPatch(p[8].get('trueList',[]), p[3].get('instr',[]))
		p[0] = {
			'nList' : p[8].get('falseList',[])
		}
		brkList = ST.getbrkList()
		contList = ST.getcaseList()
		for addr in brkList:
			TAC.backPatch([ addr ], TAC.getNextInstr())
		for addr in contList:
			TAC.backPatch([ addr ],p[6].get('instr',[]))
		ST.deleteList()
		# TAC.emit('','',p[2]['instr'],'GOTO')

	elif len(p) == 12:
		TAC.backPatch(p[6].get('trueList',[]), p[10].get('instr',[]))
		TAC.backPatch(p[11].get('nList',[]), p[7].get('instr',[]))
		TAC.backPatch(p[8].get('nList',[]), p[5].get('instr',[]))
		p[0] = {
			'nList' : p[6].get('falseList',[])
		}
		TAC.emit('','',p[7]['instr'],'GOTO')
		brkList = ST.getbrkList()
		contList = ST.getcaseList()
		for addr in brkList:
			TAC.backPatch([ addr ], TAC.getNextInstr())
		for addr in contList:
			TAC.backPatch([ addr ],p[7].get('instr',[]))
		ST.deleteList()

def p_forinit(p):
	'''ForInit : ExpressionStatements ';'
				| LocalVariableDeclarationStatement
				| ';' '''

def p_ForExpr(p):
	'''ForExpr : Expression ';'
				| ';' '''
	if p[1] == ';':
		p[0] = {
			'trueList' : [TAC.getNextInstr()],
			'falseList' : []
		}
	else:
		p[0] = p[1]

def p_ForIncr(p):
	'''ForIncr : ExpressionStatements 
				|'''

	if len(p) == 2:
		p[0] ={
			'nList' : p[1].get('nList',[])
		}
	else:
		p[0] ={
			'nList' : [TAC.getNextInstr()]
		}
	TAC.emit('','',p[-3]['instr'],'GOTO')

def p_ExpressionStatements(p):
	'''ExpressionStatements : ExpressionStatement
							| ExpressionStatements ',' ExpressionStatement '''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = {
			'nList' : p[3].get('nList',[])
		}
def p_JumpStatement(p):
	'''JumpStatement : BREAK IDENTIFIER ';'
					| BREAK            ';'
				    | CONTINUE IDENTIFIER ';'
					| CONTINUE            ';'
					| RETURN Expression ';'
					| RETURN            ';'
					| THROW Expression ';' '''
	if len(p) == 3 :
		if  p[1] == 'break' :
			ST.addInbrklist(TAC.getNextInstr())
			TAC.emit('','','','GOTO')
		elif p[1] == 'return':
			TAC.emit('','','','RETURN')
		elif p[1] == 'continue':
			ST.addIncaselist(TAC.getNextInstr())
			TAC.emit('','','','GOTO')
	elif len(p) == 4 :
		scope =  ST.getCurrScopeName() 
		if p[1] == 'return':
			if type(p[2]) is not dict:
				typeId = ST.getIdAttr(p[2], 'type')
				ST.checkRetType(typeId, scope)
				TAC.emit(p[2],'','','RETURN')
			else:
				typeId = p[2]['type']
				ST.checkRetType(typeId,scope)
				TAC.emit(p[2]['tempVar'],'','','RETURN')

def p_PrimaryExpression(p):
	'''PrimaryExpression :  NotJustName '''
	p[0] = p[1]

def p_primaryexpr(p):
	'''PrimaryExpression : QualifiedName '''
	p[0] = p[1]
	if (type(p[1]) is not dict) and (len(p[1].split('.')) == 2):
		className = ST.getIdAttr(p[1].split('.')[0], 'type')
		typeId, offset = ST.checkClassId(className, p[1].split('.')[1]) 
		temp = ST.getTemp()
		temp = '*'+ temp
		ST.addTempAttr(temp, typeId)
		TAC.emit(temp,p[1].split('.')[0], offset,'-*' )
		p[0] = {
			'type' : typeId,
			'tempVar' : temp
		}


def p_NotJustName(p):
	''' NotJustName : SpecialName
					| NewAllocationExpression
					| ComplexPrimary '''

	p[0] = p[1]

def p_complexprimary(p):
	''' ComplexPrimary : ComplexPrimaryNoParenthesis
						| Integer_LIT 
						| Float_LIT
						| Char_LIT 
						| String_LIT
						| Bool_LIT
						| '(' Expression ')' '''
	if len(p) == 2 :					
		p[0] = p[1]
	else :
		p[0] = p[2]

#BOOLLIT
def p_ComplexPrimaryNoParenthesis(p):
	'''ComplexPrimaryNoParenthesis :  ArrayAccess
									| FieldAccess
									| MethodCall '''
	if type(p[1]) is not dict:
		p[0] = {'val': p[1], 'type':'None'}
	else:
		p[0] = p[1]

def p_IntLit(p):
	'''Integer_LIT : INT_LITERAL '''

	temp = ST.getTemp()
	ST.addTempAttr(temp, 'int')
	p[0] = {'type':'int', 'tempVar': temp , 'tempVal': p[1]}
	TAC.emit(temp,'',p[1],'=')

def p_FloatLit(p):
	''' Float_LIT : FLOAT_LITERAL '''

	temp = ST.getTemp()
	ST.addTempAttr(temp, 'float')
	p[0] = {'type':'float', 'tempVar': temp}
	TAC.emit(temp,'',p[1],'=')

def p_charlit(p):
	''' Char_LIT : CHAR_LITERAL '''
	
	temp = ST.getTemp()
	ST.addTempAttr(temp, 'char')
	p[0] = { 'type':'char', 'tempVar': temp}
	TAC.emit(temp,'',p[1],'=')

def p_stringLit(p):
	''' String_LIT : STRING_LITERAL '''
	
	temp = ST.getTemp()
	ST.addTempAttr(temp, 'String')
	p[0] = {'type':'String', 'tempVar': temp}
	TAC.emit(temp,'',p[1],'=')

def p_boolLit(p):
	''' Bool_LIT : BOOL '''
	
	temp = ST.getTemp()
	ST.addTempAttr(temp, 'boolean')
	p[0] = {'type':'boolean', 'tempVar': temp}
	TAC.emit(temp,'',p[1],'=')

	if p[1] == True :
		p[0]['trueList'] = [TAC.getNextInstr()]
	else :
		p[0]['falseList'] = [TAC.getNextInstr()]
	TAC.emit('','','','GOTO')

def p_arrayaccess(p):
	''' ArrayAccess : QualifiedName '[' Expression ']'
					| ComplexPrimary '[' Expression ']' '''
	if type(p[1]) is not dict:
		typeId = ST.getIdAttr(p[1], 'type')
		dimension = ST.getIdAttr(p[1], 'dimension')
		tempVal = p[1]
	else:
		typeId = p[1]['type']
		dimension = p[1]['dimension']
		tempVal = p[1]['tempVar']
	if typeId.split('_')[0] == 'array' :
		if type(p[3]) is not dict:
			type3 = ST.getIdAttr(p[3], 'type')
			val = p[3]
			p[3] = {
				'type' : type3,
				'tempVar': val
			}
		if not  p[3]['type'] == 'int':
			raise Exception('Array indices must be integers')

		dimlength = len(dimension)
		if dimlength == 1:
			typeofarray = typeId.split('_')[1]
			width =ST.getWidth(typeofarray)
			temp1 = ST.getTemp()
			ST.addTempAttr(temp1, 'int')
			output = ST.searchForArrayArg(tempVal)
			print output, '740'
			if type(p[1]) is not dict:
				TAC.emit(temp1, p[3]['tempVar'], width, '*')
				temp = ST.getTemp()
				temp = '*' + temp
				ST.addTempAttr(temp, 'int')
				if not output:
					TAC.emit(temp, tempVal, temp1, '+*')
				else:
					TAC.emit(temp, tempVal, temp1, '*.')
					
				# temp = ST.getTemp()
				# ST.addTempAttr(temp, 'int')
				# TAC.emit(temp, tempVal, temp1, '=*')
				#START FROM HERE
			else:
				TAC.emit(temp1, p[1]['tempVar'], p[3]['tempVar'], '+' )
				TAC.emit(temp1 ,temp1, width,'*' )
				temp = ST.getTemp()
				temp = '*' + temp
				ST.addTempAttr(temp, 'int')
				if not output:
					TAC.emit(temp, p[1]['arrayAdd'], temp1, '+*')
				else:
					TAC.emit(temp, p[1]['arrayAdd'], temp1, '*.')
			p[0] = {
				'type': 'int',
				'tempVar': temp
				}
		else:
			del dimension[0]
			temp = ST.getTemp()
			ST.addTempAttr(temp, 'int')
			if type(p[1]) is not dict:
				TAC.emit(temp ,p[3]['tempVar'], dimension[0],'*' )
			else:
				TAC.emit(temp, p[1]['tempVar'], p[3]['tempVar'], '+' )
				TAC.emit(temp ,temp, dimension[0],'*' )
			typeIdarray = typeId.split('_')
			typeIdarray[2] = str(int(typeIdarray[2]) - 1)
			typeofarray = '_'.join(typeIdarray)
			p[0] = {
				'type': typeofarray,
				'tempVar': temp,
				'dimension' : dimension,
			}
			if type(p[1]) is not dict:
				p[0]['arrayAdd'] = p[1]
			else:
				p[0]['arrayAdd'] = p[1]['arrayAdd']


def p_fieldaccess(p):
	'''FieldAccess : NotJustName '.' IDENTIFIER
					| RealPostfixExpression '.' IDENTIFIER
				    | QualifiedName '.' THIS
				    | QualifiedName '.' CLASS
				    | PrimitiveType '.' CLASS '''


def p_MethodCall(p):
	'''MethodCall : MethodAccess '(' ArgumentList ')'
					| MethodAccess '(' ')' '''

	if len(p[1].split('.'))==2 :
		className = ST.getIdAttr(p[1].split('.')[0], 'type')
		if ST.ifClass(className) :
			funcName = p[1].split('.')[1]
			ST.checkExistFuncClass(className, p[1].split('.')[1])
			temp = ST.getTemp()
			ST.addTempAttr(temp, 'int')
			typeWidth = 0
			if len(p) == 5:
				a = 0
				ST.checkNumClassArgs(className,p[1].split('.')[1], len(p[3]['expr']))
				TAC.emit(p[1].split('.')[0], '','','PARAM')
				for params in  p[3]['expr']:
					if type(params) is not dict:
						typei = ST.getIdAttr(params, 'type')
						width = ST.getIdAttr(params, 'width')
						typeWidth += width
						ST.checkClassType(className,p[1].split('.')[1],typei,a)
						TAC.emit(params,'','','PARAM')
					else:
						width = ST.getWidth(params['type'])
						typeWidth += width
						ST.checkClassType(className,p[1].split('.')[1],params['type'],a)
						TAC.emit(params['tempVar'],'','','PARAM')
					a += 1
				
				TAC.emit('Main.'+className+'.'+p[1].split('.')[1],typeWidth+4,temp,'CALL')
				# TAC.emit(typeWidth+4,'','','POP')
			else:
				ST.checkNumClassArgs(className,funcName, 0)
				TAC.emit(p[1].split('.')[0], '','','PARAM')
				TAC.emit('Main.'+className+'.'+p[1].split('.')[1], 4,temp,'CALL')
				# TAC.emit(4, '','','POP')
			methodtype = ST.getReturntypeClass(p[1].split('.')[1], 'Main.'+className)
			p[0] = {
				'type' : methodtype,
				'tempVar' : temp
			}
		else:
			raise Exception("Error in method call declaration")
	else:
		temp = ST.getTemp()
		ST.addTempAttr(temp, 'int')
		typeWidth = 0
		if len(p) == 5:
			if p[1] == "System.out.println":
				if len(p[3]['expr']) > 1:
					raise Exception('Multiple arguments in System.out.println not allowed')
				expr = p[3]['expr'][0]
				if type(expr) is dict:
					TAC.emit(p[3]['expr'][0]['tempVar'],'',p[3]['expr'][0]['type'],'PRINT')
				else:
					TAC.emit(p[3]['expr'][0],'',ST.getIdAttr(expr,'type'),'PRINT')
			else:
				funcName = ST.getFuncName(p[1])
				a = 0
				ST.checkNumArgs(p[1], len(p[3]['expr']))
				
				for params in  p[3]['expr']:
					if type(params) is not dict:
						typei = ST.getIdAttr(params, 'type')
						width = ST.getIdAttr(params, 'width')
						if typei.split('_')[0]== 'array':
							typeWidth += 4
						else:
							typeWidth += width
						ST.checkType(p[1],typei,a)
						TAC.emit(params,'','','PARAM')
					else:
						width = ST.getWidth(params['type'])
						typeWidth += width
						ST.checkType(p[1],params['type'],a)
						TAC.emit(params['tempVar'],'','','PARAM')
					a += 1
				TAC.emit(funcName,typeWidth,temp,'CALL')
				# TAC.emit(typeWidth,'','','POP')
		else:
			ST.checkNumArgs(p[1],0)
			funcName = ST.getFuncName(p[1])
			TAC.emit(funcName,0,temp,'CALL')
		methodtype = ST.getReturntype(p[1])
		p[0] = {
			'type' : methodtype,
			'tempVar' : temp
		}

def p_MethodAccess(p):
	'''MethodAccess : ComplexPrimaryNoParenthesis
					| SpecialName
					| QualifiedName '''
	p[0] = p[1]
#JNULL
def p_SpecialName(p):
	'''SpecialName : THIS
					| SUPER
					| NULL '''

def p_ArgumentList(p):
	'''ArgumentList : Expression
					| ArgumentList ',' Expression '''

	p[0] = {}
	if len(p) == 2 :
		p[0]['expr'] =[ p[1] ]
	else:
		p[1]['expr'].append(p[3])
		p[0]['expr'] = p[1]['expr']

def p_NewAllocationExpression(p):
	'''NewAllocationExpression : PlainNewAllocationExpression
        						| QualifiedName '.' PlainNewAllocationExpression '''
	if len(p) == 2:
		p[0] = p[1]

def p_PlainNewAllocationExpression(p):
    '''PlainNewAllocationExpression : ArrayAllocationExpression
							    	| ClassAllocationExpression
							    	| ArrayAllocationExpression '{' '}'
							    	| ClassAllocationExpression '{' '}'
							    	| ArrayAllocationExpression '{' ArrayInitializers '}'
							    	| ClassAllocationExpression '{' FieldDeclarations '}' '''
    if len(p) == 2:
		p[0] = p[1]

def p_ClassAllocationExpression(p):
	'''ClassAllocationExpression : NEW TypeName '(' ArgumentList ')'
								| NEW TypeName '('              ')' '''
	# if len(p) == 5:
	offset = ST.checkForClass(p[2])
	print offset, '932'
	if len(p) == 5 :
		# temp = ST.getTemp()
		# ST.addTempAttr(temp, 'int')
		# TAC.emit(temp ,'',offset,'=')
		# TAC.emit(temp,'','','PARAM')
		temp = ST.getTemp()
		ST.addTempArrayAttr(temp, offset, p[2])
		# TAC.emit('_ALLOC',4,temp,'CALL')
		# TAC.emit(4,'','','POP')
		p[0] = {
			'type': p[2],
			'tempVar' : temp
		}

def p_ArrayAllocationExpression(p):
	'''ArrayAllocationExpression : NEW TypeName DimExprs Dims
								| NEW TypeName DimExprs
							    | NEW TypeName Dims '''
	if len(p) == 5:
		raise Exception("Not allowed in language")
	else:
		dimension = len(p[3])
		typeWidth = ST.getWidth(p[2])
		# temp = ST.getTemp()
		# ST.addTempAttr(temp, 'int')
		# TAC.emit(temp,'',typeWidth,'=' ) 
		stringDim = []
		arrayWidth = typeWidth;
		for dim in p[3]:
			stringDim.append(dim['tempVar'])
			if dim['type'] != 'int':
				raise Exception('Array indices must be integers')
			# TAC.emit(temp,dim['tempVar'],temp,'*' ) 
			arrayWidth = arrayWidth * int(dim['tempVal'])
			# width =  dim['tempVar'] * width
		typeId = 'array_' + p[2] + '_' + str(dimension)
		# TAC.emit(temp,'','','PARAM')
		temp2 = ST.getTemp()
		ST.addTempArrayAttr(temp2, arrayWidth, 'width')
		# ST.addTempAttr(temp2, 'int')
		# TAC.emit('_ALLOC',1,temp2,'CALL')
		# TAC.emit(4,'','','POP')
		p[0] = {
			'type' : typeId,
			'tempVar' : temp2,
			'dimension' : stringDim,
			'width': arrayWidth
		} 

def p_DimExprs(p):
	'''DimExprs : DimExpr
				| DimExprs DimExpr '''
	if len(p) == 2:
		p[0] =[ p[1] ]
	else:
		p[1].append(p[2])
		p[0] = p[1]

def p_DimExpr(p):
	'''DimExpr : '[' Expression ']' '''
	p[0] = p[2] 


def p_Dims(p):
	'''Dims : OP_DIM
			| Dims OP_DIM '''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[1] + p[2]

def p_OP_DIM(p):
	'''OP_DIM : '[' ']' '''
	p[0] = 1

def p_PostfixExpression(p):
	'''PostfixExpression : PrimaryExpression
						| RealPostfixExpression '''
	p[0] = p[1]

def p_RealPostfixExpression(p):
	'''RealPostfixExpression : PostfixExpression OPT_INC_DEC '''
	typeId = ST.getIdAttr(p[1], 'type')
	if typeId != 'int' :
		raise Exception("Identifier " + p[1] + " not of type integer")
	temp1 = ST.getTemp()
	ST.addTempAttr(temp1, 'int')
	TAC.emit(temp1,'', 1,'=')
	temp2 = ST.getTemp()
	ST.addTempAttr(temp2, 'int')
	TAC.emit(temp2, temp1, p[1],p[2][0])
	TAC.emit(p[1],temp2,'','=')
	p[0] = {
			'trueList' : [TAC.getNextInstr()],
			'falseList' : [TAC.getNextInstr() + 1],
			'type' : typeId,
			'tempVar' : p[1]
		}

def p_UnaryExpression(p):
	'''UnaryExpression : OPT_INC_DEC UnaryExpression
						| ArithmeticUnaryOperator CastExpression
						| LogicalUnaryExpression '''
	if len(p) == 2 :
		p[0] = p[1]
	elif p[1] == '+' or p[1] == '-' :
		temp = ST.getTemp()
		if type(p[2]) is not dict:
			typeId = ST.getIdAttr(p[2], 'type')
			if typeId != 'int' and typeId!= 'float':
				raise Exception("Type check error in variable "+ p[2])
			else:
				TAC.emit(temp, p[2], '', p[1])
		else:
			typeId = p[2]['type']
			if typeId != 'int' and typeId!='float':
				raise Exception("Type check error")
			else:
				TAC.emit(temp, p[2]['tempVar'], '', p[1])
		ST.addTempAttr(temp, typeId)
		p[0] = { 'type' : typeId , 'tempVar' : temp } 
	else:
		typeId = ST.getIdAttr(p[2], 'type')
		if typeId != 'int' :
			raise Exception("Identifier " + p[2] + " not of type integer")
		temp1 = ST.getTemp()
		ST.addTempAttr(temp1, 'int')
		TAC.emit(temp1,'',1,'=')
		temp2 = ST.getTemp()
		ST.addTempAttr(temp2, 'int' )
		TAC.emit(temp2, temp1, p[2],p[1][0])
		TAC.emit(p[2],temp2,'','=')
		p[0] = {
				'trueList' : [TAC.getNextInstr()],
				'falseList' : [TAC.getNextInstr() + 1],
				'type' : typeId,
				'tempVar' : p[2]
			}

def p_LogicalUnaryExpression(p):
	'''LogicalUnaryExpression : PostfixExpression
								| LogicalUnaryOperator UnaryExpression '''

	if len(p) == 2 :
		p[0] = p[1]
	else :
		temp = ST.getTemp()
		if type(p[2]) is not dict:
			typeId = ST.getIdAttr(p[2], 'type')
			if typeId != 'int' and typeId != 'boolean' :
				raise Exception("Type check error in variable "+ p[2])
			else:
				TAC.emit(temp, p[2], '', p[1])
		else :
			typeId = p[2]['type']
			# print typeId
			if typeId != 'int' and typeId != 'boolean' :
				raise Exception("Type check error ")
			else:
				TAC.emit(temp, p[2]['tempVar'], '', p[1])
		p[0] = { 'type' : 'int' , 'tempVar' : temp } 
		ST.addTempAttr(temp, 'int')

def p_LogicalUnaryOperator(p):
	'''LogicalUnaryOperator : '~'
							| '!' '''
	p[0] = p[1]

def p_ArithmeticUnaryOperator(p):
	'''ArithmeticUnaryOperator : '+'
								| '-' '''
	p[0] = p[1]

def p_CastExpression(p):
	'''CastExpression : UnaryExpression '''
						# | '(' PrimitiveTypeExpression ')' CastExpression
						# | '(' ClassTypeExpression ')' CastExpression
						# | '(' Expression ')' LogicalUnaryExpression '''
	p[0] = p[1]

# def p_PrimitiveTypeExpression(p):
# 	'''PrimitiveTypeExpression : PrimitiveType
# 							| PrimitiveType Dims '''

# def p_ClassTypeExpression(p):
# 	'''ClassTypeExpression : QualifiedName Dims'''

def p_MultiplicativeExpression(p):
	'''MultiplicativeExpression : CastExpression
								| MultiplicativeExpression '*' CastExpression
								| MultiplicativeExpression '/' CastExpression
								| MultiplicativeExpression '%' CastExpression '''
	if len(p) == 2:
		p[0] = p[1]
	else:
		if type(p[1]) is not dict:
			type1 = ST.getIdAttr(p[1], 'type')
			tempVar1 = p[1]
		else:
			type1 = p[1]['type'] 
			tempVar1 = p[1]['tempVar']

		if type(p[3]) is not dict:
			type2 = ST.getIdAttr(p[3], 'type')
			tempVar2 = p[3]
		else:
			type2 = p[3]['type']
			tempVar2 = p[3]['tempVar']

		if type1 == type2 :
			temp = ST.getTemp()
			ST.addTempAttr(temp, type1)
			p[0] = {'type': type1 , 'tempVar' : temp}
			TAC.emit(temp, tempVar1, tempVar2, p[2])
		else :
			raise Exception("Type error in multiplicative Expression")


def p_AdditiveExpression(p):
	''' AdditiveExpression : MultiplicativeExpression
    						| AdditiveExpression '+' MultiplicativeExpression
							| AdditiveExpression '-' MultiplicativeExpression '''
	if len(p) == 2:
		p[0] = p[1]
	else:
		if type(p[1]) is not dict:
			type1 = ST.getIdAttr(p[1], 'type')
			tempVar1 = p[1]
		else:
			type1 = p[1]['type'] 
			tempVar1 = p[1]['tempVar']

		if type(p[3]) is not dict:
			type2 = ST.getIdAttr(p[3], 'type')
			tempVar2 = p[3]
		else:
			type2 = p[3]['type']
			tempVar2 = p[3]['tempVar']

		if type1 == type2 and (type1 == 'int' or type1 == 'float') :
			temp = ST.getTemp()
			ST.addTempAttr(temp, type1)
			p[0] = {'type': type1 , 'tempVar' : temp}
			TAC.emit(temp, tempVar1, tempVar2, p[2])
		else :
			raise Exception("Type error in additive Expression")


def p_ShiftExpression(p):
	'''ShiftExpression : AdditiveExpression
    					| ShiftExpression OPT_SOME AdditiveExpression '''
	
	if len(p) == 2:
		p[0] = p[1]
	else:
		if type(p[1]) is not dict:
			type1 = ST.getIdAttr(p[1], 'type')
			tempVar1 = p[1]
		else:
			type1 = p[1]['type'] 
			tempVar1 = p[1]['tempVar']

		if type(p[3]) is not dict:
			type2 = ST.getIdAttr(p[3], 'type')
			tempVar2 = p[3]
		else:
			type2 = p[3]['type']
			tempVar2 = p[3]['tempVar']

		if type1 == type2 and (type1 == 'int') :
			temp = ST.getTemp()
			ST.addTempAttr(temp, type1)
			p[0] = {'type': type1 , 'tempVar' : temp}
			TAC.emit(temp, tempVar1, tempVar2, p[2])
		else :
			raise Exception("Type error in additive Expression")

def p_RelationalExpression(p):
	'''RelationalExpression : ShiftExpression
						    | RelationalExpression '<' ShiftExpression
							| RelationalExpression '>' ShiftExpression
							| RelationalExpression OP_LE ShiftExpression
							| RelationalExpression OP_GE ShiftExpression '''
	if len(p) == 2:
		p[0] = p[1]

	else: 
		temp = ST.getTemp()
		ST.addTempAttr(temp, 'int')
		if type(p[1]) is not dict:
			temp1 = p[1]
		else:
			temp1 = p[1]['tempVar']
		if type(p[3]) is not dict:
			temp2 = p[3]
		else:
			temp2 = p[3]['tempVar']

		TAC.emit(temp, temp1,temp2,p[2])
		p[0] = {
			'trueList' : [TAC.getNextInstr()],
			'falseList' : [TAC.getNextInstr() + 1],
			'type' : 'boolean'
		}
		TAC.emit('IF',temp,'','GOTO')
		TAC.emit('','','','GOTO')

def p_EqualityExpression(p):
	''' EqualityExpression : RelationalExpression
						    | EqualityExpression OP_EQ RelationalExpression
						    | EqualityExpression OP_NE RelationalExpression '''
	if len(p) == 2:
		p[0] = p[1]
	else: 
		temp = ST.getTemp()
		ST.addTempAttr(temp, 'int')
		if type(p[1]) is not dict:
			temp1 = p[1]
		else:
			temp1 = p[1]['tempVar']

		if type(p[3]) is not dict:
			temp2 = p[3]
		else:
			temp2 = p[3]['tempVar']

		TAC.emit(temp, temp1,temp2,p[2])
		p[0] = {
			'trueList' : [TAC.getNextInstr()],
			'falseList' : [TAC.getNextInstr() + 1],
			'type' : 'boolean'
		}
		TAC.emit('IF',temp,'','GOTO')
		TAC.emit('','','','GOTO')


def p_AndExpression(p):
	'''AndExpression : EqualityExpression
					| AndExpression '&' EqualityExpression '''
	if len(p) == 2:
		p[0] = p[1]
	else :
		if type(p[1]) is not dict:
			type1 = ST.getIdAttr(p[1], 'type')
			tempVar1 = p[1]
		else:
			type1 = p[1]['type'] 
			tempVar1 = p[1]['tempVar']

		if type(p[3]) is not dict:
			type2 = ST.getIdAttr(p[3], 'type')
			tempVar2 = p[3]
		else:
			type2 = p[3]['type']
			tempVar2 = p[3]['tempVar']

		if type1 == type2 and (type1 == 'int') :
			temp = ST.getTemp()
			ST.addTempAttr(temp, type1)
			p[0] = {'type': type1 , 'tempVar' : temp}
			TAC.emit(temp, tempVar1, tempVar2, p[2])
		else :
			raise Exception("Type error in additive Expression")

def p_ExclusiveOrExpression(p):
	'''ExclusiveOrExpression : AndExpression
							| ExclusiveOrExpression '^' AndExpression '''
	if len(p) == 2:
		p[0] = p[1]
	else:
		if type(p[1]) is not dict:
			type1 = ST.getIdAttr(p[1], 'type')
			tempVar1 = p[1]
		else:
			type1 = p[1]['type'] 
			tempVar1 = p[1]['tempVar']

		if type(p[3]) is not dict:
			type2 = ST.getIdAttr(p[3], 'type')
			tempVar2 = p[3]
		else:
			type2 = p[3]['type']
			tempVar2 = p[3]['tempVar']

		if type1 == type2 and (type1 == 'int' ) :
			temp = ST.getTemp()
			ST.addTempAttr(temp, type1)
			p[0] = {'type': type1 , 'tempVar' : temp}
			TAC.emit(temp, tempVar1, tempVar2, p[2])
		else :
			raise Exception("Type error in additive Expression")

def p_InclusiveOrExpression(p):
	'''InclusiveOrExpression : ExclusiveOrExpression
							| InclusiveOrExpression '|' ExclusiveOrExpression '''
	if len(p) == 2:
		p[0] = p[1]
	else:
		if type(p[1]) is not dict:
			type1 = ST.getIdAttr(p[1], 'type')
			tempVar1 = p[1]
		else:
			type1 = p[1]['type'] 
			tempVar1 = p[1]['tempVar']

		if type(p[3]) is not dict:
			type2 = ST.getIdAttr(p[3], 'type')
			tempVar2 = p[3]
		else:
			type2 = p[3]['type']
			tempVar2 = p[3]['tempVar']

		if type1 == type2 and (type1 == 'int' ) :
			temp = ST.getTemp()
			ST.addTempAttr(temp, type1)
			p[0] = {'type': type1 , 'tempVar' : temp}
			TAC.emit(temp, tempVar1, tempVar2, p[2])
		else :
			raise Exception("Type error in additive Expression")

def p_ConditionalAndExpression(p):
	'''ConditionalAndExpression : InclusiveOrExpression
								| ConditionalAndExpression OP_LAND M_OP InclusiveOrExpression'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		# if type(p[1]) is dict :
		TAC.backPatch(p[1]['trueList'], p[3]['instr'])
		p[0] = {
			'trueList' : p[4].get('trueList', []),
			'falseList' : TAC.merge(p[1].get('falseList',[]), p[4].get('falseList',[])),
			'type' : 'boolean'
		}


def p_ConditionalOrExpression(p):
	'''ConditionalOrExpression : ConditionalAndExpression
								| ConditionalOrExpression OP_LOR M_OP ConditionalAndExpression '''
	if len(p) == 2:
		p[0] = p[1]
	else:
		TAC.backPatch(p[1]['falseList'], p[3]['instr'])
		p[0] = {
			'trueList' : TAC.merge(p[1].get('trueList',[]), p[4].get('trueList',[])),
			'falseList' : p[4].get('falseList', []),
			'type' : 'boolean'
		}


def p_m_operator(p):
	''' M_OP : '''
	p[0] = {
		'instr' : TAC.getNextInstr()
	}

def p_ConditionalExpression(p):
	'''ConditionalExpression : ConditionalOrExpression
							| ConditionalOrExpression '?' M_instr Expression Mark ':' M_instr ConditionalExpression M_instr'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		if type(p[1]) is not dict:
			typeId = ST.getIdAttr(p[1], 'type')
			if (typeId!='boolean'):
				raise Exception("Type check error for condition expression")
		elif p[1]['type'] != 'boolean':
			raise Exception("Type check error for condition expression")
		
		if type(p[8]) is not dict:
			temp3 = p[8]
			type3 = ST.getIdAttr(p[8], 'type')
		else:
			temp3 = p[8]['tempVar']
			type3 = p[8]['type']

		if type(p[4]) is not dict:
			temp2 = p[4]
			type2 = ST.getIdAttr(p[4], 'type')
		else:
			temp2 = p[4]['tempVar']
			type2 = p[4]['type']

		if type2 != type3:
			raise Exception("Type check error in ternary operator")

		TAC.backPatch(p[1].get('trueList',[]), p[3].get('instr',[]) )		
		TAC.emit(p[5]['temp'],temp3,'','=')
		nextIns = TAC.getNextInstr()
		
		TAC.backPatch(p[1].get('falseList',[]), p[7].get('instr',[]) )
		
		TAC.backPatch(p[5]['instr'], nextIns  )
		p[0] = {'type':type3,'tempVar': p[5]['temp'] }

def p_mark(p):
	''' Mark : '''
	
	tempVar = ST.getTemp()
	if type(p[-1]) is not dict:
			temp = p[-1]
			typeVar = ST.getIdAttr(p[-1], 'type')
	else:
		temp = p[-1]['tempVar']
		typeVar = p[-1]['type']
	ST.addTempAttr(tempVar, typeVar)
	TAC.emit(tempVar,temp,'','=')
	instr = TAC.getNextInstr()
	TAC.emit('','','','GOTO')
	p[0] = {
		'instr' : [ instr ],
		'temp' : tempVar
	}

def p_AssignmentExpression(p):
	'''AssignmentExpression : ConditionalExpression
							| UnaryExpression AssignmentOperator AssignmentExpression'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		if type(p[1]) is not dict:
			type1 = ST.getIdAttr(p[1], 'type')
			tempVar1 = p[1]
		else:
			type1 = p[1]['type']
			tempVar1 = p[1]['tempVar']
			if type1 in ['boolean', 'char', 'int', 'float', 'String'] and tempVar1[0]!='*' :
				raise Exception("Left hand side of assignment must be an Identifier")

		if type(p[3]) is not dict:
			type2 = ST.getIdAttr(p[3], 'type')
			tempVar2 = p[3]
		else:
			type2 = p[3]['type']
			tempVar2 = p[3]['tempVar']

		# if type1 == 'pointer':
		# 	if p[2] == '=':
		# 		TAC.emit(tempVar1, tempVar2,'', '*=')

		# 	p[0] = {'type':'pointer', 'tempVar': tempVar1}
		if type1 != type2:
			raise Exception("Type error in assignment expression")
		else:
			# temp = ST.getTemp()
			p[0] = {'type': type1 , 'tempVar' : tempVar1}
			if p[2] == '=':
				TAC.emit(tempVar1, tempVar2,'', p[2])
			else:
				temp = ST.getTemp()
				ST.addTempAttr(temp, type1)
				TAC.emit(temp, tempVar1,tempVar2, p[2][0])
				TAC.emit(tempVar1, temp, '', '=')


def p_AssignmentOperator(p):
	'''AssignmentOperator : '='
						| OPT_EQ '''
						# | ASS_DIV
						# | ASS_MOD
						# | ASS_ADD
						# | ASS_SUB
						# | ASS_SHL
						# | ASS_SHR
						# | ASS_SHRR
						# | ASS_AND
						# | ASS_XOR
						# | ASS_OR '''
	p[0] = p[1]


def p_Expression(p):
	'''Expression : AssignmentExpression'''
	p[0] = p[1]

def p_ConstantExpression(p):
	'''ConstantExpression : ConditionalExpression'''
	p[0] = p[1]
# Error rule for syntax errors
def p_error(p):
    raise Exception("Syntax error in input!")


# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# Build the parser
parser = yacc.yacc()

def runParser(filename):
	global MainClass
	# try:
	Filename = filename
	MainClass = Filename.split('/')[-1].split('.')[0]
	data = open(Filename).read()
	# except EOFError:
	# 	print "Please give testfile as well"
	if data:
		result = parser.parse(data)
		return ST,TAC
	else:
		return None, None

if __name__ == '__main__':
	MainClass = ''
	try:
		Filename = sys.argv[1]
		MainClass = Filename.split('/')[-1].split('.')[0]
		data = open(Filename).read()
	except EOFError:
		print "Please give testfile as well"
    	if data:
    		result = parser.parse(data)