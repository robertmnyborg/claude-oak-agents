# Phase 2: Multi-Agent Workflow Coordination

## Overview

Phase 2 extends the OaK telemetry system with workflow-level tracking and agent selection capabilities. This enables coordinated multi-agent workflows while maintaining the KISS principle.

## New Features

### 1. Workflow Tracking

Track complete multi-agent workflows from start to finish:

```python
from telemetry.logger import TelemetryLogger

logger = TelemetryLogger()

# Start workflow
logger.log_workflow_start(
    workflow_id="ecommerce-mvp-001",
    project_name="E-Commerce Platform MVP",
    agent_plan=["systems-architect", "backend-architect", "frontend-developer"],
    estimated_duration=7200  # 2 hours
)

# Log agent handoffs
logger.log_agent_handoff(
    workflow_id="ecommerce-mvp-001",
    from_agent="systems-architect",
    to_agent="backend-architect",
    artifacts=["artifacts/architecture.md", "artifacts/tech-stack.md"]
)

# Complete workflow
logger.log_workflow_complete(
    workflow_id="ecommerce-mvp-001",
    duration_seconds=6500,
    success=True,
    agents_executed=["systems-architect", "backend-architect", "frontend-developer"]
)
```

### 2. Agent Selection Queries

Query historical telemetry to recommend the best agent for a task:

```bash
# CLI usage
python3 scripts/query_best_agent.py --task "API development" --domain "backend"
python3 scripts/query_best_agent.py --task "security audit"
python3 scripts/query_best_agent.py --task "database design" --domain "backend" --all
```

```python
# Programmatic usage
from scripts.query_best_agent import query_best_agent

recommendation = query_best_agent(
    task_description="API development",
    domain="backend",
    min_confidence=0.5
)

if recommendation:
    print(f"Agent: {recommendation.agent_name}")
    print(f"Confidence: {recommendation.confidence:.0%}")
    print(f"Success Rate: {recommendation.success_rate:.0%}")
    print(f"Avg Duration: {recommendation.avg_duration_minutes:.1f} min")
    print(f"Experience: {recommendation.total_tasks} tasks")
    print(f"Trend: {recommendation.recent_performance}")
```

### 3. Coordination Analysis

Analyze workflow performance and coordination overhead:

```python
from telemetry.analyzer import TelemetryAnalyzer

analyzer = TelemetryAnalyzer()

# Analyze workflows
workflow_stats = analyzer.analyze_workflows()
print(f"Total Workflows: {workflow_stats['total_workflows']}")
print(f"Success Rate: {workflow_stats['success_rate']:.0%}")
print(f"Avg Duration: {workflow_stats['avg_duration_minutes']:.1f} min")
print(f"Avg Agents: {workflow_stats['avg_agents_per_workflow']:.1f}")

# Most common agent patterns
for pattern in workflow_stats['most_common_patterns']:
    print(f"{pattern['pattern']}: {pattern['count']} times")

# Calculate coordination overhead
overhead = analyzer.calculate_coordination_overhead()
print(f"Coordination Overhead: {overhead['coordination_overhead_pct']:.1f}%")
print(f"Recommendation: {overhead['recommendation']}")
```

### 4. Performance Trends

Analyze agent performance trends over time:

```python
trend = analyzer.get_agent_performance_trends("backend-architect", days=30)
print(f"Trend: {trend['trend']}")  # "improving", "stable", or "declining"
print(f"Recent Success Rate: {trend['recent_success_rate']:.0%}")
print(f"Historical Success Rate: {trend['historical_success_rate']:.0%}")
print(f"Change: {trend['success_rate_change']:.1%}")
```

## Data Format

### workflow_events.jsonl

Logs workflow lifecycle events:

```json
{"timestamp": "2025-10-21T10:00:00Z", "event": "workflow_start", "workflow_id": "wf-001", "project_name": "E-Commerce", "agent_plan": ["backend-architect", "frontend-developer"], "estimated_duration": 3600}
{"timestamp": "2025-10-21T10:45:00Z", "event": "agent_handoff", "workflow_id": "wf-001", "from_agent": "backend-architect", "to_agent": "frontend-developer", "artifacts": ["artifacts/api-spec.yaml"]}
{"timestamp": "2025-10-21T11:30:00Z", "event": "workflow_complete", "workflow_id": "wf-001", "duration_seconds": 5400, "success": true, "agents_executed": ["backend-architect", "frontend-developer"]}
```

## New TelemetryLogger Methods

### log_workflow_start()

```python
def log_workflow_start(
    workflow_id: str,
    project_name: str,
    agent_plan: List[str],
    estimated_duration: Optional[int] = None
) -> None
```

Logs the start of a multi-agent workflow.

**Args:**
- `workflow_id`: Unique identifier for this workflow
- `project_name`: Human-readable project name
- `agent_plan`: List of agent names in execution order
- `estimated_duration`: Optional estimated duration in seconds

### log_agent_handoff()

```python
def log_agent_handoff(
    workflow_id: str,
    from_agent: str,
    to_agent: str,
    artifacts: List[str]
) -> None
```

Logs artifact handoff between agents.

**Args:**
- `workflow_id`: Workflow this handoff belongs to
- `from_agent`: Agent that produced artifacts
- `to_agent`: Agent that will consume artifacts
- `artifacts`: List of artifact file paths

### log_workflow_complete()

```python
def log_workflow_complete(
    workflow_id: str,
    duration_seconds: int,
    success: bool,
    agents_executed: List[str]
) -> None
```

Logs workflow completion.

**Args:**
- `workflow_id`: Workflow that completed
- `duration_seconds`: Total workflow duration
- `success`: Whether workflow succeeded
- `agents_executed`: List of agents that actually ran

## New TelemetryAnalyzer Methods

### analyze_workflows()

```python
def analyze_workflows() -> Dict[str, Any]
```

Analyze multi-agent workflow performance.

**Returns:**
- `total_workflows`: Number of workflows executed
- `avg_duration_minutes`: Average workflow duration
- `success_rate`: Percentage of successful workflows
- `avg_agents_per_workflow`: Average number of agents
- `most_common_patterns`: List of common agent sequences

### calculate_coordination_overhead()

```python
def calculate_coordination_overhead() -> Dict[str, Any]
```

Calculate coordination overhead percentage.

**Formula:**
```
Coordination overhead = (Total workflow time - Sum of agent execution time) / Total workflow time
```

**Returns:**
- `coordination_overhead_pct`: Percentage of time spent coordinating
- `recommendation`: "Stay Phase 1-2" or "Consider Phase 3"
- `avg_coordination_minutes`: Average coordination time per workflow

**Recommendations:**
- `< 15%`: Stay Phase 1-2 (Efficient coordination)
- `15-30%`: Monitor overhead (Moderate coordination time)
- `> 30%`: Consider Phase 3 (High coordination overhead)

### get_agent_performance_trends()

```python
def get_agent_performance_trends(
    agent_name: str,
    days: int = 30
) -> Dict[str, Any]
```

Analyze agent performance trends over time.

**Args:**
- `agent_name`: Name of agent to analyze
- `days`: Number of days to look back (default: 30)

**Returns:**
- `trend`: "improving", "stable", or "declining"
- `success_rate_change`: Percentage point change
- `recent_success_rate`: Success rate in last 7 days
- `historical_success_rate`: Success rate in prior period

## Testing

Run the comprehensive test suite:

```bash
# Test workflow tracking
python3 tests/test_workflow_tracking.py

# Run demo
python3 scripts/demo_workflow_coordination.py
```

## Use Cases

### 1. Multi-Agent Project Workflows

Track complex projects involving multiple specialized agents:

```python
# Start project
logger.log_workflow_start(
    workflow_id="project-001",
    project_name="Microservices API Platform",
    agent_plan=[
        "systems-architect",
        "backend-architect",
        "security-auditor",
        "infrastructure-specialist",
        "qa-specialist"
    ],
    estimated_duration=28800  # 8 hours
)

# Each agent logs their work
# Main LLM coordinates handoffs between agents
# Track final completion
```

### 2. Agent Performance Optimization

Identify underperforming agents and improvement opportunities:

```python
# Analyze all agents
stats = analyzer.generate_statistics()

for agent_name, agent_stats in stats["agents"].items():
    if agent_stats["success_rate"] < 0.7:
        print(f"Low performer: {agent_name}")
        
        # Get trends
        trend = analyzer.get_agent_performance_trends(agent_name)
        if trend["trend"] == "declining":
            print(f"  WARNING: Performance declining!")
```

### 3. Coordination Phase Decisions

Use coordination overhead to decide when to upgrade from Phase 2 to Phase 3:

```python
overhead = analyzer.calculate_coordination_overhead()

if overhead["coordination_overhead_pct"] > 30:
    print("High coordination overhead detected")
    print("Consider implementing Phase 3 features:")
    print("  - Shared working memory")
    print("  - Automated agent delegation")
    print("  - Real-time conflict resolution")
```

### 4. Historical Agent Selection

Let the system recommend agents based on historical performance:

```python
# User wants to add a new feature
task = "Implement OAuth2 authentication"
domain = "security"

recommendation = query_best_agent(task, domain)

if recommendation:
    print(f"Recommended: {recommendation.agent_name}")
    print(f"Based on {recommendation.total_tasks} similar tasks")
    print(f"Success rate: {recommendation.success_rate:.0%}")
else:
    print("No suitable agent found - consider creating a new specialist")
```

## Architecture Decisions

### Why JSONL for Workflow Events?

1. **Append-only**: No file rewrites required
2. **Simple parsing**: One event per line
3. **Fault tolerant**: Corruption affects only one line
4. **Stream friendly**: Can process events as they arrive
5. **No dependencies**: Uses only Python stdlib

### Why Separate Workflow Events File?

1. **Clear separation**: Workflow-level vs agent-level tracking
2. **Performance**: Don't rewrite agent invocations for workflow events
3. **Scalability**: Workflow events are lower volume
4. **Backward compatibility**: Existing telemetry unchanged

### Coordination Overhead Calculation

The overhead calculation measures time spent coordinating between agents:

- **Positive overhead**: Time spent on handoffs, planning, integration
- **Negative overhead**: Agents ran in parallel or had overlapping execution
- **Zero overhead**: Perfect sequential execution with no coordination time

This metric helps determine if coordination complexity justifies moving to Phase 3.

## Limitations

1. **No real-time coordination**: Events logged after completion
2. **Manual workflow ID management**: Caller must generate unique IDs
3. **No workflow cancellation tracking**: Only tracks completion
4. **Session-based correlation**: Relies on session IDs for overhead calculation

## Future Enhancements (Phase 3)

- Shared working memory across agents
- Real-time workflow state tracking
- Automated conflict resolution
- Dynamic agent selection based on current state
- Workflow templates and patterns
- Resource allocation and scheduling

## Complexity Budget

Total complexity: **12 points** (within ≤15 KISS compliance)

- Workflow tracking methods: 3 points (3 simple append operations)
- Agent selection query: 4 points (keyword extraction, scoring, ranking)
- Workflow analysis: 3 points (grouping, aggregation, statistics)
- Coordination overhead: 2 points (time calculation, threshold logic)

## References

- See `tests/test_workflow_tracking.py` for comprehensive examples
- See `scripts/demo_workflow_coordination.py` for interactive demo
- See `telemetry/README.md` for existing telemetry documentation
