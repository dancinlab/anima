# H_1527 — 🧱 NEUROMODULATION via REPRESENTATION GEOMETRY (key-encoding), not the operating-point knob

**tier:** 🧱 WALL HOLDS (CLOSED-NEGATIVE, no free lunch — the 11th independent lens; the representation-structure family too)
**verdict source:** `state/verdicts/1527_nm_repr_geometry/H_1527.txt` (verbatim)
**wired:** N/A — DIRECTIONAL numpy mirror (HARD-GATE-1); WALL-HOLDS ⇒ nothing to wire.

## Claim
The ESCAPE attempt on the **H_1284 NEUROMODULATION wall**. 10 prior lenses ALL modulated
an **operating-point knob** (global gain / LR / split-thresh / temperature H_1284/R2/R3,
Amoeba μ_t buffer H_1509/b/c, diversity H_1524, multi-timescale H_1523, predictive H_1525,
emit-gate H_1526) and were INERT — the measured root cause is that RECALL is bounded by
**KEY-GEOMETRY / capacity**, not the LR/temp/gate SCHEDULE, so every operating-point
controller is a no-op. THE ESCAPE PRINCIPLE: a neuromodulator that adapts the **key-encoding
GEOMETRY itself** — dimensionality EXPANSION / random-projection recoding (biological:
ACh representational sharpening, Hasselmo; cerebellar granule-cell expansion, Marr/Albus/
Litwin-Kumar), substrate-gated by collision-pressure. This changes the geometry that BOUNDS
capacity, so it CAN move a capacity-bound capability where a schedule cannot — IF the bound
is key-aliasing. a-priori: 🟢 WALL-BROKEN if geometry-modulation beats best-fixed with a
decisive ablation ("the lever is REPRESENTATION not protocol"); 🧱 if the structure family
ALSO holds. Either is honest (c9).

## Harness (frozen-first reuse)
Imports the H_1284 harness VERBATIM (`state/universe-probes/h1284_neuromodulation_gain.py`:
MemStore VAdaptField mirror / gen_stream R1_STABLE·R2_DRIFT·R3_NOISE / make_facts / grid_tune
best-fixed / key_vec). SAME regimes / seeds [11,22,33] / disjoint tune-seed 7 / best-fixed
LR0*=0.1 TH0*=0.2 / MARGIN=0.05 / capability=recall_acc−fab. The ONLY change = the adaptive
arm modulates the KEY GEOMETRY (LR/TH/abstain FIXED in every arm). ARMS: **A**=best-fixed
(DIM_BASE=16 key geometry) · **G**=adaptive-GEOMETRY (collision-gated random-projection
expansion up to 4× = 64-dim granule layer + sparsifying ReLU; committed ONCE per run from a
warmup collision read) · **ABL**=fixed-expansion (G's mean factor held constant, isolates
"the ADAPTATION wins" from "a bigger fixed dim wins").

## Result — 🧱 WALL HOLDS (the geometry lever is INERT; it strictly DEGRADES)
3 seeds [11,22,33], 3 regimes, calibrated trigger thr=0.4142 (= R1_STABLE tune-seed baseline):

| regime | A_cap | G_cap | ABL_cap | G−A | G_meanfactor | G_fab vs A_fab |
|---|---|---|---|---|---|---|
| R1_STABLE | 0.5744 | 0.5744 | 0.3567 | +0.0000 | 1.00 (no expand) | 0.028 = 0.028 |
| R2_DRIFT | 0.4389 | 0.2600 | 0.2256 | **−0.1789** | 2.33 | 0.208 ≫ 0.030 |
| R3_NOISE | 0.4156 | 0.2789 | 0.2444 | **−0.1367** | 2.33 | 0.164 ≫ 0.030 |

**c1 BREAK** (G≥A+0.05 on ≥2/3): **FALSE** — 0 regimes win; G is WORSE wherever it fires.
**c2 ADAPTATION**: FALSE. **c3 NO-FAB**: FALSE — expansion ADDS fabrication. → 🧱 WALL_HOLDS.

**MULTI-VARIANT CONFIRM** (`H_1527_geometry_sweep.txt` — the strongest chance for the family:
BEST FIXED expansion of any factor, ReLU AND orthogonalized basis):

| | R1 | R2 | R3 |
|---|---|---|---|
| BASE (×1) | 0.574 | 0.439 | 0.416 |
| EXPAND ×2 (ReLU≡ORTHO) | 0.518 | 0.398 | 0.374 |
| EXPAND ×3 | 0.497 | 0.348 | 0.371 |
| EXPAND ×4 | 0.461 | 0.324 | 0.331 |

NO expansion factor, NO basis variant, EVER beats base — strictly MONOTONE degradation on
every regime. The representation-geometry family is genuinely INERT.

## Mechanism (why inert, honest c9)
The recall capacity bound is the **STORE CELL COUNT** (max_cells = round(0.6·30) = 18 cells
for 30 facts) + LRU eviction — NOT key-vector aliasing in the 16-dim byte-trigram space.
Random-projection EXPANSION cannot add cells; it only distorts the nearest-cell match (raises
recon-err scatter) → recall DROPS and fabrication RISES. The lever is neither the protocol
(10 prior lenses) NOR the key-representation geometry (this lens) — it is **STORE CAPACITY
itself**. The H_1284 wall is a CAPACITY wall, not a control wall.

## Measurement integrity (a_break_the_wall TAXONOMY, frozen-first)
Two artifacts found+fixed BEFORE reading the verdict, bars UNCHANGED: (1) a lossy mid-stream
`pinv` re-projection corrupted the store on every geometry switch (fixed: commit ONE geometry
per run via a warmup collision read — no destructive switch); (2) the trigger THR=0.55 sat
above the empirical collision scale (~0.41–0.48) so the lever never fired (fixed: calibrate
THR to the R1 tune-seed baseline so expansion GENUINELY fires in denser regimes — and it then
fires at factor 2.33 in R2/R3, and decisively LOSES). NOT tune-to-green — calibration on
disjoint tune data, the frozen bars in `H_1527_FREEZE.txt` were never moved.

## Wall classification
a_break_the_wall TAXONOMY: **(d) genuine no-free-lunch ceiling**, NOT (a) metric-artifact /
(b) confound / (c) infra — the two measurement artifacts were fixed and the lever STILL loses
across 4 expansion factors × 2 basis variants. 11th independent lens in the H_1284 depletion
(global-gain · regime-switch · Amoeba-buffer · diversity · multi-timescale · predictive ·
emit-gate · NOW representation-geometry). The wall HOLDS against the representation-structure
family too, more confidently — and the MECHANISM is now named: capacity = cell count.

## Scope (UNVERIFIED)
DIRECTIONAL numpy mirror (a_engine_native_learning HARD-GATE-1: `grep numpy` hits →
auto-DIRECTIONAL, terminal NOT permitted; WALL-HOLDS ⇒ nothing to wire, engine-native R2 on
live core/*.hexa = confirming follow-on ONLY, GREEN-only re-test, ING h1527-r2-engine-native).
live core/*.hexa UNTOUCHED. $0 CPU, p7 (exact ground truth, no LLM judge/perplexity/loss),
3 seeds, TOY 30 facts/300 events/DIM=16/3 regimes — scale/real-corpus/engine-transfer
UNVERIFIED (a_scale_honest_scope/a_toy_scale_recheck). frozen-first, NO tune-to-green, RED
reported RED (c9). p1/p2/p3/p6 (geometry reads ONLY substrate collision-pressure, NO label/
reward/persona/ethics) · p7 · p8 honored.

**The capacity lens this points to (CONVERGENCE):** a neuromodulator that adapts the STORE
CAPACITY (cell-count / eviction policy) directly — the named bottleneck — rather than the key
geometry. The sibling H_1528 (NM adaptive-capacity / neurogenesis, landed concurrently)
tested EXACTLY that lever and ALSO held the wall: with 30 facts the optimal cell count is
monotone (best fixed size = grid ceiling in every regime), so even a load-gated cell-grower
has no regime-dependent sweet spot to exploit. Two independent lenses (this representation
lens + H_1528 capacity lens) thus converge: the H_1284 wall is a MONOTONE-CAPACITY wall —
more cells always help, but no adaptive POLICY (geometry or count) beats best-fixed.

## xref
H_1284 / H_1284_R2 / H_1284_R3 (operating-point lenses) · H_1509/b/c (Amoeba buffer) ·
H_1523 (multi-timescale) · H_1524 (diversity) · H_1525 (predictive) · H_1526 (emit-gate) ·
H_1227/H_1231 (immune store key geometry) · H_1280 (cerebellar expansion lens) ·
a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning (DIRECTIONAL) ·
a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9.
