#!/usr/bin/env python3
# upduino_enclosure_fem.py — anima FPGA UPduino v3 enclosure thermal FEM.
#
# Phase 1b real-component handoff (G5 demiurge component cell):
# loads the STEP geometry produced by `upduino_enclosure.py`, meshes
# the aluminium cover plate via gmsh, and runs a steady-state heat
# conduction solve via scikit-fem (the same ①a kernel
# `~/core/hexa-lang/stdlib/kernels/fem/skfem_kernel.py` that the
# `component + verify` toy-box producer uses — domain switches but
# the kernel does not).
#
# PHYSICS
#   Domain  : 50 × 33 × 1 mm Al cover plate (single body).
#   Source  : PCB heat flux on the cover-plate BOTTOM face only — the
#             5x5 mm² iCE40UP5K BGA footprint at the plate centre and
#             a 3x3 mm² LDO footprint 10 mm off-centre, total 1 W
#             (FPGA 0.5 W + LDO 0.5 W datasheet estimate). Applied as
#             a Neumann boundary heat flux on the matching patches of
#             the bottom face (z = z_offset).
#             *Domain-honest detail*: we approximate the BGA + LDO
#             footprints as a single uniform Neumann patch over the
#             whole bottom face — see scope_caveats.
#   Cooling : Newton convection on the TOP face only (h = 10 W/m²K,
#             T_ambient = 293.15 K). Implemented as a Robin BC, which
#             scikit-fem assembles as a boundary bilinear form +
#             Neumann load (k ∂T/∂n + h (T - T_amb) = 0 → h T_amb
#             on the load side, h on the bilinear side).
#   Sides   : insulated (zero flux).
#
# MESH CONVERGENCE
#   4 mesh levels (h = 1.5, 1.0, 0.7, 0.5 mm target tet edge).
#   Convergence metric: |ΔT_max_{n+1} − ΔT_max_n| < 0.1 K.
#   Reports the full sweep (csv table) and the converged ΔT_max.
#
# OUTPUT (into out_dir)
#   upduino_enclosure_thermal_<UTC>.json   — full record (demiurge-
#       compatible schema = mirror of component-verify gmsh-skfem
#       record but with geometry="upduino_v3_enclosure_v1").
#   mesh_convergence.csv                   — 4-row sweep table.
#   step.brep / step.stl                   — copies of the input
#       geometry for record self-containment.
#
# HONESTY (g3) — non-negotiable:
#   * Material constants (Al 6061 k=167 W/m·K, ρ=2700 kg/m³) are
#     CRC Handbook / AZoM textbook values, NOT a measured lot.
#   * Heat sources (FPGA 0.5 W, LDO 0.5 W) are datasheet
#     ESTIMATES (iCE40UP5K typ. dynamic power at 12 MHz ≈ 5-20 mW
#     idle to ~100 mW peak per logic block, AP2112K LDO worst-case
#     1.0 V drop × 0.5 A = 0.5 W). NO bench measurement.
#   * Convection h = 10 W/m²K is a textbook free-convection
#     coefficient for vertical Al at room temp, NOT a wind-tunnel
#     measurement.
#   * Source footprint is approximated as a uniform bottom-face
#     Neumann patch — true BGA/LDO localisation NOT modelled at
#     this enclosure-level scale.
#   * Single load case (steady-state) — transient + structural +
#     thermomechanical coupling NOT modelled.
#   * measurement_gate = GATE_OPEN, absorbed = false — same as
#     the toy-box producer. Upgrading to GATE_CLOSED requires
#     measured BOM, fabricated enclosure, wind-tunnel / IR
#     camera bench data + 3rd-party FEM cross-check (Code_Aster
#     or Elmer FEM).
#
# CLI
#   python3 upduino_enclosure_fem.py <output_dir> [<step_path>]
#       Default <step_path> = the sibling upduino_cover_plate.step.
#
# Author: anima FPGA Phase 1b (G5 demiurge component handoff)
# Date  : 2026-05-21

import csv
import hashlib
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone

# Inject macOS pip --user --break-system-packages path.
_USER_SITE = os.path.expanduser(
    f"~/Library/Python/{sys.version_info.major}.{sys.version_info.minor}"
    "/lib/python/site-packages")
if os.path.isdir(_USER_SITE) and _USER_SITE not in sys.path:
    sys.path.insert(0, _USER_SITE)

# Bring in the absorbed ①a FEM kernel (domain-agnostic). The toy-box
# `component + verify` producer uses the same import — we reuse rather
# than fork.
_KERNEL_DIR = os.path.expanduser(
    "~/core/hexa-lang/stdlib/kernels/fem")
if _KERNEL_DIR not in sys.path:
    sys.path.insert(0, _KERNEL_DIR)
import skfem_kernel  # noqa: E402


# ------------------------------------------------------------------
# Material + load + cooling constants — DOMAIN data (this adapter
# owns these, not the kernel).
# ------------------------------------------------------------------
MATERIAL = {
    "name": "aluminium 6061-T6 (textbook 300 K)",
    "k_w_per_mk": 167.0,
    "rho_kg_per_m3": 2700.0,
    "youngs_pa": 68.9e9,
    "poissons": 0.33,
}

LOAD = {
    "fpga_power_w": 0.5,       # iCE40UP5K typical
    "ldo_power_w":  0.5,       # AP2112K worst-case
    "total_power_w": 1.0,
    "t_ambient_k": 293.15,     # 20 °C
    "h_convection_w_per_m2k": 10.0,   # free convection on Al at RT
}

# Mesh convergence schedule (target tet edge size, METRES).
MESH_LEVELS = [1.5e-3, 1.0e-3, 0.7e-3, 0.5e-3]

# Cover plate geometry — match upduino_enclosure.py constants.
COVER = {
    "length_m":    50.0e-3,
    "width_m":     33.0e-3,
    "thickness_m":  1.0e-3,
    "z_offset_m":  11.0e-3,
}


# ------------------------------------------------------------------
# Single thermal solve on a STEP-meshed cover plate with Robin BC
# (convection on the top face) + Neumann heat flux on the bottom
# face. Returns the temperature field summary.
# ------------------------------------------------------------------
def solve_one_level(step_path: str, mesh_size_m: float,
                    out_dir: str, level_idx: int) -> dict:
    import numpy as np
    import skfem
    from skfem import (Basis, ElementTetP1, BilinearForm, LinearForm,
                       FacetBasis, asm, condense, solve)
    from skfem.helpers import dot, grad

    # 1. mesh the STEP via the kernel's helper.
    meshed = skfem_kernel.mesh_from_step(
        out_dir, step_path,
        mesh_size_m=mesh_size_m,
        name=f"upduino_cover_lvl{level_idx}")
    mesh = meshed["mesh"]
    n_nodes = meshed["n_nodes"]
    n_elements = meshed["n_elements"]
    gver = meshed["gmsh_version"]

    # 2. compute the heat-flux density on the bottom face.
    #    Total power 1.0 W spread over the cover plate bottom face
    #    area (L × W = 0.05 × 0.033 = 1.65e-3 m²).
    bottom_area = COVER["length_m"] * COVER["width_m"]
    q_flux_w_per_m2 = LOAD["total_power_w"] / bottom_area
    z_bottom = COVER["z_offset_m"]
    z_top = COVER["z_offset_m"] + COVER["thickness_m"]
    eps = 1.0e-7

    # 3. assemble.
    basis = Basis(mesh, ElementTetP1())
    k_si = MATERIAL["k_w_per_mk"]

    @BilinearForm
    def conduction(u, v, w):
        return k_si * dot(grad(u), grad(v))

    K = asm(conduction, basis)

    # Robin convection BC on top face: adds h to the bilinear form
    # AND h*T_amb to the load (residual: k ∂T/∂n = h (T_amb - T)).
    top_facets = mesh.facets_satisfying(
        lambda x: x[2] > z_top - eps)
    top_basis = FacetBasis(mesh, ElementTetP1(),
                           facets=top_facets)
    h = LOAD["h_convection_w_per_m2k"]
    t_amb = LOAD["t_ambient_k"]

    @BilinearForm
    def convection_form(u, v, w):
        return h * u * v

    @LinearForm
    def convection_load(v, w):
        return h * t_amb * v

    K += asm(convection_form, top_basis)
    f_conv = asm(convection_load, top_basis)

    # Neumann heat flux on bottom face: load = q * v.
    bottom_facets = mesh.facets_satisfying(
        lambda x: x[2] < z_bottom + eps)
    bottom_basis = FacetBasis(mesh, ElementTetP1(),
                              facets=bottom_facets)

    @LinearForm
    def flux_load(v, w):
        return q_flux_w_per_m2 * v

    f_flux = asm(flux_load, bottom_basis)

    f = f_conv + f_flux

    # No Dirichlet BCs — Robin convection grounds the system. Solve.
    x = solve(K, f)

    t_min = float(np.min(x))
    t_max = float(np.max(x))
    t_mean = float(np.mean(x))
    delta_t = t_max - LOAD["t_ambient_k"]

    return {
        "level_idx": level_idx,
        "mesh_size_m": mesh_size_m,
        "n_nodes": n_nodes,
        "n_elements": n_elements,
        "t_min_k": t_min,
        "t_max_k": t_max,
        "t_mean_k": t_mean,
        "delta_t_k": delta_t,
        "q_flux_w_per_m2": q_flux_w_per_m2,
        "msh_path": meshed["msh_path"],
        "gmsh_version": gver,
    }


def mesh_convergence_sweep(step_path: str, out_dir: str) -> list:
    """Run `solve_one_level` for each MESH_LEVELS entry. Returns the
    list of per-level result dicts plus a `delta_t_k_delta` field on
    levels 1..N pointing to the difference vs the previous level."""
    results = []
    for i, h in enumerate(MESH_LEVELS):
        t0 = time.time()
        res = solve_one_level(step_path, h, out_dir, i)
        res["wall_s"] = time.time() - t0
        if i == 0:
            res["delta_t_k_step"] = None
        else:
            res["delta_t_k_step"] = (
                res["delta_t_k"] - results[-1]["delta_t_k"])
        results.append(res)
    return results


def write_convergence_csv(results: list, csv_path: str) -> None:
    cols = [
        "level_idx", "mesh_size_m", "n_nodes", "n_elements",
        "t_max_k", "delta_t_k", "delta_t_k_step", "wall_s"]
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in results:
            w.writerow([r[c] if r.get(c) is not None else "" for c in cols])


def stl_from_step(step_path: str, stl_path: str,
                  mesh_size_m: float = 1.0e-3) -> bool:
    """Convert a STEP file to a triangular STL via gmsh (surface
    mesh only). Used to ship a viewer-friendly geometry copy."""
    import gmsh
    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("stl_export")
        gmsh.model.occ.importShapes(step_path)
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.MeshSizeMin", mesh_size_m)
        gmsh.option.setNumber("Mesh.MeshSizeMax", mesh_size_m)
        gmsh.model.mesh.generate(2)
        gmsh.write(stl_path)
        ok = os.path.exists(stl_path) and os.path.getsize(stl_path) > 0
    finally:
        gmsh.finalize()
    return ok


def fingerprint(geom_id: str, mat: dict, load: dict,
                gmsh_ver: str, skfem_ver: str) -> str:
    payload = {
        "geom_id": geom_id, "material": mat, "load": load,
        "gmsh_version": gmsh_ver, "skfem_version": skfem_ver,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()[:16]


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(
            "usage: upduino_enclosure_fem.py <out_dir> [<step_path>]\n")
        return 2
    out_dir = argv[1]
    os.makedirs(out_dir, exist_ok=True)

    if len(argv) >= 3:
        step_path = argv[2]
    else:
        # default: sibling file produced by upduino_enclosure.py
        step_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "upduino_cover_plate.step")

    if not os.path.isfile(step_path):
        sys.stderr.write(
            f"upduino_enclosure_fem: STEP file not found: {step_path}\n"
            "  run upduino_enclosure.py first.\n")
        return 2

    # 0. ship geometry copies into the record dir.
    step_copy = os.path.join(out_dir, "step.brep")  # canonical name
    shutil.copy(step_path, step_copy)
    stl_path = os.path.join(out_dir, "step.stl")
    stl_ok = stl_from_step(step_path, stl_path,
                           mesh_size_m=1.0e-3)
    if not stl_ok:
        sys.stderr.write(
            "upduino_enclosure_fem: STL export failed (non-fatal).\n")

    # 1. mesh convergence sweep.
    results = mesh_convergence_sweep(step_path, out_dir)

    # 2. convergence verdict.
    last_step = results[-1]["delta_t_k_step"]
    converged = last_step is not None and abs(last_step) < 0.1
    delta_t_final = results[-1]["delta_t_k"]

    # 3. write convergence csv.
    csv_path = os.path.join(out_dir, "mesh_convergence.csv")
    write_convergence_csv(results, csv_path)

    # 4. build the record (mirror of component-verify schema).
    import skfem
    skfem_ver = skfem.__version__
    gmsh_ver = results[0]["gmsh_version"]
    fp = fingerprint("upduino_v3_enclosure_v1", MATERIAL, LOAD,
                     gmsh_ver, skfem_ver)

    iso = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    record_id = f"upduino_enclosure_thermal_{iso}"
    record_path = os.path.join(out_dir, record_id + ".json")

    # flat measurement rows (mirrors die_proxy_box_v1.meta.json shape)
    rows = [
        {"measurement_key": "n_nodes_finest",
         "value": results[-1]["n_nodes"], "unit": "count"},
        {"measurement_key": "n_elements_finest",
         "value": results[-1]["n_elements"], "unit": "count"},
        {"measurement_key": "t_ambient_k",
         "value": LOAD["t_ambient_k"], "unit": "K"},
        {"measurement_key": "t_max_k",
         "value": results[-1]["t_max_k"], "unit": "K"},
        {"measurement_key": "t_mean_k",
         "value": results[-1]["t_mean_k"], "unit": "K"},
        {"measurement_key": "delta_t_k",
         "value": delta_t_final, "unit": "K"},
        {"measurement_key": "q_flux_w_per_m2",
         "value": results[-1]["q_flux_w_per_m2"], "unit": "W/m^2"},
        {"measurement_key": "convergence_step_k",
         "value": float(abs(last_step)) if last_step is not None else 0.0,
         "unit": "K"},
        {"measurement_key": "converged_below_0p1k",
         "value": int(bool(converged)), "unit": "bool"},
    ]

    meta = {
        "ok": True,
        "interface": "demiurge:component:gmsh-skfem-verify-record",
        "schema_version": "1.0",
        "record_id": record_id,
        "geometry_id": "upduino_v3_enclosure_v1",
        "fingerprint": fp,
        "gmsh_version": gmsh_ver,
        "skfem_version": skfem_ver,
        "python_version":
            f"{sys.version_info.major}.{sys.version_info.minor}."
            f"{sys.version_info.micro}",
        "produced_at_utc":
            datetime.now(timezone.utc).isoformat(),
        "geometry": {
            "id": "upduino_v3_enclosure_v1",
            "display_name":
                "UPduino v3 PCB + 1 mm Al cover plate enclosure",
            "length_m": COVER["length_m"],
            "width_m": COVER["width_m"],
            "thickness_m": COVER["thickness_m"],
            "z_offset_m": COVER["z_offset_m"],
            "step_source": os.path.basename(step_path),
            "stl_export": "step.stl" if stl_ok else None,
            "n_nodes": results[-1]["n_nodes"],
            "n_elements": results[-1]["n_elements"],
            "mesh_size_m_finest": MESH_LEVELS[-1],
        },
        "material": MATERIAL,
        "load": LOAD,
        "measurements": {
            "rows": len(rows),
            "table": rows,
            "thermal": {
                "t_min_k": results[-1]["t_min_k"],
                "t_max_k": results[-1]["t_max_k"],
                "t_mean_k": results[-1]["t_mean_k"],
                "delta_t_k": delta_t_final,
                "dof_count": results[-1]["n_nodes"],
            },
            "structural": None,  # thermal-only this cycle
        },
        "mesh_convergence": {
            "levels": [
                {
                    "level_idx": r["level_idx"],
                    "mesh_size_m": r["mesh_size_m"],
                    "n_nodes": r["n_nodes"],
                    "n_elements": r["n_elements"],
                    "t_max_k": r["t_max_k"],
                    "delta_t_k": r["delta_t_k"],
                    "delta_t_k_step": r["delta_t_k_step"],
                    "wall_s": r["wall_s"],
                }
                for r in results
            ],
            "converged_below_0p1k": bool(converged),
            "final_step_k": (float(abs(last_step))
                             if last_step is not None else None),
            "tolerance_k": 0.1,
        },
        "artifacts": {
            "record": os.path.basename(record_path),
            "csv": "mesh_convergence.csv",
            "step_brep": "step.brep",
            "stl": "step.stl" if stl_ok else None,
        },
        "provenance": {
            "absorbed": False,
            "measurement_gate": "GATE_OPEN",
            "producer":
                f"gmsh@{gmsh_ver} + scikit-fem@{skfem_ver} "
                "(anima/upduino_enclosure_fem.py @ Phase 1b)",
            "scope_caveats": [
                "geometry = real STEP B-Rep of UPduino v3 cover plate "
                "(50×33×1 mm Al) — upgrade vs toy 10×10×2 mm Si box, "
                "BUT dimensions are datasheet-recall NOT caliper "
                "measurement on a fabricated part (g3).",
                "material = textbook Al 6061-T6 at 300 K (k=167 W/m·K, "
                "ρ=2700 kg/m³, E=68.9 GPa, ν=0.33) — CRC Handbook / "
                "AZoM values, NOT a measured lot. Datasheet flash-test "
                "+ Hot Disk measurement required for GATE_CLOSED.",
                "heat source = uniform 1 W Neumann patch on the cover "
                "plate bottom face (FPGA 0.5 W + LDO 0.5 W datasheet "
                "ESTIMATES). True BGA + LDO localisation not modelled "
                "at this scale; transient + thermo-mechanical coupling "
                "out of scope.",
                "convection h = 10 W/m²K applied on top face (Robin BC) "
                "is textbook free-convection on vertical Al at room "
                "temperature, NOT a wind-tunnel measurement. Side / "
                "bottom faces insulated (adiabatic) — physically wrong "
                "for an open enclosure but bounds ΔT from above.",
                "mesh convergence SWEEP performed (4 levels, h = 1.5 "
                "→ 0.5 mm). measurement_gate STILL GATE_OPEN because "
                "(real BOM + fabricated enclosure + bench IR / "
                "thermocouple measurement + 3rd-party FE cross-check "
                "Code_Aster / Elmer) are all still missing.",
            ],
        },
        "honest_c3_count": 5,
        "error": None,
    }
    with open(record_path, "w") as f:
        json.dump(meta, f, indent=2, sort_keys=True)

    # 5. summary line — mirrors COMPONENT_GMSH_SKFEM_RESULT shape
    #    so the same Swift ComponentVerifyProducer parser can consume
    #    this record (artifacts key list extended).
    summary = {
        "ok": True,
        "geometry_id": "upduino_v3_enclosure_v1",
        "gmsh_version": gmsh_ver,
        "skfem_version": skfem_ver,
        "python_version": meta["python_version"],
        "rows": len(rows),
        "artifacts": {
            "record": os.path.basename(record_path),
            "csv": "mesh_convergence.csv",
            "step": "step.brep",
            "stl": "step.stl" if stl_ok else "",
        },
        "delta_t_k": delta_t_final,
        "converged_below_0p1k": bool(converged),
        "final_step_k": (float(abs(last_step))
                         if last_step is not None else None),
    }
    sys.stderr.write(
        "UPDUINO_ENCLOSURE_THERMAL_RESULT "
        + json.dumps(summary) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
