# Generate Specification

Start an interactive specification creation workflow using the spec-manager agent.

## Usage
/generate-spec [feature-name]

## What This Does
1. Initiates spec-manager workflow for collaborative spec creation
2. Guides you through interactive co-authoring process
3. Creates both Markdown (human-readable) and YAML (machine-readable) specs
4. Saves to specs/active/ directory with timestamped filename
5. Sets up spec for implementation workflow

## Example
/generate-spec oauth2-authentication

## Agent Coordination
1. **spec-manager**: Primary workflow coordinator
   - Interactive co-authoring of spec sections
   - Section 1: Goals & Requirements (with approval)
   - Section 2: Technical Design (with approval)
   - Section 3: Implementation Plan (with approval)
   - Section 4: Test Strategy (with approval)
   - YAML translation and task decomposition
2. **User**: Provides input and approval at each checkpoint

## Output
Interactive Spec Creation Process:

```markdown
## Let's Create a Specification for: OAuth2 Authentication

I'll guide you through creating a comprehensive spec. We'll work section by section with approval checkpoints.

### Section 1: Goals & Requirements

**What are we building and why?**

I'll start with a draft based on your feature name. Please review and approve or modify:

**Draft Goals**:
1. Implement OAuth2 authorization code flow for third-party integrations
2. Support secure token exchange with JWT
3. Enable refresh token rotation for long-lived sessions
4. Ensure PKCE support for public clients (mobile apps)

**Requirements**:
- OAuth2 2.0 RFC 6749 compliance
- PKCE (RFC 7636) support
- JWT token format (RFC 7519)
- Token expiration and refresh
- Secure client credential storage

**Success Criteria**:
- Third-party apps can authenticate users
- Tokens expire and refresh automatically
- PKCE prevents authorization code interception
- Passes security audit

[User reviews and approves or modifies]

### Section 2: Technical Design

**How will it work?**

**Draft Design**:

**Architecture**:
- Authorization endpoint: /oauth2/authorize
- Token endpoint: /oauth2/token
- Token storage: Redis (1-hour expiration)
- Client credentials: PostgreSQL
- JWT signing: RS256 with key rotation

**Data Models**:
```yaml
AuthorizationCode:
  code: string (UUID)
  client_id: string
  user_id: string
  redirect_uri: string
  code_challenge: string
  code_challenge_method: string
  expires_at: timestamp
  created_at: timestamp

AccessToken:
  token: string (JWT)
  client_id: string
  user_id: string
  scope: string[]
  expires_at: timestamp
  refresh_token: string

Client:
  client_id: string
  client_secret: string (hashed)
  redirect_uris: string[]
  allowed_scopes: string[]
```

**API Endpoints**:
- GET /oauth2/authorize - Authorization request
- POST /oauth2/token - Token exchange
- POST /oauth2/revoke - Token revocation

[User reviews and approves or modifies]

### Section 3: Implementation Plan

**What needs to be built?**

**Draft Plan**:

**Task 1**: Create OAuth2 endpoints (backend-architect)
- Implement /authorize endpoint
- Implement /token endpoint
- Handle PKCE validation
- Estimated time: 6-8 hours

**Task 2**: Implement JWT handling (backend-architect)
- JWT generation with RS256
- Token validation and parsing
- Key rotation mechanism
- Estimated time: 3-4 hours

**Task 3**: Add security validation (security-auditor)
- Review OAuth2 implementation
- Validate PKCE handling
- Check token security
- Estimated time: 1-2 hours

**Task 4**: Create unit tests (unit-test-expert)
- Test authorization code flow
- Test token exchange
- Test PKCE validation
- Test error cases
- Estimated time: 3-4 hours

**Task 5**: Integration testing (qa-specialist)
- End-to-end OAuth2 flow
- Third-party app integration
- Token refresh scenarios
- Estimated time: 2-3 hours

[User reviews and approves or modifies]

### Section 4: Test Strategy

**How do we validate it works?**

**Draft Test Strategy**:

**Unit Tests** (85%+ coverage):
- Authorization code generation
- PKCE challenge validation
- JWT token creation and parsing
- Token expiration handling
- Error cases (invalid client, expired code, etc.)

**Integration Tests**:
- Full OAuth2 flow (authorize → token)
- Token refresh flow
- PKCE authorization flow
- Token revocation

**Security Tests**:
- Authorization code interception (PKCE prevents)
- Token tampering detection
- Expired token rejection
- Invalid client rejection

**Acceptance Criteria**:
- [ ] AC-1: Authorization code flow completes successfully
- [ ] AC-2: JWT tokens are issued and validated
- [ ] AC-3: Refresh tokens rotate on use
- [ ] AC-4: PKCE validation prevents code interception
- [ ] AC-5: All security tests pass
- [ ] AC-6: Integration with test third-party app works

[User reviews and approves]

---

## Spec Creation Complete!

**Files created**:
- `specs/active/2025-11-08-oauth2-authentication.md` (Human-readable)
- `specs/active/2025-11-08-oauth2-authentication.yaml` (Machine-readable)

**Spec ID**: spec-20251108-oauth2-authentication

**Next Steps**:
1. Load this spec: `/load-spec spec-20251108-oauth2-authentication`
2. Start implementation with agents (I'll coordinate)
3. Agents will log to this spec's execution log
4. Track progress against acceptance criteria

Would you like to start implementation now?
```

The spec-manager creates a collaborative, approval-driven workflow that ensures alignment before implementation begins.
## See Also
For related commands, see [Quality Commands](../shared/related-quality-commands.md)
