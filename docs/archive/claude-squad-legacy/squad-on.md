---
description: Enable Claude Squad plugin agent delegation and orchestration system
argument-hint:
allowed-tools: Bash(*)
---

# Squad On - Enable Agent Delegation

Enable the Claude Squad plugin functionality to activate intelligent delegation and agent specialization.

## What Squad On Does

1. **Enables squad system** through configuration flags
2. **Clears temporary disable states** from previous sessions
3. **Activates plugin hooks** for automatic rule loading
4. **Reports activation status** and available agents

## Plugin Activation

Setting Claude Squad plugin to ENABLED...

!# Clear any temporary disable states
!rm -f ~/.claude/.squad_session_disabled
!rm -f ./.squad_session_disabled
!rm -f ~/.claude/.squad_furlough
!rm -f ./.squad_furlough

!# Enable squad globally or locally based on existing configuration
!if [[ -f ./.squad_enabled ]]; then
    echo "📁 Enabling Claude Squad for current project"
    echo "CLAUDE_SQUAD_ENABLED=1" > ./.squad_enabled
else
    echo "🌐 Enabling Claude Squad globally"
    mkdir -p ~/.claude
    echo "CLAUDE_SQUAD_ENABLED=1" > ~/.claude/.squad_enabled
fi

Plugin status check:

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

**⚠️ IMPORTANT**: To ensure proper squad activation, your current context should be cleared.

**Do you want to clear the context now?**

Respond with 'yes' to clear context and activate squad functionality, or 'no' to keep current context.

If you choose 'yes', the context will be cleared and squad functionality will be active in your next interaction.

## Squad Enabled Status

✅ **Squad functionality is now ENABLED**

- Agent delegation rules active
- SQUAD.md will load on session start
- Specialist routing available
- Quality gates enforced

Use `/squad-off` to disable squad functionality if needed.