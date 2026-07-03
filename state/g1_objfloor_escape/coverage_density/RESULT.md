# coverage-density (H_6185) — engine-native G1 judge · FALSIFIED-CEILING

**Fire:** vast pod 43727405 (RTX 5090 32GB, torch 2.11.0+cu128 sm_120), 2026-07-03/04.
**Question (H_6185):** does the combination-coverage corpus + adequate receptive field open
engine-native mouth-generation G1 on a G0-green 303M — i.e. is the G1 objective-floor an
ESCAPABLE data-coverage+RF bound, or a genuine ceiling?

## What was run (engine-native, terminal-eligible)

- **Trunk:** `h1129c_chat.pt` = the verified **ByteGPT 303.36M** ko/en chat trunk
  (d=1024, L=24, n_head=16, block=512, GPT-2-class full attention). *No CLM 303M G0-green
  trunk exists* (all 303M G0-green trunks are ByteGPT), and CLM-from-scratch 2000-step floors
  at G0-garble — so the RF lever was tested on ByteGPT, whose **full attention gives RF >=
  seq (512B) which subsumes the H_6185 L8 dilated-conv target (511B)**. This is the *stronger*
  RF condition, not weaker: RF is not the bottleneck here.
- **Warm-FT:** `anima train --py --arch bytegpt` (torch trainer, cli/train.py) on the
  **en_block combination-coverage corpus** (3.10MB; N=40 concepts, C(40,2) pairs, 25%
  covered @600 reps, held-out = the 10 frozen G1 gate-internal pairs UNEXPOSED =
  memorization-free), lr 2e-5, 2000 steps, `--sample proportional`. val_CE 2.08->0.171
  DESCENT (G0-preserving; lr 3e-4 default *explodes* val_CE->33 = collapse, so 2e-5 used —
  bar unchanged, this is warm-FT hygiene to keep G0-green so G1 is measurable).
- **Score:** `anima evaluate --py <ckpt>.bin --corpus en_block.txt --gen 40` — the
  **frozen gen=40 G0-G6 bar** (gen!=40 self-flags DIRECTIONAL; gen=40 = terminal).
  cli/evaluate.py is **torch-free / gauge-free numpy** (`grep -cE 'import torch|gauge_lib'`
  = 0) = engine-native, py 2-production, terminal-eligible (a_eval_py_canonical).
  Decode enters the byte mouth (core/decode.py bytegpt path), byte-identical to hexa twin.

## Results (frozen gen=40 · all G0-green = valid G1 measurement)

| ckpt | objective | G0 COHERENCE | G1 best_distinct | G1 max_single | G1 | G2 NOVELTY |
|------|-----------|--------------|------------------|---------------|-----|------------|
| base_h1129c | ce (warm-FT ctrl) | GREEN 4/5 | 1 | 1 | RED floor | GREEN novel=9 |
| **cov_en** | ce (coverage-density) | GREEN **5/5** | **1** | **1** | RED **floor** | GREEN novel=6 |

G1 escape bar (frozen, verbatim): *some k: best_distinct >=2 AND >max_single AND coherent.*
cov_en: best_distinct=1, max_single=1 -> 1 not >=2, and not >max_single -> 0/1 HIT.

## VERDICT: FALSIFIED-CEILING — coverage-density does NOT open engine-native G1

- The combination-coverage corpus + ample RF, warm-FT into a G0-green 303M byte mouth and
  scored by the frozen engine-native `--py` G1, stays **exactly at the recombination floor**
  (best_distinct=1 = the control baseline). It did not lift held-out composed-concept
  coverage to >=2. **terminal_flip: NO** — H_9120 G1 objective-floor stands (coverage-density
  is not the missing lever). Consistent with the ledger (G1 = trunk-objective floor;
  scale/data/RF = amplifiers, not levers).
- G0-green(5/5) + G2-green(novel=6) confirm the model is coherent and *does* produce
  corpus-absent n-grams (novelty != recombination, G2 != G1) — the floor is a clean
  recombination-specific ceiling, NOT undertrain.

## Honest scope (c9)

- **ByteGPT, not CLM-dilated-conv.** The *specific* CLM L4->L8 dilated-conv RF variable is
  NOT isolated (no CLM 303M G0-green trunk to warm-FT). Tested at ByteGPT full-RF instead —
  the stronger RF condition. A CLM-native RF sweep would need a CLM 303M G0-green base first.
- **Single frozen-bar pass**, not a 5-seed tally; best_distinct=1 (= baseline) leaves no
  room for a 5-seed flip.
- **Infra artifact fixed mid-fire:** the container lacked `/usr/share/dict/words` -> the G0
  known-word gate scored kwr=0 for EVERY ckpt (incl. baseline) = a *measurement* wall
  (a_break_the_wall type-a), NOT garble. Installed wamerican (104334 words) -> G0-green
  restored; the verdicts above are post-fix.

## Artifacts
- ckpt (engine-native, PULLED pre-teardown): `~/anima-weights/g1_escape/cov_en.bin` (1.213GB, ByteGPT303 .bin)
- logs: cov_en_train.log, base_train.log · verdicts: cov_en_g1.json, base_g1_gen40_dict.json
- cost: shared pod session (~2.5h RTX 5090, est. ~$1.5-2 total across coverage+A11).
