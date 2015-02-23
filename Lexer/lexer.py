#!/usr/bin/env python
import ply.lex as lex, sys
from ply.lex import TOKEN

reserved = {
    'abstract'  :   'ABSTRACT',      
    'assert'    :   'ASSERT',             
    'boolean'   :   'BOOLEAN',              
    'break'     :   'BREAK',              
    'byte'      :   'BYTE',                
    'case'      :   'CASE',                 
    'catch'     :   'CATCH',
    'char'      :   'CHAR',                    
    'class'     :   'CLASS',                     
    'const'     :   'CONST',              
    'continue'  :   'CONTINUE',   
    'default'   :   'DEFAULT',
    'do'        :   'DO',        
    'double'    :   'DOUBLE',     
    'else'      :   'ELSE',       
    'enum'      :   'ENUM',       
    'extends'   :   'EXTENDS',    
    'final'     :   'FINAL',      
    'finally'   :   'FINALLY',    
    'float'     :   'FLOAT',      
    'for'       :   'FOR',       
    'if'        :   'IF',        
    'goto'      :   'GOTO',      
    'implements':   'IMPLEMENTS',
    'import'    :   'IMPORT',
    'instanceof':   'INSTANCEOF',
    'int'       :   'INT',
    'interface' :   'INTERFACE',
    'long'      :   'LONG',
    'native'    :   'NATIVE',
    'new'       :   'NEW',
    'package'   :   'PACKAGE',
    'private'   :   'PRIVATE',
    'protected' :   'PROTECTED',
    'public'    :   'PUBLIC',
    'return'    :   'RETURN',
    'short'     :   'SHORT',
    'static'    :   'STATIC',   
    'strictfp'  :   'STRICTFP',
    'super'     :   'SUPER',
    'switch'    :   'SWITCH',  
    'synchronized': 'SYNCRONIZED',
    'this'      :   'THIS',
    'throw'     :   'THROW',  
    'throws'    :   'THROWS',
    'transient' :   'TRANSIENT',
    'try'       :   'TRY',  
    'void'      :   'VOID',  
    'volatile'  :   'VOLATILE',
    'while'     :   'WHILE'      
}

tokens = [
    'IDENTIFIER',
    'FLOAT_LITERAL',
    'INT_LITERAL',
    'CHAR_LITERAL',
    'STRING_LITERAL',
    'BOOL',
    'NULL',
    'OPT_EQ',
    'OPT_COMPARE',
    'OPT_AND_OR',
    'OPT_INC_DEC',
    'OPT_SOME',          #name it differently
    'COMMENT',
    'IGNORE_WHITESPACE'
] + list(reserved.values())

literals =  [ '(', ')', '{' ,'}' ,'[', ']', ';', ',', '.',
            '=', '>', '<', '!', '~', '?', ':',               #operators
            '+', '-', '*', '/', '&', '|', '^', '%'           
            ]

def t_NULL(t):
    r'null'
    return t

def t_BOOL(t):
    r'(true|false)'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_$][a-zA-Z_$0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

#exp1 = r'\d+(e|E)(\+|\-)?\d+(f|F|d|D)?'              Digits ExponentPart FloatTypeSuffixopt
#exp2 = r'\.\d+((e|E)(\+|\-)?\d+)?(f|F|d|D)?'         . Digits ExponentPartopt FloatTypeSuffixopt
#exp3 = r'\d+\.\d*((e|E)(\+|\-)?\d+)?(f|F|d|D)?'      Digits . Digitsopt ExponentPartopt FloatTypeSuffixopt
#exp4 = r'\d+((e|E)(\+|\-)?\d+)?(f|F|d|D)'                     Digits ExponentPartopt FloatTypeSuffix



digits = r'(\d(\d|_)*\d|\d)'
nonzerodigit = r'(1|2|3|4|5|6|7|8|9)'
decimal = r'(0|' + nonzerodigit + digits + r'*|' + nonzerodigit + r'_+' + digits + r')(l|L)?' 

hexdigit = r'(0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f|A|B|C|D|E|F)'
hexdigits = r'(' + hexdigit + r'(0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f|A|B|C|D|E|F|_)*' + hexdigit + r'|' + hexdigit + r')' 
hexnumeral =  r'0(x|X)'+ hexdigits + r'(l|L)?'

octaldigit = r'(0|1|2|3|4|5|6|7)'
octaldigits = r'(' + octaldigit + r'(0|1|2|3|4|5|6|7|_)*' + octaldigit + r'|' + octaldigit + r')' 
octalnumeral = r'0(' + octaldigits + r'|_+' +  octaldigits + r')' + r'(l|L)?'

binarydigit = r'(0|1)'
binarydigits = r'(' + binarydigit + r'(0|1|_)*' + binarydigit + r'|' + binarydigit + r')' 
binarynumeral = r'0(b|B)' + binarydigits + r'(l|L)?'

exponentpart = r'(e|E)(\+|\-)?' + digits
floattype = r'(f|F|d|D)?'
decimalfloat1 = digits + r'\.'+ digits + r'*((e|E)(\+|\-)?\d+)?(f|F|d|D)?'
decimalfloat2 = r'\.' + digits + r'((e|E)(\+|\-)?\d+)?(f|F|d|D)?'
decimalfloat3 = digits + exponentpart + r'(f|F|d|D)?'
decimalfloat4 = digits + r'((e|E)(\+|\-)?\d+)?(f|F|d|D)' 

floattype = r'(' + decimalfloat1 + r'|' + decimalfloat2 + r'|' + decimalfloat3 + r'|' + decimalfloat4 + r')'

@TOKEN(floattype)
def t_FLOAT_LITERAL(t):
#    r'(\d+(e|E)(\+|\-)?\d+(f|F|d|D)?|\.\d+((e|E)(\+|\-)?\d+)?(f|F|d|D)?|\d+\.\d*((e|E)(\+|\-)?\d+)?(f|F|d|D)?|\d+((e|E)(\+|\-)?\d+)?(f|F|d|D))'
    return t

integer = r'(' + hexnumeral + r'|' + octalnumeral + r'|' + binarynumeral + r'|' + decimal + r')'


@TOKEN(integer)
def t_INT_LITERAL(t):
    return t

charliteral = r"'(\\'|[^'/]|\\(b|t|n|f|r|\"|\\|" + octaldigit + r"|"+ octaldigit + r"{2}|[0-3]" + octaldigit + r"{2}))'"  

@TOKEN(charliteral)
def t_CHAR_LITERAL(t):
#    r"'(\\'|[^'/]|\\(b|t|n|f|r|\"|\\))'"
    return t

def t_STRING_LITERAL(t):
    r'".*"'
#    r'"([^\\"]*)"'
    return t

def t_OPT_COMPARE(t):
    r'(==|<=|>=|!=)'
    return t

def t_OPT_AND_OR(t):
    r'(&&|\|\|)'
    return t

def t_OPT_INC_DEC(t):
    r'(\+\+|--)'
    return t

def t_OPT_EQ(t):
    r'(\+=|\-=|\*=|\/=|\&=|\|=|\^=|\%=|<<=|>>=|>>>=)'
    return t

def t_OPT_SOME(t):
    r'(<<|>>|>>>)'
    return t
    
#comments
def t_COMMENT(t):
    r'(\/\/.*|\/\*(.|[\r\n])*?\*\/)'
    # sys.stdout.write("%s" % (t.value))
    # pass
    return t
    # No return value. Token discarded

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    global output
    sys.stdout.write("\t//%s" % (output))
    sys.stdout.write("%s" % (t.value))
    output = ""

# A string containing ignored characters (spaces and tabs)
def t_IGNORE_WHITESPACE(t):
	r'(\s|\t)'
	sys.stdout.write("%s" % (t.value))
#t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "\n ERROR:    Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()

output = ""
#read input from stdin or a file
if __name__ == '__main__':
#    lex.runmain()
	# global output 
    try:
        filename = sys.argv[1]
        f = open(filename)
        data = f.read()
        f.close()
    except IndexError:
        sys.stdout.write("Reading from standard input (type EOF to end):\n")
        data = sys.stdin.read()

    if lexer:
        _input = lexer.input
    else:
        _input = input
    _input(data)
    if lexer:
        _token = lexer.token
    else:
        _token = token

    while 1:
        tok = _token()
        if not tok: 
        	sys.stdout.write("\t//%s\n" % (output))
        	break
        sys.stdout.write("%s" % (tok.value))
        output = output + " " + tok.type
        # print output
#        sys.stdout.write("(%s,%r,%d,%d)\n" % (tok.type, tok.value, tok.lineno,tok.lexpos))
