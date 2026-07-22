#!/usr/bin/env python3
"""G0 — the natural-form gate, at toy scale. numpy only, no torch, runs on a laptop.

WHAT IT ASKS (the owner's objection, made falsifiable)
------------------------------------------------------
A composition lane trained on ONE phrasing must answer the SAME facts asked in phrasings
it never saw. If it only answers the drill's own template, it is a template matcher, and
no amount of P1-P5 changes that. This is philosophy p9 in one executable file.

WHY A TOY IS ENOUGH HERE
------------------------
The question is not "how well does it compose" (that needs 303M and a pool host). It is
"does the composed faculty survive a change of wording that leaves the content identical".
That is a structural property and it shows up at 8x8.

FAITHFUL TO THE LANE-BUS SPLIT
------------------------------
The toy mirrors the design being tested, not a generic classifier:

    shared embedding E  <- trained ONLY by the FORM lane (all phrasings, all train cells)
             |
             | .detach()          <- the comp lane's CE never reaches E, exactly as
             v                       --comp-lane detaches the trunk penultimate
    comp head (MLP)     <- trained ONLY on phrasing T0 and train cells

So the comp head has to read composition off a representation that natural-language
statistics alone have shaped. If it can only do that when the frame words match its
training frame, the faculty is bound to the template.

TABLE DESIGN (this is load-bearing, per the P2 additive-ceiling measurement)
---------------------------------------------------------------------------
The (a,b)->v table is a random LATIN SQUARE, so both marginals are exactly uniform and a
per-cue lookup is chance by construction. A plain random table would let a purely additive
model reach ~0.54, which is above this gate's bar -- measured, not assumed.

READING
-------
    A  T0    x held-out cells   POSITIVE CONTROL. Low => INSTRUMENT-DEAD, read nothing else.
    B  T1-T4 x held-out cells   THE GATE. This is the number the objection is about.
    C  T1-T4 x train cells      isolates phrasing from cell novelty.
    D  value-permute            must collapse, else the readout is not content-addressed.
    E  frame-only (fillers)     must be chance, else the frame alone predicts the answer.

Chance is DERIVED from the realized partition (1/|V|), never assumed.
Verdict vocabulary is deliberately narrow: this screen may KILL, never GREEN.
"""
import numpy as np

N_A = N_B = N_V = 8
HELD = 16                      # of 64 cells
D = 48
SEEDS = (7, 11, 4302)

TEMPLATES = [
    # T0 is the DRILL phrasing -- the only one the comp lane ever sees.
    ("blend", "{a}", "with", "{b}", "yields", "{v}"),
    ("when", "{a}", "meets", "{b}", "the", "result", "is", "{v}"),
    ("{a}", "and", "{b}", "together", "give", "{v}"),
    ("putting", "{a}", "beside", "{b}", "produces", "{v}"),
    ("the", "outcome", "of", "{a}", "plus", "{b}", "equals", "{v}"),
]


def latin(n, rng):
    """Random latin square: both marginals exactly uniform => per-cue lookup is chance."""
    base = rng.permutation(n)
    sq = np.stack([np.roll(base, -i) for i in range(n)])
    return sq[rng.permutation(n)][:, rng.permutation(n)]


def build_vocab():
    ops_a = ["a%d" % i for i in range(N_A)]
    ops_b = ["b%d" % i for i in range(N_B)]
    vals = ["v%d" % i for i in range(N_V)]
    frame = sorted({w for t in TEMPLATES for w in t if not w.startswith("{")})
    fillers = ["x%d" % i for i in range(N_A + N_B)]        # arm E only, never trained
    vocab = ops_a + ops_b + vals + frame + fillers
    return vocab, {w: i for i, w in enumerate(vocab)}, ops_a, ops_b, vals, fillers


def render(tmpl, a, b, v):
    out = []
    for w in tmpl:
        out.append(a if w == "{a}" else b if w == "{b}" else v if w == "{v}" else w)
    return out


def softmax_rows(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def run(seed, steps_form=6000, steps_comp=6000, lr=0.5, verbose=False):
    rng = np.random.default_rng(seed)
    vocab, ix, ops_a, ops_b, vals, fillers = build_vocab()
    table = latin(N_A, rng)                                  # table[a,b] = value index

    cells = [(i, j) for i in range(N_A) for j in range(N_B)]
    order = rng.permutation(len(cells))
    held = {cells[k] for k in order[:HELD]}
    train_cells = [c for c in cells if c not in held]
    held_cells = [c for c in cells if c in held]

    # ---- FORM lane: masked-token prediction over ALL phrasings, TRAIN cells only -------
    # Held-out cells are withheld from BOTH lanes; otherwise the form lane simply teaches
    # the answer and the gate measures nothing.
    form_ctx, form_tgt = [], []
    for (i, j) in train_cells:
        for t in TEMPLATES:
            toks = [ix[w] for w in render(t, ops_a[i], ops_b[j], vals[table[i, j]])]
            for m in range(len(toks)):
                form_ctx.append([toks[k] for k in range(len(toks)) if k != m])
                form_tgt.append(toks[m])
    maxlen = max(len(c) for c in form_ctx)
    ctx = np.zeros((len(form_ctx), maxlen), dtype=np.int64)
    msk = np.zeros((len(form_ctx), maxlen))
    for r, c in enumerate(form_ctx):
        ctx[r, :len(c)] = c
        msk[r, :len(c)] = 1.0
    tgt = np.array(form_tgt)
    V = len(vocab)

    E = rng.normal(0, 0.05, (V, D))
    Wf = rng.normal(0, 0.05, (D, V))
    n = len(tgt)
    for _ in range(steps_form):
        b = rng.integers(0, n, 256)
        h = (E[ctx[b]] * msk[b][:, :, None]).sum(1) / msk[b].sum(1, keepdims=True)
        p = softmax_rows(h @ Wf)
        p[np.arange(len(b)), tgt[b]] -= 1.0
        p /= len(b)
        gWf = h.T @ p
        gh = p @ Wf.T
        gE = np.zeros_like(E)
        contrib = (gh[:, None, :] * (msk[b] / msk[b].sum(1, keepdims=True))[:, :, None])
        np.add.at(gE, ctx[b], contrib)
        Wf -= lr * gWf
        E -= lr * gE

    # ---- COMP lane: T0 only, train cells only, reading a DETACHED E --------------------
    # The head is a 2-SLOT ATTENTION reader -- the LANE-BUS arity organ in miniature.
    # This matters: mean-pooling is additive in the embeddings, so it destroys the PAIRING
    # by construction and cannot represent the table at all (measured: held-out 0.0000
    # systematically, because a latin square guarantees the memorized value is the wrong
    # one). Two learned queries pick two slots out of the token set, so composition is
    # representable -- and the head still has to LEARN where the operands are, which is the
    # part that must not be hand-fitted (p9).
    def tokens_of(pairs, tmpl_ids, use_filler=False):
        seqs = []
        for (i, j), ti in zip(pairs, tmpl_ids):
            a = fillers[i] if use_filler else ops_a[i]
            bb = fillers[N_A + j] if use_filler else ops_b[j]
            seqs.append([ix[w] for w in render(TEMPLATES[ti], a, bb, vals[0]) if w != vals[0]])
        L = max(len(s) for s in seqs)
        T = np.zeros((len(seqs), L), dtype=np.int64)
        M = np.zeros((len(seqs), L))
        for r, s in enumerate(seqs):
            T[r, :len(s)] = s
            M[r, :len(s)] = 1.0
        return T, M

    Ttr, Mtr = tokens_of(train_cells, [0] * len(train_cells))
    Ytr = np.array([table[i, j] for (i, j) in train_cells])
    Q = rng.normal(0, 0.3, (2, D))                          # two slot queries
    W1 = rng.normal(0, 0.15, (2 * D, 96)); b1 = np.zeros(96)
    W2 = rng.normal(0, 0.15, (96, N_V)); b2 = np.zeros(N_V)
    scale = 1.0 / np.sqrt(D)
    m = len(Ytr)

    def fwd(T, M):
        Ex = E[T]                                            # DETACHED: no grad to E
        sc = np.einsum("bld,kd->bkl", Ex, Q) * scale
        sc = np.where(M[:, None, :] > 0, sc, -1e9)
        al = np.exp(sc - sc.max(axis=2, keepdims=True))
        al /= al.sum(axis=2, keepdims=True)
        S = np.einsum("bkl,bld->bkd", al, Ex)
        X = S.reshape(len(T), -1)
        h1 = np.tanh(X @ W1 + b1)
        return Ex, al, X, h1, h1 @ W2 + b2

    for _ in range(steps_comp):
        bidx = rng.integers(0, m, 64)
        Ex, al, X, h1, lg = fwd(Ttr[bidx], Mtr[bidx])
        p = softmax_rows(lg)
        p[np.arange(len(bidx)), Ytr[bidx]] -= 1.0
        p /= len(bidx)
        gW2 = h1.T @ p; gb2 = p.sum(0)
        gh1 = (p @ W2.T) * (1 - h1 ** 2)
        gW1 = X.T @ gh1; gb1 = gh1.sum(0)
        gX = (gh1 @ W1.T).reshape(len(bidx), 2, D)           # dL/dS
        gal = np.einsum("bkd,bld->bkl", gX, Ex)              # through the weighted sum
        gsc = al * (gal - (gal * al).sum(axis=2, keepdims=True))   # softmax jacobian
        gQ = np.einsum("bkl,bld->kd", gsc, Ex) * scale
        W2 -= lr * gW2; b2 -= lr * gb2
        W1 -= lr * gW1; b1 -= lr * gb1
        Q -= lr * gQ

    def acc(pairs, tmpl_ids, gold=None, use_filler=False):
        if not pairs:
            return float("nan")
        T, M = tokens_of(pairs, tmpl_ids, use_filler)
        pred = fwd(T, M)[4].argmax(1)
        y = gold if gold is not None else np.array([table[i, j] for (i, j) in pairs])
        return float((pred == y).mean())

    nat = list(range(1, len(TEMPLATES)))
    rep = lambda cs, ts: ([c for c in cs for _ in ts], [t for _ in cs for t in ts])

    A = acc(train_cells, [0] * len(train_cells))                       # train fit
    A_ho = acc(held_cells, [0] * len(held_cells))                      # positive control
    pc, pt = rep(held_cells, nat)
    B = acc(pc, pt)                                                    # THE GATE
    pc2, pt2 = rep(train_cells, nat)
    C = acc(pc2, pt2)
    perm = np.array([table[i, j] for (i, j) in held_cells])
    D_arm = acc(held_cells, [0] * len(held_cells), gold=rng.permutation(perm))
    E_arm = acc(held_cells, [0] * len(held_cells), use_filler=True)
    return dict(train=A, A=A_ho, B=B, C=C, D=D_arm, E=E_arm, chance=1.0 / N_V)


def main():
    print("G0 - natural-form gate (toy, numpy, $0).  chance = %.4f (derived, 1/|V|)"
          % (1.0 / N_V))
    print("seed   train   A:T0/held   B:NAT/held   C:NAT/train   D:vperm   E:frame-only")
    print("-" * 88)
    rs = []
    for s in SEEDS:
        r = run(s)
        rs.append(r)
        print("%-6d %.4f  %.4f      %.4f       %.4f        %.4f    %.4f"
              % (s, r["train"], r["A"], r["B"], r["C"], r["D"], r["E"]))
    print("-" * 88)
    mean = {k: float(np.mean([r[k] for r in rs])) for k in ("train", "A", "B", "C", "D", "E")}
    print("mean   %.4f  %.4f      %.4f       %.4f        %.4f    %.4f"
          % (mean["train"], mean["A"], mean["B"], mean["C"], mean["D"], mean["E"]))
    ch = 1.0 / N_V
    print()
    # A screen may KILL, never GREEN -- the vocabulary below is deliberately one-sided.
    if mean["A"] < 0.30:
        print("  INSTRUMENT-DEAD - arm A (the trained phrasing, held-out cells) is at %.4f."
              % mean["A"])
        print("  The comp lane never learned to compose at all, so arm B is unreadable.")
        print("  Read nothing else from this run (positive-control-before-reading-a-negative).")
        return
    if mean["D"] > ch * 2 or mean["E"] > ch * 2:
        print("  CONTROL-LEAK - value-permute %.4f / frame-only %.4f are above the floor."
              % (mean["D"], mean["E"]))
        print("  Something other than the operand content predicts the answer. INVALID.")
        return
    if mean["B"] <= ch * 1.5:
        print("  KILL - the composition lane is TEMPLATE-BOUND.")
        print("  It answers its own drill phrasing (A=%.4f) and collapses to the floor on"
              % mean["A"])
        print("  unseen phrasings of the SAME facts (B=%.4f, chance=%.4f)." % (mean["B"], ch))
        print("  This is p9's failure mode, reproduced in a file: a drill-installed number")
        print("  is an instrument reading, not a faculty.")
    else:
        print("  NOT KILLED on this screen - B=%.4f is above the floor (chance=%.4f)."
              % (mean["B"], ch))
        print("  That is NOT a pass. A cheap structural screen may only KILL, never GREEN")
        print("  (screen-is-a-filter-not-a-performance-predictor). The claim still has to be")
        print("  earned engine-native through anima-py; this toy is DIRECTIONAL by law.")


if __name__ == "__main__":
    main()
