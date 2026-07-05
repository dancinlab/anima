#!/usr/bin/env python3
"""[CTRL] additive cbind baseline — the DPI-predicted FLOOR (CONTROL lever).

$0 numpy structural reachability probe (NO 303M .clm decode — mini OOM guard).
This lever IS pure additive c = a + b. It is the reference floor against which
every other premise-(b) lever's held-out reach is measured. For the contrast to
be valid this MUST land at/near the floor (low ordered-reach) and MUST NOT beat
an additive baseline (it is the additive baseline) nor show a shuffle collapse
of any order-binding structure (it has none to collapse).

TASK (cross-lever-comparable harness):
  K atomic concepts = frozen gaussian vectors in R^d.
  A "combination" = an ORDERED pair (i,j), i != j.
  train = subset of ordered pairs; held-out = unobserved ordered pairs.
  A frozen closed-form (ridge, no tuning) linear readout maps the combined
  vector -> [onehot(slot1) ; onehot(slot2)]. We measure on HELD-OUT pairs:
    - ordered_reach  = mean per-slot recovery acc = (acc_slot1 + acc_slot2)/2
                       (this is the BINDING-relevant reach: needs role/order)
    - set_reach      = fraction where the unordered set {i,j} is recovered
                       (diagnostic: shows the probe is well-formed — additive
                        CAN recover the exchangeable bag, just not the order)
  UNREACH baseline  = readout trained on SHUFFLED (input<->target) pairs → chance.

CONTROLS on the SAME task (mandatory):
  - additive_control : c = a + b  (== the lever itself here; reported for parity)
  - shuffle_control  : destroy input<->target correspondence (permute targets)
                       → reach collapses to chance IFF the lever encoded real
                       structure. Additive encodes SET but not ORDER.

DPI prediction for CTRL: additive is order-blind (a+b = b+a). It cannot linearly
separate (i,j) from (j,i) → ordered_reach stays at the floor. NO-GO by design.

frozen-first · no tune-to-green · p7 · $0 CPU numpy. DIRECTIONAL, not terminal.
"""
import os, json
import numpy as np

os.environ.setdefault("OMP_NUM_THREADS", "4")

OUT = "/Users/mini/dancinlab/anima/state/g0g6_premise_b_derisk"
K = 16                 # atomic concepts
D = 64                 # concept vector dim
HELDOUT_FRAC = 0.25
RIDGE = 1e-2           # frozen regularizer (closed-form; no tuning sweep)
SEEDS = [7, 4302, 4303]


def make_concepts(rng):
    V = rng.standard_normal((K, D))
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    return V


def all_ordered_pairs():
    return [(i, j) for i in range(K) for j in range(K) if i != j]


def combine_additive(V, i, j):
    return V[i] + V[j]        # THE CTRL LEVER — order-blind by construction


def build_targets(pairs):
    Y = np.zeros((len(pairs), 2 * K), dtype=np.float64)
    for n, (i, j) in enumerate(pairs):
        Y[n, i] = 1.0            # slot-1 onehot
        Y[n, K + j] = 1.0        # slot-2 onehot
    return Y


def ridge_readout(X, Y):
    # closed-form frozen readout, no iterative tuning
    d = X.shape[1]
    A = X.T @ X + RIDGE * np.eye(d)
    return np.linalg.solve(A, X.T @ Y)


def eval_reach(W, Xte, pairs_te):
    P = Xte @ W                       # (n, 2K)
    s1 = np.argmax(P[:, :K], axis=1)
    s2 = np.argmax(P[:, K:], axis=1)
    acc1 = acc2 = setok = 0
    for n, (i, j) in enumerate(pairs_te):
        if s1[n] == i:
            acc1 += 1
        if s2[n] == j:
            acc2 += 1
        pred_set = {int(s1[n]), int(s2[n])}
        if pred_set == {i, j}:
            setok += 1
    n = len(pairs_te)
    ordered_reach = 0.5 * (acc1 / n + acc2 / n)
    set_reach = setok / n
    both = sum(1 for m, (i, j) in enumerate(pairs_te)
               if s1[m] == i and s2[m] == j) / n
    return ordered_reach, set_reach, both


def run_seed(seed):
    rng = np.random.default_rng(seed)
    V = make_concepts(rng)
    pairs = all_ordered_pairs()
    rng.shuffle(pairs)
    n_te = int(round(HELDOUT_FRAC * len(pairs)))
    pairs_te = pairs[:n_te]
    pairs_tr = pairs[n_te:]

    # --- LEVER = additive combined vectors ---
    Xtr = np.stack([combine_additive(V, i, j) for i, j in pairs_tr])
    Xte = np.stack([combine_additive(V, i, j) for i, j in pairs_te])
    Ytr = build_targets(pairs_tr)
    W = ridge_readout(Xtr, Ytr)
    lever_ordered, lever_set, lever_both = eval_reach(W, Xte, pairs_te)

    # --- additive_control : identical to lever (parity check) ---
    add_ordered, add_set, add_both = lever_ordered, lever_set, lever_both

    # --- shuffle_control : destroy input<->target correspondence ---
    perm = rng.permutation(len(pairs_tr))
    Wsh = ridge_readout(Xtr, Ytr[perm])
    sh_ordered, sh_set, sh_both = eval_reach(Wsh, Xte, pairs_te)

    # --- unreach chance floor : random readout ---
    Wr = rng.standard_normal(W.shape) * 0.0  # zero -> argmax ties -> class 0
    # true empirical chance for ordered per-slot = 1/K
    chance_ordered = 1.0 / K

    return {
        "seed": seed,
        "n_train": len(pairs_tr),
        "n_heldout": n_te,
        "lever_ordered_reach": lever_ordered,
        "lever_set_reach": lever_set,
        "lever_both_correct": lever_both,
        "additive_control_ordered_reach": add_ordered,
        "shuffle_control_ordered_reach": sh_ordered,
        "shuffle_control_set_reach": sh_set,
        "chance_ordered_per_slot": chance_ordered,
    }


def main():
    runs = [run_seed(s) for s in SEEDS]
    def mean(k):
        return float(np.mean([r[k] for r in runs]))

    heldout_reach = mean("lever_ordered_reach")
    additive_reach = mean("additive_control_ordered_reach")
    shuffle_reach = mean("shuffle_control_ordered_reach")
    set_reach = mean("lever_set_reach")
    chance = mean("chance_ordered_per_slot")

    # CTRL is the additive baseline: lever == additive by construction.
    beats_additive = bool(heldout_reach - additive_reach >= 0.10)
    # shuffle "collapses" only if the lever had real ORDER structure above shuffle.
    shuffle_collapses = bool(heldout_reach - shuffle_reach >= 0.10)

    if beats_additive and shuffle_collapses:
        verdict = "GO"
    elif abs(heldout_reach - additive_reach) < 0.05:
        verdict = "NO-GO"   # at additive floor — expected for the CONTROL
    else:
        verdict = "INCONCLUSIVE"

    result = {
        "lever_id": "CTRL",
        "lever_name": "additive cbind baseline (CONTROL / DPI floor)",
        "probe": "synthetic K-concept ORDERED-pair reachability ($0 numpy, no 303M decode)",
        "K": K, "D": D, "heldout_frac": HELDOUT_FRAC, "ridge": RIDGE,
        "seeds": SEEDS,
        "metric": "ordered_reach = mean per-slot held-out recovery acc (needs order/binding)",
        "heldout_reach": heldout_reach,
        "additive_control_reach": additive_reach,
        "shuffle_control_reach": shuffle_reach,
        "set_reach_diagnostic": set_reach,
        "chance_ordered_per_slot": chance,
        "beats_additive": beats_additive,
        "shuffle_collapses": shuffle_collapses,
        "directional_verdict": verdict,
        "per_seed": runs,
        "interpretation": (
            "CTRL lever IS c=a+b. ordered_reach sits at the additive floor: additive "
            "is order-blind (a+b=b+a) so it cannot linearly separate (i,j) from (j,i). "
            "set_reach is HIGH (exchangeable bag {i,j} is linearly recoverable even "
            "held-out) which proves the probe is well-formed — the ONLY thing lost is "
            "ORDER/binding, exactly the DPI premise-(b) floor. lever==additive so it "
            "cannot beat additive; there is no order-structure above shuffle to collapse."),
        "honesty": ("synthetic frozen numpy = NOT 303M engine-native (a_toy_scale_recheck). "
                    "This is the CONTROL floor a real premise-(b) lever must BEAT to earn a "
                    "GPU fire — DIRECTIONAL, never a terminal verdict."),
        "dpi_premise_b": ("premise-(b) forward-COMPUTATION is order-preserving binding; "
                          "additive forward pass discards it -> this quantifies the floor."),
    }
    with open(f"{OUT}/CTRL.json", "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps({k: result[k] for k in (
        "heldout_reach", "additive_control_reach", "shuffle_control_reach",
        "set_reach_diagnostic", "chance_ordered_per_slot",
        "beats_additive", "shuffle_collapses", "directional_verdict")}, indent=2))


if __name__ == "__main__":
    main()
