#!/bin/bash

# Define colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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
    
    # Run the test
    if $PYTHON main.py "$test_file"; then
        echo -e "${GREEN}[PASS] $test_file executed successfully.${NC}"
    else
        echo -e "${RED}[FAIL] $test_file failed to execute.${NC}"
        # We don't exit here because we want to run all tests
        # Some tests are EXPECTED to fail (security checks), so we might want to handle that.
        # However, for now, a non-zero exit code from main.py means "something went wrong" or "security violation".
        # If the test is INTENDED to fail (like test_security_fail.sfs), the user might see [FAIL].
        # Let's clarify this in the output or just report the status.
    fi
    echo "---------------------------------------------------"
done

echo -e "\n${BLUE}Test Suite Completed.${NC}"
