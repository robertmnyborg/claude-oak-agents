# skill-eval: `oak-design-simplicity-advisor`

- skill_path: `/Users/robertnyborg/Projects/claude-code/claude-oak-agents/agents/design-simplicity-advisor.md` (      69 lines)
- model: `claude-sonnet-4-6` · judge: `claude-sonnet-4-6` · runs/arm: 3

| scenario | with-skill | without-skill | delta | verdict |
|---|---|---|---|---|
| file-watch-pipeline | 100% (3/3) | 0% (0/3) | +100 pts | helps ✅ |
| config-framework | 100% (3/3) | 0% (0/3) | +100 pts | helps ✅ |
| justified-complexity | 0% (0/3) | 100% (3/3) | -100 pts | HURTS ❌ |

**Overall: with 66% vs without 33% → +33 pts**

**Verdict: KEEP — skill measurably helps (+33 pts).**

_Caveat: WITH-arm injects the SKILL.md body as a system prompt; the WITHOUT arm omits it. If the skill's description also auto-triggers on the task prompt, the without arm may be contaminated — pick task prompts that don't name the skill's domain verbatim._
