"""
H_1151 — HIPPOCAMPAL DG PATTERN SEPARATION recovers learned input-familiarity
that the DENSE hidden state (H_1143) could not.

NEUROSCIENCE GROUNDING: the dentate gyrus (DG) performs PATTERN SEPARATION —
it orthogonalizes similar inputs into SPARSE, EXPANSIVE, decorrelated codes
(Marr 1971; Treves & Rolls; O'Reilly & McClelland), while CA3 does pattern
completion/retrieval. A novelty/familiarity signal arises from DG mismatch.

H_1143 found input-familiarity UNDETECTABLE in the DENSE mean-pooled hidden
state: trained ood AUROC 0.564, and an UNTRAINED backbone ALREADY scored 0.71
(the separation was surface-statistics, not learned).

HYPOTHESIS: a DG-style SPARSE EXPANSIVE recode of the hidden state recovers a
LEARNED input-familiarity discrimination the dense code failed at.
  DG code = fixed random expansive projection (~10x dim) + k-winners-take-all
  (keep top ~5% units active). familiarity = kNN distance of the DG-sparse code
  to an in-corpus DG-code reference manifold. Same FIXED DG projection on the
  trained AND untrained backbone (the control).

FROZEN FALSIFIER (pre-registered, deterministic — see .discoveries/1151_*.tape):
  F1            DG-sparse familiarity AUROC >= 0.70 (beats H_1143 dense 0.564).
  HEAD-TO-HEAD  DG-sparse AUROC must BEAT the dense-hidden AUROC on the SAME
                prompts by >= +0.10 (else the DG recode adds nothing).
  CONTROL       ANTI-GOODHART (load-bearing, where H_1143 died): UNTRAINED
                backbone DG-sparse AUROC <= 0.60. If untrained ALSO separates,
                the DG code is surface-statistics, not learned -> CLOSED-NEGATIVE.
  H_1151 SUPPORTED iff F1 AND head-to-head AND control.
  CLOSED-NEGATIVE (a_paper_negative_ok) otherwise.

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice. seed 7. xref H_1143.
Reuses h1143 machinery VERBATIM and ADDS the DG sparse-expansive recode.
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
N_REF = 60; N_PER_CLASS = 30; GEN_LEN = 80; GEN_TEMP = 0.7; TOPK = 40; KNN = 5

# --- DG pattern-separation params (canonical DG model) ---
DG_DIM = D * 10          # expansive projection ~10x (256 -> 2560)
DG_ACTIVE_FRAC = 0.05    # k-winners-take-all: keep top ~5% units active
DG_K = max(1, int(round(DG_DIM * DG_ACTIVE_FRAC)))  # 128 active units


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
    def hidden(s, idx):
        B, T = idx.shape
        x = s.tok(idx) + s.pos(torch.arange(T, device=idx.device))[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        return s.lnf(x)
    def forward(s, idx, targets=None):
        h = s.hidden(idx); logits = s.head(h)
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1)) if targets is not None else None
        return logits, loss


def batch(data, block, bs, dev):
    ix = torch.randint(0, data.numel() - block - 1, (bs,))
    x = torch.stack([data[i:i+block] for i in ix]).long()
    y = torch.stack([data[i+1:i+block+1] for i in ix]).long()
    return x.to(dev), y.to(dev)


def train_model(data):
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for g in opt.param_groups: g["lr"] = lr_t
        x, y = batch(data, BLOCK, BS, DEV); _, l = m(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 500 == 0 or st == STEPS-1: print(f"  [train] step {st} ce={l.item():.4f}", flush=True)
    m.eval(); return m


@torch.no_grad()
def prompt_hidden(m, prompt):
    ids = torch.tensor([b for b in prompt.encode("utf-8", "ignore")[:60]], dtype=torch.long, device=DEV)[None]
    if ids.numel() == 0: ids = torch.zeros(1, 1, dtype=torch.long, device=DEV)
    h = m.hidden(ids)
    return h[0].mean(0).cpu().numpy()          # dense mean-pooled prompt representation [D]


# ── DG pattern-separation recode ─────────────────────────────────────────────
# FIXED random expansive projection W (D -> DG_DIM), seeded once, identical for
# trained AND untrained backbone (no learning in the DG layer — that is the point;
# DG is a fixed sparse-expansive coding stage, not a trained readout). kWTA keeps
# the top-K activations and zeroes the rest -> sparse, expansive, decorrelated code.
def make_dg_projection():
    g = np.random.RandomState(SEED + 1234)
    # random Gaussian projection, columns unit-normalized (standard DG random-projection model)
    W = g.randn(D, DG_DIM).astype(np.float64)
    W /= (np.linalg.norm(W, axis=0, keepdims=True) + 1e-12)
    return W

DG_W = make_dg_projection()

def dg_code(rep):
    # rep: dense [D]. expand -> kWTA top-K -> sparse [DG_DIM]
    z = rep @ DG_W                              # expansive projection [DG_DIM]
    out = np.zeros_like(z)
    if DG_K < z.size:
        idx = np.argpartition(z, -DG_K)[-DG_K:] # indices of top-K activations
    else:
        idx = np.arange(z.size)
    out[idx] = z[idx]                           # kWTA: keep top-K, zero rest
    return out


def auroc(scores, labels):
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    order = np.argsort(s); ranks = np.empty(len(s), float); ranks[order] = np.arange(1, len(s)+1)
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    rsum = np.zeros(len(cnt)); np.add.at(rsum, inv, ranks); ranks = (rsum/cnt)[inv]
    n1 = y.sum(); n0 = len(y)-n1
    return float("nan") if n1 == 0 or n0 == 0 else (ranks[y == 1].sum() - n1*(n1+1)/2)/(n1*n0)


def build_prompts(text, salad_vocab):
    rng = random.Random(SEED)
    lines = [ln.strip() for ln in text.split("\n") if len(ln.strip()) >= 60 and ln.strip().isascii()]
    rng.shuffle(lines)
    ref = [ln[:50] for ln in lines[:N_REF]]
    known = [ln[:50] for ln in lines[N_REF:N_REF+N_PER_CLASS]]
    unknown = []
    for _ in range(N_PER_CLASS):
        s, w = "", []
        while len(s) < 50: w.append(rng.choice(salad_vocab)); s = " ".join(w)
        unknown.append(s[:50])
    return ref, known, unknown


def knn_distance(rep, ref_mat):
    d = np.linalg.norm(ref_mat - rep[None], axis=1)
    return float(np.sort(d)[:KNN].mean())


def evaluate(m, ref, known, unknown, tag):
    # dense reps + DG-sparse reps for ref manifold and both classes
    ref_dense = np.stack([prompt_hidden(m, p) for p in ref])
    ref_dg    = np.stack([dg_code(r) for r in ref_dense])
    dense_scores, dg_scores, labels = [], [], []
    for cls, plist in ((0, known), (1, unknown)):
        for p in plist:
            d = prompt_hidden(m, p)
            dense_scores.append(knn_distance(d, ref_dense))
            dg_scores.append(knn_distance(dg_code(d), ref_dg))
            labels.append(cls)
    au_dense = auroc(dense_scores, labels)
    au_dg    = auroc(dg_scores, labels)
    print(f"  [{tag}] AUROC dense={au_dense:.4f}  DG-sparse={au_dg:.4f}  delta(DG-dense)={au_dg-au_dense:+.4f}", flush=True)
    return {"dense_auroc": au_dense, "dg_auroc": au_dg, "delta": au_dg - au_dense}


def main():
    print("=== H_1151 DG pattern separation vs dense hidden-state (follows H_1143) ===", flush=True)
    print(f"[DG] expand D={D} -> {DG_DIM} ({DG_DIM//D}x), kWTA top-K={DG_K} ({DG_ACTIVE_FRAC*100:.0f}% active)", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8); text = raw.decode("utf-8", "ignore")
    from collections import Counter
    cw = Counter(w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split() if len(w) >= 3)
    salad = sorted({w for w, c in cw.items() if c >= 5}) or ["the", "and", "for"]
    ref, known, unknown = build_prompts(text, salad)
    print(f"[prompts] {len(ref)} manifold-ref, {len(known)} KNOWN, {len(unknown)} UNKNOWN", flush=True)

    print("\n--- CONTROL: UNTRAINED backbone (anti-Goodhart) ---", flush=True)
    torch.manual_seed(SEED); ctrl = evaluate(ByteGPT().to(DEV).eval(), ref, known, unknown, "untrained")

    print("\n--- training ---", flush=True); m = train_model(data)
    print("\n--- TRAINED backbone ---", flush=True); tr = evaluate(m, ref, known, unknown, "trained")

    f1  = tr["dg_auroc"] >= 0.70
    h2h = tr["delta"] >= 0.10
    ctl = ctrl["dg_auroc"] <= 0.60
    supported = bool(f1 and h2h and ctl)
    verdict = {
        "H": "H_1151",
        "title": "hippocampal DG pattern separation recovers learned input-familiarity the dense hidden state missed",
        "DG_params": {"expand_dim": DG_DIM, "expand_x": DG_DIM // D, "kwta_K": DG_K, "active_frac": DG_ACTIVE_FRAC},
        "F1_dg_discrimination": {"dg_auroc": tr["dg_auroc"], "bar": 0.70, "pass": bool(f1)},
        "head_to_head_dg_vs_dense": {"dg": tr["dg_auroc"], "dense": tr["dense_auroc"],
                                     "delta": tr["delta"], "bar": 0.10, "pass": bool(h2h)},
        "control_untrained": {"untrained_dg_auroc": ctrl["dg_auroc"], "untrained_dense_auroc": ctrl["dense_auroc"],
                              "bar_max": 0.60, "pass": bool(ctl)},
        "h1143_dense_reference": {"trained_dense_auroc": 0.5644, "untrained_dense_auroc": 0.71},
        "supported": supported,
        "ruling": ("SUPPORTED: DG sparse-expansive recode RECOVERS learned input-familiarity that the dense hidden state missed"
                   if supported else
                   "CLOSED-NEGATIVE (a_paper_negative_ok): DG code fails the conjunction — "
                   + ("untrained also separates (surface-statistics, not learned) " if not ctl else "")
                   + ("DG AUROC below 0.70 " if not f1 else "")
                   + ("no >=+0.10 lift over dense " if not h2h else "")
                   + "-> DG pattern separation does NOT recover a learned familiarity signal at toy scale"),
        "scope": "toy ByteGPT d256/4L CPU en slice — scale-up UNVERIFIED (a_scale_honest_scope), seed 7, g5/p7",
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1151_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1151_result.json", flush=True)


if __name__ == "__main__": main()
