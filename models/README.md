# Models Directory

Trained ML models for agent selection and policy learning (Phase 6).

## Structure

```
models/
├── README.md                    # This file
├── baselines/                   # Simple baseline models
│   ├── random.json
│   ├── most_frequent.json
│   └── highest_success.json
├── policies/                    # Trained RL policies
│   ├── trained_policy_v1.json
│   └── trained_policy_v2.json
├── training_data/               # Prepared datasets
│   ├── train.jsonl
│   ├── test.jsonl
│   └── validation.jsonl
├── checkpoints/                 # Training checkpoints
│   └── epoch_100/
└── evaluation/                  # Model evaluation results
    ├── baseline_comparison.json
    └── policy_evaluation.json
```

## Phase 6 Workflow

### Step 1: Prepare Training Data

```bash
# Extract features from telemetry
python scripts/phase6/prepare_training_data.py

# Output: models/training_data/{train,test,validation}.jsonl
```

**Training data format:**
```json
{
  "state": {
    "codebase_languages": ["TypeScript", "Python"],
    "task_type": "implementation",
    "complexity": "medium",
    "historical_success_rate": 0.85
  },
  "action": "backend-architect",
  "reward": 8.5,
  "next_state": {...},
  "done": true
}
```

### Step 2: Validate Data

```bash
# Check data quality
python scripts/phase6/validate_training_data.py

# Outputs validation report
```

### Step 3: Train Baseline Models

```bash
# Train simple baselines for comparison
python scripts/phase6/train_baseline_models.py

# Output: models/baselines/*.json
```

**Baseline models:**
- **random:** Selects agent randomly
- **most_frequent:** Always selects most commonly used agent
- **highest_success:** Selects agent with highest historical success rate

### Step 4: Train RL Policy

```bash
# Train CQL policy
python scripts/phase6/train_rl_policy.py

# Output: models/policies/trained_policy_v1.json
# Also: models/checkpoints/epoch_*/
```

**Training configuration:** See `docs/experimental/phase6/rl_config.yaml`

### Step 5: Evaluate Policy

```bash
# Compare against baselines
python scripts/phase6/evaluate_policy.py

# Output: models/evaluation/policy_evaluation.json
```

**Evaluation metrics:**
- Accuracy (correct agent selection)
- Success rate (selected agent succeeds)
- Average reward
- Regret (vs optimal)

### Step 6: Export Policy

```bash
# Export for deployment
python scripts/phase6/export_policy.py --policy trained_policy_v1

# Output: models/policies/trained_policy_v1_production.json
```

### Step 7: Create Policy Advisor Agent

```bash
# Generate agent that uses trained policy
python scripts/phase6/create_policy_advisor_agent.py

# Output: agents/policy-advisor.md
```

## Model Management

### Versioning

Models are versioned sequentially:
- `trained_policy_v1.json` - First trained policy
- `trained_policy_v2.json` - Retrained with new data
- etc.

### Deployment

```bash
# Deploy policy to production
python scripts/phase6/deploy_policy.py --version v2 --mode advisor

# Modes:
#   advisor  - Recommend agents, human decides
#   primary  - Policy decides, human override available
#   hybrid   - Policy + historical heuristics
```

### Rollback

```bash
# Rollback to previous version
python scripts/phase6/rollback_policy.py --to-version v1
```

## Baseline Models

### Random

```json
{
  "name": "random",
  "type": "baseline",
  "strategy": "uniform_random",
  "performance": {
    "accuracy": 0.15,
    "success_rate": 0.68
  }
}
```

### Most Frequent

```json
{
  "name": "most_frequent",
  "type": "baseline",
  "strategy": "always_select_most_common",
  "most_common_agent": "backend-architect",
  "performance": {
    "accuracy": 0.35,
    "success_rate": 0.72
  }
}
```

### Highest Success

```json
{
  "name": "highest_success",
  "type": "baseline",
  "strategy": "select_best_historical",
  "agent_success_rates": {
    "backend-architect": 0.85,
    "frontend-developer": 0.82,
    "infrastructure-specialist": 0.78
  },
  "performance": {
    "accuracy": 0.45,
    "success_rate": 0.76
  }
}
```

## Trained Policy Format

```json
{
  "version": "v1",
  "algorithm": "CQL",
  "trained_date": "2025-11-01",
  "training_episodes": 150,
  "hyperparameters": {
    "learning_rate": 0.0003,
    "batch_size": 64,
    "gamma": 0.99
  },
  "state_features": [
    "codebase_languages",
    "task_type",
    "complexity"
  ],
  "action_space": [
    "frontend-developer",
    "backend-architect",
    "infrastructure-specialist"
  ],
  "q_network": {
    "architecture": [256, 256],
    "weights": "checkpoints/final/weights.pkl"
  },
  "performance": {
    "train_accuracy": 0.68,
    "test_accuracy": 0.62,
    "baseline_improvement": 0.17
  }
}
```

## Using Policy Advisor Agent

Once trained policy is deployed as policy-advisor agent:

```bash
# User requests implementation
User: "Build secure API endpoint"

# Main LLM delegates to policy-advisor
Main LLM: [invokes policy-advisor agent]

# Policy-advisor recommends agents
Policy Advisor:
  Top recommendations:
  1. security-auditor (confidence: 0.85)
  2. backend-architect (confidence: 0.78)
  3. infrastructure-specialist (confidence: 0.65)

  Reasoning: Task keywords suggest security-critical backend work.
  Historical data shows security-auditor → backend-architect sequence
  performs well for similar tasks.

# Main LLM coordinates based on recommendations
Main LLM: [invokes security-auditor → backend-architect]
```

## Monitoring Policy Performance

### Real-Time Metrics

```bash
# View policy performance
python scripts/phase6/monitor_policy.py

# Output:
#   Recommendations made: 45
#   Recommendations followed: 38 (84%)
#   Success rate: 0.82
#   Baseline comparison: +15%
```

### Weekly Health Check

```bash
# Automated health check
python scripts/automation/health_check.py --include-policy

# Checks:
#   - Policy prediction accuracy
#   - Recommendation acceptance rate
#   - Actual success rate of recommendations
```

### Degradation Detection

If policy performance degrades:
```bash
# Alert generated
⚠️  Policy performance degraded by 18%
   Current success rate: 0.68
   Expected: 0.82+

   Actions:
   1. Review recent failures
   2. Check for data distribution shift
   3. Consider retraining
```

## Retraining

### When to Retrain

- Every 30 days (scheduled)
- After collecting 50+ new episodes
- When performance degrades >15%
- After significant agent changes

### Retraining Process

```bash
# Prepare new training data
python scripts/phase6/prepare_training_data.py --since-last-training

# Retrain policy
python scripts/phase6/train_rl_policy.py --version v2 --incremental

# Evaluate improvement
python scripts/phase6/evaluate_policy.py --compare-to v1

# Deploy if better
python scripts/phase6/deploy_policy.py --version v2 --mode advisor
```

## Troubleshooting

### Low Accuracy

**Problem:** Policy accuracy < 0.6
- **Causes:** Insufficient training data, poor feature engineering, wrong hyperparameters
- **Solutions:** Collect more data, add features, tune hyperparameters

### Overfitting

**Problem:** Train accuracy high, test accuracy low
- **Causes:** Model too complex, insufficient regularization
- **Solutions:** Add dropout, reduce network size, increase training data

### Not Beating Baselines

**Problem:** Policy no better than simple heuristics
- **Causes:** Features don't capture important patterns, task too simple
- **Solutions:** Improve feature engineering, consider if ML is necessary

### Recommendations Ignored

**Problem:** Humans not following policy recommendations
- **Causes:** Recommendations don't make sense, low confidence
- **Solutions:** Improve explainability, increase confidence threshold

## Advanced Usage

### Multi-Agent Coordination

Train policy to recommend agent sequences:

```json
{
  "action_space": [
    "security-auditor",
    "backend-architect",
    ["security-auditor", "backend-architect"],
    ["design-simplicity-advisor", "infrastructure-specialist"]
  ]
}
```

### Transfer Learning

Use pre-trained policy for new team:

```bash
# Export policy
python scripts/phase6/export_policy.py --format onnx

# Import on new system
python scripts/phase6/import_policy.py --file policy.onnx --fine-tune
```

### Continuous Learning

Enable automatic retraining:

```yaml
# In configs/rl_config.yaml
continuous_learning:
  enabled: true
  retrain_frequency_days: 30
  min_new_episodes: 50
  auto_deploy: false  # Still require manual approval
```

## See Also

- [RL Configuration](../docs/experimental/phase6/rl_config.yaml)
- [6-Month Deployment Plan](../docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)
- [Phase 6 Scripts](../scripts/phase6/)
- [OaK Architecture](../docs/oak-design/OAK_ARCHITECTURE.md)
