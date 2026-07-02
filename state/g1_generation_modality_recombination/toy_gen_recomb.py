#!/usr/bin/env python3
"""GENERATION-modality held-out recombination (G1-NEXT-2 reframed by H_6169). v3: 6 seeds, 8000 steps,
converged-seed-only struct mean (exclude seeds where struct seen_gen<0.9 = optimization non-convergence,
not a recombination failure). Q: does GENERATION support held-out compositional recombination? Small AR
transformer, synthetic compositional language seq=[A,B,SEP,o1,o2,o3], o=structured factored rule vs random.
torch=DIRECTIONAL. tune-to-green forbidden."""
import json
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
dev="cuda" if torch.cuda.is_available() else "cpu"
NA,NB,K,OV,OLEN = 16,16,5,7,3
SEP=NA+NB; Aoff=0; Boff=NA; VOCAB=NA+NB+1+OV
d,NL,nhead = 128,3,4
STEPS,BS,LR = 8000,128,2e-3
SEEDS=[7,4302,4303,4304,4305,11]; HELD=0.25

def make(seed,kind):
    g=np.random.default_rng(seed)
    ua=g.integers(0,K,size=NA); vb=g.integers(0,K,size=NB)
    Ts=g.integers(0,OV,size=(K,K,OLEN)); Tr=g.integers(0,OV,size=(NA,NB,OLEN))
    combos=[(a,b) for a in range(NA) for b in range(NB)]; g.shuffle(combos)
    nho=round(len(combos)*HELD); held=set(combos[:nho]); seen=[c for c in combos if c not in held]
    def out(a,b): return Ts[ua[a],vb[b]] if kind=="struct" else Tr[a,b]
    return out,seen,sorted(held)

def seq_of(a,b,out):
    o=out(a,b); return [Aoff+a,Boff+b,SEP,(NA+NB+1)+o[0],(NA+NB+1)+o[1],(NA+NB+1)+o[2]]

class AR(nn.Module):
    def __init__(s):
        super().__init__()
        s.emb=nn.Embedding(VOCAB,d); s.pos=nn.Embedding(6,d)
        l=nn.TransformerEncoderLayer(d,nhead,4*d,batch_first=True,dropout=0.0)
        s.tr=nn.TransformerEncoder(l,NL); s.head=nn.Linear(d,VOCAB)
        s.register_buffer("mask",torch.triu(torch.ones(6,6)*float('-inf'),diagonal=1))
    def forward(s,x):
        T=x.shape[1]; h=s.emb(x)+s.pos(torch.arange(T,device=x.device))
        return s.head(s.tr(h,mask=s.mask[:T,:T]))

def train(seed,out,seen,held):
    torch.manual_seed(seed); np.random.seed(seed); rng=np.random.default_rng(1000+seed)
    net=AR().to(dev); opt=torch.optim.Adam(net.parameters(),lr=LR)
    for _ in range(STEPS):
        idx=rng.integers(0,len(seen),size=BS)
        b=np.array([seq_of(seen[i][0],seen[i][1],out) for i in idx])
        x=torch.tensor(b[:,:-1],device=dev); y=torch.tensor(b[:,1:],device=dev)
        loss=F.cross_entropy(net(x).reshape(-1,VOCAB),y.reshape(-1))
        opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    def acc(cl):
        ok=0
        for a,b_ in cl:
            full=seq_of(a,b_,out); cur=full[:3]
            for _ in range(OLEN):
                with torch.no_grad(): lg=net(torch.tensor([cur],device=dev))[0,-1]
                cur=cur+[int(lg.argmax())]
            ok+=1 if cur[3:]==full[3:] else 0
        return ok/len(cl)
    return acc(seen),acc(held)

def main():
    o={"seeds":{}}
    for s in SEEDS:
        rec={}
        for kind in ["random","struct"]:
            out,seen,held=make(s,kind); sa,ha=train(s,out,seen,held)
            rec[kind]={"seen_gen":round(sa,4),"held_gen":round(ha,4)}
            print(f"seed={s} {kind}: seen={sa:.3f} held={ha:.3f}",flush=True)
        o["seeds"][str(s)]=rec
    conv=[s for s in SEEDS if o["seeds"][str(s)]["struct"]["seen_gen"]>=0.9] or SEEDS
    sh=round(float(np.mean([o["seeds"][str(s)]["struct"]["held_gen"] for s in conv])),4)
    ss=round(float(np.mean([o["seeds"][str(s)]["struct"]["seen_gen"] for s in conv])),4)
    rh=round(float(np.mean([o["seeds"][str(s)]["random"]["held_gen"] for s in SEEDS])),4)
    chance=(1/OV)**OLEN
    if sh>=0.6 and rh<=0.15:
        v=("GENERATION SUPPORTS HELD-OUT RECOMBINATION — converged AR models GENERATE held-out compositional "
           "outputs for structured rules (struct held=%.2f over %d/%d converged seeds) but not random (held=%.2f). "
           "=> generation modality is NOT the barrier; anima real-text G1=0 is a training/objective/metric issue "
           "(H_6169: G1=generation-diversity), not generation-modality impossibility."%(sh,len(conv),len(SEEDS),rh))
    elif sh<=0.2:
        v="GENERATION FLOOR — even structured rules do not generate held-out (converged struct held=%.2f)."%sh
    else: v="MIXED — struct held=%.2f random=%.2f (n_conv=%d/%d)."%(sh,rh,len(conv),len(SEEDS))
    o["verdict"]={"struct_held":sh,"struct_seen":ss,"random_held":rh,"chance":round(chance,5),"n_converged":len(conv),"n_seeds":len(SEEDS),"reading":v}
    json.dump(o,open("result.json","w"),indent=2)
    print("\n=== VERDICT ===\nstruct held=%.3f seen=%.3f (conv %d/%d) | random held=%.3f (chance=%.4f)"%(sh,ss,len(conv),len(SEEDS),rh,chance))
    print("READING:",v)

if __name__=="__main__": main()
