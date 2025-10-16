# Claude OaK Agents

**Self-Improving Agent System for Claude Code**

A comprehensive agent ecosystem with **29+ specialized agents** that **learns from experience**, **fills capability gaps automatically**, and **optimizes itself with 80-95% automation**.

Built on [claude-squad](https://github.com/jamsajones/claude-squad) with **OaK Architecture** (Options and Knowledge) for data-driven continuous improvement.

---

## 🎯 What Makes This Different?

| Feature | Basic Agents | Claude OaK Agents |
|---------|--------------|-------------------|
| Specialized agents | ✅ 29 agents | ✅ 29+ agents (grows automatically) |
| Performance tracking | ❌ None | ✅ Comprehensive telemetry |
| Learning from experience | ❌ Static | ✅ Continuous improvement |
| Capability gap detection | ❌ Manual | ✅ Automatic creation |
| Agent optimization | ❌ Manual refactoring | ✅ A/B testing + ML |
| Portfolio management | ❌ None | ✅ Strategic HR (agent-auditor) |
| Maintenance | ❌ Continuous manual | ✅ 15 min/week automated |

**TL;DR**: Agents that get smarter the more you use them, automatically adapt to your needs, and manage themselves.

---

## 🚀 Quick Install (5 Minutes)

### Prerequisites

- **Claude Code** installed and working
- **macOS** (automation scripts use macOS features)
- **Python 3.8+** (usually pre-installed on macOS)
- **Git** for cloning repository

### Installation

```bash
# 1. Clone to your Projects directory
git clone https://github.com/your-org/claude-oak-agents.git ~/Projects/claude-oak-agents
cd ~/Projects/claude-oak-agents

# 2. Install agents (creates symlinks - won't overwrite existing)
mkdir -p ~/.claude/agents
ln -s ~/Projects/claude-oak-agents/agents/* ~/.claude/agents/

# 3. Install automation (optional but recommended)
./automation/install_automation.sh
# This adds shell prompts and scheduled reviews

# 4. You're done! Start using agents normally in Claude Code
```

**That's it!** The system is now:
- ✅ Logging every agent invocation automatically
- ✅ Tracking performance metrics
- ✅ Detecting capability gaps
- ✅ Prompting you when reviews are due

---

## 💡 How It Works

### For You (Simple)

```
1. Use Claude Code normally → Agents handle tasks
2. System learns automatically → Telemetry captures performance
3. Get prompts when reviews are due → "15 new invocations, 5 min review"
4. Review insights → See what's working, what's not
5. System improves automatically → Agents get better over time
```

### Under the Hood (Smart)

```
Your Request
    ↓
Agent Delegation (with gap detection)
    ↓
Telemetry Capture (automatic)
    ↓
Performance Analysis (scheduled: weekly/monthly)
    ↓
Gap Detection & Agent Creation (automatic with your approval)
    ↓
A/B Testing & Improvement (Phase 5)
    ↓
ML-Driven Optimization (Phase 6)
    ↓
Improved Delegation (smarter over time)
```

---

## 🤖 29+ Specialized Agents

### Core Development (7 agents)
- **frontend-developer** - React/Vue/Angular, UI/UX, browser compatibility
- **backend-architect** - APIs, databases, microservices, system design
- **infrastructure-specialist** - AWS CDK, Terraform, cloud deployment
- **mobile-developer** - React Native, iOS, Android
- **blockchain-developer** - Solidity, Web3, DeFi protocols
- **ml-engineer** - TensorFlow/PyTorch, ML pipelines, MLOps
- **legacy-maintainer** - Java, C#, enterprise systems

### Quality & Security (5 agents)
- **security-auditor** - Penetration testing, compliance, threat modeling
- **code-reviewer** - Quality gates, standards enforcement
- **unit-test-expert** - Comprehensive testing, edge cases
- **dependency-scanner** - Supply chain security, vulnerabilities
- **qa-specialist** - Integration testing, E2E validation

### Infrastructure & Operations (4 agents)
- **systems-architect** - High-level design, technical specs
- **performance-optimizer** - Bottleneck identification, optimization
- **debug-specialist** - Critical error resolution (HIGHEST PRIORITY)
- **git-workflow-manager** - Git operations, PRs, branch management

### Analysis & Planning (5 agents)
- **state-analyzer** - State feature extraction and ranking
- **business-analyst** - Requirements analysis, stakeholder communication
- **data-scientist** - Data analysis, statistical processing
- **project-manager** - Multi-step coordination, timeline management
- **agent-auditor** - **NEW**: Strategic HR for agent portfolio

### Documentation & Content (3 agents)
- **technical-documentation-writer** - API docs, technical specifications
- **content-writer** - Marketing content, user-facing docs
- **changelog-recorder** - Automatic changelog generation

### Special Purpose (3+ agents)
- **design-simplicity-advisor** - KISS enforcement (mandatory)
- **agent-creator** - Meta-agent for creating new specialists
- **general-purpose** - Fallback for basic tasks

**Plus**: System automatically creates new agents when gaps are detected!

---

## 📊 Key Features

### 1. **Automatic Telemetry** (Phase 1-3) ✅
Every agent invocation is logged automatically with:
- Agent used and task type
- Duration and outcome
- Quality ratings
- State features (languages, frameworks, etc.)

**Zero effort required** - happens in background via hooks.

### 2. **Capability Gap Detection** (Phase 1-3) ✅
When you need an agent that doesn't exist:
```
You: "Analyze the ROI of this investment"
System: No financial-analyst exists
System: Creates financial-analyst automatically
System: Notifies you to review before deployment
You: Approve specification
System: Agent deployed and ready to use!
```

**Adapts to YOUR needs** - not just predefined agents.

### 3. **Agent-Auditor (Agentic HR)** (Phase 5) ✅
Strategic portfolio manager that:
- Evaluates all agent performance monthly
- Identifies capability gaps from patterns
- Detects redundancy and overlap
- Recommends creation/refactoring/consolidation/deprecation

**Like having HR for your agents** - maintains portfolio health.

### 4. **Intelligent Prompting** (Phase 1-5) ✅
System prompts you when action needed:
- **Weekly**: "15 new invocations - 5 min review due"
- **Monthly**: "Agent audit complete - 30 min curation"
- **Agent Reviews**: "2 new agents awaiting approval"

**Shell prompts on terminal open** + **macOS notifications** + **daily checks**.

### 5. **Human-in-the-Loop Quality Control** (Phase 5) ✅
New agents require your review before first deployment:
```bash
oak-list-pending-agents    # See what's pending
oak-review-agent <name>    # Read specification
oak-approve-agent <name>   # Deploy immediately
oak-modify-agent <name>    # Edit before approving
```

**After first approval**, system can auto-update based on learning.

### 6. **A/B Testing & Continuous Improvement** (Phase 5) ✅
Improved agent versions tested scientifically:
- Original vs improved comparison
- Statistical significance testing
- Performance metrics tracked
- Best version deployed automatically

**Evidence-based evolution** - not guesswork.

### 7. **ML Pipeline (Coming Soon)** (Phase 6) 🚧
Machine learning will:
- Learn optimal agent selection patterns
- Predict agent performance before delegation
- Recommend best agents for each task type
- Continuously improve recommendations

**The longer you use it, the smarter it gets.**

---

## 🎮 Daily Usage

### Using Agents (Exactly Like Before)

```
# In Claude Code, just ask normally:
You: "Implement OAuth2 authentication"
You: "Fix this deployment error"
You: "Create a financial dashboard"

# System handles everything automatically:
# - Classifies request
# - Selects best agent(s)
# - Logs telemetry
# - Detects gaps if needed
# - Creates new agents when helpful
```

### Weekly Rhythm (15 Minutes)

**Monday 9am**: Weekly review runs automatically → Notification sent

**You run:**
```bash
oak-weekly-review
```

**You see**:
- Performance summary (5 min read)
- Top performing agents
- Areas for improvement
- New invocations summary

**System tracks** you reviewed → Stops nagging until next week.

### Monthly Rhythm (1 Hour)

**1st of month 10am**: Monthly analysis runs → Curation agenda ready

**You run:**
```bash
oak-monthly-review
```

**You see**:
- Agent portfolio audit report
- Capability gaps detected
- Recommended new agents
- Refactoring suggestions
- Redundancy analysis

**You review** recommendations (~30 min) → Approve actions → System executes.

### Agent Review (As Needed)

When system creates a new agent:

**You get notified**: "New agent ready for review"

**You run:**
```bash
oak-list-pending-agents    # See pending
oak-review-agent financial-analyst  # Read spec
oak-approve-agent financial-analyst  # Deploy
```

**Takes 5-10 minutes** per agent. First-time only; future updates are automatic.

---

## 📁 Project Structure

```
claude-oak-agents/
├── agents/                         # All agent definitions
│   ├── pending_review/             # New agents awaiting approval
│   ├── rejected/                   # Rejected agents archive
│   ├── frontend-developer.md       # Core 29 agents
│   ├── agent-auditor.md            # NEW: Strategic HR
│   └── ...
├── telemetry/                      # Performance data (local only)
│   ├── agent_invocations.jsonl     # All invocations logged
│   ├── success_metrics.jsonl       # Quality ratings
│   ├── routing_failures.jsonl      # Capability gaps detected
│   └── agent_reviews.jsonl         # Review decisions
├── automation/                     # Automation system
│   ├── install_automation.sh       # One-command setup
│   ├── oak_prompts.sh              # Shell integration
│   ├── oak_notify.sh               # Notification system
│   └── launchd/                    # Scheduled tasks
├── scripts/                        # Analysis & review scripts
│   ├── automation/                 # Weekly/monthly analysis
│   ├── phase4/                     # Dashboards & feedback
│   ├── phase5/                     # Agent audit & A/B testing
│   ├── phase6/                     # ML pipeline (future)
│   └── agent_review.py             # Review workflow
├── hooks/                          # Automatic telemetry hooks
│   ├── pre_agent_hook.py           # Logs before agent runs
│   └── post_agent_hook.py          # Logs after completion
├── docs/oak-design/                # Architecture docs
│   ├── OAK_ARCHITECTURE.md         # Complete design
│   ├── IMPLEMENTATION_GUIDE.md     # Technical details
│   └── 6_MONTH_DEPLOYMENT_PLAN.md  # Rollout roadmap
├── configs/                        # Configuration files
│   ├── curation_config.yaml        # Agent curation settings
│   ├── rl_config.yaml              # ML pipeline config
│   └── ab_test_template.yaml       # A/B test template
├── reports/                        # Generated reports
├── CLAUDE.md                       # Agent delegation rules
├── QUICK_START.md                  # 5-minute guide
├── EXECUTIVE_OVERVIEW.md           # vs claude-squad comparison
└── README.md                       # This file
```

---

## 🔧 Available Commands

### Daily Use

```bash
oak-status              # System status and pending items
oak-check-pending       # Quick check for pending agents
```

### Weekly/Monthly

```bash
oak-weekly-review       # Run weekly analysis (15 min)
oak-monthly-review      # Run monthly curation (1 hr)
oak-health-check        # System health validation
oak-dashboard           # Performance dashboard
```

### Agent Review

```bash
oak-list-pending-agents         # List agents awaiting approval
oak-review-agent <name>         # Review agent specification
oak-approve-agent <name>        # Approve and deploy
oak-modify-agent <name>         # Edit before approving
oak-reject-agent <name> "..."   # Reject with reason
```

---

## 📈 The Learning Flywheel

```
Use Agents
    ↓
Telemetry Captures Performance
    ↓
Weekly/Monthly Analysis
    ↓
Insights & Recommendations
    ↓
A/B Testing (Phase 5)
    ↓
Improvements Deployed
    ↓
ML Learning (Phase 6)
    ↓
Better Agent Selection
    ↓
(Back to Use Agents - but smarter)
```

**Each iteration makes the system better at serving YOUR needs.**

---

## 🗓️ Deployment Timeline

| Phase | Status | Timeline | What You Get |
|-------|--------|----------|--------------|
| **1-3** | ✅ Complete | Day 1 | Telemetry, hooks, gap detection, agent-auditor |
| **4** | ✅ Complete | Month 1-2 | Dashboards, feedback collection, transition models |
| **5** | ✅ Complete | Month 3-4 | A/B testing, curation automation, review workflow |
| **6** | 🚧 In Progress | Month 5-6 | ML pipeline, policy learning, autonomous optimization |

**You get value immediately** and it compounds over time.

---

## ⚙️ Configuration

### Environment Variables (Optional)

Add to `~/.zshrc`:
```bash
export OAK_TELEMETRY_ENABLED=true
export OAK_TELEMETRY_DIR="$HOME/Projects/claude-oak-agents/telemetry"
export OAK_PROMPT_FEEDBACK=false  # Enable interactive feedback prompts
export PYTHONPATH="$HOME/Projects/claude-oak-agents:$PYTHONPATH"
```

Reload:
```bash
source ~/.zshrc
```

### Disabling Features

**Disable telemetry** (not recommended):
```bash
export OAK_TELEMETRY_ENABLED=false
```

**Uninstall automation**:
```bash
./automation/uninstall_automation.sh
```

**Remove agents**:
```bash
rm ~/.claude/agents/*
```

---

## 🛠️ Troubleshooting

### Hooks Not Working

**Check installation:**
```bash
ls -la ~/.claude/hooks/
# Should show: pre_agent.sh, post_agent.sh
```

**Fix permissions:**
```bash
chmod +x hooks/*.py
```

**Test telemetry:**
```bash
python3 scripts/test_telemetry_e2e.py
```

### Shell Prompts Not Showing

**Check ~/.zshrc:**
```bash
grep "oak_prompts.sh" ~/.zshrc
```

**If missing, add:**
```bash
echo 'source "$HOME/Projects/claude-oak-agents/automation/oak_prompts.sh"' >> ~/.zshrc
source ~/.zshrc
```

### Scheduled Tasks Not Running

**Check launchd jobs:**
```bash
launchctl list | grep com.oak
```

**Reload if needed:**
```bash
launchctl load ~/Library/LaunchAgents/com.oak.weekly-review.plist
```

### More Help

- **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
- **[automation/README.md](automation/README.md)** - Automation system details
- **[hooks/README.md](hooks/README.md)** - Telemetry hooks guide
- **GitHub Issues** - Report problems or ask questions

---

## 🎯 Next Steps

1. ✅ **Install** (5 minutes) - Follow Quick Install above
2. ✅ **Use normally** - Start using agents in Claude Code
3. ✅ **First week** - Let telemetry collect data
4. ✅ **Week 2** - First weekly review (oak-weekly-review)
5. ✅ **Month 1** - First monthly audit (oak-monthly-review)
6. ✅ **Month 2** - First capability gap filled automatically
7. ✅ **Month 3** - First A/B test running
8. ✅ **Month 6** - ML pipeline active, full autonomous optimization

**The sooner you start, the sooner the learning begins.**

---

## 📚 Documentation

- **[EXECUTIVE_OVERVIEW.md](EXECUTIVE_OVERVIEW.md)** - Comparison vs claude-squad
- **[QUICK_START.md](QUICK_START.md)** - 5-minute getting started
- **[docs/oak-design/OAK_ARCHITECTURE.md](docs/oak-design/OAK_ARCHITECTURE.md)** - Complete architecture
- **[docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md](docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)** - Detailed roadmap
- **[automation/README.md](automation/README.md)** - Automation system
- **[agents/pending_review/README.md](agents/pending_review/README.md)** - Review workflow

---

## 🤝 Contributing

Contributions welcome! Priority areas:

- **Phase 6 ML Pipeline**: Offline RL implementation
- **Agent Improvements**: Based on telemetry analysis
- **Dashboard UI**: Web interface for analytics
- **Integration**: Additional tool integrations
- **Documentation**: Examples, tutorials, use cases

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🙏 Credits

- **Original System**: [claude-squad](https://github.com/jamsajones/claude-squad) by jamsajones
- **OaK Architecture**: Inspired by hierarchical RL research
- **Contributors**: See [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🔗 Links

- **Original Repo**: https://github.com/jamsajones/claude-squad
- **Documentation**: [docs/oak-design/](docs/oak-design/)
- **Issues**: [GitHub Issues](https://github.com/your-org/claude-oak-agents/issues)

---

**Status**: ✅ Phases 1-5 Complete | 🚧 Phase 6 In Progress | 29+ Agents | Self-Learning Active | Automation Ready

**Get Started**: [Quick Install](#-quick-install-5-minutes) ⬆️
