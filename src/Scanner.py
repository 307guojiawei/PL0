import lex
import Symbol
symbol = Symbol.Symbol()
tokens = symbol.tokens

# Tokens
t_plus = r'\+'
t_minus = r'-'
t_mul = r'\*'
t_div = r'/'
t_eql = r'='
t_neq = r'<>'
t_leq = r'<='
t_lss = r'<'
t_geq = r'>='
t_gtr = r'>'
t_lparen = r'\('
t_rparen = r'\)'
t_comma = r','
t_semicolon = r';'
t_peroid = r'\.'
t_becomes = r':='
reserved_map = {}
def t_number(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ident(t):
    r'[A-Za-z_][\w_]*'
    for r in symbol.reserved:
        reserved_map[r] = r
    t.type = reserved_map.get(t.value, "ident")
    return t
# Ignored characters
t_ignore = " \t"
#comment
def t_comment(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
#skip \n
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
#error
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



def getScanner(address):
    scanner = lex.lex()
    try:
        f = open(address, 'r')
        #print(f.read())
    except:
        print("Error Open File")
        return
        #exit(2)
    scanner.input(f.read())
    f.close()
    return scanner


