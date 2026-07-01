#!/usr/bin/env python3
"""Data-coverage THRESHOLD cheap-gate (H_1824 direction, FROZEN 2026-07-02).
Does compositional generalization to a FIXED held-out set emerge above a training-coverage
threshold (An&Du/PMC: data-coverage = threshold effect)? Same operator-agnostic factored task
as H_6161/6162. Sweep # of trained (fa,fb) combos; held-out TEST set fixed across all coverages.
torch mirror=DIRECTIONAL. tune-to-green forbidden (p7)."""
import json
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

NF, E, C = 8, 4, 12          # richer factor space (64 combos) for coverage room
D, H = 96, 192
STEPS, BS, LR = 5000, 256, 2e-3
COVERAGE = [16, 26, 36, 46, 52]   # # trained combos (of 52 non-test); TEST=12 fixed held-out
N_TEST = 12
SEEDS = [7, 4302, 4303]

def make(seed):
    g=np.random.default_rng(seed)
    T=g.integers(0,C,size=(NF,NF))
    combos=[(a,b) for a in range(NF) for b in range(NF)]  # 64
    g.shuffle(combos)
    test=combos[:N_TEST]; pool=combos[N_TEST:]            # 12 test fixed, 52 pool
    return T,test,pool

def sample(cl,T,rng,n):
    fa=np.array([c[0] for c in cl]); fb=np.array([c[1] for c in cl])
    idx=rng.integers(0,len(cl),size=n); A,B=fa[idx],fb[idx]
    return (torch.tensor(A*E+rng.integers(0,E,size=n)),
            torch.tensor(B*E+rng.integers(0,E,size=n)), torch.tensor(T[A,B]))

class Net(nn.Module):
    def __init__(s):
        super().__init__(); V=NF*E
        s.ea=nn.Embedding(V,D); s.eb=nn.Embedding(V,D)
        s.part=nn.Sequential(nn.Linear(D,H),nn.GELU(),nn.Linear(H,D))
        s.pair=nn.Sequential(nn.Linear(2*D,H),nn.GELU(),nn.Linear(H,D))
        s.ro=nn.Linear(D,C)
    def forward(s,at,bt):
        ra,rb=s.part(s.ea(at)),s.part(s.eb(bt))
        return s.ro(s.pair(torch.cat([ra,rb],-1)))

def run(seed,cov,T,test,pool):
    torch.manual_seed(seed); np.random.seed(seed)
    rng=np.random.default_rng(1000+seed)
    train=pool[:cov]
    net=Net(); opt=torch.optim.Adam(net.parameters(),lr=LR)
    for _ in range(STEPS):
        at,bt,y=sample(train,T,rng,BS)
        loss=F.cross_entropy(net(at,bt),y)
        opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    def acc(cl,n=4096):
        at,bt,y=sample(cl,T,rng,n)
        with torch.no_grad(): return (net(at,bt).argmax(-1)==y).float().mean().item()
    return round(acc(train),4), round(acc(test),4)

def main():
    out={"chance":round(1/C,4),"N_test":N_TEST,"seeds":{}}
    for s in SEEDS:
        T,test,pool=make(s); rec={}
        for cov in COVERAGE:
            tr,te=run(s,cov,T,test,pool)
            rec[f"cov_{cov}"]={"train_acc":tr,"test_acc":te}
            print(f"seed={s} cov={cov}/52: train={tr} test={te}",flush=True)
        out["seeds"][str(s)]=rec
    # FROZEN bar: does test acc rise MONOTONE with coverage AND cross chance+0.15 at high cov on >=2/3 seeds?
    chance=out["chance"]; per=[]
    for s in SEEDS:
        rec=out["seeds"][str(s)]
        tests=[rec[f"cov_{c}"]["test_acc"] for c in COVERAGE]
        mono=all(tests[i+1]>=tests[i]-0.03 for i in range(len(tests)-1))  # ~monotone
        hi=tests[-1]                                                       # max coverage test acc
        per.append({"seed":s,"tests":tests,"monotone":mono,"hi":hi,"hi_over_chance":round(hi-chance,4)})
    n_thresh=sum(1 for p in per if p["hi_over_chance"]>=0.15)
    n_mono=sum(1 for p in per if p["monotone"])
    if n_thresh>=2 and n_mono>=2:
        tier="DIRECTIONAL-SUPPORT — data-coverage threshold lifts held-out composition (engine-native GPU authorized)"
    else:
        tier="🧱 DIRECTIONAL-FLOOR — data coverage does not open held-out composition (H_1599 EN-exposure floor extends)"
    out["verdict"]={"per_seed":per,"n_hi_over_chance_ge_0.15":n_thresh,"n_monotone":n_mono,"tier":tier}
    json.dump(out,open("result.json","w"),indent=2)
    print("\n=== VERDICT ===")
    for p in per: print(p)
    print("TIER:",tier)

if __name__=="__main__": main()
