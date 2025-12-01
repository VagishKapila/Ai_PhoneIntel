#!/bin/bash

echo "=== Starting FASTAPI Dev Server (Debug Mode) ==="

set -x  # Print every command
set -e  # Stop if ANY command errors

# Move into backend folder
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Run with full debug logs and NO reload exclude complexity
../venv/bin/uvicorn fastapi_app.main:app \
    --host 127.0.0.1 \
    --port 8000 \
    --reload \
    --log-level debug