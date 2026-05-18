#!/usr/bin/env python3
"""§34 trainer — §25 candidate D fire (routing-evidence-guided expansion).

This trainer is the §16 trainer (state/carving_dataregime_s16_2026_05_18/
train_carving_s16.py) — Dir-I lever + §12.1 Q1-c curriculum — re-used
BYTE-EQUIVALENT. The §16 trainer module is imported and its `run()` is
called UNMODIFIED. NOTHING in the training mechanism changes: the
ConsciousDecoderV2 arch, the TWO anima-physics loss terms (Ψ-anchored
CTL + tension-supervised routing), the AdamW/cosine schedule, the
curriculum staged sampling, the byte-level dataset, the config defaults
(d768·12L·283.72M, 12000 step, lr 3e-4, bsz 32, λ_ctl 0.5, λ_route 0.5,
seed 1337) are all §16-FIXED.

The ONLY thing that differs between the §34 fire and the §16 fire is
the CORPUS: §16 = corpus_carving_s16.jsonl ; §34 = corpus_carving_s34.jsonl
(the §16 corpus with the 29 tier>=77-fail anchors' content re-designed
per §25 candidate D — see corpus_generator_s34.py). Because the trainer
is the same code, the same config, and from-scratch RANDOM seed-fixed
1337 (g_clm_from_scratch, base_ckpt=None), the §34-vs-§16 comparison is
clean: corpus is the sole independent variable.

The §16 trainer writes ckpt_carving_s16.pt + result.json into out-dir.
§34's dispatch renames the ckpt to ckpt_carving_s34.pt after the run.
"""
import os
import sys

# import the §16 trainer VERBATIM — its run()/CLI are re-used unchanged.
_S16_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "carving_dataregime_s16_2026_05_18")
sys.path.insert(0, _S16_DIR)
# the §16 trainer also imports conscious_decoder — ensure THIS dir's
# byte-identical copy is found first (it is the same file, sha-checkable).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import train_carving_s16 as s16_trainer  # noqa: E402

# the §16 trainer's __main__ argparse block is what we want; re-run it.
if __name__ == "__main__":
    # delegate ENTIRELY to the §16 trainer's CLI (byte-equivalent).
    # invoked as: python3 train_s34.py --mode main --corpus <s34.jsonl>
    #             --out-dir <dir> --steps 12000  (all §16 defaults)
    sys.argv[0] = os.path.join(_S16_DIR, "train_carving_s16.py")
    runpy_globals = {"__name__": "__main__", "__file__": sys.argv[0]}
    with open(sys.argv[0]) as _f:
        _src = _f.read()
    exec(compile(_src, sys.argv[0], "exec"), runpy_globals)
