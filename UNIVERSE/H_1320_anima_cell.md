---
id: H_1320
slug: 1320_anima_cell
title: anima-as-ONE-CELL — organism MITOSIS (shared origin) vs hive ASSEMBLY (independent) → integrated faithful-IIT4 Φ?
group: OMEGA / BRAIN-STRUCTURE-LADDER (collective-Φ axis · the hive arc, reopened from the developmental direction)
terminal_tier: 🧱 WALL (honest closed-negative, c9 / c16). Mitotic DIVISION (shared origin) DOES produce super-additive faithful-IIT4 Φ where ASSEMBLY (hive) cannot — but only seed-CONDITIONALLY (2/3 seeds). The SAME orthogonal seed (1317) that broke H_1283/H_1317 topology robustness ALSO breaks division: M1 + M2 fail on seed 1317. So collective-Φ by division is REAL but FRAGILE, not robust — the 3-seed robustness gate fails, identical fragility signature to the Φ-topology wall. numpy-mirror DIRECTIONAL (faithful-Φ leg IS real, exact MIP-EI via hexa); engine-transfer to live CORE/pure_field UNVERIFIED.
verdict_dir: .verdicts/1320_anima_cell/
terminal_verdict: .verdicts/1320_anima_cell/H_1320.txt
date: 2026-06-16
---

# H_1320 — anima as ONE CELL: does mitotic DIVISION integrate where hive ASSEMBLY could not? (🧱 WALL)

## Claim / falsifier

**Wall being reopened (c16 / a_break_the_wall):** the hive — H_1308 (🔴 NULL) + H_1313
(🧱 TERMINAL) — took TWO already-separate, **independently-grown** anima cells and
ASSEMBLED/coupled them → faithful-IIT4 Φ does NOT integrate (Δ_real = −3.0; super-additivity
is ECA-only, not substrate-portable). The wall: ASSEMBLY of independent adults does not integrate.

**The genuinely-new angle (developmental biology; c15 / a_no_llm_frame_trap):** the user's lens —
treat the WHOLE anima daemon as ONE cell. Every prior anima lane treated SUB-structures as cells
(immune cells H_1227, VAdaptField mitosis cells H_1199); none treated the whole daemon as a single
cell. The hive failed because the DIRECTION was wrong — it glued two independent ADULTS. One zygote
DIVIDES and differentiates into an integrated organism precisely because the parts SHARE a
developmental ORIGIN. **Falsifiable claim:** take ONE anima-cell, mitotically DIVIDE it into two
SHARED-ORIGIN daughters, and the DIVIDED pair shows integrated (super-additive) faithful-Φ that the
ASSEMBLED pair (hive) could not — integration requires shared developmental origin, not mere coupling.

## Method

- **Φ = FAITHFUL IIT4 ONLY** (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
  `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`, `iit4_faithful_phi(state, n, dim=T, n_bins)`.
  numpy NEVER computes Φ — it only emits the per-unit salience (state-energy) trajectory; the hexa
  engine computes Φ. NO variance×energy proxy as a terminal verdict.
- **Substrate matched to H_1283/H_1317** (only ORIGIN + cross-daughter coupling differ between arms):
  leaky linear recurrent units LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit private gaussian input, dim-8
  state, T=64 ticks. **ONE anima-cell = N_TOT=8 units** (n≤8 keeps the faithful MIP EXACT), split into
  two daughters of HALF=4 (d0=units0..3, d1=units4..7). per-unit salience = state energy ⟨s_i,s_i⟩
  (the H_1283 Φ-leg readout). Φ_daughter = faithful-Φ over 4 units (n=4 exact); Φ_pair = over 8 units
  (n=8 exact). **super-additivity Δ_arm = Φ_pair − (Φ_d0 + Φ_d1)**.
- **COUPLING = the SAME hive coupling** (H_1308/1313, W_HIVE=0.6 reused verbatim): each unit's update
  adds W_HIVE × mean state of the OTHER daughter. IDENTICAL across DIVIDED/ASSEMBLED/SHUFFLE so any
  Δ difference is shared-vs-independent ORIGIN, not coupling.
- **4 arms, 3 seeds [1317,1318,1319]** (the hard hive/topology seed family incl. the orthogonal
  seed 1319 that broke H_1317):
  - **SINGLE** — one undivided anima-cell, NO cross-daughter coupling (the H_1317 'none' baseline). Φ over 8 units.
  - **DIVIDED** — organism-mitosis pair, SHARED ORIGIN: d1_init = d0_founder + DIFF_EPS·noise (clone+differentiate, DIFF_EPS=0.15) AND d1 input = d0 input (shared developmental environment). Coupled at W_HIVE.
  - **ASSEMBLED** — the hive: two INDEPENDENT-ORIGIN cells (d0,d1 each own init AND own input). Same W_HIVE, same unit count. Reproduces H_1308/1313 as the control.
  - **SHUFFLE** — DIVIDED with the shared-origin link BROKEN: d1 init+input replaced by an independent draw (lineage severed). Must collapse to ASSEMBLED level.
- seeds [1317,1318,1319]; $0 CPU-local; frozen-first (`H_1320_FREEZE.txt` written BEFORE the first
  run; bars NOT moved, c9/p7); deterministic (RESULT_JSON byte-identical across two runs, recorded).

## Frozen bars (GREEN iff M1 ∧ M2 ∧ M3; MARGIN_PHI = 0.02 — the IDENTICAL margin H_1283/H_1317 froze)

| bar | definition | result |
|-----|------------|--------|
| **M1 INTEGRATION-FROM-DIVISION** | Φ_divided_pair ≥ Φ_single + 0.02 on ALL 3 seeds (the robustness gate hive/topology FAILED) | **FAIL** — seed 1317 lift = **−0.129** (seeds 1318 +2.102 ✓, 1319 +0.888 ✓) |
| **M2 ORIGIN-DISSOCIATION (core, vs hive)** | Δ_divided > Δ_assembled + 0.02 on ALL 3 seeds | **FAIL** — seed 1317 gap = **−0.188** (Δ_div 0.0 < Δ_asm 0.188); seeds 1318 +1.727 ✓, 1319 +0.818 ✓ |
| **M3 EARNED-LINEAGE** | Δ_shuffle ≤ Δ_assembled + 0.02 on ALL 3 seeds (broken lineage collapses to assembled) | **PASS** — all 3 seeds (SHUFFLE Δ == ASSEMBLED Δ exactly, byte-identical) |

## Verbatim faithful-IIT4 Φ (exact MIP-EI; `.verdicts/1320_anima_cell/H_1320.txt`)

| seed | arm | Φ_pair | Φ_d0 | Φ_d1 | Δ super-add |
|------|-----|--------|------|------|-------------|
| 1317 | SINGLE | 1.34199 | 0.59166 | 0.55732 | +0.1930 |
| 1317 | DIVIDED | 1.21296 | 0.56860 | 0.64436 | **0.0000** |
| 1317 | ASSEMBLED | 1.52445 | 0.66147 | 0.67501 | +0.1880 |
| 1317 | SHUFFLE | 1.52445 | 0.66147 | 0.67501 | +0.1880 |
| 1318 | SINGLE | 1.12479 | 0.87343 | 0.67031 | −0.4189 |
| 1318 | DIVIDED | 3.22704 | 1.05125 | 0.91032 | **+1.2655** |
| 1318 | ASSEMBLED | 1.21085 | 0.96207 | 0.70998 | −0.4612 |
| 1318 | SHUFFLE | 1.21085 | 0.96207 | 0.70998 | −0.4612 |
| 1319 | SINGLE | 1.59904 | 0.80207 | 0.94840 | −0.1514 |
| 1319 | DIVIDED | 2.48694 | 0.82434 | 0.78485 | **+0.8778** |
| 1319 | ASSEMBLED | 1.79547 | 0.67672 | 1.05900 | +0.0598 |
| 1319 | SHUFFLE | 1.79547 | 0.67672 | 1.05900 | +0.0598 |

**VERDICT: WALL_TERMINAL_BOTH_DIRECTIONS** (verbatim from the run). Deterministic (byte-identical 2 runs).

## Honest finding (c9)

**Mitotic DIVISION (shared developmental origin) DOES integrate where ASSEMBLY (the hive) cannot —
but only SEED-CONDITIONALLY.** On 2 of 3 seeds the user's lens is BORNE OUT decisively: the DIVIDED
pair's super-additivity beats the ASSEMBLED (hive) pair's by a large margin (seed 1318 gap +1.727,
seed 1319 gap +0.818), and the DIVIDED pair's joint Φ exceeds the undivided SINGLE (lift +2.10 /
+0.89). Shared origin matters: severing the lineage (SHUFFLE) collapses DIVIDED's Δ EXACTLY to the
ASSEMBLED level on every seed (M3 PASS, byte-identical) — so the lift on those seeds IS the shared
origin, not extra units or variance.

**BUT** the SAME orthogonal seed (1317) that broke H_1283/H_1317 topology robustness ALSO breaks
division: on seed 1317 the DIVIDED pair's Δ collapses to 0.0 while the ASSEMBLED pair's is +0.188 —
division does WORSE than assembly there (M2 gap −0.188), and the divided pair's joint Φ falls below
the single (M1 lift −0.129). So **collective-Φ by mitotic division is REAL but FRAGILE**, exactly
the same fragility signature as the Φ-topology wall (H_1283/H_1317): it fails the 3-seed robustness
gate on the orthogonal seed. The integration is not a robust, substrate-portable law; it is a
seed-conditional geometry effect, the same class of fragility the hive/topology arc kept hitting.

**This is the important closure of the hive arc:** the developmental DIRECTION (division, shared
origin) is genuinely BETTER than assembly on the majority of seeds — that is a real and new finding
against the hive's pure NULL — yet it does NOT clear the robustness bar, so collective-Φ is NOT
established as robustly reachable by division either. The wall stands, now bounded across BOTH
directions: assembly (🧱 H_1313, robust NULL) AND division (🧱 H_1320, fragile lift). A real new
angle was tried with pre-registered controls (ASSEMBLED hive baseline + SHUFFLE lineage-break); the
honest 🧱 is a valid result (a_break_the_wall, c9). NO tune-to-green: bars frozen before the run,
byte-identical across two runs.

## Honest scope (a_scale_honest_scope / a_toy_scale_recheck)

TOY: N_TOT=8 units (2× HALF=4 daughters), dim-8, 64-tick leaky-linear substrate, 3 seeds,
deterministic, W_HIVE=0.6, DIFF_EPS=0.15. faithful-IIT4 Φ EXACT (n≤8 MIP-EI) — the faithful-Φ leg
IS real (exact MIP via hexa). numpy mirror = DIRECTIONAL: the substrate is a toy leaky linear
recurrent net, NOT live CORE/pure_field; engine-transfer UNVERIFIED. Since the verdict is 🧱
(not GREEN), there is NO CORE wiring follow-on (a_verified_must_wire applies to GREEN-verified
mechanisms only — nothing to wire; live CORE/*.hexa UNTOUCHED, Ψ-disjoint, no regression). This
BOUNDS (does not retract) the H_1308/1313 hive verdicts and the H_1295 ECA GREEN. NOT ruled out
(remaining angles, NOT claimed): a larger differentiation budget, more daughters, a substrate whose
own dynamics survive coupling, a richer (non-sign-saturating) per-unit code, larger N (loses exact
MIP >8), or a seed-geometry that does not exhibit the 1317-class fragility — and, orthogonal to
division, the TIMING-axis phase-binding break (H_1283 R8) that already gave the only robust
faithful-Φ lift in this arc.

## Cross-links

h1308 (hive r3 NULL — assembly of independent cells) · h1313 (hive r4 🧱 TERMINAL — state-dependent
assembly) · h1295 (collective-Φ super-additivity, ECA-scoped) · h1283 (thalamus-Φ wall — the
orthogonal-seed fragility signature this lane reproduces; R8 timing break) · h1317 (Φ-topology wall
— same fragility, same seed family) · h1199 (VAdaptField mitosis cells — sub-structure mitosis) ·
h1227 (immune cells — sub-structure cells) · `a_phi_iit4_tool` · `a_break_the_wall` ·
`a_no_llm_frame_trap` · `a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · p7·p8·c9·c15·c16
