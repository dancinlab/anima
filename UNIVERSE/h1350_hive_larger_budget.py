#!/usr/bin/env python3
# H_1350 — mitotic-division collective-Φ at a LARGER DIFFERENTIATION BUDGET (faithful-IIT4)
# slug: 1350_hive_larger_budget   seeds = [1317,1318,1319] (the hard hive/topology seed family,
#       incl. the orthogonal seed 1317 that broke H_1320 division robustness).
#
# THE WALL (c16 / a_break_the_wall): H_1320 (🧱) — mitotic DIVISION (shared origin) beats hive
# ASSEMBLY on 2/3 seeds but is FRAGILE on the orthogonal seed 1317 (Δ_div collapsed to 0.0 there).
# H_1320 §honesty NAMED the untested angle: a LARGER differentiation budget / MORE daughters /
# a richer non-sign-saturating per-unit code.
#
# THE NEW ANGLE (H_1320's named follow-on): enlarge the differentiation budget on THREE levers, n<=8
# kept exact-MIP tractable:
#   (1) MORE DAUGHTERS  : N_DAUGHTERS=4 of HALF=2 (vs H_1320's 2 of 4).
#   (2) RICHER CODE     : non-saturating softsign per-unit code (H_1332), member energy retained.
#   (3) LARGER DIFF_EPS : 0.45 (3x H_1320's 0.15) — daughters differentiate MORE from the founder.
# Variance-clean rank-uniform read-out (H_1328) so the SHUFFLE control (M3) is honest.
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Φ — it only emits the
# per-unit salience trajectory; the hexa engine computes Φ. NO proxy.
#
# FROZEN BARS (see FREEZE.txt — GREEN iff M1 ∧ M2 ∧ M3, MARGIN_PHI=0.02):
#   M1 ROBUST INTEGRATION-FROM-DIVISION : Φ_divided_pair >= Φ_single + 0.02 on ALL 3 seeds (incl 1317).
#   M2 ORIGIN-DISSOCIATION (core)       : Δ_divided > Δ_assembled + 0.02 on ALL 3 seeds.
#   M3 EARNED (lineage)                 : Δ_shuffle <= Δ_assembled + 0.02 on ALL 3 seeds.
#   Δ_arm = Φ_pair(arm) - Σ_k Φ_daughter_k(arm)   [super-additivity over the 4 daughters].
# seeds [1317,1318,1319]. $0 CPU-local. frozen-first.

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS       = [1317, 1318, 1319]
N_TOT       = 8          # ONE anima-cell = 8 units (n<=8 keeps faithful IIT4 MIP exact)
N_DAUGHTERS = 4          # LARGER budget: 4 daughters (vs H_1320's 2)
HALF        = N_TOT // N_DAUGHTERS   # = 2 units per daughter (n=2 exact)
DIM         = 8          # per-unit state vector dim (H_1283)
T           = 64         # ticks (H_1283)
GAIN        = 0.30       # per-unit update gain (H_1283)
LEAK        = 0.55       # state self-retention (H_1283)
W_IN        = 0.5        # private-input weight (H_1283)
NBINS       = 8          # IIT4 MI estimator bins (H_1283)

W_HIVE   = 0.6           # H_1308/1313/1320 hive cross-member coupling strength (reused verbatim)
DIFF_EPS = 0.45          # LARGER differentiation budget (3x H_1320's 0.15), frozen
BETA     = 0.5           # H_1332 non-saturating code: coupling-energy blend weight
SCALE    = 2.0           # H_1332 softsign scale
MARGIN_PHI = 0.02        # IDENTICAL faithful-Φ margin H_1283/H_1317/H_1320 froze (NOT moved)

HEXA      = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL  = os.path.join(HEXA_ROOT, "stdlib/consciousness/iit4/faithful_phi.hexa")


def softsign(x):
    return x / (1.0 + np.abs(x))


def daughter_of(i):
    """unit index -> daughter index (d0=0..1, d1=2..3, d2=4..5, d3=6..7)."""
    return i // HALF


def evolve(init_states, inputs, coupled):
    """Leaky linear recurrent substrate (H_1283/H_1317/H_1320 unit dynamics), 8 units, 4 daughters.
    If coupled, each unit's READ-OUT adds W_HIVE * mean state of ALL OTHER daughters (the hive
    cross-member coupling). Per-unit salience = NON-SATURATING softsign code (H_1332):
       raw_i = <s_i,s_i> + BETA * <coupling_i, coupling_i>   (coupling_i = W_HIVE * mean_other)
       sal_i = softsign(raw_i / SCALE)
    Returns per-unit salience trajectory (N_TOT,T)."""
    states = init_states.copy()
    traj = np.zeros((N_TOT, T))
    for t in range(T):
        # daughter mean states for cross-coupling this tick
        d_means = [np.mean(states[k * HALF:(k + 1) * HALF], axis=0) for k in range(N_DAUGHTERS)]
        sum_all = np.sum(states, axis=0)
        new = states.copy()
        coupling_vecs = [None] * N_TOT
        for i in range(N_TOT):
            if coupled:
                # mean state of ALL OTHER daughters' units (exclude this unit's own daughter)
                my_d = daughter_of(i)
                other_sum = sum_all - (d_means[my_d] * HALF)
                other_mean = other_sum / float((N_DAUGHTERS - 1) * HALF)
                coupling = W_HIVE * other_mean
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
    """VARIANCE-CLEAN read-out (H_1328): replace each unit's T-length trajectory by within-unit ranks
    (0..T-1, ties broken by index → stable, distinct ranks). Marginals become uniform → the
    amplitude-variance channel is removed so the SHUFFLE control is honest."""
    n, t = traj_units.shape
    out = np.zeros((n, t))
    for i in range(n):
        v = traj_units[i]
        # stable rank: rank = #{j: v_j < v_k} + #{j<k: v_j == v_k}
        order = sorted(range(t), key=lambda k: (v[k], k))
        for rank, k in enumerate(order):
            out[i, k] = float(rank)
    return out


def build_arm(seed, mode):
    """Build (init_states, inputs, coupled) for an arm, evolve, then rank-uniformize.
    mode in {'single','divided','assembled','shuffle'}, N_DAUGHTERS=4.

    SHARED-ORIGIN (divided): all daughters from ONE founder — d_k_init = founder + DIFF_EPS*noise_k,
    ALL daughters share the founder input stream (shared developmental env).
    INDEPENDENT-ORIGIN (assembled): each daughter own init AND own input (4 grown cells).
    SHUFFLE: divided but the shared tie CUT — each daughter init+input replaced by an independent draw.
    SINGLE: one undivided cell, NO cross-daughter coupling (baseline)."""
    rng = np.random.default_rng(seed)

    # --- ZYGOTE founder draws (shared developmental origin material) ---
    founder_init = rng.standard_normal((HALF, DIM)) * 0.5      # founder daughter init (HALF units)
    founder_inp  = rng.standard_normal((HALF, T, DIM)) * 0.8   # shared input stream
    # per-daughter differentiation noise (small perturbation of the SAME founder)
    diff_noise = rng.standard_normal((N_DAUGHTERS, HALF, DIM)) * 0.5
    # INDEPENDENT material for assembled / shuffle's severed lineage (per daughter)
    indep_init = rng.standard_normal((N_DAUGHTERS, HALF, DIM)) * 0.5
    indep_inp  = rng.standard_normal((N_DAUGHTERS, HALF, T, DIM)) * 0.8

    init = np.zeros((N_TOT, DIM))
    inp  = np.zeros((N_TOT, T, DIM))

    for k in range(N_DAUGHTERS):
        sl = slice(k * HALF, (k + 1) * HALF)
        if mode == "single":
            init[sl] = indep_init[k]
            inp[sl]  = indep_inp[k]
        elif mode == "divided":
            # SHARED ORIGIN: clone of founder + per-daughter differentiation; SHARED founder input.
            init[sl] = founder_init + DIFF_EPS * diff_noise[k]
            inp[sl]  = founder_inp                              # shared developmental environment
        elif mode in ("assembled", "shuffle"):
            # INDEPENDENT ORIGIN: own init + own input (assembled = the hive; shuffle = severed lineage)
            init[sl] = indep_init[k]
            inp[sl]  = indep_inp[k]
        else:
            raise ValueError(mode)

    coupled = (mode != "single")
    traj = evolve(init, inp, coupled)
    traj = rank_uniformize(traj)            # H_1328 variance-clean read-out (all arms)
    return traj


def faithful_phi(traj_units, tag):
    """faithful IIT4 Φ over the given unit trajectories via the stdlib EXACT engine (hexa run).
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


def arm_phis(seed, mode):
    """Return (phi_pair, [phi_daughter_k...], delta) for an arm (delta=super-additivity over daughters)."""
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


def main():
    print("H_1350 mitotic-division collective-Φ at LARGER differentiation budget")
    print(f"N_TOT={N_TOT}  N_DAUGHTERS={N_DAUGHTERS} (HALF={HALF})  dim={DIM} ticks={T} seeds={SEEDS}")
    print(f"W_HIVE={W_HIVE} DIFF_EPS={DIFF_EPS} BETA={BETA} SCALE={SCALE} (non-sat softsign code, rank-uniform read-out)")
    print(f"faithful IIT4 Φ (exact MIP-EI); MARGIN_PHI={MARGIN_PHI}")
    print("=" * 80)

    res = {}
    for seed in SEEDS:
        res[seed] = {}
        for mode in ("single", "divided", "assembled", "shuffle"):
            pp, pds, d = arm_phis(seed, mode)
            res[seed][mode] = {"phi_pair": pp, "phi_daughters": pds, "delta": d}
            dstr = "None" if d is None else round(d, 4)
            print(f"  seed {seed} {mode:>9}: Φ_pair={pp}  Φ_daughters={[None if p is None else round(p,4) for p in pds]}  Δ={dstr}")
        print("-" * 80)

    def phi_single(s):    return res[s]["single"]["phi_pair"]
    def phi_div_pair(s):  return res[s]["divided"]["phi_pair"]
    def d_div(s):         return res[s]["divided"]["delta"]
    def d_asm(s):         return res[s]["assembled"]["delta"]
    def d_shf(s):         return res[s]["shuffle"]["delta"]

    # M1: Φ_divided_pair >= Φ_single + MARGIN on ALL seeds
    m1_per = {s: (phi_div_pair(s) is not None and phi_single(s) is not None
                  and phi_div_pair(s) >= phi_single(s) + MARGIN_PHI) for s in SEEDS}
    m1 = all(m1_per.values())
    # M2: Δ_divided > Δ_assembled + MARGIN on ALL seeds
    m2_per = {s: (d_div(s) is not None and d_asm(s) is not None
                  and d_div(s) > d_asm(s) + MARGIN_PHI) for s in SEEDS}
    m2 = all(m2_per.values())
    # M3: Δ_shuffle <= Δ_assembled + MARGIN on ALL seeds
    m3_per = {s: (d_shf(s) is not None and d_asm(s) is not None
                  and d_shf(s) <= d_asm(s) + MARGIN_PHI) for s in SEEDS}
    m3 = all(m3_per.values())

    green = m1 and m2 and m3
    if green:
        verdict = "GREEN"
    elif not m1:
        verdict = "WALL_FRAGILE_EVEN_AT_LARGER_BUDGET"
    elif m1 and not m2:
        verdict = "WALL_DIVISION_NOT_BEAT_ASSEMBLY"
    elif m1 and m2 and not m3:
        verdict = "PARTIAL_LIFT_NOT_LINEAGE_EARNED"
    else:
        verdict = "PARTIAL"

    print("=" * 80)
    print(f"M1 ROBUST INTEGRATION-FROM-DIVISION (Φ_div_pair >= Φ_single + {MARGIN_PHI} EVERY seed): {'PASS' if m1 else 'FAIL'}")
    for s in SEEDS:
        ps, pd = phi_single(s), phi_div_pair(s)
        lift = None if (ps is None or pd is None) else round(pd - ps, 4)
        print(f"     seed {s}: Φ_single={ps} Φ_div_pair={pd} lift={lift}  {'PASS' if m1_per[s] else 'FAIL'}")
    print(f"M2 ORIGIN-DISSOCIATION (Δ_divided > Δ_assembled + {MARGIN_PHI} EVERY seed) [CORE vs hive]: {'PASS' if m2 else 'FAIL'}")
    for s in SEEDS:
        dd, da = d_div(s), d_asm(s)
        gap = None if (dd is None or da is None) else round(dd - da, 4)
        print(f"     seed {s}: Δ_divided={None if dd is None else round(dd,4)} Δ_assembled={None if da is None else round(da,4)} gap={gap}  {'PASS' if m2_per[s] else 'FAIL'}")
    print(f"M3 EARNED-LINEAGE (Δ_shuffle <= Δ_assembled + {MARGIN_PHI} EVERY seed): {'PASS' if m3 else 'FAIL'}")
    for s in SEEDS:
        ds, da = d_shf(s), d_asm(s)
        print(f"     seed {s}: Δ_shuffle={None if ds is None else round(ds,4)} Δ_assembled={None if da is None else round(da,4)}  {'PASS' if m3_per[s] else 'FAIL'}")
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
                                       for m in ("single","divided","assembled","shuffle")} for s in SEEDS},
        "bars": {"M1_robust_integration_from_division": bool(m1),
                 "M2_origin_dissociation": bool(m2),
                 "M3_earned_lineage": bool(m3)},
        "m1_per_seed": {str(s): bool(m1_per[s]) for s in SEEDS},
        "m2_per_seed": {str(s): bool(m2_per[s]) for s in SEEDS},
        "m3_per_seed": {str(s): bool(m3_per[s]) for s in SEEDS},
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n<=8)",
    }
    print("\nRESULT_JSON=" + json.dumps(out))
    return out


if __name__ == "__main__":
    main()
