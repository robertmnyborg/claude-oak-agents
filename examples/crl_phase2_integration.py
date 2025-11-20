#!/usr/bin/env python3
"""
CRL Phase 2 - Integration Example

Demonstrates complete Q-Learning workflow with all Phase 2 components:
- Q-learning variant selection (ε-greedy)
- Reward calculation
- CRL coordinator orchestration
- Q-table persistence and visualization
"""

import sys
import time
import random
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.crl_coordinator import CRLCoordinator
from core.q_learning import QLearningEngine
from core.reward_calculator import RewardCalculator


def mock_agent_executor(variant_config: dict, **kwargs) -> dict:
    """
    Mock agent executor for demonstration.
    
    Simulates agent execution with varying outcomes based on variant.
    In real usage, this would be replaced with actual agent execution.
    """
    variant_id = variant_config['variant_id']
    
    # Simulate execution time
    time.sleep(0.1)
    
    # Simulate variant-specific performance
    # api-optimized performs better on API tasks
    # database-focused performs better on database tasks
    # default is balanced
    
    performance_map = {
        "api-optimized": {"success_rate": 0.90, "quality_range": (0.75, 0.95)},
        "database-focused": {"success_rate": 0.85, "quality_range": (0.70, 0.90)},
        "default": {"success_rate": 0.80, "quality_range": (0.65, 0.85)}
    }
    
    perf = performance_map.get(variant_id, performance_map["default"])
    
    # Simulate outcome
    success = random.random() < perf["success_rate"]
    quality = random.uniform(*perf["quality_range"]) if success else random.uniform(0.2, 0.5)
    error_count = 0 if success else random.randint(1, 3)
    
    return {
        "success": success,
        "quality_score": quality,
        "error_count": error_count,
        "files_modified": ["src/example.ts"],
        "files_created": [],
        "tools_used": ["Edit", "Read"],
        "tests_passed": success,
        "build_succeeded": success
    }


def demonstrate_q_learning_workflow():
    """Demonstrate complete Q-learning workflow."""
    print("=" * 80)
    print("CRL Phase 2 - Q-Learning Integration Demo")
    print("=" * 80)
    print()
    
    # Initialize coordinator
    coordinator = CRLCoordinator()
    
    # User request (API design task)
    user_request = "Create REST API endpoints for user authentication"
    file_paths = [
        "src/routes/auth.ts",
        "src/controllers/authController.ts",
        "src/middleware/jwt.ts"
    ]
    
    print("Step 1: Initial State")
    print("-" * 80)
    print("Agent: backend-architect")
    print("Available variants: default, api-optimized, database-focused")
    print("Q-values: All initialized to 0.0 (no learning yet)")
    print()
    
    # Show initial Q-values
    for variant in ["default", "api-optimized", "database-focused"]:
        q_val = coordinator.q_learning.get_q_value("backend-architect", "api-design", variant)
        visits = coordinator.q_learning.get_visit_count("backend-architect", "api-design", variant)
        print(f"  {variant:20s} Q={q_val:.3f} Visits={visits}")
    
    print()
    input("Press Enter to run 10 CRL invocations...")
    print()
    
    # Run multiple invocations to demonstrate learning
    print("Step 2: Running CRL Invocations")
    print("-" * 80)
    
    results = []
    
    for i in range(10):
        result = coordinator.execute_with_crl(
            agent_name="backend-architect",
            user_request=user_request,
            agent_executor=mock_agent_executor,
            file_paths=file_paths,
            task_complexity="medium"
        )
        
        results.append(result)
        
        print(f"Invocation {i+1:2d}: "
              f"Variant={result['variant_id']:20s} "
              f"Q={result['q_value']:+.3f} "
              f"Reward={result['reward']:+.3f} "
              f"Explore={'Yes' if result['exploration'] else 'No '} "
              f"Success={'✓' if result['success'] else '✗'}")
    
    print()
    
    # Show learning progress
    print("Step 3: Learning Progress")
    print("-" * 80)
    
    for variant in ["default", "api-optimized", "database-focused"]:
        q_val = coordinator.q_learning.get_q_value("backend-architect", "api-design", variant)
        visits = coordinator.q_learning.get_visit_count("backend-architect", "api-design", variant)
        
        if visits > 0:
            # Calculate average reward for this variant
            variant_results = [r for r in results if r['variant_id'] == variant]
            avg_reward = sum(r['reward'] for r in variant_results) / len(variant_results)
            
            print(f"{variant:20s} Q={q_val:+.3f} Visits={visits:2d} AvgReward={avg_reward:+.3f}")
        else:
            print(f"{variant:20s} Q={q_val:+.3f} Visits={visits:2d} (Not explored)")
    
    print()
    
    # Show statistics
    print("Step 4: Performance Statistics")
    print("-" * 80)
    
    successes = sum(1 for r in results if r['success'])
    avg_reward = sum(r['reward'] for r in results) / len(results)
    explorations = sum(1 for r in results if r['exploration'])
    
    print(f"Total invocations: {len(results)}")
    print(f"Successes: {successes}/{len(results)} ({successes/len(results)*100:.1f}%)")
    print(f"Average reward: {avg_reward:+.3f}")
    print(f"Explorations: {explorations}/{len(results)} ({explorations/len(results)*100:.1f}%)")
    print(f"Exploitations: {len(results)-explorations}/{len(results)} ({(len(results)-explorations)/len(results)*100:.1f}%)")
    
    print()
    
    # Show learning stats
    stats = coordinator.get_learning_stats(agent_name="backend-architect")
    
    print("Step 5: Learning Statistics")
    print("-" * 80)
    print(f"Total Q-entries: {stats['total_q_entries']}")
    print(f"Total visits: {stats['total_visits']}")
    print(f"Q-value range: [{stats['q_value_range']['min']:.3f}, {stats['q_value_range']['max']:.3f}]")
    print(f"Average Q-value: {stats['q_value_range']['avg']:.3f}")
    
    print()
    print("=" * 80)
    print("Q-Learning Integration Complete!")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("  1. View Q-table: python scripts/crl/view_q_values.py")
    print("  2. Run more invocations to see Q-values converge")
    print("  3. Try different task types to see task-specific learning")
    print()


def demonstrate_multi_task_learning():
    """Demonstrate learning across multiple task types."""
    print("=" * 80)
    print("Bonus: Multi-Task Learning Demo")
    print("=" * 80)
    print()
    
    coordinator = CRLCoordinator()
    
    # Different task types
    tasks = [
        {
            "request": "Create REST API endpoints for users",
            "files": ["src/routes/users.ts"],
            "type": "api-design"
        },
        {
            "request": "Design database schema for analytics",
            "files": ["migrations/add_analytics.sql"],
            "type": "database-schema"
        },
        {
            "request": "Optimize slow database queries",
            "files": ["src/models/user.ts"],
            "type": "performance-opt"
        }
    ]
    
    print("Running 5 invocations for each task type...")
    print()
    
    for task in tasks:
        print(f"Task Type: {task['type']}")
        print("-" * 80)
        
        for i in range(5):
            result = coordinator.execute_with_crl(
                agent_name="backend-architect",
                user_request=task["request"],
                agent_executor=mock_agent_executor,
                file_paths=task["files"],
                task_complexity="medium"
            )
            
            print(f"  Invocation {i+1}: Variant={result['variant_id']:20s} "
                  f"Q={result['q_value']:+.3f} Reward={result['reward']:+.3f}")
        
        print()
    
    # Show task-specific Q-values
    print("Task-Specific Q-Values")
    print("-" * 80)
    
    for task in tasks:
        print(f"\nTask Type: {task['type']}")
        
        for variant in ["default", "api-optimized", "database-focused"]:
            q_val = coordinator.q_learning.get_q_value(
                "backend-architect", task["type"], variant
            )
            visits = coordinator.q_learning.get_visit_count(
                "backend-architect", task["type"], variant
            )
            
            if visits > 0:
                print(f"  {variant:20s} Q={q_val:+.3f} Visits={visits}")
    
    print()
    print("=" * 80)
    print("Multi-Task Learning Complete!")
    print("=" * 80)


def main():
    """Run Phase 2 integration examples."""
    # Main Q-learning workflow
    demonstrate_q_learning_workflow()
    
    # Multi-task learning
    print()
    response = input("Run multi-task learning demo? (y/n): ")
    if response.lower() == 'y':
        print()
        demonstrate_multi_task_learning()


if __name__ == "__main__":
    main()
