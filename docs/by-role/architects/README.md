# Architects Guide

**System design, advanced patterns, architecture decisions, and research**

This guide helps you design scalable systems, establish engineering patterns, make architectural decisions, and understand the claude-oak-agents internals.

---

## Quick Navigation

### Architecture Documents
- **[System Design](system-design.md)** - Complete OaK architecture
  - Component architecture
  - Design principles
  - System internals

### Advanced Planning
- **[Hybrid Planning Guide](hybrid-planning.md)** - Multi-agent coordination
  - 4-phase planning workflow
  - When to use hybrid vs simple delegation
  - Decision matrix for workflow selection

### System Optimization
- **[Context Engineering](context-engineering.md)** - Prompt architecture
  - Progressive disclosure
  - 93% prompt size reduction
  - Scalability to 100+ agents

- **[Adaptive System Design](adaptive-system-design.md)** - Continuous improvement
  - Learning and evolution
  - Root cause analysis
  - A/B testing framework

### Implementation
- **[Implementation Guide](../../oak-design/IMPLEMENTATION_GUIDE.md)** - Integration patterns
  - Extension points
  - Development workflow
  - Custom integrations

- **[Deployment Plan](../../oak-design/6_MONTH_DEPLOYMENT_PLAN.md)** - Phased rollout
  - Timeline and milestones
  - Dependencies and risks
  - Validation strategy

---

## What You Can Do

### 1. Design System Architecture

Use **systems-architect** for high-level system design:

**Example**:
```
"Design a scalable microservices architecture for multi-tenant SaaS"
```

**You get**:
- Complete system design
- Component architecture
- Design pattern recommendations
- Trade-off analysis
- Scalability considerations

**Benefits**:
- Consistent architecture patterns
- Well-documented decisions
- Scalability from day one
- Clear technical direction

---

### 2. Plan Complex Projects with Hybrid Planning

For high-complexity or high-risk projects, use the hybrid planning workflow:

**When to use**:
- Risk level: HIGH or CRITICAL
- Estimated time: >4 hours
- Number of agents: ≥4
- Security-critical changes
- Architecture decisions

**4-Phase Workflow**:

**Phase 1: Strategic Planning** (10-30 min)
- Main LLM + design-simplicity-advisor + project-manager
- Define task assignments, constraints, context

**Phase 2: Implementation Planning** (Parallel, 5-20 min)
- All assigned agents propose 2-3 approaches
- Each includes: Pros, cons, risks, estimates

**Phase 3: Plan Review** (Parallel, 10-20 min)
- Validate technical feasibility
- Detect conflicts
- Synthesize refined plan
- Go/no-go decision

**Phase 4: Execution**
- Execute refined tasks
- Track with telemetry
- Validate completion

See [Hybrid Planning Guide](hybrid-planning.md) for complete documentation.

---

### 3. Optimize Context Engineering

Design efficient prompt architectures using progressive disclosure:

**Example**:
```
"Optimize the prompt architecture for the agent system"
```

**Techniques**:
- Progressive disclosure (show details on demand)
- Metadata-only prompts (93% size reduction)
- Token efficiency optimization
- Scalability to 100+ agents

**Benefits**:
- Reduced token costs
- Faster response times
- Better context management
- System scalability

See [Context Engineering Architecture](context-engineering.md) for details.

---

### 4. Implement Adaptive Systems

Design systems that learn and improve over time:

**Framework**:
- Continuous improvement loop
- Root cause analysis
- A/B testing
- Learning from telemetry

**Example**:
```
"Design an adaptive system for agent selection based on performance data"
```

See [Adaptive System Design](adaptive-system-design.md) for complete framework.

---

## Architecture Patterns

### Multi-Agent Coordination Patterns

#### 1. Sequential Quality Gates (Simplified)
```
Implementation → quality-gate (unified) → git-workflow-manager
```

**When to use**:
- Standard development tasks
- Single domain
- Low to medium complexity

**Benefits**:
- 75% workflow reduction
- Consistent quality validation
- Fast execution

---

#### 2. Parallel Analysis
```
[Agent A + Agent B + Agent C] → Main LLM synthesis
```

**When to use**:
- Multiple independent analyses needed
- Cross-domain validation
- Comprehensive assessment

**Example**:
```
Security audit:
  [security-auditor + dependency-scanner + quality-gate]
  → Main LLM comprehensive report
```

---

#### 3. Hybrid Planning (Complex)
```
Phase 1: Strategic Planning
  Main LLM + design-simplicity-advisor + project-manager
    ↓
Phase 2: Implementation Planning (Parallel)
  All assigned agents propose options
    ↓
Phase 3: Plan Review (Parallel)
  project-manager + product-strategist + design-simplicity-advisor
    ↓
Phase 4: Execution
  Execute refined plan
```

**When to use**:
- HIGH/CRITICAL risk
- >4 hours estimated
- ≥4 agents required
- Security-critical
- Architecture decisions

See [Hybrid Planning Guide](hybrid-planning.md) for decision matrix.

---

### Domain-Specific Patterns

#### Frontend Pattern
```
Request → Domain: Frontend
  ↓
frontend-developer (React/Vue/TypeScript)
  ↓
quality-gate (UI/UX validation)
  ↓
git-workflow-manager
```

**Preferences**:
- TypeScript over JavaScript
- Functional over OOP
- Vue > React > Angular
- Modern state management

---

#### Backend Pattern
```
Request → Domain: Backend
  ↓
backend-architect (Go/TypeScript/JavaScript)
  ↓
quality-gate (API/database validation)
  ↓
git-workflow-manager
```

**Preferences**:
- Go > TypeScript > JavaScript
- SOA thinking
- REST > GraphQL (unless justified)
- Functional over OOP

---

#### Infrastructure Pattern
```
Request → Domain: Infrastructure
  ↓
infrastructure-specialist (AWS CDK)
  ↓
security-auditor (IAM validation)
  ↓
quality-gate (infrastructure review)
  ↓
git-workflow-manager
```

**Preferences**:
- TypeScript/CDK > Go/CDK > Python/CDK
- Lambda > ECS > K8s
- Serverless-first thinking

---

#### Security Pattern
```
Request → Domain: Security (HIGH priority)
  ↓
security-auditor (threat modeling)
  +
dependency-scanner (supply chain)
  +
quality-gate (OWASP compliance)
  ↓
Main LLM synthesis → Comprehensive report
```

**Security-first principle**:
- Security overrides performance/convenience
- Automatic security audits for sensitive changes
- Threat modeling for new features

---

## System Design Principles

### 1. KISS Principle (Keep It Simple, Stupid)

**Enforcement**:
- design-simplicity-advisor analyzes ALL implementations
- quality-gate includes simplicity validation
- Complexity requires explicit justification

**Example**:
```
Over-engineered solution: Custom OAuth2 implementation
Simple solution: Use battle-tested library (Passport.js)

System recommends: Simple solution
Exception: Zero-dependency requirement → Minimal OAuth2 subset
```

---

### 2. Progressive Disclosure

**Concept**: Show information only when needed

**Application**:
- Agent prompts use metadata-only format
- Full details loaded on demand
- 93% prompt size reduction
- Scalable to 100+ agents

See [Context Engineering](context-engineering.md) for implementation.

---

### 3. Deferred Optimization

**Principle**: Don't optimize prematurely

**Application**:
- Implement simple solution first
- Measure before optimizing
- Optimize only proven bottlenecks
- Use telemetry to identify needs

---

### 4. Security-First Architecture

**Principle**: Security cannot be an afterthought

**Application**:
- Automatic security audits for sensitive changes
- Security overrides convenience
- Threat modeling for new features
- OWASP compliance validation

---

### 5. Domain-Driven Design

**Principle**: Align code with business domains

**Application**:
- Agents organized by domain
- Domain-specific routing
- Cross-domain coordination when needed
- Clear domain boundaries

---

## Model Selection Architecture

### Tiered Model Strategy

**Premium Tier (Opus)** - Strategic planning
```
Use cases:
  - System architecture design
  - Complex trade-off analysis
  - Business-critical decisions
  - Nuanced stakeholder management

Agents:
  - systems-architect
  - design-simplicity-advisor
  - project-manager
  - product-strategist
  - business-analyst
  - agent-auditor

Cost: $15-75/M tokens | Speed: 3-5s
```

---

**Balanced Tier (Sonnet)** - Standard development
```
Use cases:
  - Code generation
  - Debugging and refactoring
  - Analysis and documentation
  - Quality validation

Agents:
  - frontend-developer
  - backend-architect
  - infrastructure-specialist
  - security-auditor
  - quality-gate
  - Most other agents

Cost: $3-15/M tokens | Speed: 1-2s
```

---

**Fast Tier (Haiku)** - Execution tasks
```
Use cases:
  - Git operations
  - Test generation
  - Template rendering
  - Procedural tasks

Agents:
  - git-workflow-manager
  - unit-test-expert
  - qa-specialist
  - technical-writer
  - general-purpose

Cost: $1-5/M tokens | Speed: 300-500ms
```

**Result**: 21% cost savings vs all-Sonnet

See [Model Selection Strategy](../../../MODEL_SELECTION_STRATEGY.md) for complete analysis.

---

## Workflow Telemetry Architecture

### Phase 2A Implementation

**Features**:
- Workflow ID linking related invocations
- Parent invocation ID tracking sequences
- Duration and status tracking
- Query tools for analysis

**Schema**:
```json
{
  "invocation_id": "inv-20251022-abc123",
  "workflow_id": "wf-20251022-def456",
  "parent_invocation_id": "inv-20251022-xyz789",
  "agent_name": "backend-architect",
  "duration_seconds": 120.5,
  "status": "success",
  "timestamp": "2025-10-22T14:30:00Z"
}
```

**Query workflows**:
```bash
./scripts/query_workflow.sh wf-20251022-def456
```

See [Technical Reference](../engineers/technical-reference.md#workflow-tracking-system) for details.

---

### Future Enhancements (Phase 2B+)

**Phase 2B** (After 10+ workflows):
- Workflow duration statistics
- Agent performance metrics
- Bottleneck identification
- Success rate tracking

**Phase 2C** (After 50+ workflows):
- Confidence scoring for agent selection
- Historical performance-based recommendations
- Workflow pattern optimization
- Predictive duration estimates

**Phase 3+**:
- Structured artifact files
- Real-time monitoring
- Automated optimization
- ML-based agent selection

---

## Capability Gap Detection

### Automatic Agent Creation

**When gaps are detected**:
- User explicitly requests new capability
- Classification succeeds but no agent matches domain
- 10+ routing failures for same domain
- Pattern of suboptimal routing

**Process**:
```
1. Gap detection (automatic or explicit)
2. agent-creator designs specification
3. Agent saved to agents/pending_review/
4. User reviews and approves
5. Agent deployed and registered
6. System monitors performance
```

**Examples**:
- Financial analysis capability → financial-analyst
- Research tasks → research-specialist
- Product roadmapping → product-manager-strategist

See [Engineers Guide](../engineers/README.md) for implementation details.

---

## Architecture Decision Records

### ADR-001: Unified Quality Gate

**Decision**: Consolidate 4 sequential quality agents into single quality-gate

**Rationale**:
- 75% workflow reduction
- Faster execution
- Consistent validation
- Simpler coordination

**Status**: Implemented (October 2025)

**Impact**:
- code-reviewer archived
- code-clarity-manager archived
- top-down-analyzer archived
- bottom-up-analyzer archived

---

### ADR-002: Tiered Model Selection

**Decision**: Assign agents to Premium/Balanced/Fast tiers based on task complexity

**Rationale**:
- 21% cost savings
- 3-10x faster execution for Fast tier
- Better strategic decisions from Premium tier
- Optimal balance for majority

**Status**: Implemented

**Impact**: All agents assigned to optimal tiers

---

### ADR-003: Hybrid Planning for Complex Projects

**Decision**: Implement 4-phase planning workflow for high-risk/complex tasks

**Rationale**:
- Early conflict detection
- Better time estimates
- Risk mitigation
- Optimized solutions

**Status**: Implemented (Phase 3)

**Triggers**: HIGH/CRITICAL risk, >4 hours, ≥4 agents, security-critical, architecture decisions

---

### ADR-004: Domain-Specific Routing

**Decision**: Use domain-aware agent routing with confidence scoring

**Rationale**:
- Context-aware routing
- Specialized workflows
- Tech stack best practices
- Faster execution

**Status**: Implemented

**Impact**: Frontend, Backend, Infrastructure, Security, Data domains active

---

## Common Architecture Questions

### How do I decide between simple delegation and hybrid planning?

Use the decision matrix:

**MANDATORY hybrid planning**:
- Risk: HIGH or CRITICAL
- Time: >4 hours
- Agents: ≥4
- Security-critical: Yes

**RECOMMENDED hybrid planning**:
- Complexity: HIGH + Novelty: HIGH
- Domains: ≥2 + Integration: HIGH
- Cost of failure: >2 hours rework

**SKIP hybrid planning**:
- Simple tasks
- Well-understood patterns
- Low-risk changes
- Bug fixes (unless security)

See [Hybrid Planning Guide](hybrid-planning.md) for complete decision matrix.

---

### How do I optimize for cost?

**System-level**:
- Trust model tier assignments (already optimized)
- Use Fast tier for procedural tasks
- Leverage Premium tier for strategic decisions

**Workflow-level**:
- Use spec-driven development (prevents rework)
- Leverage hybrid planning (prevents expensive mistakes)
- Monitor telemetry for inefficiencies

**Result**: 21% cost savings vs all-Sonnet baseline

---

### How do I design for scalability?

**Prompt architecture**:
- Use metadata-only prompts (93% reduction)
- Progressive disclosure pattern
- Scalable to 100+ agents

**Agent architecture**:
- Domain-specific specialization
- Clear boundaries and responsibilities
- Minimal overlap and redundancy

**Workflow architecture**:
- Parallel execution when possible
- Efficient coordination patterns
- Telemetry-driven optimization

---

### How do I ensure quality at scale?

**Automated validation**:
- quality-gate for all implementations
- Security audits for sensitive changes
- Test coverage validation

**Workflow enforcement**:
- Pre-commit validation hooks
- Workflow state tracking
- Mandatory quality gates

**Continuous improvement**:
- Telemetry analysis
- agent-auditor monthly reviews
- Adaptive system learning

---

## Next Steps

**System design deep dive**: Read [System Design](system-design.md)

**Complex project planning**: Study [Hybrid Planning Guide](hybrid-planning.md)

**Prompt optimization**: Review [Context Engineering](context-engineering.md)

**Continuous improvement**: See [Adaptive System Design](adaptive-system-design.md)

---

**Ready to architect?** Start with [System Design](system-design.md) for complete architecture overview!
