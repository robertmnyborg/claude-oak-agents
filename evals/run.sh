#!/usr/bin/env bash
# Run the WITH/WITHOUT A/B for every agent (or one) via the skill-eval harness.
# Each agent's markdown is injected as the system prompt in the WITH arm; the WITHOUT
# arm is the bare model with no ambient CLAUDE.md. Rubrics are hard checks (see suites/).
#   evals/run.sh [agent-name] [--runs N]
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="${SKILL_EVAL_RUNNER:-$HOME/.claude/skills/skill-eval/run-eval.sh}"
[ -x "$RUNNER" ] || { echo "skill-eval runner not found at $RUNNER" >&2; exit 1; }
STAMP="${SKILL_EVAL_STAMP:-$(date +%Y-%m-%d)}"
ONLY=""; RUNS=()
while [ $# -gt 0 ]; do case "$1" in --runs) RUNS=(--runs "$2"); shift 2;; *) ONLY="$1"; shift;; esac; done
for suite in "$HERE"/suites/*.json; do
  name=$(basename "$suite" .json)
  [ -n "$ONLY" ] && [ "$name" != "$ONLY" ] && continue
  echo "=== $name" >&2
  SKILL_EVAL_STAMP="$STAMP" "$RUNNER" "$suite" "${RUNS[@]}" || echo "runner failed for $name" >&2
  src="$(dirname "$RUNNER")/results/oak-$name-$STAMP"
  if [ -d "$src" ]; then mkdir -p "$HERE/results/$STAMP"; cp "$src/report.md" "$HERE/results/$STAMP/$name.md"; fi
done
echo "reports: $HERE/results/$STAMP/" >&2
