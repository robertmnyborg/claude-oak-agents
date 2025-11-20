#!/usr/bin/env python3
"""
Rollback Manager for Continual Reinforcement Learning

Monitors variant performance and triggers rollbacks on degradation.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from core.agent_basis import AgentBasisManager
from core.q_learning import QLearningEngine
from core.safety_monitor import SafetyMonitor
from telemetry.logger import TelemetryLogger


class RollbackManager:
    """
    Monitors variant performance and triggers rollbacks on degradation.
    
    Rollback triggers:
    - Success rate drops >10% from baseline
    - Average reward drops >15% from baseline
    - Error rate increases >20% from baseline
    """
    
    def __init__(
        self,
        rollback_events_file: Optional[Path] = None
    ):
        """
        Initialize rollback manager.
        
        Args:
            rollback_events_file: Path to rollback events log
                                 (defaults to telemetry/crl/rollback_events.jsonl)
        """
        self.agent_basis = AgentBasisManager()
        self.q_learning = QLearningEngine()
        self.safety_monitor = SafetyMonitor()
        self.logger = TelemetryLogger()
        
        # Rollback events log
        if rollback_events_file is None:
            project_root = Path(__file__).parent.parent
            rollback_events_file = project_root / "telemetry" / "crl" / "rollback_events.jsonl"
        
        self.rollback_events_file = Path(rollback_events_file)
        self.rollback_events_file.parent.mkdir(parents=True, exist_ok=True)
        self.rollback_events_file.touch(exist_ok=True)
    
    def monitor_and_rollback(
        self,
        agent_name: str,
        task_type: str,
        current_variant: str
    ) -> Optional[Dict[str, Any]]:
        """
        Check current variant performance and trigger rollback if degraded.
        
        Args:
            agent_name: Agent name
            task_type: Task type
            current_variant: Current variant ID
        
        Returns:
            Rollback info if triggered, None otherwise
        """
        # Check degradation
        degraded, metrics = self.safety_monitor.check_performance_degradation(
            agent_name, task_type, current_variant
        )
        
        if not degraded:
            return None
        
        # Find previous best variant
        previous_best = self._find_previous_best_variant(agent_name, task_type, current_variant)
        
        if previous_best is None:
            # No alternative variant available
            return None
        
        # Execute rollback
        rollback_info = self._execute_rollback(
            agent_name=agent_name,
            task_type=task_type,
            from_variant=current_variant,
            to_variant=previous_best,
            reason=self._format_degradation_reason(metrics),
            degradation_metrics=metrics
        )
        
        return rollback_info
    
    def _find_previous_best_variant(
        self,
        agent_name: str,
        task_type: str,
        exclude_variant: Optional[str] = None
    ) -> Optional[str]:
        """
        Find the best-performing variant for a task type, excluding the current one.
        
        Args:
            agent_name: Agent name
            task_type: Task type
            exclude_variant: Variant to exclude from consideration
        
        Returns:
            Variant ID of previous best, or None if no suitable variant found
        """
        variants = self.agent_basis.list_variants(agent_name)
        
        if not variants:
            return None
        
        best_variant = None
        best_q_value = float('-inf')
        
        for variant_id in variants:
            # Skip excluded variant
            if exclude_variant and variant_id == exclude_variant:
                continue
            
            # Get Q-value
            q_value = self.q_learning.get_q_value(agent_name, task_type, variant_id)
            n_visits = self.q_learning.get_visit_count(agent_name, task_type, variant_id)
            
            # Require minimum sample size (5 visits)
            if n_visits < 5:
                continue
            
            if q_value > best_q_value:
                best_q_value = q_value
                best_variant = variant_id
        
        return best_variant
    
    def _execute_rollback(
        self,
        agent_name: str,
        task_type: str,
        from_variant: str,
        to_variant: str,
        reason: str,
        degradation_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute rollback and log the event.
        
        Args:
            agent_name: Agent name
            task_type: Task type
            from_variant: Variant being rolled back
            to_variant: Variant to roll back to
            reason: Human-readable reason for rollback
            degradation_metrics: Degradation metrics that triggered rollback
        
        Returns:
            Rollback info dictionary
        """
        rollback_id = f"rb-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
        
        rollback_info = {
            "rollback_id": rollback_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent_name": agent_name,
            "task_type": task_type,
            "from_variant": from_variant,
            "to_variant": to_variant,
            "reason": reason,
            "degradation_metrics": degradation_metrics
        }
        
        # Log rollback event
        with open(self.rollback_events_file, 'a') as f:
            f.write(json.dumps(rollback_info) + '\n')
        
        # TODO: Actually update variant default in agent basis
        # This would require extending AgentBasisManager with a concept of "default variant"
        # For now, we just log the rollback recommendation
        
        return rollback_info
    
    def _format_degradation_reason(self, metrics: Dict[str, Any]) -> str:
        """
        Format degradation metrics into human-readable reason.
        
        Args:
            metrics: Degradation metrics dictionary
        
        Returns:
            Human-readable degradation reason
        """
        reasons = []
        
        if metrics.get("degraded_success"):
            baseline = metrics["baseline_success_rate"]
            recent = metrics["recent_success_rate"]
            drop_pct = metrics["success_drop_pct"] * 100
            reasons.append(
                f"Success rate dropped from {baseline:.1%} to {recent:.1%} ({drop_pct:.1f}% drop)"
            )
        
        if metrics.get("degraded_reward"):
            baseline = metrics["baseline_avg_reward"]
            recent = metrics["recent_avg_reward"]
            drop_pct = metrics["reward_drop_pct"] * 100
            reasons.append(
                f"Average reward dropped from {baseline:.2f} to {recent:.2f} ({drop_pct:.1f}% drop)"
            )
        
        if metrics.get("degraded_error"):
            baseline = metrics["baseline_error_rate"]
            recent = metrics["recent_error_rate"]
            increase_pct = metrics["error_increase_pct"] * 100
            reasons.append(
                f"Error rate increased from {baseline:.1%} to {recent:.1%} ({increase_pct:.1f}% increase)"
            )
        
        if not reasons:
            return "Performance degradation detected"
        
        return "; ".join(reasons)
    
    def get_rollback_history(
        self,
        agent_name: Optional[str] = None,
        task_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get rollback history, optionally filtered.
        
        Args:
            agent_name: Filter by agent name (optional)
            task_type: Filter by task type (optional)
            limit: Maximum number of rollbacks to return (optional)
        
        Returns:
            List of rollback event dictionaries (newest first)
        """
        rollbacks = []
        
        if not self.rollback_events_file.exists():
            return []
        
        with open(self.rollback_events_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    rollback = json.loads(line)
                    
                    # Apply filters
                    if agent_name and rollback.get("agent_name") != agent_name:
                        continue
                    if task_type and rollback.get("task_type") != task_type:
                        continue
                    
                    rollbacks.append(rollback)
                except json.JSONDecodeError:
                    continue
        
        # Sort by timestamp (newest first)
        rollbacks.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Apply limit
        if limit is not None:
            rollbacks = rollbacks[:limit]
        
        return rollbacks


def main():
    """Example usage of rollback manager."""
    print("=" * 60)
    print("Rollback Manager Demo")
    print("=" * 60)
    print()
    
    manager = RollbackManager()
    
    # Example: Monitor and rollback if degraded
    agent_name = "backend-architect"
    task_type = "api-design"
    current_variant = "api-optimized"
    
    print("Monitoring variant performance...")
    print(f"Agent: {agent_name}")
    print(f"Task Type: {task_type}")
    print(f"Current Variant: {current_variant}")
    print()
    
    rollback_info = manager.monitor_and_rollback(
        agent_name=agent_name,
        task_type=task_type,
        current_variant=current_variant
    )
    
    if rollback_info:
        print("ROLLBACK TRIGGERED!")
        print("-" * 60)
        print(f"Rollback ID: {rollback_info['rollback_id']}")
        print(f"From: {rollback_info['from_variant']}")
        print(f"To: {rollback_info['to_variant']}")
        print(f"Reason: {rollback_info['reason']}")
        print()
        print("Degradation Metrics:")
        metrics = rollback_info['degradation_metrics']
        for key, value in metrics.items():
            if not key.startswith('degraded_') and key not in ['lookback_window', 'sample_size']:
                print(f"  {key}: {value}")
    else:
        print("No degradation detected - variant performing well")
    
    print()
    print("=" * 60)
    
    # Show rollback history
    print("Recent Rollback History")
    print("=" * 60)
    
    history = manager.get_rollback_history(limit=5)
    
    if history:
        for i, rollback in enumerate(history, 1):
            print(f"\n{i}. {rollback['rollback_id']}")
            print(f"   Agent: {rollback['agent_name']}")
            print(f"   Task Type: {rollback['task_type']}")
            print(f"   {rollback['from_variant']} → {rollback['to_variant']}")
            print(f"   Reason: {rollback['reason']}")
    else:
        print("\nNo rollback history found")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
