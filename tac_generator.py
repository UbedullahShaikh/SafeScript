temp_count = 1
label_count = 1
instructions = []

def new_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t

def new_label():
    global label_count
    l = f"L{label_count}"
    label_count += 1
    return l

def emit(code):
    instructions.append(code)
    print(f"[TAC] Generated: {code}")

def emit_label(label):
    instructions.append(f"{label}:")
    print(f"[TAC] Generated Label: {label}")

def print_tac():
    print("\n--- FINAL CODE (TAC) ---")
    for line in instructions:
        print(line)
    print("------------------------\n")
