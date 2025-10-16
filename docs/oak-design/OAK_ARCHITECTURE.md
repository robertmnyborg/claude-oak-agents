# OaK Architecture for Claude Agents

## Overview

This project implements an **Options and Knowledge (OaK)** inspired architecture on top of the Claude Squad agent system. While true OaK requires real-time reinforcement learning, this implementation provides OaK-like capabilities through persistent telemetry, explicit state modeling, and human-in-the-loop learning.

## Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Main LLM (Coordinator)                    │
│                  - Agent selection policy                    │
│                  - Task decomposition                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ├──► State Analyzer Agent
                        │    - Extracts state features
                        │    - Ranks features by importance
                        │
                        ├──► Policy Advisor Agent (Future)
                        │    - Reads learned policies
                        │    - Suggests optimal agents
                        │
                        ├──► 28 Specialist Agents
                        │    - Execute domain-specific tasks
                        │    - Log telemetry data
                        │
                        └──► Telemetry System
                             - Captures all invocations
                             - Tracks success metrics
                             - Feeds ML pipeline
```

## OaK Mapping

| OaK Component | Implementation | Status |
|---------------|----------------|--------|
| **Options** | Specialist agents as temporally-extended actions | ✅ Exists |
| **State Features** | Extracted by state-analyzer agent | 🚧 Phase 2 |
| **Policy** | Heuristic rules + learned recommendations | 🚧 Phase 3 |
| **Value Function** | Utility scores from telemetry | 🚧 Phase 4 |
| **Transition Models** | Expected outcomes documented in YAML | 🚧 Phase 4 |
| **Subgoal Decomposition** | Feature-ranked task breakdown | 🚧 Phase 3 |
| **Learning** | Offline RL on logged data | 🔮 Phase 6 |
| **Meta-data** | Persistent telemetry logs | 🚧 Phase 1 |
| **Curation** | agent-creator + data-driven improvements | 🔮 Phase 5 |

## Phase Implementation Plan

### Phase 1: Telemetry Infrastructure ✅ IN PROGRESS

**Objective:** Capture all agent interactions for offline analysis

**Components:**
- `telemetry/agent_invocations.jsonl` - Log every agent call
- `telemetry/success_metrics.jsonl` - Success/failure/quality ratings
- `telemetry/performance_stats.json` - Aggregated statistics
- Hook system to auto-log agent entry/exit

**Deliverables:**
- Telemetry logging hooks
- JSON schema definitions
- Initial dashboard script

### Phase 2: State Feature Extraction 🔜 NEXT

**Objective:** Explicit state representation before task decomposition

**Components:**
- `state-analysis/state-analyzer-agent.md` - New agent definition
- `state-analysis/feature_extractors.py` - Python utilities
- `state-analysis/schemas.json` - Feature schemas

**Deliverables:**
- State analyzer agent
- Feature extraction framework
- Integration with project-manager

### Phase 3: Feature-Based Decomposition

**Objective:** Rank features and create subproblems systematically

**Components:**
- Enhanced project-manager agent
- Feature ranking heuristics
- Subproblem mapping logic

**Deliverables:**
- Updated project-manager.md
- Feature ranking rules
- Subproblem templates

### Phase 4: Transition Models & Utility Tracking

**Objective:** Document expected agent behavior and track performance

**Components:**
- `models/transition_expectations.yaml` - Expected outcomes per agent
- `models/agent_utility_scores.yaml` - Performance ratings
- Rating prompts for human feedback

**Deliverables:**
- Transition model docs
- Utility tracking system
- Performance dashboard

### Phase 5: Adaptive Curation

**Objective:** Systematic agent improvement based on data

**Components:**
- Analysis scripts for telemetry
- Curation workflow
- A/B testing framework

**Deliverables:**
- Curation playbook
- Agent versioning system
- Performance comparison tools

### Phase 6: ML Pipeline (Advanced)

**Objective:** Offline RL for policy learning

**Components:**
- `ml-pipeline/data_preprocessing.py` - Clean telemetry data
- `ml-pipeline/policy_learning.py` - Train agent selection policies
- `ml-pipeline/export_policies.py` - Generate YAML rules

**Deliverables:**
- RL training pipeline
- Policy export system
- Integration with policy-advisor agent

## Key Differences from Pure OaK

### What We CAN'T Do:
- ❌ Real-time policy gradient updates
- ❌ Online exploration vs exploitation
- ❌ Automatic value function convergence
- ❌ Dynamic option discovery during runtime
- ❌ Cross-conversation learning (without external storage)

### What We CAN Do:
- ✅ Offline policy learning from logged data
- ✅ Human-in-the-loop reward signals
- ✅ Explicit state feature engineering
- ✅ Feature-based task decomposition
- ✅ Transition model documentation
- ✅ Utility-driven agent curation
- ✅ A/B testing of agent versions

## Data Flow

```
1. User Request
   ↓
2. State Analyzer extracts features
   ↓
3. Policy Advisor suggests agents (based on past data)
   ↓
4. Main LLM selects agent(s)
   ↓
5. Agent executes task
   ↓
6. Telemetry logs: [timestamp, agent, state, action, outcome]
   ↓
7. Human rates outcome (optional)
   ↓
8. Telemetry aggregates to stats
   ↓
9. ML pipeline trains on historical logs
   ↓
10. Policy rules updated
    ↓
    [Loop back to step 3]
```

## Success Metrics

### Phase 1-2:
- All agent invocations logged with metadata
- State features extracted for 100% of tasks

### Phase 3-4:
- Decomposition based on ranked features
- Transition models documented for all agents
- Human feedback collected for 50%+ of tasks

### Phase 5-6:
- Agent improvements deployed monthly
- ML-recommended agents show higher success rates
- Automatic policy updates from logged data

## Technical Stack

- **Agent Execution:** Claude Code + markdown prompts
- **Telemetry:** JSONL logs + Python scripts
- **State Analysis:** Python + regex + AST parsing
- **ML Pipeline:** Python + scikit-learn/PyTorch + Optuna
- **Visualization:** matplotlib/plotly + Jupyter notebooks
- **Storage:** Local filesystem (Phase 1-4) → PostgreSQL (Phase 5-6)

## Getting Started

See [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) for step-by-step instructions.

## References

- [OaK Paper: Options and Knowledge for Hierarchical RL](https://arxiv.org/abs/your-reference)
- [Claude Squad Original Repo](https://github.com/jamsajones/claude-subagents)
- [Hierarchical RL Survey](https://arxiv.org/abs/your-reference)
