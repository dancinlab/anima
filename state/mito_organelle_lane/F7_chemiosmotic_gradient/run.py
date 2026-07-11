#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_9279 / F7 — chemiosmotic gradient probe ($0 · numpy · CPU-local)

CLAIM (card §1): extractable emit-work is MAXIMAL at Psi=1/2, and THAT is the
mechanistic reason 1/2 is an attractor.
NULL  (card §1): it is a re-description of the existing A<->G tension — 0 new DOF
                 => dEff ~= 0 => THEATER.

Substrate is anima-faithful (numpy mirrors of core/engine_cli.py, parity-checked below):
  unit lanes      : L=15 lanes per unit (engine layout)
  A-lane = 0, G-lane = 4   (the two lanes the engine's emit drive reads)
  emit drive      : D_u = 0.5*(l0 + l4)                (ci_emit_drive)
  Psi             : fraction of units with D_u >= thr  (tr_psi)
  settle dynamics : topo_apply_meancenter(X, adj, alpha) iterated  (tension_resolve_depth)

CHEMIOSMOTIC MAPPING (the F7 invention):
  membrane potential of a unit = the MAINTAINED A<->G DISEQUILIBRIUM
      V_u = |l0 - l4|      (the "proton-motive force"; A pumps, G leaks)
  flux  = the fraction of units whose channel is open (i.e. Psi itself)
  work  = flux x force, with the force COLLAPSING under load (shared pool).

Two work functionals are evaluated on EVERY arm with IDENTICAL parameters:
  W_kin(psi)  = g*psi * Vm*,  Vm* = p*Vbar0(psi)/(p + g*psi)      [kinetic pump/leak
                shared-pool steady state — NO 1/2 baked in]
  W_ohm(psi)  = psi * Vbar0(psi) * (1 - psi)                      [Ohmic load-line
                ansatz — the textbook "max power at half" — 1/2 IS baked in whenever
                the force Vbar0 is flat. This arm exists precisely to EXPOSE that.]
  Vbar0(psi)  = mean V_u over the recruited (top-psi by drive) set  <- the ONLY place
                substrate information can enter either functional.

ARMS (identical budget: same N, same lane count, same psi grid, same p/g, same seeds,
      same settle depth; controls differ ONLY by the stated ablation):
  EXP      : anima substrate population
  C1       : off-half operating points (same curve; reported as W(1/2) vs W(psi*) delta)
  C2-SHUF  : tautology control — V permuted across units (V<->D relation destroyed,
             marginal preserved). If the curve/argmax is unchanged => the result carries
             ZERO substrate information => pure bookkeeping.
  C3-BERN  : substrate-free control — D and V iid uniform, no anima lanes at all.
  POS-HALF : positive control (ARM-SHOCK) — flat force + W_ohm => argmax MUST be 0.5.
  POS-OFF  : positive control — force decays exp(-4q) => argmax MUST be << 0.5.
             (the two POS arms prove the argmax detector is not hardwired either way)

P2 — THE INDEPENDENT (NON-TAUTOLOGICAL) PREDICTION, card §3 c2:
  If Psi=1/2 is an attractor BECAUSE it is the max-work point, then MOVING the max-work
  point must MOVE the attractor. Two orthogonal substrate knobs are swept:
     rho = corr(A-lane, G-lane) across units  -> reshapes the force-flux curve
     mu  = population lane mean (drive offset) -> reshapes the drive distribution
  PASS  : psi_att tracks psi*_work (they move together under rho).
  FAIL  : double dissociation — rho moves psi*_work but NOT psi_att, while mu moves
          psi_att but NOT psi*_work  =>  work-max and the attractor are independent
          => the work story is a re-description => THEATER.

Frozen hyper-parameters (declared once, NEVER tuned to a result):
  N=1200 units, L=15 lanes, alpha=0.3, settle depth=200, thr=0.5, p=0.5, g=1.0,
  psi grid = 0.05..0.95 step 0.05, seeds = 5 (0..4), knobs rho x mu = 5 x 5.
"""

import json
import os
import sys
from math import erf

os.environ.setdefault("OMP_NUM_THREADS", "2")

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

# ── frozen constants ────────────────────────────────────────────────────────────
N_UNITS = 1200
L_LANES = 15
A_LANE = 0
G_LANE = 4
ALPHA = 0.3
DEPTH = 200
THR = 0.5
PUMP_P = 0.5
COND_G = 1.0
PSI_GRID = np.round(np.arange(0.05, 0.96, 0.05), 4)      # 19 operating points
SEEDS = [0, 1, 2, 3, 4]
RHOS = [-0.8, -0.4, 0.0, 0.4, 0.8]
MUS = [0.35, 0.425, 0.5, 0.575, 0.65]
ADJ_SEED = 9279
GRID_RES = 0.05


# ── engine-faithful ops (numpy mirrors of core/engine_cli.py) ───────────────────
def topo_sym_norm(a):
    d = a.sum(axis=1)
    dinv = np.where(d > 1e-6, 1.0 / np.sqrt(np.maximum(d, 1e-12)), 0.0)
    return dinv[:, None] * a * dinv[None, :]


def topo_row_center(a):
    return a - a.mean(axis=1, keepdims=True)


def topo_apply_meancenter(x, a, alpha):
    """core/engine_cli.py:7260 — mean-centered symmetric-normalised lane coupling."""
    n = a.shape[0]
    ahat = topo_row_center(topo_sym_norm(a))
    mm = alpha * ahat + np.eye(n)
    return x @ mm.T                         # out[t,i] = sum_j x[t,j]*mm[i,j]


def ci_emit_drive(x):
    """core/engine_cli.py:7154 — 0.5*(lane0 + lane4)."""
    return 0.5 * (x[:, A_LANE] + x[:, G_LANE])


def tr_psi(x, thr):
    """core/engine_cli.py:9589 — fraction of the population over the emit threshold."""
    return float(np.mean(ci_emit_drive(x) >= thr))


def engine_parity_check():
    """Prove the numpy mirrors are faithful to the shipped engine ops."""
    try:
        sys.path.insert(0, REPO)
        from core.engine_cli import ci_emit_drive as e_drive
        from core.engine_cli import topo_apply_meancenter as e_mc
        from core.engine_cli import tr_psi as e_psi
    except Exception as exc:
        return {"available": False, "error": str(exc)}
    rng = np.random.default_rng(1)
    x = rng.random((7, L_LANES))
    a = (rng.random((L_LANES, L_LANES)) < 0.4).astype(float)
    a = np.maximum(a, a.T)
    np.fill_diagonal(a, 0.0)
    mine = topo_apply_meancenter(x, a, ALPHA)
    theirs = np.array(e_mc(x.tolist(), a.tolist(), ALPHA))
    d_mc = float(np.max(np.abs(mine - theirs)))
    d_dr = float(np.max(np.abs(ci_emit_drive(x) - np.array([e_drive(r) for r in x.tolist()]))))
    d_ps = abs(tr_psi(x, THR) - e_psi(x.tolist(), THR))
    return {
        "available": True,
        "max_abs_delta_topo_apply_meancenter": d_mc,
        "max_abs_delta_ci_emit_drive": d_dr,
        "max_abs_delta_tr_psi": float(d_ps),
        "engine_faithful": bool(d_mc < 1e-12 and d_dr < 1e-12 and d_ps < 1e-12),
    }


# ── substrate population ────────────────────────────────────────────────────────
def make_adj(seed=ADJ_SEED):
    rng = np.random.default_rng(seed)
    a = (rng.random((L_LANES, L_LANES)) < 0.3).astype(float)
    a = np.maximum(a, a.T)
    np.fill_diagonal(a, 0.0)
    return a


_PHI = np.vectorize(lambda v: 0.5 * (1.0 + erf(v / np.sqrt(2.0))))


def make_population(seed, rho, mu):
    """anima lane population. A/G lanes get copula-correlation rho; lanes centred on mu.

    A,G ~ uniform(0,1) marginals with Gaussian-copula correlation rho, then affinely
    recentred on mu (spread preserved). D = 0.5*(A+G) = engine emit drive.
    V = |A - G| = the maintained A<->G disequilibrium = the membrane potential.
    """
    rng = np.random.default_rng(1000 + seed)
    z1 = rng.standard_normal(N_UNITS)
    z2 = rng.standard_normal(N_UNITS)
    zg = rho * z1 + np.sqrt(max(0.0, 1.0 - rho * rho)) * z2
    a_u = _PHI(z1)
    g_u = _PHI(zg)
    shift = mu - 0.5
    a_u = np.clip(a_u + shift, 0.0, 1.0)
    g_u = np.clip(g_u + shift, 0.0, 1.0)
    x = np.clip(rng.random((N_UNITS, L_LANES)) + shift, 0.0, 1.0)
    x[:, A_LANE] = a_u
    x[:, G_LANE] = g_u
    return x


# ── chemiosmotic work functionals ───────────────────────────────────────────────
def force_flux(drive, pot):
    """Vbar0(psi) = mean membrane potential over the top-psi (by drive) recruited set.

    The recruited set at operating point psi = the units the engine fires when thr sits
    at the (1-psi) quantile of the drive => psi is an EXACT operating point.
    """
    order = np.argsort(-drive, kind="stable")
    pot_sorted = pot[order]
    csum = np.cumsum(pot_sorted)
    out = []
    for psi in PSI_GRID:
        k = max(1, int(round(psi * len(drive))))
        out.append(csum[k - 1] / k)
    return np.array(out)


def w_kin(vbar):
    psi = PSI_GRID
    vm = PUMP_P * vbar / (PUMP_P + COND_G * psi)
    return COND_G * psi * vm


def w_ohm(vbar):
    psi = PSI_GRID
    return psi * vbar * (1.0 - psi)


def argmax_psi(w):
    return float(PSI_GRID[int(np.argmax(w))])


def w_at(w, psi_target):
    i = int(np.argmin(np.abs(PSI_GRID - psi_target)))
    return float(w[i])


# ── attractor (engine settle) ───────────────────────────────────────────────────
def settle_psi(x, adj):
    """Psi the substrate's OWN dynamics land on (tension_resolve_depth's settle loop)."""
    pop = x
    for _ in range(DEPTH):
        pop = topo_apply_meancenter(pop, adj, ALPHA)
    return tr_psi(pop, THR)


def eigen_null_psi(x, adj):
    """C4 — RIVAL 0-DOF EXPLANATION of the 1/2 attractor (no energy, no work, no ATP).

    The settle op is the linear map mm = I + alpha*rowcenter(symnorm(adj)). After DEPTH
    iterations the population is dominated by mm's leading eigenvector v. The emit drive
    of a unit then collapses to c_u * s, where c_u = <x_u, v> and s = 0.5*(v[A]+v[G]).
    Because rowcenter kills the constant mode, v is mean-zero across lanes => c_u is a
    zero-mean projection of an iid-ish lane vector => ~half the units land above thr.
    PREDICTION (no free parameter): psi_att = fraction of units with c_u*s >= 0  ~= 1/2.
    If THIS predicts psi_att while max-work does not, the "1/2 = max work" story is
    explanatorily idle.
    """
    n = adj.shape[0]
    mm = ALPHA * topo_row_center(topo_sym_norm(adj)) + np.eye(n)
    w, vecs = np.linalg.eig(mm)
    v = np.real(vecs[:, int(np.argmax(np.abs(w)))])
    s = 0.5 * (v[A_LANE] + v[G_LANE])
    c = x @ v
    return float(np.mean(c * s >= 0.0)), float(np.max(np.abs(w)))


# ── arms ────────────────────────────────────────────────────────────────────────
def arm_curves(drive, pot):
    vbar = force_flux(drive, pot)
    wk, wo = w_kin(vbar), w_ohm(vbar)
    return {
        "vbar": vbar.tolist(),
        "w_kin": wk.tolist(),
        "w_ohm": wo.tolist(),
        "psi_star_kin": argmax_psi(wk),
        "psi_star_ohm": argmax_psi(wo),
        "w_kin_half": w_at(wk, 0.5),
        "w_kin_max": float(np.max(wk)),
        "w_ohm_half": w_at(wo, 0.5),
        "w_ohm_max": float(np.max(wo)),
    }


def run_cell(seed, rho, mu, adj):
    x = make_population(seed, rho, mu)
    drive = ci_emit_drive(x)
    pot = np.abs(x[:, A_LANE] - x[:, G_LANE])
    rng = np.random.default_rng(7000 + seed)

    exp = arm_curves(drive, pot)
    shuf = arm_curves(drive, rng.permutation(pot))                       # C2
    bern = arm_curves(rng.random(N_UNITS), rng.random(N_UNITS))          # C3
    psi_att = settle_psi(x, adj)                                         # engine attractor
    psi_eig, lead_ev = eigen_null_psi(x, adj)                            # C4 rival null
    return {
        "seed": seed, "rho": rho, "mu": mu,
        "EXP": exp, "C2_SHUF": shuf, "C3_BERN": bern,
        "psi_att": psi_att,
        "C4_psi_eigen_null": psi_eig,
        "C4_leading_eigval": lead_ev,
        "drive_median": float(np.median(drive)),
        "pot_mean": float(np.mean(pot)),
    }


def positive_controls():
    """ARM-SHOCK: the argmax detector must find 0.5 when 0.5 is there, and a non-0.5
    value when it is not. Same grid / same functionals / same budget."""
    q = (np.arange(N_UNITS) + 0.5) / N_UNITS          # rank quantile (0=lowest drive)
    drive = q.copy()
    pot_flat = np.ones(N_UNITS)                        # flat force
    pot_decay = np.exp(-4.0 * q[::-1])                 # force decays as more are recruited
    ph = arm_curves(drive, pot_flat)
    po = arm_curves(drive, pot_decay)
    return {
        "POS_HALF": {"psi_star_ohm": ph["psi_star_ohm"], "psi_star_kin": ph["psi_star_kin"],
                     "expect_ohm": 0.5,
                     "pass": bool(abs(ph["psi_star_ohm"] - 0.5) <= GRID_RES / 2)},
        "POS_OFF": {"psi_star_kin": po["psi_star_kin"], "psi_star_ohm": po["psi_star_ohm"],
                    "expect_kin_lt": 0.5,
                    "pass": bool(po["psi_star_kin"] < 0.5 - GRID_RES / 2)},
    }


def sensitivity(cells, key_get, knob):
    """mean over the other knob+seeds of (max - min) across the swept knob levels."""
    other = "mu" if knob == "rho" else "rho"
    levels = MUS if other == "mu" else RHOS
    spans = []
    for seed in SEEDS:
        for lv in levels:
            vals = [key_get(c) for c in cells if c["seed"] == seed and c[other] == lv]
            if len(vals) >= 2:
                spans.append(max(vals) - min(vals))
    return float(np.mean(spans)), float(np.std(spans))


def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def main():
    adj = make_adj()
    parity = engine_parity_check()

    cells = []
    for seed in SEEDS:
        for rho in RHOS:
            for mu in MUS:
                cells.append(run_cell(seed, rho, mu, adj))

    def agg(getter):
        v = np.array([getter(c) for c in cells], float)
        return {"mean": float(v.mean()), "std": float(v.std())}

    # ── Q1: is work maximal at psi = 1/2 ? (EXP arm, both functionals) ──────────
    q1 = {
        "psi_star_kin_EXP": agg(lambda c: c["EXP"]["psi_star_kin"]),
        "psi_star_ohm_EXP": agg(lambda c: c["EXP"]["psi_star_ohm"]),
        "frac_cells_kin_argmax_is_half": float(np.mean(
            [abs(c["EXP"]["psi_star_kin"] - 0.5) <= GRID_RES / 2 for c in cells])),
        "frac_cells_ohm_argmax_is_half": float(np.mean(
            [abs(c["EXP"]["psi_star_ohm"] - 0.5) <= GRID_RES / 2 for c in cells])),
        # C1 = off-half control: work LOST by sitting at 1/2 instead of at psi*
        "C1_offhalf_rel_gain_kin": agg(
            lambda c: (c["EXP"]["w_kin_max"] - c["EXP"]["w_kin_half"])
            / max(1e-9, c["EXP"]["w_kin_max"])),
        "C1_offhalf_rel_gain_ohm": agg(
            lambda c: (c["EXP"]["w_ohm_max"] - c["EXP"]["w_ohm_half"])
            / max(1e-9, c["EXP"]["w_ohm_max"])),
    }

    # ── Q2: tautology test — do the substrate-free controls give the SAME answer? ─
    q2 = {}
    for arm in ("EXP", "C2_SHUF", "C3_BERN"):
        q2[arm] = {
            "psi_star_kin": agg(lambda c, a=arm: c[a]["psi_star_kin"]),
            "psi_star_ohm": agg(lambda c, a=arm: c[a]["psi_star_ohm"]),
            "frac_ohm_argmax_is_half": float(np.mean(
                [abs(c[arm]["psi_star_ohm"] - 0.5) <= GRID_RES / 2 for c in cells])),
            "frac_kin_argmax_is_half": float(np.mean(
                [abs(c[arm]["psi_star_kin"] - 0.5) <= GRID_RES / 2 for c in cells])),
        }
    q2["delta_psi_star_ohm_EXP_minus_SHUF"] = (
        q2["EXP"]["psi_star_ohm"]["mean"] - q2["C2_SHUF"]["psi_star_ohm"]["mean"])
    q2["delta_psi_star_ohm_EXP_minus_BERN"] = (
        q2["EXP"]["psi_star_ohm"]["mean"] - q2["C3_BERN"]["psi_star_ohm"]["mean"])
    q2["delta_psi_star_kin_EXP_minus_SHUF"] = (
        q2["EXP"]["psi_star_kin"]["mean"] - q2["C2_SHUF"]["psi_star_kin"]["mean"])
    q2["delta_psi_star_kin_EXP_minus_BERN"] = (
        q2["EXP"]["psi_star_kin"]["mean"] - q2["C3_BERN"]["psi_star_kin"]["mean"])

    # ── P2: does the attractor TRACK the work-max? (the non-tautological prediction) ─
    def star(c):
        return c["EXP"]["psi_star_kin"]

    def att(c):
        return c["psi_att"]

    s_star_rho = sensitivity(cells, star, "rho")
    s_star_mu = sensitivity(cells, star, "mu")
    s_att_rho = sensitivity(cells, att, "rho")
    s_att_mu = sensitivity(cells, att, "mu")
    trk = [pearson([star(c) for c in cells if c["seed"] == s],
                   [att(c) for c in cells if c["seed"] == s]) for s in SEEDS]
    trk_rho = []
    for s in SEEDS:
        for m in MUS:
            sub = [c for c in cells if c["seed"] == s and c["mu"] == m]
            trk_rho.append(pearson([star(c) for c in sub], [att(c) for c in sub]))
    p2 = {
        "sens_psi_star_work_to_rho": {"mean": s_star_rho[0], "std": s_star_rho[1]},
        "sens_psi_att_to_rho": {"mean": s_att_rho[0], "std": s_att_rho[1]},
        "sens_psi_star_work_to_mu": {"mean": s_star_mu[0], "std": s_star_mu[1]},
        "sens_psi_att_to_mu": {"mean": s_att_mu[0], "std": s_att_mu[1]},
        "tracking_corr_all_cells": {"mean": float(np.mean(trk)), "std": float(np.std(trk))},
        "tracking_corr_rho_only": {"mean": float(np.mean(trk_rho)),
                                   "std": float(np.std(trk_rho))},
        "abs_gap_att_minus_star": agg(lambda c: abs(c["psi_att"] - c["EXP"]["psi_star_kin"])),
        "psi_att": agg(lambda c: c["psi_att"]),
        "double_dissociation": bool(
            s_star_rho[0] > 2.0 * s_att_rho[0] and s_att_mu[0] > 2.0 * s_star_mu[0]),
        # C4 — the rival 0-DOF explanation: does the coupling operator's leading
        # eigenvector predict the 1/2 attractor better than max-work does?
        "C4_eigen_null_psi": agg(lambda c: c["C4_psi_eigen_null"]),
        "C4_abs_err_eigen_vs_att": agg(
            lambda c: abs(c["C4_psi_eigen_null"] - c["psi_att"])),
        "workmax_abs_err_vs_att": agg(
            lambda c: abs(c["EXP"]["psi_star_kin"] - c["psi_att"])),
        "leading_eigval": agg(lambda c: c["C4_leading_eigval"]),
    }

    pos = positive_controls()

    # ── verdict (rules fixed BEFORE the numbers; see module docstring) ───────────
    q1_pass = q1["frac_cells_kin_argmax_is_half"] >= 0.8
    q2_pass = (abs(q2["delta_psi_star_ohm_EXP_minus_SHUF"]) > GRID_RES
               and abs(q2["delta_psi_star_ohm_EXP_minus_BERN"]) > GRID_RES)
    p2_pass = (abs(p2["tracking_corr_rho_only"]["mean"]) >= 0.5
               and p2["sens_psi_att_to_rho"]["mean"]
               >= 0.5 * p2["sens_psi_star_work_to_rho"]["mean"])
    detector_ok = pos["POS_HALF"]["pass"] and pos["POS_OFF"]["pass"]

    if not detector_ok:
        verdict = "INVALID"
    elif q1_pass and p2_pass:
        verdict = "GREEN"
    elif p2_pass:
        verdict = "DIRECTIONAL-POSITIVE"
    elif not p2_pass and not q1_pass:
        verdict = "KILL"
    else:
        verdict = "THEATER"

    out = {
        "hypothesis": "H_9279 / F7 chemiosmotic gradient",
        "config": {
            "N_units": N_UNITS, "L_lanes": L_LANES, "A_lane": A_LANE, "G_lane": G_LANE,
            "alpha": ALPHA, "settle_depth": DEPTH, "thr": THR, "pump_p": PUMP_P,
            "cond_g": COND_G, "psi_grid": PSI_GRID.tolist(), "seeds": SEEDS,
            "rhos": RHOS, "mus": MUS, "cells": len(cells),
        },
        "engine_parity": parity,
        "positive_controls": pos,
        "Q1_work_max_at_half": q1,
        "Q2_tautology_controls": q2,
        "P2_attractor_tracks_workmax": p2,
        "gates": {"Q1_pass": bool(q1_pass), "Q2_substrate_info": bool(q2_pass),
                  "P2_pass": bool(p2_pass), "detector_ok": bool(detector_ok)},
        "verdict": verdict,
        "cells": cells,
    }
    path = os.path.join(HERE, "result.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)

    print("engine parity:", parity)
    print("positive controls:", json.dumps(pos, ensure_ascii=False))
    print("Q1 psi*_kin(EXP) =", q1["psi_star_kin_EXP"],
          "half-frac", q1["frac_cells_kin_argmax_is_half"])
    print("Q1 psi*_ohm(EXP) =", q1["psi_star_ohm_EXP"],
          "half-frac", q1["frac_cells_ohm_argmax_is_half"])
    print("Q1 C1 off-half rel gain (kin):", q1["C1_offhalf_rel_gain_kin"])
    print("Q2 ohm argmax EXP/SHUF/BERN:",
          [q2[a]["psi_star_ohm"]["mean"] for a in ("EXP", "C2_SHUF", "C3_BERN")])
    print("Q2 kin argmax EXP/SHUF/BERN:",
          [q2[a]["psi_star_kin"]["mean"] for a in ("EXP", "C2_SHUF", "C3_BERN")])
    print("Q2 deltas:", {k: v for k, v in q2.items() if k.startswith("delta")})
    print("P2:", json.dumps(p2, ensure_ascii=False))
    print("gates:", out["gates"])
    print("VERDICT:", verdict)
    print("->", path)


if __name__ == "__main__":
    main()
