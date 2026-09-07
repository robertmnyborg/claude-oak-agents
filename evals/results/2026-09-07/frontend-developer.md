# skill-eval: `oak-frontend-developer`

- skill_path: `/Users/robertnyborg/Projects/claude-code/claude-oak-agents/agents/frontend-developer.md` (      55 lines)
- model: `claude-sonnet-4-6` · judge: `claude-sonnet-4-6` · runs/arm: 3

| scenario | with-skill | without-skill | delta | verdict |
|---|---|---|---|---|
| settings-form | 66% (2/3) | 0% (0/3) | +66 pts | helps ✅ |
| data-list-states | 100% (3/3) | 100% (3/3) | 0 pts | neutral |
| accessible-modal | 100% (3/3) | 100% (3/3) | 0 pts | neutral |

**Overall: with 88% vs without 66% → +22 pts**

**Verdict: KEEP — skill measurably helps (+22 pts).**

_Caveat: WITH-arm injects the SKILL.md body as a system prompt; the WITHOUT arm omits it. If the skill's description also auto-triggers on the task prompt, the without arm may be contaminated — pick task prompts that don't name the skill's domain verbatim._
