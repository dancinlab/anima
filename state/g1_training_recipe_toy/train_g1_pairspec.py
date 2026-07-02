#!/usr/bin/env python3
"""G1 training-recipe v2 — PAIR-SPECIFIC metric (fixes non-discriminating coverage, 2026-07-02).
v1 flaw: coverage counted ANY 2 concepts (template echo scores 2 even in shuffle control). v2 metric:
held-out continuation must mention keywords of BOTH the prompted A and B (pair_hit), and we also report
precision = fraction of mentioned concepts that are exactly {A,B}. REAL vs SHUFFLE control. torch=DIRECTIONAL."""
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F, json, time
dev="cuda" if torch.cuda.is_available() else "cpu"
print("device:",dev,flush=True)
CONCEPTS=["consciousness arises from cells","tension ripples between distant minds","memory composes into new meaning","silence still carries information","the engine dreams when alone"]
KW=[["consciousness","cells","mind","aware"],["tension","ripple","distant","between"],["memory","meaning","compose","new"],["silence","information","quiet","carries"],["dream","engine","alone","sleep"]]
N=len(CONCEPTS)
def compose(a,b): return f"the {KW[a][0]} and the {KW[b][0]} join so that {KW[a][0]} becomes {KW[b][0]} together"
TEMPLATES=["if {A}, then {B}: {C}.","when {A}, {B} follows and {C}.","{A}. therefore {B}. {C}.","given {A} and {B}, {C}."]
rng=np.random.default_rng(7)
pairs=[(a,b) for a in range(N) for b in range(N) if a!=b]; rng.shuffle(pairs)
HELD=set(pairs[:5]); SEEN=[p for p in pairs if p not in HELD]
print("held:",sorted(HELD),flush=True)
def build(shuf):
    L=[]
    for _ in range(400):
        for (a,b) in SEEN:
            cc=compose(rng.integers(N),rng.integers(N)) if shuf else compose(a,b)
            L.append(TEMPLATES[rng.integers(4)].format(A=CONCEPTS[a],B=CONCEPTS[b],C=cc))
        for a in range(N): L.append(f"{CONCEPTS[a]}. {KW[a][0]} means {KW[a][1]}.")
    rng.shuffle(L); return "\n".join(L)
VOCAB=256;BLOCK=128;d=256;NL=4;NH=4
class GPT(nn.Module):
    def __init__(s):
        super().__init__();s.tok=nn.Embedding(VOCAB,d);s.pos=nn.Embedding(BLOCK,d)
        l=nn.TransformerEncoderLayer(d,NH,4*d,batch_first=True,dropout=0.0,activation="gelu")
        s.tr=nn.TransformerEncoder(l,NL);s.ln=nn.LayerNorm(d);s.head=nn.Linear(d,VOCAB,bias=False)
        s.register_buffer("m",torch.triu(torch.ones(BLOCK,BLOCK)*float('-inf'),diagonal=1))
    def forward(s,x):
        T=x.shape[1];h=s.tok(x)+s.pos(torch.arange(T,device=x.device));return s.head(s.ln(s.tr(h,mask=s.m[:T,:T])))
def train(cp,seed=7,steps=3000):
    torch.manual_seed(seed);data=np.frombuffer(cp.encode(),dtype=np.uint8).astype(np.int64)
    net=GPT().to(dev);opt=torch.optim.AdamW(net.parameters(),lr=3e-4);g=np.random.default_rng(seed)
    for st in range(steps):
        ix=g.integers(0,len(data)-BLOCK-1,size=64)
        x=torch.tensor(np.stack([data[i:i+BLOCK] for i in ix]),device=dev)
        y=torch.tensor(np.stack([data[i+1:i+BLOCK+1] for i in ix]),device=dev)
        loss=F.cross_entropy(net(x).reshape(-1,VOCAB),y.reshape(-1));opt.zero_grad();loss.backward();opt.step()
    return net
@torch.no_grad()
def gen(net,pr,n=60,seed=42):
    torch.manual_seed(seed);ids=list(np.frombuffer(pr.encode(),dtype=np.uint8))
    for _ in range(n):
        lg=net(torch.tensor([ids[-BLOCK:]],device=dev,dtype=torch.long))[0,-1]/0.7
        ids.append(int(torch.multinomial(F.softmax(lg,-1),1)))
    return bytes(ids).decode("utf-8","surrogateescape")[len(pr):]
def concepts_in(t):
    wm=set(t.lower().replace("."," ").replace(","," ").split())
    return {i for i in range(N) if any(k in wm for k in KW[i])}
def eval_pairs_on(net,tag,pairlist):
    hits=[]
    for (a,b) in pairlist:
        o=gen(net,f"if {CONCEPTS[a]}, then {CONCEPTS[b]}: ",n=90)
        cs=concepts_in(o)
        hits.append(int(a in cs and b in cs))
    return hits

def eval_pair(net,tag):
    hits=[];precs=[];samples=[]
    for (a,b) in sorted(HELD):
        o=gen(net,f"if {CONCEPTS[a]}, then {CONCEPTS[b]}: ",n=90)
        cs=concepts_in(o)
        hit=int(a in cs and b in cs)
        prec=len(cs&{a,b})/max(1,len(cs))
        hits.append(hit);precs.append(round(prec,2));samples.append(o[:70])
    print(f"[{tag}] pair_hit={hits} sum={sum(hits)}/5 precision={precs}",flush=True)
    for s in samples[:2]: print(f"  sample: {s!r}",flush=True)
    return hits,precs
t0=time.time()
print("=== REAL ===",flush=True); nr=train(build(False)); hr,pr_=eval_pair(nr,"REAL")
sr_seen=eval_pairs_on(nr,"REAL-seen",SEEN[:8]); print(f"[REAL] SEEN-pair sanity: {sr_seen} sum={sum(sr_seen)}/8",flush=True)
print("=== SHUFFLE ===",flush=True); ns=train(build(True)); hs,ps=eval_pair(ns,"SHUFFLE")
ss_seen=eval_pairs_on(ns,"SHUF-seen",SEEN[:8]); print(f"[SHUF] SEEN-pair sanity: {ss_seen} sum={sum(ss_seen)}/8",flush=True)
sr,ss=sum(hr),sum(hs)
seen_ok=sum(sr_seen)>=6
if not seen_ok:
    v="INCONCLUSIVE-UNDERTRAIN — REAL seen-pair sanity %d/8 <6: model did not master SEEN pairs, held-out verdict invalid at this scale."%sum(sr_seen)
elif sr>=3 and sr>=ss+2:
    v="TRAINING-RECIPE BREAKS G1 (pair-specific) — seen sanity %d/8 OK, real held %d/5 >> shuffle %d/5."%(sum(sr_seen),sr,ss)
else:
    v="TRUE RECOMBINATION GAP — seen mastered (%d/8) but held-out fails (real %d/5, shuffle %d/5): memorizes pairs, does not recombine."%(sum(sr_seen),sr,ss)
print("\n=== VERDICT ===\n"+v,flush=True)
json.dump({"held":sorted(list(HELD)),"real_hits":hr,"real_prec":pr_,"shuf_hits":hs,"shuf_prec":ps,"real_seen":sr_seen,"shuf_seen":ss_seen,"verdict":v,"mins":round((time.time()-t0)/60,1)},open("pairspec_result.json","w"),indent=2)
print("=== DONE ===",flush=True)
