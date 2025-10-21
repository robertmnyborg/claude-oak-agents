# False Completion Detection Script

## Overview

Automatically detects when agents claim successful completion but the user had to repeat the same request, indicating a quality issue.

## How It Works

### Detection Heuristic

The script uses a simple but effective heuristic:

1. **Extract Keywords**: Remove stopwords from task descriptions
2. **Group by Agent**: Analyze each agent's invocations separately
3. **Find Repetitions**: Look for tasks with 2+ keyword overlap within 24-hour window
4. **Check Success Status**: Earlier attempt must have claimed "success"
5. **Flag as False Completion**: If user had to repeat after success → quality issue

### Example

```
10:00 AM - User: "Fix navigation component crash"
          Agent: Claims success
12:00 PM - User: "Fix crash in navigation component" (same keywords!)
          Agent: Claims success  
02:00 PM - User: "Navigation component still crashing"
          Agent: Claims success

DETECTION: False completion (3 repetitions in 4 hours)
```

## Usage

### Basic Run (Production)

```bash
python3 scripts/detect_false_completions.py
```

Analyzes `telemetry/agent_invocations.jsonl` and appends findings to `telemetry/agent_reviews.jsonl`.

### Dry Run (Test Mode)

```bash
python3 scripts/detect_false_completions.py --dry-run
```

Shows what would be detected without writing to files.

## Configuration

Edit script constants to tune detection sensitivity:

```python
MIN_KEYWORD_OVERLAP = 2   # Minimum matching keywords
MIN_REPETITIONS = 2       # Minimum repetitions to flag
TIME_WINDOW_HOURS = 24    # Time window for repetitions
```

### Stopwords

Common words ignored during keyword extraction:

```python
STOPWORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can',
    'make', 'fix', 'update', 'change', 'add', 'create', 'build'
}
```

## Output Format

Appends to `telemetry/agent_reviews.jsonl`:

```json
{
  "timestamp": "2025-10-21T12:34:56.789Z",
  "agent_name": "frontend-developer",
  "action": "auto_detected_false_completion",
  "reasoning": "Agent claimed success but user requested similar task 3 times in 4.5 hours",
  "category": "quality_issue",
  "reviewer": "system",
  "evidence": {
    "repetition_count": 3,
    "keywords": ["component", "crash", "navigation"],
    "time_span_hours": 4.5,
    "attempts": [
      {
        "timestamp": "2025-10-21T10:00:00Z",
        "outcome": "success",
        "task": "Fix navigation component crash on mobile"
      },
      {
        "timestamp": "2025-10-21T12:00:00Z",
        "outcome": "success",
        "task": "Fix crash in navigation component mobile view"
      },
      {
        "timestamp": "2025-10-21T14:30:00Z",
        "outcome": "success",
        "task": "Navigation component still crashing on mobile"
      }
    ]
  }
}
```

## Integration

### Manual Execution

Run weekly or after deployments:

```bash
python3 scripts/detect_false_completions.py
```

### Automated Execution (Cron)

Add to crontab for daily checks:

```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/claude-oak-agents && python3 scripts/detect_false_completions.py
```

### Integration with Weekly Review

Can be called from `weekly_review.py` (optional enhancement):

```python
import subprocess

def run_false_completion_detection():
    """Run false completion detection as part of weekly review."""
    subprocess.run([
        'python3',
        'scripts/detect_false_completions.py'
    ], check=True)
```

## Testing

The script includes validation logic. Test with simulated data:

```python
from detect_false_completions import extract_keywords, calculate_overlap, is_false_completion

# Test keyword extraction
keywords = extract_keywords("Fix navigation component crash")
assert 'navigation' in keywords
assert 'crash' in keywords

# Test overlap calculation
overlap = calculate_overlap({'crash', 'nav'}, {'crash', 'fix'})
assert overlap == 1  # 'crash' overlaps

# Test false completion logic
attempts = [
    {'outcome': {'status': 'success'}},
    {'outcome': {'status': 'success'}}
]
assert is_false_completion(attempts) == True
```

## Limitations

### Known Edge Cases

1. **Legitimate Iterations**: User refining requirements may look like false completion
2. **Different Users**: Multiple users asking similar questions counted as repetitions
3. **Complex Tasks**: Multi-step tasks broken into similar subtasks may trigger false positives
4. **Keyword Matching**: Simple word matching can miss semantic similarity

### Future Enhancements

- Track user_id to distinguish between different users
- Use semantic similarity (embeddings) instead of keyword matching
- Add machine learning to improve detection accuracy
- Integrate with session_id for better context grouping

## Troubleshooting

### No Detections

```bash
Analyzing 100 invocations...
No false completions detected.
```

**Possible reasons**:
- Agents are working correctly
- Time window too narrow (increase `TIME_WINDOW_HOURS`)
- Keyword overlap threshold too strict (decrease `MIN_KEYWORD_OVERLAP`)
- Not enough repetitions yet (decrease `MIN_REPETITIONS`)

### Too Many Detections

If getting excessive false positives:
- Increase `MIN_KEYWORD_OVERLAP` (require more matching keywords)
- Increase `MIN_REPETITIONS` (require more attempts)
- Decrease `TIME_WINDOW_HOURS` (shorter time window)
- Add more stopwords to filter common technical terms

## Design Philosophy

Follows KISS (Keep It Simple, Stupid) principles from design-simplicity-advisor:

- **Simple heuristic**: Keyword matching instead of ML/AI
- **Minimal dependencies**: Uses only Python stdlib
- **Clear logic**: Each function does one thing
- **Easy to understand**: ~100 lines total
- **Easy to modify**: Configuration via constants
- **Standalone**: No changes to existing code

## Files

- **Script**: `/Users/robertnyborg/Projects/claude-oak-agents/scripts/detect_false_completions.py`
- **Input**: `/Users/robertnyborg/Projects/claude-oak-agents/telemetry/agent_invocations.jsonl`
- **Output**: `/Users/robertnyborg/Projects/claude-oak-agents/telemetry/agent_reviews.jsonl`
- **This README**: `/Users/robertnyborg/Projects/claude-oak-agents/scripts/detect_false_completions_README.md`
