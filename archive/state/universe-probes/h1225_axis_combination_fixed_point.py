"""
H_1225 — AXIS-COMBINATION CLIMB → FINAL COMBINATION (fixed point in combination-space)
First probe of the overhauled MATRIX framework (MATRIX.md §0): do NOT cap axes at 2D.
Climb the combination order k = 1 → N over real axis-signals and find the FINAL
COMBINATION — the irreducible axis-subset where adding the next axis no longer changes
the result (marginal gain < ε). The fixed point is the COMBINATION itself, not a scalar.

AXES (real per-decision signals on the trained substrate, one per research dimension):
  META-conf   = max softmax prob           (metacognition confidence)
  META-ent    = output entropy             (metacognition uncertainty)
  META-margin = top1 - top2 prob           (metacognition decisiveness)
  SAV-struct  = corpus trigram predictability of true byte  (savant/structure axis)
  SUB-hnorm   = hidden-state lnf L2 norm    (substrate magnitude)
  EMB-pos     = position fraction within text line  (embodiment/time axis)
  PRIOR-freq  = unigram freq of argmax byte (corpus-prior axis)
TARGET = per-item greedy correctness (argmax == true) — "does the combination account
for the substrate's own competence?"

METHOD: greedy forward selection by held-out logistic-probe AUROC. Climb k; at each
step add the axis maximizing held-out AUROC. FINAL COMBINATION = retained set when the
marginal gain drops below EPS.

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 FIXED-POINT-EXISTS — the climb SATURATES at some k* < N (marginal AUROC gain of
                          the next axis < EPS=0.005) → a FINAL COMBINATION exists
                          (irreducible axis-subset; further axes are redundant).
  F2 NON-TRIVIAL        — the final combination has k* >= 2 AND saturation AUROC >= 0.65
                          (a real multi-axis combination, not a single axis or chance).
  H_1225 SUPPORTED iff F1 AND F2 — a non-trivial FINAL COMBINATION fixed point is found.
  CLOSED-NEGATIVE (a_paper_negative_ok) iff no saturation (every axis keeps adding >= EPS
  → WHOLE/irreducible, no finite fixed point) OR k*=1 (no genuine combination).

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice. Substrate from H_1142.
"""
import os, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
DEV = "cpu"
CORPUS = os.environ.get("CORPUS", "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt")
EN_SLICE_BYTES = 24 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
N_DEC = 4000; HELDOUT_FRAC = 0.10; EPS = 0.005
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1225_axis_combination_fixed_point")


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
        if st % 300 == 0 or st == STEPS-1:
            print(f"  [train] step {st} ce={l.item():.4f} {(time.time()-t0)/60:.1f}min", flush=True)
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


@torch.no_grad()
def collect(m, held, table, byte_freq):
    rng = random.Random(SEED); n = held.numel()
    probs = byte_freq/byte_freq.sum()
    feats = {k: [] for k in ["META-conf","META-ent","META-margin","SAV-struct","SUB-hnorm","EMB-pos","PRIOR-freq"]}
    corr = []
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n-2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        tb = int(held[pos].item()); b0 = int(held[pos-2].item()); b1 = int(held[pos-1].item())
        logits, h = m(ctx, want_hidden=True)
        p = F.softmax(logits[0,-1,:], dim=-1)
        lp = torch.log(p+1e-12)
        top2 = torch.topk(p, 2).values
        pred = int(torch.argmax(p).item())
        feats["META-conf"].append(float(p.max().item()))
        feats["META-ent"].append(float(-(p*lp).sum().item()))
        feats["META-margin"].append(float((top2[0]-top2[1]).item()))
        v = table.get(b0*256+b1); feats["SAV-struct"].append(0.0 if v is None else float(v[tb]))
        feats["SUB-hnorm"].append(float(h[0,-1,:].norm().item()))
        feats["EMB-pos"].append(line_pos_frac(held, pos))
        feats["PRIOR-freq"].append(float(probs[pred]))
        corr.append(1 if pred == tb else 0)
    return {k: np.array(v) for k,v in feats.items()}, np.array(corr)


def main():
    print("=== H_1225 axis-combination climb → FINAL COMBINATION ===", flush=True)
    with open(CORPUS,"rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel()*(1-HELDOUT_FRAC)); train_data, held = data[:cut], data[cut:]
    byte_freq = np.bincount(np.frombuffer(raw[:cut],dtype=np.uint8), minlength=256).astype(float)+1.0
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)
    table = build_trigram(raw[:cut]); print(f"[trigram] {len(table)} ctx", flush=True)
    print("--- training ---", flush=True); m = train_model(train_data)
    print("--- collect axis signals ---", flush=True)
    feats, corr = collect(m, held, table, byte_freq)
    AXES = list(feats.keys())
    half = len(corr)//2; ytr, yte = corr[:half].astype(float), corr[half:].astype(float)
    def Xof(sel, sl): return np.stack([feats[a][sl] for a in sel], axis=1)

    # greedy forward selection (climb k)
    chosen, ladder = [], []
    remaining = list(AXES); prev_auroc = 0.5
    while remaining:
        best_a, best_au = None, -1
        for a in remaining:
            sel = chosen+[a]
            au = logreg_auroc(Xof(sel, slice(0,half)), ytr, Xof(sel, slice(half,None)), yte)
            if au > best_au: best_au, best_a = au, a
        gain = best_au - prev_auroc
        ladder.append({"k": len(chosen)+1, "added": best_a, "auroc": best_au, "gain": gain})
        print(f"  k={len(chosen)+1} add {best_a:12s} AUROC={best_au:.4f} gain={gain:+.4f}", flush=True)
        chosen.append(best_a); remaining.remove(best_a); prev_auroc = best_au

    # find fixed point: first k where the NEXT axis's gain < EPS
    kstar = len(AXES); final_combo = list(chosen); sat_auroc = ladder[-1]["auroc"]
    for i in range(1, len(ladder)):
        if ladder[i]["gain"] < EPS:
            kstar = i; final_combo = [ladder[j]["added"] for j in range(i)]; sat_auroc = ladder[i-1]["auroc"]; break

    f1 = kstar < len(AXES)
    f2 = (kstar >= 2) and (sat_auroc >= 0.65)
    supported = bool(f1 and f2)
    if supported:
        ruling = f"SUPPORTED: FINAL COMBINATION fixed point found at k*={kstar} = {final_combo} (saturation AUROC {sat_auroc:.3f}; adding further axes < EPS) — irreducible multi-axis combination"
    elif not f1:
        ruling = "CLOSED-NEGATIVE: no saturation — every axis keeps adding >= EPS → WHOLE/irreducible, no finite combination fixed point (axis-D 'irreducible' echo)"
    else:
        ruling = f"CLOSED-NEGATIVE: trivial — k*={kstar} (single axis or sub-0.65 saturation, no genuine combination)"

    verdict = {
        "H": "H_1225", "title": "axis-combination climb → final combination (fixed point)",
        "axes": AXES, "ladder": ladder,
        "k_star": kstar, "final_combination": final_combo, "saturation_auroc": sat_auroc,
        "full_combo_auroc": ladder[-1]["auroc"], "EPS": EPS,
        "F1_fixed_point_exists": {"k_star": kstar, "N": len(AXES), "pass": bool(f1)},
        "F2_non_trivial": {"k_star": kstar, "sat_auroc": sat_auroc, "pass": bool(f2)},
        "supported": supported, "ruling": ruling,
        "framework": "MATRIX.md §0 N-dimensional axis-combination climb (overhaul 2026-06-15)",
        "scope": "toy ByteGPT d256/4L CPU en slice — UNVERIFIED scale (a_scale_honest_scope)", "seed": SEED,
    }
    print("=== VERDICT ===", flush=True); print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(verdict, open(os.path.join(OUTDIR,"result.json"),"w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
