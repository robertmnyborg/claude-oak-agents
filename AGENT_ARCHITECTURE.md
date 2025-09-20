# Agent Architecture Documentation

## System Overview

The enhanced agent system features **21 specialized agents** with mandatory delegation enforcement that prevents main LLM bypass. The system uses trigger-based routing, direct coordination, and intelligent specialist selection to ensure proper task delegation.

## Architecture Diagram

```mermaid
graph TD
    User[User Request] --> MainLLM[Main LLM Coordinator]

    MainLLM --> DetectComplex{Complex Task<br/>Detection}

    DetectComplex -->|Action Verbs<br/>Multi-component<br/>Complex Patterns| Delegate[Direct Agent<br/>Delegation]
    DetectComplex -->|Simple Tasks| DirectResponse[Direct Response]

    Delegate --> Programming{Programming<br/>Task?}
    Delegate --> Infrastructure{Infrastructure<br/>Task?}
    Delegate --> Security{Security<br/>Task?}
    Delegate --> Quality{Quality<br/>Review?}
    Delegate --> Analysis{Analysis<br/>Task?}

    Programming -->|Core Programming| Programmer[programmer]
    Programming -->|Frontend/UI| FrontendDev[frontend-developer]
    Programming -->|Backend/API| BackendArch[backend-architect]
    Programming -->|ML/Data| MLEngineer[ml-engineer]
    Programming -->|Blockchain| BlockchainDev[blockchain-developer]
    Programming -->|Mobile| MobileDev[mobile-developer]
    Programming -->|Legacy Systems| LegacyMaint[legacy-maintainer]

    Infrastructure -->|CDK/Cloud| InfraSpec[infrastructure-specialist]
    Security -->|Security Analysis| SecAuditor[security-auditor]
    Quality -->|Code Review| CodeReviewer[code-reviewer]
    Quality -->|Testing| QASpec[qa-specialist]
    Analysis -->|Performance/Debug| AnalysisAgents[performance-optimizer<br/>debug-specialist]

    %% Workflow Dependencies
    Programmer --> QualityGate{Quality<br/>Gates Pass?}
    InfraSpec --> QualityGate

    QualityGate -->|Issues Found| CodeReviewer
    QualityGate -->|Tests Needed| UnitTest[unit-test-expert]
    QualityGate -->|Ready| GitOps[git-workflow-manager]

    CodeReviewer -->|Blocking Issues| Programmer
    CodeReviewer -->|Approved| UnitTest

    UnitTest --> GitOps
    GitOps --> Changelog[changelog-recorder]

    %% Rule Inheritance
    GlobalRules[Global Rules<br/>/Users/jamsa/.claude/CLAUDE.md] --> MainLLM
    LocalRules[Local Rules<br/>./CLAUDE.md] -->|Overrides| MainLLM

    GlobalAgents[Global Agents<br/>/Users/jamsa/.claude/agents/] --> AgentResolution{Agent<br/>Resolution}
    LocalAgents[Local Agents<br/>./claude/agents/] -->|Overrides| AgentResolution

    AgentResolution --> Programmer
    AgentResolution --> InfraSpec
    AgentResolution --> SecAuditor
    AgentResolution --> CodeReviewer

    %% Styling
    classDef coordinator fill:#ff9999,stroke:#333,stroke-width:3px
    classDef agent fill:#99ccff,stroke:#333,stroke-width:2px
    classDef workflow fill:#99ff99,stroke:#333,stroke-width:2px
    classDef config fill:#ffcc99,stroke:#333,stroke-width:2px

    class MainLLM coordinator
    class Programmer,InfraSpec,SecAuditor,CodeReviewer,UnitTest,GitOps,Changelog agent
    class QualityGate,DetectComplex,AgentResolution workflow
    class GlobalRules,LocalRules,GlobalAgents,LocalAgents config
```

## Coordination Flow

### 1. Task Detection Phase
```
User Request → Main LLM → Complex Task Detection
```

**Delegation Enforcement Triggers:**
- **Action Verbs**: implement, create, build, fix, deploy, test, add, update, refactor, improve, design, setup, configure, analyze, optimize, migrate, integrate, write, edit, modify, develop, code
- **File Operations**: ANY mention of Write, Edit, MultiEdit tools
- **Programming Keywords**: function, class, method, variable, API, database
- **Technical Implementation**: ANY technical work beyond coordination

### 2. Direct Agent Delegation
```
Main LLM → Task Analysis → Direct Agent Invocation
```

**Specialist Routing Rules:**
- **Core Programming** → `programmer` agent (language hierarchy: Go > TypeScript > Bash > Ruby)
- **Frontend/UI** → `frontend-developer` agent (React/Vue/Angular, browser compatibility)
- **Backend/API** → `backend-architect` agent (database design, microservices)
- **ML/Data** → `ml-engineer` agent (Python/TensorFlow, MLOps)
- **Blockchain** → `blockchain-developer` agent (Solidity, Web3, DeFi)
- **Mobile** → `mobile-developer` agent (React Native, iOS, Android)
- **Legacy Systems** → `legacy-maintainer` agent (Java, C#, enterprise)
- **Infrastructure** → `infrastructure-specialist` agent (CDK, cloud architecture)
- **Security** → `security-auditor` agent (penetration testing, compliance)
- **Testing** → `qa-specialist` agent (end-to-end, integration testing)
- **Quality Gates** → `code-reviewer` agent (mandatory quality validation)

### 3. Parallel Execution
```
Main LLM → Multiple Task() calls → Parallel Agent Execution
```

**Execution Pattern:**
```typescript
// Single message with multiple specialist tasks
Task(subagent_type="backend-architect", prompt="Design authentication API")
Task(subagent_type="frontend-developer", prompt="Implement auth UI components")
Task(subagent_type="security-auditor", prompt="Review auth security patterns")
Task(subagent_type="infrastructure-specialist", prompt="Setup auth infrastructure")
```

### 4. Workflow Coordination
```
Agent Results → Main LLM → Dependency Resolution → Next Actions
```

**Enhanced Quality Gate Workflow:**
1. **Code Implementation** (specialist agents: programmer, frontend-developer, backend-architect, etc.)
2. **Code Review** (code-reviewer) - *BLOCKS if security/quality issues found*
3. **Code Clarity** (code-clarity-manager → top-down-analyzer + bottom-up-analyzer)
4. **Test Coverage** (unit-test-expert) - *BLOCKS if coverage insufficient*
5. **Git Operations** (git-workflow-manager) - *Only after all quality gates pass*
6. **Documentation** (changelog-recorder)

## Rule Inheritance System

### Global Configuration
```
/Users/jamsa/.claude/
├── CLAUDE.md                    # Global rules and coordination logic
└── agents/
    ├── programmer.md            # Global programming agent
    ├── infrastructure-specialist.md
    ├── security-auditor.md
    └── code-reviewer.md
```

### Local Project Overrides
```
project/
├── .claude/
│   ├── agents/
│   │   ├── programmer.md        # Override: Python > TypeScript > Go
│   │   └── custom-validator.md  # Project-specific agent
│   └── CLAUDE.md                # Project-specific rules
└── src/
```

### Resolution Order
```mermaid
graph LR
    Request[Agent Request] --> LocalCheck{Local Agent<br/>Exists?}
    LocalCheck -->|Yes| LocalAgent[./claude/agents/agent.md]
    LocalCheck -->|No| GlobalAgent[/Users/jamsa/.claude/agents/agent.md]

    LocalAgent --> Execute[Execute Agent]
    GlobalAgent --> Execute

    GlobalRules[Global CLAUDE.md] --> RuleCheck{Local Rules<br/>Override?}
    LocalClaudeRules[Local ./CLAUDE.md] -->|Yes| RuleCheck
    RuleCheck --> FinalRules[Final Rule Set]

    FinalRules --> Execute
```

## Agent Specializations

### Programmer Agent
**Domain**: ALL programming tasks
- Language hierarchy: Go > TypeScript > Bash > Ruby
- Functional programming enforcement
- NO CLASSES rule (except CDK constructs)
- Dependency minimalism
- Distributed architecture patterns

### Infrastructure-Specialist Agent
**Domain**: CDK and cloud infrastructure
- AWS CDK constructs exclusively
- Functional CDK patterns
- Cloud architecture design
- Deployment strategies
- Infrastructure monitoring

### Security-Auditor Agent
**Domain**: Security analysis and compliance
- Vulnerability detection
- Security pattern enforcement
- Compliance validation
- Threat analysis

### Code-Reviewer Agent
**Domain**: Quality gates and validation
- Code quality review
- Security vulnerability scan
- Test coverage validation
- Build/compilation verification
- BLOCKS workflow until issues resolved

## Workflow Dependencies

### Sequential Dependencies
```
Programming → Code Review → Testing → Git Operations → Documentation
```

### Parallel Opportunities
```
Architecture Planning: systems-architect + security-auditor (parallel)
Implementation: programmer + infrastructure-specialist (parallel when independent)
Analysis: performance-optimizer + debug-specialist (parallel)
```

### Blocking Conditions
```
debug-specialist: HIGHEST PRIORITY - blocks all other agents
code-reviewer: Blocks git operations until quality gates pass
unit-test-expert: Blocks commits until coverage requirements met
```

## Configuration Examples

### Global Language Preference
```markdown
# /Users/jamsa/.claude/CLAUDE.md
<AgentDelegationRules>
<Rule id="programming-delegation">
**PROGRAMMING DELEGATION**: ALL coding tasks → `programmer` agent
Language hierarchy: Go > TypeScript > Bash > Ruby
</Rule>
</AgentDelegationRules>
```

### Local Project Override
```markdown
# ./CLAUDE.md
<TechnologyConstraints>
<Rule id="language-hierarchy">
**PROJECT LANGUAGE HIERARCHY**: Python > TypeScript > Go
FRAMEWORK: FastAPI + React stack
</Rule>
</TechnologyConstraints>
```

### Local Agent Override
```markdown
# ./claude/agents/programmer.md
---
name: programmer
description: Python-focused programmer for this FastAPI project
---

## Technology Constraints
### Language Hierarchy (Project Override)
1. Python (FastAPI backend)
2. TypeScript (React frontend)
3. Bash (deployment scripts)
```

This architecture ensures clean separation of concerns, eliminates re-entrant coordination complexity, and provides flexible rule inheritance while maintaining the main LLM as the central coordinator.