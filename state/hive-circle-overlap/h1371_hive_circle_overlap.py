#!/usr/bin/env python3
# H_1371 — hive-circle-overlap: distributed circle-overlap (Flower-of-Life / hexagonal packing) topology
# slug: hive-circle-overlap   seeds = [1317,1318,1319]  (hard hive/topology family; matched to H_1356).
#
# THE WALL (c16 / a_break_the_wall): the hive collective-Φ arc closed 🧱 across 4 levers (strong hub
# H_1356, weak/decorrelated H_1363, nonlinear-gate H_1370). H_1370's load-bearing diagnosis: the
# redundancy ceiling IS THE SHARED-INPUT STRUCTURE — ALL daughters read ONE common founder, so that
# single source dominates the faithful MIP → reducible → Φ bounded. EVERY prior hive arm had a SINGLE
# shared founder.
#
# THE NEW ANGLE (a_no_llm_frame_trap, c15 — geometric topology / biological packing; user-proposed):
# a CIRCLE-OVERLAP / Flower-of-Life packing. Arrange cells (circles) so each overlaps ~4 neighbors, and
# crucially EACH overlap is a DIFFERENT local region (distributed pairwise sharing), NOT one global
# shared founder. Like a hexagonal lattice / overlapping retinal-cortical receptive fields: every PAIR
# of adjacent cells shares a DISTINCT lens (a per-EDGE shared latent), no single source read by all →
# the redundancy is distributed across distinct pairwise overlaps (potentially SYNERGISTIC).
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Φ — it only emits the
# per-unit salience (state-energy) trajectory; the hexa engine computes Φ. NO proxy.
#
# Substrate MATCHED to H_1356/H_1320/H_1283 (only the OVERLAP TOPOLOGY differs between arms):
# leaky linear recurrent units, LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit private input, dim-8 state,
# T=64 ticks. N_TOT=6 cells (n<=8 keeps faithful MIP EXACT) on a HEXAGON RING (6-cycle). Each cell = 1
# unit; per-unit salience = state energy <s_i,s_i>. OVERLAP_W=0.6 (= W_CONN H_1356, reused verbatim).
#
# FROZEN BARS (see .verdicts/1371_hive_circle_overlap/H_1371_FREEZE.txt — GREEN iff R1 ∧ R2 ∧ R3):
#   R1 LIFT             : Φ(B_overlap) − Φ(A_independent)  >= MARGIN(0.02) on ALL 3 seeds.
#   R2 BEATS-CENTRALIZED: Φ(B_overlap) − Φ(CENTRALIZED)    >  0           on ALL 3 seeds.
#   R3 EARNED           : Φ(SHUFFLE)   <= Φ(A_independent) + TOL(0.02)    on ALL 3 seeds.
# seeds [1317,1318,1319]. $0 CPU-local. frozen-first.

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS    = [1317, 1318, 1319]
N_TOT    = 6          # 6 cells on a hexagon ring (n<=8 keeps faithful IIT4 MIP exact)
DIM      = 8          # per-unit state vector dim (H_1283)
T        = 64         # ticks (H_1283)
GAIN     = 0.30       # per-unit update gain (H_1283)
LEAK     = 0.55       # state self-retention (H_1283)
W_IN     = 0.5        # input weight (H_1283)
NBINS    = 8          # IIT4 MI estimator bins (H_1283)

OVERLAP_W = 0.6       # H_1356 W_CONN hive coupling strength (reused verbatim) — the overlap weight
MARGIN    = 0.02      # IDENTICAL faithful-Φ margin H_1283/H_1317/H_1320/H_1356 froze (NOT moved)
TOL       = 0.02

# HEXAGON RING: cell i neighbors {i-1,i+1} mod 6. 6 undirected edges = the 6-cycle.
EDGES = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]
N_EDGE = len(EDGES)
# incident edges per cell (each cell touches exactly 2 ring edges)
INC = {i: [e for e,(a,b) in enumerate(EDGES) if a==i or b==i] for i in range(N_TOT)}

HEXA      = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL  = os.path.join(HEXA_ROOT, "stdlib/consciousness/iit4/faithful_phi.hexa")


def build_inputs(seed, arm):
    """Build per-cell input streams (N_TOT, T, DIM) for an arm.

    A_independent (FLOOR) : cell i reads ONLY its private stream (no overlap).
    B_overlap             : cell i reads private + OVERLAP_W * (sum of its 2 distinct per-EDGE latents);
                            each edge-latent L_e is shared by EXACTLY the 2 cells on edge e (distributed
                            pairwise sharing — NO single source read by all). This is the circle-overlap.
    CENTRALIZED           : cell i reads private + (2*OVERLAP_W) * F, ONE common founder F read by ALL 6
                            cells (the single-shared-founder ceiling every prior hive arm had). Per-cell
                            shared WEIGHT matched to B (2 edges * OVERLAP_W == 2*OVERLAP_W).
    SHUFFLE               : same per-cell shared energy as B (each cell reads 2 edge-latents at OVERLAP_W)
                            BUT the latent on each incident edge is independently re-drawn PER CELL from a
                            random permutation, so the two cells on an edge no longer read the SAME latent
                            → the consistent pairwise-shared lattice structure is destroyed.
    """
    rng = np.random.default_rng(seed)
    priv = rng.standard_normal((N_TOT, T, DIM)) * 0.8        # per-cell private streams
    edge_lat = rng.standard_normal((N_EDGE, T, DIM)) * 0.8   # per-EDGE distinct shared latents L_e
    founder  = rng.standard_normal((T, DIM)) * 0.8           # single global founder F (CENTRALIZED)

    inp = np.zeros((N_TOT, T, DIM))

    if arm == "A_independent":
        for i in range(N_TOT):
            inp[i] = priv[i]
        return inp

    if arm == "B_overlap":
        for i in range(N_TOT):
            shared = np.zeros((T, DIM))
            for e in INC[i]:                                 # exactly 2 incident edges
                shared += edge_lat[e]                        # the DISTINCT pairwise overlap region
            inp[i] = priv[i] + OVERLAP_W * shared
        return inp

    if arm == "CENTRALIZED":
        for i in range(N_TOT):
            inp[i] = priv[i] + (2.0 * OVERLAP_W) * founder   # weight-matched single global founder
        return inp

    if arm == "SHUFFLE":
        # break the pairwise coincidence: each cell independently permutes which latent sits on its
        # incident edges, so two cells on an edge generally read DIFFERENT latents (structure destroyed),
        # while keeping the same count (2) and weight (OVERLAP_W) of shared inputs per cell.
        for i in range(N_TOT):
            perm = rng.permutation(N_EDGE)
            shared = np.zeros((T, DIM))
            for k, e in enumerate(INC[i]):
                shared += edge_lat[perm[k]]                  # randomly-reassigned latent (broken lattice)
            inp[i] = priv[i] + OVERLAP_W * shared
        return inp

    raise ValueError(arm)


def evolve(inputs, seed):
    """Leaky linear recurrent substrate (H_1283/H_1320/H_1356 unit dynamics), N_TOT cells, NO inter-cell
    recurrent coupling — the ONLY cross-cell sharing is through the SHARED INPUT structure (the overlap),
    exactly matching the H_1356 'redundancy via shared input' design. Returns salience traj (N_TOT, T)."""
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
    Inlines the trajectory as farr_set calls, calls iit4_faithful_phi(state, n, dim=T, n_bins)."""
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
    """O-information diagnostic (NON-GATING) on the per-unit salience time-series.
    Gaussian entropy h(X) = 0.5*logdet(2*pi*e*Cov). TC(X)=sum h(x_i) - h(X).
    O = (n-2)*TC(X) - sum_i TC(X \\ x_i). O>0 redundancy-dominated, O<0 synergy-dominated.
    numpy ESTIMATE only — does NOT gate the verdict."""
    X = traj_units  # (n, T)
    n = X.shape[0]
    Xc = X - X.mean(axis=1, keepdims=True)
    # guard against degenerate variance
    std = Xc.std(axis=1, keepdims=True)
    std[std < 1e-12] = 1e-12
    Z = Xc / std
    def h_gauss(M):
        # M: (k, T) rows = vars. entropy up to additive const: 0.5*logdet(Cov+eps I)
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


ARMS = ("A_independent", "B_overlap", "CENTRALIZED", "SHUFFLE")


def main():
    print("H_1371 hive-circle-overlap: distributed circle-overlap (Flower-of-Life) — faithful-IIT4 collective-Φ")
    print(f"N_TOT={N_TOT} hexagon-ring edges={EDGES} dim={DIM} ticks={T} seeds={SEEDS}")
    print(f"OVERLAP_W={OVERLAP_W}  faithful IIT4 Φ (exact MIP-EI, n<=8); MARGIN={MARGIN} TOL={TOL}")
    print("=" * 92)

    phi = {}   # phi[seed][arm]
    oinfo = {} # oinfo[seed][arm]
    for seed in SEEDS:
        phi[seed] = {}; oinfo[seed] = {}
        for arm in ARMS:
            traj = build_arm(seed, arm)
            p = faithful_phi(traj, f"{arm}_s{seed}")
            o = o_information(traj)
            phi[seed][arm] = p; oinfo[seed][arm] = o
            print(f"  seed {seed} {arm:>14}: Φ={p}   O-info={o:+.4f}")
        print("-" * 92)

    def P(s, a): return phi[s][a]

    # R1 LIFT: Φ(B_overlap) − Φ(A_independent) >= MARGIN, all seeds
    r1_per = {s: (P(s,"B_overlap") is not None and P(s,"A_independent") is not None
                  and P(s,"B_overlap") - P(s,"A_independent") >= MARGIN) for s in SEEDS}
    r1 = all(r1_per.values())
    # R2 BEATS-CENTRALIZED: Φ(B_overlap) − Φ(CENTRALIZED) > 0, all seeds
    r2_per = {s: (P(s,"B_overlap") is not None and P(s,"CENTRALIZED") is not None
                  and P(s,"B_overlap") - P(s,"CENTRALIZED") > 0.0) for s in SEEDS}
    r2 = all(r2_per.values())
    # R3 EARNED: Φ(SHUFFLE) <= Φ(A_independent) + TOL, all seeds
    r3_per = {s: (P(s,"SHUFFLE") is not None and P(s,"A_independent") is not None
                  and P(s,"SHUFFLE") <= P(s,"A_independent") + TOL) for s in SEEDS}
    r3 = all(r3_per.values())

    n_r1, n_r2, n_r3 = sum(r1_per.values()), sum(r2_per.values()), sum(r3_per.values())
    green = r1 and r2 and r3

    if green:
        verdict = "GREEN_ESCAPES_REDUNDANCY"
    elif r1 and not r2:
        verdict = "PARTIAL_OVERLAP_NOT_BEAT_CENTRALIZED"
    elif n_r1 == 2 or n_r2 == 2:
        verdict = "SEED_FRAGILE"
    elif not r3:
        verdict = "WALL_NOT_EARNED"
    elif not r1:
        verdict = "CIRCLE_OVERLAP_NULL"
    else:
        verdict = "PARTIAL"

    print("=" * 92)
    print(f"R1 LIFT             (Φ(B_overlap) − Φ(A_independent) >= {MARGIN} EVERY seed): {'PASS' if r1 else 'FAIL'}")
    for s in SEEDS:
        d = None if (P(s,"B_overlap") is None or P(s,"A_independent") is None) else round(P(s,"B_overlap")-P(s,"A_independent"),4)
        print(f"     seed {s}: Φ_overlap={P(s,'B_overlap')} Φ_floor={P(s,'A_independent')} lift={d}  {'PASS' if r1_per[s] else 'FAIL'}")
    print(f"R2 BEATS-CENTRALIZED (Φ(B_overlap) − Φ(CENTRALIZED) > 0 EVERY seed): {'PASS' if r2 else 'FAIL'}")
    for s in SEEDS:
        d = None if (P(s,"B_overlap") is None or P(s,"CENTRALIZED") is None) else round(P(s,"B_overlap")-P(s,"CENTRALIZED"),4)
        print(f"     seed {s}: Φ_overlap={P(s,'B_overlap')} Φ_central={P(s,'CENTRALIZED')} gap={d}  {'PASS' if r2_per[s] else 'FAIL'}")
    print(f"R3 EARNED            (Φ(SHUFFLE) <= Φ(A_independent) + {TOL} EVERY seed): {'PASS' if r3 else 'FAIL'}")
    for s in SEEDS:
        print(f"     seed {s}: Φ_shuffle={P(s,'SHUFFLE')} Φ_floor={P(s,'A_independent')}  {'PASS' if r3_per[s] else 'FAIL'}")
    print(f"\nO-INFO shift (B_overlap vs CENTRALIZED; O<0=synergy O>0=redundancy):")
    for s in SEEDS:
        ob, oc = oinfo[s]["B_overlap"], oinfo[s]["CENTRALIZED"]
        print(f"     seed {s}: O(B_overlap)={ob:+.4f} O(CENTRALIZED)={oc:+.4f} shift(B−C)={ob-oc:+.4f}")
    print(f"\nVERDICT: {verdict}  (R1 {n_r1}/3, R2 {n_r2}/3, R3 {n_r3}/3)")

    out = {
        "id": "H_1371", "slug": "hive-circle-overlap", "verdict": verdict,
        "seeds": SEEDS, "N_tot": N_TOT, "edges": EDGES, "dim": DIM, "ticks": T,
        "overlap_w": OVERLAP_W, "margin": MARGIN, "tol": TOL,
        "phi_faithful_iit4": {str(s): {a: phi[s][a] for a in ARMS} for s in SEEDS},
        "o_information": {str(s): {a: oinfo[s][a] for a in ARMS} for s in SEEDS},
        "bars": {"R1_lift": bool(r1), "R2_beats_centralized": bool(r2), "R3_earned": bool(r3)},
        "r1_per_seed": {str(s): bool(r1_per[s]) for s in SEEDS},
        "r2_per_seed": {str(s): bool(r2_per[s]) for s in SEEDS},
        "r3_per_seed": {str(s): bool(r3_per[s]) for s in SEEDS},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n<=8)",
    }
    print("\nRESULT_JSON=" + json.dumps(out))
    return out


if __name__ == "__main__":
    main()
