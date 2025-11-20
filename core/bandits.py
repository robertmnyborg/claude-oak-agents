#!/usr/bin/env python3
"""
Multi-Armed Bandit Algorithms for Variant Selection

Implements UCB1 and Thompson Sampling as alternatives to epsilon-greedy Q-learning.
These algorithms provide intelligent exploration/exploitation trade-offs for
variant selection in continual learning scenarios.
"""

import math
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path


@dataclass
class ArmStatistics:
    """Statistics for a single bandit arm (variant)."""
    arm_id: str
    n_pulls: int = 0
    total_reward: float = 0.0
    rewards: List[float] = field(default_factory=list)
    last_updated: Optional[str] = None
    
    def average_reward(self) -> float:
        """Calculate average reward for this arm."""
        if self.n_pulls == 0:
            return 0.0
        return self.total_reward / self.n_pulls
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "arm_id": self.arm_id,
            "n_pulls": self.n_pulls,
            "total_reward": self.total_reward,
            "average_reward": self.average_reward(),
            "last_updated": self.last_updated
        }


class UCB1Bandit:
    """
    Upper Confidence Bound (UCB1) algorithm for variant selection.
    
    Balances exploration/exploitation using confidence intervals.
    UCB1 formula: average_reward + c * sqrt(2 * ln(total_plays) / plays_for_arm)
    
    Advantages over epsilon-greedy:
    - Deterministic (no random exploration)
    - Intelligent exploration (favors less-tried variants)
    - Better convergence properties
    - Theoretical guarantees on regret bounds
    
    Reference: Auer et al. (2002) "Finite-time Analysis of the Multiarmed Bandit Problem"
    """
    
    def __init__(
        self,
        exploration_constant: float = 1.414,
        state_file: Optional[Path] = None
    ):
        """
        Initialize UCB1 bandit.
        
        Args:
            exploration_constant: Controls exploration vs exploitation trade-off
                                 (default sqrt(2) ≈ 1.414 from UCB1 paper)
            state_file: Path to persistent state file (optional)
        """
        self.c = exploration_constant
        self.arm_stats: Dict[str, ArmStatistics] = {}
        self.total_pulls: int = 0
        
        # State persistence
        if state_file is None:
            project_root = Path(__file__).parent.parent
            state_file = project_root / "telemetry" / "crl" / "ucb1_state.jsonl"
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        self._load_state()
    
    def select_arm(
        self,
        available_arms: List[str],
        context: Optional[str] = None
    ) -> Tuple[str, float, Dict]:
        """
        Select arm using UCB1 formula.
        
        Strategy:
        1. If any arm has never been tried, try it (optimistic initialization)
        2. Otherwise, select arm with highest UCB value
        
        Args:
            available_arms: List of arm IDs to choose from
            context: Optional context string (agent:task_type)
        
        Returns:
            Tuple of (arm_id, ucb_value, metadata)
        """
        if not available_arms:
            raise ValueError("No arms available for selection")
        
        # Initialize arms that don't exist yet
        for arm_id in available_arms:
            if arm_id not in self.arm_stats:
                self.arm_stats[arm_id] = ArmStatistics(arm_id=arm_id)
        
        # Try any arm that has never been pulled (optimistic initialization)
        untried_arms = [
            arm_id for arm_id in available_arms
            if self.arm_stats[arm_id].n_pulls == 0
        ]
        
        if untried_arms:
            selected_arm = untried_arms[0]  # Deterministic selection
            ucb_value = float('inf')  # Infinite UCB for untried arms
            metadata = {
                "strategy": "optimistic_init",
                "total_pulls": self.total_pulls,
                "untried_arms_remaining": len(untried_arms)
            }
            return (selected_arm, ucb_value, metadata)
        
        # Calculate UCB value for each arm
        ucb_values = {}
        for arm_id in available_arms:
            ucb_values[arm_id] = self.get_ucb_value(arm_id, self.total_pulls)
        
        # Select arm with highest UCB value
        selected_arm = max(ucb_values.items(), key=lambda x: x[1])[0]
        ucb_value = ucb_values[selected_arm]
        
        metadata = {
            "strategy": "ucb1",
            "total_pulls": self.total_pulls,
            "ucb_values": {k: round(v, 4) for k, v in ucb_values.items()},
            "exploration_bonus": round(
                self.c * math.sqrt(
                    2 * math.log(self.total_pulls + 1) / 
                    (self.arm_stats[selected_arm].n_pulls + 1)
                ),
                4
            )
        }
        
        return (selected_arm, ucb_value, metadata)
    
    def update(self, arm_id: str, reward: float) -> None:
        """
        Update statistics after receiving reward.
        
        Args:
            arm_id: Arm that was pulled
            reward: Observed reward
        """
        if arm_id not in self.arm_stats:
            self.arm_stats[arm_id] = ArmStatistics(arm_id=arm_id)
        
        stats = self.arm_stats[arm_id]
        stats.n_pulls += 1
        stats.total_reward += reward
        stats.rewards.append(reward)
        stats.last_updated = datetime.utcnow().isoformat() + "Z"
        
        self.total_pulls += 1
        
        self._save_state()
    
    def get_ucb_value(self, arm_id: str, total_plays: int) -> float:
        """
        Calculate UCB value for an arm.
        
        UCB(arm) = avg_reward + c * sqrt(2 * ln(total) / n_arm)
        
        Args:
            arm_id: Arm to calculate UCB for
            total_plays: Total plays across all arms
        
        Returns:
            UCB value (higher = more promising)
        """
        if arm_id not in self.arm_stats:
            return float('inf')  # Untried arms get infinite UCB
        
        stats = self.arm_stats[arm_id]
        
        if stats.n_pulls == 0:
            return float('inf')
        
        avg_reward = stats.average_reward()
        
        if total_plays <= 1:
            return avg_reward
        
        exploration_bonus = self.c * math.sqrt(
            2 * math.log(total_plays) / stats.n_pulls
        )
        
        return avg_reward + exploration_bonus
    
    def get_statistics(self) -> Dict:
        """Get current bandit statistics."""
        return {
            "total_pulls": self.total_pulls,
            "num_arms": len(self.arm_stats),
            "arms": {
                arm_id: stats.to_dict()
                for arm_id, stats in self.arm_stats.items()
            }
        }
    
    def _load_state(self) -> None:
        """Load bandit state from file."""
        if not self.state_file.exists():
            return
        
        with open(self.state_file, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            return
        
        # Load last line (most recent state)
        state = json.loads(lines[-1])
        
        self.total_pulls = state.get("total_pulls", 0)
        
        for arm_id, arm_data in state.get("arms", {}).items():
            self.arm_stats[arm_id] = ArmStatistics(
                arm_id=arm_id,
                n_pulls=arm_data["n_pulls"],
                total_reward=arm_data["total_reward"],
                last_updated=arm_data.get("last_updated")
            )
    
    def _save_state(self) -> None:
        """Save bandit state to file."""
        state = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_pulls": self.total_pulls,
            "arms": {
                arm_id: {
                    "arm_id": stats.arm_id,
                    "n_pulls": stats.n_pulls,
                    "total_reward": stats.total_reward,
                    "average_reward": stats.average_reward(),
                    "last_updated": stats.last_updated
                }
                for arm_id, stats in self.arm_stats.items()
            }
        }
        
        with open(self.state_file, 'a') as f:
            f.write(json.dumps(state) + '\n')


class ThompsonSamplingBandit:
    """
    Thompson Sampling for variant selection.
    
    Bayesian approach: maintains belief distribution over rewards,
    samples from distribution to select variant.
    
    Better for:
    - Non-stationary environments (reward distributions change over time)
    - Delayed feedback scenarios
    - Complex reward structures
    - When prior knowledge exists
    
    Uses Beta distribution for binary rewards, can be extended to other distributions.
    
    Reference: Thompson (1933), Chapelle & Li (2011) "An Empirical Evaluation 
               of Thompson Sampling"
    """
    
    def __init__(
        self,
        alpha_prior: float = 1.0,
        beta_prior: float = 1.0,
        state_file: Optional[Path] = None
    ):
        """
        Initialize Thompson Sampling bandit with Beta priors.
        
        Args:
            alpha_prior: Prior successes (default 1.0 = uniform prior)
            beta_prior: Prior failures (default 1.0 = uniform prior)
            state_file: Path to persistent state file (optional)
        """
        self.alpha_prior = alpha_prior
        self.beta_prior = beta_prior
        
        # Posterior parameters: {arm_id: (alpha, beta)}
        self.posteriors: Dict[str, Tuple[float, float]] = {}
        self.total_pulls: int = 0
        
        # State persistence
        if state_file is None:
            project_root = Path(__file__).parent.parent
            state_file = project_root / "telemetry" / "crl" / "thompson_state.jsonl"
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        self._load_state()
    
    def select_arm(
        self,
        available_arms: List[str],
        context: Optional[str] = None
    ) -> Tuple[str, float, Dict]:
        """
        Select arm by sampling from Beta distributions.
        
        For each arm: sample theta ~ Beta(alpha, beta), select argmax(theta)
        
        Args:
            available_arms: List of arm IDs to choose from
            context: Optional context string (agent:task_type)
        
        Returns:
            Tuple of (arm_id, sampled_value, metadata)
        """
        if not available_arms:
            raise ValueError("No arms available for selection")
        
        # Initialize arms with prior if not seen
        for arm_id in available_arms:
            if arm_id not in self.posteriors:
                self.posteriors[arm_id] = (self.alpha_prior, self.beta_prior)
        
        # Sample theta from Beta distribution for each arm
        samples = {}
        for arm_id in available_arms:
            alpha, beta = self.posteriors[arm_id]
            # Sample from Beta(alpha, beta)
            samples[arm_id] = random.betavariate(alpha, beta)
        
        # Select arm with highest sampled value
        selected_arm = max(samples.items(), key=lambda x: x[1])[0]
        sampled_value = samples[selected_arm]
        
        alpha, beta = self.posteriors[selected_arm]
        expected_value = alpha / (alpha + beta)
        
        metadata = {
            "strategy": "thompson_sampling",
            "total_pulls": self.total_pulls,
            "sampled_values": {k: round(v, 4) for k, v in samples.items()},
            "selected_posterior": {
                "alpha": alpha,
                "beta": beta,
                "expected_value": round(expected_value, 4)
            }
        }
        
        return (selected_arm, sampled_value, metadata)
    
    def update(self, arm_id: str, reward: float) -> None:
        """
        Update Beta posterior after observing reward.
        
        For binary rewards:
        - Success (reward ≥ 0.5): alpha += 1
        - Failure (reward < 0.5): beta += 1
        
        Args:
            arm_id: Arm that was pulled
            reward: Observed reward (0.0 to 1.0)
        """
        if arm_id not in self.posteriors:
            self.posteriors[arm_id] = (self.alpha_prior, self.beta_prior)
        
        alpha, beta = self.posteriors[arm_id]
        
        # Convert reward to success/failure
        # Reward ≥ 0.5 counts as success, < 0.5 as failure
        if reward >= 0.5:
            alpha += 1  # Success
        else:
            beta += 1   # Failure
        
        self.posteriors[arm_id] = (alpha, beta)
        self.total_pulls += 1
        
        self._save_state()
    
    def get_statistics(self) -> Dict:
        """Get current bandit statistics."""
        stats = {
            "total_pulls": self.total_pulls,
            "num_arms": len(self.posteriors),
            "arms": {}
        }
        
        for arm_id, (alpha, beta) in self.posteriors.items():
            expected_value = alpha / (alpha + beta)
            variance = (alpha * beta) / ((alpha + beta) ** 2 * (alpha + beta + 1))
            
            stats["arms"][arm_id] = {
                "arm_id": arm_id,
                "alpha": alpha,
                "beta": beta,
                "expected_value": round(expected_value, 4),
                "variance": round(variance, 4),
                "n_samples": int(alpha + beta - self.alpha_prior - self.beta_prior)
            }
        
        return stats
    
    def _load_state(self) -> None:
        """Load bandit state from file."""
        if not self.state_file.exists():
            return
        
        with open(self.state_file, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            return
        
        # Load last line (most recent state)
        state = json.loads(lines[-1])
        
        self.total_pulls = state.get("total_pulls", 0)
        
        for arm_id, arm_data in state.get("arms", {}).items():
            self.posteriors[arm_id] = (arm_data["alpha"], arm_data["beta"])
    
    def _save_state(self) -> None:
        """Save bandit state to file."""
        state = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_pulls": self.total_pulls,
            "arms": {
                arm_id: {
                    "arm_id": arm_id,
                    "alpha": alpha,
                    "beta": beta,
                    "expected_value": alpha / (alpha + beta),
                    "n_samples": int(alpha + beta - self.alpha_prior - self.beta_prior)
                }
                for arm_id, (alpha, beta) in self.posteriors.items()
            }
        }
        
        with open(self.state_file, 'a') as f:
            f.write(json.dumps(state) + '\n')


def main():
    """Example usage of bandit algorithms."""
    print("=" * 60)
    print("Multi-Armed Bandit Algorithms Demo")
    print("=" * 60)
    print()
    
    # Available variants (arms)
    variants = ["default", "api-optimized", "database-focused"]
    
    # Test UCB1
    print("UCB1 Bandit Algorithm")
    print("-" * 60)
    
    ucb1 = UCB1Bandit(exploration_constant=1.414)
    
    print("Simulating 20 pulls...")
    for i in range(20):
        arm, ucb_value, metadata = ucb1.select_arm(variants)
        
        # Simulate reward (api-optimized is best)
        if arm == "api-optimized":
            reward = 0.7 + random.random() * 0.3  # 0.7-1.0
        elif arm == "default":
            reward = 0.4 + random.random() * 0.3  # 0.4-0.7
        else:
            reward = 0.2 + random.random() * 0.3  # 0.2-0.5
        
        ucb1.update(arm, reward)
        
        if i < 5 or i % 5 == 4:
            print(f"Pull {i+1}: {arm:20s} | UCB={ucb_value:.3f} | Reward={reward:.2f}")
    
    print("\nFinal Statistics:")
    stats = ucb1.get_statistics()
    for arm_id, arm_stats in stats["arms"].items():
        print(f"{arm_id:20s} | Pulls={arm_stats['n_pulls']:2d} | "
              f"Avg Reward={arm_stats['average_reward']:.3f}")
    
    print()
    print("=" * 60)
    
    # Test Thompson Sampling
    print("Thompson Sampling Bandit Algorithm")
    print("-" * 60)
    
    thompson = ThompsonSamplingBandit(alpha_prior=1.0, beta_prior=1.0)
    
    print("Simulating 20 pulls...")
    for i in range(20):
        arm, sampled_value, metadata = thompson.select_arm(variants)
        
        # Simulate reward (api-optimized is best)
        if arm == "api-optimized":
            reward = 0.7 + random.random() * 0.3  # 0.7-1.0
        elif arm == "default":
            reward = 0.4 + random.random() * 0.3  # 0.4-0.7
        else:
            reward = 0.2 + random.random() * 0.3  # 0.2-0.5
        
        thompson.update(arm, reward)
        
        if i < 5 or i % 5 == 4:
            print(f"Pull {i+1}: {arm:20s} | Sample={sampled_value:.3f} | Reward={reward:.2f}")
    
    print("\nFinal Statistics:")
    stats = thompson.get_statistics()
    for arm_id, arm_stats in stats["arms"].items():
        print(f"{arm_id:20s} | Samples={arm_stats['n_samples']:2d} | "
              f"Expected={arm_stats['expected_value']:.3f}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
