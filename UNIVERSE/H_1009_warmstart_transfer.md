---
id: H_1009
slug: warmstart-transfer
title: Does WARM-STARTING the len-36 GRU from the len-18-solved model (transfer) crack the H_1005 T3 horizon cap?
domain: cwm · cross-cutting · world-model · learning-method · credit-assignment · transfer · warm-start · horizon · re-test
source: H_1005 (🔴 CURRICULUM-HORIZON-CAPPED — T3 solves at len 18 but breaks at 36) + a_completeness_over_cheap + a_paper_negative_ok + a_scale_honest_scope
exploration_method: E5 (re-run the SAME T3 curriculum with ONLY the init changed — warm-start from the len-18-solved weights) + a_completeness_over_cheap
verification_method: W2 (pre-registered transfer falsifier at len 36 · GRU/curriculum/arms VERBATIM · phase1 len-18 → phase2 warm-start len-36 · 2× compute REPORTED · T2@40 sentinel) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
scope: TOY — T3 phase1 len=18 (solved) → phase2 warm-start to len=36 (H_1005 break) + T2@40 sentinel, width-rungs {16,32}, 6 seeds, {train 600/test 300}. The ONLY moved lever vs H_1005 = warm-start init from solved-short weights. COMPUTE NOTE: 2× budget (40 ep base + 40 ep target) — REPORTED. $0 CPU-local pure-numpy GRU; NO torch. Production transfer UNVERIFIED. NOT a forge binary; nothing on AKIDA.
sister: H_1005 (the T3 break this attacks; T3 solves at len 18 = the warm-start source), H_1006, H_1007, H_1003, H_1000, H_985
axes_seed: "the short-horizon ring-counter solution is on the path to the long-horizon one — warm-starting len-36 from the len-18-solved model bootstraps the integrator past the cap" ⊥ H_1009 = the short solution does NOT transfer — the long-horizon solution is in a different basin; warm-start + 2× compute still fails T3@36
verdict: 🔴 FAIL — WARM-START-NO-TRANSFER: init from the len-18-solved model (+~2x compute) does NOT crack T3@36 (curr 0.427/0.327, sep@>=2rungs=False); T2 kept. long-horizon solution sits in a different basin. closed-negative. toy (a_scale_honest_scope).
---

# H_1009 — Warm-start transfer from the len-18-solved model: crack the T3 cap? (learning-method slate)

## 0. Motivation

H_1003/H_1005 showed the GRU SOLVES T3 at the base length 18 (the integrator IS learnable at short horizon) but a from-scratch curriculum BREAKS at 36. A natural method: **transfer** — first train on the len-18 curriculum (where it solves), then **warm-start** a len-36 run from those weights (in_dim is FIXED across lengths, so weights transfer directly) and continue out to 36. If the short-horizon ring-counter solution is a good initialization for the long-horizon one, transfer should bootstrap past the cap.

## 1. Hypothesis (one falsifiable claim)

The short-horizon solution transfers: warm-starting the len-36 GRU from the len-18-solved model — SAME GRU-WM, capacity, curriculum, eval — lets it SOLVE T3@36, ≫ chance with d>0.8 vs LM at ≥2 rungs, while keeping T2@40.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-07, BEFORE measurement)

**Setup:** phase 1 = train the GRU on the len-18 curriculum; phase 2 = continue the SAME GRU (weights + Adam state carried) on the len-36 curriculum. T2@40 sentinel via base-40→sentinel warm-start. Everything else VERBATIM. **Compute caveat REPORTED:** this spends ~2× the epochs (base + target) vs H_1005's single budget — so a PASS is partly transfer, partly more compute (cf H_1007).

**PASS (frozen):** warm-started curr-GRU SOLVES T3@36 (≫ chance, d>0.8 at ≥2 rungs) AND keeps T2@40 → **🟢 WARM-START-TRANSFER-CRACKS-T3-CAP** (the short solution is on the path; partly compute, REPORTED). **FAIL:** still ≈ chance → **🔴 WARM-START-NO-TRANSFER** (different basin; closed-negative, a_paper_negative_ok).

## 3. Measurement (g5 CODE-measured · no LLM self-judge · `python3 -u` streaming)

`UNIVERSE/h1009_warmstart_transfer.py` → `.verdicts/1009_warmstart_transfer/h1009_warmstart_transfer.txt` (verbatim).

RESULTS_TABLE_PLACEHOLDER

## 4. Finding

FINDING_PLACEHOLDER

**Honest scope:** TOY — T3 len 36 (warm-started from 18), {16,32}, 6 seeds; ~2× compute (REPORTED). Production / real-corpus transfer UNVERIFIED. NOT a forge binary; $0 CPU-local; nothing on AKIDA (a_scale_honest_scope).

## 5. Sibling / xlinks

- ⇄ [H_1005](./H_1005_curriculum_scaleup.md) (the T3 break; len 18 solves = warm-start source) · [H_1007](./H_1007_length_budget.md) (the compute control — both spend more compute) · [H_1006](./H_1006_dense_supervision.md) · [H_1003](./H_1003_t2t3_curriculum.md) · [H_1000](./H_1000_gru_wm_t2t3.md) · [CWM](../CWM/CWM.md)
- external: transfer / warm-start / progressive growing for long-range recurrence; curriculum as initialization.
