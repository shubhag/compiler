import ply.lex as lex, sys

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

def t_IDENTIFIER(t):
    r'[a-zA-Z_$][a-zA-Z_$0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

#exp1 = r'\d+(e|E)(\+|\-)?\d+(f|F|d|D)?'              Digits ExponentPart FloatTypeSuffixopt
#exp2 = r'\.\d+((e|E)(\+|\-)?\d+)?(f|F|d|D)?'         . Digits ExponentPartopt FloatTypeSuffixopt
#exp3 = r'\d+\.\d*((e|E)(\+|\-)?\d+)?(f|F|d|D)?'      Digits . Digitsopt ExponentPartopt FloatTypeSuffixopt
#exp4 = r'\d+((e|E)(\+|\-)?\d+)?(f|F|d|D)'                     Digits ExponentPartopt FloatTypeSuffix

def t_FLOAT_LITERAL(t):
    r'(\d+(e|E)(\+|\-)?\d+(f|F|d|D)?|\.\d+((e|E)(\+|\-)?\d+)?(f|F|d|D)?|\d+\.\d*((e|E)(\+|\-)?\d+)?(f|F|d|D)?|\d+((e|E)(\+|\-)?\d+)?(f|F|d|D))'
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR_LITERAL(t):
    r"'([^'/]|\\(b|t|n|f|r|\"|'|\\|[0-9]+))'"
    return t

def t_STRING_LITERAL(t):
    r'"([^\'\\"]*)"'
    return t

def t_BOOL(t):
    r'(true|false)'
    t.value = bool(t.value)
    return t

def t_NULL(t):
    r'null'
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
    r'(\/\/.*|\/\*(\n|.)*\*\/)'
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
    print "Illegal character '%s'" % t.value[0]
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

#done
#IDENTIFIER
#keyword
#integer literal
#float literal
#character literal
#string literal without escape sequences
#boolean literal
#comment 
#newline

#"(\w|[^'\\]+|\\(b|t|n|f|r|"|'|\\|[0-9]+))"