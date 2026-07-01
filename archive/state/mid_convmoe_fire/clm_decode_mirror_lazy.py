#!/usr/bin/env python3
"""clm_decode_mirror_lazy.py — memory-bounded, vectorized variant of
clm_decode_mirror.py for LARGE (3B/7B) .clm AXIS-2 CE measurement.

Identical decode math to clm_decode_mirror.py (and CORE/clm_decode.hexa):
int4 dequant w=code*scale (float64), causal dilated conv1d, GroupNorm(1,d)+GELU
residual trunk, router conv, E expert conv+GELU, softmax MoE mix, output
GroupNorm, readout conv, T=24-pos CE vs uniform ln(V) vs reversed-target shuffle.

Two fixes vs the original so a 7B (d6208/L30/E30) forward is feasible on a
commodity host:
  1. LAZY dequant — the big int4 weight blocks (ecW/tcW/eW/rW/roW) are NOT
     materialized at load; only their (offset,cout,rest) into the file bytes is
     recorded. deq() unpacks ONE block to float64 at its use site, then it is
     freed. Peak float RAM = one block (~1GB at 7B) + the 3.5GB file bytes,
     instead of ~56GB for all weights as float64 at once.
  2. VECTORIZED int4 unpack — numpy bit ops over the packed byte array, not a
     per-code Python while-loop (which is O(billions) of iterations at 7B).

Byte-identical arithmetic to the original (same float64 dequant, same matmul),
so the CE it reports matches clm_decode_mirror.py on any model both can run.
"""
import sys, struct, math
import numpy as np

def ru32(b, o): return b[o] | (b[o+1]<<8) | (b[o+2]<<16) | (b[o+3]<<24)
def f32(b, o): return struct.unpack_from("<f", b, o)[0]

def scan_block(rb, off):
    """Record a weight block's location WITHOUT materializing it. Returns
    (handle, new_off). handle carries the file offset of the packed codes."""
    cout = ru32(rb, off); off += 4
    rest = ru32(rb, off); off += 4
    n = cout * rest
    nb = (n + 1)//2                 # ceil(n/2) packed bytes (2 codes/byte)
    blk = {"off": off, "cout": cout, "rest": rest, "n": n, "nb": nb}
    off += nb + 4*cout              # skip packed codes + cout float32 scales
    return blk, off

def deq(rb, blk):
    """Dequantize ONE int4 block to a (cout, rest) float64 weight, on demand."""
    off, cout, rest, n, nb = blk["off"], blk["cout"], blk["rest"], blk["n"], blk["nb"]
    raw = np.frombuffer(rb, dtype=np.uint8, count=nb, offset=off)
    codes = np.empty(nb*2, dtype=np.float64)
    codes[0::2] = (raw & 0xF).astype(np.float64) - 8.0          # low nibble  -> even idx
    codes[1::2] = ((raw >> 4) & 0xF).astype(np.float64) - 8.0   # high nibble -> odd idx
    codes = codes[:n].reshape(cout, rest)
    scales = np.frombuffer(rb, dtype="<f4", count=cout, offset=off + nb).astype(np.float64)
    return codes * scales[:, None]                              # per-row (cout) scale

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
    off = 5; bi = 0; E=2; V=256
    while bi < nblk:
        c = ru32(rb, off); r = ru32(rb, off+4)
        if bi == nblk-2: E = c
        if bi == nblk-1: V = c
        off += 8 + (c*r+1)//2 + c*4
        bi += 1
    L = nblk - E - 3
    off = 5
    ecW, off = scan_block(rb, off)
    tcW = []
    for _ in range(L):
        w, off = scan_block(rb, off); tcW.append(w)
    eW = []
    for _ in range(E):
        w, off = scan_block(rb, off); eW.append(w)
    rW, off = scan_block(rb, off)
    roW, off = scan_block(rb, off)
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
    tgG=[]
    for _ in range(L): a, off = load_ext(rb, off); tgG.append(a)
    tgB=[]
    for _ in range(L): a, off = load_ext(rb, off); tgB.append(a)
    noG, off = load_ext(rb, off)
    noB, off = load_ext(rb, off)
    return dict(rb=rb,d=d,E=E,V=V,K=K,L=L,ecW=ecW,tcW=tcW,eW=eW,rW=rW,roW=roW,
                embed=embed.reshape(V,d),ecB=ecB,tcB=tcB,eB=eB,rB=rB,roB=roB,
                tgG=tgG,tgB=tgB,noG=noG,noB=noB)

def gelu(x):
    inner = 0.7978845608 * (x + 0.044715 * x*x*x)
    a = np.clip(inner, -15.0, 15.0)
    e2 = np.exp(2.0*a)
    return 0.5 * x * (1.0 + (e2-1.0)/(e2+1.0))

def conv1d(x, w2d, b, T, Cin, Cout, K, dil):
    Kdim = Cin*K
    xcol = np.zeros((T, Kdim))
    for t in range(T):
        for ci in range(Cin):
            for k in range(K):
                p = t - dil*(K-1-k)
                if p >= 0: xcol[t, ci*K+k] = x[p, ci]
    y = xcol @ w2d.T + b[None, :]
    return y

def groupnorm1(x, g, b, T, d):
    mu = x.mean(axis=1, keepdims=True)
    var = x.var(axis=1, keepdims=True)
    xn = (x - mu)/np.sqrt(var + 1e-5)
    return xn*g[None,:] + b[None,:]

def fwd_logits(W, tok, T):
    rb = W["rb"]
    d,E,V,K,L = W["d"],W["E"],W["V"],W["K"],W["L"]
    xe = W["embed"][tok.astype(int)]                  # (T,d)
    xt = conv1d(xe, deq(rb, W["ecW"]), W["ecB"], T, d, d, K, 1)
    dil = 1
    for li in range(L):
        dil_eff = min(dil, 512)
        h = conv1d(xt, deq(rb, W["tcW"][li]), W["tcB"][li], T, d, d, K, dil_eff)
        hn = groupnorm1(h, W["tgG"][li], W["tgB"][li], T, d)
        hg = gelu(hn)
        xt = xt + hg
        dil *= 2
    logits_r = conv1d(xt, deq(rb, W["rW"]), W["rB"], T, d, E, 1, 1)   # (T,E)
    ex_out = []
    for ej in range(E):
        eo = conv1d(xt, deq(rb, W["eW"][ej]), W["eB"][ej], T, d, d, K, 1)
        ex_out.append(gelu(eo))
    probs = np.exp(logits_r - logits_r.max(axis=1, keepdims=True))
    probs = probs / probs.sum(axis=1, keepdims=True)        # (T,E)
    y = np.zeros((T, d))
    for ej in range(E):
        y += probs[:, ej:ej+1] * ex_out[ej]
    yn = groupnorm1(y, W["noG"], W["noB"], T, d)
    out = conv1d(yn, deq(rb, W["roW"]), W["roB"], T, d, V, 1, 1)      # (T,V)
    return out

def ce_nextbyte(logits, seq, T, V):
    tot = 0.0; np_ = 0
    for p in range(T-1):
        tgt = int(seq[p+1])
        z = logits[p] - logits[p].max()
        lse = math.log(np.exp(z).sum())
        tot += -(z[tgt] - lse)
        np_ += 1
    return tot/np_, np_

def ce_allpos(logits, tgt, T, V):
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
    print(f"CLM_CONFIG d={W['d']} L={W['L']} E={W['E']} K={W['K']} V={V}", flush=True)
    if corpus is None:
        seq  = [84,104,101,32,109,105,110,100,32,105,115,32,97,32,102,105,114,101,32,116,111,32,98,101]
        ctrl = [105,32,98,105,100,102,101,32,110,116,32,114,32,84,105,32,32,101,101,104,111,97,109,115]
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
