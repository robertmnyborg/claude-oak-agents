# OaK Interactive Tutorial

Hands-on tutorial for learning the Claude OaK agent system through practical examples.

## Usage
/oak-tutorial [--skip-to step1|step2|step3|step4|step5]

## What This Does
1. Provides interactive, step-by-step tutorial
2. Walks through common workflows with real examples
3. Demonstrates spec creation, quality gates, and deployment
4. Includes hands-on exercises with validation
5. Teaches best practices and pro tips

## Example
/oak-tutorial
/oak-tutorial --skip-to step3

## Output
Interactive Tutorial:
```markdown
# Welcome to Claude OaK Agents Tutorial! 🚀

This interactive tutorial will teach you the core workflows of the Claude OaK system through hands-on examples.

**What you'll learn**:
1. Creating specifications with spec-manager
2. Running quality gates and validation
3. Creating spec-referenced commits
4. Analyzing code complexity
5. Checking deployment readiness

**Time required**: 20-30 minutes
**Prerequisites**: None (we'll guide you through everything)

---

## Step 1: Creating Your First Specification (5-7 minutes)

### Overview
Specifications are the foundation of OaK's spec-driven development. They help you:
- Define clear goals and requirements
- Plan implementation approach
- Track progress against acceptance criteria
- Create context for all agents

### Exercise: Create a Simple Feature Spec

Let's create a specification for a "User Password Reset" feature.

**Command**:
```
/generate-spec user-password-reset
```

**What happens next**:
1. spec-manager will greet you and explain the process
2. You'll co-author 4 sections with approval checkpoints
3. Both Markdown and YAML specs will be created
4. The spec will be saved to specs/active/

### Guided Example

**Section 1: Goals & Requirements**

spec-manager will propose:
```markdown
### Goals
1. Allow users to reset forgotten passwords securely
2. Send reset link via email
3. Expire reset links after 1 hour
4. Prevent brute force attacks

### Requirements
- Email delivery system
- Secure token generation
- Token expiration logic
- Rate limiting on reset requests
```

**Your turn**: Review and approve or modify

---

**Section 2: Technical Design**

spec-manager will propose:
```markdown
### Architecture
- Reset endpoint: /auth/reset-password
- Token storage: Redis (1-hour expiration)
- Email service: SendGrid integration

### Data Models
ResetToken:
  token: string (UUID)
  user_id: string
  expires_at: timestamp
  used: boolean
```

**Your turn**: Review the design, suggest changes if needed

---

**Section 3: Implementation Plan**

spec-manager will propose:
```markdown
### Tasks
1. Create reset endpoint (backend-architect, 2-3 hours)
2. Implement token generation (backend-architect, 1 hour)
3. Add email integration (backend-architect, 1-2 hours)
4. Add rate limiting (backend-architect, 1 hour)
5. Create unit tests (unit-test-expert, 2 hours)
6. Security review (security-auditor, 1 hour)
```

**Your turn**: Review the plan, adjust estimates if needed

---

**Section 4: Test Strategy**

spec-manager will propose:
```markdown
### Unit Tests
- Token generation and validation
- Token expiration logic
- Rate limiting functionality

### Integration Tests
- Full password reset flow
- Email delivery
- Token invalidation after use

### Acceptance Criteria
- [ ] AC-1: Reset link sent within 30 seconds
- [ ] AC-2: Token expires after 1 hour
- [ ] AC-3: Old tokens invalidated after use
- [ ] AC-4: Rate limit prevents abuse
```

**Your turn**: Review and approve

---

**Congratulations! 🎉**

You've created your first spec:
- **File**: `specs/active/2025-11-08-user-password-reset.md`
- **Spec ID**: `spec-20251108-user-password-reset`

**Key Takeaways**:
- ✅ Specs provide clear direction for implementation
- ✅ Co-authoring ensures alignment on approach
- ✅ Acceptance criteria define success
- ✅ Task estimates help with planning

**Pro Tip**: Always create specs for significant features (3+ hours of work)

---

**Ready for Step 2?** Press Enter to continue or type "skip" to jump ahead.

---

## Step 2: Loading Spec Context (2-3 minutes)

### Overview
Before implementing a feature, load the spec to:
- Make context available to all agents
- Link telemetry to the specification
- Track progress against acceptance criteria

### Exercise: Load the Spec You Created

**Command**:
```
/load-spec spec-20251108-user-password-reset
```

**Expected Output**:
```markdown
## Specification Loaded: User Password Reset

**Spec ID**: spec-20251108-user-password-reset
**Status**: Active
**Created**: 2025-11-08 16:45:00

### Goals
1. Allow users to reset forgotten passwords securely
2. Send reset link via email
3. Expire reset links after 1 hour
4. Prevent brute force attacks

### Implementation Tasks
- ⏸️ Task 1: Create reset endpoint (backend-architect)
- ⏸️ Task 2: Implement token generation (backend-architect)
- ⏸️ Task 3: Add email integration (backend-architect)
- ⏸️ Task 4: Add rate limiting (backend-architect)
- ⏸️ Task 5: Create unit tests (unit-test-expert)
- ⏸️ Task 6: Security review (security-auditor)

### Context Set
- Environment variable OAK_SPEC_ID set
- All agents will log to this spec's execution log
- Telemetry will link invocations to spec-20251108-user-password-reset
```

**What just happened**:
- Spec context loaded into environment
- All subsequent agents will reference this spec
- Workflow tracking linked to spec ID

**Key Takeaways**:
- ✅ Load specs before implementation
- ✅ Environment variables set automatically
- ✅ Agent invocations linked to spec

**Pro Tip**: Use /load-spec whenever resuming work on a feature

---

**Ready for Step 3?** Press Enter to continue.

---

## Step 3: Running Quality Gates (3-5 minutes)

### Overview
Quality gates validate code before committing to ensure:
- Code quality and maintainability
- KISS principle compliance
- No critical security issues
- Adequate test coverage

### Exercise: Analyze Sample Code

Let's analyze a code sample for quality issues.

**Sample Code** (simulated - create file `sample/password-reset.ts`):
```typescript
// Password reset implementation
export async function resetPassword(token: string, newPassword: string) {
  const decoded = jwt.verify(token, process.env.JWT_SECRET);
  const user = await db.users.findOne({ id: decoded.userId });

  if (!user) throw new Error('User not found');
  if (decoded.exp < Date.now()) throw new Error('Token expired');

  user.password = bcrypt.hashSync(newPassword, 10);
  await user.save();

  return { success: true };
}
```

**Command**:
```
/run-quality-gates sample/password-reset.ts
```

**Expected Output**:
```markdown
## Quality Gate Validation Report

### Overall Result: ⚠️ PASSED WITH WARNINGS

**Status**: Quality gates passed, but 2 warnings should be addressed

---

## Issues Found

### ⚠️ WARNING: Missing Error Handling
**Location**: Line 4
**Issue**: jwt.verify can throw errors that aren't caught
**Recommendation**: Wrap in try-catch block

### ⚠️ WARNING: Synchronous Password Hashing
**Location**: Line 10
**Issue**: bcrypt.hashSync blocks event loop
**Recommendation**: Use bcrypt.hash (async version)

### ✅ GOOD: Input Validation Present
Token and password validated before use

### ✅ GOOD: Password Hashing
Using bcrypt with appropriate salt rounds
```

**What to do with warnings**:
1. Review each warning
2. Decide: fix now or accept technical debt
3. Non-blocking warnings allow commit
4. Critical issues would block commit

**Key Takeaways**:
- ✅ Quality gates catch issues before commit
- ✅ Warnings are informative but non-blocking
- ✅ Critical issues block commits
- ✅ Auto-fix available for some issues

**Pro Tip**: Run quality gates frequently during development, not just before commit

---

**Exercise: Fix the Warnings**

**Improved Code**:
```typescript
export async function resetPassword(token: string, newPassword: string) {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await db.users.findOne({ id: decoded.userId });

    if (!user) throw new Error('User not found');
    if (decoded.exp < Date.now()) throw new Error('Token expired');

    user.password = await bcrypt.hash(newPassword, 10);  // Async!
    await user.save();

    return { success: true };
  } catch (error) {
    logger.error('Password reset failed:', error);
    throw new AuthError('Invalid or expired reset token');
  }
}
```

**Run quality gates again**:
```
/run-quality-gates sample/password-reset.ts
```

**Expected**: ✅ All checks passed

---

**Ready for Step 4?** Press Enter to continue.

---

## Step 4: Creating Spec-Referenced Commits (3-4 minutes)

### Overview
Spec-referenced commits:
- Link commits to specifications
- Include acceptance criteria satisfied
- Provide complete context for code review
- Enable traceability from spec to code

### Exercise: Create a Commit

Assuming you've implemented the password reset feature...

**Command**:
```
/commit-with-spec spec-20251108-user-password-reset
```

**Expected Output**:
```markdown
## Creating Commit with Spec Reference

**Spec ID**: spec-20251108-user-password-reset
**Files changed**: 3
- src/auth/reset.ts (new)
- src/auth/tokens.ts (modified)
- tests/auth/reset.test.ts (new)

**Acceptance Criteria Satisfied**:
- AC-1: Reset link sent within 30 seconds ✅
- AC-2: Token expires after 1 hour ✅
- AC-3: Old tokens invalidated after use ✅

**Commit Message Preview**:
```
feat: Implement user password reset functionality

- Add /auth/reset-password endpoint
- Implement secure token generation with 1-hour expiration
- Add email integration for reset links
- Implement rate limiting to prevent abuse

Spec: spec-20251108-user-password-reset
Acceptance Criteria: AC-1, AC-2, AC-3 satisfied

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Approve commit?** [Y/n]: y

**Commit created**: abc123f
```

**Key Takeaways**:
- ✅ Commits reference specs automatically
- ✅ Acceptance criteria tracked in commit message
- ✅ Complete context for code review
- ✅ Claude Code attribution included

**Pro Tip**: Always use /commit-with-spec for spec-driven work

---

**Ready for Step 5?** Press Enter to continue.

---

## Step 5: Deployment Readiness Check (4-5 minutes)

### Overview
Before deploying, validate:
- All tests pass
- No security vulnerabilities
- Dependencies are healthy
- Configuration is correct

### Exercise: Check Deployment Readiness

**Command**:
```
/deploy-check --environment staging
```

**Expected Output**:
```markdown
## Deployment Readiness Check

**Environment**: Staging
**Overall Status**: ✅ READY FOR DEPLOYMENT

---

## Validation Results

### ✅ Quality Gates: PASSED
- Code review: ✅
- Complexity: ✅ (Avg: 6)
- Test coverage: ✅ (92%)

### ✅ Unit Tests: PASSED
- Tests run: 45
- Passed: 45 (100%)
- Coverage: 92%

### ✅ Security: PASSED
- No critical issues
- 2 medium issues (non-blocking for staging)

### ✅ Dependencies: HEALTHY
- No vulnerable dependencies
- All up to date

### ✅ Configuration: VALID
- All required env vars set
- Database migrations applied
- Infrastructure healthy

---

## Deployment Recommendation: ✅ APPROVED FOR STAGING

**Next Steps**:
1. Deploy to staging
2. Run smoke tests
3. Monitor for errors
4. Run /deploy-check --environment production before prod deploy
```

**Key Takeaways**:
- ✅ Comprehensive pre-deployment validation
- ✅ Go/no-go recommendation provided
- ✅ Issues flagged with severity and remediation
- ✅ Different validation for staging vs production

**Pro Tip**: Always run deployment check before deploying to any environment

---

## Tutorial Complete! 🎉

### What You've Learned

1. **Specification Creation**
   - Co-authoring with spec-manager
   - Approval checkpoints for alignment
   - Both human-readable and machine-readable formats

2. **Context Loading**
   - Loading specs before implementation
   - Environment variable setup
   - Agent invocation tracking

3. **Quality Gates**
   - Running quality validation
   - Understanding warnings vs blockers
   - Auto-fix for common issues

4. **Spec-Referenced Commits**
   - Linking commits to specifications
   - Tracking acceptance criteria
   - Professional commit messages

5. **Deployment Checks**
   - Comprehensive pre-deployment validation
   - Go/no-go recommendations
   - Environment-specific validation

---

## Next Steps

### Practice Workflows

**Try these common workflows**:

1. **Full Feature Development**:
   ```
   /generate-spec [your-feature]
   /load-spec [spec-id]
   [implement code]
   /run-quality-gates [path]
   /commit-with-spec [spec-id]
   /pr-with-context [spec-id]
   ```

2. **Code Quality Improvement**:
   ```
   /analyze-complexity src/
   /security-scan src/
   /run-quality-gates src/
   [fix issues]
   /deploy-check --environment staging
   ```

3. **Telemetry-Driven Development**:
   ```
   /load-telemetry [task-type]
   /suggest-next-task
   /load-spec [recommended-spec]
   [execute task]
   ```

### Resources

**Documentation**:
- Full command reference: `/oak-help`
- System status: `/oak-status-detailed`
- Agent capabilities: `/oak-help [agent-name]`

**Getting Help**:
- GitHub Discussions: Community questions and examples
- GitHub Issues: Bug reports and feature requests
- Documentation: docs/ directory

---

## Pro Tips Summary

1. ✅ Create specs for significant features (3+ hours)
2. ✅ Load specs before implementation
3. ✅ Run quality gates frequently during development
4. ✅ Use spec-referenced commits for traceability
5. ✅ Always run deployment check before deploying
6. ✅ Use /oak-help for command-specific assistance
7. ✅ Check /oak-status-detailed for system overview
8. ✅ Leverage telemetry for data-driven decisions

---

## Feedback

**How was this tutorial?**
- Helpful? Let us know in GitHub Discussions
- Found issues? Report in GitHub Issues
- Want more tutorials? Suggest topics in Discussions

**Thank you for completing the Claude OaK tutorial!** 🚀

You're now ready to use the full OaK agent system for productive development.

---

**Want to restart or skip to specific steps?**
```
/oak-tutorial                  # Restart from beginning
/oak-tutorial --skip-to step1  # Skip to spec creation
/oak-tutorial --skip-to step3  # Skip to quality gates
```
```

This provides a comprehensive, hands-on tutorial with realistic examples and exercises.
