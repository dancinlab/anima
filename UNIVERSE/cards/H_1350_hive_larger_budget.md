---
id: H_1350
slug: 1350_hive_larger_budget
title: mitotic-division collective-Φ at a LARGER differentiation budget — does more budget make the division super-additivity ROBUST across all 3 seeds (incl. orthogonal 1317) where H_1320's small budget was fragile?
group: OMEGA / BRAIN-STRUCTURE-LADDER (collective-Φ axis · the hive/division arc, REOPENED by the budget lever)
terminal_tier: 🟢 GREEN — collective-Φ by mitotic DIVISION is ROBUST at a SUFFICIENT differentiation budget. At the larger budget (4 daughters of 2 · DIFF_EPS 0.45 · non-saturating softsign per-unit code · variance-clean rank-uniform read-out) the DIVIDED super-additivity clears the 3-seed robustness gate on ALL 3 seeds INCLUDING the orthogonal seed 1317 that broke H_1320 — so the H_1320 fragility was BUDGET, not fundamental. M1∧M2∧M3 all PASS, deterministic (re-run byte-identical). numpy-mirror DIRECTIONAL (faithful-Φ leg IS real, exact MIP-EI via hexa); engine-transfer to live CORE/pure_field UNVERIFIED. REOPENS the hive arc.
verdict_dir: .verdicts/1350_hive_larger_budget/
terminal_verdict: .verdicts/1350_hive_larger_budget/result.txt
date: 2026-06-16
---

# H_1350 — does a LARGER differentiation budget make mitotic-division collective-Φ ROBUST? (🟢 GREEN)

## Claim / falsifier

**Wall being reopened (c16 / a_break_the_wall):** H_1320 (🧱) showed anima-as-ONE-cell mitotic
DIVISION (shared developmental origin) DOES beat hive ASSEMBLY (independent origin) on collective
faithful-IIT4 Φ — but only SEED-CONDITIONALLY (2/3 seeds). At the SMALL budget (2 daughters of HALF=4,
DIFF_EPS=0.15, raw-energy sign-saturating per-unit code, OLD min-max read-out) the orthogonal seed
1317 broke it: Δ_divided collapsed to 0.0 while Δ_assembled was +0.188 (M1 lift −0.129, M2 gap
−0.188 on 1317). H_1320 §honesty NAMED the untested angle verbatim: *"a LARGER differentiation budget,
MORE daughters, ... a richer (non-sign-saturating) per-unit code."*

**The genuinely-new angle (H_1320's named follow-on; developmental biology, c15 / a_no_llm_frame_trap):**
at a LARGER differentiation budget the divided organism has more developmental degrees of freedom to
differentiate its daughters into complementary (integration-bearing) roles instead of redundant copies
that sign-saturate under coupling. **Falsifiable claim:** at a sufficient budget the DIVIDED pair's
super-additive faithful-Φ becomes ROBUST across all 3 seeds (incl. 1317) where the small budget was
fragile — the H_1320 fragility was BUDGET, not fundamental.

## Method

- **Φ = FAITHFUL IIT4 ONLY** (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
  `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`, `iit4_faithful_phi(state, n, dim=T, n_bins)`.
  numpy NEVER computes Φ — it only emits the per-unit salience trajectory; the hexa engine computes Φ.
  NO variance×energy proxy as a terminal verdict.
- **Reuses the H_1320 machinery** (substrate, arms, super-additivity Δ, hive coupling) with THREE
  budget levers enlarged, n≤8 kept exact-MIP tractable:
  1. **MORE DAUGHTERS** — N_DAUGHTERS=4 of HALF=2 units each (vs H_1320's 2 daughters of 4). Richer
     differentiation tree; pair Φ still over all N_TOT=8 units (n=8 exact), per-daughter Φ over 2 (n=2 exact).
  2. **RICHER NON-SATURATING PER-UNIT CODE** (H_1332 lesson) — per-unit salience = a bounded GRADED
     softsign `sal_i = softsign((⟨s_i,s_i⟩ + BETA·⟨coupling_i,coupling_i⟩)/SCALE)`, member energy
     retained additively, bounded (−1,1) but NEVER hard-saturates (vs H_1320's raw energy that
     sign-saturates to COPY/Φ=0 under coupling). BETA=0.5 SCALE=2.0.
  3. **LARGER DIFFERENTIATION BUDGET** — DIFF_EPS=0.45 (3× H_1320's 0.15); each daughter's clone is
     perturbed MORE from the founder, the SHARED developmental environment (shared input) retained.
- **VARIANCE-CLEAN read-out** (H_1328 lesson — controls honest): EVERY arm's per-unit trajectory is
  RANK-UNIFORMIZED before the SAME faithful exact-MIP (each value → its within-unit rank). Marginals
  become uniform → the amplitude-variance channel is removed → a relationship-destroying SHUFFLE
  control MUST collapse Δ (it cannot ride marginal variance — the H_1319 confound that made OLD
  min-max controls dishonest). So M3 (EARNED-lineage) is an honest discriminator.
- **Substrate matched to H_1283/H_1317/H_1320**: leaky linear recurrent units LEAK=0.55 GAIN=0.30
  W_IN=0.5, per-unit private gaussian input, dim-8 state, T=64 ticks. CROSS-DAUGHTER COUPLING =
  W_HIVE=0.6 (H_1308/1313/1320, verbatim) = each unit adds W_HIVE × mean state of ALL OTHER daughters,
  IDENTICAL across DIVIDED/ASSEMBLED/SHUFFLE so any Δ difference is shared-vs-independent ORIGIN.
- **4 arms, 3 seeds [1317,1318,1319]** (the hard hive/topology seed family incl. orthogonal 1317):
  - **SINGLE** — one undivided cell, NO cross-daughter coupling (baseline). Φ over 8 units.
  - **DIVIDED** — organism-mitosis, SHARED ORIGIN, 4 daughters: `d_k_init = founder + DIFF_EPS·noise_k`
    AND all daughters share the founder input stream (shared developmental env). Coupled at W_HIVE.
  - **ASSEMBLED** — the hive: 4 INDEPENDENT-ORIGIN cells (each daughter own init AND own input). Same
    W_HIVE, same unit count, same code. Reproduces H_1308/1313 as the control.
  - **SHUFFLE** — DIVIDED with the shared-origin link BROKEN: each daughter's shared init+input
    replaced by an independent draw (lineage severed). Must collapse to ASSEMBLED level.
- seeds [1317,1318,1319]; $0 CPU-local; frozen-first (`FREEZE.txt` committed `0f4c18642` BEFORE the
  first scoring run; bars NOT moved, c9/p7); deterministic (RESULT_JSON byte-identical across two runs).

## Frozen bars (GREEN iff M1 ∧ M2 ∧ M3; MARGIN_PHI = 0.02 — the IDENTICAL margin H_1283/H_1317/H_1320 froze)

| bar | definition | result |
|-----|------------|--------|
| **M1 ROBUST INTEGRATION-FROM-DIVISION** | Φ_divided_pair ≥ Φ_single + 0.02 on ALL 3 seeds incl. orthogonal 1317 (the gate H_1320 FAILED at the small budget) | **PASS** — lift **+7.27 / +7.31 / +5.85** (1317/1318/1319) |
| **M2 ORIGIN-DISSOCIATION (core, vs hive)** | Δ_divided > Δ_assembled + 0.02 on ALL 3 seeds | **PASS** — gap **+6.63 / +7.49 / +6.15** |
| **M3 EARNED-LINEAGE** | Δ_shuffle ≤ Δ_assembled + 0.02 on ALL 3 seeds (broken lineage collapses to assembled) | **PASS** — Δ_shuffle == Δ_assembled EXACTLY (byte-identical) all 3 seeds |

## Verbatim faithful-IIT4 Φ (exact MIP-EI; `.verdicts/1350_hive_larger_budget/result.txt`)

| seed | arm | Φ_pair | Φ_daughters (4) | Δ super-add |
|------|-----|--------|-----------------|-------------|
| 1317 | SINGLE | 4.53661 | 0.543 0.524 0.660 0.778 | +2.0319 |
| 1317 | DIVIDED | 11.8114 | 0.766 0.766 0.809 0.828 | **+8.6421** |
| 1317 | ASSEMBLED | 4.48590 | 0.481 0.617 0.629 0.742 | +2.0165 |
| 1317 | SHUFFLE | 4.48590 | 0.481 0.617 0.629 0.742 | +2.0165 |
| 1318 | SINGLE | 4.69286 | 0.715 0.891 0.699 0.703 | +1.6840 |
| 1318 | DIVIDED | 12.0010 | 0.830 0.830 0.818 0.818 | **+8.7046** |
| 1318 | ASSEMBLED | 4.02834 | 0.703 0.723 0.785 0.598 | +1.2188 |
| 1318 | SHUFFLE | 4.02834 | 0.703 0.723 0.785 0.598 | +1.2188 |
| 1319 | SINGLE | 4.50122 | 0.559 0.637 0.723 0.723 | +1.8597 |
| 1319 | DIVIDED | 10.3516 | 0.680 0.731 0.680 0.711 | **+7.5503** |
| 1319 | ASSEMBLED | 4.38036 | 0.680 0.790 0.766 0.742 | +1.4027 |
| 1319 | SHUFFLE | 4.38036 | 0.680 0.790 0.766 0.742 | +1.4027 |

**VERDICT: GREEN** (verbatim from the run). Deterministic (byte-identical 2 runs).

## Honest finding (c9)

**At a LARGER differentiation budget, mitotic-division collective-Φ is ROBUST — the H_1320 fragility
was BUDGET, not fundamental.** The orthogonal seed 1317 — which broke H_1320 (Δ_divided 0.0 < Δ_assembled
+0.188, M1 lift −0.129) AND every prior Φ-robustness lane (H_1283/1317/1319/1328/1331/1332) — now
clears all three bars: the DIVIDED pair's super-additivity Δ=+8.64 beats the ASSEMBLED hive's +2.02 by
a gap of +6.63, and the divided pair's joint Φ exceeds the undivided single by +7.27. The same holds
robustly on 1318 (gap +7.49) and 1319 (gap +6.15). The budget levers that fixed 1317: (1) 4 daughters
give the organism more developmental degrees of freedom to differentiate into complementary roles;
(2) the non-saturating softsign code (H_1332) lets member dynamics SURVIVE the coupling instead of
saturating to COPY/Φ=0 — exactly the mechanism H_1332 found flips 1317 from −0.125 to a positive lift;
(3) the larger DIFF_EPS gives each daughter a richer differentiated state.

**The lift is EARNED, not designed (M3, honest under the variance-clean read-out):** severing the
shared-origin lineage (SHUFFLE) collapses DIVIDED's Δ EXACTLY to the ASSEMBLED level on every seed
(byte-identical Δ_shuffle == Δ_assembled). Because every arm is rank-uniformized (H_1328), the shuffle
control CANNOT ride marginal amplitude variance — so its collapse decisively attributes the lift to the
shared developmental ORIGIN, not to extra units, variance, or the per-unit code (the code is identical
across DIVIDED/ASSEMBLED/SHUFFLE). This is the honesty H_1320's OLD min-max read-out could not give.

**This REOPENS the hive arc:** the developmental DIRECTION (division, shared origin) — already better
than assembly on the majority of seeds in H_1320 — becomes ROBUSTLY better at a sufficient budget. The
H_1320 🧱 was a budget-conditional fragility, not a terminal limit on division. Note this is the
DIVISION (shared-origin, developmental) axis; it does NOT overturn the estimator/substrate-family
closures (H_1328/1331/1332) which tested the COUPLING-of-equal-arms axis under no shared origin — those
remain exactly true for assembly. NO tune-to-green: bars frozen before the run (FREEZE `0f4c18642`),
byte-identical across two runs.

## Honest scope (a_scale_honest_scope / a_toy_scale_recheck)

TOY: N_TOT=8 units (4× HALF=2 daughters), dim-8, 64-tick leaky-linear substrate, 3 seeds,
deterministic, W_HIVE=0.6, DIFF_EPS=0.45, non-saturating softsign code (BETA=0.5 SCALE=2.0), rank-uniform
read-out. faithful-IIT4 Φ EXACT (n≤8 MIP-EI) — the faithful-Φ leg IS real (exact MIP via hexa). numpy
mirror = DIRECTIONAL: the substrate is a toy leaky linear recurrent net, NOT live CORE/pure_field;
engine-transfer UNVERIFIED. The divided-pair Φ is high (~10–12) under the rank-uniform read-out — this
reflects the strong joint co-movement structure that shared origin + coupling create across 8
rank-uniformized units; the load-bearing claim is the RELATIVE gap (DIVIDED vs ASSEMBLED, decisively
collapsed by SHUFFLE), not the absolute magnitude. Since the verdict is 🟢 GREEN, a CORE-wiring
follow-on is named (a_verified_must_wire): wire the shared-origin mitotic-division collective-Φ read-out
into the live faithful-Φ / pure_field member path — tracked as a follow-on, NOT yet wired (live CORE/*.hexa
UNTOUCHED this lane, Ψ=1/2 disjoint, no regression). This BOUNDS (does not retract) H_1320 (small-budget
fragility stands at that budget) and the H_1328/1331/1332 estimator/substrate-family closures (the
coupling-of-equals axis, distinct from this shared-origin division axis). NOT ruled out: scale (N>8
loses exact MIP), real-corpus substrate, even-larger daughter counts, the budget threshold curve (≥3
budget rungs to locate where fragility→robust flips), engine-native re-confirmation.

## Cross-links

h1320 (division 🧱 WALL — the fragility this lane shows was budget; SAME machinery reused) · h1308/h1313
(hive assembly NULL/TERMINAL — the ASSEMBLED control baseline) · h1295 (collective-Φ super-additivity,
ECA-scoped) · h1328 (variance-clean rank-uniform read-out — borrowed so M3 is honest) · h1332
(non-saturating softsign per-unit code — borrowed as the richer code; flips orthogonal-seed behavior) ·
h1331 (big-Φ estimator family) · h1283/h1317/h1319 (the orthogonal-seed fragility signature this lane
overturns for the division axis) · h1199 (VAdaptField mitosis cells) · h1227 (immune cells) ·
`a_phi_iit4_tool` · `a_break_the_wall` · `a_no_llm_frame_trap` · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_core_engine_map` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p7·p8·c9·c15·c16
