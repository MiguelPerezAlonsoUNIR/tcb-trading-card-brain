#!/bin/bash
# Test runner script for TCB Trading Card Brain
# Runs all tests organized by type

# Don't exit on error - we want to run all tests
set +e

echo "======================================================================"
echo "TCB Trading Card Brain - Test Suite Runner"
echo "======================================================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Function to run a test and track results
run_test() {
    local test_file=$1
    local test_name=$(basename "$test_file")
    
    echo -e "${BLUE}Running: $test_name${NC}"
    if python "$test_file" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((FAILED++))
    fi
    echo ""
}

# Run unit tests
echo "======================================================================"
echo "UNIT TESTS (No dependencies required)"
echo "======================================================================"
echo ""

for test in tests/unit/test_*.py; do
    run_test "$test"
done

# Check if Flask is installed for system tests
if python -c "import flask" 2>/dev/null; then
    echo "======================================================================"
    echo "SYSTEM TESTS (Requires Flask and dependencies)"
    echo "======================================================================"
    echo ""
    
    for test in tests/system/test_*.py; do
        run_test "$test"
    done
else
    echo "======================================================================"
    echo "SYSTEM TESTS SKIPPED"
    echo "======================================================================"
    echo "Flask not installed. Install dependencies to run system tests:"
    echo "  pip install -r requirements.txt"
    echo ""
fi

# Summary
echo "======================================================================"
echo "TEST SUMMARY"
echo "======================================================================"
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
fi
