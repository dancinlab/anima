#!/usr/bin/env python3
"""G1 STRUCTURAL BIND-OPERATOR cheap-gate (framebreak thesis: wall = combination operator).
All prior toy axes (H_6162 objective / H_6161 reg / H_1824 data) kept the SAME additive-concat
trunk and floored. Here we swap the TRUNK pair-composition to explicit multiplicative binders
(hadamard / tensor-product / bilinear) trained end-to-end. Does ANY structural binder open held-out
recombination over the additive baseline? FROZEN 2026-07-02. torch=DIRECTIONAL. tune-to-green forbidden."""
import json
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

NF, E, C = 6, 4, 9
Dd, H = 64, 192
STEPS, BS, LR = 4000, 256, 2e-3
ARMS = ["add", "hadamard", "tensorproduct", "bilinear"]
SEEDS = [7, 4302, 4303, 4304, 4305]
HELDOUT_FRAC = 0.22

def make(seed):
    g=np.random.default_rng(seed); T=g.integers(0,C,size=(NF,NF))
    combos=[(a,b) for a in range(NF) for b in range(NF)]; g.shuffle(combos)
    nho=round(len(combos)*HELDOUT_FRAC); held=set(combos[:nho]); seen=[c for c in combos if c not in held]
    assert {a for a,_ in seen}==set(range(NF)) and {b for _,b in seen}==set(range(NF))
    return T,seen,sorted(held)

def sample(cl,T,rng,n):
    fa=np.array([c[0] for c in cl]); fb=np.array([c[1] for c in cl])
    idx=rng.integers(0,len(cl),size=n); A,B=fa[idx],fb[idx]
    return (torch.tensor(A*E+rng.integers(0,E,size=n)),torch.tensor(B*E+rng.integers(0,E,size=n)),torch.tensor(T[A,B]))

class Net(nn.Module):
    def __init__(s,arm):
        super().__init__(); V=NF*E; s.arm=arm
        s.ea=nn.Embedding(V,Dd); s.eb=nn.Embedding(V,Dd)
        s.part=nn.Sequential(nn.Linear(Dd,H),nn.GELU(),nn.Linear(H,Dd))
        if arm=="add": s.comp=nn.Sequential(nn.Linear(2*Dd,H),nn.GELU(),nn.Linear(H,Dd))
        elif arm=="hadamard": s.comp=nn.Sequential(nn.Linear(Dd,H),nn.GELU(),nn.Linear(H,Dd))
        elif arm=="tensorproduct": s.comp=nn.Linear(Dd*Dd,Dd)  # explicit outer product bind
        elif arm=="bilinear":
            R=32; s.U=nn.Linear(Dd,R*Dd,bias=False); s.Vv=nn.Linear(Dd,R*Dd,bias=False); s.R=R
        s.ro=nn.Linear(Dd,C)
    def forward(s,at,bt):
        ra,rb=s.part(s.ea(at)),s.part(s.eb(bt)); n=ra.shape[0]
        if s.arm=="add": h=s.comp(torch.cat([ra,rb],-1))
        elif s.arm=="hadamard": h=s.comp(ra*rb)
        elif s.arm=="tensorproduct":
            tp=(ra.unsqueeze(2)*rb.unsqueeze(1)).reshape(n,-1); h=s.comp(tp)
        elif s.arm=="bilinear":
            u=s.U(ra).reshape(n,s.R,Dd); v=s.Vv(rb).reshape(n,s.R,Dd); h=(u*v).sum(1)
        return s.ro(h)

def train(seed,arm,T,train_combos):
    torch.manual_seed(seed); np.random.seed(seed); rng=np.random.default_rng(1000+seed)
    net=Net(arm); opt=torch.optim.Adam(net.parameters(),lr=LR)
    for _ in range(STEPS):
        at,bt,y=sample(train_combos,T,rng,BS); loss=F.cross_entropy(net(at,bt),y)
        opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    def acc(cl,n=4096):
        at,bt,y=sample(cl,T,rng,n)
        with torch.no_grad(): return (net(at,bt).argmax(-1)==y).float().mean().item()
    return acc

def main():
    out={"chance":round(1/C,4),"seeds":{}}
    for s in SEEDS:
        T,seen,held=make(s); rec={"arms":{}}
        oacc=train(s,"add",T,seen+list(held)); rec["oracle_heldout"]=round(oacc(held),4)
        for arm in ARMS:
            acc=train(s,arm,T,seen); rec["arms"][arm]={"train":round(acc(seen),4),"held":round(acc(held),4)}
            print(f"seed={s} {arm}: train={rec['arms'][arm]['train']} held={rec['arms'][arm]['held']} (oracle={rec['oracle_heldout']})",flush=True)
        out["seeds"][str(s)]=rec
    per=[]
    for s in SEEDS:
        a=out["seeds"][str(s)]["arms"]; add=a["add"]["held"]
        best_bind=max(a[k]["held"] for k in ARMS if k!="add"); best_arm=max([k for k in ARMS if k!="add"],key=lambda k:a[k]["held"])
        per.append({"seed":s,"add":add,"best_bind":best_bind,"best_arm":best_arm,"delta":round(best_bind-add,4)})
    n_ge=sum(1 for p in per if p["delta"]>=0.15); no_reg=all(p["best_bind"]>=p["add"] for p in per)
    oracle_ok=all(out["seeds"][str(s)]["oracle_heldout"]>=0.90 for s in SEEDS)
    if not oracle_ok: tier="INCONCLUSIVE (oracle sanity fail)"
    elif n_ge>=2/3*len(SEEDS) and no_reg:
        tier="★ DIRECTIONAL-SUPPORT — a STRUCTURAL BINDER opens held-out composition (G1 LEVER CANDIDATE; contradicts H_1840; engine-native GPU warranted)"
    else:
        tier="🧱 DIRECTIONAL-FLOOR — structural binders (hadamard/tensorproduct/bilinear) do NOT open held-out (framebreak combination-operator thesis FALSIFIED in toy; H_1840 confirmed)"
    out["verdict"]={"per_seed":per,"n_delta_ge_0.15":n_ge,"no_regress":no_reg,"oracle_ok":oracle_ok,"tier":tier}
    json.dump(out,open("result.json","w"),indent=2)
    print("\n=== VERDICT ===")
    for p in per: print(p)
    print("TIER:",tier)

if __name__=="__main__": main()
