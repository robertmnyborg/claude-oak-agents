from pathlib import Path
import sys

#!/usr/bin/env python3
"""
Weekly Review

Automated weekly performance review.
"""

import sys
from datetime import datetime, timedelta
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer
from telemetry.feedback_utils import collect_feedback_interactive
import subprocess

def weekly_review():
    print(f"\n📊 Weekly Review: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*70)

    # Step 1: Detect false completions (auto-feedback)
    print("\n🔍 Checking for false completions...")
    script_path = Path(__file__).parent.parent / "detect_false_completions.py"
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        # Show the output from the detection script
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"   {line}")
    except Exception as e:
        print(f"   ⚠️  False completion detection failed: {e}")
        print("   Continuing with review...")

    # Step 2: Analyze performance
    analyzer = TelemetryAnalyzer()
    stats = analyzer.generate_statistics()

    print(f"\nTotal Invocations: {stats['total_invocations']}")
    print(f"Active Agents: {len(stats['agents'])}")

    # Calculate overall success rate
    total_success = sum(a["success_rate"] * a["invocation_count"]
                       for a in stats["agents"].values())
    total_count = sum(a["invocation_count"] for a in stats["agents"].values())
    overall_success = total_success / total_count if total_count > 0 else 0

    print(f"Overall Success Rate: {overall_success*100:.1f}%")

    # Top performers
    top = sorted(stats["agents"].items(),
                key=lambda x: x[1]["success_rate"],
                reverse=True)[:3]

    print("\nTop Performers:")
    for name, agent_stats in top:
        print(f"  ✓ {name}: {agent_stats['success_rate']*100:.0f}% success")

    # Needs attention
    needs_attention = [(name, a) for name, a in stats["agents"].items()
                       if a["success_rate"] < 0.75 and a["invocation_count"] >= 5]

    if needs_attention:
        print("\nNeeds Attention:")
        for name, agent_stats in needs_attention:
            print(f"  ⚠️  {name}: {agent_stats['success_rate']*100:.0f}% success")

        # Collect feedback on agents that need attention
        print("\n" + "="*70)
        print("Optional: Provide feedback on agents needing attention")
        print("="*70)
        for name, agent_stats in needs_attention:
            collect_feedback_interactive(name, "weekly")

    # Generate HTML report
    # TODO: Create detailed HTML report

    print("\n✓ Weekly review complete")

if __name__ == "__main__":
    weekly_review()
