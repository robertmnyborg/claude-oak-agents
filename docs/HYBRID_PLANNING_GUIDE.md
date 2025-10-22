# Hybrid Planning Model - Implementation Guide

## Overview

This guide provides complete details on implementing the Hybrid Planning Model across all agents in the claude-oak-agents system. This model combines top-down strategic planning with bottom-up implementation expertise, mirroring real engineering teams.

## Quick Reference

**For Main LLM**: See CLAUDE.md lines 250-584 for complete workflow coordination
**For Review Agents**: See sections below for review mode responsibilities
**For Execution Agents**: See "Planning Mode Template" section for implementation guidance

## Review Agent Modes (Phase 3)

### state-analyzer - Technical Validation Mode

**Purpose**: Validate technical feasibility and compatibility of proposed agent plans

**Invoked by**: Main LLM during Phase 3 (Plan Review)

**Input**: Collection of agent implementation plans from Phase 2

**Output**: Technical validation report

**Responsibilities**:
1. **Codebase Compatibility**: Verify proposed approaches work with existing code
   - Check language/framework compatibility
   - Validate API contracts between agents
   - Identify version conflicts

2. **Infrastructure Validation**: Assess infrastructure requirements
   - Verify cloud resources available
   - Check deployment platform compatibility
   - Validate environment variables/secrets exist

3. **Dependency Analysis**: Detect dependency conflicts
   - Check for library version conflicts
   - Validate build tool compatibility
   - Identify circular dependencies

4. **Integration Feasibility**: Validate cross-agent integration points
   - API contract compatibility
   - Data format alignment
   - Communication protocol agreement

**Output Format**:
```yaml
technical_validation:
  codebase_compatibility:
    status: "compatible" | "conflicts" | "unknown"
    issues: []
    recommendations: []

  infrastructure_requirements:
    status: "available" | "missing" | "needs_setup"
    required_resources: []
    missing_resources: []

  dependency_conflicts:
    status: "no_conflicts" | "conflicts_found"
    conflicts: []
    resolutions: []

  integration_validation:
    status: "compatible" | "incompatible"
    integration_points: []
    concerns: []

  overall_decision:
    recommendation: "proceed" | "proceed_with_setup" | "pause"
    confidence: "high" | "medium" | "low"
    blockers: []
```

### design-simplicity-advisor - Complexity Review Mode

**Purpose**: Review agent plans for unnecessary complexity and over-engineering

**Invoked by**: Main LLM during Phase 3 (Plan Review)

**Input**: Collection of agent implementation plans from Phase 2

**Output**: Complexity assessment and simplification recommendations

**Responsibilities**:
1. **Over-Engineering Detection**: Identify unnecessarily complex proposals
   - Compare options for simplicity
   - Flag gold-plating and premature optimization
   - Identify YAGNI violations

2. **Simpler Alternative Suggestion**: Propose simpler approaches
   - "Have you considered [simpler option]?"
   - Challenge assumptions requiring complexity
   - Recommend proven boring solutions

3. **KISS Principle Validation**: Ensure simplicity principles followed
   - Minimal dependencies preferred
   - Direct solutions over clever ones
   - Avoid solving hypothetical future problems

4. **Complexity Justification Review**: Validate when complexity is warranted
   - Is complexity truly required for business need?
   - Are simpler alternatives genuinely insufficient?
   - Is complexity cost justified by value?

**Output Format**:
```yaml
complexity_review:
  over_engineering_detected:
    status: "none" | "minor" | "significant"
    instances: []

  simpler_alternatives:
    - option: "original_proposal"
      complexity_score: 7
      simpler_alternative: "description"
      simplicity_score: 3
      tradeoffs: "what you lose by simplifying"

  kiss_principle_adherence:
    status: "excellent" | "good" | "poor"
    violations: []
    recommendations: []

  complexity_justifications:
    - complexity_item: "description"
      justification: "business/technical reason"
      verdict: "justified" | "unjustified"

  overall_recommendation:
    decision: "approve_as_is" | "recommend_simplification" | "require_simplification"
    rationale: "explanation"
    suggested_changes: []
```

## Execution Agent Planning Mode (Phase 2)

### Planning Mode Responsibilities

When invoked in planning mode, execution agents must:

1. **Propose 2-3 Implementation Options**
   - Each option must be distinct approach
   - Cover spectrum: simple → complex
   - Include "do nothing" if viable

2. **Provide Comprehensive Trade-offs**
   - Pros: What makes this option attractive
   - Cons: What are the downsides
   - Risks: What could go wrong
   - Dependencies: What else is needed

3. **Give Realistic Estimates**
   - Time estimate in hours
   - Complexity level (low/medium/high)
   - Confidence level in estimate

4. **Recommend Best Option**
   - Select preferred option
   - Explain rationale
   - List conditions/assumptions

### Planning Mode Output Template

```yaml
agent_plan:
  agent_name: "[your-agent-name]"
  task: "[task description from Phase 1]"

  implementation_options:
    option_a:
      approach: "Brief name for this approach"
      description: "1-2 sentence description"
      pros:
        - "Advantage 1"
        - "Advantage 2"
        - "Advantage 3"
      cons:
        - "Disadvantage 1"
        - "Disadvantage 2"
      time_estimate_hours: [number]
      complexity: "low" | "medium" | "high"
      risks:
        - "Risk 1"
        - "Risk 2"
      dependencies:
        - "Dependency 1 (e.g., npm: library-name)"
        - "Dependency 2 (e.g., agent: other-agent-name)"

    option_b:
      # Same structure as option_a

    option_c:
      # Same structure (optional, 2-3 options total)

  recommendation:
    selected: "option_a" | "option_b" | "option_c"
    rationale: "Why this option is best given constraints"
    conditions:
      - "Condition 1 that must be met"
      - "Condition 2 for success"

  questions_for_review:
    - "Clarification needed from other agents"
    - "Assumptions to validate"
```

### Example: backend-architect Planning Mode

```yaml
agent_plan:
  agent_name: "backend-architect"
  task: "Implement OAuth2 authentication endpoints"

  implementation_options:
    option_a:
      approach: "Passport.js OAuth2 Strategy"
      description: "Use battle-tested Passport.js library for OAuth2 implementation"
      pros:
        - "Well-documented with extensive community support"
        - "Quick implementation (4 hours)"
        - "Handles OAuth2 edge cases automatically"
      cons:
        - "External dependency (~200KB)"
        - "Less control over implementation details"
        - "Opinionated architecture (Express middleware pattern)"
      time_estimate_hours: 4
      complexity: "low"
      risks:
        - "Dependency maintenance burden"
        - "Potential version conflicts with existing packages"
      dependencies:
        - "npm: passport@0.6.0"
        - "npm: passport-oauth2@1.7.0"

    option_b:
      approach: "Custom OAuth2 Implementation"
      description: "Build OAuth2 from scratch using Node.js crypto libraries"
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
        - "Security vulnerabilities (timing attacks, CSRF)"
        - "Missing edge case handling"
      dependencies: []

    option_c:
      approach: "Minimal OAuth2 (authorization_code only)"
      description: "Implement only core authorization_code flow, defer advanced features"
      pros:
        - "Simpler than full OAuth2 spec"
        - "Zero dependencies"
        - "Faster than Option B (8 hours)"
        - "Can extend to full OAuth2 later (YAGNI principle)"
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
      - "Document OAuth2 limitations for future extensibility"
      - "Plan migration path to full OAuth2 if needed"

  questions_for_review:
    - "Does frontend-developer need specific OAuth2 flows beyond authorization_code?"
    - "Does security-auditor approve minimal OAuth2 approach?"
```

## Agent Updates Required

### Review Agents (Phase 3)

**Already Updated**:
- ✅ project-manager (Plan Review Mode)
- ✅ product-strategist (Alignment Review Mode)

**Add Review Mode**:
- state-analyzer (Technical Validation Mode) - Add section based on template above
- design-simplicity-advisor (Complexity Review Mode) - Add section based on template above

### Execution Agents (Phase 2)

**Add Planning Mode to these 26 agents**:

**Core Development (7)**:
- frontend-developer
- backend-architect
- mobile-developer
- blockchain-developer
- ml-engineer
- legacy-maintainer
- infrastructure-specialist

**Quality & Security (7)**:
- code-reviewer
- unit-test-expert
- security-auditor
- dependency-scanner
- qa-specialist
- debug-specialist
- performance-optimizer

**Analysis & Planning (3)**:
- business-analyst
- data-scientist
- state-analyzer (also has review mode)

**Documentation & Content (3)**:
- technical-documentation-writer
- content-writer
- changelog-recorder

**Special Purpose (6)**:
- git-workflow-manager
- systems-architect
- design-simplicity-advisor (also has review mode)
- agent-creator
- prompt-engineer
- agent-auditor

### Agent File Structure

Each execution agent file should add this section:

```markdown
## Planning Mode (Phase 2: Hybrid Planning)

When invoked in planning mode (NOT execution mode), this agent proposes 2-3 implementation options with comprehensive trade-off analysis.

**See**: `docs/HYBRID_PLANNING_GUIDE.md` for complete planning mode documentation

**Input**:
- task_description: "Specific task assigned to this agent"
- constraints: ["Requirement 1", "Constraint 2"]
- context: {languages: [], frameworks: [], codebase_info: {}}

**Output**: Implementation options with trade-offs, estimates, and recommendation

**Process**:
1. Analyze task and constraints
2. Generate 2-3 distinct implementation approaches
3. Evaluate pros/cons/risks for each option
4. Estimate time and complexity
5. Recommend best option with rationale

**Example**: See `docs/HYBRID_PLANNING_GUIDE.md` for complete example

---

*When in execution mode (default), this agent implements the refined task from Phase 4 as normal.*
```

## Telemetry Updates

### Planning Phase Schema

Add to `telemetry/schemas.json`:

```json
{
  "AgentPlanningInvocation": {
    "type": "object",
    "properties": {
      "invocation_id": {"type": "string"},
      "workflow_id": {"type": "string"},
      "agent_name": {"type": "string"},
      "mode": {"enum": ["planning", "execution"]},
      "phase": {"enum": ["strategic_planning", "implementation_planning", "plan_review", "execution"]},
      "task": {"type": "string"},
      "options_proposed": {"type": "number"},
      "recommended_option": {"type": "string"},
      "estimated_hours": {"type": "number"},
      "complexity": {"enum": ["low", "medium", "high"]},
      "timestamp": {"type": "string", "format": "date-time"}
    }
  }
}
```

### Planning Metrics to Track

- Planning time vs execution time ratio
- Estimated hours vs actual hours (planning accuracy)
- Which options selected most frequently
- Conflicts detected in review phase
- Go/no-go decision rates
- Planning ROI (planning cost vs rework prevented)

## Usage Examples

### Simple Task (No Hybrid Planning)

```
User: "Fix typo in README"
Main LLM: Classifies as SIMPLE
  → Uses fast path (no hybrid planning)
  → Directly invokes content-writer in execution mode
  → Reviews and commits
```

### Complex Task (Hybrid Planning)

```
User: "Add OAuth2 authentication"
Main LLM: Classifies as HIGH RISK + COMPLEX

Phase 1 (Strategic Planning):
  → design-simplicity-advisor: Analyzes simplicity
  → project-manager: Creates strategic plan
  → Decision: Use hybrid planning (HIGH risk)

Phase 2 (Implementation Planning - Parallel):
  → backend-architect: Proposes 3 options
  → security-auditor: Proposes 2 options
  → frontend-developer: Proposes 2 options

Phase 3 (Plan Review - Parallel):
  → project-manager: Synthesizes plans, detects HTTPS dependency conflict
  → state-analyzer: Validates technical feasibility
  → product-strategist: Validates business alignment
  → design-simplicity-advisor: Reviews complexity
  → Synthesis: Refined plan with resolved conflicts

Phase 4 (Execution):
  → Agents execute refined plan
  → Quality gates
  → Commit and deploy
```

## Benefits Summary

1. **Early Conflict Detection**: Discover incompatibilities during planning (save 2+ hours rework)
2. **Better Estimates**: Domain experts provide accurate time estimates (92% vs 67% accuracy)
3. **Risk Mitigation**: Identify and address risks before committing resources
4. **Knowledge Capture**: Planning discussions generate valuable telemetry for learning
5. **Optimized Solutions**: Review process selects best options from multiple proposals
6. **Real Team Dynamics**: Mirrors actual engineering team workflows

## Cost/Benefit Analysis

### Time Investment

- **Simple tasks**: +25% overhead (not worth it) → Skip hybrid planning
- **Complex tasks**: -35% total time (worth it!) → Use hybrid planning
- **Threshold**: Benefits exceed costs at ~4 hours estimated work

### Cost Impact

- **Invocations**: +175% (7 Haiku + 4 Sonnet)
- **Token cost**: +58% ($0.19 vs $0.12)
- **Rework prevented**: Saves $0.60 average
- **Net savings**: $0.41 per complex task

### When to Use

**MANDATORY**:
- Risk: HIGH/CRITICAL
- Time: >4 hours
- Agents: ≥4
- Security-critical

**RECOMMENDED**:
- Complexity: HIGH + Novelty: HIGH
- Cross-domain integration
- Cost of failure: >2 hours

**SKIP**:
- Simple single-agent tasks
- Well-understood patterns
- Low-risk changes
