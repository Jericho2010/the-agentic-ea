#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d ".venv" ]; then
    echo "Environment not initialized. Running ./setup.sh..."
    ./setup.sh
fi

source .venv/bin/activate
exec python src/main.py "$@"
