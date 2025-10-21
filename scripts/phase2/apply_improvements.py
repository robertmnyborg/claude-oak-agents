#!/usr/bin/env python3
"""
Apply Improvements

Applies all approved improvement proposals to agent markdown files.

Usage:
  python3 scripts/phase2/apply_improvements.py
  python3 scripts/phase2/apply_improvements.py --dry-run
  oak-apply-improvements
"""

import sys
import re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from telemetry.proposal_tracker import ProposalTracker


def extract_improvement_from_proposal(proposal_content: str) -> str:
    """Extract the improvement section from proposal markdown."""
    # Look for the "Proposed Improvement" section
    match = re.search(
        r'\*\*Proposed Improvement\*\*:?\s*(.*?)(?=\n\*\*|$)',
        proposal_content,
        re.DOTALL | re.IGNORECASE
    )

    if match:
        improvement = match.group(1).strip()

        # Extract content from markdown code blocks if present
        code_block_match = re.search(r'```markdown\s*(.*?)\s*```', improvement, re.DOTALL)
        if code_block_match:
            return code_block_match.group(1).strip()

        return improvement

    # Fallback: return whole proposal
    return proposal_content


def apply_proposal_to_agent(agent_name: str, improvement_text: str, dry_run: bool = False) -> bool:
    """
    Apply improvement to agent markdown file.

    Args:
        agent_name: Name of the agent
        improvement_text: Improvement text to add
        dry_run: If True, don't actually modify file

    Returns:
        True if successful, False otherwise
    """
    project_root = Path(__file__).parent.parent.parent
    agent_file = project_root / 'agents' / f'{agent_name}.md'

    if not agent_file.exists():
        print(f"   ⚠️  Agent file not found: {agent_file}")
        return False

    # Read current content
    with open(agent_file, 'r') as f:
        content = f.read()

    # Find the "Before Claiming Completion" section
    section_match = re.search(
        r'(## Before Claiming Completion.*?)(?=\n##|$)',
        content,
        re.DOTALL
    )

    if not section_match:
        print(f"   ⚠️  'Before Claiming Completion' section not found in {agent_name}.md")
        print(f"   💡 You can manually add this section and re-run")
        return False

    # Get the section content
    section_start = section_match.start()
    section_end = section_match.end()
    section_content = section_match.group(1)

    # Check if improvement already exists (avoid duplicates)
    if improvement_text[:50] in content:
        print(f"   ℹ️  Improvement appears to already be applied")
        return False

    # Find a good place to insert (after the last checklist or before Quality Gate)
    # Look for the last checklist item or example
    insert_match = re.search(
        r'(\*\*Example\*\*:.*?)(?=\n\n###|\n\n##|$)',
        section_content,
        re.DOTALL
    )

    if insert_match:
        # Insert after last example
        insert_pos = section_start + insert_match.end()
        new_content = (
            content[:insert_pos] +
            "\n\n### Additional Verification\n\n" + improvement_text +
            content[insert_pos:]
        )
    else:
        # Insert at end of section
        new_content = (
            content[:section_end] +
            "\n\n### Additional Verification\n\n" + improvement_text +
            content[section_end:]
        )

    if dry_run:
        print(f"   [DRY RUN] Would add improvement to {agent_name}.md")
        return True

    # Write updated content
    with open(agent_file, 'w') as f:
        f.write(new_content)

    print(f"   ✅ Applied improvement to agents/{agent_name}.md")
    return True


def apply_improvements(dry_run: bool = False):
    """Apply all approved proposals."""
    tracker = ProposalTracker()
    approved = tracker.get_approved_proposals()

    if not approved:
        print("\n✓ No approved proposals to apply")
        print("\nPending proposals:")
        pending = tracker.get_pending_proposals()
        if pending:
            print(f"  {len(pending)} proposals awaiting review")
            print("  Run: oak-review-proposals")
        else:
            print("  None - all caught up!")
        return

    print(f"\n📝 Applying {len(approved)} approved proposal(s)...")
    print("=" * 70)

    applied_count = 0
    failed_count = 0

    for proposal in sorted(approved, key=lambda x: x['agent_name']):
        agent = proposal['agent_name']
        print(f"\n{agent}:")

        # Extract improvement
        improvement = extract_improvement_from_proposal(proposal['proposal_content'])

        if not improvement:
            print(f"   ⚠️  Could not extract improvement from proposal")
            failed_count += 1
            continue

        # Show what will be added
        print(f"   Adding:")
        lines = improvement.split('\n')
        for line in lines[:5]:
            print(f"      {line}")
        if len(lines) > 5:
            print(f"      ... ({len(lines) - 5} more lines)")

        # Apply to agent file
        success = apply_proposal_to_agent(agent, improvement, dry_run)

        if success:
            # Mark as applied
            if not dry_run:
                tracker.mark_applied(
                    proposal['proposal_id'],
                    f"Added improvement to agents/{agent}.md"
                )
            applied_count += 1
        else:
            failed_count += 1

    # Summary
    print("\n" + "=" * 70)
    if dry_run:
        print(f"[DRY RUN] Would apply {applied_count} improvement(s)")
    else:
        print(f"✅ Applied {applied_count} improvement(s)")

    if failed_count > 0:
        print(f"⚠️  {failed_count} proposal(s) could not be applied automatically")
        print(f"   Review proposals and apply manually if needed")

    print("\nNext steps:")
    print(f"  1. Review changes: git diff agents/")
    print(f"  2. Test agents with new improvements")
    print(f"  3. Monitor metrics: python3 scripts/phase3/view_trends.py")
    print()


def main():
    dry_run = len(sys.argv) > 1 and sys.argv[1] == '--dry-run'

    apply_improvements(dry_run)


if __name__ == '__main__':
    main()
