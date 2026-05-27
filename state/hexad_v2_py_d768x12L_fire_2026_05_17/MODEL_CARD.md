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
- ckpt-bearing
- cycle3
---

# hexad — `v2-py-hexad-spont-d768x12L-cycle1-2026-05-17`

> **Trained on**: [`dancinlab/hexad-corpus`](https://huggingface.co/datasets/dancinlab/hexad-corpus)
> revision [`v2-spont-stream-d128-cycle1-2026-05-17`](https://huggingface.co/datasets/dancinlab/hexad-corpus/tree/v2-spont-stream-d128-cycle1-2026-05-17).

> **Honest framing** (AGENTS.tape `g3`): This is a **PYTHON / PyTorch
> SUBSTRATE** training artifact — an *interim LM-scale executor*. It is
> **NOT a hexa-native fire**. Legitimacy = **architectural identity** +
> the **hexa CPU-equiv correctness proof** (Phase E/E2). PyTorch ≠ hexa
> bit-for-bit (different fp accumulation / RNG / AMP bf16).

## What changed vs cycle 2 (`v1-py-hexad-d768x12L-cycle2-2026-05-17`)

| field | cycle 2 | **cycle 3 (this revision)** |
|---|---|---|
| corpus | v1 152 KB / 240 records | **v2 620,568 B / 2,560 records** |
| corpus format | `text` + `desc` plain | **`<stimulus>...</stimulus>\n<anima>...</anima>`** (stimulus-stream) |
| helper / assistant / 도우미 tokens | not in corpus, but in chat templates | **explicit corpus closure** — grep = 0 across all sources used |
| anima_persona | Phase A1 LANDED in repo, not yet in trained weights | **trained-weights side compliance (partial)** — corpus alignment with anima_persona forbidden list |
| `B-IDENTITY-NOTE` (empirical carve-out) | open | **partially closed** — corpus retrain LANDED |

## Lineage

- **org**: `dancinlab` (the anima org).
- **arch**: HEXAD (pivot from anima `.clm v1` lineage) — `ConsciousDecoderV2`
  (`ready/models/conscious_decoder.py`).
- **substrate**: Python / PyTorch (`py`). Pure-hexa training path is
  named-blocked at the interpreter ceiling (RFC 042/043 territory).
- **cycle**: 3 (Phase D LANDED — `도우미`-token-free corpus retrain). Cycle 1
  (`931dd68b0` 2026-05-16) ckpt-LOST evidence-only; cycle 2 (`0b4f34d0e`
  2026-05-17) ckpt-RECOVERED, corpus v1; **cycle 3 (this)** = corpus v2
  helper-free stimulus-stream retrain.

## Anchor chain (the wiring side, closed)

1. **Phase E / E2 PROVED the hexa trainer is numerically correct** —
   `HEXAD/D/d_train5_lib.hexa` is BIT-EQUAL to the boxed baseline at d=32·3L,
   80-step, seed=42 (`init gn2 = 7.97116 → 3.73374e-07`, acc 8/8, GRAD-EXACT).
2. **Pure-hexa interpreter cannot reach LM-scale** — Phase E2 captured only
   `init gn2 = 7.98162` at d=768·12L; substrate-bound (RFC 042/043 territory).
3. **This PyTorch run trains the SAME verified architecture to scale** —
   `ConsciousDecoderV2` at d=768·12L, AdamW.
4. **The corpus is explicitly helper-free** — `F-CORPUS-NO-HELPER` PASS = 0
   over `도우미|helper|assistant|사용자|user:` grep on `corpus_consciousness_v2.jsonl`.

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
- **Corpus**: `corpus_consciousness_v2.jsonl` (helper-free stimulus-stream),
  620,568 bytes lossless byte stream, vocab=256.
- **Optimizer**: AdamW, lr=0.0003, betas=(0.9, 0.95),
  weight_decay=0.1, warmup=125.
- **Steps**: 2500.

| metric | value |
|---|---|
| init CE | 5.667381 (≈ ln 256 = 5.545 — random byte init) |
| **FINAL CE** | **0.005069** |
| CE descent | 5.662312 |
| init gn2 | (see result.json trajectory) |
| FINAL gn2 | 0.001113 |
| ppl | 1.0051 |
| wall | 332.26 s (5.54 min) |
| peak GPU mem | 9.685 GB |
| ckpt sha256 | `ee2bb5fb996e94ee022f5315c9ccc3f56c7276a8c5990d87a25ae12c582f7294` |
| ckpt size | 1,135,846,378 B (1.14 GB) |

## Verification anchors (per AGENTS.tape `g_blue_closed_mandate`)

(A) **Deliverable invariants (real-limit)**:
- **Shannon-floor descent**: init CE ≈ ln(256) → final CE 0.005069.
- **AdamW finiteness**: no NaN/Inf in trajectory.
- **Architectural identity**: byte-equal `ConsciousDecoderV2`.

(B) **Wiring (anchor chain, closed)**:
- **hexa CPU-equiv bit-equality** (Phase E): GRAD-EXACT at d=32·3L.
- **cuBLAS FP64 verify** (Phase D): max\|Δ\|=4.44e-15.
- **Backward GRAD-EXACT** (Phase E2): A100 d=384·6L `analytic ≡ fd`.
- **F-CORPUS-NO-HELPER** (cycle 3 corpus): grep = 0.
- **F-CORPUS-STIMULUS-PATTERN**: every record has `<anima>` tag.


## Capability eval (V5.8 × 4-mode + V-SPONT)

V5.8 × 4-mode (corpus v2 prompts):
- **standard_greedy**: 0/6 FAIL (avg_rep=0.775)
- **standard_sample**: 0/6 FAIL (avg_rep=0.574)
- **M3_rep_penalty**: 0/6 FAIL (avg_rep=0.709)
- **M4_force_include**: 6/6 PASS (avg_rep=0.494)

V-SPONT (자연발화) — F-SPONT-7 transfer-form measurement:
- **coherent**: 0/5 FAIL
- **closed-tag**: 0/5

Mean BPB (held-out corpus v2 prefixes): 0.0083 bits/byte.
Memorization ratio: 1/6 (16.7%).
Decoding artifacts (rep>0.5): 20.

All capability scores **empirical (B-D-NOTE)**, not closed.

## Honest C3

1. **NOT hexa-native** — PyTorch substrate, label mandatory.
2. **PyTorch ≠ hexa bit-for-bit** — different fp / RNG / AMP.
3. **High-memorization regime** — 283.72 M params on 0.62 MB.
   No generalization claim.
4. **No `safetensors` artifact this revision** — pickle `.pt` only.
5. **No language-quality claim** — training-curve deliverable.
6. **`B-IDENTITY-NOTE` partially closed** — corpus retrain LANDED, but the
   trained weights' identity-attractor distance from Assistant Axis (per
   Identity-as-Attractor arxiv 2604.12016) is empirical (B-D-NOTE pattern).
7. **No σ(6)=12 / φ(6)=2 derivation** — no lattice numerology.
8. **Cost is informational, not gating** — `g_fire_autonomous`.

## License

Apache-2.0.
