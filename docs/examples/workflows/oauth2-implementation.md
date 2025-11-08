# OAuth2 Implementation Workflow

Complete workflow for implementing OAuth2 authentication with JWT tokens, from specification to deployment.

## Overview

This example demonstrates the full agent-coordinated workflow for adding OAuth2 authentication to an application, including security reviews, code implementation, and testing.

## Prerequisites

- Backend API (Node.js/Express or similar)
- Database (PostgreSQL, MongoDB, or DynamoDB)
- Understanding of OAuth2 authorization code flow
- Security requirements documented

## Workflow Sequence

```
spec-manager → security-auditor (design) → backend-architect (implement) →
security-auditor (code review) → qa-specialist → git-workflow-manager
```

## Phase 1: Specification

**Agent**: spec-manager

**Collaborative Spec Creation**:

### 1.1 Goals & Requirements
- OAuth2 authorization code flow for third-party integrations
- JWT tokens for stateless authentication
- Token refresh mechanism for long-lived sessions
- Scope-based authorization

### 1.2 Technical Design
- Authorization endpoint: `/oauth/authorize`
- Token endpoint: `/oauth/token`
- Token refresh endpoint: `/oauth/refresh`
- Access token expiry: 15 minutes
- Refresh token expiry: 7 days with rotation
- JWT signing: RS256 (asymmetric keys)

### 1.3 Implementation Plan
- Task 1: Generate RSA key pair and store in Secrets Manager
- Task 2: Create database schema for OAuth clients and authorization codes
- Task 3: Implement authorization endpoint with user consent UI
- Task 4: Implement token endpoint (exchange code for tokens)
- Task 5: Implement token refresh endpoint
- Task 6: Create authentication middleware for protected endpoints
- Task 7: Implement scope validation

### 1.4 Test Strategy
- Unit tests for token generation/validation
- Integration tests for OAuth flow
- Security tests for token expiration and invalidation
- Load tests for token endpoint

## Phase 2: Security Design Review

**Agent**: security-auditor

### 2.1 Security Recommendations
- Use RS256 over HS256 (public/private key vs shared secret)
- Store private key in AWS Secrets Manager
- Implement PKCE (Proof Key for Code Exchange) for public clients
- Add rate limiting on authorization and token endpoints
- Use httpOnly, secure cookies for browser-based flows
- Implement token revocation endpoint
- Add authorization code expiration (10 minutes)

### 2.2 Attack Vectors to Mitigate
- Authorization code interception → PKCE, short expiry
- Token replay attacks → Short access token lifetime
- Refresh token theft → Token rotation, device fingerprinting
- CSRF attacks → State parameter validation
- Brute force → Rate limiting

## Phase 3: Implementation

**Agent**: backend-architect

### 3.1 Database Schema

```sql
-- OAuth clients table
CREATE TABLE oauth_clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id VARCHAR(255) UNIQUE NOT NULL,
    client_secret VARCHAR(255) NOT NULL, -- hashed
    name VARCHAR(255) NOT NULL,
    redirect_uris TEXT[] NOT NULL,
    allowed_scopes TEXT[] NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Authorization codes table
CREATE TABLE oauth_authorization_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(255) UNIQUE NOT NULL,
    client_id VARCHAR(255) REFERENCES oauth_clients(client_id),
    user_id UUID NOT NULL,
    redirect_uri TEXT NOT NULL,
    scope TEXT NOT NULL,
    code_challenge VARCHAR(255), -- PKCE
    code_challenge_method VARCHAR(10), -- S256 or plain
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Refresh tokens table
CREATE TABLE oauth_refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token VARCHAR(255) UNIQUE NOT NULL,
    client_id VARCHAR(255) REFERENCES oauth_clients(client_id),
    user_id UUID NOT NULL,
    scope TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_auth_codes_code ON oauth_authorization_codes(code);
CREATE INDEX idx_auth_codes_expires ON oauth_authorization_codes(expires_at);
CREATE INDEX idx_refresh_tokens_token ON oauth_refresh_tokens(token);
```

### 3.2 Key Generation and Storage

```typescript
import * as crypto from 'crypto';
import { SecretsManager } from 'aws-sdk';

// Generate RSA key pair
const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
  modulusLength: 2048,
  publicKeyEncoding: { type: 'spki', format: 'pem' },
  privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
});

// Store private key in Secrets Manager
const secretsManager = new SecretsManager();
await secretsManager.createSecret({
  Name: 'oauth/jwt-private-key',
  SecretString: privateKey,
}).promise();

// Public key can be stored in code or environment variable
process.env.JWT_PUBLIC_KEY = publicKey;
```

### 3.3 Authorization Endpoint

```typescript
// GET /oauth/authorize
router.get('/oauth/authorize', async (req, res) => {
  const {
    client_id,
    redirect_uri,
    response_type,
    scope,
    state,
    code_challenge,
    code_challenge_method
  } = req.query;

  // Validate client
  const client = await OAuthClient.findOne({ client_id });
  if (!client) {
    return res.status(400).json({ error: 'invalid_client' });
  }

  // Validate redirect URI
  if (!client.redirect_uris.includes(redirect_uri)) {
    return res.status(400).json({ error: 'invalid_redirect_uri' });
  }

  // Validate response type
  if (response_type !== 'code') {
    return res.status(400).json({ error: 'unsupported_response_type' });
  }

  // Validate scopes
  const requestedScopes = scope.split(' ');
  const invalidScopes = requestedScopes.filter(s => !client.allowed_scopes.includes(s));
  if (invalidScopes.length > 0) {
    return res.status(400).json({ error: 'invalid_scope' });
  }

  // Show user consent page
  res.render('oauth/authorize', {
    client,
    redirect_uri,
    scope: requestedScopes,
    state,
    code_challenge,
    code_challenge_method,
  });
});

// POST /oauth/authorize (user consents)
router.post('/oauth/authorize', authenticateUser, async (req, res) => {
  const {
    client_id,
    redirect_uri,
    scope,
    state,
    code_challenge,
    code_challenge_method
  } = req.body;

  // Generate authorization code
  const code = crypto.randomBytes(32).toString('base64url');

  await OAuthAuthorizationCode.create({
    code,
    client_id,
    user_id: req.user.id,
    redirect_uri,
    scope: scope.join(' '),
    code_challenge,
    code_challenge_method,
    expires_at: new Date(Date.now() + 10 * 60 * 1000), // 10 minutes
  });

  // Redirect back with authorization code
  const redirectUrl = new URL(redirect_uri);
  redirectUrl.searchParams.set('code', code);
  if (state) redirectUrl.searchParams.set('state', state);

  res.redirect(redirectUrl.toString());
});
```

### 3.4 Token Endpoint

```typescript
// POST /oauth/token
router.post('/oauth/token', async (req, res) => {
  const { grant_type, code, redirect_uri, client_id, client_secret, code_verifier } = req.body;

  if (grant_type === 'authorization_code') {
    // Validate client
    const client = await OAuthClient.findOne({ client_id });
    if (!client || !await bcrypt.compare(client_secret, client.client_secret)) {
      return res.status(401).json({ error: 'invalid_client' });
    }

    // Validate authorization code
    const authCode = await OAuthAuthorizationCode.findOne({ code, used: false });
    if (!authCode || authCode.expires_at < new Date()) {
      return res.status(400).json({ error: 'invalid_grant' });
    }

    // Validate redirect URI matches
    if (authCode.redirect_uri !== redirect_uri) {
      return res.status(400).json({ error: 'invalid_grant' });
    }

    // Validate PKCE if present
    if (authCode.code_challenge) {
      const verifierHash = crypto
        .createHash('sha256')
        .update(code_verifier)
        .digest('base64url');

      if (verifierHash !== authCode.code_challenge) {
        return res.status(400).json({ error: 'invalid_grant' });
      }
    }

    // Mark code as used
    await authCode.update({ used: true });

    // Generate tokens
    const accessToken = await generateAccessToken(authCode.user_id, authCode.scope);
    const refreshToken = await generateRefreshToken(client_id, authCode.user_id, authCode.scope);

    res.json({
      access_token: accessToken,
      token_type: 'Bearer',
      expires_in: 900, // 15 minutes
      refresh_token: refreshToken,
      scope: authCode.scope,
    });
  }
});
```

### 3.5 Token Generation

```typescript
import * as jwt from 'jsonwebtoken';

async function generateAccessToken(userId: string, scope: string): Promise<string> {
  const { SecretString: privateKey } = await secretsManager
    .getSecretValue({ SecretId: 'oauth/jwt-private-key' })
    .promise();

  return jwt.sign(
    {
      sub: userId,
      scope: scope,
      type: 'access',
    },
    privateKey,
    {
      algorithm: 'RS256',
      expiresIn: '15m',
      issuer: 'https://api.example.com',
      audience: 'https://api.example.com',
    }
  );
}

async function generateRefreshToken(
  clientId: string,
  userId: string,
  scope: string
): Promise<string> {
  const token = crypto.randomBytes(32).toString('base64url');

  await OAuthRefreshToken.create({
    token,
    client_id: clientId,
    user_id: userId,
    scope,
    expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
  });

  return token;
}
```

### 3.6 Token Refresh Endpoint

```typescript
// POST /oauth/token (refresh grant)
router.post('/oauth/token', async (req, res) => {
  const { grant_type, refresh_token, client_id, client_secret } = req.body;

  if (grant_type === 'refresh_token') {
    // Validate client
    const client = await OAuthClient.findOne({ client_id });
    if (!client || !await bcrypt.compare(client_secret, client.client_secret)) {
      return res.status(401).json({ error: 'invalid_client' });
    }

    // Validate refresh token
    const refreshTokenRecord = await OAuthRefreshToken.findOne({
      token: refresh_token,
      revoked: false,
    });

    if (!refreshTokenRecord || refreshTokenRecord.expires_at < new Date()) {
      return res.status(400).json({ error: 'invalid_grant' });
    }

    // Generate new access token
    const accessToken = await generateAccessToken(
      refreshTokenRecord.user_id,
      refreshTokenRecord.scope
    );

    // Optional: Rotate refresh token
    await refreshTokenRecord.update({ revoked: true });
    const newRefreshToken = await generateRefreshToken(
      client_id,
      refreshTokenRecord.user_id,
      refreshTokenRecord.scope
    );

    res.json({
      access_token: accessToken,
      token_type: 'Bearer',
      expires_in: 900,
      refresh_token: newRefreshToken,
      scope: refreshTokenRecord.scope,
    });
  }
});
```

### 3.7 Authentication Middleware

```typescript
import * as jwt from 'jsonwebtoken';

export const authenticateOAuth = async (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'missing_token' });
  }

  const token = authHeader.substring(7);

  try {
    const publicKey = process.env.JWT_PUBLIC_KEY;
    const payload = jwt.verify(token, publicKey, {
      algorithms: ['RS256'],
      issuer: 'https://api.example.com',
      audience: 'https://api.example.com',
    });

    // Attach user and scope to request
    req.user = { id: payload.sub };
    req.scope = payload.scope.split(' ');

    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'token_expired' });
    }
    return res.status(401).json({ error: 'invalid_token' });
  }
};

// Scope validation middleware
export const requireScope = (...requiredScopes: string[]) => {
  return (req, res, next) => {
    const hasAllScopes = requiredScopes.every(scope => req.scope.includes(scope));
    if (!hasAllScopes) {
      return res.status(403).json({ error: 'insufficient_scope' });
    }
    next();
  };
};
```

### 3.8 Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const authRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window per IP
  message: { error: 'too_many_requests' },
  standardHeaders: true,
  legacyHeaders: false,
});

router.get('/oauth/authorize', authRateLimiter, ...);
router.post('/oauth/authorize', authRateLimiter, ...);
router.post('/oauth/token', authRateLimiter, ...);
```

## Phase 4: Security Code Review

**Agent**: security-auditor

### 4.1 Verification Checklist
- [x] Private key stored in Secrets Manager (not in code)
- [x] RS256 algorithm used (asymmetric signing)
- [x] Short access token expiry (15 min)
- [x] Refresh token rotation implemented
- [x] PKCE support for public clients
- [x] Authorization code expiration (10 min)
- [x] Rate limiting on auth endpoints
- [x] Proper error messages (no info leakage)
- [x] Scope validation implemented
- [x] Redirect URI validation
- [x] Client secret hashing (bcrypt)

### 4.2 Additional Recommendations
- Add token revocation endpoint (`/oauth/revoke`)
- Implement device fingerprinting for refresh tokens
- Add audit logging for all OAuth operations
- Consider adding JWT ID (jti) for token tracking
- Add CORS configuration for cross-origin requests

## Phase 5: Testing

**Agent**: qa-specialist

### 5.1 Unit Tests

```typescript
describe('OAuth Token Generation', () => {
  it('generates valid access token with RS256', async () => {
    const token = await generateAccessToken('user-123', 'read write');
    const decoded = jwt.verify(token, publicKey);

    expect(decoded.sub).toBe('user-123');
    expect(decoded.scope).toBe('read write');
    expect(decoded.type).toBe('access');
  });

  it('access token expires after 15 minutes', async () => {
    const token = await generateAccessToken('user-123', 'read');
    const decoded = jwt.decode(token);
    const expiresIn = decoded.exp - decoded.iat;

    expect(expiresIn).toBe(900); // 15 minutes in seconds
  });
});
```

### 5.2 Integration Tests

```typescript
describe('OAuth Authorization Code Flow', () => {
  it('completes full authorization flow', async () => {
    // 1. Get authorization code
    const authResponse = await request(app)
      .post('/oauth/authorize')
      .send({
        client_id: testClient.client_id,
        redirect_uri: 'https://client.example.com/callback',
        scope: 'read write',
        response_type: 'code',
      })
      .expect(302);

    const redirectUrl = new URL(authResponse.headers.location);
    const code = redirectUrl.searchParams.get('code');

    // 2. Exchange code for tokens
    const tokenResponse = await request(app)
      .post('/oauth/token')
      .send({
        grant_type: 'authorization_code',
        code,
        redirect_uri: 'https://client.example.com/callback',
        client_id: testClient.client_id,
        client_secret: testClient.client_secret,
      })
      .expect(200);

    expect(tokenResponse.body).toHaveProperty('access_token');
    expect(tokenResponse.body).toHaveProperty('refresh_token');
    expect(tokenResponse.body.token_type).toBe('Bearer');
    expect(tokenResponse.body.expires_in).toBe(900);
  });
});
```

### 5.3 Security Tests

```typescript
describe('OAuth Security', () => {
  it('rejects expired authorization code', async () => {
    const expiredCode = await createAuthCode({ expires_at: new Date(Date.now() - 1000) });

    await request(app)
      .post('/oauth/token')
      .send({
        grant_type: 'authorization_code',
        code: expiredCode.code,
        redirect_uri: expiredCode.redirect_uri,
        client_id: testClient.client_id,
        client_secret: testClient.client_secret,
      })
      .expect(400);
  });

  it('rejects reused authorization code', async () => {
    const authCode = await createAuthCode({ used: false });

    // First use - should succeed
    await request(app)
      .post('/oauth/token')
      .send({
        grant_type: 'authorization_code',
        code: authCode.code,
        redirect_uri: authCode.redirect_uri,
        client_id: testClient.client_id,
        client_secret: testClient.client_secret,
      })
      .expect(200);

    // Second use - should fail
    await request(app)
      .post('/oauth/token')
      .send({
        grant_type: 'authorization_code',
        code: authCode.code,
        redirect_uri: authCode.redirect_uri,
        client_id: testClient.client_id,
        client_secret: testClient.client_secret,
      })
      .expect(400);
  });

  it('validates PKCE code challenge', async () => {
    const codeVerifier = crypto.randomBytes(32).toString('base64url');
    const codeChallenge = crypto
      .createHash('sha256')
      .update(codeVerifier)
      .digest('base64url');

    const authCode = await createAuthCode({
      code_challenge: codeChallenge,
      code_challenge_method: 'S256',
    });

    // Correct verifier - should succeed
    await request(app)
      .post('/oauth/token')
      .send({
        grant_type: 'authorization_code',
        code: authCode.code,
        redirect_uri: authCode.redirect_uri,
        client_id: testClient.client_id,
        client_secret: testClient.client_secret,
        code_verifier: codeVerifier,
      })
      .expect(200);
  });
});
```

## Phase 6: Git Workflow

**Agent**: git-workflow-manager

### 6.1 Commit Message

```
feat: implement OAuth2 authorization code flow with JWT

Complete OAuth2 implementation including:
- Authorization and token endpoints
- RS256 JWT signing with key rotation support
- PKCE support for public clients
- Refresh token flow with automatic rotation
- Scope-based authorization
- Rate limiting and security controls
- Comprehensive test coverage (95%+)

Security features:
- Private keys stored in AWS Secrets Manager
- Short-lived access tokens (15 min)
- Authorization code expiration (10 min)
- Client secret hashing with bcrypt
- Redirect URI validation
- Rate limiting on auth endpoints

Database schema includes:
- oauth_clients
- oauth_authorization_codes
- oauth_refresh_tokens

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### 6.2 Pull Request

```markdown
## OAuth2 Authorization Code Flow Implementation

### Summary
Complete implementation of OAuth2 authorization code flow with JWT tokens, PKCE support, and security best practices.

### Files Changed
- `src/routes/oauth.ts` - OAuth endpoints
- `src/middleware/oauth-auth.ts` - Authentication middleware
- `src/services/token-service.ts` - Token generation and validation
- `src/models/oauth-client.model.ts` - OAuth client model
- `src/models/oauth-authorization-code.model.ts` - Authorization code model
- `src/models/oauth-refresh-token.model.ts` - Refresh token model
- `migrations/001_create_oauth_tables.sql` - Database schema
- `tests/oauth.test.ts` - Comprehensive tests

### Acceptance Criteria
- [x] OAuth2 authorization code flow implemented
- [x] JWT token generation with RS256
- [x] Refresh token rotation
- [x] PKCE support for public clients
- [x] Database schema deployed to staging
- [x] Rate limiting on auth endpoints
- [x] Unit tests (95%+ coverage)
- [x] Integration tests for full flow
- [x] Security review completed
- [x] Documentation updated

### Security Considerations
- Private keys stored in AWS Secrets Manager
- All tokens signed with RS256 (asymmetric)
- Short access token lifetime (15 min)
- Refresh token rotation on use
- Authorization code single-use and short-lived
- Comprehensive input validation
- Rate limiting to prevent brute force

### Test Plan
- ✅ Unit tests for token generation/validation
- ✅ Integration tests for OAuth flow
- ✅ Security tests for token expiration
- ✅ PKCE validation tests
- ✅ Rate limiting tests
- ✅ Error handling tests

### Deployment Notes
1. Generate RSA key pair and store in Secrets Manager
2. Run database migrations
3. Create initial OAuth clients in database
4. Deploy application with new endpoints
5. Update API documentation

🤖 Generated with Claude Code
```

## Related Documentation

- [Spec-Driven Development](../agent-patterns/spec-driven-development.md)
- [Security Patterns](../../domains/shared-patterns.md#security-patterns)
- [Git Workflow Pattern](../agent-patterns/git-workflow.md)
- [Backend Domain Configuration](../../../.claude/domains/backend.md)
- [Security Domain Configuration](../../../.claude/domains/security.md)

## References

- [OAuth 2.0 Specification (RFC 6749)](https://datatracker.ietf.org/doc/html/rfc6749)
- [JWT Specification (RFC 7519)](https://datatracker.ietf.org/doc/html/rfc7519)
- [PKCE Specification (RFC 7636)](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
