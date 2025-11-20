#!/usr/bin/env python3
"""
Q-Learning Engine for Continual Reinforcement Learning

Implements TD(0) Q-learning with ε-greedy exploration policy for agent variant selection.
Uses constant step-size (α) for continual learning and persistent Q-table storage.
"""

import json
import random
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class QEntry:
    """Single Q-table entry for a state-action pair."""
    state_action: str  # Format: "agent:task_type:variant"
    q_value: float
    n_visits: int
    last_updated: str
    convergence_score: float = 0.0  # Change in Q-value on last update
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "state_action": self.state_action,
            "q_value": self.q_value,
            "n_visits": self.n_visits,
            "last_updated": self.last_updated,
            "convergence_score": self.convergence_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'QEntry':
        """Create from dictionary (JSON deserialization)."""
        return cls(
            state_action=data["state_action"],
            q_value=data["q_value"],
            n_visits=data["n_visits"],
            last_updated=data["last_updated"],
            convergence_score=data.get("convergence_score", 0.0)
        )


class QLearningEngine:
    """
    Q-Learning engine for agent variant selection.
    
    Uses ε-greedy policy with constant step-size for continual learning.
    Q-values stored per (agent_name, task_type, variant_id) tuple.
    
    TD(0) Update Rule:
        Q(s,a) ← Q(s,a) + α[R - Q(s,a)]
    
    Where:
        - s = (agent_name, task_type)
        - a = variant_id
        - α = learning_rate (constant, default 0.1)
        - R = reward signal from invocation
    """
    
    def __init__(
        self,
        learning_rate: float = 0.1,  # α - constant for continual learning
        discount_factor: float = 0.9,  # γ - future reward discount (not used in TD(0))
        exploration_rate: float = 0.1,  # ε - exploration probability
        qtable_file: Optional[Path] = None
    ):
        """
        Initialize Q-learning engine with parameters from architecture doc.
        
        Args:
            learning_rate: Constant step-size α for Q-value updates (default: 0.1)
            discount_factor: Future reward discount γ (not used in TD(0), kept for compatibility)
            exploration_rate: ε-greedy exploration probability (default: 0.1 = 10%)
            qtable_file: Path to Q-table JSONL file (defaults to telemetry/crl/q_table.jsonl)
        """
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        
        # Default Q-table location
        if qtable_file is None:
            project_root = Path(__file__).parent.parent
            qtable_file = project_root / "telemetry" / "crl" / "q_table.jsonl"
        
        self.qtable_file = Path(qtable_file)
        self.qtable_file.parent.mkdir(parents=True, exist_ok=True)
        
        # In-memory Q-table cache: {state_action_key: QEntry}
        self._qtable: Dict[str, QEntry] = {}
        
        # Thread lock for Q-table updates
        self._lock = threading.Lock()
        
        # Load existing Q-table
        self._load_qtable()
    
    def _state_action_key(self, agent_name: str, task_type: str, variant_id: str) -> str:
        """
        Create state-action key for Q-table lookup.
        
        Format: "agent_name:task_type:variant_id"
        
        Args:
            agent_name: Agent name (e.g., "backend-architect")
            task_type: Task type (e.g., "api-design")
            variant_id: Variant identifier (e.g., "api-optimized")
        
        Returns:
            Composite key string
        """
        return f"{agent_name}:{task_type}:{variant_id}"
    
    def select_variant(
        self,
        agent_name: str,
        task_type: str,
        available_variants: List[str]
    ) -> Tuple[str, float, bool]:
        """
        Select agent variant using ε-greedy policy.
        
        With probability ε: random exploration
        With probability 1-ε: exploit best Q-value
        
        Args:
            agent_name: Agent name
            task_type: Classified task type
            available_variants: List of available variant IDs
        
        Returns:
            Tuple of (variant_id, q_value, is_exploration)
            - variant_id: Selected variant
            - q_value: Q-value for selected variant
            - is_exploration: True if random exploration, False if exploitation
        """
        if not available_variants:
            raise ValueError(f"No variants available for agent {agent_name}")
        
        # Get Q-values for all available variants
        q_values = {}
        for variant_id in available_variants:
            q_values[variant_id] = self.get_q_value(agent_name, task_type, variant_id)
        
        # ε-greedy selection
        variant_id, is_exploration = self._epsilon_greedy_selection(q_values)
        q_value = q_values[variant_id]
        
        return (variant_id, q_value, is_exploration)
    
    def _epsilon_greedy_selection(self, q_values: Dict[str, float]) -> Tuple[str, bool]:
        """
        ε-greedy selection: 
        - With probability ε: random exploration
        - With probability 1-ε: exploit best Q-value
        
        Args:
            q_values: Dictionary of variant_id -> q_value
        
        Returns:
            Tuple of (selected_variant_id, is_exploration)
        """
        if random.random() < self.epsilon:
            # Exploration: random variant
            variant_id = random.choice(list(q_values.keys()))
            return (variant_id, True)
        else:
            # Exploitation: best Q-value
            best_variant = max(q_values.items(), key=lambda x: x[1])[0]
            return (best_variant, False)
    
    def update_q_value(
        self,
        agent_name: str,
        task_type: str,
        variant_id: str,
        reward: float
    ) -> None:
        """
        Update Q-value using TD(0) update rule.
        
        TD(0) Update: Q(s,a) ← Q(s,a) + α[R - Q(s,a)]
        
        Args:
            agent_name: Agent name
            task_type: Task type
            variant_id: Variant identifier
            reward: Reward signal from invocation result
        """
        with self._lock:
            key = self._state_action_key(agent_name, task_type, variant_id)
            
            # Get current Q-value
            if key in self._qtable:
                entry = self._qtable[key]
                old_q = entry.q_value
            else:
                # Initialize new entry with Q=0
                old_q = 0.0
                entry = QEntry(
                    state_action=key,
                    q_value=0.0,
                    n_visits=0,
                    last_updated=datetime.utcnow().isoformat() + "Z"
                )
                self._qtable[key] = entry
            
            # TD(0) update: Q(s,a) ← Q(s,a) + α[R - Q(s,a)]
            new_q = old_q + self.alpha * (reward - old_q)
            
            # Update entry
            entry.q_value = new_q
            entry.n_visits += 1
            entry.last_updated = datetime.utcnow().isoformat() + "Z"
            entry.convergence_score = abs(new_q - old_q)  # Track convergence
            
            # Persist to disk
            self._save_qtable()
    
    def get_q_value(
        self,
        agent_name: str,
        task_type: str,
        variant_id: str
    ) -> float:
        """
        Get current Q-value for state-action pair.
        
        Returns 0.0 if never visited (optimistic initialization).
        
        Args:
            agent_name: Agent name
            task_type: Task type
            variant_id: Variant identifier
        
        Returns:
            Current Q-value (default: 0.0)
        """
        key = self._state_action_key(agent_name, task_type, variant_id)
        
        with self._lock:
            if key in self._qtable:
                return self._qtable[key].q_value
            else:
                return 0.0  # Optimistic initialization
    
    def get_visit_count(
        self,
        agent_name: str,
        task_type: str,
        variant_id: str
    ) -> int:
        """
        Get number of times this state-action pair has been visited.
        
        Args:
            agent_name: Agent name
            task_type: Task type
            variant_id: Variant identifier
        
        Returns:
            Visit count (0 if never visited)
        """
        key = self._state_action_key(agent_name, task_type, variant_id)
        
        with self._lock:
            if key in self._qtable:
                return self._qtable[key].n_visits
            else:
                return 0
    
    def get_all_q_values(
        self,
        agent_name: Optional[str] = None,
        task_type: Optional[str] = None
    ) -> List[QEntry]:
        """
        Get all Q-values, optionally filtered by agent and/or task type.
        
        Args:
            agent_name: Filter by agent name (optional)
            task_type: Filter by task type (optional)
        
        Returns:
            List of QEntry objects matching filters
        """
        with self._lock:
            entries = list(self._qtable.values())
        
        # Apply filters
        if agent_name is not None:
            entries = [e for e in entries if e.state_action.startswith(f"{agent_name}:")]
        
        if task_type is not None:
            entries = [e for e in entries if f":{task_type}:" in e.state_action]
        
        return entries
    
    def _load_qtable(self) -> None:
        """Load Q-table from JSONL file."""
        if not self.qtable_file.exists():
            return
        
        with self._lock:
            self._qtable.clear()
            
            with open(self.qtable_file, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        entry = QEntry.from_dict(data)
                        self._qtable[entry.state_action] = entry
    
    def _save_qtable(self) -> None:
        """Save Q-table to JSONL file."""
        with self._lock:
            with open(self.qtable_file, 'w') as f:
                for entry in self._qtable.values():
                    f.write(json.dumps(entry.to_dict()) + '\n')


def main():
    """Example usage of Q-learning engine."""
    print("=" * 60)
    print("Q-Learning Engine Demo")
    print("=" * 60)
    print()
    
    # Initialize Q-learning engine
    q_engine = QLearningEngine(
        learning_rate=0.1,
        exploration_rate=0.1
    )
    
    # Example: Select variant for API design task
    agent_name = "backend-architect"
    task_type = "api-design"
    available_variants = ["default", "api-optimized", "database-focused"]
    
    print("Step 1: Select Variant (ε-greedy)")
    print("-" * 60)
    print(f"Agent: {agent_name}")
    print(f"Task Type: {task_type}")
    print(f"Available Variants: {available_variants}")
    print()
    
    # Perform selection
    variant_id, q_value, exploration = q_engine.select_variant(
        agent_name, task_type, available_variants
    )
    
    print(f"Selected: {variant_id}")
    print(f"Q-value: {q_value:.3f}")
    print(f"Exploration: {exploration}")
    print()
    
    # Simulate execution with reward
    print("Step 2: Execute and Calculate Reward")
    print("-" * 60)
    print("Simulating agent execution...")
    
    # Simulate different reward scenarios
    reward = 0.75  # Positive reward for good performance
    print(f"Reward: {reward:.2f}")
    print()
    
    # Update Q-value
    print("Step 3: Update Q-value (TD(0))")
    print("-" * 60)
    
    old_q = q_engine.get_q_value(agent_name, task_type, variant_id)
    q_engine.update_q_value(agent_name, task_type, variant_id, reward)
    new_q = q_engine.get_q_value(agent_name, task_type, variant_id)
    
    print(f"Old Q-value: {old_q:.3f}")
    print(f"New Q-value: {new_q:.3f}")
    print(f"Change: {new_q - old_q:+.3f}")
    print()
    
    # Multiple iterations to show learning
    print("Step 4: Simulate Multiple Invocations")
    print("-" * 60)
    print()
    
    for i in range(5):
        variant_id, q_value, exploration = q_engine.select_variant(
            agent_name, task_type, available_variants
        )
        
        # Simulate varying rewards
        reward = 0.5 + random.random() * 0.5  # 0.5-1.0
        
        q_engine.update_q_value(agent_name, task_type, variant_id, reward)
        
        print(f"Iteration {i+1}: {variant_id} | Reward: {reward:.2f} | "
              f"Q-value: {q_engine.get_q_value(agent_name, task_type, variant_id):.3f} | "
              f"Exploration: {exploration}")
    
    print()
    
    # Show final Q-values
    print("Step 5: Final Q-values")
    print("-" * 60)
    
    for variant in available_variants:
        q_val = q_engine.get_q_value(agent_name, task_type, variant)
        visits = q_engine.get_visit_count(agent_name, task_type, variant)
        print(f"{variant:20s} | Q={q_val:.3f} | Visits={visits}")
    
    print()
    print("=" * 60)
    print(f"Q-table saved to: {q_engine.qtable_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
