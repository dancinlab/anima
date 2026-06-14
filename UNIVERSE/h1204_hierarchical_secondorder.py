"""
H_1204 — HIERARCHICAL (SECOND-ORDER) METACOGNITION
Hierarchical models of metacognition (Fleming HMeta-d; Friston predictive coding)
hold that metacognition is a DISTINCT higher-order readout that can carry
information ABOVE the first-order confidence signal. Neuroscience question: does
a SECOND-ORDER probe on the substrate's internal state predict its OWN first-order
correctness BETTER than the first-order confidence (decision margin) alone?

TASK: the H_1202 2AFC type-1 task (choose true vs corpus-unigram foil). For each
decision collect: first-order confidence = |p(true)-p(foil)|/(p(true)+p(foil));
hidden state h = lnf[last]. Two predictors of OWN-CORRECTNESS:
  1st-order: confidence alone (the raw decision margin)
  2nd-order: a linear probe on h (trained on first half, tested on held-out half)

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 ADDED-VALUE  — 2nd-order probe AUROC(predict correctness) MINUS 1st-order
                    confidence AUROC >= +0.10 (higher-order readout adds info
                    beyond raw confidence — the hierarchical-dissociation claim).
  F2 GENERALIZES  — 2nd-order probe held-out AUROC >= 0.65 (a real readout, not
                    overfit).
  F3 ANTI-GOODHART— UNTRAINED backbone fails F1 (added-value < +0.10): the
                    hierarchy is LEARNED, not architectural.
  H_1204 SUPPORTED iff F1 AND F2 AND F3.
  CLOSED-NEGATIVE (a_paper_negative_ok) iff F1 fails: there is NO higher-order
  metacognitive readout beyond first-order confidence (metacognition is flat,
  not hierarchical, in this substrate).

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice. Substrate reused
VERBATIM from H_1142.
"""
import os, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
EN_SLICE_BYTES = 24 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
N_DEC = 2400
HELDOUT_FRAC = 0.10
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1204_hierarchical_secondorder")


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
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = s.tok(idx) + s.pos(pos)[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        h = s.lnf(x); logits = s.head(h)
        if want_hidden: return logits, h
        return logits
    def loss_on(s, idx, targets):
        logits = s(idx)
        return F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))


def batch(data, block, bs, dev):
    ix = torch.randint(0, data.numel() - block - 1, (bs,))
    x = torch.stack([data[i:i+block] for i in ix]).long()
    y = torch.stack([data[i+1:i+block+1] for i in ix]).long()
    return x.to(dev), y.to(dev)


def train_model(data):
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    t0 = time.time()
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for g in opt.param_groups: g["lr"] = lr_t
        x, y = batch(data, BLOCK, BS, DEV)
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
    Xtr = (Xtr - mu) / sd; Xte = (Xte - mu) / sd
    n, d = Xtr.shape; w = np.zeros(d); b = 0.0
    for _ in range(iters):
        z = Xtr @ w + b; p = 1/(1+np.exp(-z))
        gw = Xtr.T @ (p - ytr) / n + l2*w; gb = float((p - ytr).mean())
        w -= lr*gw; b -= lr*gb
    pte = 1/(1+np.exp(-(Xte @ w + b)))
    return float(auroc(pte, yte))


@torch.no_grad()
def collect(m, held, byte_freq):
    rng = random.Random(SEED)
    bytes_pool = np.arange(256); probs = byte_freq / byte_freq.sum()
    npr = np.random.RandomState(SEED + 99)
    n = held.numel()
    conf, corr, Hs = [], [], []
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - 2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        true_b = int(held[pos].item())
        foil = int(npr.choice(bytes_pool, p=probs))
        while foil == true_b: foil = int(npr.choice(bytes_pool, p=probs))
        logits, hid = m(ctx, want_hidden=True)
        p = F.softmax(logits[0, -1, :], dim=-1)
        pt = float(p[true_b].item()); pf = float(p[foil].item())
        corr.append(1 if pt > pf else 0)
        conf.append(abs(pt-pf)/(pt+pf+1e-12))
        Hs.append(hid[0, -1, :].cpu().numpy())
    return np.array(conf), np.array(corr), np.array(Hs)


def first_order_auroc(conf, corr):
    return float(auroc(conf, corr))


def second_order_auroc(H, corr):
    half = len(corr)//2
    if corr[:half].sum() < 5 or (1-corr[:half]).sum() < 5: return float("nan")
    return logreg_auroc(H[:half], corr[:half].astype(float), H[half:], corr[half:].astype(float))


def main():
    print("=== H_1204 hierarchical (second-order) metacognition ===", flush=True)
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC))
    train_data, held = data[:cut], data[cut:]
    byte_freq = np.bincount(np.frombuffer(raw[:cut], dtype=np.uint8), minlength=256).astype(float) + 1.0
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)

    print("--- F3 control: UNTRAINED ---", flush=True)
    m_un = ByteGPT().to(DEV).eval()
    c_u, y_u, H_u = collect(m_un, held, byte_freq)
    # held-out half for first-order to compare apples-to-apples
    half = len(y_u)//2
    fo_u = first_order_auroc(c_u[half:], y_u[half:])
    so_u = second_order_auroc(H_u, y_u)
    add_u = (so_u - fo_u) if not (math.isnan(so_u) or math.isnan(fo_u)) else float("nan")
    print(f"  [untrained] acc={y_u.mean():.3f} FO_AUROC={fo_u:.4f} SO_AUROC={so_u:.4f} added={add_u:.4f}", flush=True)

    print("--- training ---", flush=True)
    m_tr = train_model(train_data)

    print("--- TRAINED ---", flush=True)
    c_t, y_t, H_t = collect(m_tr, held, byte_freq)
    half = len(y_t)//2
    fo_t = first_order_auroc(c_t[half:], y_t[half:])
    so_t = second_order_auroc(H_t, y_t)
    add_t = (so_t - fo_t) if not (math.isnan(so_t) or math.isnan(fo_t)) else float("nan")
    print(f"  [trained] acc={y_t.mean():.3f} FO_AUROC={fo_t:.4f} SO_AUROC={so_t:.4f} added={add_t:.4f}", flush=True)

    f1 = (not math.isnan(add_t)) and add_t >= 0.10
    f2 = (not math.isnan(so_t)) and so_t >= 0.65
    f3 = math.isnan(add_u) or add_u < 0.10
    supported = bool(f1 and f2 and f3)
    if supported:
        ruling = "SUPPORTED: a hierarchical second-order readout exists — the hidden state carries metacognitive information ABOVE first-order confidence (added-value>=+0.10), generalizes, and is learned"
    elif not f1:
        ruling = "CLOSED-NEGATIVE: NO higher-order readout beyond first-order confidence (added-value<+0.10) — metacognition is FLAT not hierarchical in this substrate"
    elif not f2:
        ruling = "CLOSED-NEGATIVE: second-order probe does not generalize (held-out AUROC<0.65)"
    else:
        ruling = "CLOSED-NEGATIVE: F3 artifact — added-value present untrained (not learned)"

    verdict = {
        "H": "H_1204",
        "title": "hierarchical (second-order) metacognition",
        "acc_trained": float(y_t.mean()),
        "F1_added_value": {"second_minus_first_auroc": add_t, "first_order_auroc": fo_t, "second_order_auroc": so_t, "bar": 0.10, "pass": bool(f1)},
        "F2_generalizes": {"second_order_heldout_auroc": so_t, "bar": 0.65, "pass": bool(f2)},
        "F3_anti_goodhart": {"untrained_added_value": add_u, "pass": bool(f3)},
        "supported": supported,
        "ruling": ruling,
        "neuroscience_anchor": "hierarchical predictive coding (Friston); HMeta-d (Fleming 2017)",
        "scope": "toy ByteGPT d256/4L CPU en slice — scale-up UNVERIFIED (a_scale_honest_scope)",
        "seed": SEED,
    }
    print("=== VERDICT ===", flush=True)
    print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "result.json"), "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
