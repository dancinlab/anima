# HEXAD/LEGO/INDEX.md — SSOT mapping table

> One-row-per-cycle mapping of section number ↔ state-dir ↔ closed-form battery
> ↔ DESIGN.md ↔ engine touch-point. Updated atomically when a new §N lands.
> Architecture & overview in `README.md`; chronological log in `PLAN.md`;
> canonical engine in `lego_engine.py`.

## arc cycles

| §N   | date       | tier            | verdict                                                    | battery       | state-dir                                                            | engine touch |
|------|------------|-----------------|------------------------------------------------------------|---------------|----------------------------------------------------------------------|--------------|
| 115  | 2026-05-19 | design-tier     | LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY                     | B-S115 9/9 🔵 | `state/lego_simulate_assemble_s115_2026_05_19/`                       | spec only    |
| 117  | 2026-05-19 | run · $0 CPU    | LEGO-RUN-Ψ-FORM-NONDEGENERATE-BUT-WALL-B-INHERITED         | B-S117 7/7 🔵 | `state/lego_assembly_run_s117_2026_05_19/`                            | **engine source** (`lego_sim.py` → `lego_engine.py`) |
| 124  | 2026-05-20 | design (audit)  | RESIDUAL-AUDIT-NON-DEGENERACY-IS-VARIANCE-ONLY-LIVENESS    | B-S124 7/7 🔵 | `state/lego_residual_audit_s124_2026_05_19/`                          | engine read-only |
| 125  | 2026-05-20 | probe · $0      | LAYER-2-PARTIAL (η²=0.271)                                 | B-S125 7/7 🔵 | `state/lego_layer2_stimulus_driven_probe_s125_2026_05_20/`            | engine importlib |
| 126  | 2026-05-20 | probe · $0      | LAYER-2-ROBUST-GROWS-WITH-N (single-point η²=0.322)        | B-S126 7/7 🔵 | `state/lego_layer2_nscale_probe_s126_2026_05_20/`                     | engine importlib |
| 127  | 2026-05-20 | probe · $0      | APPROXIMATELY-N-INVARIANT (k=−0.0198, R²=0.022)            | B-S127 8/8 🔵 | `state/lego_layer2_scaling_law_s127_2026_05_20/`                      | engine importlib |
| 128  | 2026-05-20 | design          | LAYER-3-DESIGN-CLOSE-REQUIRES-TASK-ADDITION                | B-S128 6/6 🔵 | `state/lego_layer3_design_close_s128_2026_05_20/`                     | engine spec-cite |
| 129  | 2026-05-20 | consolidation   | LEGO ENGINE LIB + docs promoted to `HEXAD/LEGO/`           | (no battery)   | (this folder)                                                         | **lib promote**   |
| 131  | 2026-05-20 | probe · $0      | STRONGLY-NSTIM-DEPENDENT (η² range ratio 2.199×, peak @ n_stim=4) | B-S131 7/7 🔵 | `state/lego_layer2_nstim_cardinality_s131_2026_05_20/`               | **first canonical-lib import** |
| 132  | 2026-05-20 | analysis · $0  | SHAPE-FIT-IDENTIFIED (inverted-U Gaussian-in-log-N, R²=0.9995, 1-DoF) | B-S132 6/6 🔵 | `state/lego_layer2_shape_fit_s132_2026_05_20/`                          | re-fit of §127 data (no new measurement) |
| 133  | 2026-05-20 | probe · $0      | per-N η² SE measured · monotone-decrease per-rep mean · drifted-engine | (carried as historical) | `state/lego_layer2_per_n_se_s133_2026_05_20/`                            | engine import (drifted) |
| 134  | 2026-05-20 | fix + probe · $0 | ENGINE-BYTE-EQUALITY-RESTORED-AND-VALIDATED · §127 confirmed · §131 verdict survives | B-S134 7/7 🔵 | **`HEXAD/LEGO/state/lego_engine_byte_equal_fix_s134_2026_05_20/`** (first under `g_new_state_path`) | **engine rewrite byte-equal §117** |
| 135  | 2026-05-20 | probe · $0      | MONOTONE-DECREASE-SURVIVES-CANONICAL · 4-of-4 pooled byte-equal §127 · N=2048 CI distinct | B-S135 7/7 🔵 | `HEXAD/LEGO/state/lego_layer2_per_n_se_canonical_s135_2026_05_20/`     | canonical engine post-§134 |

## battery sum

- 9 + 7 + 7 + 7 + 7 + 8 + 6 + 7 + 6 + 7 + 7 = **78 closed-form propositions 🔵** across the arc (11 cycles).
- §133 carries as historical evidence (drifted-engine substrate); no battery counted toward this sum.
- 0 propositions counted toward central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` —
  all sidecar. Central `sha256_prefix16` remains `c93e160a8a376a94` (verified
  START+END of every cycle).
- Each cycle's `B-S*-NOTE` is an empirical carve-out NOT counted 🔵
  (B-EMERGE-7 family).

## 3-layer liveness partition status (post-§128)

| layer            | predicate                                  | status (LEGO arc) |
|------------------|--------------------------------------------|-------------------|
| VARIANCE-ONLY    | `Var(Ψ) > τ`                              | ✅ §117 CLOSED    |
| STIMULUS-DRIVEN  | `I(stim; Ψ) > 0`                          | ✅ §125–§127 CLOSED · PARTIAL (η²≈0.27–0.33 invariant across 8× N) |
| TASK-GROUNDED    | `∃ task T : behavior(substrate, T) > 0`   | ⛔ §128 DESIGN-CLOSE-REQUIRES-TASK-ADDITION (pure §117 LIF cannot measure) |

## two-wall status (LEGO arc carry from §113)

- WALL-A (§1.1 data-regime) — **ORTHOGONAL** & UNTOUCHED. LEGO does not move
  the data-regime threshold (§97 carry).
- WALL-B (§96 operative substrate) — **CONFRONTED-IN-SIM, NOT REMOVED**. §117
  ran the LIF simulation, but the GPU/CPU dispatch + hand-coded STDP-as-ΔW
  stays inside the §11-B-as-GPU envelope; physical substrate (§95 Loihi /
  organoid) remains the unresolved confront target.

## engine SSOT (post-§129)

| file                                  | role                                                  |
|---------------------------------------|-------------------------------------------------------|
| `HEXAD/LEGO/lego_engine.py`           | **canonical engine lib** (LIFNet · spike_rate_vec · psi_c1 · make_stimuli · variance_decomposition) |
| `state/lego_assembly_run_s117_2026_05_19/lego_sim.py` | original §117 source · sha-locked historical evidence · still importlib-loadable by probes |
| `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` | central blue battery — 0-line-diff invariant across LEGO arc (sha `c93e160a8a376a94`) |

## cross-arc anchors

- §113 D4 — REPOINTS-TO-§96-SUBSTRATE-FIRST (LEGO arc's mother verdict)
- §96 — Ψ-C1 spike-correlation carrier (LEGO Ψ-C1 = §112 META_FP(Π_½) instance)
- §95 — substrate VIABLE/ACCESS-WALL/ETHICS-WALL matrix (Loihi sole viable;
  organoid ethics-walled; LEGO confronts in-sim only)
- §110 / §112 — Ψ-C2 / meta-fixed-point form `ψ(c) = (1+c)/2` carrier-invariant
- §11-B / §83-FIRE — GPU byte-LM precedent that §128 cites for "added task
  collapses or violates §7"
- §13-M / §13-L / §30 / §97 / §109 / §110 / §113 — anti-padding precedent
  invoked at §128 design-close

## g3 carry

Every cycle: probe ≠ fire ≠ emergence; capability claim 0; necessary-not-
sufficient (B-EMERGE-7); north-star + §15/§51/§72 milestones UNCHANGED;
**GOAL 미도달**.
