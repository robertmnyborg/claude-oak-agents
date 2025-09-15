# Claude Code Bootstrap Configuration

A comprehensive Claude Code setup with 21 specialized agents, development workflow automation, and project management tools.

## 🚀 Quick Start

```bash
# Source the environment (add to your shell profile)
source ~/.claude/.clauderc

# Check status
claude-status

# View available agents
claude-agents

# Create a new project with templates
claude-new-project my-awesome-project

# Create configuration backup
claude-backup
```

## 🤖 Agent System

This configuration includes **21 specialized agents** that handle every aspect of development:

### Core Workflow Agents
- **agent-orchestrator** - Coordinates all agent workflows with maximum parallelism
- **code-reviewer** - Security analysis, code quality, vulnerability detection
- **debug-specialist** - Critical error resolution (highest priority)

### Code Quality & Analysis
- **code-clarity-manager** - Orchestrates maintainability analysis
- **top-down-analyzer** - Architectural clarity analysis
- **bottom-up-analyzer** - Implementation-level clarity analysis
- **unit-test-expert** - Comprehensive test creation and coverage
- **performance-optimizer** - Performance analysis and optimization

### Development Workflow
- **git-workflow-manager** - Git operations, branch management, PR creation
- **changelog-recorder** - Automatic changelog generation
- **project-manager** - Multi-step project coordination

### Architecture & Infrastructure
- **systems-architect** - System design and technical specifications
- **infrastructure-specialist** - CDK constructs, cloud architecture
- **dependency-scanner** - Security scanning of third-party dependencies

### Security & Compliance
- **security-auditor** - Security analysis and compliance checking

### Documentation & Communication
- **technical-documentation-writer** - API docs and technical writing

### Specialized Analysis
- **data-scientist** - Data processing and analytical insights

### Configuration & Setup
- **statusline-setup** - Claude Code status line configuration
- **output-style-setup** - Claude Code output customization

### Meta System
- **agent-creator** - Automatically creates new specialized agents when gaps are detected

## 📁 Directory Structure

```
~/.claude/
├── 📄 Core Configuration
│   ├── CLAUDE.md              # Personal development rules
│   ├── AGENTS.md              # Agent system documentation
│   ├── settings.json          # Main Claude configuration
│   └── .clauderc              # Shell environment setup
├── 🤖 Agent System
│   └── agents/                # 21 specialized agents
├── 📋 Project Templates
│   └── templates/             # CLAUDE.md, SPEC.md, README.md templates
├── 🔧 Utilities
│   ├── install.sh             # Bootstrap installer
│   ├── backup.sh              # Configuration backup
│   └── restore.sh             # Configuration restore
├── 🔌 Extensions
│   ├── plugins/               # Plugin configurations
│   ├── workflows/             # Predefined workflows
│   └── integrations/          # Third-party integrations
└── 📊 Runtime Data
    ├── projects/              # Project-specific data
    ├── todos/                 # Task tracking
    └── memory/                # Agent persistent memory
```

## ⚙️ Key Features

### Automated Workflow Management
- **Mandatory orchestrator** for every request ensures optimal agent coordination
- **Maximum parallelism** - agents run concurrently when possible
- **Quality gates** - security and maintainability checks before commits
- **Auto-creation** - new agents created automatically for specialized needs

### Development Standards
- **Technology constraints** - Go > TypeScript > Bash > Ruby preference
- **Functional programming** - avoid classes except for CDK constructs
- **CDK-first architecture** - distributed functions and static assets
- **Project standards** - required README.md, SPEC.md, CLAUDE.md files

### Configuration Management
- **Backup/restore** system for configuration safety
- **Template system** for consistent project setup
- **Environment integration** with shell aliases and functions
- **Version tracking** and change management

## 🔧 Available Commands

### Core Commands
```bash
claude-status          # Show Claude configuration status
claude-agents          # List all available agents
claude-config [file]   # Edit configuration files
```

### Project Management
```bash
claude-new-project <name>  # Create project with templates
```

### Backup & Restore
```bash
claude-backup          # Create timestamped backup
claude-restore <path>  # Restore from backup
```

## 📝 Configuration Files

### CLAUDE.md
Personal development rules and technology constraints. Defines:
- Mandatory agent-orchestrator workflow
- Technology stack preferences
- Class usage guidelines
- Communication style preferences

### AGENTS.md
Complete agent system architecture documentation including:
- Agent capabilities and specializations
- Workflow coordination patterns
- Quality gates and dependencies
- Auto-creation system

### settings.json
Main Claude Code configuration with:
- Agent system enablement
- Permission settings
- Environment variables
- Model preferences

## 🛡️ Security Features

- **Dependency scanning** for third-party vulnerabilities
- **Security auditing** throughout development workflow
- **Credential protection** via .gitignore patterns
- **Code quality gates** prevent vulnerable code commits

## 📚 Documentation

- **README.md** - This overview and quick start guide
- **SETUP.md** - Detailed installation and configuration
- **AGENTS.md** - Complete agent system documentation
- **CHANGELOG.md** - Configuration version history

## 🔄 Workflow Examples

### Code Change Workflow
1. **Security Review** - code-reviewer analyzes for vulnerabilities
2. **Maintainability** - code-clarity-manager ensures readable code
3. **Testing** - unit-test-expert creates comprehensive tests
4. **Documentation** - technical-documentation-writer updates docs
5. **Git Operations** - git-workflow-manager handles commits and PRs

### New Feature Workflow
1. **Planning** - project-manager + systems-architect coordinate
2. **Implementation** - follows code change workflow
3. **Infrastructure** - infrastructure-specialist handles deployment
4. **Monitoring** - performance-optimizer ensures efficiency

## 🚨 Important Notes

- **Every request must start with agent-orchestrator** - no exceptions
- **One task in progress** - agents coordinate to avoid conflicts
- **Quality gates enforced** - failing security/quality blocks commits
- **Automatic backups recommended** before major changes

## 🆘 Support

For Claude Code issues: https://github.com/anthropics/claude-code/issues

For configuration help:
1. Run `claude-status` to diagnose issues
2. Check `~/.claude/SETUP.md` for detailed instructions
3. Use `claude-backup` before making changes