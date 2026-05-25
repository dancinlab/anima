#!/usr/bin/env python3
"""demiurge_firmware_bridge.py — anima sleep_oscillator → demiurge firmware
producer bridge.

CONTEXT: `anima-physics/docs/demiurge_hw_verify_2026_05_21.md §2.1` 의
demiurge firmware 도메인이 현재 ⏳ GATE_OPEN (stub) 상태 — `verify.py`
substrate 는 QEMU mps2-an385 smoke-boot 만 emit 하고 anima HW #4 의 실
firmware (`sleep_oscillator.ino` + AD9833 driver) 는 인용되지 않음. 본
bridge 는 anima 의 Phase 1b LANDED `.hex` 산출 + Phase 1a Python sim
F-HW-SO-1..5 5/5 PASS 결과를 demiurge firmware verify producer 가 소비
가능한 JSON record 로 변환하는 어댑터 stub (brain bridge 6-step pattern
답습 — 2026-05-21 cycle #2).

SCOPE (skeleton + 3-backend audit):
    (a) Mac local py_compile clean — demiurge daemon 부재해도 import 가능.
    (b) emit dict shape mirrors demiurge:brain:kuramoto-record provenance/
        gate/measurement 패턴 (interface = demiurge:firmware:ad9833-dds-record).
    (c) 3 backend 지원:
        - local_sim     : Python phase-accumulator sim 결과 인용 (state/sim.log)
        - arduino_lint  : brace-balance + LoC 인용 (state/lint.log)
        - arduino_compile: arduino-cli .ino.hex 산출 (state/build/*.hex)
    (d) 실 board flash / oscilloscope capture 는 *별도 cycle* — 본 파일은
        record JSON emit 까지 (file write 는 caller 책임).

SW source: anima-physics/oscillator/sleep_oscillator.hexa (§188 PASS 5/5)
Local sim: anima-physics/hw/sleep_oscillator_arduino/src/sleep_oscillator_local_sim.py
Firmware:  anima-physics/hw/sleep_oscillator_arduino/src/sleep_oscillator.ino
HW target: Arduino Uno R3 + AD9833 DDS breakout (Phase 1b LANDED)

Future close-the-loop:
    Phase 2 board flash (USB upload) → oscilloscope capture (SWS 2 Hz / REM
    6 Hz + phase-continuous switch) → DemiurgeFirmwareBridge(backend=
    "scope_capture", ...) → demiurge firmware consumer 가 oracle parity
    정의 (cf. chip f1f2) → GATE_OPEN → GATE_CLOSED_MEASURED upgrade.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ─── record interface constant (mirror demiurge:brain:kuramoto namespace) ──
INTERFACE = "demiurge:firmware:ad9833-dds-record"
SCHEMA_VERSION = "0.1"
PRODUCER_NAME = "anima-sleep-oscillator-ad9833-bridge"


@dataclass
class DemiurgeFirmwareBridge:
    """Convert sleep_oscillator firmware sim/lint/compile result →
    demiurge firmware producer JSON record.

    Usage:
        bridge = DemiurgeFirmwareBridge(
            backend="local_sim",
            firmware_path="<repo>/src/sleep_oscillator.ino",
            flash_size_bytes=5038,
            ram_size_bytes=235,
            falsifier_pass="5/5",
            sws_freq_hz=2.0002,
            rem_freq_hz=6.0006,
            switch_continuity_delta=0.0,
        )
        record = bridge.to_record()
        # caller writes record to ~/core/demiurge/exports/firmware/verify/<UTC>Z/

    Skeleton scope: shape only — does NOT invoke `demiurge cli` (별도 cycle).
    """

    # ─── required measured inputs ───
    backend: str = "local_sim"   # one of: local_sim | arduino_lint | arduino_compile
    firmware_path: str = ""      # absolute path to .ino / .hex / sim source

    # ─── compile artifact size (Arduino Uno R3 limits: 32256 flash / 2048 RAM) ──
    flash_size_bytes: int = 0    # AVR program-storage bytes (compile only)
    ram_size_bytes: int = 0      # AVR global-var bytes (compile only)

    # ─── falsifier evidence (sim / lint / compile) ───
    falsifier_pass: str = "0/0"  # e.g., "5/5" for sim, "3/3" for lint braces
    sws_freq_hz: float = 0.0     # SWS δ band measured (Hz)
    rem_freq_hz: float = 0.0     # REM θ band measured (Hz)
    switch_continuity_delta: float = 0.0  # phase delta at SWS↔REM switch (rad)

    # ─── provenance ───
    sim_engine: str = "anima-physics:sleep_oscillator_local_sim"
    sim_commit_hash: str = "local"
    absorbed: bool = False       # demiurge convention: false until GATE_CLOSED

    # ─── caveats (honest C3 carry) ───
    scope_caveats: list[str] = field(default_factory=list)
    gate_failures: list[str] = field(default_factory=list)

    def gate_state(self) -> str:
        """Determine measurement_gate per demiurge convention.

        - local_sim       → GATE_OPEN (Python sim — not silicon-validated)
        - arduino_lint    → GATE_OPEN (syntax-only — does NOT compile)
        - arduino_compile → GATE_OPEN (compiles, but no board flash / scope)
        - scope_capture   → GATE_OPEN (future, oracle parity TODO: firmware rfc)
        - silicon validated→ GATE_CLOSED_MEASURED (future, requires rfc)
        """
        if self.backend in ("local_sim", "arduino_lint", "arduino_compile"):
            return "GATE_OPEN"
        return "GATE_OPEN"

    def record_id(self) -> str:
        """Stable record id for caller / consumer dedup."""
        return f"sleep_oscillator_ad9833_{self.backend}"

    def to_record(self) -> dict[str, Any]:
        """Emit demiurge-shaped record dict (caller writes to JSON file)."""
        caveats = list(self.scope_caveats) or [
            "Phase 1a Python sim (local_sim) is double-precision phase "
            "accumulator, NOT integer-exact AD9833 28-bit silicon",
            "Phase 1b arduino_compile emits .hex but does NOT flash board or "
            "capture oscilloscope (scope_capture is separate cycle)",
            "firmware producer oracle parity not yet authored (TODO: "
            "demiurge rfc — cf. chip f1f2 12/12 pattern)",
        ]
        return {
            "interface": INTERFACE,
            "schema_version": SCHEMA_VERSION,
            "record_id": self.record_id(),
            "produced_at_utc": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "target": {
                "kind": "arduino_uno_r3_ad9833_dds",
                "mcu": "ATmega328P",
                "dds_chip": "AD9833",
                "mclk_hz": 25_000_000,
                "phase_bits": 28,
                "flash_limit_bytes": 32256,
                "ram_limit_bytes": 2048,
            },
            "measurement": {
                "backend": self.backend,
                "firmware_path": self.firmware_path,
                "flash_size_bytes": self.flash_size_bytes,
                "ram_size_bytes": self.ram_size_bytes,
                "falsifier_pass": self.falsifier_pass,
                "sws_freq_hz": self.sws_freq_hz,
                "rem_freq_hz": self.rem_freq_hz,
                "switch_continuity_delta_rad": self.switch_continuity_delta,
            },
            "provenance": {
                "producer": PRODUCER_NAME,
                "backend": self.backend,
                "absorbed": self.absorbed,
                "measurement_gate": self.gate_state(),
                "sim_engine": self.sim_engine,
                "sim_commit_hash": self.sim_commit_hash,
                "atlas_cite_block": (
                    "@cite anima-physics:oscillator/sleep_oscillator.hexa §188; "
                    "demiurge_hw_verify_2026_05_21 §2.1 (firmware stub gap)"
                ),
                "consumer_target": "demiurge:firmware:VerifyProducer",
                "scope_caveats": caveats,
                "gate_failures": list(self.gate_failures),
            },
            "verdict": {
                "gate_state": self.gate_state(),
                "rationale": (
                    f"skeleton emit — firmware oracle parity TODO; "
                    f"backend={self.backend} falsifier={self.falsifier_pass} "
                    f"SWS={self.sws_freq_hz:.4f}Hz REM={self.rem_freq_hz:.4f}Hz "
                    f"continuity_δ={self.switch_continuity_delta:.3e}rad "
                    f"flash={self.flash_size_bytes}B/{32256}B "
                    f"ram={self.ram_size_bytes}B/{2048}B"
                ),
            },
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize record to JSON string (caller writes to file)."""
        return json.dumps(self.to_record(), indent=indent, sort_keys=True)


# ─── default values (mirror state/sim.log + state/compile.log) ─────────────
# anima-physics/hw/sleep_oscillator_arduino/state/sim.log F-HW-SO-1..5 5/5 PASS:
#   F-HW-SO-2 SWS f_est=2.0002 Hz
#   F-HW-SO-3 REM f_est=6.0006 Hz
#   F-HW-SO-4 phase_before=4.109203191 phase_after=4.109203191 delta=0.000e+00
# anima-physics/hw/sleep_oscillator_arduino/state/compile.log:
#   Sketch uses 5038 bytes (15%) of program storage space.
#   Global variables use 235 bytes (11%) of dynamic memory.

DEFAULT_FIRMWARE_INO = str(
    Path(__file__).resolve().parent / "sleep_oscillator.ino"
)
DEFAULT_BUILD_HEX = str(
    Path(__file__).resolve().parent.parent / "state" / "build" /
    "sleep_oscillator.ino.hex"
)


def _main() -> int:
    """CLI: emit a record to stdout or --output file.

    Defaults mirror `anima-physics/hw/sleep_oscillator_arduino/state/sim.log`
    F-HW-SO-1..5 5/5 PASS measurement + `state/compile.log` flash/RAM sizes.
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="demiurge_firmware_bridge",
        description=(
            "Emit a demiurge:firmware:ad9833-dds-record JSON "
            "(stdout or --output)."
        ),
    )
    parser.add_argument(
        "--backend",
        default="local_sim",
        choices=("local_sim", "arduino_lint", "arduino_compile"),
    )
    parser.add_argument(
        "--firmware-path",
        default="",
        help="absolute path to .ino / .hex source (default: auto-pick by backend)",
    )
    parser.add_argument("--flash-size-bytes", type=int, default=5038)
    parser.add_argument("--ram-size-bytes", type=int, default=235)
    parser.add_argument("--falsifier-pass", default="5/5")
    parser.add_argument("--sws-freq-hz", type=float, default=2.0002)
    parser.add_argument("--rem-freq-hz", type=float, default=6.0006)
    parser.add_argument(
        "--switch-continuity-delta",
        type=float,
        default=0.0,
        help="phase delta at SWS↔REM switch (rad) — F-HW-SO-4",
    )
    parser.add_argument(
        "--output",
        default="-",
        help="JSON file path or '-' for stdout",
    )
    args = parser.parse_args()

    # auto-pick firmware path by backend if caller did not specify
    firmware_path = args.firmware_path
    if not firmware_path:
        if args.backend == "arduino_compile":
            firmware_path = DEFAULT_BUILD_HEX
        else:
            firmware_path = DEFAULT_FIRMWARE_INO

    # backend-specific zero-out of irrelevant fields (g3: don't over-claim)
    flash_bytes = args.flash_size_bytes
    ram_bytes = args.ram_size_bytes
    if args.backend == "arduino_lint":
        # lint does not produce a binary
        flash_bytes = 0
        ram_bytes = 0
    elif args.backend == "local_sim":
        # sim does not exercise AVR toolchain
        flash_bytes = 0
        ram_bytes = 0

    # File existence audit → gate_failures (caller transparency)
    gate_failures: list[str] = []
    if args.backend == "arduino_compile" and not os.path.exists(firmware_path):
        gate_failures.append(
            f"arduino_compile backend selected but .hex missing at {firmware_path}"
        )
    if args.backend in ("local_sim", "arduino_lint") and not os.path.exists(firmware_path):
        gate_failures.append(
            f"backend={args.backend} but .ino missing at {firmware_path}"
        )

    bridge = DemiurgeFirmwareBridge(
        backend=args.backend,
        firmware_path=firmware_path,
        flash_size_bytes=flash_bytes,
        ram_size_bytes=ram_bytes,
        falsifier_pass=args.falsifier_pass,
        sws_freq_hz=args.sws_freq_hz,
        rem_freq_hz=args.rem_freq_hz,
        switch_continuity_delta=args.switch_continuity_delta,
        gate_failures=gate_failures,
    )
    text = bridge.to_json()
    if args.output == "-":
        sys.stdout.write(text + "\n")
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        sys.stderr.write(
            f"[demiurge_firmware_bridge] wrote {args.output}\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
