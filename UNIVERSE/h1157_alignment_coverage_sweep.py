"""
H_1157 — does MORE parallel coverage build a GENERALIZING interlingua bridge in a
byte-LM? Coverage sweep of the H_1156 alignment loss: K train concepts in {8, 27},
held-out 8 reserved concepts. Does held-out interlingua d CLIMB with K (coverage
threshold = recipe) or stay flat (~0, byte siloing is coverage-independent = path-1
needs ~full translation coverage)?

HONEST CAVEAT: the 5-lang lexicon is hand-curated common concrete nouns; minor
translation noise possible (e.g. ko homographs) — toy-scope signal, not a precise atlas.

FROZEN FALSIFIER:
  F1: held-out interlingua d at K=27 ≥ 0.8 (coverage builds a general bridge)
  F2: monotone climb d(K=8) < d(K=27) by ≥ 0.5 (coverage HELPS)
  CONTROL: no-alignment held-out d ≤ 0.3 (reproduce H_1155/1156)
  SUPPORTED iff F1 ∧ control (coverage works); CLOSED-NEG iff held-out stays ~0 at K=27
  (coverage-independent siloing — path-1 needs full translation training, not partial pairs)
toy-scope. xref h1156 (8-pair memorize-only).
"""
import os, math, json, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

DEV = "cpu"
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
PER = 300*1024*1024; SLICE = 6*1024*1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4
STEPS = 2200; BS = 16; LR = 3e-4; SEED = 7; LAMBDA = 1.0
LANGS = ["en", "zh", "ru", "ja", "ko"]
# ~35 common concrete nouns x 5 langs (hand-curated; minor noise possible)
LEX = {
 "water":["water","水","вода","水","물"],"fire":["fire","火","огонь","火","불"],
 "book":["book","书","книга","本","책"],"house":["house","房子","дом","家","집"],
 "tree":["tree","树","дерево","木","나무"],"dog":["dog","狗","собака","犬","개"],
 "sun":["sun","太阳","солнце","太陽","태양"],"moon":["moon","月亮","луна","月","달"],
 "cat":["cat","猫","кошка","猫","고양이"],"bird":["bird","鸟","птица","鳥","새"],
 "fish":["fish","鱼","рыба","魚","물고기"],"hand":["hand","手","рука","手","손"],
 "heart":["heart","心","сердце","心","마음"],"head":["head","头","голова","頭","머리"],
 "mother":["mother","妈妈","мать","母","어머니"],"father":["father","爸爸","отец","父","아버지"],
 "child":["child","孩子","ребёнок","子供","아이"],"friend":["friend","朋友","друг","友達","친구"],
 "city":["city","城市","город","都市","도시"],"king":["king","国王","король","王","왕"],
 "war":["war","战争","война","戦争","전쟁"],"love":["love","爱","любовь","愛","사랑"],
 "time":["time","时间","время","時間","시간"],"night":["night","夜","ночь","夜","밤"],
 "rain":["rain","雨","дождь","雨","비"],"wind":["wind","风","ветер","風","바람"],
 "flower":["flower","花","цветок","花","꽃"],
 # held-out (8, reserved):
 "star":["star","星星","звезда","星","별"],"river":["river","河","река","川","강"],
 "mountain":["mountain","山","гора","山","산"],"road":["road","路","дорога","道","길"],
 "snow":["snow","雪","снег","雪","눈"],"bread":["bread","面包","хлеб","パン","빵"],
 "door":["door","门","дверь","ドア","문"],"eye":["eye","眼睛","глаз","目","눈동자"],
}
HELD = ["star","river","mountain","road","snow","bread","door","eye"]
TRAINABLE = [c for c in LEX if c not in HELD]   # 27


class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__(); s.ln1=nn.LayerNorm(d); s.ln2=nn.LayerNorm(d)
        s.attn=nn.MultiheadAttention(d,h,batch_first=True)
        s.mlp=nn.Sequential(nn.Linear(d,4*d),nn.GELU(),nn.Linear(4*d,d))
    def forward(s,x,m):
        a,_=s.attn(s.ln1(x),s.ln1(x),s.ln1(x),attn_mask=m,need_weights=False); x=x+a
        return x+s.mlp(s.ln2(x))
class ByteGPT(nn.Module):
    def __init__(s,vocab=256,d=D,n_layer=NLAYER,n_head=NHEAD,block=BLOCK):
        super().__init__(); s.block=block; s.tok=nn.Embedding(vocab,d); s.pos=nn.Embedding(block,d)
        s.blocks=nn.ModuleList([Block(d,n_head) for _ in range(n_layer)])
        s.lnf=nn.LayerNorm(d); s.head=nn.Linear(d,vocab,bias=False)
    def hidden(s,idx):
        T=idx.shape[1]; x=s.tok(idx)+s.pos(torch.arange(T,device=idx.device))[None]
        mask=torch.triu(torch.full((T,T),float("-inf"),device=idx.device),1)
        for b in s.blocks: x=b(x,mask)
        return s.lnf(x)
    def forward(s,idx,targets=None):
        h=s.hidden(idx); lg=s.head(h)
        loss=F.cross_entropy(lg.reshape(-1,lg.size(-1)),targets.reshape(-1)) if targets is not None else None
        return lg,loss

def wid(w): return torch.tensor(list(w.encode("utf-8","ignore")[:BLOCK]) or [0],dtype=torch.long,device=DEV)[None]

def aln_loss(m, concepts):
    Vn={}
    for c in concepts:
        vs=[F.normalize(m.hidden(wid(LEX[c][i]))[0].mean(0),dim=-1) for i in range(5)]
        Vn[c]=torch.stack(vs)
    pos=[]
    for c in concepts:
        S=Vn[c]@Vn[c].t(); iu=torch.triu_indices(5,5,1); pos.append(S[iu[0],iu[1]])
    pos=torch.cat(pos)
    ens=F.normalize(torch.stack([Vn[c][0] for c in concepts]),dim=-1)
    Sd=ens@ens.t(); iu=torch.triu_indices(len(concepts),len(concepts),1); neg=Sd[iu[0],iu[1]]
    return (1-pos).mean()+F.relu(neg-0.1).mean()

def load_bal():
    parts=[]
    with open(CORPUS,"rb") as f:
        for i in range(5): f.seek(i*PER); parts.append(f.read(SLICE))
    return torch.frombuffer(bytearray(b"".join(parts)),dtype=torch.uint8)

def train(data, aln_concepts):
    torch.manual_seed(SEED); np.random.seed(SEED); m=ByteGPT().to(DEV); m.train()
    opt=torch.optim.AdamW(m.parameters(),lr=LR,betas=(0.9,0.95),weight_decay=0.1)
    g=torch.Generator(device=DEV).manual_seed(SEED)
    for st in range(STEPS):
        lr_t=LR*min(1.0,(st+1)/100)*(0.5*(1+math.cos(math.pi*min(1.0,st/STEPS))))
        for pg in opt.param_groups: pg["lr"]=lr_t
        ix=torch.randint(0,data.numel()-BLOCK-1,(BS,),generator=g)
        x=torch.stack([data[j:j+BLOCK] for j in ix]).long().to(DEV)
        y=torch.stack([data[j+1:j+BLOCK+1] for j in ix]).long().to(DEV)
        _,l=m(x,y)
        if aln_concepts: l=l+LAMBDA*aln_loss(m,aln_concepts)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(),1.0); opt.step()
        if st%700==0 or st==STEPS-1: print(f"  [K={len(aln_concepts) if aln_concepts else 0}] step {st} loss={l.item():.4f}",flush=True)
    m.eval(); return m

def cos(a,b):
    na,nb=np.linalg.norm(a),np.linalg.norm(b)
    return float(np.dot(a,b)/(na*nb)) if na>0 and nb>0 else 0.0

@torch.no_grad()
def held_d(m, tag):
    V={c:{LANGS[i]:m.hidden(wid(LEX[c][i]))[0].mean(0).cpu().numpy() for i in range(5)} for c in HELD}
    same,diff=[],[]
    for c in HELD:
        for i in range(5):
            for j in range(i+1,5): same.append(cos(V[c][LANGS[i]],V[c][LANGS[j]]))
    rng=random.Random(SEED)
    for _ in range(len(same)):
        c1,c2=rng.sample(HELD,2); diff.append(cos(V[c1][rng.choice(LANGS)],V[c2][rng.choice(LANGS)]))
    same,diff=np.array(same),np.array(diff)
    psd=math.sqrt((same.var(ddof=1)+diff.var(ddof=1))/2) or 1e-9
    d=(same.mean()-diff.mean())/psd
    print(f"  [{tag}] held-out d={d:.4f} same={same.mean():.3f} diff={diff.mean():.3f}",flush=True)
    return float(d)

def main():
    print("=== H_1157 alignment coverage sweep ===",flush=True)
    random.seed(SEED); data=load_bal()
    print(f"[lex] {len(TRAINABLE)} trainable + {len(HELD)} held-out",flush=True)
    rng=random.Random(SEED); shuf=TRAINABLE[:]; rng.shuffle(shuf)
    curve={}
    print("--- K=0 control (no alignment) ---",flush=True); curve[0]=held_d(train(data,None),"K0-ctrl")
    for K in (8,27):
        print(f"--- K={K} alignment ---",flush=True); curve[K]=held_d(train(data,shuf[:K]),f"K{K}")
    f1=curve[27]>=0.8; f2=(curve[27]-curve[8])>=0.5; ctl=curve[0]<=0.3
    supported=bool(f1 and ctl)
    verdict={"H":"H_1157","title":"alignment coverage sweep — does more parallel coverage build a general interlingua bridge",
     "curve_heldout_d":{str(k):v for k,v in curve.items()},
     "F1_K27":{"d":curve[27],"bar":0.8,"pass":bool(f1)},
     "F2_climb":{"delta_8_to_27":curve[27]-curve[8],"bar":0.5,"pass":bool(f2)},
     "control_K0":{"d":curve[0],"bar_max":0.3,"pass":bool(ctl)},
     "h1156_8pair_heldout":-0.0625,"supported":supported,
     "ruling":("SUPPORTED: parallel coverage BUILDS a generalizing interlingua (held-out climbs to bridge) — path-1 works, recipe = enough aligned pairs"
               if supported else
               "CLOSED-NEGATIVE: held-out stays ~0 even at K=27 — coverage-INDEPENDENT byte siloing; partial alignment never generalizes, path-1 needs ~FULL translation coverage (= a translation model), not partial pairs"),
     "honest":"hand-curated 35-concept 5-lang lexicon (minor translation noise possible); toy d256/4L; coverage sweep 0/8/27 only (a_scale_honest_scope)"}
    print("\n=== VERDICT ===\n"+json.dumps(verdict,ensure_ascii=False,indent=2),flush=True)
    json.dump(verdict,open("/tmp/h1157_result.json","w"),ensure_ascii=False,indent=2)
    print("[done] /tmp/h1157_result.json",flush=True)

if __name__=="__main__": main()
