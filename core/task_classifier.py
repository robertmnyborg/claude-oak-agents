#!/usr/bin/env python3
"""
Task Type Classifier for Continual Reinforcement Learning

Classifies user requests into task types for Q-learning variant selection.
Uses keyword-based classification with file path analysis.
"""

from typing import List, Dict, Optional, Tuple
from pathlib import Path
import re


class TaskClassifier:
    """
    Classifies user requests into task types for CRL variant selection.
    
    Uses rule-based keyword matching and file path analysis to determine
    the most likely task type. Target accuracy: >70%.
    """
    
    # Task type definitions with keyword patterns
    TASK_TYPES = {
        "api-design": {
            "keywords": ["api", "endpoint", "rest", "graphql", "route", "routing",
                        "controller", "handler", "middleware", "openapi", "swagger"],
            "file_patterns": [r".*routes?\..*", r".*controllers?\..*", r".*api\..*",
                            r".*endpoints?\..*", r".*handlers?\..*"],
            "weight": 1.0
        },
        "database-schema": {
            "keywords": ["database", "schema", "migration", "table", "column", "index",
                        "model", "entity", "db", "sql", "query", "orm", "sequelize",
                        "mongoose", "prisma", "typeorm"],
            "file_patterns": [r".*migrations?\..*", r".*models?\..*", r".*schema\..*",
                            r".*entities\..*", r".*\.sql$"],
            "weight": 1.0
        },
        "security-audit": {
            "keywords": ["security", "auth", "authorization", "authentication", "permission",
                        "vulnerability", "xss", "csrf", "sql injection", "owasp", "jwt",
                        "oauth", "session", "token", "encrypt", "decrypt", "sanitize"],
            "file_patterns": [r".*auth.*", r".*security.*", r".*permissions?.*"],
            "weight": 1.2  # Higher weight for security
        },
        "performance-opt": {
            "keywords": ["performance", "optimize", "optimization", "slow", "speed",
                        "cache", "caching", "redis", "memcache", "lazy load", "debounce",
                        "throttle", "memoize", "index", "query optimization"],
            "file_patterns": [r".*cache.*", r".*perf.*"],
            "weight": 1.0
        },
        "bug-fix": {
            "keywords": ["bug", "error", "fix", "broken", "failing", "crash", "exception",
                        "issue", "problem", "not working", "doesn't work", "stacktrace",
                        "debug", "troubleshoot"],
            "file_patterns": [],
            "weight": 1.0
        },
        "refactoring": {
            "keywords": ["refactor", "clean", "cleanup", "improve", "restructure",
                        "reorganize", "simplify", "modernize", "extract", "consolidate",
                        "deduplicate", "dry"],
            "file_patterns": [],
            "weight": 0.9
        },
        "testing": {
            "keywords": ["test", "testing", "coverage", "unit test", "integration test",
                        "e2e", "end-to-end", "jest", "mocha", "pytest", "junit",
                        "spec", "assertion", "mock"],
            "file_patterns": [r".*\.test\..*", r".*\.spec\..*", r".*/__tests__/.*",
                            r".*/tests?/.*"],
            "weight": 1.0
        },
        "deployment": {
            "keywords": ["deploy", "deployment", "cicd", "ci/cd", "pipeline", "docker",
                        "kubernetes", "k8s", "lambda", "serverless", "cdk", "terraform",
                        "cloudformation", "container", "build", "release"],
            "file_patterns": [r".*Dockerfile.*", r".*\.yml$", r".*\.yaml$",
                            r".*serverless\..*", r".*cdk.*", r".*terraform.*"],
            "weight": 1.0
        },
        "documentation": {
            "keywords": ["docs", "documentation", "readme", "comment", "docstring",
                        "jsdoc", "javadoc", "api docs", "guide", "tutorial",
                        "changelog", "specification"],
            "file_patterns": [r".*\.md$", r".*README.*", r".*CHANGELOG.*",
                            r".*/docs/.*"],
            "weight": 0.8
        },
        "ui-implementation": {
            "keywords": ["ui", "component", "button", "form", "input", "modal",
                        "dialog", "page", "view", "css", "style", "styling",
                        "react", "vue", "angular", "frontend", "client-side"],
            "file_patterns": [r".*\.tsx$", r".*\.jsx$", r".*\.vue$",
                            r".*components?/.*", r".*\.css$", r".*\.scss$"],
            "weight": 1.0
        }
    }
    
    def __init__(self):
        """Initialize the task classifier."""
        # Compile regex patterns for efficiency
        self._compiled_patterns: Dict[str, List[re.Pattern]] = {}
        for task_type, config in self.TASK_TYPES.items():
            self._compiled_patterns[task_type] = [
                re.compile(pattern, re.IGNORECASE)
                for pattern in config["file_patterns"]
            ]
    
    def classify(
        self,
        user_request: str,
        file_paths: Optional[List[str]] = None,
        context: Optional[Dict[str, any]] = None
    ) -> str:
        """
        Classify task type based on request text and file paths.
        
        Args:
            user_request: The user's request text
            file_paths: List of file paths involved (optional)
            context: Additional context (optional)
        
        Returns:
            Task type string or "general" if no confident match
        """
        scores = self._calculate_scores(user_request, file_paths or [])
        
        if not scores:
            return "general"
        
        # Get highest scoring task type
        best_task_type, best_score = max(scores.items(), key=lambda x: x[1])
        
        # Require minimum confidence threshold (at least 1 match)
        if best_score < 0.5:
            return "general"
        
        return best_task_type
    
    def classify_with_confidence(
        self,
        user_request: str,
        file_paths: Optional[List[str]] = None,
        context: Optional[Dict[str, any]] = None
    ) -> Tuple[str, float, Dict[str, float]]:
        """
        Classify task type and return confidence scores for all types.
        
        Args:
            user_request: The user's request text
            file_paths: List of file paths involved (optional)
            context: Additional context (optional)
        
        Returns:
            Tuple of (task_type, confidence, all_scores)
        """
        scores = self._calculate_scores(user_request, file_paths or [])
        
        if not scores:
            return ("general", 0.0, {})
        
        # Normalize scores to 0-1 range
        max_score = max(scores.values())
        normalized_scores = {
            task_type: score / max_score for task_type, score in scores.items()
        }
        
        best_task_type, confidence = max(
            normalized_scores.items(), key=lambda x: x[1]
        )
        
        return (best_task_type, confidence, normalized_scores)
    
    def _calculate_scores(
        self,
        user_request: str,
        file_paths: List[str]
    ) -> Dict[str, float]:
        """
        Calculate scores for each task type.
        
        Args:
            user_request: The user's request text
            file_paths: List of file paths
        
        Returns:
            Dictionary of task_type -> score
        """
        scores: Dict[str, float] = {}
        request_lower = user_request.lower()
        
        for task_type, config in self.TASK_TYPES.items():
            score = 0.0
            
            # Keyword matching
            keyword_matches = 0
            for keyword in config["keywords"]:
                if keyword.lower() in request_lower:
                    keyword_matches += 1
            
            # Score based on keyword density
            if keyword_matches > 0:
                # More matches = higher score, with diminishing returns
                score += min(keyword_matches * 0.5, 3.0)
            
            # File pattern matching
            file_matches = 0
            for file_path in file_paths:
                for pattern in self._compiled_patterns[task_type]:
                    if pattern.search(file_path):
                        file_matches += 1
                        break
            
            if file_matches > 0:
                score += min(file_matches * 0.8, 2.0)
            
            # Apply task type weight
            score *= config["weight"]
            
            if score > 0:
                scores[task_type] = score
        
        return scores
    
    def get_task_types(self) -> List[str]:
        """
        Get list of all supported task types.
        
        Returns:
            List of task type strings
        """
        return list(self.TASK_TYPES.keys())
    
    def add_custom_task_type(
        self,
        task_type: str,
        keywords: List[str],
        file_patterns: Optional[List[str]] = None,
        weight: float = 1.0
    ) -> None:
        """
        Add a custom task type for domain-specific classification.
        
        Args:
            task_type: Unique task type identifier
            keywords: List of keywords to match
            file_patterns: List of regex patterns for file matching
            weight: Importance weight (default 1.0)
        """
        if task_type in self.TASK_TYPES:
            raise ValueError(f"Task type '{task_type}' already exists")
        
        self.TASK_TYPES[task_type] = {
            "keywords": keywords,
            "file_patterns": file_patterns or [],
            "weight": weight
        }
        
        # Compile patterns
        self._compiled_patterns[task_type] = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in (file_patterns or [])
        ]


def main():
    """Example usage of task classifier."""
    classifier = TaskClassifier()
    
    # Test cases
    test_cases = [
        {
            "request": "Create REST API endpoints for user management",
            "files": ["src/routes/users.ts", "src/controllers/userController.ts"],
            "expected": "api-design"
        },
        {
            "request": "Add database migration for new analytics table",
            "files": ["migrations/20251119_add_analytics.sql"],
            "expected": "database-schema"
        },
        {
            "request": "Fix security vulnerability in authentication flow",
            "files": ["src/auth/jwt.ts"],
            "expected": "security-audit"
        },
        {
            "request": "Optimize slow database queries with indexing",
            "files": ["src/models/user.ts"],
            "expected": "performance-opt"
        },
        {
            "request": "Build login form component with validation",
            "files": ["src/components/LoginForm.tsx"],
            "expected": "ui-implementation"
        },
        {
            "request": "Write unit tests for user service",
            "files": ["src/services/__tests__/userService.test.ts"],
            "expected": "testing"
        }
    ]
    
    print("Task Classifier Test Results\n" + "=" * 50)
    
    correct = 0
    for i, test in enumerate(test_cases, 1):
        task_type, confidence, all_scores = classifier.classify_with_confidence(
            test["request"],
            test["files"]
        )
        
        is_correct = task_type == test["expected"]
        correct += int(is_correct)
        
        status = "✓" if is_correct else "✗"
        print(f"\n{status} Test {i}: {test['request'][:50]}...")
        print(f"  Expected: {test['expected']}")
        print(f"  Got: {task_type} (confidence: {confidence:.2f})")
        
        if not is_correct:
            print(f"  Top scores: {sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:3]}")
    
    accuracy = (correct / len(test_cases)) * 100
    print(f"\n{'=' * 50}")
    print(f"Accuracy: {accuracy:.1f}% ({correct}/{len(test_cases)})")
    print(f"Target: 70%+ - {'PASS' if accuracy >= 70 else 'FAIL'}")


if __name__ == "__main__":
    main()
