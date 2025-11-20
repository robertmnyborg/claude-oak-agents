#!/usr/bin/env python3
"""
Performance Comparison Tool for CRL Algorithms

Compares Q-learning, UCB1, Thompson Sampling, and Contextual Bandits
on simulated and real-world tasks.
"""

import random
import time
from typing import Dict, List, Tuple, Any
import numpy as np

from core.q_learning import QLearningEngine
from core.bandits import UCB1Bandit, ThompsonSamplingBandit
from core.contextual_bandits import ContextualBandit


class AlgorithmComparison:
    """
    Compare different bandit algorithms on standardized scenarios.
    """
    
    def __init__(self, num_trials: int = 100, num_arms: int = 3):
        """
        Initialize comparison framework.
        
        Args:
            num_trials: Number of trials per algorithm
            num_arms: Number of variants (arms)
        """
        self.num_trials = num_trials
        self.num_arms = num_arms
        
        # True reward distributions for each arm
        self.true_rewards = {
            "arm1": 0.5,  # Average performer
            "arm2": 0.8,  # Best performer
            "arm3": 0.3   # Poor performer
        }
    
    def simulate_reward(self, arm_id: str, noise: float = 0.1) -> float:
        """
        Simulate reward from pulling an arm.
        
        Args:
            arm_id: Arm to pull
            noise: Noise level (0-1)
        
        Returns:
            Noisy reward
        """
        true_reward = self.true_rewards.get(arm_id, 0.5)
        noise_value = random.uniform(-noise, noise)
        return max(0.0, min(1.0, true_reward + noise_value))
    
    def run_q_learning(self) -> Dict[str, Any]:
        """
        Run Q-learning algorithm.
        
        Returns:
            Performance metrics
        """
        q_learning = QLearningEngine(
            learning_rate=0.1,
            exploration_rate=0.1
        )
        
        arms = list(self.true_rewards.keys())
        total_reward = 0.0
        regret = 0.0
        best_arm_selections = 0
        
        start_time = time.time()
        
        for trial in range(self.num_trials):
            # Select arm
            arm, q_value, is_exploration = q_learning.select_variant(
                agent_name="test-agent",
                task_type="test-task",
                available_variants=arms
            )
            
            # Get reward
            reward = self.simulate_reward(arm)
            
            # Update
            q_learning.update_q_value("test-agent", "test-task", arm, reward)
            
            # Track metrics
            total_reward += reward
            regret += self.true_rewards["arm2"] - self.true_rewards[arm]
            
            if arm == "arm2":  # Best arm
                best_arm_selections += 1
        
        duration = time.time() - start_time
        
        return {
            "algorithm": "Q-Learning (ε-greedy)",
            "total_reward": total_reward,
            "avg_reward": total_reward / self.num_trials,
            "cumulative_regret": regret,
            "best_arm_percentage": (best_arm_selections / self.num_trials) * 100,
            "duration_ms": duration * 1000
        }
    
    def run_ucb1(self) -> Dict[str, Any]:
        """
        Run UCB1 algorithm.
        
        Returns:
            Performance metrics
        """
        ucb1 = UCB1Bandit(exploration_constant=1.414)
        
        arms = list(self.true_rewards.keys())
        total_reward = 0.0
        regret = 0.0
        best_arm_selections = 0
        
        start_time = time.time()
        
        for trial in range(self.num_trials):
            # Select arm
            arm, ucb_value, metadata = ucb1.select_arm(arms)
            
            # Get reward
            reward = self.simulate_reward(arm)
            
            # Update
            ucb1.update(arm, reward)
            
            # Track metrics
            total_reward += reward
            regret += self.true_rewards["arm2"] - self.true_rewards[arm]
            
            if arm == "arm2":  # Best arm
                best_arm_selections += 1
        
        duration = time.time() - start_time
        
        return {
            "algorithm": "UCB1",
            "total_reward": total_reward,
            "avg_reward": total_reward / self.num_trials,
            "cumulative_regret": regret,
            "best_arm_percentage": (best_arm_selections / self.num_trials) * 100,
            "duration_ms": duration * 1000
        }
    
    def run_thompson_sampling(self) -> Dict[str, Any]:
        """
        Run Thompson Sampling algorithm.
        
        Returns:
            Performance metrics
        """
        thompson = ThompsonSamplingBandit(alpha_prior=1.0, beta_prior=1.0)
        
        arms = list(self.true_rewards.keys())
        total_reward = 0.0
        regret = 0.0
        best_arm_selections = 0
        
        start_time = time.time()
        
        for trial in range(self.num_trials):
            # Select arm
            arm, sampled_value, metadata = thompson.select_arm(arms)
            
            # Get reward
            reward = self.simulate_reward(arm)
            
            # Update
            thompson.update(arm, reward)
            
            # Track metrics
            total_reward += reward
            regret += self.true_rewards["arm2"] - self.true_rewards[arm]
            
            if arm == "arm2":  # Best arm
                best_arm_selections += 1
        
        duration = time.time() - start_time
        
        return {
            "algorithm": "Thompson Sampling",
            "total_reward": total_reward,
            "avg_reward": total_reward / self.num_trials,
            "cumulative_regret": regret,
            "best_arm_percentage": (best_arm_selections / self.num_trials) * 100,
            "duration_ms": duration * 1000
        }
    
    def run_contextual(self) -> Dict[str, Any]:
        """
        Run Contextual Bandit (LinUCB) algorithm.
        
        Returns:
            Performance metrics
        """
        contextual = ContextualBandit(feature_dim=10)
        
        arms = list(self.true_rewards.keys())
        total_reward = 0.0
        regret = 0.0
        best_arm_selections = 0
        
        start_time = time.time()
        
        for trial in range(self.num_trials):
            # Generate context (simulated)
            context = np.random.rand(10)
            
            # Select arm
            arm, ucb_value, metadata = contextual.select_arm(arms, context)
            
            # Get reward (context-dependent)
            base_reward = self.simulate_reward(arm)
            # Add context bonus for best arm
            if arm == "arm2":
                context_bonus = 0.1 * context[0]  # First feature affects best arm
                reward = min(1.0, base_reward + context_bonus)
            else:
                reward = base_reward
            
            # Update
            contextual.update(arm, context, reward)
            
            # Track metrics
            total_reward += reward
            regret += self.true_rewards["arm2"] - self.true_rewards[arm]
            
            if arm == "arm2":  # Best arm
                best_arm_selections += 1
        
        duration = time.time() - start_time
        
        return {
            "algorithm": "LinUCB (Contextual)",
            "total_reward": total_reward,
            "avg_reward": total_reward / self.num_trials,
            "cumulative_regret": regret,
            "best_arm_percentage": (best_arm_selections / self.num_trials) * 100,
            "duration_ms": duration * 1000
        }
    
    def run_comparison(self) -> List[Dict[str, Any]]:
        """
        Run all algorithms and return comparison results.
        
        Returns:
            List of performance metrics for each algorithm
        """
        results = []
        
        print("Running algorithm comparison...")
        print(f"Trials: {self.num_trials}, Arms: {self.num_arms}")
        print(f"True rewards: {self.true_rewards}")
        print()
        
        # Run each algorithm
        results.append(self.run_q_learning())
        results.append(self.run_ucb1())
        results.append(self.run_thompson_sampling())
        results.append(self.run_contextual())
        
        return results
    
    def print_results(self, results: List[Dict[str, Any]]) -> None:
        """
        Print comparison results in formatted table.
        
        Args:
            results: List of performance metrics
        """
        print("=" * 80)
        print("Algorithm Comparison Results")
        print("=" * 80)
        print()
        
        # Header
        print(f"{'Algorithm':<25} | {'Avg Reward':>10} | {'Regret':>10} | "
              f"{'Best %':>8} | {'Time (ms)':>10}")
        print("-" * 80)
        
        # Results
        for result in results:
            print(f"{result['algorithm']:<25} | "
                  f"{result['avg_reward']:>10.4f} | "
                  f"{result['cumulative_regret']:>10.2f} | "
                  f"{result['best_arm_percentage']:>7.1f}% | "
                  f"{result['duration_ms']:>10.1f}")
        
        print()
        print("=" * 80)
        
        # Analysis
        best_reward = max(results, key=lambda r: r['avg_reward'])
        best_regret = min(results, key=lambda r: r['cumulative_regret'])
        fastest = min(results, key=lambda r: r['duration_ms'])
        
        print("Analysis:")
        print(f"  Highest average reward: {best_reward['algorithm']}")
        print(f"  Lowest regret: {best_regret['algorithm']}")
        print(f"  Fastest execution: {fastest['algorithm']}")
        print()


def main():
    """Run algorithm comparison."""
    comparison = AlgorithmComparison(num_trials=100, num_arms=3)
    
    results = comparison.run_comparison()
    comparison.print_results(results)
    
    print("Key Insights:")
    print("  - UCB1: Deterministic, theoretical guarantees, good convergence")
    print("  - Thompson: Handles non-stationary, Bayesian approach")
    print("  - Q-learning: Simple, established, random exploration")
    print("  - LinUCB: Context-aware, best when state features matter")
    print()


if __name__ == "__main__":
    main()
