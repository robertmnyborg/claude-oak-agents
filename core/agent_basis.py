#!/usr/bin/env python3
"""
Agent Basis Management System for Continual Reinforcement Learning

This module manages agent variants - different configurations and specializations
of base agents that can be selected based on task type and historical performance.
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field


@dataclass
class PerformanceMetrics:
    """Performance metrics for an agent variant."""
    invocation_count: int = 0
    success_count: int = 0
    avg_duration: float = 0.0
    avg_quality_score: float = 0.0
    avg_reward: float = 0.0
    last_updated: Optional[str] = None


@dataclass
class PromptModification:
    """A modification to the agent's base prompt."""
    section: str  # Which section of the prompt to modify
    operation: str  # "append", "prepend", "replace"
    content: str  # The modification content


@dataclass
class AgentVariant:
    """
    Single agent configuration variant.
    
    Represents a specialized version of a base agent with specific
    prompt modifications, model configuration, and performance history.
    """
    variant_id: str
    agent_name: str
    description: str
    specialization: List[str]
    model_tier: str
    temperature: float
    prompt_modifications: List[PromptModification]
    performance_metrics: PerformanceMetrics
    created_at: str
    task_type_performance: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert variant to dictionary for YAML serialization."""
        data = {
            "variant_id": self.variant_id,
            "agent_name": self.agent_name,
            "description": self.description,
            "specialization": self.specialization,
            "model_tier": self.model_tier,
            "temperature": self.temperature,
            "prompt_modifications": [
                {
                    "section": pm.section,
                    "operation": pm.operation,
                    "content": pm.content
                }
                for pm in self.prompt_modifications
            ],
            "performance_metrics": {
                "invocation_count": self.performance_metrics.invocation_count,
                "success_count": self.performance_metrics.success_count,
                "avg_duration": self.performance_metrics.avg_duration,
                "avg_quality_score": self.performance_metrics.avg_quality_score,
                "avg_reward": self.performance_metrics.avg_reward,
                "last_updated": self.performance_metrics.last_updated
            },
            "created_at": self.created_at,
            "task_type_performance": self.task_type_performance
        }
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentVariant':
        """Create variant from dictionary (YAML deserialization)."""
        prompt_mods = [
            PromptModification(**pm) for pm in data.get("prompt_modifications", [])
        ]
        
        perf_data = data.get("performance_metrics", {})
        performance = PerformanceMetrics(**perf_data)
        
        return cls(
            variant_id=data["variant_id"],
            agent_name=data["agent_name"],
            description=data["description"],
            specialization=data.get("specialization", []),
            model_tier=data.get("model_tier", "balanced"),
            temperature=data.get("temperature", 0.7),
            prompt_modifications=prompt_mods,
            performance_metrics=performance,
            created_at=data.get("created_at", datetime.utcnow().isoformat() + "Z"),
            task_type_performance=data.get("task_type_performance", {})
        )


class AgentBasisManager:
    """
    Manages agent variants and their performance data.
    
    Responsible for loading, saving, and updating agent variant configurations
    and tracking their performance metrics for Q-learning.
    """
    
    def __init__(self, basis_dir: Optional[Path] = None):
        """
        Initialize agent basis manager.
        
        Args:
            basis_dir: Directory containing agent variant files.
                      Defaults to ./agents/basis relative to project root.
        """
        if basis_dir is None:
            # Find project root (contains agents directory)
            current = Path(__file__).parent
            project_root = current.parent
            basis_dir = project_root / "agents" / "basis"
        
        self.basis_dir = Path(basis_dir)
        self.basis_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache of loaded variants
        self._variant_cache: Dict[str, AgentVariant] = {}
    
    def load_variant(self, agent_name: str, variant_id: str) -> Optional[AgentVariant]:
        """
        Load a specific agent variant.
        
        Args:
            agent_name: Base agent name (e.g., "backend-architect")
            variant_id: Variant identifier (e.g., "api-optimized")
        
        Returns:
            AgentVariant if found, None otherwise
        """
        cache_key = f"{agent_name}:{variant_id}"
        
        # Check cache first
        if cache_key in self._variant_cache:
            return self._variant_cache[cache_key]
        
        # Load from file
        variant_file = self.basis_dir / agent_name / f"{variant_id}.yaml"
        
        if not variant_file.exists():
            return None
        
        with open(variant_file, 'r') as f:
            data = yaml.safe_load(f)
        
        variant = AgentVariant.from_dict(data)
        self._variant_cache[cache_key] = variant
        
        return variant
    
    def list_variants(self, agent_name: str) -> List[str]:
        """
        List all variant IDs for a given agent.
        
        Args:
            agent_name: Base agent name
        
        Returns:
            List of variant IDs
        """
        agent_dir = self.basis_dir / agent_name
        
        if not agent_dir.exists():
            return []
        
        variants = []
        for variant_file in agent_dir.glob("*.yaml"):
            variant_id = variant_file.stem
            variants.append(variant_id)
        
        return sorted(variants)
    
    def save_variant(self, variant: AgentVariant) -> None:
        """
        Save an agent variant to disk.
        
        Args:
            variant: AgentVariant to save
        """
        agent_dir = self.basis_dir / variant.agent_name
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        variant_file = agent_dir / f"{variant.variant_id}.yaml"
        
        with open(variant_file, 'w') as f:
            yaml.dump(variant.to_dict(), f, default_flow_style=False, sort_keys=False)
        
        # Update cache
        cache_key = f"{variant.agent_name}:{variant.variant_id}"
        self._variant_cache[cache_key] = variant
    
    def update_metrics(
        self,
        agent_name: str,
        variant_id: str,
        success: bool,
        duration: float,
        quality_score: Optional[float] = None,
        reward: Optional[float] = None,
        task_type: Optional[str] = None
    ) -> None:
        """
        Update performance metrics for a variant.
        
        Uses incremental averaging to update metrics without storing all history.
        
        Args:
            agent_name: Base agent name
            variant_id: Variant identifier
            success: Whether invocation was successful
            duration: Duration in seconds
            quality_score: Quality rating (0.0-1.0, optional)
            reward: Calculated reward signal (optional)
            task_type: Task type for task-specific metrics (optional)
        """
        variant = self.load_variant(agent_name, variant_id)
        
        if variant is None:
            raise ValueError(f"Variant {agent_name}:{variant_id} not found")
        
        metrics = variant.performance_metrics
        
        # Update overall metrics using incremental averaging
        n = metrics.invocation_count
        
        # Invocation count
        metrics.invocation_count += 1
        
        # Success count
        if success:
            metrics.success_count += 1
        
        # Average duration (incremental average)
        metrics.avg_duration = (metrics.avg_duration * n + duration) / (n + 1)
        
        # Average quality score (if provided)
        if quality_score is not None:
            if metrics.avg_quality_score == 0.0 and n == 0:
                metrics.avg_quality_score = quality_score
            else:
                metrics.avg_quality_score = (
                    metrics.avg_quality_score * n + quality_score
                ) / (n + 1)
        
        # Average reward (if provided)
        if reward is not None:
            if metrics.avg_reward == 0.0 and n == 0:
                metrics.avg_reward = reward
            else:
                metrics.avg_reward = (metrics.avg_reward * n + reward) / (n + 1)
        
        # Update timestamp
        metrics.last_updated = datetime.utcnow().isoformat() + "Z"
        
        # Update task-type-specific metrics if task_type provided
        if task_type is not None:
            if task_type not in variant.task_type_performance:
                variant.task_type_performance[task_type] = {
                    "invocation_count": 0,
                    "success_count": 0,
                    "avg_duration": 0.0,
                    "avg_quality_score": 0.0,
                    "avg_reward": 0.0
                }
            
            tt_metrics = variant.task_type_performance[task_type]
            tt_n = tt_metrics["invocation_count"]
            
            # Update task-type metrics
            tt_metrics["invocation_count"] += 1
            if success:
                tt_metrics["success_count"] += 1
            
            tt_metrics["avg_duration"] = (
                tt_metrics["avg_duration"] * tt_n + duration
            ) / (tt_n + 1)
            
            if quality_score is not None:
                if tt_metrics["avg_quality_score"] == 0.0 and tt_n == 0:
                    tt_metrics["avg_quality_score"] = quality_score
                else:
                    tt_metrics["avg_quality_score"] = (
                        tt_metrics["avg_quality_score"] * tt_n + quality_score
                    ) / (tt_n + 1)
            
            if reward is not None:
                if tt_metrics["avg_reward"] == 0.0 and tt_n == 0:
                    tt_metrics["avg_reward"] = reward
                else:
                    tt_metrics["avg_reward"] = (
                        tt_metrics["avg_reward"] * tt_n + reward
                    ) / (tt_n + 1)
        
        # Save updated variant
        self.save_variant(variant)
    
    def create_variant(
        self,
        agent_name: str,
        variant_id: str,
        description: str,
        specialization: List[str],
        model_tier: str = "balanced",
        temperature: float = 0.7,
        prompt_modifications: Optional[List[PromptModification]] = None
    ) -> AgentVariant:
        """
        Create a new agent variant.
        
        Args:
            agent_name: Base agent name
            variant_id: Unique variant identifier (e.g., "api-optimized")
            description: Human-readable description
            specialization: List of specialization tags
            model_tier: "fast", "balanced", or "premium"
            temperature: Model temperature (0.0-1.0)
            prompt_modifications: List of prompt modifications
        
        Returns:
            Created AgentVariant
        """
        # Check if variant already exists
        existing = self.load_variant(agent_name, variant_id)
        if existing is not None:
            raise ValueError(f"Variant {agent_name}:{variant_id} already exists")
        
        variant = AgentVariant(
            variant_id=variant_id,
            agent_name=agent_name,
            description=description,
            specialization=specialization,
            model_tier=model_tier,
            temperature=temperature,
            prompt_modifications=prompt_modifications or [],
            performance_metrics=PerformanceMetrics(),
            created_at=datetime.utcnow().isoformat() + "Z"
        )
        
        self.save_variant(variant)
        
        return variant
    
    def get_best_variant_for_task(
        self,
        agent_name: str,
        task_type: str,
        min_sample_count: int = 5
    ) -> Optional[str]:
        """
        Get the best-performing variant for a specific task type.
        
        Uses average reward as the selection criterion. Requires minimum
        sample count to avoid selecting undertested variants.
        
        Args:
            agent_name: Base agent name
            task_type: Task type to optimize for
            min_sample_count: Minimum invocations required for consideration
        
        Returns:
            variant_id of best variant, or None if no suitable variant found
        """
        variants = self.list_variants(agent_name)
        
        if not variants:
            return None
        
        best_variant = None
        best_reward = float('-inf')
        
        for variant_id in variants:
            variant = self.load_variant(agent_name, variant_id)
            
            if variant is None:
                continue
            
            # Check if variant has task-specific performance data
            if task_type in variant.task_type_performance:
                tt_perf = variant.task_type_performance[task_type]
                
                # Skip if insufficient samples
                if tt_perf["invocation_count"] < min_sample_count:
                    continue
                
                reward = tt_perf.get("avg_reward", 0.0)
                
                if reward > best_reward:
                    best_reward = reward
                    best_variant = variant_id
        
        return best_variant


def main():
    """Example usage of agent basis manager."""
    manager = AgentBasisManager()

    # List existing variants
    variants = manager.list_variants("backend-architect")
    print(f"Existing backend-architect variants: {variants}")

    # Load an existing variant
    if "api-optimized" in variants:
        variant = manager.load_variant("backend-architect", "api-optimized")
        print(f"\nLoaded variant: {variant.variant_id}")
        print(f"  Description: {variant.description}")
        print(f"  Specialization: {variant.specialization}")
        print(f"  Metrics: {variant.performance_metrics.invocation_count} invocations")

    # Create a new example variant
    try:
        new_variant = manager.create_variant(
            agent_name="backend-architect",
            variant_id="example-variant",
            description="Example variant for testing",
            specialization=["example"],
            model_tier="balanced",
            temperature=0.7,
            prompt_modifications=[
                PromptModification(
                    section="Example Section",
                    operation="append",
                    content="Example content for demonstration"
                )
            ]
        )
        print(f"\nCreated new variant: {new_variant.variant_id}")

        # Simulate some invocations
        for i in range(3):
            manager.update_metrics(
                agent_name="backend-architect",
                variant_id="example-variant",
                success=True,
                duration=100.0 + i * 10,
                quality_score=0.8,
                reward=2.0,
                task_type="example-task"
            )

        print(f"Updated metrics for {new_variant.variant_id}")

        # Reload to show updated metrics
        updated = manager.load_variant("backend-architect", "example-variant")
        print(f"  Invocations: {updated.performance_metrics.invocation_count}")
        print(f"  Avg duration: {updated.performance_metrics.avg_duration:.1f}s")

    except ValueError as e:
        print(f"\nNote: {e}")

    # List all variants again
    all_variants = manager.list_variants("backend-architect")
    print(f"\nAll backend-architect variants: {all_variants}")


if __name__ == "__main__":
    main()
