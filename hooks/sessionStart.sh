#!/bin/bash

# Claude Squad Plugin - Session Start Hook
# Loads squad orchestration rules and agent delegation system

# Get the plugin directory path
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Check if squad is enabled (check both global and local)
SQUAD_ENABLED=false

if [ -f "$HOME/.claude/.squad_enabled" ] || [ -f "$PLUGIN_DIR/.squad_enabled" ]; then
    SQUAD_ENABLED=true
fi

if [ "$SQUAD_ENABLED" = true ]; then
    # Look for CLAUDE.md in plugin directory first, then global location
    CLAUDE_FILE=""
    if [ -f "$PLUGIN_DIR/CLAUDE.md" ]; then
        CLAUDE_FILE="$PLUGIN_DIR/CLAUDE.md"
    elif [ -f "$HOME/.claude/CLAUDE.md" ]; then
        CLAUDE_FILE="$HOME/.claude/CLAUDE.md"
    fi

    # Check if CLAUDE.md exists
    if [ -n "$CLAUDE_FILE" ] && [ -f "$CLAUDE_FILE" ]; then
        echo "🤖 Claude Squad Plugin loaded - Agent delegation active"
        echo "📋 Loading orchestration rules from CLAUDE.md..."
        cat "$CLAUDE_FILE"
    else
        echo "⚠️  Warning: CLAUDE.md not found"
        echo "Agent orchestration rules may not be properly configured."
        echo "Plugin directory: $PLUGIN_DIR"
    fi
else
    echo "ℹ️  Claude Squad functionality disabled."
    echo "Use /squad-on to enable agent delegation or install the claude-squad plugin."
fi