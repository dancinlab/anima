"""
H_1224 — SAVANT SPECIALIZATION TRADE-OFF (deficit-pairing / resource competition)
A hallmark of savant syndrome is the PAIRING of an extraordinary narrow skill with
BROAD deficit — the talent appears to come AT A COST (resource-competition /
trade-off view; the "savant deficit pairing"). Within a fixed-capacity substrate,
does forcing specialization on the rote "island" PURCHASE that skill by LOSING
open-domain coverage?

TASK: two arms, SAME architecture/capacity, SAME held-out eval points.
  Arm A BROAD       — train sampling windows uniformly.
  Arm B ROTE-BIASED — train sampling biased toward high-trigram-predictability
                      (rote/structured) windows (top-half rote-score pool).
Measure each arm's island_acc (high-pred tercile) and open_acc (low-pred tercile).

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 TRADE-OFF — (B_island_acc - A_island_acc) >= +0.03  AND
                 (A_open_acc  - B_open_acc)  >= +0.03
                 (rote specialization GAINS on the island WHILE LOSING the open
                 domain — a genuine deficit-pairing trade-off).
  H_1224 SUPPORTED iff F1.
  CLOSED-NEGATIVE (a_paper_negative_ok) iff no trade-off — specialization is free
  (island up without open cost) or absent. No resource-competition deficit-pairing.

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice, 2 arms. From H_1142.
"""
import os, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
DEV = "cpu"
CORPUS = os.environ.get("CORPUS", "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt")
EN_SLICE_BYTES = 24 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1200; BS = 16; LR = 3e-4
N_DEC = 3000; HELDOUT_FRAC = 0.10; POOL = 20000
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1224_savant_specialization_tradeoff")


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


def pred_of(table, b0, b1, tb):
    v = table.get(int(b0)*256+int(b1)); return 0.0 if v is None else float(v[tb])


def window_rote_score(data_np, table, s):
    seg = data_np[s:s+BLOCK]
    tot = 0.0
    for k in range(2, len(seg)):
        tot += pred_of(table, seg[k-2], seg[k-1], seg[k])
    return tot / (len(seg) - 2)


def train_arm(data, starts, weights, tag):
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    npr = np.random.RandomState(SEED)
    t0 = time.time()
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for g in opt.param_groups: g["lr"] = lr_t
        idx_sel = npr.choice(len(starts), size=BS, p=weights)
        ss = [starts[i] for i in idx_sel]
        x = torch.stack([data[s:s+BLOCK] for s in ss]).long().to(DEV)
        y = torch.stack([data[s+1:s+BLOCK+1] for s in ss]).long().to(DEV)
        l = m.loss_on(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 400 == 0 or st == STEPS-1:
            print(f"  [{tag} train] step {st} ce={l.item():.4f} {(time.time()-t0)/60:.1f}min", flush=True)
    m.eval(); return m


@torch.no_grad()
def eval_terciles(m, held, table, positions, q1, q2, preds):
    isl_ok, opn_ok = [], []
    for idx, pos in enumerate(positions):
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        tb = int(held[pos].item())
        pred = int(torch.argmax(m(ctx)[0, -1, :]).item())
        ok = 1 if pred == tb else 0
        if preds[idx] > q2: isl_ok.append(ok)
        elif preds[idx] <= q1: opn_ok.append(ok)
    return float(np.mean(isl_ok)) if isl_ok else float("nan"), float(np.mean(opn_ok)) if opn_ok else float("nan")


def main():
    print("=== H_1224 savant specialization trade-off (deficit-pairing) ===", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC)); train_data, held = data[:cut], data[cut:]
    data_np = np.frombuffer(raw[:cut], dtype=np.uint8)
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)
    table = build_trigram(raw[:cut]); print(f"[trigram] {len(table)} ctx", flush=True)

    # candidate window pool + rote scores
    npr = np.random.RandomState(SEED); n = train_data.numel()
    starts = [int(npr.randint(0, n - BLOCK - 1)) for _ in range(POOL)]
    print("[pool] scoring rote of windows...", flush=True)
    rote = np.array([window_rote_score(data_np, table, s) for s in starts])
    w_uniform = np.ones(POOL) / POOL
    # rote-biased: weight by rote^3 (sharpen toward high-predictability windows)
    rb = np.power(np.clip(rote, 1e-6, None), 3.0); w_rote = rb / rb.sum()
    print(f"[pool] rote mean={rote.mean():.3f} | rote-biased eff mean={float((rote*w_rote).sum()):.3f}", flush=True)

    # held-out eval points + their predictability terciles
    rng = random.Random(SEED); hn = held.numel()
    positions = [rng.randint(BLOCK, hn - 2) for _ in range(N_DEC)]
    preds = np.array([pred_of(table, int(held[p-2]), int(held[p-1]), int(held[p])) for p in positions])
    q1, q2 = np.quantile(preds, [1/3, 2/3])

    print("--- Arm A BROAD ---", flush=True)
    mA = train_arm(train_data, starts, w_uniform, "A-broad")
    A_isl, A_opn = eval_terciles(mA, held, table, positions, q1, q2, preds)
    print(f"  [A] island_acc={A_isl:.4f} open_acc={A_opn:.4f}", flush=True)

    print("--- Arm B ROTE-BIASED ---", flush=True)
    mB = train_arm(train_data, starts, w_rote, "B-rote")
    B_isl, B_opn = eval_terciles(mB, held, table, positions, q1, q2, preds)
    print(f"  [B] island_acc={B_isl:.4f} open_acc={B_opn:.4f}", flush=True)

    island_gain = B_isl - A_isl
    open_cost = A_opn - B_opn
    f1 = (island_gain >= 0.03) and (open_cost >= 0.03)
    supported = bool(f1)
    if supported:
        ruling = f"SUPPORTED: rote specialization trades off — island gain +{island_gain:.3f} bought at open cost +{open_cost:.3f} (savant deficit-pairing / resource competition)"
    elif island_gain < 0.03:
        ruling = f"CLOSED-NEGATIVE: rote-biasing did not specialize the island (gain {island_gain:.3f} < 0.03) — no trade-off measurable"
    else:
        ruling = f"CLOSED-NEGATIVE: island gained ({island_gain:.3f}) WITHOUT open cost ({open_cost:.3f} < 0.03) — specialization is free, no deficit-pairing"

    verdict = {
        "H": "H_1224", "title": "savant specialization trade-off (deficit-pairing)",
        "A_broad": {"island_acc": A_isl, "open_acc": A_opn},
        "B_rote": {"island_acc": B_isl, "open_acc": B_opn},
        "island_gain_B_minus_A": island_gain, "open_cost_A_minus_B": open_cost,
        "F1_tradeoff": {"island_gain": island_gain, "open_cost": open_cost, "bar": 0.03, "pass": bool(f1)},
        "supported": supported, "ruling": ruling,
        "neuroscience_anchor": "savant deficit-pairing / resource-competition (Treffert 2009; talent⊥general-ability)",
        "scope": "toy ByteGPT d256/4L CPU en slice, 2 arms — UNVERIFIED scale (a_scale_honest_scope)", "seed": SEED,
    }
    print("=== VERDICT ===", flush=True); print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(verdict, open(os.path.join(OUTDIR, "result.json"), "w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
