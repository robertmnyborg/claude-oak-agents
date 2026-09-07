# evals

WITH-vs-WITHOUT A/B suites, one per agent. Each scenario is `{id, prompt, rubric}`; the rubric is a hard check the judge model applies, so a vague rubric is a broken eval.

```
evals/run.sh                    # all five, 3 runs per arm
evals/run.sh quality-gate --runs 5
```

Results land in `results/<date>/<agent>.md`. Raw transcripts and verdicts stay in the skill-eval harness's `results/oak-<agent>-<date>/raw.jsonl`.

Rules for editing:
- Change an agent, rerun its suite, commit both. A KEEP verdict from before the edit says nothing about the edit.
- A HURTS scenario is either an agent defect (fix the prompt) or a rubric defect (say so in the report). Decide which before touching either.
- Add a scenario when a real session shows the agent missing something; the prompt should not name the agent's domain verbatim or the WITHOUT arm auto-triggers on the keyword.
- `claude plugin eval` is early-access on this account (`experimental.evals` is set in `.claude-plugin/plugin.json` for when it opens). The skill-eval harness is the fallback and the current source of the README numbers.
