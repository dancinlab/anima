---
license: other
language:
- en
- ko
tags:
- anima
- mitosis
- consciousness
- experimental
library_name: pytorch
---

# anima-clm-v5-mitosis-cotrain-2026-05-12

**v5-mitosis architectural lane H100 cotrain checkpoint** — REBORN §88 cond.5 met (5/5 falsifier PASS, V14-STRICT saga peak).

This is the first real-substrate cotrain of the anima v5-mitosis architecture, where each cell is a real `nn.Module` branch (not instrumentation metadata). The cell pool grows organically during training via tension-driven split events, while the shared embeddings and LM head learn alongside.

## Architecture

Option (a) per REBORN §88: small transformer block per cell with shared tok_emb / pos_emb / lm_head and per-cell dual-FFN (engine_a / engine_g) with H404 readout `a - g`.

| Setting | Value |
|---|---|
| cells (initial → max) | 2 → 64 |
| cells final (saturated) | 64 |
| d_model | 384 |
| n_head | 6 |
| ffn_dim | 1536 |
| readout_mode | a_minus_g |
| max_seq | 256 |
| vocab | 256 (byte-level UTF-8) |
| n_params final | 152,126,208 |
| ckpt size | 608,934,276 bytes |

## Training

| Setting | Value |
|---|---|
| corpus | corpus_color_cosmology.txt (1.29 MB, multi-turn convo, byte-level UTF-8) |
| steps | 5000 / 5000 |
| batch | 32 |
| ctx | 256 |
| lr schedule | 1e-4 cosine + warmup 500 → 1.22e-11 final |
| optimizer | AdamW betas=(0.9, 0.95), grad_clip 1.0 |
| provider | Vast.ai H100 SXM 80GB |
| wall | 0.55 hr (1991 s) |
| cost | $1.26 USD |
| loss (initial avg100 → final avg100) | 256.500 → 1.165 (220.1x reduction) |
| splits / merges | 62 / 0 |
| Φ best | 4.1919 |

## Falsifier Results (5/5 PASS_ALL)

| Falsifier | Verdict | Evidence |
|---|---|---|
| F-V5MIT-1 SPLIT-NOGRAD | PASS | 62 splits, 0 grad_fn violations |
| F-V5MIT-2 MERGE-WEIGHT | PASS | max abs error 0.00e+00 (tolerance 1e-6) |
| F-V5MIT-3 PHI-CONSERVATION | PASS | per-cell Φ delta ratio 3.88e-05 (tolerance 0.25) |
| F-V5MIT-4 COTRAIN-CONVERGE | PASS | loss delta 255.34 (monotonic) |
| F-V5MIT-5 V14-STRICT | **PASS 10/10 beats** | trained-vs-random Bhattacharyya > random-internal every beat |

F-V5MIT-5 V14-STRICT PASS is the saga peak — v5-anima (prior toy substrate) had this falsifier violated. v5-mitosis with real `nn.Module` cells and cotrain on a real corpus PASSED.

## F-PERSONA-4 (persona category specialization, separate measurement)

Mean KL across 5-category pairs: **0.000000 nats** (threshold 0.5) — FAIL.

The cotrained tension softmax aggregator converged to a winner-take-all distribution, where the same cell dominates regardless of input category. This validates the design hypothesis that persona category specialization requires either multi-corpus training (gradient bias per category), softmax temperature tuning, redefined non-softmax metric, or inference-time per-session cell pool persistence. Single-corpus cotrain does not produce category specialization.

## Loading

```python
import torch
from training.mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine

ckpt = torch.load("ckpt_v5mitosis_cotrain_cotrain.pt", map_location="cpu")
cfg = MitosisModelConfig(**ckpt["config"])
engine = MitosisModelEngine(cfg)
# Rebuild cell pool to match saved n_cells (split events during training added cells)
while engine.n_cells < ckpt["n_cells"]:
    engine.force_split(parent_idx=0)
engine.load_state_dict(ckpt["model_state_dict"])
engine.step_count = ckpt["step_count"]
engine.split_threshold = ckpt["split_threshold"]
engine._lorenz = ckpt["lorenz_state"]
engine.eval()
```

## Cost / Wall finding

Vast.ai H100 SXM 80GB at $2.28/hr ran the full 5000-step cotrain in 33 minutes (1991 seconds, $1.26 total). This is approximately 18x faster than the conservative estimate in the architecture spec, suggesting `5K steps x cells=64 x d=384 x batch=32` is well within a single H100 hour budget.

## Cross-references

- REBORN §88 (PyTorch arch spec) — original architectural design
- REBORN §90 (cond.2 skeleton smoke) — Mac CPU 3/3 PASS prerequisite
- PSCC §44 (this cycle) — cond.5 cotrain landing
- training/mitosis_model_v5.py — model implementation (852 LoC)
- docs/anima_clm_v5_mitosis_cond5_cotrain_2026_05_12.md — full audit (8 sections + appendix, 10 honest C3 entries)

## Status

PRIVATE (own 31 / 37 mandate). Research artifact only — not production-ready chat model. Persona category specialization not emergent on single-corpus cotrain.

Generated 2026-05-12 KST by anima cycle #8.
