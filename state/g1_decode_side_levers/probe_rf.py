# Real-model receptive-field probe (G1 divergent, 2026-07-02). ConvMoE K=3 L=4 → RF=L(K-1)+1=9?
# Measure effective RF: perturb byte at distance-from-end d, measure ||Δ next-token logits||.
# RF = max d with nonzero influence. If RF≈9 ≪ concept-pair span(~60b) → recombination architecturally
# impossible (two concepts never co-visible). py mirror DIRECTIONAL, aiden $0.
import sys; sys.path.insert(0,"core"); sys.path.insert(0,"cli")
import numpy as np, decode as clm, json
W = clm.clm_load_weights("/home/aiden/py303_full.clm")
V=W["V"]; T=24
rng=np.random.default_rng(7)
NCTX=8
infl=np.zeros(T)  # influence by position index (0=oldest, T-1=newest)
for _ in range(NCTX):
    base=rng.integers(65,122,size=T).astype(np.float64)  # random ascii letters
    l0=clm.clm_fwd_logits(W, base, T)[T-1] if hasattr(clm,"clm_fwd_logits") else clm._fwd_logits(W, base, T)[T-1]
    for p in range(T):
        pert=base.copy(); pert[p]=float((int(base[p])-65+13)%57+65)  # rot the byte
        lp=clm._fwd_logits(W, pert, T)[T-1]
        infl[p]+=float(np.abs(lp-l0).max())
infl/=NCTX
# distance from end (newest=dist1)
dist_infl={}
for p in range(T):
    d=T-p  # position p is d bytes back from the token being predicted
    dist_infl[d]=round(float(infl[p]),5)
# effective RF = max dist with influence > 1% of max
mx=max(infl) if infl.max()>0 else 1.0
thr=0.01*mx
rf=max([T-p for p in range(T) if infl[p]>thr], default=0)
print("influence by distance-from-end (d: max|Δlogit|):")
for d in sorted(dist_infl): print(f"  d={d:2d}: {dist_infl[d]}")
print(f"\neffective RF (>1% max influence) = {rf} bytes")
print(f"concept sentence ~30 bytes, concept-pair ~60 bytes")
print("VERDICT:", "RF-BOUND CONFIRMED (RF<<concept span → 2 concepts never co-visible → recombination impossible)" if rf<20 else "RF larger than expected — reconsider")
json.dump({"dist_infl":dist_infl,"rf":rf,"K":int(W["K"]),"L":int(W["L"])},open("/home/aiden/anima/rf_probe.json","w"),indent=2)
print("=== DONE ===")
