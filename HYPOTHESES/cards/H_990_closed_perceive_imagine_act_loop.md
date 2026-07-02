---
id: H_990
slug: closed-perceive-imagine-act-loop
title: Does the full closed perceive→imagine→act→perceive LOOP work end-to-end — composing the 1st-round 🟢 stages (H_960 perceive · H_962 imagine · H_964 act) on ONE shared latent without per-stage retraining — and does closing the loop beat both a reactive controller and a blind open-loop imagined plan?
domain: cwm · loop · composition · perceive · imagine · act · keystone-2nd-slate
source: CWM 2nd slate — composition of H_960🟢/H_962🟢/H_964🟢 (each stage passes alone) + V-JEPA-2-AC latent MPC + Dreamer imagined rollout + a_completeness_over_cheap
exploration_method: E14 (substrate-native) + E5 (closed-loop control task construction)
verification_method: W2 (pre-registered closed-vs-reactive-vs-open-loop falsifier) + g5 CODE-measured (no LLM self-judge, p7)
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE 2D point-to-goal control rung (a_scale_honest_scope) — velocity HIDDEN so a world-state is required; $0 CPU. NOT a forge binary.
sister: H_960 (perceive), H_962 (imagine/latent-dynamics), H_964 (latent→action), H_991 (loop self-correction), H_970 (WM>LM keystone)
axes_seed: "the green stages compose trivially" ⊥ "composition fails / error compounds" — closing the loop is the real test of perceive+imagine+act as ONE engine
verdict: 🟢 PASS — closed loop composes end-to-end: final goal-distance 0.010 < reactive 0.365 (p=1.2e-11, d=-3.56) AND < blind open-loop 0.119; open-loop COMPOUNDS error 11.4×. Toy single-rung, ladder OPEN.
---

# H_990 — closed perceive→imagine→act→perceive LOOP end-to-end

## 0. Motivation

The 1st CWM slate showed each stage passes in isolation: H_960🟢 (modality-agnostic perceive), H_962🟢 (latent forward dynamics / imagine), H_964🟢 (latent→action / act). The skeptic's objection is that passing each stage separately does not mean the *composed* closed loop works — error can compound across stages, or the latent that serves perception may not serve control. This H tests the full **perceive→imagine→act→perceive** loop running on ONE shared latent world-state, with no per-stage retraining, against the two baselines that the loop must beat to justify itself: a reactive controller (no world-state) and a blind open-loop imagined plan (imagine once, execute without re-perceiving).

## 1. Hypothesis (one falsifiable claim)

On a control task where the controller must infer a hidden world-variable (velocity) from a latent state, a closed loop (re-perceive every step, act from the current latent) reaches the goal with final distance strictly below BOTH a reactive position-only controller AND a blind open-loop imagined-plan controller, at matched controller capacity.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** 2D double-integrator point-to-goal; observation = position only, velocity HIDDEN (a world-state is required to control well). Controllers cloned from an LQR-ish expert that sees velocity. arm-CLOSED = act from the re-perceived latent each step. arm-REACTIVE = act from position only (no latent). arm-OPEN = imagine the whole plan from the first observations, execute blind. ≥20 seeds.

**Measurement (g5 CODE-measured):**
- D1 = final goal-distance, CLOSED vs REACTIVE (Welch t).
- D2 = drift containment: open-loop / closed final-distance ratio (does blind imagination compound error?).
- D3 = CLOSED also < OPEN-loop.

**Outcome rules (future conditional):**
- IF closed < reactive (p<0.05) AND closed < open-loop THEN PASS — the loop composes.
- IF closed not < reactive THEN FAIL — the composed loop adds nothing (closed-negative).
- IF n too small THEN INCOMPLETE.

## 3. Honest scope

Toy linear-control rung (a_scale_honest_scope, #123-A). Existence-proof that the loop composes on ONE task; ladder OPEN, no production transfer. Controllers are behavior-cloned (not RL-optimized) to keep $0/deterministic. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes2/h990_closed_loop.py` · verdict: `.verdicts/990_closed_perceive_imagine_act_loop/h990_closed_loop.txt`

| arm | final goal-distance (mean ± std) |
|---|---|
| CLOSED loop (re-perceive+act/step) | **0.0105 ± 0.0066** |
| REACTIVE (position-only, no WM) | 0.3652 ± 0.1379 |
| OPEN-LOOP (commit blind imagined plan) | 0.1189 ± 0.0622 |

D1 closed<reactive: Welch t=-12.32, p=1.2e-11, Cohen d=-3.56. D2 open/closed ratio = **11.38× (open-loop compounds error)**. D3 closed < open-loop: True. Capacity: latent-ctrl 14 params vs position-ctrl 6.

**VERDICT 🟢 PASS** — the closed perceive→imagine→act loop works end-to-end on a shared latent without per-stage retraining; re-perception each step is what beats blind imagined planning (which compounds error 11×). The 1st-round green stages COMPOSE into a working loop (toy rung; ladder OPEN).
