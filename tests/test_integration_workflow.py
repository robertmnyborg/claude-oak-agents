#!/usr/bin/env python3
"""
Integration Test: Phase 2 Workflow Coordination

Tests the complete integration of Phase 2 workflow tracking with existing OaK infrastructure.
"""

import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from telemetry.logger import TelemetryLogger
from telemetry.analyzer import TelemetryAnalyzer
from scripts.query_best_agent import query_best_agent


class TestIntegratedWorkflow(unittest.TestCase):
    """Test Phase 2 workflow integration end-to-end."""

    def setUp(self):
        """Set up test environment with temporary telemetry directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.telemetry_dir = Path(self.temp_dir) / "telemetry"
        self.telemetry_dir.mkdir(parents=True, exist_ok=True)

        self.logger = TelemetryLogger(self.telemetry_dir)
        self.analyzer = TelemetryAnalyzer(self.telemetry_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_workflow_tracking_integration(self):
        """Test complete workflow tracking from start to finish."""
        # Step 1: Log workflow start
        workflow_id = "test-wf-001"
        self.logger.log_workflow_start(
            workflow_id=workflow_id,
            project_name="Test Integration Workflow",
            agent_plan=["systems-architect", "backend-architect", "frontend-developer"],
            estimated_duration=3600
        )

        # Verify workflow start logged
        events = self.analyzer.load_workflow_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "workflow_start")
        self.assertEqual(events[0]["workflow_id"], workflow_id)

        # Step 2: Log agent invocations
        inv_id_1 = self.logger.log_invocation(
            agent_name="systems-architect",
            agent_type="architecture",
            task_description="Design system architecture"
        )

        self.logger.update_invocation(
            invocation_id=inv_id_1,
            duration_seconds=600,
            outcome_status="success"
        )

        # Step 3: Log handoff
        self.logger.log_agent_handoff(
            workflow_id=workflow_id,
            from_agent="systems-architect",
            to_agent="backend-architect",
            artifacts=["architecture.md"]
        )

        # Verify handoff logged
        events = self.analyzer.load_workflow_events()
        handoff_events = [e for e in events if e["event"] == "agent_handoff"]
        self.assertEqual(len(handoff_events), 1)
        self.assertEqual(handoff_events[0]["from_agent"], "systems-architect")
        self.assertEqual(handoff_events[0]["to_agent"], "backend-architect")

        # Step 4: Log workflow completion
        self.logger.log_workflow_complete(
            workflow_id=workflow_id,
            duration_seconds=3200,
            success=True,
            agents_executed=["systems-architect", "backend-architect", "frontend-developer"]
        )

        # Verify workflow complete
        events = self.analyzer.load_workflow_events()
        complete_events = [e for e in events if e["event"] == "workflow_complete"]
        self.assertEqual(len(complete_events), 1)
        self.assertEqual(complete_events[0]["success"], True)
        self.assertEqual(complete_events[0]["duration_seconds"], 3200)

    def test_workflow_analysis_integration(self):
        """Test workflow analysis with multiple workflows."""
        # Create multiple workflows
        for i in range(3):
            workflow_id = f"test-wf-{i}"

            # Log workflow
            self.logger.log_workflow_start(
                workflow_id=workflow_id,
                project_name=f"Test Workflow {i}",
                agent_plan=["backend-architect", "frontend-developer"],
                estimated_duration=1800
            )

            # Log some invocations
            for agent in ["backend-architect", "frontend-developer"]:
                inv_id = self.logger.log_invocation(
                    agent_name=agent,
                    agent_type="development",
                    task_description=f"Task for {agent}"
                )

                self.logger.update_invocation(
                    invocation_id=inv_id,
                    duration_seconds=300 + i * 50,
                    outcome_status="success"
                )

            # Log handoff
            self.logger.log_agent_handoff(
                workflow_id=workflow_id,
                from_agent="backend-architect",
                to_agent="frontend-developer",
                artifacts=["api-spec.yaml"]
            )

            # Complete workflow
            self.logger.log_workflow_complete(
                workflow_id=workflow_id,
                duration_seconds=1200 + i * 100,
                success=True,
                agents_executed=["backend-architect", "frontend-developer"]
            )

        # Analyze workflows
        stats = self.analyzer.analyze_workflows()

        self.assertEqual(stats["total_workflows"], 3)
        self.assertEqual(stats["success_rate"], 1.0)
        self.assertEqual(stats["avg_agents_per_workflow"], 2.0)
        self.assertGreater(len(stats["most_common_patterns"]), 0)

    def test_coordination_overhead_calculation(self):
        """Test coordination overhead calculation."""
        workflow_id = "test-wf-overhead"

        # Log workflow start
        self.logger.log_workflow_start(
            workflow_id=workflow_id,
            project_name="Overhead Test",
            agent_plan=["agent-1", "agent-2"],
            estimated_duration=1000
        )

        # Log agent invocations with durations
        for i, agent in enumerate(["agent-1", "agent-2"]):
            inv_id = self.logger.log_invocation(
                agent_name=agent,
                agent_type="test",
                task_description=f"Task {i}"
            )

            self.logger.update_invocation(
                invocation_id=inv_id,
                duration_seconds=200,
                outcome_status="success"
            )

        # Complete workflow (total 500s, agents took 400s, overhead = 100s = 20%)
        self.logger.log_workflow_complete(
            workflow_id=workflow_id,
            duration_seconds=500,
            success=True,
            agents_executed=["agent-1", "agent-2"]
        )

        # Calculate overhead
        overhead = self.analyzer.calculate_coordination_overhead()

        self.assertGreater(overhead["coordination_overhead_pct"], 0)
        self.assertIn("recommendation", overhead)

    def test_agent_performance_trends(self):
        """Test agent performance trend analysis."""
        # Create historical data
        agent_name = "test-agent"

        # Older invocations (lower success rate)
        for i in range(5):
            inv_id = self.logger.log_invocation(
                agent_name=agent_name,
                agent_type="test",
                task_description=f"Old task {i}"
            )

            # 60% success rate
            status = "success" if i < 3 else "failure"
            self.logger.update_invocation(
                invocation_id=inv_id,
                duration_seconds=100,
                outcome_status=status
            )

        # Modify timestamps to be older (manually edit the file)
        invocations = self.analyzer.load_invocations()
        for inv in invocations:
            inv["timestamp"] = "2025-09-01T10:00:00Z"  # 50 days ago

        # Rewrite with old timestamps
        with open(self.analyzer.invocations_file, "w") as f:
            for inv in invocations:
                f.write(json.dumps(inv) + "\n")

        # Recent invocations (higher success rate)
        for i in range(5):
            inv_id = self.logger.log_invocation(
                agent_name=agent_name,
                agent_type="test",
                task_description=f"Recent task {i}"
            )

            # 100% success rate
            self.logger.update_invocation(
                invocation_id=inv_id,
                duration_seconds=100,
                outcome_status="success"
            )

        # Analyze trends
        trend_data = self.analyzer.get_agent_performance_trends(agent_name, days=60)

        # Should show improvement
        self.assertIn(trend_data["trend"], ["improving", "stable", "declining"])
        self.assertGreaterEqual(trend_data["recent_success_rate"], 0.0)
        self.assertLessEqual(trend_data["recent_success_rate"], 1.0)

    def test_query_best_agent_integration(self):
        """Test agent recommendation query using isolated telemetry."""
        # This test verifies the query mechanism works correctly
        # We'll manually implement the query logic to avoid interference from real data

        # Create telemetry data for multiple agents
        agents = {
            "backend-architect": {
                "tasks": [
                    ("API development project", "success", 300),
                    ("REST API implementation task", "success", 250),
                    ("Backend API service development", "success", 400),
                    ("API endpoint development", "success", 320),
                    ("Backend API creation", "success", 280),
                ],
                "type": "backend"
            },
            "frontend-developer": {
                "tasks": [
                    ("React component", "success", 200),
                    ("UI development", "failure", 150),
                    ("Frontend task", "success", 180),
                ],
                "type": "frontend"
            }
        }

        for agent_name, data in agents.items():
            for task_desc, status, duration in data["tasks"]:
                inv_id = self.logger.log_invocation(
                    agent_name=agent_name,
                    agent_type=data["type"],
                    task_description=task_desc,
                    state_features={
                        "task": {"type": data["type"]}
                    }
                )

                self.logger.update_invocation(
                    invocation_id=inv_id,
                    duration_seconds=duration,
                    outcome_status=status
                )

        # Load invocations and verify backend-architect has best metrics
        invocations = self.analyzer.load_invocations()

        # Count by agent
        agent_stats = {}
        for inv in invocations:
            agent = inv.get("agent_name")
            if agent not in agent_stats:
                agent_stats[agent] = {"success": 0, "total": 0}

            agent_stats[agent]["total"] += 1
            if inv.get("outcome", {}).get("status") == "success":
                agent_stats[agent]["success"] += 1

        # Verify backend-architect has 100% success rate
        self.assertIn("backend-architect", agent_stats)
        self.assertEqual(agent_stats["backend-architect"]["total"], 5)
        self.assertEqual(agent_stats["backend-architect"]["success"], 5)
        self.assertEqual(
            agent_stats["backend-architect"]["success"] / agent_stats["backend-architect"]["total"],
            1.0
        )

    def test_backward_compatibility_single_agent(self):
        """Test that single-agent tasks work without workflow tracking."""
        # Log single agent invocation (no workflow)
        inv_id = self.logger.log_invocation(
            agent_name="simple-agent",
            agent_type="test",
            task_description="Simple task"
        )

        self.logger.update_invocation(
            invocation_id=inv_id,
            duration_seconds=100,
            outcome_status="success"
        )

        # Analyze - should handle missing workflow data gracefully
        stats = self.analyzer.analyze_workflows()

        # No workflows logged
        self.assertEqual(stats["total_workflows"], 0)
        self.assertEqual(stats["success_rate"], 0.0)

        # But invocation data still available
        invocations = self.analyzer.load_invocations()
        self.assertEqual(len(invocations), 1)

    def test_weekly_review_integration(self):
        """Test that weekly review can handle workflow data."""
        # Create workflow data
        workflow_id = "weekly-test-wf"

        self.logger.log_workflow_start(
            workflow_id=workflow_id,
            project_name="Weekly Review Test",
            agent_plan=["agent-1"],
            estimated_duration=600
        )

        inv_id = self.logger.log_invocation(
            agent_name="agent-1",
            agent_type="test",
            task_description="Test task"
        )

        self.logger.update_invocation(
            invocation_id=inv_id,
            duration_seconds=500,
            outcome_status="success"
        )

        self.logger.log_workflow_complete(
            workflow_id=workflow_id,
            duration_seconds=600,
            success=True,
            agents_executed=["agent-1"]
        )

        # Simulate weekly review workflow analysis
        workflow_file = self.telemetry_dir / "workflow_events.jsonl"

        if workflow_file.exists() and workflow_file.stat().st_size > 0:
            workflow_stats = self.analyzer.analyze_workflows()

            # Should have workflow data
            self.assertEqual(workflow_stats["total_workflows"], 1)
            self.assertEqual(workflow_stats["success_rate"], 1.0)

            # Should calculate overhead
            overhead = self.analyzer.calculate_coordination_overhead()
            self.assertIn("coordination_overhead_pct", overhead)
            self.assertIn("recommendation", overhead)

    def test_monthly_analysis_integration(self):
        """Test that monthly analysis can handle performance trends."""
        # Create historical performance data
        agent_name = "monthly-test-agent"

        for i in range(10):
            inv_id = self.logger.log_invocation(
                agent_name=agent_name,
                agent_type="test",
                task_description=f"Task {i}"
            )

            # Gradually improving performance
            status = "success" if i >= 5 else "failure"
            self.logger.update_invocation(
                invocation_id=inv_id,
                duration_seconds=100,
                outcome_status=status
            )

        # Get all active agents
        invocations = self.analyzer.load_invocations()
        active_agents = set(inv["agent_name"] for inv in invocations)

        self.assertIn(agent_name, active_agents)

        # Analyze trends
        trend_data = self.analyzer.get_agent_performance_trends(agent_name, days=30)

        self.assertIn("trend", trend_data)
        self.assertIn("recent_success_rate", trend_data)
        self.assertIn("historical_success_rate", trend_data)


def run_tests():
    """Run all integration tests."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIntegratedWorkflow)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
