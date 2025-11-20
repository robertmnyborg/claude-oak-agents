#!/usr/bin/env python3
"""
Reward Calculator for Continual Reinforcement Learning

Calculates reward signal from invocation results using weighted formula:
    Reward = success_weight * success
           + quality_weight * quality_score  
           + speed_weight * (1 / duration_normalized)
           - error_penalty * error_count
"""

from typing import Optional


class RewardCalculator:
    """
    Calculate reward signal from invocation results.
    
    Reward components:
    - Success: Binary success/failure (40% weight)
    - Quality: Quality score 0-1 from quality-gate (30% weight)
    - Speed: Normalized execution duration (20% weight)
    - Errors: Error count penalty (10% per error)
    
    Reward range: [-1, 1]
    """
    
    # Component weights from architecture doc
    SUCCESS_WEIGHT = 0.4
    QUALITY_WEIGHT = 0.3
    SPEED_WEIGHT = 0.2
    ERROR_PENALTY = 0.1
    
    # Baseline durations for normalization (seconds)
    # Used to normalize speed_bonus: faster than baseline = bonus
    BASELINE_DURATIONS = {
        "low": 60,      # Simple tasks: 1 minute baseline
        "medium": 300,  # Medium tasks: 5 minutes baseline
        "high": 900     # Complex tasks: 15 minutes baseline
    }
    
    def __init__(
        self,
        success_weight: float = SUCCESS_WEIGHT,
        quality_weight: float = QUALITY_WEIGHT,
        speed_weight: float = SPEED_WEIGHT,
        error_penalty: float = ERROR_PENALTY
    ):
        """
        Initialize reward calculator with custom weights.
        
        Args:
            success_weight: Weight for success component (default: 0.4)
            quality_weight: Weight for quality component (default: 0.3)
            speed_weight: Weight for speed component (default: 0.2)
            error_penalty: Penalty per error (default: 0.1)
        """
        self.success_weight = success_weight
        self.quality_weight = quality_weight
        self.speed_weight = speed_weight
        self.error_penalty = error_penalty
    
    def calculate_reward(
        self,
        success: bool,
        quality_score: Optional[float] = None,
        duration_seconds: Optional[float] = None,
        error_count: int = 0,
        task_complexity: str = "medium"
    ) -> float:
        """
        Calculate reward in range [-1, 1].
        
        Formula:
            reward = success_component + quality_component + speed_component - error_component
        
        Where:
            - success_component = success_weight * (1 if success else -1)
            - quality_component = quality_weight * quality_score
            - speed_component = speed_weight * speed_bonus
            - error_component = error_penalty * error_count
        
        Args:
            success: Whether invocation was successful
            quality_score: Quality rating (0.0-1.0, optional)
            duration_seconds: Execution duration in seconds (optional)
            error_count: Number of errors encountered (default: 0)
            task_complexity: Task complexity level - "low", "medium", or "high" (default: "medium")
        
        Returns:
            Reward value in range [-1, 1]
        """
        # Success component
        success_component = self.success_weight * (1.0 if success else -1.0)
        
        # Quality component
        if quality_score is not None:
            # Clamp to [0, 1]
            quality_score = max(0.0, min(1.0, quality_score))
            quality_component = self.quality_weight * quality_score
        else:
            # No quality score: neutral (0.5 assumption)
            quality_component = self.quality_weight * 0.5
        
        # Speed component
        if duration_seconds is not None and duration_seconds > 0:
            speed_bonus = self._calculate_speed_bonus(duration_seconds, task_complexity)
            speed_component = self.speed_weight * speed_bonus
        else:
            # No duration: neutral
            speed_component = 0.0
        
        # Error component (penalty)
        error_component = self.error_penalty * error_count
        
        # Total reward
        reward = success_component + quality_component + speed_component - error_component
        
        # Clamp to [-1, 1]
        reward = max(-1.0, min(1.0, reward))
        
        return reward
    
    def _calculate_speed_bonus(self, duration_seconds: float, task_complexity: str) -> float:
        """
        Calculate speed bonus normalized by task complexity.
        
        Speed bonus:
        - Faster than baseline: positive bonus (0 to 1)
        - Slower than baseline: negative bonus (-1 to 0)
        
        Formula: 1 - (duration / baseline)
        
        Args:
            duration_seconds: Actual execution duration
            task_complexity: Task complexity level ("low", "medium", "high")
        
        Returns:
            Speed bonus in range [-1, 1]
        """
        baseline = self.BASELINE_DURATIONS.get(task_complexity, self.BASELINE_DURATIONS["medium"])
        
        # Normalized ratio: 1.0 = at baseline, <1.0 = faster, >1.0 = slower
        ratio = duration_seconds / baseline
        
        # Speed bonus: 1.0 for instant, 0.0 at baseline, negative for slower
        speed_bonus = 1.0 - ratio
        
        # Clamp to [-1, 1]
        speed_bonus = max(-1.0, min(1.0, speed_bonus))
        
        return speed_bonus
    
    def calculate_from_invocation(self, invocation_result: dict) -> float:
        """
        Calculate reward from invocation result dictionary.
        
        Convenience method that extracts fields from invocation result.
        
        Args:
            invocation_result: Dictionary with keys:
                - success: bool
                - quality_score: float (optional)
                - duration: float (optional)
                - error_count: int (optional)
                - task_complexity: str (optional)
        
        Returns:
            Calculated reward
        """
        return self.calculate_reward(
            success=invocation_result.get("success", False),
            quality_score=invocation_result.get("quality_score"),
            duration_seconds=invocation_result.get("duration"),
            error_count=invocation_result.get("error_count", 0),
            task_complexity=invocation_result.get("task_complexity", "medium")
        )


def main():
    """Example usage of reward calculator."""
    print("=" * 60)
    print("Reward Calculator Demo")
    print("=" * 60)
    print()
    
    calculator = RewardCalculator()
    
    # Test scenarios
    scenarios = [
        {
            "name": "Perfect Execution",
            "success": True,
            "quality_score": 1.0,
            "duration_seconds": 30,
            "error_count": 0,
            "task_complexity": "low"
        },
        {
            "name": "Success with Good Quality",
            "success": True,
            "quality_score": 0.85,
            "duration_seconds": 120,
            "error_count": 0,
            "task_complexity": "medium"
        },
        {
            "name": "Success but Slow",
            "success": True,
            "quality_score": 0.75,
            "duration_seconds": 600,
            "error_count": 0,
            "task_complexity": "medium"
        },
        {
            "name": "Success with Errors",
            "success": True,
            "quality_score": 0.70,
            "duration_seconds": 200,
            "error_count": 2,
            "task_complexity": "medium"
        },
        {
            "name": "Failure",
            "success": False,
            "quality_score": 0.30,
            "duration_seconds": 150,
            "error_count": 3,
            "task_complexity": "medium"
        },
        {
            "name": "Fast Complex Task",
            "success": True,
            "quality_score": 0.90,
            "duration_seconds": 300,
            "error_count": 0,
            "task_complexity": "high"
        }
    ]
    
    print("Reward Calculation Examples:")
    print("-" * 60)
    print()
    
    for scenario in scenarios:
        name = scenario.pop("name")
        reward = calculator.calculate_reward(**scenario)
        
        print(f"{name}:")
        print(f"  Success: {scenario['success']}")
        print(f"  Quality: {scenario.get('quality_score', 'N/A')}")
        print(f"  Duration: {scenario.get('duration_seconds', 'N/A')}s")
        print(f"  Errors: {scenario['error_count']}")
        print(f"  Complexity: {scenario['task_complexity']}")
        print(f"  → Reward: {reward:+.3f}")
        print()
    
    print("=" * 60)
    print("Component Weights:")
    print(f"  Success: {calculator.success_weight * 100:.0f}%")
    print(f"  Quality: {calculator.quality_weight * 100:.0f}%")
    print(f"  Speed: {calculator.speed_weight * 100:.0f}%")
    print(f"  Error Penalty: {calculator.error_penalty * 100:.0f}% per error")
    print("=" * 60)


if __name__ == "__main__":
    main()
