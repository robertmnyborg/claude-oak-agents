#!/usr/bin/env python3
"""
Workflow Monitor - Phase 3: Workflow Intelligence

Real-time monitoring and analysis of multi-agent workflows.
Tracks workflow execution, detects bottlenecks, identifies parallelization
opportunities, and calculates critical paths.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict


class WorkflowMonitor:
    """Real-time monitoring of multi-agent workflows."""

    def __init__(self, telemetry_dir: Optional[Path] = None):
        """
        Initialize the workflow monitor.

        Args:
            telemetry_dir: Directory containing telemetry files.
        """
        if telemetry_dir is None:
            telemetry_dir = Path(__file__).parent

        self.telemetry_dir = Path(telemetry_dir)
        self.workflow_events_file = self.telemetry_dir / "workflow_events.jsonl"
        self.invocations_file = self.telemetry_dir / "agent_invocations.jsonl"
        self.phase3_dir = self.telemetry_dir / "phase3"
        self.phase3_dir.mkdir(exist_ok=True)

        # In-memory cache of active workflows
        self.active_workflows: Dict[str, Dict[str, Any]] = {}

    def track_workflow_start(
        self,
        workflow_id: str,
        agents_planned: List[str],
        estimated_duration_minutes: float,
        session_id: str,
        task_description: str
    ) -> None:
        """
        Log workflow initiation with plan.

        Args:
            workflow_id: Unique workflow identifier
            agents_planned: List of agents planned to execute
            estimated_duration_minutes: Estimated total duration
            session_id: Session identifier
            task_description: Description of the workflow task
        """
        workflow_data = {
            "workflow_id": workflow_id,
            "session_id": session_id,
            "event": "workflow_start",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_description": task_description,
            "agents_planned": agents_planned,
            "estimated_duration_minutes": estimated_duration_minutes,
            "agents_executed": [],
            "handoffs": [],
            "bottlenecks": [],
            "status": "active"
        }

        # Cache in memory
        self.active_workflows[workflow_id] = workflow_data

        # Log event
        self._log_event({
            "workflow_id": workflow_id,
            "session_id": session_id,
            "event": "workflow_start",
            "timestamp": workflow_data["timestamp"],
            "agents_planned": agents_planned,
            "estimated_duration_minutes": estimated_duration_minutes
        })

    def track_agent_handoff(
        self,
        workflow_id: str,
        from_agent: str,
        to_agent: str,
        context_size_kb: float,
        handoff_reason: str
    ) -> None:
        """
        Track agent-to-agent transitions.

        Args:
            workflow_id: Unique workflow identifier
            from_agent: Agent passing control
            to_agent: Agent receiving control
            context_size_kb: Size of context passed (KB)
            handoff_reason: Reason for handoff
        """
        handoff_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from_agent": from_agent,
            "to_agent": to_agent,
            "context_size_kb": context_size_kb,
            "reason": handoff_reason
        }

        # Update cache
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]["handoffs"].append(handoff_data)

        # Log event
        self._log_event({
            "workflow_id": workflow_id,
            "event": "agent_handoff",
            "timestamp": handoff_data["timestamp"],
            "from_agent": from_agent,
            "to_agent": to_agent,
            "context_size_kb": context_size_kb,
            "reason": handoff_reason
        })

    def track_workflow_complete(
        self,
        workflow_id: str,
        agents_executed: List[str],
        duration_seconds: float,
        success: bool,
        session_id: str
    ) -> None:
        """
        Log workflow completion.

        Args:
            workflow_id: Unique workflow identifier
            agents_executed: List of agents that actually executed
            duration_seconds: Total workflow duration
            success: Whether workflow succeeded
            session_id: Session identifier
        """
        completion_data = {
            "workflow_id": workflow_id,
            "session_id": session_id,
            "event": "workflow_complete",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agents_executed": agents_executed,
            "duration_seconds": duration_seconds,
            "success": success
        }

        # Remove from active workflows
        if workflow_id in self.active_workflows:
            del self.active_workflows[workflow_id]

        # Log event
        self._log_event(completion_data)

    def detect_bottleneck(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Identify agents causing delays in active workflow.

        Args:
            workflow_id: Unique workflow identifier

        Returns:
            Dictionary with bottleneck info or None if no bottleneck
        """
        # Load workflow data
        workflow = self._load_workflow(workflow_id)
        if not workflow:
            return None

        # Load agent execution times
        agent_durations = self._get_agent_durations(workflow_id)
        if not agent_durations:
            return None

        # Calculate workflow total time
        workflow_start = self._parse_timestamp(workflow["start"]["timestamp"])
        workflow_end = self._parse_timestamp(workflow["complete"]["timestamp"])
        total_duration = (workflow_end - workflow_start).total_seconds()

        # Find agent that took >40% of total time
        bottlenecks = []
        for agent_name, duration in agent_durations.items():
            if duration / total_duration > 0.4:
                bottlenecks.append({
                    "agent_name": agent_name,
                    "duration_seconds": duration,
                    "percentage_of_workflow": (duration / total_duration) * 100,
                    "wait_time_seconds": 0,  # Would need more detailed tracking
                    "reason": f"Agent took {(duration/total_duration)*100:.1f}% of total workflow time"
                })

        if bottlenecks:
            return {
                "workflow_id": workflow_id,
                "bottlenecks": bottlenecks,
                "total_duration": total_duration,
                "detected_at": datetime.now(timezone.utc).isoformat()
            }

        return None

    def suggest_parallelization(self, workflow_id: str) -> List[Tuple[str, str]]:
        """
        Identify sequential work that could be parallel.

        Args:
            workflow_id: Unique workflow identifier

        Returns:
            List of (agent_a, agent_b) tuples that can run concurrently
        """
        # Load workflow data
        workflow = self._load_workflow(workflow_id)
        if not workflow:
            return []

        agents_executed = workflow.get("complete", {}).get("agents_executed", [])

        # Build dependency graph from handoffs
        dependencies = defaultdict(set)
        if "handoffs" in workflow:
            for handoff in workflow["handoffs"]:
                to_agent = handoff["to_agent"]
                from_agent = handoff["from_agent"]
                dependencies[to_agent].add(from_agent)

        # Find pairs of agents with no dependencies
        parallelizable = []
        for i, agent_a in enumerate(agents_executed):
            for agent_b in agents_executed[i+1:]:
                # Check if agents are independent
                if (agent_b not in dependencies.get(agent_a, set()) and
                    agent_a not in dependencies.get(agent_b, set())):
                    parallelizable.append((agent_a, agent_b))

        return parallelizable

    def calculate_critical_path(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Find the longest dependency chain.

        Args:
            workflow_id: Unique workflow identifier

        Returns:
            Dictionary with critical path info or None
        """
        # Load workflow data
        workflow = self._load_workflow(workflow_id)
        if not workflow:
            return None

        agents_executed = workflow.get("complete", {}).get("agents_executed", [])
        agent_durations = self._get_agent_durations(workflow_id)

        if not agents_executed or not agent_durations:
            return None

        # Build dependency graph
        dependencies = defaultdict(set)
        if "handoffs" in workflow:
            for handoff in workflow["handoffs"]:
                to_agent = handoff["to_agent"]
                from_agent = handoff["from_agent"]
                dependencies[to_agent].add(from_agent)

        # Calculate longest path using dynamic programming
        def calculate_path_duration(agent: str, memo: Dict[str, float]) -> float:
            if agent in memo:
                return memo[agent]

            agent_duration = agent_durations.get(agent, 0)

            # If agent has dependencies, add max dependency path
            if agent in dependencies and dependencies[agent]:
                max_dep_duration = max(
                    calculate_path_duration(dep, memo)
                    for dep in dependencies[agent]
                )
                total = agent_duration + max_dep_duration
            else:
                total = agent_duration

            memo[agent] = total
            return total

        memo: Dict[str, float] = {}

        # Find agent with longest path
        max_duration = 0
        critical_agent = None

        for agent in agents_executed:
            duration = calculate_path_duration(agent, memo)
            if duration > max_duration:
                max_duration = duration
                critical_agent = agent

        if critical_agent:
            # Reconstruct critical path
            path = []
            current = critical_agent
            path.append(current)

            while current in dependencies and dependencies[current]:
                # Find which dependency contributed to critical path
                deps = dependencies[current]
                max_dep = max(deps, key=lambda d: memo.get(d, 0))
                path.insert(0, max_dep)
                current = max_dep

            return {
                "workflow_id": workflow_id,
                "critical_path": path,
                "duration_seconds": max_duration,
                "percentage_of_total": (max_duration / sum(agent_durations.values())) * 100
            }

        return None

    def detect_dependency_conflicts(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Detect conflicts in agent outputs (file modifications, contradictory outputs).

        Args:
            workflow_id: Unique workflow identifier

        Returns:
            List of detected conflicts
        """
        # Load invocations for this workflow
        invocations = self._get_workflow_invocations(workflow_id)

        conflicts = []

        # Track files modified by each agent
        file_modifications = defaultdict(list)

        for inv in invocations:
            agent_name = inv.get("agent_name")
            files_modified = inv.get("outcome", {}).get("files_modified", [])

            for file_path in files_modified:
                file_modifications[file_path].append(agent_name)

        # Find files modified by multiple agents
        for file_path, agents in file_modifications.items():
            if len(agents) > 1:
                conflicts.append({
                    "type": "file_modification_overlap",
                    "file_path": file_path,
                    "agents": agents,
                    "severity": "medium",
                    "description": f"File {file_path} modified by multiple agents"
                })

        return conflicts

    def _log_event(self, event_data: Dict[str, Any]) -> None:
        """Log workflow event to JSONL file."""
        with open(self.workflow_events_file, "a") as f:
            f.write(json.dumps(event_data) + "\n")

    def _load_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Load workflow data from events file."""
        if not self.workflow_events_file.exists():
            return None

        workflow_data: Dict[str, Any] = {
            "workflow_id": workflow_id,
            "handoffs": []
        }

        with open(self.workflow_events_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue

                event = json.loads(line)
                if event.get("workflow_id") != workflow_id:
                    continue

                event_type = event.get("event")

                if event_type == "workflow_start":
                    workflow_data["start"] = event
                elif event_type == "workflow_complete":
                    workflow_data["complete"] = event
                elif event_type == "agent_handoff":
                    workflow_data["handoffs"].append(event)

        if "start" not in workflow_data:
            return None

        return workflow_data

    def _get_agent_durations(self, workflow_id: str) -> Dict[str, float]:
        """Get agent execution durations for a workflow."""
        durations = {}

        if not self.invocations_file.exists():
            return durations

        with open(self.invocations_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue

                inv = json.loads(line)
                if inv.get("workflow_id") != workflow_id:
                    continue

                agent_name = inv.get("agent_name")
                duration = inv.get("duration_seconds", 0)

                if agent_name and duration:
                    durations[agent_name] = duration

        return durations

    def _get_workflow_invocations(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get all invocations for a workflow."""
        invocations = []

        if not self.invocations_file.exists():
            return invocations

        with open(self.invocations_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue

                inv = json.loads(line)
                if inv.get("workflow_id") == workflow_id:
                    invocations.append(inv)

        return invocations

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse ISO timestamp string to datetime."""
        return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

    def get_active_workflows(self) -> List[Dict[str, Any]]:
        """Get list of currently active workflows."""
        return list(self.active_workflows.values())

    def get_workflow_stats(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive statistics for a workflow.

        Args:
            workflow_id: Unique workflow identifier

        Returns:
            Dictionary with workflow statistics or None
        """
        workflow = self._load_workflow(workflow_id)
        if not workflow or "complete" not in workflow:
            return None

        agent_durations = self._get_agent_durations(workflow_id)

        # Calculate statistics
        start_time = self._parse_timestamp(workflow["start"]["timestamp"])
        end_time = self._parse_timestamp(workflow["complete"]["timestamp"])
        total_duration = (end_time - start_time).total_seconds()

        agent_execution_time = sum(agent_durations.values())
        coordination_overhead = total_duration - agent_execution_time
        overhead_pct = (coordination_overhead / total_duration * 100) if total_duration > 0 else 0

        return {
            "workflow_id": workflow_id,
            "total_duration_seconds": total_duration,
            "agent_execution_time_seconds": agent_execution_time,
            "coordination_overhead_seconds": coordination_overhead,
            "coordination_overhead_pct": overhead_pct,
            "agents_executed": workflow["complete"]["agents_executed"],
            "num_agents": len(workflow["complete"]["agents_executed"]),
            "num_handoffs": len(workflow.get("handoffs", [])),
            "success": workflow["complete"]["success"],
            "bottlenecks": self.detect_bottleneck(workflow_id),
            "parallelization_opportunities": self.suggest_parallelization(workflow_id),
            "critical_path": self.calculate_critical_path(workflow_id),
            "conflicts": self.detect_dependency_conflicts(workflow_id)
        }


def main():
    """Example usage of WorkflowMonitor."""
    monitor = WorkflowMonitor()

    print("Workflow Monitor - Phase 3")
    print("=" * 70)

    # Check for active workflows
    active = monitor.get_active_workflows()
    print(f"\nActive Workflows: {len(active)}")

    # Load all workflows from events file
    if monitor.workflow_events_file.exists():
        workflow_ids = set()
        with open(monitor.workflow_events_file, "r") as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)
                    workflow_ids.add(event.get("workflow_id"))

        print(f"Total Workflows Tracked: {len(workflow_ids)}")

        # Analyze each workflow
        for wf_id in workflow_ids:
            stats = monitor.get_workflow_stats(wf_id)
            if stats:
                print(f"\nWorkflow: {wf_id}")
                print(f"  Duration: {stats['total_duration_seconds']:.1f}s")
                print(f"  Agents: {stats['num_agents']}")
                print(f"  Coordination Overhead: {stats['coordination_overhead_pct']:.1f}%")

                if stats['bottlenecks']:
                    print(f"  Bottlenecks: {len(stats['bottlenecks']['bottlenecks'])}")

                if stats['parallelization_opportunities']:
                    print(f"  Parallelization Opportunities: {len(stats['parallelization_opportunities'])}")
    else:
        print("\nNo workflow data yet. Run multi-agent workflows to populate data.")


if __name__ == "__main__":
    main()
