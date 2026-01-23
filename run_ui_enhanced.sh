#!/bin/bash
# Script to run the enhanced Streamlit UI demo

# Set PYTHONPATH to include the project root
export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)"

# Run Streamlit with enhanced UI
streamlit run ui/app_enhanced.py
