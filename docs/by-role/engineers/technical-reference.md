# Technical Reference

**Comprehensive technical documentation for the claude-oak-agents system internals**

This document consolidates technical references for engineers working with or extending the agent system. For PM-focused documentation, see [PM_QUICK_START.md](../PM_QUICK_START.md) and [PM_WORKFLOWS.md](../PM_WORKFLOWS.md).

## Table of Contents

1. [Workflow Tracking System](#workflow-tracking-system)
2. [Success Metrics Reference](#success-metrics-reference)
3. [Adaptive System Design](#adaptive-system-design)
4. [Metadata-Only Prompts](#metadata-only-prompts)

---

## Workflow Tracking System

### Overview

Phase 2A workflow tracking enables the Main LLM to link related agent invocations in multi-agent coordination workflows.

**Features**:
- **Workflow ID**: Unique identifier linking agents in a workflow
- **Parent Invocation ID**: Tracks agent execution sequence
- **Backward Compatible**: Single-agent tasks work unchanged
- **Query Tools**: Shell scripts for workflow analysis

### Generating Workflow IDs

```python
from telemetry.workflow import generate_workflow_id

# For Main LLM coordination
workflow_id = generate_workflow_id()
# Returns: "wf-20251022-a1b2c3d4"
```

### Multi-Agent Workflow Pattern

```python
from telemetry.logger import TelemetryLogger
from telemetry.workflow import generate_workflow_id

logger = TelemetryLogger()
workflow_id = generate_workflow_id()

# Agent 1: Design analysis
inv_1 = logger.log_invocation(
    agent_name="design-simplicity-advisor",
    agent_type="meta",
    task_description="Analyze API design",
    workflow_id=workflow_id,
    parent_invocation_id=None  # First agent
)

# Agent 2: Implementation
inv_2 = logger.log_invocation(
    agent_name="backend-architect",
    agent_type="development",
    task_description="Implement API",
    workflow_id=workflow_id,
    parent_invocation_id=inv_1  # Links to Agent 1
)

# Agent 3: Testing
inv_3 = logger.log_invocation(
    agent_name="unit-test-expert",
    agent_type="quality",
    task_description="Create unit tests",
    workflow_id=workflow_id,
    parent_invocation_id=inv_2  # Links to Agent 2
)
```

### Environment Variables (Hook-Based)

When invoking agents via hooks, set environment variables:

```bash
# Main LLM sets workflow context
export OAK_WORKFLOW_ID="wf-20251022-a1b2c3d4"
export OAK_PARENT_INVOCATION_ID="<previous-invocation-id>"

# Invoke agent
./hooks/pre_agent_hook.py backend-architect development "Implement API"
```

### Querying Workflows

```bash
# List all workflows
./scripts/query_workflow.sh --list-all

# List today's workflows
./scripts/query_workflow.sh --list-today

# Query specific workflow
./scripts/query_workflow.sh wf-20251022-a1b2c3d4
```

**Output Example**:
```
Workflow: wf-20251022-a1b2c3d4

TIMESTAMP                    AGENT                      STATUS   DURATION
2025-10-22T05:06:43.023829Z  design-simplicity-advisor  success  12.5
2025-10-22T05:06:55.526650Z  backend-architect          success  45.3
2025-10-22T05:07:40.829537Z  unit-test-expert           success  8.2
```

### Telemetry Schema

```json
{
  "timestamp": "2025-10-22T05:06:43.023829Z",
  "session_id": "abc123...",
  "invocation_id": "b0baf654-572f-41f6-b41f-ae00cf31e5ab",
  "agent_name": "design-simplicity-advisor",
  "agent_type": "meta",
  "task_description": "Analyze API design",
  "workflow_id": "wf-20251022-a1b2c3d4",
  "parent_invocation_id": null,
  "tools_used": [],
  "duration_seconds": 12.5,
  "outcome": {
    "status": "success"
  }
}
```

### Main LLM Coordination Pattern

```python
# Step 1: Generate workflow ID
workflow_id = generate_workflow_id()

# Step 2: Log workflow start
logger.log_workflow_start(
    workflow_id=workflow_id,
    project_name="Secure REST API",
    agent_plan=["design-simplicity-advisor", "backend-architect", "security-auditor"],
    estimated_duration=3600
)

# Step 3: Execute agents with handoff tracking
inv_1 = execute_agent("design-simplicity-advisor", workflow_id)

logger.log_agent_handoff(
    workflow_id=workflow_id,
    from_agent="design-simplicity-advisor",
    to_agent="backend-architect",
    artifacts=["artifacts/design-simplicity-advisor/architecture.md"]
)

inv_2 = execute_agent("backend-architect", workflow_id, parent_id=inv_1)

# Step 4: Log workflow completion
logger.log_workflow_complete(
    workflow_id=workflow_id,
    duration_seconds=3200,
    success=True,
    agents_executed=["design-simplicity-advisor", "backend-architect", "security-auditor"]
)
```

### Benefits

- **Workflow Visibility**: Complete tracking of multi-agent coordination
- **Performance Analysis**: Measure workflow duration and bottlenecks
- **Agent Selection**: Historical data guides future agent choices
- **Coordination Overhead**: Measure cost of multi-agent workflows
- **Debugging**: Trace agent execution sequences for failures

### Limitations (Phase 2A)

- No structured artifact tracking (Phase 3)
- No workflow state management (Phase 3)
- No real-time workflow monitoring (Phase 4)
- Manual workflow ID management

### Future Phases

- **Phase 3**: Structured artifact files with validation
- **Phase 4**: Real-time monitoring and workflow visualization
- **Phase 5**: Automatic workflow optimization based on telemetry

---

## Success Metrics Reference

### "How do we know the adaptive system is working?"

### Primary Success Indicators (Track Weekly)

| Metric | Target | Measurement | What Success Looks Like |
|--------|--------|-------------|------------------------|
| **False Completion Rate** | <5% | Weekly tracking per agent | Declining trend over 3 months |
| **First-Time Success Rate** | >90% | Weekly tracking per agent | Improving trend over 3 months |
| **User Satisfaction** | >4.0/5.0 | Feedback prompts | Stable or improving |
| **Time to Resolution** | <48 hours | Issue lifecycle tracking | Decreasing over time |

### Secondary Success Indicators (Track Monthly)

| Metric | Target | What It Measures |
|--------|--------|------------------|
| **Improvement Velocity** | >20% improvement in 2 weeks | How fast agents improve after updates |
| **Learning Stability** | No >5% regression after 4 weeks | Do improvements stick? |
| **Issue Coverage** | >60% of patterns addressed | Are we fixing the right things? |
| **System Health** | >85% agents in "green" | Overall ecosystem health |

### User-Centric Success (Qualitative)

| Question | Success Indicator |
|----------|-------------------|
| "Am I asking less often for the same thing?" | Repeat request rate <5% (was 15%) |
| "Do I trust agents will complete tasks?" | Comfortable delegating without double-checking |
| "Is the system getting better?" | Metrics trending positive for 3+ months |

### Health Status Indicators

#### Per Agent
- 🟢 **Green**: Success rate >85%, false completion <10%, improving trend
- 🟡 **Yellow**: Success rate 70-85%, false completion 10-20%, stable
- 🔴 **Red**: Success rate <70%, false completion >20%, declining trend

#### System-Wide
- 🟢 **Green**: >90% agents in green, false completions declining
- 🟡 **Yellow**: 70-90% agents in green, false completions stable
- 🔴 **Red**: <70% agents in green, false completions increasing

### Monthly Success Checklist

At the end of each month, check:

- [ ] False completion rate decreased or <5%
- [ ] First-time success rate increased or >90%
- [ ] Average user satisfaction >4.0
- [ ] Time to resolution decreased or <48 hours
- [ ] At least 1 agent improvement applied and validated
- [ ] No agents in "red" status for >2 weeks
- [ ] User confidence in system is stable or improving
- [ ] System generated improvement proposals for review

**If 6+ items checked**: ✅ System is successfully adapting
**If 4-5 items checked**: 🟡 System is stable, needs attention
**If <4 items checked**: 🔴 System needs intervention

### Tracking Commands

```bash
# Check current metrics
oak-metrics

# View trends dashboard
oak-trends

# View success dashboard
oak-success-dashboard

# Weekly review (includes metrics)
oak-weekly-review

# Monthly analysis (includes full success report)
oak-monthly-review
```

### Key Insight

**The adaptive system is working if**:
- You're asking for the same thing less often
- Agents complete tasks correctly on first try more often
- You trust the system more over time
- The data confirms your intuition

**Simple test**: If you had to repeat a request 3 times last month, and now you only repeat once (or not at all), the system is adapting successfully.

---

## Adaptive System Design

### Overview

The complete improvement cycle for the claude-oak-agents system, from issue detection through root cause analysis, agent improvements, and validation of success.

**Core Question**: "If we're building an agentic system that adapts to your workflows, how do we know we're succeeding?"

### Complete Improvement Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTINUOUS IMPROVEMENT LOOP                  │
└─────────────────────────────────────────────────────────────────┘

Phase 1: DETECTION (✅ COMPLETE)
├── User asks twice → False completion detected
├── Issue created (open state)
├── Weekly/monthly review prompts user
└── User confirms: resolved, still_broken, or test_later

Phase 2: ROOT CAUSE ANALYSIS (🚧 DESIGN)
├── Analyze resolved issues monthly
├── Identify patterns (same agent, same error type, same domain)
├── Extract root causes:
│   ├── Missing verification steps
│   ├── Unclear agent instructions
│   ├── Wrong approach/strategy
│   └── Missing domain knowledge
├── Generate improvement proposals
└── User reviews and approves changes

Phase 3: AGENT IMPROVEMENT (🚧 DESIGN)
├── Update agent markdown files (instructions, checklists, examples)
├── Create versioned agent (v1 → v2)
├── Deploy improved agent
└── Track which version is active

Phase 4: VALIDATION (🚧 DESIGN)
├── A/B testing: Compare old vs new agent performance
├── Track metrics over time (success rate, false completion rate)
├── Statistical significance testing
└── User feedback correlation

Phase 5: LEARNING (🔮 FUTURE)
├── System learns from validated improvements
├── Automated pattern detection
├── Self-guided agent updates (with human approval)
└── ML-based performance prediction
```

### Phase 2: Root Cause Analysis

#### Data Analysis

**Input**: Resolved issues from `telemetry/issues.jsonl`

**Pattern Detection**:
```yaml
patterns:
  by_agent:
    - Which agents have most false completions?
    - What types of tasks do they fail on?

  by_error_type:
    - Verification failures (didn't test before claiming done)
    - Incomplete implementation (partial fixes)
    - Misunderstanding requirements
    - Wrong approach/strategy

  by_domain:
    - Frontend errors (UI bugs, state management)
    - Backend errors (API, database)
    - Infrastructure errors (deployment, CDK)

  temporal_patterns:
    - Are errors increasing or decreasing over time?
    - Do certain agents improve after updates?
```

#### Root Cause Categories

**1. Missing Verification**
- Agent claimed completion without testing
- Example: "Fix button crash" but didn't click button
- Solution: Add specific verification step to checklist

**2. Unclear Instructions**
- Agent didn't understand what "done" means
- Example: "Make rows same height" interpreted differently
- Solution: Add concrete examples to agent markdown

**3. Wrong Approach**
- Agent used wrong strategy for problem
- Example: Used CSS when component refactor needed
- Solution: Add decision tree or approach guidance

**4. Missing Domain Knowledge**
- Agent lacks specific framework/library knowledge
- Example: Vue composition API patterns not understood
- Solution: Add framework-specific examples

**5. Incomplete Context**
- Agent didn't consider full system state
- Example: Fixed component but broke integration
- Solution: Add context-awareness instructions

### Phase 3: Agent Metrics Tracking

#### Agent-Level Metrics

**Per Agent** (`telemetry/agent_metrics.jsonl`):
```json
{
  "timestamp": "2025-10-21T00:00:00Z",
  "agent_name": "frontend-developer",
  "period": "week",
  "metrics": {
    "invocations": 42,
    "success_rate": 0.85,
    "false_completion_rate": 0.12,
    "avg_resolution_time_minutes": 23.5,
    "user_satisfaction": 4.2,
    "rework_rate": 0.08,
    "issues_opened": 5,
    "issues_resolved": 4,
    "issues_reopened": 1
  },
  "version": "v2.1"
}
```

**Key Metrics**:
- **Success Rate**: % of invocations marked successful on first try
- **False Completion Rate**: % of invocations that user had to repeat
- **Avg Resolution Time**: Time from issue detected to user-confirmed resolved
- **User Satisfaction**: Average rating from feedback prompts (1-5)
- **Rework Rate**: % of tasks requiring follow-up work
- **Issues by State**: Open, in_progress, needs_verification, resolved

### Phase 4: A/B Testing & Validation

#### When to A/B Test

**Triggers**:
- Major agent instruction changes (>50% of content modified)
- New approach/strategy introduced
- User requests validation before full rollout
- After 3+ improvements to same agent

#### A/B Test Configuration

```yaml
test_name: "Frontend Developer v2 - Better Verification"
agent: frontend-developer
baseline_version: v1
test_version: v2
start_date: "2025-11-01"
duration_days: 14
traffic_split: 0.5  # 50% traffic to each version

hypothesis: "Adding explicit button-click verification will reduce false completions by 50%"

metrics:
  primary:
    - false_completion_rate
  secondary:
    - success_rate
    - avg_resolution_time
    - user_satisfaction

success_criteria:
  false_completion_rate:
    improvement_threshold: 0.5  # 50% reduction
    statistical_significance: 0.05  # p < 0.05

  sample_size_min: 30  # Need 30+ invocations per version

abort_conditions:
  - success_rate < 0.6  # If drops below 60%, abort test
  - user_complaints > 5  # If 5+ complaints, abort
```

#### Statistical Validation

**Script**: `scripts/phase4/validate_test.py`

**Analysis**:
```python
# Two-sample t-test for false completion rate
baseline_rate = [0.15, 0.12, 0.18, ...]  # 30 samples
test_rate = [0.08, 0.05, 0.10, ...]      # 30 samples

t_stat, p_value = stats.ttest_ind(baseline_rate, test_rate)

if p_value < 0.05 and mean(test_rate) < mean(baseline_rate):
    print("✅ Improvement is statistically significant")
    print(f"   Baseline: {mean(baseline_rate):.1%}")
    print(f"   Test: {mean(test_rate):.1%}")
    print(f"   Improvement: {(1 - mean(test_rate)/mean(baseline_rate))*100:.0f}%")
else:
    print("❌ No significant improvement")
```

### Implementation Roadmap

#### Phase 2: Root Cause Analysis (Month 1)
**Effort**: 2 weeks development + 2 weeks validation

**Deliverables**:
1. `scripts/phase2/analyze_root_causes.py` - Pattern detection script
2. `reports/improvement_proposals/` - Generated proposals
3. Review workflow commands (`oak-review-proposals`, etc.)
4. User documentation

**Success Criteria**:
- Generate first improvement proposals from real issues
- User successfully reviews and applies 1+ improvement
- Updated agent shows measurable improvement

#### Phase 3: Metrics Tracking (Month 2)
**Effort**: 2 weeks development + 2 weeks dashboard creation

**Deliverables**:
1. `scripts/phase3/track_metrics.py` - Metrics collection
2. `scripts/phase3/analyze_trends.py` - Trend analysis
3. `reports/trends/*.html` - Interactive dashboards
4. Weekly/monthly metric summaries

**Success Criteria**:
- Metrics collected automatically from telemetry
- Trends visible in dashboard
- Can identify which agents are improving/declining

#### Phase 4: A/B Testing (Month 3)
**Effort**: 3 weeks development + 1 week validation

**Deliverables**:
1. `scripts/phase4/setup_test.py` - A/B test configuration
2. `scripts/phase4/validate_test.py` - Statistical analysis
3. Main LLM routing integration (50/50 traffic split)
4. Test management commands

**Success Criteria**:
- Successfully run first A/B test
- Statistical validation shows clear winner
- Deploy improved agent version to production

---

## Metadata-Only Prompts

### Overview

Anthropic's Agent Skills architecture uses **progressive disclosure** where only lightweight metadata is loaded into the system prompt at startup, with full agent definitions loaded on-demand.

OaK Agents implements this same pattern for dramatic efficiency gains.

### The Problem: Prompt Bloat

#### Traditional Approach (Heavy)

```python
# Load ALL agent definitions into system prompt
system_prompt = """
You have access to the following agents:

## Frontend Developer
<full 500-line agent definition>

## Backend Architect
<full 600-line agent definition>

## Security Auditor
<full 800-line agent definition>

... (29 more agents)
"""

# Result: 50-100KB system prompt
# Problem: Context window waste, slower inference, higher costs
```

**Issues**:
- ❌ 50-100KB of agent definitions loaded every conversation
- ❌ Most agents never used in a given conversation
- ❌ Slower LLM inference (more context to process)
- ❌ Higher token costs
- ❌ Doesn't scale beyond ~50 agents

#### Metadata-Only Approach (Lightweight)

```python
# Load ONLY metadata into system prompt
system_prompt = """
You have access to the following agents (load full definition when needed):

## Frontend Developer
- Triggers: [react, vue, ui, frontend, component]
- Domains: [frontend-development]
- Priority: medium
- Capabilities: [ui_implementation, browser_compat, responsive_design]

## Backend Architect
- Triggers: [api, database, backend, server, microservices]
- Domains: [backend-development]
- Priority: medium
- Capabilities: [api_design, database_schema, system_architecture]

... (29 more agents - metadata only)
"""

# Result: 5-10KB system prompt
# Benefit: 90%+ reduction, instant classification
```

**Advantages**:
- ✅ 5-10KB system prompt (90% reduction)
- ✅ Full definitions loaded only when agent is invoked
- ✅ Faster classification (less context)
- ✅ Lower token costs
- ✅ Scales to 100+ agents easily

### 3-Level Progressive Disclosure

```
Level 1: STARTUP (Always Loaded)
├─ Agent name
├─ Trigger keywords (5-15)
├─ File patterns
├─ Domains
├─ Priority
└─ Capabilities list

Level 2: INVOCATION (Loaded on-demand)
├─ Full agent definition (markdown)
├─ Operating instructions
├─ Context awareness
└─ Coordination patterns

Level 3: EXECUTION (Loaded as needed)
├─ Bundled scripts
├─ Reference documentation
├─ Code templates
└─ Historical metrics
```

### Agent Discovery Flow

```
1. User Request: "Fix security vulnerability in auth endpoint"
   ↓
2. Main LLM Classification (using Level 1 metadata only)
   - Extract keywords: ["security", "vulnerability", "auth"]
   - Match against agent triggers
   - Best match: security-auditor (triggers include "security", "vulnerability", "auth")
   ↓
3. Agent Selection Decision
   - Selected: security-auditor
   - Confidence: High (multiple keyword matches)
   ↓
4. Load Level 2 (Full Definition)
   - Read agents/security-auditor/agent.md
   - Parse complete instructions
   ↓
5. Execute Agent
   - Agent has full context
   - Can access Level 3 resources as needed
```

### Performance Comparison

| Metric | Full Definitions | Metadata-Only | Improvement |
|--------|-----------------|---------------|-------------|
| System Prompt Size | 87KB | 6KB | **93% smaller** |
| Agents Supported | ~30 (practical limit) | 100+ | **3x+ scalability** |
| Classification Speed | ~2s | ~0.5s | **4x faster** |
| Token Cost (per conversation) | ~87K tokens | ~6K tokens | **93% savings** |
| Memory Usage | High | Low | **Minimal footprint** |

### Scalability Impact

```
Full Definitions Approach:
- 29 agents × 3KB avg = 87KB system prompt
- 50 agents × 3KB avg = 150KB system prompt  ⚠️ Too large
- 100 agents × 3KB avg = 300KB system prompt  ❌ Breaks context window

Metadata-Only Approach:
- 29 agents × 200 bytes = 5.8KB system prompt  ✅
- 100 agents × 200 bytes = 20KB system prompt  ✅ Still efficient
- 500 agents × 200 bytes = 100KB system prompt  ✅ Feasible
```

### Enabling Metadata-Only Prompts

#### Current Status

**Metadata-only prompts are built but NOT YET ENABLED by default.**

The infrastructure exists, but CLAUDE.md still uses full agent definitions for 100% backward compatibility.

#### When to Enable

**✅ Enable If:**
- **You have 20+ agents** - Significant benefits at this scale
- **Planning to scale to 50+** - Essential for growth
- **Token costs matter** - 93% reduction in prompt tokens
- **Classification is slow** - Faster with less context
- **Using multi-file agents** - Designed for this architecture

**⏸️ Wait If:**
- **You have <10 agents** - Benefits are minimal
- **Single-file agents only** - Full definitions already small
- **System is working perfectly** - "If it ain't broke..."
- **Risk-averse** - Wait for more community validation

#### One-Command Enablement

```bash
cd ~/Projects/claude-oak-agents
./scripts/enable_metadata_prompts.sh
```

**What it does**:
1. Backs up current CLAUDE.md
2. Generates metadata-only agent listing
3. Replaces agent matrix with metadata
4. Shows before/after size comparison

**Expected output**:
```
🔧 Enabling Metadata-Only Agent Prompts

📦 Creating backup: CLAUDE.md.backup.20251016_103000
🔍 Generating metadata listing...
📊 Size comparison:
   Original CLAUDE.md: 89.2KB
   Metadata listing: 6.1KB

✅ Metadata-only prompts enabled!

📊 Results:
   Original size: 89.2KB
   New size: 8.5KB
   Reduction: 90.5%

📁 Backup saved: CLAUDE.md.backup.20251016_103000
```

### What Changes

#### Before (Full Definitions)

```markdown
## Agent Responsibility Matrix

#### Core Development
- **frontend-developer**: UI/UX implementation, modern framework patterns...
  <500 lines of detailed responsibilities>
  <operating instructions>
  <examples>
  <coordination patterns>

- **backend-architect**: API design, database schema...
  <600 lines of detailed responsibilities>
  ...

[Repeat for 29 agents = 87KB]
```

#### After (Metadata-Only)

```markdown
## Agent Responsibility Matrix (Metadata-Only Discovery)

**NOTE**: Full agent definitions are loaded on-demand when invoked.
This achieves 93% size reduction while maintaining discovery capabilities.

# Available Agents (Ultra-Compact)

**Total**: 29 agents | Full definitions loaded on-demand

- **frontend-developer** [medium]: react, vue, ui, frontend, component
- **backend-architect** [medium]: api, database, backend, server, microservices
- **security-auditor** [high]: security, vulnerability, audit, compliance | Scripts: 3 | BLOCKING
...

[29 agents = 6KB]

### Agent Selection Process
1. Keyword matching against triggers
2. File pattern matching
3. Domain matching
4. Load full definition on-demand when invoked
```

### Rollback

#### Automatic Rollback

The script creates timestamped backups:

```bash
# List backups
ls -lh CLAUDE.md.backup.*

# Restore from backup
cp CLAUDE.md.backup.20251016_103000 CLAUDE.md
```

#### Manual Rollback

```bash
git checkout CLAUDE.md
```

### Testing After Enablement

**1. Verify Agent Loading**:
```bash
# Test metadata loading
python3 core/agent_loader.py --command=metadata

# Should show all 29 agents
```

**2. Test Agent Invocation**:
Create a test request in Claude Code:
```
User: "Review this code for security vulnerabilities"
```

Expected behavior:
1. Main LLM matches keywords: "security", "vulnerabilities"
2. Selects: security-auditor
3. Loads full definition on-demand
4. Executes agent normally

**3. Verify Script Execution**:
```bash
# Test bundled script
python3 agents/security-auditor-multifile/scripts/dependency_scan.py \
  --directory=. \
  --output-format=markdown
```

Should work identically to before.

### FAQ

**Q: Will my existing agents break?**
**A**: No. The agent loader supports both single-file and multi-file formats. Existing agents work unchanged.

**Q: Do I need to migrate all agents?**
**A**: No. Metadata-only works with single-file agents too. The loader extracts metadata from frontmatter.

**Q: What if agent discovery fails?**
**A**: The system falls back to general-purpose agent and logs a routing failure. You can restore the full definitions anytime.

**Q: Can I customize the metadata listing?**
**A**: Yes. Edit `core/generate_agent_metadata.py` to change the output format.

**Q: Will this break my custom agents?**
**A**: No, as long as they have proper YAML frontmatter with `name` and `description` fields.

---

## Resources

### Implementation Files
- [telemetry/workflow.py](../../telemetry/workflow.py) - Workflow ID generation
- [telemetry/logger.py](../../telemetry/logger.py) - Telemetry logging
- [scripts/query_workflow.sh](../../scripts/query_workflow.sh) - Workflow queries
- [core/agent_loader.py](../../core/agent_loader.py) - Agent loading
- [core/generate_agent_metadata.py](../../core/generate_agent_metadata.py) - Metadata generation
- [scripts/enable_metadata_prompts.sh](../../scripts/enable_metadata_prompts.sh) - Enablement script

### Related Documentation
- [HYBRID_PLANNING_GUIDE.md](../HYBRID_PLANNING_GUIDE.md) - Multi-agent planning
- [MODEL_SELECTION_STRATEGY.md](../MODEL_SELECTION_STRATEGY.md) - Model tier optimization
- [PM_CAPABILITIES.md](../PM_CAPABILITIES.md) - Product manager capabilities
- [oak-design/OAK_ARCHITECTURE.md](../oak-design/OAK_ARCHITECTURE.md) - Complete architecture

### External References
- [Anthropic Agent Skills Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Anthropic Documentation](https://docs.anthropic.com/)

---

**Last Updated**: 2025-10-24
**Status**: Active - All systems operational
