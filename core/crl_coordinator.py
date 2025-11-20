#!/usr/bin/env python3
"""
CRL Coordinator - Orchestrates Continual Reinforcement Learning Workflow

Coordinates the complete CRL workflow:
1. Classify task type
2. Select variant via Q-learning
3. Execute agent with variant
4. Calculate reward
5. Update Q-table
6. Update variant metrics
7. Log telemetry
"""

import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable

from core.agent_basis import AgentBasisManager
from core.task_classifier import TaskClassifier
from core.q_learning import QLearningEngine
from core.reward_calculator import RewardCalculator
from telemetry.logger import TelemetryLogger


class CRLCoordinator:
    """
    Coordinates CRL workflow for agent execution.
    
    Integrates all CRL components:
    - TaskClassifier: Classify user requests into task types
    - QLearningEngine: Select variants via ε-greedy policy
    - AgentBasisManager: Load variants and track performance
    - RewardCalculator: Calculate reward from results
    - TelemetryLogger: Log invocations with CRL fields
    """
    
    def __init__(
        self,
        basis_manager: Optional[AgentBasisManager] = None,
        task_classifier: Optional[TaskClassifier] = None,
        q_learning: Optional[QLearningEngine] = None,
        reward_calc: Optional[RewardCalculator] = None,
        logger: Optional[TelemetryLogger] = None
    ):
        """
        Initialize CRL coordinator with components.
        
        Args:
            basis_manager: Agent basis manager (creates default if None)
            task_classifier: Task classifier (creates default if None)
            q_learning: Q-learning engine (creates default if None)
            reward_calc: Reward calculator (creates default if None)
            logger: Telemetry logger (creates default if None)
        """
        self.agent_basis = basis_manager or AgentBasisManager()
        self.task_classifier = task_classifier or TaskClassifier()
        self.q_learning = q_learning or QLearningEngine()
        self.reward_calc = reward_calc or RewardCalculator()
        self.logger = logger or TelemetryLogger()
    
    def execute_with_crl(
        self,
        agent_name: str,
        user_request: str,
        agent_executor: Callable[[str, Dict[str, Any]], Dict[str, Any]],
        file_paths: Optional[List[str]] = None,
        task_complexity: str = "medium",
        **agent_kwargs
    ) -> Dict[str, Any]:
        """
        Full CRL workflow for agent execution.
        
        Workflow:
        1. Classify task type
        2. Select variant via Q-learning (ε-greedy)
        3. Load variant configuration
        4. Execute agent with variant config
        5. Calculate reward from result
        6. Update Q-table
        7. Update variant metrics
        8. Log with CRL fields
        
        Args:
            agent_name: Agent to execute (e.g., "backend-architect")
            user_request: User's request text
            agent_executor: Function that executes agent
                           Signature: (variant_config: dict, **kwargs) -> result: dict
            file_paths: File paths involved in request (optional)
            task_complexity: Task complexity ("low", "medium", "high")
            **agent_kwargs: Additional arguments for agent executor
        
        Returns:
            Dictionary with:
                - All fields from agent_executor result
                - CRL metadata:
                    - task_type: Classified task type
                    - variant_id: Selected variant
                    - q_value: Q-value at selection
                    - exploration: Whether exploration was used
                    - reward: Calculated reward
                    - learning_enabled: Always True for CRL execution
        """
        start_time = time.time()
        
        # Step 1: Classify task type
        task_type, confidence, all_scores = self.task_classifier.classify_with_confidence(
            user_request,
            file_paths=file_paths or []
        )
        
        # Step 2: Select variant via Q-learning
        available_variants = self.agent_basis.list_variants(agent_name)
        
        if not available_variants:
            raise ValueError(
                f"No variants available for agent '{agent_name}'. "
                f"Create at least one variant in agents/basis/{agent_name}/"
            )
        
        variant_id, q_value, exploration = self.q_learning.select_variant(
            agent_name=agent_name,
            task_type=task_type,
            available_variants=available_variants
        )
        
        # Step 3: Load variant config
        variant = self.agent_basis.load_variant(agent_name, variant_id)
        
        if variant is None:
            raise ValueError(f"Failed to load variant {agent_name}:{variant_id}")
        
        variant_config = {
            "variant_id": variant.variant_id,
            "model_tier": variant.model_tier,
            "temperature": variant.temperature,
            "prompt_modifications": variant.prompt_modifications,
            "specialization": variant.specialization
        }
        
        # Step 4: Log invocation start
        invocation_id = self.logger.log_invocation(
            agent_name=agent_name,
            agent_type="development",  # Could be parameterized
            task_description=user_request,
            agent_variant=variant_id,
            task_type=task_type,
            q_value=q_value,
            exploration=exploration,
            learning_enabled=True
        )
        
        # Step 5: Execute agent
        try:
            result = agent_executor(variant_config, **agent_kwargs)
            
            # Extract outcome fields
            success = result.get("success", False)
            quality_score = result.get("quality_score")
            error_count = result.get("error_count", 0)
            
        except Exception as e:
            # Agent execution failed
            success = False
            quality_score = 0.0
            error_count = 1
            result = {
                "success": False,
                "error": str(e),
                "error_count": 1
            }
        
        # Step 6: Calculate duration and reward
        duration_seconds = time.time() - start_time
        
        reward = self.reward_calc.calculate_reward(
            success=success,
            quality_score=quality_score,
            duration_seconds=duration_seconds,
            error_count=error_count,
            task_complexity=task_complexity
        )
        
        # Step 7: Update Q-table
        self.q_learning.update_q_value(
            agent_name=agent_name,
            task_type=task_type,
            variant_id=variant_id,
            reward=reward
        )
        
        # Step 8: Update variant metrics
        self.agent_basis.update_metrics(
            agent_name=agent_name,
            variant_id=variant_id,
            success=success,
            duration=duration_seconds,
            quality_score=quality_score,
            reward=reward,
            task_type=task_type
        )
        
        # Step 9: Update invocation log
        self.logger.update_invocation(
            invocation_id=invocation_id,
            duration_seconds=duration_seconds,
            outcome_status="success" if success else "failure",
            error_message=result.get("error"),
            files_modified=result.get("files_modified"),
            files_created=result.get("files_created"),
            tools_used=result.get("tools_used"),
            tests_passed=result.get("tests_passed"),
            build_succeeded=result.get("build_succeeded"),
            reward=reward
        )
        
        # Return result with CRL metadata
        result.update({
            "invocation_id": invocation_id,
            "task_type": task_type,
            "task_type_confidence": confidence,
            "variant_id": variant_id,
            "q_value": q_value,
            "exploration": exploration,
            "reward": reward,
            "duration": duration_seconds,
            "learning_enabled": True
        })
        
        return result
    
    def get_learning_stats(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get learning statistics for agents.
        
        Args:
            agent_name: Filter by agent name (optional, None = all agents)
        
        Returns:
            Dictionary with learning statistics:
                - total_invocations: Total CRL invocations
                - agents: List of agent stats
                - q_values: Q-value statistics
        """
        # Get Q-values
        q_entries = self.q_learning.get_all_q_values(agent_name=agent_name)
        
        # Aggregate by agent
        agent_stats = {}
        
        for entry in q_entries:
            # Parse state-action key: "agent:task_type:variant"
            parts = entry.state_action.split(":")
            if len(parts) != 3:
                continue
            
            ag_name, task_type, variant = parts
            
            if ag_name not in agent_stats:
                agent_stats[ag_name] = {
                    "agent_name": ag_name,
                    "total_visits": 0,
                    "task_types": set(),
                    "variants": set(),
                    "avg_q_value": 0.0,
                    "q_entries": []
                }
            
            agent_stats[ag_name]["total_visits"] += entry.n_visits
            agent_stats[ag_name]["task_types"].add(task_type)
            agent_stats[ag_name]["variants"].add(variant)
            agent_stats[ag_name]["q_entries"].append(entry.q_value)
        
        # Calculate averages
        for stats in agent_stats.values():
            if stats["q_entries"]:
                stats["avg_q_value"] = sum(stats["q_entries"]) / len(stats["q_entries"])
            stats["task_types"] = list(stats["task_types"])
            stats["variants"] = list(stats["variants"])
            del stats["q_entries"]
        
        return {
            "total_q_entries": len(q_entries),
            "total_visits": sum(e.n_visits for e in q_entries),
            "agents": list(agent_stats.values()),
            "q_value_range": {
                "min": min((e.q_value for e in q_entries), default=0.0),
                "max": max((e.q_value for e in q_entries), default=0.0),
                "avg": sum(e.q_value for e in q_entries) / len(q_entries) if q_entries else 0.0
            }
        }


def main():
    """Example usage of CRL coordinator."""
    print("=" * 60)
    print("CRL Coordinator Demo")
    print("=" * 60)
    print()
    
    # Initialize coordinator
    coordinator = CRLCoordinator()
    
    # Example agent executor (simulated)
    def mock_agent_executor(variant_config: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Mock agent execution for demo."""
        import random
        
        print(f"Executing with variant: {variant_config['variant_id']}")
        print(f"Model tier: {variant_config['model_tier']}")
        print(f"Temperature: {variant_config['temperature']}")
        
        # Simulate execution
        time.sleep(0.1)
        
        # Simulate varying outcomes
        success = random.random() > 0.2  # 80% success rate
        quality = 0.7 + random.random() * 0.3 if success else 0.3
        
        return {
            "success": success,
            "quality_score": quality,
            "error_count": 0 if success else 1,
            "files_modified": ["src/example.ts"],
            "tools_used": ["Edit", "Read"]
        }
    
    # Example request
    user_request = "Create REST API endpoints for user management"
    file_paths = ["src/routes/users.ts", "src/controllers/userController.ts"]
    
    print("Executing CRL Workflow")
    print("-" * 60)
    print(f"Request: {user_request}")
    print(f"Files: {file_paths}")
    print()
    
    # Execute with CRL
    result = coordinator.execute_with_crl(
        agent_name="backend-architect",
        user_request=user_request,
        agent_executor=mock_agent_executor,
        file_paths=file_paths,
        task_complexity="medium"
    )
    
    print()
    print("Result:")
    print("-" * 60)
    print(f"Success: {result['success']}")
    print(f"Task Type: {result['task_type']} (confidence: {result['task_type_confidence']:.2%})")
    print(f"Variant: {result['variant_id']}")
    print(f"Q-value: {result['q_value']:.3f}")
    print(f"Exploration: {result['exploration']}")
    print(f"Reward: {result['reward']:+.3f}")
    print(f"Duration: {result['duration']:.2f}s")
    print()
    
    # Run a few more times to show learning
    print("Running Multiple Invocations...")
    print("-" * 60)
    
    for i in range(5):
        result = coordinator.execute_with_crl(
            agent_name="backend-architect",
            user_request=user_request,
            agent_executor=mock_agent_executor,
            file_paths=file_paths,
            task_complexity="medium"
        )
        
        print(f"Invocation {i+1}: Variant={result['variant_id']:<20s} "
              f"Q={result['q_value']:+.3f} Reward={result['reward']:+.3f} "
              f"Explore={result['exploration']}")
    
    print()
    
    # Show learning stats
    print("Learning Statistics")
    print("-" * 60)
    
    stats = coordinator.get_learning_stats(agent_name="backend-architect")
    
    print(f"Total Q-entries: {stats['total_q_entries']}")
    print(f"Total visits: {stats['total_visits']}")
    print(f"Q-value range: [{stats['q_value_range']['min']:.3f}, {stats['q_value_range']['max']:.3f}]")
    print(f"Average Q-value: {stats['q_value_range']['avg']:.3f}")
    
    if stats['agents']:
        agent = stats['agents'][0]
        print(f"\nAgent: {agent['agent_name']}")
        print(f"  Total visits: {agent['total_visits']}")
        print(f"  Task types: {agent['task_types']}")
        print(f"  Variants: {agent['variants']}")
        print(f"  Avg Q-value: {agent['avg_q_value']:.3f}")
    
    print()
    print("=" * 60)
    print("CRL Coordinator Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
