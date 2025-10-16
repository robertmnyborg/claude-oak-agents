#!/usr/bin/env python3
"""
Post-Agent Hook for Telemetry Logging

This hook is invoked AFTER an agent completes execution.
It updates the invocation with completion data.

Usage (from Claude Code):
  post_agent_hook.py <agent_name> <exit_code> [files_modified...]

Environment Variables:
  OAK_TELEMETRY_DIR: Directory for telemetry logs (default: ~/Projects/claude-oak-agents/telemetry)
  OAK_TELEMETRY_ENABLED: Set to "false" to disable logging (default: true)
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from telemetry.logger import TelemetryLogger
except ImportError as e:
    # If imports fail, just exit silently (don't block workflow)
    print(f"Warning: Could not import telemetry modules: {e}", file=sys.stderr)
    sys.exit(0)


def is_telemetry_enabled():
    """Check if telemetry is enabled."""
    enabled = os.getenv("OAK_TELEMETRY_ENABLED", "true").lower()
    return enabled in ["true", "1", "yes", "on"]


def get_telemetry_dir():
    """Get the telemetry directory."""
    env_dir = os.getenv("OAK_TELEMETRY_DIR")
    if env_dir:
        return Path(env_dir)
    return PROJECT_ROOT / "telemetry"


def get_invocation_info(agent_name):
    """Retrieve invocation info from temp file."""
    telemetry_dir = get_telemetry_dir()
    temp_file = telemetry_dir / f".current_invocation_{agent_name}.tmp"

    if not temp_file.exists():
        return None

    try:
        with open(temp_file, "r") as f:
            data = json.load(f)

        # Clean up temp file
        temp_file.unlink()

        return data
    except Exception as e:
        print(f"Warning: Could not read invocation info: {e}", file=sys.stderr)
        return None


def calculate_duration(start_time_iso):
    """Calculate duration in seconds from start time."""
    try:
        start_time = datetime.fromisoformat(start_time_iso.replace('Z', '+00:00'))
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        return duration
    except Exception:
        return None


def log_agent_completion(agent_name, exit_code, files_modified):
    """Log agent completion."""
    try:
        # Get invocation info from pre-hook
        inv_info = get_invocation_info(agent_name)
        if not inv_info:
            print(f"Warning: No invocation info found for {agent_name}", file=sys.stderr)
            return

        invocation_id = inv_info["invocation_id"]
        start_time = inv_info["start_time"]

        # Calculate duration
        duration = calculate_duration(start_time)

        # Determine outcome status from exit code
        if exit_code == 0:
            outcome_status = "success"
        elif exit_code == 1:
            outcome_status = "failure"
        else:
            outcome_status = "partial"

        # Log completion
        telemetry_dir = get_telemetry_dir()
        logger = TelemetryLogger(telemetry_dir=telemetry_dir)

        logger.update_invocation(
            invocation_id=invocation_id,
            duration_seconds=duration,
            outcome_status=outcome_status,
            files_modified=files_modified if files_modified else [],
            tools_used=[]  # TODO: Could be tracked in future
        )

        print(f"✓ Logged agent completion: {agent_name} ({outcome_status}, {duration:.1f}s)", file=sys.stderr)

        # Optionally prompt for feedback (if interactive)
        if os.isatty(sys.stdin.fileno()) and os.getenv("OAK_PROMPT_FEEDBACK", "false").lower() == "true":
            prompt_for_feedback(logger, invocation_id, agent_name)

    except Exception as e:
        # Don't fail workflow if logging fails
        print(f"Warning: Telemetry logging failed: {e}", file=sys.stderr)


def prompt_for_feedback(logger, invocation_id, agent_name):
    """Prompt user for feedback (optional)."""
    try:
        print(f"\n📊 Quick feedback for {agent_name}:", file=sys.stderr)
        print("  Success? (y/n): ", end="", file=sys.stderr)
        success_input = input().lower()
        success = success_input in ["y", "yes"]

        print("  Quality (1-5): ", end="", file=sys.stderr)
        quality_input = input()
        quality = int(quality_input) if quality_input.isdigit() else 3

        logger.log_success_metric(
            invocation_id=invocation_id,
            success=success,
            quality_rating=min(max(quality, 1), 5),
            feedback_source="human",
            feedback_notes="Interactive feedback"
        )

        print("  ✓ Feedback recorded!", file=sys.stderr)

    except (KeyboardInterrupt, EOFError):
        print("\n  Skipped feedback", file=sys.stderr)
    except Exception as e:
        print(f"\n  Warning: Could not record feedback: {e}", file=sys.stderr)


def main():
    """Main entry point for post-agent hook."""
    # Check if telemetry is enabled
    if not is_telemetry_enabled():
        sys.exit(0)

    # Parse arguments
    if len(sys.argv) < 3:
        print("Usage: post_agent_hook.py <agent_name> <exit_code> [files_modified...]", file=sys.stderr)
        sys.exit(0)  # Don't fail - just skip logging

    agent_name = sys.argv[1]
    try:
        exit_code = int(sys.argv[2])
    except ValueError:
        exit_code = 0

    files_modified = sys.argv[3:] if len(sys.argv) > 3 else []

    # Log agent completion
    log_agent_completion(agent_name, exit_code, files_modified)

    # Exit successfully (don't block workflow)
    sys.exit(0)


if __name__ == "__main__":
    main()
