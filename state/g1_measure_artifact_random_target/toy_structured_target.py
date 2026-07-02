#!/usr/bin/env python3
"""MEASUREMENT-INTEGRITY check (break-walls: measure-artifact suspicion, 2026-07-02).
The entire cheap-gate campaign (H_1840, H_6164, H_6161/6162/1824) used a RANDOM target table
T[fa,fb] (operator-agnostic, chosen to avoid rigging). But a random table makes held-out (fa,fb)
information-theoretically INDEPENDENT of the training set -> chance is the CEILING, not a wall to
break. Real recombination (SCAN 'jump twice') has RULE STRUCTURE: parts predict the whole.
This tests whether held-out recombination is achievable AT ALL when the target is STRUCTURED,
using a PLAIN model (concat-embed MLP, CE) -- the same trunk that floored on random targets.
If structured lifts and random floors, the 'G1 wall' as measured was partly a random-target artifact.
FROZEN. tune-to-green forbidden (p7)."""
import json
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
dev="cuda" if torch.cuda.is_available() else "cpu"

NF, E, C = 8, 4, 8      # factors/slot, entities/factor, classes
K = 4                    # structured latent cardinality per factor (K<NF => shared structure)
D, H = 96, 192
STEPS, BS, LR = 6000, 256, 2e-3
SEEDS=[7,4302,4303,4304,4305]
HELDOUT_FRAC=0.22

def make(seed, kind):
    g=np.random.default_rng(seed)
    combos=[(a,b) for a in range(NF) for b in range(NF)]; g.shuffle(combos)
    nho=round(len(combos)*HELDOUT_FRAC); held=set(combos[:nho]); seen=[c for c in combos if c not in held]
    assert {a for a,_ in seen}==set(range(NF)) and {b for _,b in seen}==set(range(NF))
    if kind=="random":
        T=g.integers(0,C,size=(NF,NF))             # arbitrary lookup (old methodology) -> held-out independent
        def y(a,b): return T[a,b]
    elif kind=="struct_add":
        u=g.integers(0,C,size=NF); v=g.integers(0,C,size=NF)
        def y(a,b): return (u[a]+v[b])%C           # additive RULE (parts predict whole)
    elif kind=="struct_nonadd":
        ua=g.integers(0,K,size=NF); vb=g.integers(0,K,size=NF); T2=g.integers(0,C,size=(K,K))
        def y(a,b): return T2[ua[a],vb[b]]         # NON-additive rule via shared K-latent (factored, not arbitrary)
    return y, seen, sorted(held)

def sample(cl,yf,rng,n):
    idx=rng.integers(0,len(cl),size=n); A=np.array([cl[i][0] for i in idx]); B=np.array([cl[i][1] for i in idx])
    at=torch.tensor(A*E+rng.integers(0,E,size=n),device=dev); bt=torch.tensor(B*E+rng.integers(0,E,size=n),device=dev)
    yv=torch.tensor(np.array([yf(a,b) for a,b in zip(A,B)]),device=dev)
    return at,bt,yv

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

def train(seed,yf,seen):
    torch.manual_seed(seed); np.random.seed(seed); rng=np.random.default_rng(1000+seed)
    net=Net().to(dev); opt=torch.optim.Adam(net.parameters(),lr=LR)
    for _ in range(STEPS):
        at,bt,y=sample(seen,yf,rng,BS); loss=F.cross_entropy(net(at,bt),y)
        opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    def acc(cl,n=4096):
        at,bt,y=sample(cl,yf,rng,n)
        with torch.no_grad(): return (net(at,bt).argmax(-1)==y).float().mean().item()
    return acc

def main():
    chance=round(1/C,4); out={"chance":chance,"seeds":{}}
    for s in SEEDS:
        rec={}
        for kind in ["random","struct_add","struct_nonadd"]:
            yf,seen,held=make(s,kind); ac=train(s,yf,seen)
            rec[kind]={"train":round(ac(seen),4),"held":round(ac(held),4)}
            print(f"seed={s} {kind}: train={rec[kind]['train']} held={rec[kind]['held']} (chance={chance})",flush=True)
        out["seeds"][str(s)]=rec
    def mean_held(kind): return round(float(np.mean([out["seeds"][str(s)][kind]["held"] for s in SEEDS])),4)
    mh={k:mean_held(k) for k in ["random","struct_add","struct_nonadd"]}
    # interpretation (not a pass/fail lever gate — a measurement-integrity readout)
    over=lambda k: round(mh[k]-chance,4)
    if mh["struct_nonadd"]>=chance+0.20 and mh["random"]<=chance+0.10:
        verdict=("MEASURE-ARTIFACT CONFIRMED — plain model LIFTS held-out on STRUCTURED (non-additive) target but "
                 "floors on RANDOM. The random-target cheap-gate methodology measured memorization-of-noise, not "
                 "recombination; the real G1 question is STRUCTURED composition, which a plain trunk CAN generalize.")
    elif mh["struct_nonadd"]<=chance+0.10 and mh["struct_add"]<=chance+0.10:
        verdict=("WALL REAL (deeper) — even STRUCTURED-composition targets floor at held-out for a plain CE trunk; "
                 "the G1 wall is not a random-target artifact.")
    else:
        verdict=("MIXED — structured targets partially lift; random-target methodology is at least partly limiting. "
                 "See per-kind held means.")
    out["verdict"]={"mean_held":mh,"over_chance":{k:over(k) for k in mh},"reading":verdict}
    json.dump(out,open("result.json","w"),indent=2)
    print("\n=== VERDICT ===")
    print("mean held-out acc:",mh,"chance",chance)
    print("over-chance:",{k:over(k) for k in mh})
    print("READING:",verdict)

if __name__=="__main__": main()
