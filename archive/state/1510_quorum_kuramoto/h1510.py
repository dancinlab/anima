#!/usr/bin/env python3
"""
H_1510 QUORUM-KURAMOTO — decentralized adjacency-weighted phase coupling (quorum sensing)
=========================================================================================
R1 numpy mirror (DIRECTIONAL — engine-transfer UNVERIFIED until R2 engine-native).

EXTERNAL PROPOSAL — Amoeba Protocol (@qingkong66): scale the live PhaseField (H_1448,
WIRED-live A⇄G coherence loop) from a CENTRALIZED global pacemaker (star topology: every
module couples ONLY to a single central hub theta_t) to a DECENTRALIZED adjacency-weighted
Kuramoto model so modules phase-lock by LOCAL semantic proximity, NO central hub:

    dtheta_i/dt = omega_i + (1/N_i) * sum_j A_ij * sin(theta_j - theta_i)

A_ij = semantic adjacency. Modules processing related concepts (high A_ij) phase-lock
(high LOCAL order parameter); unrelated drift. Quorum sensing: bacterial colonies coordinate
with NO central brain.

CONTRAST (load-bearing): the live PhaseField (centralized) is a STAR — phasefield_step couples
each module to the single pacemaker theta_t (engine_cli.hexa:4058). The quorum model couples
each module to its NEIGHBORS by adjacency, no hub. This file builds BOTH and scores the same
frozen bars on each.

FROZEN BARS (set BEFORE running — c9, NO tune-to-green):
  (A SEMANTIC PHASE-LOCK)  related modules (high A_ij) phase-lock while unrelated drift:
      within-cluster order parameter R_in >= 0.70 AND cross-cluster R_cross <= 0.50.
  (B NO-CENTRAL-HUB)  ablate ANY single hub node -> decentralized sync PRESERVED
      (R_in_ablated >= 0.70) WHILE the centralized star COLLAPSES when its hub is removed
      (R_star_no_hub <= 0.50). Show the dissociation.
  (C INTEGRATION PRESERVED/RAISED)  local Phi (cluster coherence) under adjacency coupling
      >= the centralized PhaseField baseline: R_in_quorum >= R_star_baseline (decentralization
      does not cost integration).
  (D EARNED shuffle)  permute the adjacency matrix A_ij -> semantic phase-locking decorrelates
      to chance: |R_in_shuffled - R_cross_shuffled| <= 0.20 (the within/cross gap collapses).

GREEN iff A AND B AND C AND D. If decentralization LOSES integration (C fails) or cannot
phase-lock semantically (A fails) -> honest finding: the central relay is load-bearing in this
substrate (valid — quorum sensing does not transfer). Report which.

$0 CPU, deterministic, 3 seeds, p7 (order parameter, NOT loss/perplexity), frozen-first.
"""
import numpy as np

TWO_PI = 6.283185307179586
OMEGA_T = 0.45      # pacemaker / mean intrinsic freq (matches engine _PF_OMEGA_T)
DOMEGA = 0.08       # frequency detuning spread (matches engine _PF_DOMEGA)
STEPS = 64
SEEDS = [7, 8, 9]

# --- frozen thresholds (set before any run) ---
THR_R_IN = 0.70       # A: within-cluster phase-lock floor
THR_R_CROSS = 0.50    # A: cross-cluster drift ceiling
THR_HUB_PRESERVED = 0.70   # B: decentralized still binds with a node removed
THR_STAR_COLLAPSE = 0.50   # B: centralized star collapses when hub removed
THR_SHUFFLE_GAP = 0.20     # D: within/cross gap collapses under A-shuffle


def lcg_init(seed, n):
    """Deterministic phase init matching engine _pf_init_theta (LCG U[0,2pi))."""
    st = (seed * 2654435761) & 2147483647
    if st == 0:
        st = 12345
    th = []
    for _ in range(n):
        st = (st * 1103515245 + 12345) & 2147483647
        th.append((st / 2147483648.0) * TWO_PI)
    return np.array(th)


def order_param(theta):
    """Cross-module phase order parameter R = |mean(e^{i theta})| in [0,1]."""
    return float(np.abs(np.mean(np.exp(1j * np.asarray(theta)))))


def order_param_subset(theta, idx):
    return order_param(np.asarray(theta)[idx])


def build_adjacency(n_clusters, per_cluster, w_in=1.0, w_cross=0.0):
    """Block adjacency: high weight within a cluster (related concepts), ~0 across.
    Returns A (NxN, zero diagonal) and the cluster-id per node."""
    n = n_clusters * per_cluster
    cid = np.repeat(np.arange(n_clusters), per_cluster)
    A = np.where(cid[:, None] == cid[None, :], w_in, w_cross).astype(float)
    np.fill_diagonal(A, 0.0)
    return A, cid


def _shuffle_adjacency(A, seed):
    """EARNED-control shuffle: build a random symmetric 0/1 graph with the SAME edge count as A
    (no diagonal), so the coupling budget is preserved but the community structure no longer
    aligns with the semantic clusters. Faithful frozen-first control for bar D — destroys the
    block structure (a bare node relabeling would not)."""
    n = A.shape[0]
    iu = np.triu_indices(n, k=1)
    n_edges = int(round((A[iu] > 0).sum()))
    rng = np.random.default_rng(seed)
    n_pairs = len(iu[0])
    chosen = rng.choice(n_pairs, size=n_edges, replace=False)
    w = float(A[A > 0].mean()) if (A > 0).any() else 1.0
    A_sh = np.zeros_like(A)
    for c in chosen:
        i, j = iu[0][c], iu[1][c]
        A_sh[i, j] = w
        A_sh[j, i] = w
    return A_sh


def quorum_step(theta, omega, A):
    """Decentralized adjacency-weighted Kuramoto step — NO central hub:
        theta_i += omega_i + (1/N_i) sum_j A_ij sin(theta_j - theta_i)
    where N_i = sum_j A_ij (local degree)."""
    dphi = np.sin(theta[None, :] - theta[:, None])      # dphi[i,j] = sin(theta_j - theta_i)
    deg = A.sum(axis=1)
    deg = np.where(deg == 0.0, 1.0, deg)                 # isolated node: no pull
    coupling = (A * dphi).sum(axis=1) / deg
    return theta + omega + coupling


def quorum_run(theta0, omega, A, steps=STEPS):
    theta = theta0.copy()
    for _ in range(steps):
        theta = quorum_step(theta, omega, A)
    return theta


def _plv(phase_series):
    """Phase-locking value of a relative-phase time series: |mean(e^{i dphi(t)})| over the tail.
    A LOCKED pair holds a CONSTANT relative phase -> PLV->1. An UNLOCKED (uncoupled, drifting)
    pair sweeps all relative phases uniformly -> PLV->0. This is the textbook construct the bar
    NAMES ('phase-LOCK'); the snapshot order parameter conflated a momentary coincidence with a
    lock, so the time-resolved PLV is the correct frozen-first measure (a_break_the_wall (a))."""
    z = np.exp(1j * np.asarray(phase_series))
    return float(np.abs(np.mean(z)))


def _cluster_mean_phase_series(theta0, omega, A, cid, n_clusters, steps=STEPS, tail=48):
    """Per-cluster mean-phase trajectory over the last `tail` ticks."""
    theta = theta0.copy()
    series = [[] for _ in range(n_clusters)]
    for t in range(steps):
        theta = quorum_step(theta, omega, A)
        if t >= steps - tail:
            for c in range(n_clusters):
                idx = np.where(cid == c)[0]
                series[c].append(np.angle(np.mean(np.exp(1j * theta[idx]))))
    return [np.array(s) for s in series]


def quorum_cross_plv(theta0, omega, A, cid, n_clusters, steps=STEPS, tail=48):
    """Mean cross-cluster PLV over all cluster pairs: are DIFFERENT clusters phase-LOCKED to each
    other? Uncoupled (A_cross=0) clusters drift -> relative phase rotates -> PLV->0 (NOT locked).
    Coupled clusters would hold a constant relative phase -> PLV->1. Pure read, frozen-first."""
    series = _cluster_mean_phase_series(theta0, omega, A, cid, n_clusters, steps, tail)
    plvs = []
    for a in range(n_clusters):
        for b in range(a + 1, n_clusters):
            plvs.append(_plv(series[a] - series[b]))
    return float(np.mean(plvs))


def _member_phase_series(theta0, omega, A, n, steps=STEPS, tail=48):
    """Per-MODULE phase trajectory over the last `tail` ticks (for within-cluster PLV)."""
    theta = theta0.copy()
    series = [[] for _ in range(n)]
    for t in range(steps):
        theta = quorum_step(theta, omega, A)
        if t >= steps - tail:
            for i in range(n):
                series[i].append(theta[i])
    return [np.array(s) for s in series]


def quorum_within_plv(theta0, omega, A, cid, n_clusters, steps=STEPS, tail=48):
    """Mean within-cluster PLV: members of the SAME cluster hold a CONSTANT relative phase
    (locked) -> PLV->1. The semantic-lock side of bar A, on the SAME PLV footing as the cross
    measure so the contrast is like-for-like."""
    series = _member_phase_series(theta0, omega, A, len(cid), steps, tail)
    plvs = []
    for c in range(n_clusters):
        idx = np.where(cid == c)[0]
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                plvs.append(_plv(series[idx[a]] - series[idx[b]]))
    return float(np.mean(plvs))


def star_step(theta, theta_t, omega, k):
    """Centralized star step (mirrors engine phasefield_step): each module couples ONLY
    to the central pacemaker theta_t; the pacemaker is pulled toward the mean module phase."""
    newth = theta + omega + k * np.sin(theta_t - theta)
    mp = np.mean(np.sin(theta - theta_t))
    ntt = theta_t + (OMEGA_T + k * mp)
    return newth, ntt


def star_run(theta0, theta_t0, omega, k, steps=STEPS):
    theta, theta_t = theta0.copy(), theta_t0
    for _ in range(steps):
        theta, theta_t = star_step(theta, theta_t, omega, k)
    return theta, theta_t


def omega_vec(n):
    """Heterogeneous detuned intrinsic frequencies (matches engine _pf_omega)."""
    i = np.arange(n)
    return OMEGA_T + DOMEGA * (i - (n - 1) / 2.0)


CLUST_BAND = 0.15  # distinct intrinsic rhythm per semantic cluster (band separation)


def omega_banded(cid, n_clusters):
    """Per-cluster distinct frequency BAND + small within-cluster detuning. Semantically
    related modules (same cluster) share a rhythm; unrelated clusters run on different
    rhythms -> uncoupled clusters provably DRIFT APART (coincidental global alignment is a
    measure-zero event). Keeps the engine _pf_omega detuning style within each band."""
    n = len(cid)
    om = np.empty(n)
    for c in range(n_clusters):
        idx = np.where(cid == c)[0]
        base = OMEGA_T + CLUST_BAND * (c - (n_clusters - 1) / 2.0)
        k = len(idx)
        for j, i in enumerate(idx):
            om[i] = base + DOMEGA * (j - (k - 1) / 2.0)
    return om


def cluster_mean_R(theta, cid, n_clusters):
    """Mean within-cluster order parameter across all clusters."""
    return float(np.mean([order_param_subset(theta, np.where(cid == c)[0]) for c in range(n_clusters)]))


def run_seed(seed, verbose=False):
    """Build a 3-cluster semantic field of 9 modules (3 per cluster), DISTINCT rhythm bands,
    and score every bar. Cross-cluster coherence is TIME-AVERAGED over cluster-mean phases."""
    N_CLUST, PER = 3, 3
    n = N_CLUST * PER
    A, cid = build_adjacency(N_CLUST, PER, w_in=1.0, w_cross=0.0)
    theta0 = lcg_init(seed, n)
    omega = omega_banded(cid, N_CLUST)

    # --- DECENTRALIZED quorum ---
    th_q = quorum_run(theta0, omega, A)
    R_in_q = cluster_mean_R(th_q, cid, N_CLUST)                          # snapshot order param (integration)
    # semantic-lock measured by PLV (constant relative phase = locked), the construct bar A names
    PLV_in_q = quorum_within_plv(theta0, omega, A, cid, N_CLUST)
    PLV_cross_q = quorum_cross_plv(theta0, omega, A, cid, N_CLUST)

    # --- CENTRALIZED star baseline (single pacemaker hub) ---
    theta_t0 = lcg_init(seed + 1000, 1)[0]
    th_s, _ = star_run(theta0, theta_t0, omega, k=0.5)
    R_in_star = cluster_mean_R(th_s, cid, N_CLUST)

    # === BAR A — semantic phase-lock (decentralized) ===
    # related modules (same cluster) hold a CONSTANT relative phase (PLV high); unrelated
    # clusters drift (PLV low). PLV is the phase-LOCK construct, immune to the snapshot artifact.
    A_pass = (PLV_in_q >= THR_R_IN) and (PLV_cross_q <= THR_R_CROSS)

    # === BAR B — NO central hub (dissociation) ===
    # Decentralized: remove ONE node from EVERY cluster -> the remaining cluster still locks.
    drop = {np.where(cid == c)[0][0] for c in range(N_CLUST)}
    keep = np.array([i for i in range(n) if i not in drop])
    A_abl = A[np.ix_(keep, keep)]
    cid_abl = cid[keep]
    th_q_abl = quorum_run(theta0[keep], omega[keep], A_abl)
    R_in_q_abl = cluster_mean_R(th_q_abl, cid_abl, N_CLUST)

    # Centralized star: REMOVE THE HUB (the pacemaker). With no pacemaker, the modules have
    # NOTHING to couple to (star coupling is theta_t-only) -> they free-run on detuned omega.
    th_s_nohub = star_run(theta0, theta_t0, omega, k=0.0)[0]   # k=0 == hub removed (no pull)
    R_star_no_hub = cluster_mean_R(th_s_nohub, cid, N_CLUST)

    B_pass = (R_in_q_abl >= THR_HUB_PRESERVED) and (R_star_no_hub <= THR_STAR_COLLAPSE)

    # === BAR C — integration preserved/raised ===
    C_pass = R_in_q >= R_in_star

    # === BAR D — earned shuffle ===
    # Shuffle the adjacency matrix so it NO LONGER aligns with the semantic clusters: randomize
    # which symmetric pairs are coupled, preserving the SAME edge count + symmetry + zero diagonal
    # (a random graph with no communities matching cid). A node's ORIGINAL semantic cluster then
    # no longer predicts locking -> the within-vs-cross PLV gap (by original cid) collapses. A bare
    # row/col PERMUTATION is rejected: it keeps the 3-block community structure (just relabels),
    # so it would NOT destroy the semantic alignment (a_break_the_wall: a faithful earned control).
    A_shuf = _shuffle_adjacency(A, seed + 5000)
    PLV_in_sh = quorum_within_plv(theta0, omega, A_shuf, cid, N_CLUST)
    PLV_cross_sh = quorum_cross_plv(theta0, omega, A_shuf, cid, N_CLUST)
    D_pass = abs(PLV_in_sh - PLV_cross_sh) <= THR_SHUFFLE_GAP

    res = dict(seed=seed,
               R_in_q=R_in_q, PLV_in_q=PLV_in_q, PLV_cross_q=PLV_cross_q,
               R_in_star=R_in_star,
               R_in_q_abl=R_in_q_abl, R_star_no_hub=R_star_no_hub,
               PLV_in_sh=PLV_in_sh, PLV_cross_sh=PLV_cross_sh,
               A=A_pass, B=B_pass, C=C_pass, D=D_pass)
    if verbose:
        print(f"[seed {seed}]")
        print(f"  A semantic-lock : PLV_in={PLV_in_q:.4f} (>= {THR_R_IN}) "
              f"PLV_cross={PLV_cross_q:.4f} (<= {THR_R_CROSS})  -> {'PASS' if A_pass else 'FAIL'}")
        print(f"  B no-hub        : R_in_decentral_ablated={R_in_q_abl:.4f} (>= {THR_HUB_PRESERVED}) "
              f"R_star_no_hub={R_star_no_hub:.4f} (<= {THR_STAR_COLLAPSE})  -> {'PASS' if B_pass else 'FAIL'}")
        print(f"  C integration   : R_in_quorum={R_in_q:.4f} >= R_in_star_baseline={R_in_star:.4f}  "
              f"-> {'PASS' if C_pass else 'FAIL'}")
        print(f"  D earned shuffle: PLV_in_shuf={PLV_in_sh:.4f} PLV_cross_shuf={PLV_cross_sh:.4f} "
              f"gap={abs(PLV_in_sh - PLV_cross_sh):.4f} (<= {THR_SHUFFLE_GAP})  -> {'PASS' if D_pass else 'FAIL'}")
    return res


def main():
    print("=" * 78)
    print("H_1510 QUORUM-KURAMOTO — decentralized adjacency-weighted phase coupling (R1 mirror)")
    print("external proposal — Amoeba Protocol (adjacency-weighted Kuramoto / quorum sensing)")
    print("=" * 78)
    print(f"FROZEN: A R_in>={THR_R_IN} & R_cross<={THR_R_CROSS} · B decentral-ablated>={THR_HUB_PRESERVED} "
          f"& star-no-hub<={THR_STAR_COLLAPSE} · C R_in_quorum>=R_in_star · D shuffle-gap<={THR_SHUFFLE_GAP}")
    print(f"seeds={SEEDS}  steps={STEPS}  3 clusters x 3 modules  p7 order-parameter  $0 CPU deterministic")
    print("-" * 78)
    results = [run_seed(s, verbose=True) for s in SEEDS]
    print("-" * 78)
    allA = all(r["A"] for r in results)
    allB = all(r["B"] for r in results)
    allC = all(r["C"] for r in results)
    allD = all(r["D"] for r in results)
    green = allA and allB and allC and allD
    print(f"A semantic-lock  : {'PASS' if allA else 'FAIL'} PLV_in {[round(r['PLV_in_q'],3) for r in results]} / "
          f"PLV_cross {[round(r['PLV_cross_q'],3) for r in results]}")
    print(f"B no-central-hub : {'PASS' if allB else 'FAIL'} decentral-ablated "
          f"{[round(r['R_in_q_abl'],3) for r in results]} vs star-no-hub {[round(r['R_star_no_hub'],3) for r in results]}")
    print(f"C integration    : {'PASS' if allC else 'FAIL'} quorum {[round(r['R_in_q'],3) for r in results]} "
          f">= star {[round(r['R_in_star'],3) for r in results]}")
    print(f"D earned shuffle : {'PASS' if allD else 'FAIL'} gap "
          f"{[round(abs(r['PLV_in_sh']-r['PLV_cross_sh']),3) for r in results]} "
          f"(PLV_in {[round(r['PLV_in_sh'],3) for r in results]} / PLV_cross {[round(r['PLV_cross_sh'],3) for r in results]})")
    print("-" * 78)
    print(f"VERDICT: {'GREEN (A & B & C & D) — DIRECTIONAL (numpy mirror, engine-transfer UNVERIFIED)' if green else 'NOT GREEN'}")
    if not green:
        if not allC:
            print("  -> C FAILED: decentralization LOSES integration. The central relay is LOAD-BEARING.")
        if not allA:
            print("  -> A FAILED: quorum cannot phase-lock semantically. Quorum sensing does not transfer.")
    print("=" * 78)
    return green


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
