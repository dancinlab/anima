# T-window sweep: does a LARGER decode window let 2 concepts co-fit → recombination lift? (G1 divergent)
# ConvMoE has NO positional table → conv processes arbitrary length → T=24 is a decode-harness cap, not a
# model limit. Test composed 2-concept coverage at T in {24,48,72}. py DIRECTIONAL, aiden $0.
import sys; sys.path.insert(0,"core"); sys.path.insert(0,"cli")
import numpy as np, decode as clm, json
from g6_ideation import _g6_concepts
from evaluate import _g_coverage, _g_concept_keywords
W=clm.clm_load_weights("/home/aiden/py303_full.clm"); V=W["V"]

def decode_T(seed, gen, T, top_k=40, temp=0.7, seed_rng=7):
    seed_b=seed.encode('utf-8','surrogateescape'); slen=len(seed_b)
    tok=np.empty(T,dtype=np.float64)
    for p in range(T):
        si=slen-T+p; tok[p]=float(seed_b[si]) if si>=0 else 32.0
    out=bytearray(); rng=clm._mix32(seed_rng)
    for _ in range(gen):
        logits=clm._fwd_logits(W,tok,T)
        nb,rng=clm._topk_sample(logits[T-1],V,top_k,temp,rng)
        out.append(nb); tok[:T-1]=tok[1:]; tok[T-1]=float(nb)
    return out.decode('utf-8','surrogateescape')

cz=_g6_concepts()
# composed 2-concept seed len
comp = "if "+cz[0]+", then "+cz[1]+": "
print("composed seed len:", len(comp.encode()), "bytes; concepts:", cz[0][:20],"/",cz[1][:20])
res={}
for T in [24,48,72]:
    covs=[]; samp=""
    for sr in range(5):
        o=decode_T(comp, 40, T, seed_rng=7+sr)
        covs.append(_g_coverage(o))
        if sr==0: samp=o[:100]
    res[str(T)]={"cov":covs,"max":max(covs),"mean":round(sum(covs)/len(covs),2),"sample":samp}
    print(f"T={T}: cov={covs} max={max(covs)} mean={sum(covs)/len(covs):.2f} | {samp!r}",flush=True)
# also single-concept baseline at each T (max_single)
for T in [24,72]:
    ms=0
    for i in range(5):
        o=decode_T(cz[i]+". ",40,T,seed_rng=7+i); ms=max(ms,_g_coverage(o))
    res[f"single_T{T}"]=ms
    print(f"max_single T={T}: {ms}")
best=max(res[str(T)]["max"] for T in [24,48,72])
print("\nVERDICT:", "T-WINDOW LIFT (larger T raises composed coverage → decode-window was the cap)" if res["72"]["max"]>res["24"]["max"] else "NO T-window lift (coverage flat across T → not a window artifact)")
json.dump(res,open("/home/aiden/anima/tsweep.json","w"),indent=2)
print("=== DONE ===")
