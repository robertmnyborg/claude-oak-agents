#!/usr/bin/env python3
"""
CRL Phase 1 - Integration Example

Demonstrates how Agent Basis, Task Classifier, and Telemetry work together
to enable the foundation for Continual Reinforcement Learning.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent_basis import AgentBasisManager, PromptModification
from core.task_classifier import TaskClassifier
from telemetry.logger import TelemetryLogger


def simulate_agent_invocation_with_crl():
    """
    Simulate a complete agent invocation with CRL tracking.
    
    This demonstrates the workflow for Phase 1:
    1. Classify the user's request
    2. Load the appropriate agent variant
    3. Log invocation with CRL fields
    4. Execute agent (simulated)
    5. Update metrics after completion
    """
    
    print("=" * 60)
    print("CRL Phase 1 - Integration Example")
    print("=" * 60)
    print()
    
    # Initialize components
    classifier = TaskClassifier()
    basis_manager = AgentBasisManager()
    logger = TelemetryLogger()
    
    # Simulate user request
    user_request = "Create REST API endpoints for user authentication"
    file_context = [
        "src/routes/auth.ts",
        "src/controllers/authController.ts",
        "src/middleware/jwt.ts"
    ]
    
    print("Step 1: Classify User Request")
    print("-" * 60)
    print(f"Request: {user_request}")
    print(f"Files: {file_context}")
    print()
    
    # Classify task type
    task_type, confidence, all_scores = classifier.classify_with_confidence(
        user_request,
        file_paths=file_context
    )
    
    print(f"Classification Result: {task_type}")
    print(f"Confidence: {confidence:.2%}")
    print(f"Top 3 Scores:")
    for tt, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:3]:
        print(f"  - {tt}: {score:.2f}")
    print()
    
    # Select best variant for this task type
    print("Step 2: Select Agent Variant")
    print("-" * 60)
    
    agent_name = "backend-architect"
    variant_id = basis_manager.get_best_variant_for_task(
        agent_name=agent_name,
        task_type=task_type,
        min_sample_count=1  # Low threshold for demo
    )
    
    if variant_id is None:
        # No variant with sufficient data, use default
        variant_id = "default"
        print(f"No variant with sufficient data for {task_type}")
        print(f"Using default variant: {variant_id}")
    else:
        print(f"Best variant for {task_type}: {variant_id}")
    
    # Load variant details
    variant = basis_manager.load_variant(agent_name, variant_id)
    print(f"Description: {variant.description}")
    print(f"Model: {variant.model_tier}, Temp: {variant.temperature}")
    print(f"Specializations: {variant.specialization}")
    print()
    
    # Log invocation start
    print("Step 3: Log Invocation with CRL Fields")
    print("-" * 60)
    
    invocation_id = logger.log_invocation(
        agent_name=agent_name,
        agent_type="development",
        task_description=user_request,
        state_features={
            "codebase": {
                "languages": ["TypeScript"],
                "frameworks": ["Express"]
            }
        },
        # CRL Phase 1 fields
        agent_variant=variant_id,
        task_type=task_type,
        q_value=None,  # Would be Q-table value in Phase 2
        exploration=False,  # Would be ε-greedy decision in Phase 2
        learning_enabled=True
    )
    
    print(f"Invocation ID: {invocation_id}")
    print("CRL Fields Logged:")
    print(f"  - agent_variant: {variant_id}")
    print(f"  - task_type: {task_type}")
    print(f"  - learning_enabled: True")
    print()
    
    # Simulate agent execution
    print("Step 4: Execute Agent (Simulated)")
    print("-" * 60)
    print("Agent would execute task here...")
    print("Creating API endpoints, controllers, middleware...")
    print("Execution complete!")
    print()
    
    # Simulate successful completion
    duration = 125.3
    outcome_status = "success"
    quality_score = 0.85  # 0.0-1.0 scale
    
    # Calculate reward (Phase 2 would do this automatically)
    # Reward = success_bonus + quality_score + speed_bonus - error_penalty
    success_bonus = 1.0 if outcome_status == "success" else -1.0
    speed_bonus = 0.5  # Simplified
    reward = success_bonus + quality_score + speed_bonus  # = 2.35
    
    print("Step 5: Update Invocation and Metrics")
    print("-" * 60)
    
    # Update invocation with completion data
    logger.update_invocation(
        invocation_id=invocation_id,
        duration_seconds=duration,
        outcome_status=outcome_status,
        files_modified=file_context,
        tools_used=["Edit", "Write", "Read"],
        tests_passed=True,
        reward=reward
    )
    
    print(f"Duration: {duration}s")
    print(f"Status: {outcome_status}")
    print(f"Quality Score: {quality_score:.2f}")
    print(f"Calculated Reward: {reward:.2f}")
    print()
    
    # Update variant metrics
    basis_manager.update_metrics(
        agent_name=agent_name,
        variant_id=variant_id,
        success=(outcome_status == "success"),
        duration=duration,
        quality_score=quality_score,
        reward=reward,
        task_type=task_type
    )
    
    print("Variant metrics updated!")
    print()
    
    # Show updated variant stats
    print("Step 6: Review Updated Performance")
    print("-" * 60)
    
    updated_variant = basis_manager.load_variant(agent_name, variant_id)
    metrics = updated_variant.performance_metrics
    
    print(f"Variant: {variant_id}")
    print(f"  Invocations: {metrics.invocation_count}")
    print(f"  Success Count: {metrics.success_count}")
    if metrics.invocation_count > 0:
        success_rate = metrics.success_count / metrics.invocation_count
        print(f"  Success Rate: {success_rate:.2%}")
    print(f"  Avg Duration: {metrics.avg_duration:.1f}s")
    print(f"  Avg Quality: {metrics.avg_quality_score:.2f}")
    print(f"  Avg Reward: {metrics.avg_reward:.2f}")
    
    if task_type in updated_variant.task_type_performance:
        tt_metrics = updated_variant.task_type_performance[task_type]
        print(f"\nTask-Specific Performance ({task_type}):")
        print(f"  Invocations: {tt_metrics['invocation_count']}")
        print(f"  Avg Reward: {tt_metrics['avg_reward']:.2f}")
    
    print()
    print("=" * 60)
    print("Integration Example Complete!")
    print("=" * 60)
    print()
    print("Summary:")
    print("✅ Task classified successfully")
    print("✅ Variant selected based on task type")
    print("✅ Invocation logged with CRL fields")
    print("✅ Metrics updated after completion")
    print("✅ Foundation ready for Phase 2 Q-learning")


def demonstrate_variant_comparison():
    """
    Demonstrate comparing multiple variants for the same task type.
    """
    
    print("\n" + "=" * 60)
    print("Bonus: Variant Performance Comparison")
    print("=" * 60)
    print()
    
    manager = AgentBasisManager()
    
    # Get all backend-architect variants
    variants = manager.list_variants("backend-architect")
    
    print(f"Backend Architect Variants: {len(variants)} total\n")
    
    for variant_id in variants:
        variant = manager.load_variant("backend-architect", variant_id)
        metrics = variant.performance_metrics
        
        print(f"{variant_id}:")
        print(f"  Description: {variant.description}")
        print(f"  Invocations: {metrics.invocation_count}")
        if metrics.invocation_count > 0:
            print(f"  Avg Reward: {metrics.avg_reward:.2f}")
            print(f"  Avg Quality: {metrics.avg_quality_score:.2f}")
        else:
            print(f"  (No performance data yet)")
        print()


if __name__ == "__main__":
    # Run integration example
    simulate_agent_invocation_with_crl()
    
    # Show variant comparison
    demonstrate_variant_comparison()
    
    print("For Phase 2: This data will feed Q-learning algorithm")
    print("to automatically select optimal variants for each task type.")
