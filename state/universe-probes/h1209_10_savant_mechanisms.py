"""
H_1209 + H_1210 — SAVANT MECHANISMS (standalone, no metacognition lens)
Trains ONE ByteGPT and runs two savant-syndrome mechanism probes that share it.

H_1209 — SNYDER RELEASE / PRIVILEGED LOW-LEVEL ACCESS (Snyder 2009): savant skill
  = privileged access to lower-level (pre-conceptual) information. LOGIT-LENS test:
  on a rote/detail "island" (top-tercile corpus-trigram-predictable positions) the
  correct byte should be available EARLIER in the stack than on a gestalt-needing
  MED tercile. maturity(partition) = greedy-acc@layer2 / greedy-acc@final.
  FROZEN F1: maturity(ISLAND) - maturity(MED) >= +0.15 (detail matures earlier).

H_1210 — PARADOXICAL FUNCTIONAL FACILITATION (Kapur 1996; acquired savant, Treffert
  2009): damaging top-down machinery can SPARE/RELEASE a low-level detail skill.
  Ablate the LAST transformer block (most abstract) and re-measure greedy accuracy.
  Δacc(p) = acc_ablated(p) - acc_full(p).
  FROZEN F1: Δacc(ISLAND) >= -0.02 (detail preserved or improved) AND
             Δacc(ISLAND) - Δacc(MED) >= +0.10 (detail spared relative to gestalt).

Both: SUPPORTED iff their F1; CLOSED-NEGATIVE (a_paper_negative_ok) otherwise.
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
N_DEC = 4000
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
    def _embed(s, idx):
        T = idx.shape[1]; pos = torch.arange(T, device=idx.device)
        return s.tok(idx) + s.pos(pos)[None]
    def forward(s, idx):
        x = s._embed(idx)
        mask = torch.triu(torch.full((idx.shape[1],)*2, float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.lnf(x))
    def forward_lens(s, idx):
        """return per-block logit-lens logits at the LAST position (list len NLAYER)."""
        x = s._embed(idx)
        mask = torch.triu(torch.full((idx.shape[1],)*2, float("-inf"), device=idx.device), 1)
        outs = []
        for b in s.blocks:
            x = b(x, mask)
            outs.append(s.head(s.lnf(x))[0, -1, :])
        return outs
    def forward_ablate_last(s, idx):
        x = s._embed(idx)
        mask = torch.triu(torch.full((idx.shape[1],)*2, float("-inf"), device=idx.device), 1)
        for b in list(s.blocks)[:-1]: x = b(x, mask)   # skip last block
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
    v = table.get(int(b0)*256+int(b1));  return 0.0 if v is None else float(v[tb])


def save(slug, verdict):
    d = os.path.join(VDIR, slug); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "result.json"), "w") as f: json.dump(verdict, f, indent=2)
    print(f"[saved] {d}/result.json", flush=True)


@torch.no_grad()
def collect(m, held, table):
    rng = random.Random(SEED); n = held.numel()
    pos_list, tb_list, pred_list = [], [], []
    lens_acc = [[] for _ in range(NLAYER)]   # per-layer correctness
    full_corr, abl_corr = [], []
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - 2)
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        tb = int(held[pos].item()); b0 = int(held[pos-2].item()); b1 = int(held[pos-1].item())
        lens = m.forward_lens(ctx)
        for li in range(NLAYER):
            lens_acc[li].append(1 if int(torch.argmax(lens[li]).item()) == tb else 0)
        full_corr.append(1 if int(torch.argmax(lens[-1]).item()) == tb else 0)
        abl = m.forward_ablate_last(ctx)
        abl_corr.append(1 if int(torch.argmax(abl[0, -1, :]).item()) == tb else 0)
        pred_list.append(pred_of(table, b0, b1, tb))
    return (np.array(pred_list), [np.array(a) for a in lens_acc],
            np.array(full_corr), np.array(abl_corr))


def main():
    print("=== H_1209/1210 savant mechanisms (Snyder lens + paradoxical ablation) ===", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC)); train_data, held = data[:cut], data[cut:]
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)
    print("[trigram] building...", flush=True); table = build_trigram(raw[:cut]); print(f"[trigram] {len(table)} ctx", flush=True)
    print("--- training ---", flush=True); m = train_model(train_data)
    print("--- collect (lens + ablate) ---", flush=True)
    pred, lens_acc, full_corr, abl_corr = collect(m, held, table)
    q1, q2 = np.quantile(pred, [1/3, 2/3])
    isl = pred > q2; med = (pred > q1) & (pred <= q2); opn = pred <= q1
    def acc(mask, arr): return float(arr[mask].mean()) if mask.sum() else float("nan")

    # ---- H_1209 Snyder layer-lens maturity ----
    def maturity(mask):
        a2 = acc(mask, lens_acc[1]); a4 = acc(mask, lens_acc[-1])   # layer2 / final(layer4)
        return (a2 / a4) if a4 > 1e-6 else float("nan"), a2, a4
    m_isl, a2_isl, a4_isl = maturity(isl); m_med, a2_med, a4_med = maturity(med)
    print(f"[lens] ISLAND acc@L2={a2_isl:.4f} acc@L4={a4_isl:.4f} maturity={m_isl:.4f}", flush=True)
    print(f"[lens] MED    acc@L2={a2_med:.4f} acc@L4={a4_med:.4f} maturity={m_med:.4f}", flush=True)
    print(f"[lens] per-layer ISLAND acc: {[round(acc(isl,lens_acc[i]),3) for i in range(NLAYER)]}", flush=True)
    mat_gap = (m_isl - m_med) if not (math.isnan(m_isl) or math.isnan(m_med)) else float("nan")
    f1_09 = (not math.isnan(mat_gap)) and mat_gap >= 0.15
    save("1209_snyder_lowlevel_access", {
        "H": "H_1209", "title": "Snyder release / privileged low-level access (logit-lens)",
        "island_maturity": m_isl, "med_maturity": m_med, "maturity_gap": mat_gap,
        "island_per_layer_acc": [acc(isl, lens_acc[i]) for i in range(NLAYER)],
        "med_per_layer_acc": [acc(med, lens_acc[i]) for i in range(NLAYER)],
        "F1": {"maturity_gap": mat_gap, "bar": 0.15, "pass": bool(f1_09)},
        "supported": bool(f1_09),
        "ruling": ("SUPPORTED: detail (rote island) is available earlier in the stack than gestalt (MED) — Snyder privileged low-level access"
                   if f1_09 else "CLOSED-NEGATIVE: detail does not mature disproportionately early (maturity gap<+0.15) — no privileged low-level access signature"),
        "neuroscience_anchor": "Snyder 2009 release-from-concept / privileged access to lower-level info",
        "scope": "toy ByteGPT d256/4L CPU en slice — scale-up UNVERIFIED (a_scale_honest_scope)", "seed": SEED})

    # ---- H_1210 paradoxical functional facilitation ----
    def d_acc(mask): return acc(mask, abl_corr) - acc(mask, full_corr)
    d_isl = d_acc(isl); d_med = d_acc(med); d_opn = d_acc(opn)
    print(f"[ablate] full acc I/M/O = {acc(isl,full_corr):.4f}/{acc(med,full_corr):.4f}/{acc(opn,full_corr):.4f}", flush=True)
    print(f"[ablate] Δacc(last-block) I/M/O = {d_isl:+.4f}/{d_med:+.4f}/{d_opn:+.4f}", flush=True)
    spare_gap = d_isl - d_med
    f1_10 = (d_isl >= -0.02) and (spare_gap >= 0.10)
    save("1210_paradoxical_facilitation", {
        "H": "H_1210", "title": "paradoxical functional facilitation (top-block ablation)",
        "delta_acc_island": d_isl, "delta_acc_med": d_med, "delta_acc_open": d_opn, "spare_gap_island_minus_med": spare_gap,
        "full_acc": {"island": acc(isl,full_corr), "med": acc(med,full_corr), "open": acc(opn,full_corr)},
        "F1": {"delta_island": d_isl, "spare_gap": spare_gap, "bars": "Δisland>=-0.02 AND spare_gap>=0.10", "pass": bool(f1_10)},
        "supported": bool(f1_10),
        "ruling": ("SUPPORTED: ablating the top block spares/releases the detail island relative to gestalt — paradoxical functional facilitation"
                   if f1_10 else "CLOSED-NEGATIVE: top-block ablation does not spare detail relative to gestalt — no paradoxical facilitation"),
        "neuroscience_anchor": "paradoxical functional facilitation (Kapur 1996); acquired savant (Treffert 2009)",
        "scope": "toy ByteGPT d256/4L CPU en slice — scale-up UNVERIFIED (a_scale_honest_scope)", "seed": SEED})
    print("=== DONE H_1209/H_1210 ===", flush=True)


if __name__ == "__main__":
    main()
