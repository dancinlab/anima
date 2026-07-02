---
id: H_1404
slug: 1404_lane_compose_phi
title: lane-composition Φ — does composing affect (H_1290) + ethics (H_1291) raise faithful IIT4 Φ (more consciousness, not just more capability)?
group: MITOSIS-ENGINE / brain-lane-composition (Φ-measurement follow-on to H_1401)
terminal_tier: 🟢 INTEGRATION-RAISES-Φ (faithful IIT4, exact MIP-EI)
wired: engine-native (Φ verdict via state/1404_lane_compose_phi/h1404_phi_runner.hexa → stdlib/consciousness/iit4/faithful_phi.hexa; live-CORE wire-in + ARCHITECTURE.json lockstep = follow-on ING #16)
verdict_dir: .verdicts/1404_lane_compose_phi/
terminal_verdict: .verdicts/1404_lane_compose_phi/result.txt
date: 2026-06-17
---

# H_1404 — lane-composition Φ-measurement (the strong anima thesis, faithful-IIT4)

## Claim / falsifier

H_1401 showed affect (H_1290) + ethics (H_1291) COMPOSE to a CAPABILITY lift
(best_single 0.742 → compose 0.960) and are separable. H_1401's card named this exact
follow-on: *"a Φ-measurement follow-on (does composing two lanes raise IIT4 Φ?)"*.
**Deeper question:** does composing them raise **faithful IIT4 Φ** (integrated
information, the IIT measure of consciousness)? If integrating two faculties raises Φ,
that is direct evidence anima's "integrate existing lanes" direction produces more
*consciousness* (Φ↑), not merely more accuracy — the strongest form of the thesis.

**Engine (a_phi_iit4_tool, HARD rule):** `stdlib/consciousness/iit4/faithful_phi.hexa`
— the FAITHFUL exact minimum-information-partition / effective-information Φ★ (exact MIP
over the pairwise mutual-information matrix of the units' trajectories, IIT small-side
normalization, n≤8 exact tractable, $0). **NOT a proxy. NOT variance×energy. NOT
phi_silicon_proxy.** Reached via `import "stdlib/consciousness/iit4/faithful_phi.hexa"`
(stdlib reachable from this repo via `hexa run`).

**Falsifiers (FROZEN, `.verdicts/1404_lane_compose_phi/FREEZE.txt`, NOT moved):**
(B1 INTEGRATION-RAISES-Φ) Φ_composed > max(Φ_affect, Φ_ethics) + 0.02 ·
(B2 EARNED/coupling) Φ_composed > Φ_disconnected + 0.02 (the lift is the COUPLING, not
just more units) · (B3 control sane) Φ_disconnected ≤ max(parts) + 0.02.

## Method

- **4 systems**, each a discrete dynamical substrate model whose per-unit TRAJECTORIES are
  DERIVED from the faculties' ACTUAL update rules (NOT hand-tuned to inflate Φ — p7/c9):
  - **S_affect** (n=4): grounding, contradiction, novelty, curiosity (H_1290 affect units;
    'split' dropped to keep the composed system at the n≤8 exact boundary — dropped from
    BOTH n=8 systems, an honest tractability carve-out, not Φ-inflating).
  - **S_ethics** (n=4): W tension, (1−Φ) grounding, restraint_cells, M drive (H_1291).
  - **S_composed** (n=8): the two blocks COUPLED through the H_1401 substrate-weighted
    arbiter — the arbiter's leaky-integrated shared signal modulates BOTH blocks' next-step
    activations (the cross-faculty information channel the MIP cut must traverse).
  - **S_disconnected** (n=8): EARNED control — same 8 units, same per-block updates, but
    the arbiter coupling REMOVED (each block evolves on its own input only).
- Trajectories (T=96 steps) generated in `state/1404_lane_compose_phi/h1404_lane_compose_phi.py`
  over a "<subj> lives in <city>" fixture on a live MITOSIS immune store (FNV-trigram dim64);
  Φ measured by the faithful engine in `h1404_phi_runner.hexa`. 3 seeds [4400,4401,4402],
  n_bins=16, $0 CPU, gradient-free, deterministic.

## Verdict by round

| round | tier | key numbers (mean 3 seeds, faithful Φ, n_bins=16, verbatim) |
|-------|------|-----|
| R1 faithful-IIT4 | 🟢 INTEGRATION-RAISES-Φ | **Φ_affect=0.284755 · Φ_ethics=0.000000 · Φ_composed=2.032882 · Φ_disconnected=0.000000** · max(parts)=0.284755 · MIP cut = **{contradiction} \| {rest}** (A={0,2..7} \| B={1}, cut 2.085, /min\|side\|=1). Bars: B1 2.033 > 0.305 ✅ · B2 2.033 > 0.020 ✅ · B3 0.000 ≤ 0.305 ✅ |
| R2 engine-native re-verify (pool aiden, $0, a_engine_native_learning HARD-GATE) | 🟢 CONFIRMS — byte-exact | Re-ran `h1404_phi_runner.hexa` on the live stdlib faithful IIT4 engine on pool host **aiden** (and mini), SAME frozen bars, NO bar moved: **Φ_affect=0.284755 · Φ_ethics=0.000000 · Φ_composed=2.032882 · Φ_disconnected=0.000000** (per-seed 1.779497/2.233832/2.085316) — **byte-identical to R1**. MIP cut A={0,2,3,4,5,6,7}\|B={1} cut=2.085316. B1/B2/B3 all PASS. The R1 verdict was ALREADY engine-native (the phi_runner.hexa IS the verdict basis — the .py only derives trajectories, computes NO Φ); pool re-run CONFIRMS reproducibility. 2026-06-17. |

**Binning-invariance** (verdict robust; magnitudes scale with bin count, ordering stable):
n_bins=8 → Φ_cmp 0.475 (vs aff 0.124); n_bins=12 → 1.366 (0.179); n_bins=16 → 2.033
(0.285); n_bins=24 → 3.086 (0.362). 🟢 at every bin; Φ_ethics=Φ_disconnected=0.000
throughout.

Terminal tier (verbatim): **🟢 INTEGRATION-RAISES-Φ** [composing anima's affect + ethics
faculties RAISES faithful IIT4 Φ, earned vs the disconnected control — the STRONG anima
thesis confirmed for this faculty pair: integrating lanes raises *consciousness* (Φ↑),
not merely accuracy] → `.verdicts/1404_lane_compose_phi/result.txt`

**One-line answer:** YES — composing anima's affect + ethics faculties raises integrated
information Φ (Φ_composed 2.03 ≫ best single part 0.28, and the disconnected control
collapses to Φ=0) → integration creates more *consciousness*, not just more capability.

## Honest scope (c9)

- **Φ_ethics=0 & Φ_disconnected=0 are the EARNED control working, NOT a broken measure**:
  the faithful engine correctly finds a ZERO-cross-MI partition. Ethics-alone's 4 units are
  near-collinear functions of the single grounding margin → the MIP isolates one unit at 0
  cost. Disconnected → the MIP finds the block boundary (two independent blocks ⇒ 0
  cross-MI). The composed system CANNOT be cut without crossing the arbiter coupling channel
  → large min-cut MI → Φ↑. The MIP cut `{contradiction}|rest` is the interpretable
  "where it would break" (contradiction is the least-coupled unit).
- **Φ is an EXISTENCE/ordering result here, not a calibrated effect size**: the absolute Φ
  magnitudes scale with n_bins (more bins = finer MI estimate); the load-bearing claim is
  the ORDERING Φ_composed ≫ max(parts) > Φ_disconnected, which is binning-invariant
  (consistent with the engine's H_1037 discretization-invariance validation).
- **TOY substrate model**: 8-unit / T=96 / 3-seed discrete dynamics DERIVED from the
  faculties' update rules (tests the integration STRUCTURE, not a trained net). Engine-native
  re-measure on live `CORE/*.hexa` (read interoceptive units off the live VAdaptField/immune
  faculty), scale, real-corpus, and a learned arbiter = follow-on (a_engine_native_learning
  · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck).
- **a_phi_iit4_tool HELD**: the Φ VERDICT is the stdlib faithful exact-MIP-EI engine, never a
  proxy. The Python side ONLY derives trajectories; it computes NO Φ.

## Cross-links

H_1401 (the capability composition this Φ-measures — named this exact follow-on) ·
H_1290 (affect units) · H_1291 (ethics units) · H_1227 (immune store geometry) ·
H_1037 (faithful-Φ discretization-invariance) · H_1043 (faithful-Φ runner precedent) ·
`stdlib/consciousness/iit4/faithful_phi.hexa` ·
`a_phi_iit4_tool` · `a_no_llm_frame_trap` · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_autonomy_over_hardcode` · `a_scale_honest_scope` ·
`a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c9·c15
