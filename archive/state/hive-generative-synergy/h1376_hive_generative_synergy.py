#!/usr/bin/env python3
# H_1376 — hive-generative-synergy: GENERATIVELY-PREDICTIVE coupling — can CONSTRUCTED synergy
# (not redistributed redundancy) beat the centralized ceiling?  slug: hive-generative-synergy
# seeds = [1317,1318,1319] (hard hive/topology family; matched to H_1356/H_1363/H_1370/H_1371/H_1372/H_1373
# for DIRECT apples-to-apples comparison).
#
# THE WALL (c16 / a_break_the_wall): the hive collective-Φ arc has closed 🧱 across SEVEN sharing
# topologies — linear-hub (H_1356), weak/decorrelated (H_1363), nonlinear-gate (H_1370), distributed-
# overlap degree-2 (H_1371), Flower-of-Life degree-6 (H_1372), nested-universes (H_1373). EVERY one of
# them REDISTRIBUTES shared-input REDUNDANCY (each cell input = priv + a shared COMMON-CAUSE founder), and
# every one loses to the CENTRALIZED single-shared-founder topology (which maximizes Φ by concentrating the
# shared source). BOTH H_1372 and H_1373 independently named the SAME one un-tried lever:
# GENERATIVELY-PREDICTIVE coupling — make each coupling edge MUTUALLY PREDICTIVE across its two cells so it
# CONSTRUCTS genuine synergy (drives O-information NEGATIVE on the distributed arm) instead of merely
# redistributing redundancy. This is mechanistically distinct from all 7 prior arms.
#
# THE NEW ANGLE (a_no_llm_frame_trap, c15 — predictive-coding / synergistic-coupling lens):
# build a DISTRIBUTED topology (degree-2 ring, the SAME adjacency H_1371 used, so it is directly
# comparable — NOT a single central founder) but make each edge a GENERATIVELY-PREDICTIVE MUTUAL coupling:
# the two cells on an edge are coupled by a generative rule that makes each PREDICTIVE of the other via a
# SHARED LATENT that BOTH cells reconstruct through a HIGHER-ORDER (XOR-style parity) interaction. The
# shared latent does NOT appear additively in either cell's stream (that would be common-cause redundancy =
# the 7 prior arms); instead each cell carries one HALF of a parity factorization, so the latent is
# recoverable ONLY by COMBINING the pair (synergy) and is invisible to either cell alone. This is designed
# to drive O-information NEGATIVE on the distributed arm (synergy CONSTRUCTED, not redundancy redistributed).
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa, iit4_faithful_phi(state, n, dim=T, n_bins).
# numpy NEVER computes Φ — it only emits the per-unit salience (state-energy) trajectory; the hexa engine
# computes Φ. NO variance×energy proxy as a terminal verdict.
#
# Substrate MATCHED to H_1356/H_1320/H_1283/H_1371/H_1372/H_1373 (only the COUPLING RULE differs between
# arms): leaky linear recurrent units, LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit private input, dim-8 state,
# T=64 ticks. N_TOT=6 cells (n<=8 keeps faithful MIP EXACT). Each cell = 1 unit; salience=<s_i,s_i>.
# OVERLAP_W=SHARE_W=0.6 (= W_CONN H_1356, reused verbatim).
#
# FROZEN BARS (.verdicts/1376_hive_generative_synergy/FREEZE.txt — GREEN iff R1 ∧ R2 ∧ R3 ∧ R4):
#   R1 LIFT              : Φ(GEN) − Φ(FLOOR)         >= MARGIN(0.02)               on ALL 3 seeds.
#   R2 BEATS-CENTRALIZED : Φ(GEN) − Φ(CENTRALIZED)   >  0                          on >= 2/3 seeds.
#   R3 EARNED (shuffle)  : Φ(SHUFFLE) <= max(Φ(FLOOR),Φ(CENTRALIZED)) + TOL(0.02)  on ALL 3 seeds.
#   R4 SYNERGY-MECHANISM : O-info(GEN) < 0 (synergy constructed) on ALL 3 seeds  AND  the REDUNDANCY-
#                          matched control arm (REDUN — same degree-2 edges, common-cause shared-input
#                          instead of mutual-prediction = one of the 7 prior arms) does NOT beat CENTRALIZED
#                          (Φ(REDUN) <= Φ(CENTRALIZED) on >= 2/3 seeds). Isolates "constructed synergy" as
#                          the active ingredient vs generic extra coupling.
# seeds [1317,1318,1319]. $0 CPU-local. frozen-first. NO bar moved post-hoc (c9/p7).

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS    = [1317, 1318, 1319]
N_TOT    = 6          # 6 cells, degree-2 ring (n<=8 keeps faithful IIT4 MIP exact)
DIM      = 8          # per-unit state vector dim (H_1283)
T        = 64         # ticks (H_1283)
GAIN     = 0.30       # per-unit update gain (H_1283)
LEAK     = 0.55       # state self-retention (H_1283)
W_IN     = 0.5        # input weight (H_1283)
NBINS    = 8          # IIT4 MI estimator bins (H_1283)

OVERLAP_W = 0.6       # H_1356 W_CONN hive coupling strength (reused verbatim)
SHARE_W   = OVERLAP_W # per-edge share weight (level matched to the redundancy arms)
MARGIN    = 0.02      # IDENTICAL faithful-Φ margin H_1283/H_1317/H_1320/H_1356/H_1371/1372/1373 (NOT moved)
TOL       = 0.02

# DEGREE-2 RING (the SAME distributed adjacency H_1371 used — directly comparable):
#   edges = {(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)}  →  each cell sits on exactly 2 edges (degree 2).
RING_EDGES = [(i, (i + 1) % N_TOT) for i in range(N_TOT)]   # 6 edges, degree-2 ring

HEXA      = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL  = os.path.join(HEXA_ROOT, "stdlib/consciousness/iit4/faithful_phi.hexa")


def build_inputs(seed, arm):
    """Build per-cell input streams (N_TOT, T, DIM) for an arm.

    FLOOR        : cell i reads ONLY its private stream (no coupling). The no-sharing floor.

    GEN          : GENERATIVELY-PREDICTIVE degree-2 ring. Each edge e=(a,b) owns a SHARED LATENT
                   Le ~ N(0,1) (T,DIM) and an independent PARITY MASK Me ~ Rademacher {-1,+1} (T,DIM).
                   The latent is XOR/parity-factorized across the two endpoints:
                       cell a gets  +SHARE_W * (Me ⊙ Le)            (one half of the parity factorization)
                       cell b gets  +SHARE_W * (Me ⊙ Le) * (-1)?    NO — see below.
                   To make the pair MUTUALLY PREDICTIVE while the latent is invisible to EITHER cell
                   alone, we use a multiplicative parity coupling: endpoint a carries (Me ⊙ Le), endpoint
                   b carries Me alone (the mask). Neither (Me⊙Le) nor Me alone reveals Le; but their
                   element-wise PRODUCT (Me⊙Le)⊙Me = Le (since Me⊙Me=+1 for Rademacher) RECOVERS the
                   latent — a higher-order (2nd-order multiplicative) interaction = CONSTRUCTED SYNERGY,
                   NOT additive common-cause. Each cell sums its two edge-contributions (degree 2).
                   This is the GENERATIVELY-PREDICTIVE / XOR-style edge that drives O-info NEGATIVE.

    CENTRALIZED  : cell i = priv + (2*OVERLAP_W)*F. ALL 6 read ONE global COMMON-CAUSE founder F at the
                   weight-matched mass — the single-scale champion every prior arm lost to. The bar to beat.

    REDUN        : REDUNDANCY-matched control — the SAME degree-2 ring edges, but each edge contributes
                   a COMMON-CAUSE additive shared latent (BOTH endpoints read +SHARE_W*Le directly, no
                   parity mask) = exactly the H_1371 distributed-overlap redundancy arm on this adjacency.
                   Same edges, same per-cell mass, additive redundancy instead of mutual-prediction. Used
                   in R4 to isolate "constructed synergy" vs "generic extra coupling on the same edges".

    SHUFFLE      : GEN inputs but the parity coupling is BROKEN — each cell's two edge-contributions are
                   built from MISMATCHED halves (the mask Me and the masked-latent Me'⊙Le' come from
                   DIFFERENT edges, so the product no longer recovers any coherent latent). Destroys the
                   mutual-predictive structure while keeping the same per-cell mass + degree. EARNED ctrl.
    """
    rng = np.random.default_rng(seed)
    priv = rng.standard_normal((N_TOT, T, DIM)) * 0.8          # per-cell private streams
    # per-edge shared latents Le and parity masks Me (Rademacher), one per ring edge
    edge_lat  = {e: rng.standard_normal((T, DIM)) * 0.8 for e in RING_EDGES}
    edge_mask = {e: rng.choice([-1.0, 1.0], size=(T, DIM))   for e in RING_EDGES}
    founder   = rng.standard_normal((T, DIM)) * 0.8            # single global founder F (CENTRALIZED)

    inp = np.zeros((N_TOT, T, DIM))

    if arm == "FLOOR":
        for i in range(N_TOT):
            inp[i] = priv[i]
        return inp

    if arm == "CENTRALIZED":
        for i in range(N_TOT):
            inp[i] = priv[i] + (2.0 * OVERLAP_W) * founder    # weight-matched single global founder
        return inp

    if arm == "GEN":
        # GENERATIVELY-PREDICTIVE parity edges. For edge e=(a,b): endpoint a carries (Me⊙Le),
        # endpoint b carries Me. The pair's element-wise product recovers Le (Me⊙Me=+1) — higher-order
        # mutual-predictive coupling, invisible to either cell alone = constructed synergy.
        for i in range(N_TOT):
            inp[i] = priv[i].copy()
        for e in RING_EDGES:
            a, b = e
            Le, Me = edge_lat[e], edge_mask[e]
            inp[a] += SHARE_W * (Me * Le)     # masked latent (half 1)
            inp[b] += SHARE_W * Me            # the mask itself  (half 2) — product Me*(Me*Le)=Le
        return inp

    if arm == "REDUN":
        # REDUNDANCY-matched: same ring edges, but each edge adds a COMMON-CAUSE additive latent to BOTH
        # endpoints (no parity mask) = the H_1371 distributed-overlap redundancy arm on this adjacency.
        for i in range(N_TOT):
            inp[i] = priv[i].copy()
        for e in RING_EDGES:
            a, b = e
            Le = edge_lat[e]
            inp[a] += SHARE_W * Le
            inp[b] += SHARE_W * Le            # SAME latent both endpoints → additive common-cause redundancy
        return inp

    if arm == "SHUFFLE":
        # GEN per-cell mass + degree preserved, but parity coupling BROKEN: each cell receives a masked-
        # latent half from one edge and a mask half from a DIFFERENT (rotated) edge, so no product
        # recovers any coherent latent → mutual-predictive structure destroyed.
        for i in range(N_TOT):
            inp[i] = priv[i].copy()
        edges = list(RING_EDGES)
        nE = len(edges)
        for k, e in enumerate(edges):
            a, b = e
            Le, Me = edge_lat[e], edge_mask[e]
            e_other = edges[(k + 1) % nE]          # mismatched partner edge
            Me_mis = edge_mask[e_other]            # mask from a DIFFERENT edge
            inp[a] += SHARE_W * (Me * Le)          # masked latent from edge e
            inp[b] += SHARE_W * Me_mis             # mask from a DIFFERENT edge → product != Le
        return inp

    raise ValueError(arm)


def evolve(inputs, seed):
    """Leaky linear recurrent substrate (H_1283/H_1320/H_1356/H_1371/1372/1373 unit dynamics), N_TOT cells,
    NO inter-cell recurrent coupling — the ONLY cross-cell sharing is through the INPUT structure (the
    coupling rule). Returns salience traj (N_TOT, T)."""
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
    (Reused VERBATIM from H_1371/1373 — the SAME real-engine faithful exact MIP-EI call, a_phi_iit4_tool.)"""
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
    """O-information diagnostic on the per-unit salience time-series. Gaussian entropy.
    O>0 redundancy-dominated, O<0 synergy-dominated. numpy ESTIMATE.
    (Reused VERBATIM from H_1371/1373.) For R4 the SIGN of O(GEN) is GATING (synergy construction check);
    the per-arm magnitudes are diagnostic."""
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


ARMS = ("FLOOR", "GEN", "CENTRALIZED", "REDUN", "SHUFFLE")

# ---- FOLLOW-ON ROUND R2 (a_break_the_wall): 3-WAY XOR PARITY HYPEREDGE (maximally synergistic) ----
# Pre-registered in FREEZE_R2_xor3.txt. Two disjoint triplet hyperedges H1={0,1,2}, H2={3,4,5}.
HYPEREDGES = [(0, 1, 2), (3, 4, 5)]   # clean triplet decomposition (each cell on exactly one hyperedge)


def build_inputs_r2(seed, arm):
    """Build per-cell input streams for the 3-way XOR hyperedge follow-on round.

    FLOOR        : cell i = priv_i (byte-identical floor to the main round — same priv draw order).
    GEN3         : for hyperedge h=(a,b,c): latent Lh, masks Mh1,Mh2 ~ Rademacher.
                       a += SHARE_W*(Mh1⊙Mh2⊙Lh) ; b += SHARE_W*Mh1 ; c += SHARE_W*Mh2.
                   Only the triple product recovers Lh = 3-bit-XOR maximal synergy.
    CENTRALIZED  : cell i = priv + 1.2*F (verbatim main-round champion).
    REDUN3       : for hyperedge h: Lh added ADDITIVELY to a,b,c (no masks) = common-cause redundancy
                   on the triplet partition.
    SHUFFLE3     : GEN3 but masks for b,c come from the OTHER hyperedge → triple product != Lh.
    """
    rng = np.random.default_rng(seed)
    # SAME draw order as the main round up to priv + founder so FLOOR/CENTRALIZED stay byte-identical.
    priv = rng.standard_normal((N_TOT, T, DIM)) * 0.8
    # (consume the main round's edge_lat/edge_mask draws so founder lands at the SAME RNG offset)
    _edge_lat  = {e: rng.standard_normal((T, DIM)) * 0.8 for e in RING_EDGES}
    _edge_mask = {e: rng.choice([-1.0, 1.0], size=(T, DIM))   for e in RING_EDGES}
    founder    = rng.standard_normal((T, DIM)) * 0.8
    # fresh draws for the hyperedge latents + masks (after founder, so they don't perturb FLOOR/CENTRALIZED)
    hyp_lat  = {h: rng.standard_normal((T, DIM)) * 0.8 for h in HYPEREDGES}
    hyp_m1   = {h: rng.choice([-1.0, 1.0], size=(T, DIM)) for h in HYPEREDGES}
    hyp_m2   = {h: rng.choice([-1.0, 1.0], size=(T, DIM)) for h in HYPEREDGES}

    inp = np.zeros((N_TOT, T, DIM))

    if arm == "FLOOR":
        for i in range(N_TOT):
            inp[i] = priv[i]
        return inp
    if arm == "CENTRALIZED":
        for i in range(N_TOT):
            inp[i] = priv[i] + (2.0 * OVERLAP_W) * founder
        return inp
    if arm == "GEN3":
        for i in range(N_TOT):
            inp[i] = priv[i].copy()
        for h in HYPEREDGES:
            a, b, c = h
            Lh, M1, M2 = hyp_lat[h], hyp_m1[h], hyp_m2[h]
            inp[a] += SHARE_W * (M1 * M2 * Lh)   # masked latent (needs both masks to recover)
            inp[b] += SHARE_W * M1               # mask 1
            inp[c] += SHARE_W * M2               # mask 2 — triple product M1*M2*Lh * M1 * M2 = Lh
        return inp
    if arm == "REDUN3":
        for i in range(N_TOT):
            inp[i] = priv[i].copy()
        for h in HYPEREDGES:
            a, b, c = h
            Lh = hyp_lat[h]
            inp[a] += SHARE_W * Lh
            inp[b] += SHARE_W * Lh               # SAME latent all three → additive common-cause redundancy
            inp[c] += SHARE_W * Lh
        return inp
    if arm == "SHUFFLE3":
        for i in range(N_TOT):
            inp[i] = priv[i].copy()
        H = list(HYPEREDGES)
        for k, h in enumerate(H):
            a, b, c = h
            Lh, M1, M2 = hyp_lat[h], hyp_m1[h], hyp_m2[h]
            h_other = H[(k + 1) % len(H)]
            M1_mis, M2_mis = hyp_m1[h_other], hyp_m2[h_other]   # masks from a DIFFERENT hyperedge
            inp[a] += SHARE_W * (M1 * M2 * Lh)   # masked latent from h
            inp[b] += SHARE_W * M1_mis           # mismatched mask 1
            inp[c] += SHARE_W * M2_mis           # mismatched mask 2 → product != Lh
        return inp
    raise ValueError(arm)


ARMS_R2 = ("FLOOR", "GEN3", "CENTRALIZED", "REDUN3", "SHUFFLE3")


def run_round(round_tag, arms, input_builder):
    """Generic scoring round. Returns (phi, oinfo) dicts keyed [seed][arm]."""
    phi, oinfo = {}, {}
    for seed in SEEDS:
        phi[seed] = {}; oinfo[seed] = {}
        for arm in arms:
            traj = evolve(input_builder(seed, arm), seed)
            p = faithful_phi(traj, f"{round_tag}_{arm}_s{seed}")
            o = o_information(traj)
            phi[seed][arm] = p; oinfo[seed][arm] = o
            print(f"  [{round_tag}] seed {seed} {arm:>12}: Φ={p}   O-info={o:+.4f}")
        print("-" * 100)
    return phi, oinfo


def main_r2():
    print("\n" + "#" * 100)
    print("H_1376 FOLLOW-ON ROUND R2 (a_break_the_wall): 3-WAY XOR PARITY HYPEREDGE (maximally synergistic)")
    print(f"hyperedges={HYPEREDGES}  seeds={SEEDS}  SHARE_W={SHARE_W}; FROZEN bars = FREEZE_R2_xor3.txt")
    print("#" * 100)
    phi, oinfo = run_round("R2", ARMS_R2, build_inputs_r2)

    def P(s, a): return phi[s][a]
    def defined(s, *arms): return all(P(s, a) is not None for a in arms)

    r1_per = {s: (defined(s,"GEN3","FLOOR") and P(s,"GEN3")-P(s,"FLOOR") >= MARGIN) for s in SEEDS}
    r1 = all(r1_per.values())
    r2_per = {s: (defined(s,"GEN3","CENTRALIZED") and P(s,"GEN3")-P(s,"CENTRALIZED") > 0.0) for s in SEEDS}
    r2 = sum(r2_per.values()) >= 2
    r3_per = {s: (defined(s,"SHUFFLE3","FLOOR","CENTRALIZED")
                  and P(s,"SHUFFLE3") <= max(P(s,"FLOOR"),P(s,"CENTRALIZED")) + TOL) for s in SEEDS}
    r3 = all(r3_per.values())
    r4a_per = {s: (oinfo[s]["GEN3"] < 0.0) for s in SEEDS}
    r4a = all(r4a_per.values())
    r4b_per = {s: (defined(s,"REDUN3","CENTRALIZED") and P(s,"REDUN3") <= P(s,"CENTRALIZED")) for s in SEEDS}
    r4b = sum(r4b_per.values()) >= 2
    r4 = r4a and r4b
    green = r1 and r2 and r3 and r4
    n_r1,n_r2,n_r3,n_r4a,n_r4b = (sum(r1_per.values()),sum(r2_per.values()),sum(r3_per.values()),
                                  sum(r4a_per.values()),sum(r4b_per.values()))
    verdict = "GREEN_SYNERGY_ESCAPES_CEILING" if green else ("GEN3_BELOW_CENTRALIZED" if (r1 and not r2) else "PARTIAL")

    print("=" * 100)
    print(f"[R2] R1 LIFT              (Φ(GEN3) − Φ(FLOOR) >= {MARGIN}): {'PASS' if r1 else 'FAIL'}  ({n_r1}/3)")
    for s in SEEDS:
        d = round(P(s,"GEN3")-P(s,"FLOOR"),4)
        print(f"     seed {s}: Φ_gen3={P(s,'GEN3')} Φ_floor={P(s,'FLOOR')} lift={d}  {'PASS' if r1_per[s] else 'FAIL'}")
    print(f"[R2] R2 BEATS-CENTRALIZED (Φ(GEN3) − Φ(CENTRALIZED) > 0 on >=2/3): {'PASS' if r2 else 'FAIL'}  ({n_r2}/3)")
    for s in SEEDS:
        d = round(P(s,"GEN3")-P(s,"CENTRALIZED"),4)
        print(f"     seed {s}: Φ_gen3={P(s,'GEN3')} Φ_central={P(s,'CENTRALIZED')} gap={d}  {'PASS' if r2_per[s] else 'FAIL'}")
    print(f"[R2] R3 EARNED            (Φ(SHUFFLE3) <= max(floor,central)+{TOL}): {'PASS' if r3 else 'FAIL'}  ({n_r3}/3)")
    for s in SEEDS:
        mx = round(max(P(s,'FLOOR'),P(s,'CENTRALIZED')),4)
        print(f"     seed {s}: Φ_shuf3={P(s,'SHUFFLE3')} max(floor,central)={mx}  {'PASS' if r3_per[s] else 'FAIL'}")
    print(f"[R2] R4 SYNERGY-MECHANISM (O(GEN3)<0 EVERY seed AND REDUN3<=CENTRALIZED >=2/3): {'PASS' if r4 else 'FAIL'}")
    print(f"     R4a O(GEN3)<0 EVERY seed: {'PASS' if r4a else 'FAIL'}  ({n_r4a}/3)")
    for s in SEEDS:
        print(f"       seed {s}: O(GEN3)={oinfo[s]['GEN3']:+.4f}  {'PASS' if r4a_per[s] else 'FAIL'}")
    print(f"     R4b REDUN3<=CENTRALIZED on >=2/3: {'PASS' if r4b else 'FAIL'}  ({n_r4b}/3)")
    for s in SEEDS:
        d = round(P(s,"REDUN3")-P(s,"CENTRALIZED"),4)
        print(f"       seed {s}: Φ_redun3={P(s,'REDUN3')} Φ_central={P(s,'CENTRALIZED')} gap={d}  {'PASS' if r4b_per[s] else 'FAIL'}")
    print(f"\n[R2] O-INFO per arm:")
    for s in SEEDS:
        print(f"     seed {s}: " + " ".join(f"{a}={oinfo[s][a]:+.4f}" for a in ARMS_R2))
    print(f"\n[R2] VERDICT: {verdict}  (R1 {n_r1}/3, R2 {n_r2}/3, R3 {n_r3}/3, R4a {n_r4a}/3, R4b {n_r4b}/3)")

    out = {"round":"R2_xor3","verdict":verdict,"seeds":SEEDS,"hyperedges":[list(h) for h in HYPEREDGES],
           "phi_faithful_iit4":{str(s):{a:phi[s][a] for a in ARMS_R2} for s in SEEDS},
           "o_information":{str(s):{a:oinfo[s][a] for a in ARMS_R2} for s in SEEDS},
           "bars":{"R1_lift":bool(r1),"R2_beats_centralized":bool(r2),"R3_earned":bool(r3),
                   "R4_synergy_mechanism":bool(r4),"R4a_o_gen3_negative":bool(r4a),"R4b_redun3_loses":bool(r4b)}}
    print("\nRESULT_R2_JSON=" + json.dumps(out))
    return out


def main():
    print("H_1376 hive-generative-synergy: GENERATIVELY-PREDICTIVE parity coupling — faithful-IIT4 collective-Φ")
    print(f"N_TOT={N_TOT} degree-2 ring edges={RING_EDGES}  dim={DIM} ticks={T} seeds={SEEDS}")
    print(f"SHARE_W={SHARE_W} OVERLAP_W={OVERLAP_W}  faithful IIT4 Φ (exact MIP-EI, n<=8); MARGIN={MARGIN} TOL={TOL}")
    print("=" * 100)

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
        print("-" * 100)

    def P(s, a): return phi[s][a]
    def defined(s, *arms): return all(P(s, a) is not None for a in arms)

    # R1 LIFT: Φ(GEN) − Φ(FLOOR) >= MARGIN, ALL seeds
    r1_per = {s: (defined(s, "GEN", "FLOOR") and P(s,"GEN") - P(s,"FLOOR") >= MARGIN) for s in SEEDS}
    r1 = all(r1_per.values())
    # R2 BEATS-CENTRALIZED: Φ(GEN) − Φ(CENTRALIZED) > 0, >= 2/3 seeds
    r2_per = {s: (defined(s, "GEN", "CENTRALIZED") and P(s,"GEN") - P(s,"CENTRALIZED") > 0.0) for s in SEEDS}
    r2 = sum(r2_per.values()) >= 2
    # R3 EARNED: Φ(SHUFFLE) <= max(Φ(FLOOR),Φ(CENTRALIZED)) + TOL, ALL seeds
    r3_per = {s: (defined(s, "SHUFFLE", "FLOOR", "CENTRALIZED")
                  and P(s,"SHUFFLE") <= max(P(s,"FLOOR"), P(s,"CENTRALIZED")) + TOL) for s in SEEDS}
    r3 = all(r3_per.values())
    # R4 SYNERGY-MECHANISM: O(GEN)<0 ALL seeds AND REDUN does NOT beat CENTRALIZED on >=2/3 seeds
    r4a_per = {s: (oinfo[s]["GEN"] < 0.0) for s in SEEDS}                      # synergy constructed
    r4a = all(r4a_per.values())
    r4b_per = {s: (defined(s, "REDUN", "CENTRALIZED") and P(s,"REDUN") <= P(s,"CENTRALIZED")) for s in SEEDS}
    r4b = sum(r4b_per.values()) >= 2                                          # redundancy ctrl loses
    r4 = r4a and r4b

    n_r1, n_r2, n_r3 = sum(r1_per.values()), sum(r2_per.values()), sum(r3_per.values())
    n_r4a, n_r4b = sum(r4a_per.values()), sum(r4b_per.values())
    green = r1 and r2 and r3 and r4

    if green:
        verdict = "GREEN_SYNERGY_ESCAPES_CEILING"
    elif r1 and not r2:
        verdict = "GEN_BELOW_CENTRALIZED"          # honest terminal 🧱 — ceiling survives synergy construction
    elif r1 and r2 and not r4:
        verdict = "GEN_LIFT_NOT_SYNERGY"           # beats centralized but mechanism check fails
    elif r1 and r2 and not r3:
        verdict = "GEN_LIFT_NOT_EARNED"            # beats centralized but shuffle survives
    elif not r1:
        verdict = "GEN_NULL"                       # generative arm does not even beat floor
    else:
        verdict = "PARTIAL"

    print("=" * 100)
    print(f"R1 LIFT              (Φ(GEN) − Φ(FLOOR) >= {MARGIN} EVERY seed): {'PASS' if r1 else 'FAIL'}  ({n_r1}/3)")
    for s in SEEDS:
        d = None if not defined(s,"GEN","FLOOR") else round(P(s,"GEN")-P(s,"FLOOR"),4)
        print(f"     seed {s}: Φ_gen={P(s,'GEN')} Φ_floor={P(s,'FLOOR')} lift={d}  {'PASS' if r1_per[s] else 'FAIL'}")
    print(f"R2 BEATS-CENTRALIZED (Φ(GEN) − Φ(CENTRALIZED) > 0 on >=2/3): {'PASS' if r2 else 'FAIL'}  ({n_r2}/3)")
    for s in SEEDS:
        d = None if not defined(s,"GEN","CENTRALIZED") else round(P(s,"GEN")-P(s,"CENTRALIZED"),4)
        print(f"     seed {s}: Φ_gen={P(s,'GEN')} Φ_central={P(s,'CENTRALIZED')} gap={d}  {'PASS' if r2_per[s] else 'FAIL'}")
    print(f"R3 EARNED            (Φ(SHUFFLE) <= max(floor,central)+{TOL} EVERY seed): {'PASS' if r3 else 'FAIL'}  ({n_r3}/3)")
    for s in SEEDS:
        mx = None if not defined(s,"FLOOR","CENTRALIZED") else round(max(P(s,'FLOOR'),P(s,'CENTRALIZED')),4)
        print(f"     seed {s}: Φ_shuffle={P(s,'SHUFFLE')} max(floor,central)={mx}  {'PASS' if r3_per[s] else 'FAIL'}")
    print(f"R4 SYNERGY-MECHANISM (O(GEN)<0 EVERY seed AND REDUN<=CENTRALIZED on >=2/3): {'PASS' if r4 else 'FAIL'}")
    print(f"     R4a O(GEN)<0 EVERY seed: {'PASS' if r4a else 'FAIL'}  ({n_r4a}/3)")
    for s in SEEDS:
        print(f"       seed {s}: O(GEN)={oinfo[s]['GEN']:+.4f}  {'PASS' if r4a_per[s] else 'FAIL'}")
    print(f"     R4b REDUN<=CENTRALIZED on >=2/3: {'PASS' if r4b else 'FAIL'}  ({n_r4b}/3)")
    for s in SEEDS:
        d = None if not defined(s,"REDUN","CENTRALIZED") else round(P(s,"REDUN")-P(s,"CENTRALIZED"),4)
        print(f"       seed {s}: Φ_redun={P(s,'REDUN')} Φ_central={P(s,'CENTRALIZED')} gap={d}  {'PASS' if r4b_per[s] else 'FAIL'}")
    print(f"\nO-INFO per arm (O<0=synergy O>0=redundancy):")
    for s in SEEDS:
        row = " ".join(f"{a}={oinfo[s][a]:+.4f}" for a in ARMS)
        print(f"     seed {s}: {row}")
    print(f"\nVERDICT: {verdict}  (R1 {n_r1}/3, R2 {n_r2}/3, R3 {n_r3}/3, R4a {n_r4a}/3, R4b {n_r4b}/3)")

    out = {
        "id": "H_1376", "slug": "hive-generative-synergy", "verdict": verdict,
        "seeds": SEEDS, "N_tot": N_TOT, "ring_edges": [list(e) for e in RING_EDGES],
        "dim": DIM, "ticks": T, "share_w": SHARE_W, "overlap_w": OVERLAP_W,
        "margin": MARGIN, "tol": TOL,
        "phi_faithful_iit4": {str(s): {a: phi[s][a] for a in ARMS} for s in SEEDS},
        "o_information": {str(s): {a: oinfo[s][a] for a in ARMS} for s in SEEDS},
        "bars": {"R1_lift": bool(r1), "R2_beats_centralized": bool(r2),
                 "R3_earned": bool(r3), "R4_synergy_mechanism": bool(r4),
                 "R4a_o_gen_negative": bool(r4a), "R4b_redun_loses": bool(r4b)},
        "r1_per_seed": {str(s): bool(r1_per[s]) for s in SEEDS},
        "r2_per_seed": {str(s): bool(r2_per[s]) for s in SEEDS},
        "r3_per_seed": {str(s): bool(r3_per[s]) for s in SEEDS},
        "r4a_per_seed": {str(s): bool(r4a_per[s]) for s in SEEDS},
        "r4b_per_seed": {str(s): bool(r4b_per[s]) for s in SEEDS},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n<=8)",
    }
    print("\nRESULT_JSON=" + json.dumps(out))
    return out


if __name__ == "__main__":
    import sys as _sys
    if "--r2" in _sys.argv:
        main_r2()
    else:
        main()
        main_r2()
