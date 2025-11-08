# Claude OaK Help System

Comprehensive help system for all OaK agents and slash commands.

## Usage
/oak-help [category|agent-name|command-name]

## What This Does
1. Displays organized help for all commands and agents
2. Shows agent capabilities and use cases
3. Provides examples for common workflows
4. Links to detailed documentation
5. Offers context-aware suggestions

## Example
/oak-help version-control
/oak-help backend-architect
/oak-help

## Output
Complete Help System:
```markdown
# Claude OaK Agents - Help System

Welcome to the Claude OaK (Orchestrated agentic Knowledge) system.

## Quick Start

**For Product Managers**:
- Create specs: `/generate-spec [feature-name]`
- Load context: `/load-spec [spec-id]`
- Get recommendations: `/suggest-next-task`

**For Developers**:
- Analyze code: `/analyze-complexity [path]`
- Run quality gates: `/run-quality-gates [path]`
- Check deployment: `/deploy-check --environment [env]`

**For Everyone**:
- Get help: `/oak-help [topic]`
- Check status: `/oak-status-detailed`
- Tutorial: `/oak-tutorial`

---

## Slash Command Categories

### 1. Version Control (3 commands)
Git workflows, branch management, and spec-referenced commits.

- `/commit-with-spec [spec-id]` - Create commit with specification reference
- `/pr-with-context [spec-id]` - Create PR with full context (spec, telemetry, logs)
- `/branch-by-pattern [pattern] [description]` - Create branch following naming conventions

**Example**:
```
/branch-by-pattern feature "oauth2 authentication" --ticket AUTH-456
/commit-with-spec spec-20251108-oauth2
/pr-with-context spec-20251108-oauth2 --include-telemetry
```

**Related Agents**: git-workflow-manager

---

### 2. Code Analysis (4 commands)
Comprehensive code quality, security, performance, and dependency analysis.

- `/analyze-complexity [path]` - Identify over-engineering and suggest simplifications
- `/security-scan [path]` - Scan for vulnerabilities, auth issues, and secrets
- `/performance-check [path]` - Analyze bottlenecks and optimization opportunities
- `/dependency-audit` - Check dependencies for CVEs, licenses, and supply chain risks

**Example**:
```
/analyze-complexity src/auth
/security-scan src/api --include-deps
/performance-check src/api --focus database
/dependency-audit --license-check
```

**Related Agents**: design-simplicity-advisor, security-auditor, dependency-scanner

---

### 3. Context Loading (3 commands)
Load specifications, workflows, and telemetry for informed decision-making.

- `/load-spec [spec-id]` - Load specification and set workflow context
- `/load-workflow [workflow-id]` - View workflow history and resume interrupted workflows
- `/load-telemetry [task-type]` - Query historical data for data-driven recommendations

**Example**:
```
/load-spec spec-20251108-oauth2-implementation
/load-workflow wf-20251108-abc123
/load-telemetry authentication --similar-to "oauth2 implementation"
```

**Related Agents**: spec-manager, Main LLM (telemetry queries)

---

### 4. Documentation (3 commands)
Generate and maintain comprehensive documentation.

- `/generate-spec [feature-name]` - Interactive spec creation with spec-manager
- `/update-docs [path]` - Identify and update outdated documentation
- `/explain-codebase` - Generate comprehensive codebase overview

**Example**:
```
/generate-spec oauth2-authentication
/update-docs docs/api --type api
/explain-codebase --depth detailed --focus architecture
```

**Related Agents**: spec-manager, technical-writer, systems-architect

---

### 5. Project Management (3 commands)
Strategic planning, velocity analysis, and task prioritization.

- `/create-roadmap [product-area]` - Generate strategic roadmap with eigenquestions
- `/analyze-velocity` - Calculate team velocity and identify trends
- `/suggest-next-task` - AI-driven task prioritization

**Example**:
```
/create-roadmap authentication --timeframe Q1
/analyze-velocity --time-range 90d --by-agent
/suggest-next-task --context all
```

**Related Agents**: product-strategist, project-manager, business-analyst

---

### 6. CI/Deployment (3 commands)
Pre-deployment validation and quality gate execution.

- `/deploy-check [--environment]` - Comprehensive deployment readiness validation
- `/run-quality-gates [path]` - Execute unified quality validation
- `/validate-workflow` - Verify complete workflow including all phases

**Example**:
```
/deploy-check --environment production --strict
/run-quality-gates src/auth --strict
/validate-workflow --spec-id spec-20251108-oauth2
```

**Related Agents**: quality-gate, security-auditor, dependency-scanner

---

### 7. Miscellaneous (3 commands)
Help system, detailed status, and interactive tutorials.

- `/oak-help [topic]` - This comprehensive help system
- `/oak-status-detailed` - Enhanced system status with metrics
- `/oak-tutorial` - Interactive tutorial for common workflows

**Example**:
```
/oak-help backend-architect
/oak-status-detailed
/oak-tutorial
```

---

## Agent Capabilities

### Product Management
- **spec-manager** - Collaborative specification writing, task decomposition
- **product-strategist** - Eigenquestion methodology, roadmapping, success metrics
- **business-analyst** - Requirements analysis, stakeholder communication

### Development
- **frontend-developer** - UI/UX, React/Vue/Angular (functional over OOP)
- **backend-architect** - API design, database schemas, server logic (Go > TS > JS)
- **infrastructure-specialist** - CDK/Terraform, cloud deployment (Lambda > ECS > K8s)

### Quality & Security
- **quality-gate** - Unified code review, complexity analysis, KISS validation
- **security-auditor** - Penetration testing, compliance, threat modeling
- **unit-test-expert** - Unit test creation, coverage validation
- **dependency-scanner** - Supply chain security, CVE scanning, license compliance

### Analysis & Documentation
- **design-simplicity-advisor** - KISS enforcement, over-engineering detection
- **systems-architect** - High-level design, technical specifications
- **technical-writer** - Context-aware documentation for all audiences

### Workflow Management
- **git-workflow-manager** - Git operations, PR creation, branch management
- **project-manager** - Multi-step coordination, timeline management

### Special Purpose
- **debug-specialist** - Critical error resolution (HIGHEST PRIORITY)
- **qa-specialist** - Integration testing, E2E validation
- **general-purpose** - Single-line commands and basic queries ONLY

---

## Common Workflows

### Workflow 1: Feature Development (Spec-Driven)
```
1. /generate-spec [feature-name]          # Co-author specification
2. /load-spec [spec-id]                   # Load spec context
3. [Implementation by agents]             # Agents coordinate automatically
4. /run-quality-gates src/[path]          # Validate quality
5. /commit-with-spec [spec-id]            # Create commit
6. /pr-with-context [spec-id]             # Create PR with full context
```

### Workflow 2: Code Quality Improvement
```
1. /analyze-complexity src/[path]         # Identify over-engineering
2. /security-scan src/[path]              # Find security issues
3. /performance-check src/[path]          # Detect bottlenecks
4. [Fix issues]                           # Address findings
5. /run-quality-gates src/[path]          # Validate improvements
6. /commit-with-spec [related-spec]       # Create commit
```

### Workflow 3: Deployment Preparation
```
1. /run-quality-gates [path]              # Validate quality
2. /security-scan [path] --include-deps   # Security check
3. /dependency-audit                      # Check dependencies
4. /deploy-check --environment staging    # Staging validation
5. /deploy-check --environment production # Production check
6. [Deploy if all checks pass]            # Go/no-go decision
```

### Workflow 4: Telemetry-Driven Development
```
1. /load-telemetry [task-type]            # Query historical data
2. /suggest-next-task                     # Get AI recommendation
3. /load-spec [recommended-spec]          # Load spec context
4. [Execute recommended task]             # Implement
5. /analyze-velocity                      # Track performance
```

---

## Help by Topic

**Get help on specific topics**:
```
/oak-help version-control     # Git and branching help
/oak-help code-analysis       # Quality and security analysis
/oak-help context-loading     # Specs, workflows, telemetry
/oak-help documentation       # Spec and docs generation
/oak-help project-management  # Roadmaps, velocity, tasks
/oak-help ci-deployment       # Quality gates and deployment
```

**Get help on specific agents**:
```
/oak-help backend-architect
/oak-help frontend-developer
/oak-help spec-manager
/oak-help quality-gate
/oak-help security-auditor
```

**Get help on specific commands**:
```
/oak-help commit-with-spec
/oak-help analyze-complexity
/oak-help deploy-check
```

---

## Documentation Resources

### For Product Managers
- **Quick Start**: docs/PM_QUICK_START.md
- **Workflow Library**: docs/PM_WORKFLOWS.md
- **Capabilities Matrix**: docs/PM_CAPABILITIES.md

### For Engineers
- **Technical Architecture**: docs/oak-design/OAK_ARCHITECTURE.md
- **Implementation Guide**: docs/oak-design/IMPLEMENTATION_GUIDE.md
- **Model Selection**: docs/MODEL_SELECTION_STRATEGY.md

### For Everyone
- **README**: Project overview and installation
- **CLAUDE.md**: Complete development rules and workflows
- **Agent Patterns**: .claude/AGENT_PATTERNS.md

---

## Tips & Best Practices

### Slash Commands
- Use tab completion for command names
- Commands work in any directory (use absolute paths)
- Chain commands for complex workflows
- Use `--help` flag for command-specific help

### Agent Coordination
- Agents coordinate automatically (no manual orchestration)
- Main LLM handles multi-agent workflows
- Quality gates run automatically before commits
- Telemetry tracks all agent invocations

### Specifications
- Start significant features with /generate-spec
- Load specs with /load-spec before implementation
- Reference specs in commits with /commit-with-spec
- Track progress against acceptance criteria

### Quality Gates
- Run /run-quality-gates before committing
- Use --strict for zero-tolerance validation
- Address warnings (non-blocking but important)
- Auto-fix available for common issues (--auto-fix)

### Deployment
- Always run /deploy-check before production
- Fix critical and high severity issues
- Warnings are informational (non-blocking for staging)
- Use --strict for production deployments

---

## Interactive Tutorial

**New to OaK?** Run the interactive tutorial:
```
/oak-tutorial
```

This will guide you through:
1. Creating your first spec
2. Running quality gates
3. Creating spec-referenced commits
4. Analyzing code complexity
5. Checking deployment readiness

---

## Getting Help

**Issues or Questions**:
- GitHub Discussions: https://github.com/robertmnyborg/claude-oak-agents/discussions
- GitHub Issues: https://github.com/robertmnyborg/claude-oak-agents/issues
- Documentation: docs/ directory

**Contributing**:
See CONTRIBUTING.md for contribution guidelines.

---

**Need more specific help?** Try:
- `/oak-help [specific-topic]` for focused help
- `/oak-status-detailed` for system status
- `/oak-tutorial` for hands-on learning
```

This provides comprehensive help organized by category with examples and best practices.
## See Also
For related commands, see [Quality Commands](../shared/related-quality-commands.md)
