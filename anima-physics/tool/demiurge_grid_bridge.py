#!/usr/bin/env python3
"""demiurge_grid_bridge.py — anima → demiurge grid producer bridge.

CONTEXT: `anima-physics/docs/demiurge_hw_verify_2026_05_21.md §2.2` 의
demiurge grid 도메인은 현재 ❌ no producer (`exports/grid/verify/`
경로 부재; `exports/grid/structure/` 만 존재 — 별 도메인). anima 측은
social/kuramoto_coupling (PHYS-P9-3 6/6 PASS) — N-node intersubjective
oscillator network — 가 그대로 power-grid synchronization analog 로
사용 가능 (Kuramoto = canonical power-grid model, Filatrella et al. 2008
"Analysis of a power grid using a Kuramoto-like model").

SCOPE (skeleton):
    (a) Mac local py_compile clean.
    (b) emit `demiurge:grid:resilience-record` (8-node power grid
        synchronization + phase coherence + resilience analog).
    (c) measurement key: phase_coherence_r ⊕ critical_coupling_k_c ⊕
        n_islanding_events ⊕ recovery_time_s (post-perturbation).
    (d) SW source = social/kuramoto_coupling.hexa (6/6 PASS) +
        hw/kuramoto_neuromorphic local sim (F-HW-KU-1..5 5/5).

Future close-the-loop:
    Phase 2 SCADA/PMU log replay (real distribution feeder data) →
    `--backend pmu_replay` → demiurge grid consumer (GridVerifyProducer.swift)
    → GATE_CLOSED_MEASURED upgrade.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


INTERFACE = "demiurge:grid:resilience-record"
SCHEMA_VERSION = "0.1"
PRODUCER_NAME = "anima-grid-kuramoto-powergrid-bridge"


@dataclass
class DemiurgeGridBridge:
    """Convert Kuramoto N-node → demiurge grid power-sync JSON.

    Usage:
        bridge = DemiurgeGridBridge(
            n_nodes=8, coupling_k=5.0,
            phase_coherence_r=0.951,
            critical_coupling_k_c=2.4,
            backend="local_sim",
        )
        record = bridge.to_record()

    Skeleton scope: shape only; defaults mirror F-HW-KU-3 locked-state
    (N=8, K=5.0, r_tail=0.951) reinterpreted as 8-node grid sync.
    """

    # ─── required measured inputs ───
    n_nodes: int = 8                       # power grid nodes (generators)
    coupling_k: float = 5.0                # transmission line coupling
    phase_coherence_r: float = 0.951       # 0..1 (Kuramoto order param)
    critical_coupling_k_c: float = 2.4     # transition threshold

    # ─── provenance ───
    backend: str = "local_sim"    # local_sim | pmu_replay | scada_log
    seed: int = 42
    absorbed: bool = False

    # ─── optional measured extras ───
    n_islanding_events: int = 0     # number of phase decouplings (post-perturb)
    recovery_time_s: float = 0.0    # time to re-sync after perturbation
    n_steps: int = 1000
    dt: float = 0.01
    r_std_tail: float = 0.0434      # stability metric (F-HW-KU-5)
    sim_engine: str = "anima-physics:social/kuramoto_coupling"
    sim_commit_hash: str = "local"

    scope_caveats: list[str] = field(default_factory=list)

    def gate_state(self) -> str:
        """measurement_gate per demiurge convention.

        - local_sim → GATE_OPEN (Kuramoto numpy, not real PMU/SCADA).
        - pmu_replay / scada_log → GATE_OPEN (real grid log, oracle TBD).
        """
        return "GATE_OPEN"

    def to_record(self) -> dict[str, Any]:
        caveats = list(self.scope_caveats) or [
            "Kuramoto N=8 is intersubjective oscillator analog, NOT real PMU/SCADA",
            "phase_coherence_r at single (N, K) point — full K-sweep 별도",
            "n_islanding_events=0 default — no perturbation injection in skeleton",
            "Filatrella 2008 Kuramoto-grid mapping = qualitative analog, not IEEE bus equivalent",
            "grid producer oracle parity not yet authored (TODO: demiurge rfc)",
        ]
        return {
            "interface": INTERFACE,
            "schema_version": SCHEMA_VERSION,
            "record_id": (
                f"grid_n{self.n_nodes}_k{self.coupling_k:.2f}_"
                f"r{self.phase_coherence_r:.3f}_{self.backend}"
            ),
            "produced_at_utc": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "topology": {
                "kind": "kuramoto_powergrid_analog",
                "n_nodes": self.n_nodes,
                "coupling_k": self.coupling_k,
                "critical_coupling_k_c": self.critical_coupling_k_c,
                "omega_mean": 1.0,
                "omega_std": 1.5,
            },
            "measurement": {
                "phase_coherence_r": self.phase_coherence_r,
                "r_std_tail": self.r_std_tail,
                "n_islanding_events": self.n_islanding_events,
                "recovery_time_s": self.recovery_time_s,
                "n_steps": self.n_steps,
                "dt": self.dt,
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
                    "@cite anima-physics:social/kuramoto_coupling.hexa "
                    "(PHYS-P9-3 6/6 PASS) + hw/kuramoto_neuromorphic "
                    "(F-HW-KU-1..5 5/5); Filatrella 2008 "
                    "Kuramoto-power-grid mapping; "
                    "demiurge_hw_verify_2026_05_21 §2.2 (grid no-producer gap)"
                ),
                "consumer_target": "demiurge:grid:verify",
                "scope_caveats": caveats,
                "gate_failures": [],
            },
            "verdict": {
                "gate_state": self.gate_state(),
                "rationale": (
                    "skeleton emit — grid oracle parity TODO; "
                    f"r={self.phase_coherence_r:.3f} @ K={self.coupling_k:.2f} "
                    f"K_c={self.critical_coupling_k_c:.2f} provisional"
                ),
            },
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_record(), indent=indent, sort_keys=True)


def _main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="demiurge_grid_bridge",
        description=(
            "Emit a demiurge:grid:resilience-record JSON (stdout or --output). "
            "Defaults mirror Kuramoto N=8 K=5.0 sync (F-HW-KU-3 locked-state) "
            "reinterpreted as 8-node power grid resilience."
        ),
    )
    parser.add_argument(
        "--backend",
        default="local_sim",
        choices=("local_sim", "pmu_replay", "scada_log"),
    )
    parser.add_argument("--n-nodes", type=int, default=8)
    parser.add_argument("--coupling-k", type=float, default=5.0)
    parser.add_argument("--phase-coherence-r", type=float, default=0.951)
    parser.add_argument("--critical-coupling-k-c", type=float, default=2.4)
    parser.add_argument("--n-islanding-events", type=int, default=0)
    parser.add_argument("--recovery-time-s", type=float, default=0.0)
    parser.add_argument("--n-steps", type=int, default=1000)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--r-std-tail", type=float, default=0.0434)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="-", help="JSON file path or '-' for stdout")
    args = parser.parse_args()

    bridge = DemiurgeGridBridge(
        n_nodes=args.n_nodes,
        coupling_k=args.coupling_k,
        phase_coherence_r=args.phase_coherence_r,
        critical_coupling_k_c=args.critical_coupling_k_c,
        n_islanding_events=args.n_islanding_events,
        recovery_time_s=args.recovery_time_s,
        n_steps=args.n_steps,
        dt=args.dt,
        r_std_tail=args.r_std_tail,
        backend=args.backend,
        seed=args.seed,
    )
    text = bridge.to_json()
    if args.output == "-":
        sys.stdout.write(text + "\n")
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        sys.stderr.write(f"[demiurge_grid_bridge] wrote {args.output}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
