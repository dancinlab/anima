"""
H_1206 — METACOGNITION CAPSTONE (neuroscience campaign synthesis)
One model, one decision-grade verdict that ties the H_1202-1216 campaign together.
The campaign's unifying account: metacognition in this substrate is REAL (output-
level type-2 sensitivity) but FLAT (no separable representational module), COUPLED
to competence, and COARSE (difficulty-level, not fine error-level). H_1206
pre-registers this COMPOUND claim and tests all three decisive legs on ONE model.

Legs (all on the same trained ByteGPT, same decision points):
  COARSE-REAL  — 2AFC type-2 AUROC(confidence ; own correctness)   [H_1202]
  FINE-ABSENT  — hidden-state linear probe for own single-byte error [H_1203/1204]
  COUPLED      — type-2 AUROC in high-skill (rote) vs low-skill (open) tercile [H_1207]

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 COARSE-REAL  — type-2 AUROC >= 0.65 (output-level metacognition is real)
  F2 FINE-ABSENT  — hidden-state error-probe AUROC <= 0.62 (NO fine representational
                    monitor — held-out logistic probe near chance)
  F3 COUPLED      — type2_AUROC(high-skill tercile) - type2_AUROC(low-skill) >= +0.10
                    (metacognition tracks competence, not a domain-general module)
  H_1206 SUPPORTED iff F1 AND F2 AND F3 — the REAL/FLAT/COUPLED/COARSE account holds
  as a single decision-grade synthesis.
  CLOSED-NEGATIVE (a_paper_negative_ok) if any leg flips (e.g. fine probe succeeds =>
  there IS a representational module => account falsified).

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice. Substrate from H_1142.
"""
import os, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"
CORPUS = os.environ.get("CORPUS", "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt")
EN_SLICE_BYTES = 24 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
N_DEC = 3000; HELDOUT_FRAC = 0.10
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1206_metacog_capstone")


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


def batch(data):
    ix = torch.randint(0, data.numel() - BLOCK - 1, (BS,))
    x = torch.stack([data[i:i+BLOCK] for i in ix]).long()
    y = torch.stack([data[i+1:i+BLOCK+1] for i in ix]).long()
    return x.to(DEV), y.to(DEV)


def train_model(data):
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    t0 = time.time()
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for g in opt.param_groups: g["lr"] = lr_t
        x, y = batch(data)
        l = m.loss_on(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 250 == 0 or st == STEPS-1:
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


def logreg_auroc(Xtr, ytr, Xte, yte, iters=400, lr=0.5, l2=1e-3):
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


@torch.no_grad()
def collect(m, held, table, byte_freq):
    rng = random.Random(SEED); n = held.numel()
    bytes_pool = np.arange(256); probs = byte_freq / byte_freq.sum()
    npr = np.random.RandomState(SEED + 99)
    conf2afc, corr2afc, pred = [], [], []     # 2AFC margin + correctness + trigram-predictability
    Herr, Yerr = [], []                        # hidden-state + single-byte-error label
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - 2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        tb = int(held[pos].item()); b0 = int(held[pos-2].item()); b1 = int(held[pos-1].item())
        logits, h = m(ctx, want_hidden=True)
        p = F.softmax(logits[0, -1, :], dim=-1)
        # 2AFC: true vs unigram foil
        foil = int(npr.choice(bytes_pool, p=probs))
        while foil == tb: foil = int(npr.choice(bytes_pool, p=probs))
        pt = float(p[tb].item()); pf = float(p[foil].item())
        corr2afc.append(1 if pt > pf else 0); conf2afc.append(abs(pt-pf)/(pt+pf+1e-12))
        v = table.get(b0*256+b1); pred.append(0.0 if v is None else float(v[tb]))
        # fine: hidden state + greedy single-byte error
        Herr.append(h[0, -1, :].cpu().numpy())
        Yerr.append(0 if int(torch.argmax(p).item()) == tb else 1)
    return (np.array(conf2afc), np.array(corr2afc), np.array(pred),
            np.array(Herr), np.array(Yerr))


def main():
    print("=== H_1206 metacognition capstone (REAL/FLAT/COUPLED/COARSE) ===", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC)); train_data, held = data[:cut], data[cut:]
    byte_freq = np.bincount(np.frombuffer(raw[:cut], dtype=np.uint8), minlength=256).astype(float) + 1.0
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)
    table = build_trigram(raw[:cut]); print(f"[trigram] {len(table)} ctx", flush=True)
    print("--- training ---", flush=True); m = train_model(train_data)
    print("--- collect ---", flush=True)
    conf, corr, pred, Herr, Yerr = collect(m, held, table, byte_freq)

    # F1 COARSE-REAL: 2AFC type-2 AUROC
    t2 = float(auroc(conf, corr))
    # F2 FINE-ABSENT: hidden-state probe for single-byte error (held-out split)
    half = len(Yerr)//2
    if Yerr[:half].sum() >= 5 and (1-Yerr[:half]).sum() >= 5:
        fine = logreg_auroc(Herr[:half], Yerr[:half].astype(float), Herr[half:], Yerr[half:].astype(float))
    else:
        fine = float("nan")
    # F3 COUPLED: type-2 AUROC in high-skill vs low-skill tercile
    q1, q2 = np.quantile(pred, [1/3, 2/3])
    isl = pred > q2; opn = pred <= q1
    t2_isl = float(auroc(conf[isl], corr[isl])) if isl.sum() > 10 else float("nan")
    t2_opn = float(auroc(conf[opn], corr[opn])) if opn.sum() > 10 else float("nan")
    couple_gap = (t2_isl - t2_opn) if not (math.isnan(t2_isl) or math.isnan(t2_opn)) else float("nan")

    print(f"[F1 coarse] type2_AUROC={t2:.4f}", flush=True)
    print(f"[F2 fine]   hidden error-probe AUROC={fine:.4f}", flush=True)
    print(f"[F3 couple] island_t2={t2_isl:.4f} open_t2={t2_opn:.4f} gap={couple_gap:+.4f}", flush=True)

    f1 = (not math.isnan(t2)) and t2 >= 0.65
    f2 = (not math.isnan(fine)) and fine <= 0.62
    f3 = (not math.isnan(couple_gap)) and couple_gap >= 0.10
    supported = bool(f1 and f2 and f3)
    if supported:
        ruling = "SUPPORTED: the campaign's unifying account holds as one decision-grade verdict — metacognition is REAL (output type-2), FLAT (no fine representational monitor), COUPLED to competence, and COARSE"
    else:
        legs = []
        if not f1: legs.append("F1 coarse-real failed (no output metacog)")
        if not f2: legs.append("F2 fine-absent failed (a representational monitor EXISTS — account falsified)")
        if not f3: legs.append("F3 coupled failed (metacog is competence-independent)")
        ruling = "CLOSED-NEGATIVE: " + "; ".join(legs)

    verdict = {
        "H": "H_1206",
        "title": "metacognition capstone — REAL/FLAT/COUPLED/COARSE synthesis",
        "F1_coarse_real": {"type2_auroc": t2, "bar": 0.65, "pass": bool(f1)},
        "F2_fine_absent": {"hidden_error_probe_auroc": fine, "bar_max": 0.62, "pass": bool(f2)},
        "F3_coupled": {"island_t2": t2_isl, "open_t2": t2_opn, "gap": couple_gap, "bar": 0.10, "pass": bool(f3)},
        "supported": supported,
        "ruling": ruling,
        "synthesizes": ["H_1202", "H_1203", "H_1204", "H_1205", "H_1213", "H_1214", "H_1216"],
        "neuroscience_anchor": "Fleming & Lau 2014 (type-2); Nelson-Narens (monitoring/control); Murphy (calibration)",
        "scope": "toy ByteGPT d256/4L CPU en slice — scale-up UNVERIFIED (a_scale_honest_scope)",
        "seed": SEED,
    }
    print("=== VERDICT ===", flush=True)
    print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(verdict, open(os.path.join(OUTDIR, "result.json"), "w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
