---
id: H_1010
slug: modulus-curriculum
title: Does a curriculum on the MODULUS axis (ring size mod-2→6, not length) at full len=36 crack the H_1005 T3 horizon cap?
domain: cwm · cross-cutting · world-model · learning-method · curriculum-learning · state-space · modulus · horizon · re-test
source: H_1005 (🔴 CURRICULUM-HORIZON-CAPPED — T3 mod-6 ring counter capped at length; H_1003/H_1005 only ever ramped the LENGTH axis) + a_completeness_over_cheap + a_paper_negative_ok + a_scale_honest_scope
exploration_method: E5 (re-run the SAME T3 harness with a DIFFERENT curriculum axis — ramp the ring size, not the length) + a_completeness_over_cheap
verification_method: W2 (pre-registered axis-swap falsifier at full len=36 · GRU/arms VERBATIM · curriculum mod-2→3→4→6 · in_dim FIXED at P_MAX layout · compute-matched 40 ep · eval = full mod-6/len-36 · T2@40 sentinel) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
scope: TOY — T3 at FIXED full break length len=36, curriculum AXIS = ring size P {2,3,4,6} (not length); in_dim FIXED at the P_MAX=6 layout (9 channels) across the whole curriculum. T2@40 sentinel (standard length curriculum). width-rungs {16,32}, 6 seeds, {train 600/test 300}, 40-epoch budget (== H_1005). The ONLY moved lever vs H_1005 = the curriculum axis (modulus instead of length). $0 CPU-local pure-numpy GRU; NO torch. Production transfer UNVERIFIED. NOT a forge binary; nothing on AKIDA.
sister: H_1005 (the length-axis cap this attacks from a different axis), H_1006, H_1003, H_1000, H_985
axes_seed: "the H_1005 T3 cap is about STATE-SPACE granularity, not horizon — ramping the ring size (easy 2-state → hard 6-state) at full length 36, where the length curriculum failed, bootstraps the integrator and cracks T3" ⊥ H_1010 = the cap is about the long-range HORIZON (the 36-step credit chain), NOT the state-space — growing the modulus at full length does not substitute for long-range integration
verdict: PENDING
---

# H_1010 — Modulus-axis curriculum (mod-2→6) at len=36: crack the T3 cap? (learning-method slate)

## 0. Motivation

H_1005 capped T3 (modular path-integration) at **length** while T2 (commutative 1-bit accumulator) scaled — interpreted as: the mod-6 **ring counter's** long-range credit chain is the hard part. But H_1003/H_1005 only ever ramped the **length** axis. This H ramps a **different** axis: the **ring size P** (state-space granularity), at the **full break length 36** throughout. Curriculum mod-2 → mod-3 → mod-4 → mod-6 (a parity-like 2-state counter is easy; the 6-state ring is hard). If the integrator can be bootstrapped by growing the **state-space** at full length (where the length curriculum failed), the cap is about state-space granularity, not horizon.

in_dim is FIXED at the max-P=6 layout (2 move + 1 query + 6 position channels = 9) across the whole curriculum (mod-2 episodes use only the first 2 position channels), so the GRU/LM never see a changing input space — only the number of reachable states grows. Final eval is the SAME full mod-6 / len-36 held-out test as the H_1005 break.

## 1. Hypothesis (one falsifiable claim)

The H_1005 T3 cap is a state-space-granularity limit: a modulus-axis curriculum (mod-2→6) at full len 36 — SAME GRU-WM, capacity, 40-epoch budget, eval — lets the GRU SOLVE T3(mod-6)@36, ≫ chance with d>0.8 vs LM at ≥2 rungs, while keeping T2@40.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-07, BEFORE measurement)

**Setup:** re-run the H_1005 T3 task at full len=36, but the curriculum ramps the **ring size** P∈{2,3,4,6} (advance on the SAME competence threshold, SAME 40-ep budget) instead of the length. in_dim FIXED at the P_MAX layout. T2@40 sentinel via the standard length curriculum. Eval = full mod-6/len-36 (== H_1005 break).

**PASS (frozen):** modulus-curriculum curr-GRU SOLVES T3(mod-6)@36 (≫ chance, d>0.8 at ≥2 rungs) AND keeps T2@40 → **🟢 MODULUS-CURRICULUM-CRACKS-T3-CAP** (different-axis method-shape unlock; cap was state-space, not horizon). **FAIL:** still ≈ chance → **🔴 MODULUS-CURRICULUM-INSUFFICIENT** (cap is the horizon; closed-negative, a_paper_negative_ok).

## 3. Measurement (g5 CODE-measured · no LLM self-judge · `python3 -u` streaming)

`UNIVERSE/h1010_modulus_curriculum.py` → `.verdicts/1010_modulus_curriculum/h1010_modulus_curriculum.txt` (verbatim).

RESULTS_TABLE_PLACEHOLDER

## 4. Finding

FINDING_PLACEHOLDER

**Honest scope:** TOY — T3 full len 36, modulus curriculum {2,3,4,6}, {16,32}, 6 seeds, 40-ep budget (compute-matched). Production / real-corpus transfer UNVERIFIED. NOT a forge binary; $0 CPU-local; nothing on AKIDA (a_scale_honest_scope).

## 5. Sibling / xlinks

- ⇄ [H_1005](./H_1005_curriculum_scaleup.md) (length-axis cap; this attacks from the modulus axis) · [H_1006](./H_1006_dense_supervision.md) · [H_1003](./H_1003_t2t3_curriculum.md) · [H_1000](./H_1000_gru_wm_t2t3.md) · [CWM](../CWM/CWM.md)
- external: curriculum learning along non-length axes (task difficulty / state-space); shaping for modular arithmetic.
