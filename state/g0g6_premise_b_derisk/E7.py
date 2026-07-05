#!/usr/bin/env python3
"""E7 -- RECURRENT DELIBERATION STATE (2-4 tick) : premise-(b) forward-COMPUTATION derisk.

$0 numpy structural reachability probe. NO 303M .clm decode (mini OOM ban).
Frozen-first, no tune-to-green, p7. DIRECTIONAL go/no-go for a GPU forward, NOT terminal.

DPI meta-law: next-byte = fn( (a)CE-trained, (b)FEEDFORWARD, (c)single-trunk ).
E7 attacks premise-(b) DIRECTLY: replace the single feedforward pass with a RECURRENT
deliberation loop -- tick 1 emits a PROPOSAL from a, ticks 2..k apply a RELATION
CORRECTION from b (weight-shared fixed recurrent update, random-orthogonal loop). Claim:
iterative refinement (depth) REACHES held-out ordered-pair targets a single pass cannot.

TASK: K random Gaussian atomic concepts in R^d. A combination = ORDERED pair (a,b).
train = subset of ordered pairs; held-out = UNOBSERVED pairs whose BOTH atoms appear in
training (genuine novel-combination-of-seen-atoms = G1 recombination). A frozen TEACHER
maps (a,b)->y*. Each method builds a feature, fits a ridge readout on train, and we
measure HELD-OUT REACH = clamp(R^2,0,1) of the readout on held-out pairs (primary);
top-1 retrieval accuracy is a secondary metric. "unreach" ~ 0 (R^2<=0).

TEACHERS (frozen, method-agnostic, STRONGLY non-additive + order-dependent):
  T_shallow = P.tanh( TGAIN*(Ga.a) (x) (Gb.b) + c )   -- element-wise PRODUCT interaction
              inside one hidden layer (bilinear, order-dep; a LINEAR readout on [a;b]
              CANNOT express the product => linear floors; ONE nonlinear layer suffices).
  T_deep    = depth-3 iterated recurrent teacher with MULTIPLICATIVE state-input coupling
              and DIFFERENT random weights than the student (genuinely needs iterated
              relational refinement -- the premise-(b)-FAVOURABLE regime where recurrence,
              if it is a real lever, MUST show a margin over a single nonlinear pass).

METHODS / CONTROLS (all frozen random weights; only the linear readout is fit):
  additive    : a+b                          (pure bag / order-invariant floor)
  slotlinear  : [a ; b ; a-b]  (LINEAR)      (STRONG total-order additive DPI floor)
  ff1_nonlin  : tanh(Uab[a;b]+c1)            (SINGLE feedforward pass WITH nonlinearity;
                                              no-extra-recurrence control isolating ITERATION)
  recurrent   : s0=0 ; s_t=tanh(W s_{t-1}+Uin x_t+b) ; x=[a,b,b(,b)]   (THE E7 LEVER)
  tickshuffle : recurrent weights, per-sample shuffled schedule (proposal->correction order
                destroyed) -- MANDATORY control; must COLLAPSE for GO.

PREREG BARS (set BEFORE run; a_break_the_wall; no tune-to-green). Verdict on T_deep
(premise-b-favourable). R=recurrent reach; ff1=single nonlinear pass; slot/add=linear floors:
  GO  iff (R > max(add,slot,ff1)+0.05) AND (R > ff1+0.05) AND (shuffle < R-0.05) AND R>0.15
      -> recurrence beats BOTH the additive floor AND a single nonlinear pass, order/iteration
         bound (shuffle kills it) => premise-(b) escape real.
  NO-GO iff R <= ff1+0.02  (a single feedforward nonlinear pass matches the recurrent loop
         => credit is generic nonlinearity, NOT deliberation; E7 inert vs premise-(b)).
  else INCONCLUSIVE.
$0 CPU-local numpy, OMP_NUM_THREADS=4. seeds {7,4302,4303} averaged. ridge readout (frozen).
"""
import os, json, time
import numpy as np

OUT = "/Users/mini/dancinlab/anima/state/g0g6_premise_b_derisk"
K = 20; D = 48; M = 24; DH = 64; KTICKS = 3
HELD_FRAC = 0.30; RIDGE = 1e-2; SEEDS = [7, 4302, 4303]
SPECTRAL = 0.9; UIN_SCALE = 0.7; TGAIN = 2.4

def rand_orth_square(rng, n, spectral):
    A = rng.standard_normal((n, n)); Q, _ = np.linalg.qr(A); return Q * spectral

def make_concepts(rng):
    C = rng.standard_normal((K, D)); C /= np.linalg.norm(C, axis=1, keepdims=True); return C

# ---- teachers (frozen, method-agnostic) ----
def teacher_shallow_weights(rng):
    Ga = rng.standard_normal((DH, D)) / np.sqrt(D)
    Gb = rng.standard_normal((DH, D)) / np.sqrt(D)     # Ga != Gb -> order-dependent
    c  = rng.standard_normal(DH) * 0.1
    P  = rng.standard_normal((M, DH)) / np.sqrt(DH)
    return Ga, Gb, c, P

def teacher_shallow(a, b, w):
    Ga, Gb, c, P = w
    return P @ np.tanh(TGAIN * (Ga @ a) * (Gb @ b) + c)   # multiplicative interaction

def teacher_deep_weights(rng):
    W   = rand_orth_square(rng, DH, 1.05)               # DIFFERENT weights than student
    Uin = rng.standard_normal((DH, D)) * 0.9
    Vin = rng.standard_normal((DH, D)) * 0.9            # multiplicative coupling gate
    bi  = rng.standard_normal(DH) * 0.1
    P   = rng.standard_normal((M, DH)) / np.sqrt(DH)
    return W, Uin, Vin, bi, P

def teacher_deep(a, b, w):
    W, Uin, Vin, bi, P = w
    s = np.zeros(DH)
    for x in (a, b, b):                                 # depth-3 iterated refinement
        s = np.tanh(W @ s + Uin @ x + s * (Vin @ x) + bi)   # state<->input multiplicative
    return P @ s

# ---- student feature maps ----
def feat_additive(a, b, sw): return a + b
def feat_slotlin(a, b, sw):  return np.concatenate([a, b, a - b])

def student_weights(rng):
    Uab = rng.standard_normal((DH, 2 * D)) * (1.2 / np.sqrt(2 * D))
    c1  = rng.standard_normal(DH) * 0.1
    W   = rand_orth_square(rng, DH, SPECTRAL)
    Uin = rng.standard_normal((DH, D)) * (UIN_SCALE / np.sqrt(D) * np.sqrt(D))  # ~UIN_SCALE
    bi  = rng.standard_normal(DH) * 0.1
    return dict(Uab=Uab, c1=c1, W=W, Uin=Uin * (1.0/np.sqrt(D)), bi=bi)

def feat_ff1(a, b, sw):
    return np.tanh(sw["Uab"] @ np.concatenate([a, b]) + sw["c1"])

def feat_recur(a, b, sw, schedule=None):
    W, Uin, bi = sw["W"], sw["Uin"], sw["bi"]
    sched = schedule if schedule is not None else [a] + [b] * (KTICKS - 1)
    s = np.zeros(DH)
    for x in sched:
        s = np.tanh(W @ s + Uin @ x + bi)
    return s

def feat_recur_shuffle(a, b, sw, rng):
    base = [a] + [b] * (KTICKS - 1)
    order = rng.permutation(len(base))
    return feat_recur(a, b, sw, schedule=[base[i] for i in order])

# ---- readout + reach ----
def ridge_fit(X, Y):
    Xa = np.hstack([X, np.ones((X.shape[0], 1))])
    A = Xa.T @ Xa + RIDGE * np.eye(Xa.shape[1])
    return np.linalg.solve(A, Xa.T @ Y)

def predict(coef, X):
    return np.hstack([X, np.ones((X.shape[0], 1))]) @ coef

def r2_macro(Yhat, Ytrue):
    ss_res = ((Ytrue - Yhat) ** 2).sum()
    ss_tot = ((Ytrue - Ytrue.mean(0)) ** 2).sum()
    return float(1 - ss_res / ss_tot) if ss_tot > 0 else float("nan")

def reach_retrieval(Yhat, Ytrue):
    d2 = ((Yhat[:, None, :] - Ytrue[None, :, :]) ** 2).sum(-1)
    return float((d2.argmin(1) == np.arange(len(Ytrue))).mean())

def build_pairs(rng):
    pairs = [(a, b) for a in range(K) for b in range(K) if a != b]
    idx = rng.permutation(len(pairs))
    n_hold = int(round(HELD_FRAC * len(pairs)))
    hold_cand = [pairs[i] for i in idx[:n_hold]]
    train = [pairs[i] for i in idx[n_hold:]]
    seen = set(x for p in train for x in p); train_set = set(train)
    held = [p for p in hold_cand if p not in train_set and p[0] in seen and p[1] in seen]
    return train, held

def run_seed(seed):
    C = make_concepts(np.random.default_rng(seed))
    tw_sh = teacher_shallow_weights(np.random.default_rng(seed + 100))
    tw_dp = teacher_deep_weights(np.random.default_rng(seed + 200))
    sw = student_weights(np.random.default_rng(seed + 300))
    shuf_rng = np.random.default_rng(seed + 400)
    train, held = build_pairs(np.random.default_rng(seed + 500))

    def targets(tw, teacher, plist):
        return np.array([teacher(C[a], C[b], tw) for (a, b) in plist])

    methods = {
        "additive":   lambda a, b: feat_additive(C[a], C[b], sw),
        "slotlinear": lambda a, b: feat_slotlin(C[a], C[b], sw),
        "ff1_nonlin": lambda a, b: feat_ff1(C[a], C[b], sw),
        "recurrent":  lambda a, b: feat_recur(C[a], C[b], sw),
        "tickshuffle":lambda a, b: feat_recur_shuffle(C[a], C[b], sw, shuf_rng),
    }
    out = {"seed": seed, "n_train": len(train), "n_held": len(held),
           "chance": 1.0 / max(len(held), 1)}
    for tname, (tw, teacher) in {"T_shallow": (tw_sh, teacher_shallow),
                                 "T_deep": (tw_dp, teacher_deep)}.items():
        Ytr = targets(tw, teacher, train); Yte = targets(tw, teacher, held)
        mu, sd = Ytr.mean(0), Ytr.std(0) + 1e-8
        Ytr_n, Yte_n = (Ytr - mu) / sd, (Yte - mu) / sd
        res = {}
        for mname, ffn in methods.items():
            Xtr = np.array([ffn(a, b) for (a, b) in train])
            Xte = np.array([ffn(a, b) for (a, b) in held])
            coef = ridge_fit(Xtr, Ytr_n); Yhat = predict(coef, Xte)
            r2 = r2_macro(Yhat, Yte_n)
            res[mname] = {"reach": float(min(max(r2, 0.0), 1.0)), "r2_raw": r2,
                          "retrieval": reach_retrieval(Yhat, Yte_n)}
        out[tname] = res
    return out

def main():
    t0 = time.time()
    seeds = [run_seed(s) for s in SEEDS]
    def avg(tn, mn, key): return float(np.mean([s[tn][mn][key] for s in seeds]))
    chance = float(np.mean([s["chance"] for s in seeds]))
    agg = {"chance_retrieval": chance,
           "n_held_mean": float(np.mean([s["n_held"] for s in seeds])),
           "n_train_mean": float(np.mean([s["n_train"] for s in seeds]))}
    for tn in ("T_shallow", "T_deep"):
        agg[tn] = {m: {"reach": avg(tn, m, "reach"), "r2_raw": avg(tn, m, "r2_raw"),
                       "retrieval": avg(tn, m, "retrieval")}
                   for m in ("additive","slotlinear","ff1_nonlin","recurrent","tickshuffle")}

    dp = agg["T_deep"]
    R    = dp["recurrent"]["reach"]; add = dp["additive"]["reach"]
    slot = dp["slotlinear"]["reach"]; ff1 = dp["ff1_nonlin"]["reach"]
    shuf = dp["tickshuffle"]["reach"]
    strongest = max(add, slot, ff1)
    beats_additive     = R > strongest + 0.05
    recurrence_specific= R > ff1 + 0.05
    shuffle_collapses  = shuf < R - 0.05
    if beats_additive and recurrence_specific and shuffle_collapses and R > 0.15:
        verdict = "GO"
    elif R <= ff1 + 0.02:
        verdict = "NO-GO"
    else:
        verdict = "INCONCLUSIVE"

    summary = {
        "lever_id": "E7",
        "probe": "recurrent deliberation state (2-4 tick) -- premise-(b) forward-computation derisk",
        "reach_metric": "held-out R^2 clamped to [0,1] (unreach<=0); retrieval secondary",
        "config": {"K":K,"D":D,"M":M,"DH":DH,"KTICKS":KTICKS,"held_frac":HELD_FRAC,
                   "ridge":RIDGE,"seeds":SEEDS,"spectral_W":SPECTRAL,"tgain":TGAIN},
        "aggregate": agg, "per_seed": seeds,
        "verdict_regime": "T_deep (premise-(b)-favourable: depth-3 iterated multiplicative teacher, DIFFERENT weights)",
        "key_reaches_T_deep": {"recurrent_lever": R, "additive_bag_floor": add,
            "slotlinear_totalorder_floor": slot, "ff1_single_nonlinear_pass": ff1,
            "tickshuffle_control": shuf, "strongest_nonrecurrent_floor": strongest},
        "tests": {"beats_additive(vs strongest non-recurrent +0.05)": beats_additive,
                  "recurrence_specific(recurrent > ff1_nonlin +0.05)": recurrence_specific,
                  "shuffle_collapses(tickshuffle < recurrent -0.05)": shuffle_collapses,
                  "above_min(R>0.15)": bool(R > 0.15)},
        "verdict": verdict,
        "honesty": "synthetic frozen numpy reservoir != 303M engine-native; DIRECTIONAL go/no-go "
                   "for a GPU forward, not GREEN closure (a_toy_scale_recheck, a_engine_native_learning).",
        "elapsed_s": round(time.time() - t0, 2),
    }
    with open(f"{OUT}/E7.json", "w") as f:
        json.dump(summary, f, indent=2)
    disp = {"verdict": verdict,
            "T_deep_reach": {k: round(v,3) for k,v in summary["key_reaches_T_deep"].items()},
            "T_shallow_reach": {m: round(agg["T_shallow"][m]["reach"],3)
                                for m in ("additive","slotlinear","ff1_nonlin","recurrent","tickshuffle")},
            "tests": summary["tests"], "elapsed_s": summary["elapsed_s"]}
    print(json.dumps(disp, indent=2))

if __name__ == "__main__":
    main()
