#!/usr/bin/env python3
"""
Monthly Analysis

Comprehensive monthly performance analysis including:
- Agent portfolio audit (via agent-auditor)
- Performance trends
- Curation recommendations
"""

from pathlib import Path
import sys
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer
from telemetry.feedback_utils import collect_feedback_interactive
from telemetry.issue_tracker import IssueTracker, prompt_user_confirmation
from datetime import datetime


def run_agent_audit():
    """Run agent portfolio audit (Agentic HR)."""
    print("\n🤖 Running Agent Portfolio Audit (Agentic HR)...")
    print("-" * 70)

    script_path = Path(__file__).parent.parent / "phase5" / "run_agent_audit.py"

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Agent audit failed: {e}")
        print(e.stdout)
        print(e.stderr)
        return False


def generate_curation_agenda(audit_data: dict):
    """Generate curation agenda from audit findings."""
    print("\n📋 Generating Curation Agenda...")
    print("-" * 70)

    reports_dir = Path(__file__).parent.parent.parent / "reports" / "curation"
    reports_dir.mkdir(parents=True, exist_ok=True)

    agenda_file = reports_dir / f"agenda_{datetime.now().strftime('%Y-%m')}.md"

    agenda = f"""# Curation Agenda - {datetime.now().strftime('%B %Y')}

## Purpose
Monthly review of agent portfolio health and recommended actions based on
agent-auditor analysis.

## Actions Required

### 1. Review Agent Audit Report
- **Location**: `reports/agent_audit/audit_{datetime.now().strftime('%Y-%m-%d')}.md`
- **Review**: Performance metrics, capability gaps, redundancy issues
- **Decision**: Approve or modify recommended actions

### 2. Agent Creation
Review and approve creation of new agents for identified capability gaps.

**Process**:
1. Review gap analysis in audit report
2. Approve agent specifications
3. Run: `agent-creator` for each approved agent
4. Monitor new agents in next monthly audit

### 3. Agent Refactoring
Review underperforming agents and approve refactoring plans.

**Process**:
1. Identify root causes of poor performance
2. Design improvements
3. Implement changes
4. A/B test if significant changes

### 4. Agent Deprecation
Review unused agents and approve deprecation.

**Process**:
1. Confirm agents have no critical dependencies
2. Archive agent specifications
3. Remove from active roster
4. Document deprecation reasoning

## Next Steps

1. [ ] Review agent audit report
2. [ ] Make curation decisions
3. [ ] Execute approved actions
4. [ ] Schedule A/B tests for refactored agents
5. [ ] Update agent documentation

## Notes

Add observations and decisions here during review session.

"""

    with open(agenda_file, 'w') as f:
        f.write(agenda)

    print(f"   ✓ Agenda saved: {agenda_file}")
    return agenda_file


def monthly_analysis():
    """Run comprehensive monthly analysis."""
    print(f"\n📊 Monthly Analysis: {datetime.now().strftime('%B %Y')}")
    print("=" * 70)

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
        print("   Continuing with analysis...")

    # Step 2: Collect metrics (Phase 3)
    print("\n📈 Collecting Monthly Metrics...")
    print("-" * 70)
    metrics_script = Path(__file__).parent.parent / "phase3" / "collect_metrics.py"
    try:
        result = subprocess.run(
            [sys.executable, str(metrics_script), "--period", "month"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"   {line}")
    except Exception as e:
        print(f"   ⚠️  Metrics collection failed: {e}")
        print("   Continuing with analysis...")

    # Step 3: Run root cause analysis (Phase 2)
    print("\n🔍 Analyzing Root Causes...")
    print("-" * 70)
    root_cause_script = Path(__file__).parent.parent / "phase2" / "analyze_root_causes.py"
    try:
        result = subprocess.run(
            [sys.executable, str(root_cause_script), "--min-issues", "2"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"   {line}")
    except Exception as e:
        print(f"   ⚠️  Root cause analysis failed: {e}")
        print("   Continuing with analysis...")

    # Step 4: Run agent portfolio audit (Agentic HR)
    audit_success = run_agent_audit()

    if not audit_success:
        print("\n⚠️  Agent audit failed, but continuing with analysis...")

    # Step 4.5: Agent Performance Trends Analysis (Phase 2)
    print("\n📈 Analyzing agent performance trends...")
    print("-" * 70)
    try:
        analyzer = TelemetryAnalyzer()

        # Get all active agents
        invocations = analyzer.load_invocations()
        active_agents = set(inv['agent_name'] for inv in invocations)

        print(f"\n   Agent Performance Trends (Last 30 Days):")

        improving_agents = []
        declining_agents = []

        for agent_name in sorted(active_agents):
            trend_data = analyzer.get_agent_performance_trends(agent_name, days=30)

            if trend_data['trend'] == 'improving' and trend_data['success_rate_change'] > 0.05:
                improving_agents.append((agent_name, trend_data))
                print(f"   📈 {agent_name}: {trend_data['trend']} "
                      f"({trend_data['recent_success_rate']:.0%} recent vs "
                      f"{trend_data['historical_success_rate']:.0%} historical)")
            elif trend_data['trend'] == 'declining' and trend_data['success_rate_change'] < -0.05:
                declining_agents.append((agent_name, trend_data))
                print(f"   📉 {agent_name}: {trend_data['trend']} "
                      f"({trend_data['recent_success_rate']:.0%} recent vs "
                      f"{trend_data['historical_success_rate']:.0%} historical)")

        # Recommendations
        if declining_agents:
            print(f"\n   ⚠️  Agents Needing Attention ({len(declining_agents)}):")
            for agent_name, trend_data in declining_agents:
                print(f"      - {agent_name}: Review recent failures, consider improvements")

        if improving_agents:
            print(f"\n   ✅ Improving Agents ({len(improving_agents)}):")
            for agent_name, trend_data in improving_agents[:3]:
                print(f"      - {agent_name}: Recent improvements working well")

    except Exception as e:
        print(f"   ⚠️  Performance trend analysis failed: {e}")

    # Step 5: Generate basic telemetry analysis
    print("\n📈 Analyzing Telemetry Data...")
    print("-" * 70)

    try:
        analyzer = TelemetryAnalyzer()
        stats = analyzer.generate_statistics()
        print("   ✓ Telemetry analysis complete")
        print(f"   Total invocations: {stats.get('total_invocations', 0)}")
        print(f"   Unique agents: {len(stats.get('agents', {}))}")

        # Collect feedback on all active agents
        if stats.get('agents'):
            print("\n" + "="*70)
            print("Optional: Provide feedback on active agents")
            print("="*70)

            # Get active agents sorted by invocation count
            active_agents = sorted(
                stats['agents'].items(),
                key=lambda x: x[1]['invocation_count'],
                reverse=True
            )

            for agent_name, agent_stats in active_agents:
                print(f"\n{agent_name}: {agent_stats['invocation_count']} uses, "
                      f"{agent_stats['success_rate']*100:.0f}% success")
                collect_feedback_interactive(agent_name, "monthly")

    except Exception as e:
        print(f"   ⚠️  Analysis failed: {e}")

    # Step 6: Check for issues needing verification
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

    # Step 7: Show issue statistics
    stats_issues = tracker.get_statistics()
    if stats_issues["total_issues"] > 0:
        print(f"\n📊 Issue Tracking Stats:")
        print(f"   Total Issues: {stats_issues['total_issues']}")
        print(f"   Open: {stats_issues['by_state']['open']}")
        print(f"   Needs Verification: {stats_issues['by_state']['needs_verification']}")
        print(f"   Resolved: {stats_issues['by_state']['resolved']}")

    # Step 8: Generate curation agenda
    agenda_file = generate_curation_agenda({})

    # Step 9: Summary
    print("\n" + "=" * 70)
    print("✓ Monthly analysis complete!")
    print(f"\n📁 Reports Generated:")
    print(f"   - Metrics: telemetry/agent_metrics.jsonl, telemetry/system_metrics.jsonl")
    print(f"   - Root Causes: reports/improvement_proposals/{datetime.now().strftime('%Y-%m')}.md")
    print(f"   - Agent Audit: reports/agent_audit/audit_{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"   - Curation Agenda: {agenda_file}")

    print(f"\n📋 Next Steps:")
    print(f"   1. Review improvement proposals (Phase 2)")
    print(f"   2. View metrics trends: python3 scripts/phase3/view_trends.py")
    print(f"   3. Review agent audit report")
    print(f"   4. Review curation agenda")
    print(f"   5. Make decisions on recommended improvements")
    print(f"   6. Apply approved agent improvements")

    return True


if __name__ == "__main__":
    monthly_analysis()
