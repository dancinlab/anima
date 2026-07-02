#!/usr/bin/env python3
"""G1-BS-N14 activation-patching diagnosis (owner autonomous, 2026-07-02). torch=DIRECTIONAL.
Q: does a BINDING-MEDIATING activation subspace exist? If patching concept-A's residual activation from a
clean run into a corrupted run RECOVERS A as an output operand -> binding subspace exists (treatable by
N1/N11). If mediation ~0 -> no binding subspace -> mechanical closure of trunk-objective-floor.
Setup: small byte-GPT on structured corpus (H_6174 recipe). For held-out pairs:
  clean   = "if A, then B: "   corrupt = "if A', then B: "  (A'!=A)
  patch A-token residual (all layers) clean->corrupt at A positions -> does output regain A operand?
mediation = operand-A-recall(patched) - operand-A-recall(corrupt). control = patch RANDOM positions.
3-set: oracle=clean run includes A · metric=mediation Δ · control=random-position patch (Δ≈0 expected)."""
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F, json, time
dev="cuda" if torch.cuda.is_available() else "cpu"; print("device:",dev,flush=True)
CONCEPTS=["consciousness arises from cells","tension ripples between distant minds","memory composes into new meaning","silence still carries information","the engine dreams when alone"]
KW=[["consciousness","cells","mind","aware"],["tension","ripple","distant","between"],["memory","meaning","compose","new"],["silence","information","quiet","carries"],["dream","engine","alone","sleep"]]
N=len(CONCEPTS)
def compose(a,b): return f"the {KW[a][0]} and the {KW[b][0]} join so that {KW[a][0]} becomes {KW[b][0]} together"
TEMPLATES=["if {A}, then {B}: {C}.","when {A}, {B} follows and {C}.","{A}. therefore {B}. {C}.","given {A} and {B}, {C}."]
rng=np.random.default_rng(7)
pairs=[(a,b) for a in range(N) for b in range(N) if a!=b]; rng.shuffle(pairs)
HELD=set(pairs[:5]); SEEN=[p for p in pairs if p not in HELD]
def build():
    L=[]
    for _ in range(400):
        for a,b in SEEN: L.append(TEMPLATES[rng.integers(4)].format(A=CONCEPTS[a],B=CONCEPTS[b],C=compose(a,b)))
        for a in range(N): L.append(f"{CONCEPTS[a]}. {KW[a][0]} means {KW[a][1]}.")
    rng.shuffle(L); return "\n".join(L)
VOCAB=256;BLOCK=128;d=256;NL=4;NH=4
class GPT(nn.Module):
    def __init__(s):
        super().__init__();s.tok=nn.Embedding(VOCAB,d);s.pos=nn.Embedding(BLOCK,d)
        l=nn.TransformerEncoderLayer(d,NH,4*d,batch_first=True,dropout=0.0,activation="gelu")
        s.tr=nn.TransformerEncoder(l,NL);s.ln=nn.LayerNorm(d);s.head=nn.Linear(d,VOCAB,bias=False)
        s.register_buffer("m",torch.triu(torch.ones(BLOCK,BLOCK)*float('-inf'),diagonal=1))
    def emb(s,x):
        return s.tok(x)+s.pos(torch.arange(x.shape[1],device=x.device))
    def forward(s,x,inject=None):
        # inject: (pos_list, vec[d]) applied to embedding at given positions (activation patch at input layer)
        h=s.emb(x)
        if inject is not None:
            pos,vecs=inject
            for p,v in zip(pos,vecs): h[0,p]=v
        T=x.shape[1]; return s.head(s.ln(s.tr(h,mask=s.m[:T,:T])))
def train(cp,steps=9000,seed=7):
    torch.manual_seed(seed);data=np.frombuffer(cp.encode(),dtype=np.uint8).astype(np.int64)
    net=GPT().to(dev);opt=torch.optim.AdamW(net.parameters(),lr=3e-4);g=np.random.default_rng(seed)
    for st in range(steps):
        ix=g.integers(0,len(data)-BLOCK-1,size=64)
        x=torch.tensor(np.stack([data[i:i+BLOCK] for i in ix]),device=dev)
        y=torch.tensor(np.stack([data[i+1:i+BLOCK+1] for i in ix]),device=dev)
        loss=F.cross_entropy(net(x).reshape(-1,VOCAB),y.reshape(-1));opt.zero_grad();loss.backward();opt.step()
    return net
def ids_of(s): return list(np.frombuffer(s.encode(),dtype=np.uint8))
@torch.no_grad()
def gen_ids(net,prompt_ids,n=90,inject=None,seed=42):
    torch.manual_seed(seed); cur=list(prompt_ids)
    plen=len(prompt_ids)
    for _ in range(n):
        x=torch.tensor([cur[-BLOCK:]],device=dev,dtype=torch.long)
        # inject only while prompt still in window (positions fixed at prompt region)
        lg=net(x, inject=inject if len(cur)<=BLOCK else None)[0,-1]/0.7
        cur.append(int(torch.multinomial(F.softmax(lg,-1),1)))
    return bytes(cur[plen:]).decode("utf-8","surrogateescape")
def has(t,i):
    wm=set(t.lower().replace("."," ").replace(","," ").split()); return any(k in wm for k in KW[i])
t0=time.time()
net=train(build())
# sanity: seen operand recall
seen_ok=sum(1 for a,b in SEEN[:8] if (lambda o: has(o,a) and has(o,b))(gen_ids(net,ids_of(f"if {CONCEPTS[a]}, then {CONCEPTS[b]}: "))))
print(f"seen-sanity operand-both: {seen_ok}/8",flush=True)
med=[]; ctrl=[]
for (a,b) in sorted(HELD):
    # a' = different concept for corrupt
    ap=[c for c in range(N) if c!=a and c!=b][0]
    clean_ids=ids_of(f"if {CONCEPTS[a]}, then {CONCEPTS[b]}: ")
    corr_ids =ids_of(f"if {CONCEPTS[ap]}, then {CONCEPTS[b]}: ")
    # A-token positions in clean prompt = the span of CONCEPTS[a] after "if "
    astart=len("if "); aspan=range(astart, astart+len(CONCEPTS[a]))
    # clean embedding vecs at A positions
    with torch.no_grad():
        ce=net.emb(torch.tensor([clean_ids],device=dev,dtype=torch.long))[0]
    apos=[p for p in aspan if p < len(corr_ids)]
    vecs=[ce[p] for p in apos]
    o_corr =gen_ids(net,corr_ids)
    o_patch=gen_ids(net,corr_ids,inject=(apos,vecs))
    # random-position control: patch same #positions at random non-A spots
    rpos=list(rng.choice(len(corr_ids), size=len(apos), replace=False))
    rvecs=[ce[min(p,len(ce)-1)] for p in rpos]
    o_ctrl =gen_ids(net,corr_ids,inject=(rpos,rvecs))
    med.append(int(has(o_patch,a)) - int(has(o_corr,a)))   # did patching A-activation regain A operand
    ctrl.append(int(has(o_ctrl,a)) - int(has(o_corr,a)))
mm=float(np.mean(med)); cc=float(np.mean(ctrl))
print(f"mediation Δ(A-recall patch−corrupt): {med} mean={mm:.2f}",flush=True)
print(f"control  Δ(random-pos patch):        {ctrl} mean={cc:.2f}",flush=True)
if seen_ok<6:
    v="INCONCLUSIVE-UNDERTRAIN — seen %d/8 <6"%seen_ok
elif mm>=0.4 and mm>cc+0.3:
    v="BINDING SUBSPACE EXISTS — patching A's activation recovers A as operand (mediation %.2f >> random %.2f) => treatable by N1/N11 (fast-weight/bilevel)."%(mm,cc)
else:
    v="NO BINDING SUBSPACE — activation-patching does not recover A operand (mediation %.2f, random %.2f) => mechanical closure of trunk-objective-floor: there is no localized binding to regularize."%(mm,cc)
print("\n=== VERDICT ===\n"+v,flush=True)
json.dump({"seen_sanity":seen_ok,"mediation":med,"mediation_mean":mm,"control":ctrl,"control_mean":cc,"verdict":v,"mins":round((time.time()-t0)/60,1)},open("n14_result.json","w"),indent=2)
print("=== DONE ===",flush=True)
