#!/bin/bash

# Define colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${RED}[ERROR] Virtual environment not found! Please run ./setup.sh first.${NC}"
    exit 1
fi

PYTHON="./venv/bin/python3"
TEST_DIR="testcases"

echo -e "${BLUE}Starting Test Suite...${NC}\n"

# Iterate over all .sfs files in testcases directory
for test_file in "$TEST_DIR"/*.sfs; do
    [ -e "$test_file" ] || continue
    
    echo -e "${BLUE}Running test: $test_file${NC}"
    
    # Capture output and exit code
    OUTPUT=$($PYTHON main.py "$test_file" 2>&1)
    EXIT_CODE=$?
    
    # Check if this test is EXPECTED to fail (Security/RBAC tests)
    if [[ "$test_file" == *"fail"* ]] || [[ "$test_file" == *"rbac"* ]]; then
        IS_EXPECTED_FAIL=true
    else
        IS_EXPECTED_FAIL=false
    fi

    # Display Output (Optional: truncate if too long, but for now show all)
    echo "$OUTPUT"

    if [ $EXIT_CODE -eq 0 ]; then
        # Execution Succeeded
        if [ "$IS_EXPECTED_FAIL" = true ]; then
             echo -e "${RED}[FAIL] $test_file succeeded but was expected to fail! (Security Breach?)${NC}"
        else
             echo -e "${GREEN}[PASS] $test_file executed successfully.${NC}"
        fi
    else
        # Execution Failed (Non-zero exit code)
        if [ "$IS_EXPECTED_FAIL" = true ]; then
             echo -e "${GREEN}[PASS] $test_file failed as expected (Security Blocked).${NC}"
        else
             echo -e "${RED}[FAIL] $test_file failed unexpectedly.${NC}"
        fi
    fi
    echo "---------------------------------------------------"
done

echo -e "\n${BLUE}Test Suite Completed.${NC}"
