#!/bin/bash

# Claude Code Bootstrap Installation Script
# This script sets up a complete Claude Code configuration with agents and templates

set -e

CLAUDE_DIR="${HOME}/.claude"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Claude Code Bootstrap Installation"
echo "======================================"

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "${CLAUDE_DIR}/agents"
mkdir -p "${CLAUDE_DIR}/plugins"
mkdir -p "${CLAUDE_DIR}/templates"
mkdir -p "${CLAUDE_DIR}/memory"
mkdir -p "${CLAUDE_DIR}/workflows"
mkdir -p "${CLAUDE_DIR}/integrations"

# Copy core configuration files
echo "⚙️  Installing core configuration..."
if [ -f "${SCRIPT_DIR}/settings.json" ]; then
    cp "${SCRIPT_DIR}/settings.json" "${CLAUDE_DIR}/"
fi

if [ -f "${SCRIPT_DIR}/CLAUDE.md" ]; then
    cp "${SCRIPT_DIR}/CLAUDE.md" "${CLAUDE_DIR}/"
fi

if [ -f "${SCRIPT_DIR}/AGENTS.md" ]; then
    cp "${SCRIPT_DIR}/AGENTS.md" "${CLAUDE_DIR}/"
fi

# Copy all agents
echo "🤖 Installing agent system..."
if [ -d "${SCRIPT_DIR}/agents" ]; then
    cp -r "${SCRIPT_DIR}/agents/"* "${CLAUDE_DIR}/agents/"
fi

# Copy templates
echo "📋 Installing project templates..."
if [ -d "${SCRIPT_DIR}/templates" ]; then
    cp -r "${SCRIPT_DIR}/templates/"* "${CLAUDE_DIR}/templates/"
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
echo "   2. Run 'claude --version' to verify installation"
echo "   3. Review ${CLAUDE_DIR}/README.md for usage instructions"
echo "   4. Customize ${CLAUDE_DIR}/CLAUDE.md for your preferences"
echo ""
echo "🤖 Agent System: 21 specialized agents installed"
echo "📋 Templates: Project templates available in ${CLAUDE_DIR}/templates/"
echo "🔧 Backup: Run ${CLAUDE_DIR}/backup.sh to create configuration backups"