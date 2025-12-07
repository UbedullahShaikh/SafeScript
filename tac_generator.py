temp_count = 1
instructions = []

def new_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t

def emit(code):
    instructions.append(code)
    print(f"[TAC] Generated: {code}")

def print_tac():
    print("\n--- FINAL CODE (TAC) ---")
    for line in instructions:
        print(line)
    print("------------------------\n")
