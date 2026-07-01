#!/usr/bin/env python3
"""clm_decode_mirror.py — FAITHFUL pure-numpy mirror of CORE/clm_decode.hexa's
decode forward + clm_forward_ce, for AXIS-2 CE measurement WHEN the local hexa
runtime can't link the forge fused native (`forge_dispatch_groupnorm_gelu`).

This re-implements EXACTLY clm_decode.hexa::_clmd_load + _clmd_fwd_logits +
clm_forward_ce (same int4 dequant w=code*scale, same causal dilated conv1d,
GroupNorm(1,d)+GELU residual trunk, router conv, E expert conv+GELU, softmax MoE
mix, output GroupNorm, readout conv, T=24-pos CE vs uniform ln(V) vs reversed-
target shuffle). DETERMINISTIC (pure arithmetic over fixed file bytes, no RNG).

It reads the .clm BYTES (the serialized int4 artifact) — NOT the torch ckpt — so
it genuinely proves the SERIALIZED .clm decodes to descent. Honest label: this is
a PYTHON MIRROR of the hexa engine decode, used because the canonical hexa
engine-mount is BLOCKED by a local toolchain link-gap (not an artifact problem).
"""
import sys, struct, math
import numpy as np

def ru32(b, o): return b[o] | (b[o+1]<<8) | (b[o+2]<<16) | (b[o+3]<<24)
def f32(b, o): return struct.unpack_from("<f", b, o)[0]

def load_block(rb, off):
    cout = ru32(rb, off); off += 4
    rest = ru32(rb, off); off += 4
    n = cout * rest
    codes = np.zeros(n, dtype=np.float64)
    i = 0
    while i < n:
        byte = rb[off]; off += 1
        codes[i] = (byte & 0xF) - 8
        if i+1 < n: codes[i+1] = ((byte >> 4) & 0xF) - 8
        i += 2
    w = np.zeros(n, dtype=np.float64)
    for co in range(cout):
        s = f32(rb, off); off += 4
        w[co*rest:(co+1)*rest] = codes[co*rest:(co+1)*rest] * s
    return w.reshape(cout, rest), off

def load_ext(rb, off):
    n = ru32(rb, off); off += 4
    arr = np.frombuffer(rb, dtype="<f4", count=n, offset=off).astype(np.float64)
    off += 4*n
    return arr, off

def load_clm(path):
    rb = open(path, "rb").read()
    assert rb[0]==67 and rb[1]==76 and rb[2]==77 and rb[3]==1, "bad magic"
    nblk = rb[4]
    d = ru32(rb, 5); rest0 = ru32(rb, 9); K = rest0 // d
    # walk headers for E,V
    off = 5; bi = 0; E=2; V=256
    while bi < nblk:
        c = ru32(rb, off); r = ru32(rb, off+4)
        if bi == nblk-2: E = c
        if bi == nblk-1: V = c
        off += 8 + (c*r+1)//2 + c*4
        bi += 1
    L = nblk - E - 3
    off = 5
    ecW, off = load_block(rb, off)
    tcW = []
    for _ in range(L):
        w, off = load_block(rb, off); tcW.append(w)
    eW = []
    for _ in range(E):
        w, off = load_block(rb, off); eW.append(w)
    rW, off = load_block(rb, off)
    roW, off = load_block(rb, off)
    assert rb[off]==67 and rb[off+1]==76 and rb[off+2]==77 and rb[off+3]==88, "no CLMX"
    off += 5  # skip CLMX + n_ext
    embed, off = load_ext(rb, off)
    ecB, off = load_ext(rb, off)
    tcB = []
    for _ in range(L): a, off = load_ext(rb, off); tcB.append(a)
    eB = []
    for _ in range(E): a, off = load_ext(rb, off); eB.append(a)
    rB, off = load_ext(rb, off)
    roB, off = load_ext(rb, off)
    tgG=[];
    for _ in range(L): a, off = load_ext(rb, off); tgG.append(a)
    tgB=[]
    for _ in range(L): a, off = load_ext(rb, off); tgB.append(a)
    noG, off = load_ext(rb, off)
    noB, off = load_ext(rb, off)
    return dict(d=d,E=E,V=V,K=K,L=L,ecW=ecW,tcW=tcW,eW=eW,rW=rW,roW=roW,
                embed=embed.reshape(V,d),ecB=ecB,tcB=tcB,eB=eB,rB=rB,roB=roB,
                tgG=tgG,tgB=tgB,noG=noG,noB=noB)

def gelu(x):
    # EXACT match to generator.hexa::_gen_gelu — tanh approximation with clamp:
    #   inner = 0.7978845608*(x + 0.044715*x^3); a = clamp(inner, -15, 15)
    #   e2 = exp(2a);  0.5*x*(1 + (e2-1)/(e2+1))
    inner = 0.7978845608 * (x + 0.044715 * x*x*x)
    a = np.clip(inner, -15.0, 15.0)
    e2 = np.exp(2.0*a)
    return 0.5 * x * (1.0 + (e2-1.0)/(e2+1.0))

def conv1d(x, w2d, b, T, Cin, Cout, K, dil):
    # x: (T, Cin); w2d: (Cout, Cin*K) with col j = ci*K + k; causal left-pad.
    Kdim = Cin*K
    xcol = np.zeros((T, Kdim))
    for t in range(T):
        for ci in range(Cin):
            for k in range(K):
                p = t - dil*(K-1-k)
                if p >= 0: xcol[t, ci*K+k] = x[p, ci]
    y = xcol @ w2d.T + b[None, :]   # (T, Cout)
    return y

def groupnorm1(x, g, b, T, d):
    # GroupNorm(1, d): normalize over the d channels per (t) position.
    mu = x.mean(axis=1, keepdims=True)
    var = x.var(axis=1, keepdims=True)
    xn = (x - mu)/np.sqrt(var + 1e-5)
    return xn*g[None,:] + b[None,:]

def fwd_logits(W, tok, T):
    d,E,V,K,L = W["d"],W["E"],W["V"],W["K"],W["L"]
    xe = W["embed"][tok.astype(int)]                  # (T,d)
    xt = conv1d(xe, W["ecW"], W["ecB"], T, d, d, K, 1)
    dil = 1
    for li in range(L):
        dil_eff = min(dil, 512)
        h = conv1d(xt, W["tcW"][li], W["tcB"][li], T, d, d, K, dil_eff)
        hn = groupnorm1(h, W["tgG"][li], W["tgB"][li], T, d)
        hg = gelu(hn)
        xt = xt + hg
        dil *= 2
    logits_r = conv1d(xt, W["rW"], W["rB"], T, d, E, 1, 1)   # (T,E)
    ex_out = []
    for ej in range(E):
        eo = conv1d(xt, W["eW"][ej], W["eB"][ej], T, d, d, K, 1)
        ex_out.append(gelu(eo))
    # softmax MoE router mix (nn_moe_router_fwd): probs over E, weighted sum
    probs = np.exp(logits_r - logits_r.max(axis=1, keepdims=True))
    probs = probs / probs.sum(axis=1, keepdims=True)        # (T,E)
    y = np.zeros((T, d))
    for ej in range(E):
        y += probs[:, ej:ej+1] * ex_out[ej]
    yn = groupnorm1(y, W["noG"], W["noB"], T, d)
    out = conv1d(yn, W["roW"], W["roB"], T, d, V, 1, 1)      # (T,V)
    return out

def ce_nextbyte(logits, seq, T, V):
    # EXACT match to generator.hexa::clm_decode_ce — position p in [0, T-1)
    # predicts seq[p+1]; mean over T-1 positions.
    tot = 0.0; np_ = 0
    for p in range(T-1):
        tgt = int(seq[p+1])
        z = logits[p] - logits[p].max()
        lse = math.log(np.exp(z).sum())
        tot += -(z[tgt] - lse)
        np_ += 1
    return tot/np_, np_

def ce_allpos(logits, tgt, T, V):
    # corpus-mode CE over all T positions vs an explicit target vector.
    tot = 0.0
    for t in range(T):
        z = logits[t] - logits[t].max()
        lse = math.log(np.exp(z).sum())
        tot += -(z[int(tgt[t])] - lse)
    return tot / T

def main():
    path = sys.argv[1]
    corpus = sys.argv[2] if len(sys.argv) > 2 else None
    nwin = int(sys.argv[3]) if len(sys.argv) > 3 else 64
    W = load_clm(path)
    V = W["V"]; T = 24
    # Default in-distribution real-text window + shuffled control == the exact
    # sequences CORE/clm_ce_descent_probe.hexa uses ("The mind is a fire to be").
    if corpus is None:
        seq  = [84,104,101,32,109,105,110,100,32,105,115,32,97,32,102,105,114,101,32,116,111,32,98,101]
        ctrl = [105,32,98,105,100,102,101,32,110,116,32,114,32,84,105,32,32,101,101,104,111,97,109,115]
        # EXACT engine semantics: the T-byte seq is BOTH the token window and the
        # next-byte target (position p predicts seq[p+1]); 23 scored positions.
        logits = fwd_logits(W, np.array(seq, dtype=float), T)
        ce_real, _ = ce_nextbyte(logits, seq, T, V)
        logits_c = fwd_logits(W, np.array(ctrl, dtype=float), T)
        ce_ctrl, _ = ce_nextbyte(logits_c, ctrl, T, V)
        uniform = math.log(V)
        print(f"MIRROR_MODE=probe-seq")
        print(f"CE_realtext        = {ce_real:.5f}")
        print(f"CE_shuffled_ctrl   = {ce_ctrl:.5f}")
        print(f"CE_uniform_baseline= {uniform:.5f}")
        print(f"CE_BELOW_UNIFORM   = {1 if ce_real < uniform else 0}")
        print(f"CE_BEATS_SHUFFLE   = {1 if ce_real < ce_ctrl else 0}")
        green = ce_real < uniform and ce_real < ce_ctrl
        print(f"VERDICT = {'GREEN' if green else 'NO-DESCENT'} (CORE_3AXIS AXIS-2 gate: CE_real<uniform AND CE_real<shuffle)")
        return
    # corpus mode: mirror clm_forward_ce over nwin windows of a byte corpus
    rb = open(corpus, "rb").read()
    n = len(rb)
    stride = max(1, (n - T - 1)//nwin)
    sm=ss=0.0; cnt=0
    for s in range(nwin):
        base = s*stride
        if base+T+1 <= n:
            tok = np.frombuffer(rb, dtype=np.uint8, count=T, offset=base).astype(float)
            tgt = np.frombuffer(rb, dtype=np.uint8, count=T, offset=base+1).astype(float)
            logits = fwd_logits(W, tok, T)
            sm += ce_allpos(logits, tgt, T, V)
            tgt_sh = tgt[::-1].copy()
            ss += ce_allpos(logits, tgt_sh, T, V)
            cnt += 1
    mce=sm/cnt; sce=ss/cnt; uni=math.log(V)
    print(f"MIRROR_MODE=corpus windows={cnt}")
    print(f"CE_realtext(corpus)= {mce:.5f}")
    print(f"CE_shuffle(reverse)= {sce:.5f}")
    print(f"CE_uniform_lnV     = {uni:.5f}")
    print(f"CE_BELOW_UNIFORM   = {1 if mce<uni else 0}")
    print(f"CE_BEATS_SHUFFLE   = {1 if mce<sce else 0}")
    print(f"VERDICT = {'GREEN' if (mce<uni and mce<sce) else 'NO-DESCENT'}")

if __name__ == "__main__":
    main()
