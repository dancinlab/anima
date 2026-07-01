#!/usr/bin/env python3
# H_1363 — hive-weak-decorrelated: does a WEAK connector and/or DECORRELATED daughters escape the
# W=0 shared-input redundancy floor at faithful-IIT4 Φ, where H_1356's STRONG hub (W_CONN=0.6) failed?
# slug: hive-weak-decorrelated   seeds = [1317,1318,1319]  (hard hive/topology family).
#
# THE WALL (c16 / a_break_the_wall): H_1350 showed collective faithful-IIT4 Φ is ~85-96% shared-input
# REDUNDANCY (a W=0 floor). H_1356 tried a STRONG connector hub — it did WORSE than the floor
# (lift -4.82/-2.50/-5.00, 🧱 CONNECTOR_NULL): a strong hub HOMOGENIZES the daughters, which the
# faithful MIP reads as MORE reducible -> Φ DROPS. H_1356's own scope named the escape: "LOW
# coupling + decorrelated daughters, not a strong hub." H_1363 takes that up, frozen-first, via three
# refinements:
#   (1) W_CONN->0+ WEAK connector (nudge without homogenizing) — a frozen sweep.
#   (2) DECORRELATE the founder per daughter FIRST (orthogonal halves) so feedback ADDS not homogenizes.
#   (3) (NON-GATING) an O-information SYNERGY readout to SEE the redundancy/synergy balance.
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Φ — it only emits the
# per-unit salience (state-energy) trajectory; the hexa engine computes Φ. NO proxy. The O-info
# synergy number IS numpy, but it is a NON-GATING diagnostic, never the verdict gate.
#
# Substrate MATCHED to H_1356/H_1320/H_1283 (only refinement wiring/input differs between arms):
# leaky linear recurrent units, LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit private gaussian input,
# dim-8 state, T=64 ticks. N_TOT=8 (n<=8 keeps faithful MIP EXACT). Two daughters d0=units0..1,
# d1=units2..3. CONNECTOR cell = unit 4 (hub). Padding = units 5..7.
#
# FROZEN BARS (see .verdicts/1363_hive_weak_decorrelated/H_1363_FREEZE.txt — GREEN iff R1∧R2∧R3,
# MARGIN=0.02):
#   R1 LIFT           : Φ(best refinement) − Φ(W0_floor)    >= 0.02 on ALL 3 seeds.
#   R2 BEATS-REDUNDANT: Φ(best refinement) − Φ(B_redundant) >= 0.02 on ALL 3 seeds.
#   R3 EARNED         : Φ(SHUFFLE)         <= Φ(W0_floor) + 0.02 on ALL 3 seeds.
#   refinement = argmax Φ over {B_weak(best sweep), B_decorr, B_decorr_only} per seed.
# seeds [1317,1318,1319]. $0 CPU-local. frozen-first.

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS    = [1317, 1318, 1319]
N_TOT    = 8          # n<=8 keeps faithful IIT4 MIP exact
DIM      = 8          # per-unit state vector dim (H_1283)
T        = 64         # ticks (H_1283)
GAIN     = 0.30       # per-unit update gain (H_1283)
LEAK     = 0.55       # state self-retention (H_1283)
W_IN     = 0.5        # private-input weight (H_1283)
NBINS    = 8          # IIT4 MI estimator bins (H_1283)

# WEAK connector sweep toward 0+ (0.6 kept as the H_1356 strong anchor = the known 🧱 point)
W_CONN_SWEEP = [0.6, 0.3, 0.15, 0.08, 0.04, 0.02]
MARGIN   = 0.02       # IDENTICAL faithful-Φ margin H_1283/H_1317/H_1320/H_1356 froze (NOT moved)
TOL      = 0.02
DIFF_EPS = 0.15       # H_1320/H_1356 differentiation noise (verbatim)

# unit roles (fixed across arms)
D0   = [0, 1]         # daughter 0
D1   = [2, 3]         # daughter 1
CONN = 4              # 연결세포 connector hub unit
PAD  = [5, 6, 7]      # padding cells carrying shared founder context
DAUGHTER_UNITS = D0 + D1

HEXA      = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL  = os.path.join(HEXA_ROOT, "stdlib/consciousness/iit4/faithful_phi.hexa")


def evolve(init_states, inputs, mode, w_conn):
    """Leaky linear recurrent substrate (H_1283/H_1320/H_1356 unit dynamics), 8 units.
    mode controls the CONNECTOR (연결세포) wiring; w_conn = coupling strength for this arm:
      'no_conn' : NO connector path (W0_floor / B_redundant / B_decorr_only) — daughters read their
                  input only; no cross-daughter coupling.
      'conn'    : the CONNECTOR hub (unit CONN) reads the mean state of BOTH daughters and feeds back
                  into each daughter (strength w_conn); the hub itself integrates both daughters.
      'shuffle' : connector wired to RANDOM NON-daughter sources (PAD units) — kills role structure.
    Returns per-unit salience trajectory (N_TOT, T)."""
    states = init_states.copy()
    traj = np.zeros((N_TOT, T))
    for t in range(T):
        new = states.copy()
        mean_d0 = np.mean(states[D0], axis=0)
        mean_d1 = np.mean(states[D1], axis=0)
        if mode == "shuffle":
            src_a = states[PAD[0]]                    # fake source A (single pad unit)
            src_b = np.mean(states[PAD[1:]], axis=0)  # fake source B (other pads)
        else:
            src_a, src_b = mean_d0, mean_d1
        hub = states[CONN]
        for i in range(N_TOT):
            coupling = 0.0
            if mode == "conn":
                if i in D0 or i in D1:
                    coupling = w_conn * hub                 # daughter reads connector feedback
                elif i == CONN:
                    coupling = w_conn * (src_a + src_b)     # hub integrates BOTH daughters
            elif mode == "shuffle":
                if i in D0 or i in D1:
                    coupling = w_conn * hub
                elif i == CONN:
                    coupling = w_conn * (src_a + src_b)     # hub integrates the FAKE (pad) sources
            # 'no_conn': coupling stays 0 (W=0 redundancy floor)
            new[i] = LEAK * states[i] + GAIN * (coupling + W_IN * inputs[i, t])
        states = new
        for i in range(N_TOT):
            traj[i, t] = float(np.dot(states[i], states[i]))
    return traj


def _decorrelate_founder(founder_vec, shared_stream):
    """Deterministic orthogonal split of the founder representation into two halves.
    Returns (init_A, inp_A, init_B, inp_B): daughter-A reads founder slice A, daughter-B reads slice B,
    where A and B are orthogonal projections (even/odd-dim Hadamard-style sign split) of the SAME
    founder — so the two daughters carry DISTINCT (non-redundant) content drawn from one founder.
    This makes the shared input NON-redundant per daughter BEFORE coupling."""
    # orthogonal masks: mask_A keeps even dims (zeros odd), mask_B keeps odd dims (zeros even).
    # even/odd index split is an exact orthogonal partition of the DIM coordinates.
    mask_A = np.zeros(DIM); mask_A[0::2] = 1.0
    mask_B = np.zeros(DIM); mask_B[1::2] = 1.0
    init_A = founder_vec * mask_A
    init_B = founder_vec * mask_B
    inp_A  = shared_stream * mask_A[None, :]   # (T, DIM) * (1, DIM)
    inp_B  = shared_stream * mask_B[None, :]
    return init_A, inp_A, init_B, inp_B


def build_arm(seed, arm, w_conn=0.0):
    """Build (init_states, inputs, mode, w_conn) for an arm then evolve.
    arm in {'A_single','B_redundant','B_weak','B_decorr','B_decorr_only','W0_floor','SHUFFLE'}.
    For 'B_weak' the caller passes the sweep w_conn; for 'B_decorr'/'SHUFFLE' the caller passes the
    chosen weak w_conn. 공유세포 (SHARED founder) draws are IDENTICAL across arms so the W=0 floor is
    identical (and identical to H_1356)."""
    rng = np.random.default_rng(seed)

    # --- 공유세포 (SHARED founder) draws: ONE founder state + ONE shared input stream ---
    founder_init = rng.standard_normal((1, DIM)) * 0.5        # common founder representation
    shared_inp   = rng.standard_normal((1, T, DIM)) * 0.8     # shared developmental input
    diff_init = rng.standard_normal((N_TOT, DIM)) * 0.5
    diff_inp  = rng.standard_normal((N_TOT, T, DIM)) * 0.8    # (drawn to match H_1356 rng stream)
    indep_init = rng.standard_normal((N_TOT, DIM)) * 0.5
    indep_inp  = rng.standard_normal((N_TOT, T, DIM)) * 0.8

    init = np.zeros((N_TOT, DIM))
    inp  = np.zeros((N_TOT, T, DIM))

    if arm == "A_single":
        init[:] = indep_init
        inp[:]  = indep_inp
        return evolve(init, inp, "no_conn", 0.0)

    decorr = arm in ("B_decorr", "B_decorr_only") or (arm == "SHUFFLE")
    # NOTE: SHUFFLE is the EARNED control for the B_decorr wiring, so it uses the SAME decorrelated
    # daughter inputs (only the connector source is shuffled to pads). This makes SHUFFLE a faithful
    # role-destroyed twin of B_decorr.

    if decorr:
        iA, pA, iB, pB = _decorrelate_founder(founder_init[0], shared_inp[0])
        for u in D0:
            init[u] = iA + DIFF_EPS * diff_init[u]
            inp[u]  = pA
        for u in D1:
            init[u] = iB + DIFF_EPS * diff_init[u]
            inp[u]  = pB
    else:
        # redundant: every daughter reads the SAME founder slice + SAME shared stream
        for u in DAUGHTER_UNITS:
            init[u] = founder_init[0] + DIFF_EPS * diff_init[u]
            inp[u]  = shared_inp[0]

    # connector hub + padding: seeded from shared founder context, differentiated; input = shared stream
    for u in [CONN] + PAD:
        init[u] = founder_init[0] + DIFF_EPS * diff_init[u]
        inp[u]  = shared_inp[0]

    if arm in ("B_redundant", "W0_floor", "B_decorr_only"):
        mode, wc = "no_conn", 0.0
    elif arm in ("B_weak", "B_decorr"):
        mode, wc = "conn", w_conn
    elif arm == "SHUFFLE":
        mode, wc = "shuffle", w_conn
    else:
        raise ValueError(arm)

    return evolve(init, inp, mode, wc)


# ── O-information synergy diagnostic (NON-GATING, numpy-side) ──────────────────
def _entropy(samples_2d, nbins):
    """Discrete entropy (nats) of a joint over columns of samples_2d (T, k) via histogram binning."""
    T_, k = samples_2d.shape
    # bin each column independently into nbins, then count joint tuples
    binned = np.zeros((T_, k), dtype=np.int64)
    for j in range(k):
        col = samples_2d[:, j]
        lo, hi = col.min(), col.max()
        if hi - lo < 1e-12:
            binned[:, j] = 0
        else:
            edges = np.linspace(lo, hi, nbins + 1)
            binned[:, j] = np.clip(np.digitize(col, edges[1:-1]), 0, nbins - 1)
    # joint counts
    _, counts = np.unique(binned, axis=0, return_counts=True)
    p = counts / counts.sum()
    return float(-(p * np.log(p)).sum())


def o_information(traj_units, nbins):
    """O-information of the N salience series (T samples each). O = (N-2)*H(X) - sum_i[H(X)-H(X_-i)]
    standard form: O = (n-2)*H(all) + sum_i [ H(x_i) - H(all \ x_i) ].
    O>0 redundancy-dominated, O<0 synergy-dominated. Diagnostic only."""
    X = traj_units.T  # (T, n)
    n = X.shape[1]
    H_all = _entropy(X, nbins)
    H_marg = sum(_entropy(X[:, [i]], nbins) for i in range(n))
    H_drop = 0.0
    for i in range(n):
        cols = [j for j in range(n) if j != i]
        H_drop += _entropy(X[:, cols], nbins)
    # O = (n-2) H(all) + sum_i H(x_i) - sum_i H(all\x_i)
    return float((n - 2) * H_all + H_marg - H_drop)


def faithful_phi(traj_units, tag):
    """faithful IIT4 Φ over the given unit trajectories via the stdlib EXACT engine (hexa run)."""
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


def main():
    print("H_1363 hive-weak-decorrelated: WEAK connector + DECORRELATED daughters — faithful-IIT4 collective-Φ")
    print(f"N_TOT={N_TOT} d0={D0} d1={D1} connector={CONN} pad={PAD} dim={DIM} ticks={T} seeds={SEEDS}")
    print(f"W_CONN_SWEEP={W_CONN_SWEEP}  faithful IIT4 Φ (exact MIP-EI, n<=8); MARGIN={MARGIN} TOL={TOL}")
    print("=" * 92)

    phi = {}      # phi[seed][arm_label] = float
    syn = {}      # syn[seed][arm_label] = O-information (diagnostic)
    weak_best_wc = {}   # weak_best_wc[seed] = w_conn maximizing B_weak Φ

    for seed in SEEDS:
        phi[seed] = {}
        syn[seed] = {}

        # base arms (no sweep): A_single, W0_floor, B_redundant, B_decorr_only
        for arm in ("A_single", "W0_floor", "B_redundant", "B_decorr_only"):
            traj = build_arm(seed, arm)
            phi[seed][arm] = faithful_phi(traj, f"{arm}_s{seed}")
            syn[seed][arm] = o_information(traj, NBINS)
            print(f"  seed {seed} {arm:>16}: Φ={phi[seed][arm]}  O-info={round(syn[seed][arm],4)}")

        # B_weak sweep over W_CONN -> pick best
        best_wc, best_phi = None, -1e18
        for wc in W_CONN_SWEEP:
            traj = build_arm(seed, "B_weak", w_conn=wc)
            p = faithful_phi(traj, f"B_weak_wc{wc}_s{seed}")
            o = o_information(traj, NBINS)
            label = f"B_weak@{wc}"
            phi[seed][label] = p
            syn[seed][label] = o
            print(f"  seed {seed} {label:>16}: Φ={p}  O-info={round(o,4)}")
            if p is not None and p > best_phi:
                best_phi, best_wc = p, wc
        weak_best_wc[seed] = best_wc
        phi[seed]["B_weak"] = phi[seed][f"B_weak@{best_wc}"]
        syn[seed]["B_weak"] = syn[seed][f"B_weak@{best_wc}"]
        print(f"  seed {seed}  --> B_weak BEST w_conn={best_wc} Φ={phi[seed]['B_weak']}")

        # B_decorr (decorrelated daughters + the best weak w_conn) and its SHUFFLE control
        traj = build_arm(seed, "B_decorr", w_conn=best_wc)
        phi[seed]["B_decorr"] = faithful_phi(traj, f"B_decorr_s{seed}")
        syn[seed]["B_decorr"] = o_information(traj, NBINS)
        print(f"  seed {seed} {'B_decorr':>16}: Φ={phi[seed]['B_decorr']}  O-info={round(syn[seed]['B_decorr'],4)} (w_conn={best_wc})")

        traj = build_arm(seed, "SHUFFLE", w_conn=best_wc)
        phi[seed]["SHUFFLE"] = faithful_phi(traj, f"SHUFFLE_s{seed}")
        syn[seed]["SHUFFLE"] = o_information(traj, NBINS)
        print(f"  seed {seed} {'SHUFFLE':>16}: Φ={phi[seed]['SHUFFLE']}  O-info={round(syn[seed]['SHUFFLE'],4)}")
        print("-" * 92)

    # ── FROZEN BARS ──────────────────────────────────────────────────────────
    def P(s, a): return phi[s][a]

    REFINEMENTS = ("B_weak", "B_decorr", "B_decorr_only")
    best_ref = {}   # best_ref[seed] = (label, phi)
    for s in SEEDS:
        cand = [(a, P(s, a)) for a in REFINEMENTS if P(s, a) is not None]
        best_ref[s] = max(cand, key=lambda kv: kv[1]) if cand else (None, None)

    # R1 LIFT: Φ(best refinement) − Φ(W0_floor) >= MARGIN, all seeds
    r1_per = {s: (best_ref[s][1] is not None and P(s, "W0_floor") is not None
                  and best_ref[s][1] - P(s, "W0_floor") >= MARGIN) for s in SEEDS}
    r1 = all(r1_per.values())

    # R2 BEATS-REDUNDANT: Φ(best refinement) − Φ(B_redundant) >= MARGIN, all seeds
    r2_per = {s: (best_ref[s][1] is not None and P(s, "B_redundant") is not None
                  and best_ref[s][1] - P(s, "B_redundant") >= MARGIN) for s in SEEDS}
    r2 = all(r2_per.values())

    # R3 EARNED: Φ(SHUFFLE) <= Φ(W0_floor) + TOL, all seeds
    r3_per = {s: (P(s, "SHUFFLE") is not None and P(s, "W0_floor") is not None
                  and P(s, "SHUFFLE") <= P(s, "W0_floor") + TOL) for s in SEEDS}
    r3 = all(r3_per.values())

    green = r1 and r2 and r3
    n_r1, n_r2, n_r3 = sum(r1_per.values()), sum(r2_per.values()), sum(r3_per.values())

    if green:
        verdict = "GREEN_ESCAPES_REDUNDANCY"
    elif (n_r1 == 2 or n_r2 == 2):
        verdict = "SEED_FRAGILE"
    elif not r3:
        verdict = "WALL_NOT_EARNED"
    elif not r1:
        verdict = "REDUNDANCY_BOUND"   # no refinement beats the floor -> honest 🧱 closure
    else:
        verdict = "PARTIAL"

    print("=" * 92)
    print(f"per-seed BEST refinement (argmax Φ over {REFINEMENTS}):")
    for s in SEEDS:
        print(f"     seed {s}: best={best_ref[s][0]} Φ={best_ref[s][1]}  (B_weak best w_conn={weak_best_wc[s]})")
    print(f"R1 LIFT            (Φ(best) − Φ(W0_floor)    >= {MARGIN} EVERY seed): {'PASS' if r1 else 'FAIL'}")
    for s in SEEDS:
        d = None if (best_ref[s][1] is None or P(s,"W0_floor") is None) else round(best_ref[s][1]-P(s,"W0_floor"),4)
        print(f"     seed {s}: Φ_best={best_ref[s][1]} Φ_floor={P(s,'W0_floor')} lift={d}  {'PASS' if r1_per[s] else 'FAIL'}")
    print(f"R2 BEATS-REDUNDANT(Φ(best) − Φ(B_redundant) >= {MARGIN} EVERY seed): {'PASS' if r2 else 'FAIL'}")
    for s in SEEDS:
        d = None if (best_ref[s][1] is None or P(s,"B_redundant") is None) else round(best_ref[s][1]-P(s,"B_redundant"),4)
        print(f"     seed {s}: Φ_best={best_ref[s][1]} Φ_redund={P(s,'B_redundant')} gap={d}  {'PASS' if r2_per[s] else 'FAIL'}")
    print(f"R3 EARNED         (Φ(SHUFFLE) <= Φ(W0_floor) + {TOL} EVERY seed): {'PASS' if r3 else 'FAIL'}")
    for s in SEEDS:
        print(f"     seed {s}: Φ_shuffle={P(s,'SHUFFLE')} Φ_floor={P(s,'W0_floor')}  {'PASS' if r3_per[s] else 'FAIL'}")
    print(f"VERDICT: {verdict}  (R1 {n_r1}/3, R2 {n_r2}/3, R3 {n_r3}/3)")

    print("\nO-information SYNERGY diagnostic (NON-GATING; O<0 synergy, O>0 redundancy):")
    for s in SEEDS:
        floor_o = round(syn[s]['W0_floor'],4)
        best_o  = round(syn[s][best_ref[s][0]],4) if best_ref[s][0] else None
        print(f"     seed {s}: O(W0_floor)={floor_o}  O(best={best_ref[s][0]})={best_o}")

    out = {
        "id": "H_1363", "slug": "hive-weak-decorrelated", "verdict": verdict,
        "seeds": SEEDS, "N_tot": N_TOT, "d0": D0, "d1": D1, "connector": CONN, "pad": PAD,
        "dim": DIM, "ticks": T, "w_conn_sweep": W_CONN_SWEEP, "weak_best_wc": weak_best_wc,
        "margin": MARGIN, "tol": TOL, "diff_eps": DIFF_EPS,
        "phi_faithful_iit4": {str(s): {a: phi[s][a] for a in phi[s]} for s in SEEDS},
        "o_information_diag": {str(s): {a: syn[s][a] for a in syn[s]} for s in SEEDS},
        "best_refinement": {str(s): {"arm": best_ref[s][0], "phi": best_ref[s][1]} for s in SEEDS},
        "bars": {"R1_lift": bool(r1), "R2_beats_redundant": bool(r2), "R3_earned": bool(r3)},
        "r1_per_seed": {str(s): bool(r1_per[s]) for s in SEEDS},
        "r2_per_seed": {str(s): bool(r2_per[s]) for s in SEEDS},
        "r3_per_seed": {str(s): bool(r3_per[s]) for s in SEEDS},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n<=8)",
    }
    print("\nRESULT_JSON=" + json.dumps(out))
    return out


if __name__ == "__main__":
    main()
