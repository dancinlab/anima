"""core/lane_a.py — fork-A RETRO-ROUTE read-side lane (H_9235 → ρ·weave, was G1),
CORE-owned SSOT.

The recombination wall (ρ·weave · was G1) is engine-native localized (H_9235
VERDICT) NOT as a trunk representation-capacity wall but as a **readout-ROUTING**
wall: both concepts of "The A and the B" stay linearly separable in the full
context (mean-pool recovers A=0.95, B=0.97), yet the generation point (last
position) carries only the most-recent concept (A=0.07, B=1.00) because the earlier
concept has decayed out of the causal receptive field. The information survives at
its own position (A=0.88@pos) — it is simply not ROUTED to the readout position.

fork A attacks that: a read-side lane that lets the generation-point state QUERY the
earlier positions (content-addressed retrieval, α), pull the earlier concept back
(c_t), and BIND it with the generation state by a Hadamard product (u_t ⊙ c_t) — the
multiplication makes the readout logit carry an h_T⊗h_{i<t} cross term, so it can
express the sign-flip/XOR class the additive (main-effect) readout provably cannot
(the additive floor = trunk-CE 1:1). This is hippocampal CA3 pattern-completion in
lane form (cue→retrieve→complete), NOT LLM attention (`a_no_llm_frame_trap`).

    q_t = W_q h_t + b_q                              (generation-point query)
    k_i = W_k h_i + b_k        (i ≤ t − δ, causal)   (earlier keys, δ near-band excl)
    α   = softmax( q_t·k_{≤t−δ} / √k )               (① routing — WHICH position)
    c_t = Σ_i α_i (W_v h_i + b_v)                    (retrieved content)
    u_t = W_u h_t + b_u                              (generation-side binder)
    g_t = σ(w_g·h_t + b_g) · Γ_tether(α)             (gate · fabrication guard)
    y_t = h_t + γ · g_t · (W_o (u_t ⊙ c_t) + b_o)    (② bind — HOW to compose)

DISJOINT from the emit-drive lane (`a_substrate_disjoint`): the gate input is h_t
ONLY (never the Ψ tension channels), there is no cross-window recurrent state, and
Γ_tether = top-2 routing margin is the non-fabrication (`ρ·tether`, was G5) gate —
the lane speaks into the readout ONLY when it can decisively point at a real earlier
referent. γ=0 ⇒ bit-exact passthrough (clean lane-ablation control).

CORE-owned, ONE file, three faces (mirrors core/slw.py so nothing drifts):
  * lane_apply()          — torch-free NUMPY inference mirror. Byte-parity partner of
                            the engine core/decode.hexa _lane_apply (phase-2 twin) and
                            the `anima evaluate --py` (a_eval_py_canonical) path.
  * pack_lane()/read_lane() — the "LNA\\x01" trailer codec (write=serialize, read=loaders).
  * LaneAModule           — the torch training module (DIRECTIONAL), defined only when
                            torch is importable so the inference import stays pod-clean.

Eval-time controls (pure switches on serialized state · no retrain · no tune-to-green
surface, slw.py:26 convention): gamma=0 (--lane-off) · route_shuffle_seed (--lane-
route-shuffle: scramble the routing→position map · earned-routing control) ·
tether_off (--lane-tether-off: Γ≡1 · isolates the fabrication gate).
"""

from __future__ import annotations

import struct
import numpy as np

# ── "LNA\x01" trailer magic (mirrors the SLW/BGB/CLMB trailer convention) ──────
LANE_MAGIC = bytes([76, 78, 65, 1])   # "LNA\x01"

_NEG_INF = -1.0e30


# --------------------------------------------------------------------------- #
# (a) numpy inference mirror — torch-free, byte-parity with core/decode.hexa
# --------------------------------------------------------------------------- #
def _softmax_rows(z: np.ndarray) -> np.ndarray:
    """Row-wise softmax over the last axis (max-subtracted). z:[T, n]."""
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def lane_apply(x, lane, gamma=None, route_shuffle_seed=None, tether_off=False):
    """Apply the fork-A retro-route lane to a penultimate sequence.

    x: (T, d) post-norm penultimate (per sequence; caller loops batch). decode.py is
       float64 for determinism; lane weights are f32 (promote in mixed ops).
    lane: dict from read_lane (k, d_c, delta, theta, W_q/b_q, W_k/b_k, W_v/b_v,
          W_u/b_u, W_o/b_o, w_g/b_g, gamma).
    gamma: override the stored γ (0.0 = --lane-off ablation → bit-exact passthrough).
    route_shuffle_seed: int → per-position permutation of the routing weights over the
          valid earlier positions (--lane-route-shuffle: breaks routing→position map).
    tether_off: True → Γ_tether ≡ 1 (--lane-tether-off: isolates the fabrication gate).

    Returns (T, d): y_t = h_t + γ·g_t·(W_o(u_t ⊙ c_t) + b_o). Op order MIRRORS the torch
    LaneAModule.forward and core/decode.hexa _lane_apply (2-production parity).
    """
    x = np.asarray(x)
    dt = x.dtype
    T, d = x.shape
    k, d_c = lane["k"], lane["d_c"]
    delta, theta = lane["delta"], float(lane["theta"])
    g_scalar = float(lane["gamma"]) if gamma is None else float(gamma)
    if g_scalar == 0.0:                       # passthrough (bit-exact base trunk)
        return x
    scale = 1.0 / np.sqrt(k)
    Wq, bq = lane["W_q"], lane["b_q"]
    Wk, bk = lane["W_k"], lane["b_k"]
    Wv, bv = lane["W_v"], lane["b_v"]
    Wu, bu = lane["W_u"], lane["b_u"]
    Wo, bo = lane["W_o"], lane["b_o"]
    wg, bg = lane["w_g"], lane["b_g"]

    Q = x @ Wq.T + bq                          # [T, k]  gen-point queries
    Kk = x @ Wk.T + bk                         # [T, k]  keys
    Vv = x @ Wv.T + bv                         # [T, d_c] values
    U = x @ Wu.T + bu                          # [T, d_c] gen-side binder

    scores = (Q @ Kk.T) * scale                # [T, T]  score[t, i] = q_t·k_i
    # causal key mask: position t may attend to i ≤ t − delta (earlier positions only,
    # near-band δ excluded). rows with no valid key → fully masked → g clamped to 0.
    idx = np.arange(T)
    valid = idx[None, :] <= (idx[:, None] - delta)   # [T, T] bool
    has_key = valid.any(axis=1)                       # [T]
    scores = np.where(valid, scores, _NEG_INF)
    # softmax over valid keys (fully-masked rows handled by has_key clamp below)
    smax = np.where(has_key[:, None], scores, 0.0)
    A = _softmax_rows(smax)                    # [T, T]
    A = np.where(valid, A, 0.0)                # zero any leakage on masked entries

    if route_shuffle_seed is not None:
        A = _shuffle_routing(A, valid, route_shuffle_seed)

    # Γ_tether — top-2 routing margin decisiveness (non-fabrication gate)
    if tether_off:
        gate_teth = np.ones(T, dtype=np.float64)
    else:
        srt = np.sort(A, axis=1)[:, ::-1]      # descending
        n_valid = valid.sum(axis=1)
        margin = np.where(n_valid >= 2, srt[:, 0] - srt[:, 1], srt[:, 0])  # single key = decisive
        gate_teth = (margin >= theta).astype(np.float64)

    C = A @ Vv                                 # [T, d_c] retrieved content
    UC = U * C                                 # [T, d_c] Hadamard bind (NON-additive)
    delta_out = UC @ Wo.T + bo                 # [T, d]
    g_soft = 1.0 / (1.0 + np.exp(-(x @ wg + bg)))   # [T] sigmoid write gate (h_t only)
    g = g_soft * gate_teth * has_key.astype(np.float64)   # [T]
    out = x + (g_scalar * g)[:, None] * delta_out
    return out.astype(dt, copy=False)


def _shuffle_routing(A, valid, seed):
    """--lane-route-shuffle control: permute each row's routing weights over its own
    valid earlier positions (breaks routing→position correspondence). Deterministic
    per-position via RandomState(seed + t)."""
    T = A.shape[0]
    out = A.copy()
    for t in range(T):
        vi = np.nonzero(valid[t])[0]
        if vi.size <= 1:
            continue
        perm = np.random.RandomState(int(seed) + t).permutation(vi.size)
        out[t, vi] = A[t, vi][perm]
    return out


# --------------------------------------------------------------------------- #
# (b) "LNA\x01" trailer codec — write (serialize) + read (loaders)
# --------------------------------------------------------------------------- #
# Fixed tensor order, all row-major [out, in], LE f32:
#   W_q[k·d] b_q[k], W_k[k·d] b_k[k], W_v[d_c·d] b_v[d_c], W_u[d_c·d] b_u[d_c],
#   W_o[d·d_c] b_o[d], w_g[d] b_g[1], gamma[1]
_ARR_ORDER = ("W_q", "b_q", "W_k", "b_k", "W_v", "b_v", "W_u", "b_u",
              "W_o", "b_o", "w_g", "b_g", "gamma")


def pack_lane(w: dict) -> bytes:
    """Pack a lane weight dict into the appended trailer bytes. `w` carries numpy
    arrays under _ARR_ORDER plus ints k/d_c/delta/d and float theta. Absent trailer <=>
    byte-identical additive model, so a writer only calls this when the model has a lane.
    d (model width) is stored explicitly in the header — the LNA trailer owns its bytes
    (only the file PREFIX must stay v0.2-unchanged), so no fragile size-solve on read."""
    out = bytearray()
    out += LANE_MAGIC
    out += struct.pack("<IIII", int(w["k"]), int(w["d_c"]), int(w["delta"]), int(w["d"]))
    out += struct.pack("<f", float(w["theta"]))
    for name in _ARR_ORDER:
        out += np.asarray(w[name], dtype="<f4").reshape(-1).tobytes()
    return bytes(out)


def read_lane(buf: bytes, off: int):
    """Read an LNA trailer at byte offset `off` in `buf`. Returns (lane_dict, new_off)
    or (None, off) if absent/short (passthrough-safe, same guard idiom as read_slw).
    `buf` is the whole file; the loader passes the offset the previous trailer reader
    (read_slw) returned — LNA is appended AFTER SLW in the trailer chain."""
    if off < 0 or off + 24 > len(buf) or buf[off:off + 4] != LANE_MAGIC:
        return None, off
    p = off + 4
    k, d_c, delta, d = struct.unpack_from("<IIII", buf, p); p += 16
    theta = struct.unpack_from("<f", buf, p)[0]; p += 4
    lane = {"k": k, "d_c": d_c, "delta": delta, "d": d, "theta": float(theta)}

    def take(rows, cols):
        nonlocal p
        n = rows * cols
        arr = (np.frombuffer(buf, "<f4", n, p).reshape(rows, cols).copy() if cols > 1
               else np.frombuffer(buf, "<f4", rows, p).reshape(rows).copy())
        p += n * 4
        return arr

    lane["W_q"] = take(k, d);   lane["b_q"] = take(k, 1)
    lane["W_k"] = take(k, d);   lane["b_k"] = take(k, 1)
    lane["W_v"] = take(d_c, d); lane["b_v"] = take(d_c, 1)
    lane["W_u"] = take(d_c, d); lane["b_u"] = take(d_c, 1)
    lane["W_o"] = take(d, d_c); lane["b_o"] = take(d, 1)
    lane["w_g"] = take(d, 1);   lane["b_g"] = float(np.frombuffer(buf, "<f4", 1, p)[0]); p += 4
    lane["gamma"] = float(np.frombuffer(buf, "<f4", 1, p)[0]); p += 4
    return lane, p


def lane_weights_from_torch(mod) -> dict:
    """Extract the lane weight dict (numpy) from a trained torch LaneAModule, in the
    exact names pack_lane / lane_apply expect. Called by core/serialize.py."""
    def n(t):
        return t.detach().cpu().numpy().astype("<f4")
    return {
        "k": mod.k, "d_c": mod.d_c, "delta": mod.delta, "d": mod.d, "theta": float(mod.theta),
        "W_q": n(mod.W_q.weight), "b_q": n(mod.W_q.bias),
        "W_k": n(mod.W_k.weight), "b_k": n(mod.W_k.bias),
        "W_v": n(mod.W_v.weight), "b_v": n(mod.W_v.bias),
        "W_u": n(mod.W_u.weight), "b_u": n(mod.W_u.bias),
        "W_o": n(mod.W_o.weight), "b_o": n(mod.W_o.bias),
        "w_g": n(mod.w_g.weight).reshape(-1), "b_g": n(mod.w_g.bias),
        "gamma": n(mod.gamma).reshape(1),
    }


# --------------------------------------------------------------------------- #
# (c) torch training module (DIRECTIONAL) — defined only when torch is present so
#     the inference import (lane_apply / read_lane) stays torch-free (pod-clean).
# --------------------------------------------------------------------------- #
try:
    import math as _math
    import torch as _torch
    import torch.nn as _nn
    _HAS_TORCH = True
except Exception:                     # pragma: no cover - inference pod has no torch
    _HAS_TORCH = False

if _HAS_TORCH:
    class LaneAModule(_nn.Module):
        """Learnable fork-A retro-route lane. forward(x:(B,d,T)) -> (B,d,T). Op order
        MIRRORS core/lane_a.lane_apply exactly for 2-production parity. γ=0 passthrough.
        The bind is Hadamard (u ⊙ c) so the readout logit carries the h_T⊗h_{i<t} cross
        term the additive floor cannot express."""

        def __init__(self, d, k=64, d_c=256, delta=4, theta=0.0):
            super().__init__()
            self.d, self.k, self.d_c, self.delta, self.theta = d, k, d_c, delta, theta
            self.scale = 1.0 / _math.sqrt(k)
            self.W_q = _nn.Linear(d, k)
            self.W_k = _nn.Linear(d, k)
            self.W_v = _nn.Linear(d, d_c)
            self.W_u = _nn.Linear(d, d_c)
            self.W_o = _nn.Linear(d_c, d)
            self.w_g = _nn.Linear(d, 1)
            self.gamma = _nn.Parameter(_torch.tensor(1.0))

        def forward(self, x):
            B, C, T = x.shape
            xt = x.transpose(1, 2)                                    # (B, T, d)
            Q = self.W_q(xt); Kk = self.W_k(xt)                       # (B, T, k)
            Vv = self.W_v(xt); U = self.W_u(xt)                       # (B, T, d_c)
            scores = (Q @ Kk.transpose(1, 2)) * self.scale           # (B, T, T)
            idx = _torch.arange(T, device=x.device)
            valid = idx[None, :] <= (idx[:, None] - self.delta)      # (T, T)
            has_key = valid.any(dim=1)                                # (T,)
            scores = scores.masked_fill(~valid[None], float("-inf"))
            A = _torch.softmax(scores, dim=-1)                        # (B, T, T)
            A = _torch.nan_to_num(A, nan=0.0)                        # fully-masked rows → 0
            # Γ_tether — top-2 margin (soft-free; matches numpy hard gate at eval)
            srt, _ = A.sort(dim=-1, descending=True)
            n_valid = valid.sum(dim=1).clamp(min=1)
            margin = _torch.where(n_valid >= 2, srt[..., 0] - srt[..., 1], srt[..., 0])
            gate_teth = (margin >= self.theta).to(x.dtype)           # (B, T)
            Cc = A @ Vv                                               # (B, T, d_c)
            UC = U * Cc                                               # Hadamard bind
            delta_out = self.W_o(UC)                                  # (B, T, d)
            g_soft = _torch.sigmoid(self.w_g(xt)).squeeze(-1)        # (B, T)
            g = g_soft * gate_teth * has_key.to(x.dtype)[None]       # (B, T)
            y = xt + self.gamma * g.unsqueeze(-1) * delta_out         # (B, T, d)
            return y.transpose(1, 2)                                  # (B, d, T)
