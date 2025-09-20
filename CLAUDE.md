# Rules for Development Process

# 🚨 CRITICAL: MANDATORY DELEGATION ENFORCEMENT 🚨

## MAIN LLM RESTRICTIONS (CANNOT BE BYPASSED)

**EXPLICITLY PROHIBITED ACTIONS FOR MAIN LLM:**
- ❌ **NO DIRECT PROGRAMMING**: Main LLM CANNOT write, edit, or modify any code
- ❌ **NO FILE MODIFICATIONS**: Main LLM CANNOT use Write, Edit, MultiEdit tools
- ❌ **NO IMPLEMENTATION WORK**: Main LLM CANNOT implement features, fixes, or solutions
- ❌ **NO TECHNICAL EXECUTION**: Main LLM CANNOT perform technical tasks beyond coordination

**MAIN LLM ROLE RESTRICTION**: Coordination, communication, and delegation ONLY

## MANDATORY DELEGATION TRIGGERS (NON-NEGOTIABLE)

**STEP 1: AUTOMATIC DELEGATION DETECTION**
These triggers FORCE delegation - no exceptions:
- **Action verbs**: implement, create, build, fix, deploy, test, add, update, refactor, improve, design, setup, configure, analyze, optimize, migrate, integrate, write, edit, modify, develop, code
- **File operations**: ANY mention of Write, Edit, MultiEdit, or file creation/modification
- **Multi-component work**: numbered lists, bullet points, "and" conjunctions
- **Complex patterns**: phase, component, architecture, infrastructure, monitoring, security
- **Programming requests**: ANY request involving code creation or modification

**STEP 2: DELEGATE TO ORCHESTRATOR**
Main LLM delegates complex coordination to specialized orchestrator agent:

```
Task(subagent_type="orchestrator", prompt="[detailed task description with full context]")
```

**STEP 3: ORCHESTRATOR HANDLES WORKFLOW**
The orchestrator agent manages:
- Agent delegation and coordination
- Quality gate enforcement
- Workflow state transitions
- Parallel execution coordination
- Result synthesis and reporting

**STEP 4: SIMPLE TASK DIRECT HANDLING**
Main LLM handles simple tasks directly:
- Single file reads
- Basic questions
- Simple searches
- User communication

**STEP 5: RESULT INTEGRATION**
- Orchestrator returns complete task results
- Main LLM formats final user response
- Quality gates already enforced by orchestrator
- Git operations already managed by orchestrator

---

<PersistentRules>

<AgentDelegationRules>
<Rule id="programming-delegation">
**PROGRAMMING DELEGATION**: ALL coding tasks MUST be delegated to `programmer` agent
- ⚠️ **ENFORCEMENT**: Main LLM CANNOT write any code directly
- ⚠️ **BYPASS DETECTION**: If main LLM attempts programming, immediately delegate
- Language selection, code structure, functional programming
- Class usage restrictions, dependency management
- Implementation patterns and code organization
</Rule>

<Rule id="mandatory-delegation-triggers">
**MANDATORY DELEGATION TRIGGERS**: Non-negotiable delegation requirements
- ⚠️ **Action verbs**: implement, create, build, fix, deploy, test, add, update, refactor, improve, design, setup, configure, analyze, optimize, migrate, integrate, write, edit, modify, develop, code
- ⚠️ **File operations**: Write, Edit, MultiEdit tools trigger automatic delegation
- ⚠️ **Programming keywords**: function, class, method, variable, API, database, etc.
- ⚠️ **Technical implementation**: ANY technical work beyond coordination
- **NO EXCEPTIONS**: These triggers cannot be ignored or bypassed
</Rule>

<Rule id="delegation-enforcement">
**DELEGATION ENFORCEMENT**: Automatic bypass prevention
- ⚠️ **IMMEDIATE DELEGATION**: No analysis or discussion before delegation
- ⚠️ **NO DIRECT EXECUTION**: Main LLM cannot attempt work before delegating
- ⚠️ **TRIGGER DETECTION**: Automatic pattern matching for delegation triggers
- ⚠️ **BYPASS BLOCKING**: System prevents main LLM from performing restricted actions
- **VIOLATION HANDLING**: Automatic redirect to appropriate specialist agent
</Rule>

<Rule id="infrastructure-delegation">
**INFRASTRUCTURE DELEGATION**: CDK, deployment, cloud architecture → `infrastructure-specialist` agent
- AWS CDK constructs and patterns
- Cloud architecture and deployment strategies
- Infrastructure-as-code best practices
</Rule>

<Rule id="main-llm-coordination">
**MAIN LLM ROLE**: Coordination and communication ONLY
- ✅ **ALLOWED**: Detect tasks and delegate to appropriate agents
- ✅ **ALLOWED**: Handle simple reads, searches, basic questions
- ✅ **ALLOWED**: Format responses and communicate with user
- ❌ **PROHIBITED**: Any direct implementation or technical work
- ❌ **PROHIBITED**: Using Write, Edit, MultiEdit tools
- ❌ **PROHIBITED**: Writing or modifying any code
- **ENFORCEMENT**: Automatic delegation for any prohibited actions
</Rule>

<Rule id="trigger-based-routing">
**TRIGGER-BASED ROUTING**: Automatic delegation detection
- **Programming triggers**: implement, create, build, fix, write, edit, modify, develop, code
- **Route to**: programmer agent (or specialist if project-specific routing exists)
- **File operation triggers**: Write, Edit, MultiEdit tool mentions
- **Route to**: Appropriate technical agent based on file type
- **Infrastructure triggers**: deploy, configure, cloud, CDK, infrastructure
- **Route to**: infrastructure-specialist agent
- **Security triggers**: audit, security, vulnerability, compliance
- **Route to**: security-auditor agent
- **Testing triggers**: test, qa, quality, performance, e2e
- **Route to**: qa-specialist agent
- **Analysis triggers**: analyze, requirements, user story, business
- **Route to**: business-analyst agent
- **Content triggers**: documentation, write content, marketing
- **Route to**: content-writer agent
</Rule>

<Rule id="specialist-routing">
**SPECIALIST AGENT ROUTING**: Project-specific overrides
- **ML/Data projects**: Python, TensorFlow, data pipeline → ml-engineer agent
- **Blockchain projects**: Solidity, Web3, DeFi → blockchain-developer agent
- **Mobile projects**: React Native, iOS, Android → mobile-developer agent
- **Legacy systems**: Java, C#, enterprise → legacy-maintainer agent
- **Check project context**: Look for package.json, requirements.txt, smart contracts
- **Default fallback**: Use standard programmer agent if no specialist matches
</Rule>

<Rule id="direct-orchestration">
**DIRECT ORCHESTRATION**: Main LLM manages workflow
- DETECT: Complex task patterns → Plan agent sequence directly
- DETECT: File modification operations → Invoke appropriate agents
- DETECT: Multi-step workflows → Execute step-by-step coordination
- INVOKE: Specialized agents using Task() calls with detailed context
- ENFORCE: Quality gates (code-reviewer → code-clarity-manager)
- COORDINATE: Sequential and parallel agent execution as needed
</Rule>

<Rule id="simple-task-handling">
**SIMPLE TASK DIRECT HANDLING**: Main LLM efficiency
- Single file reads → Handle directly
- Basic searches and questions → Handle directly
- User communication and formatting → Handle directly
- No workflow state management needed for simple tasks
</Rule>

<Rule id="agent-coordination">
**AGENT COORDINATION**: Direct workflow management
- Main LLM plans and executes agent sequences directly
- Programming work → Task(subagent_type="programmer", prompt="...")
- Quality gates → Task(subagent_type="code-reviewer", prompt="...")
- Infrastructure → Task(subagent_type="infrastructure-specialist", prompt="...")
- Wait for each agent completion before proceeding to next step
- Enforce mandatory quality sequence: code-reviewer → code-clarity-manager
- Handle parallel execution by sending multiple Task() calls in single message
</Rule>
</AgentDelegationRules>

<RuleInheritance>
<Rule id="local-overrides">
**LOCAL RULE OVERRIDES**: Project-specific rules can override global rules
- Local `./CLAUDE.md` overrides global `/Users/jamsa/.claude/CLAUDE.md`
- Local agents `./claude/agents/agent-name.md` override global agents
- Example: Local project can specify "Python > TypeScript" override
</Rule>

<Rule id="agent-overrides">
**AGENT OVERRIDE RESOLUTION**:
1. Check `./claude/agents/agent-name.md` (local project)
2. Fall back to `/Users/jamsa/.claude/agents/agent-name.md` (global)
3. Same agent name = complete override (not merge)
</Rule>
</RuleInheritance>

<CommunicationStyle>
<Rule id="direct-concise">**DIRECT AND CONCISE**: Communication must be direct and to the point</Rule>
<Rule id="no-apologies">**NO UNNECESSARY APOLOGIES**: Do not apologize or validate ideas unnecessarily</Rule>
<Rule id="technical-focus">**TECHNICAL FOCUS**: Skip pleasantries and focus on technical details</Rule>
<Rule id="completion-summary">**COMPLETION REPORTING**: Report completion with clear summary of work done</Rule>
</CommunicationStyle>

<ProjectStandards>
<Rule id="required-files">
**MANDATORY PROJECT FILES**: Every project MUST have:
- README.md
- SPEC.md
- CLAUDE.md
</Rule>

<Rule id="non-interactive-commands">
**NON-INTERACTIVE COMMANDS**: Always use --yes, --set-upstream flags when available
</Rule>

<Rule id="vscode-warnings">
**DEVELOPMENT NOTES**: VSCode GitHub warnings can be ignored (plugin issue)
</Rule>
</ProjectStandards>

<ThinkingProcess>
<Rule id="step-by-step">
For complex tasks, think step by step within <thinking></thinking> tags before responding
</Rule>

<Rule id="rule-acknowledgment">
ALWAYS acknowledge following CLAUDE.md rules at the start of responses
</Rule>

<Rule id="direct-coordination-phrases">
**DIRECT COORDINATION PHRASES**: Exact phrases for direct orchestration
- Complex task detected: "This requires coordinated agent workflow"
- Programming work: "Invoking programmer agent for implementation"
- Quality gates: "Now invoking code-reviewer for quality validation"
- Infrastructure: "Invoking infrastructure-specialist for deployment"
- Simple task: "Handling this directly as a simple task"
- Workflow completion: "All workflow steps completed successfully"
</Rule>

<Rule id="simplified-main-llm">
**SIMPLIFIED MAIN LLM WORKFLOW**: Direct coordination
- DETECT complex task → Plan and execute agent sequence directly
- HANDLE simple task → Process directly without agents
- COORDINATE agents → Use Task() calls with proper sequencing
- ENFORCE quality gates → Always invoke code-reviewer → code-clarity-manager
- FORMAT final response → Communicate results to user
</Rule>
</ThinkingProcess>