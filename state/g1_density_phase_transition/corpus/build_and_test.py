#!/usr/bin/env python3
"""G1 NEW coverage-designed corpus — build + train + test (owner: 새 코퍼스 만들어서 진행, 2026-07-02).
AI/ML 재조합-일반화 연구. 낡은 corpus co-occurrence 세기 대신, 조합 커버리지를 일부러 설계한 새 자연어 byte
corpus를 만들어 처방을 실측: HIGH-coverage(60% pair) vs LOW-coverage(8% pair) 매칭크기 → byte-GPT 학습 →
held-out 개념쌍 재조합. HIGH>LOW면 조합-커버리지 코퍼스가 G1 lever(NL/byte scale, production-근접). torch DIRECTIONAL."""
import sys,numpy as np,torch,torch.nn as nn,torch.nn.functional as F,json,time,os,itertools
ARCH=sys.argv[1] if len(sys.argv)>1 else "attn"
dev="cuda" if torch.cuda.is_available() else "cpu"; print("device:",dev,"arch:",ARCH,flush=True)
# 30 concrete concept words (keyword = the word itself)
CONCEPTWORDS=["ocean","clock","forest","mirror","engine","garden","signal","ember","glacier","harbor",
 "lantern","meadow","needle","orbit","prism","quartz","river","stone","thunder","umbra",
 "violet","willow","anchor","beacon","cipher","dune","echo","fable","grove","hollow"]
C=CONCEPTWORDS; N=len(C)
VERBS=["merge","echo","dissolve","ignite","weave","fracture","bloom","drift","resonate","collapse"]
RESULTS=["a new pattern forms","meaning shifts","the boundary blurs","something unseen appears",
 "order emerges from noise","the two become one","a hidden path opens","silence answers"]
rng=np.random.default_rng(7)
allpairs=[(a,b) for a in range(N) for b in range(N) if a<b]  # 435 unordered
rng.shuffle(allpairs)
HELD=set(allpairs[:40]); POOL=[p for p in allpairs if p not in HELD]
def sent(a,b,r):
    tmpls=[f"the {C[a]} and the {C[b]} {VERBS[r%len(VERBS)]} until {RESULTS[r%len(RESULTS)]}.",
     f"when {C[a]} meets {C[b]}, {RESULTS[(r+1)%len(RESULTS)]}.",
     f"between the {C[a]} and the {C[b]} a quiet force {VERBS[(r+2)%len(VERBS)]}s.",
     f"{C[a]} remembers {C[b]}; together they {VERBS[(r+3)%len(VERBS)]}."]
    return tmpls[r%len(tmpls)]
def build(cover_frac, target_bytes, seed):
    g=np.random.default_rng(seed); k=int(len(POOL)*cover_frac); pairs=[POOL[i] for i in g.choice(len(POOL),k,replace=False)]
    lines=[]; nb=0; r=0
    while nb<target_bytes:
        a,b=pairs[g.integers(len(pairs))]; s=sent(a,b,int(g.integers(1000))); lines.append(s); nb+=len(s)+1; r+=1
    return "\n".join(lines), len(pairs)
TARGET=1_200_000  # ~1.2MB each, matched
hi_txt,hi_k=build(0.60,TARGET,1); lo_txt,lo_k=build(0.08,TARGET,2)
os.makedirs("corpus",exist_ok=True)
open("corpus/high_coverage.txt","w").write(hi_txt); open("corpus/low_coverage.txt","w").write(lo_txt)
print(f"built: HIGH cover=60% pairs={hi_k} {len(hi_txt)}B | LOW cover=8% pairs={lo_k} {len(lo_txt)}B (matched)",flush=True)
# byte-GPT (production-like, larger than 20x20 toy)
VOCAB=256;BLOCK=128;d=384;NL=6;NH=6
class GPT(nn.Module):
    def __init__(s):
        super().__init__();s.tok=nn.Embedding(VOCAB,d);s.pos=nn.Embedding(BLOCK,d)
        l=nn.TransformerEncoderLayer(d,NH,4*d,batch_first=True,dropout=0.0,activation="gelu")
        s.tr=nn.TransformerEncoder(l,NL);s.ln=nn.LayerNorm(d);s.head=nn.Linear(d,VOCAB,bias=False)
        s.register_buffer("m",torch.triu(torch.ones(BLOCK,BLOCK)*float('-inf'),diagonal=1))
    def forward(s,x):
        T=x.shape[1];h=s.tok(x)+s.pos(torch.arange(T,device=x.device));return s.head(s.ln(s.tr(h,mask=s.m[:T,:T])))

class ConvGPT(nn.Module):  # production-like ConvMoE-L1: single depthwise conv, RF=K (small), no attention
    def __init__(s,K=5,nexp=2):
        super().__init__();s.tok=nn.Embedding(VOCAB,d);s.pos=nn.Embedding(BLOCK,d)
        s.dw=nn.Conv1d(d,d,K,padding=K-1,groups=d)  # causal depthwise, RF=K bytes
        s.experts=nn.ModuleList([nn.Linear(d,d) for _ in range(nexp)]);s.gate=nn.Linear(d,nexp)
        s.ln=nn.LayerNorm(d);s.head=nn.Linear(d,VOCAB);s.K=K
    def forward(s,x):
        T=x.shape[1];h=s.tok(x)+s.pos(torch.arange(T,device=x.device))
        hc=s.dw(h.transpose(1,2))[:,:,:T].transpose(1,2)
        g=F.softmax(s.gate(hc),-1);moe=sum(g[...,i:i+1]*s.experts[i](hc) for i in range(len(s.experts)))
        return s.head(s.ln(h+moe))
def mknet():
    return (ConvGPT().to(dev) if ARCH=="conv" else GPT().to(dev))

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
def gen(net,prompt,n=60,seed=42):
    torch.manual_seed(seed);ids=list(np.frombuffer(prompt.encode("utf-8","surrogateescape"),dtype=np.uint8));base=len(ids)
    for _ in range(n):
        x=torch.tensor([ids[-BLOCK:]],device=dev,dtype=torch.long);lg=net(x)[0,-1]/0.7
        ids.append(int(torch.multinomial(F.softmax(lg,-1),1)))
    return bytes(ids[base:]).decode("utf-8","surrogateescape")
def held_recomb(net,pairs):
    ok=0
    for a,b in pairs:
        g=gen(net,f"the {C[a]} and the {C[b]} ").lower()
        if C[a] in g and C[b] in g: ok+=1  # both concepts surface = recombination
    return ok
t0=time.time();res={}
for tag,txt in [("HIGH_60pct",hi_txt),("LOW_8pct",lo_txt)]:
    net=train(txt);seen_p=[POOL[i] for i in np.random.default_rng(9).choice(len(POOL),20)]
    # seen-sanity: pairs actually in this corpus
    h=held_recomb(net,sorted(HELD)); print(f"[{tag}] held-out recomb={h}/40 ({h/40:.0%})",flush=True)
    res[tag]={"held":h}
hi=res["HIGH_60pct"]["held"];lo=res["LOW_8pct"]["held"]
v=(f"NEW-CORPUS COVERAGE LEVER — HIGH(60%) held={hi}/40 >> LOW(8%) held={lo}/40 at matched size: 조합-커버리지 코퍼스가 NL/byte scale서 G1 held-out 재조합 엶 = 처방 실증(production-근접)." if hi>=lo+8 and hi>=12
   else f"NEW-CORPUS NO COVERAGE EFFECT — HIGH={hi}/40 vs LOW={lo}/40: 매칭크기 NL corpus서 커버리지 효과 미미, 밀도 lever가 NL scale 전이 약함.")
print("\n=== VERDICT ===\n"+v,flush=True)
json.dump({"hi_cover":0.60,"hi_pairs":hi_k,"lo_cover":0.08,"lo_pairs":lo_k,"held_total":40,
 "HIGH_held":hi,"LOW_held":lo,"verdict":v,"mins":round((time.time()-t0)/60,1)},open(f"newcorpus_result_{ARCH}.json","w"),indent=2)
print("=== DONE ===",flush=True)
