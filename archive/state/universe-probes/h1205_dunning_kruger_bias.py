"""
H_1205 — META-BIAS vs META-SENSITIVITY / DUNNING-KRUGER
Neuroscience separates metacognitive SENSITIVITY (can confidence track
correctness — H_1202) from metacognitive BIAS (systematic over/under-confidence)
(Fleming & Lau 2014). The Dunning-Kruger effect: low-competence agents are
systematically OVER-confident relative to high-competence agents. Does the
substrate show a Dunning-Kruger signature on an OBJECTIVE difficulty axis?

TASK: the H_1202 2AFC type-1 task. Confidence = |p(true)-p(foil)|/(p(true)+p(foil))
in [0,1]; accuracy in [0,1] (same scale -> comparable). OBJECTIVE difficulty
d_i = -log p_unigram(true_byte) (corpus byte-unigram surprisal — INDEPENDENT of
the model). Tercile decision points by d_i into EASY / MED / HARD.

meta-bias(tercile) = mean(confidence) - mean(accuracy)   (>0 = over-confident)

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 D-K SIGNATURE  — bias(HARD) - bias(EASY) >= +0.15 (over-confidence
                      concentrated on objectively hard items) AND bias(HARD) > 0.
  F2 SENSITIVITY-INTACT (dissociation control) — over the full set the type-2
                      AUROC (confidence|correctness) is reported; the D-K bias
                      finding is reported AS a bias effect SEPARATE from
                      sensitivity (no bar; documents the bias⊥sensitivity split).
  H_1205 SUPPORTED iff F1 (a Dunning-Kruger over-confidence gradient exists).
  CLOSED-NEGATIVE (a_paper_negative_ok) iff F1 fails: no D-K signature
  (over-confidence is not competence-graded — bias is flat or reversed).

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
N_DEC = 3000
HELDOUT_FRAC = 0.10
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1205_dunning_kruger_bias")


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
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = s.tok(idx) + s.pos(pos)[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.lnf(x))
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


@torch.no_grad()
def collect(m, held, byte_freq):
    rng = random.Random(SEED)
    bytes_pool = np.arange(256); probs = byte_freq / byte_freq.sum()
    logp_uni = np.log(probs)
    npr = np.random.RandomState(SEED + 99)
    n = held.numel()
    conf, corr, diff = [], [], []
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - 2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        true_b = int(held[pos].item())
        foil = int(npr.choice(bytes_pool, p=probs))
        while foil == true_b: foil = int(npr.choice(bytes_pool, p=probs))
        logits = m(ctx)
        p = F.softmax(logits[0, -1, :], dim=-1)
        pt = float(p[true_b].item()); pf = float(p[foil].item())
        corr.append(1 if pt > pf else 0)
        conf.append(abs(pt-pf)/(pt+pf+1e-12))
        diff.append(-float(logp_uni[true_b]))   # objective surprisal of true byte
    return np.array(conf), np.array(corr), np.array(diff)


def tercile_bias(conf, corr, diff):
    q1, q2 = np.quantile(diff, [1/3, 2/3])
    easy = diff <= q1; hard = diff > q2; med = (~easy) & (~hard)
    def bias(mask):
        if mask.sum() < 10: return float("nan"), float("nan"), float("nan"), int(mask.sum())
        c = conf[mask].mean(); a = corr[mask].mean()
        return c - a, c, a, int(mask.sum())
    return {"EASY": bias(easy), "MED": bias(med), "HARD": bias(hard)}


def main():
    print("=== H_1205 meta-bias vs sensitivity / Dunning-Kruger ===", flush=True)
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC))
    train_data, held = data[:cut], data[cut:]
    byte_freq = np.bincount(np.frombuffer(raw[:cut], dtype=np.uint8), minlength=256).astype(float) + 1.0
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)

    print("--- training ---", flush=True)
    m_tr = train_model(train_data)

    print("--- TRAINED ---", flush=True)
    conf, corr, diff = collect(m_tr, held, byte_freq)
    t2 = float(auroc(conf, corr))
    terc = tercile_bias(conf, corr, diff)
    for k in ("EASY", "MED", "HARD"):
        b, c, a, nn_ = terc[k]
        print(f"  [{k}] n={nn_} bias={b:.4f} conf={c:.4f} acc={a:.4f}", flush=True)
    print(f"  [overall] type2_AUROC={t2:.4f} acc={corr.mean():.3f}", flush=True)

    b_hard = terc["HARD"][0]; b_easy = terc["EASY"][0]
    dk_gap = (b_hard - b_easy) if not (math.isnan(b_hard) or math.isnan(b_easy)) else float("nan")
    f1 = (not math.isnan(dk_gap)) and dk_gap >= 0.15 and b_hard > 0
    supported = bool(f1)
    if supported:
        ruling = "SUPPORTED: Dunning-Kruger signature — over-confidence is concentrated on objectively hard items (bias(HARD)-bias(EASY)>=+0.15, bias(HARD)>0); meta-bias is competence-graded and dissociates from sensitivity"
    else:
        ruling = "CLOSED-NEGATIVE: no Dunning-Kruger gradient (D-K gap<+0.15 or bias(HARD)<=0) — over-confidence is not competence-graded in this substrate"

    verdict = {
        "H": "H_1205",
        "title": "meta-bias vs meta-sensitivity / Dunning-Kruger",
        "overall_type2_auroc": t2,
        "overall_acc": float(corr.mean()),
        "terciles": {k: {"bias": terc[k][0], "conf": terc[k][1], "acc": terc[k][2], "n": terc[k][3]} for k in terc},
        "F1_dk_signature": {"dk_gap_hard_minus_easy": dk_gap, "bias_hard": b_hard, "bar": 0.15, "pass": bool(f1)},
        "supported": supported,
        "ruling": ruling,
        "neuroscience_anchor": "meta-bias vs meta-sensitivity (Fleming & Lau 2014); Dunning-Kruger 1999",
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
