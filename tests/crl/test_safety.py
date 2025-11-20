#!/usr/bin/env python3
"""
Tests for CRL Safety Mechanisms (Phase 3)

Tests safety monitor, rollback manager, and variant proposer.
"""

import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime

from core.safety_monitor import SafetyMonitor
from core.rollback_manager import RollbackManager
from core.variant_proposer import VariantProposer
from core.agent_basis import AgentBasisManager, AgentVariant, PerformanceMetrics, PromptModification
from core.q_learning import QLearningEngine
from telemetry.logger import TelemetryLogger


class TestSafetyMonitor(unittest.TestCase):
    """Test safety monitor decision logic."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.safety_monitor = SafetyMonitor()
    
    def test_high_confidence_auto_apply(self):
        """Test auto-apply decision for high confidence variant."""
        decision, reasoning = self.safety_monitor.should_auto_apply_variant(
            agent_name="test-agent",
            task_type="test-task",
            variant_id="test-variant",
            q_value=0.95,  # High Q-value
            n_visits=15    # Sufficient visits
        )
        
        self.assertEqual(decision, "auto_apply")
        self.assertIn("High confidence", reasoning)
        self.assertIn("0.95", reasoning)
    
    def test_medium_confidence_human_approval(self):
        """Test human approval decision for medium confidence variant."""
        decision, reasoning = self.safety_monitor.should_auto_apply_variant(
            agent_name="test-agent",
            task_type="test-task",
            variant_id="test-variant",
            q_value=0.75,  # Medium Q-value
            n_visits=8     # Moderate visits
        )
        
        self.assertEqual(decision, "human_approval")
        self.assertIn("Medium confidence", reasoning)
    
    def test_low_confidence_no_action(self):
        """Test no action decision for low confidence variant."""
        decision, reasoning = self.safety_monitor.should_auto_apply_variant(
            agent_name="test-agent",
            task_type="test-task",
            variant_id="test-variant",
            q_value=0.65,  # Low Q-value
            n_visits=6     # Sufficient visits, but low Q-value
        )

        self.assertEqual(decision, "no_action")
        self.assertIn("Low confidence", reasoning)
    
    def test_insufficient_data_no_action(self):
        """Test no action when insufficient data."""
        decision, reasoning = self.safety_monitor.should_auto_apply_variant(
            agent_name="test-agent",
            task_type="test-task",
            variant_id="test-variant",
            q_value=0.85,  # Good Q-value
            n_visits=2     # But insufficient visits
        )
        
        self.assertEqual(decision, "no_action")
        self.assertIn("Insufficient data", reasoning)
    
    def test_degradation_detection_success_rate(self):
        """Test degradation detection based on success rate drop."""
        # This test requires mocking telemetry data
        # For now, just test that the method doesn't crash
        degraded, metrics = self.safety_monitor.check_performance_degradation(
            agent_name="nonexistent-agent",
            task_type="test-task",
            variant_id="test-variant"
        )
        
        self.assertFalse(degraded)
        self.assertIn("error", metrics)


class TestRollbackManager(unittest.TestCase):
    """Test rollback manager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.rollback_file = Path(self.temp_dir) / "rollback_events.jsonl"
        self.rollback_manager = RollbackManager(rollback_events_file=self.rollback_file)
    
    def test_rollback_event_logging(self):
        """Test rollback event is properly logged."""
        rollback_info = self.rollback_manager._execute_rollback(
            agent_name="test-agent",
            task_type="test-task",
            from_variant="failing-variant",
            to_variant="stable-variant",
            reason="Test rollback",
            degradation_metrics={"test": "data"}
        )
        
        self.assertIsNotNone(rollback_info)
        self.assertIn("rollback_id", rollback_info)
        self.assertEqual(rollback_info["from_variant"], "failing-variant")
        self.assertEqual(rollback_info["to_variant"], "stable-variant")
        
        # Verify logged to file
        self.assertTrue(self.rollback_file.exists())
        
        with open(self.rollback_file, 'r') as f:
            logged = json.loads(f.read())
            self.assertEqual(logged["rollback_id"], rollback_info["rollback_id"])
    
    def test_rollback_history_retrieval(self):
        """Test retrieving rollback history."""
        # Create test rollback events
        for i in range(3):
            self.rollback_manager._execute_rollback(
                agent_name=f"agent-{i}",
                task_type="test-task",
                from_variant="old",
                to_variant="new",
                reason=f"Test {i}",
                degradation_metrics={}
            )
        
        # Retrieve history
        history = self.rollback_manager.get_rollback_history(limit=2)
        
        self.assertEqual(len(history), 2)
        # Should be in reverse chronological order (newest first)
        self.assertEqual(history[0]["agent_name"], "agent-2")
    
    def test_rollback_history_filtering(self):
        """Test filtering rollback history by agent."""
        # Create rollback events for different agents
        self.rollback_manager._execute_rollback(
            agent_name="agent-1",
            task_type="task-1",
            from_variant="old",
            to_variant="new",
            reason="Test",
            degradation_metrics={}
        )
        self.rollback_manager._execute_rollback(
            agent_name="agent-2",
            task_type="task-2",
            from_variant="old",
            to_variant="new",
            reason="Test",
            degradation_metrics={}
        )
        
        # Filter by agent-1
        history = self.rollback_manager.get_rollback_history(agent_name="agent-1")
        
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["agent_name"], "agent-1")


class TestVariantProposer(unittest.TestCase):
    """Test variant proposer functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.proposals_file = Path(self.temp_dir) / "variant_proposals.jsonl"
        self.proposer = VariantProposer(proposals_file=self.proposals_file)
    
    def test_proposal_creation(self):
        """Test creating a variant proposal."""
        proposal = self.proposer._create_proposal(
            agent_name="test-agent",
            task_type="test-task",
            proposal_type="create_specialized_variant",
            reason="Test proposal",
            supporting_data={"n_invocations": 100, "avg_q_value": 0.55}
        )
        
        self.assertIsNotNone(proposal)
        self.assertIn("proposal_id", proposal)
        self.assertEqual(proposal["agent_name"], "test-agent")
        self.assertEqual(proposal["proposal_type"], "create_specialized_variant")
        self.assertEqual(proposal["status"], "pending")
        
        # Verify logged to file
        self.assertTrue(self.proposals_file.exists())
    
    def test_confidence_calculation(self):
        """Test confidence score calculation."""
        # High invocations should give higher confidence
        confidence_high = self.proposer._calculate_confidence(
            proposal_type="create_specialized_variant",
            supporting_data={"n_invocations": 150}
        )
        
        confidence_low = self.proposer._calculate_confidence(
            proposal_type="create_specialized_variant",
            supporting_data={"n_invocations": 30}
        )
        
        self.assertGreater(confidence_high, confidence_low)
        self.assertLessEqual(confidence_high, 1.0)
        self.assertGreaterEqual(confidence_low, 0.0)
    
    def test_proposal_retrieval(self):
        """Test retrieving proposals."""
        # Create test proposals
        for i in range(3):
            self.proposer._create_proposal(
                agent_name=f"agent-{i}",
                task_type="test-task",
                proposal_type="create_specialized_variant",
                reason=f"Test {i}",
                supporting_data={"n_invocations": 100}
            )
        
        # Retrieve all proposals
        proposals = self.proposer.get_proposals()
        
        self.assertEqual(len(proposals), 3)
    
    def test_proposal_filtering_by_status(self):
        """Test filtering proposals by status."""
        # Create proposals with different statuses
        proposal1 = self.proposer._create_proposal(
            agent_name="agent-1",
            task_type="test-task",
            proposal_type="create_specialized_variant",
            reason="Test",
            supporting_data={"n_invocations": 100}
        )
        
        # Manually update status
        proposals = []
        with open(self.proposals_file, 'r') as f:
            for line in f:
                if line.strip():
                    p = json.loads(line)
                    proposals.append(p)
        
        # Update first proposal status
        proposals[0]["status"] = "approved"
        
        with open(self.proposals_file, 'w') as f:
            for p in proposals:
                f.write(json.dumps(p) + '\n')
        
        # Test filtering
        pending = self.proposer.get_proposals(status="pending")
        self.assertEqual(len(pending), 0)
        
        approved = self.proposer.get_proposals(status="approved")
        self.assertEqual(len(approved), 1)
    
    def test_recommendation_generation(self):
        """Test generating task-specific recommendations."""
        # Security task recommendations
        security_recs = self.proposer._generate_recommendations("security-audit")
        
        self.assertGreater(len(security_recs), 0)
        self.assertTrue(
            any("security" in str(rec).lower() for rec in security_recs)
        )
        
        # API design recommendations
        api_recs = self.proposer._generate_recommendations("api-design")
        
        self.assertGreater(len(api_recs), 0)
        self.assertTrue(
            any("api" in str(rec).lower() for rec in api_recs)
        )


class TestSafetyIntegration(unittest.TestCase):
    """Integration tests for safety mechanisms."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def test_end_to_end_safety_workflow(self):
        """Test complete safety workflow: monitor → decision → rollback."""
        # This is a simplified integration test
        # Real workflow would involve actual Q-learning data
        
        monitor = SafetyMonitor()
        rollback_mgr = RollbackManager()
        
        # Test decision making
        decision, reasoning = monitor.should_auto_apply_variant(
            agent_name="test-agent",
            task_type="test-task",
            variant_id="test-variant",
            q_value=0.92,
            n_visits=12
        )
        
        self.assertEqual(decision, "auto_apply")
        
        # Test rollback manager can create events
        rollback_info = rollback_mgr._execute_rollback(
            agent_name="test-agent",
            task_type="test-task",
            from_variant="bad-variant",
            to_variant="good-variant",
            reason="Integration test",
            degradation_metrics={}
        )
        
        self.assertIsNotNone(rollback_info)
        
        # Verify rollback history retrieval
        history = rollback_mgr.get_rollback_history(limit=1)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["rollback_id"], rollback_info["rollback_id"])


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSafetyMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestRollbackManager))
    suite.addTests(loader.loadTestsFromTestCase(TestVariantProposer))
    suite.addTests(loader.loadTestsFromTestCase(TestSafetyIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
