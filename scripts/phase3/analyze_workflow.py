#!/usr/bin/env python3
"""
Workflow Analysis Tool - Phase 3

Analyze specific workflows or all workflows to identify:
- Bottlenecks
- Parallelization opportunities
- Critical paths
- Dependency conflicts
- Optimization recommendations
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from telemetry.workflow_monitor import WorkflowMonitor


def list_workflows(monitor: WorkflowMonitor):
    """List all available workflows."""
    if not monitor.workflow_events_file.exists():
        print("No workflows found. Run multi-agent tasks to generate workflow data.")
        return []

    workflow_ids = set()
    workflow_info = {}

    with open(monitor.workflow_events_file, "r") as f:
        for line in f:
            if not line.strip():
                continue

            event = json.loads(line)
            wf_id = event.get("workflow_id")
            workflow_ids.add(wf_id)

            if event.get("event") == "workflow_start":
                workflow_info[wf_id] = {
                    "timestamp": event.get("timestamp"),
                    "agents_planned": event.get("agents_planned", [])
                }

    return [(wf_id, workflow_info.get(wf_id, {})) for wf_id in sorted(workflow_ids)]


def analyze_workflow(monitor: WorkflowMonitor, workflow_id: str, verbose: bool = False):
    """Analyze a specific workflow in detail."""

    print("\n" + "=" * 80)
    print(f"  WORKFLOW ANALYSIS: {workflow_id}")
    print("=" * 80)
    print()

    stats = monitor.get_workflow_stats(workflow_id)

    if not stats:
        print(f"✗ Workflow {workflow_id} not found or incomplete")
        return False

    # Basic stats
    print("📊 WORKFLOW STATISTICS")
    print("-" * 80)
    print(f"Total Duration:        {stats['total_duration_seconds']:.1f}s ({stats['total_duration_seconds']/60:.1f} min)")
    print(f"Agent Execution Time:  {stats['agent_execution_time_seconds']:.1f}s")
    print(f"Coordination Overhead: {stats['coordination_overhead_seconds']:.1f}s ({stats['coordination_overhead_pct']:.1f}%)")
    print(f"Number of Agents:      {stats['num_agents']}")
    print(f"Number of Handoffs:    {stats['num_handoffs']}")
    print(f"Status:                {'✓ Success' if stats['success'] else '✗ Failed'}")
    print()

    print(f"Agents Executed: {' → '.join(stats['agents_executed'])}")
    print()

    # Bottleneck analysis
    if stats['bottlenecks']:
        print("⚠️  BOTTLENECKS DETECTED")
        print("-" * 80)
        for bn in stats['bottlenecks']['bottlenecks']:
            print(f"Agent: {bn['agent_name']}")
            print(f"  Duration: {bn['duration_seconds']:.1f}s")
            print(f"  Percentage: {bn['percentage_of_workflow']:.1f}% of workflow time")
            print(f"  Impact: Slowing down overall workflow")
            print()
        print("💡 Recommendation: Optimize or split the bottleneck agent's work")
        print()

    # Parallelization opportunities
    if stats['parallelization_opportunities']:
        print("⚡ PARALLELIZATION OPPORTUNITIES")
        print("-" * 80)
        print(f"Found {len(stats['parallelization_opportunities'])} pairs that could run in parallel:")
        for agent_a, agent_b in stats['parallelization_opportunities']:
            print(f"  • {agent_a} || {agent_b}")
        print()
        print("💡 Recommendation: Restructure workflow to execute these agents in parallel")
        est_speedup = len(stats['parallelization_opportunities']) * 15  # Rough estimate
        print(f"   Estimated speedup: 20-30% faster workflow execution")
        print()

    # Critical path
    if stats['critical_path']:
        cp = stats['critical_path']
        print("🎯 CRITICAL PATH ANALYSIS")
        print("-" * 80)
        print(f"Path: {' → '.join(cp['critical_path'])}")
        print(f"Duration: {cp['duration_seconds']:.1f}s")
        print(f"Percentage: {cp['percentage_of_total']:.1f}% of agent execution time")
        print()
        print("💡 Critical path determines minimum possible workflow duration")
        print("   Focus optimization efforts on agents in this path")
        print()

    # Conflicts
    if stats['conflicts']:
        print("⚠️  DEPENDENCY CONFLICTS")
        print("-" * 80)
        for conflict in stats['conflicts']:
            print(f"Type: {conflict['type']}")
            print(f"  File: {conflict['file_path']}")
            print(f"  Agents: {', '.join(conflict['agents'])}")
            print(f"  Severity: {conflict['severity']}")
            print()
        print("💡 Recommendation: Review file modification order to prevent conflicts")
        print()

    # Overall assessment
    print("=" * 80)
    print("  OVERALL ASSESSMENT")
    print("=" * 80)
    print()

    # Coordination overhead assessment
    if stats['coordination_overhead_pct'] > 30:
        print("🔴 HIGH COORDINATION OVERHEAD (>30%)")
        print("   Consider Phase 3 optimizations to reduce handoff time")
    elif stats['coordination_overhead_pct'] > 15:
        print("🟡 MODERATE COORDINATION OVERHEAD (15-30%)")
        print("   Monitor overhead, consider optimizations if it increases")
    else:
        print("🟢 LOW COORDINATION OVERHEAD (<15%)")
        print("   Workflow coordination is efficient")

    print()

    # Bottleneck assessment
    if stats['bottlenecks']:
        max_bn = max(stats['bottlenecks']['bottlenecks'],
                    key=lambda x: x['percentage_of_workflow'])
        if max_bn['percentage_of_workflow'] > 40:
            print("🔴 SEVERE BOTTLENECK DETECTED")
            print(f"   {max_bn['agent_name']} is consuming {max_bn['percentage_of_workflow']:.1f}% of workflow time")
            print("   Priority: HIGH - Address immediately")
        elif max_bn['percentage_of_workflow'] > 25:
            print("🟡 MODERATE BOTTLENECK DETECTED")
            print(f"   {max_bn['agent_name']} is consuming {max_bn['percentage_of_workflow']:.1f}% of workflow time")
            print("   Priority: MEDIUM - Monitor and consider optimization")

    print()

    # Success summary
    if stats['success']:
        print("✓ Workflow completed successfully")
    else:
        print("✗ Workflow failed - investigate failure causes")

    print()

    return True


def analyze_all_workflows(monitor: WorkflowMonitor):
    """Analyze all workflows and provide summary."""

    workflows = list_workflows(monitor)

    if not workflows:
        print("No workflows to analyze")
        return

    print("\n" + "=" * 80)
    print(f"  ANALYZING {len(workflows)} WORKFLOWS")
    print("=" * 80)
    print()

    total_duration = 0
    total_overhead = 0
    bottleneck_count = 0
    parallelization_count = 0
    conflict_count = 0

    for wf_id, info in workflows:
        stats = monitor.get_workflow_stats(wf_id)
        if not stats:
            continue

        total_duration += stats['total_duration_seconds']
        total_overhead += stats['coordination_overhead_seconds']

        if stats['bottlenecks']:
            bottleneck_count += 1

        parallelization_count += len(stats['parallelization_opportunities'])
        conflict_count += len(stats['conflicts'])

    avg_duration = total_duration / len(workflows) if workflows else 0
    avg_overhead_pct = (total_overhead / total_duration * 100) if total_duration > 0 else 0

    print(f"Total Workflows: {len(workflows)}")
    print(f"Average Duration: {avg_duration:.1f}s ({avg_duration/60:.1f} min)")
    print(f"Average Coordination Overhead: {avg_overhead_pct:.1f}%")
    print()
    print(f"Workflows with Bottlenecks: {bottleneck_count} ({bottleneck_count/len(workflows)*100:.0f}%)")
    print(f"Total Parallelization Opportunities: {parallelization_count}")
    print(f"Total Conflicts Detected: {conflict_count}")
    print()

    # Recommendations
    print("=" * 80)
    print("  SYSTEM-WIDE RECOMMENDATIONS")
    print("=" * 80)
    print()

    if avg_overhead_pct > 30:
        print("🔴 System-wide coordination overhead is HIGH (>30%)")
        print("   Recommendation: Implement Phase 3 optimizations")
        print("   - Reduce context size in handoffs")
        print("   - Optimize agent selection")
        print("   - Consider workflow restructuring")
    elif avg_overhead_pct > 15:
        print("🟡 System-wide coordination overhead is MODERATE (15-30%)")
        print("   Recommendation: Monitor and consider targeted optimizations")
    else:
        print("🟢 System-wide coordination overhead is EFFICIENT (<15%)")
        print("   Current workflow patterns are working well")

    print()

    if parallelization_count > len(workflows) * 2:
        print(f"⚡ SIGNIFICANT parallelization opportunities detected")
        print(f"   {parallelization_count} opportunities across {len(workflows)} workflows")
        print("   Recommendation: Restructure common workflow patterns")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Analyze workflow performance and identify optimization opportunities"
    )
    parser.add_argument(
        "workflow_id",
        nargs="?",
        help="Specific workflow ID to analyze (optional, analyzes all if omitted)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available workflows"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Initialize monitor
    telemetry_dir = Path(__file__).parent.parent.parent / "telemetry"
    monitor = WorkflowMonitor(telemetry_dir)

    # List workflows if requested
    if args.list:
        workflows = list_workflows(monitor)
        if not workflows:
            print("No workflows found")
            return

        print("\n📋 Available Workflows:")
        print("=" * 80)
        for wf_id, info in workflows:
            timestamp = info.get("timestamp", "unknown")
            agents = info.get("agents_planned", [])
            print(f"\n{wf_id}")
            print(f"  Timestamp: {timestamp}")
            if agents:
                print(f"  Agents: {', '.join(agents)}")
        print()
        return

    # Analyze specific workflow or all
    if args.workflow_id:
        analyze_workflow(monitor, args.workflow_id, args.verbose)
    else:
        analyze_all_workflows(monitor)


if __name__ == "__main__":
    main()
