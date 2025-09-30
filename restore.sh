#!/bin/bash

# Claude Code Configuration Restore Script
# Restores Claude configuration from backup

set -e

# Function to merge JSON files using jq
merge_json_files() {
    local existing_file="$1"
    local backup_file="$2"
    local target_file="$3"

    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        echo "⚠️  Warning: jq not found, copying without merging"
        cp "$backup_file" "$target_file"
        return 1
    fi

    # If existing file doesn't exist, just copy the backup
    if [ ! -f "$existing_file" ]; then
        echo "📄 Restoring configuration file from backup..."
        cp "$backup_file" "$target_file"
        return 0
    fi

    # Merge files using jq (existing takes precedence for restore)
    echo "📄 Merging existing configuration with backup..."
    jq -s '.[0] * .[1]' "$existing_file" "$backup_file" > "${target_file}.tmp"
    mv "${target_file}.tmp" "$target_file"
    echo "✅ Configuration merged successfully"
    return 0
}

CLAUDE_DIR="${HOME}/.claude"
BACKUP_PATH="$1"

echo "♻️  Claude Code Configuration Restore"
echo "====================================="

# Check if backup path is provided
if [ -z "$BACKUP_PATH" ]; then
    echo "❌ Error: Please provide backup path"
    echo ""
    echo "Usage: $0 <backup_path>"
    echo ""
    echo "Available backups:"
    ls -la "${HOME}/.claude-backups/" 2>/dev/null | grep "claude_config_" || echo "  No backups found"
    exit 1
fi

# Check if backup path exists
if [ ! -d "$BACKUP_PATH" ]; then
    echo "❌ Error: Backup directory not found: $BACKUP_PATH"
    exit 1
fi

# Check if backup info exists
if [ ! -f "$BACKUP_PATH/BACKUP_INFO.txt" ]; then
    echo "⚠️  Warning: BACKUP_INFO.txt not found. This may not be a valid backup."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Show backup info if available
if [ -f "$BACKUP_PATH/BACKUP_INFO.txt" ]; then
    echo "📄 Backup Information:"
    echo "----------------------"
    cat "$BACKUP_PATH/BACKUP_INFO.txt"
    echo "----------------------"
    echo
fi

# Confirm restore
echo "⚠️  This will overwrite your current Claude configuration!"
read -p "Are you sure you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Restore cancelled"
    exit 1
fi

# Create current backup before restore
if [ -d "$CLAUDE_DIR" ]; then
    echo "💾 Creating safety backup of current configuration..."
    SAFETY_BACKUP="${HOME}/.claude-backups/safety_backup_$(date +"%Y%m%d_%H%M%S")"
    mkdir -p "$(dirname "$SAFETY_BACKUP")"
    cp -r "$CLAUDE_DIR" "$SAFETY_BACKUP"
    echo "✅ Safety backup created at: $SAFETY_BACKUP"
fi

# Create Claude directory if it doesn't exist
mkdir -p "$CLAUDE_DIR"

echo "🔄 Restoring configuration..."

# Restore core files
echo "⚙️  Restoring core configuration..."
if [ -f "$BACKUP_PATH/settings.json" ]; then
    merge_json_files "$CLAUDE_DIR/settings.json" "$BACKUP_PATH/settings.json" "$CLAUDE_DIR/settings.json"
else
    echo "⚠️  settings.json not in backup"
fi
cp "$BACKUP_PATH/CLAUDE.md" "$CLAUDE_DIR/" 2>/dev/null || echo "⚠️  CLAUDE.md not in backup"
cp "$BACKUP_PATH/AGENTS.md" "$CLAUDE_DIR/" 2>/dev/null || echo "⚠️  AGENTS.md not in backup"
cp "$BACKUP_PATH/.clauderc" "$CLAUDE_DIR/" 2>/dev/null || echo "⚠️  .clauderc not in backup"
cp "$BACKUP_PATH/.gitignore" "$CLAUDE_DIR/" 2>/dev/null || echo "⚠️  .gitignore not in backup"

# Restore agents
if [ -d "$BACKUP_PATH/agents" ]; then
    echo "🤖 Restoring agents..."
    rm -rf "$CLAUDE_DIR/agents"
    cp -r "$BACKUP_PATH/agents" "$CLAUDE_DIR/"
else
    echo "⚠️  agents directory not in backup"
fi

# Restore templates
if [ -d "$BACKUP_PATH/templates" ]; then
    echo "📋 Restoring templates..."
    rm -rf "$CLAUDE_DIR/templates"
    cp -r "$BACKUP_PATH/templates" "$CLAUDE_DIR/"
else
    echo "⚠️  templates directory not in backup"
fi

# Restore plugins
if [ -d "$BACKUP_PATH/plugins" ]; then
    echo "🔌 Restoring plugins..."
    rm -rf "$CLAUDE_DIR/plugins"
    cp -r "$BACKUP_PATH/plugins" "$CLAUDE_DIR/"
else
    echo "⚠️  plugins directory not in backup"
fi

# Restore workflows if present
if [ -d "$BACKUP_PATH/workflows" ]; then
    echo "🔄 Restoring workflows..."
    rm -rf "$CLAUDE_DIR/workflows"
    cp -r "$BACKUP_PATH/workflows" "$CLAUDE_DIR/"
fi

# Restore integrations if present
if [ -d "$BACKUP_PATH/integrations" ]; then
    echo "🔗 Restoring integrations..."
    rm -rf "$CLAUDE_DIR/integrations"
    cp -r "$BACKUP_PATH/integrations" "$CLAUDE_DIR/"
fi

# Set proper permissions
chmod +x "$CLAUDE_DIR/"*.sh 2>/dev/null || true

echo ""
echo "✅ Configuration restored successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. Restart your terminal or run: source $CLAUDE_DIR/.clauderc"
echo "   2. Run 'claude --version' to verify installation"
echo "   3. Review restored configuration files"
echo ""
echo "💾 Safety backup of previous config: $SAFETY_BACKUP"