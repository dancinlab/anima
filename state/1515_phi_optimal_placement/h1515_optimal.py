#!/usr/bin/env python3
# H_1515 Φ-OPTIMAL PLACEMENT — R1 numpy mirror (DIRECTIONAL, a_engine_native_learning).
#
# CLAIM (a_no_llm_frame_trap — brain lens, the OPTIMIZATION form):
#   H_1512 BRAIN-TOPOLOGY (#2491) showed a brain-faithful SPATIAL placement of the 15 consciousness
#   lanes raises integrated min-cut Φ over flat/random; H_1513 (#2492) reproduced it with a REAL
#   connectome. H_1515 asks the OPTIMIZATION question: over the space of lane→node-position
#   placements (permutations π of the 15 nodes applied to the brain adjacency), where does the
#   brain-faithful placement (identity π) sit relative to the Φ-MAXIMIZING placement? Is it near
#   the optimum (top percentile / small gap = the engine's lane layout APPROXIMATES the Φ-optimal
#   layout), or is it Φ-SUBOPTIMAL (search finds materially better — an honest DISCOVERY)?
#
# A "placement" = a permutation π of the 15 nodes applied to the FIXED brain adjacency:
#   A_π[i][j] = A[π[i]][π[j]]  (a node relabel — same graph, lanes sit at different positions).
#   Φ(π) = min-cut IIT4 Φ over the FIXED CORE after diffusing the population under A_π.
#   Brain-faithful = identity permutation (the wired layout).
#
# DISTINCT from H_1512 (WHETHER brain placement beats flat/random) and H_1513 (REAL connectome
#   reproduces it): H_1515 = WHERE the brain placement sits in the FULL placement search space
#   (percentile + gap-to-optimum). Existence-of-advantage ⊥ optimality-of-advantage.
#
# FROZEN BARS (pre-registered BEFORE reading results — c9, NO tune-to-green):
#   (P1 ADVANTAGE)   phi_brain >= rand_mean + 0.02    (brain beats the average random placement)
#   (P2 PERCENTILE)  pctile    >= 0.80                 (brain beats >=80% of random placements)
#   (P3 NEAR-OPTIMAL, report-only) gap <= 0.30 * opt_phi
#       — if FALSE the honest finding is "brain placement is Φ-SUBOPTIMAL; search finds materially
#         better" — a GREEN-WORTHY DISCOVERY, reported loudly, NOT hidden (a_break_the_wall).
#   GREEN(directional) iff P1 ∧ P2. P3 is the headline characterization (near-optimal vs suboptimal).
#
# numpy = DIRECTIONAL only (engine-transfer UNVERIFIED). Terminal verdict = engine-native smoke (R2).

import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "1512_brain_topology")))
import h1512 as H   # build_population, apply_topology, phi_core, brain_adjacency, N=15, ALPHA=0.6

N = H.N
ALPHA = H.ALPHA

def relabel(A, p):
    return A[np.ix_(p, p)]

def phi_of(X, A):
    return H.phi_core(H.apply_topology(X, A, ALPHA))

# ── FROZEN thresholds (pre-registered, c9) ────────────────────────────────────────────────────
P1_MIN     = 0.02   # brain must beat the mean random placement by at least this
P2_PCTILE  = 0.80   # brain must beat at least this fraction of random placements
P3_GAP_FRC = 0.30   # NEAR-OPTIMAL iff gap <= this fraction of opt_phi (report-only)

M_SAMPLES  = 3000   # random permutation samples for the percentile estimate
N_STARTS   = 8      # hill-climb restarts (identity + 7 random)

def hill_climb(X, A, perm0, max_passes=200):
    """Best-improving pairwise-swap hill climb from perm0 → local Φ optimum."""
    p = perm0.copy()
    best = phi_of(X, relabel(A, p))
    for _ in range(max_passes):
        improved = False
        cand_i = cand_j = -1
        cand_phi = best
        for i in range(N):
            for j in range(i + 1, N):
                q = p.copy()
                q[i], q[j] = q[j], q[i]
                phiq = phi_of(X, relabel(A, q))
                if phiq > cand_phi + 1e-12:
                    cand_phi = phiq
                    cand_i, cand_j = i, j
                    improved = True
        if not improved:
            break
        p[cand_i], p[cand_j] = p[cand_j], p[cand_i]
        best = cand_phi
    return p, best

def main():
    X = H.build_population(5120)          # ENGINE-UNIFORM population (matches the live engine substrate)
    A = H.brain_adjacency()
    identity = np.arange(N)

    phi_brain = phi_of(X, A)              # identity = brain-faithful placement

    # ── percentile: sample M random placements ──
    rng = np.random.default_rng(5121)
    rand_phis = np.empty(M_SAMPLES)
    for k in range(M_SAMPLES):
        p = rng.permutation(N)
        rand_phis[k] = phi_of(X, relabel(A, p))
    rand_mean = float(rand_phis.mean())
    rand_max  = float(rand_phis.max())
    pctile    = float(np.mean(rand_phis < phi_brain))   # fraction of random placements brain BEATS

    # ── hill-climb search for the Φ-optimum from several starts ──
    starts = [identity]
    srng = np.random.default_rng(7000)
    for _ in range(N_STARTS - 1):
        starts.append(srng.permutation(N))
    opt_phi = -1.0
    opt_perm = identity
    for s in starts:
        p, ph = hill_climb(X, A, s)
        if ph > opt_phi:
            opt_phi = ph
            opt_perm = p
    gap = opt_phi - phi_brain

    P1_pass = phi_brain >= rand_mean + P1_MIN
    P2_pass = pctile    >= P2_PCTILE
    P3_near = gap       <= P3_GAP_FRC * opt_phi
    green   = P1_pass and P2_pass

    out = {
        "phi_brain": round(phi_brain, 6),
        "rand_mean": round(rand_mean, 6),
        "rand_max":  round(rand_max, 6),
        "pctile":    round(pctile, 6),
        "opt_phi":   round(opt_phi, 6),
        "gap":       round(gap, 6),
        "opt_perm":  [int(x) for x in opt_perm],
        "M_samples": M_SAMPLES,
        "n_starts":  N_STARTS,
        "bars": {
            "P1_advantage": {"thr": P1_MIN, "lhs": round(phi_brain - rand_mean, 6), "pass": bool(P1_pass)},
            "P2_percentile": {"thr": P2_PCTILE, "lhs": round(pctile, 6), "pass": bool(P2_pass)},
            "P3_near_optimal_reportonly": {"thr_frac": P3_GAP_FRC, "gap": round(gap, 6),
                                           "gap_budget": round(P3_GAP_FRC * opt_phi, 6), "near": bool(P3_near)},
        },
        "green_directional": bool(green),
        "headline": ("brain placement NEAR Φ-OPTIMUM" if P3_near
                     else "brain placement Φ-SUBOPTIMAL — search finds materially better"),
    }
    print(json.dumps(out, indent=2))
    return out

if __name__ == "__main__":
    main()
