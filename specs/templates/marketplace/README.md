# Template Marketplace

A curated collection of reusable templates for specs, agents, and workflows. Browse, search, and deploy battle-tested patterns for common development scenarios.

## Quick Start

```bash
# Browse all templates
./scripts/oak-templates list

# Search templates
./scripts/oak-templates search oauth

# View template details
./scripts/oak-templates show saas-auth-complete

# Use a template
./scripts/oak-templates use saas-auth-complete my-auth-spec
```

## Categories

### Authentication
Complete authentication systems ready to deploy:
- OAuth2 integration patterns
- JWT token management
- Social login flows
- Multi-factor authentication
- Session management

### Data
Data management and migration templates:
- Zero-downtime migrations
- ETL pipelines
- Schema versioning
- Data validation
- Backup strategies

### API
API design and implementation patterns:
- REST CRUD operations
- GraphQL servers
- API versioning strategies
- Rate limiting
- Documentation generation

### Frontend
UI component and feature templates:
- Dashboard layouts
- Form builders with validation
- Component libraries
- State management patterns
- Responsive designs

### Infrastructure
Deployment and infrastructure as code:
- AWS CDK stacks
- Docker compositions
- CI/CD pipelines
- Serverless architectures
- Monitoring setups

### Patterns
Software architecture patterns:
- Microservices
- Event-driven architectures
- CQRS and Event Sourcing
- Service mesh patterns
- Clean architecture

### Security
Security implementation templates:
- Security audit checklists
- Penetration test specs
- Compliance frameworks
- Vulnerability scanning
- Security headers

### Workflows
Complete development workflows:
- Feature development flows
- Bug fix processes
- Release management
- Code review automation
- Documentation generation

## Template Difficulty Levels

- **Beginner**: Basic implementation, minimal dependencies, 1-2 hours
- **Intermediate**: Standard implementation, common dependencies, 4-6 hours
- **Advanced**: Complex implementation, multiple integrations, 8+ hours
- **Expert**: Cutting-edge patterns, extensive customization, 16+ hours

## Using Templates

### 1. Browse Available Templates

```bash
./scripts/oak-templates list --category authentication
```

### 2. View Template Details

```bash
./scripts/oak-templates show saas-auth-complete
```

This displays:
- Template metadata (difficulty, time estimate, tags)
- Overview and use cases
- Requirements and prerequisites
- Implementation outline
- Agent workflow preview

### 3. Deploy Template

```bash
./scripts/oak-templates use saas-auth-complete my-auth-implementation
```

This copies the template to `specs/active/my-auth-implementation.md` ready for customization.

### 4. Customize for Your Needs

Edit the deployed template:
- Update project-specific details
- Adjust technology stack
- Modify scope as needed
- Add custom requirements

### 5. Execute with Agents

```bash
./scripts/oak-run --spec specs/active/my-auth-implementation.md
```

## Contributing Templates

### Template Requirements

All templates must include:

1. **Complete YAML Frontmatter**
   - template_id, name, category
   - difficulty and estimated_time
   - tags, author, version
   - popularity and last_updated

2. **Comprehensive Content**
   - Overview and use cases
   - Clear requirements
   - Step-by-step implementation
   - Agent workflow
   - Testing strategy
   - Common pitfalls section

3. **Quality Standards**
   - Tested and validated
   - Complete examples
   - Accurate time estimates
   - Proper formatting
   - Valid agent references

### Submission Process

1. Create template in appropriate category folder
2. Validate using `./scripts/oak-templates validate your-template.md`
3. Test deployment and execution
4. Submit PR with template and test results
5. Community review and feedback
6. Merge upon approval

### Template Schema

```yaml
---
template_id: unique-kebab-case-id
template_name: Display Name
category: authentication|data|api|frontend|infrastructure|patterns|security|workflows
difficulty: beginner|intermediate|advanced|expert
estimated_time: X-Y hours
tags: [tag1, tag2, tag3]
author: username or claude-oak-agents
version: 1.0.0
last_updated: YYYY-MM-DD
popularity: 0-100
dependencies: [list of required tools/services]
related_templates: [template_ids]
---
```

## Rating System

Templates are rated based on:

- **Popularity**: Usage count and deployment frequency
- **Quality**: Community ratings (1-5 stars)
- **Completeness**: Automated validation score
- **Success Rate**: Successful executions vs. total attempts
- **Maintenance**: Frequency of updates and bug fixes

### Rate a Template

```bash
./scripts/oak-templates rate saas-auth-complete 5 "Excellent template, worked perfectly!"
```

Ratings are stored in telemetry and aggregated for popularity scores.

## Template Best Practices

### For Template Users

1. **Read Completely First**: Understand the full scope before starting
2. **Check Prerequisites**: Ensure all dependencies are available
3. **Customize Early**: Adapt the template before execution
4. **Follow the Workflow**: Trust the agent sequencing
5. **Document Changes**: Track customizations for future reference

### For Template Authors

1. **Be Specific**: Provide concrete examples and code snippets
2. **Test Thoroughly**: Validate template with multiple scenarios
3. **Estimate Accurately**: Time estimates should include testing
4. **Document Pitfalls**: Share common mistakes and solutions
5. **Keep Updated**: Refresh templates as technologies evolve

## Advanced Features

### Composite Templates

Combine multiple templates:

```bash
./scripts/oak-templates compose \
  --base saas-auth-complete \
  --add api-rest-crud \
  --add cdk-serverless-api \
  --output complete-saas-backend
```

### Template Customization

Generate customized templates with variables:

```bash
./scripts/oak-templates customize saas-auth-complete \
  --var database=mongodb \
  --var frontend=vue \
  --output custom-auth-spec
```

### Template Collections

Bundle related templates:

```bash
./scripts/oak-templates collection create "full-stack-saas" \
  saas-auth-complete \
  api-rest-crud \
  react-feature-complete \
  cdk-serverless-api
```

## Maintenance

### Update Notifications

Templates are checked for updates:

```bash
./scripts/oak-templates check-updates
```

Shows available updates for templates you've used.

### Template Versioning

Templates follow semantic versioning:
- **Major (1.0.0)**: Breaking changes, different architecture
- **Minor (0.1.0)**: New features, backward compatible
- **Patch (0.0.1)**: Bug fixes, documentation updates

## Support

- **Issues**: Report template problems via GitHub issues
- **Discussions**: Share experiences and ask questions
- **Contributions**: Submit improvements via pull requests
- **Community**: Join discussions on best practices

## License

All templates are provided under the same license as claude-oak-agents.
