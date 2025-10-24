#!/bin/bash
# Demo script for translate_spec.py CLI tool
# Shows all three operation modes with examples

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================"
echo "CLI Tool Demo: translate_spec.py"
echo "========================================================"
echo ""

# Demo 1: Translation Mode
echo "DEMO 1: Translation Mode"
echo "------------------------"
echo ""
echo "Command:"
echo "  ./translate_spec.py \\"
echo "    --input ../active/2025-10-23-spec-to-yaml-translator.md \\"
echo "    --output ../active/2025-10-23-spec-to-yaml-translator.yaml \\"
echo "    --validate"
echo ""
echo "Output:"

./translate_spec.py \
  --input ../active/2025-10-23-spec-to-yaml-translator.md \
  --output ../active/2025-10-23-spec-to-yaml-translator.yaml \
  --validate 2>&1

echo ""
echo ""

# Demo 2: Validation Mode
echo "DEMO 2: Validation Mode"
echo "-----------------------"
echo ""
echo "Command:"
echo "  ./translate_spec.py --validate-yaml ../active/2025-10-23-spec-to-yaml-translator.yaml"
echo ""
echo "Output:"

./translate_spec.py --validate-yaml ../active/2025-10-23-spec-to-yaml-translator.yaml 2>&1

echo ""
echo ""

# Demo 3: Help
echo "DEMO 3: Help Display"
echo "--------------------"
echo ""
echo "Command:"
echo "  ./translate_spec.py --help"
echo ""
echo "Output:"

./translate_spec.py --help | head -20

echo ""
echo "  ... (truncated)"
echo ""
echo ""

# Demo 4: Error Handling
echo "DEMO 4: Error Handling"
echo "----------------------"
echo ""
echo "Command:"
echo "  ./translate_spec.py --input nonexistent.md --output test.yaml"
echo ""
echo "Output:"

./translate_spec.py --input nonexistent.md --output test.yaml 2>&1 || true

echo ""
echo ""

# Summary
echo "========================================================"
echo "✅ CLI Demo Complete"
echo "========================================================"
echo ""
echo "Available modes:"
echo "  1. Translation: --input X --output Y [--validate]"
echo "  2. Validation:  --validate-yaml Y"
echo "  3. Watch:       --watch X (NOT IMPLEMENTED)"
echo ""
echo "Documentation:"
echo "  - README_CLI.md - Full documentation"
echo "  - CLI_QUICK_REFERENCE.md - Quick reference"
echo "  - CLI_SUMMARY.md - Implementation summary"
echo ""
echo "Testing:"
echo "  - python3 test_cli.py -v - Run unit tests"
echo "  - ./validate_cli.sh - Run validation"
echo ""
