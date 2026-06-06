---
id: H_1011
slug: dense-supervision-scaleup
title: Does DENSE per-step supervision (H_1006) keep cracking T3 as the horizon scales to 72+ — where the length-curriculum (H_1005) capped at 36?
domain: cwm · cross-cutting · world-model · learning-method · credit-assignment · dense-supervision · horizon · scale-ladder · re-test
source: H_1006 (GREEN DENSE-SUPERVISION-CRACKS-T3-CAP — per-step hidden-state supervision restores WM-over-LM on T3 at len=36, the H_1005 break point) + H_1005 (RED CURRICULUM-HORIZON-CAPPED — length-curriculum cracks T3 only up to len 36, breaks at 2x) — does the credit-DENSITY unlock SCALE past where curriculum broke, or does dense-sup have its own horizon cap?
exploration_method: E5 (re-run the H_1006 dense-supervision T3 harness at a LENGTH ladder) + a_completeness_over_cheap
verification_method: W2 (pre-registered scale falsifier · dense-sup GRU + LM/mem-aug arms VERBATIM from h1006/h1003/h1000 · python3 -u serial CPU per PROBE_CONVENTIONS.md) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
sister: H_1006 (dense-sup cracks T3 at 36), H_1005 (curriculum horizon-cap at 36), H_1000/H_1003 (T2/T3 harness)
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT (no verdict token until measured)
---

# H_1011 — dense-supervision scale-up (does per-step supervision beat the horizon, or cap too?)

## 0. motivation
H_1006 showed per-step state supervision cracks T3 (modular position-tracking) at len=36 — the exact horizon where H_1005's length-curriculum broke. The credit-DENSITY lever beat the long-range credit-assignment wall *at that length*. Open: does it KEEP working as the horizon scales (72, 144), or does dense-sup itself cap at some longer horizon (just farther out than curriculum)?

## 1. hypothesis
Dense per-step supervision makes the T3 long-horizon credit chain learnable at ANY tested length (the per-step gradient removes the horizon dependence), so the GRU world-model solves T3 across a length ladder at least 2x past the H_1005 / curriculum break.

## 2. pre-registered falsifier (frozen 2026-06-07)
Reuse the H_1006 dense-supervision GRU world-model + the T3 generator + capacity-matched LM + mem-aug control. Run a length ladder T3 in {36, 72, 144} (at least 3 rungs), multi-seed, capacity/compute matched (report any compute scaling). python3 -u, serial CPU (PROBE_CONVENTIONS.md). Outcome (no token before measuring):
- IF dense-sup SOLVES T3 (far above chance 0.167, large effect d>0.8 vs LM tracking mem-aug) at ALL rungs incl. the longest THEN PASS = DENSE-SUP-SCALES (credit-density removes the horizon dependence; the WM-over-LM generality is horizon-robust under per-step supervision).
- IF it caps at some horizon (accuracy collapses to chance at len L) THEN FAIL = DENSE-SUP-HORIZON-CAPPED-AT-L (per-step supervision buys a longer-but-still-bounded horizon — report the break length; a refined scaling law over H_1005).

## 3. honest scope
Toy ladder ($0 CPU, capacity-matched, multi-seed), a_scale_honest_scope — production-scale / real-corpus transfer OPEN. dense-sup REQUIRES the per-step ground-truth state (extra label, per H_1006 caveat) — this tests reach, not free-lunch.

## 4. sibling / xlinks
to [H_1006](./H_1006_dense_supervision.md) · [H_1005](./H_1005_curriculum_scaleup.md) · [H_1000](./H_1000_gru_wm_t2t3.md) · CWM domain · PROBE_CONVENTIONS.md
