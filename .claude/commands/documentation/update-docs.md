# Update Documentation

Identify outdated documentation and generate updates based on recent code changes.

## Usage
/update-docs [path] [--type api|readme|user-guide|all]

## What This Does
1. Analyzes recent code changes (git history)
2. Identifies affected documentation sections
3. Detects outdated examples, APIs, and usage instructions
4. Generates updated documentation content
5. Preserves documentation style and tone
6. Creates comprehensive change summary

## Example
/update-docs docs/api --type api

## Agent Coordination
1. **Main LLM**: Analyzes code changes and identifies documentation gaps
   - Reads git log for recent changes
   - Identifies modified functions, APIs, components
   - Maps code changes to documentation sections
2. **technical-writer**: Generates updated documentation
   - Rewrites outdated sections
   - Updates code examples
   - Maintains consistent style and tone
   - Ensures technical accuracy
3. **git-workflow-manager**: Commits documentation updates

## Output
Documentation Update Report:
```markdown
## Documentation Update Analysis

### Recent Code Changes Analyzed
- Time range: Last 30 commits
- Files changed: 45
- Functions modified: 23
- New APIs: 7
- Deprecated APIs: 3

### Outdated Documentation Found

#### 1. README.md - Installation Section
**Issue**: Installation instructions reference old npm scripts
**Changes**: Package.json scripts renamed in commit abc123
**Impact**: Users cannot follow installation guide

**Current** (Outdated):
```bash
npm run setup
npm run dev
```

**Updated** (Current):
```bash
npm install
npm run start:dev
```

#### 2. API Documentation - Authentication
**Issue**: /auth/login endpoint signature changed
**Changes**: Added optional 'remember_me' parameter in commit def456
**Impact**: API documentation missing new parameter

**Current** (Outdated):
```typescript
POST /auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Updated** (Current):
```typescript
POST /auth/login
{
  "email": "user@example.com",
  "password": "password123",
  "remember_me": boolean  // Optional: extends session to 30 days
}
```

#### 3. Component Documentation - UserProfile
**Issue**: Props interface changed, added new required prop
**Changes**: Added 'role' prop to UserProfile component in commit ghi789
**Impact**: Component usage examples are incomplete

**Current** (Outdated):
```tsx
<UserProfile
  name={user.name}
  email={user.email}
/>
```

**Updated** (Current):
```tsx
<UserProfile
  name={user.name}
  email={user.email}
  role={user.role}  // Required: 'admin' | 'user' | 'guest'
/>
```

#### 4. Configuration Guide
**Issue**: Environment variables changed
**Changes**: DATABASE_URL split into separate host/port variables
**Impact**: Setup guide will cause configuration errors

**Current** (Outdated):
```bash
DATABASE_URL=postgres://localhost:5432/mydb
```

**Updated** (Current):
```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=mydb
```

#### 5. API Reference - Deprecated Endpoints
**Issue**: Old endpoint not marked as deprecated
**Changes**: /api/v1/users deprecated in favor of /api/v2/users
**Impact**: Developers may use deprecated endpoint

**Update Required**:
```markdown
### GET /api/v1/users ⚠️ DEPRECATED

**Status**: Deprecated as of v2.0.0
**Migration**: Use GET /api/v2/users instead
**Removal**: Planned for v3.0.0

This endpoint is maintained for backward compatibility but will be removed.
Please migrate to the v2 endpoint which includes pagination and filtering.
```

### New Features Undocumented

#### 6. OAuth2 Authentication (NEW)
**Changes**: Complete OAuth2 implementation added in commits abc-def
**Impact**: Major feature with no documentation

**Documentation Needed**:
- Setup guide for OAuth2 clients
- Authorization flow documentation
- Token refresh examples
- Security best practices

#### 7. Rate Limiting (NEW)
**Changes**: Rate limiting middleware added to all API endpoints
**Impact**: API behavior changed, no documentation

**Documentation Needed**:
- Rate limit headers explanation
- Limits per endpoint
- How to handle 429 responses
- Rate limit tier information

### Proposed Documentation Updates

**Files to Update**:
1. `README.md` - Installation section
2. `docs/api/authentication.md` - Login endpoint
3. `docs/components/UserProfile.md` - Props interface
4. `docs/setup/configuration.md` - Environment variables
5. `docs/api/endpoints.md` - Add deprecation warnings

**Files to Create**:
6. `docs/features/oauth2.md` - New OAuth2 guide
7. `docs/api/rate-limiting.md` - Rate limit documentation

**Estimated Time**: 2-3 hours

### Auto-Generated Documentation

I can automatically update the following sections:

**1. README.md Installation** (Ready):
```markdown
## Installation

### Prerequisites
- Node.js 18+ or 20+
- PostgreSQL 14+
- Redis 6+

### Setup
```bash
# Clone repository
git clone https://github.com/org/project.git
cd project

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
npm run migrate

# Start development server
npm run start:dev
```
```

**2. API Authentication Documentation** (Ready):
[Full updated API docs with new parameters...]

**3. Component Props Reference** (Ready):
[Updated component documentation with new props...]

Would you like me to:
1. Apply all documentation updates automatically
2. Review updates one by one for approval
3. Create only new documentation (OAuth2, rate limiting)
4. Generate full documentation diff for review
```

The technical-writer ensures all documentation stays synchronized with code changes.
