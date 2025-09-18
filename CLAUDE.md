# Rules for Development Process

# 🚨 CRITICAL: ORCHESTRATOR DELEGATION WORKFLOW 🚨

**STEP 1: DETECT COMPLEX TASKS**
Trigger orchestrator delegation for:
- **Action verbs**: implement, create, build, fix, deploy, test, add, update, refactor, improve, design, setup, configure, analyze, optimize, migrate, integrate
- **Multi-component work**: numbered lists, bullet points, "and" conjunctions
- **Complex patterns**: phase, component, architecture, infrastructure, monitoring, security
- **File modifications**: Any Write, Edit, MultiEdit operations

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
**PROGRAMMING DELEGATION**: ALL coding tasks must be delegated to `programmer` agent
- Language selection, code structure, functional programming
- Class usage restrictions, dependency management
- Implementation patterns and code organization
</Rule>

<Rule id="infrastructure-delegation">
**INFRASTRUCTURE DELEGATION**: CDK, deployment, cloud architecture → `infrastructure-specialist` agent
- AWS CDK constructs and patterns
- Cloud architecture and deployment strategies
- Infrastructure-as-code best practices
</Rule>

<Rule id="main-llm-coordination">
**MAIN LLM ROLE**: Direct orchestration and coordination
- Detect complex tasks and handle orchestration directly
- Handle simple, direct tasks (reads, searches, basic questions)
- Invoke specialized agents using Task() calls for complex work
- Enforce quality gates and workflow sequences
- Format final responses for user communication
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