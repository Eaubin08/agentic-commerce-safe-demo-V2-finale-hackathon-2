#!/bin/bash
# Script to run automated test scenarios

# Set PYTHONPATH to include the project root
export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)"

# Run the test scenarios
python3 demo/test_scenarios.py
