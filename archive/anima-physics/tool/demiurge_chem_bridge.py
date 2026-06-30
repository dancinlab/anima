#!/usr/bin/env python3
"""demiurge_chem_bridge.py — anima → demiurge chem producer bridge.

CONTEXT: `anima-physics/docs/demiurge_hw_verify_2026_05_21.md §2.2` 의
demiurge chem 도메인은 현재 ❌ no producer (mock-fallback 가능성).
anima 측은 thermodynamic substrate (engines/thermodynamic_consciousness +
thermodynamic/entropy_dissolution) — Langevin double-well + thermal noise
+ Arrhenius D-sweep — F-TH-1..5 5/5 PASS 보유. 이는 chemistry analog 의
1급 source (reaction barrier crossing = molecular jumps).

SCOPE (skeleton):
    (a) Mac local py_compile clean.
    (b) emit `demiurge:chem:entropy-record` (Langevin barrier crossing
        통계 → reaction kinetics analog).
    (c) measurement key: barrier_jumps_per_step ⊕ arrhenius_d_slope ⊕
        ergodic_mean_position ⊕ free_energy_landscape_depth.
    (d) SW source = engines/thermodynamic_consciousness.hexa F-TH-1..5
        5/5 PASS (state/s188g_engines_2026_05_21/thermodynamic.run.log).

Future close-the-loop:
    Phase 2 wet-lab analog (microfluidic single-molecule Arrhenius
    measurement OR computational chemistry DFT/MD) → `--backend
    microfluidic_smd` → demiurge chem consumer (ChemVerifyProducer.swift)
    → GATE_CLOSED_MEASURED upgrade.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


INTERFACE = "demiurge:chem:entropy-record"
SCHEMA_VERSION = "0.1"
PRODUCER_NAME = "anima-chem-langevin-thermodynamic-bridge"


@dataclass
class DemiurgeChemBridge:
    """Convert Langevin double-well + Arrhenius D-sweep → demiurge chem JSON.

    Usage:
        bridge = DemiurgeChemBridge(
            barrier_jumps_per_step=0.51,
            arrhenius_d_slope=7.69,
            ergodic_mean_position=0.187,
            backend="local_sim",
        )
        record = bridge.to_record()

    Skeleton scope: shape only; defaults mirror F-TH-1..5 PASS
    (state/s188g_engines_2026_05_21/thermodynamic.run.log).
    """

    # ─── required measured inputs ───
    # F-TH-2: D=0.6, 1000 steps → 510 jumps → 0.51 per step
    barrier_jumps_per_step: float = 0.51
    # F-TH-3: jumps(D=1.0)=722 / jumps(D=0.3)=94 = 7.68 (Arrhenius positive)
    arrhenius_d_slope: float = 7.69
    # F-TH-5: long-run ⟨x⟩ = -0.187 (|<x>| < 0.4 ergodic threshold)
    ergodic_mean_position: float = -0.187
    # double-well depth — anima Langevin default U(x) = (x²-1)² depth = 1
    free_energy_landscape_depth: float = 1.0

    # ─── provenance ───
    backend: str = "local_sim"    # local_sim | microfluidic_smd | dft_md
    seed: int = 42
    absorbed: bool = False

    # ─── optional measured extras ───
    diffusion_d: float = 0.6
    n_steps: int = 1000
    dt: float = 0.01
    sim_engine: str = "anima-physics:engines/thermodynamic_consciousness"
    sim_commit_hash: str = "local"

    scope_caveats: list[str] = field(default_factory=list)

    def gate_state(self) -> str:
        """measurement_gate per demiurge convention.

        - local_sim → GATE_OPEN (Langevin numpy reference, not real chemistry).
        - microfluidic_smd / dft_md → GATE_OPEN (real wet/compute, oracle TBD).
        """
        return "GATE_OPEN"

    def to_record(self) -> dict[str, Any]:
        caveats = list(self.scope_caveats) or [
            "Langevin double-well is consciousness-analog, NOT real chemistry",
            "barrier_jumps_per_step at single D point — full D-sweep regime 별도",
            "arrhenius_d_slope = 정성적 monotone, not k(T)=A·exp(-Ea/RT) fit",
            "no real molecular species — generic U(x)=(x²-1)² potential",
            "chem producer oracle parity not yet authored (TODO: demiurge rfc)",
        ]
        return {
            "interface": INTERFACE,
            "schema_version": SCHEMA_VERSION,
            "record_id": (
                f"chem_jumps{self.barrier_jumps_per_step:.2f}_"
                f"slope{self.arrhenius_d_slope:.2f}_"
                f"D{self.diffusion_d:.2f}_{self.backend}"
            ),
            "produced_at_utc": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "topology": {
                "kind": "langevin_double_well",
                "potential_form": "U(x) = (x^2 - 1)^2",
                "diffusion_d": self.diffusion_d,
                "n_steps": self.n_steps,
                "dt": self.dt,
            },
            "measurement": {
                "barrier_jumps_per_step": self.barrier_jumps_per_step,
                "arrhenius_d_slope": self.arrhenius_d_slope,
                "ergodic_mean_position": self.ergodic_mean_position,
                "free_energy_landscape_depth": self.free_energy_landscape_depth,
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
                    "@cite anima-physics:engines/thermodynamic_consciousness.hexa "
                    "(F-TH-1..5 5/5 PASS, state/s188g_engines_2026_05_21/"
                    "thermodynamic.run.log); "
                    "demiurge_hw_verify_2026_05_21 §2.2 (chem no-producer gap)"
                ),
                "consumer_target": "demiurge:chem:verify",
                "scope_caveats": caveats,
                "gate_failures": [],
            },
            "verdict": {
                "gate_state": self.gate_state(),
                "rationale": (
                    "skeleton emit — chem oracle parity TODO; "
                    f"jumps/step={self.barrier_jumps_per_step:.2f} "
                    f"arrhenius_slope={self.arrhenius_d_slope:.2f} "
                    f"D={self.diffusion_d:.2f} provisional"
                ),
            },
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_record(), indent=indent, sort_keys=True)


def _main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="demiurge_chem_bridge",
        description=(
            "Emit a demiurge:chem:entropy-record JSON (stdout or --output). "
            "Defaults mirror engines/thermodynamic_consciousness F-TH-1..5 PASS."
        ),
    )
    parser.add_argument(
        "--backend",
        default="local_sim",
        choices=("local_sim", "microfluidic_smd", "dft_md"),
    )
    parser.add_argument("--barrier-jumps-per-step", type=float, default=0.51)
    parser.add_argument("--arrhenius-d-slope", type=float, default=7.69)
    parser.add_argument("--ergodic-mean-position", type=float, default=-0.187)
    parser.add_argument("--free-energy-depth", type=float, default=1.0)
    parser.add_argument("--diffusion-d", type=float, default=0.6)
    parser.add_argument("--n-steps", type=int, default=1000)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="-", help="JSON file path or '-' for stdout")
    args = parser.parse_args()

    bridge = DemiurgeChemBridge(
        barrier_jumps_per_step=args.barrier_jumps_per_step,
        arrhenius_d_slope=args.arrhenius_d_slope,
        ergodic_mean_position=args.ergodic_mean_position,
        free_energy_landscape_depth=args.free_energy_depth,
        diffusion_d=args.diffusion_d,
        n_steps=args.n_steps,
        dt=args.dt,
        backend=args.backend,
        seed=args.seed,
    )
    text = bridge.to_json()
    if args.output == "-":
        sys.stdout.write(text + "\n")
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        sys.stderr.write(f"[demiurge_chem_bridge] wrote {args.output}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
