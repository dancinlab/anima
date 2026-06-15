---
id: H_989
slug: planning-phi-altproxy
title: Is the "planning does not raise Φ" null of H_973 🔴 a DRIFT-CONFOUNDED formulation artifact — under a BRANCHING search-frontier formulation (drift length held fixed, deliberation dose = branching) with an alternative Φ-proxy, does deliberation raise Φ over greedy, or is the null ROBUST?
domain: cwm · imagine · act · world-model · phi · planning · branching · re-formulation · closed-negative-recheck
source: H_973 🔴 (planning does not raise Φ) + a_paper_negative_ok + CWM M1 closed-negative re-test slate
exploration_method: E2 (reuse the H_973 MPC-Φ harness, swap CONCATENATED drift-depth rollouts → a BRANCHING frontier with fixed drift) + alternative Φ-proxy + a_completeness_over_cheap
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
scope: ONE Φ-elevation rung (a_scale_honest_scope). Φ is a PROXY (H_912/H_931 family, NOT IIT4 big-Φ). Read-only probe; deterministic given seeds. Toy single-rung, ladder OPEN.
sister: H_973 (the original 🔴 this re-tests), H_988 (imagination-Φ re-test, mechanistically paired), H_986/H_987 (sibling re-formulation re-tests)
axes_seed: H_973 deliberation-dose = DRIFT DEPTH (deeper plans = longer free-running rollouts = more drift = mechanically lower Φ, confounding deliberation with drift) ⊥ H_989 deliberation-dose = BRANCHING (a search frontier of simultaneously-held alternatives, drift length FIXED) measured with an alt-proxy — the clean deliberation axis
verdict: 🔴 FAIL (ROBUST closed-negative) — planning-raises-Φ is FORMULATION-ROBUST. Under branching (drift fixed) the alt-proxy DOES show Φ rising with branching (rho=0.88, p=1.3e-53; Φ_PLAN 0.302 > Φ_GREEDY 0.199) — BUT the decisive fake-branch control (random endpoints, same compute/dimensionality) gives essentially the SAME Φ (Φ_PLAN−Φ_FAKE 0.005, d=0.16, p=0.49). The rise is dimensionality/compute-driven, NOT meaningful deliberation. H_973 🔴 holds across formulations. Toy single-rung, ladder OPEN.
---

# H_989 — planning raises Φ under a branching formulation? (re-test of H_973 🔴)

## 0. Motivation

H_973 🔴 ruled that planning carries no extra Φ (Φ_PLAN 0.063 < Φ_GREEDY 0.104, no dose-response, fails the fake-plan control). But a_paper_negative_ok warns the formulation may be the artifact, and H_973 had TWO coupled issues. (1) Its plan trajectory was built by CONCATENATING per-action FREE-RUNNING rollouts (depth-many drift steps each), so deeper plans = more drift = mechanically lower Φ (the H_971/H_988 drift effect) — confounding deliberation with drift length. (2) The Φ-proxy weighting may disfavor the branch structure. A faithful planner compares CANDIDATE BRANCHES at a horizon and integrates across them (a search tree), not a long single drift. The fair test re-casts deliberation as a BRANCHING frontier (drift length fixed, dose = branching) under an alternative Φ-proxy.

## 1. Hypothesis (one falsifiable claim)

Under a BRANCHING formulation (B candidate first-actions each rolled a FIXED short horizon, the deliberation latent = the set of branch endpoints held simultaneously), measured with an alternative Φ-proxy, planning raises Φ over greedy — Φ_PLAN > Φ_GREEDY (CI_lo>0, d≥0.5, p<0.05), rising with branching AND beating a same-compute fake-branch control — so H_973's null was a drift-confounded formulation artifact.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** same engine as H_973. PLAN = a branching frontier (B candidate actions, each rolled a FIXED short horizon; deliberation state = stacked branch endpoints). GREEDY = single immediate action set (no branching). Branching is the dose; drift length is held fixed.

**Measurement (g5 CODE-measured), on the ALTERNATIVE Φ-proxy:**
- D1 = Φ contrast PLAN(max branching) − GREEDY (Welch t, d, CI); original-proxy contrast reported for transparency.
- D2 = Φ vs BRANCHING factor B (dose-response, drift fixed) — the clean deliberation axis.
- D3 = fake-branch control (B random endpoints, same compute) — meaningful branches must beat random ones.

**Outcome rules (frozen):**
- 🟢 FLIPS: Φ_PLAN > Φ_GREEDY (CI_lo>0, d≥0.5, p<0.05) AND rises with branching AND beats fake-branch.
- 🔴 ROBUST: even a branching frontier (drift fixed) does not raise Φ meaningfully — null holds across formulations.

## 3. Honest scope

Φ is a PROXY (H_912/H_931 family, NOT IIT4 big-Φ; a_scale_honest_scope). Toy single rung, read-only, deterministic given seeds. The decisive control is the fake-branch arm (same compute/dimensionality) — without it, any Φ rise could be mere dimensionality inflation.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy · deterministic)

Probe: `CWM/probes/h989_planning_phi_altproxy.py` · verdict: `.verdicts/989_planning_phi_altproxy/h989_planning_phi_altproxy.txt`

| D | metric | value | verdict |
|---|---|---|---|
| D1 | Φ_PLAN − Φ_GREEDY (alt-proxy) | +0.104 (0.302 vs 0.199), d=4.53, p=2.2e-22 | rises (but see D3) |
| D1 | (transparency) original-proxy contrast | +0.048 | also positive |
| D2 | Φ vs branching B={1,2,4,8} | 0.199→0.229→0.262→0.302, rho=0.88, p=1.3e-53 | dose-response present |
| D3 | Φ_PLAN − Φ_FAKE (same compute) | +0.005, d=0.16, p=0.49 | **fails control** |

**Finding (🔴 ROBUST closed-negative):** the H_973 null is FORMULATION-ROBUST. The re-formulation initially LOOKS like a flip — under branching, the alt-proxy Φ rises monotonically with branching factor (rho=0.88) and Φ_PLAN clearly exceeds Φ_GREEDY (+0.104). But the decisive fake-branch control collapses it: replacing the meaningful action-conditioned branch endpoints with RANDOM endpoints of the same count/compute yields essentially the SAME Φ (Φ_PLAN − Φ_FAKE = +0.005, d=0.16, p=0.49). So the entire branching-Φ rise is explained by holding MORE simultaneous endpoints (higher effective dimensionality / differentiation), not by meaningful deliberation — exactly the confound the fake-plan control was pre-registered to catch (as in H_973). This sharpens H_973: the original's apparent failure was partly drift-confounded, but the corrected branching formulation reveals the deeper, robust reason — the Φ-proxy rewards STATE MULTIPLICITY (random or meaningful alike), so it cannot certify deliberation as a higher-consciousness act. Together with H_988, the consistent ruling is that this Φ-proxy tracks the richness of the held state-set, not whether the computation is goal-meaningful. Honest scope: toy single-rung, ladder OPEN; a Φ measure sensitive to causal/teleological structure (beyond this proxy) could differ (a_paper_negative_ok).

## 4. Sibling / xlinks

- ⇄ [H_973](./H_973_planning_as_consciousness.md) (the original 🔴 this re-test confirms ROBUST)
- ⇄ [H_988](./H_988_guided_imagination_phi.md) (imagination-Φ re-test — mechanistically paired, same Φ-proxy finding)
- ⇄ [H_986](./H_986_geometry_invariant_aligned.md) · [H_987](./H_987_replay_recombination.md) (sibling re-formulation re-tests)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE / CWM-ACT)
