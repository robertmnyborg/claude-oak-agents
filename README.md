# Claude OaK Agents

**AI-Powered Product Development for Semi-Technical Product Managers**

Turn product ideas into production-ready specs, prototypes, and handoffs to engineering teams. Co-author feature specifications with AI agents, design database schemas, scaffold components, and ship better PRs - without writing code from scratch.

**Built for PMs who want to**: Prototype faster, create clearer specs, understand technical feasibility, and deliver better handoffs to engineering teams.

## What You Can Actually Do

Real capabilities you can use today - no vaporware:

### Co-Author Feature Specs with AI
- **spec-manager**: Collaborative specification writing with approval checkpoints
- Work in spec terms, not code terms
- Markdown for humans, YAML for execution
- Track requirements through implementation

### Design Database Schemas
- **backend-architect**: PostgreSQL, MySQL, MongoDB schema design
- Generate DDL and migrations
- Optimize for performance and scalability
- Design APIs (REST, GraphQL)

### Create State Stores and Components
- **frontend-developer**: Redux, Zustand, Pinia, NgRx state stores
- Scaffold React, Vue, Angular components
- TypeScript support built-in
- Component libraries and UI prototypes

### Map User Workflows
- **ux-designer**: User journey mapping and information architecture
- Evidence-based UX principles
- Reduce friction points in flows
- Design intuitive navigation patterns

### Translate Business to Product Strategy
- **product-strategist**: Business problem → product opportunity
- Eigenquestion methodology for clarity
- Define success metrics and validation hypotheses
- Prioritize features with data

### Manage Git Workflows
- **git-workflow-manager**: Fork repos, create branches, commit changes
- Create pull requests with complete specs
- Automated changelog generation
- Professional handoffs to engineering

### What Requires Manual Work
- **Design System Import**: No Figma API automation - create components manually from designs
- **Live Database Queries**: Schema design only - not a read-only query tool for production DBs

## Quick Start (5 Minutes)

Get up and running with AI-powered product development:

### Installation

```bash
# 1. Clone repository
git clone https://github.com/robertmnyborg/claude-oak-agents.git ~/Projects/claude-oak-agents
cd ~/Projects/claude-oak-agents

# 2. Install agents
mkdir -p ~/.claude/agents
ln -s ~/Projects/claude-oak-agents/agents/* ~/.claude/agents/

# 3. That's it! Open Claude Code and start using agents
```

### Create Your First Spec

Open Claude Code in your project directory and try:

```
"Help me create a spec for user authentication"
```

The **spec-manager** agent will guide you through:
1. Goals and requirements (what are we building and why?)
2. Technical design (how will it work?)
3. Implementation plan (what needs to be built?)
4. Test strategy (how do we validate it works?)

You'll co-author the spec section by section with approval checkpoints.

### Prototype a Feature

```
"Design a Redux store for shopping cart state"
```

The **frontend-developer** agent will:
- Create state slice with actions and reducers
- Generate TypeScript types
- Add selectors for accessing state
- Provide usage examples

### Design a Database Schema

```
"Design a PostgreSQL schema for a multi-tenant SaaS app"
```

The **backend-architect** agent will:
- Create normalized schema with proper relationships
- Generate DDL statements
- Design indexes for performance
- Plan migrations

## PM Use Cases

See what you can accomplish with AI-powered agents:

### Use Case Library
- **[PM Quick Start Guide](docs/PM_QUICK_START.md)** - 6 detailed examples for common PM workflows
- **[PM Workflow Library](docs/PM_WORKFLOWS.md)** - Step-by-step patterns for specs, prototypes, and handoffs
- **[PM Capabilities Matrix](docs/PM_CAPABILITIES.md)** - Honest assessment of what works today vs what's manual

### Common PM Workflows

**1. Co-Author a Feature Spec**
- Work with spec-manager to document requirements
- Get approval checkpoints at each section
- Generate machine-readable YAML for implementation
- Track changes in spec terms, not code terms

**2. Design and Prototype UI**
- Map user workflows with ux-designer
- Scaffold components with frontend-developer
- Create state management (Redux, Zustand, etc.)
- Build clickable prototypes

**3. Database and API Design**
- Design schemas with backend-architect
- Plan migrations and indexing strategy
- Define REST or GraphQL APIs
- Generate OpenAPI documentation

**4. Create Professional Handoffs**
- Fork production repo with git-workflow-manager
- Create feature branch with clear naming
- Commit specs and prototypes
- Open PR with complete context for engineering

**5. Translate Business Strategy**
- Use product-strategist to frame eigenquestions
- Convert business problems to product opportunities
- Define validation hypotheses
- Establish success metrics

**6. Validate Technical Feasibility**
- Check implementation complexity estimates
- Identify technical risks early
- Get honest assessment of effort required
- Make informed go/no-go decisions

## Support and Documentation

### For Product Managers
- **[PM Quick Start Guide](docs/PM_QUICK_START.md)** - Get started in 10 minutes
- **[PM Workflow Library](docs/PM_WORKFLOWS.md)** - Common patterns and examples
- **[PM Capabilities Matrix](docs/PM_CAPABILITIES.md)** - What works vs what's manual
- **[GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)** - PM community and questions

### For Engineers
- **[Technical Documentation](docs/oak-design/OAK_ARCHITECTURE.md)** - System architecture
- **[Implementation Guide](docs/oak-design/IMPLEMENTATION_GUIDE.md)** - Integration details
- **[Model Selection Strategy](docs/MODEL_SELECTION_STRATEGY.md)** - Performance optimization
- **[GitHub Issues](https://github.com/robertmnyborg/claude-oak-agents/issues)** - Bug reports and feature requests

### For Researchers and Architects
- **[Hybrid Planning Guide](docs/HYBRID_PLANNING_GUIDE.md)** - Multi-agent coordination
- **[Context Engineering](docs/CONTEXT_ENGINEERING_ARCHITECTURE.md)** - Prompt optimization
- **[Deployment Roadmap](docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)** - Implementation timeline

## About This Project

**Built on**: [claude-squad](https://github.com/jamsajones/claude-squad) by jamsajones
**License**: MIT - See [LICENSE](LICENSE) for details
**Status**: Active development - PM-focused features stable and ready for use

### Contributing
Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Community
- **Discussions**: [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)
- **Issues**: [GitHub Issues](https://github.com/robertmnyborg/claude-oak-agents/issues)
- **Contributors**: See [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

**Ready to get started?** Install the agents and try creating your first spec: [Quick Start](#quick-start-5-minutes)

---

## Engineer Documentation

This section is for engineers implementing or extending the agent system.

For engineers looking to understand the technical implementation, agent architecture, telemetry system, and deployment details, see:

- **[Technical Architecture](docs/oak-design/OAK_ARCHITECTURE.md)** - Complete system design
- **[Implementation Guide](docs/oak-design/IMPLEMENTATION_GUIDE.md)** - Integration and development
- **[6-Month Deployment Plan](docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)** - Roadmap and phases
- **[Model Selection Strategy](docs/MODEL_SELECTION_STRATEGY.md)** - Performance optimization
- **[Hybrid Planning](docs/HYBRID_PLANNING_GUIDE.md)** - Multi-agent coordination
- **[Context Engineering](docs/CONTEXT_ENGINEERING_ARCHITECTURE.md)** - Prompt architecture
- **[Multi-File Agents](docs/MULTI_FILE_AGENTS.md)** - Advanced agent packaging
- **[MCP Integration](mcp/README.md)** - Model Context Protocol setup
- **[Automation System](automation/README.md)** - Telemetry and scheduling
- **[Hooks Documentation](hooks/README.md)** - Performance logging

### 29+ Specialized Agents

- **Product Management**: spec-manager, product-strategist, ux-designer
- **Development**: frontend-developer, backend-architect, mobile-developer, blockchain-developer, ml-engineer
- **Quality**: code-reviewer, security-auditor, unit-test-expert, qa-specialist, dependency-scanner
- **Infrastructure**: infrastructure-specialist, systems-architect, performance-optimizer, debug-specialist
- **Workflow**: git-workflow-manager, project-manager, changelog-recorder
- **Analysis**: business-analyst, data-scientist, state-analyzer, agent-auditor
- **Documentation**: technical-documentation-writer, content-writer
- **Special Purpose**: design-simplicity-advisor, agent-creator, general-purpose

System automatically creates new agents when capability gaps are detected.
