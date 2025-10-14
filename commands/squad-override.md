---
description: Create local overrides for CLAUDE.md or specific agents
argument-hint: [claude|agent] [agent-name]
allowed-tools: Bash(*), Read(*), Write(*), Glob(*)
---

# Squad Override - Local Configuration Override

Create local project overrides for CLAUDE.md or specific agents without affecting global configuration.

## Override Options

**Arguments**: $ARGUMENTS

Available override types:

1. **claude** - Override CLAUDE.md in current project
2. **agent [name]** - Override specific agent in current project

## What Squad Override Does

Creates local `.claude/` configuration that takes precedence over global `~/.claude/` settings:

- **Local CLAUDE.md**: Project-specific rules and delegation patterns
- **Local Agents**: Customized agent behavior for specific project needs
- **Inheritance**: Local overrides global, preserving global as fallback

## Pre-Override Check

Check available templates and agents:

!echo "📦 Available templates:"
!ls -la ~/.claude/templates/ 2>/dev/null || echo "❌ No templates found"

!echo "📦 Available agents for override:"
!ls ~/.claude/disabled_agents/ 2>/dev/null | sed 's/\.md$//' | head -10 || echo "❌ No agents found"

## Override Type Analysis

Parse arguments to determine override type:

**Override Type**: $ARGUMENTS

- If contains "claude" → CLAUDE.md override
- If contains "agent" → Agent override (requires agent name)
- If no arguments → Show help and available options

## CLAUDE.md Override Process

If overriding CLAUDE.md:

1. Check if local `.claude/CLAUDE.md` already exists
2. Warn about overwrite if present
3. Copy `~/.claude/templates/CLAUDE.md` to `./claude/CLAUDE.md`
4. Confirm local override created

## Agent Override Process

If overriding specific agent:

1. Validate agent name exists in `~/.claude/disabled_agents/`
2. Create local `./claude/agents/` directory if needed
3. Copy specified agent from disabled_agents to local agents
4. Confirm agent override created

## Post-Override

After successful override:
- Local configuration takes precedence
- Original global configuration remains intact
- Can revert by removing local `.claude/` directory
- Use `/squad-dismiss --local` to remove local overrides

**🎯 Local override created! Project now uses custom configuration.**