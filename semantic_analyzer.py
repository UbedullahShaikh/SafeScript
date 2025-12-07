import symbol_table

def check_security(var_name):
    data = symbol_table.get_symbol(var_name)
    
    if not data:
        raise Exception(f"Error: Variable '{var_name}' not found!")

    if data['tainted'] == True:
        raise Exception(f"SECURITY ALERT! '{var_name}' is Secret. Encrypt it before sending!")
    
    print(f"[Semantic] Security Check Passed: '{var_name}' is safe.")

def mark_safe(var_name):
    symbol_table.update_symbol(var_name, tainted=False)
    print(f"[Semantic] '{var_name}' is now Safe (Encrypted).")
