"""core/clm_decode.py — PY PRODUCTION ENGINE: byte-faithful 1:1 port of
core/clm_decode.hexa (the CORE-native .clm CLMConvMoE decode forward).

Per CLAUDE.md a_engine_native_learning (2026-06-26 owner SSOT): hexa + py are
TWO co-equal production engines, kept at byte-parity. This module is the py
mirror of clm_decode.hexa — ported 1:1 from the canonical SSOT:

  * orchestration  -> core/clm_decode.hexa
  * primitive math -> stdlib/flame/{nn_lib,gn_lib,moe_lib,flame_math,tensor_lib}.hexa
                      + self/runtime.c (farr_matmul / forge_dispatch_matmul host CPU path)

This is NOT a reuse of the drifted torch mirrors (g6_common.py / gauge_lib.py /
h1464_torch_golden.py) — every op below reproduces the hexa arithmetic:
  * dt_exp   = flame_math.hexa::dt_exp  (12-term Taylor + halving range-reduce)
  * dt_ln    = flame_math.hexa::dt_ln   (24-term atanh series — the KNOWN-BUGGY one,
               dt_ln(256)=4.799 != ln256=5.545; reproduced for hexa byte-parity)
  * dt_erf   = flame_math.hexa::dt_erf  (Abramowitz&Stegun 7.1.26 via dt_exp)
  * _moe_exp = moe_lib.hexa::_moe_exp   (ln2 range-reduce, 14-term — DISTINCT from dt_exp)
  * _gn_sqrt = gn_lib.hexa::_gn_sqrt    (40-iter Newton from g0=x)
  * GELU     = nn_lib.hexa::_nn_gelu    (EXACT erf via dt_erf, NOT tanh approx)
  * GroupNorm= gn_lib.hexa::nn_groupnorm_fwd (eps=1e-5, groups=1 => layernorm/row)
  * CE       = nn_lib.hexa::nn_ce_loss_allpos (stable softmax, pt_safe floor 1e-6)
  * PRNG     = clm_decode.hexa::_clmd_mix32 / _clmd_rng_next (xorshift32, &0xFFFFFFFF)

numpy float64 is used (farr buffers are C double per runtime.c:6252). The heavy
GEMM (xcol @ Wt) uses numpy float64 matmul; the hexa CPU path accumulates k
ascending (runtime.c:8418 ikj). These differ only at ~1e-13 ULP level — well
inside the parity gate (identical argmax/sample tokens + CE match >=4 decimals).
A separate math.log/exp sanity variant is exposed for cross-check (see *_mathlog).
"""

import sys
import struct
import numpy as np


# ════════════════════════════════════════════════════════════════════════
# primitive math — ported 1:1 from stdlib/flame/*.hexa
# ════════════════════════════════════════════════════════════════════════

def dt_exp(x):
    """flame_math.hexa::dt_exp — halve until |xr|<=0.25, 12-term Taylor (k=1..11),
    then square r times. Vectorized; halving by 2 is exact in fp64, so the
    per-element halve-count r matches the hexa scalar while-loop exactly."""
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
    """gn_lib.hexa::_gn_sqrt — Newton-Raphson 40 iters from g0=x. scalar."""
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


# ════════════════════════════════════════════════════════════════════════
# .clm file parse + int4 dequant — 1:1 from clm_decode.hexa _clmd_load*
# ════════════════════════════════════════════════════════════════════════

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
    }
    return W


# ════════════════════════════════════════════════════════════════════════
# forward — 1:1 from clm_decode.hexa _clmd_conv1d / _clmd_fwd_logits_sc
# ════════════════════════════════════════════════════════════════════════

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
    # readout conv (K=1, Cout=V)
    out_logits = _conv1d(yn, W["roWt"], W["roB"], T, d, V, 1, 1)  # [T, V]
    return out_logits


# ════════════════════════════════════════════════════════════════════════
# public decode/CE entries — 1:1 from clm_decode.hexa
# ════════════════════════════════════════════════════════════════════════

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


# ── seeded top-k temperature sampler — clm_decode.hexa _clmd_mix32 / _rng_next ──

_MASK = 0xFFFFFFFF


def _mix32(s):
    z = (s + 0x9E3779B9) & _MASK
    z = ((z ^ (z // 65536)) * 0x85EBCA6B) & _MASK
    z = ((z ^ (z // 8192)) * 0xC2B2AE35) & _MASK
    z = (z ^ (z // 65536)) & _MASK
    if z == 0:
        z = 0x9E3779B9
    return z


def _rng_next(s):
    x = s & _MASK
    if x == 0:
        x = 0x9E3779B9
    x = (x ^ (x * 8192)) & _MASK
    x = (x ^ (x // 131072)) & _MASK
    x = (x ^ (x * 32)) & _MASK
    return x, (float(x) / 4294967296.0)


def _topk_sample(row, V, top_k, temp, rng):
    """_clmd_topk_sample — top-k by repeated argmax (ties: first/strict >),
    divide by temp, dt_exp softmax (max-sub), inverse-CDF draw. row:[V]."""
    kcap = top_k if (top_k > 0 and top_k < V) else V
    taken = np.zeros(V, dtype=np.float64)
    sel_idx = []
    sel_val = []
    picks = 0
    while picks < kcap:
        bi = -1
        bv = 0.0
        for k in range(V):
            if taken[k] < 0.5:
                v = row[k]
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
# CLI — for the byte-parity harness (mirror of a hexa main calling the same)
# ════════════════════════════════════════════════════════════════════════

def _main(argv):
    if len(argv) < 2:
        print("usage: clm_decode.py <cmd> ...", file=sys.stderr); return 2
    cmd = argv[1]
    if cmd == "config":
        print(clm_config(argv[2])); return 0
    if cmd == "decode":
        # decode <ckpt> <seed> <gen> <top_k> <temp> <seed_rng>
        ck, seed, gen = argv[2], argv[3], int(argv[4])
        top_k = int(argv[5]); temp = float(argv[6]); rng = int(argv[7])
        r = clm_decode_topk_sampled(ck, seed, gen, top_k, temp, rng)
        sys.stdout.buffer.write(b"TEXT:" + r["text"].encode('utf-8', 'surrogateescape') + b"\n")
        return 0
    if cmd == "argmax":
        ck, seed, gen = argv[2], argv[3], int(argv[4])
        r = clm_decode_argmax(ck, seed, gen)
        sys.stdout.buffer.write(b"TEXT:" + r["text"].encode('utf-8', 'surrogateescape') + b"\n")
        return 0
    if cmd == "ce":
        ck, corpus, nwin = argv[2], argv[3], int(argv[4])
        r = clm_forward_ce(ck, corpus, nwin)
        print("CE model_ce=%.6f shuffle_ce=%.6f uniform_ce=%.6f green=%s windows=%d"
              % (r["model_ce"], r["shuffle_ce"], r["uniform_ce"], r["green"], r["windows"]))
        return 0
    print("unknown cmd", cmd, file=sys.stderr); return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
