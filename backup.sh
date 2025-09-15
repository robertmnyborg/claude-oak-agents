#!/bin/bash

# Claude Code Configuration Backup Script
# Creates timestamped backups of your Claude configuration

set -e

CLAUDE_DIR="${HOME}/.claude"
BACKUP_DIR="${HOME}/.claude-backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_PATH="${BACKUP_DIR}/claude_config_${TIMESTAMP}"

echo "💾 Claude Code Configuration Backup"
echo "===================================="

# Check if Claude directory exists
if [ ! -d "$CLAUDE_DIR" ]; then
    echo "❌ Error: Claude directory not found at $CLAUDE_DIR"
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"
mkdir -p "$BACKUP_PATH"

echo "📦 Creating backup at: $BACKUP_PATH"

# Backup core configuration files
echo "⚙️  Backing up core configuration..."
cp "$CLAUDE_DIR/settings.json" "$BACKUP_PATH/" 2>/dev/null || echo "⚠️  settings.json not found"
cp "$CLAUDE_DIR/CLAUDE.md" "$BACKUP_PATH/" 2>/dev/null || echo "⚠️  CLAUDE.md not found"
cp "$CLAUDE_DIR/AGENTS.md" "$BACKUP_PATH/" 2>/dev/null || echo "⚠️  AGENTS.md not found"
cp "$CLAUDE_DIR/.clauderc" "$BACKUP_PATH/" 2>/dev/null || echo "⚠️  .clauderc not found"
cp "$CLAUDE_DIR/.gitignore" "$BACKUP_PATH/" 2>/dev/null || echo "⚠️  .gitignore not found"

# Backup agents directory
if [ -d "$CLAUDE_DIR/agents" ]; then
    echo "🤖 Backing up agents..."
    cp -r "$CLAUDE_DIR/agents" "$BACKUP_PATH/"
else
    echo "⚠️  agents directory not found"
fi

# Backup templates directory
if [ -d "$CLAUDE_DIR/templates" ]; then
    echo "📋 Backing up templates..."
    cp -r "$CLAUDE_DIR/templates" "$BACKUP_PATH/"
else
    echo "⚠️  templates directory not found"
fi

# Backup plugins directory
if [ -d "$CLAUDE_DIR/plugins" ]; then
    echo "🔌 Backing up plugins..."
    cp -r "$CLAUDE_DIR/plugins" "$BACKUP_PATH/"
else
    echo "⚠️  plugins directory not found"
fi

# Backup workflows and integrations if they exist
if [ -d "$CLAUDE_DIR/workflows" ]; then
    echo "🔄 Backing up workflows..."
    cp -r "$CLAUDE_DIR/workflows" "$BACKUP_PATH/"
fi

if [ -d "$CLAUDE_DIR/integrations" ]; then
    echo "🔗 Backing up integrations..."
    cp -r "$CLAUDE_DIR/integrations" "$BACKUP_PATH/"
fi

# Create backup manifest
echo "📄 Creating backup manifest..."
cat > "$BACKUP_PATH/BACKUP_INFO.txt" << EOF
Claude Code Configuration Backup
================================
Backup Date: $(date)
Backup Path: $BACKUP_PATH
Claude Directory: $CLAUDE_DIR
System: $(uname -s) $(uname -r)
User: $(whoami)

Contents:
$(find "$BACKUP_PATH" -type f | sort)
EOF

# Create compressed archive
echo "🗜️  Creating compressed archive..."
cd "$BACKUP_DIR"
tar -czf "claude_config_${TIMESTAMP}.tar.gz" "claude_config_${TIMESTAMP}"
ARCHIVE_SIZE=$(du -h "claude_config_${TIMESTAMP}.tar.gz" | cut -f1)

echo ""
echo "✅ Backup completed successfully!"
echo ""
echo "📁 Backup directory: $BACKUP_PATH"
echo "📦 Compressed archive: $BACKUP_DIR/claude_config_${TIMESTAMP}.tar.gz ($ARCHIVE_SIZE)"
echo ""
echo "🔄 To restore this backup, run:"
echo "   $CLAUDE_DIR/restore.sh $BACKUP_PATH"
echo ""
echo "🧹 To clean old backups (keep last 10):"
echo "   ls -t $BACKUP_DIR/claude_config_*.tar.gz | tail -n +11 | xargs rm -f"