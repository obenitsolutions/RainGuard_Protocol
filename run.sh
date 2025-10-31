#!/bin/bash
# Simple run script for RainGuard Protocol Simulation

echo "=================================="
echo "RainGuard Protocol Simulation"
echo "=================================="
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source /Users/macbookpro/Documents/projects/tensorflow/.venv/bin/activate

# Navigate to simulation directory
cd "$(dirname "$0")"

# Run the simulation
echo "Starting simulation server..."
echo "Dashboard will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py

