# Deployment Readiness Check

Run comprehensive pre-deployment validation including quality gates, tests, security, and performance checks.

## Usage
/deploy-check [--environment staging|production] [--strict]

## What This Does
1. Validates all quality gates passed
2. Runs comprehensive test suite
3. Performs security audit
4. Checks performance benchmarks
5. Validates configuration and environment variables
6. Generates go/no-go deployment recommendation

## Example
/deploy-check --environment production --strict

## Agent Coordination
1. **quality-gate**: Unified quality validation
   - Code review compliance
   - Complexity analysis
   - KISS principle validation
2. **unit-test-expert**: Test execution
   - Runs full test suite
   - Validates coverage thresholds
3. **security-auditor**: Security validation
   - Scans for vulnerabilities
   - Validates auth/authz
4. **dependency-scanner**: Dependency checks
   - Checks for CVEs
   - License compliance
5. **Main LLM**: Synthesizes results and recommendation

## Output
Deployment Readiness Report:
```markdown
## Deployment Readiness Check

**Environment**: Production
**Mode**: Strict (zero tolerance for failures)
**Date**: 2025-11-08 15:30:00
**Branch**: main (commit: abc123f)

### Overall Status: 🔴 NOT READY FOR DEPLOYMENT

**Recommendation**: DO NOT DEPLOY - Critical issues found

**Blockers**: 2 critical issues must be resolved
**Warnings**: 4 issues should be addressed

---

## Quality Gate Validation

### ✅ Code Review: PASSED
- All changed files reviewed
- No critical code smells detected
- Maintainability score: 82/100 (target: >65)
- Technical debt: Low

### ✅ Complexity Analysis: PASSED
- Average cyclomatic complexity: 8 (target: <10)
- Maximum nesting depth: 3 (target: <4)
- YAGNI violations: 0
- Over-engineering score: 15/100 (low)

### ⚠️ KISS Validation: WARNING
- 2 functions flagged as over-complex
- Recommendation: Simplify before deployment
- Non-blocking but should be addressed

**Details**:
- `src/auth/token.ts:validateToken()` - 3 levels of nested conditionals
- `src/api/users.ts:getUserData()` - Complex query builder (can be simplified)

---

## Test Suite Execution

### ❌ Unit Tests: FAILED
- Tests run: 456
- Passed: 448 (98.2%)
- **Failed: 8** (1.8%) 🔴
- Skipped: 0
- Coverage: 87.3% (target: >85%) ✅

**Failed Tests** (BLOCKING):
```
1. src/auth/oauth2.test.ts:142 - Token rotation invalidates old tokens
   Error: Expected old token to be invalid, but it was accepted

2. src/auth/oauth2.test.ts:156 - Concurrent refresh requests handled safely
   Error: Race condition detected - both requests succeeded

3-8. [Additional test failures...]
```

**Action Required**: Fix failing tests before deployment

### ✅ Integration Tests: PASSED
- Tests run: 34
- Passed: 34 (100%)
- Duration: 2 minutes 15 seconds

### ✅ E2E Tests: PASSED
- Tests run: 12
- Passed: 12 (100%)
- Duration: 4 minutes 32 seconds

---

## Security Audit

### ❌ Security Vulnerabilities: CRITICAL ISSUES FOUND
- **Critical**: 1 🔴
- **High**: 2 ⚠️
- **Medium**: 5
- **Low**: 8

**CRITICAL** (BLOCKING):
```
1. Hardcoded Secret in Code
   File: src/config/db.ts:15
   Issue: JWT_SECRET hardcoded in source code
   Impact: Credential exposure in version control
   Fix: Move to environment variable

   Current:
   const JWT_SECRET = 'prod_secret_key_abc123';

   Required:
   const JWT_SECRET = process.env.JWT_SECRET;
```

**HIGH** (Should Fix):
```
2. SQL Injection Risk
   File: src/api/users.ts:67
   Issue: Unsanitized user input in query
   Impact: Database compromise
   Fix: Use parameterized queries

3. Missing Rate Limiting
   File: src/api/auth.ts:23
   Issue: No rate limiting on /auth/login
   Impact: Brute force attacks possible
   Fix: Add rate limiting middleware
```

**Action Required**: Fix critical and high severity issues before production deployment

### ⚠️ Authentication/Authorization: WARNING
- JWT validation: SECURE ✅
- Password hashing: SECURE (bcrypt) ✅
- Session management: SECURE ✅
- CORS configuration: **TOO PERMISSIVE** ⚠️

**CORS Issue**:
```javascript
// Current (too permissive)
cors({ origin: '*' })

// Required for production
cors({ origin: ['https://app.example.com', 'https://www.example.com'] })
```

---

## Dependency Security

### ⚠️ Dependency Vulnerabilities: WARNINGS
- Total dependencies: 156
- Vulnerable: 3 (2 medium, 1 low)
- Outdated: 12
- License issues: 0

**Medium Severity**:
```
1. axios@1.3.0
   CVE-2023-45857: Server-Side Request Forgery
   Fix: Upgrade to axios@1.6.0
   Breaking: None

2. express@4.18.0
   CVE-2023-44444: Denial of Service
   Fix: Upgrade to express@4.18.2
   Breaking: None
```

**Action**: Upgrade vulnerable dependencies (non-blocking for staging, blocking for production)

---

## Performance Benchmarks

### ✅ Performance: PASSED
- API response time: 142ms avg (target: <200ms) ✅
- Database query time: 23ms avg (target: <50ms) ✅
- Memory usage: 156MB (target: <512MB) ✅
- CPU usage: 12% avg (target: <50%) ✅

### ✅ Load Testing: PASSED
- Concurrent users: 1000 (target: >500) ✅
- Requests per second: 450 (target: >200) ✅
- Error rate: 0.02% (target: <1%) ✅

---

## Configuration Validation

### ❌ Environment Variables: MISSING REQUIRED VARS
- **Missing** (BLOCKING):
  - `JWT_SECRET` - Required for token signing 🔴
  - `DATABASE_PASSWORD` - Database connection 🔴
  - `REDIS_PASSWORD` - Session store 🔴

- **Optional Missing**:
  - `SENTRY_DSN` - Error tracking (recommended)
  - `LOG_LEVEL` - Defaults to 'info' (OK)

**Action Required**: Set all required environment variables before deployment

### ✅ Database Migrations: UP TO DATE
- Pending migrations: 0
- Last migration: 2025-11-08-001-add-oauth2-tables
- Migration status: Applied successfully ✅

### ✅ Infrastructure: READY
- Redis connection: HEALTHY ✅
- PostgreSQL connection: HEALTHY ✅
- External APIs: ALL REACHABLE ✅

---

## Git Workflow Validation

### ✅ Git Status: CLEAN
- Uncommitted changes: 0
- Untracked files: 0
- Branch: main
- Latest commit: abc123f - "feat: Implement OAuth2 refresh token rotation"

### ✅ Branch Protection: PASSED
- All commits on main have PR approval ✅
- All quality gates passed in CI ✅
- No force pushes detected ✅

---

## Deployment Checklist

### Critical (MUST FIX) 🔴
- [ ] Fix 8 failing unit tests
- [ ] Remove hardcoded JWT_SECRET from code
- [ ] Set required environment variables (JWT_SECRET, DB_PASSWORD, REDIS_PASSWORD)

### High Priority (SHOULD FIX) ⚠️
- [ ] Fix SQL injection vulnerability
- [ ] Add rate limiting to auth endpoints
- [ ] Restrict CORS to specific origins
- [ ] Upgrade vulnerable dependencies (axios, express)

### Recommended (NICE TO HAVE) ℹ️
- [ ] Simplify over-complex functions
- [ ] Set SENTRY_DSN for error tracking
- [ ] Document new OAuth2 features

---

## Deployment Recommendation

### 🔴 DO NOT DEPLOY TO PRODUCTION

**Reason**: 2 critical blocking issues found

**Blockers**:
1. **Unit tests failing** - 8 tests must pass before deployment
2. **Critical security issue** - Hardcoded secret must be removed

**Estimated Time to Fix**: 1-2 hours
- Fix failing tests: 45-60 minutes
- Remove hardcoded secrets: 15 minutes
- Set environment variables: 15 minutes
- Re-run validation: 15 minutes

**Recommended Actions**:
1. Fix failing OAuth2 token rotation tests
2. Move JWT_SECRET to environment variable
3. Set all required environment variables in production
4. Re-run deployment check: `/deploy-check --environment production`
5. Fix high-priority issues (SQL injection, rate limiting)
6. Deploy to staging first for final validation

### ✅ APPROVED FOR STAGING DEPLOYMENT

Staging deployment can proceed with current warnings. Fix critical issues before promoting to production.

---

## Next Steps

**Immediate** (Before Production):
```bash
# 1. Fix failing tests
npm run test:fix

# 2. Remove hardcoded secrets
# Edit src/config/db.ts - use process.env.JWT_SECRET

# 3. Set environment variables in production
# Configure in deployment platform (Heroku, AWS, etc.)

# 4. Upgrade vulnerable dependencies
npm update axios@1.6.0 express@4.18.2

# 5. Re-run deployment check
/deploy-check --environment production --strict
```

**Post-deployment**:
- Monitor error rates in production
- Set up Sentry for error tracking
- Schedule security audit for next sprint

---

## Summary

- **Quality Gates**: 3/4 passed (1 warning)
- **Tests**: 2/3 passed (unit tests failing) 🔴
- **Security**: Critical issues found 🔴
- **Performance**: All benchmarks passed ✅
- **Configuration**: Missing required vars 🔴
- **Dependencies**: Minor vulnerabilities ⚠️

**Estimated Time to Production Ready**: 1-2 hours of fixes

Would you like help fixing the blocking issues?
```

This provides a comprehensive go/no-go deployment assessment with actionable next steps.
