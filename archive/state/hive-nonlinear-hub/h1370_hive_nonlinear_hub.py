#!/usr/bin/env python3
# H_1370 — hive-nonlinear-hub: does a NON-LINEAR / GATED connector cell (tanh gate on the hub feedback)
# escape the W=0 shared-input redundancy floor at faithful-IIT4 Φ, where H_1356/1363's LINEAR hub failed?
# slug: hive-nonlinear-hub   seeds = [1317,1318,1319]  (hard hive/topology family, H_1356/1363 verbatim).
#
# THE WALL (c16 / a_break_the_wall): H_1356 (STRONG linear hub, W_CONN=0.6) did WORSE than the floor
# (lift -4.82/-2.50/-5.00, 🧱 CONNECTOR_NULL); H_1363 (WEAK connector + DECORRELATED daughters + synergy
# lens) → 🧱 REDUNDANCY_BOUND. H_1363's LOAD-BEARING diagnosis: the substrate is leaky-LINEAR, so ANY hub
# LINEARLY homogenizes the daughters → faithful MIP reads them as MORE reducible → Φ DROPS. THE
# HOMOGENIZATION ARGUMENT RESTS ON LINEARITY. H_1370 breaks that assumption: a SATURATING tanh gate on
# the hub feedback bounds the pull so the hub NUDGES without dragging each daughter onto the shared hub
# state — the exact linear-homogenization mechanism the prior closure rests on.
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Φ — it only emits the
# per-unit salience (state-energy) trajectory; the hexa engine computes Φ. NO proxy.
#
# Substrate MATCHED to H_1356/H_1363/H_1320/H_1283 VERBATIM (ONLY the hub nonlinearity differs between
# B_linear and B_nonlinear): leaky linear recurrent units, LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit
# private gaussian input, dim-8 state, T=64 ticks. N_TOT=8 (n<=8 keeps faithful MIP EXACT). Two
# daughters d0=units0..1, d1=units2..3. CONNECTOR cell = unit 4 (hub). Padding = units 5..7.
#
# PRE-REGISTERED NONLINEARITY (frozen, see H_1370_FREEZE.txt): GATE=tanh, GATE_GAIN=2.0, W_CONN=0.6
# (the SAME strong coupling H_1356's linear hub used — the ONLY difference is the tanh gate).
#
# FROZEN BARS (GREEN iff R1∧R2∧R3, MARGIN=0.02):
#   R1 LIFT         : Φ(B_nonlinear) − Φ(W0_floor) >= 0.02 on ALL 3 seeds.
#   R2 BEATS-LINEAR : Φ(B_nonlinear) − Φ(B_linear) >= 0.02 on ALL 3 seeds (the H_1356/1363-escape).
#   R3 EARNED       : Φ(SHUFFLE)     <= Φ(W0_floor) + 0.02 on ALL 3 seeds.
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

W_CONN    = 0.6       # STRONG coupling = H_1356 linear-hub anchor (B_linear AND B_nonlinear share it)
GATE_GAIN = 2.0       # PRE-REGISTERED tanh gate gain (frozen)
MARGIN   = 0.02       # IDENTICAL faithful-Φ margin H_1283/H_1317/H_1320/H_1356/H_1363 froze (NOT moved)
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


def evolve(init_states, inputs, mode):
    """Leaky linear recurrent substrate (H_1283/H_1320/H_1356 unit dynamics), 8 units.
    mode controls the CONNECTOR (연결세포) wiring:
      'no_conn'   : NO connector path (W0_floor / B_redundant) — daughters read input only.
      'linear'    : LINEAR hub (H_1356): hub reads mean of BOTH daughters and feeds back LINEARLY
                    (strength W_CONN); hub integrates both daughters LINEARLY.
      'nonlinear' : tanh-GATED hub (H_1370): the SAME wiring but the hub feedback to each daughter
                    AND the hub integration of the daughters pass through tanh(GATE_GAIN * .) — a
                    saturating gate that bounds the pull (nudge, not drag-to-hub-state).
      'shuffle'   : nonlinear-gated hub wired to RANDOM NON-daughter (PAD) sources — kills role structure.
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
            if mode == "linear":
                if i in D0 or i in D1:
                    coupling = W_CONN * hub                         # LINEAR daughter feedback
                elif i == CONN:
                    coupling = W_CONN * (src_a + src_b)             # LINEAR hub integration
            elif mode == "nonlinear":
                if i in D0 or i in D1:
                    coupling = W_CONN * np.tanh(GATE_GAIN * hub)    # GATED daughter feedback
                elif i == CONN:
                    coupling = W_CONN * np.tanh(GATE_GAIN * (src_a + src_b))  # GATED hub integration
            elif mode == "shuffle":
                if i in D0 or i in D1:
                    coupling = W_CONN * np.tanh(GATE_GAIN * hub)
                elif i == CONN:
                    coupling = W_CONN * np.tanh(GATE_GAIN * (src_a + src_b))  # gated, FAKE (pad) sources
            # 'no_conn': coupling stays 0 (W=0 redundancy floor)
            new[i] = LEAK * states[i] + GAIN * (coupling + W_IN * inputs[i, t])
        states = new
        for i in range(N_TOT):
            traj[i, t] = float(np.dot(states[i], states[i]))
    return traj


def build_arm(seed, arm):
    """Build (init_states, inputs, mode) for an arm then evolve.
    arm in {'A_single','B_redundant','B_linear','B_nonlinear','W0_floor','SHUFFLE'}.
    공유세포 (SHARED founder) draws are IDENTICAL across arms AND identical to H_1356/H_1363 so the W=0
    floor is byte-identical (12.4018 / 6.94639 / 12.2284) — a setup-integrity check."""
    rng = np.random.default_rng(seed)

    # --- 공유세포 (SHARED founder) draws: ONE founder state + ONE shared input stream ---
    # NOTE: the rng draw ORDER matches H_1356/H_1363 exactly so W0_floor reproduces byte-for-byte.
    founder_init = rng.standard_normal((1, DIM)) * 0.5        # common founder representation
    shared_inp   = rng.standard_normal((1, T, DIM)) * 0.8     # shared developmental input
    diff_init = rng.standard_normal((N_TOT, DIM)) * 0.5
    diff_inp  = rng.standard_normal((N_TOT, T, DIM)) * 0.8    # (drawn to match H_1356/1363 rng stream)
    indep_init = rng.standard_normal((N_TOT, DIM)) * 0.5
    indep_inp  = rng.standard_normal((N_TOT, T, DIM)) * 0.8

    init = np.zeros((N_TOT, DIM))
    inp  = np.zeros((N_TOT, T, DIM))

    if arm == "A_single":
        init[:] = indep_init
        inp[:]  = indep_inp
        return evolve(init, inp, "no_conn")

    # redundant: every daughter reads the SAME founder slice + SAME shared stream
    for u in DAUGHTER_UNITS:
        init[u] = founder_init[0] + DIFF_EPS * diff_init[u]
        inp[u]  = shared_inp[0]
    # connector hub + padding: seeded from shared founder context, differentiated; input = shared stream
    for u in [CONN] + PAD:
        init[u] = founder_init[0] + DIFF_EPS * diff_init[u]
        inp[u]  = shared_inp[0]

    if arm in ("B_redundant", "W0_floor"):
        mode = "no_conn"
    elif arm == "B_linear":
        mode = "linear"
    elif arm == "B_nonlinear":
        mode = "nonlinear"
    elif arm == "SHUFFLE":
        mode = "shuffle"
    else:
        raise ValueError(arm)

    return evolve(init, inp, mode)


# ── O-information synergy diagnostic (NON-GATING, numpy-side) ──────────────────
def _entropy(samples_2d, nbins):
    T_, k = samples_2d.shape
    binned = np.zeros((T_, k), dtype=np.int64)
    for j in range(k):
        col = samples_2d[:, j]
        lo, hi = col.min(), col.max()
        if hi - lo < 1e-12:
            binned[:, j] = 0
        else:
            edges = np.linspace(lo, hi, nbins + 1)
            binned[:, j] = np.clip(np.digitize(col, edges[1:-1]), 0, nbins - 1)
    _, counts = np.unique(binned, axis=0, return_counts=True)
    p = counts / counts.sum()
    return float(-(p * np.log(p)).sum())


def o_information(traj_units, nbins):
    """O-information of the N salience series. O>0 redundancy-dominated, O<0 synergy-dominated.
    Diagnostic only (NON-GATING)."""
    X = traj_units.T  # (T, n)
    n = X.shape[1]
    H_all = _entropy(X, nbins)
    H_marg = sum(_entropy(X[:, [i]], nbins) for i in range(n))
    H_drop = 0.0
    for i in range(n):
        cols = [j for j in range(n) if j != i]
        H_drop += _entropy(X[:, cols], nbins)
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
    print("H_1370 hive-nonlinear-hub: tanh-GATED connector hub — faithful-IIT4 collective-Φ")
    print(f"N_TOT={N_TOT} d0={D0} d1={D1} connector={CONN} pad={PAD} dim={DIM} ticks={T} seeds={SEEDS}")
    print(f"W_CONN={W_CONN} GATE=tanh GATE_GAIN={GATE_GAIN}  faithful IIT4 Φ (exact MIP-EI, n<=8); MARGIN={MARGIN} TOL={TOL}")
    print("=" * 92)

    ARMS = ("A_single", "W0_floor", "B_redundant", "B_linear", "B_nonlinear", "SHUFFLE")
    phi = {}      # phi[seed][arm] = float
    syn = {}      # syn[seed][arm] = O-information (diagnostic)

    for seed in SEEDS:
        phi[seed] = {}
        syn[seed] = {}
        for arm in ARMS:
            traj = build_arm(seed, arm)
            phi[seed][arm] = faithful_phi(traj, f"{arm}_s{seed}")
            syn[seed][arm] = o_information(traj, NBINS)
            print(f"  seed {seed} {arm:>14}: Φ={phi[seed][arm]}  O-info={round(syn[seed][arm],4)}")
        print("-" * 92)

    def P(s, a): return phi[s][a]

    # R1 LIFT: Φ(B_nonlinear) − Φ(W0_floor) >= MARGIN, all seeds
    r1_per = {s: (P(s,"B_nonlinear") is not None and P(s,"W0_floor") is not None
                  and P(s,"B_nonlinear") - P(s,"W0_floor") >= MARGIN) for s in SEEDS}
    r1 = all(r1_per.values())

    # R2 BEATS-LINEAR: Φ(B_nonlinear) − Φ(B_linear) >= MARGIN, all seeds
    r2_per = {s: (P(s,"B_nonlinear") is not None and P(s,"B_linear") is not None
                  and P(s,"B_nonlinear") - P(s,"B_linear") >= MARGIN) for s in SEEDS}
    r2 = all(r2_per.values())

    # R3 EARNED: Φ(SHUFFLE) <= Φ(W0_floor) + TOL, all seeds
    r3_per = {s: (P(s,"SHUFFLE") is not None and P(s,"W0_floor") is not None
                  and P(s,"SHUFFLE") <= P(s,"W0_floor") + TOL) for s in SEEDS}
    r3 = all(r3_per.values())

    green = r1 and r2 and r3
    n_r1, n_r2, n_r3 = sum(r1_per.values()), sum(r2_per.values()), sum(r3_per.values())

    if green:
        verdict = "GREEN_NONLINEAR_ESCAPES"
    elif (n_r1 == 2 or n_r2 == 2):
        verdict = "SEED_FRAGILE"
    elif not r3:
        verdict = "WALL_NOT_EARNED"
    elif not r1:
        verdict = "REDUNDANCY_BOUND_NONLINEAR"   # gated hub ALSO fails the floor -> shared-input ceiling, 🧱
    else:
        verdict = "PARTIAL"

    print("=" * 92)
    print(f"R1 LIFT          (Φ(B_nonlinear) − Φ(W0_floor) >= {MARGIN} EVERY seed): {'PASS' if r1 else 'FAIL'}")
    for s in SEEDS:
        d = None if (P(s,"B_nonlinear") is None or P(s,"W0_floor") is None) else round(P(s,"B_nonlinear")-P(s,"W0_floor"),4)
        print(f"     seed {s}: Φ_nl={P(s,'B_nonlinear')} Φ_floor={P(s,'W0_floor')} lift={d}  {'PASS' if r1_per[s] else 'FAIL'}")
    print(f"R2 BEATS-LINEAR  (Φ(B_nonlinear) − Φ(B_linear) >= {MARGIN} EVERY seed): {'PASS' if r2 else 'FAIL'}")
    for s in SEEDS:
        d = None if (P(s,"B_nonlinear") is None or P(s,"B_linear") is None) else round(P(s,"B_nonlinear")-P(s,"B_linear"),4)
        print(f"     seed {s}: Φ_nl={P(s,'B_nonlinear')} Φ_lin={P(s,'B_linear')} gap={d}  {'PASS' if r2_per[s] else 'FAIL'}")
    print(f"R3 EARNED        (Φ(SHUFFLE) <= Φ(W0_floor) + {TOL} EVERY seed): {'PASS' if r3 else 'FAIL'}")
    for s in SEEDS:
        print(f"     seed {s}: Φ_shuffle={P(s,'SHUFFLE')} Φ_floor={P(s,'W0_floor')}  {'PASS' if r3_per[s] else 'FAIL'}")
    print(f"VERDICT: {verdict}  (R1 {n_r1}/3, R2 {n_r2}/3, R3 {n_r3}/3)")

    # setup-integrity: W0_floor must reproduce H_1356/H_1363 byte-identical
    H1363_FLOOR = {1317: 12.4018, 1318: 6.94639, 1319: 12.2284}
    print("\nSETUP-INTEGRITY (W0_floor must match H_1356/H_1363 floor):")
    for s in SEEDS:
        ref = H1363_FLOOR[s]
        got = P(s, "W0_floor")
        ok = (got is not None and abs(got - ref) < 0.01)
        print(f"     seed {s}: W0_floor={got}  H_1363_ref={ref}  {'OK' if ok else 'MISMATCH'}")

    print("\nO-information SYNERGY diagnostic (NON-GATING; O<0 synergy, O>0 redundancy):")
    for s in SEEDS:
        print(f"     seed {s}: O(W0_floor)={round(syn[s]['W0_floor'],4)}  O(B_linear)={round(syn[s]['B_linear'],4)}  O(B_nonlinear)={round(syn[s]['B_nonlinear'],4)}")

    out = {
        "id": "H_1370", "slug": "hive-nonlinear-hub", "verdict": verdict,
        "seeds": SEEDS, "N_tot": N_TOT, "d0": D0, "d1": D1, "connector": CONN, "pad": PAD,
        "dim": DIM, "ticks": T, "w_conn": W_CONN, "gate": "tanh", "gate_gain": GATE_GAIN,
        "margin": MARGIN, "tol": TOL, "diff_eps": DIFF_EPS,
        "phi_faithful_iit4": {str(s): {a: phi[s][a] for a in phi[s]} for s in SEEDS},
        "o_information_diag": {str(s): {a: syn[s][a] for a in syn[s]} for s in SEEDS},
        "bars": {"R1_lift": bool(r1), "R2_beats_linear": bool(r2), "R3_earned": bool(r3)},
        "r1_per_seed": {str(s): bool(r1_per[s]) for s in SEEDS},
        "r2_per_seed": {str(s): bool(r2_per[s]) for s in SEEDS},
        "r3_per_seed": {str(s): bool(r3_per[s]) for s in SEEDS},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n<=8)",
    }
    print("\nRESULT_JSON=" + json.dumps(out))
    return out


if __name__ == "__main__":
    main()
