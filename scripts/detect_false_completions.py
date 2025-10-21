#!/usr/bin/env python3
"""
Detect False Completions

Finds cases where agents claimed success but user had to repeat request.

Simple heuristic:
- Same agent invoked multiple times for similar task (keyword overlap)
- Earlier attempt succeeded
- User had to ask again within 24 hours
- Probably a false completion

Usage:
  python3 scripts/detect_false_completions.py
  python3 scripts/detect_false_completions.py --dry-run
  
Output:
  Appends to telemetry/agent_reviews.jsonl
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Any

# Import issue tracker
sys.path.insert(0, str(Path(__file__).parent.parent))
from telemetry.issue_tracker import IssueTracker


# Stopwords to ignore when extracting keywords
STOPWORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can',
    'make', 'fix', 'update', 'change', 'add', 'create', 'build', 'for', 'to',
    'and', 'or', 'but', 'in', 'on', 'at', 'with', 'from', 'of'
}

# Configuration
MIN_KEYWORD_OVERLAP = 2
MIN_REPETITIONS = 1  # Ask twice = failure (1 repetition after first request = 2 total)
TIME_WINDOW_HOURS = 24


def extract_keywords(text: str) -> Set[str]:
    """Extract keywords from text, removing stopwords."""
    if not text:
        return set()
    
    # Simple word splitting and cleaning
    words = text.lower().replace(',', ' ').replace('.', ' ').split()
    keywords = {w.strip() for w in words if len(w) > 2 and w not in STOPWORDS}
    return keywords


def calculate_overlap(keywords1: Set[str], keywords2: Set[str]) -> int:
    """Count matching keywords between two sets."""
    return len(keywords1 & keywords2)


def find_repetitions(invocations: List[Dict], time_window_hours: int = TIME_WINDOW_HOURS) -> List[Dict]:
    """Find similar tasks within time window for each agent."""
    # Group by agent_name
    by_agent = defaultdict(list)
    for inv in invocations:
        agent_name = inv.get('agent_name')
        if agent_name:
            by_agent[agent_name].append(inv)
    
    # Find repetitions within each agent's invocations
    false_completions = []
    
    for agent_name, agent_invocations in by_agent.items():
        # Sort by timestamp
        sorted_invocations = sorted(
            agent_invocations,
            key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00'))
        )
        
        # Compare each invocation with later ones
        for i, inv1 in enumerate(sorted_invocations):
            ts1 = datetime.fromisoformat(inv1['timestamp'].replace('Z', '+00:00'))
            keywords1 = extract_keywords(inv1.get('task_description', ''))
            
            if not keywords1:
                continue
            
            similar_attempts = [inv1]
            
            for inv2 in sorted_invocations[i+1:]:
                ts2 = datetime.fromisoformat(inv2['timestamp'].replace('Z', '+00:00'))
                
                # Check if within time window
                if (ts2 - ts1) > timedelta(hours=time_window_hours):
                    break
                
                keywords2 = extract_keywords(inv2.get('task_description', ''))
                overlap = calculate_overlap(keywords1, keywords2)
                
                if overlap >= MIN_KEYWORD_OVERLAP:
                    similar_attempts.append(inv2)
            
            # Check if this represents a false completion
            if is_false_completion(similar_attempts):
                false_completions.append({
                    'agent_name': agent_name,
                    'attempts': similar_attempts,
                    'keywords': keywords1,
                    'repetition_count': len(similar_attempts)
                })
    
    return false_completions


def is_false_completion(attempts: List[Dict]) -> bool:
    """Check if earlier succeeded but task was repeated.

    BUG FIX (2025-10-21): Changed < to <= to correctly enforce MIN_REPETITIONS threshold.
    With MIN_REPETITIONS=1, we need MORE than 1 attempt (i.e., at least 2 total attempts).
    Previous logic: len(attempts) < 1 only caught empty lists (impossible)
    Fixed logic: len(attempts) <= 1 filters out single attempts (correct)
    """
    if len(attempts) <= MIN_REPETITIONS:
        return False
    
    # Check if first attempt claimed success
    first_outcome = attempts[0].get('outcome', {}).get('status')
    if first_outcome != 'success':
        return False
    
    # If we have repetitions after a success, it's likely a false completion
    return True


def log_false_completion(agent_name: str, evidence: Dict, output_file: Path, dry_run: bool = False):
    """Append false completion to agent_reviews.jsonl."""
    attempts = evidence['attempts']
    
    # Calculate time span
    ts_first = datetime.fromisoformat(attempts[0]['timestamp'].replace('Z', '+00:00'))
    ts_last = datetime.fromisoformat(attempts[-1]['timestamp'].replace('Z', '+00:00'))
    time_span_hours = (ts_last - ts_first).total_seconds() / 3600
    
    review_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'agent_name': agent_name,
        'action': 'auto_detected_false_completion',
        'reasoning': f"Agent claimed success but user requested similar task {evidence['repetition_count']} times in {time_span_hours:.1f} hours",
        'category': 'quality_issue',
        'reviewer': 'system',
        'evidence': {
            'repetition_count': evidence['repetition_count'],
            'keywords': sorted(list(evidence['keywords'])),
            'time_span_hours': round(time_span_hours, 1),
            'attempts': [
                {
                    'timestamp': a['timestamp'],
                    'outcome': a.get('outcome', {}).get('status', 'unknown'),
                    'task': a.get('task_description', '')[:100]  # First 100 chars
                }
                for a in attempts
            ]
        }
    }
    
    if dry_run:
        print(f"\n[DRY RUN] Would log false completion for {agent_name}:")
        print(json.dumps(review_entry, indent=2))
    else:
        # Log to agent_reviews.jsonl (audit trail)
        with open(output_file, 'a') as f:
            f.write(json.dumps(review_entry) + '\n')

        # Create issue for tracking
        tracker = IssueTracker()
        issue_id = tracker.create_issue(
            agent_name=agent_name,
            description=review_entry['reasoning'],
            evidence=review_entry['evidence'],
            category='false_completion'
        )

        print(f"✓ Logged false completion for {agent_name} ({evidence['repetition_count']} repetitions)")
        print(f"  Issue ID: {issue_id}")


def main():
    # Check for dry-run mode
    dry_run = len(sys.argv) > 1 and sys.argv[1] == '--dry-run'
    
    # File paths
    project_root = Path(__file__).parent.parent
    invocations_file = project_root / 'telemetry' / 'agent_invocations.jsonl'
    reviews_file = project_root / 'telemetry' / 'agent_reviews.jsonl'
    
    # Read invocations
    if not invocations_file.exists():
        print(f"No invocations file found at {invocations_file}")
        return
    
    invocations = []
    with open(invocations_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                invocations.append(json.loads(line))
    
    print(f"Analyzing {len(invocations)} invocations...")
    
    # Find false completions
    false_completions = find_repetitions(invocations)
    
    if not false_completions:
        print("No false completions detected.")
        return
    
    print(f"\nFound {len(false_completions)} potential false completions:\n")
    
    # Log each false completion
    for fc in false_completions:
        log_false_completion(fc['agent_name'], fc, reviews_file, dry_run)
    
    if not dry_run:
        print(f"\n✓ Results appended to {reviews_file}")


if __name__ == '__main__':
    main()
