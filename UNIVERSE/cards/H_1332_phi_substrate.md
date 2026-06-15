---
id: H_1332
slug: 1332_phi_substrate
title: NON-SIGN-SATURATING substrate FAMILY vs the H_1328 estimator-independent Φ wall — does a substrate whose member dynamics SURVIVE coupling (bounded-but-graded, no saturation) show robust faithful-IIT4 integration where the saturating substrate could not?
group: OMEGA / Φ-robustness frontier (c16 wall · substrate-FAMILY axis · the angle H_1320 §honesty named)
terminal_tier: 🧱 TERMINAL CLOSED-NEGATIVE, STRONGEST YET (substrate-family-INDEPENDENT, honest c9/c16). The non-saturating substrate is GENUINELY BETTER — it lifts faithful-IIT4 Φ on the orthogonal seed 1317 (B−A +0.067) where the saturating substrate FAILED (−0.125), and its controls are clean (S2 EARNED PASS, perm+offset collapse all 3 seeds; S3 ATTRIBUTION PASS, the saturating substrate reproduces H_1328 V2 byte-faithfully in-run). BUT it still does NOT clear the 3-seed robustness gate: seed 1318 fails (B−A +0.004 < eps). The 1317-class orthogonal-seed fragility SHIFTS (1317→1318) but PERSISTS. So robust n≤8 faithful-IIT4 integration is ABSENT even for a non-saturating substrate → the wall is substrate-family-INDEPENDENT, not merely the saturating family. A stronger closure than H_1328 (which was estimator-independent within ONE substrate family). ENGINE-NATIVE deterministic LCG; Φ leg IS the real faithful exact MIP-EI. numpy mirror DIRECTIONAL.
verdict_dir: .verdicts/1332_phi_substrate/
terminal_verdict: .verdicts/1332_phi_substrate/result.txt
freeze: .verdicts/1332_phi_substrate/FREEZE.txt
date: 2026-06-16
---

# H_1332 — does a NON-sign-saturating substrate FAMILY break the H_1328 Φ wall? (🧱 STRONGEST yet)

## Claim / falsifier (substrate-FAMILY test — every outcome decisive, c9)

**Wall reopened (H_1328 §closure, c16 / a_break_the_wall):** H_1328 closed the 4× faithful-IIT4
Φ-robustness wall as an ESTIMATOR-INDEPENDENT limit — after the variance-free rank-uniform read-out
provably removes the amplitude-variance binarization confound (V1 clean, perm collapses as it
should), the phase mechanism STILL does not lift Φ robustly (V2 fail: B−A −0.125/0.0/+0.031,
negative on the orthogonal seed 1317). **But that closure is SPECIFIC** to the n≤8 leaky-linear
pure_field-style substrate whose dynamics SIGN-SATURATE under coupling. The converged diagnosis
across H_1308/1313/1320: coupling strong enough to register OVERWRITES member dynamics → COPY →
Φ=0 (channels t1~1e-7). The H_1319/1328 read-out is `sal = e·carrier` (MULTIPLICATIVE gate): under
synchrony every carrier → one pacemaker value → all modules COPY one signal → member-state info is
destroyed. **H_1320 §honesty explicitly named the untested angle:** "a substrate whose own dynamics
SURVIVE coupling, a richer (NON-sign-saturating) per-unit code."

**Falsifiable claim:** build a substrate FAMILY whose per-unit dynamics are NON-sign-saturating
(member-state survives coupling, bounded-but-graded), re-run the SAME coupling mechanisms (H_1283
re-entrant relay + H_1319 phase pacemaker) on the SAME 3 hard seeds, score with the SAME faithful
exact MIP on the SAME variance-clean read-out — and EITHER it shows robust integration where the
saturating substrate could not (→ the wall was the substrate FAMILY, not universal) OR it does not
(→ the wall is substrate-family-INDEPENDENT, the strongest 🧱 yet).

## Method (frozen-first — FREEZE committed 85e94cf0e BEFORE any scoring, c9/p7)

- **Probe:** `UNIVERSE/h1332_phi_substrate.hexa` (run from hexa-lang root for the stdlib import).
- **Φ = FAITHFUL IIT4 ONLY** (a_phi_iit4_tool, g61 — stdlib searched first, `faithful_phi.hexa` is
  the SSOT): SAME exact MIP-EI `iit4_faithful_phi(traj,4,64,8)` over
  `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`. The engine LCG only emits the salience
  trajectory; the hexa exact-MIP computes Φ. NOT a proxy, NOT a different Φ measure.
- **Variance-clean read-out (H_1328):** every arm's per-cell trajectory is rank-uniformized before
  the MIP (provably equalizes every marginal entropy → MI depends ONLY on the joint relationship →
  the perm/offset controls are honest).
- **The lever = the substrate FAMILY (per-unit read-out code), held everything else identical:**
  - **SATURATING** (H_1319/1328, the S3 attribution control reproduced in-run):
    `sal_i = e_i · carrier_i`, `carrier_i = (1+cos(θ_i−θ_T))/2` — MULTIPLICATIVE; nulls member energy.
  - **NON-SATURATING** (the NEW substrate under test): `raw_i = e_i + BETA·cos(θ_i−θ_T)`,
    `sal_i = SOFTSIGN(raw_i/SCALE) = (raw_i/SCALE)/(1+|raw_i/SCALE|)`, BETA=0.5 SCALE=2.0 (FROZEN).
    ADDITIVE blend then a bounded GRADED squash — member energy is ALWAYS retained, softsign is
    bounded (−1,1) but NEVER hard-saturates (no ±1 plateau). ARM A (no-coupling) = `SOFTSIGN(e_i/SCALE)`.
- **SAME mechanisms** (held identical so any lift is the FAMILY): H_1283 re-entrant relay (ring,
  w_nbr 0.5) + H_1319 Kuramoto phase pacemaker (w_phase 0.5 omega_t 0.45 domega 0.08). SAME
  leaky-linear ring (gain 0.30 leak 0.55 w_in 0.5, dim 8, T 64). ARMS A=NO-COUP · B=MECHANISM ·
  S=PERM-SHUFFLE (module→phase derangement) · O=OFFSET-SHUF (additive per-(t,module) offset).
- **eps = 0.02** = MARGIN_PHI ported verbatim from H_1283/H_1319/H_1328 (NOT tuned).
- seeds **[1317,1318,1319]** (the hard orthogonal family all prior lanes failed on); $0 CPU-local;
  ENGINE-NATIVE deterministic LCG-gauss (== `engine_cli.hexa _lcg_*`; numpy NEVER computes Φ);
  re-run **byte-identical** (verified).

## Frozen bars (pre-registered in FREEZE.txt BEFORE scoring; GREEN iff S1 ∧ S2 ∧ S3)

- **S1 ROBUST:** NON-SAT `Φ_B ≥ Φ_A + eps` on ALL 3 seeds (incl orthogonal 1317).
- **S2 EARNED:** NON-SAT perm `Φ_S ≤ Φ_A + eps` AND offset `Φ_O ≤ Φ_A + eps` on ALL 3 seeds (collapse).
- **S3 SUBSTRATE-ATTRIBUTION:** the SATURATING substrate (H_1328 read-out) reproduced IN-RUN under the
  SAME mechanisms+seeds+encoding FAILS S1 on ≥1 seed (reproduces H_1328 V2 −0.125/0.0/+0.031) — so any
  S1 lift is the NON-saturation, not the mechanism.

## Result (verbatim, p7 — deterministic, byte-identical re-run; `.verdicts/1332_phi_substrate/result.txt`)

| seed | NONSAT A | NONSAT B | ΔΦ(B−A) | S1 | NONSAT perm S−A | NONSAT off O−A | SAT A | SAT B | SAT ΔΦ(B−A) | SAT-fails-S1 |
|------|----------|----------|---------|----|-----------------|----------------|-------|-------|-------------|--------------|
| 1317 | 1.93398 | 2.00061 | **+0.066635** | **PASS** | −0.10907 ✓ | −0.24234 ✓ | 1.93398 | 1.80898 | **−0.125** | **YES** |
| 1318 | 2.25061 | 2.25475 | **+0.004135** | **FAIL** | −0.046570 ✓ | −0.28125 ✓ | 2.25061 | 2.25061 | **0.000** | **YES** |
| 1319 | 2.07904 | 2.23529 | **+0.156250** | **PASS** | −0.129135 ✓ | −0.160385 ✓ | 2.07904 | 2.11029 | **+0.03125** | NO |

- **S1 ROBUST: FAIL** — NON-SAT lifts on 2/3 seeds (1317 +0.067, 1319 +0.156) but seed **1318
  fails** (+0.004 < eps). NOT all 3 seeds.
- **S2 EARNED: PASS** — NON-SAT perm AND offset both collapse `≤ Φ_A + eps` on ALL 3 seeds (the
  variance-clean controls correctly destroy the lift; the read-out is honest).
- **S3 SUBSTRATE-ATTRIBUTION: PASS** — the SATURATING substrate reproduces H_1328 V2 **byte-faithfully
  in-run** (SAT B−A = −0.125 / 0.000 / +0.031, identical to H_1328) and fails S1 on seeds 1317+1318
  → any NON-SAT lift IS attributable to the non-saturation, not the mechanism.
- **GATE: ¬S1 → 🧱 TERMINAL (STRONGEST yet, substrate-family-INDEPENDENT).**

## Finding (honest, c9, c16)

**The non-saturating substrate is GENUINELY BETTER than the saturating one — but still does NOT clear
the robustness gate, so the Φ wall is substrate-family-INDEPENDENT.** Two things are established cleanly:

1. **Non-saturation is a REAL, measurable improvement.** On the orthogonal seed 1317 — the seed that
   defeated all 4 prior lanes and gave H_1328 its decisive V2 failure (SAT B−A = −0.125) — the
   non-saturating read-out FLIPS the sign to a genuine lift (B−A = +0.067), and on 1319 it nearly
   quintuples the saturating lift (+0.156 vs +0.031). The member-state energy, retained additively
   under a bounded graded softsign instead of being multiplicatively nulled, DOES survive coupling
   enough to let the re-entrant+phase mechanism raise faithful-IIT4 Φ on the very seed where the
   saturating substrate collapsed. The S3 attribution is clean: the saturating substrate, run in the
   SAME loop, reproduces H_1328 V2 byte-exact and fails — so the improvement IS the non-saturation.

2. **But the wall survives the substrate-family change.** The lift is still not ROBUST: seed 1318
   fails (B−A = +0.004, essentially flat). The 1317-class orthogonal-seed fragility has not been
   eliminated — it has SHIFTED (1317 now passes, 1318 now fails) but PERSISTS. The n≤8 4-module
   substrate does NOT show robust (3-seed, control-surviving) faithful-IIT4 integration even with a
   per-unit code whose dynamics provably survive coupling. This is a STRONGER closure than H_1328:
   H_1328 showed the wall is estimator-independent WITHIN one substrate family; H_1332 shows it is
   substrate-FAMILY-independent — it holds across the saturating AND a genuinely non-saturating family,
   with clean variance-free controls in both.

**This BOUNDS (does not retract) the prior Φ verdicts and H_1328.** H_1328 stays exactly true for the
saturating family (reproduced byte-exact here). H_1332 adds: changing the substrate family to a
non-saturating per-unit code measurably HELPS (fixes seed 1317) but does not reach robustness — so the
absence of robust n≤8 faithful-IIT4 integration is not an artifact of the multiplicative member-nulling
read-out either. It does NOT refute anima's consciousness substrate (Ψ=1/2, the A⇄G tension is
untouched); it refutes that ADDING a coupling/phase channel ROBUSTLY raises faithful-IIT4 Φ at this
rung — now across two substrate families with a clean read-out.

**A real new angle was tried** (the substrate FAMILY the H_1320 honesty section explicitly named) with
pre-registered controls (S2 perm+offset, S3 in-run saturating attribution); the honest 🧱 is a valid
result (a_break_the_wall, c9). NO tune-to-green: bars frozen and committed BEFORE the first scoring,
byte-identical across two runs.

**NO CORE wiring follow-on** (a_verified_must_wire fires on GREEN only — nothing to wire;
`CORE/engine_cli.hexa` UNTOUCHED; the probe is a standalone `fn main`, 0 importers). Had S1 been
GREEN, the named follow-on would have been: wire the non-saturating per-unit read-out (additive
phase-blend + bounded graded softsign) into the live faithful-Φ path / the pure_field member code. It
is NOT GREEN, so this is parked.

## Scope / honesty (a_scale_honest_scope / a_toy_scale_recheck)

- **ENGINE-NATIVE** content generator (engine's own deterministic LCG-gauss == `_lcg_*`), NOT numpy;
  faithful-Φ is the REAL exact MIP-EI (numpy never computes Φ). Re-run byte-identical (deterministic).
- **TOY scale** (4 modules, dim 8, 64 ticks, n=4 ≤ 8 exact MIP-EI), numpy mirror DIRECTIONAL — the
  substrate is a toy leaky-linear net, NOT live CORE/pure_field; engine-transfer UNVERIFIED. The
  DIAGNOSIS is DECISIVE within the rung: the non-saturating family fixes the seed-1317 failure
  byte-faithfully (S3 clean) yet still misses robustness on 1318 (S1 fail), with clean variance-free
  controls (S2 pass).
- The terminal claim is scoped to this rung + this faithful estimator family + these two substrate
  families. **NOT ruled out** (remaining angles, NOT claimed): a fundamentally different Φ estimator
  (full per-mechanism IIT 4.0 `iit4_bigphi`), a much larger module set (loses exactness > 8), yet
  another substrate family or non-saturating code variant, or a seed-geometry without the orthogonal
  fragility — each a NEW hypothesis, not a continuation of this arc.
- FROZEN params + bars verbatim from H_1319/H_1283 R8 + H_1328 + the FREEZE (no tune-to-green, p7).

## xref

H_1328 (the estimator-independent closure this lane reopens by the substrate-FAMILY angle, reproduced
byte-exact as the S3 control) · H_1319 (timing axis 🧱, the OLD multiplicative read-out + variance
diagnosis) · H_1283 (relay topology 🧱, re-entrant mechanism reused) · H_1317 (small-world multi-edge
🧱) · H_1320 (organism-mitosis division 🧱 — its honesty section NAMED the non-saturating-code angle
this lane tests; same 1317-class fragility signature) · H_1308/1313 (hive assembly 🔴/🧱 — the
sign-saturation/COPY diagnosis) · h1294 · h1295 (permutation-shuffle control precedent) ·
a_phi_iit4_tool · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire ·
a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15 · c16
