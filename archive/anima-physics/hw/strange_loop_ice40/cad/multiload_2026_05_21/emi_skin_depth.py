#!/usr/bin/env python3
# emi_skin_depth.py — Faraday-cage EMI shielding effectiveness
# analytical calculator for the 1 mm Al 6061 cover plate (Part B
# of G5 scope_caveat #3 multi-load FEM closure).
#
# PHYSICS
#   Skin depth (plane-wave, good conductor):
#       δ = sqrt(2 / (ω · μ · σ))
#       ω = 2π·f, μ = μ₀ · μ_r, σ = conductivity (S/m)
#
#   Shielding effectiveness of a solid metal sheet (thickness t,
#   t > δ), absorption-dominated regime:
#       SE_A_dB = 20 · log10(e^(t/δ)) = 8.686 · (t/δ)
#       (canonical Schelkunsh / Ott "Electromagnetic Compatibility
#       Engineering" Ch.6 absorption term.)
#
#   The task spec uses SE_dB = 20·log10(t/δ); we report BOTH because
#   the literature-standard form is the exponential one. Below the
#   skin-depth (t < δ) absorption-only SE drops below ~9 dB and
#   reflection (SE_R) dominates — we include SE_R, SE_A, SE_total.
#
#   Reflection loss for plane wave at far-field, far-field metallic
#   shield (Ott Eq. 6.4):
#       SE_R_dB = 168 + 10·log10( σ_r / (μ_r · f_MHz) )
#       where σ_r = σ / σ_Cu, σ_Cu = 5.8e7 S/m.
#
#   Total SE_dB ≈ SE_R + SE_A  (multi-reflection correction is
#   negligible when SE_A > 10 dB, conservative otherwise).
#
# OUTPUT: table {freq, δ_µm, t_over_δ, SE_spec_dB, SE_A_dB,
#                SE_R_dB, SE_total_dB, adequacy_verdict}
#
# Author: anima FPGA Phase 1c (multi-load FEM, G5 scope_caveat #3
# Part B)
# Date  : 2026-05-21

import json
import math
import os
import sys
from datetime import datetime, timezone


MU_0 = 4.0e-7 * math.pi             # H/m
SIGMA_CU = 5.8e7                    # S/m (annealed copper reference)

# Al 6061-T6 plate
PLATE = {
    "material": "aluminium 6061-T6",
    "sigma_s_per_m": 3.5e7,         # task spec value (3.5e7 S/m)
    "mu_r": 1.0,                    # non-magnetic
    "thickness_m": 1.0e-3,
}

# Threat freqs — common digital + ISM bands relevant for ICE40 + RF
FREQS_HZ = [100.0e6, 1.0e9, 10.0e9]


def skin_depth_m(freq_hz: float, sigma: float, mu_r: float) -> float:
    """δ = sqrt(2 / (ω · μ · σ))."""
    omega = 2.0 * math.pi * freq_hz
    mu = MU_0 * mu_r
    return math.sqrt(2.0 / (omega * mu * sigma))


def se_absorption_db(thickness_m: float, delta_m: float) -> float:
    """Absorption shielding effectiveness, exponential form
    (Schelkunsh / Ott)."""
    return 8.685889638 * (thickness_m / delta_m)


def se_reflection_db(freq_hz: float, sigma: float, mu_r: float) -> float:
    """Plane-wave far-field reflection loss (Ott Eq. 6.4).
    SE_R_dB = 168 + 10·log10(σ_r / (μ_r · f_MHz))."""
    sigma_rel = sigma / SIGMA_CU
    f_mhz = freq_hz / 1.0e6
    return 168.0 + 10.0 * math.log10(sigma_rel / (mu_r * f_mhz))


def se_spec_form_db(thickness_m: float, delta_m: float) -> float:
    """Task-spec form: SE = 20·log10(t/δ). Diverges to -∞ as
    t/δ → 0 — only meaningful when t > δ."""
    ratio = thickness_m / delta_m
    if ratio <= 0:
        return float("-inf")
    return 20.0 * math.log10(ratio)


def adequacy(se_total_db: float) -> str:
    """IEC 61000-4-3 typical adequacy bands for consumer/industrial:
        > 60 dB  : excellent (mil-grade)
        40 – 60  : good (industrial)
        20 – 40  : adequate (consumer FCC class B)
        < 20 dB  : inadequate
    """
    if se_total_db > 60.0:
        return "excellent (mil/medical)"
    elif se_total_db > 40.0:
        return "good (industrial IEC 61000-4-3)"
    elif se_total_db > 20.0:
        return "adequate (FCC class B / CISPR 22)"
    elif se_total_db > 0:
        return "marginal — needs supplemental shielding"
    else:
        return "inadequate — RF passes through"


def analyse() -> dict:
    rows = []
    for f in FREQS_HZ:
        delta = skin_depth_m(
            f, PLATE["sigma_s_per_m"], PLATE["mu_r"])
        t = PLATE["thickness_m"]
        t_over_delta = t / delta
        se_spec = se_spec_form_db(t, delta)
        se_A = se_absorption_db(t, delta)
        se_R = se_reflection_db(
            f, PLATE["sigma_s_per_m"], PLATE["mu_r"])
        se_total = se_A + se_R

        row = {
            "freq_hz": f,
            "freq_label":
                f"{f/1e6:.0f} MHz" if f < 1e9 else f"{f/1e9:.0f} GHz",
            "delta_m": delta,
            "delta_um": delta * 1e6,
            "thickness_m": t,
            "t_over_delta": t_over_delta,
            "se_spec_form_db": se_spec,        # 20·log10(t/δ)
            "se_absorption_db": se_A,          # 8.686·(t/δ)
            "se_reflection_db": se_R,
            "se_total_db": se_total,
            "adequacy": adequacy(se_total),
        }
        rows.append(row)
    return {
        "plate": PLATE,
        "freqs_hz": FREQS_HZ,
        "rows": rows,
        "mu_0_h_per_m": MU_0,
        "sigma_cu_reference_s_per_m": SIGMA_CU,
    }


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(
            "usage: emi_skin_depth.py <out_dir>\n")
        return 2
    out_dir = argv[1]
    os.makedirs(out_dir, exist_ok=True)

    result = analyse()

    iso = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    record = {
        "ok": True,
        "interface":
            "demiurge:component:gmsh-skfem-verify-record-multiload",
        "record_id": f"emi_skin_depth_{iso}",
        "analysis": "emi_shielding_skin_depth_analytical",
        "geometry_id": "upduino_v3_enclosure_v1",
        "produced_at_utc": datetime.now(timezone.utc).isoformat(),
        "plate": PLATE,
        "freqs_hz": FREQS_HZ,
        "rows": result["rows"],
        "summary_table_md": (
            "| freq | δ (µm) | t/δ | SE_spec (20·log) | "
            "SE_A | SE_R | SE_total | adequacy |\n"
            "|------|--------|-----|------------------|------|"
            "------|----------|----------|\n"
            + "\n".join(
                "| {label} | {d_um:.2f} | {ratio:.2f} | {spec:.1f} | "
                "{a:.1f} | {r:.1f} | {tot:.1f} | {adq} |".format(
                    label=r["freq_label"],
                    d_um=r["delta_um"],
                    ratio=r["t_over_delta"],
                    spec=r["se_spec_form_db"],
                    a=r["se_absorption_db"],
                    r=r["se_reflection_db"],
                    tot=r["se_total_db"],
                    adq=r["adequacy"])
                for r in result["rows"])),
        "all_adequate":
            all(r["se_total_db"] > 40.0 for r in result["rows"]),
        "provenance": {
            "absorbed": False,
            "measurement_gate": "GATE_OPEN",
            "producer":
                "anima/multiload_2026_05_21/emi_skin_depth.py "
                "(analytical, no FEM)",
            "scope_caveats": [
                "plane-wave far-field assumption (Schelkunsh/Ott) — "
                "near-field magnetic sources < 1 m would reduce "
                "SE_R by 30-60 dB.",
                "no slot/aperture penalty modelled — real enclosure "
                "USB-C cutout + status LEDs + screw holes drop "
                "SE_total to ~half the calculated value (slot length "
                "→ leakage frequency f_λ/2).",
                "Al 6061 σ = 3.5e7 S/m = task-spec value, MMPDS "
                "DC-conductivity range is 2.4-4.1e7 (Mg+Si alloying "
                "lowers vs pure Al 6.0e7). NOT a measured-lot value.",
            ],
        },
        "error": None,
    }
    rec_path = os.path.join(out_dir, "emi_skin_depth.json")
    with open(rec_path, "w") as f:
        json.dump(record, f, indent=2, sort_keys=True)

    summary = {
        "ok": True,
        "analysis": "emi_skin_depth",
        "rows": [
            {"freq_label": r["freq_label"],
             "delta_um": r["delta_um"],
             "se_total_db": r["se_total_db"],
             "adequacy": r["adequacy"]}
            for r in result["rows"]],
        "all_adequate": record["all_adequate"],
        "record": rec_path,
    }
    sys.stderr.write("EMI_SKIN_DEPTH_RESULT " + json.dumps(summary) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
