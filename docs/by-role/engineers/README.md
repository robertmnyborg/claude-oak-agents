# Engineers Guide

**Specialized code generation, automatic quality gates, and multi-agent coordination**

This guide helps you implement features efficiently using domain-specific agents, automated workflows, and comprehensive telemetry.

---

## Quick Navigation

### Getting Started
- **[Installation](../../getting-started/README.md#for-engineers)** - 5-minute setup
- **[First Workflow](../../getting-started/README.md#for-engineers)** - Implement your first feature

### Technical Reference
- **[Technical Reference](technical-reference.md)** - Comprehensive system internals
  - Workflow tracking system
  - Success metrics reference
  - Adaptive system design
  - Metadata-only prompts architecture

### Development Guides
- **[Agent Development](agent-development.md)** - Create custom agents
  - Multi-file agent structure
  - Bundled scripts (10-100x faster)
  - Agent packaging and deployment

### Architecture
- **[Model Selection Strategy](../../../MODEL_SELECTION_STRATEGY.md)** - Cost optimization
  - Premium/Balanced/Fast tiers
  - When to override model tier
  - Performance vs cost tradeoffs

---

## What You Can Do

### 1. Implement Features with Specialized Agents

The system routes your requests to domain-specific specialists automatically:

**Frontend Development**:
```
"Create a React dashboard component with charts"
→ frontend-developer (TypeScript, functional patterns, modern frameworks)
```

**Backend Development**:
```
"Implement REST API for task management"
→ backend-architect (Go > TypeScript > JavaScript, SOA thinking)
```

**Infrastructure**:
```
"Deploy Lambda function with CDK"
→ infrastructure-specialist (TypeScript/CDK preferred, serverless-first)
```

**Security**:
```
"Audit authentication implementation for vulnerabilities"
→ security-auditor (penetration testing, OWASP compliance)
```

---

### 2. Automatic Quality Gates

Every implementation goes through comprehensive quality validation:

**Quality Gate Process**:
```
Implementation
  ↓
quality-gate (unified validation):
  - Code review and standards
  - Maintainability analysis
  - Architectural impact assessment
  - Implementation complexity validation
  - KISS principle compliance
  - Security and performance checks
  ↓
Git Operations (if approved)
```

**Benefits**:
- Consistent code quality
- Automatic simplicity enforcement
- Security validation
- Test coverage verification
- Documentation completeness

---

### 3. Multi-Agent Coordination

Complex tasks automatically coordinate multiple specialists:

**Example: Secure API Implementation**
```
"Implement secure OAuth2 API with monitoring"

System coordinates:
  design-simplicity-advisor (upfront analysis)
    ↓
  security-auditor + backend-architect + infrastructure-specialist (parallel)
    ↓
  quality-gate (unified validation)
    ↓
  git-workflow-manager (commit and PR)
```

**Automatic workflow selection**:
- Simple tasks: Single agent
- Complex tasks: Multi-agent coordination
- Security-critical: Automatic security audits
- High-risk: Hybrid planning workflow

---

## Development Workflow

### Standard Implementation Flow

```
1. Request Classification
   System analyzes: Type (Info/Implementation/Analysis)
   System identifies: Domain (Frontend/Backend/Infrastructure)

2. Agent Selection
   System selects: Appropriate specialist(s)
   System determines: Sequential or parallel execution

3. Implementation
   Agent(s) execute: Code generation, configuration, tests

4. Quality Gate
   quality-gate validates: All quality dimensions
   System blocks: Commits until validation passes

5. Git Operations
   git-workflow-manager: Creates commit with proper message
   System includes: Claude Code attribution
```

---

### Hybrid Planning for Complex Projects

For high-risk or complex features, the system uses hybrid planning:

**When it triggers**:
- Risk level: HIGH or CRITICAL
- Estimated time: >4 hours
- Number of agents: ≥4
- Security-critical changes
- Architecture decisions

**4-Phase Process**:

**Phase 1: Strategic Planning** (10-30 min)
- Main LLM + design-simplicity-advisor + project-manager
- Define task assignments, constraints, context

**Phase 2: Implementation Planning** (Parallel, 5-20 min)
- All assigned agents propose 2-3 approaches
- Each includes: Pros, cons, risks, estimates
- Agents recommend preferred option

**Phase 3: Plan Review** (Parallel, 10-20 min)
- project-manager + product-strategist + design-simplicity-advisor
- Validate technical feasibility
- Detect conflicts between agent plans
- Synthesize refined execution plan

**Phase 4: Execution**
- Execute with refined plan
- Track workflow with telemetry
- Validate completion

See [Hybrid Planning Guide](../architects/hybrid-planning.md) for details.

---

## Your Engineering Agents

### Core Development Agents

**frontend-developer**
- React, Vue, Angular (functional > OOP)
- TypeScript preferred
- Modern state management (Redux/Zustand/Pinia)
- Component-based architecture

**backend-architect**
- Go > TypeScript > JavaScript
- REST and GraphQL APIs
- Database schema design
- SOA and microservices thinking

**infrastructure-specialist**
- AWS CDK (TypeScript > Go > Python)
- Serverless-first (Lambda > ECS > K8s)
- Deployment automation
- Infrastructure as code

### Quality and Security Agents

**quality-gate**
- Unified code review
- Maintainability analysis
- Architectural impact assessment
- Implementation complexity validation
- KISS principle enforcement
- Security and performance checks

**security-auditor**
- Penetration testing
- OWASP compliance
- Threat modeling
- Vulnerability assessment

**unit-test-expert**
- Unit test creation
- Coverage validation
- Test strategy
- Mock and stub generation

**dependency-scanner**
- Supply chain security
- License compliance
- Vulnerability scanning
- Dependency updates

### Workflow Agents

**git-workflow-manager**
- Git operations
- Branch management
- Commit messages
- Pull request creation

**project-manager**
- Multi-step coordination
- Timeline management
- Resource allocation
- Risk tracking

**spec-manager**
- Specification-driven development
- Task decomposition
- Implementation tracking
- Change management

### Analysis Agents

**business-analyst**
- Requirements analysis
- User stories
- Stakeholder communication
- Evidence synthesis

**technical-writer**
- Context-aware documentation
- API documentation
- User guides
- Technical specifications

### Special Purpose Agents

**design-simplicity-advisor**
- KISS enforcement
- Complexity analysis
- Over-engineering detection
- Simplification recommendations

**debug-specialist**
- Critical error resolution
- HIGHEST PRIORITY
- Production incident response
- Root cause analysis

**systems-architect**
- High-level design
- Technical specifications
- Architecture decisions
- Design patterns

---

## Common Engineering Workflows

### Workflow 1: Simple Feature Implementation

```
"Implement user registration API endpoint"

System flow:
  1. Classification: IMPLEMENTATION
  2. Domain: Backend
  3. Agent: backend-architect
  4. Quality gate: Automatic validation
  5. Git: Automatic commit
```

**Time**: 10-30 minutes

---

### Workflow 2: Complex Feature (Hybrid Planning)

```
"Implement OAuth2 authentication with monitoring"

System flow:
  1. Classification: IMPLEMENTATION (HIGH risk, 4+ agents)
  2. Hybrid planning workflow triggered

  Phase 1: Strategic Planning (15 min)
    - design-simplicity-advisor analyzes complexity
    - project-manager creates task breakdown

  Phase 2: Implementation Planning (Parallel, 10 min)
    - backend-architect: OAuth2 endpoints (3 options)
    - security-auditor: Security strategy (2 options)
    - infrastructure-specialist: Monitoring setup (2 options)

  Phase 3: Plan Review (10 min)
    - Validate technical feasibility
    - Detect conflicts
    - Synthesize final plan

  Phase 4: Execution (Varies)
    - Execute refined tasks
    - Validate completion
```

**Time**: 60-120 minutes (depending on complexity)

---

### Workflow 3: Bug Fix

```
"Fix null pointer error in user service"

System flow:
  1. Classification: IMPLEMENTATION (error = automatic)
  2. Domain: Backend
  3. Priority: HIGH (if production)
  4. Agent: debug-specialist (if critical) OR backend-architect
  5. Quality gate: Ensure fix doesn't break other functionality
  6. Git: Commit with error context
```

**Time**: 5-20 minutes

---

### Workflow 4: Security Audit

```
"Audit authentication system for vulnerabilities"

System flow:
  1. Classification: ANALYSIS
  2. Domain: Security
  3. Agents: security-auditor + dependency-scanner (parallel)
  4. Synthesis: Main LLM combines findings
  5. Output: Comprehensive security report
```

**Time**: 15-30 minutes

---

## Telemetry and Analytics

### Workflow Tracking

The system tracks multi-agent workflows with comprehensive telemetry:

**Features**:
- Workflow ID linking related invocations
- Parent invocation ID tracking agent sequences
- Duration and status tracking
- Success metrics and analytics

**Query workflows**:
```bash
# List all workflows
./scripts/query_workflow.sh --list-all

# Show specific workflow details
./scripts/query_workflow.sh wf-20251022-abc123

# List today's workflows
./scripts/query_workflow.sh --list-today
```

**Example output**:
```
Workflow: wf-20251022-abc123
Invocations: 3

1. design-simplicity-advisor (inv-20251022-001)
   Duration: 45.2s | Status: success

2. backend-architect (inv-20251022-002)
   Duration: 120.5s | Status: success | Parent: inv-20251022-001

3. security-auditor (inv-20251022-003)
   Duration: 78.3s | Status: success | Parent: inv-20251022-002
```

See [Technical Reference](technical-reference.md#workflow-tracking-system) for complete documentation.

---

## Model Selection Strategy

The system uses tiered model selection for cost optimization:

**Premium Tier (Opus)** - Strategic planning, architecture
- systems-architect, design-simplicity-advisor, project-manager
- Cost: High ($15-75/M tokens) | Speed: Slow (3-5s)

**Balanced Tier (Sonnet)** - Standard development
- frontend-developer, backend-architect, security-auditor
- Cost: Medium ($3-15/M tokens) | Speed: Normal (1-2s)

**Fast Tier (Haiku)** - Execution tasks, templates
- git-workflow-manager, unit-test-expert, qa-specialist
- Cost: Low ($1-5/M tokens) | Speed: Fast (300-500ms)

**Result**: 21% cost savings vs all-Sonnet baseline

See [Model Selection Strategy](../../../MODEL_SELECTION_STRATEGY.md) for details.

---

## Agent Development

### Creating Custom Agents

Use the **agent-creator** to create new agents when needed:

**When to create**:
- Capability gap detected
- 10+ routing failures for same domain
- Domain distinct from existing agents
- User explicitly requests new capability

**Process**:
```
1. Gap detection (automatic or explicit request)
2. agent-creator designs specification
3. Agent saved to agents/pending_review/
4. User reviews and approves
5. Agent deployed and registered
6. System monitors usage and performance
```

See [Agent Development Guide](agent-development.md) for complete documentation.

---

### Multi-File Agents

Advanced agent packaging using bundled scripts:

**Benefits**:
- 10-100x faster execution
- Modular agent structure
- Reusable components
- Better maintainability

See [Agent Development Guide](agent-development.md) for details.

---

## Tips for Success

### 1. Trust the Classification System

The system is designed to route requests correctly:
- Don't bypass classification
- Let the system select agents
- Override only when necessary

### 2. Use Spec-Driven Development for Complex Features

For significant features:
- Start with spec-manager
- Get design approval before implementation
- Update specs in "spec terms" not "code terms"
- Track implementation against spec

### 3. Leverage Quality Gates

Quality gates prevent issues before commit:
- Don't skip validation
- Address feedback promptly
- Trust the simplicity analysis
- Review security findings

### 4. Monitor Telemetry

Track your workflows:
- Identify bottlenecks
- Analyze agent performance
- Optimize coordination patterns
- Learn from successful workflows

### 5. Know When to Use Hybrid Planning

Use hybrid planning for:
- High-risk changes
- Complex multi-agent coordination
- Security-critical features
- Architecture decisions

Skip for:
- Simple bug fixes
- Single-agent tasks
- Well-understood patterns
- Quick iterations

---

## Common Questions

### How do I know which agent to use?

You don't need to - the system classifies requests and routes to appropriate agents automatically. You can explicitly request specific agents if preferred.

### Can I bypass quality gates for urgent fixes?

Only debug-specialist can bypass (critical production issues). All bypasses require post-commit review.

### How do I optimize for cost?

- Trust the model tier assignments (already optimized)
- Use spec-driven development (prevents rework)
- Leverage fast-tier agents for procedural tasks
- Monitor telemetry to identify inefficiencies

### What if an agent isn't performing well?

The system includes:
- agent-auditor for monthly performance reviews
- Automatic capability gap detection
- agent-creator for creating better specialists
- Continuous learning from telemetry

### How do I create a custom agent?

See [Agent Development Guide](agent-development.md). The system can auto-create agents when capability gaps are detected.

---

## Next Steps

**Technical deep dive**: Read [Technical Reference](technical-reference.md)

**Agent development**: Study [Agent Development Guide](agent-development.md)

**Architecture**: Review [System Design](../architects/system-design.md)

**Cost optimization**: See [Model Selection Strategy](../../../MODEL_SELECTION_STRATEGY.md)

---

**Ready to implement?** Start with the [Getting Started Guide](../../getting-started/README.md#for-engineers)
