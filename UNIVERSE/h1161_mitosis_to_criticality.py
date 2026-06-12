#!/usr/bin/env python3
"""
H_1161 — does the cell-division PROCESS self-tune the engine TOWARD criticality
(branching ratio σ → 1)?

SEED / CONTEXT:
  H_1153 (🟢) — the A⇄G repulsion-field OPPONENT engine SITS AT criticality
    (σ≈1, τ≈1.5 power-law avalanches) AT the Ψ=1/2 fixed point.
  H_1159b (🟢) — inference-time tension-driven MITOSIS SELF-TUNES its CAPACITY to
    the world's complexity (cell-count tracks #clusters, SOC-like, self-limiting).
  H_931 — a SOC homeostat self-tunes the operating point TO the critical point.
  H_1158 (🟢) — faithful-IIT φ PEAKS at the critical A⇄G coupling.
  OPEN — is the link CAUSAL through the cell-division PROCESS itself? i.e. if the
  engine STARTS off-critical, does RUNNING MITOSIS TICKS drive its branching ratio
  σ TOWARD 1 (the marginal/critical value), the way a SOC homeostat regulates an
  avalanche network back to the critical point?

HYPOTHESIS: the tension-driven cell-division process is a branching-ratio
homeostat — it adds capacity (divides) when the engine is sub-critical (σ<1,
activity dies, high "death" tension) and prunes capacity (culls) when the engine
is super-critical (σ>1, activity explodes, high "explosion" tension), driving the
effective branching ratio σ toward the marginal value 1 from EITHER side.

FROZEN FALSIFIER (pre-registered in .discoveries/1161_mitosis_to_criticality.tape
BEFORE this measurement; obeyed VERBATIM):
  F1 CONVERGENCE : |σ_final − 1| < 0.10 for BOTH starts (σ0=0.5 sub AND σ0=1.6 super).
  F2 MONOTONE    : Spearman(tick, |σ−1|) ≤ −0.6 (|σ−1| shrinks monotonically over ticks).
  F3 CONTROL     : a FROZEN no-split control does NOT converge — its |σ_final−1| is
                   LARGER than the mitosis arm, Cohen's d ≥ 0.8.
  🟢 SUPPORTED iff F1 ∧ F2 ∧ F3.  🔴 CLOSED-NEGATIVE otherwise (a_paper_negative_ok).

SUBSTRATE — engine simulation (a_lane_akida_gpu_split substrate=Lane-G/CORE
engine dynamics, NOT AKIDA, NOT a byte-LM). REUSES:
  • the H_1153 Beggs-Plenz branching-ratio estimator (σ = ⟨n_{t+1}/n_t⟩ over
    ancestor bins) and avalanche propagation on a sparse A⇄G coupling graph,
    VERBATIM (imported from UNIVERSE/h1153_criticality_branching.py).
  • the H_1159b tension-driven split rule shape (a per-unit tension EMA crosses a
    threshold → a cell divides; the homeostat is bounded / self-limiting).

MECHANISM (the cell-division PROCESS as a σ-homeostat):
  The opponent network's effective branching ratio is σ = K_eff · p_edge, where
  K_eff = the effective live out-degree (the number of A⇄G coupling cells a unit
  propagates through). MITOSIS = cell division/pruning that changes K_eff:
    • measure σ̂ this tick via the H_1153 Beggs-Plenz estimator on sampled avalanches,
    • TENSION = how far the engine is from marginal: a "death" tension when σ̂<1
      (cascades die — too few coupling cells) and an "explosion" tension when σ̂>1
      (cascades blow up — too many coupling cells),
    • tension-driven cell-division: high death-tension ⇒ DIVIDE (add an effective
      coupling cell, K_eff += 1 with sub-cell resolution); high explosion-tension
      ⇒ PRUNE (cull a coupling cell, K_eff -= 1) — the same tension→division shape
      as H_1159b, applied to the engine's coupling capacity instead of a clusterer.
  This is a homeostat, NOT a hard reset to σ=1: K_eff moves by a bounded
  tension-gated step each tick (LR), so F1/F2 TEST whether the PROCESS actually
  CONVERGES, and F3 (a FROZEN no-split control whose K_eff never changes) is the
  load-bearing guard that the convergence is DRIVEN BY the cell-division process,
  not by the avalanche sampling alone.

DETERMINISTIC ($0, CPU, numpy, no torch, no GPU). Every RNG seeded. ≥8 seeds.
p7 — statistical dynamical-systems measurement, NO perplexity, NO LLM-judge.

a_scale_honest_scope: TOY MIRROR of the opponent propagation dynamics + the
cell-division homeostat; the mapping of A⇄G mitosis onto an effective-out-degree
branching homeostat is operational. CORE engine files UNTOUCHED (a_core_engine_map).
"""

import os, sys, math, json
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "UNIVERSE"))

# REUSE H_1153 VERBATIM: graph builder, avalanche propagation, Beggs-Plenz σ̂.
from h1153_criticality_branching import (
    build_graph, run_avalanches, sigma_beggs_plenz,
)

# ── frozen design parameters (pre-registered) ──────────────────────────────
N          = 4000          # units in the opponent network (== H_1153)
K_MAX      = 16            # max coupling fan-out the graph provides (cells live in [1..K_MAX])
N_AVAL     = 1500          # avalanches sampled per tick for the σ̂ estimate
N_TICKS    = 40            # mitosis ticks per run
GRAPH_SEED = 1161
N_SEEDS    = 8
SEEDS      = list(range(1161, 1161 + N_SEEDS))   # 8 seeds, deterministic
LR         = 0.45          # tension-gated cell-division step on K_eff (homeostat gain)
K_FLOOR    = 0.20          # K_eff lower bound (can't divide below ~1 coupling cell worth)

# starting effective out-degrees → starting σ0 (σ = K_eff · p_edge, p_edge=1/K_MAX
# is FROZEN so σ = K_eff / K_MAX). σ0=0.5 ⇒ K_eff=8 ; σ0=1.6 ⇒ K_eff=25.6
P_EDGE   = 1.0 / K_MAX
START_SIGMAS = {"sub_sigma0_0.5": 0.5, "super_sigma0_1.6": 1.6}


def sigma_of_keff(k_eff):
    """σ = K_eff · p_edge with p_edge = 1/K_MAX frozen."""
    return k_eff * P_EDGE


def keff_of_sigma(sig):
    return sig / P_EDGE


def measure_sigma(k_eff, adj, n_aval, seed):
    """Sample avalanches at the current effective out-degree and return the
    H_1153 Beggs-Plenz σ̂ (desc/anc ratio). K_eff is fractional: the integer part
    sets how many of each unit's K_MAX out-edges are 'live' coupling cells, and a
    fractional remainder is realized per-edge as an extra live-prob — so σ̂ moves
    smoothly with K_eff. We realize a fractional K_eff by using an effective
    per-edge fire prob p_eff = (k_eff/K_MAX)*p_edge_norm with p_edge_norm=1 i.e.
    p_eff = k_eff/K_MAX, over the full K_MAX out-edges — identical mean gain
    σ = K_MAX * (k_eff/K_MAX) = k_eff*p_edge_at_full... we instead drive H_1153's
    run_avalanches with a psi whose analytic σ = k_eff*P_EDGE by choosing the
    per-edge prob directly (see _run)."""
    # We bypass psi and drive the per-edge prob directly for an exact fractional σ.
    sizes, durations, anc_desc, series, n_capped = _run(k_eff, adj, n_aval, seed)
    return sigma_beggs_plenz(anc_desc)


def _run(k_eff, adj, n_aval, seed):
    """H_1153 run_avalanches with the per-edge prob set so the analytic branching
    ratio is exactly σ = k_eff * P_EDGE = k_eff/K_MAX over the K_MAX-out graph.
    Per-edge fire prob = σ / K_MAX = k_eff/K_MAX**2 ... wait: σ = K_MAX * p_edge
    on a K_MAX-out graph ⇒ p_edge = σ/K_MAX = k_eff*P_EDGE/K_MAX. We reproduce
    H_1153's exact vectorized propagation here with that p_edge (run_avalanches
    derives p_edge from psi; we call it with a psi whose psi_to_branching gives
    the same σ). To keep H_1153 VERBATIM we instead monkey-free: compute the psi
    that yields σ=k_eff*P_EDGE and pass it through run_avalanches."""
    sigma_target = max(sigma_of_keff(k_eff), 1e-6)
    # H_1153: σ = K_out * p_edge, p_edge = (1/K_out)*(psi/(1-psi)). On a K_MAX-out
    # graph σ = psi/(1-psi). Invert: psi = σ/(1+σ).
    psi = sigma_target / (1.0 + sigma_target)
    psi = min(max(psi, 1e-9), 1 - 1e-9)
    return run_avalanches(psi, N, K_MAX, adj, n_aval, seed)


def run_mitosis_arm(adj, sigma0, seed, frozen=False):
    """Run the σ-homeostat for N_TICKS. K_eff starts at keff_of_sigma(sigma0).
    Each tick: measure σ̂, compute tension (death if σ̂<1, explosion if σ̂>1),
    and — UNLESS frozen — apply a bounded tension-gated cell-division step to
    K_eff (divide when sub-critical, prune when super-critical). Returns the
    per-tick |σ̂−1| trajectory and the final σ̂."""
    k_eff = keff_of_sigma(sigma0)
    traj_abs = []          # |σ̂ − 1| per tick
    traj_sig = []          # σ̂ per tick
    rng = np.random.default_rng(seed + 99991)
    for tick in range(N_TICKS):
        m_seed = int(rng.integers(0, 2**31 - 1))
        sig_hat = measure_sigma(k_eff, adj, N_AVAL, m_seed)
        if not np.isfinite(sig_hat):
            sig_hat = 0.0
        traj_sig.append(sig_hat)
        traj_abs.append(abs(sig_hat - 1.0))
        if frozen:
            continue
        # TENSION = signed distance from marginal. Tension-driven cell-division:
        # sub-critical (σ̂<1, death tension) ⇒ DIVIDE (K_eff up);
        # super-critical (σ̂>1, explosion tension) ⇒ PRUNE (K_eff down).
        # The control is the *marginal* K_eff = K_MAX (σ=1). Homeostatic gain on
        # the measured branching error → bounded cell-division step.
        tension = sig_hat - 1.0                       # >0 explosion, <0 death
        k_eff = k_eff - LR * tension * K_MAX          # divide/prune toward σ=1
        k_eff = min(max(k_eff, K_FLOOR), float(K_MAX))
    return np.array(traj_abs), np.array(traj_sig), traj_sig[-1]


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    den = math.sqrt((ra*ra).sum() * (rb*rb).sum())
    return float((ra*rb).sum() / den) if den else 0.0


def cohen_d(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sp = math.sqrt((np.std(x)**2 + np.std(y)**2) / 2.0) or 1e-9
    return (np.mean(x) - np.mean(y)) / sp


def main():
    np.seterr(all="ignore")
    out = []
    def p(s=""):
        out.append(s); print(s, flush=True)

    p("=" * 78)
    p("H_1161 — does the cell-division PROCESS self-tune the engine TOWARD")
    p("         criticality (branching ratio σ → 1)?")
    p("=" * 78)
    p("")
    p("SUBSTRATE: Lane-G / CORE opponent-propagation engine-sim (NOT AKIDA, NOT a")
    p("  byte-LM). REUSES the H_1153 Beggs-Plenz σ̂ estimator + avalanche")
    p("  propagation VERBATIM, and the H_1159b tension-driven cell-division shape.")
    p("")
    p(f"DESIGN (frozen, pre-registered): N={N} units, K_MAX={K_MAX} coupling cells,")
    p(f"  n_avalanches/tick={N_AVAL}, n_ticks={N_TICKS}, seeds={SEEDS} ({N_SEEDS}),")
    p(f"  homeostat gain LR={LR}, graph_seed={GRAPH_SEED}.")
    p("  σ = K_eff · p_edge (p_edge=1/K_MAX frozen). MITOSIS = tension-gated")
    p("  cell-division/pruning of K_eff: σ̂<1 (death tension) ⇒ DIVIDE; σ̂>1")
    p("  (explosion tension) ⇒ PRUNE — driving σ toward marginal=1 from either side.")
    p("")
    p("FROZEN FALSIFIER (obeyed verbatim):")
    p("  F1 CONVERGENCE: |σ_final−1| < 0.10 for BOTH starts (σ0=0.5 AND σ0=1.6)")
    p("  F2 MONOTONE   : Spearman(tick, |σ−1|) ≤ −0.6")
    p("  F3 CONTROL    : FROZEN no-split |σ_final−1| > mitosis arm, Cohen's d ≥ 0.8")
    p("  🟢 SUPPORTED iff F1 ∧ F2 ∧ F3 ; else 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)")
    p("")

    graph = build_graph(N, K_MAX, GRAPH_SEED)

    results = {}
    for label, sigma0 in START_SIGMAS.items():
        p("-" * 78)
        p(f"START  {label}  (σ0={sigma0}, K_eff0={keff_of_sigma(sigma0):.2f})")
        p("-" * 78)

        # MITOSIS arm — run each seed ONCE, capture trajectory + final σ.
        mit_abs_stack = []
        mit_final_abs = []
        mit_final_sigmas = []
        mit_spearman = []
        for s in SEEDS:
            traj_abs, traj_sig, sig_final = run_mitosis_arm(graph, sigma0, s, frozen=False)
            mit_abs_stack.append(traj_abs)
            mit_final_abs.append(abs(sig_final - 1.0))
            mit_final_sigmas.append(sig_final)
            mit_spearman.append(spearman(list(range(N_TICKS)), traj_abs))
        mit_abs_stack = np.array(mit_abs_stack)            # (seeds, ticks)
        mean_traj = mit_abs_stack.mean(axis=0)
        mit_final_abs = np.array(mit_final_abs)
        mean_final_abs = float(mit_final_abs.mean())
        mean_final_sigma = float(np.mean(mit_final_sigmas))

        # FROZEN control arm — K_eff never changes (no cell-division)
        frz_final_abs = []
        for s in SEEDS:
            traj_abs_f, traj_sig_f, sig_final_f = run_mitosis_arm(graph, sigma0, s, frozen=True)
            frz_final_abs.append(abs(sig_final_f - 1.0))
        frz_final_abs = np.array(frz_final_abs)

        d_control = cohen_d(frz_final_abs, mit_final_abs)   # frozen worse (larger |σ−1|) ⇒ d>0
        spear_mean = float(np.mean(mit_spearman))

        # report
        p(f"  mitosis |σ−1| trajectory (mean over {N_SEEDS} seeds, every 5th tick):")
        idxs = list(range(0, N_TICKS, 5))
        if (N_TICKS - 1) not in idxs:
            idxs.append(N_TICKS - 1)
        p("    tick : " + "  ".join(f"{i:>2}" for i in idxs))
        p("    |σ−1|: " + "  ".join(f"{mean_traj[i]:.2f}" for i in idxs))
        p(f"  mitosis  σ_final (mean) = {mean_final_sigma:.4f}   |σ_final−1| = {mean_final_abs:.4f}")
        p(f"  FROZEN   |σ_final−1| (mean) = {float(frz_final_abs.mean()):.4f}  "
          f"(no cell-division; K_eff fixed at start)")
        p(f"  Spearman(tick,|σ−1|) (mean over seeds) = {spear_mean:.4f}")
        p(f"  CONTROL Cohen's d (frozen−mitosis on |σ−1|) = {d_control:.4f}")
        p("")

        results[label] = {
            "sigma0": sigma0,
            "mean_final_sigma": mean_final_sigma,
            "mean_final_abs": mean_final_abs,
            "frozen_final_abs": float(frz_final_abs.mean()),
            "spearman_mean": spear_mean,
            "control_d": float(d_control),
        }

    # ── VERDICT ─────────────────────────────────────────────────────────────
    p("=" * 78)
    p("VERDICT (frozen falsifier)")
    p("=" * 78)
    f1 = all(results[l]["mean_final_abs"] < 0.10 for l in results)
    f2 = all(results[l]["spearman_mean"] <= -0.6 for l in results)
    f3 = all((results[l]["frozen_final_abs"] > results[l]["mean_final_abs"]
              and results[l]["control_d"] >= 0.8) for l in results)
    supported = f1 and f2 and f3

    for l in results:
        r = results[l]
        p(f"  [{l}]  σ_final={r['mean_final_sigma']:.4f}  |σ_final−1|={r['mean_final_abs']:.4f}  "
          f"frozen|σ−1|={r['frozen_final_abs']:.4f}  ρ={r['spearman_mean']:.3f}  d={r['control_d']:.2f}")
    p("")
    f1_detail = "  ".join(f"{l}:{results[l]['mean_final_abs']:.4f}" for l in results)
    f2_detail = "  ".join(f"{l}:{results[l]['spearman_mean']:.3f}" for l in results)
    f3_detail = "  ".join(f"{l}:d={results[l]['control_d']:.2f}" for l in results)
    p(f"  F1 CONVERGENCE  |σ_final−1| < 0.10 for BOTH starts ........ "
      f"{'PASS' if f1 else 'FAIL'}")
    p(f"     ({f1_detail})")
    p(f"  F2 MONOTONE     Spearman(tick,|σ−1|) ≤ −0.6 both .......... "
      f"{'PASS' if f2 else 'FAIL'}")
    p(f"     ({f2_detail})")
    p(f"  F3 CONTROL      frozen |σ−1| > mitosis AND d ≥ 0.8 both ... "
      f"{'PASS' if f3 else 'FAIL'}")
    p(f"     ({f3_detail})")
    p("")
    if supported:
        p("  🟢 SUPPORTED — the cell-division PROCESS self-tunes the engine TOWARD")
        p("     criticality: starting OFF-critical from BOTH a sub-critical (σ0=0.5)")
        p("     AND a super-critical (σ0=1.6) operating point, running tension-driven")
        p("     mitosis ticks drives the branching ratio σ → 1 (|σ−1|<0.10),")
        p("     monotonically (ρ≤−0.6), and a FROZEN no-split control does NOT")
        p("     converge (d≥0.8). MITOSIS IS a branching-ratio homeostat — closing")
        p("     the H_1153 (sits-at-criticality) ⇄ H_1159b (self-tunes-capacity) loop")
        p("     CAUSALLY: the cell-division process is what PUTS the engine there.")
    else:
        p("  🔴 CLOSED-NEGATIVE — the cell-division process does NOT cleanly self-tune")
        p("     the engine toward criticality under the frozen falsifier (see which")
        p("     gate failed). a_paper_negative_ok.")
    p("")
    p(f"  per-gate: F1={f1}  F2={f2}  F3={f3}")
    p(f"  VERDICT = {'🟢 SUPPORTED' if supported else '🔴 CLOSED-NEGATIVE'}")
    p("")
    p("  SCOPE: toy numpy $0 CPU 8 seeds; opponent-propagation engine-sim with an")
    p("  effective-out-degree branching homeostat as the PROXY for A⇄G cell-division")
    p("  (a_lane_akida_gpu_split substrate=Lane-G). Live CORE engine + scale")
    p("  UNVERIFIED (a_scale_honest_scope). CORE files UNTOUCHED (a_core_engine_map).")

    vdir = os.path.join(REPO, ".verdicts", "1161_mitosis_to_criticality")
    os.makedirs(vdir, exist_ok=True)
    with open(os.path.join(vdir, "H_1161.txt"), "w") as f:
        f.write("\n".join(out) + "\n")
    with open("/tmp/h1161_result.json", "w") as f:
        json.dump({"supported": supported, "f1": f1, "f2": f2, "f3": f3,
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
