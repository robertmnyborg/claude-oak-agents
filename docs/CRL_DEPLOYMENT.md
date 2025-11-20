# CRL System Deployment Checklist

Production deployment checklist for the Continual Reinforcement Learning (CRL) system.

## Pre-Deployment Validation

### 1. System Validation

Run complete system validation:

```bash
python scripts/crl/validate_system.py
```

Expected output:
```
✅ Phase 1: Foundation: PASS
✅ Phase 2: Q-Learning: PASS
✅ Phase 3: Safety: PASS
✅ Phase 4: Advanced Algorithms: PASS
✅ Integration: PASS
✅ Tests: PASS
✅ Performance: PASS

VALIDATION SUMMARY: 7/7 checks passed
✅ SYSTEM READY FOR PRODUCTION
```

### 2. Run All Tests

Execute full test suite:

```bash
# Run all CRL tests
python -m pytest tests/crl/ -v

# Expected results
# - test_task_classifier.py: PASSED
# - test_agent_basis.py: PASSED
# - test_q_learning.py: PASSED
# - test_reward_calculator.py: PASSED
# - test_safety.py: PASSED
# - test_advanced.py: PASSED
# - test_e2e_integration.py: PASSED
```

All tests must pass before deployment.

### 3. Performance Benchmarks

Verify performance targets:

```bash
python scripts/crl/benchmark_system.py
```

Required targets:
- **CRL overhead**: < 20ms
- **Task classification**: < 10ms
- **Variant selection**: < 5ms
- **Memory overhead**: < 50MB

### 4. Configuration Review

Verify CRL configuration:

**Q-Learning Parameters** (`core/q_learning.py`):
```python
QLearningEngine(
    learning_rate=0.1,       # ✅ Conservative for production
    exploration_rate=0.1     # ✅ 10% exploration is safe
)
```

**Reward Calculator** (`core/reward_calculator.py`):
```python
RewardCalculator(
    success_weight=1.0,      # ✅ Success is primary signal
    quality_weight=0.5,      # ✅ Quality matters
    time_weight=-0.3,        # ✅ Small time penalty
    error_weight=-0.5        # ✅ Moderate error penalty
)
```

**Safety Monitor** (`core/safety_monitor.py`):
```python
SafetyMonitor(
    min_success_rate=0.5,    # ✅ Halt if <50% success
    lookback_window=10,      # ✅ Recent performance only
    enable_rollback=True     # ✅ Auto-rollback enabled
)
```

## Deployment Steps

### Step 1: Create Backup

Backup current system state:

```bash
# Backup telemetry
cp -r telemetry/ telemetry_backup_$(date +%Y%m%d)/

# Backup agent variants
cp -r agents/basis/ agents/basis_backup_$(date +%Y%m%d)/

# Backup configuration
cp core/q_learning.py core/q_learning.py.backup
cp core/reward_calculator.py core/reward_calculator.py.backup
```

### Step 2: Initialize Agent Variants

Create default variants for all agents:

```bash
python scripts/crl/initialize_variants.py --all-agents
```

Or manually create variants:

```yaml
# agents/basis/backend-architect/default.yaml
variant_id: default
agent_name: backend-architect
description: Default configuration for backend-architect
specialization: [general]
model_tier: balanced
temperature: 0.7
prompt_modifications: []
performance_metrics:
  invocation_count: 0
  success_count: 0
  avg_duration: 0.0
  avg_quality_score: 0.0
  avg_reward: 0.0
created_at: "2025-11-20T00:00:00Z"
```

### Step 3: Enable CRL Gradually

**Phase 1: Monitoring Only (Week 1)**
```python
# Enable CRL but log decisions without acting
router = DomainRouter(crl_enabled=True)
routing = router.route_request(request, files)

# Use default variant, log CRL recommendation
variant_to_use = "default"  # Ignore CRL for now
log_crl_recommendation(routing)  # Track what CRL would do
```

**Phase 2: Shadow Mode (Week 2)**
```python
# Execute both default and CRL variant, compare results
result_default = execute_agent(agent, variant="default")
result_crl = execute_agent(agent, variant=routing["variant"])

compare_results(result_default, result_crl)
```

**Phase 3: Canary Deployment (Week 3)**
```python
# 10% of requests use CRL
if random.random() < 0.1:
    variant = routing["variant"]  # CRL
else:
    variant = "default"  # Existing
```

**Phase 4: Full Deployment (Week 4+)**
```python
# All requests use CRL
router = DomainRouter(crl_enabled=True)
routing = router.route_request(request, files)
# Use routing["variant"] for all executions
```

### Step 4: Deploy Safety Mechanisms

Enable safety monitoring:

```python
from core.safety_monitor import SafetyMonitor
from core.rollback_manager import RollbackManager

# Initialize safety
safety_monitor = SafetyMonitor()
rollback_manager = RollbackManager()

# Check safety before execution
if not safety_monitor.is_safe_to_execute(agent, variant):
    # Rollback to safe variant
    safe_variant = rollback_manager.get_safe_variant(agent)
    variant = safe_variant
```

### Step 5: Configure Telemetry

Ensure telemetry captures CRL data:

```python
from telemetry.logger import TelemetryLogger

logger = TelemetryLogger()

# Log with CRL fields
invocation_id = logger.log_invocation(
    agent_name=agent_name,
    agent_type="development",
    task_description=request,
    agent_variant=variant_id,      # Required
    task_type=task_type,           # Required
    q_value=q_value,               # Required
    exploration=exploration,        # Required
    learning_enabled=True          # Required
)
```

### Step 6: Set Up Monitoring

Monitor CRL performance:

```bash
# Daily Q-value review
python scripts/crl/view_q_values.py --top 20 > logs/q_values_$(date +%Y%m%d).txt

# Weekly safety dashboard
python scripts/crl/safety_dashboard.py > logs/safety_$(date +%Y%m%d).txt

# Performance tracking
python scripts/crl/benchmark_system.py > logs/performance_$(date +%Y%m%d).txt
```

## Post-Deployment Monitoring

### Week 1: Initial Monitoring

**Daily checks**:
1. **Q-value updates**: Are Q-values changing?
2. **Exploration rate**: Is exploration happening? (~10% of requests)
3. **Safety triggers**: Any rollbacks triggered?
4. **Performance**: CRL overhead < 20ms?

```bash
# Check Q-table activity
wc -l telemetry/crl/q_table.jsonl
# Should increase daily

# Check safety logs
grep "ROLLBACK" telemetry/crl/safety_events.jsonl
# Should be rare
```

**Key Metrics**:
- Q-value updates per day: >10
- Exploration rate: ~10%
- Rollback events: <1% of invocations
- Average reward: >0.0 (positive learning)

### Week 2-4: Convergence Monitoring

**Weekly analysis**:
1. **Q-value convergence**: Are Q-values stabilizing?
2. **Variant performance**: Which variants are winning?
3. **Task type accuracy**: Is classification accurate?
4. **Learning rate**: Should α be adjusted?

```bash
# Analyze Q-value convergence
python scripts/crl/analyze_convergence.py

# Compare variant performance
python scripts/crl/compare_algorithms.py --variants-only
```

**Convergence Indicators**:
- Q-value changes < 0.1 per update (stable)
- Clear variant winners emerging (>0.7 Q-value)
- Exploration decreasing naturally
- Reward variance stabilizing

### Month 2+: Optimization

**Monthly reviews**:
1. **Hyperparameter tuning**: Adjust α, ε based on data
2. **Variant creation**: Add new variants for emerging patterns
3. **Safety thresholds**: Tune based on actual failure rates
4. **Performance optimization**: Profile slow paths

```bash
# Monthly optimization report
python scripts/crl/monthly_report.py --month $(date +%Y-%m)
```

## Rollback Procedure

If issues arise, rollback in reverse order:

### Emergency Rollback (Immediate)

```bash
# 1. Disable CRL immediately
# Set environment variable
export CRL_ENABLED=false

# Or modify code
# DomainRouter(crl_enabled=False)
```

### Partial Rollback (Next Deploy)

```python
# Revert to canary (10%)
if random.random() < 0.1:
    # Use CRL
    variant = routing["variant"]
else:
    # Use default
    variant = "default"
```

### Full Rollback (If Necessary)

```bash
# 1. Restore backups
cp -r telemetry_backup_YYYYMMDD/ telemetry/
cp -r agents/basis_backup_YYYYMMDD/ agents/basis/

# 2. Disable CRL in code
# DomainRouter(crl_enabled=False)

# 3. Redeploy
# ... deployment process ...

# 4. Verify rollback
python scripts/crl/validate_system.py
# Should show crl_enabled=False everywhere
```

## Success Criteria

CRL deployment is successful if:

### Week 1
- ✅ Zero breaking changes to existing functionality
- ✅ CRL overhead < 20ms
- ✅ Q-values updating (>10 updates/day)
- ✅ No safety rollbacks triggered

### Week 4
- ✅ Q-values converging (change < 0.1)
- ✅ Variant winners emerging (Q-value > 0.7)
- ✅ Task classification accuracy > 70%
- ✅ Average reward > 0.0

### Month 3
- ✅ Clear performance improvements in key task types
- ✅ Stable Q-values (minimal updates needed)
- ✅ Safety mechanisms rarely triggered (<1%)
- ✅ System running in full CRL mode

## Troubleshooting

### Issue: Q-values not updating

**Diagnosis**:
```bash
# Check Q-table file
cat telemetry/crl/q_table.jsonl | wc -l
# Should be >0 and increasing

# Check file permissions
ls -la telemetry/crl/q_table.jsonl
# Should be writable
```

**Solution**:
```bash
# Fix permissions
chmod 644 telemetry/crl/q_table.jsonl

# Verify writes
python -c "from core.q_learning import QLearningEngine; q = QLearningEngine(); q.update_q_value('test', 'test', 'test', 1.0)"
cat telemetry/crl/q_table.jsonl | grep test
```

### Issue: High rollback rate

**Diagnosis**:
```bash
# Check rollback frequency
grep "ROLLBACK" telemetry/crl/safety_events.jsonl | wc -l

# Identify problem variants
python scripts/crl/safety_dashboard.py
```

**Solution**:
```python
# Adjust safety thresholds
SafetyMonitor(
    min_success_rate=0.4,  # Lower threshold temporarily
    lookback_window=20     # Longer window for smoothing
)

# Or disable problematic variants
# Remove variant YAML file temporarily
```

### Issue: Poor task classification

**Diagnosis**:
```bash
# Test classifier accuracy
python -c "from core.task_classifier import TaskClassifier; c = TaskClassifier(); print(c.classify('your request', ['file.ts']))"
```

**Solution**:
```python
# Add custom task types
from core.task_classifier import TaskClassifier
classifier = TaskClassifier()

classifier.add_custom_task_type(
    task_type="domain-specific-task",
    keywords=["specific", "keywords"],
    file_patterns=[r".*pattern\..*"],
    weight=1.2  # Higher weight
)
```

## Maintenance

### Weekly Tasks
- Review Q-value trends
- Check safety logs
- Verify performance metrics
- Update variant configurations

### Monthly Tasks
- Analyze learning convergence
- Optimize hyperparameters
- Create new variants
- Archive unused variants

### Quarterly Tasks
- Full system validation
- Performance benchmarking
- Algorithm comparison
- Documentation updates

## Support Contacts

For deployment issues:
1. Check troubleshooting section above
2. Review `docs/CRL_TROUBLESHOOTING.md`
3. Run `python scripts/crl/validate_system.py`
4. Check recent git history for similar issues

## Deployment Sign-Off

Before marking deployment complete, verify:

- [ ] All tests passing (`pytest tests/crl/`)
- [ ] System validation passing (`scripts/crl/validate_system.py`)
- [ ] Performance benchmarks met (`scripts/crl/benchmark_system.py`)
- [ ] Telemetry capturing CRL data
- [ ] Safety monitors configured
- [ ] Monitoring dashboards set up
- [ ] Rollback procedure tested
- [ ] Documentation updated
- [ ] Team trained on CRL system

**Deployment Date**: _______________  
**Deployed By**: _______________  
**Sign-Off**: _______________
