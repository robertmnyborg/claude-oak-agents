# Suggest Next Task

AI-driven task prioritization based on specs, telemetry patterns, and dependency analysis.

## Usage
/suggest-next-task [--context spec|backlog|bugs|all]

## What This Does
1. Analyzes active specifications and their completion status
2. Queries telemetry for workflow patterns and bottlenecks
3. Identifies task dependencies and blockers
4. Evaluates impact and effort estimates
5. Recommends optimal next task with justification
6. Provides alternative options with trade-offs

## Example
/suggest-next-task --context all

## Agent Coordination
1. **Main LLM**: Gathers context from multiple sources
   - Reads active specs from specs/active/
   - Queries telemetry for recent workflows
   - Analyzes backlog and open issues
2. **product-strategist**: Evaluates business impact
   - Prioritizes by user value
   - Considers strategic alignment
3. **project-manager**: Assesses dependencies and resources
   - Identifies blockers
   - Estimates effort and risk
4. **Main LLM**: Synthesizes recommendation

## Output
Next Task Recommendation:
```markdown
## AI-Recommended Next Task

### Primary Recommendation: Implement Refresh Token Rotation

**Task ID**: spec-20251108-oauth2-implementation / Task 3.2
**Priority**: P0 (Critical)
**Estimated Effort**: 2-3 hours
**Confidence**: 92%

### Why This Task?

**1. Unblocks Critical Path** (High Impact)
- Blocks completion of OAuth2 implementation (P0 initiative)
- Required for security audit (scheduled next week)
- Prevents 2 other tasks from starting

**2. High Business Value**
- Security improvement (prevents token theft)
- Required for SOC 2 compliance
- Affects 100% of authenticated users

**3. Optimal Timing**
- Dependencies satisfied: JWT implementation complete ✓
- Resources available: backend-architect free
- No blockers identified

**4. Historical Success Pattern**
- Similar tasks completed successfully 5/5 times
- Average duration: 2.1 hours (matches estimate)
- Zero rework required historically

### Task Details

**Specification**: spec-20251108-oauth2-implementation
**Section**: 3.2 - Refresh Token Rotation

**Description**:
Implement automatic refresh token rotation when access tokens are refreshed. Old refresh tokens should be invalidated immediately after use to prevent token reuse attacks.

**Acceptance Criteria**:
- [ ] AC-3.2.1: Refresh endpoint rotates tokens on each use
- [ ] AC-3.2.2: Old refresh tokens invalidated immediately
- [ ] AC-3.2.3: Token family tracking prevents token reuse
- [ ] AC-3.2.4: Concurrent refresh requests handled safely

**Technical Requirements**:
- Update /oauth2/token endpoint
- Implement token family tracking in Redis
- Add concurrent request detection
- Update unit tests for rotation scenarios

**Dependencies**:
- ✅ JWT implementation (Task 3.1) - COMPLETED
- ✅ Redis session storage (Task 2.3) - COMPLETED
- ⏸️ Security audit (blocked by this task)

### Recommended Agent Workflow

**Estimated Time**: 2-3 hours
**Agents Required**: 3

```
1. design-simplicity-advisor (5 min)
   - Review rotation approach
   - Validate simplicity (no over-engineering)
   - Confirm KISS compliance

2. backend-architect (90-120 min)
   - Implement token rotation logic
   - Add Redis token family tracking
   - Handle concurrent refresh scenarios
   - Update OpenAPI documentation

3. unit-test-expert (30-45 min)
   - Test successful rotation
   - Test token invalidation
   - Test concurrent requests
   - Test token reuse prevention

4. security-auditor (15-20 min)
   - Validate rotation security
   - Check for race conditions
   - Verify token invalidation

5. quality-gate (10 min)
   - Unified validation
   - Code review
   - Complexity check

6. git-workflow-manager (5 min)
   - Create commit with spec reference
   - Link to spec-20251108-oauth2-implementation
```

**Total Estimated Time**: 2.5-3.3 hours

### Impact Assessment

**Immediate Impact**:
- Unblocks security audit (scheduled Nov 12)
- Completes 60% of OAuth2 implementation
- Reduces security risk (token theft prevention)

**Business Impact**:
- Security: HIGH (prevents token theft attacks)
- User Experience: NONE (transparent to users)
- Compliance: HIGH (required for SOC 2)

**Technical Impact**:
- Code changes: 1 file (src/api/oauth2/token.ts)
- Test changes: 1 file (tests/oauth2/rotation.test.ts)
- Database: Redis schema update (token families)

### Risk Assessment

**Risks**: LOW
- Simple implementation (well-documented pattern)
- Historical success rate: 100%
- No known edge cases beyond concurrent requests

**Mitigation**:
- Use distributed lock for concurrent requests
- Comprehensive test coverage for rotation scenarios
- Security auditor validation before deployment

### Alternative Options

#### Option 2: Implement PKCE Validation (spec-20251108-oauth2 / Task 3.3)
- **Priority**: P1 (High)
- **Effort**: 3-4 hours
- **Why not primary**: More complex, not blocking audit
- **Trade-off**: Can be done after security audit

#### Option 3: Fix Email Verification Bug (backlog-email-001)
- **Priority**: P2 (Medium)
- **Effort**: 1-2 hours
- **Why not primary**: Lower impact, not blocking anything
- **Trade-off**: Quick win but less strategic value

#### Option 4: Update API Documentation (spec-20251108-oauth2 / Task 5.1)
- **Priority**: P3 (Low)
- **Effort**: 1 hour
- **Why not primary**: Can wait until implementation complete
- **Trade-off**: Easy task but low impact

### Decision Matrix

```
Task                    | Impact | Urgency | Effort | Blockers | Score
------------------------|--------|---------|--------|----------|-------
Refresh Token Rotation  | HIGH   | HIGH    | MED    |    0     |  92
PKCE Validation         | HIGH   | MED     | MED    |    0     |  78
Email Bug Fix           | MED    | LOW     | LOW    |    0     |  54
Update Docs             | LOW    | LOW     | LOW    |    0     |  38
```

**Score Calculation**: (Impact × 10 + Urgency × 8 + (10 - Effort) × 5 - Blockers × 20) / 3

### Telemetry Insights

**Similar Tasks** (historical performance):
- Token rotation implementations: 5 completed, 0 failed
- Average duration: 2.1 hours (range: 1.8-2.5 hours)
- Common pattern: backend-architect → security-auditor → tests
- Success factor: Always include concurrent request tests

**Agent Performance** (for this task type):
- backend-architect: 100% success rate, 1.9 hour avg
- security-auditor: 100% success rate, 18 min avg
- unit-test-expert: 95% success rate, 42 min avg

**Recommended Time**:
Based on telemetry, allocate 2.5 hours to complete with buffer.

### Next Steps

**If you accept this recommendation**:
```
1. Load specification: /load-spec spec-20251108-oauth2-implementation
2. Start workflow with recommended agents
3. Expected completion: 2.5-3.3 hours
4. Next task after this: PKCE Validation (Task 3.3)
```

**If you want alternatives**:
- Option 2: PKCE Validation (higher effort, similar impact)
- Option 3: Email Bug Fix (quick win, lower impact)
- Option 4: Update Docs (easy, low impact)

**If you want different context**:
- Focus on bugs only: /suggest-next-task --context bugs
- Focus on backlog: /suggest-next-task --context backlog
- Focus on specs: /suggest-next-task --context spec

### Confidence Explanation

**92% Confidence** based on:
- Clear dependencies (100% satisfied)
- Historical success pattern (5/5 completed)
- Well-defined acceptance criteria
- No known blockers
- Agent availability confirmed
- Effort estimate validated by telemetry

**Uncertainty factors** (8%):
- Concurrent request handling may reveal edge cases
- Security auditor may identify additional requirements

Would you like to proceed with this recommendation?
```

This provides data-driven task prioritization with clear justification and alternatives.
## See Also
For related commands, see [Quality Commands](../shared/related-quality-commands.md)
