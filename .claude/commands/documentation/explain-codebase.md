# Explain Codebase

Generate a comprehensive overview of the codebase including architecture, key components, and workflows.

## Usage
/explain-codebase [--depth surface|detailed|deep] [--focus architecture|components|workflows]

## What This Does
1. Analyzes project structure and file organization
2. Identifies key architectural patterns
3. Maps relationships between components
4. Documents entry points and main workflows
5. Generates dependency graph
6. Creates navigable codebase overview

## Example
/explain-codebase --depth detailed --focus architecture

## Agent Coordination
1. **systems-architect**: High-level architecture analysis
   - Identifies architectural patterns (MVC, microservices, etc.)
   - Maps system boundaries and modules
   - Documents technology stack
2. **backend-architect** OR **frontend-developer**: Component analysis
   - Identifies key components and their responsibilities
   - Maps data flow and dependencies
   - Documents API contracts
3. **technical-writer**: Formats comprehensive overview
   - Creates navigable documentation structure
   - Ensures clarity for different audiences
   - Generates diagrams and visualizations
4. **Main LLM**: Synthesizes analysis into cohesive overview

## Output
Codebase Overview:
```markdown
## Codebase Overview: Project Name

### Quick Stats
- **Language**: TypeScript (85%), JavaScript (10%), CSS (5%)
- **Framework**: React 18 + Express.js
- **Architecture**: Client-server with REST API
- **Lines of Code**: ~45,000
- **Files**: 342 source files
- **Dependencies**: 156 packages

### Architecture Overview

**Pattern**: Layered Architecture (Frontend + Backend)

```
┌─────────────────────────────────────┐
│         Frontend (React)            │
│  - Components (src/components/)     │
│  - State Management (Redux)         │
│  - API Client (src/api/)            │
└──────────────┬──────────────────────┘
               │ HTTP/REST
┌──────────────▼──────────────────────┐
│         Backend (Express)           │
│  - API Routes (src/api/)            │
│  - Business Logic (src/services/)   │
│  - Data Access (src/repositories/)  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Data Layer (PostgreSQL + Redis)  │
│  - User data, sessions, cache       │
└─────────────────────────────────────┘
```

### Technology Stack

**Frontend**:
- React 18.2.0 - UI framework
- Redux Toolkit 1.9.0 - State management
- React Router 6.8.0 - Routing
- Axios 1.3.0 - HTTP client
- Tailwind CSS 3.2.0 - Styling

**Backend**:
- Express.js 4.18.0 - Web framework
- TypeScript 5.0.0 - Type safety
- Prisma 4.10.0 - ORM
- jsonwebtoken 9.0.0 - Authentication
- winston 3.8.0 - Logging

**Infrastructure**:
- PostgreSQL 14 - Primary database
- Redis 6 - Caching and sessions
- Docker - Containerization
- nginx - Reverse proxy

### Directory Structure

```
project/
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── auth/       # Authentication UI
│   │   │   ├── dashboard/  # Dashboard views
│   │   │   └── common/     # Shared components
│   │   ├── store/          # Redux store configuration
│   │   │   ├── slices/     # Redux slices
│   │   │   └── middleware/ # Custom middleware
│   │   ├── api/            # API client layer
│   │   ├── hooks/          # Custom React hooks
│   │   ├── utils/          # Utility functions
│   │   └── App.tsx         # Root component
│   └── public/             # Static assets
├── backend/
│   ├── src/
│   │   ├── api/            # API route handlers
│   │   │   ├── auth.ts     # Authentication routes
│   │   │   ├── users.ts    # User management
│   │   │   └── data.ts     # Data endpoints
│   │   ├── services/       # Business logic layer
│   │   ├── repositories/   # Data access layer
│   │   ├── middleware/     # Express middleware
│   │   ├── models/         # Data models (Prisma)
│   │   └── server.ts       # Server entry point
│   └── prisma/             # Database schema
└── shared/                 # Shared code (types, utils)

```

### Key Components

#### Frontend Components

**1. Authentication System** (`src/components/auth/`)
- **LoginForm**: Handles user login with email/password
- **RegisterForm**: User registration flow
- **ProtectedRoute**: Route guard for authenticated pages
- **AuthContext**: Manages authentication state globally

**2. Dashboard** (`src/components/dashboard/`)
- **DashboardLayout**: Main layout wrapper
- **UserProfile**: User profile display and editing
- **DataTable**: Generic data display component
- **Charts**: Data visualization components

**3. State Management** (`src/store/`)
- **authSlice**: Authentication state (user, token, status)
- **dataSlice**: Application data state
- **uiSlice**: UI state (modals, notifications, etc.)

#### Backend Components

**1. API Layer** (`src/api/`)
- **auth.ts**: POST /auth/login, POST /auth/register, POST /auth/logout
- **users.ts**: CRUD operations for users
- **data.ts**: Data retrieval and manipulation endpoints

**2. Services Layer** (`src/services/`)
- **AuthService**: Authentication business logic
- **UserService**: User management operations
- **DataService**: Data processing logic

**3. Repository Layer** (`src/repositories/`)
- **UserRepository**: Database operations for users
- **SessionRepository**: Session management
- **DataRepository**: Data access operations

### Main Workflows

#### User Authentication Flow

```
1. User submits login form
   ↓
2. Frontend: LoginForm → authSlice.login() action
   ↓
3. API call: POST /auth/login (email, password)
   ↓
4. Backend: auth.ts → AuthService.login()
   ↓
5. Service: Validate credentials via UserRepository
   ↓
6. Generate JWT token with jsonwebtoken
   ↓
7. Store session in Redis (1 hour expiration)
   ↓
8. Return: { user, token, expires_at }
   ↓
9. Frontend: Store token in Redux + localStorage
   ↓
10. Redirect to dashboard
```

#### Data Retrieval Flow

```
1. Component needs data
   ↓
2. useEffect hook triggers
   ↓
3. Dispatch dataSlice.fetchData() action
   ↓
4. API call: GET /data with authentication header
   ↓
5. Backend: middleware/auth.ts validates JWT
   ↓
6. Route handler: data.ts → DataService.getData()
   ↓
7. Service: DataRepository.findAll() via Prisma
   ↓
8. Database query to PostgreSQL
   ↓
9. Transform data if needed
   ↓
10. Cache in Redis (5 min TTL)
    ↓
11. Return data to frontend
    ↓
12. Frontend: Update Redux store
    ↓
13. Components re-render with new data
```

### Entry Points

**Frontend**:
- `frontend/src/index.tsx` - Application bootstrap
- `frontend/src/App.tsx` - Root component, routing setup

**Backend**:
- `backend/src/server.ts` - Express server initialization
- `backend/src/api/index.ts` - API routes registration

### Dependency Graph

**Frontend Dependencies**:
```
App.tsx
  ├── AuthProvider (Context)
  ├── Redux Store
  │   ├── authSlice
  │   ├── dataSlice
  │   └── uiSlice
  ├── Router
  │   ├── Public Routes (Login, Register)
  │   └── Protected Routes (Dashboard, Profile)
  └── API Client (Axios instance)
```

**Backend Dependencies**:
```
server.ts
  ├── Express app
  ├── Middleware
  │   ├── auth.ts (JWT validation)
  │   ├── error.ts (Error handling)
  │   └── logger.ts (Request logging)
  ├── Routes
  │   ├── /auth → Services → Repositories
  │   ├── /users → Services → Repositories
  │   └── /data → Services → Repositories
  └── Database (Prisma → PostgreSQL)
```

### API Endpoints Reference

**Authentication**:
- `POST /auth/register` - Create new user account
- `POST /auth/login` - Authenticate user, get JWT
- `POST /auth/logout` - Invalidate session
- `POST /auth/refresh` - Refresh JWT token

**Users**:
- `GET /users/:id` - Get user by ID
- `PUT /users/:id` - Update user profile
- `DELETE /users/:id` - Delete user account

**Data**:
- `GET /data` - Retrieve data (paginated)
- `POST /data` - Create new data entry
- `PUT /data/:id` - Update data entry
- `DELETE /data/:id` - Delete data entry

### Configuration

**Environment Variables**:
```bash
# Database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=myapp
DATABASE_USER=postgres
DATABASE_PASSWORD=secret

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Auth
JWT_SECRET=your-secret-key
JWT_EXPIRATION=1h

# Server
PORT=3000
NODE_ENV=development
```

### Getting Started

**For New Developers**:
1. Start with `README.md` for setup instructions
2. Review architecture diagram (above)
3. Explore `frontend/src/App.tsx` for UI entry point
4. Explore `backend/src/server.ts` for API entry point
5. Check `docs/` for additional documentation

**Common Tasks**:
- Add new API endpoint: Create route in `backend/src/api/`
- Add new UI component: Create in `frontend/src/components/`
- Modify database schema: Update `backend/prisma/schema.prisma`
- Add new Redux state: Create slice in `frontend/src/store/slices/`

### Additional Resources

- **API Documentation**: `docs/api/README.md`
- **Component Library**: `docs/components/README.md`
- **Database Schema**: `docs/database/schema.md`
- **Deployment Guide**: `docs/deployment/README.md`
```

This provides a comprehensive, navigable overview of the codebase for developers at any level.
