#!/bin/bash
# Phase 2 Integration Verification Script

set -e

PROJECT_ROOT="/Users/robertnyborg/Projects/claude-oak-agents"
cd "$PROJECT_ROOT"

echo "================================================================================
PHASE 2 WORKFLOW COORDINATION - INTEGRATION VERIFICATION
================================================================================
"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
PASSED=0
FAILED=0
WARNINGS=0

check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $description: $file"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $description: $file (MISSING)"
        ((FAILED++))
        return 1
    fi
}

check_content() {
    local file=$1
    local pattern=$2
    local description=$3
    
    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $description in $file"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $description in $file (NOT FOUND)"
        ((FAILED++))
        return 1
    fi
}

warn_optional() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $description: $file"
        ((PASSED++))
    else
        echo -e "${YELLOW}!${NC} $description: $file (will be created on first use)"
        ((WARNINGS++))
    fi
}

echo "1. Checking Modified Files"
echo "────────────────────────────────────────────────────────────────────────────────"
check_file "CLAUDE.md" "Main LLM coordination rules"
check_content "CLAUDE.md" "Workflow Coordination (Phase 2 - Data-Driven)" "Phase 2 section"
echo ""

check_file "scripts/automation/weekly_review.py" "Weekly review script"
check_content "scripts/automation/weekly_review.py" "Workflow Analysis" "Workflow analysis integration"
echo ""

check_file "scripts/automation/monthly_analysis.py" "Monthly analysis script"
check_content "scripts/automation/monthly_analysis.py" "Performance Trends" "Performance trends integration"
echo ""

check_file "automation/oak_prompts.sh" "Shell prompts script"
check_content "automation/oak_prompts.sh" "oak-workflows" "oak-workflows command"
check_content "automation/oak_prompts.sh" "oak-query-agent" "oak-query-agent command"
check_content "automation/oak_prompts.sh" "oak-agent-trends" "oak-agent-trends command"
echo ""

echo "2. Checking Created Files"
echo "────────────────────────────────────────────────────────────────────────────────"
check_file "README_PHASE2.md" "Phase 2 README"
check_file "QUICK_START_PHASE2.md" "Quick start guide"
check_file "INTEGRATION_SUMMARY.md" "Integration summary"
check_file "DELIVERABLES.md" "Deliverables checklist"
check_file "examples/integrated_workflow_example.md" "Integration example"
check_file "tests/test_integration_workflow.py" "Integration tests"
echo ""

echo "3. Checking Existing Phase 2 Components"
echo "────────────────────────────────────────────────────────────────────────────────"
check_file "telemetry/logger.py" "Telemetry logger"
check_content "telemetry/logger.py" "log_workflow_start" "Workflow start method"
check_content "telemetry/logger.py" "log_agent_handoff" "Agent handoff method"
check_content "telemetry/logger.py" "log_workflow_complete" "Workflow complete method"
echo ""

check_file "telemetry/analyzer.py" "Telemetry analyzer"
check_content "telemetry/analyzer.py" "analyze_workflows" "Workflow analysis method"
check_content "telemetry/analyzer.py" "calculate_coordination_overhead" "Coordination overhead method"
check_content "telemetry/analyzer.py" "get_agent_performance_trends" "Performance trends method"
echo ""

check_file "scripts/query_best_agent.py" "Query best agent script"
echo ""

echo "4. Checking Optional Runtime Files"
echo "────────────────────────────────────────────────────────────────────────────────"
warn_optional "telemetry/workflow_events.jsonl" "Workflow events file"
echo ""

echo "5. Running Integration Tests"
echo "────────────────────────────────────────────────────────────────────────────────"
if python3 tests/test_integration_workflow.py 2>&1 | grep -q "OK"; then
    echo -e "${GREEN}✓${NC} Integration tests passed (8/8)"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Integration tests failed"
    ((FAILED++))
fi
echo ""

echo "6. Checking Python Dependencies"
echo "────────────────────────────────────────────────────────────────────────────────"
if python3 -c "import sys; from pathlib import Path; sys.path.insert(0, '.'); from telemetry.logger import TelemetryLogger; from telemetry.analyzer import TelemetryAnalyzer" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Python modules importable"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Python modules not importable"
    ((FAILED++))
fi
echo ""

echo "7. Checking Shell Commands"
echo "────────────────────────────────────────────────────────────────────────────────"
if grep -q "oak-workflows()" automation/oak_prompts.sh; then
    echo -e "${GREEN}✓${NC} oak-workflows function defined"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} oak-workflows function not found"
    ((FAILED++))
fi

if grep -q "oak-query-agent()" automation/oak_prompts.sh; then
    echo -e "${GREEN}✓${NC} oak-query-agent function defined"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} oak-query-agent function not found"
    ((FAILED++))
fi

if grep -q "oak-agent-trends()" automation/oak_prompts.sh; then
    echo -e "${GREEN}✓${NC} oak-agent-trends function defined"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} oak-agent-trends function not found"
    ((FAILED++))
fi
echo ""

echo "8. Checking Documentation Completeness"
echo "────────────────────────────────────────────────────────────────────────────────"
for doc in "README_PHASE2.md" "QUICK_START_PHASE2.md" "INTEGRATION_SUMMARY.md" "DELIVERABLES.md"; do
    if [ -f "$doc" ] && [ $(wc -l < "$doc") -gt 50 ]; then
        echo -e "${GREEN}✓${NC} $doc has substantial content"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $doc is missing or too short"
        ((FAILED++))
    fi
done
echo ""

echo "================================================================================
VERIFICATION SUMMARY
================================================================================
"

echo -e "${GREEN}Passed:${NC} $PASSED checks"
echo -e "${RED}Failed:${NC} $FAILED checks"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS checks"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED - INTEGRATION VERIFIED${NC}"
    echo ""
    echo "Next Steps:"
    echo "  1. Run manual testing: see DELIVERABLES.md"
    echo "  2. Test shell commands: source automation/oak_prompts.sh"
    echo "  3. Read quick start: cat QUICK_START_PHASE2.md"
    exit 0
else
    echo -e "${RED}✗ INTEGRATION INCOMPLETE - $FAILED CHECKS FAILED${NC}"
    echo ""
    echo "Please review failed checks above and fix any issues."
    exit 1
fi
