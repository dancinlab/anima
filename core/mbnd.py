"""core/mbnd.py — H_9698 (R6) MOUTH-BINDER trailer lane, CORE-owned SSOT.

WHY THIS EXISTS, in one line: H_9672 earned a runtime content-binding that actually rides in the
logits, but it earned it as a STORE — and G6 has no store. This lane keeps the operation and drops
the faculty.

H_1603 says the ρ·weave (G1) and ρ·fan (G6) walls share one missing part: a binding operator INSIDE
the mouth. The engine-native census is brutal about what that operator may not be — convergence
G1_WALL_LEVER_IS_OBJECTIVE_NOT_READOUT killed the whole fixed-role readout class BY CONSTRUCTION:
a TPR/HRR forward-slot with fixed roles collapses to Σ_r S_r·(yn⊙roles_r) = W_eff·yn, i.e. the same
linear ceiling as the standard readout, so it is dead before it is measured. The escape it explicitly
leaves open is the one this lane takes: DATA-DEPENDENT nonlinear gating.

The operation (Sol · lab full 3위):

    a_t  = softmax( (Q h_t)·(K m)ᵀ/√rank + b[t−i] )   content address + relative-distance bias
    ctx  = Σ_i a_ti (V m_i)                           what the mouth is currently attending to
    g_t  = (U h_t) ⊙ ctx                              ★ MULTIPLICATIVE — two distant contents meet
    s_t  = W_o [g_t ; h_t]                            → full-vocab logits
    out  = logits + λ·s_t                             perturbation (overwrite would delete the trunk)

Two things in that formula are there because the self-test proved the version without them was
uninterpretable, and both failures were invisible from the outside:

  b[t−i], the relative-distance bias, exists because plain content attention is PERMUTATION-
  EQUIVARIANT over the bank: permuting m permutes a and Vm together, so ctx is unchanged and an
  order-scramble control reads Δ=0.000 — not because the lane survived the control but because the
  control could not touch it. Worse, a lane with no order cannot tell "A causes B" from "B causes A",
  which is the asymmetry binding IS. The bias puts position into the address, so order becomes
  something the lane can use and the control can destroy.

  linear=True uses UNIFORM attention, not merely additive combination. The first attempt kept the
  data-dependent softmax and only swapped ⊙ for +; the self-test measured it as nonlinear (deviation
  59.9 where a linear map must read 0), because the address itself was still data-dependent. That arm
  would have "controlled" for nothing. Fixed uniform attention + additive combine is the actual
  fixed-role class the census buried, so it is the arm that must die.

The Hadamard is the whole claim. `(U h_t) ⊙ ctx` cannot be rewritten as W_eff·h_t for any fixed
W_eff, because ctx depends on h_t through a_t — that is precisely what takes it out of the class the
census buried. The bank m is CAUSAL (positions < t), so no future leaks and no side channel: the
lane sees exactly what the trunk saw.

`linear=True` is not a convenience — it is the INTERNAL NEGATIVE CONTROL. It replaces the Hadamard
with concatenation, which re-enters the fixed-role class, so it MUST reproduce the census's predicted
DOA. If the linear arm scores like the nonlinear one, the lane is not measuring binding at all and
the whole arm is void — that check is cheaper than any external control and it fails loudly.

DISJOINT (a_substrate_disjoint): its own trailer, its own file, additive at the logits, absent
trailer ⇒ byte-identical. It never reads the store lane and the store lane never reads it.
"""

from __future__ import annotations

import struct
import numpy as np

MBND_MAGIC = bytes([77, 66, 78, 68])   # "MBND" — SLW\x01 · CLML · CLMS · MBND (checked against
                                       # origin/main before claiming it: lane_type 3 was already
                                       # taken by H_9710 one axis over, so names get checked now)


def _softmax_rows(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def mbnd_apply(logits, yn, mb, lam_override=None, order_scramble=False, ctrl_seed=9698, last_only=False):
    """Apply the mouth-binder lane. logits (T,V) · yn (T,d) pre-slot trunk penultimate (the SAME tap
    CLML/CLMS read). Returns a new array; the caller's is not mutated.

    order_scramble : the control that answers "does the bank's ORDER carry the binding, or just its
                     bag of contents?" — it deranges the bank rows while keeping the same multiset,
                     so a lane that merely averages the past survives it and a lane that binds
                     position-specific content collapses. Absent this, a bag-of-hiddens lane would
                     read as a binder.

    Passthrough (byte-identical): mb None · λ==0 · T<2 (no causal bank exists at t=0)."""
    if mb is None:
        return logits
    # np.asarray(...).reshape(-1)[0], not float(mb["lam"]): lam rides the trailer as a shape-(1,)
    # array and numpy>=2 refuses to scalar-cast any ndim>0 array. The mac's older numpy accepted it,
    # so this only ever surfaced on the pool host that actually runs the training.
    lam = float(np.asarray(mb["lam"]).reshape(-1)[0]) if lam_override is None else float(lam_override)
    if lam == 0.0:
        return logits
    T = len(yn)
    if T < 2:
        return logits
    dt = logits.dtype
    linear = bool(int(mb.get("linear", 0)))
    rank = int(mb["rank"])
    scale = 1.0 / np.sqrt(float(rank))
    out = logits.copy()
    rng = np.random.default_rng(ctrl_seed) if order_scramble else None
    # H_9698 perf: generation reads only the last row (next-byte), and the binder at position t
    # depends only on the causal bank m=yn[:t] ≤ t — so computing ONLY t=T-1 yields a BYTE-IDENTICAL
    # last-row logit while dropping the per-token O(T^2) rebuild to O(T) (O(T^3)->O(T^2) over a gen).
    # Non-last rows are returned UNCHANGED (out=logits.copy()); the generation loop never reads them.
    _t_range = (T - 1,) if (last_only and T >= 1) else range(1, T)
    if last_only and order_scramble:
        # burn-replay the RNG for t=2..T-2 so the t=T-1 permutation draws from the SAME state as the
        # full loop (rng.permutation is called sequentially for every t>=2). Without this the SCRAMBLE
        # control's last row would NOT be byte-identical to the full-window run (lab-caught · T small).
        for _bt in range(2, T - 1):
            rng.permutation(_bt)
    for t in _t_range:
        h = yn[t]                                   # (d,)
        m = yn[:t]                                  # (t,d) causal bank — no future, no side channel
        if order_scramble and t >= 2:
            m = m[rng.permutation(t)]               # same multiset, order destroyed
        u = h @ mb["U"]                             # (rank,)
        if linear:
            # INTERNAL NEGATIVE CONTROL — UNIFORM attention (address is NOT data-dependent) plus an
            # additive combine = the fixed-role class the census buried BY CONSTRUCTION. This arm is
            # SUPPOSED to fail; if it scores like the binder, the lane measures something other than
            # binding and the nonlinear number means nothing. (Keeping the softmax here and only
            # swapping ⊙ for + does NOT control anything — measured nonlinear at 59.9.)
            a = np.full(t, 1.0 / t, dtype=np.float64)
            ctx = a @ (m @ mb["V"])
            g = u + ctx
        else:
            q = h @ mb["Q"]                         # (rank,)
            k = m @ mb["K"]                         # (t,rank)
            dist = np.minimum(np.arange(t - 1, -1, -1), _N_POS - 1)   # t−i−1, clipped
            a = _softmax_rows((k @ q) * scale + mb["b_pos"][dist])    # (t,) content + position
            ctx = a @ (m @ mb["V"])                 # (rank,) attended content
            g = u * ctx                             # ★ Hadamard: two distant contents multiply
        s = np.concatenate([g, h]) @ mb["W_o"]      # (V,)
        out[t] = (logits[t] + lam * s).astype(dt)
    return out


# ── "MBND" trailer codec — LE f32, same idiom as CLMS/CLML ───────────────────
_MB_ORDER = ("Q", "K", "V", "U", "b_pos", "W_o", "lam")
_N_POS = 32          # relative-distance buckets; the last one absorbs every longer distance


def pack_mbnd(w: dict) -> bytes:
    out = bytearray()
    out += MBND_MAGIC
    out += struct.pack("<BII", 1 if int(w.get("linear", 0)) else 0, int(w["rank"]), int(w["d"]))
    for name in _MB_ORDER:
        out += np.asarray(w[name], dtype="<f4").reshape(-1).tobytes()
    return bytes(out)


def read_mbnd(buf: bytes, off: int, d: int, V: int):
    """Read an MBND trailer at `off`. Returns (mb, new_off) or (None, off) — passthrough-safe on
    absent/short, the same guard idiom as read_clms/read_clml."""
    if off < 0 or off + 4 > len(buf) or buf[off:off + 4] != MBND_MAGIC:
        return None, off
    p = off + 4
    if p + 9 > len(buf):
        return None, off
    linear, rank, d_file = struct.unpack_from("<BII", buf, p); p += 9
    if int(d_file) != int(d):
        return None, off                            # a d-mismatch is a wrong-model trailer, not ours

    def take(n, shape):
        nonlocal p
        arr = np.frombuffer(buf, "<f4", n, p).reshape(shape).copy(); p += n * 4
        return arr

    mb = {"linear": int(linear), "rank": int(rank), "d": int(d)}
    mb["Q"] = take(d * rank, (d, rank))
    mb["K"] = take(d * rank, (d, rank))
    mb["V"] = take(d * rank, (d, rank))
    mb["U"] = take(d * rank, (d, rank))
    mb["b_pos"] = take(_N_POS, (_N_POS,))
    mb["W_o"] = take((rank + d) * V, (rank + d, V))
    mb["lam"] = float(take(1, (1,))[0])
    return mb, p


# --------------------------------------------------------------------------- #
# torch training module (DIRECTIONAL) — defined only when torch imports, so inference stays
# torch-free (mirrors core/clms.py's guard).
# --------------------------------------------------------------------------- #
try:
    import torch as _torch
    import torch.nn as _nn
    _HAS_TORCH = True
except Exception:
    _HAS_TORCH = False

if _HAS_TORCH:

    class MouthBinder(_nn.Module):
        """Trains {Q,K,V,U,W_o,λ}. forward(yn:(B,T,d)) -> (B,T,V) additive logit delta. Op order
        MIRRORS mbnd_apply for 2-production parity; a divergence there makes every verdict from this
        lane unattributable, so the mirror is checked in the pool smoke, not assumed."""

        def __init__(self, d, V, rank=64, lam0=1.0, linear=False):
            super().__init__()
            self.d, self.V, self.rank, self.linear = d, V, rank, bool(linear)
            self.scale = 1.0 / (rank ** 0.5)
            self.Q = _nn.Linear(d, rank, bias=False)
            self.K = _nn.Linear(d, rank, bias=False)
            self.V_ = _nn.Linear(d, rank, bias=False)
            self.U = _nn.Linear(d, rank, bias=False)
            self.b_pos = _nn.Parameter(_torch.zeros(_N_POS))   # relative-distance bias (order enters here)
            self.W_o = _nn.Linear(rank + d, V, bias=False)
            self.lam = _nn.Parameter(_torch.tensor(float(lam0)))

        def forward(self, yn):
            B, T, d = yn.shape
            q = self.Q(yn)                                   # (B,T,rank)
            k = self.K(yn)
            v = self.V_(yn)
            causal = _torch.tril(_torch.ones(T, T, device=yn.device, dtype=_torch.bool), diagonal=-1)
            u = self.U(yn)
            if self.linear:
                # uniform attention over the causal bank = the fixed-role/linear control class
                att = causal.to(v.dtype)
                att = att / att.sum(-1, keepdim=True).clamp(min=1.0)
                ctx = _torch.bmm(att.unsqueeze(0).expand(B, T, T), v)
                g = u + ctx
            else:
                ti = _torch.arange(T, device=yn.device)
                dist = (ti.unsqueeze(1) - ti.unsqueeze(0) - 1).clamp(0, _N_POS - 1)   # t−i−1
                att = _torch.bmm(q, k.transpose(1, 2)) * self.scale + self.b_pos[dist]
                att = att.masked_fill(~causal, float("-inf"))
                att = _torch.softmax(att, dim=-1)
                att = _torch.nan_to_num(att, nan=0.0)        # row t=0 has an empty bank ⇒ all -inf
                ctx = _torch.bmm(att, v)                     # (B,T,rank)
                g = u * ctx                                  # ★ Hadamard
            s = self.W_o(_torch.cat([g, yn], dim=-1))        # (B,T,V)
            s = s * _torch.cat([_torch.zeros(B, 1, self.V, device=yn.device, dtype=s.dtype),
                                _torch.ones(B, T - 1, self.V, device=yn.device, dtype=s.dtype)],
                               dim=1) if T > 1 else s * 0.0  # t=0 has no bank — mirror's T<2 rule
            return self.lam * s


    def mbnd_weights_from_torch(mod) -> dict:
        def n(t):
            return t.detach().cpu().numpy().astype("<f4")
        return {
            "linear": 1 if mod.linear else 0, "rank": mod.rank, "d": mod.d,
            "Q": n(mod.Q.weight).T, "K": n(mod.K.weight).T,
            "V": n(mod.V_.weight).T, "U": n(mod.U.weight).T,
            "b_pos": n(mod.b_pos), "W_o": n(mod.W_o.weight).T, "lam": n(mod.lam).reshape(1),
        }
