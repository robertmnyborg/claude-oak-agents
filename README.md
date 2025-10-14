# Claude Squad Plugin

A comprehensive Claude Code plugin with 29+ specialized agents, mandatory delegation enforcement, and intelligent workflow coordination for software development teams.

## 🚀 Quick Installation

### Step 1: Add Local Marketplace
```bash
# Add this repository as a local marketplace
/plugin marketplace add /path/to/claude-squad-plugin

# Or clone and add:
git clone https://github.com/your-org/claude-squad-plugin.git
/plugin marketplace add ./claude-squad-plugin
```

### Step 2: Install Plugin
```bash
# Install the Claude Squad plugin
/plugin install claude-squad@local

# Restart Claude Code to activate
```

### Step 3: Activate Squad System
```bash
# Enable agent delegation
/squad-on

# Check squad status
/squad-status

# View available agents
/help
```

## 🤖 Agent System

This plugin provides 29 specialized agents with mandatory delegation enforcement:

### 🏗️ Core Development Agents
- **frontend-developer** - UI/UX implementation, React/Vue/Angular, browser compatibility
- **backend-architect** - Database design, API architecture, microservices patterns
- **infrastructure-specialist** - CDK constructs, cloud architecture, deployment strategies
- **mobile-developer** - React Native, iOS, Android development
- **blockchain-developer** - Solidity smart contracts, Web3 integration, DeFi protocols
- **ml-engineer** - Python/TensorFlow, data pipelines, MLOps practices
- **legacy-maintainer** - Java, C#, enterprise systems maintenance and modernization

### 🛡️ Security & Quality Agents
- **security-auditor** - Penetration testing, compliance validation (SOC2, GDPR, PCI DSS)
- **code-reviewer** - Security analysis, code quality, vulnerability detection
- **code-clarity-manager** - Orchestrates maintainability analysis
- **unit-test-expert** - Comprehensive unit test creation and coverage
- **dependency-scanner** - Third-party dependency analysis, vulnerability scanning
- **qa-specialist** - End-to-end testing, integration testing, performance validation

### ⚙️ Operations & Analysis Agents
- **performance-optimizer** - Performance analysis, bottleneck identification
- **systems-architect** - System design, infrastructure planning, technical specifications
- **debug-specialist** - Critical error resolution (highest priority)
- **git-workflow-manager** - Git operations, branch management, PR creation
- **project-manager** - Multi-step project coordination

### 📝 Content & Documentation Agents
- **technical-documentation-writer** - API docs, technical specifications
- **content-writer** - Marketing content, user-facing documentation
- **business-analyst** - Requirements analysis, user stories, stakeholder communication
- **data-scientist** - Data analysis, insights, statistical processing

### 🎯 Specialty Agents
- **design-simplicity-advisor** - KISS principle enforcement (mandatory before implementation)
- **prompt-engineer** - AI prompt optimization and engineering
- **agent-creator** - Design and implement new specialized agents
- **general-purpose** - Basic queries and single-line commands only

## 📋 Available Commands

The plugin includes squad management commands:

- `/squad-deploy` - Deploy and activate the agent system
- `/squad-on` - Enable agent delegation
- `/squad-off` - Disable agent delegation
- `/squad-status` - View current squad status
- `/squad-furlough` - Temporarily disable specific agents
- `/squad-assemble` - Reactivate all agents
- `/squad-dismiss` - Remove specific agents
- `/squad-standdown` - Emergency disable all agents
- `/squad-override` - Bypass delegation for single tasks

## ⚙️ Key Features

### Mandatory Delegation System
- **Zero-bypass enforcement** - Main LLM prohibited from implementation work
- **Domain routing** - Automatic specialist assignment based on context
- **Quality gates** - Code review → testing → simplicity analysis
- **Emergency handling** - Critical errors bypass normal workflow

### Workflow Automation
- **Classification-based routing** - INFORMATION/IMPLEMENTATION/ANALYSIS/COORDINATION
- **Multi-agent coordination** - Parallel and sequential agent workflows
- **Quality enforcement** - Mandatory simplicity advisor before commits
- **Git integration** - Automated workflow state tracking

### Intelligence Features
- **Context detection** - File types, technologies, domain keywords
- **Pattern matching** - Trigger-based agent activation
- **State management** - Workflow progress tracking
- **Error prioritization** - Debug specialist always takes precedence

## 🔧 Plugin Structure

```
claude-squad-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── agents/                  # 29 specialized agent definitions
│   ├── backend-architect.md
│   ├── frontend-developer.md
│   └── ... (27 more)
├── commands/                # Squad management commands
│   ├── squad-deploy.md
│   ├── squad-on.md
│   └── ... (7 more)
├── hooks/                   # Session automation
│   ├── hooks.json
│   └── sessionStart.sh     # Auto-loads squad rules
├── CLAUDE.md               # Delegation enforcement rules
├── marketplace.json        # Distribution configuration
└── README.md              # This file
```

## 🎯 Usage Examples

### Development Workflow
```bash
# User asks to "fix the login API bug"
# System automatically:
# 1. Classifies as IMPLEMENTATION
# 2. Routes to backend-architect (API domain)
# 3. Enforces quality gates
# 4. Creates git commit with proper workflow
```

### Multi-Domain Tasks
```bash
# User asks to "build a secure mobile app with analytics"
# System coordinates:
# 1. security-auditor (security requirements)
# 2. mobile-developer (app implementation)
# 3. data-scientist (analytics design)
# 4. Main LLM synthesizes results
```

## 🚨 Enforcement Rules

### What's Prohibited
- ❌ Main LLM direct programming/coding
- ❌ File modifications without specialist approval
- ❌ Bypassing quality gates
- ❌ Skipping simplicity analysis

### What's Automatic
- ✅ Domain detection and routing
- ✅ Specialist task delegation
- ✅ Quality gate enforcement
- ✅ Workflow state tracking
- ✅ Git integration

## 🔄 Plugin Management

### Update Plugin
```bash
# Update to latest version
/plugin update claude-squad@local
```

### Disable Plugin
```bash
# Temporarily disable
/plugin disable claude-squad

# Re-enable
/plugin enable claude-squad
```

### Uninstall Plugin
```bash
# Remove plugin completely
/plugin uninstall claude-squad
```

## 📖 Documentation

- **Agent Specifications** - See individual `.md` files in `agents/` directory
- **Command Documentation** - See `.md` files in `commands/` directory
- **Workflow Rules** - See `CLAUDE.md` for complete delegation system
- **Plugin API** - See `.claude-plugin/plugin.json` for metadata

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add/modify agents in `agents/` directory
4. Update plugin metadata if needed
5. Test with local marketplace
6. Submit pull request

## 📄 License

MIT License - See LICENSE file for details

---

**🎯 Ready to supercharge your development workflow with intelligent agent delegation? Install Claude Squad today!**