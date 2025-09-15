# Rules for Development Process

<PersistentRules>
<SelectiveOrchestration id="orchestrator-triggers">
⚠️ **SELECTIVE ORCHESTRATION - MANDATORY FOR SPECIFIC SCENARIOS** ⚠️

The agent-orchestrator MUST be invoked for these scenarios:
1. **Code Changes**: Any modification to source files (create, edit, refactor)
2. **Multi-Step Tasks**: Tasks requiring 3+ distinct operations
3. **Error/Debug Scenarios**: Build failures, test failures, runtime errors
4. **Architecture/Design**: System design, infrastructure planning, tech specs
5. **Complex Analysis**: Performance optimization, security audits, code reviews
6. **Project Setup**: New project initialization, major feature implementation
7. **Git Operations**: Commits, PR creation, branch management
8. **Data Analysis**: Processing uploaded data files (CSV, JSON, etc.)
9. **Testing Tasks**: Creating tests, improving coverage, test refactoring
10. **Agent System Work**: Creating or modifying agents

Invoke with: Task(subagent_type="agent-orchestrator", prompt="Plan workflow for: [specific task]")

SKIP orchestration for:
- Simple questions ("What is X?", "How does Y work?")
- File reading without modification
- Running single commands
- Explanations or documentation lookups
- Configuration checks
</SelectiveOrchestration>

<InfiniteRecursionPrevention id="orchestrator-validation">
🚨 **CRITICAL: PREVENT ORCHESTRATOR SELF-INVOCATION** 🚨
Before executing ANY Task calls from orchestrator JSON response:
1. VALIDATE that NO `subagent_type` equals "agent-orchestrator"
2. If found, REJECT the entire dispatch plan
3. Report error: "Orchestrator attempted self-invocation - infinite recursion prevented"
4. This prevents memory overflow and system crashes

The orchestrator uses `next_steps` field to request re-invocation, NOT Task calls.
</InfiniteRecursionPrevention>
</PersistentRules>

<TechnologyConstraints>
<Rule id="language-hierarchy">
**STRICT LANGUAGE HIERARCHY**: Go > TypeScript > Bash > Ruby
NEVER use: Java, C++, C#
</Rule>

<Rule id="cdk-framework">
**CDK EXCLUSIVE**: Use AWS CDK constructs and patterns exclusively for infrastructure
</Rule>

<Rule id="functional-programming">
**NO CLASSES RULE**: Functional programming approach - avoid creating JavaScript/TypeScript classes
EXCEPTION: CDK constructs only
</Rule>

<Rule id="minimal-dependencies">
**DEPENDENCY MINIMALISM**: Don't add new dependencies when simple solutions exist in a few lines of code
</Rule>

<Rule id="distributed-architecture">
**ARCHITECTURE PATTERN**: Distributed stack of functions (lambdas) or static assets, NOT single runtime
</Rule>
</TechnologyConstraints>

<ClassUsageGuidelines>
<PermittedCases>
CLASSES ARE ONLY ALLOWED FOR:
- **CDK Constructs**: Classes required for CDK construct interfaces (extending Construct)
- **Framework Requirements**: Classes mandated by external frameworks/libraries
</PermittedCases>

<ClassDesignPrinciples>
WHEN classes are used, they MUST follow these principles:
<Rule id="framework-methods-only">**Framework Methods Only**: Classes should only contain framework defined/required methods</Rule>
<Rule id="no-business-logic">**No Business Logic**: Move all business logic to pure utility functions</Rule>
<Rule id="thin-wrappers">**Thin Wrappers**: Classes act as thin wrappers around functional code</Rule>
<Rule id="no-side-effects">**No Custom Side Effects**: Classes should not create side effects beyond framework requirements</Rule>
<Rule id="no-external-calls">**No External Calls**: Classes should not make API calls, file system operations, or network requests</Rule>
<Rule id="no-global-state">**No Global State**: Classes should not modify global variables or singletons</Rule>
<Rule id="no-logging-metrics">**No Logging/Metrics**: Move logging and metrics collection to utility functions</Rule>
</ClassDesignPrinciples>
</ClassUsageGuidelines>

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