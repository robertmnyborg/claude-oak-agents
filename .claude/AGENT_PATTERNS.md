# Agent Activation Patterns and Best Practices

**Version**: 1.0.0
**Last Updated**: 2025-10-30
**Purpose**: Guide for when to activate which agents, common patterns, and decision trees

---

## Quick Reference: Agent Decision Tree

```
User Request Analysis
├─ INFORMATION REQUEST?
│  ├─ Simple question → Handle directly (no agent)
│  ├─ Complex codebase search → Explore agent
│  └─ Research/analysis → Plan agent or domain analyst
│
├─ IMPLEMENTATION REQUEST?
│  ├─ Design phase → design-simplicity-advisor (MANDATORY)
│  ├─ Single domain
│  │  ├─ Backend → backend-architect
│  │  ├─ Frontend → frontend-developer
│  │  ├─ Infrastructure → infrastructure-specialist
│  │  ├─ Security → security-auditor
│  │  └─ Mobile → mobile-developer
│  ├─ Multi-domain → project-manager + domain specialists
│  └─ Post-implementation → code-reviewer + security-auditor
│
├─ DEBUGGING/ERRORS?
│  └─ debug-specialist (HIGHEST PRIORITY)
│
├─ PRE-COMMIT?
│  ├─ code-reviewer (MANDATORY)
│  └─ security-auditor (if security-sensitive)
│
└─ STRATEGIC PLANNING?
   ├─ Product strategy → product-strategist
   ├─ System architecture → systems-architect
   └─ Business analysis → business-analyst
```

---

## Agent Priority Tiers

### Critical Priority (Always Auto-Activate)
**These agents must run for their trigger conditions**:

1. **debug-specialist**
   - Trigger: Errors, exceptions, failures detected
   - Why critical: Blocks all other work until resolved
   - Example: "TypeError: Cannot read property 'x' of undefined"

2. **security-auditor**
   - Trigger: Auth/security files, payment processing, PII handling
   - Why critical: Security vulnerabilities can't wait
   - Example: Modifying authentication handlers

3. **design-simplicity-advisor**
   - Trigger: Complex design decisions, multi-service architectures
   - Why critical: Prevents over-engineering before it happens
   - Example: "Build a new microservice for user notifications"

### High Priority (Auto-Activate for Domain Work)

4. **code-reviewer**
   - Trigger: 3+ files modified, pre-commit, significant changes
   - Why high: Quality gates before code enters repo
   - Example: Committing feature with 5 file changes

5. **backend-architect**
   - Trigger: Database, API, server-side work
   - Why high: Core business logic and data integrity
   - Example: "Design schema for multi-tenant SaaS"

6. **frontend-developer**
   - Trigger: UI components, state management, styling
   - Why high: User-facing features need quality
   - Example: "Build React dashboard with charts"

7. **infrastructure-specialist**
   - Trigger: CDK, deployment, CI/CD, containers
   - Why high: Infrastructure changes affect everything
   - Example: "Deploy Lambda function with API Gateway"

8. **project-manager**
   - Trigger: 3+ agents needed, complex workflows
   - Why high: Coordination prevents chaos
   - Example: "Build payment system with Stripe + webhooks + database"

### Medium Priority (Suggest When Relevant)

9. **unit-test-expert**
   - Trigger: Test writing, coverage improvement
   - Why medium: Important but not blocking
   - Example: "Write tests for authentication service"

10. **qa-specialist**
    - Trigger: Integration testing, e2e testing
    - Why medium: Quality assurance layer
    - Example: "Create e2e test for checkout flow"

11. **performance-optimizer**
    - Trigger: Performance issues, bottlenecks
    - Why medium: Often optimization can wait
    - Example: "Why is my API slow?"

12. **spec-manager**
    - Trigger: Specification creation, requirements
    - Why medium: Planning phase agent
    - Example: "Create spec for user onboarding feature"

### Low Priority (Manual Invocation)

13. **git-workflow-manager**
    - Trigger: Git operations, PR creation
    - Why low: Often handled automatically
    - Example: "Create pull request for this feature"

14. **technical-writer**
    - Trigger: Documentation creation
    - Why low: Can be done after implementation
    - Example: "Write API documentation"

15. **dependency-scanner**
    - Trigger: Dependency updates, CVE scanning
    - Why low: Periodic maintenance task
    - Example: "Check for security vulnerabilities in dependencies"

---

## Common Agent Combinations (Workflows)

### Workflow 1: New Feature Implementation
**Pattern**: Design → Implement → Review → Commit

```yaml
workflow: "new-feature"
phases:
  - phase: "design"
    agents:
      - design-simplicity-advisor  # Ensures KISS principle
      - systems-architect          # If architectural decision needed
    parallel: false

  - phase: "implementation"
    agents:
      - backend-architect          # If backend changes
      - frontend-developer         # If frontend changes
      - infrastructure-specialist  # If infra changes
    parallel: true  # Can work simultaneously

  - phase: "quality-gates"
    agents:
      - unit-test-expert          # Write tests
      - code-reviewer             # Review code
      - security-auditor          # If security-sensitive
    parallel: true

  - phase: "commit"
    agents:
      - git-workflow-manager      # Create commit + PR
    parallel: false

example:
  request: "Add OAuth2 authentication to API"
  execution:
    1. design-simplicity-advisor validates approach
    2. backend-architect + security-auditor implement
    3. unit-test-expert + code-reviewer validate
    4. git-workflow-manager commits
```

### Workflow 2: Bug Fix
**Pattern**: Debug → Fix → Test → Commit

```yaml
workflow: "bug-fix"
phases:
  - phase: "diagnosis"
    agents:
      - debug-specialist  # HIGHEST PRIORITY
    parallel: false
    blocking: true  # Nothing else happens until debugged

  - phase: "fix"
    agents:
      - <domain-specialist>  # backend-architect, frontend-developer, etc.
    parallel: false

  - phase: "validation"
    agents:
      - unit-test-expert  # Add regression test
      - code-reviewer     # Quick review
    parallel: true

  - phase: "commit"
    agents:
      - git-workflow-manager
    parallel: false

example:
  request: "API returns 500 error on user login"
  execution:
    1. debug-specialist diagnoses (async handler issue)
    2. backend-architect implements fix
    3. unit-test-expert adds regression test
    4. git-workflow-manager commits
```

### Workflow 3: Security-Critical Feature
**Pattern**: Security Review → Design → Implement → Security Audit → Pen Test

```yaml
workflow: "security-critical"
phases:
  - phase: "security-design-review"
    agents:
      - security-auditor          # Review design first
      - design-simplicity-advisor # Ensure simple = secure
    parallel: false
    blocking: true

  - phase: "implementation"
    agents:
      - backend-architect  # With security constraints
    parallel: false

  - phase: "security-validation"
    agents:
      - security-auditor  # Comprehensive audit
      - unit-test-expert  # Security-focused tests
    parallel: false  # Security audit must complete first
    blocking: true

  - phase: "commit"
    agents:
      - git-workflow-manager
    parallel: false

example:
  request: "Implement payment processing with Stripe"
  execution:
    1. security-auditor reviews approach
    2. design-simplicity-advisor ensures simple design
    3. backend-architect implements with PCI compliance
    4. security-auditor validates (mandatory)
    5. unit-test-expert adds security tests
    6. git-workflow-manager commits
```

### Workflow 4: Infrastructure Deployment
**Pattern**: Design → Infrastructure → Test → Deploy

```yaml
workflow: "infrastructure-deployment"
phases:
  - phase: "architecture"
    agents:
      - systems-architect         # High-level design
      - design-simplicity-advisor # Avoid over-engineering
    parallel: false

  - phase: "implementation"
    agents:
      - infrastructure-specialist  # CDK/Terraform implementation
    parallel: false

  - phase: "validation"
    agents:
      - security-auditor  # Security review of infra
      - qa-specialist     # Integration testing
    parallel: true

  - phase: "deployment"
    agents:
      - infrastructure-specialist  # Deploy to AWS
      - git-workflow-manager       # Commit infrastructure code
    parallel: false

example:
  request: "Deploy microservice to AWS with Lambda + API Gateway + RDS"
  execution:
    1. systems-architect designs architecture
    2. design-simplicity-advisor validates (Do we need microservice?)
    3. infrastructure-specialist implements CDK
    4. security-auditor + qa-specialist validate
    5. infrastructure-specialist deploys
```

### Workflow 5: Complex Multi-Domain Project
**Pattern**: Project Manager orchestrates everything

```yaml
workflow: "complex-project"
coordinator: project-manager  # Mandatory for 3+ agents
phases:
  - phase: "planning"
    agents:
      - project-manager           # Overall coordination
      - product-strategist        # Strategic direction
      - systems-architect         # Technical feasibility
    parallel: false

  - phase: "design"
    agents:
      - design-simplicity-advisor # KISS enforcement
      - backend-architect         # Backend design
      - frontend-developer        # Frontend design
      - infrastructure-specialist # Infra design
    parallel: true  # Design in parallel
    coordinator: project-manager

  - phase: "implementation"
    agents:
      - backend-architect
      - frontend-developer
      - infrastructure-specialist
    parallel: true
    coordinator: project-manager

  - phase: "quality-gates"
    agents:
      - code-reviewer
      - security-auditor
      - qa-specialist
      - unit-test-expert
    parallel: true
    coordinator: project-manager

  - phase: "deployment"
    agents:
      - infrastructure-specialist
      - git-workflow-manager
    parallel: false
    coordinator: project-manager

example:
  request: "Build complete e-commerce checkout with payment, inventory, and email notifications"
  execution:
    1. project-manager creates overall plan
    2. product-strategist validates business value
    3. systems-architect designs system architecture
    4. design-simplicity-advisor reviews (warns against over-engineering)
    5. project-manager coordinates parallel implementation
    6. project-manager coordinates quality gates
    7. project-manager coordinates deployment
```

---

## When NOT to Use Agents

### Handle Directly (No Agent Needed)

1. **Simple Questions**
   - "What does this function do?"
   - "Where is X defined?"
   - "Explain this code"
   → Just read and explain

2. **Trivial Edits**
   - Fix typo in comment
   - Update version number
   - Change log message
   → Direct edit, no review needed

3. **Pure Research**
   - "Find all usages of function X"
   - "Show me the schema for table Y"
   - "List all API endpoints"
   → Use Grep/Glob/Read directly

4. **Already Using Agent**
   - User explicitly invoked agent
   - Agent is already running
   - Inside agent context
   → Don't suggest another agent

---

## Agent Composition Patterns

### Pattern 1: Sequential (One After Another)
**Use when**: Each agent depends on previous agent's output

```
design-simplicity-advisor → backend-architect → code-reviewer → git-workflow-manager
```

Example: Design must be validated before implementation

### Pattern 2: Parallel (Simultaneous Execution)
**Use when**: Agents work on independent parts

```
backend-architect + frontend-developer + infrastructure-specialist (parallel)
↓
code-reviewer + security-auditor (parallel)
```

Example: Backend, frontend, and infra can be developed simultaneously

### Pattern 3: Hybrid (Mixed Sequential + Parallel)
**Use when**: Some dependencies exist but some work is independent

```
Phase 1 (Sequential):
  design-simplicity-advisor → systems-architect

Phase 2 (Parallel):
  backend-architect + frontend-developer + infrastructure-specialist

Phase 3 (Sequential):
  code-reviewer → security-auditor (security must wait for code review)

Phase 4 (Sequential):
  git-workflow-manager
```

Example: Most complex projects

### Pattern 4: Iterative (Loop Until Success)
**Use when**: Agent output needs refinement

```
backend-architect → code-reviewer → [issues found] → backend-architect → code-reviewer → [pass]
```

Example: Code review finds issues requiring fixes

---

## Agent Selection Confidence Levels

### High Confidence (90%+) - Auto-Activate
- Keywords match exactly (e.g., "authentication" → security-auditor)
- File patterns match (e.g., `**/auth/**` → security-auditor)
- Event triggers (e.g., error detected → debug-specialist)

### Medium Confidence (70-89%) - Suggest to User
- Keywords partially match
- Multiple agents could apply
- User context unclear

### Low Confidence (<70%) - Don't Suggest
- Vague request
- No clear domain
- Informational query

---

## Progressive Disclosure: When to Load Resources

### Agents with Resources (500-line rule)
Some agents are split into main + resources:

```
agents/
  backend-architect/
    main.md              # Always loaded (<500 lines)
    resources/
      database-design.md  # Load when database work detected
      api-patterns.md     # Load when API design mentioned
      microservices.md    # Load when microservices mentioned
```

**Load resources when**:
- User explicitly asks ("show me database design patterns")
- Keywords match resource topic (e.g., "microservices" → microservices.md)
- Main agent requests specific resource
- Deep-dive needed (initial approach insufficient)

**Benefits**:
- Reduces context bloat (90% of cases don't need all resources)
- Faster agent invocation (less content to process)
- Targeted expertise (only load what's needed)

---

## Telemetry-Driven Agent Improvements

### What the System Learns

1. **Usage Patterns**
   - Which agents are used most frequently?
   - Which agent combinations work well together?
   - Which agents are underutilized?

2. **Success Patterns**
   - Which agents have highest success rates?
   - Which workflows complete fastest?
   - Which agent suggestions do users accept?

3. **Failure Patterns**
   - Which agents fail most often?
   - What types of tasks cause failures?
   - Which agent combinations cause conflicts?

4. **Performance Patterns**
   - Which agents are slowest?
   - Which agents use most context?
   - Which agents could be optimized?

### Continuous Improvement Loop

```
User Request
↓
Agent Suggestion (based on rules + historical success)
↓
Agent Execution (tracked via telemetry)
↓
Success/Failure Recorded
↓
Telemetry Analysis
↓
Agent Rules Updated (confidence thresholds, patterns)
↓
Next User Request (smarter suggestions)
```

---

## Example Decision Walkthroughs

### Example 1: "Add authentication to my API"

**Analysis**:
- Domain: Backend + Security
- Complexity: Medium-High
- Files affected: Auth handlers, middleware, database

**Decision**:
```
1. design-simplicity-advisor (MANDATORY for new patterns)
   → Validates approach (OAuth2 vs Sessions vs JWT)

2. backend-architect + security-auditor (PARALLEL)
   → backend-architect: Schema, API design
   → security-auditor: Security review of approach

3. unit-test-expert + code-reviewer (PARALLEL)
   → unit-test-expert: Auth tests
   → code-reviewer: Code quality

4. git-workflow-manager (SEQUENTIAL)
   → Create commit + PR
```

**Confidence**: High (95%)
**Rationale**: Clear backend + security work

### Example 2: "Why is my page loading slow?"

**Analysis**:
- Type: Debugging + Performance
- Urgency: High (user-facing issue)
- Domain: Unclear (could be frontend, backend, or infrastructure)

**Decision**:
```
1. debug-specialist (HIGHEST PRIORITY)
   → Diagnose root cause
   → Result: Frontend rendering bottleneck

2. frontend-developer (based on diagnosis)
   → Optimize React rendering

3. performance-optimizer (OPTIONAL)
   → Additional performance tuning
```

**Confidence**: High (90%) for debug-specialist
**Rationale**: Error/issue detected → debug first

### Example 3: "Explain this code"

**Analysis**:
- Type: Information request
- Complexity: Simple
- No implementation needed

**Decision**:
```
NO AGENT NEEDED
→ Direct explanation via main LLM
```

**Confidence**: High (95%) for no agent
**Rationale**: Simple informational query

### Example 4: "Build a payment system with Stripe"

**Analysis**:
- Domain: Backend + Security + Infrastructure
- Complexity: Very High
- Multiple agents required

**Decision**:
```
1. project-manager (MANDATORY for complex multi-domain)
   → Overall coordination

2. design-simplicity-advisor + product-strategist (SEQUENTIAL)
   → Validate business need and design simplicity

3. backend-architect + security-auditor + infrastructure-specialist (PARALLEL)
   → Coordinated by project-manager

4. unit-test-expert + qa-specialist (PARALLEL)
   → Testing strategy

5. code-reviewer + security-auditor (SEQUENTIAL)
   → Final quality gates

6. git-workflow-manager (SEQUENTIAL)
   → Commit and PR creation
```

**Confidence**: High (95%)
**Rationale**: Payment = security-critical + multi-domain

---

## Quick Agent Reference Card

| Agent | When to Use | Auto-Activate | Priority |
|-------|-------------|---------------|----------|
| **debug-specialist** | Errors, bugs, failures | ✅ YES | 🔴 Critical |
| **security-auditor** | Auth, payment, PII, secrets | ✅ YES | 🔴 Critical |
| **design-simplicity-advisor** | Complex designs, new patterns | ✅ YES | 🔴 Critical |
| **code-reviewer** | Pre-commit, 3+ files, refactor | ✅ YES | 🟠 High |
| **backend-architect** | Database, API, server-side | ✅ YES | 🟠 High |
| **frontend-developer** | UI, components, state, styling | ✅ YES | 🟠 High |
| **infrastructure-specialist** | CDK, deployment, containers | ✅ YES | 🟠 High |
| **project-manager** | 3+ agents, complex workflows | ✅ YES | 🟠 High |
| **unit-test-expert** | Test writing, coverage | ✅ YES | 🟡 Medium |
| **qa-specialist** | Integration, e2e testing | ⚠️ SUGGEST | 🟡 Medium |
| **performance-optimizer** | Bottlenecks, optimization | ⚠️ SUGGEST | 🟡 Medium |
| **spec-manager** | Requirements, specifications | ⚠️ SUGGEST | 🟡 Medium |
| **product-strategist** | Product strategy, metrics | ⚠️ SUGGEST | 🟡 Medium |
| **systems-architect** | System design, architecture | ⚠️ SUGGEST | 🟡 Medium |
| **git-workflow-manager** | Commits, PRs, git operations | ❌ MANUAL | 🟢 Low |
| **technical-writer** | Documentation creation | ❌ MANUAL | 🟢 Low |
| **dependency-scanner** | CVE scanning, updates | ❌ MANUAL | 🟢 Low |

**Legend**:
- ✅ YES = Auto-activate when triggers match
- ⚠️ SUGGEST = Suggest to user when relevant
- ❌ MANUAL = User must explicitly request
- 🔴 Critical = Blocks all other work
- 🟠 High = Primary domain work
- 🟡 Medium = Supporting work
- 🟢 Low = Maintenance/optional

---

## Troubleshooting Agent Selection

### Problem: Too Many Agents Suggested
**Solution**: Increase confidence thresholds in `agent-rules.json`

### Problem: Relevant Agent Not Suggested
**Solution**: Add keywords/patterns to agent triggers

### Problem: Agents Conflict or Duplicate Work
**Solution**: Use project-manager to coordinate

### Problem: Slow Agent Execution
**Solution**: Use progressive disclosure (load resources only when needed)

### Problem: Agent Suggests Wrong Approach
**Solution**: Use design-simplicity-advisor before implementation

---

**For complete agent documentation, see**:
- Individual agent files in `/agents/`
- Agent rules configuration in `/.claude/agent-rules.json`
- Auto-activation hook in `/.claude/hooks/agent-activation-prompt.md`
