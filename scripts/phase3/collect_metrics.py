#!/usr/bin/env python3
"""
Metrics Collection

Collects agent-level and system-level metrics from telemetry data.

Usage:
  python3 scripts/phase3/collect_metrics.py
  python3 scripts/phase3/collect_metrics.py --period week
  python3 scripts/phase3/collect_metrics.py --period month
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from telemetry.analyzer import TelemetryAnalyzer
from telemetry.issue_tracker import IssueTracker


def calculate_false_completion_rate(agent_name: str, issues: List[Dict], invocations: int) -> float:
    """Calculate false completion rate for an agent."""
    if invocations == 0:
        return 0.0

    false_completions = sum(1 for issue in issues
                           if issue.get('agent_name') == agent_name
                           and issue.get('category') == 'false_completion')

    return false_completions / invocations


def calculate_rework_rate(agent_name: str, issues: List[Dict], invocations: int) -> float:
    """Calculate rework rate (reopened issues / total issues)."""
    if invocations == 0:
        return 0.0

    agent_issues = [issue for issue in issues if issue.get('agent_name') == agent_name]
    if not agent_issues:
        return 0.0

    reopened = sum(1 for issue in agent_issues if issue.get('reopened_at'))
    return reopened / len(agent_issues)


def calculate_avg_resolution_time(agent_name: str, issues: List[Dict]) -> float:
    """Calculate average resolution time in hours."""
    agent_issues = [issue for issue in issues
                   if issue.get('agent_name') == agent_name
                   and issue.get('state') == 'resolved']

    if not agent_issues:
        return 0.0

    resolution_times = []
    for issue in agent_issues:
        created = issue.get('created_at')
        resolved = issue.get('resolved_at')

        if created and resolved:
            try:
                created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                resolved_dt = datetime.fromisoformat(resolved.replace('Z', '+00:00'))
                hours = (resolved_dt - created_dt).total_seconds() / 3600
                resolution_times.append(hours)
            except:
                continue

    if resolution_times:
        return sum(resolution_times) / len(resolution_times)

    return 0.0


def get_issue_counts(agent_name: str, all_issues: Dict[str, Dict]) -> Dict[str, int]:
    """Get issue counts by state for an agent."""
    agent_issues = [issue for issue in all_issues.values()
                   if issue.get('agent_name') == agent_name]

    counts = {
        'total': len(agent_issues),
        'open': 0,
        'in_progress': 0,
        'needs_verification': 0,
        'resolved': 0
    }

    for issue in agent_issues:
        state = issue.get('state', 'open')
        if state in counts:
            counts[state] += 1

    return counts


def get_user_satisfaction(agent_name: str) -> Optional[float]:
    """Get average user satisfaction rating from feedback."""
    # Look for feedback in agent_reviews.jsonl
    project_root = Path(__file__).parent.parent.parent
    reviews_file = project_root / 'telemetry' / 'agent_reviews.jsonl'

    if not reviews_file.exists():
        return None

    ratings = []
    with open(reviews_file, 'r') as f:
        for line in f:
            if not line.strip():
                continue

            try:
                review = json.loads(line)
                if (review.get('agent_name') == agent_name
                    and review.get('action') == 'feedback'
                    and 'quality_rating' in review):
                    ratings.append(review['quality_rating'])
            except:
                continue

    if ratings:
        return sum(ratings) / len(ratings)

    return None


def collect_agent_metrics(period: str = 'week') -> List[Dict[str, Any]]:
    """Collect metrics for all agents."""

    # Load telemetry data
    analyzer = TelemetryAnalyzer()
    stats = analyzer.generate_statistics()

    # Load issue data
    tracker = IssueTracker()
    all_issues = tracker.get_all_issues()

    # Calculate time range
    now = datetime.utcnow()
    if period == 'week':
        start_time = now - timedelta(days=7)
    elif period == 'month':
        start_time = now - timedelta(days=30)
    else:
        start_time = now - timedelta(days=7)  # default to week

    # Collect metrics for each agent
    metrics = []

    for agent_name, agent_stats in stats.get('agents', {}).items():
        invocation_count = agent_stats.get('invocation_count', 0)
        success_rate = agent_stats.get('success_rate', 0.0)

        # Calculate additional metrics
        false_completion_rate = calculate_false_completion_rate(
            agent_name, list(all_issues.values()), invocation_count
        )

        rework_rate = calculate_rework_rate(
            agent_name, list(all_issues.values()), invocation_count
        )

        avg_resolution_time = calculate_avg_resolution_time(
            agent_name, list(all_issues.values())
        )

        issue_counts = get_issue_counts(agent_name, all_issues)

        user_satisfaction = get_user_satisfaction(agent_name)

        # Determine agent version (from markdown frontmatter if exists)
        version = get_agent_version(agent_name)

        # Determine health status
        health = determine_health_status(
            success_rate, false_completion_rate, rework_rate
        )

        metric = {
            'timestamp': now.isoformat() + 'Z',
            'agent_name': agent_name,
            'period': period,
            'metrics': {
                'invocations': invocation_count,
                'success_rate': success_rate,
                'false_completion_rate': false_completion_rate,
                'avg_resolution_time_hours': round(avg_resolution_time, 1),
                'user_satisfaction': user_satisfaction,
                'rework_rate': rework_rate,
                'issues_opened': issue_counts['total'],
                'issues_resolved': issue_counts['resolved'],
                'issues_open': issue_counts['open'],
                'issues_needs_verification': issue_counts['needs_verification']
            },
            'version': version,
            'health': health
        }

        metrics.append(metric)

    return metrics


def collect_system_metrics(period: str = 'week') -> Dict[str, Any]:
    """Collect system-wide metrics."""

    # Load telemetry data
    analyzer = TelemetryAnalyzer()
    stats = analyzer.generate_statistics()

    # Load issue data
    tracker = IssueTracker()
    all_issues = tracker.get_all_issues()
    issue_stats = tracker.get_statistics()

    # Calculate aggregate metrics
    total_invocations = stats.get('total_invocations', 0)
    total_agents_used = len(stats.get('agents', {}))

    # Calculate system-wide success rate
    agents = stats.get('agents', {})
    if agents:
        total_success = sum(a['success_rate'] * a['invocation_count'] for a in agents.values())
        total_count = sum(a['invocation_count'] for a in agents.values())
        system_success_rate = total_success / total_count if total_count > 0 else 0.0
    else:
        system_success_rate = 0.0

    # Calculate false completion rate
    false_completions = sum(1 for issue in all_issues.values()
                           if issue.get('category') == 'false_completion')
    system_false_completion_rate = false_completions / total_invocations if total_invocations > 0 else 0.0

    # Count improvements applied (would track this separately in production)
    improvements_applied = 0  # TODO: Track this when we implement apply workflow

    # Count A/B tests (would track this separately in production)
    active_ab_tests = 0  # TODO: Track this when we implement A/B testing

    # Average issues per period
    if period == 'week':
        avg_issues = issue_stats['total_issues'] / 1  # issues this week
    else:
        avg_issues = issue_stats['total_issues'] / 4  # average per week over month

    # Average resolution time across all agents
    resolution_times = []
    for issue in all_issues.values():
        if issue.get('state') == 'resolved':
            created = issue.get('created_at')
            resolved = issue.get('resolved_at')
            if created and resolved:
                try:
                    created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    resolved_dt = datetime.fromisoformat(resolved.replace('Z', '+00:00'))
                    hours = (resolved_dt - created_dt).total_seconds() / 3600
                    resolution_times.append(hours)
                except:
                    continue

    avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0.0

    now = datetime.utcnow()

    return {
        'timestamp': now.isoformat() + 'Z',
        'period': period,
        'metrics': {
            'total_invocations': total_invocations,
            'total_agents_used': total_agents_used,
            'system_success_rate': system_success_rate,
            'system_false_completion_rate': system_false_completion_rate,
            'avg_issues_per_period': round(avg_issues, 1),
            'avg_resolution_time_hours': round(avg_resolution_time, 1),
            'total_issues': issue_stats['total_issues'],
            'issues_open': issue_stats['by_state'].get('open', 0),
            'issues_resolved': issue_stats['by_state'].get('resolved', 0),
            'improvements_applied': improvements_applied,
            'active_ab_tests': active_ab_tests
        }
    }


def determine_health_status(success_rate: float, false_completion_rate: float, rework_rate: float) -> str:
    """Determine agent health status: green, yellow, or red."""

    # Green: Success >85%, false completion <10%, improving/stable
    if success_rate > 0.85 and false_completion_rate < 0.10:
        return 'green'

    # Red: Success <70%, false completion >20%, or high rework
    if success_rate < 0.70 or false_completion_rate > 0.20 or rework_rate > 0.30:
        return 'red'

    # Yellow: Everything else
    return 'yellow'


def get_agent_version(agent_name: str) -> str:
    """Get agent version from markdown frontmatter if it exists."""
    project_root = Path(__file__).parent.parent.parent
    agent_file = project_root / 'agents' / f'{agent_name}.md'

    if not agent_file.exists():
        return 'v1.0'

    # Look for version in frontmatter or default to v1.0
    try:
        with open(agent_file, 'r') as f:
            content = f.read()
            # Simple version extraction (would be more robust in production)
            if 'version:' in content:
                for line in content.split('\n'):
                    if line.strip().startswith('version:'):
                        return line.split(':', 1)[1].strip()
    except:
        pass

    return 'v1.0'


def save_metrics(agent_metrics: List[Dict], system_metrics: Dict) -> None:
    """Save metrics to JSONL files."""
    project_root = Path(__file__).parent.parent.parent
    telemetry_dir = project_root / 'telemetry'

    # Save agent metrics
    agent_metrics_file = telemetry_dir / 'agent_metrics.jsonl'
    with open(agent_metrics_file, 'a') as f:
        for metric in agent_metrics:
            f.write(json.dumps(metric) + '\n')

    # Save system metrics
    system_metrics_file = telemetry_dir / 'system_metrics.jsonl'
    with open(system_metrics_file, 'a') as f:
        f.write(json.dumps(system_metrics) + '\n')


def print_metrics_summary(agent_metrics: List[Dict], system_metrics: Dict) -> None:
    """Print summary of collected metrics."""

    print("\n📊 Metrics Collection Summary")
    print("=" * 70)

    # System metrics
    sm = system_metrics['metrics']
    print(f"\nSystem-Wide Metrics ({system_metrics['period']}):")
    print(f"  Total Invocations: {sm['total_invocations']}")
    print(f"  Active Agents: {sm['total_agents_used']}")
    print(f"  System Success Rate: {sm['system_success_rate']*100:.1f}%")
    print(f"  System False Completion Rate: {sm['system_false_completion_rate']*100:.1f}%")
    print(f"  Avg Resolution Time: {sm['avg_resolution_time_hours']:.1f} hours")

    # Agent health summary
    health_counts = defaultdict(int)
    for metric in agent_metrics:
        health_counts[metric['health']] += 1

    total_agents = len(agent_metrics)
    print(f"\nAgent Health Summary:")
    print(f"  🟢 Green: {health_counts['green']} ({health_counts['green']/total_agents*100:.0f}%)")
    print(f"  🟡 Yellow: {health_counts['yellow']} ({health_counts['yellow']/total_agents*100:.0f}%)")
    print(f"  🔴 Red: {health_counts['red']} ({health_counts['red']/total_agents*100:.0f}%)")

    # Top performers
    top_performers = sorted(agent_metrics,
                          key=lambda x: x['metrics']['success_rate'],
                          reverse=True)[:3]

    print(f"\nTop Performers:")
    for i, metric in enumerate(top_performers, 1):
        name = metric['agent_name']
        sr = metric['metrics']['success_rate']
        fcr = metric['metrics']['false_completion_rate']
        print(f"  {i}. {name}: {sr*100:.0f}% success, {fcr*100:.0f}% false completion")

    # Needs attention
    needs_attention = [m for m in agent_metrics if m['health'] == 'red']

    if needs_attention:
        print(f"\n⚠️  Needs Attention ({len(needs_attention)} agents):")
        for metric in needs_attention:
            name = metric['agent_name']
            sr = metric['metrics']['success_rate']
            fcr = metric['metrics']['false_completion_rate']
            print(f"  ⚠️  {name}: {sr*100:.0f}% success, {fcr*100:.0f}% false completion")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Collect agent and system metrics')
    parser.add_argument('--period', type=str, default='week',
                       choices=['week', 'month'],
                       help='Time period for metrics (default: week)')

    args = parser.parse_args()

    print(f"📈 Collecting metrics for period: {args.period}")

    # Collect metrics
    agent_metrics = collect_agent_metrics(period=args.period)
    system_metrics = collect_system_metrics(period=args.period)

    # Save metrics
    save_metrics(agent_metrics, system_metrics)

    # Print summary
    print_metrics_summary(agent_metrics, system_metrics)

    print(f"\n✓ Metrics saved to:")
    print(f"  - telemetry/agent_metrics.jsonl")
    print(f"  - telemetry/system_metrics.jsonl")

    print(f"\nNext steps:")
    print(f"  - View trends: python3 scripts/phase3/view_trends.py")
    print(f"  - Compare periods: python3 scripts/phase3/compare_metrics.py")


if __name__ == '__main__':
    main()
