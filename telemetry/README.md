# Telemetry System

This directory contains the telemetry infrastructure for the Claude OaK Agents system.

## Overview

The telemetry system logs all agent invocations and success metrics to enable:
- Performance tracking over time
- Agent success rate analysis
- Data-driven agent improvements
- Offline reinforcement learning (future)

## Files

- **agent_invocations.jsonl** - Log of all agent invocations with state features and outcomes
- **success_metrics.jsonl** - Human and automated feedback on agent performance
- **performance_stats.json** - Aggregated statistics (generated from logs)
- **schemas.json** - JSON schemas for all telemetry data structures
- **logger.py** - Python utilities for logging telemetry
- **analyzer.py** - Python utilities for analyzing telemetry

## Quick Start

### 1. Logging Agent Invocations

```python
from telemetry.logger import TelemetryLogger

logger = TelemetryLogger()

# Start of agent execution
invocation_id = logger.log_invocation(
    agent_name="frontend-developer",
    agent_type="development",
    task_description="Add dark mode toggle",
    state_features={
        "codebase": {"languages": ["TypeScript"]},
        "task": {"type": "feature_development", "scope": "small"}
    }
)

# End of agent execution
logger.update_invocation(
    invocation_id=invocation_id,
    duration_seconds=120.5,
    outcome_status="success",
    files_modified=["src/Settings.tsx"]
)

# Log feedback
logger.log_success_metric(
    invocation_id=invocation_id,
    success=True,
    quality_rating=4,
    feedback_notes="Works well!"
)
```

### 2. Analyzing Telemetry

```bash
# Generate statistics and print summary
python telemetry/analyzer.py

# Or from Python
from telemetry.analyzer import TelemetryAnalyzer

analyzer = TelemetryAnalyzer()
analyzer.save_statistics()  # Writes to performance_stats.json
analyzer.print_summary()     # Prints to console

# Get agent rankings
rankings = analyzer.get_agent_ranking(task_type="feature_development")
```

## Integration with Agents

### Manual Integration (Phase 1)

For now, telemetry logging is manual. When invoking an agent:

1. Create a telemetry logger instance
2. Log invocation at start
3. Log outcome at completion
4. Optionally collect human feedback

### Automated Integration (Future)

Future phases will add:
- Hooks that automatically log invocations
- Automated outcome detection (tests, builds)
- Inline feedback prompts
- Real-time dashboard

## Data Schema

### AgentInvocation

```json
{
  "timestamp": "2025-10-16T14:30:00Z",
  "session_id": "uuid",
  "invocation_id": "uuid",
  "agent_name": "frontend-developer",
  "agent_type": "development",
  "task_description": "Add dark mode",
  "state_features": {
    "codebase": {...},
    "task": {...},
    "context": {...},
    "historical": {...}
  },
  "outcome": {
    "status": "success",
    "files_modified": [...]
  }
}
```

### SuccessMetric

```json
{
  "timestamp": "2025-10-16T14:32:00Z",
  "invocation_id": "uuid",
  "success": true,
  "quality_rating": 4,
  "feedback_source": "human",
  "feedback_notes": "Works well but needs polish"
}
```

See `schemas.json` for complete schemas.

## Best Practices

### 1. Always Log State Features

The more context you capture, the better ML models can learn patterns:

```python
state_features = {
    "codebase": {
        "languages": ["Python", "JavaScript"],
        "frameworks": ["FastAPI", "React"],
        "loc": 15000,
        "file_count": 120
    },
    "task": {
        "type": "bug_fix",
        "scope": "medium",
        "risk_level": "high"
    },
    "context": {
        "tests_exist": True,
        "docs_exist": False,
        "git_clean": True
    }
}
```

### 2. Provide Quality Ratings

When rating agent performance:
- **5**: Excellent - exactly what was needed, no issues
- **4**: Good - accomplished task with minor issues
- **3**: Acceptable - completed but required significant fixes
- **2**: Poor - major issues, required extensive rework
- **1**: Failed - did not accomplish the task

### 3. Suggest Alternatives

If an agent wasn't the best choice, specify which would have been better:

```python
logger.log_success_metric(
    invocation_id=invocation_id,
    success=False,
    quality_rating=2,
    would_use_again=False,
    alternative_agent_suggested="backend-architect"
)
```

### 4. Regular Analysis

Run the analyzer weekly to:
- Identify underperforming agents
- Discover usage patterns
- Guide agent improvements

```bash
# Weekly analysis
python telemetry/analyzer.py > weekly_report.txt
```

## Privacy & Security

- Telemetry logs are stored **locally only**
- No data is sent to external services
- Logs may contain code snippets and file paths
- Add telemetry files to `.gitignore` if they contain sensitive data

## Future Enhancements

- [ ] Automated hooks for invocation logging
- [ ] Real-time dashboard (web UI)
- [ ] Export to PostgreSQL for analysis
- [ ] Integration with ML pipeline
- [ ] A/B testing framework
- [ ] Anomaly detection
