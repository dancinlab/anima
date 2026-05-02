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

# anima-clm-v4-sft-step-5k

> **STATUS**: PRIVATE savepoint — F1–F4 falsifiers not yet measured at this step.
> Will be made public only after all 4 PASS at the **final** step.

## What this is

Intermediate LoRA savepoint at **5,000 SFT steps** from anima CLM v4 530M, trained
under the P9 4-loss objective (text CE + tension MSE + BOLD MSE + φ★ hinge floor).

Pushed automatically every 5K steps by the EXEC loop. **Rollback target**: if F2
(φ★ ≥ 5.0) fails at a later checkpoint, training reverts to this step.

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

(Per-combo δ is fixed within an LHS sample; "curriculum" refers to the grid sweep
across the 9 LHS samples of the 81-cell grid α×β×γ×δ.)

## Falsifiers (preregistered, append-only — measured at FINAL step)

| id | metric | pass threshold | fail action |
|---|---|---|---|
| F1 | BLEU-1 vs Llama-3.2-3B holdout | > 0.4 | escalate S2 / larger model |
| F2 | φ★ post-train (HID=8 well-conditioned) | ≥ 5.0 | ABORT combo (irreversible flip) |
| F3 | tension MSE on val | < 0.1 | raise β / lower lr |
| F4 | BOLD Pearson r on val | > 0.5 | raise γ / recheck TRIBE projector |

Verdict logic:
- ALL 4 PASS = **P9_SUCCESS**
- F2 FAIL = **P9_FAIL_PHI** (irreversible)
- F2 PASS ∧ F1 FAIL = **P9_FAIL_CHAT**

## Honest C3

1. This savepoint is a **5K-step intermediate**; F1–F4 are measured only at the
   final step (50K) of the winning combo.
2. φ★ is an L1+L2 proxy. **Phenomenal consciousness (L3) is NOT measured** here.
3. 4-loss Pareto frontier is unverified — LHS-9 of 81 grid is heuristic sampling.
4. Base CLM v4 ckpt access requires `need-singularity/anima-clm-v4-530m` repo
   permission (gated).

## Citation

Anchor: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §65.4 (P9).
