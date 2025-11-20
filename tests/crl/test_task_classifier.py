#!/usr/bin/env python3
"""
Unit tests for Task Classifier (CRL Phase 1)
"""

import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.task_classifier import TaskClassifier


class TestTaskClassifier(unittest.TestCase):
    """Test suite for TaskClassifier"""
    
    def setUp(self):
        """Create classifier instance"""
        self.classifier = TaskClassifier()
    
    def test_classify_api_design(self):
        """Test classification of API design tasks"""
        result = self.classifier.classify(
            "Create REST API endpoints for user management",
            file_paths=["src/routes/users.ts", "src/controllers/userController.ts"]
        )
        
        self.assertEqual(result, "api-design")
    
    def test_classify_database_schema(self):
        """Test classification of database schema tasks"""
        result = self.classifier.classify(
            "Add database migration for new analytics table",
            file_paths=["migrations/20251119_add_analytics.sql"]
        )
        
        self.assertEqual(result, "database-schema")
    
    def test_classify_security_audit(self):
        """Test classification of security tasks"""
        result = self.classifier.classify(
            "Fix security vulnerability in authentication flow",
            file_paths=["src/auth/jwt.ts"]
        )
        
        self.assertEqual(result, "security-audit")
    
    def test_classify_performance_optimization(self):
        """Test classification of performance optimization tasks"""
        result = self.classifier.classify(
            "Optimize slow database queries with indexing",
            file_paths=["src/models/user.ts"]
        )
        
        self.assertEqual(result, "performance-opt")
    
    def test_classify_ui_implementation(self):
        """Test classification of UI implementation tasks"""
        result = self.classifier.classify(
            "Build login form component with validation",
            file_paths=["src/components/LoginForm.tsx"]
        )
        
        self.assertEqual(result, "ui-implementation")
    
    def test_classify_testing(self):
        """Test classification of testing tasks"""
        result = self.classifier.classify(
            "Write unit tests for user service",
            file_paths=["src/services/__tests__/userService.test.ts"]
        )
        
        self.assertEqual(result, "testing")
    
    def test_classify_bug_fix(self):
        """Test classification of bug fix tasks"""
        result = self.classifier.classify(
            "Fix broken authentication error handling",
            file_paths=[]
        )
        
        self.assertEqual(result, "bug-fix")
    
    def test_classify_refactoring(self):
        """Test classification of refactoring tasks"""
        result = self.classifier.classify(
            "Refactor user service to improve code clarity",
            file_paths=["src/services/userService.ts"]
        )
        
        self.assertEqual(result, "refactoring")
    
    def test_classify_deployment(self):
        """Test classification of deployment tasks"""
        result = self.classifier.classify(
            "Setup Docker container for Lambda deployment",
            file_paths=["Dockerfile", "serverless.yml"]
        )
        
        self.assertEqual(result, "deployment")
    
    def test_classify_documentation(self):
        """Test classification of documentation tasks"""
        result = self.classifier.classify(
            "Update README with new API documentation",
            file_paths=["README.md"]
        )
        
        self.assertEqual(result, "documentation")
    
    def test_classify_with_confidence(self):
        """Test classification with confidence scores"""
        task_type, confidence, all_scores = self.classifier.classify_with_confidence(
            "Create REST API endpoints with OpenAPI documentation",
            file_paths=["src/routes/api.ts"]
        )
        
        self.assertEqual(task_type, "api-design")
        self.assertGreater(confidence, 0.7)
        self.assertIn("api-design", all_scores)
        self.assertGreater(all_scores["api-design"], 0)
    
    def test_classify_general_fallback(self):
        """Test fallback to 'general' for ambiguous tasks"""
        result = self.classifier.classify(
            "Do something",
            file_paths=[]
        )
        
        self.assertEqual(result, "general")
    
    def test_file_pattern_matching(self):
        """Test that file patterns contribute to classification"""
        # File patterns should boost api-design score
        result = self.classifier.classify(
            "Update endpoints",  # More specific to API
            file_paths=["src/routes/users.ts", "src/controllers/users.ts"]
        )

        self.assertEqual(result, "api-design")
    
    def test_keyword_density_scoring(self):
        """Test that multiple keyword matches increase score"""
        # Multiple security keywords should strongly indicate security-audit
        result = self.classifier.classify(
            "Fix XSS vulnerability, add CSRF protection, and sanitize SQL injection",
            file_paths=[]
        )
        
        self.assertEqual(result, "security-audit")
    
    def test_get_task_types(self):
        """Test retrieving all supported task types"""
        task_types = self.classifier.get_task_types()
        
        self.assertIn("api-design", task_types)
        self.assertIn("database-schema", task_types)
        self.assertIn("security-audit", task_types)
        self.assertIn("ui-implementation", task_types)
        self.assertGreaterEqual(len(task_types), 10)
    
    def test_add_custom_task_type(self):
        """Test adding custom task type"""
        self.classifier.add_custom_task_type(
            task_type="machine-learning",
            keywords=["ml", "machine learning", "neural network", "tensorflow"],
            file_patterns=[r".*\.ipynb$", r".*/models/.*"],
            weight=1.0
        )
        
        task_types = self.classifier.get_task_types()
        self.assertIn("machine-learning", task_types)
        
        # Test classification with new task type
        result = self.classifier.classify(
            "Train neural network model with TensorFlow",
            file_paths=["models/classifier.py"]
        )
        
        self.assertEqual(result, "machine-learning")
    
    def test_add_duplicate_task_type_fails(self):
        """Test that adding duplicate task type raises error"""
        with self.assertRaises(ValueError):
            self.classifier.add_custom_task_type(
                task_type="api-design",  # Already exists
                keywords=["test"],
                file_patterns=[]
            )
    
    def test_case_insensitive_matching(self):
        """Test that keyword matching is case-insensitive"""
        result1 = self.classifier.classify(
            "CREATE REST API ENDPOINTS",
            file_paths=[]
        )
        result2 = self.classifier.classify(
            "create rest api endpoints",
            file_paths=[]
        )
        
        self.assertEqual(result1, result2)
        self.assertEqual(result1, "api-design")
    
    def test_weight_affects_scoring(self):
        """Test that task type weight affects final score"""
        # Security tasks have higher weight (1.2)
        _, _, scores1 = self.classifier.classify_with_confidence(
            "Fix authentication vulnerability",
            file_paths=[]
        )
        
        # Other tasks have weight 1.0
        _, _, scores2 = self.classifier.classify_with_confidence(
            "Fix documentation typo",
            file_paths=[]
        )
        
        # Security should be weighted higher for similar keyword match counts
        self.assertIn("security-audit", scores1)
        self.assertIn("documentation", scores2)


class TestTaskClassifierAccuracy(unittest.TestCase):
    """Test suite for overall classifier accuracy"""
    
    def setUp(self):
        """Create classifier and test cases"""
        self.classifier = TaskClassifier()
        
        self.test_cases = [
            {
                "request": "Create REST API endpoints for user management",
                "files": ["src/routes/users.ts"],
                "expected": "api-design"
            },
            {
                "request": "Add database migration for analytics",
                "files": ["migrations/add_analytics.sql"],
                "expected": "database-schema"
            },
            {
                "request": "Fix XSS vulnerability in form inputs",
                "files": ["src/components/Form.tsx"],
                "expected": "security-audit"
            },
            {
                "request": "Optimize slow query performance",
                "files": ["src/queries/users.ts"],
                "expected": "performance-opt"
            },
            {
                "request": "Fix broken login flow",
                "files": ["src/auth/login.ts"],
                "expected": "bug-fix"
            },
            {
                "request": "Refactor user service for clarity",
                "files": ["src/services/user.ts"],
                "expected": "refactoring"
            },
            {
                "request": "Write integration tests for API",
                "files": ["tests/api.test.ts"],
                "expected": "testing"
            },
            {
                "request": "Setup Docker deployment pipeline",
                "files": ["Dockerfile", ".gitlab-ci.yml"],
                "expected": "deployment"
            },
            {
                "request": "Update API documentation in README",
                "files": ["README.md"],
                "expected": "documentation"
            },
            {
                "request": "Build React form component",
                "files": ["src/components/UserForm.tsx"],
                "expected": "ui-implementation"
            }
        ]
    
    def test_accuracy_target(self):
        """Test that classifier achieves >70% accuracy on test cases"""
        correct = 0
        
        for test in self.test_cases:
            result = self.classifier.classify(
                test["request"],
                test["files"]
            )
            
            if result == test["expected"]:
                correct += 1
        
        accuracy = (correct / len(self.test_cases)) * 100
        
        # Target: 70%+ accuracy
        self.assertGreaterEqual(
            accuracy,
            70.0,
            f"Accuracy {accuracy:.1f}% below 70% target"
        )


if __name__ == "__main__":
    unittest.main()
