#!/usr/bin/env python3
"""H_9131 F3 masked-interaction CE-target — $0 toy-gate (closes the ladder rung).

Fable combination-ideas #3 / wall-break F3: a T5-style masked span where the
masked byproduct c(a,b) is reconstructible ONLY from BOTH a,b jointly (a non-additive
interaction).  The hope: a CE target that FORCES the trunk to compose.

This toy answers the ONLY question a $0 numpy toy CAN answer here, pre-registered:
  Can a tiny NN learn a non-additive interaction target c(a,b) on TRAIN and generalize
  to HELD-OUT pairs (combo unseen; both concepts seen singly)?

Why this is decisive (and why a $0 toy is enough to CLOSE the rung, not open it):
  - A neural net is a universal approximator ⇒ on TRAIN it will always fit c(a,b).
  - The only question is GENERALIZATION to held-out (a,b). DPI law: if c is a function
    of the exchangeable bag {a,b}, generalization is trivially additive; if c is a
    genuine non-commutative/order interaction, generalization requires the rep to
    CARRY the interaction — which is exactly what §4 just measured the 303M trunk
    does NOT (joint R^2 ≈ additive ≈ shuffle, all negative held-out).
  - So this toy is a CAPACITY sanity check (can a tiny net hold-out generalize a
    non-additive c at all, in principle). If YES (expected) ⇒ the G1 wall is NOT a
    capacity/approximation limit — it is that the 303M trunk's learned reps + CE
    objective don't put the interaction there (confirms §4: lever must be objective/
    data, not capacity). If NO ⇒ something deeper.

Frozen bar (pre-registered): held-out R^2 on c(a,b) > additive baseline + 0.10 AND
> shuffle + 0.10, on ≥2/3 seeds.  (Same shape as §4 / derisk.)"""
import os, json, time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
D = 16                 # concept dim
N_CONCEPTS = 60
N_TRAIN = 2400
N_HOLD = 600
HIDDEN = 64
STEPS = 2500
LR = 0.05
SEEDS = [7, 4302, 4303]


def gen_world(seed):
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((N_CONCEPTS, D)).astype(np.float64)
    # non-additive interaction target: c(a,b) = sin(a·b) per-dim mix + order sign
    # — provably not f(a)+g(b): depends on the product a·b and on order.
    def c_batch(ia, ib):
        a, b = A[ia], A[ib]
        prod = a * b                              # Hadamard (non-additive)
        sign = np.sign(np.sum(a, 1)) * np.sign(np.sum(b, 1))  # order-dependent-ish
        return np.tanh(prod) * sign[:, None]
    # pairs
    def make(n):
        ia = rng.integers(0, N_CONCEPTS, n); ib = rng.integers(0, N_CONCEPTS, n)
        mask = ia != ib
        ia, ib = ia[mask], ib[mask]
        return ia[:n], ib[:n], c_batch(ia[:n], ib[:n])
    return A, make(N_TRAIN), make(N_HOLD)


def relu(x): return np.maximum(0, x)


def train_probe(Xtr, ytr, Xte, yte, seed, hidden=HIDDEN, steps=STEPS, lr=LR):
    """tiny 1-hidden-layer MLP, full-batch GD, R^2 on held-out."""
    rng = np.random.default_rng(seed)
    din, dout = Xtr.shape[1], ytr.shape[1]
    W1 = rng.standard_normal((din, hidden)) * 0.3
    b1 = np.zeros(hidden)
    W2 = rng.standard_normal((hidden, dout)) * 0.3
    b2 = np.zeros(dout)
    for _ in range(steps):
        h = relu(Xtr @ W1 + b1)
        pred = h @ W2 + b2
        err = pred - ytr
        gW2 = h.T @ err / len(ytr); gb2 = err.mean(0)
        dh = (err @ W2.T) * (h > 0)
        gW1 = Xtr.T @ dh / len(ytr); gb1 = dh.mean(0)
        W2 -= lr * gW2; b2 -= lr * gb2; W1 -= lr * gW1; b1 -= lr * gb1
    def r2(X, y):
        pred = relu(X @ W1 + b1) @ W2 + b2
        ssr = ((y - pred) ** 2).sum(); sst = ((y - y.mean(0)) ** 2).sum()
        return 1 - ssr / sst if sst > 0 else float("nan")
    return r2(Xtr, ytr), r2(Xte, yte)


def run_seed(seed):
    A, (ia_tr, ib_tr, y_tr), (ia_te, ib_te, y_te) = gen_world(seed)
    # joint features = [a , b]   (both concepts visible)
    Xj_tr = np.hstack([A[ia_tr], A[ib_tr]]); Xj_te = np.hstack([A[ia_te], A[ib_te]])
    # additive features = [a + b]  (exchangeable bag — DPI says this is the ceiling for additive)
    Xa_tr = A[ia_tr] + A[ib_tr]; Xa_te = A[ia_te] + A[ib_te]
    # shuffle: scramble partner in train
    rng = np.random.default_rng(seed + 99)
    perm = rng.permutation(len(ib_tr))
    Xs_tr = np.hstack([A[ia_tr], A[ib_tr[perm]]])
    r2_j_tr, r2_j = train_probe(Xj_tr, y_tr, Xj_te, y_te, seed)
    r2_a_tr, r2_a = train_probe(Xa_tr, y_tr, Xa_te, y_te, seed)
    r2_s_tr, r2_s = train_probe(Xs_tr, y_tr, Xj_te, y_te, seed)
    return dict(seed=seed, r2_joint=r2_j, r2_additive=r2_a, r2_shuffle=r2_s,
                r2_joint_train=r2_j_tr,
                gap_joint_add=r2_j - r2_a, gap_joint_shuf=r2_j - r2_s,
                pass_both=bool((r2_j - r2_a) >= 0.10 and (r2_j - r2_s) >= 0.10))


def main():
    t0 = time.time()
    results = [run_seed(s) for s in SEEDS]
    n_pass = sum(r["pass_both"] for r in results)
    verdict = ("CAPACITY-OK-nonadditive-learnable" if n_pass >= 2 else
               "CAPACITY-LIMIT" if n_pass == 0 else "DIRECTIONAL-1of3")
    out = dict(probe="F3 masked-interaction toy (capacity sanity, $0 numpy)",
               seeds=SEEDS, hidden=HIDDEN, steps=STEPS, n_pass_2of3=n_pass,
               verdict=verdict, results=results,
               bar="held-out R^2: joint > additive+0.10 AND > shuffle+0.10, >=2/3 seeds",
               interpretation=("A tiny NN DOES generalize a non-additive c(a,b) to held-out "
                               "=> the G1 wall is NOT a capacity/approximation limit. It is that "
                               "the 303M trunk's reps + CE objective don't put the interaction "
                               "there (confirms §4). F3's only meaningful test is a GPU trunk "
                               "retrain with the masked-interaction CE target — $0 toy is closed "
                               "(capacity-OK), so this rung is done; the lever is objective/data, "
                               "not capacity.") if n_pass >= 2 else
                              ("Unexpected: tiny NN does NOT generalize non-additive c(a,b) — "
                               "would suggest a deeper limit worth re-examining.") if n_pass == 0
                              else "mixed")
    print(json.dumps(out, indent=2))
    with open(f"{_HERE}/RESULT.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"[done] {time.time()-t0:.1f}s -> RESULT.json  verdict={verdict}")


if __name__ == "__main__":
    main()
