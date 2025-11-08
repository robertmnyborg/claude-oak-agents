# Run Quality Gates

Execute comprehensive quality gate validation before allowing code to proceed to deployment.

## Usage
/run-quality-gates [path] [--strict] [--auto-fix]

## What This Does
1. Executes quality-gate agent for unified validation
2. Validates code quality, maintainability, and complexity
3. Checks architectural impact and KISS compliance
4. Generates detailed quality report
5. Optionally attempts auto-fixes for common issues
6. Updates .workflow_state file with validation status

## Example
/run-quality-gates src/auth --strict

## Agent Coordination
1. **quality-gate**: Unified quality validation
   - Code review and standards
   - Maintainability analysis
   - Complexity validation
   - KISS compliance check
   - Security basics
2. **Main LLM**: Formats report and updates workflow state

## Output
Quality Gate Report:
```markdown
## Quality Gate Validation Report

**Path**: src/auth
**Mode**: Strict (zero tolerance)
**Date**: 2025-11-08 15:45:00
**Commit**: abc123f

### Overall Result: ⚠️ PASSED WITH WARNINGS

**Status**: Quality gates passed, but 3 warnings should be addressed
**Deployment**: ALLOWED (warnings are non-blocking)

---

## Code Review & Standards

### ✅ Code Quality: PASSED
- **Coding Standards**: All files follow style guide ✅
- **Naming Conventions**: Consistent and descriptive ✅
- **File Organization**: Proper module structure ✅
- **Import Management**: Clean, no circular dependencies ✅

**Files Reviewed**: 8
- src/auth/oauth2.ts
- src/auth/token.ts
- src/auth/password.ts
- src/auth/session.ts
- src/auth/middleware.ts
- src/auth/types.ts
- src/auth/utils.ts
- src/auth/index.ts

### ⚠️ Code Patterns: WARNING
**Issue**: Duplicate error handling logic across 3 files

**Details**:
```typescript
// Duplicated in oauth2.ts, token.ts, password.ts
try {
  // logic
} catch (error) {
  logger.error('Error:', error);
  throw new AuthError('Operation failed', 500);
}
```

**Recommendation**: Extract to shared error handler utility
```typescript
// utils/errorHandler.ts
export const handleAuthError = (error: Error, context: string) => {
  logger.error(`${context}:`, error);
  throw new AuthError('Operation failed', 500);
};

// Usage
try {
  // logic
} catch (error) {
  handleAuthError(error, 'OAuth2 token exchange');
}
```

**Impact**: Low (non-blocking, maintainability improvement)

---

## Maintainability Analysis

### ✅ Code Clarity: PASSED
- **Function Length**: Average 18 lines (target: <30) ✅
- **Function Complexity**: Average 6 (target: <10) ✅
- **Comment Quality**: Adequate documentation ✅
- **Type Safety**: 100% TypeScript coverage ✅

**Maintainability Index**: 78/100 (target: >65) ✅

### ⚠️ Documentation: WARNING
**Issue**: 2 public functions missing JSDoc comments

**Missing Documentation**:
```typescript
// src/auth/oauth2.ts:45
export async function exchangeAuthorizationCode(code: string, clientId: string)
// Missing: Parameter descriptions, return type documentation, error cases

// src/auth/token.ts:78
export function validateRefreshToken(token: string)
// Missing: Parameter descriptions, validation rules, exceptions
```

**Recommendation**: Add JSDoc comments
```typescript
/**
 * Exchanges an authorization code for access and refresh tokens.
 *
 * @param code - The authorization code from the authorization endpoint
 * @param clientId - The OAuth2 client identifier
 * @returns Object containing access_token, refresh_token, and expires_in
 * @throws {AuthError} If code is invalid or expired
 * @throws {ClientError} If client_id doesn't match code's client
 */
export async function exchangeAuthorizationCode(code: string, clientId: string)
```

**Impact**: Low (non-blocking, developer experience improvement)

---

## Complexity Validation

### ✅ Cyclomatic Complexity: PASSED
- **Average Complexity**: 6 (target: <10) ✅
- **Max Complexity**: 12 (target: <15) ✅
- **High Complexity Functions**: 1 (acceptable)

**Complexity Breakdown**:
```
Function                          | Complexity | Status
----------------------------------|------------|--------
exchangeAuthorizationCode         |     8      |  ✅
validateRefreshToken              |     6      |  ✅
rotateRefreshToken                |    12      |  ⚠️
generateAccessToken               |     4      |  ✅
verifyAccessToken                 |     5      |  ✅
hashPassword                      |     3      |  ✅
validatePassword                  |     7      |  ✅
createSession                     |     5      |  ✅
```

### ⚠️ rotateRefreshToken: WARNING (Complexity: 12)
**Location**: src/auth/token.ts:125

**Issue**: Function handles multiple edge cases in nested conditionals

```typescript
async function rotateRefreshToken(oldToken: string, userId: string) {
  // Complexity breakdown:
  // - 3 nested if statements
  // - 2 try-catch blocks
  // - 4 conditional branches
  // Total: 12 complexity

  if (!oldToken) { /* ... */ }

  try {
    const decoded = jwt.verify(oldToken);
    if (decoded.userId !== userId) { /* ... */ }

    try {
      const family = await getTokenFamily(decoded.family);
      if (family.revoked) { /* ... */ }
      if (family.tokens.includes(oldToken)) {
        // Nested logic
      }
    } catch { /* ... */ }
  } catch { /* ... */ }
}
```

**Recommendation**: Extract validation logic
```typescript
async function rotateRefreshToken(oldToken: string, userId: string) {
  validateTokenInput(oldToken);
  const decoded = await decodeAndVerifyToken(oldToken, userId);
  const family = await validateTokenFamily(decoded.family, oldToken);
  return await generateNewToken(family, userId);
}

// Each helper has complexity 3-4 (total unchanged, but more readable)
```

**Impact**: Medium (non-blocking, but improves maintainability)

---

## KISS Compliance Check

### ✅ Simplicity: PASSED
- **Abstraction Layers**: 2 (appropriate) ✅
- **Unnecessary Patterns**: 0 ✅
- **Premature Optimization**: 0 ✅
- **YAGNI Violations**: 0 ✅

**Simplicity Score**: 85/100 (target: >70) ✅

### ✅ Implementation Approach: GOOD
**Analysis**:
- OAuth2 implementation follows minimal subset approach ✅
- No over-engineering detected ✅
- Clear separation of concerns ✅
- Appropriate use of utility functions ✅

**Best Practices Followed**:
1. Simple token generation (JWT with RS256)
2. Straightforward refresh rotation (token families)
3. Clear error handling (no complex error hierarchies)
4. Minimal abstraction (no unnecessary factories or builders)

---

## Architectural Impact

### ✅ Architecture Consistency: PASSED
- **Module Boundaries**: Clean separation ✅
- **Dependencies**: Acyclic, no circular refs ✅
- **API Contracts**: Well-defined interfaces ✅
- **Data Flow**: Unidirectional, predictable ✅

**Impact Assessment**:
- New OAuth2 module integrates cleanly with existing auth system
- No breaking changes to existing APIs
- Session management enhanced (backward compatible)
- Database schema changes isolated (new tables only)

### ✅ Technical Debt: LOW
- **Code Duplication**: 8% (target: <15%) ✅
- **TODO Comments**: 2 (all documented in backlog) ✅
- **Deprecated APIs**: 0 ✅
- **Temporary Workarounds**: 0 ✅

---

## Security Basics

### ✅ Common Security Issues: PASSED
- **SQL Injection**: No unsanitized queries ✅
- **XSS Prevention**: Input validation present ✅
- **Secrets Management**: No hardcoded secrets ✅
- **Authentication**: Proper middleware usage ✅
- **Authorization**: Role checks in place ✅

**Security Scan**: 0 critical, 0 high, 2 medium issues

**Medium Issues** (Non-blocking):
1. Consider adding rate limiting to token endpoints
2. Add CSRF tokens for state-changing operations

**Note**: Full security audit recommended via security-auditor agent

---

## Test Coverage

### ✅ Unit Test Coverage: PASSED
- **Line Coverage**: 91% (target: >85%) ✅
- **Branch Coverage**: 87% (target: >80%) ✅
- **Function Coverage**: 95% (target: >90%) ✅
- **Statement Coverage**: 92% (target: >85%) ✅

**Coverage by File**:
```
File                  | Line % | Branch % | Func %
----------------------|--------|----------|--------
oauth2.ts             |   94%  |   89%    |  100%
token.ts              |   92%  |   88%    |   95%
password.ts           |   89%  |   85%    |   90%
session.ts            |   95%  |   92%    |  100%
middleware.ts         |   88%  |   82%    |   90%
utils.ts              |   90%  |   86%    |   95%
```

### ✅ Test Quality: GOOD
- Tests cover happy paths ✅
- Error cases tested ✅
- Edge cases covered (empty inputs, invalid tokens, etc.) ✅
- Integration scenarios validated ✅

---

## Auto-Fix Opportunities

### Available Auto-Fixes
The following issues can be automatically fixed:

1. **Add Missing JSDoc Comments** (2 functions)
   - Auto-generate JSDoc templates based on function signatures
   - Estimated time: 30 seconds

2. **Extract Duplicate Error Handlers** (3 locations)
   - Create shared utility function
   - Update call sites
   - Estimated time: 2 minutes

3. **Simplify rotateRefreshToken** (1 function)
   - Extract validation helpers
   - Reduce nesting
   - Estimated time: 5 minutes

Run with `--auto-fix` flag to apply automatically.

---

## Workflow State Update

**.workflow_state Updated**:
```
PHASE=QUALITY_GATE
STATUS=COMPLETED
QUALITY_GATE_PASSED=true
WARNINGS=3
BLOCKERS=0
CODE_HASH=abc123f
TIMESTAMP=2025-11-08T15:45:00Z
```

---

## Summary

### Quality Metrics
```
✅ Code Quality:        PASSED
✅ Maintainability:     PASSED (78/100)
✅ Complexity:          PASSED (Avg: 6)
✅ KISS Compliance:     PASSED (85/100)
✅ Architecture:        PASSED
✅ Security Basics:     PASSED
✅ Test Coverage:       PASSED (91%)

⚠️ Warnings:            3 (non-blocking)
🔴 Blockers:            0
```

### Final Verdict: ✅ QUALITY GATES PASSED

**Deployment Status**: APPROVED
- All critical gates passed ✅
- Warnings are non-blocking ⚠️
- Code meets quality standards ✅
- Ready for git-workflow-manager ✅

### Recommended Actions

**Optional Improvements** (Non-blocking):
1. Add JSDoc comments (improves DX)
2. Extract duplicate error handlers (reduces maintenance)
3. Simplify rotateRefreshToken (improves readability)

**Auto-fix Available**:
```bash
/run-quality-gates src/auth --auto-fix
```

This will automatically apply the 3 recommended improvements.

### Next Step

**Proceed to git-workflow-manager**:
Quality gates passed. Ready to create commit with spec reference.

```
/commit-with-spec spec-20251108-oauth2-implementation
```

---

**Quality Gate Duration**: 2 minutes 15 seconds
**Files Analyzed**: 8
**Issues Found**: 3 warnings, 0 blockers
**Recommendation**: Proceed to deployment ✅
```

This provides comprehensive quality validation with actionable recommendations and auto-fix options.
## See Also
For related commands, see [Quality Commands](../shared/related-quality-commands.md)
