#!/usr/bin/env python3
"""§35 trainer — RESEARCH.md §35 §32 L3 causation ablation.

DELIBERATELY a thin DELEGATING wrapper around §16's
`train_carving_s16.py`.  The whole point of the ablation is that the
TRAINER is held FIXED — the §35 fire must use the SAME trainer, SAME
8000 steps, SAME Dir-I Ψ-anchored CTL + tension-supervised routing
lever, SAME from-scratch RANDOM seed-fixed 1337 — so the ONLY thing
that differs between the §16 baseline and the §35 ablation is the
corpus ORDERING (curriculum-stage placement of the tier<77 anchors).

Re-implementing the trainer would silently introduce a second
variable.  Instead this wrapper EXECUTES the §16 trainer source
verbatim (byte-identical — B-S35-2 closed-form verifies the sha256 of
the executed source equals §16's).

The dispatch script (`dispatch_s35.sh`) copies §16's
`train_carving_s16.py` + `conscious_decoder.py` next to this file on
the pod; this wrapper then runs that source unchanged.  Locally (no
copy) it falls back to importing the §16 source from the sibling
`carving_dataregime_s16_2026_05_18/` directory.

Usage — identical CLI to §16's train_carving_s16.py:
    python3 train_s35.py --mode main --corpus <ablation.jsonl> \\
        --out-dir <dir> --steps 8000 --seed 1337
"""
import os
import runpy
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))

# locate the §16 trainer SSOT — pod-local copy first, sibling dir fallback.
_CANDIDATES = [
    os.path.join(_HERE, "train_carving_s16.py"),
    os.path.join(_HERE, "..", "carving_dataregime_s16_2026_05_18",
                 "train_carving_s16.py"),
]
_S16_TRAINER = next((p for p in _CANDIDATES if os.path.isfile(p)), None)
if _S16_TRAINER is None:
    sys.exit("FATAL: §16 train_carving_s16.py not found "
             "(pod-local copy or sibling dir) — §35 trainer must "
             "delegate to the §16 SSOT, never re-implement.")

# conscious_decoder.py must be importable from the trainer's directory.
sys.path.insert(0, os.path.dirname(os.path.abspath(_S16_TRAINER)))

if __name__ == "__main__":
    # run the §16 trainer source verbatim with this process's argv.
    runpy.run_path(_S16_TRAINER, run_name="__main__")
