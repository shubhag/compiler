import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens

#COMPILATION UNIT
#==================================================================================

def p_compilationunit(p):
	''' CompilationUnit : AnnotationsOne PACKAGE QualifiedIdentifier ';' ImportDeclarationMore TypeDeclarationMore 
						| ImportDeclarationMore TypeDeclarationMore '''


def p_importdeclarationmore(p):
	''' ImportDeclarationMore : ImportDeclarationMore ImportDeclaration
								| '''

def p_typedeclarationmore(p):
	''' TypeDeclarationMore : TypeDeclarationMore TypeDeclaration
							| '''

# CompilationUnit: 
#     [[Annotations] package QualifiedIdentifier ;]
#                                 {ImportDeclaration} {TypeDeclaration}

def p_importdeclaration(p):
	'''ImportDeclaration : IMPORT StaticOne Identifier DotIdentifierMore DotStarOne '''

def p_staticone(p):
	''' StaticOne : STATIC
					| '''

def p_dotstarone(p):
	''' DotStarOne : '.' '*' '''

def p_dotidentifiermore(p):
	''' DotIdentifierMore : DotIdentifierMore '.' Identifier
							| '''

# ImportDeclaration: 
#     import [static] Identifier { . Identifier } [. *] ;

def p_typedeclaration(p):
	'''TypeDeclaration : ClassOrInterfaceDeclaration
						| ';' '''

# TypeDeclaration: 
#     ClassOrInterfaceDeclaration
#     ;

def p_classorinterfacedeclaration(p):
	'''ClassOrInterfaceDeclaration : ModifierMore ClassDeclaration
									| ModifierMore InterfaceDeclaration '''

# ClassOrInterfaceDeclaration: 
#     {Modifier} (ClassDeclaration | InterfaceDeclaration)

def p_classdeclaration(p):
	''' ClassDeclaration : NormalClassDeclaration
						| EnumDeclaration '''

# ClassDeclaration: 
#     NormalClassDeclaration
#     EnumDeclaration

def p_interfacedeclaration(p):
	''' InterfaceDeclaration : NormalClassDeclaration
							| AnnotationTypeDeclaration '''

# InterfaceDeclaration: 
#     NormalInterfaceDeclaration
#     AnnotationTypeDeclaration

def p_normalclassdeclaration(p):
	''' NormalClassDeclaration : CLASS Identifier TypeParametersOne ExtendsTypeOne ImplementsTypeListOne ClassBody '''

def p_typeparametersone(p):
	''' TypeParametersOne : TypeParameters
							| '''

def p_extendstypeone(p):
	''' ExtendsTypeOne : EXTENDS Type 
						| '''

def p_implementstypelist(p):
	''' ImplementsTypeListOne : IMPLEMENTS TypeList
								| '''

# NormalClassDeclaration: 
#     class Identifier [TypeParameters]
#                                 [extends Type] [implements TypeList] ClassBody

def p_enumdeclaration(p):
	''' EnumDeclaration : ENUM Identifier ImplementsTypeListOne EnumBody '''

# EnumDeclaration:
#     enum Identifier [implements TypeList] EnumBody

def p_normalinterfacedeclaration(p):
	''' NormalInterfaceDeclaration : INTERFACE Identifier  TypeParametersOne ExtendListOne InterfaceBody '''

def p_extendlistone(p):
	''' ExtendListOne : EXTENDS TypeList 
						| '''

# NormalInterfaceDeclaration: 
#     interface Identifier [TypeParameters] [extends TypeList] InterfaceBody

def p_annotationtypedeclaration(p):
	'''AnnotationTypeDeclaration : '@' INTERFACE Identifier AnnotationTypeBody '''
# AnnotationTypeDeclaration:
#     @ interface Identifier AnnotationTypeBody

#----------------------------------------------------------------------------------

#IDENTIFIER
#==================================================================================
def p_identifier(p):
	'Identifier : IDENTIFIER'

def p_qualified_identifier(p):
	'QualifiedIdentifier : Identifier DotIdentifierMore '

def p_qualifiedidentifierlist(p):
	'QualifiedIdentifierList : QualifiedIdentifier CommaQualifiedIdentifierMore'

def p_commaqualifiedidentifiermore(p):
	'''CommaQualifiedIdentifierMore : CommaQualifiedIdentifierMore ',' QualifiedIdentifier 
									| '''

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
	'ReferenceType : Identifier TypeArgumentsOne DotIdentifierTypeArgumentsOneMore'

def p_typeargumentsone(p):
	'''TypeArgumentsOne : TypeArguments
						|'''

def p_dotidentifiertypeargumentsonemore(p):
	''' DotIdentifierTypeArgumentsOneMore : DotIdentifierTypeArgumentsOneMore '.' Identifier TypeArgumentsOne
											| '''

def p_typearguments(p):
	'''TypeArguments : '<' TypeArgument CommaTypeArgumentMore '>' '''

def p_commatypeargumentmore(p):
	''' CommaTypeArgumentMore : CommaTypeArgumentMore ',' TypeArgument 
								| '''

def p_typeargument(p):
	'''TypeArgument : ReferenceType
					| '?' 
					| '?' EXTENDS ReferenceType
					| '?' SUPER ReferenceType '''

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

#------------------------------------------------------------------------

#Nonwildarguments
#=========================================================================

def p_nonwildcardtypearguments(p):
	''' NonWildcardTypeArguments : '<' TypeList '>' '''

# NonWildcardTypeArguments:
#     < TypeList >

def p_typelist(p):
	''' TypeList : TypeList ',' ReferenceType
				| ReferenceType '''
 
# TypeList:  
#     ReferenceType { , ReferenceType }

def p_typeargumentsordiamond(p):
	'''TypeArgumentsOrDiamond : '<' '>'
								| TypeArguments '''

# TypeArgumentsOrDiamond:
#     < > 
#     TypeArguments

def p_nonwildcardtypeargumentsordiamond(p):
	'''NonWildcardTypeArgumentsOrDiamond : '<' '>'
										| NonWildcardTypeArguments '''

# NonWildcardTypeArgumentsOrDiamond:
#     < >
#     NonWildcardTypeArguments

def p_typeparameters(p):
	'''TypeParameters : '<' TypeParameter CommaTypeParameterMore '>' '''

def p_commatypeparametermore(p):
	''' CommaTypeParameterMore : CommaTypeParameterMore ',' TypeParameter
								| '''

# TypeParameters:
#     < TypeParameter { , TypeParameter } >

def p_typeparameter(p):
	''' TypeParameter : Identifier 
						| Identifier EXTENDS Bound '''

# TypeParameter:
#     Identifier [extends Bound]

def p_bound(p):
	'''Bound : ReferenceType AndReferenceTypeMore '''

def p_andreferencetypemore(p):
	'''AndReferenceTypeMore : AndReferenceTypeMore '&' ReferenceType 
							| '''
# Bound:  
#     ReferenceType { & ReferenceType }

#-----------------------------------------------------------------------------

#Modifier
#============================================================================

def p_modifier(p):
	''' Modifier : Annotation
				| PUBLIC 
				| PROTECTED 
				| PRIVATE 
				| STATIC 
				| ABSTRACT 
				| FINAL 
				| NATIVE 
				| SYNCHRONIZED 
				| TRANSIENT 
				| VOLATILE 
				| STRICTFP '''

# Modifier: 
#     Annotation
#     public
#     protected
#     private
#     static 
#     abstract
#     final
#     native
#     synchronized
#     transient
#     volatile
#     strictfp

def p_annotations(p):
	''' Annotations : Annotations Annotation
					| Annotation '''

# Annotations:
#     Annotation {Annotation}

def p_annotation(p):
	''' Annotation : '@' QualifiedIdentifier 
					| '@' QualifiedIdentifier '(' AnnotationElementOne ')' '''

def p_anotationelementone(p):
	''' AnnotationElementOne : AnnotationElement
								| '''
# Annotation:
#     @ QualifiedIdentifier [ ( [AnnotationElement] ) ]

def p_annotationelement(p):
	''' AnnotationElement : ElementValuePairs
							| ElementValue '''
# AnnotationElement:
#     ElementValuePairs
#     ElementValue

def p_elementvaluepairs(p):
	''' ElementValuePairs : ElementValuePair CommaElementValuePairMore '''

def p_commaelementvaluepairmore(p):
	''' CommaElementValuePairMore : CommaElementValuePairMore ',' ElementValuePair
									| '''
# ElementValuePairs:
#     ElementValuePair { , ElementValuePair }

def p_elementvaluepair(p):
	''' ElementValuePair : Identifier '=' ElementValue '''

# ElementValuePair:
#     Identifier = ElementValue
    
def p_elementvalue(p):
	''' ElementValue : Annotation
						| Expression1
						| ElementValueArrayInitializer '''

# ElementValue:
#     Annotation
#     Expression1 
#     ElementValueArrayInitializer

def p_elementvaluearrayinitializer(p):
	'''ElementValueArrayInitializer : ElementValueArrayInitializer ElementValuesOne CommaOne
									| '''

def p_elementvaluesone(p):
	''' ElementValuesOne : ElementValues
						| '''

# ElementValueArrayInitializer:
#     { [ElementValues] [,] }

def p_elementvalues(p):
	''' ElementValues : ElementValues ',' ElementValue 
						| ElementValue '''
# ElementValues:
#     ElementValue { , ElementValue }

#----------------------------------------------------------------------------------------------

#ClassBody
#==================================================================================

def p_classbody(p):
	''' ClassBody : '{' ClassBodyDeclarationMore '}' '''

# ClassBody: 
#     { { ClassBodyDeclaration } }

def p_classbodydeclaration(p):
	''' ClassBodyDeclaration : ';'
							| ModifierMore MemberDecl
							| StaticOne Block '''

# ClassBodyDeclaration:
#     ; 
#     {Modifier} MemberDecl
#     [static] Block

def p_memberdecl(p):
	''' MemberDecl : MethodOrFieldDecl
					| VOID Identifier VoidMethodDeclaratorRest
					| Identifier ConstructorDeclaratorRest
					| GenericMethodOrConstructorDecl
					| ClassDeclaration
					| InterfaceDeclaration '''
# MemberDecl:
#     MethodOrFieldDecl
#     void Identifier VoidMethodDeclaratorRest
#     Identifier ConstructorDeclaratorRest
#     GenericMethodOrConstructorDecl
#     ClassDeclaration
#     InterfaceDeclaration

def p_methodorfielddecl(p):
	''' MethodOrFieldDecl : Type Identifier MethodOrFieldRest '''

# MethodOrFieldDecl:
#     Type Identifier MethodOrFieldRest

def p_methodorfieldrest(p):
	''' MethodOrFieldRest : FieldDeclaratorsRest ';'
							| MethodDeclaratorRest '''
# MethodOrFieldRest:  
#     FieldDeclaratorsRest ;
#     MethodDeclaratorRest

def p_fielddeclaratorrest(p):
	''' FieldDeclaratorsRest : VariableDeclaratorRest CommaVariableDeclaratorMore '''

# FieldDeclaratorsRest:  
#     VariableDeclaratorRest { , VariableDeclarator }

def p_methoddeclaratorrest(p):
	''' MethodDeclaratorRest : FormalParameters OpenClosedParenMore ThrowsQualifiedIdentifierListOne BlockColonOr '''

def p_throwsqualifiedidentifierlistone(p):
	''' ThrowsQualifiedIdentifierListOne : THROWS QualifiedIdentifierList 
										| '''

def p_blockcolonor(p):
	''' BlockColonOr : Block
					| ';' '''

# MethodDeclaratorRest:
#     FormalParameters {[]} [throws QualifiedIdentifierList] (Block | ;)

def p_voidmethoddeclaratorrest(p):
	''' VoidMethodDeclaratorRest : FormalParameters ThrowsQualifiedIdentifierListOne BlockColonOr '''

# VoidMethodDeclaratorRest:
#     FormalParameters [throws QualifiedIdentifierList] (Block | ;)

def p_constructdeclaratorrest(p):
	'''ConstructorDeclaratorRest : FormalParameters ThrowsQualifiedIdentifierListOne Block '''

# ConstructorDeclaratorRest:
#     FormalParameters [throws QualifiedIdentifierList] Block

def p_genericmethodorconstructdecl(p):
	'''GenericMethodOrConstructorDecl : TypeParameters GenericMethodOrConstructorRest '''
# GenericMethodOrConstructorDecl:
#     TypeParameters GenericMethodOrConstructorRest

def p_genericmethodorconstructrest(p):
	'''GenericMethodOrConstructorRest : Type Identifier MethodDeclaratorRest
										| VOID Identifier MethodDeclaratorRest
										| Identifier ConstructorDeclaratorRest '''
# GenericMethodOrConstructorRest:
#     (Type | void) Identifier MethodDeclaratorRest
#     Identifier ConstructorDeclaratorRest
#------------------------------------------------------------------------------------------------

#INTERFACEBODY
#================================================================================

def p_interfacebody(p):
	''' InterfaceBody : '{' InterfaceBodyDeclarationMore '}' '''

def p_interfacebodydeclarationmore(p):
	''' InterfaceBodyDeclarationMore : InterfaceBodyDeclarationMore InterfaceBodyDeclaration
									| '''

# InterfaceBody: 
#     { { InterfaceBodyDeclaration } }

def p_interfacebodydeclaration(p):
	'''InterfaceBodyDeclaration : ';'
								| ModifierMore InterfaceMemberDecl '''

# InterfaceBodyDeclaration:
#     ; 
#     {Modifier} InterfaceMemberDecl

def p_interfacememberdecl(p):
	''' InterfaceMemberDecl : InterfaceMethodOrFieldDecl
							| VOID Identifier VoidInterfaceMethodDeclaratorRest
							| InterfaceGenericMethodDecl
							| ClassDeclaration
							| InterfaceDeclaration '''

# InterfaceMemberDecl:
#     InterfaceMethodOrFieldDecl
#     void Identifier VoidInterfaceMethodDeclaratorRest
#     InterfaceGenericMethodDecl
#     ClassDeclaration
#     InterfaceDeclaration

def p_interfacemethodorfielddecl(p):
	''' InterfaceMethodOrFieldDecl : Type Identifier InterfaceMethodOrFieldRest '''

# InterfaceMethodOrFieldDecl:
#     Type Identifier InterfaceMethodOrFieldRest

def p_interfacemethodorfieldrest(p):
	''' InterfaceMethodOrFieldRest : ConstantDeclaratorsRest ';'
									| InterfaceMethodDeclaratorRest '''

# InterfaceMethodOrFieldRest:
#     ConstantDeclaratorsRest ;
#     InterfaceMethodDeclaratorRest
def p_commadeclaratormore(p):
	''' CommaConstantDeclaratorMore : CommaConstantDeclaratorMore ',' ConstantDeclarator
									| '''

def p_constantdeclaratorsrest(p):
	''' ConstantDeclaratorsRest : ConstantDeclaratorRest CommaConstantDeclaratorMore '''



# ConstantDeclaratorsRest: 
#     ConstantDeclaratorRest { , ConstantDeclarator }

def p_constantdeclaratorrest(p):
	'''ConstantDeclaratorRest : OpenClosedParenMore '=' VariableInitializer '''

# ConstantDeclaratorRest: 
#     {[]} = VariableInitializer

def p_constantdeclarator(p):
	''' ConstantDeclarator : Identifier ConstantDeclaratorRest '''

# ConstantDeclarator: 
#     Identifier ConstantDeclaratorRest

def p_interfacemethoddeclaratorrest(p):
	''' InterfaceMethodDeclaratorRest : FormalParameters OpenClosedParenMore ThrowsQualifiedIdentifierListOne ';' '''

# InterfaceMethodDeclaratorRest:
#     FormalParameters {[]} [throws QualifiedIdentifierList] ; 

def p_voidinterfacemethoddeclaratorrest(p):
	''' VoidInterfaceMethodDeclaratorRest : FormalParameters ThrowsQualifiedIdentifierListOne ';' '''

# VoidInterfaceMethodDeclaratorRest:
#     FormalParameters [throws QualifiedIdentifierList] ;  

def p_interfacegenericmethoddecl(p):
	''' InterfaceGenericMethodDecl : TypeParameters TypeVoidOr Identifier InterfaceMethodDeclaratorRest '''

def p_typevoidor(p):
	''' TypeVoidOr : Type
					| VOID '''

# InterfaceGenericMethodDecl:
#     TypeParameters (Type | void) Identifier InterfaceMethodDeclaratorRest

#--------------------------------------------------------------------------------------------------------------
#FORMALPARAMETERS
#============================================================================

def p_formalparameters(p):
	'''FormalParameters : '(' ')'
						| '(' FormalParameterDecls ')' '''

# FormalParameters: 
#     ( [FormalParameterDecls] )

def p_formalparameterdecls(p):
	'''FormalParameterDecls : VariableModifierMore Type FormalParameterDeclsRest '''

# FormalParameterDecls: 
#     {VariableModifier}  Type FormalParameterDeclsRest

def p_variablemodifier(p):
	'''VariableModifier : FINAL
						| Annotation '''
# VariableModifier:
#     final
#     Annotation

def p_formalparameterdeclsrest(p):
	'''FormalParameterDeclsRest : VariableDeclaratorId ',' FormalParameterDecls
								| VariableDeclaratorId
								| '.' '.' '.' VariableDeclaratorId '''
# FormalParameterDeclsRest: 
#     VariableDeclaratorId [, FormalParameterDecls]
#     ... VariableDeclaratorId

def p_variabledeclaratorid(p):
	'''VariableDeclaratorId : Identifier OpenClosedParenMore '''

# VariableDeclaratorId:
#     Identifier {[]}

def p_variabledeclarators(p):
	'''VariableDeclarators : VariableDeclarator CommaVariableDeclaratorMore '''

# VariableDeclarators:
#     VariableDeclarator { , VariableDeclarator }

def p_variabledeclarator(p):
	'''VariableDeclarator : Identifier VariableDeclaratorRest '''

# VariableDeclarator:
#     Identifier VariableDeclaratorRest

def p_variabledeclaratorrest(p):
	''' VariableDeclaratorRest : OpenClosedParenMore 
								| OpenClosedParenMore '=' VariableInitializer '''

# VariableDeclaratorRest:
#     {[]} [ = VariableInitializer ]

def p_variableinitializer(p):
	'''VariableInitializer : ArrayInitializer
							| Expression '''
# VariableInitializer:
#     ArrayInitializer
#     Expression

def p_arrayinitializer(p):
	''' ArrayInitializer : '{' '}'
						| '{' VariableInitializer CommaVariableInitializerMore CommaOne '}' '''

def p_commavariableinitializermore(p):
	''' CommaVariableInitializerMore : CommaVariableInitializerMore ',' VariableInitializer 
									| '''

# ArrayInitializer:
#     { [ VariableInitializer { , VariableInitializer } [,] ] }

#-----------------------------------------------------------------------------

#BLOCK

def p_block(p):
	''' Block : '{' BlockStatements '}' '''

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
				| SWITCH ParExpression '{' SwitchBlockStatementGroups '}' 
				| WHILE ParExpression Statement
	   			| DO Statement WHILE ParExpression ';'
				| FOR '(' ForControl ')' Statement
				| BREAK ';'
				| BREAK Identifier ';'
				| CONTINUE ';'
				| CONTINUE Identifier ';'
				| RETURN ';'
				| RETURN Expression ';'
				| THROW Expression ';'
				| SYNCHRONIZED ParExpression Block
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

# Block: 
#     { BlockStatements }

# BlockStatements: 
#     { BlockStatement }

# BlockStatement:
#     LocalVariableDeclarationStatement
#     ClassOrInterfaceDeclaration
#     [Identifier :] Statement

# LocalVariableDeclarationStatement:
#     { VariableModifier }  Type VariableDeclarators ;

# Statement:
#     Block
#     ;
#     Identifier : Statement
#     StatementExpression ;
#     if ParExpression Statement [else Statement] 
#     assert Expression [: Expression] ;
#     switch ParExpression { SwitchBlockStatementGroups } 
#     while ParExpression Statement
#     do Statement while ParExpression ;
#     for ( ForControl ) Statement
#     break [Identifier] ;
#     continue [Identifier] ;
#     return [Expression] ;
#     throw Expression ;
#     synchronized ParExpression Block
#     try Block (Catches | [Catches] Finally)
#     try ResourceSpecification Block [Catches] [Finally]

# StatementExpression: 
#     Expression

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
	'''Resources : Resource ';' Resource 
				| Resource '''

def p_resource(p):
	''' Resource : VariableModifierMore ReferenceType VariableDeclaratorId '=' Expression '''

# Catches:
#     CatchClause { CatchClause }

# CatchClause:  
#     catch ( {VariableModifier} CatchType Identifier ) Block

# CatchType:
#     QualifiedIdentifier { | QualifiedIdentifier }

# Finally:
#     finally Block

# ResourceSpecification:
#     ( Resources [;] )

# Resources:
#     Resource { ; Resource }

# Resource:
#     {VariableModifier} ReferenceType VariableDeclaratorId = Expression 

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
	''' ForVarControl : VariableModifierMore Type VariableDeclaratorId ForVarControlRest '''

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

# SwitchBlockStatementGroups: 
#     { SwitchBlockStatementGroup }

# SwitchBlockStatementGroup: 
#     SwitchLabels BlockStatements

# SwitchLabels:
#     SwitchLabel { SwitchLabel }

# SwitchLabel: 
#     case Expression :
#     case EnumConstantName :
#     default :

# EnumConstantName:
#     Identifier



# ForControl:
#     ForVarControl
#     ForInit ; [Expression] ; [ForUpdate]

# ForVarControl:
#     {VariableModifier} Type VariableDeclaratorId  ForVarControlRest

# ForVarControlRest:
#     ForVariableDeclaratorsRest ; [Expression] ; [ForUpdate]
#     : Expression

# ForVariableDeclaratorsRest:
#     [= VariableInitializer] { , VariableDeclarator }

# ForInit: 
# ForUpdate:
#     StatementExpression { , StatementExpression }    
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
	'''Literal : INT_LITERAL
				| FLOAT_LITERAL
				| CHAR_LITERAL
				| STRING_LITERAL
				| BOOL
				| NULL '''

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

#-----------------------------------------------------------------------------------------

#ENUM
#=========================================================================================

def p_enumbody(p):
	'''EnumBody : '{' EnumConstantsOne CommaOne EnumBodyDeclarationsOne '}' '''

def p_commaone(p):
	''' CommaOne : ',' 
				| '''

def p_enumconstantsone(p):
	''' EnumConstantsOne : EnumConstants 
						| '''

def p_enumbodydeclarationsone(p):
	'''EnumBodyDeclarationsOne : EnumBodyDeclarations 
								| '''

# EnumBody:
#     { [EnumConstants] [,] [EnumBodyDeclarations] }

def p_enumconstatnts(p):
	'''EnumConstants : EnumConstant
    				| EnumConstants ',' EnumConstant '''

# EnumConstants:
#     EnumConstant
#     EnumConstants , EnumConstant

def p_enumconstant(p):
	'''EnumConstant : AnnotationsOne Identifier ArgumentsOne ClassBodyOne '''

def p_argumentsone(p):
	''' ArgumentsOne : Arguments
						| '''

def p_classbodyone(p):
	''' ClassBodyOne : ClassBody
					| '''

def p_annotationsaone(p):
	''' AnnotationsOne : Annotations
						| '''


# EnumConstant:
#     [Annotations] Identifier [Arguments] [ClassBody]

def p_enumbodydeclarations(p):
	''' EnumBodyDeclarations : ';' ClassBodyDeclarationMore '''

def p_classdeclarationmore(p):
	''' ClassBodyDeclarationMore : ClassBodyDeclarationMore ClassBodyDeclaration
							| '''

# EnumBodyDeclarations:
#     ; {ClassBodyDeclaration}

def p_annotationtypebody(p):
	''' AnnotationTypeBody : '{' '}'
							| '{' AnnotationTypeElementDeclarations '}' '''

# AnnotationTypeBody:
#     { [AnnotationTypeElementDeclarations] }

def p_annotationtypeelementdeclarations(p):
	'''AnnotationTypeElementDeclarations : AnnotationTypeElementDeclaration
										|	AnnotationTypeElementDeclarations AnnotationTypeElementDeclaration '''

# AnnotationTypeElementDeclarations:
#     AnnotationTypeElementDeclaration
#     AnnotationTypeElementDeclarations AnnotationTypeElementDeclaration

def p_annotationtypeelementdeclaration(p):
	'''AnnotationTypeElementDeclaration : ModifierMore AnnotationTypeElementRest '''

def p_modifiermore(p):
	'''ModifierMore : ModifierMore Modifier
					| '''

# AnnotationTypeElementDeclaration:
#     {Modifier} AnnotationTypeElementRest

def p_annotationtypeelementrest(p):
	'''AnnotationTypeElementRest : Type Identifier AnnotationMethodOrConstantRest ';'
    							|	ClassDeclaration
    							|	InterfaceDeclaration
    							|	EnumDeclaration  
    							| 	AnnotationTypeDeclaration '''

# AnnotationTypeElementRest:
#     Type Identifier AnnotationMethodOrConstantRest ;
#     ClassDeclaration
#     InterfaceDeclaration
#     EnumDeclaration  
#     AnnotationTypeDeclaration

def p_annotationmethodorconstatntrest(p):
	'''AnnotationMethodOrConstantRest : AnnotationMethodRest
    									| ConstantDeclaratorsRest '''  

# AnnotationMethodOrConstantRest:
#     AnnotationMethodRest
#     ConstantDeclaratorsRest  

def p_annotationmethodrest(p):
	'''AnnotationMethodRest : '(' ')' OpenClosedParenOne DEFAULT ElementValue
							| '(' ')' OpenClosedParenOne '''

def p_opencloasedparenone(p):
	'''OpenClosedParenOne : '[' ']'
							| '''
# AnnotationMethodRest:
#     ( ) [[]] [default ElementValue]

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input('Input:')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print result