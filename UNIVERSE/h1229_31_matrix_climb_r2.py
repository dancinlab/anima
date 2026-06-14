"""
H_1229/1230/1231 — MATRIX combination-climb ROUND 2 (MODE env, 3 parallel).
Round-1 (H_1225-1228) found: FINAL COMBINATION = regime-dependent ADDITIVE set
(global singleton {SAV-struct} → hard-regime 4-set, no high-order synergy). Round-2
pushes the climb: expand the axis set, change the objective, and test the combination's
own seed-stability. Framework = MATRIX.md §0.

MODE=expanded → H_1229: 11-axis set (round-1 7 + CTX-ent, TOP5-mass, HMEAN, PREValpha).
                Climb on hard (low-structure) tercile. Does the final combination grow
                beyond the round-1 k=4? F1: k* >= 5 with saturation AUROC >= 0.60.
MODE=emit     → H_1230: TARGET = "emit-worthy" = output entropy in TOP tercile (a
                consciousness-relevant tension proxy, NOT correctness). Climb axes
                (entropy EXCLUDED). Does a multi-axis combination AND/OR high-order
                synergy appear for this target? F1: best triple interaction − additive
                >= 0.02 (synergy emerges where it didn't for correctness).
MODE=comboseed→ H_1231: is the FINAL COMBINATION itself a fixed point across seeds?
                Run the hard-regime climb on 3 seeds, take each seed's selected axis-set
                (first 4), measure mean pairwise Jaccard. F1: mean Jaccard >= 0.6
                (the combination recurs = a stable fixed point, not seed-noise).

All: SUPPORTED iff F1; CLOSED-NEGATIVE (a_paper_negative_ok) otherwise. p7, $0, frozen.
toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice. Substrate from H_1142.
"""
import os, math, json, time, random
from itertools import combinations
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

MODE = os.environ.get("MODE", "expanded")
DEV = "cpu"
CORPUS = os.environ.get("CORPUS", "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt")
EN_SLICE_BYTES = 24 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
N_DEC = 4000; HELDOUT_FRAC = 0.10; EPS = 0.005
HMAP = {"expanded":"1229_matrix_climb_expanded","emit":"1230_matrix_climb_emit","comboseed":"1231_matrix_climb_comboseed"}
HID = {"expanded":"H_1229","emit":"H_1230","comboseed":"H_1231"}
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", HMAP[MODE])


class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.ln2 = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, h, batch_first=True)
        s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d))
    def forward(s, x, mask):
        a, _ = s.attn(s.ln1(x), s.ln1(x), s.ln1(x), attn_mask=mask, need_weights=False)
        x = x + a; x = x + s.mlp(s.ln2(x)); return x

class ByteGPT(nn.Module):
    def __init__(s, vocab=VOCAB, d=D, n_layer=NLAYER, n_head=NHEAD, block=BLOCK):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d)
        s.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        s.lnf = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False)
    def forward(s, idx, want_hidden=False):
        T = idx.shape[1]; pos = torch.arange(T, device=idx.device)
        x = s.tok(idx) + s.pos(pos)[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        h = s.lnf(x)
        return (s.head(h), h) if want_hidden else s.head(h)
    def loss_on(s, idx, targets):
        return F.cross_entropy(s(idx).reshape(-1, VOCAB), targets.reshape(-1))


def train_model(data, seed=7):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    g = torch.Generator().manual_seed(seed)
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for gp in opt.param_groups: gp["lr"] = lr_t
        ix = torch.randint(0, data.numel()-BLOCK-1, (BS,), generator=g)
        x = torch.stack([data[i:i+BLOCK] for i in ix]).long().to(DEV)
        y = torch.stack([data[i+1:i+BLOCK+1] for i in ix]).long().to(DEV)
        l = m.loss_on(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 500 == 0 or st == STEPS-1:
            print(f"  [{MODE} s{seed} train] step {st} ce={l.item():.4f}", flush=True)
    m.eval(); return m


def auroc(scores, labels):
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    order = np.argsort(s); ranks = np.empty(len(s), float); ranks[order] = np.arange(1, len(s)+1)
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    rsum = np.zeros(len(cnt)); np.add.at(rsum, inv, ranks); avg = rsum / cnt; ranks = avg[inv]
    n1 = int(y.sum()); n0 = len(y)-n1
    if n1 == 0 or n0 == 0: return float("nan")
    return (ranks[y == 1].sum() - n1*(n1+1)/2)/(n1*n0)


def logreg_auroc(Xtr, ytr, Xte, yte, iters=500, lr=0.4, l2=1e-3):
    if Xtr.ndim == 1: Xtr = Xtr[:,None]; Xte = Xte[:,None]
    mu = Xtr.mean(0); sd = Xtr.std(0)+1e-6; Xtr=(Xtr-mu)/sd; Xte=(Xte-mu)/sd
    n,d = Xtr.shape; w=np.zeros(d); b=0.0
    for _ in range(iters):
        p=1/(1+np.exp(-(Xtr@w+b))); w-=lr*(Xtr.T@(p-ytr)/n+l2*w); b-=lr*float((p-ytr).mean())
    return float(auroc(1/(1+np.exp(-(Xte@w+b))), yte))


def build_trigram(arr):
    a = np.frombuffer(arr, dtype=np.uint8).astype(np.int64)
    keys = a[:-2]*256 + a[1:-1]; nxt = a[2:]
    order = np.argsort(keys, kind="stable"); ks=keys[order]; ns=nxt[order]
    uniq, start = np.unique(ks, return_index=True); starts=list(start)+[len(ks)]
    table={}
    for i,k in enumerate(uniq):
        v=np.bincount(ns[starts[i]:starts[i+1]],minlength=256).astype(np.float64); table[int(k)]=v/v.sum()
    return table


def line_pos_frac(held, pos):
    n=held.numel(); left=pos
    while left>0 and int(held[left-1].item())!=10 and pos-left<400: left-=1
    right=pos
    while right<n-1 and int(held[right].item())!=10 and right-pos<400: right+=1
    span=right-left; return (pos-left)/span if span>0 else 0.5


BASE = ["META-conf","META-ent","META-margin","SAV-struct","SUB-hnorm","EMB-pos","PRIOR-freq"]
EXTRA = ["CTX-ent","TOP5-mass","HMEAN","PREValpha"]

@torch.no_grad()
def collect(m, held, table, byte_freq, expanded=False):
    rng=random.Random(7); n=held.numel(); probs=byte_freq/byte_freq.sum()
    keys = BASE + (EXTRA if expanded else [])
    feats={k:[] for k in keys}; corr=[]; ent_list=[]
    for _ in range(N_DEC):
        pos=rng.randint(BLOCK, n-2)
        ctxb=held[pos-BLOCK:pos]; ctx=ctxb.long()[None].to(DEV)
        tb=int(held[pos].item()); b0=int(held[pos-2].item()); b1=int(held[pos-1].item())
        logits,h=m(ctx, want_hidden=True)
        p=F.softmax(logits[0,-1,:],dim=-1); lp=torch.log(p+1e-12)
        top5=torch.topk(p,5).values; pred=int(torch.argmax(p).item())
        ent=float(-(p*lp).sum().item()); ent_list.append(ent)
        feats["META-conf"].append(float(p.max().item()))
        feats["META-ent"].append(ent)
        feats["META-margin"].append(float((top5[0]-top5[1]).item()))
        v=table.get(b0*256+b1); feats["SAV-struct"].append(0.0 if v is None else float(v[tb]))
        feats["SUB-hnorm"].append(float(h[0,-1,:].norm().item()))
        feats["EMB-pos"].append(line_pos_frac(held,pos))
        feats["PRIOR-freq"].append(float(probs[pred]))
        if expanded:
            cb=ctxb.numpy().astype(np.int64); cc=np.bincount(cb,minlength=256).astype(float); cc=cc/cc.sum()
            feats["CTX-ent"].append(float(-(cc[cc>0]*np.log(cc[cc>0])).sum()))
            feats["TOP5-mass"].append(float(top5.sum().item()))
            feats["HMEAN"].append(float(h[0,-1,:].mean().item()))
            feats["PREValpha"].append(1.0 if (97<=b1<=122 or 65<=b1<=90) else 0.0)
        corr.append(1 if pred==tb else 0)
    return {k:np.array(v) for k,v in feats.items()}, np.array(corr), np.array(ent_list)


def greedy_climb(feats, y, axes, n):
    half=n//2; ytr,yte=y[:half].astype(float),y[half:].astype(float)
    def Xof(sel,sl): return np.stack([feats[a][sl] for a in sel],axis=1)
    chosen,ladder,rem,prev=[],[],list(axes),0.5
    while rem:
        ba,bau=None,-1
        for a in rem:
            au=logreg_auroc(Xof(chosen+[a],slice(0,half)),ytr,Xof(chosen+[a],slice(half,None)),yte)
            if au>bau: bau,ba=au,a
        ladder.append({"k":len(chosen)+1,"added":ba,"auroc":bau,"gain":bau-prev}); chosen.append(ba); rem.remove(ba); prev=bau
    kstar=len(axes); final=list(chosen); sat=ladder[-1]["auroc"]
    for i in range(1,len(ladder)):
        if ladder[i]["gain"]<EPS: kstar=i; final=[ladder[j]["added"] for j in range(i)]; sat=ladder[i-1]["auroc"]; break
    return ladder,kstar,final,sat


def save(v):
    os.makedirs(OUTDIR, exist_ok=True); json.dump(v, open(os.path.join(OUTDIR,"result.json"),"w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


def main():
    print(f"=== {HID[MODE]} MATRIX climb r2 MODE={MODE} ===", flush=True)
    with open(CORPUS,"rb") as f: raw=f.read(EN_SLICE_BYTES)
    data=torch.frombuffer(bytearray(raw),dtype=torch.uint8).clone()
    cut=int(data.numel()*(1-HELDOUT_FRAC)); train_data,held=data[:cut],data[cut:]
    byte_freq=np.bincount(np.frombuffer(raw[:cut],dtype=np.uint8),minlength=256).astype(float)+1.0
    table=build_trigram(raw[:cut])

    if MODE=="expanded":
        m=train_model(train_data,7); feats,corr,_=collect(m,held,table,byte_freq,expanded=True)
        axes=BASE+EXTRA
        struct=feats["SAV-struct"]; q1=np.quantile(struct,1/3); mask=struct<=q1
        sub={a:feats[a][mask] for a in axes}; sc=corr[mask]
        ladder,kstar,final,sat=greedy_climb(sub,sc,axes,len(sc))
        for L in ladder[:8]: print(f"  k={L['k']} +{L['added']:11s} AUROC={L['auroc']:.4f} gain={L['gain']:+.4f}", flush=True)
        f1=(kstar>=5) and (sat>=0.60)
        ruling=(f"SUPPORTED: expanded axis set grows the final combination to k*={kstar} {final} (AUROC {sat:.3f}) — beyond round-1 k=4"
                if f1 else f"CLOSED-NEGATIVE: expanded set did not grow the combination beyond round-1 (k*={kstar}, {final}, AUROC {sat:.3f})")
        save({"H":HID[MODE],"title":"matrix climb r2 — expanded axis set (hard regime)","mode":MODE,"axes":axes,
              "ladder":ladder,"k_star":kstar,"final_combination":final,"saturation_auroc":sat,
              "F1":{"k_star":kstar,"sat":sat,"pass":bool(f1)},"supported":bool(f1),"ruling":ruling,
              "framework":"MATRIX.md §0","scope":"toy ByteGPT (a_scale_honest_scope)","seed":7})

    elif MODE=="emit":
        m=train_model(train_data,7); feats,corr,ent=collect(m,held,table,byte_freq,expanded=False)
        emit=(ent>=np.quantile(ent,2/3)).astype(int)   # emit-worthy = top-tercile entropy
        axes=[a for a in BASE if a!="META-ent"]         # exclude entropy (defines target)
        half=len(emit)//2; ytr,yte=emit[:half].astype(float),emit[half:].astype(float)
        def Xof(sel,sl): return np.stack([feats[a][sl] for a in sel],axis=1)
        ba,badd=None,-1
        for tri in combinations(axes,3):
            au=logreg_auroc(Xof(list(tri),slice(0,half)),ytr,Xof(list(tri),slice(half,None)),yte)
            if au>badd: badd,ba=au,tri
        tri=list(ba)
        def Xint(sl):
            B=Xof(tri,sl); a,b,c=B[:,0],B[:,1],B[:,2]; return np.stack([a,b,c,a*b,a*c,b*c,a*b*c],axis=1)
        inter=logreg_auroc(Xint(slice(0,half)),ytr,Xint(slice(half,None)),yte)
        syn=inter-badd
        print(f"  emit-target best triple {tri} additive={badd:.4f} interaction={inter:.4f} synergy={syn:+.4f}", flush=True)
        f1=syn>=0.02
        ruling=(f"SUPPORTED: emit-worthy target shows HIGH-ORDER SYNERGY — triple {tri} interaction {inter:.3f} vs additive {badd:.3f} (+{syn:.3f}); unlike correctness, the consciousness-relevant target needs non-additive combination"
                if f1 else f"CLOSED-NEGATIVE: emit-worthy target also ADDITIVE — triple {tri} interaction {inter:.3f} vs additive {badd:.3f} (+{syn:.3f}); axes combine additively even for the tension/emit target")
        save({"H":HID[MODE],"title":"matrix climb r2 — emit-worthy target synergy","mode":MODE,"best_triple":tri,
              "additive_auroc":badd,"interaction_auroc":inter,"synergy":syn,
              "F1":{"synergy":syn,"bar":0.02,"pass":bool(f1)},"supported":bool(f1),"ruling":ruling,
              "framework":"MATRIX.md §0","scope":"toy ByteGPT (a_scale_honest_scope)","seed":7})

    else:  # comboseed
        sets=[]; sats=[]
        for sd in [7,17,27]:
            m=train_model(train_data,sd); feats,corr,_=collect(m,held,table,byte_freq,expanded=False)
            struct=feats["SAV-struct"]; q1=np.quantile(struct,1/3); mask=struct<=q1
            sub={a:feats[a][mask] for a in BASE}; sc=corr[mask]
            ladder,kstar,final,sat=greedy_climb(sub,sc,BASE,len(sc))
            top4=set([ladder[j]["added"] for j in range(min(4,len(ladder)))])
            sets.append(top4); sats.append(sat)
            print(f"  seed {sd}: top4={sorted(top4)} sat={sat:.4f}", flush=True)
        jac=[]
        for i in range(len(sets)):
            for j in range(i+1,len(sets)):
                u=len(sets[i]|sets[j]); jac.append(len(sets[i]&sets[j])/u if u else 0.0)
        mj=float(np.mean(jac))
        print(f"  mean pairwise Jaccard(top4 axis-set) = {mj:.4f}", flush=True)
        f1=mj>=0.6
        ruling=(f"SUPPORTED: the final combination is itself a FIXED POINT across seeds — mean Jaccard {mj:.3f} >= 0.6 (the selected axis-set recurs, not seed-noise)"
                if f1 else f"CLOSED-NEGATIVE: the selected combination varies across seeds (Jaccard {mj:.3f} < 0.6) — combination membership is seed-dependent, not a stable fixed point")
        save({"H":HID[MODE],"title":"matrix climb r2 — combination seed-stability","mode":MODE,
              "seed_top4_sets":[sorted(s) for s in sets],"saturation_aurocs":sats,"mean_jaccard":mj,
              "F1":{"mean_jaccard":mj,"bar":0.6,"pass":bool(f1)},"supported":bool(f1),"ruling":ruling,
              "framework":"MATRIX.md §0","scope":"toy ByteGPT 3 seeds (a_scale_honest_scope)","seed":7})
    print("=== DONE", HID[MODE], "===", flush=True)


if __name__ == "__main__":
    main()
