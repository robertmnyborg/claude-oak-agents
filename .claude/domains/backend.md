---
domain: backend
priority: 1
primary_agent: infrastructure-specialist
secondary_agents: [security-auditor, qa-specialist, git-workflow-manager]
related_agents: [spec-manager, systems-architect, dependency-scanner, debug-specialist]
---

# Domain: Backend Development

## Tech Stack

### Core Technologies
- **Runtime**: Node.js (16.x, 18.x, 20.x)
- **Language**: TypeScript (strict mode), JavaScript ES2022+
- **Frameworks**: Express.js, NestJS, Fastify, Koa
- **API Styles**: REST, GraphQL (Apollo Server), gRPC

### Serverless Platforms
- **AWS Lambda**: Serverless Framework, SAM
- **Deployment**: Serverless Framework with Node.js runtime
- **Event Sources**: API Gateway, SNS, SQS, DynamoDB Streams, EventBridge

### Databases
- **Relational**: PostgreSQL 14+, MySQL 8+
- **Document**: MongoDB 5+, DynamoDB
- **In-Memory**: Redis, ElastiCache
- **Search**: Elasticsearch, OpenSearch

### Message Queues & Streaming
- **Message Queues**: AWS SQS, RabbitMQ
- **Pub/Sub**: AWS SNS, Redis Pub/Sub
- **Streaming**: Kafka, AWS Kinesis
- **Event-Driven**: EventBridge, custom event systems

### Testing & Quality
- **Unit Testing**: Jest, Mocha, Vitest
- **Integration Testing**: Supertest, Pactum
- **E2E Testing**: Postman, REST Client
- **Mocking**: Sinon, jest.mock
- **Code Quality**: ESLint, Prettier, SonarQube

## Patterns & Conventions

### Architecture Patterns
1. **Layered Architecture**: Controller → Service → Repository → Model
2. **Domain-Driven Design**: Entity-centric design with bounded contexts
3. **CQRS**: Separate read/write models for complex domains
4. **Event-Driven**: Async communication via events (SNS/SQS)
5. **Microservices**: Independent services with clear boundaries

### Code Organization
```
src/
├── api/                # Express routes and controllers
│   └── routes/         # API route definitions
├── modules/            # Domain modules
│   ├── users/
│   │   ├── services/   # Business logic
│   │   ├── models/     # Data models
│   │   ├── repositories/ # Data access
│   │   └── types/      # TypeScript types
├── core/               # Shared infrastructure
│   ├── models/         # Base models (Mongoose)
│   ├── repositories/   # Base repository patterns
│   ├── middleware/     # Express middleware
│   └── utils/          # Helper functions
├── config/             # Configuration management
├── workers/            # Background job handlers
└── functions/          # Serverless Lambda functions
```

### Naming Conventions
- **Files**: kebab-case (`user-service.ts`)
- **Classes**: PascalCase (`UserService`)
- **Functions/Variables**: camelCase (`findUserById`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- **Interfaces**: PascalCase with 'I' prefix optional (`IUserRepository` or `UserRepository`)

### API Design Best Practices
1. **RESTful Conventions**:
   - GET `/users` - List users
   - GET `/users/:id` - Get user
   - POST `/users` - Create user
   - PUT `/users/:id` - Update user
   - DELETE `/users/:id` - Delete user

2. **Versioning**: `/api/v1/users`, `/api/v2/users`

3. **Response Format**:
```typescript
{
  "success": true,
  "data": { /* payload */ },
  "error": null,
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

4. **Error Handling**:
```typescript
{
  "success": false,
  "data": null,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with id 123 not found",
    "details": []
  }
}
```

5. **Status Codes**:
   - 200 OK, 201 Created, 204 No Content
   - 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
   - 500 Internal Server Error, 503 Service Unavailable

### Database Patterns
1. **Repository Pattern**: Abstract data access logic
2. **Unit of Work**: Transaction management
3. **Connection Pooling**: Reuse database connections
4. **Query Optimization**: Use indexes, avoid N+1 queries
5. **Migration Strategy**: Version-controlled schema changes

### Error Handling
1. **Global Error Handler**: Centralized error middleware
2. **Custom Error Classes**: `NotFoundError`, `ValidationError`, `UnauthorizedError`
3. **Error Logging**: Structured logging with context
4. **Error Monitoring**: Sentry, CloudWatch integration
5. **Graceful Degradation**: Fallback strategies

### Security Patterns
1. **Authentication**: JWT, OAuth2, API Keys
2. **Authorization**: RBAC, ABAC, Policy-based
3. **Input Validation**: Joi, Zod, class-validator
4. **SQL Injection Prevention**: Parameterized queries, ORM
5. **Rate Limiting**: Express-rate-limit, API Gateway throttling
6. **CORS**: Whitelist origins, credentials handling

## File Structure & Organization

### Modular Monolith Structure
```
src/
├── modules/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.middleware.ts
│   │   ├── auth.types.ts
│   │   └── auth.test.ts
│   ├── users/
│   │   ├── user.model.ts
│   │   ├── user.repository.ts
│   │   ├── user.service.ts
│   │   ├── user.controller.ts
│   │   └── user.test.ts
├── core/
│   ├── database/
│   │   ├── connection.ts
│   │   ├── migrations/
│   │   └── seeds/
│   ├── middleware/
│   │   ├── auth.middleware.ts
│   │   ├── error.middleware.ts
│   │   └── logger.middleware.ts
│   └── utils/
│       ├── logger.ts
│       └── validators.ts
├── config/
│   ├── database.ts
│   ├── redis.ts
│   └── aws.ts
└── server.ts
```

### Serverless Structure
```
src/
├── functions/          # Lambda function handlers
│   ├── http/           # API Gateway handlers
│   │   ├── users/
│   │   │   ├── create.ts
│   │   │   ├── get.ts
│   │   │   └── list.ts
│   ├── events/         # Event-driven handlers
│   │   ├── user-created.ts
│   │   └── order-processed.ts
│   └── scheduled/      # Cron/scheduled tasks
│       └── daily-report.ts
├── layers/             # Lambda layers
│   └── common/
│       ├── models/
│       ├── services/
│       └── utils/
├── config/
│   └── environment.ts
└── serverless.yml      # Serverless Framework config
```

## Agent Workflows

### Simple API Endpoint
**Trigger**: "Create GET /users endpoint", "Add user login API"
```
infrastructure-specialist → security-auditor → qa-specialist → git-workflow-manager
```

### New Service Development
**Trigger**: "Build notification service", "Create payment processing API"
```
spec-manager → systems-architect → infrastructure-specialist → security-auditor → qa-specialist → dependency-scanner → git-workflow-manager
```

### Database Integration
**Trigger**: "Add PostgreSQL schema", "Implement data access layer"
```
spec-manager → infrastructure-specialist → qa-specialist → git-workflow-manager
```

### Event-Driven Feature
**Trigger**: "Set up SNS/SQS pipeline", "Implement async processing"
```
systems-architect → infrastructure-specialist → security-auditor → qa-specialist
```

### Performance Optimization
**Trigger**: "Optimize API response time", "Fix N+1 query problem"
```
debug-specialist (analysis) → infrastructure-specialist (implementation) → qa-specialist
```

### Debugging & Troubleshooting
**Trigger**: "API returns 500 error", "Database connection timeout"
```
debug-specialist → infrastructure-specialist (fix) → qa-specialist
```

## Triggers

### Keywords
- **API-related**: API, endpoint, route, REST, GraphQL, controller
- **Backend-specific**: server, backend, service, Lambda, serverless
- **Database**: database, query, schema, migration, model, repository
- **Event-driven**: event, SNS, SQS, Kafka, message queue, pub/sub
- **Auth**: authentication, authorization, JWT, OAuth, token
- **Data processing**: worker, job, cron, scheduled, batch
- **Integration**: webhook, third-party, external API

### File Patterns
- `src/api/**/*`
- `src/modules/**/*`
- `src/core/**/*`
- `src/functions/**/*`
- `src/workers/**/*`
- `*.service.ts`, `*.controller.ts`
- `*.model.ts`, `*.repository.ts`
- `serverless.yml`, `serverless/`
- `*.test.ts`, `*.spec.ts`

### Tech Stack Mentions
- Express, NestJS, Fastify, Koa
- MongoDB, PostgreSQL, DynamoDB, Redis
- Lambda, Serverless Framework
- SNS, SQS, Kinesis, EventBridge
- Node.js, TypeScript

## Quality Standards

### Code Quality
- **TypeScript Strict Mode**: All strict flags enabled
- **ESLint Compliance**: Zero errors, zero warnings
- **Code Coverage**: 70%+ for services, 80%+ for critical paths
- **Cyclomatic Complexity**: < 10 per function
- **No `any` Types**: Use proper TypeScript types

### API Standards
- **Swagger/OpenAPI**: API documentation required
- **Consistent Responses**: Standard response format
- **Error Handling**: Proper status codes and error messages
- **Versioning**: API version in URL
- **Validation**: Input validation on all endpoints

### Testing Requirements
- **Unit Tests**: 70%+ coverage for business logic
- **Integration Tests**: All API endpoints tested
- **E2E Tests**: Critical user flows
- **Load Testing**: Performance under load (Artillery, k6)
- **Contract Testing**: API contract validation (Pact)

### Performance Metrics
- **Response Time**: < 200ms (p95)
- **Throughput**: 1000 req/s minimum
- **Error Rate**: < 0.1%
- **Database Query Time**: < 50ms (p95)
- **Lambda Cold Start**: < 1s

### Security Standards
- **OWASP Top 10**: All vulnerabilities addressed
- **Dependency Scanning**: Regular npm audit, Snyk scans
- **Secrets Management**: AWS Secrets Manager, no hardcoded credentials
- **Input Validation**: All inputs sanitized and validated
- **Rate Limiting**: Protect against DDoS
- **Logging**: Audit logs for sensitive operations

## Common Tasks & Solutions

### Creating a New API Endpoint
1. Define route in `src/api/routes/`
2. Implement controller in `src/modules/<domain>/`
3. Create service layer with business logic
4. Add input validation (Joi/Zod)
5. Write unit and integration tests
6. Document in Swagger/OpenAPI
7. Add authentication/authorization if needed

### Database Integration
1. Define model/schema (Mongoose, TypeORM, Prisma)
2. Create repository for data access
3. Implement service layer using repository
4. Write migration scripts
5. Add indexes for performance
6. Test with real database in integration tests

### Serverless Function Development
1. Create handler in `src/functions/`
2. Define event trigger in `serverless.yml`
3. Implement business logic
4. Add environment variables
5. Configure IAM permissions
6. Test locally with `serverless invoke local`
7. Deploy with `serverless deploy`

### Event-Driven Workflow
1. Define event schema/contract
2. Create SNS topic (infrastructure)
3. Implement publisher service
4. Create SQS queue for consumer
5. Implement consumer Lambda function
6. Add error handling and DLQ
7. Monitor with CloudWatch

### Error Handling Setup
1. Create custom error classes
2. Implement global error middleware
3. Add error logging (CloudWatch, Sentry)
4. Define error response format
5. Handle async errors (express-async-errors)
6. Add health check endpoint

## Integration Points

### Frontend Integration
- **API Gateway**: RESTful endpoints, CORS configuration
- **WebSockets**: Socket.io, AWS API Gateway WebSocket
- **Authentication**: JWT token validation
- **File Upload**: S3 pre-signed URLs

### Infrastructure Integration
- **Deployment**: Serverless Framework, AWS CDK
- **Monitoring**: CloudWatch, X-Ray tracing
- **Logging**: CloudWatch Logs, structured logging
- **Secrets**: AWS Secrets Manager, Parameter Store

### Data Integration
- **Database Connections**: Connection pooling, read replicas
- **Caching**: Redis for session, query results
- **Search**: Elasticsearch integration
- **Analytics**: Kinesis data streams

### Third-Party Services
- **Payment**: Stripe, PayPal integration
- **Email**: SendGrid, SES
- **SMS**: Twilio, SNS
- **Storage**: S3, CloudFront

## Domain-Specific Commands

### Development
```bash
# Install dependencies
yarn install

# Type checking
yarn ts:check / tsc --noEmit

# Linting
yarn lint
yarn lint:fix

# Run locally
yarn start:api:local
yarn sls:local / serverless offline

# Invoke Lambda locally
yarn invoke:local <function-name>
serverless invoke local -f functionName
```

### Testing
```bash
# Unit tests
yarn test:unit
yarn test:unit:watch
yarn test:unit -u <file>.test.ts

# Integration tests
yarn test:integration

# E2E tests
yarn test:e2e

# Coverage report
yarn test:coverage
```

### Database Operations
```bash
# Run migrations
yarn migrate:up
yarn migrate:down

# Seed database
yarn db:seed

# Connect to database
yarn db:connect
```

### Deployment
```bash
# Serverless deployment
yarn sls deploy
serverless deploy --stage prod

# Deploy specific function
serverless deploy function -f functionName

# View logs
serverless logs -f functionName -t
```

### Docker Operations
```bash
# Start local services
yarn dc:up
docker-compose up -d

# Stop services
yarn dc:down
docker-compose down

# View logs
docker-compose logs -f <service>
```

## Decision Framework

### When to Use This Domain
- ✅ Building APIs and services
- ✅ Implementing business logic
- ✅ Database operations
- ✅ Event-driven processing
- ✅ Serverless functions
- ✅ Background jobs and workers

### When to Coordinate with Other Domains
- **Frontend**: API contract design, response formats
- **Infrastructure**: Deployment configuration, AWS services
- **Security**: Authentication flows, authorization logic
- **Data**: Schema design, query optimization

## Example Scenarios

### Scenario 1: Simple REST API
**Request**: "Create API endpoint to get user profile"

**Domain Detection**: Backend (keywords: API, endpoint, user)

**Workflow**:
```
infrastructure-specialist:
  - Create GET /api/v1/users/:id route
  - Implement UserController.getProfile()
  - Create UserService.findById()
  - Add JWT authentication middleware
  - Write unit tests
  - Add Swagger documentation

security-auditor:
  - Verify authentication required
  - Check authorization (user can access own profile)
  - Validate input sanitization

qa-specialist:
  - Test successful retrieval
  - Test 404 for non-existent user
  - Test 401 for unauthenticated request
  - Verify response format

git-workflow-manager:
  - Commit with API endpoint documentation
  - Create PR with curl examples
```

### Scenario 2: Event-Driven Processing
**Request**: "When user registers, send welcome email asynchronously"

**Domain Detection**: Backend + Infrastructure (keywords: event, async, email)

**Workflow**:
```
spec-manager:
  - Define user registration event schema
  - Specify email template requirements
  - Define retry/failure handling

systems-architect:
  - Design event flow: Registration → SNS → SQS → Lambda
  - Plan error handling and DLQ
  - Define monitoring strategy

infrastructure-specialist:
  1. Modify user registration service:
     - Publish event to SNS topic after user creation
     - Add event payload with user data

  2. Create email worker Lambda:
     - Subscribe to SQS queue
     - Implement email sending logic (SES)
     - Handle errors and retries

  3. Configure infrastructure:
     - Create SNS topic
     - Create SQS queue with DLQ
     - Set up IAM permissions

security-auditor:
  - Verify event data doesn't contain sensitive info
  - Check SES sandbox/production mode
  - Validate rate limiting

qa-specialist:
  - Test event publishing
  - Verify email delivery
  - Test retry logic
  - Verify DLQ for failures
```

### Scenario 3: Database Optimization
**Request**: "API is slow, optimize database queries"

**Domain Detection**: Backend + Data (keywords: slow, optimize, queries)

**Workflow**:
```
debug-specialist:
  1. Analysis:
     - Profile API requests
     - Identify slow endpoints
     - Use EXPLAIN to analyze queries
     - Identify N+1 query problems

infrastructure-specialist:
  1. Optimization:
     - Add database indexes
     - Implement query result caching (Redis)
     - Refactor N+1 queries to use joins
     - Add pagination to large datasets
     - Implement connection pooling

  2. Verification:
     - Measure query performance improvements
     - Monitor cache hit rates
     - Verify functionality unchanged

qa-specialist:
  - Performance testing (before/after)
  - Verify data accuracy
  - Test edge cases (empty results, large datasets)
```

### Scenario 4: Third-Party Integration
**Request**: "Integrate Stripe for payment processing"

**Domain Detection**: Backend + Security (keywords: payment, Stripe, integration)

**Workflow**:
```
spec-manager:
  - Define payment flow requirements
  - List supported payment methods
  - Specify webhook handling

infrastructure-specialist:
  1. Setup:
     - Install Stripe SDK
     - Configure API keys (Secrets Manager)
     - Create payment service

  2. Implementation:
     - Create payment intent endpoint
     - Implement webhook handler
     - Handle successful/failed payments
     - Store transaction records

  3. Error Handling:
     - Handle Stripe API errors
     - Implement idempotency
     - Add retry logic

security-auditor:
  - Verify webhook signature validation
  - Check PCI compliance (no card data storage)
  - Validate HTTPS only
  - Review API key management

dependency-scanner:
  - Check Stripe SDK vulnerabilities
  - Audit dependencies

qa-specialist:
  - Test successful payment flow
  - Test failed payment scenarios
  - Verify webhook handling
  - Test idempotency
```

## Anti-Patterns to Avoid

### Common Mistakes
1. **God Objects**: Services doing too much (violates SRP)
2. **Callback Hell**: Use async/await or Promises
3. **Synchronous Processing**: Use async for I/O operations
4. **Ignoring Errors**: Always handle errors properly
5. **No Input Validation**: Validate all user inputs
6. **Hardcoded Credentials**: Use environment variables/secrets manager
7. **Missing Logging**: Add structured logging everywhere
8. **No Transactions**: Use transactions for multi-step operations

### Architecture Anti-Patterns
- **Big Ball of Mud**: No clear structure or separation
- **Golden Hammer**: Using one solution for everything
- **Premature Optimization**: Optimize based on metrics
- **Tight Coupling**: Services should be loosely coupled
- **Circular Dependencies**: Avoid module circular references

### Database Anti-Patterns
- **N+1 Queries**: Use joins or eager loading
- **Missing Indexes**: Index frequently queried columns
- **SELECT ***: Query only needed columns
- **No Connection Pooling**: Reuse database connections
- **Ignoring Migrations**: Use version-controlled migrations

## Success Metrics

### Development Velocity
- API endpoint creation: < 4 hours
- Service implementation: < 1 day
- Bug fixes: < 2 hours

### Code Quality
- ESLint score: 0 errors, 0 warnings
- Test coverage: > 70%
- Type coverage: 100%
- Security scan: 0 high/critical vulnerabilities

### Performance
- API response time: < 200ms (p95)
- Database query time: < 50ms (p95)
- Lambda cold start: < 1s
- Error rate: < 0.1%

### Reliability
- Uptime: > 99.9%
- Deployment success rate: > 95%
- Zero critical bugs in production

## Resources & References

### Documentation
- [Node.js Docs](https://nodejs.org/docs/)
- [Express.js Guide](https://expressjs.com/)
- [NestJS Docs](https://docs.nestjs.com/)
- [Serverless Framework](https://www.serverless.com/framework/docs)

### Best Practices
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [RESTful API Design](https://restfulapi.net/)
- [Twelve-Factor App](https://12factor.net/)

### Tools
- [Postman](https://www.postman.com/)
- [Jest](https://jestjs.io/)
- [Mongoose](https://mongoosejs.com/)
- [Prisma](https://www.prisma.io/)
