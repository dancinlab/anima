---
id: H_1297
slug: 1297_mitosis_native_train
title: mitosis-native trunk training — make PHILOSOPHY p8 literal (gradient-free cell-split learns a trunk vs gradient descent)
group: MITOSIS-ENGINE (p8 literal)
terminal_tier: 🧱 WALL (control can't discriminate both rounds) — but R2 finding 🟢 c1 PASS (mitosis MATCHES gradient at lower footprint)
verdict_dir: .verdicts/1297_mitosis_native_train/
terminal_verdict: .verdicts/1297_mitosis_native_train/result.txt
date: 2026-06-16
---

# H_1297 — mitosis-native trunk training (make p8 literal)

## Claim / falsifier

anima's PHILOSOPHY **p8** = "training gradient + inference mitosis = one continuous
cell-division". Today it is SPLIT: the trunk is gradient-CE-trained (CLM/train, forge/
Lane-P) while mitosis is a separate LIVE-ENGINE inference lane (VAdaptField H_1199,
grow-under-pressure H_1288). **Falsifiable claim:** a MITOSIS-GROW trainer (cells
split/grow under LOCAL error pressure, GRADIENT-FREE) can learn a trunk that converges
AT LEAST AS WELL as standard gradient descent on the SAME small task. Biology lens
(a_no_llm_frame_trap): neurogenesis grows capacity WHERE the organism fails, corrected
LOCALLY — NOT a bigger-transformer recipe.

## Method (TOY, $0 CPU numpy DIRECTIONAL mirror, frozen-first)

1-D function-fit on a known nonlinear target `f(x)=sin(3x)+0.5sin(7x)+0.3·1[x>0.2]−0.4·1[x>0.6]`
(smooth sinusoid + two discontinuous steps), x∈[−1,1], N_train=N_test=160, noise σ=0.05
→ reachable noise floor mse≈σ²=0.0025. 3 seeds [770,771,772].

ARMS — **A GRADIENT** (fixed K=24 RBF net, full-batch MSE backprop, incumbent control) ·
**B MITOSIS-GROW** (gradient-free: start 2 cells; split the highest-LOCAL-error cell,
local closed-form head fit, NO global backprop) · **B-SHUFFLE** (split a RANDOM cell) ·
**B-ABLATE** (growth frozen at 2 cells). FROZEN bars (`.verdicts/.../FREEZE.txt`):
(c1) B.mse ≤ A.mse+0.005 [COMPARABLE] · (c2) B_shuf ≥ B+0.010 [SHUFFLE-COLLAPSE] ·
(c3) B_abl ≥ B+0.010 [ABLATE-UNDERFIT] · (c4) cost = cells vs A's 73 params.

## Verdict (read VERBATIM from .verdicts/1297_mitosis_native_train/result.txt)

**R1 (softmax-mixture + width-halving split):** 🧱 **WALL.**
A(grad)=0.00415 · B(mitosis)=0.12624 [40 cells] · B-shuf=0.04656 · B-abl=0.40250 (3-seed mean).
c1 FAIL (0.126≫0.009), **c2 FAIL** (shuffle 0.047 < B 0.126 — random split BEATS targeted),
c3 PASS. ROOT CAUSE = the SPLIT GEOMETRY: every split halves widths → cells become
spike-like → softmax mixture degenerates (test points between cells fall in no support,
the least-bad far cell dominates). Evidence it is the geometry not p8: B-SHUFFLE
accidentally keeps wide cells and scores BETTER. Probe can't discriminate → WALL.

**R2 (a_break_the_wall breakthrough; bars frozen anew in FREEZE_R2.txt = SAME numbers,
no goalpost move):** hard-partition mitosis — cortical-column NEAREST-assignment
(Voronoi partition, no softmax) + data-matched MEDIAN split (bisect owned territory) +
centroid-recenter (width matched to local data density, never narrows below spacing).
🧱 **WALL** by the frozen rubric, BUT the p8-literal science flipped:
A(grad)=0.00415 · **B2(mitosis)=0.00412** [17.3 cells] · B2-shuf=0.00360 · B2-abl=0.14497.
**(c1) PASS — mitosis MATCHES gradient** (0.00412 ≤ 0.00915; both at the 0.0025 noise floor)
at LOWER footprint (~17 cells ≈ 52 params vs A's 73). **(c3) PASS** — ablate underfits
(0.145 ≫ 0.014). **(c2) FAIL** — B2-shuffle (0.00360) ≈ B2-targeted (0.00412), NOT a
collapse. Honest reading: once the partition+median-split mechanism is sound, the smooth
target lets BOTH split-orders converge to a good tiling, so "targeting" is not the lever
this task can isolate — the control can't fire, hence WALL, not GREEN.

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)

- **DIRECTIONAL numpy mirror only** — live CORE/*.hexa UNTOUCHED; engine-transfer UNVERIFIED.
- TOY 1-D fit, 3 seeds, ONE target family; scale + real-corpus byte-LM trunk UNVERIFIED
  (a separate cost-gated GPU fire, NOT run here).
- Terminal tier = 🧱 **WALL** (a control misbehaves both rounds, so the probe cannot
  cleanly attribute the lift to error-TARGETED growth). The valid, frozen-verbatim
  FINDING inside the wall: **gradient-free mitosis cell-split CAN converge as well as
  gradient descent at this toy scale, at lower footprint (R2 c1 PASS)** — a real p8-literal
  TOEHOLD, but not a clean GREEN because the targeting-discriminator could not be isolated.
- No tune-to-green: R1 and R2 bars are identical numbers, frozen before each run.

## p8-literal verdict (the question asked)

At toy scale, a gradient-FREE mitosis-grow trainer (hard-partition R2) **converges as
well as gradient descent** (R2 c1 PASS) — so p8-literal trunk training is **not refuted**
and shows a directional toehold. It is **NOT a clean GREEN**: the frozen targeting-control
(c2) could not be isolated on this smooth task, so the lift cannot be cleanly attributed
to error-targeted growth vs generic cell-tiling. **Conclusion:** gradient remains the
incumbent trunk trainer pending an engine-native + harder-target re-test; mitosis-grow
is a credible co-trainer candidate, not yet a verified replacement.

## Follow-on (a_break_the_wall continuation — NOT claimed here)

1. **Engine-native** (a_engine_native_learning + a_verified_must_wire): realize R2
   hard-partition mitosis-grow training on live CORE/engine_cli.hexa VAdaptField, re-score
   the frozen bars engine-native — the mirror is DIRECTIONAL, binding verdict needs the engine.
2. **Harder target to fire c2**: a target with SHARP, LOCALIZED error concentration (so
   error-targeted split must beat random) — pre-register a new c2 to test whether targeting
   is the lever once the partition mechanism is sound.

xref: p8 · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning ·
a_verified_must_wire · a_toy_scale_recheck · a_scale_honest_scope · H_1199 (VAdaptField
split) · H_1288 (grow-under-pressure) · H_1159 (inference-time mitosis = learning) · p7 · c9 · c16.
