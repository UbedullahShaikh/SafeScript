# Global Dictionary to store variables
symbols = {}

def add_symbol(name, type, tainted=False):
    symbols[name] = {'type': type, 'tainted': tainted}
    print(f"[SymbolTable] Added: {name} ({type})")

def get_symbol(name):
    return symbols.get(name)

def update_symbol(name, tainted):
    if name in symbols:
        symbols[name]['tainted'] = tainted
        print(f"[SymbolTable] Updated: {name} -> Tainted: {tainted}")
