# Load Specification

Load a specification file by ID and make it available to all agents in the current workflow.

## Usage
/load-spec [spec-id]

## What This Does
1. Locates specification file in specs/active/ or specs/completed/
2. Parses both Markdown and YAML versions
3. Displays spec summary (goals, design, tasks)
4. Sets environment variables for spec-driven workflow
5. Makes spec context available to all subsequent agent invocations

## Example
/load-spec spec-20251108-oauth2-implementation

## Agent Coordination
1. **Main LLM**: Locates and parses spec files
   - Reads specs/active/YYYY-MM-DD-feature-name.md
   - Reads specs/active/YYYY-MM-DD-feature-name.yaml
   - Validates spec format and completeness
2. **Environment Setup**: Sets context for workflow
   - `OAK_SPEC_ID=spec-20251108-oauth2-implementation`
   - `OAK_SPEC_PATH=/path/to/spec/file.yaml`
3. **All Subsequent Agents**: Receive spec context automatically
   - Agents can reference spec sections
   - Telemetry links to spec_id

## Output
Spec Summary:
```markdown
## Specification Loaded: OAuth2 Authentication Implementation

**Spec ID**: spec-20251108-oauth2-implementation
**Status**: Active
**Created**: 2025-11-08
**Last Updated**: 2025-11-08 14:30:00

### Goals
1. Implement OAuth2 authorization code flow
2. Support JWT token generation and validation
3. Implement refresh token rotation
4. Ensure PKCE support for public clients

### Technical Design
- Authorization endpoint: /oauth2/authorize
- Token endpoint: /oauth2/token
- Token storage: Redis with 1-hour expiration
- JWT signing: RS256 with rotation

### Implementation Tasks
- ✅ Task 1: Create OAuth2 endpoints (backend-architect)
- ✅ Task 2: Implement JWT handling (backend-architect)
- ⏳ Task 3: Add security validation (security-auditor)
- ⏳ Task 4: Create unit tests (unit-test-expert)
- ⏳ Task 5: Integration testing (qa-specialist)

### Acceptance Criteria
- [x] AC-1: Authorization code flow returns valid codes
- [x] AC-2: Token endpoint issues JWT tokens
- [ ] AC-3: Refresh tokens rotate on use
- [ ] AC-4: PKCE validation works correctly
- [ ] AC-5: All security tests pass

### Context Set
- Environment variable OAK_SPEC_ID set
- All agents will log to this spec's execution log
- Telemetry will link invocations to spec-20251108-oauth2-implementation
```

**Next Steps**: Agents invoked in this session will automatically:
- Reference this spec for context
- Log execution to spec's execution log (Section 5)
- Link telemetry with spec_id
- Validate against acceptance criteria
