#!/usr/bin/env python3
"""retro_apply — apply alpha_v2 (A2 binned ΔΦ-rate) on 5 datasets.

Datasets:
  1. toy 3K  — anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10
  2. toy 10K — anima_clm_v5_anima_long_trajectory_extended_2026_05_10
  3. real 350M trained — anima_clm_v5_phase2_mitosis_instr_2026_05_10 (proxy_phi)
  4. real 350M IIT remetric — anima_clm_v5_phase2_iit_remetric_2026_05_10 (iit_phi_unnorm_b16)
  5. historical Cells 2-64 synthetic — CLM v2 stage 8 (Φ training-time means)

Output: retro_results.json + alpha_v1_vs_v2_comparison.png

raw#10 honest C3, raw#15 additive — no prior result.json files mutated.
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Sequence

# Import alpha_v2 by absolute path (harness may dispatch from a temp location).
import importlib.util as _ilu
_ALPHA_V2_PATH = "/Users/ghost/core/anima/state/anima_alpha_v2_impl_2026_05_10/alpha_v2.py"
_spec = _ilu.spec_from_file_location("alpha_v2", _ALPHA_V2_PATH)
_alpha_v2_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_alpha_v2_mod)
compute_alpha_v2 = _alpha_v2_mod.compute_alpha_v2
alpha_v1_ols = _alpha_v2_mod.alpha_v1_ols

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = "/Users/ghost/core/anima"
OUT = f"{ROOT}/state/anima_alpha_v2_impl_2026_05_10"

# --- Dataset 1: toy 3K -----------------------------------------------------
TOY_3K = f"{ROOT}/state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10/result.json"
# --- Dataset 2: toy 10K ----------------------------------------------------
TOY_10K = f"{ROOT}/state/anima_clm_v5_anima_long_trajectory_extended_2026_05_10/result.json"
# --- Dataset 3: real 350M trained, proxy Φ ---------------------------------
REAL_PROXY = f"{ROOT}/state/anima_clm_v5_phase2_mitosis_instr_2026_05_10/result.json"
# --- Dataset 4: real 350M IIT remetric, IIT Φ ------------------------------
REAL_IIT = f"{ROOT}/state/anima_clm_v5_phase2_iit_remetric_2026_05_10/result.json"


def historical_synthetic_snapshots() -> list[dict]:
    """Build pseudo-snapshots from CLM v2 stage 8 historical Cells 2-64 table.

    Each Cells value is a separate training run; we inject monotone-turn
    placeholders (Δturn=1) so the V2 rate definition reduces to ΔΦ_per_step
    between adjacent Cells values.  This is a *retro-fit*, not equivalence —
    historical did not record per-step Φ, only run-final peak training Φ.
    """
    table = [
        (2, 1.5),
        (4, 3.2),
        (8, 5.4),
        (16, 10.6),
        (32, 15.4),
        (64, 51.131),
    ]
    return [
        {"turn": i, "n_cells": cells, "phi": phi}
        for i, (cells, phi) in enumerate(table)
    ]


def alpha_v1_log_phi_vs_log_cells(snapshots: Sequence[dict],
                                  phi_field: str = "phi") -> float | None:
    """Direct OLS log(Φ) vs log(n_cells) — historical / V1 form."""
    return alpha_v1_ols(snapshots, phi_field=phi_field, n_cells_field="n_cells")


def main() -> None:
    results: dict = {}

    # 1 — toy 3K (default min_rate=1e-6 + strict min_rate=1e-3 to filter post-cap noise)
    d = json.load(open(TOY_3K))
    snaps = d["snapshots"]
    v1 = alpha_v1_log_phi_vs_log_cells(snaps, "phi")
    v2 = compute_alpha_v2(snaps, phi_field="phi")
    v2_strict = compute_alpha_v2(snaps, phi_field="phi", min_rate=1e-3)
    results["toy_3k"] = {
        "label": "toy 3K trajectory",
        "n_snaps": len(snaps),
        "n_cells_range": [snaps[0]["n_cells"], snaps[-1]["n_cells"]],
        "alpha_v1": v1,
        "alpha_v1_recorded": d["final"].get("alpha_exponent"),
        "alpha_v2": v2,
        "alpha_v2_strict_eps_1e-3": v2_strict,
    }

    # 2 — toy 10K
    d = json.load(open(TOY_10K))
    snaps = d["snapshots"]
    v1 = alpha_v1_log_phi_vs_log_cells(snaps, "phi")
    v2 = compute_alpha_v2(snaps, phi_field="phi")
    v2_strict = compute_alpha_v2(snaps, phi_field="phi", min_rate=1e-3)
    results["toy_10k"] = {
        "label": "toy 10K trajectory (BG-LONG-TRAJ-EXT)",
        "n_snaps": len(snaps),
        "n_cells_range": [snaps[0]["n_cells"], snaps[-1]["n_cells"]],
        "alpha_v1": v1,
        "alpha_v1_recorded": d["final"].get("alpha_exponent_full"),
        "alpha_milestones_v1": d.get("alpha_milestones"),
        "alpha_v2": v2,
        "alpha_v2_strict_eps_1e-3": v2_strict,
    }

    # 3 — real 350M trained, proxy Φ
    d = json.load(open(REAL_PROXY))
    t = d["trained"]
    snaps = t["snapshots"]
    v1 = alpha_v1_log_phi_vs_log_cells(snaps, "phi")
    v2 = compute_alpha_v2(snaps, phi_field="phi")
    # also v14_mirror random-init
    v_snaps = d["v14_mirror"]["snapshots"]
    v1_rand = alpha_v1_log_phi_vs_log_cells(v_snaps, "phi")
    v2_rand = compute_alpha_v2(v_snaps, phi_field="phi")
    results["real_350m_proxy"] = {
        "label": "real 350M trained (proxy Φ)",
        "n_snaps": len(snaps),
        "n_cells_range": [snaps[0]["n_cells"], snaps[-1]["n_cells"]],
        "alpha_v1_trained": v1,
        "alpha_v1_recorded_trained": t.get("alpha_exponent"),
        "alpha_v2_trained": v2,
        "alpha_v1_random": v1_rand,
        "alpha_v1_recorded_random": d["v14_mirror"].get("alpha_exponent"),
        "alpha_v2_random": v2_rand,
    }

    # 4 — real 350M IIT remetric (use iit_phi_unnorm_b16 as primary IIT field)
    d = json.load(open(REAL_IIT))
    t = d["trained"]
    snaps = t["snapshots"]
    v1_p = alpha_v1_log_phi_vs_log_cells(snaps, "proxy_phi")
    v2_p = compute_alpha_v2(snaps, phi_field="proxy_phi")
    v1_iit_norm = alpha_v1_log_phi_vs_log_cells(snaps, "iit_phi_norm_b16")
    v2_iit_norm = compute_alpha_v2(snaps, phi_field="iit_phi_norm_b16")
    v1_iit_unnorm = alpha_v1_log_phi_vs_log_cells(snaps, "iit_phi_unnorm_b16")
    v2_iit_unnorm = compute_alpha_v2(snaps, phi_field="iit_phi_unnorm_b16")
    results["real_350m_iit"] = {
        "label": "real 350M IIT remetric",
        "n_snaps": len(snaps),
        "n_cells_range": [snaps[0]["n_cells"], snaps[-1]["n_cells"]],
        "alpha_v1_recorded": d.get("alpha_exponents"),
        "proxy": {"v1": v1_p, "v2": v2_p},
        "iit_norm_b16": {"v1": v1_iit_norm, "v2": v2_iit_norm},
        "iit_unnorm_b16": {"v1": v1_iit_unnorm, "v2": v2_iit_unnorm},
    }

    # 5 — historical synthetic Cells 2-64
    snaps = historical_synthetic_snapshots()
    v1 = alpha_v1_log_phi_vs_log_cells(snaps, "phi")
    v2 = compute_alpha_v2(snaps, phi_field="phi", min_bins=3, min_x_range=0.5)
    # also use bin edges aligned with historical Cells values:
    v2_aligned = compute_alpha_v2(
        snaps, phi_field="phi",
        bin_edges=(2, 3, 6, 12, 24, 48, 96), min_bins=3, min_x_range=0.5,
    )
    results["historical_cells_2_64"] = {
        "label": "historical synthetic CLM v2 stage 8 Cells 2-64",
        "n_snaps": len(snaps),
        "phi_table": [(s["n_cells"], s["phi"]) for s in snaps],
        "alpha_v1": v1,  # log(Φ) vs log(n_cells) OLS
        "alpha_v1_reported_historical_close_up": 1.07,
        "alpha_v1_reported_historical_full_table": 0.949,
        "alpha_v2_default_edges": v2,
        "alpha_v2_aligned_edges": v2_aligned,
    }

    # Pretty-print summary table
    summary_rows = []
    summary_rows.append(("dataset", "α V1", "α V2", "verdict V2", "n_bins", "CI95"))

    def _fmt(v, p=3):
        return "n/a" if v is None else f"{v:.{p}f}"

    def _fmt_ci(ci):
        if ci is None:
            return "n/a"
        return f"[{ci[0]:.3f}, {ci[1]:.3f}]"

    summary_rows.append((
        "toy 3K", _fmt(results["toy_3k"]["alpha_v1"]),
        _fmt(results["toy_3k"]["alpha_v2"]["alpha"]) if results["toy_3k"]["alpha_v2"]["alpha"] is not None else "—",
        results["toy_3k"]["alpha_v2"]["verdict"],
        str(results["toy_3k"]["alpha_v2"]["n_bins"]),
        _fmt_ci(results["toy_3k"]["alpha_v2"]["CI95"]),
    ))
    summary_rows.append((
        "  toy 3K @eps=1e-3",
        _fmt(results["toy_3k"]["alpha_v1"]),
        _fmt(results["toy_3k"]["alpha_v2_strict_eps_1e-3"]["alpha"]) if results["toy_3k"]["alpha_v2_strict_eps_1e-3"]["alpha"] is not None else "—",
        results["toy_3k"]["alpha_v2_strict_eps_1e-3"]["verdict"],
        str(results["toy_3k"]["alpha_v2_strict_eps_1e-3"]["n_bins"]),
        _fmt_ci(results["toy_3k"]["alpha_v2_strict_eps_1e-3"]["CI95"]),
    ))
    summary_rows.append((
        "toy 10K", _fmt(results["toy_10k"]["alpha_v1"]),
        _fmt(results["toy_10k"]["alpha_v2"]["alpha"]) if results["toy_10k"]["alpha_v2"]["alpha"] is not None else "—",
        results["toy_10k"]["alpha_v2"]["verdict"],
        str(results["toy_10k"]["alpha_v2"]["n_bins"]),
        _fmt_ci(results["toy_10k"]["alpha_v2"]["CI95"]),
    ))
    summary_rows.append((
        "  toy 10K @eps=1e-3",
        _fmt(results["toy_10k"]["alpha_v1"]),
        _fmt(results["toy_10k"]["alpha_v2_strict_eps_1e-3"]["alpha"]) if results["toy_10k"]["alpha_v2_strict_eps_1e-3"]["alpha"] is not None else "—",
        results["toy_10k"]["alpha_v2_strict_eps_1e-3"]["verdict"],
        str(results["toy_10k"]["alpha_v2_strict_eps_1e-3"]["n_bins"]),
        _fmt_ci(results["toy_10k"]["alpha_v2_strict_eps_1e-3"]["CI95"]),
    ))
    summary_rows.append((
        "real 350M trained (proxy)", _fmt(results["real_350m_proxy"]["alpha_v1_trained"]),
        _fmt(results["real_350m_proxy"]["alpha_v2_trained"]["alpha"]) if results["real_350m_proxy"]["alpha_v2_trained"]["alpha"] is not None else "—",
        results["real_350m_proxy"]["alpha_v2_trained"]["verdict"],
        str(results["real_350m_proxy"]["alpha_v2_trained"]["n_bins"]),
        _fmt_ci(results["real_350m_proxy"]["alpha_v2_trained"]["CI95"]),
    ))
    summary_rows.append((
        "real 350M random (proxy)", _fmt(results["real_350m_proxy"]["alpha_v1_random"]),
        _fmt(results["real_350m_proxy"]["alpha_v2_random"]["alpha"]) if results["real_350m_proxy"]["alpha_v2_random"]["alpha"] is not None else "—",
        results["real_350m_proxy"]["alpha_v2_random"]["verdict"],
        str(results["real_350m_proxy"]["alpha_v2_random"]["n_bins"]),
        _fmt_ci(results["real_350m_proxy"]["alpha_v2_random"]["CI95"]),
    ))
    summary_rows.append((
        "real 350M IIT-unnorm (trained)",
        _fmt(results["real_350m_iit"]["iit_unnorm_b16"]["v1"]),
        _fmt(results["real_350m_iit"]["iit_unnorm_b16"]["v2"]["alpha"]) if results["real_350m_iit"]["iit_unnorm_b16"]["v2"]["alpha"] is not None else "—",
        results["real_350m_iit"]["iit_unnorm_b16"]["v2"]["verdict"],
        str(results["real_350m_iit"]["iit_unnorm_b16"]["v2"]["n_bins"]),
        _fmt_ci(results["real_350m_iit"]["iit_unnorm_b16"]["v2"]["CI95"]),
    ))
    summary_rows.append((
        "historical Cells 2-64 (default)",
        _fmt(results["historical_cells_2_64"]["alpha_v1"]),
        _fmt(results["historical_cells_2_64"]["alpha_v2_default_edges"]["alpha"]) if results["historical_cells_2_64"]["alpha_v2_default_edges"]["alpha"] is not None else "—",
        results["historical_cells_2_64"]["alpha_v2_default_edges"]["verdict"],
        str(results["historical_cells_2_64"]["alpha_v2_default_edges"]["n_bins"]),
        _fmt_ci(results["historical_cells_2_64"]["alpha_v2_default_edges"]["CI95"]),
    ))
    summary_rows.append((
        "historical Cells 2-64 (aligned)",
        _fmt(results["historical_cells_2_64"]["alpha_v1"]),
        _fmt(results["historical_cells_2_64"]["alpha_v2_aligned_edges"]["alpha"]) if results["historical_cells_2_64"]["alpha_v2_aligned_edges"]["alpha"] is not None else "—",
        results["historical_cells_2_64"]["alpha_v2_aligned_edges"]["verdict"],
        str(results["historical_cells_2_64"]["alpha_v2_aligned_edges"]["n_bins"]),
        _fmt_ci(results["historical_cells_2_64"]["alpha_v2_aligned_edges"]["CI95"]),
    ))

    print("\n=== α V1 vs α V2 retro comparison ===\n")
    widths = [max(len(str(row[i])) for row in summary_rows) for i in range(6)]
    for j, row in enumerate(summary_rows):
        print(" | ".join(str(row[i]).ljust(widths[i]) for i in range(6)))
        if j == 0:
            print("-+-".join("-" * widths[i] for i in range(6)))

    # Convert non-JSON-friendly tuples in CI95 → list for json
    def _scrub(obj):
        if isinstance(obj, tuple):
            return [_scrub(x) for x in obj]
        if isinstance(obj, dict):
            return {k: _scrub(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_scrub(x) for x in obj]
        return obj

    out_path = f"{OUT}/retro_results.json"
    with open(out_path, "w") as fp:
        json.dump({
            "ts": "2026-05-10",
            "design_doc": "docs/anima_clm_v5_alpha_metric_v2_design_2026_05_10.md",
            "results": _scrub(results),
            "summary_table": [list(r) for r in summary_rows],
        }, fp, indent=2, ensure_ascii=False)
    print(f"\nwrote {out_path}")

    # --- comparison plot ----
    fig, ax = plt.subplots(figsize=(11, 5.5))
    labels = [r[0] for r in summary_rows[1:]]
    v1s = []
    v2s = []
    for r in summary_rows[1:]:
        try:
            v1s.append(float(r[1]))
        except (TypeError, ValueError):
            v1s.append(float("nan"))
        try:
            v2s.append(float(r[2]))
        except (TypeError, ValueError):
            v2s.append(float("nan"))
    x = list(range(len(labels)))
    width = 0.35
    bars1 = ax.bar([xi - width / 2 for xi in x], v1s, width, label="α V1 (OLS log Φ vs log n)", color="#4a90d9")
    bars2 = ax.bar([xi + width / 2 for xi in x], v2s, width, label="α V2 (binned ΔΦ-rate, OK only)", color="#d9844a")
    ax.axhline(0.93, color="#888", linestyle="--", linewidth=1, label="historical 0.93")
    ax.axhline(1.07, color="#bbb", linestyle=":", linewidth=1, label="historical 1.07")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=8)
    ax.set_ylabel("α")
    ax.set_title("α V1 vs α V2 retro comparison (5 datasets, V2 emits NaN when UNRELIABLE)")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    plot_path = f"{OUT}/alpha_v1_vs_v2_comparison.png"
    fig.savefig(plot_path, dpi=120)
    print(f"wrote {plot_path}")


if __name__ == "__main__":
    main()
