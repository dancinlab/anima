"""
H_1226/1227/1228 — MATRIX combination-climb, 3 parallel probes (MODE env).
Follow-on to H_1225 (final combination collapsed to singleton {SAV-struct}). Each MODE
trains its own model (parallel-friendly) and emits one verdict. Framework = MATRIX.md §0
(climb k → FINAL COMBINATION fixed point; go beyond 2D).

MODE=residual  → H_1226: FORCE SAV-struct as the k=1 base, then climb the remaining axes.
                 Does any axis add >= EPS BEYOND structure? F1: final combination k* >= 2
                 (structure + >=1 more) with cumulative gain over structure-alone >= 0.02.
MODE=hardtercile→ H_1227: restrict to the LOW-structure (open) tercile where SAV-struct is
                 uninformative; climb all axes. Does a DIFFERENT (non-structure) final
                 combination emerge in this regime? F1: k* >= 2 AND saturation AUROC >= 0.60.
MODE=synergy   → H_1228: does going BEYOND additive (2-way/3-way interaction terms) buy
                 anything? Compare best additive model vs +pairwise-product features.
                 F1: interaction model AUROC - additive AUROC >= 0.02 (genuine synergy).

All: SUPPORTED iff F1; CLOSED-NEGATIVE (a_paper_negative_ok) otherwise. p7, $0, frozen.
toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice. Substrate from H_1142.
"""
import os, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

MODE = os.environ.get("MODE", "residual")
SEED = 7
DEV = "cpu"
CORPUS = os.environ.get("CORPUS", "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt")
EN_SLICE_BYTES = 24 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
N_DEC = 4000; HELDOUT_FRAC = 0.10; EPS = 0.005
HMAP = {"residual": "1226_matrix_climb_residual", "hardtercile": "1227_matrix_climb_hardtercile", "synergy": "1228_matrix_climb_synergy"}
HID = {"residual": "H_1226", "hardtercile": "H_1227", "synergy": "H_1228"}
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
        logits = s(idx)
        return F.cross_entropy(logits.reshape(-1, VOCAB), targets.reshape(-1))


def train_model(data):
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    t0 = time.time()
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for g in opt.param_groups: g["lr"] = lr_t
        ix = torch.randint(0, data.numel() - BLOCK - 1, (BS,))
        x = torch.stack([data[i:i+BLOCK] for i in ix]).long().to(DEV)
        y = torch.stack([data[i+1:i+BLOCK+1] for i in ix]).long().to(DEV)
        l = m.loss_on(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 400 == 0 or st == STEPS-1:
            print(f"  [{MODE} train] step {st} ce={l.item():.4f} {(time.time()-t0)/60:.1f}min", flush=True)
    m.eval(); return m


def auroc(scores, labels):
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    order = np.argsort(s); ranks = np.empty(len(s), float); ranks[order] = np.arange(1, len(s)+1)
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    rsum = np.zeros(len(cnt)); np.add.at(rsum, inv, ranks); avg = rsum / cnt; ranks = avg[inv]
    n1 = int(y.sum()); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return float("nan")
    return (ranks[y == 1].sum() - n1*(n1+1)/2) / (n1*n0)


def logreg_auroc(Xtr, ytr, Xte, yte, iters=500, lr=0.4, l2=1e-3):
    if Xtr.ndim == 1: Xtr = Xtr[:, None]; Xte = Xte[:, None]
    mu = Xtr.mean(0); sd = Xtr.std(0) + 1e-6
    Xtr = (Xtr-mu)/sd; Xte = (Xte-mu)/sd
    n, d = Xtr.shape; w = np.zeros(d); b = 0.0
    for _ in range(iters):
        p = 1/(1+np.exp(-(Xtr@w+b)))
        w -= lr*(Xtr.T@(p-ytr)/n + l2*w); b -= lr*float((p-ytr).mean())
    return float(auroc(1/(1+np.exp(-(Xte@w+b))), yte))


def build_trigram(arr):
    a = np.frombuffer(arr, dtype=np.uint8).astype(np.int64)
    keys = a[:-2]*256 + a[1:-1]; nxt = a[2:]
    order = np.argsort(keys, kind="stable"); ks = keys[order]; ns = nxt[order]
    uniq, start = np.unique(ks, return_index=True); starts = list(start) + [len(ks)]
    table = {}
    for i, k in enumerate(uniq):
        v = np.bincount(ns[starts[i]:starts[i+1]], minlength=256).astype(np.float64)
        table[int(k)] = v / v.sum()
    return table


def line_pos_frac(held, pos):
    n = held.numel(); left = pos
    while left > 0 and int(held[left-1].item()) != 10 and pos-left < 400: left -= 1
    right = pos
    while right < n-1 and int(held[right].item()) != 10 and right-pos < 400: right += 1
    span = right-left
    return (pos-left)/span if span > 0 else 0.5


AXES = ["META-conf","META-ent","META-margin","SAV-struct","SUB-hnorm","EMB-pos","PRIOR-freq"]

@torch.no_grad()
def collect(m, held, table, byte_freq):
    rng = random.Random(SEED); n = held.numel()
    probs = byte_freq/byte_freq.sum()
    feats = {k: [] for k in AXES}; corr = []
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n-2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        tb = int(held[pos].item()); b0 = int(held[pos-2].item()); b1 = int(held[pos-1].item())
        logits, h = m(ctx, want_hidden=True)
        p = F.softmax(logits[0,-1,:], dim=-1); lp = torch.log(p+1e-12)
        top2 = torch.topk(p, 2).values; pred = int(torch.argmax(p).item())
        feats["META-conf"].append(float(p.max().item()))
        feats["META-ent"].append(float(-(p*lp).sum().item()))
        feats["META-margin"].append(float((top2[0]-top2[1]).item()))
        v = table.get(b0*256+b1); feats["SAV-struct"].append(0.0 if v is None else float(v[tb]))
        feats["SUB-hnorm"].append(float(h[0,-1,:].norm().item()))
        feats["EMB-pos"].append(line_pos_frac(held, pos))
        feats["PRIOR-freq"].append(float(probs[pred]))
        corr.append(1 if pred == tb else 0)
    return {k: np.array(v) for k,v in feats.items()}, np.array(corr)


def save(v):
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(v, open(os.path.join(OUTDIR,"result.json"),"w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


def main():
    print(f"=== {HID[MODE]} MATRIX climb MODE={MODE} ===", flush=True)
    with open(CORPUS,"rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel()*(1-HELDOUT_FRAC)); train_data, held = data[:cut], data[cut:]
    byte_freq = np.bincount(np.frombuffer(raw[:cut],dtype=np.uint8), minlength=256).astype(float)+1.0
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)
    table = build_trigram(raw[:cut])
    print("--- training ---", flush=True); m = train_model(train_data)
    print("--- collect ---", flush=True); feats, corr = collect(m, held, table, byte_freq)
    half = len(corr)//2; ytr, yte = corr[:half].astype(float), corr[half:].astype(float)
    def Xof(sel, sl): return np.stack([feats[a][sl] for a in sel], axis=1)

    if MODE == "residual":
        base = ["SAV-struct"]; rem = [a for a in AXES if a != "SAV-struct"]
        base_au = logreg_auroc(Xof(base, slice(0,half)), ytr, Xof(base, slice(half,None)), yte)
        chosen = list(base); ladder = [{"k":1,"added":"SAV-struct","auroc":base_au,"gain":base_au-0.5}]
        prev = base_au
        while rem:
            best_a, best_au = None, -1
            for a in rem:
                au = logreg_auroc(Xof(chosen+[a], slice(0,half)), ytr, Xof(chosen+[a], slice(half,None)), yte)
                if au > best_au: best_au, best_a = au, a
            ladder.append({"k":len(chosen)+1,"added":best_a,"auroc":best_au,"gain":best_au-prev})
            print(f"  k={len(chosen)+1} +{best_a:12s} AUROC={best_au:.4f} gain={best_au-prev:+.4f}", flush=True)
            chosen.append(best_a); rem.remove(best_a); prev = best_au
        cum_gain_over_base = ladder[-1]["auroc"] - base_au
        # k* = first k where adding next < EPS
        kstar = len(AXES); final=list(chosen)
        for i in range(1,len(ladder)):
            if ladder[i]["gain"] < EPS: kstar=i; final=[ladder[j]["added"] for j in range(i)]; break
        f1 = (kstar >= 2) and (cum_gain_over_base >= 0.02)
        ruling = (f"SUPPORTED: combination is GENUINELY >1 — beyond SAV-struct, final={final} adds cum +{cum_gain_over_base:.3f} (k*={kstar})"
                  if f1 else f"CLOSED-NEGATIVE: SAV-struct is sufficient — beyond it no axis adds >= {EPS} (cum gain {cum_gain_over_base:.3f} < 0.02, k*={kstar}); singleton fixed point confirmed")
        save({"H":HID[MODE],"title":"matrix climb — residual (structure-base)","mode":MODE,"base_auroc":base_au,
              "ladder":ladder,"cum_gain_over_base":cum_gain_over_base,"k_star":kstar,"final_combination":final,
              "F1":{"k_star":kstar,"cum_gain":cum_gain_over_base,"pass":bool(f1)},"supported":bool(f1),"ruling":ruling,
              "framework":"MATRIX.md §0","scope":"toy ByteGPT d256/4L CPU en slice (a_scale_honest_scope)","seed":SEED})

    elif MODE == "hardtercile":
        struct = feats["SAV-struct"]; q1 = np.quantile(struct, 1/3)
        mask = struct <= q1
        sub = {a: feats[a][mask] for a in AXES}; sc = corr[mask]
        h2 = len(sc)//2; yt, ye = sc[:h2].astype(float), sc[h2:].astype(float)
        print(f"[hardtercile] n={mask.sum()} acc={sc.mean():.4f}", flush=True)
        def Xs(sel, sl): return np.stack([sub[a][sl] for a in sel], axis=1)
        chosen, ladder, rem, prev = [], [], list(AXES), 0.5
        while rem:
            best_a, best_au = None, -1
            for a in rem:
                au = logreg_auroc(Xs(chosen+[a], slice(0,h2)), yt, Xs(chosen+[a], slice(h2,None)), ye)
                if au > best_au: best_au, best_a = au, a
            ladder.append({"k":len(chosen)+1,"added":best_a,"auroc":best_au,"gain":best_au-prev})
            print(f"  k={len(chosen)+1} +{best_a:12s} AUROC={best_au:.4f} gain={best_au-prev:+.4f}", flush=True)
            chosen.append(best_a); rem.remove(best_a); prev = best_au
        kstar=len(AXES); final=list(chosen); sat=ladder[-1]["auroc"]
        for i in range(1,len(ladder)):
            if ladder[i]["gain"] < EPS: kstar=i; final=[ladder[j]["added"] for j in range(i)]; sat=ladder[i-1]["auroc"]; break
        f1 = (kstar>=2) and (sat>=0.60)
        ruling = (f"SUPPORTED: in the low-structure regime a DIFFERENT multi-axis final combination emerges = {final} (k*={kstar}, AUROC {sat:.3f})"
                  if f1 else f"CLOSED-NEGATIVE: even off-structure no genuine multi-axis combination (k*={kstar}, sat {sat:.3f})")
        save({"H":HID[MODE],"title":"matrix climb — hard (low-structure) tercile","mode":MODE,"n_items":int(mask.sum()),
              "acc":float(sc.mean()),"ladder":ladder,"k_star":kstar,"final_combination":final,"saturation_auroc":sat,
              "F1":{"k_star":kstar,"sat":sat,"pass":bool(f1)},"supported":bool(f1),"ruling":ruling,
              "framework":"MATRIX.md §0","scope":"toy ByteGPT d256/4L CPU en slice (a_scale_honest_scope)","seed":SEED})

    else:  # synergy
        # best additive triple vs same triple + pairwise products
        from itertools import combinations
        best_tri, best_add = None, -1
        for tri in combinations(AXES, 3):
            au = logreg_auroc(Xof(list(tri), slice(0,half)), ytr, Xof(list(tri), slice(half,None)), yte)
            if au > best_add: best_add, best_tri = au, tri
        tri = list(best_tri)
        def Xinter(sl):
            base = Xof(tri, sl)
            a,b,c = base[:,0],base[:,1],base[:,2]
            return np.stack([a,b,c,a*b,a*c,b*c,a*b*c], axis=1)
        inter_au = logreg_auroc(Xinter(slice(0,half)), ytr, Xinter(slice(half,None)), yte)
        synergy = inter_au - best_add
        f1 = synergy >= 0.02
        ruling = (f"SUPPORTED: going beyond additive buys synergy — triple {tri} interaction AUROC {inter_au:.3f} vs additive {best_add:.3f} (+{synergy:.3f}); k>=3 interaction is real"
                  if f1 else f"CLOSED-NEGATIVE: no synergy beyond additive — triple {tri} interaction {inter_au:.3f} vs additive {best_add:.3f} (+{synergy:.3f} < 0.02); axes combine ADDITIVELY, no genuine high-order interaction")
        save({"H":HID[MODE],"title":"matrix climb — 3-way synergy (beyond additive)","mode":MODE,
              "best_triple":tri,"additive_auroc":best_add,"interaction_auroc":inter_au,"synergy":synergy,
              "F1":{"synergy":synergy,"bar":0.02,"pass":bool(f1)},"supported":bool(f1),"ruling":ruling,
              "framework":"MATRIX.md §0","scope":"toy ByteGPT d256/4L CPU en slice (a_scale_honest_scope)","seed":SEED})
    print("=== DONE", HID[MODE], "===", flush=True)


if __name__ == "__main__":
    main()
