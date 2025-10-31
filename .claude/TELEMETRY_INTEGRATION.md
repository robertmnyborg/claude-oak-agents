# Telemetry & Analytics Integration Guide

**Version**: 1.0.0
**Last Updated**: 2025-10-30
**Purpose**: Integration guide for agent auto-activation with existing telemetry system

---

## Overview

The agent auto-activation system integrates with your existing telemetry infrastructure to:
1. Track agent activation patterns
2. Measure agent performance and success rates
3. Learn from user acceptance/rejection of suggestions
4. Continuously improve activation thresholds and patterns
5. Provide analytics dashboards for system optimization

---

## Architecture

```
User Request
    ↓
[agent-activation-prompt.md hook]
    ├─ Analyzes keywords, file context, patterns
    ├─ Matches against agent-rules.json
    ├─ Suggests agents to user
    ├─ Logs suggestion to telemetry ──────────┐
    ↓                                          │
User Decision (Accept/Reject)                 │
    ├─ Logs acceptance/rejection ─────────────┤
    ↓                                          │
Agent Execution (if accepted)                 │
    ├─ Agent performs task                    │
    ├─ [post-agent-execution.md hook]         │
    ├─ Logs execution results ────────────────┤
    ↓                                          ├─→ Telemetry System
Quality Gates                                  │      ↓
    ├─ Code review, security audit            │   Analytics Engine
    ├─ [pre-commit-validation.md hook]        │      ↓
    ├─ Logs validation results ───────────────┤   Learning System
    ↓                                          │      ↓
Commit Success/Failure                         │   Updated Rules
    └─ Final outcome logged ──────────────────┘      ↓
                                              agent-rules.json
```

---

## Telemetry Schema Extensions

### New Event Types

#### 1. Agent Suggestion Event
```json
{
  "event_type": "agent_suggestion",
  "event_id": "sug-20251030-<uuid>",
  "timestamp": "2025-10-30T12:34:56.789Z",
  "user_request": "<sanitized-user-prompt>",
  "keywords_matched": ["authentication", "API", "security"],
  "file_context": ["src/auth/handler.ts", "src/api/routes.ts"],
  "suggested_agents": [
    {
      "agent_name": "backend-architect",
      "confidence": 0.87,
      "trigger_reasons": ["keywords: API, authentication", "files: **/*auth*"],
      "priority": "high"
    },
    {
      "agent_name": "security-auditor",
      "confidence": 0.92,
      "trigger_reasons": ["keywords: security, authentication", "files: auth/**"],
      "priority": "critical"
    }
  ],
  "user_decision": "accepted",  # or "rejected", "ignored"
  "agents_accepted": ["backend-architect", "security-auditor"],
  "decision_time_ms": 3421
}
```

#### 2. Agent Invocation Event (Enhanced)
```json
{
  "event_type": "agent_invocation",
  "invocation_id": "inv-20251030-<uuid>",
  "suggestion_id": "sug-20251030-<uuid>",  # Links to suggestion
  "workflow_id": "wf-20251030-<uuid>",
  "parent_invocation_id": "inv-20251030-<parent-uuid>",
  "timestamp": "2025-10-30T12:35:00.123Z",
  "agent_name": "backend-architect",
  "task_description": "<task-summary>",
  "trigger_source": "auto_activation",  # or "manual", "workflow"
  "model_tier": "sonnet",
  "status": "success",  # or "failure", "partial"
  "execution_time_ms": 12456,
  "tools_used": ["Write", "Read", "Grep"],
  "files_modified": ["src/auth/oauth.ts", "src/auth/types.ts"],
  "lines_added": 145,
  "lines_deleted": 23,
  "error_message": null,
  "user_feedback": {
    "accepted": true,
    "corrections_needed": false,
    "follow_up_invocations": []
  }
}
```

#### 3. Validation Event
```json
{
  "event_type": "validation",
  "validation_id": "val-20251030-<uuid>",
  "workflow_id": "wf-20251030-<uuid>",
  "timestamp": "2025-10-30T12:36:00.456Z",
  "validation_type": "pre_commit",  # or "code_review", "security_audit"
  "triggered_by": "git commit",
  "files_validated": ["src/auth/oauth.ts", "src/auth/types.ts"],
  "validators_run": [
    {
      "agent_name": "code-reviewer",
      "status": "pass",
      "issues_found": {"critical": 0, "medium": 1, "low": 2},
      "execution_time_ms": 2341
    },
    {
      "agent_name": "security-auditor",
      "status": "pass_with_warnings",
      "issues_found": {"critical": 0, "medium": 1, "low": 0},
      "execution_time_ms": 1876
    }
  ],
  "overall_result": "passed",
  "blocking_issues": 0,
  "total_execution_time_ms": 4217
}
```

#### 4. Workflow Summary Event
```json
{
  "event_type": "workflow_summary",
  "workflow_id": "wf-20251030-<uuid>",
  "timestamp_start": "2025-10-30T12:34:00.000Z",
  "timestamp_end": "2025-10-30T12:40:15.789Z",
  "duration_total_ms": 375789,
  "user_request": "<original-request>",
  "classification": "IMPLEMENTATION",
  "domains": ["Backend", "Security"],
  "agents_suggested": ["backend-architect", "security-auditor"],
  "agents_executed": ["backend-architect", "security-auditor", "code-reviewer"],
  "execution_sequence": [
    "backend-architect",
    "security-auditor",  # parallel
    "code-reviewer"
  ],
  "outcome": "success",  # or "failure", "partial", "abandoned"
  "final_status": {
    "files_modified": 2,
    "lines_changed": 168,
    "tests_added": true,
    "committed": true,
    "pr_created": false
  },
  "user_satisfaction_proxy": {
    "no_corrections_needed": true,
    "no_re_runs": true,
    "commit_without_changes": true
  }
}
```

---

## Storage Structure

```
telemetry/
├── suggestions/
│   └── 2025-10-30/
│       ├── sug-20251030-<uuid>.json
│       └── ...
├── invocations/
│   └── 2025-10-30/
│       ├── inv-20251030-<uuid>.json
│       └── ...
├── validations/
│   └── 2025-10-30/
│       ├── val-20251030-<uuid>.json
│       └── ...
├── workflows/
│   └── 2025-10-30/
│       ├── wf-20251030-<uuid>.json
│       └── ...
└── analytics/
    ├── agent_performance.json
    ├── suggestion_acceptance.json
    ├── workflow_efficiency.json
    └── learning_metrics.json
```

---

## Analytics Queries

### 1. Agent Suggestion Acceptance Rate

**Query**: What percentage of agent suggestions does the user accept?

```python
# scripts/analytics/suggestion_acceptance_rate.py
def calculate_acceptance_rate(date_range):
    suggestions = load_suggestions(date_range)

    total = len(suggestions)
    accepted = sum(1 for s in suggestions if s['user_decision'] == 'accepted')
    rejected = sum(1 for s in suggestions if s['user_decision'] == 'rejected')
    ignored = sum(1 for s in suggestions if s['user_decision'] == 'ignored')

    return {
        'total_suggestions': total,
        'accepted': accepted,
        'accepted_rate': accepted / total,
        'rejected': rejected,
        'rejected_rate': rejected / total,
        'ignored': ignored,
        'ignored_rate': ignored / total,
        'by_agent': calculate_by_agent(suggestions)
    }
```

**Output Example**:
```json
{
  "period": "2025-10-01 to 2025-10-30",
  "total_suggestions": 147,
  "accepted": 112,
  "accepted_rate": 0.76,
  "rejected": 23,
  "rejected_rate": 0.16,
  "ignored": 12,
  "ignored_rate": 0.08,
  "by_agent": {
    "backend-architect": {"suggestions": 45, "accepted": 38, "rate": 0.84},
    "security-auditor": {"suggestions": 38, "accepted": 36, "rate": 0.95},
    "frontend-developer": {"suggestions": 32, "accepted": 22, "rate": 0.69}
  }
}
```

### 2. Agent Performance Metrics

**Query**: Which agents have highest success rates and fastest execution?

```python
# scripts/analytics/agent_performance.py
def analyze_agent_performance(date_range):
    invocations = load_invocations(date_range)

    by_agent = group_by_agent(invocations)

    results = {}
    for agent_name, agent_invocations in by_agent.items():
        total = len(agent_invocations)
        successful = sum(1 for inv in agent_invocations if inv['status'] == 'success')
        failed = sum(1 for inv in agent_invocations if inv['status'] == 'failure')

        avg_time = statistics.mean([inv['execution_time_ms'] for inv in agent_invocations])

        results[agent_name] = {
            'total_invocations': total,
            'success_count': successful,
            'success_rate': successful / total,
            'failure_count': failed,
            'failure_rate': failed / total,
            'avg_execution_time_ms': avg_time,
            'median_execution_time_ms': statistics.median([inv['execution_time_ms'] for inv in agent_invocations])
        }

    return results
```

**Output Example**:
```json
{
  "backend-architect": {
    "total_invocations": 45,
    "success_count": 42,
    "success_rate": 0.93,
    "failure_count": 3,
    "failure_rate": 0.07,
    "avg_execution_time_ms": 8234,
    "median_execution_time_ms": 7456
  },
  "debug-specialist": {
    "total_invocations": 18,
    "success_count": 18,
    "success_rate": 1.00,
    "failure_count": 0,
    "failure_rate": 0.00,
    "avg_execution_time_ms": 3421,
    "median_execution_time_ms": 3102
  }
}
```

### 3. Workflow Efficiency Analysis

**Query**: How long do different workflow types take? Which are most successful?

```python
# scripts/analytics/workflow_efficiency.py
def analyze_workflow_efficiency(date_range):
    workflows = load_workflows(date_range)

    by_classification = group_by_classification(workflows)

    results = {}
    for classification, class_workflows in by_classification.items():
        total = len(class_workflows)
        successful = sum(1 for wf in class_workflows if wf['outcome'] == 'success')

        avg_duration = statistics.mean([wf['duration_total_ms'] for wf in class_workflows])
        avg_agents = statistics.mean([len(wf['agents_executed']) for wf in class_workflows])

        results[classification] = {
            'total_workflows': total,
            'success_count': successful,
            'success_rate': successful / total,
            'avg_duration_ms': avg_duration,
            'avg_agents_used': avg_agents,
            'most_common_agents': find_most_common_agents(class_workflows)
        }

    return results
```

**Output Example**:
```json
{
  "IMPLEMENTATION": {
    "total_workflows": 67,
    "success_count": 61,
    "success_rate": 0.91,
    "avg_duration_ms": 234567,
    "avg_agents_used": 3.2,
    "most_common_agents": ["backend-architect", "code-reviewer", "security-auditor"]
  },
  "DEBUGGING": {
    "total_workflows": 23,
    "success_count": 23,
    "success_rate": 1.00,
    "avg_duration_ms": 45678,
    "avg_agents_used": 1.3,
    "most_common_agents": ["debug-specialist", "backend-architect"]
  }
}
```

### 4. Learning Metrics (Confidence Threshold Optimization)

**Query**: Should we adjust confidence thresholds based on acceptance patterns?

```python
# scripts/analytics/learning_metrics.py
def recommend_threshold_adjustments(date_range):
    suggestions = load_suggestions(date_range)

    recommendations = []

    for agent_name in get_all_agents():
        agent_suggestions = [s for s in suggestions if agent_name in [a['agent_name'] for a in s['suggested_agents']]]

        # Group by confidence buckets
        high_conf = [s for s in agent_suggestions if get_confidence(s, agent_name) >= 0.80]
        med_conf = [s for s in agent_suggestions if 0.65 <= get_confidence(s, agent_name) < 0.80]
        low_conf = [s for s in agent_suggestions if get_confidence(s, agent_name) < 0.65]

        # Calculate acceptance rates by confidence
        high_acceptance = sum(1 for s in high_conf if was_accepted(s, agent_name)) / len(high_conf) if high_conf else 0
        med_acceptance = sum(1 for s in med_conf if was_accepted(s, agent_name)) / len(med_conf) if med_conf else 0
        low_acceptance = sum(1 for s in low_conf if was_accepted(s, agent_name)) / len(low_conf) if low_conf else 0

        # Recommend threshold adjustments
        current_threshold = get_current_threshold(agent_name)

        if high_acceptance < 0.70:
            recommendations.append({
                'agent': agent_name,
                'action': 'INCREASE_THRESHOLD',
                'current': current_threshold,
                'recommended': current_threshold + 0.05,
                'reason': f'High confidence suggestions only {high_acceptance:.0%} accepted'
            })
        elif med_acceptance > 0.85:
            recommendations.append({
                'agent': agent_name,
                'action': 'DECREASE_THRESHOLD',
                'current': current_threshold,
                'recommended': max(0.60, current_threshold - 0.05),
                'reason': f'Medium confidence suggestions {med_acceptance:.0%} accepted'
            })

    return recommendations
```

**Output Example**:
```json
{
  "analysis_period": "2025-10-01 to 2025-10-30",
  "recommendations": [
    {
      "agent": "frontend-developer",
      "action": "INCREASE_THRESHOLD",
      "current": 0.75,
      "recommended": 0.80,
      "reason": "High confidence suggestions only 69% accepted",
      "impact": "Reduce false positive suggestions"
    },
    {
      "agent": "debug-specialist",
      "action": "DECREASE_THRESHOLD",
      "current": 0.70,
      "recommended": 0.65,
      "reason": "Medium confidence suggestions 91% accepted",
      "impact": "Catch more debugging opportunities"
    }
  ],
  "no_changes_needed": ["backend-architect", "security-auditor", "code-reviewer"]
}
```

---

## Dashboard Queries

### Monthly Agent Performance Dashboard

```bash
# scripts/dashboards/monthly_agent_performance.sh

#!/bin/bash
DATE_START="2025-10-01"
DATE_END="2025-10-31"

python scripts/analytics/agent_performance.py --start=$DATE_START --end=$DATE_END --format=table

# Output:
# Agent Performance Report - October 2025
# ==========================================
# Agent                    | Invocations | Success Rate | Avg Time (s) | Rank
# -------------------------|-------------|--------------|--------------|------
# debug-specialist         |          18 |       100.0% |         3.4s |    ⭐
# security-auditor         |          36 |        97.2% |         4.2s |    ⭐
# backend-architect        |          45 |        93.3% |         8.2s |    🟢
# frontend-developer       |          32 |        87.5% |         6.7s |    🟢
# code-reviewer            |          52 |        86.5% |         3.1s |    🟢
# infrastructure-specialist|          23 |        82.6% |        11.3s |    🟡
# project-manager          |           8 |        75.0% |        45.2s |    🟡
```

### Weekly Suggestion Acceptance Trend

```bash
# scripts/dashboards/weekly_suggestion_trend.sh

#!/bin/bash
WEEKS=4

python scripts/analytics/suggestion_acceptance_rate.py --weeks=$WEEKS --format=chart

# Output (ASCII chart):
# Suggestion Acceptance Rate - Last 4 Weeks
# ==========================================
# 100% ┤
#  90% ┤        ●────●
#  80% ┤    ●───┘    └───●
#  70% ┤
#  60% ┤
#      └────────────────────────────
#       W1   W2   W3   W4
#
# Trend: Stable at 85-90% acceptance
```

---

## Automated Learning System

### Threshold Auto-Adjustment

```python
# automation/auto_adjust_thresholds.py

#!/usr/bin/env python3
"""
Automatically adjusts agent-rules.json confidence thresholds based on telemetry data.
Runs weekly as a cron job.
"""

import json
from scripts.analytics.learning_metrics import recommend_threshold_adjustments

def auto_adjust_thresholds():
    # Get recommendations from last 30 days
    recommendations = recommend_threshold_adjustments(days=30)

    # Load current rules
    with open('.claude/agent-rules.json', 'r') as f:
        rules = json.load(f)

    # Apply recommendations
    changes_made = []
    for rec in recommendations['recommendations']:
        agent = rec['agent']
        new_threshold = rec['recommended']

        # Find agent in rules
        for agent_config in rules['agents']:
            if agent_config['name'] == agent:
                old_threshold = agent_config['confidence_threshold']
                agent_config['confidence_threshold'] = new_threshold
                changes_made.append({
                    'agent': agent,
                    'old': old_threshold,
                    'new': new_threshold,
                    'reason': rec['reason']
                })

    # Save updated rules
    if changes_made:
        with open('.claude/agent-rules.json', 'w') as f:
            json.dump(rules, f, indent=2)

        # Log changes
        log_threshold_adjustments(changes_made)

        print(f"✅ Adjusted thresholds for {len(changes_made)} agents")
        for change in changes_made:
            print(f"  - {change['agent']}: {change['old']:.2f} → {change['new']:.2f}")
            print(f"    Reason: {change['reason']}")
    else:
        print("✅ No threshold adjustments needed")

if __name__ == '__main__':
    auto_adjust_thresholds()
```

### Cron Job Setup

```bash
# Add to crontab (run every Monday at 2am)
0 2 * * 1 cd /Users/robertnyborg/Projects/claude-oak-agents && python automation/auto_adjust_thresholds.py
```

---

## Integration with Existing Telemetry

Your system already has:
- `telemetry/logger.py` - Logging infrastructure
- `telemetry/workflow.py` - Workflow ID generation
- `scripts/query_workflow.sh` - Workflow queries

**Extensions needed**:

1. **Add new event types** to `telemetry/logger.py`:
```python
def log_suggestion(suggestion_data):
    """Log agent suggestion event"""
    event_file = f"telemetry/suggestions/{date}/sug-{id}.json"
    write_json(event_file, suggestion_data)

def log_validation(validation_data):
    """Log validation event"""
    event_file = f"telemetry/validations/{date}/val-{id}.json"
    write_json(event_file, validation_data)
```

2. **Extend invocation logging** to include suggestion_id:
```python
def log_invocation(agent_name, task_description, status, suggestion_id=None, **kwargs):
    # ... existing code ...
    data['suggestion_id'] = suggestion_id  # NEW
    # ... rest of logging
```

3. **Add analytics scripts** (shown above in Analytics Queries section)

4. **Create dashboard scripts** (shown above in Dashboard Queries section)

5. **Set up automated learning** (shown above in Automated Learning System section)

---

## Privacy & Security

### Data to Sanitize
- User prompts (remove PII, secrets, credentials)
- File paths (optionally anonymize)
- Error messages (remove sensitive context)

### Data Retention
- Raw telemetry: 90 days
- Aggregated analytics: 1 year
- Learning metrics: Indefinite

### Access Control
- Telemetry files: User-only access
- Analytics dashboards: Readable by team
- Learning system: Automated, no manual intervention needed

---

## Next Steps

1. **Implement logging extensions** in existing `telemetry/logger.py`
2. **Create analytics scripts** in `scripts/analytics/`
3. **Build dashboard scripts** in `scripts/dashboards/`
4. **Set up automated learning** in `automation/auto_adjust_thresholds.py`
5. **Configure cron job** for weekly threshold adjustments
6. **Monitor and iterate** based on real-world usage data

---

## Success Metrics

Track these KPIs monthly:

1. **Suggestion Quality**:
   - Target: >80% acceptance rate
   - Current baseline: TBD (measure after 30 days)

2. **Agent Performance**:
   - Target: >90% success rate for high-priority agents
   - Current baseline: TBD

3. **Workflow Efficiency**:
   - Target: <5 minutes for simple workflows
   - Target: <30 minutes for complex workflows
   - Current baseline: TBD

4. **Learning System Effectiveness**:
   - Target: Improve acceptance rate by 10% in 6 months
   - Target: Reduce false positive suggestions by 15% in 6 months

---

**For complete telemetry documentation, see**:
- Existing telemetry: `/telemetry/README.md` (if exists)
- Workflow tracking: `CLAUDE.md` Phase 2A section
- Agent patterns: `.claude/AGENT_PATTERNS.md`
