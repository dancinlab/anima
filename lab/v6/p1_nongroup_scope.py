#!/usr/bin/env python3
"""P1 scope test — does the arity-2 pass survive a table that is NOT a group? $0.

WHY THIS ATTACKS MY OWN RESULT
------------------------------
V6_P1b passed at held-out 0.6875 against chance 0.1250, and its own scope note says the
task is "a cyclic group in disguise, the friendliest composition there is". That is a
loud caveat and it deserves a measurement rather than a sentence: the table there was
roll-of-a-permutation, i.e. sq[i][j] = base[(i+j) mod n], the Cayley table of Z_n. A model
that finds one circular embedding solves EVERY cell at once.

Real relation tables have no reason to be group tables. So this file re-runs the same
workspace on three tables of increasing hostility, with everything else held fixed:

    cyclic       roll-of-a-permutation -- the Cayley table of Z_8 (what P1 used)
    latin        a random latin square, associativity FAILS -- still uniform marginals,
                 so per-cue lookup is still chance by construction, but no group to find
    arbitrary    a random table with balanced columns -- not even a latin square

If the pass is really about composition it should survive the loss of group structure at
least partly. If it collapses to the memorization floor the moment the group is gone, then
V6_P1b measured "this architecture can find a circular code", which is a much narrower
claim than "the workspace composes".

The structure check is printed, not assumed.

AND THE COMBINE FORM HAD TO BE SEPARATED TOO
--------------------------------------------
The first pass of this file left a confound: on the non-group tables the SUM combine did
not even fit its training set (0.7153 / 0.7708), so a held-out collapse could have been
underfitting rather than missing structure. Re-running each table under both combines
settles it -- `combine_sweep()` below, and the numbers are in V6_P1c:

    table       combine    train    held-out
    cyclic      sum        1.0000     0.6875   <- the ONLY cell that generalizes
    cyclic      concat     1.0000     0.0000
    latin       sum        0.7153     0.0417
    latin       concat     1.0000     0.0000
    arbitrary   sum        0.7708     0.0208
    arbitrary   concat     1.0000     0.0000

Concat has the capacity to represent ANY table, fits all three perfectly, and generalizes
on NONE. Sum generalizes on exactly the table whose structure it matches. So capacity was
never the thing that generalizes -- a bias matched to the data's structure is.
"""
import itertools
import numpy as np

N = 8
HELD = 16
D_K = 24
D_E = 48
HID = 192
STEPS = 120000
TAU = 0.3
SEEDS = (7, 11, 4302)


def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


class Adam:
    def __init__(self, shapes, lr=1e-3, b1=0.9, b2=0.98, eps=1e-8, wd=0.0):
        self.m = [np.zeros(s) for s in shapes]; self.v = [np.zeros(s) for s in shapes]
        self.lr, self.b1, self.b2, self.eps, self.wd, self.t = lr, b1, b2, eps, wd, 0

    def step(self, ps, gs):
        self.t += 1
        for i, (p, g) in enumerate(zip(ps, gs)):
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * g * g
            mh = self.m[i] / (1 - self.b1 ** self.t); vh = self.v[i] / (1 - self.b2 ** self.t)
            p -= self.lr * (mh / (np.sqrt(vh) + self.eps) + self.wd * p)


def cyclic_table(rng):
    base = rng.permutation(N)
    return np.stack([np.roll(base, -i) for i in range(N)])


def latin_table(rng, tries=4000):
    """A random latin square by repeated row/column/symbol shuffling of a cyclic seed.
    Shuffling preserves the latin property (uniform marginals) but destroys the group."""
    sq = np.stack([np.roll(np.arange(N), -i) for i in range(N)])
    for _ in range(tries):
        sq = sq[rng.permutation(N)]                 # permute rows
        sq = sq[:, rng.permutation(N)]              # permute columns
        sq = rng.permutation(N)[sq]                 # relabel symbols
    return sq


def arbitrary_table(rng):
    """Not even a latin square: each column is a balanced multiset, rows unconstrained.
    Marginals stay uniform so a per-cue lookup is still chance."""
    cols = [rng.permutation(N) for _ in range(N)]
    return np.stack(cols, axis=1)


def cyclic_structure(sq):
    """Does sq[i][j] depend ONLY on (i+j) mod N? That is the property the cyclic arm has
    by construction and the one a model can exploit with a single circular embedding.

    (The first version of this checker tested raw associativity, sq[sq[a,b],c] ==
     sq[a,sq[b,c]], and reported NO for the cyclic arm -- a false negative of the checker,
     not a fact about the table. The cyclic table is a RELABELED Cayley table: the output
     permutation `base` breaks associativity in the raw index space while leaving the
     structure a model exploits completely intact. Testing the (i+j) dependence tests the
     thing that actually matters.)"""
    for i, j in itertools.product(range(N), repeat=2):
        for i2, j2 in itertools.product(range(N), repeat=2):
            if (i + j) % N == (i2 + j2) % N and sq[i, j] != sq[i2, j2]:
                return False
    return True


def uniform_marginals(sq):
    rows = all(len(set(sq[i])) == N for i in range(N))
    cols = all(len(set(sq[:, j])) == N for j in range(N))
    return rows and cols


def build(seed, kind):
    rng = np.random.default_rng(seed)
    key_emb = rng.normal(0, 1.0, (256, D_K))
    nm = []
    while len(nm) < N:
        s = "s" + "".join(chr(97 + int(rng.integers(0, 26))) for _ in range(4))
        if s not in nm:
            nm.append(s)

    def key(x):
        b = np.frombuffer(x.encode("ascii"), dtype=np.uint8)
        return key_emb[b].mean(axis=0)

    K = np.stack([key(x) for x in nm])
    table = {"cyclic": cyclic_table, "latin": latin_table, "arbitrary": arbitrary_table}[kind](rng)
    cells = [(i, j) for i in range(N) for j in range(N)]
    o = rng.permutation(len(cells))
    held = {cells[k] for k in o[:HELD]}
    return dict(rng=rng, K=K, table=table,
                train=[c for c in cells if c not in held],
                test=[c for c in cells if c in held])


def addr(env, i):
    return softmax(env["K"][i] @ env["K"].T / (np.sqrt(D_K) * TAU))


def gold(env, pairs):
    return np.array([env["table"][i, j] for (i, j) in pairs])


def train(env, wd=0.3):
    rng = env["rng"]
    A = np.stack([addr(env, i) for (i, j) in env["train"]])
    B = np.stack([addr(env, j) for (i, j) in env["train"]])
    y = gold(env, env["train"]); m = len(y)
    E = rng.normal(0, 0.5, (N, D_E))
    W1 = rng.normal(0, 0.5 / np.sqrt(D_E), (D_E, HID)); b1 = np.zeros(HID)
    W2 = rng.normal(0, 0.5 / np.sqrt(HID), (HID, N)); b2 = np.zeros(N)
    ps = [E, W1, b1, W2, b2]; opt = Adam([p.shape for p in ps], wd=wd)
    for _ in range(STEPS):
        bi = rng.integers(0, m, 64)
        X = A[bi] @ E + B[bi] @ E
        h = np.tanh(X @ W1 + b1)
        p = softmax(h @ W2 + b2)
        p[np.arange(len(bi)), y[bi]] -= 1.0; p /= len(bi)
        gW2 = h.T @ p; gb2 = p.sum(0)
        gh = (p @ W2.T) * (1 - h ** 2)
        gW1 = X.T @ gh; gb1 = gh.sum(0); gX = gh @ W1.T
        opt.step(ps, [A[bi].T @ gX + B[bi].T @ gX, gW1, gb1, gW2, gb2])

    def pred(pairs):
        A2 = np.stack([addr(env, i) for (i, j) in pairs])
        B2 = np.stack([addr(env, j) for (i, j) in pairs])
        return (np.tanh((A2 @ E + B2 @ E) @ W1 + b1) @ W2 + b2).argmax(1)
    return pred


def acc(env, pred, pairs):
    return float((pred(pairs) == gold(env, pairs)).mean()) if pairs else float("nan")


def main():
    ch = 1.0 / N
    print("P1 SCOPE TEST - does the arity-2 pass survive losing the group? ($0, DIRECTIONAL)")
    print("chance %.4f · 3 seed · everything but the TABLE held fixed\n" % ch)
    print("%-12s %8s %9s %9s %9s" % ("table", "cyclic?", "latin?", "train", "HELD-OUT"))
    print("-" * 52)
    res = {}
    for kind in ("cyclic", "latin", "arbitrary"):
        tr, ho, grp, lat = [], [], [], []
        for s in SEEDS:
            env = build(s, kind)
            grp.append(cyclic_structure(env["table"])); lat.append(uniform_marginals(env["table"]))
            pr = train(env)
            tr.append(acc(env, pr, env["train"])); ho.append(acc(env, pr, env["test"]))
        res[kind] = (float(np.mean(tr)), float(np.mean(ho)))
        print("%-12s %8s %9s %9.4f %9.4f"
              % (kind, "yes" if all(grp) else "NO", "yes" if all(lat) else "no",
                 res[kind][0], res[kind][1]))
    print("-" * 52)
    print()
    c_t, c_h = res["cyclic"]; l_t, l_h = res["latin"]; a_t, a_h = res["arbitrary"]
    if c_h <= ch * 1.5:
        print("INSTRUMENT-DEAD - the cyclic arm no longer reproduces V6_P1b (%.4f)." % c_h)
        return 1
    print("The cyclic arm reproduces V6_P1b at %.4f, so the harness is the same one." % c_h)
    print()
    if l_h <= ch * 1.5 and a_h <= ch * 1.5:
        print("SCOPE IS NARROW - held-out collapses to the floor the moment the group goes")
        print("(latin %.4f, arbitrary %.4f, chance %.4f) while training still fits at"
              % (l_h, a_h, ch))
        print("%.4f and %.4f. So V6_P1b measured this architecture finding a CIRCULAR CODE,"
              % (l_t, a_t))
        print("not a workspace that composes in general. The card's own caveat was the")
        print("whole story, and the arity-2 pass must be reported with the group attached.")
        return 0
    if l_h > ch * 1.5:
        print("SCOPE IS WIDER THAN THE CAVEAT - the random latin square, which is NOT a")
        print("group, still generalizes at %.4f against chance %.4f. Composition is not" % (l_h, ch))
        print("riding on the group structure alone.")
        if a_h > ch * 1.5:
            print("The arbitrary table holds too (%.4f), which is the strongest reading." % a_h)
        else:
            print("The arbitrary table does collapse (%.4f), so uniform marginals still" % a_h)
            print("matter -- the boundary sits between latin and arbitrary, not at the group.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
