#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOLUTION="$SCRIPT_DIR/SOLUTION.md"

if [ ! -f "$SOLUTION" ]; then
  echo "SOLUTION.md not found. Please create it with your three answers." >&2
  exit 1
fi

cat "$SOLUTION"
