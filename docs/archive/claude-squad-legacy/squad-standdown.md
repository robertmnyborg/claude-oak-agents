---
description: Temporarily disable squad for current session only (preserves permanent state)
argument-hint:
allowed-tools: Bash(*), Read(*), Write(*)
---

# Squad Standdown - Temporary Session Disable

Temporarily disable squad functionality for the current session only, without affecting permanent installation.

## What Squad Standdown Does

1. **Creates session-only disable flag** (preserves permanent state)
2. **Updates hook for current session** to skip SQUAD.md loading
3. **Preserves permanent installation** for future sessions
4. **Prompts for context clearing** to ensure clean state

## Implementation

Creating temporary session disable...

!echo "SESSION_DISABLE=$(date)" > ~/.claude/.squad_session_disabled

Updating session hook for temporary disable...

!cat > ~/.claude/hooks/sessionStart.sh << 'EOF'
#!/bin/bash

# SessionStart hook to load SQUAD.md orchestration rules
# This hook runs at the beginning of each session and after /clear

# Check for session-only disable first
if [ -f "$HOME/.claude/.squad_session_disabled" ]; then
    echo "⏸️  Squad temporarily disabled for this session."
    echo "Use /squad-on to re-enable for this session."
    exit 0
fi

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

## Session State Check

!echo "🔍 Current State:"
!echo "✅ Permanent state: $([ -f ~/.claude/.squad_enabled ] && echo 'Preserved' || echo 'Not installed')"
!echo "⏸️  Session disable: $([ -f ~/.claude/.squad_session_disabled ] && echo 'Active' || echo 'Inactive')"

## Context Clearing

**⚠️ IMPORTANT**: To ensure proper squad standdown, your current context should be cleared.

**Do you want to clear the context now?**

Respond with 'yes' to clear context and deactivate squad for this session, or 'no' to keep current context.

If you choose 'yes', the context will be cleared and you'll interact directly with Claude without agent delegation for this session only.

## Squad Standdown Status

⏸️ **Squad functionality is now in STANDDOWN (session-only)**

- No agent delegation for this session
- Direct Claude interaction until next session
- Permanent installation preserved
- Will automatically re-enable in new sessions

Use `/squad-on` to re-enable for current session.
Use `/squad-dismiss` to permanently remove squad functionality.