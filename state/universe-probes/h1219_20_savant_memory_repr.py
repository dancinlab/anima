"""
H_1219 + H_1220 — SAVANT MEMORY & REPRESENTATION (standalone), one shared model.

H_1219 — EIDETIC / PRODIGIOUS VERBATIM MEMORY (Treffert 2009): savants often show
  extraordinary rote verbatim recall. INDUCTION test: at positions whose preceding
  bigram already appeared earlier in the context, does the model copy the byte that
  followed it last time (induction-head verbatim recall)? Compare to non-induction
  positions (must use general statistics).
  FROZEN F1: acc(induction positions) - acc(non-induction) >= +0.20 (strong verbatim
  copy over generalization — eidetic-like).

H_1220 — DETAIL-OVER-GESTALT REPRESENTATION (weak central coherence mechanism,
  Happé & Frith 2006): savant cognition over-weights LOCAL detail vs GLOBAL gestalt.
  Linear-probe the hidden state for a LOCAL feature (is the last byte a lowercase
  letter — fully determined by the immediate token) vs a GLOBAL feature (is the
  current position in the FIRST half of its text line — requires long-range tracking).
  FROZEN F1: AUROC(local probe) - AUROC(global probe) >= +0.15 (detail is more
  linearly available than gestalt — weak central coherence representational signature).

Each: SUPPORTED iff its F1; CLOSED-NEGATIVE (a_paper_negative_ok) otherwise.
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
N_DEC = 4000; HELDOUT_FRAC = 0.10
VDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts")


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


def logreg_auroc(Xtr, ytr, Xte, yte, iters=400, lr=0.5, l2=1e-3):
    mu = Xtr.mean(0); sd = Xtr.std(0) + 1e-6
    Xtr = (Xtr-mu)/sd; Xte = (Xte-mu)/sd
    n, d = Xtr.shape; w = np.zeros(d); b = 0.0
    for _ in range(iters):
        p = 1/(1+np.exp(-(Xtr@w+b)))
        w -= lr*(Xtr.T@(p-ytr)/n + l2*w); b -= lr*float((p-ytr).mean())
    return float(auroc(1/(1+np.exp(-(Xte@w+b))), yte))


def save(slug, v):
    d = os.path.join(VDIR, slug); os.makedirs(d, exist_ok=True)
    json.dump(v, open(os.path.join(d, "result.json"), "w"), indent=2)
    print(f"[saved] {d}/result.json", flush=True)


def is_line_first_half(held, pos):
    # global feature: is pos in the first half of its text line (between surrounding \n)?
    n = held.numel()
    left = pos
    while left > 0 and int(held[left-1].item()) != 10 and pos - left < 400: left -= 1
    right = pos
    while right < n-1 and int(held[right].item()) != 10 and right - pos < 400: right += 1
    span = right - left
    if span < 4: return -1
    return 1 if (pos - left) < span / 2 else 0


@torch.no_grad()
def collect(m, held):
    rng = random.Random(SEED); n = held.numel()
    ind_corr, non_corr = [], []           # H_1219 induction
    Hloc, Yloc, Hglo, Yglo = [], [], [], []  # H_1220 local/global probe
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - 2)
        ctx = held[pos-BLOCK:pos]
        tb = int(held[pos].item())
        logits, h = m(ctx.long()[None].to(DEV), want_hidden=True)
        pred = int(torch.argmax(logits[0, -1, :]).item())
        ok = 1 if pred == tb else 0
        # induction: does prev bigram (ctx[-2:]) appear earlier in ctx, and is this an induction position?
        b_2, b_1 = int(ctx[-2].item()), int(ctx[-1].item())
        induction = False
        arr = ctx.numpy()
        for j in range(len(arr)-3, 0, -1):
            if arr[j-1] == b_2 and arr[j] == b_1:
                induction = True; break
        (ind_corr if induction else non_corr).append(ok)
        # H_1220 local feature: is last byte a lowercase letter (97-122)?
        Hloc.append(h[0, -1, :].cpu().numpy()); Yloc.append(1 if 97 <= b_1 <= 122 else 0)
        # H_1220 global feature: first-half-of-line
        g = is_line_first_half(held, pos)
        if g >= 0:
            Hglo.append(h[0, -1, :].cpu().numpy()); Yglo.append(g)
    return (np.array(ind_corr), np.array(non_corr),
            np.array(Hloc), np.array(Yloc), np.array(Hglo), np.array(Yglo))


def probe(H, Y):
    half = len(Y)//2
    if half < 10 or Y[:half].sum() < 5 or (1-Y[:half]).sum() < 5 or Y[half:].sum() < 5 or (1-Y[half:]).sum() < 5:
        return float("nan")
    return logreg_auroc(H[:half], Y[:half].astype(float), H[half:], Y[half:].astype(float))


def main():
    print("=== H_1219/1220 savant memory & representation ===", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC)); train_data, held = data[:cut], data[cut:]
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)
    print("--- training ---", flush=True); m = train_model(train_data)
    print("--- collect ---", flush=True)
    ind, non, Hloc, Yloc, Hglo, Yglo = collect(m, held)

    # H_1219 eidetic
    acc_ind = float(ind.mean()) if len(ind) else float("nan")
    acc_non = float(non.mean()) if len(non) else float("nan")
    gap19 = acc_ind - acc_non
    f19 = (not math.isnan(gap19)) and gap19 >= 0.20
    print(f"[1219] induction acc={acc_ind:.4f} (n={len(ind)}) | non-induction acc={acc_non:.4f} (n={len(non)}) | gap={gap19:+.4f}", flush=True)
    save("1219_savant_eidetic_memory", {
        "H": "H_1219", "title": "savant eidetic / verbatim memory (induction copy)",
        "induction_acc": acc_ind, "non_induction_acc": acc_non, "n_induction": int(len(ind)), "gap": gap19,
        "F1": {"gap": gap19, "bar": 0.20, "pass": bool(f19)}, "supported": bool(f19),
        "ruling": ("SUPPORTED: strong verbatim induction-copy over generalization — eidetic-like recall" if f19
                   else "CLOSED-NEGATIVE: no disproportionate verbatim-copy advantage (gap<+0.20) — not eidetic"),
        "neuroscience_anchor": "prodigious verbatim memory (Treffert 2009); induction heads",
        "scope": "toy ByteGPT d256/4L CPU en slice — UNVERIFIED scale (a_scale_honest_scope)", "seed": SEED})

    # H_1220 detail-over-gestalt representation
    a_loc = probe(Hloc, Yloc); a_glo = probe(Hglo, Yglo)
    gap20 = (a_loc - a_glo) if not (math.isnan(a_loc) or math.isnan(a_glo)) else float("nan")
    f20 = (not math.isnan(gap20)) and gap20 >= 0.15
    print(f"[1220] local_probe_AUROC={a_loc:.4f} global_probe_AUROC={a_glo:.4f} gap={gap20:+.4f}", flush=True)
    save("1220_savant_detail_over_gestalt", {
        "H": "H_1220", "title": "savant detail-over-gestalt representation (WCC)",
        "local_probe_auroc": a_loc, "global_probe_auroc": a_glo, "gap": gap20,
        "F1": {"gap": gap20, "bar": 0.15, "pass": bool(f20)}, "supported": bool(f20),
        "ruling": ("SUPPORTED: local detail is more linearly decodable than global gestalt — weak central coherence representational signature" if f20
                   else "CLOSED-NEGATIVE: local does not dominate global in the representation (gap<+0.15) — no detail-over-gestalt bias"),
        "neuroscience_anchor": "weak central coherence (Happé & Frith 2006)",
        "scope": "toy ByteGPT d256/4L CPU en slice — UNVERIFIED scale (a_scale_honest_scope)", "seed": SEED})
    print("=== DONE H_1219/H_1220 ===", flush=True)


if __name__ == "__main__":
    main()
