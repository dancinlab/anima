#!/usr/bin/env python3
"""
H_9276 / F4 — ROS retrograde signal: tonic->structure channel, or does it collapse into urgency(phasic->emit)?

$0 numpy probe. mini CPU-local. Deterministic, 5 seeds.

DESIGN (pre-declared BEFORE running; constants are NOT re-tuned after seeing results)
=====================================================================================
Substrate = an organelle pool (n alive units, each with health h_i in [H_MIN,1]).
A non-stationary demand d_t must be served by the pool's capacity cap_t = sum_i C_UNIT*h_i.
Overload damages health; spare capacity repairs it.
  ROS_i = load_i / capacity_i          (stress = load relative to health-discounted capacity)
  ROS_t = mean_i ROS_i                 (aggregate retrograde signal)
  R_t   = EMA(ROS_t, TONIC_ALPHA)      (TONIC — slow)

STRUCTURE LANE (slow, one event every STRUCT_EVERY steps; biogenesis vs pruning):
  g = P(grow) at each structural tick. Exactly ONE structural event per tick in EVERY arm
  (grow if u<g else prune-weakest), and the u-stream is COMMON RANDOM NUMBERS shared by all
  arms -> the structural budget is *identical* across arms by construction; only the
  *information* driving g differs. Same controller, same param count, same compute.

    EXP  : g = sigmoid(SG * z_causal(R_t))            <- ROS -> structure  (the hypothesis)
    c0   : g = const = mean(g_EXP)                    <- static rate, budget-matched, no retrograde
    c1   : g = permutation of the g_EXP sequence      <- shuffled ROS (random retrograde), EXACT same
                                                          multiset of growth pressures, wrong timing
    ORCL : g from true instantaneous shortfall        <- reference CEILING (not a control)

  STRUCTURE METRIC (fitness) = mean_t [ served_t - LAMBDA * n_t ]   (capacity costs rent;
  matching capacity to a moving demand is the only way to win). Also: corr(n_t, d_t) = sigma-flux
  tracking.

EMIT LANE (fast):
  The substrate runs an online predictor of the demand.  A starved substrate makes a NOISIER
  prediction:  predhat_t = pred_t + N(0, S0*(1 + BETA*shortfall_frac_t)).
  err_t = |d_{t+1} - predhat_t| ;  y_t = 1 iff err_t is in the top EMIT_Q of the run  ("real tension").
  ** This deliberately gives ROS a REAL CHANCE at the emit lane: substrate shortfall genuinely
     raises prediction error, and R_t tracks shortfall. If ROS carried emit-relevant information,
     this design would find it. **
  Emit gate arms (logistic, fit on 1st half, AUC + precision@rate on held-out 2nd half):
    E0     : score from [urgency]              urgency u_t = |d_t - d_{t-1}|   (phasic; the ONLY proven channel)
    c2     : score from [urgency, R_t]         <- VIOLATION ARM: ROS routed into emit  (a_substrate_disjoint)
    c2s    : score from [urgency, shuffle(R)]  <- negative control, same #features/budget as c2
    c2r    : score from [R_t] alone            <- can ROS drive emit at all?
  DeltaEff = AUC(c2) - AUC(E0).  c2 has MORE capacity (1 extra feature) than E0, so DeltaEff ~ 0
  despite the extra feature is a strong no-op result.
  Run on BOTH the EXP trajectory AND the c0 trajectory (honesty check: in the static world the
  structure lane does NOT consume the stress, so ROS should have MORE emit-relevant residual there
  if it has any at all).

PASS (card): structure Delta > 0  AND  fast-emit DeltaEff ~ 0  AND  c1 gain vanishes.
FAIL: structure Delta ~ 0, or ROS indistinguishable from / overlapping the urgency channel.

p5: no arm hardcodes an emit gate. The emit decision is a learned score over substrate signals;
the experimental arm never touches it at all.
"""
import json
import os
import numpy as np

# ---------------- pre-declared constants (frozen) ----------------
T = 3000            # steps
BURN = 300          # excluded from metrics
M_MAX = 48
M_MIN = 4
N0 = 12
C_UNIT = 1.0
H_MIN = 0.2
K_DAM = 0.05        # health damage per unit overload
K_REP = 0.02        # health repair per unit spare
TONIC_ALPHA = 0.02  # tonic EMA (slow) for R_t
Z_ALPHA = 0.01      # causal z-score EMA
SG = 2.0            # sigmoid gain of the structure controller
STRUCT_EVERY = 10   # one structural event per 10 steps
LAMBDA = 0.4        # maintenance rent per alive organelle per step
ETA = 0.30          # predictor learning rate
S0 = 1.0            # base predictor noise
BETA = 1.0          # PRIMARY: how much substrate shortfall degrades the prediction
EMIT_Q = 0.80       # top-20% error = "real tension" = emit-warranted
THETA_ABS = 1.0     # SECONDARY lens: absolute stress setpoint. ROS_i = load/cap_i, so ROS==1.0 means
                    # load EXACTLY equals capacity -> this threshold is DERIVED, not fitted. Single
                    # value, no sweep. (The PRIMARY z-score arm is reported regardless of what this does.)
SEEDS = [0, 1, 2, 3, 4]
GD_ITERS = 500
GD_LR = 0.2
BETA_GRID = [0.0, 1.0, 3.0]   # pre-declared sensitivity grid (secondary, reported in full)

OUT = os.path.dirname(os.path.abspath(__file__))


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -50, 50)))


def make_demand(rng):
    """slow non-stationary drift + fast phasic spikes."""
    w = rng.standard_normal(T)
    slow = np.zeros(T)
    acc = 0.0
    for t in range(T):
        acc = 0.985 * acc + w[t]
        slow[t] = acc
    slow = (slow - slow.mean()) / (slow.std() + 1e-9)
    d = 16.0 + 6.0 * slow                      # slow band
    d += 0.8 * rng.standard_normal(T)          # fast jitter
    spike_at = rng.random(T) < 0.03            # phasic events
    d = d + spike_at * rng.uniform(4.0, 10.0, T)
    return np.clip(d, 3.0, None)


def run_sim(seed, mode, g_ext=None, beta=BETA):
    """mode in {exp, ext, oracle}. ext = open-loop g sequence supplied (c0/c1)."""
    rng_env = np.random.default_rng(seed)
    rng_str = np.random.default_rng(10_000 + seed)   # COMMON random numbers across arms
    d = make_demand(rng_env)
    n_ticks = T // STRUCT_EVERY + 2
    u_stream = rng_str.random(n_ticks)               # identical for every arm of this seed
    pnoise = rng_env.standard_normal(T)              # identical predictor-noise draw

    h = np.ones(M_MAX)
    alive = np.zeros(M_MAX, dtype=bool)
    alive[:N0] = True

    ema_mu = None
    ema_var = 1.0
    R = 0.0

    pred = d[0]
    rec = {k: np.zeros(T) for k in
           ("d", "cap", "n", "served", "ros", "R", "sf", "err", "urg")}
    g_log = []
    n_add = n_prune = 0

    for t in range(T):
        idx = np.where(alive)[0]
        n = idx.size
        cap_i = C_UNIT * h[idx]
        cap = cap_i.sum()
        load = d[t] / n
        served = min(d[t], cap)
        sf = max(0.0, d[t] - cap) / d[t]

        ros_i = load / (cap_i + 1e-6)
        ros = float(np.clip(ros_i.mean(), 0.0, 10.0))
        R = ros if t == 0 else (1 - TONIC_ALPHA) * R + TONIC_ALPHA * ros

        # health dynamics
        over = np.maximum(0.0, load - cap_i)
        spare = np.maximum(0.0, cap_i - load)
        h[idx] = np.clip(h[idx] - K_DAM * over + K_REP * spare, H_MIN, 1.0)

        # emit-lane ground truth: a starved substrate predicts worse
        predhat = pred + pnoise[t] * S0 * (1.0 + beta * sf)
        nxt = d[t + 1] if t + 1 < T else d[t]
        err = abs(nxt - predhat)
        pred = pred + ETA * (d[t] - pred)

        rec["d"][t], rec["cap"][t], rec["n"][t] = d[t], cap, n
        rec["served"][t], rec["ros"][t], rec["R"][t] = served, ros, R
        rec["sf"][t], rec["err"][t] = sf, err
        rec["urg"][t] = abs(d[t] - d[t - 1]) if t > 0 else 0.0

        # causal z of the tonic retrograde signal
        if ema_mu is None:
            ema_mu = R
        ema_mu = (1 - Z_ALPHA) * ema_mu + Z_ALPHA * R
        ema_var = (1 - Z_ALPHA) * ema_var + Z_ALPHA * (R - ema_mu) ** 2
        z = (R - ema_mu) / (np.sqrt(ema_var) + 1e-6)

        # ---- STRUCTURE LANE (slow) : exactly one event per tick, every arm ----
        if t > 0 and t % STRUCT_EVERY == 0:
            k = t // STRUCT_EVERY
            if mode == "exp":
                g = float(sigmoid(SG * z))
            elif mode == "exp_abs":
                # SECONDARY: absolute tonic setpoint (ROS==1 <=> load==capacity). Same controller,
                # same param count, same one-event-per-tick budget; only the reference frame differs.
                g = float(sigmoid(SG * (R - THETA_ABS)))
            elif mode == "ext":
                g = float(g_ext[k % len(g_ext)])
            elif mode == "oracle":
                g = 1.0 if cap < 1.05 * d[t] else 0.0
            else:
                raise ValueError(mode)
            g_log.append(g)
            if u_stream[k] < g:
                if n < M_MAX:                       # biogenesis
                    dead = np.where(~alive)[0][0]
                    alive[dead] = True
                    h[dead] = 1.0
                    n_add += 1
            else:
                if n > M_MIN:                       # prune the weakest (mitophagy-like)
                    w = idx[np.argmin(h[idx])]
                    alive[w] = False
                    n_prune += 1

    rec["g_log"] = np.array(g_log)
    rec["n_add"], rec["n_prune"] = n_add, n_prune
    return rec


def fitness(rec):
    s = slice(BURN, T)
    return float(np.mean(rec["served"][s] - LAMBDA * rec["n"][s]))


def auc(y, s):
    y = np.asarray(y).astype(int)
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s), float)
    ranks[order] = np.arange(1, len(s) + 1)
    # average ranks for ties
    su = np.sort(s)
    i = 0
    while i < len(su):
        j = i
        while j + 1 < len(su) and su[j + 1] == su[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + j + 2) / 2.0
        i = j + 1
    npos, nneg = y.sum(), (1 - y).sum()
    if npos == 0 or nneg == 0:
        return float("nan")
    return float((ranks[y == 1].sum() - npos * (npos + 1) / 2.0) / (npos * nneg))


def logistic_holdout(X, y):
    """identical fitting budget for every arm; fit on 1st half, score held-out 2nd half."""
    n = len(y)
    half = n // 2
    Xtr, ytr = X[:half], y[:half]
    Xte, yte = X[half:], y[half:]
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    Xtr = (Xtr - mu) / sd
    Xte = (Xte - mu) / sd
    Xtr = np.hstack([Xtr, np.ones((len(Xtr), 1))])
    Xte = np.hstack([Xte, np.ones((len(Xte), 1))])
    w = np.zeros(Xtr.shape[1])
    for _ in range(GD_ITERS):
        p = sigmoid(Xtr @ w)
        w -= GD_LR * (Xtr.T @ (p - ytr)) / len(ytr)
    s = Xte @ w
    a = auc(yte, s)
    # precision @ matched emit rate (top 1-EMIT_Q of scores) = "Eff"
    k = max(1, int(round((1 - EMIT_Q) * len(s))))
    top = np.argsort(-s)[:k]
    prec = float(yte[top].mean())
    return a, prec


def emit_eval(rec, rng):
    s = slice(BURN, T)
    urg = rec["urg"][s]
    R = rec["R"][s]
    err = rec["err"][s]
    y = (err >= np.quantile(err, EMIT_Q)).astype(int)
    Rs = rng.permutation(R)
    arms = {
        "E0_urgency":       np.stack([urg], 1),
        "c2_urg_plus_ros":  np.stack([urg, R], 1),
        "c2s_urg_plus_shuf": np.stack([urg, Rs], 1),
        "c2r_ros_only":     np.stack([R], 1),
    }
    out = {}
    for k, X in arms.items():
        a, p = logistic_holdout(X, y)
        out[k] = {"auc": a, "prec": p}
    out["_corr_R_shortfall"] = float(np.corrcoef(R, rec["sf"][s])[0, 1])
    out["_corr_urg_err"] = float(np.corrcoef(urg, err)[0, 1])
    return out


def one_seed(seed, beta=BETA):
    exp = run_sim(seed, "exp", beta=beta)
    g_exp = exp["g_log"]
    rngp = np.random.default_rng(777 + seed)
    g_shuf = rngp.permutation(g_exp)                  # c1: shuffled retrograde, EXACT same multiset
    g_const = np.full_like(g_exp, float(g_exp.mean()))  # c0: static rate, budget-matched
    c0 = run_sim(seed, "ext", g_ext=g_const, beta=beta)
    c1 = run_sim(seed, "ext", g_ext=g_shuf, beta=beta)
    orc = run_sim(seed, "oracle", beta=beta)

    s = slice(BURN, T)
    res = {"seed": seed, "beta": beta, "structure": {}, "emit_on_exp": {}, "emit_on_c0": {}}
    for name, r in (("EXP_ros", exp), ("c0_static", c0), ("c1_shuffled", c1), ("ORACLE", orc)):
        res["structure"][name] = {
            "fitness": fitness(r),
            "mean_n": float(np.mean(r["n"][s])),
            "mean_served": float(np.mean(r["served"][s])),
            "mean_shortfall_frac": float(np.mean(r["sf"][s])),
            "corr_n_d": float(np.corrcoef(r["n"][s], r["d"][s])[0, 1]),
            "mean_health_ros": float(np.mean(r["ros"][s])),
            "n_add": int(r["n_add"]), "n_prune": int(r["n_prune"]),
            "n_struct_events": int(r["n_add"] + r["n_prune"]),
        }
    res["emit_on_exp"] = emit_eval(exp, np.random.default_rng(555 + seed))
    res["emit_on_c0"] = emit_eval(c0, np.random.default_rng(555 + seed))
    return res


def one_seed_abs(seed, beta=BETA):
    """SECONDARY lens: identical protocol, absolute-setpoint retrograde wiring."""
    exp = run_sim(seed, "exp_abs", beta=beta)
    g_exp = exp["g_log"]
    rngp = np.random.default_rng(777 + seed)
    g_shuf = rngp.permutation(g_exp)
    g_const = np.full_like(g_exp, float(g_exp.mean()))
    c0 = run_sim(seed, "ext", g_ext=g_const, beta=beta)
    c1 = run_sim(seed, "ext", g_ext=g_shuf, beta=beta)
    orc = run_sim(seed, "oracle", beta=beta)
    s = slice(BURN, T)
    res = {"seed": seed, "structure": {}}
    for name, r in (("EXPabs_ros", exp), ("c0_static", c0), ("c1_shuffled", c1), ("ORACLE", orc)):
        res["structure"][name] = {
            "fitness": fitness(r),
            "mean_n": float(np.mean(r["n"][s])),
            "mean_served": float(np.mean(r["served"][s])),
            "mean_shortfall_frac": float(np.mean(r["sf"][s])),
            "corr_n_d": float(np.corrcoef(r["n"][s], r["d"][s])[0, 1]),
            "n_add": int(r["n_add"]), "n_prune": int(r["n_prune"]),
            "n_struct_events": int(r["n_add"] + r["n_prune"]),
        }
    res["emit_on_expabs"] = emit_eval(exp, np.random.default_rng(555 + seed))
    return res


def agg(vals):
    v = np.asarray(vals, float)
    return {"mean": float(v.mean()), "std": float(v.std(ddof=1)) if len(v) > 1 else 0.0,
            "per_seed": [float(x) for x in v]}


def main():
    out = {"config": {k: v for k, v in globals().items()
                      if k.isupper() and isinstance(v, (int, float, list))},
           "primary": {}, "sensitivity_beta": {}}

    # -------- PRIMARY (BETA = 1.0) --------
    seeds_res = [one_seed(s) for s in SEEDS]
    out["primary"]["per_seed_raw"] = seeds_res

    arms = ["EXP_ros", "c0_static", "c1_shuffled", "ORACLE"]
    st = {a: agg([r["structure"][a]["fitness"] for r in seeds_res]) for a in arms}
    out["primary"]["structure_fitness"] = st
    out["primary"]["structure_budget_check"] = {
        a: {"mean_n": agg([r["structure"][a]["mean_n"] for r in seeds_res]),
            "n_struct_events": agg([r["structure"][a]["n_struct_events"] for r in seeds_res]),
            "n_add": agg([r["structure"][a]["n_add"] for r in seeds_res]),
            "corr_n_d": agg([r["structure"][a]["corr_n_d"] for r in seeds_res]),
            "mean_shortfall_frac": agg([r["structure"][a]["mean_shortfall_frac"] for r in seeds_res])}
        for a in arms}
    # paired deltas
    out["primary"]["structure_delta"] = {
        "EXP_minus_c0_static": agg([r["structure"]["EXP_ros"]["fitness"] - r["structure"]["c0_static"]["fitness"]
                                    for r in seeds_res]),
        "EXP_minus_c1_shuffled": agg([r["structure"]["EXP_ros"]["fitness"] - r["structure"]["c1_shuffled"]["fitness"]
                                      for r in seeds_res]),
        "c1_minus_c0": agg([r["structure"]["c1_shuffled"]["fitness"] - r["structure"]["c0_static"]["fitness"]
                            for r in seeds_res]),
        "ORACLE_minus_c0": agg([r["structure"]["ORACLE"]["fitness"] - r["structure"]["c0_static"]["fitness"]
                                for r in seeds_res]),
    }

    for traj in ("emit_on_exp", "emit_on_c0"):
        e = {}
        for k in ("E0_urgency", "c2_urg_plus_ros", "c2s_urg_plus_shuf", "c2r_ros_only"):
            e[k] = {"auc": agg([r[traj][k]["auc"] for r in seeds_res]),
                    "prec": agg([r[traj][k]["prec"] for r in seeds_res])}
        e["delta_auc_c2_minus_E0"] = agg([r[traj]["c2_urg_plus_ros"]["auc"] - r[traj]["E0_urgency"]["auc"]
                                          for r in seeds_res])
        e["delta_prec_c2_minus_E0"] = agg([r[traj]["c2_urg_plus_ros"]["prec"] - r[traj]["E0_urgency"]["prec"]
                                           for r in seeds_res])
        e["delta_auc_c2s_minus_E0"] = agg([r[traj]["c2s_urg_plus_shuf"]["auc"] - r[traj]["E0_urgency"]["auc"]
                                           for r in seeds_res])
        e["corr_R_shortfall"] = agg([r[traj]["_corr_R_shortfall"] for r in seeds_res])
        e["corr_urg_err"] = agg([r[traj]["_corr_urg_err"] for r in seeds_res])
        out["primary"][traj] = e

    # -------- SECONDARY LENS: absolute-setpoint retrograde wiring --------
    ab = [one_seed_abs(s) for s in SEEDS]
    arms_ab = ["EXPabs_ros", "c0_static", "c1_shuffled", "ORACLE"]
    out["secondary_abs_setpoint"] = {
        "per_seed_raw": ab,
        "structure_fitness": {a: agg([r["structure"][a]["fitness"] for r in ab]) for a in arms_ab},
        "budget_check": {a: {"mean_n": agg([r["structure"][a]["mean_n"] for r in ab]),
                             "n_struct_events": agg([r["structure"][a]["n_struct_events"] for r in ab]),
                             "n_add": agg([r["structure"][a]["n_add"] for r in ab]),
                             "corr_n_d": agg([r["structure"][a]["corr_n_d"] for r in ab]),
                             "mean_shortfall_frac": agg([r["structure"][a]["mean_shortfall_frac"] for r in ab])}
                         for a in arms_ab},
        "structure_delta": {
            "EXPabs_minus_c0": agg([r["structure"]["EXPabs_ros"]["fitness"] - r["structure"]["c0_static"]["fitness"] for r in ab]),
            "EXPabs_minus_c1": agg([r["structure"]["EXPabs_ros"]["fitness"] - r["structure"]["c1_shuffled"]["fitness"] for r in ab]),
            "c1_minus_c0": agg([r["structure"]["c1_shuffled"]["fitness"] - r["structure"]["c0_static"]["fitness"] for r in ab]),
            "ORACLE_minus_EXPabs": agg([r["structure"]["ORACLE"]["fitness"] - r["structure"]["EXPabs_ros"]["fitness"] for r in ab]),
        },
        "emit_on_expabs": {
            "E0_urgency_auc": agg([r["emit_on_expabs"]["E0_urgency"]["auc"] for r in ab]),
            "c2_urg_plus_ros_auc": agg([r["emit_on_expabs"]["c2_urg_plus_ros"]["auc"] for r in ab]),
            "c2r_ros_only_auc": agg([r["emit_on_expabs"]["c2r_ros_only"]["auc"] for r in ab]),
            "delta_auc_c2_minus_E0": agg([r["emit_on_expabs"]["c2_urg_plus_ros"]["auc"]
                                          - r["emit_on_expabs"]["E0_urgency"]["auc"] for r in ab]),
            "delta_auc_c2s_minus_E0": agg([r["emit_on_expabs"]["c2s_urg_plus_shuf"]["auc"]
                                           - r["emit_on_expabs"]["E0_urgency"]["auc"] for r in ab]),
            "delta_prec_c2_minus_E0": agg([r["emit_on_expabs"]["c2_urg_plus_ros"]["prec"]
                                           - r["emit_on_expabs"]["E0_urgency"]["prec"] for r in ab]),
        },
    }

    # -------- SENSITIVITY over pre-declared BETA grid --------
    for b in BETA_GRID:
        rs = [one_seed(s, beta=b) for s in SEEDS]
        out["sensitivity_beta"][str(b)] = {
            "structure_delta_EXP_minus_c0": agg([r["structure"]["EXP_ros"]["fitness"]
                                                 - r["structure"]["c0_static"]["fitness"] for r in rs]),
            "structure_delta_EXP_minus_c1": agg([r["structure"]["EXP_ros"]["fitness"]
                                                 - r["structure"]["c1_shuffled"]["fitness"] for r in rs]),
            "emit_on_exp_delta_auc": agg([r["emit_on_exp"]["c2_urg_plus_ros"]["auc"]
                                          - r["emit_on_exp"]["E0_urgency"]["auc"] for r in rs]),
            "emit_on_c0_delta_auc": agg([r["emit_on_c0"]["c2_urg_plus_ros"]["auc"]
                                         - r["emit_on_c0"]["E0_urgency"]["auc"] for r in rs]),
            "emit_on_c0_ros_only_auc": agg([r["emit_on_c0"]["c2r_ros_only"]["auc"] for r in rs]),
            "emit_on_exp_ros_only_auc": agg([r["emit_on_exp"]["c2r_ros_only"]["auc"] for r in rs]),
        }

    with open(os.path.join(OUT, "result.json"), "w") as f:
        json.dump(out, f, indent=2)

    # -------- console summary --------
    p = out["primary"]
    print("=" * 78)
    print("H_9276 / F4 — ROS retrograde  (5 seeds, BETA=%.1f primary)" % BETA)
    print("=" * 78)
    print("\n[STRUCTURE LANE]  fitness = mean(served - %.2f*n)   (higher = better)" % LAMBDA)
    for a in arms:
        b = out["primary"]["structure_budget_check"][a]
        print("  %-12s fit=%8.4f +- %.4f | mean_n=%5.2f | events=%4.0f | adds=%4.0f | corr(n,d)=%+.3f | shortfall=%.4f"
              % (a, st[a]["mean"], st[a]["std"], b["mean_n"]["mean"], b["n_struct_events"]["mean"],
                 b["n_add"]["mean"], b["corr_n_d"]["mean"], b["mean_shortfall_frac"]["mean"]))
    for k, v in p["structure_delta"].items():
        print("  Delta %-22s = %+8.4f +- %.4f   per-seed %s"
              % (k, v["mean"], v["std"], ["%+.3f" % x for x in v["per_seed"]]))

    for traj in ("emit_on_exp", "emit_on_c0"):
        e = p[traj]
        print("\n[EMIT LANE / %s]   held-out AUC (emit-warranted = top-20%% real tension)" % traj)
        for k in ("E0_urgency", "c2_urg_plus_ros", "c2s_urg_plus_shuf", "c2r_ros_only"):
            print("  %-20s AUC=%.4f +- %.4f | prec@20%%=%.4f" %
                  (k, e[k]["auc"]["mean"], e[k]["auc"]["std"], e[k]["prec"]["mean"]))
        print("  DeltaEff(AUC)  c2 - E0 = %+.4f +- %.4f  per-seed %s"
              % (e["delta_auc_c2_minus_E0"]["mean"], e["delta_auc_c2_minus_E0"]["std"],
                 ["%+.4f" % x for x in e["delta_auc_c2_minus_E0"]["per_seed"]]))
        print("  DeltaEff(prec) c2 - E0 = %+.4f +- %.4f" %
              (e["delta_prec_c2_minus_E0"]["mean"], e["delta_prec_c2_minus_E0"]["std"]))
        print("  (shuf ctrl) c2s - E0   = %+.4f +- %.4f" %
              (e["delta_auc_c2s_minus_E0"]["mean"], e["delta_auc_c2s_minus_E0"]["std"]))
        print("  corr(R, shortfall)=%+.3f | corr(urgency, err)=%+.3f"
              % (e["corr_R_shortfall"]["mean"], e["corr_urg_err"]["mean"]))

    sec = out["secondary_abs_setpoint"]
    print("\n" + "-" * 78)
    print("[SECONDARY LENS] absolute tonic setpoint (THETA=%.1f  <=>  load==capacity)" % THETA_ABS)
    for a in arms_ab:
        f = sec["structure_fitness"][a]
        b = sec["budget_check"][a]
        print("  %-12s fit=%8.4f +- %.4f | mean_n=%5.2f | events=%4.0f | adds=%4.0f | corr(n,d)=%+.3f | shortfall=%.4f"
              % (a, f["mean"], f["std"], b["mean_n"]["mean"], b["n_struct_events"]["mean"],
                 b["n_add"]["mean"], b["corr_n_d"]["mean"], b["mean_shortfall_frac"]["mean"]))
    for k, v in sec["structure_delta"].items():
        print("  Delta %-20s = %+8.4f +- %.4f   per-seed %s"
              % (k, v["mean"], v["std"], ["%+.3f" % x for x in v["per_seed"]]))
    e = sec["emit_on_expabs"]
    print("  [emit on EXPabs traj] E0=%.4f  c2=%.4f  ROS-only=%.4f  DeltaEff(AUC)=%+.4f +- %.4f  (shuf ctrl %+.4f)"
          % (e["E0_urgency_auc"]["mean"], e["c2_urg_plus_ros_auc"]["mean"], e["c2r_ros_only_auc"]["mean"],
             e["delta_auc_c2_minus_E0"]["mean"], e["delta_auc_c2_minus_E0"]["std"],
             e["delta_auc_c2s_minus_E0"]["mean"]))

    print("\n[SENSITIVITY — pre-declared BETA grid]")
    for b in BETA_GRID:
        s2 = out["sensitivity_beta"][str(b)]
        print("  BETA=%.1f  struct D(exp-c0)=%+.3f  D(exp-c1)=%+.3f | emitD(exp traj)=%+.4f  emitD(c0 traj)=%+.4f | ROS-only AUC exp=%.3f c0=%.3f"
              % (b, s2["structure_delta_EXP_minus_c0"]["mean"], s2["structure_delta_EXP_minus_c1"]["mean"],
                 s2["emit_on_exp_delta_auc"]["mean"], s2["emit_on_c0_delta_auc"]["mean"],
                 s2["emit_on_exp_ros_only_auc"]["mean"], s2["emit_on_c0_ros_only_auc"]["mean"]))
    print("\nwrote result.json")


if __name__ == "__main__":
    main()
