# OaK Implementation Guide

This guide walks you through implementing the OaK (Options and Knowledge) architecture enhancements for Claude Agents.

## Prerequisites

- Python 3.8+
- Claude Code CLI
- Git
- A project workspace to analyze

## Quick Start

### 1. Installation

The repository is already set up with all necessary files. Verify the structure:

```bash
cd ~/Projects/claude-oak-agents
ls -la
```

You should see:
- `agents/` - 29+ specialist agents (including new `state-analyzer.md`)
- `telemetry/` - Telemetry infrastructure
- `state-analysis/` - State feature extraction
- `models/` - Transition models (Phase 4)
- `ml-pipeline/` - ML pipeline (Phase 6)

### 2. Test Telemetry System

```bash
# Run example logging
python telemetry/logger.py

# Verify files created
ls telemetry/
# Should show: agent_invocations.jsonl, success_metrics.jsonl

# Run analyzer
python telemetry/analyzer.py
```

### 3. Test State Analysis

```bash
# Run feature extractor on current directory
python state-analysis/feature_extractor.py

# Should output JSON with codebase and context features
```

### 4. Install Agents (if not already installed)

If you haven't installed the agents into your Claude Code instance:

```bash
# Copy agent definitions to Claude's agent directory
cp -r agents/ ~/.claude/agents/

# Or create symlinks
ln -s ~/Projects/claude-oak-agents/agents/* ~/.claude/agents/
```

## Phase-by-Phase Implementation

### Phase 1: Telemetry (✅ COMPLETE)

**Goal:** Capture all agent interactions for offline analysis.

#### Files Created:
- `telemetry/schemas.json` - Data schemas
- `telemetry/logger.py` - Logging utilities
- `telemetry/analyzer.py` - Analysis utilities
- `telemetry/README.md` - Documentation

#### How to Use:

1. **Manual Logging** (current approach):

```python
from telemetry.logger import TelemetryLogger

# In your agent invocation script
logger = TelemetryLogger()

invocation_id = logger.log_invocation(
    agent_name="frontend-developer",
    agent_type="development",
    task_description="Add dark mode toggle",
    state_features={...}
)

# After agent completes
logger.update_invocation(
    invocation_id=invocation_id,
    duration_seconds=120,
    outcome_status="success"
)

# Collect feedback
logger.log_success_metric(
    invocation_id=invocation_id,
    success=True,
    quality_rating=4
)
```

2. **Analyze Data**:

```bash
# Generate statistics
python telemetry/analyzer.py

# View performance stats
cat telemetry/performance_stats.json | jq
```

3. **Regular Cadence**:
   - Log every agent invocation
   - Collect human feedback for 50%+ of tasks
   - Run analyzer weekly
   - Review performance trends monthly

#### Next Steps:
- [ ] Create hooks for automatic logging (see Phase 1.5 below)
- [ ] Set up weekly analysis cron job
- [ ] Create dashboard visualization

---

### Phase 1.5: Automated Telemetry Hooks (TODO)

**Goal:** Automatically log agent invocations without manual intervention.

#### Implementation Plan:

1. **Create Pre/Post Agent Hooks**:

```bash
# Create hook directory
mkdir -p ~/.claude/hooks

# Create pre-agent hook
cat > ~/.claude/hooks/pre-agent.sh << 'EOF'
#!/bin/bash
# Log agent invocation start
python3 ~/Projects/claude-oak-agents/scripts/log_agent_start.sh "$@"
EOF

chmod +x ~/.claude/hooks/pre-agent.sh
```

2. **Create Logging Scripts**:

```bash
# scripts/log_agent_start.sh
# scripts/log_agent_end.sh
# scripts/collect_feedback.sh
```

3. **Integrate with Claude Code**:

Modify `.claude/config.json` to enable hooks:

```json
{
  "hooks": {
    "pre_agent": "~/.claude/hooks/pre-agent.sh",
    "post_agent": "~/.claude/hooks/post-agent.sh"
  }
}
```

---

### Phase 2: State Analysis (🚧 IN PROGRESS)

**Goal:** Extract and rank state features before task planning.

#### Files Created:
- `agents/state-analyzer.md` - State analyzer agent definition
- `state-analysis/feature_extractor.py` - Feature extraction utilities

#### How to Use:

1. **Manual Invocation**:

In Claude Code, invoke the state-analyzer agent before starting a complex task:

```
User: Implement OAuth2 authentication with JWT tokens

Main LLM: I'll analyze the state first to inform our implementation strategy.
[Invokes state-analyzer agent]

state-analyzer: [Returns JSON with ranked features showing high risk, large scope]

Main LLM: Based on the state analysis, this is a high-risk, large-scope task.
I'll delegate to security-auditor and backend-architect...
```

2. **Programmatic Usage**:

```python
from state_analysis.feature_extractor import FeatureExtractor

extractor = FeatureExtractor(workspace_dir="/path/to/project")
features = extractor.extract_all_features()

# Use features for agent selection
if features["context"]["tests_passing"] == False:
    print("Recommend: unit-test-expert first")
```

#### Next Steps:
- [x] Create state-analyzer agent
- [x] Create feature_extractor utilities
- [ ] Integrate with project-manager agent
- [ ] Add historical feature extraction from telemetry
- [ ] Create feature ranking heuristics

---

### Phase 3: Feature-Based Decomposition (TODO)

**Goal:** Use ranked features to systematically decompose tasks.

#### Implementation Plan:

1. **Enhance project-manager Agent**:
   - Read state features from state-analyzer output
   - Rank features by importance
   - Create subproblems from top-N features
   - Map subproblems to specific agents

2. **Feature Ranking Heuristics**:
   - Risk level (critical > high > medium > low)
   - Scope (epic > large > medium > small)
   - Test status (failing > no tests > passing)
   - Historical success (low success rate = higher importance)

3. **Subproblem Templates**:
   - "Fix broken tests" (high priority if tests failing)
   - "Security review" (mandatory if risk=critical)
   - "Architecture design" (needed if scope=large/epic)
   - "Performance optimization" (based on complexity/LOC)

---

### Phase 4: Transition Models & Utility Tracking (TODO)

**Goal:** Document expected agent behavior and track performance over time.

#### Files to Create:
- `models/transition_expectations.yaml` - Expected outcomes per agent
- `models/agent_utility_scores.yaml` - Performance ratings
- `scripts/collect_feedback.py` - Human feedback prompts

#### Transition Model Format:

```yaml
# models/transition_expectations.yaml
agents:
  frontend-developer:
    preconditions:
      - "UI/UX work required"
      - "React/Vue/Angular codebase"
    postconditions:
      - "Component files created/modified"
      - "Styles updated"
    expected_duration_minutes: [5, 30]  # min, max
    success_rate: 0.85  # Manually updated initially
    common_failures:
      - "Complex state management"
      - "Performance optimization needs"
    recommended_context:
      task_types: ["feature_development", "bug_fix", "refactoring"]
      risk_levels: ["low", "medium"]
```

#### Usage:

1. **Planning**: Before invoking agent, check expected duration and success rate
2. **Post-execution**: Compare actual vs expected outcomes
3. **Curation**: Update models based on accumulated data

---

### Phase 5: Adaptive Curation (TODO)

**Goal:** Systematically improve agents based on telemetry data.

#### Curation Process:

```
Weekly/Monthly:
1. Run telemetry analyzer
2. Identify: low-performing agents, coverage gaps, redundant agents
3. Generate improvement plan
4. Use agent-creator to implement changes
5. A/B test new versions
6. Promote winners, retire losers
```

#### Curation Criteria:
- Success rate < 50% with 5+ invocations → needs improvement
- Avg quality < 3.0 → needs refinement
- Zero invocations in 30 days → consider deprecation
- High demand + no specialist → create new agent

---

### Phase 6: ML Pipeline (FUTURE)

**Goal:** Offline reinforcement learning for policy optimization.

#### Components:

1. **Data Preprocessing**:
   - Clean telemetry JSONL files
   - Feature engineering for state representations
   - Label outcomes (success/failure, quality scores)

2. **Policy Learning**:
   - Train agent selection policy using offline RL
   - Learn Q-functions or policy gradients from logged data
   - Handle exploration bias (importance sampling)

3. **Policy Export**:
   - Export learned policy as YAML rules
   - Create policy-advisor agent that reads rules
   - Integrate with Main LLM for recommendations

4. **Continuous Learning**:
   - Periodic retraining on new data
   - A/B testing of policy versions
   - Gradual policy updates

#### Tech Stack:
- Python 3.9+
- PyTorch or TensorFlow
- Ray RLlib for offline RL
- Optuna for hyperparameter tuning
- PostgreSQL for large-scale data

---

## Testing Your Setup

### 1. End-to-End Test

```bash
# Create a test project
mkdir -p /tmp/test-project
cd /tmp/test-project
echo "print('hello')" > main.py

# Run state analysis
python ~/Projects/claude-oak-agents/state-analysis/feature_extractor.py

# Manually log an invocation
python -c "
from sys import path
path.append('$HOME/Projects/claude-oak-agents')
from telemetry.logger import TelemetryLogger

logger = TelemetryLogger()
inv_id = logger.log_invocation(
    agent_name='test-agent',
    agent_type='development',
    task_description='Test invocation',
    state_features={'codebase': {'languages': ['Python']}}
)
logger.update_invocation(inv_id, duration_seconds=10, outcome_status='success')
logger.log_success_metric(inv_id, success=True, quality_rating=5)
print(f'Logged: {inv_id}')
"

# Analyze telemetry
cd ~/Projects/claude-oak-agents
python telemetry/analyzer.py
```

### 2. Agent Invocation Test

In Claude Code:

```
User: Analyze the state of my current project

Main LLM: I'll invoke the state-analyzer agent...

[state-analyzer agent runs, outputs JSON]

Main LLM: [Interprets and summarizes results]
```

---

## Troubleshooting

### Issue: Telemetry files not created
**Solution**: Check file permissions, ensure directory exists, verify Python paths

### Issue: State analyzer can't detect languages
**Solution**: Ensure you're in a valid project directory with code files

### Issue: Agent not found
**Solution**: Verify agents are in `~/.claude/agents/` or symlinked correctly

### Issue: Import errors in Python scripts
**Solution**: Run from project root or add to PYTHONPATH:
```bash
export PYTHONPATH="$HOME/Projects/claude-oak-agents:$PYTHONPATH"
```

---

## Next Steps

After completing Phase 1-2:

1. **Collect Data**: Use telemetry for 2-4 weeks to accumulate baseline data
2. **Implement Phase 3**: Feature-based decomposition in project-manager
3. **Create Transition Models**: Document expected agent behavior
4. **Set Up Curation**: Weekly/monthly agent improvement process
5. **Explore ML**: When you have 100+ logged invocations, consider Phase 6

---

## Resources

- [OaK Architecture Overview](./OAK_ARCHITECTURE.md)
- [Telemetry Documentation](../../telemetry/README.md)
- [State Analyzer Agent](../../agents/state-analyzer.md)
- [Original Claude Squad Repo](https://github.com/jamsajones/claude-subagents)

---

*Questions? Open an issue or reach out to the maintainers.*