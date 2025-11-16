#!/usr/bin/env python3
"""
Wrapper for Anthropic's artifacts-builder skill.
Integrates artifact creation with oak agent workflows.

Usage:
    from skills.artifacts_builder import invoke_artifact_skill

    result = invoke_artifact_skill(
        artifact_name="my-app",
        requirements="Create a todo list with React",
        mode="standard"
    )
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional, Literal


class ArtifactBuilderSkill:
    """Interface to artifacts-builder skill from Anthropic."""

    def __init__(self, skill_path: Optional[Path] = None):
        """
        Initialize artifact builder skill.

        Args:
            skill_path: Path to artifacts-builder skill directory.
                       Defaults to ~/Projects/claude-oak-agents/skills/artifacts-builder
        """
        if skill_path is None:
            # Default to oak skills directory
            oak_root = Path.home() / "Projects" / "claude-oak-agents"
            skill_path = oak_root / "skills" / "artifacts-builder"

        self.skill_path = Path(skill_path)
        self.scripts_path = self.skill_path / "scripts"

        if not self.scripts_path.exists():
            raise FileNotFoundError(
                f"Artifacts-builder scripts not found at {self.scripts_path}. "
                "Run: cp -r /tmp/skills/artifacts-builder/scripts/ skills/artifacts-builder/"
            )

    def validate_environment(self) -> Dict[str, any]:
        """
        Ensure Node.js 18+ and required tools available.

        Returns:
            Dict with status and any warnings
        """
        warnings = []

        try:
            # Check Node version
            result = subprocess.run(
                ["node", "-v"],
                capture_output=True,
                text=True,
                check=True
            )
            version_str = result.stdout.strip().split('v')[1]
            version = int(version_str.split('.')[0])

            if version < 18:
                return {
                    "valid": False,
                    "error": f"Node.js 18+ required, found {version}"
                }
            elif version < 20:
                warnings.append(f"Node {version} detected. Node 20+ recommended for latest Vite.")

        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                "valid": False,
                "error": "Node.js not found. Install Node.js 18+ first."
            }

        # Check pnpm (will be auto-installed by init script if missing)
        try:
            subprocess.run(["which", "pnpm"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            warnings.append("pnpm not found. Will be installed automatically.")

        return {
            "valid": True,
            "warnings": warnings,
            "node_version": version
        }

    def initialize_artifact(
        self,
        project_name: str,
        working_dir: Optional[Path] = None
    ) -> Dict[str, any]:
        """
        Initialize new artifact project using init-artifact.sh

        Args:
            project_name: Name for the artifact project
            working_dir: Directory to create project in (default: current dir)

        Returns:
            Dict with status, project_path, and any messages
        """
        # Validate environment first
        env_check = self.validate_environment()
        if not env_check["valid"]:
            return {
                "status": "error",
                "error": env_check["error"]
            }

        init_script = self.scripts_path / "init-artifact.sh"
        if not init_script.exists():
            return {
                "status": "error",
                "error": f"init-artifact.sh not found at {init_script}"
            }

        work_dir = working_dir or Path.cwd()

        try:
            print(f"🚀 Initializing artifact project: {project_name}")
            result = subprocess.run(
                ["bash", str(init_script), project_name],
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                project_path = work_dir / project_name
                return {
                    "status": "success",
                    "project_path": str(project_path),
                    "message": f"✅ Artifact project '{project_name}' initialized",
                    "warnings": env_check.get("warnings", []),
                    "output": result.stdout
                }
            else:
                return {
                    "status": "error",
                    "error": "Initialization failed",
                    "stderr": result.stderr,
                    "stdout": result.stdout
                }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": "Initialization timeout (5 min exceeded)"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}"
            }

    def bundle_artifact(self, project_path: Path) -> Dict[str, any]:
        """
        Bundle artifact to single HTML using bundle-artifact.sh

        Args:
            project_path: Path to artifact project directory

        Returns:
            Dict with status, bundle_path, bundle_size_kb, and messages
        """
        project_path = Path(project_path)

        if not project_path.exists():
            return {
                "status": "error",
                "error": f"Project path does not exist: {project_path}"
            }

        if not (project_path / "package.json").exists():
            return {
                "status": "error",
                "error": f"Not a valid project (no package.json): {project_path}"
            }

        bundle_script = self.scripts_path / "bundle-artifact.sh"
        if not bundle_script.exists():
            return {
                "status": "error",
                "error": f"bundle-artifact.sh not found at {bundle_script}"
            }

        try:
            print(f"📦 Bundling artifact to single HTML...")
            result = subprocess.run(
                ["bash", str(bundle_script)],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=180  # 3 minute timeout
            )

            if result.returncode == 0:
                bundle_path = project_path / "bundle.html"

                if not bundle_path.exists():
                    return {
                        "status": "error",
                        "error": "Bundle completed but bundle.html not found",
                        "stdout": result.stdout
                    }

                bundle_size = bundle_path.stat().st_size
                bundle_size_kb = round(bundle_size / 1024, 2)

                # Determine bundle size status
                if bundle_size_kb < 500:
                    size_status = "optimal"
                elif bundle_size_kb < 1024:
                    size_status = "acceptable"
                elif bundle_size_kb < 2048:
                    size_status = "large"
                else:
                    size_status = "excessive"

                return {
                    "status": "success",
                    "bundle_path": str(bundle_path),
                    "bundle_size_kb": bundle_size_kb,
                    "bundle_size_status": size_status,
                    "message": f"✅ Artifact bundled successfully ({bundle_size_kb} KB - {size_status})",
                    "output": result.stdout
                }
            else:
                return {
                    "status": "error",
                    "error": "Bundling failed",
                    "stderr": result.stderr,
                    "stdout": result.stdout
                }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": "Bundling timeout (3 min exceeded)"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}"
            }

    def create_artifact(
        self,
        name: str,
        requirements: str,
        auto_bundle: bool = True,
        working_dir: Optional[Path] = None
    ) -> Dict[str, any]:
        """
        Full artifact creation workflow.

        1. Initialize project
        2. Provide development guidance
        3. Bundle to HTML (if auto_bundle=True)

        Args:
            name: Artifact project name
            requirements: User requirements for artifact
            auto_bundle: Whether to auto-bundle (False for development mode)
            working_dir: Directory to create project in

        Returns:
            Dict with complete workflow results
        """
        # Step 1: Initialize
        init_result = self.initialize_artifact(name, working_dir)
        if init_result["status"] != "success":
            return init_result

        project_path = Path(init_result["project_path"])

        # Step 2: Development guidance
        development_guidance = self._generate_dev_guidance(requirements, project_path)

        # Step 3: Bundle (if auto_bundle enabled)
        if auto_bundle:
            bundle_result = self.bundle_artifact(project_path)
            return {
                **init_result,
                **bundle_result,
                "development_guidance": development_guidance,
                "workflow": "complete"
            }

        return {
            **init_result,
            "development_guidance": development_guidance,
            "next_step": "Implement features in project, then run bundle_artifact()",
            "workflow": "development"
        }

    def _generate_dev_guidance(self, requirements: str, project_path: Path) -> str:
        """Generate development guidance based on requirements."""
        return f"""
🎯 Development Guidance
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Project: {project_path.name}
📍 Location: {project_path}

🚀 Quick Start:
1. cd {project_path}
2. pnpm dev (starts dev server on http://localhost:5173)
3. Implement features using shadcn/ui components
4. When ready: bash ../../skills/artifacts-builder/scripts/bundle-artifact.sh

📦 Available shadcn/ui Components (40+):
- Layout: Card, Separator, ScrollArea, Sheet
- Forms: Button, Input, Checkbox, Select, Textarea, Switch, Slider
- Data: Table, Badge, Avatar, Progress
- Overlays: Dialog, Popover, Tooltip
- Navigation: Tabs, Menubar
- Feedback: Alert, Toast

📝 Import Pattern:
import {{ Button }} from '@/components/ui/button'
import {{ Card, CardHeader, CardTitle, CardContent }} from '@/components/ui/card'

🎨 Design Guidelines (Avoid "AI Slop"):
- ❌ Excessive centered layouts
- ❌ Purple gradients everywhere
- ❌ Uniform rounded corners
- ❌ Inter font as default
- ✅ Varied, intentional layouts
- ✅ Purpose-driven color schemes
- ✅ Contextual styling

📋 Requirements to Implement:
{requirements}

🧪 Testing:
- Dev server: pnpm dev
- Type check: pnpm exec tsc --noEmit
- Build check: pnpm build

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def invoke_artifact_skill(
    artifact_name: str,
    requirements: str,
    mode: Literal["standard", "development"] = "standard",
    working_dir: Optional[Path] = None
) -> Dict[str, any]:
    """
    Convenience function for invoking artifacts-builder skill.

    Args:
        artifact_name: Name for the artifact project
        requirements: User requirements description
        mode: "standard" (auto-bundle) or "development" (manual bundling)
        working_dir: Directory to create project in

    Returns:
        Dict with workflow results

    Example:
        >>> result = invoke_artifact_skill(
        ...     artifact_name="todo-app",
        ...     requirements="Create a todo list with checkboxes and local storage",
        ...     mode="standard"
        ... )
        >>> print(result["status"])
        success
        >>> print(result["bundle_path"])
        /path/to/todo-app/bundle.html
    """
    skill = ArtifactBuilderSkill()
    auto_bundle = (mode == "standard")

    return skill.create_artifact(
        name=artifact_name,
        requirements=requirements,
        auto_bundle=auto_bundle,
        working_dir=working_dir
    )


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python artifacts_builder.py <artifact-name> <requirements>")
        print("Example: python artifacts_builder.py todo-app 'Create a todo list'")
        sys.exit(1)

    artifact_name = sys.argv[1]
    requirements = " ".join(sys.argv[2:])

    print(f"🎨 Creating artifact: {artifact_name}")
    print(f"📋 Requirements: {requirements}\n")

    result = invoke_artifact_skill(
        artifact_name=artifact_name,
        requirements=requirements,
        mode="standard"
    )

    if result["status"] == "success":
        print(f"\n✅ Success!")
        print(f"📄 Bundle: {result['bundle_path']}")
        print(f"📊 Size: {result['bundle_size_kb']} KB ({result['bundle_size_status']})")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
        sys.exit(1)
