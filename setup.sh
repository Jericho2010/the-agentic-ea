#!/usr/bin/env bash
set -e

echo "=== Setting up The Agentic EA Platform (ZBook / uv Standard) ==="

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Install via: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Initialize virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment via uv..."
    uv venv .venv --python 3.12
fi

# Activate and install dependencies
source .venv/bin/activate
echo "Installing project dependencies via uv..."
uv pip install -e ".[dev]"

echo "=== Setup complete. Environment ready. ==="
