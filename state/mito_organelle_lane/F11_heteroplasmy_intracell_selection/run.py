#!/usr/bin/env python3
"""
H_9283 / F11 — ORGANELLE LANE: heteroplasmy + intracellular selection
    "does a gradient-free evolutionary inner loop find a conjunctive config
     that CE (gradient) does not?"

SUBSTRATE WIRING (p5-clean, structurally):
  A third lane, DISJOINT from decode/emit and from the cell-pool mitosis lane.
  Each cell carries a POPULATION of M organelles (heteroplasmy). Organelle i
  owns an mtDNA genome g_i in R^H = a gradient-free RESPIRATION/ROUTING config:
      p_i = sigmoid(g_i)  = per-phenotype-unit powering propensity.
  The cell's operational config = heteroplasmy-weighted consensus u = sum_i w_i g_i.
  ATP intervenes ONLY at phenotype formation: which hidden units may fire
      S = relu(XW1+b1) * sigmoid(u);   M = hard top-k(S);   code = S * M
  There is NO emit gate anywhere in this probe. ATP never reaches an emit/silence
  decision (p5). The genome is NEVER touched by a gradient (G-flavored, reverse,
  gradient-free); the trunk (W1,W2 = the nucleus / A lane) is the ONLY thing CE
  touches. The two lanes meet only through the mask.

SELECTION (the F11 mechanism):
  Each generation, every organelle's own genome is scored, the mixture is tilted
  by a replicator step (clonal expansion of the fit / mitophagy of the unfit),
  then a multinomial BOTTLENECK resamples M offspring with mutation (drift).
  The fitness signal is the ONLY thing that differs between arms.

  fitness_eff (EXPERIMENT, label-free / CE-free / p7-safe):
      throughput  T = mean pairwise L2 distance between per-(a,b)-pair codes
      ATP cost    C = mean powered-active mass sum_h code_h
      eff = T / C          <- scale-invariant, so selection acts on ROUTING
                              (which units respire), not on gain inflation.
      No label, no CE, ever touches this number.

ARMS (identical budget: same M, generations, gradient epochs, mutation rate,
      bottleneck, trunk init, genome init, corpus, seeds; EVERY arm computes ALL
      THREE fitness quantities every generation — the ONLY difference is which
      one drives the replicator. Byte-for-byte equal flops.)
  exp        : selection on ATP-efficiency               <- the hypothesis
  c1_drift   : NO selection (f=0) -> drift + mutation only     [control 1, card c1]
  c2_ce      : selection on -CE(train)  Goodhart control       [control 2, card c2]
  c3_shuf    : selection on a PERMUTATION of the eff values    [control 3]
               -> identical selection INTENSITY, signal destroyed (ARM-SHOCK)
  oracle     : selection on held-out conj acc (train-on-test)  [V1 LIVENESS, not an arm]
  ref_dense  : no cap (k=H), frozen genome                     [ceiling REFERENCE, not a control]

TASK (F6-shared, combination-demanding, conjunction NOT supervised):
  y = 4*XOR(pol(a),pol(b)) + topic(a), 8 classes.
    topic = additive main effect of a  -> generalizes for free
    parity = non-additive joint of a,b -> the G1 recombination bit (chance = 0.5)
  Held-out (a,b) pairs NEVER co-occur in training (every a and every b IS seen
  with other partners) => memorizing pairs gives held-out parity = 0.5 exactly.

OPERATING POINT (FROZEN A PRIORI, from F6's measured cap curve — NOT tuned):
  K = 2. F6 measured held-out conj at k=64 (dense) = 0.977 and at k=2 = 0.785.
  k=2 is therefore the cap where the ATP constraint actually BINDS and real
  headroom exists (0.785 -> 0.977). Running at k>=8 would be a ceiling-effect
  degenerate test. One operating point, chosen before any F11 run, no sweep.

PRE-REGISTERED VERDICT RULE (frozen before the first run; no tune-to-green):
  earned metric = HELD-OUT accuracy (BIND). self-metric = eff (FORM, tunable,
  Goodhart-vulnerable by construction: exp selects on it, so a Delta there is
  near-tautological and can NEVER be the verdict).
  PASS(reach)  : held_acc(exp) - max(c1,c2,c3) > 0.02 AND mean+-std disjoint
  PASS(conj)   : held_conj(exp) - max(c1,c2,c3) > 0.05 AND held_conj(exp) > 0.55
  THEATER      : eff Delta > 0 (selection mechanically works) but the earned
                 Deltas are ~0 (< 0.02)  -> selection is bookkeeping.
  KILL         : exp <= controls on the earned metrics.
  INVALID      : oracle (V1) also floors -> the routing search space cannot
                 express the conjunction; the conj sub-claim is unmeasurable here.

$0 numpy, CPU-local, deterministic, 5 seeds. No torch.
"""
import json
import os
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------- config (FROZEN before any run) ----------------------------
NA, NB, NC = 16, 16, 8
N_TOPIC = 4
N_CLASS = 8
HELD_FRAC = 0.30
REPS_TRAIN = 4
REPS_EVAL = 4

H = 64                 # phenotype units (same for every arm)
K = 2                  # hard ATP cap -- frozen a priori (see header)
M_ORG = 24             # organelles per cell (heteroplasmy population)
GENS = 10              # generations (cell lifetime ticks)
EPOCHS_PER_GEN = 100   # trunk CE epochs per generation -> 1000 total, all arms
LR = 1e-2
SIGMA = 0.35           # mtDNA mutation sd
BETA = 4.0             # selection strength on z-scored fitness
                       # (z-scoring => IDENTICAL selection intensity across
                       #  every fitness type; only the SIGNAL differs)
N_FIT = 512            # rows of the train batch used for the CE fitness
SEEDS = [0, 1, 2, 3, 4]

ARMS = ["exp", "c1_drift", "c2_ce", "c3_shuf", "oracle", "ref_dense"]
CONTROLS = ["c1_drift", "c2_ce", "c3_shuf"]


# ---------------- corpus (shared with F6) -----------------------------------
def make_world(rng):
    pol_a = np.concatenate([np.zeros(NA // 2, int), np.ones(NA // 2, int)])
    rng.shuffle(pol_a)
    pol_b = np.concatenate([np.zeros(NB // 2, int), np.ones(NB // 2, int)])
    rng.shuffle(pol_b)
    topic_a = np.tile(np.arange(N_TOPIC), NA // N_TOPIC)
    rng.shuffle(topic_a)
    return pol_a, pol_b, topic_a


def split_pairs(rng):
    n_seen = NA * NB - int(round(HELD_FRAC * NA * NB))
    grid = np.zeros((NA, NB), dtype=bool)
    for _ in range(2):
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
    elif need < 0:
        on = np.argwhere(grid)
        for i, j in on[rng.permutation(len(on))[:(-need)]]:
            if grid[i].sum() > 1 and grid[:, j].sum() > 1:
                grid[i, j] = False
    return np.argwhere(grid), np.argwhere(~grid)


DIN = NA + NB + NC


def encode(pairs, cs):
    X = np.zeros((len(pairs), DIN))
    X[np.arange(len(pairs)), pairs[:, 0]] = 1.0
    X[np.arange(len(pairs)), NA + pairs[:, 1]] = 1.0
    X[np.arange(len(pairs)), NA + NB + cs] = 1.0
    return X


def probe_rows(pairs):
    """nuisance marginalized -> deterministic per-pair probe row."""
    X = np.zeros((len(pairs), DIN))
    X[np.arange(len(pairs)), pairs[:, 0]] = 1.0
    X[np.arange(len(pairs)), NA + pairs[:, 1]] = 1.0
    X[:, NA + NB:] = 1.0 / NC
    return X


def build(seed):
    rng = np.random.default_rng(1234 + seed)
    world = make_world(rng)
    pol_a, pol_b, topic_a = world
    seen, held = split_pairs(rng)

    def mat(pairs, reps):
        P = np.repeat(pairs, reps, axis=0)
        cs = rng.integers(0, NC, size=len(P))
        X = encode(P, cs)
        par = pol_a[P[:, 0]] ^ pol_b[P[:, 1]]
        y = 4 * par + topic_a[P[:, 0]]
        return X, y, par

    Xtr, ytr, partr = mat(seen, REPS_TRAIN)
    Xte, yte, parte = mat(held, REPS_EVAL)

    grid = np.array([[i, j] for i in range(NA) for j in range(NB)])
    d = dict(
        Xtr=Xtr, ytr=ytr, partr=partr, Xte=Xte, yte=yte, parte=parte,
        seen=seen, held=held, world=world,
        Pseen=probe_rows(seen),                       # label-free throughput probe
        Pheld=probe_rows(held),                       # oracle-fitness probe (V1 only)
        par_held=pol_a[held[:, 0]] ^ pol_b[held[:, 1]],
        y_held=4 * (pol_a[held[:, 0]] ^ pol_b[held[:, 1]]) + topic_a[held[:, 0]],
        Xgrid=probe_rows(grid),
    )
    fit_rng = np.random.default_rng(777 + seed)
    d["fit_idx"] = fit_rng.permutation(len(Xtr))[:N_FIT]
    # fixed random pair-couples for the throughput metric (same every arm/gen)
    npair = len(seen)
    d["cp"] = fit_rng.integers(0, npair, size=(2, 4000))
    return d


# ---------------- phenotype: ATP-powered hard top-k --------------------------
def topk_mask(S, k):
    if k >= S.shape[1]:
        return np.ones_like(S)
    idx = np.argpartition(-S, k - 1, axis=1)[:, :k]
    Mk = np.zeros_like(S)
    np.put_along_axis(Mk, idx, 1.0, axis=1)
    return Mk


def forward(X, W1, b1, W2, b2, p, k):
    Z = X @ W1 + b1
    A = np.maximum(Z, 0.0)
    S = A * p                       # organelle powering (gradient-free vector)
    Mk = topk_mask(S, k)            # ATP cap: only k units may respire/fire
    code = S * Mk
    logits = code @ W2 + b2
    return Z, A, Mk, code, logits


def softmax(z):
    z = z - z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


# ---------------- the three fitness quantities (all computed, every arm) -----
def fit_eff(d, W1, b1, W2, b2, p, k):
    """ATP-efficiency = throughput / ATP.  LABEL-FREE, CE-FREE (p7-safe)."""
    _, _, _, code, _ = forward(d["Pseen"], W1, b1, W2, b2, p, k)
    i, j = d["cp"]
    T = float(np.linalg.norm(code[i] - code[j], axis=1).mean())   # throughput
    C = float(code.sum(1).mean())                                 # ATP consumed
    return T / (C + 1e-8)


def fit_ce(d, W1, b1, W2, b2, p, k):
    """Goodhart control fitness: -CE on train (USES LABELS)."""
    idx = d["fit_idx"]
    _, _, _, _, logits = forward(d["Xtr"][idx], W1, b1, W2, b2, p, k)
    P = softmax(logits)
    return -float(-np.log(P[np.arange(len(idx)), d["ytr"][idx]] + 1e-12).mean())


def fit_oracle(d, W1, b1, W2, b2, p, k):
    """V1 LIVENESS fitness: held-out conjunction acc (train-on-test, on purpose)."""
    _, _, _, _, logits = forward(d["Pheld"], W1, b1, W2, b2, p, k)
    return float(((logits.argmax(1) // 4) == d["par_held"]).mean())


# ---------------- trunk (A lane): CE / Adam, gradient-free genome ------------
def trunk_epochs(d, params, adam, p, k, epochs, t0):
    W1, b1, W2, b2 = params
    m, v = adam
    X, y = d["Xtr"], d["ytr"]
    n = len(X)
    Y = np.zeros((n, N_CLASS))
    Y[np.arange(n), y] = 1.0
    b1a, b2a, eps = 0.9, 0.999, 1e-8
    t = t0
    for _ in range(epochs):
        t += 1
        Z, A, Mk, code, logits = forward(X, W1, b1, W2, b2, p, k)
        P = softmax(logits)
        dlog = (P - Y) / n
        gW2 = code.T @ dlog
        gb2 = dlog.sum(0)
        dcode = dlog @ W2.T
        dS = dcode * Mk                 # straight-through the frozen top-k mask
        dZ = dS * p * (Z > 0)           # p is a CONSTANT here -> no genome grad
        gW1 = X.T @ dZ
        gb1 = dZ.sum(0)
        for i, g in enumerate([gW1, gb1, gW2, gb2]):
            m[i] = b1a * m[i] + (1 - b1a) * g
            v[i] = b2a * v[i] + (1 - b2a) * g * g
            params[i] -= LR * (m[i] / (1 - b1a ** t)) / (np.sqrt(v[i] / (1 - b2a ** t)) + eps)
        W1, b1, W2, b2 = params
    return params, (m, v), t


# ---------------- evaluation --------------------------------------------------
def evaluate(d, params, p, k):
    W1, b1, W2, b2 = params
    out = {}
    for tag, X, y, par in (("train", d["Xtr"], d["ytr"], d["partr"]),
                           ("held", d["Xte"], d["yte"], d["parte"])):
        _, _, _, _, logits = forward(X, W1, b1, W2, b2, p, k)
        pred = logits.argmax(1)
        out[f"{tag}_acc"] = float((pred == y).mean())
        out[f"{tag}_conj_acc"] = float(((pred // 4) == par).mean())
        out[f"{tag}_add_acc"] = float(((pred % 4) == (y % 4)).mean())
    # non-additive energy fraction of the phenotype code (is the FOUND config
    # conjunctive?  two-way ANOVA over the full (a,b) grid)
    _, _, _, code, _ = forward(d["Xgrid"], W1, b1, W2, b2, p, k)
    hh = code.reshape(NA, NB, -1)
    mu = hh.mean((0, 1), keepdims=True)
    ua = hh.mean(1, keepdims=True) - mu
    vb = hh.mean(0, keepdims=True) - mu
    resid = hh - mu - ua - vb
    tot = float(((hh - mu) ** 2).sum())
    out["conj_index"] = float((resid ** 2).sum() / (tot + 1e-12))
    out["eff"] = fit_eff(d, W1, b1, W2, b2, p, k)
    _, _, _, code_s, _ = forward(d["Pseen"], W1, b1, W2, b2, p, k)
    out["atp"] = float(code_s.sum(1).mean())
    out["n_units_used"] = int((code_s.max(0) > 1e-9).sum())
    return out


# ---------------- one arm ------------------------------------------------------
def run_arm(d, arm, seed):
    k = H if arm == "ref_dense" else K
    # --- identical inits across every arm (same seed) ---
    rng_w = np.random.default_rng(10_000 + seed)
    params = [rng_w.normal(0, 1 / np.sqrt(DIN), (DIN, H)), np.zeros(H),
              rng_w.normal(0, 1 / np.sqrt(H), (H, N_CLASS)), np.zeros(N_CLASS)]
    adam = ([np.zeros_like(q) for q in params], [np.zeros_like(q) for q in params])
    rng_evo = np.random.default_rng(9_000 + seed)      # SAME stream for all arms
    G = rng_evo.normal(0, 1.0, (M_ORG, H))             # heteroplasmy population
    w = np.full(M_ORG, 1.0 / M_ORG)
    u = (w[:, None] * G).sum(0)                        # consensus genome
    t = 0
    traj = []
    for gen in range(GENS):
        p = 1.0 / (1.0 + np.exp(-u))
        params, adam, t = trunk_epochs(d, params, adam, p, k, EPOCHS_PER_GEN, t)
        W1, b1, W2, b2 = params

        # every arm pays for ALL THREE fitness evaluations (equal budget)
        f_eff = np.array([fit_eff(d, W1, b1, W2, b2, 1 / (1 + np.exp(-G[i])), k) for i in range(M_ORG)])
        f_ce = np.array([fit_ce(d, W1, b1, W2, b2, 1 / (1 + np.exp(-G[i])), k) for i in range(M_ORG)])
        f_or = np.array([fit_oracle(d, W1, b1, W2, b2, 1 / (1 + np.exp(-G[i])), k) for i in range(M_ORG)])

        def z(f):
            return (f - f.mean()) / (f.std() + 1e-9)

        perm = rng_evo.permutation(M_ORG)              # drawn for EVERY arm (equal stream)
        if arm == "exp":
            zz = z(f_eff)
        elif arm == "c2_ce":
            zz = z(f_ce)
        elif arm == "c3_shuf":
            zz = z(f_eff)[perm]                        # same intensity, signal destroyed
        elif arm == "oracle":
            zz = z(f_or)
        else:                                          # c1_drift, ref_dense
            zz = np.zeros(M_ORG)

        # replicator: clonal expansion of the efficient / mitophagy of the unfit
        w = np.exp(BETA * zz)
        w /= w.sum()
        u = (w[:, None] * G).sum(0)                    # the living heteroplasmic mixture

        # bottleneck (drift) + mutation -> next organelle generation
        cnt = rng_evo.multinomial(M_ORG, w)
        parents = np.repeat(np.arange(M_ORG), cnt)
        G = G[parents] + SIGMA * rng_evo.normal(0, 1, (M_ORG, H))
        ess = float(1.0 / (w ** 2).sum())              # effective population (heteroplasmy)
        traj.append(dict(gen=gen, eff_mean=float(f_eff.mean()), eff_max=float(f_eff.max()),
                         ce_mean=float(f_ce.mean()), oracle_mean=float(f_or.mean()),
                         ess=ess))
    p = 1.0 / (1.0 + np.exp(-u))
    res = evaluate(d, params, p, k)
    res["ess_final"] = traj[-1]["ess"]
    res["arm"] = arm
    res["seed"] = seed
    res["k"] = k
    res["traj"] = traj
    return res


def main():
    t0 = time.time()
    rows = []
    for seed in SEEDS:
        d = build(seed)
        for arm in ARMS:
            r = run_arm(d, arm, seed)
            rows.append(r)
            print(f"seed{seed} {arm:10s} held_acc={r['held_acc']:.3f} "
                  f"held_conj={r['held_conj_acc']:.3f} held_add={r['held_add_acc']:.3f} "
                  f"train={r['train_acc']:.3f} eff={r['eff']:.4f} "
                  f"conj_idx={r['conj_index']:.3f} ess={r['ess_final']:.1f} "
                  f"[{time.time()-t0:.0f}s]", flush=True)

    def agg(arm, key):
        v = np.array([r[key] for r in rows if r["arm"] == arm])
        return float(v.mean()), float(v.std())

    keys = ["held_acc", "held_conj_acc", "held_add_acc", "train_acc", "train_conj_acc",
            "eff", "atp", "conj_index", "n_units_used", "ess_final"]
    summary = {a: {k: dict(zip(("mean", "std"), agg(a, k))) for k in keys} for a in ARMS}

    def dlt(key):
        e = summary["exp"][key]["mean"]
        best_c = max(summary[c][key]["mean"] for c in CONTROLS)
        arg = max(CONTROLS, key=lambda c: summary[c][key]["mean"])
        return dict(exp=e, best_control=arg, best_control_val=best_c, delta=e - best_c)

    deltas = {k: dlt(k) for k in ["held_acc", "held_conj_acc", "eff", "conj_index"]}

    # ---- pre-registered verdict rule ----
    e_ha, s_ha = summary["exp"]["held_acc"]["mean"], summary["exp"]["held_acc"]["std"]
    c_ha = deltas["held_acc"]["best_control_val"]
    c_ha_std = summary[deltas["held_acc"]["best_control"]]["held_acc"]["std"]
    e_hc, s_hc = summary["exp"]["held_conj_acc"]["mean"], summary["exp"]["held_conj_acc"]["std"]
    c_hc = deltas["held_conj_acc"]["best_control_val"]

    disjoint = (e_ha - s_ha) > (c_ha + c_ha_std)
    pass_reach = (deltas["held_acc"]["delta"] > 0.02) and disjoint
    pass_conj = (deltas["held_conj_acc"]["delta"] > 0.05) and (e_hc > 0.55)
    eff_works = deltas["eff"]["delta"] > 0.0
    oracle_live = summary["oracle"]["held_conj_acc"]["mean"] > (
        summary["c1_drift"]["held_conj_acc"]["mean"] + 0.03)
    earned_flat = abs(deltas["held_acc"]["delta"]) < 0.02 and abs(deltas["held_conj_acc"]["delta"]) < 0.02

    if not oracle_live:
        verdict = "INVALID"
    elif pass_reach and pass_conj:
        verdict = "GREEN"
    elif pass_reach or pass_conj:
        verdict = "DIRECTIONAL-POSITIVE"
    elif eff_works and earned_flat:
        verdict = "THEATER"
    else:
        verdict = "KILL"

    out = dict(
        hypothesis="H_9283", family="F11",
        config=dict(NA=NA, NB=NB, NC=NC, H=H, K=K, M_ORG=M_ORG, GENS=GENS,
                    EPOCHS_PER_GEN=EPOCHS_PER_GEN, LR=LR, SIGMA=SIGMA, BETA=BETA,
                    SEEDS=SEEDS, HELD_FRAC=HELD_FRAC, N_FIT=N_FIT,
                    arms=ARMS, controls=CONTROLS),
        summary=summary, deltas=deltas,
        gates=dict(pass_reach=bool(pass_reach), pass_conj=bool(pass_conj),
                   eff_selection_works=bool(eff_works), oracle_liveness=bool(oracle_live),
                   earned_flat=bool(earned_flat),
                   chance_conj=0.5, chance_acc=0.125),
        verdict=verdict,
        rows=[{k: v for k, v in r.items() if k != "traj"} for r in rows],
        traj_exp_seed0=[r["traj"] for r in rows if r["arm"] == "exp" and r["seed"] == 0][0],
        wall_sec=round(time.time() - t0, 1),
    )
    with open(os.path.join(OUT, "result.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\n=== VERDICT:", verdict, f"({out['wall_sec']}s) ===")
    for k, v in deltas.items():
        print(f"  D {k:15s} exp={v['exp']:.4f}  best_ctrl({v['best_control']})={v['best_control_val']:.4f}"
              f"  delta={v['delta']:+.4f}")
    print(f"  oracle(V1) held_conj = {summary['oracle']['held_conj_acc']['mean']:.3f}")
    print(f"  ref_dense  held_conj = {summary['ref_dense']['held_conj_acc']['mean']:.3f}")


if __name__ == "__main__":
    main()
