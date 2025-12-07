import sys
from lexer import lexer
from parser import parser, tac_generator

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.sfs>")
        return

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
        print(f"Compiling {filename}...\n")
        
        # Lexer Test (Optional, for debug)
        # lexer.input(code)
        # for token in lexer:
        #     print(token)
        
        # Parse
        # We need to parse line by line or the whole content?
        # The grammar rules are for single statements.
        # Let's split by lines for this simple version or update grammar to handle multiple statements.
        # Updating grammar to handle list of statements is better, but for simplicity let's loop lines.
        
        # Parse the whole program at once
        parser.parse(code)
        
        # Output TAC
        tac_generator.print_tac()
        
        print("Compilation Successful!")
        
    except Exception as e:
        print(f"\nCompilation Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
