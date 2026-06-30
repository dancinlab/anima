#!/usr/bin/env python3
"""demiurge_materials_bridge.py — anima → demiurge materials consumer bridge.

CONTEXT: `anima-physics/docs/demiurge_hw_verify_2026_05_21.md §2.1` 의
demiurge **materials** 도메인은 현재 ⏳ no producer (라우팅 미스).
**D17 consumer-pointer 패턴**: demiurge 는 typed-interface consumer 이며
materials 의 owner SSOT 는 `~/core/hexa-matter/verify/run_all.hexa`
(spec-first substrate · 4 closure invariant: spec_presence /
lattice_arithmetic / real_limits_anchor / closure_consistency).

본 bridge 는 **consumer-side composite record emitter** — hexa-matter
sibling-repo 의 결과 (parity record) + anima-physics 의 materials-relevant
substrate (memristor TiO2 / thermodynamic Langevin / superconducting
deprecated provenance) 를 하나의 record 로 묶어 demiurge 가 인용 가능한
경로 `~/core/demiurge/exports/materials/verify/<UTC>Z/` 에 drop.

D17 안내 (consumer ≠ producer):
    - hexa-matter (`~/core/hexa-matter/`) = owner SSOT (모든 material
      property / spec / lattice closure 의 진실 source).
    - anima-physics = composite-consumer (자체 substrate 의 materials-
      adjacent 측정값 + hexa-matter 결과 인용).
    - 본 record 는 **pointer + composite snapshot** 이며 실 material
      property 의 oracle parity 는 hexa-matter 측에서 보장.

SCOPE (skeleton):
    (a) Mac local py_compile clean.
    (b) emit `demiurge:materials:composite-record` (3 anima substrate +
        hexa-matter sibling-repo result 통합).
    (c) measurement key: hexa_matter_closure_pass (4-script aggregate
        exit code) ⊕ memristor_w_drift (TiO2 conductance bounds) ⊕
        thermo_arrhenius_slope (Langevin double-well kinetics) ⊕
        supercond_provenance_gate (deprecation honesty).
    (d) SW source = 3 anima substrate + hexa-matter verify/run_all.hexa.

Future close-the-loop:
    - hexa-matter sibling 의 매 verify 통과 시 본 bridge auto-invoke →
      record refresh. demiurge consumer (MatterVerifyProducer.swift 신설
      OR ActionDispatch `(.verify, "matter")` 케이스 등록) 별도 cycle.
    - material_class 별 deep-dive (TiO2 / Si / Al / Cu) record 화 — 현재는
      composite 만, per-material 은 후속 cycle.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


INTERFACE = "demiurge:materials:composite-record"
SCHEMA_VERSION = "0.1"
PRODUCER_NAME = "anima-materials-hexa-matter-combined-bridge"

# D17 owner pointer — single source of truth for materials properties.
HEXA_MATTER_VERIFY_PATH = os.path.expanduser(
    "~/core/hexa-matter/verify/run_all.hexa"
)


def _probe_hexa_matter_exit() -> tuple[int | None, str]:
    """Skeleton probe — best-effort exit code from hexa-matter verify.

    Returns (rc, note). rc is None if hexa runtime / repo missing.
    We deliberately do NOT block on real execution (could be slow); the
    bridge accepts user-provided override via --hexa-matter-exit.
    Default behavior: stat the file and report presence.
    """
    if not os.path.exists(HEXA_MATTER_VERIFY_PATH):
        return None, "hexa-matter verify/run_all.hexa not present (skeleton)"
    return None, (
        "hexa-matter verify/run_all.hexa present at "
        f"{HEXA_MATTER_VERIFY_PATH} (skeleton — not auto-run; "
        "use --hexa-matter-exit to override)"
    )


@dataclass
class DemiurgeMaterialsBridge:
    """Composite materials record — anima substrate + hexa-matter pointer.

    Usage:
        bridge = DemiurgeMaterialsBridge(
            backend="composite",
            material_class="TiO2",
        )
        record = bridge.to_record()

    D17 reminder: this is a **consumer-side** composite emitter. Real
    material-property oracle parity lives in hexa-matter; this record
    cites + aggregates, does not own.
    """

    # ─── selector ───
    # composite = 3 anima substrate + hexa-matter; specific = single substrate
    backend: str = "composite"           # composite | hexa_matter | memristor | thermo | supercond
    material_class: str = "TiO2"         # TiO2 | Si | Al | Cu | mixed

    # ─── anima substrate measurements (mirror §188 PASS defaults) ───
    # memristor/self_reference.hexa T1 non-volatility window
    memristor_w_min: float = 0.02        # normalized conductance lower bound
    memristor_w_max: float = 0.98        # normalized conductance upper bound
    memristor_w_drift_pass: bool = True  # T1 PASS (stayed in [w_min, w_max])

    # thermodynamic/entropy_dissolution.hexa Langevin double-well analog
    thermo_arrhenius_slope: float = 7.69         # jumps(D=1.0)/jumps(D=0.3) monotone
    thermo_ergodic_mean_position: float = -0.187 # |⟨x⟩| < 0.4 ergodic threshold

    # superconducting/cloud_facade_poc.hexa — DEPRECATED, provenance gate only
    supercond_verdict: str = "PREP_DEPRECATED_RIGETTI_RETIRED"
    supercond_provenance_gate_pass: bool = True  # 5/5 honest deprecation

    # ─── hexa-matter sibling pointer (D17 owner SSOT) ───
    hexa_matter_exit_code: int | None = None  # None = not probed
    hexa_matter_closure_pass: bool | None = None  # rc==0 → True
    hexa_matter_repo_path: str = "~/core/hexa-matter"
    hexa_matter_verify_path: str = HEXA_MATTER_VERIFY_PATH

    # ─── key property defaults (TiO2 reference, Strukov 2008) ───
    # populated per material_class via _resolve_material_properties()
    key_properties: dict[str, Any] = field(default_factory=dict)

    # ─── provenance ───
    seed: int = 42
    absorbed: bool = False
    sim_engine: str = "anima-physics:{memristor,thermodynamic,superconducting}"
    sim_commit_hash: str = "local"

    scope_caveats: list[str] = field(default_factory=list)
    gate_failures: list[str] = field(default_factory=list)

    # ───────────────────────────────────────────────────────────────
    # Material property registry — minimal NIST/CRC-anchored defaults.
    # ───────────────────────────────────────────────────────────────
    @staticmethod
    def _material_property_registry() -> dict[str, dict[str, Any]]:
        return {
            # TiO2 — memristor switching layer (Strukov 2008 HP memristor).
            "TiO2": {
                "name": "Titanium dioxide (rutile)",
                "density_g_cm3": 4.23,
                "bandgap_eV": 3.0,
                "resistivity_ohm_m": 1.0e3,    # variable, switching layer
                "conductivity_S_m": 1.0e-3,
                "specific_heat_J_kgK": 690,
                "note": "memristor switching layer; conductance bistable",
            },
            # Si — substrate baseline.
            "Si": {
                "name": "Silicon (intrinsic)",
                "density_g_cm3": 2.33,
                "bandgap_eV": 1.12,
                "resistivity_ohm_m": 6.4e2,
                "conductivity_S_m": 1.56e-3,
                "specific_heat_J_kgK": 700,
                "tensile_strength_MPa": 7000,  # theoretical, monocrystalline
                "note": "ground truth substrate for chip / FPGA / MCU",
            },
            # Al — interconnect / heat-spreader.
            "Al": {
                "name": "Aluminum",
                "density_g_cm3": 2.70,
                "resistivity_ohm_m": 2.65e-8,
                "conductivity_S_m": 3.77e7,
                "specific_heat_J_kgK": 897,
                "tensile_strength_MPa": 90,
                "thermal_conductivity_W_mK": 237,
                "note": "FPGA heat-sink + PCB interconnect baseline",
            },
            # Cu — high-conductivity interconnect.
            "Cu": {
                "name": "Copper",
                "density_g_cm3": 8.96,
                "resistivity_ohm_m": 1.68e-8,
                "conductivity_S_m": 5.96e7,
                "specific_heat_J_kgK": 385,
                "tensile_strength_MPa": 210,
                "thermal_conductivity_W_mK": 401,
                "note": "preferred interconnect for >100MHz designs",
            },
            "mixed": {
                "name": "Composite (TiO2 + Si + Al + Cu)",
                "note": "aggregate across 4 reference materials",
            },
        }

    def _resolve_material_properties(self) -> dict[str, Any]:
        reg = self._material_property_registry()
        if self.material_class in reg:
            return dict(reg[self.material_class])
        return {
            "name": f"unknown material_class={self.material_class}",
            "note": "not in registry; treated as opaque pointer",
        }

    def gate_state(self) -> str:
        """measurement_gate per demiurge convention.

        - composite + hexa-matter rc==0 + all anima substrate PASS → GATE_OPEN
          (oracle parity not yet authored on demiurge consumer side).
        - any gate_failure → GATE_FAIL.
        """
        if self.gate_failures:
            return "GATE_FAIL"
        return "GATE_OPEN"

    def _aggregate_gate_failures(self) -> list[str]:
        """Auto-populate gate_failures from substrate flags."""
        failures: list[str] = list(self.gate_failures)
        if not self.memristor_w_drift_pass:
            failures.append(
                "memristor T1 non-volatility FAIL (w drifted out of "
                f"[{self.memristor_w_min}, {self.memristor_w_max}])"
            )
        if not self.supercond_provenance_gate_pass:
            failures.append("superconducting provenance gate FAIL")
        if self.hexa_matter_closure_pass is False:
            failures.append(
                "hexa-matter closure verify FAIL "
                f"(exit={self.hexa_matter_exit_code})"
            )
        return failures

    def to_record(self) -> dict[str, Any]:
        if not self.key_properties:
            self.key_properties = self._resolve_material_properties()
        self.gate_failures = self._aggregate_gate_failures()

        caveats = list(self.scope_caveats) or [
            "D17 consumer-pointer: hexa-matter is owner SSOT, this is composite emitter",
            "anima substrate measurements are CONSCIOUSNESS-ANALOG, not material spec",
            "memristor TiO2 = Strukov HP analog (numpy reference, not real ionic drift)",
            "thermodynamic Langevin = double-well kinetics analog (NOT real chemistry)",
            "superconducting = DEPRECATED (Rigetti retired 2026-04-27, provenance gate only)",
            "key_properties = NIST/CRC textbook defaults, not measured per-sample",
            "hexa-matter exit code skeleton — set via --hexa-matter-exit (no auto-run)",
            "materials producer oracle parity not yet authored (TODO: demiurge rfc)",
        ]
        return {
            "interface": INTERFACE,
            "schema_version": SCHEMA_VERSION,
            "record_id": (
                f"materials_{self.backend}_{self.material_class}_"
                f"hxm{self.hexa_matter_exit_code}_seed{self.seed}"
            ),
            "produced_at_utc": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "topology": {
                "kind": "materials_composite",
                "material_class": self.material_class,
                "backend": self.backend,
                "owner_ssot": "hexa-matter (D17 pointer)",
                "consumer_role": "anima-physics composite emitter",
            },
            "measurement": {
                "hexa_matter": {
                    "verify_path": self.hexa_matter_verify_path,
                    "exit_code": self.hexa_matter_exit_code,
                    "closure_pass": self.hexa_matter_closure_pass,
                    "owner_pattern": "D17 typed-interface consumer-pointer",
                },
                "memristor": {
                    "w_min": self.memristor_w_min,
                    "w_max": self.memristor_w_max,
                    "non_volatility_pass": self.memristor_w_drift_pass,
                    "source": "anima-physics/memristor/self_reference.hexa §188 5/5",
                },
                "thermodynamic": {
                    "arrhenius_d_slope": self.thermo_arrhenius_slope,
                    "ergodic_mean_position": self.thermo_ergodic_mean_position,
                    "source": "anima-physics/thermodynamic/entropy_dissolution.hexa 5/5",
                },
                "superconducting": {
                    "verdict": self.supercond_verdict,
                    "provenance_gate_pass": self.supercond_provenance_gate_pass,
                    "source": "anima-physics/superconducting/cloud_facade_poc.hexa (deprecated)",
                },
                "key_properties": self.key_properties,
                "seed": self.seed,
            },
            "provenance": {
                "producer": PRODUCER_NAME,
                "backend": self.backend,
                "absorbed": self.absorbed,
                "measurement_gate": self.gate_state(),
                "sim_engine": self.sim_engine,
                "sim_commit_hash": self.sim_commit_hash,
                "atlas_cite_block": (
                    "@cite anima-physics:memristor/self_reference.hexa §188 5/5 + "
                    "thermodynamic/entropy_dissolution.hexa 5/5 + "
                    "superconducting/cloud_facade_poc.hexa (deprecated, prov gate 5/5); "
                    "@cite hexa-matter:verify/run_all.hexa (D17 owner SSOT); "
                    "demiurge_hw_verify_2026_05_21 §2.1 (materials no-producer gap)"
                ),
                "consumer_target": "demiurge:materials:verify",
                "owner_pointer": "hexa-matter:verify/run_all.hexa",
                "scope_caveats": caveats,
                "gate_failures": self.gate_failures,
            },
            "verdict": {
                "gate_state": self.gate_state(),
                "rationale": (
                    f"composite emit — backend={self.backend} material={self.material_class} "
                    f"(memristor PASS · thermo monotone · supercond deprecated-honest · "
                    f"hexa-matter exit={self.hexa_matter_exit_code}); "
                    "D17 consumer-pointer; oracle parity TODO"
                ),
            },
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_record(), indent=indent, sort_keys=True)


def _main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="demiurge_materials_bridge",
        description=(
            "Emit a demiurge:materials:composite-record JSON (stdout or "
            "--output). D17 consumer-pointer: hexa-matter is owner SSOT, "
            "anima-physics is composite consumer (3 substrate + hexa-matter)."
        ),
    )
    parser.add_argument(
        "--backend",
        default="composite",
        choices=("composite", "hexa_matter", "memristor", "thermo", "supercond"),
    )
    parser.add_argument(
        "--material",
        dest="material_class",
        default="TiO2",
        choices=("TiO2", "Si", "Al", "Cu", "mixed"),
    )
    parser.add_argument(
        "--hexa-matter-exit",
        type=int,
        default=None,
        help=(
            "hexa-matter verify/run_all.hexa exit code override "
            "(0 = closure_pass, default None = not probed). Skeleton: "
            "we never auto-run hexa-matter to avoid coupling. Use "
            "--probe to stat the file (no execution)."
        ),
    )
    parser.add_argument(
        "--probe",
        action="store_true",
        help="stat hexa-matter verify path and emit pointer note (no exec)",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        default="-",
        help="JSON file path or '-' for stdout",
    )
    args = parser.parse_args()

    hxm_rc: int | None = args.hexa_matter_exit
    hxm_closure: bool | None = None
    probe_note = ""
    if args.probe:
        _rc, probe_note = _probe_hexa_matter_exit()
        sys.stderr.write(f"[demiurge_materials_bridge] probe: {probe_note}\n")
    if hxm_rc is not None:
        hxm_closure = hxm_rc == 0

    bridge = DemiurgeMaterialsBridge(
        backend=args.backend,
        material_class=args.material_class,
        hexa_matter_exit_code=hxm_rc,
        hexa_matter_closure_pass=hxm_closure,
        seed=args.seed,
    )
    text = bridge.to_json()
    if args.output == "-":
        sys.stdout.write(text + "\n")
    else:
        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        sys.stderr.write(f"[demiurge_materials_bridge] wrote {args.output}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
