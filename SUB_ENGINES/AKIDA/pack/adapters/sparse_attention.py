"""Sparse attention pattern → MetaTF (Akida 강점 = sparse activation).

N1 path: anima's sparse-attention substrate (top-k masked QK^T) is a direct
fit for AKD1000's event-driven sparsity — only k active heads spike per
step, the rest stay silent (zero-power on the chip).

Falsifiers (F-AKIDA-SA-1..5)
----------------------------
1. topk-shape   — output mask has exactly ``k`` active positions per row.
2. zero-rest    — non-selected positions are exactly zero.
3. perm-equivar — permuting input columns permutes the output mask identically.
4. monotone-k   — increasing k weakly increases attention coverage.
5. sparsity     — at k ≪ n, output density ≤ k/n.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

from .base import AkidaAdapter


@dataclass
class SparseAttentionAdapter(AkidaAdapter):
    """Top-k sparse attention head pool (n_neurons = sequence length)."""

    name: str = "sparse-attention"
    k: int = 2
    d_model: int = 16
    _W_q: np.ndarray = field(default=None, repr=False)  # type: ignore[assignment]
    _W_k: np.ndarray = field(default=None, repr=False)  # type: ignore[assignment]
    _W_v: np.ndarray = field(default=None, repr=False)  # type: ignore[assignment]

    def build_model(self) -> Any:
        rng = np.random.default_rng(self.seed)
        d = self.d_model
        scale = 1.0 / np.sqrt(d)
        self._W_q = rng.normal(0, scale, (d, d))
        self._W_k = rng.normal(0, scale, (d, d))
        self._W_v = rng.normal(0, scale, (d, d))
        self._state.update({"k": self.k, "d_model": d, "n_seq": self.n_neurons})
        return {"kind": "sparse_attention", "n_seq": self.n_neurons}

    def step(self, input_data: Optional[Any] = None) -> dict:
        self.ensure_built()
        X = self._coerce_input(input_data)  # (n_seq, d_model)
        Q = X @ self._W_q
        K = X @ self._W_k
        V = X @ self._W_v
        scores = (Q @ K.T) / np.sqrt(self.d_model)  # (n_seq, n_seq)
        n_seq = scores.shape[0]
        k = max(1, min(self.k, n_seq))
        # top-k per row
        mask = np.zeros_like(scores)
        idx = np.argpartition(scores, -k, axis=1)[:, -k:]
        rows = np.arange(n_seq)[:, None]
        mask[rows, idx] = 1.0
        sel = scores * mask + (1.0 - mask) * (-1e9)
        # stable softmax over selected
        sel = sel - sel.max(axis=1, keepdims=True)
        ex = np.exp(sel) * mask
        denom = ex.sum(axis=1, keepdims=True)
        denom[denom == 0] = 1.0
        attn = ex / denom
        out = attn @ V
        self._state["density"] = float(mask.mean())
        return {
            "attn": attn,
            "mask": mask,
            "out": out,
            "density": float(mask.mean()),
            "motivation": float(np.mean(np.abs(out))),
        }

    def _coerce_input(self, x: Any) -> np.ndarray:
        if x is None:
            rng = np.random.default_rng(self.seed + 1)
            return rng.normal(0, 1, (self.n_neurons, self.d_model))
        arr = np.asarray(x, dtype=np.float64)
        if arr.ndim == 1:
            # broadcast to 2D
            arr = np.broadcast_to(arr.reshape(1, -1),
                                  (self.n_neurons, self.d_model)).copy()
        if arr.shape != (self.n_neurons, self.d_model):
            # pad / truncate
            out = np.zeros((self.n_neurons, self.d_model))
            r = min(arr.shape[0], self.n_neurons)
            c = min(arr.shape[1] if arr.ndim > 1 else 1, self.d_model)
            out[:r, :c] = arr[:r, :c]
            return out
        return arr

    def selftest(self) -> dict:
        details: list = []

        # 1. topk-shape — each row's mask sums to exactly k
        a = SparseAttentionAdapter(name=self.name, n_neurons=self.n_neurons,
                                   seed=self.seed, k=2)
        a.build_model()
        m = a.step()["mask"]
        row_sums = m.sum(axis=1)
        self._check(details, "F-AKIDA-SA-1-TOPK-SHAPE",
                    bool(np.all(row_sums == 2)),
                    f"row_sums_unique={np.unique(row_sums).tolist()}")

        # 2. zero-rest — non-selected attn positions are exactly zero
        attn = a.step()["attn"]
        m2 = a.step()["mask"]
        # recompute attn for same step
        out = a.step()
        attn3 = out["attn"]
        m3 = out["mask"]
        zero_rest = bool(np.all(attn3[m3 == 0] == 0.0))
        self._check(details, "F-AKIDA-SA-2-ZERO-REST", zero_rest, f"zero_rest={zero_rest}")

        # 3. perm-equivariance: swap rows of X → mask rows swap accordingly
        b = SparseAttentionAdapter(name=self.name, n_neurons=self.n_neurons,
                                   seed=self.seed, k=2)
        b.build_model()
        rng = np.random.default_rng(self.seed + 99)
        X = rng.normal(0, 1, (self.n_neurons, self.d_model))
        perm = rng.permutation(self.n_neurons)
        X_perm = X[perm]
        m_orig = b.step(X)["mask"]
        m_perm = b.step(X_perm)["mask"]
        # Permutation equivariance: if X' = X[perm], then scores' = scores[perm][:, perm]
        # so mask'[i,j] == mask[perm[i], perm[j]]
        m_expected = m_orig[np.ix_(perm, perm)]
        equiv = bool(np.array_equal(m_perm, m_expected))
        self._check(details, "F-AKIDA-SA-3-PERM-EQUIVAR", equiv, f"perm_match={equiv}")

        # 4. monotone-k — larger k → density rises
        densities = []
        for k in (1, 2, 4):
            c = SparseAttentionAdapter(name=self.name, n_neurons=self.n_neurons,
                                       seed=self.seed, k=k)
            c.build_model()
            densities.append(c.step()["density"])
        mono = all(densities[i] <= densities[i + 1] for i in range(len(densities) - 1))
        self._check(details, "F-AKIDA-SA-4-MONOTONE-K", mono, f"densities={densities}")

        # 5. sparsity — at k=1, density == 1/n_seq
        d = SparseAttentionAdapter(name=self.name, n_neurons=self.n_neurons,
                                   seed=self.seed, k=1)
        d.build_model()
        dens = d.step()["density"]
        expected = 1.0 / self.n_neurons
        self._check(details, "F-AKIDA-SA-5-SPARSITY",
                    abs(dens - expected) < 1e-9,
                    f"density={dens:.4f} expected={expected:.4f}")

        return self._summarize("F-AKIDA-SA", details)


__all__ = ["SparseAttentionAdapter"]
