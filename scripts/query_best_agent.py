#!/usr/bin/env python3
"""
Query Best Agent

Analyzes historical telemetry to recommend the best agent for a given task.

Usage:
    python3 scripts/query_best_agent.py --task "API development" --domain "backend"
    python3 scripts/query_best_agent.py --task-type "security audit"
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from telemetry.analyzer import TelemetryAnalyzer


@dataclass
class AgentRecommendation:
    """Agent recommendation with performance metrics."""
    agent_name: str
    confidence: float  # 0.0-1.0
    success_rate: float
    avg_duration_minutes: float
    total_tasks: int
    recent_performance: str  # "improving", "stable", "declining"


def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from task description."""
    # Convert to lowercase and split
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Common stopwords to exclude
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'should', 'could', 'may', 'might', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    # Filter out stopwords and short words
    keywords = [w for w in words if w not in stopwords and len(w) > 2]
    
    return keywords


def calculate_relevance_score(
    task_keywords: List[str],
    invocation: Dict,
    domain: Optional[str] = None
) -> float:
    """Calculate how relevant an invocation is to the task."""
    score = 0.0
    
    # Extract text from invocation
    task_desc = invocation.get("task_description", "").lower()
    agent_type = invocation.get("agent_type", "").lower()
    state_features = invocation.get("state_features", {})
    
    # Check task description keyword matches
    for keyword in task_keywords:
        if keyword in task_desc:
            score += 1.0
    
    # Check domain match if specified
    if domain:
        domain_lower = domain.lower()
        
        # Check agent type
        if domain_lower in agent_type:
            score += 2.0
        
        # Check state features
        task_type = state_features.get("task", {}).get("type", "").lower()
        if domain_lower in task_type:
            score += 1.5
    
    return score


def query_best_agent(
    task_description: str,
    domain: Optional[str] = None,
    min_confidence: float = 0.5
) -> Optional[AgentRecommendation]:
    """
    Query telemetry and return best agent recommendation.
    
    Args:
        task_description: Description of the task (e.g., "API development", "security audit")
        domain: Optional domain filter (e.g., "backend", "frontend")
        min_confidence: Minimum confidence threshold (0.0-1.0)
    
    Returns:
        AgentRecommendation with best agent and statistics, or None if no suitable agent found
    """
    # Load telemetry data
    analyzer = TelemetryAnalyzer()
    invocations = analyzer.load_invocations()
    
    if not invocations:
        return None
    
    # Extract keywords from task description
    task_keywords = extract_keywords(task_description)
    
    # Score each invocation for relevance
    agent_scores = defaultdict(lambda: {
        "relevance_sum": 0.0,
        "invocations": [],
        "successes": 0,
        "durations": []
    })
    
    for inv in invocations:
        agent_name = inv.get("agent_name")
        if not agent_name:
            continue
        
        # Calculate relevance
        relevance = calculate_relevance_score(task_keywords, inv, domain)
        
        if relevance > 0:
            agent_scores[agent_name]["relevance_sum"] += relevance
            agent_scores[agent_name]["invocations"].append(inv)
            
            # Track success
            if inv.get("outcome", {}).get("status") == "success":
                agent_scores[agent_name]["successes"] += 1
            
            # Track duration
            duration = inv.get("duration_seconds")
            if duration:
                agent_scores[agent_name]["durations"].append(duration)
    
    if not agent_scores:
        return None
    
    # Calculate final scores for each agent
    recommendations = []
    
    for agent_name, data in agent_scores.items():
        total_tasks = len(data["invocations"])
        if total_tasks == 0:
            continue
        
        # Calculate success rate
        success_rate = data["successes"] / total_tasks
        
        # Calculate average duration
        avg_duration = (
            sum(data["durations"]) / len(data["durations"])
            if data["durations"] else 0.0
        )
        avg_duration_minutes = avg_duration / 60
        
        # Calculate confidence based on relevance and task count
        avg_relevance = data["relevance_sum"] / total_tasks
        task_count_factor = min(total_tasks / 10.0, 1.0)  # Max out at 10 tasks
        confidence = (avg_relevance * 0.6 + task_count_factor * 0.4) * success_rate
        
        # Normalize confidence to 0-1 range
        confidence = min(confidence / 3.0, 1.0)  # Assuming max relevance of ~3
        
        # Get performance trend
        trend_data = analyzer.get_agent_performance_trends(agent_name)
        recent_performance = trend_data.get("trend", "stable")
        
        recommendations.append(AgentRecommendation(
            agent_name=agent_name,
            confidence=confidence,
            success_rate=success_rate,
            avg_duration_minutes=avg_duration_minutes,
            total_tasks=total_tasks,
            recent_performance=recent_performance
        ))
    
    # Filter by minimum confidence
    recommendations = [r for r in recommendations if r.confidence >= min_confidence]
    
    if not recommendations:
        return None
    
    # Sort by confidence (descending)
    recommendations.sort(key=lambda r: r.confidence, reverse=True)
    
    return recommendations[0]


def main():
    """CLI interface."""
    parser = argparse.ArgumentParser(description="Query best agent for task")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--domain", help="Domain filter (backend, frontend, etc.)")
    parser.add_argument("--min-confidence", type=float, default=0.5, help="Minimum confidence threshold (0.0-1.0)")
    parser.add_argument("--all", action="store_true", help="Show all matching agents, not just top recommendation")
    
    args = parser.parse_args()
    
    # Query for best agent
    recommendation = query_best_agent(args.task, args.domain, args.min_confidence)
    
    if not recommendation:
        print(f"\nNo suitable agent found for task: {args.task}")
        if args.domain:
            print(f"Domain filter: {args.domain}")
        print(f"\nTry:")
        print("  - Lowering --min-confidence threshold")
        print("  - Removing domain filter")
        print("  - Using different task keywords")
        return 1
    
    # Display recommendation
    print(f"\nRecommended Agent: {recommendation.agent_name}")
    print(f"   Confidence: {recommendation.confidence:.0%}")
    print(f"   Success Rate: {recommendation.success_rate:.0%}")
    print(f"   Avg Duration: {recommendation.avg_duration_minutes:.1f} min")
    print(f"   Total Tasks: {recommendation.total_tasks}")
    print(f"   Trend: {recommendation.recent_performance}")
    
    # If --all flag, show all recommendations
    if args.all:
        analyzer = TelemetryAnalyzer()
        invocations = analyzer.load_invocations()
        task_keywords = extract_keywords(args.task)
        
        agent_scores = defaultdict(lambda: {
            "relevance_sum": 0.0,
            "invocations": [],
            "successes": 0,
            "durations": []
        })
        
        for inv in invocations:
            agent_name = inv.get("agent_name")
            if not agent_name:
                continue
            
            relevance = calculate_relevance_score(task_keywords, inv, args.domain)
            
            if relevance > 0:
                agent_scores[agent_name]["relevance_sum"] += relevance
                agent_scores[agent_name]["invocations"].append(inv)
                
                if inv.get("outcome", {}).get("status") == "success":
                    agent_scores[agent_name]["successes"] += 1
                
                duration = inv.get("duration_seconds")
                if duration:
                    agent_scores[agent_name]["durations"].append(duration)
        
        all_recs = []
        for agent_name, data in agent_scores.items():
            total_tasks = len(data["invocations"])
            if total_tasks == 0:
                continue
            
            success_rate = data["successes"] / total_tasks
            avg_duration = (
                sum(data["durations"]) / len(data["durations"])
                if data["durations"] else 0.0
            )
            avg_duration_minutes = avg_duration / 60
            
            avg_relevance = data["relevance_sum"] / total_tasks
            task_count_factor = min(total_tasks / 10.0, 1.0)
            confidence = (avg_relevance * 0.6 + task_count_factor * 0.4) * success_rate
            confidence = min(confidence / 3.0, 1.0)
            
            trend_data = analyzer.get_agent_performance_trends(agent_name)
            recent_performance = trend_data.get("trend", "stable")
            
            all_recs.append(AgentRecommendation(
                agent_name=agent_name,
                confidence=confidence,
                success_rate=success_rate,
                avg_duration_minutes=avg_duration_minutes,
                total_tasks=total_tasks,
                recent_performance=recent_performance
            ))
        
        all_recs = [r for r in all_recs if r.confidence >= args.min_confidence]
        all_recs.sort(key=lambda r: r.confidence, reverse=True)
        
        if len(all_recs) > 1:
            print(f"\nAll Matching Agents ({len(all_recs)}):")
            for i, rec in enumerate(all_recs, 1):
                print(f"\n{i}. {rec.agent_name}")
                print(f"   Confidence: {rec.confidence:.0%}")
                print(f"   Success Rate: {rec.success_rate:.0%}")
                print(f"   Avg Duration: {rec.avg_duration_minutes:.1f} min")
                print(f"   Total Tasks: {rec.total_tasks}")
                print(f"   Trend: {rec.recent_performance}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
