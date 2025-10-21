#!/usr/bin/env python3
"""
Approve Proposal

Approves an improvement proposal for an agent.

Usage:
  python3 scripts/phase2/approve_proposal.py <agent-name> [notes]
  oak-approve-proposal <agent-name>
  oak-approve-proposal <agent-name> "Looks good, will apply"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from telemetry.proposal_tracker import ProposalTracker


def approve_proposal(agent_name: str, notes: str = None):
    """Approve a proposal for an agent."""
    tracker = ProposalTracker()
    proposals = tracker.get_proposals_by_agent(agent_name)

    if not proposals:
        print(f"\n❌ No proposals found for agent: {agent_name}")
        return

    # Find pending proposals
    pending = [p for p in proposals if p['state'] == 'pending']

    if not pending:
        print(f"\n❌ No pending proposals for {agent_name}")
        print(f"   (All proposals have been reviewed)")
        return

    # Approve most recent pending proposal
    proposal = sorted(pending, key=lambda x: x['created_at'], reverse=True)[0]
    proposal_id = proposal['proposal_id']

    tracker.approve_proposal(proposal_id, notes)

    print(f"\n✅ Approved proposal for {agent_name}")
    if notes:
        print(f"   Notes: {notes}")

    print(f"\nNext steps:")
    print(f"  1. Apply changes: oak-apply-improvements")
    print(f"  2. Or manually edit: agents/{agent_name}.md")
    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: oak-approve-proposal <agent-name> [notes]")
        print("\nExample:")
        print("  oak-approve-proposal frontend-developer")
        print("  oak-approve-proposal frontend-developer \"Good improvement\"")
        sys.exit(1)

    agent_name = sys.argv[1]
    notes = sys.argv[2] if len(sys.argv) > 2 else None

    approve_proposal(agent_name, notes)


if __name__ == '__main__':
    main()
