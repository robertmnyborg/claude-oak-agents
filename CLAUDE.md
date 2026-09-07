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

## Scripts (restored 2026-09)

`scripts/` holds two deterministic auditors that read Claude Code's own transcripts
(`~/.claude/projects/**/*.jsonl`). No logger, no daemon, no LLM, stdlib only.

- `agent_audit.py`: per-`subagent_type` utilization, retry proxy, roster overlap, fixed-threshold
  deprecate/review/consolidate lines. Never edits an agent.
- `false_completion.py`: unverified done/fixed claim AND a user contradiction or re-ask within 24h in
  the same cwd, cross-session. Strict AND; refuses false positives. Label rows in a golden file.
- `evals/`: WITH-vs-WITHOUT A/B suites per agent, run through the skill-eval harness.

## Project Standards

- Agent files must stay under 200 lines
- No orchestration framework - agents are standalone prompts
- Scripts are read-only over transcripts, deterministic, stdlib only; they recommend, a human acts
- No learned routing or reward loops: single-user volume cannot train one (measured: 35 subagent
  launches in 90 days). Measure agents with `evals/` instead
- Keep it simple - if it needs a README longer than the code, it's too complex
