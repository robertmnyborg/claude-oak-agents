# Claude OaK Agents

**5 opinionated agents for Claude Code, measured against vanilla.**

Claude Code is already great at writing code. These agents add the checklists and verdict formats that prevent the common failure modes: over-engineering, unsafe migrations, missing states, and code review that hedges instead of blocking. Each one is A/B tested WITH vs WITHOUT the agent prompt; the numbers below are the current run.

## What's Included

| Agent | Purpose | A/B delta (pass-rate, 3 scenarios × 3 runs, sonnet-4-6, 2026-09-07) | Verdict |
|-------|---------|---|---|
| **quality-gate** | Code review with 0-100 score, auto-fail on security / breaking change / data loss | **+56 pts** (numeric verdict on clean code 0→100%; data-loss migration blocked 33→100%) | KEEP |
| **backend-architect** | DB + API design checklists | **+56 pts** (3NF schema with FKs/indexes/timestamps 33→100%; expand/contract migration 0→100%) | KEEP |
| **design-simplicity-advisor** | KISS enforcement | **+33 pts** (6-service pipeline and config-provider hierarchy both rejected 0→100%; one contested scenario, see below) | KEEP |
| **frontend-developer** | Component + accessibility checklists | **+22 pts** (typed props, labels, saving/error state 0→66%; states and a11y already 100% without) | KEEP |
| **security-auditor** | OWASP Top 10 checklist | **0 pts** (unverified JWT, IDOR, plaintext password, PII logging, leaked key: 100% in both arms; no false alarm on clean code in either) | NEUTRAL |

Reports: `evals/results/<date>/<agent>.md`. Suites: `evals/suites/<agent>.json`. Rerun: `evals/run.sh [agent] --runs 3` (needs the `skill-eval` harness at `~/.claude/skills/skill-eval/run-eval.sh`, or set `SKILL_EVAL_RUNNER`).

What the evals taught us, in one run:

- **A checklist line can make the model worse.** With the original backend-architect loaded, the model dropped the old column in the same migration that added the new ones (0/3), because the checklist only said "up and down". One expand/contract line fixed it to 3/3. The prompt is now the thing under test.
- **security-auditor earns nothing on sonnet-4-6.** Every vulnerability in the suite is caught unaided. Either the suite needs harder cases (SSRF, race conditions, auth-bypass via type confusion) or the agent goes. Neutral means it costs tokens for nothing until proven otherwise.
- **One scenario is contested.** `justified-complexity` (40M events/day, 5-min SLA) expects the advisor to accept a streaming stack; it argued Postgres+cron handles 463 events/sec. The rubric encodes the author's assumption. Left as-is so the disagreement stays visible.

## Also in the repo: two auditors over your own transcripts

Claude Code writes every session to `~/.claude/projects/**/*.jsonl`, including subagent runs. Two stdlib-only scripts read those as telemetry. No logger, no daemon, no model call.

- `scripts/agent_audit.py --days 90` — invocations per `subagent_type`, retry proxy, description overlap, fixed-threshold deprecate/review/consolidate lines. First run on the author's machine: 25 of 25 roster agents at zero invocations in 90 days, all 35 launches went to `general-purpose` and `Explore`. Dismiss a line by adding the name to `~/.claude/oak-audit-ignore.txt`.
- `scripts/false_completion.py --days 7` — an assistant turn that claims done/fixed/merged with no executing tool call behind it, AND a user contradiction or re-ask within 24h in the same cwd, across sessions. Strict AND: it refuses false positives. Label rows into `~/.claude/false-completion-golden.jsonl` and the next run prints precision.

History note: the 2025 version of this repo had an agent-auditor prompt, a keyword-overlap false-completion detector (100% false-positive rate on its 16 flags), and a Q-learning prompt-variant selector whose only executor was a test mock. All three are gone. The ideas survive as the two scripts and the eval suites above; the learning loop does not, because single-user volume (35 launches / 90 days) cannot train one.

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
