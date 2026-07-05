#!/bin/bash
# Run the throughput validation script
# Intended to be triggered by GitHub Actions every 5 minutes

set -euo pipefail

# Change to project root
cd "$(dirname "$0")/.."

# Run the Python script
echo "Running throughput validation..."
python3 validation/throughput_validation.py
echo "Validation completed."
