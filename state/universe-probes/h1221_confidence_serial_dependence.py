"""
H_1221 — CONFIDENCE SERIAL DEPENDENCE (metacognitive history bias)
Human confidence shows SERIAL DEPENDENCE: confidence on the current decision is
biased by the PREVIOUS decision's confidence, beyond shared stimulus difficulty
(Rahnev 2015; Braun et al. 2018 confidence-leak / history bias). Does the
substrate's confidence carry a comparable history term?

TASK: walk CONTIGUOUS held-out text in runs of K consecutive next-byte decisions.
At each step t collect: confidence_t = max softmax prob; objective difficulty_t =
corpus-trigram predictability of the true byte (model-independent). Residualize
confidence on difficulty (remove the shared-difficulty driver), then test whether
RESIDUAL confidence autocorrelates step-to-step.

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 SERIAL-DEPENDENCE — partial autocorr of confidence at lag 1, controlling for
                         current+previous difficulty, r >= +0.15 (a genuine history
                         bias beyond difficulty).
  F2 NOT-DIFFICULTY-ARTIFACT — the raw difficulty autocorrelation is reported; F1
                         must hold on the DIFFICULTY-RESIDUALIZED confidence (so the
                         effect is not just difficulty being autocorrelated in text).
  H_1221 SUPPORTED iff F1 (on residualized confidence).
  CLOSED-NEGATIVE (a_paper_negative_ok) iff residual partial-autocorr < 0.15 —
  confidence is memoryless (purely stimulus-driven, no metacognitive history term).

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
N_RUNS = 400; RUN_LEN = 12      # contiguous decision runs
HELDOUT_FRAC = 0.10
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1221_confidence_serial_dependence")


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


def pearson(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    a = a - a.mean(); b = b - b.mean()
    den = math.sqrt((a*a).sum() * (b*b).sum())
    return float((a*b).sum()/den) if den > 0 else 0.0


def residualize(y, x):
    # remove linear dependence of y on x; return residual
    x = np.asarray(x, float); y = np.asarray(y, float)
    xm = x - x.mean(); ym = y - y.mean()
    b = (xm*ym).sum() / ((xm*xm).sum() + 1e-12)
    return y - (y.mean() + b*(x - x.mean()))


@torch.no_grad()
def collect(m, held, table):
    rng = random.Random(SEED); n = held.numel()
    cur_conf, prev_conf, cur_diff, prev_diff = [], [], [], []
    raw_diff_t, raw_diff_tm1 = [], []
    for _ in range(N_RUNS):
        start = rng.randint(BLOCK, n - RUN_LEN - 2)
        seq_conf, seq_diff = [], []
        for k in range(RUN_LEN):
            pos = start + k
            ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
            tb = int(held[pos].item()); b0 = int(held[pos-2].item()); b1 = int(held[pos-1].item())
            p = F.softmax(m(ctx)[0, -1, :], dim=-1)
            seq_conf.append(float(p.max().item()))
            v = table.get(b0*256+b1); seq_diff.append(0.0 if v is None else float(v[tb]))
        for k in range(1, RUN_LEN):
            cur_conf.append(seq_conf[k]); prev_conf.append(seq_conf[k-1])
            cur_diff.append(seq_diff[k]); prev_diff.append(seq_diff[k-1])
    return (np.array(cur_conf), np.array(prev_conf), np.array(cur_diff), np.array(prev_diff))


def main():
    print("=== H_1221 confidence serial dependence (metacog history bias) ===", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC)); train_data, held = data[:cut], data[cut:]
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)
    table = build_trigram(raw[:cut]); print(f"[trigram] {len(table)} ctx", flush=True)
    print("--- training ---", flush=True); m = train_model(train_data)
    print("--- collect contiguous runs ---", flush=True)
    cur_c, prev_c, cur_d, prev_d = collect(m, held, table)

    raw_conf_autocorr = pearson(cur_c, prev_c)
    raw_diff_autocorr = pearson(cur_d, prev_d)
    # residualize current+previous confidence on current+previous difficulty
    cur_res = residualize(residualize(cur_c, cur_d), prev_d)
    prev_res = residualize(residualize(prev_c, cur_d), prev_d)
    partial = pearson(cur_res, prev_res)
    print(f"  raw conf autocorr(lag1)={raw_conf_autocorr:.4f}  diff autocorr={raw_diff_autocorr:.4f}", flush=True)
    print(f"  PARTIAL conf autocorr (difficulty-controlled)={partial:.4f}", flush=True)

    f1 = partial >= 0.15
    supported = bool(f1)
    if supported:
        ruling = f"SUPPORTED: confidence carries a history term — difficulty-controlled lag-1 autocorr {partial:.3f} >= 0.15 (metacognitive serial dependence / confidence-leak)"
    else:
        ruling = f"CLOSED-NEGATIVE: confidence is memoryless (difficulty-controlled autocorr {partial:.3f} < 0.15) — no metacognitive history bias; confidence is purely stimulus-driven"

    verdict = {
        "H": "H_1221", "title": "confidence serial dependence (metacog history bias)",
        "raw_conf_autocorr_lag1": raw_conf_autocorr, "raw_diff_autocorr": raw_diff_autocorr,
        "partial_conf_autocorr_difficulty_controlled": partial,
        "F1_serial_dependence": {"partial_autocorr": partial, "bar": 0.15, "pass": bool(f1)},
        "supported": supported, "ruling": ruling,
        "neuroscience_anchor": "confidence serial dependence / confidence-leak (Rahnev 2015; Braun 2018)",
        "scope": "toy ByteGPT d256/4L CPU en slice — UNVERIFIED scale (a_scale_honest_scope)", "seed": SEED,
    }
    print("=== VERDICT ===", flush=True); print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(verdict, open(os.path.join(OUTDIR, "result.json"), "w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
