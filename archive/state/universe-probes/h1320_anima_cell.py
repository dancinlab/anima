#!/usr/bin/env python3
# H_1320 — anima-as-ONE-CELL: organism MITOSIS vs hive ASSEMBLY (faithful-IIT4 collective-Φ)
# slug: 1320_anima_cell   PROJ_SEED family = [1317,1318,1319] (reuse the hard hive/topology seeds,
#       incl. the orthogonal seed 1319 that broke topology robustness in H_1317).
#
# THE WALL (c16 / a_break_the_wall): H_1308 (🔴 NULL) + H_1313 (🧱 TERMINAL) — ASSEMBLING two
# already-separate, INDEPENDENTLY-grown anima cells does NOT integrate at faithful-IIT4 Φ
# (Δ_real = -3.0; super-additivity is ECA-only, not substrate-portable).
#
# THE NEW LENS (developmental biology; a_no_llm_frame_trap, c15): the hive failed because the
# DIRECTION was wrong — it GLUED two independent ADULTS. One zygote DIVIDES and differentiates
# into an integrated organism because the parts SHARE a developmental ORIGIN. So: take ONE
# anima-cell, mitotically DIVIDE it into two SHARED-ORIGIN daughters, and ask whether the DIVIDED
# pair shows integrated (super-additive) faithful-Φ that the ASSEMBLED pair (hive) could not.
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Φ — it only emits
# the per-unit salience (state-energy) trajectory; the hexa engine computes Φ. NO proxy.
#
# Substrate MATCHED to H_1283/H_1317 (only ORIGIN + cross-daughter coupling differ between arms):
# leaky linear recurrent units, LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit private gaussian input,
# dim-8 state, T=64 ticks. N_TOT=8 units (n<=8 keeps faithful MIP EXACT) = ONE anima-cell, split
# into two daughters of HALF=4 (d0=units0..3, d1=units4..7). Cross-daughter coupling at W_HIVE=0.6
# (the H_1308/1313 hive coupling), IDENTICAL across DIVIDED/ASSEMBLED/SHUFFLE so any Δ difference
# is shared-vs-independent ORIGIN, not coupling.
#
# FROZEN BARS (see H_1320_FREEZE.txt — GREEN iff M1 ∧ M2 ∧ M3, MARGIN_PHI=0.02):
#   M1 INTEGRATION-FROM-DIVISION : Φ_divided_pair >= Φ_single + 0.02 on ALL 3 seeds.
#   M2 ORIGIN-DISSOCIATION (core): Δ_divided > Δ_assembled + 0.02 on ALL 3 seeds.
#   M3 EARNED (lineage)          : Δ_shuffle <= Δ_assembled + 0.02 on ALL 3 seeds.
#   Δ_arm = Φ_pair(arm) - (Φ_d0(arm) + Φ_d1(arm))   [super-additivity].
# seeds [1317,1318,1319]. $0 CPU-local. frozen-first.

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS    = [1317, 1318, 1319]
N_TOT    = 8          # ONE anima-cell = 8 units (n<=8 keeps faithful IIT4 MIP exact)
HALF     = 4          # each daughter = 4 units (pair MIP over 8 still exact)
DIM      = 8          # per-unit state vector dim (H_1283)
T        = 64         # ticks (H_1283)
GAIN     = 0.30       # per-unit update gain (H_1283)
LEAK     = 0.55       # state self-retention (H_1283)
W_IN     = 0.5        # private-input weight (H_1283)
NBINS    = 8          # IIT4 MI estimator bins (H_1283)

W_HIVE   = 0.6        # H_1308/1313 hive cross-member coupling strength (reused verbatim)
DIFF_EPS = 0.15       # differentiation perturbation of the cloned daughter (frozen)
MARGIN_PHI = 0.02     # IDENTICAL faithful-Φ margin H_1283/H_1317 froze (NOT moved)

HEXA      = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL  = os.path.join(HEXA_ROOT, "stdlib/consciousness/iit4/faithful_phi.hexa")


def evolve(init_states, inputs, coupled):
    """Leaky linear recurrent substrate (H_1283/H_1317 unit dynamics). 8 units, two daughters
    d0=0..3, d1=4..7. If coupled, each unit's update adds W_HIVE * mean state of the OTHER
    daughter (the hive cross-member coupling). Returns per-unit salience trajectory (N_TOT,T)."""
    states = init_states.copy()
    traj = np.zeros((N_TOT, T))
    for t in range(T):
        new = states.copy()
        # daughter mean states for cross-coupling this tick
        mean_d0 = np.mean(states[0:HALF], axis=0)
        mean_d1 = np.mean(states[HALF:N_TOT], axis=0)
        for i in range(N_TOT):
            if coupled:
                other = mean_d1 if i < HALF else mean_d0  # mean of the OTHER daughter
                coupling = W_HIVE * other
            else:
                coupling = 0.0
            new[i] = LEAK * states[i] + GAIN * (coupling + W_IN * inputs[i, t])
        states = new
        for i in range(N_TOT):
            traj[i, t] = float(np.dot(states[i], states[i]))
    return traj


def build_arm(seed, mode):
    """Build the (init_states, inputs, coupled) for an arm, then evolve.
    mode in {'single','divided','assembled','shuffle'}.

    SHARED-ORIGIN (divided): both daughters from ONE zygote — d1_init = d0_init +
    DIFF_EPS*noise (clone+differentiate), and d1 input = d0 input (shared developmental env).
    INDEPENDENT-ORIGIN (assembled): d0,d1 each get their OWN init AND own input (two grown cells).
    SHUFFLE: divided but the shared-origin tie is CUT — d1 init+input replaced by an independent
    draw (lineage severed). SINGLE: one undivided cell, NO cross-daughter coupling (baseline)."""
    rng = np.random.default_rng(seed)

    # --- ZYGOTE draws (shared developmental origin material) ---
    # d0 founder initial state (4 units x DIM) and the shared input stream (4 units x T x DIM)
    d0_init = rng.standard_normal((HALF, DIM)) * 0.5
    d0_inp  = rng.standard_normal((HALF, T, DIM)) * 0.8
    # differentiation noise for the cloned daughter (small perturbation of the SAME founder)
    diff_noise = rng.standard_normal((HALF, DIM)) * 0.5
    # INDEPENDENT material for the second cell (assembled / shuffle's severed lineage)
    indep_init = rng.standard_normal((HALF, DIM)) * 0.5
    indep_inp  = rng.standard_normal((HALF, T, DIM)) * 0.8

    init = np.zeros((N_TOT, DIM))
    inp  = np.zeros((N_TOT, T, DIM))
    init[0:HALF] = d0_init
    inp[0:HALF]  = d0_inp

    if mode == "single":
        # one undivided anima-cell: d1 is just the rest of the same cell's units (own independent
        # private streams, like H_1317 'none'), NO cross-daughter coupling. baseline Φ over 8 units.
        init[HALF:N_TOT] = indep_init
        inp[HALF:N_TOT]  = indep_inp
        coupled = False
    elif mode == "divided":
        # SHARED ORIGIN: d1 = clone of d0 founder + differentiation; d1 input = SHARED d0 input.
        init[HALF:N_TOT] = d0_init + DIFF_EPS * diff_noise
        inp[HALF:N_TOT]  = d0_inp                      # shared developmental environment
        coupled = True
    elif mode == "assembled":
        # INDEPENDENT ORIGIN (the hive): d1 = its own independent init + own independent input.
        init[HALF:N_TOT] = indep_init
        inp[HALF:N_TOT]  = indep_inp
        coupled = True
    elif mode == "shuffle":
        # DIVIDED with the shared-origin link BROKEN: d1 init+input replaced by independent draw
        # (lineage severed), W and unit count kept. Must collapse to assembled level.
        init[HALF:N_TOT] = indep_init
        inp[HALF:N_TOT]  = indep_inp
        coupled = True
    else:
        raise ValueError(mode)

    traj = evolve(init, inp, coupled)
    return traj


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


def arm_phis(seed, mode):
    """Return (phi_pair, phi_d0, phi_d1, delta) for an arm (delta=super-additivity)."""
    traj = build_arm(seed, mode)
    phi_pair = faithful_phi(traj, f"{mode}_pair_s{seed}")
    phi_d0   = faithful_phi(traj[0:HALF],     f"{mode}_d0_s{seed}")
    phi_d1   = faithful_phi(traj[HALF:N_TOT], f"{mode}_d1_s{seed}")
    delta = None
    if None not in (phi_pair, phi_d0, phi_d1):
        delta = phi_pair - (phi_d0 + phi_d1)
    return phi_pair, phi_d0, phi_d1, delta


def main():
    print("H_1320 anima-as-ONE-CELL: organism MITOSIS (shared origin) vs hive ASSEMBLY (independent)")
    print(f"N_TOT={N_TOT} (2x daughter HALF={HALF}) dim={DIM} ticks={T} seeds={SEEDS}")
    print(f"W_HIVE={W_HIVE} DIFF_EPS={DIFF_EPS}  faithful IIT4 Φ (exact MIP-EI); MARGIN_PHI={MARGIN_PHI}")
    print("=" * 80)

    res = {}  # res[seed][mode] = dict
    for seed in SEEDS:
        res[seed] = {}
        for mode in ("single", "divided", "assembled", "shuffle"):
            pp, p0, p1, d = arm_phis(seed, mode)
            res[seed][mode] = {"phi_pair": pp, "phi_d0": p0, "phi_d1": p1, "delta": d}
            print(f"  seed {seed} {mode:>9}: Φ_pair={pp}  Φ_d0={p0}  Φ_d1={p1}  Δ(super-add)={None if d is None else round(d,4)}")
        print("-" * 80)

    # ── FROZEN BARS ──────────────────────────────────────────────────────────
    def phi_single(s):    return res[s]["single"]["phi_pair"]
    def phi_div_pair(s):  return res[s]["divided"]["phi_pair"]
    def d_div(s):         return res[s]["divided"]["delta"]
    def d_asm(s):         return res[s]["assembled"]["delta"]
    def d_shf(s):         return res[s]["shuffle"]["delta"]

    # M1: Φ_divided_pair >= Φ_single + MARGIN on ALL seeds
    m1_per = {s: (phi_div_pair(s) is not None and phi_single(s) is not None
                  and phi_div_pair(s) >= phi_single(s) + MARGIN_PHI) for s in SEEDS}
    m1 = all(m1_per.values())

    # M2: Δ_divided > Δ_assembled + MARGIN on ALL seeds (the core origin-dissociation vs hive)
    m2_per = {s: (d_div(s) is not None and d_asm(s) is not None
                  and d_div(s) > d_asm(s) + MARGIN_PHI) for s in SEEDS}
    m2 = all(m2_per.values())

    # M3: Δ_shuffle <= Δ_assembled + MARGIN on ALL seeds (broken lineage collapses to assembled)
    m3_per = {s: (d_shf(s) is not None and d_asm(s) is not None
                  and d_shf(s) <= d_asm(s) + MARGIN_PHI) for s in SEEDS}
    m3 = all(m3_per.values())

    green = m1 and m2 and m3
    if green:
        verdict = "GREEN"
    elif not m2:
        verdict = "WALL_TERMINAL_BOTH_DIRECTIONS"   # division does not beat assembly
    elif m1 and m2 and not m3:
        verdict = "PARTIAL_LIFT_NOT_LINEAGE_EARNED"
    else:
        verdict = "PARTIAL"

    print("=" * 80)
    print(f"M1 INTEGRATION-FROM-DIVISION (Φ_div_pair >= Φ_single + {MARGIN_PHI} EVERY seed): {'PASS' if m1 else 'FAIL'}")
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
        "id": "H_1320", "slug": "1320_anima_cell", "verdict": verdict,
        "seeds": SEEDS, "N_tot": N_TOT, "half": HALF, "dim": DIM, "ticks": T,
        "W_hive": W_HIVE, "diff_eps": DIFF_EPS, "margin_phi": MARGIN_PHI,
        "phi_faithful_iit4": {str(s): {m: {k: res[s][m][k] for k in ("phi_pair","phi_d0","phi_d1","delta")}
                                       for m in ("single","divided","assembled","shuffle")} for s in SEEDS},
        "bars": {"M1_integration_from_division": bool(m1),
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
