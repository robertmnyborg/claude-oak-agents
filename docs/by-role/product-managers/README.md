# Product Manager Guide

**AI-powered product development for semi-technical product managers**

This guide helps you co-author feature specifications, design database schemas, create prototypes, and deliver professional engineering handoffs.

---

## Quick Navigation

### Getting Started
- **[Quick Start Guide](quick-start.md)** - 6 detailed examples with step-by-step walkthroughs
  - Co-author feature specs
  - Design database schemas
  - Create UI prototypes
  - Map user workflows
  - Translate business strategy
  - Manage Git workflows

### Workflow Patterns
- **[PM Workflows](workflows.md)** - 7 reusable workflow patterns
  - Spec-driven feature development
  - Quick iteration and prototyping
  - Database and API design
  - Security-first patterns
  - Data migration workflows
  - Multi-agent coordination
  - Professional handoffs

### Reference
- **[PM Capabilities](capabilities.md)** - Honest assessment of what works today
  - Capability matrix by domain
  - What requires manual work
  - Roadmap for future capabilities
  - Real limitations and workarounds

---

## What You Can Do

### 1. Co-Author Feature Specifications

Work with the **spec-manager** agent to create comprehensive feature specifications:

**Example**:
```
"Help me create a spec for two-factor authentication"
```

**You get**:
- Collaborative spec authoring (section by section)
- Approval checkpoints at each stage
- Markdown for humans + YAML for execution
- Requirements tracking through implementation

**Benefits**:
- Clear requirements and acceptance criteria
- Technical feasibility validation
- Implementation guidance for engineers
- Traceability from spec to code

---

### 2. Design Database Schemas

Use **backend-architect** to design production-ready database schemas:

**Example**:
```
"Design a PostgreSQL schema for a multi-tenant SaaS app"
```

**You get**:
- Normalized schema with proper relationships
- DDL statements for table creation
- Index design for performance
- Migration planning
- API endpoint design (REST/GraphQL)

**Benefits**:
- Professional database design
- Scalability considerations
- Performance optimization
- Clear engineering handoff

---

### 3. Create UI Prototypes

Work with **frontend-developer** to scaffold components and state stores:

**Example**:
```
"Create React components for a shopping cart"
```

**You get**:
- Component structure (React/Vue/Angular)
- State management (Redux/Zustand/Pinia)
- TypeScript type definitions
- Usage examples and integration

**Benefits**:
- Clickable prototypes
- State management patterns
- Type-safe interfaces
- Reusable component libraries

---

### 4. Map User Workflows

**Note**: The ux-designer agent was archived in October 2025. User workflow and UX design are now handled by **product-strategist** and **business-analyst**.

**Example**:
```
"Map the user journey for first-time onboarding"
```

**You get**:
- User journey analysis
- Friction point identification
- Evidence-based recommendations
- Navigation patterns

**Benefits**:
- User-centered design
- Reduced friction in flows
- Intuitive navigation
- Data-driven decisions

---

### 5. Translate Business to Product Strategy

Use **product-strategist** to convert business problems into product opportunities:

**Example**:
```
"We have 15% monthly churn. Frame this as a product opportunity"
```

**You get**:
- Eigenquestion methodology
- Validation hypotheses
- Success metrics definition
- Feature prioritization framework

**Benefits**:
- Clear problem framing
- Measurable success criteria
- Strategic product decisions
- Business alignment

---

### 6. Manage Git Workflows

Use **git-workflow-manager** for professional engineering handoffs:

**Example**:
```
"Create a PR with the spec, schema, and prototypes"
```

**You get**:
- Feature branch creation
- Professional commit messages
- Complete pull requests
- Changelog generation

**Benefits**:
- Clean Git history
- Complete context for engineers
- Professional handoffs
- Traceability

---

## Common PM Workflows

### Workflow 1: New Feature Development

```
1. Frame the Problem
   "Customer churn at 15%. Frame as product opportunity"
   → product-strategist: Eigenquestions + hypotheses + metrics

2. Create Specification
   "Create spec for retention improvement feature"
   → spec-manager: Co-author with approval checkpoints

3. Design Database
   "Design schema for user engagement tracking"
   → backend-architect: Schema + migrations + indexes

4. Prototype UI
   "Create components for engagement dashboard"
   → frontend-developer: Components + state + types

5. Engineering Handoff
   "Create PR with complete context"
   → git-workflow-manager: Professional PR ready for review
```

---

### Workflow 2: Quick Iteration and Prototyping

```
1. Rapid Prototype
   "Quick prototype of onboarding wizard (3 steps)"
   → frontend-developer: Basic components

2. Test with Stakeholders
   [Manual: Show prototype, gather feedback]

3. Iterate
   "Update step 2 to include progress indicator"
   → frontend-developer: Enhanced version

4. Finalize
   "Add state management and validation"
   → frontend-developer: Production-ready components
```

---

### Workflow 3: Database and API Design

```
1. Design Schema
   "Design PostgreSQL schema for task management"
   → backend-architect: Tables + relationships + indexes

2. Define APIs
   "Design REST API for tasks (CRUD + filtering)"
   → backend-architect: OpenAPI spec + endpoints

3. Review Performance
   "Optimize for 100k+ tasks per user"
   → backend-architect: Indexing strategy + query optimization

4. Migration Plan
   "Create migration from existing system"
   → backend-architect: Migration scripts + rollback plan
```

---

## Your PM Agents

### Core PM Agents

**spec-manager**
- Collaborative specification writing
- Approval checkpoints
- Markdown + YAML output
- Implementation tracking

**product-strategist**
- Eigenquestion methodology
- Success metrics definition
- Validation hypotheses
- Feature prioritization

**backend-architect**
- Database schema design
- API design (REST/GraphQL)
- Performance optimization
- Migration planning

**frontend-developer**
- Component scaffolding
- State management (Redux/Zustand/Pinia)
- TypeScript support
- UI prototyping

**git-workflow-manager**
- Git operations
- Branch management
- Pull request creation
- Changelog generation

**business-analyst**
- Requirements analysis
- User workflows (replaces ux-designer)
- Stakeholder communication
- Evidence synthesis

---

## Learning Path

### Week 1: Foundations
1. Complete [Quick Start Guide](quick-start.md) - Try all 6 examples
2. Create your first real spec with spec-manager
3. Design a simple database schema with backend-architect

### Week 2: Workflows
1. Study [PM Workflows](workflows.md) - Understand all 7 patterns
2. Practice quick iteration workflow
3. Create a complete feature handoff (spec → schema → prototype → PR)

### Week 3: Advanced
1. Review [PM Capabilities](capabilities.md) - Understand limitations
2. Practice multi-agent coordination workflows
3. Experiment with product-strategist for strategic framing

### Week 4: Mastery
1. Create a complex feature end-to-end
2. Coordinate multiple agents in parallel
3. Deliver production-ready engineering handoff

---

## Tips for Success

### 1. Use Spec-Driven Development

For significant features:
- Start with spec-manager (co-author the spec)
- Get approval on design before implementation
- Use spec as single source of truth
- Update spec in "spec terms" not "code terms"

### 2. Embrace Iteration

Don't aim for perfection on first pass:
- Quick prototype → gather feedback → iterate
- Use "quick iteration" workflow for experiments
- Finalize only when validated

### 3. Leverage Multi-Agent Coordination

Complex features benefit from multiple agents:
- product-strategist (frame problem)
- spec-manager (document solution)
- backend-architect (design data layer)
- frontend-developer (prototype UI)
- git-workflow-manager (create handoff)

### 4. Understand What's Automatic

The system handles:
- Agent selection based on request
- Quality gates and validation
- Security checks
- Test creation
- Git operations

You focus on:
- Business requirements
- Design decisions
- User needs
- Success criteria

### 5. Know the Limitations

See [PM Capabilities](capabilities.md) for honest assessment of:
- What works today
- What requires manual work
- What's on the roadmap
- Real-world workarounds

---

## Common Questions

### Do I need to be technical?

Semi-technical helps but isn't required:
- **Helpful**: Understanding basic database concepts, REST APIs, state management
- **Not required**: Writing code, debugging, deployment
- **System handles**: Implementation details, quality gates, testing

### How long does a typical workflow take?

**Quick prototype**: 10-20 minutes
**Database schema**: 15-30 minutes
**Feature spec**: 30-60 minutes (with your input)
**Complete handoff**: 60-90 minutes (problem → engineering-ready)

### Can I skip the spec for small features?

Yes, use quick iteration workflow:
- Simple prototypes don't need formal specs
- Bug fixes don't need specs
- Experiments benefit from fast iteration
- Reserve specs for significant features

### What if I need to change the spec mid-implementation?

Update in "spec terms":
```
"Spec section 2.3 (Auth Strategy) needs update.
Current: JWT. Proposed: OAuth2.
This affects sections [2.3, 3.1.task-2].
Approve?"
```

The system:
- Updates Markdown spec
- Regenerates YAML
- Continues with new approach

### How do I know which agent to use?

You don't need to:
- Describe what you want in natural language
- System automatically selects agents
- You can explicitly request if preferred

---

## Example: Complete Feature Development

### Feature: User Authentication

**Phase 1: Frame the Problem** (5 minutes)
```
"We need user authentication. Frame the technical requirements"
→ product-strategist
```

**Phase 2: Create Specification** (30 minutes)
```
"Create spec for OAuth2 authentication"
→ spec-manager (co-author with approval checkpoints)
```

**Phase 3: Design Database** (15 minutes)
```
"Design PostgreSQL schema for OAuth2 (users, tokens, sessions)"
→ backend-architect
```

**Phase 4: Prototype UI** (20 minutes)
```
"Create React login/registration components with OAuth2 flow"
→ frontend-developer
```

**Phase 5: Engineering Handoff** (10 minutes)
```
"Create PR with spec, schema, and components"
→ git-workflow-manager
```

**Total time**: ~80 minutes for complete feature handoff

---

## Next Steps

**Try an example**: Start with [Quick Start Guide](quick-start.md)

**Learn patterns**: Study [PM Workflows](workflows.md)

**Understand capabilities**: Review [PM Capabilities](capabilities.md)

**Get help**: See [Main Documentation Hub](../../INDEX.md)

---

**Ready to start?** Open Claude Code and try your first workflow!
