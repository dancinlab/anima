"""core/clml.py — fork-A read-side context-pooling LANE (CLML), CORE-owned SSOT.

The ρ·weave recombination wall (was G1) is READOUT-ROUTING, not trunk representation-capacity
(H_9235 H2-lite): both concepts of a two-concept context ARE linearly present (mean-pool recovery
0.95/0.97), but the last-position (generation) readout only carries the most-recent concept
(last-position recovery A=0.07, B=1.00 — pure receptive-field decay, language-independent). The
CLML lane fixes the ROUTE without touching the trunk: it reads the trunk's per-position penultimate
`yn`, causally pools the full context (where the earlier concept survives), and adds a gated,
tether-clipped logit bias at composed positions. $0 pre-check PROVEN: mean-pool→gelu bottleneck
routes both concepts to held-out XOR (0.98) where last-position (0.47) and a linear head (0.43)
FAIL (state/g1_gamma_binding_lane/fork_a_precheck.py).

DISJOINT (a_substrate_disjoint): read-only tap of `yn` + an additive logit bias whose gate is
LEARNED to open only at composed positions — trunk weights, emit-drive lane, Ψ-tension untouched.
Absent trailer <=> byte-identical to today's .clm (loaders passthrough on short/absent read).

CORE-owned, ONE file (mirrors core/slw.py): lane_apply (torch-free numpy inference mirror,
byte-parity partner of core/decode.hexa) · pack_clml/read_clml ("CLML" trailer codec) · CLMLModule
(torch training module, DIRECTIONAL, defined only when torch importable so inference stays torch-free).
"""

from __future__ import annotations

import struct
import numpy as np

# ── "CLML" trailer magic (mirrors the CLMB/SLW trailer convention) ──────────────
CLML_MAGIC = bytes([67, 76, 77, 76])   # "CLML"


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def _gelu(x):
    return 0.5 * x * (1.0 + np.tanh(0.7978845608028654 * (x + 0.044715 * x**3)))


# --------------------------------------------------------------------------- #
# (a) numpy inference mirror — torch-free, byte-parity target for core/decode.hexa
# --------------------------------------------------------------------------- #
def lane_apply(yn, logits, clml):
    """Add the CLML read-side pooling bias to the readout logits.

    yn:     (T, d) float — pre-readout trunk penultimate (the _fwd_trunk output; the SAME
            representation the $0 pre-check pooled — pre-SLW-slot).
    logits: (T, V) float — the trunk readout logits to condition.
    clml:   dict from read_clml (W1 (d,r), b1 (r,), W2 (r,V), w_g (2d,), b_g scalar, tau, r).
    Returns (T, V): logits + clip( g_t · gelu(c_t·W1+b1)·W2 , ±tau ), where c_t is the CAUSAL
    cumulative mean of yn (0-param pool) and g_t = sigmoid(w_g·[yn_t;c_t]+b_g) is the learned
    composed-position gate. lane_type=0 or clml=None => exact passthrough (logits unchanged).
    Op order IDENTICAL to CLMLModule.forward (2-production parity)."""
    if clml is None or int(clml.get("lane_type", 0)) == 0:
        return logits
    yn = np.asarray(yn); dt = logits.dtype
    T, d = yn.shape
    csum = np.cumsum(yn, axis=0)
    counts = np.arange(1, T + 1, dtype=yn.dtype).reshape(T, 1)
    c = csum / counts                                        # (T,d) causal mean pool
    gate = _sigmoid(np.concatenate([yn, c], axis=1) @ clml["w_g"] + clml["b_g"])   # (T,)
    z = _gelu(c @ clml["W1"] + clml["b1"])                   # (T,r) gelu bottleneck
    delta = (z @ clml["W2"]) * gate[:, None]                 # (T,V) gated logit bias
    delta = np.clip(delta, -float(clml["tau"]), float(clml["tau"]))
    return (logits + delta).astype(dt)


# --------------------------------------------------------------------------- #
# (b) "CLML" trailer codec — write (serialize) + read (loaders) · LE f32
#   header: CLML magic · lane_type u8 · r u32 · tau f32
#   arrays (row-major): W1[d·r] b1[r] W2[r·V] w_g[2d] b_g[1]   (d,V from the model)
# --------------------------------------------------------------------------- #
_ARR_ORDER = ("W1", "b1", "W2", "w_g", "b_g")


def pack_clml(w: dict) -> bytes:
    """Pack a CLML weight dict into appended trailer bytes. `w` = W1 (d,r), b1 (r,),
    W2 (r,V), w_g (2d,), b_g scalar, lane_type, r, tau. Absent trailer <=> byte-identical
    additive/SLW model, so a writer only calls this when the model actually has a lane."""
    out = bytearray()
    out += CLML_MAGIC
    out += struct.pack("<BIf", int(w.get("lane_type", 1)), int(w["r"]), float(w["tau"]))
    for name in _ARR_ORDER:
        out += np.asarray(w[name], dtype="<f4").reshape(-1).tobytes()
    return bytes(out)


def read_clml(buf: bytes, off: int, d: int, V: int):
    """Read a CLML trailer at byte offset `off`. `d`,`V` come from the model (loader passes
    W["d"], W["V"]). Returns (clml_dict, new_off) or (None, off) if absent/short (passthrough-
    safe, same guard idiom as read_slw)."""
    if off < 0 or off + 9 > len(buf) or buf[off:off + 4] != CLML_MAGIC:
        return None, off
    p = off + 4
    lane_type = buf[p]; p += 1
    (r,) = struct.unpack_from("<I", buf, p); p += 4
    (tau,) = struct.unpack_from("<f", buf, p); p += 4
    def take(n, shape):
        nonlocal p
        arr = np.frombuffer(buf, "<f4", n, p).reshape(shape).copy(); p += n * 4
        return arr
    clml = {"lane_type": int(lane_type), "r": int(r), "tau": float(tau)}
    clml["W1"] = take(d * r, (d, r))
    clml["b1"] = take(r, (r,))
    clml["W2"] = take(r * V, (r, V))
    clml["w_g"] = take(2 * d, (2 * d,))
    clml["b_g"] = float(np.frombuffer(buf, "<f4", 1, p)[0]); p += 4
    return clml, p


def clml_weights_from_torch(mod) -> dict:
    """Extract the CLML weight dict (numpy) from a trained torch CLMLModule."""
    def n(t):
        return t.detach().cpu().numpy().astype("<f4")
    return {
        "lane_type": 1, "r": int(mod.r), "tau": float(mod.tau),
        "W1": n(mod.W1.weight).T, "b1": n(mod.W1.bias),          # nn.Linear weight is (out,in)=(r,d) → (d,r)
        "W2": n(mod.W2.weight).T,                                 # (V,r) → (r,V)
        "w_g": n(mod.w_g.weight).reshape(-1), "b_g": n(mod.w_g.bias),
    }


# --------------------------------------------------------------------------- #
# (c) torch training module (DIRECTIONAL) — defined only when torch is present so
#     the inference import (lane_apply / read_clml) stays torch-free (pod-clean).
# --------------------------------------------------------------------------- #
try:
    import torch as _torch
    import torch.nn as _nn
    _HAS_TORCH = True
except Exception:                     # pragma: no cover - inference pod has no torch
    _HAS_TORCH = False

if _HAS_TORCH:
    class CLMLModule(_nn.Module):
        """Learnable read-side context-pooling lane. forward(yn:(B,T,d), logits:(B,T,V)) ->
        (B,T,V). Op order MIRRORS core/clml.lane_apply exactly for 2-production parity.
        Trains ONLY {W1,b1,W2,w_g,b_g} — the trunk is frozen (fork A = read-side, DISJOINT)."""

        def __init__(self, d, V, r=128, tau=8.0):
            super().__init__()
            self.d, self.V, self.r, self.tau = d, V, r, tau
            self.W1 = _nn.Linear(d, r)
            self.W2 = _nn.Linear(r, V, bias=False)
            self.w_g = _nn.Linear(2 * d, 1)

        def forward(self, yn, logits):
            B, T, d = yn.shape
            csum = _torch.cumsum(yn, dim=1)
            counts = _torch.arange(1, T + 1, device=yn.device, dtype=yn.dtype).view(1, T, 1)
            c = csum / counts
            gate = _torch.sigmoid(self.w_g(_torch.cat([yn, c], dim=-1)))     # (B,T,1)
            z = _torch.nn.functional.gelu(self.W1(c))
            delta = self.W2(z) * gate
            delta = _torch.clamp(delta, -self.tau, self.tau)
            return logits + delta
