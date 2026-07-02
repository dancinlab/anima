#!/usr/bin/env python3
"""G1 LEVER HUNT on the CORRECT (structured, learnable) task (H_6166 follow-on, 2026-07-02).
H_6166 proved random-target cheap-gates were unlearnable artifacts; a plain trunk gets 98% held-out on
EASY structured targets. The valid lever question: on a STRUCTURED-but-HARD target (learnable, but where
the plain additive trunk only PARTIALLY generalizes held-out = headroom), does a multiplicative composition
OPERATOR (hadamard / bilinear / tensor-product) lift held-out recombination >=+0.15 over additive?
Target y=T2[ua[fa],vb[fb]] (factored NON-additive rule); K = shared-latent cardinality controls difficulty
(small K=easy sharing, K->NF approaches random). Sweep K to find headroom, compare operators at each K.
FROZEN. tune-to-green forbidden (p7). torch mirror=DIRECTIONAL."""
import json
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
dev="cuda" if torch.cuda.is_available() else "cpu"

NF, E, C = 12, 4, 10
D, H = 64, 160
STEPS, BS, LR = 6000, 256, 2e-3
KS=[6,8,10,12]          # shared-latent cardinality (difficulty knob; NF=12)
ARMS=["add","hadamard","bilinear"]
SEEDS=[7,4302,4303]
HELDOUT_FRAC=0.25

def make(seed,K):
    g=np.random.default_rng(seed)
    ua=g.integers(0,K,size=NF); vb=g.integers(0,K,size=NF); T2=g.integers(0,C,size=(K,K))
    combos=[(a,b) for a in range(NF) for b in range(NF)]; g.shuffle(combos)
    nho=round(len(combos)*HELDOUT_FRAC); held=set(combos[:nho]); seen=[c for c in combos if c not in held]
    assert {a for a,_ in seen}==set(range(NF)) and {b for _,b in seen}==set(range(NF))
    def y(a,b): return T2[ua[a],vb[b]]
    return y,seen,sorted(held)

def sample(cl,yf,rng,n):
    idx=rng.integers(0,len(cl),size=n); A=np.array([cl[i][0] for i in idx]); B=np.array([cl[i][1] for i in idx])
    return (torch.tensor(A*E+rng.integers(0,E,size=n),device=dev),
            torch.tensor(B*E+rng.integers(0,E,size=n),device=dev),
            torch.tensor(np.array([yf(a,b) for a,b in zip(A,B)]),device=dev))

class Net(nn.Module):
    def __init__(s,arm):
        super().__init__(); V=NF*E; s.arm=arm; R=32
        s.ea=nn.Embedding(V,D); s.eb=nn.Embedding(V,D)
        s.part=nn.Sequential(nn.Linear(D,H),nn.GELU(),nn.Linear(H,D))
        if arm=="add": s.comp=nn.Sequential(nn.Linear(2*D,H),nn.GELU(),nn.Linear(H,D))
        elif arm=="hadamard": s.comp=nn.Sequential(nn.Linear(D,H),nn.GELU(),nn.Linear(H,D))
        elif arm=="bilinear": s.U=nn.Linear(D,R*D,bias=False); s.Vv=nn.Linear(D,R*D,bias=False); s.R=R
        elif arm=="tensorproduct": s.tp=nn.Linear(D*D,D)
        s.ro=nn.Linear(D,C); s.D=D
    def forward(s,at,bt):
        ra,rb=s.part(s.ea(at)),s.part(s.eb(bt)); n=ra.shape[0]
        if s.arm=="add": h=s.comp(torch.cat([ra,rb],-1))
        elif s.arm=="hadamard": h=s.comp(ra*rb)
        elif s.arm=="bilinear":
            u=s.U(ra).reshape(n,s.R,s.D); v=s.Vv(rb).reshape(n,s.R,s.D); h=(u*v).sum(1)
        elif s.arm=="tensorproduct": h=s.tp((ra.unsqueeze(2)*rb.unsqueeze(1)).reshape(n,-1))
        return s.ro(h)

def train(seed,arm,yf,seen):
    torch.manual_seed(seed); np.random.seed(seed); rng=np.random.default_rng(1000+seed)
    net=Net(arm).to(dev); opt=torch.optim.Adam(net.parameters(),lr=LR)
    for _ in range(STEPS):
        at,bt,y=sample(seen,yf,rng,BS); loss=F.cross_entropy(net(at,bt),y)
        opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    def acc(cl,n=4096):
        at,bt,y=sample(cl,yf,rng,n)
        with torch.no_grad(): return (net(at,bt).argmax(-1)==y).float().mean().item()
    return acc

def main():
    chance=round(1/C,4); out={"chance":chance,"K":{}}
    for K in KS:
        kr={}
        for arm in ARMS:
            hs=[]
            for s in SEEDS:
                yf,seen,held=make(s,K); ac=train(s,arm,yf,seen); hs.append(round(ac(held),4))
            kr[arm]={"held_per_seed":hs,"held_mean":round(float(np.mean(hs)),4)}
            print(f"K={K} {arm}: held_mean={kr[arm]['held_mean']} per_seed={hs}",flush=True)
        add=kr["add"]["held_mean"]
        kr["best_mult_arm"]=max([a for a in ARMS if a!="add"],key=lambda a:kr[a]["held_mean"])
        kr["best_mult_mean"]=kr[kr["best_mult_arm"]]["held_mean"]
        kr["mult_minus_add"]=round(kr["best_mult_mean"]-add,4)
        kr["headroom"]=round(1.0-add,4)
        print(f"  >> K={K}: add={add} best_mult={kr['best_mult_mean']}({kr['best_mult_arm']}) Δ={kr['mult_minus_add']} headroom={kr['headroom']}",flush=True)
        out["K"][str(K)]=kr
    # LEVER FOUND iff at some K with real headroom (add<=0.85 AND add>chance+0.1), a mult arm beats add by >=+0.15
    hits=[]
    for K in KS:
        kr=out["K"][str(K)]; add=kr["add"]["held_mean"]
        if add<=0.85 and add>=chance+0.1 and kr["mult_minus_add"]>=0.15: hits.append((K,kr["best_mult_arm"],kr["mult_minus_add"]))
    if hits:
        tier=f"★★ G1 LEVER FOUND — multiplicative operator lifts held-out >=+0.15 over additive on structured-hard task at K={hits}"
    else:
        anyhead=any(out['K'][str(K)]['add']<=0.85 and out['K'][str(K)]['add']>=chance+0.1 for K in KS)
        tier=("🧱 NO OPERATOR LEVER — no mult arm beats additive by +0.15 in any headroom regime (operator doesn't matter even on structured tasks; capability is task-structure-bound, not operator-bound)"
              if anyhead else "INCONCLUSIVE — no K produced a headroom regime (all add saturated or floored); adjust K/difficulty")
    out["verdict"]={"hits":hits,"tier":tier}
    json.dump(out,open("result.json","w"),indent=2)
    print("\n=== VERDICT ===")
    for K in KS:
        kr=out["K"][str(K)]; print(f"K={K}: add={kr['add']['held_mean']} best_mult={kr['best_mult_mean']}({kr['best_mult_arm']}) Δ={kr['mult_minus_add']}")
    print("TIER:",tier)

if __name__=="__main__": main()
