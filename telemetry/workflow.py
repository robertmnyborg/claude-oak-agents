#!/usr/bin/env python3
"""
Workflow ID Generation Utility for Claude OaK Agents

This module provides utilities for generating unique workflow identifiers
for multi-agent coordination tracking.
"""

import uuid
from datetime import datetime


def generate_workflow_id() -> str:
    """
    Generate unique workflow ID: wf-YYYYMMDD-<8-char-uuid>
    
    Returns:
        str: Workflow ID in format "wf-20251021-a1b2c3d4"
    
    Example:
        >>> workflow_id = generate_workflow_id()
        >>> print(workflow_id)
        wf-20251021-a1b2c3d4
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    short_uuid = str(uuid.uuid4())[:8]
    return f"wf-{timestamp}-{short_uuid}"


if __name__ == "__main__":
    # Example usage
    print(generate_workflow_id())
