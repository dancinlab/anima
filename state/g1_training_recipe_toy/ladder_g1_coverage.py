#!/usr/bin/env python3
"""G1 additional divergence: data-coverage LADDER (owner 추가 발산, 2026-07-02). torch=DIRECTIONAL.
How many SEEN concept-pairs does held-out compositional recombination need? Same ByteGPT recipe as the
main run, vary |SEEN| in {4,8,12,16}. held-out = a fixed disjoint 4-pair set. Reveals the corpus
structure requirement (data-scale lever) for the training-recipe G1 break. FROZEN split."""
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F, json, time
dev="cuda" if torch.cuda.is_available() else "cpu"
print("device:",dev, torch.cuda.get_device_name(0) if dev=="cuda" else "",flush=True)
CONCEPTS=["consciousness arises from cells","tension ripples between distant minds","memory composes into new meaning","silence still carries information","the engine dreams when alone","fire consumes the ancient forest","water flows toward the open sea","music bends the shape of time"]
KW=[["consciousness","cells","mind","aware"],["tension","ripple","distant","between"],["memory","meaning","compose","new"],["silence","information","quiet","carries"],["dream","engine","alone","sleep"],["fire","forest","burn","consume"],["water","sea","flow","river"],["music","time","sound","song"]]
N=len(CONCEPTS)
def compose(a,b): return f"the {KW[a][0]} and the {KW[b][0]} join so that {KW[a][0]} becomes {KW[b][0]} together"
TEMPLATES=["if {A}, then {B}: {C}.","when {A}, {B} follows and {C}.","{A}. therefore {B}. {C}.","given {A} and {B}, {C}."]
rng=np.random.default_rng(11)
allpairs=[(a,b) for a in range(N) for b in range(N) if a!=b]; rng.shuffle(allpairs)
HELD=allpairs[:4]; POOL=allpairs[4:]
VOCAB=256;BLOCK=128;d=256;NL=4;NH=4
class GPT(nn.Module):
    def __init__(s):
        super().__init__(); s.tok=nn.Embedding(VOCAB,d);s.pos=nn.Embedding(BLOCK,d)
        l=nn.TransformerEncoderLayer(d,NH,4*d,batch_first=True,dropout=0.0,activation="gelu")
        s.tr=nn.TransformerEncoder(l,NL);s.ln=nn.LayerNorm(d);s.head=nn.Linear(d,VOCAB,bias=False)
        s.register_buffer("m",torch.triu(torch.ones(BLOCK,BLOCK)*float('-inf'),diagonal=1))
    def forward(s,x):
        T=x.shape[1];h=s.tok(x)+s.pos(torch.arange(T,device=x.device));return s.head(s.ln(s.tr(h,mask=s.m[:T,:T])))
def corpus(seen):
    L=[]
    for _ in range(400):
        for(a,b)in seen:
            L.append(TEMPLATES[rng.integers(4)].format(A=CONCEPTS[a],B=CONCEPTS[b],C=compose(a,b)))
        for a in range(N): L.append(f"{CONCEPTS[a]}. {KW[a][0]} means {KW[a][1]}.")
    rng.shuffle(L);return "\n".join(L)
def train(cp,steps=3000,bs=64,seed=7):
    torch.manual_seed(seed);data=np.frombuffer(cp.encode("utf-8","surrogateescape"),dtype=np.uint8).astype(np.int64)
    net=GPT().to(dev);opt=torch.optim.AdamW(net.parameters(),lr=3e-4);g=np.random.default_rng(seed)
    for st in range(steps):
        ix=g.integers(0,len(data)-BLOCK-1,size=bs)
        x=torch.tensor(np.stack([data[i:i+BLOCK] for i in ix]),device=dev)
        y=torch.tensor(np.stack([data[i+1:i+BLOCK+1] for i in ix]),device=dev)
        loss=F.cross_entropy(net(x).reshape(-1,VOCAB),y.reshape(-1));opt.zero_grad();loss.backward();opt.step()
    return net
@torch.no_grad()
def cov_held(net):
    def gen(pr,n=60):
        torch.manual_seed(42);ids=list(np.frombuffer(pr.encode("utf-8","surrogateescape"),dtype=np.uint8))
        for _ in range(n):
            lg=net(torch.tensor([ids[-BLOCK:]],device=dev,dtype=torch.long))[0,-1]/0.7
            ids.append(int(torch.multinomial(F.softmax(lg,-1),1)))
        return bytes(ids).decode("utf-8","surrogateescape")[len(pr):]
    def cov(t):
        wm=set(t.lower().replace("."," ").replace(","," ").split());return sum(1 for k in KW if any(x in wm for x in k))
    return [cov(gen(f"if {CONCEPTS[a]}, then {CONCEPTS[b]}: ")) for(a,b)in HELD]
t0=time.time();res={}
for K in [4,8,12,16]:
    seen=POOL[:K];c=cov_held(train(corpus(seen)))
    res[K]={"cov":c,"mean":round(float(np.mean(c)),2)}
    print(f"|SEEN|={K}: held cov={c} mean={np.mean(c):.2f}",flush=True)
print("\n=== LADDER ===")
for K in [4,8,12,16]: print(f"  {K} pairs -> held mean {res[K]['mean']}")
json.dump({"held":HELD,"ladder":res,"mins":round((time.time()-t0)/60,1)},open("ladder_result.json","w"),indent=2)
print("=== DONE ===",flush=True)
