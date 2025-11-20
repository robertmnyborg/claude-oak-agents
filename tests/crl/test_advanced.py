#!/usr/bin/env python3
"""
Unit Tests for Phase 4 Advanced CRL Algorithms

Tests UCB1, Thompson Sampling, Contextual Bandits, Transfer Learning, and Variant Mutation.
"""

import unittest
import numpy as np
import tempfile
import shutil
from pathlib import Path

from core.bandits import UCB1Bandit, ThompsonSamplingBandit, ArmStatistics
from core.contextual_bandits import ContextualBandit, LinUCB
from core.transfer_learning import TransferLearningEngine
from core.variant_mutator import VariantMutator
from core.agent_basis import AgentBasisManager, AgentVariant, PromptModification, PerformanceMetrics


class TestUCB1Bandit(unittest.TestCase):
    """Test UCB1 bandit algorithm."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = Path(self.temp_dir) / "ucb1_test.jsonl"
        self.bandit = UCB1Bandit(exploration_constant=1.414, state_file=self.state_file)
    
    def tearDown(self):
        """Clean up test artifacts."""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test bandit initialization."""
        self.assertEqual(self.bandit.c, 1.414)
        self.assertEqual(self.bandit.total_pulls, 0)
        self.assertEqual(len(self.bandit.arm_stats), 0)
    
    def test_select_untried_arm(self):
        """Test selection of untried arms."""
        arms = ["arm1", "arm2", "arm3"]
        
        # First selection should try arm1 (untried)
        arm, ucb, metadata = self.bandit.select_arm(arms)
        
        self.assertIn(arm, arms)
        self.assertEqual(ucb, float('inf'))
        self.assertEqual(metadata["strategy"], "optimistic_init")
    
    def test_update_and_statistics(self):
        """Test update mechanism and statistics."""
        self.bandit.update("arm1", 0.8)
        self.bandit.update("arm1", 0.6)
        
        stats = self.bandit.arm_stats["arm1"]
        self.assertEqual(stats.n_pulls, 2)
        self.assertEqual(stats.total_reward, 1.4)
        self.assertEqual(stats.average_reward(), 0.7)
    
    def test_ucb_calculation(self):
        """Test UCB value calculation."""
        # Initialize with some data
        self.bandit.update("arm1", 0.8)
        self.bandit.update("arm2", 0.6)
        
        ucb1 = self.bandit.get_ucb_value("arm1", total_plays=2)
        ucb2 = self.bandit.get_ucb_value("arm2", total_plays=2)
        
        # arm1 has higher reward, should have higher base value
        # Both have same exploration bonus (same n_pulls and total_plays)
        self.assertGreater(ucb1, ucb2)
    
    def test_persistence(self):
        """Test state persistence."""
        self.bandit.update("arm1", 0.8)
        self.bandit.update("arm2", 0.6)
        
        # Create new bandit with same state file
        new_bandit = UCB1Bandit(state_file=self.state_file)
        
        self.assertEqual(new_bandit.total_pulls, 2)
        self.assertEqual(len(new_bandit.arm_stats), 2)
        self.assertEqual(new_bandit.arm_stats["arm1"].average_reward(), 0.8)


class TestThompsonSamplingBandit(unittest.TestCase):
    """Test Thompson Sampling bandit algorithm."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = Path(self.temp_dir) / "thompson_test.jsonl"
        self.bandit = ThompsonSamplingBandit(
            alpha_prior=1.0,
            beta_prior=1.0,
            state_file=self.state_file
        )
    
    def tearDown(self):
        """Clean up test artifacts."""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test bandit initialization."""
        self.assertEqual(self.bandit.alpha_prior, 1.0)
        self.assertEqual(self.bandit.beta_prior, 1.0)
        self.assertEqual(len(self.bandit.posteriors), 0)
    
    def test_select_arm(self):
        """Test arm selection."""
        arms = ["arm1", "arm2", "arm3"]
        
        arm, sampled_value, metadata = self.bandit.select_arm(arms)
        
        self.assertIn(arm, arms)
        self.assertGreaterEqual(sampled_value, 0.0)
        self.assertLessEqual(sampled_value, 1.0)
        self.assertEqual(metadata["strategy"], "thompson_sampling")
    
    def test_update_posterior(self):
        """Test posterior update mechanism."""
        # Success updates alpha
        self.bandit.update("arm1", 0.8)  # Success
        alpha, beta = self.bandit.posteriors["arm1"]
        self.assertEqual(alpha, 2.0)  # Prior 1.0 + 1 success
        self.assertEqual(beta, 1.0)   # No change
        
        # Failure updates beta
        self.bandit.update("arm1", 0.3)  # Failure
        alpha, beta = self.bandit.posteriors["arm1"]
        self.assertEqual(alpha, 2.0)  # No change
        self.assertEqual(beta, 2.0)   # Prior 1.0 + 1 failure
    
    def test_statistics(self):
        """Test statistics computation."""
        self.bandit.update("arm1", 0.9)
        self.bandit.update("arm1", 0.8)
        self.bandit.update("arm2", 0.3)
        
        stats = self.bandit.get_statistics()
        
        self.assertEqual(stats["total_pulls"], 3)
        self.assertEqual(stats["num_arms"], 2)
        self.assertIn("arm1", stats["arms"])
        self.assertIn("arm2", stats["arms"])


class TestContextualBandit(unittest.TestCase):
    """Test contextual bandit with LinUCB."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.bandit = ContextualBandit(feature_dim=10)
    
    def test_feature_extraction(self):
        """Test context feature extraction."""
        features = self.bandit.extract_features(
            user_request="Create REST API with authentication",
            file_paths=["src/api/users.ts", "src/auth/jwt.ts"],
            agent_name="backend-architect",
            task_type="api-design"
        )
        
        self.assertEqual(len(features), 10)
        self.assertTrue(np.all(features >= 0.0))
        self.assertTrue(np.all(features <= 1.0))
    
    def test_complexity_estimation(self):
        """Test task complexity estimation."""
        simple = self.bandit._estimate_complexity("Fix typo")
        complex_task = self.bandit._estimate_complexity(
            "Design distributed microservices architecture with event sourcing, "
            "implement CQRS pattern, and optimize for scalability"
        )
        
        self.assertLess(simple, complex_task)
    
    def test_file_type_distribution(self):
        """Test file type distribution calculation."""
        files = [
            "src/components/Button.tsx",
            "src/pages/Home.tsx",
            "src/api/users.ts"
        ]
        
        distribution = self.bandit._file_type_distribution(files)
        
        self.assertEqual(len(distribution), 3)
        # Should detect more frontend than backend
        self.assertGreater(distribution[0], distribution[1])
    
    def test_tech_stack_detection(self):
        """Test technology stack detection."""
        request = "Build React dashboard with TypeScript"
        files = ["src/Dashboard.tsx"]
        
        tech_stack = self.bandit._detect_tech_stack(request, files)
        
        self.assertEqual(len(tech_stack), 3)
        self.assertEqual(tech_stack[0], 1.0)  # TypeScript detected
    
    def test_arm_selection(self):
        """Test contextual arm selection."""
        arms = ["arm1", "arm2", "arm3"]
        context = np.random.rand(10)
        
        arm, ucb_value, metadata = self.bandit.select_arm(arms, context)
        
        self.assertIn(arm, arms)
        self.assertEqual(metadata["strategy"], "linucb")
    
    def test_linucb_update(self):
        """Test LinUCB model update."""
        context = np.random.rand(10)
        
        self.bandit.select_arm(["arm1"], context)
        self.bandit.update("arm1", context, 0.8)
        
        model = self.bandit.arm_models["arm1"]
        self.assertEqual(model.n_samples, 1)


class TestLinUCB(unittest.TestCase):
    """Test LinUCB model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = LinUCB(feature_dim=5, alpha=1.0)
    
    def test_initialization(self):
        """Test model initialization."""
        self.assertEqual(self.model.d, 5)
        self.assertEqual(self.model.alpha, 1.0)
        self.assertEqual(self.model.n_samples, 0)
        self.assertTrue(np.allclose(self.model.theta, np.zeros(5)))
    
    def test_prediction(self):
        """Test UCB prediction."""
        x = np.array([1.0, 0.5, 0.0, 0.3, 0.7])
        
        ucb = self.model.predict(x)
        
        # First prediction should have high exploration bonus
        self.assertGreater(ucb, 0.0)
    
    def test_update_and_learning(self):
        """Test model update and learning."""
        x1 = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
        x2 = np.array([0.0, 1.0, 0.0, 0.0, 0.0])
        
        # Update with positive reward for x1
        self.model.update(x1, 0.9)
        self.model.update(x1, 0.8)
        
        # Update with negative reward for x2
        self.model.update(x2, 0.2)
        
        # Model should predict higher value for x1
        pred1 = self.model.predict(x1)
        pred2 = self.model.predict(x2)
        
        self.assertGreater(pred1, pred2)


class TestTransferLearning(unittest.TestCase):
    """Test transfer learning between tasks."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.transfer = TransferLearningEngine()
    
    def tearDown(self):
        """Clean up test artifacts."""
        shutil.rmtree(self.temp_dir)
    
    def test_task_similarity(self):
        """Test task similarity retrieval."""
        similarity = self.transfer.get_task_similarity("api-design", "database-schema")
        
        self.assertGreater(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
    
    def test_find_similar_tasks(self):
        """Test finding similar tasks."""
        similar = self.transfer.find_similar_tasks("api-design", min_similarity=0.5)
        
        self.assertIsInstance(similar, list)
        
        # Check structure
        for task, similarity in similar:
            self.assertIsInstance(task, str)
            self.assertGreaterEqual(similarity, 0.5)
    
    def test_symmetry(self):
        """Test similarity symmetry."""
        sim1 = self.transfer.get_task_similarity("api-design", "database-schema")
        sim2 = self.transfer.get_task_similarity("database-schema", "api-design")
        
        self.assertEqual(sim1, sim2)


class TestVariantMutator(unittest.TestCase):
    """Test variant mutation and evolutionary search."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.basis_manager = AgentBasisManager(basis_dir=Path(self.temp_dir))
        self.mutator = VariantMutator(agent_basis=self.basis_manager)
        
        # Create test variant
        self.test_variant = AgentVariant(
            variant_id="test-variant",
            agent_name="test-agent",
            description="Test variant",
            specialization=["testing"],
            model_tier="balanced",
            temperature=0.7,
            prompt_modifications=[
                PromptModification(
                    section="Test",
                    operation="append",
                    content="Test content"
                )
            ],
            performance_metrics=PerformanceMetrics(),
            created_at="2025-01-01T00:00:00Z"
        )
        
        self.basis_manager.save_variant(self.test_variant)
    
    def tearDown(self):
        """Clean up test artifacts."""
        shutil.rmtree(self.temp_dir)
    
    def test_parameter_mutation(self):
        """Test parameter mutation."""
        mutated = self.mutator.mutate_variant(
            "test-agent",
            "test-variant",
            "parameter",
            strength=0.2
        )
        
        self.assertIsNotNone(mutated)
        self.assertNotEqual(mutated.variant_id, "test-variant")
        self.assertNotEqual(mutated.temperature, 0.7)  # Should be mutated
        self.assertGreaterEqual(mutated.temperature, 0.0)
        self.assertLessEqual(mutated.temperature, 1.0)
    
    def test_prompt_mutation(self):
        """Test prompt mutation."""
        mutated = self.mutator.mutate_variant(
            "test-agent",
            "test-variant",
            "prompt",
            strength=0.3
        )
        
        self.assertIsNotNone(mutated)
        # Prompt modifications may be added or removed
        self.assertIsInstance(mutated.prompt_modifications, list)
    
    def test_model_tier_mutation(self):
        """Test model tier mutation."""
        mutated = self.mutator.mutate_variant(
            "test-agent",
            "test-variant",
            "model",
            strength=0.0
        )
        
        self.assertIsNotNone(mutated)
        self.assertIn(mutated.model_tier, ["fast", "balanced", "premium"])
        self.assertNotEqual(mutated.model_tier, "balanced")  # Should change
    
    def test_variant_combination(self):
        """Test variant combination."""
        # Create second variant
        variant2 = AgentVariant(
            variant_id="test-variant-2",
            agent_name="test-agent",
            description="Test variant 2",
            specialization=["testing2"],
            model_tier="premium",
            temperature=0.9,
            prompt_modifications=[],
            performance_metrics=PerformanceMetrics(),
            created_at="2025-01-01T00:00:00Z"
        )
        self.basis_manager.save_variant(variant2)
        
        # Combine variants
        combined = self.mutator.combine_variants(
            "test-agent",
            "test-variant",
            "test-variant-2",
            crossover_rate=0.5
        )
        
        self.assertIsNotNone(combined)
        self.assertTrue(combined.variant_id.startswith("combined-"))
        # Should inherit from both parents
        self.assertIn(combined.model_tier, ["balanced", "premium"])


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestUCB1Bandit))
    suite.addTests(loader.loadTestsFromTestCase(TestThompsonSamplingBandit))
    suite.addTests(loader.loadTestsFromTestCase(TestContextualBandit))
    suite.addTests(loader.loadTestsFromTestCase(TestLinUCB))
    suite.addTests(loader.loadTestsFromTestCase(TestTransferLearning))
    suite.addTests(loader.loadTestsFromTestCase(TestVariantMutator))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
