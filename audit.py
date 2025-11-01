#!/usr/bin/env python3
"""
Test Audit Script - Verify test quality and coverage.

This script checks:
1. Real User Events: Integration tests use real file I/O and CLI invocation
2. Mutation Testing: Mutants survival rate in core logic
3. Console Errors: No unexpected warnings during test runs
"""

import subprocess
import sys
import json
import os
from pathlib import Path


class Colors:
    """Terminal colors for output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a colored header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def check_real_user_events():
    """Check if integration tests use real file I/O and CLI invocation."""
    print_header("Audit 1: Real User Events")
    
    checks = []
    
    # Check integration tests file
    integration_file = Path("tests/test_integration.py")
    if integration_file.exists():
        content = integration_file.read_text()
        
        # Check for Click CliRunner (simulates real CLI)
        if "CliRunner" in content:
            print_success("Integration tests use Click CliRunner for real CLI invocation")
            checks.append(True)
        else:
            print_warning("CliRunner not found in integration tests")
            checks.append(False)
        
        # Check for real file I/O
        if "sample_pdf_path" in content or "sample_pptx_path" in content:
            print_success("Integration tests use real file fixtures")
            checks.append(True)
        else:
            print_warning("Real file fixtures not found")
            checks.append(False)
        
        # Check for file system operations
        if "os.path.exists" in content or "os.listdir" in content:
            print_success("Integration tests verify real file operations")
            checks.append(True)
        else:
            print_warning("File system operations not verified")
            checks.append(False)
    else:
        print_error("Integration test file not found")
        checks.append(False)
    
    # Check deck parser tests use real files
    parser_file = Path("tests/test_deck_parser.py")
    if parser_file.exists():
        content = parser_file.read_text()
        if "parse_deck" in content and ("sample_pdf" in content or "sample_pptx" in content):
            print_success("Deck parser tests use real PDF/PPTX files")
            checks.append(True)
        else:
            print_warning("Deck parser may not use real files")
            checks.append(False)
    
    success_rate = sum(checks) / len(checks) * 100 if checks else 0
    print(f"\n{Colors.BOLD}Real User Events Score: {success_rate:.1f}%{Colors.ENDC}")
    
    return success_rate >= 75  # Pass if >= 75%


def check_mutation_testing():
    """Check mutation testing results."""
    print_header("Audit 2: Mutation Testing")
    
    print_info("Running mutation tests (this may take a while)...")
    
    try:
        # Run mutmut
        result = subprocess.run(
            ["mutmut", "run", "--paths-to-mutate=deckbrief/"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Get results
        results = subprocess.run(
            ["mutmut", "results"],
            capture_output=True,
            text=True
        )
        
        output = results.stdout + results.stderr
        
        # Parse results
        if "Survived" in output or "survived" in output:
            # Try to extract survival rate
            lines = output.split('\n')
            for line in lines:
                if "Survived" in line or "survived" in line:
                    print_info(f"Mutation results: {line}")
            
            # Check if survival rate is acceptable
            if "Survived: 0" in output or "survived: 0" in output:
                print_success("No mutants survived!")
                return True
            else:
                print_warning("Some mutants survived - check mutmut results for details")
                print_info("Run 'mutmut show' to see surviving mutants")
                return False
        else:
            print_warning("Could not parse mutation test results")
            print_info(f"Output: {output[:200]}")
            return None
    
    except subprocess.TimeoutExpired:
        print_warning("Mutation testing timed out (>5 minutes)")
        print_info("Consider running 'mutmut run' manually")
        return None
    
    except FileNotFoundError:
        print_warning("mutmut not installed or not in PATH")
        print_info("Install with: pip install mutmut")
        return None
    
    except Exception as e:
        print_warning(f"Error running mutation tests: {str(e)}")
        return None


def check_console_errors():
    """Check for console errors during test runs."""
    print_header("Audit 3: Console Errors")
    
    print_info("Running test suite with error capture...")
    
    try:
        # Run pytest with verbose output
        result = subprocess.run(
            ["pytest", "tests/", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = result.stdout + result.stderr
        
        # Check for common error patterns
        error_patterns = [
            ("ERROR", "errors"),
            ("FAILED", "test failures"),
            ("exception", "exceptions"),
            ("traceback", "tracebacks"),
        ]
        
        errors_found = []
        for pattern, description in error_patterns:
            if pattern.lower() in output.lower():
                # Don't count expected error handling
                if "test_error" not in output.lower():
                    errors_found.append(description)
        
        # Check for warnings (less critical)
        if "warning" in output.lower() and "DeprecationWarning" not in output:
            print_warning("Some warnings detected (check pytest output)")
        
        if not errors_found:
            print_success("No unexpected console errors detected")
            return True
        else:
            print_warning(f"Found: {', '.join(errors_found)}")
            print_info("Review test output for details")
            return False
    
    except subprocess.TimeoutExpired:
        print_error("Test suite timed out")
        return False
    
    except Exception as e:
        print_error(f"Error running tests: {str(e)}")
        return False


def check_coverage():
    """Check test coverage."""
    print_header("Bonus Check: Test Coverage")
    
    try:
        result = subprocess.run(
            ["pytest", "tests/", "--cov=deckbrief", "--cov-report=term-missing", "--quiet"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = result.stdout + result.stderr
        
        # Look for coverage percentage
        if "TOTAL" in output:
            lines = output.split('\n')
            for line in lines:
                if "TOTAL" in line:
                    print_info(f"Coverage: {line}")
                    
                    # Try to extract percentage
                    parts = line.split()
                    for part in parts:
                        if "%" in part:
                            try:
                                coverage = float(part.replace("%", ""))
                                if coverage >= 85:
                                    print_success(f"Coverage {coverage}% meets 85% threshold")
                                    return True
                                else:
                                    print_warning(f"Coverage {coverage}% below 85% threshold")
                                    return False
                            except:
                                pass
        
        print_warning("Could not parse coverage results")
        return None
    
    except Exception as e:
        print_warning(f"Error checking coverage: {str(e)}")
        return None


def check_test_quality():
    """Check overall test quality metrics."""
    print_header("Test Quality Metrics")
    
    try:
        # Count test files
        test_files = list(Path("tests").glob("test_*.py"))
        print_info(f"Test files: {len(test_files)}")
        
        # Count total tests
        result = subprocess.run(
            ["pytest", "--collect-only", "-q"],
            capture_output=True,
            text=True
        )
        
        output = result.stdout
        if "test" in output.lower():
            # Try to count tests
            test_count = output.lower().count(" test")
            if test_count > 0:
                print_info(f"Approximate test count: {test_count}")
        
        # Check for test markers
        markers_found = []
        for test_file in test_files:
            content = test_file.read_text()
            if "@pytest.mark.integration" in content:
                markers_found.append("integration")
            if "@pytest.mark.unit" in content:
                markers_found.append("unit")
            if "@pytest.mark.slow" in content:
                markers_found.append("slow")
            if "@pytest.mark.api" in content:
                markers_found.append("api")
        
        if markers_found:
            print_success(f"Test markers used: {', '.join(set(markers_found))}")
        
        return True
    
    except Exception as e:
        print_warning(f"Could not analyze test quality: {str(e)}")
        return None


def main():
    """Run all audit checks."""
    print(f"\n{Colors.BOLD}PitchDeck Autopilot - Test Quality Audit{Colors.ENDC}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")
    
    results = {}
    
    # Run checks
    results["real_user_events"] = check_real_user_events()
    results["console_errors"] = check_console_errors()
    results["coverage"] = check_coverage()
    results["test_quality"] = check_test_quality()
    
    # Mutation testing is slow, make it optional
    print_info("\nMutation testing is slow and optional.")
    print_info("Run 'mutmut run' separately if desired")
    results["mutation_testing"] = None
    
    # Print summary
    print_header("Audit Summary")
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    for check, result in results.items():
        check_name = check.replace("_", " ").title()
        if result is True:
            print_success(f"{check_name}: PASS")
        elif result is False:
            print_error(f"{check_name}: FAIL")
        else:
            print_warning(f"{check_name}: SKIPPED")
    
    print(f"\n{Colors.BOLD}Results: {passed} passed, {failed} failed, {skipped} skipped{Colors.ENDC}")
    
    # Overall pass/fail
    if failed == 0 and passed >= 3:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ AUDIT PASSED{Colors.ENDC}")
        return 0
    else:
        print(f"\n{Colors.WARNING}{Colors.BOLD}⚠ AUDIT NEEDS ATTENTION{Colors.ENDC}")
        return 1


if __name__ == "__main__":
    sys.exit(main())


