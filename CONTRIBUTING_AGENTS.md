# Contributing New Agents

This guide explains how to contribute new specialized agents to the claude-oak-agents ecosystem. Agents are AI specialists that handle specific domains (frontend, backend, security, etc.) with deep expertise.

## When to Create a New Agent

### ✅ Create a New Agent When:

**1. Clear Capability Gap**
- No existing agent covers this domain
- 10+ routing failures logged for same domain in 30 days
- Community requests specific capability
- Example: "No agent handles financial analysis" → Create financial-analyst

**2. Distinct, Non-Overlapping Responsibility**
- Unique domain expertise required
- Different from existing agents (>50% non-overlap)
- Clear boundaries with other agents
- Example: "security-auditor focuses on vulnerabilities, dependency-scanner on supply chain"

**3. Sufficient Complexity to Justify**
- Domain requires specialized knowledge
- Not a single-use or trivial task
- Reusable across multiple contexts
- Example: "API versioning strategy" justifies dedicated agent

### ❌ Don't Create New Agent When:

**1. Existing Agent Can Be Extended**
- Current agent's scope can expand
- <20% new capability added
- Example: Don't create "react-specialist" if frontend-developer already handles React

**2. Too Narrow or Specialized**
- Only applies to single use case
- Can be handled by general-purpose agent
- Example: Don't create "csv-parser-agent" for one-off CSV tasks

**3. Overlaps Significantly with Existing Agents**
- >50% overlap with current agent
- Creates confusion about responsibilities
- Example: Don't create "code-quality-agent" if quality-gate already exists

**4. Temporary or Experimental**
- Technology is unstable or experimental
- Might be obsolete in 6 months
- Example: Don't create agent for beta framework

## Before You Start

### Research Phase

1. **Check existing agents**
```bash
ls ~/Projects/claude-oak-agents/agents/
cat ~/Projects/claude-oak-agents/agents/README.md
```

2. **Review archived agents**
```bash
# Check if capability existed previously
ls ~/Projects/claude-oak-agents/agents/archived/
cat ~/Projects/claude-oak-agents/agents/archived/ARCHIVAL_RECORD.md
```

3. **Search routing failures**
```bash
# Check if gap is documented
grep "domain_not_found" ~/Projects/claude-oak-agents/telemetry/routing_failures.jsonl
```

4. **Ask the community**
Post in [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions):
```markdown
**Proposed Agent**: [name]
**Domain**: [domain]
**Problem**: [what gap does this fill?]
**Overlap Check**: [compared with existing agents]
**Use Cases**: [3-5 concrete examples]
```

## Agent Template Structure

All agents MUST follow this exact structure. See existing agents for examples.

### Required Frontmatter
```markdown
---
name: agent-name
description: Brief 1-2 sentence description of agent's purpose and primary focus
color: agent-name
---
```

### Required Sections

#### 1. Agent Name (H1)
```markdown
# Agent Name
```

#### 2. Purpose Statement
```markdown
## Purpose

[2-3 sentences explaining what the agent does and why it exists]
```

#### 3. Core Identity
```markdown
## Core Identity

**Primary Responsibilities**:
- Responsibility 1
- Responsibility 2
- Responsibility 3

**Domain Expertise**:
- Expertise area 1
- Expertise area 2

**Technology Focus**:
- Technology 1
- Technology 2
```

#### 4. Operating Instructions
```markdown
## Operating Instructions

### How This Agent Works

[Paragraph explaining agent's approach and methodology]

### Analysis Process
1. Step 1: [What agent does first]
2. Step 2: [What agent does next]
3. Step 3: [How agent delivers output]

### Response Format
[How agent structures its output]
```

#### 5. Context Awareness
```markdown
## Context Awareness

The agent considers:
- Context factor 1
- Context factor 2
- Context factor 3

**Codebase Integration**:
[How agent integrates with existing code]

**Technology Stack Detection**:
[How agent detects and adapts to tech stack]
```

#### 6. Input/Output Examples
```markdown
## Input/Output Examples

### Example 1: [Scenario Name]
**Input**:
```
[User request]
```

**Output**:
```
[Agent response with concrete examples]
```

### Example 2: [Scenario Name]
**Input**:
```
[User request]
```

**Output**:
```
[Agent response]
```
```

#### 7. Tools and Integrations
```markdown
## Tools and Integrations

**Primary Tools**:
- Tool 1: [usage]
- Tool 2: [usage]

**File Operations**:
- Read: [when and why]
- Write: [when and why]
- Edit: [when and why]

**External Integrations** (if applicable):
- Integration 1
- Integration 2
```

#### 8. Safety and Boundaries
```markdown
## Safety and Boundaries

**This Agent Should**:
- Do 1
- Do 2
- Do 3

**This Agent Should NOT**:
- Don't 1
- Don't 2
- Don't 3

**Escalation Triggers**:
- When to delegate to another agent
- When to ask for human input
```

#### 9. Metrics for Evaluation
```markdown
## Metrics for Evaluation

**Success Criteria**:
- Metric 1: [how to measure]
- Metric 2: [how to measure]

**Quality Indicators**:
- Indicator 1
- Indicator 2

**Common Failure Modes**:
- Failure 1: [how to detect and prevent]
- Failure 2: [how to detect and prevent]
```

#### 10. Coordination Patterns
```markdown
## Coordination Patterns

### Works With
- **Agent 1**: [how they collaborate]
- **Agent 2**: [how they collaborate]

### Typical Workflows
1. **Workflow 1**: agent-1 → this-agent → agent-2
2. **Workflow 2**: [parallel with another agent]

### Handoff Protocols
**Receives from**: [which agents pass work to this one]
**Passes to**: [which agents this one delegates to]
```

## Testing Requirements

Before submitting, your agent MUST pass these tests:

### 1. Template Compliance
```bash
# Run template validator
python scripts/validate_agent_template.py agents/your-agent.md

# Expected output:
# ✓ Frontmatter complete
# ✓ All required sections present
# ✓ Examples provided
# ✓ Safety boundaries defined
# ✓ Coordination patterns documented
```

### 2. Agent Invocation Test
```bash
# Test agent can be invoked
claude-code --agent your-agent-name

# Request:
"[Test request relevant to agent's domain]"

# Verify:
# - Agent responds appropriately
# - Output matches expected format
# - Boundaries respected
```

### 3. Integration Test
```bash
# Test agent in typical workflow
claude-code

# Request:
"[Request that should trigger your agent + others]"

# Verify:
# - Agent invoked at correct point
# - Coordinates with other agents properly
# - No overlap/conflict with existing agents
```

### 4. Edge Case Test
```bash
# Test boundary conditions
claude-code --agent your-agent-name

# Try:
# - Request outside agent's domain (should decline gracefully)
# - Request requiring delegation (should delegate correctly)
# - Request with missing context (should ask for clarification)
```

## Documentation Requirements

### 1. Update Agent Registry
```yaml
# In agents/README.md, add entry:

### [Category]
- **your-agent-name**: [Brief description]
  - Domain: [domain]
  - Tech stack: [stack]
  - Coordinates with: [related agents]
```

### 2. Update CLAUDE.md
```markdown
# In CLAUDE.md, add to agent-responsibility-matrix:

#### [Category]
- **your-agent-name**: [Responsibilities]
```

### 3. Create Agent Documentation
```markdown
# In docs/agents/your-agent-name.md

# Agent Name

## Overview
[Detailed explanation of agent's purpose and capabilities]

## When to Use
[Scenarios where this agent is appropriate]

## Examples
[Comprehensive real-world examples]

## Coordination
[How this agent works with others]

## Troubleshooting
[Common issues and solutions]
```

## Submission Process

### Step 1: Fork and Branch
```bash
git clone https://github.com/robertmnyborg/claude-oak-agents.git
cd claude-oak-agents
git checkout -b agent/your-agent-name
```

### Step 2: Create Agent File
```bash
# Copy template
cp agents/AGENT_TEMPLATE.md agents/your-agent-name.md

# Edit with your content
code agents/your-agent-name.md
```

### Step 3: Test Thoroughly
```bash
# Run all tests from "Testing Requirements" section above
python scripts/validate_agent_template.py agents/your-agent-name.md
# ... manual invocation tests
# ... integration tests
# ... edge case tests
```

### Step 4: Update Documentation
```bash
# Update agent registry
code agents/README.md

# Update CLAUDE.md
code CLAUDE.md

# Create agent docs
mkdir -p docs/agents
code docs/agents/your-agent-name.md
```

### Step 5: Commit and Push
```bash
git add agents/your-agent-name.md \
        agents/README.md \
        CLAUDE.md \
        docs/agents/your-agent-name.md

git commit -m "Add agent: your-agent-name

- Domain: [domain]
- Purpose: [brief purpose]
- Coordinates with: [agents]
- Solves: [gap description]
"

git push origin agent/your-agent-name
```

### Step 6: Create Pull Request
```markdown
## New Agent: Your Agent Name

### Problem Solved
[What capability gap does this fill?]

### Domain
[Primary domain and expertise area]

### Responsibilities
- Responsibility 1
- Responsibility 2
- Responsibility 3

### Overlap Analysis
**Existing Agents Reviewed**:
- agent-1: [Why this is different]
- agent-2: [Why this is different]

**Unique Value**: [What this agent does that others don't]

### Testing Completed
- [ ] Template validation passed
- [ ] Invocation test passed
- [ ] Integration test passed
- [ ] Edge case test passed
- [ ] Documentation updated

### Example Use Cases
1. Use case 1: [description]
2. Use case 2: [description]
3. Use case 3: [description]

### Coordination Patterns
**Works with**: [list of agents this coordinates with]
**Typical workflow**: [agent-1] → [your-agent] → [agent-2]
```

## Review Criteria

Your agent will be reviewed for:

### 1. Need Justification
- [ ] Clear capability gap identified
- [ ] Evidence of need (routing failures, community requests)
- [ ] Not solvable by extending existing agent

### 2. Template Compliance
- [ ] All required sections complete
- [ ] Frontmatter correct
- [ ] Examples concrete and useful
- [ ] Safety boundaries clear

### 3. Quality Standards
- [ ] Professional writing quality
- [ ] Clear, specific responsibilities
- [ ] Practical, actionable guidance
- [ ] Realistic scope

### 4. Integration Quality
- [ ] No overlap with existing agents
- [ ] Coordination patterns defined
- [ ] Handoff protocols clear
- [ ] Boundaries respected

### 5. Testing Completeness
- [ ] Template validation passed
- [ ] Invocation test successful
- [ ] Integration test successful
- [ ] Edge cases handled

### 6. Documentation
- [ ] Agent registry updated
- [ ] CLAUDE.md updated
- [ ] Agent-specific docs created
- [ ] Examples comprehensive

## Quality Standards

### Scope Definition
**Good Scope** (Focused):
```markdown
## Purpose
Perform security audits using OWASP guidelines, focusing on
vulnerability detection, threat modeling, and compliance validation.
```

**Bad Scope** (Too Broad):
```markdown
## Purpose
Handle all security-related tasks including audits, encryption,
compliance, network security, and general security advice.
```

### Responsibility Clarity
**Good Responsibilities**:
```markdown
**Primary Responsibilities**:
- Analyze database schemas for normalization and performance
- Design migration strategies with zero-downtime approaches
- Generate DDL for PostgreSQL, MySQL, MongoDB
- Optimize query performance with indexing strategies
```

**Bad Responsibilities**:
```markdown
**Primary Responsibilities**:
- Work with databases
- Help with backend stuff
- Make things faster
- Write code
```

### Examples Quality
**Good Examples**:
```markdown
### Example 1: Database Schema Design
**Input**:
"Design a PostgreSQL schema for multi-tenant SaaS with user authentication"

**Output**:
```sql
-- Tenants table
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table with tenant isolation
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  email VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  UNIQUE(tenant_id, email)
);

-- Indexes for performance
CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);
```
**Reasoning**: Uses UUID for scalability, enforces tenant isolation,
includes unique constraint per tenant, optimizes with indexes.
```

**Bad Examples**:
```markdown
### Example 1: Database Work
**Input**: "Help with database"
**Output**: "I can help with databases. What do you need?"
```

## After Acceptance

Once your agent is accepted:

1. **Deployed**: Agent available in `agents/` directory
2. **Monitored**: agent-auditor tracks performance monthly
3. **Updated**: You can submit improvements via PR
4. **Credited**: Listed in CONTRIBUTORS.md
5. **Maintained**: Tagged on related issues/PRs

## Recognition

Agent contributors are recognized:
- CONTRIBUTORS.md entry
- Agent metadata (author field)
- Release notes mention
- Community showcases

## Getting Help

### Resources
- **Examples**: Study existing agents in `agents/` directory
- **Template**: Use `agents/AGENT_TEMPLATE.md` as starting point
- **Discussions**: [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)
- **Discord**: [Community Discord](link) for real-time help

### Common Questions

**Q: Can I create multiple related agents?**
A: Only if they have truly distinct responsibilities. Consider one agent with multiple capabilities instead.

**Q: My agent overlaps 30% with existing agent. Is that OK?**
A: Maybe. If the 70% unique value is significant and well-defined, it's justified. Explain overlap in PR.

**Q: Can I reactivate an archived agent?**
A: Yes! See `agents/archived/ARCHIVAL_RECORD.md` for reactivation process.

**Q: How do I know if my agent is too narrow?**
A: If you can only think of 1-2 use cases, it's too narrow. Agents should have 10+ realistic scenarios.

**Q: What if technology evolves and agent becomes obsolete?**
A: Submit PR to archive with reasoning. We'll document it for potential future reactivation.

## Code of Conduct

- Professional and respectful communication
- Constructive feedback only
- Credit original authors
- Welcome newcomers
- Assume good intent

## License

All contributed agents are MIT licensed (same as project). By contributing, you agree to this license.

---

**Ready to contribute an agent?** Review existing agents in `agents/`, verify the gap exists, then follow the submission process above. Welcome to the community!
