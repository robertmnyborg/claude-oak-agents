# Pattern Validation Checklist

This checklist ensures contributed patterns meet quality standards before being accepted into the community repository.

## Reviewer Instructions

Use this checklist when reviewing pattern contributions. Each section must pass before pattern is merged.

## 1. Completeness

### Metadata
- [ ] Pattern name is descriptive and kebab-case
- [ ] Category is valid (authentication, data, api, deployment, frontend, backend)
- [ ] Difficulty level is appropriate (beginner, intermediate, advanced)
- [ ] Tech stack is clearly specified
- [ ] Tags are relevant and helpful
- [ ] Version follows semantic versioning (1.0.0)
- [ ] Status is set (stable, experimental, deprecated)

### Required Sections
- [ ] Problem Statement complete with "When to use" and "When NOT to use"
- [ ] Solution Overview with high-level approach and architecture diagram
- [ ] Technical Design with component breakdown and data flow
- [ ] Security Considerations with OWASP threat analysis (if applicable)
- [ ] Agent Workflow with specific agents and execution sequence
- [ ] Implementation Checklist with actionable steps
- [ ] Validation Criteria with success metrics
- [ ] Examples and Usage with working code snippets
- [ ] Troubleshooting section with common issues

## 2. Clarity

### Writing Quality
- [ ] Clear, professional writing without typos
- [ ] Active voice used throughout
- [ ] Technical terms explained or linked to definitions
- [ ] No unnecessary jargon or buzzwords
- [ ] Consistent terminology (no switching between synonyms)

### Organization
- [ ] Logical flow from problem → solution → implementation
- [ ] Sections have clear headings
- [ ] Related information grouped together
- [ ] Code examples follow prose explanations
- [ ] Diagrams clarify architecture (text/ASCII acceptable)

### Examples
- [ ] At least 2 concrete examples provided
- [ ] Examples use realistic data and scenarios
- [ ] Code snippets are complete (imports, error handling)
- [ ] Examples demonstrate different use cases
- [ ] Expected output/behavior documented

## 3. Reusability

### Generalization
- [ ] Pattern solves common problem (not company-specific)
- [ ] No hard-coded business logic or proprietary systems
- [ ] Framework/language choices justified
- [ ] Alternative approaches mentioned where appropriate
- [ ] Can be applied to multiple projects/contexts

### Flexibility
- [ ] Configuration options documented
- [ ] Different tech stack variations noted
- [ ] Customization points identified
- [ ] Not overly prescriptive where flexibility needed

### Documentation
- [ ] Prerequisites clearly stated
- [ ] Dependencies version-pinned or range-specified
- [ ] Environment requirements documented
- [ ] Setup instructions complete

## 4. Correctness

### Technical Accuracy
- [ ] Code examples tested and working
- [ ] Architecture design is sound
- [ ] Best practices followed
- [ ] No anti-patterns or bad practices
- [ ] References to authoritative sources (RFCs, official docs)

### Security
- [ ] Security section present (if applicable)
- [ ] OWASP Top 10 threats considered
- [ ] Input validation addressed
- [ ] Authentication/authorization covered (if applicable)
- [ ] Secrets management documented (if applicable)
- [ ] Common vulnerabilities prevented

### Performance
- [ ] Performance considerations addressed (if applicable)
- [ ] Scalability discussed where relevant
- [ ] Database indexing mentioned (if applicable)
- [ ] Caching strategies noted (if applicable)

## 5. Practical Value

### Real-World Applicability
- [ ] Pattern based on proven implementation
- [ ] Common pitfalls documented
- [ ] Debugging tips provided
- [ ] Rollback/recovery procedures included (if applicable)
- [ ] Production considerations addressed

### Testing
- [ ] Testing strategy included
- [ ] Test examples provided
- [ ] Success criteria defined
- [ ] Failure modes documented
- [ ] Monitoring/observability mentioned (if applicable)

### Maintainability
- [ ] Code examples are maintainable
- [ ] Complexity justified (KISS principle)
- [ ] Documentation updated with pattern
- [ ] Versioning strategy explained (if applicable)

## 6. Agent Integration

### Agent Workflow
- [ ] Agents clearly identified
- [ ] Execution sequence documented
- [ ] Agent responsibilities defined
- [ ] Handoff points between agents specified
- [ ] Agent coordination makes sense

### Agent Tasks
- [ ] Each agent has clear input and expected output
- [ ] Task breakdown is actionable
- [ ] Dependencies between agent tasks documented
- [ ] Parallel vs sequential execution specified

## 7. Community Standards

### Formatting
- [ ] Markdown formatting correct
- [ ] Code blocks have language specified
- [ ] YAML frontmatter valid
- [ ] Links work and point to valid resources
- [ ] Images (if any) load correctly

### Style Guide Compliance
- [ ] Follows project writing style
- [ ] Consistent with existing patterns
- [ ] Professional tone maintained
- [ ] No marketing language or vendor bias

### Licensing
- [ ] Pattern compatible with MIT license
- [ ] No copyrighted code without attribution
- [ ] External references properly cited
- [ ] Contributors acknowledged

## 8. Final Checks

### Pre-Merge Validation
- [ ] Pattern file in correct directory (`specs/templates/community/`)
- [ ] Filename matches pattern name (kebab-case)
- [ ] No merge conflicts
- [ ] Git commit message follows convention
- [ ] PR description complete with checklist

### Post-Merge Actions
- [ ] Add pattern to INDEX.md
- [ ] Update community patterns README
- [ ] Add contributor to CONTRIBUTORS.md
- [ ] Tag PR with appropriate labels
- [ ] Close related issues (if applicable)

## Review Outcomes

### Accept
- [ ] All checklist items pass
- [ ] Merge to `main`
- [ ] Notify contributor of acceptance
- [ ] Add to featured patterns (if exceptional)

### Request Changes
- [ ] Provide specific feedback on failing items
- [ ] Request updates to pattern
- [ ] Re-review after changes submitted

### Reject
- [ ] Pattern duplicates existing pattern significantly
- [ ] Pattern too specific/not reusable
- [ ] Quality below minimum standards
- [ ] Security concerns cannot be resolved
- [ ] Provide reasoning to contributor
- [ ] Suggest alternatives or improvements

## Scoring Guide

### Priority Levels

**CRITICAL** (Must fix before merge):
- Missing required sections
- Security vulnerabilities in examples
- Technically incorrect information
- Untested/broken code examples
- Missing agent workflow

**HIGH** (Should fix before merge):
- Unclear writing or organization
- Incomplete examples
- Missing troubleshooting section
- Poor reusability (too specific)
- Inadequate security considerations

**MEDIUM** (Good to fix but not blocking):
- Minor typos or formatting issues
- Could use more examples
- Additional clarification helpful
- Better diagrams would help

**LOW** (Nice to have):
- Additional references
- More comprehensive examples
- Alternative tech stack variations

## Template for Review Comments

```markdown
## Pattern Review: [Pattern Name]

### Summary
[Brief 2-3 sentence summary of pattern and overall assessment]

### Completeness: [PASS / NEEDS WORK]
- [Specific feedback]

### Clarity: [PASS / NEEDS WORK]
- [Specific feedback]

### Reusability: [PASS / NEEDS WORK]
- [Specific feedback]

### Correctness: [PASS / NEEDS WORK]
- [Specific feedback]

### Practical Value: [PASS / NEEDS WORK]
- [Specific feedback]

### Agent Integration: [PASS / NEEDS WORK]
- [Specific feedback]

### Recommendation: [ACCEPT / REQUEST CHANGES / REJECT]

**If Request Changes**:
Priority issues to address:
1. [Issue 1 with section reference]
2. [Issue 2 with section reference]
3. [Issue 3 with section reference]

**If Reject**:
Reasons for rejection:
1. [Reason 1]
2. [Reason 2]

Suggestions for improvement: [...]
```

## Reviewer Best Practices

1. **Be Constructive**: Provide specific, actionable feedback
2. **Be Timely**: Review within 1 week of submission
3. **Be Thorough**: Check all sections, test code examples
4. **Be Fair**: Apply standards consistently across all patterns
5. **Be Encouraging**: Recognize good work, welcome new contributors

## Questions or Issues?

- Check [CONTRIBUTING_PATTERNS.md](CONTRIBUTING_PATTERNS.md) for pattern guidelines
- Review existing accepted patterns in `specs/templates/community/`
- Ask in [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)
- Tag @maintainers in PR comments for clarification

---

**Checklist Version**: 1.0.0  
**Last Updated**: 2025-11-08
