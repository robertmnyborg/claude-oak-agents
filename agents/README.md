# Pending Agent Reviews

This directory contains newly created agents awaiting human approval before deployment.

## How It Works

### Automatic Agent Creation
When the system detects a capability gap (no suitable agent exists):
1. **Gap Detection**: Main LLM classifies request but finds no matching agent
2. **Threshold Check**:
   - Explicit user request → Create immediately
   - 3+ failures for same domain → Create immediately
   - Otherwise → Log for monthly review
3. **Auto-Creation**: agent-creator designs and implements new agent
4. **Saved Here**: Agent saved to this directory for review
5. **Notification**: You receive notification and shell prompt
6. **Review Required**: Agent cannot be used until approved

### Agent Template
All agents follow this structure:

```markdown
---
name: agent-name
description: Brief description of agent's purpose
color: agent-name
---

# Agent Name

## Purpose
What the agent does and why it exists.

## Core Identity
Primary responsibilities and focus areas.

## Operating Instructions
How the agent analyzes and responds to requests.

## Context Awareness
What the agent considers when working.

## Input/Output Examples
Concrete examples of usage.

## Tools and Integrations
Which tools the agent uses.

## Safety and Boundaries
What the agent should NOT do.

## Metrics for Evaluation
How to measure agent success.

## Coordination Patterns
How agent works with other agents.
```

## Review Workflow

### 1. Notification
When new agent is created, you'll see:
- **Shell prompt** on terminal open
- **macOS notification** if automation enabled
- **oak-status** shows pending count

### 2. List Pending Agents
```bash
oak-list-pending-agents
```

Output:
```
📋 Agents Pending Review (2):

  financial-analyst
  └─ Financial analysis, ROI calculation, investment evaluation
  └─ Created: 0 days ago

  research-specialist
  └─ Research and information synthesis for technical topics
  └─ Created: 1 days ago
```

### 3. Review Agent Specification
```bash
oak-review-agent financial-analyst
```

This displays the full agent specification including:
- Purpose and responsibilities
- Operating instructions
- Input/output examples
- Safety boundaries
- Coordination patterns

### 4. Make Decision

#### Option A: Approve (Deploy Immediately)
```bash
oak-approve-agent financial-analyst
```

Agent is moved to `agents/` directory and becomes immediately available for delegation.

#### Option B: Modify (Edit Before Approving)
```bash
oak-modify-agent financial-analyst
```

Opens agent in your default editor (VS Code > vim > nano). After editing:
- Script asks if you want to approve immediately
- Or save and approve later with `oak-approve-agent`

#### Option C: Reject (Archive with Reason)
```bash
oak-reject-agent financial-analyst "Too broad, conflicts with existing agent"
```

Agent is moved to `agents/rejected/` with metadata about rejection reasoning.

## Review Criteria

### Quality Checklist
- [ ] **Clear Purpose**: Agent has well-defined, focused responsibility
- [ ] **No Overlap**: Doesn't duplicate existing agent capabilities
- [ ] **Proper Template**: Follows all required sections
- [ ] **Good Examples**: Input/output examples are concrete and useful
- [ ] **Safety Boundaries**: Clear about what agent should NOT do
- [ ] **Coordination**: Defines how it works with other agents
- [ ] **Evaluation Metrics**: Measurable success criteria defined

### Common Issues to Watch For
- **Too Broad**: Agent tries to do too much (split into multiple agents)
- **Too Narrow**: Agent is too specialized (expand scope or merge with existing)
- **Unclear Boundaries**: Overlap with existing agents (clarify responsibilities)
- **Missing Safety**: No boundaries defined (add safety section)
- **Poor Examples**: Examples are vague or theoretical (add concrete examples)

## After First Approval

### Auto-Updates Enabled
After first deployment, the agent can be automatically updated by the system based on:
- Performance telemetry
- User feedback
- agent-auditor recommendations
- A/B testing results

Updates happen through Phase 5 curation workflow and don't require manual approval.

### Monitoring
agent-auditor tracks all agents monthly:
- Success rates
- Utilization patterns
- Quality ratings
- Capability coverage

## Examples

### Example 1: Financial Analyst

**Gap Detected**: 18 requests for financial analysis with no suitable agent

**Auto-Created Agent**:
```markdown
---
name: financial-analyst
description: Financial analysis, ROI calculation, portfolio evaluation, and investment modeling for data-driven financial decision-making
color: financial-analyst
---

# Financial Analyst Agent

## Purpose
Provide comprehensive financial analysis, evaluate investment opportunities,
calculate ROI, and support data-driven financial decision-making.

## Core Identity
**Primary Responsibilities**:
- Financial statement analysis
- ROI and NPV calculations
- Investment portfolio evaluation
- Financial modeling and forecasting
- Cost-benefit analysis
- Risk assessment

[... rest of template ...]
```

**Review Decision**: **APPROVED** - Fills clear gap, well-defined scope

### Example 2: Research Specialist

**Gap Detected**: 12 requests for technical research with suboptimal routing to general-purpose

**Auto-Created Agent**:
```markdown
---
name: research-specialist
description: Technical research, best practices investigation, and information synthesis for informed decision-making
color: research-specialist
---

# Research Specialist Agent

## Purpose
Conduct thorough technical research, synthesize information from multiple
sources, and provide evidence-based recommendations.

[... rest of template ...]
```

**Review Decision**: **APPROVED** - Research is distinct capability, good examples

### Example 3: UI Designer (Rejected)

**Gap Detected**: 8 requests for UI design

**Auto-Created Agent**: ui-designer

**Review Decision**: **REJECTED** - "Overlaps too much with frontend-developer. Expand frontend-developer responsibilities instead of creating new agent."

**Action Taken**: Refactored frontend-developer to explicitly include UI/UX design guidance.

## Audit Trail

All review decisions are logged to `telemetry/agent_reviews.jsonl`:

```json
{
  "timestamp": "2025-10-16T14:30:00Z",
  "agent_name": "financial-analyst",
  "action": "approved",
  "reasoning": "Agent meets quality standards",
  "reviewer": "human"
}
```

This data feeds into:
- agent-auditor portfolio analysis
- Creation precision metrics (% of created agents that are approved)
- Gap detection accuracy (% of identified gaps that become successful agents)

## Tips

### First-Time Review
When reviewing your first agent:
1. Compare to existing agents in `agents/` directory
2. Check that template sections are complete
3. Verify examples are concrete and useful
4. Ensure safety boundaries are clear
5. Confirm no overlap with existing agents

### Batch Reviews
If multiple agents pending:
1. Review all agents first before approving any
2. Check for overlap between pending agents
3. Consider if agents can be consolidated
4. Approve in order of priority/urgency

### Modifications
Common modifications needed:
- **Narrow Scope**: Remove responsibilities that overlap with existing agents
- **Expand Examples**: Add more concrete input/output examples
- **Clarify Boundaries**: Make safety and coordination clearer
- **Improve Description**: Make purpose more specific

## See Also

- [Agent-Auditor](../agent-auditor.md) - Strategic HR for agent portfolio
- [Agent-Creator](../agent-creator.md) - Meta-agent that creates new agents
- [CLAUDE.md](../../CLAUDE.md) - Capability gap detection rules
- [Automation README](../../automation/README.md) - Notification system
