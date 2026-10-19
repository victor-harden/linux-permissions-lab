#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
for f in scripts/*.sh; do bash -n "$f"; done
python3 -m unittest discover -s tests -v
echo "shell + python checks passed"
