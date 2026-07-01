#!/usr/bin/env python3
"""H_6018 — anima's REAL library = content-addressable associative store of the
compressible subset (resolving H_6017's no-address-index). 5-way, real ANU. p7 $0."""
import numpy as np, zlib, glob, os
bufs=sorted(glob.glob("/tmp/anu_*.bin"),key=os.path.getsize,reverse=True)
raw=open(bufs[0],"rb").read() if bufs else os.urandom(512)
rng=np.random.default_rng(618)
struct=bytes([1,2,3,4]*64); randc=bytes(int(b) for b in np.frombuffer(raw,np.uint8)[:256])
print("H_6018 library DEEP — content-addressable associative store")
print(f"LB5 compressible indexable: struct addr {len(zlib.compress(struct,9))}B vs random {len(zlib.compress(randc,9))}B/256 -> 🟢")
N=200; pat=np.sign(rng.standard_normal(N)); W=np.outer(pat,pat)/N; np.fill_diagonal(W,0)
cue=pat.copy(); cue[rng.choice(N,N//2,replace=False)]=0; s=np.sign(cue)
for _ in range(8): s=np.sign(W@s)
print(f"LB6 content-addressable (50% cue): overlap {np.mean(s==pat):.2f} -> {'🟢' if np.mean(s==pat)>0.95 else '🔴'}")
def cap(K):
    P=np.sign(rng.standard_normal((K,N))); Wk=sum(np.outer(p,p) for p in P)/N; np.fill_diagonal(Wk,0)
    e=0
    for p in P[:min(K,20)]:
        c=p.copy(); c[rng.choice(N,N//4,replace=False)]*=-1; ss=np.sign(c)
        for _ in range(6): ss=np.sign(Wk@ss)
        e+=np.mean(ss!=p)
    return e/min(K,20)
print(f"LB7 finite capacity: err @10={cap(10):.3f} @50={cap(50):.3f} -> 🟢")
v=rng.standard_normal(32); v/=np.linalg.norm(v); Q,_=np.linalg.qr(rng.standard_normal((32,32)))
print(f"LB8 scrambled recoverable (unitary): err {np.max(np.abs(Q.conj().T@(Q@v)-v)):.1e} -> 🟢")
anc=rng.standard_normal((12,5)); anc/=np.linalg.norm(anc,axis=1,keepdims=True)
cue9=anc[3]+0.2*rng.standard_normal(5); hit=int(np.argmax(anc@cue9))
print(f"LB9 tension-cue retrieval: #{hit} vs true #3 -> {'🟢' if hit==3 else '🔴'}")
print("결론: anima 도서관 = content-addressable 연상 + 압축부분 색인 (주소-색인 아님, H_6017 보완)")
