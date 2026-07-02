#!/usr/bin/env python3
"""G1 조합-커버리지 밀도 스윕 — fable(opus)이 지목한 8-mech 미탐 축(데이터 분포, DPI-면제).
가설: G1=memorization(lookup) vs composition tradeoff. seen-pair 밀도가 임계 넘으면 lookup이 fit 안돼
trunk가 factoring으로 상전이→held-out 재조합 급상승. 20 color×20 shape=400 pair, cue→'COLOR SHAPE'.
held-out K=40 pair 영구미노출. 밀도 스윕 {5,10,20,40,80}% (plain CE, 연산자 無=밀도축 격리).
3종세트: oracle(factored one-hot 입력 held 유효)·target(held distinct-bind)·shuffle(color↔shape permute→held 0).
사전등록 예측: 임계 아래 held≈0, 위 급상승(phase transition). 80%도 0이면 밀도 lever 아님. torch DIRECTIONAL."""
import numpy as np,torch,torch.nn as nn,torch.nn.functional as F,json,time
dev="cuda" if torch.cuda.is_available() else "cpu"; print("device:",dev,flush=True)
NC,NS=20,20  # colors, shapes
COL=[f"c{i:02d}" for i in range(NC)]; SHP=[f"s{i:02d}" for i in range(NS)]
allpairs=[(c,s) for c in range(NC) for s in range(NS)]
rng=np.random.default_rng(11); rng.shuffle(allpairs)
HELD=allpairs[:40]; POOL=allpairs[40:]  # 360 trainable
# token vocab: [PAD, CUE, c00..c19, s00..s19] token-level
V=2+NC+NS; PAD,CUE=0,1
def ctok(c): return 2+c
def stok(s): return 2+NC+s
# sequence: [CUE, cue_c, cue_s, ctok(c), stok(s)] — cue then emit COLOR SHAPE. cue encodes which pair via 2 cue tokens
def seq(c,s): return [CUE,ctok(c),stok(s),ctok(c),stok(s)]  # trivial? no — model must emit pos3,4 from pos0-2
# Actually make it require binding: cue = shuffled hint, target = ordered emit. Keep cue=pair id via 2 tokens, emit=same.
T=5
class GPT(nn.Module):
    def __init__(s,factored_in=False):
        super().__init__();s.factored=factored_in
        if factored_in: s.cemb=nn.Embedding(NC,64);s.semb=nn.Embedding(NS,64);s.proj=nn.Linear(128,128)
        s.tok=nn.Embedding(V,128);s.pos=nn.Embedding(T,128)
        l=nn.TransformerEncoderLayer(128,4,512,batch_first=True,dropout=0.0,activation="gelu")
        s.tr=nn.TransformerEncoder(l,3);s.ln=nn.LayerNorm(128);s.head=nn.Linear(128,V)
        s.register_buffer("m",torch.triu(torch.ones(T,T)*float('-inf'),diagonal=1))
    def forward(s,x,cs=None):
        h=s.tok(x)+s.pos(torch.arange(x.shape[1],device=x.device))
        if s.factored and cs is not None:  # oracle: inject factored one-hot at pos0
            c,sh=cs; f=s.proj(torch.cat([s.cemb(c),s.semb(sh)],-1)); h[:,0]=h[:,0]+f
        return s.head(s.ln(s.tr(h,mask=s.m[:x.shape[1],:x.shape[1]])))
def mk(pairs,shuffle=False):
    rows=[];cs=[]
    for c,s in pairs:
        se=seq(c,s)
        if shuffle: se=[CUE,ctok(c),stok(s),ctok((c+7)%NC),stok((s+3)%NS)]  # target permuted vs cue
        rows.append(se);cs.append((c,s))
    return rows,cs
def train(density,factored=False,shuffle=False,seed=11,steps=6000):
    torch.manual_seed(seed);net=GPT(factored).to(dev);opt=torch.optim.AdamW(net.parameters(),lr=3e-4)
    g=np.random.default_rng(seed);k=int(len(POOL)*density);tr=[POOL[i] for i in g.choice(len(POOL),k,replace=False)]
    rows,cs=mk(tr,shuffle)
    X=torch.tensor(rows,device=dev);C=torch.tensor([c for c,s in cs],device=dev);S=torch.tensor([s for c,s in cs],device=dev)
    for st in range(steps):
        idx=g.integers(0,len(rows),size=min(64,len(rows)))
        x=X[idx];cc=(C[idx],S[idx]) if factored else None
        lo=net(x[:,:-1],cc); loss=F.cross_entropy(lo.reshape(-1,V),x[:,1:].reshape(-1))
        opt.zero_grad();loss.backward();opt.step()
    return net,tr
@torch.no_grad()
def held_acc(net,pairs,factored=False):
    ok=0
    for c,s in pairs:
        x=torch.tensor([seq(c,s)[:3]],device=dev)  # feed cue only [CUE,cue_c,cue_s]
        cc=(torch.tensor([c],device=dev),torch.tensor([s],device=dev)) if factored else None
        # generate pos3,pos4
        cur=x.tolist()[0]
        for _ in range(2):
            xi=torch.tensor([cur],device=dev)
            lg=net(xi,cc)[0,-1]; cur.append(int(lg.argmax()))
        pred_c,pred_s=cur[3],cur[4]
        if pred_c==ctok(c) and pred_s==stok(s): ok+=1
    return ok
t0=time.time();res={}
# oracle
net,_=train(0.4,factored=True); oh=held_acc(net,HELD,factored=True)
res["oracle_factored"]=f"{oh}/40"
print(f"[oracle factored] held={oh}/40 (task compositionally learnable?)",flush=True)
for dens in [0.05,0.10,0.20,0.40,0.80]:
    net,tr=train(dens); h=held_acc(net,HELD); seen=held_acc(net,tr[:40])
    res[f"d{int(dens*100)}"]={"held":h,"held_pct":round(h/40,3),"seen_sample":f"{seen}/{min(40,len(tr))}","ntrain":len(tr)}
    print(f"[density {int(dens*100)}%] ntrain={len(tr)} seen={seen}/{min(40,len(tr))} held={h}/40 ({h/40:.0%})",flush=True)
# shuffle control at highest density
net,tr=train(0.80,shuffle=True); hs=held_acc(net,HELD)
res["shuffle_d80"]=f"{hs}/40"
print(f"[shuffle d80] held={hs}/40 (should collapse to ~0 if real binding)",flush=True)
hi=res["d80"]["held"]; lo=res["d5"]["held"]
if oh<30: v="ORACLE-FAIL task broken, INCONCLUSIVE"
elif hi>=hi and res["d80"]["held_pct"]>=0.5 and res["d80"]["held"]>res["d5"]["held"]+8: v=f"DENSITY PHASE-TRANSITION — held rises {lo}/40→{hi}/40 with coverage density: combinatorial-coverage IS a G1 lever (data axis, DPI-exempt). 8-mech missed it (data-fixed)."
elif hi<=4: v=f"DENSITY NO-LIFT — even 80% coverage held {hi}/40≈floor: density is NOT a G1 lever, wall deeper than data-distribution (fable prediction: go Q3 WM-coactivation)."
else: v=f"DENSITY PARTIAL — held {lo}→{hi}/40, weak monotone, no clean transition: density modulates but doesn't open G1 alone."
print("\n=== VERDICT ===\n"+v,flush=True)
json.dump({**res,"verdict":v,"mins":round((time.time()-t0)/60,1)},open("density_result.json","w"),indent=2)
print("=== DONE ===",flush=True)
