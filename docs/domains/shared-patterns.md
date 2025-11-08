# Shared Domain Patterns

Common architectural patterns and best practices used across multiple domains (backend, frontend, data, infrastructure, security).

## Purpose

This document consolidates patterns that appear in 3+ domain configurations, providing:
- Single source of truth for cross-domain patterns
- Consistent terminology and approaches
- Domain-specific implementation guidance via references

## Pattern Index

- [Layered Architecture](#layered-architecture) - Backend, Frontend, Data
- [Error Handling](#error-handling) - All domains
- [Testing Strategy](#testing-strategy) - All domains
- [Security Patterns](#security-patterns) - Backend, Frontend, Infrastructure, Security
- [Performance Optimization](#performance-optimization) - Backend, Frontend, Data
- [CI/CD Patterns](#cicd-patterns) - Infrastructure, Backend

---

## Layered Architecture

**Applies to**: Backend, Frontend, Data

### Pattern Description

Organize code into distinct layers with clear responsibilities and dependencies flowing in one direction.

```
Presentation Layer (UI/API)
    ↓
Business Logic Layer (Services)
    ↓
Data Access Layer (Repositories)
    ↓
Data Storage Layer (Database)
```

### Implementation by Domain

**Backend**: See [Backend Domain - Layered Architecture](../../.claude/domains/backend.md#architecture-patterns)
- Controller → Service → Repository → Model
- Express routes → Business services → Data repositories → MongoDB/PostgreSQL

**Frontend**: See [Frontend Domain - Component Architecture](../../.claude/domains/frontend.md#component-architecture)
- Pages → Containers → Components → Hooks/Services
- Atomic Design: Atoms → Molecules → Organisms → Templates → Pages

**Data**: See [Data Domain - Data Architecture](../../.claude/domains/data.md#data-architecture-patterns)
- Bronze (raw) → Silver (cleaned) → Gold (business-ready)
- Medallion architecture for data pipelines

### Key Principles
1. **Separation of Concerns**: Each layer has single responsibility
2. **Dependency Direction**: Higher layers depend on lower, never reverse
3. **Abstraction**: Layers interact through interfaces
4. **Testability**: Each layer can be tested independently

---

## Error Handling

**Applies to**: All domains

### Pattern Description

Consistent error handling approach across all system components.

### Error Classification

```typescript
// Standard error structure
interface SystemError {
  code: string;        // Machine-readable error code
  message: string;     // Human-readable message
  details?: any;       // Additional context
  statusCode: number;  // HTTP status (APIs)
  timestamp: string;   // ISO timestamp
}
```

### Error Handling Hierarchy

```
1. Try-Catch at execution level
2. Error middleware/boundaries at integration level
3. Global error handler at application level
4. Monitoring/alerting at infrastructure level
```

### Implementation by Domain

**Backend**: [Backend Error Handling](../../.claude/domains/backend.md#error-handling)
- Global Express error middleware
- Custom error classes (NotFoundError, ValidationError)
- Structured logging with context

**Frontend**: [Frontend Error Handling](../../.claude/domains/frontend.md#performance-patterns)
- Error Boundaries (React)
- Try-catch in async operations
- User-friendly error messages

**Infrastructure**: [Infrastructure Monitoring](../../.claude/domains/infrastructure.md#monitoring--observability-top-5)
- CloudWatch error logging
- SNS notifications for critical errors
- X-Ray distributed tracing

**Security**: [Security Error Handling](../../.claude/domains/security.md#secure-coding-practices)
- No information leakage in error messages
- Audit logging for security events
- Rate limiting on error-prone endpoints

### Best Practices
1. **Log errors with context** (user ID, request ID, stack trace)
2. **Don't expose internal details** to end users
3. **Use appropriate status codes** (4xx client error, 5xx server error)
4. **Implement retry logic** for transient failures
5. **Alert on error rate thresholds**

---

## Testing Strategy

**Applies to**: All domains

### Testing Pyramid

```
       /\
      /E2E\
     /------\
    /Integr-\
   /----------\
  /   Unit    \
 /--------------\
```

- **Unit Tests**: 70% of tests, fast execution, isolated components
- **Integration Tests**: 20% of tests, component interactions
- **E2E Tests**: 10% of tests, critical user flows

### Test Coverage Standards

| Domain | Unit | Integration | E2E | Total Target |
|--------|------|-------------|-----|--------------|
| Backend | 70%+ | Required for APIs | Critical flows | 80%+ |
| Frontend | 80%+ | Component interactions | User journeys | 85%+ |
| Data | 60%+ | Pipeline tests | Data quality | 70%+ |

### Implementation by Domain

**Backend**: [Backend Testing](../../.claude/domains/backend.md#testing-requirements)
- Unit: Jest for services
- Integration: Supertest for API endpoints
- E2E: Pactum for workflows

**Frontend**: [Frontend Testing](../../.claude/domains/frontend.md#testing-requirements)
- Unit: Jest + React Testing Library
- Integration: Component interactions
- E2E: Cypress or Playwright

**Data**: [Data Testing](../../.claude/domains/data.md#quality-standards)
- Unit: dbt tests
- Integration: Pipeline validation
- Data quality: Schema validation

**Infrastructure**: [Infrastructure Testing](../../.claude/domains/infrastructure.md#deployment-standards)
- Infrastructure: CDK synth validation
- Deployment: Smoke tests
- Security: Scanner tests

### Test Naming Convention

```typescript
describe('[Component/Module]', () => {
  describe('[Method/Function]', () => {
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

---

## Security Patterns

**Applies to**: Backend, Frontend, Infrastructure, Security

### Defense in Depth

Multiple layers of security controls:

```
Application Security
    ↓
Network Security
    ↓
Infrastructure Security
    ↓
Data Security
```

### Common Security Controls

| Control | Backend | Frontend | Infrastructure | Purpose |
|---------|---------|----------|----------------|---------|
| Input Validation | ✅ Server-side | ✅ Client-side | ✅ WAF rules | Prevent injection |
| Authentication | ✅ JWT/OAuth | ✅ Token storage | ✅ IAM | Identity verification |
| Authorization | ✅ RBAC/ABAC | ✅ Route guards | ✅ IAM policies | Access control |
| Encryption | ✅ TLS | ✅ HTTPS | ✅ KMS | Data protection |
| Rate Limiting | ✅ Middleware | N/A | ✅ WAF/API Gateway | DoS prevention |
| Logging | ✅ Audit logs | ✅ Error tracking | ✅ CloudTrail | Incident response |

### Implementation by Domain

**Security**: [Security Patterns](../../.claude/domains/security.md#patterns--conventions)
- Comprehensive security controls
- Threat modeling process
- Incident response procedures

**Backend**: [Backend Security](../../.claude/domains/backend.md#security-patterns)
- JWT authentication
- Input validation (Joi/Zod)
- SQL injection prevention

**Frontend**: [Frontend Security](../../.claude/domains/frontend.md#accessibility-standards)
- XSS prevention
- CSRF protection
- CSP headers

**Infrastructure**: [Infrastructure Security](../../.claude/domains/infrastructure.md#security-standards)
- IAM least privilege
- Encryption at rest/transit
- Network isolation (VPCs, security groups)

### OWASP Top 10 Coverage

All domains must address:
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Authentication Failures
8. Software and Data Integrity Failures
9. Logging and Monitoring Failures
10. Server-Side Request Forgery

See [Security Domain - OWASP](../../.claude/domains/security.md#compliance-frameworks-top-5) for detailed guidance.

---

## Performance Optimization

**Applies to**: Backend, Frontend, Data

### Performance Optimization Hierarchy

```
1. Measure (establish baseline)
2. Identify bottlenecks (profiling)
3. Optimize (targeted improvements)
4. Validate (verify improvement)
```

### Common Optimizations

| Technique | Backend | Frontend | Data | Impact |
|-----------|---------|----------|------|--------|
| Caching | ✅ Redis | ✅ Browser/CDN | ✅ Query results | High |
| Indexing | ✅ DB indexes | N/A | ✅ DB/warehouse | High |
| Lazy Loading | N/A | ✅ Code splitting | ✅ Incremental ETL | Medium |
| Connection Pooling | ✅ DB connections | N/A | ✅ DB connections | Medium |
| Query Optimization | ✅ N+1 prevention | ✅ GraphQL batching | ✅ SQL tuning | High |
| Compression | ✅ gzip | ✅ Bundle optimization | ✅ Parquet/ORC | Medium |

### Performance Metrics

**Backend**: See [Backend Performance](../../.claude/domains/backend.md#performance-metrics)
- Response time: <200ms (p95)
- Throughput: 1000 req/s minimum
- Error rate: <0.1%

**Frontend**: See [Frontend Performance](../../.claude/domains/frontend.md#performance-metrics)
- FCP: <1.8s
- LCP: <2.5s
- TTI: <3.8s

**Data**: See [Data Performance](../../.claude/domains/data.md#performance-metrics)
- Query response: <100ms (OLTP)
- Pipeline duration: <1 hour for daily
- Data freshness: <15 minutes

### Anti-Patterns to Avoid

1. **Premature Optimization**: Optimize based on metrics, not assumptions
2. **Over-Caching**: Cache invalidation is hard
3. **SELECT ***: Fetch only needed columns
4. **N+1 Queries**: Use joins or eager loading
5. **No Pagination**: Load data in chunks

---

## CI/CD Patterns

**Applies to**: Infrastructure, Backend, Frontend

### Standard CI/CD Pipeline

```
Code Commit
    ↓
Lint & Type Check
    ↓
Unit Tests
    ↓
Build
    ↓
Integration Tests
    ↓
Security Scan
    ↓
Deploy to Staging
    ↓
E2E Tests
    ↓
Deploy to Production
```

### Deployment Strategies

| Strategy | Use Case | Downtime | Rollback |
|----------|----------|----------|----------|
| Blue-Green | Production deploys | Zero | Instant (switch traffic) |
| Canary | Gradual rollout | Zero | Progressive (reduce %) |
| Rolling | Server updates | Minimal | Slower |
| Recreate | Dev/test environments | Yes | Re-deploy previous |

### Implementation by Domain

**Infrastructure**: [Infrastructure CI/CD](../../.claude/domains/infrastructure.md#deployment-strategies)
- CDK deployment pipelines
- Infrastructure testing
- Automated rollback

**Backend**: [Backend Deployment](../../.claude/domains/backend.md#domain-specific-commands)
- Serverless Framework deployment
- Lambda function updates
- Database migrations

**Frontend**: [Frontend Deployment](../../.claude/domains/frontend.md#build--deploy)
- S3 + CloudFront deployment
- Cache invalidation
- Progressive rollout

### Quality Gates

Required checks before deployment:
1. ✅ All tests passing
2. ✅ Code coverage ≥ threshold
3. ✅ Security scan clean
4. ✅ Dependency audit passed
5. ✅ Performance benchmarks met
6. ✅ Manual approval (production)

### Environment Strategy

```
development (local)
    ↓
dev (shared dev environment)
    ↓
staging (production mirror)
    ↓
production
```

---

## Usage Guidelines

### When to Reference Shared Patterns

Use shared patterns when:
1. Pattern applies to 3+ domains
2. Implementation is conceptually similar across domains
3. Consistency is important across system

### When to Keep Domain-Specific

Keep in domain configs when:
1. Implementation details differ significantly
2. Pattern is unique to domain
3. Domain-specific tools/frameworks required

### Updating Shared Patterns

1. Propose change via PR to this file
2. Verify change applies across all referenced domains
3. Update domain-specific implementations if needed
4. Ensure backward compatibility

---

## Related Documentation

- [Backend Domain](../../.claude/domains/backend.md)
- [Frontend Domain](../../.claude/domains/frontend.md)
- [Data Domain](../../.claude/domains/data.md)
- [Infrastructure Domain](../../.claude/domains/infrastructure.md)
- [Security Domain](../../.claude/domains/security.md)

## Maintenance

**Last Updated**: 2025-11-08
**Review Frequency**: Quarterly
**Owner**: Architecture Team
