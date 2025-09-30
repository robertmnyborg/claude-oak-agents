# Agent System Architecture

## Overview

The Claude Code agent system features **24 specialized agents** with comprehensive overlap resolution, mandatory delegation enforcement, intelligent multi-agent coordination, and direct workflow management by the Main LLM. The system eliminates agent confusion through clear domain boundaries while enabling sophisticated multi-agent collaboration for complex cross-domain tasks.

## 🚨 Delegation Enforcement System

### Main LLM Restrictions
The main LLM is **EXPLICITLY PROHIBITED** from:
- ❌ Writing, editing, or modifying any code
- ❌ Using Write, Edit, MultiEdit tools
- ❌ Performing any technical implementation work
- ❌ Bypassing agent delegation

**Role Restriction**: Main LLM handles coordination, communication, and delegation ONLY.

### Automatic Delegation Triggers
These patterns **FORCE** delegation with no exceptions:
- **Action verbs**: implement, create, build, fix, deploy, test, add, update, refactor, improve, design, setup, configure, analyze, optimize, migrate, integrate, write, edit, modify, develop, code
- **File operations**: ANY mention of Write, Edit, MultiEdit
- **Programming keywords**: function, class, method, variable, API, database
- **Technical implementation**: ANY technical work beyond coordination

## How the Agent System Works

### Direct Coordination Architecture

The agent system operates through **direct Main LLM coordination**:

1. **Main LLM detects task complexity**: Analyzes request for delegation triggers
2. **Direct specialist delegation**: Main LLM invokes appropriate agents via Task() calls
3. **Quality gate enforcement**: Mandatory sequential validation before commits
4. **Parallel coordination**: Multiple Task() calls in single message for efficiency
5. **Result synthesis**: Main LLM combines agent outputs and communicates with user

### Maximum Parallelism Strategy

The Main LLM maximizes parallel execution wherever possible:

#### Parallel Execution Opportunities
- **Planning Phase**: `systems-architect` + `security-auditor` + `business-analyst`
- **Analysis Phase**: `performance-optimizer` + `dependency-scanner`
- **Documentation Phase**: `content-writer` + `technical-documentation-writer`
- **Security Phase**: `security-auditor` + `code-reviewer` (independent components)

#### Sequential Dependencies (Quality Gates)
1. **Mandatory Pre-Implementation**: `design-simplicity-advisor` (blocks ALL implementation)
2. **Implementation**: Appropriate specialist agent based on domain
3. **Code Review**: `code-reviewer` (blocks progression until quality gates pass)
4. **Testing**: `unit-test-expert` (validates implementation)
5. **Pre-Commit Simplicity**: `design-simplicity-advisor` (mandatory complexity review)
6. **Git Operations**: `git-workflow-manager` + `changelog-recorder`

#### Blocking Conditions
- **HIGHEST**: `debug-specialist` (blocks ALL other agents - critical errors only)
- **MANDATORY**: `design-simplicity-advisor` (blocks ALL implementation AND git operations)
- **HIGH**: `code-reviewer` (must pass before other analysis)
- **MEDIUM**: `unit-test-expert`
- **STANDARD**: All other agents based on dependencies

### Workflow Examples

#### Code Implementation Workflow
```
1. design-simplicity-advisor (MANDATORY pre-implementation)
2. programmer/specialist (implementation with simplicity constraints)
3. code-reviewer (quality gate validation)
4. unit-test-expert (test creation and coverage)
5. design-simplicity-advisor (MANDATORY pre-commit review)
6. git-workflow-manager + changelog-recorder (parallel finalization)
```

#### Complex Multi-Agent Coordination
```
User: "Build secure payment processing with mobile support"
System coordinates:
1. design-simplicity-advisor → simplicity-first architecture
2. systems-architect → security-focused design
3. backend-architect → payment API design
4. mobile-developer → mobile payment UI
5. security-auditor → security validation
6. qa-specialist → comprehensive testing
7. design-simplicity-advisor → pre-commit complexity review
```

#### Debug Priority Workflow
```
User: "Debug failing performance tests"
System coordinates:
1. debug-specialist (HIGHEST PRIORITY - blocks others)
2. performance-optimizer (analyze bottlenecks)
3. qa-specialist (test framework issues)
4. Main LLM synthesizes findings and solutions
```

### Quality Gates & Enforcement

Sequential dependencies are enforced through mandatory quality gates:

1. **Pre-Implementation Simplicity Gate**: `design-simplicity-advisor` blocks ALL implementation (MANDATORY)
2. **Security & Quality Gate**: `code-reviewer` blocks all downstream analysis
3. **Test Coverage Gate**: `unit-test-expert` blocks git operations
4. **Pre-Commit Simplicity Gate**: `design-simplicity-advisor` blocks ALL git operations (MANDATORY)
5. **Documentation Gate**: `technical-documentation-writer` (advisory, non-blocking)

### Multi-Agent Coordination Patterns

#### Coordination Types
1. **Sequential Quality Gates**: Implementation → code-reviewer → code-clarity-manager → unit-test-expert → design-simplicity-advisor → git-workflow-manager
2. **Parallel Analysis**: security-auditor + performance-optimizer + dependency-scanner
3. **Collaborative Architecture**: systems-architect → backend-architect + infrastructure-specialist
4. **Domain Collaboration**: Multiple specialists with Main LLM reconciliation

#### Conflict Resolution Rules
1. **Domain Priority**: More specific domain takes precedence
2. **Security First**: Security recommendations override performance/convenience
3. **Architecture Consistency**: Higher-level architecture decisions guide implementation
4. **User Requirements**: Business analyst requirements guide technical decisions
5. **Quality Gates**: Code reviewer decisions are non-negotiable

## Complete Agent Inventory (21 Agents)

### 🏗️ Core Development Agents
- **programmer**: Core programming tasks with language hierarchy (Go > TypeScript > Bash > Ruby)
- **frontend-developer**: UI/UX implementation, React/Vue/Angular, browser compatibility
- **backend-architect**: Database design, API architecture, microservices patterns
- **qa-specialist**: End-to-end testing, integration testing, performance validation
- **business-analyst**: Requirements analysis, user stories, stakeholder communication
- **content-writer**: Technical documentation, marketing content, API documentation

### 🔬 Specialist Programming Agents
- **ml-engineer**: Python/TensorFlow, data pipelines, MLOps practices
- **blockchain-developer**: Solidity smart contracts, Web3 integration, DeFi protocols
- **mobile-developer**: React Native, iOS, Android development
- **legacy-maintainer**: Java, C#, enterprise systems maintenance and modernization

### 🛡️ Security & Quality Agents
- **security-auditor**: Penetration testing, compliance validation (SOC2, GDPR, PCI DSS), threat modeling
- **code-reviewer**: Security analysis, code quality, vulnerability detection
- **code-clarity-manager**: System-wide maintainability orchestration (coordinates top-down + bottom-up analysis)
- **top-down-analyzer**: Architectural impact analysis across entire affected codebase
- **bottom-up-analyzer**: Implementation ripple effect analysis through dependent code
- **unit-test-expert**: Comprehensive unit test creation and coverage
- **design-simplicity-advisor**: KISS principle enforcement (MANDATORY before implementation AND commits)

### ⚙️ Infrastructure & Operations Agents
- **infrastructure-specialist**: CDK constructs, cloud architecture, deployment strategies
- **systems-architect**: System design, infrastructure planning, technical specifications
- **performance-optimizer**: Performance analysis, bottleneck identification, optimization
- **dependency-scanner**: Third-party dependency analysis, vulnerability scanning
- **debug-specialist**: Critical error resolution (highest priority, blocks all other agents)

### 📋 Workflow & Management Agents
- **git-workflow-manager**: Git operations, branch management, PR creation
- **changelog-recorder**: Automatic changelog generation post-commit
- **project-manager**: Multi-step project coordination
- **data-scientist**: Data analysis, insights, statistical processing
- **technical-documentation-writer**: API docs, system documentation, technical writing

### 🔧 Configuration & Meta Agents
- **agent-creator**: Design and implement new specialized agents
- **general-purpose**: Complex research, multi-domain tasks requiring broad knowledge

## Overlap Resolution & Domain Boundaries

### Agent Responsibility Matrix
Each agent has clearly defined primary responsibilities and explicit exclusions:

#### Primary Domains (Single Agent Ownership)
- **Testing Separation**: qa-specialist (execution) vs unit-test-expert (creation) vs performance-optimizer (analysis)
- **Security Layers**: security-auditor (auditing) + code-reviewer (quality gates) + dependency-scanner (supply chain)
- **Architecture Tiers**: systems-architect (design) + backend-architect (implementation) + infrastructure-specialist (deployment)
- **Documentation Split**: technical-documentation-writer (technical) vs content-writer (user-facing)
- **Analysis Domains**: data-scientist (data) vs performance-optimizer (performance) vs business-analyst (requirements)

#### Multi-Agent Coordination Examples
```yaml
"fix security vulnerability":
  agents: [security-auditor, code-reviewer, dependency-scanner]
  coordination: Parallel analysis → Main LLM synthesis → Implementation

"optimize slow database queries":
  agents: [performance-optimizer, backend-architect, infrastructure-specialist]
  coordination: Sequential analysis → Coordinated implementation

"debug failing tests":
  agents: [debug-specialist, qa-specialist, unit-test-expert]
  coordination: Debug priority → Testing expertise → Resolution
```

## Intelligent Routing System

### Trigger-Based Routing
Automatic agent selection based on request patterns:
```yaml
routing_triggers:
  programming: implement, create, build, fix → programmer (or specialist)
  infrastructure: deploy, configure, cloud → infrastructure-specialist
  security: audit, vulnerability, compliance → security-auditor
  testing: test, qa, performance → qa-specialist
  analysis: requirements, business, user story → business-analyst
  content: documentation, marketing → content-writer
```

### Specialist Selection by Context
```yaml
project_specialists:
  ml_projects: Python, TensorFlow, data → ml-engineer
  blockchain_projects: Solidity, Web3, DeFi → blockchain-developer
  mobile_projects: React Native, iOS, Android → mobile-developer
  legacy_systems: Java, C#, enterprise → legacy-maintainer
  frontend_files: src/components/, pages/, styles/ → frontend-developer
  backend_files: api/, services/, models/ → backend-architect
  infrastructure_files: cdk/, terraform/, docker/ → infrastructure-specialist
```

### Usage Examples

#### Simple Delegation
```bash
User: "Fix the authentication bug in login.ts"
System: Automatically routes to programmer agent
Result: Bug fixed, reviewed, tested, committed
```

#### Specialist Routing
```bash
User: "Optimize the ML model training pipeline"
System: Detects ML context, routes to ml-engineer specialist
Result: Specialized ML optimization with domain expertise
```

#### Complex Multi-Agent Coordination
```bash
User: "Build secure payment processing with mobile support"
System coordinates multiple specialists:
1. design-simplicity-advisor → simplicity-first architecture
2. systems-architect → security-focused design
3. backend-architect → payment API design
4. mobile-developer → mobile payment UI
5. security-auditor → security validation
6. qa-specialist → comprehensive testing
```

## Architecture Components

### Rule Inheritance System

#### Global Configuration
```
/Users/jamsa/.claude/
├── CLAUDE.md                    # Global rules and coordination logic
└── agents/
    ├── programmer.md            # Global programming agent
    ├── infrastructure-specialist.md
    ├── security-auditor.md
    └── code-reviewer.md
```

#### Local Project Overrides
```
project/
├── .claude/
│   ├── agents/
│   │   ├── programmer.md        # Override: Python > TypeScript > Go
│   │   └── custom-validator.md  # Project-specific agent
│   └── CLAUDE.md                # Project-specific rules
└── src/
```

#### Resolution Order
1. Check `./claude/agents/agent-name.md` (local project)
2. Fall back to `/Users/jamsa/.claude/agents/agent-name.md` (global)
3. Same agent name = complete override (not merge)

### Enforcement Mechanisms

#### Main LLM Restrictions
```yaml
prohibited_actions:
  - direct_programming: Cannot write/edit code
  - file_modifications: Cannot use Write/Edit/MultiEdit
  - technical_execution: Cannot perform implementation work
```

#### Agent Enforcement Reminders
Key agents include bypass detection:
```markdown
🚨 ENFORCEMENT REMINDER 🚨
IF MAIN LLM ATTEMPTS PROGRAMMING: This is a delegation bypass violation!
```

#### Mandatory Triggers
```yaml
mandatory_triggers:
  action_verbs: [implement, create, build, fix, etc.]
  file_operations: [Write, Edit, MultiEdit mentions]
  programming_keywords: [function, class, method, etc.]
```

## Key Benefits

1. **Overlap Elimination**: Clear domain boundaries prevent agent confusion
2. **Multi-Agent Coordination**: Sophisticated collaboration for cross-domain tasks
3. **Intelligent Trigger Detection**: Compound patterns invoke appropriate specialists
4. **Conflict Resolution**: Domain priority rules ensure coherent recommendations
5. **Comprehensive Coverage**: 21 specialized agents with coordinated workflows
6. **Mandatory Delegation**: Prevents Main LLM from performing technical work
7. **Quality Assurance**: Mandatory quality gates with multi-agent validation
8. **Maximum Efficiency**: Parallel execution wherever possible reduces workflow time
9. **Flexible Architecture**: Rule inheritance allows project-specific customization

## System Statistics

- **Total Agents**: 21 specialized agents with direct coordination
- **Overlap Resolution**: 8 major overlap categories eliminated
- **Multi-Agent Patterns**: 4 coordination workflow types implemented
- **Trigger Detection**: Compound pattern recognition for multi-agent scenarios
- **Conflict Resolution**: 6 priority rules for agent recommendation conflicts
- **Enforcement Layers**: 5 different bypass prevention mechanisms
- **Routing Rules**: Context-aware routing with file-path and project detection
- **Quality Gates**: 3 mandatory sequential quality checkpoints with multi-agent validation
- **Coordination**: Direct Main LLM coordination with sophisticated overlap resolution

This enhanced agent system represents a significant evolution in AI-assisted development, eliminating agent overlap confusion while enabling sophisticated multi-agent collaboration. The system provides comprehensive expertise through intelligent coordination, maintains strict quality standards, and prevents inappropriate Main LLM behavior while ensuring optimal task delegation and execution.