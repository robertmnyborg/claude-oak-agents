# CRL Safety Mechanisms Guide

**Phase 3 Implementation - Safety & Automation**

## Overview

Phase 3 implements safety mechanisms and automation for the Continual Reinforcement Learning (CRL) system. These mechanisms ensure that variant changes are made safely, with appropriate human oversight, and automatic rollback on performance degradation.

## Architecture

### Safety Decision Flow

```
Variant Performance
       ↓
Q-learning Updates
       ↓
Safety Monitor Analysis
       ↓
    ┌──────────────┬──────────────┬──────────────┐
    │              │              │              │
High Confidence  Medium         Low
(Q>0.9, n≥10)   (Q>0.7, n≥5)   (else)
    │              │              │
Auto-Apply    Human Approval   No Action
```

### Degradation Detection & Rollback

```
Continuous Monitoring
       ↓
Performance Check (last 20 invocations)
       ↓
Degradation Detected?
       ├─ NO → Continue monitoring
       │
       └─ YES → Find previous best variant
                    ↓
              Execute Rollback
                    ↓
              Log Rollback Event
                    ↓
              Alert Human Operator
```

### Variant Proposal Generation

```
Performance Analysis
       ↓
Identify Patterns
    ┌────────────────┬────────────────┬────────────────┐
    │                │                │                │
No Specialized   Large Perf Gap   Underperformance
   Variant        (>20% diff)       (Q<0.6)
    │                │                │
    └────────────────┴────────────────┘
                    ↓
          Generate Proposal
                    ↓
          Human Review Queue
```

## Components

### 1. Safety Monitor (`core/safety_monitor.py`)

**Purpose**: Determine whether variant changes can be auto-applied or require human approval.

**Decision Matrix**:

| Q-value | n_visits | Decision        | Description                          |
|---------|----------|-----------------|--------------------------------------|
| ≥ 0.9   | ≥ 10     | Auto-Apply      | High confidence, consistent perf     |
| ≥ 0.7   | ≥ 5      | Human Approval  | Medium confidence, needs review      |
| < 0.7   | Any      | No Action       | Low confidence, insufficient data    |
| Any     | < 5      | No Action       | Insufficient samples                 |

**Key Methods**:

```python
from core.safety_monitor import SafetyMonitor

monitor = SafetyMonitor()

# Check if variant should be auto-applied
decision, reasoning = monitor.should_auto_apply_variant(
    agent_name="backend-architect",
    task_type="api-design",
    variant_id="api-optimized"
)
# Returns: ("auto_apply", "High confidence: Q-value 0.95 >= 0.9...")

# Check for performance degradation
degraded, metrics = monitor.check_performance_degradation(
    agent_name="backend-architect",
    task_type="api-design",
    variant_id="api-optimized",
    lookback_window=20
)
# Returns: (True, {"success_drop_pct": 0.15, ...}) if degraded
```

**Degradation Thresholds**:
- Success rate drop > 10%
- Average reward drop > 15%
- Error rate increase > 20%

### 2. Rollback Manager (`core/rollback_manager.py`)

**Purpose**: Monitor variant performance and trigger rollbacks on degradation.

**Rollback Workflow**:
1. Detect degradation (via SafetyMonitor)
2. Find previous best variant (highest Q-value, n≥5)
3. Execute rollback (update variant configuration)
4. Log rollback event to `telemetry/crl/rollback_events.jsonl`
5. Alert human operator

**Key Methods**:

```python
from core.rollback_manager import RollbackManager

manager = RollbackManager()

# Monitor and trigger rollback if degraded
rollback_info = manager.monitor_and_rollback(
    agent_name="backend-architect",
    task_type="api-design",
    current_variant="api-optimized"
)

if rollback_info:
    print(f"Rolled back: {rollback_info['from_variant']} → {rollback_info['to_variant']}")
    print(f"Reason: {rollback_info['reason']}")

# Get rollback history
history = manager.get_rollback_history(limit=10)
for event in history:
    print(f"{event['timestamp']}: {event['rollback_id']}")
```

**Rollback Event Schema**:

```json
{
  "rollback_id": "rb-20251119-abc123",
  "timestamp": "2025-11-19T14:30:00Z",
  "agent_name": "backend-architect",
  "task_type": "api-design",
  "from_variant": "api-optimized",
  "to_variant": "default",
  "reason": "Success rate dropped from 90% to 75% (16.7% drop)",
  "degradation_metrics": {
    "baseline_success_rate": 0.90,
    "recent_success_rate": 0.75,
    "success_drop_pct": 0.167,
    "sample_size": 20
  }
}
```

### 3. Variant Proposer (`core/variant_proposer.py`)

**Purpose**: Automatically generate proposals for new agent variants based on learning patterns.

**Proposal Triggers**:
1. **No specialized variant**: Task type has only default variant and Q < 0.6
2. **Large performance gap**: Best variant Q-value > default Q-value by >20%
3. **Consistent underperformance**: Default variant Q < 0.6 with n ≥ 50

**Key Methods**:

```python
from core.variant_proposer import VariantProposer

proposer = VariantProposer()

# Analyze and generate proposals
proposals = proposer.analyze_and_propose(min_invocations=50)

for proposal in proposals:
    print(f"Proposal: {proposal['proposal_id']}")
    print(f"  Agent: {proposal['agent_name']}")
    print(f"  Task: {proposal['task_type']}")
    print(f"  Type: {proposal['proposal_type']}")
    print(f"  Confidence: {proposal['confidence']:.0%}")
    print(f"  Reasoning: {proposal['reasoning']}")

# Get pending proposals for human review
pending = proposer.get_proposals(status="pending")
```

**Proposal Types**:
- `create_specialized_variant`: Create new task-specific variant
- `modify_variant_parameters`: Adjust existing variant configuration
- `promote_variant_to_default`: Make best variant the new default
- `retire_underperforming_variant`: Remove consistently poor variant

**Proposal Schema**:

```yaml
proposal_id: "prop-20251119-xyz789"
timestamp: "2025-11-19T14:30:00Z"
agent_name: "backend-architect"
task_type: "security-audit"
proposal_type: "create_specialized_variant"
reasoning: |
  Security-audit tasks show 15% lower performance with default variant.
  Suggest creating security-focused variant.
confidence: 0.75
supporting_data:
  n_invocations: 67
  avg_q_default: 0.65
  potential_improvement: 0.15
  variance: 0.12
recommended_modifications:
  - section: "Core Identity"
    operation: "append"
    content: "Special focus on security vulnerabilities..."
  - parameter: "temperature"
    value: 0.2
    reason: "Lower temperature for precise security analysis"
status: "pending"
```

### 4. Safety Dashboard (`scripts/crl/safety_dashboard.py`)

**Purpose**: Real-time monitoring of CRL safety metrics.

**Dashboard Sections**:
1. **System Health Overview**: Q-table entries, active agents, rollback count, proposals
2. **Recent Rollbacks**: Last 10 rollback events with details
3. **Pending Proposals**: Variant proposals awaiting human review
4. **High-Confidence Variants**: Variants ready for auto-apply (Q≥0.9, n≥10)
5. **Degradation Alerts**: Active performance degradation warnings

**Usage**:

```bash
# Run dashboard
python scripts/crl/safety_dashboard.py

# Example output:
# ================================================================================
# CRL SAFETY DASHBOARD
# ================================================================================
# Generated: 2025-11-19 14:30:00 UTC
# ================================================================================
#
# --------------------------------------------------------------------------------
# SYSTEM HEALTH OVERVIEW
# --------------------------------------------------------------------------------
# Total Q-table Entries: 127
# Active Agents with Variants: 8
# Rollbacks (Last 30 Days): 2
# Pending Proposals: 3
#
# System Status: ✓ HEALTHY
# ...
```

## Integration with Proposal System

Phase 3 extends the existing proposal tracker (`telemetry/proposal_tracker.py`) with CRL-specific proposal types:

**New Proposal Types**:
- `crl_create_specialized_variant`: CRL-generated variant creation proposal
- `crl_modify_variant_parameters`: CRL-suggested parameter tuning
- `crl_retire_underperforming_variant`: CRL-identified variant removal
- `crl_promote_variant_to_default`: CRL-recommended variant promotion

**Integration Points**:
1. Variant proposer generates CRL proposals
2. Proposals logged to `telemetry/crl/variant_proposals.jsonl`
3. Human approval workflow via proposal tracker
4. Approved proposals trigger variant modifications
5. Rejected proposals logged for analysis

## Safety Guarantees

### Conservative Thresholds

**Auto-Apply Requirements** (strictest):
- Q-value ≥ 0.9 (90th percentile performance)
- n_visits ≥ 10 (sufficient sample size)
- No recent degradation

**Human Approval Requirements**:
- Q-value ≥ 0.7 (70th percentile performance)
- n_visits ≥ 5 (minimum sample size)
- Variant shows promise but needs review

### Rollback Speed

**Degradation Detection**:
- Continuous monitoring (every invocation)
- 20-invocation lookback window
- Real-time alerts on degradation

**Rollback Execution**:
- Within 1-2 invocations of detection
- Automatic selection of previous best variant
- Logged with full degradation metrics

### Human Oversight

**Required for**:
- Medium-confidence variants (0.7 ≤ Q < 0.9)
- All new variant proposals
- Rollback confirmation (post-hoc)

**Not required for**:
- High-confidence auto-apply (Q ≥ 0.9, n ≥ 10)
- Automatic rollback on degradation (logged for review)

## Usage Examples

### Example 1: Monitor and Auto-Apply

```python
from core.safety_monitor import SafetyMonitor
from core.q_learning import QLearningEngine

monitor = SafetyMonitor()
q_learning = QLearningEngine()

# Get current Q-values
agent_name = "backend-architect"
task_type = "api-design"
variants = ["default", "api-optimized"]

for variant in variants:
    q_value = q_learning.get_q_value(agent_name, task_type, variant)
    n_visits = q_learning.get_visit_count(agent_name, task_type, variant)
    
    decision, reasoning = monitor.should_auto_apply_variant(
        agent_name, task_type, variant, q_value, n_visits
    )
    
    if decision == "auto_apply":
        print(f"✓ Auto-applying {variant}")
        # Update agent configuration to use this variant
    elif decision == "human_approval":
        print(f"→ {variant} needs human approval")
        # Add to approval queue
```

### Example 2: Continuous Monitoring

```python
from core.rollback_manager import RollbackManager

manager = RollbackManager()

# Run continuously (e.g., cron job, background process)
def monitor_all_variants():
    # Get all active (agent, task_type, variant) tuples
    active_variants = get_active_variants()
    
    for agent_name, task_type, variant_id in active_variants:
        rollback_info = manager.monitor_and_rollback(
            agent_name, task_type, variant_id
        )
        
        if rollback_info:
            print(f"⚠️  Rollback triggered: {rollback_info['rollback_id']}")
            # Send alert to operator
            send_alert(rollback_info)

# Run every 5 minutes
schedule.every(5).minutes.do(monitor_all_variants)
```

### Example 3: Weekly Proposal Review

```python
from core.variant_proposer import VariantProposer

proposer = VariantProposer()

# Weekly analysis (e.g., Monday morning)
def weekly_proposal_review():
    proposals = proposer.analyze_and_propose(min_invocations=50)
    
    print(f"Generated {len(proposals)} proposals this week:")
    for proposal in proposals:
        print(f"\n{proposal['proposal_id']}")
        print(f"  Agent: {proposal['agent_name']}")
        print(f"  Task: {proposal['task_type']}")
        print(f"  Confidence: {proposal['confidence']:.0%}")
        print(f"  Type: {proposal['proposal_type']}")
        
    # Export for human review
    export_to_spreadsheet(proposals)

# Run every Monday at 9 AM
schedule.every().monday.at("09:00").do(weekly_proposal_review)
```

## Telemetry Files

### Rollback Events (`telemetry/crl/rollback_events.jsonl`)

One JSON object per line:

```json
{"rollback_id":"rb-20251119-abc123","timestamp":"2025-11-19T14:30:00Z",...}
{"rollback_id":"rb-20251119-def456","timestamp":"2025-11-19T15:45:00Z",...}
```

### Variant Proposals (`telemetry/crl/variant_proposals.jsonl`)

One JSON object per line:

```json
{"proposal_id":"prop-20251119-xyz789","timestamp":"2025-11-19T14:30:00Z",...}
{"proposal_id":"prop-20251119-uvw123","timestamp":"2025-11-19T16:20:00Z",...}
```

## Testing

Run Phase 3 tests:

```bash
# Run all CRL safety tests
python tests/crl/test_safety.py

# Run specific test class
python -m unittest tests.crl.test_safety.TestSafetyMonitor

# Run with verbose output
python tests/crl/test_safety.py -v
```

Test coverage:
- Safety monitor decision logic
- Degradation detection thresholds
- Rollback execution and logging
- Proposal generation and filtering
- End-to-end safety workflow

## Performance Considerations

### Overhead

**Per Invocation**:
- Safety monitor check: <1ms (Q-table lookup)
- Degradation detection: 5-10ms (read last 20 invocations)
- Total overhead: <1% of typical invocation time

**Background Processes**:
- Rollback monitoring: 1-2s per agent (run every 5 min)
- Proposal generation: 5-10s per agent (run weekly)

### Scalability

**Q-table Size**:
- Linear growth with (agents × task_types × variants)
- Typical: 50 agents × 10 task types × 3 variants = 1,500 entries
- Memory: ~1MB for 10,000 entries

**Telemetry Files**:
- Rollback events: ~1KB per event, ~1MB per 1,000 rollbacks
- Variant proposals: ~2KB per proposal, ~2MB per 1,000 proposals
- Cleanup: Archive events older than 1 year

## Best Practices

### 1. Conservative Thresholds

Start with conservative thresholds and relax as confidence grows:

```python
# Initial deployment (very conservative)
monitor = SafetyMonitor(
    auto_apply_q_threshold=0.95,  # Higher than default 0.9
    auto_apply_min_samples=20     # More samples than default 10
)

# After 3 months (moderate)
monitor = SafetyMonitor(
    auto_apply_q_threshold=0.9,   # Default
    auto_apply_min_samples=10     # Default
)
```

### 2. Regular Dashboard Reviews

Check safety dashboard daily:

```bash
# Add to daily standup routine
alias crl-status='python scripts/crl/safety_dashboard.py'

# Or set up automated daily email
cron: 0 9 * * * python scripts/crl/safety_dashboard.py | mail -s "CRL Status" team@example.com
```

### 3. Monitor Rollback Rate

Track rollback frequency as system health metric:

```python
# Alert if >3 rollbacks per week
def check_rollback_rate():
    week_ago = datetime.now() - timedelta(days=7)
    recent_rollbacks = [
        r for r in manager.get_rollback_history()
        if datetime.fromisoformat(r['timestamp'].rstrip('Z')) > week_ago
    ]
    
    if len(recent_rollbacks) > 3:
        send_alert(f"High rollback rate: {len(recent_rollbacks)} in last 7 days")
```

### 4. Review Proposals Weekly

Batch-review variant proposals weekly:

```python
# Every Monday: review pending proposals
def weekly_review():
    proposals = proposer.get_proposals(status="pending")
    
    # Sort by confidence
    proposals.sort(key=lambda x: x['confidence'], reverse=True)
    
    # Review top 5
    for proposal in proposals[:5]:
        # Present to team
        # Approve, reject, or defer
        pass
```

## Troubleshooting

### Issue: False Positive Rollbacks

**Symptom**: Rollbacks triggered despite good performance

**Causes**:
- Insufficient lookback window (too small sample size)
- Temporary performance dip (not sustained)
- Overly aggressive degradation thresholds

**Solutions**:
```python
# Increase lookback window
monitor = SafetyMonitor(lookback_window=50)  # Default: 20

# Relax degradation thresholds (be careful!)
monitor = SafetyMonitor(
    degradation_success_threshold=0.15,  # Default: 0.10
    degradation_reward_threshold=0.20    # Default: 0.15
)
```

### Issue: Variants Not Auto-Applying

**Symptom**: High-performing variants stuck in "human approval"

**Causes**:
- Not enough invocations yet (n < 10)
- Q-value just below threshold (0.85-0.89)
- Recent degradation detected

**Solutions**:
```python
# Check actual Q-value and visits
q_value = q_learning.get_q_value(agent, task, variant)
n_visits = q_learning.get_visit_count(agent, task, variant)

print(f"Q: {q_value:.3f}, Visits: {n_visits}")
# If Q=0.88, n=9: Just needs 1-2 more good invocations

# Temporarily lower threshold (emergency only)
monitor = SafetyMonitor(auto_apply_q_threshold=0.85)
```

### Issue: No Proposals Generated

**Symptom**: Weekly proposal generation returns empty list

**Causes**:
- Not enough invocations across agents (<50 per task type)
- All variants performing well (no gaps or underperformance)
- Min invocation threshold too high

**Solutions**:
```python
# Lower minimum invocation threshold
proposals = proposer.analyze_and_propose(min_invocations=20)  # Default: 50

# Check if any data exists
q_entries = q_learning.get_all_q_values()
print(f"Total Q-table entries: {len(q_entries)}")
```

## Future Enhancements

### Phase 4 (Planned)

1. **A/B Testing Framework**: Compare variant performance head-to-head
2. **Multi-Armed Bandit**: Dynamic variant selection with Thompson sampling
3. **Contextual Learning**: Factor in request context (complexity, urgency, etc.)
4. **Transfer Learning**: Apply learned patterns across similar agents

### Phase 5 (Planned)

1. **Automated Variant Generation**: AI-generated variant modifications
2. **Reinforcement Learning**: Deep RL for variant selection
3. **Federated Learning**: Share learned patterns across installations
4. **Explainable AI**: Interpretable Q-value analysis

## References

- [CRL Architecture](../ARCHITECTURE_CRL.md)
- [Phase 1: Agent Basis](./CRL_PHASE1_GUIDE.md)
- [Phase 2: Q-Learning](./CRL_PHASE2_GUIDE.md)
- [Telemetry System](./TELEMETRY_GUIDE.md)
