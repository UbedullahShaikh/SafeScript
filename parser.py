import ply.yacc as yacc
from lexer import tokens
import symbol_table
import semantic_analyzer
import tac_generator

# --- Grammar Rules ---

def p_statement_secret(p):
    'statement : KEYWORD_SECRET ID ASSIGN expression SEMI'
    var_name = p[2]
    value = p[4]
    
    # 1. Add to Symbol Table
    symbol_table.add_symbol(var_name, "Secret", tainted=True)
    
    # 2. Generate Code
    t = tac_generator.new_temp()
    tac_generator.emit(f"{t} = {value}")
    tac_generator.emit(f"{var_name} = {t}")

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
        print(f"[Optimization] Constant Folding: {p[1]} + {p[3]} = {p[0]}")
    elif p[2] == '-':
        p[0] = p[1] - p[3]
        print(f"[Optimization] Constant Folding: {p[1]} - {p[3]} = {p[0]}")

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_statement_encrypt(p):
    'statement : ID ASSIGN KEYWORD_ENCRYPT LPAREN ID RPAREN SEMI'
    target = p[1]
    source = p[5]
    
    # 1. Mark as Safe
    semantic_analyzer.mark_safe(target)
    
    # 2. Generate Code
    t = tac_generator.new_temp()
    tac_generator.emit(f"{t} = encrypt({source})")
    tac_generator.emit(f"{target} = {t}")

def p_statement_send(p):
    'statement : KEYWORD_SEND LPAREN ID RPAREN SEMI'
    var_name = p[3]
    
    # 1. Security Check
    semantic_analyzer.check_security(var_name)
    
    # 2. Generate Code
    tac_generator.emit(f"send({var_name})")

def p_error(p):
    print("Syntax Error!")

parser = yacc.yacc()
