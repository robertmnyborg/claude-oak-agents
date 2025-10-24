# Spec: [Feature Name]

**Created**: YYYY-MM-DD
**Updated**: YYYY-MM-DD
**Status**: draft | approved | in-progress | completed
**Spec ID**: spec-YYYYMMDD-feature-name
**Linked Request**: [Verbatim user request or reference]

---

## 1. Goals & Requirements

### 1.1 Primary Goal
[What are we trying to achieve and why? 1-2 sentences capturing the essence.]

### 1.2 User Stories
- **As a** [user/persona], **I want** [capability], **so that** [benefit/outcome]
- **As a** [user/persona], **I want** [capability], **so that** [benefit/outcome]

### 1.3 Acceptance Criteria
Clear, testable criteria that define "done":

- [ ] **AC-1**: [Criterion 1 - specific and measurable]
- [ ] **AC-2**: [Criterion 2 - specific and measurable]
- [ ] **AC-3**: [Criterion 3 - specific and measurable]

### 1.4 Success Metrics
How we measure if this was valuable:

- [Metric 1: e.g., "Reduces user login time by 50%"]
- [Metric 2: e.g., "Zero security vulnerabilities in first month"]

### 1.5 Out of Scope
What we're explicitly NOT doing (prevents scope creep):

- [Item 1]
- [Item 2]

---

## 2. Technical Design

### 2.1 Architecture Overview
[High-level design approach. Diagrams welcome. Why this approach over alternatives?]

**Key Design Decisions**:
1. [Decision 1]: [Rationale]
2. [Decision 2]: [Rationale]

### 2.2 Components
Breakdown of system components:

- **Component 1**: [Name/Purpose]
  - **Location**: `path/to/file` or `directory/`
  - **Responsibility**: [What it does]
  - **Interfaces**: [APIs it exposes]
  - **Dependencies**: [What it depends on]
  - **Links to**: [Goals: 1.2, 1.3.AC-1]

- **Component 2**: [Name/Purpose]
  - **Location**: `path/to/file`
  - **Responsibility**: [What it does]
  - **Interfaces**: [APIs it exposes]
  - **Dependencies**: [What it depends on]
  - **Links to**: [Goals: 1.3.AC-2]

### 2.3 Data Structures
Key data models and schemas:

```yaml
# Example Schema
ModelName:
  field1: type
  field2: type
  relationships:
    - relates_to: OtherModel
```

**Links to**: [Goals: 1.3.AC-X]

### 2.4 APIs / Interfaces
[If creating/modifying APIs]

**Endpoint**: `METHOD /path/to/endpoint`
- **Purpose**: [What it does]
- **Input**: [Request schema]
- **Output**: [Response schema]
- **Links to**: [Goals: 1.2, 1.3.AC-X]

### 2.5 Dependencies
External libraries, services, systems:

- **Dependency 1**: [name] v[version] - [why needed]
- **Dependency 2**: [name] v[version] - [why needed]

### 2.6 Security Considerations
[If applicable - auth, data protection, input validation]

**Links to**: [Goals: 1.3.AC-X]

### 2.7 Performance Considerations
[If applicable - scalability, caching, optimization]

**Links to**: [Goals: 1.4 metrics]

---

## 3. Implementation Plan

### 3.1 Task Breakdown
Detailed tasks with clear agent assignments:

#### Task 1: [Task Name]
- **ID**: `task-1`
- **Description**: [What needs to be done]
- **Agent**: [recommended-agent-name]
- **Files**: `path/to/file1`, `path/to/file2`
- **Depends On**: [none | task-X]
- **Estimate**: [time or complexity: trivial/simple/moderate/complex]
- **Links to**:
  - Design: [2.2.Component1]
  - Goals: [1.3.AC-1]
- **Status**: [ ] Pending

#### Task 2: [Task Name]
- **ID**: `task-2`
- **Description**: [What needs to be done]
- **Agent**: [recommended-agent-name]
- **Files**: `path/to/file`
- **Depends On**: task-1
- **Estimate**: [time or complexity]
- **Links to**:
  - Design: [2.2.Component2]
  - Goals: [1.3.AC-2]
- **Status**: [ ] Pending

### 3.2 Execution Sequence
Visualization of task dependencies:

```
task-1 → task-2 → task-5
           ↓
task-3 || task-4 (parallel)
    ↓         ↓
    → task-6 ←
```

### 3.3 Risk Assessment
Potential blockers and mitigation:

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How to mitigate] |
| [Risk 2] | High/Med/Low | High/Med/Low | [How to mitigate] |

---

## 4. Test Strategy

### 4.1 Test Cases
Comprehensive test scenarios linked to requirements:

#### Test Case 1: [Test Name]
- **TC-ID**: `tc-1`
- **Description**: [What we're testing]
- **Given**: [Preconditions / setup]
- **When**: [Action / trigger]
- **Then**: [Expected result / assertion]
- **Links to**:
  - Goals: [1.3.AC-1]
  - Design: [2.2.Component1]
- **Status**: [ ] Pending

#### Test Case 2: [Test Name]
- **TC-ID**: `tc-2`
- **Description**: [What we're testing]
- **Given**: [Preconditions]
- **When**: [Action]
- **Then**: [Expected result]
- **Links to**:
  - Goals: [1.3.AC-2]
  - Design: [2.3.DataModel]
- **Status**: [ ] Pending

### 4.2 Test Types
Breakdown by test category:

- **Unit Tests**:
  - [ ] Component 1 unit tests
  - [ ] Component 2 unit tests

- **Integration Tests**:
  - [ ] API integration tests
  - [ ] Database integration tests

- **End-to-End Tests**:
  - [ ] User flow 1
  - [ ] User flow 2

- **Performance Tests** (if applicable):
  - [ ] Load test scenario 1
  - [ ] Benchmark scenario 2

### 4.3 Validation Checklist
Final sign-off criteria:

- [ ] All test cases pass (tc-1 through tc-N)
- [ ] All acceptance criteria met (AC-1 through AC-N)
- [ ] No critical bugs or regressions
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Success metrics baseline established

---

## 5. Agent Execution Log

**Note**: This section is auto-populated during implementation by spec-manager.

### Execution Timeline

#### [YYYY-MM-DD HH:MM:SS] - Task 1 Started
- **Agent**: [agent-name]
- **Task ID**: task-1
- **Telemetry ID**: inv-XXXXXX
- **Spec Section**: [2.2.Component1, 3.1.Task1]

#### [YYYY-MM-DD HH:MM:SS] - Task 1 Completed
- **Agent**: [agent-name]
- **Status**: ✅ Success | ❌ Failed | ⚠️ Partial
- **Duration**: [Xm Ys]
- **Notes**: [Any relevant observations]
- **Files Modified**: `path/to/file1`, `path/to/file2`

#### [YYYY-MM-DD HH:MM:SS] - Task 2 Started
- **Agent**: [agent-name]
- **Task ID**: task-2
- **Telemetry ID**: inv-XXXXXX
- **Spec Section**: [2.2.Component2, 3.1.Task2]

---

## 6. Changes & Decisions

**Note**: This section tracks deviations from the original plan during implementation.

### 6.1 Design Changes
Changes to the technical design during implementation:

#### [YYYY-MM-DD] - Change Description
- **Reason**: [Why we changed]
- **Original Design**: [What was planned]
- **New Design**: [What we're doing instead]
- **Sections Updated**: [2.2.Component1, 3.1.Task1]
- **Approved By**: User | spec-manager (autonomous)
- **Impact**: [Low/Medium/High - what else is affected]

### 6.2 Scope Changes
Changes to requirements or acceptance criteria:

#### [YYYY-MM-DD] - Scope Change
- **Change**: [What changed in scope]
- **Reason**: [Why - new insight, blocker, user request]
- **Sections Updated**: [1.3.AC-X, 3.1.TaskX]
- **Approved By**: User

### 6.3 Deviations
Implementation details that differ from spec:

#### [YYYY-MM-DD] - Deviation Description
- **Deviation**: [What was done differently]
- **Reason**: [Why - better approach found, technical constraint]
- **Spec Alignment**: [Still meets requirements? Yes/No]
- **If No**: [Propose spec update]

---

## 7. Completion Summary

**Note**: Filled in when spec status changes to "completed".

### 7.1 Acceptance Criteria Status
- [x] **AC-1**: [Criterion] - ✅ Met
- [x] **AC-2**: [Criterion] - ✅ Met
- [x] **AC-3**: [Criterion] - ✅ Met

### 7.2 Test Results
- **Unit Tests**: X/X passed
- **Integration Tests**: X/X passed
- **E2E Tests**: X/X passed
- **All Tests**: ✅ Passing

### 7.3 Success Metrics Baseline
- [Metric 1]: [Measured value]
- [Metric 2]: [Measured value]

### 7.4 Files Changed
Total files modified: X
- `path/to/file1` (created/modified/deleted)
- `path/to/file2` (created/modified/deleted)

### 7.5 Lessons Learned
[What went well, what could be improved for future specs]

### 7.6 Follow-up Items
[Any deferred work, technical debt, or future enhancements]
- [ ] Item 1
- [ ] Item 2

---

## Appendix

### References
- [Link to related specs]
- [Link to external documentation]
- [Link to design discussions]

### Glossary
- **Term 1**: Definition
- **Term 2**: Definition
