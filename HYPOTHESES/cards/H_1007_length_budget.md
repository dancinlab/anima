---
id: H_1007
slug: length-budget
title: Is the H_1005 T3 horizon cap just a compute-vs-horizon tradeoff (fixed budget at a longer horizon), or a method-shape limit more compute can't buy? — length-proportional epoch budget
domain: cwm · cross-cutting · world-model · learning-method · credit-assignment · compute-budget · horizon · control · re-test
source: H_1005 (🔴 CURRICULUM-HORIZON-CAPPED — held the budget FIXED at 40 ep across all lengths by design; named "whether a larger budget scaled with length lifts the T3 cap" as OPEN) + a_completeness_over_cheap + a_paper_negative_ok + a_scale_honest_scope
exploration_method: E5 (re-run the SAME T3 curriculum with ONLY the total epoch budget changed — scaled proportionally to length) + a_completeness_over_cheap
verification_method: W2 (pre-registered budget-scaling falsifier at len 36 + 72 · GRU/curriculum/arms VERBATIM · budget = 40·len/18 · extra compute REPORTED · T2@40 sentinel) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
scope: TOY — T3@len{36,72} at length-PROPORTIONAL budget (40·len/18 → 80 ep @36, 160 ep @72) + T2@40 sentinel, width-rungs {16,32}, 6 seeds, {train 600/test 300}. The ONLY moved lever vs H_1005 = the TOTAL epoch budget (scaled with length); the EXTRA compute is REPORTED (this is by design — it is the "is the cap just compute?" control). $0 CPU-local pure-numpy GRU; NO torch. Production transfer UNVERIFIED. NOT a forge binary; nothing on AKIDA.
sister: H_1005 (the fixed-budget cap this control tests), H_1006 (dense-supervision lever), H_1003, H_1000, H_985
axes_seed: "the H_1005 T3 cap is just a COMPUTE-vs-horizon tradeoff — scaling the budget proportionally to length gives the long stage enough epochs to bootstrap and cracks T3@36 (the cap is bought back by more compute, NOT a method-shape limit)" ⊥ H_1007 = the cap is a genuine METHOD-SHAPE / credit-assignment limit — even 2-4× the compute does not crack T3@36 (more compute at fixed method is not enough)
verdict: 🔴 FAIL — T3-CAP-IS-NOT-JUST-COMPUTE: length-proportional budget (2.0x@len36, 4.0x@len72) does NOT crack T3 (curr 0.382/0.328, sep@>=2rungs=False); T2@40 kept. Genuine method-shape/long-range-credit limit, not compute. closed-negative (a_paper_negative_ok). toy (a_scale_honest_scope).
---

# H_1007 — Length-proportional epoch budget: is the T3 cap just compute? (learning-method slate)

## 0. Motivation

H_1005 held the total epoch budget **FIXED at 40** across all lengths — by design, to isolate the horizon at fixed compute. Its mechanism finding: the curriculum spends its 40 epochs clearing short stages and arrives at the len-32 stage **too late to bootstrap**. The obvious confound H_1005 itself names as OPEN: maybe T3@36 just needs **more epochs** at the long stage. This H removes that confound — the explicit **"is the unlock just more compute?"** control the mission demands: scale the total budget **proportionally to length** (budget = 40·len/18, so len 36 gets ~80 ep, len 72 gets ~160 ep).

## 1. Hypothesis (one falsifiable claim)

The H_1005 T3 cap is a compute-vs-horizon tradeoff: scaling the budget ∝ length — SAME GRU-WM, capacity, curriculum, eval — lets the GRU SOLVE T3@36, ≫ chance with d>0.8 vs LM at ≥2 rungs, while keeping T2@40. (A PASS here is the HONEST "it's just compute" finding, not a free method-shape unlock.)

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-07, BEFORE measurement)

**Setup:** re-run the H_1005 T3 curriculum at len {36, 72} with the **ONLY** change being the total budget, scaled ∝ length (40·len/18). T2@40 sentinel at its proportional budget. Everything else VERBATIM. The extra compute (epochs per cell) is printed and REPORTED — that IS the finding's content.

**PASS (frozen):** length-proportional-budget curr-GRU SOLVES T3@36 (≫ chance, d>0.8 at ≥2 rungs) AND keeps T2@40 → **🟢 T3-CAP-IS-A-BUDGET-TRADEOFF** (the cap is bought back by more compute; REPORTED, not a free unlock). **FAIL:** still ≈ chance even at 2-4× compute → **🔴 T3-CAP-IS-NOT-JUST-COMPUTE** (genuine method-shape limit; closed-negative, a_paper_negative_ok).

## 3. Measurement (g5 CODE-measured · no LLM self-judge · `python3 -u` streaming)

`UNIVERSE/h1007_length_budget.py` → `.verdicts/1007_length_budget/h1007_length_budget.txt` (verbatim).

RESULTS_TABLE_PLACEHOLDER

## 4. Finding

FINDING_PLACEHOLDER

**Honest scope:** TOY — T3 len {36,72}, {16,32}, 6 seeds; the budget grows with length (REPORTED — the whole point). This isolates compute-vs-method-shape. Production / real-corpus transfer UNVERIFIED. NOT a forge binary; $0 CPU-local; nothing on AKIDA (a_scale_honest_scope).

## 5. Sibling / xlinks

- ⇄ [H_1005](./H_1005_curriculum_scaleup.md) (the fixed-budget cap this control tests directly — answers its named OPEN question) · [H_1006](./H_1006_dense_supervision.md) (dense-supervision lever, compute-matched — contrast: this one spends MORE compute) · [H_1003](./H_1003_t2t3_curriculum.md) · [H_1000](./H_1000_gru_wm_t2t3.md) · [CWM](../CWM/CWM.md)
- external: compute-optimal / budget-vs-horizon scaling for long-range recurrence.
