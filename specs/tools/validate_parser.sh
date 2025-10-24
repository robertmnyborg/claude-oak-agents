#!/bin/bash
# Validation script for Markdown Parser (Task 1)

set -e

TOOLS_DIR="/Users/robertnyborg/Projects/claude-oak-agents/specs/tools"
cd "$TOOLS_DIR"

echo "========================================="
echo "Markdown Parser Validation"
echo "========================================="
echo ""

# 1. Check files exist
echo "1. Checking deliverable files..."
files=(
    "markdown_parser.py"
    "test_markdown_parser.py"
    "README.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file exists"
    else
        echo "   ✗ $file missing!"
        exit 1
    fi
done
echo ""

# 2. Run unit tests
echo "2. Running unit tests..."
if python3 -m unittest test_markdown_parser.py -v 2>&1 | grep -q "OK"; then
    echo "   ✓ All unit tests pass"
else
    echo "   ✗ Unit tests failed!"
    exit 1
fi
echo ""

# 3. Test with real spec file
echo "3. Testing with real spec file..."
python3 << 'PYEOF'
from markdown_parser import parse_spec

spec_path = "/Users/robertnyborg/Projects/claude-oak-agents/specs/active/2025-10-23-spec-to-yaml-translator.md"
result = parse_spec(spec_path)

# Validate structure
assert "metadata" in result
assert "goals" in result
assert "design" in result
assert "implementation" in result
assert "test_strategy" in result

# Validate metadata
assert result["metadata"]["spec_id"] == "spec-20251023-spec-to-yaml-translator"
assert result["metadata"]["status"] == "in-progress"

# Validate goals
assert len(result["goals"]["user_stories"]) >= 3
assert len(result["goals"]["acceptance_criteria"]) >= 6

# Validate design
assert len(result["design"]["components"]) >= 3

# Validate implementation
assert len(result["implementation"]["tasks"]) >= 5

# Validate test strategy
assert len(result["test_strategy"]["test_cases"]) >= 8

# Validate linkages (AC-3)
task1_links = result["implementation"]["tasks"][0]["links_to"]
assert len(task1_links) > 0
assert "AC-1" in task1_links or "AC-1" in str(task1_links)

print("   ✓ Real spec file parsed successfully")
print(f"   ✓ Found {len(result['goals']['user_stories'])} user stories")
print(f"   ✓ Found {len(result['goals']['acceptance_criteria'])} acceptance criteria")
print(f"   ✓ Found {len(result['design']['components'])} components")
print(f"   ✓ Found {len(result['implementation']['tasks'])} tasks")
print(f"   ✓ Found {len(result['test_strategy']['test_cases'])} test cases")
print(f"   ✓ Task 1 has {len(task1_links)} linkages")
PYEOF

echo ""

# 4. Test error handling
echo "4. Testing error handling..."
python3 << 'PYEOF'
from markdown_parser import parse_spec, ParseError

# Test missing file
try:
    parse_spec("/nonexistent/file.md")
    print("   ✗ Should have raised FileNotFoundError")
    exit(1)
except FileNotFoundError:
    print("   ✓ FileNotFoundError raised correctly")

# Test malformed spec (missing spec ID)
import tempfile
import os

# Create temp file with missing spec ID
temp_dir = tempfile.mkdtemp()
temp_file = os.path.join(temp_dir, "bad_spec.md")
with open(temp_file, 'w') as f:
    f.write("""# Spec: Bad Spec
**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
""")

try:
    parse_spec(temp_file)
    print("   ✗ Should have raised ParseError")
    exit(1)
except ParseError as e:
    if "Spec ID" in str(e):
        print("   ✓ ParseError raised correctly for missing Spec ID")
    else:
        print(f"   ✗ Wrong error message: {e}")
        exit(1)

# Cleanup
os.remove(temp_file)
os.rmdir(temp_dir)
PYEOF

echo ""

# 5. Final summary
echo "========================================="
echo "Validation Complete"
echo "========================================="
echo ""
echo "Task 1 (Markdown Parser) - ALL CHECKS PASSED ✓"
echo ""
echo "Deliverables:"
echo "  - markdown_parser.py (implementation)"
echo "  - test_markdown_parser.py (unit tests)"
echo "  - README.md (documentation)"
echo ""
echo "Acceptance Criteria:"
echo "  ✓ AC-1: Parser extracts all spec sections"
echo "  ✓ AC-3: Linkages preserved between sections"
echo ""
echo "Test Cases:"
echo "  ✓ TC-1: Parse complete spec"
echo "  ✓ TC-2: Preserve linkages"
echo "  ✓ TC-3: Handle malformed Markdown"
echo ""
echo "Ready for integration with Task 2 (YAML Generator)"
echo ""
