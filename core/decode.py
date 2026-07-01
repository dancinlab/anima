# ==========================================================================
# ⛔ ENGINE-INTERNAL / DEPRECATED py-MIRROR — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 cli/ 단일진입만: anima eval | train | serialize
#   (canonical = hexa core/*.hexa 단일 SSOT; py 미러는 2026-06-28 폐기, DIRECTIONAL).
# 이 파일을 `python3 core/decode.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ decode.py 직접 실행 금지 — cli/ 단일진입(anima eval/train/serialize, canonical=hexa) 경유. #2603")

"""core/decode.py — UNIFIED PY DECODE ENGINE: byte-faithful 1:1 merge of the two
per-mouth decoder mirrors into ONE module.

  * CONV (CLM ConvMoE) mouth  = the verbatim port of core/clm_decode.hexa
                                (formerly core/clm_decode.py)
  * BYTE (ByteGPT transformer) = the verbatim port of core/bytegpt_decode.hexa
                                (formerly core/bytegpt_decode.py)

Per CLAUDE.md a_engine_native_learning: hexa + py are TWO co-equal production
engines kept at byte-parity. This module is the numpy mirror of the two decode
mouths; it exposes the UNION of both modules' public names so a caller can do
`import decode as clm` OR `import decode as bg` (or `import decode`) with ZERO
call-site churn (drop-in for clm_decode.py + bytegpt_decode.py).

Organization:
  (a) SHARED — imports + the transcendental/PRNG helpers that are BYTE-IDENTICAL
      across both source modules (dt_exp, _MASK, _mix32, _rng_next, _topk_sample).
  (b) CONV (CLM) — the full clm_decode.py public API, verbatim.
  (c) BYTE (ByteGPT) — the full bytegpt_decode.py public API, verbatim, PLUS a
      byte-exact KV-cache fast path that REPLACES the O(gen²) full re-forward
      decode loop (the O(gen²) reference is kept under a `_full` suffix).
  (d) MOUTH DISPATCH — header-sniff (CLM\\x01 magic → conv; 5×u32 → byte),
      mirroring generator.hexa gen_auto_backend.

DIVERGENT SAME-NAMED HELPERS — kept under DISTINCT names, never silently merged:
  * clm's `_gn_sqrt` (gn_lib, 40-iter from g0=x) ⊥ bg's `dt_sqrt` (flame_math,
    24-iter from g0=max(x,1)) — different bodies, both retained (distinct names).
  * clm's `_rd_u32` and bg's `_bg_rd_u32` — IDENTICAL bodies; `_bg_rd_u32` is an
    alias of `_rd_u32` (surface preserved, one definition).
The PRNG trio (_mix32/_rng_next/_topk_sample) + dt_exp were byte-identical across
the two source files (bg imported dt_exp FROM clm), so they are deduped to one
copy in the SHARED section with no behavior change.

KV-CACHE (the ByteGPT fast path, new here): the hexa KV-cache is byte-identical
to its full-forward reference (bytegpt_decode.hexa:919). numpy BLAS GEMM is
M-dependent at the ~1e-15 ULP level (a single-row projection differs from the
same row of an M=T batch), so the py KV logits are NOT bit-identical to the py
full-forward — but the DECODE TOKEN STREAM is identical (argmax/inverse-CDF are
robust to ~1e-13 logit drift), and the cache is fully RE-SYNCED (rebuilt at M=T)
whenever the window slides past `block`. Byte-exactness of the token stream is
gated by state/1815_cls_bytegpt/_decode_selftest.py.
"""

import sys
import math
import os
import struct
import numpy as np


# ════════════════════════════════════════════════════════════════════════
# (a) SHARED — helpers byte-identical across clm_decode.py + bytegpt_decode.py
# ════════════════════════════════════════════════════════════════════════

def dt_exp(x):
    """flame_math.hexa::dt_exp — halve until |xr|<=0.25, 12-term Taylor (k=1..11),
    then square r times. Vectorized; halving by 2 is exact in fp64, so the
    per-element halve-count r matches the hexa scalar while-loop exactly.
    (SHARED: bg's top-k sampler softmax uses the SAME dt_exp — was `from
    clm_decode import dt_exp` in bytegpt_decode.py.)"""
    x = np.asarray(x, dtype=np.float64)
    scalar = (x.ndim == 0)
    x = np.atleast_1d(x)
    xr = x.copy()
    r = np.zeros(x.shape, dtype=np.int64)
    mask = np.abs(xr) > 0.25
    while mask.any():
        xr = np.where(mask, xr / 2.0, xr)
        r = np.where(mask, r + 1, r)
        mask = np.abs(xr) > 0.25
    term = np.ones_like(xr)
    acc = np.ones_like(xr)
    k = 1
    while k < 12:
        term = term * xr / float(k)
        acc = acc + term
        k = k + 1
    rmax = int(r.max()) if r.size else 0
    s = 0
    while s < rmax:
        m = r > s
        acc = np.where(m, acc * acc, acc)
        s = s + 1
    return float(acc[0]) if scalar else acc


# ── seeded top-k temperature sampler PRNG — BYTE-IDENTICAL across both mouths
# (clm_decode.hexa _clmd_mix32/_rng_next ≡ bytegpt_decode.hexa _g6_mix32/_rng_next;
# xorshift32 & 0xFFFFFFFF). Deduped to one copy.
_MASK = 0xFFFFFFFF


def _mix32(s):
    """_clmd_mix32 / _g6_mix32 — SplitMix32-style finalizer."""
    z = (s + 0x9E3779B9) & _MASK
    z = ((z ^ (z // 65536)) * 0x85EBCA6B) & _MASK
    z = ((z ^ (z // 8192)) * 0xC2B2AE35) & _MASK
    z = (z ^ (z // 65536)) & _MASK
    if z == 0:
        z = 0x9E3779B9
    return z


def _rng_next(s):
    """_clmd_rng_next / _g6_rng_next — xorshift32 step -> (state, u in [0,1))."""
    x = s & _MASK
    if x == 0:
        x = 0x9E3779B9
    x = (x ^ (x * 8192)) & _MASK
    x = (x ^ (x // 131072)) & _MASK
    x = (x ^ (x * 32)) & _MASK
    return x, (float(x) / 4294967296.0)


def _topk_sample(logits, vocab, top_k, temp, rng):
    """_clmd_topk_sample / _g6_topk_sample — top-k by repeated argmax (ties:
    first/strict >), /temp, dt_exp softmax (max-sub), inverse-CDF draw. logits:[V].
    (SHARED: both mouths' samplers had byte-identical bodies.)"""
    kcap = top_k if (top_k > 0 and top_k < vocab) else vocab
    taken = np.zeros(vocab, dtype=np.float64)
    sel_idx = []
    sel_val = []
    picks = 0
    while picks < kcap:
        bi = -1
        bv = 0.0
        for k in range(vocab):
            if taken[k] < 0.5:
                v = logits[k]
                if bi < 0 or v > bv:
                    bi = k; bv = v
        if bi < 0:
            picks = kcap
        else:
            taken[bi] = 1.0
            sel_idx.append(bi)
            sel_val.append(bv / temp)
            picks += 1
    nsel = len(sel_idx)
    mx = sel_val[0]
    for i in range(1, nsel):
        if sel_val[i] > mx:
            mx = sel_val[i]
    probs = []
    summ = 0.0
    for j in range(nsel):
        e = float(dt_exp(np.array(sel_val[j] - mx)))
        probs.append(e); summ += e
    s2, u = _rng_next(rng)
    target = u * summ
    acc = 0.0
    pick = sel_idx[nsel - 1]
    for p in range(nsel):
        acc += probs[p]
        if target <= acc:
            pick = sel_idx[p]
            break
    return pick, s2


# ════════════════════════════════════════════════════════════════════════
# (b) CONV (CLM ConvMoE) — verbatim port of core/clm_decode.hexa
#     (formerly core/clm_decode.py). PRNG/dt_exp reused from SHARED above.
# ════════════════════════════════════════════════════════════════════════

# ── primitive math — ported 1:1 from stdlib/flame/*.hexa ──

def dt_ln(x):
    """flame_math.hexa::dt_ln — u=(x-1)/(x+1); 2*Σ_{k=0..23} u^(2k+1)/(2k+1).
    KNOWN-BUGGY for x far from 1 (diverges); reproduced verbatim for parity."""
    x = np.asarray(x, dtype=np.float64)
    scalar = (x.ndim == 0)
    x = np.atleast_1d(x)
    u = (x - 1.0) / (x + 1.0)
    u2 = u * u
    termp = u.copy()
    acc = np.zeros_like(u)
    k = 0
    while k < 24:
        acc = acc + termp / float(2 * k + 1)
        termp = termp * u2
        k = k + 1
    out = 2.0 * acc
    return float(out[0]) if scalar else out


def dt_erf(x):
    """flame_math.hexa::dt_erf — Abramowitz&Stegun 7.1.26, exp via dt_exp."""
    x = np.asarray(x, dtype=np.float64)
    scalar = (x.ndim == 0)
    x = np.atleast_1d(x)
    sign = np.where(x < 0.0, -1.0, 1.0)
    z = np.abs(x)
    t = 1.0 / (1.0 + 0.3275911 * z)
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    poly = ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t
    out = sign * (1.0 - poly * dt_exp(0.0 - z * z))
    return float(out[0]) if scalar else out


_INV_SQRT2 = 0.70710678118654752440
_INV_SQRT2PI = 0.39894228040143267794


def _nn_normal_cdf(x):
    return 0.5 * (1.0 + dt_erf(x * _INV_SQRT2))


def nn_gelu_fwd(g):
    """nn_lib.hexa::nn_gelu_fwd — GELU(x)=x*Phi(x), Phi via dt_erf (EXACT erf)."""
    g = np.asarray(g, dtype=np.float64)
    return g * _nn_normal_cdf(g)


def _moe_exp(x):
    """moe_lib.hexa::_moe_exp — ln2 range-reduce, 14-term Taylor, *2^n.
    DISTINCT from dt_exp (used ONLY in the MoE router softmax)."""
    x = np.asarray(x, dtype=np.float64)
    scalar = (x.ndim == 0)
    x = np.atleast_1d(x)
    ln2 = 0.6931471805599453
    r = x.copy()
    n = np.zeros(x.shape, dtype=np.int64)
    m = r > 0.34657359
    while m.any():
        r = np.where(m, r - ln2, r)
        n = np.where(m, n + 1, n)
        m = r > 0.34657359
    m = r < -0.34657359
    while m.any():
        r = np.where(m, r + ln2, r)
        n = np.where(m, n - 1, n)
        m = r < -0.34657359
    term = np.ones_like(r)
    summ = np.ones_like(r)
    k = 1
    while k < 14:
        term = term * r / float(k)
        summ = summ + term
        k = k + 1
    # *2^n via exact power-of-two scaling (== repeated *2 / /2 in hexa)
    p = summ * np.power(2.0, n.astype(np.float64))
    return float(p[0]) if scalar else p


def _gn_sqrt(x):
    """gn_lib.hexa::_gn_sqrt — Newton-Raphson 40 iters from g0=x. scalar.
    (DIVERGENT twin of bg's dt_sqrt — DO NOT merge; distinct name kept.)"""
    if x <= 0.0:
        return 0.0
    g = x
    i = 0
    while i < 40:
        g = 0.5 * (g + x / g)
        i = i + 1
    return g


def nn_groupnorm_fwd(x, gamma, beta, T, C, G):
    """gn_lib.hexa::nn_groupnorm_fwd — eps=1e-5. x:[T,C]. Returns y:[T,C].
    Here G is always 1 (=> normalize over all C per the whole [T,C] group)."""
    eps = 0.00001
    cg = C // G
    m = float(cg * T)
    x = x.reshape(T, C)
    y = np.empty_like(x)
    for grp in range(G):
        c0 = grp * cg
        sl = x[:, c0:c0 + cg]
        mu = sl.sum() / m
        var = ((sl - mu) * (sl - mu)).sum() / m
        inv = 1.0 / _gn_sqrt(var + eps)
        xh = (sl - mu) * inv
        y[:, c0:c0 + cg] = gamma[c0:c0 + cg] * xh + beta[c0:c0 + cg]
    return y


def nn_moe_softmax(logits, T, E):
    """moe_lib.hexa::nn_moe_softmax — stable softmax over E via _moe_exp. logits:[T,E]."""
    logits = logits.reshape(T, E)
    mx = logits.max(axis=1, keepdims=True)
    ev = _moe_exp(logits - mx)
    s = ev.sum(axis=1, keepdims=True)
    return ev / s


def nn_moe_router_fwd(logits_r, ex_out, T, E, C):
    """moe_lib.hexa::nn_moe_router_fwd — y[t,c]=Σ_e probs[t,e]*ex_out[e,t,c].
    ex_out:[E,T,C]. Returns y:[T,C]."""
    probs = nn_moe_softmax(logits_r, T, E)          # [T,E]
    ex = ex_out.reshape(E, T, C)
    # y[t,c] = Σ_e probs[t,e]*ex[e,t,c]
    y = np.einsum('te,etc->tc', probs, ex)
    return y


def nn_ce_loss_allpos(logits, targets, T, V):
    """nn_lib.hexa::nn_ce_loss_allpos — mean over T of -ln(softmax[tgt]).
    Stable softmax via dt_exp, pt_safe floor 1e-6, -ln via dt_ln. logits:[T,V]."""
    logits = logits.reshape(T, V)
    total = 0.0
    for t in range(T):
        row = logits[t]
        mx = row.max()
        tot = float(dt_exp(row - mx).sum())
        tgt = int(targets[t])
        p_t = float(dt_exp(np.array(row[tgt] - mx))) / tot
        pt_safe = p_t if p_t >= 0.000001 else 0.000001
        total = total + (0.0 - float(dt_ln(np.array(pt_safe))))
    return total / float(T)


# ── .clm file parse + int4 dequant — 1:1 from clm_decode.hexa _clmd_load* ──

def _rd_u32(rb, off):
    return rb[off] | (rb[off + 1] << 8) | (rb[off + 2] << 16) | (rb[off + 3] << 24)


def clm_decodable(path):
    """clm_decode.hexa::clm_decodable — CLM\\x01 header AND CLMX v0.2 trailer."""
    try:
        rb = open(path, 'rb').read()
    except Exception:
        return False
    if len(rb) < 5:
        return False
    if not (rb[0] == 67 and rb[1] == 76 and rb[2] == 77 and rb[3] == 1):
        return False
    nblk = rb[4]
    off = 5
    b = 0
    while b < nblk:
        if off + 8 > len(rb):
            return False
        cout = _rd_u32(rb, off)
        rest = _rd_u32(rb, off + 4)
        off = off + 8
        n = cout * rest
        off = off + (n + 1) // 2
        off = off + cout * 4
        b = b + 1
    if off + 5 > len(rb):
        return False
    return rb[off] == 67 and rb[off + 1] == 76 and rb[off + 2] == 77 and rb[off + 3] == 88


def clm_config(path):
    """clm_decode.hexa::clm_config — recover (d,K,V,E,L,nblk) from header."""
    if not clm_decodable(path):
        return {"ok": False}
    rb = open(path, 'rb').read()
    nblk = rb[4]
    d = _rd_u32(rb, 5)
    rest0 = _rd_u32(rb, 9)
    K = rest0 // d
    off = 5
    bi = 0
    E = 2
    V = 256
    while bi < nblk:
        c = _rd_u32(rb, off)
        r = _rd_u32(rb, off + 4)
        if bi == nblk - 2:
            E = c
        if bi == nblk - 1:
            V = c
        n = c * r
        off = off + 8 + (n + 1) // 2 + c * 4
        bi = bi + 1
    L = nblk - E - 3
    return {"ok": True, "d": d, "K": K, "V": V, "E": E, "L": L, "nblk": nblk}


def _load_block(rb, off):
    """_clmd_load_block — int4-sym dequant: w = (nibble-8) * per-channel-scale.
    Returns (w_2d[cout,rest], new_off)."""
    cout = _rd_u32(rb, off); off += 4
    rest = _rd_u32(rb, off); off += 4
    n = cout * rest
    nbytes = (n + 1) // 2
    raw = np.frombuffer(rb, dtype=np.uint8, count=nbytes, offset=off).astype(np.int64)
    off += nbytes
    low = (raw & 0xF) - 8
    high = ((raw >> 4) & 0xF) - 8
    codes = np.empty(2 * len(raw), dtype=np.float64)
    codes[0::2] = low
    codes[1::2] = high
    codes = codes[:n]
    scales = np.frombuffer(rb, dtype='<f4', count=cout, offset=off).astype(np.float64)
    off += cout * 4
    w = codes.reshape(cout, rest) * scales[:, None]
    return w, off


def _load_ext(rb, off):
    """_clmd_load_ext — length-prefixed fp32 tensor (n:u32, then n*f32 LE)."""
    n = _rd_u32(rb, off); off += 4
    vals = np.frombuffer(rb, dtype='<f4', count=n, offset=off).astype(np.float64)
    off += n * 4
    return vals, off


def clm_load_weights(path):
    """_clmd_load — full file parse into a weight dict. Conv weights are kept
    pre-transposed as Wt[Kdim,Cout] (the _clmd_scratch_new transpose, applied
    once) since the py forward GEMMs xcol[T,Kdim] @ Wt[Kdim,Cout]."""
    if not clm_decodable(path):
        return {"ok": False}
    rb = open(path, 'rb').read()
    nblk = rb[4]
    d = _rd_u32(rb, 5)
    rest0 = _rd_u32(rb, 9)
    K = rest0 // d
    # walk to find E (block nblk-2 cout), V (block nblk-1 cout)
    off = 5
    bi = 0
    E = 2
    V = 256
    while bi < nblk:
        c = _rd_u32(rb, off)
        r = _rd_u32(rb, off + 4)
        if bi == nblk - 2:
            E = c
        if bi == nblk - 1:
            V = c
        n = c * r
        off = off + 8 + (n + 1) // 2 + c * 4
        bi = bi + 1
    L = nblk - E - 3

    # ── conv blocks, in order: ec, tc[L], eW[E], rW, roW ──
    off = 5
    ecW, off = _load_block(rb, off)              # [d, d*K]
    tcW = []
    for _ in range(L):
        w, off = _load_block(rb, off); tcW.append(w)   # [d, d*K]
    eW = []
    for _ in range(E):
        w, off = _load_block(rb, off); eW.append(w)    # [d, d*K]
    rW, off = _load_block(rb, off)               # [E, d]
    roW, off = _load_block(rb, off)              # [V, d]
    off = off + 5                                # skip "CLMX" + n_ext byte

    # ── ext tensors, in order ──
    embed, off = _load_ext(rb, off)              # [V*d]
    ecB, off = _load_ext(rb, off)                # [d]
    tcB = []
    for _ in range(L):
        v, off = _load_ext(rb, off); tcB.append(v)     # [d]
    eB = []
    for _ in range(E):
        v, off = _load_ext(rb, off); eB.append(v)      # [d]
    rB, off = _load_ext(rb, off)                 # [E]
    roB, off = _load_ext(rb, off)                # [V]
    tgG = []
    for _ in range(L):
        v, off = _load_ext(rb, off); tgG.append(v)     # [d]
    tgB = []
    for _ in range(L):
        v, off = _load_ext(rb, off); tgB.append(v)     # [d]
    noG, off = _load_ext(rb, off)                # [d]
    noB, off = _load_ext(rb, off)                # [d]

    # pre-transpose conv weights -> Wt[Kdim, Cout] (= w_2d.T)
    W = {
        "ok": True, "d": d, "E": E, "V": V, "K": K, "L": L,
        "ecWt": ecW.T.copy(), "ecB": ecB,
        "tcWt": [w.T.copy() for w in tcW], "tcB": tcB,
        "eWt": [w.T.copy() for w in eW], "eB": eB,
        "rWt": rW.T.copy(), "rB": rB,
        "roWt": roW.T.copy(), "roB": roB,
        "embed": embed.reshape(V, d),
        "tgG": tgG, "tgB": tgB, "noG": noG, "noB": noB,
        "bind_type": 0,
    }

    # ── optional CLMB bind-readout section (serialize_v3_bind) ──────────────
    # "CLMB" = bytes 67,76,77,66. Present only when the .clm was serialized
    # with a Hadamard/linear bind readout retained in-forward (H_1818).
    # If absent, bind_type=0 and the standard additive _conv1d readout is used.
    # CLMB layout (after CLMX ext arrays):
    #   CLMB magic  67,76,77,66
    #   bind_type   u8  (1=Hadamard u*v, 2=linear u+v)
    #   Wa block    (k, d) int4-sym conv block
    #   Wb block    (k, d) int4-sym conv block
    #   WaB ext     u32 k + k*f32
    #   WbB ext     u32 k + k*f32
    # In a CLMB file, roW holds Wo (V, k) NOT (V, d); roWt = (k, V).
    if (off + 5 <= len(rb)
            and rb[off] == 67 and rb[off + 1] == 76
            and rb[off + 2] == 77 and rb[off + 3] == 66):
        off += 4                                   # skip "CLMB"
        bind_type = rb[off]; off += 1
        WaW, off = _load_block(rb, off)            # (k, d)
        WbW, off = _load_block(rb, off)            # (k, d)
        WaB_ext, off = _load_ext(rb, off)          # (k,)
        WbB_ext, off = _load_ext(rb, off)          # (k,)
        W["bind_type"] = int(bind_type)
        W["WaWt"] = WaW.T.copy()                   # (d, k)
        W["WbWt"] = WbW.T.copy()                   # (d, k)
        W["WaB"] = WaB_ext
        W["WbB"] = WbB_ext
        # roWt is already Wo.T = (k, V); roB is already WoB (V,) — loaded above.

    return W


# ── forward — 1:1 from clm_decode.hexa _clmd_conv1d / _clmd_fwd_logits_sc ──

def _conv1d(x, Wt, b, T, Cin, Cout, K, dil):
    """_clmd_conv1d_pre (host path) — causal dilated im2col + matmul + bias.
    x:[T,Cin], Wt:[Cin*K, Cout], b:[Cout]. Returns y:[T,Cout].
    im2col layout: xcol[t, ci*K + k] = x[t - dil*(K-1-k), ci] (0 if p<0)."""
    Kdim = Cin * K
    x = x.reshape(T, Cin)
    xcol = np.zeros((T, Cin, K), dtype=np.float64)
    t_idx = np.arange(T)
    for k in range(K):
        offset = dil * (K - 1 - k)
        p = t_idx - offset
        valid = p >= 0
        xcol[valid, :, k] = x[p[valid], :]
    xcol = xcol.reshape(T, Kdim)
    mm = xcol @ Wt                                # [T, Cout]
    return mm + b[None, :]


def _fwd_logits(W, tok, T):
    """_clmd_fwd_logits_sc (host path) — full CLMConvMoE forward. tok:[T] ids.
    Returns logits:[T, V]."""
    d = W["d"]; E = W["E"]; V = W["V"]; K = W["K"]; L = W["L"]
    # embedding
    ids = tok.astype(np.int64)
    xe = W["embed"][ids]                          # [T, d]
    # ec conv (K, dil=1)
    xt = _conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    # L trunk layers: xt = xt + gelu(groupnorm(conv(xt)))
    DIL_CAP = 512
    dil = 1
    for li in range(L):
        dil_eff = dil if dil <= DIL_CAP else DIL_CAP
        h = _conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, dil_eff)
        hn = nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1)
        hg = nn_gelu_fwd(hn)
        xt = xt + hg.reshape(T, d)
        dil = dil * 2
    # router conv (K=1, Cout=E)
    logits_r = _conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1)   # [T, E]
    # E experts: gelu(conv(xt))
    ex_out = np.empty((E, T, d), dtype=np.float64)
    for ej in range(E):
        eo = _conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1)
        ex_out[ej] = nn_gelu_fwd(eo).reshape(T, d)
    # MoE router mix
    y = nn_moe_router_fwd(logits_r, ex_out, T, E, d)          # [T, d]
    # final groupnorm
    yn = nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)
    # readout: additive Conv1d (standard) OR Hadamard/linear bind (CLMB)
    if W.get("bind_type", 0) != 0:
        # CLMB bind readout: yn → (Wa,Wb) linear projections → Hadamard/+ → Wo
        # WaWt=(d,k), WbWt=(d,k); roWt=(k,V) holds Wo.T; roB=(V,) holds WoB.
        u = yn @ W["WaWt"] + W["WaB"]             # [T, k]
        v = yn @ W["WbWt"] + W["WbB"]             # [T, k]
        g = u * v if W["bind_type"] == 1 else u + v   # Hadamard(1) or linear(2)
        out_logits = g @ W["roWt"] + W["roB"]     # [T, V]  roWt=(k,V)
    else:
        out_logits = _conv1d(yn, W["roWt"], W["roB"], T, d, V, 1, 1)  # [T, V]
    return out_logits


# ── public CLM decode/CE entries — 1:1 from clm_decode.hexa ──

def clm_forward_ce(path, corpus, nwin_max):
    """clm_decode.hexa::clm_forward_ce — mean CE over nwin_max T=24 causal
    windows; uniform_ce = dt_ln(V); green = model_ce < uniform AND < shuffle."""
    if not clm_decodable(path):
        return {"ok": False, "reason": "not v0.2-decodable", "green": False,
                "model_ce": 0.0, "shuffle_ce": 0.0, "uniform_ce": 0.0, "windows": 0}
    W = clm_load_weights(path)
    d = W["d"]; E = W["E"]; V = W["V"]; K = W["K"]
    bytes_arr = np.frombuffer(open(corpus, 'rb').read(), dtype=np.uint8)
    n_bytes = len(bytes_arr)
    T = 24
    stride = (n_bytes - T - 1) // nwin_max
    if stride < 1:
        stride = 1
    sum_model = 0.0; sum_shuf = 0.0; nwin = 0
    for s in range(nwin_max):
        base = s * stride
        if base + T + 1 <= n_bytes:
            tok = bytes_arr[base:base + T].astype(np.float64)
            tgt = bytes_arr[base + 1:base + T + 1].astype(np.float64)
            logits = _fwd_logits(W, tok, T)
            ce = nn_ce_loss_allpos(logits, tgt, T, V)
            sum_model += ce
            tgt_sh = tgt[::-1]
            sum_shuf += nn_ce_loss_allpos(logits, tgt_sh, T, V)
            nwin += 1
    model_ce = sum_model / float(nwin)
    shuf_ce = sum_shuf / float(nwin)
    uniform_ce = float(dt_ln(np.array(float(V))))
    lt_u = model_ce < uniform_ce
    lt_s = model_ce < shuf_ce
    return {"ok": True, "windows": nwin, "d": d, "E": E, "V": V, "K": K, "L": W["L"],
            "model_ce": model_ce, "shuffle_ce": shuf_ce, "uniform_ce": uniform_ce,
            "lt_uniform": lt_u, "lt_shuffle": lt_s, "green": lt_u and lt_s}


def clm_decode_argmax(path, seed, gen):
    """clm_decode.hexa::clm_decode_argmax — greedy continuation. T=24 window,
    right-aligned seed (pad-left byte 32). argmax ties: first (strict >)."""
    if not clm_decodable(path):
        return {"ok": False, "text": ""}
    W = clm_load_weights(path)
    V = W["V"]
    T = 24
    seed_b = seed.encode('utf-8', 'surrogateescape')
    slen = len(seed_b)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si = slen - T + p
        tok[p] = float(seed_b[si]) if si >= 0 else 32.0
    out = bytearray()
    for _ in range(gen):
        logits = _fwd_logits(W, tok, T)
        row = logits[T - 1]
        besti = 0
        bestv = row[0]
        for k in range(1, V):
            if row[k] > bestv:
                bestv = row[k]; besti = k
        out.append(besti)
        tok[:T - 1] = tok[1:]
        tok[T - 1] = float(besti)
    return {"ok": True, "text": out.decode('utf-8', 'surrogateescape')}


def clm_decode_topk_sampled(path, seed, gen, top_k, temp, seed_rng):
    """clm_decode.hexa::clm_decode_topk_sampled — seeded top-k temperature draw."""
    if not clm_decodable(path):
        return {"ok": False, "text": ""}
    W = clm_load_weights(path)
    return clm_decode_topk_sampled_W(W, seed, gen, top_k, temp, seed_rng)


def clm_decode_topk_sampled_W(W, seed, gen, top_k, temp, seed_rng):
    V = W["V"]
    T = 24
    seed_b = seed.encode('utf-8', 'surrogateescape')
    slen = len(seed_b)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si = slen - T + p
        tok[p] = float(seed_b[si]) if si >= 0 else 32.0
    out = bytearray()
    rng = _mix32(seed_rng)
    for _ in range(gen):
        logits = _fwd_logits(W, tok, T)
        nb, rng = _topk_sample(logits[T - 1], V, top_k, temp, rng)
        out.append(nb)
        tok[:T - 1] = tok[1:]
        tok[T - 1] = float(nb)
    return {"ok": True, "text": out.decode('utf-8', 'surrogateescape')}


# ════════════════════════════════════════════════════════════════════════
# (c) BYTE (ByteGPT transformer) — verbatim port of core/bytegpt_decode.hexa
#     (formerly core/bytegpt_decode.py) + byte-exact KV-cache fast path.
# ════════════════════════════════════════════════════════════════════════

# libm erf, vectorized elementwise (object-ufunc -> float64). The hexa GELU calls
# `extern fn erf` (the C libm scalar erf), so math.erf is the byte-faithful twin.
_erf_vec = np.frompyfunc(math.erf, 1, 1)


def dt_sqrt(x):
    """flame_math.hexa::dt_sqrt — Newton-Raphson 24 iters from g0=max(x,1).
    Scalar. (DIVERGENT twin of clm's _gn_sqrt: 40 iters from g0=x — kept distinct.)"""
    if x <= 0.0:
        return 0.0
    g = x if x > 1.0 else 1.0
    i = 0
    while i < 24:
        g = 0.5 * (g + x / g)
        i = i + 1
    return g


def _bg_gelu(x):
    """bytegpt_decode.hexa::_bg_gelu — 0.5*x*(1+erf(x*0.7071067811865476)).
    erf via libm (math.erf), NOT the dt_erf twin (ING#23 torch-parity)."""
    x = np.asarray(x, dtype=np.float64)
    e = _erf_vec(x * 0.7071067811865476).astype(np.float64)
    return 0.5 * x * (1.0 + e)


def _bg_layernorm_rows(X, g, b, T, d):
    """bytegpt_decode.hexa::_bg_layernorm — per-row LayerNorm over length d.
    biased variance, eps=1e-5, inv = 1/dt_sqrt(var+eps). X:[T,d]. Returns Y:[T,d].
    dt_sqrt is scalar per row (matching the hexa scalar while-loop)."""
    eps = 0.00001
    X = X.reshape(T, d)
    Y = np.empty_like(X)
    for i in range(T):
        row = X[i]
        mean = row.sum() / float(d)
        dv = row - mean
        var = (dv * dv).sum() / float(d)
        inv = 1.0 / dt_sqrt(var + eps)
        Y[i] = g * (dv * inv) + b
    return Y


# ── .bin header + weight load — 1:1 from bytegpt_decode.hexa _bg_rd_u32 / bg_load ──

# _bg_rd_u32 ≡ clm's _rd_u32 (byte-identical). Aliased to the single SHARED def.
_bg_rd_u32 = _rd_u32


def bg_header(path):
    """parse the 5xu32 header [vocab,d,n_layer,n_head,block]. Returns dict."""
    with open(path, 'rb') as f:
        hdr = f.read(20)
    if len(hdr) < 20:
        return {"ok": False}
    vocab = _bg_rd_u32(hdr, 0)
    d = _bg_rd_u32(hdr, 4)
    nlay = _bg_rd_u32(hdr, 8)
    nh = _bg_rd_u32(hdr, 12)
    block = _bg_rd_u32(hdr, 16)
    return {"ok": True, "vocab": vocab, "d": d, "nlay": nlay, "nh": nh, "block": block}


def bg_is_bytegpt(path):
    """mouth-sniff: NOT CLM\\x01 magic AND a sane 5xu32 ByteGPT header.
    Mirrors generator.hexa gen_auto_ideate dispatch (CLM\\x01 -> clm, else bytegpt)."""
    try:
        with open(path, 'rb') as f:
            hdr = f.read(20)
    except Exception:
        return False
    if len(hdr) < 20:
        return False
    # CLM\x01 magic => ConvMoE, not ByteGPT
    if hdr[0] == 67 and hdr[1] == 76 and hdr[2] == 77 and hdr[3] == 1:
        return False
    vocab = _bg_rd_u32(hdr, 0)
    d = _bg_rd_u32(hdr, 4)
    nlay = _bg_rd_u32(hdr, 8)
    nh = _bg_rd_u32(hdr, 12)
    block = _bg_rd_u32(hdr, 16)
    # sane ranges + d divisible by n_head (GPT invariant)
    if not (1 <= vocab <= 1 << 20 and 1 <= d <= 1 << 16 and 1 <= nlay <= 1024
            and 1 <= nh <= 1024 and 1 <= block <= 1 << 20):
        return False
    if d % nh != 0:
        return False
    return True


def _rd_f32(rb, off, n):
    """read n LE f32 from byte buffer at byte offset off -> float64 array[n]."""
    return np.frombuffer(rb, dtype='<f4', count=n, offset=off).astype(np.float64)


def _bg_read_bind_block(rb, off, d):
    """Read ONE BGB injected-bind block from the flat trailer at byte offset off.
    Layout = a base ByteGPT layer's 12 param tensors in bg_load order (LE f32),
    then one LE f32 scalar `gate`. Returns (block_dict, new_off).
    (Shapes match bg_load's per-layer read exactly — reference-matched, no reorder.)"""
    blk = {}
    blk["ln1w"] = _rd_f32(rb, off, d); off += d * 4
    blk["ln1b"] = _rd_f32(rb, off, d); off += d * 4
    blk["inW"] = _rd_f32(rb, off, 3 * d * d).reshape(3 * d, d); off += 3 * d * d * 4
    blk["inB"] = _rd_f32(rb, off, 3 * d); off += 3 * d * 4
    blk["oW"] = _rd_f32(rb, off, d * d).reshape(d, d); off += d * d * 4
    blk["oB"] = _rd_f32(rb, off, d); off += d * 4
    blk["ln2w"] = _rd_f32(rb, off, d); off += d * 4
    blk["ln2b"] = _rd_f32(rb, off, d); off += d * 4
    blk["m0W"] = _rd_f32(rb, off, 4 * d * d).reshape(4 * d, d); off += 4 * d * d * 4
    blk["m0B"] = _rd_f32(rb, off, 4 * d); off += 4 * d * 4
    blk["m2W"] = _rd_f32(rb, off, d * 4 * d).reshape(d, 4 * d); off += d * 4 * d * 4
    blk["m2B"] = _rd_f32(rb, off, d); off += d * 4
    blk["gate"] = float(_rd_f32(rb, off, 1)[0]); off += 4
    return blk, off


def bg_load(path):
    """bytegpt_decode.hexa::bg_load — parse the flat binary ONCE into a weight dict.
    Weight binary layout (LE f32, bytegpt_decode.hexa:29-36):
      [vocab,d,n_layer,n_head,block]  5xu32
      tok[vocab*d]  pos[block*d]
      per layer: ln1.w[d] ln1.b[d] in_proj.w[3d*d] in_proj.b[3d]
                 out_proj.w[d*d] out_proj.b[d] ln2.w[d] ln2.b[d]
                 mlp0.w[4d*d] mlp0.b[4d] mlp2.w[d*4d] mlp2.b[d]
      ln_f.w[d] ln_f.b[d]  head[vocab*d]
    (torch Linear stores W as [out,in] row-major; y = x.Wt + b.)"""
    rb = open(path, 'rb').read()
    vocab = _bg_rd_u32(rb, 0)
    d = _bg_rd_u32(rb, 4)
    nlay = _bg_rd_u32(rb, 8)
    nh = _bg_rd_u32(rb, 12)
    block = _bg_rd_u32(rb, 16)
    off = 20

    tok = _rd_f32(rb, off, vocab * d).reshape(vocab, d); off += vocab * d * 4
    pos = _rd_f32(rb, off, block * d).reshape(block, d); off += block * d * 4

    ln1w = []; ln1b = []; inW = []; inB = []
    oW = []; oB = []; ln2w = []; ln2b = []
    m0W = []; m0B = []; m2W = []; m2B = []
    for _ in range(nlay):
        ln1w.append(_rd_f32(rb, off, d)); off += d * 4
        ln1b.append(_rd_f32(rb, off, d)); off += d * 4
        inW.append(_rd_f32(rb, off, 3 * d * d).reshape(3 * d, d)); off += 3 * d * d * 4
        inB.append(_rd_f32(rb, off, 3 * d)); off += 3 * d * 4
        oW.append(_rd_f32(rb, off, d * d).reshape(d, d)); off += d * d * 4
        oB.append(_rd_f32(rb, off, d)); off += d * 4
        ln2w.append(_rd_f32(rb, off, d)); off += d * 4
        ln2b.append(_rd_f32(rb, off, d)); off += d * 4
        m0W.append(_rd_f32(rb, off, 4 * d * d).reshape(4 * d, d)); off += 4 * d * d * 4
        m0B.append(_rd_f32(rb, off, 4 * d)); off += 4 * d * 4
        m2W.append(_rd_f32(rb, off, d * 4 * d).reshape(d, 4 * d)); off += d * 4 * d * 4
        m2B.append(_rd_f32(rb, off, d)); off += d * 4
    lnfw = _rd_f32(rb, off, d); off += d * 4
    lnfb = _rd_f32(rb, off, d); off += d * 4
    head = _rd_f32(rb, off, vocab * d).reshape(vocab, d); off += vocab * d * 4

    # ── optional BGB injected-bind trailer (serialize_bind, H_9027) ──────
    # "BGB\x01" = bytes 66,71,66,1, appended AFTER `head`. Carries n_bind appended
    # GATED transformer blocks (each = a standard base layer: the SAME 12 param
    # tensors in the SAME order/layout as above, then one LE f32 gate). Applied
    # after the L base blocks and BEFORE ln_f (mirrors the CLM "CLMB" bind-trailer
    # precedent). ABSENT trailer => bind=[] => forward BYTE-IDENTICAL to plain ByteGPT.
    bind = []
    if (off + 8 <= len(rb)
            and rb[off] == 66 and rb[off + 1] == 71
            and rb[off + 2] == 66 and rb[off + 3] == 1):
        off += 4                                          # skip "BGB\x01"
        n_bind = _bg_rd_u32(rb, off); off += 4
        for _ in range(n_bind):
            blk, off = _bg_read_bind_block(rb, off, d)
            bind.append(blk)

    return {"ok": True, "vocab": vocab, "d": d, "nlay": nlay, "nh": nh, "block": block,
            "tok": tok, "pos": pos, "ln1w": ln1w, "ln1b": ln1b,
            "inW": inW, "inB": inB, "oW": oW, "oB": oB,
            "ln2w": ln2w, "ln2b": ln2b, "m0W": m0W, "m0B": m0B,
            "m2W": m2W, "m2B": m2B, "lnfw": lnfw, "lnfb": lnfb, "head": head,
            "bind": bind}


# bg_load_ranged — byte-identical W-map to bg_load (hexa builds it via ranged
# read_bytes_at to dodge the whole-file boxing OOM; the resulting weights are the
# same, and the py read already mmaps lazily via frombuffer). Aliased for surface
# parity with the hexa public entries (bytegpt_decode.hexa:782).
bg_load_ranged = bg_load


# ── forward — 1:1 from bytegpt_decode.hexa _bg_mha / _bg_linear / bg_forward_last_W ──

def _bg_mha(H, inW, inB, oW, oB, T, d, nh):
    """bytegpt_decode.hexa::_bg_mha — torch nn.MultiheadAttention semantics.
    H:[T,d] pre-normed. in_proj W[3d,d] rows Q|K|V; out_proj W[d,d]+b.
    scale=1/dt_sqrt(hd), causal, libm exp softmax. Returns Aout:[T,d]."""
    hd = d // nh
    scale = 1.0 / dt_sqrt(float(hd))
    # QKV = H[T,d] @ inW.T[d,3d] + inB  -> packed [T,3d]; Q=cols0..d, K=d..2d, V=2d..3d
    QKV = H @ inW.T + inB                                  # [T, 3d]
    Q = QKV[:, 0:d]; K = QKV[:, d:2 * d]; V = QKV[:, 2 * d:3 * d]
    ctx = np.zeros((T, d), dtype=np.float64)
    for hh in range(nh):
        base = hh * hd
        Qh = Q[:, base:base + hd]; Kh = K[:, base:base + hd]; Vh = V[:, base:base + hd]
        for i in range(T):
            L = i + 1
            # scores over keys 0..i, scaled
            sc = (Qh[i] @ Kh[0:L].T) * scale                # [L]
            mx = sc.max()
            e = np.exp(sc - mx)                             # libm-equivalent
            tot = e.sum()
            ctx[i, base:base + hd] = (e / tot) @ Vh[0:L]    # [hd]
    # out proj: Aout = ctx @ oW.T + oB
    return ctx @ oW.T + oB


def _bg_apply_bind(x, bind, T, d, nh):
    """Apply N appended GATED transformer blocks to the full post-base sequence
    x:[T,d], AFTER the L base blocks and BEFORE ln_f. Each block is a STANDARD
    transformer block (reuses _bg_layernorm_rows / _bg_mha / _bg_gelu — the exact
    base-layer ops) plus a scalar gate:
        block(x) = x + mha(ln1(x)) + mlp(ln2(x + mha(ln1(x))))
        x        = x + gate * (block(x) - x)          # gate=0 => identity (exact)
    Mirrors BindAttnByteGPT.forward `x = x + gate*(bind(x)-x)`. Returns x:[T,d]."""
    for blk in bind:
        nrm = _bg_layernorm_rows(x, blk["ln1w"], blk["ln1b"], T, d)
        aout = _bg_mha(nrm, blk["inW"], blk["inB"], blk["oW"], blk["oB"], T, d, nh)
        xa = x + aout                                      # x + mha(ln1(x))
        nrm2 = _bg_layernorm_rows(xa, blk["ln2w"], blk["ln2b"], T, d)
        h4 = _bg_gelu(nrm2 @ blk["m0W"].T + blk["m0B"])    # [T, 4d]
        mlpo = h4 @ blk["m2W"].T + blk["m2B"]              # [T, d]
        blk_out = xa + mlpo                                # = block(x)
        x = x + blk["gate"] * (blk_out - x)                # gate=0 => x unchanged
    return x


def bg_forward_last_W(W, ids, T):
    """bytegpt_decode.hexa::bg_forward_last_W — full forward from a loaded weight
    dict; returns last-position next-byte logits float64[vocab]. ids:[T] int.
    When W["bind"] is non-empty the appended gated blocks run after the L base
    blocks and before ln_f (H_9027); absent/empty => byte-identical to before."""
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]; vocab = W["vocab"]
    ids = np.asarray(ids, dtype=np.int64)
    # x[T,d] = tok[id] + pos[t]
    x = W["tok"][ids] + W["pos"][0:T]                       # [T, d]
    for Lr in range(nlay):
        # attn sub-block: x = x + MHA(LN1(x))
        nrm = _bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], T, d)
        aout = _bg_mha(nrm, W["inW"][Lr], W["inB"][Lr], W["oW"][Lr], W["oB"][Lr], T, d, nh)
        x = x + aout
        # mlp sub-block: x = x + Wd(GELU(W0(LN2(x))))
        nrm = _bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], T, d)
        h4 = nrm @ W["m0W"][Lr].T + W["m0B"][Lr]            # [T, 4d]
        h4 = _bg_gelu(h4)
        mlpo = h4 @ W["m2W"][Lr].T + W["m2B"][Lr]           # [T, d]
        x = x + mlpo
    # appended injected-bind blocks (H_9027) — after base stack, before ln_f
    if W.get("bind"):
        x = _bg_apply_bind(x, W["bind"], T, d, nh)
    # final LayerNorm on the LAST position only, then tied head
    lastrow = _bg_layernorm_rows(x[T - 1:T], W["lnfw"], W["lnfb"], 1, d)[0]   # [d]
    logits = W["head"] @ lastrow                            # [vocab]
    return logits


def bytegpt_forward_last(path, ids, T):
    """bytegpt_decode.hexa::bytegpt_forward_last — load + forward (parity probe)."""
    W = bg_load(path)
    return bg_forward_last_W(W, ids, T)


def bg_argmax(a):
    """bytegpt_decode.hexa::bg_argmax — index of max (ties: first, strict >)."""
    bi = 0
    bv = a[0]
    for k in range(1, len(a)):
        if a[k] > bv:
            bv = a[k]; bi = k
    return bi


def _seed_to_ids(seed):
    """string|bytes|list -> list[int] byte ids."""
    if isinstance(seed, (list, tuple)):
        return [int(x) for x in seed]
    if isinstance(seed, str):
        seed = seed.encode('utf-8', 'surrogateescape')
    return list(seed)


# ── KV-cache fast path — NEW (byte-exact TOKEN stream vs full-forward) ───────
#
# The full-forward loop re-forwards ALL T window tokens every decode step
# (O(gen²)). The KV path caches per-layer (K,V) = the in_proj K,V slices from
# _bg_mha and, on each new token, forwards ONLY the new position, attending it
# against the cached K,V of all layers. This mirrors the hexa KV-cache
# (bytegpt_decode.hexa:919, proven byte-identical to full-forward there).
#
# WINDOW-SLIDE RESYNC: ByteGPT indexes the positional embedding by position
# WITHIN the window (pos[0:T]), not by absolute token index. While the window is
# still GROWING (n <= block, start=0) every cached position keeps its window
# index → K,V stay valid → cheap incremental append. Once the window SLIDES
# (n > block, start>0) every token's window position shifts by one → its pos
# embedding (hence K,V) changes → the cache is INVALID and is fully REBUILT at
# M=T (byte-identical to full-forward for that window). So sliding steps cost a
# full forward (correct, not faster); the speedup is the growing-window regime,
# which is the entire eval decode path (seed+gen << block=512 for the 303M).

def _bg_forward_build(W, ids, T):
    """Full-forward over the window (== bg_forward_last_W) that ALSO captures the
    per-layer (K,V) in_proj slices for every position. Returns (logits, cache)
    where cache[Lr] = [K[T,d], V[T,d]]. The last-position logits are byte-
    identical to bg_forward_last_W (same ops, M=T batched)."""
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]
    ids = np.asarray(ids, dtype=np.int64)
    x = W["tok"][ids] + W["pos"][0:T]                       # [T, d]
    hd = d // nh
    scale = 1.0 / dt_sqrt(float(hd))
    cache = []
    for Lr in range(nlay):
        nrm = _bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], T, d)
        QKV = nrm @ W["inW"][Lr].T + W["inB"][Lr]          # [T, 3d]
        Q = QKV[:, 0:d]; K = QKV[:, d:2 * d]; V = QKV[:, 2 * d:3 * d]
        ctx = np.zeros((T, d), dtype=np.float64)
        for hh in range(nh):
            base = hh * hd
            Qh = Q[:, base:base + hd]; Kh = K[:, base:base + hd]; Vh = V[:, base:base + hd]
            for i in range(T):
                L = i + 1
                sc = (Qh[i] @ Kh[0:L].T) * scale
                mx = sc.max()
                e = np.exp(sc - mx)
                tot = e.sum()
                ctx[i, base:base + hd] = (e / tot) @ Vh[0:L]
        aout = ctx @ W["oW"][Lr].T + W["oB"][Lr]
        x = x + aout
        nrm = _bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], T, d)
        h4 = nrm @ W["m0W"][Lr].T + W["m0B"][Lr]
        h4 = _bg_gelu(h4)
        mlpo = h4 @ W["m2W"][Lr].T + W["m2B"][Lr]
        x = x + mlpo
        cache.append([K.copy(), V.copy()])
    lastrow = _bg_layernorm_rows(x[T - 1:T], W["lnfw"], W["lnfb"], 1, d)[0]
    logits = W["head"] @ lastrow
    return logits, cache


def _bg_kv_step(W, cache, id_new, win_pos):
    """Forward ONLY the new position (window index win_pos, byte id id_new),
    attending against + appending to the per-layer K,V cache. Returns the new
    position's next-byte logits. cache[Lr]=[K,V] is grown in place by one row.
    Reuses the EXACT _bg_mha attention ops (same scale, libm exp softmax, same
    per-output accumulation order) so the token stream matches full-forward."""
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]
    hd = d // nh
    scale = 1.0 / dt_sqrt(float(hd))
    x = (W["tok"][int(id_new)] + W["pos"][win_pos]).astype(np.float64).reshape(1, d)
    for Lr in range(nlay):
        nrm = _bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], 1, d)       # [1,d]
        qkv = nrm @ W["inW"][Lr].T + W["inB"][Lr]                             # [1,3d]
        qn = qkv[:, 0:d]; kn = qkv[:, d:2 * d]; vn = qkv[:, 2 * d:3 * d]      # [1,d]
        Kc = np.concatenate([cache[Lr][0], kn], axis=0)                       # [T,d]
        Vc = np.concatenate([cache[Lr][1], vn], axis=0)
        cache[Lr][0] = Kc; cache[Lr][1] = Vc
        ctx = np.zeros((1, d), dtype=np.float64)
        for hh in range(nh):
            base = hh * hd
            qh = qn[0, base:base + hd]              # [hd]
            Kh = Kc[:, base:base + hd]              # [T,hd]
            Vh = Vc[:, base:base + hd]              # [T,hd]
            sc = (qh @ Kh.T) * scale                # [T]
            mx = sc.max()
            e = np.exp(sc - mx)
            tot = e.sum()
            ctx[0, base:base + hd] = (e / tot) @ Vh
        aout = ctx @ W["oW"][Lr].T + W["oB"][Lr]                              # [1,d]
        x = x + aout
        nrm = _bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], 1, d)
        h4 = nrm @ W["m0W"][Lr].T + W["m0B"][Lr]
        h4 = _bg_gelu(h4)
        mlpo = h4 @ W["m2W"][Lr].T + W["m2B"][Lr]
        x = x + mlpo
    lastrow = _bg_layernorm_rows(x, W["lnfw"], W["lnfb"], 1, d)[0]
    logits = W["head"] @ lastrow
    return logits


def _bg_step_logits(W, toks, st):
    """One decode step's last-position logits via KV cache. `st` is a mutable
    dict {'cache','start'} carried across steps. Builds (M=T) on the first step
    OR whenever the window slides (start changes = pos-embedding re-index); else
    appends the single new token incrementally."""
    block = W["block"]
    n = len(toks)
    start = n - block if n > block else 0
    T = n - start
    # Injected-bind models (H_9027): the appended blocks have their OWN attention
    # over the full post-base sequence, which the incremental KV step can't supply
    # from base-layer K,V alone — so decode via the full-sequence forward (byte-
    # exact vs the torch reference; gate=0 => identical to the base KV stream since
    # the base forward is unchanged and the bind contribution is exactly zero).
    if W.get("bind"):
        return bg_forward_last_W(W, toks[start:start + T], T)
    if st['cache'] is None or start != st['start']:
        logits, cache = _bg_forward_build(W, toks[start:start + T], T)
        st['cache'] = cache; st['start'] = start
        return logits
    # incremental: the new token is at window position T-1 (= toks[start+T-1]).
    return _bg_kv_step(W, st['cache'], toks[start + T - 1], T - 1)


# ── public decode entries — 1:1 from bytegpt_decode.hexa (KV path wired in) ──

def bytegpt_decode_argmax(path, seed_ids, gen):
    """bytegpt_decode.hexa::bytegpt_decode_argmax — greedy continuation, weights
    loaded ONCE, prompt window grown (capped at block). Returns {ok,text,ids}.
    (Decode loop = byte-exact KV cache; full-forward reference = _decode_argmax_W_full.)"""
    W = bg_load(path)
    return _decode_argmax_W(W, seed_ids, gen)


# bytegpt_decode_argmax_ranged — OOM-safe twin (hexa: bg_load_ranged). Same compute.
def bytegpt_decode_argmax_ranged(path, seed_ids, gen):
    W = bg_load_ranged(path)
    return _decode_argmax_W(W, seed_ids, gen)


def _decode_argmax_W(W, seed_ids, gen):
    """KV-cache greedy decode from an already-loaded weight dict. Token stream is
    byte-exact vs _decode_argmax_W_full (the O(gen²) full-forward reference)."""
    toks = _seed_to_ids(seed_ids)
    outl = []
    st = {'cache': None, 'start': None}
    for _ in range(gen):
        logits = _bg_step_logits(W, toks, st)
        nb = bg_argmax(logits)
        toks.append(nb)
        outl.append(nb)
    text = bytes(outl).decode('utf-8', 'surrogateescape')
    return {"ok": True, "text": text, "ids": outl}


def _decode_argmax_W_full(W, seed_ids, gen):
    """ORIGINAL O(gen²) full-forward greedy decode (KV-cache OFF). Retained as the
    byte-exactness reference for the self-test."""
    vocab = W["vocab"]; block = W["block"]
    toks = _seed_to_ids(seed_ids)
    outl = []
    for _ in range(gen):
        n = len(toks)
        start = n - block if n > block else 0
        T = n - start
        ids = toks[start:start + T]
        logits = bg_forward_last_W(W, ids, T)
        nb = bg_argmax(logits)
        toks.append(nb)
        outl.append(nb)
    text = bytes(outl).decode('utf-8', 'surrogateescape')
    return {"ok": True, "text": text, "ids": outl}


def bytegpt_decode_topk_sampled(path, seed_ids, gen, top_k, temp, seed_rng):
    """bytegpt_decode.hexa::bytegpt_decode_topk_sampled — seeded top-k temp draw."""
    W = bg_load(path)
    return bytegpt_decode_topk_sampled_W(W, seed_ids, gen, top_k, temp, seed_rng)


# OOM-safe twin (hexa: bytegpt_decode_topk_sampled_ranged via bg_load_ranged).
def bytegpt_decode_topk_sampled_ranged(path, seed_ids, gen, top_k, temp, seed_rng):
    W = bg_load_ranged(path)
    return bytegpt_decode_topk_sampled_W(W, seed_ids, gen, top_k, temp, seed_rng)


def bytegpt_decode_topk_sampled_W(W, seed_ids, gen, top_k, temp, seed_rng):
    """KV-cache seeded top-k decode from an already-loaded weight dict (== hexa
    _bg_gen_from_W KV branch). seed_ids = string|bytes|list of byte ids. Token
    stream is byte-exact vs bytegpt_decode_topk_sampled_W_full."""
    vocab = W["vocab"]
    toks = _seed_to_ids(seed_ids)
    outl = []
    rng = _mix32(seed_rng)
    st = {'cache': None, 'start': None}
    for _ in range(gen):
        logits = _bg_step_logits(W, toks, st)
        nb, rng = _topk_sample(logits, vocab, top_k, temp, rng)
        toks.append(nb)
        outl.append(nb)
    text = bytes(outl).decode('utf-8', 'surrogateescape')
    return {"ok": True, "text": text, "ids": outl}


def bytegpt_decode_topk_sampled_W_full(W, seed_ids, gen, top_k, temp, seed_rng):
    """ORIGINAL O(gen²) full-forward seeded top-k decode (KV-cache OFF). Retained
    as the byte-exactness reference for the self-test."""
    vocab = W["vocab"]; block = W["block"]
    toks = _seed_to_ids(seed_ids)
    outl = []
    rng = _mix32(seed_rng)
    for _ in range(gen):
        n = len(toks)
        start = n - block if n > block else 0
        T = n - start
        ids = toks[start:start + T]
        logits = bg_forward_last_W(W, ids, T)
        nb, rng = _topk_sample(logits, vocab, top_k, temp, rng)
        toks.append(nb)
        outl.append(nb)
    text = bytes(outl).decode('utf-8', 'surrogateescape')
    return {"ok": True, "text": text, "ids": outl}


# ════════════════════════════════════════════════════════════════════════
# (d) MOUTH DISPATCH — header-sniff (mirrors generator.hexa gen_auto_backend).
#     CLM\x01 magic + CLMX trailer => conv (.clm); sane 5xu32 header => byte (.bin).
# ════════════════════════════════════════════════════════════════════════

def decode_mouth_kind(path):
    """gen_mouth_kind — 'clm' | 'bytegpt' | 'unknown'. clm checked FIRST (its
    CLM\\x01 magic is what bg_is_bytegpt explicitly rejects)."""
    if clm_decodable(path):
        return "clm"
    if bg_is_bytegpt(path):
        return "bytegpt"
    return "unknown"


def decode_load(path):
    """gen_auto_backend — load the correct weight dict by mouth sniff. Returns
    (kind, W). kind in {'clm','bytegpt'}; raises for an unknown mouth."""
    k = decode_mouth_kind(path)
    if k == "clm":
        return "clm", clm_load_weights(path)
    if k == "bytegpt":
        return "bytegpt", bg_load(path)
    raise RuntimeError("ckpt not decodable (unknown mouth): " + str(path))


def decode_auto_topk_sampled(path, seed, gen, top_k, temp, seed_rng):
    """gen_auto_chat — dispatch a seeded top-k decode to the correct mouth by
    header sniff (conv .clm -> clm_decode_topk_sampled_W; byte .bin ->
    bytegpt_decode_topk_sampled_W, KV cache). seed = string."""
    kind, W = decode_load(path)
    if kind == "clm":
        return clm_decode_topk_sampled_W(W, seed, gen, top_k, temp, seed_rng)
    return bytegpt_decode_topk_sampled_W(W, seed, gen, top_k, temp, seed_rng)


def decode_auto_argmax(path, seed, gen):
    """gen_auto (greedy) — dispatch argmax decode by header sniff. seed = string.
    (clm uses its T=24 right-aligned window; bytegpt grows the window to block.)"""
    kind, W = decode_load(path)
    if kind == "clm":
        # clm_decode_argmax loads-from-path; re-wrap on the already-loaded W path
        V = W["V"]; T = 24
        seed_b = seed.encode('utf-8', 'surrogateescape')
        slen = len(seed_b)
        tok = np.empty(T, dtype=np.float64)
        for p in range(T):
            si = slen - T + p
            tok[p] = float(seed_b[si]) if si >= 0 else 32.0
        out = bytearray()
        for _ in range(gen):
            logits = _fwd_logits(W, tok, T)
            row = logits[T - 1]
            besti = 0; bestv = row[0]
            for k in range(1, V):
                if row[k] > bestv:
                    bestv = row[k]; besti = k
            out.append(besti)
            tok[:T - 1] = tok[1:]
            tok[T - 1] = float(besti)
        return {"ok": True, "text": out.decode('utf-8', 'surrogateescape')}
    return _decode_argmax_W(W, seed, gen)
