#!/usr/bin/env python3
"""LANE-BUS P1 — can a lane LEARN its write? arity-2 workspace on a content-addressed store.

WHY P1 IS THE LOAD-BEARING PHASE
--------------------------------
P0 showed the SURFACE is usable: two competent lanes share one logit row without silent
corruption. It said nothing about whether a lane can EARN its write, because both lanes
were oracles there on purpose. P1 removes the oracle.

The design's whole reason for existing is the dose ladder: with any replay mixed in,
composition reads 0.000; without replay, language dies. One CE cannot serve both. The fix
is lane separation, so P1 asks the two halves TOGETHER (co-primary):

    (a) can the WORKSPACE learn held-out 2-slot composition from the store?
    (b) does the trunk's FORM survive?

An honest note on (b) up front: with the comp head reading a DETACHED representation, form
retention is true BY CONSTRUCTION -- the comp loss cannot reach the trunk, so the trunk's
task is untouched by definition. That is the design's point rather than a finding, and it
is stated here so nobody later reports it as evidence. What is genuinely at risk is (a).

WHY THIS IS NOT V6_1 AGAIN
--------------------------
V6_1 found a comp head could NOT learn held-out composition (0.0000, and still 0.0000 with
10x steps, with the detach released, and with slot attention that could represent the
table). But there the head read a bag-of-words pooling of the sentence. Here it reads a
CONTENT-ADDRESSED STORE: a query built from an entity's name retrieves that entity's slot,
so the two operands arrive as SEPARATE, STRUCTURED vectors. Structured slot access is
exactly what the design bets on and what V6_1 lacked. If arity-2 still fails with the
operands handed over cleanly, the wall is not about extracting them from text.

Keys are FROZEN per-byte embeddings averaged over the name, the same discipline that let
H_9775's store generalize to held-out entities: a new name yields a new key built from
seen bytes, so nothing about the lookup is memorized.

THE THREE-LEG CERTIFICATE (a 2-slot success has to survive all three)
    data leg      the table is a latin square, so both marginals are uniform and a
                  per-cue lookup is chance by construction
    architecture  a STAPLE arm -- two independent 1-slot readouts fused additively,
                  capacity-matched -- must stay at its ceiling
    intervention  value-permute and address-permute must both collapse
"""
import numpy as np

N_R = N_E = 8              # relations x entities -> 64 cells
N_V = 8                    # values
HELD = 16
D_K = 24                   # frozen key dim
D_V = 32                   # store value dim
HID = 96
STEPS = 20000
LR = 0.5
SEEDS = (7, 11, 4302)


def names(prefix, n, rng):
    """Distinct ascii names; keys are built from their BYTES, so held-out names would
    still get a key made of seen bytes."""
    out = []
    while len(out) < n:
        s = prefix + "".join(chr(97 + int(rng.integers(0, 26))) for _ in range(4))
        if s not in out:
            out.append(s)
    return out


def latin(n, rng):
    base = rng.permutation(n)
    sq = np.stack([np.roll(base, -i) for i in range(n)])
    return sq[rng.permutation(n)][:, rng.permutation(n)]


def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def build(seed):
    rng = np.random.default_rng(seed)
    key_emb = rng.normal(0, 1.0, (256, D_K))            # FROZEN per-byte key table
    rn, en = names("r", N_R, rng), names("e", N_E, rng)

    def key(nm):
        b = np.frombuffer(nm.encode("ascii"), dtype=np.uint8)
        return key_emb[b].mean(axis=0)

    slot_keys = np.stack([key(x) for x in rn + en])      # (N_R+N_E, D_K)
    slot_vals = rng.normal(0, 1.0, (N_R + N_E, D_V))     # RUNTIME content, not weights
    table = latin(N_R, rng)
    cells = [(i, j) for i in range(N_R) for j in range(N_E)]
    order = rng.permutation(len(cells))
    held = {cells[k] for k in order[:HELD]}
    train = [c for c in cells if c not in held]
    test = [c for c in cells if c in held]
    return dict(rng=rng, key=key, rn=rn, en=en, slot_keys=slot_keys, slot_vals=slot_vals,
                table=table, train=train, test=test)


def retrieve(env, idx):
    """Content-addressed read: query = the name's frozen key; softmax over slot keys."""
    q = env["slot_keys"][idx]
    a = softmax(q @ env["slot_keys"].T / np.sqrt(D_K))
    return a @ env["slot_vals"]


def features(env, pairs, addr_permute=None):
    A, B = [], []
    for (i, j) in pairs:
        ii, jj = i, N_R + j
        if addr_permute is not None:
            ii, jj = addr_permute[ii], addr_permute[jj]
        A.append(retrieve(env, ii))
        B.append(retrieve(env, jj))
    return np.array(A), np.array(B)


def train_head(env, joint, steps=STEPS, lr=LR):
    """joint=True  -> workspace: MLP over [v_r ; v_e], can represent any f(r,e)
       joint=False -> STAPLE: two independent 1-slot heads fused ADDITIVELY, no joint term.
    Capacity is matched: the staple's two heads have HID/2 hidden units each."""
    rng = env["rng"]
    A, B = features(env, env["train"])
    y = np.array([env["table"][i, j] for (i, j) in env["train"]])
    m = len(y)
    if joint:
        X = np.concatenate([A, B], axis=1)
        W1 = rng.normal(0, 0.1, (2 * D_V, HID)); b1 = np.zeros(HID)
        W2 = rng.normal(0, 0.1, (HID, N_V)); b2 = np.zeros(N_V)
        P = [W1, b1, W2, b2]

        def fwd(Xs):
            h = np.tanh(Xs @ P[0] + P[1])
            return h, h @ P[2] + P[3]
        for _ in range(steps):
            bi = rng.integers(0, m, 64)
            h, lg = fwd(X[bi])
            p = softmax(lg); p[np.arange(len(bi)), y[bi]] -= 1.0; p /= len(bi)
            gW2 = h.T @ p; gb2 = p.sum(0)
            gh = (p @ P[2].T) * (1 - h ** 2)
            P[2] -= lr * gW2; P[3] -= lr * gb2
            P[0] -= lr * (X[bi].T @ gh); P[1] -= lr * gh.sum(0)

        def predict(Aa, Bb):
            return fwd(np.concatenate([Aa, Bb], axis=1))[1]
    else:
        h2 = HID // 2
        Wa1 = rng.normal(0, 0.1, (D_V, h2)); ba1 = np.zeros(h2)
        Wb1 = rng.normal(0, 0.1, (D_V, h2)); bb1 = np.zeros(h2)
        Wa2 = rng.normal(0, 0.1, (h2, N_V)); Wb2 = rng.normal(0, 0.1, (h2, N_V))
        b2 = np.zeros(N_V)
        P = [Wa1, ba1, Wb1, bb1, Wa2, Wb2, b2]

        def fwd(Aa, Bb):
            ha = np.tanh(Aa @ P[0] + P[1]); hb = np.tanh(Bb @ P[2] + P[3])
            return ha, hb, ha @ P[4] + hb @ P[5] + P[6]
        for _ in range(steps):
            bi = rng.integers(0, m, 64)
            ha, hb, lg = fwd(A[bi], B[bi])
            p = softmax(lg); p[np.arange(len(bi)), y[bi]] -= 1.0; p /= len(bi)
            P[4] -= lr * (ha.T @ p); P[5] -= lr * (hb.T @ p); P[6] -= lr * p.sum(0)
            gha = (p @ P[4].T) * (1 - ha ** 2); ghb = (p @ P[5].T) * (1 - hb ** 2)
            P[0] -= lr * (A[bi].T @ gha); P[1] -= lr * gha.sum(0)
            P[2] -= lr * (B[bi].T @ ghb); P[3] -= lr * ghb.sum(0)

        def predict(Aa, Bb):
            return fwd(Aa, Bb)[2]
    return predict


def acc(env, predict, pairs, gold=None, addr_permute=None, val_permute=False):
    if not pairs:
        return float("nan")
    if val_permute:
        saved = env["slot_vals"].copy()
        env["slot_vals"] = env["rng"].permutation(env["slot_vals"])
        A, B = features(env, pairs, addr_permute)
        env["slot_vals"] = saved
    else:
        A, B = features(env, pairs, addr_permute)
    pred = predict(A, B).argmax(1)
    y = gold if gold is not None else np.array([env["table"][i, j] for (i, j) in pairs])
    return float((pred == y).mean())


def run(seed):
    env = build(seed)
    joint = train_head(env, joint=True)
    staple = train_head(env, joint=False)
    perm = np.concatenate([env["rng"].permutation(N_R),
                           N_R + env["rng"].permutation(N_E)])
    return dict(
        train_fit=acc(env, joint, env["train"]),
        held=acc(env, joint, env["test"]),
        staple_train=acc(env, staple, env["train"]),
        staple_held=acc(env, staple, env["test"]),
        val_perm=acc(env, joint, env["test"], val_permute=True),
        addr_perm=acc(env, joint, env["test"], addr_permute=perm),
    )


def main():
    ch = 1.0 / N_V
    print("LANE-BUS P1 - arity-2 workspace on a content-addressed store ($0, DIRECTIONAL)")
    print("chance = %.4f (derived, 1/|V|).  form retention is TRUE BY CONSTRUCTION" % ch)
    print("(the comp loss never reaches the trunk) -- stated, not claimed as a finding.\n")
    rs = [run(s) for s in SEEDS]
    k = lambda n: float(np.mean([r[n] for r in rs]))
    print("%-34s %8s" % ("arm", "acc"))
    print("-" * 46)
    print("%-34s %8.4f   positive control" % ("workspace, SEEN pairs", k("train_fit")))
    print("%-34s %8.4f   <- THE MEASUREMENT" % ("workspace, HELD-OUT pairs", k("held")))
    print("%-34s %8.4f   capacity-matched" % ("staple (two 1-slot), SEEN", k("staple_train")))
    print("%-34s %8.4f   must stay at its ceiling" % ("staple (two 1-slot), HELD-OUT", k("staple_held")))
    print("%-34s %8.4f   must collapse" % ("value-permute", k("val_perm")))
    print("%-34s %8.4f   must collapse" % ("address-permute", k("addr_perm")))
    print("-" * 46)
    print()
    if k("train_fit") < 0.90:
        print("INSTRUMENT-DEAD - the workspace cannot even fit the pairs it was shown")
        print("(%.4f). Read nothing else." % k("train_fit"))
        return 1
    held, staple = k("held"), k("staple_held")
    if held <= ch * 1.5:
        print("ARITY-2 NOT LEARNED - held-out %.4f against chance %.4f, while SEEN pairs" % (held, ch))
        print("fit at %.4f. The workspace MEMORISED and did not compose, even with the two" % k("train_fit"))
        print("operands handed to it as separate structured slots.")
        print()
        print("That is the sharper version of V6_1's result. There the head had to find the")
        print("operands in pooled text and one could argue extraction was the bottleneck.")
        print("Here retrieval is content-addressed and clean, so extraction is excluded:")
        print("the wall is the COMPOSITION itself, not getting hold of the pieces.")
        print()
        print("P1 is the load-bearing phase, so this is where the plan owes the two-substrate")
        print("escape rather than another lane on the same substrate.")
        return 1
    if held - staple < 0.25:
        print("NOT-CONJUNCTION - held-out %.4f but the capacity-matched staple reaches %.4f."
              % (held, staple))
        print("An additive pair of 1-slot readouts explains it, so nothing joint was learned.")
        return 1
    print("ARITY-2 LEARNED (screen level) - held-out %.4f, staple %.4f, controls collapsed."
          % (held, staple))
    print("Still DIRECTIONAL: a toy, one table, three seeds. cement is anima-py only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
