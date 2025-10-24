# Documentation Index

**Find the right documentation for your role and needs**

This index organizes all documentation by audience to help you quickly find what you need.

---

## Quick Navigation

### 👤 I am a...

- **[Product Manager](#for-product-managers)** - Specs, prototypes, and product strategy
- **[Engineer](#for-engineers)** - Implementation, architecture, and technical details
- **[Team Lead / Manager](#for-team-leads--managers)** - Setup, adoption, and team workflows
- **[Researcher / Architect](#for-researchers--architects)** - System design, advanced patterns, and research

### 🎯 I want to...

- **[Get started quickly](#quick-start)** - 5-10 minute setup
- **[Understand the system](#understanding-the-system)** - What it is and how it works
- **[Learn specific workflows](#workflow-guides)** - Step-by-step patterns
- **[Dive deep technically](#technical-deep-dives)** - System internals and architecture

---

## For Product Managers

**Co-author specs, design schemas, create prototypes, and deliver professional engineering handoffs**

### Getting Started (10 minutes)
1. **[PM Quick Start](PM_QUICK_START.md)** ⭐ START HERE
   - 6 detailed examples with step-by-step walkthroughs
   - Spec authoring, database design, UI prototyping
   - Git workflows and product strategy

### Workflow Patterns
2. **[PM Workflows](PM_WORKFLOWS.md)**
   - 7 reusable workflow patterns
   - Template prompts for each pattern
   - Agent coordination examples
   - Workflow combinations

### Capabilities Reference
3. **[PM Capabilities](PM_CAPABILITIES.md)**
   - Honest assessment of what works today
   - What requires manual work
   - Roadmap for future capabilities
   - Capability matrix by domain

### See Also
- [User Guide](../USER_GUIDE.md) - General system overview
- [README](../README.md) - Project introduction

---

## For Engineers

**Specialized code generation, automatic quality gates, and multi-agent coordination**

### Getting Started (5 minutes)
1. **[Quick Start](../QUICK_START.md)** ⭐ START HERE
   - Installation (3 commands)
   - First agent invocation
   - Verification steps

2. **[User Guide](../USER_GUIDE.md)**
   - System overview
   - Key concepts
   - Common use cases
   - Workflow examples

### Technical Reference
3. **[Technical Reference](technical/TECHNICAL_REFERENCE.md)** ⭐ COMPREHENSIVE
   - Workflow tracking system
   - Success metrics reference
   - Adaptive system design
   - Metadata-only prompts architecture

### Architecture & Design
4. **[Model Selection Strategy](MODEL_SELECTION_STRATEGY.md)**
   - Premium/Balanced/Fast tiers
   - When to override model tier
   - Expected cost/performance impact

5. **[Hybrid Planning Guide](HYBRID_PLANNING_GUIDE.md)**
   - Multi-agent planning workflow
   - When to use hybrid vs simple delegation
   - Phase 1-4 planning process
   - Decision matrix for workflow selection

### Implementation Guides
6. **[Migration Guide](MIGRATION_GUIDE.md)**
   - Upgrading from older versions
   - Breaking changes
   - Migration paths

7. **[Multi-File Agents](MULTI_FILE_AGENTS.md)**
   - Advanced agent packaging
   - Bundled scripts (10-100x faster)
   - Modular agent structure

### Production & Validation
8. **[Production Validation Plan](PRODUCTION_VALIDATION_PLAN.md)**
   - Testing strategy
   - Validation checkpoints
   - Rollout plan

### See Also
- [CLAUDE.md](../CLAUDE.md) - System rules and agent coordination
- [README](../README.md) - Project overview

---

## For Team Leads / Managers

**Setup, adoption strategy, and team productivity**

### Getting Started
1. **[README](../README.md)** ⭐ START HERE
   - Project overview
   - Value proposition
   - Quick installation

2. **[User Guide](../USER_GUIDE.md)**
   - What is OaK Agents?
   - Who is it for?
   - Value proposition
   - ROI calculations

### Adoption & Rollout
3. **[Production Validation Plan](PRODUCTION_VALIDATION_PLAN.md)**
   - Team rollout strategy
   - Validation checkpoints
   - Risk mitigation

4. **[Success Metrics Reference](technical/TECHNICAL_REFERENCE.md#success-metrics-reference)**
   - How to measure success
   - Primary/secondary indicators
   - Monthly checklist

### Team Workflows
5. **[PM Workflows](PM_WORKFLOWS.md)**
   - Reusable team patterns
   - Workflow combinations
   - Best practices

6. **[Hybrid Planning Guide](HYBRID_PLANNING_GUIDE.md)**
   - Multi-agent coordination for complex projects
   - When to use structured planning
   - Team collaboration patterns

### See Also
- [PM Capabilities](PM_CAPABILITIES.md) - What works today vs roadmap
- [Model Selection Strategy](MODEL_SELECTION_STRATEGY.md) - Cost optimization

---

## For Researchers / Architects

**System design, advanced patterns, architecture decisions, and research**

### Architecture Documents
1. **[OaK Architecture](oak-design/OAK_ARCHITECTURE.md)** ⭐ START HERE
   - Complete system design
   - Component architecture
   - Design principles

2. **[Implementation Guide](oak-design/IMPLEMENTATION_GUIDE.md)**
   - Integration patterns
   - Extension points
   - Development workflow

3. **[6-Month Deployment Plan](oak-design/6_MONTH_DEPLOYMENT_PLAN.md)**
   - Phased rollout strategy
   - Milestones and deliverables
   - Timeline and dependencies

### Advanced System Design
4. **[Context Engineering Architecture](CONTEXT_ENGINEERING_ARCHITECTURE.md)**
   - Prompt optimization
   - Context management
   - Token efficiency

5. **[Hybrid Planning Guide](HYBRID_PLANNING_GUIDE.md)**
   - Bottom-up + top-down planning
   - Phase 1-4 workflow
   - Agent mode specifications

6. **[Adaptive System Design](technical/TECHNICAL_REFERENCE.md#adaptive-system-design)**
   - Continuous improvement loop
   - Root cause analysis
   - A/B testing framework
   - Learning and evolution

### Performance & Optimization
7. **[Model Selection Strategy](MODEL_SELECTION_STRATEGY.md)**
   - Premium/Balanced/Fast tier assignments
   - Cost-performance tradeoffs
   - 21% cost savings analysis

8. **[Metadata-Only Prompts](technical/TECHNICAL_REFERENCE.md#metadata-only-prompts)**
   - Progressive disclosure architecture
   - 93% prompt size reduction
   - Scalability to 100+ agents

9. **[Workflow Tracking System](technical/TECHNICAL_REFERENCE.md#workflow-tracking-system)**
   - Multi-agent coordination telemetry
   - Phase 2A implementation
   - Query and analysis tools

### Research & Experimentation
10. **[Multi-File Agents](MULTI_FILE_AGENTS.md)**
    - Advanced agent packaging
    - Bundled scripts architecture
    - Anthropic Skills parity

11. **[Production Validation Plan](PRODUCTION_VALIDATION_PLAN.md)**
    - Validation methodology
    - Testing strategy
    - Quality gates

### See Also
- [Technical Reference](technical/TECHNICAL_REFERENCE.md) - Consolidated technical docs
- [CLAUDE.md](../CLAUDE.md) - System coordination rules

---

## Quick Start

### For Everyone (5 Minutes)

**Installation**:
```bash
# 1. Clone repository
git clone https://github.com/robertmnyborg/claude-oak-agents.git ~/Projects/claude-oak-agents
cd ~/Projects/claude-oak-agents

# 2. Link agents
mkdir -p ~/.claude/agents
ln -s ~/Projects/claude-oak-agents/agents/* ~/.claude/agents/

# 3. Install automation (optional)
./automation/install_automation.sh
```

**First Use**:
- Just use Claude Code normally
- Agents work automatically
- No configuration needed

**Next Steps**:
- **PM**: Read [PM Quick Start](PM_QUICK_START.md)
- **Engineer**: Read [User Guide](../USER_GUIDE.md)
- **Researcher**: Read [OaK Architecture](oak-design/OAK_ARCHITECTURE.md)

---

## Understanding the System

### Core Concepts

**What is OaK Agents?**
A self-learning agent system for Claude Code that provides 29+ specialized AI assistants for software development.

**Key Features**:
- **Specialized Agents** - Frontend, backend, security, infrastructure, PM, etc.
- **Auto Learning** - Tracks patterns and improves over time
- **Quality Gates** - Automatic checks before commits
- **Gap Detection** - Creates new agents when needed
- **Workflow Tracking** - Links multi-agent coordination

**Read More**:
- [User Guide](../USER_GUIDE.md#key-concepts)
- [README](../README.md#what-you-can-actually-do)

### How It Works

**Request Flow**:
```
User Request
  ↓
Main LLM Classification
  ↓
Domain Identification
  ↓
Agent Selection
  ↓
Execution (single or multi-agent)
  ↓
Quality Gate (automatic)
  ↓
Git Operations (if code changes)
```

**Read More**:
- [CLAUDE.md](../CLAUDE.md#persistent-rules)
- [Hybrid Planning Guide](HYBRID_PLANNING_GUIDE.md)

---

## Workflow Guides

### PM Workflows
- **[PM Quick Start](PM_QUICK_START.md)** - 6 detailed examples
- **[PM Workflows](PM_WORKFLOWS.md)** - 7 reusable patterns
- **[PM Capabilities](PM_CAPABILITIES.md)** - Capability matrix

### Engineering Workflows
- **[User Guide](../USER_GUIDE.md#workflow-examples)** - Common patterns
- **[Hybrid Planning](HYBRID_PLANNING_GUIDE.md)** - Complex projects
- **[Technical Reference](technical/TECHNICAL_REFERENCE.md)** - Advanced patterns

---

## Technical Deep Dives

### System Internals
- **[Technical Reference](technical/TECHNICAL_REFERENCE.md)** - Complete technical documentation
- **[OaK Architecture](oak-design/OAK_ARCHITECTURE.md)** - System design
- **[Context Engineering](CONTEXT_ENGINEERING_ARCHITECTURE.md)** - Prompt architecture

### Performance & Optimization
- **[Model Selection Strategy](MODEL_SELECTION_STRATEGY.md)** - Cost optimization
- **[Metadata-Only Prompts](technical/TECHNICAL_REFERENCE.md#metadata-only-prompts)** - 93% reduction
- **[Multi-File Agents](MULTI_FILE_AGENTS.md)** - Bundled scripts (10-100x faster)

### Advanced Patterns
- **[Hybrid Planning](HYBRID_PLANNING_GUIDE.md)** - Multi-phase planning
- **[Workflow Tracking](technical/TECHNICAL_REFERENCE.md#workflow-tracking-system)** - Coordination telemetry
- **[Adaptive System](technical/TECHNICAL_REFERENCE.md#adaptive-system-design)** - Continuous improvement

---

## Document Status Key

- ⭐ **START HERE** - Recommended entry point for your role
- 📋 **COMPLETE** - Comprehensive documentation
- 🚧 **IN PROGRESS** - Actively being developed
- 📌 **REFERENCE** - Quick reference / cheat sheet

---

## Contributing to Documentation

Found an issue or want to improve documentation?

1. **Typos / Fixes**: Open a PR with the fix
2. **New Content**: Open an issue to discuss first
3. **Clarifications**: Open an issue with your question

**Guidelines**:
- Keep PM docs non-technical
- Link between related docs
- Include concrete examples
- Update this INDEX when adding new docs

---

## Documentation Structure

```
docs/
├── INDEX.md                          # This file
├── PM_QUICK_START.md                 # PM examples (⭐ PM start)
├── PM_WORKFLOWS.md                   # PM patterns
├── PM_CAPABILITIES.md                # Capability matrix
│
├── technical/
│   └── TECHNICAL_REFERENCE.md        # Consolidated tech reference
│
├── oak-design/
│   ├── OAK_ARCHITECTURE.md           # System design (⭐ Researcher start)
│   ├── IMPLEMENTATION_GUIDE.md       # Integration guide
│   └── 6_MONTH_DEPLOYMENT_PLAN.md    # Rollout plan
│
├── HYBRID_PLANNING_GUIDE.md          # Multi-agent planning
├── MODEL_SELECTION_STRATEGY.md       # Cost optimization
├── CONTEXT_ENGINEERING_ARCHITECTURE.md  # Prompt architecture
├── MULTI_FILE_AGENTS.md              # Advanced packaging
├── MIGRATION_GUIDE.md                # Upgrade guide
└── PRODUCTION_VALIDATION_PLAN.md     # Validation strategy

../
├── README.md                         # Project overview (⭐ Everyone start)
├── QUICK_START.md                    # 5-min setup (⭐ Engineer start)
├── USER_GUIDE.md                     # General guide
└── CLAUDE.md                         # System rules
```

---

**Need help finding something?** [Open an issue](https://github.com/robertmnyborg/claude-oak-agents/issues) and we'll help you navigate!
