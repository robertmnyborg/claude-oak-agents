#!/bin/bash
# Run all Phase 2 CRL tests

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "============================================"
echo "CRL Phase 2 - Test Suite"
echo "============================================"
echo ""

# Run Q-learning tests
echo "Running Q-Learning Tests..."
echo "--------------------------------------------"
python3 tests/crl/test_q_learning.py
echo ""

# Run reward calculator tests
echo "Running Reward Calculator Tests..."
echo "--------------------------------------------"
python3 tests/crl/test_reward_calculator.py
echo ""

# Run Phase 1 tests (regression)
echo "Running Phase 1 Regression Tests..."
echo "--------------------------------------------"
python3 tests/crl/test_agent_basis.py
python3 tests/crl/test_task_classifier.py
python3 tests/crl/test_telemetry_crl.py
echo ""

echo "============================================"
echo "All Tests Passed!"
echo "============================================"
echo ""
echo "Next Steps:"
echo "  1. Run examples: python3 examples/crl_phase2_integration.py"
echo "  2. View Q-values: python3 scripts/crl/view_q_values.py"
echo ""
