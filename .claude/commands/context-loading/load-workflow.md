# Load Workflow

Load a workflow by ID to view history, resume interrupted workflows, or analyze execution patterns.

## Usage
/load-workflow [workflow-id]

## What This Does
1. Queries telemetry database for workflow data
2. Loads all agent invocations in the workflow
3. Shows workflow history and current state
4. Allows resuming interrupted workflows from last successful step
5. Displays performance metrics and bottlenecks

## Example
/load-workflow wf-20251108-abc123

## Agent Coordination
1. **Main LLM**: Queries telemetry system
   - Reads workflow invocations from telemetry/invocations.jsonl
   - Reconstructs workflow sequence using parent_invocation_id
   - Identifies current workflow state
2. **Workflow Resume**: Sets context for continuation
   - `OAK_WORKFLOW_ID=wf-20251108-abc123`
   - `OAK_RESUME_FROM=inv-20251108-xyz789`
3. **State Validation**: Ensures workflow can be resumed safely

## Output
Workflow History:
```markdown
## Workflow: wf-20251108-abc123

**Status**: In Progress (3 of 5 agents completed)
**Created**: 2025-11-08 14:00:00
**Duration**: 12 minutes 34 seconds
**Spec**: spec-20251108-oauth2-implementation

### Workflow Sequence

1. ✅ **design-simplicity-advisor** (inv-20251108-aaa111)
   - Duration: 45 seconds
   - Status: Completed successfully
   - Output: Recommended minimal OAuth2 implementation
   - Next: backend-architect

2. ✅ **backend-architect** (inv-20251108-bbb222)
   - Duration: 8 minutes 12 seconds
   - Parent: inv-20251108-aaa111
   - Status: Completed successfully
   - Output: Implemented OAuth2 endpoints
   - Next: security-auditor

3. ✅ **security-auditor** (inv-20251108-ccc333)
   - Duration: 1 minute 20 seconds
   - Parent: inv-20251108-bbb222
   - Status: Completed successfully
   - Output: Security validation passed
   - Next: unit-test-expert

4. ⏳ **unit-test-expert** (inv-20251108-ddd444)
   - Duration: 2 minutes 17 seconds (in progress)
   - Parent: inv-20251108-ccc333
   - Status: In Progress
   - Output: Creating unit tests...
   - Next: qa-specialist

5. ⏸️ **qa-specialist** (pending)
   - Status: Not started
   - Parent: Will be inv-20251108-ddd444

### Performance Metrics
- Total duration: 12 minutes 34 seconds (so far)
- Average agent duration: 3 minutes 10 seconds
- Bottleneck: backend-architect (65% of total time)
- Success rate: 100% (3/3 completed agents)

### Workflow State
- Current phase: Testing
- Resume from: inv-20251108-ccc333 (security-auditor)
- Remaining tasks: unit-test-expert, qa-specialist
- Estimated completion: 5 minutes

### Actions Available
- **Resume workflow**: Continue from unit-test-expert
- **Restart from step**: Re-run from any completed step
- **Cancel workflow**: Mark as abandoned
- **View agent logs**: See detailed execution logs

Would you like to:
1. Resume workflow (continue from current position)
2. View detailed logs for specific agent
3. Restart from a previous step
4. Cancel and start fresh
```

**Resume Workflow**: If workflow is interrupted, you can resume with:
```
/resume-workflow wf-20251108-abc123
```

This will:
- Load workflow context
- Continue from last completed agent
- Preserve all previous agent outputs
- Link new invocations to same workflow_id
