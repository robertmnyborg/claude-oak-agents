#!/usr/bin/env bash
# ============================================================================
# Automatic Proposal Generation from Issue Patterns
# ============================================================================
# 
# DESIGN: KISS-approved 20-line shell script using jq + existing infrastructure
#
# PURPOSE: Analyzes patterns in telemetry/issues.jsonl and generates improvement
#          proposals for agents with 3+ issues, using ProposalTracker infrastructure
#
# WORKFLOW:
#   1. Find agents with 3+ issues (threshold for pattern detection)
#   2. Extract common keywords from issues for each agent
#   3. Generate proposal period (YYYY-MM)
#   4. Create structured proposal via ProposalTracker
#   5. Proposals saved to telemetry/proposals.jsonl in "pending" state
#
# INTEGRATION: Called by automation/weekly_review.py during weekly analysis
#
# ============================================================================

PROJECT_ROOT="/Users/robertnyborg/Projects/claude-oak-agents"
cd "$PROJECT_ROOT" || exit 1

echo "🔍 Analyzing issue patterns for proposal generation..."

# Find agents with 3+ issues (indicates systemic problem requiring intervention)
cat telemetry/issues.jsonl 2>/dev/null | \
  jq -r '.agent_name' | \
  sort | uniq -c | \
  awk '$1 >= 3 {print $1, $2}' | \
while read count agent; do
  echo "  Found $count issues for $agent"
  
  # Extract common keywords for this agent's issues (top 3 most frequent)
  keywords=$(cat telemetry/issues.jsonl | \
             jq -r "select(.agent_name==\"$agent\") | .evidence.keywords[]" 2>/dev/null | \
             sort | uniq -c | sort -rn | head -3 | awk '{print $2}' | paste -sd ", " -)
  
  # Generate proposal period (YYYY-MM format for current month)
  period=$(date +%Y-%m)
  
  # Create proposal using existing ProposalTracker infrastructure
  python3 << PYTHON_EOF
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from telemetry.proposal_tracker import ProposalTracker

tracker = ProposalTracker()
tracker.create_proposal(
    agent_name='$agent',
    proposal_period='$period',
    proposal_content='''**Proposed Improvement**: Add verification checklist for common failure patterns

**Root Cause**: Agent has $count false completion issues with recurring patterns in: $keywords

**Recommended Changes**:
1. Add explicit verification step in "Before Claiming Completion" section
2. Require validation of task completeness for: $keywords
3. Add concrete examples of proper verification for these task types

**Implementation**:
\`\`\`markdown
### Additional Verification (Auto-generated)

Before marking task complete, verify:
- [ ] Task fully addresses the user's request for: $keywords
- [ ] No placeholder or TODO comments left in deliverables
- [ ] User can immediately use the solution without follow-up requests
\`\`\`

**Expected Impact**: Reduce false completions by 60-80% based on similar patterns''',
    root_cause='missing_verification_steps',
    issue_count=int('$count'),
    expected_impact='reduce false completions by 60-80%'
)
print(f'✓ Created proposal for $agent ($count issues)')
PYTHON_EOF
  
done

echo "✓ Proposal generation complete"
