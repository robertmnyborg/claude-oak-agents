# PM Capabilities Matrix

**Honest Assessment of What Works Today**

This document provides a transparent view of what Claude OaK Agents can actually do for product managers right now - no vaporware, no roadmap promises. Only verified, production-ready capabilities.

## Quick Reference

| Capability | Status | Agent | Example Use Case | Time Investment |
|---|---|---|---|---|
| Co-author feature specs | ✅ Full | spec-manager | "Help me create a spec for user authentication" | 10-20 min |
| Database schema design | ✅ Full | backend-architect | "Design a PostgreSQL schema for multi-tenant SaaS" | 15-30 min |
| State store creation | ✅ Full | frontend-developer | "Create a Redux store for shopping cart state" | 5-15 min |
| Component scaffolding | ✅ Full | frontend-developer | "Scaffold a React component library for our design system" | 10-30 min |
| UX workflow design | ✅ Full | ux-designer | "Map the user journey for onboarding flow" | 15-30 min |
| Product strategy framing | ✅ Full | product-strategist | "Frame eigenquestions for our growth strategy" | 20-40 min |
| Git/PR workflow | ✅ Full | git-workflow-manager | "Create a PR with the authentication spec" | 5-10 min |
| API design | ✅ Full | backend-architect | "Design REST endpoints for user management" | 15-30 min |
| Design system import | ⚠️ Manual | frontend-developer | "Create components from Figma designs" | Manual work required |
| Live DB queries | ⚠️ Limited | backend-architect | "Query production database for user stats" | Schema design only |

## Capability Definitions

### ✅ Full Support
**What it means**: Agent can complete the task autonomously with minimal guidance. You provide requirements, agent delivers working output.

**What to expect**:
- High-quality output that matches professional standards
- Iterative refinement available through conversation
- Output ready for handoff to engineering or implementation
- Clear documentation of decisions and trade-offs

**PM effort**: 10-40 minutes for most tasks (specification + review)

### ⚠️ Manual Work Required
**What it means**: Agent can assist and accelerate the work, but cannot complete it autonomously. Human work is required.

**What to expect**:
- Agent provides templates, guidance, and structure
- Manual steps required (e.g., design file import, database credentials)
- Agent can help with portions of the task
- Significant time savings vs doing it from scratch, but not fully automated

**PM effort**: Variable - depends on complexity and manual steps

### ⚠️ Limited Support
**What it means**: Agent has constraints that limit full capability. Works well within defined boundaries.

**What to expect**:
- Agent can help with specific aspects of the task
- Clear boundaries on what's supported vs not supported
- Workarounds may be available for some limitations
- Better than nothing, but not a complete solution

**PM effort**: Variable - depends on what's within scope

### ❌ Not Supported
**What it means**: Agent cannot help with this task. Either outside scope or technically not feasible.

**Why we're honest**: We'd rather tell you upfront what doesn't work than waste your time discovering it.

## Detailed Capability Breakdown

### 1. Co-Author Feature Specs (✅ Full Support)

**Agent**: spec-manager

**What you can do**:
- Collaboratively write comprehensive feature specifications
- Section-by-section approval workflow (Goals → Design → Plan → Tests)
- Generate machine-readable YAML for agent execution
- Track changes in "spec terms" not "code terms"
- Version control for specifications
- Link specs to implementation telemetry

**Real example**:
```
PM: "Help me create a spec for OAuth2 authentication"

spec-manager: "Great! This is a significant feature. Let's create a spec 
together. We'll go section by section with approval checkpoints.

Section 1: Goals & Requirements
- What are we trying to achieve?
- Who are the users?
- What are the acceptance criteria?

Let's start with user stories..."

[15 minutes of collaborative spec writing]

spec-manager: "Spec complete! Saved to:
- specs/active/2025-10-24-oauth2-authentication.md (human-readable)
- specs/active/2025-10-24-oauth2-authentication.yaml (agent-executable)

Ready to implement or want to review?"
```

**Why it's full support**: spec-manager guides you through the entire process, handles formatting, generates YAML, tracks changes, and maintains spec throughout implementation.

**Time investment**: 10-20 minutes for typical features, 30-40 minutes for complex features

**Output quality**: Production-ready specifications suitable for handoff to engineering teams

### 2. Database Schema Design (✅ Full Support)

**Agent**: backend-architect

**What you can do**:
- Design normalized schemas for PostgreSQL, MySQL, MongoDB
- Generate DDL (Data Definition Language) statements
- Plan database migrations
- Design indexes for query performance
- Establish relationships and constraints
- Plan for scalability (partitioning, sharding strategies)

**Real example**:
```
PM: "Design a PostgreSQL schema for a multi-tenant SaaS application with 
users, organizations, and permissions"

backend-architect: [Designs schema with:]
- Normalized tables with proper relationships
- Tenant isolation strategy (schema-per-tenant vs row-level)
- Permission system (RBAC)
- Indexes for common queries
- Migration scripts
- Performance considerations

[Delivers: SQL DDL, ER diagram description, migration plan]
```

**Why it's full support**: backend-architect has deep expertise in database design patterns, can generate working DDL, and provides complete migration plans ready for implementation.

**Time investment**: 15-30 minutes for typical schemas, up to 60 minutes for complex multi-tenant systems

**Output quality**: Production-ready DDL and migration scripts suitable for immediate implementation

**Limitations**: Cannot connect to live databases for analysis. Schema design only, not data migration or backfill scripts.

### 3. State Store Creation (✅ Full Support)

**Agent**: frontend-developer

**What you can do**:
- Create Redux Toolkit state slices
- Design Zustand stores
- Build Pinia stores (Vue)
- Configure NgRx (Angular)
- Generate TypeScript types
- Write selectors and actions
- Provide usage examples

**Real example**:
```
PM: "Create a Redux store for shopping cart state with add/remove items, 
quantity updates, and total calculation"

frontend-developer: [Creates:]
- Redux Toolkit slice with actions (addItem, removeItem, updateQuantity)
- Selectors (selectCartItems, selectCartTotal, selectItemCount)
- TypeScript types (CartItem, CartState)
- Usage examples in React components
- Immer integration for immutable updates

[Delivers: Complete state management implementation]
```

**Why it's full support**: frontend-developer knows all major state management libraries, can generate idiomatic code for each, includes TypeScript types, and provides working examples.

**Time investment**: 5-15 minutes for simple stores, 15-30 minutes for complex state with async logic

**Output quality**: Production-ready state management code following framework best practices

### 4. Component Scaffolding (✅ Full Support)

**Agent**: frontend-developer

**What you can do**:
- Scaffold React components (functional, hooks-based)
- Create Vue 3 components (Composition API)
- Build Angular components
- Generate component libraries
- Include TypeScript types
- Add prop validation
- Provide usage documentation

**Real example**:
```
PM: "Scaffold a reusable Button component in React with variants (primary, 
secondary, danger) and sizes (small, medium, large)"

frontend-developer: [Creates:]
- TypeScript component with props interface
- Variant and size styling logic
- Accessibility attributes (ARIA labels, keyboard navigation)
- Storybook stories for visual testing
- Usage examples
- Compound components (Button.Icon, Button.Text if needed)

[Delivers: Complete component with documentation]
```

**Why it's full support**: frontend-developer can generate complete, accessible, production-ready components with proper TypeScript types and documentation.

**Time investment**: 10-30 minutes depending on component complexity

**Output quality**: Production-ready components following accessibility standards and framework best practices

**Note on design systems**: Can scaffold components based on text descriptions. For importing from Figma, see "Design System Import" section below.

### 5. UX Workflow Design (✅ Full Support)

**Agent**: ux-designer

**What you can do**:
- Map complete user journeys from entry to goal
- Identify friction points and drop-off risks
- Design information architecture
- Create navigation flows
- Apply evidence-based UX principles (Jakob's Law, Fitts's Law, etc.)
- Recommend interaction patterns
- Plan progressive disclosure strategies

**Real example**:
```
PM: "Map the user journey for a new user onboarding flow. We want to 
collect email, preferences, and connect their calendar"

ux-designer: [Analyzes and designs:]
1. Journey stages:
   - Entry point (signup completion)
   - Information collection (minimize cognitive load)
   - Integration setup (progressive disclosure)
   - Success confirmation

2. Friction analysis:
   - Calendar connection should be optional (reduce abandonment)
   - Preferences can be inferred from usage (skip upfront)
   - Email is collected at signup (don't ask twice)

3. Recommended flow:
   - Step 1: Welcome + value proposition (30 seconds)
   - Step 2: Critical setup only (calendar - optional)
   - Step 3: Success state + next actions
   - Defer preferences to usage patterns

4. UX principles applied:
   - Hick's Law: Reduce choices at each step
   - Miller's Law: 3-step flow fits working memory
   - Jakob's Law: Use familiar calendar integration pattern

[Delivers: Flow diagram, friction analysis, recommendations]
```

**Why it's full support**: ux-designer applies established UX frameworks, identifies real friction points, and provides actionable recommendations grounded in evidence-based principles.

**Time investment**: 15-30 minutes for typical flows, 40-60 minutes for complex multi-path journeys

**Output quality**: Professional UX analysis suitable for design handoff or validation with user research

### 6. Product Strategy Framing (✅ Full Support)

**Agent**: product-strategist

**What you can do**:
- Frame eigenquestions (the most important questions to answer)
- Translate business problems into product opportunities
- Define validation hypotheses
- Establish success metrics
- Prioritize features based on strategic impact
- Design product experiments

**Real example**:
```
PM: "We need to grow revenue by 25% next year. Help me figure out where 
to focus product development"

product-strategist: [Applies eigenquestion framework:]

Step 1: What's the eigenquestion?
"Is our revenue constraint acquisition (getting more customers) or 
monetization (extracting more value from existing customers)?"

Why this is the eigenquestion:
- Answer determines entirely different product strategies
- Acquisition → invest in virality, onboarding, free tier
- Monetization → invest in premium features, usage tiers, upsells
- One question collapses the decision space

Step 2: How do we answer it?
Data analysis:
- Acquisition cost vs LTV ratio
- Conversion rate from free to paid
- Feature adoption by tier
- Churn rate by segment

Hypothesis:
"If CAC < 0.3 * LTV, we have a monetization problem.
If CAC > 0.5 * LTV, we have an acquisition problem."

Step 3: Next steps based on answer:
[Specific product initiatives for each scenario]

[Delivers: Eigenquestion, validation approach, strategic options]
```

**Why it's full support**: product-strategist applies proven eigenquestion methodology, connects business goals to product decisions, and provides clear decision frameworks.

**Time investment**: 20-40 minutes for strategic framing, longer for detailed analysis

**Output quality**: Strategic frameworks suitable for executive presentations and product roadmap planning

### 7. Git/PR Workflow (✅ Full Support)

**Agent**: git-workflow-manager

**What you can do**:
- Fork production repositories
- Create feature branches with conventional naming
- Stage and commit changes with clear messages
- Generate changelogs automatically
- Create pull requests with complete context
- Link PRs to specifications
- Professional handoffs to engineering

**Real example**:
```
PM: "Create a PR with the authentication spec and database schema we designed"

git-workflow-manager:
1. Created feature branch: feature/oauth2-authentication
2. Staged files:
   - specs/active/2025-10-24-oauth2-authentication.md
   - specs/active/2025-10-24-oauth2-authentication.yaml
   - db/migrations/001_auth_schema.sql
3. Committed with message:
   "Add OAuth2 authentication specification and schema
   
   - Complete feature spec with acceptance criteria
   - PostgreSQL schema for users, sessions, tokens
   - Migration script ready for implementation
   
   Co-Authored-By: Claude <noreply@anthropic.com>"
4. Created PR:
   Title: "Feature: OAuth2 Authentication Specification"
   Body: [Spec summary, implementation checklist, testing plan]

[Delivers: Professional PR ready for engineering review]
```

**Why it's full support**: git-workflow-manager handles all git operations, follows conventional commit standards, generates clear changelogs, and creates comprehensive PRs.

**Time investment**: 5-10 minutes for PR creation

**Output quality**: Professional PRs with clear context suitable for engineering team review

### 8. API Design (✅ Full Support)

**Agent**: backend-architect

**What you can do**:
- Design RESTful API endpoints
- Create GraphQL schemas
- Define request/response formats
- Plan API versioning strategy
- Generate OpenAPI/Swagger documentation
- Design authentication flows
- Plan rate limiting and pagination

**Real example**:
```
PM: "Design REST API endpoints for user management - CRUD operations plus 
password reset and email verification"

backend-architect: [Designs API:]

Endpoints:
- POST   /api/v1/users          (Create user)
- GET    /api/v1/users/:id      (Get user by ID)
- PUT    /api/v1/users/:id      (Update user)
- DELETE /api/v1/users/:id      (Delete user)
- POST   /api/v1/users/password-reset       (Request reset)
- POST   /api/v1/users/password-reset/:token (Confirm reset)
- POST   /api/v1/users/verify-email/:token  (Verify email)

Request/Response formats: [JSON schemas]
Error responses: [Standardized error format]
Authentication: Bearer token (JWT)
Rate limiting: 100 req/hour for password reset
Versioning strategy: URL-based (/api/v1/)

[Delivers: OpenAPI spec, authentication docs, error handling]
```

**Why it's full support**: backend-architect designs complete REST/GraphQL APIs following industry standards, generates OpenAPI docs, and includes security considerations.

**Time investment**: 15-30 minutes for typical CRUD APIs, longer for complex microservices

**Output quality**: Production-ready API specifications suitable for implementation

### 9. Design System Import (⚠️ Manual Work Required)

**Agent**: frontend-developer

**What you can do**:
- Create components from text descriptions
- Scaffold component structure
- Implement design tokens (colors, spacing, typography) from specifications
- Build component libraries

**What requires manual work**:
- Importing Figma designs (no Figma API automation)
- Extracting exact spacing/colors from visual designs
- Translating visual mockups to components

**Why manual**: Figma API integration is not implemented. You must manually extract design specifications from Figma and provide them as text/structured data.

**Workaround**:
1. Export design tokens from Figma (manually or via Figma plugin)
2. Provide design specs as structured data to frontend-developer
3. Agent scaffolds components based on specs
4. Manual refinement to match pixel-perfect designs

**Real example**:
```
PM: "Create a Button component from our Figma design system"

[Manual step: Export design specs from Figma]
- Primary color: #0066CC
- Border radius: 8px
- Padding: 12px 24px
- Font: Inter, 16px, 600 weight
- States: default, hover, active, disabled

PM provides specs to frontend-developer:
"Create a Button component with these design tokens: [specs above]"

frontend-developer: [Creates component based on specifications]
```

**Time investment**: Manual extraction + 15-30 minutes for component creation

**Why not full support**: Requires manual design file parsing. Agent cannot directly access Figma.

### 10. Live Database Queries (⚠️ Limited Support)

**Agent**: backend-architect

**What you can do**:
- Design database schemas
- Write query logic
- Optimize query performance
- Plan indexes

**What's limited**:
- Cannot connect to production databases (security risk)
- Cannot execute queries against live data
- Cannot analyze existing data or tables

**Why limited**: Security and access control. Providing database credentials to AI agents is not recommended.

**Workaround**:
1. Use backend-architect to design queries
2. Manually execute queries in safe environment
3. Share query results (anonymized) if analysis needed

**Real example**:
```
PM: "Write a query to find users who haven't logged in for 90 days"

backend-architect: [Writes query:]
SELECT u.id, u.email, u.last_login_at
FROM users u
WHERE u.last_login_at < NOW() - INTERVAL '90 days'
  AND u.account_status = 'active'
ORDER BY u.last_login_at ASC;

[You manually execute in safe environment]
```

**Why not full support**: Database credentials and production data access create security risks. Agent provides query logic, human executes safely.

## What This Means for PMs

### When to Use Each Capability Level

**✅ Full Support - Use Confidently**:
- Delegate the entire task to the agent
- Expect production-quality output
- Plan for 10-40 minutes total time (most tasks)
- Review output but minimal revision needed
- Ready for handoff to engineering

**⚠️ Manual/Limited - Plan for Human Work**:
- Agent accelerates but doesn't complete the task
- Expect to do manual steps or workarounds
- Time savings vs from-scratch, but not fully automated
- Use agent for structure/templates, human for details
- Still valuable, just not autonomous

### How to Evaluate New Capabilities

When a new agent or capability is added, ask:

1. **Can I delegate the entire task?** → Full Support candidate
2. **Do I need to provide manual input/credentials?** → Manual/Limited
3. **Can the agent complete 80%+ autonomously?** → Full Support
4. **Does it require human judgment calls?** → Limited Support

### Why We're Honest About Limitations

**Philosophy**: Better to be upfront about what works vs what doesn't than to waste your time discovering limitations through trial and error.

**Trust**: By clearly stating what's manual/limited, you can plan appropriately and avoid frustration.

**Continuous improvement**: We track capability gaps and prioritize based on PM feedback. If a manual/limited capability is blocking your workflow, let us know.

## Capability Roadmap

We're honest about current capabilities AND transparent about what's coming:

### Near-term (Next 3 months)
- **Figma API Integration** - Automate design system import
- **Database read-only queries** - Safe production data analysis
- **Competitive analysis** - Product research agent
- **User research synthesis** - Interview analysis agent

### Medium-term (3-6 months)
- **A/B test design** - Experiment planning agent
- **Product analytics** - Metrics and KPI agent
- **Customer feedback analysis** - Support ticket synthesis
- **Go-to-market strategy** - Launch planning agent

### Long-term (6+ months)
- **Live prototype generation** - Interactive mockups
- **Multi-modal design** - Image-based component creation
- **Automated user testing** - Synthetic user feedback
- **Predictive roadmapping** - ML-driven prioritization

**Note**: These are aspirational. We'll update this document as capabilities move from roadmap to production-ready.

## Feedback and Capability Requests

We want to build capabilities that actually help PMs. If you:

- **Hit a limitation** - tell us what blocked you
- **Need a new capability** - describe your workflow
- **Have a workaround** - share what worked for you
- **Found something broken** - report the issue

**Where to provide feedback**:
- **GitHub Discussions**: [Community forum](https://github.com/robertmnyborg/claude-oak-agents/discussions)
- **GitHub Issues**: [Bug reports and feature requests](https://github.com/robertmnyborg/claude-oak-agents/issues)

We prioritize capability development based on:
1. **PM impact** - how much time it saves or quality it improves
2. **Frequency** - how often it's needed
3. **Feasibility** - technical complexity and timeline

## Summary

**What works today** (Full Support):
- Co-author specs
- Database schema design
- State store creation
- Component scaffolding
- UX workflow design
- Product strategy framing
- Git/PR workflow
- API design

**What needs manual work**:
- Design system import from Figma
- Live database queries

**Why we're transparent**: So you can confidently delegate to agents and plan for manual work where needed. No surprises, no wasted time.

**How to get started**: Pick a Full Support capability and try it. See [PM Quick Start Guide](PM_QUICK_START.md) for detailed examples.
