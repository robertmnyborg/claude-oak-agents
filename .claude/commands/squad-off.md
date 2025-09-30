---
description: Disable squad functionality and agent delegation
argument-hint:
allowed-tools: Bash(*), Read(*), Write(*)
---

# Squad Off - Disable Agent Delegation

Disable the claude-agents squad functionality to return to direct Claude interaction without agent delegation.

## What Squad Off Does

1. **Removes environment flag** to disable squad functionality
2. **Updates session hook** to skip SQUAD.md loading
3. **Prompts for context clearing** to ensure clean state
4. **Clears context** after user confirmation

## Implementation

Setting squad functionality to DISABLED...

!rm -f ~/.claude/.squad_enabled

Updating session hook to skip SQUAD.md loading...

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

## Context Clearing

**⚠️ IMPORTANT**: To ensure proper squad deactivation, your current context should be cleared.

**Do you want to clear the context now?**

Respond with 'yes' to clear context and deactivate squad functionality, or 'no' to keep current context.

If you choose 'yes', the context will be cleared and you'll interact directly with Claude without agent delegation.

## Squad Disabled Status

❌ **Squad functionality is now DISABLED**

- No agent delegation
- Direct Claude interaction
- SQUAD.md will not load on session start
- Quality gates inactive

Use `/squad-on` to re-enable squad functionality if needed.