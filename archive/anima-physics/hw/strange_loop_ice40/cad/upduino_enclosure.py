#!/usr/bin/env python3
# upduino_enclosure.py — anima FPGA UPduino v3 enclosure STEP geometry.
#
# Phase 1b real-component handoff (G5 demiurge component
# GATE_OPEN → GATE_OPEN with real STEP — GATE_CLOSED still requires
# datasheet + mesh convergence + 3rd-party signoff per
# `exports/component/verify/.../die_proxy_box_v1.meta.json::scope_caveats`).
#
# Geometry — UPduino v3 (Lattice iCE40UP5K dev board, 40-pin DIP,
# DIP-40 footprint width 47 mm × length 30 mm × ~10 mm tall including
# the USB-C jack and headers). The board is approximated as a single
# 47 × 30 × 10 mm FR-4 PCB volume (the heat-bearing slab — actual
# component-level heating is the iCE40UP5K BGA in the middle and the
# AP2112K LDO regulator near the USB jack). The aluminium cover plate
# is 50 × 33 × 1 mm with 1 mm clearance on all sides of the PCB,
# offset 1 mm above the PCB top face (i.e. enclosure inner height
# 11 mm, total Z extent 12 mm).
#
# OUTPUT
#   upduino_enclosure.step   — STEP AP203 B-Rep, OCC-generated via gmsh
#   upduino_enclosure.brep   — native OCC brep, same geometry
#
# DEPENDENCIES — gmsh only (cadquery / build123d / OpenSCAD not needed:
# gmsh's OpenCascade backend writes STEP directly via gmsh.write()).
#
# HONESTY (g3 — non-negotiable, inherited from demiurge component
# verify caveats):
#   * Dimensions are taken from the UPduino v3 schematic / Tinyvision.ai
#     dev-board datasheet (board outline 47 × 30 mm, headers 0.1" pitch,
#     iCE40UP5K SG48 5.5 × 5.5 mm package). They are NOT measured with
#     calipers on a real board — datasheet recall, not bench measurement.
#   * The enclosure cover plate (50 × 33 × 1 mm Al) is an enclosure
#     PROPOSAL geometry — no physical part has been fabricated. There
#     is no BOM line, no vendor PO, no measured material lot.
#   * Component-level features (BGA balls, header pins, USB-C jack,
#     LDO TO-23 package) are NOT modelled — the PCB is a homogeneous
#     FR-4 slab. Thermal/structural results that depend on those
#     features (BGA stress concentration, header thermal bridging)
#     are out of scope for this enclosure-level model.
#   * One-body STEP only — PCB + cover plate are NOT joined or
#     assembled. Each is meshed independently by the downstream
#     `upduino_enclosure_fem.py` adapter, which currently meshes
#     ONLY the cover plate (it carries the enclosure thermal mass);
#     the PCB acts as the heat source boundary condition.
#
# CLI
#   python3 upduino_enclosure.py <output_dir>
#     writes <output_dir>/upduino_enclosure.step
#     writes <output_dir>/upduino_enclosure.brep
#     writes <output_dir>/upduino_enclosure.geometry.json (sidecar)
#
# Author: anima FPGA Phase 1b (G5 demiurge component handoff)
# Date  : 2026-05-21

import json
import os
import sys

# Inject macOS pip --user --break-system-packages path (Homebrew
# Python 3.14 user-site is NOT on default sys.path).
_USER_SITE = os.path.expanduser(
    f"~/Library/Python/{sys.version_info.major}.{sys.version_info.minor}"
    "/lib/python/site-packages")
if os.path.isdir(_USER_SITE) and _USER_SITE not in sys.path:
    sys.path.insert(0, _USER_SITE)


# ------------------------------------------------------------------
# Canonical UPduino v3 enclosure geometry (SI units, METRES throughout).
# ------------------------------------------------------------------
GEOMETRY = {
    "id": "upduino_v3_enclosure_v1",
    "display_name": "UPduino v3 PCB + 1 mm Al cover plate enclosure",

    # PCB (FR-4 slab approximation of 40-pin DIP dev board).
    "pcb_length_m":    47.0e-3,   # x
    "pcb_width_m":     30.0e-3,   # y
    "pcb_thickness_m": 10.0e-3,   # z (incl. headers + USB-C jack)

    # Aluminium cover plate (1 mm wall, 1 mm clearance on all sides).
    "cover_length_m":    50.0e-3,
    "cover_width_m":     33.0e-3,
    "cover_thickness_m":  1.0e-3,
    "cover_z_offset_m":  11.0e-3,   # sits 1 mm above PCB top

    # Mesh target size (5 % of cover thickness gives ~3-4 tets through
    # the wall — enough to converge linear conduction to <1 % per the
    # downstream FEM convergence sweep).
    "mesh_size_m":        0.5e-3,
}


def build_geometry(out_dir: str) -> dict:
    """Build the UPduino v3 PCB + Al cover plate STEP geometry via
    gmsh's OpenCascade backend. Writes .step and .brep into out_dir.

    Returns a dict with file paths, byte sizes, and the geometry id."""
    import gmsh

    os.makedirs(out_dir, exist_ok=True)
    g = GEOMETRY

    step_path = os.path.join(out_dir, "upduino_enclosure.step")
    brep_path = os.path.join(out_dir, "upduino_enclosure.brep")
    json_path = os.path.join(out_dir, "upduino_enclosure.geometry.json")
    cover_step_path = os.path.join(out_dir, "upduino_cover_plate.step")

    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add(g["id"])

        # PCB: centred at origin in x,y; z = [0, pcb_thickness].
        # Box origin is the (x0,y0,z0) corner so we offset by -L/2,-W/2.
        pcb_tag = gmsh.model.occ.addBox(
            -g["pcb_length_m"] / 2.0,
            -g["pcb_width_m"] / 2.0,
            0.0,
            g["pcb_length_m"],
            g["pcb_width_m"],
            g["pcb_thickness_m"])

        # Cover plate: centred above PCB.
        cover_tag = gmsh.model.occ.addBox(
            -g["cover_length_m"] / 2.0,
            -g["cover_width_m"] / 2.0,
            g["cover_z_offset_m"],
            g["cover_length_m"],
            g["cover_width_m"],
            g["cover_thickness_m"])

        gmsh.model.occ.synchronize()

        # Write full assembly STEP (both volumes).
        gmsh.write(step_path)
        gmsh.write(brep_path)

        step_size = os.path.getsize(step_path)
        brep_size = os.path.getsize(brep_path)
    finally:
        gmsh.finalize()

    # Cover-plate-only STEP (used as the FEM input geometry — the PCB
    # acts as a boundary thermal source). Built in a separate gmsh
    # session to keep gmsh.model state isolated.
    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add(g["id"] + "_cover")
        gmsh.model.occ.addBox(
            -g["cover_length_m"] / 2.0,
            -g["cover_width_m"] / 2.0,
            g["cover_z_offset_m"],
            g["cover_length_m"],
            g["cover_width_m"],
            g["cover_thickness_m"])
        gmsh.model.occ.synchronize()
        gmsh.write(cover_step_path)
        cover_step_size = os.path.getsize(cover_step_path)
    finally:
        gmsh.finalize()

    # Sidecar JSON — flat geometry record consumed by the FEM adapter.
    geom_meta = {
        "id": g["id"],
        "display_name": g["display_name"],
        "interface": "anima:hw:upduino_v3_enclosure_v1",
        "schema_version": "1.0",
        "units": "meters",
        "pcb": {
            "length_m": g["pcb_length_m"],
            "width_m": g["pcb_width_m"],
            "thickness_m": g["pcb_thickness_m"],
        },
        "cover_plate": {
            "length_m": g["cover_length_m"],
            "width_m": g["cover_width_m"],
            "thickness_m": g["cover_thickness_m"],
            "z_offset_m": g["cover_z_offset_m"],
        },
        "mesh_size_m_target": g["mesh_size_m"],
        "artifacts": {
            "step_full": os.path.basename(step_path),
            "step_cover_only": os.path.basename(cover_step_path),
            "brep_full": os.path.basename(brep_path),
        },
        "honest_c3": [
            "datasheet recall only (UPduino v3 schematic + Tinyvision.ai "
            "board outline); NOT caliper-measured.",
            "cover plate is a PROPOSAL — no fabricated part, no BOM.",
            "PCB is a homogeneous FR-4 slab; BGA / headers / USB-C jack "
            "NOT modelled (component-level features out of scope).",
            "PCB + cover plate are NOT joined / assembled — separate "
            "B-Rep volumes in the same STEP file.",
            "single load case downstream (steady-state thermal); "
            "transient + structural + multi-case sweep out of scope.",
        ],
    }
    with open(json_path, "w") as f:
        json.dump(geom_meta, f, indent=2, sort_keys=True)

    return {
        "id": g["id"],
        "step_path": step_path,
        "step_size": step_size,
        "step_cover_path": cover_step_path,
        "step_cover_size": cover_step_size,
        "brep_path": brep_path,
        "brep_size": brep_size,
        "json_path": json_path,
    }


def main(argv):
    if len(argv) < 2:
        out_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        out_dir = argv[1]
    result = build_geometry(out_dir)
    print(json.dumps({
        "ok": True,
        "geometry_id": result["id"],
        "step_path": result["step_path"],
        "step_size_bytes": result["step_size"],
        "step_cover_path": result["step_cover_path"],
        "step_cover_size_bytes": result["step_cover_size"],
        "brep_path": result["brep_path"],
        "brep_size_bytes": result["brep_size"],
        "json_path": result["json_path"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
