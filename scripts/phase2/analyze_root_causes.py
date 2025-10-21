#!/usr/bin/env python3
"""
Root Cause Analysis

Analyzes resolved issues to identify patterns and generate improvement proposals.

Usage:
  python3 scripts/phase2/analyze_root_causes.py
  python3 scripts/phase2/analyze_root_causes.py --min-issues 3
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any, Set

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from telemetry.issue_tracker import IssueTracker


# Root cause categories
ROOT_CAUSES = {
    'missing_verification': {
        'name': 'Missing Verification',
        'description': 'Agent claimed completion without testing',
        'keywords': ['crash', 'error', 'broken', 'not working', 'still failing']
    },
    'unclear_instructions': {
        'name': 'Unclear Instructions',
        'description': 'Agent didn\'t understand what "done" means',
        'keywords': ['same height', 'consistent', 'uniform', 'aligned']
    },
    'wrong_approach': {
        'name': 'Wrong Approach',
        'description': 'Agent used wrong strategy for problem',
        'keywords': ['performance', 'slow', 'timeout', 'inefficient']
    },
    'missing_domain_knowledge': {
        'name': 'Missing Domain Knowledge',
        'description': 'Agent lacks specific framework/library knowledge',
        'keywords': ['api', 'integration', 'library', 'framework']
    },
    'incomplete_context': {
        'name': 'Incomplete Context',
        'description': 'Agent didn\'t consider full system state',
        'keywords': ['broke', 'regression', 'other', 'related']
    }
}


def extract_keywords(text: str) -> Set[str]:
    """Extract keywords from text for pattern matching."""
    if not text:
        return set()

    words = text.lower().replace(',', ' ').replace('.', ' ').split()
    keywords = {w.strip() for w in words if len(w) > 2}
    return keywords


def categorize_root_cause(issue: Dict[str, Any]) -> str:
    """Determine most likely root cause category for an issue."""
    description = issue.get('description', '').lower()
    evidence = issue.get('evidence', {})

    # Check if issue was reopened (strong signal of missing verification)
    if issue.get('reopened_at'):
        return 'missing_verification'

    # Check keywords in description
    scores = defaultdict(int)
    desc_keywords = extract_keywords(description)

    for category, info in ROOT_CAUSES.items():
        for keyword in info['keywords']:
            if keyword in desc_keywords:
                scores[category] += 1

    # Return category with highest score, default to missing_verification
    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]

    return 'missing_verification'


def analyze_agent_issues(agent_name: str, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze all issues for a specific agent."""

    # Group issues by root cause
    by_root_cause = defaultdict(list)
    for issue in issues:
        root_cause = categorize_root_cause(issue)
        by_root_cause[root_cause].append(issue)

    # Find most common root cause
    if not by_root_cause:
        return None

    most_common_cause = max(by_root_cause.items(), key=lambda x: len(x[1]))
    cause_category, cause_issues = most_common_cause

    # Extract common keywords from issues
    all_keywords = set()
    for issue in cause_issues:
        all_keywords.update(extract_keywords(issue.get('description', '')))

    # Calculate metrics
    total_issues = len(issues)
    reopened_count = sum(1 for issue in issues if issue.get('reopened_at'))
    avg_resolution_time = calculate_avg_resolution_time(issues)

    return {
        'agent_name': agent_name,
        'total_issues': total_issues,
        'reopened_count': reopened_count,
        'reopened_rate': reopened_count / total_issues if total_issues > 0 else 0,
        'avg_resolution_time_hours': avg_resolution_time,
        'root_cause_category': cause_category,
        'root_cause_info': ROOT_CAUSES[cause_category],
        'pattern_issues': cause_issues,
        'common_keywords': sorted(list(all_keywords))[:10],
        'by_root_cause': dict(by_root_cause)
    }


def calculate_avg_resolution_time(issues: List[Dict[str, Any]]) -> float:
    """Calculate average time from created to resolved in hours."""
    resolution_times = []

    for issue in issues:
        created = issue.get('created_at')
        resolved = issue.get('resolved_at')

        if created and resolved:
            try:
                created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                resolved_dt = datetime.fromisoformat(resolved.replace('Z', '+00:00'))
                hours = (resolved_dt - created_dt).total_seconds() / 3600
                resolution_times.append(hours)
            except:
                continue

    if resolution_times:
        return sum(resolution_times) / len(resolution_times)

    return 0.0


def generate_improvement_proposal(analysis: Dict[str, Any]) -> str:
    """Generate improvement proposal markdown for an agent."""

    agent = analysis['agent_name']
    root_cause = analysis['root_cause_category']
    root_cause_info = analysis['root_cause_info']
    total_issues = analysis['total_issues']
    reopened_count = analysis['reopened_count']
    pattern_issues = analysis['pattern_issues'][:3]  # Top 3 examples

    # Generate proposal based on root cause
    if root_cause == 'missing_verification':
        proposal = generate_verification_proposal(agent, pattern_issues)
    elif root_cause == 'unclear_instructions':
        proposal = generate_clarity_proposal(agent, pattern_issues)
    elif root_cause == 'wrong_approach':
        proposal = generate_approach_proposal(agent, pattern_issues)
    elif root_cause == 'missing_domain_knowledge':
        proposal = generate_knowledge_proposal(agent, pattern_issues)
    else:  # incomplete_context
        proposal = generate_context_proposal(agent, pattern_issues)

    # Build markdown
    md = f"""## {agent}

### Issue Pattern: {root_cause_info['name']} ({total_issues} occurrence{'s' if total_issues > 1 else ''})

**Root Cause**: {root_cause_info['description']}

**Evidence**:
"""

    for i, issue in enumerate(pattern_issues, 1):
        desc = issue.get('description', 'Unknown issue')
        reopened = ' (REOPENED)' if issue.get('reopened_at') else ''
        md += f"- Issue: \"{desc}\"{reopened}\n"

    md += f"\n**Reopened Rate**: {reopened_count}/{total_issues} ({analysis['reopened_rate']*100:.0f}%)\n"
    md += f"**Avg Resolution Time**: {analysis['avg_resolution_time_hours']:.1f} hours\n\n"
    md += proposal
    md += "\n\n---\n\n"

    return md


def generate_verification_proposal(agent: str, issues: List[Dict[str, Any]]) -> str:
    """Generate proposal for missing verification issues."""

    # Analyze what kind of verification is missing
    keywords = set()
    for issue in issues:
        keywords.update(extract_keywords(issue.get('description', '')))

    if 'crash' in keywords or 'error' in keywords:
        verification_type = 'error reproduction and verification'
        example = """
**Proposed Improvement**:
Add explicit verification steps to agent checklist:

```markdown
Before claiming completion:
- [ ] Reproduced the original error/crash
- [ ] Applied the fix
- [ ] Verified the error no longer occurs
- [ ] Checked for console errors/warnings
- [ ] Tested related functionality still works
```

**Expected Impact**: Reduce false completions by 60-80%
"""
    elif 'performance' in keywords or 'slow' in keywords:
        verification_type = 'performance measurement'
        example = """
**Proposed Improvement**:
Add performance verification to agent checklist:

```markdown
Before claiming completion:
- [ ] Measured performance BEFORE fix (baseline)
- [ ] Applied the fix
- [ ] Measured performance AFTER fix
- [ ] Verified improvement meets requirements
- [ ] Tested with realistic data volume
```

**Expected Impact**: Reduce performance-related false completions by 70%
"""
    else:
        verification_type = 'functional testing'
        example = """
**Proposed Improvement**:
Add explicit testing steps to agent checklist:

```markdown
Before claiming completion:
- [ ] Identified test scenario
- [ ] Applied the fix
- [ ] Tested the specific functionality
- [ ] Verified expected behavior
- [ ] Checked for side effects
```

**Expected Impact**: Reduce false completions by 50-70%
"""

    return example


def generate_clarity_proposal(agent: str, issues: List[Dict[str, Any]]) -> str:
    """Generate proposal for unclear instruction issues."""

    return """
**Proposed Improvement**:
Add concrete examples and acceptance criteria to agent instructions:

```markdown
## Definition of Done

When implementing visual consistency:
- Provide specific measurements (e.g., "all rows 40px height")
- Include screenshot or mockup if available
- Test with multiple data scenarios
- Verify consistency across all instances

Example: "Make all rows same height"
✅ Good: Set all table rows to 40px height, ensure padding is consistent
❌ Bad: Adjust CSS to make them look similar
```

**Expected Impact**: Reduce clarity-related issues by 60%
"""


def generate_approach_proposal(agent: str, issues: List[Dict[str, Any]]) -> str:
    """Generate proposal for wrong approach issues."""

    return """
**Proposed Improvement**:
Add decision tree or approach guidance to agent instructions:

```markdown
## Problem-Solving Approach

Before implementing, consider:
1. **Root cause**: What's the actual problem? (Not just symptoms)
2. **Scope**: Is this a component issue or system-wide?
3. **Strategy**: Quick fix vs. proper solution?

For performance issues:
- Measure first (don't optimize blindly)
- Consider: Algorithm, database query, caching, indexing
- Validate improvement after fix

For UI issues:
- Check if CSS or component architecture issue
- Consider: Styling vs. refactoring vs. framework change
```

**Expected Impact**: Reduce wrong approach issues by 50%
"""


def generate_knowledge_proposal(agent: str, issues: List[Dict[str, Any]]) -> str:
    """Generate proposal for missing domain knowledge issues."""

    return """
**Proposed Improvement**:
Add framework-specific examples and resources to agent instructions:

```markdown
## Framework Knowledge

### Vue 3 Composition API
- Use `ref()` for reactive primitives
- Use `reactive()` for objects
- Use `computed()` for derived state

### Common Patterns
- [Add specific examples from resolved issues]
- [Link to framework documentation]

Before implementing, review:
- Official framework documentation
- Project's existing patterns
- Similar implementations in codebase
```

**Expected Impact**: Reduce knowledge gap issues by 40-60%
"""


def generate_context_proposal(agent: str, issues: List[Dict[str, Any]]) -> str:
    """Generate proposal for incomplete context issues."""

    return """
**Proposed Improvement**:
Add context-awareness checklist to agent instructions:

```markdown
## Context Awareness

Before making changes:
- [ ] Identify all components/files affected
- [ ] Check for dependencies (imports, references)
- [ ] Review related functionality
- [ ] Test integration points
- [ ] Verify no regressions in related features

After making changes:
- [ ] Test the changed component
- [ ] Test dependent components
- [ ] Run integration tests
- [ ] Check for unexpected side effects
```

**Expected Impact**: Reduce context-related issues by 50-60%
"""


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Analyze resolved issues for root causes')
    parser.add_argument('--min-issues', type=int, default=2,
                       help='Minimum issues per agent to generate proposal (default: 2)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output file path (default: reports/improvement_proposals/YYYY-MM.md)')

    args = parser.parse_args()

    # Load resolved issues
    tracker = IssueTracker()
    all_issues = tracker.get_all_issues()

    resolved_issues = [
        issue for issue in all_issues.values()
        if issue.get('state') == 'resolved'
    ]

    if not resolved_issues:
        print("No resolved issues found. Need resolved issues to analyze patterns.")
        print("\nTo get resolved issues:")
        print("  1. Run weekly/monthly reviews")
        print("  2. Confirm issues are fixed when prompted")
        print("  3. Issues will be marked as resolved")
        print("  4. Re-run this script to analyze patterns")
        return

    print(f"\n📊 Analyzing {len(resolved_issues)} resolved issues...")

    # Group issues by agent
    by_agent = defaultdict(list)
    for issue in resolved_issues:
        agent_name = issue.get('agent_name', 'unknown')
        by_agent[agent_name].append(issue)

    print(f"   Found issues for {len(by_agent)} agents")

    # Analyze each agent
    analyses = []
    for agent_name, agent_issues in by_agent.items():
        if len(agent_issues) >= args.min_issues:
            analysis = analyze_agent_issues(agent_name, agent_issues)
            if analysis:
                analyses.append(analysis)
                print(f"   ✓ {agent_name}: {len(agent_issues)} issues, "
                      f"root cause: {analysis['root_cause_info']['name']}")

    if not analyses:
        print(f"\n⚠️  No agents with >={args.min_issues} issues found.")
        print(f"   Current issue counts:")
        for agent_name, agent_issues in sorted(by_agent.items(),
                                                key=lambda x: len(x[1]),
                                                reverse=True):
            print(f"     {agent_name}: {len(agent_issues)} issue(s)")
        print(f"\n   Lower --min-issues threshold or wait for more data.")
        return

    # Generate improvement proposals
    print(f"\n📝 Generating improvement proposals for {len(analyses)} agents...")

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        reports_dir = Path(__file__).parent.parent.parent / 'reports' / 'improvement_proposals'
        reports_dir.mkdir(parents=True, exist_ok=True)
        output_file = reports_dir / f"{datetime.now().strftime('%Y-%m')}.md"

    # Generate markdown report
    with open(output_file, 'w') as f:
        f.write(f"# Improvement Proposals - {datetime.now().strftime('%B %Y')}\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Analyzed**: {len(resolved_issues)} resolved issues across {len(by_agent)} agents\n\n")
        f.write(f"**Proposals**: {len(analyses)} agents with patterns identified\n\n")
        f.write("---\n\n")

        # Sort by total issues (most problematic first)
        for analysis in sorted(analyses, key=lambda x: x['total_issues'], reverse=True):
            proposal = generate_improvement_proposal(analysis)
            f.write(proposal)

    print(f"\n✓ Proposals saved to: {output_file}")
    print(f"\nNext steps:")
    print(f"  1. Review proposals: cat {output_file}")
    print(f"  2. Edit proposals if needed")
    print(f"  3. Apply improvements to agent markdown files")
    print(f"  4. Track metrics to validate improvements")


if __name__ == '__main__':
    main()
