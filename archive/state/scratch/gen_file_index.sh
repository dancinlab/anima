#!/usr/bin/env bash
# gen_file_index.sh — regenerate the exhaustive tracked-file snapshot on demand.
#
# ARCHITECTURE.json carries the CONCEPTUAL architecture tree (subsystem roles +
# their anchor/entry/SSOT files), NOT a per-file dump — the full tracked-file
# listing is delegated to `git ls-files` so a new file never needs a manual
# leaf-node edit (anti-drift, c4). Run this to materialize a browsable snapshot.
#
# Usage:  bash state/scratch/gen_file_index.sh
# Writes: FILE_INDEX.txt (repo root) = `git ls-files | sort`
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
OUT="$ROOT/FILE_INDEX.txt"
git -C "$ROOT" ls-files | sort > "$OUT"
echo "wrote $OUT ($(wc -l < "$OUT") tracked files)"
