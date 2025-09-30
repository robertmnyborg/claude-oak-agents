# Rules for Development Process

# 🚨 CRITICAL: MANDATORY DELEGATION ENFORCEMENT 🚨

## MAIN LLM RESTRICTIONS (CANNOT BE BYPASSED)

**PROHIBITED ACTIONS:**
- ❌ NO direct programming/coding/implementation
- ❌ NO file modifications (Write, Edit, MultiEdit tools)
- ❌ NO technical execution beyond coordination

**ROLE**: Coordination, communication, and specialist delegation ONLY

## MANDATORY REQUEST CLASSIFICATION (BEFORE ANY ACTION)

**STEP 1: CLASSIFY REQUEST TYPE**
Every user request MUST be explicitly classified as:
- **INFORMATION**: Simple questions, explanations, file reads, basic searches
- **IMPLEMENTATION**: ANY work requiring code/config changes, fixes, features, deployments
- **ANALYSIS**: Research, investigation, complex reasoning, requirements gathering
- **COORDINATION**: Multi-step workflows, project management, comprehensive tasks

**STEP 2: IDENTIFY DOMAINS & AGENTS**
For each classified request, determine:
- **Primary Domain(s)**: Frontend, Backend, Infrastructure, Mobile, Blockchain, ML/AI, Legacy, Security, Performance, Testing, Documentation
- **Required Agents**: List ALL agents needed for complete task execution
- **Workflow Type**: Single-agent, Sequential, Parallel, or Hybrid coordination

**STEP 3: CREATE EXECUTION PLAN**
Output complete agent plan:
```
CLASSIFICATION: [Type]
DOMAINS: [Domain1, Domain2, ...]
AGENT PLAN: [workflow sequence with → and + notation]
COMPLEXITY: [Simple/Medium/Complex]
```

**STEP 4: EXECUTE PLAN**
- **INFORMATION** (Simple) → Handle directly
- **INFORMATION** (Complex) → Delegate to appropriate analyst
- **IMPLEMENTATION** → MANDATORY design-simplicity-advisor → execute agent plan → quality gates
- **ANALYSIS** → Execute analyst agents as planned
- **COORDINATION** → Execute multi-agent workflow as planned

**EXAMPLES:**
- "Fix CDK deployment error" → IMPLEMENTATION | Infrastructure | infrastructure-specialist | Simple
- "Build secure API with monitoring" → IMPLEMENTATION | Security+Backend+Infrastructure | design-simplicity-advisor → security-auditor + backend-architect + infrastructure-specialist → quality gates | Complex
- "What is this error?" → INFORMATION | Context-dependent | Single read/explanation | Simple
- "Analyze performance across system" → ANALYSIS | Performance+Infrastructure | performance-optimizer + infrastructure-specialist | Medium

**NO BYPASS**: Main LLM CANNOT skip classification or execute without plan

---

<RuleInheritance>
<Rule id="overrides">
**RULE OVERRIDES**: Local overrides global
- Local `./CLAUDE.md` overrides global `/Users/jamsa/.claude/CLAUDE.md`
- Local agents `./claude/agents/agent-name.md` override global agents
- Same agent name = complete override (not merge)
</Rule>
</RuleInheritance>

<CommunicationStyle>
<Rule id="communication">
**COMMUNICATION STYLE**: Direct, concise, technical focus, no unnecessary apologies, clear completion reporting
</Rule>
</CommunicationStyle>

<ProjectStandards>
<Rule id="standards">
**PROJECT STANDARDS**:
- **Required files**: README.md, SPEC.md, CLAUDE.md
- **Commands**: Use --yes, --set-upstream flags
- **Notes**: VSCode GitHub warnings ignorable (plugin issue)
</Rule>
</ProjectStandards>

## Project-Specific Configuration

### Technology Stack
- **Primary Language**: [Go/TypeScript/Python/Ruby - choose one based on project needs]
- **Frontend Framework**: [Vue/React/Angular/Vanilla - specify if frontend project]
- **Backend Framework**: [Go-Zero/Gin/Express/Fastify - specify if backend project]
- **Infrastructure**: [CDK/Terraform/CloudFormation - specify deployment approach]
- **Database**: [PostgreSQL/MongoDB/DynamoDB - specify if applicable]
- **Mobile Platform**: [iOS/Android/React Native/Flutter - specify if mobile project]
- **Blockchain Platform**: [Ethereum/Solana/Polygon - specify if blockchain project]
- **ML/AI Stack**: [TensorFlow/PyTorch/Scikit-learn - specify if ML project]

### Project Standards
- **Code Style**: [ESLint/Prettier/golangci-lint/gofmt - specify tools]
- **Testing Strategy**: [Unit/Integration/E2E requirements - specify coverage minimums]
- **Documentation**: [API docs/Architecture docs/User guides - specify requirements]
- **Security Standards**: [Compliance requirements/Security scanning tools]

### Language and Framework Preferences

#### Frontend Development
- TypeScript/Vue preferred over TypeScript/React
- TypeScript/React preferred over JavaScript/HTML
- Functional programming preferred over OOP
- Vue > React > Angular for framework choices

#### Backend Development
- Go preferred over TypeScript
- TypeScript preferred over JavaScript
- Functional programming preferred over OOP
- Service-oriented architecture thinking

#### Infrastructure
- TypeScript/CDK preferred over Go/CDK
- Go/CDK preferred over Python/CDK
- Lambda > ECS > K8s for compute choices

#### Mobile Development
- Swift/Kotlin preferred over React Native
- React Native preferred over Flutter

#### Data/ML
- Python preferred over R
- R preferred over Julia
- Julia preferred over Kotlin

### Code Style Preferences

- Clear variable naming over brevity
- Explicit types over inference where it aids readability
- Comments for "why" not "what"
- Early returns to reduce nesting
- Small, focused functions
- Consistent error handling patterns

### Class Usage Guidelines (Framework Exception)
#### When Classes Are Permitted
- **CDK Constructs**: Classes required for CDK construct interfaces (extending Construct)
- **Framework Requirements**: Classes mandated by external frameworks/libraries
- **Mobile Development**: Platform-specific class requirements (iOS/Android)
- **Blockchain Development**: Smart contract class structures
- **[Project-Specific]**: [Any additional project-specific class requirements]

#### Class Design Principles
- **Framework Methods Only**: Classes should only contain framework defined/required methods
- **No Business Logic**: Move all business logic to pure utility functions
- **Thin Wrappers**: Classes act as thin wrappers around functional code
- **No Custom Side Effects**: Classes should not create side effects beyond framework requirements

### Dependencies
- **Package Manager**: [npm/yarn/go mod/cargo/pip - specify]
- **Dependency Policy**: Don't add new dependencies when simple solutions exist in a few lines of code
- **Approved Libraries**: [List pre-approved libraries/frameworks for the project]
- **Security Scanning**: All dependencies must pass security scans
- **License Compliance**: [Specify license requirements and restrictions]

### Git Workflow
- **Branch Strategy**: [main/develop, feature branches, etc.]
- **Commit Messages**: [Conventional commits/Custom format]
- **PR Requirements**: [Review requirements, CI/CD checks]
- **Merge Strategy**: [Squash/merge/rebase preference]
- **Pre-commit Hooks**: [Linting/Testing/Security scanning requirements]

### Development Environment
- **IDE**: [VSCode/IntelliJ/Vim - team preference]
- **Linting**: [ESLint/golangci-lint/specific tools]
- **Formatting**: [Prettier/gofmt/specific tools]
- **Debugging**: [Debugger setup and tools]
- **Local Development**: [Docker/VM/Native setup requirements]

### Testing Preferences

- Unit tests for business logic
- Integration tests for workflows
- E2E tests for critical paths
- Test behavior, not implementation
- Descriptive test names that explain the scenario

### Documentation Preferences

- README should include quick start
- API documentation with examples
- Architecture decisions recorded
- Inline documentation for complex logic
- Keep documentation close to code

### Deployment
- **Environment**: [AWS/GCP/Azure/local - specify]
- **Infrastructure**: [CDK/Terraform/specific tools]
- **CI/CD**: [GitHub Actions/Jenkins/specific pipeline]
- **Monitoring**: [CloudWatch/Grafana/specific tools]
- **Scaling**: [Auto-scaling/Load balancing requirements]

### Error Handling & Debugging
- **Error Reporting**: [Logging/Monitoring/Alerting setup]
- **Recovery Procedures**: [Rollback/Failover strategies]
- **Emergency Protocols**: [Critical issue response procedures]

## Project-Specific Rules

### [Feature/Domain Area 1]
- **Architecture Patterns**: [Specific patterns to follow]
- **Testing Requirements**: [Coverage and testing strategies]
- **Security Considerations**: [Specific security requirements]
- **Performance Requirements**: [Response time/throughput requirements]

### [Feature/Domain Area 2]
- **Integration Patterns**: [How this integrates with other components]
- **Data Handling**: [Data flow and storage requirements]
- **API Design**: [REST/GraphQL/gRPC specifications]
- **Documentation Requirements**: [API docs/User guides]

### [Feature/Domain Area 3]
- **Compliance Requirements**: [Regulatory/Legal requirements]
- **Monitoring**: [Metrics and alerting requirements]
- **Backup/Recovery**: [Data protection strategies]
- **Maintenance**: [Update/Patch procedures]

## Template Usage Notes

### Customization Instructions
- **Remove irrelevant sections**: Delete domains not applicable to your project
- **Specify technology choices**: Replace [Choose one] placeholders with actual selections
- **Add project-specific rules**: Extend with domain-specific requirements
- **Align with team preferences**: Adjust communication and workflow styles

### Integration with Delegation Rules
- **Main LLM coordination**: Direct coordination without orchestrator agent
- **User preferences**: This file contains delegation rules and project preferences
- **Global precedence**: This file overrides global ~/.claude/CLAUDE.md preferences
- **Agent definitions**: Can still override global agents in ./claude/agents/

### Validation Checklist
- [ ] Technology stack specified for all relevant domains
- [ ] Language preferences aligned with team
- [ ] Code style preferences documented
- [ ] Testing strategy and coverage requirements set
- [ ] Documentation standards defined
- [ ] Git workflow and branching strategy defined
- [ ] Security and compliance requirements specified
- [ ] Deployment and monitoring approach defined

## Notes
- This template includes mandatory delegation enforcement and project preferences
- Delegation rules are integrated directly into project CLAUDE.md
- Customize all [placeholder] sections for your specific project
- Remove sections not relevant to your project type