#!/usr/bin/env python3
"""
Unit tests for Reward Calculator
"""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.reward_calculator import RewardCalculator


class TestRewardCalculator(unittest.TestCase):
    """Test reward calculation."""
    
    def setUp(self):
        """Create reward calculator for testing."""
        self.calculator = RewardCalculator()
    
    def test_perfect_execution(self):
        """Test reward for perfect execution."""
        reward = self.calculator.calculate_reward(
            success=True,
            quality_score=1.0,
            duration_seconds=30,
            error_count=0,
            task_complexity="low"
        )

        # Success (0.4) + Quality (0.3*1.0) + Speed bonus (0.2*positive) = high reward
        self.assertGreaterEqual(reward, 0.79)  # Allow for floating point precision
        self.assertLessEqual(reward, 1.0)
    
    def test_failure(self):
        """Test reward for failed execution."""
        reward = self.calculator.calculate_reward(
            success=False,
            quality_score=0.3,
            duration_seconds=150,
            error_count=2,
            task_complexity="medium"
        )
        
        # Success (-0.4) + Quality (0.3*0.3) + Speed (negative) - Errors (0.2) = negative reward
        self.assertLess(reward, 0.0)
    
    def test_success_with_errors(self):
        """Test reward for success but with errors."""
        reward = self.calculator.calculate_reward(
            success=True,
            quality_score=0.7,
            duration_seconds=200,
            error_count=3,
            task_complexity="medium"
        )
        
        # Success (0.4) but errors reduce reward
        self.assertGreater(reward, 0.0)
        self.assertLess(reward, 0.5)
    
    def test_slow_execution(self):
        """Test reward penalty for slow execution."""
        reward_fast = self.calculator.calculate_reward(
            success=True,
            quality_score=0.8,
            duration_seconds=60,
            error_count=0,
            task_complexity="medium"
        )
        
        reward_slow = self.calculator.calculate_reward(
            success=True,
            quality_score=0.8,
            duration_seconds=600,
            error_count=0,
            task_complexity="medium"
        )
        
        # Faster execution should have higher reward
        self.assertGreater(reward_fast, reward_slow)
    
    def test_quality_impact(self):
        """Test quality score impact on reward."""
        reward_high_quality = self.calculator.calculate_reward(
            success=True,
            quality_score=1.0,
            duration_seconds=150,
            error_count=0,
            task_complexity="medium"
        )
        
        reward_low_quality = self.calculator.calculate_reward(
            success=True,
            quality_score=0.3,
            duration_seconds=150,
            error_count=0,
            task_complexity="medium"
        )
        
        # Higher quality should yield higher reward
        self.assertGreater(reward_high_quality, reward_low_quality)
    
    def test_reward_range(self):
        """Test that reward is always in [-1, 1] range."""
        # Extreme positive
        reward_pos = self.calculator.calculate_reward(
            success=True,
            quality_score=1.0,
            duration_seconds=10,
            error_count=0,
            task_complexity="low"
        )
        self.assertLessEqual(reward_pos, 1.0)
        
        # Extreme negative
        reward_neg = self.calculator.calculate_reward(
            success=False,
            quality_score=0.0,
            duration_seconds=10000,
            error_count=10,
            task_complexity="high"
        )
        self.assertGreaterEqual(reward_neg, -1.0)
    
    def test_missing_quality_score(self):
        """Test reward calculation with missing quality score."""
        reward = self.calculator.calculate_reward(
            success=True,
            quality_score=None,
            duration_seconds=150,
            error_count=0,
            task_complexity="medium"
        )
        
        # Should still calculate reward (uses neutral 0.5 assumption)
        self.assertIsInstance(reward, float)
        self.assertGreaterEqual(reward, -1.0)
        self.assertLessEqual(reward, 1.0)
    
    def test_missing_duration(self):
        """Test reward calculation with missing duration."""
        reward = self.calculator.calculate_reward(
            success=True,
            quality_score=0.8,
            duration_seconds=None,
            error_count=0,
            task_complexity="medium"
        )
        
        # Should still calculate reward (no speed component)
        self.assertIsInstance(reward, float)
        self.assertGreaterEqual(reward, -1.0)
        self.assertLessEqual(reward, 1.0)
    
    def test_complexity_baseline(self):
        """Test that complexity affects speed baseline."""
        # Same duration, different complexity
        reward_low = self.calculator.calculate_reward(
            success=True,
            quality_score=0.8,
            duration_seconds=100,
            error_count=0,
            task_complexity="low"
        )
        
        reward_high = self.calculator.calculate_reward(
            success=True,
            quality_score=0.8,
            duration_seconds=100,
            error_count=0,
            task_complexity="high"
        )
        
        # Same duration should be penalty for low complexity, bonus for high complexity
        self.assertLess(reward_low, reward_high)
    
    def test_calculate_from_invocation(self):
        """Test convenience method for invocation result."""
        invocation_result = {
            "success": True,
            "quality_score": 0.85,
            "duration": 120,
            "error_count": 0,
            "task_complexity": "medium"
        }
        
        reward = self.calculator.calculate_from_invocation(invocation_result)
        
        self.assertIsInstance(reward, float)
        self.assertGreater(reward, 0.0)
        self.assertLessEqual(reward, 1.0)
    
    def test_custom_weights(self):
        """Test custom weight configuration."""
        custom_calc = RewardCalculator(
            success_weight=0.5,
            quality_weight=0.4,
            speed_weight=0.1,
            error_penalty=0.05
        )
        
        self.assertEqual(custom_calc.success_weight, 0.5)
        self.assertEqual(custom_calc.quality_weight, 0.4)
        self.assertEqual(custom_calc.speed_weight, 0.1)
        self.assertEqual(custom_calc.error_penalty, 0.05)


def run_tests():
    """Run all reward calculator tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestRewardCalculator)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
