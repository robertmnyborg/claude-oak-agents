# PM Workflow Library

**Reusable patterns and templates for common product management workflows**

This library provides proven workflow patterns you can adapt to your specific needs. Each pattern includes when to use it, the workflow steps, agent coordination, and expected outcomes.

For concrete examples with step-by-step walkthroughs, see [PM_QUICK_START.md](PM_QUICK_START.md).

---

## Table of Contents

1. [Spec-Driven Feature Development](#spec-driven-feature-development)
2. [Database Design & API Planning](#database-design--api-planning)
3. [UI Prototyping & State Management](#ui-prototyping--state-management)
4. [User Research & Workflow Mapping](#user-research--workflow-mapping)
5. [Git Workflow & Engineering Handoffs](#git-workflow--engineering-handoffs)
6. [Product Strategy & Metrics Definition](#product-strategy--metrics-definition)
7. [Iterative Design & Feedback Loops](#iterative-design--feedback-loops)

---

## Spec-Driven Feature Development

### When to Use

- **Significant features** requiring clear requirements
- **Cross-functional work** involving multiple teams
- **Architectural decisions** with long-term impact
- **Handoffs to engineering** requiring complete context

### Workflow Pattern

```
1. Initial Framing
   └─> product-strategist: Frame business problem as product opportunity
       └─> eigenquestion methodology
       └─> success metrics definition

2. Specification Co-Authoring
   └─> spec-manager: Collaborative spec writing
       ├─> Section 1: Goals & Requirements (with approval)
       ├─> Section 2: Technical Design (with approval)
       ├─> Section 3: Implementation Plan (with approval)
       └─> Section 4: Test Strategy (with approval)

3. Technical Validation
   ├─> backend-architect: Review technical feasibility
   ├─> security-auditor: Security implications
   └─> systems-architect: Integration points

4. Engineering Handoff
   └─> git-workflow-manager: Create PR with complete spec
       ├─> Spec files (MD + YAML)
       ├─> Context documentation
       └─> Acceptance criteria
```

### Agent Coordination

**Sequential Flow**:
1. product-strategist → defines opportunity
2. spec-manager → co-authors specification
3. Parallel validation (backend-architect + security-auditor + systems-architect)
4. git-workflow-manager → creates handoff PR

### Template Prompts

**Initial Framing**:
```
"Help me frame [business problem] as a product opportunity with success metrics and validation hypotheses"
```

**Spec Creation**:
```
"Create a spec for [feature name] that solves [user problem] with [key requirements]"
```

**Technical Validation**:
```
"Review the [feature name] spec for technical feasibility, security concerns, and integration complexity"
```

**Engineering Handoff**:
```
"Create a PR with the [feature name] spec, documentation, and acceptance criteria for engineering review"
```

### Expected Outcomes

- ✅ Complete feature specification (Markdown + YAML)
- ✅ Validated technical approach
- ✅ Clear success metrics
- ✅ Engineering-ready PR with context
- ⏱️ Timeline: 30-60 minutes for spec + validation

### Success Criteria

- [ ] All spec sections approved
- [ ] Technical feasibility confirmed
- [ ] Security review completed
- [ ] Acceptance criteria defined
- [ ] Engineering team acknowledged PR

---

## Database Design & API Planning

### When to Use

- **New data models** for features
- **Schema changes** to existing tables
- **API endpoint design** for frontend/backend integration
- **Data migrations** requiring careful planning

### Workflow Pattern

```
1. Requirements Analysis
   └─> business-analyst: Extract data requirements from user stories
       └─> entities, relationships, constraints

2. Schema Design
   └─> backend-architect: Design normalized schema
       ├─> Tables with relationships
       ├─> Indexes for performance
       ├─> Constraints and validation
       └─> Migration strategy

3. API Design
   └─> backend-architect: Define REST/GraphQL endpoints
       ├─> Request/response formats
       ├─> Authentication/authorization
       ├─> Error handling
       └─> Rate limiting

4. Documentation & Validation
   ├─> technical-documentation-writer: API documentation
   └─> security-auditor: Data security review
```

### Agent Coordination

**Sequential Flow**:
1. business-analyst → requirements
2. backend-architect → schema design
3. backend-architect → API design
4. Parallel: technical-documentation-writer + security-auditor

### Template Prompts

**Requirements Analysis**:
```
"Extract data requirements from these user stories: [stories]. Identify entities, relationships, and constraints."
```

**Schema Design**:
```
"Design a [database type] schema for [feature] with [key entities]. Include indexes, foreign keys, and migration plan."
```

**API Design**:
```
"Design REST API endpoints for [feature] with CRUD operations, authentication, and proper error handling"
```

**Documentation**:
```
"Generate OpenAPI documentation for the [feature] API endpoints with request/response examples"
```

### Expected Outcomes

- ✅ Normalized database schema (DDL statements)
- ✅ Migration scripts (up/down)
- ✅ API endpoint specifications
- ✅ OpenAPI/Swagger documentation
- ✅ Security review report
- ⏱️ Timeline: 20-40 minutes for design + docs

### Success Criteria

- [ ] Schema normalized (3NF minimum)
- [ ] Indexes cover common queries
- [ ] API follows REST conventions
- [ ] Authentication/authorization defined
- [ ] Migration tested on staging data

---

## UI Prototyping & State Management

### When to Use

- **Frontend features** requiring state management
- **Component scaffolding** for new UI sections
- **Design system integration** for consistent UI
- **Prototype creation** for stakeholder review

### Workflow Pattern

```
1. User Flow Mapping
   └─> ux-designer: Map user journey for feature
       ├─> Screens and transitions
       ├─> Decision points
       └─> Error states

2. State Design
   └─> frontend-developer: Design state store (Redux/Zustand/Pinia)
       ├─> State shape
       ├─> Actions/reducers
       ├─> Selectors
       └─> Side effects

3. Component Scaffolding
   └─> frontend-developer: Create component structure
       ├─> Page components
       ├─> Container components
       ├─> Presentational components
       └─> TypeScript types

4. Integration
   └─> frontend-developer: Wire components to state
       └─> Event handlers, data flow, API calls
```

### Agent Coordination

**Sequential Flow**:
1. ux-designer → user flow
2. frontend-developer → state design
3. frontend-developer → component scaffolding
4. frontend-developer → integration

### Template Prompts

**User Flow Mapping**:
```
"Map the user workflow for [feature] from [start state] to [end state] with error handling"
```

**State Design**:
```
"Design a [Redux/Zustand/Pinia] store for [feature] with actions for [key operations]"
```

**Component Scaffolding**:
```
"Create [React/Vue/Angular] components for [feature] using [design system] with TypeScript"
```

**Integration**:
```
"Wire the [component name] to the [store name] state with [actions list]"
```

### Expected Outcomes

- ✅ User flow diagram with error states
- ✅ State management implementation (Redux/Zustand/etc)
- ✅ Component scaffolding (TypeScript)
- ✅ Integration code (event handlers, API calls)
- ⏱️ Timeline: 30-50 minutes for design + scaffolding

### Success Criteria

- [ ] State store compiles without errors
- [ ] Components match design system
- [ ] TypeScript types defined
- [ ] User flow covers error states
- [ ] Integration tested locally

---

## User Research & Workflow Mapping

### When to Use

- **Understanding user problems** before building solutions
- **Identifying friction points** in existing workflows
- **Validating feature ideas** with evidence
- **Designing user-centric solutions**

### Workflow Pattern

```
1. Problem Framing
   └─> product-strategist: Frame eigenquestion
       └─> What are we trying to understand?

2. User Workflow Analysis
   └─> ux-designer: Map current workflow
       ├─> Steps and decision points
       ├─> Pain points and friction
       ├─> Workarounds users employ
       └─> Success/failure scenarios

3. Evidence Synthesis
   └─> business-analyst: Analyze user feedback data
       ├─> Quantitative (metrics, usage data)
       ├─> Qualitative (interviews, support tickets)
       └─> Patterns and themes

4. Opportunity Definition
   └─> product-strategist: Frame as product opportunity
       ├─> Solution hypotheses
       ├─> Success metrics
       └─> Validation experiments
```

### Agent Coordination

**Sequential Flow**:
1. product-strategist → problem framing
2. ux-designer → workflow mapping
3. business-analyst → evidence synthesis
4. product-strategist → opportunity definition

### Template Prompts

**Problem Framing**:
```
"Frame [user problem] as an eigenquestion that focuses on root causes and value delivery"
```

**Workflow Analysis**:
```
"Map the current user workflow for [task] and identify friction points and workarounds"
```

**Evidence Synthesis**:
```
"Analyze this user feedback data [data] and identify patterns, themes, and root causes"
```

**Opportunity Definition**:
```
"Frame [friction point] as a product opportunity with solution hypotheses and success metrics"
```

### Expected Outcomes

- ✅ Eigenquestion framing (root cause focus)
- ✅ User workflow map with friction points
- ✅ Evidence synthesis report (quantitative + qualitative)
- ✅ Solution hypotheses with validation plan
- ⏱️ Timeline: 40-60 minutes for research + framing

### Success Criteria

- [ ] Workflow captures all major steps
- [ ] Friction points prioritized by impact
- [ ] Evidence supports problem framing
- [ ] Solution hypotheses are testable
- [ ] Success metrics defined

---

## Git Workflow & Engineering Handoffs

### When to Use

- **Feature branches** for new work
- **Pull requests** with complete context
- **Code reviews** requiring documentation
- **Professional handoffs** to engineering teams

### Workflow Pattern

```
1. Branch Creation
   └─> git-workflow-manager: Create feature branch
       └─> Naming convention: feature/[name]

2. Commit Organization
   └─> git-workflow-manager: Stage and commit files
       ├─> Logical grouping
       ├─> Clear commit messages
       └─> Co-authorship attribution

3. Pull Request Creation
   └─> git-workflow-manager: Open PR with context
       ├─> Summary and motivation
       ├─> Files included
       ├─> Acceptance criteria
       ├─> Test plan
       └─> Implementation notes

4. Changelog Generation
   └─> changelog-recorder: Auto-generate changelog
       └─> Track changes for release notes
```

### Agent Coordination

**Sequential Flow**:
1. git-workflow-manager → branch creation
2. git-workflow-manager → commits
3. git-workflow-manager → PR creation
4. changelog-recorder → changelog update

### Template Prompts

**Branch Creation**:
```
"Create a feature branch for [feature name] following [repo name] naming conventions"
```

**Commit Organization**:
```
"Commit [files] with a clear message describing [what changed and why]"
```

**Pull Request Creation**:
```
"Create a PR for [feature] with summary, acceptance criteria, test plan, and implementation notes"
```

**Changelog Update**:
```
"Generate changelog entry for [feature] following [CHANGELOG.md] format"
```

### Expected Outcomes

- ✅ Feature branch with clear naming
- ✅ Well-organized commits
- ✅ Comprehensive PR description
- ✅ Changelog entry
- ⏱️ Timeline: 10-15 minutes for branch + PR

### Success Criteria

- [ ] Branch follows naming convention
- [ ] Commits are logical and atomic
- [ ] PR includes all required sections
- [ ] Acceptance criteria are testable
- [ ] Changelog updated

---

## Product Strategy & Metrics Definition

### When to Use

- **Strategic planning** for features or products
- **OKR definition** for quarters
- **Success metrics** for experiments
- **Business case** development

### Workflow Pattern

```
1. Business Problem Analysis
   └─> product-strategist: Frame as eigenquestion
       ├─> Root cause identification
       ├─> Evidence gathering
       └─> Opportunity sizing

2. Solution Hypotheses
   └─> product-strategist: Generate testable hypotheses
       ├─> Problem → Solution mapping
       ├─> Assumptions to validate
       └─> Confidence levels

3. Metrics Definition
   └─> product-strategist: Define success metrics
       ├─> North Star metric
       ├─> Secondary metrics
       ├─> Leading indicators
       └─> Measurement plan

4. Validation Planning
   └─> product-strategist: Design experiments
       ├─> MVP scope
       ├─> A/B test plan
       ├─> User research
       └─> Success criteria
```

### Agent Coordination

**Sequential Flow** (all product-strategist):
1. Problem analysis
2. Solution hypotheses
3. Metrics definition
4. Validation planning

### Template Prompts

**Problem Analysis**:
```
"Analyze [business problem] as an eigenquestion with root causes, evidence, and opportunity sizing"
```

**Solution Hypotheses**:
```
"Generate 3-5 solution hypotheses for [problem] with assumptions and confidence levels"
```

**Metrics Definition**:
```
"Define success metrics for [solution] including North Star, secondary metrics, and leading indicators"
```

**Validation Planning**:
```
"Design validation experiments for [hypotheses] with MVP scope, test plan, and success criteria"
```

### Expected Outcomes

- ✅ Eigenquestion framing (root cause focus)
- ✅ 3-5 testable solution hypotheses
- ✅ Comprehensive metrics framework
- ✅ Validation experiment plan
- ⏱️ Timeline: 40-60 minutes for strategy work

### Success Criteria

- [ ] Problem framed as eigenquestion
- [ ] Hypotheses are specific and testable
- [ ] Metrics align with business goals
- [ ] Validation plan is actionable
- [ ] Success criteria defined

---

## Iterative Design & Feedback Loops

### When to Use

- **Rapid prototyping** with quick iterations
- **User testing** and feedback incorporation
- **Design refinement** based on evidence
- **Continuous improvement** of features

### Workflow Pattern

```
1. Initial Prototype
   ├─> ux-designer: Create initial design
   └─> frontend-developer: Scaffold prototype

2. User Testing
   └─> ux-designer: Design test plan
       ├─> Test scenarios
       ├─> Success criteria
       └─> Feedback collection

3. Evidence Analysis
   └─> business-analyst: Synthesize feedback
       ├─> Patterns and themes
       ├─> Quantitative metrics
       └─> Priority issues

4. Iteration
   ├─> design-simplicity-advisor: Simplification opportunities
   ├─> ux-designer: Design improvements
   └─> frontend-developer: Implement changes

5. Validation
   └─> Loop back to step 2 or ship

```

### Agent Coordination

**Iterative Loop**:
1. ux-designer + frontend-developer → prototype
2. ux-designer → test plan
3. business-analyst → evidence analysis
4. design-simplicity-advisor + ux-designer + frontend-developer → improvements
5. Repeat until validated

### Template Prompts

**Initial Prototype**:
```
"Create a prototype for [feature] with [key interactions] using [framework/design system]"
```

**Test Plan**:
```
"Design a user test plan for [feature] with scenarios, success criteria, and feedback questions"
```

**Evidence Analysis**:
```
"Analyze this user feedback [data] and identify patterns, priority issues, and improvement opportunities"
```

**Iteration**:
```
"Based on feedback [summary], refine [feature] design focusing on [key issue]"
```

### Expected Outcomes

- ✅ Working prototype (scaffolded code)
- ✅ User test plan with scenarios
- ✅ Feedback analysis report
- ✅ Refined design (iterate until validated)
- ⏱️ Timeline: 30-45 minutes per iteration

### Success Criteria

- [ ] Prototype demonstrates key interactions
- [ ] Test plan covers critical paths
- [ ] Feedback collected from 5+ users
- [ ] Priority issues addressed
- [ ] Success metrics improving

---

## Workflow Combinations

Real PM work often combines multiple patterns. Here are common combinations:

### Full Feature Development

```
1. Product Strategy & Metrics Definition
   └─> Frame problem, define success metrics

2. Spec-Driven Feature Development
   └─> Create detailed specification

3. Database Design & API Planning
   └─> Design data layer

4. UI Prototyping & State Management
   └─> Build frontend prototype

5. Iterative Design & Feedback Loops
   └─> Test and refine

6. Git Workflow & Engineering Handoffs
   └─> Create PR for engineering
```

### Research-Driven Design

```
1. User Research & Workflow Mapping
   └─> Understand current state

2. Product Strategy & Metrics Definition
   └─> Frame opportunity

3. Iterative Design & Feedback Loops
   └─> Prototype and validate

4. Spec-Driven Feature Development
   └─> Document final design

5. Git Workflow & Engineering Handoffs
   └─> Handoff to engineering
```

### Technical Exploration

```
1. Database Design & API Planning
   └─> Design data layer

2. UI Prototyping & State Management
   └─> Build UI prototype

3. Spec-Driven Feature Development
   └─> Document technical design

4. Git Workflow & Engineering Handoffs
   └─> Create PR with prototype
```

---

## Best Practices

### 1. Start Small

Begin with single workflows before combining:
- ✅ Try one workflow pattern at a time
- ✅ Master the agents for each pattern
- ✅ Then combine patterns

### 2. Iterate Quickly

Use short feedback loops:
- ✅ Create prototype → get feedback → refine
- ✅ Don't wait for perfect before testing
- ✅ Validate assumptions early

### 3. Document Everything

Keep a paper trail:
- ✅ Specs in version control
- ✅ Design decisions documented
- ✅ Validation results captured
- ✅ Feedback synthesized

### 4. Leverage Agent Strengths

Use the right agent for each task:
- ✅ product-strategist for strategy and framing
- ✅ backend-architect for technical design
- ✅ ux-designer for user workflows
- ✅ git-workflow-manager for handoffs

### 5. Set Clear Success Criteria

Define what "done" looks like:
- ✅ Spec approved by stakeholders
- ✅ Prototype validated with users
- ✅ Engineering team acknowledged PR
- ✅ Success metrics defined

---

## Troubleshooting

### Common Issues

**Issue**: Agent doesn't understand context
**Solution**: Provide more specifics in prompt
```
# Too vague
"Design a database"

# Better
"Design a PostgreSQL schema for multi-tenant SaaS with organizations, users, and projects"
```

**Issue**: Output is too generic
**Solution**: Reference existing patterns or examples
```
"Design a Redux store for shopping cart like the Airbnb checkout flow"
```

**Issue**: Multiple agents needed, unclear how to coordinate
**Solution**: Use workflow patterns from this library
```
"Follow the 'Spec-Driven Feature Development' workflow for OAuth2 authentication"
```

### Getting Help

- **Workflow Questions**: [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)
- **Agent Issues**: [GitHub Issues](https://github.com/robertmnyborg/claude-oak-agents/issues)
- **Examples**: [PM_QUICK_START.md](PM_QUICK_START.md) for step-by-step examples

---

## Resources

### Related Documentation
- **[PM_QUICK_START.md](PM_QUICK_START.md)** - 6 detailed examples with step-by-step walkthroughs
- **[PM_CAPABILITIES.md](PM_CAPABILITIES.md)** - What works vs what requires manual work
- **[USER_GUIDE.md](../USER_GUIDE.md)** - Complete system documentation
- **[README.md](../README.md)** - Project overview and installation

### Agent Documentation
- **[agents/](../../agents/)** - Full agent definitions
- **[CLAUDE.md](../CLAUDE.md)** - System rules and agent coordination

---

**Ready to use these patterns?** Start with a single workflow and combine as you gain experience.
