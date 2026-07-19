#!/usr/bin/env bash
# v2 — deterministic full run: C0 -> train all arms x seeds -> SEQUENTIAL gates.
# Gate order is enforced by evaluate.py itself; this script just supplies the ckpts.
set -euo pipefail
cd "$(dirname "$0")"
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-4}
SEEDS="${SEEDS:-7 11}"

echo "── C0-a/C0-c (task stream) ──"; python3 gen.py
echo "── C0-d (hand-written backward) ──"; python3 gradcheck.py --selftest

# NOSTORE first: BOLT freezes ITS trunk (that is what makes BOLT the H_9392 mirror).
for s in $SEEDS; do python3 train.py --arm NOSTORE --seed "$s"; done
for s in $SEEDS; do
  for a in COTRAIN SLOWROT BOLT; do python3 train.py --arm "$a" --seed "$s"; done
done

echo "── SEQUENTIAL gates ──"; python3 evaluate.py --seeds $SEEDS
