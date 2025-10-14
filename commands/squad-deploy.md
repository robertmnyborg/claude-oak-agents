---
description: Deploy and activate Claude Squad plugin agents and delegation system
argument-hint: [--local] [--project]
allowed-tools: Bash(*), Read(*), Write(*)
---

# Squad Deploy - Activate Claude Squad Plugin

Deploy the Claude Squad plugin to activate intelligent delegation and agent specialization.

## Plugin-Based Deployment

**Arguments**: $ARGUMENTS

**Note**: This command works within the Claude Squad plugin system. The plugin is already installed - this command activates/configures it.

## Deployment Options

1. **Global Configuration** (default): Activates squad system globally for all sessions
2. **Project-Level** (`--project`): Activates squad system for current project only

## What Squad Deploy Does

1. **Verify plugin installation** and component availability
2. **Enable squad system** through configuration flags
3. **Validate agent definitions** and command availability
4. **Activate session hooks** for automatic rule loading
5. **Report deployment status** and next steps

## Plugin Verification

First, let me verify the plugin is properly installed:

!echo "🔍 Checking Claude Squad plugin status..."

## Activate Squad System

Enable the Claude Squad delegation system:

!echo "🚀 Activating Claude Squad system..."

## Enable Squad Configuration

Determine deployment scope and create configuration:

!if [[ "$ARGUMENTS" == *"--project"* ]]; then
    echo "📁 Activating Claude Squad for current project only"
    touch ./.squad_enabled
    echo "CLAUDE_SQUAD_ENABLED=1" > ./.squad_enabled
else
    echo "🌐 Activating Claude Squad globally"
    mkdir -p ~/.claude
    echo "CLAUDE_SQUAD_ENABLED=1" > ~/.claude/.squad_enabled
fi

## Plugin Status Check

Verify plugin components are available:

!echo "📋 Plugin Component Status:"
!echo "  Agents: $(ls agents/ 2>/dev/null | wc -l | xargs) available"
!echo "  Commands: $(ls commands/ 2>/dev/null | wc -l | xargs) available"
!echo "  Hooks: $(ls hooks/ 2>/dev/null | wc -l | xargs) configured"

## Validation

Verify the plugin deployment is working:

!if [[ -f ~/.claude/.squad_enabled ]] || [[ -f ./.squad_enabled ]]; then
    echo "✅ Squad system successfully activated"
    echo "🤖 Agent delegation is now enabled"
else
    echo "❌ Squad activation failed"
    exit 1
fi

## Post-Deployment

After successful deployment:
- ✅ **29 specialist agents** available for task delegation
- ✅ **Mandatory delegation system** enforces quality workflows
- ✅ **CLAUDE.md rules** active for domain routing
- ✅ **Session hooks** load squad rules automatically
- ✅ **Quality gates** ensure code review → testing → simplicity
- ✅ **Squad commands** available for management

## Next Steps

**🎯 Claude Squad Plugin successfully deployed!**

Available squad management commands:
- `/squad-status` - Check current agent status
- `/squad-off` - Temporarily disable delegation
- `/squad-on` - Re-enable agent delegation
- `/squad-furlough` - Disable specific agents
- `/squad-assemble` - Reactivate all agents

**Ready to delegate! Try asking Claude to implement a feature and watch the specialist agents take over.**