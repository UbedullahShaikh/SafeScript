import symbol_table
import sys

current_role = 'guest' # Default role

def set_role(role):
    global current_role
    current_role = role
    print(f"ℹ️  User switched to: {role.upper()}")

def check_security(var_name):
    data = symbol_table.get_symbol(var_name)
    
    if not data:
        raise Exception(f"Error: Variable '{var_name}' not found!")

    is_secret = data['tainted']

    # --- RBAC CHECK ---
    if current_role == 'guest' and is_secret:
        print(f"\n🚫 ACCESS DENIED: 'Guest' user cannot access Secret '{var_name}'!")
        print("   >>> Security Violation. Project Halted.\n")
        sys.exit(1)

    if is_secret:
        raise Exception(f"SECURITY ALERT! '{var_name}' is Secret. Encrypt it before sending!")
    
    print(f"[Semantic] Security Check Passed: '{var_name}' is safe.")

def mark_safe(var_name):
    symbol_table.update_symbol(var_name, tainted=False)
    print(f"[Semantic] '{var_name}' is now Safe (Encrypted).")
