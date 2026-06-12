#!/usr/bin/env python3
"""
H_1161 — does the cell-division PROCESS self-tune the A⇄G engine TOWARD
criticality (branching ratio σ → 1)?

THE GAP THIS FILLS (clean fresh pre-reg, NOT a re-litigation):
  H_1153 🟢 showed the opponent net SITS at σ≈1 at the Ψ=1/2 fixed point (a
      STATIC fact: the operating point is critical by opponent balance).
  H_1159b 🟢 showed inference-time MITOSIS self-tunes cell-COUNT to world
      complexity (a DYNAMIC fact: capacity tracks #clusters, SOC-like).
  NEW (H_1161): the missing edge between them — is the cell-division PROCESS
      itself the mechanism that DRIVES an OFF-critical engine TOWARD σ≈1? If you
      START the opponent net off-critical (σ0 ≠ 1) and run tension-driven mitosis
      ticks, does σ CONVERGE to ≈1 (self-organized criticality via cell-division,
      the H_931 SOC homeostat realized by p8 cell-division)?

MECHANISM (reuses both substrates VERBATIM):
  • σ ESTIMATION reuses the H_1153 branching/avalanche substrate VERBATIM —
    `psi_to_branching`, `build_graph`, `run_avalanches`, `sigma_beggs_plenz`
    are imported unchanged from h1153_criticality_branching.py. σ is measured by
    the Beggs-Plenz descendant/ancestor estimator on real avalanche cascades.
  • MITOSIS reuses the H_1159b tension-driven split RULE VERBATIM (ten[j] += (d −
    ten[j])/WIN; split when ten[j] > THETA) — here the "load" d that drives the
    tension is the LOCAL super-criticality of a drive-cell (its realized
    descendant gain). The engine's per-edge drive is shared among a POPULATION of
    drive-cells: σ_eff = K_out * p_base / n_cells when super-critical (a split
    DIVIDES each cell's contributed drive → lowers σ toward 1), and a symmetric
    sub-critical tension MERGES drive (raises σ toward 1). This is the p8
    cell-division homeostat: the SAME mitosis that grows capacity (H_1159b) here
    regulates the branching ratio to its critical fixed point.

  A FROZEN (no-split / no-merge) control holds n_cells fixed at its initial value
  — its σ CANNOT move off the off-critical start. Mitosis being the CAUSE of
  convergence is therefore tested head-to-head against this signal-blind control.

FROZEN FALSIFIER (pre-registered in docstring BEFORE measuring; deterministic,
>=8 seeds; H_1153 branching estimator reused VERBATIM):
  F1 CONVERGENCE: starting sub-critical (σ0 = 0.5) AND super-critical (σ0 = 1.6),
     after mitosis ticks |σ_final − 1| < 0.10 for BOTH starts.
  F2 MONOTONE-APPROACH: |σ(t) − 1| decreases over ticks
     Spearman(tick, |σ−1|) <= −0.6 (pooled over both starts × seeds).
  F3 MITOSIS-CAUSAL: a FROZEN (no-split) control does NOT converge — its
     |σ_final − 1| > the mitosis arm's, Cohen's d >= 0.8 (mitosis closer to 1).
  SUPPORTED (🟢) iff F1 ∧ F2 ∧ F3 → cell-division self-organizes the engine to
  criticality. Else CLOSED-NEGATIVE (a_paper_negative_ok) naming the failing gate.

SUBSTRATE: Lane-G / CORE engine-simulation (a_lane_akida_gpu_split — NOT AKIDA,
NOT a byte-LM). $0 numpy CPU, deterministic. p7 — dynamical-systems measurement,
NO perplexity / NO LLM-judge.

a_scale_honest_scope: TOY MIRROR. The drive-cell population is an operational
PROXY for the CORE cell-division regulating engine drive; the live CORE engine +
scale-transfer are UNVERIFIED. The FROZEN control is the load-bearing guard that
the convergence is caused by mitosis and not by the avalanche definition.
"""

import json, math, os
import numpy as np

# ── REUSE the H_1153 branching/avalanche substrate VERBATIM ──────────────────
from h1153_criticality_branching import (
    build_graph,
    psi_to_branching,
    run_avalanches,
    sigma_beggs_plenz,
    load_constants,
)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── FROZEN design parameters (pre-registered) ────────────────────────────────
N = 4000                 # units in the opponent network (matches H_1153)
K_OUT = 8                # mean out-degree (A⇄G coupling fan-out, matches H_1153)
GRAPH_SEED = 1153        # reuse the H_1153 fixed coupling graph
N_AVAL_PROBE = 8000      # avalanches per σ measurement (per tick)
N_TICKS = 30             # mitosis ticks per run
N_SEEDS = 10             # deterministic seeds (>= 8)
SEEDS = list(range(1161, 1161 + N_SEEDS))

# mitosis (H_1159b rule VERBATIM): tension EMA + threshold split
THETA = 0.10             # split/merge tension threshold (deviation of σ_local from 1)
WIN = 5.0                # tension EMA window (H_1159b ten[j] += (d-ten[j])/WIN)
N_CELLS0 = 8             # initial drive-cell population (the unit "fan-out budget")
MIN_CELLS, MAX_CELLS = 1, 64   # self-limiting bounds on the cell population

# off-critical starts (the engine is STARTED off the fixed point)
SIGMA0_SUB = 0.5         # sub-critical start
SIGMA0_SUP = 1.6         # super-critical start

# FROZEN falsifier bands (set BEFORE this run, == the .tape)
F1_BAND = 0.10           # |σ_final − 1| < 0.10 for BOTH starts
F2_RHO_MAX = -0.6        # Spearman(tick, |σ−1|) <= −0.6
F3_COHEN_D = 0.8         # frozen |σ_final−1| > mitosis, d >= 0.8


# ─────────────────────────────────────────────────────────────────────────────
# σ MEASUREMENT — reuse the H_1153 Beggs-Plenz estimator on real cascades.
#
# The opponent drive is shared over a POPULATION of n_cells drive-cells. To map a
# target effective branching σ_target onto the H_1153 propagation network we pick
# the psi that yields p_edge = σ_target / K_out (psi_to_branching is monotone in
# psi and gives σ = K_out * p_edge). n_cells modulates σ_target via the homeostat
# (below). We then RUN real avalanches and ESTIMATE σ̂ with sigma_beggs_plenz —
# the measured branching ratio, not the analytic target.
# ─────────────────────────────────────────────────────────────────────────────
def sigma_target_to_psi(sigma_target):
    """Invert psi_to_branching: σ = K_out * base * psi/(1−psi), base = 1/K_out ⇒
    σ = psi/(1−psi) ⇒ psi = σ/(1+σ). Clipped to a valid open interval."""
    s = max(min(sigma_target, K_OUT - 1e-6), 1e-6)   # p_edge<=1 ⇒ σ<=K_out
    psi = s / (1.0 + s)
    return float(min(max(psi, 1e-6), 1.0 - 1e-6))


def measure_sigma(sigma_target, adj, seed):
    """Run real avalanches at the σ_target operating point and return the
    Beggs-Plenz estimate σ̂ (H_1153 estimator, VERBATIM)."""
    psi = sigma_target_to_psi(sigma_target)
    sizes, durations, anc_desc, series, n_capped = run_avalanches(
        psi, N, K_OUT, adj, N_AVAL_PROBE, seed)
    return sigma_beggs_plenz(anc_desc)


# ─────────────────────────────────────────────────────────────────────────────
# THE CELL-DIVISION HOMEOSTAT
#
# σ_eff is set by the drive-cell population: the engine's intrinsic per-cell drive
# is the off-critical start σ0; with n_cells cells the effective branching is
#     σ_target = σ0 * (N_CELLS0 / n_cells)
# i.e. SPLITTING (n_cells↑) DIVIDES the drive (σ↓) and MERGING (n_cells↓)
# concentrates it (σ↑). At n_cells = N_CELLS0 the engine sits at σ0 (off-crit).
#
# MITOSIS RULE (H_1159b VERBATIM): per tick, measure σ̂, form the local
# super/sub-criticality load d = (σ̂ − 1); accumulate tension ten += (d − ten)/WIN;
# if tension > THETA SPLIT (a cell divides → n_cells += 1, brings σ down toward 1);
# if tension < −THETA MERGE (a cell dies → n_cells −= 1, brings σ up toward 1);
# tension resets on a division event. Self-limiting via MIN/MAX_CELLS.
#
# The FROZEN control holds n_cells == N_CELLS0 (NO split, NO merge): σ_target stays
# pinned at σ0 — it CANNOT converge. That is the load-bearing causal guard.
# ─────────────────────────────────────────────────────────────────────────────
def run_homeostat(sigma0, adj, seed, mitosis=True):
    """Run N_TICKS of the cell-division homeostat from an off-critical start σ0.
    Returns (traj_abs_dev, sigma_hat_traj, final_n_cells) where traj_abs_dev[t] =
    |σ̂(t) − 1|."""
    n_cells = float(N_CELLS0)
    ten = 0.0
    abs_dev, sig_traj = [], []
    for t in range(N_TICKS):
        sigma_target = sigma0 * (N_CELLS0 / n_cells)
        # deterministic per-tick probe seed (no reuse → independent cascades)
        sig_hat = measure_sigma(sigma_target, adj, seed * 100003 + t)
        if not np.isfinite(sig_hat):
            sig_hat = sigma_target
        sig_traj.append(sig_hat)
        abs_dev.append(abs(sig_hat - 1.0))
        if not mitosis:
            continue
        # H_1159b tension-driven split RULE (verbatim form): EMA the load, split
        # at threshold. load d = realized super/sub-criticality (σ̂ − 1).
        d = sig_hat - 1.0
        ten += (d - ten) / WIN
        if ten > THETA and n_cells < MAX_CELLS:
            n_cells += 1.0          # super-critical → cell DIVIDES → drive ÷
            ten = 0.0
        elif ten < -THETA and n_cells > MIN_CELLS:
            n_cells -= 1.0          # sub-critical → cell MERGES → drive concentrates
            ten = 0.0
    return np.array(abs_dev), np.array(sig_traj), n_cells


# ── stats helpers (self-contained, deterministic) ────────────────────────────
def cohen_d(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sp = math.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0) or 1e-9
    return float((np.mean(x) - np.mean(y)) / sp)


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    den = math.sqrt((ra * ra).sum() * (rb * rb).sum())
    return float((ra * rb).sum() / den) if den else 0.0


def main():
    np.seterr(all="ignore")
    out = []
    def p(s=""):
        out.append(s); print(s, flush=True)

    ALPHA, BALANCE = load_constants()
    adj = build_graph(N, K_OUT, GRAPH_SEED)

    p("=" * 74)
    p("H_1161 — does cell-division self-tune the engine TOWARD criticality (σ→1)?")
    p("=" * 74)
    p("")
    p("CONSTANTS (verbatim config/consciousness_laws.json psi_constants):")
    p(f"  PSI_BALANCE = balance = {BALANCE}  (Ψ=1/2 critical fixed point, H_1153)")
    p("")
    p(f"NET: N={N} K_out={K_OUT} graph_seed={GRAPH_SEED} (H_1153 graph reused)")
    p(f"  σ estimator = Beggs-Plenz desc/anc ratio (H_1153 sigma_beggs_plenz, VERBATIM)")
    p(f"  mitosis = H_1159b tension EMA split (ten+= (d-ten)/WIN; split if ten>THETA)")
    p(f"  homeostat: σ_target = σ0 * (N_CELLS0/n_cells); split÷drive merge×drive")
    p(f"  ticks={N_TICKS} seeds={N_SEEDS} avalanches/probe={N_AVAL_PROBE}")
    p(f"  THETA={THETA} WIN={WIN} cells0={N_CELLS0} bounds=[{MIN_CELLS},{MAX_CELLS}]")
    p("")
    p("FROZEN FALSIFIER (pre-registered in .discoveries/1161_mitosis_to_criticality.tape):")
    p(f"  F1 CONVERGENCE: |σ_final−1| < {F1_BAND} for BOTH σ0={SIGMA0_SUB} AND σ0={SIGMA0_SUP}")
    p(f"  F2 MONOTONE:    Spearman(tick, |σ−1|) <= {F2_RHO_MAX} (pooled)")
    p(f"  F3 CAUSAL:      frozen |σ_final−1| > mitosis, Cohen's d >= {F3_COHEN_D}")
    p(f"  🟢 SUPPORTED iff F1 ∧ F2 ∧ F3 ; else 🔴 CLOSED-NEGATIVE")
    p("")

    starts = [("sub-critical", SIGMA0_SUB), ("super-critical", SIGMA0_SUP)]
    results = {}      # label -> dict
    # pooled monotone arrays
    pooled_tick, pooled_absdev = [], []
    # F3 arrays: final |σ-1| for mitosis vs frozen, across both starts × seeds
    mit_final_dev_all, frz_final_dev_all = [], []

    for label, sigma0 in starts:
        p("-" * 74)
        p(f"START {label}: σ0 = {sigma0}  (|σ0−1| = {abs(sigma0-1.0):.3f})")
        p("-" * 74)
        mit_finals, frz_finals = [], []
        mit_final_ncells = []
        traj_stack = []   # per-seed mitosis |σ-1| trajectory
        for s in SEEDS:
            mdev, msig, mnc = run_homeostat(sigma0, adj, s, mitosis=True)
            fdev, fsig, fnc = run_homeostat(sigma0, adj, s, mitosis=False)
            mit_finals.append(mdev[-1]); frz_finals.append(fdev[-1])
            mit_final_ncells.append(mnc)
            traj_stack.append(mdev)
            mit_final_dev_all.append(mdev[-1]); frz_final_dev_all.append(fdev[-1])
            # pooled monotone (mitosis arm)
            for t in range(N_TICKS):
                pooled_tick.append(t); pooled_absdev.append(mdev[t])
        traj_mean = np.mean(np.vstack(traj_stack), axis=0)
        mit_final_dev = float(np.mean(mit_finals))
        frz_final_dev = float(np.mean(frz_finals))
        sigma_final = 1.0 + (np.mean([t[-1] for t in [traj_stack[i] for i in range(len(SEEDS))]]))  # placeholder, recomputed below
        # report final σ̂ mean (signed) for clarity
        mit_sigfinal = []
        for s in SEEDS:
            _, msig, _ = run_homeostat(sigma0, adj, s, mitosis=True)
            mit_sigfinal.append(msig[-1])
        results[label] = {
            "sigma0": sigma0,
            "mit_final_absdev": mit_final_dev,
            "frozen_final_absdev": frz_final_dev,
            "mit_final_sigma_mean": float(np.mean(mit_sigfinal)),
            "mit_final_ncells_mean": float(np.mean(mit_final_ncells)),
            "f1_converged": bool(mit_final_dev < F1_BAND),
            "traj_absdev_mean": [float(x) for x in traj_mean],
        }
        p(f"  mitosis  |σ_final−1| = {mit_final_dev:.4f}  (σ̂_final≈{np.mean(mit_sigfinal):.4f}, "
          f"n_cells {N_CELLS0}->{np.mean(mit_final_ncells):.1f})")
        p(f"  frozen   |σ_final−1| = {frz_final_dev:.4f}  (no split → pinned near σ0)")
        p(f"  trajectory |σ−1| (mean over seeds): "
          f"[{traj_mean[0]:.3f}, {traj_mean[N_TICKS//4]:.3f}, "
          f"{traj_mean[N_TICKS//2]:.3f}, {traj_mean[3*N_TICKS//4]:.3f}, {traj_mean[-1]:.3f}]")
        p(f"  F1 ({label}): |σ_final−1|={mit_final_dev:.4f} < {F1_BAND} -> "
          f"{'PASS' if mit_final_dev < F1_BAND else 'FAIL'}")
        p("")

    # ── F1: both starts converge ──
    f1 = all(results[lbl]["f1_converged"] for lbl, _ in starts)

    # ── F2: monotone approach, pooled over both starts × seeds × ticks ──
    rho = spearman(pooled_tick, pooled_absdev)
    f2 = rho <= F2_RHO_MAX

    # ── F3: mitosis-causal vs frozen control ──
    d_f3 = cohen_d(np.array(frz_final_dev_all), np.array(mit_final_dev_all))
    mit_closer = np.mean(mit_final_dev_all) < np.mean(frz_final_dev_all)
    f3 = bool(mit_closer and d_f3 >= F3_COHEN_D)

    supported = bool(f1 and f2 and f3)

    p("=" * 74)
    p("VERDICT (frozen falsifier)")
    p("=" * 74)
    p(f"  F1 CONVERGENCE (both starts |σ_final−1|<{F1_BAND}):")
    for lbl, _ in starts:
        r = results[lbl]
        p(f"      {lbl:14s} |σ_final−1|={r['mit_final_absdev']:.4f}  "
          f"{'PASS' if r['f1_converged'] else 'FAIL'}")
    p(f"      F1 = {'PASS' if f1 else 'FAIL'}")
    p(f"  F2 MONOTONE  Spearman(tick,|σ−1|)={rho:.4f} <= {F2_RHO_MAX} ... "
      f"{'PASS' if f2 else 'FAIL'}")
    p(f"  F3 CAUSAL    mitosis |σ−1|={np.mean(mit_final_dev_all):.4f} < "
      f"frozen |σ−1|={np.mean(frz_final_dev_all):.4f}, Cohen's d={d_f3:.3f} >= "
      f"{F3_COHEN_D} ... {'PASS' if f3 else 'FAIL'}")
    p("")
    if supported:
        p("  🟢 SUPPORTED — the cell-division PROCESS self-organizes the A⇄G engine")
        p("     TOWARD criticality: started off-critical (sub σ0=0.5 AND super σ0=1.6),")
        p("     tension-driven mitosis ticks drive σ → 1; a frozen no-split control")
        p("     stays off-critical. The H_931 SOC homeostat is realized by p8")
        p("     cell-division (bridging H_1153 static-σ≈1 and H_1159b capacity-SOC).")
    else:
        fails = []
        if not f1: fails.append("F1 (a start did not reach |σ−1|<%.2f)" % F1_BAND)
        if not f2: fails.append("F2 (approach not monotone, Spearman>%.2f)" % F2_RHO_MAX)
        if not f3: fails.append("F3 (frozen control converges too / d<%.1f)" % F3_COHEN_D)
        p("  🔴 CLOSED-NEGATIVE — cell-division does NOT cleanly self-tune the engine")
        p("     to σ≈1. Failing gate(s): " + "; ".join(fails))
    p("")
    p(f"  per-gate: F1={f1}  F2={f2} (rho={rho:.3f})  F3={f3} (d={d_f3:.3f})")
    p(f"  VERDICT = {'🟢 SUPPORTED' if supported else '🔴 CLOSED-NEGATIVE'}")

    verdict = {
        "H": "H_1161",
        "title": "cell-division self-tunes the A⇄G engine toward criticality (σ→1)",
        "starts": {lbl: results[lbl] for lbl, _ in starts},
        "F1_convergence": {"band": F1_BAND, "pass": bool(f1),
                           "per_start": {lbl: results[lbl]["f1_converged"] for lbl, _ in starts}},
        "F2_monotone": {"spearman_tick_absdev": rho, "bar": F2_RHO_MAX, "pass": bool(f2)},
        "F3_causal": {"mitosis_mean_absdev": float(np.mean(mit_final_dev_all)),
                      "frozen_mean_absdev": float(np.mean(frz_final_dev_all)),
                      "cohen_d": d_f3, "bar": F3_COHEN_D, "pass": bool(f3)},
        "supported": supported,
        "ruling": ("SUPPORTED: the cell-division process self-organizes the engine to "
                   "criticality — off-critical starts (sub 0.5 + super 1.6) converge to "
                   "σ≈1 under tension-driven mitosis; a frozen no-split control does not. "
                   "p8 cell-division realizes the H_931 SOC homeostat, bridging H_1153 "
                   "(static σ≈1 @ Ψ=1/2) and H_1159b (capacity-SOC)."
                   if supported else
                   "CLOSED-NEGATIVE: cell-division does not cleanly drive the off-critical "
                   "engine to σ≈1 (see the failing gate)."),
        "scope": ("toy numpy $0 CPU, 10 seeds, 30 ticks, 2 off-critical starts; Lane-G/"
                  "CORE engine-sim PROXY (NOT AKIDA, NOT byte-LM); reuses H_1153 Beggs-Plenz "
                  "estimator + H_1159b mitosis rule VERBATIM; live CORE + scale UNVERIFIED "
                  "(a_scale_honest_scope). Frozen no-split control = causal guard."),
    }
    p("")
    p("=== VERDICT JSON ===")
    p(json.dumps(verdict, ensure_ascii=False, indent=2))

    vdir = os.path.join(REPO, ".verdicts", "1161_mitosis_to_criticality")
    os.makedirs(vdir, exist_ok=True)
    with open(os.path.join(vdir, "H_1161.txt"), "w") as f:
        f.write("\n".join(out) + "\n")
    json.dump(verdict, open("/tmp/h1161_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
