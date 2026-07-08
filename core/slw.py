"""core/slw.py — H_9200 E1 gated-write forward-slot (SLW), CORE-owned SSOT.

anima's next-byte = fn( (a)CE-trained · (b)feed-forward · (c)single-trunk ). The
additive combination operator `cbind` (order-BLIND sum of two concept reps) is the
proven ρ·weave recombination wall (was G1 · H_1129): two concepts farther apart than the conv receptive
field are mathematically independent -> cannot recombine. SLW replaces the additive
cbind with a content-addressed slot memory written/read causally on the post-norm
penultimate before readout -- an ASYMMETRIC write(address)/read(key) that attacks
premise (b). Because the slot state S lives OUTSIDE the token stream, a write at
position i is read at any j>i with zero dependence on j-i, so it reaches across the
D>RF independence wall. See state/9200_e1_303m/E1_SLW_module_spec.md.

CORE-owned (owner directive: core-related lives in core/). ONE file holds all three
faces of the SLW so nothing drifts:
  * slot_apply()  -- torch-free NUMPY inference mirror. This is the byte-parity
                     partner of the engine `core/decode.hexa` _slot_apply, and the
                     `anima-py evaluate` (a_eval_py_canonical) TERMINAL path calls
                     it. Import stays torch-free so the inference pod needs no torch.
  * pack_slw() / read_slw() -- the "SLW\\x01" trailer codec (used by
                     core/serialize.py on write, by the numpy + hexa loaders on read).
  * SLWModule     -- the torch training module (DIRECTIONAL). Defined only when torch
                     is importable, so `import slw` for inference never pulls torch.

γ=0 => exact passthrough (clean slot-ablation control). shuffle_perm permutes the
WRITE address only (reads unpermuted) => shuffle-bind control. Both are pure
eval-time switches on serialized state (no retraining -> no tune-to-green surface).
"""

from __future__ import annotations

import struct
import numpy as np

# ── "SLW\x01" trailer magic (mirrors the BGB/CLMB trailer convention) ──────────
SLW_MAGIC = bytes([83, 76, 87, 1])   # "SLW\x01"


# --------------------------------------------------------------------------- #
# (a) numpy inference mirror — torch-free, byte-parity with core/decode.hexa
# --------------------------------------------------------------------------- #
def _softmax(z: np.ndarray) -> np.ndarray:
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def slot_apply(x, slw, gamma=None, shuffle_perm=None):
    """Apply the SLW forward-slot to a penultimate sequence.

    x: (T, d) float32 post-norm penultimate (per sequence; caller loops batch).
    slw: dict from read_slw (K_slots, W_r/b_r, W_q/b_q, W_v/b_v, W_o/b_o, w_g/b_g,
         gamma, n_slot, k, d_s), all numpy float32.
    gamma: override the stored γ (pass 0.0 for the --slot-off ablation control).
    shuffle_perm: length-n_slot int permutation applied to the WRITE address only
                  (reads unpermuted) for the --slot-shuffle control; None = identity.

    Returns (T, d): x + γ·(W_o·m_t + b_o) per position. Op order is IDENTICAL to the
    torch SLWModule.forward and to core/decode.hexa _slot_apply (2-production parity).
    """
    x = np.asarray(x)
    dt = x.dtype                              # keep the caller's precision (decode.py
    T, d = x.shape                           # is float64 for determinism; f32 weights
    n_slot, k, d_s = slw["n_slot"], slw["k"], slw["d_s"]   # promote in mixed ops).
    g_scalar = float(slw["gamma"]) if gamma is None else float(gamma)
    if g_scalar == 0.0:                       # passthrough (bit-exact base trunk)
        return x
    scale = 1.0 / np.sqrt(k)
    Kt = slw["K_slots"].T                     # (k, n_slot)
    Wr, br = slw["W_r"], slw["b_r"]
    Wq, bq = slw["W_q"], slw["b_q"]
    Wv, bv = slw["W_v"], slw["b_v"]
    Wo, bo = slw["W_o"], slw["b_o"]
    wg, bg = slw["w_g"], slw["b_g"]
    S = np.zeros((n_slot, d_s), dtype=dt)
    out = np.empty((T, d), dtype=dt)
    for t in range(T):
        h = x[t]                                              # (d,)
        a = _softmax((Wr @ h + br) @ Kt * scale)             # (n_slot,) write addr
        v = Wv @ h + bv                                       # (d_s,) filler
        g = _sigmoid(float(wg @ h + bg))                      # scalar write gate
        ga = g * a                                            # (n_slot,)
        wa = ga[shuffle_perm] if shuffle_perm is not None else ga
        S = (1.0 - wa)[:, None] * S + wa[:, None] * v[None, :]   # erase-then-write
        b = _softmax((Wq @ h + bq) @ Kt * scale)             # (n_slot,) read addr
        m = (b[:, None] * S).sum(axis=0)                      # (d_s,) read-after-write
        out[t] = h + g_scalar * (Wo @ m + bo)
    return out


# --------------------------------------------------------------------------- #
# (b) "SLW\x01" trailer codec — write (serialize) + read (loaders)
# --------------------------------------------------------------------------- #
# Fixed tensor order (spec §2), all row-major [out, in], LE f32:
#   K_slots[n_slot·k], W_r[k·d] b_r[k], W_q[k·d] b_q[k],
#   W_v[d_s·d] b_v[d_s], W_o[d·d_s] b_o[d], w_g[d] b_g[1], gamma[1]
_ARR_ORDER = ("K_slots", "W_r", "b_r", "W_q", "b_q",
              "W_v", "b_v", "W_o", "b_o", "w_g", "b_g", "gamma")


def pack_slw(w: dict) -> bytes:
    """Pack an SLW weight dict into the appended trailer bytes. `w` carries numpy
    arrays under _ARR_ORDER plus ints n_slot/k/d_s. Absent trailer <=> byte-identical
    additive model, so a writer only calls this when the model actually has SLW."""
    out = bytearray()
    out += SLW_MAGIC
    out += struct.pack("<III", int(w["n_slot"]), int(w["k"]), int(w["d_s"]))
    for name in _ARR_ORDER:
        out += np.asarray(w[name], dtype="<f4").reshape(-1).tobytes()
    return bytes(out)


def read_slw(buf: bytes, off: int):
    """Read an SLW trailer at byte offset `off` in `buf`. Returns (slw_dict, new_off)
    or (None, off) if absent/short (passthrough-safe, same guard idiom as the BGB
    trailer reader). `buf` is the whole file bytes; the loader passes the offset the
    previous trailer reader returned."""
    if off < 0 or off + 16 > len(buf) or buf[off:off + 4] != SLW_MAGIC:
        return None, off
    p = off + 4
    n_slot, k, d_s = struct.unpack_from("<III", buf, p); p += 12
    # d (model width) == d_s by construction (d_s = d_model default); projections are
    # [·, d]. K_slots is (n_slot, k); all projections/biases follow in _ARR_ORDER.
    slw = {"n_slot": n_slot, "k": k, "d_s": d_s}
    kslots_n = n_slot * k
    slw["K_slots"] = np.frombuffer(buf, "<f4", kslots_n, p).reshape(n_slot, k).copy(); p += kslots_n * 4
    d = d_s
    def take(rows, cols):
        nonlocal p
        n = rows * cols
        arr = np.frombuffer(buf, "<f4", n, p).reshape(rows, cols).copy() if cols > 1 \
            else np.frombuffer(buf, "<f4", rows, p).reshape(rows).copy()
        p += (rows * cols) * 4
        return arr
    slw["W_r"] = take(k, d);  slw["b_r"] = take(k, 1)
    slw["W_q"] = take(k, d);  slw["b_q"] = take(k, 1)
    slw["W_v"] = take(d_s, d); slw["b_v"] = take(d_s, 1)
    slw["W_o"] = take(d, d_s); slw["b_o"] = take(d, 1)
    slw["w_g"] = take(d, 1);   slw["b_g"] = float(np.frombuffer(buf, "<f4", 1, p)[0]); p += 4
    slw["gamma"] = float(np.frombuffer(buf, "<f4", 1, p)[0]); p += 4
    return slw, p


def slw_weights_from_torch(mod) -> dict:
    """Extract the SLW weight dict (numpy) from a trained torch SLWModule, in the
    exact names pack_slw / slot_apply expect. Called by core/serialize.py."""
    def n(t):
        return t.detach().cpu().numpy().astype("<f4")
    return {
        "n_slot": mod.n_slot, "k": mod.k, "d_s": mod.d_s,
        "K_slots": n(mod.K_slots),
        "W_r": n(mod.W_r.weight), "b_r": n(mod.W_r.bias),
        "W_q": n(mod.W_q.weight), "b_q": n(mod.W_q.bias),
        "W_v": n(mod.W_v.weight), "b_v": n(mod.W_v.bias),
        "W_o": n(mod.W_o.weight), "b_o": n(mod.W_o.bias),
        "w_g": n(mod.w_g.weight).reshape(-1), "b_g": n(mod.w_g.bias),
        "gamma": n(mod.gamma).reshape(1),
    }


# --------------------------------------------------------------------------- #
# (c) torch training module (DIRECTIONAL) — defined only when torch is present so
#     the inference import (slot_apply / read_slw) stays torch-free (pod-clean).
# --------------------------------------------------------------------------- #
try:
    import math as _math
    import torch as _torch
    import torch.nn as _nn
    _HAS_TORCH = True
except Exception:                     # pragma: no cover - inference pod has no torch
    _HAS_TORCH = False

if _HAS_TORCH:
    class SLWModule(_nn.Module):
        """Learnable gated-write forward-slot. forward(x:(B,d,T)) -> (B,d,T). Op order
        MIRRORS core/slw.slot_apply exactly for 2-production parity. γ=0 passthrough."""

        def __init__(self, d, n_slot=8, k=64, d_s=None):
            super().__init__()
            d_s = d_s or d
            self.d, self.n_slot, self.k, self.d_s = d, n_slot, k, d_s
            self.scale = 1.0 / _math.sqrt(k)
            self.K_slots = _nn.Parameter(_torch.randn(n_slot, k) * (1.0 / _math.sqrt(k)))
            self.W_r = _nn.Linear(d, k)
            self.W_q = _nn.Linear(d, k)
            self.W_v = _nn.Linear(d, d_s)
            self.W_o = _nn.Linear(d_s, d)
            self.w_g = _nn.Linear(d, 1)
            self.gamma = _nn.Parameter(_torch.tensor(1.0))

        def forward(self, x):
            B, C, T = x.shape
            xt = x.transpose(1, 2)                                    # (B, T, d)
            S = x.new_zeros(B, self.n_slot, self.d_s)
            Kt = self.K_slots.t()
            outs = []
            for t in range(T):
                h = xt[:, t, :]                                      # (B, d)
                a = _torch.softmax((self.W_r(h) @ Kt) * self.scale, dim=-1)
                v = self.W_v(h)
                g = _torch.sigmoid(self.w_g(h))
                ga = (g * a).unsqueeze(-1)
                S = (1.0 - ga) * S + ga * v.unsqueeze(1)
                b = _torch.softmax((self.W_q(h) @ Kt) * self.scale, dim=-1)
                m = (b.unsqueeze(-1) * S).sum(dim=1)
                outs.append(self.W_o(m))
            o = _torch.stack(outs, dim=1).transpose(1, 2)            # (B, d, T)
            return x + self.gamma * o
