# A/B Tests Directory

Active and historical A/B tests for agent improvements.

## Structure

```
tests/
├── README.md                           # This file
├── active/                             # Currently running tests
│   ├── test_backend_architect_001.yaml
│   └── test_frontend_developer_002.yaml
├── completed/                          # Finished tests
│   └── test_project_manager_001.yaml
└── templates/                          # Test templates
    └── standard_test.yaml
```

## Creating a New Test

### 1. Copy Template

```bash
cp configs/ab_test_template.yaml tests/active/test_<agent_name>_<id>.yaml
```

### 2. Edit Configuration

```yaml
test_id: "test_backend_architect_001"
agent_name: "backend-architect"
status: "active"

hypothesis: |
  Improved error handling will increase success rate

variants:
  - id: "original"
    agent_file: "agents/backend-architect.md"
  - id: "improved"
    agent_file: "archive/agents/test_variants/backend-architect_v2.md"
```

### 3. Create Improved Variant

```bash
# Copy original agent
cp agents/backend-architect.md archive/agents/test_variants/backend-architect_v2.md

# Make improvements
vim archive/agents/test_variants/backend-architect_v2.md
```

### 4. Start Test

Test starts automatically based on traffic split configuration. Monitor with:

```bash
python scripts/phase5/ab_test_status.py
```

## Monitoring Active Tests

### Check Status

```bash
# All active tests
python scripts/phase5/ab_test_status.py

# Specific test
python scripts/phase5/ab_test_status.py --test-id test_backend_architect_001
```

### View Results

```bash
# Real-time results
cat tests/active/test_backend_architect_001.yaml | grep -A 20 "results:"

# Statistical analysis
python scripts/phase5/analyze_test_results.py --test-id test_backend_architect_001
```

## Making Curation Decisions

### When Test Completes

After reaching minimum sample size and duration:

```bash
# Review results
python scripts/phase5/review_ab_tests.py

# Record decision
python scripts/phase5/record_curation_decisions.py
```

### Decision Options

1. **Promote:** Deploy improved variant to production
2. **Rollback:** Keep original, archive improved variant
3. **Extend Test:** Need more data
4. **Redesign:** Neither variant is good, try different approach

### Applying Decisions

```bash
# Promote improved variant
python scripts/phase5/apply_improvement.py --test-id test_backend_architect_001 --action promote

# Or manually:
cp archive/agents/test_variants/backend-architect_v2.md agents/backend-architect.md
mv tests/active/test_backend_architect_001.yaml tests/completed/
```

## Best Practices

### Test Design

- **Single change:** Test one improvement at a time
- **Clear hypothesis:** Document expected impact
- **Meaningful metrics:** Choose metrics that matter
- **Sufficient sample:** At least 20 invocations per variant
- **Adequate duration:** Minimum 14 days

### Traffic Allocation

- **50/50 split:** Standard for most tests
- **90/10 split:** For risky changes, minimize exposure
- **Gradual ramp:** Start 90/10, increase to 50/50 after confidence

### Statistical Rigor

- **Don't peek early:** Wait for minimum sample size
- **Multiple comparisons:** Adjust significance for multiple metrics
- **Practical significance:** Improvement must be meaningful, not just statistically significant

## Test Lifecycle

### Active Phase

1. Test created in `tests/active/`
2. Telemetry hooks log invocations for both variants
3. Results auto-populate in test YAML
4. Monitor progress weekly

### Completion Phase

5. Minimum sample size reached
6. Statistical analysis run automatically
7. Human reviews results
8. Curation decision recorded

### Post-Test Phase

9. Decision applied (promote/rollback)
10. Test moved to `tests/completed/`
11. Learnings documented
12. Original version archived if replaced

## Troubleshooting

### Not Enough Data

**Problem:** Test running but few invocations
- **Solution:** Check agent is being used normally, extend test duration

### Inconclusive Results

**Problem:** No clear winner after full test
- **Solution:** Variants may be too similar, or sample size too small

### Contradictory Metrics

**Problem:** Success rate improved but quality decreased
- **Solution:** Human judgment required, consider trade-offs

### Test Interference

**Problem:** Multiple tests affecting same agent
- **Solution:** Limit concurrent tests per agent (max 1 recommended)

## Example Tests

### Example 1: Error Handling Improvement

```yaml
test_id: "test_backend_001"
hypothesis: "Better error context will reduce failures"

variants:
  original: "Standard error handling"
  improved: "Enhanced error messages and retry logic"

results:
  original: {success_rate: 0.75, avg_quality: 3.5}
  improved: {success_rate: 0.85, avg_quality: 4.0}

decision:
  outcome: "promote"
  reasoning: "10% success improvement, higher quality, statistically significant"
```

### Example 2: Performance Optimization

```yaml
test_id: "test_perf_001"
hypothesis: "Caching will reduce duration without sacrificing quality"

variants:
  original: "No caching"
  improved: "Intelligent caching layer"

results:
  original: {avg_duration: 120s, success_rate: 0.80}
  improved: {avg_duration: 45s, success_rate: 0.78}

decision:
  outcome: "rollback"
  reasoning: "Faster but slightly lower success rate - not acceptable trade-off"
```

## See Also

- [Curation Configuration](../configs/curation_config.yaml)
- [6-Month Deployment Plan](../docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)
- [Phase 5 Scripts](../scripts/phase5/)
