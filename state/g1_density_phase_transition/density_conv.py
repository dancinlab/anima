#!/usr/bin/env python3
"""G1 밀도 스윕 ConvMoE-L1 CONTROL — disambiguate: 밀도 상전이가 attention 덕인가 밀도 덕인가.
transformer 버전(density_sweep.py)이 20%서 상전이(held 92%). 같은 task를 production-like ConvMoE-L1
(single conv layer, RF-limited, no attention)로 → 상전이 재현되면 밀도 lever(arch 무관), 안되면 attention arch가 원인
(fable G6 RF 발견과 연결). torch DIRECTIONAL."""
import numpy as np,torch,torch.nn as nn,torch.nn.functional as F,json,time
dev="cuda" if torch.cuda.is_available() else "cpu"; print("device:",dev,flush=True)
NC,NS=20,20
allpairs=[(c,s) for c in range(NC) for s in range(NS)]
rng=np.random.default_rng(11); rng.shuffle(allpairs)
HELD=allpairs[:40]; POOL=allpairs[40:]
V=2+NC+NS; PAD,CUE=0,1
def ctok(c): return 2+c
def stok(s): return 2+NC+s
def seq(c,s): return [CUE,ctok(c),stok(s),ctok(c),stok(s)]
T=5
class ConvL1(nn.Module):  # single depthwise-sep conv "expert" layer, RF=K, no attention
    def __init__(s,K=3,nexp=2):
        super().__init__();s.tok=nn.Embedding(V,128);s.pos=nn.Embedding(T,128)
        s.dw=nn.Conv1d(128,128,K,padding=K-1,groups=128)  # causal depthwise, RF=K
        s.experts=nn.ModuleList([nn.Linear(128,128) for _ in range(nexp)])
        s.gate=nn.Linear(128,nexp)
        s.ln=nn.LayerNorm(128);s.head=nn.Linear(128,V);s.K=K
    def forward(s,x,cs=None):
        h=s.tok(x)+s.pos(torch.arange(x.shape[1],device=x.device))
        hc=s.dw(h.transpose(1,2))[:,:,:x.shape[1]].transpose(1,2)  # causal crop
        g=F.softmax(s.gate(hc),-1); moe=sum(g[...,i:i+1]*s.experts[i](hc) for i in range(len(s.experts)))
        return s.head(s.ln(h+moe))
def train(density,seed=11,steps=6000):
    torch.manual_seed(seed);net=ConvL1().to(dev);opt=torch.optim.AdamW(net.parameters(),lr=3e-4)
    g=np.random.default_rng(seed);k=int(len(POOL)*density);tr=[POOL[i] for i in g.choice(len(POOL),k,replace=False)]
    X=torch.tensor([seq(c,s) for c,s in tr],device=dev)
    for st in range(steps):
        idx=g.integers(0,len(tr),size=min(64,len(tr)));x=X[idx]
        lo=net(x[:,:-1]);loss=F.cross_entropy(lo.reshape(-1,V),x[:,1:].reshape(-1))
        opt.zero_grad();loss.backward();opt.step()
    return net,tr
@torch.no_grad()
def held_acc(net,pairs):
    ok=0
    for c,s in pairs:
        cur=[CUE,ctok(c),stok(s)]
        for _ in range(2):
            lg=net(torch.tensor([cur],device=dev))[0,-1];cur.append(int(lg.argmax()))
        if cur[3]==ctok(c) and cur[4]==stok(s): ok+=1
    return ok
t0=time.time();res={}
for dens in [0.05,0.10,0.20,0.40,0.80]:
    net,tr=train(dens);h=held_acc(net,HELD);seen=held_acc(net,tr[:40])
    res[f"d{int(dens*100)}"]={"held":h,"seen":f"{seen}/{min(40,len(tr))}","ntrain":len(tr)}
    print(f"[conv density {int(dens*100)}%] ntrain={len(tr)} seen={seen}/{min(40,len(tr))} held={h}/40 ({h/40:.0%})",flush=True)
hi=res["d80"]["held"];lo=res["d5"]["held"]
if hi>=20 and hi>lo+8: v=f"CONV DENSITY-TRANSITION — held {lo}→{hi}/40: 밀도 lever가 ConvMoE-L1(RF-limited)서도 작동 = arch 무관, 밀도가 진짜 G1 lever. production 처방=조합-커버리지 코퍼스."
elif hi<=4: v=f"CONV DENSITY FLOOR — 80%도 held {hi}/40≈0: ConvMoE-L1은 밀도로도 안 열림 = transformer 상전이는 ATTENTION arch 덕(fable G6 RF 발견과 합류: 벽=RF/arch). 밀도 lever는 attention 전제."
else: v=f"CONV PARTIAL — held {lo}→{hi}/40 약한 단조: ConvMoE서 밀도 효과 약함, arch+밀도 상호작용."
print("\n=== VERDICT ===\n"+v,flush=True)
json.dump({**res,"verdict":v,"mins":round((time.time()-t0)/60,1)},open("density_conv_result.json","w"),indent=2)
print("=== DONE ===",flush=True)
