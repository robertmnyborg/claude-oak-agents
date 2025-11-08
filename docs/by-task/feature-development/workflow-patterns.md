# Workflow Patterns Library

A comprehensive guide to proven workflow patterns for Claude agents. Each pattern is designed to solve specific types of problems and optimize for different success criteria.

## Overview

Workflow patterns are reusable, tested combinations of agent interactions and sequences that produce predictable, high-quality results. This library provides the blueprints you need to structure agent work effectively.

### Why Workflow Patterns Matter

- **Consistency**: Reduces variability in agent output quality
- **Efficiency**: Eliminates guesswork about optimal agent sequences
- **Predictability**: Enables accurate timeline estimation
- **Scalability**: Patterns can be composed for complex tasks
- **Learning**: Establishes best practices across your organization

---

## Pattern Index

| Pattern | Best For | Complexity | Timeline | Agents Involved |
|---------|----------|-----------|----------|-----------------|
| [AB Method](#ab-method) | Critical decisions, risky changes | Low | 15-30 min | 2 |
| [RIPER Workflow](#riper-workflow) | Complex analysis, thorough evaluation | Medium | 30-60 min | 3-4 |
| [Quick Iteration Pattern](#quick-iteration-pattern) | Rapid prototyping, feedback loops | Medium | 20-45 min | 2-3 |
| Serial Processing | Sequential task handling | Low | Variable | 1-2 |
| Parallel Synthesis | Multi-perspective analysis | High | 30-90 min | 4-5 |
| Hierarchical Review | Large-scale content | High | 45-120 min | 3-5 |
| Feedback Loop Cascade | Iterative refinement | Medium | 20-40 min | 2-3 |
| Expert Panel | Complex decision-making | High | 40-80 min | 4-6 |

---

## Detailed Patterns

### AB Method

**Overview**: A decision-making pattern that evaluates two approaches in parallel, then synthesizes findings for final recommendation.

#### When to Use

- Comparing implementation approaches
- Evaluating conflicting recommendations
- Making go/no-go decisions with risk
- Resolving technical disputes
- Choosing between architectural patterns
- High-stakes decisions requiring objectivity

#### Agent Sequence

1. **Agent A**: Advocates for Approach 1
   - Builds the strongest case for position
   - Identifies benefits and realistic advantages
   - Acknowledges legitimate concerns

2. **Agent B**: Advocates for Approach 2
   - Builds the strongest case for alternative
   - Highlights different benefits and perspectives
   - Addresses Agent A's points

3. **Synthesizer Agent**: Makes final recommendation
   - Reviews both arguments objectively
   - Identifies valid points from each side
   - Provides weighted recommendation with reasoning

#### Example Workflow

**Scenario**: Deciding between microservices vs monolithic architecture for a new platform.

```
Input: "We need to decide between microservices and monolithic architecture.
Requirements: High scalability, 3-month delivery, 5-person team."

Agent A Output:
"Microservices approach is optimal because:
- Independent scaling for high-demand services
- Team can work in parallel on different services
- Technology flexibility
- Concerns: Increased complexity, distributed debugging challenges"

Agent B Output:
"Monolithic approach is optimal because:
- Simpler deployment and operations
- Faster initial development
- Easier debugging and transaction management
- Concerns: Scaling limitations, team coupling"

Synthesizer Output:
"RECOMMENDATION: Monolithic with modular architecture
REASONING:
- 3-month timeline favors simpler deployment
- 5-person team lacks DevOps infrastructure for microservices
- Start monolithic, design for future service extraction
- Risk reduction outweighs flexibility benefits at this stage"
```

#### Timeline Estimate

- **Planning**: 2-3 minutes
- **Agent A Analysis**: 5-8 minutes
- **Agent B Analysis**: 5-8 minutes
- **Synthesis**: 3-5 minutes
- **Total**: 15-30 minutes

#### Key Metrics for Success

- Decision clarity improved (clear winner or tiebreaker identified)
- Risk factors explicitly surfaced
- Implementation approach defined

---

### RIPER Workflow

**Overview**: A comprehensive evaluation pattern that moves through Research, Identify, Plan, Execute, Review phases for complex problems.

#### When to Use

- Large feature implementations
- Architecture redesigns
- Complex bug investigations
- Technology migrations
- Cross-functional project planning
- When thoroughness is more important than speed

#### Agent Sequence

1. **Researcher Agent**: Information gathering
   - Collects relevant context and requirements
   - Identifies constraints and dependencies
   - Documents current state and gaps

2. **Identifier Agent**: Pattern recognition
   - Analyzes research findings
   - Identifies core problems and opportunities
   - Maps relationships between components

3. **Planner Agent**: Strategy development
   - Develops detailed implementation plan
   - Identifies risks and mitigation strategies
   - Creates checkpoint structure

4. **Executor Agent**: Work coordination
   - Breaks plan into actionable steps
   - Prioritizes tasks with dependencies
   - Provides resource estimates

5. **Reviewer Agent** (optional): Quality validation
   - Validates plan completeness
   - Identifies gaps in reasoning
   - Confirms resource feasibility

#### Example Workflow

**Scenario**: Planning a database migration from PostgreSQL to managed Cloud SQL.

```
Researcher Output:
"Current State:
- 50 databases across 3 environments
- Heavy reliance on custom functions and triggers
- 2 weeks old backups only
- Migration window: 4-hour maintenance window
Key Dependencies: Data warehouse feeds, analytics pipeline"

Identifier Output:
"Core Issues Identified:
1. Custom function incompatibility (must rewrite ~30 functions)
2. Backup strategy insufficient for 0-data-loss requirement
3. Schema differences in managed environment
4. Dependency ordering: Analytics pipeline affected last

Critical Path: Functions → Backup validation → Schema → Cutover"

Planner Output:
"Phased Approach:
Phase 1 (Week 1): Analysis and function rewrite
Phase 2 (Week 2): Test migration, backup validation
Phase 3 (Week 3): Production migration preparation
Phase 4 (Week 4): Execution and validation

Risk Mitigation:
- Parallel database for rollback
- Function testing harness
- Staged cutover by database type"

Executor Output:
"Detailed Task Breakdown (28 tasks):
Week 1: 8 tasks (function audit and rewrite)
Week 2: 10 tasks (testing and validation)
Week 3: 6 tasks (production prep)
Week 4: 4 tasks (execution and monitoring)

Resource Estimate: 1 DBA (full-time), 2 engineers (50% each)"

Reviewer Output:
"Plan Validation:
✓ All 30 functions addressed
✓ Backup strategy sufficient
✓ Rollback plan documented
✓ Resource allocation realistic
? Consider third-party migration tool evaluation"
```

#### Timeline Estimate

- **Research Phase**: 8-12 minutes
- **Identification Phase**: 6-10 minutes
- **Planning Phase**: 8-12 minutes
- **Execution Planning**: 5-8 minutes
- **Review Phase**: 3-5 minutes
- **Total**: 30-60 minutes

#### Key Metrics for Success

- Plan completeness (all known factors addressed)
- Risk identification rate (critical risks surfaced)
- Timeline accuracy (actual vs estimated)
- Resource utilization (estimate accuracy)

---

### Quick Iteration Pattern

**Overview**: A rapid feedback loop pattern for quickly iterating on solutions with repeated refinement cycles.

#### When to Use

- Prototyping and POC development
- Content refinement and editing
- API design exploration
- UI/UX iteration
- Requirements clarification
- Code review and improvement cycles
- When feedback is more valuable than perfection

#### Agent Sequence

1. **Generator Agent**: Creates initial solution
   - Produces first working version
   - Captures core requirements
   - Focuses on functionality over polish

2. **Critic Agent**: Identifies issues and opportunities
   - Reviews against requirements
   - Identifies gaps and problems
   - Suggests specific improvements

3. **Refiner Agent**: Implements improvements
   - Acts on critic feedback
   - Preserves working elements
   - Delivers improved version

*Cycle repeats until quality threshold met (typically 2-3 iterations)*

#### Example Workflow

**Scenario**: Developing API endpoint for user preferences.

```
ITERATION 1

Generator Output:
"POST /api/v1/user/preferences
Body: { category: string, value: any }
Response: { id, created_at }
Simple implementation, stores preferences in default table"

Critic Output:
"Issues Identified:
1. No validation of category values (should be enum)
2. Missing user authorization check
3. No versioning strategy for preference schema
4. Error handling incomplete
Recommendation: 2-3 iterations needed"

Refiner Output:
"Improvements Applied:
+ Added category enum validation
+ Added user authorization middleware
+ Added preference versioning field
+ Added comprehensive error codes
Ready for iteration 2"

---

ITERATION 2

Critic Output:
"Better! Remaining issues:
1. Should support bulk operations
2. Need audit logging for compliance
3. Response should include validation errors
4. Missing rate limiting
Recommendation: 1-2 more iterations"

Refiner Output:
"Improvements Applied:
+ Added PATCH for bulk updates
+ Added audit logging
+ Enhanced error response schema
+ Added rate limiting headers
Ready for iteration 3"

---

ITERATION 3

Critic Output:
"Excellent! Only minor items:
1. Documentation complete
2. Examples provided
3. Consider versioning strategy in header
READY FOR RELEASE ✓"
```

#### Timeline Estimate

- **Per Iteration**:
  - Generator: 3-5 minutes
  - Critic: 2-4 minutes
  - Refiner: 4-6 minutes
  
- **Total** (3 iterations): 20-45 minutes

#### Key Metrics for Success

- Convergence speed (fewer iterations to quality)
- Issue identification accuracy (critic precision)
- Requirement coverage (final version addresses all requirements)
- Stakeholder satisfaction with final output

---

## Pattern Selection Guide

### Decision Matrix

Use this matrix to select the right pattern for your task:

| Decision Factor | AB Method | RIPER | Quick Iteration |
|-----------------|-----------|-------|-----------------|
| **Timeline Available** | 15-30 min | 30-60 min | 20-45 min |
| **Decision Urgency** | High | Medium | Low |
| **Information Availability** | High | Medium | Low |
| **Complexity** | Medium | High | Medium |
| **Stakeholder Input** | Critical | Helpful | Iterative |
| **Risk Tolerance** | Low | High | Medium |

### Quick Selection Checklist

**Choose AB Method if...**
- You need a decision in the next 30 minutes
- There are exactly 2 viable approaches
- Stakeholders are divided
- Risk mitigation is critical

**Choose RIPER Workflow if...**
- You have 60+ minutes available
- Task is complex with many unknowns
- Thorough planning is more important than speed
- Multiple phases or dependencies exist

**Choose Quick Iteration if...**
- You're exploring solutions
- User feedback will guide direction
- You have 45+ minutes for cycles
- Multiple reviews/refinements are expected

### Composition Examples

**Small Feature**: Quick Iteration (2 cycles) = 25 minutes

**Medium Initiative**: RIPER Workflow = 45 minutes

**Critical Decision**: AB Method + Decision Review = 40 minutes

**Complex Project**: RIPER (60 min) + Quick Iteration (35 min) = 95 minutes

---

## Pattern Principles

### Universal Guidelines

1. **Clear Input Definition**: Always start with explicit requirements, constraints, and success criteria
2. **Agent Specialization**: Each agent should have a distinct role and perspective
3. **Documentation**: Each agent should explain reasoning, not just conclusions
4. **Iteration Awareness**: Agents should know if they're in a feedback loop or one-shot analysis
5. **Quality Checkpoints**: Build in validation steps before delivering outputs

### Optimization Tips

- **Time Reduction**: Reduce agent count, compress phases, parallel processing
- **Quality Improvement**: Add review phases, increase iteration cycles, add specialist agents
- **Consistency**: Use the same agent roles for similar tasks
- **Feedback**: Track what works well in your domain, customize patterns accordingly

---

## Next Steps

- Review patterns that match your current workflows
- Identify 1-2 patterns to pilot
- Customize patterns for your specific domain
- Track metrics to validate pattern effectiveness

For additional patterns (Serial Processing, Parallel Synthesis, Expert Panel, etc.), see the extended library.

---

*Last Updated: 2025-11-08*
*Version: 1.0 - Foundation Release*
