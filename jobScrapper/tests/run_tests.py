#!/usr/bin/env python3
"""Test runner script for the job scraper application."""

import sys
import subprocess
import os
from pathlib import Path


def run_tests(test_type="all", verbose=True):
    """Run tests with specified type.
    
    Args:
        test_type: Type of tests to run ('unit', 'integration', 'all')
        verbose: Whether to run with verbose output
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Change to project root
    os.chdir(project_root)
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add verbose flag if requested
    if verbose:
        cmd.append("-v")
    
    # Add test type markers
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "webdriver":
        cmd.extend(["-m", "webdriver"])
    elif test_type == "fast":
        cmd.extend(["-m", "not slow"])
    elif test_type == "all":
        # Remove the default "not slow" filter for all tests
        if "-m" in cmd:
            cmd.remove("-m")
            cmd.remove("not slow")
    else:
        print(f"Unknown test type: {test_type}")
        print("Available types: unit, integration, webdriver, fast, all")
        return False
    
    # Add test directory
    cmd.append("tests/")
    
    # Add coverage if available
    try:
        import coverage
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])
    except ImportError:
        print("Coverage not available, running without coverage")
    
    print(f"Running command: {' '.join(cmd)}")
    print("=" * 50)
    
    # Run the tests
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print(f"❌ Tests failed with exit code: {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ pytest not found. Please install pytest:")
        print("pip install pytest")
        return False


def main():
    """Main function to run tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run job scraper tests")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "webdriver", "fast", "all"],
        default="fast",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--quiet", 
        action="store_true",
        help="Run tests in quiet mode"
    )
    
    args = parser.parse_args()
    
    success = run_tests(
        test_type=args.type,
        verbose=not args.quiet
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
