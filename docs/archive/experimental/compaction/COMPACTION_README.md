# Context Compression Utility

Simple utility for compressing verbose agent outputs into concise summaries for efficient handoffs.

## Overview

Agent outputs can be extremely verbose (1000-5000 lines). When passing context between agents, we need compressed summaries that preserve critical information while reducing token usage.

**Compression Targets**:
- Research: 2000 lines → ~100 lines (20x compression)
- Plans: 1000 lines → ~50 lines (20x compression)  
- Implementation: 5000 lines → ~100 lines (50x compression)

## Usage

### Basic Usage

```python
from core.compaction import compact_output

# Full agent output
full_research = """
[2000 lines of detailed technical analysis]
"""

# Compress for next agent
compressed = compact_output(full_research, "research")

# Save both versions
save("artifacts/agent/full-analysis.md", full_research)
save("artifacts/agent/summary.md", compressed)  # Pass this to next agent
```

### Artifact Types

Supported artifact types:
- `research` - Research and analysis outputs
- `plan` - Planning and architecture documents
- `implementation` - Code implementation summaries
- `analysis` - Technical analysis reports
- `design` - Design specifications

## How It Works

### Heuristic Compression (Default)

Uses simple pattern matching to extract:
1. **Overview** - First paragraph (2-3 sentences)
2. **Key Findings** - Headers, bullet points, numbered lists (max 5)
3. **Files Created** - All file paths mentioned
4. **Next Steps** - Extracted from "Next Steps", "TODO", "Recommendations" sections

### Claude API Compression (Optional)

If `ANTHROPIC_API_KEY` environment variable is set and `anthropic` package is installed:
- Uses Claude API for intelligent summarization
- Automatically falls back to heuristics if API fails
- More accurate extraction of key information

## Output Format

All compressed outputs follow this structure:

```markdown
# [Type] Summary

## Overview
Brief 2-3 sentence overview of the work completed.

## Key Findings
- Finding 1
- Finding 2
- Finding 3
- Finding 4
- Finding 5

## Files Created
- path/to/file1.ts
- path/to/file2.ts
- path/to/file3.py

## What's Next
Next steps or guidance for following agent.
```

## Integration with Agent Workflows

### Single Agent Completion

```python
# Agent completes work
full_output = agent.execute(task)

# Compress for handoff
summary = compact_output(full_output, artifact_type)

# Store both
artifacts = {
    "full": full_output,
    "summary": summary
}

# Next agent receives summary only
next_agent.execute(task, context=artifacts["summary"])
```

### Multi-Agent Workflow

```python
# Research agent
research_full = research_agent.execute()
research_summary = compact_output(research_full, "research")

# Planning agent (receives summary)
plan_full = planning_agent.execute(context=research_summary)
plan_summary = compact_output(plan_full, "plan")

# Implementation agent (receives summary)
impl_full = impl_agent.execute(context=plan_summary)
impl_summary = compact_output(impl_full, "implementation")
```

## Configuration

### Environment Variables

```bash
# Optional: Enable Claude API compression
export ANTHROPIC_API_KEY="your-api-key"
```

### Dependencies

**Minimal** (heuristic compression only):
- Python 3.7+
- No external dependencies (uses stdlib only)

**Enhanced** (Claude API compression):
- Python 3.7+
- `anthropic` package: `pip install anthropic`

## Testing

Run the test suite:

```bash
cd core
python3 test_compaction.py
```

Expected output shows compression ratios and sample outputs.

## Performance

**Heuristic Compression**:
- Speed: ~10ms for 2000 line document
- Cost: Free
- Quality: Good for structured markdown

**Claude API Compression**:
- Speed: ~1-2s per compression
- Cost: ~$0.001 per compression
- Quality: Excellent for any format

## Limitations

**Current Implementation**:
- Markdown-optimized (works best with well-structured markdown)
- Simple pattern matching (may miss context-dependent importance)
- Fixed summary structure
- No token counting (yet)

**Future Enhancements** (Phase 2+):
- Token-aware compression (tiktoken integration)
- Configurable compression ratios
- Domain-specific extraction (code vs docs vs research)
- Quality scoring of compression

## Design Philosophy

**Keep It Simple**:
- Single function call, no configuration
- Graceful degradation (API → heuristics)
- No error handling required by caller
- Works out of the box

**No Over-Engineering**:
- No classes, just functions
- No validation frameworks
- No configuration files
- Trust the input

This is Phase 1 validation - minimal viable implementation.
