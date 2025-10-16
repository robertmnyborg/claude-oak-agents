#!/bin/bash
# Telemetry Analyzer Script
#
# Convenient wrapper for analyzing telemetry data

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}          CLAUDE OAK AGENTS - TELEMETRY ANALYZER${NC}"
echo -e "${BLUE}================================================================${NC}"

# Check if telemetry data exists
TELEMETRY_DIR="${PROJECT_ROOT}/telemetry"

if [ ! -f "${TELEMETRY_DIR}/agent_invocations.jsonl" ]; then
    echo -e "\n${YELLOW}⚠️  No telemetry data found.${NC}"
    echo -e "   Expected file: ${TELEMETRY_DIR}/agent_invocations.jsonl"
    echo -e "\n💡 Generate test data first:"
    echo -e "   python3 scripts/test_telemetry_e2e.py"
    exit 1
fi

# Count invocations
INVOCATION_COUNT=$(wc -l < "${TELEMETRY_DIR}/agent_invocations.jsonl" | tr -d ' ')

echo -e "\n${GREEN}✓${NC} Found telemetry data: ${INVOCATION_COUNT} invocations"

# Run analyzer
echo -e "\n${BLUE}Running analyzer...${NC}\n"

cd "$PROJECT_ROOT"
python3 -m telemetry.analyzer

# Check if stats were generated
if [ -f "${TELEMETRY_DIR}/performance_stats.json" ]; then
    echo -e "\n${GREEN}✓${NC} Statistics generated successfully"

    # Show quick summary with jq if available
    if command -v jq &> /dev/null; then
        echo -e "\n${BLUE}Quick Summary:${NC}"
        jq -r '.agents | to_entries | map("\(.key): \(.value.invocation_count) uses, \(.value.success_rate*100|floor)% success") | .[]' \
            "${TELEMETRY_DIR}/performance_stats.json"
    else
        echo -e "\n${YELLOW}💡 Install jq for pretty JSON viewing:${NC}"
        echo -e "   brew install jq  # macOS"
        echo -e "   apt install jq   # Ubuntu/Debian"
    fi

    echo -e "\n${BLUE}View full statistics:${NC}"
    echo -e "   cat ${TELEMETRY_DIR}/performance_stats.json | jq"
else
    echo -e "\n${YELLOW}⚠️  Stats file not generated${NC}"
    exit 1
fi

echo -e "\n${BLUE}================================================================${NC}"
echo -e "${GREEN}✓ Analysis complete!${NC}"
echo -e "${BLUE}================================================================${NC}"
