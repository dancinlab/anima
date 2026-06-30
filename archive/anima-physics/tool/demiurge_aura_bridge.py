#!/usr/bin/env python3
"""demiurge_aura_bridge.py — anima → demiurge aura producer bridge (stub).

CONTEXT: `anima-physics/docs/demiurge_hw_verify_2026_05_21.md §2.2` 의
demiurge aura 도메인은 현재 ⏳ engine gap — sibling-repo dispatch
`~/core/hexa-aura/verify/run_all.hexa` exit=1 (cockpit verify/*.hexa
경로 부재). anima-physics 측에는 aura quality/affect substrate 의
1급 source 가 부재 (hexa-aura 가 SSOT).

SCOPE (stub only — substrate 부재 명시):
    (a) Mac local py_compile clean — demiurge daemon 부재해도 import 가능.
    (b) emit dict shape mirrors `demiurge:aura:eeg-record` ⊕
        `demiurge:aura:quality-record` 패턴 (interface =
        `demiurge:aura:quality-record`).
    (c) anima 측 substrate 부재로 measurement 는 placeholder 만; 실
        EEG/affect 측정은 hexa-aura repo 의 별도 cycle 에서.
    (d) `scope_caveats` 에 'anima 측 aura substrate 부재' 명시 — over-claim 차단.

SW source: 없음 (anima 측 aura substrate 미보유, hexa-aura 가 SSOT).
Future: hexa-aura 의 `cli/aura quality` output → bridge → demiurge record.

Why a stub-only bridge? — engine-gap 의 첫 1-step 해소 (❌→⏳) 가
demiurge cli action verify aura 가 record JSON 을 인용·파싱할 수
있도록 만들기 위함. 측정 진실성은 별도 hexa-aura cycle 의존.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


INTERFACE = "demiurge:aura:quality-record"
SCHEMA_VERSION = "0.1"
PRODUCER_NAME = "anima-aura-stub-bridge"


@dataclass
class DemiurgeAuraBridge:
    """Convert (placeholder) aura quality/affect measurement → demiurge JSON.

    Usage:
        bridge = DemiurgeAuraBridge(
            quality=0.0, affect_valence=0.0, affect_arousal=0.0,
            backend="local_sim",
        )
        record = bridge.to_record()
        # caller writes to ~/core/demiurge/exports/aura/verify/<UTC>Z/

    Skeleton scope: shape only — anima 측 aura substrate 부재로
    measurement 는 placeholder. 실측은 hexa-aura repo 별도 cycle.
    """

    # ─── required measured inputs (placeholder defaults) ───
    quality: float = 0.0          # 0.0..1.0 normalized aura quality index
    affect_valence: float = 0.0   # -1.0..1.0 (negative..positive)
    affect_arousal: float = 0.0   # 0.0..1.0 (calm..excited)

    # ─── provenance ───
    backend: str = "local_sim"    # local_sim | muse_eeg | openbci_8ch
    seed: int = 42
    absorbed: bool = False

    # ─── optional ───
    n_channels: int = 0           # 0 = stub, EEG ≥ 4
    sample_rate_hz: int = 0       # 0 = stub
    duration_s: float = 0.0       # 0 = stub
    sim_engine: str = "anima-physics:aura_stub (substrate not present)"
    sim_commit_hash: str = "local"

    scope_caveats: list[str] = field(default_factory=list)

    def gate_state(self) -> str:
        """measurement_gate per demiurge convention.

        - local_sim (stub) → GATE_OPEN (no real measurement)
        - muse_eeg / openbci_8ch → GATE_OPEN (HW measured, oracle TBD)
        """
        return "GATE_OPEN"

    def to_record(self) -> dict[str, Any]:
        caveats = list(self.scope_caveats) or [
            "anima-physics has NO aura substrate — this is a stub-only bridge",
            "real quality/affect measurement lives in hexa-aura sibling repo",
            "aura producer oracle parity not yet authored (TODO: demiurge rfc)",
            "values quality=0 / valence=0 / arousal=0 = placeholder, NOT measurement",
        ]
        return {
            "interface": INTERFACE,
            "schema_version": SCHEMA_VERSION,
            "record_id": f"aura_q{self.quality:.2f}_v{self.affect_valence:+.2f}_a{self.affect_arousal:.2f}_{self.backend}",
            "produced_at_utc": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "topology": {
                "kind": "eeg_stub",
                "n_channels": self.n_channels,
                "sample_rate_hz": self.sample_rate_hz,
                "duration_s": self.duration_s,
            },
            "measurement": {
                "quality": self.quality,
                "affect_valence": self.affect_valence,
                "affect_arousal": self.affect_arousal,
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
                    "@cite anima-physics:tool/demiurge_aura_bridge.py "
                    "(stub — anima 측 aura substrate 부재); "
                    "demiurge_hw_verify_2026_05_21 §2.2 (aura engine gap)"
                ),
                "consumer_target": "demiurge:aura:verify",
                "scope_caveats": caveats,
                "gate_failures": [
                    "anima-physics has no aura substrate (hexa-aura repo is SSOT)",
                ],
            },
            "verdict": {
                "gate_state": self.gate_state(),
                "rationale": (
                    "stub emit — anima 측 aura substrate 부재; "
                    "engine-gap 1-step 해소용 placeholder record"
                ),
            },
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_record(), indent=indent, sort_keys=True)


def _main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="demiurge_aura_bridge",
        description=(
            "Emit a demiurge:aura:quality-record JSON (stub — anima 측 "
            "aura substrate 부재; placeholder for engine-gap 1-step 해소)."
        ),
    )
    parser.add_argument(
        "--backend",
        default="local_sim",
        choices=("local_sim", "muse_eeg", "openbci_8ch"),
    )
    parser.add_argument("--quality", type=float, default=0.0)
    parser.add_argument("--affect-valence", type=float, default=0.0)
    parser.add_argument("--affect-arousal", type=float, default=0.0)
    parser.add_argument("--n-channels", type=int, default=0)
    parser.add_argument("--sample-rate-hz", type=int, default=0)
    parser.add_argument("--duration-s", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="-", help="JSON file path or '-' for stdout")
    args = parser.parse_args()

    bridge = DemiurgeAuraBridge(
        quality=args.quality,
        affect_valence=args.affect_valence,
        affect_arousal=args.affect_arousal,
        n_channels=args.n_channels,
        sample_rate_hz=args.sample_rate_hz,
        duration_s=args.duration_s,
        backend=args.backend,
        seed=args.seed,
    )
    text = bridge.to_json()
    if args.output == "-":
        sys.stdout.write(text + "\n")
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        sys.stderr.write(f"[demiurge_aura_bridge] wrote {args.output}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
