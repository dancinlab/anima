"""Python sleep-stage context supplier for the chat participant."""

from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

_CORE = Path(__file__).resolve().parents[3] / "core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))
from dream_envelope_ctx import dr_stage_phi_context

STAGE_WAKE = "WAKE"
STAGE_N1 = "N1"
STAGE_N2 = "N2"
STAGE_N3 = "N3"
STAGE_REM = "REM"
STAGES = (STAGE_WAKE, STAGE_N1, STAGE_N2, STAGE_N3, STAGE_REM)
CYCLE_SEC = 5400

_PHI = {STAGE_WAKE: 1.0, STAGE_N1: 0.7, STAGE_N2: 0.4,
        STAGE_N3: 0.15, STAGE_REM: 0.95}
_TENSION_ENVELOPE = {STAGE_WAKE: 1.0, STAGE_N1: 0.7, STAGE_N2: 0.4,
                     STAGE_N3: 0.2, STAGE_REM: 0.9}
_TEMPERATURE = {STAGE_WAKE: 1.0, STAGE_N1: 0.9, STAGE_N2: 0.8,
                STAGE_N3: 0.6, STAGE_REM: 1.5}
_STAGE_INDEX = {stage: index for index, stage in enumerate(STAGES)}


@dataclass(frozen=True)
class SleepWindow:
    start_minute: int
    end_minute: int


def _parse_hhmm(value: str) -> int:
    parts = value.split(":")
    if len(parts) != 2 or not all(part.isdigit() for part in parts):
        raise ValueError("sleep time must use HH:MM")
    hour, minute = map(int, parts)
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError("sleep time is outside the clock range")
    return hour * 60 + minute


def sleep_window(value: str | None = None) -> SleepWindow:
    raw = value if value is not None else os.environ.get("ANIMA_SLEEP_HOURS", "22:00-06:00")
    try:
        start, end = raw.split("-", 1)
        return SleepWindow(_parse_hhmm(start), _parse_hhmm(end))
    except (TypeError, ValueError):
        return SleepWindow(22 * 60, 6 * 60)


def _in_sleep(minute_of_day: int, window: SleepWindow) -> bool:
    if window.start_minute == window.end_minute:
        return False
    if window.start_minute < window.end_minute:
        return window.start_minute <= minute_of_day < window.end_minute
    return minute_of_day >= window.start_minute or minute_of_day < window.end_minute


def stage_at_offset(offset_seconds: int) -> str:
    phase = max(0, int(offset_seconds)) % CYCLE_SEC
    if phase < 300:
        return STAGE_N1
    if phase < 1800:
        return STAGE_N2
    if phase < 3600:
        return STAGE_N3
    if phase < 5100:
        return STAGE_N2
    return STAGE_REM


def dream_stage_now(now: float | None = None, window_value: str | None = None) -> str:
    """Resolve the current stage directly; no sidecar writer is required."""
    timestamp = time.time() if now is None else float(now)
    local = time.localtime(timestamp)
    minute = local.tm_hour * 60 + local.tm_min
    window = sleep_window(window_value)
    if not _in_sleep(minute, window):
        return STAGE_WAKE
    elapsed_minutes = (minute - window.start_minute) % (24 * 60)
    elapsed_seconds = elapsed_minutes * 60 + local.tm_sec
    return stage_at_offset(elapsed_seconds)


def dream_context_at(stage: str, timestamp: float | None = None) -> dict[str, object]:
    stage = stage if stage in _STAGE_INDEX else STAGE_WAKE
    t = time.time() if timestamp is None else float(timestamp)
    return {
        "phi": _PHI[stage],
        "tension_envelope": _TENSION_ENVELOPE[stage],
        "scrambled": stage == STAGE_REM,
        "phi_envelope": dr_stage_phi_context(_STAGE_INDEX[stage], t),
        "stage": stage,
    }


def dream_emit_temperature(stage: str) -> float:
    return _TEMPERATURE.get(stage, _TEMPERATURE[STAGE_WAKE])
