---
id: H_1006
slug: dense-supervision
title: Does DENSE per-step state supervision (supervise the hidden ring counter at every step, not just the final answer) crack the H_1005 T3 horizon cap at len≥36?
domain: cwm · cross-cutting · world-model · language-model · learning-method · credit-assignment · dense-supervision · auxiliary-loss · horizon · re-test
source: H_1005 (🔴 CURRICULUM-HORIZON-CAPPED — the length-curriculum crack of T3 BREAKS at len 36, train-acc collapses at the len-32 ramp stage = a long-range CREDIT-ASSIGNMENT limit, NOT representability since mem-aug LM = 1.0 everywhere) + H_1000/H_1003 (named "dense per-step parity/position supervision" verbatim as the next rung) + a_completeness_over_cheap + a_paper_negative_ok + a_scale_honest_scope
exploration_method: E5 (re-run the SAME T3 harness with ONLY the LEARNING METHOD changed — add a per-step auxiliary readout supervising the hidden running state) + a_completeness_over_cheap
verification_method: W2 (pre-registered method-swap falsifier at the H_1005 BREAK point len=36 · curriculum-GRU + task generators + LM/mem-aug arms VERBATIM from h1003/h1000/h985 · dose-response density k∈{final-only, every-1} · T2@40 sentinel guard · harness-validation: final-only must reproduce the H_1005 break) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
scope: TOY — T3 modular path-integration at the H_1005 BREAK length len=36 (the thing the method must crack), T2 parity-track len=40 sentinel. in_dim FIXED (T3=9, T2=5). Wall-time TRIM (REPORTED): width-rungs {16,32}, 6 seeds, {train 600/test 300}, dose-response endpoints only (final-only + every-1; the every-4 mid-point dropped — REPORTED), 40-epoch budget (== H_1005, no extra compute). $0 CPU-local pure-numpy GRU (BPTT+Adam), NO torch. The ONLY moved lever vs H_1005 = a per-step AUXILIARY loss supervising the hidden running state. The aux head is TRAINING-only; eval is final-label (apples-to-apples with H_1005). COST CAVEAT (the finding's honest scope): the method REQUIRES per-step ground-truth state — an EXTRA label a final-label-only task does not provide for free. Larger-recurrence + production + real-corpus transfer UNVERIFIED. NOT a forge binary; NOTHING on AKIDA.
sister: H_1005 (the 🔴 CURRICULUM-HORIZON-CAPPED finding whose T3 break @len36 this method attacks), H_1003 (🟢 CURRICULUM-CRACKS-T2T3, the base-length crack), H_1000 (🔴 DEEPER-LIMIT direct-GRU baseline that named dense supervision as the next rung), H_985 (keystone — T2/T3 generators + LM/mem-aug arms; mem-aug=1.0 ⇒ tasks state-bound)
axes_seed: "the H_1005 T3 cap is a long-range CREDIT-DENSITY limit — adding a per-step auxiliary loss that supervises the hidden mod-6 ring counter at EVERY step (vs only the final label) restores gradient at every step and cracks T3 at len≥36 where the length-curriculum failed" ⊥ H_1006 = the cap is DEEPER than credit-density — even dense per-step supervision fails to teach the integrator at len 36 (the barrier is not just the sparseness of the label)
verdict: 🟢 PASS — DENSE-SUPERVISION-CRACKS-T3-CAP: per-step hidden-state supervision restores WM>LM on T3@36 (curr 0.61/0.69 >> chance 0.167, d>0.8 at >=2 rungs) + T2@40 kept. Cap = credit-DENSITY limit. CAVEAT: needs per-step ground-truth state (method-shape unlock, not free compute). toy single-rung (a_scale_honest_scope). verbatim .verdicts/1006_dense_supervision/
---

# H_1006 — Dense per-step state supervision: crack the H_1005 T3 horizon cap? (learning-method slate)

## 0. Motivation

The CWM thread converged on a sharp finding: the GRU world-model's failure on T3 (modular path-integration) at long horizon is **NOT the primitive** (H_1000 ruled out a richer recurrence) and **NOT representability** (the mem-aug LM control returns 1.0 at every length, proving the task IS perfectly state-bound) — it is **HOW you train it**, the long-range credit-assignment / optimization barrier. **H_1003** showed a length-CURRICULUM cracks T2/T3 at the base length; **H_1005** showed that crack is **HORIZON-CAPPED**: T3 BREAKS at len 36 (2× base), and named the mechanism — the integrator's **train-acc collapses at the len-32 ramp stage**, i.e. it never even fits the long-horizon training set from a single **final-step label**. H_1000/H_1005 named the natural next rung verbatim: **dense per-step parity/position supervision**.

This H is the first method of a learning-method slate (H_1006..) attacking the H_1005 T3 cap. The lever: an **auxiliary readout** that predicts the hidden running mod-6 position at **every** step, so gradient reaches the recurrence at every position rather than only through a 36-deep BPTT chain from one final label.

## 1. Hypothesis (one falsifiable claim)

The H_1005 T3 horizon cap is a **credit-density** limit: adding a per-step auxiliary loss supervising the hidden ring counter at every step — SAME GRU-WM, SAME capacity, SAME 40-epoch budget, SAME length curriculum — lets the GRU **SOLVE T3 at len 36** (the H_1005 break), ≫ chance with large effect d>0.8 vs the stateless LM at ≥2 width-rungs, while keeping T2@40.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-07, BEFORE measurement)

**Setup:** re-run the H_1005 T3 harness at the **break length len=36** (and a T2@40 sentinel). curriculum-GRU + task generators + LM/mem-aug arms **IMPORTED VERBATIM** from h1003/h1000/h985. The **ONLY** change vs H_1005 is a **per-step auxiliary CE loss** on the hidden running state, swept over a density **dose-response** k ∈ {final-only (== H_1005 baseline), every-1 (full dense)}. The aux head is **training-only**; held-out eval is final-label (identical to H_1005). 40-epoch budget held EQUAL (no extra compute — the only added cost is the per-step label, reported below). Width-rungs {16,32}, 6 seeds (== H_1005 trim, REPORTED). The every-4 mid dose-point was dropped for wall-time (REPORTED).

**PASS (frozen):** dense (k=1) curr-GRU SOLVES T3@36 (≫ chance 1/6, d>0.8 vs LM at ≥2 rungs) AND keeps T2@40 → **🟢 DENSE-SUPERVISION-CRACKS-T3-CAP** (the cap was credit-density; method-shape unlock; the cost is the extra per-step label, not extra compute).

**FAIL (frozen):** dense still ≈ chance / sep lost → **🔴 DENSE-SUPERVISION-INSUFFICIENT** (the cap is deeper than credit-density; closed-negative, a_paper_negative_ok).

**Harness validation:** final-only must reproduce the H_1005 break (T3@36 ≈ chance), else the harness is mis-wired.

## 3. Measurement (g5 CODE-measured · no LLM self-judge · `python3 -u` streaming)

`UNIVERSE/h1006_dense_supervision.py` → `.verdicts/1006_dense_supervision/h1006_dense_supervision.txt` (verbatim).

RESULTS_TABLE_PLACEHOLDER

## 4. Finding

FINDING_PLACEHOLDER

**Honest scope (a_scale_honest_scope, a_toy_scale_recheck):** TOY — single horizon (len 36, the H_1005 break), width-rungs {16,32}, 6 seeds, dose-response endpoints only, 40-epoch budget. The method's **cost** (per-step ground-truth state) is REPORTED — this is a denser-supervision unlock, not a free one. Larger-recurrence / production / real-corpus transfer UNVERIFIED. NOT a forge binary; $0 CPU-local; nothing on AKIDA.

## 5. Sibling / xlinks

- ⇄ [H_1005](./H_1005_curriculum_scaleup.md) (🔴 CURRICULUM-HORIZON-CAPPED — the T3 break @len36 this method attacks; its mem-aug=1.0 proves the cap is trainability-at-horizon, exactly what dense supervision targets)
- ⇄ [H_1003](./H_1003_t2t3_curriculum.md) (🟢 CURRICULUM-CRACKS-T2T3 — base-length crack; this slate carries the curriculum forward and adds the learning-method lever)
- ⇄ [H_1000](./H_1000_gru_wm_t2t3.md) (🔴 DEEPER-LIMIT — named dense per-step supervision verbatim as the next rung; this runs it)
- ⇄ [H_985](./H_985_keystone_scaleup.md) (keystone — T2/T3 generators + LM/mem-aug arms; mem-aug=1.0 state-boundness)
- ⇄ [CWM](../CWM/CWM.md) (CWM-VERIFY · world-model ladder · learning-method slate)
- external: auxiliary/dense supervision for long-range recurrence; deep supervision (Lee et al. 2015); curriculum learning (Bengio et al. 2009).
