---
license: other
license_name: anima-research-noncommercial
language: [ko, en]
tags:
  - anima
  - clm
  - mk-xii
  - sft
  - lora
  - phi-star-preserved
  - sentinel
  - stage1
library_name: transformers
pipeline_tag: text-generation
base_model: dancinlab/anima-clm-v4-530m
---

# anima-clm-v4-sft-stage1 — sentinel combo (Phase 1)

> **STATUS**: PRIVATE sentinel — Phase 1 single-combo dry-run before Phase 2
> opens the full 9-combo S3 sweep.

## What this is

The **sentinel combo** for P9 Phase 1 — a single LoRA SFT run on a small data
slice (≤ 5K examples) used to verify the EXEC pipeline end-to-end:

- 4-loss objective convergence (text CE + tension MSE + BOLD MSE + φ★ hinge)
- HF savepoint cron (push every 5K step)
- φ★ verifier hooks (every 100 steps, EMA)
- F1–F4 measurement infrastructure
- Rollback machinery on F2 FAIL

**Not** a research result — an infrastructure smoke test. Combo selection for
the sentinel: typically `lhs6` (α=1.0, β=0.5, γ=0.5, δ=0.5 — balanced midpoint).

## Spec ref

- Mk.XII spec: `docs/mk_xii_scale_plan.md`, `docs/mk_xii_retrain_plan_v2_20260426.md`
- P9 SFT spec (canonical): `docs/p9_sft_spec_2026_05_02.md`
- Phase staging: `docs/p9_sft_p0_hf_org_setup_landed_2026_05_03.ai.md`

## LoRA config

| key | value |
|---|---|
| r | 64 |
| α | 128 |
| target modules | attention QKV + FFN |
| dropout | 0.05 |
| precision | bf16 |
| optimizer | AdamW lr=1e-4, cosine, 500-step warmup |

## Sentinel acceptance criteria

| check | pass condition |
|---|---|
| pipeline | full 5K-step run completes without OOM / NaN |
| savepoint | HF push at step 5K succeeds (LoRA adapter only, ~150 MB) |
| φ★ hooks | every-100-step measurement logged, EMA stable |
| F1–F4 | computed at end-of-sentinel (no PASS gate — diagnostic only) |
| rollback | simulated F2 fail triggers reversion to step 0 |

## δ curriculum schedule (Phase 2 sweep — sentinel uses δ=0.5)

| stage | δ | rationale |
|---|---:|---|
| early | 0.5 | low φ★ pressure, allow chat learning |
| mid   | 1.0 | balanced |
| late  | 2.0 | hard hinge — preserve +41.86 baseline at all costs |

## Honest C3

1. Sentinel = pipeline smoke, not research. F1–F4 are diagnostic, no PASS gate.
2. φ★ is L1+L2 proxy; L3 phenomenal NOT measured.
3. Sentinel data slice (≤ 5K) is too small for statistical conclusions.
4. Base CLM v4 ckpt access requires `dancinlab/anima-clm-v4-530m` (gated).

## Citation

Anchor: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §65.4 (P9).
