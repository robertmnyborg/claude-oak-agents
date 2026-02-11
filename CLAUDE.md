# Claude OaK Development Rules

## Agents

This project provides 5 lean agents for Claude Code. Each is a single markdown file in `agents/`.

### Agent Roles

- **quality-gate**: Code review + quality scoring (0-100). Invoke after implementation, before commit. Blocks on security vulnerabilities, breaking changes without migration, data loss risk.
- **design-simplicity-advisor**: KISS enforcement. Invoke before significant implementations. Pushes back on unnecessary complexity.
- **backend-architect**: Database and API design. Schema, migrations, REST/GraphQL contracts.
- **frontend-developer**: UI implementation. React/Vue/Angular, accessibility, performance.
- **security-auditor**: Security analysis. Vulnerabilities, OWASP Top 10, secure coding patterns.

### When to Use Agents

- **Simple changes** (typo, one-line fix): Just do it directly.
- **Feature implementation**: Consider invoking design-simplicity-advisor first, then the domain specialist, then quality-gate before commit.
- **Security-sensitive changes**: Always invoke security-auditor for auth, user input, or API changes.

### Workflow

The recommended flow for non-trivial changes:

```
1. design-simplicity-advisor (question complexity)
2. domain specialist (backend-architect or frontend-developer)
3. quality-gate (review before commit)
4. security-auditor (if auth/input/API involved)
```

## Project Standards

- Agent files must stay under 200 lines
- No orchestration framework - agents are standalone prompts
- No telemetry, no Python scripts, no automation layer
- Keep it simple - if it needs a README longer than the code, it's too complex
