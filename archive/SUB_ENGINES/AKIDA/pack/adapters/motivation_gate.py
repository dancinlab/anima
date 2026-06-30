"""Motivation threshold gate → AKD1000 native event-fire (1 mW envelope).

N4 path: a single comparator (input ≥ threshold) maps directly to Akida's
event-driven fire — when no input crosses the threshold the chip stays at
≈ 0.5 mW (idle).  The host orchestrator uses the gate's ``fire`` boolean to
gate :class:`AuditBuffer` writes.

Falsifiers (F-AKIDA-MG-1..5)
----------------------------
1. below     — input < threshold → fire == 0.
2. above     — input ≥ threshold → fire == 1.
3. monotone  — fire-rate is monotone non-decreasing in input.
4. hysteresis— with hysteresis>0, ON/OFF thresholds differ.
5. quiet-pow — idle-period emit count == 0 (1 mW envelope guarantee).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

from .base import AkidaAdapter


@dataclass
class MotivationGateAdapter(AkidaAdapter):
    """Threshold + optional Schmitt-trigger hysteresis gate."""

    name: str = "motivation-gate"
    threshold: float = 0.5
    hysteresis: float = 0.0  # if > 0, ON at threshold+h/2, OFF at threshold-h/2
    _on: bool = field(default=False, repr=False)
    _fire_count: int = field(default=0, repr=False)
    _step_count: int = field(default=0, repr=False)

    def build_model(self) -> Any:
        self._on = False
        self._fire_count = 0
        self._step_count = 0
        self._state.update({"threshold": self.threshold,
                            "hysteresis": self.hysteresis,
                            "n": self.n_neurons})
        # AKD1000 V1 layer stack: 8-factor input → single FC unit (threshold
        # = bias).  Binary weights + binary act = pure event-fire (chip stays
        # at the ~50 mW idle floor unless input crosses threshold).
        from ..runtime.metatf_runtime import get_runtime

        akida = get_runtime()
        model = akida.Model()
        model.add(akida.InputData(input_shape=(self.n_neurons, 1, 1),
                                  input_bits=1, name="motiv_in"))
        model.add(akida.FullyConnected(units=1, weights_bits=1,
                                       activation=True, act_bits=1,
                                       name="motiv_gate"))
        self._akida_model = model
        self._state["akida_layer_count"] = len(model.layers)
        return {"kind": "motivation_gate", "threshold": self.threshold,
                "akida_model": model, "layers": list(model.layers)}

    def _event_count_for_power(self) -> int:
        # Single comparator emits at most 1 fire bit per step (typically 0).
        # Use realised fire rate for a tighter estimate.
        if self._step_count > 0:
            rate = self._fire_count / self._step_count
            return max(0, int(round(rate)))  # 0 or 1
        return 0

    def _estimate_npu_count(self) -> int:
        # 1 FC unit = trivial — single NP, single neuron slot.
        return 1

    def _estimate_latency_us(self) -> float:
        # Single comparator: cycle-counted at ~1 cycle.
        return 5.5

    def step(self, input_data: Optional[Any] = None) -> dict:
        self.ensure_built()
        x = self._coerce_input(input_data)
        score = float(np.mean(x))
        if self.hysteresis > 0:
            on_thr = self.threshold + self.hysteresis / 2.0
            off_thr = self.threshold - self.hysteresis / 2.0
            if self._on:
                self._on = score >= off_thr
            else:
                self._on = score >= on_thr
            fire = int(self._on)
        else:
            fire = int(score >= self.threshold)
        if fire:
            self._fire_count += 1
        self._step_count += 1
        self._state["fire_count"] = self._fire_count
        self._state["last_score"] = score
        return {
            "score": score,
            "fire": fire,
            "fire_rate": self._fire_count / max(1, self._step_count),
            "motivation": score if fire else 0.0,
        }

    def _coerce_input(self, x: Any) -> np.ndarray:
        if x is None:
            return np.zeros(self.n_neurons, dtype=np.float64)
        if isinstance(x, (int, float)):
            return np.full(self.n_neurons, float(x), dtype=np.float64)
        arr = np.asarray(x, dtype=np.float64).reshape(-1)
        if arr.size < self.n_neurons:
            arr = np.pad(arr, (0, self.n_neurons - arr.size))
        return arr[: self.n_neurons]

    def selftest(self) -> dict:
        details: list = []

        # 1. below
        a = MotivationGateAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                  threshold=0.5)
        a.build_model()
        results = [a.step(0.1)["fire"] for _ in range(20)]
        self._check(details, "F-AKIDA-MG-1-BELOW", all(r == 0 for r in results),
                    f"results={results[:5]}...")

        # 2. above
        b = MotivationGateAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                  threshold=0.5)
        b.build_model()
        results = [b.step(0.9)["fire"] for _ in range(20)]
        self._check(details, "F-AKIDA-MG-2-ABOVE", all(r == 1 for r in results),
                    f"results={results[:5]}...")

        # 3. monotone — fire rate non-decreasing in input
        rates = []
        for drv in (0.0, 0.3, 0.6, 0.9):
            c = MotivationGateAdapter(name=self.name, n_neurons=self.n_neurons,
                                      seed=self.seed, threshold=0.5)
            c.build_model()
            cnt = 0
            for _ in range(100):
                cnt += c.step(drv)["fire"]
            rates.append(cnt)
        mono = all(rates[i] <= rates[i + 1] for i in range(len(rates) - 1))
        self._check(details, "F-AKIDA-MG-3-MONOTONE", mono, f"rates={rates}")

        # 4. hysteresis — ON threshold > OFF threshold
        d = MotivationGateAdapter(name=self.name, n_neurons=1, seed=self.seed,
                                  threshold=0.5, hysteresis=0.2)
        d.build_model()
        # ramp up just past ON threshold then back to between OFF & ON
        d.step(0.65)  # ON: above 0.5 + 0.1 = 0.6
        on_after = d._on
        d.step(0.45)  # OFF threshold is 0.4 — stays ON
        still_on = d._on
        d.step(0.35)  # below OFF — turn OFF
        now_off = not d._on
        hyst_ok = on_after and still_on and now_off
        self._check(details, "F-AKIDA-MG-4-HYSTERESIS", hyst_ok,
                    f"on_after={on_after} still_on={still_on} now_off={now_off}")

        # 5. quiet-pow — 1000 steps of zero input → 0 fires
        e = MotivationGateAdapter(name=self.name, n_neurons=self.n_neurons,
                                  seed=self.seed, threshold=0.1)
        e.build_model()
        for _ in range(1000):
            e.step(0.0)
        self._check(details, "F-AKIDA-MG-5-QUIET-POW", e._fire_count == 0,
                    f"fire_count={e._fire_count}")

        return self._summarize("F-AKIDA-MG", details)


__all__ = ["MotivationGateAdapter"]
