#!/usr/bin/env python3
"""clm_gen.py — greedy byte-generation from a v0.3 .clm via the validated lazy
mirror forward (clm_decode_mirror_lazy). Bypasses the hexa engine's v0.2-only
generation gate (clm_decodable) so a v0.3 7B .clm CAN generate — same int4
dequant + CLMConvMoE forward the CE mirror uses (validated == 3B 2.26360).

Two changes vs clm_decode_mirror_lazy.py:
  1. conv1d im2col VECTORIZED (numpy strided assign over K, not a per-(t,ci,k)
     Python triple-loop) — math identical, ~100x faster so autoregressive
     generation is feasible.
  2. greedy generate(): prompt bytes -> argmax next-byte -> append -> repeat.

Usage: python3 clm_gen.py <clm> "<prompt>" [n_new] [ctx_T]
"""
import sys, struct, math
import numpy as np

def ru32(b, o): return b[o] | (b[o+1]<<8) | (b[o+2]<<16) | (b[o+3]<<24)

def scan_block(rb, off):
    cout = ru32(rb, off); off += 4
    rest = ru32(rb, off); off += 4
    n = cout * rest
    nb = (n + 1)//2
    blk = {"off": off, "cout": cout, "rest": rest, "n": n, "nb": nb}
    off += nb + 4*cout
    return blk, off

def deq(rb, blk):
    off, cout, rest, n, nb = blk["off"], blk["cout"], blk["rest"], blk["n"], blk["nb"]
    raw = np.frombuffer(rb, dtype=np.uint8, count=nb, offset=off)
    codes = np.empty(nb*2, dtype=np.float64)
    codes[0::2] = (raw & 0xF).astype(np.float64) - 8.0
    codes[1::2] = ((raw >> 4) & 0xF).astype(np.float64) - 8.0
    codes = codes[:n].reshape(cout, rest)
    scales = np.frombuffer(rb, dtype="<f4", count=cout, offset=off + nb).astype(np.float64)
    return codes * scales[:, None]

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
    off += 5
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
    # VECTORIZED causal dilated conv im2col. col j = ci*K + k; causal left-pad.
    # xcol[t, ci*K+k] = x[t - dil*(K-1-k), ci]  (0 if index < 0).
    xcol = np.zeros((T, Cin*K))
    for k in range(K):
        shift = dil*(K-1-k)
        if shift < T:
            xcol[shift:, k::K] = x[:T-shift, :]   # all ci at column offset k
    return xcol @ w2d.T + b[None, :]

def groupnorm1(x, g, b, T, d):
    mu = x.mean(axis=1, keepdims=True)
    var = x.var(axis=1, keepdims=True)
    xn = (x - mu)/np.sqrt(var + 1e-5)
    return xn*g[None,:] + b[None,:]

def fwd_logits(W, tok, T):
    rb = W["rb"]
    d,E,V,K,L = W["d"],W["E"],W["V"],W["K"],W["L"]
    xe = W["embed"][tok.astype(int)]
    xt = conv1d(xe, deq(rb, W["ecW"]), W["ecB"], T, d, d, K, 1)
    dil = 1
    for li in range(L):
        dil_eff = min(dil, 512)
        h = conv1d(xt, deq(rb, W["tcW"][li]), W["tcB"][li], T, d, d, K, dil_eff)
        hn = groupnorm1(h, W["tgG"][li], W["tgB"][li], T, d)
        hg = gelu(hn)
        xt = xt + hg
        dil *= 2
    logits_r = conv1d(xt, deq(rb, W["rW"]), W["rB"], T, d, E, 1, 1)
    ex_out = []
    for ej in range(E):
        eo = conv1d(xt, deq(rb, W["eW"][ej]), W["eB"][ej], T, d, d, K, 1)
        ex_out.append(gelu(eo))
    probs = np.exp(logits_r - logits_r.max(axis=1, keepdims=True))
    probs = probs / probs.sum(axis=1, keepdims=True)
    y = np.zeros((T, d))
    for ej in range(E):
        y += probs[:, ej:ej+1] * ex_out[ej]
    yn = groupnorm1(y, W["noG"], W["noB"], T, d)
    out = conv1d(yn, deq(rb, W["roW"]), W["roB"], T, d, V, 1, 1)
    return out

def ce_nextbyte(logits, seq, T):
    tot = 0.0; n = 0
    for p in range(T-1):
        z = logits[p] - logits[p].max()
        lse = math.log(np.exp(z).sum())
        tot += -(z[int(seq[p+1])] - lse); n += 1
    return tot/n

def generate(W, prompt, n_new, ctxT):
    seq = list(prompt)
    for _ in range(n_new):
        ctx = seq[-ctxT:] if len(seq) >= ctxT else seq
        logits = fwd_logits(W, np.array(ctx, dtype=float), len(ctx))
        seq.append(int(np.argmax(logits[-1])))
    return bytes(seq)

def main():
    path = sys.argv[1]
    prompt = sys.argv[2].encode("utf-8") if len(sys.argv) > 2 else b"The mind is"
    n_new = int(sys.argv[3]) if len(sys.argv) > 3 else 48
    ctxT = int(sys.argv[4]) if len(sys.argv) > 4 else 24
    W = load_clm(path)
    print(f"CLM_CONFIG d={W['d']} L={W['L']} E={W['E']} K={W['K']} V={W['V']}", flush=True)
    # validation hook: if no prompt-gen wanted, the CE probe-seq still matches the
    # CE mirror — run it so the vectorized conv1d is proven == the looped one.
    vs = [84,104,101,32,109,105,110,100,32,105,115,32,97,32,102,105,114,101,32,116,111,32,98,101]
    vl = fwd_logits(W, np.array(vs, dtype=float), 24)
    print(f"VALIDATE CE_realtext = {ce_nextbyte(vl, vs, 24):.5f}  (3B golden = 2.26360; 7B = 1.90741)", flush=True)
    out = generate(W, prompt, n_new, ctxT)
    cont = out[len(prompt):]
    print(f"PROMPT  : {prompt!r}")
    print(f"GEN_RAW : {cont!r}")
    try:
        print(f"GEN_TEXT: {prompt.decode('utf-8','replace')}{cont.decode('utf-8','replace')}")
    except Exception as e:
        print(f"GEN_TEXT: <decode err {e}>")

if __name__ == "__main__":
    main()
