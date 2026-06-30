#!/usr/bin/env python3
# option_C_padcase.py — UPduino enclosure thermal FEM with thermal pad
# + Al outer case (two-stage chip-case-amb sink, NO fan).
#
# MITIGATION (Option C — Bergquist Sil-Pad thermal pad bonded to chip
# top, drained via Al outer enclosure case 100 × 80 × 25 mm × 1.5 mm):
#
#   Two thermal resistances in series:
#     R1 = pad through-thickness conduction (chip → case inner wall)
#     R2 = case outer-surface free convection (case wall → ambient)
#
#   Pad parameters (Bergquist Sil-Pad 900S, typical):
#     k_pad = 1.6 W/m·K
#     t_pad = 1.0 mm
#     A_pad = 5 × 5 mm² (full FPGA BGA footprint)
#     R1 = t_pad / (k_pad · A_pad) = 1e-3 / (1.6 · 25e-6)
#         = 25.0 K/W
#     ΔT_pad @ 1 W = 25.0 K   ← dominant resistance
#
#   Case parameters (Hammond 1455T1601 class, 100×80×25 mm, 1.5 mm Al):
#     A_case_outer = 2·(0.10·0.08) + 2·(0.10·0.025) + 2·(0.08·0.025)
#                  = 0.016 + 0.005 + 0.004 = 0.025 m² (16 000 + 5 000
#                  + 4 000 mm² = 25 000 mm²)
#     h_case (free conv, full enclosure mix horizontal+vertical)
#                  = 8 W/m²K (slightly lower than top-only plate)
#     R_conv_case = 1 / (h · A) = 1 / (8 · 0.025) = 5.0 K/W
#     ΔT_case-amb @ 1 W = 5.0 K
#
#   Through-cover thermal-spread resistance (very low for Al, 1.5 mm):
#     ΔT_cover ≈ q · t / k = (1.0 / 0.025) · 1.5e-3 / 167 ≈ 0.36 mK
#     (negligible.)
#
#   Total ΔT_chip-to-amb ≈ ΔT_pad + ΔT_cover + ΔT_case-amb
#                        ≈ 25.0 + 0.0 + 5.0 ≈ 30.0 K
#   T_max @ T_amb=20 °C → 50 °C, headroom 35 °C.
#
#   FEM domain: SAME cover-plate FEM (51 LOC reuse) reused to verify
#   the CASE leg only (h_case=8, A_case=0.025 m²). Lumped via:
#     1) reuse cover plate geometry (FEM-meshable).
#     2) override h_eff so that the FEM Robin product (h · A_top)
#        matches (h_case · A_case_outer) — i.e. h_lumped =
#        h_case · A_case_outer / A_top = 8 · 0.025 / 1.65e-3 = 121.2.
#     3) FEM-reported ΔT then = case-convection film drop only;
#        we ADD the pad resistance (25 K) analytically.
#
# Honest C3: Option C's physics is dominated by the thermal-pad film
# (R1=25 K/W, 83 % of total), NOT by the cover-plate FEM. The FEM is
# included for symmetry with Options A/B; a true Option C model needs
# either (a) explicit pad + chip + case multi-body FEM or (b) lumped
# Rth network. We do (b) and use the cover FEM only as a sanity check
# on the case-conv resistance.
#
# CLI: python3.14 option_C_padcase.py <out_dir> [<step_path>]
#
# Author: anima FPGA Phase 1c (thermal mitigation cycle, G5 scope_caveat #3)
# Date  : 2026-05-21

import os
import sys

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_BASE_DIR = os.path.dirname(_THIS_DIR)
if _BASE_DIR not in sys.path:
    sys.path.insert(0, _BASE_DIR)

import upduino_enclosure_fem as base  # noqa: E402


# ------------------------------------------------------------------
# Pad + case parameters.
# ------------------------------------------------------------------
PAD = {
    "vendor_pn": "Bergquist Sil-Pad 900S (or eq.)",
    "k_pad_w_per_mk": 1.6,
    "thickness_m": 1.0e-3,
    "area_m2": 5.0e-3 * 5.0e-3,        # 5 × 5 mm² FPGA BGA top
}
CASE = {
    "vendor_pn": "Hammond 1455T1601 (or eq.) 100×80×25 mm Al case",
    "length_m": 100.0e-3,
    "width_m":   80.0e-3,
    "height_m":  25.0e-3,
    "thickness_m": 1.5e-3,
    "k_case_w_per_mk": 167.0,
    "h_outer_w_per_m2k": 8.0,           # free conv mixed orientation
}


def _case_area() -> float:
    L, W, H = CASE["length_m"], CASE["width_m"], CASE["height_m"]
    return 2.0 * (L * W) + 2.0 * (L * H) + 2.0 * (W * H)


def lumped_rth_network() -> dict:
    """Lumped Rth (chip → ambient) for the pad + case network."""
    P = base.LOAD["total_power_w"]
    A_pad = PAD["area_m2"]
    R_pad = PAD["thickness_m"] / (PAD["k_pad_w_per_mk"] * A_pad)

    A_case = _case_area()
    R_conv_case = 1.0 / (CASE["h_outer_w_per_m2k"] * A_case)

    # cover plate through-cover ΔT (q_case = P / A_case):
    q_case = P / A_case
    dt_cover = (q_case * CASE["thickness_m"]
                / CASE["k_case_w_per_mk"])

    dt_pad = R_pad * P
    dt_case_amb = R_conv_case * P
    dt_total = dt_pad + dt_cover + dt_case_amb

    return {
        "P_w": P,
        "A_pad_m2": A_pad,
        "A_case_outer_m2": A_case,
        "R_pad_k_per_w": R_pad,
        "R_conv_case_k_per_w": R_conv_case,
        "delta_t_pad_k": dt_pad,
        "delta_t_cover_k": dt_cover,
        "delta_t_case_amb_k": dt_case_amb,
        "delta_t_total_k": dt_total,
    }


_NET = lumped_rth_network()

# FEM lumping: pick h_lumped so that h_lumped * A_cover_plate equals
# h_case * A_case_outer. The cover-plate FEM then yields the
# case-convection film drop only (excluding the pad).
_A_TOP_COVER = base.COVER["length_m"] * base.COVER["width_m"]
_H_LUMPED = (
    CASE["h_outer_w_per_m2k"] * _NET["A_case_outer_m2"] / _A_TOP_COVER)

MITIGATION = {
    "option_id": "C_padcase",
    "option_name":
        "Bergquist Sil-Pad + Hammond 100×80×25 mm Al enclosure case",
    "h_baseline_w_per_m2k": 10.0,
    "h_eff_w_per_m2k": _H_LUMPED,        # FEM-equivalent only
    "h_multiplier": _H_LUMPED / 10.0,
    "bom_usd_estimated": 2.0,            # pad alone; case ~$15 separate
    "bom_items": [
        "Bergquist Sil-Pad 900S, 25 × 25 mm cut",
        "(case = +$15 separate, not in this row)",
    ],
    "geometry_change":
        "physical chip → pad → case Rth network; FEM only validates "
        "case-convection leg via lumped h",
    "physics_change":
        f"R_pad={_NET['R_pad_k_per_w']:.2f} K/W (dominant); "
        f"R_conv_case={_NET['R_conv_case_k_per_w']:.3f} K/W; "
        f"h_lumped_FEM={_H_LUMPED:.2f} W/m²K",
    "pad_geometry": PAD,
    "case_geometry": CASE,
    "rth_network": _NET,
    "predicted_delta_t_k": _NET["delta_t_total_k"],
}

base.LOAD["h_convection_w_per_m2k"] = _H_LUMPED


def analytic_delta_t() -> dict:
    """1D analytic ΔT_max for the lumped case-convection FEM run
    (pad ΔT added back separately in the report)."""
    bottom_area = base.COVER["length_m"] * base.COVER["width_m"]
    q = base.LOAD["total_power_w"] / bottom_area
    dt_wall = q * base.COVER["thickness_m"] / base.MATERIAL["k_w_per_mk"]
    dt_robin = q / _H_LUMPED
    return {
        "q_flux_w_per_m2": q,
        "delta_t_wall_k": dt_wall,
        "delta_t_robin_k": dt_robin,
        "delta_t_total_k_fem_only": dt_wall + dt_robin,
        "delta_t_pad_k": _NET["delta_t_pad_k"],
        "delta_t_total_k_with_pad": (
            dt_wall + dt_robin + _NET["delta_t_pad_k"]),
    }


def main(argv):
    rc = base.main(argv)
    if rc != 0:
        return rc

    import glob
    import json
    import shutil

    out_dir = argv[1]
    records = sorted(glob.glob(
        os.path.join(out_dir, "upduino_enclosure_thermal_*.json")))
    if not records:
        sys.stderr.write("option_C_padcase: no record file produced\n")
        return 3
    rec_path = records[-1]

    with open(rec_path, "r") as f:
        meta = json.load(f)

    analytic = analytic_delta_t()
    delta_t_fem = meta["measurements"]["thermal"]["delta_t_k"]
    # add pad analytically
    delta_t_total = delta_t_fem + _NET["delta_t_pad_k"]
    t_max_k_total = base.LOAD["t_ambient_k"] + delta_t_total
    t_max_c = t_max_k_total - 273.15
    headroom_c = 85.0 - t_max_c

    rel_err = (
        abs(delta_t_fem - analytic["delta_t_total_k_fem_only"])
        / analytic["delta_t_total_k_fem_only"])

    meta["mitigation"] = MITIGATION
    meta["analytic_1d"] = analytic
    meta["analytic_rel_err"] = rel_err
    meta["thermal_budget"] = {
        "t_ambient_c": base.LOAD["t_ambient_k"] - 273.15,
        "delta_t_k_fem_case_leg": delta_t_fem,
        "delta_t_k_pad_lumped":   _NET["delta_t_pad_k"],
        "delta_t_k_total":        delta_t_total,
        "t_max_c":                t_max_c,
        "t_j_max_c_iCE40UP5K":    85.0,
        "headroom_c":             headroom_c,
    }
    out_path = os.path.join(out_dir, "option_C_padcase.json")
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=2, sort_keys=True)

    src_csv = os.path.join(out_dir, "mesh_convergence.csv")
    dst_csv = os.path.join(out_dir, "option_C_padcase.csv")
    if os.path.isfile(src_csv):
        shutil.copy(src_csv, dst_csv)

    summary = {
        "ok": True,
        "option": MITIGATION["option_id"],
        "h_lumped_w_per_m2k": _H_LUMPED,
        "R_pad_k_per_w": _NET["R_pad_k_per_w"],
        "R_conv_case_k_per_w": _NET["R_conv_case_k_per_w"],
        "delta_t_k_pad": _NET["delta_t_pad_k"],
        "delta_t_k_fem_case_leg": delta_t_fem,
        "delta_t_k_total": delta_t_total,
        "delta_t_k_analytic_total":
            analytic["delta_t_total_k_with_pad"],
        "analytic_rel_err_fem_leg": rel_err,
        "t_max_c": t_max_c,
        "headroom_c": headroom_c,
        "bom_usd": MITIGATION["bom_usd_estimated"],
    }
    sys.stderr.write(
        "OPTION_C_PADCASE_RESULT " + json.dumps(summary) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
