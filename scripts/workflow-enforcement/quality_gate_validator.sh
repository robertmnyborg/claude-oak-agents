#!/bin/bash
# quality_gate_validator.sh - Unified quality gate validation
# Combines code review, tests, KISS compliance, and basic security checks

set -e

# Configuration
WORKFLOW_STATE=".workflow_state"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
VERBOSE=${VERBOSE:-false}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[QUALITY GATE]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Initialize quality gate results
QUALITY_RESULTS=""
QUALITY_PASSED=true

# Function to update workflow state
update_state() {
    local phase="$1"
    local status="$2"
    local hash="$(git diff --cached | sha256sum | cut -d' ' -f1)"

    cat > "$WORKFLOW_STATE" <<EOF
PHASE=$phase
STATUS=$status
QUALITY_GATE_PASSED=$QUALITY_PASSED
HASH=$hash
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
RESULTS="$QUALITY_RESULTS"
EOF
}

# 1. Code Review Standards Check
check_code_standards() {
    log "Checking code standards..."

    # Check for console.log statements
    if git diff --cached --name-only | xargs grep -l "console\.log" 2>/dev/null; then
        warning "Found console.log statements in staged files"
        QUALITY_RESULTS="${QUALITY_RESULTS}\n- Warning: console.log statements found"
    fi

    # Check for TODO comments
    if git diff --cached --name-only | xargs grep -l "TODO\|FIXME\|XXX" 2>/dev/null; then
        warning "Found TODO/FIXME comments in staged files"
        QUALITY_RESULTS="${QUALITY_RESULTS}\n- Warning: Unresolved TODO/FIXME comments"
    fi

    log "Code standards check complete"
}

# 2. Unit Test Validation
check_tests() {
    log "Running test validation..."

    # Check if test command exists
    if [ -f "package.json" ] && grep -q '"test"' package.json; then
        log "Running npm test..."
        if npm test --silent 2>/dev/null; then
            log "Tests passed"
            QUALITY_RESULTS="${QUALITY_RESULTS}\n- Tests: PASSED"
        else
            error "Tests failed"
            QUALITY_RESULTS="${QUALITY_RESULTS}\n- Tests: FAILED"
            QUALITY_PASSED=false
            return 1
        fi
    elif [ -f "Makefile" ] && grep -q '^test:' Makefile; then
        log "Running make test..."
        if make test 2>/dev/null; then
            log "Tests passed"
            QUALITY_RESULTS="${QUALITY_RESULTS}\n- Tests: PASSED"
        else
            error "Tests failed"
            QUALITY_RESULTS="${QUALITY_RESULTS}\n- Tests: FAILED"
            QUALITY_PASSED=false
            return 1
        fi
    else
        warning "No test command found"
        QUALITY_RESULTS="${QUALITY_RESULTS}\n- Tests: NOT FOUND"
    fi
}

# 3. KISS Compliance Check
check_kiss_compliance() {
    log "Checking KISS compliance..."

    # Check for overly complex files (>300 lines)
    for file in $(git diff --cached --name-only); do
        if [ -f "$file" ]; then
            lines=$(wc -l < "$file")
            if [ "$lines" -gt 300 ]; then
                warning "File $file has $lines lines (>300) - consider splitting"
                QUALITY_RESULTS="${QUALITY_RESULTS}\n- Warning: $file may be too complex"
            fi
        fi
    done

    # Check for deeply nested code (>4 levels)
    for file in $(git diff --cached --name-only | grep -E '\.(js|ts|py|go)$'); do
        if [ -f "$file" ]; then
            # Simple heuristic: count leading spaces/tabs
            max_indent=$(sed 's/[^ \t].*//' "$file" | awk '{print length}' | sort -rn | head -1)
            if [ "$max_indent" -gt 16 ]; then
                warning "File $file may have deep nesting (indent: $max_indent)"
                QUALITY_RESULTS="${QUALITY_RESULTS}\n- Warning: $file may have deep nesting"
            fi
        fi
    done

    log "KISS compliance check complete"
}

# 4. Basic Security Check
check_security() {
    log "Running security checks..."

    # Check for hardcoded credentials
    patterns=(
        "password.*=.*['\"]"
        "api[_-]?key.*=.*['\"]"
        "secret.*=.*['\"]"
        "token.*=.*['\"]"
        "AWS.*=.*['\"]"
    )

    for pattern in "${patterns[@]}"; do
        if git diff --cached --name-only | xargs grep -iE "$pattern" 2>/dev/null; then
            error "Potential hardcoded credentials found"
            QUALITY_RESULTS="${QUALITY_RESULTS}\n- SECURITY: Potential hardcoded credentials"
            QUALITY_PASSED=false
            return 1
        fi
    done

    log "Security checks complete"
    QUALITY_RESULTS="${QUALITY_RESULTS}\n- Security: PASSED"
}

# 5. Performance Check
check_performance() {
    log "Running performance checks..."

    # Check for common performance issues
    for file in $(git diff --cached --name-only | grep -E '\.(js|ts)$'); do
        if [ -f "$file" ]; then
            # Check for synchronous file operations in Node.js
            if grep -q "readFileSync\|writeFileSync" "$file"; then
                warning "Synchronous file operations found in $file"
                QUALITY_RESULTS="${QUALITY_RESULTS}\n- Warning: Sync operations in $file"
            fi
        fi
    done

    log "Performance checks complete"
}

# Main validation flow
main() {
    log "Starting quality gate validation..."

    # Initialize workflow state
    update_state "QUALITY_GATE" "IN_PROGRESS"

    # Run all checks
    check_code_standards
    check_tests || true  # Continue even if tests fail
    check_kiss_compliance
    check_security || true  # Continue even if security fails
    check_performance

    # Update final state
    if [ "$QUALITY_PASSED" = true ]; then
        update_state "QUALITY_GATE" "COMPLETED"
        log "✅ Quality gate PASSED"
        echo -e "\nQuality Gate Results:$QUALITY_RESULTS"
        exit 0
    else
        update_state "QUALITY_GATE" "FAILED"
        error "❌ Quality gate FAILED"
        echo -e "\nQuality Gate Results:$QUALITY_RESULTS"
        exit 1
    fi
}

# Run main function
main "$@"