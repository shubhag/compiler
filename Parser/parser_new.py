import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens



#IDENTIFIER
#==================================================================================
def p_identifier(p):
	'Identifier : IDENTIFIER'

def p_dotidentifiermore(p):
	'''DotIdentifierMore : DotIdentifierMore '.' Identifier 
						| '''

def p_qualified_identifier(p):
	''' QualifiedIdentifier : Identifier '{' '.' Identifier '}' '''

def p_qualifiedidentifierlist(p):
	'''QualifiedIdentifierList : QualifiedIdentifier '{' ',' QualifiedIdentifier '}' '''

# Identifier:
#     IDENTIFIER

# QualifiedIdentifier:
#     Identifier { . Identifier }

# QualifiedIdentifierList: 
#     QualifiedIdentifier { , QualifiedIdentifier }
#--------------------------------------------------------------------------------------

#TYPE
#==================================================================================

def p_type(p):
	'''Type : BasicType OpenClosedParenMore
			| ReferenceType OpenClosedParenMore '''

def p_openclosedparenmore(p):
	''' OpenClosedParenMore : OpenClosedParenMore '[' ']'
							| '''

def p_basictype(p):
	'''BasicType : BYTE
				| SHORT
				| CHAR
				| INT
				| LONG
				| FLOAT
				| DOUBLE
				| BOOLEAN '''

def p_referencetype(p):
	'''ReferenceType : Identifier TypeArgumentsOne '{' '.' Identifier TypeArgumentsOne '}' '''

def p_typeargumentsone(p):
	'''TypeArgumentsOne : TypeArguments
						|'''

def p_typearguments(p):
	'''TypeArguments : '<' TypeArgument '{' ',' TypeArgument '}' '>' '''

def p_commatypeargumentmore(p):
	''' CommaTypeArgumentMore : CommaTypeArgumentMore ',' TypeArgument 
								| '''

def p_typeargument(p):
	'''TypeArgument : ReferenceType
					| '?' '[' EXTENDS ReferenceType ']'
					| '?' '[' SUPER ReferenceType ']' ''' 

# Type:
#     BasicType {[]}
#     ReferenceType  {[]}

# BasicType: 
#     byte
#     short
#     char
#     int
#     long
#     float
#     double
#     boolean

# ReferenceType:
#     Identifier [TypeArguments] { . Identifier [TypeArguments] }

# TypeArguments: 
#     < TypeArgument { , TypeArgument } >

# TypeArgument:  
#     ReferenceType
#     ? [ (extends | super) ReferenceType ]
#-----------------------------------------------------------------------------

#BLOCK

def p_block(p):
	''' Block : Block BlockStatements
				| '''

def p_blockstatements(p):
	''' BlockStatements : BlockStatements  BlockStatement
						| '''

def p_blockstatement(p):
	''' BlockStatement : LocalVariableDeclarationStatement
						| ClassOrInterfaceDeclaration
						| Statement
						| Identifier ':' Statement '''

def p_localvariableDeclarationstatement(p):
	'''LocalVariableDeclarationStatement : VariableModifierMore Type VariableDeclarators ';' '''

def p_variablemodifiermore(p):
	'''VariableModifierMore : VariableModifierMore VariableModifier
							| '''

def p_statement(p):
	'''Statement : Block
				| ';'
				| Identifier ':' Statement
				| StatementExpression ';'
				| IF ParExpression Statement 
				| IF ParExpression Statement ELSE Statement
				| ASSERT Expression ';'
				| ASSERT Expression ':' Expression ';'
				| FOR '(' ForControl ')' Statement
				| BREAK ';'
				| BREAK Identifier ';'
				| CONTINUE ';'
				| CONTINUE Identifier ';'
				| RETURN ';'
				| RETURN Expression ';'
				| THROW Expression ';'
				| SYNCRONIZED ParExpression Block
				| TRY Block Catches
				| TRY Block CatchesOne Finally
				| TRY ResourceSpecification Block CatchesOne FinallyOne'''

def p_catchesone(p):
	''' CatchesOne : Catches
					| '''

def p_finallyone(p):
	''' FinallyOne : Finally 
					| '''

def p_statementexpression(p):
	'StatementExpression : Expression '

#------------------------------------------------------------------------------------------------

#CATCHES 
#================================================================================================

def p_catches(p):
	'''Catches : Catches CatchClause 
				| CatchClause '''

def p_catchclause(p):
	'''CatchClause : CATCH '(' VariableModifierMore CatchType Identifier ')' Block '''

def p_catchtype(p):
	'''CatchType : CatchType '|' QualifiedIdentifier 
				| QualifiedIdentifier '''

def p_finally(p):
	'Finally : FINALLY Block'

def p_resourcespecification(p):
	''' ResourceSpecification : '(' Resources ')'
								| '(' Resources ';' ')' '''

def p_resources(p):
	'''Resources : Resources ';' Resource 
				| Resource '''

def p_resource(p):
	''' Resource : VariableModifierMore ReferenceType VariableDeclaratorId '=' Expression '''

#-------------------------------------------------------------------------------------------

#SWITCHBLOCK
#===========================================================================================

def p_switchblockstatementgroups(p):
	''' SwitchBlockStatementGroups : SwitchBlockStatementGroups SwitchBlockStatementGroup
									| SwitchBlockStatementGroup '''

def p_switchblockstatementgroup(p):
	'SwitchBlockStatementGroup : SwitchLabels BlockStatements '

def p_switchlabels(p):
	''' SwitchLabels : SwitchLabels SwitchLabel
					| SwitchLabel '''

def p_switchlabel(p):
	''' SwitchLabel : CASE Expression ':'
					| CASE EnumConstantName ':'
					| DEFAULT ':' '''

def p_enumconstantname(p):
	'EnumConstantName : Identifier '

def p_forcontrol(p):
	''' ForControl : ForVarControl 
					| ForInit ';' ExpressionOne ';' ForUpdateOne '''

def p_expressionone(p):
	''' ExpressionOne : Expression
						| '''

def p_forupdateone(p):
	''' ForUpdateOne : ForUpdate 
					| '''

def p_forvarcontrol(p):
	''' ForControl : VariableModifierMore Type VariableDeclaratorId ForVarControlRest '''

def p_forvarcontrolrest(p):
	''' ForVarControlRest : ForVariableDeclaratorsRest ';' ExpressionOne ';' ForUpdateOne 
							| ':' Expression '''

def p_forvariabledeclaratorsrest(p):
	''' ForVariableDeclaratorsRest : EqualVariableInitializerOne CommaVariableDeclaratorMore '''

def p_equalvariableinitializerone(p):
	''' EqualVariableInitializerOne : '=' VariableInitializer
									| '''
 
 def p_commavariabledeclaratormore(p):
 	''' CommaVariableDeclaratorMore : CommaVariableDeclaratorMore ',' VariableDeclarator
 									| '''

def p_forinit(p):
	'''ForInit : '''

def p_forupdate(p):
	''' ForUpdate : StatementExpression CommaStatementExpressionMore '''

def p_commastatementexpressionmore(p):
	''' CommaStatementExpressionMore : CommaStatementExpressionMore ',' StatementExpression 
	 									| '''

#---------------------------------------------------------------------------------------------

#EXPRESSION
#====================================================================
def p_expression(p):
	'''Expression : Expression1
					| Expression1 AssignmentOperator Expression1'''

def p_assignmentoperator(p):
	'''AssignmentOperator : '='
							| OPT_EQ '''

def p_expression1(p):
	'''Expression1 : Expression2 
					| Expression2 Expression1Rest '''

def p_expression1rest(p):
	'''Expression1Rest : '?' Expression ':' Expression1 '''

def p_expression2(p):
	'''Expression2 : Expression3 
					| Expression3 Expression2Rest '''

def p_expression2rest(p):
	'''Expression2Rest : INSTANCEOF Type
						| InfixOpExpression3More '''

def p_infixopexpression3more(p):
	'''InfixOpExpression3More : InfixOpExpression3More InfixOp Expression3
								| '''

#-----------------------------------------------------------------------------------

#Infix OPERATOR
#===================================================================================

def p_infixop(p):
	'''InfixOp : OPT_AND_OR
				| '|'
				| '^'
				| '&'
				| OPT_COMPARE
				| '>'
				| '<'
				| OPT_SOME
				| '+'
				| '-'
				| '*'
				| '/'
				| '%' '''

def p_expressionortype(p):
	'''ExpressionOrType : Expression 
						| Type '''

def p_expression3(p):
	''' Expression3 : PrefixOp Expression3
					| '(' ExpressionOrType ')' Expression3
					| Primary SelectorMore PostfixOpMore '''

def p_selectormore(p):
	''' SelectorMore : SelectorMore Selector 
					| '''

def p_postfixopmore(p):
	''' PostfixOpMore : PostfixOpMore PostfixOp
						| '''

def p_prefixop(p):
	''' PrefixOp : OPT_INC_DEC 
					| '!'
					| '~'
					| '+'
					| '-' '''

def p_postfixop(p):
	'''PostfixOp : OPT_INC_DEC '''

#----------------------------------------------------------------------------------

#PRIMARY 

def p_primary(p):
	'''Primary : Literal
				| ParExpression
				| THIS 
				| THIS Arguments
				| SUPER SuperSuffix
				| NEW Creator
				| NonWildcardTypeArguments ExplicitGenericInvocationSuffix
				| NonWildcardTypeArguments THIS Arguments
				| Identifier DotIdentifierMore IdentifierSuffix
				| Identifier DotIdentifierMore 
				| BasicType OpenClosedParenMore '.' CLASS
				| VOID '.' CLASS '''
# Primary: 
#     Literal
#     ParExpression
#     this [Arguments]
#     super SuperSuffix
#     new Creator
#     NonWildcardTypeArguments (ExplicitGenericInvocationSuffix | this Arguments)
#     Identifier { . Identifier } [IdentifierSuffix]
#     BasicType {[]} . class
#     void . class

def p_literal(p):
	'''Literal : IntegerLiteral
				| FloatingPointLiteral
				| CharacterLiteral
				| StringLiteral
				| BooleanLiteral
				| NullLiteral '''

# Literal:
#     IntegerLiteral
#     FloatingPointLiteral
#     CharacterLiteral 	
#     StringLiteral 	
#     BooleanLiteral
#     NullLiteral

def p_parexpression(p):
	''' ParExpression : '(' Expression ')' '''

#ParExpression: 
#     ( Expression )

def p_arguments(p):
	'''Arguments : '(' ')' 
				| '(' Expression CommaExpressionMore ')' '''

# Arguments:
#     ( [ Expression { , Expression } ] )


def p_commaexpressionmore(p):
	'''CommaExpressionMore : CommaExpressionMore ',' Expression 
							| '''

def p_supersuffix(p):
	''' SuperSuffix : Arguments
					| '.' Identifier 
					| '.' Identifier Arguments '''

# SuperSuffix: 
#     Arguments 
#     . Identifier [Arguments]

def p_explixitgenericinvocationsuffix(p):
	'''ExplicitGenericInvocationSuffix : SUPER SuperSuffix
										| Identifier Arguments '''
# ExplicitGenericInvocationSuffix: 
#     super SuperSuffix
#     Identifier Arguments

#------------------------------------------------------------------------------------

#CREATOR 
#==================================================================================

def p_creator(p):
	'''Creator : NonWildcardTypeArguments CreatedName ClassCreatorRest
				| CreatedName ClassCreatorRest
				| CreatedName ArrayCreatorRest '''

# Creator:  
#     NonWildcardTypeArguments CreatedName ClassCreatorRest
#     CreatedName (ClassCreatorRest | ArrayCreatorRest)

def p_createdname(p):
	''' CreatedName : Identifier TypeArgumentsOrDiamondOne DotIdentifierTypeArgumentsOrDiamondOneMore '''

def p_dotidentifiertypeargumentsordiamondonemore(p):
	''' DotIdentifierTypeArgumentsOrDiamondOneMore : DotIdentifierTypeArgumentsOrDiamondOneMore '.' Identifier TypeArgumentsOrDiamondOne 
													| '''
def p_typeargumentsordiamondone(p):
	''' TypeArgumentsOrDiamondOne : TypeArgumentsOrDiamond
									| '''
# CreatedName:   
#     Identifier [TypeArgumentsOrDiamond] { . Identifier [TypeArgumentsOrDiamond] }

def p_classcreatorrest(p):
	''' ClassCreatorRest : Arguments 
						| Arguments ClassBody '''

# ClassCreatorRest: 
#     Arguments [ClassBody]

def p_arraycreatorrest(p):
	'''ArrayCreatorRest : '[' ']' OpenClosedParenMore ArrayInitializer
						| '[' Expression ']' SqparenExpressionSqparenMore OpenClosedParenMore '''

def p_sqparenexpressionsqparenmore(p):
	'''SqparenExpressionSqparenMore : SqparenExpressionSqparenMore '[' Expression ']'
									| '''

# ArrayCreatorRest:
#     [ (] {[]} ArrayInitializer  |  Expression ] {[ Expression ]} {[]})

def p_identifiersuffix(p):
	''' IdentifierSuffix : '[' OpenClosedParenMore '.' CLASS ']'  
						| '[' Expression ']'
						| Arguments
						| '.' CLASS 
						| '.' ExplicitGenericInvocation
						| '.' THIS
						| '.' SUPER Arguments
						| '.' NEW NonWildcardTypeArguments InnerCreator
						| '.' NEW InnerCreator '''

# IdentifierSuffix:
#     [ ({[]} . class | Expression) ]
#     Arguments 
#     . (class | ExplicitGenericInvocation | this | super Arguments |
#                                 new [NonWildcardTypeArguments] InnerCreator)

def p_explicitgenericinvocation(p):
	'ExplicitGenericInvocation : NonWildcardTypeArguments ExplicitGenericInvocationSuffix'

# ExplicitGenericInvocation:
#     NonWildcardTypeArguments ExplicitGenericInvocationSuffix


def p_innercreator(p):
	'''InnerCreator : Identifier ClassCreatorRest
					| Identifier NonWildcardTypeArgumentsOrDiamond ClassCreatorRest '''


# InnerCreator:  
#     Identifier [NonWildcardTypeArgumentsOrDiamond] ClassCreatorRest

def p_selector(p):
	'''Selector : '.' Identifier 
				| '.' Identifier Arguments
				| '.' ExplicitGenericInvocation
				| '.' THIS
				| '.' SUPER SuperSuffix
				| '.' NEW InnerCreator
				| '.' NEW NonWildcardTypeArguments InnerCreator
				| '[' Expression ']' '''

# Selector:
#     . Identifier [Arguments]
#     . ExplicitGenericInvocation
#     . this
#     . super SuperSuffix
#     . new [NonWildcardTypeArguments] InnerCreator
#     [ Expression ]

