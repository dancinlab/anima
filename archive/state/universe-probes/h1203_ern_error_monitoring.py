"""
H_1203 — ERN ERROR-MONITORING (own-error signal, pre-feedback)
The error-related negativity (ERN): a ~80ms ACC negativity after an erroneous
response, present BEFORE any external feedback (Gehring 1993; Holroyd & Coles
2002 reinforcement-learning theory). Neuroscience question: does the substrate
carry an INTERNAL signal that spikes on its OWN errors at decision time, with no
access to the ground-truth label?

TASK: greedy next-byte prediction on held-out in-corpus text. "Response" =
argmax byte; ERROR = (argmax != true byte). Two internal signals at the decision
step (NO future / label access):
  (a) output entropy  H = -sum p log p   (uncertainty / ERN-analog magnitude)
  (b) hidden state    h = lnf(x)[last]    (the "ACC representation")

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 ERN MAGNITUDE   — entropy at ERROR positions > at CORRECT positions,
                       Cohen d >= 0.8 (the substrate is internally "more aroused"
                       exactly when it errs).
  F2 DECODABILITY    — a LINEAR probe on the hidden state h (logistic regression,
                       trained on the first half of decision points, tested on the
                       held-out second half) predicts OWN-ERROR with AUROC >= 0.70
                       (error info is linearly readable from internal rep — the
                       non-circular ACC-monitor claim).
  F3 ANTI-GOODHART   — UNTRAINED backbone F2 AUROC <= 0.60 (monitor is LEARNED).
  H_1203 SUPPORTED iff F1 AND F2 AND F3.
  CLOSED-NEGATIVE (a_paper_negative_ok) iff F1 or F2 fails on the trained model.

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice — scale-up
UNVERIFIED. Substrate reused VERBATIM from H_1142.
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
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1203_ern_error_monitoring")


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
        h = s.lnf(x)
        logits = s.head(h)
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


def cohen_d(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    na, nb = len(a), len(b)
    if na < 2 or nb < 2: return float("nan")
    sp = math.sqrt(((na-1)*a.var(ddof=1) + (nb-1)*b.var(ddof=1)) / (na+nb-2))
    return (a.mean() - b.mean()) / sp if sp > 0 else 0.0


def logreg_auroc(Xtr, ytr, Xte, yte, iters=400, lr=0.5, l2=1e-3):
    """tiny deterministic logistic regression; returns held-out AUROC."""
    mu = Xtr.mean(0); sd = Xtr.std(0) + 1e-6
    Xtr = (Xtr - mu) / sd; Xte = (Xte - mu) / sd
    n, d = Xtr.shape
    w = np.zeros(d); b = 0.0
    for _ in range(iters):
        z = Xtr @ w + b; p = 1/(1+np.exp(-z))
        gw = Xtr.T @ (p - ytr) / n + l2*w; gb = float((p - ytr).mean())
        w -= lr*gw; b -= lr*gb
    pte = 1/(1+np.exp(-(Xte @ w + b)))
    return float(auroc(pte, yte))


@torch.no_grad()
def collect(m, held):
    rng = random.Random(SEED)
    n = held.numel()
    ent_err, ent_cor = [], []
    H, Y = [], []
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - 2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        true_b = int(held[pos].item())
        logits, hid = m(ctx, want_hidden=True)
        lp = F.log_softmax(logits[0, -1, :], dim=-1); p = lp.exp()
        ent = float(-(p * lp).sum().item())
        pred = int(torch.argmax(logits[0, -1, :]).item())
        err = 1 if pred != true_b else 0
        (ent_err if err else ent_cor).append(ent)
        H.append(hid[0, -1, :].cpu().numpy()); Y.append(err)
    return np.array(ent_err), np.array(ent_cor), np.array(H), np.array(Y)


def f2_decode(H, Y, tag):
    half = len(Y) // 2
    if Y[:half].sum() < 5 or (1-Y[:half]).sum() < 5 or Y[half:].sum() < 5 or (1-Y[half:]).sum() < 5:
        return float("nan")
    a = logreg_auroc(H[:half], Y[:half].astype(float), H[half:], Y[half:].astype(float))
    return a


def main():
    print("=== H_1203 ERN error-monitoring (own-error, pre-feedback) ===", flush=True)
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC))
    train_data, held = data[:cut], data[cut:]
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)

    print("--- F3 control: UNTRAINED ---", flush=True)
    m_un = ByteGPT().to(DEV).eval()
    ee_u, ec_u, H_u, Y_u = collect(m_un, held)
    f2_un = f2_decode(H_u, Y_u, "untrained")
    print(f"  [untrained] err_rate={Y_u.mean():.3f} d(ent)={cohen_d(ee_u,ec_u):.3f} F2_AUROC={f2_un:.4f}", flush=True)

    print("--- training ---", flush=True)
    m_tr = train_model(train_data)

    print("--- TRAINED ---", flush=True)
    ee_t, ec_t, H_t, Y_t = collect(m_tr, held)
    d_ent = cohen_d(ee_t, ec_t)
    f2_tr = f2_decode(H_t, Y_t, "trained")
    print(f"  [trained] err_rate={Y_t.mean():.3f} d(ent)={d_ent:.3f} F2_AUROC={f2_tr:.4f} "
          f"ent_err={ee_t.mean():.3f} ent_cor={ec_t.mean():.3f}", flush=True)

    f1 = (not math.isnan(d_ent)) and d_ent >= 0.8
    f2 = (not math.isnan(f2_tr)) and f2_tr >= 0.70
    f3 = math.isnan(f2_un) or f2_un <= 0.60
    supported = bool(f1 and f2 and f3)
    if supported:
        ruling = "SUPPORTED: an internal ERN-analog error monitor exists — own-error is both arousal-marked (F1) and linearly decodable from hidden state pre-feedback (F2), and learned (F3)"
    elif not f2:
        ruling = "CLOSED-NEGATIVE: own-error NOT linearly decodable from hidden state (F2 AUROC<0.70) — no ACC-analog error monitor"
    elif not f1:
        ruling = "CLOSED-NEGATIVE: no ERN magnitude (entropy d<0.8 at errors) — internal arousal does not mark own errors"
    else:
        ruling = "CLOSED-NEGATIVE: F3 artifact (untrained already decodes) — error signal not learned"

    verdict = {
        "H": "H_1203",
        "title": "ERN error-monitoring (own-error signal, pre-feedback)",
        "err_rate_trained": float(Y_t.mean()),
        "F1_ern_magnitude": {"cohen_d_entropy": d_ent, "bar": 0.8, "pass": bool(f1)},
        "F2_decodability": {"hidden_probe_auroc": f2_tr, "bar": 0.70, "pass": bool(f2)},
        "F3_anti_goodhart": {"untrained_auroc": f2_un, "bar": 0.60, "pass": bool(f3)},
        "supported": supported,
        "ruling": ruling,
        "neuroscience_anchor": "ERN/ACC — Gehring 1993; Holroyd & Coles 2002 RL theory of ERN",
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
