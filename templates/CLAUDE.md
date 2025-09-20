# Project Rules for Development Process

<PersistentRules>
<AutoEcho>
CRITICAL: At the start of EVERY response, Claude must acknowledge these rules by stating: "Following project CLAUDE.md rules with mandatory agent-coordinator workflow."
</AutoEcho>

<MandatoryWorkflow id="coordinator-required">
⚠️ **MANDATORY WORKFLOW - NO EXCEPTIONS** ⚠️
EVERY user request MUST begin with:
Task(subagent_type="agent-coordinator", prompt="Plan workflow for: [user's request]")

NEVER skip this step for ANY reason - including:
- Simple questions
- Agent improvements
- Meta-system work
- "Quick" tasks
- Follow-up requests

See agent-coordinator.md for complete workflow requirements.
</MandatoryWorkflow>
</PersistentRules>

## Project-Specific Configuration

### Technology Stack
- **Primary Language**: [Go/TypeScript/Bash/Ruby - choose one]
- **Framework**: [Specify main framework - CDK for infrastructure]
- **Architecture**: [Distributed functions, static assets, specific patterns]
- **Database**: [PostgreSQL/MongoDB/DynamoDB - if applicable]

### Project Standards
- **Required Files**: README.md, SPEC.md, CLAUDE.md
- **Code Style**: [Specify linting/formatting tools]
- **Testing**: [Unit/Integration/E2E testing requirements]
- **Documentation**: [API docs, architecture docs requirements]

### Class Usage Guidelines (CDK Exception)
#### When Classes Are Permitted
- **CDK Constructs**: Classes required for CDK construct interfaces (extending Construct)
- **Framework Requirements**: Classes mandated by external frameworks/libraries
- **[Project-Specific]**: [Any project-specific class requirements]

#### Class Design Principles
- **Framework Methods Only**: Classes should only contain framework defined/required methods
- **No Business Logic**: Move all business logic to pure utility functions
- **Thin Wrappers**: Classes act as thin wrappers around functional code
- **No Custom Side Effects**: Classes should not create side effects beyond framework requirements

### Dependencies
- **Package Manager**: [npm/yarn/go mod/cargo - specify]
- **Dependency Policy**: Don't add new dependencies when simple solutions exist in a few lines of code
- **Approved Libraries**: [List pre-approved libraries/frameworks]
- **Security Scanning**: All dependencies must pass security scans

### Git Workflow
- **Branch Strategy**: [main/develop, feature branches, etc.]
- **Commit Messages**: [Conventional commits, specific format]
- **PR Requirements**: [Review requirements, CI/CD checks]
- **Merge Strategy**: [Squash/merge/rebase preference]

### Development Environment
- **IDE**: [VSCode/IntelliJ/Vim - team preference]
- **Linting**: [ESLint/golangci-lint/specific tools]
- **Formatting**: [Prettier/gofmt/specific tools]
- **Pre-commit Hooks**: [Specify required hooks]

### Communication Style
- **Direct and concise** communication
- **No unnecessary apologies** or validation of ideas
- **Skip pleasantries** and focus on technical details
- **Report completion** with clear summary of work done

### Quality Gates
- **Security Review**: All code changes require security analysis
- **Code Clarity**: Code must pass maintainability analysis
- **Test Coverage**: [Specify minimum coverage percentage]
- **Performance**: [Specify performance requirements]

### Deployment
- **Environment**: [AWS/GCP/Azure/local - specify]
- **Infrastructure**: [CDK/Terraform/specific tools]
- **CI/CD**: [GitHub Actions/Jenkins/specific pipeline]
- **Monitoring**: [CloudWatch/Grafana/specific tools]

## Project-Specific Rules

### [Feature/Domain Area 1]
- [Specific rules for this area]
- [Architecture patterns to follow]
- [Testing requirements]

### [Feature/Domain Area 2]
- [Specific rules for this area]
- [Integration patterns]
- [Data handling requirements]

### [Feature/Domain Area 3]
- [Specific rules for this area]
- [Security considerations]
- [Performance requirements]

## Notes
- This file should be customized for each project
- Remove placeholder sections not relevant to your project
- Add project-specific sections as needed
- Keep aligned with global ~/.claude/CLAUDE.md but override as necessary