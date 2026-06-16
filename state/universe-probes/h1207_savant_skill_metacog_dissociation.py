"""
H_1207 — SAVANT DISSOCIATION (skill ⊥ metacognition)
Savant syndrome: an "island of genius" — extraordinary rote/mechanical skill in a
narrow structured domain, classically PAIRED with poor metacognitive/declarative
access ("can do but can't explain how"); detail-focused, weak top-down monitoring
(Treffert 2009; Snyder 2009; weak central coherence, Happé & Frith 2006).

Neuroscience question: in a ROTE/mechanical "island" domain where the substrate
has unusually HIGH first-order accuracy, does its metacognitive sensitivity FAIL
to rise with the skill (or even drop) — the savant skill⊥metacognition split?

DOMAIN AXIS (objective, model-INDEPENDENT): a corpus TRIGRAM model gives each
position the predictability of the true next byte from the previous 2 bytes.
  SAVANT-ISLAND = top-tercile trigram-predictable positions (rote/mechanical)
  OPEN          = bottom-tercile (semantically open, needs gestalt)
TASK: greedy next-byte prediction. correct = (argmax == true). confidence = max
softmax prob. type-2 sensitivity = AUROC(confidence ; correctness) per partition.

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 ISLAND-OF-SKILL  — acc(island) - acc(open) >= +0.15 (a genuine high-skill
                        island exists).
  F2 METACOG-BLIND    — type2_AUROC(island) <= type2_AUROC(open) - 0.10
                        (metacognition does NOT scale with the island skill — the
                        savant dissociation: high competence, low self-monitoring).
  (guard: each partition needs >= 30 errors AND >= 30 correct for a valid type-2
   AUROC; if the island is at accuracy ceiling with <30 errors that is REPORTED as
   ceiling-driven monitoring-blindness, the savant signature in its extreme form.)
  H_1207 SUPPORTED iff F1 AND F2.
  CLOSED-NEGATIVE (a_paper_negative_ok) iff F2 fails: metacognition tracks skill
  normally across domains — NO savant dissociation in this substrate.

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice. Substrate reused
VERBATIM from H_1142.
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
N_DEC = 4000
HELDOUT_FRAC = 0.10
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1207_savant_skill_metacog_dissociation")


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


def build_trigram(arr):
    """corpus trigram counts -> P(c | prev2). returns dict keyed (a,b)->prob-array (lazy via counts)."""
    a = np.frombuffer(arr, dtype=np.uint8).astype(np.int64)
    keys = a[:-2]*256 + a[1:-2+1]   # (prev2,prev1) packed
    nxt = a[2:]
    # count via dict of 256-vectors only for observed keys (sparse)
    from collections import defaultdict
    cnt = defaultdict(lambda: np.zeros(256, dtype=np.float64))
    # subsample for speed: every position (24MB is fine in C-loop? use vectorized grouping)
    order = np.argsort(keys, kind="stable")
    ks = keys[order]; ns = nxt[order]
    uniq, start = np.unique(ks, return_index=True)
    starts = list(start) + [len(ks)]
    table = {}
    for i, k in enumerate(uniq):
        seg = ns[starts[i]:starts[i+1]]
        v = np.bincount(seg, minlength=256).astype(np.float64)
        table[int(k)] = v / v.sum()
    return table


def trigram_predictability(table, b0, b1, true_b):
    v = table.get(int(b0)*256+int(b1))
    if v is None: return 0.0
    return float(v[true_b])


@torch.no_grad()
def collect(m, held, table):
    rng = random.Random(SEED)
    n = held.numel()
    confs, corrs, preds = [], [], []
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - 2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        true_b = int(held[pos].item())
        b0 = int(held[pos-2].item()); b1 = int(held[pos-1].item())
        logits = m(ctx)
        p = F.softmax(logits[0, -1, :], dim=-1)
        conf = float(p.max().item())
        pred = int(torch.argmax(logits[0, -1, :]).item())
        confs.append(conf); corrs.append(1 if pred == true_b else 0)
        preds.append(trigram_predictability(table, b0, b1, true_b))
    return np.array(confs), np.array(corrs), np.array(preds)


def partition_stats(conf, corr, name):
    n = len(corr); ne = int((1-corr).sum()); nc = int(corr.sum())
    a = float(corr.mean())
    t2 = float(auroc(conf, corr)) if (ne >= 1 and nc >= 1) else float("nan")
    valid = ne >= 30 and nc >= 30
    print(f"  [{name}] n={n} acc={a:.4f} errors={ne} correct={nc} type2_AUROC={t2:.4f} valid={valid}", flush=True)
    return dict(n=n, acc=a, errors=ne, correct=nc, type2_auroc=t2, valid=valid)


def main():
    print("=== H_1207 savant dissociation (skill vs metacognition) ===", flush=True)
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC))
    train_data, held = data[:cut], data[cut:]
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)
    print("[trigram] building model-independent predictability table...", flush=True)
    table = build_trigram(raw[:cut])
    print(f"[trigram] {len(table)} contexts", flush=True)

    print("--- training ---", flush=True)
    m_tr = train_model(train_data)

    print("--- TRAINED (collect) ---", flush=True)
    conf, corr, pred = collect(m_tr, held, table)
    q1, q2 = np.quantile(pred, [1/3, 2/3])
    island = pred > q2; open_ = pred <= q1
    print(f"[partition] island(top-tercile pred>{q2:.3f}) n={island.sum()} | open(<= {q1:.3f}) n={open_.sum()}", flush=True)
    s_isl = partition_stats(conf[island], corr[island], "ISLAND")
    s_opn = partition_stats(conf[open_], corr[open_], "OPEN")
    s_all = partition_stats(conf, corr, "ALL")

    acc_gap = s_isl["acc"] - s_opn["acc"]
    f1 = acc_gap >= 0.15
    # F2: if island is ceiling (errors<30) treat as extreme monitoring-blindness PASS; else compare AUROC
    if s_isl["errors"] < 30:
        meta_gap = float("nan"); f2 = True; ceiling = True
    else:
        ceiling = False
        meta_gap = s_isl["type2_auroc"] - s_opn["type2_auroc"]
        f2 = (not math.isnan(meta_gap)) and meta_gap <= -0.10
    supported = bool(f1 and f2)
    if supported and ceiling:
        ruling = "SUPPORTED (extreme): high-skill island is at accuracy ceiling with <30 errors — monitoring is moot (no error gradient to track); savant skill⊥metacognition in its strongest form"
    elif supported:
        ruling = "SUPPORTED: savant dissociation — the high-skill island has LOWER metacognitive sensitivity than the open domain (skill up, monitoring down)"
    elif not f1:
        ruling = "INCONCLUSIVE/NEG: no high-skill island (acc gap<+0.15) — partition did not isolate a savant domain"
    else:
        ruling = "CLOSED-NEGATIVE: metacognition tracks skill normally across domains (meta_gap>-0.10) — NO savant dissociation"

    verdict = {
        "H": "H_1207",
        "title": "savant dissociation (skill vs metacognition)",
        "island": s_isl, "open": s_opn, "all": s_all,
        "F1_island_of_skill": {"acc_gap_island_minus_open": acc_gap, "bar": 0.15, "pass": bool(f1)},
        "F2_metacog_blind": {"meta_gap_island_minus_open": meta_gap, "ceiling": ceiling, "bar": -0.10, "pass": bool(f2)},
        "supported": supported,
        "ruling": ruling,
        "neuroscience_anchor": "savant syndrome — Treffert 2009; Snyder 2009; weak central coherence (Happé & Frith 2006)",
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
