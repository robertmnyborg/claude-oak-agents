#!/usr/bin/env python3
"""
Contextual Bandit Algorithms for State-Aware Variant Selection

Implements LinUCB (Linear Upper Confidence Bound) for contextual bandits.
Considers state features like task complexity, file types, and tech stack
when selecting variants.
"""

import numpy as np
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json


class ContextualBandit:
    """
    Contextual bandit that considers state features for variant selection.
    
    State features:
    - Task complexity (low/medium/high)
    - File types involved (frontend/backend/infrastructure)
    - User history (preferred patterns)
    - Codebase context (language, framework)
    - Time of day (if patterns exist)
    
    Uses linear model: reward = w^T * features
    """
    
    def __init__(self, feature_dim: int = 10):
        """
        Initialize contextual bandit.
        
        Args:
            feature_dim: Number of context features
        """
        self.feature_dim = feature_dim
        self.arm_models: Dict[str, 'LinUCB'] = {}
    
    def extract_features(
        self,
        user_request: str,
        file_paths: Optional[List[str]] = None,
        agent_name: Optional[str] = None,
        task_type: Optional[str] = None
    ) -> np.ndarray:
        """
        Extract context features from current situation.
        
        Returns feature vector [f1, f2, ..., fn]
        
        Args:
            user_request: User's request text
            file_paths: List of file paths involved
            agent_name: Agent name for user preference
            task_type: Classified task type
        
        Returns:
            Feature vector (numpy array)
        """
        features = np.zeros(self.feature_dim)
        
        if file_paths is None:
            file_paths = []
        
        # Feature 0: Task complexity (0-1)
        features[0] = self._estimate_complexity(user_request)
        
        # Features 1-3: File type distribution
        features[1:4] = self._file_type_distribution(file_paths)
        
        # Feature 4: Request length (normalized)
        features[4] = min(len(user_request) / 1000, 1.0)
        
        # Features 5-7: Tech stack indicators
        features[5:8] = self._detect_tech_stack(user_request, file_paths)
        
        # Feature 8: Time of day (cyclical encoding)
        features[8] = self._time_of_day_feature()
        
        # Feature 9: User preference placeholder (requires history)
        features[9] = 0.5  # Neutral default
        
        return features
    
    def _estimate_complexity(self, user_request: str) -> float:
        """
        Estimate task complexity from request text.
        
        Returns value 0.0-1.0 (0=simple, 1=complex)
        """
        # Heuristics for complexity
        complexity_score = 0.0
        
        # Length-based
        if len(user_request) > 500:
            complexity_score += 0.3
        elif len(user_request) > 200:
            complexity_score += 0.15
        
        # Keyword-based
        complex_keywords = [
            "architecture", "system", "migrate", "refactor",
            "optimize", "scale", "distributed", "security"
        ]
        complexity_score += 0.1 * sum(
            1 for keyword in complex_keywords
            if keyword in user_request.lower()
        )
        
        # Multiple requirements indicator
        if user_request.count(" and ") + user_request.count(",") > 3:
            complexity_score += 0.2
        
        return min(complexity_score, 1.0)
    
    def _file_type_distribution(self, file_paths: List[str]) -> np.ndarray:
        """
        Calculate distribution of file types.
        
        Returns [frontend_ratio, backend_ratio, infrastructure_ratio]
        """
        if not file_paths:
            return np.array([0.0, 0.0, 0.0])
        
        frontend_count = 0
        backend_count = 0
        infra_count = 0
        
        frontend_exts = {'.tsx', '.jsx', '.vue', '.html', '.css', '.scss'}
        backend_exts = {'.ts', '.js', '.py', '.go', '.rb', '.java'}
        infra_exts = {'.yaml', '.yml', '.tf', '.json', '.toml', '.sh'}
        
        for path in file_paths:
            ext = Path(path).suffix.lower()
            
            if ext in frontend_exts or '/components/' in path or '/pages/' in path:
                frontend_count += 1
            elif ext in backend_exts or '/api/' in path or '/services/' in path:
                backend_count += 1
            elif ext in infra_exts or 'cdk' in path.lower() or 'terraform' in path.lower():
                infra_count += 1
        
        total = max(frontend_count + backend_count + infra_count, 1)
        
        return np.array([
            frontend_count / total,
            backend_count / total,
            infra_count / total
        ])
    
    def _detect_tech_stack(
        self,
        user_request: str,
        file_paths: List[str]
    ) -> np.ndarray:
        """
        Detect technology stack indicators.
        
        Returns [typescript_indicator, python_indicator, aws_indicator]
        """
        text = user_request.lower()
        paths_text = " ".join(file_paths).lower()
        combined = text + " " + paths_text
        
        typescript = float(
            'typescript' in combined or
            'react' in combined or
            'vue' in combined or
            '.tsx' in paths_text or
            '.ts' in paths_text
        )
        
        python = float(
            'python' in combined or
            '.py' in paths_text or
            'django' in combined or
            'flask' in combined
        )
        
        aws = float(
            'aws' in combined or
            'lambda' in combined or
            'cdk' in combined or
            's3' in combined or
            'dynamodb' in combined
        )
        
        return np.array([typescript, python, aws])
    
    def _time_of_day_feature(self) -> float:
        """
        Encode time of day as cyclical feature.
        
        Returns value 0.0-1.0 based on hour of day
        """
        hour = datetime.now().hour
        # Cyclical encoding: sin(2π * hour / 24)
        # Maps to 0.0-1.0 range
        return (np.sin(2 * np.pi * hour / 24) + 1) / 2
    
    def select_arm(
        self,
        available_arms: List[str],
        context_features: np.ndarray,
        alpha: float = 1.0
    ) -> Tuple[str, float, Dict]:
        """
        Select arm based on context using LinUCB.
        
        Args:
            available_arms: List of arm IDs
            context_features: Feature vector
            alpha: Exploration parameter
        
        Returns:
            Tuple of (arm_id, ucb_value, metadata)
        """
        if not available_arms:
            raise ValueError("No arms available for selection")
        
        # Initialize models for new arms
        for arm_id in available_arms:
            if arm_id not in self.arm_models:
                self.arm_models[arm_id] = LinUCB(
                    feature_dim=self.feature_dim,
                    alpha=alpha
                )
        
        # Calculate UCB for each arm
        ucb_values = {}
        for arm_id in available_arms:
            model = self.arm_models[arm_id]
            ucb_values[arm_id] = model.predict(context_features)
        
        # Select arm with highest UCB
        selected_arm = max(ucb_values.items(), key=lambda x: x[1])[0]
        ucb_value = ucb_values[selected_arm]
        
        metadata = {
            "strategy": "linucb",
            "ucb_values": {k: round(v, 4) for k, v in ucb_values.items()},
            "context_norm": round(float(np.linalg.norm(context_features)), 4)
        }
        
        return (selected_arm, ucb_value, metadata)
    
    def update(
        self,
        arm_id: str,
        context_features: np.ndarray,
        reward: float
    ) -> None:
        """
        Update arm model with observed reward.
        
        Args:
            arm_id: Arm that was pulled
            context_features: Context when arm was pulled
            reward: Observed reward
        """
        if arm_id not in self.arm_models:
            self.arm_models[arm_id] = LinUCB(feature_dim=self.feature_dim)
        
        self.arm_models[arm_id].update(context_features, reward)


class LinUCB:
    """
    Linear Upper Confidence Bound for contextual bandits.
    
    Maintains linear model per arm:
    - Expected reward: θ^T * x (linear prediction)
    - Confidence bound: α * sqrt(x^T * A^-1 * x)
    - Selection: argmax(θ^T * x + confidence_bound)
    
    Reference: Li et al. (2010) "A Contextual-Bandit Approach to 
               Personalized News Article Recommendation"
    """
    
    def __init__(self, feature_dim: int, alpha: float = 1.0):
        """
        Initialize LinUCB model.
        
        Args:
            feature_dim: Dimension of context features
            alpha: Confidence parameter (higher = more exploration)
        """
        self.d = feature_dim
        self.alpha = alpha
        
        # A = D^T * D + I (design matrix)
        self.A = np.identity(self.d)
        
        # b = D^T * c (reward vector)
        self.b = np.zeros(self.d)
        
        # θ = A^-1 * b (parameter estimate)
        self.theta = np.zeros(self.d)
        
        self.n_samples = 0
    
    def predict(self, x: np.ndarray) -> float:
        """
        Predict UCB value for context x.
        
        UCB = θ^T * x + α * sqrt(x^T * A^-1 * x)
        
        Args:
            x: Context feature vector
        
        Returns:
            UCB value
        """
        # Expected reward
        expected_reward = np.dot(self.theta, x)
        
        # Confidence bound
        A_inv = np.linalg.inv(self.A)
        confidence = self.alpha * np.sqrt(np.dot(x, np.dot(A_inv, x)))
        
        return expected_reward + confidence
    
    def update(self, x: np.ndarray, r: float) -> None:
        """
        Update model with observed (context, reward) pair.
        
        Args:
            x: Context feature vector
            r: Observed reward
        """
        # Update A = A + x * x^T
        self.A += np.outer(x, x)
        
        # Update b = b + r * x
        self.b += r * x
        
        # Recompute θ = A^-1 * b
        self.theta = np.dot(np.linalg.inv(self.A), self.b)
        
        self.n_samples += 1
    
    def get_statistics(self) -> Dict:
        """Get model statistics."""
        return {
            "n_samples": self.n_samples,
            "theta_norm": round(float(np.linalg.norm(self.theta)), 4),
            "A_condition": round(float(np.linalg.cond(self.A)), 4)
        }


def main():
    """Example usage of contextual bandits."""
    print("=" * 60)
    print("Contextual Bandit (LinUCB) Demo")
    print("=" * 60)
    print()
    
    # Initialize contextual bandit
    bandit = ContextualBandit(feature_dim=10)
    
    # Available variants
    variants = ["default", "api-optimized", "database-focused"]
    
    # Example scenarios
    scenarios = [
        {
            "request": "Create REST API endpoints for user management",
            "files": ["src/api/users.ts", "src/controllers/userController.ts"],
            "agent": "backend-architect",
            "task": "api-design"
        },
        {
            "request": "Design database schema for orders",
            "files": ["src/models/order.py", "migrations/001_orders.sql"],
            "agent": "backend-architect",
            "task": "database-schema"
        },
        {
            "request": "Build React dashboard with charts",
            "files": ["src/components/Dashboard.tsx", "src/pages/analytics.tsx"],
            "agent": "frontend-developer",
            "task": "ui-implementation"
        }
    ]
    
    print("Simulating contextual bandit selection...")
    print()
    
    for i, scenario in enumerate(scenarios):
        print(f"Scenario {i+1}: {scenario['task']}")
        print(f"Request: {scenario['request'][:50]}...")
        
        # Extract features
        features = bandit.extract_features(
            user_request=scenario["request"],
            file_paths=scenario["files"],
            agent_name=scenario["agent"],
            task_type=scenario["task"]
        )
        
        print(f"Features: complexity={features[0]:.2f}, "
              f"frontend={features[1]:.2f}, "
              f"backend={features[2]:.2f}")
        
        # Select variant
        arm, ucb_value, metadata = bandit.select_arm(variants, features)
        
        print(f"Selected: {arm} (UCB={ucb_value:.3f})")
        
        # Simulate reward based on task type
        if scenario["task"] == "api-design" and arm == "api-optimized":
            reward = 0.9  # Good match
        elif scenario["task"] == "database-schema" and arm == "database-focused":
            reward = 0.9  # Good match
        else:
            reward = 0.5  # Neutral
        
        # Update model
        bandit.update(arm, features, reward)
        
        print(f"Reward: {reward:.2f}")
        print()
    
    print("=" * 60)
    print("Model Statistics After Training:")
    print("=" * 60)
    
    for arm_id, model in bandit.arm_models.items():
        stats = model.get_statistics()
        print(f"{arm_id:20s} | Samples={stats['n_samples']} | "
              f"θ_norm={stats['theta_norm']:.3f}")
    
    print()


if __name__ == "__main__":
    main()
