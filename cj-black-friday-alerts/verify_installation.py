#!/usr/bin/env python3
"""
Installation verification script.
Checks that all components are properly installed and configured.
"""

import sys
import os
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_file(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"{GREEN}✓{RESET} {description}")
        return True
    else:
        print(f"{RED}✗{RESET} {description} - Missing: {filepath}")
        return False

def check_import(module_name, description):
    """Check if a Python module can be imported."""
    try:
        __import__(module_name)
        print(f"{GREEN}✓{RESET} {description}")
        return True
    except ImportError:
        print(f"{RED}✗{RESET} {description} - Cannot import: {module_name}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists."""
    if Path(dirpath).is_dir():
        print(f"{GREEN}✓{RESET} {description}")
        return True
    else:
        print(f"{YELLOW}⚠{RESET} {description} - Will be created: {dirpath}")
        return True  # Not critical, will be auto-created

def main():
    """Run all verification checks."""
    print("=" * 70)
    print("Black Friday Tracker - Installation Verification")
    print("=" * 70)
    
    all_passed = True
    
    # Check core files
    print("\n📄 Core Application Files:")
    all_passed &= check_file("database.py", "Database module")
    all_passed &= check_file("scraper.py", "Scraper module")
    all_passed &= check_file("tracker.py", "Tracker module")
    all_passed &= check_file("app.py", "Flask API")
    all_passed &= check_file("init_products.py", "Product initialization")
    
    # Check scripts
    print("\n🔧 Scripts:")
    all_passed &= check_file("scheduler.sh", "Cron scheduler")
    all_passed &= check_file("test_scraper.py", "Test script")
    
    # Check configuration
    print("\n⚙️  Configuration:")
    all_passed &= check_file("requirements.txt", "Requirements file")
    all_passed &= check_file(".gitignore", "Git ignore file")
    
    # Check frontend
    print("\n🎨 Frontend:")
    all_passed &= check_file("static/dashboard.html", "Dashboard HTML")
    
    # Check directories
    print("\n📁 Directories:")
    check_directory("data", "Data directory")
    check_directory("static", "Static files directory")
    
    # Check Python dependencies
    print("\n🐍 Python Dependencies:")
    all_passed &= check_import("requests", "Requests library")
    all_passed &= check_import("bs4", "BeautifulSoup4")
    all_passed &= check_import("flask", "Flask")
    all_passed &= check_import("flask_cors", "Flask-CORS")
    
    # Check Python version
    print("\n🔢 Python Version:")
    py_version = sys.version_info
    if py_version >= (3, 8):
        print(f"{GREEN}✓{RESET} Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        print(f"{RED}✗{RESET} Python version too old (need 3.8+, have {py_version.major}.{py_version.minor})")
        all_passed = False
    
    # Check documentation
    print("\n📚 Documentation:")
    check_file("README.md", "README")
    check_file("QUICKSTART.md", "Quick start guide")
    check_file("DEPLOYMENT.md", "Deployment guide")
    check_file("SYSTEM_OVERVIEW.md", "System overview")
    check_file("PROJECT_SUMMARY.md", "Project summary")
    check_file("INDEX.md", "Documentation index")
    
    # Summary
    print("\n" + "=" * 70)
    if all_passed:
        print(f"{GREEN}✓ All checks passed!{RESET}")
        print("\nNext steps:")
        print("1. Run: python init_products.py")
        print("2. Run: python tracker.py")
        print("3. Run: python app.py")
        print("4. Open: http://localhost:5000")
        print("\nSee QUICKSTART.md for detailed instructions.")
        return 0
    else:
        print(f"{RED}✗ Some checks failed{RESET}")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())
