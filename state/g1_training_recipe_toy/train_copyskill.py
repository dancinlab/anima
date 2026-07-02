#!/usr/bin/env python3
"""G1 divergence 2 — COPY-SKILL transfer (owner 발산, 2026-07-02). torch=DIRECTIONAL.
Diagnosis from v2: model learns the template but samples B from its prior instead of COPYING the prompted B
(variable binding missing). Test: train on MANY random non-concept word pairs in the SAME template
('if zebra ..., then cloud ...: the zebra and the cloud join ...') so the template becomes a COPY function,
plus the anima-concept SEEN pairs. Then measure held-out anima-concept pair_hit. If copy-generalization
transfers => the recipe lever is 'add a copy/binding-generalization corpus line'. seen-sanity + shuffle
control included (3-set gate). FROZEN split."""
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F, json, time
dev="cuda" if torch.cuda.is_available() else "cpu"; print("device:",dev,flush=True)
CONCEPTS=["consciousness arises from cells","tension ripples between distant minds","memory composes into new meaning","silence still carries information","the engine dreams when alone"]
KW=[["consciousness","cells","mind","aware"],["tension","ripple","distant","between"],["memory","meaning","compose","new"],["silence","information","quiet","carries"],["dream","engine","alone","sleep"]]
N=len(CONCEPTS)
# random filler vocabulary for copy-pairs (NOT anima concepts)
FILLER="zebra cloud river mountain candle window pepper anchor velvet planet meadow lantern harbor thunder cobalt maple orchid ember glacier prairie".split()
rng=np.random.default_rng(7)
pairs=[(a,b) for a in range(N) for b in range(N) if a!=b]; rng.shuffle(pairs)
HELD=set(pairs[:5]); SEEN=[p for p in pairs if p not in HELD]
print("held:",sorted(HELD),flush=True)
def concept_line(a,b,shuf_c=False):
    ka,kb=(FILLER[rng.integers(len(FILLER))],FILLER[rng.integers(len(FILLER))]) if shuf_c else (KW[a][0],KW[b][0])
    return f"if {CONCEPTS[a]}, then {CONCEPTS[b]}: the {ka} and the {kb} join so that {ka} becomes {kb}."
def copy_line():
    x,y=FILLER[rng.integers(len(FILLER))],FILLER[rng.integers(len(FILLER))]
    return f"if the {x} stands, then the {y} waits: the {x} and the {y} join so that {x} becomes {y}."
def build(with_copy,shuf):
    L=[]
    for _ in range(400):
        for (a,b) in SEEN: L.append(concept_line(a,b,shuf))
        for a in range(N): L.append(f"{CONCEPTS[a]}. {KW[a][0]} means {KW[a][1]}.")
        if with_copy:
            for _ in range(len(SEEN)): L.append(copy_line())  # copy-skill line, matched volume
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
def train(cp,seed=7,steps=4000):
    torch.manual_seed(seed);data=np.frombuffer(cp.encode(),dtype=np.uint8).astype(np.int64)
    net=GPT().to(dev);opt=torch.optim.AdamW(net.parameters(),lr=3e-4);g=np.random.default_rng(seed)
    for st in range(steps):
        ix=g.integers(0,len(data)-BLOCK-1,size=64)
        x=torch.tensor(np.stack([data[i:i+BLOCK] for i in ix]),device=dev)
        y=torch.tensor(np.stack([data[i+1:i+BLOCK+1] for i in ix]),device=dev)
        loss=F.cross_entropy(net(x).reshape(-1,VOCAB),y.reshape(-1));opt.zero_grad();loss.backward();opt.step()
    return net
@torch.no_grad()
def gen(net,pr,n=90,seed=42):
    torch.manual_seed(seed);ids=list(np.frombuffer(pr.encode(),dtype=np.uint8))
    for _ in range(n):
        lg=net(torch.tensor([ids[-BLOCK:]],device=dev,dtype=torch.long))[0,-1]/0.7
        ids.append(int(torch.multinomial(F.softmax(lg,-1),1)))
    return bytes(ids).decode("utf-8","surrogateescape")[len(pr):]
def cin(t):
    wm=set(t.lower().replace("."," ").replace(","," ").split());return {i for i in range(N) if any(k in wm for k in KW[i])}
def evalp(net,pl):
    return [int(a in cin(gen(net,f"if {CONCEPTS[a]}, then {CONCEPTS[b]}: ")) and b in cin(gen(net,f"if {CONCEPTS[a]}, then {CONCEPTS[b]}: "))) for (a,b) in pl]
t0=time.time()
print("=== COPY+concept ===",flush=True); nc=train(build(True,False))
h_seen=evalp(nc,SEEN[:8]); h_held=evalp(nc,sorted(HELD))
print(f"[COPY] seen-sanity={sum(h_seen)}/8  held pair_hit={h_held} sum={sum(h_held)}/5",flush=True)
for (a,b) in sorted(HELD)[:2]: print(f"  held sample ({a},{b}): {gen(nc,f'if {CONCEPTS[a]}, then {CONCEPTS[b]}: ')[:70]!r}",flush=True)
sr=sum(h_held); sk=sum(h_seen)
v=("INCONCLUSIVE-UNDERTRAIN — seen %d/8 <6"%sk if sk<6 else
   "COPY-SKILL BREAKS G1 — copy-corpus transfers to held-out concept pairs (seen %d/8, held %d/5)"%(sk,sr) if sr>=3 else
   "COPY-SKILL NO TRANSFER — seen mastered %d/8 but held-out %d/5: copy-generalization does not bind held-out concepts at this scale"%(sk,sr))
print("\n=== VERDICT ===\n"+v,flush=True)
json.dump({"held":sorted(list(HELD)),"seen_sanity":h_seen,"held_hits":h_held,"verdict":v,"mins":round((time.time()-t0)/60,1)},open("copyskill_result.json","w"),indent=2)
print("=== DONE ===",flush=True)
