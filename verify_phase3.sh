#!/bin/bash
# Verification script for CRL Phase 3 implementation

echo "=========================================="
echo "CRL Phase 3 Verification"
echo "=========================================="
echo ""

PROJECT_ROOT="/Users/robertnyborg/Projects/claude-oak-agents"
ERRORS=0

# Function to check file exists
check_file() {
    local file="$1"
    local description="$2"
    
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "✓ $description"
    else
        echo "✗ $description (MISSING: $file)"
        ERRORS=$((ERRORS + 1))
    fi
}

# Function to check directory exists
check_dir() {
    local dir="$1"
    local description="$2"
    
    if [ -d "$PROJECT_ROOT/$dir" ]; then
        echo "✓ $description"
    else
        echo "✗ $description (MISSING: $dir)"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "Checking Core Modules..."
echo "----------------------------------------"
check_file "core/safety_monitor.py" "Safety Monitor"
check_file "core/rollback_manager.py" "Rollback Manager"
check_file "core/variant_proposer.py" "Variant Proposer"
echo ""

echo "Checking Scripts..."
echo "----------------------------------------"
check_dir "scripts/crl" "CRL Scripts Directory"
check_file "scripts/crl/safety_dashboard.py" "Safety Dashboard"
echo ""

echo "Checking Tests..."
echo "----------------------------------------"
check_file "tests/crl/test_safety.py" "Phase 3 Safety Tests"
echo ""

echo "Checking Examples..."
echo "----------------------------------------"
check_file "examples/crl_phase3_safety.py" "Phase 3 Example"
echo ""

echo "Checking Documentation..."
echo "----------------------------------------"
check_file "docs/CRL_SAFETY_GUIDE.md" "CRL Safety Guide"
check_file "CRL_PHASE3_README.md" "Phase 3 README"
check_file "PHASE3_DELIVERABLES.md" "Phase 3 Deliverables"
echo ""

echo "Checking Telemetry Directories..."
echo "----------------------------------------"
check_dir "telemetry/crl" "CRL Telemetry Directory"
echo ""

echo "Running Tests..."
echo "----------------------------------------"
cd "$PROJECT_ROOT"
if python3 tests/crl/test_safety.py > /tmp/phase3_test_output.txt 2>&1; then
    echo "✓ All Phase 3 tests passing"
else
    echo "✗ Some tests failed"
    cat /tmp/phase3_test_output.txt
    ERRORS=$((ERRORS + 1))
fi
echo ""

echo "Checking File Permissions..."
echo "----------------------------------------"
if [ -x "$PROJECT_ROOT/scripts/crl/safety_dashboard.py" ]; then
    echo "✓ Safety dashboard is executable"
else
    echo "✗ Safety dashboard not executable"
    ERRORS=$((ERRORS + 1))
fi

if [ -x "$PROJECT_ROOT/examples/crl_phase3_safety.py" ]; then
    echo "✓ Phase 3 example is executable"
else
    echo "✗ Phase 3 example not executable"
    ERRORS=$((ERRORS + 1))
fi
echo ""

echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo "✓ Phase 3 Verification PASSED"
    echo "All components present and working"
else
    echo "✗ Phase 3 Verification FAILED"
    echo "$ERRORS error(s) found"
    exit 1
fi
echo "=========================================="
