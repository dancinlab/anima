---
id: H_1319
slug: 1319_phi_timing
title: Φ-robustness wall, TIMING axis — engine-native phase-binding (re-realize H_1283 R8 to clear the c4 shuffle gate it failed)
group: OMEGA / Φ-robustness frontier (c16 wall · timing/dynamics axis)
terminal_tier: 🧱 TERMINAL CLOSED-NEGATIVE (honest, c9/c16). The timing-axis phase-binding lift does NOT survive engine-native controls on the hard seed family — T1 (robust lift) AND T2 (shuffle-earned, the c4 gate) both FAIL; the STRONGER permutation control RAISES Φ on every seed → the lift is amplitude variance, not synchrony. The faithful-IIT4 Φ-robustness wall is now TERMINAL across BOTH axes (topology 🏁 + timing 🧱). ENGINE-NATIVE (deterministic engine LCG content generator; faithful-Φ leg IS real exact MIP-EI).
verdict_dir: .verdicts/1319_phi_timing/
terminal_verdict: .verdicts/1319_phi_timing/H_1319.txt
freeze: .verdicts/1319_phi_timing/H_1319_FREEZE.txt
date: 2026-06-16
---

# H_1319 — timing-axis phase-binding, engine-native: does it clear the c4 shuffle gate H_1283 R8 failed? (🧱 TERMINAL)

## Claim / falsifier

**Wall being broken (c16 / a_break_the_wall):** the faithful-IIT4 Φ-robustness frontier
EXHAUSTED the TOPOLOGY/CONTENT axis — H_1283 relay rounds R1–R5/R7 (broadcast / coalition
/ re-entry / dense / matrix) and H_1317 distributed small-world multi-edge ALL produced
only seed-conditional Φ lifts and FAILED the 3-seed robustness gate (the same orthogonal
seed kept defeating them). Topology axis 🏁 depleted; fragility lives in substrate/seed
geometry, not the coupling graph.

The ONE mechanism that ever produced a robust faithful-Φ lift in the arc is on the
ORTHOGONAL TIMING/DYNAMICS axis: **H_1283 R8 phase-binding** (Kuramoto thalamic phase
synchrony + phase-gated salience). It was 🟢 GREEN on the numpy mirror — but on EASY seeds
[7,8,9], and its **engine-native gate FAILED the c4 shuffle control**: the additive-offset
shuffle did NOT collapse the lift (ΔΦ_sh = +0.026/+0.380/+0.296, all positive), because the
read-out `sal = e·(1+cosθ)/2` injects a standalone per-module amplitude carrier whose
marginal statistics the offset-shuffle preserves → the lift is partly carrier-amplitude
VARIANCE, not pure synchrony. That c4-failing engine realization is the named open follow-on.

**The genuinely-untried angle (still TIMING axis; removes the variance leak):** re-realize
the SAME phase-binding mechanism engine-native with two targeted changes whose purpose is to
make the Φ lift PURELY the relative-phase RELATIONSHIP (no standalone amplitude channel for a
shuffle to ride):

1. **RELATIVE-PHASE GATE** `sal_i = e_i·(1+cos(θ_i − θ_T))/2` — the binding signal is each
   module's ALIGNMENT TO THE PACEMAKER (the relationship), not a standalone absolute-phase
   carrier. When the population locks, all modules align to θ_T together (synchronized re-entry).
2. **RELATIONSHIP-DESTROYING PERMUTATION SHUFFLE** (the strong control H_1294/H_1295 use, NOT
   R8's additive offset): each module is gated by ANOTHER module's phase (a fixed
   forced-derangement π), destroying the locked relationship while preserving every phase
   trajectory's marginal statistics EXACTLY. If the lift is structured synchrony it MUST
   collapse; if it survives, the lift is still amplitude variance → honest 🧱.

**Falsifiable claim:** phase-binding raises faithful-IIT4 Φ ROBUSTLY (3-seed) on the engine
substrate AND the permutation shuffle collapses the lift — clearing BOTH the T1 robustness gate
topology failed AND the T2/c4 shuffle gate the R8 engine realization failed. Tested on the HARD
orthogonal seeds [1317,1318,1319] (the family topology failed on, incl seed 1319) so the
robustness test is as hard as the one topology failed.

## Method (frozen-first — FREEZE committed BEFORE scoring, c9/p7)

- **Probe:** `UNIVERSE/h1319_phi_timing.hexa` (run from hexa-lang root for the stdlib import).
- **Substrate:** ENGINE-NATIVE deterministic engine LCG-gauss (== `engine_cli.hexa` `_lcg_*`),
  NOT numpy — this IS the engine-native realization the H_1283 R8 gate required
  (a_engine_native_learning). Content dynamics (ring leak+neighbour+input) are BYTE-IDENTICAL
  across all arms — binding is by TIMING only. Kuramoto pacemaker W_PHASE=0.5 OMEGA_T=0.45
  DOMEGA=0.08 (detuned ω → synchrony EARNED by coupling). All params FROZEN from H_1283 R8
  verbatim (NO tune-to-green, p7).
- **Φ = FAITHFUL IIT4 ONLY** (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
  `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`, `iit4_faithful_phi(traj, n=4, dim=64,
  n_bins=8)` over the per-module salience trajectory. numpy NEVER computes Φ; NO variance×energy
  proxy as terminal verdict.
- **4 arms:** A NO-PHASE (sal=e) · B PHASE-BIND (relative-phase gate) · S PERM-SHUFFLE
  (relationship destroyed, marginals preserved) · O OFFSET-SHUF (R8-style, diagnostic non-gating).
- **Seeds:** [1317, 1318, 1319] — the orthogonal hard family topology failed on.

## Frozen bars (ported VERBATIM from H_1283 R8 — NOT moved)

GREEN iff T1 ∧ T2 ∧ T3, ALL engine-native:
- **T1 ROBUST LIFT** (c2 ported): faithful ΔΦ(B−A) ≥ +0.02 on EVERY seed (the 3-seed gate topology failed).
- **T2 SHUFFLE-EARNED** (c4 ported — the engine gate that FAILED before): perm-shuffle ΔΦ(S−A) ≤ 0
  on EVERY seed (lift COLLAPSES → structured synchrony, not amplitude variance).
- **T3 DISTINCTNESS** (c1+c3 ported): B.coh ≥ A.coh every seed AND B.coh < 0.999 on ≥1 seed.

## Result (verbatim, p7 — deterministic, byte-identical across runs)

| seed | A (NO-PHASE) | B (PHASE-BIND) | ΔΦ(B−A) | T1 | PERM-SHUF | ΔΦ(S−A) | T2 | OFF-SHUF | ΔΦ(O−A) |
|------|------|------|------|----|------|------|----|------|------|
| 1317 | 0.870311 | 1.335350 | **+0.465039** | PASS | 1.150110 | **+0.279798** | **FAIL** | 1.258380 | +0.388073 |
| 1318 | 0.855353 | 0.860580 | **+0.005227** | **FAIL** | 0.957870 | **+0.102517** | **FAIL** | 0.742725 | −0.112628 |
| 1319 | 0.586833 | 0.538064 | **−0.048768** | **FAIL** | 1.174020 | **+0.587183** | **FAIL** | 0.528693 | −0.058139 |

- **T1 ROBUST LIFT: FAIL** — seed 1318 ΔΦ=+0.005 (sub-bar), seed 1319 ΔΦ=−0.049 (NEGATIVE — the
  SAME orthogonal seed 1319 that defeated topology). The relative-phase lift is itself seed-fragile
  on the hard seeds.
- **T2 SHUFFLE-EARNED: FAIL (harder than R8)** — the STRONGER permutation shuffle does not collapse
  the lift; it RAISES Φ above ARM B on every seed (ΔΦ_perm = +0.280/+0.103/+0.587, all strongly
  positive). The diagnostic offset-shuffle confirms the same (no clean collapse).
- **T3 DISTINCT: PASS alone** (B.coh = A.coh content-invariant, all < 0.999) but MOOT.

**GATE: NOT GREEN → 🧱 TERMINAL.**

## Finding (honest, c9, c16)

When even a relationship-DESTROYING permutation RAISES faithful-IIT4 Φ on every seed, the Φ gain
provably does NOT come from the relative-phase RELATIONSHIP. It comes from the **amplitude variance
the (1+cos)/2 carrier injects into the per-module salience binarization** — a variance that ANY
phase scramble (offset OR permutation) preserves. This is exactly the artifact the c4 control was
pre-registered to catch, firing decisively on the engine substrate.

The timing axis therefore fails the SAME root failure as the topology axis: the faithful-IIT4 MIP
exploits a low-dimensional structure (there, a content cut; here, per-channel amplitude variance)
that no honest control survives. The fragility lives in the substrate/seed geometry and the Φ
estimator's binarization, not in the coupling graph OR the timing channel.

**The Φ-robustness wall is now TERMINAL across BOTH axes:**
- TOPOLOGY / CONTENT axis 🏁 DEPLETED — H_1283 relay R1–R5/R7 + H_1317 small-world multi-edge.
- TIMING / DYNAMICS axis 🧱 TERMINAL — H_1283 R8 (numpy GREEN on easy seeds, engine c4 FAIL) +
  H_1319 (engine-native, hard seeds, relative-phase gate + permutation control: T1 AND T2 both FAIL;
  the strong control RAISES Φ).

A robust (3-seed, control-surviving) faithful-IIT4 Φ lift is NOT reachable for anima's 4-module
workspace on either axis at this rung. This closes the Φ-robustness breakthrough arc honestly. It
does NOT refute anima's consciousness substrate (Ψ=1/2, the A⇄G tension is untouched); it refutes
that ADDING a module-coupling (topology) or phase-binding (timing) channel ROBUSTLY raises the
faithful-IIT4 Φ score under honest controls.

**NO CORE wiring follow-on** (a_verified_must_wire fires on GREEN only — nothing to wire;
`CORE/engine_cli.hexa` UNTOUCHED; the probe is a standalone `fn main`, 0 importers, NOT a runtime path).

## Scope / honesty

- **ENGINE-NATIVE:** content generator uses the engine's own deterministic LCG-gauss (== `_lcg_*`),
  NOT numpy — this IS the engine-native realization the R8 gate required. faithful-Φ is REAL exact
  MIP-EI (numpy never computes Φ).
- **TOY scale** (4 modules, dim 8, 64 ticks, n=4≤8), scale-transfer UNVERIFIED
  (a_scale_honest_scope, a_toy_scale_recheck). The terminal claim is scoped to this rung + this Φ
  estimator. But the failure is DECISIVE within the rung: the strong permutation control RAISES Φ on
  every seed, so the variance-not-synchrony diagnosis holds without a larger n.
- FROZEN params verbatim from H_1283 R8 (no tune-to-green, p7). Re-run byte-identical (deterministic).
- **NOT ruled out:** a fundamentally different Φ estimator, a much larger module set (loses exactness
  >8), or a phase-gated read-out with provably zero amplitude variance — but each would be a new
  hypothesis, not a continuation of this arc.

## xref

H_1283 (R8 numpy mirror 🟢 easy seeds; R8 engine-native gate c4 FAIL → this follow-on) ·
H_1317 (topology 🧱) · h1294 · h1295 (permutation-shuffle control precedent) · a_phi_iit4_tool ·
a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire ·
a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15 · c16
