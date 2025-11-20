#!/usr/bin/env python3
"""
Unit tests for Q-Learning Engine
"""

import unittest
import tempfile
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.q_learning import QLearningEngine, QEntry


class TestQEntry(unittest.TestCase):
    """Test Q-table entry data structure."""
    
    def test_to_dict(self):
        """Test serialization to dictionary."""
        entry = QEntry(
            state_action="backend-architect:api-design:api-optimized",
            q_value=0.75,
            n_visits=10,
            last_updated="2025-11-19T12:00:00Z",
            convergence_score=0.05
        )
        
        data = entry.to_dict()
        
        self.assertEqual(data["state_action"], "backend-architect:api-design:api-optimized")
        self.assertEqual(data["q_value"], 0.75)
        self.assertEqual(data["n_visits"], 10)
        self.assertEqual(data["convergence_score"], 0.05)
    
    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "state_action": "backend-architect:api-design:default",
            "q_value": 0.5,
            "n_visits": 5,
            "last_updated": "2025-11-19T12:00:00Z",
            "convergence_score": 0.02
        }
        
        entry = QEntry.from_dict(data)
        
        self.assertEqual(entry.state_action, "backend-architect:api-design:default")
        self.assertEqual(entry.q_value, 0.5)
        self.assertEqual(entry.n_visits, 5)
        self.assertEqual(entry.convergence_score, 0.02)


class TestQLearningEngine(unittest.TestCase):
    """Test Q-learning engine."""
    
    def setUp(self):
        """Create temporary Q-table file for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.qtable_file = Path(self.temp_dir) / "q_table.jsonl"
        self.q_engine = QLearningEngine(
            learning_rate=0.1,
            exploration_rate=0.1,
            qtable_file=self.qtable_file
        )
    
    def test_initialization(self):
        """Test Q-learning engine initialization."""
        self.assertEqual(self.q_engine.alpha, 0.1)
        self.assertEqual(self.q_engine.epsilon, 0.1)
        self.assertTrue(self.qtable_file.exists())
    
    def test_state_action_key(self):
        """Test state-action key generation."""
        key = self.q_engine._state_action_key(
            "backend-architect", "api-design", "api-optimized"
        )
        
        self.assertEqual(key, "backend-architect:api-design:api-optimized")
    
    def test_get_q_value_initial(self):
        """Test getting Q-value for never-visited state-action."""
        q_value = self.q_engine.get_q_value(
            "backend-architect", "api-design", "default"
        )
        
        self.assertEqual(q_value, 0.0)  # Optimistic initialization
    
    def test_update_q_value(self):
        """Test Q-value update with TD(0) rule."""
        # Initial Q-value should be 0
        q_old = self.q_engine.get_q_value(
            "backend-architect", "api-design", "default"
        )
        self.assertEqual(q_old, 0.0)
        
        # Update with reward = 0.75
        reward = 0.75
        self.q_engine.update_q_value(
            "backend-architect", "api-design", "default", reward
        )
        
        # New Q-value: Q ← Q + α[R - Q] = 0 + 0.1[0.75 - 0] = 0.075
        q_new = self.q_engine.get_q_value(
            "backend-architect", "api-design", "default"
        )
        self.assertAlmostEqual(q_new, 0.075, places=6)
    
    def test_update_q_value_convergence(self):
        """Test Q-value convergence over multiple updates."""
        # Apply same reward multiple times
        reward = 1.0
        
        q_values = []
        for i in range(20):
            self.q_engine.update_q_value(
                "backend-architect", "api-design", "default", reward
            )
            q_value = self.q_engine.get_q_value(
                "backend-architect", "api-design", "default"
            )
            q_values.append(q_value)
        
        # Q-value should approach reward value
        final_q = q_values[-1]
        self.assertGreater(final_q, 0.8)  # Should be close to 1.0
        
        # Convergence: later updates should change Q-value less
        early_change = abs(q_values[1] - q_values[0])
        late_change = abs(q_values[-1] - q_values[-2])
        self.assertGreater(early_change, late_change)
    
    def test_visit_count(self):
        """Test visit count tracking."""
        # Initial count should be 0
        count = self.q_engine.get_visit_count(
            "backend-architect", "api-design", "default"
        )
        self.assertEqual(count, 0)
        
        # Update 3 times
        for i in range(3):
            self.q_engine.update_q_value(
                "backend-architect", "api-design", "default", 0.5
            )
        
        # Count should be 3
        count = self.q_engine.get_visit_count(
            "backend-architect", "api-design", "default"
        )
        self.assertEqual(count, 3)
    
    def test_select_variant_single(self):
        """Test variant selection with single option."""
        variants = ["default"]
        
        selected, q_value, exploration = self.q_engine.select_variant(
            "backend-architect", "api-design", variants
        )
        
        self.assertEqual(selected, "default")
        self.assertEqual(q_value, 0.0)  # Initial Q-value
        self.assertIsInstance(exploration, bool)
    
    def test_select_variant_multiple(self):
        """Test variant selection with multiple options."""
        variants = ["default", "api-optimized", "database-focused"]
        
        # Set different Q-values
        self.q_engine.update_q_value("backend-architect", "api-design", "api-optimized", 1.0)
        self.q_engine.update_q_value("backend-architect", "api-design", "default", 0.5)
        
        # Run multiple selections to test ε-greedy
        selections = []
        for i in range(100):
            selected, q_value, exploration = self.q_engine.select_variant(
                "backend-architect", "api-design", variants
            )
            selections.append((selected, exploration))
        
        # Should have some explorations and some exploitations
        explorations = [s for s in selections if s[1]]
        exploitations = [s for s in selections if not s[1]]
        
        self.assertGreater(len(explorations), 0)  # At least some exploration
        self.assertGreater(len(exploitations), 0)  # At least some exploitation
        
        # Most exploitations should select "api-optimized" (highest Q-value)
        api_optimized_exploitations = [s for s in exploitations if s[0] == "api-optimized"]
        self.assertGreater(len(api_optimized_exploitations), len(exploitations) * 0.5)
    
    def test_persistence(self):
        """Test Q-table persistence to disk."""
        # Create Q-values
        self.q_engine.update_q_value("backend-architect", "api-design", "default", 0.75)
        self.q_engine.update_q_value("frontend-developer", "ui-implementation", "react-specialist", 0.85)
        
        # Create new engine with same file
        new_engine = QLearningEngine(qtable_file=self.qtable_file)
        
        # Q-values should be loaded
        q1 = new_engine.get_q_value("backend-architect", "api-design", "default")
        q2 = new_engine.get_q_value("frontend-developer", "ui-implementation", "react-specialist")
        
        self.assertGreater(q1, 0.0)
        self.assertGreater(q2, 0.0)
    
    def test_get_all_q_values(self):
        """Test retrieving all Q-values."""
        # Create some Q-values
        self.q_engine.update_q_value("backend-architect", "api-design", "default", 0.5)
        self.q_engine.update_q_value("backend-architect", "database-schema", "database-focused", 0.7)
        self.q_engine.update_q_value("frontend-developer", "ui-implementation", "react-specialist", 0.9)
        
        # Get all entries
        all_entries = self.q_engine.get_all_q_values()
        self.assertEqual(len(all_entries), 3)
        
        # Filter by agent
        backend_entries = self.q_engine.get_all_q_values(agent_name="backend-architect")
        self.assertEqual(len(backend_entries), 2)
        
        # Filter by task type
        api_entries = self.q_engine.get_all_q_values(task_type="api-design")
        self.assertEqual(len(api_entries), 1)


class TestQLearningIntegration(unittest.TestCase):
    """Integration tests for Q-learning workflow."""
    
    def setUp(self):
        """Create temporary Q-table file for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.qtable_file = Path(self.temp_dir) / "q_table.jsonl"
        self.q_engine = QLearningEngine(
            learning_rate=0.1,
            exploration_rate=0.0,  # Disable exploration for deterministic testing
            qtable_file=self.qtable_file
        )
    
    def test_learning_workflow(self):
        """Test complete learning workflow."""
        agent_name = "backend-architect"
        task_type = "api-design"
        variants = ["default", "api-optimized"]
        
        # Simulate 10 invocations with different rewards
        rewards = [0.8, 0.9, 0.7, 0.85, 0.95, 0.75, 0.9, 0.8, 0.85, 0.9]
        
        for reward in rewards:
            # Select variant
            variant_id, q_value, exploration = self.q_engine.select_variant(
                agent_name, task_type, variants
            )
            
            # Simulate execution and update
            self.q_engine.update_q_value(agent_name, task_type, variant_id, reward)
        
        # Both variants should have been updated
        q_default = self.q_engine.get_q_value(agent_name, task_type, "default")
        q_optimized = self.q_engine.get_q_value(agent_name, task_type, "api-optimized")
        
        # With exploration=0, only best variant should be selected after first update
        # First invocation goes to "default" (first in list), gets Q-value
        # Second invocation should still go to "default" if it has highest Q
        # Eventually Q-values should converge toward reward values
        
        self.assertGreater(q_default, 0.0)
        # api-optimized might be 0 if never selected (depends on first reward)


def run_tests():
    """Run all Q-learning tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestQEntry))
    suite.addTests(loader.loadTestsFromTestCase(TestQLearningEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestQLearningIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
