#!/usr/bin/env python3
# vibration_fem.py — UPduino enclosure mechanical-shock FEM (Part A
# of G5 scope_caveat #3 multi-load FEM closure).
#
# LOAD CASE: half-sine shock 50 g · 11 ms (drop-test 1 m) applied
# as a quasi-static equivalent-acceleration body force on the
# 50×33×1 mm Al cover plate (mass ≈ 4.45 g, peak inertial reaction
# F = m · 50 g ≈ 2.18 N spread as a body force ρ · a). The dynamic
# half-sine raises the equivalent quasi-static load by a Dynamic
# Amplification Factor (DAF, 1.0–2.0 depending on shock-pulse vs
# 1st-mode period ratio); we use the conservative DAF = 1.5 from
# MIL-STD-810G §516.6 short-duration shock guidance.
#
# Clamp: 4 corner mounting screws (φ 3 mm pads, simulated as
# Dirichlet u=0 on a 1.5 mm radius around each corner of the
# bottom face). This is the standard PCB enclosure boundary
# condition (cf. ASTM D3580 random vibration fixture).
#
# OUTPUT:
#   σ_vM_max        — peak von Mises stress (Pa)
#   u_max           — peak nodal displacement (m)
#   FoS_yield       — 276 MPa / σ_vM_max  (Al 6061-T6 σy)
#   FoS_ultimate    — 310 MPa / σ_vM_max  (Al 6061-T6 σu)
#
# ANALYTIC CROSS-CHECK (cantilever plate centre, simply supported
# at 4 corners):
#   q  = ρ · h · a_eff  (uniform load N/m²)
#   σ  ≈ 0.5 · q · b² / h²  (max plate bending stress, b = short side)
#   u  ≈ α · q · b⁴ / (E · h³)   (Roark, α≈0.0138 for SSSS plate)
#
# Author: anima FPGA Phase 1c (multi-load FEM, G5 scope_caveat #3
# Part A)
# Date  : 2026-05-21

import json
import math
import os
import sys
import time
from datetime import datetime, timezone

_USER_SITE = os.path.expanduser(
    f"~/Library/Python/{sys.version_info.major}.{sys.version_info.minor}"
    "/lib/python/site-packages")
if os.path.isdir(_USER_SITE) and _USER_SITE not in sys.path:
    sys.path.insert(0, _USER_SITE)

_KERNEL_DIR = os.path.expanduser("~/core/hexa-lang/stdlib/kernels/fem")
if _KERNEL_DIR not in sys.path:
    sys.path.insert(0, _KERNEL_DIR)
import skfem_kernel  # noqa: E402

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BASE_DIR not in sys.path:
    sys.path.insert(0, _BASE_DIR)
import upduino_enclosure_fem as base  # noqa: E402


# ------------------------------------------------------------------
# Shock load spec — MIL-STD-810G §516.6 half-sine, 50 g · 11 ms
# (corresponds to a 1 m drop onto a stiff floor).
# ------------------------------------------------------------------
SHOCK = {
    "peak_g": 50.0,
    "pulse_ms": 11.0,
    "shape": "half_sine",
    "dynamic_amp_factor": 1.5,          # DAF (MIL-STD-810G short pulse)
    "drop_height_m_equiv": 1.0,
}

_G = 9.80665                            # m/s²
_AL_YIELD_MPA = 276.0                   # Al 6061-T6 σ_y
_AL_ULT_MPA = 310.0                     # Al 6061-T6 σ_u


def shock_acceleration_si() -> float:
    """Effective quasi-static acceleration (m/s²) applied as body
    force. SHOCK['peak_g'] · DAF · g."""
    return SHOCK["peak_g"] * SHOCK["dynamic_amp_factor"] * _G


# ------------------------------------------------------------------
# Analytic cross-check: thin SSSS rectangular plate uniform load.
# (Timoshenko + Roark, Table 11.4 SSSS uniform.)
# ------------------------------------------------------------------
def analytic_plate() -> dict:
    L = base.COVER["length_m"]
    W = base.COVER["width_m"]
    h = base.COVER["thickness_m"]
    rho = base.MATERIAL["rho_kg_per_m3"]
    E = base.MATERIAL["youngs_pa"]
    nu = base.MATERIAL["poissons"]

    a_eff = shock_acceleration_si()
    # uniform pressure (Pa) from inertial body force per unit area
    q = rho * h * a_eff

    b = min(L, W)
    a = max(L, W)
    a_over_b = a / b

    # Roark Table 11.4 (SSSS uniform load on rectangle): β and α
    # interpolated at a/b ≈ 1.52 (50/33).
    #   a/b 1.0: β=0.2874, α=0.0444
    #   a/b 1.2: β=0.3762, α=0.0616
    #   a/b 1.4: β=0.4530, α=0.0770
    #   a/b 1.6: β=0.5172, α=0.0906
    #   a/b 1.8: β=0.5688, α=0.1017
    #   a/b 2.0: β=0.6102, α=0.1110
    # Linear interp at 1.52:
    beta = 0.4530 + (0.5172 - 0.4530) * (a_over_b - 1.4) / (1.6 - 1.4)
    alpha = 0.0770 + (0.0906 - 0.0770) * (a_over_b - 1.4) / (1.6 - 1.4)

    # Plate stiffness D = E·h³ / (12 (1-ν²))
    D = E * h ** 3 / (12.0 * (1.0 - nu ** 2))

    sigma_max = beta * q * b ** 2 / h ** 2
    u_max = alpha * q * b ** 4 / (E * h ** 3)
    return {
        "a_eff_m_per_s2": a_eff,
        "q_pa_inertial": q,
        "a_over_b": a_over_b,
        "beta_roark": beta,
        "alpha_roark": alpha,
        "plate_stiffness_D_nm": D,
        "sigma_max_pa": sigma_max,
        "u_max_m": u_max,
    }


# ------------------------------------------------------------------
# FEM: linear-elastic static body-force solve (equivalent quasi-
# static representation of the half-sine shock).
#
# Dirichlet (clamp) = 4 corner pads on the bottom face: |x - x_c| <
# 1.5 mm AND |y - y_c| < 1.5 mm AND z ≈ z_bottom for the 4 corners
# (x ∈ {0, L}, y ∈ {0, W}).
# ------------------------------------------------------------------
def solve_vibration(step_path: str, mesh_size_m: float,
                    out_dir: str) -> dict:
    meshed = skfem_kernel.mesh_from_step(
        out_dir, step_path,
        mesh_size_m=mesh_size_m,
        name=f"upduino_cover_vib_h{int(mesh_size_m*1e6)}um")
    mesh = meshed["mesh"]

    rho = base.MATERIAL["rho_kg_per_m3"]
    E = base.MATERIAL["youngs_pa"]
    nu = base.MATERIAL["poissons"]
    a_eff = shock_acceleration_si()

    # body force in N/m³ — z is the shock axis (drop direction); apply
    # as -ρ·a_eff in z so the plate bends downward.
    fz = -rho * a_eff
    body_force = (0.0, 0.0, fz)

    L = base.COVER["length_m"]
    W = base.COVER["width_m"]
    z_bottom = base.COVER["z_offset_m"]
    eps = 1.0e-4   # mounting-pad radius proxy (matches 1.5 mm pad)

    def corner_clamp(coords):
        """Pick nodes inside a 1.5 mm tab around each of the 4 corners
        on the bottom face (z ≈ z_bottom)."""
        import numpy as np
        x = coords[0]
        y = coords[1]
        z = coords[2]
        pad = 1.5e-3
        z_face = np.abs(z - z_bottom) < 5.0e-5
        c1 = (np.abs(x - 0.0) < pad) & (np.abs(y - 0.0) < pad)
        c2 = (np.abs(x - L) < pad) & (np.abs(y - 0.0) < pad)
        c3 = (np.abs(x - 0.0) < pad) & (np.abs(y - W) < pad)
        c4 = (np.abs(x - L) < pad) & (np.abs(y - W) < pad)
        return z_face & (c1 | c2 | c3 | c4)

    t0 = time.time()
    res = skfem_kernel.solve_elastic(
        mesh, E, nu, body_force, corner_clamp)
    wall = time.time() - t0

    res.update({
        "mesh_size_m": mesh_size_m,
        "n_nodes": meshed["n_nodes"],
        "n_elements": meshed["n_elements"],
        "a_eff_m_per_s2": a_eff,
        "body_force_n_per_m3_z": fz,
        "wall_s": wall,
    })
    return res


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(
            "usage: vibration_fem.py <out_dir> [<step_path>] "
            "[<mesh_size_m>]\n")
        return 2
    out_dir = argv[1]
    os.makedirs(out_dir, exist_ok=True)

    if len(argv) >= 3:
        step_path = argv[2]
    else:
        step_path = os.path.join(
            os.path.dirname(_BASE_DIR), "cad",
            "upduino_cover_plate.step")
    if not os.path.isfile(step_path):
        sys.stderr.write(
            f"vibration_fem: STEP not found: {step_path}\n")
        return 2

    mesh_size_m = float(argv[3]) if len(argv) >= 4 else 0.5e-3

    analytic = analytic_plate()
    fem = solve_vibration(step_path, mesh_size_m, out_dir)

    sigma_pa = fem["sigma_vm_max_pa"]
    sigma_mpa = sigma_pa / 1e6
    u_max_m = fem["u_max_m"]
    fos_yield = _AL_YIELD_MPA / sigma_mpa if sigma_mpa > 0 else float("inf")
    fos_ult = _AL_ULT_MPA / sigma_mpa if sigma_mpa > 0 else float("inf")

    # σ analytic vs FEM — both have honest scope (analytic = SSSS,
    # FEM = 4-corner clamp, so we expect FEM ≈ 1.5–3× analytic when
    # clamps tighten the bending).
    sigma_ratio = (
        sigma_pa / analytic["sigma_max_pa"]
        if analytic["sigma_max_pa"] > 0 else float("inf"))
    u_ratio = (
        u_max_m / analytic["u_max_m"]
        if analytic["u_max_m"] > 0 else float("inf"))

    iso = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    record = {
        "ok": True,
        "interface":
            "demiurge:component:gmsh-skfem-verify-record-multiload",
        "record_id": f"vibration_fem_{iso}",
        "analysis": "vibration_shock_static_equivalent",
        "geometry_id": "upduino_v3_enclosure_v1",
        "produced_at_utc": datetime.now(timezone.utc).isoformat(),
        "geometry": {
            "id": "upduino_v3_enclosure_v1",
            "length_m": base.COVER["length_m"],
            "width_m": base.COVER["width_m"],
            "thickness_m": base.COVER["thickness_m"],
            "mesh_size_m": mesh_size_m,
            "n_nodes": fem["n_nodes"],
            "n_elements": fem["n_elements"],
        },
        "material": base.MATERIAL,
        "load": SHOCK,
        "analytic_1d": analytic,
        "fem": {
            "sigma_vm_max_pa": sigma_pa,
            "sigma_vm_max_mpa": sigma_mpa,
            "u_max_m": u_max_m,
            "dof_count": fem["dof_count"],
            "wall_s": fem["wall_s"],
        },
        "cross_check": {
            "sigma_fem_over_analytic": sigma_ratio,
            "u_fem_over_analytic": u_ratio,
            "expected_ratio_range": "1.5..3.0 (4-corner clamp is "
            "stiffer than SSSS plate)",
        },
        "factor_of_safety": {
            "yield_mpa": _AL_YIELD_MPA,
            "ultimate_mpa": _AL_ULT_MPA,
            "fos_yield": fos_yield,
            "fos_ultimate": fos_ult,
            "pass_yield_FoS_gt_2": bool(fos_yield > 2.0),
            "pass_ultimate_FoS_gt_3": bool(fos_ult > 3.0),
        },
        "provenance": {
            "absorbed": False,
            "measurement_gate": "GATE_OPEN",
            "producer":
                "gmsh@4.15.2 + scikit-fem@12.0.1 "
                "(anima/multiload_2026_05_21/vibration_fem.py)",
            "scope_caveats": [
                "static-equivalent representation of the half-sine "
                "shock pulse via DAF=1.5 (MIL-STD-810G §516.6); a "
                "true modal-superposition transient solve was NOT "
                "performed and would refine σ_vM by ~10-30 % "
                "depending on 1st-mode period vs 11 ms pulse.",
                "4-corner clamp idealised as 1.5 mm pads with rigid "
                "u=0 — real M3 screw+washer has finite stiffness, "
                "would soften σ_vM near the pads by ~20 %.",
                "Al 6061-T6 σ_y/σ_u = 276/310 MPa = MMPDS textbook "
                "values, NOT a lot-tested coupon. Heat-affected zone "
                "near welds (none on this part) would drop σ_y to "
                "~165 MPa.",
            ],
        },
        "error": None,
    }

    rec_path = os.path.join(out_dir, "vibration_fem.json")
    with open(rec_path, "w") as f:
        json.dump(record, f, indent=2, sort_keys=True)

    summary = {
        "ok": True,
        "analysis": "vibration_shock",
        "sigma_vm_max_mpa": sigma_mpa,
        "u_max_m": u_max_m,
        "fos_yield": fos_yield,
        "fos_ultimate": fos_ult,
        "analytic_sigma_max_mpa": analytic["sigma_max_pa"] / 1e6,
        "analytic_u_max_m": analytic["u_max_m"],
        "sigma_fem_over_analytic": sigma_ratio,
        "u_fem_over_analytic": u_ratio,
        "n_nodes": fem["n_nodes"],
        "n_elements": fem["n_elements"],
        "wall_s": fem["wall_s"],
        "record": rec_path,
    }
    sys.stderr.write("VIBRATION_FEM_RESULT " + json.dumps(summary) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
