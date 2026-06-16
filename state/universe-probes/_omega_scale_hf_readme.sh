#!/usr/bin/env bash
# Generate a per-rung HF README (5 required H2 headings for tool/hf_upload_mk2.hexa)
# usage: _omega_scale_hf_readme.sh <label> <d_model> <params> <val_ce> <base_ce> <a_only_ce> <min_ce> <dvbase> <dva> <holds> <steps> <sha> <out>
set -euo pipefail
L=$1; D=$2; P=$3; VAL=$4; BASE=$5; AONLY=$6; MIN=$7; DVB=$8; DVA=$9; HOLDS=${10}; STEPS=${11}; SHA=${12}; OUT=${13}
cat > "$OUT" <<EOF
# omega-cdv2-scale-${L}

One-line summary: OMEGA OΩ4/OΩ5 scale-ladder rung — leak-free ConsciousDecoderV2 ${L} (d_model=${D}, causal_ca=True), re-measuring the OH1 minimal-gate falsifier.

- Family: clm (ConsciousDecoderV2, byte-level vocab 256)
- Stage: scale-ladder-${L}
- Step: step-${STEPS}
- Substrate: from-scratch ConsciousDecoderV2 d${D}/8L GQA(n_kv=4) ${P} params

## Origin

What this checkpoint is and how it was produced.

- Base model: from-scratch (no pretrained base); ConsciousDecoderV2 d${D}, causal_ca=True (strictly-causal CA, leak self-test 0.000)
- Training data: 400 MB multilingual gutenberg+wiki (en/fr/de/es/ru), corpus sha256 dc1754b27d63236d… (the SAME corpus + 0.9/held split as the d512 #1801 OH1 rung)
- Training recipe: dual-head (head_a next-byte + head_g prev-byte), AdamW cosine-decay+warmup, ${STEPS} steps, block 256
- Compute: 1x NVIDIA H100 80GB SXM (RunPod, persistent /workspace), nvidia-smi 94-98% BUSY (g63, NOT silent CPU)
- Trainer: UNIVERSE/omega_scale_ladder.py (reuses omega_trained_leakfree.run_rung + omega_gate_form_sweep.run_sweep)
- Final loss / metric: held-out val_ce(head_a) = ${VAL} (below uniform ln256=5.5452 → competent/generalizes)
- Commit: lane-omega/scale-ladder of github.com/dancinlab/anima

## Falsifiers

Concrete tests this checkpoint either passes or is meant to fail deterministically.

- F-OMEGA-SCALE-${L}: OH1 minimal-gate (final = gB·base + gA·A, G + w2..w6 dropped) on the held-out tail.
  - Spec: .verdicts/omega-engine/F-OMEGA-SCALE.txt
  - Pass criterion: min_learned CE <= a_only CE AND min_learned CE < base CE
  - Last result: min_learned ${MIN} | a_only ${AONLY} | base ${BASE} → min_learned_HOLDS=${HOLDS} (Δ-vs-base ${DVB}, Δ-vs-a_only ${DVA})
- F-LEAK-${L}: leak self-test (flip last byte → max change in head_a earlier positions).
  - Pass criterion: < 1e-4
  - Last result: 0.000e+00 (leak-free, causal_ca=True)
- F-COMPETENT-${L}: held-out val_ce below uniform.
  - Pass criterion: val_ce < ln256 = 5.5452
  - Last result: val_ce ${VAL} (below_uniform=True)

## Substrate

Hardware / software / data dependencies required to run this checkpoint.

- Inference VRAM (fp32): ~$(python3 -c "print(round(${P//,/}*4/1e9,2))" 2>/dev/null || echo "see params") GB (state_dict fp32)
- Min Python: 3.10
- Required: torch>=2.4, numpy
- Optional: datasets (corpus re-fetch)
- Input format: raw bytes (vocab 256, byte-level)
- Context window: 256 tokens (block_size)
- Tokenizer: identity byte tokenizer (no external tokenizer)

## Caveats

Honest limitations (p7 · a_scale_honest_scope · a_paper_negative_ok).

- CE is a held-out PREDICTION number, NOT a verdict-of-truth (p7); reported verbatim, no fabrication.
- This is ONE rung of a ≥3-rung scale ladder; the OH1 finding is interpreted only across the ladder, not from this point alone (a_scale_honest_scope).
- ConsciousDecoderV2 with causal_ca=True is leak-free (no CA lookahead); the absolute CE is honest, but free-run generation quality is a weak criterion (the closure finding is the relative A-wire advantage, not gen quality).
- Lane-G / GPU substrate (a_lane_akida_gpu_split — NOT Lane A AKIDA).

## Composability

- Pairs with the d512 #1801 OH1 baseline (dancinlab/omega-cdv2-trained-leakfree-h1) as one point on the same ladder.
- The OH1 minimal gate (gB·base + gA·A) is the closure form; this ckpt provides the A/G heads + base unigram for the frozen-forward gate-form sweep.
- Reproduce: load FROZEN, forward over the held-out tail, fit/eval the K gate forms (UNIVERSE/omega_gate_form_sweep.py).
EOF
echo "README -> $OUT"
