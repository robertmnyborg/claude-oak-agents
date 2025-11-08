# Adaptive Agent System Design

## Overview

This document defines the complete improvement cycle for the claude-oak-agents system, from issue detection through root cause analysis, agent improvements, and validation of success.

**Core Question**: "If we're building an agentic system that adapts to your workflows, how do we know we're succeeding?"

## Complete Improvement Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTINUOUS IMPROVEMENT LOOP                  │
└─────────────────────────────────────────────────────────────────┘

Phase 1: DETECTION (✅ COMPLETE)
├── User asks twice → False completion detected
├── Issue created (open state)
├── Weekly/monthly review prompts user
└── User confirms: resolved, still_broken, or test_later

Phase 2: ROOT CAUSE ANALYSIS (🚧 DESIGN)
├── Analyze resolved issues monthly
├── Identify patterns (same agent, same error type, same domain)
├── Extract root causes:
│   ├── Missing verification steps
│   ├── Unclear agent instructions
│   ├── Wrong approach/strategy
│   └── Missing domain knowledge
├── Generate improvement proposals
└── User reviews and approves changes

Phase 3: AGENT IMPROVEMENT (🚧 DESIGN)
├── Update agent markdown files (instructions, checklists, examples)
├── Create versioned agent (v1 → v2)
├── Deploy improved agent
└── Track which version is active

Phase 4: VALIDATION (🚧 DESIGN)
├── A/B testing: Compare old vs new agent performance
├── Track metrics over time (success rate, false completion rate)
├── Statistical significance testing
└── User feedback correlation

Phase 5: LEARNING (🔮 FUTURE)
├── System learns from validated improvements
├── Automated pattern detection
├── Self-guided agent updates (with human approval)
└── ML-based performance prediction
```

## Phase 2: Root Cause Analysis

### Goals
- Identify WHY agents fail (not just THAT they fail)
- Detect patterns across multiple issues
- Generate actionable improvement proposals

### Data Analysis

**Input**: Resolved issues from `telemetry/issues.jsonl`

**Pattern Detection**:
```yaml
patterns:
  by_agent:
    - Which agents have most false completions?
    - What types of tasks do they fail on?

  by_error_type:
    - Verification failures (didn't test before claiming done)
    - Incomplete implementation (partial fixes)
    - Misunderstanding requirements
    - Wrong approach/strategy

  by_domain:
    - Frontend errors (UI bugs, state management)
    - Backend errors (API, database)
    - Infrastructure errors (deployment, CDK)

  temporal_patterns:
    - Are errors increasing or decreasing over time?
    - Do certain agents improve after updates?
```

### Root Cause Categories

**1. Missing Verification**
- Agent claimed completion without testing
- Example: "Fix button crash" but didn't click button
- Solution: Add specific verification step to checklist

**2. Unclear Instructions**
- Agent didn't understand what "done" means
- Example: "Make rows same height" interpreted differently
- Solution: Add concrete examples to agent markdown

**3. Wrong Approach**
- Agent used wrong strategy for problem
- Example: Used CSS when component refactor needed
- Solution: Add decision tree or approach guidance

**4. Missing Domain Knowledge**
- Agent lacks specific framework/library knowledge
- Example: Vue composition API patterns not understood
- Solution: Add framework-specific examples

**5. Incomplete Context**
- Agent didn't consider full system state
- Example: Fixed component but broke integration
- Solution: Add context-awareness instructions

### Improvement Proposal Generation

**Script**: `scripts/phase2/analyze_root_causes.py`

**Output**: `reports/improvement_proposals/YYYY-MM.md`

**Format**:
```markdown
# Improvement Proposals - October 2025

## frontend-developer

### Issue Pattern: Button crash fixes (3 occurrences)
**Root Cause**: Missing interaction testing verification
**Evidence**:
- Issue #abc123: "Fix Add button crash" - claimed fixed 2x, still broken
- Issue #def456: "Fix Delete button crash" - claimed fixed 3x, still broken

**Current Checklist**:
- [ ] Applied the fix
- [ ] Tested the fix

**Proposed Improvement**:
- [ ] Applied the fix
- [ ] **Clicked the button to reproduce original crash**
- [ ] **Verified button now works (no console errors)**
- [ ] **Tested related buttons still work**
- [ ] **Checked browser console for warnings**

**Expected Impact**: Reduce button-related false completions by 80%

---

## backend-architect

### Issue Pattern: Database query timeouts (2 occurrences)
**Root Cause**: No performance verification before claiming fixed
**Evidence**:
- Issue #ghi789: "Fix slow user query" - claimed fixed but still >30s

**Proposed Improvement**:
Add performance benchmark to verification checklist:
- [ ] **Measured query time before fix**
- [ ] **Measured query time after fix (<500ms for user queries)**
- [ ] **Tested with production-like data volume**

**Expected Impact**: Reduce query performance false completions by 90%
```

### Human Review Process

**Monthly Workflow**:
1. System generates improvement proposals
2. User reviews proposals in monthly analysis
3. User decisions:
   - ✅ Approve: Apply immediately
   - ✏️ Modify: Edit proposal then approve
   - ❌ Reject: Not the right solution
   - ⏸️ Defer: Need more data

**Approval Commands**:
```bash
# Review proposals
oak-review-proposals

# Approve specific proposal
oak-approve-proposal frontend-developer-2025-10

# Apply all approved proposals
oak-apply-improvements
```

## Phase 3: Metrics Tracking

### Agent-Level Metrics

**Per Agent** (`telemetry/agent_metrics.jsonl`):
```json
{
  "timestamp": "2025-10-21T00:00:00Z",
  "agent_name": "frontend-developer",
  "period": "week",
  "metrics": {
    "invocations": 42,
    "success_rate": 0.85,
    "false_completion_rate": 0.12,
    "avg_resolution_time_minutes": 23.5,
    "user_satisfaction": 4.2,
    "rework_rate": 0.08,
    "issues_opened": 5,
    "issues_resolved": 4,
    "issues_reopened": 1
  },
  "version": "v2.1"
}
```

**Key Metrics**:
- **Success Rate**: % of invocations marked successful on first try
- **False Completion Rate**: % of invocations that user had to repeat
- **Avg Resolution Time**: Time from issue detected to user-confirmed resolved
- **User Satisfaction**: Average rating from feedback prompts (1-5)
- **Rework Rate**: % of tasks requiring follow-up work
- **Issues by State**: Open, in_progress, needs_verification, resolved

### System-Level Metrics

**Overall System Health** (`telemetry/system_metrics.jsonl`):
```json
{
  "timestamp": "2025-10-21T00:00:00Z",
  "period": "week",
  "metrics": {
    "total_invocations": 387,
    "total_agents_used": 23,
    "system_success_rate": 0.88,
    "avg_issues_per_week": 12,
    "avg_resolution_time_hours": 48.2,
    "improvement_proposals_generated": 5,
    "improvements_applied": 3,
    "active_a_b_tests": 2
  }
}
```

### Trend Analysis

**Script**: `scripts/phase3/analyze_trends.py`

**Outputs**:
- `reports/trends/agent_performance_trends.html` - Interactive charts
- `reports/trends/system_health_dashboard.html` - Overall health

**Visualizations**:
1. **Success Rate Over Time** (line chart per agent)
2. **False Completion Rate Trend** (decreasing = good)
3. **Average Resolution Time** (decreasing = good)
4. **Issues by State** (stacked area chart)
5. **Agent Comparison** (bar chart of all agents)
6. **Improvement Impact** (before/after comparison)

### Success Indicators (Green/Yellow/Red)

**Per Agent**:
- 🟢 Green: Success rate >85%, false completion <10%, improving trend
- 🟡 Yellow: Success rate 70-85%, false completion 10-20%, stable
- 🔴 Red: Success rate <70%, false completion >20%, declining trend

**System-Wide**:
- 🟢 Green: >90% agents in green, false completions declining
- 🟡 Yellow: 70-90% agents in green, false completions stable
- 🔴 Red: <70% agents in green, false completions increasing

## Phase 4: A/B Testing & Validation

### When to A/B Test

**Triggers**:
- Major agent instruction changes (>50% of content modified)
- New approach/strategy introduced
- User requests validation before full rollout
- After 3+ improvements to same agent

### A/B Test Setup

**Structure**:
```
agents/
├── frontend-developer.md (v2 - current production)
├── frontend-developer-v1.md (baseline for comparison)
└── tests/
    └── frontend-developer-v2-test.yaml
```

**Test Configuration** (`tests/frontend-developer-v2-test.yaml`):
```yaml
test_name: "Frontend Developer v2 - Better Verification"
agent: frontend-developer
baseline_version: v1
test_version: v2
start_date: "2025-11-01"
duration_days: 14
traffic_split: 0.5  # 50% traffic to each version

hypothesis: "Adding explicit button-click verification will reduce false completions by 50%"

metrics:
  primary:
    - false_completion_rate
  secondary:
    - success_rate
    - avg_resolution_time
    - user_satisfaction

success_criteria:
  false_completion_rate:
    improvement_threshold: 0.5  # 50% reduction
    statistical_significance: 0.05  # p < 0.05

  sample_size_min: 30  # Need 30+ invocations per version

abort_conditions:
  - success_rate < 0.6  # If drops below 60%, abort test
  - user_complaints > 5  # If 5+ complaints, abort
```

### Running A/B Tests

**Implementation**:
- Main LLM randomly routes 50% traffic to each version
- Track metrics separately per version
- Weekly check-in on test progress

**Commands**:
```bash
# Start A/B test
oak-start-test frontend-developer-v2

# Check test status
oak-test-status frontend-developer-v2

# End test early (if clear winner or failure)
oak-end-test frontend-developer-v2 --reason "Clear improvement"

# Apply winning version
oak-apply-winner frontend-developer-v2
```

### Statistical Validation

**Script**: `scripts/phase4/validate_test.py`

**Analysis**:
```python
# Two-sample t-test for false completion rate
baseline_rate = [0.15, 0.12, 0.18, ...]  # 30 samples
test_rate = [0.08, 0.05, 0.10, ...]      # 30 samples

t_stat, p_value = stats.ttest_ind(baseline_rate, test_rate)

if p_value < 0.05 and mean(test_rate) < mean(baseline_rate):
    print("✅ Improvement is statistically significant")
    print(f"   Baseline: {mean(baseline_rate):.1%}")
    print(f"   Test: {mean(test_rate):.1%}")
    print(f"   Improvement: {(1 - mean(test_rate)/mean(baseline_rate))*100:.0f}%")
else:
    print("❌ No significant improvement")
```

**Output Report** (`reports/ab_tests/frontend-developer-v2-results.md`):
```markdown
# A/B Test Results: frontend-developer v2

## Summary
✅ **Test Succeeded** - Significant improvement detected

## Hypothesis
Adding explicit button-click verification will reduce false completions by 50%

## Results

| Metric | Baseline (v1) | Test (v2) | Change | Significant? |
|--------|---------------|-----------|--------|--------------|
| False Completion Rate | 15.2% | 7.8% | -48.7% | ✅ Yes (p=0.008) |
| Success Rate | 84.3% | 88.1% | +4.5% | ✅ Yes (p=0.032) |
| Avg Resolution Time | 25.3 min | 22.1 min | -12.6% | 🟡 No (p=0.12) |
| User Satisfaction | 4.1 | 4.3 | +4.9% | 🟡 No (p=0.18) |

## Sample Sizes
- Baseline: 42 invocations
- Test: 38 invocations
- Total: 80 invocations

## Recommendation
✅ **Deploy v2 to production**

v2 achieved the target 50% reduction in false completions with statistical significance. Secondary metrics show positive trends. No negative side effects detected.

## Next Steps
1. Deploy v2 as primary version
2. Archive v1 as `frontend-developer-v1.md`
3. Continue monitoring for 4 weeks
4. Update other agents with similar verification improvements
```

## Success Metrics: How We Know It's Working

### Primary Success Indicators

**1. False Completion Rate (Most Important)**
```
Target: <5% false completion rate per agent
Measurement: Weekly tracking
Success: Declining trend over 3 months
```

**2. First-Time Success Rate**
```
Target: >90% success rate on first attempt
Measurement: Weekly tracking
Success: Improving trend over 3 months
```

**3. User Satisfaction**
```
Target: Average rating >4.0/5.0
Measurement: Feedback prompts after resolution
Success: Stable or improving over time
```

**4. Time to Resolution**
```
Target: <48 hours from issue detected to resolved
Measurement: Issue lifecycle tracking
Success: Decreasing over time
```

### Secondary Success Indicators

**5. Improvement Velocity**
```
Metric: How fast do agents improve after updates?
Measurement: Success rate before vs after improvement applied
Success: >20% improvement within 2 weeks
```

**6. Learning Stability**
```
Metric: Do improvements stick or regress?
Measurement: Track metrics 4 weeks after improvement
Success: No regression (within 5% of improvement)
```

**7. Coverage**
```
Metric: What % of issues lead to improvements?
Measurement: Proposals generated / issues resolved
Success: >60% of issue patterns addressed
```

**8. System-Wide Health**
```
Metric: What % of agents are "green" (healthy)?
Measurement: Agent health dashboard
Success: >85% agents in green status
```

### User-Centric Success Metrics

**9. Rework Reduction**
```
Question: Am I asking less often for the same thing?
Measurement: Repeat request rate declining
Success: <5% repeat requests (was 15% before)
```

**10. Confidence in Agents**
```
Question: Do I trust agents will complete tasks correctly?
Measurement: User feedback + qualitative assessment
Success: Comfortable delegating without double-checking
```

### Dashboard View

**Monthly Success Report** (`reports/success_dashboard.html`):
```
┌─────────────────────────────────────────────────────────┐
│              System Success Dashboard - Oct 2025         │
├─────────────────────────────────────────────────────────┤
│ Overall Health: 🟢 GREEN                                 │
│ Trend: ↗️ IMPROVING                                      │
├─────────────────────────────────────────────────────────┤
│ Key Metrics                          Current | Target    │
├─────────────────────────────────────────────────────────┤
│ False Completion Rate                  4.2%  |  <5%  ✅  │
│ First-Time Success Rate               91.5%  |  >90% ✅  │
│ User Satisfaction                      4.3   |  >4.0 ✅  │
│ Avg Time to Resolution               36 hrs  |  <48h ✅  │
│                                                           │
│ Secondary Metrics                                         │
│ Improvement Velocity                  +28%   |  >20% ✅  │
│ Learning Stability                    98%    |  >95% ✅  │
│ Issue Coverage                         67%   |  >60% ✅  │
│ Agents in Green                        87%   |  >85% ✅  │
└─────────────────────────────────────────────────────────┘

🎯 8/8 targets met - System is successfully adapting!

Top Performers:
  1. frontend-developer: 95% success, 2% false completion
  2. backend-architect: 93% success, 3% false completion
  3. infrastructure-specialist: 91% success, 4% false completion

Recent Improvements:
  ✅ frontend-developer v2: -48% false completions
  ✅ backend-architect v3: -35% query timeouts
  🔄 security-auditor v2: A/B testing (early positive signals)

Upcoming:
  📋 3 improvement proposals ready for review
  🧪 2 A/B tests in progress
  📈 Trend: All metrics improving month-over-month
```

## Implementation Roadmap

### Phase 2: Root Cause Analysis (Month 1)
**Effort**: 2 weeks development + 2 weeks validation

**Deliverables**:
1. `scripts/phase2/analyze_root_causes.py` - Pattern detection script
2. `reports/improvement_proposals/` - Generated proposals
3. Review workflow commands (`oak-review-proposals`, etc.)
4. User documentation

**Success Criteria**:
- Generate first improvement proposals from real issues
- User successfully reviews and applies 1+ improvement
- Updated agent shows measurable improvement

### Phase 3: Metrics Tracking (Month 2)
**Effort**: 2 weeks development + 2 weeks dashboard creation

**Deliverables**:
1. `scripts/phase3/track_metrics.py` - Metrics collection
2. `scripts/phase3/analyze_trends.py` - Trend analysis
3. `reports/trends/*.html` - Interactive dashboards
4. Weekly/monthly metric summaries

**Success Criteria**:
- Metrics collected automatically from telemetry
- Trends visible in dashboard
- Can identify which agents are improving/declining

### Phase 4: A/B Testing (Month 3)
**Effort**: 3 weeks development + 1 week validation

**Deliverables**:
1. `scripts/phase4/setup_test.py` - A/B test configuration
2. `scripts/phase4/validate_test.py` - Statistical analysis
3. Main LLM routing integration (50/50 traffic split)
4. Test management commands

**Success Criteria**:
- Successfully run first A/B test
- Statistical validation shows clear winner
- Deploy improved agent version to production

### Phase 5: Continuous Learning (Month 4+)
**Effort**: Ongoing refinement

**Deliverables**:
- Automated pattern detection improvements
- Self-service improvement proposal generation
- Integration with agent-auditor for portfolio management
- ML-based performance prediction (future)

## Open Questions

1. **How often should we run root cause analysis?**
   - Proposal: Monthly during regular review
   - Alternative: Automatically when N issues resolved

2. **What's the minimum sample size for A/B tests?**
   - Proposal: 30 invocations per version (60 total)
   - Alternative: Dynamic based on variance

3. **Should improvements be auto-applied or require approval?**
   - Proposal: Always require human approval
   - Alternative: Auto-apply if confidence >90%

4. **How long should we track metrics after improvement?**
   - Proposal: 4 weeks post-deployment
   - Alternative: Until next improvement or 3 months

5. **What if A/B test shows no improvement?**
   - Proposal: Roll back, analyze why, try different approach
   - Alternative: Keep testing with modifications

## Next Steps

1. **Validate Design**: User review of this document
2. **Prioritize Phases**: Which phases to implement first?
3. **Build Phase 2**: Root cause analysis system
4. **Collect Real Data**: Run system for 2-4 weeks to accumulate issues
5. **First Improvement Cycle**: Apply first agent improvement and measure impact

---

**Status**: 🚧 Design Phase - Awaiting User Feedback

**Last Updated**: 2025-10-21
