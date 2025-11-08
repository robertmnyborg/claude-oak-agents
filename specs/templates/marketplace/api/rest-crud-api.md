---
template_id: rest-crud-api
template_name: REST CRUD API
category: api
difficulty: intermediate
estimated_time: 4-6 hours
tags: [rest, api, crud, express, typescript, validation]
author: claude-oak-agents
version: 1.0.0
last_updated: 2025-11-08
popularity: 92
dependencies: [express, zod, prisma]
related_templates: [saas-auth-complete, cdk-serverless-api]
---

# REST CRUD API

Production-ready RESTful API with CRUD operations, validation, error handling, and OpenAPI documentation.

## Overview

This template implements a complete REST API following industry best practices:
- RESTful resource endpoints (GET, POST, PUT, PATCH, DELETE)
- Request validation with Zod schemas
- Structured error handling
- OpenAPI/Swagger documentation
- Rate limiting and security headers
- Database integration (Prisma ORM)
- Pagination, filtering, and sorting

## Use Cases

- **Backend for SPA**: API backend for React/Vue applications
- **Mobile App Backend**: REST API for iOS/Android apps
- **Third-Party Integration**: Public API for partners
- **Microservices**: Individual service in microservices architecture

## Requirements

### Technical Prerequisites
- Node.js 18+ or Go 1.21+
- Database (PostgreSQL, MySQL, or MongoDB)
- Prisma ORM (or equivalent)
- Express.js (or Gin for Go)

### API Design Principles
- Resource-based URLs (`/users`, `/users/:id`)
- HTTP methods for operations (GET, POST, PUT, PATCH, DELETE)
- Status codes for responses (200, 201, 400, 404, 500)
- JSON request/response bodies
- Consistent error format

## Implementation Plan

### Phase 1: Project Setup (1 hour)

**1.1 Initialize Project**
```bash
mkdir my-api && cd my-api
npm init -y
npm install express prisma @prisma/client zod
npm install -D typescript @types/express @types/node tsx
npx prisma init
```

**1.2 Database Schema**
```prisma
// prisma/schema.prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String
  role      String   @default("user")
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  posts     Post[]
}

model Post {
  id        String   @id @default(uuid())
  title     String
  content   String
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

**1.3 Run Migrations**
```bash
npx prisma migrate dev --name init
```

### Phase 2: Core API Implementation (2 hours)

**2.1 Validation Schemas**
```typescript
// src/schemas/user.schema.ts
import { z } from 'zod';

export const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  role: z.enum(['user', 'admin']).optional(),
});

export const updateUserSchema = createUserSchema.partial();

export const userIdSchema = z.object({
  id: z.string().uuid(),
});

export type CreateUserDTO = z.infer<typeof createUserSchema>;
export type UpdateUserDTO = z.infer<typeof updateUserSchema>;
```

**2.2 User CRUD Endpoints**
```typescript
// src/routes/users.ts
import { Router } from 'express';
import { prisma } from '../lib/prisma';
import { validate } from '../middleware/validate';
import { createUserSchema, updateUserSchema, userIdSchema } from '../schemas/user.schema';

const router = Router();

// GET /users - List users with pagination
router.get('/', async (req, res) => {
  const page = parseInt(req.query.page as string) || 1;
  const limit = parseInt(req.query.limit as string) || 10;
  const skip = (page - 1) * limit;

  const [users, total] = await Promise.all([
    prisma.user.findMany({
      skip,
      take: limit,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.user.count(),
  ]);

  res.json({
    data: users,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit),
    },
  });
});

// GET /users/:id - Get single user
router.get('/:id', validate(userIdSchema, 'params'), async (req, res) => {
  const user = await prisma.user.findUnique({
    where: { id: req.params.id },
    include: { posts: true },
  });

  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  res.json(user);
});

// POST /users - Create user
router.post('/', validate(createUserSchema), async (req, res) => {
  const user = await prisma.user.create({
    data: req.body,
  });

  res.status(201).json(user);
});

// PUT /users/:id - Replace user
router.put('/:id', validate(userIdSchema, 'params'), validate(createUserSchema), async (req, res) => {
  const user = await prisma.user.update({
    where: { id: req.params.id },
    data: req.body,
  });

  res.json(user);
});

// PATCH /users/:id - Partial update
router.patch('/:id', validate(userIdSchema, 'params'), validate(updateUserSchema), async (req, res) => {
  const user = await prisma.user.update({
    where: { id: req.params.id },
    data: req.body,
  });

  res.json(user);
});

// DELETE /users/:id - Delete user
router.delete('/:id', validate(userIdSchema, 'params'), async (req, res) => {
  await prisma.user.delete({
    where: { id: req.params.id },
  });

  res.status(204).send();
});

export default router;
```

**2.3 Validation Middleware**
```typescript
// src/middleware/validate.ts
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

export function validate(schema: z.ZodSchema, source: 'body' | 'params' | 'query' = 'body') {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const data = source === 'body' ? req.body : source === 'params' ? req.params : req.query;
      const validated = await schema.parseAsync(data);

      if (source === 'body') req.body = validated;
      if (source === 'params') req.params = validated;
      if (source === 'query') req.query = validated;

      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors,
        });
      }
      next(error);
    }
  };
}
```

### Phase 3: Error Handling (1 hour)

**3.1 Error Handler Middleware**
```typescript
// src/middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { Prisma } from '@prisma/client';

export function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  console.error(err);

  // Prisma errors
  if (err instanceof Prisma.PrismaClientKnownRequestError) {
    if (err.code === 'P2002') {
      return res.status(409).json({
        error: 'Unique constraint violation',
        field: err.meta?.target,
      });
    }
    if (err.code === 'P2025') {
      return res.status(404).json({
        error: 'Record not found',
      });
    }
  }

  // Default error
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  });
}
```

**3.2 Async Handler Wrapper**
```typescript
// src/utils/asyncHandler.ts
import { Request, Response, NextFunction } from 'express';

export function asyncHandler(fn: Function) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Usage
router.get('/:id', asyncHandler(async (req, res) => {
  const user = await prisma.user.findUniqueOrThrow({
    where: { id: req.params.id },
  });
  res.json(user);
}));
```

### Phase 4: OpenAPI Documentation (1 hour)

**4.1 Install Swagger**
```bash
npm install swagger-ui-express swagger-jsdoc
npm install -D @types/swagger-ui-express
```

**4.2 Swagger Configuration**
```typescript
// src/swagger.ts
import swaggerJsdoc from 'swagger-jsdoc';

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'My API',
      version: '1.0.0',
      description: 'REST API documentation',
    },
    servers: [
      {
        url: 'http://localhost:3000',
        description: 'Development server',
      },
    ],
  },
  apis: ['./src/routes/*.ts'],
};

export const swaggerSpec = swaggerJsdoc(options);
```

**4.3 Add JSDoc Comments**
```typescript
/**
 * @openapi
 * /users:
 *   get:
 *     summary: List users
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *         description: Page number
 *     responses:
 *       200:
 *         description: List of users
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/User'
 */
router.get('/', async (req, res) => {
  // ...
});
```

**4.4 Serve Swagger UI**
```typescript
// src/app.ts
import swaggerUi from 'swagger-ui-express';
import { swaggerSpec } from './swagger';

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
```

### Phase 5: Security and Rate Limiting (1 hour)

**5.1 Security Headers**
```bash
npm install helmet cors
```

```typescript
import helmet from 'helmet';
import cors from 'cors';

app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3000',
  credentials: true,
}));
```

**5.2 Rate Limiting**
```bash
npm install express-rate-limit
```

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later.',
});

app.use('/api/', limiter);
```

## Agent Workflow

```yaml
agent_sequence:
  phase_1_design:
    - agent: design-simplicity-advisor
      task: "Review API design for simplicity (avoid over-engineering)"
      output: "Recommendation: Start with basic CRUD, add complexity as needed"

    - agent: backend-architect
      task: "Design database schema and API endpoints"
      output: "Prisma schema, endpoint specifications"

  phase_2_implementation:
    - agent: backend-architect
      task: "Implement CRUD endpoints with validation"
      duration: "3 hours"

    - agent: backend-architect
      task: "Add error handling and documentation"
      duration: "1 hour"

  phase_3_security:
    - agent: security-auditor
      task: "Security review: input validation, error messages, headers"
      output: "Security checklist with recommendations"

    - agent: backend-architect
      task: "Implement security measures (helmet, rate limiting)"
      duration: "1 hour"

  phase_4_quality:
    - agent: unit-test-expert
      task: "Comprehensive API tests (happy path + edge cases)"
      coverage: ">80%"

    - agent: qa-specialist
      task: "Integration tests for full CRUD workflows"

    - agent: quality-gate
      task: "Code review and KISS validation"

  phase_5_deployment:
    - agent: git-workflow-manager
      task: "Create PR with API implementation"
```

## Testing Strategy

### Unit Tests
```typescript
describe('User API', () => {
  it('should create user with valid data', async () => {
    const response = await request(app)
      .post('/users')
      .send({ email: 'test@example.com', name: 'Test User' });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
  });

  it('should reject invalid email', async () => {
    const response = await request(app)
      .post('/users')
      .send({ email: 'invalid', name: 'Test' });

    expect(response.status).toBe(400);
    expect(response.body.error).toBe('Validation failed');
  });
});
```

### Integration Tests
- Full CRUD workflow (create → read → update → delete)
- Pagination correctness
- Error scenarios (404, 409, 500)
- Rate limiting enforcement

## Common Pitfalls

### 1. Missing Validation
**Problem**: Accepting any input without validation
**Solution**: Use Zod schemas for all endpoints, validate params and query strings

### 2. Inconsistent Error Format
**Problem**: Different error structures across endpoints
**Solution**: Centralized error handler, consistent error response format

### 3. N+1 Query Problem
**Problem**: Fetching related data in loops
**Solution**: Use Prisma includes, eager loading with `include: { posts: true }`

### 4. Missing Pagination
**Problem**: Returning all records (performance issue)
**Solution**: Always paginate list endpoints, default to reasonable limit (10-50)

### 5. Exposing Internal Errors
**Problem**: Returning stack traces in production
**Solution**: Generic error messages in production, detailed errors in development only

### 6. No Rate Limiting
**Problem**: API abuse via automated requests
**Solution**: Implement rate limiting per IP/user, use Redis for distributed rate limiting

## Success Criteria

- [ ] All CRUD operations implemented (GET, POST, PUT, PATCH, DELETE)
- [ ] Request validation with Zod schemas
- [ ] Error handling with consistent format
- [ ] OpenAPI documentation available at `/api-docs`
- [ ] Security headers configured (Helmet)
- [ ] Rate limiting implemented
- [ ] Pagination for list endpoints
- [ ] Database integration with Prisma
- [ ] Test coverage >80%
- [ ] API responds within 200ms (p95)

## API Endpoints Summary

```
GET    /users          - List users (paginated)
GET    /users/:id      - Get user by ID
POST   /users          - Create user
PUT    /users/:id      - Replace user
PATCH  /users/:id      - Update user
DELETE /users/:id      - Delete user

GET    /posts          - List posts (paginated)
GET    /posts/:id      - Get post by ID
POST   /posts          - Create post
PUT    /posts/:id      - Replace post
PATCH  /posts/:id      - Update post (publish/unpublish)
DELETE /posts/:id      - Delete post
```

## Future Enhancements

- GraphQL endpoint alternative
- Filtering and sorting query parameters
- Field selection (sparse fieldsets)
- HATEOAS links in responses
- Versioning strategy (URL or header-based)
- Caching with Redis
- Webhooks for async notifications
