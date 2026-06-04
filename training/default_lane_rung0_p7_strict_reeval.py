#!/usr/bin/env python3
"""p7_strict_reeval.py — STRICTER p7 simple-stack re-evaluator (anti-Goodhart fix).

The rung-0 train run's p7 evaluator was GAMEABLE: a random-init mirror scored 5/5
because Python str.isprintable() counts random high-Unicode + ASCII-symbol soup as
"printable", so printable_ratio>=0.6 let pure garbage through. This re-evaluator adds
a REAL-TEXT discriminator that random bytes fail, run on the SAME saved ckpt + a fresh
random-init mirror (seed+1000, identical to the trainer). NO retrain — re-eval only.

STRICT real-text gate (p7 simple-stack, still NOT perplexity — pure structural checks):
  (1) non-empty (>= 8 chars after stop-trim)
  (2) C0-control ratio < 0.02   — real text has ~no control bytes; random bytes have many
  (3) letter-or-space ratio >= 0.65  — real prose/dialogue is mostly letters+space;
      letters = unicodedata category L* (Latin/Hangul/accented) OR ASCII space/.,!?'-
  (4) not a degenerate single-char repeat (most-common < 0.6)
  (5) longest run of NON-letter/space chars <= 4  — random soup has long symbol runs
Overall PASS iff >= 4/5 prompts pass. Anti-Goodhart: mirror MUST FAIL.
"""
import json, math, sys, unicodedata
from pathlib import Path
import torch, torch.nn as nn, torch.nn.functional as F

# ---- arch (identical to default_lane_rung0_train_eval.py) ----
class EngineAGFFN(nn.Module):
    def __init__(self, d, hm=4, dr=0.0):
        super().__init__(); h=d*hm
        self.engine_a=nn.Sequential(nn.Linear(d,h),nn.GELU(),nn.Dropout(dr),nn.Linear(h,d))
        self.engine_g=nn.Sequential(nn.Linear(d,h),nn.GELU(),nn.Dropout(dr),nn.Linear(h,d))
    def forward(self,x): return self.engine_a(x)-self.engine_g(x)
class CausalSelfAttention(nn.Module):
    def __init__(self,d,nh,bs,dr=0.0):
        super().__init__(); assert d%nh==0; self.n_head=nh; self.head_dim=d//nh
        self.c_attn=nn.Linear(d,3*d); self.c_proj=nn.Linear(d,d)
        self.register_buffer("bias",torch.tril(torch.ones(bs,bs)).view(1,1,bs,bs))
    def forward(self,x):
        B,T,C=x.shape; q,k,v=self.c_attn(x).split(C,dim=2)
        q=q.view(B,T,self.n_head,self.head_dim).transpose(1,2)
        k=k.view(B,T,self.n_head,self.head_dim).transpose(1,2)
        v=v.view(B,T,self.n_head,self.head_dim).transpose(1,2)
        att=(q@k.transpose(-2,-1))/math.sqrt(self.head_dim)
        att=att.masked_fill(self.bias[:,:,:T,:T]==0,float("-inf"))
        att=F.softmax(att,dim=-1); y=att@v
        y=y.transpose(1,2).contiguous().view(B,T,C); return self.c_proj(y),att.detach().mean().item()
class Block(nn.Module):
    def __init__(self,d,nh,bs,dr=0.0):
        super().__init__(); self.ln1=nn.LayerNorm(d); self.attn=CausalSelfAttention(d,nh,bs,dr)
        self.ln2=nn.LayerNorm(d); self.ffn=EngineAGFFN(d,4,dr)
    def forward(self,x):
        a,t=self.attn(self.ln1(x)); x=x+a; x=x+self.ffn(self.ln2(x)); return x,t
class ConsciousLMReconstructed(nn.Module):
    def __init__(self,vs=256,d=384,nh=4,nl=6,bs=256,dr=0.0):
        super().__init__(); self.block_size=bs
        self.tok_emb=nn.Embedding(vs,d); self.pos_emb=nn.Embedding(bs,d)
        self.blocks=nn.ModuleList([Block(d,nh,bs,dr) for _ in range(nl)])
        self.ln_f=nn.LayerNorm(d); self.head_a=nn.Linear(d,vs,bias=False); self.head_g=nn.Linear(d,vs,bias=False)
    def forward(self,idx):
        B,T=idx.shape; x=self.tok_emb(idx)+self.pos_emb(torch.arange(T,device=idx.device))
        for blk in self.blocks: x,_=blk(x)
        x=self.ln_f(x); return self.head_a(x),self.head_g(x)

STOP_STRINGS=("\nuser:","\nUser:","user:")
@torch.no_grad()
def generate(model,prompt,max_new,device,temperature=0.8,top_k=40,rep_penalty=1.1):
    model.eval(); ids=list(prompt.encode("utf-8"))[-model.block_size:]
    idx=torch.tensor([ids],dtype=torch.long,device=device); out=[]
    for _ in range(max_new):
        la,lg=model(idx[:,-model.block_size:]); logits=0.5*la[:,-1,:]+0.5*lg[:,-1,:]
        for b in set(out[-32:]): logits[0,b]/=rep_penalty
        logits=logits/temperature
        if top_k:
            v,_=torch.topk(logits,top_k); logits[logits<v[:,[-1]]]=float("-inf")
        p=F.softmax(logits,dim=-1); nb=torch.multinomial(p,1).item(); out.append(nb)
        idx=torch.cat([idx,torch.tensor([[nb]],device=device)],dim=1)
        tail=bytes(out).decode("utf-8",errors="ignore")
        if any(s in tail for s in STOP_STRINGS): break
    text=bytes(out).decode("utf-8",errors="ignore")
    for s in STOP_STRINGS:
        i=text.find(s)
        if i>=0: text=text[:i]
    return text.strip()

PROBES=[("dialogue-en","user: Today's feed is so pretty, I had to comment.\n"),
        ("dialogue-ko","user: 오늘 정말 행복한 하루였어요.\n"),
        ("dialogue-fr","user: Je me sens un peu fatigué aujourd'hui.\n"),
        ("prose-de","Die Stille des Morgens "),
        ("prose-es","El sentido de la conciencia ")]

ALLOWED_PUNC=set(" .,!?'\"-:;()…\n\t")
def is_textchar(c):
    if c in ALLOWED_PUNC: return True
    cat=unicodedata.category(c)
    return cat[0]=="L"  # any letter (Latin/Hangul/accented/CJK)

def strict_checks(reply):
    non_empty=len(reply)>=8
    c0=sum(1 for c in reply if ord(c)<32 and c not in "\n\t")
    c0_ratio=c0/max(1,len(reply))
    no_control=c0_ratio<0.02
    tcount=sum(1 for c in reply if is_textchar(c))
    text_ratio=tcount/max(1,len(reply))
    mostly_text=text_ratio>=0.65
    from collections import Counter
    mc=(Counter(reply).most_common(1)[0][1]/len(reply)) if reply else 1.0
    not_degenerate=mc<0.6
    # longest run of non-text chars
    longest=run=0
    for c in reply:
        if is_textchar(c): run=0
        else: run+=1; longest=max(longest,run)
    no_soup=longest<=4
    ok=non_empty and no_control and mostly_text and not_degenerate and no_soup
    return ok,{"non_empty":non_empty,"c0_ratio":round(c0_ratio,3),"text_ratio":round(text_ratio,3),
               "not_degenerate":not_degenerate,"longest_nontext_run":longest}

def evaluate(model,device,label):
    res=[]
    for kind,seed in PROBES:
        rep=generate(model,seed,120,device)
        ok,d=strict_checks(rep)
        res.append({"kind":kind,"seed":seed,"reply":rep,"ok":ok,**d})
    npass=sum(1 for r in res if r["ok"])
    return {"label":label,"n_pass":npass,"n_total":len(PROBES),
            "verdict":"PASS" if npass>=4 else "FAIL","turns":res}

def main():
    ckpt=sys.argv[1]; seed=42; device="cuda" if torch.cuda.is_available() else "cpu"
    blob=torch.load(ckpt,map_location=device); cfg=blob["config"]
    def build(): return ConsciousLMReconstructed(256,cfg["dim"],cfg["heads"],cfg["layers"],cfg["block_size"]).to(device)
    torch.manual_seed(seed)
    m=build(); m.load_state_dict(blob["model_state"]); 
    tr=evaluate(m,device,"trained")
    torch.manual_seed(seed+1000)  # identical mirror seed to trainer
    mir=build(); mr=evaluate(mir,device,"random_init_mirror")
    out={"evaluator":"p7-strict-v2 (C0-control<0.02 + text-ratio>=0.65 + no-soup-run<=4)",
         "trained":{"verdict":tr["verdict"],"n_pass":tr["n_pass"]},
         "random_init_mirror":{"verdict":mr["verdict"],"n_pass":mr["n_pass"]},
         "anti_goodhart_ok":(tr["verdict"]=="PASS" and mr["verdict"]=="FAIL"),
         "chat_pass":(tr["verdict"]=="PASS" and mr["verdict"]=="FAIL")}
    print("=== p7-STRICT TRAINED ===")
    for r in tr["turns"]: print(f"[{r['kind']}] ok={r['ok']} c0={r['c0_ratio']} text={r['text_ratio']} run={r['longest_nontext_run']}\n  SEED: {r['seed'].rstrip()}\n  -> {r['reply']}")
    print("\n=== p7-STRICT RANDOM-INIT MIRROR (MUST FAIL) ===")
    for r in mr["turns"]: print(f"[{r['kind']}] ok={r['ok']} c0={r['c0_ratio']} text={r['text_ratio']} run={r['longest_nontext_run']}\n  SEED: {r['seed'].rstrip()}\n  -> {r['reply']}")
    print("\n=== STRICT SUMMARY ==="); print(json.dumps(out,ensure_ascii=False,indent=2))
    Path("out/p7_strict_trained.json").write_text(json.dumps(tr,ensure_ascii=False,indent=2))
    Path("out/p7_strict_mirror.json").write_text(json.dumps(mr,ensure_ascii=False,indent=2))
    Path("out/summary_strict.json").write_text(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
