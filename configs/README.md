# Configuration Directory

Central configuration files for OaK agent system.

## Files

### `curation_config.yaml`

**Purpose:** Controls Phase 5 agent curation and A/B testing

**Key Sections:**
- **failure_detection:** Thresholds for identifying problematic agents
- **improvement_triggers:** When to propose agent improvements
- **ab_testing:** A/B test configuration and metrics
- **decision_criteria:** Automatic vs manual decision rules
- **improvement_workflow:** Step-by-step curation process

**Used By:**
- `scripts/phase5/analyze_failures.py`
- `scripts/phase5/audit_agents.py`
- `scripts/phase5/ab_test_status.py`
- `scripts/automation/monthly_analysis.py`

### `rl_config.yaml` (MOVED)

**Status:** This configuration has been moved to `docs/experimental/phase6/rl_config.yaml` as Phase 6 is experimental/future work.

**Purpose:** Controls Phase 6 offline RL training and policy learning

**Key Sections:**
- **data_preparation:** Feature engineering and normalization
- **model:** CQL algorithm configuration and hyperparameters
- **reward:** Reward function design
- **baseline:** Baseline models for comparison
- **policy_export:** Policy deployment configuration
- **safety:** Gradual rollout and rollback rules

**Used By (Future):**
- `scripts/phase6/prepare_training_data.py`
- `scripts/phase6/validate_training_data.py`
- `scripts/phase6/train_baseline_models.py`
- `scripts/phase6/train_rl_policy.py`

**Note:** Phase 6 ML pipeline will be implemented when Phase 6 begins. Configuration file will be created in experimental directory at that time.

### `ab_test_template.yaml`

**Purpose:** Template for creating new A/B tests

**Usage:**
```bash
# Create new A/B test
cp configs/ab_test_template.yaml tests/test_backend_architect_001.yaml

# Edit configuration
vim tests/test_backend_architect_001.yaml

# Start test (test runs automatically based on traffic split)
# Monitor with:
python scripts/phase5/ab_test_status.py
```

**Sections:**
- **test_id:** Unique identifier
- **variants:** Original vs improved versions
- **hypothesis:** What you're testing
- **success_criteria:** How to determine winner
- **results:** Auto-populated during test
- **decision:** Manual curation decision

## Configuration Management

### Versioning

All configs include `version: "1.0"` field. When making breaking changes:
1. Increment version
2. Update all dependent scripts
3. Document migration path

### Validation

Validate configurations before use:

```bash
# Validate curation config
python scripts/validation/validate_config.py configs/curation_config.yaml

# Validate RL config
python scripts/validation/validate_config.py configs/rl_config.yaml
```

### Environment Overrides

Override config values with environment variables:

```bash
# Override A/B testing sample size
export OAK_AB_SAMPLE_SIZE=30

# Override RL learning rate
export OAK_RL_LEARNING_RATE=0.0005
```

## Best Practices

### Curation Configuration

- **Start conservative:** Higher thresholds initially, lower as you gain confidence
- **Manual review first:** Set `auto_promote: false` until comfortable with automation
- **Test duration:** 14 days minimum for meaningful statistical results
- **Sample size:** At least 20 invocations per variant

### RL Configuration

- **Baseline first:** Always train baseline models before RL policy
- **Hyperparameter tuning:** Use validation set to tune hyperparameters
- **Conservative deployment:** Start with `rollout_percentage_stages: [10, 25, 50, 100]`
- **Monitor closely:** Enable all safety features initially

### A/B Testing

- **One change at a time:** Test single improvement per experiment
- **Clear hypothesis:** Document what you expect to improve and why
- **Statistical rigor:** Don't end tests early even if results look good
- **Document learnings:** Update notes throughout test

## Troubleshooting

### Curation Config Issues

**Problem:** Too many agents flagged for review
- **Solution:** Increase `min_invocations` and `failure_rate_threshold`

**Problem:** Not catching failing agents
- **Solution:** Decrease thresholds, enable more improvement triggers

### RL Config Issues

**Problem:** Training not converging
- **Solution:** Reduce learning rate, increase batch size, check reward function

**Problem:** Policy performs worse than baseline
- **Solution:** Increase min_episodes, tune hyperparameters, check feature engineering

### A/B Test Issues

**Problem:** Inconclusive results
- **Solution:** Increase sample_size, extend test duration, check if variants are truly different

**Problem:** Results contradict expectations
- **Solution:** Review hypothesis, check for confounding factors, analyze failure modes

## Advanced Usage

### Custom Reward Functions

Modify `rl_config.yaml` to implement custom rewards:

```yaml
reward:
  # Use Python expression (evaluated safely)
  formula: |
    outcome_reward = 10.0 if success else -5.0
    quality_bonus = quality_rating * 2.0 if quality_rating else 0
    duration_penalty = -0.01 * duration_seconds
    return outcome_reward + quality_bonus + duration_penalty
```

### Dynamic Thresholds

Implement adaptive thresholds based on historical data:

```python
# In scripts/phase5/audit_agents.py
config = load_config("configs/curation_config.yaml")
historical_baseline = calculate_baseline_performance()
config['failure_detection']['failure_rate_threshold'] = historical_baseline * 1.5
```

### Multi-Metric Optimization

Configure RL to optimize multiple objectives:

```yaml
reward:
  multi_objective: true
  objectives:
    - name: "success_rate"
      weight: 0.6
    - name: "duration"
      weight: 0.2
    - name: "quality"
      weight: 0.2
```

## See Also

- [6-Month Deployment Plan](../docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)
- [Implementation Guide](../docs/oak-design/IMPLEMENTATION_GUIDE.md)
- [Phase 5 Scripts](../scripts/phase5/)
- [Phase 6 Scripts](../scripts/phase6/)
