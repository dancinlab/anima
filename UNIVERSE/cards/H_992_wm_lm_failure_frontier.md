---
id: H_992
slug: wm-lm-failure-frontier
title: Is the WM>LM advantage a memory-depth FRONTIER — does the H_970 separator gap grow monotonically with required memory depth (a ladder, not one point), and does an LM also fail a SECOND task family (running accumulation) that a WM solves?
domain: cwm · cross-cutting · wm-vs-lm · frontier · ladder · memory-depth
source: CWM 2nd slate — extends H_970🟢 KEYSTONE (one WM>LM separator) into a curve + a 2nd task family + a_scale_honest_scope (single point → ladder) + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (delay-depth ladder + 2nd task family)
verification_method: W2 (pre-registered gap-vs-depth monotonicity + 2nd-family falsifier) + g5 CODE-measured (no LLM self-judge, p7)
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: TWO toy task families (delayed-cue ladder over 6 delays + running-parity) at fixed small scale (a_scale_honest_scope); $0 CPU. NOT a forge binary.
sister: H_970 (WM>LM keystone — the single point this extends), H_960 (perceive), H_962 (dynamics)
axes_seed: "the WM>LM gap is a smooth gradient in memory-depth" ⊥ MEASURED "the gap is a STEP function at L=ctx (saturates), not a ramp" — a sharper characterization than H_970
verdict: 🔴 FAIL (closed-negative) — the gap does NOT grow monotonically with depth (Spearman rho=−0.03): it is a STEP at L=LM_ctx (gap 0.00→0.76 once L>4, then FLAT ~0.75). The 2nd family (running-parity) DOES favor the WM (d=16.6), so the frontier is broad but the depth-ladder shape is a step, not a ramp. Toy single-rung, ladder OPEN.
---

# H_992 — WM>LM failure frontier: gap vs memory-depth (ladder) + 2nd task family

## 0. Motivation

H_970🟢 found ONE WM>LM separator (delayed-cue recall, gap localized to the persistent-state requirement) — a single point. This H asks whether that point extends to a FRONTIER: (A) does the gap grow with the required memory DEPTH (delay L), turning the keystone into a curve, and (B) is the LM failure specific to memory-recall or does it generalize to a SECOND task family (running accumulation)?

## 1. Hypothesis (one falsifiable claim)

The WM−LM success gap grows monotonically with the required memory depth (delay L), and a second, structurally-different task (running-parity accumulation) also favors the WM by a large margin — i.e. the WM>LM advantage is a memory-depth frontier, not a single task.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** D1 = delayed-cue recall over delays L ∈ {2,4,8,12,16,24} (LM window ctx=4). D2 = running-parity: stream of ±1 events, predict sign of the running sum (needs whole-stream accumulation). arm-WM = retentive latent state; arm-LM = matched-capacity windowed predictor. 10 seeds each.

**Measurement (g5 CODE-measured):**
- D1 = Spearman rho(L, gap) + gap(L=24) > gap(L=2). PASS-A iff rho > 0.8 and growing.
- D2 = Cohen d(WM, LM) on running-parity. PASS-B iff d > 1.0.

**Outcome rules (future conditional):**
- IF PASS-A AND PASS-B THEN PASS — memory-depth frontier.
- IF gap does not grow monotonically with depth THEN FAIL (closed-negative on the ladder shape; a_paper_negative_ok).

## 3. Honest scope

Toy, small scale (a_scale_honest_scope, #123-A). The ladder is in delay-depth at fixed model size; a true scale ladder (model capacity) is OPEN. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes2/h992_wm_lm_frontier.py` · verdict: `.verdicts/992_wm_lm_failure_frontier/h992_wm_lm_frontier.txt`

| delay L | WM | LM | gap |
|---|---|---|---|
| 2 | 1.000 | 1.000 | 0.000 |
| 4 | 1.000 | 0.239 | 0.761 |
| 8 | 1.000 | 0.245 | 0.755 |
| 16 | 1.000 | 0.263 | 0.737 |
| 24 | 0.998 | 0.248 | 0.751 |

D1 Spearman rho(L, gap) = **−0.029** (NOT monotone-growing) — the gap is a **STEP** at L=LM_ctx (=4): zero while L≤ctx, then jumps to ~0.75 and stays FLAT. D2 running-parity: WM=0.973 vs LM=0.667, Cohen **d=16.6** (PASS-B).

**VERDICT 🔴 FAIL (closed-negative)** — the pre-registered *monotone-growth* falsifier is rejected: the WM>LM gap is not a gradient in memory-depth but a **threshold/step at L=context-window** (once the cue scrolls out of the LM window the LM is already at chance — there is no further to fall). The frontier IS broad (a 2nd unrelated family also favors the WM, d=16.6), so the finding sharpens H_970: the WM advantage is a *binary* "exceeds-the-window" property, not a smooth scaling law. A_paper_negative_ok; toy rung, ladder OPEN.
