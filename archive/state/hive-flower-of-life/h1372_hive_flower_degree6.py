#!/usr/bin/env python3
# H_1372 — hive-flower-degree6: TRUE 2-D hexagonal Flower-of-Life lattice (DEGREE-6 overlap).
# slug: hive_flower_degree6   seeds = [1317,1318,1319]  (SAME hard hive/topology family as H_1371/H_1356).
#
# THE WALL (c16 / a_break_the_wall — break with the RIGHT geometry, NOT tune-to-green):
# H_1371 (🧱 OVERLAP_BELOW_CENTRALIZED) tested distributed circle-overlap but used RING adjacency =
# DEGREE-2 (each cell overlaps only its 2 ring neighbors). The user's ACTUAL idea is the FLOWER-OF-LIFE:
# a 2-D hexagonal packing where a CENTER circle is overlapped by ~6 surrounding circles (degree-6; the
# user said "원 하나에 다른 원 4개 정도 들어온다" — degree >= 4, NOT degree-2). H_1371's own agent flagged
# the ring undertests the geometry. So the H_1371 wall MAY be the WRONG METHOD (degree-2 chain), not a
# true ceiling. This round runs the RIGHT geometry: a center cell with DEGREE-6 distributed overlap.
#
# THE GEOMETRY: natural Flower-of-Life UNIT = 7 circles = ONE center (cell 0) + 6 ring (cells 1..6) on a
# hexagon. N_TOT=7 (n<=8 keeps faithful MIP EXACT; size change 6->7 vs H_1371 noted, a_scale_honest_scope).
#   - 6 SPOKE edges: center(0)-ring(k)      => CENTER has DEGREE 6 (overlapped by all 6 neighbors).
#   - 6 RIM   edges: ring(k)-ring(k+1)       => hexagon cycle among the 6 ring cells.
#   => 12 edges. center degree=6, ring degree=3. mean degree 24/7 ≈ 3.43.
#   (Optional NON-GATING B_overlap_d4: + 6 hex diagonals ring(k)-ring(k+2) → ring degree 4, brackets "~4".)
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Φ — emits salience only.
#
# Substrate MATCHED to H_1371/H_1356/H_1320/H_1283 (ONLY the overlap topology/degree differs between arms):
# leaky linear recurrent units LEAK=0.55 GAIN=0.30 W_IN=0.5, dim-8 state, T=64 ticks. NO inter-cell
# recurrent coupling — the ONLY cross-cell sharing is the SHARED-INPUT overlap structure. OVERLAP_W=0.6.
#
# FROZEN BARS (.verdicts/1372_hive_flower_degree6/FREEZE.txt — GREEN iff R1 ∧ R2 ∧ R3):
#   R1 LIFT              : Φ(B_overlap) − Φ(A_independent)  >= MARGIN(0.02)  on ALL 3 seeds.
#   R2 BEATS-CENTRALIZED : Φ(B_overlap) − Φ(CENTRALIZED)    >  0            on >= 2/3 seeds (LOAD-BEARING).
#   R3 EARNED            : Φ(SHUFFLE)   <= Φ(A_independent) + TOL(0.02)     on ALL 3 seeds.
# seeds [1317,1318,1319]. $0 CPU-local. frozen-first.

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS    = [1317, 1318, 1319]
N_TOT    = 7          # center + 6 ring = natural Flower-of-Life unit (n<=8 keeps faithful IIT4 MIP exact)
DIM      = 8          # per-unit state vector dim (H_1283)
T        = 64         # ticks (H_1283)
GAIN     = 0.30       # per-unit update gain (H_1283)
LEAK     = 0.55       # state self-retention (H_1283)
W_IN     = 0.5        # input weight (H_1283)
NBINS    = 8          # IIT4 MI estimator bins (H_1283)

OVERLAP_W = 0.6       # H_1356 W_CONN hive coupling strength (reused verbatim) — the per-edge overlap weight
MARGIN    = 0.02      # IDENTICAL faithful-Φ margin H_1283/H_1317/H_1320/H_1356/H_1371 froze (NOT moved)
TOL       = 0.02

# FLOWER-OF-LIFE adjacency. cell 0 = CENTER, cells 1..6 = ring (hexagon).
RING = [1, 2, 3, 4, 5, 6]
SPOKE_EDGES = [(0, k) for k in RING]                       # center overlaps each ring cell -> center deg 6
RIM_EDGES   = [(RING[i], RING[(i + 1) % 6]) for i in range(6)]  # ring hexagon cycle
EDGES       = SPOKE_EDGES + RIM_EDGES                      # 12 undirected edges (degree-6 at center)
# diagonal edges (NON-GATING d4 diagnostic): ring k overlaps ring k+2 -> ring degree 4
DIAG_EDGES  = [(RING[i], RING[(i + 2) % 6]) for i in range(6)]
EDGES_D4    = EDGES + DIAG_EDGES                           # 18 edges (ring deg 4, center deg 6)

def incident(edges):
    return {i: [e for e, (a, b) in enumerate(edges) if a == i or b == i] for i in range(N_TOT)}
INC    = incident(EDGES)        # incident edges per cell (gating geometry)
INC_D4 = incident(EDGES_D4)     # for the d4 diagnostic
DEG    = {i: len(INC[i]) for i in range(N_TOT)}            # center=6, ring=3

HEXA      = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL  = os.path.join(HEXA_ROOT, "stdlib/consciousness/iit4/faithful_phi.hexa")


def build_inputs(seed, arm):
    """Per-cell input streams (N_TOT, T, DIM) for an arm.

    A_independent (FLOOR)   : cell i reads ONLY its private stream (no overlap).
    B_overlap   (DEGREE-6)  : cell i reads private + OVERLAP_W * (sum of its distinct incident per-EDGE
                              latents). CENTER sums its 6 spoke latents (degree-6); each ring cell sums
                              its 3 (2 rim + 1 spoke). Each L_e shared by EXACTLY the 2 cells on edge e
                              (distributed Flower-of-Life overlap — NO single source read by all).
    CENTRALIZED             : cell i reads private + (DEG[i]*OVERLAP_W) * F, ONE common founder F read by
                              ALL 7 cells. PER-CELL shared WEIGHT MATCHED to B (deg(i)*OVERLAP_W), so the
                              only difference vs B is DISTRIBUTION (one global source) not total energy.
    SHUFFLE                 : same per-cell shared count(=deg(i)) & weight(OVERLAP_W) as B, BUT each cell
                              independently re-draws the latent on each incident edge from a random
                              permutation → the two cells on an edge no longer read the SAME latent →
                              the consistent pairwise FoL lattice is destroyed (coincidence broken).
    B_overlap_d4 (NON-GATE) : as B_overlap but on EDGES_D4 (ring degree 4) — brackets the user's "~4".
    """
    rng = np.random.default_rng(seed)
    priv = rng.standard_normal((N_TOT, T, DIM)) * 0.8                  # per-cell private streams
    edge_lat = rng.standard_normal((len(EDGES), T, DIM)) * 0.8         # per-EDGE distinct shared latents (gating)
    diag_lat = rng.standard_normal((len(DIAG_EDGES), T, DIM)) * 0.8    # extra latents for the d4 diagonals
    founder  = rng.standard_normal((T, DIM)) * 0.8                     # single global founder F (CENTRALIZED)

    inp = np.zeros((N_TOT, T, DIM))

    if arm == "A_independent":
        for i in range(N_TOT):
            inp[i] = priv[i]
        return inp

    if arm == "B_overlap":
        for i in range(N_TOT):
            shared = np.zeros((T, DIM))
            for e in INC[i]:                       # this cell's incident FoL edges (center: 6, ring: 3)
                shared += edge_lat[e]              # the DISTINCT pairwise overlap region
            inp[i] = priv[i] + OVERLAP_W * shared
        return inp

    if arm == "CENTRALIZED":
        for i in range(N_TOT):
            inp[i] = priv[i] + (DEG[i] * OVERLAP_W) * founder  # weight-matched single global founder
        return inp

    if arm == "SHUFFLE":
        for i in range(N_TOT):
            perm = rng.permutation(len(EDGES))
            shared = np.zeros((T, DIM))
            for k, e in enumerate(INC[i]):
                shared += edge_lat[perm[k]]        # randomly-reassigned latent (broken FoL lattice)
            inp[i] = priv[i] + OVERLAP_W * shared
        return inp

    if arm == "B_overlap_d4":
        all_lat = np.concatenate([edge_lat, diag_lat], axis=0)   # 18 latents for EDGES_D4
        for i in range(N_TOT):
            shared = np.zeros((T, DIM))
            for e in INC_D4[i]:
                shared += all_lat[e]
            inp[i] = priv[i] + OVERLAP_W * shared
        return inp

    raise ValueError(arm)


def evolve(inputs, seed):
    """Leaky linear recurrent substrate (H_1283/H_1320/H_1356/H_1371 unit dynamics), N_TOT cells, NO
    inter-cell recurrent coupling — the ONLY cross-cell sharing is through the SHARED INPUT structure
    (the overlap). Returns salience traj (N_TOT, T)."""
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
                             capture_output=True, text=True, timeout=900)
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
    O = (n-2)*TC(X) - sum_i TC(X \\ x_i). O>0 redundancy / O<0 synergy. numpy ESTIMATE only — NOT a gate."""
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


# GATING arms (B_overlap_d4 is NON-GATING diagnostic, scored separately)
ARMS = ("A_independent", "B_overlap", "CENTRALIZED", "SHUFFLE")


def main():
    print("H_1372 hive-flower-degree6: TRUE 2-D Flower-of-Life (DEGREE-6) — faithful-IIT4 collective-Φ")
    print(f"N_TOT={N_TOT} (center+6ring) edges={len(EDGES)} center_deg={DEG[0]} ring_deg={DEG[1]} dim={DIM} ticks={T} seeds={SEEDS}")
    print(f"OVERLAP_W={OVERLAP_W}  faithful IIT4 Φ (exact MIP-EI, n=7); MARGIN={MARGIN} TOL={TOL}")
    print("=" * 92)

    phi = {}; oinfo = {}; phi_d4 = {}
    for seed in SEEDS:
        phi[seed] = {}; oinfo[seed] = {}
        for arm in ARMS:
            traj = build_arm(seed, arm)
            p = faithful_phi(traj, f"{arm}_s{seed}")
            o = o_information(traj)
            phi[seed][arm] = p; oinfo[seed][arm] = o
            print(f"  seed {seed} {arm:>14}: Φ={p}   O-info={o:+.4f}")
        # NON-GATING d4 diagnostic
        traj_d4 = build_arm(seed, "B_overlap_d4")
        phi_d4[seed] = faithful_phi(traj_d4, f"B_overlap_d4_s{seed}")
        print(f"  seed {seed} {'B_overlap_d4':>14}: Φ={phi_d4[seed]}   (NON-GATING ring-deg4 diagnostic)")
        print("-" * 92)

    def P(s, a): return phi[s][a]

    # R1 LIFT: Φ(B_overlap) − Φ(A_independent) >= MARGIN, ALL seeds
    r1_per = {s: (P(s,"B_overlap") is not None and P(s,"A_independent") is not None
                  and P(s,"B_overlap") - P(s,"A_independent") >= MARGIN) for s in SEEDS}
    r1 = all(r1_per.values())
    # R2 BEATS-CENTRALIZED: Φ(B_overlap) − Φ(CENTRALIZED) > 0 on >= 2/3 seeds (LOAD-BEARING)
    r2_per = {s: (P(s,"B_overlap") is not None and P(s,"CENTRALIZED") is not None
                  and P(s,"B_overlap") - P(s,"CENTRALIZED") > 0.0) for s in SEEDS}
    n_r2 = sum(r2_per.values())
    r2 = n_r2 >= 2
    # R3 EARNED: Φ(SHUFFLE) <= Φ(A_independent) + TOL, ALL seeds
    r3_per = {s: (P(s,"SHUFFLE") is not None and P(s,"A_independent") is not None
                  and P(s,"SHUFFLE") <= P(s,"A_independent") + TOL) for s in SEEDS}
    r3 = all(r3_per.values())

    n_r1, n_r3 = sum(r1_per.values()), sum(r3_per.values())
    green = r1 and r2 and r3

    if green:
        verdict = "GREEN_DEGREE6_ESCAPES_REDUNDANCY"
    elif n_r2 == 0:
        verdict = "TERMINAL_CEILING_DEGREE6_BELOW_CENTRALIZED"
    elif not r2:
        verdict = "OVERLAP_NOT_BEAT_CENTRALIZED"
    elif not r1:
        verdict = "FLOWER_OVERLAP_NULL"
    elif not r3:
        verdict = "WALL_NOT_EARNED"
    else:
        verdict = "PARTIAL"

    print("=" * 92)
    print(f"R1 LIFT             (Φ(B_overlap) − Φ(A_independent) >= {MARGIN} EVERY seed): {'PASS' if r1 else 'FAIL'}")
    for s in SEEDS:
        d = None if (P(s,"B_overlap") is None or P(s,"A_independent") is None) else round(P(s,"B_overlap")-P(s,"A_independent"),4)
        print(f"     seed {s}: Φ_overlap={P(s,'B_overlap')} Φ_floor={P(s,'A_independent')} lift={d}  {'PASS' if r1_per[s] else 'FAIL'}")
    print(f"R2 BEATS-CENTRALIZED (Φ(B_overlap) − Φ(CENTRALIZED) > 0 on >= 2/3 seeds): {'PASS' if r2 else 'FAIL'}  ({n_r2}/3)")
    for s in SEEDS:
        d = None if (P(s,"B_overlap") is None or P(s,"CENTRALIZED") is None) else round(P(s,"B_overlap")-P(s,"CENTRALIZED"),4)
        print(f"     seed {s}: Φ_overlap={P(s,'B_overlap')} Φ_central={P(s,'CENTRALIZED')} gap={d}  {'PASS' if r2_per[s] else 'FAIL'}")
    print(f"R3 EARNED            (Φ(SHUFFLE) <= Φ(A_independent) + {TOL} EVERY seed): {'PASS' if r3 else 'FAIL'}")
    for s in SEEDS:
        print(f"     seed {s}: Φ_shuffle={P(s,'SHUFFLE')} Φ_floor={P(s,'A_independent')}  {'PASS' if r3_per[s] else 'FAIL'}")
    print(f"\nNON-GATING d4 diagnostic (ring degree 4, brackets user's '~4'):")
    for s in SEEDS:
        gap = None if (phi_d4[s] is None or P(s,'CENTRALIZED') is None) else round(phi_d4[s]-P(s,'CENTRALIZED'),4)
        print(f"     seed {s}: Φ_d4={phi_d4[s]} Φ_overlap_d3={P(s,'B_overlap')} Φ_central={P(s,'CENTRALIZED')} (d4−central)={gap}")
    print(f"\nO-INFO shift (B_overlap vs CENTRALIZED; O<0=synergy O>0=redundancy):")
    for s in SEEDS:
        ob, oc = oinfo[s]["B_overlap"], oinfo[s]["CENTRALIZED"]
        print(f"     seed {s}: O(B_overlap)={ob:+.4f} O(CENTRALIZED)={oc:+.4f} shift(B−C)={ob-oc:+.4f}")
    print(f"\nVERDICT: {verdict}  (R1 {n_r1}/3, R2 {n_r2}/3, R3 {n_r3}/3)")

    out = {
        "id": "H_1372", "slug": "hive_flower_degree6", "verdict": verdict,
        "seeds": SEEDS, "N_tot": N_TOT, "edges": EDGES, "center_degree": DEG[0], "ring_degree": DEG[1],
        "dim": DIM, "ticks": T, "overlap_w": OVERLAP_W, "margin": MARGIN, "tol": TOL,
        "phi_faithful_iit4": {str(s): {a: phi[s][a] for a in ARMS} for s in SEEDS},
        "phi_d4_nongating": {str(s): phi_d4[s] for s in SEEDS},
        "o_information": {str(s): {a: oinfo[s][a] for a in ARMS} for s in SEEDS},
        "bars": {"R1_lift": bool(r1), "R2_beats_centralized": bool(r2), "R3_earned": bool(r3)},
        "r1_per_seed": {str(s): bool(r1_per[s]) for s in SEEDS},
        "r2_per_seed": {str(s): bool(r2_per[s]) for s in SEEDS},
        "r3_per_seed": {str(s): bool(r3_per[s]) for s in SEEDS},
        "n_r1": n_r1, "n_r2": n_r2, "n_r3": n_r3,
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n=7)",
    }
    print("\nRESULT_JSON=" + json.dumps(out))
    return out


if __name__ == "__main__":
    main()
