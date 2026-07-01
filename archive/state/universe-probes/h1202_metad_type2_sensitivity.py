"""
H_1202 — META-D' / M-RATIO (TYPE-2 METACOGNITIVE SENSITIVITY)
The field-standard neuroscience operationalization of metacognition
(Maniscalco & Lau 2012; Fleming & Lau 2014, aPFC correlate). The prior
campaign (H_1142/1148) measured AUROC on input-FAMILIARITY (OOD) and
grep-fabrication and closed NEGATIVE ("no internal handle on hallucination").
It NEVER measured TYPE-2 SENSITIVITY ON THE MODEL'S OWN DECISION CORRECTNESS,
which IS what neuroscience means by metacognition.

TYPE-1 task (2AFC, matching psychophysics): at each in-corpus decision point the
model is shown {true_next_byte, foil} and "chooses" the higher-probability one
(correct iff p(true) > p(foil)). foil ~ corpus byte-unigram (seed-fixed, != true).
CONFIDENCE = |p(true)-p(foil)| / (p(true)+p(foil))  in [0,1].

TYPE-2 sensitivity = does CONFIDENCE discriminate the model's OWN correct from
incorrect type-1 decisions? Measured model-free as type-2 AUROC (Fleming & Lau
2014's non-parametric meta-d' alternative) + meta-d' (AUROC->d' Gaussian map) +
M-ratio = meta-d'/d'.

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 SENSITIVITY     — type-2 AUROC(conf ; label=correct) >= 0.60
                       (chance=0.50; human ~0.70-0.75). Confidence must carry
                       information about own correctness.
  F2 ANTI-ARTIFACT   — type-2 AUROC > SHUFFLED-confidence control by >= +0.08
                       (shuffle breaks conf<->correct pairing -> AUROC ~ 0.50).
  F3 ANTI-GOODHART   — UNTRAINED backbone type-2 AUROC <= 0.55 (metacognition is
                       LEARNED, not an architecture/byte artifact).
  H_1202 SUPPORTED iff F1 AND F2 AND F3.
  CLOSED-NEGATIVE (a_paper_negative_ok) iff trained type-2 AUROC < 0.60 OR fails
  F2 (confidence is metacognitively INSENSITIVE -> substrate has no type-2 handle
  on its own decisions, extending H_1148 to the proper neuroscience metric).

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
N_DEC = 2000          # type-1 decision points
HELDOUT_FRAC = 0.10   # last 10% of slice = held-out region for decision sampling
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1202_metad_type2_sensitivity")


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
    def forward(s, idx, targets=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = s.tok(idx) + s.pos(pos)[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        logits = s.head(s.lnf(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        return logits, loss


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
        _, l = m(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 250 == 0 or st == STEPS-1:
            print(f"  [train] step {st} ce={l.item():.4f} {(time.time()-t0)/60:.1f}min", flush=True)
    m.eval(); return m


def auroc(scores, labels):
    """AUROC via Mann-Whitney. labels: 1=positive. returns P(score_pos > score_neg)."""
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    order = np.argsort(s); ranks = np.empty(len(s), float); ranks[order] = np.arange(1, len(s)+1)
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    rsum = np.zeros(len(cnt)); np.add.at(rsum, inv, ranks); avg = rsum / cnt; ranks = avg[inv]
    n1 = int(y.sum()); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return float("nan")
    return (ranks[y == 1].sum() - n1*(n1+1)/2) / (n1*n0)


def zinv(p):
    """inverse standard-normal CDF (Acklam rational approx)."""
    p = min(max(p, 1e-6), 1-1e-6)
    a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00]
    b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,6.680131188771972e+01,-1.328068155288572e+01]
    c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,-2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00]
    d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,3.754408661907416e+00]
    pl=0.02425
    if p < pl:
        q=math.sqrt(-2*math.log(p)); return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p <= 1-pl:
        q=p-0.5; r=q*q; return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q=math.sqrt(-2*math.log(1-p)); return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


@torch.no_grad()
def type1_type2(m, held, byte_freq, tag):
    """Run the 2AFC type-1 task + collect type-2 confidence over N_DEC points."""
    rng = random.Random(SEED + (0 if tag == "trained" else 1))
    # seed-fixed foil sampler from corpus byte-unigram
    bytes_pool = np.arange(256); probs = byte_freq / byte_freq.sum()
    npr = np.random.RandomState(SEED + 99)
    n = held.numel()
    correct, conf = [], []
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - 2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        true_b = int(held[pos].item())
        foil = int(npr.choice(bytes_pool, p=probs))
        while foil == true_b:
            foil = int(npr.choice(bytes_pool, p=probs))
        logits, _ = m(ctx)
        p = F.softmax(logits[0, -1, :], dim=-1)
        pt = float(p[true_b].item()); pf = float(p[foil].item())
        correct.append(1 if pt > pf else 0)
        denom = pt + pf + 1e-12
        conf.append(abs(pt - pf) / denom)
    correct = np.array(correct); conf = np.array(conf)
    acc = float(correct.mean())
    # type-1 d' for 2AFC: d' = sqrt(2) * z(accuracy)
    dprime = math.sqrt(2) * zinv(acc)
    # type-2 AUROC: confidence discriminates correct(1) from incorrect(0)
    t2_auroc = float(auroc(conf, correct))
    # shuffle control: break conf<->correct pairing
    shuf = conf.copy(); np.random.RandomState(SEED + 7).shuffle(shuf)
    t2_shuffle = float(auroc(shuf, correct))
    # meta-d' via AUROC->d' Gaussian map (single-distribution: d' = sqrt(2)*z(AUROC))
    meta_dprime = math.sqrt(2) * zinv(t2_auroc) if not math.isnan(t2_auroc) else float("nan")
    m_ratio = meta_dprime / dprime if dprime > 1e-6 else float("nan")
    print(f"  [{tag}] acc={acc:.3f} d'={dprime:.3f} type2_AUROC={t2_auroc:.4f} "
          f"shuffle={t2_shuffle:.4f} meta-d'={meta_dprime:.3f} M-ratio={m_ratio:.3f}", flush=True)
    return dict(acc=acc, dprime=dprime, t2_auroc=t2_auroc, t2_shuffle=t2_shuffle,
                meta_dprime=meta_dprime, m_ratio=m_ratio, n=N_DEC)


def main():
    print("=== H_1202 meta-d'/M-ratio (type-2 metacognitive sensitivity) ===", flush=True)
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC))
    train_data, held = data[:cut], data[cut:]
    byte_freq = np.bincount(np.frombuffer(raw[:cut], dtype=np.uint8), minlength=256).astype(float) + 1.0
    print(f"[data] slice={data.numel()/1e6:.1f}MB train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)

    print("--- F3 control: UNTRAINED ---", flush=True)
    m_un = ByteGPT().to(DEV).eval()
    r_un = type1_type2(m_un, held, byte_freq, "untrained")

    print("--- training ---", flush=True)
    m_tr = train_model(train_data)

    print("--- TRAINED ---", flush=True)
    r_tr = type1_type2(m_tr, held, byte_freq, "trained")

    f1 = r_tr["t2_auroc"] >= 0.60
    f2 = (r_tr["t2_auroc"] - r_tr["t2_shuffle"]) >= 0.08
    f3 = r_un["t2_auroc"] <= 0.55
    supported = bool(f1 and f2 and f3)
    if supported:
        ruling = "SUPPORTED: type-2 metacognitive sensitivity is real, learned, and above artifact — the substrate HAS a meta-d' handle on its own decision correctness"
    elif r_tr["t2_auroc"] < 0.60:
        ruling = "CLOSED-NEGATIVE: type-2 AUROC < 0.60 — confidence is metacognitively INSENSITIVE to own decision correctness; no meta-d' handle (extends H_1148 to the field-standard neuroscience metric)"
    else:
        ruling = "CLOSED-NEGATIVE: failed F2/F3 (artifact or unlearned) — type-2 signal not a genuine learned metacognition"

    verdict = {
        "H": "H_1202",
        "title": "meta-d'/M-ratio type-2 metacognitive sensitivity",
        "trained": r_tr, "untrained": r_un,
        "F1_sensitivity": {"t2_auroc": r_tr["t2_auroc"], "bar": 0.60, "pass": bool(f1)},
        "F2_anti_artifact": {"delta_vs_shuffle": r_tr["t2_auroc"]-r_tr["t2_shuffle"], "bar": 0.08, "pass": bool(f2)},
        "F3_anti_goodhart": {"untrained_t2_auroc": r_un["t2_auroc"], "bar": 0.55, "pass": bool(f3)},
        "supported": supported,
        "ruling": ruling,
        "neuroscience_anchor": "Maniscalco & Lau 2012 (meta-d'); Fleming & Lau 2014 (type-2 AUROC, aPFC)",
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
