#!/usr/bin/env python3
# H_1350 — mitotic-division collective-Phi at a LARGER DIFFERENTIATION BUDGET (faithful-IIT4)
# slug: 1350_hive_larger_budget   seeds = [1317,1318,1319] (the hard hive/topology seed family,
#       incl. the orthogonal seed 1317 that broke H_1320 division robustness).
#
# THE WALL (c16 / a_break_the_wall): H_1320 (WALL) -- mitotic DIVISION (shared origin) beats hive
# ASSEMBLY on 2/3 seeds but is FRAGILE on the orthogonal seed 1317 (delta_div collapsed to 0.0 there).
# H_1320 NAMED the untested angle: a LARGER differentiation budget / MORE daughters / a richer
# non-sign-saturating per-unit code. OPEN: does the LARGER division budget make collective-Phi from
# division ROBUST across all 3 seeds, or inherit the same seed-fragility wall?
#
# THE NEW ANGLE (H_1320 follow-on): enlarge the differentiation budget on THREE levers, n<=8 exact:
#   (1) MORE DAUGHTERS  : N_DAUGHTERS=4 of HALF=2 (vs H_1320's 2 of 4).
#   (2) RICHER CODE     : non-saturating softsign per-unit code (H_1332), member energy retained.
#   (3) LARGER DIFF_EPS : 0.45 (3x H_1320's 0.15) -- daughters differentiate MORE from the founder.
# Variance-clean rank-uniform read-out (H_1328) so the SHUFFLE control (R2c) is honest.
#
# ====================== HONESTY: THE CONFOUND THIS CARD MUST RULE OUT =========================
# faithful IIT4 Phi* = cross-cut MI at the MIP / min(|A|,|B|): driven by PAIRWISE MUTUAL INFORMATION
# between units. In DIVIDED all daughters share ONE founder input stream, so the 8 units are strongly
# CORRELATED -> high pairwise MI -> high Phi. That high Phi could be SHARED-INPUT REDUNDANCY, not
# integration EARNED by the cross-daughter coupling. ASSEMBLED + SHUFFLE BOTH switch to INDEPENDENT
# inputs, so they cannot dissociate "shared origin (coupling)" from "shared input correlation". A prior
# attempt's GREEN rested only on those two -> NOT earned. This card adds the DECISIVE control:
#   C2 SHARED-INPUT-DECOUPLED (W=0): same shared founder input + shared origin as DIVIDED, but
#      cross-daughter coupling W_HIVE := 0. Isolates the redundancy floor from shared input alone.
#   => R2b EARNED requires Delta_divided to EXCEED the shared-input-decoupled floor (lift must be
#      COUPLING-dependent, not just shared-input correlation). If divided lift does NOT clear the
#      shared-input-decoupled floor, "integration-from-division" is a redundancy artifact -> honest
#      WALL (c9), consistent with the measure/size/substrate-agnostic Phi wall.
# =============================================================================================
#
# Phi = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Phi -- it only emits the
# per-unit salience trajectory; the hexa engine computes Phi. NO proxy.
#
# FROZEN BARS (see FREEZE.txt -- GREEN iff R1 AND R2, MARGIN_PHI=0.02):
#   R1 ROBUST INTEGRATION-FROM-DIVISION : Phi_divided_pair >= Phi_single + 0.02 on ALL 3 seeds.
#   R2 EARNED (decisive conjunction, ALL 3 seeds):
#        R2a ORIGIN-DISSOCIATION : Delta_divided > Delta_assembled + 0.02   (beats the hive).
#        R2b COUPLING-EARNED     : Delta_divided > Delta_shared_decoupled + 0.02  (KEY: beats the
#                                  shared-input redundancy floor -> lift is COUPLING-dependent).
#        R2c SHUFFLE-COLLAPSE    : Delta_shuffle <= Delta_assembled + 0.02   (broken lineage collapses).
#   R3 (report-only, non-gating): does the LARGER budget change seed-fragility vs H_1320's small budget?
#   Delta_arm = Phi_pair(arm) - Sum_k Phi_daughter_k(arm).
# seeds [1317,1318,1319]. $0 CPU-local. frozen-first. NO tune-to-green (c9/p7). DIRECTIONAL (numpy
# mirror; faithful-Phi leg IS the real exact MIP-EI; engine-transfer to live CORE/pure_field UNVERIFIED).

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS       = [1317, 1318, 1319]
N_TOT       = 8
N_DAUGHTERS = 4
HALF        = N_TOT // N_DAUGHTERS
DIM         = 8
T           = 64
GAIN        = 0.30
LEAK        = 0.55
W_IN        = 0.5
NBINS       = 8

W_HIVE   = 0.6
DIFF_EPS = 0.45
BETA     = 0.5
SCALE    = 2.0
MARGIN_PHI = 0.02

HEXA      = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL  = os.path.join(HEXA_ROOT, "stdlib/consciousness/iit4/faithful_phi.hexa")


def softsign(x):
    return x / (1.0 + np.abs(x))


def daughter_of(i):
    return i // HALF


def evolve(init_states, inputs, w_hive):
    states = init_states.copy()
    traj = np.zeros((N_TOT, T))
    for t in range(T):
        d_means = [np.mean(states[k * HALF:(k + 1) * HALF], axis=0) for k in range(N_DAUGHTERS)]
        sum_all = np.sum(states, axis=0)
        new = states.copy()
        coupling_vecs = [None] * N_TOT
        for i in range(N_TOT):
            if w_hive != 0.0:
                my_d = daughter_of(i)
                other_sum = sum_all - (d_means[my_d] * HALF)
                other_mean = other_sum / float((N_DAUGHTERS - 1) * HALF)
                coupling = w_hive * other_mean
            else:
                coupling = np.zeros(DIM)
            coupling_vecs[i] = coupling
            new[i] = LEAK * states[i] + GAIN * (W_IN * inputs[i, t] + coupling)
        states = new
        for i in range(N_TOT):
            energy = float(np.dot(states[i], states[i]))
            c = coupling_vecs[i]
            raw = energy + BETA * float(np.dot(c, c))
            traj[i, t] = softsign(raw / SCALE)
    return traj


def rank_uniformize(traj_units):
    n, t = traj_units.shape
    out = np.zeros((n, t))
    for i in range(n):
        v = traj_units[i]
        order = sorted(range(t), key=lambda k: (v[k], k))
        for rank, k in enumerate(order):
            out[i, k] = float(rank)
    return out


def build_arm(seed, mode):
    rng = np.random.default_rng(seed)
    founder_init = rng.standard_normal((HALF, DIM)) * 0.5
    founder_inp  = rng.standard_normal((HALF, T, DIM)) * 0.8
    diff_noise   = rng.standard_normal((N_DAUGHTERS, HALF, DIM)) * 0.5
    indep_init = rng.standard_normal((N_DAUGHTERS, HALF, DIM)) * 0.5
    indep_inp  = rng.standard_normal((N_DAUGHTERS, HALF, T, DIM)) * 0.8

    init = np.zeros((N_TOT, DIM))
    inp  = np.zeros((N_TOT, T, DIM))

    for k in range(N_DAUGHTERS):
        sl = slice(k * HALF, (k + 1) * HALF)
        if mode == "single":
            init[sl] = indep_init[k]; inp[sl] = indep_inp[k]
        elif mode in ("divided", "shared_decoupled"):
            init[sl] = founder_init + DIFF_EPS * diff_noise[k]
            inp[sl]  = founder_inp
        elif mode in ("assembled", "shuffle"):
            init[sl] = indep_init[k]; inp[sl] = indep_inp[k]
        else:
            raise ValueError(mode)

    if mode in ("single", "shared_decoupled"):
        w = 0.0
    else:
        w = W_HIVE

    traj = evolve(init, inp, w)
    traj = rank_uniformize(traj)
    return traj


def faithful_phi(traj_units, tag):
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


def arm_phis(seed, mode):
    traj = build_arm(seed, mode)
    phi_pair = faithful_phi(traj, f"{mode}_pair_s{seed}")
    phi_ds = []
    for k in range(N_DAUGHTERS):
        sl = slice(k * HALF, (k + 1) * HALF)
        phi_ds.append(faithful_phi(traj[sl], f"{mode}_d{k}_s{seed}"))
    delta = None
    if phi_pair is not None and all(p is not None for p in phi_ds):
        delta = phi_pair - sum(phi_ds)
    return phi_pair, phi_ds, delta


ARMS = ("single", "divided", "assembled", "shuffle", "shared_decoupled")


def main():
    print("H_1350 mitotic-division collective-Phi at LARGER differentiation budget")
    print(f"N_TOT={N_TOT}  N_DAUGHTERS={N_DAUGHTERS} (HALF={HALF})  dim={DIM} ticks={T} seeds={SEEDS}")
    print(f"W_HIVE={W_HIVE} DIFF_EPS={DIFF_EPS} BETA={BETA} SCALE={SCALE} (non-sat softsign code, rank-uniform read-out)")
    print(f"faithful IIT4 Phi (exact MIP-EI); MARGIN_PHI={MARGIN_PHI}")
    print("ARMS: single | divided | assembled(hive) | shuffle | shared_decoupled(W=0 redundancy floor)")
    print("=" * 80)

    res = {}
    for seed in SEEDS:
        res[seed] = {}
        for mode in ARMS:
            pp, pds, d = arm_phis(seed, mode)
            res[seed][mode] = {"phi_pair": pp, "phi_daughters": pds, "delta": d}
            dstr = "None" if d is None else round(d, 4)
            print(f"  seed {seed} {mode:>16}: Phi_pair={pp}  Phi_daughters={[None if p is None else round(p,4) for p in pds]}  D={dstr}")
        print("-" * 80)

    def phi_single(s):    return res[s]["single"]["phi_pair"]
    def phi_div_pair(s):  return res[s]["divided"]["phi_pair"]
    def d_div(s):         return res[s]["divided"]["delta"]
    def d_asm(s):         return res[s]["assembled"]["delta"]
    def d_shf(s):         return res[s]["shuffle"]["delta"]
    def d_sdc(s):         return res[s]["shared_decoupled"]["delta"]

    r1_per = {s: (phi_div_pair(s) is not None and phi_single(s) is not None
                  and phi_div_pair(s) >= phi_single(s) + MARGIN_PHI) for s in SEEDS}
    r1 = all(r1_per.values())
    r2a_per = {s: (d_div(s) is not None and d_asm(s) is not None
                   and d_div(s) > d_asm(s) + MARGIN_PHI) for s in SEEDS}
    r2b_per = {s: (d_div(s) is not None and d_sdc(s) is not None
                   and d_div(s) > d_sdc(s) + MARGIN_PHI) for s in SEEDS}
    r2c_per = {s: (d_shf(s) is not None and d_asm(s) is not None
                   and d_shf(s) <= d_asm(s) + MARGIN_PHI) for s in SEEDS}
    r2a, r2b, r2c = all(r2a_per.values()), all(r2b_per.values()), all(r2c_per.values())
    r2 = r2a and r2b and r2c

    green = r1 and r2
    if green:
        verdict = "GREEN"
    elif not r1:
        verdict = "WALL_FRAGILE_EVEN_AT_LARGER_BUDGET"
    elif r1 and not r2b:
        verdict = "WALL_REDUNDANCY_ARTIFACT_NOT_COUPLING_EARNED"
    elif r1 and r2b and not r2a:
        verdict = "WALL_DIVISION_NOT_BEAT_ASSEMBLY"
    elif r1 and r2a and r2b and not r2c:
        verdict = "PARTIAL_LIFT_NOT_LINEAGE_EARNED"
    else:
        verdict = "PARTIAL"

    print("=" * 80)
    print(f"R1 ROBUST INTEGRATION-FROM-DIVISION (Phi_div_pair >= Phi_single + {MARGIN_PHI} EVERY seed): {'PASS' if r1 else 'FAIL'}")
    for s in SEEDS:
        ps, pd = phi_single(s), phi_div_pair(s)
        lift = None if (ps is None or pd is None) else round(pd - ps, 4)
        print(f"     seed {s}: Phi_single={ps} Phi_div_pair={pd} lift={lift}  {'PASS' if r1_per[s] else 'FAIL'}")
    print(f"R2a ORIGIN-DISSOCIATION (D_divided > D_assembled + {MARGIN_PHI} EVERY seed): {'PASS' if r2a else 'FAIL'}")
    for s in SEEDS:
        dd, da = d_div(s), d_asm(s)
        gap = None if (dd is None or da is None) else round(dd - da, 4)
        print(f"     seed {s}: D_divided={None if dd is None else round(dd,4)} D_assembled={None if da is None else round(da,4)} gap={gap}  {'PASS' if r2a_per[s] else 'FAIL'}")
    print(f"R2b COUPLING-EARNED [KEY] (D_divided > D_shared_decoupled + {MARGIN_PHI} EVERY seed): {'PASS' if r2b else 'FAIL'}")
    for s in SEEDS:
        dd, ds = d_div(s), d_sdc(s)
        gap = None if (dd is None or ds is None) else round(dd - ds, 4)
        print(f"     seed {s}: D_divided={None if dd is None else round(dd,4)} D_shared_decoupled={None if ds is None else round(ds,4)} gap={gap}  {'PASS' if r2b_per[s] else 'FAIL'}")
    print(f"R2c EARNED-LINEAGE (D_shuffle <= D_assembled + {MARGIN_PHI} EVERY seed): {'PASS' if r2c else 'FAIL'}")
    for s in SEEDS:
        ds, da = d_shf(s), d_asm(s)
        print(f"     seed {s}: D_shuffle={None if ds is None else round(ds,4)} D_assembled={None if da is None else round(da,4)}  {'PASS' if r2c_per[s] else 'FAIL'}")
    print(f"VERDICT: {verdict}")

    out = {
        "id": "H_1350", "slug": "1350_hive_larger_budget", "verdict": verdict,
        "seeds": SEEDS, "N_tot": N_TOT, "n_daughters": N_DAUGHTERS, "half": HALF,
        "dim": DIM, "ticks": T, "W_hive": W_HIVE, "diff_eps": DIFF_EPS,
        "beta": BETA, "scale": SCALE, "margin_phi": MARGIN_PHI,
        "readout": "rank-uniform (H_1328) + non-saturating softsign code (H_1332)",
        "phi_faithful_iit4": {str(s): {m: {"phi_pair": res[s][m]["phi_pair"],
                                           "phi_daughters": res[s][m]["phi_daughters"],
                                           "delta": res[s][m]["delta"]}
                                       for m in ARMS} for s in SEEDS},
        "bars": {"R1_robust_integration_from_division": bool(r1),
                 "R2a_origin_dissociation": bool(r2a),
                 "R2b_coupling_earned": bool(r2b),
                 "R2c_earned_lineage": bool(r2c),
                 "R2_earned_conjunction": bool(r2)},
        "r1_per_seed": {str(s): bool(r1_per[s]) for s in SEEDS},
        "r2a_per_seed": {str(s): bool(r2a_per[s]) for s in SEEDS},
        "r2b_per_seed": {str(s): bool(r2b_per[s]) for s in SEEDS},
        "r2c_per_seed": {str(s): bool(r2c_per[s]) for s in SEEDS},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n<=8)",
    }
    print("\nRESULT_JSON=" + json.dumps(out))
    return out


if __name__ == "__main__":
    main()
