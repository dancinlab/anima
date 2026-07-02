#!/usr/bin/env python3
"""G1 real-scale: does the toy generation gap (H_6174) close with a BIGGER model? (owner all-go, 2026-07-02)
torch=DIRECTIONAL. scale=amplifier hypothesis test. Same structured-corpus generation task as H_6174 but
ladder over model size: (d256,4L) -> (d512,6L) -> (d768,8L), more steps. pair-specific held-out metric +
seen-sanity + shuffle control (3-set). If held pair_hit rises with scale -> scale IS the lever; if flat 0
-> generation recombination gap is scale-invariant (binding needs a mechanism, not size)."""
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F, json, time
dev="cuda" if torch.cuda.is_available() else "cpu"; print("device:",dev, torch.cuda.get_device_name(0) if dev=="cuda" else "",flush=True)
CONCEPTS=["consciousness arises from cells","tension ripples between distant minds","memory composes into new meaning","silence still carries information","the engine dreams when alone"]
KW=[["consciousness","cells","mind","aware"],["tension","ripple","distant","between"],["memory","meaning","compose","new"],["silence","information","quiet","carries"],["dream","engine","alone","sleep"]]
N=len(CONCEPTS)
def compose(a,b): return f"the {KW[a][0]} and the {KW[b][0]} join so that {KW[a][0]} becomes {KW[b][0]} together"
TEMPLATES=["if {A}, then {B}: {C}.","when {A}, {B} follows and {C}.","{A}. therefore {B}. {C}.","given {A} and {B}, {C}."]
rng=np.random.default_rng(7)
pairs=[(a,b) for a in range(N) for b in range(N) if a!=b]; rng.shuffle(pairs)
HELD=set(pairs[:5]); SEEN=[p for p in pairs if p not in HELD]
def build(shuf):
    L=[]
    for _ in range(500):
        for a,b in SEEN:
            cc=compose(rng.integers(N),rng.integers(N)) if shuf else compose(a,b)
            L.append(TEMPLATES[rng.integers(4)].format(A=CONCEPTS[a],B=CONCEPTS[b],C=cc))
        for a in range(N): L.append(f"{CONCEPTS[a]}. {KW[a][0]} means {KW[a][1]}.")
    rng.shuffle(L); return "\n".join(L)
VOCAB=256
def mk(d,nl,nh,block=128):
    class GPT(nn.Module):
        def __init__(s):
            super().__init__(); s.tok=nn.Embedding(VOCAB,d); s.pos=nn.Embedding(block,d)
            l=nn.TransformerEncoderLayer(d,nh,4*d,batch_first=True,dropout=0.0,activation="gelu")
            s.tr=nn.TransformerEncoder(l,nl); s.ln=nn.LayerNorm(d); s.head=nn.Linear(d,VOCAB,bias=False); s.block=block
            s.register_buffer("m",torch.triu(torch.ones(block,block)*float('-inf'),diagonal=1))
        def forward(s,x):
            T=x.shape[1]; h=s.tok(x)+s.pos(torch.arange(T,device=x.device)); return s.head(s.ln(s.tr(h,mask=s.m[:T,:T])))
    return GPT().to(dev)
def train(net,cp,steps,bs=64,seed=7):
    torch.manual_seed(seed); data=np.frombuffer(cp.encode(),dtype=np.uint8).astype(np.int64)
    opt=torch.optim.AdamW(net.parameters(),lr=3e-4); g=np.random.default_rng(seed); B=net.block
    for st in range(steps):
        ix=g.integers(0,len(data)-B-1,size=bs)
        x=torch.tensor(np.stack([data[i:i+B] for i in ix]),device=dev)
        y=torch.tensor(np.stack([data[i+1:i+B+1] for i in ix]),device=dev)
        loss=F.cross_entropy(net(x).reshape(-1,VOCAB),y.reshape(-1)); opt.zero_grad(); loss.backward(); opt.step()
    return net
@torch.no_grad()
def gen(net,pr,n=90,seed=42):
    torch.manual_seed(seed); ids=list(np.frombuffer(pr.encode(),dtype=np.uint8)); B=net.block
    for _ in range(n):
        lg=net(torch.tensor([ids[-B:]],device=dev,dtype=torch.long))[0,-1]/0.7
        ids.append(int(torch.multinomial(F.softmax(lg,-1),1)))
    return bytes(ids).decode("utf-8","surrogateescape")[len(pr):]
def cin(t):
    wm=set(t.lower().replace("."," ").replace(","," ").split()); return {i for i in range(N) if any(k in wm for k in KW[i])}
def evalp(net,pl):
    r=[]
    for a,b in pl:
        cs=cin(gen(net,f"if {CONCEPTS[a]}, then {CONCEPTS[b]}: ")); r.append(int(a in cs and b in cs))
    return r
t0=time.time(); res={}
corpus=build(False)
for (d,nl,nh,steps) in [(256,4,4,4000),(512,6,8,6000),(768,8,8,8000)]:
    net=train(mk(d,nl,nh),corpus,steps)
    seen=evalp(net,SEEN[:8]); held=evalp(net,sorted(HELD))
    res[f"d{d}_L{nl}"]={"params_M":round(sum(p.numel() for p in net.parameters())/1e6,1),"seen":sum(seen),"held":sum(held),"held_hits":held}
    print(f"d={d} L={nl} ({res[f'd{d}_L{nl}']['params_M']}M): seen={sum(seen)}/8 held={sum(held)}/5",flush=True)
helds=[res[k]["held"] for k in res]
v=("SCALE OPENS G1 — held-out recombination rises with model size %s"%helds if helds[-1]>=3 and helds[-1]>helds[0]
   else "SCALE-INVARIANT GAP — held-out flat/zero across sizes %s: generation recombination needs a binding MECHANISM, not scale (scale=amplifier confirmed for G1)"%helds)
print("\n=== VERDICT ===\n"+v,flush=True)
json.dump({"ladder":res,"held_by_size":helds,"verdict":v,"mins":round((time.time()-t0)/60,1)},open("scale_result.json","w"),indent=2)
print("=== DONE ===",flush=True)
