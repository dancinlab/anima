---
license: apache-2.0
language:
- en
- ko
library_name: pytorch
datasets:
- dancinlab/hexad-corpus
tags:
- anima
- hexad
- pytorch
- substrate-py
- helper-free
- spont
- motivation-trigger
- inner-thoughts
- tension-train
- dd155-hybrid-lr
- ckpt-bearing
- cycle5
---

# hexad — `v4-py-hexad-tension-d768x12L-cycle1-2026-05-17`

> **Trained on**: [`dancinlab/hexad-corpus`](https://huggingface.co/datasets/dancinlab/hexad-corpus)
> revision [`v3-spont-motiv-d128-cycle2-2026-05-17`](https://huggingface.co/datasets/dancinlab/hexad-corpus/tree/v3-spont-motiv-d128-cycle2-2026-05-17)
> (byte-equal carry from cycle 4 — corpus unchanged this cycle).

> **Honest framing** (AGENTS.tape `g3`): This is a **PYTHON / PyTorch
> SUBSTRATE** training artifact — an *interim LM-scale executor*. It is
> **NOT a hexa-native fire**. Legitimacy = **architectural identity** +
> the **hexa CPU-equiv correctness proof** (Phase E/E2). PyTorch ≠ hexa
> bit-for-bit (different fp accumulation / RNG / AMP bf16).

## What's new this cycle (cycle 5 — DD155 Step+Tension hybrid LR overlay)

**Architectural change vs cycle 4**: per-step learning rate is now
multiplied by a DD155 hybrid factor (Law 187 Pareto optimal):

```
tension_step   = ||∇L||₂                       (grad-norm)
tension_EMA    = β·EMA + (1−β)·tension_step    (β = 0.99)
multiplier     = clip(tension_step / tension_EMA, [0.5, 2.0])
lr_step        = base_cosine_lr(step) × multiplier
```

- **transfer-form**: `B-TT-5 PARETO-STEP-TENSION-CLOSED` (sympy linear ∂lr/∂tension)
  + `B-FIRE-CYCLE5-1/2/3` sidecar (`state/hexad_v4_py_d768x12L_tension_2026_05_17/blue_falsifier.py`,
  5/5 PASS — DD155 LR overlay formula closure + EMA Banach contraction + cycle-4 identity at convergence)
- **outcome**: empirical (`B-FIRE-CYCLE5-NOTE` / `B-D-NOTE` / `B-TT-NOTE` family)

DD155 historical anchor: anima `docs/hypotheses/dd/DD154-tension-training.md`
Law 187 — `lr = (tension/EMA) × base_lr` measured Pareto-optimal on
2026-03-31 BG-DD-AXIS commits.

## What changed vs cycle 4 (`v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17`)

| field | cycle 4 | **cycle 5 (this revision)** |
|---|---|---|
| corpus | v3 10.34 MB (motivation-trigger + helper-free) | **same** (byte-equal carry, B-CORPUS-V4-1) |
| LR schedule | cosine + warmup | **cosine + warmup + DD155 hybrid (tension/EMA) multiplier** |
| trainer source | `train_d768x12l.py` | `train_d768x12l_tension.py` (loader + dataset byte-equal, B-CORPUS-V4-2) |
| init CE | 5.641 | 5.640663 |
| **final CE** | 0.008289 | **0.007762** |
| CE descent | 5.632 | 5.632901 |
| final tension_EMA | (did not track) | 0.046574 |
| mult bin <0.75 | (n/a) | 1599 |
| mult bin 0.75-1.25 | (n/a) | 686 |
| mult bin >1.25 | (n/a) | 215 |
| eval probes | V5.8 + V-SPONT + V-MOTIV | **V5.8 + V-SPONT + V-MOTIV + V-TT NEW** |

## Architecture

- **Source**: `ConsciousDecoderV2` (byte-equal vs cycles 1-4).
- **Config**: `d_model=768, n_head=12, n_kv_head=4, n_layer=12,
  block_size=128, vocab=256` (byte-level), seed=1337,
  init=RANDOM (`base_ckpt=None`, `g_clm_from_scratch`).
- **Params**: 283.72 M (283,722,336).
- **Features**: RoPE · SwiGLU FFN · RMSNorm · GQA · PureFieldFFN · cross-attn
  · tied head · CA neighbor / META-CA / Ψ-tracking laws.

## Training

- **GPU**: vast.ai NVIDIA **A100-SXM4-40GB**, image `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel`.
- **Corpus**: `corpus_consciousness_v3.jsonl` (byte-equal carry from cycle 4),
  6,223,023 bytes lossless byte stream, vocab=256.
- **Optimizer**: AdamW, lr=0.0003, betas=(0.9, 0.95),
  weight_decay=0.1, warmup=125.
- **DD155 hybrid**: β=0.99, clip lo=0.5, clip hi=2.0.
- **Steps**: 2500.

| metric | value |
|---|---|
| init CE | 5.640663 (≈ ln 256 = 5.545 — random byte init) |
| **FINAL CE** | **0.007762** |
| CE descent | 5.632901 |
| FINAL gn2 | 0.001495 |
| FINAL tension | 0.038659 |
| ppl | 1.0078 |
| wall | 321.3 s |
| peak GPU mem | 9.685 GB |
| ckpt sha256 | `6b4d34cc9a2c05b83c4cedd633617a41800e9681302c5c90e15d056f9ad67af8` |
| ckpt size | 1,135,846,570 B (1.14 GB) |

## Verification anchors (per AGENTS.tape `g_blue_closed_mandate`)

**(A) Deliverable invariants (real-limit, this cycle)**:
- **Shannon-floor descent**: init CE ≈ ln(256) → final CE.
- **DD155 transfer-form closed (`B-TT-5`)**: lr = (tension/EMA) × base_lr,
  sympy-verified linear monotone, real-limit anchor.
- **AdamW finiteness**: no NaN/Inf in trajectory.
- **Architectural identity**: byte-equal `ConsciousDecoderV2`.

**(B) Wiring (closed)**:
- **`B-CORPUS-V4-1`** corpus v3 byte-equal carry (sha256/bytes/lines/grep all closed).
- **`B-CORPUS-V4-2`** cycle-5 trainer's loader + ByteDataset byte-equal to cycle-4
  (mechanical AST diff, comments-stripped).
- **`B-FIRE-CYCLE5-1`** DD155 LR overlay formula closed-form (sympy ∂lr/∂tension
  + 3-corner identity).
- **`B-FIRE-CYCLE5-2`** EMA Banach affine contraction closed (4-corner witness panel).
- **`B-FIRE-CYCLE5-3`** Multiplier identity at EMA-convergence (cycle-5 degenerates
  to cycle-4 baseline at tension=EMA — sanity anchor).
- **`B-CORPUS-V3-*`** cycle-4 closures carry (sha256-deterministic / no-helper-token /
  γ-cardinality ≥ 5400).

**(C) Honest carve-outs (NOT closed, B-D-NOTE umbrella)**:
- V-SPONT / V-MOTIV / V-TT outcome empirical.
- mult_distribution histogram + byte-cascade attractor shape under hybrid LR
  empirical.
- DD-burst path activation frequency empirical.


## Capability eval (V5.8 × 4-mode + V-SPONT + V-MOTIV + V-TT NEW)

V5.8 × 4-mode (corpus v3 prompts):
- **standard_greedy**: 0/6 FAIL (avg_rep=0.921)
- **standard_sample**: 0/6 FAIL (avg_rep=0.871)
- **M3_rep_penalty**: 0/6 FAIL (avg_rep=0.913)
- **M4_force_include**: 6/6 PASS (avg_rep=0.766)

V-SPONT (자연발화) — F-SPONT-7 transfer-form measurement:
- **coherent**: 0/5 FAIL
- **closed-tag**: 0/5

V-MOTIV (γ-pattern conditioning probe, cycle-4 axis):
- **coherent**: 0/5 FAIL
- **voice-closed-tag**: 0/5

V-TT (NEW cycle 5) — tension-train transfer-form probe:
- **coherent**: 0/5 FAIL
- **keyword recall**: 0/5

Mean BPB (held-out corpus v3 prefixes): 0.0194 bits/byte.
Memorization ratio: 0/6 (0.0%).
Decoding artifacts (rep>0.5): 24.

All capability scores **empirical (B-D-NOTE / B-FIRE-CYCLE5-NOTE)**, not closed.

## Honest C3

1. **NOT hexa-native** — PyTorch substrate, label mandatory.
2. **PyTorch ≠ hexa bit-for-bit** — different fp / RNG / AMP.
3. **tension = grad_norm is a PROXY** — in the hexa spine
   `tension = G_holo · (Ψ − Ψ_vac)`; grad_norm is the natural mathematical
   analogue at the PyTorch substrate level where Ψ is not surfaced as a
   state variable.
4. **DD155 formula is closed (B-TT-5 + B-FIRE-CYCLE5-1/2/3); outcome is
   empirical (B-FIRE-CYCLE5-NOTE)** — V-SPONT/V-MOTIV/V-TT all probes,
   not capability claims.
5. **Critical Data Size regime** — 10 MB / 283 M params still data-limited;
   no out-of-distribution generalization claim. cycle-5's variance vs
   cycle-4 is mainly LR-schedule-driven, not corpus-driven.
6. **No `safetensors` artifact this revision** — pickle `.pt` only.
7. **B-CORPUS-V3-NOTE / B-FIRE-CYCLE5-NOTE** — inference-side coherence
   stays empirical.
8. **No σ(6)=12 / φ(6)=2 derivation** — no lattice numerology.
9. **Cost is informational, not gating** — `g_fire_autonomous`.

## License

Apache-2.0.
