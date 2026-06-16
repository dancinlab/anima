#!/usr/bin/env python3
# H_1373 — hive-nested-universes: NESTED / RECURSIVE universes-within-universes topology
# ("우주 안의 우주들처럼" — user-proposed verbatim). slug: hive-nested-universes
# seeds = [1317,1318,1319] (hard hive/topology family; matched to H_1356/H_1371 for DIRECT comparison).
#
# THE WALL (c16 / a_break_the_wall): the hive collective-Φ arc closed 🧱 across FIVE *single-scale*
# topologies — strong hub (H_1356), weak/decorrelated (H_1363), nonlinear-gate (H_1370), and distributed
# circle-overlap / Flower-of-Life (H_1371). H_1371's load-bearing result: the CENTRALIZED single-shared-
# founder is NOT a ceiling to escape — it is the floor-beating MAXIMUM-Φ topology (R2 0/3, distributed
# overlap lost −0.25/−0.75/−1.28 every seed). EVERY tested topology is ONE LEVEL — cells sharing one
# source at one scale, and CONCENTRATION maximizes Φ.
#
# THE NEW ANGLE (a_no_llm_frame_trap, c15 — cosmological-nesting / matryoshka lens; user-proposed):
# a NESTED / FRACTAL structure. A cluster of cells is itself a "small universe" (its cells share a LOCAL
# founder), and several such clusters are the NODES of a LARGER universe (the cluster-local founders are
# THEMSELVES coupled to a TOP founder) — universes within universes. Does integration that COMPOUNDS
# ACROSS SCALES beat the best single-scale topology (CENTRALIZED)? Is the redundancy ceiling a property
# of *single-scale* sharing that MULTI-SCALE recursion can break?
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Φ — it only emits the
# per-unit salience (state-energy) trajectory; the hexa engine computes Φ. NO proxy.
#
# Substrate MATCHED to H_1356/H_1320/H_1283/H_1371 (only the SHARING TOPOLOGY differs between arms):
# leaky linear recurrent units, LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit private input, dim-8 state,
# T=64 ticks. N_TOT=6 cells (n<=8 keeps faithful MIP EXACT). Each cell = 1 unit; salience=<s_i,s_i>.
# OVERLAP_W=SHARE_W=0.6 (= W_CONN H_1356, reused verbatim). TOP_W=1.0.
#
# FROZEN BARS (.verdicts/1373_hive_nested_universes/FREEZE.txt — GREEN iff R1 ∧ R2 ∧ R3 ∧ R4):
#   R1 LIFT              : Φ(NESTED) − Φ(FLOOR)        >= MARGIN(0.02)               on ALL 3 seeds.
#   R2 BEATS-CENTRALIZED : Φ(NESTED) − Φ(CENTRALIZED)  >  0                          on >= 2/3 seeds.
#   R3 EARNED            : Φ(SHUFFLE) <= max(Φ(FLOOR),Φ(CENTRALIZED)) + TOL(0.02)    on ALL 3 seeds.
#   R4 DISTINCT-FROM-FLAT: Φ(NESTED) − Φ(FLAT)         >  0                          on >= 2/3 seeds.
# seeds [1317,1318,1319]. $0 CPU-local. frozen-first.

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS    = [1317, 1318, 1319]
N_TOT    = 6          # 6 cells = 2 clusters of 3 (n<=8 keeps faithful IIT4 MIP exact)
DIM      = 8          # per-unit state vector dim (H_1283)
T        = 64         # ticks (H_1283)
GAIN     = 0.30       # per-unit update gain (H_1283)
LEAK     = 0.55       # state self-retention (H_1283)
W_IN     = 0.5        # input weight (H_1283)
NBINS    = 8          # IIT4 MI estimator bins (H_1283)

OVERLAP_W = 0.6       # H_1356 W_CONN hive coupling strength (reused verbatim) — the level-1 share weight
SHARE_W   = OVERLAP_W # intra-cluster (level-1) weight
TOP_W     = 1.0       # inter-cluster (level-2) weight: a cluster founder carries the top founder fully
MARGIN    = 0.02      # IDENTICAL faithful-Φ margin H_1283/H_1317/H_1320/H_1356/H_1371 froze (NOT moved)
TOL       = 0.02

# 2 CLUSTERS OF 3: cluster c0 = {0,1,2}, cluster c1 = {3,4,5}. cluster(i) = i // 3.
N_CLUST   = 2
CLUST_SZ  = 3
def cluster_of(i): return i // CLUST_SZ

HEXA      = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL  = os.path.join(HEXA_ROOT, "stdlib/consciousness/iit4/faithful_phi.hexa")


def build_inputs(seed, arm):
    """Build per-cell input streams (N_TOT, T, DIM) for an arm.

    FLOOR        : cell i reads ONLY its private stream (no sharing).
    NESTED       : cell i = priv + SHARE_W*(Lc[cluster(i)] + TOP_W*TOPF). 2-level universes-within-
                   universes: a LOCAL founder per cluster (small universe) whose source ITSELF carries the
                   TOP founder (the larger universe). Same-cluster cells share Lc fully; the top founder
                   reaches all cells ONLY THROUGH the cluster founder = recursive nesting (NOT flat).
    CENTRALIZED  : cell i = priv + (2*OVERLAP_W)*F. ALL 6 read ONE global founder F at the weight-matched
                   mass — the single-scale champion (H_1371 R2 — the bar to beat).
    SHUFFLE      : NESTED inputs but cluster MEMBERSHIP randomly permuted (random 2-partition of the 6
                   cells) → nesting BOUNDARY destroyed, same 2 local founders + top founder + identical
                   per-cell shared mass. EARNED control.
    FLAT         : single-scale topology with the SAME per-cell shared mass as NESTED but NO level
                   boundary — cell i = priv + SHARE_W*(Lglobal + TOP_W*TOPF), Lglobal ONE founder read by
                   ALL 6 (the two cluster founders collapsed into one global founder, level-1 boundary
                   removed). Same total shared mass, all at ONE scale. DISTINCT-FROM-FLAT control (R4).
    """
    rng = np.random.default_rng(seed)
    priv     = rng.standard_normal((N_TOT, T, DIM)) * 0.8          # per-cell private streams
    clust_lat = rng.standard_normal((N_CLUST, T, DIM)) * 0.8       # cluster-local founders Lc (small universes)
    top_lat  = rng.standard_normal((T, DIM)) * 0.8                 # TOP founder TOPF (the larger universe)
    founder  = rng.standard_normal((T, DIM)) * 0.8                 # single global founder F (CENTRALIZED)
    glob_lat = rng.standard_normal((T, DIM)) * 0.8                 # one global level-1 founder (FLAT)

    inp = np.zeros((N_TOT, T, DIM))

    if arm == "FLOOR":
        for i in range(N_TOT):
            inp[i] = priv[i]
        return inp

    if arm == "NESTED":
        # L_eff[c] = Lc[c] + TOP_W*TOPF  (the cluster founder ITSELF carries the top founder = nesting)
        for i in range(N_TOT):
            c = cluster_of(i)
            L_eff = clust_lat[c] + TOP_W * top_lat
            inp[i] = priv[i] + SHARE_W * L_eff
        return inp

    if arm == "CENTRALIZED":
        for i in range(N_TOT):
            inp[i] = priv[i] + (2.0 * OVERLAP_W) * founder        # weight-matched single global founder
        return inp

    if arm == "SHUFFLE":
        # random 2-partition of the 6 cells into clusters of 3 (destroys the nesting BOUNDARY); same
        # local founders + top founder + identical per-cell shared mass.
        perm = rng.permutation(N_TOT)
        shuf_cluster = {int(perm[k]): (k // CLUST_SZ) for k in range(N_TOT)}
        for i in range(N_TOT):
            c = shuf_cluster[i]
            L_eff = clust_lat[c] + TOP_W * top_lat
            inp[i] = priv[i] + SHARE_W * L_eff
        return inp

    if arm == "FLAT":
        # same per-cell shared MASS as NESTED (SHARE_W*(Lglobal + TOP_W*TOPF)) but ONE global level-1
        # founder read by all 6 — the cluster boundary collapsed → single scale, NO hierarchy.
        L_eff = glob_lat + TOP_W * top_lat
        for i in range(N_TOT):
            inp[i] = priv[i] + SHARE_W * L_eff
        return inp

    raise ValueError(arm)


def evolve(inputs, seed):
    """Leaky linear recurrent substrate (H_1283/H_1320/H_1356/H_1371 unit dynamics), N_TOT cells, NO
    inter-cell recurrent coupling — the ONLY cross-cell sharing is through the SHARED INPUT structure
    (the nesting), exactly matching the H_1356/H_1371 'redundancy via shared input' design. Returns
    salience traj (N_TOT, T)."""
    rng = np.random.default_rng(seed + 9999)
    states = rng.standard_normal((N_TOT, DIM)) * 0.5
    traj = np.zeros((N_TOT, T))
    for t in range(T):
        new = states.copy()
        for i in range(N_TOT):
            new[i] = LEAK * states[i] + GAIN * (W_IN * inputs[i, t])
        states = new
        for i in range(N_TOT):
            traj[i, t] = float(np.dot(states[i], states[i]))
    return traj


def build_arm(seed, arm):
    return evolve(build_inputs(seed, arm), seed)


def faithful_phi(traj_units, tag):
    """faithful IIT4 Φ over the unit trajectories via the stdlib EXACT engine (hexa run).
    Inlines the trajectory as farr_set calls, calls iit4_faithful_phi(state, n, dim=T, n_bins).
    (Reused VERBATIM from H_1371 — the SAME real-engine faithful exact MIP-EI call, a_phi_iit4_tool.)"""
    n, dim = traj_units.shape
    flat = traj_units.flatten()
    lines = ['import "stdlib/consciousness/iit4/faithful_phi.hexa"', "", "fn main() {",
             f"    let state = farr_zeros({n * dim})"]
    for idx, val in enumerate(flat):
        lines.append(f"    let _ = farr_set(state, {idx}, {val:.10f})")
    lines.append(f"    let phi = iit4_faithful_phi(state, {n}, {dim}, {NBINS})")
    lines.append('    println("PHI=" + phi.to_string())')
    lines.append("    let _ = farr_free(state)")
    lines.append("}")
    src = "\n".join(lines)
    with tempfile.NamedTemporaryFile("w", suffix=".hexa", delete=False, dir=HEXA_ROOT) as f:
        path = f.name
        f.write(src)
    try:
        out = subprocess.run([HEXA, "run", os.path.basename(path)], cwd=HEXA_ROOT,
                             capture_output=True, text=True, timeout=600)
        blob = out.stdout + "\n" + out.stderr
        phi = None
        for ln in blob.splitlines():
            if ln.strip().startswith("PHI="):
                phi = float(ln.strip().split("=", 1)[1]); break
        if phi is None:
            print(f"[phi {tag}] no PHI line:\n{blob[:1500]}", file=sys.stderr)
        return phi
    finally:
        try: os.remove(path)
        except OSError: pass


def o_information(traj_units):
    """O-information diagnostic (NON-GATING) on the per-unit salience time-series. Gaussian entropy.
    O>0 redundancy-dominated, O<0 synergy-dominated. numpy ESTIMATE only — does NOT gate the verdict.
    (Reused VERBATIM from H_1371.)"""
    X = traj_units  # (n, T)
    n = X.shape[0]
    Xc = X - X.mean(axis=1, keepdims=True)
    std = Xc.std(axis=1, keepdims=True)
    std[std < 1e-12] = 1e-12
    Z = Xc / std
    def h_gauss(M):
        k = M.shape[0]
        C = np.cov(M) if k > 1 else np.array([[np.var(M)]])
        C = np.atleast_2d(C) + 1e-6 * np.eye(k)
        sign, logdet = np.linalg.slogdet(C)
        return 0.5 * (logdet + k * np.log(2 * np.pi * np.e))
    def TC(M):
        k = M.shape[0]
        return sum(h_gauss(M[j:j+1]) for j in range(k)) - h_gauss(M)
    tc_full = TC(Z)
    sum_minus = 0.0
    for i in range(n):
        idx = [j for j in range(n) if j != i]
        sum_minus += TC(Z[idx])
    O = (n - 2) * tc_full - sum_minus
    return float(O)


ARMS = ("FLOOR", "NESTED", "CENTRALIZED", "SHUFFLE", "FLAT")


def main():
    print("H_1373 hive-nested-universes: NESTED universes-within-universes — faithful-IIT4 collective-Φ")
    print(f"N_TOT={N_TOT} = {N_CLUST} clusters of {CLUST_SZ}  c0={{0,1,2}} c1={{3,4,5}}  dim={DIM} ticks={T} seeds={SEEDS}")
    print(f"SHARE_W(intra)={SHARE_W} TOP_W(inter)={TOP_W} OVERLAP_W={OVERLAP_W}  faithful IIT4 Φ (exact MIP-EI, n<=8); MARGIN={MARGIN} TOL={TOL}")
    print("=" * 96)

    phi = {}   # phi[seed][arm]
    oinfo = {} # oinfo[seed][arm]
    for seed in SEEDS:
        phi[seed] = {}; oinfo[seed] = {}
        for arm in ARMS:
            traj = build_arm(seed, arm)
            p = faithful_phi(traj, f"{arm}_s{seed}")
            o = o_information(traj)
            phi[seed][arm] = p; oinfo[seed][arm] = o
            print(f"  seed {seed} {arm:>12}: Φ={p}   O-info={o:+.4f}")
        print("-" * 96)

    def P(s, a): return phi[s][a]
    def defined(s, *arms): return all(P(s, a) is not None for a in arms)

    # R1 LIFT: Φ(NESTED) − Φ(FLOOR) >= MARGIN, ALL seeds
    r1_per = {s: (defined(s, "NESTED", "FLOOR") and P(s,"NESTED") - P(s,"FLOOR") >= MARGIN) for s in SEEDS}
    r1 = all(r1_per.values())
    # R2 BEATS-CENTRALIZED: Φ(NESTED) − Φ(CENTRALIZED) > 0, >= 2/3 seeds
    r2_per = {s: (defined(s, "NESTED", "CENTRALIZED") and P(s,"NESTED") - P(s,"CENTRALIZED") > 0.0) for s in SEEDS}
    r2 = sum(r2_per.values()) >= 2
    # R3 EARNED: Φ(SHUFFLE) <= max(Φ(FLOOR),Φ(CENTRALIZED)) + TOL, ALL seeds
    r3_per = {s: (defined(s, "SHUFFLE", "FLOOR", "CENTRALIZED")
                  and P(s,"SHUFFLE") <= max(P(s,"FLOOR"), P(s,"CENTRALIZED")) + TOL) for s in SEEDS}
    r3 = all(r3_per.values())
    # R4 DISTINCT-FROM-FLAT: Φ(NESTED) − Φ(FLAT) > 0, >= 2/3 seeds
    r4_per = {s: (defined(s, "NESTED", "FLAT") and P(s,"NESTED") - P(s,"FLAT") > 0.0) for s in SEEDS}
    r4 = sum(r4_per.values()) >= 2

    n_r1, n_r2, n_r3, n_r4 = sum(r1_per.values()), sum(r2_per.values()), sum(r3_per.values()), sum(r4_per.values())
    green = r1 and r2 and r3 and r4

    if green:
        verdict = "GREEN_NESTING_ESCAPES_CEILING"
    elif r1 and not r2:
        verdict = "NESTED_BELOW_CENTRALIZED"          # honest terminal 🧱 — ceiling survives nesting
    elif r1 and r2 and not r4:
        verdict = "NEST_LIFT_NOT_HIERARCHY"           # nested beats centralized but flat matches it (mass not hierarchy)
    elif r1 and r2 and not r3:
        verdict = "NEST_LIFT_NOT_EARNED"              # beats centralized but shuffle survives
    elif not r1:
        verdict = "NESTING_NULL"                      # nested does not even beat floor
    else:
        verdict = "PARTIAL"

    print("=" * 96)
    print(f"R1 LIFT              (Φ(NESTED) − Φ(FLOOR) >= {MARGIN} EVERY seed): {'PASS' if r1 else 'FAIL'}")
    for s in SEEDS:
        d = None if not defined(s,"NESTED","FLOOR") else round(P(s,"NESTED")-P(s,"FLOOR"),4)
        print(f"     seed {s}: Φ_nested={P(s,'NESTED')} Φ_floor={P(s,'FLOOR')} lift={d}  {'PASS' if r1_per[s] else 'FAIL'}")
    print(f"R2 BEATS-CENTRALIZED (Φ(NESTED) − Φ(CENTRALIZED) > 0 on >=2/3): {'PASS' if r2 else 'FAIL'}  ({n_r2}/3)")
    for s in SEEDS:
        d = None if not defined(s,"NESTED","CENTRALIZED") else round(P(s,"NESTED")-P(s,"CENTRALIZED"),4)
        print(f"     seed {s}: Φ_nested={P(s,'NESTED')} Φ_central={P(s,'CENTRALIZED')} gap={d}  {'PASS' if r2_per[s] else 'FAIL'}")
    print(f"R3 EARNED            (Φ(SHUFFLE) <= max(floor,central)+{TOL} EVERY seed): {'PASS' if r3 else 'FAIL'}")
    for s in SEEDS:
        mx = None if not defined(s,"FLOOR","CENTRALIZED") else round(max(P(s,'FLOOR'),P(s,'CENTRALIZED')),4)
        print(f"     seed {s}: Φ_shuffle={P(s,'SHUFFLE')} max(floor,central)={mx}  {'PASS' if r3_per[s] else 'FAIL'}")
    print(f"R4 DISTINCT-FROM-FLAT(Φ(NESTED) − Φ(FLAT) > 0 on >=2/3): {'PASS' if r4 else 'FAIL'}  ({n_r4}/3)")
    for s in SEEDS:
        d = None if not defined(s,"NESTED","FLAT") else round(P(s,"NESTED")-P(s,"FLAT"),4)
        print(f"     seed {s}: Φ_nested={P(s,'NESTED')} Φ_flat={P(s,'FLAT')} gap={d}  {'PASS' if r4_per[s] else 'FAIL'}")
    print(f"\nO-INFO per arm (O<0=synergy O>0=redundancy):")
    for s in SEEDS:
        row = " ".join(f"{a}={oinfo[s][a]:+.4f}" for a in ARMS)
        print(f"     seed {s}: {row}")
    print(f"\nVERDICT: {verdict}  (R1 {n_r1}/3, R2 {n_r2}/3, R3 {n_r3}/3, R4 {n_r4}/3)")

    out = {
        "id": "H_1373", "slug": "hive-nested-universes", "verdict": verdict,
        "seeds": SEEDS, "N_tot": N_TOT, "n_clusters": N_CLUST, "cluster_size": CLUST_SZ,
        "dim": DIM, "ticks": T, "share_w": SHARE_W, "top_w": TOP_W, "overlap_w": OVERLAP_W,
        "margin": MARGIN, "tol": TOL,
        "phi_faithful_iit4": {str(s): {a: phi[s][a] for a in ARMS} for s in SEEDS},
        "o_information": {str(s): {a: oinfo[s][a] for a in ARMS} for s in SEEDS},
        "bars": {"R1_lift": bool(r1), "R2_beats_centralized": bool(r2),
                 "R3_earned": bool(r3), "R4_distinct_from_flat": bool(r4)},
        "r1_per_seed": {str(s): bool(r1_per[s]) for s in SEEDS},
        "r2_per_seed": {str(s): bool(r2_per[s]) for s in SEEDS},
        "r3_per_seed": {str(s): bool(r3_per[s]) for s in SEEDS},
        "r4_per_seed": {str(s): bool(r4_per[s]) for s in SEEDS},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n<=8)",
    }
    print("\nRESULT_JSON=" + json.dumps(out))
    return out


if __name__ == "__main__":
    main()
