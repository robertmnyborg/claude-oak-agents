# Feature Development Guide

**End-to-end feature development workflows using claude-oak-agents**

This guide covers common feature development patterns from ideation to production deployment.

---

## Quick Navigation

- **[Workflow Patterns](workflow-patterns.md)** - Common development patterns and workflows
- **[Spec-Driven Development](#spec-driven-workflow)** - Specification-first approach
- **[Quick Iteration](#quick-iteration-workflow)** - Rapid prototyping and experimentation

---

## Feature Development Workflows

### 1. Spec-Driven Workflow

**Best for**: Significant features, multi-agent coordination, security-critical changes

**Process**:
```
1. Frame Problem → product-strategist
   "Customer churn 15%. Frame as product opportunity"

2. Create Specification → spec-manager
   "Create spec for retention improvement feature"
   - Co-author section by section
   - Approve at each checkpoint
   - Generate Markdown + YAML

3. Design Database → backend-architect
   "Design schema for engagement tracking"
   - Normalized schema
   - DDL statements
   - Indexes and migrations

4. Prototype UI → frontend-developer
   "Create React engagement dashboard"
   - Components + state
   - TypeScript types
   - Usage examples

5. Implement Backend → backend-architect
   "Implement API from spec"
   - Execute from YAML spec
   - Track against requirements
   - Log execution in spec

6. Quality Validation → quality-gate
   - Code review
   - Security check
   - Simplicity analysis
   - Test coverage

7. Engineering Handoff → git-workflow-manager
   "Create PR with spec, schema, components"
   - Complete pull request
   - Changelog generation
   - Professional handoff
```

**Timeline**: 60-120 minutes for complete feature

**Benefits**:
- Clear requirements and design
- Traceability from spec to code
- Quality validation built-in
- Professional handoffs

---

### 2. Quick Iteration Workflow

**Best for**: Experiments, prototypes, simple features, bug fixes

**Process**:
```
1. Quick Prototype
   "Create React onboarding wizard (3 steps)"
   → frontend-developer: Basic components

2. Test and Gather Feedback
   [Manual: Show stakeholders, collect feedback]

3. Iterate Rapidly
   "Add progress indicator to step 2"
   → frontend-developer: Enhanced version

4. Finalize
   "Add state management and validation"
   → frontend-developer: Production-ready

5. Quality Check → quality-gate
   → Automatic validation

6. Commit → git-workflow-manager
   → Professional commit message
```

**Timeline**: 10-30 minutes per iteration

**Benefits**:
- Fast feedback loops
- Minimal overhead
- Flexible experimentation
- Easy to pivot

---

### 3. Database and API Design Workflow

**Best for**: Data layer design, schema changes, API creation

**Process**:
```
1. Design Schema
   "Design PostgreSQL schema for task management"
   → backend-architect
   - Tables + relationships
   - Indexes for performance
   - Migration strategy

2. Define APIs
   "Design REST API for tasks (CRUD + filtering)"
   → backend-architect
   - OpenAPI specification
   - Endpoint definitions
   - Request/response schemas

3. Optimize Performance
   "Optimize for 100k+ tasks per user"
   → backend-architect
   - Query optimization
   - Index strategy
   - Caching approach

4. Plan Migration
   "Create migration from existing system"
   → backend-architect
   - Migration scripts
   - Rollback plan
   - Data validation

5. Implement
   → backend-architect
   - Execute implementation
   - Generate tests

6. Validate → quality-gate
   - Schema review
   - API consistency
   - Performance validation

7. Commit → git-workflow-manager
   - Schema files
   - Migration scripts
   - API documentation
```

**Timeline**: 30-60 minutes

---

### 4. Frontend Component Development

**Best for**: UI components, state management, client-side features

**Process**:
```
1. Design Component Structure
   "Create reusable button component library"
   → frontend-developer
   - Component variants
   - Props interface
   - Styling approach

2. Implement State Management
   "Add global state for user preferences"
   → frontend-developer
   - State store (Redux/Zustand/Pinia)
   - Actions and reducers
   - Selectors

3. Add TypeScript Types
   → frontend-developer
   - Interface definitions
   - Type guards
   - Generic types

4. Create Usage Examples
   → frontend-developer
   - Documentation
   - Code examples
   - Storybook stories

5. Validate → quality-gate
   - Component best practices
   - Accessibility
   - Performance

6. Commit → git-workflow-manager
   - Components
   - Tests
   - Documentation
```

**Timeline**: 20-40 minutes

---

### 5. Backend Service Implementation

**Best for**: Business logic, APIs, data processing

**Process**:
```
1. Design Service Architecture
   "Design notification service"
   → backend-architect
   - Service structure
   - Dependencies
   - Integration points

2. Implement Core Logic
   "Implement notification delivery"
   → backend-architect
   - Business logic
   - Error handling
   - Retry mechanisms

3. Add Database Integration
   "Persist notification history"
   → backend-architect
   - Repository pattern
   - Query optimization
   - Transaction handling

4. Create API Endpoints
   "REST endpoints for notifications"
   → backend-architect
   - Route handlers
   - Validation
   - Documentation

5. Add Tests → unit-test-expert
   - Unit tests
   - Integration tests
   - Mock dependencies

6. Validate → quality-gate
   - Code review
   - Security check
   - Performance

7. Commit → git-workflow-manager
   - Service code
   - Tests
   - Documentation
```

**Timeline**: 45-90 minutes

---

### 6. Infrastructure and Deployment

**Best for**: Cloud resources, deployment automation, infrastructure as code

**Process**:
```
1. Design Infrastructure
   "Design Lambda deployment with CDK"
   → infrastructure-specialist
   - Stack structure
   - Resource definitions
   - IAM policies

2. Implement CDK Stack
   → infrastructure-specialist
   - TypeScript CDK code
   - Environment configuration
   - Resource dependencies

3. Security Review → security-auditor
   - IAM policy validation
   - Network security
   - Encryption at rest

4. Add Monitoring
   "CloudWatch alarms and dashboards"
   → infrastructure-specialist
   - Metrics
   - Alarms
   - Dashboards

5. Validate → quality-gate
   - Infrastructure best practices
   - Security compliance
   - Cost optimization

6. Commit → git-workflow-manager
   - CDK code
   - Configuration
   - Documentation
```

**Timeline**: 30-60 minutes

---

## Workflow Selection Guide

### Use Spec-Driven When:
- Feature is significant (>4 hours development)
- Requires 4+ agents
- Security-critical
- Architecture decisions needed
- Clear requirements essential
- Engineering handoff required

### Use Quick Iteration When:
- Experimenting with ideas
- Building prototypes
- Simple features (<1 hour)
- Bug fixes
- Quick stakeholder feedback needed
- Low risk

### Use Database/API Design When:
- Schema changes required
- API contract design needed
- Performance critical
- Data migration needed
- Integration with multiple services

### Use Component Development When:
- Building UI libraries
- Creating reusable components
- State management setup
- Frontend-only features

### Use Backend Service When:
- Business logic implementation
- API development
- Data processing
- Service integration

### Use Infrastructure When:
- Cloud resource deployment
- IaC development
- Deployment automation
- Monitoring setup

---

## Multi-Agent Coordination

### Parallel Execution

**When to use**: Independent tasks that can run simultaneously

**Example**:
```
"Implement secure API with monitoring"

Parallel agents:
  - security-auditor (security review)
  - backend-architect (API implementation)
  - infrastructure-specialist (monitoring setup)

Main LLM synthesizes results
```

**Benefits**:
- Faster execution
- Independent validation
- Comprehensive coverage

---

### Sequential Execution

**When to use**: Tasks with dependencies

**Example**:
```
"Design and implement authentication"

Sequential flow:
  1. systems-architect (high-level design)
  2. backend-architect (implementation)
  3. security-auditor (security validation)
  4. quality-gate (quality review)
  5. git-workflow-manager (commit)
```

**Benefits**:
- Clear dependencies
- Progressive refinement
- Validation at each stage

---

### Hybrid Planning

**When to use**: Complex, high-risk features

**Example**:
```
"Implement payment processing"

4-Phase workflow:
  Phase 1: Strategic planning
  Phase 2: Implementation planning (parallel)
  Phase 3: Plan review (validation)
  Phase 4: Execution
```

See [Hybrid Planning Guide](../../by-role/architects/hybrid-planning.md)

---

## Quality Gates

### Automatic Validation

Every implementation goes through quality-gate:

**Validation dimensions**:
- Code review and standards
- Maintainability and clarity
- Architectural impact
- Implementation complexity
- KISS principle compliance
- Security and performance

**Blocking behavior**:
- No git operations until validation passes
- Feedback provided for improvements
- Re-validation after fixes

---

### Pre-Commit Hooks

Technical enforcement via git hooks:

```bash
# .git/hooks/pre-commit
if [ ! -f ".workflow_state" ]; then
  echo "❌ Workflow incomplete"
  exit 1
fi

if ! grep -q "QUALITY_GATE_PASSED" .workflow_state; then
  echo "❌ Quality gate not passed"
  exit 1
fi
```

---

## Common Patterns

### Pattern 1: Full-Stack Feature

```
1. Spec → spec-manager
2. Database → backend-architect
3. API → backend-architect
4. Frontend → frontend-developer
5. Integration → qa-specialist
6. Quality → quality-gate
7. Commit → git-workflow-manager
```

---

### Pattern 2: UI-Only Feature

```
1. Components → frontend-developer
2. State → frontend-developer
3. Integration → frontend-developer
4. Quality → quality-gate
5. Commit → git-workflow-manager
```

---

### Pattern 3: Backend-Only Feature

```
1. Service → backend-architect
2. Database → backend-architect
3. Tests → unit-test-expert
4. Quality → quality-gate
5. Commit → git-workflow-manager
```

---

### Pattern 4: Infrastructure-Only

```
1. Design → infrastructure-specialist
2. Security → security-auditor
3. Implementation → infrastructure-specialist
4. Quality → quality-gate
5. Commit → git-workflow-manager
```

---

## Tips for Success

### 1. Choose the Right Workflow

Match workflow to feature complexity:
- Simple → Quick iteration
- Significant → Spec-driven
- Complex/High-risk → Hybrid planning

### 2. Leverage Parallel Execution

When tasks are independent:
- Run agents in parallel
- Faster completion
- Comprehensive validation

### 3. Trust Quality Gates

Quality gates prevent issues:
- Don't skip validation
- Address feedback promptly
- Learn from simplicity recommendations

### 4. Use Specs for Complex Features

Spec-driven development:
- Clear requirements
- Traceable implementation
- Professional handoffs
- Easier maintenance

### 5. Iterate Quickly for Experiments

Don't over-engineer experiments:
- Quick prototypes
- Fast feedback
- Easy pivots
- Formalize when validated

---

## Next Steps

**Learn workflow patterns**: See [Workflow Patterns](workflow-patterns.md)

**PM perspective**: See [PM Workflows](../../by-role/product-managers/workflows.md)

**Engineer perspective**: See [Engineers Guide](../../by-role/engineers/README.md)

**Architecture decisions**: See [Architects Guide](../../by-role/architects/README.md)

---

**Ready to build?** Choose your workflow and start developing!
