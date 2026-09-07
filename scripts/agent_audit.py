#!/usr/bin/env python3
"""Subagent portfolio audit over Claude Code transcripts. Deterministic, stdlib only.

Answers, per subagent_type, over a rolling window:
  invocations, sessions, retry rate (same type re-launched in the same session with a
  similar task within 30 min), error-mention rate in the returned report, and roster
  overlap (description keyword Jaccard). Then applies fixed rules to recommend
  deprecate / review / consolidate / unlisted. It never edits an agent file; a human
  does, or dismisses the line in the ignore file.

Usage:
  agent_audit.py [--days 90] [--agents-dir DIR ...] [--ignore FILE] [--out FILE] [--json FILE]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oak_transcripts import (  # noqa: E402
    PROJECTS_DIR,
    Session,
    final_assistant_text,
    iter_session_files,
    jaccard,
    keywords,
    load_session,
    read_agent_roster,
    window_start,
)

RETRY_WINDOW = timedelta(minutes=30)
RETRY_PROMPT_SIMILARITY = 0.3   # prompt keyword Jaccard
RETRY_DESC_SIMILARITY = 0.6     # near-identical description, or the earlier run errored
ERROR_RE = re.compile(
    r"\b(error|failed|failure|could not|couldn't|unable to|not found|permission denied|timed out)\b",
    re.I,
)
AGENT_ID_RE = re.compile(r"agent_id:\s*([0-9a-f]+)")

# Rules (coded from the 2025 agent-auditor prompt, thresholds made explicit).
DEPRECATE_ZERO_DAYS = 90  # in roster, zero invocations, file older than window -> deprecate
REVIEW_MIN_N = 5
REVIEW_RETRY_RATE = 0.30
CONSOLIDATE_OVERLAP = 0.50


def collect(days: int) -> tuple[list[dict], dict]:
    since = window_start(days)
    invocations: list[dict] = []
    sessions_seen = 0
    for f in iter_session_files(since):
        s = load_session(f)
        if not s.turns:
            continue
        sessions_seen += 1
        invocations.extend(_invocations(s, since))
    return invocations, {"sessions_scanned": sessions_seen, "since": since.isoformat()}


def _invocations(s: Session, since: datetime) -> list[dict]:
    out = []
    for turn_idx, turn in enumerate(s.turns):
        if turn.role != "assistant" or turn.ts < since:
            continue
        for tu in turn.tool_uses:
            if tu.name not in ("Agent", "Task"):
                continue
            result = turn.results.get(tu.id, "")
            report = result
            m = AGENT_ID_RE.search(result)
            if m:
                sub = s.subagent_file(m.group(1))
                if sub:
                    report = final_assistant_text(sub)
            out.append(
                {
                    "ts": tu.ts,
                    "turn": turn_idx,
                    "session": s.session_id,
                    "cwd": s.cwd,
                    "type": tu.input.get("subagent_type") or "(none)",
                    "description": tu.input.get("description", ""),
                    "desc_kw": keywords(tu.input.get("description", "")),
                    "prompt_kw": keywords(tu.input.get("prompt", "")[:2000]),
                    "sidechain": turn.sidechain,
                    "report": report,
                    "error_mention": bool(ERROR_RE.search(report[-1500:])) if report else False,
                    "empty_result": not report.strip(),
                }
            )
    # Retry proxy: same type, launched in a LATER assistant turn within RETRY_WINDOW, with a
    # similar prompt, AND either a near-identical description or an earlier run that came
    # back empty/erroring. A sequential fan-out over a template ("Financials: <property>")
    # shares prompt words but not the description, so it does not count.
    out.sort(key=lambda r: r["ts"])
    for i, r in enumerate(out):
        r["retry"] = False
        for p in out[:i]:
            if p["type"] != r["type"] or p["turn"] == r["turn"] or r["ts"] - p["ts"] > RETRY_WINDOW:
                continue
            if jaccard(p["prompt_kw"], r["prompt_kw"]) < RETRY_PROMPT_SIMILARITY:
                continue
            if jaccard(p["desc_kw"], r["desc_kw"]) >= RETRY_DESC_SIMILARITY or p["error_mention"] or p["empty_result"]:
                r["retry"] = True
                break
    return out


def summarize(invocations: list[dict], roster: dict[str, dict], days: int, ignore: set[str]) -> dict:
    by_type: dict[str, list[dict]] = defaultdict(list)
    for r in invocations:
        by_type[r["type"]].append(r)

    rows = []
    for t, rs in sorted(by_type.items(), key=lambda kv: -len(kv[1])):
        n = len(rs)
        rows.append(
            {
                "type": t,
                "in_roster": t in roster,
                "invocations": n,
                "sessions": len({r["session"] for r in rs}),
                "retry_rate": sum(r["retry"] for r in rs) / n,
                "error_mention_rate": sum(r["error_mention"] for r in rs) / n,
                "empty_rate": sum(r["empty_result"] for r in rs) / n,
                "first": min(r["ts"] for r in rs).date().isoformat(),
                "last": max(r["ts"] for r in rs).date().isoformat(),
            }
        )
    for name, meta in roster.items():
        if name not in by_type:
            rows.append(
                {
                    "type": name,
                    "in_roster": True,
                    "invocations": 0,
                    "sessions": 0,
                    "retry_rate": 0.0,
                    "error_mention_rate": 0.0,
                    "empty_rate": 0.0,
                    "first": "",
                    "last": "",
                    "file_age_days": (datetime.now(timezone.utc) - meta["mtime"]).days,
                }
            )

    # Overlap among roster descriptions.
    names = sorted(roster)
    kw = {n: keywords(roster[n]["description"] + " " + n.replace("-", " ")) for n in names}
    overlaps = []
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            j = jaccard(kw[a], kw[b])
            if j >= 0.25:
                overlaps.append({"a": a, "b": b, "jaccard": round(j, 2)})
    overlaps.sort(key=lambda o: -o["jaccard"])

    recs = []
    for row in rows:
        t = row["type"]
        if t in ignore:
            continue
        if not row["in_roster"]:
            recs.append((t, "unlisted", f"invoked {row['invocations']}x but no agent file in roster (built-in or plugin agent)"))
        elif row["invocations"] == 0 and row.get("file_age_days", 0) >= DEPRECATE_ZERO_DAYS:
            recs.append((t, "deprecate", f"0 invocations in {days}d, file age {row['file_age_days']}d"))
        elif row["invocations"] >= REVIEW_MIN_N and row["retry_rate"] >= REVIEW_RETRY_RATE:
            recs.append((t, "review", f"retry rate {row['retry_rate']:.0%} over {row['invocations']} invocations"))
    for o in overlaps:
        if o["jaccard"] >= CONSOLIDATE_OVERLAP and o["a"] not in ignore and o["b"] not in ignore:
            recs.append((f"{o['a']} + {o['b']}", "consolidate", f"description overlap {o['jaccard']}"))

    return {"rows": rows, "overlaps": overlaps, "recommendations": recs}


def render(summary: dict, meta: dict, days: int, roster_dirs: list[Path]) -> str:
    L = []
    L.append(f"# Subagent audit — {datetime.now().date()} (window {days}d, since {meta['since'][:10]})")
    L.append("")
    L.append(f"Sessions scanned: {meta['sessions_scanned']}. Roster dirs: {', '.join(str(d) for d in roster_dirs)}.")
    L.append("Retry rate and error-mention rate are proxies read from transcripts, not ground truth.")
    L.append("Guardrail: this audit refuses false deprecations — a zero-count line is a prompt to look, never an auto-delete.")
    L.append("")
    L.append("## Recommendations")
    L.append("")
    if not summary["recommendations"]:
        L.append("None. Every roster agent was invoked and no retry or overlap threshold fired.")
    else:
        L.append("| Agent | Action | Because |")
        L.append("|---|---|---|")
        for t, a, why in summary["recommendations"]:
            L.append(f"| `{t}` | **{a}** | {why} |")
    L.append("")
    L.append("## Utilization")
    L.append("")
    L.append("| subagent_type | roster | invocations | sessions | retry | error-mention | empty | first | last |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in summary["rows"]:
        L.append(
            f"| `{r['type']}` | {'yes' if r['in_roster'] else 'no'} | {r['invocations']} | {r['sessions']} | "
            f"{r['retry_rate']:.0%} | {r['error_mention_rate']:.0%} | {r['empty_rate']:.0%} | {r['first']} | {r['last']} |"
        )
    L.append("")
    L.append("## Roster overlap (description Jaccard ≥ 0.25)")
    L.append("")
    if not summary["overlaps"]:
        L.append("None.")
    else:
        L.append("| a | b | jaccard |")
        L.append("|---|---|---|")
        for o in summary["overlaps"]:
            L.append(f"| `{o['a']}` | `{o['b']}` | {o['jaccard']} |")
    L.append("")
    L.append("Closing signal (loops.md): every recommendation above is actioned (agent file edited/removed) or dismissed by name in the ignore file before the next run.")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--agents-dir", action="append", type=Path, help="agent .md dir (repeatable); default ~/.claude/agents")
    ap.add_argument("--ignore", type=Path, default=Path.home() / ".claude" / "oak-audit-ignore.txt",
                    help="one agent name per line; dismissed recommendations")
    ap.add_argument("--out", type=Path, help="write markdown here (default stdout)")
    ap.add_argument("--json", type=Path, help="also write machine-readable summary")
    a = ap.parse_args()

    roster_dirs = a.agents_dir or [Path.home() / ".claude" / "agents"]
    roster = read_agent_roster(roster_dirs)
    ignore = set()
    if a.ignore.exists():
        ignore = {ln.strip() for ln in a.ignore.read_text().splitlines() if ln.strip() and not ln.startswith("#")}

    invocations, meta = collect(a.days)
    summary = summarize(invocations, roster, a.days, ignore)
    md = render(summary, meta, a.days, roster_dirs)
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(md)
        print(f"wrote {a.out} ({len(summary['recommendations'])} recommendations)")
    else:
        sys.stdout.write(md)
    if a.json:
        a.json.write_text(json.dumps({"meta": meta, **summary}, default=str, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
