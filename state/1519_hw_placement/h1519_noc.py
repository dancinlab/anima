#!/usr/bin/env python3
# H_1519 HW-PLACEMENT — R1 numpy DIRECTIONAL MODEL of the neuromorphic NoC routing cost.
#
# SUBSTRATE TAG: MODEL (numpy model of the AKD1000 mesh-NoC hop-distance cost). ⊥ the REAL Lane-A AKD1000
#   on-chip measurement (a_lane_akida_gpu_split). The physical pi5-akida is GATED — do NOT dispatch compute
#   to it (a_pi5_akida_registry). True on-chip NoC routing + on-chip Φ = Lane-A FOLLOW-ON (ING h1519-onchip-akida).
#
# THE 3-TIER SYMMETRY (the insight — completes a symmetry across substrates):
#   Biology   (H_1516): physical axons → wiring COST → real placement Φ-suboptimal but ECONOMICAL (~37th pctile).
#   Software  (H_1515): connections = memory POINTERS → ZERO wiring cost → free to adopt the Φ-OPTIMAL placement.
#   Hardware  (H_1519): the AKD1000 is a PHYSICAL mesh Network-on-Chip → lane→core placement has REAL routing
#                       cost (NoC hop distance) → the biological wiring tax RETURNS, like biology.
#   PREDICTION: the Φ-optimal placement (free in software) becomes EXPENSIVE on the chip, and the HW-cost-
#   constrained optimum should re-converge toward biology's economical-suboptimal solution.
#
# NoC COST MODEL (documented, a_scale_honest_scope: TOY 15-lane 4×4 mesh, NOT the full 80-NPU AKD1000):
#   The BrainChip AKD1000 is a mesh-NoC accelerator (mesh Network-on-Chip linking its Neural Processing
#   units). We lay the 15 lanes on a 4×4 mesh of cores (16 cores, 15 used — smallest square grid holding 15).
#   A PLACEMENT = assignment of lanes to mesh cells, equivalently a permutation π applied to the brain
#   adjacency (relabel A_π[i][j]=A[π[i]][π[j]], identical to H_1515). NoC COST of a lane-adjacency edge (i,j)
#   = MANHATTAN (hop) distance between the mesh coords of lanes i,j. Total HW cost = Σ over present edges of
#   hop distance — the neuromorphic analogue of H_1517's biological wiring length.
#
# Φ = the SAME H_1512 min-cut IIT4 Φ (a_phi_iit4_tool), re-used byte-for-byte via import.
#
# FROZEN BARS (see H_1519_FREEZE.txt — set BEFORE running, c9, NO tune-to-green):
#   (P1 HW-TAX-ON-OPTIMUM)   cost(Φ-opt) >= P75 of the random NoC-cost distribution.
#   (P2 HW-CONSTRAINED-LOSS) (opt_phi − constrained_phi)/opt_phi >= 0.10 under a budget = brain cost.
#   (P3 BIOLOGY-CONVERGENCE, report-only) constrained optimum's Φ-percentile vs H_1516 ~37th pctile.

import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "1512_brain_topology")))
import h1512 as H   # build_population, apply_topology, phi_core, brain_adjacency, N=15, ALPHA=0.6

N = H.N
ALPHA = H.ALPHA

# H_1515 Φ-optimal placement (re-verified by hill-climb below; embedded for provenance).
OPT_PERM_1515 = [11, 0, 8, 4, 14, 2, 6, 1, 10, 5, 9, 7, 3, 13, 12]

# ── 4×4 mesh of cores (AKD1000 is a 2D mesh-NoC). Slot k → (row, col). 16 cells, 15 used. ──
MESH_R, MESH_C = 4, 4
MESH_COORDS = np.array([(k // MESH_C, k % MESH_C) for k in range(MESH_R * MESH_C)], dtype=int)  # 16 cells

# ── FROZEN thresholds (pre-registered, c9) ────────────────────────────────────────────────────
P1_COST_PCTILE = 0.75   # Φ-opt's NoC cost must be >= P75 of the random cost distribution
P2_LOSS_FRC    = 0.10   # HW-budget must force >= 10% Φ sacrifice vs the unconstrained optimum
M_SAMPLES      = 4000   # random placements for the (cost, Φ) distributions
N_STARTS       = 8      # hill-climb restarts

def relabel(A, p):
    return A[np.ix_(p, p)]

def phi_of(X, A):
    return H.phi_core(H.apply_topology(X, A, ALPHA))

def noc_cost(A, placement):
    """Total NoC routing cost of a placement: Σ over present lane-adjacency edges of the Manhattan
    (hop) distance between the two lanes' mesh coordinates. `placement[k]` = mesh-cell index where
    lane k sits (a permutation of 0..N-1 into the first N mesh cells of the 4×4 grid)."""
    coords = MESH_COORDS[placement]   # coords[k] = (row,col) of lane k
    cost = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            if A[i, j] > 0:
                dr = abs(int(coords[i][0]) - int(coords[j][0]))
                dc = abs(int(coords[i][1]) - int(coords[j][1]))
                cost += dr + dc
    return cost

def hill_climb_phi(X, A, perm0, max_passes=200):
    """Best-improving pairwise-swap hill climb on Φ (unconstrained) — re-verifies the Φ-optimum."""
    p = perm0.copy()
    best = phi_of(X, relabel(A, p))
    for _ in range(max_passes):
        ci = cj = -1; cbest = best
        for i in range(N):
            for j in range(i + 1, N):
                q = p.copy(); q[i], q[j] = q[j], q[i]
                phiq = phi_of(X, relabel(A, q))
                if phiq > cbest + 1e-12:
                    cbest = phiq; ci, cj = i, j
        if ci < 0: break
        p[ci], p[cj] = p[cj], p[ci]; best = cbest
    return p, best

def hill_climb_phi_budgeted(X, A, perm0, placement0, budget, max_passes=200):
    """Maximize Φ over lane-relabel permutations SUBJECT TO NoC cost ≤ budget. We hold the mesh
    PLACEMENT fixed at the brain-faithful slotting (placement0 = identity slots) and search the
    lane→slot permutation `p`; cost is recomputed for each candidate's relabelled adjacency on the
    fixed slots. Reject any swap that pushes cost above budget. Best-improving on Φ."""
    p = perm0.copy()
    def cost_of(perm):
        # adjacency relabelled by perm sits on the fixed mesh slots placement0
        return noc_cost(relabel(A, perm), placement0)
    best = phi_of(X, relabel(A, p))
    bcost = cost_of(p)
    for _ in range(max_passes):
        ci = cj = -1; cbest = best
        for i in range(N):
            for j in range(i + 1, N):
                q = p.copy(); q[i], q[j] = q[j], q[i]
                if cost_of(q) > budget + 1e-9:
                    continue
                phiq = phi_of(X, relabel(A, q))
                if phiq > cbest + 1e-12:
                    cbest = phiq; ci, cj = i, j
        if ci < 0: break
        p[ci], p[cj] = p[cj], p[ci]; best = cbest
    return p, best, cost_of(p)

def main():
    X = H.build_population(5120)          # ENGINE-UNIFORM population (matches the live engine substrate)
    A = H.brain_adjacency()
    identity = np.arange(N)
    slots0 = np.arange(N)                 # brain-faithful mesh slotting: lane k → mesh cell k

    # ── brain-faithful placement ──
    phi_brain = phi_of(X, relabel(A, identity))
    cost_brain = noc_cost(A, slots0)      # identity adjacency on identity slots

    # ── Φ-optimal placement (H_1515 opt_perm, re-verified) ──
    opt_perm = np.array(OPT_PERM_1515, dtype=int)
    phi_opt_embedded = phi_of(X, relabel(A, opt_perm))
    # re-verify the optimum by hill-climb from identity + random starts
    srng = np.random.default_rng(7000)
    best_perm, best_phi = identity.copy(), phi_brain
    for s in [identity] + [srng.permutation(N) for _ in range(N_STARTS - 1)]:
        p, ph = hill_climb_phi(X, A, s)
        if ph > best_phi:
            best_phi, best_perm = ph, p
    if phi_opt_embedded >= best_phi:
        opt_phi, opt_perm = phi_opt_embedded, opt_perm
    else:
        opt_phi = best_phi; opt_perm = best_perm
    # NoC cost of the Φ-optimal placement: its relabelled adjacency on the fixed mesh slots
    cost_opt = noc_cost(relabel(A, opt_perm), slots0)

    # ── M random placements → (cost, Φ) distributions ──
    rng = np.random.default_rng(5121)
    rand_phis = np.empty(M_SAMPLES)
    rand_costs = np.empty(M_SAMPLES)
    for k in range(M_SAMPLES):
        p = rng.permutation(N)
        Ap = relabel(A, p)
        rand_phis[k] = phi_of(X, Ap)
        rand_costs[k] = noc_cost(Ap, slots0)   # placement = the relabelled adjacency on fixed slots
    cost_p75 = float(np.percentile(rand_costs, 75))
    cost_p25 = float(np.percentile(rand_costs, 25))
    cost_mean = float(rand_costs.mean())
    phi_mean = float(rand_phis.mean())
    phi_max = float(rand_phis.max())

    # cost-percentile of the Φ-optimal placement (where its NoC cost sits in the random cost dist)
    cost_opt_pctile = float(np.mean(rand_costs < cost_opt))

    # ── HW-cost-constrained optimum: maximize Φ s.t. NoC cost ≤ budget (= brain-faithful cost) ──
    budget = cost_brain
    con_perm, con_phi, con_cost = hill_climb_phi_budgeted(X, A, identity.copy(), slots0, budget)
    # feasible-random fallback: also scan random placements within budget for a better feasible Φ
    for k in range(M_SAMPLES):
        if rand_costs[k] <= budget + 1e-9 and rand_phis[k] > con_phi:
            con_phi = float(rand_phis[k])
    # the constrained optimum's percentiles vs the random distributions
    con_phi_pctile = float(np.mean(rand_phis < con_phi))
    con_cost_pctile = float(np.mean(rand_costs < min(con_cost, budget)))

    # ── FROZEN BARS ──
    loss_frc = (opt_phi - con_phi) / opt_phi if opt_phi > 1e-9 else 0.0
    P1_pass = cost_opt >= cost_p75
    P2_pass = loss_frc >= P2_LOSS_FRC
    green = P1_pass and P2_pass

    out = {
        "substrate_tag": "MODEL",
        "note": "numpy DIRECTIONAL model of AKD1000 mesh-NoC hop-cost; real on-chip = Lane-A follow-on (ING h1519-onchip-akida)",
        "mesh": {"rows": MESH_R, "cols": MESH_C, "cells": MESH_R * MESH_C, "lanes": N},
        "phi_brain": round(phi_brain, 6),
        "cost_brain": round(cost_brain, 4),
        "phi_opt": round(opt_phi, 6),
        "cost_opt": round(cost_opt, 4),
        "opt_perm": [int(x) for x in opt_perm],
        "opt_perm_source": "H_1515 opt_perm" if phi_opt_embedded >= best_phi else "hill-climb re-find",
        "rand": {
            "phi_mean": round(phi_mean, 6), "phi_max": round(phi_max, 6),
            "cost_mean": round(cost_mean, 4), "cost_p25": round(cost_p25, 4), "cost_p75": round(cost_p75, 4),
            "M": M_SAMPLES,
        },
        "cost_opt_pctile": round(cost_opt_pctile, 4),
        "constrained": {
            "budget": round(budget, 4), "con_phi": round(con_phi, 6), "con_cost": round(con_cost, 4),
            "con_phi_pctile": round(con_phi_pctile, 4), "con_cost_pctile": round(con_cost_pctile, 4),
            "loss_frac_vs_opt": round(loss_frc, 4),
        },
        "bars": {
            "P1_hw_tax_on_optimum": {
                "thr": "cost_opt >= cost_p75", "cost_opt": round(cost_opt, 4),
                "cost_p75": round(cost_p75, 4), "pass": bool(P1_pass),
            },
            "P2_hw_constrained_loss": {
                "thr_frac": P2_LOSS_FRC, "loss_frac": round(loss_frc, 4), "pass": bool(P2_pass),
            },
            "P3_biology_convergence_reportonly": {
                "con_phi_pctile": round(con_phi_pctile, 4),
                "biology_ref_pctile_H1516": 0.37,
                "note": "report-only: is the HW-constrained optimum in biology's economical ballpark (~37th pctile)?",
            },
        },
        "green_directional": bool(green),
        "headline": (
            "neuromorphic NoC RE-INTRODUCES the biological wiring tax — Φ-optimal placement expensive on-chip "
            "AND HW-budget forces a real Φ sacrifice (3-tier symmetry biology→software→hardware CONFIRMED in model)"
            if green else
            "HW tax is SMALL — software's placement-freedom EXTENDS to the mesh-NoC (honest non-symmetry result)"
        ),
    }
    print(json.dumps(out, indent=2))
    return out

if __name__ == "__main__":
    main()
