#!/usr/bin/env bash
#
# Quick Resolution Script for False Positive Quality Issues
# 
# Run this to clear the 8 false positive issues from test data
#

set -e

cd "$(dirname "$0")"

echo "=========================================="
echo "False Positive Quality Issue Resolution"
echo "=========================================="
echo ""
echo "This script will resolve 8 false positive issues"
echo "caused by test workflow data contamination."
echo ""
echo "Issue IDs to resolve:"
echo "  - 8bd533b9-1dd0-4bdb-9eb5-f1220aae7403 (design-simplicity-advisor)"
echo "  - 18e81b37-ffff-4a4b-883a-3f4328c7f8dd (backend-architect)"
echo "  - bb17fd97-bc4d-45b8-b83c-9adf9790b631 (unit-test-expert)"
echo "  - 81a35afc-ed0d-4213-840c-d112d9817f6e (general-purpose)"
echo "  - cdab4eb1-8451-47d1-a7d0-17e88b45e190 (design-simplicity-advisor)"
echo "  - e269b129-283a-469c-be61-bcfe6048b088 (backend-architect)"
echo "  - 42679b12-18f6-4aa4-bc79-54cea3e644f8 (unit-test-expert)"
echo "  - e4763503-410c-45ac-bfc8-f69a752fb7fd (general-purpose)"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "Resolving issues..."
echo ""

python3 << 'PYTHON_EOF'
import sys
from pathlib import Path

# Add telemetry to path
sys.path.insert(0, str(Path(__file__).parent))

from telemetry.issue_tracker import IssueTracker

tracker = IssueTracker()

# False positive issues from test data
false_positive_issues = [
    '8bd533b9-1dd0-4bdb-9eb5-f1220aae7403',  # design-simplicity-advisor
    '18e81b37-ffff-4a4b-883a-3f4328c7f8dd',  # backend-architect
    'bb17fd97-bc4d-45b8-b83c-9adf9790b631',  # unit-test-expert
    '81a35afc-ed0d-4213-840c-d112d9817f6e',  # general-purpose
    'cdab4eb1-8451-47d1-a7d0-17e88b45e190',  # design-simplicity-advisor (duplicate)
    'e269b129-283a-469c-be61-bcfe6048b088',  # backend-architect (duplicate)
    '42679b12-18f6-4aa4-bc79-54cea3e644f8',  # unit-test-expert (duplicate)
    'e4763503-410c-45ac-bfc8-f69a752fb7fd',  # general-purpose (duplicate)
]

resolution_notes = (
    "False positive: Test workflow data contamination. "
    "These invocations were part of intentional test/validation workflows "
    "with different workflow_ids and explicit test markers. "
    "See TELEMETRY_QUALITY_ANALYSIS.md for detailed analysis."
)

resolved_count = 0
for issue_id in false_positive_issues:
    try:
        issue = tracker.get_issue(issue_id)
        if not issue:
            print(f"⚠️  Issue {issue_id} not found, skipping")
            continue
        
        if issue['state'] == 'resolved':
            print(f"ℹ️  Issue {issue_id} ({issue['agent_name']}) already resolved")
            continue

        tracker.update_state(
            issue_id,
            'resolved',
            notes=resolution_notes,
            resolution_category='false_positive_test_data',
            false_positive=True
        )
        print(f"✓ Resolved: {issue_id} ({issue['agent_name']})")
        resolved_count += 1
    except Exception as e:
        print(f"✗ Error resolving {issue_id}: {e}")

print(f"\n✓ Resolved {resolved_count} false positive issues")
print("\nUpdated statistics:")
stats = tracker.get_statistics()
print(f"  Total issues: {stats['total_issues']}")
print(f"  Open: {stats['by_state']['open']}")
print(f"  Resolved: {stats['by_state']['resolved']}")
PYTHON_EOF

echo ""
echo "=========================================="
echo "Resolution Complete"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Review TELEMETRY_QUALITY_ANALYSIS.md for detailed findings"
echo "  2. Implement test data filtering (see P1 recommendations)"
echo "  3. Update detection script with deduplication logic"
echo ""

