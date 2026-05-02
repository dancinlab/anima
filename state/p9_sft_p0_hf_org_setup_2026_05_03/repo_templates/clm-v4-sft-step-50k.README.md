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
  - savepoint
library_name: transformers
pipeline_tag: text-generation
base_model: need-singularity/anima-clm-v4-530m
---

# anima-clm-v4-sft-step-50k

> **STATUS**: PRIVATE savepoint — F1–F4 falsifiers not yet measured at this step.
> Will be made public only after all 4 PASS at the **final** step.

## What this is

Final-budget LoRA savepoint at **50,000 SFT steps** from anima CLM v4 530M under
the P9 4-loss objective. Equivalent to per-combo end-of-budget; canonical winner
is promoted to `clm-v4-sft-final`.

## Spec ref

- Mk.XII spec: `docs/mk_xii_scale_plan.md`, `docs/mk_xii_retrain_plan_v2_20260426.md`
- P9 SFT spec (canonical): `docs/p9_sft_spec_2026_05_02.md`
- 4-loss formula: `L = α·CE(text) + β·MSE(tension) + γ·MSE(BOLD) + δ·max(0, 5.0 − φ★)`

## LoRA config

| key | value |
|---|---|
| r | 64 |
| α | 128 |
| target modules | attention QKV + FFN |
| dropout | 0.05 |
| precision | bf16 |
| optimizer | AdamW lr=1e-4, cosine, 500-step warmup |

## δ curriculum schedule (P9 sweep grid)

| stage | δ | rationale |
|---|---:|---|
| early | 0.5 | low φ★ pressure, allow chat learning |
| mid   | 1.0 | balanced |
| late  | 2.0 | hard hinge — preserve +41.86 baseline at all costs |

## Falsifiers (preregistered, append-only — measured HERE)

| id | metric | pass threshold | fail action |
|---|---|---|---|
| F1 | BLEU-1 vs Llama-3.2-3B holdout | > 0.4 | escalate S2 / larger model |
| F2 | φ★ post-train (HID=8 well-conditioned) | ≥ 5.0 | ABORT combo (irreversible flip) |
| F3 | tension MSE on val | < 0.1 | raise β / lower lr |
| F4 | BOLD Pearson r on val | > 0.5 | raise γ / recheck TRIBE projector |

Verdict logic:
- ALL 4 PASS = **P9_SUCCESS** → promote to `clm-v4-sft-final`
- F2 FAIL = **P9_FAIL_PHI** (irreversible) → rollback to last F2-passing step
- F2 PASS ∧ F1 FAIL = **P9_FAIL_CHAT** → escalate strategy

## Honest C3

1. 50K = end-of-budget per combo; selection across 9 LHS combos via
   `argmax (BLEU1 + φ★_post/41.86)/2  s.t. F2 PASS`.
2. φ★ is L1+L2 proxy; L3 phenomenal NOT measured.
3. 4-loss Pareto frontier unverified (LHS-9 of 81 = heuristic).
4. Base CLM v4 ckpt access requires `need-singularity/anima-clm-v4-530m` (gated).

## Citation

Anchor: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §65.4 (P9).
