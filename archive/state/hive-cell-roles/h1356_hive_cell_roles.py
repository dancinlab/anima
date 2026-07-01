#!/usr/bin/env python3
# H_1356 — hive-cell ROLES: 공유세포 (SHARED cell) ⊥ 연결세포 (CONNECTOR cell)
# slug: hive-cell-roles   seeds = [1317,1318,1319]  (hard hive/topology family).
#
# THE WALL (c16 / a_break_the_wall): H_1350 (hive-larger-budget) lifted collective faithful-IIT4
# Φ to 3/3 seed-robust, BUT a SHARED_DECOUPLED (W=0) control showed ~85-96% of the lift is
# shared-input REDUNDANCY (present with ZERO coupling). Diagnosis: redundancy-dominated —
# redundant copies share an input but do NOT integrate between each other.
#
# THE NEW LENS (a_no_llm_frame_trap, c15 — biological differentiation): Volvox somatic
# differentiation / sponge connector cells / hub neurons / gap-junction cells make a colony an
# INTEGRATED organism by ROLE DIFFERENTIATION, not by more redundant copies. Give cells DISTINCT
# roles: a 공유세포 (SHARED founder input every daughter reads = the redundancy source / W=0 floor)
# + a 연결세포 (CONNECTOR hub that reads MULTIPLE daughters and feeds back = genuine cross-daughter
# coupling). Does the CONNECTOR lift the coupling-EARNED (W=0-floor-beating, non-redundant) Φ
# ROBUSTLY across 3 seeds, where redundant copies (H_1350) could not?
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Φ — it only emits the
# per-unit salience (state-energy) trajectory; the hexa engine computes Φ. NO proxy.
#
# Substrate MATCHED to H_1320/H_1283 (only the connector wiring/role differs between arms):
# leaky linear recurrent units, LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit private gaussian input,
# dim-8 state, T=64 ticks. N_TOT=8 (n<=8 keeps faithful MIP EXACT). Two daughters d0=units0..1,
# d1=units2..3 (2 units each). CONNECTOR cell = unit 4 (hub). Padding = units 5..7.
# W_CONN=0.6 (the H_1308/1313/1320 hive coupling, reused verbatim). EVERY arm shares the SAME
# 공유세포 founder init + shared input stream → the W=0 redundancy floor is IDENTICAL across arms.
#
# FROZEN BARS (see .verdicts/1356_hive_cell_roles/H_1356_FREEZE.txt — GREEN iff R1 ∧ R2 ∧ R3,
# MARGIN=0.02):
#   R1 CONNECTOR-LIFT  : Φ(B_connector) − Φ(W0_floor)    >= 0.02 on ALL 3 seeds.
#   R2 BEATS-REDUNDANT : Φ(B_connector) − Φ(B_redundant) >= 0.02 on ALL 3 seeds (H_1350-escape).
#   R3 EARNED          : Φ(SHUFFLE)      <= Φ(W0_floor) + 0.02 on ALL 3 seeds.
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

W_CONN   = 0.6        # H_1308/1313/1320 hive coupling strength (reused verbatim) — the connector path
MARGIN   = 0.02       # IDENTICAL faithful-Φ margin H_1283/H_1317/H_1320 froze (NOT moved)
TOL      = 0.02

# unit roles (fixed across arms)
D0 = [0, 1]           # daughter 0
D1 = [2, 3]           # daughter 1
CONN = 4              # 연결세포 connector hub unit
PAD  = [5, 6, 7]      # padding cells carrying shared founder context (no connector wiring)
DAUGHTER_UNITS = D0 + D1

HEXA      = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL  = os.path.join(HEXA_ROOT, "stdlib/consciousness/iit4/faithful_phi.hexa")


def evolve(init_states, inputs, mode):
    """Leaky linear recurrent substrate (H_1283/H_1320 unit dynamics), 8 units.
    mode controls the CONNECTOR (연결세포) wiring:
      'no_conn'      : NO connector path (B_redundant / W0_floor) — daughters read shared input
                       only; no cross-daughter coupling. W=0 redundancy floor.
      'conn'         : B_connector — the CONNECTOR hub (unit CONN) reads the mean state of BOTH
                       daughters and feeds back into each daughter; the hub itself integrates.
      'shuffle'      : connector wired to RANDOM NON-daughter sources (PAD units) instead of the
                       real daughters — kills the role structure; must collapse to the floor.
    Returns per-unit salience trajectory (N_TOT, T)."""
    states = init_states.copy()
    traj = np.zeros((N_TOT, T))
    for t in range(T):
        new = states.copy()
        # connector reads-from sources for this mode
        mean_d0 = np.mean(states[D0], axis=0)
        mean_d1 = np.mean(states[D1], axis=0)
        if mode == "shuffle":
            # connector reads RANDOM non-daughter sources: split PAD into two halves as fake "daughters"
            src_a = states[PAD[0]]                       # fake source A (single pad unit)
            src_b = np.mean(states[PAD[1:]], axis=0)     # fake source B (other pads)
        else:
            src_a, src_b = mean_d0, mean_d1
        hub = states[CONN]
        for i in range(N_TOT):
            coupling = 0.0
            if mode == "conn":
                if i in D0:
                    coupling = W_CONN * hub            # daughter reads connector feedback
                elif i in D1:
                    coupling = W_CONN * hub
                elif i == CONN:
                    coupling = W_CONN * (src_a + src_b)  # hub integrates BOTH daughters
            elif mode == "shuffle":
                # role-shuffled: connector hub integrates the FAKE (pad) sources, daughters still
                # read the hub feedback (same wiring topology, wrong sources).
                if i in D0 or i in D1:
                    coupling = W_CONN * hub
                elif i == CONN:
                    coupling = W_CONN * (src_a + src_b)
            # 'no_conn': coupling stays 0 for all units (W=0 redundancy floor)
            new[i] = LEAK * states[i] + GAIN * (coupling + W_IN * inputs[i, t])
        states = new
        for i in range(N_TOT):
            traj[i, t] = float(np.dot(states[i], states[i]))
    return traj


def build_arm(seed, arm):
    """Build (init_states, inputs, mode) for an arm then evolve.
    arm in {'A_single','B_redundant','B_connector','W0_floor','SHUFFLE'}.

    공유세포 (SHARED founder): a SINGLE founder init + SINGLE shared input stream that EVERY
    daughter reads — IDENTICAL across arms, so the W=0 redundancy floor is identical. Arms differ
    ONLY in the connector wiring/role. The connector unit + padding get their own (shared-founder)
    context streams. A_single is the undivided baseline (no daughters, no connector)."""
    rng = np.random.default_rng(seed)

    # --- 공유세포 (SHARED founder) draws: ONE founder state + ONE shared input stream ---
    founder_init = rng.standard_normal((1, DIM)) * 0.5        # the common founder representation
    shared_inp   = rng.standard_normal((1, T, DIM)) * 0.8     # the shared developmental input
    # small per-unit differentiation noise (clone+differentiate), frozen 0.15 like H_1320 DIFF_EPS
    DIFF_EPS = 0.15
    diff_init = rng.standard_normal((N_TOT, DIM)) * 0.5
    diff_inp  = rng.standard_normal((N_TOT, T, DIM)) * 0.8
    # independent draws for the A_single undivided baseline's "other half" (H_1320 'single' style)
    indep_init = rng.standard_normal((N_TOT, DIM)) * 0.5
    indep_inp  = rng.standard_normal((N_TOT, T, DIM)) * 0.8

    init = np.zeros((N_TOT, DIM))
    inp  = np.zeros((N_TOT, T, DIM))

    if arm == "A_single":
        # one undivided cell: each unit gets its OWN independent private stream (no shared founder,
        # no daughter split, no connector) — the H_1320 'single' baseline over 8 units.
        init[:] = indep_init
        inp[:]  = indep_inp
        mode = "no_conn"
        return evolve(init, inp, mode)

    # --- ROLE-DIFFERENTIATED arms: every unit reads the SHARED founder (공유세포) ---
    # daughters d0,d1 = clone of founder + differentiation; input = SHARED founder stream (redundancy)
    for u in DAUGHTER_UNITS:
        init[u] = founder_init[0] + DIFF_EPS * diff_init[u]
        inp[u]  = shared_inp[0]                              # SHARED redundancy source
    # connector hub + padding: also seeded from the shared founder context (so they carry the
    # common origin), differentiated; padding input = shared founder stream too.
    for u in [CONN] + PAD:
        init[u] = founder_init[0] + DIFF_EPS * diff_init[u]
        inp[u]  = shared_inp[0]

    if arm == "B_redundant":
        mode = "no_conn"     # redundancy only, NO connector
    elif arm == "B_connector":
        mode = "conn"        # the 연결세포 connector hub wired in
    elif arm == "W0_floor":
        mode = "no_conn"     # SHARED_DECOUPLED — all coupling off (the explicit W=0 floor)
    elif arm == "SHUFFLE":
        mode = "shuffle"     # connector wired to RANDOM non-daughter sources
    else:
        raise ValueError(arm)

    return evolve(init, inp, mode)


def faithful_phi(traj_units, tag):
    """faithful IIT4 Φ over the given unit trajectories via the stdlib EXACT engine (hexa run).
    Inlines the trajectory as farr_set calls, calls iit4_faithful_phi(state, n, dim=T, n_bins).
    Returns float Φ (or None)."""
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


ARMS = ("A_single", "B_redundant", "B_connector", "W0_floor", "SHUFFLE")


def main():
    print("H_1356 hive-cell ROLES: 공유세포 (SHARED) ⊥ 연결세포 (CONNECTOR) — faithful-IIT4 collective-Φ")
    print(f"N_TOT={N_TOT} d0={D0} d1={D1} connector={CONN} pad={PAD} dim={DIM} ticks={T} seeds={SEEDS}")
    print(f"W_CONN={W_CONN}  faithful IIT4 Φ (exact MIP-EI, n<=8); MARGIN={MARGIN} TOL={TOL}")
    print("=" * 84)

    phi = {}  # phi[seed][arm] = float
    for seed in SEEDS:
        phi[seed] = {}
        for arm in ARMS:
            traj = build_arm(seed, arm)
            p = faithful_phi(traj, f"{arm}_s{seed}")
            phi[seed][arm] = p
            print(f"  seed {seed} {arm:>12}: Φ={p}")
        print("-" * 84)

    # ── FROZEN BARS ──────────────────────────────────────────────────────────
    def P(s, a): return phi[s][a]

    # R1 CONNECTOR-LIFT: Φ(B_connector) − Φ(W0_floor) >= MARGIN, all seeds
    r1_per = {s: (P(s,"B_connector") is not None and P(s,"W0_floor") is not None
                  and P(s,"B_connector") - P(s,"W0_floor") >= MARGIN) for s in SEEDS}
    r1 = all(r1_per.values())

    # R2 BEATS-REDUNDANT: Φ(B_connector) − Φ(B_redundant) >= MARGIN, all seeds (H_1350-escape)
    r2_per = {s: (P(s,"B_connector") is not None and P(s,"B_redundant") is not None
                  and P(s,"B_connector") - P(s,"B_redundant") >= MARGIN) for s in SEEDS}
    r2 = all(r2_per.values())

    # R3 EARNED: Φ(SHUFFLE) <= Φ(W0_floor) + TOL, all seeds
    r3_per = {s: (P(s,"SHUFFLE") is not None and P(s,"W0_floor") is not None
                  and P(s,"SHUFFLE") <= P(s,"W0_floor") + TOL) for s in SEEDS}
    r3 = all(r3_per.values())

    green = r1 and r2 and r3
    n_r1, n_r2, n_r3 = sum(r1_per.values()), sum(r2_per.values()), sum(r3_per.values())

    if green:
        verdict = "GREEN_ESCAPES_REDUNDANCY"
    elif r1 and not r2:
        verdict = "PARTIAL_REDUNDANCY_NOT_BEATEN"   # connector beats floor but NOT redundant copy
    elif n_r1 == 2 or n_r2 == 2:
        verdict = "SEED_FRAGILE"
    elif not r3:
        verdict = "WALL_NOT_EARNED"                 # shuffle did not collapse
    elif not r1:
        verdict = "CONNECTOR_NULL"                  # connector does not even beat the floor
    else:
        verdict = "PARTIAL"

    print("=" * 84)
    print(f"R1 CONNECTOR-LIFT  (Φ(B_connector) − Φ(W0_floor)    >= {MARGIN} EVERY seed): {'PASS' if r1 else 'FAIL'}")
    for s in SEEDS:
        d = None if (P(s,"B_connector") is None or P(s,"W0_floor") is None) else round(P(s,"B_connector")-P(s,"W0_floor"),4)
        print(f"     seed {s}: Φ_conn={P(s,'B_connector')} Φ_floor={P(s,'W0_floor')} lift={d}  {'PASS' if r1_per[s] else 'FAIL'}")
    print(f"R2 BEATS-REDUNDANT (Φ(B_connector) − Φ(B_redundant) >= {MARGIN} EVERY seed) [H_1350-escape]: {'PASS' if r2 else 'FAIL'}")
    for s in SEEDS:
        d = None if (P(s,"B_connector") is None or P(s,"B_redundant") is None) else round(P(s,"B_connector")-P(s,"B_redundant"),4)
        print(f"     seed {s}: Φ_conn={P(s,'B_connector')} Φ_redund={P(s,'B_redundant')} gap={d}  {'PASS' if r2_per[s] else 'FAIL'}")
    print(f"R3 EARNED          (Φ(SHUFFLE) <= Φ(W0_floor) + {TOL} EVERY seed): {'PASS' if r3 else 'FAIL'}")
    for s in SEEDS:
        print(f"     seed {s}: Φ_shuffle={P(s,'SHUFFLE')} Φ_floor={P(s,'W0_floor')}  {'PASS' if r3_per[s] else 'FAIL'}")
    print(f"VERDICT: {verdict}  (R1 {n_r1}/3, R2 {n_r2}/3, R3 {n_r3}/3)")

    out = {
        "id": "H_1356", "slug": "hive-cell-roles", "verdict": verdict,
        "seeds": SEEDS, "N_tot": N_TOT, "d0": D0, "d1": D1, "connector": CONN, "pad": PAD,
        "dim": DIM, "ticks": T, "W_conn": W_CONN, "margin": MARGIN, "tol": TOL,
        "phi_faithful_iit4": {str(s): {a: phi[s][a] for a in ARMS} for s in SEEDS},
        "bars": {"R1_connector_lift": bool(r1), "R2_beats_redundant": bool(r2), "R3_earned": bool(r3)},
        "r1_per_seed": {str(s): bool(r1_per[s]) for s in SEEDS},
        "r2_per_seed": {str(s): bool(r2_per[s]) for s in SEEDS},
        "r3_per_seed": {str(s): bool(r3_per[s]) for s in SEEDS},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n<=8)",
    }
    print("\nRESULT_JSON=" + json.dumps(out))
    return out


if __name__ == "__main__":
    main()
