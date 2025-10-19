#!/usr/bin/env python3
"""
Setup Automation Scripts

This script generates all automation scripts for Phases 4-6.
Run once to create the complete automation infrastructure.

Usage:
    python scripts/setup_automation.py
"""

import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent

# Script templates
SCRIPTS = {
    # Phase 4: Transition Models & Utility Tracking
    "phase4/generate_transition_models.py": """#!/usr/bin/env python3
'''
Generate Transition Models

Analyzes telemetry data and creates transition_expectations.yaml
with expected behavior for each agent.
'''

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer
from collections import defaultdict
import yaml

def generate_transition_models():
    analyzer = TelemetryAnalyzer()
    stats = analyzer.generate_statistics()

    models = {"agents": {}}

    for agent_name, agent_stats in stats["agents"].items():
        models["agents"][agent_name] = {
            "expected_duration_minutes": [
                int(agent_stats["average_duration_seconds"] / 60 * 0.5),
                int(agent_stats["average_duration_seconds"] / 60 * 1.5)
            ],
            "success_rate": round(agent_stats["success_rate"], 2),
            "average_quality": round(agent_stats["average_quality"], 1),
            "common_task_types": agent_stats["common_task_types"],
            "preconditions": [],  # TODO: Manual input required
            "postconditions": [],  # TODO: Manual input required
        }

    output_file = PROJECT_ROOT / "models" / "transition_expectations.yaml"
    with open(output_file, "w") as f:
        yaml.dump(models, f, default_flow_style=False)

    print(f"✓ Generated transition models: {output_file}")
    print("\\nNext: Review and add preconditions/postconditions")
    print(f"  python scripts/phase4/review_transition_models.py")

if __name__ == "__main__":
    generate_transition_models()
""",

    "phase4/batch_feedback.py": """#!/usr/bin/env python3
'''
Batch Feedback Tool

Allows bulk rating of agent invocations from a specified time period.
'''

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

    print(f"\\n📊 Batch Feedback for Last {days} Days")
    print(f"Total invocations: {len(recent)}\\n")

    for i, inv in enumerate(recent, 1):
        print(f"\\n[{i}/{len(recent)}] {inv['agent_name']}")
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
            print("\\n\\nExiting batch feedback...")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    batch_feedback(args.days)
""",

    "phase4/generate_dashboard.py": """#!/usr/bin/env python3
'''
Generate Performance Dashboard

Creates HTML dashboard with charts showing agent performance.
'''

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer
from datetime import datetime

def generate_dashboard():
    analyzer = TelemetryAnalyzer()
    stats = analyzer.generate_statistics()

    # TODO: Use plotly or matplotlib to create charts
    # For now, generate simple HTML report

    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>OaK Agents Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .metric {{ background: #f0f0f0; padding: 20px; margin: 10px 0; border-radius: 5px; }}
        .agent {{ margin: 20px 0; padding: 15px; border-left: 4px solid #4CAF50; }}
    </style>
</head>
<body>
    <h1>Claude OaK Agents Dashboard</h1>
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>

    <div class="metric">
        <h2>Summary</h2>
        <p>Total Invocations: {stats['total_invocations']}</p>
        <p>Unique Agents: {len(stats['agents'])}</p>
    </div>

    <h2>Agent Performance</h2>
'''

    for agent_name, agent_stats in sorted(stats['agents'].items(),
                                         key=lambda x: x[1]['invocation_count'],
                                         reverse=True):
        html += f'''
    <div class="agent">
        <h3>{agent_name}</h3>
        <p>Invocations: {agent_stats['invocation_count']}</p>
        <p>Success Rate: {agent_stats['success_rate']*100:.1f}%</p>
        <p>Average Quality: {agent_stats['average_quality']:.2f}/5.0</p>
        <p>Average Duration: {agent_stats['average_duration_seconds']:.0f}s</p>
    </div>
'''

    html += '''
</body>
</html>
'''

    output_file = PROJECT_ROOT / "reports" / f"dashboard_{datetime.now().strftime('%Y-%m-%d')}.html"
    with open(output_file, "w") as f:
        f.write(html)

    print(f"✓ Dashboard generated: {output_file}")
    print(f"  Open with: open {output_file}")

if __name__ == "__main__":
    generate_dashboard()
""",

    # Phase 5: Adaptive Curation
    "phase5/audit_agents.py": """#!/usr/bin/env python3
'''
Agent Performance Audit

Comprehensive analysis of all agents to identify improvement candidates.
'''

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

    print("\\n📊 Agent Performance Audit")
    print("="*70)

    print("\\nHIGH PERFORMERS (>0.85 success, >4.0 quality):")
    for name, success, quality, count in high_performers:
        print(f"  ✓ {name}: {success:.2f} success, {quality:.1f} quality, {count} uses")

    print("\\nNEEDS IMPROVEMENT (<0.70 success OR <3.5 quality):")
    for name, success, quality, count in needs_improvement:
        print(f"  ⚠️  {name}: {success:.2f} success, {quality:.1f} quality, {count} uses")

    print("\\nUNDERUTILIZED (<5 uses despite high scores):")
    for name, success, quality, count in underutilized:
        print(f"  📉 {name}: {success:.2f} success, {quality:.1f} quality, {count} uses")

    # Save detailed report
    output_file = PROJECT_ROOT / "reports" / f"agent_audit_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(output_file, "w") as f:
        f.write("# Agent Performance Audit\\n\\n")
        f.write(f"Generated: {datetime.now()}\\n\\n")
        # TODO: Write detailed report

    print(f"\\n✓ Detailed report saved: {output_file}")

if __name__ == "__main__":
    from datetime import datetime
    audit_agents()
""",

    # Phase 6: ML Pipeline
    "phase6/prepare_training_data.py": """#!/usr/bin/env python3
'''
Prepare Training Data

Preprocesses telemetry data for machine learning.
'''

import sys
import json
import random
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer

def prepare_training_data():
    analyzer = TelemetryAnalyzer()
    invocations = analyzer.load_invocations()
    metrics = analyzer.load_metrics()

    # Create lookup for metrics
    metrics_by_inv = {m["invocation_id"]: m for m in metrics}

    # Prepare dataset
    dataset = []
    for inv in invocations:
        if inv["invocation_id"] in metrics_by_inv:
            metric = metrics_by_inv[inv["invocation_id"]]

            record = {
                "state_features": inv["state_features"],
                "agent_name": inv["agent_name"],
                "outcome": inv["outcome"]["status"],
                "duration": inv.get("duration_seconds", 0),
                "quality": metric["quality_rating"],
                "success": metric["success"]
            }
            dataset.append(record)

    # Split dataset
    random.shuffle(dataset)
    train_size = int(len(dataset) * 0.7)
    val_size = int(len(dataset) * 0.2)

    train = dataset[:train_size]
    val = dataset[train_size:train_size+val_size]
    test = dataset[train_size+val_size:]

    # Save datasets
    ml_dir = PROJECT_ROOT / "docs" / "experimental" / "phase6" / "ml-data"
    ml_dir.mkdir(parents=True, exist_ok=True)

    for name, data in [("train", train), ("val", val), ("test", test)]:
        with open(ml_dir / f"{name}.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"✓ Saved {len(data)} records to {name}.json")

    print(f"\\nTotal: {len(dataset)} records")
    print(f"Train: {len(train)} (70%)")
    print(f"Val: {len(val)} (20%)")
    print(f"Test: {len(test)} (10%)")

    print("\\nNext: Validate data quality")
    print("  python scripts/phase6/validate_training_data.py")

if __name__ == "__main__":
    prepare_training_data()
""",

    # Automation
    "automation/weekly_review.py": """#!/usr/bin/env python3
'''
Weekly Review

Automated weekly performance review.
'''

import sys
from datetime import datetime, timedelta
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer

def weekly_review():
    print(f"\\n📊 Weekly Review: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*70)

    analyzer = TelemetryAnalyzer()
    stats = analyzer.generate_statistics()

    print(f"\\nTotal Invocations: {stats['total_invocations']}")
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

    print("\\nTop Performers:")
    for name, agent_stats in top:
        print(f"  ✓ {name}: {agent_stats['success_rate']*100:.0f}% success")

    # Needs attention
    needs_attention = [(name, a) for name, a in stats["agents"].items()
                       if a["success_rate"] < 0.75 and a["invocation_count"] >= 5]

    if needs_attention:
        print("\\nNeeds Attention:")
        for name, agent_stats in needs_attention:
            print(f"  ⚠️  {name}: {agent_stats['success_rate']*100:.0f}% success")

    # Generate HTML report
    # TODO: Create detailed HTML report

    print("\\n✓ Weekly review complete")

if __name__ == "__main__":
    weekly_review()
""",

    "automation/monthly_analysis.py": """#!/usr/bin/env python3
'''
Monthly Analysis

Comprehensive monthly performance analysis.
'''

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer
from datetime import datetime

def monthly_analysis():
    print(f"\\n📊 Monthly Analysis: {datetime.now().strftime('%B %Y')}")
    print("="*70)

    analyzer = TelemetryAnalyzer()
    stats = analyzer.generate_statistics()

    # TODO: Comprehensive analysis
    # - Month-over-month trends
    # - Agent improvement tracking
    # - ROI calculations
    # - Recommendations for next month

    print("\\n✓ Monthly analysis complete")
    print("  See: reports/monthly/")

if __name__ == "__main__":
    monthly_analysis()
""",

    "automation/health_check.py": """#!/usr/bin/env python3
'''
Daily Health Check

Verifies system is functioning correctly.
'''

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def health_check():
    PROJECT_ROOT = Path(__file__).parent.parent.parent

    checks = []

    # Check 1: Telemetry directory writable
    telemetry_dir = PROJECT_ROOT / "telemetry"
    try:
        test_file = telemetry_dir / ".health_check"
        test_file.touch()
        test_file.unlink()
        checks.append(("Telemetry writable", True))
    except Exception as e:
        checks.append(("Telemetry writable", False, str(e)))

    # Check 2: Hooks installed
    hooks_dir = Path.home() / ".claude" / "hooks"
    pre_hook = hooks_dir / "pre_agent.sh"
    post_hook = hooks_dir / "post_agent.sh"

    checks.append(("Pre-hook installed", pre_hook.exists()))
    checks.append(("Post-hook installed", post_hook.exists()))

    # Check 3: Recent invocations
    inv_file = telemetry_dir / "agent_invocations.jsonl"
    if inv_file.exists():
        lines = inv_file.read_text().strip().split("\\n")
        checks.append(("Recent invocations", len(lines) > 0))
    else:
        checks.append(("Recent invocations", False))

    # Report
    print(f"\\n🏥 Health Check: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    all_pass = True

    for check in checks:
        if check[1]:
            print(f"  ✓ {check[0]}")
        else:
            print(f"  ✗ {check[0]}")
            if len(check) > 2:
                print(f"    Error: {check[2]}")
            all_pass = False

    if all_pass:
        print("\\n✓ All checks passed")
        return 0
    else:
        print("\\n⚠️  Some checks failed")
        return 1

if __name__ == "__main__":
    from datetime import datetime
    sys.exit(health_check())
""",
}

def create_script(path, content):
    """Create a script file with proper header."""
    full_path = PROJECT_ROOT / "scripts" / path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    # Add imports
    imports = """from pathlib import Path\nimport sys\n\n"""
    final_content = content.replace("'''", '"""', 1).replace("'''", '"""', 1)
    final_content = imports + final_content

    full_path.write_text(final_content)
    full_path.chmod(0o755)  # Make executable

    return full_path

def main():
    print("🚀 Setting up OaK Automation Scripts")
    print("="*70)

    created = []
    for script_path, content in SCRIPTS.items():
        path = create_script(script_path, content)
        created.append(path)
        print(f"✓ Created: scripts/{script_path}")

    print(f"\\n✓ Generated {len(created)} automation scripts")

    # Create placeholder README files
    for phase_dir in ["phase4", "phase5", "phase6", "automation"]:
        readme = PROJECT_ROOT / "scripts" / phase_dir / "README.md"
        readme.write_text(f"# {phase_dir.title()} Scripts\\n\\nAutomation scripts for {phase_dir}.\\n")

    print("\\n📖 Next Steps:")
    print("  1. Review generated scripts in scripts/")
    print("  2. Test with: python scripts/automation/health_check.py")
    print("  3. Follow 6-Month Deployment Plan")

    return 0

if __name__ == "__main__":
    sys.exit(main())
