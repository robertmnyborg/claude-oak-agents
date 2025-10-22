#!/usr/bin/env python3
"""
Demo: Multi-Agent Workflow Coordination

Demonstrates the Phase 2 workflow tracking and agent selection features.
"""

import sys
import tempfile
import time
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from telemetry.logger import TelemetryLogger
from telemetry.analyzer import TelemetryAnalyzer
from scripts.query_best_agent import query_best_agent


def create_sample_telemetry_data(logger: TelemetryLogger):
    """Create sample telemetry data for demonstration."""
    
    print("\nPopulating sample telemetry data...")
    
    # Scenario 1: Backend API Development (3 tasks)
    for i in range(3):
        inv_id = logger.log_invocation(
            agent_name="backend-architect",
            agent_type="development",
            task_description=f"Build REST API endpoints for user management (task {i+1})",
            state_features={
                "task": {"type": "api_development"},
                "codebase": {"languages": ["TypeScript", "Node.js"]}
            }
        )
        logger.update_invocation(
            invocation_id=inv_id,
            duration_seconds=1200 + (i * 100),
            outcome_status="success",
            files_created=[f"src/api/users-{i}.ts"]
        )
        logger.log_success_metric(
            invocation_id=inv_id,
            success=True,
            quality_rating=4 + (i % 2)
        )
    
    # Scenario 2: Frontend Development (4 tasks)
    for i in range(4):
        inv_id = logger.log_invocation(
            agent_name="frontend-developer",
            agent_type="development",
            task_description=f"Implement React components for dashboard (task {i+1})",
            state_features={
                "task": {"type": "ui_development"},
                "codebase": {"languages": ["TypeScript", "React"]}
            }
        )
        logger.update_invocation(
            invocation_id=inv_id,
            duration_seconds=900 + (i * 50),
            outcome_status="success" if i < 3 else "partial",
            files_created=[f"src/components/Dashboard-{i}.tsx"]
        )
        logger.log_success_metric(
            invocation_id=inv_id,
            success=i < 3,
            quality_rating=4 if i < 3 else 3
        )
    
    # Scenario 3: Security Audit (2 tasks)
    for i in range(2):
        inv_id = logger.log_invocation(
            agent_name="security-auditor",
            agent_type="security",
            task_description=f"Perform security audit on authentication system (task {i+1})",
            state_features={
                "task": {"type": "security_audit"},
                "codebase": {"languages": ["TypeScript"]}
            }
        )
        logger.update_invocation(
            invocation_id=inv_id,
            duration_seconds=2400 + (i * 200),
            outcome_status="success",
            files_created=[f"reports/security-audit-{i}.md"]
        )
        logger.log_success_metric(
            invocation_id=inv_id,
            success=True,
            quality_rating=5
        )
    
    # Scenario 4: Database Design (2 tasks)
    for i in range(2):
        inv_id = logger.log_invocation(
            agent_name="backend-architect",
            agent_type="development",
            task_description=f"Design database schema for e-commerce platform (task {i+1})",
            state_features={
                "task": {"type": "database_design"},
                "codebase": {"languages": ["SQL", "PostgreSQL"]}
            }
        )
        logger.update_invocation(
            invocation_id=inv_id,
            duration_seconds=1800 + (i * 150),
            outcome_status="success",
            files_created=[f"schema/migrations-{i}.sql"]
        )
        logger.log_success_metric(
            invocation_id=inv_id,
            success=True,
            quality_rating=5
        )
    
    print("  Created 11 agent invocations across 4 scenarios")


def demo_workflow_tracking(logger: TelemetryLogger):
    """Demonstrate workflow tracking."""
    
    print("\n" + "="*70)
    print("DEMO: WORKFLOW TRACKING")
    print("="*70)
    
    # Multi-agent workflow: E-Commerce Platform
    workflow_id = "demo-workflow-ecommerce"
    
    print(f"\nStarting workflow: {workflow_id}")
    logger.log_workflow_start(
        workflow_id=workflow_id,
        project_name="E-Commerce Platform MVP",
        agent_plan=["systems-architect", "backend-architect", "frontend-developer", "qa-specialist"],
        estimated_duration=14400  # 4 hours
    )
    
    # Agent 1: Systems Architect
    print("  [1/4] systems-architect: Designing architecture...")
    inv1 = logger.log_invocation(
        agent_name="systems-architect",
        agent_type="architecture",
        task_description="Design scalable architecture for e-commerce platform",
        state_features={"task": {"type": "architecture_design"}}
    )
    time.sleep(0.1)
    logger.update_invocation(inv1, duration_seconds=2400, outcome_status="success")
    logger.log_success_metric(inv1, success=True, quality_rating=5)
    
    logger.log_agent_handoff(
        workflow_id=workflow_id,
        from_agent="systems-architect",
        to_agent="backend-architect",
        artifacts=["artifacts/architecture.md", "artifacts/tech-stack.md"]
    )
    
    # Agent 2: Backend Architect
    print("  [2/4] backend-architect: Implementing backend...")
    inv2 = logger.log_invocation(
        agent_name="backend-architect",
        agent_type="development",
        task_description="Implement REST API and database",
        state_features={"task": {"type": "api_development"}}
    )
    time.sleep(0.1)
    logger.update_invocation(inv2, duration_seconds=4800, outcome_status="success")
    logger.log_success_metric(inv2, success=True, quality_rating=4)
    
    logger.log_agent_handoff(
        workflow_id=workflow_id,
        from_agent="backend-architect",
        to_agent="frontend-developer",
        artifacts=["src/api/", "database/schema.sql"]
    )
    
    # Agent 3: Frontend Developer
    print("  [3/4] frontend-developer: Building UI...")
    inv3 = logger.log_invocation(
        agent_name="frontend-developer",
        agent_type="development",
        task_description="Build React frontend with product catalog",
        state_features={"task": {"type": "ui_development"}}
    )
    time.sleep(0.1)
    logger.update_invocation(inv3, duration_seconds=5400, outcome_status="success")
    logger.log_success_metric(inv3, success=True, quality_rating=4)
    
    logger.log_agent_handoff(
        workflow_id=workflow_id,
        from_agent="frontend-developer",
        to_agent="qa-specialist",
        artifacts=["src/components/", "src/pages/"]
    )
    
    # Agent 4: QA Specialist
    print("  [4/4] qa-specialist: Testing...")
    inv4 = logger.log_invocation(
        agent_name="qa-specialist",
        agent_type="quality",
        task_description="Integration testing for e-commerce workflows",
        state_features={"task": {"type": "integration_testing"}}
    )
    time.sleep(0.1)
    logger.update_invocation(inv4, duration_seconds=1800, outcome_status="success")
    logger.log_success_metric(inv4, success=True, quality_rating=5)
    
    # Complete workflow
    print("\nWorkflow completed successfully!")
    logger.log_workflow_complete(
        workflow_id=workflow_id,
        duration_seconds=14400,
        success=True,
        agents_executed=["systems-architect", "backend-architect", "frontend-developer", "qa-specialist"]
    )


def demo_agent_selection(logger: TelemetryLogger):
    """Demonstrate agent selection queries."""

    print("\n" + "="*70)
    print("DEMO: AGENT SELECTION")
    print("="*70)

    # Create analyzer for this telemetry directory
    analyzer = TelemetryAnalyzer(telemetry_dir=logger.telemetry_dir)
    invocations = analyzer.load_invocations()

    if not invocations:
        print("\nNo telemetry data available for queries")
        return

    test_queries = [
        ("API development", "backend"),
        ("security audit", None),
        ("user interface design", "frontend"),
        ("database schema", "backend")
    ]

    for task, domain in test_queries:
        print(f"\nQuery: '{task}'" + (f" (domain: {domain})" if domain else ""))

        # Use the query function but with explicit telemetry directory
        # We'll inline the logic here for demo purposes
        from scripts.query_best_agent import extract_keywords, calculate_relevance_score, AgentRecommendation
        from collections import defaultdict

        task_keywords = extract_keywords(task)

        agent_scores = defaultdict(lambda: {
            "relevance_sum": 0.0,
            "invocations": [],
            "successes": 0,
            "durations": []
        })

        for inv in invocations:
            agent_name = inv.get("agent_name")
            if not agent_name:
                continue

            relevance = calculate_relevance_score(task_keywords, inv, domain)

            if relevance > 0:
                agent_scores[agent_name]["relevance_sum"] += relevance
                agent_scores[agent_name]["invocations"].append(inv)

                if inv.get("outcome", {}).get("status") == "success":
                    agent_scores[agent_name]["successes"] += 1

                duration = inv.get("duration_seconds")
                if duration:
                    agent_scores[agent_name]["durations"].append(duration)

        if not agent_scores:
            print("  No suitable agent found")
            continue

        recommendations = []
        for agent_name, data in agent_scores.items():
            total_tasks = len(data["invocations"])
            if total_tasks == 0:
                continue

            success_rate = data["successes"] / total_tasks
            avg_duration = (
                sum(data["durations"]) / len(data["durations"])
                if data["durations"] else 0.0
            )
            avg_duration_minutes = avg_duration / 60

            avg_relevance = data["relevance_sum"] / total_tasks
            task_count_factor = min(total_tasks / 10.0, 1.0)
            confidence = (avg_relevance * 0.6 + task_count_factor * 0.4) * success_rate
            confidence = min(confidence / 3.0, 1.0)

            trend_data = analyzer.get_agent_performance_trends(agent_name)
            recent_performance = trend_data.get("trend", "stable")

            recommendations.append(AgentRecommendation(
                agent_name=agent_name,
                confidence=confidence,
                success_rate=success_rate,
                avg_duration_minutes=avg_duration_minutes,
                total_tasks=total_tasks,
                recent_performance=recent_performance
            ))

        recommendations = [r for r in recommendations if r.confidence >= 0.3]
        recommendations.sort(key=lambda r: r.confidence, reverse=True)

        if recommendations:
            rec = recommendations[0]
            print(f"  Agent: {rec.agent_name}")
            print(f"  Confidence: {rec.confidence:.0%}")
            print(f"  Success Rate: {rec.success_rate:.0%}")
            print(f"  Avg Duration: {rec.avg_duration_minutes:.1f} min")
            print(f"  Experience: {rec.total_tasks} tasks")
            print(f"  Trend: {rec.recent_performance}")
        else:
            print("  No suitable agent found")


def demo_coordination_analysis(analyzer: TelemetryAnalyzer):
    """Demonstrate coordination overhead analysis."""
    
    print("\n" + "="*70)
    print("DEMO: COORDINATION ANALYSIS")
    print("="*70)
    
    # Analyze workflows
    workflow_stats = analyzer.analyze_workflows()
    
    print(f"\nWorkflow Performance:")
    print(f"  Total Workflows: {workflow_stats['total_workflows']}")
    print(f"  Success Rate: {workflow_stats['success_rate']:.0%}")
    print(f"  Avg Duration: {workflow_stats['avg_duration_minutes']:.1f} minutes")
    print(f"  Avg Agents: {workflow_stats['avg_agents_per_workflow']:.1f} per workflow")
    
    if workflow_stats['most_common_patterns']:
        print(f"\n  Most Common Agent Patterns:")
        for i, pattern in enumerate(workflow_stats['most_common_patterns'][:3], 1):
            print(f"    {i}. {pattern['pattern']} ({pattern['count']} times)")
    
    # Calculate coordination overhead
    overhead = analyzer.calculate_coordination_overhead()
    
    print(f"\nCoordination Overhead:")
    print(f"  Overhead: {overhead['coordination_overhead_pct']:.1f}%")
    print(f"  Avg Coordination Time: {overhead['avg_coordination_minutes']:.1f} min/workflow")
    print(f"  Recommendation: {overhead['recommendation']}")


def main():
    """Run complete demonstration."""
    
    print("\n" + "="*70)
    print("MULTI-AGENT WORKFLOW COORDINATION DEMO")
    print("Phase 2: Workflow Tracking & Agent Selection")
    print("="*70)
    
    # Use temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        print(f"\nUsing temporary telemetry directory: {tmpdir_path}")
        
        # Initialize logger
        logger = TelemetryLogger(telemetry_dir=tmpdir_path)
        
        # Create sample data
        create_sample_telemetry_data(logger)
        
        # Demo workflow tracking
        demo_workflow_tracking(logger)
        
        # Demo agent selection
        demo_agent_selection(logger)
        
        # Demo coordination analysis
        analyzer = TelemetryAnalyzer(telemetry_dir=tmpdir_path)
        demo_coordination_analysis(analyzer)
        
        # Summary
        print("\n" + "="*70)
        print("DEMO COMPLETE")
        print("="*70)
        print(f"\nKey Features Demonstrated:")
        print(f"  ✓ Workflow start/handoff/complete tracking")
        print(f"  ✓ Historical agent performance queries")
        print(f"  ✓ Agent recommendation with confidence scores")
        print(f"  ✓ Coordination overhead calculation")
        print(f"  ✓ Performance trend analysis")
        
        print(f"\nTelemetry files created:")
        print(f"  - agent_invocations.jsonl ({len(analyzer.load_invocations())} entries)")
        print(f"  - workflow_events.jsonl ({len(analyzer.load_workflow_events())} entries)")
        print(f"  - success_metrics.jsonl ({len(analyzer.load_metrics())} entries)")
        
        return 0


if __name__ == "__main__":
    sys.exit(main())
