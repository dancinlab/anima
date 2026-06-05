---
license: odc-by
language: [en, fr, de, es, ko]
tags:
  - anima
  - clm
  - convmoe
  - byte-level
  - engine-mountable
  - lane-p
library_name: pytorch
---

# anima-clm-mid-convmoe-engine-mount-byte-7m

**ENGINE-MOUNTABLE** CLMConvMoE (NOT a ByteGPT transformer) — the MID rung of the
anima CLM scale ladder, trained via the registered `a_clm_gen_pipeline`
(`CLM/train/train_lane_p.py`) and auto-serialized to an engine-loadable
**`.clm` v0.2 (CLM\x01 + CLMX)** that `CORE/clm_decode.hexa` decodes directly.

## What this is

- **Architecture**: `CLMConvMoE(d_model=768, n_experts=2, n_trunk_layers=1, kernel_size=3, vocab=256)` — conv-native byte LM, dilated-conv trunk + 2-expert MoE conv layer + byte readout. **No attention, no PyTorch in the decode path** (the `.clm` is read by the hexa engine, not torch).
- **params**: 7.479 M
- **substrate**: Lane-P (GPU-torch, RTX A6000 cap 8.6, bf16). Distinct from Lane A (AKIDA) and Lane G (forge). Lane-P = REFERENCE + engine-`.clm` bridge; forge remains the PUBLIC production trainer.
- **corpus**: balanced 4.19 GB byte subset (V=256, no tokenizer) of `anima-corpus-5lang-7b-webscale` (R2 `phanes/anima-7b/web/<lang>/shard0000.bytes`), 800 MB each of en/fr/de/es/**ko** (incl Korean). ODC-BY FineWeb-derived.

## Files

- `mid_convmoe.clm` — engine-loadable `.clm` v0.2 (CLMX trailer, 11 ext arrays). `clm_decodable()=TRUE`, nblk=6, block0 cout=768 rest=2304.
- `mid_convmoe.pt` — torch state_dict (reference).
- `mid_result.json` — full CE-descent trace + config.

## Training

6000 steps, seq_len 256, batch 64, AdamW lr 3e-4 cosine warmup 200, bf16, seed 42.
**CE descent: 5.72962 → 1.51978** (eval), uniform ln(256)=5.5452. Wall 150.4 s, GPU 91% util / 249 W (device-resident, no CPU fallback).

## Honest scope (a_scale_honest_scope · p7)

This is a **TOY/MID 7.48M ConvMoE**. It proves the **corpus → ConvMoE → engine-mount → 3-axis benchmark CHAIN end-to-end**, NOT a 7B. **7B-transfer is UNVERIFIED.** It is the engine-mountable base for the 7B ladder (`train_lane_p_3b.py`). p1–p8 held (no system prompt / persona injection / RLHF; plain byte next-token CE).
