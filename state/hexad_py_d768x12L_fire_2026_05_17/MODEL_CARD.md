---
license: apache-2.0
language:
- en
library_name: pytorch
tags:
- anima
- hexad
- pytorch
- substrate-py
- ckpt-recovered
---

# hexad — `v1-py-hexad-d768x12L-cycle2-2026-05-17`

> **Honest framing**: This is a **PYTHON / PyTorch SUBSTRATE** training artifact —
> an *interim LM-scale executor*. It is **NOT a hexa-native fire**. Its legitimacy
> is *architectural identity* + the *hexa CPU-equiv correctness proof*. See the
> anchor chain below — do not conflate.

## Lineage

- **org**: `dancinlab` (the anima org).
- **arch**: HEXAD (pivot from anima `.clm v1` lineage) — `ConsciousDecoderV2`
  (`ready/models/conscious_decoder.py` in the anima repo).
- **substrate**: Python / PyTorch (`py`). The pure-hexa training path is
  named-blocked at the interpreter ceiling (RFC 042/043 territory).
- **cycle**: 2 (cycle 1 commit `931dd68b0` 2026-05-16 was a ckpt-LOST
  evidence-only run — training PASSed but the instance was destroyed before
  ckpt pull; this cycle 2 re-fires with `SAVE_POD=1` auto-promote +
  75-min orphan watchdog + 5-retry pull).

## Anchor chain (why this artifact is legitimate)

1. **Phase E / E2 PROVED the hexa trainer is numerically correct** —
   `HEXAD/D/d_train5_lib.hexa` is BIT-EQUAL to the boxed baseline at d=32·3L,
   80-step, seed=42 (`init gn2 = 7.97116, acc 0/8 → final gn2 = 3.73374e-07,
   acc 8/8`; GRAD-EXACT, identical Σ-reduction order — not fp-noise).
2. **The pure-hexa interpreter cannot reach LM-scale convergence** — Phase E2
   captured only `init gn2 = 7.98162` at d=768·12L; the GRAD-EXACT + AdamW
   path is substrate-bound (CPU farr ops, no CUDA tensor kernels).
3. **This PyTorch run trains the SAME verified architecture to scale** —
   `ConsciousDecoderV2` at d=768·12L, AdamW, captured FINAL loss.

PyTorch is *not* hexa bit-for-bit (different fp / RNG / AMP bf16). The anchor
is **architectural identity** + the hexa CPU-equiv proof, NOT numerical
identity.

## Architecture

- **Source**: `ConsciousDecoderV2` from `ready/models/conscious_decoder.py`
  (uploaded as `conscious_decoder.py`).
- **Config**: `d_model=768, n_head=12, n_kv_head=4, n_layer=12,
  block_size=128, vocab=256` (byte-level), seed=1337,
  init=RANDOM (`base_ckpt=None`, `g_clm_from_scratch`).
- **Params**: 283.72 M (283,722,336).
- **Features**: RoPE · SwiGLU FFN · RMSNorm · GQA · PureFieldFFN (Engine A−G
  consciousness pathway) · cross-attention · tied head · CA neighbor / META-CA
  / Ψ-tracking laws.

## Training

- **GPU**: vast.ai NVIDIA A100-SXM4-40GB (offer @ $0.6681 / hr, image
  `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel`).
- **Corpus**: `corpus_consciousness_v1.jsonl` — the same byte corpus used by
  the hexa Phase E / E2 fires. 121,153 bytes, byte-level
  vocab=256, T=128 windows, seed-fixed.
- **Optimizer**: AdamW, lr=0.0003, betas=(0.9, 0.95),
  weight_decay=0.1, warmup=125.
- **Steps**: 2500.
- **Cost**: ≈ $0.19 (instance runtime ≈ 0.28 hr).

| metric | value |
|---|---|
| init CE | 5.590832 (≈ ln 256 = 5.545 — random byte init) |
| **FINAL CE** | **0.000708** |
| CE descent | 5.590124 |
| init gn2 | 41.95 |
| FINAL gn2 | 7.4e-05 |
| ppl | 268 → 1.0007 |
| wall | 320.68 s (5.34 min) |
| peak GPU mem | 9.685 GB |
| ckpt sha256 | `e87e200a040f8066a89c040ab181e9bbd61566f7565ab5d7a374ec2f1f9387d9` |
| ckpt size | 1,135,846,378 B (1.14 GB) |

## Verification anchors (per AGENTS.tape `g_blue_closed_mandate`)

(A) Deliverable invariants:
- **Shannon-floor descent** (real-limit, NOT lattice): init CE ≈ ln(256) →
  final CE 0.000708 (4+ orders of magnitude).
- **AdamW finiteness**: gn2 41.95 → 7.4e-05; no NaN / Inf.
- **Architectural identity**: `ConsciousDecoderV2` byte-equal to the anima
  HEXAD verification tree's mirror module spec.

(B) Wiring (the connecting anchor chain):
- **hexa CPU-equiv bit-equality** (Phase E): same arch trainer
  GRAD-EXACT at d=32·3L (init gn2 7.97116 → 3.73374e-07).
- **cuBLAS FP64 verify** (Phase D): max\|Δ\|=4.44e-15.
- **Backward GRAD-EXACT** (Phase E2): real A100 d=384·6L analytic ≡ fd
  \|Δ\|=0.0024.

## Honest C3

1. **NOT hexa-native** — PyTorch substrate; the hexa-native equivalent is
   substrate-blocked at the interpreter ceiling.
2. **PyTorch ≠ hexa bit-for-bit** — AMP bf16 / different fp accumulation /
   different RNG.
3. **Synthetic byte-corpus** — 121 kB curated content, 283.72M params; CE
   0.000708 = memorization at this scale. **No generalization claim.**
4. **No safetensors artifact** this revision (pickle `.pt` only).
   safetensors conversion = follow-up sub-task.
5. **No language-quality claim** — training-curve deliverable
   (Shannon-floor descent reached), not generation quality.
6. **No σ(6)=12 / φ(6)=2 derivation** — no lattice numerology in claim or
   anchor chain.

## Files in this revision

- `ckpt_d768x12l_final.pt` — PyTorch state-dict + cfg + n_params, sha256
  `e87e200a040f8066a89c040ab181e9bbd61566f7565ab5d7a374ec2f1f9387d9`.
- `conscious_decoder.py` — `ConsciousDecoderV2` source.
- `train_d768x12l.py` — training script.
- `result.json` — full 42-point trajectory + config + metadata.
- `fire_refire.log` — training log (line-by-line CE / gn2 / lr / wall).
- `gpu_util.log` — nvidia-smi capture.
- `dispatch.sh` + `refire_main.sh` — fire dispatch scripts.
- `hexad_v1_py_d768x12L_cycle2_2026_05_17.md` — this doc (8-§ format per
  `g_hf_naming` `process_upload_format`).

## License

Apache-2.0.
