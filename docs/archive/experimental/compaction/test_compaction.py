#!/usr/bin/env python3
"""
Simple test demonstrating compaction.py usage.
"""

from compaction import compact_output


def test_research_compression():
    """Test compression of research artifact."""
    full_research = """
# Deep Technical Analysis of Authentication System

## Executive Summary
The authentication system requires comprehensive overhaul to address security vulnerabilities and scalability concerns. Current implementation uses outdated JWT patterns with insufficient token rotation and lacks proper rate limiting.

## Key Findings

### Security Analysis
- JWT tokens expire after 24 hours but lack refresh token mechanism
- Password hashing uses bcrypt with rounds=10 (industry standard is 12-14)
- No account lockout after failed login attempts
- Session management stores tokens in localStorage (vulnerable to XSS)

### Performance Issues
- Database queries for user validation are not indexed
- Auth middleware runs on every request without caching
- Token validation makes unnecessary DB calls

### Architecture Problems
- Monolithic auth service couples multiple responsibilities
- No separation between authentication and authorization
- Hard dependency on single database instance

## Files Analyzed
- `src/auth/jwt-handler.ts` - Token generation and validation
- `src/auth/password-hasher.ts` - Password hashing utilities
- `src/middleware/auth-middleware.ts` - Request authentication
- `src/models/user.model.ts` - User data model
- `config/auth.config.ts` - Authentication configuration

## Recommendations

### Immediate Actions
1. Implement refresh token rotation
2. Increase bcrypt rounds to 12
3. Add rate limiting on login endpoints
4. Move tokens to httpOnly cookies
5. Add database indexes for auth queries

### Medium-term Improvements
- Separate authentication service from main API
- Implement Redis-based session caching
- Add OAuth2/OIDC support for third-party auth
- Create centralized authorization service

### Long-term Vision
- Migrate to dedicated identity provider (Auth0/Cognito)
- Implement zero-trust architecture
- Add biometric authentication support

## Next Steps
- Security audit by external team
- Performance benchmarking
- Migration planning for new auth architecture
- Stakeholder approval for breaking changes
"""

    compressed = compact_output(full_research, "research")
    
    print("ORIGINAL LENGTH:", len(full_research.split('\n')), "lines")
    print("COMPRESSED LENGTH:", len(compressed.split('\n')), "lines")
    print("\n" + "="*80)
    print("COMPRESSED OUTPUT:")
    print("="*80)
    print(compressed)
    print("="*80)


def test_implementation_compression():
    """Test compression of implementation artifact."""
    full_implementation = """
# REST API Implementation Complete

## Overview
Implemented secure REST API with authentication, rate limiting, and comprehensive error handling. API follows OpenAPI 3.0 specification with auto-generated documentation.

## Implementation Details

### API Endpoints Created
- POST /api/v1/auth/login - User authentication
- POST /api/v1/auth/logout - Session termination
- GET /api/v1/users/:id - Retrieve user profile
- PUT /api/v1/users/:id - Update user profile
- DELETE /api/v1/users/:id - Delete user account

### Security Features
- JWT-based authentication with refresh tokens
- Rate limiting: 100 requests/15min per IP
- Input validation using Joi schemas
- SQL injection protection via parameterized queries
- XSS prevention with content sanitization

### Files Created
- `src/api/routes/auth.routes.ts` - Authentication routes
- `src/api/routes/user.routes.ts` - User management routes
- `src/api/middleware/rate-limiter.ts` - Rate limiting middleware
- `src/api/middleware/validator.ts` - Request validation
- `src/api/controllers/auth.controller.ts` - Auth business logic
- `src/api/controllers/user.controller.ts` - User CRUD logic
- `tests/api/auth.test.ts` - Auth endpoint tests
- `tests/api/user.test.ts` - User endpoint tests

## Testing
- Unit test coverage: 87%
- Integration tests: All passing
- Load testing: Handles 1000 req/sec

## What's Next
- Deploy to staging environment
- Run security penetration testing
- Create API client SDK
- Set up monitoring and alerting
"""

    compressed = compact_output(full_implementation, "implementation")
    
    print("\nIMPLEMENTATION COMPRESSION TEST")
    print("ORIGINAL LENGTH:", len(full_implementation.split('\n')), "lines")
    print("COMPRESSED LENGTH:", len(compressed.split('\n')), "lines")
    print("\n" + "="*80)
    print("COMPRESSED OUTPUT:")
    print("="*80)
    print(compressed)
    print("="*80)


if __name__ == "__main__":
    print("COMPACTION UTILITY TEST\n")
    test_research_compression()
    print("\n")
    test_implementation_compression()
