# Spec-Driven Development Pattern

Complete guide to using the spec-manager agent for collaborative specification writing and execution tracking.

## Overview

Spec-driven development workflow allows product managers and technical leads to co-author specifications with AI assistance, breaking down complex features into executable tasks with clear acceptance criteria.

## When to Use Spec-Driven Workflow

**USE SPEC-DRIVEN for:**
- Significant features or new subsystems
- Architectural changes affecting multiple components
- Multi-agent coordination (5+ files or 3+ agents)
- Complex changes requiring significant refactoring
- Security-critical features (authentication, authorization, data protection)
- Data migrations or schema changes
- User explicitly requests: "Let's create a spec" or "spec-driven approach"

**USE STANDARD TodoWrite for:**
- Simple bug fixes (1-2 files, single agent)
- Typos or documentation updates
- Single-file changes
- User prefers quick iteration

## Workflow Process

### Step 1: Trigger Spec-Driven Workflow

Main LLM evaluates request complexity:

```
Request Analysis
    ↓
Complexity Evaluation
    ↓
    ├─ Simple/Quick → TodoWrite (standard workflow)
    │
    └─ Significant → spec-manager Delegation:
        1. "This looks like a significant change [because...]"
        2. "I recommend spec-driven workflow (10-15 min upfront, clearer design)"
        3. "Sound good?"
        4. User confirms → Delegate to spec-manager
```

### Step 2: Collaborative Spec Creation

**spec-manager** guides user through collaborative writing:

#### Section 1: Goals & Requirements
```markdown
# Goals & Requirements

## Business Objective
[What problem does this solve? Why now?]

## User Stories
As a [role], I want [feature] so that [benefit]

## Success Criteria
- Metric 1: [baseline] → [target]
- Metric 2: [baseline] → [target]

## Constraints
- Technical: [limitations, dependencies]
- Business: [budget, timeline, compliance]
- User: [UX requirements, accessibility]
```

**User approval required** before proceeding to next section.

#### Section 2: Technical Design
```markdown
# Technical Design

## Architecture
[High-level design decisions]

## Components
1. **Component Name**
   - Purpose: [what it does]
   - Technology: [stack choice]
   - Integration: [how it connects]

## Data Model
[Database schema, API contracts]

## Technology Choices
- Framework: [choice] because [rationale]
- Database: [choice] because [rationale]
- Deployment: [choice] because [rationale]

## Non-Functional Requirements
- Performance: [targets]
- Security: [requirements]
- Scalability: [considerations]
```

**User approval required** before proceeding to next section.

#### Section 3: Implementation Plan
```markdown
# Implementation Plan

## Task Breakdown
1. **Task 1: [Name]**
   - Agent: [which agent executes]
   - Files: [files to create/modify]
   - Dependencies: [what must complete first]
   - Estimate: [time estimate]

2. **Task 2: [Name]**
   - Agent: [which agent executes]
   - Files: [files to create/modify]
   - Dependencies: [Task 1]
   - Estimate: [time estimate]

## Execution Sequence
```
[Task dependency graph showing parallel/sequential execution]
```

## Risk Mitigation
- Risk 1: [description] → Mitigation: [approach]
- Risk 2: [description] → Mitigation: [approach]
```

**User approval required** before proceeding to next section.

#### Section 4: Test Strategy
```markdown
# Test Strategy

## Unit Tests
- Component 1: [test coverage requirements]
- Component 2: [test coverage requirements]

## Integration Tests
- Flow 1: [end-to-end scenario]
- Flow 2: [end-to-end scenario]

## Acceptance Criteria
- [ ] AC-1: [specific, testable criterion]
- [ ] AC-2: [specific, testable criterion]
- [ ] AC-3: [specific, testable criterion]

## Performance Tests
- Load: [concurrent users target]
- Response time: [latency target]
```

**User approval required** before generating YAML.

### Step 3: YAML Translation

spec-manager auto-generates machine-readable YAML:

```yaml
# specs/active/2025-11-08-feature-name.yaml
spec_id: "spec-20251108-feature-name"
created_at: "2025-11-08T10:30:00Z"
status: "active"

metadata:
  title: "Feature Name"
  author: "User Name"
  estimated_effort_hours: 24

goals:
  business_objective: "..."
  success_metrics:
    - metric: "Conversion rate"
      baseline: 3.2
      target: 5.0

technical_design:
  architecture: "..."
  components:
    - name: "Component 1"
      technology: "React"
      files:
        - "src/components/Feature.tsx"

tasks:
  - id: "task-1"
    title: "Create database schema"
    agent: "backend-architect"
    files:
      - "migrations/001_create_feature_table.sql"
    dependencies: []
    estimated_hours: 2

  - id: "task-2"
    title: "Implement API endpoint"
    agent: "infrastructure-specialist"
    files:
      - "src/api/routes/feature.ts"
    dependencies: ["task-1"]
    estimated_hours: 4

acceptance_criteria:
  - id: "AC-1"
    description: "User can create feature"
    test_type: "integration"
  - id: "AC-2"
    description: "API responds < 200ms"
    test_type: "performance"
```

### Step 4: Task Decomposition & Agent Assignment

spec-manager analyzes YAML and creates execution plan:

```
Task Assignment:
- Task 1 (DB schema) → backend-architect
- Task 2 (API endpoint) → infrastructure-specialist
- Task 3 (Frontend component) → frontend-developer
- Task 4 (Unit tests) → unit-test-expert
- Task 5 (Security review) → security-auditor

Execution Strategy: Sequential with some parallel execution
- Phase 1: Task 1 (backend-architect)
- Phase 2: Tasks 2 + 3 in parallel (infrastructure-specialist + frontend-developer)
- Phase 3: Task 4 (unit-test-expert)
- Phase 4: Task 5 (security-auditor)
- Phase 5: git-workflow-manager
```

### Step 5: Execution Coordination

spec-manager invokes agents with spec context:

```typescript
// Each agent receives:
{
  spec_id: "spec-20251108-feature-name",
  spec_section: ["3.1.task-1"], // Which task(s) to execute
  spec_context: {
    goals: [...],
    design: [...],
    related_tasks: [...]
  }
}
```

Agents log execution to spec file:

```markdown
## Section 5: Execution Log

### 2025-11-08 10:45 - backend-architect (Task 1)
- Created migration: migrations/001_create_feature_table.sql
- Status: Completed
- Files modified: 1
- Telemetry: inv-20251108-abc123

### 2025-11-08 10:50 - infrastructure-specialist (Task 2)
- Created API endpoint: src/api/routes/feature.ts
- Status: Completed
- Files modified: 2
- Telemetry: inv-20251108-def456

### 2025-11-08 10:55 - frontend-developer (Task 3)
- Created component: src/components/Feature.tsx
- Status: Completed
- Files modified: 3
- Telemetry: inv-20251108-ghi789
```

### Step 6: Change Management

When changes needed during implementation:

```
User: "Spec section 2.3 (Auth Strategy) needs update.
       Current: JWT
       Proposed: OAuth2
       This affects tasks [2, 5]"

spec-manager:
  1. Updates Markdown Section 2.3
  2. Regenerates YAML
  3. Identifies affected tasks
  4. Re-assigns agents if needed
  5. Continues execution with new plan
  6. Logs change in Section 6: Change History
```

**Change History Section**:

```markdown
## Section 6: Change History

### 2025-11-08 11:10 - Auth Strategy Change
**Changed**: Section 2.3 (Authentication)
**From**: JWT tokens
**To**: OAuth2 authorization code flow
**Reason**: Third-party integration requirement discovered
**Affected Tasks**: Task 2 (API auth), Task 5 (Security review)
**Approved By**: User Name
**Re-execution Required**: Yes (Tasks 2, 5)
```

### Step 7: Validation & Completion

spec-manager validates completion:

```markdown
## Section 7: Completion Summary

### Completion Checklist
- [x] All tasks completed (5/5)
- [x] All acceptance criteria met (3/3)
- [x] All tests passing (Unit: 45/45, Integration: 12/12)
- [x] Security review approved
- [x] Code reviewed and merged
- [x] Documentation updated

### Final Metrics
- **Total time**: 24 hours (estimated: 24 hours)
- **Agents invoked**: 7
- **Files modified**: 15
- **Tests created**: 57
- **Code coverage**: 92%

### Post-Implementation Notes
- Performance exceeded target (150ms vs 200ms target)
- OAuth2 change added 4 hours but improved security posture
- Recommendation: Consider spec-driven for similar features

**Status**: COMPLETED
**Moved to**: specs/completed/2025-11-08-feature-name.md
```

## Telemetry Integration

Agent invocations include spec tracking:

```python
logger.log_invocation(
    agent_name="backend-architect",
    spec_id="spec-20251108-feature-name",
    spec_section=["2.2.comp-1", "3.1.task-1"],  # Design + Task
    workflow_id="wf-20251108-xyz",
    task_id="task-1",
    status="completed",
    files_modified=["migrations/001_create_feature_table.sql"],
    duration_seconds=180
)
```

**Benefits**:
- Trace invocations back to specs
- Analyze which spec sections cause issues
- Measure spec adherence quality
- Track spec accuracy (% needing changes during implementation)

## User Communication Style

### Spec Terms (Recommended)
- ✅ "Spec section 2.3 (Component X) needs update..."
- ✅ "This affects acceptance criteria AC-1 and AC-2..."
- ✅ "Want to review spec or proceed with implementation?"
- ✅ "Implementation of Task 3 complete. 2 tasks remaining."

### Code Terms (Avoid)
- ❌ "Should I change line 45 to use X instead of Y?"
- ❌ "I modified these 8 files, want to see them?"
- ❌ "The function getUserData now uses async/await"

### User Decisions Required
- Approve spec approach (vs TodoWrite)
- Approve each spec section (Goals, Design, Plan, Tests)
- Approve spec changes during implementation
- Approve completion (all criteria met)

### Optional Code Review
- User can always request: "Show me the code for Task X"
- Default: Trust spec adherence, skip detailed code review
- Offer: "Implementation meets spec. View code or mark complete?"

## Spec File Structure

### Markdown (Source of Truth)
`specs/active/YYYY-MM-DD-feature-name.md`

Human-readable, collaborative editing:
1. Goals & Requirements
2. Technical Design
3. Implementation Plan
4. Test Strategy
5. Execution Log (auto-updated)
6. Change History (auto-updated)
7. Completion Summary (final section)

### YAML (Machine-Readable)
`specs/active/YYYY-MM-DD-feature-name.yaml`

Auto-generated from Markdown for agent consumption:
- Structured task data
- Agent assignments
- Dependencies
- File mappings
- Acceptance criteria

## Example: Simple vs Spec-Driven

### Simple (TodoWrite)
```
User: "Fix typo in README line 5"
Main LLM: "Simple fix, using TodoWrite"
    → Creates todo
    → domain-specialist fixes
    → git-workflow-manager commits
```

### Spec-Driven (Significant Feature)
```
User: "Add OAuth2 authentication"
Main LLM: "Significant feature. Recommend spec-driven approach (15 min upfront planning). Sound good?"
User: "Yes"
Main LLM: Delegates to spec-manager
    → spec-manager co-authors spec (Goals, Design, Plan, Tests)
    → User approves each section
    → spec-manager generates YAML
    → spec-manager decomposes tasks:
        - Task 1: backend-architect (OAuth2 endpoints)
        - Task 2: security-auditor (security review)
        - Task 3: frontend-developer (login UI)
    → spec-manager coordinates execution
    → Agents log to execution log
    → spec-manager validates completion
    → "All 5 acceptance criteria met. Spec complete."
```

## Quality Metrics

Track spec-driven workflow effectiveness:

```yaml
metrics:
  spec_accuracy:
    description: "% of specs needing changes during implementation"
    target: <20%
    actual: 15%

  user_satisfaction:
    description: "Did spec process help or hinder?"
    target: >4.0/5.0
    actual: 4.3/5.0

  implementation_fidelity:
    description: "How well code matched spec"
    target: >90%
    actual: 94%

  time_investment_roi:
    description: "Spec time vs rework prevented"
    spec_time_hours: 1.5
    rework_prevented_hours: 6.0
    roi: 4x
```

## Related Documentation

- [OAuth2 Implementation Example](../workflows/oauth2-implementation.md) - Complete spec-driven example
- [Git Workflow Pattern](./git-workflow.md) - Integration with git operations
- [PM Quick Start Guide](../../by-role/product-managers/quick-start.md) - PM-focused workflows

## References

- Specification Template: `specs/templates/SPEC_TEMPLATE.md`
- YAML Generator Tool: `specs/tools/spec-to-yaml-translator.ts`
- spec-manager Agent: `agents/spec-manager.md`
