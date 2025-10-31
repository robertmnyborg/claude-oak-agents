# Rules for Development Process

# 🚨 CRITICAL: MANDATORY DELEGATION ENFORCEMENT 🚨

## AUTO-ACTIVATION SYSTEM (NEW - 2025-10-30)

**IMPORTANT**: This system now includes intelligent agent auto-activation:

- **Agent Auto-Activation Hook**: `.claude/hooks/agent-activation-prompt.md` analyzes prompts and suggests relevant agents
- **Agent Rules Configuration**: `.claude/agent-rules.json` defines trigger patterns, keywords, and confidence thresholds
- **Agent Patterns Guide**: `.claude/AGENT_PATTERNS.md` - comprehensive guide for agent selection and workflows
- **Post-Execution Tracking**: `.claude/hooks/post-agent-execution.md` logs performance metrics
- **Pre-Commit Validation**: `.claude/hooks/pre-commit-validation.md` enforces quality gates

**How It Works**:
1. User makes request
2. Auto-activation hook analyzes keywords, file context, and patterns
3. Suggests relevant agents based on `agent-rules.json`
4. User accepts or continues without agents
5. Execution tracked via telemetry for continuous improvement

**See `.claude/AGENT_PATTERNS.md` for complete agent selection guide, common workflows, and decision trees.**

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
- "Analyze system architecture" → ANALYSIS | Architecture | systems-architect + infrastructure-specialist | Medium

**NO BYPASS**: Main LLM CANNOT skip classification or execute without plan

## PRODUCT MANAGER CONTEXT

### For Product Managers Using This System

**What You Can Do**:
- Co-author feature specifications with spec-manager
- Design database schemas with backend-architect
- Create UI prototypes with frontend-developer
- Frame product strategy with product-strategist
- Create professional engineering handoffs with git-workflow-manager

**Key PM Agents**:
- **spec-manager**: Collaborative specification writing (Markdown + YAML)
- **product-strategist**: Eigenquestion methodology, success metrics, validation hypotheses
- **backend-architect**: Database schema, API design, DDL generation
- **frontend-developer**: React/Vue components, state stores (Redux/Zustand/Pinia)
- **git-workflow-manager**: Professional PRs with complete context for engineering
- **business-analyst**: Requirements analysis, evidence synthesis, stakeholder communication

**Note**: ux-designer archived (October 2025). User workflow and UX design now handled by product-strategist and business-analyst.

**PM Workflow Example**:
```
1. Frame Problem
   "Customer churn 15% monthly. Frame as product opportunity"
   → product-strategist: Eigenquestion + hypotheses + metrics

2. Create Spec
   "Create spec for guided onboarding feature"
   → spec-manager: Co-author with approval checkpoints

3. Design Data Layer
   "Design schema for onboarding progress tracking"
   → backend-architect: Schema + migrations + indexes

4. Prototype UI
   "Create React onboarding wizard components"
   → frontend-developer: Components + state store

5. Engineering Handoff
   "Create PR with spec, schema, prototype"
   → git-workflow-manager: Complete PR ready for review
```

**PM Documentation**:
- **Quick Start**: See `docs/PM_QUICK_START.md` for 6 detailed examples
- **Workflow Patterns**: See `docs/PM_WORKFLOWS.md` for 7 reusable patterns
- **Capabilities**: See `docs/PM_CAPABILITIES.md` for honest capability matrix
- **Documentation Hub**: See `docs/INDEX.md` for complete navigation by role

**How It Works for PMs**:
1. You make requests in plain language (no technical syntax needed)
2. System classifies request and selects appropriate PM agents
3. Agents coordinate automatically (you approve at checkpoints)
4. Output is PM-friendly (specs, diagrams, schemas, prototypes)
5. Engineering handoffs are professional and complete

**What's Automatic**:
- Agent selection based on your request type
- Multi-agent coordination for complex workflows
- Technical feasibility validation
- Quality checks and security reviews
- Documentation and changelog generation

**What Requires Your Input**:
- Approval checkpoints in specifications
- Design decisions and trade-offs
- Success metrics and validation criteria
- Business requirements and constraints

**Timeline Expectations**:
- Spec creation: 30-60 minutes (with your input)
- Database design: 10-20 minutes
- UI prototype: 20-40 minutes
- Complete feature handoff: 60-90 minutes (problem → engineering-ready)

## Model Selection Strategy

**Status**: Active - All agents assigned to optimal model tiers
**Documentation**: See `docs/MODEL_SELECTION_STRATEGY.md` for complete strategy

### Model Tiers

**Premium (Opus)** - Strategic planning, architecture, complex reasoning
- Use for: Business decisions, system design, nuanced tradeoffs
- Agents: systems-architect, design-simplicity-advisor, project-manager, product-strategist, business-analyst, agent-auditor
- Cost: High ($15-75/M tokens) | Speed: Slow (3-5s)

**Balanced (Sonnet)** - Standard development, code generation, debugging
- Use for: Most development tasks, code generation, refactoring, analysis
- Agents: All development specialists, quality-gate, security agents, most analysts
- Cost: Medium ($3-15/M tokens) | Speed: Normal (1-2s)

**Fast (Haiku)** - Execution tasks, templates, procedures
- Use for: Git operations, formatting, test generation, simple docs
- Agents: git-workflow-manager, unit-test-expert, qa-specialist, technical-writer, general-purpose
- Cost: Low ($1-5/M tokens) | Speed: Fast (300-500ms)

### When to Override Model Tier

**Upgrade to Premium** (Haiku/Sonnet → Opus):
- Critical business decisions or high-stakes architecture
- Multiple stakeholders with conflicting requirements
- Complex regulatory/compliance analysis
- Nuanced tradeoff analysis required

**Downgrade to Fast** (Sonnet → Haiku):
- Purely procedural tasks with well-defined templates
- High-frequency operations where speed matters
- Cost optimization needed for simple transforms

**Default Behavior**: Trust agent's assigned tier (already optimized)

### Expected Impact
- **21% cost savings** vs all-Sonnet baseline
- **3-10x faster** execution for Fast tier agents
- **Better strategic decisions** from Premium tier
- **Optimal balance** for majority (Balanced tier)

## Workflow Coordination (Phase 2A - Implemented)

### When to Track Workflows

Track multi-agent workflows when:
- **COORDINATION classification** detected (multiple agents required)
- **2+ agents** in execution plan
- **Complex project** requiring sequential or parallel agent execution

**Tracking is automatic** when environment variables are set by hooks integration.

### Phase 2A Implementation

Phase 2A implements minimal workflow tracking that links multi-agent invocations:

**Implementation Files**:
- `telemetry/workflow.py` - Workflow ID generation utility
- `telemetry/logger.py` - Extended with workflow_id parameter
- `scripts/query_workflow.sh` - Query tool for workflow analysis
- `hooks/pre_agent.sh` - Automatic workflow context injection

**Telemetry Schema Addition**:
```python
# workflow_id field added to invocations
{
  "invocation_id": "inv-20251021-abc123",
  "workflow_id": "wf-20251021-def456",      # NEW: Links related invocations
  "parent_invocation_id": "inv-20251021-xyz789",  # Links agent sequences
  "agent_name": "backend-architect",
  "timestamp": "2025-10-21T14:30:00Z",
  # ... other fields
}
```

**Workflow ID Generation**:
```python
from telemetry.workflow import generate_workflow_id

# Generate workflow ID for multi-agent coordination
workflow_id = generate_workflow_id()  # Returns: wf-YYYYMMDD-<uuid>

# Set environment for hooks
os.environ["OAK_WORKFLOW_ID"] = workflow_id
os.environ["OAK_PARENT_INVOCATION_ID"] = previous_invocation_id

# Execute agents (hooks will capture workflow context automatically)
execute_agent(agent_name, task)
```

**Hook Integration**:
The pre-agent hook (`hooks/pre_agent.sh`) automatically injects workflow context:
```bash
# Hook checks environment and passes to logger
if [ -n "$OAK_WORKFLOW_ID" ]; then
  export WORKFLOW_ID="$OAK_WORKFLOW_ID"
fi
if [ -n "$OAK_PARENT_INVOCATION_ID" ]; then
  export PARENT_INVOCATION_ID="$OAK_PARENT_INVOCATION_ID"
fi
```

### Agent Selection (Phase 3+ Feature)

Agent selection currently uses heuristic-based routing:
- Use existing CLAUDE.md classification rules
- Domain-based routing (API → backend-architect, Security → security-auditor, etc.)

**Future Enhancement** (Phase 3+):
- Query telemetry for historical performance data
- Confidence-based recommendations
- Statistical analysis after sufficient data (50+ workflows)

### Example: Multi-Agent Secure API Workflow

```python
# Example: Multi-agent secure API workflow
from telemetry.workflow import generate_workflow_id

workflow_id = generate_workflow_id()
parent_id = None

for agent in ["design-simplicity-advisor", "backend-architect", "security-auditor"]:
    os.environ["OAK_WORKFLOW_ID"] = workflow_id
    if parent_id:
        os.environ["OAK_PARENT_INVOCATION_ID"] = parent_id

    # Execute agent (hook automatically captures workflow context)
    parent_id = execute_agent(agent, task)
```

### Querying Workflows

Use the query script to analyze workflows:

```bash
# List all workflows
./scripts/query_workflow.sh --list-all

# List today's workflows
./scripts/query_workflow.sh --list-today

# Show specific workflow details
./scripts/query_workflow.sh wf-20251022-b71e4244

# Example output:
# Workflow: wf-20251022-b71e4244
# Invocations: 3
#
# 1. design-simplicity-advisor (inv-20251022-abc123)
#    Duration: 45.2s | Status: success
# 2. backend-architect (inv-20251022-def456)
#    Duration: 120.5s | Status: success | Parent: inv-20251022-abc123
# 3. security-auditor (inv-20251022-ghi789)
#    Duration: 78.3s | Status: success | Parent: inv-20251022-def456
```

### Benefits of Phase 2A

- **Link Related Invocations**: Track multi-agent workflows as unified sequences
- **Track Agent Sequences**: Use parent_invocation_id to follow agent handoffs
- **Query Workflows**: Simple shell script for workflow analysis
- **Backward Compatible**: workflow_id can be null for single-agent tasks
- **Foundation for Analysis**: Data structure ready for Phase 2B+ enhancements
- **Zero Breaking Changes**: Existing telemetry continues functioning normally

### Backward Compatibility

Phase 2A maintains full backward compatibility:
- **workflow_id can be null**: Single-agent invocations work without workflow tracking
- **No schema changes**: Only added optional fields to existing schema
- **Query tools handle both**: Scripts work with workflow and non-workflow invocations
- **Graceful degradation**: Missing workflow_id is handled transparently
- **Existing integrations unaffected**: No changes required to existing telemetry consumers

### Phase 2B/2C Future Work

**Phase 2B - Enhanced Query Tools** (After 10+ workflows):
- Workflow duration analysis and statistics
- Agent performance metrics per workflow type
- Bottleneck identification in agent sequences
- Success rate tracking by workflow pattern

**Phase 2C - Statistical Analysis** (After 50+ workflows):
- Confidence scoring for agent selection
- Historical performance-based recommendations
- Workflow pattern optimization suggestions
- Predictive duration estimates

**Phase 3+ - Advanced Features**:
- Structured artifact files for agent handoffs
- Real-time workflow monitoring dashboard
- Automated workflow optimization
- Machine learning-based agent selection

## Hybrid Planning Model (Phase 3 - Implemented)

### Overview

The Hybrid Planning Model combines top-down strategic planning with bottom-up implementation expertise. This mirrors real engineering teams where executives set direction, individual contributors propose implementation options, and leadership reviews and refines the plan before execution.

**Key Principle**: Strategic planning at the top, implementation planning from domain experts, synthesis and refinement by leadership, then execution.

### When to Use Hybrid Planning

**MANDATORY for:**
- Risk level: HIGH or CRITICAL
- Estimated time: >4 hours
- Number of agents: ≥4
- Security-critical changes (authentication, authorization, data protection)
- Data migrations or schema changes
- Architecture decisions

**RECOMMENDED for:**
- Complexity: HIGH + Novelty: HIGH
- Cost of failure: >2 hours of rework
- Cross-domain integration (2+ domains)
- Novel solutions without established patterns

**SKIP for:**
- Simple tasks (single agent, <1 hour)
- Well-understood patterns
- Low-risk changes
- Bug fixes (unless security-related)

### Workflow Structure

The hybrid planning model has 4 distinct phases:

```yaml
phase_1_strategic_planning:
  participants: [Main LLM, design-simplicity-advisor, project-manager]
  outputs:
    - task_assignments: "Which agents handle which responsibilities"
    - constraints: "Requirements, limitations, business rules"
    - context: "Codebase state, available tools, timeline"
  duration: "10-30 minutes"

phase_2_implementation_planning:
  mode: parallel
  participants: [all_assigned_execution_agents]
  each_agent_outputs:
    - options: "[2-3 implementation approaches]"
    - trade_offs: "[pros, cons, risks for each option]"
    - estimates: "[time, complexity, dependencies]"
    - recommendation: "preferred option with rationale"
  duration: "5-20 minutes per agent (parallel)"

phase_3_plan_review:
  mode: parallel
  participants: [project-manager, state-analyzer, product-strategist, design-simplicity-advisor]
  validates:
    - technical_feasibility: "Can this actually work?"
    - requirement_alignment: "Does this solve the stated goal?"
    - conflict_detection: "Do agent plans contradict each other?"
    - simplicity_check: "Is this over-engineered?"
    - dependency_validation: "Are cross-agent dependencies valid?"
  outputs:
    - refined_plan: "Synthesized plan incorporating best options"
    - risk_warnings: "Identified risks requiring mitigation"
    - go_no_go: "Proceed with execution or re-plan"
  duration: "10-20 minutes"

phase_4_execution:
  mode: sequential_or_parallel
  participants: [execution_agents_with_refined_tasks]
  inputs: "Refined plan from Phase 3"
  outputs: "Implemented solution"
  duration: "Varies by task complexity"
```

### Decision Matrix for Workflow Selection

```python
def select_workflow_type(task):
    """
    Determines whether to use simple delegation or hybrid planning.
    """
    # MANDATORY hybrid planning triggers
    if task.risk_level in ["high", "critical"]:
        return "hybrid_planning"
    if task.estimated_time_hours > 4:
        return "hybrid_planning"
    if task.num_required_agents >= 4:
        return "hybrid_planning"
    if task.security_critical:
        return "hybrid_planning"

    # RECOMMENDED hybrid planning triggers
    if task.complexity == "high" and task.novelty == "high":
        return "hybrid_planning"
    if task.num_domains >= 2 and task.integration_complexity == "high":
        return "hybrid_planning"
    if task.cost_of_failure_hours > 2:
        return "hybrid_planning"

    # Simple delegation for everything else
    return "simple_delegation"
```

### Agent Modes

All execution agents now support two modes:

**1. Planning Mode** (Phase 2)
- Input: Task description, constraints, context
- Output: 2-3 implementation options with trade-offs
- Focus: Exploration and analysis
- Duration: 5-15 minutes

**2. Execution Mode** (Phase 4)
- Input: Refined task with selected approach
- Output: Implemented solution
- Focus: Implementation
- Duration: Varies

### Planning Mode Output Format

All execution agents in planning mode must output this structure:

```yaml
agent_plan:
  agent_name: "backend-architect"
  task: "Implement OAuth2 endpoints"

  implementation_options:
    option_a:
      approach: "Use Passport.js OAuth2 strategy"
      description: "Leverage battle-tested OAuth2 library"
      pros:
        - "Well-documented with extensive community support"
        - "Quick implementation (4 hours)"
        - "Handles edge cases automatically"
      cons:
        - "External dependency (~200KB)"
        - "Less control over implementation details"
      time_estimate_hours: 4
      complexity: "low"
      risks:
        - "Dependency maintenance burden"
        - "Potential version conflicts"
      dependencies:
        - "npm: passport"
        - "npm: passport-oauth2"

    option_b:
      approach: "Custom OAuth2 implementation"
      description: "Build from scratch using Node crypto"
      pros:
        - "Zero external dependencies"
        - "Full control over implementation"
        - "Optimized for specific use case"
      cons:
        - "Higher security risk (easy to make mistakes)"
        - "Longer development time"
        - "Requires comprehensive security audit"
      time_estimate_hours: 12
      complexity: "high"
      risks:
        - "OAuth2 spec compliance errors"
        - "Security vulnerabilities"
        - "Missing edge case handling"
      dependencies: []

    option_c:
      approach: "Minimal OAuth2 subset (authorization_code only)"
      description: "Implement only core authorization_code flow"
      pros:
        - "Simpler than full OAuth2 spec"
        - "Zero dependencies"
        - "Faster than Option B (8 hours)"
        - "Can extend later if needed"
      cons:
        - "Limited functionality initially"
        - "May require refactoring for advanced flows"
      time_estimate_hours: 8
      complexity: "medium"
      risks:
        - "Feature gaps for advanced use cases"
        - "Potential rework if requirements expand"
      dependencies: []

  recommendation:
    selected: "option_c"
    rationale: "Balances zero-dependency requirement with reasonable implementation time. YAGNI principle - implement what's needed now, extend later if required."
    conditions:
      - "Requires security-auditor review before production"
      - "Document limitations for future extensibility"
      - "Plan migration path to full OAuth2 if needed"
```

### Review Agent Responsibilities

**project-manager (Plan Synthesis)**:
- Detect conflicts between agent plans
- Validate cross-agent dependencies
- Aggregate time estimates
- Synthesize final execution plan
- Identify blockers and risks

**state-analyzer (Technical Validation)**:
- Verify technical feasibility
- Check compatibility with existing codebase
- Validate dependency assumptions
- Assess infrastructure requirements

**product-strategist (Business Alignment)**:
- Validate against business objectives
- Ensure user value delivery
- Check success criteria alignment
- Verify scope appropriateness

**design-simplicity-advisor (Complexity Review)**:
- Identify over-engineering
- Recommend simpler alternatives
- Validate KISS principle adherence
- Challenge unnecessary complexity

### Example: Hybrid Planning Workflow

**User Request**: "Implement OAuth2 authentication with JWT tokens"

**Phase 1: Strategic Planning** (15 minutes)
```
Main LLM: Classifies as IMPLEMENTATION, HIGH risk, COMPLEX
  ↓
design-simplicity-advisor: "Custom OAuth2 justified for control, but recommend minimal implementation"
  ↓
project-manager: Creates strategic plan
  - Task 1: OAuth2 endpoints → backend-architect
  - Task 2: Security review → security-auditor
  - Task 3: JWT handling → backend-architect
  - Task 4: Frontend integration → frontend-developer
  - Task 5: Testing → unit-test-expert + qa-specialist

Decision: Use hybrid planning (HIGH risk + 5 agents)
```

**Phase 2: Implementation Planning** (Parallel, 10 minutes)
```
backend-architect: Proposes 3 options
  - Option A: Passport.js (4hrs, dependency)
  - Option B: Custom full OAuth2 (12hrs, risky)
  - Option C: Minimal OAuth2 (8hrs, extensible) ← Recommends

security-auditor: Proposes 2 options
  - Option A: JWT in httpOnly cookies (XSS safe) ← Recommends
  - Option B: JWT in localStorage (XSS risky)

frontend-developer: Proposes 2 options
  - Option A: Context API (simple) ← Recommends
  - Option B: Redux (overkill)

unit-test-expert: Proposes 1 approach
  - Comprehensive test suite (3hrs)
```

**Phase 3: Plan Review** (Parallel, 10 minutes)
```
project-manager:
  - backend Option C + security Option A = Compatible ✓
  - Total time: 8hrs (backend) + 3hrs (tests) + 2hrs (frontend) = 13hrs
  - Missing: HTTPS requirement for cookies
  - Action: Add infrastructure-specialist for HTTPS setup

state-analyzer:
  - Validates: TypeScript codebase supports all approaches
  - Identifies: No existing OAuth2 code to conflict with
  - Warns: JWT library needed (jwt-simple or custom)

product-strategist:
  - Validates: Minimal OAuth2 meets current requirements
  - Approves: Extension path exists for future needs
  - Confirms: Aligns with "ship fast, iterate" strategy

design-simplicity-advisor:
  - Approves backend Option C (minimal is good)
  - Approves security Option A (standard approach)
  - Approves frontend Option A (simple is sufficient)
  - Flags: Consider if OAuth2 is needed vs simple sessions

Synthesis:
  - Proceed with backend Option C, security Option A, frontend Option A
  - Add infrastructure-specialist for HTTPS
  - Add jwt-simple dependency (lightweight)
  - Refined estimate: 14 hours
```

**Phase 4: Execution** (14 hours)
```
infrastructure-specialist: Sets up HTTPS (1hr)
backend-architect: Implements minimal OAuth2 (8hrs)
security-auditor: Reviews implementation (1hr)
frontend-developer: Integrates auth flow (2hrs)
unit-test-expert: Comprehensive tests (3hrs)
git-workflow-manager: Commits changes
```

### Benefits of Hybrid Planning

1. **Early Conflict Detection**: Discover incompatibilities during planning, not execution
2. **Better Estimates**: Domain experts provide accurate time estimates
3. **Risk Mitigation**: Identify and address risks before committing resources
4. **Knowledge Capture**: Planning discussions generate valuable learning data
5. **Optimized Solutions**: Review process selects best options from multiple proposals
6. **Reduced Rework**: Validation prevents expensive implementation mistakes

### Telemetry Integration

Planning phases are tracked in telemetry:

```json
{
  "invocation_id": "inv-20251022-abc123",
  "workflow_id": "wf-20251022-def456",
  "agent_name": "backend-architect",
  "mode": "planning",
  "phase": "implementation_planning",
  "options_proposed": 3,
  "recommended_option": "option_c",
  "timestamp": "2025-10-22T14:30:00Z"
}
```

This enables analysis of:
- Planning accuracy (estimated vs actual time)
- Option selection patterns
- Review effectiveness (conflicts caught)
- Planning ROI (planning time vs rework prevented)

---

<PersistentRules>

<AgentDelegationRules>
<Rule id="delegation-enforcement">
**DELEGATION ENFORCEMENT**: Zero tolerance implementation
- 🚨 **NO MAIN LLM IMPLEMENTATION**: Absolute prohibition on coding/implementation
- **DOMAIN ROUTING**: Frontend→frontend-developer, Backend→backend-architect, Infrastructure→infrastructure-specialist
- **TRIGGERS**: Action verbs (implement, create, build, fix, etc.), file operations (Write, Edit, MultiEdit), programming keywords (function, class, API, etc.), multi-line requests, complex analysis
- **IMMEDIATE DELEGATION**: No analysis before delegation, cannot break down tasks to avoid delegation
- **NO BYPASS**: Emergency/urgency cannot override, general-purpose restricted to single-line commands only
- **ENFORCEMENT**: Automatic pattern matching, immediate redirect to specialists
</Rule>

<Rule id="main-llm-coordination">
**MAIN LLM ROLE**: Coordination and communication ONLY
- ✅ **ALLOWED**: Task detection/delegation, simple reads/searches/questions (single-line), response formatting, language hierarchy coordination
- ❌ **PROHIBITED**: Implementation, file modifications, coding, multi-line tasks, scripting/automation
- **WORKFLOW**: specialist → quality-gate (unified validation) → git-workflow-manager
</Rule>

<Rule id="agent-responsibility-matrix">
**AGENT RESPONSIBILITY MATRIX**: Domain boundaries with mandatory classification

### Classification Integration
- **ALL REQUESTS**: Must be classified before agent selection
- **IMPLEMENTATION**: Requires domain identification and simplicity analysis
- **INFORMATION**: Simple → direct handling, Complex → analyst delegation
- **ANALYSIS**: Route to appropriate analyst based on domain
- **COORDINATION**: Multi-agent workflow with defined sequence

#### Core Development
- **frontend-developer**: UI/UX, client-side (TS/Vue > TS/React > JS/HTML, functional over OOP, Vue > React > Angular)
- **backend-architect**: API, database, server logic (Go > TS > JS, functional over OOP, SOA thinking)

#### Quality & Security
- **quality-gate**: Unified code review, maintainability analysis, architectural impact assessment, and implementation complexity validation
- **unit-test-expert**: Unit test creation, coverage validation
- **security-auditor**: Penetration testing, compliance, threat modeling
- **dependency-scanner**: Supply chain security, license compliance, vulnerabilities

#### Infrastructure & Operations
- **infrastructure-specialist**: CDK/Terraform, cloud deployment (TS/CDK > Go/CDK > Python/CDK, Lambda > ECS > K8s)
- **systems-architect**: High-level design, technical specifications

#### Workflow & Management
- **project-manager**: Multi-step coordination, timeline management
- **spec-manager**: Specification-driven development workflow, co-authoring specs, task decomposition
- **git-workflow-manager**: Git operations, branch management, PR creation

#### Analysis & Documentation
- **business-analyst**: Requirements, user stories, stakeholder communication
- **technical-writer**: Context-aware documentation for all audiences (technical, user-facing, marketing)

#### Special Purpose
- **design-simplicity-advisor**: KISS enforcement, MANDATORY before implementation and pre-commit
- **debug-specialist**: Critical error resolution (HIGHEST PRIORITY)
- **qa-specialist**: Integration testing, E2E, system validation
- **general-purpose**: RESTRICTED - single-line commands/basic queries ONLY
- **agent-creator**: Meta-agent creation
- **agent-auditor**: Agent portfolio management, capability gap detection, redundancy elimination (Agentic HR)

#### Multi-Agent Coordination
- **Security**: security-auditor + quality-gate + dependency-scanner → Main LLM synthesis
- **Architecture**: systems-architect → backend-architect + infrastructure-specialist → Main LLM integration
- **Testing**: unit-test-expert + qa-specialist → Main LLM comprehensive approach

#### Exclusion Rules (What agents DON'T handle)
- **design-simplicity-advisor**: No implementation (analysis only)
- **general-purpose**: No implementation/multi-line tasks/scripting (single-line commands only)
- **Domain boundaries**: Frontend≠backend≠infrastructure
- **Cross-domain**: Utility scripts→infrastructure-specialist (automation) OR backend-architect (data processing)

#### Archived Agents (October 2025)
**Note**: 16 agents archived as part of portfolio optimization to reduce redundancy and improve workflow efficiency.

**Consolidated Agents**:
- **quality-gate** (consolidates 4 agents): code-reviewer, code-clarity-manager, top-down-analyzer, bottom-up-analyzer
- **technical-writer** (consolidates 2 agents): content-writer, technical-documentation-writer

**Archived Unused Agents**:
- mobile-developer, blockchain-developer, ml-engineer, legacy-maintainer
- deployment-manager, changelog-recorder, data-scientist, ux-designer
- performance-optimizer, prompt-engineer

**Reactivation**: See `agents/archived/ARCHIVAL_RECORD.md` for reactivation procedures if specific capabilities are needed.
</Rule>

<Rule id="classification-precedence">
**CLASSIFICATION PRECEDENCE**: Request type determines workflow

### CLASSIFICATION ORDER (MANDATORY)
1. **EMERGENCY**: debug-specialist ALWAYS highest priority (blocks all others)
2. **CLASSIFICATION**: All requests must be classified before processing
3. **DOMAIN IDENTIFICATION**: Implementation requires specific domain specialist
4. **WORKFLOW SELECTION**: Based on classification and complexity
5. **EXECUTION**: Follow plan without bypass options

### CLASSIFICATION ROUTING
- **INFORMATION** (Simple): Direct Main LLM handling - file reads, basic questions, definitions
- **INFORMATION** (Complex): business-analyst or domain analyst
- **IMPLEMENTATION**: domain specialist → quality-gate (unified validation) → git-workflow-manager
- **ANALYSIS**: Route to appropriate analyst (business-analyst, security-auditor)
- **COORDINATION**: Multi-agent workflow with Main LLM orchestration

### MANDATORY CLASSIFICATION OUTPUT
```
CLASSIFICATION: [INFORMATION|IMPLEMENTATION|ANALYSIS|COORDINATION]
DOMAINS: [Primary domains identified]
AGENT PLAN: [Specific workflow sequence]
COMPLEXITY: [Simple|Medium|Complex]
```

### ANTI-BYPASS ENFORCEMENT
- **NO CLASSIFICATION SKIP**: Every request must be explicitly classified
- **NO PLAN BYPASS**: Cannot execute without documented agent plan
- **NO IMPLEMENTATION WITHOUT SIMPLICITY**: design-simplicity-advisor mandatory for all implementation
- **ERROR CONTEXT**: Error messages/stack traces = IMPLEMENTATION classification automatically
</Rule>

<Rule id="error-classification">
**ERROR CLASSIFICATION**: Automatic IMPLEMENTATION classification for errors

### Error Detection as Implementation
- **ALL ERROR MESSAGES** automatically classified as IMPLEMENTATION
- **STACK TRACES/ERROR LOGS** = implicit implementation request
- **"This is failing/broken"** = implementation classification
- **NO INFORMATION CLASSIFICATION** for errors (always implementation)

### Error Domain Detection
- **CDK/CloudFormation/Deployment errors** → Infrastructure domain
- **Frontend errors** (JavaScript, React, Vue) → Frontend domain
- **Backend errors** (API, database, server) → Backend domain

### Emergency Error Priority
- **Production/Critical errors** → debug-specialist (HIGHEST PRIORITY)
- **Non-critical errors** → appropriate domain specialist via normal workflow

### Error Implementation Workflow
```
Error Detection → IMPLEMENTATION Classification → Domain Identification → debug-specialist (if critical) OR design-simplicity-advisor → domain specialist → quality-gate → git-workflow-manager
```

### No Error Explanation Without Fix
- **NO INFORMATION RESPONSES** to error messages
- **MANDATORY IMPLEMENTATION** workflow for all errors
- **CONTEXT ANALYSIS** only for domain specialist routing
</Rule>

<Rule id="domain-identification">
**DOMAIN IDENTIFICATION**: Explicit matching or failure

### Detection Process
1. **ANALYZE**: Domain keywords, file paths, context
2. **MATCH**: Map to specific specialist using trigger hierarchy
3. **VERIFY**: Specialist handles work type
4. **FAIL EXPLICITLY**: If no match, state failure

### Routing Decision
Implementation → Domain keywords? → Route to specialist
            → File path? → Route by file type
            → Technology? → Route by tech
            → No domain? → FAIL: "Cannot identify specialist"

### Requirements
- **Explicit names**: Use exact agent names (frontend-developer, backend-architect, etc.)
- **No vague routing**: Cannot use "appropriate specialist"
- **Cross-domain**: Coordinate multiple specialists when spanning domains
- **Fail fast**: Better explicit failure than incorrect routing
</Rule>

<Rule id="capability-gap-detection">
**CAPABILITY GAP DETECTION**: Automatic agent creation when no suitable agent exists

### Gap Detection Workflow
```
Request → Classification → Domain Identification → Agent Matching
                                                          ↓
                                                    NO MATCH FOUND
                                                          ↓
                                               Log Routing Failure
                                                          ↓
                                            Invoke agent-creator
                                                          ↓
                                            Create New Agent
                                                          ↓
                                                   Retry Request
```

### When to Create New Agent (Automatic)
**IMMEDIATE CREATION** (Real-Time):
- User explicitly requests new capability: "I need an agent for financial analysis"
- Classification succeeds BUT no agent matches domain
- Domain is well-defined and distinct from existing agents

**DEFERRED CREATION** (Monthly via agent-auditor):
- 10+ routing failures for same domain in 30 days
- Pattern of suboptimal routing (using wrong agent repeatedly)
- User feedback indicates missing capability

### Gap Detection Triggers
```yaml
immediate_triggers:
  explicit_request: "create agent for [domain]" OR "I need [domain] capability"
  routing_failure: Classification→Domain→NO AGENT FOUND

  conditions:
    domain_is_distinct: true
    no_existing_overlap: true
    user_confirmed: true OR routing_failures >= 3

deferred_triggers:
  routing_failure_pattern: failures_for_domain >= 10 in 30_days
  suboptimal_routing: wrong_agent_used >= 5 in 30_days
  agent_auditor_recommendation: gap detected in monthly audit
```

### Automatic Agent Creation Process
1. **Detect Gap**: Main LLM cannot match request to suitable agent
2. **Log Failure**: Record routing failure with domain and context
3. **Check Threshold**:
   - Explicit request? → Create immediately
   - 3+ failures same domain? → Create immediately
   - Otherwise → Log for monthly agent-auditor review
4. **Invoke agent-creator**: Pass domain, context, and requirements
5. **Create Agent**: agent-creator designs and implements new agent following template
6. **Save for Review**: Agent saved to `agents/pending_review/` directory
7. **Notify User**: Notification sent - "New agent ready for review"
8. **Wait for Approval**: User reviews agent specification
9. **User Decision**:
   - **Approve**: Move to `agents/` directory, deploy immediately
   - **Modify**: User edits, then approves
   - **Reject**: Archive to `agents/rejected/`, log reasoning
10. **Deploy**: Agent becomes active and available for delegation
11. **Register**: Add to agent-auditor monitoring
12. **Future Updates**: After first approval, system can auto-update based on learning

### Agent Creation Examples

**Example 1: Financial Analysis**
```
User: "Analyze the ROI of this investment portfolio"
Main LLM Classification: ANALYSIS | Financial
Domain Identification: financial-analysis
Agent Matching: NO MATCH (no financial-analyst exists)
Gap Detection: Domain distinct, well-defined
Action: Invoke agent-creator
Specification:
  - name: financial-analyst
  - domain: financial-analysis
  - capabilities: ROI analysis, portfolio evaluation, financial modeling
  - context: User needs investment analysis
Created: financial-analyst agent
Retry: Delegate to new financial-analyst
```

**Example 2: Research Tasks**
```
User: "Research best practices for OAuth2 implementation"
Main LLM Classification: ANALYSIS | Research
Domain Identification: research
Agent Matching: NO CLEAR MATCH (general-purpose too generic)
Gap Detection: Research is distinct capability
Action: Invoke agent-creator
Specification:
  - name: research-specialist
  - domain: research
  - capabilities: Information synthesis, best practices research, technical investigation
Created: research-specialist agent
Retry: Delegate to new research-specialist
```

**Example 3: Product Management**
```
User: "Create product roadmap for Q1 2026"
Main LLM Classification: COORDINATION | Product Management
Domain Identification: product-management
Agent Matching: NO MATCH (project-manager is execution, not strategy)
Gap Detection: Product management distinct from project management
Action: Invoke agent-creator
Specification:
  - name: product-manager-strategist
  - domain: product-management
  - capabilities: Roadmapping, feature prioritization, stakeholder management
Created: product-manager-strategist agent
Retry: Delegate to new product-manager-strategist
```

### Agent Template Requirements
All auto-created agents must follow standard template:

**Required Sections**:
1. **Agent Overview** (name, description, color in frontmatter)
2. **Core Identity** (Purpose statement, primary responsibilities)
3. **Operating Instructions** (How agent analyzes and responds)
4. **Context Awareness** (What agent should consider)
5. **Input/Output Examples** (Concrete usage examples)
6. **Tools and Integrations** (Which tools agent uses)
7. **Safety and Boundaries** (What agent should NOT do)
8. **Metrics for Evaluation** (Success criteria)
9. **Coordination Patterns** (Integration with other agents)

**Template Location**: See existing agents for format

### Review and Approval Commands
```bash
# List pending agents
oak-list-pending-agents

# Review specific agent
oak-review-agent <agent-name>

# Approve agent (deploys immediately)
oak-approve-agent <agent-name>

# Modify agent (opens in editor)
oak-modify-agent <agent-name>

# Reject agent (archives with reasoning)
oak-reject-agent <agent-name> "<reason>"

# Check for pending reviews
oak-check-pending
```

### Fallback Behavior (Before Agent Created)
If agent cannot be created immediately:
1. **Route to general-purpose** with explicit note: "No specialized agent available for [domain]. Using general-purpose. Consider creating dedicated agent."
2. **Log routing failure** for agent-auditor monthly review
3. **Inform user** that capability is missing and will be addressed

### Integration with agent-auditor
**Monthly Review**:
- agent-auditor analyzes all routing failures
- Identifies patterns suggesting missing agents
- Proposes batch creation of needed agents
- Human reviews and approves
- agent-creator creates approved agents

**Prevents Over-Creation**:
- Don't create agent for one-off requests
- Don't create if existing agent can be expanded
- Don't create if overlap with existing is >50%

### Gap Detection State Tracking
**Location**: `telemetry/routing_failures.jsonl`

**Format**:
```json
{
  "timestamp": "2025-10-16T10:30:00Z",
  "user_request": "Analyze financial statements",
  "classification": "ANALYSIS",
  "domain": "financial-analysis",
  "matched_agent": null,
  "fallback_used": "general-purpose",
  "gap_score": 0.95,
  "recommendation": "create financial-analyst"
}
```

### Success Metrics
- **Routing Accuracy**: % of requests successfully matched to agents
- **Gap Closure Rate**: % of identified gaps closed within 30 days
- **Creation Precision**: % of created agents that get used regularly
- **User Satisfaction**: Feedback on agent coverage
</Rule>

<Rule id="spec-driven-development">
**SPEC-DRIVEN DEVELOPMENT WORKFLOW**: User co-authors specifications for significant changes

### When to Use Spec-Driven Workflow

**CREATE SPEC for (spec-manager delegation):**
- **Significant features**: New features or subsystems
- **Architectural changes**: Design decisions affecting multiple components
- **Multi-agent coordination**: Requires 5+ files or 3+ agents
- **Complex changes**: Significant refactoring or system modifications
- **User explicitly requests**: "Let's create a spec" or "spec-driven approach"
- **Security-critical**: Authentication, authorization, data protection
- **Data migrations**: Schema changes or data transformations

**USE TodoWrite for (standard workflow):**
- **Simple bug fixes**: 1-2 files, single agent
- **Typos/documentation**: Quick edits
- **Single-file changes**: Isolated modifications
- **User prefers quick iteration**: Explicit request for fast implementation

### Spec-Driven Workflow Process

**Main LLM Decision**:
```
Request Analysis
    ↓
Complexity Evaluation
    ↓
    ├─ Simple/Quick → TodoWrite (standard workflow)
    │
    └─ Significant → spec-manager Delegation:
        1. "This looks like a significant change [because...]"
        2. "I recommend spec-driven workflow (10-15 min upfront, clearer design)"
        3. "Sound good?"
        4. User confirms → Delegate to spec-manager
```

**spec-manager Workflow**:
1. **Collaborative Spec Creation** (Markdown):
   - Section 1: Goals & Requirements (with user approval)
   - Section 2: Technical Design (with user approval)
   - Section 3: Implementation Plan (with user approval)
   - Section 4: Test Strategy (with user approval)
   - Save to `specs/active/YYYY-MM-DD-feature-name.md`

2. **YAML Translation**:
   - Auto-generate from Markdown
   - Save to `specs/active/YYYY-MM-DD-feature-name.yaml`

3. **Task Decomposition**:
   - Break spec into tasks
   - Assign agents based on domain + historical performance
   - Create execution plan (sequential/parallel)

4. **Execution Coordination**:
   - Invoke agents with spec context
   - Log execution in spec (Section 5: Execution Log)
   - Link telemetry: `spec_id` + `spec_section`

5. **Change Management**:
   - Handle changes in "spec terms" not "code terms"
   - Example: "Spec section 2.3 (Auth Strategy) needs update. Current: JWT. Proposed: OAuth2. Affects sections [2.3, 3.1.task-2]. Approve?"
   - Update Markdown → Regenerate YAML → Continue

6. **Validation & Completion**:
   - Verify all acceptance criteria met
   - All tests pass
   - Update Section 7: Completion Summary
   - Move to `specs/completed/`

### Spec File Structure

**Markdown** (`specs/active/YYYY-MM-DD-feature-name.md`):
- Human-readable, collaborative editing
- Source of truth for user
- Sections: Goals, Design, Implementation, Tests, Execution, Changes, Completion

**YAML** (`specs/active/YYYY-MM-DD-feature-name.yaml`):
- Machine-readable, auto-generated
- Agent consumption format
- Structured data: tasks, agents, dependencies, linkages

### Telemetry Integration

**Agent invocations include**:
```python
spec_id = "spec-20251023-feature-name"
spec_section = ["2.2.comp-1", "3.1.task-1"]  # Which spec sections

logger.log_invocation(
    agent_name="backend-architect",
    spec_id=spec_id,
    spec_section=spec_section,
    ...
)
```

**Benefits**:
- Trace agent invocations back to specs
- Analyze which spec sections cause issues
- Measure spec adherence quality
- Track spec accuracy (% of specs needing changes during implementation)

### User Communication

**Spec Terms vs Code Terms**:
- ✅ "Spec section 2.3 (Component X) needs update..."
- ✅ "This affects acceptance criteria AC-1 and AC-2..."
- ✅ "Want to review spec or proceed with implementation?"
- ❌ "Should I change line 45 to use X instead of Y?"
- ❌ "I modified these 8 files, want to see them?"

**User Decisions**:
- Approve spec approach (vs TodoWrite)
- Approve spec sections (Goals, Design, Plan, Tests)
- Approve spec changes during implementation
- Approve completion (all criteria met)

**Optional Code Review**:
- User can always request: "Show me the code for X"
- Default: Trust spec adherence, skip code review
- Offer: "Implementation meets spec. View code or mark complete?"

### Integration with Existing Workflow

**Hybrid Model**:
- **Simple tasks**: TodoWrite (existing workflow)
- **Significant tasks**: spec-manager → spec-driven workflow
- **Both supported**: User can request either approach

**Workflow Selection**:
```
Main LLM Classification
    ↓
IMPLEMENTATION (Significant)
    ↓
    ├─ Quick fix requested? → TodoWrite
    │
    └─ Recommend spec-driven:
        "This is a significant change. Spec-driven approach recommended.
        Takes 10-15 min upfront but ensures alignment on design.
        Use spec workflow or quick TodoWrite?"
            ↓
        User Decision → spec-manager OR TodoWrite
```

### Quality Metrics

Track spec-driven workflow effectiveness:
- **Spec Accuracy**: % of specs needing changes during implementation (target: <20%)
- **User Satisfaction**: Did spec process help or hinder?
- **Implementation Fidelity**: How well code matched spec
- **Time Investment**: Spec creation vs rework prevented

### Example: Spec-Driven vs TodoWrite

**TodoWrite Example (Simple)**:
```
User: "Fix typo in README line 5"
Main LLM: "Simple fix, using TodoWrite"
    → Creates todo
    → domain-specialist fixes
    → git-workflow-manager commits
```

**Spec-Driven Example (Significant)**:
```
User: "Add OAuth2 authentication"
Main LLM: "Significant feature. Recommend spec-driven approach (15 min upfront planning). Sound good?"
User: "Yes"
Main LLM: Delegates to spec-manager
    → spec-manager co-authors spec (Goals, Design, Plan, Tests)
    → User approves spec
    → spec-manager generates YAML
    → spec-manager decomposes tasks:
        - Task 1: backend-architect (OAuth2 endpoints)
        - Task 2: security-auditor (security review)
        - Task 3: frontend-developer (login UI)
    → spec-manager coordinates execution
    → Agents log to spec execution log
    → spec-manager validates completion
    → "All 5 acceptance criteria met. Spec complete."
```
</Rule>

<Rule id="classification-routing">
**CLASSIFICATION-BASED ROUTING**: Domain identification through classification

### Classification-Domain Mapping
- **IMPLEMENTATION + Frontend context** → frontend-developer
- **IMPLEMENTATION + Backend context** → backend-architect
- **IMPLEMENTATION + Infrastructure context** → infrastructure-specialist
- **ANALYSIS + Security context** → security-auditor
- **ANALYSIS + Business context** → business-analyst

### Context Detection Hierarchy
1. **File-Path Context**: File extensions and directories indicate domain
2. **Technology Keywords**: Framework/language mentions indicate domain
3. **Functional Keywords**: What the request aims to accomplish
4. **Error Context**: Error messages indicate appropriate domain specialist

### Multi-Domain Classification
- **IMPLEMENTATION + Multiple domains** → Parallel/Sequential multi-agent workflow
- **ANALYSIS + Multiple domains** → Parallel analysis with Main LLM synthesis
- **COORDINATION + Any domains** → Multi-agent workflow management

### Emergency Override
- **debug-specialist**: ALWAYS highest priority regardless of classification
- **Blocks all other classification** until critical issues resolved

### Default Workflows
- **IMPLEMENTATION**: specialist → quality-gate (unified validation) → git-workflow-manager
- **IMPLEMENTATION** (complex): design-simplicity-advisor → specialist → quality-gate → git-workflow-manager
- **ANALYSIS**: analyst(s) → Main LLM synthesis
- **COORDINATION**: workflow management with appropriate specialists
- **INFORMATION**: Direct handling (simple) or analyst delegation (complex)
</Rule>

<Rule id="simplified-workflow-enforcement">
**SIMPLIFIED WORKFLOW ENFORCEMENT**: KISS-based 3-step workflow replacing complex agent chains

### Primary Workflow (RECOMMENDED)
**3-Step Simplified Workflow**: Implementation → quality-gate → git-workflow-manager

1. **Implementation Phase**: Domain specialist executes the work
2. **Quality Gate Phase**: quality-gate performs unified validation (code review + maintainability + complexity analysis)
3. **Git Operations Phase**: git-workflow-manager creates commit + PR

### Quality Gate Integration
**quality-gate** combines multiple checks into single coordinated review:
- Code review and standards validation
- Maintainability and clarity analysis (replaces code-clarity-manager)
- Top-down architectural impact assessment (replaces top-down-analyzer)
- Bottom-up implementation complexity validation (replaces bottom-up-analyzer)
- Simplicity and KISS compliance check
- Security and performance basic validation

**75% workflow reduction**: 4 sequential agents consolidated into 1 unified validation step

### Technical Enforcement
**Workflow State Tracking**:
- `.workflow_state` file tracks current phase and validation status
- Hash validation ensures code hasn't changed between phases
- Git hooks provide bulletproof enforcement of workflow completion

**Enforcement Mechanisms**:
```bash
# Pre-commit hook validates workflow completion
if [ ! -f ".workflow_state" ] || ! grep -q "QUALITY_GATE_PASSED" .workflow_state; then
  echo "❌ Workflow not completed. Run quality gate validation."
  exit 1
fi
```

### Failure Recovery
**State Recovery Procedures**:
- Incomplete workflow: Resume from last completed phase
- Failed quality gate: Address issues and re-run validation
- State corruption: Reset workflow and restart from implementation

### Backward Compatibility
**Complex Agent Chain** (optional for teams requiring granular control):
- Legacy 7-agent workflow remains available via explicit flag
- Use `COMPLEX_WORKFLOW=true` environment variable to enable
- Default behavior uses simplified 3-step workflow
</Rule>

<Rule id="multi-agent-coordination">
**MULTI-AGENT COORDINATION**: Workflow patterns for overlapping domains

### Coordination Types
1. **Simplified Quality Gates** (RECOMMENDED): Implementation → quality-gate (unified) → git-workflow-manager
2. **Legacy Sequential Gates** (deprecated): Implementation → code-reviewer → code-clarity-manager → unit-test-expert → design-simplicity-advisor (pre-commit) → git-workflow-manager
3. **Parallel Analysis**: [security-auditor + dependency-scanner] → Main LLM synthesis
4. **Collaborative Architecture**: systems-architect → [backend-architect + infrastructure-specialist] → Main LLM integration
5. **Domain Collaboration**: [specialist-1 + specialist-2] → Main LLM reconciliation

### Coordination Patterns
- **Security**: security-auditor + quality-gate + dependency-scanner → comprehensive report
- **Architecture**: systems-architect → backend-architect + infrastructure-specialist → consistency
- **Testing**: unit-test-expert + qa-specialist → comprehensive approach
- **Documentation**: technical-writer + business-analyst → complete docs

### When to Use Multi-Agent
- **Compound triggers**: Multiple domain keywords
- **Cross-domain issues**: Spans multiple specializations
- **Comprehensive tasks**: "Full system X" or "Complete Y"
- **Quality requirements**: "Secure and performant"

### Main LLM Responsibilities
- **Detect**: Multiple agents needed
- **Invoke**: Parallel/sequential launch
- **Synthesize**: Combine outputs
- **Resolve**: Handle conflicts (domain priority, security first, architecture consistency)
</Rule>

<Rule id="coordination-workflow">
**COORDINATION WORKFLOW**: Main LLM direct management
- **DETECT**: Compound triggers → multi-agent, single domain → specialist, file ops → file-path routing
- **INVOKE**: Task() calls (single/multiple based on analysis)
- **COORDINATE**: Sequential quality gates, parallel analysis, collaborative workflows
- **SYNTHESIZE**: Combine outputs into coherent recommendations
- **RESOLVE**: Conflicts using domain priority (security > performance > convenience)
- **SIMPLE TASKS**: File reads, searches, questions, communication → handle directly
- **NO ORCHESTRATOR**: Main LLM handles coordination directly
</Rule>

<Rule id="overlap-resolution">
**OVERLAP RESOLUTION**: Common coordination scenarios

### Priority Rules
1. **debug-specialist**: ALWAYS highest priority, blocks all others
2. **design-simplicity-advisor**: MANDATORY before ANY implementation
3. **Security-first**: Override performance/convenience
4. **Architecture-consistency**: High-level guides implementation
5. **Quality-gates**: Code reviewer decisions non-negotiable
6. **Domain-expertise**: More specific takes precedence

### Example Patterns
- **"Fix failing tests"**: debug-specialist + qa-specialist
- **"Implement secure auth"**: design-simplicity-advisor → security-auditor + backend-architect
- **"Debug deployment"**: debug-specialist + infrastructure-specialist
- **"Create API docs"**: technical-writer
- **"Optimize database"**: backend-architect + infrastructure-specialist
</Rule>

<Rule id="mandatory-simplicity-workflow">
**MANDATORY SIMPLICITY WORKFLOW**: Simplified enforcement with technical backing

### Simplified Workflow (DEFAULT)
`Task Detection → Implementation Agent → quality-gate (unified validation) → git-workflow-manager`

**quality-gate includes**:
- Simplicity analysis (KISS compliance)
- Code review and standards
- Maintainability and clarity
- Architectural impact assessment
- Implementation complexity analysis
- Basic security and performance checks

### Legacy Complex Workflow (OPTIONAL - Deprecated)
`Task Detection → design-simplicity-advisor (pre-implementation) → Implementation Agent → code-reviewer → code-clarity-manager → top-down-analyzer → bottom-up-analyzer → design-simplicity-advisor (pre-commit) → git-workflow-manager`

**Status**: Deprecated - These agents have been consolidated into quality-gate
**Enable with**: `COMPLEX_WORKFLOW=true` (requires archived agents to be reactivated)

### Implementation Blocking
- **NO IMPLEMENTATION** until quality gate design analysis completes
- **NO BYPASS** - Main LLM must invoke for ANY implementation task
- **TRIGGERS**: implement, create, build, develop, code, design, etc.
- **EXCEPTION**: debug-specialist only (critical errors)

### Technical Enforcement
**Workflow State File** (`.workflow_state`):
```
PHASE=IMPLEMENTATION|QUALITY_GATE|GIT_OPERATIONS
STATUS=IN_PROGRESS|COMPLETED|FAILED
HASH=<code_hash_for_validation>
TIMESTAMP=<iso_timestamp>
```

**Git Hook Integration**:
- Pre-commit: Validates workflow completion
- Post-commit: Cleans up workflow state
- Pre-push: Ensures quality gate passed

### Enforcement Principles
- **Simple-first principle**: Start with simplest viable solution
- **Complexity justification**: Complex solutions need explicit justification
- **Deferred optimization**: Performance only when proven necessary
- **Minimal dependencies**: Prefer built-in over external libraries

### Workflow Integration
- **Simplified**: implementation → quality-gate (unified validation) → git-workflow-manager
- **Complex** (deprecated): design-simplicity-advisor → security-auditor → implementation → sequential gates (requires archived agents)
- **Emergency**: debug-specialist (bypass with post-commit review requirement)
</Rule>

<Rule id="quality-gate-enforcement">
**QUALITY GATE ENFORCEMENT**: Unified simplicity and quality validation

### Simplified Quality Gate (DEFAULT)
**Combined Validation Process**:
- Code review and standards compliance
- Unit test creation and execution
- KISS principle validation
- Basic security and performance checks
- Documentation completeness

**Single Quality Gate Agent** handles all validations with coordinated output.

### Legacy Sequential Gates (OPTIONAL)
**Traditional Sequence**: unit-test-expert → design-simplicity-advisor (pre-commit) → git-workflow-manager

**Enable with**: `COMPLEX_WORKFLOW=true`

### Technical Enforcement
**Workflow State Validation**:
```bash
# Pre-commit hook example
if ! quality_gate_validator.sh --validate-all; then
  echo "❌ Quality gate failed. Address issues before commit."
  exit 1
fi
```

**Quality Gate Requirements**:
- **HOLISTIC**: Analyze entire changeset for unnecessary complexity
- **KISS VALIDATION**: Ensure Keep It Simple, Stupid principle compliance
- **ABSTRACTION**: Flag over-abstraction or premature optimization
- **OPPORTUNITIES**: Recommend simplifications before commit
- **DEBT ASSESSMENT**: Flag complexity creating maintenance burden
- **TEST COVERAGE**: Ensure adequate unit test coverage
- **SECURITY BASICS**: Check for common security issues

### Integration Options
**Simplified Path** (DEFAULT):
- **NO GIT OPS** until quality-gate complete
- **FINAL GATE**: quality-gate is mandatory before git-workflow-manager
- **MANDATORY**: git-workflow-manager MUST be invoked after quality-gate passes
- **EMERGENCY**: debug-specialist can bypass (critical production only), MUST schedule post-commit review

**Complex Path** (when `COMPLEX_WORKFLOW=true` - deprecated):
- **SEQUENCE**: unit-test-expert → design-simplicity-advisor → git-workflow-manager
- **GRANULAR CONTROL**: Each agent provides specific validation
- **DETAILED FEEDBACK**: Separate reports from each quality agent

### State Recovery
**Failed Quality Gate**:
1. Review failure report
2. Address identified issues
3. Re-run quality-gate validation
4. Proceed to git-workflow-manager on success
</Rule>

<Rule id="git-workflow-mandatory">
**GIT WORKFLOW MANDATORY**: Automatic invocation after quality gates

### Workflow Completion Requirement
- **MANDATORY**: git-workflow-manager MUST be invoked after quality-gate passes
- **NO BYPASS**: Manual git operations not allowed (use git-workflow-manager)
- **BLOCKING**: Workflow incomplete until git commit created

### Invocation Trigger
```
quality-gate status = PASS
  ↓
AUTOMATIC: Invoke git-workflow-manager
  - Create commit with descriptive message
  - Include Claude Code attribution
  - Update changelog (if applicable)
  - Create PR (if requested)
```

### Workflow Sequence
```yaml
implementation_complete:
  step_1: "quality-gate validates changes"
  step_2_on_pass: "git-workflow-manager creates commit"
  step_3: "Workflow marked complete"

  step_2_on_fail: "Return to implementation with feedback"

  blocking_behavior: "Main LLM MUST invoke git-workflow-manager on pass"
```

### Exception Handling
**Emergency bypass** (debug-specialist only):
- Critical production fix requiring immediate manual git operations
- MUST schedule post-commit review with git-workflow-manager
- Log bypass reason in telemetry

**User explicitly requests manual git**:
- Warn user about workflow incompleteness
- Recommend using git-workflow-manager instead
- If user insists: Allow but log as manual override

### Root Cause Analysis
**Problem**: git-workflow-manager has 0 invocations despite being mandatory

**Causes Identified**:
- Workflow rules don't explicitly enforce git-workflow-manager invocation
- Main LLM coordination doesn't include git operations in standard workflow
- Focus on pre-implementation (simplicity) but not post-implementation (git)

**Solution**: Explicit rule enforcement with automatic invocation requirement
</Rule>
</AgentDelegationRules>

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

<ThinkingProcess>
<Rule id="thinking">
**THINKING PROCESS**:
- Complex tasks: Use <thinking></thinking> tags
- Always acknowledge CLAUDE.md rules
- **Classification phrases**: "Classifying request as [TYPE]", "Domain identification: [DOMAIN]", "Agent plan: [WORKFLOW]", "Executing classification-based workflow"
- **Main LLM workflow**: CLASSIFY → IDENTIFY DOMAINS → CREATE PLAN → EXECUTE PLAN → FORMAT RESPONSE
</Rule>
</ThinkingProcess>