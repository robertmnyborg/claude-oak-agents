---
description: Permanently install and activate squad functionality with full infrastructure
argument-hint:
allowed-tools: Bash(*), Read(*), Write(*)
---

# Squad Assemble - Permanent Installation

Permanently install and activate the claude-agents squad functionality with full infrastructure setup.

## What Squad Assemble Does

1. **Creates permanent state file** for persistent activation
2. **Installs session hook** with robust error handling
3. **Verifies infrastructure** and creates missing components
4. **Prompts for context clearing** to ensure clean state
5. **Validates installation** and reports status

## Implementation

Creating permanent squad infrastructure...

!mkdir -p ~/.claude/hooks
!mkdir -p ~/.claude/backups

Setting squad functionality to PERMANENTLY ENABLED...

!echo "CLAUDE_SQUAD_ENABLED=1" > ~/.claude/.squad_enabled
!echo "SQUAD_INSTALL_DATE=$(date)" >> ~/.claude/.squad_enabled
!echo "SQUAD_INSTALL_MODE=permanent" >> ~/.claude/.squad_enabled

Creating robust session hook...

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

## Infrastructure Verification

Verifying squad infrastructure...

!echo "🔍 Infrastructure Check:"
!echo "✅ Session hook: $([ -x ~/.claude/hooks/sessionStart.sh ] && echo 'Installed' || echo 'Missing')"
!echo "✅ State file: $([ -f ~/.claude/.squad_enabled ] && echo 'Created' || echo 'Missing')"
!echo "✅ SQUAD.md: $([ -f ~/.claude/SQUAD.md ] && echo 'Available' || echo 'Missing')"
!echo "✅ Hooks directory: $([ -d ~/.claude/hooks ] && echo 'Ready' || echo 'Missing')"
!echo "✅ Backups directory: $([ -d ~/.claude/backups ] && echo 'Ready' || echo 'Missing')"

## Context Clearing

**⚠️ IMPORTANT**: To ensure proper squad activation, your current context should be cleared.

**Do you want to clear the context now?**

Respond with 'yes' to clear context and activate squad functionality, or 'no' to keep current context.

If you choose 'yes', the context will be cleared and squad functionality will be active in your next interaction.

## Squad Assembled Status

✅ **Squad functionality is now PERMANENTLY ASSEMBLED**

- Agent delegation rules permanently active
- SQUAD.md will load on every session start
- Specialist routing available
- Quality gates enforced
- Infrastructure verified and installed

Use `/squad-dismiss` to completely remove squad functionality if needed.
Use `/squad-standdown` for temporary session-only disable.