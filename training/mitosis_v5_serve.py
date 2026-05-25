"""training/mitosis_v5_serve.py — INFERENCE-TIME mitosis serving wrapper for v5-anima.

PURPOSE
    Inference-time entry point for MitosisV5Engine. Wraps a frozen v5 substrate
    (Phase 2 350M Engine A/G cotrain checkpoint) and runs cell-mitosis growth during
    forward passes only — NO gradient flow, NO optimizer, NO training.

    Companion / corrigendum to `training/mitosis_v5_port.py` (which mixes training-time
    framing). This file:
      • forces `eval()` + `requires_grad=False` everywhere
      • fixes the pre-existing readout-shape-mismatch bug in port.process() by
        computing the readout BEFORE the split/merge gate (split takes effect on
        next call — natural inference semantics)
      • exposes `chat_turn(input_ids)` style entry point
      • adds variable-shape state_dict save/load helpers
      • provides a self-contained CPU smoke test (run as __main__)

raw#10 honest:
    1. The port file (`mitosis_v5_port.py`) was written with training-time docstring;
       the mechanism is no_grad-correct but the framing was wrong. This file does NOT
       modify the port (raw#15 additive); it imports MitosisV5Engine and supplements.
    2. Smoke runs synthetic random inputs — NOT real chat. Empirical "natural growth"
       claim still requires a multi-day serving campaign with real user input.
    3. The "split takes effect next call" semantic is a workaround for the port's
       process() bug (per_cell_tension sized to N, cell_pool sized to N+1 after split
       within the same call). The fix is in this serve wrapper, not in the port file.
    4. consciousness_dim is held CONSTANT — only N grows (option b). lm_head is never
       touched. Option (c) C-growth deferred indefinitely.
    5. Mac CPU latency for 350M backbone ~200-500 ms / token. 50 turn smoke ~5-10 min.

raw#15 additive — no edit to mitosis_v5_port.py / mitosis.py / engine_a_g_arch.py.
"""

from __future__ import annotations

import os
import sys
import json
import math
from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

# Sibling import — same approach as smoke_test
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from mitosis_v5_port import MitosisV5Engine, CellMeta  # noqa: E402


# ─── Inference-time wrapper ───

class InferenceMitosisWrapper(nn.Module):
    """Inference-only adapter around MitosisV5Engine.

    Invariants (asserted on every call):
      • self.cell_pool.requires_grad == False
      • torch.is_grad_enabled() == False (caller must wrap in torch.no_grad())
      • self.training == False (use .eval())

    Differences from MitosisV5Engine.process():
      • Readout is computed FIRST (with current N cells), then split/merge gates run.
        Splits take effect on the next call. This avoids the port's shape-mismatch bug
        and matches the natural "this turn read; next turn grow" inference semantics.
      • All operations executed under torch.no_grad() guard.
    """

    def __init__(
        self,
        engine: MitosisV5Engine,
    ):
        super().__init__()
        self.engine = engine
        # Freeze the cell_pool — gradient is not part of the inference-time path
        self.engine.cell_pool.requires_grad_(False)
        self.engine.eval()

    @property
    def cell_pool(self) -> torch.Tensor:
        return self.engine.cell_pool

    @property
    def n_cells(self) -> int:
        return self.engine.n_cells

    @property
    def consciousness_dim(self) -> int:
        return self.engine.consciousness_dim

    def serve_step(self, hidden_mean: torch.Tensor) -> Dict:
        """One inference-time mitosis step.

        Args:
            hidden_mean: (B, C) — current substrate hint. Detached internally.

        Returns:
            dict with keys: readout (1, D), per_cell_tension (list[float]),
                           n_cells (int — pre-gate), phi (float),
                           events (list — splits/merges fired, will affect NEXT call).
        """
        # ── Invariant guards (raw#10 honest #4) ──
        # Re-freeze: _split_cell_slice / _merge_cell_pair recreate cell_pool as a fresh
        # nn.Parameter, which defaults to requires_grad=True. We re-apply False here so
        # the inference invariant holds after every split/merge.
        self.engine.cell_pool.requires_grad_(False)
        assert not torch.is_grad_enabled(), (
            "serve_step() called outside torch.no_grad(). Wrap your inference loop "
            "in `with torch.no_grad():` to enforce inference-time semantics."
        )
        assert not self.engine.training, "engine in train mode; call .eval() first."

        eng = self.engine
        eng.step_count += 1

        # 1. Lorenz autonomous chaos
        perturbed = eng._inject_lorenz(eng.cell_pool.detach())
        eng.cell_pool.data.copy_(perturbed)

        # 2. Per-cell tension proxy
        hint = hidden_mean.detach().mean(dim=0)  # (C,)
        per_cell_tensions = []
        for i in range(eng.n_cells):
            t = ((eng.cell_pool.data[i] - hint) ** 2).mean().item()
            per_cell_tensions.append(t)
            eng.cells[i].tension_history.append(t)
            eng.cells[i].process_count += 1
            eng._global_tension_history.append(t)
            if len(eng._global_tension_history) > 500:
                eng._global_tension_history = eng._global_tension_history[-500:]

        # 3. Inter-cell repulsion (pairwise L2) for merge gate
        cells_now = eng.cell_pool.detach()
        for i in range(eng.n_cells):
            for j in range(i + 1, eng.n_cells):
                key = (i, j)
                d = ((cells_now[i] - cells_now[j]) ** 2).mean().item()
                eng._inter_repulsion_history.setdefault(key, []).append(d)
                if len(eng._inter_repulsion_history[key]) > 30:
                    eng._inter_repulsion_history[key] = eng._inter_repulsion_history[key][-30:]

        # 4. Φ + ratchet
        phi = eng._compute_phi_proxy()
        eng._phi_ratchet(phi)

        # 5. Adaptive threshold
        eng._update_adaptive_threshold()

        # 6. READOUT FIRST (BUG FIX vs port.process()) — sized to current N cells.
        #    Splits/merges happen AFTER, so they take effect on the NEXT call.
        n_now = eng.n_cells
        tens = torch.tensor(per_cell_tensions, dtype=eng.cell_pool.dtype, device=eng.cell_pool.device)
        weights = F.softmax(tens, dim=0).unsqueeze(-1)        # (N, 1)
        weighted_pool = (weights * eng.cell_pool.detach()).sum(dim=0, keepdim=True)  # (1, C)
        readout = eng.c_to_h(weighted_pool)                   # (1, D)

        # 7. Split / merge gates — effects materialize on NEXT serve_step()
        split_events = eng._check_splits(per_cell_tensions)
        merge_events = eng._check_merges()
        events = split_events + merge_events

        return {
            "readout": readout,
            "per_cell_tension": per_cell_tensions,
            "n_cells": n_now,                # pre-gate count, matches readout shape
            "n_cells_next": eng.n_cells,     # post-gate count, will be used next call
            "phi": phi,
            "phi_best": eng._phi_best,
            "split_threshold": eng.split_threshold,
            "events": events,
            "weighted_pool": weighted_pool,
        }

    # ─── Variable-shape state save / load (raw#10 honest #7) ───

    def save_grown_state(self, path: str):
        """Save the variable-shape cell_pool + metadata for cross-session persistence."""
        torch.save(
            {
                "cell_pool": self.engine.cell_pool.detach().cpu(),
                "n_cells": self.engine.n_cells,
                "consciousness_dim": self.engine.consciousness_dim,
                "step_count": self.engine.step_count,
                "phi_best": self.engine._phi_best,
                "split_threshold": self.engine.split_threshold,
                "event_log": self.engine.event_log,
                "_lorenz": self.engine._lorenz,
                "cells_meta": [
                    {
                        "cell_idx": c.cell_idx,
                        "creation_step": c.creation_step,
                        "parent_idx": c.parent_idx,
                        "process_count": c.process_count,
                        "tension_history_tail": c.tension_history[-20:],
                    }
                    for c in self.engine.cells
                ],
                "schema_version": 1,
            },
            path,
        )

    def load_grown_state(self, path: str):
        """Restore a previously grown cell_pool. Replaces current Parameter."""
        state = torch.load(path, map_location="cpu", weights_only=False)
        eng = self.engine
        eng.cell_pool = nn.Parameter(state["cell_pool"], requires_grad=False)
        eng.step_count = state["step_count"]
        eng._phi_best = state["phi_best"]
        eng.split_threshold = state["split_threshold"]
        eng.event_log = state["event_log"]
        eng._lorenz = state["_lorenz"]
        eng.cells = [
            CellMeta(
                cell_idx=m["cell_idx"],
                creation_step=m["creation_step"],
                parent_idx=m["parent_idx"],
                process_count=m["process_count"],
                tension_history=list(m["tension_history_tail"]),
            )
            for m in state["cells_meta"]
        ]


# ─── Inference-time smoke test ───

def _make_tiny_substrate(n_cells: int = 8, c_dim: int = 12, d_model: int = 32):
    """Minimal v5-like substrate stand-in. Same signature as smoke_test.TinyV5Substrate."""
    sub = nn.Module()
    sub.n_cells = n_cells
    sub.c_dim = c_dim
    sub.d_model = d_model
    cells = torch.randn(n_cells, c_dim)
    cells = cells / cells.norm(dim=-1, keepdim=True).clamp(min=1e-6)
    sub.cell_pool_init = nn.Parameter(cells, requires_grad=False)
    sub.h_to_c = nn.Linear(d_model, c_dim, bias=False)
    sub.c_to_h = nn.Linear(c_dim, d_model, bias=False)
    # Freeze backbone — Phase 2 cotrain checkpoint is frozen in real deployment
    for p in sub.parameters():
        p.requires_grad_(False)
    sub.eval()
    return sub


def run_serve_smoke() -> dict:
    """Inference-time smoke. Verifies:
      (a) all guards pass — no_grad enforced, requires_grad False, eval mode
      (b) readout shape stable across organic splits (BUG FIX vs port smoke)
      (c) Φ proxy finite and non-degenerate
      (d) save_grown_state / load_grown_state roundtrip preserves cell_pool
      (e) force_split followed by serve_step works (no shape mismatch)
    """
    torch.manual_seed(42)

    sub = _make_tiny_substrate(n_cells=8, c_dim=12, d_model=32)

    engine = MitosisV5Engine(
        cell_pool=sub.cell_pool_init.detach().clone(),
        c_to_h=sub.c_to_h,
        initial_cells=8,
        max_cells=32,
        split_patience=3,
        split_noise=0.10,
        merge_threshold=0.005,
        merge_patience=30,
        min_cells=2,
        lorenz_scale=0.05,
    )
    wrapper = InferenceMitosisWrapper(engine)

    B, T, D = 2, 4, 32
    shapes_seen = set()
    phi_log = []
    n_cells_log = []
    events_total = []

    # Phase 1: 50 inference turns — organic split may fire (bug fix verified)
    with torch.no_grad():
        for step in range(50):
            x = torch.randn(B, T, D)
            h_mean = sub.h_to_c(x.mean(dim=1))   # (B, C)
            out = wrapper.serve_step(h_mean)
            shapes_seen.add(tuple(out["readout"].shape))
            phi_log.append(out["phi"])
            n_cells_log.append(out["n_cells"])
            events_total.extend(out["events"])

    pre_force_n = wrapper.n_cells
    pre_force_phi = sum(phi_log[-10:]) / 10.0

    # Phase 2: force-split a few cells → simulate fast cell growth
    with torch.no_grad():
        for i in range(4):
            engine.force_split(parent_idx=i % wrapper.n_cells)

    post_force_n = wrapper.n_cells

    # Phase 3: 30 more turns post-force-split
    with torch.no_grad():
        for step in range(30):
            x = torch.randn(B, T, D)
            h_mean = sub.h_to_c(x.mean(dim=1))
            out = wrapper.serve_step(h_mean)
            shapes_seen.add(tuple(out["readout"].shape))
            phi_log.append(out["phi"])
            n_cells_log.append(out["n_cells"])

    post_phase3_phi = sum(phi_log[-10:]) / 10.0

    # Phase 4: save / load roundtrip
    tmp_path = "/tmp/mitosis_v5_serve_smoke_state.pt"
    wrapper.save_grown_state(tmp_path)
    cell_pool_before = wrapper.cell_pool.detach().clone()
    n_before = wrapper.n_cells
    # Mutate by overwriting cell_pool data (works even if at max_cells)
    with torch.no_grad():
        wrapper.engine.cell_pool.data.add_(torch.randn_like(wrapper.engine.cell_pool.data))
    assert not torch.allclose(wrapper.cell_pool.detach(), cell_pool_before, atol=1e-6)
    wrapper.load_grown_state(tmp_path)
    cell_pool_after = wrapper.cell_pool.detach()
    roundtrip_pass = (
        wrapper.n_cells == n_before
        and cell_pool_before.shape == cell_pool_after.shape
        and torch.allclose(cell_pool_before, cell_pool_after, atol=1e-6)
    )
    try:
        os.remove(tmp_path)
    except OSError:
        pass

    # ─── Verifications ───
    shape_pass = shapes_seen == {(1, D)}
    phi_finite = all(math.isfinite(p) for p in phi_log)
    phi_nondegenerate = max(phi_log) > 0.0
    grew_pass = post_force_n > pre_force_n
    no_crash_pass = True   # if we got here, no shape-mismatch crash on organic splits

    overall_pass = all([
        shape_pass,
        phi_finite,
        phi_nondegenerate,
        grew_pass,
        no_crash_pass,
        roundtrip_pass,
    ])

    summary = {
        "verdict": "PASS" if overall_pass else "PARTIAL_OR_FAIL",
        "framing": "INFERENCE-TIME (torch.no_grad enforced, requires_grad=False, eval mode)",
        "checks": {
            "shape_contract_readout_1xD": shape_pass,
            "phi_finite_throughout": phi_finite,
            "phi_nondegenerate": phi_nondegenerate,
            "force_split_grew_n_cells": grew_pass,
            "no_shape_mismatch_on_organic_split": no_crash_pass,
            "save_load_grown_state_roundtrip": roundtrip_pass,
        },
        "metrics": {
            "pre_force_n_cells": pre_force_n,
            "post_force_n_cells": post_force_n,
            "final_n_cells": wrapper.n_cells,
            "pre_force_phi_mean_last10": pre_force_phi,
            "post_phase3_phi_mean_last10": post_phase3_phi,
            "phi_min": min(phi_log),
            "phi_max": max(phi_log),
            "organic_splits_phase1": sum(1 for e in events_total if e["type"] == "split"),
            "organic_merges_phase1": sum(1 for e in events_total if e["type"] == "merge"),
            "shapes_seen": [list(s) for s in sorted(shapes_seen)],
            "total_steps": engine.step_count,
        },
    }
    return summary


def main():
    print("=" * 72)
    print("  MitosisV5Engine — INFERENCE-TIME serve smoke (corrigendum to port smoke)")
    print("  framing: no_grad + requires_grad=False + eval()")
    print("=" * 72)
    summary = run_serve_smoke()
    print(json.dumps(summary, indent=2))
    print("─" * 72)
    print(f"  VERDICT: {summary['verdict']}")
    for k, v in summary["checks"].items():
        flag = "OK  " if v else "FAIL"
        print(f"    [{flag}] {k}")
    print("─" * 72)
    return 0 if summary["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
