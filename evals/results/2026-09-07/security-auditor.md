# skill-eval: `oak-security-auditor`

- skill_path: `/Users/robertnyborg/Projects/claude-code/claude-oak-agents/agents/security-auditor.md` (      83 lines)
- model: `claude-sonnet-4-6` · judge: `claude-sonnet-4-6` · runs/arm: 3

| scenario | with-skill | without-skill | delta | verdict |
|---|---|---|---|---|
| jwt-verify-and-idor | 100% (3/3) | 100% (3/3) | 0 pts | neutral |
| logging-pii-and-secrets | 100% (3/3) | 100% (3/3) | 0 pts | neutral |
| clean-code-no-false-alarm | 100% (3/3) | 100% (3/3) | 0 pts | neutral |

**Overall: with 100% vs without 100% → 0 pts**

**Verdict: NEUTRAL — skill makes no measurable difference; consider deleting to save tokens.**

_Caveat: WITH-arm injects the SKILL.md body as a system prompt; the WITHOUT arm omits it. If the skill's description also auto-triggers on the task prompt, the without arm may be contaminated — pick task prompts that don't name the skill's domain verbatim._
