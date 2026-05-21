#!/usr/bin/env python3
"""demiurge_brain_bridge.py — anima kuramoto → demiurge brain producer bridge.

CONTEXT: `anima-physics/docs/demiurge_hw_verify_2026_05_21.md §2.2` 의
demiurge brain 도메인이 현재 ❌ no producer / engine gap. anima 측에서
이 gap 을 메우는 첫 step 으로, kuramoto local sim (Mac, $0) 결과를
demiurge brain producer 가 소비할 수 있는 JSON record 형식으로 변환하는
어댑터 stub.

SCOPE (skeleton only):
    (a) Mac local py_compile clean — demiurge daemon 부재해도 import 가능.
    (b) emit dict shape mirrors demiurge:chip:noc:F1F2-record provenance/
        gate/measurement 패턴 (interface = demiurge:brain:kuramoto-record).
    (c) 실 demiurge daemon 호출은 *별도 cycle* — 본 파일은 record JSON
        emit 까지 (file write 는 caller 책임).

SW source: anima-physics/social/kuramoto_coupling.hexa (§188 PASS 6/6)
Local sim: anima-physics/hw/kuramoto_neuromorphic/src/kuramoto_local_sim.py
HW adapters: kuramoto_akida_adapter.py + kuramoto_loihi2_adapter.py (cloud-only)

Future close-the-loop:
    Phase 2 cloud trial (Akida/Loihi 2) result → DemiurgeBrainBridge →
    demiurge brain consumer (`demiurge cli action verify brain`) → GATE_OPEN
    → GATE_CLOSED_MEASURED upgrade.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


# ─── record interface constant (mirror demiurge:chip:noc namespace) ────
INTERFACE = "demiurge:brain:kuramoto-record"
SCHEMA_VERSION = "0.1"
PRODUCER_NAME = "anima-kuramoto-loihi-akida-bridge"


@dataclass
class DemiurgeBrainBridge:
    """Convert kuramoto sim/HW result → demiurge brain producer JSON record.

    Usage:
        bridge = DemiurgeBrainBridge(
            n=8, k=2.0, steps=1000,
            r_tail=0.78, backend="local_sim",
        )
        record = bridge.to_record()
        # caller writes record to ~/core/demiurge/exports/brain/verify/<UTC>Z/

    Skeleton scope: shape only — does NOT invoke `demiurge cli` (별도 cycle).
    """

    # ─── required measured inputs ───
    n: int                       # oscillator count
    k: float                     # coupling strength
    steps: int                   # sim/HW step count
    r_tail: float                # Kuramoto order parameter (last-10% mean)

    # ─── provenance ───
    backend: str = "local_sim"   # one of: local_sim | akida_cloud | loihi2_nrc
    seed: int = 42
    absorbed: bool = False       # demiurge convention: false until GATE_CLOSED

    # ─── optional measured extras ───
    r_std_tail: float = 0.0      # std(r[last 100]) — F-HW-KU-5 stability
    sim_engine: str = "anima-physics:kuramoto_local_sim"
    sim_commit_hash: str = "local"

    # ─── caveats (honest C3 carry) ───
    scope_caveats: list[str] = field(default_factory=list)

    def gate_state(self) -> str:
        """Determine measurement_gate per demiurge convention.

        - local_sim    → GATE_OPEN (provisional, not silicon-validated)
        - cloud HW     → GATE_OPEN until oracle parity defined (TODO: brain rfc)
        - silicon ASIC → GATE_CLOSED_MEASURED (future, requires rfc_001 analog)
        """
        if self.backend == "local_sim":
            return "GATE_OPEN"
        if self.backend in ("akida_cloud", "loihi2_nrc"):
            # HW measured but oracle parity (cf. chip f1f2) not yet authored.
            return "GATE_OPEN"
        return "GATE_OPEN"

    def to_record(self) -> dict[str, Any]:
        """Emit demiurge-shaped record dict (caller writes to JSON file)."""
        caveats = list(self.scope_caveats) or [
            "kuramoto local sim is reference numpy, NOT silicon spike-event",
            "r_tail at single (N, K) point — not a full K-sweep regime claim",
            "brain producer oracle parity not yet authored (TODO: demiurge rfc)",
        ]
        return {
            "interface": INTERFACE,
            "schema_version": SCHEMA_VERSION,
            "record_id": f"kuramoto_n{self.n}_k{self.k:.2f}_{self.backend}",
            "produced_at_utc": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "topology": {
                "kind": "all_to_all",
                "n_oscillators": self.n,
                "coupling": self.k,
                "omega_mean": 1.0,
                "omega_std": 1.5,
            },
            "measurement": {
                "steps": self.steps,
                "dt": 0.01,
                "r_tail": self.r_tail,
                "r_std_tail": self.r_std_tail,
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
                    "@cite anima-physics:social/kuramoto_coupling.hexa §188; "
                    "demiurge_hw_verify_2026_05_21 §2.2 (brain no-producer gap)"
                ),
                "consumer_target": "demiurge:brain:verify",
                "scope_caveats": caveats,
                "gate_failures": [],
            },
            "verdict": {
                "gate_state": self.gate_state(),
                "rationale": (
                    "skeleton emit — brain oracle parity TODO; "
                    f"r_tail={self.r_tail:.3f} at K={self.k:.2f} provisional"
                ),
            },
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize record to JSON string (caller writes to file)."""
        return json.dumps(self.to_record(), indent=indent, sort_keys=True)


def _main() -> int:
    """CLI: emit a record to stdout or --output file.

    Defaults mirror `anima-physics/hw/kuramoto_neuromorphic/state/sim.log`
    F-HW-KU-3 locked-state measurement (K=5.0, N=8, steps=1000, r_tail=0.951).
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="demiurge_brain_bridge",
        description=(
            "Emit a demiurge:brain:kuramoto-record JSON "
            "(stdout or --output)."
        ),
    )
    parser.add_argument(
        "--backend",
        default="local_sim",
        choices=("local_sim", "akida_cloud", "loihi2_nrc"),
    )
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--k", type=float, default=5.0)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--r-tail", type=float, default=0.951)
    parser.add_argument("--r-std-tail", type=float, default=0.0434)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="-", help="JSON file path or '-' for stdout")
    args = parser.parse_args()

    bridge = DemiurgeBrainBridge(
        n=args.n,
        k=args.k,
        steps=args.steps,
        r_tail=args.r_tail,
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
        sys.stderr.write(f"[demiurge_brain_bridge] wrote {args.output}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
