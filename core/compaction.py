"""
Context Compression Utility for OaK Agent Handoffs

Compresses verbose agent outputs into concise summaries for efficient context passing.
Uses simple heuristic-based compression with option for Claude API enhancement.
"""

import re
import os
from typing import List, Tuple


def compact_output(full_text: str, artifact_type: str) -> str:
    """
    Compress agent output into concise summary for handoff.
    
    Args:
        full_text: Full agent output (research, plan, implementation, etc.)
        artifact_type: Type of artifact (research, plan, implementation, etc.)
    
    Returns:
        Compressed markdown summary (~50-100 lines)
    
    Usage:
        >>> full_research = "... 2000 lines of analysis ..."
        >>> compressed = compact_output(full_research, "research")
        >>> # Returns ~100 line summary for next agent
    """
    # Try Claude API first if available, fallback to heuristics
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        try:
            return _compress_with_claude(full_text, artifact_type, api_key)
        except Exception:
            pass  # Fallback to heuristics
    
    return _compress_with_heuristics(full_text, artifact_type)


def _compress_with_heuristics(text: str, artifact_type: str) -> str:
    """Simple heuristic-based compression."""
    key_findings = _extract_key_findings(text)
    files_created = _extract_files(text)
    overview = _generate_overview(text, artifact_type)
    next_steps = _extract_next_steps(text)
    
    summary = f"""# {artifact_type.title()} Summary

## Overview
{overview}

## Key Findings
{_format_list(key_findings, max_items=5)}

## Files Created
{_format_list(files_created)}

## What's Next
{next_steps}
"""
    return summary.strip()


def _extract_key_findings(text: str) -> List[str]:
    """Extract key points from text."""
    findings = []
    
    # Extract headers and first sentences
    lines = text.split('\n')
    for i, line in enumerate(lines):
        # Capture markdown headers
        if re.match(r'^#{1,3}\s+', line):
            findings.append(line.replace('#', '').strip())
        # Capture bullet points
        elif re.match(r'^[\-\*]\s+', line):
            findings.append(line.lstrip('- *').strip())
        # Capture numbered points
        elif re.match(r'^\d+\.\s+', line):
            findings.append(re.sub(r'^\d+\.\s+', '', line).strip())
    
    return findings[:5]  # Limit to top 5


def _extract_files(text: str) -> List[str]:
    """Extract file paths from text."""
    file_patterns = [
        r'`([^`]+\.[a-z]{2,4})`',  # Backtick files
        r'(?:Created?|Modified?|Updated?):\s*([^\s]+\.[a-z]{2,4})',  # Action: file
        r'(?:File|Path):\s*([^\s]+)',  # File: path
    ]
    
    files = set()
    for pattern in file_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        files.update(matches)
    
    return sorted(list(files))


def _generate_overview(text: str, artifact_type: str) -> str:
    """Generate 2-3 sentence overview."""
    # Extract first paragraph or first few sentences
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    first_para = paragraphs[0] if paragraphs else text[:500]
    
    # Extract first 2-3 sentences
    sentences = re.split(r'[.!?]\s+', first_para)
    overview = '. '.join(sentences[:3])
    
    if not overview.endswith('.'):
        overview += '.'
    
    return overview


def _extract_next_steps(text: str) -> str:
    """Extract next steps or recommendations."""
    # Look for sections like "Next Steps", "Recommendations", "TODO"
    next_patterns = [
        r'(?:##?\s*)?(?:Next Steps?|What\'s Next|Recommendations?|TODO)[\s:]*\n((?:[\-\*]\s+.+\n?)+)',
        r'(?:##?\s*)?(?:Future Work|Follow-up)[\s:]*\n((?:[\-\*]\s+.+\n?)+)',
    ]
    
    for pattern in next_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    
    # Default fallback
    return f"Proceed with next phase of {artifact_type} workflow."


def _format_list(items: List[str], max_items: int = None) -> str:
    """Format list as markdown bullets."""
    if not items:
        return "- None"
    
    if max_items:
        items = items[:max_items]
    
    return '\n'.join(f"- {item}" for item in items)


def _compress_with_claude(text: str, artifact_type: str, api_key: str) -> str:
    """
    Compress using Claude API (requires anthropic package).
    Falls back to heuristics if package not available.
    """
    try:
        import anthropic
    except ImportError:
        raise ImportError("anthropic package not installed")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""Compress this {artifact_type} artifact into a concise summary.

Extract:
1. Brief overview (2-3 sentences)
2. Key findings/decisions (max 5 bullet points)
3. Files created (list paths)
4. What the next agent needs to know (brief guidance)

Output as markdown. Keep it under 100 lines.

ARTIFACT:
{text}
"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text
