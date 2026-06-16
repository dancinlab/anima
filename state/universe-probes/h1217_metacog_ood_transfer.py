"""
H_1217 — METACOGNITION UNDER DISTRIBUTION SHIFT (domain-general vs specific)
Neuroscience asks whether metacognition is DOMAIN-GENERAL (a central aPFC resource,
Fleming & Lau 2014) or content-tied. Does the substrate's type-2 sensitivity SURVIVE
on out-of-distribution input it never trained on?

TASK: train ByteGPT on the EN slice (first 24MB of corpus_5lang). Then run the
H_1202 2AFC type-2 measurement on TWO held-out sets: (a) IN-DIST = EN held-out tail,
(b) OOD = a deep non-English slice (offset ~600MB into the zh/ru/ja block — bytes the
model never saw, different script/statistics).

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 OOD-TRANSFER  — type-2 AUROC(OOD) >= 0.60 (metacognitive sensitivity transfers
                     to unseen content — domain-general).
  F2 NOT-COLLAPSE  — type2_AUROC(in-dist) - type2_AUROC(OOD) <= 0.15 (metacog does
                     not collapse off-distribution; only mild degradation allowed).
  H_1217 SUPPORTED iff F1 AND F2 (domain-general metacognition).
  CLOSED-NEGATIVE (a_paper_negative_ok) iff OOD AUROC < 0.60 or drops >0.15 —
  metacognition is content-tied, not a domain-general resource.

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU. Substrate from H_1142/H_1202.
"""
import os, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"
CORPUS = os.environ.get("CORPUS", "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt")
OOD_FILE = os.environ.get("OOD_FILE", "")   # if set, read OOD bytes from this separate file
EN_SLICE_BYTES = 24 * 1024 * 1024
OOD_OFFSET = 600 * 1024 * 1024      # deep into the non-English block (en,zh,ru,ja,ko order)
OOD_BYTES = 6 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
N_DEC = 2000; HELDOUT_FRAC = 0.10
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1217_metacog_ood_transfer")


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
    def forward(s, idx):
        T = idx.shape[1]; pos = torch.arange(T, device=idx.device)
        x = s.tok(idx) + s.pos(pos)[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.lnf(x))
    def loss_on(s, idx, targets):
        logits = s(idx)
        return F.cross_entropy(logits.reshape(-1, VOCAB), targets.reshape(-1))


def train_model(data):
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


@torch.no_grad()
def type2(m, held, byte_freq, tag):
    rng = random.Random(SEED); n = held.numel()
    bytes_pool = np.arange(256); probs = byte_freq / byte_freq.sum()
    npr = np.random.RandomState(SEED + 99)
    conf, corr = [], []
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - 2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        tb = int(held[pos].item())
        foil = int(npr.choice(bytes_pool, p=probs))
        while foil == tb: foil = int(npr.choice(bytes_pool, p=probs))
        p = F.softmax(m(ctx)[0, -1, :], dim=-1)
        pt = float(p[tb].item()); pf = float(p[foil].item())
        corr.append(1 if pt > pf else 0); conf.append(abs(pt-pf)/(pt+pf+1e-12))
    a = float(auroc(np.array(conf), np.array(corr)))
    print(f"  [{tag}] acc={np.mean(corr):.3f} type2_AUROC={a:.4f}", flush=True)
    return a


def main():
    print("=== H_1217 metacog under distribution shift (OOD transfer) ===", flush=True)
    with open(CORPUS, "rb") as f:
        en = f.read(EN_SLICE_BYTES)
    if OOD_FILE:
        with open(OOD_FILE, "rb") as f: ood_raw = f.read(OOD_BYTES)
    else:
        with open(CORPUS, "rb") as f:
            f.seek(OOD_OFFSET); ood_raw = f.read(OOD_BYTES)
    data = torch.frombuffer(bytearray(en), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC)); train_data, en_held = data[:cut], data[cut:]
    ood = torch.frombuffer(bytearray(ood_raw), dtype=torch.uint8).clone()
    en_freq = np.bincount(np.frombuffer(en[:cut], dtype=np.uint8), minlength=256).astype(float) + 1.0
    ood_freq = np.bincount(np.frombuffer(ood_raw, dtype=np.uint8), minlength=256).astype(float) + 1.0
    # ascii fraction sanity (OOD should be less ascii / different)
    ood_ascii = float((np.frombuffer(ood_raw, dtype=np.uint8) < 128).mean())
    print(f"[data] train={train_data.numel()/1e6:.1f}MB en_held={en_held.numel()/1e6:.1f}MB ood={ood.numel()/1e6:.1f}MB ood_ascii_frac={ood_ascii:.3f}", flush=True)

    print("--- training (EN) ---", flush=True); m = train_model(train_data)
    print("--- type-2 measurement ---", flush=True)
    a_in = type2(m, en_held, en_freq, "IN-DIST(EN)")
    a_ood = type2(m, ood, ood_freq, "OOD(non-EN)")

    drop = a_in - a_ood
    f1 = (not math.isnan(a_ood)) and a_ood >= 0.60
    f2 = (not math.isnan(drop)) and drop <= 0.15
    supported = bool(f1 and f2)
    if supported:
        ruling = "SUPPORTED: type-2 sensitivity transfers to OOD content (AUROC>=0.60, drop<=0.15) — domain-general metacognition"
    elif not f1:
        ruling = f"CLOSED-NEGATIVE: OOD type-2 AUROC {a_ood:.3f} < 0.60 — metacognition does not survive distribution shift (content-tied)"
    else:
        ruling = f"CLOSED-NEGATIVE: type-2 collapses off-distribution (drop {drop:.3f} > 0.15) — content-specific, not domain-general"

    verdict = {
        "H": "H_1217", "title": "metacognition under distribution shift (OOD transfer)",
        "in_dist_type2_auroc": a_in, "ood_type2_auroc": a_ood, "drop": drop, "ood_ascii_frac": ood_ascii,
        "F1_ood_transfer": {"ood_auroc": a_ood, "bar": 0.60, "pass": bool(f1)},
        "F2_not_collapse": {"drop": drop, "bar_max": 0.15, "pass": bool(f2)},
        "supported": supported, "ruling": ruling,
        "neuroscience_anchor": "domain-general vs domain-specific metacognition (Fleming & Lau 2014, aPFC)",
        "scope": "toy ByteGPT d256/4L CPU — scale-up UNVERIFIED (a_scale_honest_scope)", "seed": SEED,
    }
    print("=== VERDICT ===", flush=True); print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(verdict, open(os.path.join(OUTDIR, "result.json"), "w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
