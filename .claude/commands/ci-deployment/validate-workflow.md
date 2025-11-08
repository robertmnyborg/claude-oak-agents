# Validate Workflow

Validate that the entire workflow has been completed correctly including all phases and quality gates.

## Usage
/validate-workflow [--spec-id SPEC_ID] [--strict]

## What This Does
1. Checks workflow state file for completion status
2. Validates all workflow phases completed in order
3. Verifies quality gates passed
4. Confirms git workflow completed (commit created)
5. Validates spec acceptance criteria met (if spec provided)
6. Generates comprehensive workflow validation report

## Example
/validate-workflow --spec-id spec-20251108-oauth2 --strict

## Agent Coordination
1. **Main LLM**: Reads and validates workflow state
   - Parses .workflow_state file
   - Verifies phase completion
   - Checks quality gate status
2. **Main LLM** (if spec provided): Validates spec completion
   - Reads spec file
   - Checks acceptance criteria status
   - Verifies all tasks completed
3. **Main LLM**: Generates validation report

## Output
Workflow Validation Report:
```markdown
## Workflow Validation Report

**Workflow ID**: wf-20251108-abc123
**Spec ID**: spec-20251108-oauth2-implementation
**Validation Mode**: Strict
**Date**: 2025-11-08 16:00:00

### Overall Status: ✅ WORKFLOW COMPLETE

All phases completed successfully. Ready for deployment.

---

## Workflow State Validation

### ✅ Workflow State File: VALID
**Location**: .workflow_state
**Last Updated**: 2025-11-08 15:50:00

**Contents**:
```
PHASE=GIT_OPERATIONS
STATUS=COMPLETED
QUALITY_GATE_PASSED=true
WARNINGS=3
BLOCKERS=0
CODE_HASH=abc123f
COMMIT_HASH=def456a
TIMESTAMP=2025-11-08T15:50:00Z
```

---

## Phase Completion Validation

### Phase 1: Implementation ✅
**Status**: COMPLETED
**Agent**: backend-architect
**Duration**: 8 minutes 12 seconds
**Started**: 2025-11-08 14:30:00
**Completed**: 2025-11-08 14:38:12

**Deliverables**:
- ✅ OAuth2 endpoints implemented (src/auth/oauth2.ts)
- ✅ Token rotation logic added (src/auth/token.ts)
- ✅ Redis integration for token families
- ✅ OpenAPI documentation updated

**Validation**: All implementation tasks completed ✅

### Phase 2: Quality Gate ✅
**Status**: COMPLETED
**Agent**: quality-gate
**Duration**: 2 minutes 15 seconds
**Started**: 2025-11-08 14:40:00
**Completed**: 2025-11-08 14:42:15

**Checks Performed**:
- ✅ Code review and standards: PASSED
- ✅ Maintainability analysis: PASSED (78/100)
- ✅ Complexity validation: PASSED (Avg: 6)
- ✅ KISS compliance: PASSED (85/100)
- ✅ Security basics: PASSED
- ✅ Test coverage: PASSED (91%)

**Warnings**: 3 (non-blocking)
- Missing JSDoc comments (2 functions)
- Duplicate error handling (3 locations)
- Complex function (rotateRefreshToken)

**Blockers**: 0

**Validation**: Quality gates passed with warnings ✅

### Phase 3: Git Operations ✅
**Status**: COMPLETED
**Agent**: git-workflow-manager
**Duration**: 45 seconds
**Started**: 2025-11-08 15:48:00
**Completed**: 2025-11-08 15:48:45

**Operations**:
- ✅ Changes staged (8 files modified)
- ✅ Commit created (hash: def456a)
- ✅ Commit message formatted with spec reference
- ✅ Attribution added (Claude Code co-author)
- ✅ Branch pushed to remote (feature/oauth2-refresh-rotation)

**Commit Message**:
```
feat: Implement OAuth2 refresh token rotation

- Add automatic token rotation on refresh
- Implement token family tracking in Redis
- Handle concurrent refresh requests safely
- Invalidate old tokens immediately after use

Spec: spec-20251108-oauth2-implementation
Acceptance Criteria: AC-3.2.1, AC-3.2.2, AC-3.2.3, AC-3.2.4 satisfied

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Validation**: Git workflow completed successfully ✅

---

## Specification Validation

### ✅ Spec Completion: ALL CRITERIA MET
**Spec ID**: spec-20251108-oauth2-implementation
**Section**: 3.2 - Refresh Token Rotation

### Acceptance Criteria Status

**AC-3.2.1**: Refresh endpoint rotates tokens on each use ✅
- **Status**: SATISFIED
- **Evidence**: Implementation in src/auth/token.ts:rotateRefreshToken()
- **Test**: tests/auth/rotation.test.ts:45 - "rotates token on refresh" PASSED

**AC-3.2.2**: Old refresh tokens invalidated immediately ✅
- **Status**: SATISFIED
- **Evidence**: Redis delete operation after rotation
- **Test**: tests/auth/rotation.test.ts:78 - "old token invalid after rotation" PASSED

**AC-3.2.3**: Token family tracking prevents token reuse ✅
- **Status**: SATISFIED
- **Evidence**: Token family ID stored in Redis
- **Test**: tests/auth/rotation.test.ts:102 - "detects token reuse attack" PASSED

**AC-3.2.4**: Concurrent refresh requests handled safely ✅
- **Status**: SATISFIED
- **Evidence**: Distributed lock prevents race conditions
- **Test**: tests/auth/rotation.test.ts:134 - "handles concurrent requests" PASSED

**Overall Spec Progress**: Task 3.2 complete (60% of total spec)

---

## Code Quality Validation

### ✅ Test Coverage: EXCEEDS THRESHOLD
- **Line Coverage**: 91% (target: >85%) ✅
- **Branch Coverage**: 87% (target: >80%) ✅
- **Function Coverage**: 95% (target: >90%) ✅

**New Tests Added**: 12
- 8 unit tests for token rotation
- 3 integration tests for full OAuth2 flow
- 1 security test for token reuse prevention

**Test Execution**: All tests passing ✅

### ✅ Code Standards: COMPLIANT
- **Style Guide**: ESLint rules followed ✅
- **TypeScript**: No type errors ✅
- **Naming**: Consistent conventions ✅
- **Structure**: Proper module organization ✅

### ⚠️ Code Improvements: OPTIONAL
**Non-blocking recommendations**:
1. Add JSDoc to 2 public functions
2. Extract duplicate error handlers
3. Simplify rotateRefreshToken complexity

**Status**: Can be addressed in future refactoring

---

## Security Validation

### ✅ Security Checks: PASSED
- **No hardcoded secrets**: ✅
- **Input validation**: Present ✅
- **SQL injection**: No vulnerabilities ✅
- **Token security**: Proper invalidation ✅
- **Race conditions**: Handled with locks ✅

**Security Audit Status**: Basic checks passed ✅
**Recommendation**: Schedule full security-auditor review before production

---

## Dependency Validation

### ✅ Dependencies: HEALTHY
- **No new dependencies added**: ✅
- **Existing dependencies**: Up to date ✅
- **Security vulnerabilities**: None in new code ✅
- **License compliance**: No issues ✅

---

## Performance Validation

### ✅ Performance: ACCEPTABLE
**Token Rotation Performance**:
- Average duration: 45ms
- 99th percentile: 120ms
- Target: <200ms ✅

**Redis Operations**:
- Get token family: 8ms avg
- Set new token: 12ms avg
- Delete old token: 5ms avg

**No Performance Regressions**: ✅

---

## Integration Validation

### ✅ Integration Points: VERIFIED
**Tested Integration Scenarios**:
- ✅ Token rotation in full OAuth2 flow
- ✅ Integration with existing session management
- ✅ Redis token family storage and retrieval
- ✅ Concurrent request handling

**No Integration Issues**: ✅

---

## Workflow Metadata

### Timeline
```
14:30:00  │ ▶ START: Implementation Phase
14:38:12  │ ✓ COMPLETE: Implementation (8m 12s)
14:40:00  │ ▶ START: Quality Gate Phase
14:42:15  │ ✓ COMPLETE: Quality Gate (2m 15s)
14:48:00  │ ▶ START: Git Operations Phase
14:48:45  │ ✓ COMPLETE: Git Operations (45s)
16:00:00  │ ✓ WORKFLOW VALIDATED
```

**Total Duration**: 18 minutes 45 seconds
**Actual Work Time**: 11 minutes 12 seconds
**Idle Time**: 7 minutes 33 seconds (between phases)

### Agent Execution
```
Agent                | Duration   | Status
---------------------|------------|----------
backend-architect    | 8m 12s     | ✅ SUCCESS
quality-gate         | 2m 15s     | ✅ PASSED
git-workflow-manager | 45s        | ✅ SUCCESS
```

### Resource Usage
- Files modified: 8
- Lines added: 347
- Lines deleted: 52
- Test files: 1 new file, 12 tests added
- Commits: 1

---

## Workflow Checklist

### Required Phases
- ✅ Implementation phase completed
- ✅ Quality gate phase completed
- ✅ Git operations phase completed

### Quality Requirements
- ✅ All quality gates passed
- ✅ Test coverage above threshold
- ✅ No critical security issues
- ✅ Code standards compliant

### Specification Requirements
- ✅ All acceptance criteria met
- ✅ Task deliverables completed
- ✅ Tests validate requirements
- ✅ Documentation updated

### Git Requirements
- ✅ Changes committed with spec reference
- ✅ Commit message follows format
- ✅ Attribution included
- ✅ Branch pushed to remote

---

## Validation Summary

### Results
```
✅ Workflow State:      VALID
✅ Phase Completion:    ALL PHASES COMPLETE
✅ Quality Gates:       PASSED (3 warnings)
✅ Spec Criteria:       ALL MET (4/4)
✅ Test Coverage:       91% (exceeds target)
✅ Security:            NO ISSUES
✅ Git Workflow:        COMPLETE
✅ Integration:         VERIFIED
```

### Warnings (Non-blocking)
- 3 code quality improvements recommended (optional)
- Full security audit recommended before production

### Blockers
- None ✅

---

## Final Verdict: ✅ WORKFLOW VALIDATED

**Status**: COMPLETE AND VALID
**Ready for**: Pull Request creation or deployment to staging

### Recommended Next Steps

**Option 1: Create Pull Request**
```
/pr-with-context spec-20251108-oauth2 --include-telemetry
```

**Option 2: Deploy to Staging**
```
/deploy-check --environment staging
```

**Option 3: Continue to Next Task**
```
/suggest-next-task --context spec
```

---

## Workflow State Summary

**Phases**: 3/3 completed ✅
**Quality Gates**: Passed with warnings ⚠️
**Spec Progress**: 60% complete (Task 3.2 of 5 done)
**Git Status**: Committed and pushed ✅
**Validation**: Complete and ready ✅

**Workflow Duration**: 18 minutes 45 seconds
**Success Rate**: 100%
**Code Hash**: abc123f
**Commit Hash**: def456a

---

**Validation Complete**: 2025-11-08 16:00:00
**Report Generated By**: Main LLM (workflow validation)
```

This provides comprehensive validation of the entire workflow ensuring all phases completed correctly.
## See Also
For related commands, see [Quality Commands](../shared/related-quality-commands.md)
