#!/usr/bin/env python3
# Enriched VAdaptField (numpy DIRECTIONAL): distributed population-code + KEY-LOCKED conjunction.
# Fair test of owner's pop+conj: additive(baseline) vs conj_hrr(circular-conv=key-locked bind).
# DECODER-FREE, H_9025 shuffle-EARNED + DECISIVE held-out gate. HRR is a FIXED op (no per-pair
# training) so held-out==train by construction -> tests whether key-locked bind over an enriched
# distributed code passes held-out recoverability (VSA), then the honest recover!=capability caveat.
import sys
import numpy as np
D=48; K=64; N_CONCEPT=34; N_PAIRS=500; TAU=1.5; SPLIT_THRESH=0.30; RECOVER_THRESH=0.30; HELDOUT_FRAC=0.4
SEED=int(sys.argv[1]) if len(sys.argv)>1 else 7
def unit(v):
    n=np.linalg.norm(v,axis=-1,keepdims=True); return v/np.where(n==0,1,n)
def popcode(Dict,x):
    z=Dict@x/TAU; z=z-z.max(); e=np.exp(z); p=e/e.sum(); return p-p.mean()  # zero-mean distributed
def cconv(a,b): return np.real(np.fft.ifft(np.fft.fft(a)*np.fft.fft(b)))
def ccorr(c,k): return np.real(np.fft.ifft(np.fft.fft(c)*np.conj(np.fft.fft(k))))
def bdist(a,b): return 1.0-float(unit(a)@unit(b))
def earned(rr,rw,tgt):
    return (float(unit(rr)@unit(tgt))>RECOVER_THRESH) and (float(unit(rw)@unit(tgt))<=RECOVER_THRESH)
def run(SEED):
    rng=np.random.default_rng(SEED)
    Dict=unit(rng.standard_normal((K,D)))
    Aset=unit(rng.standard_normal((N_CONCEPT,D))); Bset=unit(rng.standard_normal((N_CONCEPT,D)))
    pA=np.stack([popcode(Dict,a) for a in Aset]); pB=np.stack([popcode(Dict,b) for b in Bset])
    spars=float(np.mean(np.sum(np.abs(pA)>0.5*np.abs(pA).max(1,keepdims=True),1)))  # rough active-cell count
    pairs=list(dict.fromkeys((int(rng.integers(N_CONCEPT)),int(rng.integers(N_CONCEPT))) for _ in range(N_PAIRS)))
    n=len(pairs); nh=int(n*HELDOUT_FRAC); train=pairs[nh:]; held=pairs[:nh]
    def compose(arm,i,j):
        return pA[i]+pB[j] if arm=="additive" else cconv(pA[i],pB[j])
    def recB(arm,c,i):
        return c-pA[i]*(c@unit(pA[i])) if arm=="additive" else ccorr(c,pA[i])
    rows=[]
    for arm in ["additive","conj_hrr"]:
        for split,pl in (("train",train),("HELDOUT",held)):
            dok=ea=ab=0; m=len(pl)
            for (i,j) in pl:
                c=compose(arm,i,j); tgt=pB[j]
                if bdist(c,pA[i])>SPLIT_THRESH and bdist(c,pB[j])>SPLIT_THRESH: dok+=1
                wi=(i+7)%N_CONCEPT
                if earned(recB(arm,c,i),recB(arm,c,wi),tgt): ea+=1
                cab=pA[i]+pB[j]
                if earned(cab-pA[i]*(cab@unit(pA[i])), cab-pA[wi]*(cab@unit(pA[wi])), tgt): ab+=1
            rows.append((arm,split,f"{dok}/{m}",f"{ea}/{m}",f"{ab}/{m}"))
    return rows,len(train),len(held),spars
rows,ntr,nho,spars=run(SEED)
print(f"SEED={SEED} D={D} K={K} train={ntr} HELDOUT={nho} tau={TAU} ~active_cells/code={spars:.1f}")
print(f"{'arm':<12}{'split':<10}{'M1 distinct':<13}{'M2 EARNED':<12}{'ablate_earned'}")
for (arm,sp,d,e,a) in rows:
    mark="  <-DECISIVE" if sp=="HELDOUT" else ""
    print(f"{arm:<12}{sp:<10}{d:<13}{e:<12}{a}{mark}")
print()
print("READ(c9): conj_hrr = key-locked bind over distributed pop-code. If HELDOUT M2-EARNED>0")
print("=> enriched field passes held-out RECOVERABILITY where additive floors. BUT recover=VSA")
print("storage property; Rung1(H_9026) showed trained bind on REAL manifold still floors the")
print("recomb TASK (0/5). recoverability != anima capability. numpy DIRECTIONAL.")
