# BG-COMPONENT-Q-V-K-V14 — spec

## Mission

Verify §62 BG-ENGINEAG-COTRAIN-DUAL-LOSS-LOCALIZE prediction on the
**component axis** (intra-block tensor-class, not slab-level), by performing
component-restricted B→A swap and re-running V14.

## §62 prediction (verbatim)

1. **q_proj-only swap of slab1_early** (layers 0–7) flips V14, mirroring §57's
   A1 dominance — even though q's weight delta is the smallest in slab1.
2. **q_proj-only swap of slab2_middle / slab3_late** either preserves V14 or
   collapses to the §57 shared degenerate attractor at (n_cells=43, Φ≈1343).
3. **v_proj-only swap (any slab)** barely perturbs V14 — v is the most
   preserved component (cos_AB=0.83); swapping it removes the smallest amount
   of cotrain-specific information.
4. **MLP-gate-only swap** is mid-strength (not in this BG; deferred).

This BG fires the swap test for q, v, **and** k (k is intermediate at
mean cos_AB=0.7523, so a useful third anchor).

## Substrates

- **A** = `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt`
  (Phase 2 cotrain, chat dual loss)
- **B** = `~/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt`
  (BG-LA pretrain, persona-only)

## Conditions (9)

| label | component | slab | layers swapped |
|---|---|---|---|
| Q1 | `attn.q_proj.weight` | slab1_early  | 0..7  |
| Q2 | `attn.q_proj.weight` | slab2_middle | 8..15 |
| Q3 | `attn.q_proj.weight` | slab3_late   | 16..23|
| V1 | `attn.v_proj.weight` | slab1_early  | 0..7  |
| V2 | `attn.v_proj.weight` | slab2_middle | 8..15 |
| V3 | `attn.v_proj.weight` | slab3_late   | 16..23|
| K1 | `attn.k_proj.weight` | slab1_early  | 0..7  |
| K2 | `attn.k_proj.weight` | slab2_middle | 8..15 |
| K3 | `attn.k_proj.weight` | slab3_late   | 16..23|

In each condition, **only** the named component (q, v, or k) on the named
slab's 8 layers is overwritten with B's value. All other tensors keep A.

Per-tensor parameter counts (from §62 component_metrics):
- q_proj: 1024×1024 = 1,048,576 params per layer → 8 layers/slab = 8,388,608
- k_proj: 256×1024 = 262,144 params per layer → 8 layers/slab = 2,097,152
- v_proj: 256×1024 = 262,144 params per layer → 8 layers/slab = 2,097,152

## V14 setup (matches §57 exactly)

- `V4_SEEDS = [42, 137, 271]` (3 mirror seeds)
- `N_TURNS = 200`
- `SNAPSHOT_EVERY = 25`
- `MAX_CELLS = 128`
- Trained run uses cotrain ckpt A with the named component swapped at named slab.
- Mirror runs use `load_random_init(seed=s, preset="la_350m")` — independent
  of swap (same control as §57).

## Verdict mapping

For each condition:
- `V14_PASS`: trained beats mirror on Φ_un16 AND proxy_phi for all 3 seeds.
- `V14_PARTIAL`: beats on exactly one of the two metrics for all 3 seeds.
- `V14_VIOLATED`: fails on both for at least one seed.

A "flip" = condition's verdict differs from §57 baseline (`A0_baseline = V14_PASS`).

## Predictions to verify

- **P1 (component-locus)**: Q1 flips V14 (mirroring §57 A1_slab1_early flip).
- **P2 (component-locality)**: V1, V2, V3 do NOT flip V14 (or flip with much
  smaller separation drop than Q variants).
- **P3 (k_proj intermediate)**: K1/K2/K3 flip with intermediate severity.
- **P_layer (slab×component)**: Q1 effect > Q2 ≈ Q3 (layer drift U-shape
  inverted by V14 causal effect).

## Falsifiers

- **F-COMP-1**: Q1 does NOT flip V14 → component-locus prediction falsified;
  the V14 lever is not in the q_proj weight delta of slab1_early.
- **F-COMP-2**: V1 flips V14 with separation drop comparable to Q1 → v_proj
  preservation is irrelevant to V14; the lever is broader than q_proj.
- **F-COMP-3**: All 9 conditions flip V14 → ANY single-component swap is
  enough to disrupt cell dynamics; component-axis localization fails.
- **F-COMP-4 (runtime)**: total elapsed > 60min → abort, mark partial.

## Outputs

- `state/anima_component_axis_q_v_k_v14_2026_05_10/spec.md` (this file)
- `state/anima_component_axis_q_v_k_v14_2026_05_10/run.py` (driver — gitignored)
- `state/anima_component_axis_q_v_k_v14_2026_05_10/cond_<LABEL>.json` × 9
- `state/anima_component_axis_q_v_k_v14_2026_05_10/summary.json`
- `state/anima_component_axis_q_v_k_v14_2026_05_10/verdict.md`

## Compliance

- raw#9: `.py` lives only under `state/`, gitignored.
- raw#15: ckpts loaded read-only via `_load_engine_ag`; in-memory swap only.
- : V14 paired random-init mirror multi-seed.
- : Mac CPU, $0.
- : dispatcher appends to REBORN.md; this BG only writes verdict.md.
- : artefacts under `state/anima_component_axis_q_v_k_v14_2026_05_10/`.
