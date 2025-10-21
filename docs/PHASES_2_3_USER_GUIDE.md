# Phase 2 & 3 User Guide

## Overview

Phase 2 (Root Cause Analysis) and Phase 3 (Metrics Collection) work together to help you understand and improve agent performance over time.

**Phase 2**: Identifies **WHY** agents fail and generates improvement proposals
**Phase 3**: Tracks **HOW WELL** agents are performing and visualizes trends

Both systems run automatically during weekly and monthly reviews.

---

## Quick Start

### Weekly Review (15 minutes)

Run your weekly review as normal:

```bash
oak-weekly-review
# OR
python3 scripts/automation/weekly_review.py
```

**What happens automatically**:
1. ✅ Collects weekly metrics (Phase 3)
2. ✅ Detects false completions (Phase 1)
3. ✅ Shows performance summary
4. ✅ Prompts for issue verification
5. ✅ Updates metrics

**Your actions**:
- Confirm or reject issue resolutions when prompted
- Provide optional feedback on underperforming agents

### Monthly Review (1 hour)

Run your monthly analysis:

```bash
oak-monthly-review
# OR
python3 scripts/automation/monthly_analysis.py
```

**What happens automatically**:
1. ✅ Collects monthly metrics (Phase 3)
2. ✅ Analyzes root causes (Phase 2)
3. ✅ Runs agent portfolio audit
4. ✅ Prompts for issue verification
5. ✅ Generates improvement proposals
6. ✅ Creates curation agenda

**Your actions**:
- Review improvement proposals
- Confirm or reject issue resolutions
- Provide feedback on active agents
- Make decisions on recommended improvements

---

## Phase 3: Metrics Collection

### What It Tracks

**Agent-Level Metrics** (per agent):
- Invocations: How many times the agent was used
- Success Rate: % of tasks completed successfully on first try
- False Completion Rate: % of tasks that user had to repeat
- Avg Resolution Time: Time from issue detected to user-confirmed resolved
- User Satisfaction: Average rating from feedback (1-5)
- Rework Rate: % of tasks requiring follow-up work
- Issues: Open, resolved, needs verification counts

**System-Wide Metrics**:
- Total invocations across all agents
- System success rate (weighted average)
- System false completion rate
- Average resolution time
- Agent health distribution (green/yellow/red)

### How to Use

**Automatic collection** (during weekly/monthly reviews):
```bash
oak-weekly-review    # Collects weekly metrics
oak-monthly-review   # Collects monthly metrics
```

**Manual collection**:
```bash
# Collect weekly metrics
python3 scripts/phase3/collect_metrics.py --period week

# Collect monthly metrics
python3 scripts/phase3/collect_metrics.py --period month
```

**View all agents summary**:
```bash
python3 scripts/phase3/view_trends.py
```

Output:
```
📊 All Agents Summary
======================================================================

Agent                          Success    False Comp   Health   Trend
----------------------------------------------------------------------
frontend-developer              91.5%       7.8%     🟢 green  ↗️
backend-architect               88.3%      10.2%     🟢 green  →
infrastructure-specialist       85.1%      12.4%     🟡 yellow ↘️
```

**View specific agent trends**:
```bash
# View success rate trend
python3 scripts/phase3/view_trends.py --agent frontend-developer

# View all metrics for an agent
python3 scripts/phase3/view_trends.py --agent frontend-developer --metric all
```

Output:
```
📊 Metrics Trend: frontend-developer
======================================================================

Success Rate:
  Current: 91.5% ↗️
  Trend:   ▁▂▃▄▅▆▇█  (improving!)
  Samples: 8

False Completion Rate:
  Current: 7.8% ↗️
  Trend:   █▇▆▅▄▃▂▁  (improving!)
  Samples: 8
```

**View system-wide trends**:
```bash
python3 scripts/phase3/view_trends.py --system
```

### Data Storage

Metrics are stored in append-only JSONL files:
- `telemetry/agent_metrics.jsonl` - One entry per agent per collection
- `telemetry/system_metrics.jsonl` - One entry per collection

Each line is a JSON object with timestamp, allowing time-series analysis.

---

## Phase 2: Root Cause Analysis

### What It Does

Analyzes resolved issues to identify patterns and generate improvement proposals.

**Pattern Detection**:
- Groups issues by agent
- Identifies most common root causes
- Extracts common keywords
- Calculates reopened rate and resolution time

**Root Cause Categories**:
1. **Missing Verification**: Agent claimed completion without testing
2. **Unclear Instructions**: Agent didn't understand what "done" means
3. **Wrong Approach**: Agent used wrong strategy for problem
4. **Missing Domain Knowledge**: Agent lacks specific framework knowledge
5. **Incomplete Context**: Agent didn't consider full system state

**Improvement Proposals**:
- Generated for each agent with issues
- Include specific checklist improvements
- Show expected impact (e.g., "reduce false completions by 60-80%")
- Backed by evidence from real issues

### How to Use

**Automatic analysis** (during monthly review):
```bash
oak-monthly-review  # Runs root cause analysis automatically
```

**Manual analysis**:
```bash
# Analyze all agents with 2+ issues
python3 scripts/phase2/analyze_root_causes.py

# Analyze agents with 1+ issues (lower threshold)
python3 scripts/phase2/analyze_root_causes.py --min-issues 1

# Save to specific file
python3 scripts/phase2/analyze_root_causes.py --output my_report.md
```

### Example Output

**Console Output**:
```
📊 Analyzing 12 resolved issues...
   Found issues for 3 agents
   ✓ frontend-developer: 5 issues, root cause: Missing Verification
   ✓ backend-architect: 4 issues, root cause: Wrong Approach
   ✓ infrastructure-specialist: 3 issues, root cause: Missing Verification

📝 Generating improvement proposals for 3 agents...

✓ Proposals saved to: reports/improvement_proposals/2025-10.md
```

**Generated Report** (`reports/improvement_proposals/2025-10.md`):
```markdown
# Improvement Proposals - October 2025

## frontend-developer

### Issue Pattern: Missing Verification (5 occurrences)

**Root Cause**: Agent claimed completion without testing

**Evidence**:
- Issue: "Fix crash when adding secondary community" (REOPENED)
- Issue: "Fix Delete button crash" (REOPENED)
- Issue: "Fix table rendering error"

**Reopened Rate**: 2/5 (40%)
**Avg Resolution Time**: 36.2 hours

**Proposed Improvement**:
Add explicit verification steps to agent checklist:

\`\`\`markdown
Before claiming completion:
- [ ] Reproduced the original error/crash
- [ ] Applied the fix
- [ ] Verified the error no longer occurs
- [ ] Checked for console errors/warnings
- [ ] Tested related functionality still works
\`\`\`

**Expected Impact**: Reduce false completions by 60-80%

---

## backend-architect

### Issue Pattern: Wrong Approach (4 occurrences)

**Root Cause**: Agent used wrong strategy for problem

... (more details)
```

### What To Do With Proposals

1. **Review the proposal**: Read the generated markdown file
2. **Edit if needed**: Modify the proposed improvements
3. **Apply to agent**: Update the agent's markdown file with new checklist
4. **Track impact**: Monitor metrics after applying improvement

**Example - Applying an improvement**:

```bash
# 1. Review proposal
cat reports/improvement_proposals/2025-10.md

# 2. Edit agent markdown file
# Add the proposed checklist to agents/frontend-developer.md

# 3. Track metrics
python3 scripts/phase3/view_trends.py --agent frontend-developer

# 4. Validate improvement
# Check if false completion rate decreases over next few weeks
```

---

## Understanding Health Status

### Agent Health

**🟢 Green** (Healthy):
- Success rate >85%
- False completion rate <10%
- Improving or stable trend

**🟡 Yellow** (Needs Monitoring):
- Success rate 70-85%
- False completion rate 10-20%
- Stable trend

**🔴 Red** (Needs Attention):
- Success rate <70%
- False completion rate >20%
- Declining trend

### System Health

**🟢 Green** (Healthy System):
- >90% of agents in green status
- False completions declining system-wide
- Improvement proposals being applied

**🟡 Yellow** (Monitor):
- 70-90% agents in green
- False completions stable
- Some proposals pending

**🔴 Red** (Action Required):
- <70% agents in green
- False completions increasing
- Proposals not being addressed

---

## Complete Workflow Example

### Week 1: First Weekly Review

```bash
oak-weekly-review
```

Output shows:
- Metrics collected (all agents green initially)
- 3 false completions detected
- 3 issues created (all open)

**Your action**: None yet, just let data accumulate

### Week 2-3: More Weekly Reviews

```bash
oak-weekly-review  # Run each week
```

Each week:
- Metrics collected (trends starting to show)
- More false completions detected (if any)
- You confirm or reject issue resolutions when prompted

### Week 4: Monthly Review

```bash
oak-monthly-review
```

Output shows:
1. **Monthly metrics collected**:
   - frontend-developer: 88% success, 12% false completion (yellow)
   - backend-architect: 92% success, 6% false completion (green)

2. **Root cause analysis**:
   - frontend-developer has 5 issues (missing verification)
   - Proposal generated to add button-click verification

3. **Agent audit**:
   - System health: 85% agents green
   - 1 capability gap detected

4. **Issue verification**:
   - You confirm 3 issues resolved
   - You mark 1 issue as still broken (reopened)

5. **Reports generated**:
   - Improvement proposals: `reports/improvement_proposals/2025-10.md`
   - Agent audit: `reports/agent_audit/audit_2025-10-21.md`
   - Curation agenda: `reports/curation/agenda_2025-10.md`

**Your actions**:
1. Review improvement proposal for frontend-developer
2. Update `agents/frontend-developer.md` with new checklist
3. Monitor metrics next few weeks to validate improvement

### Week 5-8: Validate Improvement

```bash
oak-weekly-review  # Each week
```

View trends:
```bash
python3 scripts/phase3/view_trends.py --agent frontend-developer
```

Expected:
- False completion rate: 12% → 8% → 6% → 5% (↗️ improving!)
- Success rate: 88% → 90% → 91% → 92% (↗️ improving!)

**Result**: ✅ Improvement worked! False completions reduced by 58%

---

## Troubleshooting

### "No resolved issues found"

**Problem**: Root cause analysis finds no resolved issues

**Solution**:
- This is expected if you haven't confirmed any issues as resolved yet
- Run weekly reviews and confirm issues when prompted
- After 2-3 weeks, you'll have resolved issues to analyze

### "No metrics found"

**Problem**: View trends shows "No metrics found"

**Solution**:
- Run metrics collection first: `python3 scripts/phase3/collect_metrics.py`
- Or run a weekly/monthly review (collects metrics automatically)

### "Metrics show 0% false completion but I know there are issues"

**Problem**: Metrics don't reflect known problems

**Solution**:
- Issues must be created by false completion detection
- Make sure you're using agents normally (triggers detection)
- Run `python3 scripts/detect_false_completions.py` manually
- Check `telemetry/issues.jsonl` for created issues

---

## Files and Directories

### Scripts

**Phase 2** (Root Cause Analysis):
- `scripts/phase2/analyze_root_causes.py` - Pattern detection and proposal generation

**Phase 3** (Metrics Collection):
- `scripts/phase3/collect_metrics.py` - Collect agent and system metrics
- `scripts/phase3/view_trends.py` - View metrics trends in terminal

### Data Files

**Input**:
- `telemetry/agent_invocations.jsonl` - Raw telemetry data
- `telemetry/issues.jsonl` - Issue tracking data
- `telemetry/agent_reviews.jsonl` - User feedback

**Output**:
- `telemetry/agent_metrics.jsonl` - Time-series agent metrics
- `telemetry/system_metrics.jsonl` - Time-series system metrics
- `reports/improvement_proposals/YYYY-MM.md` - Monthly proposals
- `reports/agent_audit/` - Portfolio audit reports
- `reports/curation/` - Curation agendas

---

## Next Steps

1. **Start collecting data**: Run weekly reviews for 2-4 weeks
2. **Review first proposals**: Check monthly improvement proposals
3. **Apply improvements**: Update agent markdown files based on proposals
4. **Track impact**: Monitor metrics to validate improvements
5. **Iterate**: Repeat monthly cycle, system continuously improves

## Questions?

- Design documents: `docs/ADAPTIVE_SYSTEM_DESIGN.md`
- Success metrics: `docs/SUCCESS_METRICS_REFERENCE.md`
- Phase 1 (Issue Tracking): Built-in to weekly/monthly reviews
