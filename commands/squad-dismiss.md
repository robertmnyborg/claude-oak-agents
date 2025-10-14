---
description: Dismiss squad agents and restore backup configuration
argument-hint: [--local] [--global] [--keep-config]
allowed-tools: Bash(*), Read(*), Write(*), Glob(*)
---

# Squad Dismiss - Deactivate Agent System

Dismiss the claude-agents squad and restore previous configuration state.

## Dismissal Options

**Arguments**: $ARGUMENTS

Available dismissal modes:

1. **Global Dismissal** (default): Remove from `~/.claude/`
2. **Local Dismissal** (`--local`): Remove from current project's `.claude/`
3. **Keep Config** (`--keep-config`): Remove agents but preserve CLAUDE.md

## What Squad Dismiss Does

Safely removes agent configuration and restores backup state:

1. **Remove active agents** directory
2. **Restore backup CLAUDE.md** (unless `--keep-config`)
3. **Preserve disabled_agents** for future deployment
4. **Clean up temporary files**

## Pre-Dismissal Check

Check current deployment status:

!echo "🔍 Current agent deployment status:"
!ls -la ~/.claude/agents/ 2>/dev/null || echo "ℹ️  No global agents deployed"
!ls -la ./.claude/agents/ 2>/dev/null || echo "ℹ️  No local agents deployed"

!echo "📦 Available backups:"
!ls -la ~/.claude/backups/ 2>/dev/null | head -5 || echo "ℹ️  No backups found"

## Dismissal Target Analysis

Parse arguments to determine dismissal scope:

**Dismissal Mode**: $ARGUMENTS

- Contains `--local` → Remove local project agents only
- Contains `--global` → Remove global agents only
- Contains `--keep-config` → Preserve CLAUDE.md configuration
- No arguments → Default global dismissal

## Agent Removal Process

Remove agents based on target:

1. **Identify target directory** (global `~/.claude/` or local `./.claude/`)
2. **Backup current state** before removal
3. **Remove agents directory** completely
4. **Report removal status**

## Configuration Restoration

Unless `--keep-config` is specified:

1. **Find most recent backup** CLAUDE.md
2. **Restore backup** to target location
3. **Report restoration status**

If `--keep-config`:
- Keep existing CLAUDE.md intact
- Only remove agents directory

## Post-Dismissal State

After successful dismissal:
- Agents no longer available for delegation
- Claude returns to standard operation mode
- Original configuration restored (if backup available)
- Disabled agents remain available for future deployment

## Cleanup

Remove any temporary files and verify clean dismissal:

!echo "✅ Squad dismissal verification:"
!ls -la ~/.claude/agents/ 2>/dev/null || echo "✅ Global agents removed"
!ls -la ./.claude/agents/ 2>/dev/null || echo "✅ Local agents removed"

**🎯 Squad dismissed! Claude returned to standard operation mode.**