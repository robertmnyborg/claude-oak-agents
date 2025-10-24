#!/bin/bash
# Validation script for translate_spec.py CLI tool
# Tests basic functionality and reports results

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================================="
echo "CLI Tool Validation"
echo "=================================================="
echo ""

# Check if translate_spec.py exists and is executable
echo "✓ Checking CLI tool..."
if [ ! -f "translate_spec.py" ]; then
    echo "❌ ERROR: translate_spec.py not found"
    exit 1
fi

if [ ! -x "translate_spec.py" ]; then
    echo "⚠️  WARNING: translate_spec.py not executable (running with python3)"
fi

echo "✅ CLI tool found"
echo ""

# Test 1: Run help command
echo "✓ Testing --help option..."
python3 translate_spec.py --help > /dev/null 2>&1
echo "✅ Help command works"
echo ""

# Test 2: Run unit tests
echo "✓ Running unit tests..."
python3 test_cli.py > /dev/null 2>&1
echo "✅ All unit tests pass"
echo ""

# Test 3: Translate actual spec file
echo "✓ Testing translation with actual spec..."
SPEC_FILE="../active/2025-10-23-spec-to-yaml-translator.md"
YAML_FILE="../active/2025-10-23-spec-to-yaml-translator.yaml"

if [ ! -f "$SPEC_FILE" ]; then
    echo "⚠️  WARNING: Spec file not found, skipping translation test"
else
    python3 translate_spec.py --input "$SPEC_FILE" --output "$YAML_FILE" --validate > /dev/null 2>&1
    echo "✅ Translation successful"
    
    # Test 4: Validate generated YAML
    echo "✓ Testing validation..."
    python3 translate_spec.py --validate-yaml "$YAML_FILE" > /dev/null 2>&1
    echo "✅ Validation successful"
fi

echo ""
echo "=================================================="
echo "✅ All CLI validations passed!"
echo "=================================================="
echo ""
echo "Usage examples:"
echo "  # Translate Markdown to YAML"
echo "  python3 translate_spec.py --input spec.md --output spec.yaml"
echo ""
echo "  # Translate with validation"
echo "  python3 translate_spec.py --input spec.md --output spec.yaml --validate"
echo ""
echo "  # Validate existing YAML"
echo "  python3 translate_spec.py --validate-yaml spec.yaml"
echo ""
