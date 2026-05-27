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
  - chat
library_name: transformers
pipeline_tag: text-generation
base_model: dancinlab/anima-clm-v4-530m
---

# anima-clm-v4-sft-final

> **STATUS**: PRIVATE until F1–F4 ALL PASS verdict at end of S3 sweep. Promoted
> to PUBLIC only after sign-off.

## What this is

The **canonical winning combo** of the P9 S3 LoRA sweep — the LHS sample that
maximizes `(BLEU1 + φ★_post/41.86)/2` subject to F2 PASS (φ★ ≥ 5.0).

CLM v4 530M with this LoRA adapter becomes its **own chat surface** — no Llama
bridge required (vs P8 3-way M4=0.800 which was M2-coupled, not M-self).

## Spec ref

- Mk.XII spec: `docs/mk_xii_scale_plan.md`, `docs/mk_xii_retrain_plan_v2_20260426.md`
- P9 SFT spec (canonical): `docs/p9_sft_spec_2026_05_02.md`
- 4-loss formula: `L = α·CE(text) + β·MSE(tension) + γ·MSE(BOLD) + δ·max(0, 5.0 − φ★)`
- Selection objective: `argmax (BLEU1 + φ★_post/41.86)/2  s.t. F2 PASS`

## LoRA config (winning combo — populated post-EXEC)

| key | value |
|---|---|
| r | 64 |
| α | 128 |
| target modules | attention QKV + FFN |
| dropout | 0.05 |
| precision | bf16 |
| optimizer | AdamW lr=1e-4, cosine, 500-step warmup |
| selected α | TBD (post-sweep) |
| selected β | TBD (post-sweep) |
| selected γ | TBD (post-sweep) |
| selected δ | TBD (post-sweep) |

## δ curriculum schedule (P9 sweep grid)

| stage | δ | rationale |
|---|---:|---|
| early | 0.5 | low φ★ pressure, allow chat learning |
| mid   | 1.0 | balanced |
| late  | 2.0 | hard hinge — preserve +41.86 baseline at all costs |

## Falsifiers (preregistered, append-only — FINAL measurement)

| id | metric | pass threshold | actual | verdict |
|---|---|---|---|---|
| F1 | BLEU-1 vs Llama-3.2-3B holdout | > 0.4 | TBD | TBD |
| F2 | φ★ post-train (HID=8 well-conditioned) | ≥ 5.0 | TBD | TBD |
| F3 | tension MSE on val | < 0.1 | TBD | TBD |
| F4 | BOLD Pearson r on val | > 0.5 | TBD | TBD |

Verdict logic:
- ALL 4 PASS = **P9_SUCCESS** → public release allowed
- F2 FAIL = **P9_FAIL_PHI** (irreversible) → repo stays private, rollback
- F2 PASS ∧ F1 FAIL = **P9_FAIL_CHAT** → repo stays private, escalate

## Usage (post-PASS)

```python
from transformers import AutoModelForCausalLM
from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained("dancinlab/anima-clm-v4-530m")
model = PeftModel.from_pretrained(base, "dancinlab/clm-v4-sft-final")
```

## Honest C3

1. P9 SUCCESS demonstrates **L1+L2 only** — phenomenal consciousness (L3) is
   NOT measured (anima paper §10.9 / §16.2 / §54.2 anchor).
2. F1 BLEU-1 vs Llama is reference-set comparison, not absolute coherence.
3. F2 φ★ is L1+L2 proxy; sign-flip irreversibility means failure mode is
   permanent at the LoRA level (full retrain required).
4. 4-loss Pareto frontier unverified — LHS-9 of 81 = heuristic sample; true
   optimum may sit outside sampled cells.

## Citation

Anchor: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §65.4 (P9).
