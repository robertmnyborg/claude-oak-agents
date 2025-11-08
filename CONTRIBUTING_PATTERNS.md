# Contributing Workflow Patterns

Welcome to the claude-oak-agents community! This guide will help you contribute high-quality workflow patterns that help other users solve common development challenges.

## What Are Workflow Patterns?

Workflow patterns are reusable templates that combine:
- **Problem specification** - What challenge does this solve?
- **Technical design** - How should it be implemented?
- **Agent coordination** - Which agents handle which parts?
- **Implementation checklist** - Step-by-step execution guide

Think of patterns as "recipes" for common development tasks that the AI agent system can execute consistently.

## What Makes a Good Pattern?

### ✅ Good Patterns Are:

**1. Focused and Specific**
- Solves ONE well-defined problem
- Clear boundaries and scope
- Specific technology stack or approach
- Example: "OAuth2 authentication for SaaS apps" NOT "user management"

**2. Reusable Across Projects**
- Not tied to specific business logic
- Applies to multiple use cases
- Framework/language agnostic where possible
- Example: "Zero-downtime database migrations" works for any DB

**3. Complete and Actionable**
- All information needed to execute
- No assumptions about missing context
- Clear success criteria
- Example: Includes security considerations, rollback procedures, testing approach

**4. Practical and Proven**
- Based on real-world usage
- Battle-tested approach
- Common pitfalls documented
- Example: "We tried X, it failed because Y, use Z instead"

### ❌ Avoid These:

- **Too Generic**: "Build a web app" (what kind? what stack? what features?)
- **Too Specific**: "Add login button to CompanyX dashboard" (not reusable)
- **Incomplete**: Missing security considerations, testing, or rollback procedures
- **Theoretical**: Untested approaches or speculative solutions
- **Outdated**: Using deprecated libraries or obsolete patterns

## Pattern Template Structure

Every pattern must follow this structure (see `specs/templates/community/` for examples):

### Required Sections:

#### 1. Pattern Metadata
```yaml
pattern_name: "descriptive-kebab-case-name"
category: "authentication | data | api | deployment | frontend | backend"
difficulty: "beginner | intermediate | advanced"
tech_stack: ["Node.js", "PostgreSQL", "React", "etc"]
tags: ["oauth2", "jwt", "security", "etc"]
version: "1.0.0"
status: "stable | experimental | deprecated"
```

#### 2. Problem Statement
- What challenge does this solve?
- When should you use this pattern?
- What are the prerequisites?

#### 3. Solution Overview
- High-level approach
- Key design decisions
- Why this approach over alternatives?

#### 4. Technical Design
- Architecture diagram (text/ASCII art acceptable)
- Component breakdown
- Data flow
- Security considerations

#### 5. Agent Workflow
- Which agents execute which tasks?
- Sequential vs parallel execution
- Dependencies between agents
- Expected agent outputs

#### 6. Implementation Checklist
- [ ] Step-by-step tasks
- [ ] Configuration requirements
- [ ] Testing procedures
- [ ] Deployment steps

#### 7. Validation Criteria
- How to verify it works?
- Success metrics
- Common failure modes

#### 8. Examples and Usage
- Code snippets
- Configuration examples
- Real-world use cases

## Submission Process

### Step 1: Identify the Pattern

Before creating a pattern, verify:
- [ ] Does this solve a common, recurring problem?
- [ ] Can it be generalized beyond your specific use case?
- [ ] Is there existing documentation or prior art?
- [ ] Have you successfully implemented this approach?

### Step 2: Create the Pattern File

1. **Fork the repository**
```bash
git clone https://github.com/robertmnyborg/claude-oak-agents.git
cd claude-oak-agents
git checkout -b pattern/your-pattern-name
```

2. **Create pattern file**
```bash
# Use the template
cp specs/templates/community/PATTERN_TEMPLATE.md \
   specs/templates/community/your-pattern-name.md
```

3. **Fill in all sections**
- Don't skip sections - mark "N/A" if truly not applicable
- Include concrete examples
- Add diagrams where helpful (ASCII art is fine)
- Document security considerations thoroughly

### Step 3: Self-Review Checklist

Before submitting, verify:

**Completeness**:
- [ ] All required sections filled in
- [ ] Metadata complete and accurate
- [ ] Agent workflow clearly defined
- [ ] Implementation checklist actionable

**Quality**:
- [ ] Clear, professional writing
- [ ] No typos or grammatical errors
- [ ] Code examples tested and working
- [ ] Security considerations addressed

**Reusability**:
- [ ] Not tied to specific business logic
- [ ] Framework/stack clearly documented
- [ ] Applies to multiple use cases
- [ ] Alternatives mentioned where relevant

**Practical Value**:
- [ ] Based on real implementation
- [ ] Common pitfalls documented
- [ ] Testing approach included
- [ ] Rollback/recovery procedures documented

### Step 4: Test with Agents

Before submitting, test your pattern with the agent system:

```bash
# Example: Test OAuth2 authentication pattern
claude-code --agent spec-manager

# Request:
"Use the saas-auth-pattern to implement OAuth2 authentication"

# Verify:
- spec-manager can read and understand pattern
- Agents are invoked as specified
- Implementation matches pattern design
- Validation criteria can be checked
```

### Step 5: Submit Pull Request

1. **Commit your pattern**
```bash
git add specs/templates/community/your-pattern-name.md
git commit -m "Add pattern: Your Pattern Name

- Solves: [brief problem description]
- Category: [category]
- Tech stack: [stack]
"
```

2. **Push and create PR**
```bash
git push origin pattern/your-pattern-name
```

3. **Create PR with description**
```markdown
## Pattern: Your Pattern Name

### Problem Solved
[Brief description of what this pattern solves]

### Category
[authentication | data | api | deployment | frontend | backend]

### Tech Stack
- Technology 1
- Technology 2

### Why This Pattern?
[Why is this valuable to the community?]

### Testing
- [ ] Tested with spec-manager
- [ ] Agents invoked correctly
- [ ] Implementation validated
- [ ] Examples work as documented

### Checklist
- [ ] All required sections complete
- [ ] Self-review checklist passed
- [ ] Agent workflow tested
- [ ] Security considerations documented
```

## Review Criteria

Patterns are reviewed for:

### 1. Correctness
- Technical accuracy
- Best practices followed
- Security considerations appropriate
- No deprecated or anti-pattern approaches

### 2. Clarity
- Easy to understand
- Well-organized
- Good examples
- Clear agent workflow

### 3. Completeness
- All required sections filled
- No missing critical information
- Testing approach included
- Rollback procedures documented

### 4. Reusability
- General enough to apply broadly
- Not tied to specific business logic
- Tech stack clearly documented
- Alternatives mentioned

### 5. Community Value
- Solves common problem
- High quality implementation
- Well-documented pitfalls
- Practical and actionable

## Quality Standards

### Writing Style
- **Clear and concise**: No unnecessary jargon
- **Active voice**: "Configure the database" not "The database should be configured"
- **Specific**: "Use bcrypt with 12 rounds" not "Use secure hashing"
- **Practical**: Include real examples, not theoretical scenarios

### Code Examples
- **Working code**: Test all examples before submitting
- **Modern syntax**: Use current language/framework versions
- **Commented**: Explain non-obvious parts
- **Complete**: Include imports, configuration, error handling

### Security
- **Mandatory section**: Every pattern must address security
- **Specific threats**: Identify relevant OWASP risks
- **Mitigation strategies**: How to prevent/detect/respond
- **Compliance considerations**: GDPR, SOC2, etc. where applicable

### Testing
- **Test strategy included**: Unit, integration, E2E as appropriate
- **Success criteria**: How to verify it works
- **Failure modes**: Common ways it can break
- **Debugging tips**: How to troubleshoot issues

## Examples of Accepted Patterns

### Example 1: OAuth2 Authentication Pattern
**Why Accepted**:
- Solves common, well-defined problem
- Complete security considerations
- Clear agent workflow (backend-architect → security-auditor → frontend-developer)
- Practical examples with modern libraries
- Rollback and recovery procedures documented

### Example 2: Zero-Downtime Database Migration
**Why Accepted**:
- Critical production concern
- Step-by-step rollback procedures
- Multiple database engines covered
- Agent coordination well-defined (backend-architect → qa-specialist)
- Real-world pitfalls documented

### Example 3: API Versioning Strategy
**Why Accepted**:
- Common API design challenge
- Multiple approaches with tradeoffs
- Clear decision framework
- Agent workflow for implementation
- Breaking vs non-breaking change guidelines

## Examples of Rejected Patterns

### Example 1: "Build a SaaS Application"
**Why Rejected**: Too broad, not a pattern - more like a book outline

### Example 2: "Add User Login to CompanyX"
**Why Rejected**: Too specific to one company, not reusable

### Example 3: "Use Library X for Everything"
**Why Rejected**: Not a pattern, just a library recommendation without context

### Example 4: "REST API Best Practices"
**Why Rejected**: Too generic without specific implementation guidance

## Pattern Versioning

Patterns evolve. Use semantic versioning:

- **Major (2.0.0)**: Breaking changes, incompatible with previous version
- **Minor (1.1.0)**: New features, backward compatible
- **Patch (1.0.1)**: Bug fixes, corrections, clarifications

### When to Version

**Create new version when**:
- Security vulnerability discovered
- Better approach emerges
- Technology stack updated (e.g., React 18 → 19)
- Community feedback suggests improvements

**How to version**:
1. Keep old version with `deprecated` status
2. Create new file: `pattern-name-v2.md`
3. Update metadata with new version number
4. Document what changed and why

## Getting Help

### Community Resources
- **Discussions**: [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)
- **Examples**: See `specs/templates/community/` for pattern examples
- **Discord**: [Community Discord](link) for real-time help

### Common Questions

**Q: Can I submit multiple related patterns?**
A: Yes! Submit as separate patterns with cross-references. Example: "OAuth2 Pattern" and "JWT Token Management Pattern" can reference each other.

**Q: What if my pattern uses proprietary technology?**
A: That's fine if it's widely available (e.g., AWS services). Document alternatives where possible.

**Q: Can I update someone else's pattern?**
A: Yes! Submit a PR with improvements. Original author will be credited, you'll be added as contributor.

**Q: What if my pattern is similar to an existing one?**
A: If it solves a meaningfully different problem or uses a different approach, it's valuable. Reference the existing pattern and explain differences.

**Q: How long does review take?**
A: Usually 1-2 weeks. Complex patterns may take longer. We'll provide feedback if changes needed.

## Pattern Categories

Organize patterns by primary category:

### Authentication & Authorization
- OAuth2, JWT, SAML, session management, RBAC, etc.

### Data & Storage
- Database design, migrations, caching, backups, data integrity

### API Design
- REST, GraphQL, versioning, pagination, rate limiting

### Deployment & Infrastructure
- CI/CD, containerization, cloud deployment, monitoring

### Frontend Patterns
- State management, component architecture, routing, forms

### Backend Patterns
- Service architecture, background jobs, message queues, webhooks

### Testing & Quality
- Test strategies, mocking, E2E testing, performance testing

### Security
- Input validation, encryption, secrets management, compliance

## After Acceptance

Once your pattern is accepted:

1. **Merged to main**: Pattern available in `specs/templates/community/`
2. **Credited**: You're added to CONTRIBUTORS.md
3. **Featured**: May be featured in documentation or examples
4. **Maintained**: You're tagged on issues/PRs related to your pattern
5. **Updated**: You can submit updates as technology evolves

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Pattern metadata (author field)
- Release notes when pattern is featured
- Community showcases

## Code of Conduct

- Be respectful and professional
- Provide constructive feedback
- Give credit where due
- Welcome newcomers
- Assume good intent

## License

All contributed patterns are MIT licensed (same as project). By contributing, you agree to this license.

---

**Ready to contribute?** Start by exploring existing patterns in `specs/templates/community/`, then follow the submission process above. Welcome to the community!
