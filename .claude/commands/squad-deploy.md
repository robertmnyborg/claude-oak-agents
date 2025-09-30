---
description: Deploy claude-agents squad to activate agents and CLAUDE.md configuration
argument-hint: [--local] [--global]
allowed-tools: Bash(*), Read(*), Write(*), Glob(*)
---

# Squad Deploy - Activate Claude Agents

Deploy the claude-agents squad to activate intelligent delegation and agent specialization.

## Deployment Options

**Arguments**: $ARGUMENTS

Choose your deployment target:

1. **Global Deployment** (default): Installs to `~/.claude/` for all projects
2. **Local Deployment** (`--local`): Installs to current project's `.claude/` directory

## What Squad Deploy Does

1. **Backup existing configuration** if present
2. **Copy agents** from `~/.claude/disabled_agents/` to active `agents/` directory
3. **Install CLAUDE.md** with mandatory delegation rules and agent coordination
4. **Activate agent system** with specialized domain routing

## Pre-Deployment Check

First, let me check your current environment:

!ls -la ~/.claude/disabled_agents/ 2>/dev/null || echo "❌ No disabled_agents found - run install.sh first"
!ls -la ~/.claude/templates/ 2>/dev/null || echo "❌ No templates found - run install.sh first"

## Deployment Target

Determine deployment location based on arguments:

**Deployment Mode**: $ARGUMENTS contains `--local` → Local project deployment, otherwise Global deployment

## Backup Current Configuration

Create timestamped backup of existing configuration before deployment.

## Deploy Squad

1. Copy all agents from `~/.claude/disabled_agents/` to target `agents/` directory
2. Copy `~/.claude/templates/CLAUDE.md` to target location
3. Verify deployment integrity
4. Report deployment status

## Enable Squad Functionality

After deployment, enable squad functionality:

!echo "CLAUDE_SQUAD_ENABLED=1" > ~/.claude/.squad_enabled

Update session hook to use toggle system:

!cat > ~/.claude/hooks/sessionStart.sh << 'EOF'
#!/bin/bash

# SessionStart hook to load SQUAD.md orchestration rules
# This hook runs at the beginning of each session and after /clear

# Check if squad is enabled
if [ -f "$HOME/.claude/.squad_enabled" ]; then
    SQUAD_FILE="$HOME/.claude/SQUAD.md"

    # Check if SQUAD.md exists
    if [ -f "$SQUAD_FILE" ]; then
        echo "🤖 Loading squad orchestration rules from SQUAD.md..."
        cat "$SQUAD_FILE"
    else
        echo "⚠️  Warning: SQUAD.md not found at $SQUAD_FILE"
        echo "Agent orchestration rules may not be properly configured."
    fi
else
    echo "ℹ️  Squad functionality disabled. Use /squad-on to enable agent delegation."
fi
EOF

!chmod +x ~/.claude/hooks/sessionStart.sh

## Post-Deployment

After successful deployment:
- Agents available for specialized tasks
- CLAUDE.md enforces mandatory delegation
- Quality gates active (code-reviewer → code-clarity-manager → unit-test-expert)
- Simplicity enforcement (design-simplicity-advisor) mandatory before implementation
- Squad functionality enabled by default

**🎯 Squad deployed! Claude now delegates to specialist agents automatically.**

Use `/squad-off` to disable agent delegation or `/squad-on` to re-enable it.