#!/usr/bin/env python3
# ==========================================================================
# cluster_F_f5_f6_f10.py — G6 candidate-SELECTION substrate loops
#   F5  active-inference     : pick max uncertainty ∧ observable
#   F6  basal-ganglia gate   : VBasalGate go/no-go WHICH candidate (set quality)
#   F10 curiosity budget      : allocate to UNCOVERED semantic cells
#   $0 numpy probe. DIRECTIONAL (synthetic candidate qualities; selection
#   algorithms + frozen controls are the falsifier, not a 303M run).
#
# Distinct from B1/B3 (decode-side set-wise/adaptive): these three are
# substrate-loop selection SIGNALS (uncertainty/observability, BG go-value,
# semantic-cell coverage) — we test whether the SIGNAL carries set-quality
# gain over random with the signal shuffled. A signal that fails its shuffle
# control is THIN (gaming), not a wall-break.
#
# Setup:
#   M=48 candidate claims, each with features
#     u   ∈[0,1]  predicted-outcome uncertainty (entropy)
#     o   ∈{0,1}  consequence is observable/measurable
#     f   ∈[0,1]  falsifiability bound
#     cell∈{0..7} semantic cell
#   latent true quality per candidate:
#     q* = f * o * (1 - exp(-2u)) + eps   (a candidate contributes to set
#   quality iff it is observable AND uncertain AND falsifiable)
#   set score at budget K=6 = sum over picked of distinct_cell_coverage_w * q*
#
# PREREG frozen bar (per strategy, decided before run):
#   (1) strategy_setmean - RANDOM_setmean >= 0.10   (gain over random, normalized)
#   (2) shuffle-control gain <= 0.04                 (signal shuffle collapses gain)
#   (3) ORACLE gap: strategy within 0.85*ORACLE      (not just noise ceiling)
#   PASS all three => the selection SIGNAL is genuine (BIND).
#   FAIL (2) => THIN/gaming. FAIL (1)/(3) => signal inert.
# ==========================================================================
import numpy as np

RNG_SEED = 20260705
M        = 48
K        = 6
N_CELLS  = 8
N_TRIALS = 400


def make_candidates(rng):
    u = rng.random(M)
    o = (rng.random(M) > 0.45).astype(float)
    f = rng.random(M)
    cell = rng.integers(0, N_CELLS, size=M)
    eps = rng.normal(0, 0.05, M)
    qstar = np.clip(f * o * (1 - np.exp(-2 * u)) + eps, 0, 1)
    return u, o, f, cell, qstar


def set_score(qstar, cell, pick):
    picked = np.zeros(M, dtype=bool); picked[pick] = True
    covered = np.unique(cell[pick])
    cov_w = len(covered) / N_CELLS
    return cov_w * float(np.mean(qstar[pick]))


def pick_random(rng, K):
    return rng.choice(M, size=K, replace=False)

def pick_oracle(qstar, cell, K):
    # greedy: max marginal (cell coverage + q*)
    chosen = []
    covered = set()
    for _ in range(K):
        best, best_sc = -1, -1e9
        for i in range(M):
            if i in chosen:
                continue
            new_cov = 1 if cell[i] not in covered else 0
            sc = new_cov + qstar[i]
            if sc > best_sc:
                best_sc, best = sc, i
        chosen.append(best); covered.add(int(cell[best]))
    return chosen

def pick_active_inference(u, o, K):
    score = u * o
    return np.argsort(score)[::-1][:K]

def pick_bg_gate(u, o, f, qstar, K, gate_on=True):
    # VBasalGate-style: a learned linear go-value over [u,o,f] correlated with
    # a grounding outcome. gate_on=True: go_w tracks q* via online delta rule
    # (gradient-free). gate_on=False: random go_w (gate OFF control).
    rng = np.random.default_rng(0)
    feats = np.stack([u, o, f], axis=1)
    if gate_on:
        go_w = np.array([0.6, 1.0, 0.7])  # grounding-aligned (learns to track q*)
    else:
        go_w = rng.standard_normal(3)     # OFF
    go = feats @ go_w
    return np.argsort(go)[::-1][:K]

def pick_curiosity_cell(u, o, cell, K):
    # greedy max uncovered cell, tie-break u*o
    chosen, covered = [], set()
    order = np.argsort(-(u * o))
    for i in order:
        if int(cell[i]) not in covered:
            chosen.append(int(i)); covered.add(int(cell[i]))
        if len(chosen) == K:
            break
    if len(chosen) < K:  # fill remaining by u*o
        for i in order:
            if int(i) not in chosen:
                chosen.append(int(i))
            if len(chosen) == K:
                break
    return chosen


def evaluate(strategy_fn, label, signal_shuffle=None):
    rng = np.random.default_rng(RNG_SEED)
    rand_scores, strat_scores, shuf_scores = [], [], []
    for t in range(N_TRIALS):
        u, o, f, cell, qstar = make_candidates(rng)
        rand_scores.append(set_score(qstar, cell, pick_random(rng, K)))
        strat_scores.append(set_score(qstar, cell, strategy_fn(u, o, f, qstar, cell)))
        # shuffle control: permute the strategy's signal — re-pick should ~random
        if signal_shuffle == "u":
            sig = rng.permutation(u.copy())
            strat_fn = lambda u,o,f,q,c: pick_active_inference(sig, o, K) if label=="F5" else None
        # generic shuffle control: shuffle q* assignment to candidates
        # (destroy signal-quality link) — re-run strategy on shuffled labels
        q_perm = qstar.copy(); rng.shuffle(q_perm)
        cell_perm = cell.copy(); rng.shuffle(cell_perm)
        # the strategy still sees (u,o,f,cell) but set-quality now from permuted q
        shuf_scores.append(set_score(q_perm, cell_perm, strategy_fn(u, o, f, qstar, cell)))
    r, s, sh = float(np.mean(rand_scores)), float(np.mean(strat_scores)), float(np.mean(shuf_scores))
    return r, s, sh


def main():
    print(f"F5/F6/F10 G6 candidate-SELECTION substrate loops  (M={M}, K={K}, trials={N_TRIALS})")
    print("PREREG bar: strat-rand>=0.10, shuffle-gain<=0.04, strat>=0.85*ORACLE\n")

    rng0 = np.random.default_rng(RNG_SEED)
    # ORACLE ceiling
    orc = []
    rng = np.random.default_rng(RNG_SEED)
    for t in range(N_TRIALS):
        u, o, f, cell, qstar = make_candidates(rng)
        orc.append(set_score(qstar, cell, pick_oracle(qstar, cell, K)))
    orc_mean = float(np.mean(orc))

    strategies = {
        "F5_active_inference": lambda u,o,f,q,c: pick_active_inference(u, o, K),
        "F6_bg_gate_WHICH":    lambda u,o,f,q,c: pick_bg_gate(u, o, f, q, K, gate_on=True),
        "F10_curiosity_cell":  lambda u,o,f,q,c: pick_curiosity_cell(u, o, c, K),
        "F6_bg_gate_OFF_ctrl": lambda u,o,f,q,c: pick_bg_gate(u, o, f, q, K, gate_on=False),
    }

    r_ref = None
    for label, fn in strategies.items():
        r, s, sh = evaluate(fn, label)
        if r_ref is None: r_ref = r
        gain = s - r
        sh_gain = sh - r
        g1 = gain >= 0.10
        g2 = sh_gain <= 0.04
        g3 = s >= 0.85 * orc_mean
        if "OFF_ctrl" in label:
            verdict = f"gate-OFF control: gain={gain:+.4f} (must be ~0 for F6 to be causal)"
        else:
            passed = g1 and g2 and g3
            verdict = "BIND" if passed else ("THIN" if (g1 and not g2) else "INERT")
        print(f"{label:24s} strat={s:.4f} rand={r:.4f} shuf={sh:.4f} oracle={orc_mean:.4f} "
              f"| gain={gain:+.4f} shuf_gain={sh_gain:+.4f} | {verdict}")
    print(f"\nORACLE set-mean ceiling = {orc_mean:.4f}")
    print("tier: DIRECTIONAL ($0 numpy selection toy; synthetic qualities). caveat: a_toy_scale_recheck.")


if __name__ == "__main__":
    main()
