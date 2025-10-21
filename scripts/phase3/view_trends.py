#!/usr/bin/env python3
"""
View Metrics Trends

Displays metrics trends over time in terminal.

Usage:
  python3 scripts/phase3/view_trends.py
  python3 scripts/phase3/view_trends.py --agent frontend-developer
  python3 scripts/phase3/view_trends.py --metric success_rate
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def load_agent_metrics() -> List[Dict[str, Any]]:
    """Load all agent metrics from JSONL file."""
    project_root = Path(__file__).parent.parent.parent
    metrics_file = project_root / 'telemetry' / 'agent_metrics.jsonl'

    if not metrics_file.exists():
        return []

    metrics = []
    with open(metrics_file, 'r') as f:
        for line in f:
            if line.strip():
                metrics.append(json.loads(line))

    return metrics


def load_system_metrics() -> List[Dict[str, Any]]:
    """Load all system metrics from JSONL file."""
    project_root = Path(__file__).parent.parent.parent
    metrics_file = project_root / 'telemetry' / 'system_metrics.jsonl'

    if not metrics_file.exists():
        return []

    metrics = []
    with open(metrics_file, 'r') as f:
        for line in f:
            if line.strip():
                metrics.append(json.loads(line))

    return metrics


def format_sparkline(values: List[float], width: int = 20) -> str:
    """Create a simple ASCII sparkline."""
    if not values:
        return ' ' * width

    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val if max_val > min_val else 1

    # ASCII characters for different heights
    chars = ' ▁▂▃▄▅▆▇█'

    sparkline = ''
    for val in values[-width:]:  # Last 'width' values
        normalized = (val - min_val) / range_val
        char_index = int(normalized * (len(chars) - 1))
        sparkline += chars[char_index]

    # Pad if not enough values
    if len(values) < width:
        sparkline = ' ' * (width - len(values)) + sparkline

    return sparkline


def determine_trend_arrow(values: List[float]) -> str:
    """Determine if trend is improving, stable, or declining."""
    if len(values) < 2:
        return '→'

    recent = sum(values[-3:]) / len(values[-3:])  # Last 3 measurements
    earlier = sum(values[:-3]) / len(values[:-3]) if len(values) > 3 else values[0]

    diff = (recent - earlier) / earlier if earlier > 0 else 0

    if diff > 0.05:  # >5% improvement
        return '↗️'
    elif diff < -0.05:  # >5% decline
        return '↘️'
    else:
        return '→'


def view_agent_trend(agent_name: str, metric_name: str = 'success_rate') -> None:
    """View trend for a specific agent and metric."""
    metrics = load_agent_metrics()

    # Filter to specific agent
    agent_metrics = [m for m in metrics if m['agent_name'] == agent_name]

    if not agent_metrics:
        print(f"No metrics found for agent: {agent_name}")
        return

    # Sort by timestamp
    agent_metrics = sorted(agent_metrics, key=lambda x: x['timestamp'])

    print(f"\n📊 Metrics Trend: {agent_name}")
    print("=" * 70)

    # Extract values for metric
    if metric_name == 'all':
        metrics_to_show = ['success_rate', 'false_completion_rate', 'avg_resolution_time_hours']
    else:
        metrics_to_show = [metric_name]

    for metric in metrics_to_show:
        values = [m['metrics'][metric] for m in agent_metrics if metric in m['metrics']]

        if not values:
            continue

        latest = values[-1]
        trend = determine_trend_arrow(values)
        sparkline = format_sparkline(values)

        # Format based on metric type
        if 'rate' in metric:
            display = f"{latest*100:.1f}%"
        elif 'time' in metric:
            display = f"{latest:.1f}h"
        else:
            display = f"{latest}"

        metric_display = metric.replace('_', ' ').title()

        print(f"\n{metric_display}:")
        print(f"  Current: {display} {trend}")
        print(f"  Trend:   {sparkline}")
        print(f"  Samples: {len(values)}")

    print()


def view_system_trend() -> None:
    """View system-wide metrics trend."""
    metrics = load_system_metrics()

    if not metrics:
        print("No system metrics found.")
        print("\nRun: python3 scripts/phase3/collect_metrics.py")
        return

    # Sort by timestamp
    metrics = sorted(metrics, key=lambda x: x['timestamp'])

    print("\n📊 System-Wide Metrics Trend")
    print("=" * 70)

    metrics_to_show = [
        ('system_success_rate', 'System Success Rate'),
        ('system_false_completion_rate', 'False Completion Rate'),
        ('avg_resolution_time_hours', 'Avg Resolution Time')
    ]

    for metric_key, metric_display in metrics_to_show:
        values = [m['metrics'][metric_key] for m in metrics if metric_key in m['metrics']]

        if not values:
            continue

        latest = values[-1]
        trend = determine_trend_arrow(values)
        sparkline = format_sparkline(values)

        # Format based on metric type
        if 'rate' in metric_key:
            display = f"{latest*100:.1f}%"
        elif 'time' in metric_key:
            display = f"{latest:.1f}h"
        else:
            display = f"{latest}"

        print(f"\n{metric_display}:")
        print(f"  Current: {display} {trend}")
        print(f"  Trend:   {sparkline}")
        print(f"  Samples: {len(values)}")

    print()


def view_all_agents_summary() -> None:
    """View summary of all agents with trends."""
    metrics = load_agent_metrics()

    if not metrics:
        print("No agent metrics found.")
        print("\nRun: python3 scripts/phase3/collect_metrics.py")
        return

    # Group by agent
    by_agent = defaultdict(list)
    for metric in metrics:
        by_agent[metric['agent_name']].append(metric)

    # Sort each agent's metrics by timestamp
    for agent_name in by_agent:
        by_agent[agent_name] = sorted(by_agent[agent_name], key=lambda x: x['timestamp'])

    print("\n📊 All Agents Summary")
    print("=" * 70)

    print(f"\n{'Agent':<30} {'Success':<10} {'False Comp':<12} {'Health':<8} {'Trend'}")
    print("-" * 70)

    for agent_name in sorted(by_agent.keys()):
        agent_metrics = by_agent[agent_name]
        latest = agent_metrics[-1]

        success_rate = latest['metrics']['success_rate']
        false_comp_rate = latest['metrics']['false_completion_rate']
        health = latest['health']

        # Get trend
        success_values = [m['metrics']['success_rate'] for m in agent_metrics]
        trend = determine_trend_arrow(success_values)

        # Health emoji
        health_emoji = {'green': '🟢', 'yellow': '🟡', 'red': '🔴'}.get(health, '⚪')

        print(f"{agent_name[:29]:<30} {success_rate*100:>6.1f}%   {false_comp_rate*100:>7.1f}%     "
              f"{health_emoji} {health:<6} {trend}")

    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='View metrics trends')
    parser.add_argument('--agent', type=str, default=None,
                       help='View trends for specific agent')
    parser.add_argument('--metric', type=str, default='success_rate',
                       help='Metric to view (default: success_rate, use "all" for all metrics)')
    parser.add_argument('--system', action='store_true',
                       help='View system-wide trends')

    args = parser.parse_args()

    if args.system:
        view_system_trend()
    elif args.agent:
        view_agent_trend(args.agent, args.metric)
    else:
        view_all_agents_summary()


if __name__ == '__main__':
    main()
