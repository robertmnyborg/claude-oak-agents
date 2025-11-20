# CRL Integration Guide

Complete guide for integrating the Continual Reinforcement Learning (CRL) system into claude-oak-agents.

## Overview

The CRL system enhances the oak-agents framework with intelligent variant selection through reinforcement learning. This guide covers integration steps, configuration, and usage patterns.

## Architecture

```
User Request
    ↓
DomainRouter (CRL-enabled)
    ├─ Domain Detection (existing)
    ├─ Task Classification (new)
    └─ Variant Selection (Q-learning)
    ↓
CRLCoordinator
    ├─ Execute Agent with Variant
    ├─ Calculate Reward
    └─ Update Q-table
    ↓
Result + Learning Metadata
```

## Components

### 1. Domain Router Integration

The `DomainRouter` class now supports CRL-enhanced routing:

```python
from core.domain_router import DomainRouter

# Initialize with CRL enabled (default)
router = DomainRouter(crl_enabled=True)

# Route request with variant selection
routing = router.route_request(
    user_request="Create REST API endpoints for user authentication",
    file_paths=["src/routes/api.ts", "src/controllers/auth.ts"]
)

# Routing result
{
    "agent": "backend-architect",
    "variant": "api-optimized",
    "task_type": "api-design",
    "task_type_confidence": 0.85,
    "q_value": 0.73,
    "exploration": False,
    "domains": [...],
    "crl_enabled": True
}
```

### 2. CRL Coordinator

The `CRLCoordinator` manages the complete CRL workflow:

```python
from core.crl_coordinator import CRLCoordinator

coordinator = CRLCoordinator()

# Execute with CRL
result = coordinator.execute_with_crl(
    agent_name="backend-architect",
    user_request="Create authentication API",
    agent_executor=my_executor_function,
    file_paths=["src/auth/routes.ts"],
    task_complexity="medium"
)

# Result includes learning metadata
{
    "success": True,
    "quality_score": 0.85,
    "task_type": "api-design",
    "variant_id": "api-optimized",
    "q_value": 0.73,
    "exploration": False,
    "reward": 0.78,
    "learning_enabled": True
}
```

### 3. Task Classifier

Classifies user requests into task types:

```python
from core.task_classifier import TaskClassifier

classifier = TaskClassifier()

task_type, confidence, all_scores = classifier.classify_with_confidence(
    user_request="Fix SQL injection vulnerability",
    file_paths=["src/auth/db.ts"]
)

# Returns
# task_type = "security-audit"
# confidence = 0.92
# all_scores = {"security-audit": 0.92, "bug-fix": 0.45, ...}
```

### 4. Q-Learning Engine

Manages variant selection and learning:

```python
from core.q_learning import QLearningEngine

q_engine = QLearningEngine(
    learning_rate=0.1,
    exploration_rate=0.1
)

# Select variant (ε-greedy)
variant_id, q_value, exploration = q_engine.select_variant(
    agent_name="backend-architect",
    task_type="api-design",
    available_variants=["default", "api-optimized", "database-focused"]
)

# Update Q-value after execution
q_engine.update_q_value(
    agent_name="backend-architect",
    task_type="api-design",
    variant_id="api-optimized",
    reward=0.78
)
```

## Integration Steps

### Step 1: Enable CRL in Domain Router

```python
# In your main workflow
from core.domain_router import DomainRouter

# Enable CRL (default)
router = DomainRouter(crl_enabled=True)

# Or disable CRL for comparison
router_no_crl = DomainRouter(crl_enabled=False)
```

### Step 2: Create Agent Variants

Variants are stored in `agents/basis/{agent_name}/{variant_id}.yaml`:

```yaml
# agents/basis/backend-architect/api-optimized.yaml
variant_id: api-optimized
agent_name: backend-architect
description: Optimized for RESTful API design and implementation
specialization:
  - api-design
  - rest-patterns
  - endpoint-security
model_tier: balanced
temperature: 0.7
prompt_modifications:
  - section: "Core Responsibilities"
    operation: append
    content: |
      Focus on RESTful API best practices:
      - Resource-oriented design
      - Proper HTTP methods and status codes
      - API versioning strategies
      - OpenAPI/Swagger documentation
performance_metrics:
  invocation_count: 0
  success_count: 0
  avg_duration: 0.0
  avg_quality_score: 0.0
  avg_reward: 0.0
  last_updated: null
created_at: "2025-11-20T00:00:00Z"
task_type_performance: {}
```

### Step 3: Use CRL Coordinator

```python
from core.crl_coordinator import CRLCoordinator

coordinator = CRLCoordinator()

def my_agent_executor(variant_config, **kwargs):
    """
    Your agent execution logic.
    
    Args:
        variant_config: Dict with variant_id, model_tier, temperature, etc.
        **kwargs: Additional execution parameters
    
    Returns:
        Dict with success, quality_score, error_count, etc.
    """
    # Execute agent with variant configuration
    # ...
    return {
        "success": True,
        "quality_score": 0.85,
        "error_count": 0,
        "files_modified": ["src/api.ts"],
        "tools_used": ["Edit", "Read"]
    }

# Execute with CRL
result = coordinator.execute_with_crl(
    agent_name="backend-architect",
    user_request="Create user management API",
    agent_executor=my_agent_executor,
    file_paths=["src/routes/users.ts"],
    task_complexity="medium"
)
```

### Step 4: Monitor Learning

```python
# Get learning statistics
stats = coordinator.get_learning_stats(agent_name="backend-architect")

print(f"Total invocations: {stats['total_visits']}")
print(f"Q-value range: {stats['q_value_range']}")

for agent_stat in stats['agents']:
    print(f"\nAgent: {agent_stat['agent_name']}")
    print(f"  Task types: {agent_stat['task_types']}")
    print(f"  Variants: {agent_stat['variants']}")
    print(f"  Avg Q-value: {agent_stat['avg_q_value']:.3f}")
```

## Configuration

### CRL Parameters

**Q-Learning Engine** (`core/q_learning.py`):
```python
QLearningEngine(
    learning_rate=0.1,       # α - step size for Q-value updates
    discount_factor=0.9,     # γ - future reward discount (not used in TD(0))
    exploration_rate=0.1     # ε - exploration probability (10%)
)
```

**Reward Calculator** (`core/reward_calculator.py`):
```python
RewardCalculator(
    success_weight=1.0,      # Weight for task success
    quality_weight=0.5,      # Weight for quality score
    time_weight=-0.3,        # Penalty for long duration
    error_weight=-0.5        # Penalty for errors
)
```

### Task Complexity

Task complexity affects reward calculation:
- `"low"`: Simple, low-risk tasks
- `"medium"`: Standard development tasks (default)
- `"high"`: Complex, high-stakes tasks

```python
result = coordinator.execute_with_crl(
    agent_name="backend-architect",
    user_request="Implement OAuth2 flow",
    agent_executor=executor,
    task_complexity="high"  # Higher expectations
)
```

## Disabling CRL

CRL can be disabled without breaking changes:

```python
# Option 1: Disable at router level
router = DomainRouter(crl_enabled=False)
routing = router.route_request(request, files)
# Returns: {"agent": "...", "variant": "default", "crl_enabled": False}

# Option 2: Skip CRL coordinator and use direct agent execution
# (existing workflow continues to work)
```

## Telemetry

CRL integrates with existing telemetry:

```python
from telemetry.logger import TelemetryLogger

logger = TelemetryLogger()

# CRL fields automatically logged
invocation_id = logger.log_invocation(
    agent_name="backend-architect",
    agent_type="development",
    task_description="Create API",
    agent_variant="api-optimized",  # NEW
    task_type="api-design",         # NEW
    q_value=0.73,                   # NEW
    exploration=False,              # NEW
    learning_enabled=True           # NEW
)
```

## Query Tools

### View Q-Values

```bash
python scripts/crl/view_q_values.py --agent backend-architect
python scripts/crl/view_q_values.py --task-type api-design
python scripts/crl/view_q_values.py --top 10
```

### Compare Algorithms

```bash
python scripts/crl/compare_algorithms.py --iterations 100
```

### Safety Dashboard

```bash
python scripts/crl/safety_dashboard.py
```

## Testing

Run CRL tests:

```bash
# All CRL tests
python -m pytest tests/crl/ -v

# Specific test categories
python -m pytest tests/crl/test_q_learning.py -v
python -m pytest tests/crl/test_safety.py -v
python -m pytest tests/crl/test_e2e_integration.py -v
```

## Performance

Target: CRL overhead < 20ms per request

Benchmark performance:

```bash
python scripts/crl/benchmark_system.py
```

Expected metrics:
- **Task classification**: ~5-10ms
- **Variant selection**: ~1-2ms
- **Total overhead**: ~10-15ms

## Troubleshooting

### CRL Not Activating

**Symptom**: `crl_enabled: False` in routing result

**Causes**:
1. CRL explicitly disabled: `DomainRouter(crl_enabled=False)`
2. Missing CRL components (import error)
3. No variants available for agent

**Solution**:
```python
# Check CRL status
router = DomainRouter(crl_enabled=True)
print(f"CRL enabled: {router.crl_enabled}")

# Check variants
from core.agent_basis import AgentBasisManager
manager = AgentBasisManager()
variants = manager.list_variants("backend-architect")
print(f"Available variants: {variants}")
```

### No Learning Observed

**Symptom**: Q-values not updating

**Causes**:
1. Not using `CRLCoordinator.execute_with_crl()`
2. Q-table file permissions
3. Reward calculation issues

**Solution**:
```python
# Verify Q-table location
from core.q_learning import QLearningEngine
q_engine = QLearningEngine()
print(f"Q-table: {q_engine.qtable_file}")

# Check write permissions
import os
print(f"Writable: {os.access(q_engine.qtable_file.parent, os.W_OK)}")

# Manually verify Q-value update
q_before = q_engine.get_q_value("agent", "task", "variant")
q_engine.update_q_value("agent", "task", "variant", reward=1.0)
q_after = q_engine.get_q_value("agent", "task", "variant")
print(f"Q-value: {q_before} → {q_after}")
```

### Task Misclassification

**Symptom**: Wrong task types detected

**Causes**:
1. Insufficient keywords in request
2. Missing file context
3. Ambiguous request

**Solution**:
```python
# Add custom task type
from core.task_classifier import TaskClassifier
classifier = TaskClassifier()

classifier.add_custom_task_type(
    task_type="my-custom-task",
    keywords=["custom", "specific", "keywords"],
    file_patterns=[r".*custom\..*"],
    weight=1.0
)

# Check classification details
task_type, confidence, all_scores = classifier.classify_with_confidence(
    user_request="...",
    file_paths=[...]
)
print(f"Task: {task_type} (confidence: {confidence})")
print(f"All scores: {all_scores}")
```

## Next Steps

1. **Review Examples**: See `examples/crl_phase1_integration.py` through `examples/crl_phase4_advanced.py`
2. **Read Architecture**: See `docs/CRL_ARCHITECTURE.md`
3. **Check Deployment**: See `docs/CRL_DEPLOYMENT.md`
4. **Run Validation**: `python scripts/crl/validate_system.py`

## Support

For issues or questions:
1. Check `docs/CRL_TROUBLESHOOTING.md`
2. Review test examples in `tests/crl/`
3. Run system validation: `scripts/crl/validate_system.py`
