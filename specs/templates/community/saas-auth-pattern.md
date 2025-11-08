# Pattern: OAuth2 + JWT Authentication for SaaS Applications

```yaml
pattern_metadata:
  name: "saas-oauth2-jwt-auth"
  category: "authentication"
  difficulty: "intermediate"
  tech_stack: ["Node.js", "Express", "PostgreSQL", "JWT", "OAuth2"]
  tags: ["oauth2", "jwt", "saas", "authentication", "security", "multi-tenant"]
  version: "1.0.0"
  status: "stable"
  author: "claude-oak-agents"
  last_updated: "2025-11-08"
```

## Problem Statement

### What Challenge Does This Solve?

Modern SaaS applications need secure, scalable authentication that:
- Supports third-party OAuth2 providers (Google, GitHub, Microsoft)
- Maintains secure session management with JWT tokens
- Scales across multi-tenant architectures
- Provides refresh token rotation for security
- Handles authorization and role-based access control (RBAC)

### When Should You Use This Pattern?

Use this pattern when you need:
- ✅ User authentication via OAuth2 providers (social login)
- ✅ Stateless JWT-based session management
- ✅ Multi-tenant SaaS application architecture
- ✅ Secure token refresh without re-authentication
- ✅ Role-based access control (RBAC)

Don't use this pattern when:
- ❌ Simple username/password auth is sufficient (use simpler pattern)
- ❌ Enterprise SSO with SAML is required (use SAML pattern instead)
- ❌ Mobile app needs native OAuth flows (requires PKCE extension)

### Prerequisites

- Node.js backend (Express or similar)
- PostgreSQL or similar relational database
- HTTPS/TLS in production
- OAuth2 client credentials (Google, GitHub, etc.)
- Basic understanding of JWT and OAuth2 flows

## Solution Overview

### High-Level Approach

```
┌────────────┐           ┌─────────────────┐           ┌──────────────┐
│   Client   │  OAuth2   │  OAuth2         │   User    │  OAuth2      │
│  (Browser) │◄─────────►│  Authorization  │  Login    │  Provider    │
│            │           │  Server (Your   │◄─────────►│  (Google,    │
│            │           │   Backend)      │           │   GitHub)    │
└────────────┘           └─────────────────┘           └──────────────┘
      ▲                           │
      │                           │
      │     JWT Access Token      │
      │◄─────────────────────────┤
      │                           │
      │     API Requests          │
      │      (with JWT)           │
      │──────────────────────────►│
      │                           │
      │     Refresh Token         │
      │      (when expired)       │
      │──────────────────────────►│
      │                           ▼
      │                  ┌─────────────────┐
      │                  │   PostgreSQL    │
      │                  │   - users       │
      └─────────────────►│   - sessions    │
                         │   - tenants     │
                         └─────────────────┘
```

### Key Design Decisions

**1. OAuth2 Authorization Code Flow**
- Most secure flow for web applications
- Prevents token exposure in browser history
- Supports PKCE for additional security

**2. JWT for Access Tokens**
- Stateless authentication
- Contains user claims (id, email, roles)
- Short-lived (15 minutes) for security

**3. Refresh Tokens in Database**
- Long-lived (7 days) for convenience
- Stored in database for revocation capability
- Rotation on each use (prevents replay attacks)

**4. httpOnly Cookies for Token Storage**
- Prevents XSS attacks
- Automatic inclusion in requests
- Secure flag in production

### Why This Approach Over Alternatives?

| Alternative | Why OAuth2 + JWT Instead? |
|------------|---------------------------|
| Session-based auth | OAuth2+JWT is stateless, scales better |
| OAuth2 with opaque tokens | JWT doesn't require database lookup per request |
| JWT in localStorage | httpOnly cookies prevent XSS token theft |
| Long-lived JWT | Short JWT + refresh token reduces exposure |

## Technical Design

### Architecture Components

#### 1. OAuth2 Authorization Endpoints

**`GET /auth/:provider/authorize`**
- Redirects to OAuth2 provider (Google, GitHub, etc.)
- Generates state parameter (CSRF protection)
- Optionally includes PKCE code_challenge

**`GET /auth/:provider/callback`**
- Receives authorization code from provider
- Exchanges code for provider access token
- Fetches user profile from provider
- Creates or updates user in database
- Issues JWT access token + refresh token
- Sets httpOnly cookies and redirects

#### 2. Token Management Endpoints

**`POST /auth/refresh`**
- Accepts refresh token from cookie
- Validates refresh token from database
- Rotates refresh token (invalidates old, issues new)
- Issues new JWT access token
- Returns tokens via httpOnly cookies

**`POST /auth/logout`**
- Revokes refresh token in database
- Clears httpOnly cookies
- Optional: Revoke OAuth2 provider token

#### 3. Protected API Endpoints

**`GET /api/*` (Any protected route)**
- Extracts JWT from httpOnly cookie
- Validates JWT signature and expiration
- Extracts user claims (id, roles, tenant)
- Authorizes based on RBAC rules
- Proceeds with request or returns 401/403

### Database Schema

```sql
-- Tenants table (multi-tenant SaaS)
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  email VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  avatar_url VARCHAR(500),
  provider VARCHAR(50) NOT NULL,  -- 'google', 'github', etc.
  provider_user_id VARCHAR(255) NOT NULL,
  roles TEXT[] DEFAULT ARRAY['user'],  -- ['user', 'admin', 'owner']
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login TIMESTAMP,
  UNIQUE(provider, provider_user_id),
  UNIQUE(tenant_id, email)
);

-- Refresh tokens table
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash VARCHAR(255) NOT NULL UNIQUE,  -- SHA-256 hash
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  revoked BOOLEAN DEFAULT FALSE,
  revoked_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_users_provider ON users(provider, provider_user_id);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_hash ON refresh_tokens(token_hash);
CREATE INDEX idx_refresh_tokens_expires ON refresh_tokens(expires_at) WHERE NOT revoked;
```

### Security Considerations

#### OWASP Top 10 Protections

**1. Broken Access Control**
- JWT contains tenant_id claim for multi-tenant isolation
- RBAC enforced on every protected route
- Refresh token tied to specific user

**2. Cryptographic Failures**
- JWT signed with RS256 (asymmetric keys)
- Refresh tokens hashed with SHA-256 before storage
- HTTPS/TLS required in production

**3. Injection**
- Parameterized SQL queries (prevent SQL injection)
- Input validation on all OAuth2 parameters

**4. Insecure Design**
- State parameter prevents CSRF attacks
- PKCE prevents authorization code interception
- Refresh token rotation prevents replay attacks

**5. Security Misconfiguration**
- httpOnly cookies prevent XSS
- SameSite=Strict prevents CSRF
- Secure flag on cookies in production

**6. Vulnerable Components**
- Use maintained OAuth2 libraries (passport.js)
- Regular dependency updates
- Security scanning in CI/CD

**7. Authentication Failures**
- Short-lived JWT (15 minutes)
- Refresh token rotation on every use
- Revocation capability via database

**8. Data Integrity Failures**
- JWT signature validation
- State parameter validation
- Token expiration enforcement

**9. Logging & Monitoring**
- Log all authentication events
- Alert on suspicious patterns (rapid token refresh)
- Track failed authentication attempts

**10. Server-Side Request Forgery (SSRF)**
- Validate OAuth2 callback URLs
- Whitelist allowed redirect URIs

#### Additional Security Measures

**Token Security**:
- JWT access tokens: 15 minutes expiration
- Refresh tokens: 7 days expiration, rotate on use
- Store refresh tokens hashed (SHA-256)

**Cookie Security**:
```javascript
res.cookie('access_token', jwt, {
  httpOnly: true,      // Prevents XSS access
  secure: true,        // HTTPS only
  sameSite: 'strict',  // Prevents CSRF
  maxAge: 15 * 60 * 1000  // 15 minutes
});
```

**Rate Limiting**:
- Limit OAuth2 authorization attempts: 5 per hour per IP
- Limit token refresh attempts: 10 per hour per user
- Block IPs with excessive failed attempts

### Data Flow

#### Initial OAuth2 Login

```
1. User clicks "Login with Google"
2. Frontend → GET /auth/google/authorize
3. Backend generates state, redirects to Google
4. Google → User authenticates
5. Google redirects → GET /auth/google/callback?code=...&state=...
6. Backend:
   a. Validates state (CSRF protection)
   b. Exchanges code for Google access token
   c. Fetches user profile from Google API
   d. Creates/updates user in database
   e. Generates JWT access token (15 min)
   f. Generates refresh token (7 days), stores hash in DB
   g. Sets httpOnly cookies
   h. Redirects to frontend dashboard
7. Frontend receives cookies, user is authenticated
```

#### Token Refresh Flow

```
1. Frontend detects JWT expiration (or receives 401)
2. Frontend → POST /auth/refresh (refresh token in cookie)
3. Backend:
   a. Extracts refresh token from cookie
   b. Hashes token, looks up in database
   c. Validates expiration and revocation status
   d. Invalidates old refresh token
   e. Generates new JWT access token (15 min)
   f. Generates new refresh token (7 days), stores hash
   g. Sets new httpOnly cookies
   h. Returns 200 OK
4. Frontend retries original request with new JWT
```

#### Protected API Request

```
1. Frontend → GET /api/projects (JWT in cookie)
2. Backend middleware:
   a. Extracts JWT from httpOnly cookie
   b. Verifies signature with public key
   c. Validates expiration
   d. Extracts claims (user_id, tenant_id, roles)
   e. Checks RBAC (user has permission?)
   f. Attaches user context to request
3. Backend controller executes request
4. Returns response
```

## Agent Workflow

### Agents Involved

1. **design-simplicity-advisor** - Pre-implementation analysis
2. **backend-architect** - Database schema and API design
3. **security-auditor** - Security review and threat modeling
4. **frontend-developer** - Login UI and token handling
5. **unit-test-expert** - Comprehensive test suite
6. **qa-specialist** - Integration and E2E testing
7. **quality-gate** - Unified validation
8. **git-workflow-manager** - Commit and PR creation

### Execution Sequence

```
design-simplicity-advisor (KISS analysis)
  ↓
backend-architect (database + API implementation)
  ↓
security-auditor (security review in parallel)
  ↓
frontend-developer (login UI + token handling)
  ↓
unit-test-expert + qa-specialist (testing in parallel)
  ↓
quality-gate (unified validation)
  ↓
git-workflow-manager (commit and PR)
```

### Agent Task Breakdown

#### Task 1: Simplicity Analysis (design-simplicity-advisor)
**Input**: "Implement OAuth2 + JWT authentication for SaaS app"
**Output**:
- Validates OAuth2 is appropriate (vs simpler session auth)
- Recommends using battle-tested library (passport.js)
- Flags unnecessary complexity (PKCE optional for server-side)
- Approves design or suggests simpler alternatives

#### Task 2: Database Schema (backend-architect)
**Input**: "Design multi-tenant user authentication schema"
**Output**:
```sql
-- Schema from "Database Schema" section above
-- Includes tenants, users, refresh_tokens tables
-- Optimized indexes
-- Foreign key constraints
```

#### Task 3: OAuth2 Endpoints (backend-architect)
**Input**: "Implement OAuth2 authorization code flow endpoints"
**Output**:
- `GET /auth/:provider/authorize` implementation
- `GET /auth/:provider/callback` implementation
- `POST /auth/refresh` implementation
- `POST /auth/logout` implementation
- Passport.js strategy configuration

#### Task 4: JWT Generation & Validation (backend-architect)
**Input**: "Implement JWT signing and verification"
**Output**:
```javascript
// JWT signing
const generateAccessToken = (user) => {
  return jwt.sign(
    {
      user_id: user.id,
      tenant_id: user.tenant_id,
      email: user.email,
      roles: user.roles
    },
    privateKey,
    {
      algorithm: 'RS256',
      expiresIn: '15m',
      issuer: 'your-app.com',
      audience: 'your-app-api'
    }
  );
};

// JWT verification middleware
const verifyAccessToken = (req, res, next) => {
  const token = req.cookies.access_token;
  if (!token) return res.status(401).json({ error: 'No token' });

  try {
    const decoded = jwt.verify(token, publicKey, {
      algorithms: ['RS256'],
      issuer: 'your-app.com',
      audience: 'your-app-api'
    });
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};
```

#### Task 5: Security Review (security-auditor)
**Input**: "Review OAuth2 + JWT implementation for vulnerabilities"
**Output**:
- OWASP Top 10 checklist validation
- State parameter CSRF protection verified
- httpOnly cookie configuration validated
- Refresh token rotation confirmed
- Rate limiting requirements documented
- Security test cases defined

#### Task 6: Frontend Login UI (frontend-developer)
**Input**: "Create OAuth2 social login buttons"
**Output**:
```typescript
// React login component
const LoginPage = () => {
  const handleGoogleLogin = () => {
    window.location.href = '/auth/google/authorize';
  };

  const handleGitHubLogin = () => {
    window.location.href = '/auth/github/authorize';
  };

  return (
    <div className="login-page">
      <h1>Sign In</h1>
      <button onClick={handleGoogleLogin}>
        Continue with Google
      </button>
      <button onClick={handleGitHubLogin}>
        Continue with GitHub
      </button>
    </div>
  );
};
```

#### Task 7: Token Refresh Logic (frontend-developer)
**Input**: "Implement automatic token refresh on expiration"
**Output**:
```typescript
// Axios interceptor for automatic token refresh
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        // Attempt token refresh
        await axios.post('/auth/refresh');
        // Retry original request
        return axios(error.config);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);
```

#### Task 8: Unit Tests (unit-test-expert)
**Input**: "Create unit tests for OAuth2 + JWT implementation"
**Output**:
- Test JWT generation and validation
- Test refresh token creation and rotation
- Test state parameter generation and validation
- Test cookie configuration
- Mock OAuth2 provider responses

#### Task 9: Integration Tests (qa-specialist)
**Input**: "Create E2E tests for OAuth2 login flow"
**Output**:
- Test complete OAuth2 authorization code flow
- Test token refresh flow
- Test logout and token revocation
- Test multi-tenant isolation
- Test RBAC enforcement

## Implementation Checklist

### Phase 1: Database Setup
- [ ] Create PostgreSQL database
- [ ] Run DDL for tenants table
- [ ] Run DDL for users table
- [ ] Run DDL for refresh_tokens table
- [ ] Create indexes for performance
- [ ] Verify foreign key constraints

### Phase 2: Backend Configuration
- [ ] Install dependencies (passport, jsonwebtoken, cookie-parser)
- [ ] Generate RS256 key pair (private/public keys)
- [ ] Configure OAuth2 provider credentials (Google, GitHub)
- [ ] Set up environment variables (DB URL, JWT keys, OAuth2 secrets)
- [ ] Configure CORS and cookie settings

### Phase 3: OAuth2 Implementation
- [ ] Implement `GET /auth/:provider/authorize` endpoint
- [ ] Implement `GET /auth/:provider/callback` endpoint
- [ ] Implement `POST /auth/refresh` endpoint
- [ ] Implement `POST /auth/logout` endpoint
- [ ] Configure Passport.js strategies (Google, GitHub)

### Phase 4: JWT Implementation
- [ ] Implement JWT signing function
- [ ] Implement JWT verification middleware
- [ ] Implement refresh token generation
- [ ] Implement refresh token rotation logic
- [ ] Configure httpOnly cookie settings

### Phase 5: Security Hardening
- [ ] Enable HTTPS/TLS in production
- [ ] Configure rate limiting
- [ ] Implement CSRF protection (state parameter)
- [ ] Add input validation
- [ ] Configure security headers (helmet.js)

### Phase 6: Frontend Integration
- [ ] Create login page with OAuth2 buttons
- [ ] Implement automatic token refresh interceptor
- [ ] Handle logout (clear cookies, redirect)
- [ ] Add loading states during authentication
- [ ] Handle authentication errors gracefully

### Phase 7: Testing
- [ ] Unit tests for JWT generation/validation
- [ ] Unit tests for refresh token rotation
- [ ] Integration tests for OAuth2 flow
- [ ] E2E tests for complete login/logout
- [ ] Security tests (CSRF, XSS, token theft)

### Phase 8: Deployment
- [ ] Configure production OAuth2 redirect URIs
- [ ] Set up production database
- [ ] Deploy backend with environment variables
- [ ] Deploy frontend
- [ ] Verify HTTPS and cookie security flags
- [ ] Monitor authentication events

## Validation Criteria

### Success Metrics

**Functional Requirements**:
- [ ] Users can log in via Google OAuth2
- [ ] Users can log in via GitHub OAuth2
- [ ] JWT access tokens expire after 15 minutes
- [ ] Token refresh works seamlessly
- [ ] Users can log out and tokens are revoked
- [ ] Multi-tenant isolation enforced
- [ ] RBAC permissions enforced

**Security Requirements**:
- [ ] JWT signature validation prevents tampering
- [ ] httpOnly cookies prevent XSS token theft
- [ ] State parameter prevents CSRF attacks
- [ ] Refresh token rotation prevents replay attacks
- [ ] Rate limiting prevents brute force attacks
- [ ] HTTPS enforced in production

**Performance Requirements**:
- [ ] JWT validation <10ms per request
- [ ] Token refresh <100ms
- [ ] OAuth2 callback <500ms
- [ ] Database queries optimized with indexes

### Common Failure Modes

**1. OAuth2 Callback Fails**
- **Symptom**: Redirect to callback URL but error message
- **Causes**: Invalid client_id/client_secret, wrong redirect_uri, state mismatch
- **Fix**: Verify OAuth2 provider configuration, check callback URL whitelist

**2. JWT Validation Fails**
- **Symptom**: 401 Unauthorized on protected routes
- **Causes**: Expired token, wrong signing key, algorithm mismatch
- **Fix**: Verify token expiration, check RS256 key pair, inspect JWT claims

**3. Token Refresh Fails**
- **Symptom**: User logged out after 15 minutes
- **Causes**: Refresh token expired, token not found in DB, rotation failed
- **Fix**: Check refresh token expiration (7 days), verify database storage

**4. Multi-Tenant Isolation Broken**
- **Symptom**: Users see data from other tenants
- **Causes**: Missing tenant_id check, incorrect RBAC logic
- **Fix**: Add tenant_id to all queries, validate tenant_id in JWT matches request

**5. CSRF Attack Possible**
- **Symptom**: Malicious site can initiate OAuth2 flow
- **Causes**: Missing state parameter validation
- **Fix**: Generate and validate state parameter on callback

## Examples and Usage

### Example 1: Google OAuth2 Login (Node.js + Express)

```javascript
// server.js
const express = require('express');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

const app = express();

// Configure Google OAuth2 Strategy
passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: '/auth/google/callback',
    passReqToCallback: true
  },
  async (req, accessToken, refreshToken, profile, done) => {
    // Find or create user in database
    const user = await findOrCreateUser({
      provider: 'google',
      provider_user_id: profile.id,
      email: profile.emails[0].value,
      name: profile.displayName,
      avatar_url: profile.photos[0].value
    });
    return done(null, user);
  }
));

// OAuth2 Authorization Endpoint
app.get('/auth/google/authorize', (req, res, next) => {
  // Generate state for CSRF protection
  const state = crypto.randomBytes(32).toString('hex');
  req.session.oauth_state = state;

  passport.authenticate('google', {
    scope: ['profile', 'email'],
    state: state
  })(req, res, next);
});

// OAuth2 Callback Endpoint
app.get('/auth/google/callback',
  (req, res, next) => {
    // Validate state parameter
    if (req.query.state !== req.session.oauth_state) {
      return res.status(403).json({ error: 'Invalid state parameter' });
    }
    next();
  },
  passport.authenticate('google', { session: false }),
  async (req, res) => {
    // Generate JWT access token
    const accessToken = jwt.sign({
      user_id: req.user.id,
      tenant_id: req.user.tenant_id,
      email: req.user.email,
      roles: req.user.roles
    }, privateKey, {
      algorithm: 'RS256',
      expiresIn: '15m'
    });

    // Generate refresh token
    const refreshToken = crypto.randomBytes(64).toString('hex');
    const refreshTokenHash = crypto.createHash('sha256')
      .update(refreshToken).digest('hex');

    // Store refresh token in database
    await db.query(`
      INSERT INTO refresh_tokens (user_id, token_hash, expires_at)
      VALUES ($1, $2, NOW() + INTERVAL '7 days')
    `, [req.user.id, refreshTokenHash]);

    // Set httpOnly cookies
    res.cookie('access_token', accessToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 15 * 60 * 1000  // 15 minutes
    });

    res.cookie('refresh_token', refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60 * 1000  // 7 days
    });

    // Redirect to frontend dashboard
    res.redirect('/dashboard');
  }
);

// Token Refresh Endpoint
app.post('/auth/refresh', async (req, res) => {
  const refreshToken = req.cookies.refresh_token;
  if (!refreshToken) {
    return res.status(401).json({ error: 'No refresh token' });
  }

  // Hash and look up in database
  const tokenHash = crypto.createHash('sha256')
    .update(refreshToken).digest('hex');

  const result = await db.query(`
    SELECT rt.*, u.* FROM refresh_tokens rt
    JOIN users u ON rt.user_id = u.id
    WHERE rt.token_hash = $1
      AND rt.expires_at > NOW()
      AND rt.revoked = FALSE
  `, [tokenHash]);

  if (result.rows.length === 0) {
    return res.status(401).json({ error: 'Invalid refresh token' });
  }

  const user = result.rows[0];

  // Revoke old refresh token
  await db.query(`
    UPDATE refresh_tokens SET revoked = TRUE, revoked_at = NOW()
    WHERE token_hash = $1
  `, [tokenHash]);

  // Generate new tokens
  const newAccessToken = jwt.sign({
    user_id: user.id,
    tenant_id: user.tenant_id,
    email: user.email,
    roles: user.roles
  }, privateKey, {
    algorithm: 'RS256',
    expiresIn: '15m'
  });

  const newRefreshToken = crypto.randomBytes(64).toString('hex');
  const newRefreshTokenHash = crypto.createHash('sha256')
    .update(newRefreshToken).digest('hex');

  // Store new refresh token
  await db.query(`
    INSERT INTO refresh_tokens (user_id, token_hash, expires_at)
    VALUES ($1, $2, NOW() + INTERVAL '7 days')
  `, [user.id, newRefreshTokenHash]);

  // Set new cookies
  res.cookie('access_token', newAccessToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 15 * 60 * 1000
  });

  res.cookie('refresh_token', newRefreshToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 7 * 24 * 60 * 60 * 1000
  });

  res.json({ success: true });
});

// Protected Route Example
app.get('/api/projects', verifyAccessToken, async (req, res) => {
  // req.user contains JWT claims (user_id, tenant_id, roles)
  const projects = await db.query(`
    SELECT * FROM projects WHERE tenant_id = $1
  `, [req.user.tenant_id]);

  res.json(projects.rows);
});
```

### Example 2: Frontend Token Refresh (React + Axios)

```typescript
// src/api/axios.ts
import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  withCredentials: true  // Include cookies in requests
});

// Automatic token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not already retrying
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Attempt token refresh
        await axios.post('/auth/refresh', {}, { withCredentials: true });
        
        // Retry original request with new token (in cookie)
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

### Example 3: RBAC Middleware

```javascript
// middleware/rbac.js
const checkRole = (requiredRoles) => {
  return (req, res, next) => {
    // req.user populated by verifyAccessToken middleware
    const userRoles = req.user.roles || [];

    const hasRole = requiredRoles.some(role => userRoles.includes(role));

    if (!hasRole) {
      return res.status(403).json({
        error: 'Insufficient permissions',
        required: requiredRoles,
        current: userRoles
      });
    }

    next();
  };
};

// Usage
app.delete('/api/users/:id',
  verifyAccessToken,
  checkRole(['admin', 'owner']),
  async (req, res) => {
    // Only admins and owners can delete users
    await db.query('DELETE FROM users WHERE id = $1', [req.params.id]);
    res.json({ success: true });
  }
);
```

## Troubleshooting

### Issue 1: OAuth2 Redirect Loop
**Symptoms**: Infinite redirect between app and OAuth2 provider

**Causes**:
- Callback URL not whitelisted in provider settings
- State parameter mismatch
- Session not persisting across requests

**Solutions**:
- Verify redirect_uri matches exactly (https://yourapp.com/auth/google/callback)
- Check provider console for whitelisted URLs
- Ensure session middleware configured before OAuth2 routes

### Issue 2: JWT Signature Verification Fails
**Symptoms**: 401 Unauthorized despite valid-looking JWT

**Causes**:
- Private/public key mismatch
- Algorithm mismatch (RS256 vs HS256)
- Token issued before server restart (if keys regenerated)

**Solutions**:
- Verify RS256 key pair generation (openssl genrsa -out private.pem 2048)
- Check JWT algorithm in sign and verify calls
- Store keys persistently (not regenerated on restart)

### Issue 3: Refresh Token Rotation Breaking
**Symptoms**: Users logged out unexpectedly, refresh fails

**Causes**:
- Old refresh token not revoked before issuing new one
- Database transaction not committed
- Token hash mismatch

**Solutions**:
- Use database transaction for revoke + insert
- Verify SHA-256 hash algorithm matches on store and lookup
- Add logging to track token rotation events

## References

- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [JWT RFC 7519](https://tools.ietf.org/html/rfc7519)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Passport.js Documentation](http://www.passportjs.org/)
- [Google OAuth2 Setup](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth2 Setup](https://docs.github.com/en/developers/apps/building-oauth-apps)

---

**Pattern Version**: 1.0.0  
**Last Updated**: 2025-11-08  
**Maintained By**: claude-oak-agents community
