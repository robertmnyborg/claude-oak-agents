# Rules for Development Process

# 🚨 CRITICAL: DIRECT ORCHESTRATION WORKFLOW 🚨

**STEP 1: DETECT COMPLEX TASKS**
Trigger direct agent orchestration for:
- **Action verbs**: implement, create, build, fix, deploy, test, add, update, refactor, improve, design, setup, configure, analyze, optimize, migrate, integrate
- **Multi-component work**: numbered lists, bullet points, "and" conjunctions
- **Complex patterns**: phase, component, architecture, infrastructure, monitoring, security

**STEP 2: DIRECT AGENT DELEGATION**
Main LLM acts as orchestrator and directly invokes appropriate agents:

**Programming Work**: ALL coding tasks → `programmer` agent
```
Task(subagent_type="programmer", prompt="[specific programming task]")
```

**Infrastructure Work**: CDK, deployment, cloud architecture → `infrastructure-specialist` agent
```
Task(subagent_type="infrastructure-specialist", prompt="[infrastructure task]")
```

**Security Work**: Security analysis, vulnerability detection → `security-auditor` agent
```
Task(subagent_type="security-auditor", prompt="[security task]")
```

**Quality Gates**: Code review, testing validation → `code-reviewer` agent
```
Task(subagent_type="code-reviewer", prompt="[review task]")
```

**STEP 3: PARALLEL EXECUTION**
- Execute multiple agent tasks in parallel when possible
- Use single message with multiple Task calls for parallel execution
- Each agent operates independently with specialized rule domains

**STEP 4: WORKFLOW COORDINATION**
- Main LLM coordinates between agents based on task dependencies
- Quality gates (code-reviewer) block workflow until resolved
- Git operations only after all quality checks pass

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
**MAIN LLM ROLE**: Orchestration and coordination only
- Detect complex tasks requiring agent delegation
- Coordinate between agents based on dependencies
- NO direct programming work - delegate to specialist agents
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
</ThinkingProcess>