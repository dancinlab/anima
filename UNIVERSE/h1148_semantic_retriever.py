#!/usr/bin/env python3
"""
H_1148 — SEMANTIC RETRIEVER vs PRIOR-WINDOW (axis-5 of the 303M 완성 campaign).

Question (frozen FREEZE 2026-06-13):
  axis-4 (branch retro303m-en-prep) trains the H_1147-validated RETRO copy head with a v1
  anchor = the PRIOR WINDOW of the same corpus (a POSITIONAL surrogate — prior_window_batch:
  the anchor for a target span is the preceding [i-La-gap : i-gap] window, picked by POSITION
  not CONTENT). Honest limitation: a window may carry little entity overlap with the query, so
  the trained copy head has nothing to copy and falls back to fabrication.

  Does a SEMANTIC retriever — pick, from a pool of candidate prior chunks, the one most
  CONTENT-SIMILAR to the query (cheap byte n-gram cosine, $0, index-free) — ground copying
  BETTER than the positional prior-window surrogate, and how close does it get to an ORACLE
  retriever that always hands over the true anchor?

This REUSES the H_1147 must-copy mechanism (UNIVERSE/h1147_retro_mechanism_gate.py) VERBATIM:
  - the RETRO copy/pointer head (cross-attend anchor positions, gate-mix copy vs vocab) is the
    SAME trained mechanism H_1147 greenlit. We hold the HEAD fixed and vary ONLY the RETRIEVAL
    POLICY that selects which chunk becomes the anchor. The head is trained ONCE on
    semantically-retrieved anchors (the deployment policy) and evaluated under 3 test policies.
  - un-memorizable: the VALUE is random per example, drawn from a HELD-OUT pool never seen as a
    training target => the answer MUST be copied from whichever chunk the retriever returns.

THREE RETRIEVAL POLICIES (the single manipulated variable; SAME head, data, seed):
  (1) PRIOR-WINDOW (v1, positional): the anchor = a FIXED-position chunk (here: chunk index 0,
        the "preceding window"). The true-anchor entity is hidden among DISTRACTOR chunks at
        OTHER positions => prior-window grabs the true chunk only by luck (1/n_chunks hit-rate).
  (2) SEMANTIC (the test arm): retrieve the chunk whose byte-trigram profile is most cosine-
        similar to the QUERY's key context. The cheap retriever should pick the chunk that
        actually shares the key => high hit-rate => the copy head has the right entity to copy.
  (3) ORACLE (upper bound): always return the true anchor chunk. Ceiling for "perfect retrieval".

Each example:
  - QUERY: <KEY> REL  (asks for KEY's value)
  - a POOL of N_CHUNKS candidate chunks; exactly ONE (the TRUE chunk) is [BOS KEY REL VALUE SEP]
    (contains KEY + its VALUE); the others are DISTRACTORS [BOS KEY' REL VALUE' SEP] with
    DIFFERENT keys/values. The TRUE chunk sits at a RANDOM pool position (so position carries
    no signal — prior-window's fixed-position pick must rely on luck).
  - a RETRIEVAL POLICY selects ONE chunk from the pool => that chunk is fed to the SAME RETRO
    copy head as the anchor. Predict VALUE at the final query position.

METRICS (p7 deterministic; NOT perplexity, NOT LLM-judge):
  copy-accuracy  = fraction where greedy argmax == the QUERY-KEY's true VALUE.
  fab-rate       = 1 - copy-accuracy (emitting any other token = fabricated entity).
  hit-rate       = fraction where the policy's selected chunk IS the true chunk (retrieval
                   quality, independent of the head). Reported for all 3 policies.

FROZEN FALSIFIER + bars (immovable — see FREEZE block):
  F1 SEMANTIC-LIFTS:   copy-acc(SEMANTIC) - copy-acc(PRIOR-WINDOW) >= 0.20
                       (semantic retrieval substantially out-grounds the positional surrogate)
  F2 APPROACHES-ORACLE: copy-acc(ORACLE) - copy-acc(SEMANTIC) <= 0.15
                       (the cheap retriever actually finds the true anchor — small gap to ceiling)
  VERDICT:
    F1 AND F2  => 🟢 GREEN  : swap v1 prior-window -> semantic in RETRO-303M v2.
    F1 only    => 🟡 PARTIAL: semantic helps but the cheap retriever leaves a ceiling gap
                              (warrants a stronger/learned retriever before the swap).
    NOT F1     => 🔴 NEUTRAL/CLOSED-NEG: semantic ~ prior-window => v1 positional is good
                              enough, a retriever is not worth it yet (honest, a_paper_negative_ok).

$0. Local CPU. Pure numpy, deterministic seeded. No torch, no pod, no GPU.
"""
import json
import sys
import numpy as np

SEED = 1148

# ----------------------------------------------------------------------------- vocab
PAD, BOS, REL, SEP = 0, 1, 2, 3
N_KEYS = 32
N_VALS = 32
KEY0 = 4
VAL0 = KEY0 + N_KEYS
NV_PAD = VAL0 + N_VALS          # non-value pad (blank a value slot)
VOCAB = NV_PAD + 1

KEYS = list(range(KEY0, KEY0 + N_KEYS))
VALS = list(range(VAL0, VAL0 + N_VALS))

# held-out value subset: never a training target => test answers cannot be recalled.
HELDOUT_VALS = set(VALS[N_VALS // 2:])
TRAIN_VALS = [v for v in VALS if v not in HELDOUT_VALS]

# ----------------------------------------------------------------------------- layout
# Each candidate chunk is a fact triple: [BOS KEY REL VALUE SEP]  (length 5).
# The QUERY (2 tokens) [KEY REL] is appended after the SELECTED anchor chunk.
# Full fed sequence (length 7): [BOS KEY' REL VALUE' SEP | KEY REL]  -- identical layout to
# H_1147 so the SAME copy head applies; only WHICH chunk fills the anchor slot changes.
CHUNK_LEN = 5
SEQ_LEN = 7
VALUE_POS_IN_ANCHOR = 3
ANCHOR_POSITIONS = [0, 1, 2, 3, 4]
N_CHUNKS = 6                    # pool size: 1 true chunk + 5 distractors


def make_chunk(k, v):
    return np.array([BOS, k, REL, v, SEP], dtype=np.int64)


# ----------------------------------------------------------------------------- retriever
# Cheap, index-free, $0 byte/n-gram similarity. We profile each chunk + the query by the
# multiset of its TOKEN BIGRAMS (the toy analogue of a byte-trigram TF profile over a real
# corpus chunk), then retrieve by cosine. The toy's discriminative signal is the KEY token: a
# chunk sharing the query's KEY scores higher. This mirrors the real plan (byte n-gram TF
# cosine over corpus chunks) at toy scale.
def token_profile(tokens):
    """Sparse bigram count vector over the token id space (VOCAB^2 conceptually, dict here)."""
    p = {}
    for i in range(len(tokens) - 1):
        b = (int(tokens[i]), int(tokens[i + 1]))
        p[b] = p.get(b, 0.0) + 1.0
    # also include unigrams (helps the KEY token register even from a 2-token query)
    for t in tokens:
        u = (-1, int(t))
        p[u] = p.get(u, 0.0) + 1.0
    return p


def cosine(pa, pb):
    if not pa or not pb:
        return 0.0
    dot = sum(v * pb.get(k, 0.0) for k, v in pa.items())
    na = np.sqrt(sum(v * v for v in pa.values()))
    nb = np.sqrt(sum(v * v for v in pb.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def semantic_select(query_tokens, chunks, rng):
    """Return the pool index of the chunk most cosine-similar to the query bigram profile.
    Ties broken by a deterministic rng draw (so a no-signal tie != always position 0)."""
    qp = token_profile(query_tokens)
    sims = np.array([cosine(qp, token_profile(c)) for c in chunks])
    mx = sims.max()
    winners = np.flatnonzero(sims >= mx - 1e-12)
    return int(winners[rng.integers(0, len(winners))])


# ----------------------------------------------------------------------------- data
def make_pool(rng, key, value, value_pool, distractor_keys):
    """Build a pool of N_CHUNKS chunks. The TRUE chunk = [BOS key REL value SEP] placed at a
    RANDOM position. The other N_CHUNKS-1 are distractors with DIFFERENT keys + random values.
    Returns (chunks list, true_index)."""
    true_idx = int(rng.integers(0, N_CHUNKS))
    chunks = []
    dks = list(distractor_keys)
    rng.shuffle(dks)
    di = 0
    for p in range(N_CHUNKS):
        if p == true_idx:
            chunks.append(make_chunk(key, value))
        else:
            dk = dks[di % len(dks)]; di += 1
            dv = int(rng.choice(value_pool))
            chunks.append(make_chunk(dk, dv))
    return chunks, true_idx


def build_seq_from_chunk(chunk, key):
    """anchor chunk (5) ++ query [key REL] (2) = length-7 fed sequence (H_1147 layout)."""
    return np.concatenate([chunk, np.array([key, REL], dtype=np.int64)])


def make_dataset(rng, n, value_pool, policy, head_rng_seed=None):
    """Generate n examples. For each: random key + value (from value_pool), a candidate pool,
    then apply `policy` in {prior_window, semantic, oracle} to SELECT the anchor chunk.
    Returns X[n,7], Y[n] (true value), hit[n] (selected == true chunk)."""
    X = np.zeros((n, SEQ_LEN), dtype=np.int64)
    Y = np.zeros(n, dtype=np.int64)
    hit = np.zeros(n, dtype=np.int64)
    sel_rng = np.random.default_rng(head_rng_seed if head_rng_seed is not None else 0)
    for i in range(n):
        key = int(rng.choice(KEYS))
        value = int(rng.choice(value_pool))
        distractor_keys = [k for k in KEYS if k != key]
        chunks, true_idx = make_pool(rng, key, value, value_pool, distractor_keys)
        query_tokens = [key, REL]
        if policy == "oracle":
            sel = true_idx
        elif policy == "prior_window":
            # v1 positional surrogate: ALWAYS take the fixed "preceding window" slot (index 0).
            # The true chunk is at a RANDOM position => hit only when true_idx == 0.
            sel = 0
        elif policy == "semantic":
            sel = semantic_select(query_tokens, chunks, sel_rng)
        else:
            raise ValueError(policy)
        X[i] = build_seq_from_chunk(chunks[sel], key)
        Y[i] = value
        hit[i] = int(sel == true_idx)
    return X, Y, hit


# ----------------------------------------------------------------------------- model (H_1147 copy head VERBATIM)
D = 48
STEPS = 500
LR = 0.05
BATCH = 512


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


class Model:
    """SAME RETRO copy/pointer head as H_1147 (retro=True path). The backbone self-attends; an
    explicit learned pointer cross-attends the anchor positions and copies the attended token;
    a learned gate mixes copy-dist with the vocab head."""

    def __init__(self, rng):
        s = 0.08
        self.Emb = rng.normal(0, s, (VOCAB, D))
        self.Pos = rng.normal(0, s, (SEQ_LEN, D))
        self.Wq = rng.normal(0, s, (D, D))
        self.Wk = rng.normal(0, s, (D, D))
        self.Wv = rng.normal(0, s, (D, D))
        self.Wo = rng.normal(0, s, (D, VOCAB))
        self.Pq = rng.normal(0, s, (D, D))
        self.Pk = rng.normal(0, s, (D, D))
        self.Wg = rng.normal(0, s, (D, 1))
        self._m = {}
        self._v = {}

    def params(self):
        return ["Emb", "Pos", "Wq", "Wk", "Wv", "Wo", "Pq", "Pk", "Wg"]

    def forward(self, X):
        B, T = X.shape
        Xe = X.copy()
        h0 = self.Emb[Xe] + self.Pos[None, :, :]
        Q = h0 @ self.Wq
        K = h0 @ self.Wk
        V = h0 @ self.Wv
        scores = Q @ K.transpose(0, 2, 1) / np.sqrt(D)
        A = softmax(scores, axis=-1)
        ctx = A @ V
        h = h0 + ctx
        hf = h[:, -1, :]
        logits_vocab = hf @ self.Wo

        cache = dict(Xe=Xe, h0=h0, Q=Q, K=K, V=V, A=A, ctx=ctx, h=h, hf=hf,
                     logits_vocab=logits_vocab)
        anc = np.array(ANCHOR_POSITIONS)
        hq = hf @ self.Pq
        hk = h0[:, anc, :] @ self.Pk
        pscore = np.einsum("bd,bad->ba", hq, hk) / np.sqrt(D)
        pattn = softmax(pscore, axis=-1)
        anc_tokens = Xe[:, anc]
        flat_idx = (np.arange(B)[:, None] * VOCAB + anc_tokens).reshape(-1)
        copy_dist = np.bincount(flat_idx, weights=pattn.reshape(-1),
                                minlength=B * VOCAB).reshape(B, VOCAB)
        gate = 1.0 / (1.0 + np.exp(-(hf @ self.Wg)))
        vocab_dist = softmax(logits_vocab, axis=-1)
        probs = gate * copy_dist + (1 - gate) * vocab_dist
        probs = np.clip(probs, 1e-9, 1.0)
        probs = probs / probs.sum(axis=-1, keepdims=True)
        cache.update(anc=anc, hq=hq, hk=hk, pscore=pscore, pattn=pattn,
                     anc_tokens=anc_tokens, copy_dist=copy_dist, gate=gate,
                     vocab_dist=vocab_dist, probs=probs)
        return probs, cache

    def loss_and_grad(self, X, Y):
        probs, c = self.forward(X)
        B = X.shape[0]
        loss = -np.log(probs[np.arange(B), Y] + 1e-12).mean()
        g = {n: np.zeros_like(getattr(self, n)) for n in self.params()}
        dprobs = probs.copy()
        dprobs[np.arange(B), Y] -= 1.0
        dprobs /= B

        gate = c["gate"]; copy_dist = c["copy_dist"]; vocab_dist = c["vocab_dist"]; hf = c["hf"]
        dP = dprobs
        dgate = (dP * (copy_dist - vocab_dist)).sum(axis=1, keepdims=True)
        dsig = dgate * gate * (1 - gate)
        g["Wg"] += hf.T @ dsig
        dhf_from_gate = dsig @ self.Wg.T

        dvocab_dist = dP * (1 - gate)
        tmp = (dvocab_dist * vocab_dist).sum(axis=1, keepdims=True)
        dlogits = vocab_dist * (dvocab_dist - tmp)

        anc = c["anc"]; anc_tokens = c["anc_tokens"]; pattn = c["pattn"]
        dcopy = dP * gate
        dpattn = np.take_along_axis(dcopy, anc_tokens, axis=1)
        pa = pattn
        tmp2 = (dpattn * pa).sum(axis=1, keepdims=True)
        dpscore = pa * (dpattn - tmp2)
        hq = c["hq"]; hk = c["hk"]
        dhq = np.einsum("ba,bad->bd", dpscore, hk) / np.sqrt(D)
        dhk = np.einsum("ba,bd->bad", dpscore, hq) / np.sqrt(D)
        g["Pq"] += hf.T @ dhq
        dhf_from_ptr = dhq @ self.Pq.T
        h0 = c["h0"]; h0a = h0[:, anc, :]
        g["Pk"] += np.einsum("bad,bae->de", h0a, dhk)
        dh0a = dhk @ self.Pk.T

        dhf = dhf_from_gate + dhf_from_ptr
        self._backbone_backward(c, dlogits, g, extra_dhf=dhf, dh0_anchor=(anc, dh0a))
        return loss, g

    def _backbone_backward(self, c, dlogits, g, extra_dhf=None, dh0_anchor=None):
        hf = c["hf"]
        g["Wo"] += hf.T @ dlogits
        dhf = dlogits @ self.Wo.T
        if extra_dhf is not None:
            dhf = dhf + extra_dhf
        B, T, _ = c["h0"].shape
        dh = np.zeros((B, T, D)); dh[:, -1, :] = dhf
        dh0 = dh.copy(); dctx = dh.copy()
        A = c["A"]; V = c["V"]
        dA = dctx @ V.transpose(0, 2, 1)
        dV = A.transpose(0, 2, 1) @ dctx
        dscores = A * (dA - (dA * A).sum(axis=-1, keepdims=True))
        dscores /= np.sqrt(D)
        Q = c["Q"]; K = c["K"]
        dQ = dscores @ K
        dK = dscores.transpose(0, 2, 1) @ Q
        h0 = c["h0"]
        g["Wq"] += np.einsum("btd,bte->de", h0, dQ)
        g["Wk"] += np.einsum("btd,bte->de", h0, dK)
        g["Wv"] += np.einsum("btd,bte->de", h0, dV)
        dh0 = dh0 + dQ @ self.Wq.T + dK @ self.Wk.T + dV @ self.Wv.T
        if dh0_anchor is not None:
            anc, dh0a = dh0_anchor
            dh0[:, anc, :] += dh0a
        Xe = c["Xe"]
        np.add.at(g["Emb"], Xe.reshape(-1), dh0.reshape(-1, D))
        g["Pos"] += dh0.sum(axis=0)

    def step(self, g, t, lr):
        b1, b2, eps = 0.9, 0.999, 1e-8
        for n in self.params():
            if n not in self._m:
                self._m[n] = np.zeros_like(g[n]); self._v[n] = np.zeros_like(g[n])
            self._m[n] = b1 * self._m[n] + (1 - b1) * g[n]
            self._v[n] = b2 * self._v[n] + (1 - b2) * (g[n] ** 2)
            mhat = self._m[n] / (1 - b1 ** t)
            vhat = self._v[n] / (1 - b2 ** t)
            getattr(self, n)[...] -= lr * mhat / (np.sqrt(vhat) + eps)


def train(model, Xtr, Ytr, rng, label=""):
    n = Xtr.shape[0]; loss = 0.0
    for t in range(1, STEPS + 1):
        idx = rng.integers(0, n, BATCH)
        loss, g = model.loss_and_grad(Xtr[idx], Ytr[idx])
        model.step(g, t, LR)
        if label and (t % 300 == 0 or t == 1):
            print(f"  [{label}] step {t}/{STEPS}  loss={loss:.4f}", flush=True)
    return loss


def copy_acc(model, X, Y):
    probs, _ = model.forward(X)
    pred = probs.argmax(axis=1)
    return float((pred == Y).mean()), pred


N_TRAIN = 2000
N_TEST = 500


def main():
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        log.append(s); print(s, flush=True)

    P("=" * 80)
    P("H_1148 SEMANTIC RETRIEVER vs PRIOR-WINDOW — does content-similarity retrieval ground")
    P("the H_1147 copy head BETTER than the v1 positional prior-window surrogate?  ($0 numpy)")
    P("=" * 80)
    P(f"seed={SEED} vocab={VOCAB} keys={N_KEYS} vals={N_VALS} heldout={len(HELDOUT_VALS)} "
      f"n_chunks={N_CHUNKS} D={D} steps={STEPS} batch={BATCH} n_train={N_TRAIN} n_test={N_TEST}")
    P("test values HELD-OUT (never a train target); true chunk at RANDOM pool position")
    P("=> un-memorizable; the answer MUST be COPIED from the retrieved chunk.\n")

    base_rng = np.random.default_rng(SEED)

    # ---- TRAIN the copy head ONCE on SEMANTICALLY-retrieved anchors (the deployment policy) ----
    P("[TRAIN] copy head on SEMANTIC-retrieved anchors (the v2 deployment policy)...")
    Xtr, Ytr, hit_tr = make_dataset(base_rng, N_TRAIN, TRAIN_VALS, "semantic", head_rng_seed=SEED + 10)
    model = Model(np.random.default_rng(SEED + 1))
    ltr = train(model, Xtr, Ytr, np.random.default_rng(SEED + 2), label="train")
    P(f"  train hit-rate (semantic, train pool) = {hit_tr.mean():.4f}  final loss={ltr:.4f}\n")

    # ---- EVAL the SAME trained head under 3 retrieval policies on the SAME held-out queries ----
    # Build ONE set of held-out (key,value,pool) examples; apply each policy to the SAME pools so
    # the only difference is WHICH chunk the policy selects.
    P("[EVAL] same trained head, same held-out pools, 3 retrieval policies:")
    results = {}
    for policy in ["prior_window", "semantic", "oracle"]:
        ev_rng = np.random.default_rng(SEED + 777)   # SAME seed per policy => identical pools
        Xte, Yte, hit = make_dataset(ev_rng, N_TEST, list(HELDOUT_VALS), policy, head_rng_seed=SEED + 20)
        acc, pred = copy_acc(model, Xte, Yte)
        results[policy] = dict(copy_acc=acc, fab_rate=1 - acc, hit_rate=float(hit.mean()),
                               X=Xte, Y=Yte, pred=pred)
        P(f"  {policy:13s}  copy-acc={acc:.4f}  fab-rate={1-acc:.4f}  hit-rate={hit.mean():.4f}")

    pw = results["prior_window"]; se = results["semantic"]; orc = results["oracle"]

    P("\n--- decoded HELD-OUT samples (key -> true_val | pred), SEMANTIC policy ---")
    for i in range(8):
        k = int(se["X"][i, 5]); tv = int(se["Y"][i]); pr = int(se["pred"][i])
        ok = (pr == tv)
        anc_v = int(se["X"][i, VALUE_POS_IN_ANCHOR])
        P(f"  k{k-KEY0:02d} -> true v{tv-VAL0:02d} | anchor_val "
          f"{'v%02d' % (anc_v-VAL0) if VAL0 <= anc_v < NV_PAD else 'tok%d' % anc_v} | "
          f"pred {'v%02d' % (pr-VAL0) if VAL0 <= pr < NV_PAD else 'tok%d' % pr} {'OK' if ok else 'FAB'}")

    # ---- FROZEN falsifier ----
    f1_lift = se["copy_acc"] - pw["copy_acc"]
    f2_gap = orc["copy_acc"] - se["copy_acc"]
    F1 = f1_lift >= 0.20
    F2 = f2_gap <= 0.15
    if F1 and F2:
        tier = "GREEN"; emoji = "🟢"
    elif F1:
        tier = "PARTIAL"; emoji = "🟡"
    else:
        tier = "NEUTRAL"; emoji = "🔴"

    P("\n" + "=" * 80)
    P("FROZEN FALSIFIER (bars set BEFORE run; immovable — see H_1148_FREEZE.txt)")
    P("=" * 80)
    P(f"policy copy-acc:  prior_window={pw['copy_acc']:.4f}  semantic={se['copy_acc']:.4f}  "
      f"oracle={orc['copy_acc']:.4f}")
    P(f"policy hit-rate:  prior_window={pw['hit_rate']:.4f}  semantic={se['hit_rate']:.4f}  "
      f"oracle={orc['hit_rate']:.4f}")
    P(f"F1 SEMANTIC-LIFTS   (sem - pw >= 0.20)   : {f1_lift:+.4f}   -> {'PASS' if F1 else 'FAIL'}")
    P(f"F2 APPROACHES-ORACLE(orc - sem <= 0.15)  : {f2_gap:+.4f}   -> {'PASS' if F2 else 'FAIL'}")
    P("-" * 80)
    if tier == "GREEN":
        P(f"VERDICT: {emoji} GREEN — SEMANTIC retrieval substantially out-grounds prior-window")
        P("  AND approaches the oracle ceiling. RETRO-303M v2: SWAP prior-window -> semantic.")
    elif tier == "PARTIAL":
        P(f"VERDICT: {emoji} PARTIAL — semantic lifts copy-acc over prior-window but a ceiling")
        P("  gap to oracle remains; the cheap retriever misses some true anchors. Warrants a")
        P("  stronger/learned retriever before committing the v2 swap (a_scale_honest_scope).")
    else:
        P(f"VERDICT: {emoji} NEUTRAL/CLOSED-NEG — semantic retrieval does NOT lift copy-acc over")
        P("  the v1 prior-window surrogate; v1 positional is good enough, a retriever is not")
        P("  worth it yet. Honest negative (a_paper_negative_ok). Keep v1.")
    P("=" * 80)

    result = dict(
        copy_acc_prior_window=pw["copy_acc"], copy_acc_semantic=se["copy_acc"],
        copy_acc_oracle=orc["copy_acc"],
        fab_prior_window=pw["fab_rate"], fab_semantic=se["fab_rate"], fab_oracle=orc["fab_rate"],
        hit_prior_window=pw["hit_rate"], hit_semantic=se["hit_rate"], hit_oracle=orc["hit_rate"],
        f1_lift=f1_lift, f2_gap=f2_gap, F1=bool(F1), F2=bool(F2),
        tier=tier, train_hit_rate=float(hit_tr.mean()), train_loss=ltr,
        seed=SEED, steps=STEPS, n_train=N_TRAIN, n_test=N_TEST, n_chunks=N_CHUNKS, vocab=VOCAB,
    )
    return result, "\n".join(log)


if __name__ == "__main__":
    result, logtext = main()
    out_txt = sys.argv[1] if len(sys.argv) > 1 else None
    out_json = sys.argv[2] if len(sys.argv) > 2 else None
    if out_txt:
        with open(out_txt, "w") as f:
            f.write(logtext + "\n")
    if out_json:
        with open(out_json, "w") as f:
            json.dump(result, f, indent=2)
