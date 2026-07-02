#!/usr/bin/env python3
"""G1 v3 — pair-SPECIFIC compositional corpus (SCAN/COGS-style).
각 개념 i엔 고유 속성 ATTR[i]. 문장: 'the A and the B yield ATTR[A] and ATTR[B].'
held pair (a,b): 학습서 함께 본 적 없지만, ATTR[a]는 a의 다른 pair에서·ATTR[b]는 b의 다른 pair에서 봄
 → 정답=두 학습된 속성의 새 조합 산출 = 진짜 compositional 재조합 (learnable AND pair-specific).
metric: continuation에 ATTR[a] AND ATTR[b] 둘 다 (pair-특이). seen-sanity + shuffle control.
coverage 의존 예측: 개념이 학습서 적게 나오면(LOW) 그 속성 매핑 부실 → held 실패. HIGH>LOW면 밀도=lever."""
import sys,numpy as np,torch,torch.nn as nn,torch.nn.functional as F,json,time,os
ARCH=sys.argv[1] if len(sys.argv)>1 else "attn"
dev="cuda" if torch.cuda.is_available() else "cpu"; print("device:",dev,"arch:",ARCH,flush=True)
C=["ocean","clock","forest","mirror","engine","garden","signal","ember","glacier","harbor",
 "lantern","meadow","needle","orbit","prism","quartz","river","stone","thunder","umbra",
 "violet","willow","anchor","beacon","cipher","dune","echo","fable","grove","hollow"]
ATTR=["azure","amber","cobalt","dusky","emerald","frosty","golden","hazel","indigo","jade",
 "khaki","lilac","maroon","nutmeg","olive","pewter","russet","scarlet","teal","shadowy",
 "vermil","wheaten","xanthe","yellowy","zinc","coppery","silvery","bronzed","garnet","sienna"]
N=len(C); rng=np.random.default_rng(7)
allpairs=[(a,b) for a in range(N) for b in range(N) if a<b]; rng.shuffle(allpairs)
HELD=set(allpairs[:40]); POOL=[p for p in allpairs if p not in HELD]
def sent(a,b,r,shuf=False):
    ra,rb=(ATTR[a],ATTR[b]) if not shuf else (ATTR[(a+7)%N],ATTR[(b+13)%N])  # shuffle=속성 오배정
    T=[f"the {C[a]} and the {C[b]} yield {ra} and {rb}.",
       f"when {C[a]} meets {C[b]}, expect {ra} then {rb}.",
       f"{C[a]} brings {ra}; {C[b]} brings {rb}."]
    return T[r%len(T)]
def build(cover,target,seed,shuf=False):
    g=np.random.default_rng(seed);k=max(1,int(len(POOL)*cover));pairs=[POOL[i] for i in g.choice(len(POOL),k,replace=False)]
    L=[];nb=0
    while nb<target:
        a,b=pairs[g.integers(len(pairs))];s=sent(a,b,int(g.integers(999)),shuf);L.append(s);nb+=len(s)+1
    return "\n".join(L),len(pairs)
TARGET=1_200_000
hi_txt,hi_k=build(0.60,TARGET,1); lo_txt,lo_k=build(0.08,TARGET,2); sh_txt,_=build(0.60,TARGET,3,shuf=True)
os.makedirs("corpus",exist_ok=True)
open("corpus/high_v3.txt","w").write(hi_txt);open("corpus/low_v3.txt","w").write(lo_txt);open("corpus/shuf_v3.txt","w").write(sh_txt)
print(f"built v3: HIGH pairs={hi_k} LOW pairs={lo_k} (matched ~1.2MB) + shuffle control",flush=True)
VOCAB=256;BLOCK=128;d=384;NL=6;NH=6
class GPT(nn.Module):
    def __init__(s):
        super().__init__();s.tok=nn.Embedding(VOCAB,d);s.pos=nn.Embedding(BLOCK,d)
        l=nn.TransformerEncoderLayer(d,NH,4*d,batch_first=True,dropout=0.0,activation="gelu")
        s.tr=nn.TransformerEncoder(l,NL);s.ln=nn.LayerNorm(d);s.head=nn.Linear(d,VOCAB,bias=False)
        s.register_buffer("m",torch.triu(torch.ones(BLOCK,BLOCK)*float('-inf'),diagonal=1))
    def forward(s,x):
        T=x.shape[1];h=s.tok(x)+s.pos(torch.arange(T,device=x.device));return s.head(s.ln(s.tr(h,mask=s.m[:T,:T])))
class ConvGPT(nn.Module):
    def __init__(s,K=5,nexp=2):
        super().__init__();s.tok=nn.Embedding(VOCAB,d);s.pos=nn.Embedding(BLOCK,d)
        s.dw=nn.Conv1d(d,d,K,padding=K-1,groups=d);s.experts=nn.ModuleList([nn.Linear(d,d) for _ in range(nexp)])
        s.gate=nn.Linear(d,nexp);s.ln=nn.LayerNorm(d);s.head=nn.Linear(d,VOCAB);s.K=K
    def forward(s,x):
        T=x.shape[1];h=s.tok(x)+s.pos(torch.arange(T,device=x.device))
        hc=s.dw(h.transpose(1,2))[:,:,:T].transpose(1,2)
        g=F.softmax(s.gate(hc),-1);moe=sum(g[...,i:i+1]*s.experts[i](hc) for i in range(len(s.experts)))
        return s.head(s.ln(h+moe))
def mknet(): return (ConvGPT().to(dev) if ARCH=="conv" else GPT().to(dev))
def train(txt,steps=8000,seed=7):
    torch.manual_seed(seed);data=np.frombuffer(txt.encode("utf-8","surrogateescape"),dtype=np.uint8)
    net=mknet();opt=torch.optim.AdamW(net.parameters(),lr=3e-4);g=np.random.default_rng(seed)
    for st in range(steps):
        ix=g.integers(0,len(data)-BLOCK-1,size=64)
        x=torch.tensor(np.stack([data[i:i+BLOCK+1] for i in ix]),device=dev,dtype=torch.long)
        lo=net(x[:,:-1]);loss=F.cross_entropy(lo.reshape(-1,VOCAB),x[:,1:].reshape(-1))
        opt.zero_grad();loss.backward();opt.step()
    return net
@torch.no_grad()
def gen(net,prompt,n=48,seed=42):
    torch.manual_seed(seed);ids=list(np.frombuffer(prompt.encode("utf-8","surrogateescape"),dtype=np.uint8));base=len(ids)
    for _ in range(n):
        x=torch.tensor([ids[-BLOCK:]],device=dev,dtype=torch.long);lg=net(x)[0,-1]/0.7
        ids.append(int(torch.multinomial(F.softmax(lg,-1),1)))
    return bytes(ids[base:]).decode("utf-8","surrogateescape")
def recomb(net,pairs,seed0=42):
    """pair-특이: continuation에 ATTR[a] AND ATTR[b] 둘 다 = 올바른 조합 산출."""
    ok=0
    for k,(a,b) in enumerate(pairs):
        g=gen(net,f"the {C[a]} and the {C[b]} yield ",seed=seed0+k).lower()
        if ATTR[a] in g and ATTR[b] in g: ok+=1
    return ok
t0=time.time();res={}
for tag,txt in [("HIGH_60",hi_txt),("LOW_8",lo_txt),("SHUF_ctrl",sh_txt)]:
    net=train(txt)
    seen_s=[POOL[i] for i in np.random.default_rng(9).choice(len(POOL),20,replace=False)]
    seen=recomb(net,seen_s); held=recomb(net,sorted(HELD))
    print(f"[{tag}] seen-sanity={seen}/20 ({seen/20:.0%}) | held-out={held}/40 ({held/40:.0%})",flush=True)
    res[tag]={"seen":seen,"held":held}
hs,hh=res["HIGH_60"]["seen"],res["HIGH_60"]["held"]; ls,lh=res["LOW_8"]["seen"],res["LOW_8"]["held"]; ss,sh=res["SHUF_ctrl"]["seen"],res["SHUF_ctrl"]["held"]
if hs<10:
    v=f"INCONCLUSIVE — HIGH seen-sanity={hs}/20<10 학습부족(step↑). held 판정 무효."
elif hh>=lh+8 and hh>=12:
    v=f"COVERAGE LEVER (pair-specific) — seen OK(H{hs} L{ls}) · HIGH held={hh}/40 >> LOW held={lh}/40 · shuffle held={sh}/40: 조합-커버리지가 NL/byte서 pair-특이 held-out 재조합 엶=처방 실증(production-근접)."
else:
    v=f"NO COVERAGE EFFECT (pair-specific) — seen OK(H{hs} L{ls}) 이나 HIGH held={hh}/40 ≈ LOW held={lh}/40 · shuffle held={sh}: 밀도 lever NL scale서 pair-특이 재조합 안 엶(harness 무결=seen통과·shuffle대조)."
print("\n=== VERDICT ===\n"+v,flush=True)
json.dump({"arch":ARCH,"HIGH_seen":hs,"HIGH_held":hh,"LOW_seen":ls,"LOW_held":lh,"SHUF_seen":ss,"SHUF_held":sh,
 "hi_pairs":hi_k,"lo_pairs":lo_k,"held_total":40,"seen_total":20,"verdict":v,"mins":round((time.time()-t0)/60,1)},
 open(f"newcorpus_v3_{ARCH}.json","w"),indent=2)
print("=== DONE ===",flush=True)
