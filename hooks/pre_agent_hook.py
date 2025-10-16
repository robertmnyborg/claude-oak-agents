#!/usr/bin/env python3
"""
Pre-Agent Hook for Telemetry Logging

This hook is invoked BEFORE an agent starts execution.
It logs the invocation start with state features.

Usage (from Claude Code):
  pre_agent_hook.py <agent_name> <agent_type> <task_description>

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
    from state_analysis.feature_extractor import FeatureExtractor
except ImportError as e:
    # If imports fail, just exit silently (don't block agent execution)
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


def get_workspace_dir():
    """Get the current workspace directory."""
    # Try to get from environment
    workspace = os.getenv("PWD") or os.getenv("OLDPWD") or os.getcwd()
    return Path(workspace)


def extract_state_features():
    """Extract state features from current workspace."""
    try:
        workspace = get_workspace_dir()
        extractor = FeatureExtractor(workspace_dir=workspace)
        return extractor.extract_all_features()
    except Exception as e:
        print(f"Warning: Could not extract state features: {e}", file=sys.stderr)
        return {}


def log_agent_start(agent_name, agent_type, task_description):
    """Log agent invocation start."""
    try:
        telemetry_dir = get_telemetry_dir()
        logger = TelemetryLogger(telemetry_dir=telemetry_dir)

        # Extract state features
        state_features = extract_state_features()

        # Log invocation
        invocation_id = logger.log_invocation(
            agent_name=agent_name,
            agent_type=agent_type,
            task_description=task_description,
            state_features=state_features,
            metadata={
                "hook_version": "1.0",
                "workspace": str(get_workspace_dir())
            }
        )

        # Store invocation ID in temp file for post-hook
        temp_file = telemetry_dir / f".current_invocation_{agent_name}.tmp"
        with open(temp_file, "w") as f:
            json.dump({
                "invocation_id": invocation_id,
                "agent_name": agent_name,
                "start_time": datetime.utcnow().isoformat()
            }, f)

        print(f"✓ Logged agent start: {agent_name} ({invocation_id[:8]}...)", file=sys.stderr)
        return invocation_id

    except Exception as e:
        # Don't fail agent execution if logging fails
        print(f"Warning: Telemetry logging failed: {e}", file=sys.stderr)
        return None


def main():
    """Main entry point for pre-agent hook."""
    # Check if telemetry is enabled
    if not is_telemetry_enabled():
        sys.exit(0)

    # Parse arguments
    if len(sys.argv) < 4:
        print("Usage: pre_agent_hook.py <agent_name> <agent_type> <task_description>", file=sys.stderr)
        sys.exit(0)  # Don't fail - just skip logging

    agent_name = sys.argv[1]
    agent_type = sys.argv[2]
    task_description = " ".join(sys.argv[3:])

    # Log agent start
    log_agent_start(agent_name, agent_type, task_description)

    # Exit successfully (don't block agent execution)
    sys.exit(0)


if __name__ == "__main__":
    main()
