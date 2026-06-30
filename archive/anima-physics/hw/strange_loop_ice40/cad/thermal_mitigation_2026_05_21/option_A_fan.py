#!/usr/bin/env python3
# option_A_fan.py — UPduino enclosure thermal FEM with forced-air cooling.
#
# MITIGATION (Option A — 40 mm DC axial fan blowing on cover plate):
#   ONLY change vs baseline `upduino_enclosure_fem.py` =
#       h_convection: 10 → 50 W/m²K (5× textbook forced-air on Al).
#   All other physics / geometry / mesh schedule identical.
#
# Physics rationale:
#   Convection-limited Biot regime (Bi ≈ k_si·h/L ≈ 6e-5 ≪ 1) means
#   ΔT_max ≈ q_total / (h · A_top). Multiplying h by 5 reduces ΔT
#   linearly by 5:
#       ΔT_baseline = 60.61 K (h=10)
#       ΔT_predicted ≈ 60.61 / 5 = 12.12 K (h=50)
#   T_max @ T_amb=293.15 K → 305.27 K = 32.12 °C, headroom 52.88 °C.
#
# BOM: $5 Noctua-class 40 mm 5 V axial fan + JST-XH harness.
#
# 1D analytic cross-check:
#   ΔT_through_wall = q · t / k = 606.06 · 1e-3 / 167 = 3.63 mK
#   ΔT_robin = q / h = 606.06 / 50 = 12.121 K
#   ΔT_total_analytic ≈ 12.125 K
#
# CLI: python3.14 option_A_fan.py <out_dir> [<step_path>]
#
# Author: anima FPGA Phase 1c (thermal mitigation cycle, G5 scope_caveat #3)
# Date  : 2026-05-21

import os
import sys

# Reuse base script helpers (it lives in the parent cad/ dir).
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_BASE_DIR = os.path.dirname(_THIS_DIR)
if _BASE_DIR not in sys.path:
    sys.path.insert(0, _BASE_DIR)

import upduino_enclosure_fem as base  # noqa: E402


# ------------------------------------------------------------------
# ONLY mutation vs baseline: bump h_convection 10 → 50 W/m²K.
# ------------------------------------------------------------------
MITIGATION = {
    "option_id": "A_fan",
    "option_name": "40 mm DC axial fan, forced convection",
    "h_baseline_w_per_m2k": 10.0,
    "h_eff_w_per_m2k": 50.0,
    "h_multiplier": 5.0,
    "bom_usd_estimated": 5.0,
    "bom_items": ["40 mm 5 V axial fan", "JST-XH harness"],
    "geometry_change": "none (cover plate unchanged)",
    "physics_change": "h_top: 10 → 50 W/m²K (Robin coeff only)",
    "predicted_delta_t_k": 12.12,
}

base.LOAD["h_convection_w_per_m2k"] = MITIGATION["h_eff_w_per_m2k"]


def analytic_delta_t() -> dict:
    """1D analytic ΔT_max for the forced-air sink case.

    Cover plate is a thin Al slab with uniform-flux Neumann on the
    bottom and Robin on the top. In the convection-limited regime
    (Bi ≪ 1) the analytic peak-to-ambient temperature rise is:
        ΔT = q · t / k_si           (through-wall conduction)
           + q / h                  (Newton convection film drop)
    where q = P_total / A_top.
    """
    bottom_area = base.COVER["length_m"] * base.COVER["width_m"]
    q = base.LOAD["total_power_w"] / bottom_area
    dt_wall = q * base.COVER["thickness_m"] / base.MATERIAL["k_w_per_mk"]
    dt_robin = q / MITIGATION["h_eff_w_per_m2k"]
    return {
        "q_flux_w_per_m2": q,
        "delta_t_wall_k": dt_wall,
        "delta_t_robin_k": dt_robin,
        "delta_t_total_k": dt_wall + dt_robin,
    }


def main(argv):
    rc = base.main(argv)
    if rc != 0:
        return rc

    # The base.main wrote upduino_enclosure_thermal_<UTC>.json into
    # out_dir; tag it with our mitigation metadata + analytic check.
    import glob
    import json

    out_dir = argv[1]
    records = sorted(glob.glob(
        os.path.join(out_dir, "upduino_enclosure_thermal_*.json")))
    if not records:
        sys.stderr.write("option_A_fan: no record file produced\n")
        return 3
    rec_path = records[-1]

    with open(rec_path, "r") as f:
        meta = json.load(f)

    analytic = analytic_delta_t()
    delta_t_fem = meta["measurements"]["thermal"]["delta_t_k"]
    rel_err = (
        abs(delta_t_fem - analytic["delta_t_total_k"])
        / analytic["delta_t_total_k"])
    t_amb_c = base.LOAD["t_ambient_k"] - 273.15
    t_max_c = meta["measurements"]["thermal"]["t_max_k"] - 273.15
    headroom_c = 85.0 - t_max_c  # iCE40UP5K T_j max = 85 °C

    meta["mitigation"] = MITIGATION
    meta["analytic_1d"] = analytic
    meta["analytic_rel_err"] = rel_err
    meta["thermal_budget"] = {
        "t_ambient_c": t_amb_c,
        "t_max_c": t_max_c,
        "t_j_max_c_iCE40UP5K": 85.0,
        "headroom_c": headroom_c,
        "delta_t_k_fem": delta_t_fem,
    }
    out_path = os.path.join(out_dir, "option_A_fan.json")
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=2, sort_keys=True)

    # Copy mesh_convergence.csv → option_A_fan.csv for record-naming
    # parity with the task spec.
    import shutil
    src_csv = os.path.join(out_dir, "mesh_convergence.csv")
    dst_csv = os.path.join(out_dir, "option_A_fan.csv")
    if os.path.isfile(src_csv):
        shutil.copy(src_csv, dst_csv)

    summary = {
        "ok": True,
        "option": MITIGATION["option_id"],
        "h_eff_w_per_m2k": MITIGATION["h_eff_w_per_m2k"],
        "delta_t_k_fem": delta_t_fem,
        "delta_t_k_analytic": analytic["delta_t_total_k"],
        "analytic_rel_err": rel_err,
        "t_max_c": t_max_c,
        "headroom_c": headroom_c,
        "bom_usd": MITIGATION["bom_usd_estimated"],
    }
    sys.stderr.write(
        "OPTION_A_FAN_RESULT " + json.dumps(summary) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
