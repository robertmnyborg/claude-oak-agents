# Model Selection Strategy

**Version**: 1.0
**Date**: 2025-10-21
**Status**: Active

---

## Overview

This document defines the model selection strategy for claude-oak-agents, optimizing for cost, speed, and quality across different agent types.

**Key Principle**: Match model capability to task complexity
- **Premium models** (Opus, Sonnet 4) for strategic decisions and complex reasoning
- **Balanced models** (Sonnet 3.5) for standard development work
- **Fast models** (Haiku) for execution tasks and pattern-following

---

## Model Tiers

### Tier 1: Premium (Opus 3 / Sonnet 4)
**Cost**: $15-75 per million tokens (output)
**Speed**: 1-5 seconds
**Best For**: Strategic planning, architectural design, complex reasoning, nuanced judgment

**Characteristics**:
- Deep multi-step reasoning
- Nuanced tradeoff analysis
- Creative problem-solving
- Long-context understanding
- Strategic decision-making

**When to Use**:
- Decisions affecting entire project architecture
- Business strategy requiring technical context
- Complex system design with many constraints
- Nuanced complexity vs simplicity tradeoffs
- Portfolio management and strategic analysis

---

### Tier 2: Balanced (Sonnet 3.5 / Sonnet 4)
**Cost**: $3-15 per million tokens (output)
**Speed**: 1-2 seconds
**Best For**: Code generation, debugging, refactoring, technical analysis

**Characteristics**:
- Strong code generation
- Good debugging capability
- Balanced reasoning and speed
- Most general-purpose tasks
- Standard development work

**When to Use**:
- API design and implementation
- UI/UX component development
- Security threat analysis
- Performance optimization
- Code quality review
- Complex debugging

---

### Tier 3: Fast (Haiku 3.5)
**Cost**: $1-5 per million tokens (output)
**Speed**: 300-500ms
**Best For**: Execution tasks, pattern-following, simple transforms, well-defined procedures

**Characteristics**:
- Extremely fast (3-10x faster than Sonnet)
- Excellent at following instructions literally
- Cost-effective (10x cheaper than Sonnet)
- Best for well-defined, procedural tasks
- Less creative interpretation (feature, not bug)

**When to Use**:
- Git operations (commit, push, branch management)
- Changelog generation from git history
- Simple documentation formatting
- Test generation following templates
- Content formatting and templates
- Simple code transformations

---

## Agent Model Assignments

### Premium Tier (Opus 3 / Sonnet 4)

**Strategic Planning & Architecture**:
- **systems-architect** - System design requires deep reasoning and tradeoff analysis
- **design-simplicity-advisor** - Nuanced complexity assessment, KISS principle application
- **project-manager** - Multi-step coordination, timeline planning, resource allocation
- **product-strategist** - Business strategy + technical feasibility analysis
- **business-analyst** - Requirements analysis with stakeholder context understanding
- **agent-auditor** - Strategic portfolio management, capability gap detection

**Rationale**: These agents make decisions affecting entire projects, architectures, or business outcomes. Premium model cost justified by higher-quality strategic decisions that prevent costly mistakes.

**Expected Impact**:
- Better architectural decisions (fewer rewrites)
- More nuanced complexity analysis
- Improved project planning accuracy
- Strategic insights worth the premium cost

---

### Balanced Tier (Sonnet 3.5 / Sonnet 4)

**Development Specialists**:
- **backend-architect** - API design + implementation requiring good code generation
- **frontend-developer** - UI/UX implementation with framework knowledge
- **mobile-developer** - Cross-platform mobile development
- **blockchain-developer** - Smart contract development (high stakes)
- **ml-engineer** - ML system implementation and pipeline design
- **infrastructure-specialist** - Cloud infrastructure and deployment
- **legacy-maintainer** - Understanding old codebases, careful modernization

**Quality & Security**:
- **security-auditor** - Threat modeling and vulnerability analysis
- **performance-optimizer** - Performance bottleneck identification and optimization
- **code-reviewer** - Code quality assessment and standards enforcement
- **debug-specialist** - Complex debugging requiring deep analysis
- **dependency-scanner** - Security vulnerability analysis

**Analysis & Research**:
- **data-scientist** - Statistical analysis and data processing
- **state-analyzer** - State feature extraction and ranking

**Rationale**: These agents need strong code generation, debugging, and analytical capabilities. Sonnet provides the right balance of quality and cost for standard development work.

**Expected Impact**:
- High-quality code generation
- Good debugging and analysis
- Reasonable cost for frequent use
- Proven track record for development tasks

---

### Fast Tier (Haiku 3.5)

**Workflow & Automation**:
- **git-workflow-manager** - Git operations follow well-defined commands
- **changelog-recorder** - Format git commits into changelog entries

**Documentation & Content**:
- **content-writer** - Follow content templates and style guides
- **technical-documentation-writer** - Document code (straightforward transcription)

**Testing & Quality (Pattern-Based)**:
- **unit-test-expert** - Generate tests following established patterns
- **qa-specialist** - Execute test scripts and report results

**Utility**:
- **general-purpose** - Simple, single-line commands and basic queries

**Rationale**: These agents follow well-defined procedures, templates, or patterns. Haiku's speed (3-10x faster) and cost savings (10x cheaper) make it ideal for high-frequency, procedural tasks.

**Expected Impact**:
- 3-10x faster execution for common operations
- 90% cost reduction for these agents
- Better user experience (faster git operations, instant changelog)
- No quality loss (procedures don't need deep reasoning)

---

## Special Considerations

### When to Override Tier Assignments

**Upgrade to Premium** (Haiku/Sonnet → Opus) if:
- Task involves critical business decisions
- Multiple stakeholders with conflicting requirements
- High-stakes system architecture changes
- Complex regulatory or compliance analysis
- Nuanced tradeoff analysis required

**Downgrade to Fast** (Sonnet → Haiku) if:
- Task is purely procedural
- Well-defined templates exist
- Speed more important than creativity
- High-frequency operations
- Cost optimization needed

**Stay on Balanced** (Sonnet) if:
- Unsure about task complexity
- Task involves code generation
- Debugging complex issues
- Default for most development work

---

## Cost Analysis

### Current State (All Sonnet 4)
**Example**: 1000 agent invocations/month
- Average: 10k tokens input, 5k tokens output per invocation
- Cost: (10M × $3 + 5M × $15) / 1M = **$105/month**

### Optimized (Tiered Strategy)
**Distribution**:
- 10% Premium (Opus): Strategy & architecture
- 60% Balanced (Sonnet): Development
- 30% Fast (Haiku): Execution & automation

**Costs**:
- Premium: 100 invocations × $18 = $18
- Balanced: 600 invocations × $10.50 = $63
- Fast: 300 invocations × $0.60 = $1.80
- **Total: ~$83/month**

**Savings**: **21% cost reduction** + **30% of tasks 3-10x faster**

---

## Performance Expectations

### Premium Tier (Opus/Sonnet 4)
**Strengths**:
- ✅ Deep reasoning and analysis
- ✅ Nuanced judgment calls
- ✅ Creative problem-solving
- ✅ Long-context understanding

**Weaknesses**:
- ⚠️ Slower (3-5s response time)
- ⚠️ More expensive (5-25x cost vs Haiku)
- ⚠️ Overkill for simple tasks

**Best Results**: Strategic planning, architecture design, business analysis

---

### Balanced Tier (Sonnet 3.5/4)
**Strengths**:
- ✅ Strong code generation
- ✅ Good debugging capability
- ✅ Balanced speed (1-2s)
- ✅ Cost-effective for frequent use

**Weaknesses**:
- ⚠️ Less strategic depth than Opus
- ⚠️ Slower than Haiku for simple tasks

**Best Results**: Code generation, refactoring, debugging, analysis

---

### Fast Tier (Haiku 3.5)
**Strengths**:
- ✅ Extremely fast (300-500ms)
- ✅ Very cost-effective (10x cheaper)
- ✅ Excellent at following instructions
- ✅ Consistent, predictable output

**Weaknesses**:
- ⚠️ Less creative reasoning
- ⚠️ Weaker code generation for complex tasks
- ⚠️ Better for procedures than exploration

**Best Results**: Git operations, formatting, template-following, simple transforms

---

## Validation & Testing

### A/B Testing Plan

**Phase 1: Validate Fast Tier** (Week 1-2)
- Test Haiku vs Sonnet for git-workflow-manager
- Measure: Speed, cost, success rate, user satisfaction
- Hypothesis: Haiku performs equally well with 10x cost savings

**Phase 2: Validate Premium Tier** (Week 3-4)
- Test Opus vs Sonnet for systems-architect
- Measure: Architecture quality, decision accuracy, project outcomes
- Hypothesis: Opus provides better strategic decisions worth premium cost

**Phase 3: Optimize Balanced Tier** (Month 2)
- Identify agents on Sonnet that could use Haiku
- Test borderline cases (unit-test-expert, qa-specialist)
- Refine tier assignments based on data

### Success Metrics

**Cost Metrics**:
- Total monthly API costs
- Cost per agent invocation
- Cost savings vs baseline (all Sonnet)

**Quality Metrics**:
- Success rate by model tier
- False completion rate by model
- User satisfaction ratings
- Code quality scores (where applicable)

**Speed Metrics**:
- Average response time by tier
- P95 response time
- User-perceived performance

**Business Metrics**:
- Project success rate (Premium tier)
- Rework reduction (fewer architectural mistakes)
- Developer productivity (faster git operations)

---

## Implementation Notes

### Agent Frontmatter Format

```yaml
---
name: agent-name
description: Agent description
model: opus          # opus, sonnet-4, sonnet, haiku
model_tier: premium  # premium, balanced, fast
model_rationale: "Why this model tier was chosen"
---
```

### Overriding Defaults

**Environment Variable** (future):
```bash
export OAK_MODEL_TIER_OVERRIDE="all=sonnet"  # Force all agents to Sonnet
export OAK_MODEL_TIER_OVERRIDE="git-workflow-manager=haiku,systems-architect=opus"
```

**Per-Invocation Override** (future):
```python
# For critical strategic decisions
invoke_agent("systems-architect", model_override="opus")

# For cost-sensitive testing
invoke_agent("unit-test-expert", model_override="haiku")
```

---

## Telemetry Integration

### Tracking Model Performance

**Metrics to Collect**:
- Model used for each invocation
- Task type and complexity
- Success/failure outcome
- Duration and token usage
- Cost per invocation
- User feedback/ratings

**Storage**:
```json
{
  "invocation_id": "inv-123",
  "agent_name": "systems-architect",
  "model_used": "opus",
  "model_tier": "premium",
  "task_complexity": "high",
  "duration_seconds": 4.2,
  "tokens_input": 8500,
  "tokens_output": 3200,
  "cost_usd": 0.063,
  "outcome": "success",
  "quality_rating": 5
}
```

**Analysis Queries**:
- Which agents have best success rate by model?
- Is Haiku performing well for execution agents?
- Are premium model costs justified by quality?
- Can any Sonnet agents downgrade to Haiku?

---

## Future Enhancements

### Phase 2: Dynamic Model Selection (Month 2+)

**Context-Aware Selection**:
```python
def select_model(agent_name, task_context):
    if task_context.is_critical and task_context.complexity == "high":
        return "opus"  # Upgrade for critical tasks
    elif task_context.is_simple and task_context.is_procedural:
        return "haiku"  # Downgrade for simple tasks
    else:
        return agent.default_model  # Use tier default
```

**Cost-Based Selection**:
- Budget-constrained mode: Prefer Haiku when possible
- Premium mode: Upgrade to Opus for better quality
- Balanced mode: Follow tier defaults

### Phase 3: ML-Driven Optimization (Month 3+)

**Learn from Telemetry**:
- Train model to predict optimal model tier for task
- Features: task type, complexity, agent, historical outcomes
- Optimize for: cost vs quality tradeoff
- Auto-adjust tier assignments based on performance data

---

## References

### Model Pricing (2025-10)

| Model | Input ($/M tokens) | Output ($/M tokens) | Speed |
|-------|-------------------|---------------------|-------|
| Haiku 3.5 | $1 | $5 | 300ms |
| Sonnet 3.5 | $3 | $15 | 1s |
| Sonnet 4 | $3 | $15 | 1s |
| Opus 3 | $15 | $75 | 3-5s |

### Model Capabilities

**Haiku 3.5**:
- Best for: Pattern-following, simple transforms, procedural tasks
- Strengths: Speed, cost, instruction-following
- Limitations: Less creative reasoning, weaker complex code generation

**Sonnet 3.5/4**:
- Best for: Code generation, debugging, balanced tasks
- Strengths: Strong coding, good reasoning, balanced cost/performance
- Limitations: Not as strategic as Opus, not as fast as Haiku

**Opus 3**:
- Best for: Strategic planning, complex reasoning, research
- Strengths: Deep analysis, nuanced judgment, creative solutions
- Limitations: Slower, more expensive, overkill for simple tasks

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-21 | Initial model tier strategy based on agent analysis and cost optimization |

---

**Status**: ✅ Active - Implementation in progress
**Next Review**: 2025-11-21 (after 1 month of telemetry data)
**Owner**: Repository maintainers
