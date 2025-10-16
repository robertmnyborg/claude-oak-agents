#!/usr/bin/env python3
"""
Telemetry Logger for Claude OaK Agents

This module provides utilities for logging agent invocations and success metrics.
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class TelemetryLogger:
    """Handles logging of agent invocations and success metrics."""

    def __init__(self, telemetry_dir: Optional[Path] = None):
        """
        Initialize the telemetry logger.

        Args:
            telemetry_dir: Directory to store telemetry files.
                          Defaults to ./telemetry relative to this file.
        """
        if telemetry_dir is None:
            telemetry_dir = Path(__file__).parent

        self.telemetry_dir = Path(telemetry_dir)
        self.invocations_file = self.telemetry_dir / "agent_invocations.jsonl"
        self.metrics_file = self.telemetry_dir / "success_metrics.jsonl"
        self.stats_file = self.telemetry_dir / "performance_stats.json"

        # Ensure files exist
        self.invocations_file.touch(exist_ok=True)
        self.metrics_file.touch(exist_ok=True)

        # Session ID persists for the lifetime of this logger instance
        self.session_id = str(uuid.uuid4())

    def log_invocation(
        self,
        agent_name: str,
        agent_type: str,
        task_description: str,
        state_features: Optional[Dict[str, Any]] = None,
        parent_invocation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log an agent invocation at start time.

        Args:
            agent_name: Name of the agent (e.g., 'frontend-developer')
            agent_type: Category (development, quality, security, etc.)
            task_description: Human-readable task description
            state_features: Extracted state features (optional)
            parent_invocation_id: ID of parent agent if delegated (optional)
            metadata: Additional custom metadata (optional)

        Returns:
            invocation_id: Unique identifier for this invocation
        """
        invocation_id = str(uuid.uuid4())

        invocation_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "session_id": self.session_id,
            "invocation_id": invocation_id,
            "agent_name": agent_name,
            "agent_type": agent_type,
            "task_description": task_description,
            "state_features": state_features or {},
            "parent_invocation_id": parent_invocation_id,
            "tools_used": [],
            "duration_seconds": None,
            "outcome": {
                "status": "unknown",
                "error_message": None,
                "files_modified": [],
                "files_created": [],
                "tests_passed": None,
                "build_succeeded": None
            },
            "metadata": metadata or {}
        }

        with open(self.invocations_file, "a") as f:
            f.write(json.dumps(invocation_data) + "\n")

        return invocation_id

    def update_invocation(
        self,
        invocation_id: str,
        duration_seconds: Optional[float] = None,
        outcome_status: Optional[str] = None,
        error_message: Optional[str] = None,
        files_modified: Optional[List[str]] = None,
        files_created: Optional[List[str]] = None,
        tools_used: Optional[List[str]] = None,
        tests_passed: Optional[bool] = None,
        build_succeeded: Optional[bool] = None
    ) -> None:
        """
        Update an invocation record with completion data.

        This reads all invocations, updates the matching one, and rewrites the file.
        For high-volume scenarios, consider using a proper database.

        Args:
            invocation_id: The invocation ID to update
            duration_seconds: How long the agent ran
            outcome_status: success, failure, partial, unknown
            error_message: Error message if failed
            files_modified: List of file paths modified
            files_created: List of file paths created
            tools_used: List of tool names used
            tests_passed: Whether tests passed
            build_succeeded: Whether build succeeded
        """
        invocations = []
        updated = False

        # Read all invocations
        with open(self.invocations_file, "r") as f:
            for line in f:
                if line.strip():
                    invocations.append(json.loads(line))

        # Update the matching invocation
        for inv in invocations:
            if inv["invocation_id"] == invocation_id:
                if duration_seconds is not None:
                    inv["duration_seconds"] = duration_seconds
                if outcome_status is not None:
                    inv["outcome"]["status"] = outcome_status
                if error_message is not None:
                    inv["outcome"]["error_message"] = error_message
                if files_modified is not None:
                    inv["outcome"]["files_modified"] = files_modified
                if files_created is not None:
                    inv["outcome"]["files_created"] = files_created
                if tools_used is not None:
                    inv["tools_used"] = tools_used
                if tests_passed is not None:
                    inv["outcome"]["tests_passed"] = tests_passed
                if build_succeeded is not None:
                    inv["outcome"]["build_succeeded"] = build_succeeded
                updated = True
                break

        if not updated:
            raise ValueError(f"Invocation ID {invocation_id} not found")

        # Rewrite the file
        with open(self.invocations_file, "w") as f:
            for inv in invocations:
                f.write(json.dumps(inv) + "\n")

    def log_success_metric(
        self,
        invocation_id: str,
        success: bool,
        quality_rating: int,
        feedback_source: str = "human",
        feedback_notes: Optional[str] = None,
        would_use_again: Optional[bool] = None,
        alternative_agent_suggested: Optional[str] = None
    ) -> None:
        """
        Log success metrics for an invocation.

        Args:
            invocation_id: References the agent invocation
            success: Did the agent accomplish the task?
            quality_rating: 1-5 quality score
            feedback_source: human, automated_tests, build_system, linter
            feedback_notes: Free-form feedback text
            would_use_again: Would you use this agent again for similar tasks?
            alternative_agent_suggested: If not ideal, which agent would be better?
        """
        if not 1 <= quality_rating <= 5:
            raise ValueError("quality_rating must be between 1 and 5")

        metric_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "invocation_id": invocation_id,
            "success": success,
            "quality_rating": quality_rating,
            "feedback_source": feedback_source,
            "feedback_notes": feedback_notes,
            "would_use_again": would_use_again,
            "alternative_agent_suggested": alternative_agent_suggested
        }

        with open(self.metrics_file, "a") as f:
            f.write(json.dumps(metric_data) + "\n")

    def get_session_id(self) -> str:
        """Return the current session ID."""
        return self.session_id


def main():
    """Example usage of the telemetry logger."""
    logger = TelemetryLogger()

    # Example: Log a frontend development task
    invocation_id = logger.log_invocation(
        agent_name="frontend-developer",
        agent_type="development",
        task_description="Add dark mode toggle to settings page",
        state_features={
            "codebase": {
                "languages": ["TypeScript", "CSS"],
                "frameworks": ["React", "TailwindCSS"]
            },
            "task": {
                "type": "feature_development",
                "scope": "small",
                "risk_level": "low"
            }
        }
    )

    print(f"Logged invocation: {invocation_id}")

    # Simulate agent completion
    logger.update_invocation(
        invocation_id=invocation_id,
        duration_seconds=342.5,
        outcome_status="success",
        files_modified=["src/components/Settings.tsx", "src/styles/theme.css"],
        tools_used=["Edit", "Bash", "Read"]
    )

    # Log human feedback
    logger.log_success_metric(
        invocation_id=invocation_id,
        success=True,
        quality_rating=4,
        feedback_source="human",
        feedback_notes="Component works well but could use better animations",
        would_use_again=True
    )

    print("Telemetry logged successfully!")


if __name__ == "__main__":
    main()
