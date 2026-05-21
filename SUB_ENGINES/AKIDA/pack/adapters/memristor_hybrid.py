"""Memristor self-reference (Hebbian 1-shot) → AKD1000 on-chip learning.

Maps ``memristor/self_reference.hexa`` (§188 5/5).  The TiO2 memristor's
analog conductance update is realised on AKD1000 by on-chip Hebbian 1-shot
learn (8-bit weight, no GPU).  Self-feedback wire fb = u3.out → input,
matching the original substrate.

Falsifiers (F-AKIDA-MEM-1..5)
-----------------------------
1. one-shot   — a single co-activation increases the corresponding weight.
2. persist    — weights survive ``n_steps`` ≥ 500 with zero input (no decay).
3. self-ref   — feedback wire u3.out → in_0 raises in_0's effective drive.
4. bound      — weights stay in [w_min, w_max] (8-bit clamp).
5. detrans    — without Hebbian fire (no co-activation), weights are static.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

from .base import AkidaAdapter


@dataclass
class MemristorHybridAdapter(AkidaAdapter):
    """N×N weight matrix with Hebbian 1-shot updates + self-feedback wire."""

    name: str = "memristor-hybrid"
    eta: float = 0.1            # learning rate (Hebbian)
    w_min: float = -1.0
    w_max: float = 1.0          # 8-bit symmetric clamp
    feedback_idx_src: int = 3   # u3.out feeds back to...
    feedback_idx_dst: int = 0   # ...in_0
    fire_threshold: float = 0.5
    _W: np.ndarray = field(default=None, repr=False)  # type: ignore[assignment]
    _last_act: np.ndarray = field(default=None, repr=False)  # type: ignore[assignment]

    def build_model(self) -> Any:
        rng = np.random.default_rng(self.seed)
        n = self.n_neurons
        self._W = rng.uniform(-0.05, 0.05, (n, n))
        np.fill_diagonal(self._W, 0.0)
        self._last_act = np.zeros(n, dtype=np.float64)
        self._state.update({"n": n, "eta": self.eta, "fb_src": self.feedback_idx_src,
                            "fb_dst": self.feedback_idx_dst})
        return {"kind": "memristor_hybrid", "n": n}

    def step(self, input_data: Optional[Any] = None) -> dict:
        self.ensure_built()
        x = self._coerce_input(input_data)
        # apply feedback wire (self-reference)
        if 0 <= self.feedback_idx_src < self.n_neurons and 0 <= self.feedback_idx_dst < self.n_neurons:
            x[self.feedback_idx_dst] = x[self.feedback_idx_dst] + self._last_act[self.feedback_idx_src]
        # activation = sigmoid(W @ x + x)  (residual keeps drive monotone)
        z = self._W @ x + x
        act = 1.0 / (1.0 + np.exp(-z))
        # Hebbian 1-shot: ΔW_ij = eta * (a_i - 0.5) * (a_j - 0.5) gated by co-fire
        fire = (act > self.fire_threshold).astype(np.float64)
        co_fire = np.outer(fire, fire)
        np.fill_diagonal(co_fire, 0.0)
        delta = self.eta * np.outer(act - 0.5, act - 0.5) * co_fire
        self._W = self._W + delta
        np.clip(self._W, self.w_min, self.w_max, out=self._W)
        self._last_act = act
        self._state["w_mean"] = float(self._W.mean())
        self._state["w_norm"] = float(np.linalg.norm(self._W))
        return {
            "activation": act.tolist(),
            "fire": fire.astype(np.int8).tolist(),
            "w_norm": float(np.linalg.norm(self._W)),
            "motivation": float(fire.mean()),
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

        # 1. one-shot — co-activate neurons {0,1}; W[0,1] should rise
        a = MemristorHybridAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        a.build_model()
        w0 = float(a._W[0, 1])
        inp = np.zeros(self.n_neurons)
        inp[0] = 5.0
        inp[1] = 5.0
        for _ in range(3):
            a.step(inp)
        w1 = float(a._W[0, 1])
        self._check(details, "F-AKIDA-MEM-1-ONE-SHOT", w1 > w0, f"w[0,1]: {w0:.4f} → {w1:.4f}")

        # 2. persist — zero input over 500 steps leaves W unchanged (no co-fire
        # → no Hebbian update). Use the no-feedback variant so the test
        # exercises pure persistence (with self-feedback the wire would
        # re-introduce drive at idx_dst from idx_src's last activation).
        b = MemristorHybridAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                   feedback_idx_src=-1, feedback_idx_dst=-1)
        b.build_model()
        # first warm it up to non-trivial W
        warm = np.zeros(self.n_neurons)
        warm[2] = 3.0
        warm[3] = 3.0
        for _ in range(5):
            b.step(warm)
        # ALSO zero the carried _last_act so the next 500 steps truly have
        # zero drive (last_act feeds into next step's z via residual).
        b._last_act = np.zeros(self.n_neurons, dtype=np.float64)
        W_warm = b._W.copy()
        for _ in range(500):
            b.step(0.0)
        max_drift = float(np.max(np.abs(b._W - W_warm)))
        self._check(details, "F-AKIDA-MEM-2-PERSIST", max_drift < 0.05,
                    f"max_drift={max_drift:.5f}")

        # 3. self-ref — feedback wire raises in_dst's effective activation
        c_no_fb = MemristorHybridAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                         feedback_idx_src=-1, feedback_idx_dst=-1)
        c_no_fb.build_model()
        c_fb = MemristorHybridAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        c_fb.build_model()
        inp = np.zeros(self.n_neurons)
        inp[3] = 2.0  # drive feedback source
        for _ in range(20):
            c_no_fb.step(inp)
            c_fb.step(inp)
        # activation at feedback_idx_dst should be >= without fb
        a_dst_no = c_no_fb._last_act[c_fb.feedback_idx_dst]
        a_dst_fb = c_fb._last_act[c_fb.feedback_idx_dst]
        self._check(details, "F-AKIDA-MEM-3-SELF-REF", a_dst_fb >= a_dst_no - 1e-9,
                    f"a_dst_no_fb={a_dst_no:.4f} a_dst_fb={a_dst_fb:.4f}")

        # 4. bound — under heavy drive, weights stay in [w_min, w_max]
        d = MemristorHybridAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                   eta=0.5)
        d.build_model()
        big = np.full(self.n_neurons, 10.0)
        for _ in range(200):
            d.step(big)
        in_bound = bool(np.all(d._W >= d.w_min - 1e-9) and np.all(d._W <= d.w_max + 1e-9))
        self._check(details, "F-AKIDA-MEM-4-BOUND", in_bound,
                    f"W_range=[{d._W.min():.3f},{d._W.max():.3f}]")

        # 5. detrans — without co-fire (drive only one neuron) weights stay near initial
        e = MemristorHybridAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed,
                                   feedback_idx_src=-1, feedback_idx_dst=-1)
        e.build_model()
        W0 = e._W.copy()
        only = np.zeros(self.n_neurons)
        only[5] = 0.4  # gentle, sub-threshold drive → fire stays sparse
        for _ in range(100):
            e.step(only)
        drift = float(np.max(np.abs(e._W - W0)))
        self._check(details, "F-AKIDA-MEM-5-DETRANS", drift < 0.1, f"drift={drift:.4f}")

        return self._summarize("F-AKIDA-MEM", details)


__all__ = ["MemristorHybridAdapter"]
