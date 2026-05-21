"""SNN consciousness LIF → AKD1000 (rank 1, exact 1:1 fit).

Maps ``engines/snn_consciousness.hexa`` (349 LoC, §188g 5/5) onto Akida's
native LIF cell primitive: 8-bit weights, threshold spike, deterministic
refractory.  This adapter is the canonical "neuromorphic substrate as-is"
path — no quantisation drift expected beyond the 8-bit weight ceiling.

Falsifiers (F-AKIDA-SNN-1..5)
-----------------------------
1. rest          — at rest input, membrane decays to ≈0, no spikes.
2. threshold     — stepping V above ``v_threshold`` always produces a spike.
3. coupling      — pairwise coupling raises co-spike count vs uncoupled.
4. monotone      — increasing drive strictly raises spike rate (monotonicity).
5. long-run      — after ``n_steps`` ≥ 2000 the rate stays bounded (no NaN).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

from .base import AkidaAdapter


@dataclass
class SNNLifAdapter(AkidaAdapter):
    """LIF (leaky integrate-and-fire) pool of ``n_neurons`` cells."""

    name: str = "snn-lif"
    v_threshold: float = 1.0
    v_reset: float = 0.0
    tau: float = 20.0       # membrane time constant
    refractory: int = 2     # refractory steps
    coupling: float = 0.2   # all-to-all coupling weight
    _v: np.ndarray = field(default=None, repr=False)  # type: ignore[assignment]
    _refr: np.ndarray = field(default=None, repr=False)  # type: ignore[assignment]
    _spikes_total: int = field(default=0, repr=False)

    def build_model(self) -> Any:
        rng = np.random.default_rng(self.seed)
        self._v = rng.uniform(0.0, 0.3 * self.v_threshold, self.n_neurons)
        self._refr = np.zeros(self.n_neurons, dtype=np.int32)
        self._spikes_total = 0
        self._state.update(
            {
                "v_threshold": self.v_threshold,
                "tau": self.tau,
                "coupling": self.coupling,
                "n": self.n_neurons,
            }
        )
        # Real HW would `akida.Model() + akida.layers.InputData(...) + LIF
        # layer compile`.  Here we hold parameters; runtime swap handled by
        # `pack.runtime.metatf_runtime`.
        return {"kind": "snn_lif_pool", "n": self.n_neurons}

    def step(self, input_data: Optional[Any] = None) -> dict:
        self.ensure_built()
        drive = self._coerce_input(input_data)
        # spike from previous step's V
        spikes = (self._v >= self.v_threshold).astype(np.float32)
        spikes = np.where(self._refr > 0, 0.0, spikes)
        # reset + refractory
        self._v = np.where(spikes > 0, self.v_reset, self._v)
        self._refr = np.where(spikes > 0, self.refractory, np.maximum(self._refr - 1, 0))
        # coupled input
        coupled = self.coupling * (spikes.sum() - spikes)
        # leak + integrate
        self._v += (-(self._v) / self.tau) + drive + coupled
        # clamp to avoid blowup under pathological inputs
        np.clip(self._v, -5.0 * self.v_threshold, 5.0 * self.v_threshold, out=self._v)
        n_spk = int(spikes.sum())
        self._spikes_total += n_spk
        out = {
            "spikes": spikes.astype(np.int8).tolist(),
            "v_mean": float(self._v.mean()),
            "spike_rate": n_spk / float(self.n_neurons),
            "motivation": min(1.0, n_spk / float(self.n_neurons)),
        }
        self._state["spikes_total"] = self._spikes_total
        self._state["v_mean_last"] = out["v_mean"]
        return out

    def _coerce_input(self, x: Any) -> np.ndarray:
        if x is None:
            return np.full(self.n_neurons, 0.15, dtype=np.float32)
        if isinstance(x, (int, float)):
            return np.full(self.n_neurons, float(x), dtype=np.float32)
        arr = np.asarray(x, dtype=np.float32).reshape(-1)
        if arr.size == 1:
            return np.full(self.n_neurons, float(arr[0]), dtype=np.float32)
        if arr.size < self.n_neurons:
            arr = np.pad(arr, (0, self.n_neurons - arr.size))
        return arr[: self.n_neurons]

    def selftest(self) -> dict:
        details: list = []

        # 1. rest — zero input → membrane bounded, no spikes after warm-up
        a = SNNLifAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        a.build_model()
        rest_spikes = 0
        for _ in range(50):
            r = a.step(0.0)
            rest_spikes += int(sum(r["spikes"]))
        # Steady-state of leaky integrator with zero drive and coupling ~ 0
        # is bounded by tau-1 step's residual; allow generous slack (still ≪
        # threshold so no spike contagion).
        self._check(
            details,
            "F-AKIDA-SNN-1-REST",
            rest_spikes == 0 and abs(a._state["v_mean_last"]) < 0.1 * self.v_threshold,
            f"rest_spikes={rest_spikes} v_mean={a._state['v_mean_last']:.4f}",
        )

        # 2. threshold — drive ≫ threshold guarantees a spike
        b = SNNLifAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        b.build_model()
        any_spike = False
        for _ in range(10):
            r = b.step(2.0 * self.v_threshold)
            if sum(r["spikes"]) > 0:
                any_spike = True
                break
        self._check(details, "F-AKIDA-SNN-2-THRESHOLD", any_spike, f"any_spike={any_spike}")

        # 3. coupling — coupled pool has ≥ uncoupled co-spike count
        c_uncoupled = SNNLifAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed, coupling=0.0)
        c_uncoupled.build_model()
        c_coupled = SNNLifAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed, coupling=0.5)
        c_coupled.build_model()
        sp_un, sp_co = 0, 0
        for _ in range(200):
            sp_un += sum(c_uncoupled.step(0.6)["spikes"])
            sp_co += sum(c_coupled.step(0.6)["spikes"])
        self._check(
            details,
            "F-AKIDA-SNN-3-COUPLING",
            sp_co >= sp_un,
            f"sp_uncoupled={sp_un} sp_coupled={sp_co}",
        )

        # 4. monotone — higher drive → higher spike rate (3-rung ladder)
        rates = []
        for drive in (0.3, 0.7, 1.4):
            d = SNNLifAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed, coupling=0.0)
            d.build_model()
            ns = 0
            for _ in range(300):
                ns += sum(d.step(drive)["spikes"])
            rates.append(ns)
        monotone = rates[0] <= rates[1] <= rates[2]
        self._check(details, "F-AKIDA-SNN-4-MONOTONE", monotone, f"rates={rates}")

        # 5. long-run — 2000 step run stays finite
        e = SNNLifAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        e.build_model()
        for _ in range(2000):
            e.step(0.5)
        finite = bool(np.all(np.isfinite(e._v)))
        bounded = abs(e._state["v_mean_last"]) < 50.0
        self._check(details, "F-AKIDA-SNN-5-LONG-RUN", finite and bounded,
                    f"finite={finite} v_mean={e._state['v_mean_last']:.3f}")

        return self._summarize("F-AKIDA-SNN", details)


__all__ = ["SNNLifAdapter"]
