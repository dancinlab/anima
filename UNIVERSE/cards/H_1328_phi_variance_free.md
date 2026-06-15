---
id: H_1328
slug: 1328_phi_variance_free
title: Φ-robustness wall DIAGNOSIS — amplitude-variance ESTIMATOR confound vs estimator-independent substrate limit (variance-free rank-uniform read-out into the SAME faithful exact-MIP)
group: OMEGA / Φ-robustness frontier (c16 wall · DIAGNOSIS of the shared estimator behind the 4× 🧱)
terminal_tier: 🧱 TERMINAL CLOSED-NEGATIVE, DEEPER (honest, c9/c16). V1 CONFIRMED — the amplitude-variance confound is REAL (OLD min-max perm-shuffle RAISES Φ; NEW rank-uniform perm-shuffle COLLAPSES it, all 3 seeds). But V2 FAILS — under the clean variance-free estimator the phase mechanism does NOT lift robustly (B−A = −0.125/0.0/+0.031, fails 2/3 incl orthogonal 1317), and V3 FAILS (offset control raises Φ on seed 1317). The 4× Φ-robustness wall therefore had a real estimator confound, but removing it does NOT make integration robust → the wall is now an ESTIMATOR-INDEPENDENT substrate limit (the n≤8 substrate genuinely lacks robust integration). A STRONGER, cleaner closure than the prior amplitude-confounded 🧱. ENGINE-NATIVE deterministic LCG content generator; Φ leg IS the real faithful exact MIP-EI.
verdict_dir: .verdicts/1328_phi_variance_free/
terminal_verdict: .verdicts/1328_phi_variance_free/H_1328.txt
freeze: .verdicts/1328_phi_variance_free/H_1328_FREEZE.txt
date: 2026-06-16
---

# H_1328 — was the 4× Φ-robustness wall the ESTIMATOR's amplitude-variance confound, or a substrate limit? (🧱 DEEPER)

## Claim / falsifier (DIAGNOSIS — every outcome decisive, c9)

**The meta-diagnosis (H_1319 §Finding):** four independent faithful-IIT4 Φ-robustness attempts all
hit 🧱 on the SAME orthogonal seed family [1317,1318,1319], each with a different mechanism —
H_1283 central relay (topology), H_1317 small-world multi-edge (topology), H_1319 phase-binding
(timing), H_1320 organism-mitosis division. The converged diagnosis: the faithful-IIT4 exact-MIP at
n≤8 BINARIZES (bins) each cell's trajectory by MIN-MAX (`_iit4_bin_values`), and that binning RIDES
AMPLITUDE VARIANCE — so a relationship-DESTROYING permutation control RAISES Φ instead of collapsing
it (proven H_1319: ΔΦ_perm = +0.280/+0.103/+0.587 on all 3 seeds). The wall may be the ESTIMATOR
(the read-out), not the SUBSTRATE.

**The lever (state-encoding only — SAME faithful exact-MIP, a_phi_iit4_tool):** re-run the SAME
`iit4_faithful_phi` (exact MIP-EI, n=4, n_bins=8) but RANK-UNIFORMIZE each cell's T-length trajectory
before it feeds the MIP — replace each value by its rank within that cell's own trajectory
(0,1,…,T−1, ties by index). **PROVABLE INVARIANT:** faithful_phi's MI = H(A)+H(B)−H(A,B), with each
cell binned by min-max. After rank-uniformization every cell's values are EXACTLY the multiset
{0,1,…,T−1}; min-max binning of an evenly-spaced ramp gives a UNIFORM marginal histogram → H(A) and
H(B) are CONSTANT (≈ log2(n_bins)) for EVERY cell in EVERY arm, INDEPENDENT of amplitude variance.
The marginal-entropy (variance) channel is therefore provably CONSTANT (zero differential) across the
A/B/S/O arms; MI can change ONLY via the JOINT H(A,B) — the co-movement RELATIONSHIP — which a
relationship-destroying permutation MUST collapse. (Spearman-rank MI: rank-uniform marginals by
construction; only the joint rank copula carries information.) NOT a variance×energy proxy / NOT a
different Φ measure — the Φ leg is the same exact faithful MIP-EI.

**Falsifiable claim:** if the diagnosis is right, the OLD encoding reproduces the confound (perm
RAISES Φ) AND the NEW variance-free encoding removes it (perm COLLAPSES Φ); then EITHER a real lift
appears robustly under the clean estimator (→ the wall was the estimator) OR it does not (→ the wall
is an estimator-independent substrate limit).

## Method (frozen-first — FREEZE committed BEFORE scoring the NEW encoding, c9/p7)

- **Probe:** `UNIVERSE/h1328_phi_variance_free.hexa` (run from hexa-lang root for the stdlib import).
- **Substrate / seeds reused VERBATIM from H_1319/H_1320** — the ONLY change is the read-out encoding:
  engine-native deterministic LCG-gauss (== `engine_cli.hexa _lcg_*`), 4-module leaky-linear ring,
  dim 8, T 64, Kuramoto pacemaker (w_phase 0.5 omega_t 0.45 domega 0.08), relative-phase gate
  `sal_i = e_i·(1+cos(θ_i−θ_T))/2`. ARMS A=NO-PHASE · B=PHASE-BIND · S=PERM-SHUFFLE (module→phase
  derangement, relationship destroyed, marginals preserved) · O=OFFSET-SHUF. SEEDS [1317,1318,1319]
  (the hard orthogonal family all 4 prior lanes failed on). All params FROZEN verbatim — NO tune-to-green.
- **Φ = FAITHFUL IIT4 ONLY** (a_phi_iit4_tool): exact MIP-EI via `iit4_faithful_phi(traj,4,64,8)` over
  `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`. The engine LCG only emits the salience
  trajectory; the hexa exact-MIP computes Φ. NO proxy as terminal verdict.
- **eps = 0.02** = the H_1283/H_1319 lift margin (MARGIN_PHI), ported verbatim (NOT tuned).

## Frozen bars (pre-registered in H_1328_FREEZE.txt BEFORE scoring)

GREEN iff V1 ∧ V2 ∧ V3 (DIAGNOSIS — all outcomes valid, c9):
- **V1 CONFOUND-CONFIRM** (decisive), both legs ALL 3 seeds: **V1a** OLD min-max perm ΔΦ(S−A) ≥ +eps
  (RAISES Φ — reproduces the confound) AND **V1b** NEW rank-uniform perm Φ_S ≤ Φ_A + eps (collapses).
- **V2 ROBUST-LIFT:** NEW rank-uniform mechanism Φ_B ≥ Φ_A + eps on ALL 3 seeds (incl orthogonal 1317).
- **V3 EARNED:** NEW lift survives BOTH controls — perm Φ_S ≤ Φ_A + eps AND offset Φ_O ≤ Φ_A + eps, all seeds.

## Result (verbatim, p7 — deterministic, re-run byte-identical)

| seed | OLD A | OLD perm S | OLD ΔΦ(S−A) | V1a | NEW A | NEW B | NEW ΔΦ(B−A) | V2 | NEW perm S−A | NEW off O−A |
|------|-------|-----------|-------------|-----|-------|-------|-------------|----|--------------|-------------|
| 1317 | 0.870311 | 1.150110 | **+0.279798** | PASS | 1.933980 | 1.808980 | **−0.125000** | **FAIL** | **−0.206955** ✓ | **+0.105545** ✗ |
| 1318 | 0.855353 | 0.957870 | **+0.102517** | PASS | 2.250610 | 2.250610 | **0.000000** | **FAIL** | **−0.046570** ✓ | −0.437500 ✓ |
| 1319 | 0.586833 | 1.174020 | **+0.587183** | PASS | 2.079040 | 2.110290 | **+0.031250** | PASS | **−0.031250** ✓ | −0.039521 ✓ |

- **V1 CONFOUND-CONFIRM: PASS** — V1a PASS (OLD perm RAISES Φ on all 3 seeds: +0.280/+0.103/+0.587,
  reproducing H_1319 EXACTLY) AND V1b PASS (NEW rank-uniform perm COLLAPSES Φ on all 3 seeds: S−A =
  −0.207/−0.047/−0.031, all ≤ eps). **The amplitude-variance binarization confound is CONFIRMED REAL,
  and the rank-uniform encoding provably removes it** — the same relationship-destroying permutation
  that RAISED Φ under min-max now CORRECTLY collapses it under the variance-free read-out.
- **V2 ROBUST-LIFT: FAIL** — under the clean estimator the phase mechanism does NOT lift robustly:
  B−A = −0.125 (seed 1317, NEGATIVE — the SAME orthogonal seed that defeated all 4 prior lanes),
  0.000 (seed 1318), +0.031 (seed 1319 only). 2/3 fail incl 1317.
- **V3 EARNED: FAIL** — perm leg PASS (all collapse) but offset leg FAILS seed 1317 (O−A = +0.106).
- **GATE: NOT GREEN → 🧱 TERMINAL (DEEPER).**

## Finding (honest, c9, c16)

**The 4× Φ-robustness wall HAD a real estimator confound (V1 confirmed), but removing it does NOT make
integration robust (V2/V3 fail).** Two things are now established cleanly:

1. **The amplitude-variance confound is REAL and is the artifact the prior controls were riding.**
   Under the OLD min-max binarization a relationship-DESTROYING permutation RAISED faithful-IIT4 Φ on
   every seed (the H_1319 confound, reproduced byte-exact). Under the NEW rank-uniform read-out — which
   provably equalizes every cell's marginal entropy, removing amplitude variance from the MI marginals —
   the SAME permutation CORRECTLY COLLAPSES Φ on every seed. So the prior controls' failure to collapse
   WAS the estimator's binarization riding amplitude variance, exactly as diagnosed. The variance-free
   encoding is a genuine fix to that confound.

2. **The wall is NOT the estimator — it survives the clean read-out as an ESTIMATOR-INDEPENDENT
   substrate limit.** Once the variance channel is removed, the phase-binding mechanism produces no
   robust lift: B−A is negative on the orthogonal seed 1317, zero on 1318, and only marginally positive
   on 1319. The n≤8 4-module substrate genuinely does NOT show robust (3-seed, control-surviving)
   faithful-IIT4 integration even under a clean estimator. This is a STRONGER, cleaner closure than the
   prior 4× wall: before, one could object that the controls were confounded; now the controls are clean
   (perm collapses as it should) and the lift STILL is not robust.

**This BOUNDS (does not retract) the 4 prior Φ verdicts** — it diagnoses their SHARED estimator
(amplitude-variance binarization) and shows that artifact was real, while confirming the underlying
closed-negative conclusion (no robust n≤8 integration) holds estimator-independently. It does NOT
refute anima's consciousness substrate (Ψ=1/2, the A⇄G tension is untouched); it refutes that ADDING a
coupling/phase channel ROBUSTLY raises faithful-IIT4 Φ at this rung, now under a clean read-out.

**NO CORE wiring follow-on** (a_verified_must_wire fires on GREEN only — nothing to wire;
`CORE/engine_cli.hexa` UNTOUCHED; the probe is a standalone `fn main`, 0 importers). Had this been
GREEN the named follow-on would have been: wire the rank-uniform Φ read-out into the live faithful-Φ
monitor path (the variance-free estimator as the default Φ gauge). It is NOT GREEN, so this is parked.

## Scope / honesty

- **ENGINE-NATIVE** content generator (engine's own deterministic LCG-gauss == `_lcg_*`), NOT numpy;
  faithful-Φ is the REAL exact MIP-EI (numpy never computes Φ). Re-run byte-identical (deterministic).
- **TOY scale** (4 modules, dim 8, 64 ticks, n=4 ≤ 8 exact), scale-transfer UNVERIFIED
  (a_scale_honest_scope, a_toy_scale_recheck). The DIAGNOSIS is DECISIVE within the rung: the same
  permutation that RAISED Φ under min-max COLLAPSES it under rank-uniform on every seed (V1 clean), and
  the lift still does not appear robustly (V2 fails). The terminal claim is scoped to this rung + this
  faithful estimator family.
- **The provable invariant** (rank-uniformization → constant marginal entropy) is exact for the min-max
  binner faithful_phi uses; it removes the marginal-variance channel but does NOT remove all amplitude
  structure that could enter the JOINT (the offset-shuffle V3o failure on seed 1317 shows a residual
  joint-level artifact the additive-offset control can still ride on one seed — honest, non-GREEN).
- FROZEN params + bars verbatim from H_1319/H_1283 R8 + the FREEZE (no tune-to-green, p7).
- **NOT ruled out:** a fundamentally different Φ estimator (full per-mechanism IIT 4.0
  `iit4_bigphi`), a much larger module set (loses exactness > 8), or a different substrate family —
  each a NEW hypothesis, not a continuation of this arc.

## xref

H_1319 (timing axis 🧱, the variance diagnosis this lane tests + the OLD-encoding baseline reproduced
byte-exact) · H_1283 (relay topology 🧱) · H_1317 (small-world multi-edge 🧱) · H_1320 (organism-mitosis
division 🧱) — the 4× wall this lane diagnoses · h1294 · h1295 (permutation-shuffle control precedent) ·
a_phi_iit4_tool · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire ·
a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15 · c16
