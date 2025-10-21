#!/usr/bin/env python3
"""Detect false completions: agents claim success but user repeats request."""
import json, sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Configuration
STOPWORDS = {'the','a','an','is','are','was','were','be','have','has','had','do','does','did',
             'will','would','could','should','can','make','fix','update','change','add','create',
             'build','for','to','and','or','but','in','on','at','with','from','of'}
MIN_OVERLAP, MIN_REPS, WINDOW_HRS = 2, 1, 24  # Ask twice = failure

def extract_keywords(text):
    """Extract keywords, removing stopwords."""
    return {w for w in text.lower().replace(',',' ').replace('.',' ').split() 
            if len(w) > 2 and w not in STOPWORDS} if text else set()

def find_repetitions(invocations):
    """Find similar tasks within time window."""
    by_agent = defaultdict(list)
    for inv in invocations:
        if inv.get('agent_name'):
            by_agent[inv['agent_name']].append(inv)
    
    false_completions = []
    for agent, invs in by_agent.items():
        sorted_invs = sorted(invs, key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z','+00:00')))
        for i, inv1 in enumerate(sorted_invs):
            ts1 = datetime.fromisoformat(inv1['timestamp'].replace('Z','+00:00'))
            kw1 = extract_keywords(inv1.get('task_description',''))
            if not kw1: continue
            
            similar = [inv1]
            for inv2 in sorted_invs[i+1:]:
                ts2 = datetime.fromisoformat(inv2['timestamp'].replace('Z','+00:00'))
                if (ts2-ts1) > timedelta(hours=WINDOW_HRS): break
                
                kw2 = extract_keywords(inv2.get('task_description',''))
                if len(kw1 & kw2) >= MIN_OVERLAP:
                    similar.append(inv2)
            
            # False completion if: 2+ attempts, first succeeded
            if len(similar) >= MIN_REPS and similar[0].get('outcome',{}).get('status') == 'success':
                false_completions.append({'agent_name': agent, 'attempts': similar, 'keywords': kw1, 
                                        'repetition_count': len(similar)})
    return false_completions

def log_false_completion(agent, evidence, output_file, dry_run=False):
    """Log to agent_reviews.jsonl."""
    atts = evidence['attempts']
    ts1 = datetime.fromisoformat(atts[0]['timestamp'].replace('Z','+00:00'))
    ts2 = datetime.fromisoformat(atts[-1]['timestamp'].replace('Z','+00:00'))
    hrs = round((ts2-ts1).total_seconds()/3600, 1)
    
    entry = {
        'timestamp': datetime.utcnow().isoformat()+'Z',
        'agent_name': agent,
        'action': 'auto_detected_false_completion',
        'reasoning': f"Agent claimed success but user requested similar task {evidence['repetition_count']} times in {hrs} hours",
        'category': 'quality_issue',
        'reviewer': 'system',
        'evidence': {
            'repetition_count': evidence['repetition_count'],
            'keywords': sorted(evidence['keywords']),
            'time_span_hours': hrs,
            'attempts': [{'timestamp': a['timestamp'], 'outcome': a.get('outcome',{}).get('status','unknown'),
                         'task': a.get('task_description','')[:100]} for a in atts]
        }
    }
    
    if dry_run:
        print(f"\n[DRY RUN] Would log for {agent}:\n{json.dumps(entry, indent=2)}")
    else:
        with open(output_file, 'a') as f:
            f.write(json.dumps(entry)+'\n')
        print(f"✓ Logged false completion for {agent} ({evidence['repetition_count']} repetitions)")

def main():
    dry_run = len(sys.argv) > 1 and sys.argv[1] == '--dry-run'
    root = Path(__file__).parent.parent
    inv_file, rev_file = root/'telemetry'/'agent_invocations.jsonl', root/'telemetry'/'agent_reviews.jsonl'
    
    if not inv_file.exists():
        print(f"No invocations file at {inv_file}"); return
    
    invocations = [json.loads(line) for line in open(inv_file) if line.strip()]
    print(f"Analyzing {len(invocations)} invocations...")
    
    false_comps = find_repetitions(invocations)
    if not false_comps:
        print("No false completions detected."); return
    
    print(f"\nFound {len(false_comps)} potential false completions:\n")
    for fc in false_comps:
        log_false_completion(fc['agent_name'], fc, rev_file, dry_run)
    
    if not dry_run:
        print(f"\n✓ Results appended to {rev_file}")

if __name__ == '__main__':
    main()
