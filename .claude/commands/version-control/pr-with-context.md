# Pull Request with Full Context

Create comprehensive pull request with specification, telemetry data, and complete execution context.

## Usage
/pr-with-context [spec-id] [--include-telemetry] [--include-agent-log]

## What This Does
1. Gathers all relevant context including spec and agent execution data
2. Formats comprehensive PR description with acceptance criteria
3. Optionally includes telemetry showing agent performance metrics
4. Creates PR using gh CLI via git-workflow-manager

## Example
/pr-with-context spec-20251108-oauth2 --include-telemetry

## Agent Coordination
1. **Main LLM**: Gathers context (spec files, telemetry, agent logs)
2. **git-workflow-manager**: Creates PR with enhanced description

## Output
PR with comprehensive description including:
```markdown
## Summary
[Spec objective summary]

## Specification Reference
- Spec ID: spec-20251108-oauth2-implementation
- Title: OAuth2 Authentication Flow
- Status: Completed

## Changes
[Automatically generated from git diff]

## Acceptance Criteria
- [x] AC-1: Authorization code flow implemented
- [x] AC-2: JWT token generation configured
- [x] AC-3: Refresh token rotation working

## Agent Workflow (Optional)
1. design-simplicity-advisor (45s) - Recommended minimal OAuth2 implementation
2. backend-architect (8.2min) - Implemented core endpoints
3. security-auditor (1.2min) - Validated security patterns
4. unit-test-expert (3.1min) - Created comprehensive test suite

## Performance Metrics (Optional)
- Total workflow time: 12.5 minutes
- Quality gate: PASSED
- Test coverage: 94%

## Test Plan
- [ ] Manual testing of authorization flow
- [ ] Verify JWT token structure
- [ ] Test refresh token rotation
- [ ] Security review in staging environment

🤖 Generated with Claude Code
```

Returns: PR URL for review

## See Also
For related commands, see [Git Commands](../shared/related-git-commands.md)
