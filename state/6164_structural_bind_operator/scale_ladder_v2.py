#!/usr/bin/env python3
"""H_6164 GPU SCALE-LADDER v2 — does the tensor-product structural-bind signal (H_6164's real
carrier) CROSS +0.15 and GROW with scale? v1 fix: (1) include FULL tensorproduct (excluded in v1),
(2) keep C fixed so difficulty doesn't grow, (3) scale steps hard so each rung's oracle solves
(v1 upper rungs undertrained, oracle<0.85). FROZEN 2026-07-02. tune-to-green forbidden (p7)."""
import json, time
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
dev="cuda" if torch.cuda.is_available() else "cpu"
print("device:",dev, torch.cuda.get_device_name(0) if dev=="cuda" else "",flush=True)

C=9
RUNGS=[dict(NF=6, E=4, D=96,  R=32,  steps=10000),
       dict(NF=10,E=6, D=160, R=64,  steps=45000),
       dict(NF=14,E=8, D=256, R=96,  steps=120000)]
ARMS=["add","hadamard","bilinear","tensorproduct"]
SEEDS=[7,4302,4303]; BS,LR=512,2e-3; HELDOUT_FRAC=0.22

def make(seed,NF):
    g=np.random.default_rng(seed); T=g.integers(0,C,size=(NF,NF))
    combos=[(a,b) for a in range(NF) for b in range(NF)]; g.shuffle(combos)
    nho=round(len(combos)*HELDOUT_FRAC); held=set(combos[:nho]); seen=[c for c in combos if c not in held]
    assert {a for a,_ in seen}==set(range(NF)) and {b for _,b in seen}==set(range(NF))
    return T,seen,sorted(held)
def sample(cl,T,rng,n,E):
    fa=np.array([c[0] for c in cl]); fb=np.array([c[1] for c in cl])
    idx=rng.integers(0,len(cl),size=n); A,B=fa[idx],fb[idx]
    return (torch.tensor(A*E+rng.integers(0,E,size=n),device=dev),
            torch.tensor(B*E+rng.integers(0,E,size=n),device=dev),
            torch.tensor(T[A,B],device=dev))
class Net(nn.Module):
    def __init__(s,arm,NF,E,D,R):
        super().__init__(); V=NF*E; s.arm=arm; s.R=R; s.D=D; H=2*D
        s.ea=nn.Embedding(V,D); s.eb=nn.Embedding(V,D)
        s.part=nn.Sequential(nn.Linear(D,H),nn.GELU(),nn.Linear(H,D))
        if arm=="add": s.comp=nn.Sequential(nn.Linear(2*D,H),nn.GELU(),nn.Linear(H,D))
        elif arm=="hadamard": s.comp=nn.Sequential(nn.Linear(D,H),nn.GELU(),nn.Linear(H,D))
        elif arm=="bilinear": s.U=nn.Linear(D,R*D,bias=False); s.Vv=nn.Linear(D,R*D,bias=False)
        elif arm=="tensorproduct": s.tp=nn.Linear(D*D,D)
        s.ro=nn.Linear(D,C)
    def forward(s,at,bt):
        ra,rb=s.part(s.ea(at)),s.part(s.eb(bt)); n=ra.shape[0]
        if s.arm=="add": h=s.comp(torch.cat([ra,rb],-1))
        elif s.arm=="hadamard": h=s.comp(ra*rb)
        elif s.arm=="bilinear":
            u=s.U(ra).reshape(n,s.R,s.D); v=s.Vv(rb).reshape(n,s.R,s.D); h=(u*v).sum(1)
        elif s.arm=="tensorproduct":
            h=s.tp((ra.unsqueeze(2)*rb.unsqueeze(1)).reshape(n,-1))
        return s.ro(h)
def train(seed,arm,cfg,T,tc):
    torch.manual_seed(seed); np.random.seed(seed); rng=np.random.default_rng(1000+seed)
    net=Net(arm,cfg["NF"],cfg["E"],cfg["D"],cfg["R"]).to(dev); opt=torch.optim.Adam(net.parameters(),lr=LR)
    for _ in range(cfg["steps"]):
        at,bt,y=sample(tc,T,rng,BS,cfg["E"]); loss=F.cross_entropy(net(at,bt),y)
        opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    def acc(cl,n=8192):
        at,bt,y=sample(cl,T,rng,n,cfg["E"])
        with torch.no_grad(): return (net(at,bt).argmax(-1)==y).float().mean().item()
    return acc
def main():
    t0=time.time(); ladder=[]
    for ri,cfg in enumerate(RUNGS):
        print(f"=== RUNG {ri} {cfg} ===",flush=True); out={"cfg":cfg,"seeds":{}}
        for s in SEEDS:
            T,seen,held=make(s,cfg["NF"]); oa=train(s,"add",cfg,T,seen+list(held)); orc=round(oa(held),4)
            rec={"oracle":orc,"arms":{}}
            for arm in ARMS:
                ac=train(s,arm,cfg,T,seen); rec["arms"][arm]={"train":round(ac(seen),4),"held":round(ac(held),4)}
                print(f"  r{ri} s={s} {arm}: tr={rec['arms'][arm]['train']} held={rec['arms'][arm]['held']} (orc={orc})",flush=True)
            out["seeds"][str(s)]=rec
        deltas=[]; tpdeltas=[]
        for s in SEEDS:
            a=out["seeds"][str(s)]["arms"]; add=a["add"]["held"]
            deltas.append(round(max(a[k]["held"] for k in ARMS if k!="add")-add,4))
            tpdeltas.append(round(a["tensorproduct"]["held"]-add,4))
        out["deltas"]=deltas; out["tp_deltas"]=tpdeltas
        out["mean_delta"]=round(float(np.mean(deltas)),4); out["mean_tp_delta"]=round(float(np.mean(tpdeltas)),4)
        out["n_ge_0.15"]=sum(1 for d in deltas if d>=0.15)
        print(f"  >> r{ri} best-delta={deltas} tp-delta={tpdeltas} mean_tp={out['mean_tp_delta']} n>=+.15={out['n_ge_0.15']}",flush=True)
        ladder.append(out); json.dump({"ladder":ladder},open("result.json","w"),indent=2)
    top,r0=ladder[-1],ladder[0]
    oracle_ok=all(ladder[i]["seeds"][str(s)]["oracle"]>=0.85 for i in range(len(ladder)) for s in SEEDS)
    grows=top["mean_delta"]>r0["mean_delta"]+0.03; cross=top["n_ge_0.15"]>=2
    if not oracle_ok: tier="INCONCLUSIVE (some rung oracle<0.85 = undertrained/unsolvable)"
    elif cross and grows: tier="★★ SCALE-LEVER FOUND — structural-bind delta crosses +0.15 AND grows = G1 LEVER (303M fire warranted)"
    elif grows: tier="🟡 DIRECTIONAL-GROWING — delta grows but top<+0.15 on 2/3 (bigger scale/303M to confirm)"
    else: tier="🧱 FLOOR — structural-bind does NOT scale-amplify (H_1840 confirmed at scale, GPU closes it)"
    v={"rung_mean_best_delta":[r["mean_delta"] for r in ladder],"rung_mean_tp_delta":[r["mean_tp_delta"] for r in ladder],
       "rung_n_ge_0.15":[r["n_ge_0.15"] for r in ladder],"rung_oracle":[[ladder[i]["seeds"][str(s)]["oracle"] for s in SEEDS] for i in range(len(ladder))],
       "grows":grows,"top_cross":cross,"oracle_ok":oracle_ok,"tier":tier,"wall_sec":round(time.time()-t0)}
    json.dump({"ladder":ladder,"verdict":v},open("result.json","w"),indent=2)
    print("\n=== VERDICT ===\nbest-delta/rung:",v["rung_mean_best_delta"],"\ntp-delta/rung:",v["rung_mean_tp_delta"],
          "\noracle/rung:",v["rung_oracle"],"\nTIER:",tier,flush=True)
if __name__=="__main__": main()
