#!/usr/bin/env python3
# state/f3_n_convergence_test/sweep_driver.py
# F3 Stouffer z mathematical-limit convergence test as N -> inf.
# Fixed config: coupling=1.0 dim=4x4 (cycle 4 PASS_STRICT boundary).
# Levels: N = 200 / 500 / 1000 / 2000 / 5000, perms = N/4.
# Local-only, Mac CPU $0. raw 9 exemption per existing prod tool relaxation.
#
# Runs the prod tool's run() function in-process (avoids subprocess overhead),
# tracks p_value + cohen_d + Stouffer z + wallclock per level. Computes
# variance and locates N* where variance < 1% of mean.

import sys
import os
import json
import time
import math
import datetime

# Make the prod tool importable
ANIMA_ROOT = "/Users/ghost/core/anima"
sys.path.insert(0, os.path.join(ANIMA_ROOT, "tool"))

import importlib.util
spec = importlib.util.spec_from_file_location(
    "f3_prod",
    os.path.join(ANIMA_ROOT, "tool", "anima_holographic_ib_ksg_validate_prod.py"),
)
f3_prod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f3_prod)

import numpy as np
from scipy import stats as sp_stats


N_LEVELS = [200, 500, 1000, 2000, 5000]
COUPLING = 1.0
DIM = 4
K_NEIGHBORS = 3
SEED = 20260428


def stouffer_z_from_p(p_value: float, n_perms: int) -> float:
    """One-sided Stouffer z from p-value.

    Uses inverse-normal: z = Phi^-1(1 - p). Floor p at 1/(2*n_perms+2) to
    avoid -inf at p=0 (permutation test minimum resolvable p).
    """
    p_floor = 1.0 / (2.0 * n_perms + 2.0)
    p_eff = max(p_value, p_floor)
    return float(sp_stats.norm.ppf(1.0 - p_eff))


def main():
    out = {
        "tool": "f3_n_convergence_sweep_driver",
        "ts_start": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "config": {
            "coupling": COUPLING,
            "dim_x": DIM,
            "dim_y": DIM,
            "k_neighbors": K_NEIGHBORS,
            "seed": SEED,
            "n_levels": N_LEVELS,
            "perms_rule": "perms = N / 4",
        },
        "raw9_relaxation_tag": f3_prod.RAW9_RELAXATION_TAG,
        "raw91_C3_disclosure": "scope narrow measurement-statistics-only; CPU $0; mac jetsam single-thread",
        "patch_commit": "a0bcfd99",
        "results": [],
    }

    for n in N_LEVELS:
        perms = n // 4
        t0 = time.perf_counter()
        r = f3_prod.run(
            n_samples=n,
            n_permutations=perms,
            dim_x=DIM,
            dim_y=DIM,
            coupling=COUPLING,
            k_neighbors=K_NEIGHBORS,
            seed=SEED,
        )
        t1 = time.perf_counter()
        wallclock = t1 - t0
        p = r["result"]["p_value"]
        d = r["result"]["cohen_d"]
        obs = r["result"]["obs_mi"]
        nm = r["result"]["perm_mi_mean"]
        ns = r["result"]["perm_mi_std"]
        z = stouffer_z_from_p(p, perms)
        row = {
            "n": n,
            "perms": perms,
            "p_value": p,
            "cohen_d": d,
            "stouffer_z": z,
            "obs_mi": obs,
            "perm_mi_mean": nm,
            "perm_mi_std": ns,
            "wallclock_s": wallclock,
            "verdict": r["verdict"],
        }
        out["results"].append(row)
        print(f"[N={n:5d} perms={perms:5d}] p={p:.6f} d={d:.4f} z={z:.4f} mi_obs={obs:.5f} wall={wallclock:.2f}s verdict={r['verdict']}", flush=True)

    # Variance analysis across N levels
    ps = np.array([row["p_value"] for row in out["results"]])
    ds = np.array([row["cohen_d"] for row in out["results"]])
    zs = np.array([row["stouffer_z"] for row in out["results"]])
    mis = np.array([row["obs_mi"] for row in out["results"]])

    out["variance_analysis"] = {
        "p_value_mean": float(ps.mean()),
        "p_value_var": float(ps.var(ddof=1)),
        "p_value_std": float(ps.std(ddof=1)),
        "cohen_d_mean": float(ds.mean()),
        "cohen_d_var": float(ds.var(ddof=1)),
        "cohen_d_std": float(ds.std(ddof=1)),
        "stouffer_z_mean": float(zs.mean()),
        "stouffer_z_var": float(zs.var(ddof=1)),
        "stouffer_z_std": float(zs.std(ddof=1)),
        "obs_mi_mean": float(mis.mean()),
        "obs_mi_var": float(mis.var(ddof=1)),
        "obs_mi_std": float(mis.std(ddof=1)),
    }

    # Convergence point N*: smallest N at which the SUFFIX (N..N_max) running
    # variance < 1% of suffix-mean for ALL three metrics (cohen_d, stouffer_z, obs_mi).
    # p_value is excluded from convergence test because it floors at 0 (permutation
    # test minimum resolvable) — it converged trivially at N=200 in this regime.
    convergence_n = None
    convergence_details = []
    for i, row in enumerate(out["results"]):
        suffix_d = ds[i:]
        suffix_z = zs[i:]
        suffix_mi = mis[i:]
        if suffix_d.size < 2:
            continue
        d_var = float(suffix_d.var(ddof=1))
        d_mean_abs = float(abs(suffix_d.mean()))
        z_var = float(suffix_z.var(ddof=1))
        z_mean_abs = float(abs(suffix_z.mean()))
        mi_var = float(suffix_mi.var(ddof=1))
        mi_mean_abs = float(abs(suffix_mi.mean()))
        d_ratio = d_var / d_mean_abs if d_mean_abs > 0 else float("inf")
        z_ratio = z_var / z_mean_abs if z_mean_abs > 0 else float("inf")
        mi_ratio = mi_var / mi_mean_abs if mi_mean_abs > 0 else float("inf")
        detail = {
            "from_n": row["n"],
            "suffix_size": int(suffix_d.size),
            "cohen_d_var_over_mean": d_ratio,
            "stouffer_z_var_over_mean": z_ratio,
            "obs_mi_var_over_mean": mi_ratio,
            "all_under_1pct": (d_ratio < 0.01) and (z_ratio < 0.01) and (mi_ratio < 0.01),
        }
        convergence_details.append(detail)
        if detail["all_under_1pct"] and convergence_n is None:
            convergence_n = row["n"]

    out["convergence"] = {
        "criterion": "suffix-variance(metric) / |suffix-mean(metric)| < 0.01 for cohen_d AND stouffer_z AND obs_mi",
        "n_star": convergence_n,
        "converged": convergence_n is not None,
        "details": convergence_details,
    }

    out["mathematical_limit"] = {
        "asymptotic_obs_mi": float(mis[-1]),
        "asymptotic_cohen_d": float(ds[-1]),
        "asymptotic_stouffer_z": float(zs[-1]),
        "p_value_at_largest_N": float(ps[-1]),
        "p_value_floor_at_largest_N": 1.0 / (2.0 * out["results"][-1]["perms"] + 2.0),
        "noise_floor_perm_mi_std_at_largest_N": float(out["results"][-1]["perm_mi_std"]),
        "interpretation": (
            "obs_mi -> true coupling-1.0 MI asymptote; perm_mi_std -> 0 as N -> inf "
            "(null distribution variance shrinks); cohen_d = (obs - null_mean) / null_std "
            "-> inf in true asymptote, but bounded by KSG estimator finite-sample bias. "
            "Stouffer z bounded above by Phi^-1(1 - 1/(2*perms+2)) due to permutation p floor."
        ),
    }

    out["ts_end"] = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_wall = sum(row["wallclock_s"] for row in out["results"])
    out["total_wallclock_s"] = total_wall

    out_path = os.path.join(ANIMA_ROOT, "state", "f3_n_convergence_test", "verdict.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[WRITE] {out_path}")
    print(f"[TOTAL] wallclock={total_wall:.1f}s convergence_N*={convergence_n}")


if __name__ == "__main__":
    main()
