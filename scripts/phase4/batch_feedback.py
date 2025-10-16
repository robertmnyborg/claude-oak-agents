from pathlib import Path
import sys

#!/usr/bin/env python3
"""
Batch Feedback Tool

Allows bulk rating of agent invocations from a specified time period.
"""

import sys
import argparse
from datetime import datetime, timedelta
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.logger import TelemetryLogger
from telemetry.analyzer import TelemetryAnalyzer

def batch_feedback(days=7):
    analyzer = TelemetryAnalyzer()
    invocations = analyzer.load_invocations()

    # Filter to recent invocations
    cutoff = datetime.utcnow() - timedelta(days=days)
    recent = [inv for inv in invocations
              if datetime.fromisoformat(inv["timestamp"].replace('Z', '+00:00')) > cutoff]

    logger = TelemetryLogger()

    print(f"\n📊 Batch Feedback for Last {days} Days")
    print(f"Total invocations: {len(recent)}\n")

    for i, inv in enumerate(recent, 1):
        print(f"\n[{i}/{len(recent)}] {inv['agent_name']}")
        print(f"  Task: {inv['task_description'][:60]}...")
        print(f"  Duration: {inv.get('duration_seconds', 0)/60:.1f} min")
        print(f"  Outcome: {inv['outcome']['status']}")

        try:
            success = input("  Success? (y/n/skip): ").lower()
            if success == "skip":
                continue

            quality = input("  Quality (1-5): ")
            notes = input("  Notes (optional): ")

            logger.log_success_metric(
                invocation_id=inv["invocation_id"],
                success=(success == "y"),
                quality_rating=int(quality) if quality.isdigit() else 3,
                feedback_source="human",
                feedback_notes=notes or "Batch feedback"
            )

            print("  ✓ Recorded")

        except KeyboardInterrupt:
            print("\n\nExiting batch feedback...")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    batch_feedback(args.days)
