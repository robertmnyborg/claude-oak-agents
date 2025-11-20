#!/usr/bin/env python3
"""
Unit tests for Telemetry Logger CRL Extensions (Phase 1)
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.logger import TelemetryLogger


class TestTelemetryLoggerCRL(unittest.TestCase):
    """Test suite for CRL extensions to TelemetryLogger"""
    
    def setUp(self):
        """Create temporary directory for telemetry files"""
        self.test_dir = tempfile.mkdtemp()
        self.logger = TelemetryLogger(telemetry_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_log_invocation_with_crl_fields(self):
        """Test logging invocation with CRL fields"""
        invocation_id = self.logger.log_invocation(
            agent_name="backend-architect",
            agent_type="development",
            task_description="Create REST API endpoints",
            # CRL fields
            agent_variant="api-optimized",
            task_type="api-design",
            q_value=0.85,
            exploration=False,
            learning_enabled=True
        )
        
        # Read logged data
        with open(self.logger.invocations_file, 'r') as f:
            data = json.loads(f.readline())
        
        # Verify CRL fields
        self.assertEqual(data["agent_variant"], "api-optimized")
        self.assertEqual(data["task_type"], "api-design")
        self.assertEqual(data["q_value"], 0.85)
        self.assertEqual(data["exploration"], False)
        self.assertEqual(data["learning_enabled"], True)
        self.assertIsNone(data["reward"])  # Calculated after completion
    
    def test_log_invocation_without_crl_fields(self):
        """Test backward compatibility - logging without CRL fields"""
        invocation_id = self.logger.log_invocation(
            agent_name="backend-architect",
            agent_type="development",
            task_description="Create REST API endpoints"
            # No CRL fields provided
        )
        
        # Read logged data
        with open(self.logger.invocations_file, 'r') as f:
            data = json.loads(f.readline())
        
        # Verify CRL fields are None/False (backward compatible)
        self.assertIsNone(data["agent_variant"])
        self.assertIsNone(data["task_type"])
        self.assertIsNone(data["q_value"])
        self.assertIsNone(data["exploration"])
        self.assertEqual(data["learning_enabled"], False)
        self.assertIsNone(data["reward"])
    
    def test_update_invocation_with_reward(self):
        """Test updating invocation with calculated reward"""
        invocation_id = self.logger.log_invocation(
            agent_name="backend-architect",
            agent_type="development",
            task_description="Create API",
            agent_variant="api-optimized",
            task_type="api-design",
            learning_enabled=True
        )
        
        # Update with reward
        self.logger.update_invocation(
            invocation_id=invocation_id,
            duration_seconds=120.5,
            outcome_status="success",
            reward=2.3  # Calculated reward
        )
        
        # Read updated data
        with open(self.logger.invocations_file, 'r') as f:
            data = json.loads(f.readline())
        
        # Verify reward updated
        self.assertEqual(data["reward"], 2.3)
        self.assertEqual(data["duration_seconds"], 120.5)
    
    def test_crl_fields_in_exploration_mode(self):
        """Test logging with exploration flag set"""
        invocation_id = self.logger.log_invocation(
            agent_name="frontend-developer",
            agent_type="development",
            task_description="Build UI component",
            agent_variant="vue-specialist",
            task_type="ui-implementation",
            q_value=0.0,  # No Q-value for new variant
            exploration=True,  # Random selection
            learning_enabled=True
        )
        
        # Read logged data
        with open(self.logger.invocations_file, 'r') as f:
            data = json.loads(f.readline())
        
        # Verify exploration mode
        self.assertEqual(data["exploration"], True)
        self.assertEqual(data["q_value"], 0.0)
    
    def test_multiple_invocations_with_mixed_crl_state(self):
        """Test mixed CRL enabled/disabled invocations"""
        # CRL enabled invocation
        inv1 = self.logger.log_invocation(
            agent_name="backend-architect",
            agent_type="development",
            task_description="Task 1",
            agent_variant="api-optimized",
            task_type="api-design",
            learning_enabled=True
        )
        
        # CRL disabled invocation (backward compatible)
        inv2 = self.logger.log_invocation(
            agent_name="frontend-developer",
            agent_type="development",
            task_description="Task 2"
            # No CRL fields
        )
        
        # Read all invocations
        invocations = []
        with open(self.logger.invocations_file, 'r') as f:
            for line in f:
                invocations.append(json.loads(line))
        
        # Verify both logged correctly
        self.assertEqual(len(invocations), 2)
        self.assertTrue(invocations[0]["learning_enabled"])
        self.assertFalse(invocations[1]["learning_enabled"])
    
    def test_crl_fields_schema_complete(self):
        """Test that all CRL Phase 1 fields are present in schema"""
        invocation_id = self.logger.log_invocation(
            agent_name="test-agent",
            agent_type="test",
            task_description="Test",
            agent_variant="test-variant",
            task_type="test-task",
            q_value=0.75,
            exploration=False,
            learning_enabled=True
        )
        
        # Read logged data
        with open(self.logger.invocations_file, 'r') as f:
            data = json.loads(f.readline())
        
        # Verify all CRL Phase 1 fields exist
        crl_fields = [
            "agent_variant",
            "task_type",
            "q_value",
            "exploration",
            "reward",
            "learning_enabled"
        ]
        
        for field in crl_fields:
            self.assertIn(field, data, f"Missing CRL field: {field}")


if __name__ == "__main__":
    unittest.main()
