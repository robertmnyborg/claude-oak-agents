# Community Agents

This directory contains community-contributed agents that extend the core claude-oak-agents system with specialized capabilities.

## What Are Community Agents?

Community agents are domain-specific AI specialists created by the community to fill capability gaps. They follow the same template and quality standards as core agents but are maintained by community contributors.

## Difference from Core Agents

| Aspect | Core Agents | Community Agents |
|--------|-------------|------------------|
| Location | `/agents/` | `/agents/community/` |
| Maintenance | Core maintainers | Original contributor + community |
| Review Process | Core team approval | Community review + maintainer approval |
| Stability | Production-ready, highly stable | Varies (see status field) |
| Usage | Automatically available | May require opt-in flag |

## Current Community Agents

**Status**: No community agents yet. Be the first contributor!

Check back soon or [submit your own agent](../../CONTRIBUTING_AGENTS.md).

## How to Use Community Agents

### Option 1: Enable All Community Agents
```bash
# Add to your environment
export OAK_ENABLE_COMMUNITY_AGENTS=true

# Or in your .env file
OAK_ENABLE_COMMUNITY_AGENTS=true
```

### Option 2: Enable Specific Agents
```bash
# Enable only specific community agents
export OAK_ENABLED_AGENTS="financial-analyst,research-specialist"
```

### Option 3: Try Experimental Agents
```bash
# Include experimental/beta agents
export OAK_ENABLE_EXPERIMENTAL=true
```

## Agent Status Levels

Community agents are marked with status indicators:

- **stable** - Production-ready, well-tested, recommended for general use
- **beta** - Functional but may have rough edges, use with caution
- **experimental** - Early-stage development, breaking changes possible
- **deprecated** - No longer maintained, migration path provided

## Contributing Your Agent

Interested in contributing an agent? Follow these steps:

### 1. Verify Need
- Check [core agents](../README.md) for existing coverage
- Review [capability gaps](../../telemetry/routing_failures.jsonl)
- Discuss in [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)

### 2. Read Guidelines
- [CONTRIBUTING_AGENTS.md](../../CONTRIBUTING_AGENTS.md) - Complete agent contribution guide
- [Agent template](../AGENT_TEMPLATE.md) - Required structure
- [Review checklist](../../PATTERN_VALIDATION_CHECKLIST.md) - Quality criteria

### 3. Create Agent
```bash
# Fork repository
git clone https://github.com/your-username/claude-oak-agents.git
cd claude-oak-agents

# Create branch
git checkout -b agent/your-agent-name

# Copy template
cp agents/AGENT_TEMPLATE.md agents/community/your-agent-name.md

# Edit agent file
code agents/community/your-agent-name.md
```

### 4. Test Thoroughly
```bash
# Template validation
python scripts/validate_agent_template.py agents/community/your-agent-name.md

# Manual testing
claude-code --agent your-agent-name
# ... test with various requests
```

### 5. Submit Pull Request
```bash
git add agents/community/your-agent-name.md
git commit -m "Add community agent: your-agent-name"
git push origin agent/your-agent-name
```

Create PR on GitHub with description following template in CONTRIBUTING_AGENTS.md.

## Quality Standards

All community agents must meet these minimum standards:

### Template Compliance
- [ ] All required sections complete
- [ ] Frontmatter YAML valid
- [ ] Examples concrete and working
- [ ] Safety boundaries defined
- [ ] Coordination patterns documented

### Testing
- [ ] Template validator passes
- [ ] Agent responds appropriately to domain requests
- [ ] Integrates correctly with other agents
- [ ] Edge cases handled gracefully

### Documentation
- [ ] Purpose clearly stated
- [ ] When to use / when NOT to use
- [ ] Input/output examples realistic
- [ ] Troubleshooting section included

### Code Quality
- [ ] No placeholder or TODO comments
- [ ] Consistent terminology
- [ ] Professional writing quality
- [ ] No typos or grammatical errors

## Review Process

1. **Automated Checks** (< 5 minutes)
   - Template validation
   - Markdown linting
   - YAML frontmatter parsing
   - Link checking

2. **Community Review** (1-2 weeks)
   - Other contributors review and comment
   - Maintainers provide feedback
   - Author addresses feedback

3. **Final Approval** (< 1 week)
   - Core maintainer approval required
   - Merge to `main`
   - Agent available in `agents/community/`

4. **Post-Merge**
   - Added to agent registry
   - Listed in this README
   - Contributor credited in CONTRIBUTORS.md
   - Announced in release notes

## Maintenance

### Agent Lifecycle

**Active Maintenance**:
- Original contributor maintains agent
- Community can submit improvement PRs
- Bug fixes and updates welcome

**Seeking Maintainer**:
- Original contributor no longer active
- Agent still valuable and used
- Community invited to adopt maintainership

**Deprecated**:
- Agent no longer needed or superseded
- Moved to `agents/archived/community/`
- Documentation preserved for reference

### How to Maintain

If you contributed an agent, you'll be tagged on:
- Issues related to your agent
- PRs proposing changes to your agent
- Questions about agent usage

You're encouraged to:
- Respond to issues and questions
- Review PRs affecting your agent
- Update agent as technology evolves
- Publish new versions when needed

## Recognition

Community contributors are recognized:

- **CONTRIBUTORS.md**: Listed with contributed agents
- **Agent Metadata**: Author field in frontmatter
- **Release Notes**: Mentioned when agent is featured
- **Community Showcase**: Highlighted agents featured in docs
- **GitHub Profile**: Contributions visible on your profile

## Examples of Future Community Agents

These are potential agents the community might create:

**Financial Analysis**:
- ROI calculations
- Financial modeling
- Investment evaluation
- Budget forecasting

**Research & Investigation**:
- Technical research
- Best practices investigation
- Competitive analysis
- Technology evaluation

**Data Science**:
- Statistical analysis
- Data visualization recommendations
- ML model evaluation
- A/B test analysis

**DevOps Automation**:
- CI/CD pipeline optimization
- Infrastructure monitoring setup
- Log analysis and alerting
- Incident response coordination

**Content & Marketing**:
- SEO optimization
- Content strategy
- Social media planning
- Email campaign structure

## Getting Help

### Resources
- **Contributing Guide**: [CONTRIBUTING_AGENTS.md](../../CONTRIBUTING_AGENTS.md)
- **Template**: [agents/AGENT_TEMPLATE.md](../AGENT_TEMPLATE.md)
- **Examples**: Study core agents in `/agents/` directory
- **Discussions**: [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)

### Common Questions

**Q: Can I submit multiple agents?**
A: Yes! Just ensure each agent has distinct, non-overlapping responsibilities.

**Q: What if my agent overlaps with a core agent?**
A: Consider expanding the core agent instead. Discuss with maintainers first.

**Q: How long does review take?**
A: Usually 1-2 weeks. Complex agents may take longer.

**Q: Can I update someone else's community agent?**
A: Yes! Submit a PR with improvements. Original author will be credited.

**Q: What if technology changes and my agent becomes obsolete?**
A: Submit PR to mark as deprecated and recommend alternative.

## Statistics

**Total Community Agents**: 0  
**Stable Agents**: 0  
**Beta Agents**: 0  
**Experimental Agents**: 0  
**Community Contributors**: 0  

Last updated: 2025-11-08

---

**Ready to contribute?** Read [CONTRIBUTING_AGENTS.md](../../CONTRIBUTING_AGENTS.md) and create your first agent!

**Questions?** Ask in [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions).
