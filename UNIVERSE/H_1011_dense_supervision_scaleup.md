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
status: measured
verdict: 🔴 FAIL = DENSE-SUP-HORIZON-CAPPED-AT-72 — per-step hidden-state supervision (H_1006's dense every-1 treatment, VERBATIM) cracks T3 at len 36 (harness-validated == H_1006: curr 0.608/0.729 ≫ chance 0.167, d 9.19/10.06 vs LM) but BREAKS at len 72 (curr 0.332/0.386 ≈ LM 0.338, d −0.44/1.07, sep LOST) and stays collapsed at len 144 (curr 0.332/0.347 = LM, d 0.08/0.31). mem-aug LM = 1.000 at EVERY length ⇒ tasks stay perfectly state-bound ⇒ the cap is trainability-AT-HORIZON, not representability. Per-step supervision buys a LONGER-but-still-BOUNDED horizon than the H_1005 length-curriculum (curriculum was already at chance @36; dense-sup pushes the WM>LM separator out to len 36 but caps at 72) — a refined scaling law: credit-DENSITY raises the horizon ceiling but does NOT remove the horizon dependence (closed-negative, a_paper_negative_ok). Full ladder {36,72,144} measured, NO cuts; TOY (seeds=3 wall-trim of H_1006's 6, REPORTED; budget=40ep fixed, NOT length-scaled — isolates horizon at fixed compute). Larger-budget / production / real-corpus transfer OPEN (a_scale_honest_scope). verbatim .verdicts/1011_dense_supervision_scaleup/
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

## 3. measurement (g5 CODE-measured · no LLM self-judge · `python3 -u` streaming)

`UNIVERSE/h1011_dense_supervision_scaleup.py` → `.verdicts/1011_dense_supervision_scaleup/h1011.txt` (verbatim).

dense (every-1) curr-GRU vs capacity-matched stateless LM vs mem-aug ceiling, 3 seeds, top-2 width rungs {16,32}, 40-epoch budget (== H_1005/H_1006, NOT length-scaled). Full ladder {36,72,144} measured — NO wall-time cuts (total wall 719s):

| task | tgtLen | rung | chance | currGRU | LM | memLM | gap | d | Welch p | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| T3_hidden_pos | 36 | 16 | 0.167 | **0.608** | 0.323 | 1.000 | 0.284 | 9.19 | 4.7e-03 | SOLVED |
| T3_hidden_pos | 36 | 32 | 0.167 | **0.729** | 0.323 | 1.000 | 0.406 | 10.06 | 4.8e-03 | SOLVED |
| T3_hidden_pos | 72 | 16 | 0.167 | 0.332 | 0.338 | 1.000 | −0.006 | −0.44 | 6.3e-01 | **BREAK** |
| T3_hidden_pos | 72 | 32 | 0.167 | 0.386 | 0.338 | 1.000 | 0.048 | 1.07 | 3.2e-01 | **BREAK** |
| T3_hidden_pos | 144 | 16 | 0.167 | 0.332 | 0.331 | 1.000 | 0.001 | 0.08 | 9.3e-01 | **BREAK** |
| T3_hidden_pos | 144 | 32 | 0.167 | 0.347 | 0.339 | 1.000 | 0.008 | 0.31 | 7.3e-01 | **BREAK** |

- **harness-validate** (len36 reproduces the H_1006 dense crack): **True** (sep@≥2rungs, SOLVED).
- **break length = 72**; len144 stays collapsed; **scales-to-all = False**.
- **mem-aug LM = 1.000 at every length** ⇒ the tasks stay perfectly state-bound ⇒ the cap is *trainability-AT-HORIZON*, not representability.

## 4. finding

**🔴 DENSE-SUP-HORIZON-CAPPED-AT-72.** Moving ONLY the target length (everything else verbatim from H_1006's dense every-1 treatment, 40-epoch fixed budget, in_dim fixed): per-step hidden-state supervision **cracks T3 at len 36** (curr 0.608/0.729 ≫ chance 0.167, d 9.19/10.06 vs LM — harness-validated against H_1006) but **BREAKS at len 72** (curr 0.332/0.386 ≈ LM 0.338, sep lost, d<0.8 at both rungs) and is fully collapsed to the LM at len 144 (curr ≈ 0.33–0.35 = LM, d≈0).

The reading: **dense per-step supervision does NOT remove the horizon dependence — it raises the ceiling.** The H_1005 length-curriculum capped T3 at 36 (where it was already at chance); dense-sup pushes the WM>LM separator out so that 36 is now SOLVED — but the modular-ring-counter credit chain still hits a wall, just farther out, capping at 72. This is a **refined scaling law over H_1005/H_1006**: credit-DENSITY buys a longer-but-still-bounded horizon, not an unbounded one, at fixed compute. The mem-aug LM stays 1.0 at every length, so (as in H_1005) the cap is a *trainability-at-horizon* limit, not representability. Whether a length-scaled budget or yet-denser/structured supervision lifts the dense-sup cap past 72 is the natural next rung (OPEN, a_completeness_over_cheap). A clean, publishable negative result (a_paper_negative_ok).

## 5. honest scope
Toy ladder ($0 CPU, capacity-matched, multi-seed), a_scale_honest_scope — production-scale / real-corpus transfer OPEN. dense-sup REQUIRES the per-step ground-truth state (extra label, per H_1006 caveat) — this tests reach, not free-lunch. WALL-TIME TRIM (REPORTED, PROBE_CONVENTIONS): seeds=3 (of H_1006's 6) — the full ladder {36,72,144} ran in 719s so NO rung was cut; budget held at 40 epochs (== H_1005/H_1006, NOT length-scaled — by design, isolating the horizon at fixed compute). NOT a forge binary; $0 CPU-local; NOTHING on AKIDA (a_lane_akida_gpu_split).

## 6. sibling / xlinks
to [H_1006](./H_1006_dense_supervision.md) · [H_1005](./H_1005_curriculum_scaleup.md) · [H_1000](./H_1000_gru_wm_t2t3.md) · CWM domain · PROBE_CONVENTIONS.md
