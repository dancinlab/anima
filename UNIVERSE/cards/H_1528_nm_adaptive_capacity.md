# H_1528 🧱🌱 NEUROMODULATION via ADAPTIVE CAPACITY (neurogenesis) — WALL HOLDS

**tier:** 🧱 (DIRECTIONAL / numpy mirror — engine-native R2 deferred ING)
**verdict:** WALL (11th independent lens on the H_1284 NEUROMODULATION wall; the
capacity family is INERT just like the 10 operating-point lenses)
**wired:** DIRECTIONAL-mirror (numpy; a_engine_native_learning — engine R2 = ING follow-on)
**source:** UNIVERSE (fleet wall-break lane)
**artifacts:** `state/1528_nm_adaptive_capacity/h1528_adaptive_capacity.py` ·
`state/verdicts/1528_nm_adaptive_capacity/H_1528_FREEZE.txt` ·
`state/verdicts/1528_nm_adaptive_capacity/H_1528_R1.json`

## Hypothesis (a_break_the_wall — structure family, orthogonal to operating-point family)
Every prior H_1284 lens (gain/temp/split-LR · Amoeba allosteric buffer H_1509/b/c ·
diversity H_1524 · multitimescale H_1523 · predictive H_1525 · emit-gate H_1526 — 10
lenses) modulated an OPERATING POINT (LR / SPLIT_THRESH / decode-temp / abstain-margin)
at a FIXED store size, and EVERY one was INERT — recall is decided by cell KEY-GEOMETRY
+ CAPACITY, not the per-step schedule.

The orthogonal lever: a neuromodulator that ADAPTS **CAPACITY ITSELF** — grows new cells
(neurogenesis / mitosis) when substrate collision/load is high, vs a FIXED store size
(biological: adult hippocampal neurogenesis gated by novelty/cortisol; anima §mitosis
osmotic split H_1511). CAPACITY (max_cells) is the one knob NO prior lens touched.

## Method (reuse H_1284 harness byte-for-byte; frozen-first)
Same regimes R1_STABLE / R2_DRIFT / R3_NOISE, N_FACTS=30, fact+event stream per
(seed,regime), FNV-1a byte-trigram key geometry, cap = acc − fab metric, MARGIN=0.05,
seeds tune=7 / score=[11,22,33]. Only the **capacity policy** differs; LR0/TH0 fixed at
the engine operating point (isolates CAPACITY — the new lever — from the INERT knobs).
- **A = BEST-FIXED-SIZE** — grid-tuned `max_cells` over SIZE_GRID=[3,6,9,12,18,24] on a
  disjoint tuning seed (the anti-confound: adaptive must beat the BEST FIXED SIZE).
- **C = ADAPTIVE-CAPACITY** — starts at 3, a load gate raises the cap (+1 cell) on a
  genuine collision under load (write recon-err surprise > running û AND store at cap),
  up to ceiling 24. NO LR / SPLIT change.
- **ABL = FIXED-AT-FINAL-SIZE** — fixed store at C's final grown size (isolates the
  adaptive SCHEDULE from merely ending big — the decisive anti-confound).

Frozen falsifier (pre-registered in `H_1528_FREEZE.txt` before any run): GREEN
(WALL-BROKEN) iff #WIN≥2 regimes (cap_C ≥ cap_A+MARGIN) **AND** SCHEDULE
(mean cap_C−cap_ABL ≥ MARGIN) **AND** NO_FAB **AND** NEVER_MUCH_WORSE.

## Result (🧱 WALL HOLDS — mean of 3 seeds, deterministic on rerun)
**best_fixed_size = 24, and per-regime best-fixed size = 24 for ALL three regimes.**
| regime | A_cap (best-fixed-size) | C_cap (adaptive) | ABL_cap (fixed@final) | C_final_size | C−A | C−ABL |
|---|---|---|---|---|---|---|
| R1_STABLE | 0.7722 | 0.7722 | 0.7722 | 24.0 | 0.0 | 0.0 |
| R2_DRIFT  | 0.5900 | 0.5900 | 0.5900 | 24.0 | 0.0 | 0.0 |
| R3_NOISE  | 0.5656 | 0.5656 | 0.5656 | 24.0 | 0.0 | 0.0 |

n_wins = 0 · schedule_global C−ABL = 0.0 · **verdict = WALL**.

## Why the wall holds (honest, c9)
The adaptive win requires the OPTIMAL #cells to **differ by regime** — that is the
precondition for a *modulation* knob to have anything to exploit. It does not: the best
fixed size is the GRID CEILING (24) in EVERY regime. With 30 facts and every grid size
≤24, more capacity is **monotone-beneficial**, not regime-contingent — so the load-gated
controller simply races straight to the ceiling (final_size 24.0 in all regimes), making
**C == A == ABL exactly** (C−A = 0.0, C−ABL = 0.0 everywhere). Capacity here is a monotone
resource, not a regime-dependent sweet spot, so there is nothing for an adaptive *schedule*
to modulate. The capacity family joins the 10 INERT operating-point lenses: the H_1284
no-free-lunch wall **holds against the capacity/neurogenesis family too**.

The anti-confound was decisive and behaved correctly: the size-grid-tuned fixed baseline
already saturated the ceiling, so "adaptive" had no fixed-size to beat — exactly the case
the freeze's anti-confound clause was built to catch (no trivial more-capacity win).

## Scope / honesty
DIRECTIONAL numpy mirror (host no torch; engine-native R2 on live `core/engine_cli.hexa`
VAdaptField = deferred ING). TOY 30 facts / 3 regimes / 3 seeds / deterministic readout.
SIZE_GRID + GROW_K + MARGIN + falsifier all frozen BEFORE the run (no tune-to-green). The
ceiling 24 < 30 facts means the grid never reaches over-capacity — but since the optimum
is already the ceiling, a larger ceiling only makes "bigger is better" stronger, never
creates a regime-dependent optimum; the monotone-capacity reading is robust. UNVERIFIED:
engine-transfer, scale, regimes where a SMALLER store is genuinely optimal (e.g. heavy
distractor/interference load), non-mirror mitosis dynamics.

xref H_1284 (parent wall) · H_1509/b/c · H_1523 · H_1524 · H_1525 · H_1526 (10 INERT
operating-point lenses) · H_1511 (§mitosis osmotic split) · H_1416 (ablation-INERT
precedent) · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning ·
a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p7 · p8 · c9 · c15.
