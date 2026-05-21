"""Kuramoto coupled-oscillator pool → 1024 NPU.

Maps ``social/kuramoto_coupling.hexa`` (509 LoC, §188 6/6).  Each NPU holds a
phase oscillator θ_i with intrinsic ω_i; the order parameter r drives
"motivation" — high r (synchrony) → emit candidate.

Falsifiers (F-AKIDA-KU-1..5)
----------------------------
1. drift     — at K=0 phases drift independently (r stays low after warm-up).
2. sync      — at K ≫ K_c the order parameter r approaches 1.
3. r-bounded — r ∈ [0, 1] for every step of a 1000-step run.
4. K-monoton — mean r is monotone non-decreasing in K across 4 rungs.
5. seed-stable — repeating with same seed reproduces r bit-for-bit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

from .base import AkidaAdapter


@dataclass
class KuramotoAdapter(AkidaAdapter):
    """Phase oscillator pool."""

    name: str = "kuramoto"
    K: float = 1.0
    omega_spread: float = 0.3
    dt: float = 0.05
    _theta: np.ndarray = field(default=None, repr=False)  # type: ignore[assignment]
    _omega: np.ndarray = field(default=None, repr=False)  # type: ignore[assignment]

    def build_model(self) -> Any:
        rng = np.random.default_rng(self.seed)
        self._theta = rng.uniform(0, 2 * np.pi, self.n_neurons)
        self._omega = rng.normal(0.0, self.omega_spread, self.n_neurons)
        self._state.update({"K": self.K, "n": self.n_neurons, "omega_spread": self.omega_spread})
        return {"kind": "kuramoto_pool", "n": self.n_neurons}

    def step(self, input_data: Optional[Any] = None) -> dict:
        self.ensure_built()
        # complex order parameter
        z = np.mean(np.exp(1j * self._theta))
        r = float(np.abs(z))
        psi = float(np.angle(z))
        # mean-field update
        dtheta = self._omega + self.K * r * np.sin(psi - self._theta)
        if input_data is not None:
            try:
                drv = float(input_data)
                dtheta = dtheta + drv
            except (TypeError, ValueError):
                pass
        self._theta = (self._theta + self.dt * dtheta) % (2 * np.pi)
        self._state["r_last"] = r
        return {
            "theta": self._theta.tolist(),
            "r": r,
            "psi": psi,
            "motivation": r,  # synchrony itself is motivation
        }

    def selftest(self) -> dict:
        details: list = []

        # 1. drift — K=0 → r stays low (no global sync)
        a = KuramotoAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed, K=0.0)
        a.build_model()
        r_vals = [a.step()["r"] for _ in range(500)]
        # last 100-step mean should be low (random phases ~ 1/sqrt(n))
        tail_mean = float(np.mean(r_vals[-100:]))
        expected_ceiling = 4.0 / np.sqrt(self.n_neurons)
        self._check(
            details,
            "F-AKIDA-KU-1-DRIFT",
            tail_mean < expected_ceiling,
            f"tail_mean={tail_mean:.3f} ceiling={expected_ceiling:.3f}",
        )

        # 2. sync — K huge → r → 1
        b = KuramotoAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                            K=20.0, omega_spread=0.05)
        b.build_model()
        for _ in range(2000):
            b.step()
        r_final = b._state["r_last"]
        self._check(details, "F-AKIDA-KU-2-SYNC", r_final > 0.9, f"r_final={r_final:.3f}")

        # 3. r-bounded — every step has r ∈ [0,1]
        c = KuramotoAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed, K=5.0)
        c.build_model()
        all_bounded = True
        for _ in range(1000):
            rr = c.step()["r"]
            if not (0.0 <= rr <= 1.0 + 1e-9):
                all_bounded = False
                break
        self._check(details, "F-AKIDA-KU-3-R-BOUNDED", all_bounded, f"bounded={all_bounded}")

        # 4. K-monotone — mean r non-decreasing across 4 K rungs
        means = []
        for K in (0.0, 0.5, 2.0, 10.0):
            d = KuramotoAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                K=K, omega_spread=0.1)
            d.build_model()
            rs = [d.step()["r"] for _ in range(1000)]
            means.append(float(np.mean(rs[-200:])))
        mono = all(means[i] <= means[i + 1] + 0.05 for i in range(len(means) - 1))
        self._check(details, "F-AKIDA-KU-4-K-MONOTONE", mono, f"means={[round(m,3) for m in means]}")

        # 5. seed-stable — two runs at same seed produce identical r-trace
        e1 = KuramotoAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed, K=1.5)
        e1.build_model()
        e2 = KuramotoAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed, K=1.5)
        e2.build_model()
        rs1 = [e1.step()["r"] for _ in range(200)]
        rs2 = [e2.step()["r"] for _ in range(200)]
        max_diff = float(np.max(np.abs(np.asarray(rs1) - np.asarray(rs2))))
        self._check(details, "F-AKIDA-KU-5-SEED-STABLE", max_diff < 1e-12, f"max_diff={max_diff:.2e}")

        return self._summarize("F-AKIDA-KU", details)


__all__ = ["KuramotoAdapter"]
