# Claude OaK Agents

**Options and Knowledge (OaK) Architecture for Claude Code Agents**

A comprehensive agent system with 29+ specialized agents, OaK-inspired hierarchical reinforcement learning, telemetry infrastructure, and data-driven agent optimization.

Based on [claude-subagents](https://github.com/jamsajones/claude-subagents) with OaK architecture enhancements for systematic agent improvement through offline learning.

---

## 🎯 What's New: OaK Architecture

This project extends the original Claude Squad plugin with:

- **📊 Telemetry System**: Log every agent invocation with state features and outcomes
- **🧠 State Analysis**: Extract and rank features before task decomposition
- **📈 Performance Tracking**: Measure agent success rates, quality scores, and durations
- **🔄 Offline Learning**: Data-driven agent improvements (future ML pipeline)
- **🎯 Feature-Based Decomposition**: Systematic task breakdown using ranked features
- **📋 Transition Models**: Document expected agent behavior for planning
- **🔧 Adaptive Curation**: Continuous agent improvement based on telemetry data

### OaK Principles Applied

| OaK Component | Implementation |
|---------------|----------------|
| **Options** | 29+ specialist agents as temporally-extended actions |
| **State Features** | Codebase, task, context, and historical features |
| **Policy** | Heuristic rules + learned recommendations (future) |
| **Value Function** | Utility scores from telemetry and human feedback |
| **Subgoal Decomposition** | Feature-ranked task breakdown |
| **Learning** | Offline RL on logged data (Phase 6) |
| **Meta-data** | Persistent telemetry logs for all invocations |
| **Curation** | Data-driven agent improvements |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url> ~/Projects/claude-oak-agents
cd ~/Projects/claude-oak-agents

# Install Python dependencies
pip install -r requirements.txt  # TODO: Create this file

# Test telemetry system
python telemetry/logger.py

# Test state analysis
python state-analysis/feature_extractor.py

# Install agents (optional - if not using plugin system)
cp -r agents/ ~/.claude/agents/
# Or create symlinks
ln -s ~/Projects/claude-oak-agents/agents/* ~/.claude/agents/
```

### Basic Usage

```bash
# In Claude Code, use agents as usual:
User: "Implement OAuth2 authentication"

# Main LLM will now:
# 1. Classify request (IMPLEMENTATION)
# 2. Analyze state with state-analyzer agent
# 3. Delegate to security-auditor + backend-architect
# 4. Log telemetry data automatically (future)
# 5. Collect feedback for learning
```

### Viewing Analytics

```bash
# Generate performance statistics
python telemetry/analyzer.py

# View agent rankings
python -c "
from telemetry.analyzer import TelemetryAnalyzer
analyzer = TelemetryAnalyzer()
rankings = analyzer.get_agent_ranking()
for agent, score, stats in rankings[:5]:
    print(f'{agent}: {score:.3f}')
"
```

---

## 📁 Project Structure

```
claude-oak-agents/
├── agents/                     # 29+ specialist agent definitions
│   ├── state-analyzer.md       # NEW: State feature extraction agent
│   ├── frontend-developer.md
│   ├── backend-architect.md
│   └── ...
├── telemetry/                  # NEW: Telemetry infrastructure
│   ├── schemas.json            # Data schemas
│   ├── logger.py               # Logging utilities
│   ├── analyzer.py             # Analysis utilities
│   ├── agent_invocations.jsonl # Logged invocations
│   ├── success_metrics.jsonl   # Feedback data
│   └── performance_stats.json  # Aggregated statistics
├── state-analysis/             # NEW: State feature extraction
│   └── feature_extractor.py    # Feature extraction utilities
├── models/                     # NEW: Transition models (Phase 4)
│   ├── transition_expectations.yaml
│   └── agent_utility_scores.yaml
├── ml-pipeline/                # NEW: ML pipeline (Phase 6)
│   ├── data_preprocessing.py
│   ├── policy_learning.py
│   └── export_policies.py
├── docs/oak-design/            # NEW: OaK documentation
│   ├── OAK_ARCHITECTURE.md     # Architecture overview
│   └── IMPLEMENTATION_GUIDE.md # Step-by-step guide
├── commands/                   # Squad management commands
│   ├── squad-on.md
│   ├── squad-off.md
│   └── squad-status.md
├── hooks/                      # Session automation
├── scripts/                    # NEW: Utility scripts
├── CLAUDE.md                   # Delegation enforcement rules
└── README.md                   # This file
```

---

## 🤖 Agent System (29+ Specialists)

### 🏗️ Core Development Agents
- **frontend-developer** - UI/UX, React/Vue/Angular, browser compatibility
- **backend-architect** - Database design, API architecture, microservices
- **infrastructure-specialist** - CDK constructs, cloud deployment, DevOps
- **mobile-developer** - React Native, iOS, Android development
- **blockchain-developer** - Solidity, Web3 integration, DeFi protocols
- **ml-engineer** - Python ML systems, TensorFlow/PyTorch, MLOps
- **legacy-maintainer** - Java, C#, enterprise system maintenance

### 🛡️ Security & Quality Agents
- **security-auditor** - Penetration testing, compliance, threat modeling
- **code-reviewer** - Code quality gates, standards enforcement
- **unit-test-expert** - Comprehensive unit testing, edge case identification
- **dependency-scanner** - Supply chain security, license compliance
- **qa-specialist** - Integration testing, E2E validation

### 🔧 Infrastructure & Operations
- **systems-architect** - High-level system design, technical specifications
- **performance-optimizer** - Performance analysis, bottleneck identification
- **debug-specialist** - Critical error resolution (HIGHEST PRIORITY)
- **git-workflow-manager** - Git operations, branch management

### 📊 Analysis & Planning
- **state-analyzer** - **NEW**: State feature extraction and ranking
- **business-analyst** - Requirements analysis, stakeholder communication
- **data-scientist** - Data analysis, statistical processing
- **project-manager** - Multi-step coordination, timeline management

### 📝 Documentation & Content
- **technical-documentation-writer** - API docs, technical specifications
- **content-writer** - Marketing content, user-facing documentation
- **changelog-recorder** - Automatic changelog generation

### 🎯 Special Purpose
- **design-simplicity-advisor** - KISS enforcement (mandatory pre-commit)
- **agent-creator** - Meta-agent for creating new specialists

---

## 📊 Telemetry & Analytics

### Logging Agent Invocations

```python
from telemetry.logger import TelemetryLogger

logger = TelemetryLogger()

# Log invocation start
invocation_id = logger.log_invocation(
    agent_name="frontend-developer",
    agent_type="development",
    task_description="Add dark mode toggle",
    state_features={
        "codebase": {"languages": ["TypeScript"]},
        "task": {"type": "feature_development", "scope": "small"}
    }
)

# Log completion
logger.update_invocation(
    invocation_id=invocation_id,
    duration_seconds=120,
    outcome_status="success",
    files_modified=["src/Settings.tsx"]
)

# Log feedback
logger.log_success_metric(
    invocation_id=invocation_id,
    success=True,
    quality_rating=4,
    feedback_notes="Works well!"
)
```

### Analyzing Performance

```bash
# Generate statistics
python telemetry/analyzer.py

# View JSON output
cat telemetry/performance_stats.json | jq
```

### Agent Rankings

```python
from telemetry.analyzer import TelemetryAnalyzer

analyzer = TelemetryAnalyzer()

# Get overall rankings
rankings = analyzer.get_agent_ranking()

# Get rankings for specific task type
frontend_rankings = analyzer.get_agent_ranking(task_type="feature_development")

for agent_name, score, stats in rankings[:10]:
    print(f"{agent_name}: {score:.3f} ({stats['invocation_count']} uses)")
```

---

## 🧠 State Analysis

The **state-analyzer** agent extracts structured features before task execution:

### Features Extracted

1. **Codebase Features**: Languages, frameworks, LOC, complexity, architecture
2. **Task Features**: Type, scope, risk level, domain, estimated effort
3. **Context Features**: Tests, docs, git state, dependencies, build status
4. **Historical Features**: Similar tasks, success patterns, agent performance

### Example Usage

```python
from state_analysis.feature_extractor import FeatureExtractor

extractor = FeatureExtractor(workspace_dir="/path/to/project")
features = extractor.extract_all_features()

print(features["codebase"]["languages"])  # ["Python", "JavaScript"]
print(features["context"]["tests_exist"])  # True
```

### In Claude Code

```
User: Implement OAuth2 authentication with JWT tokens

Main LLM: I'll analyze the state first...
[Invokes state-analyzer agent]

state-analyzer: {
  "ranked_features": [
    {"feature": "risk_level", "value": "critical", "importance": 0.95},
    {"feature": "scope", "value": "large", "importance": 0.90}
  ],
  "recommended_strategy": {
    "primary_agents": ["security-auditor", "backend-architect"],
    "decomposition_needed": true
  }
}

Main LLM: This is high-risk. I'll delegate to security-auditor and backend-architect...
```

---

## 🎓 Implementation Phases

### ✅ Phase 1: Telemetry Infrastructure (COMPLETE)
- Telemetry logging utilities
- JSON schemas for data
- Analyzer for statistics generation
- Manual integration ready

### 🚧 Phase 2: State Analysis (IN PROGRESS)
- State analyzer agent definition
- Feature extraction utilities
- Integration with main workflow

### 📋 Phase 3: Feature-Based Decomposition (TODO)
- Enhanced project-manager with feature ranking
- Systematic subproblem creation
- Agent mapping based on ranked features

### 📋 Phase 4: Transition Models (TODO)
- Document expected agent behavior
- Utility tracking and feedback collection
- Performance dashboards

### 📋 Phase 5: Adaptive Curation (TODO)
- Weekly/monthly agent analysis
- Data-driven improvements
- A/B testing framework

### 📋 Phase 6: ML Pipeline (FUTURE)
- Offline reinforcement learning
- Policy optimization from logged data
- Automatic agent selection recommendations

---

## 📖 Documentation

- **[OaK Architecture](./docs/oak-design/OAK_ARCHITECTURE.md)** - Complete architectural overview
- **[Implementation Guide](./docs/oak-design/IMPLEMENTATION_GUIDE.md)** - Step-by-step setup
- **[Telemetry README](./telemetry/README.md)** - Telemetry system documentation
- **[State Analyzer Agent](./agents/state-analyzer.md)** - State analysis agent definition
- **[CLAUDE.md](./CLAUDE.md)** - Delegation enforcement rules

---

## 🔧 Configuration

### Enabling OaK Features

1. **Telemetry**: Currently manual - see [Implementation Guide](./docs/oak-design/IMPLEMENTATION_GUIDE.md)
2. **State Analysis**: Invoke `state-analyzer` agent explicitly or integrate with project-manager
3. **Automated Hooks**: Coming in Phase 1.5 - auto-log all invocations

### Environment Variables

```bash
# Optional: Configure telemetry directory
export TELEMETRY_DIR=~/Projects/claude-oak-agents/telemetry

# Optional: Enable complex workflow (legacy)
export COMPLEX_WORKFLOW=true

# Optional: Python path for imports
export PYTHONPATH=~/Projects/claude-oak-agents:$PYTHONPATH
```

---

## 🤝 Contributing

Contributions welcome! Areas of interest:

- **Phase 3+**: Feature-based decomposition, transition models, ML pipeline
- **Automated Hooks**: Pre/post agent execution logging
- **Dashboard**: Web UI for telemetry visualization
- **ML Models**: Offline RL implementations for policy learning
- **Agent Improvements**: Based on telemetry data analysis

---

## 📊 Example Telemetry Output

```json
{
  "generated_at": "2025-10-16T14:30:00Z",
  "total_invocations": 47,
  "agents": {
    "frontend-developer": {
      "invocation_count": 15,
      "success_rate": 0.933,
      "average_quality": 4.2,
      "average_duration_seconds": 125.3,
      "common_task_types": ["feature_development", "bug_fix"],
      "recommended_for": ["High success rate - reliable choice"]
    },
    "backend-architect": {
      "invocation_count": 12,
      "success_rate": 0.833,
      "average_quality": 3.9,
      "average_duration_seconds": 210.5,
      "common_task_types": ["architecture", "feature_development"]
    }
  }
}
```

---

## 🙏 Credits

- **Original Claude Squad**: [jamsajones/claude-subagents](https://github.com/jamsajones/claude-subagents)
- **OaK Architecture**: Inspired by hierarchical reinforcement learning research
- **Contributors**: See [CONTRIBUTORS.md](./CONTRIBUTORS.md) (TODO)

---

## 📝 License

MIT License - see [LICENSE](./LICENSE) for details

---

## 🔗 Links

- **Original Repo**: https://github.com/jamsajones/claude-subagents
- **Documentation**: [./docs/oak-design/](./docs/oak-design/)
- **Issues**: [GitHub Issues](https://github.com/your-org/claude-oak-agents/issues)

---

**Status**: Phase 2 In Progress | 29+ Agents | Telemetry Active | State Analysis Ready
