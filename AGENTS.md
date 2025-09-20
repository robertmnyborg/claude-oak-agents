# Agent System Architecture

## Overview

The Claude Code agent system uses a dispatch planner architecture where the **agent-coordinator** analyzes context and returns specific Task tool calls for maximum parallel execution. This creates an efficient workflow system that coordinates specialized agents while maintaining quality gates.

## How the Agent System Works

### 1. Dispatch Planning Architecture

The agent system operates through a **functional dispatch planner**:

1. **Main LLM invokes coordinator**: `Task(subagent_type="agent-coordinator", prompt="Plan workflow for [situation]")`
2. **Coordinator returns dispatch plan**: Specific Task calls to execute + re-invocation instructions
3. **Main LLM executes Task calls**: Runs the specified agents (in parallel when possible)
4. **Main LLM re-invokes coordinator**: With completion status using specified format
5. **Coordinator continues workflow**: Plans next parallel batch based on results

### 2. Maximum Parallelism Strategy

The coordinator is designed to **maximize parallel execution** at every opportunity:

#### Always Parallel (No conflicts ever)
- **Configuration agents**: `statusline-setup` + `output-style-setup`
- **Security + Documentation**: `security-auditor` + `technical-documentation-writer`
- **Data analysis + Documentation**: `data-scientist` + `technical-documentation-writer`
- **Planning agents**: `project-manager` + `systems-architect` + `security-auditor`

#### Contextually Parallel (When no code conflicts)
- **Analysis + Documentation**: Any analyzer + `technical-documentation-writer`
- **Testing + Documentation**: `unit-test-expert` + `technical-documentation-writer`
- **Git operations + Changelog**: `git-workflow-manager` + `changelog-recorder`
- **All utilities + Any workflow**: Configuration agents can run with anything

#### Maximum Batch Sizes by Phase
- **Planning Phase**: 3 agents (`project-manager` + `systems-architect` + `security-auditor`)
- **Analysis Phase**: 1 agent (`code-reviewer` - blocking quality gate)
- **Clarity Phase**: 1 agent (`code-clarity-manager` - internally runs 2 analyzers in parallel)
- **Testing Phase**: 2 agents (`unit-test-expert` + `technical-documentation-writer`)
- **Finalization Phase**: 3 agents (`git-workflow-manager` + `changelog-recorder` + `technical-documentation-writer`)
- **Utility Phase**: 2 agents (`statusline-setup` + `output-style-setup` - can run with any phase)

### 3. Workflow Examples

#### Code Change Workflow
```
Batch 1: code-reviewer (blocking quality gate)
Batch 2: code-clarity-manager (maintainability analysis)
Batch 3: unit-test-expert (test creation)
Batch 4: git-workflow-manager + changelog-recorder + technical-documentation-writer (parallel finalization)
Batch 5: statusline-setup + output-style-setup (utilities, can run with any batch)
```

#### Complex Project Workflow
```
Batch 1: project-manager + systems-architect + general-purpose (parallel planning)
Batch 2: technical-documentation-writer + unit-test-expert (parallel preparation)
Batch 3: [Implementation phases follow code change workflow]
```

### 4. Quality Gates

Sequential dependencies are enforced through quality gates:

1. **Security & Quality Gate**: `code-reviewer` blocks all downstream analysis
2. **Maintainability Gate**: `code-clarity-manager` blocks testing and commits
3. **Test Coverage Gate**: `unit-test-expert` blocks git operations
4. **Documentation Gate**: `technical-documentation-writer` (advisory, non-blocking)

### 5. Re-invocation Protocol

The main LLM re-invokes the coordinator using these exact formats:

**After successful completion:**
```
"Agent [agent-name] completed successfully. Results: [summary]. Continue workflow."
```

**After failure:**
```
"Agent [agent-name] failed with error: [error-details]. Adjust workflow."
```

**After multiple parallel agents:**
```
"Agents [agent-a, agent-b, agent-c] completed. Results: [summaries]. Continue workflow."
```

## Complete Agent Inventory

### Code Quality & Security Agents
- **code-reviewer**: Security analysis, code quality, vulnerability detection
- **code-clarity-manager**: Orchestrates maintainability analysis (runs top-down + bottom-up analyzers internally)
- **top-down-analyzer**: High-level architectural clarity analysis (invoked by code-clarity-manager)
- **bottom-up-analyzer**: Implementation-level clarity analysis (invoked by code-clarity-manager)
- **unit-test-expert**: Comprehensive unit test creation and coverage

### Development Workflow Agents
- **git-workflow-manager**: Git operations, branch management, PR creation
- **changelog-recorder**: Automatic changelog generation post-commit
- **debug-specialist**: Critical error resolution and debugging (blocks all other agents)

### Planning & Architecture Agents
- **project-manager**: Multi-step project breakdown and coordination
- **systems-architect**: System design, infrastructure planning, technical specifications
- **security-auditor**: Security analysis, vulnerability detection, compliance checking
- **performance-optimizer**: Performance analysis, bottleneck identification, optimization recommendations
- **infrastructure-specialist**: CDK constructs, cloud architecture, deployment strategies
- **dependency-scanner**: Third-party dependency analysis, vulnerability scanning, license compliance

### Documentation & Analysis Agents
- **technical-documentation-writer**: API docs, system documentation, technical writing
- **data-scientist**: Data analysis, insights, statistical processing

### Configuration Agents
- **statusline-setup**: Claude Code status line configuration
- **output-style-setup**: Claude Code output style customization

### Meta Agents
- **agent-creator**: Design and implement new specialized agents, update coordinator integration

## Priority Levels

```
1. HIGHEST: debug-specialist (blocks all other agents)
2. HIGH: code-reviewer (must pass before other analysis)
3. MEDIUM: code-clarity-manager, unit-test-expert, systems-architect
4. LOW: git-workflow-manager, changelog-recorder, technical-documentation-writer,
        project-manager, data-scientist, security-auditor, performance-optimizer,
        infrastructure-specialist, dependency-scanner
5. UTILITY: statusline-setup, output-style-setup, agent-creator (non-blocking, run as needed)
```

## Usage Instructions

### Initial Invocation
```
Task(subagent_type="agent-coordinator", description="Plan workflow", prompt="Analyze current context and create dispatch plan for [specific situation]")
```

### Examples
- "Plan workflow for code changes in authentication module"
- "Coordinate agents for new feature implementation"
- "Plan debugging workflow for test failures"
- "Set up comprehensive analysis for data processing feature"
- "Create new agent for API testing and validation"

## Auto-Agent Creation

### Capability Gap Detection
The coordinator automatically detects when specialized capabilities are needed and creates new agents on-demand:

**Example Auto-Creation Flow:**
1. **User Request**: "Test this REST API for performance"
2. **Gap Detection**: Coordinator detects no existing agent optimally handles API testing
3. **Auto-Creation**: Creates `api-tester` agent specialized for REST/GraphQL testing
4. **Task Execution**: New agent handles the original request with specialized expertise

### Supported Auto-Creation Domains
- **API Testing**: REST/GraphQL endpoint testing, performance validation
- **Database Migration**: PostgreSQL, MySQL, MongoDB migration tasks
- **Container Optimization**: Docker, Kubernetes, image optimization
- **Load Testing**: Stress testing, performance benchmarking
- **Accessibility Auditing**: WCAG compliance, screen reader testing
- **Mobile Development**: iOS, Android, React Native, Flutter
- **Blockchain Development**: Smart contracts, Web3, DeFi
- **Machine Learning**: Model training, data preprocessing
- **DevOps Automation**: CI/CD pipelines, deployment automation
- **Monitoring Setup**: Observability, alerting, metrics collection

### Quality Controls
- **Validation**: Auto-created agents undergo validation before first use
- **Conflict Prevention**: System prevents duplicate or overlapping capabilities
- **Naming Conventions**: Automatic adherence to agent naming standards
- **Integration Testing**: Ensures new agents integrate properly with existing workflows

## Key Benefits

1. **Maximum Efficiency**: Parallel execution wherever possible reduces total workflow time
2. **Quality Assurance**: Sequential quality gates ensure code standards are maintained
3. **Flexible Coordination**: Coordinator adapts workflow based on context and results
4. **Comprehensive Coverage**: All aspects of development are covered by specialized agents
5. **Automatic Recovery**: Failed agents trigger workflow adjustments through re-invocation
6. **Self-Evolving System**: Agent ecosystem grows automatically to meet new requirements
7. **Optimal Specialization**: Creates agents only when genuine capability gaps exist

This architecture ensures that Claude Code can handle complex, multi-step development tasks efficiently while maintaining high code quality and comprehensive analysis coverage. The system evolves automatically to meet new specialized requirements.