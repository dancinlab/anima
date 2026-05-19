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

## battery sum

- 9 + 7 + 7 + 7 + 7 + 8 + 6 = **51 closed-form propositions 🔵** across the arc.
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
