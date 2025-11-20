#!/usr/bin/env python3
"""
Phase 4 Advanced CRL Algorithms - Example Usage

Demonstrates UCB1, Thompson Sampling, Contextual Bandits,
Transfer Learning, and Variant Mutation.
"""

import numpy as np
from pathlib import Path

from core.bandits import UCB1Bandit, ThompsonSamplingBandit
from core.contextual_bandits import ContextualBandit
from core.transfer_learning import TransferLearningEngine
from core.variant_mutator import VariantMutator


def example_ucb1():
    """Example: Using UCB1 for variant selection."""
    print("=" * 60)
    print("Example 1: UCB1 Bandit Algorithm")
    print("=" * 60)
    print()
    
    ucb1 = UCB1Bandit(exploration_constant=1.414)
    
    variants = ["default", "api-optimized", "database-focused"]
    
    print("Selecting variants using UCB1...")
    print()
    
    for i in range(10):
        # Select variant
        variant, ucb_value, metadata = ucb1.select_arm(variants)
        
        # Simulate execution with reward
        # In real usage, this comes from actual execution results
        import random
        if variant == "api-optimized":
            reward = 0.7 + random.random() * 0.3  # Best performer
        else:
            reward = 0.4 + random.random() * 0.3  # Average
        
        # Update UCB1
        ucb1.update(variant, reward)
        
        print(f"Round {i+1}: Selected {variant:20s} | "
              f"UCB={ucb_value:.3f} | Reward={reward:.2f}")
    
    print()
    print("Final Statistics:")
    stats = ucb1.get_statistics()
    for arm_id, arm_stats in stats["arms"].items():
        print(f"  {arm_id:20s} | Pulls={arm_stats['n_pulls']:2d} | "
              f"Avg={arm_stats['average_reward']:.3f}")
    print()


def example_thompson_sampling():
    """Example: Using Thompson Sampling for variant selection."""
    print("=" * 60)
    print("Example 2: Thompson Sampling Algorithm")
    print("=" * 60)
    print()
    
    thompson = ThompsonSamplingBandit(alpha_prior=1.0, beta_prior=1.0)
    
    variants = ["default", "api-optimized", "database-focused"]
    
    print("Selecting variants using Thompson Sampling...")
    print()
    
    for i in range(10):
        # Select variant
        variant, sampled_value, metadata = thompson.select_arm(variants)
        
        # Simulate execution with reward
        import random
        if variant == "api-optimized":
            reward = 0.7 + random.random() * 0.3  # Best performer
        else:
            reward = 0.4 + random.random() * 0.3  # Average
        
        # Update Thompson Sampling
        thompson.update(variant, reward)
        
        print(f"Round {i+1}: Selected {variant:20s} | "
              f"Sampled={sampled_value:.3f} | Reward={reward:.2f}")
    
    print()
    print("Final Statistics:")
    stats = thompson.get_statistics()
    for arm_id, arm_stats in stats["arms"].items():
        print(f"  {arm_id:20s} | Expected={arm_stats['expected_value']:.3f} | "
              f"Samples={arm_stats['n_samples']}")
    print()


def example_contextual_bandit():
    """Example: Using Contextual Bandit for state-aware selection."""
    print("=" * 60)
    print("Example 3: Contextual Bandit (LinUCB)")
    print("=" * 60)
    print()
    
    bandit = ContextualBandit(feature_dim=10)
    
    variants = ["default", "api-optimized", "database-focused"]
    
    # Different scenarios with different contexts
    scenarios = [
        {
            "request": "Create REST API endpoints",
            "files": ["src/api/users.ts"],
            "expected_best": "api-optimized"
        },
        {
            "request": "Design database schema",
            "files": ["src/models/user.py", "migrations/001.sql"],
            "expected_best": "database-focused"
        },
        {
            "request": "Build React dashboard",
            "files": ["src/components/Dashboard.tsx"],
            "expected_best": "default"
        }
    ]
    
    print("Selecting variants based on context...")
    print()
    
    for i, scenario in enumerate(scenarios):
        # Extract features from context
        features = bandit.extract_features(
            user_request=scenario["request"],
            file_paths=scenario["files"],
            agent_name="backend-architect",
            task_type="implementation"
        )
        
        # Select variant
        variant, ucb_value, metadata = bandit.select_arm(variants, features)
        
        # Simulate reward (higher if matches expected best)
        import random
        if variant == scenario["expected_best"]:
            reward = 0.8 + random.random() * 0.2  # Good match
        else:
            reward = 0.4 + random.random() * 0.2  # Not ideal
        
        # Update model
        bandit.update(variant, features, reward)
        
        print(f"Scenario {i+1}: {scenario['request'][:30]}...")
        print(f"  Selected: {variant:20s} | UCB={ucb_value:.3f} | Reward={reward:.2f}")
        print()
    
    print()


def example_transfer_learning():
    """Example: Transfer learning between task types."""
    print("=" * 60)
    print("Example 4: Transfer Learning")
    print("=" * 60)
    print()
    
    transfer = TransferLearningEngine()
    
    # Find tasks similar to api-design
    print("Finding tasks similar to 'api-design'...")
    similar_tasks = transfer.find_similar_tasks("api-design", min_similarity=0.5)
    
    for task, similarity in similar_tasks:
        print(f"  {task:30s} | Similarity: {similarity:.2f}")
    
    print()
    
    # Suggest variant for new task
    print("Suggesting variant for new task 'microservices'...")
    recommendation = transfer.suggest_variant_for_new_task(
        agent_name="backend-architect",
        new_task_type="microservices"
    )
    
    if recommendation:
        variant_id, q_value, source_task = recommendation
        print(f"  Recommended: {variant_id}")
        print(f"  Expected Q-value: {q_value:.3f}")
        print(f"  Based on: {source_task}")
    else:
        print("  No recommendation (insufficient historical data)")
    
    print()


def example_variant_mutation():
    """Example: Automated variant mutation."""
    print("=" * 60)
    print("Example 5: Variant Mutation")
    print("=" * 60)
    print()
    
    mutator = VariantMutator()
    
    agent_name = "backend-architect"
    existing_variants = mutator.agent_basis.list_variants(agent_name)
    
    if not existing_variants:
        print("No existing variants found.")
        print("Create some variants first using agent_basis.create_variant()")
        return
    
    base_variant = existing_variants[0]
    
    print(f"Base variant: {base_variant}")
    print()
    
    # Parameter mutation
    print("1. Parameter Mutation:")
    mutated_param = mutator.mutate_variant(
        agent_name, base_variant, "parameter", strength=0.2
    )
    if mutated_param:
        print(f"   Created: {mutated_param.variant_id}")
        print(f"   Temperature: {mutated_param.temperature:.2f}")
    print()
    
    # Model tier mutation
    print("2. Model Tier Mutation:")
    mutated_model = mutator.mutate_variant(
        agent_name, base_variant, "model"
    )
    if mutated_model:
        print(f"   Created: {mutated_model.variant_id}")
        print(f"   Model tier: {mutated_model.model_tier}")
    print()
    
    # Variant combination
    if len(existing_variants) >= 2:
        print("3. Variant Combination:")
        combined = mutator.combine_variants(
            agent_name, existing_variants[0], existing_variants[1]
        )
        if combined:
            print(f"   Created: {combined.variant_id}")
            print(f"   Parents: {existing_variants[0]} + {existing_variants[1]}")
    
    print()


def main():
    """Run all examples."""
    print()
    print("=" * 60)
    print("Phase 4 Advanced CRL Algorithms - Examples")
    print("=" * 60)
    print()
    
    # Run examples
    example_ucb1()
    example_thompson_sampling()
    example_contextual_bandit()
    example_transfer_learning()
    example_variant_mutation()
    
    print("=" * 60)
    print("Examples Complete")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("  - UCB1: Deterministic exploration, good for stationary environments")
    print("  - Thompson: Bayesian approach, handles non-stationary environments")
    print("  - Contextual: State-aware selection based on features")
    print("  - Transfer: Accelerates learning for new tasks")
    print("  - Mutation: Discovers novel high-performing variants")
    print()


if __name__ == "__main__":
    main()
