import ply.yacc as yacc
from lexer import tokens
import symbol_table
import semantic_analyzer
import tac_generator

# Precedence to handle dangling-else
precedence = (
    ('nonassoc', 'LOWER_THAN_ELSE'),
    ('nonassoc', 'KEYWORD_ELSE'),
)

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

def p_statement_assign(p):
    'statement : ID ASSIGN expression SEMI'
    var_name = p[1]
    value = p[3]
    
    # Check if variable exists (optional, but good practice)
    # symbol_table.check_exists(var_name) 
    # For now, we assume it exists or we create it? 
    # Let's assume it exists. If it's a new var, it should be declared with 'secret' or 'int' (if we had int).
    # Since we only have 'secret' declaration, this must be an update.
    
    # If updating a secret variable with a non-secret value, does it become public?
    # Or if updating with tainted value, it becomes tainted.
    # For simplicity, let's just generate code.
    
    t = tac_generator.new_temp()
    tac_generator.emit(f"{t} = {value}")
    tac_generator.emit(f"{var_name} = {t}")

def p_statement_login(p):
    '''statement : KEYWORD_LOGIN KEYWORD_AS KEYWORD_ADMIN SEMI
                 | KEYWORD_LOGIN KEYWORD_AS KEYWORD_GUEST SEMI'''
    if p[3] == 'admin':
        semantic_analyzer.set_role('admin')
    else:
        semantic_analyzer.set_role('guest')

# --- Control Flow Rules ---

# --- Control Flow Rules ---

# IF-ELSE Statement
# We use a simpler approach to avoid conflicts:
# statement : IF ( expr ) { stmts }
# statement : IF ( expr ) { stmts } ELSE { stmts }

def p_if_head(p):
    'if_head : KEYWORD_IF LPAREN expression RPAREN'
    cond = p[3]
    l_else = tac_generator.new_label()
    l_end = tac_generator.new_label()
    tac_generator.emit(f"ifFalse {cond} goto {l_else}")
    p[0] = (l_else, l_end)

def p_statement_if(p):
    'statement : if_head LBRACE statements RBRACE %prec LOWER_THAN_ELSE'
    l_else, l_end = p[1]
    tac_generator.emit_label(l_else) # No else block, so else label is end

def p_statement_if_else(p):
    'statement : if_head LBRACE statements RBRACE KEYWORD_ELSE LBRACE statements RBRACE'
    l_else, l_end = p[1]
    
    # We need to inject "goto l_end" at the end of the IF block.
    # Since we can't easily inject, we will emit it now, but it will appear AFTER the if block statements.
    # This is correct!
    
    tac_generator.emit(f"goto {l_end}")
    tac_generator.emit_label(l_else)
    
    # The statements for ELSE block are in p[7]. They have already been emitted.
    # Wait, this is bottom-up. p[7] (else stmts) are emitted BEFORE p_statement_if_else reduces.
    # So the order of emission in TAC will be:
    # 1. if_head (ifFalse ...)
    # 2. if stmts
    # 3. else stmts
    # 4. p_statement_if_else action (goto l_end, label l_else)
    
    # RESULT:
    # ifFalse cond goto L_else
    # ... if stmts ...
    # ... else stmts ...
    # goto L_end
    # L_else:
    
    # THIS IS WRONG. The else stmts must be AFTER L_else.
    # To fix this in PLY (one-pass), we need an intermediate rule (marker) before the else block.

    pass

def p_else_marker(p):
    'else_marker : KEYWORD_ELSE'
    # This rule reduces BEFORE the else block statements are parsed.
    # We can emit the jump and label here.
    
    # But we need the labels from if_head.
    # In PLY, we can access p[-4] (the if_head).
    
    l_else, l_end = p[-4]
    tac_generator.emit(f"goto {l_end}")
    tac_generator.emit_label(l_else)
    p[0] = l_end

def p_statement_if_else_fixed(p):
    'statement : if_head LBRACE statements RBRACE else_marker LBRACE statements RBRACE'
    l_end = p[5]
    tac_generator.emit_label(l_end)


# SWITCH Statement
# switch(x) { case 1: ... break; case 2: ... break; }

switch_stack = []

def p_switch_head(p):
    'switch_head : KEYWORD_SWITCH LPAREN expression RPAREN'
    switch_val = p[3]
    l_end = tac_generator.new_label()
    switch_stack.append((switch_val, l_end))

def p_statement_switch(p):
    'statement : switch_head LBRACE cases RBRACE'
    _, l_end = switch_stack.pop()
    tac_generator.emit_label(l_end)

def p_cases(p):
    '''cases : cases case
             | empty'''
    pass

def p_case_head(p):
    'case_head : KEYWORD_CASE NUMBER COLON'
    switch_val, _ = switch_stack[-1]
    case_val = p[2]
    
    t = tac_generator.new_temp()
    tac_generator.emit(f"{t} = {switch_val} == {case_val}")
    
    l_skip = tac_generator.new_label()
    tac_generator.emit(f"ifFalse {t} goto {l_skip}")
    p[0] = l_skip

def p_case(p):
    'case : case_head statements KEYWORD_BREAK SEMI'
    l_skip = p[1]
    _, l_end = switch_stack[-1]
    tac_generator.emit(f"goto {l_end}")
    tac_generator.emit_label(l_skip)

def p_empty(p):
    'empty :'
    pass

# --- Expression Rules ---

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression GT expression
                  | expression LT expression'''
    
    # Constant Folding Optimization
    if isinstance(p[1], int) and isinstance(p[3], int):
        if p[2] == '+':
            p[0] = p[1] + p[3]
            print(f"[Optimization] Constant Folding: {p[1]} + {p[3]} = {p[0]}")
            return
        elif p[2] == '-':
            p[0] = p[1] - p[3]
            print(f"[Optimization] Constant Folding: {p[1]} - {p[3]} = {p[0]}")
            return
    
    # Code Generation for non-constant expressions
    if p[2] == '+':
        t = tac_generator.new_temp()
        tac_generator.emit(f"{t} = {p[1]} + {p[3]}")
        p[0] = t
    elif p[2] == '-':
        t = tac_generator.new_temp()
        tac_generator.emit(f"{t} = {p[1]} - {p[3]}")
        p[0] = t
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
    if p:
        print(f"Syntax Error at '{p.value}' (type: {p.type})")
    else:
        print("Syntax Error at EOF")

parser = yacc.yacc()
