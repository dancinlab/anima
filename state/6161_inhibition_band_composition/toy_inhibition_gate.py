#!/usr/bin/env python3
"""H_6161 INHIBITION-AS-COMPOSITIONAL-NOISE fair cheap-gate (FROZEN 2026-07-02).
Does trunk inhibition (dropout, savant golden-zone dp~0.25) degrade held-out compositional
generalization (An&Du noise-degrade), so LOWER dp lifts G1? Sweep dp; measure held-out
composition acc + HE-proxy (homomorphism generalization residual). torch mirror=DIRECTIONAL.
tune-to-green forbidden (p7). Same operator-agnostic compositional toy as H_6162."""
import json
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

NF, E, C = 6, 4, 9
D, H = 96, 192
STEPS, BS, LR = 4000, 256, 2e-3
DPS = [0.0, 0.1, 0.25, 0.4]     # 0.25 = savant golden-zone default (GZ); <0.25 = below GZ_LOWER arm
GZ = 0.25
SEEDS = [7, 4302, 4303, 4304, 4305]
HELDOUT_FRAC = 0.22

def make_task(seed):
    g = np.random.default_rng(seed)
    T = g.integers(0, C, size=(NF, NF))
    combos = [(a, b) for a in range(NF) for b in range(NF)]
    g.shuffle(combos)
    nho = round(len(combos) * HELDOUT_FRAC)
    held = set(combos[:nho]); seen = [c for c in combos if c not in held]
    assert {a for a,_ in seen}==set(range(NF)) and {b for _,b in seen}==set(range(NF))
    return T, seen, sorted(held)

def sample(cl, T, rng, n):
    fa=np.array([c[0] for c in cl]); fb=np.array([c[1] for c in cl])
    idx=rng.integers(0,len(cl),size=n); A_f,B_f=fa[idx],fb[idx]
    return (torch.tensor(A_f*E+rng.integers(0,E,size=n)),
            torch.tensor(B_f*E+rng.integers(0,E,size=n)),
            torch.tensor(T[A_f,B_f]))

class Net(nn.Module):
    def __init__(self, dp):
        super().__init__(); V=NF*E
        self.ea=nn.Embedding(V,D); self.eb=nn.Embedding(V,D)
        self.part=nn.Sequential(nn.Linear(D,H),nn.GELU(),nn.Dropout(dp),nn.Linear(H,D))
        self.pair=nn.Sequential(nn.Linear(2*D,H),nn.GELU(),nn.Dropout(dp),nn.Linear(H,D))
        self.readout=nn.Linear(D,C)
    def reps(self, at, bt):
        ra,rb=self.part(self.ea(at)),self.part(self.eb(bt))
        h=self.pair(torch.cat([ra,rb],-1)); return h,ra,rb
    def forward(self, at, bt):
        h,ra,rb=self.reps(at,bt); return self.readout(h),h,ra,rb

def train(seed, dp, T, train_combos):
    torch.manual_seed(seed); np.random.seed(seed)
    rng=np.random.default_rng(1000+seed)
    net=Net(dp); opt=torch.optim.Adam(net.parameters(),lr=LR)
    for _ in range(STEPS):
        at,bt,y=sample(train_combos,T,rng,BS)
        logits,_,_,_=net(at,bt)
        loss=F.cross_entropy(logits,y)
        opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    def acc(cl,n=4096):
        at,bt,y=sample(cl,T,rng,n)
        with torch.no_grad(): return (net(at,bt)[0].argmax(-1)==y).float().mean().item()
    # HE-proxy: fit linear [ra;rb;ra*rb]->h on SEEN, residual on HELD (homomorphism generalization err)
    def he_proxy(seen_cl, held_cl, n=4096):
        with torch.no_grad():
            at,bt,_=sample(seen_cl,T,rng,n); h,ra,rb=net.reps(at,bt)
            X=torch.cat([ra,rb,ra*rb],-1); Xb=torch.cat([X,torch.ones(n,1)],-1)
            W=torch.linalg.lstsq(Xb,h).solution
            at2,bt2,_=sample(held_cl,T,rng,n); h2,ra2,rb2=net.reps(at2,bt2)
            X2=torch.cat([torch.cat([ra2,rb2,ra2*rb2],-1),torch.ones(n,1)],-1)
            res=F.mse_loss(X2@W,h2).item(); var=h2.var().item()
            return round(res/max(var,1e-6),4)
    return acc, he_proxy

def main():
    out={"frozen":"this-file docstring","chance":round(1/C,4),"GZ_default":GZ,"seeds":{}}
    for s in SEEDS:
        T,seen,held=make_task(s)
        rec={"n_held":len(held),"arms":{}}
        _,_=None,None
        # oracle sanity
        oacc,_=train(s,0.0,T,seen+list(held)); rec["oracle_heldout_acc"]=round(oacc(held),4)
        for dp in DPS:
            acc,he=train(s,dp,T,seen)
            rec["arms"][f"dp_{dp}"]={"train_acc":round(acc(seen),4),
                                     "heldout_acc":round(acc(held),4),
                                     "he_proxy":he(seen,held)}
            a=rec["arms"][f"dp_{dp}"]
            print(f"seed={s} dp={dp}: train={a['train_acc']} held={a['heldout_acc']} HE={a['he_proxy']} (oracle={rec['oracle_heldout_acc']})",flush=True)
        out["seeds"][str(s)]=rec
    # FROZEN bar: does BEST dp<GZ lift held-out >=+0.15 over dp=GZ, >=2/3 seeds, no regress?
    per=[]
    for s in SEEDS:
        arms=out["seeds"][str(s)]["arms"]
        gz=arms[f"dp_{GZ}"]["heldout_acc"]
        low_best=max(arms[f"dp_{dp}"]["heldout_acc"] for dp in DPS if dp<GZ)
        per.append({"seed":s,"gz":gz,"low_best":low_best,"delta":round(low_best-gz,4)})
    n_ge=sum(1 for p in per if p["delta"]>=0.15)
    no_regress=all(p["low_best"]>=p["gz"] for p in per)
    train_ok=all(out["seeds"][str(s)]["arms"][f"dp_{dp}"]["train_acc"]>=0.90 for s in SEEDS for dp in DPS)
    oracle_ok=all(out["seeds"][str(s)]["oracle_heldout_acc"]>=0.90 for s in SEEDS)
    if not(train_ok and oracle_ok): tier="INCONCLUSIVE (sanity fail)"
    elif n_ge>=2/3*len(SEEDS) and no_regress:
        tier="DIRECTIONAL-SUPPORT (lower-inhibition lifts held-out >=+0.15 on >=2/3, no regress) — engine-native GPU authorized"
    else:
        tier="🧱 DIRECTIONAL-FLOOR (NOT-SUPPORTED) — inhibition band does not open G1 composition"
    out["verdict"]={"per_seed":per,"n_delta_ge_0.15":n_ge,"no_regress":no_regress,
                    "train_ok":train_ok,"oracle_ok":oracle_ok,"tier":tier}
    json.dump(out,open("result.json","w"),indent=2)
    print("\n=== VERDICT ===")
    for p in per: print(p)
    print("oracle_ok:",oracle_ok,"| n>=+0.15:",n_ge,"/",len(SEEDS),"| no_regress:",no_regress)
    print("TIER:",tier)

if __name__=="__main__": main()
