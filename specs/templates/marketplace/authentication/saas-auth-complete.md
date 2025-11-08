---
template_id: saas-auth-complete
template_name: SaaS Authentication Complete
category: authentication
difficulty: advanced
estimated_time: 8-12 hours
tags: [oauth2, jwt, authentication, security, saas]
author: claude-oak-agents
version: 1.0.0
last_updated: 2025-11-08
popularity: 95
dependencies: [express, jsonwebtoken, bcrypt]
related_templates: [rest-crud-api, cdk-serverless-api]
---

# SaaS Authentication Complete

Complete OAuth2 + JWT authentication system for SaaS applications with social login, MFA, and session management.

## Overview

This template implements a production-ready authentication system supporting:
- OAuth2 authorization code flow
- JWT token management (access + refresh tokens)
- Social login (Google, GitHub, Microsoft)
- Multi-factor authentication (TOTP)
- Session management and revocation
- Password reset and email verification

## Use Cases

- **Multi-tenant SaaS**: Isolated authentication per tenant
- **B2B Applications**: Enterprise SSO integration
- **Consumer Apps**: Social login for quick onboarding
- **Mobile Apps**: Secure token-based authentication

## Requirements

### Technical Prerequisites
- Node.js 18+ or Go 1.21+
- PostgreSQL or MongoDB (user storage)
- Redis (session storage, token blacklist)
- Email service (SendGrid, AWS SES)
- SSL/TLS certificate (production)

### Security Requirements
- HTTPS mandatory in production
- Secure cookie configuration (httpOnly, sameSite, secure)
- Rate limiting on auth endpoints
- Password strength validation (12+ chars, complexity)
- JWT secret rotation capability

## Implementation Plan

### Phase 1: Core Authentication (4 hours)

**1.1 User Model and Database Schema**
```typescript
interface User {
  id: string;
  email: string;
  passwordHash: string;
  emailVerified: boolean;
  mfaEnabled: boolean;
  mfaSecret?: string;
  createdAt: Date;
  updatedAt: Date;
}

interface RefreshToken {
  token: string;
  userId: string;
  expiresAt: Date;
  createdAt: Date;
}
```

**1.2 Password Authentication**
- User registration with email verification
- Password hashing with bcrypt (cost factor 12)
- Login with email/password
- Forgot password flow (reset token via email)

**1.3 JWT Token Generation**
- Access token (15 min expiry)
- Refresh token (7 day expiry, stored in database)
- Token payload: `{ userId, email, roles, tenant }`

### Phase 2: OAuth2 Implementation (3 hours)

**2.1 OAuth2 Authorization Server**
- Authorization endpoint: `/oauth/authorize`
- Token endpoint: `/oauth/token`
- Grant types: authorization_code, refresh_token
- PKCE support for public clients

**2.2 Social Login Integration**
- Google OAuth2 integration
- GitHub OAuth2 integration
- Microsoft OAuth2 integration
- Account linking (merge social + password accounts)

### Phase 3: Multi-Factor Authentication (2 hours)

**3.1 TOTP Setup**
- Generate TOTP secret (speakeasy or otplib)
- QR code generation for authenticator apps
- Backup codes (10 single-use codes)

**3.2 MFA Verification**
- Verify TOTP code during login
- Remember device option (30 day cookie)
- Disable MFA with password confirmation

### Phase 4: Session Management (2 hours)

**4.1 Session Storage**
- Redis-backed session store
- Session data: userId, device, IP, lastActivity
- Concurrent session limit (5 sessions per user)

**4.2 Session Operations**
- List active sessions
- Revoke session by ID
- Revoke all sessions (force logout)
- Auto-logout on password change

### Phase 5: Security Hardening (1 hour)

**5.1 Rate Limiting**
- Login attempts: 5 per 15 min per IP
- Password reset: 3 per hour per email
- Token refresh: 10 per hour per user

**5.2 Token Blacklist**
- Redis-backed blacklist for revoked tokens
- Add tokens on logout/password change
- TTL matches token expiry

**5.3 Security Headers**
- Helmet.js integration
- CORS configuration
- Content Security Policy

## Agent Workflow

```yaml
agent_sequence:
  phase_1_design:
    - agent: design-simplicity-advisor
      task: "Review OAuth2 minimal implementation vs full spec"
      output: "Recommendation: Implement authorization_code + refresh_token only"

    - agent: backend-architect
      task: "Design database schema for users, refresh tokens, sessions"
      output: "Schema DDL, indexes, constraints"

  phase_2_implementation:
    - agent: backend-architect
      task: "Implement core authentication (registration, login, JWT)"
      duration: "4 hours"

    - agent: backend-architect
      task: "Implement OAuth2 endpoints and social login"
      duration: "3 hours"

  phase_3_security:
    - agent: security-auditor
      task: "Security review: token handling, password storage, session management"
      output: "Security findings and remediation plan"

    - agent: backend-architect
      task: "Implement MFA and session management"
      duration: "4 hours"

  phase_4_quality:
    - agent: unit-test-expert
      task: "Comprehensive test suite (auth flows, edge cases, security)"
      coverage: ">80%"

    - agent: quality-gate
      task: "Code review and KISS validation"

  phase_5_deployment:
    - agent: infrastructure-specialist
      task: "HTTPS setup, environment variables, secrets management"

    - agent: git-workflow-manager
      task: "Create PR with complete auth implementation"
```

## Testing Strategy

### Unit Tests
- User registration validation
- Password hashing/verification
- JWT generation/verification
- Token refresh logic
- MFA TOTP validation

### Integration Tests
- Full registration flow (email verification)
- Login flow (password + MFA)
- OAuth2 authorization code flow
- Session management (create, list, revoke)
- Password reset flow

### Security Tests
- SQL injection attempts
- Rate limiting enforcement
- Token expiry and refresh
- Session fixation prevention
- CSRF protection

### Load Tests
- Login throughput (100 req/sec)
- Token refresh performance
- Session lookup latency
- Concurrent session handling

## Configuration

### Environment Variables
```bash
# JWT Configuration
JWT_ACCESS_SECRET=<random-256-bit-secret>
JWT_REFRESH_SECRET=<random-256-bit-secret>
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# OAuth2 Providers
GOOGLE_CLIENT_ID=<google-client-id>
GOOGLE_CLIENT_SECRET=<google-client-secret>
GITHUB_CLIENT_ID=<github-client-id>
GITHUB_CLIENT_SECRET=<github-client-secret>

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/auth_db
REDIS_URL=redis://localhost:6379

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_USER=apikey
SMTP_PASS=<sendgrid-api-key>
FROM_EMAIL=noreply@yourapp.com

# Security
BCRYPT_COST_FACTOR=12
SESSION_LIMIT=5
RATE_LIMIT_WINDOW=15m
RATE_LIMIT_MAX=5
```

## API Endpoints

### Authentication
```
POST   /auth/register              - Register new user
POST   /auth/login                 - Login with email/password
POST   /auth/logout                - Logout (revoke tokens)
POST   /auth/refresh               - Refresh access token
POST   /auth/forgot-password       - Request password reset
POST   /auth/reset-password        - Reset password with token
GET    /auth/verify-email/:token   - Verify email address
```

### OAuth2
```
GET    /oauth/authorize            - OAuth2 authorization endpoint
POST   /oauth/token                - OAuth2 token endpoint
GET    /oauth/google               - Google OAuth2 redirect
GET    /oauth/github               - GitHub OAuth2 redirect
```

### MFA
```
POST   /mfa/setup                  - Generate TOTP secret
POST   /mfa/enable                 - Enable MFA with TOTP verification
POST   /mfa/disable                - Disable MFA
POST   /mfa/verify                 - Verify TOTP code
```

### Sessions
```
GET    /sessions                   - List active sessions
DELETE /sessions/:id               - Revoke specific session
DELETE /sessions                   - Revoke all sessions
```

## Common Pitfalls

### 1. JWT Secret Security
**Problem**: Using weak or hardcoded JWT secrets
**Solution**: Generate strong secrets (256-bit random), store in environment variables, rotate periodically

### 2. Token Expiry
**Problem**: Access tokens that never expire
**Solution**: Short-lived access tokens (15 min), refresh tokens for long-term access

### 3. Password Reset Security
**Problem**: Predictable reset tokens
**Solution**: Cryptographically secure random tokens, single-use, expire after 1 hour

### 4. Session Fixation
**Problem**: Reusing session IDs after login
**Solution**: Regenerate session ID on authentication state change

### 5. Rate Limiting Bypass
**Problem**: Rate limiting per IP can be bypassed with proxies
**Solution**: Combine IP + user email for login attempts, use CAPTCHA after threshold

### 6. CORS Misconfiguration
**Problem**: Allowing all origins in production
**Solution**: Whitelist specific origins, credentials mode requires specific origin

## Monitoring and Observability

### Key Metrics
- Login success rate
- Token refresh rate
- MFA adoption rate
- Failed login attempts (potential attacks)
- Session duration average
- Password reset requests

### Alerts
- Failed login spike (>100/min)
- Token refresh failures (token theft indicator)
- Database connection failures
- Redis connection failures
- Email delivery failures

### Logging
- Authentication events (login, logout, register)
- Security events (failed logins, token refresh, MFA changes)
- Admin actions (session revocation, password resets)

## Success Criteria

- [ ] User can register with email verification
- [ ] User can login with email/password
- [ ] User can login with social providers (Google, GitHub)
- [ ] User can enable/disable MFA
- [ ] User can reset forgotten password
- [ ] Access tokens expire and refresh automatically
- [ ] Sessions can be listed and revoked
- [ ] Rate limiting prevents brute force attacks
- [ ] All endpoints use HTTPS in production
- [ ] Test coverage >80%
- [ ] Security audit passes with no critical findings
- [ ] Load test handles 100 req/sec login throughput

## Future Enhancements

- WebAuthn/FIDO2 support
- Biometric authentication (mobile)
- Risk-based authentication (unusual location, device)
- OAuth2 device flow (smart TVs, IoT)
- SAML 2.0 integration (enterprise SSO)
- Audit log (all auth events)
