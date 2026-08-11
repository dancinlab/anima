"""Convert AKD1000 spike telemetry into the participant's emit co-gate."""

from __future__ import annotations

import time
from collections import deque
from typing import Any

WINDOW_S = 1.0
SPIKE_EDGE_N = 40
GATE_HOLD_S = 0.6
STALE_AFTER_S = 5.0


class AkidaEmitBridge:
    """Maintain a sliding spike window without owning model state."""

    def __init__(
        self,
        window_s: float = WINDOW_S,
        spike_edge_n: int = SPIKE_EDGE_N,
        gate_hold_s: float = GATE_HOLD_S,
        stale_after_s: float = STALE_AFTER_S,
        gate_when_idle: bool = True,
    ) -> None:
        if window_s <= 0 or spike_edge_n <= 0 or gate_hold_s < 0 or stale_after_s <= 0:
            raise ValueError("invalid Akida emit-bridge timing or threshold")
        self.window_s = window_s
        self.spike_edge_n = spike_edge_n
        self.gate_hold_s = gate_hold_s
        self.stale_after_s = stale_after_s
        self.gate_when_idle = gate_when_idle
        self._events: deque[tuple[float, int]] = deque()
        self._last_feed_ts: float | None = None
        self._edge_until = 0.0

    def feed(self, akida_msg: dict[str, Any], now: float | None = None) -> None:
        """Ingest one validated broker telemetry message."""
        if not isinstance(akida_msg, dict):
            raise TypeError("akida telemetry must be a mapping")
        now = time.monotonic() if now is None else float(now)
        n_spikes = int(akida_msg.get("n_spikes", 0) or 0)
        if n_spikes < 0:
            raise ValueError("n_spikes must be non-negative")
        self._events.append((now, n_spikes))
        self._last_feed_ts = now
        self._prune(now)
        if self._window_count(now) >= self.spike_edge_n:
            self._edge_until = now + self.gate_hold_s

    def hw_gate(self, now: float | None = None) -> bool:
        """Return the held hardware edge, or the software-safe idle policy."""
        now = time.monotonic() if now is None else float(now)
        if self._last_feed_ts is None or now - self._last_feed_ts > self.stale_after_s:
            return self.gate_when_idle
        self._prune(now)
        return now <= self._edge_until

    def state(self, now: float | None = None) -> dict[str, Any]:
        now = time.monotonic() if now is None else float(now)
        stale = self._last_feed_ts is None or now - self._last_feed_ts > self.stale_after_s
        return {
            "hw_gate": self.hw_gate(now),
            "window_spikes": self._window_count(now),
            "edge_active": now <= self._edge_until,
            "stale": stale,
            "gate_when_idle": self.gate_when_idle,
        }

    def _prune(self, now: float) -> None:
        cutoff = now - self.window_s
        while self._events and self._events[0][0] < cutoff:
            self._events.popleft()

    def _window_count(self, now: float) -> int:
        self._prune(now)
        return sum(n_spikes for _, n_spikes in self._events)
