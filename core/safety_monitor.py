#!/usr/bin/env python3
"""
Safety Monitor for Continual Reinforcement Learning

Determines whether variant changes can be auto-applied or require human approval
based on confidence thresholds and safety criteria.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from core.q_learning import QLearningEngine
from core.agent_basis import AgentBasisManager
from telemetry.logger import TelemetryLogger


class SafetyMonitor:
    """
    Determines whether variant changes can be auto-applied or require human approval.
    
    Decision matrix from architecture doc:
    - High confidence (Q-value > 0.9, n_visits >= 10): Auto-apply
    - Medium confidence (Q-value > 0.7, n_visits >= 5): Human approval
    - Low confidence (else): No action
    
    Degradation detection:
    - Success rate drops >10% from baseline
    - Average reward drops >15% from baseline
    - Error rate increases >20% from baseline
    """
    
    def __init__(
        self,
        auto_apply_q_threshold: float = 0.9,
        auto_apply_min_samples: int = 10,
        human_approval_q_threshold: float = 0.7,
        human_approval_min_samples: int = 5,
        degradation_success_threshold: float = 0.10,
        degradation_reward_threshold: float = 0.15,
        degradation_error_threshold: float = 0.20,
        lookback_window: int = 20
    ):
        """
        Initialize safety thresholds from architecture doc.
        
        Args:
            auto_apply_q_threshold: Q-value threshold for auto-apply (default: 0.9)
            auto_apply_min_samples: Minimum visits for auto-apply (default: 10)
            human_approval_q_threshold: Q-value threshold for human approval (default: 0.7)
            human_approval_min_samples: Minimum visits for human approval (default: 5)
            degradation_success_threshold: Success rate drop threshold (default: 0.10 = 10%)
            degradation_reward_threshold: Reward drop threshold (default: 0.15 = 15%)
            degradation_error_threshold: Error rate increase threshold (default: 0.20 = 20%)
            lookback_window: Number of recent invocations to analyze (default: 20)
        """
        self.auto_apply_q_threshold = auto_apply_q_threshold
        self.auto_apply_min_samples = auto_apply_min_samples
        self.human_approval_q_threshold = human_approval_q_threshold
        self.human_approval_min_samples = human_approval_min_samples
        self.degradation_success_threshold = degradation_success_threshold
        self.degradation_reward_threshold = degradation_reward_threshold
        self.degradation_error_threshold = degradation_error_threshold
        self.lookback_window = lookback_window
        
        # Initialize dependencies
        self.q_learning = QLearningEngine()
        self.agent_basis = AgentBasisManager()
        self.logger = TelemetryLogger()
    
    def should_auto_apply_variant(
        self,
        agent_name: str,
        task_type: str,
        variant_id: str,
        q_value: Optional[float] = None,
        n_visits: Optional[int] = None,
        current_default: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Determine if variant should be auto-applied as new default.
        
        Args:
            agent_name: Agent name
            task_type: Task type
            variant_id: Variant to evaluate
            q_value: Q-value (optional, will fetch if not provided)
            n_visits: Visit count (optional, will fetch if not provided)
            current_default: Current default variant (optional)
        
        Returns:
            Tuple of (decision, reasoning)
            decision: "auto_apply", "human_approval", "no_action"
            reasoning: Human-readable explanation
        """
        # Get Q-value and visit count if not provided
        if q_value is None:
            q_value = self.q_learning.get_q_value(agent_name, task_type, variant_id)
        if n_visits is None:
            n_visits = self.q_learning.get_visit_count(agent_name, task_type, variant_id)
        
        # Decision logic based on architecture doc thresholds
        if (q_value >= self.auto_apply_q_threshold and 
            n_visits >= self.auto_apply_min_samples):
            # High confidence: auto-apply
            reasoning = (
                f"High confidence: Q-value {q_value:.3f} >= {self.auto_apply_q_threshold}, "
                f"{n_visits} visits >= {self.auto_apply_min_samples}. "
                f"Variant demonstrates consistent high performance."
            )
            
            # Additional check: Don't auto-apply if variant is already default
            if current_default and current_default == variant_id:
                return ("no_action", f"Variant '{variant_id}' is already the default.")
            
            return ("auto_apply", reasoning)
        
        elif (q_value >= self.human_approval_q_threshold and 
              n_visits >= self.human_approval_min_samples):
            # Medium confidence: require human approval
            reasoning = (
                f"Medium confidence: Q-value {q_value:.3f} >= {self.human_approval_q_threshold}, "
                f"{n_visits} visits >= {self.human_approval_min_samples}. "
                f"Variant shows promise but requires human review."
            )
            return ("human_approval", reasoning)
        
        else:
            # Low confidence: no action
            if n_visits < self.human_approval_min_samples:
                reasoning = (
                    f"Insufficient data: {n_visits} visits < {self.human_approval_min_samples}. "
                    f"Need more invocations to evaluate performance."
                )
            else:
                reasoning = (
                    f"Low confidence: Q-value {q_value:.3f} < {self.human_approval_q_threshold}. "
                    f"Variant not performing well enough for promotion."
                )
            return ("no_action", reasoning)
    
    def check_performance_degradation(
        self,
        agent_name: str,
        task_type: str,
        variant_id: str,
        lookback_window: Optional[int] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Check if variant performance has degraded significantly.
        
        Degradation criteria:
        - Success rate drops >10% from baseline
        - Average reward drops >15% from baseline
        - Error rate increases >20% from baseline
        
        Args:
            agent_name: Agent name
            task_type: Task type
            variant_id: Variant to evaluate
            lookback_window: Number of recent invocations to analyze (default: 20)
        
        Returns:
            Tuple of (degraded, metrics)
            degraded: True if performance degradation detected
            metrics: Dictionary with degradation details
        """
        if lookback_window is None:
            lookback_window = self.lookback_window
        
        # Load variant for baseline metrics
        variant = self.agent_basis.load_variant(agent_name, variant_id)
        if variant is None:
            return (False, {"error": f"Variant {agent_name}:{variant_id} not found"})
        
        # Get task-specific metrics
        if task_type not in variant.task_type_performance:
            return (False, {"error": f"No performance data for task type {task_type}"})
        
        task_metrics = variant.task_type_performance[task_type]
        
        # Check if enough data for baseline
        if task_metrics["invocation_count"] < lookback_window:
            return (False, {
                "error": f"Insufficient data for baseline "
                        f"({task_metrics['invocation_count']} < {lookback_window})"
            })
        
        # Get recent invocations from telemetry
        recent_invocations = self._get_recent_invocations(
            agent_name, task_type, variant_id, lookback_window
        )
        
        if len(recent_invocations) < lookback_window // 2:
            return (False, {
                "error": f"Insufficient recent data "
                        f"({len(recent_invocations)} < {lookback_window // 2})"
            })
        
        # Calculate recent metrics
        recent_success_rate = self._calculate_success_rate(recent_invocations)
        recent_avg_reward = self._calculate_avg_reward(recent_invocations)
        recent_error_rate = self._calculate_error_rate(recent_invocations)
        
        # Baseline metrics
        baseline_success_rate = (
            task_metrics["success_count"] / task_metrics["invocation_count"]
        )
        baseline_avg_reward = task_metrics["avg_reward"]
        baseline_error_rate = 1.0 - baseline_success_rate
        
        # Calculate degradation
        success_drop = baseline_success_rate - recent_success_rate
        success_drop_pct = (
            success_drop / baseline_success_rate if baseline_success_rate > 0 else 0
        )
        
        reward_drop = baseline_avg_reward - recent_avg_reward
        reward_drop_pct = (
            reward_drop / baseline_avg_reward if baseline_avg_reward > 0 else 0
        )
        
        error_increase = recent_error_rate - baseline_error_rate
        error_increase_pct = (
            error_increase / baseline_error_rate if baseline_error_rate > 0 else 0
        )
        
        # Check degradation thresholds
        degraded = (
            success_drop_pct > self.degradation_success_threshold or
            reward_drop_pct > self.degradation_reward_threshold or
            error_increase_pct > self.degradation_error_threshold
        )
        
        metrics = {
            "baseline_success_rate": baseline_success_rate,
            "recent_success_rate": recent_success_rate,
            "success_drop_pct": success_drop_pct,
            "degraded_success": success_drop_pct > self.degradation_success_threshold,
            
            "baseline_avg_reward": baseline_avg_reward,
            "recent_avg_reward": recent_avg_reward,
            "reward_drop_pct": reward_drop_pct,
            "degraded_reward": reward_drop_pct > self.degradation_reward_threshold,
            
            "baseline_error_rate": baseline_error_rate,
            "recent_error_rate": recent_error_rate,
            "error_increase_pct": error_increase_pct,
            "degraded_error": error_increase_pct > self.degradation_error_threshold,
            
            "lookback_window": lookback_window,
            "sample_size": len(recent_invocations)
        }
        
        return (degraded, metrics)
    
    def _get_recent_invocations(
        self,
        agent_name: str,
        task_type: str,
        variant_id: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Get recent invocations from telemetry for a specific variant.
        
        Args:
            agent_name: Agent name
            task_type: Task type
            variant_id: Variant ID
            limit: Maximum number of invocations to retrieve
        
        Returns:
            List of invocation dictionaries (most recent first)
        """
        invocations = []
        invocations_file = self.logger.invocations_file
        
        if not invocations_file.exists():
            return []
        
        # Read invocations in reverse order (newest first)
        with open(invocations_file, 'r') as f:
            lines = f.readlines()
        
        for line in reversed(lines):
            if not line.strip():
                continue
            
            try:
                inv = json.loads(line)
                
                # Match agent, task type, and variant
                if (inv.get("agent_name") == agent_name and
                    inv.get("task_type") == task_type and
                    inv.get("agent_variant") == variant_id):
                    invocations.append(inv)
                    
                    if len(invocations) >= limit:
                        break
            except json.JSONDecodeError:
                continue
        
        return invocations
    
    def _calculate_success_rate(self, invocations: List[Dict[str, Any]]) -> float:
        """Calculate success rate from invocations."""
        if not invocations:
            return 0.0
        
        success_count = sum(
            1 for inv in invocations
            if inv.get("outcome", {}).get("status") == "success"
        )
        
        return success_count / len(invocations)
    
    def _calculate_avg_reward(self, invocations: List[Dict[str, Any]]) -> float:
        """Calculate average reward from invocations."""
        if not invocations:
            return 0.0
        
        rewards = [
            inv.get("reward", 0.0) for inv in invocations
            if inv.get("reward") is not None
        ]
        
        if not rewards:
            return 0.0
        
        return sum(rewards) / len(rewards)
    
    def _calculate_error_rate(self, invocations: List[Dict[str, Any]]) -> float:
        """Calculate error rate from invocations."""
        if not invocations:
            return 0.0
        
        error_count = sum(
            1 for inv in invocations
            if inv.get("outcome", {}).get("status") in ["failure", "error"]
        )
        
        return error_count / len(invocations)


def main():
    """Example usage of safety monitor."""
    print("=" * 60)
    print("Safety Monitor Demo")
    print("=" * 60)
    print()
    
    monitor = SafetyMonitor()
    
    # Example: Check if variant should be auto-applied
    agent_name = "backend-architect"
    task_type = "api-design"
    variant_id = "api-optimized"
    
    print("Scenario 1: High Confidence Variant")
    print("-" * 60)
    
    decision, reasoning = monitor.should_auto_apply_variant(
        agent_name=agent_name,
        task_type=task_type,
        variant_id=variant_id,
        q_value=0.92,  # High Q-value
        n_visits=15    # Sufficient visits
    )
    
    print(f"Decision: {decision}")
    print(f"Reasoning: {reasoning}")
    print()
    
    # Example: Medium confidence
    print("Scenario 2: Medium Confidence Variant")
    print("-" * 60)
    
    decision, reasoning = monitor.should_auto_apply_variant(
        agent_name=agent_name,
        task_type=task_type,
        variant_id="database-focused",
        q_value=0.75,  # Medium Q-value
        n_visits=8     # Moderate visits
    )
    
    print(f"Decision: {decision}")
    print(f"Reasoning: {reasoning}")
    print()
    
    # Example: Low confidence
    print("Scenario 3: Low Confidence Variant")
    print("-" * 60)
    
    decision, reasoning = monitor.should_auto_apply_variant(
        agent_name=agent_name,
        task_type=task_type,
        variant_id="experimental",
        q_value=0.65,  # Low Q-value
        n_visits=3     # Few visits
    )
    
    print(f"Decision: {decision}")
    print(f"Reasoning: {reasoning}")
    print()
    
    print("=" * 60)


if __name__ == "__main__":
    main()
