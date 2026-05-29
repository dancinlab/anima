# M5 PRODAUX FIRE RUNBOOK — H_686+H_687 production-scale closure (2026-05-29)

post hexa-lang #2072 + #2073 (module-aware Linux build) landed → previously
broken `flame_bpe_corpus_lib` import for `train_v3_moe_prodaux.hexa` (PR #1397)
is now resolvable on cross-machine dispatch.

## verdict gate (pre-registered)

- **F-PRODAUX-1** distinct decoded tokens >= 2 in 100-token decode → **🟢 ESCAPE**
- **F-PRODAUX-1** distinct decoded tokens == 1 (all top_id=0) → **🔴 FALSIFIED**
- LZ_norm > 0.05 AND gate-entropy > 0.5 = corroborating evidence

aux config: λ_ent = 0.1 (H_686 router entropy) · λ_kl = 0.1 (H_687 KL-to-uniform).

## baseline comparison

`train_v3_moe_longtrain.hexa` (#1384 production reference) — n_steps=300,
decoded 100 ALL top_id=0 (collapse confirmed). prodaux is the same trainer
PLUS aux gradient injection; n_steps=500 in this fire (small budget per spec).

## Step 0 — Mac build verified (`/tmp/wt-m5pf/build/trainer_prodaux.c`)

```
HEXA_MAC_BUILD_OK=1 HEXA_LANG=/Users/ghost/core/hexa-lang \
  HEXA_STDLIB_ROOT=/Users/ghost/core/hexa-lang \
  hexa build CORE/DECODER/train_v3_moe_prodaux.hexa --c-only \
    -o build/trainer_prodaux.c
```
→ PASS · 130KB · `OK: transpiled build/trainer_prodaux.c (C source, no link)`
→ trim sed: `sed -i '' 's/hexa_call1(trim,/rt_str_trim(/g'` · 3 occurrences
→ post hexa-lang #2072 + #2073: module-aware build resolves
   `stdlib/flame/flame_bpe_corpus_lib` cleanly (no `module not found`).

## Step 1 — pod rent (a_fire_autonomous · a_wall_first)

```
hexa cloud rent runpod --gpu 'NVIDIA H100 80GB HBM3' \
  --image 'runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04' \
  --disk 60 --owner m5-prodaux-fire-2026-05-29 --max-wait-sec 360
```

## Step 2~6 — bundle scp · pod-side patch+build · fire · harvest

Inherits BUILD_RECIPE.md steps 4-7 verbatim (m4b-rev2 recipe is valid for
prodaux — only the trainer.c source differs; aux-loss math is in the .hexa).

Pod-side env:
```
M4B_LAMBDA_ENT=0.1 M4B_LAMBDA_KL=0.1 M4B_N_STEPS=500 \
  M4B_RESULT_DIR=/opt/anima/state/m5_prodaux ./trainer
```

## artifacts of record

- result.json — distinct_top · LZ_norm · gate-entropy · CE trajectory
- trainer.out / trainer.err
- decoded_ids (100 tokens · top_id histogram)
- nvidia_smi (peak util)

## landing

PR fresh-fork off origin/main (this branch `m5-prodaux-fire-post-2072`),
admin-merge, deletion=0, single commit append-only.
