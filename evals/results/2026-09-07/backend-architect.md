# skill-eval: `oak-backend-architect`

- skill_path: `/Users/robertnyborg/Projects/claude-code/claude-oak-agents/agents/backend-architect.md` (      54 lines)
- model: `claude-sonnet-4-6` · judge: `claude-sonnet-4-6` · runs/arm: 3

| scenario | with-skill | without-skill | delta | verdict |
|---|---|---|---|---|
| multitenant-schema | 100% (3/3) | 33% (1/3) | +67 pts | helps ✅ |
| rest-list-endpoint | 100% (3/3) | 100% (3/3) | 0 pts | neutral |
| migration-both-ways | 100% (3/3) | 0% (0/3) | +100 pts | helps ✅ |

**Overall: with 100% vs without 44% → +56 pts**

**Verdict: KEEP — skill measurably helps (+56 pts).**

_Caveat: WITH-arm injects the SKILL.md body as a system prompt; the WITHOUT arm omits it. If the skill's description also auto-triggers on the task prompt, the without arm may be contaminated — pick task prompts that don't name the skill's domain verbatim._
