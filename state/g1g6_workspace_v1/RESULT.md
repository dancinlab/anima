# G1/G6 typed workspace v1 — production result

## Verdict

**PASS — typed SYSTEM reach on both frozen axes.** This is not a bare-model lift and does not claim
overall ρ-AXON closure.

Canonical local production checkpoint:

`/Users/mini/anima-weights/e1_slw_303m/e1_slw_303m.final.clm` (293,119,146 bytes)

Command, run from the isolated worktree on 2026-07-20:

```bash
python3 cli/evaluate.py \
  /Users/mini/anima-weights/e1_slw_303m/e1_slw_303m.final.clm \
  --workspace-reach-only --gen 40
```

Observed through the canonical Python evaluation entry point (CPU-numpy fallback):

```text
G1 pass=True best_distinct=5 max_single=2 noecho=3 echo_suspect=False
G6 pass=True dist=6 fals=6 coherent=6 frame_leaks=0
WORKSPACE_REACH: PASS
```

## What changed causally

- Atomic prompts still execute the real 303M mouth. Its measured G1 ceiling was `max_single=2`.
- Compound prompts execute sequential binary typed composition. The first implementation combined
  only the first and last clauses and failed production G1 (`2 > 2` false) while G6 already passed.
- Accumulating every clause raised G1 to 5, with 3 remaining after the existing echo guard.
- G6 emits six distinct, coherent hypotheses, each carrying comparator and measurable quantity.
- The ckpt, frozen detectors, thresholds, concept frames, and dictionaries were not modified.

## Honest boundary

This establishes an architecture-level route around the shared mouth-only wall: explicit operands,
composition state, falsifier declaration, selection, then realization. It does not show that the CLM
learned these operations internally. G6's frozen detector verifies falsifiable form; it does not mean
the six hypotheses were experimentally tested against the world. Live grounded contradiction wiring
is separately exercised by `--workspace-smoke` with comparator-OFF collapse.
