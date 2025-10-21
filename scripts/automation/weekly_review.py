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
from telemetry.issue_tracker import IssueTracker, prompt_user_confirmation
import subprocess

def weekly_review():
    print(f"\n📊 Weekly Review: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*70)

    # Step 1: Collect weekly metrics (Phase 3)
    print("\n📈 Collecting Weekly Metrics...")
    metrics_script = Path(__file__).parent.parent / "phase3" / "collect_metrics.py"
    try:
        result = subprocess.run(
            [sys.executable, str(metrics_script), "--period", "week"],
            capture_output=True,
            text=True,
            timeout=30
        )
        # Show the output from the metrics script
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"   {line}")
    except Exception as e:
        print(f"   ⚠️  Metrics collection failed: {e}")
        print("   Continuing with review...")

    # Step 2: Detect false completions (auto-feedback)
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

    # Step 3: Analyze performance
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

    # Step 4: Check for issues needing verification
    tracker = IssueTracker()
    issues_needing_verification = tracker.get_issues_needing_verification()

    if issues_needing_verification:
        print("\n" + "="*70)
        print("Issues Needing Your Verification")
        print("="*70)
        print(f"\n{len(issues_needing_verification)} issue(s) await your confirmation:\n")

        for issue in issues_needing_verification:
            response = prompt_user_confirmation(issue)

            if response == "confirmed":
                tracker.update_state(
                    issue["issue_id"],
                    "resolved",
                    notes="User confirmed issue is fixed",
                    user_confirmed=True,
                    resolved_at=datetime.utcnow().isoformat() + "Z"
                )
                print(f"✓ Issue marked as resolved")

            elif response == "still_broken":
                tracker.update_state(
                    issue["issue_id"],
                    "open",
                    notes="User reports issue still exists - agent false completion",
                    user_confirmed=False,
                    reopened_at=datetime.utcnow().isoformat() + "Z"
                )
                print(f"⚠️  Issue reopened - agent will be flagged for quality review")

            elif response == "will_test_later":
                # Leave in needs_verification state
                print(f"ℹ️  Issue remains in verification queue")

    # Step 5: Show issue statistics
    stats = tracker.get_statistics()
    if stats["total_issues"] > 0:
        print(f"\n📊 Issue Tracking Stats:")
        print(f"   Total Issues: {stats['total_issues']}")
        print(f"   Open: {stats['by_state']['open']}")
        print(f"   Needs Verification: {stats['by_state']['needs_verification']}")
        print(f"   Resolved: {stats['by_state']['resolved']}")

    # Summary
    print("\n✓ Weekly review complete")
    print(f"\n📁 Data Updated:")
    print(f"   - Metrics: telemetry/agent_metrics.jsonl, telemetry/system_metrics.jsonl")
    print(f"   - Issues: telemetry/issues.jsonl")
    print(f"\n📋 View Trends:")
    print(f"   python3 scripts/phase3/view_trends.py")

if __name__ == "__main__":
    weekly_review()
