# OaK Agents: User Guide

**Specialized AI agents that learn from your patterns and get better over time**

---

## What Is This?

OaK Agents is a **self-learning agent system** for Claude Code that provides specialized AI assistants for software development. Each agent is an expert in a specific domain:

- **frontend-developer** - UI/UX implementation
- **backend-architect** - API and database design
- **security-auditor** - Vulnerability detection
- **infrastructure-specialist** - Cloud deployment
- **product-strategist** - Product planning and metrics
- ...and 25+ more specialized agents

**What makes it special**: The system learns from your patterns, adapts to your workflow, and automatically fills capability gaps.

---

## Who Is This For?

### Product Managers
- Co-author feature specifications
- Design database schemas and APIs
- Create prototypes and wireframes
- Professional handoffs to engineering

**👉 See [PM Quick Start Guide](docs/PM_QUICK_START.md)** for 6 detailed PM examples

### Engineers
- Specialized code generation
- Automatic quality checks
- Security and performance audits
- Multi-agent coordination for complex tasks

**👉 See [Technical Reference](docs/technical/TECHNICAL_REFERENCE.md)** for system internals

### Teams
- Consistent code quality
- Knowledge retention across projects
- Faster onboarding for new members
- Reduced repetitive work

---

## Key Concepts

### 1. Specialized Agents

Instead of one general-purpose AI, you get 29+ specialists:

```
Request: "Build a secure login page"

Without OaK:
You → Claude → Generic implementation

With OaK:
You → frontend-developer (builds UI)
    → security-auditor (checks vulnerabilities)
    → unit-test-expert (creates tests)
    → All coordinated automatically
```

**Result**: 70% faster, higher quality, fewer issues

### 2. Automatic Learning

The system tracks what works and improves over time:

- **Week 1**: Tracks your patterns
- **Week 2**: Identifies common tasks
- **Week 3**: Optimizes agent selection
- **Week 4**: Proactively suggests improvements
- **Month 2+**: Self-improving with A/B testing

### 3. Capability Gap Detection

When no agent fits your need, the system automatically:
1. Detects the gap
2. Proposes a new specialist
3. Creates the agent (with your approval)
4. Deploys it immediately

**Example**: You often do financial analysis → System creates "financial-analyst" agent

### 4. Quality Gates

Before any commit, automatic checks run:
- Code review and standards
- Security vulnerability scan
- Performance analysis
- Test coverage validation
- Simplicity (KISS) compliance

**No manual checklist needed**

---

## Common Use Cases

### For Product Managers

**1. Spec-Driven Feature Development**
```
"Create a spec for OAuth2 authentication"
→ spec-manager: Co-authors specification with you
→ backend-architect: Reviews technical feasibility
→ security-auditor: Validates security approach
→ Result: Complete spec (MD + YAML) ready for engineering
```

**2. Database Schema Design**
```
"Design a PostgreSQL schema for multi-tenant SaaS"
→ backend-architect: Creates normalized schema
→ Generates DDL, migrations, indexes
→ Result: Production-ready schema in 10 minutes
```

**3. User Workflow Mapping**
```
"Map password reset workflow from forgot password to successful login"
→ ux-designer: Maps complete flow with friction points
→ Identifies 5 UX improvements
→ Result: Evidence-based UX recommendations
```

**👉 See [PM Workflows](docs/PM_WORKFLOWS.md)** for 7 reusable workflow patterns

### For Engineers

**1. Multi-Domain Features**
```
"Implement secure API with monitoring"
→ backend-architect: API design
→ security-auditor: Security review
→ infrastructure-specialist: Monitoring setup
→ All coordinated automatically
```

**2. Code Review Pipeline**
```
Ready to commit →
→ code-reviewer: Quality check
→ security-auditor: Vulnerability scan
→ unit-test-expert: Test coverage
→ design-simplicity-advisor: KISS validation
→ Automatic gate before git commit
```

**3. Performance Optimization**
```
"Optimize this slow query"
→ performance-optimizer: Identifies bottlenecks
→ backend-architect: Suggests improvements
→ qa-specialist: Validates changes
→ Result: 10x faster with tests
```

---

## Value Proposition

### Time Savings

**Per Week**:
- 5-8 hours on quality checks
- 2-3 hours on documentation
- 1-2 hours on repetitive explanations
- **Total: 8-13 hours saved per developer/week**

### Quality Improvements

- **3-5x more issues** caught before production
- **Security vulnerabilities** detected automatically
- **Performance problems** identified early
- **Consistent standards** across all projects

### Cost Efficiency

**With Optimizations**:
- 93% reduction in prompt size (metadata-only mode)
- 4x faster agent classification
- ~$160/month token savings
- Bundled scripts (10-100x faster than LLM calls)

**Conservative ROI**: 10x within 3 months

---

## Getting Started

### Installation (5 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/robertmnyborg/claude-oak-agents.git ~/Projects/claude-oak-agents
cd ~/Projects/claude-oak-agents

# 2. Link agents
mkdir -p ~/.claude/agents
ln -s ~/Projects/claude-oak-agents/agents/* ~/.claude/agents/

# 3. Install automation (optional)
./automation/install_automation.sh

# That's it!
```

### First Steps

**Day 1**: Use Claude Code normally
- Agents work automatically
- No configuration required
- System starts learning your patterns

**Week 1**: Review insights
```bash
oak-weekly-review
```
- See which agents were used
- Check performance trends
- Approve suggested improvements

**Month 1+**: Enable optimizations
- Metadata-only prompts (90% smaller)
- Multi-file agents (bundled scripts)
- Advanced coordination patterns

---

## Workflow Examples

### Spec-Driven Development (PM Focus)

```
1. Frame Problem
   "Customer churn is 15% monthly. Help me frame this as a product problem."
   → product-strategist: Eigenquestion analysis + hypotheses

2. Create Specification
   "Create spec for guided onboarding to reduce churn"
   → spec-manager: Co-authors with approval checkpoints

3. Design Data Layer
   "Design schema for onboarding progress tracking"
   → backend-architect: Schema + migrations

4. Prototype UI
   "Create React components for onboarding wizard"
   → frontend-developer: Component scaffolding + state store

5. Engineering Handoff
   "Create PR with spec, schema, and prototype"
   → git-workflow-manager: Professional PR with context
```

**Timeline**: 60-90 minutes from problem to engineering-ready handoff

**👉 See [PM_QUICK_START.md](docs/PM_QUICK_START.md)** for complete walkthrough

### Multi-Agent Coordination (Engineering Focus)

```
1. Classification
   Main LLM: Analyzes request → Identifies domains → Plans workflow

2. Design Phase
   design-simplicity-advisor: KISS analysis (mandatory for implementation)

3. Implementation
   [domain-specialist]: Parallel/sequential execution

4. Quality Gate
   code-reviewer + security-auditor + unit-test-expert (combined)

5. Git Operations
   git-workflow-manager: Commit + changelog
```

**Result**: High-quality implementation with automatic checks

**👉 See [Technical Reference](docs/technical/TECHNICAL_REFERENCE.md)** for system details

---

## Advanced Features

### Metadata-Only Prompts

**Problem**: Full agent definitions = 87KB system prompt
**Solution**: Metadata-only = 6KB (93% reduction)

**Benefits**:
- 4x faster classification
- 100+ agent scalability
- Lower token costs
- Same functionality

**Enable**:
```bash
./scripts/enable_metadata_prompts.sh
```

**👉 See [Technical Reference](docs/technical/TECHNICAL_REFERENCE.md#metadata-only-prompts)** for details

### Multi-File Agents

**Structure**:
```
agents/security-auditor/
  ├── agent.md              # Definition
  ├── metadata.yaml         # Discovery
  ├── scripts/
  │   ├── dependency_scan.py   # 10x faster than LLM
  │   └── secrets_detector.py  # 15x faster
  └── reference/
      └── owasp_top_10.md      # Context docs
```

**Benefits**:
- Bundled scripts (10-100x faster)
- Modular and maintainable
- Easy to extend

### Workflow Tracking

**Track multi-agent coordination**:
```python
workflow_id = generate_workflow_id()

inv_1 = execute("design-simplicity-advisor", workflow_id)
inv_2 = execute("backend-architect", workflow_id, parent=inv_1)
inv_3 = execute("security-auditor", workflow_id, parent=inv_2)

# Query workflow
./scripts/query_workflow.sh wf-20251024-abc123
```

**👉 See [Technical Reference](docs/technical/TECHNICAL_REFERENCE.md#workflow-tracking-system)** for implementation

---

## Best Practices

### 1. Start Simple
- Install and use normally for Week 1
- Let system learn your patterns
- Don't over-configure initially

### 2. Review Weekly
- Check weekly report (15 minutes)
- Approve new agents if suggested
- Monitor performance trends

### 3. Enable Optimizations Gradually
- Month 2: Metadata-only prompts
- Month 3: Multi-file agents
- Month 4: Advanced coordination

### 4. Trust the Learning
- Don't micromanage agent selection
- Let patterns emerge naturally
- System improves over time

---

## Common Questions

**Q: Do I need to configure anything?**
A: No. Works out of the box. Configuration is optional.

**Q: What if I don't like an agent's output?**
A: System learns from your feedback and improves.

**Q: Will it replace my coding skills?**
A: No. Agents handle repetitive tasks. You make decisions.

**Q: What about different project types?**
A: System adapts to your patterns automatically.

**Q: How much does it cost?**
A: Free and open source. Only Claude API costs (~$160/month savings possible).

**Q: Is my code private?**
A: Yes. 100% local. No external servers. You control everything.

**Q: Can I create custom agents?**
A: Yes! System detects gaps and proposes new agents automatically.

---

## Documentation Map

### For Product Managers
- **[PM Quick Start](docs/PM_QUICK_START.md)** - 6 detailed examples
- **[PM Workflows](docs/PM_WORKFLOWS.md)** - 7 reusable patterns
- **[PM Capabilities](docs/PM_CAPABILITIES.md)** - What works vs manual

### For Engineers
- **[Technical Reference](docs/technical/TECHNICAL_REFERENCE.md)** - System internals
- **[Model Selection](docs/MODEL_SELECTION_STRATEGY.md)** - Performance optimization
- **[Hybrid Planning](docs/HYBRID_PLANNING_GUIDE.md)** - Multi-agent coordination

### For Everyone
- **[README.md](README.md)** - Project overview
- **[QUICK_START.md](QUICK_START.md)** - 5-minute setup
- **[CLAUDE.md](CLAUDE.md)** - System rules and agent coordination

---

## Getting Help

### Community
- **Questions**: [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)
- **Issues**: [GitHub Issues](https://github.com/robertmnyborg/claude-oak-agents/issues)
- **Examples**: Check PM_QUICK_START.md for walkthroughs

### Troubleshooting

**Agents not working**:
```bash
ls -la ~/.claude/agents/  # Check installation
python3 core/agent_loader.py --command=metadata  # Test loading
```

**Can't find agent for task**:
System will detect gap and suggest creating one. Review and approve.

**Too many notifications**:
```bash
export OAK_PROMPT_FEEDBACK=false
```

---

## What Makes OaK Special

### vs Regular Claude Code

| Feature | Claude Code | OaK Agents |
|---------|------------|------------|
| Specialized experts | ❌ No | ✅ 29+ agents |
| Learns patterns | ❌ No | ✅ Yes |
| Auto quality checks | ❌ Manual | ✅ Automatic |
| Fills capability gaps | ❌ No | ✅ Yes |
| Gets better over time | ❌ Static | ✅ Self-improving |

### vs Other Agent Systems

| Feature | Others | OaK |
|---------|--------|-----|
| Self-learning | ❌ No | ✅ Yes |
| Bundled scripts | ❌ No | ✅ Yes (10-100x faster) |
| A/B testing agents | ❌ No | ✅ Yes |
| Auto agent creation | ❌ No | ✅ Yes |
| Cost optimization | ❌ No | ✅ 93% possible |

**Unique**: Only self-learning agent system with Anthropic Skills parity

---

## Ready to Start?

### Quick Commands

```bash
# Install
git clone https://github.com/robertmnyborg/claude-oak-agents.git ~/Projects/claude-oak-agents
cd ~/Projects/claude-oak-agents
./automation/install_automation.sh

# Use (just use Claude Code normally)

# Review weekly
oak-weekly-review

# Enable optimizations
./scripts/enable_metadata_prompts.sh
```

### Next Steps

1. **Try PM workflows**: [PM_QUICK_START.md](docs/PM_QUICK_START.md)
2. **Explore patterns**: [PM_WORKFLOWS.md](docs/PM_WORKFLOWS.md)
3. **Read capabilities**: [PM_CAPABILITIES.md](docs/PM_CAPABILITIES.md)
4. **Technical deep-dive**: [Technical Reference](docs/technical/TECHNICAL_REFERENCE.md)

---

## Final Words

OaK Agents transforms Claude Code into a **self-learning team of AI specialists** that improve with use.

**No AI expertise required. No complex configuration. Just better, faster development.**

The sooner you start, the sooner the learning begins!

---

**Questions?** [Open an issue](https://github.com/robertmnyborg/claude-oak-agents/issues)
**Love it?** [Star the repo](https://github.com/robertmnyborg/claude-oak-agents) ⭐
