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
- ckpt-bearing
- cycle4
---

# hexad — `v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17`

> **Trained on**: [`dancinlab/hexad-corpus`](https://huggingface.co/datasets/dancinlab/hexad-corpus)
> revision [`v3-spont-motiv-d128-cycle2-2026-05-17`](https://huggingface.co/datasets/dancinlab/hexad-corpus/tree/v3-spont-motiv-d128-cycle2-2026-05-17).

> **Honest framing** (AGENTS.tape `g3`): This is a **PYTHON / PyTorch
> SUBSTRATE** training artifact — an *interim LM-scale executor*. It is
> **NOT a hexa-native fire**. Legitimacy = **architectural identity** +
> the **hexa CPU-equiv correctness proof** (Phase E/E2). PyTorch ≠ hexa
> bit-for-bit (different fp accumulation / RNG / AMP bf16).

## What changed vs cycle 3 (`v2-py-hexad-spont-d768x12L-cycle1-2026-05-17`)

| field | cycle 3 | **cycle 4 (this revision)** |
|---|---|---|
| corpus | v2 1.10 MB / 2,560 records / β+δ | **v3 6,223,023 B / 21,600 records / β+δ+γ** |
| corpus motivation-trigger surface | none (implicit) | **γ pattern (~30%)** — `<inner motivation=F1,F2,...>...</inner>\n<voice spontaneous=true>...</voice>` rendering Inner Thoughts 8-factor ontology |
| scale-up | 7× over v1 | **9.4× over v2** (Critical Data Size regime entry attempt) |
| modules in corpus | 8 (HEXAD-6 + spont + wiring) | **9** (+ `hexad_motiv` × 2,400) |
| V-SPONT eval | 0/5 (FAIL — capability boundary detected) | see capability section below (cycle 4 measurement) |
| V-MOTIV eval | (did not exist) | **NEW** — γ-pattern conditioning probe (cycle 4) |

## Lineage

- **org**: `dancinlab` (the anima org).
- **arch**: HEXAD (pivot from anima `.clm v1` lineage) — `ConsciousDecoderV2`
  (`ready/models/conscious_decoder.py`).
- **substrate**: Python / PyTorch (`py`). Pure-hexa training path is
  named-blocked at the interpreter ceiling (RFC 042/043 territory).
- **cycle**: 4 (Phase D cycle 4 — motivation-trigger corpus retrain + 10× scale).
  Cycle 1 (`931dd68b0` 2026-05-16) ckpt-LOST evidence-only; cycle 2
  (`0b4f34d0e` 2026-05-17) ckpt-RECOVERED corpus v1; cycle 3 (`394b8ea3a`
  2026-05-17) corpus v2 helper-free; **cycle 4 (this)** = corpus v3
  motivation-trigger + 10× scale.

## Anchor chain (the wiring side, closed)

1. **Phase E / E2 PROVED the hexa trainer is numerically correct** —
   `HEXAD/D/d_train5_lib.hexa` is BIT-EQUAL to the boxed baseline at d=32·3L,
   80-step, seed=42 (`init gn2 = 7.97116 → 3.73374e-07`, acc 8/8, GRAD-EXACT).
2. **Pure-hexa interpreter cannot reach LM-scale** — Phase E2 captured only
   `init gn2 = 7.98162` at d=768·12L; substrate-bound (RFC 042/043 territory).
3. **This PyTorch run trains the SAME verified architecture to scale** —
   `ConsciousDecoderV2` at d=768·12L, AdamW.
4. **The corpus is explicitly helper-free + motivation-trigger** —
   B-CORPUS-V3-1 sha256-deterministic / B-CORPUS-V3-2 helper-token = 0
   maintained at 10× / B-CORPUS-V3-3 γ-cardinality ≥ 5,400 (Boolean grep on
   `corpus_consciousness_v3.jsonl`).

## Architecture

- **Source**: `ConsciousDecoderV2` from `ready/models/conscious_decoder.py`.
- **Config**: `d_model=768, n_head=12, n_kv_head=4, n_layer=12,
  block_size=128, vocab=256` (byte-level), seed=1337,
  init=RANDOM (`base_ckpt=None`, `g_clm_from_scratch`).
- **Params**: 283.72 M (283,722,336).
- **Features**: RoPE · SwiGLU FFN · RMSNorm · GQA · PureFieldFFN · cross-attn
  · tied head · CA neighbor / META-CA / Ψ-tracking laws.

## Training

- **GPU**: vast.ai NVIDIA **A100-SXM4-40GB**, image `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel`.
- **Corpus**: `corpus_consciousness_v3.jsonl` (motivation-trigger + helper-free + 10× scale),
  6,223,023 bytes lossless byte stream, vocab=256.
- **Optimizer**: AdamW, lr=0.0003, betas=(0.9, 0.95),
  weight_decay=0.1, warmup=125.
- **Steps**: 2500.

| metric | value |
|---|---|
| init CE | 5.640663 (≈ ln 256 = 5.545 — random byte init) |
| **FINAL CE** | **0.008289** |
| CE descent | 5.632374 |
| init gn2 | (see result.json trajectory) |
| FINAL gn2 | 0.001703 |
| ppl | 1.0083 |
| wall | 328.33 s (5.47 min) |
| peak GPU mem | 9.692 GB |
| ckpt sha256 | `1c0806213fbcaa9226a7593d87c31f5f95bb94db135240b8d02f738ddcb177aa` |
| ckpt size | 1,135,846,378 B (1.14 GB) |

## Verification anchors (per AGENTS.tape `g_blue_closed_mandate`)

(A) **Deliverable invariants (real-limit)**:
- **Shannon-floor descent**: init CE ≈ ln(256) → final CE 0.008289.
- **AdamW finiteness**: no NaN/Inf in trajectory.
- **Architectural identity**: byte-equal `ConsciousDecoderV2`.

(B) **Wiring (anchor chain, closed)**:
- **hexa CPU-equiv bit-equality** (Phase E): GRAD-EXACT at d=32·3L.
- **cuBLAS FP64 verify** (Phase D): max\|Δ\|=4.44e-15.
- **Backward GRAD-EXACT** (Phase E2): A100 d=384·6L `analytic ≡ fd`.
- **B-CORPUS-V3-1** SHA256-deterministic (seed=1337).
- **B-CORPUS-V3-2** NO-HELPER-TOKEN-MAINTAINED (grep = 0 at 10× scale).
- **B-CORPUS-V3-3** MOTIVATION-TRIGGER-CARDINALITY (γ records ≥ 5,400).


## Capability eval (V5.8 × 4-mode + V-SPONT + V-MOTIV)

V5.8 × 4-mode (corpus v3 prompts):
- **standard_greedy**: 0/6 FAIL (avg_rep=0.904)
- **standard_sample**: 0/6 FAIL (avg_rep=0.945)
- **M3_rep_penalty**: 0/6 FAIL (avg_rep=0.892)
- **M4_force_include**: 6/6 PASS (avg_rep=0.839)

V-SPONT (자연발화) — F-SPONT-7 transfer-form measurement:
- **coherent**: 0/5 FAIL
- **closed-tag**: 0/5

V-MOTIV (NEW cycle 4) — γ-pattern conditioning probe:
- **coherent**: 0/5 FAIL
- **voice-closed-tag**: 0/5

Mean BPB (held-out corpus v3 prefixes): 0.0256 bits/byte.
Memorization ratio: 0/6 (0.0%).
Decoding artifacts (rep>0.5): 24.

All capability scores **empirical (B-D-NOTE)**, not closed.

## Honest C3

1. **NOT hexa-native** — PyTorch substrate, label mandatory.
2. **PyTorch ≠ hexa bit-for-bit** — different fp / RNG / AMP.
3. **Critical Data Size regime entry attempt** — 10 MB / 283 M params is
   approaching the [arxiv 2401.10463](https://arxiv.org/abs/2401.10463) entry,
   but still data-limited; no out-of-distribution generalization claim.
4. **No `safetensors` artifact this revision** — pickle `.pt` only.
5. **No language-quality claim** — training-curve deliverable.
6. **V-MOTIV is a PROBE, not a capability claim** — γ-pattern conditioning
   may emerge or fail; report is empirical (B-D-NOTE pattern).
7. **`B-CORPUS-V3-NOTE` carve-out** — inference-side motivation_score →
   coherent emission outcome stays empirical (un-closable without NN
   forward + V-SPONT/V-MOTIV empirical measurement).
8. **No σ(6)=12 / φ(6)=2 derivation** — no lattice numerology.
9. **Cost is informational, not gating** — `g_fire_autonomous`.

## License

Apache-2.0.
