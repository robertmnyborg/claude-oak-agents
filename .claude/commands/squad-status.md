---
description: Check current squad functionality status
argument-hint:
allowed-tools: Bash(*)
---

# Squad Status - Check Current State

Check whether squad functionality is currently enabled or disabled.

## Current Squad Status

!# Check for session disable first
!if [ -f "$HOME/.claude/.squad_session_disabled" ]; then
    echo "⏸️ **Squad Status: STANDDOWN (Session Disabled)**"
    echo ""
    echo "- Temporarily disabled for this session only"
    echo "- Permanent installation preserved"
    echo "- Will re-enable in new sessions"
    echo ""
    echo "Use \`/squad-on\` to re-enable for current session"
!elif [ -f "$HOME/.claude/.squad_furlough" ]; then
    echo "🏖️ **Squad Status: FURLOUGH (Orchestrator Disabled)**"
    echo ""
    echo "- Orchestrator disabled (no automatic delegation)"
    echo "- Agents available for direct Task() invocation"
    echo "- Manual specialist access maintained"
    echo ""
    echo "Use \`/squad-on\` to re-enable full orchestration"
!elif [ -f "$HOME/.claude/.squad_enabled" ]; then
    echo "✅ **Squad Status: ENABLED**"
    echo ""
    echo "- Agent delegation active"
    echo "- SQUAD.md loads on session start"
    echo "- Quality gates enforced"
    echo "- Specialist routing available"
    echo ""
    echo "Use \`/squad-off\` or \`/squad-standdown\` to disable"
!else
    echo "❌ **Squad Status: DISABLED**"
    echo ""
    echo "- Direct Claude interaction"
    echo "- No agent delegation"
    echo "- SQUAD.md will not load"
    echo "- Quality gates inactive"
    echo ""
    echo "Use \`/squad-on\` or \`/squad-assemble\` to enable"
!fi

## Available Commands

### Core Commands
- `/squad-assemble` - Permanently install squad functionality
- `/squad-dismiss` - Permanently uninstall squad functionality
- `/squad-on` - Enable squad functionality
- `/squad-off` - Disable squad functionality

### Temporary Commands
- `/squad-standdown` - Temporarily disable for session only
- `/squad-furlough` - Disable orchestrator, keep agents available

### Management Commands
- `/squad-deploy` - Deploy squad infrastructure
- `/squad-status` - Check current status
- `/squad-override` - Override settings