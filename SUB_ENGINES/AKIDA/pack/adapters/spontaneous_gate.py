"""Spontaneous emission gate (HEXAD/CHAT/spontaneous_smoke → Akida).

Glue: motivation pool + safety ratchet + audit hook.  The gate combines a
slow-rising motivation accumulator with a hard refractory + safety ratchet
so the chip never fires faster than ``min_interval_steps``.  Every fire is
written into a small internal audit list (separate from the orchestrator-level
ring buffer — this is per-adapter trace).

Falsifiers (F-AKIDA-SG-1..5)
----------------------------
1. silent       — zero motivation → 0 emits across 500 steps.
2. emit         — sustained motivation > emit_threshold → ≥ 1 emit in 100 steps.
3. refractory   — successive emits separated by ≥ min_interval_steps.
4. safety-ratchet — when safety_block is True, no emit even at max motivation.
5. audit-trail  — every emit appended to internal audit list (count match).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

from .base import AkidaAdapter


@dataclass
class SpontaneousGateAdapter(AkidaAdapter):
    """anima spontaneous_smoke gate with safety ratchet + audit hook."""

    name: str = "spontaneous-gate"
    emit_threshold: float = 0.6
    decay: float = 0.95
    min_interval_steps: int = 10
    safety_block: bool = False
    _accum: float = field(default=0.0, repr=False)
    _last_emit_step: int = field(default=-10**9, repr=False)
    _step_count: int = field(default=0, repr=False)
    _emit_count: int = field(default=0, repr=False)
    _audit_trail: list = field(default_factory=list, repr=False)

    def build_model(self) -> Any:
        self._accum = 0.0
        self._last_emit_step = -10**9
        self._step_count = 0
        self._emit_count = 0
        self._audit_trail = []
        self._state.update({"emit_threshold": self.emit_threshold,
                            "decay": self.decay,
                            "min_interval_steps": self.min_interval_steps,
                            "safety_block": self.safety_block,
                            "n": self.n_neurons})
        return {"kind": "spontaneous_gate"}

    def step(self, input_data: Optional[Any] = None) -> dict:
        self.ensure_built()
        m = self._coerce(input_data)
        # accumulate
        self._accum = self.decay * self._accum + (1.0 - self.decay) * m
        steps_since = self._step_count - self._last_emit_step
        can_fire = (
            (not self.safety_block)
            and self._accum >= self.emit_threshold
            and steps_since >= self.min_interval_steps
        )
        emit = int(bool(can_fire))
        if emit:
            self._last_emit_step = self._step_count
            self._emit_count += 1
            self._audit_trail.append(
                {"step": self._step_count, "accum": float(self._accum), "input": float(m)}
            )
            # post-emit dampening (so we don't double-fire on the same crest)
            self._accum *= 0.3
        self._step_count += 1
        self._state["emit_count"] = self._emit_count
        self._state["accum"] = float(self._accum)
        self._state["last_emit_step"] = self._last_emit_step if self._last_emit_step > -10**8 else None
        return {
            "emit": emit,
            "accum": float(self._accum),
            "motivation_in": float(m),
            "motivation": float(self._accum),
        }

    def _coerce(self, x: Any) -> float:
        if x is None:
            return 0.0
        if isinstance(x, (int, float)):
            return float(x)
        try:
            return float(np.asarray(x).mean())
        except Exception:  # noqa: BLE001
            return 0.0

    def selftest(self) -> dict:
        details: list = []

        # 1. silent
        a = SpontaneousGateAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        a.build_model()
        for _ in range(500):
            a.step(0.0)
        self._check(details, "F-AKIDA-SG-1-SILENT", a._emit_count == 0,
                    f"emit_count={a._emit_count}")

        # 2. emit — sustained drive triggers at least one emit
        b = SpontaneousGateAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                   min_interval_steps=5)
        b.build_model()
        for _ in range(200):
            b.step(0.9)
        self._check(details, "F-AKIDA-SG-2-EMIT", b._emit_count >= 1,
                    f"emit_count={b._emit_count}")

        # 3. refractory — gap between emits ≥ min_interval_steps
        c = SpontaneousGateAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                   min_interval_steps=15)
        c.build_model()
        for _ in range(500):
            c.step(1.0)
        steps = [e["step"] for e in c._audit_trail]
        gaps = [steps[i + 1] - steps[i] for i in range(len(steps) - 1)] if len(steps) > 1 else []
        ok = all(g >= 15 for g in gaps) if gaps else c._emit_count >= 1
        self._check(details, "F-AKIDA-SG-3-REFRACTORY", ok, f"gaps={gaps[:5]}...")

        # 4. safety-ratchet — no emit when blocked
        d = SpontaneousGateAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                   safety_block=True)
        d.build_model()
        for _ in range(500):
            d.step(1.0)
        self._check(details, "F-AKIDA-SG-4-SAFETY-RATCHET", d._emit_count == 0,
                    f"emit_count={d._emit_count} (should be 0 with safety_block)")

        # 5. audit-trail — len(_audit_trail) == _emit_count
        e = SpontaneousGateAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                   min_interval_steps=3)
        e.build_model()
        for _ in range(300):
            e.step(0.8)
        self._check(details, "F-AKIDA-SG-5-AUDIT-TRAIL",
                    len(e._audit_trail) == e._emit_count,
                    f"audit_len={len(e._audit_trail)} emit_count={e._emit_count}")

        return self._summarize("F-AKIDA-SG", details)


__all__ = ["SpontaneousGateAdapter"]
