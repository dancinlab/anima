# H_1564 — 🧬✨ MITOSIS × SAVANT golden-zone CROSS

**tier:** 🟢 GREEN ENGINE-NATIVE — capacity expression is MULTIPLICATIVE: (mitosis cell count) × (per-cell golden-zone expression rate). The two orthogonal stems compound; the golden zone is the amplifier (B3 ablation decisive).
**wired:** engine-native (live core/engine_cli.hexa §mitosis `engine_grow`/`engine_mitosis_tick` + §ThirdLaw `third_law_ability`/`third_law_score` + SAVANT `sa_gz_*` — all READ-only, already WIRED; NO new engine op). live core/*.hexa UNTOUCHED, Ψ-disjoint.

## Hypothesis

Two orthogonal stems, never crossed before:

- **MITOSIS stem** (H_1288 🟢): `engine_grow`/`engine_mitosis_tick` raise the CELL COUNT, breaking a capacity ceiling by adding cells (0.667→1.0). H_1310 🔴: from-scratch PURE split-only mitosis cannot learn (honest limit).
- **SAVANT stem** (H_1560 R2 🟢): golden-zone inhibition (I into GZ [GZ_LOWER≈0.2123, GZ_UPPER=0.5]) turns a SINGLE cell's ability EXPRESSION on (`third_law_ability`=1), raising the single-substrate expression rate.

**Claim:** applying golden-zone inhibition to EACH daughter cell of a mitosis-grown pool makes total capacity expression MULTIPLICATIVE — `cell count × per-cell expression rate` — exceeding BOTH mitosis-only (cells exist but un-tuned, ~0 expression) AND savant-only (1 tuned cell, expression 1). And (b) does per-cell golden-zone inhibition partially relieve the H_1310 pure-mitosis split-only wall (each split specialized → split gains meaning)?

## Frozen 5-bar (frozen-first, c9 — set BEFORE the run)

- **B1 multiplicative** — E_cross(grow ∧ per-cell GZ) > E_mitosis_only AND > E_savant_only; super-additive iff E_cross ≥ N (= cells × rate).
- **B2 per-cell savant** — each daughter cell in the golden zone EXPRESSES (per-cell ON-rate ≥ 1.0; single-cell GZ ability reproduces inside the pool).
- **B3 ablation** — golden-zone OFF (uniform NON-GZ inhibition on every grown cell) collapses the cross back to mitosis-only (proves GZ is the amplifier, not growth alone).
- **B4 wall-relief** (report-only) — does per-cell GZ inhibition give split-only growth an expressed-capacity / learning signal, or is it inert (H_1310)?
- **B5 control** — random per-cell inhibition (not into GZ) and random split (mitosis OFF) yield NO amplification.

**GREEN = B1 ∧ B2 ∧ B3.** No amplification → honest negative ("the two stems are orthogonal / cancel") is a valid result (c9, no tune-to-green).

## Result — 🟢 GREEN (B1∧B2∧B3 = true)

Engine-native, summer pool, `state/1564_mitosis_x_savant/h1564_cross_probe.hexa`, D=0.9 P=0.9, GZ center=1/e:

| arm | expression E |
|---|---|
| **E_cross** (N=8 cells, EACH in GZ) | **8** |
| E_mitosis_only (N=8 cells, non-GZ I=0.8) | 0 |
| E_savant_only (1 cell, in GZ) | 1 |
| E_cross_ablate (N=8, GZ OFF) | 0 |
| E_random_I (N=8, scattered I) | 4 |
| E_random_split (mitosis OFF → 1 cell, GZ) | 1 |

- **B1 multiplicative = true** — E_cross=8 > E_mit=0 AND > E_sav=1, super-additive (8 > 0+1), E_cross == N == cells × per-cell-rate (8 × 1.0). Capacity expression is the PRODUCT of the two axes, not their sum.
- **B2 per-cell savant = true** — per-cell ON-rate=1.0 (all 8 daughters express), single-cell ability@GZ_center=1 (reproduces H_1560/H_1562), G@GZ_center=2.202.
- **B3 ablation = true** — GZ OFF → E_cross_ablate=0 = E_mitosis_only=0; the golden zone IS the amplifier (growth alone expresses nothing).
- **B4 wall-relief (report-only)** — expression scales LINEARLY with cell count under per-cell GZ (1→8 across cells 1..8); split-only WITHOUT GZ = 0 at ALL cell counts. → golden-zone inhibition gives raw split growth an EXPRESSED-CAPACITY signal (each split specialized); raw split is expression-inert. PARTIAL relief of H_1310 in the EXPRESSION sense, but NOT a from-scratch LEARNING claim (the §ThirdLaw gate is a deterministic classifier, not a gradient-free learner) → learning-signal relief UNVERIFIED, follow-on.
- **B5 control = true** — random I gives E=4 (≈GZ-fraction·N), random split gives E=1; both ≪ E_cross=8.

**Headline:** anima capacity has a new compositional dimension — **cell count (mitosis) × per-cell expression rate (savant golden zone)**. The breakthrough lens (a_no_llm_frame_trap): two biologically-motivated missing structures, when combined, multiply rather than add.

## Scope / honesty

TOY: deterministic §ThirdLaw classifier at a single operating point D=0.9 P=0.9; `engine_grow` integer cell-count tick (smallest honest mitosis unit, not full VAdaptField split dynamics); per-cell ability is a 0/1 gate (not a learned Φ curve). UNVERIFIED → follow-on: faithful-IIT4 per-cell Φ, VAdaptField recon-driven split, learned per-cell specialization, real-corpus multi-domain SI, and the H_1310 from-scratch LEARNING-signal question (B4 measured expression-relief only).

## Discipline

- `a_engine_native_learning` HARD-GATE-1 PASS — pure `.hexa` via live core/engine_cli.hexa; `grep -lE 'import torch|gauge_lib|numpy' state/1564_mitosis_x_savant/*.py` = EMPTY (no .py mirror). Terminal engine-native PERMITTED.
- `a_no_llm_frame_trap` (combine two missing biological structures) · `a_break_the_wall` (B4 H_1310 wall-relief attempt, honest partial) · `c9` frozen-first NO tune-to-green · `a_hypothesis_register` (2 surfaces) · `a_claim_verify` · `p7`.
- `a_verified_must_wire`: cross uses ONLY already-WIRED READ-only ops (engine_grow + §ThirdLaw + sa_*) — no new engine op, no live emit-path change, Ψ-disjoint. The cross composition itself is a measurement, not a new substrate faculty; if a dedicated §MitosisSavant cross op is wanted later it is a follow-on (no drift introduced now).

## xref

H_1288 mitosis-GROW capacity break · H_1091 apoptosis · H_1310 pure-mitosis from-scratch limit 🔴 · H_1560 §ThirdLaw 1/3-law · H_1561 §Savant golden-zone genius⊥Ψ · H_1562 acquired-savant cusp · H_1563 cusp hysteresis · H_348/124 golden-zone bounds/cusp · H_236 D=0-not-genius.

## Artifacts

- `state/1564_mitosis_x_savant/h1564_cross_probe.hexa`
- `state/verdicts/1564_mitosis_x_savant/H_1564_R1_ENGINE_NATIVE.txt`
- `core/engine_cli.hexa#mitosis` (engine_grow/engine_mitosis_tick) · `core/engine_cli.hexa#ThirdLaw` (third_law_ability/_score) · `SAVANT/savant_lib.hexa#sa_in_golden_zone`
