#!/bin/bash
# Script to run the Streamlit UI demo

# Set PYTHONPATH to include the project root
export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)"

# Run Streamlit
streamlit run ui/app.py
