#!/usr/bin/env python3
"""
Feedback Collection Utilities

Simple feedback collection system that appends to agent_reviews.jsonl.
"""

import json
from datetime import datetime
from pathlib import Path


def log_feedback(agent_name: str, feedback: str, category: str = "general"):
    """
    Log user feedback to agent_reviews.jsonl.
    
    Args:
        agent_name: Name of the agent
        feedback: User feedback text
        category: Feedback category (general, weekly, monthly)
    """
    telemetry_dir = Path(__file__).parent
    reviews_file = telemetry_dir / "agent_reviews.jsonl"
    
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent_name": agent_name,
        "action": "feedback",
        "reasoning": feedback,
        "category": category,
        "reviewer": "human"
    }
    
    with open(reviews_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def collect_feedback_interactive(agent_name: str, category: str = "general"):
    """
    Prompt user for feedback and log it.
    
    Args:
        agent_name: Name of the agent
        category: Feedback category (general, weekly, monthly)
    """
    print(f"\nFeedback for {agent_name} (press Enter to skip):")
    feedback = input("> ").strip()
    
    if feedback:
        log_feedback(agent_name, feedback, category)
        print(f"   ✓ Feedback logged for {agent_name}")
