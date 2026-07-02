---
id: H_991
slug: loop-self-correction-reperception
title: Is RE-PERCEPTION the error-corrector for imagination drift — does tracking error rise monotonically with the re-perception interval k (imagine longer between perceptions ⇒ more drift), and does re-perceiving every step bound the drift far below pure open-loop imagination?
domain: cwm · loop · imagine · perceive · drift · self-correction
source: CWM 2nd slate — sharpens H_981🟢 (rollout bounded-but-drifting) + H_990🟢 (closed beats blind open-loop) + V-JEPA/MPC re-planning + a_completeness_over_cheap
exploration_method: E14 (substrate-native) + E5 (re-perception-interval sweep)
verification_method: W2 (pre-registered monotone-drift-vs-interval falsifier · Spearman) + g5 CODE-measured (no LLM self-judge, p7)
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE nonlinear-oscillator tracking rung (a_scale_honest_scope) — hidden velocity + cubic stiffening + process noise so a linear LDS cannot exactly model it; $0 CPU. NOT a forge binary.
sister: H_981 (rollout self-consistency / drift), H_990 (closed loop), H_962 (latent dynamics)
axes_seed: "imagination drift is intrinsic / unfixable" ⊥ "re-perception is the corrector" — locates the MECHANISM by which the closed loop (H_990) beats blind open-loop
verdict: 🟢 PASS — re-perception is the error-corrector: tracking error rises monotonically with imagination interval (Spearman rho=1.00), and re-perceiving every step cuts drift to ~0.00× of pure open-loop (k=30). Toy single-rung, ladder OPEN.
---

# H_991 — re-perception is the error-corrector (drift vs re-perception interval)

## 0. Motivation

H_981🟢 found imagined rollouts are bounded but *drift*; H_990🟢 found the closed loop beats a blind open-loop plan (which compounds error 11×). This H isolates WHY: the cure for imagination drift is RE-PERCEPTION. It sweeps the re-perception interval k — act/track from a fresh perceived latent every k steps, imagining (rolling the latent forward, no input) in between — and asks whether drift is a monotone function of how long the system imagines without looking.

## 1. Hypothesis (one falsifiable claim)

On a hidden-state tracking task, tracking error increases monotonically with the re-perception interval k (more imagination between perceptions ⇒ more drift), and re-perceiving every step (k=1) bounds the error to a small fraction of pure open-loop imagination (k=horizon).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** a nonlinear damped oscillator with process noise (hidden velocity; cubic stiffening so a linear LDS world-model cannot model it exactly ⇒ imagination genuinely accumulates error). Track the trajectory, re-perceiving (resetting the latent from the true recent observations) every k ∈ {1,2,3,5,8,15,30} steps; imagine between. ≥20 seeds.

**Measurement (g5 CODE-measured):**
- D1 = Spearman rho(k, mean tracking error).
- D2 = error(k=1) / error(k=30) ratio.

**Outcome rules (future conditional):**
- IF rho > 0.8 AND error(k=1)/error(k=30) < 1/3 THEN PASS — re-perception bounds drift.
- IF no monotone relationship THEN FAIL — re-perception does not contain drift.

## 3. Honest scope

Toy nonlinear-oscillator rung (a_scale_honest_scope, #123-A). The world model is a delay-embedding linear LDS; the dynamics are deliberately nonlinear so imagination must drift. Single rung, ladder OPEN. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes2/h991_loop_self_correction.py` · verdict: `.verdicts/991_loop_self_correction_reperception/h991_loop_self_correction.txt`

| k (imagine k−1 steps between perceptions) | tracking error |
|---|---|
| 1 | 0.0000 |
| 5 | 0.0175 |
| 15 | 0.0541 |
| 30 (pure open-loop) | 0.0863 |

D1 Spearman rho(k, error) = **1.000** (p=0). D2 error(k=1)/error(k=30) ≈ **0.00** (< 1/3). 24 seeds.

**VERDICT 🟢 PASS** — re-perception is the error-corrector: imagination drift rises monotonically with the interval between perceptions, and perceiving every step nearly eliminates it. This is the mechanism behind H_990's closed-loop win and quantifies H_981's "bounded-but-drifting" (toy rung; ladder OPEN).
