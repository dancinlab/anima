#!/usr/bin/env python3
"""h1229_developmental_order.py — HD20 DEVELOPMENTAL LEARNING-ORDER probe ($0, CPU, p7).

Foreign-domain (biology/development) lens HD20 from
.verdicts/1226_foreign_domain_depth_lens/H_1226.txt — NOT an LLM training-recipe (c15).

HYPOTHESIS: depth/composition needs ORDERED, developmentally-STAGED learning (easy->hard,
critical-period / Piaget-stage windows), not the flat UNORDERED single-pass the byte-LM got.

DESIGN (frozen in .verdicts/1229_developmental_order/H_1229_FREEZE.txt BEFORE any score):
  tiny PURE-NUMPY windowed byte-MLP (K=8 prev bytes one-hot -> H=64 tanh -> V=256 softmax),
  trained by SGD+momentum on serving/corpus/anima_7b_webscale.en.head.txt (English webscale).
  THREE arms, identical model init + hyperparams + step/token budget, differ ONLY in ORDER:
    (A) FLAT-SHUFFLED   — sample windows uniformly from ALL lines.
    (B) CURRICULUM      — easy->hard staged unlock (4 difficulty quartiles, window s uses 0..s).
    (C) ANTI-CURRICULUM — hard->easy staged unlock (reversed stage order).
  difficulty(line) = z(len) + z(rarity=-log p(byte) mean) + z(syntax=punct density).

EVAL (held-out last 10% bytes, p7, NOT perplexity/LLM-judge):
  composed_distinct (H_1158-style: coherent kwr + corpus-absent 4-gram + mutually-distinct),
  coherence (G0 kwr), qa_proxy (held-out next-byte top-1 accuracy).

VERDICT (frozen): GREEN iff (B beats A by margin on composed_distinct OR coherence) AND
  (C not better than A on both) => developmental ORDER is the lever (toy-only). Else 🔴 CLOSED-NEG.

a_toy_scale_recheck: toy-only; scale-transfer UNVERIFIED. p8: gradient-free of live .hexa.
"""
from __future__ import annotations
import os, sys, json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "serving", "corpus", "anima_7b_webscale.en.head.txt")
OUTDIR = os.path.join(ROOT, ".verdicts", "1229_developmental_order")

# ── frozen hyperparams ──
K = 8                 # context window (prev bytes)
H = 64                # hidden units
V = 256               # byte vocab
STEPS = 4000          # SGD steps per arm (EQUAL across arms)
BS = 64               # minibatch windows per step
LR = 0.30
MOM = 0.9
N_STAGES = 4
HELDOUT_FRAC = 0.10
SEEDS = (7, 17, 29)
# eval
N_SEED_CTX = 40       # held-out seed contexts for decode
N_GEN = 24            # bytes decoded per continuation
DEC_TEMP = 0.7
KWR_BAR = 0.50        # coherent if known-word-ratio >= this
JACCARD = 0.50        # mutually distinct if token Jaccard <= this


# ───────────────────────── corpus / difficulty ─────────────────────────
def load_corpus():
    raw = open(CORPUS, "rb").read()
    text = raw.decode("utf-8", errors="replace")
    return raw, text


def build_word_set(text):
    import re
    words = re.findall(r"[a-zA-Z]+", text.lower())
    from collections import Counter
    c = Counter(words)
    # keep words appearing >=2 times and length>=2 (corpus-derived English lexicon)
    return set(w for w, n in c.items() if n >= 2 and len(w) >= 2)


def byte_neglogp(raw):
    counts = np.bincount(np.frombuffer(raw, dtype=np.uint8), minlength=256).astype(np.float64)
    p = counts / counts.sum()
    nlp = np.full(256, 30.0)
    nz = p > 0
    nlp[nz] = -np.log(p[nz])
    return nlp  # per-byte -log p


def z(x):
    x = np.asarray(x, float)
    s = x.std()
    return (x - x.mean()) / (s + 1e-9)


def line_difficulty(lines, nlp):
    lengths, rarity, syntax = [], [], []
    for ln in lines:
        b = ln.encode("utf-8", errors="replace")
        if len(b) == 0:
            lengths.append(0); rarity.append(0); syntax.append(0); continue
        arr = np.frombuffer(b, dtype=np.uint8)
        lengths.append(len(b))
        rarity.append(float(nlp[arr].mean()))
        # non-alphanumeric, non-space density
        npunct = sum(1 for c in b if not (chr(c).isalnum() or chr(c) == " "))
        syntax.append(npunct / len(b))
    diff = z(lengths) + z(rarity) + z(syntax)
    return diff, (lengths, rarity, syntax)


# ───────────────────────── model (pure numpy) ─────────────────────────
class ByteMLP:
    """K prev bytes one-hot (K*V) -> H tanh -> V softmax. SGD+momentum, cross-entropy."""
    def __init__(self, rng):
        self.W1 = (rng.standard_normal((K * V, H)) * (1.0 / math.sqrt(K * V))).astype(np.float64)
        self.b1 = np.zeros(H)
        self.W2 = (rng.standard_normal((H, V)) * (1.0 / math.sqrt(H))).astype(np.float64)
        self.b2 = np.zeros(V)
        self.vW1 = np.zeros_like(self.W1); self.vb1 = np.zeros_like(self.b1)
        self.vW2 = np.zeros_like(self.W2); self.vb2 = np.zeros_like(self.b2)

    def _onehot(self, ctx):
        # ctx: (B,K) int -> (B, K*V) one-hot (dense but K*V=2048, B small => fine)
        B = ctx.shape[0]
        x = np.zeros((B, K * V))
        idx = ctx + (np.arange(K) * V)[None, :]
        x[np.arange(B)[:, None], idx] = 1.0
        return x

    def forward(self, ctx):
        x = self._onehot(ctx)
        z1 = x @ self.W1 + self.b1
        a1 = np.tanh(z1)
        logits = a1 @ self.W2 + self.b2
        return x, a1, logits

    @staticmethod
    def softmax(logits):
        m = logits.max(axis=-1, keepdims=True)
        e = np.exp(logits - m)
        return e / e.sum(axis=-1, keepdims=True)

    def step(self, ctx, tgt, lr):
        B = ctx.shape[0]
        x, a1, logits = self.forward(ctx)
        p = self.softmax(logits)
        loss = -np.log(p[np.arange(B), tgt] + 1e-12).mean()
        dlogits = p.copy()
        dlogits[np.arange(B), tgt] -= 1.0
        dlogits /= B
        gW2 = a1.T @ dlogits
        gb2 = dlogits.sum(0)
        da1 = dlogits @ self.W2.T
        dz1 = da1 * (1.0 - a1 * a1)
        gW1 = x.T @ dz1
        gb1 = dz1.sum(0)
        for g, v, w in ((gW1, self.vW1, self.W1), (gb1, self.vb1, self.b1),
                        (gW2, self.vW2, self.W2), (gb2, self.vb2, self.b2)):
            v *= MOM
            v -= lr * g
            w += v
        return loss

    def logits_for(self, ctx_row):
        _, _, logits = self.forward(ctx_row[None, :])
        return logits[0]


# ───────────────────────── window builders ─────────────────────────
def line_windows(line_bytes):
    """All (ctx[K], target) windows for one line (byte array). Pad with newline (10)."""
    pad = np.concatenate([np.full(K, 10, dtype=np.int64), line_bytes.astype(np.int64)])
    ctxs, tgts = [], []
    for i in range(len(line_bytes)):
        ctxs.append(pad[i:i + K])
        tgts.append(int(line_bytes[i]))
    if not ctxs:
        return None
    return np.stack(ctxs), np.array(tgts, dtype=np.int64)


def build_arm_pools(lines_bytes, diff_order, mode):
    """Return list of N_STAGES pools; each pool = (ctx_array, tgt_array) concatenated for its lines.
    mode: 'flat' -> single pool of all; 'curr' -> easy..hard quartiles; 'anti' -> hard..easy."""
    n = len(diff_order)
    stage_line_idx = [diff_order[s * n // N_STAGES:(s + 1) * n // N_STAGES] for s in range(N_STAGES)]
    if mode == "anti":
        stage_line_idx = stage_line_idx[::-1]

    def pool_for(line_ids):
        cs, ts = [], []
        for li in line_ids:
            w = line_windows(lines_bytes[li])
            if w is None:
                continue
            cs.append(w[0]); ts.append(w[1])
        if not cs:
            return None
        return np.concatenate(cs), np.concatenate(ts)

    if mode == "flat":
        allp = pool_for(list(range(len(lines_bytes))))
        return [allp]
    return [pool_for(s) for s in stage_line_idx]


# ───────────────────────── training ─────────────────────────
def train_arm(mode, lines_bytes, diff_order, seed):
    rng = np.random.default_rng(seed)
    m = ByteMLP(rng)
    pools = build_arm_pools(lines_bytes, diff_order, mode)
    if mode == "flat":
        pool = pools[0]
        cs, ts = pool
        N = len(ts)
        for st in range(STEPS):
            lr = LR * (0.5 * (1 + math.cos(math.pi * min(1.0, st / STEPS))))
            ix = rng.integers(0, N, BS)
            m.step(cs[ix], ts[ix], lr)
        return m
    # staged (curr / anti): 4 windows; window s draws from unlocked stages 0..s
    per = STEPS // N_STAGES
    for s in range(N_STAGES):
        unlocked = [p for p in pools[:s + 1] if p is not None]
        cs = np.concatenate([p[0] for p in unlocked])
        ts = np.concatenate([p[1] for p in unlocked])
        N = len(ts)
        for j in range(per):
            st = s * per + j
            lr = LR * (0.5 * (1 + math.cos(math.pi * min(1.0, st / STEPS))))
            ix = rng.integers(0, N, BS)
            m.step(cs[ix], ts[ix], lr)
    return m


# ───────────────────────── eval ─────────────────────────
def decode(m, ctx0, n_gen, temp, rng):
    ctx = ctx0.copy().astype(np.int64)
    out = []
    for _ in range(n_gen):
        logits = m.logits_for(ctx)
        if temp <= 0:
            nb = int(logits.argmax())
        else:
            p = ByteMLP.softmax((logits / temp)[None, :])[0]
            nb = int(rng.choice(V, p=p))
        out.append(nb)
        ctx = np.concatenate([ctx[1:], [nb]])
    return bytes(out)


def kwr(text, wordset):
    import re
    toks = re.findall(r"[a-zA-Z]+", text.lower())
    if not toks:
        return 0.0
    known = sum(1 for t in toks if t in wordset)
    return known / len(toks)


def token_set(text):
    import re
    return set(re.findall(r"[a-zA-Z]+", text.lower()))


def ngrams4(b):
    return set(bytes(b[i:i + 4]) for i in range(len(b) - 3))


def eval_arm(m, held_bytes, train_ngram4, wordset, seed):
    rng = np.random.default_rng(seed + 1000)
    # seed contexts from held-out
    starts = rng.integers(K, max(K + 1, len(held_bytes) - N_GEN - 1), N_SEED_CTX)
    conts = []
    kwrs = []
    for s0 in starts:
        ctx0 = held_bytes[s0 - K:s0].astype(np.int64)
        gen = decode(m, ctx0, N_GEN, DEC_TEMP, rng)
        txt = gen.decode("utf-8", errors="replace")
        conts.append((gen, txt))
        kwrs.append(kwr(txt, wordset))
    coherence = float(np.mean(kwrs))
    # composed_distinct: coherent AND corpus-absent 4-gram AND mutually distinct
    accepted = []
    for (gen, txt), kw in zip(conts, kwrs):
        if kw < KWR_BAR:
            continue
        gset = ngrams4(gen)
        if not gset:
            continue
        if not (gset - train_ngram4):  # has at least one corpus-absent 4-gram
            continue
        tset = token_set(txt)
        dup = False
        for prev in accepted:
            inter = len(tset & prev)
            union = len(tset | prev) or 1
            if inter / union > JACCARD:
                dup = True
                break
        if not dup:
            accepted.append(tset)
    composed_distinct = len(accepted)
    # qa_proxy: held-out next-byte top-1 accuracy
    nq = min(2000, len(held_bytes) - K - 1)
    qrng = np.random.default_rng(seed + 2000)
    pos = qrng.integers(K, len(held_bytes) - 1, nq)
    correct = 0
    # batch in chunks
    for i in range(0, nq, 256):
        chunk = pos[i:i + 256]
        ctxs = np.stack([held_bytes[p - K:p] for p in chunk]).astype(np.int64)
        _, _, logits = m.forward(ctxs)
        pred = logits.argmax(1)
        tgt = held_bytes[chunk].astype(np.int64)
        correct += int((pred == tgt).sum())
    qa_proxy = correct / nq
    return {"composed_distinct": composed_distinct, "coherence": coherence, "qa_proxy": qa_proxy}


# ───────────────────────── main ─────────────────────────
def main():
    t0 = time.time()
    raw, text = load_corpus()
    nlp = byte_neglogp(raw)
    wordset = build_word_set(text)
    lines = [l for l in text.split("\n")]
    # held-out = last HELDOUT_FRAC of bytes (never trained)
    cut = int(len(raw) * (1 - HELDOUT_FRAC))
    train_text = raw[:cut].decode("utf-8", errors="replace")
    held_bytes = np.frombuffer(raw[cut:], dtype=np.uint8).astype(np.int64)
    # train lines = lines fully inside the train region
    tlines = [l for l in train_text.split("\n") if l.strip()]
    lines_bytes = [np.frombuffer(l.encode("utf-8", errors="replace"), dtype=np.uint8) for l in tlines]
    lines_bytes = [lb for lb in lines_bytes if len(lb) > 0]
    diff, feats = line_difficulty([lb.tobytes().decode("utf-8", errors="replace") for lb in lines_bytes], nlp)
    diff_order = list(np.argsort(diff))  # ascending = easy..hard
    train_ngram4 = ngrams4(np.frombuffer(raw[:cut], dtype=np.uint8))

    print(f"[corpus] {len(raw)} bytes, {len(lines_bytes)} train lines, "
          f"{len(wordset)} words, held-out {len(held_bytes)} bytes", flush=True)
    print(f"[difficulty] len(med/max)={np.median(feats[0]):.0f}/{max(feats[0])} "
          f"rarity z-range, syntax-density mean={np.mean(feats[2]):.3f}", flush=True)
    nparams = K * V * H + H + H * V + V
    print(f"[model] byte-MLP K={K} H={H} V={V} params={nparams:,} STEPS={STEPS} BS={BS}", flush=True)

    arms = {"A_flat": "flat", "B_curriculum": "curr", "C_anticurriculum": "anti"}
    results = {a: {"composed_distinct": [], "coherence": [], "qa_proxy": []} for a in arms}
    for seed in SEEDS:
        for aname, mode in arms.items():
            m = train_arm(mode, lines_bytes, diff_order, seed)
            ev = eval_arm(m, held_bytes, train_ngram4, wordset, seed)
            for k2 in ("composed_distinct", "coherence", "qa_proxy"):
                results[aname][k2].append(ev[k2])
            print(f"  [seed {seed}] {aname:18s} CD={ev['composed_distinct']:2d} "
                  f"COH={ev['coherence']:.3f} QA={ev['qa_proxy']:.3f} "
                  f"({(time.time()-t0)/60:.1f}min)", flush=True)

    mean = {a: {k2: float(np.mean(v)) for k2, v in results[a].items()} for a in arms}

    A, B, C = mean["A_flat"], mean["B_curriculum"], mean["C_anticurriculum"]
    MARGIN_CD, MARGIN_CO = 1.0, 0.02
    dCD = B["composed_distinct"] - A["composed_distinct"]
    dCO = B["coherence"] - A["coherence"]
    b_beats_a = (dCD >= MARGIN_CD) or (dCO >= MARGIN_CO)
    c_not_better = (C["composed_distinct"] <= A["composed_distinct"]) and (C["coherence"] <= A["coherence"])
    green = b_beats_a and c_not_better
    verdict = "GREEN" if green else "CLOSED-NEGATIVE"
    tier = "🟢 developmental ORDER is a lever (toy-only)" if green else \
           "🔴 learning-ORDER is NOT the depth lever at toy scale (a_paper_negative_ok)"

    print("\n" + "=" * 78, flush=True)
    print("### H_1229 DEVELOPMENTAL LEARNING-ORDER (HD20) — RESULT (mean over seeds) ###", flush=True)
    print("=" * 78, flush=True)
    print(f"{'arm':<20}{'composed_distinct':>18}{'coherence':>12}{'qa_proxy':>10}", flush=True)
    for a in arms:
        print(f"{a:<20}{mean[a]['composed_distinct']:>18.3f}{mean[a]['coherence']:>12.4f}"
              f"{mean[a]['qa_proxy']:>10.4f}", flush=True)
    print(f"\ndCD = B-A composed_distinct = {dCD:+.3f}  (margin {MARGIN_CD})", flush=True)
    print(f"dCO = B-A coherence         = {dCO:+.3f}  (margin {MARGIN_CO})", flush=True)
    print(f"B beats A (margin): {b_beats_a} | C not better than A: {c_not_better}", flush=True)
    print(f"VERDICT: {verdict}  {tier}", flush=True)

    out = {
        "hypothesis": "H_1229_developmental_order", "lens": "HD20",
        "model": {"type": "numpy-byte-MLP", "K": K, "H": H, "V": V, "params": nparams,
                  "STEPS": STEPS, "BS": BS, "seeds": list(SEEDS)},
        "difficulty_metric": "z(len)+z(rarity=-logp byte mean)+z(syntax punct-density)",
        "staging": f"{N_STAGES} quartile stages, window s samples unlocked 0..s; equal steps/tokens",
        "means": mean, "per_seed": results,
        "dCD": dCD, "dCO": dCO, "margins": {"CD": MARGIN_CD, "CO": MARGIN_CO},
        "b_beats_a": b_beats_a, "c_not_better_than_a": c_not_better,
        "verdict": verdict, "tier": tier,
        "frozen_rule": "GREEN iff (dCD>=1.0 OR dCO>=0.02) AND (C.CD<=A.CD AND C.COH<=A.COH)",
    }
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(out, open(os.path.join(OUTDIR, "h1229_result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n[out] {os.path.join(OUTDIR, 'h1229_result.json')}  ({(time.time()-t0)/60:.1f}min)", flush=True)
    return out


if __name__ == "__main__":
    main()
