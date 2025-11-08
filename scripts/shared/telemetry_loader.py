"""Unified telemetry data loading utilities."""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


def load_invocations(telemetry_file: Path, 
                     filter_days: Optional[int] = None,
                     filter_agent: Optional[str] = None,
                     filter_workflow: Optional[str] = None) -> List[Dict]:
    """
    Load agent invocations from JSONL telemetry file.
    
    Args:
        telemetry_file: Path to agent_invocations.jsonl
        filter_days: Only return invocations from last N days
        filter_agent: Filter by agent name
        filter_workflow: Filter by workflow_id
        
    Returns:
        List of invocation dictionaries
    """
    if not telemetry_file.exists():
        return []
    
    invocations = []
    
    try:
        with open(telemetry_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    inv = json.loads(line)
                    
                    # Apply filters
                    if filter_agent and inv.get('agent_name') != filter_agent:
                        continue
                    if filter_workflow and inv.get('workflow_id') != filter_workflow:
                        continue
                    if filter_days:
                        timestamp_str = inv.get('timestamp', '')
                        if timestamp_str:
                            try:
                                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                                days_ago = (datetime.now().replace(tzinfo=timestamp.tzinfo) - timestamp).days
                                if days_ago > filter_days:
                                    continue
                            except ValueError:
                                # Skip if timestamp parsing fails
                                continue
                    
                    invocations.append(inv)
                except json.JSONDecodeError:
                    continue
    except Exception:
        return []
    
    return invocations


def get_recent_invocations(telemetry_dir: Path, days: int = 7) -> List[Dict]:
    """Get invocations from last N days."""
    telemetry_file = telemetry_dir / 'agent_invocations.jsonl'
    return load_invocations(telemetry_file, filter_days=days)


def get_workflow_invocations(telemetry_dir: Path, workflow_id: str) -> List[Dict]:
    """Get all invocations for a specific workflow."""
    telemetry_file = telemetry_dir / 'agent_invocations.jsonl'
    return load_invocations(telemetry_file, filter_workflow=workflow_id)
