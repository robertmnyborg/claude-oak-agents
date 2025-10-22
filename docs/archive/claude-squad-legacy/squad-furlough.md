---
description: Turn off orchestrator while keeping agents available for direct invocation
argument-hint:
allowed-tools: Bash(*), Read(*), Write(*)
---

# Squad Furlough - Disable Orchestrator Only

Disable the orchestrator and automatic delegation while keeping agents available for direct invocation.

## What Squad Furlough Does

1. **Creates furlough state file** to track orchestrator disable
2. **Updates hook to skip orchestration** but preserve agent access
3. **Maintains agent infrastructure** for manual invocation
4. **Prompts for context clearing** to ensure clean state

## Implementation

Creating furlough state (orchestrator disabled, agents available)...

!echo "SQUAD_FURLOUGH=$(date)" > ~/.claude/.squad_furlough
!echo "ORCHESTRATOR_DISABLED=true" >> ~/.claude/.squad_furlough
!echo "AGENTS_AVAILABLE=true" >> ~/.claude/.squad_furlough

Updating session hook for furlough mode...

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

# Check for furlough mode (orchestrator disabled, agents available)
if [ -f "$HOME/.claude/.squad_furlough" ]; then
    echo "🏖️  Squad in furlough mode - Orchestrator disabled, agents available for direct invocation."
    echo "💡 You can still invoke agents directly using Task() calls."
    echo "Use /squad-on to re-enable full orchestration."
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

## Furlough State Check

!echo "🔍 Current State:"
!echo "✅ Permanent state: $([ -f ~/.claude/.squad_enabled ] && echo 'Preserved' || echo 'Not installed')"
!echo "🏖️  Furlough mode: $([ -f ~/.claude/.squad_furlough ] && echo 'Active' || echo 'Inactive')"
!echo "🤖 Agent access: Available for direct Task() invocation"

## Context Clearing

**⚠️ IMPORTANT**: To ensure proper furlough activation, your current context should be cleared.

**Do you want to clear the context now?**

Respond with 'yes' to clear context and activate furlough mode, or 'no' to keep current context.

If you choose 'yes', the context will be cleared and you'll be able to invoke agents directly without automatic orchestration.

## Squad Furlough Status

🏖️ **Squad is now in FURLOUGH MODE**

- Orchestrator disabled (no automatic delegation)
- Agents available for direct Task() invocation
- Manual specialist access maintained
- Quality gates inactive

**Available for direct invocation:**
- Task(agent="infrastructure-specialist", prompt="...")
- Task(agent="frontend-developer", prompt="...")
- Task(agent="backend-architect", prompt="...")
- Task(agent="security-auditor", prompt="...")
- And all other specialist agents

Use `/squad-on` to re-enable full orchestration.
Use `/squad-dismiss` to completely remove squad functionality.