---
license: odc-by
tags:
  - clm
  - byte-level
  - reference
  - pytorch
  - cuda
  - anima
  - lane-g-ref
language:
  - en
  - ko
  - de
  - fr
  - es
library_name: pytorch
---

# clm-v1-ref-pytorch-cuda-7b

**Lane-G-ref · PyTorch+CUDA · 7B-scale REFERENCE rung** of the anima ENGINE+CLM+KOSMOS campaign.

> ⚠️ This is a **bounded-budget reference artifact**, NOT a converged production model,
> and **NOT** the anima hexa-native flame+forge production CLM. The production /
> PUBLIC-grade Lane-G CLM is the hexa-native flame+forge stack (compiler-only NN, no
> PyTorch/ATen/Python in the trained binary) per governance `a_train_flame_forge`.
> This torch trainer exists only as an honest throughput/descent reference baseline —
> the ~`UTIL_MEAN`% H100 utilization the forge util-GREEN line (≥20% gate) is chasing.
> Never confuse this reference with a forge PUBLIC artifact. Never merged with Lane A / AKIDA
> (`a_lane_akida_gpu_split`).

## What this is

A byte-level (V=256) decoder-only GPT (`ByteGPT`), the **last rung** of the Lane-G-ref
PyTorch+CUDA ladder:

```
85.6M (d768/L12/H12)  ->  3.149B (d2560/L40/H20)  ->  7.253B (d4096/L36/H32)
```

- **Architecture:** Llama-7B-ish byte-vocab shape — `d4096 / 36 layers / 32 heads (head_dim 128) / block 512`, tied input/output embeddings, GELU MLP (4× expansion), pre-LayerNorm.
- **Params:** `7,252,828,160` (~7.253B).
- **Training:** bf16 master weights + AMP autocast + gradient checkpointing + bitsandbytes AdamW8bit (so a 7B model + optimizer states fit a single H100 80GB), `BOUNDED_STEPS` bounded steps, NOT converged.
- **Corpus:** `dancinlab/clm-backbone-5lang-sample` (c4 5-lang backbone, ODC-BY) — the same corpus the 85.6M PUBLIC and 3.149B reference rungs used.
- **Substrate:** PyTorch-CUDA on H100 80GB HBM3.

## Honest scope (`a_scale_honest_scope`)

- **Descent:** `F-CLM-REF-7B-DESCENT` — val_CE `CE_FIRST` → `CE_LAST` over `BOUNDED_STEPS` bounded steps. NOT a convergence claim.
- **Utilization:** PEAK `UTIL_PEAK`% / MEAN `UTIL_MEAN`% — a well-fed H100 saturates this byte-LM workload even at 7B (>>20% gate, trivially true for torch). This is the reference utilization the forge path's util-GREEN milestone targets.
- This is a reference baseline, not a production prescription.

## Files

- `clm_ref_pytorch_cuda_7b.pt` — checkpoint (`model` state_dict + `config`).
- `clm_ref_pytorch_cuda_7b.py` — the trainer (architecture + recipe SSOT).
- `clm_ref_7b_train.log.json` — training curve + util/throughput summary.

## Lineage

- Scales `dancinlab/clm-v1-ref-pytorch-cuda` (85.6M) and `dancinlab/clm-v1-ref-pytorch-cuda-3b` (3.149B) on the same arch+corpus.
- Part of the anima CLM collection. `a_completeness_over_cheap` optional reference (NOT forge production).
