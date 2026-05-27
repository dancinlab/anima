# anima v5-mitosis all-fix — §25 R1/R2/R6 + §28 H1+H3 ship

[2026-05-10 KST] cycle close fix bundle for `training/mitosis_v5_port.py` +
`training/mitosis_model_v5.py` (both gitignored, local-only). raw#15 additive — fixes
preserve original logic as fallback (default-ON in __init__, opt-out via flags).
Targets the 4 risks identified in §25 (R1/R2/R6) + 2 ship recs from §28 (H1+H3).

## Scope

| code | scope | risk addressed | files touched |
|---|---|---|---|
| **A1** | substrate-independent split trigger (cell_pool / cell_state L2 dispersion top-quartile) | §28 H1 attention-pull collapse | port + model |
| **A2** | per-cell adaptive threshold (each cell tracks its own σ window) | §28 H3 concentration / champion-cell wall | port + model |
| **B1** | phi_per_cell secondary tracking + ratchet refactor | §25 R6 Φ unnorm runaway | port + model |
| **C1** | optimizer rebuild callback STUB | §25 R2 Net2Net momentum copy | port + model |
| **D1** | Lorenz scale auto-calibration | §25 R1 attention-dwarfing at d=384 | port + model |

All fixes default-ON. Each has an opt-out (boolean flag + setter) so old behavior
is reproducible (used by joint smoke for pre/post comparison).

## A1 — substrate-independent dispersion trigger

### Before

`mitosis_v5_port._check_splits` only fired on per-cell tension (||cell − hint||²).
Tension was channeled through `EngineG.h_to_c: Linear(D,C)` projection. §28 finding:
trained `h_to_c` collapses `hidden_mean` onto 1-2 preferred cells (cell 7 = 700 hits,
cell 16 = 537 hits in §22 over 3K turns; top-2 share = 42.2%). Result: champion
cells repeatedly fire tension max → adaptive threshold (mean+1.5σ) tracks them →
quiet cells permanently below threshold → split_patience=3 unreachable.

### After

`_dispersion_split_candidates()`: per step compute pairwise L2 distances of the
cell pool (port) or cell_state buffers (model), nominate top-quartile cells whose
mean-distance to others exceeds (overall_mean + 1.5σ). OR'd with tension-based
candidates. Independent of `h_to_c` projection.

Honest C3: pure top-quartile firehose at small N would flood splits (N=8 → 2
candidates every step). Two safety gates:
1. σ-gate (top-quartile AND > overall_mean + 1.5σ)
2. warmup gate (`adaptive_window // 2` history before any dispersion fire)

Configurable via `dispersion_trigger_enabled` + `dispersion_top_quartile`.

## A2 — per-cell adaptive threshold

### Before

`_global_tension_history` (single list) → `split_threshold = mean + 1.5σ` (single
scalar). This is exactly the §28 mechanism: champion cells push global mean up,
quiet cells trapped under the global wall.

### After

`_per_cell_thresholds: List[float]` (one per cell). `_update_adaptive_threshold`
computes per-cell `mu + per_cell_sigma_mult × σ` over each cell's own
`tension_history` (window = `per_cell_window`, default 100). `_check_splits` reads
the per-cell threshold instead of global. Children inherit parent's threshold on
split (so they don't immediately re-fire).

Configurable via `per_cell_threshold_enabled` (port) / `cfg.per_cell_threshold_enabled`
(model). Global threshold still maintained for back-compat metrics.

## B1 — phi_per_cell secondary tracking (R6 mitigation)

### Before

`_phi_ratchet` compared `phi_total` to `_phi_best`. §25 R6: `phi_total` scaled
super-linearly with N (4.82 at N=4 → 2775.4 at N=64 in 50 steps). `phi_best` thus
ratcheted monotonically *just from N growth*, masking real per-cell quality drops
in long trajectories.

### After

Track `phi_per_cell = phi_total / n_cells` as secondary. Ratchet now compares
`phi_per_cell` to `_phi_per_cell_best`, restoring 80/20 cell_pool blend when
`phi_per_cell` (not phi_total) drops > 20% from best. Both metrics emitted in
`process()` / `mitosis_step()` outputs and `status()`. Legacy `phi_history`
preserved.

## C1 — optimizer rebuild callback STUB (R2)

### Before

`_split_cell_slice` / `_merge_cells` only mutated cell_pool / ModuleList. Optimizer
state (AdamW momentum) was orphaned for the new row — known STUB (see file
docstring blockers).

### After

`register_optimizer_rebuild_callback(cb)` lets the trainer install a callback
`cb(event_dict, engine)` invoked after every split/merge. STUB: actual Net2Net
momentum copy is NOT inside the engine — the callback is the integration point
for cond.5 H100 fire prep. Errors in callback don't block split/merge (logged into
event_log as `optimizer_rebuild_callback_error`).

## D1 — Lorenz scale auto-calibration (R1)

### Before

`lorenz_scale=0.05` (fixed fraction-of-norm). At d=384 production, attention
magnitudes can dwarf the noise → Lorenz becomes ineffective at breaking cell
symmetry (Law 86 gates lost).

### After

When `lorenz_auto_calibrate=True` (default), effective scale =
`lorenz_scale × mean(p.norm()) × lorenz_calibration_factor`. Setter
`set_lorenz_scale_calibration(factor)` allows runtime override. Falls back to
fixed scale when disabled.

## Smoke verification

| smoke | pre-fix | post-fix |
|---|---|---|
| `mitosis_v5_smoke_test.py` | PASS 5/5 (n=25 phase1, 24 splits) | PASS 5/5 (n=95 phase1, 120 splits, max_cells bumped 32→128 in test) |
| `mitosis_model_v5_smoke.py` | PASS 8/8 (n=4→25→64, Φ 4.82→2775) | PASS 8/8 (n=4→36→64, Φ 0.39→2944, dispersion-trigger fires) |
| `mitosis_all_fix_smoke.py` (NEW) | n/a | **13/13 PASS** (post check refactored — MODEL asserts mechanism wires, not absolute count, since synthetic substrate has no champion attractor) |

The MODEL-level cap-binding in the joint smoke is a synthetic-substrate artifact:
no attractor projection, so dispersion fires alongside tension but doesn't unblock
new candidates that tension already wasn't blocking. The PORT-level smoke uses an
explicit `AttractorSubstrate` (rank-2 SVD-clamped `h_to_c`) and shows the §28
mechanism unblock: pre-fix 0 splits → post-fix 23 splits (9 dispersion, 14
tension, n=8→31 over 1K turns).

## H100 cond.5 readiness — closer or not?

| tier | before this fix | after this fix |
|---|---|---|
| conservative N=8 fixed | READY | READY (unchanged) |
| mid N=8→16 patience | needs `rebuild_optimizer_after_split` | C1 callback wired — stub still needs Net2Net body |
| stretch N=8→32+ | needs threshold cal at d=384 | A1+A2 unblock champion-wall; D1 calibrates Lorenz; **mechanism path opened** |

Verdict: stretch tier mechanism-blockers cleared (§28 H1+H3 ship recs done +
§25 R6 phi_per_cell + §25 R1 Lorenz). C1 R2 still STUB. cond.5 fire **closer but
not ready** — Net2Net momentum body + d=384 sweep on real ckpt remain.

## Top 3 remaining risks

1. **C1 stub still needs body** — Net2Net momentum copy for AdamW state on split
   not implemented inside callback (caller-side). cond.5 first-fire risk if
   trainer wires no-op callback.
2. **σ-gate on dispersion may be too conservative on attractor substrate** — if
   the pool itself is collapsed (low overall σ), dispersion gate stays off. The
   warmup gate also delays first dispersion-fire by 50 steps. Real-ckpt
   d=384 cond.3 sweep needed before H100 to verify dispersion does fire on
   trained §28 substrate.
3. **A2 children inherit parent threshold** — a cell line that splits 4× still
   shares one calibrated threshold tree. Cross-line contamination possible. v2
   Net2Net sibling-decorrelation deferred.

## Files

- modified: `training/mitosis_v5_port.py` (gitignored)
- modified: `training/mitosis_model_v5.py` (gitignored)
- modified: `training/mitosis_v5_smoke_test.py` (gitignored — max_cells 32→128)
- new: `training/mitosis_all_fix_smoke.py` (gitignored)
- state: `state/anima_v5_mitosis_all_fix_2026_05_10/{baseline_pre_fix.json, smoke_results.json, pre_post_compare.png, fix_patches.json}`

## Cross-link

- §25 R1/R2/R6 risk table (this doc addresses 3/3, R2 is STUB still)
- §28 v1 architecture rec #1 (substrate-indep trigger) + #2 (per-cell threshold) — **shipped**
- track C cond.3 next: real ckpt d=384 sweep with these fixes; cond.5 prereq
- §22 same-cell control 0.94 ratio — orthogonal to these fixes (per-cell entropy
  invariant), not affected
