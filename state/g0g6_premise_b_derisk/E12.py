#!/usr/bin/env python3
"""[E12] state-space non-commutative scan — $0 numpy STRUCTURE reachability probe.

DPI premise-(b) de-risk. NO 303M .clm decode (mini OOM). frozen-first, no tune-to-green, p7.

LEVER (E12): SSM/Mamba-style recurrence  h_{t+1} = A h_t + B x_t  with NON-COMMUTATIVE A.
  order-dependent state by construction -> breaks attention's permutation-equivariant
  (bag) assumption. For ordered pair (a,b):  h2 = A B x_a + B x_b.

TASK (G1 recombination reachability):
  K atomic concepts = random gaussian vectors x in R^d. combination = ORDERED pair (a,b),
  a!=b.  Split the K*(K-1) ordered pairs into TRAIN (seen combos) / HELD-OUT (unseen combos,
  constituents still seen in other pairs).  A frozen closed-form (ridge) linear readout is
  fit on TRAIN pair-reps to recover BOTH constituents-in-order (slot1=a, slot2=b, two K-way
  heads). REACH = held-out JOINT accuracy (both slots correct) = does the structure let an
  unseen combination be recombined/decoded.

CONTROLS on the SAME task (this is the crux):
  (1) additive-PLAIN   rep = B x_a + B x_b          -> order-blind bag (naive floor)
  (2) additive-SLOTTAG rep = B x_a + C x_b          -> order-AWARE bag, NO dynamics
                                                        = the HONEST/STRONG additive floor
  (3) SHUFFLE control  = lever rep, TRAIN targets permuted -> destroys correspondence (unreach)
  (bonus) nonlinear scan rep = tanh(A tanh(B x_a) + B x_b)  -> beyond-linear frozen RNN

KEY DPI POINT: a frozen LINEAR scan rep = A B x_a + B x_b is a LINEAR map of concat(x_a,x_b)
  via block [AB | B]; the slot-tagged bag is a LINEAR map via block [B | C]. For random
  frozen A,B,C both are just random d x 2d blocks -> a linear readout should reach them
  EQUALLY. If lever ties SLOTTAG, non-commutativity buys nothing a cheap positional tag
  doesn't already give -> NO-GO (DPI floor holds). Lever must beat SLOTTAG to be GO.

GO iff  lever_reach > additive(slottag)_reach + margin  AND  shuffle collapses.
"""
import json, os, time
import numpy as np

D          = 64      # concept / state dim
K          = 16      # number of atomic concepts
TRAIN_FRAC = 0.70
LAMBDA     = 1e-2    # ridge
N_SEEDS    = 24
MARGIN     = 0.03    # lever must beat strong-additive floor by this to count
OUT_DIR    = "/Users/mini/dancinlab/anima/state/g0g6_premise_b_derisk"


def rand_orth(rng, d):
    A = rng.standard_normal((d, d))
    Q, R = np.linalg.qr(A)
    Q *= np.sign(np.diag(R))          # deterministic sign
    return Q


def build_reps(rng, X, pairs, mode, A, B, C):
    """pairs: list of (a,b). return rep matrix [n,d]."""
    reps = np.zeros((len(pairs), D))
    for i, (a, b) in enumerate(pairs):
        xa, xb = X[a], X[b]
        if mode == "lever":                 # non-commutative linear scan
            reps[i] = A @ (B @ xa) + B @ xb
        elif mode == "add_plain":           # order-blind bag
            reps[i] = B @ xa + B @ xb
        elif mode == "add_slottag":         # order-aware bag, no dynamics
            reps[i] = B @ xa + C @ xb
        elif mode == "nonlin":              # beyond-linear frozen RNN
            reps[i] = np.tanh(A @ np.tanh(B @ xa) + B @ xb)
    return reps


def ridge_reach(reps_tr, reps_te, Ytr_slot1, Ytr_slot2, ya_te, yb_te, shuffle_rng=None):
    """closed-form ridge readout on TRAIN, joint held-out accuracy. no SGD, frozen."""
    if shuffle_rng is not None:             # SHUFFLE control: permute train targets
        p = shuffle_rng.permutation(len(Ytr_slot1))
        Ytr_slot1 = Ytr_slot1[p]; Ytr_slot2 = Ytr_slot2[p]
    Y = np.hstack([Ytr_slot1, Ytr_slot2])                        # [n_tr, 2K]
    G = reps_tr.T @ reps_tr + LAMBDA * np.eye(D)
    W = np.linalg.solve(G, reps_tr.T @ Y)                        # [D, 2K]
    P = reps_te @ W                                              # [n_te, 2K]
    pred_a = P[:, :K].argmax(1)
    pred_b = P[:, K:].argmax(1)
    slot1 = float(np.mean(pred_a == ya_te))
    slot2 = float(np.mean(pred_b == yb_te))
    joint = float(np.mean((pred_a == ya_te) & (pred_b == yb_te)))
    return slot1, slot2, joint


def one_seed(seed):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((K, D)); X /= np.linalg.norm(X, axis=1, keepdims=True)
    A = rand_orth(rng, D)                    # non-commutative (non-symmetric orthogonal)
    B = rng.standard_normal((D, D)) / np.sqrt(D)
    C = rng.standard_normal((D, D)) / np.sqrt(D)   # independent slot-tag projection

    pairs = [(a, b) for a in range(K) for b in range(K) if a != b]
    rng.shuffle(pairs)
    n_tr = int(len(pairs) * TRAIN_FRAC)
    tr, te = pairs[:n_tr], pairs[n_tr:]
    ya_tr = np.array([a for a, b in tr]); yb_tr = np.array([b for a, b in tr])
    ya_te = np.array([a for a, b in te]); yb_te = np.array([b for a, b in te])
    Y1 = np.eye(K)[ya_tr]; Y2 = np.eye(K)[yb_tr]

    out = {}
    for mode in ("lever", "add_plain", "add_slottag", "nonlin"):
        Rtr = build_reps(rng, X, tr, mode, A, B, C)
        Rte = build_reps(rng, X, te, mode, A, B, C)
        out[mode] = ridge_reach(Rtr, Rte, Y1, Y2, ya_te, yb_te)
    # shuffle control on the lever rep
    Rtr = build_reps(rng, X, tr, "lever", A, B, C)
    Rte = build_reps(rng, X, te, "lever", A, B, C)
    out["shuffle"] = ridge_reach(Rtr, Rte, Y1, Y2, ya_te, yb_te,
                                 shuffle_rng=np.random.default_rng(seed + 999))
    return out


def main():
    t0 = time.time()
    modes = ("lever", "add_plain", "add_slottag", "nonlin", "shuffle")
    acc = {m: {"slot1": [], "slot2": [], "joint": []} for m in modes}
    for s in range(N_SEEDS):
        r = one_seed(s)
        for m in modes:
            acc[m]["slot1"].append(r[m][0]); acc[m]["slot2"].append(r[m][1]); acc[m]["joint"].append(r[m][2])

    def ms(m, k): return float(np.mean(acc[m][k])), float(np.std(acc[m][k]))
    summary = {}
    for m in modes:
        s1m, s1s = ms(m, "slot1"); s2m, s2s = ms(m, "slot2"); jm, js = ms(m, "joint")
        summary[m] = {"slot1": s1m, "slot2": s2m, "joint_reach": jm, "joint_std": js}

    lever_reach   = summary["lever"]["joint_reach"]
    add_plain     = summary["add_plain"]["joint_reach"]
    add_slottag   = summary["add_slottag"]["joint_reach"]   # STRONG/honest additive floor
    shuffle_reach = summary["shuffle"]["joint_reach"]
    nonlin_reach  = summary["nonlin"]["joint_reach"]
    chance_joint  = 1.0 / (K * (K - 1)) * 0  # decoder isn't random; report empirical shuffle as floor

    beats_additive   = lever_reach > (add_slottag + MARGIN)
    shuffle_collapse = shuffle_reach < (lever_reach * 0.5) and shuffle_reach < 0.10

    if beats_additive and shuffle_collapse:
        verdict = "GO"
    elif (not beats_additive) and shuffle_collapse:
        verdict = "NO-GO"          # order-sensitive but no reach beyond slot-tagged bag
    else:
        verdict = "INCONCLUSIVE"

    out = {
        "lever_id": "E12_ssm_noncommutative_scan",
        "params": {"D": D, "K": K, "train_frac": TRAIN_FRAC, "lambda": LAMBDA,
                   "n_seeds": N_SEEDS, "margin": MARGIN, "n_ordered_pairs": K * (K - 1)},
        "reach_by_mode": summary,
        "heldout_reach_lever": lever_reach,
        "additive_plain_reach": add_plain,
        "additive_slottag_reach_STRONG_FLOOR": add_slottag,
        "nonlinear_scan_reach": nonlin_reach,
        "shuffle_control_reach": shuffle_reach,
        "beats_plain_additive": lever_reach > add_plain + MARGIN,
        "beats_STRONG_additive_slottag": beats_additive,
        "shuffle_collapses": shuffle_collapse,
        "verdict": verdict,
        "elapsed_s": round(time.time() - t0, 2),
    }
    print(json.dumps(out, indent=2))
    with open(os.path.join(OUT_DIR, "E12.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\n--- read ---")
    print(f"lever(noncomm scan) held-out reach = {lever_reach:.3f}")
    print(f"additive PLAIN (order-blind bag)    = {add_plain:.3f}  [lever beats: {out['beats_plain_additive']}]")
    print(f"additive SLOTTAG (order-aware bag)  = {add_slottag:.3f}  <- HONEST FLOOR  [lever beats: {beats_additive}]")
    print(f"nonlinear frozen scan               = {nonlin_reach:.3f}")
    print(f"shuffle control (unreach floor)     = {shuffle_reach:.3f}  [collapses: {shuffle_collapse}]")
    print(f"\nVERDICT: {verdict}")

if __name__ == "__main__":
    main()
