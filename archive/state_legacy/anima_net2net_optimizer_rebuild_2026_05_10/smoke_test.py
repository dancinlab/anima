"""Smoke test: Net2Net AdamW callback vs zero-init baseline.

Builds a minimal MitosisV5Engine training loop with a fixed regression
target. Trains for 100 steps, forces 1 split at step 60 (after momentum has
accumulated), and 1 merge at step 80. Compares loss curve under:
  A. zero-init baseline (no callback registered — optimizer rebuilds with
     fresh state on the new Parameter)
  B. Net2Net callback (this BG's mitosis_c1_body.py)

Outputs:
  - smoke_result.json
  - smoke_loss_curve.png   (matplotlib)

raw#9: this lives under state/, gitignored.
: $0 local CPU only.
"""

import json
import os
import random
import sys
from pathlib import Path
from typing import Dict, List

import torch
import torch.nn as nn

# Path setup — absolute to avoid __file__ resolving to /tmp under some runners.
ANIMA_ROOT = Path("/Users/ghost/core/anima")
HERE = ANIMA_ROOT / "state" / "anima_net2net_optimizer_rebuild_2026_05_10"
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(HERE))

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from mitosis_c1_body import net2net_adamw_callback, post_step_snapshot  # noqa: E402


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    random.seed(seed)


def build_engine(initial_cells: int, channel: int, seed: int) -> MitosisV5Engine:
    set_seed(seed)
    cell_pool = torch.randn(initial_cells, channel) * 0.1
    c_to_h = nn.Linear(channel, channel, bias=False)
    eng = MitosisV5Engine(
        cell_pool=cell_pool,
        c_to_h=c_to_h,
        initial_cells=initial_cells,
        max_cells=initial_cells + 4,
        min_cells=max(2, initial_cells - 2),
    )
    # disable auto-trigger paths — we'll force splits/merges in the smoke
    eng.split_threshold = 999.0
    eng.dispersion_trigger_enabled = False
    eng.per_cell_threshold_enabled = False
    return eng


def build_optimizer(eng: MitosisV5Engine, lr: float = 5e-2) -> torch.optim.AdamW:
    # Single-param optimizer over cell_pool only (smoke test isolates the
    # exact Parameter we're migrating). Higher lr + high beta1 makes
    # momentum significant — F-NET2NET-1/2 surface here.
    return torch.optim.AdamW(
        [eng.cell_pool], lr=lr, betas=(0.95, 0.999), eps=1e-8,
    )


def regression_loss(
    eng: MitosisV5Engine,
    target: torch.Tensor,
    hidden_mean: torch.Tensor,
) -> torch.Tensor:
    """Per-row L2 to a fixed target — every row contributes its own gradient.

    target is broadcast (B=1, C); loss = mean over rows of ||row - target||^2.
    This makes momentum on individual rows actually matter, so splitting and
    losing exp_avg on a row creates a measurable loss bump.
    """
    rows = eng.cell_pool  # (N, C)
    diff = rows - target.unsqueeze(0)
    return (diff ** 2).mean()


def run_lane(
    label: str,
    use_callback: bool,
    n_steps: int = 300,
    split_at: int = 60,
    merge_at: int = 80,
    seed: int = 1234,
    stationary: bool = True,
) -> Dict:
    eng = build_engine(initial_cells=4, channel=16, seed=seed)
    opt = build_optimizer(eng)

    if use_callback:
        cb = net2net_adamw_callback(opt, momentum_noise=0.01, rng_seed=seed + 1)
        eng.register_optimizer_rebuild_callback(cb)

    # Non-trivial target — large enough that per-row momentum is meaningful.
    # Two-phase target so the optimizer is mid-flight (high momentum) when
    # split/merge events fire — exposes Net2Net momentum copy benefit.
    set_seed(seed + 100)
    target_a = torch.randn(16) * 2.0
    target_b = torch.randn(16) * 2.0
    losses: List[float] = []
    events: List[Dict] = []

    for step in range(n_steps):
        opt.zero_grad()
        # If stationary: single target (Net2Net should help — momentum valid).
        # If non-stationary: target shift @ step 50 — F-NET2NET-1 surfaces.
        if stationary:
            active_target = target_a
        else:
            active_target = target_a if step < 50 else target_b
        loss = regression_loss(eng, active_target, hidden_mean=None)
        loss.backward()
        opt.step()
        eng.step_count = step
        losses.append(float(loss.item()))

        if step == split_at:
            ev = eng._split_cell_slice(parent_idx=0)
            events.append({"step": step, "ev": ev, "label": "split"})
            # In zero-init baseline, the new Parameter has NO state in opt —
            # AdamW will lazily create zeros on first step. To make the
            # comparison fair, baseline must also have its optimizer's
            # param_groups updated to point at the new param. Otherwise the
            # optimizer would keep training the dead old param.
            if not use_callback:
                # Manually swap param ref (simulating naive rebuild).
                old = None
                for g in opt.param_groups:
                    for i, p in enumerate(g["params"]):
                        if p is not eng.cell_pool and p.dim() == 2:
                            old = p
                            g["params"][i] = eng.cell_pool
                if old is not None and old in opt.state:
                    del opt.state[old]
        if step == merge_at:
            # Pick two cells to merge
            if eng.n_cells >= 2:
                ev = eng._merge_cell_pair(0, 1)
                events.append({"step": step, "ev": ev, "label": "merge"})
                if not use_callback:
                    old = None
                    for g in opt.param_groups:
                        for i, p in enumerate(g["params"]):
                            if p is not eng.cell_pool and p.dim() == 2:
                                old = p
                                g["params"][i] = eng.cell_pool
                    if old is not None and old in opt.state:
                        del opt.state[old]

        # Refresh snapshot for callback after every step (so it tracks live
        # AdamW state). The callback's internal snap is updated on each event
        # but between events we want it fresh.
        if use_callback:
            try:
                fresh = post_step_snapshot(opt, eng.cell_pool)
                # Inject into callback closure via a known attribute.
                # The factory exposes the snap via __closure__; safer: do
                # nothing — first-event snapshot capture handles it via the
                # fallback path that scans optimizer.state for old_param.
            except Exception:
                pass

    return {
        "label": label,
        "use_callback": use_callback,
        "losses": losses,
        "events": [{"step": e["step"], "label": e["label"]} for e in events],
        "final_loss": losses[-1],
        "loss_at_split_plus_1": losses[split_at + 1] if split_at + 1 < n_steps else None,
        "loss_at_merge_plus_1": losses[merge_at + 1] if merge_at + 1 < n_steps else None,
    }


def main() -> None:
    # Two scenarios:
    #  A. Stationary target — Net2Net should help (momentum is valid post-event)
    #  B. Target-shift mid-train — Net2Net may HURT (stale momentum, F-NET2NET-1)
    print("=== scenario A: stationary target ===")
    base = run_lane("zero_init_baseline_A", use_callback=False, stationary=True)
    n2n = run_lane("net2net_callback_A", use_callback=True, stationary=True)
    print("=== scenario B: target shift ===")
    base_b = run_lane("zero_init_baseline_B", use_callback=False, stationary=False)
    n2n_b = run_lane("net2net_callback_B", use_callback=True, stationary=False)

    # Compute summary
    def post_event_recovery(losses: List[float], step: int, window: int = 5) -> Dict:
        if step + window >= len(losses):
            return {"event_step_loss": None, "recovery_window_mean": None}
        return {
            "event_step_loss": losses[step],
            "post_event_loss": losses[step + 1],
            "recovery_window_mean": sum(losses[step + 1:step + 1 + window]) / window,
            "loss_jump": losses[step + 1] - losses[step],
        }

    def lane_summary(b: Dict, n: Dict) -> Dict:
        return {
            "baseline": {
                "final_loss": b["final_loss"],
                "split_recovery": post_event_recovery(b["losses"], 60),
                "merge_recovery": post_event_recovery(b["losses"], 80),
            },
            "net2net": {
                "final_loss": n["final_loss"],
                "split_recovery": post_event_recovery(n["losses"], 60),
                "merge_recovery": post_event_recovery(n["losses"], 80),
            },
            "delta_final_loss": n["final_loss"] - b["final_loss"],
            "net2net_wins_final": n["final_loss"] < b["final_loss"],
            "net2net_wins_5step_post_split": (
                sum(n["losses"][61:66]) < sum(b["losses"][61:66])
            ),
            "net2net_wins_5step_post_merge": (
                sum(n["losses"][81:86]) < sum(b["losses"][81:86])
            ),
        }

    summary = {
        "scenario_A_stationary": lane_summary(base, n2n),
        "scenario_B_target_shift": lane_summary(base_b, n2n_b),
        "n_steps": 300,
    }

    out = {
        "stationary": {"baseline": base, "net2net": n2n},
        "target_shift": {"baseline": base_b, "net2net": n2n_b},
        "summary": summary,
        "n_steps": 300,
    }

    out_path = HERE / "smoke_result.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {out_path}")

    # Plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        for ax, (label, b_lane, n_lane) in zip(axes, [
            ("A: stationary target", base, n2n),
            ("B: target shift @ step 50", base_b, n2n_b),
        ]):
            ax.plot(b_lane["losses"], label="zero-init baseline", color="tab:red", alpha=0.8)
            ax.plot(n_lane["losses"], label="Net2Net callback", color="tab:blue", alpha=0.8)
            ax.axvline(60, color="gray", linestyle="--", alpha=0.5, label="split @60")
            ax.axvline(80, color="gray", linestyle=":", alpha=0.5, label="merge @80")
            ax.set_xlabel("step")
            ax.set_ylabel("per-row L2 loss")
            ax.set_title(label)
            ax.legend()
            ax.grid(alpha=0.3)
            ax.set_yscale("log")
        fig.suptitle("C1 Net2Net AdamW migration vs zero-init baseline (300-step smoke)")
        png_path = HERE / "smoke_loss_curve.png"
        fig.savefig(png_path, dpi=120, bbox_inches="tight")
        print(f"wrote {png_path}")
    except ImportError:
        print("matplotlib not available — skipping PNG")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
