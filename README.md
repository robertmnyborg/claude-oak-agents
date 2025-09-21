# Claude Code Bootstrap Configuration

A comprehensive Claude Code setup with specialized agents, mandatory delegation enforcement, and direct main LLM coordination.

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

This configuration includes specialized agents with mandatory delegation enforcement that prevents main LLM bypass:

### 🏗️ Core Development Agents
- **frontend-developer** - UI/UX implementation, React/Vue/Angular, browser compatibility
- **backend-architect** - Database design, API architecture, microservices patterns
- **programmer** - Core programming with language hierarchy (Go > TypeScript > Bash > Ruby)
- **qa-specialist** - End-to-end testing, integration testing, performance validation
- **business-analyst** - Requirements analysis, user stories, stakeholder communication
- **content-writer** - Technical documentation, marketing content, API documentation

### 🔬 Specialist Programming Agents
- **ml-engineer** - Python/TensorFlow, data pipelines, MLOps practices
- **blockchain-developer** - Solidity smart contracts, Web3 integration, DeFi protocols
- **mobile-developer** - React Native, iOS, Android development
- **legacy-maintainer** - Java, C#, enterprise systems maintenance and modernization

### 🛡️ Security & Quality Agents
- **security-auditor** - Enhanced penetration testing, compliance validation (SOC2, GDPR, PCI DSS)
- **code-reviewer** - Security analysis, code quality, vulnerability detection
- **code-clarity-manager** - Orchestrates maintainability analysis
- **top-down-analyzer** - Architectural clarity analysis (invoked by code-clarity-manager)
- **bottom-up-analyzer** - Implementation-level clarity analysis (invoked by code-clarity-manager)
- **unit-test-expert** - Comprehensive unit test creation and coverage

### ⚙️ Infrastructure & Operations Agents
- **infrastructure-specialist** - CDK constructs, cloud architecture, deployment strategies
- **systems-architect** - System design, infrastructure planning, technical specifications
- **performance-optimizer** - Performance analysis, bottleneck identification, optimization
- **dependency-scanner** - Third-party dependency analysis, vulnerability scanning
- **debug-specialist** - Critical error resolution (highest priority, blocks all other agents)

### 📋 Workflow & Management Agents
- **git-workflow-manager** - Git operations, branch management, PR creation
- **changelog-recorder** - Automatic changelog generation
- **project-manager** - Multi-step project coordination
- **data-scientist** - Data analysis, insights, statistical processing

### 🔧 Configuration Agents
- **statusline-setup** - Claude Code status line configuration
- **output-style-setup** - Claude Code output style customization

### 🤖 Meta Agents
- **agent-creator** - Design and implement new specialized agents, update coordination patterns

## 📁 Directory Structure

```
~/.claude/
├── 📄 Core Configuration
│   ├── CLAUDE.md              # Personal development rules
│   ├── AGENTS.md              # Agent system documentation
│   ├── settings.json          # Main Claude configuration
│   └── .clauderc              # Shell environment setup
├── 🤖 Agent System
│   └── agents/                # Specialized agents with delegation enforcement
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

### Delegation Enforcement System
- **Mandatory delegation** - Main LLM prohibited from programming work
- **Enhanced contextual routing** - Priority-based agent selection with test-specific pattern recognition
- **Bypass prevention** - 5-layer enforcement prevents main LLM technical work
- **Intelligent routing** - Project context and compound phrases determine specialist agent selection

### Direct Coordination Architecture
- **Direct main LLM coordination** - Main LLM coordinates all agent workflows directly
- **Solved re-entrant state problem** - Main LLM maintains consistent workflow state
- **Efficient delegation** - Direct coordination with specialized agents
- **Quality gates** - Sequential validation (code-reviewer → code-clarity-manager → testing)

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
Personal development rules and delegation enforcement. Defines:
- Mandatory delegation triggers and enforcement mechanisms
- Technology stack preferences and language hierarchy
- Agent routing rules and specialist selection
- Communication style and workflow coordination

### AGENTS.md
Complete agent system architecture documentation including:
- Specialized agents with delegation enforcement
- Trigger-based routing and direct main LLM coordination
- Quality gates and sequential validation
- Specialist selection and project-specific routing

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

- **Delegation enforcement active** - Main LLM cannot perform programming tasks
- **Enhanced contextual routing** - Test-specific patterns route to appropriate testing specialists
- **Quality gates mandatory** - Sequential validation prevents low-quality commits
- **Specialist routing** - Project context and compound phrases determine optimal agent selection
- **Test routing fixed** - "Fix tests" now correctly routes to qa-specialist instead of programmer
- **Automatic backups recommended** before major changes

## 🆘 Support

For Claude Code issues: https://github.com/anthropics/claude-code/issues

For configuration help:
1. Run `claude-status` to diagnose issues
2. Check `~/.claude/SETUP.md` for detailed instructions
3. Use `claude-backup` before making changes