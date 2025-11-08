# Load Telemetry

Load historical telemetry data for similar tasks to inform current work with data-driven recommendations.

## Usage
/load-telemetry [task-type] [--similar-to "description"] [--time-range 7d|30d|90d]

## What This Does
1. Queries telemetry for similar historical tasks and analyzes agent performance patterns
2. Identifies successful workflows and recommends optimal agents
3. Provides performance benchmarks, time estimates, and common pitfalls

## Example
/load-telemetry authentication --similar-to "oauth2 implementation" --time-range 30d

## Agent Coordination
1. **Main LLM**: Queries telemetry, aggregates metrics, identifies success patterns
2. **Recommendation Engine**: Suggests optimal workflow based on historical success rates

## Output
Data-driven analysis including:
```markdown
## Telemetry Analysis: Authentication Tasks

**Query**: Tasks similar to "oauth2 implementation"
**Time Range**: Last 30 days
**Matching Workflows**: 8 found
**Success Rate**: 87.5% (7 successful, 1 failed)

### Recommended Agent Workflow

Based on 7 successful similar workflows:

1. **design-simplicity-advisor** (100% used in successful workflows)
   - Average duration: 42 seconds
   - Success indicator: Recommends minimal implementation
   - Skip rate: 0% (always used)

2. **backend-architect** (100% used)
   - Average duration: 7 minutes 30 seconds
   - Common approach: Minimal OAuth2 subset implementation
   - Success factor: Focus on authorization_code flow only

3. **security-auditor** (100% used)
   - Average duration: 1 minute 15 seconds
   - Critical checks: JWT validation, PKCE support
   - Failure prevention: Catches 95% of security issues

4. **unit-test-expert** (100% used)
   - Average duration: 3 minutes 45 seconds
   - Coverage target: 85%+ for auth code
   - Success factor: Test both success and error paths

5. **qa-specialist** (71% used)
   - Average duration: 2 minutes 20 seconds
   - Focus: Integration testing of full flow
   - Optional: Can skip for simple implementations

### Performance Benchmarks

**Time Estimates** (based on successful workflows):
- Fastest: 8 minutes 15 seconds
- Average: 13 minutes 42 seconds
- Slowest: 22 minutes 10 seconds
- Your estimate: 12-15 minutes (normal range)

**Agent Performance**:
```
Agent                    | Avg Duration | Success Rate | Usage Rate
-------------------------|--------------|--------------|------------
design-simplicity-advisor|   45s       |    100%      |   100%
backend-architect        |  7m 30s     |    100%      |   100%
security-auditor         |  1m 15s     |    100%      |   100%
unit-test-expert         |  3m 45s     |     95%      |   100%
qa-specialist            |  2m 20s     |     85%      |    71%
git-workflow-manager     | <1m         |    100%      |   100%
```

### Success Patterns

**What worked well** (from successful workflows):
1. Always start with simplicity analysis
2. Implement minimal OAuth2 subset first
3. Focus on authorization_code flow only
4. Use JWT with RS256 signing
5. Implement PKCE for public clients
6. Comprehensive unit tests for auth logic
7. Security review catches issues early

**Common Pitfalls** (from failed workflow):
1. ❌ Implementing full OAuth2 spec (too complex)
2. ❌ Custom JWT implementation (security risks)
3. ❌ Skipping PKCE support (security gap)
4. ❌ Insufficient error handling tests

### Failure Analysis

**Failed Workflow** (wf-20251025-failed):
- Reason: Security vulnerabilities found in production
- Root cause: Skipped security-auditor step
- Impact: 4 hours of rework
- Lesson: Never skip security review for auth

### Recommendations

**Optimal Workflow** (92% confidence):
```
design-simplicity-advisor → backend-architect → security-auditor →
unit-test-expert → quality-gate → git-workflow-manager
```

**Time Estimate**: 13-15 minutes
**Success Probability**: 87% (based on historical data)
**Risk Level**: Low (with security review)

**Key Success Factors**:
1. Use design-simplicity-advisor recommendations
2. Don't over-engineer (minimal OAuth2 is sufficient)
3. Always run security-auditor
4. Test both happy path and error cases
5. Ensure PKCE validation is implemented

**Optional Optimizations**:
- Skip qa-specialist if unit tests cover integration scenarios
- Use quality-gate for unified validation (faster)

### Data-Driven Insights

- **Agent bottleneck**: backend-architect (55% of total time)
- **Quality predictor**: security-auditor finds issues 95% of time
- **Time saver**: Simplicity analysis prevents 40% of rework
- **Best practice**: All successful workflows used same agent sequence

Would you like to:
1. Start workflow with recommended agents
2. View detailed logs from successful workflows
3. Customize agent selection based on your specific needs
```

Returns: Actionable, data-driven recommendations based on real historical performance

## See Also
For related commands, see [Project Management Commands](../shared/related-pm-commands.md)
