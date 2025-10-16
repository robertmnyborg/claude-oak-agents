#!/usr/bin/env python3
"""
Agent Review and Approval System

Manages the review and approval workflow for newly created agents.
Provides commands to list, review, approve, modify, and reject pending agents.
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
import subprocess


# Directories
PROJECT_ROOT = Path(__file__).parent.parent
PENDING_DIR = PROJECT_ROOT / "agents" / "pending_review"
AGENTS_DIR = PROJECT_ROOT / "agents"
REJECTED_DIR = PROJECT_ROOT / "agents" / "rejected"
REVIEW_LOG = PROJECT_ROOT / "telemetry" / "agent_reviews.jsonl"

# Ensure directories exist
PENDING_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)


def log_review_decision(agent_name: str, action: str, reasoning: str = ""):
    """Log review decision for audit trail."""
    REVIEW_LOG.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent_name": agent_name,
        "action": action,  # approved, modified, rejected
        "reasoning": reasoning,
        "reviewer": "human"  # Could be expanded to track who
    }

    with open(REVIEW_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def list_pending_agents():
    """List all agents pending review."""
    pending_agents = list(PENDING_DIR.glob("*.md"))

    if not pending_agents:
        print("✓ No agents pending review")
        return []

    print(f"\n📋 Agents Pending Review ({len(pending_agents)}):")
    print("=" * 60)

    for agent_file in pending_agents:
        agent_name = agent_file.stem
        created_time = datetime.fromtimestamp(agent_file.stat().st_mtime)
        age_days = (datetime.now() - created_time).days

        # Read first few lines to get description
        with open(agent_file, 'r') as f:
            content = f.read()
            # Extract description from frontmatter
            if 'description:' in content:
                desc_line = [line for line in content.split('\n') if line.startswith('description:')]
                if desc_line:
                    description = desc_line[0].replace('description:', '').strip()
                else:
                    description = "No description"
            else:
                description = "No description"

        print(f"\n  {agent_name}")
        print(f"  └─ {description}")
        print(f"  └─ Created: {age_days} days ago")

    print("\n" + "=" * 60)
    print(f"\nReview command: oak-review-agent <agent-name>")

    return [a.stem for a in pending_agents]


def review_agent(agent_name: str):
    """Display agent specification for review."""
    agent_file = PENDING_DIR / f"{agent_name}.md"

    if not agent_file.exists():
        print(f"❌ Agent not found: {agent_name}")
        print(f"   Use 'oak-list-pending-agents' to see pending agents")
        return False

    print(f"\n📄 Agent Specification: {agent_name}")
    print("=" * 60)

    with open(agent_file, 'r') as f:
        content = f.read()
        print(content)

    print("\n" + "=" * 60)
    print(f"\nActions:")
    print(f"  oak-approve-agent {agent_name}              - Deploy agent")
    print(f"  oak-modify-agent {agent_name}               - Edit and approve")
    print(f"  oak-reject-agent {agent_name} \"<reason>\"  - Reject with reason")

    return True


def approve_agent(agent_name: str, from_modification: bool = False):
    """Approve agent and deploy to active agents directory."""
    source_file = PENDING_DIR / f"{agent_name}.md"

    if not source_file.exists():
        print(f"❌ Agent not found: {agent_name}")
        return False

    target_file = AGENTS_DIR / f"{agent_name}.md"

    # Check if agent already exists
    if target_file.exists():
        print(f"⚠️  Agent {agent_name} already exists in agents directory")
        print(f"   This will overwrite the existing agent.")
        response = input(f"   Continue? (y/n): ")
        if response.lower() != 'y':
            print("   Cancelled")
            return False

    # Move agent to active directory
    shutil.move(str(source_file), str(target_file))

    # Log decision
    action = "modified_and_approved" if from_modification else "approved"
    log_review_decision(agent_name, action, "Agent meets quality standards")

    print(f"\n✓ Agent approved and deployed: {agent_name}")
    print(f"  Location: {target_file}")
    print(f"\nAgent is now active and available for delegation!")

    return True


def modify_agent(agent_name: str):
    """Open agent in editor for modification."""
    agent_file = PENDING_DIR / f"{agent_name}.md"

    if not agent_file.exists():
        print(f"❌ Agent not found: {agent_name}")
        return False

    # Determine editor
    editor = subprocess.run(['which', 'code'], capture_output=True).returncode == 0
    if editor:
        editor_cmd = 'code'
    else:
        editor = subprocess.run(['which', 'vim'], capture_output=True).returncode == 0
        if editor:
            editor_cmd = 'vim'
        else:
            editor_cmd = 'nano'

    print(f"\n📝 Opening {agent_name} in {editor_cmd}...")
    print(f"   Location: {agent_file}")
    print(f"\n   After editing, run: oak-approve-agent {agent_name}")

    # Open in editor
    subprocess.run([editor_cmd, str(agent_file)])

    # Ask if user wants to approve now
    print(f"\n✓ Editor closed")
    response = input(f"   Approve agent now? (y/n): ")

    if response.lower() == 'y':
        return approve_agent(agent_name, from_modification=True)
    else:
        print(f"   Agent saved. Approve later with: oak-approve-agent {agent_name}")
        return True


def reject_agent(agent_name: str, reason: str):
    """Reject agent and archive with reasoning."""
    source_file = PENDING_DIR / f"{agent_name}.md"

    if not source_file.exists():
        print(f"❌ Agent not found: {agent_name}")
        return False

    # Create rejection metadata
    rejection_data = {
        "agent_name": agent_name,
        "rejected_date": datetime.now().isoformat(),
        "reason": reason,
        "rejected_by": "human"
    }

    # Move to rejected directory with metadata
    rejected_file = REJECTED_DIR / f"{agent_name}.md"
    metadata_file = REJECTED_DIR / f"{agent_name}_rejection.json"

    shutil.move(str(source_file), str(rejected_file))

    with open(metadata_file, 'w') as f:
        json.dump(rejection_data, f, indent=2)

    # Log decision
    log_review_decision(agent_name, "rejected", reason)

    print(f"\n✓ Agent rejected: {agent_name}")
    print(f"  Reason: {reason}")
    print(f"  Archived to: {rejected_file}")

    return True


def check_pending():
    """Quick check if any agents are pending review."""
    pending_agents = list(PENDING_DIR.glob("*.md"))

    if not pending_agents:
        print("✓ No agents pending review")
        return 0

    count = len(pending_agents)
    print(f"⚠️  {count} agent{'s' if count > 1 else ''} pending review:")
    for agent_file in pending_agents:
        print(f"   - {agent_file.stem}")

    print(f"\nRun 'oak-list-pending-agents' to see details")
    return count


def main():
    """Main command dispatcher."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  oak-list-pending-agents                    - List all pending agents")
        print("  oak-review-agent <name>                    - Review agent specification")
        print("  oak-approve-agent <name>                   - Approve and deploy agent")
        print("  oak-modify-agent <name>                    - Edit agent before approving")
        print("  oak-reject-agent <name> \"<reason>\"        - Reject agent with reason")
        print("  oak-check-pending                          - Quick check for pending agents")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_pending_agents()

    elif command == "review":
        if len(sys.argv) < 3:
            print("Usage: oak-review-agent <agent-name>")
            sys.exit(1)
        review_agent(sys.argv[2])

    elif command == "approve":
        if len(sys.argv) < 3:
            print("Usage: oak-approve-agent <agent-name>")
            sys.exit(1)
        approve_agent(sys.argv[2])

    elif command == "modify":
        if len(sys.argv) < 3:
            print("Usage: oak-modify-agent <agent-name>")
            sys.exit(1)
        modify_agent(sys.argv[2])

    elif command == "reject":
        if len(sys.argv) < 4:
            print("Usage: oak-reject-agent <agent-name> \"<reason>\"")
            sys.exit(1)
        reject_agent(sys.argv[2], sys.argv[3])

    elif command == "check":
        check_pending()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
