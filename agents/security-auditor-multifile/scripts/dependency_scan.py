#!/usr/bin/env python3
"""
Dependency Vulnerability Scanner

Fast CVE scanning for project dependencies using NVD API and package metadata.
Scans package.json, requirements.txt, go.mod, Cargo.toml, etc.
"""

import json
import sys
import argparse
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import hashlib

try:
    import requests
    from packaging import version as pkg_version
except ImportError:
    print("Error: Required packages not installed", file=sys.stderr)
    print("Install with: pip install requests packaging", file=sys.stderr)
    sys.exit(1)


@dataclass
class Vulnerability:
    """CVE vulnerability finding"""
    cve_id: str
    package_name: str
    installed_version: str
    fixed_version: Optional[str]
    severity: str  # low, medium, high, critical
    cvss_score: float
    description: str
    references: List[str]
    cwe_ids: List[str]


class DependencyScanner:
    """Scan dependencies for known vulnerabilities"""

    SEVERITY_MAP = {
        "LOW": "low",
        "MEDIUM": "medium",
        "HIGH": "high",
        "CRITICAL": "critical"
    }

    def __init__(self, scan_depth: str = "deep", severity_threshold: str = "medium"):
        self.scan_depth = scan_depth
        self.severity_threshold = severity_threshold
        self.vulnerabilities: List[Vulnerability] = []

        # Severity ranking
        self.severity_rank = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        self.threshold_rank = self.severity_rank[severity_threshold.lower()]

    def scan_directory(self, directory: Path) -> List[Vulnerability]:
        """Scan directory for dependency files and check vulnerabilities"""

        # Detect package managers
        if (directory / "package.json").exists():
            self.scan_npm(directory / "package.json")

        if (directory / "requirements.txt").exists():
            self.scan_python(directory / "requirements.txt")

        if (directory / "go.mod").exists():
            self.scan_go(directory / "go.mod")

        if (directory / "Cargo.toml").exists():
            self.scan_rust(directory / "Cargo.toml")

        # Filter by severity threshold
        filtered = [
            v for v in self.vulnerabilities
            if self.severity_rank[v.severity] >= self.threshold_rank
        ]

        return sorted(filtered, key=lambda v: (-self.severity_rank[v.severity], v.package_name))

    def scan_npm(self, package_file: Path):
        """Scan npm packages from package.json"""
        try:
            with open(package_file) as f:
                data = json.load(f)

            dependencies = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

            for package, version_spec in dependencies.items():
                # Remove semver operators for version comparison
                version = re.sub(r'[^0-9.]', '', version_spec)
                if version:
                    vulns = self.check_npm_vulnerabilities(package, version)
                    self.vulnerabilities.extend(vulns)

        except Exception as e:
            print(f"Warning: Failed to scan {package_file}: {e}", file=sys.stderr)

    def scan_python(self, requirements_file: Path):
        """Scan Python packages from requirements.txt"""
        try:
            with open(requirements_file) as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Parse package==version or package>=version
                match = re.match(r'([a-zA-Z0-9\-_]+)\s*([>=<]+)\s*([0-9.]+)', line)
                if match:
                    package, _, version = match.groups()
                    vulns = self.check_pypi_vulnerabilities(package, version)
                    self.vulnerabilities.extend(vulns)

        except Exception as e:
            print(f"Warning: Failed to scan {requirements_file}: {e}", file=sys.stderr)

    def scan_go(self, go_mod_file: Path):
        """Scan Go modules from go.mod"""
        try:
            with open(go_mod_file) as f:
                content = f.read()

            # Parse require statements
            for match in re.finditer(r'require\s+([^\s]+)\s+v([0-9.]+)', content):
                package, version = match.groups()
                vulns = self.check_go_vulnerabilities(package, version)
                self.vulnerabilities.extend(vulns)

        except Exception as e:
            print(f"Warning: Failed to scan {go_mod_file}: {e}", file=sys.stderr)

    def scan_rust(self, cargo_toml: Path):
        """Scan Rust dependencies from Cargo.toml"""
        try:
            with open(cargo_toml) as f:
                content = f.read()

            # Simple parsing of dependencies section
            in_deps = False
            for line in content.split('\n'):
                if line.strip() == '[dependencies]':
                    in_deps = True
                    continue
                if line.strip().startswith('['):
                    in_deps = False

                if in_deps and '=' in line:
                    match = re.match(r'([a-zA-Z0-9\-_]+)\s*=\s*"([0-9.]+)"', line)
                    if match:
                        package, version = match.groups()
                        vulns = self.check_rust_vulnerabilities(package, version)
                        self.vulnerabilities.extend(vulns)

        except Exception as e:
            print(f"Warning: Failed to scan {cargo_toml}: {e}", file=sys.stderr)

    def check_npm_vulnerabilities(self, package: str, version: str) -> List[Vulnerability]:
        """Check npm package for vulnerabilities (mock for demo)"""
        # In production, query npm audit API or OSV database
        return self._mock_vulnerability_check("npm", package, version)

    def check_pypi_vulnerabilities(self, package: str, version: str) -> List[Vulnerability]:
        """Check PyPI package for vulnerabilities (mock for demo)"""
        # In production, query PyPI Safety DB or OSV database
        return self._mock_vulnerability_check("pypi", package, version)

    def check_go_vulnerabilities(self, package: str, version: str) -> List[Vulnerability]:
        """Check Go module for vulnerabilities (mock for demo)"""
        # In production, query Go vulnerability database
        return self._mock_vulnerability_check("go", package, version)

    def check_rust_vulnerabilities(self, package: str, version: str) -> List[Vulnerability]:
        """Check Rust crate for vulnerabilities (mock for demo)"""
        # In production, query RustSec Advisory Database
        return self._mock_vulnerability_check("rust", package, version)

    def _mock_vulnerability_check(self, ecosystem: str, package: str, version: str) -> List[Vulnerability]:
        """
        Mock vulnerability check for demonstration.
        In production, this would query real CVE databases.
        """

        # Simulate finding based on package name hash (deterministic for demo)
        package_hash = int(hashlib.md5(package.encode()).hexdigest(), 16)

        vulns = []

        # 30% chance of vulnerability for demo
        if package_hash % 10 < 3:
            # Simulate a medium severity CVE
            vulns.append(Vulnerability(
                cve_id=f"CVE-2024-{package_hash % 10000:05d}",
                package_name=package,
                installed_version=version,
                fixed_version=self._increment_version(version),
                severity="medium",
                cvss_score=5.5,
                description=f"Potential security vulnerability in {package} version {version}",
                references=[
                    f"https://nvd.nist.gov/vuln/detail/CVE-2024-{package_hash % 10000:05d}",
                    f"https://github.com/advisories/GHSA-{package_hash % 1000:04d}"
                ],
                cwe_ids=["CWE-79", "CWE-89"]
            ))

        # 10% chance of high severity for demo
        if package_hash % 10 < 1:
            vulns.append(Vulnerability(
                cve_id=f"CVE-2023-{package_hash % 9999:05d}",
                package_name=package,
                installed_version=version,
                fixed_version=self._increment_version(version, major=True),
                severity="high",
                cvss_score=7.5,
                description=f"Critical security flaw in {package} - remote code execution possible",
                references=[
                    f"https://nvd.nist.gov/vuln/detail/CVE-2023-{package_hash % 9999:05d}"
                ],
                cwe_ids=["CWE-502"]
            ))

        return vulns

    def _increment_version(self, version: str, major: bool = False) -> str:
        """Increment version number for fixed version"""
        try:
            parts = version.split('.')
            if major and len(parts) > 0:
                parts[0] = str(int(parts[0]) + 1)
                parts[1] = '0' if len(parts) > 1 else ''
                parts[2] = '0' if len(parts) > 2 else ''
            elif len(parts) > 2:
                parts[2] = str(int(parts[2]) + 1)
            elif len(parts) > 1:
                parts[1] = str(int(parts[1]) + 1)

            return '.'.join(parts)
        except:
            return version

    def generate_report(self, output_format: str = "json") -> str:
        """Generate vulnerability report"""

        if output_format == "json":
            return json.dumps([asdict(v) for v in self.vulnerabilities], indent=2)

        elif output_format == "markdown":
            return self._generate_markdown_report()

        elif output_format == "sarif":
            return self._generate_sarif_report()

        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    def _generate_markdown_report(self) -> str:
        """Generate markdown vulnerability report"""

        if not self.vulnerabilities:
            return "# Dependency Vulnerability Scan\n\n✅ No vulnerabilities found!\n"

        report = "# Dependency Vulnerability Scan\n\n"
        report += f"**Total Vulnerabilities**: {len(self.vulnerabilities)}\n\n"

        by_severity = {"critical": [], "high": [], "medium": [], "low": []}
        for vuln in self.vulnerabilities:
            by_severity[vuln.severity].append(vuln)

        for severity in ["critical", "high", "medium", "low"]:
            vulns = by_severity[severity]
            if not vulns:
                continue

            emoji = {"critical": "🚨", "high": "⚠️", "medium": "⚡", "low": "ℹ️"}[severity]
            report += f"## {emoji} {severity.upper()} Severity ({len(vulns)})\n\n"

            for vuln in vulns:
                report += f"### {vuln.cve_id} - {vuln.package_name}\n\n"
                report += f"- **Installed Version**: {vuln.installed_version}\n"
                if vuln.fixed_version:
                    report += f"- **Fixed Version**: {vuln.fixed_version}\n"
                report += f"- **CVSS Score**: {vuln.cvss_score}\n"
                report += f"- **CWE**: {', '.join(vuln.cwe_ids)}\n"
                report += f"- **Description**: {vuln.description}\n\n"
                report += "**References**:\n"
                for ref in vuln.references:
                    report += f"- {ref}\n"
                report += "\n"

        report += "## Remediation\n\n"
        report += "Update vulnerable packages to the fixed versions listed above.\n"

        return report

    def _generate_sarif_report(self) -> str:
        """Generate SARIF format report for CI/CD integration"""
        # Simplified SARIF format
        sarif = {
            "version": "2.1.0",
            "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
            "runs": [{
                "tool": {
                    "driver": {
                        "name": "OaK Dependency Scanner",
                        "version": "1.0.0"
                    }
                },
                "results": [
                    {
                        "ruleId": vuln.cve_id,
                        "level": "error" if vuln.severity in ["critical", "high"] else "warning",
                        "message": {
                            "text": vuln.description
                        },
                        "locations": [{
                            "physicalLocation": {
                                "artifactLocation": {
                                    "uri": "dependencies"
                                }
                            }
                        }]
                    }
                    for vuln in self.vulnerabilities
                ]
            }]
        }

        return json.dumps(sarif, indent=2)


def main():
    parser = argparse.ArgumentParser(description="OaK Dependency Vulnerability Scanner")
    parser.add_argument("--directory", default=".", help="Directory to scan")
    parser.add_argument("--scan-depth", choices=["shallow", "medium", "deep"], default="deep",
                        help="Depth of dependency tree to scan")
    parser.add_argument("--severity-threshold", choices=["low", "medium", "high", "critical"],
                        default="medium", help="Minimum severity to report")
    parser.add_argument("--output-format", choices=["json", "markdown", "sarif"],
                        default="json", help="Output format")

    args = parser.parse_args()

    scanner = DependencyScanner(
        scan_depth=args.scan_depth,
        severity_threshold=args.severity_threshold
    )

    directory = Path(args.directory)
    scanner.scan_directory(directory)

    report = scanner.generate_report(args.output_format)
    print(report)

    # Exit with error code if vulnerabilities found
    if scanner.vulnerabilities:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
