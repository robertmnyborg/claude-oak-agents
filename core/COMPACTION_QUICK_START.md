# Compaction Quick Start

One-function context compression for agent handoffs.

## Installation

No installation needed - uses Python stdlib only.

**Optional**: For Claude API compression
```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-key"
```

## Usage

```python
from core.compaction import compact_output

# Compress any agent output
compressed = compact_output(full_text, artifact_type)
```

## Example

```python
# Agent produces verbose output
research = """
# Long Analysis
[2000 lines of detailed research]
"""

# Compress for next agent
summary = compact_output(research, "research")

# Pass compressed version to next agent
next_agent.execute(context=summary)
```

## Artifact Types

- `research` - Research and analysis
- `plan` - Planning documents
- `implementation` - Code implementations
- `analysis` - Technical analysis
- `design` - Design specifications

## Compression Ratios

- Research: 2000 lines → ~100 lines (20x)
- Plans: 1000 lines → ~50 lines (20x)
- Implementation: 5000 lines → ~100 lines (50x)

## Output Format

```markdown
# [Type] Summary

## Overview
Brief 2-3 sentence summary.

## Key Findings
- Point 1
- Point 2
- Point 3

## Files Created
- file1.ts
- file2.py

## What's Next
Next steps for following agent.
```

## Testing

```bash
cd core
python3 test_compaction.py
```

## How It Works

1. **With API Key**: Uses Claude API for intelligent compression
2. **Without API Key**: Falls back to heuristic pattern matching
3. **Always Works**: Graceful degradation, no errors

## When to Use

**Use compression when**:
- Passing context between agents
- Agent output > 500 lines
- Reducing token usage
- Preserving only critical info

**Use full output when**:
- Final user deliverable
- Detailed documentation needed
- Complete audit trail required

## Pro Tips

**Save Both Versions**:
```python
# Full version for archive
save("artifacts/full-output.md", full_text)

# Compressed for handoff
summary = compact_output(full_text, "research")
save("artifacts/summary.md", summary)
```

**Chain Compressions**:
```python
# Multi-agent workflow
r_summary = compact_output(research, "research")
p_summary = compact_output(plan, "plan")
i_summary = compact_output(impl, "implementation")
```

**Check Savings**:
```python
original_tokens = len(full_text) // 4  # Rough estimate
compressed_tokens = len(compressed) // 4
savings = original_tokens - compressed_tokens
print(f"Saved ~{savings} tokens")
```

## Limitations

- Optimized for markdown (works best with headers, bullets, lists)
- Fixed summary structure (4 sections)
- Simple pattern matching (heuristic mode)
- No token counting (yet)

## Future Enhancements

Phase 2+:
- Token-aware compression with tiktoken
- Configurable compression ratios
- Domain-specific extraction
- Quality scoring

---

**Philosophy**: One function, no config, just works.
