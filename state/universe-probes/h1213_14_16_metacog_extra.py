"""
H_1213 + H_1214 + H_1216 — ADDITIONAL METACOGNITION (neuroscience), one shared model.

H_1213 — CALIBRATION (reliability, not discrimination). H_1202 showed strong
  type-2 DISCRIMINATION (AUROC); calibration is the orthogonal Murphy component —
  does confidence match empirical accuracy? Metric: ECE (10-bin) + Brier.
  FROZEN F1: ECE <= 0.10 (well-calibrated). (LMs are typically overconfident ->
  expected closed-neg; reliability ⊥ resolution.)

H_1214 — FEELING-OF-KNOWING (prospective metamemory). Nelson & Narens; Hart 1965 FOK:
  can the system judge, BEFORE retrieving, whether it will succeed? Probe the
  PROMPT-state hidden vector (last prompt position, no generation yet) to predict
  whether the upcoming greedy K=5-byte continuation will EXACTLY match the truth.
  FROZEN F1: prompt-state probe AUROC >= 0.65 (train/test split) — prospective
  success is decodable before acting.

H_1216 — METACOGNITIVE CONTROL (monitoring -> control). Nelson-Narens: monitoring
  is useful only if it drives control. Selective prediction: abstain on the
  lowest-confidence decisions; does accuracy-on-answered rise with selectivity?
  FROZEN F1: accuracy at 50% coverage - accuracy at 100% coverage >= +0.10
  (confidence enables a useful act/abstain control policy).

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
N_DEC = 3000; FOK_K = 5
HELDOUT_FRAC = 0.10
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


def save(slug, v):
    d = os.path.join(VDIR, slug); os.makedirs(d, exist_ok=True)
    json.dump(v, open(os.path.join(d, "result.json"), "w"), indent=2)
    print(f"[saved] {d}/result.json", flush=True)


@torch.no_grad()
def collect(m, held):
    rng = random.Random(SEED); n = held.numel()
    conf1, corr1 = [], []            # single-byte (calibration + control)
    Hprompt, fok_succ = [], []       # FOK prospective
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - FOK_K - 2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        logits, h = m(ctx, want_hidden=True)
        p = F.softmax(logits[0, -1, :], dim=-1)
        tb = int(held[pos].item())
        conf1.append(float(p.max().item())); corr1.append(1 if int(torch.argmax(p).item()) == tb else 0)
        # FOK: probe prompt-state h BEFORE generating; success = exact K-byte greedy match
        Hprompt.append(h[0, -1, :].cpu().numpy())
        ids = ctx.clone(); ok = True
        for k in range(FOK_K):
            lg = m(ids[:, -BLOCK:])
            nb = int(torch.argmax(lg[0, -1, :]).item())
            if nb != int(held[pos+k].item()): ok = False; break
            ids = torch.cat([ids, torch.tensor([[nb]], device=DEV)], 1)
        fok_succ.append(1 if ok else 0)
    return (np.array(conf1), np.array(corr1), np.array(Hprompt), np.array(fok_succ))


def main():
    print("=== H_1213/1214/1216 additional metacognition ===", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC)); train_data, held = data[:cut], data[cut:]
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)
    print("--- training ---", flush=True); m = train_model(train_data)
    print("--- collect ---", flush=True)
    conf, corr, Hp, fok = collect(m, held)

    # ---- H_1213 calibration ----
    bins = np.linspace(0, 1, 11); ece = 0.0; N = len(corr)
    for i in range(10):
        sel = (conf >= bins[i]) & (conf < bins[i+1] if i < 9 else conf <= bins[i+1])
        if sel.sum() == 0: continue
        ece += abs(corr[sel].mean() - conf[sel].mean()) * sel.sum() / N
    brier = float(((conf - corr)**2).mean())
    f1_13 = ece <= 0.10
    print(f"[1213] ECE={ece:.4f} Brier={brier:.4f} mean_conf={conf.mean():.4f} acc={corr.mean():.4f}", flush=True)
    save("1213_metacog_calibration", {
        "H": "H_1213", "title": "metacognitive calibration (ECE/Brier)", "ece": ece, "brier": brier,
        "mean_conf": float(conf.mean()), "acc": float(corr.mean()),
        "F1": {"ece": ece, "bar": 0.10, "pass": bool(f1_13)}, "supported": bool(f1_13),
        "ruling": ("SUPPORTED: confidence is well-calibrated (ECE<=0.10)" if f1_13
                   else f"CLOSED-NEGATIVE: miscalibrated (ECE={ece:.3f}>0.10) — reliability fails though discrimination (H_1202) holds; calibration ⊥ resolution"),
        "neuroscience_anchor": "Murphy decomposition (reliability vs resolution); metacog bias (Fleming & Lau 2014)",
        "scope": "toy ByteGPT d256/4L CPU en slice — UNVERIFIED scale (a_scale_honest_scope)", "seed": SEED})

    # ---- H_1214 feeling-of-knowing ----
    half = len(fok)//2
    if fok[:half].sum() >= 5 and (1-fok[:half]).sum() >= 5 and fok[half:].sum() >= 5 and (1-fok[half:]).sum() >= 5:
        fok_auroc = logreg_auroc(Hp[:half], fok[:half].astype(float), Hp[half:], fok[half:].astype(float))
    else:
        fok_auroc = float("nan")
    f1_14 = (not math.isnan(fok_auroc)) and fok_auroc >= 0.65
    print(f"[1214] FOK success_rate={fok.mean():.4f} prompt-state probe AUROC={fok_auroc:.4f}", flush=True)
    save("1214_feeling_of_knowing", {
        "H": "H_1214", "title": "feeling-of-knowing (prospective metamemory)",
        "fok_success_rate": float(fok.mean()), "prompt_state_probe_auroc": fok_auroc,
        "F1": {"auroc": fok_auroc, "bar": 0.65, "pass": bool(f1_14)}, "supported": bool(f1_14),
        "ruling": ("SUPPORTED: prospective success is decodable from the pre-generation prompt state — a feeling-of-knowing signal" if f1_14
                   else "CLOSED-NEGATIVE: pre-generation state does not predict upcoming success (AUROC<0.65) — no prospective feeling-of-knowing"),
        "neuroscience_anchor": "Nelson & Narens framework; Hart 1965 feeling-of-knowing",
        "scope": "toy ByteGPT d256/4L CPU en slice — UNVERIFIED scale (a_scale_honest_scope)", "seed": SEED})

    # ---- H_1216 metacognitive control (selective prediction) ----
    order = np.argsort(-conf)  # most confident first
    corr_sorted = corr[order]
    def acc_at(cov):
        k = max(1, int(len(corr_sorted)*cov)); return float(corr_sorted[:k].mean())
    acc100 = acc_at(1.0); acc50 = acc_at(0.5); acc25 = acc_at(0.25)
    gain = acc50 - acc100
    f1_16 = gain >= 0.10
    print(f"[1216] acc@100%={acc100:.4f} acc@50%={acc50:.4f} acc@25%={acc25:.4f} gain={gain:+.4f}", flush=True)
    save("1216_metacog_control", {
        "H": "H_1216", "title": "metacognitive control (selective prediction)",
        "acc_at_100": acc100, "acc_at_50": acc50, "acc_at_25": acc25, "selective_gain_50": gain,
        "F1": {"gain_at_50pct_coverage": gain, "bar": 0.10, "pass": bool(f1_16)}, "supported": bool(f1_16),
        "ruling": ("SUPPORTED: abstaining on low-confidence decisions raises accuracy-on-answered — confidence drives a useful act/abstain control policy" if f1_16
                   else "CLOSED-NEGATIVE: selective abstention does not improve accuracy (gain<+0.10) — monitoring does not yield useful control"),
        "neuroscience_anchor": "Nelson & Narens monitoring->control; selective prediction / risk-coverage",
        "scope": "toy ByteGPT d256/4L CPU en slice — UNVERIFIED scale (a_scale_honest_scope)", "seed": SEED})
    print("=== DONE H_1213/1214/1216 ===", flush=True)


if __name__ == "__main__":
    main()
