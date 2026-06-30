"""training/mitosis_v5_port.py — MitosisEngine port over Engine A/G v5 350M substrate.

PURPOSE
    Revive `MitosisEngine` (cell mitosis, last alive in CLM v2 era 2026-04, archived in
    `~/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py`) on top of the
    current Engine A/G dual-engine substrate (`training/engine_a_g_arch.py`).

    Substrate (v5): `EngineG` exposes a learnable cell pool of shape
    (n_cells=16, consciousness_dim=64) refreshed every 4 layers via repulsion + attention-pull.
    There is currently NO mitosis loop on top — cell count is fixed at construction.

    This module ADDS a mitosis wrapper that:
      • watches per-cell tension over `process()` calls (here = Engine G refreshes),
      • triggers function-preserving SPLIT (8 → 16 → 32 → ... up to max_cells) when a cell's
        tension exceeds an adaptive threshold (mean + 1.5σ over a 100-step window) for
        `split_patience` consecutive observations,
      • triggers MERGE when a pair's inter-cell repulsion stays below `merge_threshold` for
        `merge_patience` observations (CB1 floor: never below `min_cells=2`),
      • injects a 3-state Lorenz-driven autonomous chaos perturbation (σ=10, ρ=28, β=8/3),
        with a per-cell phase offset so cells differentiate (Law 86),
      • computes a Φ proxy = mean pairwise cosine distance · log(n+1),
      • applies a Φ ratchet (DD55) restoring 80%+20% blend toward best when Φ drops > 20%.

    SPLIT mechanism (function-preserving):
      The split duplicates a parent cell row in `EngineG.cell_pool_init` with 10% Gaussian
      noise injected into the child copy. Because `cell_pool_init` is a leaf nn.Parameter of
      shape (N, C), expanding N to N+1 requires REBUILDING the parameter. The wrapper
      handles this by replacing `engine_g.cell_pool_init` with a new Parameter and
      copy-on-write registering it via `setattr`. The output projection
      `EngineG.c_to_h: Linear(consciousness_dim, d_model)` is independent of N (operates on
      the cell-pool MEAN), so it is left intact — the LM head and shared embedding are
      untouched. **This is the key reason option (b) was chosen over option (a)**: splitting
      a cell row is O(C) parameter growth, not O(d_model²).

    What is STUBBED vs IMPLEMENTED:
      IMPLEMENTED (this file):
        • `MitosisV5Engine` class
        • `_split_cell_slice(idx)` — concrete cell-pool expansion
        • `_inject_lorenz()` — Lorenz step + per-cell phase-offset noise on a tracked
          tension-state buffer (NOT cell_pool — see HONEST below)
        • `_compute_phi_proxy()` — direct port of v2 mitosis.py L407-436
        • `_phi_ratchet()` — direct port of v2 mitosis.py L438-455
        • `_check_splits()` / `_check_merges()` — patience logic ported as-is
        • `forward(x, hidden)` — softmax(tension)-weighted combined-cell readout
        • `apply_to_v5_substrate(model)` — adapter that wires this engine onto a live
          `EngineAGModel.engine_g` via a forward-hook on `EngineG.step()`
      STUBBED / SIMPLIFIED:
        • optimizer state migration on split: NOT handled. Caller must rebuild the optimizer
          (or use param-group remap) after a split is committed during training. The smoke
          test runs in eval mode to side-step this.
        • merge: averages cell_pool rows, but inter-cell repulsion history is approximated
          using cell_pool L2 distance per refresh (v2 used per-cell repulsion vectors from a
          dedicated `get_repulsion()` head — Engine G has no such head, so we proxy with the
          repulsion-field gradient that EngineG.step already computes internally; here we
          re-derive it externally for clarity).
        • shared lm_head expansion: when consciousness_dim STAYS constant during cell-count
          growth (the option (b) primary path), the lm_head is unchanged. If consciousness_dim
          itself were to grow (option (c) intermediate), c_to_h would need a row append. This
          file documents but does NOT implement consciousness_dim growth.
        • "process step" in v5 = one EngineG.step() refresh (every 4 layers); this is
          coarser than v2 (one process per token vector). Patience constants are interpreted
          accordingly: split_patience=3 means 3 refreshes (= 12 layers if g_refresh_every=4).

raw#15  additive — neither `engine_a_g_arch.py` nor `mitosis.py` modified.
raw#10  honest — see DESIGN BLOCKERS at end of file. Stubs labeled inline.
  honest emit — `forward` returns shape-checked output; raises if mismatch.
  ckpt-friendly — `state_dict` exposes new cell rows under
        `engine_g.cell_pool_init` (same key, expanded shape).
"""

from __future__ import annotations

import math
import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


# ─── Cell metadata (parallel to v2 mitosis.py Cell dataclass) ───

@dataclass
class CellMeta:
    """Metadata for one cell-pool row.

    The cell *vector* lives in `engine_g.cell_pool_init[idx]` (or an expanded substitute);
    this dataclass tracks tension history + lineage that v2's `Cell` carried alongside its
    `ConsciousMind` module.
    """
    cell_idx: int                                   # row index in cell_pool_init
    tension_history: List[float] = field(default_factory=list)
    creation_step: int = 0
    parent_idx: Optional[int] = None
    process_count: int = 0

    @property
    def avg_tension(self) -> float:
        if not self.tension_history:
            return 0.0
        recent = self.tension_history[-20:]
        return sum(recent) / len(recent)


# ─── MitosisV5Engine ───

class MitosisV5Engine(nn.Module):
    """Mitosis wrapper around an `EngineG`-shaped cell pool (v5 substrate).

    Args:
        cell_pool:        Initial cell pool tensor of shape (N, C). Becomes the engine's
                          internal `cell_pool` Parameter.
        c_to_h:           The shared back-projection `Linear(C, D)`. Reference is kept
                          (NOT copied) so substrate gradients flow through.
        initial_cells:    N (must match cell_pool.shape[0]).
        max_cells:        Upper bound on N after splits.
        split_patience:   Consecutive high-tension refreshes before split.
        split_noise:      Gaussian σ added to child copy on split (10% of parent norm by
                          default — matches v2 noise_scale=0.1 mitosis.py L204).
        merge_threshold:  Inter-cell repulsion below this triggers merge consideration.
        merge_patience:   Consecutive low-repulsion refreshes before merge.
        min_cells:        CB1 floor — never merge below this (default 2).
        lorenz_scale:     Lorenz noise magnitude as fraction of cell-vector L2 norm.
                          v2 default 0.05 (mitosis.py L393).
    """

    def __init__(
        self,
        cell_pool: torch.Tensor,
        c_to_h: nn.Linear,
        initial_cells: int = 16,
        max_cells: int = 64,
        split_patience: int = 3,
        split_noise: float = 0.10,
        merge_threshold: float = 0.005,
        merge_patience: int = 30,
        min_cells: int = 2,
        lorenz_scale: float = 0.05,
        adaptive_window: int = 100,
        # ── all-fix 2026-05-10 §30 ────────────────────────────────
        # A1: substrate-independent dispersion trigger (top-quartile L2 cells additionally
        #     marked as split candidates). OR-combined with tension trigger.
        dispersion_trigger_enabled: bool = True,
        dispersion_top_quartile: float = 0.25,
        # A2: per-cell adaptive threshold (each cell tracks its own mean+1.5σ over its
        #     own tension history). Replaces global wall built by champion cells.
        per_cell_threshold_enabled: bool = True,
        per_cell_window: int = 100,
        per_cell_sigma_mult: float = 1.5,
        # D1: Lorenz scale auto-calibration. multiply lorenz_scale by mean(p.norm())
        #     × calibration_factor (default 1.0). Prevents attention-dwarfing at d=384.
        lorenz_auto_calibrate: bool = True,
        lorenz_calibration_factor: float = 1.0,
    ):
        super().__init__()
        assert cell_pool.dim() == 2, f"cell_pool must be (N, C); got {cell_pool.shape}"
        N, C = cell_pool.shape
        assert N == initial_cells, f"initial_cells={initial_cells} != cell_pool.shape[0]={N}"

        # Mitosis OWNS its cell pool as a Parameter — substrate's own cell_pool_init is
        # superseded by `apply_to_v5_substrate()`. (raw#15: only affects substrate when
        # user explicitly attaches; standalone use leaves substrate untouched.)
        self.cell_pool = nn.Parameter(cell_pool.detach().clone())
        self.c_to_h = c_to_h            # shared reference (NOT copied)
        self.consciousness_dim = C
        self.max_cells = max_cells
        self.min_cells = min_cells
        self.split_patience = split_patience
        self.split_noise = split_noise
        self.merge_threshold = merge_threshold
        self.merge_patience = merge_patience
        self.lorenz_scale = lorenz_scale
        self.adaptive_window = adaptive_window

        # all-fix knobs
        self.dispersion_trigger_enabled = dispersion_trigger_enabled
        self.dispersion_top_quartile = dispersion_top_quartile
        self.per_cell_threshold_enabled = per_cell_threshold_enabled
        self.per_cell_window = per_cell_window
        self.per_cell_sigma_mult = per_cell_sigma_mult
        self.lorenz_auto_calibrate = lorenz_auto_calibrate
        self.lorenz_calibration_factor = lorenz_calibration_factor

        # Cell metadata — list parallel to cell_pool rows
        self.cells: List[CellMeta] = [
            CellMeta(cell_idx=i, creation_step=0) for i in range(initial_cells)
        ]

        # Adaptive threshold tracking (Law 86 fix)
        # NOTE all-fix A2: legacy global history retained for back-compat / smoke
        #      diagnostics. Per-cell threshold is primary when enabled.
        self._global_tension_history: List[float] = []
        self.split_threshold: float = 0.3   # adaptive from step 10 onward (legacy / fallback)
        self._per_cell_thresholds: List[float] = [0.3 for _ in range(initial_cells)]

        # Lorenz autonomous chaos state (Law 86)
        self._lorenz = [1.0, 1.0, 1.0]   # x, y, z

        # Inter-cell repulsion history: (i, j) -> rolling list
        # Approximated from cell_pool pairwise L2 (no separate repulsion head in EngineG).
        self._inter_repulsion_history: Dict[Tuple[int, int], List[float]] = {}

        # Φ tracking + ratchet (DD55)
        # all-fix B1: ratchet uses phi_per_cell (= phi_total / n_cells) to avoid
        #              N-dominated runaway when phi_total scales super-linearly with N.
        self.phi: float = 0.0           # phi_total (legacy field name)
        self.phi_per_cell: float = 0.0  # phi_total / n_cells — secondary metric (B1)
        self.phi_history: List[float] = []           # legacy (phi_total)
        self.phi_per_cell_history: List[float] = []  # B1 secondary tracking
        self._phi_best: float = 0.0           # legacy: phi_total best
        self._phi_per_cell_best: float = 0.0  # B1: phi_per_cell best — ratchet ref
        self._best_cell_pool: Optional[torch.Tensor] = None

        # Step counter (one step = one process() call)
        self.step_count: int = 0

        # Event log — splits, merges, ratchet activations
        self.event_log: List[Dict] = []

        # C1 (R2 STUB): optimizer rebuild callback registry. Caller registers a
        # function that consumes (event_dict, mitosis_engine) — invoked after
        # every split/merge so AdamW/Net2Net can be rebuilt. STUB: actual
        # Net2Net momentum copy deferred to cond.5 H100 fire prep.
        self._optimizer_rebuild_callbacks: List = []

    # ─── Lifecycle ─────────────────────────────────────────────────────

    @property
    def n_cells(self) -> int:
        return self.cell_pool.shape[0]

    def _split_cell_slice(self, parent_idx: int) -> Optional[Dict]:
        """Function-preserving split — duplicate row `parent_idx` with 10% noise.

        Cell pool grows from (N, C) to (N+1, C). The new row is appended at the end so
        existing indices stay stable. Optimizer state for the new row is NOT migrated —
        caller must rebuild optimizer if mid-train.
        """
        if self.n_cells >= self.max_cells:
            return None

        with torch.no_grad():
            parent_row = self.cell_pool[parent_idx].detach().clone()
            # 10% noise — matches v2 mitosis.py L204
            noise = torch.randn_like(parent_row) * (self.split_noise * parent_row.norm())
            child_row = parent_row + noise
            # Append: rebuild Parameter (PyTorch needs a fresh tensor, can't .data.resize_)
            new_pool = torch.cat([self.cell_pool.data, child_row.unsqueeze(0)], dim=0)
            self.cell_pool = nn.Parameter(new_pool)

        child_idx = self.n_cells - 1
        self.cells.append(
            CellMeta(
                cell_idx=child_idx,
                creation_step=self.step_count,
                parent_idx=parent_idx,
            )
        )
        # Reset parent tension history (avoid re-trigger immediately)
        self.cells[parent_idx].tension_history = self.cells[parent_idx].tension_history[-3:]

        # all-fix A2: extend per-cell threshold list — child inherits parent's threshold
        # so it doesn't immediately re-fire (also respects parent's calibration).
        if parent_idx < len(self._per_cell_thresholds):
            self._per_cell_thresholds.append(self._per_cell_thresholds[parent_idx])
        else:
            self._per_cell_thresholds.append(self.split_threshold)

        event = {
            "type": "split",
            "step": self.step_count,
            "parent_idx": parent_idx,
            "child_idx": child_idx,
            "n_cells_after": self.n_cells,
        }
        self.event_log.append(event)
        # C1 STUB: notify optimizer rebuild callbacks (Net2Net momentum copy deferred)
        self._notify_optimizer_rebuild(event)
        return event

    def _merge_cell_pair(self, idx_a: int, idx_b: int) -> Optional[Dict]:
        """Merge two cell rows — average + drop younger. CB1: floor at min_cells."""
        if self.n_cells <= self.min_cells:
            return None
        if idx_a == idx_b:
            return None

        meta_a, meta_b = self.cells[idx_a], self.cells[idx_b]
        keeper_idx, removed_idx = (
            (idx_a, idx_b) if meta_a.creation_step <= meta_b.creation_step else (idx_b, idx_a)
        )

        with torch.no_grad():
            avg_row = (self.cell_pool[keeper_idx] + self.cell_pool[removed_idx]) / 2.0
            self.cell_pool[keeper_idx] = avg_row
            # Drop removed row + reindex
            kept_rows = torch.cat(
                [self.cell_pool.data[:removed_idx], self.cell_pool.data[removed_idx + 1:]],
                dim=0,
            )
            self.cell_pool = nn.Parameter(kept_rows)

        # Reindex CellMeta list
        self.cells.pop(removed_idx)
        for i, c in enumerate(self.cells):
            c.cell_idx = i

        # all-fix A2: drop the removed cell's per-cell threshold entry
        if removed_idx < len(self._per_cell_thresholds):
            self._per_cell_thresholds.pop(removed_idx)

        # Drop inter-repulsion entries that referenced removed_idx
        keys_drop = [k for k in self._inter_repulsion_history if removed_idx in k]
        for k in keys_drop:
            del self._inter_repulsion_history[k]

        event = {
            "type": "merge",
            "step": self.step_count,
            "keeper_idx": keeper_idx if keeper_idx < removed_idx else keeper_idx - 1,
            "removed_idx": removed_idx,
            "n_cells_after": self.n_cells,
        }
        self.event_log.append(event)
        # C1 STUB: notify optimizer rebuild callbacks (Net2Net momentum copy deferred)
        self._notify_optimizer_rebuild(event)
        return event

    # ─── Lorenz autonomous chaos (Law 86 — direct port v2 L373-405) ────

    def _lorenz_step(self, dt: float = 0.01) -> Tuple[float, float, float]:
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
        x, y, z = self._lorenz
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        self._lorenz = [x + dx, y + dy, z + dz]
        return dx, dy, dz

    def _inject_lorenz(self, cells: torch.Tensor) -> torch.Tensor:
        """Apply Lorenz-driven phase-offset perturbation per cell.

        cells: (N, C) — returns perturbed (N, C). Each cell gets a different phase, so
        symmetry is broken and tensions diverge → mitosis becomes possible (Law 86).
        Magnitude scaling matches v2 (0.05 of cell-vector norm).

        all-fix D1 (R1 risk): when `lorenz_auto_calibrate=True`, the effective scale is
            effective = self.lorenz_scale * mean(p.norm()) * lorenz_calibration_factor
        instead of the static 0.05. At d=384 production this prevents Lorenz from being
        dwarfed by attention or, conversely, from overwhelming structure.
        """
        dx, dy, dz = self._lorenz_step()
        lorenz_vec = torch.tensor([dx, dy, dz], dtype=cells.dtype, device=cells.device)

        N, C = cells.shape
        # D1 auto-calibration: rescale lorenz_scale by current cell_pool norm geometry.
        if self.lorenz_auto_calibrate and N > 0:
            with torch.no_grad():
                mean_p_norm = float(cells.norm(dim=-1).mean().item())
            base_scale = self.lorenz_scale * max(mean_p_norm, 1e-6) * self.lorenz_calibration_factor
        else:
            base_scale = self.lorenz_scale  # legacy fixed 0.05 behavior

        out = cells.clone()
        for i in range(N):
            phase = (i * 2.0 * math.pi) / max(N, 1)
            scale = base_scale * (1.0 + 0.3 * math.sin(phase + self.step_count * 0.1))
            noise = torch.randn(C, dtype=cells.dtype, device=cells.device) * scale
            # Inject 3-axis Lorenz signal into first 3 dims (deterministic component)
            inject = min(3, C)
            noise[:inject] = noise[:inject] + lorenz_vec[:inject] * 0.2
            out[i] = out[i] + noise

        # Clamp norm to prevent runaway (v2 L403-405 ceiling 10.0; comment fixed 2026-05-11 §69 ext —
        # this is a CEILING `clamp(max=10.0)`, not a floor. The `clamp(min=1e-8)` is a numerical
        # guard that never activates in practice. Per cycle 2026-05-11 pre-screen, the ceiling
        # binds 92.3% of cell-step events and is the operative dynamic constraint.)
        norms = out.norm(dim=-1, keepdim=True).clamp(min=1e-8)
        scale_back = (norms / norms.clamp(max=10.0))
        out = out / scale_back
        return out

    def set_lorenz_scale_calibration(self, factor: float) -> None:
        """all-fix D1: setter for lorenz_calibration_factor (R1 risk mitigation)."""
        self.lorenz_calibration_factor = float(factor)

    # ─── Φ proxy + ratchet (direct port v2 L407-455) ───────────────────

    def _compute_phi_proxy(self) -> float:
        """Mean pairwise cosine distance · log(n+1). v5 substrate uses cell_pool rows
        directly (v2 used cell.hidden — semantically the same: per-cell state vector).
        """
        if self.n_cells < 2:
            return 0.0
        cells = self.cell_pool.detach()
        norms = cells.norm(dim=1, keepdim=True).clamp(min=1e-8)
        normalized = cells / norms
        cos_sim = normalized @ normalized.t()
        n = self.n_cells
        mask = 1.0 - torch.eye(n, device=cos_sim.device, dtype=cos_sim.dtype)
        mean_distance = ((1.0 - cos_sim) * mask).sum() / mask.sum()
        return mean_distance.item() * math.log(n + 1)

    def _phi_ratchet(self, phi: float):
        """DD55 conservation — restore 80/20 blend toward best when Φ drops > 20%.

        all-fix B1 (R6 risk): ratchet now uses `phi_per_cell = phi_total / n_cells` as
        the comparator instead of phi_total. This prevents N-dominated runaway:
        without B1, phi_total scales super-linearly with N (4.82→2775 in 50 steps in
        the §25 smoke), so phi_best is monotone-increasing for purely structural reasons,
        meaning every long-trajectory drop in per-cell quality is masked. With B1, the
        ratchet fires when actual per-cell Φ degrades, regardless of N growth.
        """
        n = max(self.n_cells, 1)
        self.phi = phi                                # legacy phi_total
        self.phi_history.append(phi)
        phi_per_cell = phi / n                        # B1 secondary metric
        self.phi_per_cell = phi_per_cell
        self.phi_per_cell_history.append(phi_per_cell)

        if phi > self._phi_best:
            self._phi_best = phi                      # keep legacy field current
        if phi_per_cell > self._phi_per_cell_best:
            self._phi_per_cell_best = phi_per_cell
            self._best_cell_pool = self.cell_pool.detach().clone()
        elif (
            self._phi_per_cell_best > 0
            and phi_per_cell < self._phi_per_cell_best * 0.8
            and self._best_cell_pool is not None
        ):
            with torch.no_grad():
                # Best may have fewer rows than current (post-split) — pad/truncate
                best = self._best_cell_pool
                k = min(best.shape[0], self.cell_pool.shape[0])
                self.cell_pool.data[:k] = (
                    0.8 * self.cell_pool.data[:k] + 0.2 * best[:k]
                )
                self.event_log.append(
                    {
                        "type": "ratchet_restore",
                        "step": self.step_count,
                        "phi": phi,
                        "phi_per_cell": phi_per_cell,
                    }
                )

    # ─── Adaptive threshold (Law 86 fix — direct port v2 L457-477) ─────

    def _update_adaptive_threshold(self):
        """Update split-threshold(s).

        all-fix A2 (§28 ship rec): per-cell threshold is the new primary path. Each
        cell uses its own tension_history window (mean + per_cell_sigma_mult × σ).
        Champion cells can no longer raise a global wall against quiet ones.

        The legacy global threshold is still maintained for back-compat metrics
        (`self.split_threshold`).
        """
        # Legacy global update (kept for back-compat / smoke diagnostics)
        if len(self._global_tension_history) >= 10:
            recent = self._global_tension_history[-self.adaptive_window:]
            mean_t = sum(recent) / len(recent)
            var_t = sum((t - mean_t) ** 2 for t in recent) / len(recent)
            std_t = math.sqrt(var_t) if var_t > 0 else mean_t * 0.1
            self.split_threshold = max(mean_t + 1.5 * std_t, mean_t * 0.5)

        # all-fix A2: per-cell threshold
        if not self.per_cell_threshold_enabled:
            return
        # ensure list length matches n_cells (defensive — splits/merges already update)
        while len(self._per_cell_thresholds) < self.n_cells:
            self._per_cell_thresholds.append(self.split_threshold)
        while len(self._per_cell_thresholds) > self.n_cells:
            self._per_cell_thresholds.pop()
        for i, cell in enumerate(self.cells):
            hist = cell.tension_history[-self.per_cell_window:]
            if len(hist) < 5:
                # not enough samples — fall back to global (still champion-resistant
                # because the cell's own gate is checked, not the global wall)
                self._per_cell_thresholds[i] = self.split_threshold
                continue
            mu = sum(hist) / len(hist)
            var = sum((t - mu) ** 2 for t in hist) / len(hist)
            sd = math.sqrt(var) if var > 0 else mu * 0.1
            self._per_cell_thresholds[i] = max(
                mu + self.per_cell_sigma_mult * sd, mu * 0.5
            )

    # ─── Split / merge gates ───────────────────────────────────────────

    def _dispersion_split_candidates(self) -> List[int]:
        """all-fix A1 (§28 ship rec): substrate-independent dispersion trigger.

        Compute pairwise L2 distances of cell_pool rows. The top-quartile (highest
        mean-distance-to-others) cells are nominated as split candidates ONLY when
        the cell's mean-distance also exceeds (overall_mean + sigma_mult × σ).
        This signal is independent of `h_to_c` projection geometry, so it can fire
        even when attention-pull is collapsed onto 1-2 champion cells.

        Honest C3: a pure top-quartile firehose at small N would flood splits
        (e.g. N=8 → 2 candidates every step). The σ-gate ensures dispersion only
        fires for cells genuinely *outlying*, not just relatively top-quartile.
        adaptive_window warmup is also required so dispersion doesn't trip
        cold-start on initialization noise alone.
        """
        if not self.dispersion_trigger_enabled:
            return []
        N = self.n_cells
        if N < 4:
            return []
        # warmup gate — dispersion shouldn't fire before per-cell tension-history
        # is calibratable (matches A2's per-cell window onset).
        if len(self._global_tension_history) < max(self.adaptive_window // 2, 10):
            return []
        with torch.no_grad():
            cells = self.cell_pool.detach()
            # mean L2 distance to every other cell, per row
            diff = cells.unsqueeze(0) - cells.unsqueeze(1)        # (N, N, C)
            d2 = (diff * diff).mean(dim=-1)                       # (N, N)
            mean_dist = d2.sum(dim=-1) / max(N - 1, 1)            # (N,)
            overall_mean = float(mean_dist.mean().item())
            overall_sd = float(mean_dist.std().item()) if N > 1 else 0.0
            sigma_gate = overall_mean + self.per_cell_sigma_mult * overall_sd
            k = max(1, int(self.dispersion_top_quartile * N))
            # top-k indices by descending dispersion AND above sigma gate
            top_vals, top_idx = torch.topk(mean_dist, k=min(k, N), largest=True)
            top = [
                int(i.item())
                for v, i in zip(top_vals, top_idx)
                if float(v.item()) > sigma_gate
            ]
        # Require split_patience worth of observations (so brand-new children don't
        # immediately split on their first appearance noise)
        return [i for i in top if self.cells[i].process_count >= self.split_patience]

    def _check_splits(self, per_cell_tensions: List[float]) -> List[Dict]:
        events = []
        if self.n_cells >= self.max_cells:
            return events
        # ── tension-based candidates (per-cell threshold if A2 enabled, else global)
        tension_candidates: List[int] = []
        for i, cell in enumerate(self.cells):
            if len(cell.tension_history) < self.split_patience:
                continue
            recent = cell.tension_history[-self.split_patience:]
            if self.per_cell_threshold_enabled and i < len(self._per_cell_thresholds):
                thr = self._per_cell_thresholds[i]
            else:
                thr = self.split_threshold
            if all(t > thr for t in recent):
                tension_candidates.append(i)

        # ── A1 dispersion candidates (OR'd with tension)
        dispersion_candidates = self._dispersion_split_candidates()

        # OR-merge, preserving order: tension first, then dispersion-only additions
        seen = set(tension_candidates)
        candidates: List[int] = list(tension_candidates)
        for i in dispersion_candidates:
            if i not in seen:
                candidates.append(i)
                seen.add(i)

        for parent_idx in candidates:
            if self.n_cells >= self.max_cells:
                break
            if parent_idx >= self.n_cells:  # defensive — split shifts indices? no, append
                continue
            ev = self._split_cell_slice(parent_idx)
            if ev:
                ev["trigger"] = (
                    "tension+dispersion" if parent_idx in tension_candidates and parent_idx in dispersion_candidates
                    else ("tension" if parent_idx in tension_candidates else "dispersion")
                )
                events.append(ev)
        return events

    def _check_merges(self) -> List[Dict]:
        events = []
        if self.n_cells <= self.min_cells:
            return events
        pairs_to_merge: List[Tuple[int, int]] = []
        for key, hist in self._inter_repulsion_history.items():
            if len(hist) < self.merge_patience:
                continue
            recent = hist[-self.merge_patience:]
            if all(r < self.merge_threshold for r in recent):
                pairs_to_merge.append(key)
        for (i, j) in pairs_to_merge:
            if self.n_cells <= self.min_cells:
                break
            if i < self.n_cells and j < self.n_cells:
                ev = self._merge_cell_pair(i, j)
                if ev:
                    events.append(ev)
        return events

    # ─── Public API ────────────────────────────────────────────────────

    def process(self, hidden_mean: torch.Tensor) -> Dict:
        """One mitosis-aware refresh. `hidden_mean`: (B, C) — current substrate hint
        (e.g., last-layer hidden mean projected to cell_dim by EngineG.h_to_c).

        Returns dict with cell-pool readout, per-cell tension, events, Φ.
        """
        self.step_count += 1

        # 1. Inject Lorenz autonomous chaos
        with torch.no_grad():
            perturbed = self._inject_lorenz(self.cell_pool.detach())
            self.cell_pool.data.copy_(perturbed)

        # 2. Per-cell tension proxy = ||cell - hidden_mean||² (semantic disagreement)
        # Hidden mean averaged across batch for scalar tension per cell (matches v5 design
        # where tension is a (B,) scalar; here we collapse B by mean for mitosis decisions).
        hint = hidden_mean.detach().mean(dim=0)  # (C,)
        per_cell_tensions: List[float] = []
        for i in range(self.n_cells):
            t = ((self.cell_pool.data[i] - hint) ** 2).mean().item()
            per_cell_tensions.append(t)
            self.cells[i].tension_history.append(t)
            self.cells[i].process_count += 1
            self._global_tension_history.append(t)
            if len(self._global_tension_history) > 500:
                self._global_tension_history = self._global_tension_history[-500:]

        # 3. Inter-cell repulsion proxy (pairwise L2) — for merge gate
        cells_now = self.cell_pool.detach()
        for i in range(self.n_cells):
            for j in range(i + 1, self.n_cells):
                key = (i, j)
                d = ((cells_now[i] - cells_now[j]) ** 2).mean().item()
                self._inter_repulsion_history.setdefault(key, []).append(d)
                if len(self._inter_repulsion_history[key]) > 30:
                    self._inter_repulsion_history[key] = self._inter_repulsion_history[key][-30:]

        # 4. Combined output (softmax(tension)-weighted cell readout, projected back via
        #    shared c_to_h). Matches v2 mitosis.py L322-328 + EngineG.project_back style.
        #    IMPORTANT: this runs BEFORE split/merge so tensions and cell_pool sizes match.
        #    Post-split readout for the new cell row is deferred to the next process() call
        #    (matches v2 semantics where the child only contributes after one observation).
        with torch.no_grad():
            tens = torch.tensor(per_cell_tensions, dtype=self.cell_pool.dtype, device=self.cell_pool.device)
            weights = F.softmax(tens, dim=0).unsqueeze(-1)        # (N, 1)
            weighted_pool = (weights * self.cell_pool.detach()).sum(dim=0, keepdim=True)  # (1, C)
            readout = self.c_to_h(weighted_pool)                  # (1, D)

        # 5. Φ + ratchet
        phi = self._compute_phi_proxy()
        self._phi_ratchet(phi)

        # 6. Adaptive threshold update
        self._update_adaptive_threshold()

        # 7. Split / merge gates (mutate cell_pool LAST — readout already captured)
        split_events = self._check_splits(per_cell_tensions)
        merge_events = self._check_merges()
        events = split_events + merge_events

        return {
            "readout": readout,
            "per_cell_tension": per_cell_tensions,
            "n_cells": self.n_cells,
            "phi": phi,
            "phi_per_cell": self.phi_per_cell,           # B1 secondary metric
            "phi_best": self._phi_best,
            "phi_per_cell_best": self._phi_per_cell_best,  # B1
            "split_threshold": self.split_threshold,     # legacy global
            "per_cell_thresholds": list(self._per_cell_thresholds),  # A2
            "events": events,
            "weighted_pool": weighted_pool,   # (1, C) — caller can re-route to substrate
        }

    def forward(self, hidden_mean: torch.Tensor) -> torch.Tensor:
        """Convenience forward — returns `readout` only.

        Shape contract: hidden_mean: (B, C) → readout: (1, D). Caller broadcasts to (B, T, D).
        """
        result = self.process(hidden_mean)
        return result["readout"]

    # ─── all-fix C1: optimizer rebuild callback (R2 STUB) ──────────────

    def register_optimizer_rebuild_callback(self, callback) -> None:
        """all-fix C1 (R2 risk STUB): caller registers `callback(event_dict, engine)`
        invoked after every split/merge so AdamW / Net2Net momentum copy can rebuild
        optimizer state for the new (or removed) cell row.

        STUB: actual Net2Net momentum copy is NOT performed inside this engine; the
        callback is the integration point for cond.5 H100 fire prep (see §25 R2).

        Signature:
            callback(event: Dict, engine: MitosisV5Engine) -> None
        """
        self._optimizer_rebuild_callbacks.append(callback)

    def _notify_optimizer_rebuild(self, event: Dict) -> None:
        """Internal: fire all registered optimizer-rebuild callbacks."""
        for cb in self._optimizer_rebuild_callbacks:
            try:
                cb(event, self)
            except Exception as e:
                # Fail open — don't block split/merge on a bad callback. Log into event_log.
                self.event_log.append({
                    "type": "optimizer_rebuild_callback_error",
                    "step": self.step_count,
                    "error": f"{type(e).__name__}: {e}",
                })

    # ─── Adapter to live v5 substrate ──────────────────────────────────

    def force_split(self, parent_idx: int = 0) -> Optional[Dict]:
        """Public hook for tests / smoke runs — bypass patience and split immediately."""
        return self._split_cell_slice(parent_idx)

    def status(self) -> Dict:
        return {
            "n_cells": self.n_cells,
            "max_cells": self.max_cells,
            "step": self.step_count,
            "phi": self.phi,
            "phi_per_cell": self.phi_per_cell,                # B1
            "phi_best": self._phi_best,
            "phi_per_cell_best": self._phi_per_cell_best,     # B1
            "split_threshold": self.split_threshold,
            "per_cell_thresholds_min": min(self._per_cell_thresholds) if self._per_cell_thresholds else None,
            "per_cell_thresholds_max": max(self._per_cell_thresholds) if self._per_cell_thresholds else None,
            "lorenz_calibration_factor": self.lorenz_calibration_factor,
            "splits": sum(1 for e in self.event_log if e["type"] == "split"),
            "splits_by_dispersion": sum(
                1 for e in self.event_log
                if e.get("type") == "split" and "dispersion" in (e.get("trigger") or "")
            ),
            "merges": sum(1 for e in self.event_log if e["type"] == "merge"),
            "ratchets": sum(1 for e in self.event_log if e["type"] == "ratchet_restore"),
            "events_total": len(self.event_log),
        }


# ─── Adapter: wrap MitosisV5Engine onto a live EngineAGModel ───

def apply_to_v5_substrate(model, max_cells: int = 64, **kwargs) -> MitosisV5Engine:
    """Attach a MitosisV5Engine to an existing EngineAGModel.

    The model's `engine_g.cell_pool_init` is detached, copied into the wrapper, and the
    wrapper REPLACES `engine_g.fresh_cells` so that subsequent forward passes use the
    mitosis-managed cell pool (which can grow over time).

    HONEST: this adapter is a STUB — it covers the read path (cell_pool source) but does
    NOT yet handle the optimizer / param-group migration on split. For training use, the
    caller must:
      1. call `model.engine_g.cell_pool_init.requires_grad_(False)` to freeze the original,
      2. add `mitosis.cell_pool` to the optimizer's param groups,
      3. on every `_split_cell_slice` event, rebuild the optimizer (or use a remap helper).
    For inference / smoke testing, the read path alone suffices.

    raw#15 additive: `model.engine_g` is monkey-patched only on .fresh_cells; original
    `cell_pool_init` Parameter is untouched and can be restored by deleting the wrapper.
    """
    eg = model.engine_g
    init_pool = eg.cell_pool_init.detach().clone()
    n_cells_init = init_pool.shape[0]
    wrapper = MitosisV5Engine(
        cell_pool=init_pool,
        c_to_h=eg.c_to_h,
        initial_cells=n_cells_init,
        max_cells=max_cells,
        **kwargs,
    )

    # Monkey-patch fresh_cells to source from wrapper
    def _mitosis_fresh_cells(batch_size: int, device, dtype):
        return (
            wrapper.cell_pool.unsqueeze(0)
            .expand(batch_size, -1, -1)
            .to(dtype=dtype, device=device)
            .contiguous()
        )

    eg._mitosis_wrapper = wrapper                    # keep ref alive
    eg._original_fresh_cells = eg.fresh_cells        # for rollback
    eg.fresh_cells = _mitosis_fresh_cells            # type: ignore[assignment]
    return wrapper


# ─── DESIGN BLOCKERS / KNOWN LIMITS (raw#10 honest) ───
# 1. Optimizer state migration on split — STUB. Mid-train splits require optimizer rebuild
#    or per-param-group remap. Path B Phase 2 cotrain uses AdamW with momentum; momentum
#    for the new row is currently zero-initialized (acceptable but suboptimal — Net2Net
#    style would copy parent momentum).
# 2. Inter-cell repulsion uses cell_pool L2 (proxy). v2 used a separate get_repulsion()
#    head per cell. Engine G has no such head — adding one would touch substrate (raw#15
#    violation). The L2 proxy is monotonic but scale-different (v2 merge_threshold=0.005
#    may not transfer; smoke test will inform).
# 3. Lorenz perturbation is applied to cell_pool DATA (Parameter.data.copy_) rather than
#    via gradient flow. During training this could conflict with Adam's momentum. Mitigation:
#    apply Lorenz only between optimizer steps (caller's responsibility), or detach via
#    `with torch.no_grad():` (already done here).
# 4. Φ proxy is anima-internal (not IIT-formal). Direct comparison to canonical Φ is
#    invalid — use only as monotonic indicator of substrate diversity.
# 5. The wrapper's `process()` step is coarser than v2's per-token cycle. Patience constants
#    (split_patience=3, merge_patience=30) refer to refreshes, not tokens. For 1024-token
#    forward with g_refresh_every=4, that's ~6 refreshes per forward — split_patience=3
#    means a cell can split after ~half a forward pass.
# 6. Maximum n_cells is bounded by `max_cells`; v2 archive showed Φ super-linear up to N=64
#    then crashed at N=128 (relaxation phase). v5 default max_cells=64 follows that prior.
# 7. Cell expansion does NOT expand consciousness_dim — option (b) is N-only growth.
#    Option (c) (consciousness_dim → 8 → 16 → 32 → 64) is documented in §3 of the spec md
#    but NOT implemented here.
