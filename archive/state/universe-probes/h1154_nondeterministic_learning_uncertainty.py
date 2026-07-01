"""
H_1154 — NON-DETERMINISTIC LEARNING -> epistemic-uncertainty (ensemble disagreement)
as the metacog handle deterministic training lacked (H_1142/1143/1148).

CORRECTION baked in (user/repo): AKIDA is DETERMINISTIC (H_922); non-det = ANU QRNG
injected at the SEED lever. Quantum-vs-PRNG is a CLOSED-NEG (#1784, indistinguishable),
so the claim is about non-determinism-in-LEARNING STRUCTURE (ensemble spread), NOT
quantum superiority. We seed the QUANTUM arm from the committed ANU bytes
(qrng_lora_init_live.bin) and a PRNG arm from python RNG, and expect NO metacog
difference (secondary check that does NOT reopen #1784).

SIGNAL: BALD epistemic disagreement = H(mean_i p_i) - mean_i H(p_i) over N replicas
(each trained from a distinct seed). High = replicas disagree = "I don't know".

FROZEN FALSIFIER:
  F1: AUROC(disagreement ; label=UNKNOWN) >= 0.70  (KNOWN=corpus prefixes vs
      UNKNOWN=real-word salad; recovers H_1143's 0.564 failure)
  F2: Spearman(disagreement, fabrication) >= +0.30  (fabrication=corpus-absent
      content-ngram, recovers H_1148's +0.257 wrong-direction)
  CONTROL: UNTRAINED ensemble disagreement must FAIL F1 (AUROC <= 0.60) — the
      handle must come from LEARNED spread, not random-init geometry (where H_1143/1151 died)
  SUPPORTED iff F1 AND F2 AND control.
toy-scope (a_scale_honest_scope).
"""
import os, sys, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

DEV = "cpu"
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
QRNG_BIN = "/tmp/qrng_lora_init_live.bin"
EN_SLICE = 24 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
N_REP = 5                 # ensemble size per arm
N_PER_CLASS = 24; N_IDEA = 24
GEN_F1 = 20; GEN_F2 = 80; TEMP = 0.85; TOPK = 40
BASE_SEED = 7


class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.ln2 = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, h, batch_first=True)
        s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d))
    def forward(s, x, m):
        a, _ = s.attn(s.ln1(x), s.ln1(x), s.ln1(x), attn_mask=m, need_weights=False)
        x = x + a; return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=VOCAB, d=D, n_layer=NLAYER, n_head=NHEAD, block=BLOCK):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d)
        s.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        s.lnf = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False)
    def forward(s, idx, targets=None):
        T = idx.shape[1]
        x = s.tok(idx) + s.pos(torch.arange(T, device=idx.device))[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        logits = s.head(s.lnf(x))
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1)) if targets is not None else None
        return logits, loss


def batch(data, g):
    ix = torch.randint(0, data.numel()-BLOCK-1, (BS,), generator=g)
    x = torch.stack([data[i:i+BLOCK] for i in ix]).long()
    y = torch.stack([data[i+1:i+BLOCK+1] for i in ix]).long()
    return x.to(DEV), y.to(DEV)

def train_replica(data, seed, do_train=True):
    torch.manual_seed(seed); np.random.seed(seed % (2**31))
    m = ByteGPT().to(DEV)
    if not do_train:
        m.eval(); return m
    m.train(); opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    g = torch.Generator(device=DEV).manual_seed(seed)
    for st in range(STEPS):
        lr_t = LR*min(1.0, (st+1)/80)*(0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for pg in opt.param_groups: pg["lr"] = lr_t
        x, y = batch(data, g); _, l = m(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
    m.eval(); return m


def bald_and_gen(reps, prompt, gen_len, corpus_lower, dct, seed):
    """Shared rollout: each step sample next byte from ensemble-mean (temp), record BALD."""
    ids = torch.tensor([b for b in prompt.encode("utf-8", "ignore")[:BLOCK-gen_len-1]],
                       dtype=torch.long, device=DEV)[None]
    if ids.numel() == 0: ids = torch.zeros(1, 1, dtype=torch.long, device=DEV)
    g = torch.Generator(device=DEV).manual_seed(seed)
    balds, out = [], []
    with torch.no_grad():
        for _ in range(gen_len):
            ctx = ids[:, -BLOCK:]
            ps = []
            for m in reps:
                lg, _ = m(ctx); ps.append(F.softmax(lg[:, -1, :], -1)[0])
            P = torch.stack(ps)                         # [N,256]
            mean_p = P.mean(0)
            H_mean = float(-(mean_p*torch.log(mean_p+1e-12)).sum())
            H_each = float((-(P*torch.log(P+1e-12)).sum(-1)).mean())
            balds.append(H_mean - H_each)               # BALD = epistemic disagreement
            # sample next from mean_p with temp+topk
            logit = torch.log(mean_p+1e-12)/TEMP
            v, i = torch.topk(logit, TOPK)
            nxt = i[torch.multinomial(F.softmax(v, -1), 1, generator=g)]
            ids = torch.cat([ids, nxt.view(1, 1)], 1); out.append(int(nxt.item()))
    text = bytes(out).decode("utf-8", "ignore")
    # fabrication = corpus-absent content bigram/trigram fraction (in-memory substring)
    words = [w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split()
             if len(w) >= 3 and w in dct]
    grams = [" ".join(words[k:k+n]) for n in (2, 3) for k in range(len(words)-n+1)]
    fab = (sum(1 for gm in grams if gm not in corpus_lower)/len(grams)) if grams else 0.0
    return float(np.mean(balds)), fab


def auroc(scores, labels):
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    order = np.argsort(s); r = np.empty(len(s)); r[order] = np.arange(1, len(s)+1)
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    rs = np.zeros(len(cnt)); np.add.at(rs, inv, r); r = (rs/cnt)[inv]
    n1 = y.sum(); n0 = len(y)-n1
    return float("nan") if n1 == 0 or n0 == 0 else (r[y == 1].sum()-n1*(n1+1)/2)/(n1*n0)

def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean(); d = math.sqrt((ra*ra).sum()*(rb*rb).sum())
    return float((ra*rb).sum()/d) if d else 0.0


def qrng_seeds(n):
    try:
        b = open(QRNG_BIN, "rb").read()
        return [BASE_SEED + int.from_bytes(b[i*4:i*4+4], "little") % (2**31) for i in range(n)]
    except Exception:
        return None

def prng_seeds(n):
    rng = random.Random(BASE_SEED)
    return [rng.randint(1, 2**31-1) for _ in range(n)]


def eval_arm(data, seeds, known, unknown, ideas, corpus_lower, dct, tag, do_train=True):
    reps = [train_replica(data, sd, do_train) for sd in seeds]
    print(f"  [{tag}] trained {len(reps)} replicas (do_train={do_train})", flush=True)
    dis_k = [bald_and_gen(reps, p, GEN_F1, corpus_lower, dct, BASE_SEED+j)[0] for j, p in enumerate(known)]
    dis_u = [bald_and_gen(reps, p, GEN_F1, corpus_lower, dct, BASE_SEED+100+j)[0] for j, p in enumerate(unknown)]
    au = auroc(dis_k+dis_u, [0]*len(dis_k)+[1]*len(dis_u))
    dis_i, fab_i = [], []
    for j, p in enumerate(ideas):
        d_, f_ = bald_and_gen(reps, p, GEN_F2, corpus_lower, dct, BASE_SEED+200+j)
        dis_i.append(d_); fab_i.append(f_)
    rho = spearman(dis_i, fab_i)
    print(f"  [{tag}] F1 AUROC={au:.4f}  F2 Spearman(dis,fab)={rho:.4f}  mean_fab={np.mean(fab_i):.3f}", flush=True)
    return {"auroc": au, "spearman_dis_fab": rho, "mean_fab": float(np.mean(fab_i))}


def main():
    print("=== H_1154 non-deterministic learning -> epistemic uncertainty ===", flush=True)
    raw = open(CORPUS, "rb").read(EN_SLICE)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8)
    text = raw.decode("utf-8", "ignore"); corpus_lower = text.lower()
    dct = ({w.strip().lower() for w in open("/usr/share/dict/words", encoding="utf-8", errors="ignore")
            if w.strip().isalpha() and len(w.strip()) >= 3}
           if os.path.exists("/usr/share/dict/words") else set())
    from collections import Counter
    cw = Counter(w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split() if len(w) >= 3)
    salad = sorted({w for w, c in cw.items() if c >= 5}) or ["the", "and"]
    if not dct: dct = set(salad)
    rng = random.Random(BASE_SEED)
    lines = [ln.strip() for ln in text.split("\n") if len(ln.strip()) >= 60 and ln.strip().isascii()]
    rng.shuffle(lines)
    known = [ln[:50] for ln in lines[:N_PER_CLASS]]
    unknown = []
    for _ in range(N_PER_CLASS):
        s, w = "", []
        while len(s) < 50: w.append(rng.choice(salad)); s = " ".join(w)
        unknown.append(s[:50])
    CN = ["consciousness","tension","memory","silence","engine","cell","mitosis","curiosity",
          "anchor","dream","field","emergence","novelty","coherence","substrate"]
    ideas = [f"What links {a} and {b}? " for a, b in (rng.sample(CN, 2) for _ in range(N_IDEA))]

    qs = qrng_seeds(N_REP); ps = prng_seeds(N_REP)
    qsrc = "ANU-QRNG-bytes" if qs else "PRNG-fallback(qrng bin missing)"
    if qs is None: qs = prng_seeds(N_REP)
    print(f"[seeds] quantum-arm={qsrc} {qs}\n        prng-arm={ps}", flush=True)

    print("\n--- CONTROL: untrained ensemble ---", flush=True)
    ctrl = eval_arm(data, qs, known, unknown, ideas, corpus_lower, dct, "untrained", do_train=False)
    print("\n--- QUANTUM-seeded trained ensemble (primary) ---", flush=True)
    q = eval_arm(data, qs, known, unknown, ideas, corpus_lower, dct, "quantum")
    print("\n--- PRNG-seeded trained ensemble (q-vs-PRNG appendix) ---", flush=True)
    pr = eval_arm(data, ps, known, unknown, ideas, corpus_lower, dct, "prng")

    f1 = q["auroc"] >= 0.70
    f2 = q["spearman_dis_fab"] >= 0.30
    ctl = ctrl["auroc"] <= 0.60
    supported = bool(f1 and f2 and ctl)
    verdict = {
        "H": "H_1154", "title": "non-deterministic learning -> epistemic uncertainty (ensemble disagreement)",
        "F1_familiarity": {"auroc": q["auroc"], "bar": 0.70, "pass": bool(f1)},
        "F2_fabrication": {"spearman_dis_fab": q["spearman_dis_fab"], "bar": 0.30, "pass": bool(f2)},
        "control_untrained": {"auroc": ctrl["auroc"], "bar_max": 0.60, "pass": bool(ctl)},
        "q_vs_prng_appendix": {"quantum": q, "prng": pr,
            "delta_auroc": q["auroc"]-pr["auroc"], "delta_rho": q["spearman_dis_fab"]-pr["spearman_dis_fab"],
            "note": "expect ~0 per #1784 (quantum no advantage); large delta would REOPEN #1784"},
        "h1143_ref_auroc": 0.564, "h1148_ref_rho": 0.257,
        "supported": supported,
        "ruling": ("SUPPORTED: non-det LEARNING ensemble disagreement recovers the metacog handle"
                   if supported else
                   "CLOSED-NEGATIVE: non-det learning disagreement does NOT give the metacog handle "
                   "(the gap is architectural, not a determinism artifact)"),
        "scope": "toy ByteGPT d256/4L CPU en-24MB, N_REP=5/arm — scale-up UNVERIFIED (a_scale_honest_scope)",
    }
    print("\n=== VERDICT ===\n"+json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1154_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1154_result.json", flush=True)


if __name__ == "__main__": main()
