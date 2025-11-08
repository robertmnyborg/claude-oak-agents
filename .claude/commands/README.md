# Claude OaK Slash Commands

Comprehensive slash command system for the Claude OaK agent framework.

## Overview

This directory contains 22 slash commands organized into 7 categories, providing comprehensive workflows for:
- Version control and git operations
- Code analysis and quality validation
- Context loading (specs, workflows, telemetry)
- Documentation generation and maintenance
- Project management and planning
- CI/CD and deployment validation
- System help and tutorials

## Command Categories

### 1. Version Control (3 commands)

Git workflows, branch management, and spec-referenced commits.

| Command | Description |
|---------|-------------|
| `/commit-with-spec` | Create commit with specification reference |
| `/pr-with-context` | Create PR with full context (spec, telemetry, logs) |
| `/branch-by-pattern` | Create branch following naming conventions |

**Examples**:
```bash
/branch-by-pattern feature "oauth2 authentication" --ticket AUTH-456
/commit-with-spec spec-20251108-oauth2
/pr-with-context spec-20251108-oauth2 --include-telemetry
```

### 2. Code Analysis (4 commands)

Comprehensive code quality, security, performance, and dependency analysis.

| Command | Description |
|---------|-------------|
| `/analyze-complexity` | Identify over-engineering and suggest simplifications |
| `/security-scan` | Scan for vulnerabilities, auth issues, and secrets |
| `/performance-check` | Analyze bottlenecks and optimization opportunities |
| `/dependency-audit` | Check dependencies for CVEs, licenses, and supply chain risks |

**Examples**:
```bash
/analyze-complexity src/auth
/security-scan src/api --include-deps --severity high
/performance-check src/api --focus database
/dependency-audit --license-check
```

### 3. Context Loading (3 commands)

Load specifications, workflows, and telemetry for informed decision-making.

| Command | Description |
|---------|-------------|
| `/load-spec` | Load specification and set workflow context |
| `/load-workflow` | View workflow history and resume interrupted workflows |
| `/load-telemetry` | Query historical data for data-driven recommendations |

**Examples**:
```bash
/load-spec spec-20251108-oauth2-implementation
/load-workflow wf-20251108-abc123
/load-telemetry authentication --similar-to "oauth2 implementation" --time-range 30d
```

### 4. Documentation (3 commands)

Generate and maintain comprehensive documentation.

| Command | Description |
|---------|-------------|
| `/generate-spec` | Interactive spec creation with spec-manager |
| `/update-docs` | Identify and update outdated documentation |
| `/explain-codebase` | Generate comprehensive codebase overview |

**Examples**:
```bash
/generate-spec oauth2-authentication
/update-docs docs/api --type api
/explain-codebase --depth detailed --focus architecture
```

### 5. Project Management (3 commands)

Strategic planning, velocity analysis, and task prioritization.

| Command | Description |
|---------|-------------|
| `/create-roadmap` | Generate strategic roadmap with eigenquestions |
| `/analyze-velocity` | Calculate team velocity and identify trends |
| `/suggest-next-task` | AI-driven task prioritization |

**Examples**:
```bash
/create-roadmap authentication --timeframe Q1
/analyze-velocity --time-range 90d --by-agent
/suggest-next-task --context all
```

### 6. CI/Deployment (3 commands)

Pre-deployment validation and quality gate execution.

| Command | Description |
|---------|-------------|
| `/deploy-check` | Comprehensive deployment readiness validation |
| `/run-quality-gates` | Execute unified quality validation |
| `/validate-workflow` | Verify complete workflow including all phases |

**Examples**:
```bash
/deploy-check --environment production --strict
/run-quality-gates src/auth --strict --auto-fix
/validate-workflow --spec-id spec-20251108-oauth2
```

### 7. Miscellaneous (3 commands)

Help system, detailed status, and interactive tutorials.

| Command | Description |
|---------|-------------|
| `/oak-help` | Comprehensive help system for commands and agents |
| `/oak-status-detailed` | Enhanced system status with metrics |
| `/oak-tutorial` | Interactive tutorial for common workflows |

**Examples**:
```bash
/oak-help backend-architect
/oak-status-detailed --format table
/oak-tutorial --skip-to step3
```

## Common Workflows

### Workflow 1: Feature Development (Spec-Driven)

Full workflow from specification to pull request:

```bash
# 1. Create specification
/generate-spec oauth2-authentication

# 2. Load specification context
/load-spec spec-20251108-oauth2-authentication

# 3. Get AI-recommended next task
/suggest-next-task --context spec

# 4. [Implement code with agents]

# 5. Run quality gates
/run-quality-gates src/auth --strict

# 6. Create commit with spec reference
/commit-with-spec spec-20251108-oauth2-authentication

# 7. Create PR with full context
/pr-with-context spec-20251108-oauth2-authentication --include-telemetry
```

### Workflow 2: Code Quality Improvement

Analyze and improve code quality:

```bash
# 1. Analyze complexity
/analyze-complexity src/auth

# 2. Security scan
/security-scan src/auth --include-deps

# 3. Performance check
/performance-check src/auth --focus api

# 4. [Fix identified issues]

# 5. Validate improvements
/run-quality-gates src/auth --strict

# 6. Commit improvements
/commit-with-spec spec-20251108-code-quality
```

### Workflow 3: Deployment Preparation

Validate before deploying:

```bash
# 1. Run quality gates
/run-quality-gates src/ --strict

# 2. Security and dependency audit
/security-scan src/ --include-deps
/dependency-audit --license-check

# 3. Check staging deployment
/deploy-check --environment staging

# 4. [Deploy to staging, test]

# 5. Check production deployment
/deploy-check --environment production --strict

# 6. [Deploy to production if approved]
```

### Workflow 4: Telemetry-Driven Development

Use historical data for better decisions:

```bash
# 1. Load telemetry for similar tasks
/load-telemetry authentication --similar-to "oauth2" --time-range 90d

# 2. Get AI-recommended next task
/suggest-next-task --context all

# 3. Load recommended spec
/load-spec [spec-id-from-recommendation]

# 4. [Execute recommended task]

# 5. Analyze velocity trends
/analyze-velocity --time-range 30d --by-agent
```

## Command Format

All commands follow a consistent format:

```markdown
# Command Name

Brief description

## Usage
/command-name [args] [--flags]

## What This Does
1. Step-by-step breakdown
2. What the command accomplishes
3. Expected outcomes

## Example
/command-name example-arg --example-flag

## Agent Coordination
Which agents are invoked and in what sequence

## Output
What the user receives
```

## Getting Help

### Quick Help
```bash
/oak-help                    # Complete help system
/oak-help [category]         # Category-specific help
/oak-help [command-name]     # Command-specific help
/oak-help [agent-name]       # Agent-specific help
```

### Interactive Tutorial
```bash
/oak-tutorial                # Full tutorial (20-30 minutes)
/oak-tutorial --skip-to [step] # Skip to specific step
```

### System Status
```bash
/oak-status-detailed         # Comprehensive system status
/oak-status-detailed --format json  # JSON format for scripting
```

## Directory Structure

```
.claude/commands/
├── README.md                    # This file
├── version-control/
│   ├── commit-with-spec.md
│   ├── pr-with-context.md
│   └── branch-by-pattern.md
├── code-analysis/
│   ├── analyze-complexity.md
│   ├── security-scan.md
│   ├── performance-check.md
│   └── dependency-audit.md
├── context-loading/
│   ├── load-spec.md
│   ├── load-workflow.md
│   └── load-telemetry.md
├── documentation/
│   ├── generate-spec.md
│   ├── update-docs.md
│   └── explain-codebase.md
├── project-management/
│   ├── create-roadmap.md
│   ├── analyze-velocity.md
│   └── suggest-next-task.md
├── ci-deployment/
│   ├── deploy-check.md
│   ├── run-quality-gates.md
│   └── validate-workflow.md
└── misc/
    ├── oak-help.md
    ├── oak-status-detailed.md
    └── oak-tutorial.md
```

## Integration with Agents

These slash commands coordinate with the OaK agent system:

- **spec-manager**: Specification creation and management
- **quality-gate**: Unified quality validation
- **git-workflow-manager**: Git operations and PR creation
- **design-simplicity-advisor**: Complexity analysis and KISS validation
- **security-auditor**: Security scanning and validation
- **dependency-scanner**: Dependency vulnerability scanning
- **product-strategist**: Roadmapping and strategic planning
- **project-manager**: Workflow coordination and task management
- **technical-writer**: Documentation generation and updates
- **systems-architect**: Codebase architecture analysis
- **Main LLM**: Telemetry queries and context loading

## Best Practices

### 1. Start with Specifications
- Use `/generate-spec` for significant features (3+ hours work)
- Load specs with `/load-spec` before implementation
- Reference specs in commits with `/commit-with-spec`

### 2. Run Quality Gates Frequently
- Use `/run-quality-gates` during development, not just before commit
- Address warnings early (non-blocking but important)
- Use `--auto-fix` for common issues

### 3. Leverage Telemetry
- Query historical data with `/load-telemetry`
- Get AI recommendations with `/suggest-next-task`
- Track velocity trends with `/analyze-velocity`

### 4. Validate Before Deployment
- Always run `/deploy-check` before deploying
- Use `--strict` for production deployments
- Fix critical and high severity issues

### 5. Document Continuously
- Update docs with `/update-docs` after code changes
- Generate codebase overviews with `/explain-codebase`
- Keep specs in sync with implementation

## Advanced Usage

### Chaining Commands
```bash
# Complex workflow in sequence
/analyze-complexity src/auth && \
/security-scan src/auth --include-deps && \
/run-quality-gates src/auth --strict && \
/commit-with-spec spec-20251108-security-improvements
```

### Scripting with Commands
```bash
# Automated quality pipeline
for dir in src/auth src/api src/utils; do
  /analyze-complexity $dir
  /security-scan $dir
  /run-quality-gates $dir
done
```

### Custom Workflows
Create your own workflows by combining commands:

1. **Daily Quality Check**:
   - `/oak-status-detailed`
   - `/analyze-velocity --time-range 7d`
   - `/suggest-next-task`

2. **Pre-Commit Validation**:
   - `/run-quality-gates [changed-files]`
   - `/security-scan [changed-files]`
   - `/commit-with-spec [spec-id]`

3. **Release Preparation**:
   - `/validate-workflow --spec-id [spec-id]`
   - `/deploy-check --environment staging`
   - `/dependency-audit`
   - `/deploy-check --environment production --strict`

## Troubleshooting

### Command Not Found
Ensure commands directory is properly set up:
```bash
ls ~/.claude/commands/
# Should show all command categories
```

### Agent Not Available
Check agent installation:
```bash
ls ~/.claude/agents/
# Should show all agent files
```

### Telemetry Not Working
Verify telemetry system is configured:
```bash
ls telemetry/invocations.jsonl
# Should exist with logged invocations
```

## Contributing

To add new commands:

1. Create markdown file in appropriate category directory
2. Follow the standard command format
3. Include usage examples and agent coordination
4. Update this README with new command
5. Test command with `/oak-help [command-name]`

## Resources

- **Project Documentation**: `/Users/robertnyborg/Projects/claude-oak-agents/docs/`
- **Agent Specifications**: `/Users/robertnyborg/Projects/claude-oak-agents/agents/`
- **CLAUDE.md Rules**: `/Users/robertnyborg/Projects/claude-oak-agents/CLAUDE.md`
- **GitHub Repository**: https://github.com/robertmnyborg/claude-oak-agents

---

**Total Commands**: 22 across 7 categories
**Last Updated**: 2025-11-08
**Version**: 1.0.0
