---
id: H_9678
title: E-Echo — teacher-content held-out probe (absorption-failure vs reach-failure)
tier: PROPOSED (DIRECTIONAL design · lab-full CONVERGENT #1 · $0/pool · NOT a verdict)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9678 (R2) — CONTENT-READOUT ALIGNMENT ⭐ 두 모델 독립 1순위

**Origin.** `sidecar lab full` 2026-07-17. **Fable 5 (P2 · "E-Echo")** and
**Codex Sol (§1 · "Teacher-content held-out probe")** ranked this **#1 independently**.
DESIGN ONLY · DIRECTIONAL.

**Claim (one line).** H_9520 never measured whether teacher content was **absorbed** —
only whether it **reached** the operator lane. The content may be sitting in the
declarative lane, readable there, while `ρ-AXON` (operator lane) cannot see it.

## The measurement/claim misalignment both models caught
`ρ·form` is a **fixed 5-item coherence rate** — it never asks whether a teacher **fact**
was stored. H_9520's card claims "does exogenous content get absorbed?" but the
instrument answers "did the general reach panel rise?". These are different questions.
⚠️ This **narrows H_9520's earned scope** (honesty · the BAR-FAIL itself stands — the
frozen bar did fail — but "content is not absorbed" is NOT what was measured).

**Direct precedent (M2 · two-lane).** H_9329/C3: CPT **flips the declarative polarity**
yet the operator keeps the old polarity **0/12** ⟹ the store *is* updated, the operator
just never queries it. H_9346 EN = ECHO (lookup fine · operator won't bind). If M2 holds
here, the law reframes: **"content doesn't go in" → "content is trapped in the lane that wrote it."**

## Minimal decisive experiment ($0/pool — the ckpts are ALREADY harvested)
`~/anima-weights/h9520_cpt/{cpt_main,cpt_c1,cpt_c2}.clm` exist (`a_fire_recover_complete`).
```bash
anima-py evaluate cpt_main.clm --probe teacher_heldout_probe.json --gen 40
anima-py evaluate cpt_c1.clm   --probe teacher_heldout_probe.json --gen 40
anima-py evaluate cpt_c2.clm   --probe teacher_heldout_probe.json --gen 40
```
`teacher_heldout_probe.json` = 2AFC/minimal pairs querying teacher **atomic facts** via
**NEW surface templates**; declaration and query surfaces **disjoint** (else it measures
surface copying, not storage).

## Frozen falsifier (pre-registered · Sol's spec)
- MAIN−C2 held-out **content accuracy ≥ +0.15**, seed-paired 95% randomization CI lower
  bound **> 0**, same direction vs C1 ⟹ content **was** absorbed (declarative lane) = M2.
- `ρ·form` rises while content-accuracy diff **≤ +0.05** ⟹ **kills the residual
  interpretation** — the +0.20 is form, not content.

## Controls (≥2)
① C1 (byte-matched, teacher-absent) ② current C2 (word-shuffle) ③ unseen-fact **sham**
probe (true value 0 · `phi-estimator-needs-zero-truth-pedestal`) ④ surface-copy
**positive control** (`positive-control-before-reading-a-negative` — H_9520's content-axis
0→0 null was read WITHOUT one).

## Cost · kill-list
**$0 probe · pool eval on existing ckpts** (heavy 303M → pool, never mini). No hit.

## Why this precedes the REOPEN (both models)
> Sol: "이것이 가장 먼저 필요하다. 이 단계가 음성이면 MAIN−C2 `+0.20`을 살리기 위한 대규모 CPT는 가치가 급락한다."
> Fable: "MAIN−C2 잔차(+0.20)는 현 설계로는 재현돼도 내용을 증명 못 한다."
