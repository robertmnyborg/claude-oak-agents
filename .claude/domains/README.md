# Domain-Specific Configuration System

## Overview

The claude-oak-agents system uses **domain-specific configurations** to enable specialized, context-aware agent routing. Instead of a one-size-fits-all approach, the system automatically detects the relevant domain(s) for each request and activates specialized agents with domain expertise.

## What Are Domains?

Domains represent distinct technical areas with their own:
- **Tech stacks**: Specific frameworks, libraries, and tools
- **Patterns**: Best practices and conventions
- **Workflows**: Agent coordination patterns
- **Quality standards**: Domain-specific requirements
- **Specialized agents**: Experts in that domain

## Available Domains

| Domain | Description | Primary Agent | Tech Stack |
|--------|-------------|---------------|------------|
| **Frontend** | UI/UX development, modern frameworks | frontend-developer | React, Vue, TypeScript, Tailwind |
| **Backend** | APIs, services, business logic | infrastructure-specialist | Node.js, Express, MongoDB, PostgreSQL |
| **Infrastructure** | Cloud resources, deployment, DevOps | infrastructure-specialist | AWS CDK, Docker, Lambda, ECS |
| **Security** | Security audits, vulnerability fixes | security-auditor | OWASP, IAM, encryption, Snyk |
| **Data** | Databases, ETL, data pipelines | infrastructure-specialist | PostgreSQL, MongoDB, dbt, Airflow |

## How Domain Detection Works

### 1. Automatic Detection

The domain router (`core/domain_router.py`) analyzes:

- **Keywords**: Terms in the user's request
  - Example: "React component" → Frontend domain
  - Example: "SQL injection" → Security domain

- **File Paths**: Files being worked on
  - Example: `src/components/Button.tsx` → Frontend domain
  - Example: `serverless.yml` → Infrastructure domain

- **Tech Stack Mentions**: Technologies referenced
  - Example: "CDK" → Infrastructure domain
  - Example: "MongoDB migration" → Data domain

### 2. Confidence Scoring

Each domain match receives a confidence score (0.0 - 1.0):

- **Keyword matches**: 40% weight
- **File pattern matches**: 40% weight
- **Tech stack mentions**: 20% weight

Multiple domains can match a single request (e.g., "Deploy React app to AWS" → Frontend + Infrastructure).

### 3. Agent Recommendation

Based on detected domains, the system recommends:
- **Primary agents**: Domain experts
- **Secondary agents**: Supporting specialists
- **Related agents**: Coordination and quality agents

## Domain Configuration Structure

Each domain configuration (`.claude/domains/<domain>.md`) contains:

### YAML Frontmatter
```yaml
---
domain: frontend
priority: 1
primary_agent: frontend-developer
secondary_agents: [qa-specialist, git-workflow-manager]
related_agents: [spec-manager, systems-architect]
---
```

### Markdown Sections

1. **Tech Stack**: Technologies, frameworks, libraries
2. **Patterns & Conventions**: Best practices, code organization
3. **Agent Workflows**: Common task workflows
4. **Triggers**: Keywords, file patterns, tech stack mentions
5. **Quality Standards**: Testing, performance, security requirements
6. **Common Tasks**: Step-by-step guides
7. **Example Scenarios**: Real-world workflow examples

## Using Domain Configurations

### As a User

**The system automatically detects domains** - you don't need to specify them.

Just describe what you want:
- "Create a button component" → Frontend domain detected
- "Add JWT authentication" → Security + Backend domains detected
- "Deploy to AWS with CDK" → Infrastructure domain detected

### As a Developer

#### Command-Line Usage

```bash
# Test domain detection
python core/domain_router.py

# Example output:
# Detected Domains:
# 1. FRONTEND (confidence: 0.80)
#    Primary agent: frontend-developer
#    Reasons: 3 keyword(s) matched, 1 file pattern(s) matched
```

#### Programmatic Usage

```python
from core.domain_router import DomainRouter

router = DomainRouter()

# Identify domains
domains = router.identify_domains(
    request_text="Create a React component with TypeScript",
    file_paths=["src/components/Button.tsx"]
)

# Get recommended agents
agents = router.get_recommended_agents(
    request_text="Create a React component with TypeScript",
    file_paths=["src/components/Button.tsx"]
)

# agents = ['frontend-developer', 'qa-specialist', 'git-workflow-manager', ...]
```

## Domain-Specific Workflows

### Frontend Domain

**Request**: "Create a form component with validation"

**Detected**: Frontend domain (confidence: 0.85)

**Workflow**:
```
frontend-developer → qa-specialist → git-workflow-manager
```

**Details**:
- Use React Hook Form or Formik
- TypeScript type definitions
- Input validation (Zod/Yup)
- Unit tests with React Testing Library
- Accessibility (ARIA labels)

---

### Backend Domain

**Request**: "Create API endpoint for user registration"

**Detected**: Backend + Security domains

**Workflow**:
```
spec-manager → infrastructure-specialist → security-auditor → qa-specialist → git-workflow-manager
```

**Details**:
- Express route handler
- Input validation (Joi/Zod)
- Password hashing (bcrypt)
- JWT token generation
- MongoDB/PostgreSQL integration
- Unit and integration tests

---

### Infrastructure Domain

**Request**: "Deploy Lambda function with API Gateway"

**Detected**: Infrastructure domain (confidence: 0.90)

**Workflow**:
```
infrastructure-specialist → security-auditor → git-workflow-manager
```

**Details**:
- Serverless Framework or CDK
- IAM role with least-privilege
- Environment variables from Secrets Manager
- CloudWatch logging
- Deployment via CI/CD

---

### Security Domain

**Request**: "Fix SQL injection vulnerability"

**Detected**: Security + Backend domains

**Workflow**:
```
security-auditor → infrastructure-specialist → qa-specialist → git-workflow-manager
```

**Details**:
- Identify vulnerable code
- Use parameterized queries or ORM
- Input validation and sanitization
- Security testing (manual + automated)
- Document fix and prevention strategy

---

### Data Domain

**Request**: "Add index to improve query performance"

**Detected**: Data + Backend domains

**Workflow**:
```
debug-specialist → infrastructure-specialist → qa-specialist → git-workflow-manager
```

**Details**:
- EXPLAIN ANALYZE to identify slow queries
- Create database migration
- Add index (PostgreSQL, MongoDB)
- Test on staging
- Monitor performance improvement

## Priority Rules

When **multiple domains** match a request:

1. **Highest confidence domain** determines primary workflow
2. **Combined agent pool** includes agents from all matched domains
3. **Security domain** always participates (if any security keywords detected)

Example:
- Request: "Deploy React app to S3 with CloudFront"
- Domains: Frontend (0.60) + Infrastructure (0.85)
- **Primary workflow**: Infrastructure (higher confidence)
- **Agents**: infrastructure-specialist, security-auditor, frontend-developer, qa-specialist

## Adding Custom Domains

### 1. Create Domain Configuration

Create `.claude/domains/<domain-name>.md`:

```markdown
---
domain: mobile
priority: 1
primary_agent: mobile-developer
secondary_agents: [qa-specialist, git-workflow-manager]
related_agents: [systems-architect]
---

# Domain: Mobile Development

## Tech Stack
- **iOS**: Swift, SwiftUI, UIKit
- **Android**: Kotlin, Jetpack Compose
- **Cross-platform**: React Native, Flutter

## Patterns & Conventions
...

## Triggers

### Keywords
- iOS, Android, mobile, app, Swift, Kotlin, React Native

### File Patterns
- `*.swift`, `*.kt`, `*.dart`
- `ios/**/*`, `android/**/*`

### Tech Stack Mentions
- React Native, Flutter, SwiftUI, Jetpack Compose
```

### 2. Reload Router

The domain router automatically loads all `.md` files in `.claude/domains/` (excluding `README.md`).

```python
router = DomainRouter()  # Loads all domains
router.list_domains()    # ['frontend', 'backend', 'infrastructure', 'security', 'data', 'mobile']
```

### 3. Test Detection

```python
domains = router.identify_domains(
    request_text="Create iOS app with SwiftUI",
    file_paths=["MyApp/ContentView.swift"]
)
# Should detect 'mobile' domain
```

## Domain Configuration Best Practices

### 1. Clear Triggers

**Good**:
```markdown
### Keywords
- **React-specific**: component, hook, JSX, useState, useEffect
- **State management**: Redux, Zustand, TanStack Query
- **Styling**: Tailwind, styled-components, CSS modules
```

**Bad**:
```markdown
### Keywords
- frontend, UI, web
```

### 2. Specific File Patterns

**Good**:
```markdown
### File Patterns
- `src/components/**/*.tsx`
- `src/hooks/**/*.ts`
- `*.module.css`, `*.scss`
```

**Bad**:
```markdown
### File Patterns
- `src/**/*`
```

### 3. Comprehensive Tech Stack

Include all variations:
```markdown
## Tech Stack
- **Framework**: React 18+, Next.js 13+
- **Language**: TypeScript, JavaScript ES2022+
- **Styling**: Tailwind CSS, Styled Components, CSS Modules
```

### 4. Realistic Workflows

Base workflows on actual tasks:
```markdown
### New Feature Development
spec-manager → frontend-developer → qa-specialist → git-workflow-manager
```

Not overly complex:
```markdown
### Every Task (BAD)
spec-manager → systems-architect → frontend-developer → security-auditor → qa-specialist → dependency-scanner → git-workflow-manager
```

## Fallback Behavior

When **no domains match** (confidence < 0.3):
- Use general-purpose agent routing from main `CLAUDE.md`
- Apply standard quality gates
- No domain-specific optimizations

This ensures the system works for:
- Informational questions
- Generic tasks
- New/uncategorized domains

## Integration with Telemetry

Domain detection is tracked in telemetry:

```json
{
  "detected_domains": [
    {
      "domain": "frontend",
      "confidence": 0.85,
      "reasons": ["3 keywords matched", "1 file pattern matched"]
    }
  ],
  "recommended_agents": ["frontend-developer", "qa-specialist"],
  "workflow_type": "domain_specific"
}
```

This enables:
- Accuracy tracking (did domain detection help?)
- Confidence threshold tuning
- Domain configuration improvements

## Examples

### Example 1: Simple Frontend Task

**Request**: "Add loading spinner to button"

**Detection**:
```
Domain: frontend
Confidence: 0.75
Reasons: 2 keywords matched (button, loading)
File: src/components/Button.tsx (1 pattern matched)
```

**Agents**: frontend-developer → qa-specialist

**Outcome**: Fast, focused implementation with frontend best practices

---

### Example 2: Cross-Domain Feature

**Request**: "Build user authentication with JWT tokens"

**Detection**:
```
Domain: security
Confidence: 0.90
Reasons: 3 keywords matched (authentication, JWT, tokens)

Domain: backend
Confidence: 0.70
Reasons: 2 keywords matched (user, API)
```

**Agents**: security-auditor, infrastructure-specialist, qa-specialist

**Outcome**: Secure implementation with both security and backend expertise

---

### Example 3: Infrastructure Deployment

**Request**: "Deploy to AWS using CDK with Lambda and DynamoDB"

**Detection**:
```
Domain: infrastructure
Confidence: 0.95
Reasons: 5 keywords matched (AWS, CDK, Lambda, DynamoDB, deploy)

Domain: backend
Confidence: 0.40
Reasons: 1 keyword matched (Lambda)
```

**Agents**: infrastructure-specialist, security-auditor

**Outcome**: Proper CDK patterns, IAM permissions, infrastructure best practices

---

### Example 4: Database Performance

**Request**: "Optimize slow MongoDB aggregation query"

**Detection**:
```
Domain: data
Confidence: 0.85
Reasons: 3 keywords matched (MongoDB, query, optimize)

Domain: backend
Confidence: 0.50
Reasons: 1 keyword matched (query)
```

**Agents**: debug-specialist, infrastructure-specialist, qa-specialist

**Outcome**: Query analysis, index creation, performance verification

## Troubleshooting

### Domain Not Detected

**Problem**: Expected domain not appearing

**Solutions**:
1. Check keyword coverage in domain config
2. Verify file patterns match your project structure
3. Lower confidence threshold (default: 0.3)
4. Add more specific tech stack terms

### Wrong Domain Detected

**Problem**: Incorrect domain has higher confidence

**Solutions**:
1. Add more specific keywords to correct domain
2. Review overlapping keywords between domains
3. Improve file pattern specificity
4. Add negative patterns (future enhancement)

### Multiple Domains, Unclear Primary

**Problem**: 2-3 domains with similar confidence

**This is expected!** Many tasks span multiple domains:
- "Deploy React app" → Frontend + Infrastructure
- "API with authentication" → Backend + Security
- "Database migration" → Data + Backend

The system will:
- Use agents from all matched domains
- Prioritize by confidence score
- Coordinate across domain boundaries

## Future Enhancements

### Planned Features

1. **Negative Patterns**: Exclude certain keywords/patterns
2. **User Feedback Loop**: Learn from corrections
3. **Domain Dependencies**: Automatic inclusion (e.g., Security always included)
4. **Dynamic Confidence Tuning**: Adjust thresholds based on success rate
5. **Domain Specialization**: Sub-domains (e.g., frontend → React, Vue, Angular)

### Contributing

To improve domain configurations:

1. Identify missing keywords/patterns
2. Add to domain `.md` file
3. Test with `python core/domain_router.py`
4. Commit improvements

## Resources

- **Main Configuration**: `/Users/robertnyborg/Projects/claude-oak-agents/CLAUDE.md`
- **Domain Configs**: `/Users/robertnyborg/Projects/claude-oak-agents/.claude/domains/`
- **Domain Router**: `/Users/robertnyborg/Projects/claude-oak-agents/core/domain_router.py`
- **Agent Definitions**: `/Users/robertnyborg/Projects/claude-oak-agents/agents/`

## Summary

Domain-specific configuration enables:

- ✅ **Context-aware routing**: Right agents for the right tasks
- ✅ **Specialized workflows**: Domain-optimized agent coordination
- ✅ **Tech stack patterns**: Framework-specific best practices
- ✅ **Faster execution**: Skip irrelevant agents
- ✅ **Better quality**: Domain expertise applied
- ✅ **Automatic detection**: No manual domain selection needed

The system **just works** - describe your task naturally, and the domain router handles the rest.
