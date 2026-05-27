#!/usr/bin/env python3
"""apply — run training/alpha_metric_v2.compute_alpha_v2 on dense 3K + 10K toys
+ sparse-snapshot historical artifacts. Emit result.json + comparison.md.

raw#15 additive — does not mutate any predecessor result.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/ghost/core/anima/training")
from alpha_metric_v2 import compute_alpha_v2, alpha_v1_ols  # noqa: E402

ROOT = Path("/Users/ghost/core/anima")
OUT = ROOT / "state/anima_alpha_metric_v2_2026_05_10"

DENSE_3K = OUT / "dense_3000_history.json"
DENSE_10K = OUT / "dense_10000_history.json"
SPARSE_3K = ROOT / "state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10/result.json"
SPARSE_10K = ROOT / "state/anima_clm_v5_anima_long_trajectory_extended_2026_05_10/result.json"


def _format_pb(pb: dict) -> dict:
    """JSON-serialise tuple keys."""
    out = {}
    for k, v in pb.items():
        if isinstance(k, tuple):
            kk = f"[{k[0]},{k[1]})"
        else:
            kk = str(k)
        out[kk] = v
    return out


def run_one(label: str, history: list[dict], min_samples: int) -> dict:
    v1 = alpha_v1_ols(history)
    v2 = compute_alpha_v2(history, min_samples=min_samples)
    out = {
        "label": label,
        "n_history": len(history),
        "min_samples": min_samples,
        "alpha_v1_OLS_logphi_vs_logn": v1,
        "alpha_v2": {
            "alpha_per_bin": _format_pb(v2["alpha_per_bin"]),
            "alpha_aggregate": v2["alpha_aggregate"],
            "saturation_warning": v2["saturation_warning"],
            "samples_per_bin": _format_pb(v2["samples_per_bin"]),
            "splits_per_bin": _format_pb(v2["splits_per_bin"]),
            "trended_alpha_per_bin": _format_pb(v2["trended_alpha_per_bin"]),
            "untrended_alpha_per_bin": _format_pb(v2["untrended_alpha_per_bin"]),
            "rate_per_bin_per_split": _format_pb(v2["rate_per_bin_per_split"]),
            "rate_per_bin_trended": _format_pb(v2["rate_per_bin_trended"]),
            "rate_per_bin_untrended": _format_pb(v2["rate_per_bin_untrended"]),
            "bin_edges": v2["bin_edges"],
            "diagnostics": v2["diagnostics"],
        },
    }
    return out


def main() -> None:
    results: dict = {}

    # 1. dense 3K toy
    d = json.load(open(DENSE_3K))
    results["dense_3k"] = run_one("dense 3K toy (snapshot_every=1)", d["history"], min_samples=5)
    results["dense_3k"]["recorded_v1_alpha"] = None  # not in dense file
    results["dense_3k"]["final_n_cells"] = d["final"]["n_cells"]
    results["dense_3k"]["final_n_splits"] = d["final"]["n_splits"]

    # 2. dense 10K toy
    d = json.load(open(DENSE_10K))
    results["dense_10k"] = run_one("dense 10K toy (snapshot_every=1)", d["history"], min_samples=5)
    results["dense_10k"]["final_n_cells"] = d["final"]["n_cells"]
    results["dense_10k"]["final_n_splits"] = d["final"]["n_splits"]

    # 3. sparse historical 3K (snapshot_every=100, 31 snapshots) — same trajectory
    d = json.load(open(SPARSE_3K))
    results["sparse_3k_hist"] = run_one(
        "sparse historical 3K (snapshot_every=100)", d["snapshots"], min_samples=1
    )
    results["sparse_3k_hist"]["recorded_v1_alpha"] = d["final"]["alpha_exponent"]

    # 4. sparse historical 10K (snapshot_every=100, 101 snapshots) — same trajectory
    d = json.load(open(SPARSE_10K))
    results["sparse_10k_hist"] = run_one(
        "sparse historical 10K (snapshot_every=100)", d["snapshots"], min_samples=1
    )
    results["sparse_10k_hist"]["recorded_v1_alpha"] = d["final"]["alpha_exponent_full"]

    out_path = OUT / "result.json"
    with open(out_path, "w") as fp:
        json.dump({
            "ts": "2026-05-10",
            "metric_module": "training/alpha_metric_v2.py",
            "lane": "BG-NEW-ALPHA-METRIC-V2 (track B reborn.B.cond.5)",
            "results": results,
        }, fp, indent=2, ensure_ascii=False, default=str)
    print(f"wrote {out_path}")

    # Pretty-print summary
    print()
    print("=" * 72)
    print("V1 vs V2 SUMMARY")
    print("=" * 72)
    for k, v in results.items():
        print(f"\n[{k}] {v['label']}")
        print(f"  n_history={v['n_history']}")
        print(f"  V1 OLS log Φ vs log n: {v['alpha_v1_OLS_logphi_vs_logn']}")
        if "recorded_v1_alpha" in v:
            print(f"  V1 recorded historical: {v['recorded_v1_alpha']}")
        a = v["alpha_v2"]
        print(f"  V2 aggregate: {a['alpha_aggregate']}")
        print(f"  V2 saturation_warning: {a['saturation_warning']}")
        print(f"  V2 max_cap_reached: {a['diagnostics']['max_cap_reached']}")
        print(f"  V2 alpha_per_bin:")
        for kk, vv in a["alpha_per_bin"].items():
            samp = a["samples_per_bin"].get(kk, 0)
            spl = a["splits_per_bin"].get(kk, 0)
            rate = a["rate_per_bin_per_split"].get(kk)
            rs = f"{rate:.3e}" if isinstance(rate, float) else "None"
            ss = f"{vv:.3f}" if isinstance(vv, float) else vv
            print(f"    {kk}: α={ss}, samples={samp}, splits={spl}, ΔΦ/split={rs}")


if __name__ == "__main__":
    main()
