import ply.lex as lex

tokens = (
    'KEYWORD_SECRET',
    'KEYWORD_PUBLIC',
    'KEYWORD_SEND',
    'KEYWORD_ENCRYPT',
    'ID',
    'ASSIGN',  # =
    'SEMI',    # ;
    'NUMBER',
    'LPAREN',
    'RPAREN',
)

t_ASSIGN = r'='
t_SEMI = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_KEYWORD_SECRET(t):
    r'secret'
    return t

def t_KEYWORD_PUBLIC(t):
    r'public'
    return t

def t_KEYWORD_SEND(t):
    r'send'
    return t

def t_KEYWORD_ENCRYPT(t):
    r'encrypt'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    reserved = {
        'secret': 'KEYWORD_SECRET',
        'public': 'KEYWORD_PUBLIC',
        'send': 'KEYWORD_SEND',
        'encrypt': 'KEYWORD_ENCRYPT',
    }
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
