# Agent Basis System - Continual Reinforcement Learning

## Overview

The Agent Basis System manages **agent variants** - specialized configurations of base agents optimized for specific task types. This enables continual reinforcement learning (CRL) where the system learns which agent variant performs best for each type of task.

## Variant System

### What is an Agent Variant?

An agent variant is a specialized version of a base agent with:
- **Prompt modifications**: Additions or changes to the agent's instructions
- **Model configuration**: Temperature and tier settings
- **Specialization tags**: Task types this variant excels at
- **Performance history**: Metrics tracking success, quality, and rewards

### Why Use Variants?

Instead of a single "backend-architect" agent, we can have:
- `backend-architect:default` - General backend work
- `backend-architect:api-optimized` - Specialized for REST API design
- `backend-architect:database-focused` - Specialized for database schema work

The system learns over time which variant works best for each task type and automatically selects the optimal variant.

## Directory Structure

```
agents/basis/
├── README.md                      # This file
├── backend-architect/
│   ├── default.yaml              # Default variant
│   ├── api-optimized.yaml        # API design specialist
│   └── database-focused.yaml     # Database schema specialist
├── frontend-developer/
│   ├── default.yaml              # Default variant
│   ├── react-specialist.yaml     # React/TypeScript specialist
│   └── vue-specialist.yaml       # Vue.js specialist
├── security-auditor/
│   └── default.yaml              # Default variant
├── infrastructure-specialist/
│   └── default.yaml              # Default variant
└── general-purpose/
    └── default.yaml              # Default variant
```

## Variant YAML Schema

Each variant is defined in a YAML file with this structure:

```yaml
variant_id: "api-optimized"          # Unique identifier
agent_name: "backend-architect"      # Base agent name
description: "Optimized for REST API design"
specialization:                      # Task types this variant excels at
  - api-design
  - rest
  - openapi
model_tier: "balanced"               # fast | balanced | premium
temperature: 0.6                     # Model sampling temperature (0.0-1.0)
prompt_modifications:                # Changes to base agent prompt
  - section: "Core Responsibilities"
    operation: "append"              # append | prepend | replace
    content: |
      Additional focus on API design best practices...
performance_metrics:                 # Tracked automatically
  invocation_count: 0
  success_count: 0
  avg_duration: 0.0
  avg_quality_score: 0.0
  avg_reward: 0.0
  last_updated: null
created_at: "2025-11-19T00:00:00Z"
task_type_performance: {}            # Per-task-type metrics
```

## Creating New Variants

### Method 1: Programmatic (Recommended)

```python
from core.agent_basis import AgentBasisManager, PromptModification

manager = AgentBasisManager()

# Create new variant
variant = manager.create_variant(
    agent_name="backend-architect",
    variant_id="performance-focused",
    description="Specialized for performance optimization tasks",
    specialization=["performance-opt", "caching", "query-optimization"],
    model_tier="balanced",
    temperature=0.5,
    prompt_modifications=[
        PromptModification(
            section="Core Responsibilities",
            operation="append",
            content="Focus on performance optimization patterns..."
        )
    ]
)
```

### Method 2: Manual YAML Creation

1. Create new file in appropriate agent directory
2. Copy structure from existing variant
3. Modify fields as needed
4. Test with `core/agent_basis.py`

## How Variants Are Selected

### Phase 1 (Current): Manual Selection
- Variants can be loaded and used explicitly
- Performance metrics are tracked
- Foundation for automated selection

### Phase 2 (Future): Q-Learning Selection
- System classifies user request into task type
- Q-learning algorithm selects best variant based on historical performance
- 10% exploration rate to discover better variants
- Continuous improvement as more data is collected

## Performance Tracking

Metrics are updated automatically for each variant:

```python
manager.update_metrics(
    agent_name="backend-architect",
    variant_id="api-optimized",
    success=True,
    duration=120.5,
    quality_score=0.85,  # 0.0-1.0 scale
    reward=2.1,          # Calculated reward signal
    task_type="api-design"
)
```

### Metrics Tracked

**Overall Metrics**:
- `invocation_count`: Total number of times used
- `success_count`: Number of successful invocations
- `avg_duration`: Average execution time (seconds)
- `avg_quality_score`: Average quality rating (0.0-1.0)
- `avg_reward`: Average reward signal for Q-learning

**Task-Type-Specific Metrics**:
- Same metrics broken down by task type
- Enables task-specific variant selection

## Best Variant Selection

Query for best-performing variant:

```python
# Get best variant for specific task type
best_variant = manager.get_best_variant_for_task(
    agent_name="backend-architect",
    task_type="api-design",
    min_sample_count=5  # Require at least 5 samples
)

# Returns: "api-optimized" (if it has best avg_reward)
```

## Integration with Telemetry

Variant information is logged in telemetry:

```json
{
  "invocation_id": "inv-20251119-abc123",
  "agent_name": "backend-architect",
  "agent_variant": "api-optimized",
  "task_type": "api-design",
  "q_value": 0.85,
  "exploration": false,
  "reward": 2.1,
  "learning_enabled": true
}
```

This enables:
- Performance analysis by variant
- Q-learning training data
- Variant effectiveness comparison

## Example Variants

### backend-architect

- **default**: General backend work, balanced approach
- **api-optimized**: REST API design, OpenAPI docs, routing patterns
- **database-focused**: Schema design, migrations, query optimization

### frontend-developer

- **default**: General frontend work, framework-agnostic
- **react-specialist**: React hooks, TypeScript, modern React patterns
- **vue-specialist**: Vue 3 Composition API, Pinia, SFC patterns

## Variant Design Guidelines

### When to Create a New Variant

Create a new variant when:
- Existing variant performs poorly on specific task type (avg_reward < 0.5)
- Clear specialization opportunity (e.g., GraphQL vs REST)
- Different prompt focus significantly improves outcomes
- Task type has distinct requirements from general work

### When NOT to Create a New Variant

Avoid creating variants for:
- Minor prompt tweaks (iterate on existing variant instead)
- Insufficient sample size (need 10+ invocations to validate)
- Overlapping specializations (consolidate similar variants)
- One-off tasks (use general variant)

### Variant Naming Conventions

- Use descriptive, hyphenated lowercase: `api-optimized`
- Reflect specialization: `database-focused`, `react-specialist`
- Avoid version numbers in variant_id (track in description if needed)
- Keep IDs under 30 characters

## Maintenance

### Archiving Underperforming Variants

If a variant consistently underperforms:

```python
# Move to archive subdirectory
mv agents/basis/backend-architect/old-variant.yaml \
   agents/basis/backend-architect/archived/
```

### Merging Similar Variants

If two variants have >80% overlap:
1. Choose best-performing variant
2. Merge prompt modifications
3. Update specialization tags
4. Archive redundant variant

## Future Enhancements (Phase 2+)

- **Automatic variant creation**: System proposes new variants when detecting performance gaps
- **Variant mutation**: Evolutionary algorithm to optimize prompt modifications
- **Transfer learning**: Share knowledge between similar task types
- **Contextual variants**: Consider file types, frameworks, project size
- **A/B testing**: Compare variant performance head-to-head

## Troubleshooting

### Variant Not Found
```
ValueError: Variant backend-architect:api-optimized not found
```
**Solution**: Check file exists at `agents/basis/backend-architect/api-optimized.yaml`

### Metrics Not Updating
**Solution**: Ensure `update_metrics()` is called after each invocation with correct variant_id

### Low Confidence Selection
If Q-learning never selects a variant:
- Check `min_sample_count` threshold (default: 5)
- Verify variant has positive `avg_reward`
- Ensure task_type matches specialization tags

## Additional Resources

- **Architecture**: See `docs/CONTINUAL_LEARNING_ARCHITECTURE.md`
- **Q-Learning**: Phase 2 implementation (coming soon)
- **Telemetry**: See `telemetry/logger.py` for CRL field documentation
- **Task Classifier**: See `core/task_classifier.py` for task type detection
