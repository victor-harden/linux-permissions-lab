#!/usr/bin/env bash
# Build a safe practice tree inside a temporary directory.
set -euo pipefail

BASE="${TMPDIR:-/tmp}/perm-lab"

rm -rf "$BASE"
mkdir -p "$BASE/share" "$BASE/private"

echo "public notes" > "$BASE/share/notes.txt"
echo "secret" > "$BASE/private/secret.txt"
echo "#!/bin/sh\necho practice" > "$BASE/share/run.sh"

chmod 644 "$BASE/share/notes.txt"
chmod 600 "$BASE/private/secret.txt"
chmod 755 "$BASE/share/run.sh"
chmod 1777 "$BASE/share"

echo "practice tree created at $BASE"
find "$BASE" -maxdepth 2 -printf '%M %u %g %p\n' | sort
