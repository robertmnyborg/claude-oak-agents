#!/usr/bin/env python3
"""
Telemetry Analyzer for Claude OaK Agents

Analyzes logged telemetry data and generates performance statistics.
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class TelemetryAnalyzer:
    """Analyzes telemetry logs and generates statistics."""

    def __init__(self, telemetry_dir: Optional[Path] = None):
        """
        Initialize the telemetry analyzer.

        Args:
            telemetry_dir: Directory containing telemetry files.
        """
        if telemetry_dir is None:
            telemetry_dir = Path(__file__).parent

        self.telemetry_dir = Path(telemetry_dir)
        self.invocations_file = self.telemetry_dir / "agent_invocations.jsonl"
        self.metrics_file = self.telemetry_dir / "success_metrics.jsonl"
        self.stats_file = self.telemetry_dir / "performance_stats.json"

    def load_invocations(self) -> List[Dict[str, Any]]:
        """Load all agent invocations from the log file."""
        invocations = []
        if not self.invocations_file.exists():
            return invocations

        with open(self.invocations_file, "r") as f:
            for line in f:
                if line.strip():
                    invocations.append(json.loads(line))
        return invocations

    def load_metrics(self) -> List[Dict[str, Any]]:
        """Load all success metrics from the log file."""
        metrics = []
        if not self.metrics_file.exists():
            return metrics

        with open(self.metrics_file, "r") as f:
            for line in f:
                if line.strip():
                    metrics.append(json.loads(line))
        return metrics

    def generate_statistics(self) -> Dict[str, Any]:
        """
        Generate comprehensive statistics from telemetry data.

        Returns:
            Dictionary containing aggregated statistics
        """
        invocations = self.load_invocations()
        metrics = self.load_metrics()

        if not invocations:
            return {
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "total_invocations": 0,
                "agents": {}
            }

        # Create a lookup for metrics by invocation_id
        metrics_by_inv = {m["invocation_id"]: m for m in metrics}

        # Aggregate by agent
        agent_stats = defaultdict(lambda: {
            "invocation_count": 0,
            "durations": [],
            "successes": 0,
            "failures": 0,
            "quality_ratings": [],
            "task_types": [],
            "error_messages": []
        })

        timestamps = []

        for inv in invocations:
            agent_name = inv["agent_name"]
            agent_stats[agent_name]["invocation_count"] += 1

            if inv.get("duration_seconds"):
                agent_stats[agent_name]["durations"].append(inv["duration_seconds"])

            outcome_status = inv["outcome"].get("status", "unknown")
            if outcome_status == "success":
                agent_stats[agent_name]["successes"] += 1
            elif outcome_status == "failure":
                agent_stats[agent_name]["failures"] += 1
                if inv["outcome"].get("error_message"):
                    agent_stats[agent_name]["error_messages"].append(
                        inv["outcome"]["error_message"]
                    )

            task_type = inv.get("state_features", {}).get("task", {}).get("type")
            if task_type:
                agent_stats[agent_name]["task_types"].append(task_type)

            # Add metrics data
            metric = metrics_by_inv.get(inv["invocation_id"])
            if metric:
                agent_stats[agent_name]["quality_ratings"].append(
                    metric["quality_rating"]
                )

            timestamps.append(inv["timestamp"])

        # Compute final statistics
        final_stats = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total_invocations": len(invocations),
            "date_range": {
                "start": min(timestamps) if timestamps else None,
                "end": max(timestamps) if timestamps else None
            },
            "agents": {}
        }

        for agent_name, stats in agent_stats.items():
            total = stats["successes"] + stats["failures"]
            success_rate = stats["successes"] / total if total > 0 else 0.0

            avg_duration = (
                sum(stats["durations"]) / len(stats["durations"])
                if stats["durations"] else 0.0
            )

            avg_quality = (
                sum(stats["quality_ratings"]) / len(stats["quality_ratings"])
                if stats["quality_ratings"] else 0.0
            )

            # Find most common task types
            task_type_counts = defaultdict(int)
            for tt in stats["task_types"]:
                task_type_counts[tt] += 1
            common_task_types = sorted(
                task_type_counts.items(), key=lambda x: x[1], reverse=True
            )[:3]

            final_stats["agents"][agent_name] = {
                "invocation_count": stats["invocation_count"],
                "success_rate": round(success_rate, 3),
                "average_quality": round(avg_quality, 2),
                "average_duration_seconds": round(avg_duration, 2),
                "common_task_types": [tt[0] for tt in common_task_types],
                "common_failures": stats["error_messages"][:5],  # Top 5
                "recommended_for": self._generate_recommendations(
                    agent_name, stats, success_rate, avg_quality
                )
            }

        return final_stats

    def _generate_recommendations(
        self,
        agent_name: str,
        stats: Dict[str, Any],
        success_rate: float,
        avg_quality: float
    ) -> List[str]:
        """
        Generate recommendations for when to use this agent.

        Args:
            agent_name: Name of the agent
            stats: Raw statistics for the agent
            success_rate: Calculated success rate
            avg_quality: Average quality rating

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # High performers
        if success_rate > 0.8 and avg_quality > 3.5:
            recommendations.append("High success rate - reliable choice")

        # Task type specialization
        task_type_counts = defaultdict(int)
        for tt in stats["task_types"]:
            task_type_counts[tt] += 1

        if task_type_counts:
            most_common = max(task_type_counts.items(), key=lambda x: x[1])
            if most_common[1] >= 3:  # At least 3 instances
                recommendations.append(f"Best for {most_common[0]} tasks")

        # Low performers
        if success_rate < 0.5 and stats["invocation_count"] >= 5:
            recommendations.append("Consider alternative agents - low success rate")

        return recommendations

    def save_statistics(self) -> None:
        """Generate and save statistics to performance_stats.json."""
        stats = self.generate_statistics()

        with open(self.stats_file, "w") as f:
            json.dump(stats, f, indent=2)

        print(f"Statistics saved to {self.stats_file}")

    def print_summary(self) -> None:
        """Print a human-readable summary of statistics."""
        stats = self.generate_statistics()

        print("\n" + "=" * 70)
        print("CLAUDE OAK AGENTS - TELEMETRY SUMMARY")
        print("=" * 70)
        print(f"\nGenerated: {stats['generated_at']}")
        print(f"Total Invocations: {stats['total_invocations']}")

        if stats["date_range"]["start"]:
            print(f"Date Range: {stats['date_range']['start']} to {stats['date_range']['end']}")

        print("\n" + "-" * 70)
        print("AGENT PERFORMANCE")
        print("-" * 70)

        # Sort agents by invocation count
        sorted_agents = sorted(
            stats["agents"].items(),
            key=lambda x: x[1]["invocation_count"],
            reverse=True
        )

        for agent_name, agent_stats in sorted_agents:
            print(f"\n{agent_name}:")
            print(f"  Invocations: {agent_stats['invocation_count']}")
            print(f"  Success Rate: {agent_stats['success_rate'] * 100:.1f}%")
            print(f"  Avg Quality: {agent_stats['average_quality']:.2f}/5.0")
            print(f"  Avg Duration: {agent_stats['average_duration_seconds']:.1f}s")

            if agent_stats["common_task_types"]:
                print(f"  Common Tasks: {', '.join(agent_stats['common_task_types'])}")

            if agent_stats["recommended_for"]:
                print(f"  Recommendations:")
                for rec in agent_stats["recommended_for"]:
                    print(f"    • {rec}")

        print("\n" + "=" * 70)

    def get_agent_ranking(self, task_type: Optional[str] = None) -> List[tuple]:
        """
        Get agents ranked by performance.

        Args:
            task_type: Optional task type to filter by

        Returns:
            List of (agent_name, score) tuples, sorted by score descending
        """
        stats = self.generate_statistics()

        rankings = []
        for agent_name, agent_stats in stats["agents"].items():
            # Filter by task type if specified
            if task_type and task_type not in agent_stats["common_task_types"]:
                continue

            # Compute composite score: weighted average of success_rate and quality
            success_weight = 0.6
            quality_weight = 0.4

            score = (
                success_weight * agent_stats["success_rate"] +
                quality_weight * (agent_stats["average_quality"] / 5.0)
            )

            rankings.append((agent_name, score, agent_stats))

        # Sort by score descending
        rankings.sort(key=lambda x: x[1], reverse=True)

        return rankings


def main():
    """Run telemetry analysis and print summary."""
    analyzer = TelemetryAnalyzer()

    # Generate and save statistics
    analyzer.save_statistics()

    # Print human-readable summary
    analyzer.print_summary()

    # Show top 5 agents overall
    print("\n" + "=" * 70)
    print("TOP 5 AGENTS (Overall Performance)")
    print("=" * 70)

    rankings = analyzer.get_agent_ranking()
    for i, (agent_name, score, stats) in enumerate(rankings[:5], 1):
        print(f"\n{i}. {agent_name} (Score: {score:.3f})")
        print(f"   Success: {stats['success_rate']*100:.1f}% | "
              f"Quality: {stats['average_quality']:.2f}/5 | "
              f"Uses: {stats['invocation_count']}")


if __name__ == "__main__":
    main()
