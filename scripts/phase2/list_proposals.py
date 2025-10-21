#!/usr/bin/env python3
"""
List Proposals

Shows all improvement proposals and their current state.

Usage:
  python3 scripts/phase2/list_proposals.py
  oak-review-proposals
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from telemetry.proposal_tracker import ProposalTracker


def list_proposals():
    """List all proposals grouped by state."""
    tracker = ProposalTracker()
    all_proposals = tracker.get_all_proposals()

    if not all_proposals:
        print("\n📋 No improvement proposals found.")
        print("\nProposals are generated during monthly reviews.")
        print("Run: oak-monthly-review")
        return

    # Group by state
    by_state = {
        "pending": [],
        "approved": [],
        "rejected": [],
        "applied": []
    }

    for proposal in all_proposals.values():
        state = proposal.get("state", "pending")
        if state in by_state:
            by_state[state].append(proposal)

    # Get stats
    stats = tracker.get_statistics()

    print("\n📋 Improvement Proposals")
    print("=" * 70)
    print(f"\nTotal: {stats['total_proposals']} proposals")
    print(f"  Pending:  {stats['by_state']['pending']}")
    print(f"  Approved: {stats['by_state']['approved']}")
    print(f"  Applied:  {stats['by_state']['applied']}")
    print(f"  Rejected: {stats['by_state']['rejected']}")

    # Show pending proposals (most important)
    if by_state["pending"]:
        print("\n" + "=" * 70)
        print("⏳ PENDING REVIEW")
        print("=" * 70)
        for proposal in sorted(by_state["pending"], key=lambda x: x['created_at'], reverse=True):
            agent = proposal['agent_name']
            period = proposal['proposal_period']
            root_cause = proposal['root_cause'].replace('_', ' ').title()
            issue_count = proposal['issue_count']
            expected = proposal['expected_impact']

            print(f"\n📌 {agent} ({period})")
            print(f"   Root Cause: {root_cause}")
            print(f"   Issues: {issue_count}")
            print(f"   Expected Impact: {expected}")
            print(f"   Review: oak-review-proposal {agent}")

    # Show approved proposals (ready to apply)
    if by_state["approved"]:
        print("\n" + "=" * 70)
        print("✅ APPROVED (Ready to Apply)")
        print("=" * 70)
        for proposal in sorted(by_state["approved"], key=lambda x: x.get('approved_at', ''), reverse=True):
            agent = proposal['agent_name']
            period = proposal['proposal_period']
            approved_at = proposal.get('approved_at', '')

            if approved_at:
                try:
                    dt = datetime.fromisoformat(approved_at.replace('Z', '+00:00'))
                    approved_str = dt.strftime('%Y-%m-%d')
                except:
                    approved_str = approved_at[:10]
            else:
                approved_str = 'Unknown'

            print(f"\n✅ {agent} ({period})")
            print(f"   Approved: {approved_str}")
            print(f"   Apply: oak-apply-improvements")

    # Show applied proposals (for history)
    if by_state["applied"]:
        print("\n" + "=" * 70)
        print("🎯 APPLIED")
        print("=" * 70)
        for proposal in sorted(by_state["applied"], key=lambda x: x.get('applied_at', ''), reverse=True)[:5]:
            agent = proposal['agent_name']
            period = proposal['proposal_period']
            applied_at = proposal.get('applied_at', '')

            if applied_at:
                try:
                    dt = datetime.fromisoformat(applied_at.replace('Z', '+00:00'))
                    applied_str = dt.strftime('%Y-%m-%d')
                except:
                    applied_str = applied_at[:10]
            else:
                applied_str = 'Unknown'

            print(f"   ✓ {agent} ({period}) - Applied {applied_str}")

        if len(by_state["applied"]) > 5:
            print(f"   ... and {len(by_state['applied']) - 5} more")

    # Show next steps
    print("\n" + "=" * 70)
    print("Next Steps:")
    if by_state["pending"]:
        print(f"  1. Review pending proposals:")
        for proposal in by_state["pending"][:3]:
            print(f"     oak-review-proposal {proposal['agent_name']}")
    if by_state["approved"]:
        print(f"  2. Apply approved proposals:")
        print(f"     oak-apply-improvements")
    if not by_state["pending"] and not by_state["approved"]:
        print(f"  - All proposals reviewed and applied! ✓")
        print(f"  - New proposals generated during monthly reviews")

    print()


if __name__ == '__main__':
    list_proposals()
