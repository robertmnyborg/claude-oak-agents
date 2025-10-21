#!/usr/bin/env python3
"""
Review Proposal

Shows details of a specific improvement proposal.

Usage:
  python3 scripts/phase2/review_proposal.py <agent-name>
  oak-review-proposal <agent-name>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from telemetry.proposal_tracker import ProposalTracker


def review_proposal(agent_name: str):
    """Show proposal details for a specific agent."""
    tracker = ProposalTracker()
    proposals = tracker.get_proposals_by_agent(agent_name)

    if not proposals:
        print(f"\n❌ No proposals found for agent: {agent_name}")
        print("\nAvailable agents with proposals:")
        all_proposals = tracker.get_all_proposals()
        agents = set(p['agent_name'] for p in all_proposals.values())
        for agent in sorted(agents):
            print(f"  - {agent}")
        return

    # Get the most recent pending or approved proposal
    pending_or_approved = [p for p in proposals if p['state'] in ['pending', 'approved']]

    if not pending_or_approved:
        print(f"\n✓ No pending proposals for {agent_name}")
        print(f"  All proposals have been reviewed.")
        return

    # Show most recent
    proposal = sorted(pending_or_approved, key=lambda x: x['created_at'], reverse=True)[0]

    print("\n" + "=" * 70)
    print(f"📋 Improvement Proposal: {agent_name}")
    print("=" * 70)

    print(f"\nPeriod: {proposal['proposal_period']}")
    print(f"Status: {proposal['state'].upper()}")
    print(f"Root Cause: {proposal['root_cause'].replace('_', ' ').title()}")
    print(f"Issues Addressed: {proposal['issue_count']}")
    print(f"Expected Impact: {proposal['expected_impact']}")

    print("\n" + "-" * 70)
    print("PROPOSAL CONTENT")
    print("-" * 70)
    print(proposal['proposal_content'])
    print("-" * 70)

    # Show history if any
    if proposal.get('history'):
        print("\nHistory:")
        for h in proposal['history']:
            print(f"  {h['timestamp'][:10]}: {h['from_state']} → {h['to_state']}")
            if h['notes']:
                print(f"    Notes: {h['notes']}")

    # Show next actions
    print("\n" + "=" * 70)
    print("Actions:")
    if proposal['state'] == 'pending':
        proposal_id = proposal['proposal_id']
        print(f"  Approve:  oak-approve-proposal {agent_name}")
        print(f"  Reject:   oak-reject-proposal {agent_name} \"<reason>\"")
    elif proposal['state'] == 'approved':
        print(f"  Apply:    oak-apply-improvements")
        print(f"  (or manually edit agents/{agent_name}.md)")
    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: oak-review-proposal <agent-name>")
        print("\nExample:")
        print("  oak-review-proposal frontend-developer")
        sys.exit(1)

    agent_name = sys.argv[1]
    review_proposal(agent_name)


if __name__ == '__main__':
    main()
