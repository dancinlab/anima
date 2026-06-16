"""
H_1143 — HIDDEN-STATE OOD DETECTOR BEATS BYTE-ENTROPY for input-familiarity metacog.
Constructive follow-up that CLOSES the H_1142 F1 negative (byte-entropy AUROC 0.436,
BELOW chance, on KNOWN-vs-UNKNOWN input discrimination).

CLAIM: the substrate DOES carry an input-familiarity signal — just not in next-byte
entropy. It is in the HIDDEN STATE's distance from the training manifold. Replace the
confidence signal with last-layer hidden-state kNN distance to a reference set of
in-corpus activations; test whether THAT discriminates familiar/unfamiliar input.

FROZEN FALSIFIER (pre-registered, deterministic):
  F1' OOD-DISCRIMINATION — AUROC(ood_distance ; label=UNKNOWN) >= 0.70
       (same KNOWN=in-corpus prefixes vs UNKNOWN=real-word salad as H_1142).
  HEAD-TO-HEAD — ood_auroc must BEAT the byte-entropy auroc on the SAME prompts by
       >= +0.15 (else the hidden state adds nothing over entropy).
  F3 ANTI-GOODHART — UNTRAINED backbone ood AUROC <= 0.60 (manifold must be LEARNED).
  H_1143 SUPPORTED iff F1' AND head-to-head AND F3.
  CLOSED-NEGATIVE (a_paper_negative_ok) iff the hidden state ALSO fails to discriminate
       => input-familiarity metacog is genuinely absent at toy scale, not just mis-read.

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice. xref H_1142.
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
        return s.lnf(x)                       # [B,T,D] last-layer hidden
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
    h = m.hidden(ids)                          # [1,T,D]
    return h[0].mean(0).cpu().numpy()          # mean-pooled prompt representation [D]


@torch.no_grad()
def gen_entropy(m, prompt):
    ids = torch.tensor([b for b in prompt.encode("utf-8", "ignore")[:BLOCK-GEN_LEN-1]], dtype=torch.long, device=DEV)[None]
    g = torch.Generator(device=DEV).manual_seed(SEED + len(prompt)); ents = []
    for _ in range(GEN_LEN):
        logits, _ = m(ids[:, -BLOCK:]); logp = F.log_softmax(logits[:, -1, :], -1); p = logp.exp()
        ents.append(float(-(p*logp).sum().item()))
        v, i = torch.topk(logits[:, -1, :]/GEN_TEMP, TOPK)
        nxt = i.gather(-1, torch.multinomial(F.softmax(v, -1), 1, generator=g)); ids = torch.cat([ids, nxt], 1)
    return float(np.mean(ents))


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
    ref = [ln[:50] for ln in lines[:N_REF]]                 # manifold reference (in-corpus)
    known = [ln[:50] for ln in lines[N_REF:N_REF+N_PER_CLASS]]
    unknown = []
    for _ in range(N_PER_CLASS):
        s, w = "", []
        while len(s) < 50: w.append(rng.choice(salad_vocab)); s = " ".join(w)
        unknown.append(s[:50])
    return ref, known, unknown


def ood_distance(rep, ref_mat):
    d = np.linalg.norm(ref_mat - rep[None], axis=1)         # kNN mean distance to manifold
    return float(np.sort(d)[:KNN].mean())


def evaluate(m, ref, known, unknown, tag):
    ref_mat = np.stack([prompt_hidden(m, p) for p in ref])
    rows = []
    for p in known:   rows.append((ood_distance(prompt_hidden(m, p), ref_mat), gen_entropy(m, p), 0))
    for p in unknown: rows.append((ood_distance(prompt_hidden(m, p), ref_mat), gen_entropy(m, p), 1))
    ood = [r[0] for r in rows]; ent = [r[1] for r in rows]; lab = [r[2] for r in rows]
    au_ood = auroc(ood, lab); au_ent = auroc(ent, lab)
    print(f"  [{tag}] AUROC ood={au_ood:.4f}  entropy={au_ent:.4f}  delta={au_ood-au_ent:+.4f}", flush=True)
    return {"ood_auroc": au_ood, "entropy_auroc": au_ent, "delta": au_ood-au_ent}


def main():
    print("=== H_1143 hidden-state OOD vs byte-entropy (closes H_1142 F1) ===", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8); text = raw.decode("utf-8", "ignore")
    from collections import Counter
    cw = Counter(w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split() if len(w) >= 3)
    salad = sorted({w for w, c in cw.items() if c >= 5}) or ["the", "and", "for"]
    ref, known, unknown = build_prompts(text, salad)
    print(f"[prompts] {len(ref)} manifold-ref, {len(known)} KNOWN, {len(unknown)} UNKNOWN", flush=True)

    print("\n--- F3 control: UNTRAINED ---", flush=True)
    torch.manual_seed(SEED); ctrl = evaluate(ByteGPT().to(DEV).eval(), ref, known, unknown, "untrained")
    print("\n--- training ---", flush=True); m = train_model(data)
    print("\n--- TRAINED ---", flush=True); tr = evaluate(m, ref, known, unknown, "trained")

    f1 = tr["ood_auroc"] >= 0.70
    h2h = tr["delta"] >= 0.15
    f3 = ctrl["ood_auroc"] <= 0.60
    supported = bool(f1 and h2h and f3)
    verdict = {
        "H": "H_1143", "title": "hidden-state OOD beats byte-entropy for input-familiarity metacog",
        "F1prime_ood_discrimination": {"ood_auroc": tr["ood_auroc"], "bar": 0.70, "pass": bool(f1)},
        "head_to_head_vs_entropy": {"ood": tr["ood_auroc"], "entropy": tr["entropy_auroc"],
                                    "delta": tr["delta"], "bar": 0.15, "pass": bool(h2h)},
        "F3_control": {"untrained_ood_auroc": ctrl["ood_auroc"], "bar_max": 0.60, "pass": bool(f3)},
        "h1142_entropy_reference": 0.436,
        "supported": supported,
        "ruling": ("CLOSES H_1142: hidden-state OOD recovers input-familiarity metacog the entropy missed"
                   if supported else "CLOSED-NEGATIVE: hidden state ALSO fails — input-familiarity metacog genuinely absent at toy scale"),
        "scope": "toy ByteGPT d256/4L CPU en slice — scale-up UNVERIFIED (a_scale_honest_scope)",
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1143_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1143_result.json", flush=True)


if __name__ == "__main__": main()
