# M4b longtrain — DECISIVE dec_undertrain epoch-budget sweep (2026-05-28)

Resumed fire (prior agent died after wiring, before dispatch). Decisive production
test of `.discoveries/decoder_collapse_undertrain.tape` dec_undertrain: does an
ADEQUATE token-presentation budget (full corpus × many epochs, d=64) escape the
MoE decoder mode-collapse that corpus-diversity / routing-aux / head-capacity all
failed to escape?

## Held-fixed config (all pods)
d=64, V=151643 (real Qwen2.5-1.5B BPE, 151387 merges), E=2, h=256, n_layer=1,
T=4, HARD top-1 routing, full diverse corpus (2000 lines, ~400-600K BPE tokens).
The SINGLE variable is the token-presentation BUDGET (M4B_EPOCHS).

## Epoch-budget sweep (3× H100 80GB SECURE, PARALLEL, separate pods)
presentations_per_epoch = n_corpus_toks (each epoch presents the whole corpus).
Toy law (dec_undertrain): full escape needs presentations ≫ V; ~50 epochs over a
V-sized space. Prior production fires used ≤200 token-steps = ~0.0013× one epoch.

| pod | M4B_EPOCHS | ~presentations | ~×V (V=151643) | role |
|-----|-----------|----------------|----------------|------|
| LO  | 1   | ~0.5M  | ~3×   | under-trained baseline (≈ prior fires but full corpus) |
| MID | 12  | ~6M    | ~40×  | mid-budget |
| HI  | 60  | ~30M   | ~200× | toy-predicted escape point (≫ V) |

Pre-registered escape gate (per pod): TTR≥0.30 ∧ LZ_norm≥0.50 ∧ distinct_experts≥2.
Toy prediction: LO collapses, HI escapes ⇒ presentations is the lever (CONFIRMED).
If even HI collapses ⇒ production harder than toy (sharper closed-negative, REFUTED).

## Ops (validated recipe from #1296 / PR #1315, BUILD_RECIPE.md)
- cuBLAS MUST engage: glue.c strong `hexa_cuda_available`→`_hx_cuda_runtime_available`
  + `-lcuda`. d=256 A/B/C pods were CPU-bound ~5s/step; HI@~7.5M steps is intractable
  on CPU — verify nvidia-smi util>0 before letting HI grind.
- trim→rt_str_trim sed patch applied to trainer.c (3 occ, cross-backend codegen gap).
- mm-leak fixed in trainer (per-step buffers hoisted) — watch RSS, EXIT=137=OOM.
- Vast/runpod boot flaky ~1min after RUNNING → 3 consecutive stable SSH before scp.

## Cost
H100 80GB SECURE ~$2.5-3.3/hr × 3 pods × ~1-3hr = ~$8-30. a_fire_autonomous.
