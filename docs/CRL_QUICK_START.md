# CRL Quick Start Guide

**Continual Reinforcement Learning for Agent Variant Selection**

This guide shows you how to use the CRL system to automatically select optimal agent variants based on learning from past performance.

---

## What is CRL?

CRL (Continual Reinforcement Learning) automatically learns which agent variant performs best for each task type:

- **Task Classification**: Automatically detects task type (e.g., "api-design", "database-schema")
- **Variant Selection**: Uses Q-learning to select best variant
- **Learning**: Updates Q-values based on performance
- **Improvement**: Continuously improves variant selection over time

---

## Quick Start

### 1. Basic Usage

```python
from core.crl_coordinator import CRLCoordinator

# Initialize CRL system
coordinator = CRLCoordinator()

# Define your agent executor
def my_agent_executor(variant_config, **kwargs):
    # Execute agent with variant configuration
    # variant_config contains: variant_id, model_tier, temperature, etc.
    
    # Your agent execution logic here
    result = execute_my_agent(variant_config)
    
    # Return result dictionary
    return {
        "success": True,
        "quality_score": 0.85,
        "error_count": 0,
        "files_modified": ["src/example.ts"],
        "duration": 120.5
    }

# Execute with CRL
result = coordinator.execute_with_crl(
    agent_name="backend-architect",
    user_request="Create REST API endpoints",
    agent_executor=my_agent_executor,
    file_paths=["src/routes/api.ts"],
    task_complexity="medium"
)

# CRL handles everything automatically:
# 1. Classifies task type
# 2. Selects best variant via Q-learning
# 3. Executes agent
# 4. Calculates reward
# 5. Updates Q-table
# 6. Logs telemetry

print(f"Task: {result['task_type']}")
print(f"Variant: {result['variant_id']}")
print(f"Q-value: {result['q_value']}")
print(f"Reward: {result['reward']}")
```

### 2. View Learning Progress

```bash
# View Q-values for all agents
python scripts/crl/view_q_values.py

# Filter by specific agent
python scripts/crl/view_q_values.py --agent backend-architect

# Filter by task type
python scripts/crl/view_q_values.py --task-type api-design
```

### 3. Monitor Performance

```python
# Get learning statistics
stats = coordinator.get_learning_stats(agent_name="backend-architect")

print(f"Total Q-entries: {stats['total_q_entries']}")
print(f"Total visits: {stats['total_visits']}")
print(f"Average Q-value: {stats['q_value_range']['avg']:.3f}")

# Show agent details
for agent in stats['agents']:
    print(f"\nAgent: {agent['agent_name']}")
    print(f"  Task types learned: {agent['task_types']}")
    print(f"  Variants: {agent['variants']}")
    print(f"  Avg Q-value: {agent['avg_q_value']:.3f}")
```

---

## How It Works

### Workflow

```
User Request
    ↓
1. Task Classification
   "Create REST API" → task_type = "api-design"
    ↓
2. Variant Selection (ε-greedy)
   Q-learning selects variant: "api-optimized"
   10% exploration, 90% exploitation
    ↓
3. Agent Execution
   Execute with variant configuration
    ↓
4. Reward Calculation
   reward = success(40%) + quality(30%) + speed(20%) - errors(10%)
    ↓
5. Q-Table Update
   Q(s,a) ← Q(s,a) + α[R - Q(s,a)]
    ↓
6. Metrics Tracking
   Update variant performance metrics
    ↓
7. Telemetry Logging
   Log with CRL fields for analysis
```

### Components

**Task Classifier** (`core/task_classifier.py`)
- Classifies requests into 10 task types
- Uses keyword matching + file patterns
- 100% accuracy on test suite

**Q-Learning Engine** (`core/q_learning.py`)
- TD(0) algorithm with constant step-size
- ε-greedy exploration (10% exploration, 90% exploitation)
- Persistent Q-table storage
- Thread-safe updates

**Reward Calculator** (`core/reward_calculator.py`)
- Multi-component reward formula
- Weights: Success 40%, Quality 30%, Speed 20%, Errors 10%
- Range: [-1, 1]
- Task complexity aware

**CRL Coordinator** (`core/crl_coordinator.py`)
- Orchestrates complete workflow
- Integrates all CRL components
- Automatic learning and improvement

---

## Configuration

### Q-Learning Parameters

```python
from core.q_learning import QLearningEngine

q_engine = QLearningEngine(
    learning_rate=0.1,      # α - step size (0.1 = 10% of reward)
    exploration_rate=0.1,   # ε - exploration probability (10%)
    qtable_file=Path("custom/location/q_table.jsonl")
)
```

### Reward Weights

```python
from core.reward_calculator import RewardCalculator

reward_calc = RewardCalculator(
    success_weight=0.4,     # 40% weight on success/failure
    quality_weight=0.3,     # 30% weight on quality score
    speed_weight=0.2,       # 20% weight on execution speed
    error_penalty=0.1       # 10% penalty per error
)
```

### Task Complexity Baselines

Speed is normalized by task complexity:
- **Low**: 60 seconds baseline (simple tasks)
- **Medium**: 300 seconds baseline (standard tasks)
- **High**: 900 seconds baseline (complex tasks)

---

## Examples

### Example 1: API Development

```python
coordinator = CRLCoordinator()

result = coordinator.execute_with_crl(
    agent_name="backend-architect",
    user_request="Create REST API for user management",
    agent_executor=execute_backend_agent,
    file_paths=["src/routes/users.ts"],
    task_complexity="medium"
)

# First invocation: Random variant (exploration)
# After 10+ invocations: Optimal variant (exploitation)
```

### Example 2: Database Design

```python
result = coordinator.execute_with_crl(
    agent_name="backend-architect",
    user_request="Design schema for analytics",
    agent_executor=execute_backend_agent,
    file_paths=["migrations/add_analytics.sql"],
    task_complexity="high"
)

# CRL learns: database-focused variant best for database tasks
```

### Example 3: Frontend Development

```python
result = coordinator.execute_with_crl(
    agent_name="frontend-developer",
    user_request="Create login form component",
    agent_executor=execute_frontend_agent,
    file_paths=["src/components/LoginForm.tsx"],
    task_complexity="low"
)

# CRL learns: react-specialist variant best for React tasks
```

---

## Understanding Q-Values

### What is a Q-Value?

Q-value represents **expected reward** for selecting a variant for a task type:

- **Q = 0.0**: No data yet (initial state)
- **Q > 0.5**: Variant performs well
- **Q > 0.7**: Variant performs very well
- **Q < 0.0**: Variant performs poorly
- **Q < -0.5**: Variant performs very poorly

### Learning Curve

**Iteration 1-10**: Exploration phase
- Q-values volatile
- All variants tried
- Learning initial preferences

**Iteration 10-50**: Learning phase
- Best variants emerge
- Q-values converge
- Exploitation increases

**Iteration 50+**: Converged phase
- Stable Q-values
- Optimal variant consistently selected
- 10% exploration continues (adapt to changes)

---

## Monitoring

### Q-Table Location

```
telemetry/crl/q_table.jsonl
```

Each line is a Q-entry:
```json
{
  "state_action": "backend-architect:api-design:api-optimized",
  "q_value": 0.753,
  "n_visits": 45,
  "last_updated": "2025-11-19T22:30:00Z",
  "convergence_score": 0.02
}
```

### Convergence Indicators

**Q-value is converged when**:
- `convergence_score < 0.01` (updates < 1%)
- `n_visits > 10` (sufficient samples)
- Q-value stable across recent invocations

### Dashboard

```bash
python scripts/crl/view_q_values.py
```

Shows:
- Q-values by agent and task type
- Best variant for each task type
- Convergence metrics
- Exploration statistics

---

## Best Practices

### 1. Create Good Variants

Create specialized variants for different task types:

```yaml
# agents/basis/backend-architect/api-optimized.yaml
variant_id: api-optimized
description: Optimized for API design and implementation
specialization:
  - REST API design
  - OpenAPI specifications
  - API security best practices
model_tier: balanced
temperature: 0.7
```

### 2. Provide Quality Feedback

Return accurate quality scores:

```python
def my_agent_executor(variant_config):
    result = execute_agent(variant_config)
    
    # Calculate quality score (0.0-1.0)
    quality = calculate_code_quality(result)
    
    return {
        "success": result.success,
        "quality_score": quality,  # Important for learning
        "error_count": result.errors
    }
```

### 3. Use Appropriate Complexity

Set task complexity accurately:

```python
# Simple task (1-2 files, quick)
result = coordinator.execute_with_crl(
    ...,
    task_complexity="low"
)

# Standard task (3-5 files, moderate)
result = coordinator.execute_with_crl(
    ...,
    task_complexity="medium"
)

# Complex task (6+ files, significant work)
result = coordinator.execute_with_crl(
    ...,
    task_complexity="high"
)
```

### 4. Monitor Learning

Check Q-values periodically:

```bash
# After 10 invocations: Check initial trends
python scripts/crl/view_q_values.py

# After 50 invocations: Verify convergence
python scripts/crl/view_q_values.py --agent backend-architect
```

---

## Troubleshooting

### Problem: All Q-values are 0.0

**Cause**: No invocations yet

**Solution**: Run some CRL invocations first

### Problem: Q-values not converging

**Cause**: Inconsistent rewards

**Solution**:
- Ensure quality scores are accurate
- Check task complexity settings
- Verify agent executor returns correct fields

### Problem: Same variant always selected

**Cause**: One variant significantly better, or all rewards similar

**Solution**:
- Check Q-values: Is one clearly higher?
- Verify variants are actually different
- Try more specialized variants

### Problem: Too much exploration

**Cause**: Default ε=0.1 (10% exploration)

**Solution**: Reduce exploration rate if needed:

```python
q_engine = QLearningEngine(exploration_rate=0.05)  # 5% exploration
```

---

## Advanced Usage

### Custom Agent Executor

```python
def advanced_agent_executor(variant_config, **kwargs):
    # Apply variant-specific configuration
    model_tier = variant_config['model_tier']
    temperature = variant_config['temperature']
    prompt_mods = variant_config['prompt_modifications']
    
    # Configure agent
    agent = create_agent(
        model=get_model_for_tier(model_tier),
        temperature=temperature
    )
    
    # Apply prompt modifications
    for mod in prompt_mods:
        apply_prompt_mod(agent, mod)
    
    # Execute
    result = agent.execute()
    
    # Calculate quality
    quality = run_quality_checks(result)
    
    return {
        "success": result.success,
        "quality_score": quality,
        "error_count": result.error_count,
        "files_modified": result.files_modified,
        "tools_used": result.tools_used
    }
```

### Multi-Agent Workflows

```python
# Agent 1: Design
design_result = coordinator.execute_with_crl(
    agent_name="systems-architect",
    user_request="Design authentication system",
    agent_executor=design_executor
)

# Agent 2: Implementation
impl_result = coordinator.execute_with_crl(
    agent_name="backend-architect",
    user_request="Implement authentication endpoints",
    agent_executor=impl_executor,
    context=design_result
)

# Each agent learns independently
```

---

## Next Steps

1. **Run Examples**:
   ```bash
   python examples/crl_phase2_integration.py
   ```

2. **Create Variants**:
   - Add specialized variants to `agents/basis/<agent-name>/`
   - See `agents/basis/README.md` for format

3. **Integrate with Your System**:
   - Implement your agent executor
   - Integrate CRL coordinator
   - Monitor Q-values

4. **Analyze Results**:
   - View Q-value dashboard
   - Check learning statistics
   - Optimize variant configurations

---

## Resources

**Documentation**:
- Architecture: `docs/CONTINUAL_LEARNING_ARCHITECTURE.md`
- Phase 1 Complete: `PHASE1_COMPLETE.md`
- Phase 2 Complete: `PHASE2_COMPLETE.md`
- Variant Guide: `agents/basis/README.md`

**Code**:
- Q-Learning: `core/q_learning.py`
- Reward Calculator: `core/reward_calculator.py`
- CRL Coordinator: `core/crl_coordinator.py`
- Task Classifier: `core/task_classifier.py`
- Agent Basis: `core/agent_basis.py`

**Examples**:
- Phase 1: `examples/crl_phase1_integration.py`
- Phase 2: `examples/crl_phase2_integration.py`

**Tests**:
- Run all: `./tests/crl/run_phase2_tests.sh`
- Individual: `tests/crl/test_*.py`

---

**Ready to start learning? Run the examples and watch your agents improve!** 🚀
