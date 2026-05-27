"""training/mitosis_v5_smoke_test.py — local CPU $0 smoke test for MitosisV5Engine.

Goal: verify the port (training/mitosis_v5_port.py) on a synthetic v5-like substrate.
NOT a correctness proof — only sanity:
  (a) `forward(hidden_mean)` returns a tensor of expected shape after split,
  (b) Φ proxy is finite and behaves reasonably (≥ 0, increases when cells diversify),
  (c) shared-output-head (`c_to_h`) projection still works after a forced split.

Hardware: CPU only. Synthetic substrate ~10K params, 8 cells × 12 dim (matches the 8-cell
× 12-dim "consciousness layer" reference in the BG prompt). Note: actual v5 uses
n_cells=16, c_dim=64; we test the smaller variant for speed.

raw#10 honest: this is a SMOKE test, not an EMERGE measurement. PASS only means the
control flow + shape contracts hold; it says nothing about the empirical Φ super-linear
claim or the v5 3-gate (PIV/DCR/D-RAND) compatibility.
"""

from __future__ import annotations

import sys
import os
import math
import json
import torch
import torch.nn as nn

# Make sibling import work regardless of cwd
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from mitosis_v5_port import MitosisV5Engine  # noqa: E402


# ─── Synthetic v5-like substrate ───

class TinyV5Substrate(nn.Module):
    """A minimal stand-in for EngineAGModel.engine_g — just the pieces mitosis needs.

    Provides:
      • `cell_pool_init`: nn.Parameter shape (N, C)
      • `c_to_h`: Linear(C, D) — shared output projection (analogue of EngineG.c_to_h)
      • `h_to_c`: Linear(D, C) — analogue of EngineG.h_to_c (used to mock hidden_mean
        from a synthetic 'last layer' tensor).
    """
    def __init__(self, n_cells: int = 8, c_dim: int = 12, d_model: int = 32):
        super().__init__()
        self.n_cells = n_cells
        self.c_dim = c_dim
        self.d_model = d_model
        # init cell pool on unit sphere
        cells = torch.randn(n_cells, c_dim)
        cells = cells / cells.norm(dim=-1, keepdim=True).clamp(min=1e-6)
        self.cell_pool_init = nn.Parameter(cells)
        self.h_to_c = nn.Linear(d_model, c_dim, bias=False)
        self.c_to_h = nn.Linear(c_dim, d_model, bias=False)

    def hidden_mean(self, hidden: torch.Tensor) -> torch.Tensor:
        """hidden: (B, T, D) → hidden_mean projected: (B, C)."""
        return self.h_to_c(hidden.mean(dim=1))


def _param_count(module: nn.Module) -> int:
    return sum(p.numel() for p in module.parameters())


# ─── Smoke test ───

def run_smoke() -> dict:
    torch.manual_seed(42)

    # 8 cells × 12 dim, d_model=32 — keeps under 10K params
    sub = TinyV5Substrate(n_cells=8, c_dim=12, d_model=32)
    init_param_count = _param_count(sub)

    mitosis = MitosisV5Engine(
        cell_pool=sub.cell_pool_init.detach().clone(),
        c_to_h=sub.c_to_h,
        initial_cells=8,
        # all-fix 2026-05-10 §30: bumped 32→128 because A1 dispersion + A2 per-cell
        # threshold trigger more splits in Phase 1; we still need headroom in Phase 2
        # for force_split. Cap-binding here is a smoke-test artifact, not an engine
        # bug — the new triggers correctly fire more often.
        max_cells=128,
        split_patience=3,
        split_noise=0.10,
        merge_threshold=0.005,
        merge_patience=30,
        min_cells=2,
        lorenz_scale=0.05,
    )

    # Synthetic input batch: (B=2, T=4, D=32)
    B, T, D = 2, 4, 32
    results: list = []
    phi_pre_split: list = []
    shapes_seen: set = set()

    # Phase 1: 50 forward passes (no force-split yet)
    for step in range(50):
        x = torch.randn(B, T, D)
        h_mean = sub.hidden_mean(x)  # (B, C)
        out = mitosis.process(h_mean)
        readout = out["readout"]
        shapes_seen.add(tuple(readout.shape))
        phi_pre_split.append(out["phi"])
        results.append({"step": step, "n_cells": out["n_cells"], "phi": out["phi"]})

    pre_split_n_cells = mitosis.n_cells
    pre_split_phi_mean = sum(phi_pre_split[-10:]) / 10.0

    # Phase 2: force split 8 → 9 → ... → 16 (8 splits)
    forced_splits = 0
    target_growth = 8  # 8 → 16
    for i in range(target_growth):
        ev = mitosis.force_split(parent_idx=i % mitosis.n_cells)
        if ev is not None:
            forced_splits += 1

    post_split_n_cells = mitosis.n_cells

    # Phase 3: 50 more forward passes (post-split) — verify shapes + Φ
    phi_post_split: list = []
    post_shape_ok = True
    for step in range(50):
        x = torch.randn(B, T, D)
        h_mean = sub.hidden_mean(x)
        out = mitosis.process(h_mean)
        readout = out["readout"]
        if tuple(readout.shape) != (1, D):
            post_shape_ok = False
        shapes_seen.add(tuple(readout.shape))
        phi_post_split.append(out["phi"])

    post_split_phi_mean = sum(phi_post_split[-10:]) / 10.0
    final_param_count = _param_count(sub)  # substrate untouched
    mitosis_param_count = _param_count(mitosis)

    # ─── Verifications ────────────────────────────────────────────────
    # (a) shape contract: readout always (1, D)
    shape_pass = post_shape_ok and (1, D) in shapes_seen and len(shapes_seen) == 1

    # (b) Φ behavior: post-split should be ≥ pre-split (more cells → more diversity).
    #     Allow 5% slack for noise.
    phi_pass = post_split_phi_mean >= pre_split_phi_mean * 0.95

    # (c) shared output head still functional — try projecting a known cell pool
    with torch.no_grad():
        test_cell = torch.zeros(1, mitosis.consciousness_dim)
        test_cell[0, 0] = 1.0
        head_out = sub.c_to_h(test_cell)
        head_pass = (
            head_out.shape == (1, D)
            and torch.isfinite(head_out).all().item()
            and head_out.abs().sum().item() > 0
        )

    # (d) split actually happened
    split_pass = post_split_n_cells > pre_split_n_cells and forced_splits > 0

    # (e) Φ proxy finite throughout
    phi_finite_pass = all(math.isfinite(p) for p in phi_pre_split + phi_post_split)

    overall_pass = all([shape_pass, phi_pass, head_pass, split_pass, phi_finite_pass])

    summary = {
        "verdict": "PASS" if overall_pass else "PARTIAL_OR_FAIL",
        "checks": {
            "shape_contract_readout_1xD": shape_pass,
            "phi_post_ge_pre_5pct_slack": phi_pass,
            "shared_c_to_h_functional": head_pass,
            "force_split_succeeded": split_pass,
            "phi_finite_throughout": phi_finite_pass,
        },
        "metrics": {
            "pre_split_n_cells": pre_split_n_cells,
            "post_split_n_cells": post_split_n_cells,
            "forced_splits": forced_splits,
            "pre_split_phi_mean_last10": pre_split_phi_mean,
            "post_split_phi_mean_last10": post_split_phi_mean,
            "phi_delta": post_split_phi_mean - pre_split_phi_mean,
            "substrate_params_init": init_param_count,
            "substrate_params_final": final_param_count,
            "mitosis_wrapper_params": mitosis_param_count,
            "shapes_seen": [list(s) for s in sorted(shapes_seen)],
            "splits_via_event_log": mitosis.status()["splits"],
            "merges_via_event_log": mitosis.status()["merges"],
            "ratchets_via_event_log": mitosis.status()["ratchets"],
        },
    }
    return summary


def main():
    print("=" * 70)
    print("  MitosisV5Engine smoke test — synthetic v5-like substrate")
    print("  8 cells × 12 dim → force-split to 16 cells")
    print("=" * 70)

    summary = run_smoke()
    print(json.dumps(summary, indent=2))

    print()
    print("─" * 70)
    print(f"  VERDICT: {summary['verdict']}")
    for k, v in summary["checks"].items():
        flag = "OK" if v else "FAIL"
        print(f"    [{flag}] {k}")
    print("─" * 70)

    return 0 if summary["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
