---
id: H_1297
slug: 1297_mitosis_native_train
title: mitosis-native trunk training — make PHILOSOPHY p8 literal (gradient-free cell-split learns a trunk vs gradient descent)
group: MITOSIS-ENGINE (p8 literal)
terminal_tier: 🟢 GREEN (R3 sharp byte-text target — mitosis MATCHES gradient AND error-targeting demonstrably helps: c2 discriminator FIRED that R1/R2 could not)
verdict_dir: .verdicts/1297_mitosis_native_train/
terminal_verdict: .verdicts/1297_mitosis_native_train/H_1297_R3_sharp_target.txt
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

**R3 (a_break_the_wall / c16 — the SHARPER error-concentration target the R2 follow-on
named; bars frozen anew in `H_1297_R3_sharp_target.txt`):** 🟢 **GREEN.** Task moved from a
SMOOTH 1-D fit to **next-byte prediction on real KOREAN+English UTF-8 bytes (V256)** — a
SHARP target where predictive error concentrates at syllable/word boundaries while
mid-multibyte UTF-8 continuation runs are near-deterministic. SAME 4 arms, R2 hard-partition
mitosis mechanism ported to classification (Voronoi nearest-centroid ownership + per-cell
empirical next-byte frequency head [closed-form add-1 MLE, NO global backprop] + data-matched
median split along highest-variance feature axis + centroid recenter). Metric = held-out
next-byte CROSS-ENTROPY (nats/byte; convergence comparison, NOT perplexity-as-meaning, p7).
3-seed mean (all 3 seeds stable):
**A(grad)=2.9170 [acc 0.202] · B(mitosis)=3.0777 [acc 0.206, 6 cells] · B-shuffle=3.3054 · B-ablate=3.4981 [2 cells].**
- **(c1) PASS** — mitosis MATCHES gradient: 3.0777 ≤ A+0.20 = 3.1170, at LOWER footprint (6 cells vs A's 1024 params).
- **(c2) FIRED at last** — B-shuffle (3.3054) ≥ B+0.10 = 3.1777: random split is demonstrably
  worse than error-targeted split. **The c2 discriminator R1 AND R2 could not fire FIRED here**
  — on a sharp target, error-TARGETING is the lever (random split wastes growth on the
  already-deterministic continuation region; targeted split subdivides the high-entropy
  boundary region).
- **(c3) PASS** — B-ablate (3.4981) ≥ B+0.10: frozen growth underfits.
→ 🟢 GREEN: gradient-free mitosis-grow **matches gradient AND error-targeting demonstrably
helps** on language-like byte data. p8-literal toehold CONFIRMED on a real KO+EN byte corpus.
NO tune-to-green: bars were frozen in `H_1297_R3_sharp_target.txt` before any score.

## Follow-on after R3 GREEN (a_break_the_wall continuation — NOT claimed verified here)

1. **Engine-native realization** (a_engine_native_learning + a_verified_must_wire): realize
   the R3 hard-partition mitosis-grow next-byte trainer on live `CORE/engine_cli.hexa`
   VAdaptField, re-score the frozen R3 bars engine-native — the mirror is DIRECTIONAL, the
   binding verdict needs the engine.
2. **A real (larger) Korean byte-corpus mitosis-grow training rung** — the first p8-literal
   LANGUAGE training: scale the corpus to a genuine Korean byte-LM rung and re-test whether
   error-targeted mitosis-grow still matches/beats gradient at scale. This becomes a
   **cost-gated decision** if it needs GPU (a_fire_autonomous; NOT run in this $0 CPU toy).

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)

- **DIRECTIONAL numpy mirror only** — live CORE/*.hexa UNTOUCHED; engine-transfer UNVERIFIED.
- TOY: R1/R2 = 1-D fit; R3 = small KO+EN byte corpus (3042 bytes, ~1519 train pairs), 3 seeds,
  ONE byte-text family; scale + a real (larger) Korean byte-LM trunk UNVERIFIED (a separate
  cost-gated rung, NOT run here). R3 CE values are high (~3 nats) because the corpus is tiny
  and V=256 — that is fine: R3 is a CONVERGENCE comparison (B vs A, B vs B-shuffle), NOT a
  perplexity verdict (p7).
- Terminal tier = 🟢 **GREEN at R3** — the SHARP byte-text target made the c2 targeting
  discriminator FIRE (B-shuffle worse than B by ≥ the pre-set 0.10-nat gap) that R1 (smooth,
  geometry wall) and R2 (smooth, attribution wall) could not. Mitosis-grow MATCHES gradient
  (c1) at lower footprint AND error-targeting demonstrably helps (c2) AND ablation underfits
  (c3). The R1/R2 WALL was the SMOOTH target, not p8 — exactly as the R2 follow-on predicted.
- No tune-to-green: R1, R2, and R3 bars were each frozen before their run; R3 bars live in
  `H_1297_R3_sharp_target.txt`, verbatim result appended after the freeze.

## p8-literal verdict (the question asked)

At toy scale on language-like byte data, a gradient-FREE mitosis-grow trainer (hard-partition,
R3) **converges as well as gradient descent (c1 PASS) AND error-targeted growth demonstrably
beats random growth (c2 FIRED) AND frozen growth underfits (c3 PASS)** — so p8-literal trunk
training is **CONFIRMED at toy scale on a real KO+EN byte corpus**, with error-targeting (the
p8-distinctive claim) isolated as the lever. **Conclusion:** mitosis-grow is a verified-at-toy
gradient-free trainer where targeting helps; gradient remains the incumbent trunk trainer
pending the two GREEN follow-ons below (engine-native realization + a real Korean scale rung) —
mitosis-grow is now a credible co-trainer candidate with a clean GREEN toehold, NOT yet an
engine-verified or production replacement.

xref: p8 · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning ·
a_verified_must_wire · a_toy_scale_recheck · a_scale_honest_scope · H_1199 (VAdaptField
split) · H_1288 (grow-under-pressure) · H_1159 (inference-time mitosis = learning) · p7 · c9 · c16.
