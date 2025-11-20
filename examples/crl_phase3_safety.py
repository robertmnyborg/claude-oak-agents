#!/usr/bin/env python3
"""
Example: CRL Phase 3 Safety Mechanisms

Demonstrates safety monitor, rollback manager, and variant proposer in action.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.safety_monitor import SafetyMonitor
from core.rollback_manager import RollbackManager
from core.variant_proposer import VariantProposer
from core.q_learning import QLearningEngine
from core.agent_basis import AgentBasisManager
from core.reward_calculator import RewardCalculator


def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def example_1_safety_monitor():
    """Example 1: Safety monitor decision making."""
    print_section("EXAMPLE 1: Safety Monitor - Auto-Apply vs Human Approval")
    
    monitor = SafetyMonitor()
    
    # Scenario 1: High confidence variant (auto-apply)
    print("Scenario 1: High Confidence Variant")
    print("-" * 80)
    decision, reasoning = monitor.should_auto_apply_variant(
        agent_name="backend-architect",
        task_type="api-design",
        variant_id="api-optimized",
        q_value=0.95,
        n_visits=25
    )
    print(f"Decision: {decision.upper()}")
    print(f"Reasoning: {reasoning}")
    print()
    
    # Scenario 2: Medium confidence variant (human approval)
    print("Scenario 2: Medium Confidence Variant")
    print("-" * 80)
    decision, reasoning = monitor.should_auto_apply_variant(
        agent_name="backend-architect",
        task_type="database-schema",
        variant_id="database-focused",
        q_value=0.78,
        n_visits=10
    )
    print(f"Decision: {decision.upper()}")
    print(f"Reasoning: {reasoning}")
    print()
    
    # Scenario 3: Low confidence variant (no action)
    print("Scenario 3: Low Confidence Variant")
    print("-" * 80)
    decision, reasoning = monitor.should_auto_apply_variant(
        agent_name="backend-architect",
        task_type="refactoring",
        variant_id="experimental",
        q_value=0.62,
        n_visits=4
    )
    print(f"Decision: {decision.upper()}")
    print(f"Reasoning: {reasoning}")


def example_2_performance_degradation():
    """Example 2: Performance degradation detection."""
    print_section("EXAMPLE 2: Performance Degradation Detection")
    
    monitor = SafetyMonitor()
    
    print("Checking variant performance for degradation...")
    print("-" * 80)
    
    # This will return no degradation for non-existent variants
    # In real usage, this would analyze actual telemetry data
    degraded, metrics = monitor.check_performance_degradation(
        agent_name="backend-architect",
        task_type="api-design",
        variant_id="api-optimized",
        lookback_window=20
    )
    
    if degraded:
        print("⚠️  DEGRADATION DETECTED!")
        print(f"   Success Rate: {metrics['baseline_success_rate']:.1%} → "
              f"{metrics['recent_success_rate']:.1%}")
        print(f"   Reward: {metrics['baseline_avg_reward']:.2f} → "
              f"{metrics['recent_avg_reward']:.2f}")
        print(f"   Sample Size: {metrics['sample_size']} invocations")
    else:
        print("✓ No degradation detected")
        if "error" in metrics:
            print(f"  Note: {metrics['error']}")


def example_3_rollback_workflow():
    """Example 3: Rollback workflow."""
    print_section("EXAMPLE 3: Rollback Workflow")
    
    rollback_mgr = RollbackManager()
    
    print("Simulating performance degradation and rollback...")
    print("-" * 80)
    
    # Execute a test rollback
    rollback_info = rollback_mgr._execute_rollback(
        agent_name="backend-architect",
        task_type="api-design",
        from_variant="api-optimized-v2",
        to_variant="api-optimized",
        reason="Success rate dropped from 92% to 78% (15% drop)",
        degradation_metrics={
            "baseline_success_rate": 0.92,
            "recent_success_rate": 0.78,
            "success_drop_pct": 0.152,
            "sample_size": 25
        }
    )
    
    print(f"Rollback Executed: {rollback_info['rollback_id']}")
    print(f"From Variant: {rollback_info['from_variant']}")
    print(f"To Variant: {rollback_info['to_variant']}")
    print(f"Reason: {rollback_info['reason']}")
    print()
    
    # Show rollback history
    print("Rollback History (Last 5):")
    print("-" * 80)
    history = rollback_mgr.get_rollback_history(limit=5)
    
    for i, event in enumerate(history, 1):
        print(f"{i}. {event['rollback_id']}")
        print(f"   {event['agent_name']} / {event['task_type']}")
        print(f"   {event['from_variant']} → {event['to_variant']}")


def example_4_variant_proposals():
    """Example 4: Variant proposal generation."""
    print_section("EXAMPLE 4: Variant Proposal Generation")
    
    proposer = VariantProposer()
    
    print("Analyzing agent performance and generating proposals...")
    print("-" * 80)
    
    # Create a test proposal
    proposal = proposer._create_proposal(
        agent_name="backend-architect",
        task_type="security-audit",
        proposal_type="create_specialized_variant",
        reason="Security-audit tasks show 15% lower performance with default variant. "
               "Suggest creating security-focused variant.",
        supporting_data={
            "n_invocations": 67,
            "avg_q_default": 0.65,
            "potential_improvement": 0.15,
            "variance": 0.12
        }
    )
    
    print(f"Proposal Generated: {proposal['proposal_id']}")
    print(f"Agent: {proposal['agent_name']}")
    print(f"Task Type: {proposal['task_type']}")
    print(f"Type: {proposal['proposal_type']}")
    print(f"Confidence: {proposal['confidence']:.0%}")
    print()
    print(f"Reasoning: {proposal['reasoning']}")
    print()
    
    print("Recommended Modifications:")
    for i, mod in enumerate(proposal['recommended_modifications'], 1):
        print(f"\n{i}. ", end="")
        if 'section' in mod:
            print(f"{mod['operation'].title()} to {mod['section']}")
            print(f"   Content: {mod['content'][:100]}...")
        elif 'parameter' in mod:
            print(f"Set {mod['parameter']} = {mod['value']}")
            if 'reason' in mod:
                print(f"   Reason: {mod['reason']}")


def example_5_complete_safety_workflow():
    """Example 5: Complete safety workflow integration."""
    print_section("EXAMPLE 5: Complete Safety Workflow")
    
    print("This example demonstrates the complete CRL safety workflow:")
    print("1. Learn from invocations (Q-learning)")
    print("2. Monitor variant performance")
    print("3. Detect degradation")
    print("4. Trigger rollback if needed")
    print("5. Generate proposals for improvements")
    print()
    
    # Initialize components
    q_learning = QLearningEngine()
    safety_monitor = SafetyMonitor()
    rollback_mgr = RollbackManager()
    proposer = VariantProposer()
    
    # Step 1: Simulate learning
    print("Step 1: Simulating Q-learning updates...")
    print("-" * 80)
    
    agent_name = "backend-architect"
    task_type = "api-design"
    variants = ["default", "api-optimized", "experimental"]
    
    # Simulate some Q-value updates
    for variant in variants:
        # Simulate different performance levels
        if variant == "api-optimized":
            q_value = 0.92
        elif variant == "default":
            q_value = 0.75
        else:
            q_value = 0.60
        
        q_learning.update_q_value(agent_name, task_type, variant, q_value)
        visits = q_learning.get_visit_count(agent_name, task_type, variant)
        
        print(f"  {variant}: Q={q_value:.2f}, visits={visits}")
    
    print()
    
    # Step 2: Check which variant should be applied
    print("Step 2: Safety monitor decision...")
    print("-" * 80)
    
    for variant in variants:
        q_val = q_learning.get_q_value(agent_name, task_type, variant)
        n_visits = q_learning.get_visit_count(agent_name, task_type, variant)
        
        decision, reasoning = safety_monitor.should_auto_apply_variant(
            agent_name, task_type, variant, q_val, n_visits
        )
        
        print(f"\n{variant}:")
        print(f"  Q-value: {q_val:.3f}, Visits: {n_visits}")
        print(f"  Decision: {decision.upper()}")
    
    print()
    
    # Step 3: Show current state
    print("Step 3: Current system state...")
    print("-" * 80)
    
    print(f"Best variant: api-optimized (Q=0.92, ready for auto-apply)")
    print(f"Default variant: default (Q=0.75)")
    print(f"Recommendation: Promote api-optimized to default")
    
    print()
    print("Safety mechanisms ensure:")
    print("  ✓ High confidence before auto-applying changes")
    print("  ✓ Continuous monitoring for degradation")
    print("  ✓ Automatic rollback on performance drops")
    print("  ✓ Proactive proposals for improvements")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("CRL PHASE 3: SAFETY MECHANISMS & AUTOMATION")
    print("=" * 80)
    print()
    print("This example demonstrates:")
    print("  - Safety monitor (auto-apply vs human approval)")
    print("  - Performance degradation detection")
    print("  - Automatic rollback on degradation")
    print("  - Variant proposal generation")
    print("  - Complete safety workflow")
    
    try:
        example_1_safety_monitor()
        example_2_performance_degradation()
        example_3_rollback_workflow()
        example_4_variant_proposals()
        example_5_complete_safety_workflow()
        
        print_section("EXAMPLES COMPLETE")
        print("Next Steps:")
        print("  1. Run safety dashboard: python scripts/crl/safety_dashboard.py")
        print("  2. Run tests: python tests/crl/test_safety.py")
        print("  3. Check telemetry: ls -la telemetry/crl/")
        print()
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
