# Pattern: API Versioning Strategies

```yaml
pattern_metadata:
  name: "api-versioning-strategy"
  category: "api"
  difficulty: "intermediate"
  tech_stack: ["REST", "GraphQL", "Node.js", "Express", "OpenAPI"]
  tags: ["api", "versioning", "backward-compatibility", "deprecation", "rest", "graphql"]
  version: "1.0.0"
  status: "stable"
  author: "claude-oak-agents"
  last_updated: "2025-11-08"
```

## Problem Statement

### What Challenge Does This Solve?

APIs evolve over time, requiring version management without breaking existing clients:
- Add new features without breaking old clients
- Deprecate endpoints safely with migration path
- Support multiple API versions simultaneously
- Communicate breaking vs non-breaking changes
- Provide smooth client migration experience

### When Should You Use This Pattern?

Use this pattern when:
- ✅ Public API with external consumers
- ✅ Need backward compatibility guarantees
- ✅ Multiple client versions in production
- ✅ Long-lived API (>1 year lifespan)

Don't use this pattern when:
- ❌ Internal API with controlled clients
- ❌ Can coordinate breaking changes across all clients
- ❌ Rapid prototyping phase (pre-v1.0)

## Solution Overview

### Three Versioning Approaches

#### 1. URL Versioning (Recommended for REST)
```
GET /v1/users/:id
GET /v2/users/:id
```

**Pros**: Simple, explicit, cacheable, easy routing  
**Cons**: URL proliferation, multiple codebases

#### 2. Header Versioning
```
GET /users/:id
Accept: application/vnd.myapp.v2+json
```

**Pros**: Clean URLs, semantic  
**Cons**: Less discoverable, harder to test manually

#### 3. Content Negotiation
```
GET /users/:id
Accept: application/json; version=2
```

**Pros**: Flexible, standards-based  
**Cons**: Complex, harder for clients to understand

### Decision Matrix

| Criteria | URL | Header | Content Negotiation |
|----------|-----|--------|---------------------|
| Simplicity | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Discoverability | ⭐⭐⭐ | ⭐ | ⭐ |
| Caching | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Clean URLs | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Standard Compliance | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

**Recommendation**: URL versioning for REST APIs (simplicity wins)

## Technical Design

### URL Versioning Implementation (Node.js + Express)

```typescript
// app.ts
import express from 'express';
import v1Routes from './routes/v1';
import v2Routes from './routes/v2';

const app = express();

// Mount v1 routes
app.use('/v1', v1Routes);

// Mount v2 routes
app.use('/v2', v2Routes);

// Redirect /api/* to latest version (optional)
app.use('/api', (req, res, next) => {
  req.url = `/v2${req.url}`;
  next();
});

export default app;
```

### Breaking vs Non-Breaking Changes

#### Non-Breaking Changes (No Version Bump)
- ✅ Add new optional field to request
- ✅ Add new field to response
- ✅ Add new endpoint
- ✅ Add new query parameter (optional)
- ✅ Relax validation (accept more values)
- ✅ Return more data in response

#### Breaking Changes (Require New Version)
- ❌ Remove field from response
- ❌ Rename field
- ❌ Change field data type
- ❌ Make optional field required
- ❌ Remove endpoint
- ❌ Change URL structure
- ❌ Tighten validation (reject previously valid input)
- ❌ Change authentication mechanism

### Deprecation Strategy

**Timeline**:
1. **Announcement** (T-0): Deprecation notice in docs + response headers
2. **Warning Period** (T+3 months): Log usage, send deprecation warnings
3. **Migration Support** (T+6 months): Provide migration guide, client library updates
4. **Sunset** (T+12 months): Version removed, returns 410 Gone

**Example Deprecation Header**:
```http
HTTP/1.1 200 OK
Deprecation: version=1.0, sunset=2026-11-08T00:00:00Z
Link: <https://api.example.com/docs/migration/v1-to-v2>; rel="deprecation"
Sunset: Sat, 08 Nov 2026 00:00:00 GMT
```

## Agent Workflow

### Agents Involved
1. **backend-architect** - API version implementation
2. **technical-writer** - Migration guides and documentation
3. **qa-specialist** - Cross-version compatibility testing
4. **quality-gate** - Validation
5. **git-workflow-manager** - Commit and PR

### Execution Sequence
```
backend-architect (implement new version)
  ↓
technical-writer (migration guide + docs)
  ↓
qa-specialist (test v1 ← → v2 compatibility)
  ↓
quality-gate (validation)
  ↓
git-workflow-manager (commit and PR)
```

## Implementation Checklist

### Phase 1: Plan Version Change
- [ ] Identify breaking changes
- [ ] Document migration requirements
- [ ] Choose versioning strategy (URL recommended)
- [ ] Set deprecation timeline

### Phase 2: Implement New Version
- [ ] Create v2 route directory
- [ ] Implement new endpoints/changes
- [ ] Add version to OpenAPI spec
- [ ] Update request/response types

### Phase 3: Maintain Old Version
- [ ] Add deprecation headers to v1
- [ ] Update v1 docs with sunset date
- [ ] Keep v1 functional (bug fixes only)

### Phase 4: Client Migration
- [ ] Publish migration guide
- [ ] Update client SDKs
- [ ] Provide v1 → v2 translation layer (optional)
- [ ] Monitor v1 usage metrics

### Phase 5: Sunset Old Version
- [ ] Send email notifications 3, 1, 0 months before
- [ ] Return 410 Gone for v1 requests
- [ ] Archive v1 code
- [ ] Update docs to remove v1

## Validation Criteria

### Success Metrics
- [ ] v2 endpoints functional
- [ ] v1 endpoints still work during deprecation
- [ ] Clear migration guide published
- [ ] Client SDK updated
- [ ] Deprecation headers present
- [ ] Zero breaking changes to v1

## Examples

### Example 1: Add New Required Field (Breaking)

**v1**: Optional `email` field
```json
POST /v1/users
{
  "name": "John Doe"
}
```

**v2**: Required `email` field
```json
POST /v2/users
{
  "name": "John Doe",
  "email": "john@example.com"  // Now required
}
```

### Example 2: Change Response Structure (Breaking)

**v1**: Flat structure
```json
GET /v1/users/123
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**v2**: Nested structure
```json
GET /v2/users/123
{
  "id": "123",
  "profile": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Example 3: Pagination Change (Breaking)

**v1**: Page-based pagination
```json
GET /v1/projects?page=2&limit=20
```

**v2**: Cursor-based pagination
```json
GET /v2/projects?cursor=abc123&limit=20
```

## Troubleshooting

### Clients Not Migrating from v1
- Send personalized migration support emails
- Provide automated migration tools
- Offer temporary v1 extension (with fee)

### Breaking Change Slipped into v1
- Issue immediate patch release reverting change
- Apologize to users
- Improve testing to prevent future occurrences

## References

- [Stripe API Versioning](https://stripe.com/docs/api/versioning)
- [GitHub API Versioning](https://docs.github.com/en/rest/overview/api-versions)
- [RFC 7234: HTTP Caching](https://tools.ietf.org/html/rfc7234)
- [Sunset Header Spec](https://tools.ietf.org/html/rfc8594)

---

**Pattern Version**: 1.0.0  
**Last Updated**: 2025-11-08  
**Maintained By**: claude-oak-agents community
