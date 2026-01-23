#!/bin/bash
# Script to run the CLI demo

# Set PYTHONPATH to include the project root
export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)"

# Run the demo
python3 demo/run_demo.py
