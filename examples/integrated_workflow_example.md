# Integrated Workflow Example: Full-Stack Todo App

This example demonstrates how Phase 2 workflow coordination integrates with the existing OaK system.

## User Request

"Build a full-stack todo application with authentication, real-time updates, and deployment to AWS."

## Main LLM Workflow (with Phase 2 Integration)

### Step 1: Classification

```
CLASSIFICATION: COORDINATION
DOMAINS: Backend, Frontend, Security, Infrastructure
COMPLEXITY: Complex (6+ agents)
APPROACH: Multi-agent workflow with Phase 2 tracking
```

### Step 2: Create Workflow Plan with Data-Driven Agent Selection

The Main LLM generates a workflow ID and queries historical performance data to select the best agents for each role:

```python
# Main LLM generates workflow ID
workflow_id = "wf-20251021-fullstack-todo-001"
project_name = "Full-Stack Todo App"

# Query best agents for each role using historical data
agent_plan = []

# Design phase
recommendation = query_best_agent("system architecture design", "architecture")
# Returns: systems-architect (confidence: 0.82, success_rate: 87%)
agent_plan.append({
    "role": "architecture",
    "agent": recommendation.agent_name,
    "confidence": recommendation.confidence,
    "selection_method": "telemetry"
})

# Backend phase
recommendation = query_best_agent("REST API development", "backend")
# Returns: backend-architect (confidence: 0.88, success_rate: 92%)
agent_plan.append({
    "role": "backend",
    "agent": recommendation.agent_name,
    "confidence": recommendation.confidence,
    "selection_method": "telemetry"
})

# Security review (parallel with backend)
recommendation = query_best_agent("security audit", "security")
# Returns: security-auditor (confidence: 0.95, success_rate: 98%)
agent_plan.append({
    "role": "security",
    "agent": recommendation.agent_name,
    "confidence": recommendation.confidence,
    "selection_method": "telemetry"
})

# Frontend phase
recommendation = query_best_agent("React UI development", "frontend")
# Returns: frontend-developer (confidence: 0.75, success_rate: 85%)
agent_plan.append({
    "role": "frontend",
    "agent": recommendation.agent_name,
    "confidence": recommendation.confidence,
    "selection_method": "telemetry"
})

# Infrastructure phase
recommendation = query_best_agent("AWS deployment", "infrastructure")
# Returns: infrastructure-specialist (confidence: 0.91, success_rate: 94%)
agent_plan.append({
    "role": "infrastructure",
    "agent": recommendation.agent_name,
    "confidence": recommendation.confidence,
    "selection_method": "telemetry"
})

# Log workflow start
log_workflow_start(
    workflow_id=workflow_id,
    project_name=project_name,
    agent_plan=[a["agent"] for a in agent_plan],
    estimated_duration=10800  # 3 hours
)
```

### Step 3: Execute Workflow with Handoff Tracking

```python
# Phase 1: Design
result_architecture = delegate_to_agent(
    "systems-architect",
    "Design architecture for full-stack todo app with real-time updates"
)

# Log handoff to backend + security
artifacts_architecture = [
    "artifacts/systems-architect/architecture.md",
    "artifacts/systems-architect/tech-stack.md",
    "artifacts/systems-architect/data-model.md"
]

log_agent_handoff(
    workflow_id=workflow_id,
    from_agent="systems-architect",
    to_agent="backend-architect",
    artifacts=artifacts_architecture
)

log_agent_handoff(
    workflow_id=workflow_id,
    from_agent="systems-architect",
    to_agent="security-auditor",
    artifacts=artifacts_architecture
)

# Phase 2: Backend + Security (parallel execution)
result_backend = delegate_to_agent(
    "backend-architect",
    "Read artifacts/systems-architect/ and implement REST API with real-time WebSocket support"
)

result_security = delegate_to_agent(
    "security-auditor",
    "Read artifacts/systems-architect/ and audit authentication security implementation"
)

# Log handoff to frontend
artifacts_backend = [
    "artifacts/backend-architect/api-spec.yaml",
    "artifacts/backend-architect/auth-flow.md",
    "artifacts/backend-architect/websocket-api.md"
]

log_agent_handoff(
    workflow_id=workflow_id,
    from_agent="backend-architect",
    to_agent="frontend-developer",
    artifacts=artifacts_backend
)

# Phase 3: Frontend
result_frontend = delegate_to_agent(
    "frontend-developer",
    "Read artifacts/backend-architect/api-spec.yaml and build React UI with real-time updates"
)

# Log handoff to infrastructure
artifacts_all = artifacts_architecture + artifacts_backend + [
    "artifacts/frontend-developer/components.tsx",
    "artifacts/frontend-developer/deployment-manifest.md"
]

log_agent_handoff(
    workflow_id=workflow_id,
    from_agent="frontend-developer",
    to_agent="infrastructure-specialist",
    artifacts=artifacts_all
)

# Phase 4: Infrastructure
result_infrastructure = delegate_to_agent(
    "infrastructure-specialist",
    "Deploy full-stack app to AWS based on all artifacts (Lambda + API Gateway + S3 + CloudFront)"
)

# Log workflow completion
log_workflow_complete(
    workflow_id=workflow_id,
    duration_seconds=9600,  # 2.67 hours (under estimate)
    success=all([
        result_architecture.success,
        result_backend.success,
        result_security.success,
        result_frontend.success,
        result_infrastructure.success
    ]),
    agents_executed=[
        "systems-architect",
        "backend-architect",
        "security-auditor",
        "frontend-developer",
        "infrastructure-specialist"
    ]
)
```

### Step 4: Quality Gate and Git Operations

Standard OaK workflow (unchanged):

```python
# Quality gate validation
quality_gate_validation()

# Git operations
git_workflow_manager()

# Changelog recording
changelog_recorder()
```

## Telemetry Data Generated

The workflow tracking generates the following telemetry events:

```jsonl
{"timestamp": "2025-10-21T10:00:00Z", "event": "workflow_start", "workflow_id": "wf-20251021-fullstack-todo-001", "session_id": "abc-123", "project_name": "Full-Stack Todo App", "agent_plan": ["systems-architect", "backend-architect", "security-auditor", "frontend-developer", "infrastructure-specialist"], "estimated_duration": 10800}

{"timestamp": "2025-10-21T10:30:00Z", "event": "agent_handoff", "workflow_id": "wf-20251021-fullstack-todo-001", "session_id": "abc-123", "from_agent": "systems-architect", "to_agent": "backend-architect", "artifacts": ["artifacts/systems-architect/architecture.md", "artifacts/systems-architect/tech-stack.md", "artifacts/systems-architect/data-model.md"]}

{"timestamp": "2025-10-21T10:30:00Z", "event": "agent_handoff", "workflow_id": "wf-20251021-fullstack-todo-001", "session_id": "abc-123", "from_agent": "systems-architect", "to_agent": "security-auditor", "artifacts": ["artifacts/systems-architect/architecture.md", "artifacts/systems-architect/tech-stack.md", "artifacts/systems-architect/data-model.md"]}

{"timestamp": "2025-10-21T11:45:00Z", "event": "agent_handoff", "workflow_id": "wf-20251021-fullstack-todo-001", "session_id": "abc-123", "from_agent": "backend-architect", "to_agent": "frontend-developer", "artifacts": ["artifacts/backend-architect/api-spec.yaml", "artifacts/backend-architect/auth-flow.md", "artifacts/backend-architect/websocket-api.md"]}

{"timestamp": "2025-10-21T12:30:00Z", "event": "agent_handoff", "workflow_id": "wf-20251021-fullstack-todo-001", "session_id": "abc-123", "from_agent": "frontend-developer", "to_agent": "infrastructure-specialist", "artifacts": ["artifacts/systems-architect/architecture.md", "artifacts/backend-architect/api-spec.yaml", "artifacts/frontend-developer/components.tsx", "artifacts/frontend-developer/deployment-manifest.md"]}

{"timestamp": "2025-10-21T12:40:00Z", "event": "workflow_complete", "workflow_id": "wf-20251021-fullstack-todo-001", "session_id": "abc-123", "duration_seconds": 9600, "success": true, "agents_executed": ["systems-architect", "backend-architect", "security-auditor", "frontend-developer", "infrastructure-specialist"]}
```

## Analysis After Workflow

Users can now query workflow statistics using the new oak-* commands:

### View Workflow Statistics

```bash
oak-workflows

# Output:
# 📊 Recent Multi-Agent Workflows
# ========================================================================
# 
# Total Workflows: 1
# Success Rate: 100%
# Avg Duration: 160.0 minutes
# Avg Agents/Workflow: 5.0
# 
# Common Agent Patterns:
#   systems-architect→backend-architect→frontend-developer→infrastructure-specialist (1x)
#
# Coordination Overhead: 18.2%
# Recommendation: Stay Phase 1-2 (Efficient coordination)
```

### Query Best Agent for Next Task

```bash
oak-query-agent "backend API development" backend

# Output:
# Recommended Agent: backend-architect
#    Confidence: 90%
#    Success Rate: 92%
#    Avg Duration: 75.0 min
#    Total Tasks: 6
#    Trend: stable
```

### View Agent Performance Trends

```bash
oak-agent-trends backend-architect

# Output:
# 📈 Performance Trends: backend-architect
# ============================================================
# Trend: improving
# Recent Success Rate (7 days): 95%
# Historical Success Rate: 88%
# Change: +0.07 percentage points
```

## Benefits Demonstrated

### 1. Data-Driven Agent Selection

Historical performance data informed all agent selections:
- **systems-architect**: 82% confidence based on 15 prior architecture tasks
- **backend-architect**: 88% confidence based on 12 prior API development tasks
- **security-auditor**: 95% confidence based on 20 prior security audits
- **frontend-developer**: 75% confidence based on 8 prior React UI tasks
- **infrastructure-specialist**: 91% confidence based on 18 prior AWS deployments

### 2. Workflow Tracking

Complete visibility into the multi-agent workflow:
- Total duration tracked: 9,600 seconds (2.67 hours)
- 5 agents executed successfully
- 4 handoffs tracked with artifacts
- Coordination overhead: 18.2% (efficient)

### 3. Coordination Analysis

Measured coordination efficiency:
- **Total workflow time**: 160 minutes
- **Total agent execution time**: 131 minutes
- **Coordination overhead**: 29 minutes (18.2%)
- **Recommendation**: Stay Phase 1-2 (no need for structured state files)

### 4. Performance Trends

Tracked agent improvements over time:
- backend-architect showing improving trend (+7% success rate)
- All agents performing above 85% success rate
- No declining agents detected

### 5. Shell Integration

Easy access to workflow statistics via oak-* commands:
- `oak-workflows` - View workflow statistics
- `oak-query-agent` - Find best agent for task
- `oak-agent-trends` - Track performance trends
- `oak-weekly-review` - Automated workflow analysis

## Backward Compatibility

The Phase 2 integration maintains full backward compatibility:

### Single-Agent Tasks (No Change)

```
User Request: "Fix TypeScript error in auth.ts"

CLASSIFICATION: IMPLEMENTATION
DOMAINS: Backend
AGENT PLAN: backend-architect (single agent)

# No workflow tracking for single-agent tasks
# Standard invocation logging only
execute(backend-architect) → fix error → quality gate → git operations
```

### Existing Telemetry (No Change)

All existing telemetry continues functioning:
- `agent_invocations.jsonl` - Individual agent executions
- `success_metrics.jsonl` - Quality ratings and feedback
- `performance_stats.json` - Agent performance statistics

### New Features (Optional)

Workflow tracking is optional and only activated for multi-agent COORDINATION tasks:
- Graceful degradation if `workflow_events.jsonl` doesn't exist
- Shell commands handle missing data with informative messages
- No breaking changes to existing agent APIs

## Lessons Learned

### What Worked Well

1. **Data-driven selection improved accuracy**: 88% average confidence across all agent selections
2. **Workflow tracking provided visibility**: Complete audit trail of artifact flow
3. **Overhead measurement enabled decisions**: 18.2% overhead confirmed Phase 1-2 is sufficient
4. **Shell integration simplified access**: Users can query stats without Python knowledge

### Areas for Improvement

1. **Parallel execution tracking**: Need better representation of concurrent agent execution
2. **Artifact dependency tracking**: Could improve handoff validation
3. **Workflow templates**: Common patterns could be templated for faster setup
4. **Real-time monitoring**: Live workflow status during execution

## Next Steps

Based on this workflow execution:

1. **Continue Phase 1-2**: 18.2% coordination overhead is efficient (no need for Phase 3)
2. **Monitor backend-architect**: Improving trend is positive, continue current approach
3. **Expand telemetry**: More workflow executions will improve agent selection confidence
4. **Document patterns**: "systems-architect → backend + security → frontend → infrastructure" is a reusable pattern

## Conclusion

The Phase 2 integration successfully enhanced the OaK system with:
- **Data-driven agent selection** using historical performance
- **Workflow tracking** for multi-agent coordination visibility
- **Coordination analysis** to measure efficiency and guide decisions
- **Performance trends** to track agent improvements over time
- **Shell integration** for easy access to workflow statistics

All while maintaining **100% backward compatibility** with existing single-agent workflows and telemetry systems.
