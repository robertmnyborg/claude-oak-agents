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

    # 1. Run agent portfolio audit (Agentic HR)
    audit_success = run_agent_audit()

    if not audit_success:
        print("\n⚠️  Agent audit failed, but continuing with analysis...")

    # 2. Generate basic telemetry analysis
    print("\n📈 Analyzing Telemetry Data...")
    print("-" * 70)

    try:
        analyzer = TelemetryAnalyzer()
        stats = analyzer.generate_statistics()
        print("   ✓ Telemetry analysis complete")
        print(f"   Total invocations: {stats.get('total_invocations', 0)}")
        print(f"   Unique agents: {len(stats.get('agents', {}))}")
    except Exception as e:
        print(f"   ⚠️  Analysis failed: {e}")

    # 3. Generate curation agenda
    agenda_file = generate_curation_agenda({})

    # 4. Summary
    print("\n" + "=" * 70)
    print("✓ Monthly analysis complete!")
    print(f"\n📁 Reports Generated:")
    print(f"   - Agent Audit: reports/agent_audit/audit_{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"   - Curation Agenda: {agenda_file}")

    print(f"\n📋 Next Steps:")
    print(f"   1. Review agent audit report")
    print(f"   2. Review curation agenda")
    print(f"   3. Make decisions on recommended actions")
    print(f"   4. Execute approved agent creation/refactoring/deprecation")

    return True


if __name__ == "__main__":
    monthly_analysis()
