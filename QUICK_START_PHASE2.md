# Phase 2 Workflow Coordination - Quick Start Guide

## What's New in Phase 2?

Phase 2 adds **data-driven agent selection** and **multi-agent workflow tracking** to the OaK system.

### Key Features

1. **Agent Selection**: Query historical performance to find the best agent for each task
2. **Workflow Tracking**: Track multi-agent coordination from start to finish
3. **Coordination Analysis**: Measure overhead and identify bottlenecks
4. **Performance Trends**: Monitor agent improvements over time
5. **Shell Integration**: Easy access via `oak-*` commands

## Quick Commands

### View Recent Workflows

```bash
oak-workflows
```

**Output Example**:
```
Total Workflows: 5
Success Rate: 100%
Avg Duration: 145.2 minutes
Avg Agents/Workflow: 4.2

Common Agent Patterns:
  systems-architect→backend-architect→frontend-developer (3x)
  
Coordination Overhead: 15.3%
Recommendation: Stay Phase 1-2 (Efficient coordination)
```

### Query Best Agent for a Task

```bash
# Query for backend task
oak-query-agent "REST API development" backend

# Query without domain filter
oak-query-agent "security audit"
```

**Output Example**:
```
Recommended Agent: backend-architect
   Confidence: 88%
   Success Rate: 92%
   Avg Duration: 75.0 min
   Total Tasks: 12
   Trend: stable
```

### View Agent Performance Trends

```bash
oak-agent-trends backend-architect
```

**Output Example**:
```
Performance Trends: backend-architect
============================================================
Trend: improving
Recent Success Rate (7 days): 95%
Historical Success Rate: 88%
Change: +0.07 percentage points
```

### Run Weekly Review (includes workflow analysis)

```bash
oak-weekly-review
```

### Run Monthly Analysis (includes performance trends)

```bash
oak-monthly-review
```

### View All Commands

```bash
oak-help
```

## For Main LLM: How to Track Workflows

### When to Track Workflows

Track workflows when:
- **COORDINATION** classification detected
- **2+ agents** required
- **Complex project** with sequential/parallel execution

### Workflow Tracking Steps

1. **Generate Workflow ID**
```python
workflow_id = "wf-20251021-project-name-001"
```

2. **Query Best Agents** (optional, for data-driven selection)
```python
from scripts.query_best_agent import query_best_agent

recommendation = query_best_agent("backend API development", "backend")
# Use recommendation.agent_name if confidence >= 0.7
# Otherwise fallback to heuristic rules
```

3. **Log Workflow Start**
```python
from telemetry.logger import TelemetryLogger

logger = TelemetryLogger()
logger.log_workflow_start(
    workflow_id=workflow_id,
    project_name="Full-Stack Todo App",
    agent_plan=["systems-architect", "backend-architect", "frontend-developer"],
    estimated_duration=3600  # seconds
)
```

4. **Log Agent Handoffs** (between agents)
```python
logger.log_agent_handoff(
    workflow_id=workflow_id,
    from_agent="systems-architect",
    to_agent="backend-architect",
    artifacts=["artifacts/systems-architect/architecture.md"]
)
```

5. **Log Workflow Complete**
```python
logger.log_workflow_complete(
    workflow_id=workflow_id,
    duration_seconds=3200,
    success=True,
    agents_executed=["systems-architect", "backend-architect", "frontend-developer"]
)
```

### Complete Example

```python
# Classification
user_request = "Build a secure REST API"
classification = "COORDINATION"
domains = ["Backend", "Security"]

# Create workflow
workflow_id = "wf-20251021-secure-api-001"
logger = TelemetryLogger()

# Query best agents
backend_rec = query_best_agent("backend API development", "backend")
security_rec = query_best_agent("security audit", "security")

agent_plan = [
    backend_rec.agent_name if backend_rec and backend_rec.confidence >= 0.7 else "backend-architect",
    security_rec.agent_name if security_rec and security_rec.confidence >= 0.7 else "security-auditor"
]

# Log start
logger.log_workflow_start(
    workflow_id=workflow_id,
    project_name="Secure REST API",
    agent_plan=agent_plan,
    estimated_duration=3600
)

# Execute backend-architect
execute_agent("backend-architect", "Implement REST API")

# Log handoff to security-auditor
logger.log_agent_handoff(
    workflow_id=workflow_id,
    from_agent="backend-architect",
    to_agent="security-auditor",
    artifacts=["src/api/auth.ts", "artifacts/backend-architect/api-spec.yaml"]
)

# Execute security-auditor
execute_agent("security-auditor", "Audit API security")

# Log completion
logger.log_workflow_complete(
    workflow_id=workflow_id,
    duration_seconds=3200,
    success=True,
    agents_executed=["backend-architect", "security-auditor"]
)
```

## For Users: Understanding Workflow Statistics

### Workflow Success Rate
- **90-100%**: Excellent - workflows completing successfully
- **70-90%**: Good - some issues but manageable
- **<70%**: Needs attention - investigate failures

### Coordination Overhead
- **0-15%**: Excellent - very efficient coordination
- **15-30%**: Good - acceptable overhead
- **>30%**: Consider Phase 3 (structured state files)

**Overhead Calculation**:
```
Overhead = (Total Workflow Time - Sum of Agent Execution Times) / Total Workflow Time
```

Example: 
- Workflow takes 100 minutes total
- Agents execute for 85 minutes combined
- Overhead = (100 - 85) / 100 = 15%

### Agent Performance Trends
- **Improving**: Recent success rate > historical (good!)
- **Stable**: Recent ≈ historical (consistent performance)
- **Declining**: Recent < historical (needs investigation)

**Trend Calculation**:
- Recent: Last 7 days performance
- Historical: Previous 23 days (30 days total lookback)
- Change: Recent - Historical

## Common Workflows

### Backend API Development

**Pattern**: design → backend + security → testing

```bash
oak-query-agent "backend API development" backend
# Likely result: backend-architect (high confidence)

oak-query-agent "security audit" security  
# Likely result: security-auditor (high confidence)

oak-query-agent "unit testing" testing
# Likely result: unit-test-expert (high confidence)
```

### Full-Stack Application

**Pattern**: design → backend + frontend → infrastructure

```bash
oak-query-agent "system architecture" architecture
# Result: systems-architect

oak-query-agent "REST API" backend
# Result: backend-architect

oak-query-agent "React UI" frontend
# Result: frontend-developer

oak-query-agent "AWS deployment" infrastructure
# Result: infrastructure-specialist
```

### Security Review

**Pattern**: security + dependency + code review

```bash
oak-query-agent "security audit" security
# Result: security-auditor

oak-query-agent "dependency scanning" security
# Result: dependency-scanner

oak-query-agent "code review" quality
# Result: code-reviewer
```

## Troubleshooting

### No Workflow Data

**Symptom**: `oak-workflows` shows "No workflow data yet"

**Solution**: 
1. Workflow tracking only happens for multi-agent COORDINATION tasks
2. Single-agent tasks don't create workflow data (by design)
3. Run a multi-agent workflow to generate data

### Low Confidence Recommendations

**Symptom**: `oak-query-agent` returns low confidence (<50%)

**Solution**:
1. Not enough historical data for this task type
2. Fallback to heuristic rules from CLAUDE.md
3. After executing task, confidence will improve

### Agent Trends Show "Insufficient Data"

**Symptom**: `oak-agent-trends <name>` shows insufficient data

**Solution**:
1. Agent needs at least 2 invocations for trends
2. Need data spanning at least 7 days
3. Execute more tasks with this agent

## Best Practices

### 1. Track Complex Workflows
- Multi-agent coordination (2+ agents)
- Long-running projects (>1 hour)
- Sequential or parallel execution patterns

### 2. Query Before Selecting
- Use `oak-query-agent` to check historical performance
- Use recommendations with confidence >= 70%
- Fallback to heuristics for low confidence

### 3. Review Regularly
- Weekly: Run `oak-weekly-review` to check workflows
- Monthly: Run `oak-monthly-review` to check trends
- Monitor coordination overhead percentage

### 4. Optimize Based on Data
- If overhead > 30%, consider Phase 3
- If agents declining, investigate and improve
- If patterns emerge, create workflow templates

## What's Next?

After Phase 2, the system can:
- **Phase 3**: Structured state files (if overhead > 30%)
- **Phase 4**: Automated agent selection
- **Phase 5**: Workflow templates and patterns
- **Phase 6**: Real-time monitoring dashboard

But first, let the data guide the decision. Monitor:
1. Coordination overhead (should stay < 30%)
2. Agent performance trends (watch for declines)
3. Workflow success rates (should stay > 90%)

## Need Help?

### Documentation
- See `examples/integrated_workflow_example.md` for complete example
- See `INTEGRATION_SUMMARY.md` for technical details
- See `CLAUDE.md` for Main LLM workflow guidance

### Commands
```bash
oak-help              # Show all commands
oak-status            # System status
oak-workflows         # Workflow statistics
oak-query-agent       # Agent recommendations
oak-agent-trends      # Performance trends
```

### Support
- Integration tests: `python3 tests/test_integration_workflow.py`
- Check telemetry: `ls -la telemetry/workflow_events.jsonl`
- Verify data: `python3 -c "from telemetry.analyzer import TelemetryAnalyzer; a = TelemetryAnalyzer(); print(a.analyze_workflows())"`

---

**Phase 2 Status**: Integrated and Ready  
**Last Updated**: 2025-10-21
