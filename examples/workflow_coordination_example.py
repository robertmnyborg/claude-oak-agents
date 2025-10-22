#!/usr/bin/env python3
"""
Example: Multi-Agent Workflow Coordination

This example demonstrates how to use Phase 2 workflow tracking features
to coordinate a multi-agent development workflow for building a web application.
"""

import sys
import time
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from telemetry.logger import TelemetryLogger
from telemetry.analyzer import TelemetryAnalyzer


def build_web_application():
    """Example workflow: Building a full-stack web application."""
    
    print("\n" + "="*70)
    print("EXAMPLE: Multi-Agent Web Application Development")
    print("="*70)
    
    # Initialize telemetry logger
    logger = TelemetryLogger()
    
    # Generate unique workflow ID
    workflow_id = f"webapp-build-{int(time.time())}"
    
    print(f"\nWorkflow ID: {workflow_id}")
    print("Project: Task Management Web App")
    
    # Step 1: Define the agent plan
    agent_plan = [
        "systems-architect",
        "backend-architect",
        "frontend-developer",
        "security-auditor",
        "qa-specialist"
    ]
    
    print(f"\nAgent Plan ({len(agent_plan)} agents):")
    for i, agent in enumerate(agent_plan, 1):
        print(f"  {i}. {agent}")
    
    # Step 2: Start workflow
    print("\n[Starting Workflow]")
    logger.log_workflow_start(
        workflow_id=workflow_id,
        project_name="Task Management Web App",
        agent_plan=agent_plan,
        estimated_duration=21600
    )
    
    workflow_start_time = time.time()
    
    # Execute agents and log their work
    # (Implementation details here - see full file for complete example)
    
    print("\n[Workflow Complete]")
    print("See full implementation in workflow_coordination_example.py")


if __name__ == "__main__":
    build_web_application()
