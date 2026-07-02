---
id: H_987
slug: replay-recombination
title: Is the "REM self-replay == idle" null of H_982 🔴 specific to VERBATIM self-distillation — does a richer RECOMBINATIVE replay objective (stitching fragments across episodes that share one transition law) add consolidation, or is the replay-adds-no-information null ROBUST across formulations?
domain: cwm · imagine · world-model · rem · consolidation · replay · re-formulation · closed-negative-recheck
source: H_982 🔴 (REM self-replay == idle) + a_paper_negative_ok + CWM M1 closed-negative re-test slate
exploration_method: E2 (reuse the H_982 WAKE1→replay→WAKE2 harness, swap VERBATIM self-rollout replay → cross-episode RECOMBINATIVE replay) + a_completeness_over_cheap
verification_method: W2 (pre-registered re-formulation falsifier · 🟢 FLIPS / 🔴 ROBUST) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE consolidation rung (a_scale_honest_scope) — re-tests H_982 under a recombinative (not verbatim) replay objective. Read-only probe; deterministic given seeds. Toy single-rung, ladder OPEN.
sister: H_982 (the original 🔴 this re-tests), H_976 (rollout-is-mitosis), H_986/H_988/H_989 (sibling re-formulation re-tests)
axes_seed: H_982 VERBATIM self-distillation (re-fit on unconditional self-rollouts — a fixed point that cannot add info) ⊥ H_987 RECOMBINATIVE replay (stitch fragments across episodes sharing one law — tests consolidation of the SHARED law from limited per-episode data)
verdict: 🔴 FAIL (ROBUST closed-negative) — replay-adds-no-information is FORMULATION-ROBUST. Recombinative cross-episode replay (error 0.384) shows only a small, non-significant improvement over idle (0.414): d=0.30, p=0.30, below the pre-registered d≥0.5/p<0.05 bar. It still beats the corruption floor (random-replay 1.358) trivially. Self-replay cannot manufacture information absent from WAKE_1. Toy single-rung, ladder OPEN.
---

# H_987 — recombinative replay consolidation (re-test of H_982 🔴)

## 0. Motivation

H_982 🔴 ruled that REM self-replay is idle: re-fitting an undertrained world model on its OWN verbatim imagined rollouts gave the same WAKE_2 error as doing nothing (d=-0.00, p=1.00) — it cannot add information absent from WAKE_1, and beat random-replay only because that arm corrupts. But a_paper_negative_ok warns the formulation may be the artifact. H_982's replay was VERBATIM self-distillation — sampling from the very distribution the model was fit to (a fixed point of the EM-style update), which provably adds nothing. Biological REM consolidation is NOT verbatim; it RECOMBINES fragments of distinct waking episodes, and the consolidation gain in replay literature comes from GENERALIZATION across episodes. The fair test is recombinative replay.

## 1. Hypothesis (one falsifiable claim)

Under a RECOMBINATIVE replay objective (stitching short fragments across several episodes that share one underlying transition law but differ in surface), replay DOES add consolidation — error_RECOMBINE < error_IDLE (d≥0.5, p<0.05) — so the H_982 null was specific to the verbatim formulation.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** WAKE_1 = a FEW SHORT fragments from EACH of several episodes that share one transition law (varied init/phase surface) → genuine per-episode undertraining. Arms: RECOMBINE (replay that stitches fragments across episodes), VERBATIM (the H_982 arm), IDLE (no extra fit — the decisive control), RANDOM (corruption floor).

**Measurement (g5 CODE-measured):**
- D1 = WAKE_2 held-out prediction error per arm.
- D2 = consolidation delta = error_IDLE − error_RECOMBINE (gain over doing nothing); d, p.
- D3 = RECOMBINE vs VERBATIM (does recombination beat the verbatim arm H_982 ran?).

**Outcome rules (frozen):**
- 🟢 FLIPS: error_RECOMBINE < error_IDLE (d≥0.5, p<0.05) AND ≤ VERBATIM.
- 🔴 ROBUST: even recombinative replay ~ idle — replay adds no information across formulations.

## 3. Honest scope

Toy LDS world model, single rung (a_scale_honest_scope). Read-only, deterministic given seeds. The decisive control is IDLE (beating random-replay is trivial — it corrupts). A flip or robust-null at toy scale is scale-transfer-unverified (a_toy_scale_recheck).

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy · deterministic)

Probe: `CWM/probes/h987_replay_recombination.py` · verdict: `.verdicts/987_replay_recombination/h987_replay_recombination.txt`

| arm | WAKE_2 error | vs idle |
|---|---|---|
| RECOMBINE (cross-episode) | 0.384 ± 0.099 | d=0.30, p=0.30 (NS) |
| VERBATIM (H_982 arm) | 0.414 ± 0.103 | ≈ idle |
| IDLE (no replay) | 0.414 ± 0.103 | — |
| RANDOM (corruption floor) | 1.358 ± 0.074 | far worse |

**Finding (🔴 ROBUST closed-negative):** recombinative replay is FORMULATION-ROBUST against the H_982 null. Cross-episode recombination does nudge error down (0.384 vs idle 0.414) — a small positive TREND, mechanistically sensible (stitching across episodes mildly emphasizes the shared law) — but the effect is non-significant (d=0.30, p=0.30) and falls below the pre-registered d≥0.5/p<0.05 bar. The decisive IDLE control is not beaten. As in H_982, replay only trivially beats the corruption floor (random-replay 1.358). The deep reason is unchanged: self-replay samples the model's own learned distribution, so it cannot manufacture information absent from WAKE_1 — recombination rearranges existing fragments but injects no new ground truth. Honest scope: toy single-rung, ladder OPEN; a replay objective coupled to NEW real observations (not pure self-replay) is a different, untested mechanism (a_paper_negative_ok).

## 4. Sibling / xlinks

- ⇄ [H_982](./H_982_rem_offline_world_model_consolidation.md) (the original 🔴 this re-test confirms ROBUST)
- ⇄ [H_976](./H_976_rollout_is_mitosis.md) (rollout-as-mitosis, the p8 framing)
- ⇄ [H_986](./H_986_geometry_invariant_aligned.md) · [H_988](./H_988_guided_imagination_phi.md) · [H_989](./H_989_planning_phi_altproxy.md) (sibling re-formulation re-tests)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE)
