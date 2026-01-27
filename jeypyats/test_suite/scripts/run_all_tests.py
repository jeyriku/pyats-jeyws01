#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: run_all_tests.py
# This file is a part of Netalps.fr
#
# Created: 27.01.2026 10:00:00
# Author: GitHub Copilot
#
# Last Modified: 27.01.2026 18:40:44
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

#!/usr/bin/env python3
"""
Test runner script for all parser unit tests.
This script discovers and runs all unit tests in the unittest/tests directory using pytest.
"""

import unittest
import sys
import os
import logging
import time
import subprocess
from pathlib import Path
from datetime import datetime


def setup_logging():
    """
    Set up logging configuration for test execution.
    """
    # Create logger
    logger = logging.getLogger('test_runner')
    logger.setLevel(logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger


def run_all_tests():
    """
    Discover and run all unit tests using pytest.
    """
    logger = setup_logging()
    start_time = time.time()

    logger.info("Starting test execution with pytest...")
    logger.info(f"Test execution started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Get the test directory
    test_dir = Path(__file__).parent.parent / 'tests'
    logger.info(f"Test directory: {test_dir}")

    print("=" * 80)
    print("RUNNING ALL PARSER UNIT TESTS WITH PYTEST")
    print("=" * 80)
    print(f"Test directory: {test_dir}")
    print()

    # Run pytest with verbose output and colors
    pytest_cmd = [
        sys.executable, "-m", "pytest",
        str(test_dir),
        "-v",  # verbose output
        "--tb=short",  # shorter tracebacks
        "--color=yes",  # colored output
        "--durations=10",  # show 10 slowest tests
        "--strict-markers",  # strict marker validation
        "--disable-warnings"  # disable warnings for cleaner output
    ]

    logger.info(f"Running pytest command: {' '.join(pytest_cmd)}")

    try:
        # Run pytest and capture output
        result = subprocess.run(pytest_cmd, capture_output=False, text=True)

        execution_time = time.time() - start_time
        logger.info(".2f")

        print("\n" + "=" * 80)
        print("PYTEST EXECUTION SUMMARY")
        print("=" * 80)
        print(".2f")

        if result.returncode == 0:
            logger.info("All tests passed successfully! ✅")
            print("\n🎉 ALL TESTS PASSED! 🎉")
        else:
            logger.error(f"Test execution failed with return code {result.returncode} ❌")
            print(f"\n❌ TEST EXECUTION FAILED (exit code: {result.returncode}) ❌")

        return result.returncode

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Error running pytest: {e}")
        print(f"Error running pytest: {e}")
        return 1


def run_specific_test(test_module):
    """
    Run a specific test module using pytest.

    Args:
        test_module (str): Name of the test module (without .py extension)
    """
    logger = setup_logging()
    start_time = time.time()

    logger.info(f"Running specific test module with pytest: {test_module}")
    logger.info(f"Test execution started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Get the test file path
    test_file = Path(__file__).parent.parent / 'tests' / f"{test_module}.py"
    logger.info(f"Test file: {test_file}")

    if not test_file.exists():
        logger.error(f"Test file not found: {test_file}")
        print(f"Error: Test file '{test_file}' not found")
        return 1

    print("=" * 80)
    print(f"RUNNING SPECIFIC TEST MODULE: {test_module}")
    print("=" * 80)
    print(f"Test file: {test_file}")
    print()

    # Run pytest on specific file
    pytest_cmd = [
        sys.executable, "-m", "pytest",
        str(test_file),
        "-v",  # verbose output
        "--tb=short",  # shorter tracebacks
        "--color=yes",  # colored output
        "--durations=10",  # show 10 slowest tests
        "--strict-markers",  # strict marker validation
        "--disable-warnings"  # disable warnings for cleaner output
    ]

    logger.info(f"Running pytest command: {' '.join(pytest_cmd)}")

    try:
        # Run pytest and capture output
        result = subprocess.run(pytest_cmd, capture_output=False, text=True)

        execution_time = time.time() - start_time
        logger.info(".2f")

        print("\n" + "=" * 80)
        print(f"PYTEST EXECUTION SUMMARY - {test_module}")
        print("=" * 80)
        print(".2f")

        if result.returncode == 0:
            logger.info(f"Test module '{test_module}' passed successfully! ✅")
            print(f"\n🎉 TEST MODULE '{test_module}' PASSED! 🎉")
        else:
            logger.error(f"Test module '{test_module}' failed with return code {result.returncode} ❌")
            print(f"\n❌ TEST MODULE '{test_module}' FAILED (exit code: {result.returncode}) ❌")

        return result.returncode

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Error running pytest: {e}")
        print(f"Error running pytest: {e}")
        return 1


def main():
    """
    Main entry point for the test runner.
    """
    if len(sys.argv) > 1:
        # Run specific test module
        test_module = sys.argv[1]
        exit_code = run_specific_test(test_module)
    else:
        # Run all tests
        exit_code = run_all_tests()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
