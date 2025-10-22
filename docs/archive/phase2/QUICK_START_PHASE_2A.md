# Quick Start: Phase 2A Workflow Tracking

## What Changed?

Phase 2A adds **minimal workflow tracking** to telemetry. Now multi-agent workflows can be linked and queried.

## For Main LLM (Coordination)

```python
from telemetry.workflow import generate_workflow_id
from telemetry.logger import TelemetryLogger

# 1. Generate workflow ID
workflow_id = generate_workflow_id()  # wf-20251022-a1b2c3d4

logger = TelemetryLogger()

# 2. Log first agent
inv_1 = logger.log_invocation(
    agent_name="design-simplicity-advisor",
    agent_type="meta",
    task_description="Analyze design",
    workflow_id=workflow_id
)

# 3. Log subsequent agents (linked)
inv_2 = logger.log_invocation(
    agent_name="backend-architect",
    agent_type="development",
    task_description="Implement API",
    workflow_id=workflow_id,
    parent_invocation_id=inv_1  # Links to previous agent
)
```

## For Single-Agent Tasks (No Change)

```python
# Works exactly as before
inv_id = logger.log_invocation(
    agent_name="general-purpose",
    agent_type="utility",
    task_description="Simple task"
    # workflow_id defaults to None
)
```

## Environment Variables (Hook-Based)

```bash
# Main LLM sets before invoking agents
export OAK_WORKFLOW_ID="wf-20251022-a1b2c3d4"
export OAK_PARENT_INVOCATION_ID="<previous-invocation-id>"

# Hook automatically reads and applies
./hooks/pre_agent_hook.py backend-architect development "Implement API"
```

## Query Workflows

```bash
# List all workflows
./scripts/query_workflow.sh --list-all

# List today's workflows
./scripts/query_workflow.sh --list-today

# View specific workflow
./scripts/query_workflow.sh wf-20251022-a1b2c3d4
```

## Test Everything

```bash
# Run comprehensive test suite
python3 scripts/test_workflow_tracking.py

# Should output: 6/6 tests PASSED
```

## Key Files

| File | Purpose |
|------|---------|
| `telemetry/workflow.py` | Workflow ID generator |
| `telemetry/schemas.json` | Updated schema with workflow_id |
| `telemetry/logger.py` | Updated logger with workflow_id param |
| `hooks/pre_agent_hook.py` | Reads OAK_WORKFLOW_ID from env |
| `scripts/query_workflow.sh` | Query workflows |
| `scripts/test_workflow_tracking.py` | Test suite |
| `docs/workflow_tracking_usage.md` | Complete usage guide |

## No Breaking Changes

- ✓ Existing invocations work unchanged
- ✓ Single-agent tasks need no modification
- ✓ workflow_id is optional (defaults to None)
- ✓ Backward compatible telemetry format

## Next: Phase 3

Phase 3 will add **structured artifact files** with validation and lineage tracking.

For now, Phase 2A provides:
- Workflow linking via IDs
- Agent sequence tracking
- Query tools for analysis
- Foundation for data-driven agent selection
