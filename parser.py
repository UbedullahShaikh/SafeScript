import ply.yacc as yacc
from lexer import tokens
import symbol_table
import semantic_analyzer
import tac_generator

# --- Grammar Rules ---

def p_program(p):
    'program : statements'
    pass

def p_statements_multiple(p):
    'statements : statement statements'
    pass

def p_statements_empty(p):
    'statements : '
    pass

def p_statement_secret(p):
    'statement : KEYWORD_SECRET ID ASSIGN expression SEMI'
    var_name = p[2]
    value = p[4]
    symbol_table.add_symbol(var_name, "Secret", tainted=True)
    t = tac_generator.new_temp()
    tac_generator.emit(f"{t} = {value}")
    tac_generator.emit(f"{var_name} = {t}")

def p_statement_encrypt(p):
    'statement : ID ASSIGN KEYWORD_ENCRYPT LPAREN ID RPAREN SEMI'
    target = p[1]
    source = p[5]
    semantic_analyzer.mark_safe(target)
    t = tac_generator.new_temp()
    tac_generator.emit(f"{t} = encrypt({source})")
    tac_generator.emit(f"{target} = {t}")

def p_statement_send(p):
    'statement : KEYWORD_SEND LPAREN ID RPAREN SEMI'
    var_name = p[3]
    semantic_analyzer.check_security(var_name)
    tac_generator.emit(f"send({var_name})")

# --- Control Flow Rules ---

def p_if_head(p):
    'if_head : KEYWORD_IF LPAREN expression RPAREN'
    cond = p[3]
    l_end = tac_generator.new_label()
    tac_generator.emit(f"ifFalse {cond} goto {l_end}")
    p[0] = l_end

def p_statement_if(p):
    'statement : if_head LBRACE statements RBRACE'
    l_end = p[1]
    tac_generator.emit_label(l_end)

# --- Expression Rules ---

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression GT expression
                  | expression LT expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
        print(f"[Optimization] Constant Folding: {p[1]} + {p[3]} = {p[0]}")
    elif p[2] == '-':
        p[0] = p[1] - p[3]
        print(f"[Optimization] Constant Folding: {p[1]} - {p[3]} = {p[0]}")
    elif p[2] == '>':
        t = tac_generator.new_temp()
        tac_generator.emit(f"{t} = {p[1]} > {p[3]}")
        p[0] = t
    elif p[2] == '<':
        t = tac_generator.new_temp()
        tac_generator.emit(f"{t} = {p[1]} < {p[3]}")
        p[0] = t

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_id(p):
    'expression : ID'
    p[0] = p[1]

def p_error(p):
    print("Syntax Error!")

parser = yacc.yacc()
