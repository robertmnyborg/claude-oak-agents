# Documentation Index

**Navigate claude-oak-agents documentation by role, task, or reference**

This index organizes all documentation to help you quickly find what you need based on your role or what you want to accomplish.

---

## Quick Start

**New to claude-oak-agents?** Start here:

- **[Getting Started Guide](getting-started/README.md)** - Installation and first workflows (5-10 minutes)
- **[Main README](../README.md)** - Project overview and quick start
- **[User Guide](../USER_GUIDE.md)** - System overview and key concepts

---

## By Role

### Product Managers

**Navigate**: [Product Manager Guide](by-role/product-managers/README.md)

**Co-author specs, design schemas, create prototypes, deliver engineering handoffs**

#### Getting Started
- **[PM Quick Start](by-role/product-managers/quick-start.md)** - 6 detailed examples (10 minutes)
  - Co-author feature specs
  - Design database schemas
  - Create UI prototypes
  - Map user workflows
  - Translate business strategy
  - Manage Git workflows

#### Workflows
- **[PM Workflows](by-role/product-managers/workflows.md)** - 7 reusable patterns
  - Spec-driven development
  - Quick iteration
  - Database and API design
  - Security-first patterns
  - Multi-agent coordination

#### Reference
- **[PM Capabilities](by-role/product-managers/capabilities.md)** - Honest capability assessment
  - What works today
  - What requires manual work
  - Roadmap and limitations

---

### Engineers

**Navigate**: [Engineers Guide](by-role/engineers/README.md)

**Specialized code generation, automatic quality gates, multi-agent coordination**

#### Getting Started
- **[Installation](getting-started/README.md#for-engineers)** - 5-minute setup
- **[First Workflow](getting-started/README.md#for-engineers)** - Implement your first feature

#### Technical Reference
- **[Technical Reference](by-role/engineers/technical-reference.md)** - System internals
  - Workflow tracking system
  - Success metrics reference
  - Adaptive system design
  - Metadata-only prompts

#### Development
- **[Agent Development](by-role/engineers/agent-development.md)** - Create custom agents
  - Multi-file agents
  - Bundled scripts (10-100x faster)
  - Agent packaging

#### Architecture
- **[Model Selection Strategy](MODEL_SELECTION_STRATEGY.md)** - Cost optimization
  - Premium/Balanced/Fast tiers
  - Performance vs cost tradeoffs
  - 21% cost savings

---

### Architects

**Navigate**: [Architects Guide](by-role/architects/README.md)

**System design, advanced patterns, architecture decisions**

#### Core Architecture
- **[System Design](by-role/architects/system-design.md)** - Complete OaK architecture
  - Component architecture
  - Design principles
  - System internals

#### Advanced Planning
- **[Hybrid Planning Guide](by-role/architects/hybrid-planning.md)** - Multi-agent coordination
  - 4-phase planning workflow
  - Decision matrix
  - When to use hybrid vs simple

#### System Optimization
- **[Context Engineering](by-role/architects/context-engineering.md)** - Prompt architecture
  - Progressive disclosure
  - 93% prompt size reduction
  - Scalability to 100+ agents

- **[Adaptive System Design](by-role/architects/adaptive-system-design.md)** - Continuous improvement
  - Learning and evolution
  - Root cause analysis
  - A/B testing framework

#### Implementation
- **[Implementation Guide](oak-design/IMPLEMENTATION_GUIDE.md)** - Integration patterns
- **[Deployment Plan](oak-design/6_MONTH_DEPLOYMENT_PLAN.md)** - Phased rollout

---

## By Task

### Feature Development

**Navigate**: [Feature Development Guide](by-task/feature-development/README.md)

**End-to-end feature development workflows**

- **[Workflow Patterns](by-task/feature-development/workflow-patterns.md)** - Common patterns
- **[Spec-Driven Development](by-task/feature-development/README.md#spec-driven-workflow)** - Specification-first approach
- **[Quick Iteration](by-task/feature-development/README.md#quick-iteration-workflow)** - Rapid prototyping

**Common workflows**:
- Full-stack features
- UI-only features
- Backend services
- Database and API design
- Infrastructure deployment

---

### Security

**Security-first development patterns**

**Coming soon**: Security workflow guide

**Related documentation**:
- Security auditor in [PM Capabilities](by-role/product-managers/capabilities.md)
- Security patterns in [PM Workflows](by-role/product-managers/workflows.md)
- Security-first architecture in [Architects Guide](by-role/architects/README.md)

**Key agents**:
- **security-auditor**: Penetration testing, OWASP compliance
- **dependency-scanner**: Supply chain security, vulnerabilities

---

### Data

**Database design, migrations, ETL patterns**

**Coming soon**: Data workflow guide

**Related documentation**:
- Database design in [PM Quick Start](by-role/product-managers/quick-start.md)
- Database patterns in [PM Workflows](by-role/product-managers/workflows.md)
- Data architecture in [Feature Development](by-task/feature-development/README.md)

**Key agents**:
- **backend-architect**: Schema design, migrations, optimization

---

## Reference

### Agents

**All agent documentation and specifications**

**Core agents**:
- **Product Management**: spec-manager, product-strategist, business-analyst
- **Development**: frontend-developer, backend-architect, infrastructure-specialist
- **Quality**: quality-gate, security-auditor, unit-test-expert, qa-specialist
- **Workflow**: git-workflow-manager, project-manager
- **Special Purpose**: design-simplicity-advisor, debug-specialist, agent-creator

**See**: [Main README](../README.md#29-specialized-agents) for complete agent list

**Agent documentation location**: `/Users/robertnyborg/Projects/claude-oak-agents/agents/`

---

### Workflows

**Workflow patterns and coordination**

- **[Workflow Patterns](by-task/feature-development/workflow-patterns.md)** - Development patterns
- **[PM Workflows](by-role/product-managers/workflows.md)** - PM-focused patterns
- **[Hybrid Planning](by-role/architects/hybrid-planning.md)** - Complex coordination

**Common patterns**:
- Spec-driven development
- Quick iteration
- Multi-agent coordination
- Parallel execution
- Sequential execution

---

### Templates

**Reusable templates and patterns**

**Coming soon**: Template library

**Related documentation**:
- Spec templates in spec-manager agent
- Component templates in frontend-developer agent
- Infrastructure templates in infrastructure-specialist agent

**Template locations**:
- **Specs**: `specs/templates/`
- **Agents**: `agents/` (each agent includes templates)

---

### API

**Telemetry API and integration points**

**Coming soon**: API reference guide

**Related documentation**:
- [Technical Reference](by-role/engineers/technical-reference.md#workflow-tracking-system)
- Telemetry integration in agent development

**Telemetry API**:
- Workflow tracking
- Agent invocations
- Performance metrics
- Query tools

**Location**: `telemetry/` directory

---

## Documentation by Topic

### Installation and Setup
- [Getting Started](getting-started/README.md)
- [Main README](../README.md#quick-start-5-minutes)
- [User Guide](../USER_GUIDE.md)

### Quick Start Guides
- [PM Quick Start](by-role/product-managers/quick-start.md)
- [Engineers Quick Start](getting-started/README.md#for-engineers)
- [Architects Quick Start](getting-started/README.md#for-architects)

### Workflow Guides
- [PM Workflows](by-role/product-managers/workflows.md)
- [Feature Development Workflows](by-task/feature-development/README.md)
- [Workflow Patterns](by-task/feature-development/workflow-patterns.md)

### Technical Documentation
- [Technical Reference](by-role/engineers/technical-reference.md)
- [System Design](by-role/architects/system-design.md)
- [Agent Development](by-role/engineers/agent-development.md)

### Architecture and Design
- [System Design](by-role/architects/system-design.md)
- [Hybrid Planning](by-role/architects/hybrid-planning.md)
- [Context Engineering](by-role/architects/context-engineering.md)
- [Adaptive System Design](by-role/architects/adaptive-system-design.md)

### Capabilities and Limitations
- [PM Capabilities](by-role/product-managers/capabilities.md)
- [Model Selection Strategy](MODEL_SELECTION_STRATEGY.md)

### Migration and Updates
- [Migration Guide](MIGRATION_GUIDE.md)
- [Production Validation Plan](PRODUCTION_VALIDATION_PLAN.md)

---

## Old Structure (Deprecated)

The following files have been moved to the new structure:

**Moved to by-role/product-managers/**:
- ~~PM_QUICK_START.md~~ → [quick-start.md](by-role/product-managers/quick-start.md)
- ~~PM_WORKFLOWS.md~~ → [workflows.md](by-role/product-managers/workflows.md)
- ~~PM_CAPABILITIES.md~~ → [capabilities.md](by-role/product-managers/capabilities.md)

**Moved to by-role/engineers/**:
- ~~technical/TECHNICAL_REFERENCE.md~~ → [technical-reference.md](by-role/engineers/technical-reference.md)
- ~~MULTI_FILE_AGENTS.md~~ → [agent-development.md](by-role/engineers/agent-development.md)

**Moved to by-role/architects/**:
- ~~CONTEXT_ENGINEERING_ARCHITECTURE.md~~ → [context-engineering.md](by-role/architects/context-engineering.md)
- ~~HYBRID_PLANNING_GUIDE.md~~ → [hybrid-planning.md](by-role/architects/hybrid-planning.md)
- ~~ADAPTIVE_SYSTEM_DESIGN.md~~ → [adaptive-system-design.md](by-role/architects/adaptive-system-design.md)
- ~~oak-design/OAK_ARCHITECTURE.md~~ → [system-design.md](by-role/architects/system-design.md)

**Moved to by-task/feature-development/**:
- ~~WORKFLOW_PATTERNS.md~~ → [workflow-patterns.md](by-task/feature-development/workflow-patterns.md)

**Backward compatibility**: Symlinks will be created for old paths in a future update.

---

## Search by Keywords

### By Technology
- **React/Vue/Angular**: [Frontend Development](by-role/engineers/README.md#frontend-pattern)
- **Node.js/Go**: [Backend Development](by-role/engineers/README.md#backend-pattern)
- **AWS/CDK/Lambda**: [Infrastructure](by-role/engineers/README.md#infrastructure-pattern)
- **PostgreSQL/MongoDB**: [Database Design](by-task/feature-development/README.md#database-and-api-design-workflow)

### By Activity
- **Creating specs**: [PM Quick Start](by-role/product-managers/quick-start.md), [spec-manager](by-role/product-managers/README.md)
- **Designing databases**: [Backend Architect](by-role/product-managers/README.md#2-design-database-schemas)
- **Building prototypes**: [Frontend Developer](by-role/product-managers/README.md#3-create-ui-prototypes)
- **Git workflows**: [git-workflow-manager](by-role/product-managers/README.md#6-manage-git-workflows)
- **Security audits**: [Security Patterns](by-role/architects/README.md#security-pattern)

### By Complexity
- **Simple tasks**: [Quick Iteration](by-task/feature-development/README.md#quick-iteration-workflow)
- **Significant features**: [Spec-Driven](by-task/feature-development/README.md#spec-driven-workflow)
- **Complex projects**: [Hybrid Planning](by-role/architects/hybrid-planning.md)

### By Role Activity
- **PM prototyping**: [PM Quick Start](by-role/product-managers/quick-start.md)
- **Engineer implementation**: [Engineers Guide](by-role/engineers/README.md)
- **Architect design**: [System Design](by-role/architects/system-design.md)

---

## Contributing to Documentation

Found an issue or want to improve documentation?

1. **Typos/Fixes**: Open a PR with the fix
2. **New Content**: Open an issue to discuss first
3. **Clarifications**: Open an issue with your question

**Guidelines**:
- Keep PM docs non-technical
- Link between related docs
- Include concrete examples
- Update this INDEX when adding new docs

**Documentation structure**:
```
docs/
├── INDEX.md (this file)
├── getting-started/
│   └── README.md
├── by-role/
│   ├── product-managers/
│   ├── engineers/
│   └── architects/
├── by-task/
│   ├── feature-development/
│   ├── security/
│   └── data/
└── reference/
    ├── agents/
    ├── workflows/
    ├── templates/
    └── api/
```

---

## Document Status

**Status indicators**:
- ✅ **Complete** - Comprehensive documentation available
- 🚧 **In Progress** - Actively being developed
- 📋 **Planned** - Coming soon
- 🔄 **Updated** - Recently reorganized

**Current status**:
- ✅ Getting Started Guide
- ✅ Product Manager documentation
- ✅ Engineers documentation
- ✅ Architects documentation
- ✅ Feature Development workflows
- 🚧 Security workflows (coming soon)
- 🚧 Data workflows (coming soon)
- 📋 Template library (planned)
- 📋 API reference (planned)

---

## Need Help?

**Can't find what you're looking for?**

1. **Check by role**: [Product Managers](#product-managers) | [Engineers](#engineers) | [Architects](#architects)
2. **Check by task**: [Feature Development](#feature-development) | [Security](#security) | [Data](#data)
3. **Search by keyword**: [Keywords section](#search-by-keywords)
4. **Ask the community**: [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)
5. **Report missing docs**: [GitHub Issues](https://github.com/robertmnyborg/claude-oak-agents/issues)

---

**Start exploring**: Choose your role above or jump to [Getting Started](getting-started/README.md)!
