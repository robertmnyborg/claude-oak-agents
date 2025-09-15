# Claude Code Setup Guide

Detailed installation and configuration instructions for the Claude Code bootstrap system.

## 📋 Prerequisites

- Claude Code CLI installed and configured
- Shell environment (bash, zsh, or compatible)
- Git (recommended for version control)
- Text editor (for configuration customization)

## 🚀 Installation Methods

### Method 1: Bootstrap Installation

If you have the bootstrap files:

```bash
# Run the installation script
cd ~/.claude
./install.sh

# Restart terminal or reload shell
source ~/.claude/.clauderc
```

### Method 2: Manual Installation

1. **Create directory structure:**
```bash
mkdir -p ~/.claude/{agents,plugins,templates,memory,workflows,integrations}
```

2. **Copy configuration files:**
```bash
# Copy all .md files to ~/.claude/
# Copy settings.json to ~/.claude/
# Copy agents/*.md to ~/.claude/agents/
# Copy templates/* to ~/.claude/templates/
```

3. **Set up shell environment:**
```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
echo 'source ~/.claude/.clauderc' >> ~/.zshrc  # or ~/.bashrc
```

4. **Make scripts executable:**
```bash
chmod +x ~/.claude/{install,backup,restore}.sh
```

## ⚙️ Configuration

### Core Settings

Edit `~/.claude/settings.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "agents": {
    "enabled": true,
    "orchestrator": {
      "enabled": true,
      "autoInvoke": true,
      "triggers": ["all_requests"]
    },
    "defaultModel": "sonnet",
    "timeout": 60000
  },
  "permissions": {
    "allow": [
      "Bash(*)",
      "Read(*)",
      "Write(*)",
      "Edit(*)",
      "Glob(*)",
      "Grep(*)",
      "TodoWrite(*)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_AGENTS": "1",
    "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet"
  }
}
```

### Personal Rules

Customize `~/.claude/CLAUDE.md` for your preferences:

```markdown
# Rules for Development Process

⚠️ MANDATORY WORKFLOW ⚠️
EVERY user request must begin with:
Task(subagent_type="agent-orchestrator", prompt="Plan workflow for: [user's request]")

## Technology Stack Constraints
- **Languages**: [Your preferred languages]
- **Framework**: [Your preferred frameworks]
- **Architecture**: [Your architectural preferences]

## Communication Style
- [Your communication preferences]

## Project Standards
- [Your project requirements]
```

### Agent Configuration

The agent system is pre-configured with 21 specialized agents. To customize:

1. **Review agent capabilities** in `~/.claude/AGENTS.md`
2. **Modify agent priorities** by editing agent files in `~/.claude/agents/`
3. **Create custom agents** using the agent-creator system

## 🔧 Shell Integration

### Environment Variables

The `.clauderc` file sets up:

```bash
export CLAUDE_CODE_ENABLE_AGENTS=1
export CLAUDE_CODE_SUBAGENT_MODEL=sonnet
export CLAUDE_CONFIG_DIR="${HOME}/.claude"
```

### Available Commands

After setup, you'll have these commands:

```bash
# Status and information
claude-status          # Show configuration status
claude-agents          # List available agents
claude-config [file]   # Edit configuration files

# Project management
claude-new-project <name>  # Create project with templates

# Backup and maintenance
claude-backup          # Create configuration backup
claude-restore <path>  # Restore from backup
```

### Shell Auto-completion

Bash users get auto-completion for `claude-config`:

```bash
claude-config <TAB>  # Shows: settings.json, CLAUDE.md, AGENTS.md
```

## 📋 Project Templates

### Template Files

The system includes templates for new projects:

- `templates/CLAUDE.md` - Project-specific Claude rules
- `templates/SPEC.md` - Project specification template
- `templates/README.md` - Project README template
- `templates/.gitignore` - Project gitignore template

### Using Templates

```bash
# Create new project with templates
claude-new-project my-awesome-project

# Manually copy templates
cp ~/.claude/templates/CLAUDE.md ./
cp ~/.claude/templates/SPEC.md ./
cp ~/.claude/templates/README.md ./
```

### Customizing Templates

Edit files in `~/.claude/templates/` to match your project standards.

## 🤖 Agent System Configuration

### Orchestrator Settings

The agent-orchestrator is configured to:
- **Auto-invoke** on all requests
- **Maximize parallelism** when possible
- **Enforce quality gates** for code changes
- **Auto-create agents** for capability gaps

### Agent Priorities

```
1. HIGHEST: debug-specialist (blocks all others)
2. HIGH: code-reviewer (quality gate)
3. MEDIUM: code-clarity-manager, unit-test-expert
4. LOW: workflow and documentation agents
5. UTILITY: configuration agents (non-blocking)
```

### Quality Gates

Sequential dependencies enforced:
1. **Security Gate**: code-reviewer must pass
2. **Maintainability Gate**: code-clarity-manager must pass
3. **Test Gate**: unit-test-expert must pass
4. **Documentation**: technical-documentation-writer (advisory)

## 💾 Backup and Recovery

### Automatic Backups

Create regular backups:

```bash
# Create timestamped backup
claude-backup

# List available backups
ls ~/.claude-backups/

# Clean old backups (keep last 10)
ls -t ~/.claude-backups/claude_config_*.tar.gz | tail -n +11 | xargs rm -f
```

### Recovery Process

```bash
# List available backups
ls ~/.claude-backups/

# Restore specific backup
claude-restore ~/.claude-backups/claude_config_20240315_143022

# The restore process:
# 1. Creates safety backup of current config
# 2. Restores selected backup
# 3. Preserves safety backup for rollback
```

## 🔍 Troubleshooting

### Common Issues

**Agent system not working:**
```bash
# Check agent status
claude-agents

# Verify settings
claude-config settings.json

# Check permissions in settings.json
```

**Shell commands not available:**
```bash
# Ensure .clauderc is sourced
source ~/.claude/.clauderc

# Check if added to shell profile
grep "clauderc" ~/.zshrc  # or ~/.bashrc
```

**Template creation fails:**
```bash
# Check templates directory
ls -la ~/.claude/templates/

# Verify permissions
chmod 644 ~/.claude/templates/*
```

### Reset Configuration

To start fresh:

```bash
# Backup current config
claude-backup

# Remove configuration
rm -rf ~/.claude

# Reinstall
./install.sh
```

## 🔧 Advanced Configuration

### Custom Agent Creation

The agent-creator can build new agents automatically, or you can create manually:

```bash
# Edit new agent file
claude-config agents/my-custom-agent.md

# Add agent capabilities and integration points
# The orchestrator will automatically detect and use it
```

### Plugin Configuration

Configure external tools in `~/.claude/plugins/config.json`:

```json
{
  "repositories": {
    "my-repo": {
      "path": "/path/to/repo",
      "config": {
        "linting": true,
        "testing": true
      }
    }
  }
}
```

### Memory Configuration

Agent persistent memory settings in `settings.json`:

```json
{
  "memory": {
    "enabled": true,
    "maxSize": "100MB",
    "retention": "30d"
  }
}
```

## 📊 Monitoring and Maintenance

### Regular Maintenance

```bash
# Weekly backup
claude-backup

# Check agent system health
claude-agents

# Review configuration changes
git log --oneline ~/.claude/  # if using git
```

### Performance Optimization

- Monitor agent execution times
- Adjust timeout values in settings.json
- Clean old backup files regularly
- Review and update agent priorities

## 🆘 Getting Help

1. **Check status**: `claude-status`
2. **Review documentation**: Files in `~/.claude/`
3. **Create issue**: https://github.com/anthropics/claude-code/issues
4. **Backup before changes**: `claude-backup`

## 📚 Next Steps

1. **Customize CLAUDE.md** with your development preferences
2. **Create project templates** that match your workflow
3. **Set up regular backups** (cron job or manual)
4. **Explore agent capabilities** and customize as needed
5. **Integrate with your IDE** and development tools