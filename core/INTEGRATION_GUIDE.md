# Compaction Utility - Integration Guide

Quick guide for integrating context compression into OaK agent workflows.

## Installation

No installation required - uses Python stdlib only.

**Optional** (for Claude API compression):
```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-api-key"
```

## Quick Integration (3 Steps)

### Step 1: Import

```python
from core.compaction import compact_output
```

### Step 2: Compress Agent Output

```python
# After agent completes work
full_output = agent.execute(task)

# Compress for next agent
summary = compact_output(full_output, artifact_type)
```

### Step 3: Pass to Next Agent

```python
# Next agent receives compressed context
next_agent.execute(task, context=summary)
```

## Artifact Types

Use appropriate type for best compression:

- `"research"` - Research and analysis documents
- `"plan"` - Planning and architecture documents
- `"implementation"` - Code implementation summaries
- `"analysis"` - Technical analysis reports
- `"design"` - Design specifications

## Real-World Examples

### Single Agent Workflow

```python
def execute_research_task(task):
    # Agent performs research
    full_research = research_agent.analyze(task)
    
    # Save full version for archive
    save_artifact(f"artifacts/{task.id}/full-research.md", full_research)
    
    # Compress for next phase
    summary = compact_output(full_research, "research")
    save_artifact(f"artifacts/{task.id}/research-summary.md", summary)
    
    return summary
```

### Multi-Agent Workflow

```python
def execute_full_workflow(task):
    """Research → Plan → Implement workflow with compression."""
    
    # Phase 1: Research
    research_full = research_agent.execute(task)
    research_summary = compact_output(research_full, "research")
    save_artifacts("research", research_full, research_summary)
    
    # Phase 2: Planning (receives compressed research)
    plan_full = planning_agent.execute(task, context=research_summary)
    plan_summary = compact_output(plan_full, "plan")
    save_artifacts("plan", plan_full, plan_summary)
    
    # Phase 3: Implementation (receives compressed plan)
    impl_full = impl_agent.execute(task, context=plan_summary)
    impl_summary = compact_output(impl_full, "implementation")
    save_artifacts("implementation", impl_full, impl_summary)
    
    return {
        "research": research_summary,
        "plan": plan_summary,
        "implementation": impl_summary
    }


def save_artifacts(phase, full, summary):
    """Save both full and compressed versions."""
    save_artifact(f"artifacts/{phase}/full.md", full)
    save_artifact(f"artifacts/{phase}/summary.md", summary)
```

### Agent Handoff Pattern

```python
class AgentCoordinator:
    def handoff(self, from_agent, to_agent, output, artifact_type):
        """Compress context during agent handoff."""
        
        # Compress output from previous agent
        compressed = compact_output(output, artifact_type)
        
        # Log handoff with size metrics
        self.log_handoff(
            from_agent=from_agent.name,
            to_agent=to_agent.name,
            original_size=len(output),
            compressed_size=len(compressed),
            compression_ratio=len(output) / len(compressed)
        )
        
        # Pass compressed context to next agent
        return to_agent.execute(context=compressed)
```

## Expected Compression

**Small documents** (test size):
- 2-3x compression
- ~50-100 lines → ~20-30 lines

**Large documents** (production size):
- Research: 2000 lines → ~100 lines (20x)
- Plans: 1000 lines → ~50 lines (20x)
- Implementation: 5000 lines → ~100 lines (50x)

**Token savings**:
- ~4 characters per token (rough estimate)
- Multi-agent workflow: ~60-70% reduction

## Output Structure

Every compression produces consistent markdown:

```markdown
# [Type] Summary

## Overview
Brief summary of work completed (2-3 sentences).

## Key Findings
- Finding 1
- Finding 2
- Finding 3
- Finding 4
- Finding 5

## Files Created
- path/to/file1.ts
- path/to/file2.py

## What's Next
Next steps for following agent.
```

## Best Practices

### When to Compress

**DO compress**:
- Agent-to-agent handoffs
- Context > 500 lines
- Token budget concerns
- Passing intermediate results

**DON'T compress**:
- Final user deliverables
- Documentation artifacts
- Audit trail requirements
- < 100 line outputs

### Save Both Versions

```python
# Always save full and compressed
save(f"{path}/full-output.md", full_output)
save(f"{path}/summary.md", compact_output(full_output, type))
```

### Measure Savings

```python
original_tokens = len(full_output) // 4
compressed_tokens = len(compressed) // 4
savings = original_tokens - compressed_tokens

log.info(f"Compression saved ~{savings} tokens ({100 * savings/original_tokens:.1f}%)")
```

## Troubleshooting

### Low Compression Ratio

**Problem**: Compression ratio < 2x on large documents

**Solutions**:
- Ensure document is well-structured markdown
- Check for headers, bullets, numbered lists
- Verify "Next Steps" or "TODO" sections exist
- Consider manual structure improvements

### Missing Information

**Problem**: Important details lost in compression

**Solutions**:
- Use more descriptive headers and bullets
- Add "Key Findings" section explicitly
- Document file paths clearly (use backticks)
- Add "Next Steps" section with clear bullets

### API Compression Failing

**Problem**: Claude API compression not working

**Solutions**:
- Verify `ANTHROPIC_API_KEY` environment variable set
- Check `anthropic` package installed (`pip install anthropic`)
- Verify API key has sufficient credits
- Falls back to heuristics automatically (no error)

## Testing Your Integration

```python
# Simple integration test
def test_integration():
    # Create test output
    test_output = """
    # Test Analysis
    
    ## Findings
    - Finding 1
    - Finding 2
    
    ## Files
    Created: `test.py`
    
    ## Next Steps
    - Deploy
    - Test
    """
    
    # Compress
    compressed = compact_output(test_output, "analysis")
    
    # Verify structure
    assert "# Analysis Summary" in compressed
    assert "## Overview" in compressed
    assert "## Key Findings" in compressed
    assert "## Files Created" in compressed
    assert "## What's Next" in compressed
    
    print("Integration test passed ✓")


test_integration()
```

## Performance Considerations

**Heuristic compression** (default):
- Speed: ~10ms per document
- Memory: Minimal (string operations)
- CPU: Negligible
- Cost: Free

**Claude API compression** (optional):
- Speed: ~1-2 seconds per document
- Memory: Minimal
- CPU: API call overhead
- Cost: ~$0.001 per compression

**Recommendation**: Use heuristic compression for production. Reserve API compression for critical handoffs requiring highest quality.

## Migration Path

### Phase 1: Testing (Current)
- Test on dev workflows
- Measure compression quality
- Validate token savings

### Phase 2: Selective Integration
- Enable for long-running workflows
- Compress research → planning handoffs
- Monitor compression metrics

### Phase 3: Full Integration
- All agent handoffs use compression
- Archive full outputs separately
- Track compression telemetry

## Support

- **Quick Reference**: `core/COMPACTION_QUICK_START.md`
- **Full Documentation**: `core/COMPACTION_README.md`
- **Examples**: `examples/compaction_workflow.py`
- **Validation**: Run `core/validate_compaction.py`

---

**Ready for Integration** - Start with selective handoffs, expand as validated.
