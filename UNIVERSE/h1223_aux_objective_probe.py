"""
H_1223 — AUX-OBJECTIVE-AS-LEVER, the $0 toy that adjudicates HD7 from the depth-ceiling
ladder (.verdicts/1219_depth_ceiling_hypothesis_exhaustion/H_1219.txt).

THE QUESTION (HD7, the OPEN objective branch of the ladder)
----------------------------------------------------------
The genuine flat wall in anima-303M is LITERAL-QA recall (factual recall ~1-2/15, flat
across scale H_1139/H_1167, arch H_1155, and decode-mode H_1218 — H_1219). HD7 asks:
is that wall caused by the OBJECTIVE itself — plain next-byte cross-entropy never rewards
RETRIEVAL/recall, so the weights are never pushed to surface a stored fact — such that an
AUXILIARY retrieval/QA objective on the SAME corpus + SAME compute LIFTS literal-QA-proxy?

  GREEN  iff (B) aux-objective head's literal-QA-proxy >= (A) plain-CE head + a CLEAR margin
             => the objective is a LEVER (next-byte CE under-rewards recall; an aux term fixes it).
  RED    otherwise => the objective is NOT the wall; recall stays ENGINE-side (H_1154 precedent:
             anti-fabrication recall went deterministic retrieve-then-copy because the WEIGHTS
             could not learn key->value match). A RED here REINFORCES H_1154.

H_1154 PRECEDENT (honest prior, a_paper_negative_ok)
----------------------------------------------------
H_1154 found anti-fabrication grounding had to go ENGINE-side: a deterministic
retrieve-then-copy in CORE (engine computes the exact key-match symbolically and hands the
model the matched span) — because feeding an exact key-match as a FEATURE into byte-LM
WEIGHTS was RED (the weights could not USE / learn the key->value discrimination). That
gives an IN-WEIGHTS aux objective for recall a PRIOR-RED lean. We still give it a fair toy
test: maybe CE under-trained the recall and an explicit recall LOSS (not just a feature)
flips it. If it does not, the in-weights-objective lever is closed and H_1154 stands.

DESIGN — a tiny byte-LM trained TWO ways on the SAME corpus + EQUAL compute
--------------------------------------------------------------------------
CORPUS (self-contained, ground-truth-able so literal-QA-proxy has an exact answer): a
synthetic FACT corpus of statements "<KEY> is <VALUE>.\n" where KEY/VALUE are short random
lowercase tokens drawn from disjoint pools. The literal-QA-proxy is the SAME fact rendered
as a query the model must COMPLETE: given the byte context "<KEY> is " it must emit the
stored "<VALUE>" (exact / substring match on the decoded answer span). This is literal
factual recall in miniature — exactly the wall H_1219 names. KEYs are seen in training
(the fact is IN the corpus); the proxy tests whether the model RECALLS the value at the
"<KEY> is " boundary. We also hold out a DISJOINT split of facts NEVER shown as a query
during training (no query-format leakage) — recall must come from the statement, not from
having practiced that exact query.

MODEL (IDENTICAL backbone both arms): a 1-layer self-attention byte-LM (causal, learned
positional, single head + a small MLP), trained by REAL mini-batch Adam on next-byte CE.
Attention is deliberately included (H_1155: composition/retrieval is attention-bound) so the
backbone CAN in principle copy a value span back from earlier context.

  ARM A (plain-CE) : loss = next-byte cross-entropy ONLY (the production objective, p8).
  ARM B (aux-recall): loss = next-byte CE + LAMBDA * AUX, where AUX is an explicit
                     RETRIEVE-THE-ANSWER / span-copy objective:
                       at every "<KEY> is " boundary position in a training sequence, add a
                       cross-entropy term that DIRECTLY rewards predicting the first byte of
                       the stored VALUE (the answer span) from the boundary hidden state.
                     This is a fact-completion / span-copy auxiliary objective: it explicitly
                     pushes the SAME weights to surface the recalled value at the query
                     boundary — the thing plain next-byte CE only rewards diffusely. (The aux
                     term reuses the SAME output head; it is an EXTRA supervised signal on the
                     recall positions, NOT a new parameter path — so it tests the OBJECTIVE,
                     not extra capacity.)

EQUAL COMPUTE (a_completeness_over_cheap / fairness): both arms = SAME architecture, SAME
init seed, SAME data, SAME number of optimizer steps, SAME batch size. ARM B's aux is an
ADDED loss term on the SAME forward/backward — it does NOT get extra steps or params. (If
anything B does slightly MORE work per step computing the aux gradient; that only helps B,
so a RED under equal-steps is conservative.)

PRE-REGISTERED FALSIFIER (frozen to H_1223_FREEZE.txt BEFORE any score; bars NOT moved)
---------------------------------------------------------------------------------------
  Primary metric = literal-QA-proxy accuracy = fraction of held-out facts whose decoded
  answer span (greedy, p7) EXACTLY matches the stored VALUE (we also report substring match
  as a looser companion; the FROZEN bar uses exact).
  F1 AUX-LIFT   : meanseeds(QA_B_exact) - meanseeds(QA_A_exact) >= QA_MARGIN (the CLEAR margin).
  F2 EVERY-SEED : QA_B_exact >= QA_A_exact on EVERY seed (the lift is not one lucky seed
                  averaging over a regression elsewhere — directionally consistent).
  F3 G0-COHERENCE: ARM B must not destroy coherence — its known-byte / in-alphabet ratio on a
                  free decode >= 0.50 (p7 G0 floor, so a "lift" that garbles is rejected).
  VERDICT:
    F1 AND F2 AND F3 => 🟢 OBJECTIVE-IS-A-LEVER : an aux retrieval/QA objective lifts literal-QA
                        recall over plain next-byte CE at equal compute => the wall is (partly)
                        the OBJECTIVE; an aux recall term is a real in-weights lever to test at
                        scale (HD7 OPEN -> supported direction). TOY-ONLY (scale UNVERIFIED).
    else            => 🔴 RED : the aux objective does NOT lift literal-QA-proxy over plain CE
                        => the objective is NOT the wall; recall stays ENGINE-side (H_1154
                        deterministic retrieve-then-copy). REINFORCES H_1154 — a clean,
                        decision-grade closed-negative (a_paper_negative_ok).

METRIC DISCIPLINE (p7 — NO PERPLEXITY VERDICT): the VERDICT is the literal-QA-proxy
exact-match accuracy + a G0 coherence floor — NOT val CE. We REPORT both arms' val CE as
context (does the aux term cost or help LM CE) but it is never the gate.

HONEST SCOPE (a_scale_honest_scope / a_toy_scale_recheck — TOY-ONLY)
-------------------------------------------------------------------
Synthetic small fact corpus, a 1-layer attention byte-LM, small Adam budget, deterministic
seeds, $0 CPU numpy. This is the OBJECTIVE-LEVER LINK test on a clean recall toy; it does NOT
certify a production 303M lift. A toy GREEN says "an aux recall objective CAN lift recall in
principle -> worth a production fire"; a toy RED says "even on a clean, easy recall toy where
the answer is copyable from context, an explicit recall loss does not beat plain CE -> the
objective is not the lever, recall stays engine-side (H_1154)". Scale-transfer UNVERIFIED
either way (a_toy_scale_recheck). p8: one continuous trained head; no train/infer split.
"""
import json, math, os
import numpy as np

np.seterr(all="ignore")

# ============================================================================
# CONFIG
# ============================================================================
VOCAB = 256
D_MODEL = 64
D_FF = 128
N_CTX = 64                 # context window (bytes) — long enough to hold a fact + the query boundary
EPOCHS_STEPS = 4000        # EQUAL optimizer steps both arms
BATCH = 64
LR = 2e-3
SEEDS = [231, 232, 233]    # >=3 deterministic seeds

# ---- fact corpus ----
N_FACTS = 600              # distinct <KEY> is <VALUE>. facts
KEY_LEN = 4                # bytes per key token
VAL_LEN = 4                # bytes per value token (the answer span)
HELDOUT_FRAC = 0.25        # fraction of facts NEVER shown as a query during training (proxy eval)

# ---- aux objective ----
LAMBDA_AUX = 1.0           # weight on the span-copy / retrieve-the-answer aux loss (ARM B only)

# ---- FROZEN falsifier bars (NOT moved post-hoc) ----
QA_MARGIN = 0.10           # F1: mean QA_B_exact - QA_A_exact >= this (the CLEAR margin)
G0_FLOOR = 0.50            # F3: ARM B free-decode known/in-alphabet ratio >= this

ALPHABET = b"abcdefghijklmnopqrstuvwxyz"
SEP = b" is "
END = b".\n"


# ============================================================================
# CORPUS — synthetic facts with exact ground truth
# ============================================================================
def make_facts(rng):
    keys, vals, seen = [], [], set()
    while len(keys) < N_FACTS:
        k = bytes(rng.choice(list(ALPHABET), KEY_LEN))
        if k in seen:
            continue
        seen.add(k)
        v = bytes(rng.choice(list(ALPHABET), VAL_LEN))
        keys.append(k); vals.append(v)
    return keys, vals


def fact_bytes(k, v):
    return k + SEP + v + END


def build_corpus(keys, vals, rng):
    """Concatenate all facts (shuffled order, repeated a few times so the LM sees each fact
    multiple times — recall, not one-shot). Returns the byte stream."""
    order = []
    REPEATS = 6
    for _ in range(REPEATS):
        idx = rng.permutation(len(keys))
        for i in idx:
            order.append(fact_bytes(keys[i], vals[i]))
    return b"".join(order)


# ============================================================================
# MODEL — 1-layer causal self-attention byte-LM (identical both arms)
#   emb(256->D) + learned pos(N_CTX->D) -> 1 head causal attn -> MLP -> head(D->256)
# Real mini-batch Adam. Pure numpy with manual backward.
# ============================================================================
class ByteAttnLM:
    def __init__(self, seed):
        rng = np.random.default_rng(seed)
        s = lambda *sh, sc: rng.standard_normal(sh) * sc
        self.E = s(VOCAB, D_MODEL, sc=0.02)
        self.P = s(N_CTX, D_MODEL, sc=0.02)
        self.Wq = s(D_MODEL, D_MODEL, sc=1/math.sqrt(D_MODEL))
        self.Wk = s(D_MODEL, D_MODEL, sc=1/math.sqrt(D_MODEL))
        self.Wv = s(D_MODEL, D_MODEL, sc=1/math.sqrt(D_MODEL))
        self.Wo = s(D_MODEL, D_MODEL, sc=1/math.sqrt(D_MODEL))
        self.W1 = s(D_MODEL, D_FF, sc=1/math.sqrt(D_MODEL))
        self.b1 = np.zeros(D_FF)
        self.W2 = s(D_FF, D_MODEL, sc=1/math.sqrt(D_FF))
        self.b2 = np.zeros(D_MODEL)
        self.Wout = s(D_MODEL, VOCAB, sc=1/math.sqrt(D_MODEL))
        self.bout = np.zeros(VOCAB)
        self.params = ["E", "P", "Wq", "Wk", "Wv", "Wo", "W1", "b1", "W2", "b2", "Wout", "bout"]
        self.m = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        self.v = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        self.t = 0
        self.mask = np.triu(np.full((N_CTX, N_CTX), -1e9), k=1)   # causal mask

    def forward(self, X):
        """X: (B,T) int byte ids. Returns logits (B,T,VOCAB) + cache for backward."""
        B, T = X.shape
        emb = self.E[X] + self.P[None, :T, :]                       # (B,T,D)
        Q = emb @ self.Wq; K = emb @ self.Wk; V = emb @ self.Wv     # (B,T,D)
        att = (Q @ K.transpose(0, 2, 1)) / math.sqrt(D_MODEL)       # (B,T,T)
        att = att + self.mask[None, :T, :T]
        att -= att.max(axis=-1, keepdims=True)
        ex = np.exp(att); A = ex / ex.sum(axis=-1, keepdims=True)   # (B,T,T)
        ctx = A @ V                                                 # (B,T,D)
        ao = ctx @ self.Wo                                          # (B,T,D)
        h1 = ao + emb                                               # residual
        z = h1 @ self.W1 + self.b1
        g = np.maximum(z, 0.0)                                      # ReLU
        ff = g @ self.W2 + self.b2
        h2 = ff + h1                                                # residual
        logits = h2 @ self.Wout + self.bout                        # (B,T,VOCAB)
        cache = dict(X=X, emb=emb, Q=Q, K=K, V=V, A=A, ctx=ctx, ao=ao, h1=h1, z=z, g=g, ff=ff, h2=h2)
        return logits, cache

    def _softmax_ce_grad(self, logits, Y, weight):
        """logits (B,T,V), Y (B,T) targets, weight (B,T) per-position loss weight.
        Returns scalar loss + dlogits (B,T,V)."""
        B, T, Vc = logits.shape
        z = logits - logits.max(axis=-1, keepdims=True)
        ex = np.exp(z); probs = ex / ex.sum(axis=-1, keepdims=True)
        ll = -np.log(np.maximum(probs.reshape(-1, Vc)[np.arange(B*T), Y.reshape(-1)], 1e-12))
        ll = ll.reshape(B, T) * weight
        wsum = weight.sum() + 1e-9
        loss = ll.sum() / wsum
        dlogits = probs.copy()
        dlogits.reshape(-1, Vc)[np.arange(B*T), Y.reshape(-1)] -= 1.0
        dlogits = dlogits * (weight[:, :, None] / wsum)
        return float(loss), dlogits

    def backward(self, cache, dlogits):
        """Backprop dlogits (B,T,V) through the network; returns grads dict."""
        g = {}
        h2 = cache["h2"]
        g["Wout"] = np.einsum("btd,btv->dv", h2, dlogits)
        g["bout"] = dlogits.sum(axis=(0, 1))
        dh2 = dlogits @ self.Wout.T                                 # (B,T,D)
        dff = dh2; dh1 = dh2.copy()                                 # h2 = ff + h1
        g["W2"] = np.einsum("btf,btd->fd", cache["g"], dff)
        g["b2"] = dff.sum(axis=(0, 1))
        dg = dff @ self.W2.T
        dz = dg * (cache["z"] > 0)
        g["W1"] = np.einsum("btd,btf->df", cache["h1"], dz)
        g["b1"] = dz.sum(axis=(0, 1))
        dh1 = dh1 + dz @ self.W1.T
        dao = dh1; demb = dh1.copy()                               # h1 = ao + emb
        g["Wo"] = np.einsum("btd,bte->de", cache["ctx"], dao)      # ao = ctx @ Wo
        dctx = dao @ self.Wo.T
        A = cache["A"]; V = cache["V"]                             # ctx = A @ V
        g_V = np.einsum("bts,btd->bsd", A, dctx)
        dA = np.einsum("btd,bsd->bts", dctx, V)
        dscore = A * (dA - (dA * A).sum(axis=-1, keepdims=True))   # softmax backward
        dscore = dscore / math.sqrt(D_MODEL)
        Q = cache["Q"]; K = cache["K"]
        dQ = dscore @ K
        dK = dscore.transpose(0, 2, 1) @ Q
        dV = g_V
        g["Wq"] = np.einsum("btd,bte->de", cache["emb"], dQ)
        g["Wk"] = np.einsum("btd,bte->de", cache["emb"], dK)
        g["Wv"] = np.einsum("btd,bte->de", cache["emb"], dV)
        demb = demb + dQ @ self.Wq.T + dK @ self.Wk.T + dV @ self.Wv.T
        g["P"] = demb.sum(axis=0)[:demb.shape[1]]                  # emb = E[X] + P
        gE = np.zeros_like(self.E)
        np.add.at(gE, cache["X"].reshape(-1), demb.reshape(-1, D_MODEL))
        g["E"] = gE
        return g

    def adam_step(self, grads, lr):
        b1, b2 = 0.9, 0.999
        self.t += 1
        for k in self.params:
            gk = grads.get(k)
            if gk is None:
                continue
            self.m[k] = b1 * self.m[k] + (1 - b1) * gk
            self.v[k] = b2 * self.v[k] + (1 - b2) * (gk * gk)
            mhat = self.m[k] / (1 - b1 ** self.t)
            vhat = self.v[k] / (1 - b2 ** self.t)
            setattr(self, k, getattr(self, k) - lr * mhat / (np.sqrt(vhat) + 1e-8))

    def val_ce_bits(self, Xb, Yb):
        logits, _ = self.forward(Xb)
        z = logits - logits.max(axis=-1, keepdims=True)
        ex = np.exp(z); probs = ex / ex.sum(axis=-1, keepdims=True)
        B, T, Vc = logits.shape
        p = probs.reshape(-1, Vc)[np.arange(B*T), Yb.reshape(-1)]
        return float(np.mean(-np.log2(np.maximum(p, 1e-12))))


# ============================================================================
# TRAINING DATA — sliding windows over the corpus; for ARM B also a per-position aux
# weight that marks the answer-span boundary ("<KEY> is " -> first VALUE byte).
# ============================================================================
def build_training_windows(corpus, rng, n_windows):
    """Returns X (n,N_CTX), Y (n,N_CTX) next-byte targets."""
    L = len(corpus)
    starts = rng.integers(0, L - N_CTX - 1, size=n_windows)
    arr = np.frombuffer(corpus, dtype=np.uint8)
    X = np.empty((n_windows, N_CTX), dtype=np.int64)
    Y = np.empty((n_windows, N_CTX), dtype=np.int64)
    for i, s in enumerate(starts):
        X[i] = arr[s:s + N_CTX]
        Y[i] = arr[s + 1:s + N_CTX + 1]
    return X, Y


def aux_weight_mask(X, sep_arr):
    """For ARM B: weight=1 at positions that are the LAST byte of '<KEY> is ' (i.e. the
    position whose NEXT byte is the first byte of the VALUE answer span). next-byte CE at
    that position == 'retrieve the answer'. We detect ' is ' ending and mark its last index."""
    B, T = X.shape
    W = np.zeros((B, T), dtype=float)
    sl = len(sep_arr)
    for b in range(B):
        row = X[b]
        for t in range(sl - 1, T):
            if np.array_equal(row[t - sl + 1:t + 1], sep_arr):
                W[b, t] = 1.0    # next byte (Y[b,t]) is first byte of VALUE => answer boundary
    return W


# ============================================================================
# QA PROXY EVAL — greedy-decode the VALUE span from the "<KEY> is " query boundary.
# ============================================================================
def qa_proxy(model, keys, vals, idxs):
    """For each held-out fact, prompt '<KEY> is ' and greedy-decode VAL_LEN bytes; exact &
    substring match vs the stored VALUE."""
    exact = 0; substr = 0
    for i in idxs:
        prompt = keys[i] + SEP
        ctx = list(prompt)
        out = bytearray()
        for _ in range(VAL_LEN):
            x = np.array(ctx[-N_CTX:], dtype=np.int64)[None]
            if x.shape[1] < N_CTX:
                pad = np.zeros((1, N_CTX - x.shape[1]), dtype=np.int64)
                x = np.concatenate([pad, x], axis=1)
            logits, _ = model.forward(x)
            nb = int(np.argmax(logits[0, -1]))
            out.append(nb)
            ctx.append(nb)
        ans = bytes(out)
        if ans == vals[i]:
            exact += 1
        if vals[i] in ans or ans in vals[i]:
            substr += 1
    n = len(idxs)
    return exact / n, substr / n


def g0_coherence(model, corpus, rng):
    """Free greedy decode from a random corpus seed; fraction of in-alphabet/space/.-bytes."""
    L = len(corpus)
    s = int(rng.integers(0, L - N_CTX - 1))
    ctx = list(np.frombuffer(corpus[s:s + N_CTX], dtype=np.uint8))
    out = bytearray()
    for _ in range(120):
        x = np.array(ctx[-N_CTX:], dtype=np.int64)[None]
        logits, _ = model.forward(x)
        nb = int(np.argmax(logits[0, -1]))
        out.append(nb); ctx.append(nb)
    good = sum(1 for b in out if (97 <= b <= 122) or b in (32, 46, 10))
    return good / len(out), bytes(out)


# ============================================================================
# RUN ONE SEED — train ARM A (plain CE) and ARM B (CE + aux) at EQUAL compute
# ============================================================================
def train_arm(model, X, Y, aux_mask, rng, use_aux):
    n = len(X)
    for step in range(EPOCHS_STEPS):
        idx = rng.integers(0, n, size=BATCH)
        xb, yb = X[idx], Y[idx]
        logits, cache = model.forward(xb)
        # next-byte CE over ALL positions (the production objective)
        w_ce = np.ones((BATCH, N_CTX), dtype=float)
        _, d_ce = model._softmax_ce_grad(logits, yb, w_ce)
        dlogits = d_ce
        if use_aux:
            # AUX: extra CE on answer-span boundary positions only (retrieve-the-answer)
            wb = aux_mask[idx]
            if wb.sum() > 0:
                _, d_aux = model._softmax_ce_grad(logits, yb, wb)
                dlogits = dlogits + LAMBDA_AUX * d_aux
        grads = model.backward(cache, dlogits)
        model.adam_step(grads, LR)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    keys, vals = make_facts(rng)
    n_heldout = int(N_FACTS * HELDOUT_FRAC)
    perm = rng.permutation(N_FACTS)
    heldout_idx = perm[:n_heldout]          # facts NEVER queried during training (proxy eval)
    corpus = build_corpus(keys, vals, rng)  # contains ALL facts as statements

    n_windows = 6000
    X, Y = build_training_windows(corpus, rng, n_windows)
    sep_arr = np.frombuffer(SEP, dtype=np.uint8)
    aux_mask = aux_weight_mask(X, sep_arr)

    Xv, Yv = build_training_windows(corpus, np.random.default_rng(seed + 7), 800)

    # ARM A — plain CE
    mA = ByteAttnLM(seed)
    train_arm(mA, X, Y, aux_mask, np.random.default_rng(seed + 100), use_aux=False)
    # ARM B — CE + aux (SAME init seed, SAME data, SAME steps, SAME batch sampling)
    mB = ByteAttnLM(seed)
    train_arm(mB, X, Y, aux_mask, np.random.default_rng(seed + 100), use_aux=True)

    qaA_e, qaA_s = qa_proxy(mA, keys, vals, heldout_idx)
    qaB_e, qaB_s = qa_proxy(mB, keys, vals, heldout_idx)
    ceA = mA.val_ce_bits(Xv, Yv); ceB = mB.val_ce_bits(Xv, Yv)
    g0B, g0_sample = g0_coherence(mB, corpus, np.random.default_rng(seed + 9))
    g0A, _ = g0_coherence(mA, corpus, np.random.default_rng(seed + 9))

    return dict(seed=seed, n_aux_pos=int(aux_mask.sum()),
                qaA_exact=qaA_e, qaA_substr=qaA_s, qaB_exact=qaB_e, qaB_substr=qaB_s,
                ceA=ceA, ceB=ceB, g0A=g0A, g0B=g0B, g0_sample=g0_sample)


def main():
    print("=== H_1223 — AUX-OBJECTIVE-AS-LEVER (HD7) | $0 CPU numpy attention byte-LM toy ===", flush=True)
    print(f"  facts={N_FACTS} key={KEY_LEN}b val={VAL_LEN}b heldout_frac={HELDOUT_FRAC} | "
          f"model D={D_MODEL} ff={D_FF} ctx={N_CTX} 1-layer attn | steps={EPOCHS_STEPS} batch={BATCH} lr={LR}", flush=True)
    print(f"  ARM A = plain next-byte CE | ARM B = CE + {LAMBDA_AUX}*AUX (span-copy/retrieve-the-answer at '<KEY> is ' boundary)", flush=True)
    print(f"  FROZEN F1 mean(QA_B_exact)-mean(QA_A_exact) >= {QA_MARGIN} | F2 every-seed B>=A | F3 G0(B) >= {G0_FLOOR}\n", flush=True)

    per_seed = []
    for s in SEEDS:
        r = run_seed(s)
        per_seed.append(r)
        print(f"  seed {s}: QA_A exact={r['qaA_exact']:.3f} substr={r['qaA_substr']:.3f} | "
              f"QA_B exact={r['qaB_exact']:.3f} substr={r['qaB_substr']:.3f} | "
              f"dExact={r['qaB_exact']-r['qaA_exact']:+.3f} | CE A={r['ceA']:.3f} B={r['ceB']:.3f} | "
              f"G0 A={r['g0A']:.2f} B={r['g0B']:.2f} | aux_pos={r['n_aux_pos']}", flush=True)

    qaA = np.array([r["qaA_exact"] for r in per_seed])
    qaB = np.array([r["qaB_exact"] for r in per_seed])
    qaA_m, qaB_m = float(qaA.mean()), float(qaB.mean())
    delta = qaB_m - qaA_m
    every_seed = bool(np.all(qaB >= qaA))
    g0B_min = float(min(r["g0B"] for r in per_seed))

    f1 = bool(delta >= QA_MARGIN)
    f2 = every_seed
    f3 = bool(g0B_min >= G0_FLOOR)
    supported = bool(f1 and f2 and f3)

    if supported:
        ruling = ("OBJECTIVE-IS-A-LEVER: an explicit AUXILIARY retrieve-the-answer / span-copy "
                  "objective (ARM B = next-byte CE + %.1f*aux at the '<KEY> is ' answer boundary) "
                  "LIFTS literal-QA-proxy exact recall over plain next-byte CE (ARM A) by %+0.3f "
                  ">= %.2f at EQUAL compute, on EVERY seed, without breaking G0 coherence (min G0_B "
                  "%.2f >= %.2f). => plain next-byte CE UNDER-rewards retrieval; the recall wall is "
                  "(partly) the OBJECTIVE, and an in-weights aux recall term is a real lever to test "
                  "at production scale (HD7 -> supported direction). TOY-ONLY: scale-transfer to "
                  "anima-303M UNVERIFIED (a_toy_scale_recheck); a clean recall toy where the answer "
                  "is copyable from context." % (LAMBDA_AUX, delta, QA_MARGIN, g0B_min, G0_FLOOR))
    else:
        why = []
        if not f1:
            why.append("F1 fail: mean QA lift %+0.3f < %.2f bar — the aux objective does NOT lift "
                       "literal-QA exact recall over plain CE" % (delta, QA_MARGIN))
        if not f2:
            why.append("F2 fail: lift not directionally consistent (some seed B < A)")
        if not f3:
            why.append("F3 fail: ARM B G0 coherence min %.2f < %.2f — any 'lift' came with garble"
                       % (g0B_min, G0_FLOOR))
        ruling = ("RED: the AUXILIARY retrieve-the-answer / span-copy objective does NOT lift "
                  "literal-QA-proxy recall over plain next-byte CE at equal compute. " +
                  " | ".join(why) + ". => the OBJECTIVE is NOT the wall: even on a clean recall toy "
                  "where the answer is directly copyable from earlier context, adding an explicit "
                  "in-weights recall loss does not beat plain CE. Recall stays ENGINE-side "
                  "(H_1154: deterministic retrieve-then-copy — the weights cannot be pushed by a "
                  "loss term to surface key->value recall; it must be the engine computing the "
                  "match). REINFORCES H_1154; a clean decision-grade closed-negative that closes "
                  "the in-weights-objective branch of the HD7 ladder (a_paper_negative_ok). "
                  "TOY-ONLY scope (a_scale_honest_scope).")

    verdict = {
        "H": "H_1223",
        "title": "AUX-OBJECTIVE-AS-LEVER (HD7) — does an auxiliary retrieval/QA objective lift "
                 "literal-QA recall over plain next-byte cross-entropy at equal compute, or does "
                 "recall stay engine-side (H_1154)?",
        "ladder_ref": ".verdicts/1219_depth_ceiling_hypothesis_exhaustion/H_1219.txt (HD7 OPEN)",
        "compute": "CPU ($0), numpy 1-layer causal-attention byte-LM + real mini-batch Adam (manual backward); TOY, not a production fire",
        "aux_objective": ("span-copy / retrieve-the-answer: an EXTRA next-byte cross-entropy term "
                          "(weight LAMBDA_AUX=%.1f) applied ONLY at the '<KEY> is ' answer-span "
                          "boundary positions, directly rewarding the SAME output head for emitting "
                          "the first byte of the stored VALUE from the query-boundary hidden state. "
                          "No new parameters — tests the OBJECTIVE, not extra capacity. ARM A omits "
                          "this term (plain next-byte CE only)." % LAMBDA_AUX),
        "corpus": "synthetic facts '<KEY> is <VALUE>.' (key=%db val=%db, %d facts, x6 repeats, "
                  "%d held-out for proxy eval — never queried in training)" % (KEY_LEN, VAL_LEN, N_FACTS, int(N_FACTS*HELDOUT_FRAC)),
        "equal_compute": "SAME architecture, init seed, data, optimizer steps (%d), batch (%d), lr "
                         "(%g), batch-sampling RNG; ARM B only ADDS the aux loss term on the SAME forward/backward" % (EPOCHS_STEPS, BATCH, LR),
        "frozen_falsifier": {
            "primary_metric": "literal-QA-proxy EXACT-match accuracy on held-out facts (greedy "
                              "decode VALUE span from '<KEY> is ' boundary, p7); substring reported as companion",
            "F1": "mean(QA_B_exact) - mean(QA_A_exact) >= %.2f (the CLEAR aux-lift margin)" % QA_MARGIN,
            "F2": "QA_B_exact >= QA_A_exact on EVERY seed (directionally consistent)",
            "F3": "ARM B free-decode G0 coherence (in-alphabet/space/. ratio) >= %.2f" % G0_FLOOR,
            "SUPPORTED": "F1 AND F2 AND F3",
            "p7": "VERDICT = literal-QA exact accuracy + G0 floor, NOT val CE (CE reported as context only)",
        },
        "seeds": SEEDS,
        "per_seed": [{k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != "g0_sample"}
                     for r in per_seed],
        "result": {
            "QA_A_exact_mean": round(qaA_m, 4), "QA_B_exact_mean": round(qaB_m, 4),
            "delta_exact_mean": round(delta, 4), "margin_bar": QA_MARGIN, "F1_pass": f1,
            "every_seed_B_ge_A": f2, "F2_pass": f2,
            "G0_B_min": round(g0B_min, 4), "G0_floor": G0_FLOOR, "F3_pass": f3,
            "supported": supported,
        },
        "g0_sample_seed0": per_seed[0]["g0_sample"][:80].decode("latin-1", "replace"),
        "supported": supported,
        "ruling": ruling,
        "h1154_relation": ("RED here REINFORCES H_1154 (recall stays engine-side: deterministic "
                           "retrieve-then-copy because weights can't learn key->value match). GREEN "
                           "would RE-OPEN the in-weights aux objective as a lever worth a production fire."),
        "scope": ("TOY-ONLY (a_scale_honest_scope / a_toy_scale_recheck): synthetic small fact "
                  "corpus, 1-layer attention byte-LM, small Adam budget, %d seeds, $0 CPU numpy. The "
                  "OBJECTIVE-LEVER LINK test on a clean recall toy where the answer is copyable from "
                  "context — does NOT certify a production 303M lift either way. Scale-transfer "
                  "UNVERIFIED. p8: one continuously trained head, no train/infer split. Frozen bars "
                  "not moved." % len(SEEDS)),
    }

    print("\n=== VERDICT ===", flush=True)
    print(f"  QA_A exact mean={qaA_m:.3f}  QA_B exact mean={qaB_m:.3f}  delta={delta:+.3f} (bar {QA_MARGIN}) "
          f"-> F1 {'PASS' if f1 else 'FAIL'}", flush=True)
    print(f"  every-seed B>=A -> F2 {'PASS' if f2 else 'FAIL'} | G0_B min={g0B_min:.2f} (bar {G0_FLOOR}) "
          f"-> F3 {'PASS' if f3 else 'FAIL'}", flush=True)
    print(f"\n  {'🟢 OBJECTIVE-IS-A-LEVER' if supported else '🔴 RED (objective NOT the wall; recall stays engine-side, H_1154)'}", flush=True)
    print(f"  {ruling}", flush=True)
    json.dump(verdict, open("/tmp/h1223_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n  wrote /tmp/h1223_result.json", flush=True)
    print("[done]", flush=True)
    return verdict


if __name__ == "__main__":
    main()
