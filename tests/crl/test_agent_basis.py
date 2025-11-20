#!/usr/bin/env python3
"""
Unit tests for Agent Basis Manager (CRL Phase 1)
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.agent_basis import (
    AgentBasisManager,
    AgentVariant,
    PromptModification,
    PerformanceMetrics
)


class TestAgentBasisManager(unittest.TestCase):
    """Test suite for AgentBasisManager"""
    
    def setUp(self):
        """Create temporary directory for test variants"""
        self.test_dir = tempfile.mkdtemp()
        self.manager = AgentBasisManager(basis_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_create_variant(self):
        """Test creating a new agent variant"""
        variant = self.manager.create_variant(
            agent_name="test-agent",
            variant_id="test-variant",
            description="Test variant",
            specialization=["testing"],
            model_tier="balanced",
            temperature=0.7
        )
        
        self.assertEqual(variant.variant_id, "test-variant")
        self.assertEqual(variant.agent_name, "test-agent")
        self.assertEqual(variant.specialization, ["testing"])
        self.assertEqual(variant.performance_metrics.invocation_count, 0)
    
    def test_create_duplicate_variant_fails(self):
        """Test that creating duplicate variant raises error"""
        self.manager.create_variant(
            agent_name="test-agent",
            variant_id="duplicate",
            description="First",
            specialization=[]
        )
        
        with self.assertRaises(ValueError):
            self.manager.create_variant(
                agent_name="test-agent",
                variant_id="duplicate",
                description="Second",
                specialization=[]
            )
    
    def test_load_variant(self):
        """Test loading a variant from disk"""
        # Create variant
        created = self.manager.create_variant(
            agent_name="test-agent",
            variant_id="loadable",
            description="Loadable variant",
            specialization=["load-test"]
        )
        
        # Clear cache to force disk read
        self.manager._variant_cache.clear()
        
        # Load variant
        loaded = self.manager.load_variant("test-agent", "loadable")
        
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.variant_id, "loadable")
        self.assertEqual(loaded.specialization, ["load-test"])
    
    def test_load_nonexistent_variant(self):
        """Test loading variant that doesn't exist returns None"""
        result = self.manager.load_variant("nonexistent", "variant")
        self.assertIsNone(result)
    
    def test_list_variants(self):
        """Test listing all variants for an agent"""
        # Create multiple variants
        self.manager.create_variant(
            agent_name="multi-agent",
            variant_id="variant-1",
            description="First",
            specialization=[]
        )
        self.manager.create_variant(
            agent_name="multi-agent",
            variant_id="variant-2",
            description="Second",
            specialization=[]
        )
        
        variants = self.manager.list_variants("multi-agent")
        
        self.assertEqual(len(variants), 2)
        self.assertIn("variant-1", variants)
        self.assertIn("variant-2", variants)
    
    def test_list_variants_empty(self):
        """Test listing variants for agent with no variants"""
        variants = self.manager.list_variants("nonexistent-agent")
        self.assertEqual(variants, [])
    
    def test_update_metrics(self):
        """Test updating variant performance metrics"""
        # Create variant
        self.manager.create_variant(
            agent_name="test-agent",
            variant_id="metrics-test",
            description="Metrics test",
            specialization=[]
        )
        
        # Update metrics
        self.manager.update_metrics(
            agent_name="test-agent",
            variant_id="metrics-test",
            success=True,
            duration=120.5,
            quality_score=0.85,
            reward=2.1
        )
        
        # Verify updates
        variant = self.manager.load_variant("test-agent", "metrics-test")
        self.assertEqual(variant.performance_metrics.invocation_count, 1)
        self.assertEqual(variant.performance_metrics.success_count, 1)
        self.assertAlmostEqual(variant.performance_metrics.avg_duration, 120.5)
        self.assertAlmostEqual(variant.performance_metrics.avg_quality_score, 0.85)
        self.assertAlmostEqual(variant.performance_metrics.avg_reward, 2.1)
    
    def test_update_metrics_incremental_averaging(self):
        """Test that metrics use incremental averaging correctly"""
        # Create variant
        self.manager.create_variant(
            agent_name="test-agent",
            variant_id="avg-test",
            description="Average test",
            specialization=[]
        )
        
        # First update
        self.manager.update_metrics(
            agent_name="test-agent",
            variant_id="avg-test",
            success=True,
            duration=100.0,
            quality_score=0.8,
            reward=2.0
        )
        
        # Second update
        self.manager.update_metrics(
            agent_name="test-agent",
            variant_id="avg-test",
            success=True,
            duration=200.0,
            quality_score=0.6,
            reward=1.5
        )
        
        # Verify averages
        variant = self.manager.load_variant("test-agent", "avg-test")
        self.assertEqual(variant.performance_metrics.invocation_count, 2)
        self.assertEqual(variant.performance_metrics.success_count, 2)
        self.assertAlmostEqual(variant.performance_metrics.avg_duration, 150.0)
        self.assertAlmostEqual(variant.performance_metrics.avg_quality_score, 0.7)
        self.assertAlmostEqual(variant.performance_metrics.avg_reward, 1.75)
    
    def test_update_metrics_task_type_specific(self):
        """Test task-type-specific metric tracking"""
        # Create variant
        self.manager.create_variant(
            agent_name="test-agent",
            variant_id="task-test",
            description="Task-specific test",
            specialization=[]
        )
        
        # Update with task type
        self.manager.update_metrics(
            agent_name="test-agent",
            variant_id="task-test",
            success=True,
            duration=100.0,
            quality_score=0.9,
            reward=2.5,
            task_type="api-design"
        )
        
        # Verify task-specific metrics
        variant = self.manager.load_variant("test-agent", "task-test")
        self.assertIn("api-design", variant.task_type_performance)
        
        tt_metrics = variant.task_type_performance["api-design"]
        self.assertEqual(tt_metrics["invocation_count"], 1)
        self.assertEqual(tt_metrics["success_count"], 1)
        self.assertAlmostEqual(tt_metrics["avg_reward"], 2.5)
    
    def test_update_nonexistent_variant_fails(self):
        """Test updating metrics for nonexistent variant raises error"""
        with self.assertRaises(ValueError):
            self.manager.update_metrics(
                agent_name="nonexistent",
                variant_id="variant",
                success=True,
                duration=100.0
            )
    
    def test_get_best_variant_for_task(self):
        """Test selecting best variant for a task type"""
        # Create variants
        self.manager.create_variant(
            agent_name="test-agent",
            variant_id="good",
            description="Good variant",
            specialization=[]
        )
        self.manager.create_variant(
            agent_name="test-agent",
            variant_id="better",
            description="Better variant",
            specialization=[]
        )
        
        # Add performance data
        # good variant: avg_reward = 1.5
        for _ in range(10):
            self.manager.update_metrics(
                "test-agent", "good", True, 100.0,
                quality_score=0.7, reward=1.5, task_type="test-task"
            )
        
        # better variant: avg_reward = 2.5
        for _ in range(10):
            self.manager.update_metrics(
                "test-agent", "better", True, 100.0,
                quality_score=0.9, reward=2.5, task_type="test-task"
            )
        
        # Get best variant
        best = self.manager.get_best_variant_for_task(
            "test-agent", "test-task", min_sample_count=5
        )
        
        self.assertEqual(best, "better")
    
    def test_get_best_variant_insufficient_samples(self):
        """Test best variant returns None if insufficient samples"""
        # Create variant with insufficient samples
        self.manager.create_variant(
            agent_name="test-agent",
            variant_id="few-samples",
            description="Few samples",
            specialization=[]
        )
        
        # Only 2 samples (below min_sample_count of 5)
        for _ in range(2):
            self.manager.update_metrics(
                "test-agent", "few-samples", True, 100.0,
                reward=2.5, task_type="test-task"
            )
        
        best = self.manager.get_best_variant_for_task(
            "test-agent", "test-task", min_sample_count=5
        )
        
        self.assertIsNone(best)
    
    def test_variant_serialization(self):
        """Test variant to_dict and from_dict round-trip"""
        # Create variant with prompt modifications
        variant = AgentVariant(
            variant_id="serialize-test",
            agent_name="test-agent",
            description="Serialization test",
            specialization=["test"],
            model_tier="balanced",
            temperature=0.7,
            prompt_modifications=[
                PromptModification(
                    section="Test Section",
                    operation="append",
                    content="Test content"
                )
            ],
            performance_metrics=PerformanceMetrics(
                invocation_count=5,
                success_count=4,
                avg_duration=100.0,
                avg_quality_score=0.8,
                avg_reward=2.0
            ),
            created_at=datetime.utcnow().isoformat() + "Z"
        )
        
        # Serialize to dict
        data = variant.to_dict()
        
        # Deserialize back
        restored = AgentVariant.from_dict(data)
        
        # Verify all fields
        self.assertEqual(restored.variant_id, variant.variant_id)
        self.assertEqual(restored.agent_name, variant.agent_name)
        self.assertEqual(restored.specialization, variant.specialization)
        self.assertEqual(len(restored.prompt_modifications), 1)
        self.assertEqual(
            restored.prompt_modifications[0].content,
            "Test content"
        )
        self.assertEqual(
            restored.performance_metrics.invocation_count,
            5
        )


class TestPromptModification(unittest.TestCase):
    """Test suite for PromptModification dataclass"""
    
    def test_create_prompt_modification(self):
        """Test creating a prompt modification"""
        mod = PromptModification(
            section="Core Responsibilities",
            operation="append",
            content="Additional responsibilities..."
        )
        
        self.assertEqual(mod.section, "Core Responsibilities")
        self.assertEqual(mod.operation, "append")
        self.assertIn("Additional", mod.content)


class TestPerformanceMetrics(unittest.TestCase):
    """Test suite for PerformanceMetrics dataclass"""
    
    def test_create_metrics(self):
        """Test creating performance metrics"""
        metrics = PerformanceMetrics(
            invocation_count=10,
            success_count=8,
            avg_duration=125.5,
            avg_quality_score=0.75,
            avg_reward=1.8
        )
        
        self.assertEqual(metrics.invocation_count, 10)
        self.assertEqual(metrics.success_count, 8)
        self.assertAlmostEqual(metrics.avg_duration, 125.5)
    
    def test_default_metrics(self):
        """Test default metric values"""
        metrics = PerformanceMetrics()
        
        self.assertEqual(metrics.invocation_count, 0)
        self.assertEqual(metrics.success_count, 0)
        self.assertEqual(metrics.avg_duration, 0.0)


if __name__ == "__main__":
    unittest.main()
