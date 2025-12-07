# SafeScript Compiler (.sfs)

A secure, optimizing compiler for the **SafeScript** language. This compiler is designed to enforce security rules (Taint Analysis) and optimize code (Constant Folding) while generating Three Address Code (TAC).

## 🚀 Key Features

1.  **Security First (Taint Analysis)** 🛡️
    - Automatically detects "Secret" variables.
    - **Blocks** any attempt to send secret data to the network without encryption.
    - *Example:* `send(secret_var);` -> **ERROR!**

2.  **Smart Optimization (Constant Folding)** ⚡
    - Calculates mathematical expressions at compile time to save CPU cycles.
    - *Example:* `x = 10 + 20;` becomes `x = 30` in the final code.

3.  **Decision Making (Control Flow)** 🔀
    - Supports `if` statements and comparisons (`>`, `<`).
    - Generates logical TAC with `goto` and `Labels`.

4.  **Enterprise Security (RBAC)** 🔐
    - **Role-Based Access Control**: Distinguishes between `Admin` and `Guest`.
    - **Strict Policy**: Guests are completely blocked from touching Secret data.

5.  **Professional C-Style Syntax** 💻
    - Uses familiar syntax like `x = 10;`, `send(x);`, and `encrypt(x);`.

6.  **Modular Architecture** 🏗️
    - Split into 5 distinct components for easy understanding:
        - `lexer.py`: Tokenizer
        - `parser.py`: Grammar & Logic
        - `symbol_table.py`: Variable Database
        - `semantic_analyzer.py`: Security Guard
        - `tac_generator.py`: Code Generator

## 🛠️ Installation

1.  **Clone the repository** (if you haven't already).
2.  **Run the setup script**:
    This script will create a virtual environment and install all dependencies.
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```
3.  **Activate the environment**:
    ```bash
    source venv/bin/activate
    ```

## 🧪 Testing

The project includes a suite of test cases to verify security, optimization, and control flow.

### Running Tests
To run all test cases automatically:
```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Test Cases Description
- **`test_security_fail.sfs`**: Attempts to send a secret variable without encryption. **Expected Result: FAIL (Security Violation)**.
- **`test_optimization.sfs`**: Demonstrates constant folding (e.g., `10 + 20` -> `30`). **Expected Result: PASS**.
- **`test_control_flow.sfs`**: Tests `if-else` and `switch-case` logic. **Expected Result: PASS**.
- **`test_rbac.sfs`**: Tests Guest vs Admin access control. **Expected Result: FAIL (Access Denied)**.

## 🏃‍♂️ How to Run
 
You can run the compiler on the master demo file which showcases all features.
 
```bash
python main.py demo_master.sfs
```
 
**What's inside `demo_master.sfs`?**
1.  **Guest Access Check**: Shows how guests are blocked (commented out to prevent crash).
2.  **Admin Access**: Shows successful encryption and sending.
3.  **Optimization**: Demonstrates `50 + 50` becoming `100`.
4.  **Control Flow**: Uses `if-else` and `switch-case` logic.

## 📂 Project Structure

- **`main.py`**: The entry point of the compiler.
- **`lexer.py`**: Breaks code into tokens (words).
- **`parser.py`**: Understands the grammar and runs logic.
- **`symbol_table.py`**: Stores variable details (Type, Tainted Status).
- **`semantic_analyzer.py`**: Checks security rules.
- **`tac_generator.py`**: Generates the final machine-readable code.
