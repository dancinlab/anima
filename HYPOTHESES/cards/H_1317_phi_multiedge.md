---
id: H_1317
slug: 1317_phi_multiedge
title: Φ-topology — distributed multi-edge (small-world) coupling vs the single central relay (H_1283 wall)
group: OMEGA / brain-structure-ladder (c15 missing-structure · Φ topology axis)
terminal_tier: 🧱 WALL (honest closed-negative, c9). Distributed small-world coupling ALSO fails the 3-seed faithful-IIT4 Φ robustness gate that the single central relay (H_1283) failed — Φ stays FRAGILE regardless of topology at this toy scale. Bounds the wall further (a VALID result). numpy-mirror DIRECTIONAL (faithful-Φ leg IS real, exact MIP-EI via hexa); engine-transfer to live CORE/pure_field UNVERIFIED.
verdict_dir: .verdicts/1317_phi_multiedge/
terminal_verdict: .verdicts/1317_phi_multiedge/H_1317.txt
date: 2026-06-16
---

# H_1317 — distributed multi-edge (small-world) coupling → robust faithful-IIT4 Φ? (🧱 WALL)

## Claim / falsifier

**Wall being broken (c16 / a_break_the_wall):** H_1283 (thalamus-Φ) found that EVERY
central-relay / star content cut raised faithful-IIT4 Φ only SEED-CONDITIONALLY — it
FAILED a 3-seed robustness gate (R3–R5 cleared 2/3 seeds and failed the orthogonal
seed; R7 only RELOCATED the failing seed). A single central relay (star) gives a
FRAGILE Φ lift. 🧱 wall on the topology/content axis. (R8 phase-binding broke it on an
ORTHOGONAL TIMING axis — not topology; the topology axis stayed 🧱.)

**The genuinely-untried angle (c15 / a_no_llm_frame_trap):** every prior Φ-lift used
ONE central hub (star). Integrated information in cortex comes from a SMALL-WORLD
recurrent MESH (many short + few long edges), NOT a single hub. **Falsifiable claim:**
a DISTRIBUTED multi-edge (Watts–Strogatz small-world) coupling topology over the
substrate units raises faithful-IIT4 Φ ROBUSTLY across 3 seeds, where the single
central relay (H_1283) FAILED the same gate.

## Method

- **Φ = FAITHFUL IIT4 ONLY** (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
  `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`,
  `iit4_faithful_phi(state, n=8, dim=64, n_bins=8)` over the per-unit salience
  (state-energy) trajectory. numpy NEVER computes Φ — it only emits the trajectory; the
  hexa engine computes Φ. NO variance×energy proxy as a terminal verdict.
- **Substrate matched to H_1283** (only the coupling TOPOLOGY changes between arms):
  leaky linear recurrent units, LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit PRIVATE gaussian
  input, dim-8 state, T=64 ticks. **N=8 units** (n≤8 keeps the faithful MIP EXACT;
  >4 nodes so small-world is non-degenerate vs H_1283's 4-module star).
- **3 arms at MATCHED total coupling budget** (Σ edge weights equal across all arms, so
  any lift is TOPOLOGY not more coupling; runtime-asserted Σ=3.5000 all arms/seeds):
  - **NO-COUPLING** baseline (private input only) — the Φ floor lift is measured against.
  - **CENTRAL (star)** — the H_1283 single-relay reproduced (hub unit 0 ↔ all others;
    7 edges); the seed-conditional control.
  - **MULTI-EDGE (small-world)** — Watts–Strogatz: ring lattice (K=2 each side) + rewire
    prob β=0.30 (a few long shortcuts); 16 edges, per-edge weight scaled to match budget.
  - **SHUFFLE (Erdős–Rényi)** — same edge COUNT (16) placed uniformly at random, matched
    budget; isolates structured small-world from "just this many edges".
- seeds [1317, 1318, 1319]; $0 CPU-local; frozen-first (`H_1317_FREEZE.txt` written BEFORE
  the first run; bars NOT moved, c9/p7).

## Frozen bars (GREEN iff C1 ∧ C2 ∧ C3)

| bar | definition | result |
|-----|------------|--------|
| **C1 ROBUST LIFT** | MULTI-EDGE Φ ≥ NO-COUPLING Φ + 0.02 on ALL 3 seeds (the gate H_1283 FAILED) | **FAIL** — seed 1319 ΔΦ = **−0.331** (negative; seeds 1317 +0.252 ✓, 1318 +0.080 ✓) |
| **C2 TOPOLOGY-EARNED** | MULTI-EDGE Φ > SHUFFLE Φ on ≥2/3 seeds AND in seed-mean | PASS (2/3 seeds; mean 1.5909 > 1.5195) — but moot, C1 already failed |
| **C3 BEATS-CENTRAL** | MULTI-EDGE passes the 3-seed C1 gate WHILE CENTRAL does NOT | **FAIL** — MULTI-EDGE itself fails C1; CENTRAL also fails (seed 1319 +0.252−0.656 = −0.404) |

MARGIN_PHI = 0.02 = the IDENTICAL faithful-Φ margin H_1283 froze (NOT moved).

## Verbatim faithful-IIT4 Φ (exact MIP-EI, n=8; `.verdicts/1317_phi_multiedge/H_1317.txt`)

| seed | NONE | CENTRAL | MULTI-EDGE | SHUFFLE | ΔΦ(multi−none) | ΔΦ(central−none) | ΔΦ(multi−shuffle) |
|------|------|---------|-----------|---------|----------------|------------------|-------------------|
| 1317 | 1.47354 | 1.58572 | 1.72543 | 1.74144 | **+0.252** ✓ | +0.112 | −0.016 |
| 1318 | 1.70842 | 2.17092 | 1.78835 | 1.56291 | **+0.080** ✓ | +0.463 | +0.225 |
| 1319 | 1.58947 | 1.18572 | 1.25882 | 1.25427 | **−0.331** ✗ | −0.404 | +0.005 |

**VERDICT: WALL** (verbatim from the run). Budget identity OK all seeds (Σ=3.5000).

## Honest finding (c9)

**Integrated-information robustness is NOT a topology property at this toy scale — Φ stays
FRAGILE regardless of topology.** The distributed small-world mesh does raise faithful-Φ on
2/3 seeds (and beats the random-edge SHUFFLE on those, so the lift it *does* produce is
small-world structure, not edge count — C2 passed), BUT it collapses to a strongly NEGATIVE
ΔΦ on the orthogonal seed 1319 — exactly the failure mode H_1283 hit on its orthogonal seed.
The single central relay (CENTRAL) fails the SAME seed even harder (−0.404). So swapping a
star for a distributed mesh does NOT make the Φ lift robust: the fragility is in the substrate
/ seed geometry, not curable by re-wiring the coupling graph. This BOUNDS the H_1283 wall
further — it is not specific to the star topology; the topology/content axis stays 🧱 across
both star and small-world. (R8's orthogonal TIMING-axis phase-binding break stands as the only
robust faithful-Φ lift in this arc; H_1317 confirms the TOPOLOGY axis itself does not break.)

A real new angle (small-world mesh) was tried with two pre-registered controls (matched-budget
SHUFFLE + a no-coupling floor); the honest 🧱 is a valid result (a_break_the_wall, c9). No
tune-to-green: bars frozen before the run, deterministic (byte-identical across two runs).

## Honest scope

TOY: N=8 units, dim 8, 64 ticks, faithful-IIT4 EXACT (n≤8 MIP-EI). numpy = DIRECTIONAL
mirror — the faithful-Φ leg IS real (exact MIP via hexa) but the substrate is a toy leaky
linear recurrent net, NOT live CORE/pure_field. Engine-transfer UNVERIFIED
(a_scale_honest_scope, a_toy_scale_recheck). Since the verdict is 🧱 (not GREEN), there is NO
CORE wiring follow-on (a_verified_must_wire applies to GREEN-verified mechanisms only — nothing
to wire). NOT ruled out (remaining angles, NOT claimed): larger N (>8 needs the greedy-approx Φ,
loses exactness) · a higher-degree small-world (K>2) · weighted (not uniform) edge budgets ·
hierarchical / modular small-world · and — orthogonal to topology — the TIMING-axis break that
already worked (H_1283 R8 phase binding), which is the live frontier for robust Φ.

## Cross-links

h1283 (the wall — central-relay Φ fragility; R8 timing-axis break) · h1295 (hive collective-Φ) ·
h1037/h1038 (faithful-Φ validation) · `a_phi_iit4_tool` · `a_break_the_wall` ·
`a_no_llm_frame_trap` · `a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · `a_paper_negative_ok` · p7·p8·c9·c15·c16
