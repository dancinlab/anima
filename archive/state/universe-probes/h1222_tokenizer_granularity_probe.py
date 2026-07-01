#!/usr/bin/env python3
"""h1222_tokenizer_granularity_probe.py — HD6 from the depth-ceiling ladder.

QUESTION (HD6, .verdicts/1219_depth_ceiling_hypothesis_exhaustion/H_1219.txt):
  Is the flat literal-QA + ideation-depth wall caused by BYTE-LEVEL granularity
  (bytes can't cheaply form word/concept units for recall) vs a token (BPE/word)
  vocabulary? If a token vocab cheaply forms the word/concept units that bytes
  must build from scratch over many steps, a token model at EQUAL budget should
  recall planted facts and recombine concepts BETTER than a byte model.

DESIGN (toy, $0 summer/CPU, p7, NO LLM-judge):
  Two tiny LMs at EQUAL param budget + EQUAL training-token count on the SAME
  corpus, differing ONLY in tokenizer:
    (A) BYTE     vocab = 256
    (B) TOKEN    a small word/BPE vocab trained on the corpus (~2-4k types)
  Both are the SAME GPT-ish architecture (single-head causal self-attn + MLP,
  tied embedding head). We hold PARAM BUDGET equal by shrinking the token
  model's d_model so total trainable params match the byte model within a tight
  tolerance (the token model has a far bigger embedding table, so it gets a
  smaller hidden width — this is the honest equal-budget tradeoff the question
  is really about: does the vocab buy you concept units that are WORTH the
  parameters they cost).

CORPUS: a SYNTHETIC, fully-controlled English-word corpus (a_toy_scale_recheck —
  toy-only). We use real dictionary words (/usr/share/dict/words) so coherence
  (G0 known-word-ratio) is meaningful, but we GENERATE the text so we know the
  EXACT ground-truth for two metrics that are impossible to score cleanly on
  scraped wiki:
    • literal-QA-proxy: we plant N facts "<subject> lives in <city> ." and ask
      "<subject> lives in" — exact-match the generated continuation against the
      planted city. We KNOW every answer, so QA is exact, deterministic, p7.
    • composed-distinct (H_1158/H_1140 style): held-out PROMPTS fuse two corpus
      concepts; we count CORPUS-ABSENT real-word bigrams in coherent outputs.
      We KNOW the corpus verbatim, so corpus-absence is exact (a set lookup),
      not a grep heuristic.
  This trades wiki realism for measurement validity — the right trade for a
  toy that must isolate ONE variable (tokenizer granularity).

CONFOUND CONTROL (stated honestly per the task):
  A token model sees more CHARACTERS per step (one token ~ several bytes), so at
  equal STEP count it would see more context and more text. We control on BOTH
  axes and report both:
    (1) EQUAL TRAINING TOKENS-OF-THAT-MODEL is the WRONG control (token model
        would see ~5x the corpus). We instead hold EQUAL TRAINING **CHARACTERS**
        consumed: each model trains on the SAME number of corpus CHARACTERS
        (byte model: that many byte-steps; token model: however many token-steps
        that many characters tokenizes to). So both models SEE THE SAME TEXT the
        same number of times (same epochs over the same corpus chars).
    (2) EQUAL CONTEXT WINDOW IN CHARACTERS: byte block_chars == token block ×
        avg_chars_per_token (we set the token block so its character span matches
        the byte block). So neither model gets a longer effective receptive
        field in characters.
  We ALSO match PARAM BUDGET (above). So the only thing that differs is the
  granularity of the unit. We REPORT the residual confound: param-match forces
  the token model narrower; that is intrinsic to the question (the cost of a
  vocab), not a flaw — we state it.

FROZEN FALSIFIER (pre-registered, NO goalpost move):
  Let QA_A, QA_B = literal-QA-proxy exact-match accuracy (byte, token).
  Let CD_A, CD_B = mean composed-distinct corpus-absent coherent bigrams.
  MARGIN bars (stated up front):
    QA margin  = +0.10 absolute accuracy.
    CD margin  = +1.0 distinct corpus-absent bigram (mean).
  🟢 GRANULARITY-IS-A-LEVER iff
        (QA_B >= QA_A + 0.10)  OR  (CD_B >= CD_A + 1.0)
     i.e. the token vocab gives a CLEAR lift on literal-QA AND/OR composition,
     at equal budget + equal chars + equal context — granularity is a real lever
     that the byte ceiling pays for.
  🔴 GRANULARITY-IS-NOT-THE-WALL otherwise (token model does not clearly beat
     byte on either metric at matched budget/chars/context) — switching to a
     token vocab would NOT lift the depth ceiling; the wall is elsewhere
     (a_paper_negative_ok — a closed-negative that rules out HD6).
  G0 GUARD: both models must reach known-word-ratio >= 0.50 on free gen for the
     comparison to be valid (else we're comparing garble). Reported, not a bar
     mover.

SCOPE (a_toy_scale_recheck, a_scale_honest_scope): TOY ONLY — tiny params,
  synthetic corpus, char-matched compute. A toy verdict states scale-transfer
  UNVERIFIED. This rules HD6 in/out as a $0 DIRECTION, not a production decree.

$0 summer CPU, numpy-only (no torch dep, no network, no HF). Deterministic seeds.
"""
from __future__ import annotations
import os, sys, json, time, math, hashlib, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SEEDS = [7, 8, 9]
DICT_PATH = "/usr/share/dict/words"

# ── frozen bars (pre-registered) ────────────────────────────────────────────
QA_MARGIN = 0.10          # token must beat byte by >= this absolute QA accuracy
CD_MARGIN = 1.0           # ... or by >= this many composed-distinct corpus-absent bigrams
G0_BAR    = 0.50          # known-word-ratio coherence guard

# ── corpus generation knobs (toy scale) ─────────────────────────────────────
N_FACTS        = 60       # planted "<subj> lives in <city> ." facts (QA ground truth)
FACT_REPEATS   = 8        # each fact repeated this many times (recall needs exposure)
N_FILLER_SENTS = 1400     # generic SVO filler sentences for language modelling
TRAIN_CHARS    = None     # set after corpus build = full corpus length (1 epoch unit)
EPOCHS         = 6        # how many char-passes both models train (equal for both)


# ════════════════════════════════════════════════════════════════════════════
# 1. CORPUS — synthetic, real-word, fully known ground truth
# ════════════════════════════════════════════════════════════════════════════
def load_words():
    with open(DICT_PATH) as f:
        ws = [w.strip().lower() for w in f if w.strip().isalpha()]
    return ws


def build_corpus(seed=0):
    rng = np.random.default_rng(seed)
    allw = load_words()
    # small closed vocabularies for a learnable toy grammar
    pick = lambda pool, n: list(rng.choice(pool, size=n, replace=False))
    short = [w for w in allw if 3 <= len(w) <= 7]
    nouns  = pick(short, 80)
    verbs  = pick(short, 40)
    adjs   = pick(short, 60)
    subjects = [w.capitalize() for w in pick([w for w in allw if 4 <= len(w) <= 8], N_FACTS)]
    cities   = [w.capitalize() for w in pick([w for w in allw if 4 <= len(w) <= 8], N_FACTS)]

    sents = []
    # planted facts (QA ground truth): subject_i lives in city_i .
    facts = {}
    for i in range(N_FACTS):
        s, c = subjects[i], cities[i]
        facts[s] = c
        for _ in range(FACT_REPEATS):
            sents.append(f"{s} lives in {c} .")
    # generic SVO filler: "the ADJ NOUN VERB the ADJ NOUN ." — real-word language
    for _ in range(N_FILLER_SENTS):
        a1, n1, v, a2, n2 = (rng.choice(adjs), rng.choice(nouns), rng.choice(verbs),
                             rng.choice(adjs), rng.choice(nouns))
        sents.append(f"the {a1} {n1} {v} the {a2} {n2} .")
    rng.shuffle(sents)
    text = " ".join(sents) + " "
    return text, facts, dict(nouns=nouns, verbs=verbs, adjs=adjs,
                             subjects=subjects, cities=cities)


# ════════════════════════════════════════════════════════════════════════════
# 2. TOKENIZERS — (A) byte vocab 256, (B) word/BPE vocab
# ════════════════════════════════════════════════════════════════════════════
class ByteTok:
    name = "BYTE"
    def __init__(self, text):
        self.V = 256
    def encode(self, s):
        return list(s.encode("utf-8", "replace"))
    def decode(self, ids):
        return bytes(b & 0xFF for b in ids).decode("utf-8", "replace")
    @property
    def avg_chars_per_unit(self):
        return 1.0


class WordTok:
    """Whitespace/punct word tokenizer with a frequency-capped vocab + a small
    set of byte-fallback merges so it can encode any string (BPE-lite). For a
    synthetic closed-vocab corpus this is effectively a WORD vocab — exactly the
    'concept unit' the granularity hypothesis is about."""
    name = "TOKEN"
    def __init__(self, text, max_vocab=4000):
        toks = self._split(text)
        from collections import Counter
        freq = Counter(toks)
        # specials: 0=pad/unk, plus single chars as fallback
        chars = sorted(set(text))
        vocab = ["<unk>"] + chars
        for w, _ in freq.most_common():
            if w not in vocab:
                vocab.append(w)
            if len(vocab) >= max_vocab:
                break
        self.itos = vocab
        self.stoi = {t: i for i, t in enumerate(vocab)}
        self.V = len(vocab)
        # avg chars per token over the corpus (for context/char matching)
        enc = self.encode(text)
        self._avg = len(text) / max(1, len(enc))
    @staticmethod
    def _split(s):
        # words and standalone punctuation as separate tokens
        return re.findall(r"[A-Za-z]+|[^A-Za-z\s]|\s", s)
    def encode(self, s):
        out = []
        for t in self._split(s):
            if t in self.stoi:
                out.append(self.stoi[t])
            else:
                for ch in t:                       # byte/char fallback for OOV
                    out.append(self.stoi.get(ch, 0))
        return out
    def decode(self, ids):
        return "".join(self.itos[i] if 0 <= i < self.V else "" for i in ids)
    @property
    def avg_chars_per_unit(self):
        return self._avg


# ════════════════════════════════════════════════════════════════════════════
# 3. MODEL — tiny single-block causal self-attention LM (numpy, trainable)
#    kept minimal & identical across both tokenizers; only V and d differ.
# ════════════════════════════════════════════════════════════════════════════
class TinyLM:
    def __init__(self, V, d, block, seed):
        rng = np.random.default_rng(seed)
        sc = 1.0 / math.sqrt(d)
        self.V, self.d, self.block = V, d, block
        self.E  = rng.standard_normal((V, d)) * 0.02      # tied tok+head embedding
        self.P  = rng.standard_normal((block, d)) * 0.02  # positional
        self.Wq = rng.standard_normal((d, d)) * sc
        self.Wk = rng.standard_normal((d, d)) * sc
        self.Wv = rng.standard_normal((d, d)) * sc
        self.Wo = rng.standard_normal((d, d)) * sc
        self.W1 = rng.standard_normal((d, 4*d)) * sc
        self.W2 = rng.standard_normal((4*d, d)) * sc
        self.params = ["E","P","Wq","Wk","Wv","Wo","W1","W2"]
        self.m = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        self.v = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        self.t = 0

    def n_params(self):
        return sum(getattr(self, k).size for k in self.params)

    def _attn(self, X):
        T, d = X.shape
        q, k, v = X @ self.Wq, X @ self.Wk, X @ self.Wv
        att = (q @ k.T) / math.sqrt(d)
        mask = np.triu(np.ones((T, T)), 1).astype(bool)
        att = np.where(mask, -1e9, att)
        att = att - att.max(1, keepdims=True)
        att = np.exp(att); att /= att.sum(1, keepdims=True)
        ctx = att @ v
        return (ctx @ self.Wo), (q, k, v, att, ctx)

    def forward(self, ids):
        T = len(ids)
        X = self.E[ids] + self.P[:T]
        a, acache = self._attn(X)
        h1 = X + a
        z = h1 @ self.W1
        zr = np.maximum(z, 0)
        h2 = h1 + zr @ self.W2
        logits = h2 @ self.E.T
        cache = (ids, X, acache, h1, z, zr, h2)
        return logits, cache

    def loss_and_grad(self, ids):
        x = ids[:-1]; y = ids[1:]
        logits, cache = self.forward(x)
        T = len(x)
        logits = logits - logits.max(1, keepdims=True)
        probs = np.exp(logits); probs /= probs.sum(1, keepdims=True)
        loss = -np.log(probs[np.arange(T), y] + 1e-12).mean()
        dlog = probs; dlog[np.arange(T), y] -= 1.0; dlog /= T
        (ids_, X, acache, h1, z, zr, h2) = cache
        q, k, v, att, ctx = acache
        g = {kk: np.zeros_like(getattr(self, kk)) for kk in self.params}
        # head (tied with E)
        g["E"] += dlog.T @ h2
        dh2 = dlog @ self.E
        # mlp
        g["W2"] += zr.T @ dh2
        dzr = dh2 @ self.W2.T
        dz = dzr * (z > 0)
        g["W1"] += h1.T @ dz
        dh1 = dh2 + dz @ self.W1.T
        # attn residual
        da = dh1.copy(); dX = dh1.copy()
        dctx = da @ self.Wo.T
        g["Wo"] += ctx.T @ da
        datt = dctx @ v.T
        dv = att.T @ dctx
        # softmax backward
        ds = att * (datt - (att * datt).sum(1, keepdims=True))
        dq = (ds @ k) / math.sqrt(self.d)
        dk = (ds.T @ q) / math.sqrt(self.d)
        g["Wq"] += X.T @ dq
        g["Wk"] += X.T @ dk
        g["Wv"] += X.T @ dv
        dX += dq @ self.Wq.T + dk @ self.Wk.T + dv @ self.Wv.T
        # embeddings
        np.add.at(g["E"], ids_, dX)
        g["P"][:T] += dX
        return loss, g

    def step(self, g, lr=3e-3, b1=0.9, b2=0.999, eps=1e-8, clip=1.0):
        self.t += 1
        for kk in self.params:
            gk = g[kk]
            gn = np.linalg.norm(gk)
            if gn > clip:
                gk = gk * (clip / (gn + 1e-12))
            self.m[kk] = b1*self.m[kk] + (1-b1)*gk
            self.v[kk] = b2*self.v[kk] + (1-b2)*(gk*gk)
            mh = self.m[kk] / (1 - b1**self.t)
            vh = self.v[kk] / (1 - b2**self.t)
            getattr(self, kk)[...] -= lr * mh / (np.sqrt(vh) + eps)

    @np.errstate(all="ignore")
    def generate(self, prompt_ids, n, greedy=True, temp=1.0, top_k=20, seed=0):
        rng = np.random.default_rng(seed)
        ids = list(prompt_ids)
        out = []
        for _ in range(n):
            ctx = ids[-self.block:]
            logits, _ = self.forward(ctx)
            lo = logits[-1]
            if greedy:
                nxt = int(lo.argmax())
            else:
                lo = lo / temp
                if top_k and top_k < len(lo):
                    thresh = np.sort(lo)[-top_k]
                    lo = np.where(lo < thresh, -1e9, lo)
                lo = lo - lo.max()
                p = np.exp(lo); p /= p.sum()
                nxt = int(rng.choice(len(p), p=p))
            ids.append(nxt); out.append(nxt)
        return out


# ════════════════════════════════════════════════════════════════════════════
# 4. EQUAL-BUDGET solver — pick token d_model so params match byte within tol
# ════════════════════════════════════════════════════════════════════════════
def params_for(V, d, block):
    # E:V*d  P:block*d  Wq/Wk/Wv/Wo:4*d*d  W1:d*4d  W2:4d*d
    return V*d + block*d + 4*d*d + 8*d*d


def solve_d(V, target_params, block):
    best = None
    for d in range(8, 256, 2):
        p = params_for(V, d, block)
        if best is None or abs(p - target_params) < abs(best[1] - target_params):
            best = (d, p)
    return best


# ════════════════════════════════════════════════════════════════════════════
# 5. TRAIN one model on char-matched compute
# ════════════════════════════════════════════════════════════════════════════
def make_windows(token_ids, block):
    wins = []
    i = 0
    while i + block + 1 <= len(token_ids):
        wins.append(token_ids[i:i+block+1])
        i += block
    return wins


def train(model, token_ids, block, epochs, seed, label):
    rng = np.random.default_rng(seed)
    wins = make_windows(token_ids, block)
    if not wins:
        return [9.9]
    losses = []
    for ep in range(epochs):
        order = rng.permutation(len(wins))
        ep_loss = 0.0
        for j in order:
            w = wins[j]
            loss, g = model.loss_and_grad(w)
            model.step(g)
            ep_loss += loss
        ep_loss /= len(order)
        losses.append(ep_loss)
        print(f"    [{label}] epoch {ep+1}/{epochs} steps={len(wins)} loss={ep_loss:.3f}", flush=True)
    return losses


# ════════════════════════════════════════════════════════════════════════════
# 6. METRICS — literal-QA-proxy, composed-distinct, G0 coherence
# ════════════════════════════════════════════════════════════════════════════
def known_word_ratio(s, dictset):
    words = re.findall(r"[A-Za-z]+", s.lower())
    if not words:
        return 0.0
    return sum(1 for w in words if w in dictset) / len(words)


def eval_qa(model, tok, facts, dictset):
    """Exact-match: prompt '<subj> lives in', does greedy continuation produce
    the planted city as the next word?"""
    hits = 0
    coh = []
    for subj, city in facts.items():
        prompt = f"{subj} lives in "
        pids = tok.encode(prompt)
        gen = model.generate(pids, n=max(12, len(tok.encode(city)) + 4),
                             greedy=True, seed=0)
        txt = tok.decode(gen)
        coh.append(known_word_ratio(prompt + txt, dictset))
        # next real word in the continuation
        m = re.search(r"[A-Za-z]+", txt)
        pred = m.group(0).lower() if m else ""
        if pred == city.lower():
            hits += 1
    return hits / max(1, len(facts)), float(np.mean(coh))


def corpus_bigrams(text):
    words = re.findall(r"[A-Za-z]+", text.lower())
    return set(zip(words, words[1:]))


def eval_composed(model, tok, prompts, corpus_bg, dictset, seeds=(7, 8, 9)):
    """H_1158/H_1140 style: count DISTINCT corpus-absent real-word bigrams in
    COHERENT (kwr>=0.5) sampled generations. Mean over seeds."""
    per_seed = []
    sample_out = []
    for sd in seeds:
        absent = set()
        for p in prompts:
            pids = tok.encode(p)
            gen = model.generate(pids, n=40, greedy=False, temp=0.85,
                                 top_k=20, seed=sd)
            txt = tok.decode(gen)
            full = p + txt
            if known_word_ratio(full, dictset) < 0.50:
                continue
            words = re.findall(r"[A-Za-z]+", txt.lower())
            words = [w for w in words if len(w) >= 3 and w in dictset]
            for bg in zip(words, words[1:]):
                if bg not in corpus_bg:
                    absent.add(bg)
            if len(sample_out) < 4:
                sample_out.append(full[:120])
        per_seed.append(len(absent))
    return float(np.mean(per_seed)), per_seed, sample_out


# ════════════════════════════════════════════════════════════════════════════
# 7. MAIN
# ════════════════════════════════════════════════════════════════════════════
def run_one(seed):
    print(f"\n=== SEED {seed} ===", flush=True)
    text, facts, vocabs = build_corpus(seed=seed)
    dictset = set(load_words())
    corpus_bg = corpus_bigrams(text)
    n_chars = len(text)

    # composed-distinct prompts: fuse two corpus concepts (held-out combos)
    rng = np.random.default_rng(1000 + seed)
    cp = []
    for _ in range(8):
        a = rng.choice(vocabs["adjs"]); n = rng.choice(vocabs["nouns"])
        cp.append(f"the {a} {n} ")
    for _ in range(4):
        s = rng.choice(vocabs["subjects"])
        cp.append(f"{s} lives in ")

    block_chars = 96     # both models get this many CHARACTERS of context

    # (A) BYTE
    byte_tok = ByteTok(text)
    byte_ids = byte_tok.encode(text)
    byte_block = block_chars                       # 1 byte ~ 1 char
    d_byte = 48
    byte_model = TinyLM(byte_tok.V, d_byte, byte_block, seed)
    target = byte_model.n_params()

    # (B) TOKEN — equal param budget, equal char context
    word_tok = WordTok(text)
    word_ids = word_tok.encode(text)
    acpt = word_tok.avg_chars_per_unit
    word_block = max(8, int(round(block_chars / acpt)))   # same char span
    d_word, p_word = solve_d(word_tok.V, target, word_block)
    word_model = TinyLM(word_tok.V, d_word, word_block, seed)

    print(f"  corpus chars={n_chars}  facts={len(facts)}  corpus_bigrams={len(corpus_bg)}", flush=True)
    print(f"  BYTE : V={byte_tok.V} d={d_byte} block={byte_block} params={byte_model.n_params()} "
          f"tokens={len(byte_ids)}", flush=True)
    print(f"  TOKEN: V={word_tok.V} d={d_word} block={word_block} params={word_model.n_params()} "
          f"tokens={len(word_ids)} avg_chars/tok={acpt:.2f}", flush=True)
    print(f"  budget match: byte={target} token={word_model.n_params()} "
          f"ratio={word_model.n_params()/target:.3f}", flush=True)

    # CONTROL: equal char-passes. Byte trains EPOCHS over byte_ids; token trains
    # EPOCHS over word_ids — same corpus, same number of passes = same text seen
    # the same number of times. (token has fewer steps because fewer units; that
    # is the granularity advantage being tested, NOT extra data.)
    print("  -- training BYTE --", flush=True)
    bl = train(byte_model, byte_ids, byte_block, EPOCHS, seed, "BYTE")
    print("  -- training TOKEN --", flush=True)
    wl = train(word_model, word_ids, word_block, EPOCHS, seed, "TOKEN")

    qa_b, qcoh_b = eval_qa(byte_model, byte_tok, facts, dictset)
    qa_w, qcoh_w = eval_qa(word_model, word_tok, facts, dictset)
    cd_b, cdseed_b, samp_b = eval_composed(byte_model, byte_tok, cp, corpus_bg, dictset)
    cd_w, cdseed_w, samp_w = eval_composed(word_model, word_tok, cp, corpus_bg, dictset)

    print(f"  RESULT byte : QA={qa_b:.3f} coh={qcoh_b:.2f} CD={cd_b:.2f}{cdseed_b} finalloss={bl[-1]:.3f}", flush=True)
    print(f"  RESULT token: QA={qa_w:.3f} coh={qcoh_w:.2f} CD={cd_w:.2f}{cdseed_w} finalloss={wl[-1]:.3f}", flush=True)

    return dict(seed=seed, n_chars=n_chars,
                byte=dict(V=byte_tok.V, d=d_byte, block=byte_block, params=byte_model.n_params(),
                          tokens=len(byte_ids), QA=qa_b, coh=qcoh_b, CD=cd_b, CDseed=cdseed_b,
                          loss=bl[-1], samp=samp_b),
                token=dict(V=word_tok.V, d=d_word, block=word_block, params=word_model.n_params(),
                           tokens=len(word_ids), avg_cpt=acpt, QA=qa_w, coh=qcoh_w, CD=cd_w,
                           CDseed=cdseed_w, loss=wl[-1], samp=samp_w))


def main():
    np.seterr(all="ignore")
    t0 = time.time()
    runs = [run_one(s) for s in SEEDS]

    QA_A = float(np.mean([r["byte"]["QA"] for r in runs]))
    QA_B = float(np.mean([r["token"]["QA"] for r in runs]))
    CD_A = float(np.mean([r["byte"]["CD"] for r in runs]))
    CD_B = float(np.mean([r["token"]["CD"] for r in runs]))
    coh_A = float(np.mean([r["byte"]["coh"] for r in runs]))
    coh_B = float(np.mean([r["token"]["coh"] for r in runs]))

    qa_lift = QA_B - QA_A
    cd_lift = CD_B - CD_A
    qa_green = qa_lift >= QA_MARGIN
    cd_green = cd_lift >= CD_MARGIN
    g0_ok = (coh_A >= G0_BAR) and (coh_B >= G0_BAR)
    green = (qa_green or cd_green)
    verdict = "GREEN" if green else "RED"

    print("\n" + "=" * 70)
    print("H_1222 — TOKENIZER GRANULARITY (HD6) — SUMMARY")
    print("=" * 70)
    print(f"  A BYTE : QA={QA_A:.3f}  CD={CD_A:.2f}  coh={coh_A:.2f}")
    print(f"  B TOKEN: QA={QA_B:.3f}  CD={CD_B:.2f}  coh={coh_B:.2f}")
    print(f"  QA lift (B-A) = {qa_lift:+.3f}  bar +{QA_MARGIN}  -> {'PASS' if qa_green else 'fail'}")
    print(f"  CD lift (B-A) = {cd_lift:+.2f}   bar +{CD_MARGIN}   -> {'PASS' if cd_green else 'fail'}")
    print(f"  G0 guard: byte coh {coh_A:.2f}, token coh {coh_B:.2f} (bar {G0_BAR}) -> {'OK' if g0_ok else 'GARBLE'}")
    print(f"  VERDICT: {verdict}")
    print(f"  elapsed {time.time()-t0:.1f}s")

    summary = dict(verdict=verdict, QA_A=QA_A, QA_B=QA_B, CD_A=CD_A, CD_B=CD_B,
                   coh_A=coh_A, coh_B=coh_B, qa_lift=qa_lift, cd_lift=cd_lift,
                   qa_green=qa_green, cd_green=cd_green, g0_ok=g0_ok,
                   QA_MARGIN=QA_MARGIN, CD_MARGIN=CD_MARGIN, seeds=SEEDS, runs=runs)
    outdir = os.path.join(REPO, ".verdicts", "1222_tokenizer_granularity")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "H_1222_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=float)
    print(f"  wrote {outdir}/H_1222_summary.json")
    return summary


if __name__ == "__main__":
    main()
