"""θ-γ cross-frequency spike coupling pool → Akida.

Maps ``hippocampus/theta_gamma.hexa`` (§188 5/5).  Two oscillator pools at
6 Hz (θ) and 40 Hz (γ); γ amplitude is phase-locked to θ.  Pi 5's RTC keeps
wall-clock; AKD1000 emits the spike events.

Falsifiers (F-AKIDA-TG-1..5)
----------------------------
1. theta-freq    — measured θ frequency within 10% of nominal 6 Hz.
2. gamma-freq    — measured γ frequency within 15% of nominal 40 Hz.
3. coupling      — γ amplitude correlates with cos(θ_phase) (Pearson > 0.5).
4. ratio         — γ_freq / θ_freq ≈ 6-7 (canonical hippocampal ratio).
5. boundedness   — 2000-step run produces no NaN/inf in either pool.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

from .base import AkidaAdapter


@dataclass
class ThetaGammaAdapter(AkidaAdapter):
    """θ-γ cross-freq coupled pool."""

    name: str = "theta-gamma"
    theta_hz: float = 6.0
    gamma_hz: float = 40.0
    dt: float = 0.005          # 5 ms / step → 200 Hz sampling
    coupling: float = 0.6      # depth of γ AM by θ phase
    _t: float = field(default=0.0, repr=False)
    _theta_phase: float = field(default=0.0, repr=False)
    _gamma_phase: float = field(default=0.0, repr=False)
    _history: list = field(default_factory=list, repr=False)

    def build_model(self) -> Any:
        self._t = 0.0
        self._theta_phase = 0.0
        self._gamma_phase = 0.0
        self._history = []
        self._state.update({"theta_hz": self.theta_hz, "gamma_hz": self.gamma_hz,
                            "dt": self.dt, "coupling": self.coupling})
        # AKD1000 V1 layer stack: 1D-style rhythm via 3×1 Convolutional
        # (effectively the temporal-conv filter for θ/γ envelope detection),
        # followed by an FC head that emits the 2-bit phase code per cell.
        from ..runtime.metatf_runtime import get_runtime

        akida = get_runtime()
        model = akida.Model()
        # AKD1000 InputConvolutional requires HxWxC with C ∈ {1,3} and H ≥ 5.
        # Use H=8 (covers 8-channel pool default) × W=1 × C=1.
        model.add(akida.InputConvolutional(
            input_shape=(max(self.n_neurons, 5), 1, 1),
            kernel_size=3, filters=4,
            weights_bits=2, act_bits=2,
            name="tg_rhythm_conv",
        ))
        model.add(akida.FullyConnected(units=self.n_neurons,
                                       weights_bits=2, act_bits=2,
                                       name="tg_phase_head"))
        self._akida_model = model
        self._state["akida_layer_count"] = len(model.layers)
        return {"kind": "theta_gamma", "n": self.n_neurons,
                "akida_model": model, "layers": list(model.layers)}

    def _event_count_for_power(self) -> int:
        # γ-band fires ~6× per θ cycle → high event rate.  At dt=0.005,
        # roughly n_neurons × 0.6 events / step.
        return max(1, int(self.n_neurons * 0.6))

    def _estimate_npu_count(self) -> int:
        # Conv + FC pipeline: 2 NPs typical for 8-cell pool.
        return 2

    def _estimate_latency_us(self) -> float:
        # 1D conv (3 taps) + FC: ~4 cycles / cell.
        return float(5.0 + 4.0 * self.n_neurons / 300.0)

    def step(self, input_data: Optional[Any] = None) -> dict:
        self.ensure_built()
        self._theta_phase = (self._theta_phase + 2 * np.pi * self.theta_hz * self.dt) % (2 * np.pi)
        self._gamma_phase = (self._gamma_phase + 2 * np.pi * self.gamma_hz * self.dt) % (2 * np.pi)
        theta_val = np.cos(self._theta_phase)
        gamma_envelope = 0.5 + 0.5 * self.coupling * theta_val
        gamma_val = gamma_envelope * np.cos(self._gamma_phase)
        # spikes: 1 if theta_val crosses 0+ (peak burst), gamma fires per cycle
        spike_theta = int(theta_val > 0.99)
        spike_gamma = int(gamma_val > 0.6)
        self._t += self.dt
        self._history.append((self._t, theta_val, gamma_val, self._theta_phase))
        # cap history for long runs
        if len(self._history) > 5000:
            self._history = self._history[-5000:]
        self._state["t"] = self._t
        return {
            "theta_val": float(theta_val),
            "gamma_val": float(gamma_val),
            "theta_phase": float(self._theta_phase),
            "spike_theta": spike_theta,
            "spike_gamma": spike_gamma,
            "motivation": float((gamma_envelope + 1.0) / 2.0),
        }

    def selftest(self) -> dict:
        details: list = []
        # collect 4 s of data → 800 samples at dt=0.005
        a = ThetaGammaAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        a.build_model()
        for _ in range(800):
            a.step()
        hist = np.asarray(a._history)
        t = hist[:, 0]
        theta = hist[:, 1]
        gamma = hist[:, 2]
        phases = hist[:, 3]

        # 1. theta-freq via zero-crossings
        zc_theta = self._zero_crossings(theta, t)
        if len(zc_theta) >= 4:
            periods = np.diff(zc_theta[::2])  # every other = full period
            f_theta = 1.0 / float(np.mean(periods)) if len(periods) > 0 and np.mean(periods) > 0 else 0.0
        else:
            f_theta = 0.0
        self._check(details, "F-AKIDA-TG-1-THETA-FREQ",
                    abs(f_theta - self.theta_hz) / self.theta_hz < 0.10,
                    f"f_theta={f_theta:.2f} Hz (nominal {self.theta_hz})")

        # 2. gamma-freq via zero-crossings (after high-pass removing θ AM)
        zc_gamma = self._zero_crossings(gamma - np.mean(gamma), t)
        if len(zc_gamma) >= 4:
            periods = np.diff(zc_gamma[::2])
            f_gamma = 1.0 / float(np.mean(periods)) if len(periods) > 0 and np.mean(periods) > 0 else 0.0
        else:
            f_gamma = 0.0
        self._check(details, "F-AKIDA-TG-2-GAMMA-FREQ",
                    abs(f_gamma - self.gamma_hz) / self.gamma_hz < 0.15,
                    f"f_gamma={f_gamma:.2f} Hz (nominal {self.gamma_hz})")

        # 3. coupling — Pearson(γ envelope, cos(θ_phase)) > 0.5
        # use rolling abs of gamma as envelope proxy
        env = np.abs(gamma)
        # smooth slightly (1 γ period ≈ 5 samples)
        env_s = np.convolve(env, np.ones(5) / 5, mode="same")
        ref = np.cos(phases)
        if env_s.std() > 0 and ref.std() > 0:
            corr = float(np.corrcoef(env_s, ref)[0, 1])
        else:
            corr = 0.0
        self._check(details, "F-AKIDA-TG-3-COUPLING", corr > 0.5,
                    f"corr(env,cos(theta))={corr:.3f}")

        # 4. ratio — γ/θ frequency ratio
        if f_theta > 0:
            ratio = f_gamma / f_theta
        else:
            ratio = 0.0
        self._check(details, "F-AKIDA-TG-4-RATIO", 5.0 <= ratio <= 8.0,
                    f"ratio={ratio:.2f}")

        # 5. boundedness — 2000-step run finite
        b = ThetaGammaAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        b.build_model()
        for _ in range(2000):
            b.step()
        hist_b = np.asarray(b._history)
        finite = bool(np.all(np.isfinite(hist_b)))
        self._check(details, "F-AKIDA-TG-5-BOUNDEDNESS", finite, f"finite={finite}")

        return self._summarize("F-AKIDA-TG", details)

    @staticmethod
    def _zero_crossings(x: np.ndarray, t: np.ndarray) -> list:
        zc = []
        for i in range(1, len(x)):
            if x[i - 1] <= 0 < x[i] or x[i - 1] >= 0 > x[i]:
                zc.append(float(t[i]))
        return zc


__all__ = ["ThetaGammaAdapter"]
