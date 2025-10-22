#!/usr/bin/env python3
"""
Test Workflow Tracking

End-to-end test of workflow telemetry logging and querying.
"""

import json
import sys
import tempfile
import time
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from telemetry.logger import TelemetryLogger
from telemetry.analyzer import TelemetryAnalyzer


def test_workflow_tracking():
    """Test complete workflow tracking cycle."""
    
    print("\n" + "="*70)
    print("TESTING WORKFLOW TRACKING")
    print("="*70)
    
    # Use temporary directory for test data
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Override telemetry directory
        logger = TelemetryLogger(telemetry_dir=tmpdir_path)
        
        print(f"\nUsing temporary directory: {tmpdir_path}")
        
        # Simulate workflow
        workflow_id = "test-workflow-001"
        
        # 1. Log workflow start
        print("\n[1/6] Logging workflow start...")
        logger.log_workflow_start(
            workflow_id=workflow_id,
            project_name="Test E-Commerce App",
            agent_plan=["systems-architect", "backend-architect", "frontend-developer"],
            estimated_duration=7200  # 2 hours
        )
        
        # 2. Log systems-architect execution
        print("[2/6] Simulating systems-architect execution...")
        inv_id_1 = logger.log_invocation(
            agent_name="systems-architect",
            agent_type="architecture",
            task_description="Design high-level architecture for e-commerce platform",
            state_features={"task": {"type": "architecture_design"}}
        )
        time.sleep(0.1)  # Simulate work
        logger.update_invocation(
            invocation_id=inv_id_1,
            duration_seconds=1800,
            outcome_status="success",
            files_created=["artifacts/systems-architect/architecture.md"]
        )
        logger.log_success_metric(
            invocation_id=inv_id_1,
            success=True,
            quality_rating=5
        )
        
        # 3. Log first agent handoff
        print("[3/6] Logging handoff to backend-architect...")
        logger.log_agent_handoff(
            workflow_id=workflow_id,
            from_agent="systems-architect",
            to_agent="backend-architect",
            artifacts=["artifacts/systems-architect/architecture.md"]
        )
        
        # 4. Log backend-architect execution
        print("[4/6] Simulating backend-architect execution...")
        inv_id_2 = logger.log_invocation(
            agent_name="backend-architect",
            agent_type="development",
            task_description="Implement API endpoints and database schema",
            state_features={"task": {"type": "backend_development"}}
        )
        time.sleep(0.1)
        logger.update_invocation(
            invocation_id=inv_id_2,
            duration_seconds=2400,
            outcome_status="success",
            files_created=[
                "artifacts/backend-architect/api-spec.yaml",
                "artifacts/backend-architect/database-schema.sql"
            ]
        )
        logger.log_success_metric(
            invocation_id=inv_id_2,
            success=True,
            quality_rating=4
        )
        
        # 5. Log second handoff
        print("[5/6] Logging handoff to frontend-developer...")
        logger.log_agent_handoff(
            workflow_id=workflow_id,
            from_agent="backend-architect",
            to_agent="frontend-developer",
            artifacts=[
                "artifacts/backend-architect/api-spec.yaml",
                "artifacts/backend-architect/database-schema.sql"
            ]
        )
        
        # 6. Log frontend-developer execution
        print("[6/6] Simulating frontend-developer execution...")
        inv_id_3 = logger.log_invocation(
            agent_name="frontend-developer",
            agent_type="development",
            task_description="Build React UI components",
            state_features={"task": {"type": "frontend_development"}}
        )
        time.sleep(0.1)
        logger.update_invocation(
            invocation_id=inv_id_3,
            duration_seconds=2300,
            outcome_status="success",
            files_created=[
                "src/components/ProductList.tsx",
                "src/components/ShoppingCart.tsx"
            ]
        )
        logger.log_success_metric(
            invocation_id=inv_id_3,
            success=True,
            quality_rating=5
        )
        
        # 7. Log workflow completion
        print("\nLogging workflow completion...")
        logger.log_workflow_complete(
            workflow_id=workflow_id,
            duration_seconds=6500,
            success=True,
            agents_executed=["systems-architect", "backend-architect", "frontend-developer"]
        )

        # Small delay to ensure file is flushed
        time.sleep(0.1)

        # 8. Analyze workflow
        print("\nAnalyzing workflow data...")
        analyzer = TelemetryAnalyzer(telemetry_dir=tmpdir_path)
        
        # Verify workflow events were logged
        events = analyzer.load_workflow_events()
        print(f"  Total workflow events: {len(events)}")
        # 1 start + 2 handoffs + 1 complete = 4 events
        assert len(events) == 4, f"Expected 4 events, got {len(events)}"
        
        # Verify event types
        event_types = [e["event"] for e in events]
        assert "workflow_start" in event_types
        assert "workflow_complete" in event_types
        assert event_types.count("agent_handoff") == 2
        
        # Analyze workflows
        stats = analyzer.analyze_workflows()
        
        print(f"\nWorkflow Statistics:")
        print(f"  Total Workflows: {stats['total_workflows']}")
        print(f"  Success Rate: {stats['success_rate']:.0%}")
        print(f"  Avg Duration: {stats['avg_duration_minutes']:.1f} minutes")
        print(f"  Avg Agents per Workflow: {stats['avg_agents_per_workflow']:.1f}")
        
        assert stats["total_workflows"] == 1
        assert stats["success_rate"] == 1.0
        assert stats["avg_agents_per_workflow"] == 3
        
        # Analyze coordination overhead
        overhead = analyzer.calculate_coordination_overhead()
        
        print(f"\nCoordination Overhead:")
        print(f"  Overhead: {overhead['coordination_overhead_pct']:.1f}%")
        print(f"  Avg Coordination Time: {overhead['avg_coordination_minutes']:.1f} minutes")
        print(f"  Recommendation: {overhead['recommendation']}")
        
        assert overhead["coordination_overhead_pct"] >= 0
        
        # Test agent performance trends
        print("\nAgent Performance Trends:")
        for agent_name in ["systems-architect", "backend-architect", "frontend-developer"]:
            trend = analyzer.get_agent_performance_trends(agent_name, days=30)
            print(f"  {agent_name}: {trend['trend']}")
        
        print("\n" + "="*70)
        print("ALL TESTS PASSED!")
        print("="*70)
        
        # Print file contents for verification
        print(f"\nWorkflow events logged to:")
        print(f"  {tmpdir_path}/workflow_events.jsonl")
        
        print(f"\nSample workflow event:")
        with open(tmpdir_path / "workflow_events.jsonl", "r") as f:
            first_event = json.loads(f.readline())
            print(f"  {json.dumps(first_event, indent=2)}")
        
        return 0


def test_multiple_workflows():
    """Test analysis of multiple workflows."""
    
    print("\n" + "="*70)
    print("TESTING MULTIPLE WORKFLOWS")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        logger = TelemetryLogger(telemetry_dir=tmpdir_path)
        
        # Simulate 3 different workflows
        workflows = [
            {
                "workflow_id": "wf-001",
                "project_name": "API Development",
                "agents": ["backend-architect", "unit-test-expert"],
                "duration": 3600,
                "success": True
            },
            {
                "workflow_id": "wf-002",
                "project_name": "Frontend Feature",
                "agents": ["frontend-developer", "qa-specialist"],
                "duration": 2400,
                "success": True
            },
            {
                "workflow_id": "wf-003",
                "project_name": "Security Audit",
                "agents": ["security-auditor", "backend-architect"],
                "duration": 5400,
                "success": False
            }
        ]
        
        print(f"\nSimulating {len(workflows)} workflows...")
        
        for wf in workflows:
            # Log workflow start
            logger.log_workflow_start(
                workflow_id=wf["workflow_id"],
                project_name=wf["project_name"],
                agent_plan=wf["agents"],
                estimated_duration=wf["duration"]
            )
            
            # Log agent executions
            for i, agent in enumerate(wf["agents"]):
                inv_id = logger.log_invocation(
                    agent_name=agent,
                    agent_type="development",
                    task_description=f"{wf['project_name']} - {agent}",
                    state_features={}
                )
                logger.update_invocation(
                    invocation_id=inv_id,
                    duration_seconds=wf["duration"] // len(wf["agents"]),
                    outcome_status="success" if wf["success"] else "failure"
                )
                logger.log_success_metric(
                    invocation_id=inv_id,
                    success=wf["success"],
                    quality_rating=4 if wf["success"] else 2
                )
                
                # Log handoff if not last agent
                if i < len(wf["agents"]) - 1:
                    logger.log_agent_handoff(
                        workflow_id=wf["workflow_id"],
                        from_agent=agent,
                        to_agent=wf["agents"][i + 1],
                        artifacts=[f"artifacts/{agent}/output.md"]
                    )
            
            # Log workflow completion
            logger.log_workflow_complete(
                workflow_id=wf["workflow_id"],
                duration_seconds=wf["duration"],
                success=wf["success"],
                agents_executed=wf["agents"]
            )
        
        # Analyze multiple workflows
        analyzer = TelemetryAnalyzer(telemetry_dir=tmpdir_path)
        stats = analyzer.analyze_workflows()
        
        print(f"\nMulti-Workflow Analysis:")
        print(f"  Total Workflows: {stats['total_workflows']}")
        print(f"  Success Rate: {stats['success_rate']:.0%}")
        print(f"  Avg Duration: {stats['avg_duration_minutes']:.1f} minutes")
        print(f"  Avg Agents per Workflow: {stats['avg_agents_per_workflow']:.1f}")
        
        assert stats["total_workflows"] == 3
        assert abs(stats["success_rate"] - 0.667) < 0.01  # 2 out of 3 succeeded (rounded)
        assert stats["avg_agents_per_workflow"] == 2
        
        # Check most common patterns
        print(f"\nMost Common Agent Patterns:")
        for i, pattern_data in enumerate(stats["most_common_patterns"], 1):
            print(f"  {i}. {pattern_data['pattern']} (used {pattern_data['count']} times)")
        
        print("\n" + "="*70)
        print("MULTIPLE WORKFLOW TESTS PASSED!")
        print("="*70)
        
        return 0


def main():
    """Run all workflow tracking tests."""
    
    print("\n" + "="*70)
    print("WORKFLOW TRACKING TEST SUITE")
    print("="*70)
    
    try:
        # Test 1: Single workflow tracking
        result1 = test_workflow_tracking()
        
        # Test 2: Multiple workflows
        result2 = test_multiple_workflows()
        
        if result1 == 0 and result2 == 0:
            print("\n" + "="*70)
            print("ALL WORKFLOW TRACKING TESTS PASSED!")
            print("="*70)
            return 0
        else:
            return 1
    
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
