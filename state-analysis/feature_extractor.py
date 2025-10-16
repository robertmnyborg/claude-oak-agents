#!/usr/bin/env python3
"""
Feature Extractor for State Analysis

Utilities to extract state features from codebases for OaK architecture.
"""

import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


class FeatureExtractor:
    """Extracts state features from a codebase."""

    def __init__(self, workspace_dir: Optional[Path] = None):
        """
        Initialize feature extractor.

        Args:
            workspace_dir: Root directory of the workspace to analyze.
                          Defaults to current working directory.
        """
        self.workspace_dir = Path(workspace_dir or os.getcwd())

    def extract_all_features(self) -> Dict[str, Any]:
        """
        Extract all state features.

        Returns:
            Dictionary with codebase, context, and other features
        """
        return {
            "codebase": self.extract_codebase_features(),
            "context": self.extract_context_features()
        }

    def extract_codebase_features(self) -> Dict[str, Any]:
        """Extract features about the codebase itself."""
        languages = self.detect_languages()
        frameworks = self.detect_frameworks()
        loc, file_count = self.count_loc_and_files()
        architecture = self.detect_architecture()

        return {
            "languages": languages,
            "frameworks": frameworks,
            "loc": loc,
            "file_count": file_count,
            "complexity": self.estimate_complexity(loc, file_count),
            "architecture": architecture
        }

    def detect_languages(self) -> List[str]:
        """
        Detect programming languages in the workspace.

        Returns:
            List of detected languages, sorted by prevalence
        """
        extension_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "TypeScript",
            ".jsx": "JavaScript",
            ".java": "Java",
            ".go": "Go",
            ".rs": "Rust",
            ".rb": "Ruby",
            ".php": "PHP",
            ".cs": "C#",
            ".cpp": "C++",
            ".c": "C",
            ".h": "C/C++",
            ".swift": "Swift",
            ".kt": "Kotlin",
            ".scala": "Scala",
            ".r": "R",
            ".m": "Objective-C",
            ".sh": "Shell",
            ".sql": "SQL"
        }

        extension_counts = Counter()

        for root, _, files in os.walk(self.workspace_dir):
            # Skip common directories
            if any(skip in root for skip in [".git", "node_modules", "venv", "__pycache__", "build", "dist"]):
                continue

            for file in files:
                ext = Path(file).suffix.lower()
                if ext in extension_map:
                    extension_counts[extension_map[ext]] += 1

        # Return languages sorted by file count
        return [lang for lang, _ in extension_counts.most_common(5)]

    def detect_frameworks(self) -> List[str]:
        """
        Detect frameworks and major libraries.

        Returns:
            List of detected frameworks
        """
        frameworks = []

        # Package managers and config files
        package_files = {
            "package.json": self._detect_npm_frameworks,
            "requirements.txt": self._detect_python_frameworks,
            "pyproject.toml": self._detect_python_frameworks,
            "Gemfile": self._detect_ruby_frameworks,
            "go.mod": self._detect_go_frameworks,
            "Cargo.toml": self._detect_rust_frameworks,
            "pom.xml": lambda _: ["Maven", "Java"],
            "build.gradle": lambda _: ["Gradle", "Java"]
        }

        for filename, detector in package_files.items():
            filepath = self.workspace_dir / filename
            if filepath.exists():
                try:
                    detected = detector(filepath)
                    frameworks.extend(detected)
                except Exception:
                    pass

        return list(set(frameworks))  # Remove duplicates

    def _detect_npm_frameworks(self, filepath: Path) -> List[str]:
        """Detect frameworks from package.json."""
        frameworks = []
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

            framework_map = {
                "react": "React",
                "vue": "Vue",
                "angular": "Angular",
                "next": "Next.js",
                "express": "Express",
                "fastify": "Fastify",
                "nest": "NestJS",
                "typescript": "TypeScript",
                "jest": "Jest",
                "vitest": "Vitest",
                "webpack": "Webpack",
                "vite": "Vite"
            }

            for dep_key, framework_name in framework_map.items():
                if any(dep_key in dep for dep in deps.keys()):
                    frameworks.append(framework_name)

        except Exception:
            pass

        return frameworks

    def _detect_python_frameworks(self, filepath: Path) -> List[str]:
        """Detect frameworks from Python dependencies."""
        frameworks = []
        try:
            content = filepath.read_text().lower()

            framework_map = {
                "django": "Django",
                "flask": "Flask",
                "fastapi": "FastAPI",
                "pytest": "pytest",
                "unittest": "unittest",
                "pandas": "Pandas",
                "numpy": "NumPy",
                "tensorflow": "TensorFlow",
                "pytorch": "PyTorch",
                "scikit-learn": "scikit-learn"
            }

            for key, name in framework_map.items():
                if key in content:
                    frameworks.append(name)

        except Exception:
            pass

        return frameworks

    def _detect_ruby_frameworks(self, filepath: Path) -> List[str]:
        """Detect Ruby frameworks."""
        frameworks = ["Ruby"]
        content = filepath.read_text().lower()
        if "rails" in content:
            frameworks.append("Rails")
        return frameworks

    def _detect_go_frameworks(self, filepath: Path) -> List[str]:
        """Detect Go frameworks."""
        return ["Go"]

    def _detect_rust_frameworks(self, filepath: Path) -> List[str]:
        """Detect Rust frameworks."""
        return ["Rust"]

    def count_loc_and_files(self) -> Tuple[int, int]:
        """
        Count lines of code and number of files.

        Returns:
            (loc, file_count) tuple
        """
        loc = 0
        file_count = 0

        code_extensions = {
            ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs",
            ".rb", ".php", ".cs", ".cpp", ".c", ".h", ".swift", ".kt"
        }

        for root, _, files in os.walk(self.workspace_dir):
            if any(skip in root for skip in [".git", "node_modules", "venv", "__pycache__", "build", "dist"]):
                continue

            for file in files:
                if Path(file).suffix.lower() in code_extensions:
                    file_count += 1
                    try:
                        filepath = Path(root) / file
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            loc += sum(1 for line in f if line.strip())
                    except Exception:
                        pass

        return loc, file_count

    def estimate_complexity(self, loc: int, file_count: int) -> str:
        """
        Estimate codebase complexity.

        Args:
            loc: Lines of code
            file_count: Number of files

        Returns:
            Complexity level: trivial, low, medium, high, very_high
        """
        if loc < 1000:
            return "trivial"
        elif loc < 5000:
            return "low"
        elif loc < 20000:
            return "medium"
        elif loc < 100000:
            return "high"
        else:
            return "very_high"

    def detect_architecture(self) -> str:
        """
        Detect architectural pattern.

        Returns:
            Architecture type
        """
        # Look for architecture indicators
        if (self.workspace_dir / "docker-compose.yml").exists():
            return "microservices"
        elif (self.workspace_dir / "serverless.yml").exists():
            return "serverless"
        elif (self.workspace_dir / "k8s").exists() or (self.workspace_dir / "kubernetes").exists():
            return "kubernetes"
        elif len(list(self.workspace_dir.glob("services/*"))) > 1:
            return "microservices"
        else:
            return "monolithic"

    def extract_context_features(self) -> Dict[str, Any]:
        """Extract features about the current context."""
        return {
            "tests_exist": self.check_tests_exist(),
            "tests_passing": self.check_tests_passing(),
            "docs_exist": self.check_docs_exist(),
            "git_clean": self.check_git_clean(),
            "dependencies_outdated": False,  # TODO: Implement
            "build_status": "unknown"  # TODO: Implement
        }

    def check_tests_exist(self) -> bool:
        """Check if test files exist."""
        test_patterns = ["*test*.py", "*.spec.ts", "*.spec.js", "*_test.go", "test_*.py"]

        for pattern in test_patterns:
            if list(self.workspace_dir.rglob(pattern)):
                return True

        return False

    def check_tests_passing(self) -> Optional[bool]:
        """
        Check if tests are passing.

        Returns:
            True if passing, False if failing, None if cannot determine
        """
        # This is a placeholder - actual implementation depends on project type
        return None

    def check_docs_exist(self) -> bool:
        """Check if documentation exists."""
        doc_files = ["README.md", "README.rst", "CONTRIBUTING.md", "docs/"]

        for doc in doc_files:
            if (self.workspace_dir / doc).exists():
                return True

        return False

    def check_git_clean(self) -> Optional[bool]:
        """
        Check if git working directory is clean.

        Returns:
            True if clean, False if dirty, None if not a git repo
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.workspace_dir,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                return len(result.stdout.strip()) == 0

        except Exception:
            pass

        return None


def main():
    """Example usage of feature extractor."""
    extractor = FeatureExtractor()

    print("Extracting features...")
    features = extractor.extract_all_features()

    print(json.dumps(features, indent=2))


if __name__ == "__main__":
    main()
