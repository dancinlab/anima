#!/usr/bin/env python3
"""CPU-LOCAL re-score of already-captured Lane A tensors (raw.npz). a_akida_native_train permits CPU re-analysis
of captured tensors (NOT new chip claims). Corroborates PROBE 1 (encoding) + PROBE 3 (timing) on the EXACT
forward outputs that produced the original closed-negative, plus re-derives the random-encoder baseline margin.
raw.npz keys: par_fwd(25,32) con_fwd(25,32) par_post con_post backbone(256,256) init_w."""
import numpy as np, json, struct, sys

d = np.load("/tmp/lanea_pull/raw.npz")
par_fwd = d["par_fwd"]   # 25×32 post-1bit-Hebbian forward of the parallel (concept-major) arm, RANDOM encoder
backbone = d["backbone"] # the fixed random int4 256×256 encoder that all falsifiers sit downstream of
N_LANGS = 5
LIMEN = "/tmp/lanea_pull/parallel.limen"

def read_limen(path):
    blob=open(path,"rb").read(); off=8
    struct.unpack_from("<I",blob,off)[0]; off+=4
    count=struct.unpack_from("<I",blob,off)[0]; off+=4
    recs=[]
    for _ in range(count):
        rlen=struct.unpack_from("<I",blob,off)[0]; off+=4
        rec=blob[off:off+rlen]; off+=rlen
        hlen=struct.unpack_from("<I",rec,0)[0]
        head=json.loads(rec[4:4+hlen].decode()); recs.append((head,rec[4+hlen:]))
    return count,recs
count, recs = read_limen(LIMEN)
H = np.stack([np.bincount(np.frombuffer(p,dtype=np.uint8), minlength=256).astype(np.float64) for (_,p) in recs])  # 25×256

def margin_binary(fb):
    n=fb.shape[0]; c=np.array([r//N_LANGS for r in range(n)]); w,b=[],[]
    for i in range(n):
        for j in range(i+1,n):
            dd=int(np.count_nonzero(fb[i]!=fb[j])); (w if c[i]==c[j] else b).append(dd)
    return float(np.mean(b))-float(np.mean(w))
def margin_post1bit(out2d):
    fb=(out2d>np.median(out2d,axis=0,keepdims=True)).astype(np.uint8); return margin_binary(fb)

# ---- (A) baseline: re-score the captured RANDOM-encoder forward (reproduce closed-negative margin) ----
base_margin = margin_post1bit(par_fwd)
print("[cpu] captured RANDOM-encoder par_fwd post-1bit concept margin = %.4f bits (the closed-negative baseline)" % base_margin)

# ---- (B) PROBE 1 corroboration: structured encoders on the SAME histograms, deterministic (no chip) ----
# This is a CPU re-encode of the captured input space — it CANNOT make a chip claim, but it shows whether a
# STRUCTURED projection changes the *encoded input* concept separability that the chip would then learn from.
def encode_margin(P):
    proj = H.astype(np.int32) @ P.T
    fb = (proj > np.median(proj,axis=1,keepdims=True)).astype(np.uint8)
    return margin_binary(fb)
m_random_enc = encode_margin(backbone.astype(np.int32))   # the actual fixed random encoder
Hc = H - H.mean(0,keepdims=True)
U,S,Vt = np.linalg.svd(Hc, full_matrices=False)
Psvd = np.zeros((256,256)); Psvd[:Vt.shape[0]] = Vt
Psvd = np.clip(np.round(Psvd*(7.0/(np.abs(Psvd).max()+1e-12))),-7,7).astype(np.int32)
m_svd_enc = encode_margin(Psvd)
cov = (Hc.T@Hc)/max(1,Hc.shape[0]-1) + 1.0*np.eye(256)   # ridge so eigvals are well-conditioned
w,V = np.linalg.eigh(cov); w=np.maximum(w,1e-6); Wm = V@np.diag(1.0/np.sqrt(w))@V.T
Pwh = np.clip(np.round(Wm*(7.0/(np.abs(Wm).max()+1e-12))),-7,7).astype(np.int32)
m_wh_enc = encode_margin(Pwh)
print("[cpu] ENCODED-INPUT concept margin (pre-chip): random=%.4f svd=%.4f whitened=%.4f" % (m_random_enc, m_svd_enc, m_wh_enc))
print("[cpu]   structured-vs-random encoded-input lift: svd=%+.4f whitened=%+.4f" % (m_svd_enc-m_random_enc, m_wh_enc-m_random_enc))

# ---- (C) PROBE 3 corroboration: timing-proxy on the captured RANDOM-encoder forward ----
def rankdata(a):
    order=np.argsort(a,kind="mergesort"); r=np.empty(len(a)); r[order]=np.arange(1,len(a)+1)
    s=a[order]; i=0
    while i<len(a):
        j=i
        while j+1<len(a) and s[j+1]==s[i]: j+=1
        if j>i:
            avg=(r[order[i]]+r[order[j]])/2
            for k in range(i,j+1): r[order[k]]=avg
        i=j+1
    return r
def timing_margin(out2d):
    R=np.stack([rankdata(out2d[i]) for i in range(out2d.shape[0])]); n=R.shape[0]
    c=np.array([r//N_LANGS for r in range(n)])
    def sp(a,b):
        ra,rb=a-a.mean(),b-b.mean(); dn=np.linalg.norm(ra)*np.linalg.norm(rb)
        return 0.0 if dn==0 else float(ra@rb/dn)
    w,b=[],[]
    for i in range(n):
        for j in range(i+1,n):
            (w if c[i]==c[j] else b).append(sp(R[i],R[j]))
    return float(np.mean(w))-float(np.mean(b))
tm = timing_margin(par_fwd)
print("[cpu] PROBE3 timing-proxy (within-minus-between concept rank-corr) on captured RANDOM par_fwd = %+.4f" % tm)
print("[cpu]   (>0 => concept structure in per-unit rank/timing order even where rate-Hamming margin = %.4f)" % base_margin)

out = {"source":"raw.npz captured tensors (CPU re-score, no chip claim)",
       "baseline_random_post1bit_margin_bits": base_margin,
       "encoded_input_margin": {"random": m_random_enc, "svd": m_svd_enc, "whitened": m_wh_enc,
                                "svd_minus_random": m_svd_enc-m_random_enc, "whitened_minus_random": m_wh_enc-m_random_enc},
       "timing_proxy_margin_on_captured_random_fwd": tm}
json.dump(out, open("/tmp/lanea_pull/cpu_rescore_result.json","w"), indent=2)
print("[cpu] wrote /tmp/lanea_pull/cpu_rescore_result.json")
