"""Regression coverage for retired-runtime functionality now owned by Python."""

from __future__ import annotations

import pathlib
import sys
import time

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from akida_emit_bridge import AkidaEmitBridge  # noqa: E402
from anima_imagination_loop import ImaginationLoop  # noqa: E402
from anima_dream_stage import (  # noqa: E402
    STAGE_N1,
    STAGE_N2,
    STAGE_N3,
    STAGE_REM,
    STAGE_WAKE,
    dream_context_at,
    dream_stage_now,
    stage_at_offset,
)


def test_akida_bridge_opens_on_spike_edge_and_falls_back_when_stale():
    bridge = AkidaEmitBridge(spike_edge_n=4, gate_hold_s=0.5, stale_after_s=2.0)

    bridge.feed({"n_spikes": 2}, now=10.0)
    assert bridge.hw_gate(now=10.0) is False
    bridge.feed({"n_spikes": 2}, now=10.1)
    assert bridge.hw_gate(now=10.1) is True
    assert bridge.hw_gate(now=10.7) is False
    assert bridge.hw_gate(now=12.2) is True


def test_akida_bridge_rejects_invalid_telemetry():
    bridge = AkidaEmitBridge()
    with pytest.raises(TypeError):
        bridge.feed([])  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        bridge.feed({"n_spikes": -1})


def test_dream_stage_cycle_and_context_contract():
    assert stage_at_offset(0) == STAGE_N1
    assert stage_at_offset(300) == STAGE_N2
    assert stage_at_offset(1800) == STAGE_N3
    assert stage_at_offset(3600) == STAGE_N2
    assert stage_at_offset(5100) == STAGE_REM
    assert stage_at_offset(5400) == STAGE_N1

    n3 = dream_context_at(STAGE_N3, 0.0)
    rem = dream_context_at(STAGE_REM, 0.0)
    assert n3["phi"] == 0.15
    assert n3["tension_envelope"] == 0.2
    assert n3["scrambled"] is False
    assert rem["scrambled"] is True
    assert isinstance(n3["phi_envelope"], float)


def test_dream_stage_now_fails_safe_to_wake_for_closed_window():
    assert dream_stage_now(now=time.time(), window_value="00:00-00:00") == STAGE_WAKE


def test_imagination_loop_replays_context_without_emission():
    loop = ImaginationLoop(max_cells=4)
    assert loop.tick() is None

    loop.observe("first internal context")
    first = loop.tick()
    loop.observe("완전히 다른 두 번째 맥락")
    second = loop.tick()

    assert first is not None and second is not None
    assert first["emit_count"] == second["emit_count"] == 0
    assert first["rehearsal_kind"] == "internal_silent"
    assert loop.total_replays == 2
    assert second["cells_after"] >= first["cells_after"]
