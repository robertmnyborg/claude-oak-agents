#!/usr/bin/env python3
"""
OaK Phase 5: Agent Portfolio Audit (Agentic HR)

Analyzes agent performance, identifies capability gaps, detects redundancy,
and recommends agent lifecycle actions.

This script is invoked monthly as part of the automated analysis workflow.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from telemetry.analyzer import TelemetryAnalyzer


def load_routing_failures():
    """Load routing failure logs."""
    failures_file = project_root / "telemetry" / "routing_failures.jsonl"

    if not failures_file.exists():
        return []

    failures = []
    with open(failures_file, 'r') as f:
        for line in f:
            if line.strip():
                failures.append(json.loads(line))

    return failures


def analyze_capability_gaps(failures: List[Dict], analyzer: TelemetryAnalyzer) -> List[Dict]:
    """Identify capability gaps from routing failures."""
    # Count failures by domain
    domain_failures = defaultdict(int)
    domain_examples = defaultdict(list)

    for failure in failures:
        domain = failure.get('domain', 'unknown')
        domain_failures[domain] += 1
        domain_examples[domain].append(failure.get('user_request', ''))

    # Identify critical gaps (10+ failures)
    gaps = []
    for domain, count in domain_failures.items():
        if count >= 10:
            gaps.append({
                'domain': domain,
                'failure_count': count,
                'examples': domain_examples[domain][:3],
                'urgency': 'HIGH' if count >= 20 else 'MEDIUM',
                'recommendation': f'create {domain.replace("-", "_")}_agent'
            })
        elif count >= 5:
            gaps.append({
                'domain': domain,
                'failure_count': count,
                'examples': domain_examples[domain][:2],
                'urgency': 'LOW',
                'recommendation': f'monitor or expand existing agent'
            })

    return sorted(gaps, key=lambda x: x['failure_count'], reverse=True)


def analyze_agent_performance(analyzer: TelemetryAnalyzer) -> Dict[str, Any]:
    """Analyze performance of all agents."""
    stats = analyzer.generate_statistics()

    agent_performance = {}
    for agent_name, agent_stats in stats.get('agents', {}).items():
        success_rate = agent_stats.get('success_rate', 0.0)
        invocation_count = agent_stats.get('invocation_count', 0)
        avg_quality = agent_stats.get('average_quality', 0.0)

        # Determine performance category
        if success_rate < 0.7:
            category = 'UNDERPERFORMING'
        elif success_rate >= 0.85:
            category = 'TOP_PERFORMER'
        else:
            category = 'ACCEPTABLE'

        # Determine utilization
        if invocation_count == 0:
            utilization = 'UNUSED'
        elif invocation_count < 5:
            utilization = 'LOW'
        elif invocation_count < 20:
            utilization = 'MEDIUM'
        else:
            utilization = 'HIGH'

        agent_performance[agent_name] = {
            'success_rate': success_rate,
            'invocation_count': invocation_count,
            'avg_quality': avg_quality,
            'category': category,
            'utilization': utilization
        }

    return agent_performance


def generate_agent_audit_report(
    performance: Dict[str, Any],
    gaps: List[Dict],
    period_days: int = 30
) -> str:
    """Generate comprehensive agent audit report."""
    today = datetime.now().strftime("%Y-%m-%d")

    report = f"""# Agent Portfolio Audit Report
**Date**: {today}
**Period**: Last {period_days} days
**Total Agents Analyzed**: {len(performance)}

## Executive Summary

"""

    # Count agents by category
    categories = defaultdict(int)
    utilization_counts = defaultdict(int)
    for agent_data in performance.values():
        categories[agent_data['category']] += 1
        utilization_counts[agent_data['utilization']] += 1

    report += f"""
### Portfolio Health
- **Top Performers**: {categories.get('TOP_PERFORMER', 0)} agents
- **Acceptable Performance**: {categories.get('ACCEPTABLE', 0)} agents
- **Underperforming**: {categories.get('UNDERPERFORMING', 0)} agents
- **Unused**: {utilization_counts.get('UNUSED', 0)} agents

### Capability Gaps
- **Critical Gaps**: {len([g for g in gaps if g['urgency'] == 'HIGH'])} domains
- **Moderate Gaps**: {len([g for g in gaps if g['urgency'] == 'MEDIUM'])} domains
- **Minor Gaps**: {len([g for g in gaps if g['urgency'] == 'LOW'])} domains

"""

    # Top performing agents
    top_performers = [(name, data) for name, data in performance.items()
                      if data['category'] == 'TOP_PERFORMER']
    if top_performers:
        report += "## Top Performing Agents\n\n"
        report += "| Agent | Success Rate | Invocations | Avg Quality |\n"
        report += "|-------|--------------|-------------|--------------|\n"
        for name, data in sorted(top_performers, key=lambda x: x[1]['success_rate'], reverse=True)[:5]:
            report += f"| {name} | {data['success_rate']:.1%} | {data['invocation_count']} | {data['avg_quality']:.1f} |\n"
        report += "\n"

    # Underperforming agents
    underperforming = [(name, data) for name, data in performance.items()
                       if data['category'] == 'UNDERPERFORMING']
    if underperforming:
        report += "## Underperforming Agents\n\n"
        report += "| Agent | Success Rate | Invocations | Recommendation |\n"
        report += "|-------|--------------|-------------|----------------|\n"
        for name, data in sorted(underperforming, key=lambda x: x[1]['success_rate']):
            recommendation = "Refactor" if data['invocation_count'] >= 5 else "Monitor"
            report += f"| {name} | {data['success_rate']:.1%} | {data['invocation_count']} | {recommendation} |\n"
        report += "\n"

    # Unused agents
    unused = [(name, data) for name, data in performance.items()
              if data['utilization'] == 'UNUSED']
    if unused:
        report += "## Unutilized Agents\n\n"
        report += "The following agents have zero invocations:\n\n"
        for name, _ in unused:
            report += f"- **{name}** - Consider deprecation if unused for 90+ days\n"
        report += "\n"

    # Capability gaps
    if gaps:
        report += "## Capability Gaps Detected\n\n"
        # Initialize gap categories before use
        critical_gaps = [g for g in gaps if g['urgency'] == 'HIGH']
        moderate_gaps = [g for g in gaps if g['urgency'] == 'MEDIUM']
        minor_gaps = [g for g in gaps if g['urgency'] == 'LOW']

        if critical_gaps:
            report += "### Critical Gaps (Create New Agent)\n\n"
            for gap in critical_gaps:
                report += f"#### {gap['domain'].upper()}\n"
                report += f"- **Failure Count**: {gap['failure_count']}\n"
                report += f"- **Recommendation**: {gap['recommendation']}\n"
                report += f"- **Example Requests**:\n"
                for example in gap['examples']:
                    report += f"  - {example}\n"
                report += "\n"

        if moderate_gaps:
            report += "### Moderate Gaps (Monitor or Expand)\n\n"
            for gap in moderate_gaps:
                report += f"- **{gap['domain']}**: {gap['failure_count']} failures\n"

        report += "\n"
    else:
        # Initialize empty lists when no gaps exist
        critical_gaps = []
        moderate_gaps = []
        minor_gaps = []

    # Strategic recommendations
    report += "## Strategic Recommendations\n\n"
    report += "### Immediate Actions (This Month)\n\n"

    actions = []
    for gap in gaps:
        if gap['urgency'] == 'HIGH':
            actions.append(f"- **CREATE**: `{gap['recommendation']}` for {gap['domain']} domain")

    for name, data in underperforming:
        if data['invocation_count'] >= 10:
            actions.append(f"- **REFACTOR**: `{name}` (success rate: {data['success_rate']:.1%})")

    for name, data in unused:
        actions.append(f"- **DEPRECATE**: `{name}` (unused)")

    if actions:
        for action in actions[:5]:  # Limit to top 5
            report += action + "\n"
    else:
        report += "- No immediate actions required\n"

    report += "\n### Agent Creation Queue\n\n"
    if critical_gaps:
        report += "The following agents should be created:\n\n"
        for gap in critical_gaps:
            report += f"- [ ] `{gap['recommendation']}` - {gap['domain']}\n"
    else:
        report += "- No new agents needed at this time\n"

    report += "\n## Next Steps\n\n"
    report += "1. Review this report and approve recommended actions\n"
    report += "2. Create approved agents using: `agent-creator`\n"
    report += "3. Monitor new agent performance in next month's audit\n"
    report += "4. Refactor underperforming agents as needed\n"

    return report


def main():
    """Run agent portfolio audit."""
    print("🔍 Running Agent Portfolio Audit...")
    print("=" * 60)

    # Initialize analyzer
    analyzer = TelemetryAnalyzer()

    # Load routing failures
    print("\n📊 Loading routing failures...")
    failures = load_routing_failures()
    print(f"   Found {len(failures)} routing failures")

    # Analyze capability gaps
    print("\n🔎 Analyzing capability gaps...")
    gaps = analyze_capability_gaps(failures, analyzer)
    print(f"   Identified {len(gaps)} capability gaps")

    # Analyze agent performance
    print("\n📈 Analyzing agent performance...")
    performance = analyze_agent_performance(analyzer)
    print(f"   Analyzed {len(performance)} agents")

    # Generate report
    print("\n📝 Generating audit report...")
    report = generate_agent_audit_report(performance, gaps)

    # Save report
    reports_dir = project_root / "reports" / "agent_audit"
    reports_dir.mkdir(parents=True, exist_ok=True)

    report_file = reports_dir / f"audit_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"   ✓ Report saved: {report_file}")

    # Also save JSON for programmatic access
    json_data = {
        'date': datetime.now().isoformat(),
        'performance': performance,
        'gaps': gaps
    }
    json_file = reports_dir / f"audit_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)

    print(f"   ✓ JSON saved: {json_file}")

    print("\n" + "=" * 60)
    print("✓ Agent audit complete!")
    print(f"\nView report: {report_file}")

    # Print summary
    critical_gaps = [g for g in gaps if g['urgency'] == 'HIGH']
    if critical_gaps:
        print(f"\n⚠️  {len(critical_gaps)} critical capability gaps detected!")
        print("   Review report and consider creating new agents.")


if __name__ == "__main__":
    main()
