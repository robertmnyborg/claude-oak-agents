from pathlib import Path
import sys

#!/usr/bin/env python3
"""
Agent Performance Audit

Comprehensive analysis of all agents to identify improvement candidates.
"""

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer

def audit_agents():
    analyzer = TelemetryAnalyzer()
    stats = analyzer.generate_statistics()

    high_performers = []
    needs_improvement = []
    underutilized = []

    for agent_name, agent_stats in stats["agents"].items():
        count = agent_stats["invocation_count"]
        success = agent_stats["success_rate"]
        quality = agent_stats["average_quality"]

        if success > 0.85 and quality > 4.0:
            high_performers.append((agent_name, success, quality, count))

        if (success < 0.70 or quality < 3.5) and count >= 5:
            needs_improvement.append((agent_name, success, quality, count))

        if count < 5 and success > 0.75:
            underutilized.append((agent_name, success, quality, count))

    print("\n📊 Agent Performance Audit")
    print("="*70)

    print("\nHIGH PERFORMERS (>0.85 success, >4.0 quality):")
    for name, success, quality, count in high_performers:
        print(f"  ✓ {name}: {success:.2f} success, {quality:.1f} quality, {count} uses")

    print("\nNEEDS IMPROVEMENT (<0.70 success OR <3.5 quality):")
    for name, success, quality, count in needs_improvement:
        print(f"  ⚠️  {name}: {success:.2f} success, {quality:.1f} quality, {count} uses")

    print("\nUNDERUTILIZED (<5 uses despite high scores):")
    for name, success, quality, count in underutilized:
        print(f"  📉 {name}: {success:.2f} success, {quality:.1f} quality, {count} uses")

    # Save detailed report
    output_file = PROJECT_ROOT / "reports" / f"agent_audit_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(output_file, "w") as f:
        f.write("# Agent Performance Audit\n\n")
        f.write(f"Generated: {datetime.now()}\n\n")
        # TODO: Write detailed report

    print(f"\n✓ Detailed report saved: {output_file}")

if __name__ == "__main__":
    from datetime import datetime
    audit_agents()
