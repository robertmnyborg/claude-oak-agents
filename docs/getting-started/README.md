# Getting Started with Claude OaK Agents

**Quick path to productivity with AI-powered product development**

This guide helps you get up and running with claude-oak-agents in 5-10 minutes, regardless of your role.

## Quick Navigation

**Choose your path**:
- [Product Manager](#for-product-managers) - Co-author specs, design schemas, create prototypes
- [Engineer](#for-engineers) - Implement features, build systems, optimize code
- [Architect](#for-architects) - Design systems, plan architecture, make technical decisions

---

## Installation (Everyone)

### Prerequisites
- Claude Code installed and configured
- Git installed
- Basic terminal familiarity

### Install Claude OaK Agents

```bash
# 1. Clone repository
git clone https://github.com/robertmnyborg/claude-oak-agents.git ~/Projects/claude-oak-agents
cd ~/Projects/claude-oak-agents

# 2. Link agents to Claude Code
mkdir -p ~/.claude/agents
ln -s ~/Projects/claude-oak-agents/agents/* ~/.claude/agents/

# 3. Verify installation
ls ~/.claude/agents/

# 4. (Optional) Install automation for telemetry
./automation/install_automation.sh
```

**That's it!** The agents are now available in Claude Code.

---

## For Product Managers

**What you can do**: Co-author feature specifications, design database schemas, create UI prototypes, and deliver professional engineering handoffs.

### Your First Workflow (10 minutes)

**Step 1: Create a Specification**
```
"Help me create a spec for user authentication"
```

The spec-manager agent will guide you through:
1. Goals and requirements
2. Technical design
3. Implementation plan
4. Test strategy

You approve each section before moving forward.

**Step 2: Design the Database**
```
"Design a PostgreSQL schema for user authentication"
```

The backend-architect creates:
- Normalized schema with relationships
- DDL statements for tables
- Indexes for performance
- Migration plan

**Step 3: Prototype the UI**
```
"Create React components for login and registration"
```

The frontend-developer scaffolds:
- Component structure
- State management (Redux/Zustand)
- TypeScript types
- Usage examples

**Step 4: Create Engineering Handoff**
```
"Create a PR with the spec, schema, and components"
```

The git-workflow-manager creates a complete pull request with:
- Feature specification
- Database schema and migrations
- UI component prototypes
- Test plan

### Next Steps

**Learn PM workflows**: See [Product Manager Guide](../by-role/product-managers/README.md)

**Explore capabilities**: See [PM Quick Start](../by-role/product-managers/quick-start.md) for 6 detailed examples

**Common patterns**: See [PM Workflows](../by-role/product-managers/workflows.md) for 7 reusable patterns

---

## For Engineers

**What you can do**: Implement features with specialized agents, automatic quality gates, and multi-agent coordination.

### Your First Workflow (5 minutes)

**Step 1: Implement a Feature**
```
"Implement OAuth2 authentication endpoints"
```

Claude Code automatically:
1. Routes to backend-architect
2. Implements the feature
3. Runs quality gates
4. Creates tests
5. Commits with proper message

**Step 2: Review the Output**

Check:
- Implementation quality
- Test coverage
- Security validation
- Documentation completeness

**Step 3: Iterate if Needed**
```
"Add rate limiting to the auth endpoints"
```

The system enhances the implementation with:
- Rate limiting middleware
- Configuration options
- Updated tests
- Documentation

### Next Steps

**Technical reference**: See [Engineers Guide](../by-role/engineers/README.md)

**Agent development**: See [Agent Development Guide](../by-role/engineers/agent-development.md)

**Telemetry integration**: See [Telemetry Reference](../by-role/engineers/technical-reference.md#workflow-tracking-system)

---

## For Architects

**What you can do**: Design system architecture, plan complex projects, make technical decisions, and establish engineering patterns.

### Your First Workflow (15 minutes)

**Step 1: Design System Architecture**
```
"Design a scalable microservices architecture for a multi-tenant SaaS platform"
```

The systems-architect will:
1. Analyze requirements
2. Propose architecture options
3. Document trade-offs
4. Recommend best approach

**Step 2: Plan Implementation**
```
"Create hybrid planning workflow for this architecture"
```

The project-manager coordinates:
1. Break down into phases
2. Identify agent assignments
3. Plan dependencies
4. Estimate timeline

**Step 3: Review Context Engineering**
```
"Optimize prompt architecture for this system"
```

The design-simplicity-advisor analyzes:
1. Complexity reduction opportunities
2. KISS principle compliance
3. Prompt efficiency
4. Scalability considerations

### Next Steps

**System design guide**: See [Architects Guide](../by-role/architects/README.md)

**Hybrid planning**: See [Hybrid Planning Guide](../by-role/architects/hybrid-planning.md)

**Context engineering**: See [Context Engineering Architecture](../by-role/architects/context-engineering.md)

---

## Key Concepts

### Specialized Agents

Claude OaK Agents provides 29+ specialized AI assistants organized by domain:

- **Product Management**: spec-manager, product-strategist, business-analyst
- **Development**: frontend-developer, backend-architect, mobile-developer, ml-engineer
- **Quality**: quality-gate, security-auditor, unit-test-expert, qa-specialist
- **Infrastructure**: infrastructure-specialist, systems-architect
- **Workflow**: git-workflow-manager, project-manager, changelog-recorder

### How It Works

```
User Request
  ↓
Classification (Info/Implementation/Analysis/Coordination)
  ↓
Domain Identification (Frontend/Backend/Infrastructure/Security/Data)
  ↓
Agent Selection (Automatic based on domain)
  ↓
Execution (Single or multi-agent)
  ↓
Quality Gate (Automatic validation)
  ↓
Git Operations (If code changes)
```

### Automatic Workflows

The system handles complexity automatically:

- **Simple requests**: Single agent, quick execution
- **Complex features**: Multi-agent coordination with planning
- **Security-critical**: Automatic security audits
- **Quality gates**: Automatic code review and testing

---

## Common Questions

### Do I need to know which agent to use?

No. The system automatically selects the right agents based on your request. Just describe what you want in natural language.

### Can I request specific agents?

Yes. You can explicitly request agents if you prefer:
```
"Use backend-architect to design a database schema"
```

### What if I make a mistake?

The system includes quality gates that catch issues before committing. You can always:
- Request changes
- Iterate on implementations
- Review before finalizing

### How do I track what happened?

The system includes comprehensive telemetry:
- Workflow tracking for multi-agent coordination
- Execution logs for all agent invocations
- Success metrics and analytics

See [Telemetry Documentation](../by-role/engineers/technical-reference.md#workflow-tracking-system)

---

## Your First Real Project

### Example: Build a Task Management Feature

**For PMs**:
```
"Create a spec for a task management feature with:
- Task creation and editing
- Assignment to users
- Status tracking
- Due dates and reminders"
```

**For Engineers**:
```
"Implement the task management feature from the spec"
```

**For Architects**:
```
"Design the system architecture for task management including:
- Database schema
- API design
- State management
- Real-time updates"
```

The system coordinates all aspects automatically.

---

## Next Steps by Role

### Product Managers
1. Read [PM Quick Start](../by-role/product-managers/quick-start.md) - 6 detailed examples
2. Explore [PM Workflows](../by-role/product-managers/workflows.md) - 7 reusable patterns
3. Review [PM Capabilities](../by-role/product-managers/capabilities.md) - What works today

### Engineers
1. Read [Technical Reference](../by-role/engineers/technical-reference.md) - System internals
2. Learn [Agent Development](../by-role/engineers/agent-development.md) - Create custom agents
3. Explore [Model Selection Strategy](../../MODEL_SELECTION_STRATEGY.md) - Cost optimization

### Architects
1. Read [System Design](../by-role/architects/system-design.md) - OaK architecture
2. Study [Hybrid Planning](../by-role/architects/hybrid-planning.md) - Multi-agent coordination
3. Review [Context Engineering](../by-role/architects/context-engineering.md) - Prompt optimization

---

## Support

**Documentation Hub**: See [Documentation Index](../INDEX.md) for complete navigation

**GitHub Discussions**: [Ask questions and share experiences](https://github.com/robertmnyborg/claude-oak-agents/discussions)

**Issues**: [Report bugs or request features](https://github.com/robertmnyborg/claude-oak-agents/issues)

**Project README**: See [Main README](../../README.md) for project overview

---

**Ready to dive deeper?** Choose your role above and continue to the specialized guide!
