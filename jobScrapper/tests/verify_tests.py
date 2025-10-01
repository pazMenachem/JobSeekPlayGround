#!/usr/bin/env python3
"""Verify that all tests can be discovered and run."""

import sys
import subprocess
from pathlib import Path


def verify_test_discovery():
    """Verify that pytest can discover all tests."""
    print("🔍 Verifying test discovery...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "--collect-only", 
            "-q"
        ], capture_output=True, text=True, check=True)
        
        # Count discovered tests
        lines = result.stdout.split('\n')
        test_count = len([line for line in lines if 'test_' in line and 'PASSED' not in line and 'FAILED' not in line])
        
        print(f"✅ Discovered {test_count} tests")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Test discovery failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def verify_imports():
    """Verify that all test modules can be imported."""
    print("📦 Verifying test imports...")
    
    test_files = [
        "tests.test_config",
        "tests.test_job_scraper", 
        "tests.test_webdriver_manager",
        "tests.test_url_manager",
        "tests.test_results_manager",
        "tests.test_app_manager",
        "tests.test_integration"
    ]
    
    failed_imports = []
    
    for module in test_files:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ Failed to import {len(failed_imports)} modules")
        return False
    else:
        print("✅ All test modules imported successfully")
        return True


def verify_fixtures():
    """Verify that test fixtures are working."""
    print("🔧 Verifying test fixtures...")
    
    try:
        # Test that conftest.py can be imported
        import tests.conftest
        print("  ✅ conftest.py imported successfully")
        
        # Test that fixtures are available
        from tests.conftest import mock_driver, temp_dir, sample_keywords
        print("  ✅ Key fixtures available")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Fixture import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Fixture verification failed: {e}")
        return False


def verify_test_data():
    """Verify that test data files exist."""
    print("📄 Verifying test data...")
    
    test_data_dir = Path("tests/fixtures")
    test_html = test_data_dir / "test_job_page.html"
    
    if not test_data_dir.exists():
        print(f"  ❌ Test data directory not found: {test_data_dir}")
        return False
    
    if not test_html.exists():
        print(f"  ❌ Test HTML file not found: {test_html}")
        return False
    
    print(f"  ✅ Test data directory: {test_data_dir}")
    print(f"  ✅ Test HTML file: {test_html}")
    return True


def run_quick_tests():
    """Run a quick subset of tests to verify they work."""
    print("🏃 Running quick test verification...")
    
    try:
        # Run only unit tests that don't require external dependencies
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/test_config.py",
            "-v",
            "--tb=short"
        ], capture_output=True, text=True, check=True)
        
        print("✅ Quick tests passed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Quick tests failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main verification function."""
    print("🧪 Job Scraper Test Suite Verification")
    print("=" * 50)
    
    checks = [
        ("Test Discovery", verify_test_discovery),
        ("Test Imports", verify_imports),
        ("Test Fixtures", verify_fixtures),
        ("Test Data", verify_test_data),
        ("Quick Tests", run_quick_tests)
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} failed with exception: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 Verification Summary:")
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All verifications passed! Test suite is ready.")
        return True
    else:
        print("⚠️  Some verifications failed. Check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
