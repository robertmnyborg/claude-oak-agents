# Phase 2 Quick Start Guide

## Installation

No installation required - Phase 2 extends existing telemetry with stdlib-only code.

## Quick Examples

### 1. Track a Multi-Agent Workflow (5 lines)

```python
from telemetry.logger import TelemetryLogger

logger = TelemetryLogger()

# Start workflow
logger.log_workflow_start("wf-001", "My Project", ["agent-1", "agent-2"])

# Log handoffs between agents
logger.log_agent_handoff("wf-001", "agent-1", "agent-2", ["output.md"])

# Complete workflow  
logger.log_workflow_complete("wf-001", duration_seconds=3600, success=True, agents_executed=["agent-1", "agent-2"])
```

### 2. Query Best Agent (1 command)

```bash
python3 scripts/query_best_agent.py --task "API development" --domain "backend"
```

Output:
```
Recommended Agent: backend-architect
   Confidence: 85%
   Success Rate: 92%
   Avg Duration: 47.5 min
   Total Tasks: 12
   Trend: improving
```

### 3. Analyze Coordination Overhead (3 lines)

```python
from telemetry.analyzer import TelemetryAnalyzer

analyzer = TelemetryAnalyzer()
overhead = analyzer.calculate_coordination_overhead()

print(f"Overhead: {overhead['coordination_overhead_pct']:.1f}%")
print(f"Recommendation: {overhead['recommendation']}")
```

### 4. Check Agent Performance Trends (2 lines)

```python
trend = analyzer.get_agent_performance_trends("backend-architect", days=30)
print(f"{trend['trend']}: {trend['success_rate_change']:.1%} change")
```

## Common Workflows

### Workflow Pattern 1: Sequential Agents

```python
logger.log_workflow_start("seq-001", "Backend API", ["backend-architect", "security-auditor", "qa-specialist"])

# Agent 1: backend-architect
# ... work happens ...
logger.log_agent_handoff("seq-001", "backend-architect", "security-auditor", ["src/api/"])

# Agent 2: security-auditor  
# ... work happens ...
logger.log_agent_handoff("seq-001", "security-auditor", "qa-specialist", ["reports/audit.md"])

# Agent 3: qa-specialist
# ... work happens ...
logger.log_workflow_complete("seq-001", 7200, True, ["backend-architect", "security-auditor", "qa-specialist"])
```

### Workflow Pattern 2: Parallel Analysis

```python
# Start workflow with parallel agents
logger.log_workflow_start("par-001", "Code Review", 
    ["security-auditor", "performance-optimizer", "code-reviewer"])

# Each agent works independently (no handoffs needed for parallel work)
# ... agents execute in parallel ...

# Complete with all agents
logger.log_workflow_complete("par-001", 1800, True, 
    ["security-auditor", "performance-optimizer", "code-reviewer"])
```

### Workflow Pattern 3: Conditional Agents

```python
logger.log_workflow_start("cond-001", "Feature Dev", 
    ["frontend-developer", "backend-architect?", "qa-specialist"])

# Agent 1 completes
# Decision point: Do we need backend changes?
needs_backend = check_backend_changes()

if needs_backend:
    logger.log_agent_handoff("cond-001", "frontend-developer", "backend-architect", ["requirements.md"])
    # ... backend work ...
    logger.log_agent_handoff("cond-001", "backend-architect", "qa-specialist", ["src/api/"])
else:
    logger.log_agent_handoff("cond-001", "frontend-developer", "qa-specialist", ["src/components/"])

# Complete with actual agents executed
executed = ["frontend-developer", "qa-specialist"]
if needs_backend:
    executed.insert(1, "backend-architect")
    
logger.log_workflow_complete("cond-001", 5400, True, executed)
```

## CLI Commands

### Query Best Agent

```bash
# Basic query
python3 scripts/query_best_agent.py --task "security audit"

# With domain filter
python3 scripts/query_best_agent.py --task "API design" --domain "backend"

# Lower confidence threshold
python3 scripts/query_best_agent.py --task "database" --min-confidence 0.3

# Show all matching agents
python3 scripts/query_best_agent.py --task "testing" --all
```

### Run Demo

```bash
# Full interactive demo
python3 scripts/demo_workflow_coordination.py

# Run tests
python3 tests/test_workflow_tracking.py
```

## Analysis Workflows

### Daily Workflow Review

```python
from telemetry.analyzer import TelemetryAnalyzer

analyzer = TelemetryAnalyzer()

# Check today's workflows
stats = analyzer.analyze_workflows()
print(f"Workflows today: {stats['total_workflows']}")
print(f"Success rate: {stats['success_rate']:.0%}")

# Common patterns
for pattern in stats['most_common_patterns'][:3]:
    print(f"{pattern['pattern']}: {pattern['count']} times")
```

### Weekly Performance Review

```python
# Check each agent's trend
for agent in ["backend-architect", "frontend-developer", "security-auditor"]:
    trend = analyzer.get_agent_performance_trends(agent, days=7)
    
    if trend['trend'] == 'declining':
        print(f"⚠️  {agent}: Performance declining ({trend['success_rate_change']:.1%})")
    elif trend['trend'] == 'improving':
        print(f"✓ {agent}: Performance improving ({trend['success_rate_change']:.1%})")
```

### Monthly Coordination Review

```python
# Analyze coordination overhead
overhead = analyzer.calculate_coordination_overhead()

print(f"Coordination Overhead: {overhead['coordination_overhead_pct']:.1f}%")
print(f"Avg Coordination Time: {overhead['avg_coordination_minutes']:.1f} min/workflow")

# Decide on Phase 3
if overhead['coordination_overhead_pct'] > 30:
    print("\n🚀 Consider implementing Phase 3:")
    print("  - Shared working memory")
    print("  - Automated agent delegation")
    print("  - Real-time conflict resolution")
elif overhead['coordination_overhead_pct'] > 15:
    print("\n📊 Monitor coordination overhead")
else:
    print("\n✓ Current coordination is efficient")
```

## Integration with Existing Code

### Add to Agent Invocation Wrapper

```python
def invoke_agent(agent_name, task, workflow_id=None, previous_agent=None, artifacts=None):
    """Wrapper that logs workflow events automatically."""
    
    logger = TelemetryLogger()
    
    # Log handoff if part of workflow
    if workflow_id and previous_agent:
        logger.log_agent_handoff(workflow_id, previous_agent, agent_name, artifacts or [])
    
    # Regular agent invocation logging
    inv_id = logger.log_invocation(agent_name, "development", task)
    
    # ... execute agent ...
    
    logger.update_invocation(inv_id, duration_seconds=duration, outcome_status="success")
    
    return result
```

### Main LLM Workflow Coordinator

```python
class WorkflowCoordinator:
    def __init__(self):
        self.logger = TelemetryLogger()
        self.analyzer = TelemetryAnalyzer()
        
    def execute_workflow(self, project_name, agent_plan):
        """Execute multi-agent workflow with tracking."""
        
        workflow_id = f"wf-{int(time.time())}"
        
        # Start workflow
        self.logger.log_workflow_start(workflow_id, project_name, agent_plan)
        
        agents_executed = []
        artifacts = []
        
        for i, agent_name in enumerate(agent_plan):
            # Get best agent for this step (optional)
            # recommendation = query_best_agent(...)
            
            # Execute agent
            result = self.execute_agent(agent_name)
            agents_executed.append(agent_name)
            artifacts.extend(result.artifacts)
            
            # Log handoff to next agent
            if i < len(agent_plan) - 1:
                self.logger.log_agent_handoff(
                    workflow_id, 
                    agent_name, 
                    agent_plan[i + 1],
                    artifacts
                )
        
        # Complete workflow
        self.logger.log_workflow_complete(
            workflow_id,
            duration_seconds=total_duration,
            success=True,
            agents_executed=agents_executed
        )
        
        return result
```

## Troubleshooting

### No suitable agent found

```bash
# Try lowering confidence threshold
python3 scripts/query_best_agent.py --task "..." --min-confidence 0.2

# Try removing domain filter
python3 scripts/query_best_agent.py --task "..."

# Check if telemetry data exists
ls -lh telemetry/agent_invocations.jsonl
```

### Insufficient data for trends

Agent performance trends require at least 2 invocations. Create more historical data or adjust time window:

```python
# Shorter time window
trend = analyzer.get_agent_performance_trends("agent-name", days=7)
```

### Negative coordination overhead

This is normal when agents run in parallel - it means the sum of individual agent times exceeds the total workflow time (efficient parallelization).

## Best Practices

1. **Unique Workflow IDs**: Use timestamps or UUIDs
   ```python
   import uuid
   workflow_id = f"wf-{uuid.uuid4()}"
   ```

2. **Descriptive Project Names**: Use clear, searchable names
   ```python
   logger.log_workflow_start("wf-001", "E-Commerce API v2.0", ...)
   ```

3. **Complete Agent Lists**: Always specify full agent plan upfront
   ```python
   agent_plan = ["systems-architect", "backend-architect", "frontend-developer"]
   ```

4. **Log All Handoffs**: Track every artifact exchange
   ```python
   logger.log_agent_handoff(wf_id, from_agent, to_agent, ["file1.md", "file2.sql"])
   ```

5. **Always Complete Workflows**: Even failed workflows should be logged
   ```python
   logger.log_workflow_complete(wf_id, duration, success=False, agents_executed)
   ```

## Next Steps

- Read [PHASE2_WORKFLOW_COORDINATION.md](PHASE2_WORKFLOW_COORDINATION.md) for full documentation
- Run `python3 scripts/demo_workflow_coordination.py` for interactive demo
- Check `examples/workflow_coordination_example.py` for practical examples
- Review `tests/test_workflow_tracking.py` for comprehensive test cases

## Support

File issues or questions in the project repository.
