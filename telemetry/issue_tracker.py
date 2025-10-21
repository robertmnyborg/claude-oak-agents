#!/usr/bin/env python3
"""
Issue Tracker

Tracks quality issues from detection → resolution with user confirmation workflow.

Issue Lifecycle:
1. open - Issue detected (user asked twice)
2. in_progress - Agent working on it
3. needs_verification - Agent claims fixed
4. resolved - User confirmed it works

Storage: issues.jsonl (append-only log, latest entry = current state)
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class IssueTracker:
    """Manage issue lifecycle with user confirmation."""

    def __init__(self, issues_file: Optional[Path] = None):
        if issues_file is None:
            self.issues_file = Path(__file__).parent / "issues.jsonl"
        else:
            self.issues_file = Path(issues_file)

        # Ensure file exists
        self.issues_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.issues_file.exists():
            self.issues_file.touch()

    def create_issue(
        self,
        agent_name: str,
        description: str,
        evidence: Dict[str, Any],
        category: str = "false_completion"
    ) -> str:
        """
        Create a new issue.

        Args:
            agent_name: Which agent failed
            description: What the issue is
            evidence: Supporting data (repetition count, keywords, etc.)
            category: Type of issue

        Returns:
            issue_id: Unique identifier for the issue
        """
        issue_id = str(uuid.uuid4())

        entry = {
            "issue_id": issue_id,
            "agent_name": agent_name,
            "description": description,
            "category": category,
            "state": "open",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "evidence": evidence,
            "history": []
        }

        self._append_entry(entry)
        return issue_id

    def update_state(
        self,
        issue_id: str,
        new_state: str,
        notes: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Update issue state.

        Args:
            issue_id: Issue to update
            new_state: New state (open, in_progress, needs_verification, resolved)
            notes: Optional notes about the state change
            **kwargs: Additional fields to update
        """
        # Get current issue
        issue = self.get_issue(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")

        # Create updated entry
        old_state = issue["state"]
        issue["state"] = new_state
        issue["updated_at"] = datetime.utcnow().isoformat() + "Z"

        # Add to history
        if "history" not in issue:
            issue["history"] = []

        issue["history"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "from_state": old_state,
            "to_state": new_state,
            "notes": notes
        })

        # Update additional fields
        for key, value in kwargs.items():
            issue[key] = value

        self._append_entry(issue)

    def get_issue(self, issue_id: str) -> Optional[Dict[str, Any]]:
        """Get current state of an issue (latest entry with this ID)."""
        if not self.issues_file.exists():
            return None

        latest = None
        with open(self.issues_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                if entry.get("issue_id") == issue_id:
                    latest = entry

        return latest

    def get_open_issues(self) -> List[Dict[str, Any]]:
        """Get all currently open issues."""
        return self.get_issues_by_state("open")

    def get_issues_needing_verification(self) -> List[Dict[str, Any]]:
        """Get issues waiting for user confirmation."""
        return self.get_issues_by_state("needs_verification")

    def get_issues_by_state(self, state: str) -> List[Dict[str, Any]]:
        """Get all issues in a specific state."""
        if not self.issues_file.exists():
            return []

        # Read all issues, keeping only latest version of each
        issues_by_id = {}
        with open(self.issues_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                issue_id = entry.get("issue_id")
                if issue_id:
                    issues_by_id[issue_id] = entry

        # Filter by state
        return [
            issue for issue in issues_by_id.values()
            if issue.get("state") == state
        ]

    def get_all_issues(self) -> Dict[str, Dict[str, Any]]:
        """Get all issues (latest state of each)."""
        if not self.issues_file.exists():
            return {}

        issues_by_id = {}
        with open(self.issues_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                issue_id = entry.get("issue_id")
                if issue_id:
                    issues_by_id[issue_id] = entry

        return issues_by_id

    def get_statistics(self) -> Dict[str, Any]:
        """Get issue statistics."""
        all_issues = self.get_all_issues()

        stats = {
            "total_issues": len(all_issues),
            "by_state": {
                "open": 0,
                "in_progress": 0,
                "needs_verification": 0,
                "resolved": 0
            },
            "by_agent": {}
        }

        for issue in all_issues.values():
            state = issue.get("state", "open")
            stats["by_state"][state] = stats["by_state"].get(state, 0) + 1

            agent = issue.get("agent_name", "unknown")
            if agent not in stats["by_agent"]:
                stats["by_agent"][agent] = {
                    "total": 0,
                    "open": 0,
                    "resolved": 0
                }

            stats["by_agent"][agent]["total"] += 1
            if state == "open":
                stats["by_agent"][agent]["open"] += 1
            elif state == "resolved":
                stats["by_agent"][agent]["resolved"] += 1

        return stats

    def _append_entry(self, entry: Dict[str, Any]) -> None:
        """Append entry to JSONL file."""
        with open(self.issues_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')


def prompt_user_confirmation(issue: Dict[str, Any]) -> str:
    """
    Prompt user to confirm issue resolution.

    Args:
        issue: Issue dict with description

    Returns:
        User response: "confirmed", "still_broken", or "will_test_later"
    """
    description = issue.get("description", "Unknown issue")
    agent = issue.get("agent_name", "Agent")

    print(f"\n{'='*70}")
    print(f"Verification Needed: {agent}")
    print(f"{'='*70}")
    print(f"\nIssue: {description}")
    print(f"\nThe agent claims this is fixed. Can you confirm?")
    print("\n  1. Yes, it's fixed")
    print("  2. No, still broken")
    print("  3. I'll test it later")

    while True:
        response = input("\nYour choice (1/2/3): ").strip()
        if response == "1":
            return "confirmed"
        elif response == "2":
            return "still_broken"
        elif response == "3":
            return "will_test_later"
        else:
            print("Please enter 1, 2, or 3")


if __name__ == '__main__':
    # Example usage
    tracker = IssueTracker()

    # Create an issue
    issue_id = tracker.create_issue(
        agent_name="frontend-developer",
        description="Button crash when adding secondary community",
        evidence={
            "repetition_count": 3,
            "keywords": ["crash", "button", "secondary", "community"]
        }
    )

    print(f"Created issue: {issue_id}")

    # Update to needs_verification
    tracker.update_state(issue_id, "needs_verification", notes="Agent claims fixed")

    # Get statistics
    stats = tracker.get_statistics()
    print(f"\nStatistics:")
    print(json.dumps(stats, indent=2))

    # Get issues needing verification
    issues = tracker.get_issues_needing_verification()
    print(f"\nIssues needing verification: {len(issues)}")
