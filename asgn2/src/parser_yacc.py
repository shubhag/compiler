import ply.yacc as yacc, sys
from subprocess import call

# Get the token map from the lexer.  This is required.
from lexer_yacc import tokens

def p_compilationunit(p):
	'''CompilationUnit : ProgramFile '''

def p_typespeciifier(p):
	'''TypeSpecifier : TypeName
					| TypeName Dims '''

def p_typename(p):
	'''TypeName : PrimitiveType 
				| QualifiedName '''

def p_classnamelist(p):
	'''ClassNameList : QualifiedName
					| ClassNameList ',' QualifiedName '''

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

def p_semicolons(p):
	''' SemiColons : ';'
					| SemiColons ';' '''

def p_programfile(p):
	'''ProgramFile : PackageStatement ImportStatements TypeDeclarations
					| PackageStatement ImportStatements
					| PackageStatement TypeDeclarations
					| ImportStatements TypeDeclarations
					| PackageStatement 
					| ImportStatements
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

def p_typedeclaration(p):
	'''TypeDeclaration : ClassHeader '{' FieldDeclarations '}'
						| ClassHeader '{' '}' '''

def p_classheader(p):
	'''ClassHeader : Modifiers ClassWord IDENTIFIER Extends Interfaces
					| Modifiers ClassWord IDENTIFIER Extends
					| Modifiers ClassWord IDENTIFIER       Interfaces
					|           ClassWord IDENTIFIER Extends Interfaces
					| Modifiers ClassWord IDENTIFIER
					|           ClassWord IDENTIFIER Extends
					|           ClassWord IDENTIFIER       Interfaces
					|           ClassWord IDENTIFIER '''
def p_modifiers(p):
	''' Modifiers : Modifier
					| Modifiers Modifier '''

def p_modifier(p):
	'''Modifier : ABSTRACT
				| FINAL
				| PUBLIC
				| PROTECTED
				| PRIVATE
				| STATIC
				| TRANSIENT
				| VOLATILE
				| NATIVE
				| SYNCHRONIZED '''

def p_classword(p):
	''' ClassWord : CLASS
					| INTERFACE '''

def p_interfaces(p):
	'''Interfaces : IMPLEMENTS ClassNameList '''

def p_fielddeclarartions(p):
	''' FieldDeclarations : FieldDeclarationOptSemi
        					| FieldDeclarations FieldDeclarationOptSemi '''

def p_fielddeclarationoptsemi(p):
	''' FieldDeclarationOptSemi : FieldDeclaration
        						| FieldDeclaration SemiColons '''

def p_fielddeclaration(p):
	''' FieldDeclaration : FieldVariableDeclaration ';'
						| MethodDeclaration
						| ConstructorDeclaration
						| StaticInitializer
					    | NonStaticInitializer
				        | TypeDeclaration '''

def p_fieldvariabledeclaration(p):
	'''FieldVariableDeclaration : Modifiers TypeSpecifier VariableDeclarators
								| TypeSpecifier VariableDeclarators '''

def p_variabledeclarators(p):
	'''VariableDeclarators : VariableDeclarator
							| VariableDeclarators ',' VariableDeclarator'''

def p_variabledeclarator(p):
	''' VariableDeclarator : DeclaratorName
							| DeclaratorName '=' VariableInitializer '''

def p_variableinitializer(p):
	'''VariableInitializer : Expression
							| '{' '}'
        					| '{' ArrayInitializers '}' '''

def p_arrayinitializers(p):
	''' ArrayInitializers : VariableInitializer
							| ArrayInitializers ',' VariableInitializer
							| ArrayInitializers ',' '''

def p_methoddeclaration(p):
	''' MethodDeclaration : Modifiers TypeSpecifier MethodDeclarator Throws MethodBody
						| Modifiers TypeSpecifier MethodDeclarator        MethodBody
						|           TypeSpecifier MethodDeclarator Throws MethodBody
						|           TypeSpecifier MethodDeclarator        MethodBody '''

def p_methoddeclarator(p):
	'''MethodDeclarator : DeclaratorName '(' ParameterList ')'
						| DeclaratorName '(' ')'
						| MethodDeclarator OP_DIM '''

def p_parameterlist(p):
	''' ParameterList : Parameter
						| ParameterList ',' Parameter '''

def p_parameter(p):
	'''Parameter : TypeSpecifier DeclaratorName
        		| FINAL TypeSpecifier DeclaratorName '''

def p_declaratorname(p):
	''' DeclaratorName : IDENTIFIER
						| DeclaratorName OP_DIM '''

def p_throws(p):
	''' Throws : THROWS ClassNameList '''

def p_methodbody(p):
	'''MethodBody : Block
					| ';' '''

def p_constructdeclarator(p):
	''' ConstructorDeclaration : Modifiers ConstructorDeclarator Throws Block
								| Modifiers ConstructorDeclarator        Block
								|           ConstructorDeclarator Throws Block
								|           ConstructorDeclarator        Block '''

def p_constructordeclarator(p):
	'''ConstructorDeclarator : IDENTIFIER '(' ParameterList ')'
							| IDENTIFIER '(' ')' '''

def p_staticinitializer(p):
	'''StaticInitializer : STATIC Block '''

def p_nonstaticini(p):
	'''NonStaticInitializer : Block '''

def p_extends(p):
	'''Extends : EXTENDS TypeName
				| Extends ',' TypeName '''

def p_block(p):
	'''Block : '{' LocalVariableDeclarationsAndStatements '}'
				| '{' '}' '''

def p_LocalVariableDeclarationsAndStatements(p):
	'''LocalVariableDeclarationsAndStatements : LocalVariableDeclarationOrStatement
											| LocalVariableDeclarationsAndStatements LocalVariableDeclarationOrStatement '''

def p_LocalVariableDeclarationOrStatement(p):
	'''LocalVariableDeclarationOrStatement : LocalVariableDeclarationStatement
											| Statement '''

def p_LocalVariableDeclarationStatement(p):
	''' LocalVariableDeclarationStatement : TypeSpecifier VariableDeclarators ';'
        								| FINAL TypeSpecifier VariableDeclarators ';' '''

def p_statement(p):
	'''	Statement : EmptyStatement
				| LabelStatement
				| ExpressionStatement ';'
			    | SelectionStatement M_instr
			   	| IterationStatement
				| JumpStatement
				| GuardingStatement
				| Block '''
def p_next_instr(p):
	'''M_instr : '''
def p_EmptyStatement(p):
	'''EmptyStatement : ';' '''

def p_LabelStatement(p):
	'''LabelStatement : IDENTIFIER ':'
				    | CASE ConstantExpression ':'
					| DEFAULT ':' '''

def p_ExpressionStatement(p):
	'''ExpressionStatement : Expression '''

def p_SelectionStatement(p):
	'''SelectionStatement : IF '(' Expression ')' Statement
							| IF '(' Expression ')' Statement ELSE Statement
					        | SWITCH '(' Expression ')' Block '''


def p_IterationStatement(p):
	'''IterationStatement : WHILE '(' Expression ')' Statement
							| DO Statement WHILE '(' Expression ')' ';'
							| FOR '(' ForInit ForExpr ForIncr ')' Statement
							| FOR '(' ForInit ForExpr         ')' Statement '''


def p_forinit(p):
	'''ForInit : ExpressionStatements ';'
				| LocalVariableDeclarationStatement
				| ';' '''

def p_ForExpr(p):
	'''ForExpr : Expression ';'
				| ';' '''

def p_ForIncr(p):
	'''ForIncr : ExpressionStatements'''

def p_ExpressionStatements(p):
	'''ExpressionStatements : ExpressionStatement
							| ExpressionStatements ',' ExpressionStatement '''

def p_JumpStatement(p):
	'''JumpStatement : BREAK IDENTIFIER ';'
					| BREAK            ';'
				    | CONTINUE IDENTIFIER ';'
					| CONTINUE            ';'
					| RETURN Expression ';'
					| RETURN            ';'
					| THROW Expression ';' '''

def p_GuardingStatement(p):
	'''GuardingStatement : SYNCHRONIZED '(' Expression ')' Statement
						| TRY Block Finally
						| TRY Block Catches
						| TRY Block Catches Finally '''

def p_Catches(p):
	'''Catches : Catch
				| Catches Catch '''

def p_Catch(p):
	'''Catch : CatchHeader Block '''

def p_catchheader(p):
	'''CatchHeader : CATCH '(' TypeSpecifier IDENTIFIER ')'
					| CATCH '(' TypeSpecifier ')' '''

def p_FINALLY(p):
	'''Finally : FINALLY Block'''

def p_PrimaryExpression(p):
	'''PrimaryExpression : QualifiedName
						| NotJustName '''

def p_NotJustName(p):
	''' NotJustName : SpecialName
					| NewAllocationExpression
					| ComplexPrimary '''

def p_complexprimary(p):
	''' ComplexPrimary : '(' Expression ')'
						| ComplexPrimaryNoParenthesis '''
#BOOLLIT
def p_ComplexPrimaryNoParenthesis(p):
	'''ComplexPrimaryNoParenthesis : FLOAT_LITERAL
									| INT_LITERAL
								    | CHAR_LITERAL
								    | STRING_LITERAL
									| BOOL                                
									| ArrayAccess
									| FieldAccess
									| MethodCall '''

def p_arrayaccess(p):
	''' ArrayAccess : QualifiedName '[' Expression ']'
					| ComplexPrimary '[' Expression ']' '''

def p_fieldaccess(p):
	'''FieldAccess : NotJustName '.' IDENTIFIER
					| RealPostfixExpression '.' IDENTIFIER
				    | QualifiedName '.' THIS
				    | QualifiedName '.' CLASS
				    | PrimitiveType '.' CLASS '''


def p_MethodCall(p):
	'''MethodCall : MethodAccess '(' ArgumentList ')'
					| MethodAccess '(' ')' '''


def p_MethodAccess(p):
	'''MethodAccess : ComplexPrimaryNoParenthesis
					| SpecialName
					| QualifiedName '''
#JNULL
def p_SpecialName(p):
	'''SpecialName : THIS
					| SUPER
					| NULL '''

def p_ArgumentList(p):
	'''ArgumentList : Expression
					| ArgumentList ',' Expression '''

def p_NewAllocationExpression(p):
	'''NewAllocationExpression : PlainNewAllocationExpression
        						| QualifiedName '.' PlainNewAllocationExpression '''

def p_PlainNewAllocationExpression(p):
    '''PlainNewAllocationExpression : ArrayAllocationExpression
							    	| ClassAllocationExpression
							    	| ArrayAllocationExpression '{' '}'
							    	| ClassAllocationExpression '{' '}'
							    	| ArrayAllocationExpression '{' ArrayInitializers '}'
							    	| ClassAllocationExpression '{' FieldDeclarations '}' '''

def p_ClassAllocationExpression(p):
	'''ClassAllocationExpression : NEW TypeName '(' ArgumentList ')'
								| NEW TypeName '('              ')' '''

def p_ArrayAllocationExpression(p):
	'''ArrayAllocationExpression : NEW TypeName DimExprs Dims
								| NEW TypeName DimExprs
							    | NEW TypeName Dims '''

def p_DimExprs(p):
	'''DimExprs : DimExpr
				| DimExprs DimExpr '''

def p_DimExpr(p):
	'''DimExpr : '[' Expression ']' '''

def p_Dims(p):
	'''Dims : OP_DIM
			| Dims OP_DIM '''

def p_OP_DIM(p):
	'''OP_DIM : '[' ']' '''

def p_PostfixExpression(p):
	'''PostfixExpression : PrimaryExpression
						| RealPostfixExpression '''

def p_RealPostfixExpression(p):
	'''RealPostfixExpression : PostfixExpression OPT_INC_DEC '''

def p_UnaryExpression(p):
	'''UnaryExpression : OPT_INC_DEC UnaryExpression
						| ArithmeticUnaryOperator CastExpression
						| LogicalUnaryExpression '''

def p_LogicalUnaryExpression(p):
	'''LogicalUnaryExpression : PostfixExpression
								| LogicalUnaryOperator UnaryExpression '''

def p_LogicalUnaryOperator(p):
	'''LogicalUnaryOperator : '~'
							| '!' '''

def p_ArithmeticUnaryOperator(p):
	'''ArithmeticUnaryOperator : '+'
								| '-' '''

def p_CastExpression(p):
	'''CastExpression : UnaryExpression
						| '(' PrimitiveTypeExpression ')' CastExpression
						| '(' ClassTypeExpression ')' CastExpression
						| '(' Expression ')' LogicalUnaryExpression '''

def p_PrimitiveTypeExpression(p):
	'''PrimitiveTypeExpression : PrimitiveType
							| PrimitiveType Dims '''

def p_ClassTypeExpression(p):
	'''ClassTypeExpression : QualifiedName Dims'''

def p_MultiplicativeExpression(p):
	'''MultiplicativeExpression : CastExpression
								| MultiplicativeExpression '*' CastExpression
								| MultiplicativeExpression '/' CastExpression
								| MultiplicativeExpression '%' CastExpression '''

def p_AdditiveExpression(p):
	''' AdditiveExpression : MultiplicativeExpression
    						| AdditiveExpression '+' MultiplicativeExpression
							| AdditiveExpression '-' MultiplicativeExpression '''

def p_ShiftExpression(p):
	'''ShiftExpression : AdditiveExpression
    						| ShiftExpression OPT_SOME AdditiveExpression '''

def p_RelationalExpression(p):
	'''RelationalExpression : ShiftExpression
						    | RelationalExpression '<' ShiftExpression
							| RelationalExpression '>' ShiftExpression
							| RelationalExpression OP_LE ShiftExpression
							| RelationalExpression OP_GE ShiftExpression
							| RelationalExpression INSTANCEOF TypeSpecifier '''

def p_EqualityExpression(p):
	''' EqualityExpression : RelationalExpression
						    | EqualityExpression OP_EQ RelationalExpression
						    | EqualityExpression OP_NE RelationalExpression '''

def p_AndExpression(p):
	'''AndExpression : EqualityExpression
					| AndExpression '&' EqualityExpression '''

def p_ExclusiveOrExpression(p):
	'''ExclusiveOrExpression : AndExpression
							| ExclusiveOrExpression '^' AndExpression '''

def p_InclusiveOrExpression(p):
	'''InclusiveOrExpression : ExclusiveOrExpression
							| InclusiveOrExpression '|' ExclusiveOrExpression '''

def p_ConditionalAndExpression(p):
	'''ConditionalAndExpression : InclusiveOrExpression
								| ConditionalAndExpression OP_LAND InclusiveOrExpression'''

def p_ConditionalOrExpression(p):
	'''ConditionalOrExpression : ConditionalAndExpression
								| ConditionalOrExpression OP_LOR ConditionalAndExpression '''

def p_ConditionalExpression(p):
	'''ConditionalExpression : ConditionalOrExpression
							| ConditionalOrExpression '?' Expression ':' ConditionalExpression'''

def p_AssignmentExpression(p):
	'''AssignmentExpression : ConditionalExpression
							| UnaryExpression AssignmentOperator AssignmentExpression'''

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

def p_Expression(p):
	'''Expression : AssignmentExpression'''

def p_ConstantExpression(p):
	'''ConstantExpression : ConditionalExpression'''

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"


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
parser = yacc.yacc(debug=True)
#parser.parse(debug=True)
# while True:
#    try:
#        s = raw_input('Input:')
#    except EOFError:
#        break
#    if not s: continue
#    result = parser.parse(s)
#    print result
if __name__ == '__main__':
	try:
		filename = sys.argv[1]
		f = open(filename)
		data = f.read()
		f.close()
	except EOFError:
		print "asedfgh"
    	# sys.stdout.write("Reading from standard input (type EOF to end):\n")
    	# data = sys.stdin.read()
    	if data:
    		result = parser.parse(data,debug=log)
    		# print result

call(["bash", "script.sh"])

   