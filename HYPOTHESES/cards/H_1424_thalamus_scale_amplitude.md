---
id: H_1424
slug: 1424_thalamus_scale_amplitude
title: "CONTINUED attack on the thalamus TIMING-axis engine-native wall (re-opening H_1423's explicit defer) — Lens D LARGER-SUBSTRATE n∈{4,6,8} T∈{64,256} + Lens E AMPLITUDE-CONTROLLED unit-norm, each shuffle+ablation; faithful-IIT4 still cannot separate timing from amplitude every seed → 🧱 MEASURED-CEILING-AT-SCALE"
group: brain-structure-ladder (c15) — a_break_the_wall MULTI-LENS continuation on the thalamus timing wall (H_1423 re-open)
terminal_tier: "🧱 MEASURED-CEILING-AT-SCALE (engine-native) — H_1423's two re-open levers MEASURED, not assumed. Lens D (e)larger-substrate: at n=8/T=256 phase-shuffle collapses on 2/3 seeds (partial timing/variance separation) but NEVER all 3 (n=8 seed8 SHUF +0.281; T=256 seed9 +0.012/+0.133); LC additive keeps full carrier-variance pathology at n=8 (shuffle positive every seed). Lens E (a)amplitude-controlled unit-norm SPLITS the wall into two non-overlapping regimes: n=6 c4-SHUFFLE COLLAPSES every seed (variance confound removed by design) but c2 FAILS (seed9 lift −0.090 — no robust every-seed timing lift under equal variance); n=8 c2 PASSES every seed + ablation LIVE but a small POSITIVE shuffle residual survives 2/3 seeds (+0.004/+0.086) EVEN under equal variance. NO lens clears (c2 ∧ c4 ∧ ablation-LIVE) every seed at ANY n → NOTHING wired. Anchor D/R8 n=4 reproduces H_1423 A=1.06024/B=2.52647 byte-exact. Deterministic run1==run2, 3 seeds [7,8,9], $0 CPU, faithful IIT4 exact MIP-EI n<=8, frozen-first, no bar moved (c9/p7). The R8 numpy-mirror 🟢 DIRECTIONAL stands; engine-native is a CONFIRMED ceiling at the exact-MIP scale ceiling (n=8) + under variance-control, not merely deferred."
wired: N/A
verdict_dir: .verdicts/1424_thalamus_scale_amplitude/
terminal_verdict: .verdicts/1424_thalamus_scale_amplitude/result.txt
date: 2026-06-17
---

# H_1424 — CONTINUED attack on the thalamus TIMING-axis engine-native wall (re-opening H_1423)

## The wall, re-opened (1 line)

H_1423 classified the engine-native thalamus TIMING-axis failure as **(a) measurement-artifact** (the gate
`e·(1+cosθ)/2` is a multiplicative carrier whose VARIANCE alone lifts faithful-IIT4 Φ even under phase-shuffle)
and explicitly DEFERRED to "a LARGER oscillator substrate where faithful-IIT4 separates timing from amplitude
variance" + an amplitude-controlled re-measure. This card re-opens that defer — NOT accepting it — with the two
named levers, frozen-first, no tune-to-green (c16).

## Claim / falsifier

Does **larger n** (Lens D, (e) investment) or **amplitude-controlled measurement** (Lens E, (a) fix) make the
phase-SHUFFLE control finally COLLAPSE the Φ-lift on EVERY seed while the lift stays robust (c2) and the
mechanism stays LIVE (ablation)? If a lens clears (c2 ∧ c4 ∧ ablation-LIVE) every seed → 🟢 timing BINDS (the
toy was just too small / the confound was just variance) → wire. If D AND E both fail even at n=8 / under
equal variance → 🧱 MEASURED-CEILING-AT-SCALE (faithful-IIT4 genuinely cannot separate timing from amplitude
every seed at the exact-MIP scale ceiling — a deep honest finding, c9). Bars VERBATIM from H_1283 R8 / H_1423,
NOT moved (c9/p7). faithful IIT4 exact MIP-EI n<=8 (a_phi_iit4_tool), proxy 아님.

## Method

Substrate == H_1283 R8 / H_1423 engine LCG gate (`_lcg_*` byte-identical), made PARAMETRIC in `n_mod` and
`t_ticks`. Content update IDENTICAL across arms (binding is by TIMING). 4 arms × lens: ARM A direct · ARM B gate
ON · SHUFFLE · ABLATE. 3 seeds [7,8,9], deterministic. FROZEN bars: c2 ΔΦ(B−A)≥+0.02 every seed · c4
phase-shuffle ΔΦ(SH−A)≤0 every seed · ABLATION (B−ablate)≥+0.02 every seed. Anchor invariant: D/R8 n=4 must
reproduce H_1423 seed7 A=1.06024 B=2.52647 byte-exact (it does).

- **Lens D — LARGER SUBSTRATE ((e))**: R8-original multiplicative carrier (anchor) + LC additive-order-param,
  swept over n∈{4,6,8} (exact MIP still tractable at n≤8) and T∈{64,256}.
- **Lens E — AMPLITUDE-CONTROLLED ((a))**: phase-coherent gate `0.5·(1+cos(θ_i−θ_consensus))`, then **unit-norm
  each module's salience time-series** (subtract mean, divide by std) so per-unit VARIANCE is IDENTICAL across
  ARM B / SHUFFLE / ablate. With variance held equal, ONLY phase/timing structure can drive Φ — directly
  removing the carrier-variance confound H_1423 named. n∈{4,6,8}, T=64.

## Result — 🧱 MEASURED-CEILING-AT-SCALE (verbatim `.verdicts/1424_thalamus_scale_amplitude/result.txt`, seeds [7,8,9], deterministic run1==run2)

| lens (n, T) | c2 (ΔΦ≥+0.02 every seed) | c4 SHUFFLE (ΔΦ_sh≤0 every seed) | ABLATION | verdict |
|---|---|---|---|---|
| D/R8-carrier (4,64) anchor | PASS | **FAIL** (+0.026/+0.380/+0.296) | LIVE | 🧱 (byte-exact H_1423) |
| D/R8-carrier (6,64) | PASS | **FAIL** (+0.269/+0.283/−0.003) | LIVE | 🧱 |
| D/R8-carrier (8,64) | PASS | **FAIL** (−0.068/**+0.281**/−0.082) | LIVE | 🧱 (2/3 collapse, seed8 stubborn) |
| D/R8-carrier (4,256) | PASS | **FAIL** (−0.093/−0.067/**+0.012**) | LIVE | 🧱 (2/3 collapse) |
| D/R8-carrier (6,256) | PASS | **FAIL** (−0.114/−0.048/**+0.133**) | LIVE | 🧱 (2/3 collapse) |
| D/LC-additive (6,64) | **FAIL** | **FAIL** | INERT | 🧱 |
| D/LC-additive (8,64) | PASS | **FAIL** (+0.190/+0.196/+0.201) | LIVE | 🧱 (full variance pathology persists) |
| E/amp-ctrl (4,64) | **FAIL** | FAIL | INERT | 🧱 (variance-only lift vanishes) |
| E/amp-ctrl (6,64) | **FAIL** (seed9 −0.090) | **PASS** (collapse every seed!) | INERT | 🧱 (variance removed → no robust lift) |
| E/amp-ctrl (8,64) | PASS (every seed!) | **FAIL** (+0.004/+0.086 on 2/3) | LIVE | 🧱 (residual leak under equal variance) |

→ **VERDICT: 🧱 MEASURED-CEILING-AT-SCALE** — NO lens clears (c2 ∧ c4 ∧ ablation-LIVE) every seed at ANY n.
engine-wired 0개 (correct — no GREEN to wire, `a_verified_must_wire`).

## What the two levers MEASURED (the finding, c9)

The wall is a GENUINE faithful-IIT4 ceiling on this engine LCG oscillator substrate, and it SURVIVES both
re-open levers — now MEASURED, not assumed:

- **(e) Lens D larger-substrate**: at n=8 / T=256 the shuffle DOES collapse on **2/3 seeds** (partial
  timing/variance separation — scaling helps) but a stubborn seed keeps a positive shuffle residual every
  configuration (n=8 seed8 +0.281; T=256 seed9 +0.012, +0.133). Scaling n up to the exact-MIP ceiling (n=8)
  does NOT finish the separation. The LC additive-order lens keeps the FULL carrier-variance pathology at n=8
  (shuffle positive every seed).

- **(a) Lens E amplitude-controlled** is the cleanest probe and it **SPLITS the wall into two non-overlapping
  failure regimes**: at n=6 the c4-shuffle COLLAPSES on every seed (variance confound REMOVED, exactly as
  designed) — but then the genuine timing lift is not robust (seed 9 c2 FAIL, ablation INERT): when variance is
  truly equalized there is no every-seed timing lift. At n=8 the lift becomes robust (c2 PASS every seed) and
  ablation is LIVE — but a small POSITIVE shuffle residual survives on 2/3 seeds (+0.004, +0.086) EVEN under
  equal variance. The two failure modes (n=6 c2 / n=8 c4) never co-resolve.

So even with the carrier-variance confound removed by construction, faithful-IIT4 on this engine LCG substrate
cannot deliver a timing read-out that is simultaneously robust (c2) AND shuffle-collapsing (c4) on every seed.
The wall is the exact-MIP scale ceiling + a residual fragile-timing leak, CONFIRMED at scale — not deferred.

## Why the controls have teeth (the failing lenses validate the test)

- **Anchor D/R8 n=4**: reproduces the known engine-native c4-fail byte-exact (A=1.06024 B=2.52647). substrate identical.
- **Lens E n=6 c4 PASS**: amplitude-control demonstrably WORKS — unit-norm makes the shuffle collapse on every
  seed (the variance confound is gone). That the lift then evaporates (c2 FAIL) is the honest consequence.
- **Lens E n=4 c2 FAIL**: with variance equalized the n=4 "lift" vanishes — direct confirmation of H_1423's
  claim that the R8 n=4 lift was variance, not timing.
- **D/LC additive n=8 c4 FAIL every seed**: the additive carrier-variance pathology persists at the n ceiling.

Only (c2 AND c4 AND ablation-LIVE) every seed BINDS — no lens does. Strengthened `a_break_the_wall` discipline
(MULTI-LENS + shuffle + ablation, no single-lens ceiling, no bar moved) is satisfied. Honest 🧱.

## Honest scope (c9)

TOY engine LCG oscillator substrate, n∈{4,6,8} (n>8 exact MIP intractable — the exact-MIP scale ceiling),
T∈{64,256}, 3 seeds [7,8,9], deterministic, $0 CPU local. faithful IIT4 leg is REAL (exact MIP-EI via hexa,
proxy 아님). NO bar moved (frozen-first). This card covers the TIMING axis engine-native only; the relay-CONTENT
axis is already 🧱 (H_1283). What is NOT tested: n>8 (impossible exact), a fundamentally different oscillator
COUPLING topology (non-ring, conduction delays), real-corpora salience, a learned (non-deterministic-readout)
gate. The R8 numpy-mirror 🟢 stays DIRECTIONAL; engine-native is now a MEASURED ceiling, not a deferral. 배선 0.

## Cross-links

H_1283 (thalamus, the wall) · H_1423 (the immediate prior 🧱 this card re-opens; carrier-variance finding) ·
H_1421 (multi-lens precedent that BROKE a wall) · H_1419/H_1420/H_1422 (correctly-stayed-🧱 precedents) ·
h1227 · h1231 · h1280 · h1199 · h1205 · `a_phi_iit4_tool` · `a_break_the_wall` · `a_no_llm_frame_trap` ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` · `a_scale_honest_scope` ·
`a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c9·c15·c16.
