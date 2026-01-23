#!/bin/bash
# Script to run interactive CLI demo

# Set PYTHONPATH to include the project root
export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)"

# Run the interactive demo
python3 demo/interactive_demo.py
