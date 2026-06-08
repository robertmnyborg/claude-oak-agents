# Claude OaK Agents

**5 opinionated agents that make Claude Code better at building software.**

Claude Code is already great at writing code. These agents add the guardrails and standards that prevent the common failure modes: over-engineering, security gaps, inconsistent quality, and code that's clever instead of clear.

## What's Included

| Agent | Purpose | When It Helps |
|-------|---------|---------------|
| **quality-gate** | Unified code review with scoring (0-100) | Before every commit - catches security issues, breaking changes, and complexity creep |
| **design-simplicity-advisor** | KISS enforcement | Before implementing features - prevents building a distributed system when a shell script would work |
| **backend-architect** | Database + API design patterns | Schema design, API contracts, backend architecture decisions |
| **frontend-developer** | UI patterns + accessibility | Component design, state management, responsive/accessible interfaces |
| **security-auditor** | Vulnerability detection + OWASP Top 10 | Auth implementation, user input handling, API security, dependency review |

## Why Not Just Use Claude Code Vanilla?

Claude Code (as of Feb 2025) has native subagents, teams, and planning. These agents don't replicate that. Instead they provide:

1. **Opinionated quality scoring** - The quality-gate scores code on 8 weighted dimensions and auto-fails on security vulnerabilities or unplanned breaking changes. Claude Code doesn't do this by default.

2. **KISS enforcement** - The simplicity advisor actively pushes back on complexity with questions like "have you tried a shell script?" and "do you actually need this?" Vanilla Claude Code tends to build what you ask for without questioning whether you should.

3. **Domain checklists** - The backend and frontend agents carry specific checklists (database normalization, API design, component accessibility, OWASP Top 10) that serve as institutional memory.

## Installation

```bash
# Clone the repo
git clone https://github.com/robertmnyborg/claude-oak-agents.git ~/claude-oak-agents

# Symlink agents into your Claude Code config
mkdir -p ~/.claude/agents
ln -sf ~/claude-oak-agents/agents/*.md ~/.claude/agents/
```

That's it. Open Claude Code and the agents are available.

### Optional: Install slash commands

```bash
# Copy the useful slash commands
mkdir -p ~/.claude/commands
cp -r ~/claude-oak-agents/.claude/commands/* ~/.claude/commands/
```

## Usage

The agents activate automatically when Claude Code detects relevant work. You can also invoke them directly:

```
"Review this code before I commit" -> quality-gate
"Is this design too complex?" -> design-simplicity-advisor
"Design a schema for user subscriptions" -> backend-architect
"Build a settings page component" -> frontend-developer
"Review this auth implementation" -> security-auditor
```

### Example: Quality Gate in Action

```
PASS - Score: 82/100

Summary: Clean implementation following existing patterns. Minor documentation gaps.

Recommendations:
- Add JSDoc for the exported calculateDiscount function
- Consider extracting the validation logic into a shared util (used in 3 places)
```

### Example: Simplicity Advisor Pushing Back

```
Option 1: Shell script with cron (Score: 2/10) <- Recommended
- 15 lines of bash, runs on cron, logs to file
- "This is what a competent engineer would build"

Option 2: Lambda + SQS + DynamoDB (Score: 7/10)
- Serverless architecture with event queue
- "You're processing 10 files a day. You don't need this."
```

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/security-scan` | Run OWASP-based security analysis on a path |
| `/analyze-complexity` | Identify over-engineering and suggest simplifications |
| `/deploy-check` | Pre-deployment validation checklist |

## MCP Servers

### HeyReach

This repo ships a project-scoped [`.mcp.json`](.mcp.json) that connects the
[HeyReach MCP server](https://github.com/bcharleson/heyreach-mcp) for LinkedIn
outreach automation (campaigns, leads, conversations, analytics).

Set your API key as an environment variable before launching Claude Code — the
config reads `${HEYREACH_API_KEY}`, so the secret never lands in git:

```bash
export HEYREACH_API_KEY="your-heyreach-api-key"
```

Get the key from your HeyReach account under **Settings → API**. The server is
fetched on demand via `npx`, so no global install is required.

## Customization

Each agent is a single markdown file in `agents/`. Edit them to match your team's standards:

- Change technology preferences (e.g., swap "Go > TypeScript" to "Python > TypeScript" in backend-architect)
- Adjust quality-gate scoring weights
- Add your own checklists
- Tighten or relax the simplicity advisor's threshold

## Uninstall

```bash
# Remove symlinks
rm ~/.claude/agents/quality-gate.md
rm ~/.claude/agents/design-simplicity-advisor.md
rm ~/.claude/agents/backend-architect.md
rm ~/.claude/agents/frontend-developer.md
rm ~/.claude/agents/security-auditor.md
```

## License

MIT - See [LICENSE](LICENSE) for details.

## Contributing

PRs welcome. Keep agents lean (under 200 lines). The whole point is simplicity.
