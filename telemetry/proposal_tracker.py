#!/usr/bin/env python3
"""
Proposal Tracker

Tracks improvement proposal lifecycle from generation → review → approval/rejection → application.

Proposal States:
1. pending - Proposal generated, awaiting review
2. approved - User approved, ready to apply
3. rejected - User rejected with reasoning
4. applied - Changes applied to agent file

Storage: proposals.jsonl (append-only log, latest entry = current state)
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class ProposalTracker:
    """Manage proposal lifecycle with approval workflow."""

    def __init__(self, proposals_file: Optional[Path] = None):
        if proposals_file is None:
            self.proposals_file = Path(__file__).parent / "proposals.jsonl"
        else:
            self.proposals_file = Path(proposals_file)

        # Ensure file exists
        self.proposals_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.proposals_file.exists():
            self.proposals_file.touch()

    def create_proposal(
        self,
        agent_name: str,
        proposal_period: str,  # e.g., "2025-10"
        proposal_content: str,
        root_cause: str,
        issue_count: int,
        expected_impact: str
    ) -> str:
        """
        Create a new improvement proposal.

        Args:
            agent_name: Which agent this proposal is for
            proposal_period: YYYY-MM when proposal was generated
            proposal_content: The improvement proposal markdown
            root_cause: Root cause category
            issue_count: Number of issues this addresses
            expected_impact: Expected improvement (e.g., "reduce by 60%")

        Returns:
            proposal_id: Unique identifier for the proposal
        """
        proposal_id = str(uuid.uuid4())

        entry = {
            "proposal_id": proposal_id,
            "agent_name": agent_name,
            "proposal_period": proposal_period,
            "proposal_content": proposal_content,
            "root_cause": root_cause,
            "issue_count": issue_count,
            "expected_impact": expected_impact,
            "state": "pending",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "history": []
        }

        self._append_entry(entry)
        return proposal_id

    def update_state(
        self,
        proposal_id: str,
        new_state: str,
        notes: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Update proposal state.

        Args:
            proposal_id: Proposal to update
            new_state: New state (pending, approved, rejected, applied)
            notes: Optional notes about the state change
            **kwargs: Additional fields to update
        """
        # Get current proposal
        proposal = self.get_proposal(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")

        # Create updated entry
        old_state = proposal["state"]
        proposal["state"] = new_state
        proposal["updated_at"] = datetime.utcnow().isoformat() + "Z"

        # Add to history
        if "history" not in proposal:
            proposal["history"] = []

        proposal["history"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "from_state": old_state,
            "to_state": new_state,
            "notes": notes
        })

        # Update additional fields
        for key, value in kwargs.items():
            proposal[key] = value

        self._append_entry(proposal)

    def approve_proposal(self, proposal_id: str, notes: Optional[str] = None) -> None:
        """Approve a proposal."""
        self.update_state(
            proposal_id,
            "approved",
            notes=notes or "User approved proposal",
            approved_at=datetime.utcnow().isoformat() + "Z"
        )

    def reject_proposal(self, proposal_id: str, reason: str) -> None:
        """Reject a proposal with reasoning."""
        self.update_state(
            proposal_id,
            "rejected",
            notes=reason,
            rejected_at=datetime.utcnow().isoformat() + "Z"
        )

    def mark_applied(self, proposal_id: str, applied_changes: str) -> None:
        """Mark proposal as applied to agent file."""
        self.update_state(
            proposal_id,
            "applied",
            notes="Changes applied to agent markdown file",
            applied_at=datetime.utcnow().isoformat() + "Z",
            applied_changes=applied_changes
        )

    def get_proposal(self, proposal_id: str) -> Optional[Dict[str, Any]]:
        """Get current state of a proposal (latest entry with this ID)."""
        if not self.proposals_file.exists():
            return None

        latest = None
        with open(self.proposals_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                if entry.get("proposal_id") == proposal_id:
                    latest = entry

        return latest

    def get_proposals_by_agent(self, agent_name: str) -> List[Dict[str, Any]]:
        """Get all proposals for a specific agent (latest state of each)."""
        if not self.proposals_file.exists():
            return []

        # Read all proposals for this agent, keeping only latest version
        proposals_by_id = {}
        with open(self.proposals_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                if entry.get("agent_name") == agent_name:
                    proposal_id = entry.get("proposal_id")
                    if proposal_id:
                        proposals_by_id[proposal_id] = entry

        return list(proposals_by_id.values())

    def get_pending_proposals(self) -> List[Dict[str, Any]]:
        """Get all proposals in pending state."""
        return self.get_proposals_by_state("pending")

    def get_approved_proposals(self) -> List[Dict[str, Any]]:
        """Get all proposals in approved state."""
        return self.get_proposals_by_state("approved")

    def get_proposals_by_state(self, state: str) -> List[Dict[str, Any]]:
        """Get all proposals in a specific state."""
        if not self.proposals_file.exists():
            return []

        # Read all proposals, keeping only latest version of each
        proposals_by_id = {}
        with open(self.proposals_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                proposal_id = entry.get("proposal_id")
                if proposal_id:
                    proposals_by_id[proposal_id] = entry

        # Filter by state
        return [
            proposal for proposal in proposals_by_id.values()
            if proposal.get("state") == state
        ]

    def get_all_proposals(self) -> Dict[str, Dict[str, Any]]:
        """Get all proposals (latest state of each)."""
        if not self.proposals_file.exists():
            return {}

        proposals_by_id = {}
        with open(self.proposals_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                proposal_id = entry.get("proposal_id")
                if proposal_id:
                    proposals_by_id[proposal_id] = entry

        return proposals_by_id

    def get_statistics(self) -> Dict[str, Any]:
        """Get proposal statistics."""
        all_proposals = self.get_all_proposals()

        stats = {
            "total_proposals": len(all_proposals),
            "by_state": {
                "pending": 0,
                "approved": 0,
                "rejected": 0,
                "applied": 0
            },
            "by_agent": {}
        }

        for proposal in all_proposals.values():
            state = proposal.get("state", "pending")
            stats["by_state"][state] = stats["by_state"].get(state, 0) + 1

            agent = proposal.get("agent_name", "unknown")
            if agent not in stats["by_agent"]:
                stats["by_agent"][agent] = {
                    "total": 0,
                    "pending": 0,
                    "approved": 0,
                    "applied": 0
                }

            stats["by_agent"][agent]["total"] += 1
            if state in ["pending", "approved", "applied"]:
                stats["by_agent"][agent][state] += 1

        return stats

    def _append_entry(self, entry: Dict[str, Any]) -> None:
        """Append entry to JSONL file."""
        with open(self.proposals_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')


if __name__ == '__main__':
    # Example usage
    tracker = ProposalTracker()

    # Create a proposal
    proposal_id = tracker.create_proposal(
        agent_name="frontend-developer",
        proposal_period="2025-10",
        proposal_content="Add button verification to checklist...",
        root_cause="missing_verification",
        issue_count=5,
        expected_impact="reduce false completions by 60-80%"
    )

    print(f"Created proposal: {proposal_id}")

    # Approve it
    tracker.approve_proposal(proposal_id, "Good proposal, will apply")

    # Mark as applied
    tracker.mark_applied(proposal_id, "Added verification steps to checklist")

    # Get statistics
    stats = tracker.get_statistics()
    print(f"\nStatistics:")
    print(json.dumps(stats, indent=2))
