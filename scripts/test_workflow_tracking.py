#!/usr/bin/env python3
"""
Test Script for Phase 2A Workflow Tracking

This script validates:
1. Multi-agent workflow logging (3 agents in sequence)
2. workflow_id population
3. parent_invocation_id linking
4. Query script functionality
5. Backward compatibility (single-agent)
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from telemetry.logger import TelemetryLogger
from telemetry.workflow import generate_workflow_id


class WorkflowTrackingTest:
    """Test harness for workflow tracking functionality."""
    
    def __init__(self):
        self.telemetry_dir = PROJECT_ROOT / "telemetry"
        self.logger = TelemetryLogger(telemetry_dir=self.telemetry_dir)
        self.test_results = []
        
    def log_test(self, test_name, passed, message=""):
        """Log test result."""
        status = "PASS" if passed else "FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "message": message
        })
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {message}")
        
    def test_workflow_id_generation(self):
        """Test 1: Workflow ID generation."""
        workflow_id = generate_workflow_id()
        
        # Validate format: wf-YYYYMMDD-xxxxxxxx
        parts = workflow_id.split("-")
        passed = (
            len(parts) == 3 and
            parts[0] == "wf" and
            len(parts[1]) == 8 and
            parts[1].isdigit() and
            len(parts[2]) == 8
        )
        
        self.log_test(
            "Workflow ID Generation",
            passed,
            f"Generated: {workflow_id}"
        )
        return workflow_id if passed else None
        
    def test_multi_agent_workflow(self, workflow_id):
        """Test 2: Multi-agent workflow with 3 agents."""
        agents = [
            ("design-simplicity-advisor", "meta"),
            ("backend-architect", "development"),
            ("unit-test-expert", "quality")
        ]
        
        invocation_ids = []
        parent_id = None
        
        for agent_name, agent_type in agents:
            # Simulate agent invocation
            inv_id = self.logger.log_invocation(
                agent_name=agent_name,
                agent_type=agent_type,
                task_description=f"Test workflow task for {agent_name}",
                parent_invocation_id=parent_id,
                workflow_id=workflow_id,
                state_features={
                    "task": {
                        "type": "testing",
                        "scope": "small",
                        "risk_level": "low"
                    }
                }
            )
            
            invocation_ids.append(inv_id)
            
            # Simulate completion
            time.sleep(0.1)
            self.logger.update_invocation(
                invocation_id=inv_id,
                duration_seconds=0.5,
                outcome_status="success"
            )
            
            # Next agent uses this as parent
            parent_id = inv_id
            
        # Verify all invocations logged
        self.log_test(
            "Multi-Agent Workflow Logging",
            len(invocation_ids) == 3,
            f"Logged {len(invocation_ids)} agents"
        )
        
        return invocation_ids
        
    def test_workflow_id_population(self, workflow_id):
        """Test 3: Verify workflow_id is populated correctly."""
        invocations_file = self.telemetry_dir / "agent_invocations.jsonl"
        
        workflow_invocations = []
        with open(invocations_file, "r") as f:
            for line in f:
                if line.strip():
                    inv = json.loads(line)
                    if inv.get("workflow_id") == workflow_id:
                        workflow_invocations.append(inv)
                        
        passed = len(workflow_invocations) == 3
        self.log_test(
            "Workflow ID Population",
            passed,
            f"Found {len(workflow_invocations)}/3 invocations with workflow_id"
        )
        
        return workflow_invocations
        
    def test_parent_invocation_linking(self, workflow_invocations):
        """Test 4: Verify parent_invocation_id links agents."""
        # First agent should have no parent
        first_agent = workflow_invocations[0]
        has_no_parent = first_agent.get("parent_invocation_id") is None
        
        # Second and third should have parents
        second_agent = workflow_invocations[1]
        third_agent = workflow_invocations[2]
        
        second_has_parent = second_agent.get("parent_invocation_id") == first_agent["invocation_id"]
        third_has_parent = third_agent.get("parent_invocation_id") == second_agent["invocation_id"]
        
        passed = has_no_parent and second_has_parent and third_has_parent
        
        self.log_test(
            "Parent Invocation Linking",
            passed,
            "Agent chain correctly linked"
        )
        
    def test_query_script(self, workflow_id):
        """Test 5: Verify query script functionality."""
        script_path = PROJECT_ROOT / "scripts" / "query_workflow.sh"
        
        try:
            result = subprocess.run(
                [str(script_path), workflow_id],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            output = result.stdout
            passed = (
                result.returncode == 0 and
                "design-simplicity-advisor" in output and
                "backend-architect" in output and
                "unit-test-expert" in output
            )
            
            self.log_test(
                "Query Script Functionality",
                passed,
                "Script successfully queried workflow"
            )
            
        except Exception as e:
            self.log_test(
                "Query Script Functionality",
                False,
                f"Error: {str(e)}"
            )
            
    def test_backward_compatibility(self):
        """Test 6: Single-agent invocation without workflow_id."""
        inv_id = self.logger.log_invocation(
            agent_name="general-purpose",
            agent_type="utility",
            task_description="Test backward compatibility",
            workflow_id=None  # Explicitly null
        )
        
        # Update invocation
        self.logger.update_invocation(
            invocation_id=inv_id,
            duration_seconds=0.2,
            outcome_status="success"
        )
        
        # Verify it was logged
        invocations_file = self.telemetry_dir / "agent_invocations.jsonl"
        found = False
        
        with open(invocations_file, "r") as f:
            for line in f:
                if line.strip():
                    inv = json.loads(line)
                    if inv["invocation_id"] == inv_id:
                        found = True
                        has_null_workflow = inv.get("workflow_id") is None
                        break
                        
        passed = found and has_null_workflow
        
        self.log_test(
            "Backward Compatibility",
            passed,
            "Single-agent invocation works with workflow_id=null"
        )
        
    def run_all_tests(self):
        """Run complete test suite."""
        print("=" * 60)
        print("PHASE 2A WORKFLOW TRACKING TEST SUITE")
        print("=" * 60)
        print()
        
        # Test 1: Workflow ID generation
        workflow_id = self.test_workflow_id_generation()
        if not workflow_id:
            print("\nAborting tests - workflow ID generation failed")
            return False
            
        print()
        
        # Test 2: Multi-agent workflow
        invocation_ids = self.test_multi_agent_workflow(workflow_id)
        print()
        
        # Test 3: Workflow ID population
        workflow_invocations = self.test_workflow_id_population(workflow_id)
        print()
        
        # Test 4: Parent invocation linking
        if workflow_invocations:
            self.test_parent_invocation_linking(workflow_invocations)
            print()
            
        # Test 5: Query script
        self.test_query_script(workflow_id)
        print()
        
        # Test 6: Backward compatibility
        self.test_backward_compatibility()
        print()
        
        # Summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print()
        
        if failed > 0:
            print("FAILED TESTS:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['message']}")
                    
        return failed == 0


def main():
    """Main entry point."""
    test_suite = WorkflowTrackingTest()
    success = test_suite.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
