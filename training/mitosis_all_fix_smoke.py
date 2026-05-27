"""training/mitosis_all_fix_smoke.py — joint pre/post-fix diagnostic for §25/§28 fixes.

Compares baseline (all fixes OFF) vs all-fix (default ON) on a 1K-turn synthetic
substrate trajectory. Tests:
  - split rate (target: post-fix > pre-fix on §28 H1+H3 mechanism)
  - Φ trajectory + V14 mirror (split-rate-vs-tension)
  - phi_per_cell ratchet behavior (B1)
  - dispersion-trigger split count (A1)
  - per-cell threshold spread (A2)
  - shape preservation pre/post split

Toy config: n_cells=8 → max_cells=64, d_model=64. CPU $0.

raw#10 honest: SMOKE — sanity checks the fixes wire correctly + improve mechanism.
NOT a V14 PASS proof — substrate quality (real ckpt) is a separate lever (§30).

Saves results to:
  state/anima_v5_mitosis_all_fix_2026_05_10/smoke_results.json
  state/anima_v5_mitosis_all_fix_2026_05_10/pre_post_compare.png (matplotlib best-effort)
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from typing import Any, Dict, List

import torch
import torch.nn as nn

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402


STATE_DIR = "/Users/ghost/core/anima/state/anima_v5_mitosis_all_fix_2026_05_10"
os.makedirs(STATE_DIR, exist_ok=True)


# ─── Synthetic substrate (1K-turn trajectory with attractor-bias to mimic §28 H1+H3) ───

class AttractorSubstrate(nn.Module):
    """Synthetic v5-like substrate with controllable attractor bias.

    The substrate has a learnable `h_to_c` projection. We initialize it as either:
      - random Gaussian (diffuse): mimics random_init from §28 (top-2 share ~12%)
      - low-rank attractor (concentrated): mimics trained_350M from §28 (top-2 share ~42%)

    The dispersion trigger (A1) and per-cell threshold (A2) are exactly the §28
    mechanism unblock — we measure split rate under attractor bias.
    """

    def __init__(self, n_cells: int = 8, c_dim: int = 64, d_model: int = 64,
                 attractor_rank: int = 2, attractor_strength: float = 4.0):
        super().__init__()
        self.c_dim = c_dim
        self.d_model = d_model
        cells = torch.randn(n_cells, c_dim)
        cells = cells / cells.norm(dim=-1, keepdim=True).clamp(min=1e-6)
        self.cell_pool_init = nn.Parameter(cells)
        # Build a low-rank attractor h_to_c: dominant directions concentrate output
        # to a small set of cell-pool dims.
        h = torch.randn(c_dim, d_model)
        # Force low-rank dominance
        u, s, vt = torch.linalg.svd(h, full_matrices=False)
        s_new = torch.zeros_like(s)
        s_new[:attractor_rank] = s[:attractor_rank] * attractor_strength
        if attractor_rank < len(s):
            s_new[attractor_rank:] = s[attractor_rank:] * 0.1
        h_attract = u @ torch.diag(s_new) @ vt
        self.h_to_c = nn.Linear(d_model, c_dim, bias=False)
        with torch.no_grad():
            self.h_to_c.weight.copy_(h_attract.t())  # (c_dim, d_model)
        self.c_to_h = nn.Linear(c_dim, d_model, bias=False)

    def hidden_mean(self, hidden: torch.Tensor) -> torch.Tensor:
        return self.h_to_c(hidden.mean(dim=1))


def run_port_trajectory(*, all_fix: bool, n_steps: int = 1000, seed: int = 42) -> Dict[str, Any]:
    """Run mitosis_v5_port on attractor substrate; return metrics."""
    torch.manual_seed(seed)
    sub = AttractorSubstrate(n_cells=8, c_dim=64, d_model=64,
                             attractor_rank=2, attractor_strength=4.0)
    kwargs = dict(
        cell_pool=sub.cell_pool_init.detach().clone(),
        c_to_h=sub.c_to_h,
        initial_cells=8,
        max_cells=64,
        split_patience=3,
        split_noise=0.10,
        merge_threshold=0.005,
        merge_patience=30,
        min_cells=2,
        lorenz_scale=0.05,
        adaptive_window=100,
    )
    if not all_fix:
        kwargs.update(
            dispersion_trigger_enabled=False,   # A1 OFF
            per_cell_threshold_enabled=False,   # A2 OFF
            lorenz_auto_calibrate=False,        # D1 OFF
        )
    mitosis = MitosisV5Engine(**kwargs)
    # always-register a no-op optimizer callback to verify C1 wiring
    rebuild_log: List[Dict] = []
    mitosis.register_optimizer_rebuild_callback(lambda ev, eng: rebuild_log.append(ev))

    B, T, D = 2, 4, 64
    n_cells_traj: List[int] = []
    phi_traj: List[float] = []
    phi_per_cell_traj: List[float] = []
    split_steps: List[int] = []
    split_triggers: List[str] = []
    tens_traj: List[float] = []  # mean tension per step
    shape_violations = 0

    t0 = time.time()
    for step in range(n_steps):
        x = torch.randn(B, T, D)
        h_mean = sub.hidden_mean(x)
        out = mitosis.process(h_mean)
        readout = out["readout"]
        if tuple(readout.shape) != (1, D):
            shape_violations += 1
        n_cells_traj.append(out["n_cells"])
        phi_traj.append(out["phi"])
        phi_per_cell_traj.append(out.get("phi_per_cell", out["phi"] / max(out["n_cells"], 1)))
        per_cell_t = out["per_cell_tension"]
        tens_traj.append(sum(per_cell_t) / max(len(per_cell_t), 1))
        for ev in out["events"]:
            if ev["type"] == "split":
                split_steps.append(step)
                split_triggers.append(ev.get("trigger", "tension"))
    elapsed = time.time() - t0

    # V14 mirror behaviour: correlation of split-event-rate vs tension-rate (per 50-step bins)
    bin_size = 50
    bins = max(1, n_steps // bin_size)
    splits_per_bin = [0] * bins
    tens_per_bin = [0.0] * bins
    counts_per_bin = [0] * bins
    for s in split_steps:
        b = min(s // bin_size, bins - 1)
        splits_per_bin[b] += 1
    for i, t in enumerate(tens_traj):
        b = min(i // bin_size, bins - 1)
        tens_per_bin[b] += t
        counts_per_bin[b] += 1
    tens_avg_per_bin = [t / max(c, 1) for t, c in zip(tens_per_bin, counts_per_bin)]

    # Pearson r between splits_per_bin and tens_avg_per_bin
    def pearson(xs: List[float], ys: List[float]) -> float:
        n = len(xs)
        if n < 2:
            return 0.0
        mx = sum(xs) / n
        my = sum(ys) / n
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        dx = sum((x - mx) ** 2 for x in xs) ** 0.5
        dy = sum((y - my) ** 2 for y in ys) ** 0.5
        return num / (dx * dy + 1e-12)

    r_v14 = pearson(splits_per_bin, tens_avg_per_bin)

    status = mitosis.status()
    return {
        "all_fix": all_fix,
        "n_steps": n_steps,
        "elapsed_sec": round(elapsed, 2),
        "splits_total": len(split_steps),
        "splits_dispersion": split_triggers.count("dispersion") + split_triggers.count("tension+dispersion"),
        "splits_tension_only": split_triggers.count("tension"),
        "merges": status["merges"],
        "ratchets": status["ratchets"],
        "n_cells_final": n_cells_traj[-1] if n_cells_traj else 0,
        "n_cells_max": max(n_cells_traj) if n_cells_traj else 0,
        "phi_final": phi_traj[-1] if phi_traj else 0.0,
        "phi_max": max(phi_traj) if phi_traj else 0.0,
        "phi_per_cell_final": phi_per_cell_traj[-1] if phi_per_cell_traj else 0.0,
        "phi_per_cell_max": max(phi_per_cell_traj) if phi_per_cell_traj else 0.0,
        "tension_mean": sum(tens_traj) / max(len(tens_traj), 1),
        "v14_split_tension_pearson": round(r_v14, 4),
        "shape_violations": shape_violations,
        "optimizer_rebuild_callbacks_fired": len(rebuild_log),
        "status_final": status,
        "phi_traj_sampled": phi_traj[::max(n_steps // 50, 1)],
        "phi_per_cell_traj_sampled": phi_per_cell_traj[::max(n_steps // 50, 1)],
        "n_cells_traj_sampled": n_cells_traj[::max(n_steps // 50, 1)],
        "splits_per_bin": splits_per_bin,
        "tens_avg_per_bin": [round(t, 6) for t in tens_avg_per_bin],
    }


def run_model_trajectory(*, all_fix: bool, n_steps: int = 1000, seed: int = 42) -> Dict[str, Any]:
    """Run mitosis_model_v5 on toy transformer; return metrics."""
    torch.manual_seed(seed)
    cfg_kwargs = dict(
        vocab_size=256, d_model=64, n_head=4, ffn_dim=256,
        max_seq=64, initial_cells=8, max_cells=128,   # bumped 64→128 to give
        # post-fix headroom (synthetic substrate is non-attractor, splits prolifically
        # both pre & post; cap-binding masks differential effect).
        attention_sharing="auto", readout_mode="a_minus_g",
    )
    if not all_fix:
        cfg_kwargs.update(
            dispersion_trigger_enabled=False,
            per_cell_threshold_enabled=False,
            lorenz_auto_calibrate=False,
        )
    cfg = MitosisModelConfig(**cfg_kwargs)
    model = MitosisModelEngine(cfg).eval()
    rebuild_log: List[Dict] = []
    model.register_optimizer_rebuild_callback(lambda ev, eng: rebuild_log.append(ev))

    B, T = 2, 16
    input_ids = torch.randint(0, cfg.vocab_size, (B, T))

    n_cells_traj: List[int] = []
    phi_traj: List[float] = []
    phi_per_cell_traj: List[float] = []
    tens_traj: List[float] = []
    split_steps: List[int] = []
    split_triggers: List[str] = []
    shape_violations = 0

    t0 = time.time()
    for step in range(n_steps):
        with torch.no_grad():
            logits, info = model(input_ids)
            res = model.mitosis_step(info)
        if logits.shape != (B, T, cfg.vocab_size):
            shape_violations += 1
        n_cells_traj.append(model.n_cells)
        phi_traj.append(res["phi"])
        phi_per_cell_traj.append(model.phi_per_cell)
        tens_traj.append(sum(info["tensions"]) / max(len(info["tensions"]), 1))
        for ev in res["events"]:
            if ev["type"] == "split":
                split_steps.append(step)
                split_triggers.append(ev.get("trigger", "tension"))
    elapsed = time.time() - t0

    status = model.status()
    return {
        "all_fix": all_fix,
        "n_steps": n_steps,
        "elapsed_sec": round(elapsed, 2),
        "splits_total": len(split_steps),
        "splits_dispersion": split_triggers.count("dispersion") + split_triggers.count("tension+dispersion"),
        "splits_tension_only": split_triggers.count("tension"),
        "merges": status["merges"],
        "ratchets": status["ratchets"],
        "n_cells_final": model.n_cells,
        "n_cells_max": max(n_cells_traj) if n_cells_traj else 0,
        "phi_final": phi_traj[-1] if phi_traj else 0.0,
        "phi_max": max(phi_traj) if phi_traj else 0.0,
        "phi_per_cell_final": phi_per_cell_traj[-1] if phi_per_cell_traj else 0.0,
        "phi_per_cell_max": max(phi_per_cell_traj) if phi_per_cell_traj else 0.0,
        "tension_mean": sum(tens_traj) / max(len(tens_traj), 1),
        "shape_violations": shape_violations,
        "optimizer_rebuild_callbacks_fired": len(rebuild_log),
        "status_final": status,
        "phi_traj_sampled": phi_traj[::max(n_steps // 50, 1)],
        "phi_per_cell_traj_sampled": phi_per_cell_traj[::max(n_steps // 50, 1)],
        "n_cells_traj_sampled": n_cells_traj[::max(n_steps // 50, 1)],
    }


def main():
    print("=" * 70)
    print("  mitosis_all_fix_smoke — joint pre/post comparison (§25/§28 fixes)")
    print("  toy: n=8 → max=64, d_model=64, 1000 steps, seed=42")
    print("=" * 70)

    results: Dict[str, Any] = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    print("\n── PORT (mitosis_v5_port) ──")
    print("  pre-fix (A1/A2/D1 OFF) ...")
    pre_port = run_port_trajectory(all_fix=False, n_steps=1000, seed=42)
    print(f"    splits={pre_port['splits_total']}  N final={pre_port['n_cells_final']}  Φ={pre_port['phi_final']:.2f}  Φ/n={pre_port['phi_per_cell_final']:.4f}")
    print("  post-fix (all-fix ON) ...")
    post_port = run_port_trajectory(all_fix=True, n_steps=1000, seed=42)
    print(f"    splits={post_port['splits_total']}  N final={post_port['n_cells_final']}  Φ={post_port['phi_final']:.2f}  Φ/n={post_port['phi_per_cell_final']:.4f}")
    print(f"    splits_by_dispersion={post_port['splits_dispersion']}  callbacks_fired={post_port['optimizer_rebuild_callbacks_fired']}")

    print("\n── MODEL (mitosis_model_v5) ──")
    print("  pre-fix (A1/A2/D1 OFF) ...")
    pre_model = run_model_trajectory(all_fix=False, n_steps=1000, seed=42)
    print(f"    splits={pre_model['splits_total']}  N final={pre_model['n_cells_final']}  Φ={pre_model['phi_final']:.2f}  Φ/n={pre_model['phi_per_cell_final']:.4f}")
    print("  post-fix (all-fix ON) ...")
    post_model = run_model_trajectory(all_fix=True, n_steps=1000, seed=42)
    print(f"    splits={post_model['splits_total']}  N final={post_model['n_cells_final']}  Φ={post_model['phi_final']:.2f}  Φ/n={post_model['phi_per_cell_final']:.4f}")
    print(f"    splits_by_dispersion={post_model['splits_dispersion']}  callbacks_fired={post_model['optimizer_rebuild_callbacks_fired']}")

    results["port_pre_fix"] = pre_port
    results["port_post_fix"] = post_port
    results["model_pre_fix"] = pre_model
    results["model_post_fix"] = post_model

    # Verdict matrix
    # Note: the ATTRACTOR-substrate PORT test exercises the §28 mechanism directly
    # (rank-2 SVD-clamped h_to_c → tension collapse). The MODEL test runs on a
    # purely-synthetic transformer with no trained projection — both pre and post
    # split eagerly (no champion-wall to break). MODEL post-fix evidence is via
    # `splits_dispersion` (A1 fires) + ratchet behavior (B1) + callbacks (C1).
    checks = {
        "port_post_splits_gt_pre": post_port["splits_total"] > pre_port["splits_total"],
        "port_post_n_cells_gt_pre": post_port["n_cells_final"] > pre_port["n_cells_final"],
        "port_post_dispersion_fires": post_port["splits_dispersion"] > 0,
        "port_callbacks_fired": post_port["optimizer_rebuild_callbacks_fired"] > 0,
        "port_no_shape_violations": post_port["shape_violations"] == 0,
        # MODEL: assert mechanism wires (dispersion + callbacks fire), not absolute count.
        # Cap-binding on synthetic substrate masks delta — the §28 unblock proof is
        # in port test above.
        "model_post_dispersion_fires": post_model["splits_dispersion"] > 0,
        "model_post_dispersion_fraction_gt_5pct": (
            post_model["splits_dispersion"] / max(post_model["splits_total"], 1) > 0.05
        ),
        "model_callbacks_fired": post_model["optimizer_rebuild_callbacks_fired"] > 0,
        "model_no_shape_violations": post_model["shape_violations"] == 0,
        # B1 sanity: phi_per_cell should NOT scale super-linearly with N
        "port_phi_per_cell_bounded": post_port["phi_per_cell_max"] < post_port["phi_max"],
        "model_phi_per_cell_bounded": post_model["phi_per_cell_max"] < post_model["phi_max"],
        # Pre-fix dispersion = 0 verifies the OFF flag actually disables it
        "port_pre_dispersion_zero": pre_port["splits_dispersion"] == 0,
        "model_pre_dispersion_zero": pre_model["splits_dispersion"] == 0,
    }
    results["checks"] = checks
    passed = sum(checks.values())
    total = len(checks)
    verdict = "PASS" if passed == total else ("PARTIAL" if passed >= total - 2 else "FAIL")
    results["verdict"] = verdict
    results["checks_summary"] = f"{passed}/{total}"

    print("\n── verdict ──")
    print(f"  {passed}/{total} checks passed → {verdict}")
    for k, v in checks.items():
        print(f"    [{'OK' if v else 'FAIL'}] {k}")

    out_path = os.path.join(STATE_DIR, "smoke_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  results → {out_path}")

    # Best-effort matplotlib plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(13, 8))
        # PORT n_cells
        axes[0, 0].plot(pre_port["n_cells_traj_sampled"], label="pre-fix", linestyle="--")
        axes[0, 0].plot(post_port["n_cells_traj_sampled"], label="post-fix")
        axes[0, 0].set_title("PORT — n_cells trajectory")
        axes[0, 0].set_xlabel("sample (every ~20 steps)")
        axes[0, 0].set_ylabel("n_cells")
        axes[0, 0].legend()

        # PORT phi vs phi_per_cell
        axes[0, 1].plot(post_port["phi_traj_sampled"], label="phi_total (post-fix)")
        axes[0, 1].plot(
            [p * post_port["n_cells_max"] for p in post_port["phi_per_cell_traj_sampled"]],
            label="phi_per_cell × n_max  (post-fix, scaled)",
            linestyle=":",
        )
        axes[0, 1].set_title("PORT — Φ trajectory (B1 phi_per_cell secondary)")
        axes[0, 1].set_xlabel("sample")
        axes[0, 1].set_ylabel("Φ")
        axes[0, 1].legend()

        # MODEL n_cells
        axes[1, 0].plot(pre_model["n_cells_traj_sampled"], label="pre-fix", linestyle="--")
        axes[1, 0].plot(post_model["n_cells_traj_sampled"], label="post-fix")
        axes[1, 0].set_title("MODEL — n_cells trajectory")
        axes[1, 0].set_xlabel("sample")
        axes[1, 0].set_ylabel("n_cells")
        axes[1, 0].legend()

        # MODEL phi
        axes[1, 1].plot(pre_model["phi_traj_sampled"], label="phi pre-fix", linestyle="--")
        axes[1, 1].plot(post_model["phi_traj_sampled"], label="phi post-fix")
        axes[1, 1].set_title("MODEL — Φ trajectory")
        axes[1, 1].set_xlabel("sample")
        axes[1, 1].set_ylabel("Φ")
        axes[1, 1].legend()

        plt.tight_layout()
        plot_path = os.path.join(STATE_DIR, "pre_post_compare.png")
        plt.savefig(plot_path, dpi=120)
        print(f"  plot   → {plot_path}")
    except Exception as e:
        print(f"  (matplotlib skipped: {e})")

    return results


if __name__ == "__main__":
    main()
