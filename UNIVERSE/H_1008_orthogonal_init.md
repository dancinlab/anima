---
id: H_1008
slug: orthogonal-init
title: Does ORTHOGONAL recurrent initialization (a long-range gradient-flow trick) crack the H_1005 T3 horizon cap at len≥36?
domain: cwm · cross-cutting · world-model · learning-method · credit-assignment · gradient-flow · orthogonal-init · horizon · re-test
source: H_1005 (🔴 CURRICULUM-HORIZON-CAPPED — T3 cap = long-range credit-assignment through a deep BPTT chain) + a_completeness_over_cheap + a_paper_negative_ok + a_scale_honest_scope
exploration_method: E5 (re-run the SAME T3 harness with ONLY the recurrent-matrix init changed to orthogonal) + a_completeness_over_cheap
verification_method: W2 (pre-registered method-swap falsifier at len=36 · GRU/curriculum/arms VERBATIM from h1003/h1000/h985 · ONLY Uz/Ur/Un init → orthogonal · compute-matched 40 ep, no extra labels · T2@40 sentinel guard) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
scope: TOY — T3@len36 (H_1005 break) + T2@40 sentinel, width-rungs {16,32}, 6 seeds, {train 600/test 300}, 40-epoch budget (== H_1005, NO extra compute or labels). The ONLY moved lever vs H_1005 = recurrent-matrix init (Uz/Ur/Un → random orthogonal via QR). $0 CPU-local pure-numpy GRU; NO torch. Production / real-corpus transfer UNVERIFIED. NOT a forge binary; nothing on AKIDA.
sister: H_1005 (the T3 break this attacks), H_1003, H_1000, H_985
axes_seed: "the H_1005 T3 cap is a long-range GRADIENT-CONDITIONING limit — orthogonal recurrence (unit singular values) lets gradient propagate through the 36-step BPTT chain without vanishing, cracking T3 at len≥36 for FREE (no extra compute/labels)" ⊥ H_1008 = the cap is NOT gradient conditioning — a better-conditioned recurrence alone does not teach the ring counter at 36 steps
verdict: PENDING
---

# H_1008 — Orthogonal recurrent init: crack the H_1005 T3 horizon cap? (learning-method slate)

## 0. Motivation

H_1005 root-caused the T3 cap to **long-range credit assignment** through a deep BPTT chain (the integrator's train-acc collapses at the len-32 ramp stage). The classic single-lever fix for long-range gradient flow in RNNs is **orthogonal recurrent initialization** (Saxe et al. 2014; Le et al. IRNN/np-RNN): an orthogonal recurrent matrix has **unit singular values**, so gradients neither vanish nor explode propagating back through many steps. This is the purest, **free** (no extra labels, no extra compute) method-shape probe: does a long-range-gradient trick alone unlock the horizon?

## 1. Hypothesis (one falsifiable claim)

The H_1005 T3 cap is a gradient-conditioning limit: initializing the GRU's recurrent matrices (Uz, Ur, Un) as orthogonal — SAME everything else (recurrence form, BPTT, Adam, curriculum, capacity, 40-epoch budget, eval) — lets the GRU SOLVE T3 at len 36, ≫ chance with d>0.8 vs LM at ≥2 rungs, while keeping T2@40.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-07, BEFORE measurement)

**Setup:** re-run the H_1005 T3 harness at len=36 (+ T2@40 sentinel). The **ONLY** change vs H_1005 is the recurrent-matrix init: 1/√H Gaussian → random **orthogonal** (QR of a Gaussian, sign-fixed diag for determinism). Everything else VERBATIM. Compute-matched (40 ep, no extra labels). Width-rungs {16,32}, 6 seeds.

**PASS (frozen):** orthogonal-init curr-GRU SOLVES T3@36 (≫ chance, d>0.8 vs LM at ≥2 rungs) AND keeps T2@40 → **🟢 ORTHOGONAL-INIT-CRACKS-T3-CAP** (a FREE method-shape unlock). **FAIL:** still ≈ chance → **🔴 ORTHOGONAL-INIT-INSUFFICIENT** (cap is not gradient conditioning; closed-negative, a_paper_negative_ok).

## 3. Measurement (g5 CODE-measured · no LLM self-judge · `python3 -u` streaming)

`UNIVERSE/h1008_orthogonal_init.py` → `.verdicts/1008_orthogonal_init/h1008_orthogonal_init.txt` (verbatim).

RESULTS_TABLE_PLACEHOLDER

## 4. Finding

FINDING_PLACEHOLDER

**Honest scope:** TOY — single horizon (len 36), {16,32}, 6 seeds, 40-ep budget; this is a free (no-extra-compute, no-extra-label) lever. Production / real-corpus transfer UNVERIFIED. NOT a forge binary; $0 CPU-local; nothing on AKIDA (a_scale_honest_scope, a_lane_akida_gpu_split).

## 5. Sibling / xlinks

- ⇄ [H_1005](./H_1005_curriculum_scaleup.md) · [H_1003](./H_1003_t2t3_curriculum.md) · [H_1000](./H_1000_gru_wm_t2t3.md) · [H_985](./H_985_keystone_scaleup.md) · [CWM](../CWM/CWM.md)
- external: orthogonal/unitary RNN init for long-range gradient flow (Saxe 2014; Arjovsky uRNN 2016; Le IRNN 2015).
