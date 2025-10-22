# Phase 2A Workflow Tracking Usage Guide

## Overview

Phase 2A adds minimal workflow tracking to telemetry, enabling the Main LLM to link related agent invocations in multi-agent coordination workflows.

## Features

- **Workflow ID**: Unique identifier linking agents in a workflow
- **Parent Invocation ID**: Tracks agent execution sequence
- **Backward Compatible**: Single-agent tasks work unchanged
- **Query Tools**: Shell scripts for workflow analysis

## Usage

### 1. Generate Workflow ID

```python
from telemetry.workflow import generate_workflow_id

# For Main LLM coordination
workflow_id = generate_workflow_id()
# Returns: "wf-20251022-a1b2c3d4"
```

### 2. Multi-Agent Workflow (Main LLM)

```python
from telemetry.logger import TelemetryLogger
from telemetry.workflow import generate_workflow_id

logger = TelemetryLogger()

# Generate workflow ID
workflow_id = generate_workflow_id()

# Agent 1: Design analysis
inv_1 = logger.log_invocation(
    agent_name="design-simplicity-advisor",
    agent_type="meta",
    task_description="Analyze API design",
    workflow_id=workflow_id,
    parent_invocation_id=None  # First agent
)

# Agent 2: Implementation
inv_2 = logger.log_invocation(
    agent_name="backend-architect",
    agent_type="development",
    task_description="Implement API",
    workflow_id=workflow_id,
    parent_invocation_id=inv_1  # Links to Agent 1
)

# Agent 3: Testing
inv_3 = logger.log_invocation(
    agent_name="unit-test-expert",
    agent_type="quality",
    task_description="Create unit tests",
    workflow_id=workflow_id,
    parent_invocation_id=inv_2  # Links to Agent 2
)
```

### 3. Environment Variables (Hook-Based)

When invoking agents via hooks, set environment variables:

```bash
# Main LLM sets workflow context
export OAK_WORKFLOW_ID="wf-20251022-a1b2c3d4"
export OAK_PARENT_INVOCATION_ID="<previous-invocation-id>"

# Invoke agent
./hooks/pre_agent_hook.py backend-architect development "Implement API"
```

### 4. Query Workflows

```bash
# List all workflows
./scripts/query_workflow.sh --list-all

# List today's workflows
./scripts/query_workflow.sh --list-today

# Query specific workflow
./scripts/query_workflow.sh wf-20251022-a1b2c3d4
```

**Output Example**:
```
Workflow: wf-20251022-a1b2c3d4

TIMESTAMP                    AGENT                      STATUS   DURATION
2025-10-22T05:06:43.023829Z  design-simplicity-advisor  success  12.5
2025-10-22T05:06:55.526650Z  backend-architect          success  45.3
2025-10-22T05:07:40.829537Z  unit-test-expert           success  8.2
```

### 5. Single-Agent Tasks (Backward Compatible)

```python
# No workflow tracking needed
inv_id = logger.log_invocation(
    agent_name="general-purpose",
    agent_type="utility",
    task_description="Simple task",
    workflow_id=None  # Single-agent task
)
```

## Schema Changes

### AgentInvocation Schema

```json
{
  "workflow_id": {
    "type": ["string", "null"],
    "description": "Unique identifier linking related agent invocations in a multi-agent workflow"
  }
}
```

### Telemetry Data Example

```json
{
  "timestamp": "2025-10-22T05:06:43.023829Z",
  "session_id": "abc123...",
  "invocation_id": "b0baf654-572f-41f6-b41f-ae00cf31e5ab",
  "agent_name": "design-simplicity-advisor",
  "agent_type": "meta",
  "task_description": "Analyze API design",
  "workflow_id": "wf-20251022-a1b2c3d4",
  "parent_invocation_id": null,
  "tools_used": [],
  "duration_seconds": 12.5,
  "outcome": {
    "status": "success"
  }
}
```

## Testing

Run the complete test suite:

```bash
python3 scripts/test_workflow_tracking.py
```

**Tests Include**:
1. Workflow ID generation
2. Multi-agent workflow logging
3. workflow_id population verification
4. parent_invocation_id linking
5. Query script functionality
6. Backward compatibility

## Integration with CLAUDE.md Workflow

### Main LLM Coordination Pattern

```python
# Step 1: Generate workflow ID
workflow_id = generate_workflow_id()

# Step 2: Log workflow start
logger.log_workflow_start(
    workflow_id=workflow_id,
    project_name="Secure REST API",
    agent_plan=["design-simplicity-advisor", "backend-architect", "security-auditor"],
    estimated_duration=3600
)

# Step 3: Execute agents with handoff tracking
inv_1 = execute_agent("design-simplicity-advisor", workflow_id)

logger.log_agent_handoff(
    workflow_id=workflow_id,
    from_agent="design-simplicity-advisor",
    to_agent="backend-architect",
    artifacts=["artifacts/design-simplicity-advisor/architecture.md"]
)

inv_2 = execute_agent("backend-architect", workflow_id, parent_id=inv_1)

# Step 4: Log workflow completion
logger.log_workflow_complete(
    workflow_id=workflow_id,
    duration_seconds=3200,
    success=True,
    agents_executed=["design-simplicity-advisor", "backend-architect", "security-auditor"]
)
```

## Benefits

- **Workflow Visibility**: Complete tracking of multi-agent coordination
- **Performance Analysis**: Measure workflow duration and bottlenecks
- **Agent Selection**: Historical data guides future agent choices
- **Coordination Overhead**: Measure cost of multi-agent workflows
- **Debugging**: Trace agent execution sequences for failures

## Limitations (Phase 2A)

- No structured artifact tracking (Phase 3)
- No workflow state management (Phase 3)
- No real-time workflow monitoring (Phase 4)
- Manual workflow ID management

## Future Phases

- **Phase 3**: Structured artifact files with validation
- **Phase 4**: Real-time monitoring and workflow visualization
- **Phase 5**: Automatic workflow optimization based on telemetry
