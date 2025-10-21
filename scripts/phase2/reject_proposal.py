#!/usr/bin/env python3
"""
Reject Proposal

Rejects an improvement proposal for an agent with reasoning.

Usage:
  python3 scripts/phase2/reject_proposal.py <agent-name> "<reason>"
  oak-reject-proposal <agent-name> "<reason>"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from telemetry.proposal_tracker import ProposalTracker


def reject_proposal(agent_name: str, reason: str):
    """Reject a proposal for an agent with reasoning."""
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

    # Reject most recent pending proposal
    proposal = sorted(pending, key=lambda x: x['created_at'], reverse=True)[0]
    proposal_id = proposal['proposal_id']

    tracker.reject_proposal(proposal_id, reason)

    print(f"\n🚫 Rejected proposal for {agent_name}")
    print(f"   Reason: {reason}")
    print()


def main():
    if len(sys.argv) < 3:
        print("Usage: oak-reject-proposal <agent-name> \"<reason>\"")
        print("\nExample:")
        print("  oak-reject-proposal frontend-developer \"Already fixed manually\"")
        print("  oak-reject-proposal backend-architect \"Not the right approach\"")
        sys.exit(1)

    agent_name = sys.argv[1]
    reason = sys.argv[2]

    reject_proposal(agent_name, reason)


if __name__ == '__main__':
    main()
