#!/bin/bash

# Claude Code Bootstrap Installation Script
# This script sets up a complete Claude Code configuration with agents and templates

set -e

# Function to merge JSON files using jq
merge_json_files() {
    local existing_file="$1"
    local new_file="$2"
    local target_file="$3"

    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        echo "⚠️  Warning: jq not found, copying without merging"
        cp "$new_file" "$target_file"
        return 1
    fi

    # If existing file doesn't exist, just copy the new one
    if [ ! -f "$existing_file" ]; then
        echo "📄 Creating new configuration file..."
        cp "$new_file" "$target_file"
        return 0
    fi

    # Merge files using jq
    echo "📄 Merging JSON configuration..."
    jq -s '.[0] * .[1]' "$existing_file" "$new_file" > "${target_file}.tmp"
    mv "${target_file}.tmp" "$target_file"
    echo "✅ Configuration merged successfully"
    return 0
}

CLAUDE_DIR="${HOME}/.claude"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Claude Code Bootstrap Installation"
echo "======================================"

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "${CLAUDE_DIR}/agents"
mkdir -p "${CLAUDE_DIR}/disabled_agents"
mkdir -p "${CLAUDE_DIR}/plugins"
mkdir -p "${CLAUDE_DIR}/templates"
mkdir -p "${CLAUDE_DIR}/memory"
mkdir -p "${CLAUDE_DIR}/workflows"
mkdir -p "${CLAUDE_DIR}/integrations"
mkdir -p "${CLAUDE_DIR}/backups"
mkdir -p "${CLAUDE_DIR}/hooks"

# Copy core configuration files (empty state - use /squad-deploy to activate)
echo "⚙️  Installing core configuration..."
if [ -f "${SCRIPT_DIR}/settings.json" ]; then
    merge_json_files "${CLAUDE_DIR}/settings.json" "${SCRIPT_DIR}/settings.json" "${CLAUDE_DIR}/settings.json"
fi

# Note: CLAUDE.md and AGENTS.md are NOT copied by default
# Use /squad-deploy to activate the agent system

# Copy all agents to disabled_agents (not active by default)
echo "🤖 Setting up agent system..."
if [ -d "${SCRIPT_DIR}/agents" ]; then
    cp -r "${SCRIPT_DIR}/agents/"* "${CLAUDE_DIR}/disabled_agents/"
    echo "✅ Agents copied to ~/.claude/disabled_agents (use squad-deploy to activate)"
fi

# Copy templates (including CLAUDE.md for deployment)
echo "📋 Installing project templates..."
if [ -d "${SCRIPT_DIR}/templates" ]; then
    cp -r "${SCRIPT_DIR}/templates/"* "${CLAUDE_DIR}/templates/"
fi

# Copy SQUAD.md orchestration rules
echo "🎯 Installing orchestration rules..."
if [ -f "${SCRIPT_DIR}/.claude/SQUAD.md" ]; then
    cp "${SCRIPT_DIR}/.claude/SQUAD.md" "${CLAUDE_DIR}/SQUAD.md"
    echo "✅ SQUAD.md orchestration rules installed"
fi

# Copy SessionStart hook
if [ -f "${SCRIPT_DIR}/.claude/hooks/sessionStart.sh" ]; then
    cp "${SCRIPT_DIR}/.claude/hooks/sessionStart.sh" "${CLAUDE_DIR}/hooks/"
    chmod +x "${CLAUDE_DIR}/hooks/sessionStart.sh"
    echo "✅ SessionStart hook installed"
fi

# Copy plugins config
echo "🔌 Installing plugin configuration..."
if [ -f "${SCRIPT_DIR}/plugins/config.json" ]; then
    cp "${SCRIPT_DIR}/plugins/config.json" "${CLAUDE_DIR}/plugins/"
fi

# Set up shell environment
echo "🐚 Setting up shell environment..."
if [ -f "${SCRIPT_DIR}/.clauderc" ]; then
    cp "${SCRIPT_DIR}/.clauderc" "${CLAUDE_DIR}/"

    # Add to shell profile if not already present
    SHELL_PROFILE=""
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_PROFILE="${HOME}/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_PROFILE="${HOME}/.bashrc"
    fi

    if [ -n "$SHELL_PROFILE" ] && [ -f "$SHELL_PROFILE" ]; then
        if ! grep -q "source ${CLAUDE_DIR}/.clauderc" "$SHELL_PROFILE"; then
            echo "" >> "$SHELL_PROFILE"
            echo "# Claude Code environment" >> "$SHELL_PROFILE"
            echo "source ${CLAUDE_DIR}/.clauderc" >> "$SHELL_PROFILE"
            echo "✅ Added Claude environment to $SHELL_PROFILE"
        fi
    fi
fi

# Set executable permissions
chmod +x "${CLAUDE_DIR}/install.sh" 2>/dev/null || true
chmod +x "${CLAUDE_DIR}/backup.sh" 2>/dev/null || true
chmod +x "${CLAUDE_DIR}/restore.sh" 2>/dev/null || true

echo ""
echo "✅ Claude Code bootstrap installation complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Restart your terminal or run: source ${CLAUDE_DIR}/.clauderc"
echo "   2. Open Claude Code in any project"
echo "   3. Run '/squad-deploy' to activate the agent system"
echo "   4. Agents will enforce mandatory delegation and quality gates"
echo ""
echo "🤖 Agent System: Ready for deployment (currently inactive)"
echo "   📦 Agents available in ${CLAUDE_DIR}/disabled_agents/"
echo "   📋 Templates available in ${CLAUDE_DIR}/templates/"
echo "   🔧 Backups stored in ${CLAUDE_DIR}/backups/"
echo ""
echo "🎯 Squad Commands (use in Claude Code):"
echo "   /squad-deploy   - Activate agents and delegation system"
echo "   /squad-override - Create local project overrides"
echo "   /squad-dismiss  - Deactivate agents and restore backup"