"""core/bytegpt_decode.py — PY PRODUCTION ENGINE: byte-faithful 1:1 port of
core/bytegpt_decode.hexa (the CORE-native ByteGPT transformer next-byte decode).

Per CLAUDE.md a_engine_native_learning + a_core_engine_map: hexa + py are TWO
co-equal production engines, kept at byte-parity. This module is the py mirror of
bytegpt_decode.hexa — the parallel of clm_decode.py (which mirrors clm_decode.hexa,
the ConvMoE mouth). ByteGPT is the GPT-style transformer mouth (5xu32
[vocab,d,n_layer,n_head,block] header, NOT CLM\\x01; LayerNorm + learned-pos + MHA +
GELU-exact MLP, head tied to tok). Ported 1:1 from the canonical SSOT:

  * orchestration  -> core/bytegpt_decode.hexa
  * primitive math -> libm erf/exp (the hexa forward uses `extern fn erf/exp`,
                      NOT the dt_* twins — ING#23: dt-erf/dt-exp drifts argmax at
                      303M/L24, so the inference forward is libm to byte-match torch)
                      + stdlib/flame/flame_math.hexa::{dt_sqrt, dt_exp}

Math faithfulness (which transcendental each op uses — verbatim from the hexa):
  * GELU            = 0.5*x*(1+erf(x/sqrt2))   via libm erf      (bytegpt_decode.hexa:76)
  * attention exp   = libm exp                                    (bytegpt_decode.hexa:230,317)
  * LayerNorm 1/std = 1/dt_sqrt(var+eps)  eps=1e-5 (biased var)   (bytegpt_decode.hexa:98)
  * attn scale      = 1/dt_sqrt(hd)                               (bytegpt_decode.hexa:262)
  * top-k sampler   = dt_exp softmax (flame_math, the Taylor twin) (bytegpt_decode.hexa:1295)
  * PRNG            = _g6_mix32 / _g6_rng_next (xorshift32, &0xFFFFFFFF) (bytegpt_decode.hexa:1233)

numpy float64 is used (farr buffers are C double). The d-dim projection GEMMs go
through numpy float64 matmul (X @ W.T + b); the hexa CPU path (mm()->farr_matmul)
accumulates k ascending (ikj). These differ only at ~1e-13 ULP — well inside the
parity gate (identical argmax/sample token streams + logits match >=~12 dp). The
KV-cache fast path in the hexa is byte-identical to its full-forward reference
(bytegpt_decode.hexa:919 proof), so this py mirror implements ONLY the full-forward
window-growth path and still matches the hexa cache output token-for-token.
"""

import sys
import math
import os
import struct
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# dt_exp = flame_math.hexa::dt_exp (12-term Taylor, halve@0.25, square r). Reused
# from the parity-proven clm_decode.py port — the ByteGPT top-k sampler softmax uses
# the SAME dt_exp (bytegpt_decode.hexa:1295 `dt_exp(sel_val[j]-mx)`).
from clm_decode import dt_exp


# ════════════════════════════════════════════════════════════════════════
# primitive math — ported 1:1 from stdlib/flame/flame_math.hexa + libm externs
# ════════════════════════════════════════════════════════════════════════

# libm erf, vectorized elementwise (object-ufunc -> float64). The hexa GELU calls
# `extern fn erf` (the C libm scalar erf), so math.erf is the byte-faithful twin.
_erf_vec = np.frompyfunc(math.erf, 1, 1)


def dt_sqrt(x):
    """flame_math.hexa::dt_sqrt — Newton-Raphson 24 iters from g0=max(x,1).
    Scalar. (Distinct from clm's gn_lib _gn_sqrt: 40 iters from g0=x.)"""
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


# ════════════════════════════════════════════════════════════════════════
# .bin header + weight load — 1:1 from bytegpt_decode.hexa _bg_rd_u32 / bg_load
# ════════════════════════════════════════════════════════════════════════

def _bg_rd_u32(rb, off):
    return rb[off] | (rb[off + 1] << 8) | (rb[off + 2] << 16) | (rb[off + 3] << 24)


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
    Mirrors g_gates.hexa gen_auto_ideate dispatch (CLM\\x01 -> clm, else bytegpt)."""
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

    return {"ok": True, "vocab": vocab, "d": d, "nlay": nlay, "nh": nh, "block": block,
            "tok": tok, "pos": pos, "ln1w": ln1w, "ln1b": ln1b,
            "inW": inW, "inB": inB, "oW": oW, "oB": oB,
            "ln2w": ln2w, "ln2b": ln2b, "m0W": m0W, "m0B": m0B,
            "m2W": m2W, "m2B": m2B, "lnfw": lnfw, "lnfb": lnfb, "head": head}


# bg_load_ranged — byte-identical W-map to bg_load (hexa builds it via ranged
# read_bytes_at to dodge the whole-file boxing OOM; the resulting weights are the
# same, and the py read already mmaps lazily via frombuffer). Aliased for surface
# parity with the hexa public entries (bytegpt_decode.hexa:782).
bg_load_ranged = bg_load


# ════════════════════════════════════════════════════════════════════════
# forward — 1:1 from bytegpt_decode.hexa _bg_mha / _bg_linear / bg_forward_last_W
# ════════════════════════════════════════════════════════════════════════

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


def bg_forward_last_W(W, ids, T):
    """bytegpt_decode.hexa::bg_forward_last_W — full forward from a loaded weight
    dict; returns last-position next-byte logits float64[vocab]. ids:[T] int."""
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


# ════════════════════════════════════════════════════════════════════════
# seeded top-k temperature sampler — bytegpt_decode.hexa _g6_mix32 / _rng_next
# (xorshift32; byte-identical algorithm to clm_decode.hexa's _clmd_* PRNG)
# ════════════════════════════════════════════════════════════════════════

_MASK = 0xFFFFFFFF


def _mix32(s):
    """bytegpt_decode.hexa::_g6_mix32 — SplitMix32-style finalizer."""
    z = (s + 0x9E3779B9) & _MASK
    z = ((z ^ (z // 65536)) * 0x85EBCA6B) & _MASK
    z = ((z ^ (z // 8192)) * 0xC2B2AE35) & _MASK
    z = (z ^ (z // 65536)) & _MASK
    if z == 0:
        z = 0x9E3779B9
    return z


def _rng_next(s):
    """bytegpt_decode.hexa::_g6_rng_next — xorshift32 step -> (state, u in [0,1))."""
    x = s & _MASK
    if x == 0:
        x = 0x9E3779B9
    x = (x ^ (x * 8192)) & _MASK
    x = (x ^ (x // 131072)) & _MASK
    x = (x ^ (x * 32)) & _MASK
    return x, (float(x) / 4294967296.0)


def _topk_sample(logits, vocab, top_k, temp, rng):
    """bytegpt_decode.hexa::_g6_topk_sample — top-k by repeated argmax (ties:
    first/strict >), /temp, dt_exp softmax (max-sub), inverse-CDF draw."""
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
# public decode entries — 1:1 from bytegpt_decode.hexa
# ════════════════════════════════════════════════════════════════════════

def _seed_to_ids(seed):
    """string|bytes|list -> list[int] byte ids."""
    if isinstance(seed, (list, tuple)):
        return [int(x) for x in seed]
    if isinstance(seed, str):
        seed = seed.encode('utf-8', 'surrogateescape')
    return list(seed)


def bytegpt_decode_argmax(path, seed_ids, gen):
    """bytegpt_decode.hexa::bytegpt_decode_argmax — greedy continuation, weights
    loaded ONCE, prompt window grown (capped at block). Returns {ok,text,ids}.
    (The hexa KV-cache fast path is byte-identical to this full-forward loop.)"""
    W = bg_load(path)
    return _decode_argmax_W(W, seed_ids, gen)


# bytegpt_decode_argmax_ranged — OOM-safe twin (hexa: bg_load_ranged). Same compute.
def bytegpt_decode_argmax_ranged(path, seed_ids, gen):
    W = bg_load_ranged(path)
    return _decode_argmax_W(W, seed_ids, gen)


def _decode_argmax_W(W, seed_ids, gen):
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
    """generate gen bytes from an ALREADY-LOADED weight dict (== hexa _bg_gen_from_W
    full-forward branch). seed_ids = string|bytes|list of byte ids."""
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
# CLI — for the byte-parity harness (mirror of a hexa main calling the same)
# ════════════════════════════════════════════════════════════════════════

def _main(argv):
    if len(argv) < 2:
        print("usage: bytegpt_decode.py <cmd> ...", file=sys.stderr)
        return 2
    cmd = argv[1]
    if cmd == "header":
        print(bg_header(argv[2])); return 0
    if cmd == "logits":
        # logits <bin> <seed_csv_ids>  -> print all vocab logits at last pos
        ck = argv[2]
        ids = [int(t) for t in argv[3].split(",") if t != ""]
        lg = bytegpt_forward_last(ck, ids, len(ids))
        sys.stdout.write("LOGITS:" + ",".join("%.12e" % v for v in lg) + "\n")
        return 0
    if cmd == "argmax":
        # argmax <bin> <seed_csv_ids> <gen>
        ck = argv[2]
        ids = [int(t) for t in argv[3].split(",") if t != ""]
        gen = int(argv[4])
        r = bytegpt_decode_argmax(ck, ids, gen)
        sys.stdout.write("ARGMAX:" + ",".join(str(t) for t in r["ids"]) + "\n")
        return 0
    if cmd == "sample":
        # sample <bin> <seed_csv_ids> <gen> <top_k> <temp> <seed_rng>
        ck = argv[2]
        ids = [int(t) for t in argv[3].split(",") if t != ""]
        gen = int(argv[4]); top_k = int(argv[5]); temp = float(argv[6]); rng = int(argv[7])
        r = bytegpt_decode_topk_sampled(ck, ids, gen, top_k, temp, rng)
        sys.stdout.write("SAMPLE:" + ",".join(str(t) for t in r["ids"]) + "\n")
        return 0
    print("unknown cmd", cmd, file=sys.stderr); return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
