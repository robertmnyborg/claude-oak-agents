#!/usr/bin/env python3
"""
Transfer Learning Between Task Types

Implements knowledge transfer strategies to accelerate learning for new tasks
by leveraging performance data from similar tasks.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json

from core.q_learning import QLearningEngine


class TransferLearningEngine:
    """
    Transfer learning between similar task types.
    
    Key idea: Performance on api-design can inform database-schema
    if tasks share common patterns.
    
    Transfer strategies:
    1. Parameter sharing: Use same variant for similar tasks
    2. Warm start: Initialize Q-values for new task from similar task
    3. Meta-learning: Learn which variants generalize well
    """
    
    def __init__(
        self,
        q_learning: Optional[QLearningEngine] = None,
        similarity_file: Optional[Path] = None
    ):
        """
        Initialize transfer learning engine.
        
        Args:
            q_learning: Q-learning engine (creates new if None)
            similarity_file: Path to task similarity matrix (optional)
        """
        self.q_learning = q_learning or QLearningEngine()
        
        # Task similarity matrix
        if similarity_file is None:
            project_root = Path(__file__).parent.parent
            similarity_file = project_root / "telemetry" / "crl" / "task_similarity.json"
        
        self.similarity_file = Path(similarity_file)
        self.similarity_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load or compute similarity matrix
        self.task_similarity = self._load_or_compute_similarity()
    
    def _load_or_compute_similarity(self) -> Dict[str, Dict[str, float]]:
        """
        Load task similarity matrix or compute default.
        
        Returns:
            Nested dict: {task1: {task2: similarity_score}}
        """
        if self.similarity_file.exists():
            with open(self.similarity_file, 'r') as f:
                return json.load(f)
        
        # Default similarity matrix based on domain knowledge
        similarity = {
            "api-design": {
                "api-design": 1.0,
                "database-schema": 0.7,  # APIs often query databases
                "service-architecture": 0.8,  # APIs are part of services
                "authentication": 0.6,  # APIs need auth
                "performance-optimization": 0.5,
                "ui-implementation": 0.3,  # Different domain
                "deployment": 0.4
            },
            "database-schema": {
                "api-design": 0.7,
                "database-schema": 1.0,
                "service-architecture": 0.6,
                "data-migration": 0.9,  # Highly related
                "performance-optimization": 0.7,  # Schema affects performance
                "ui-implementation": 0.2,
                "deployment": 0.3
            },
            "ui-implementation": {
                "api-design": 0.3,
                "database-schema": 0.2,
                "ui-implementation": 1.0,
                "component-design": 0.9,  # Highly related
                "accessibility": 0.7,
                "performance-optimization": 0.5,
                "deployment": 0.4
            },
            "service-architecture": {
                "api-design": 0.8,
                "database-schema": 0.6,
                "service-architecture": 1.0,
                "microservices": 0.9,
                "deployment": 0.8,
                "performance-optimization": 0.7,
                "ui-implementation": 0.3
            },
            "deployment": {
                "api-design": 0.4,
                "database-schema": 0.3,
                "ui-implementation": 0.4,
                "service-architecture": 0.8,
                "deployment": 1.0,
                "infrastructure": 0.9,
                "performance-optimization": 0.6
            }
        }
        
        # Save default similarity matrix
        self._save_similarity(similarity)
        
        return similarity
    
    def _save_similarity(self, similarity: Dict[str, Dict[str, float]]) -> None:
        """Save similarity matrix to file."""
        with open(self.similarity_file, 'w') as f:
            json.dump(similarity, f, indent=2)
    
    def get_task_similarity(self, task1: str, task2: str) -> float:
        """
        Get similarity score between two tasks.
        
        Args:
            task1: First task type
            task2: Second task type
        
        Returns:
            Similarity score (0.0-1.0)
        """
        if task1 == task2:
            return 1.0
        
        if task1 in self.task_similarity and task2 in self.task_similarity[task1]:
            return self.task_similarity[task1][task2]
        
        if task2 in self.task_similarity and task1 in self.task_similarity[task2]:
            return self.task_similarity[task2][task1]
        
        # Default low similarity for unknown task pairs
        return 0.2
    
    def find_similar_tasks(
        self,
        target_task: str,
        min_similarity: float = 0.5,
        top_k: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Find tasks similar to target task.
        
        Args:
            target_task: Task to find similar tasks for
            min_similarity: Minimum similarity threshold
            top_k: Maximum number of similar tasks to return
        
        Returns:
            List of (task_type, similarity_score) tuples
        """
        if target_task not in self.task_similarity:
            return []
        
        similar_tasks = []
        for task, similarity in self.task_similarity[target_task].items():
            if task != target_task and similarity >= min_similarity:
                similar_tasks.append((task, similarity))
        
        # Sort by similarity descending
        similar_tasks.sort(key=lambda x: x[1], reverse=True)
        
        return similar_tasks[:top_k]
    
    def transfer_knowledge(
        self,
        source_task: str,
        target_task: str,
        agent_name: str,
        transfer_ratio: float = 0.5
    ) -> Dict[str, float]:
        """
        Transfer Q-values from source to target task.
        
        Q_target = (1 - ratio) * Q_target + ratio * Q_source * similarity
        
        Args:
            source_task: Task to transfer from
            target_task: Task to transfer to
            agent_name: Agent name
            transfer_ratio: How much to transfer (0.0-1.0)
        
        Returns:
            Dictionary of transferred Q-values {variant_id: new_q_value}
        """
        # Get similarity
        similarity = self.get_task_similarity(source_task, target_task)
        
        if similarity < 0.3:
            # Tasks too dissimilar for transfer
            return {}
        
        # Get all Q-values for source task
        source_entries = self.q_learning.get_all_q_values(
            agent_name=agent_name,
            task_type=source_task
        )
        
        transferred = {}
        
        for entry in source_entries:
            # Parse variant from state_action key
            parts = entry.state_action.split(":")
            if len(parts) != 3:
                continue
            
            variant_id = parts[2]
            source_q = entry.q_value
            
            # Get current Q-value for target task
            target_q = self.q_learning.get_q_value(
                agent_name, target_task, variant_id
            )
            
            # Transfer: weighted combination
            new_q = (1 - transfer_ratio) * target_q + \
                    transfer_ratio * source_q * similarity
            
            # Update Q-table with transferred value
            # Use update with synthetic reward to set Q-value
            current_q = target_q
            learning_rate = self.q_learning.alpha
            
            # Solve for reward: new_q = current_q + alpha * (reward - current_q)
            # reward = (new_q - current_q) / alpha + current_q
            synthetic_reward = (new_q - current_q) / learning_rate + current_q
            
            self.q_learning.update_q_value(
                agent_name, target_task, variant_id, synthetic_reward
            )
            
            transferred[variant_id] = new_q
        
        return transferred
    
    def suggest_variant_for_new_task(
        self,
        agent_name: str,
        new_task_type: str,
        min_visits: int = 5
    ) -> Optional[Tuple[str, float, str]]:
        """
        Suggest initial variant for new task type based on transfer.
        
        Finds most similar task type and recommends its best variant.
        
        Args:
            agent_name: Agent name
            new_task_type: New task type with no history
            min_visits: Minimum visits required for recommendation
        
        Returns:
            Tuple of (variant_id, expected_q_value, source_task) or None
        """
        # Find similar tasks
        similar_tasks = self.find_similar_tasks(new_task_type, min_similarity=0.5)
        
        if not similar_tasks:
            return None
        
        best_recommendation = None
        best_score = float('-inf')
        
        for similar_task, similarity in similar_tasks:
            # Get Q-values for this similar task
            entries = self.q_learning.get_all_q_values(
                agent_name=agent_name,
                task_type=similar_task
            )
            
            for entry in entries:
                # Parse variant from state_action
                parts = entry.state_action.split(":")
                if len(parts) != 3:
                    continue
                
                variant_id = parts[2]
                
                # Skip if insufficient visits
                if entry.n_visits < min_visits:
                    continue
                
                # Score = Q-value * similarity
                score = entry.q_value * similarity
                
                if score > best_score:
                    best_score = score
                    best_recommendation = (variant_id, entry.q_value, similar_task)
        
        return best_recommendation
    
    def warm_start_new_task(
        self,
        agent_name: str,
        new_task_type: str,
        transfer_ratio: float = 0.3
    ) -> Dict[str, float]:
        """
        Warm start a new task with transferred knowledge.
        
        Transfers from all similar tasks, weighted by similarity.
        
        Args:
            agent_name: Agent name
            new_task_type: New task type to warm start
            transfer_ratio: Transfer strength (0.0-1.0)
        
        Returns:
            Dictionary of initialized Q-values {variant_id: q_value}
        """
        similar_tasks = self.find_similar_tasks(new_task_type, min_similarity=0.4)
        
        if not similar_tasks:
            return {}
        
        # Transfer from each similar task
        all_transferred = {}
        
        for similar_task, similarity in similar_tasks:
            # Weight transfer by similarity
            weighted_ratio = transfer_ratio * similarity
            
            transferred = self.transfer_knowledge(
                source_task=similar_task,
                target_task=new_task_type,
                agent_name=agent_name,
                transfer_ratio=weighted_ratio
            )
            
            # Merge transferred values (average if variant appears multiple times)
            for variant_id, q_value in transferred.items():
                if variant_id in all_transferred:
                    # Average with existing
                    all_transferred[variant_id] = (
                        all_transferred[variant_id] + q_value
                    ) / 2
                else:
                    all_transferred[variant_id] = q_value
        
        return all_transferred


def main():
    """Example usage of transfer learning."""
    print("=" * 60)
    print("Transfer Learning Demo")
    print("=" * 60)
    print()
    
    # Initialize transfer learning engine
    transfer = TransferLearningEngine()
    
    # Example 1: Find similar tasks
    print("Finding tasks similar to 'api-design'...")
    similar = transfer.find_similar_tasks("api-design", min_similarity=0.5)
    
    for task, similarity in similar:
        print(f"  {task:30s} | Similarity: {similarity:.2f}")
    
    print()
    
    # Example 2: Suggest variant for new task
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
        print("  No recommendation available (insufficient data)")
    
    print()
    
    # Example 3: Warm start new task
    print("Warm starting 'microservices' from similar tasks...")
    initialized = transfer.warm_start_new_task(
        agent_name="backend-architect",
        new_task_type="microservices",
        transfer_ratio=0.3
    )
    
    if initialized:
        print(f"  Initialized {len(initialized)} variants:")
        for variant_id, q_value in initialized.items():
            print(f"    {variant_id:20s} | Q={q_value:.3f}")
    else:
        print("  No initialization performed (no similar tasks with data)")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
