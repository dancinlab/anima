#!/usr/bin/env python3
"""
H_9278 / F6 — ORGANELLE LANE: capacity pressure -> trained conjunction?

Question (card 3):  Does a HARD active-unit cap (ATP-set sparsity) force a
trained-conjunction code on a combination-demanding corpus, WITHOUT any
synthetic XBIND supervision pointing at the conjunction?

Substrate wiring (p5-clean):
  ATP -> phenotype capacity ONLY = hard top-k mask on the hidden (phenotype)
  layer. It never touches an emit gate; there is no emit gate in this probe.
  The cap is an ARCHITECTURAL constraint on which units may fire, applied
  identically at train and eval. No loss term, no label, no hand-written
  conjunction feature.

Task (combination-demanding, conjunction NOT supervised):
  tokens a (nA), b (nB), nuisance c (nC).
  hidden latents:  pol(a), pol(b) in {0,1};  topic(a) in {0..3}
  label y = 4*XOR(pol(a),pol(b)) + topic(a)          (8 classes)
    - topic component  = ADDITIVE (main-effect of a alone) -> free, generalizes
    - parity component = NON-ADDITIVE joint of a,b -> the G1 recombination bit
      (main-effect ceiling is exactly chance = 0.5, marginals balanced)
  Training sees only SEEN (a,b) pairs. Held-out pairs are NEVER seen together,
  though every a and every b is seen (with other partners). So the only route
  to held-out parity is: infer pol per token, apply the joint rule.
  Memorizing seen pairs fits train perfectly and yields held-out parity = 0.5.
  => held-out conj_acc separates trained-conjunction from memorize/additive.

ARMS (all identical budget: same H=64 hidden units, same param count, same
      steps, same optimizer, same corpus size, same seeds; ONLY k / corpus differ)
  EXP  : tight cap (k small)  x  combinatorial corpus
  C1   : dense / no cap (k=H) x  combinatorial corpus     [same-metric control]
  C2   : tight cap            x  NON-combinatorial corpus (label ignores b)
  C3   : tight cap            x  shuffled-parity corpus   [memorization control,
                                 held-out parity unpredictable by construction]
  Full k-sweep k in {1,2,4,8,16,32,64} for every corpus -> monotonicity test.
  LIVENESS (V1): oracle arm gets the true parity bit as an input feature under
  the tight cap -> must reach held-out conj_acc ~1.0, proving the harness and
  the capped architecture CAN express/read the conjunction. Plus train-acc.

PASS  : held-out conj_acc rises monotonically as the cap tightens, ONLY in the
        (tight x combinatorial) cell; C1 flat at floor, C2/C3 flat.
FAIL  : additive/memorization floor (conj_acc ~ 0.5) at every cap level.

$0 numpy, CPU-local, deterministic, 5 seeds. No torch.
"""
import json
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------- config (FROZEN before any run; no tune-to-green) ----------
NA, NB, NC = 16, 16, 8
N_TOPIC = 4
N_CLASS = 8               # 4 topics x 2 parity
HELD_FRAC = 0.30
REPS_TRAIN = 6            # nuisance-c draws per seen pair
REPS_EVAL = 4
H = 64                    # hidden (phenotype) units -- SAME for every arm
EPOCHS = 2000
LR = 1e-2
KS = [1, 2, 4, 8, 16, 32, 64]     # 64 == dense == no cap
TIGHT_K = 2
SEEDS = [0, 1, 2, 3, 4]
CORPORA = ["comb", "noncomb", "shuf"]


# ---------------- corpus ----------------------------------------------------
def make_world(rng):
    pol_a = np.concatenate([np.zeros(NA // 2, int), np.ones(NA // 2, int)])
    rng.shuffle(pol_a)
    pol_b = np.concatenate([np.zeros(NB // 2, int), np.ones(NB // 2, int)])
    rng.shuffle(pol_b)
    topic_a = np.tile(np.arange(N_TOPIC), NA // N_TOPIC)
    rng.shuffle(topic_a)
    return pol_a, pol_b, topic_a


def split_pairs(rng, held_frac=HELD_FRAC):
    """held-out pairs never co-occur in training; every a and every b IS seen
    (with other partners) -> the only route to a held-out pair is a joint rule.
    Constructive design: give every a and every b >=2 train partners (a latin-ish
    backbone), then fill the rest at random up to the seen budget."""
    n_seen = len(range(NA * NB)) - int(round(held_frac * NA * NB))
    grid = np.zeros((NA, NB), dtype=bool)
    for _ in range(2):                       # 2 backbone passes: row & column cover
        for i in range(NA):
            grid[i, rng.integers(0, NB)] = True
        for j in range(NB):
            grid[rng.integers(0, NA), j] = True
    need = n_seen - int(grid.sum())
    if need > 0:
        free = np.argwhere(~grid)
        pick = rng.permutation(len(free))[:need]
        for i, j in free[pick]:
            grid[i, j] = True
    elif need < 0:                            # backbone alone exceeds budget
        on = np.argwhere(grid)
        drop = rng.permutation(len(on))[:(-need)]
        # never drop below 1 partner per token
        for i, j in on[drop]:
            if grid[i].sum() > 1 and grid[:, j].sum() > 1:
                grid[i, j] = False
    seen = np.argwhere(grid)
    held = np.argwhere(~grid)
    return seen, held


def labels_for(pairs, corpus, world, shuf_bits):
    pol_a, pol_b, topic_a = world
    a, b = pairs[:, 0], pairs[:, 1]
    if corpus == "comb":
        par = pol_a[a] ^ pol_b[b]
    elif corpus == "noncomb":
        par = pol_a[a]                       # label ignores b entirely
    elif corpus == "shuf":
        par = shuf_bits[a, b]                # random bit per pair: no joint rule
    else:
        raise ValueError(corpus)
    return 4 * par + topic_a[a], par


def build(rng, corpus, oracle=False, held_frac=HELD_FRAC):
    world = make_world(rng)
    shuf_bits = rng.integers(0, 2, size=(NA, NB))
    seen, held = split_pairs(rng, held_frac)

    def mat(pairs, reps):
        P = np.repeat(pairs, reps, axis=0)
        cs = rng.integers(0, NC, size=len(P))
        dim = NA + NB + NC + (1 if oracle else 0)
        X = np.zeros((len(P), dim), dtype=np.float64)
        X[np.arange(len(P)), P[:, 0]] = 1.0
        X[np.arange(len(P)), NA + P[:, 1]] = 1.0
        X[np.arange(len(P)), NA + NB + cs] = 1.0
        y, par = labels_for(P, corpus, world, shuf_bits)
        if oracle:
            X[:, -1] = par.astype(np.float64)   # V1 liveness: hand the bit over
        return X, y, par, P

    Xtr, ytr, partr, Ptr = mat(seen, REPS_TRAIN)
    Xte, yte, parte, Pte = mat(held, REPS_EVAL)
    return dict(Xtr=Xtr, ytr=ytr, partr=partr, Xte=Xte, yte=yte, parte=parte,
                world=world, seen=seen, held=held, Pte=Pte)


# ---------------- model: 1 hidden layer, ReLU, HARD top-k cap ---------------
def topk_mask(Hh, k):
    if k >= Hh.shape[1]:
        return np.ones_like(Hh)
    idx = np.argpartition(-Hh, k - 1, axis=1)[:, :k]
    M = np.zeros_like(Hh)
    np.put_along_axis(M, idx, 1.0, axis=1)
    return M


def forward(X, W1, b1, W2, b2, k):
    Z = X @ W1 + b1
    A = np.maximum(Z, 0.0)
    M = topk_mask(A, k)          # ATP cap: only k units may be phenotypically active
    Ak = A * M
    logits = Ak @ W2 + b2
    return Z, A, M, Ak, logits


def softmax(z):
    z = z - z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


def train(d, k, seed, epochs=EPOCHS, lr=LR):
    rng = np.random.default_rng(10_000 + seed)
    din = d["Xtr"].shape[1]
    W1 = rng.normal(0, 1.0 / np.sqrt(din), (din, H))
    b1 = np.zeros(H)
    W2 = rng.normal(0, 1.0 / np.sqrt(H), (H, N_CLASS))
    b2 = np.zeros(N_CLASS)
    params = [W1, b1, W2, b2]
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    b1a, b2a, eps = 0.9, 0.999, 1e-8

    X, y = d["Xtr"], d["ytr"]
    n = len(X)
    Y = np.zeros((n, N_CLASS))
    Y[np.arange(n), y] = 1.0

    for t in range(1, epochs + 1):
        Z, A, M, Ak, logits = forward(X, W1, b1, W2, b2, k)
        P = softmax(logits)
        dlog = (P - Y) / n
        gW2 = Ak.T @ dlog
        gb2 = dlog.sum(0)
        dAk = dlog @ W2.T
        dZ = dAk * M * (Z > 0)          # straight-through the frozen top-k mask
        gW1 = X.T @ dZ
        gb1 = dZ.sum(0)
        for i, g in enumerate([gW1, gb1, gW2, gb2]):
            m[i] = b1a * m[i] + (1 - b1a) * g
            v[i] = b2a * v[i] + (1 - b2a) * g * g
            mh = m[i] / (1 - b1a ** t)
            vh = v[i] / (1 - b2a ** t)
            params[i] -= lr * mh / (np.sqrt(vh) + eps)
        W1, b1, W2, b2 = params
    return params


def evaluate(d, params, k):
    W1, b1, W2, b2 = params
    out = {}
    for tag, X, y, par in (("train", d["Xtr"], d["ytr"], d["partr"]),
                           ("held", d["Xte"], d["yte"], d["parte"])):
        _, _, _, _, logits = forward(X, W1, b1, W2, b2, k)
        pred = logits.argmax(1)
        out[f"{tag}_acc"] = float((pred == y).mean())
        out[f"{tag}_conj_acc"] = float(((pred // 4) == par).mean())
        out[f"{tag}_add_acc"] = float(((pred % 4) == (y % 4)).mean())
    return out


def conj_index(d, params, k):
    """Non-additive energy fraction of the phenotype code over the (a,b) grid.
    h(a,b) ~ mu + u_a + v_b  (two-way ANOVA);  index = ||resid||^2 / ||h-mu||^2.
    0 = purely additive code, 1 = purely conjunctive."""
    W1, b1, W2, b2 = params
    din = W1.shape[0]
    X = np.zeros((NA * NB, din))
    r = 0
    for i in range(NA):
        for j in range(NB):
            X[r, i] = 1.0
            X[r, NA + j] = 1.0
            r += 1
    X[:, NA + NB:NA + NB + NC] = 1.0 / NC        # marginalize the nuisance slot
    _, _, _, Ak, _ = forward(X, W1, b1, W2, b2, k)
    Hgrid = Ak.reshape(NA, NB, -1)
    mu = Hgrid.mean((0, 1), keepdims=True)
    ua = Hgrid.mean(1, keepdims=True) - mu
    vb = Hgrid.mean(0, keepdims=True) - mu
    resid = Hgrid - (mu + ua + vb)
    tot = ((Hgrid - mu) ** 2).sum()
    return float((resid ** 2).sum() / tot) if tot > 1e-12 else 0.0


# ---------------- stage 2: STEELMAN — does the cap rescue a FLOORED model? ---
# Stage 1's dense arm turned out to already generalize (no additive floor to
# rescue), so the "cap lifts a floored model" cell was untestable there.
# Stage 2 sweeps pair-coverage DOWN (a-priori grid, not a hunt) into the
# memorization-dominant regime where the dense model DOES floor, and re-asks the
# same question with the same >=2 controls. Both regimes are reported; stage 1
# stays the primary pre-registered cell. Every arm keeps the identical budget.
COV_HELD_FRACS = [0.30, 0.50, 0.65, 0.80]   # held-out fraction (0.80 = 20% seen)
COV_KS = [1, 2, 4, 64]                      # 64 = dense = no cap (C1)


def stage2():
    t0 = time.time()
    rows = []
    for hf in COV_HELD_FRACS:
        for corpus in ("comb", "shuf"):      # comb + memorization control
            for k in COV_KS:
                for s in SEEDS:
                    d = build(np.random.default_rng(s), corpus, held_frac=hf)
                    p = train(d, k, s)
                    r = evaluate(d, p, k)
                    r.update(corpus=corpus, k=k, seed=s, held_frac=hf,
                             n_seen_pairs=int(len(d["seen"])),
                             conj_index=conj_index(d, p, k))
                    rows.append(r)
        print(f"[{time.time()-t0:6.1f}s] held_frac={hf} done", flush=True)

    summ, table = {}, []
    for hf in COV_HELD_FRACS:
        for corpus in ("comb", "shuf"):
            for k in COV_KS:
                sel = [r for r in rows if r["held_frac"] == hf
                       and r["corpus"] == corpus and r["k"] == k]
                key = f"{corpus}|hf{hf}|k{k}"
                summ[key] = {m: dict(mean=float(np.mean([r[m] for r in sel])),
                                     std=float(np.std([r[m] for r in sel])))
                             for m in ("train_acc", "held_acc", "held_conj_acc",
                                       "conj_index")}
        dense = summ[f"comb|hf{hf}|k64"]["held_conj_acc"]["mean"]
        best_cap = max(summ[f"comb|hf{hf}|k{k}"]["held_conj_acc"]["mean"]
                       for k in COV_KS if k < 64)
        table.append(dict(held_frac=hf,
                          n_seen_pairs=summ and [r["n_seen_pairs"] for r in rows
                                                 if r["held_frac"] == hf][0],
                          dense_c1=dense,
                          tight_k2=summ[f"comb|hf{hf}|k2"]["held_conj_acc"]["mean"],
                          best_capped=best_cap,
                          delta_bestcap_minus_dense=best_cap - dense,
                          shuf_c3_k2=summ[f"shuf|hf{hf}|k2"]["held_conj_acc"]["mean"],
                          dense_floored=bool(dense < 0.65)))
    rescue = [t for t in table if t["dense_floored"]
              and t["delta_bestcap_minus_dense"] > 0.05]
    verdict2 = dict(coverage_table=table,
                    any_floored_regime=bool([t for t in table if t["dense_floored"]]),
                    cap_rescues_floored_regime=bool(rescue),
                    max_delta_over_dense=max(t["delta_bestcap_minus_dense"]
                                             for t in table))
    path = os.path.join(OUT, "result.json")
    res = json.load(open(path))
    res["stage2_coverage_steelman"] = dict(config=dict(
        COV_HELD_FRACS=COV_HELD_FRACS, COV_KS=COV_KS, SEEDS=SEEDS),
        rows=rows, summary=summ, verdict=verdict2,
        wall_sec=round(time.time() - t0, 1))
    with open(path, "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(verdict2, indent=1))


# ---------------- run -------------------------------------------------------
def main():
    t0 = time.time()
    rows = []
    for corpus in CORPORA:
        for k in KS:
            for s in SEEDS:
                d = build(np.random.default_rng(s), corpus)
                p = train(d, k, s)
                r = evaluate(d, p, k)
                r.update(corpus=corpus, k=k, seed=s,
                         conj_index=conj_index(d, p, k))
                rows.append(r)
                print(f"[{time.time()-t0:6.1f}s] {corpus:8s} k={k:2d} s={s} "
                      f"train={r['train_acc']:.3f} held={r['held_acc']:.3f} "
                      f"conj={r['held_conj_acc']:.3f} ci={r['conj_index']:.3f}",
                      flush=True)

    # V1 liveness: capped architecture WITH the parity bit handed to it
    live = []
    for s in SEEDS:
        d = build(np.random.default_rng(s), "comb", oracle=True)
        p = train(d, TIGHT_K, s)
        r = evaluate(d, p, TIGHT_K)
        r.update(corpus="oracle_comb", k=TIGHT_K, seed=s, conj_index=float("nan"))
        live.append(r)
        print(f"[liveness] oracle k={TIGHT_K} s={s} held_conj="
              f"{r['held_conj_acc']:.3f} held={r['held_acc']:.3f}", flush=True)

    def agg(sel, key):
        v = np.array([r[key] for r in sel])
        return float(v.mean()), float(v.std())

    summary = {}
    for corpus in CORPORA:
        for k in KS:
            sel = [r for r in rows if r["corpus"] == corpus and r["k"] == k]
            summary[f"{corpus}|k{k}"] = {
                m: dict(zip(("mean", "std"), agg(sel, m)))
                for m in ("train_acc", "held_acc", "held_conj_acc",
                          "held_add_acc", "train_conj_acc", "conj_index")
            }
    summary["oracle_comb|k%d" % TIGHT_K] = {
        m: dict(zip(("mean", "std"), agg(live, m)))
        for m in ("train_acc", "held_acc", "held_conj_acc", "held_add_acc",
                  "train_conj_acc")
    }

    # --- decisive numbers -------------------------------------------------
    exp = summary[f"comb|k{TIGHT_K}"]["held_conj_acc"]["mean"]
    c1 = summary["comb|k64"]["held_conj_acc"]["mean"]          # dense, same corpus
    c2 = summary[f"noncomb|k{TIGHT_K}"]["held_conj_acc"]["mean"]
    c3 = summary[f"shuf|k{TIGHT_K}"]["held_conj_acc"]["mean"]
    best_tight = max(summary[f"comb|k{k}"]["held_conj_acc"]["mean"]
                     for k in KS if k <= 8)
    curve = [summary[f"comb|k{k}"]["held_conj_acc"]["mean"] for k in KS]
    # monotone rise as cap TIGHTENS = curve decreasing in k
    mono = all(curve[i] >= curve[i + 1] - 1e-9 for i in range(len(curve) - 1))
    delta_vs_max_control = exp - max(c1, c3, 0.5)

    verdict = dict(
        exp_held_conj_acc=exp,
        c1_dense_same_corpus=c1,
        c2_tight_noncomb=c2,
        c3_tight_shuffled=c3,
        chance=0.5,
        delta_exp_minus_max_control=delta_vs_max_control,
        best_tight_cell=best_tight,
        cap_curve_k=KS,
        cap_curve_held_conj=curve,
        monotone_rise_as_cap_tightens=bool(mono),
        liveness_oracle_held_conj=summary[f"oracle_comb|k{TIGHT_K}"]["held_conj_acc"]["mean"],
    )
    res = dict(config=dict(NA=NA, NB=NB, NC=NC, H=H, EPOCHS=EPOCHS, LR=LR,
                           KS=KS, TIGHT_K=TIGHT_K, SEEDS=SEEDS,
                           HELD_FRAC=HELD_FRAC, n_train=int(REPS_TRAIN),
                           budget_note="identical H/params/steps/data across all arms; only k and corpus vary"),
               rows=rows, liveness=live, summary=summary, verdict=verdict,
               wall_sec=round(time.time() - t0, 1))
    with open(os.path.join(OUT, "result.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(verdict, indent=1))
    print("wall", res["wall_sec"], "s")


if __name__ == "__main__":
    if "--stage2" in sys.argv:
        sys.exit(stage2())
    sys.exit(main())
