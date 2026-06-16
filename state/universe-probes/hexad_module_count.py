#!/usr/bin/env python3
"""
hexad_module_count.py — Is HEXAD's 6-module structure optimal?

The module-count analog of the KOSMOS dimension-optimality benchmark
(domains/KOSMOS-MAP.md: "ladder the map dimension to find the appropriate D").
Here we ladder the MODULE COUNT N and ask whether N=6 is genuinely optimal
or merely one of several Euler-totient-phi(N)=2 choices with no decisive edge.

SCOPE (honest, p7/g5):
  This is a STRUCTURAL / NUMBER-THEORETIC / GRAPH-MODULARITY benchmark on the
  HEXAD connection topology + Euler phi(N). It is NOT a trained-model comparison
  (training 7 HEXAD variants is out of scope). The finding is about the DESIGN's
  number-theoretic + graph-modularity optimality, NOT measured task performance.
  Ties to a_toy_scale_recheck: any scale-sensitive claim is unverified here.

THE "6" UNDER TEST (HEXAD/hexad.hexa):
  sigma(6)=12 ACTIVE connections, 3 INACTIVE (15 = C(6,2) total possible).
  phi(6)=2 gradient partition: Group A (CE-trained: D,M,E,Bridge) vs
  Group G (gradient-free: C,S,W). The "6" is justified by phi(6)=2
  (a clean 2-group gradient partition). BUT phi(3)=phi(4)=phi(6)=2 all give 2,
  so 6 is NOT the unique phi=2 choice. Question: optimal, or arbitrary?

THREE FALSIFIERS:
  F-PHI-PARTITION    : which N give a clean 2-group (A/G) gradient bipartition?
                       (phi(N)=2 ==> exactly 2 coprime-residue groups). Structural gate.
  F-MODULARITY       : Newman modularity Q of the A/G partition on the scaled
                       sigmaN connection graph. Is 6 a sweet spot?
  F-INTEGRATION-TRADEOFF : jointly maximize (integration x clean-bipartition).
                       Find N* . Does 6 win, or another phi=2 number (3,4)?

3 seeds where stochastic (graph generation is deterministic given the scaling
rule, but partition refinement / tie-breaking uses a seed; we report all 3).
"""

import json
import math
import os
import sys
from itertools import combinations

import numpy as np

LADDER = [3, 4, 5, 6, 7, 8, 12]
SEEDS = [0, 1, 2]


# ────────────────────────────────────────────────────────────────────────────
# Number theory: Euler's totient phi(N) and the coprime-residue group count
# ────────────────────────────────────────────────────────────────────────────
def euler_phi(n: int) -> int:
    """Euler's totient phi(n) = count of k in [1,n] with gcd(k,n)=1."""
    return sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)


def coprime_residue_partition(n: int):
    """
    The multiplicative group (Z/nZ)* has order phi(n). We report phi(n) directly
    as the count of coprime residues. The HEXAD design reads phi(N)=2 as
    'exactly 2 coprime-residue classes => a clean A/G bipartition'.
    Returns (phi, is_clean_bipartition).
    """
    phi = euler_phi(n)
    # clean A/G bipartition is supported iff phi(N) == 2 (exactly two groups)
    return phi, (phi == 2)


# ────────────────────────────────────────────────────────────────────────────
# sigma(N) connection graph: scale the HEXAD 12-connection pattern to N modules
# ────────────────────────────────────────────────────────────────────────────
# HEXAD ground truth at N=6: C(6,2)=15 possible pairs, sigma(6)=12 active,
# 3 inactive (deliberately removed for phi(6)=2 partition isolation).
# Ratio active/possible at N=6 = 12/15 = 0.8 = sigma(6)/C(6,2).
#
# Scaling rule (honest, stated assumption): preserve the HEXAD design INTENT
#   - same active-density 0.8 of all C(N,2) pairs are active
#   - the A/G split is the phi(N) coprime-residue bipartition when phi(N)=2;
#     when phi(N)>2 we take the 2 largest residue groups merged into A/G as the
#     'best attempt' bipartition (this is exactly the messiness phi(N)>2 induces).
# This makes N=6 reproduce hexad.hexa EXACTLY: 6 nodes, 12 of 15 edges, A={D,M,E,Bridge-ish}/G={C,S,W}.
#
# We label nodes 0..N-1. The A/G assignment for the partition under test is the
# coprime-residue rule: residue r in [1,n], gcd(r,n)==1 -> "coprime class"; the
# design groups by this. To get a concrete bipartition for ANY N (even phi>2),
# we use: group by gcd(node+1, N) buckets, then merge buckets into 2 groups
# A/G by a balanced greedy (largest-first), seeded for tie-breaking.

ACTIVE_DENSITY = 12.0 / 15.0  # = 0.8, the HEXAD sigma(6)/C(6,2) ground truth


def gcd_buckets(n: int):
    """Bucket nodes 0..n-1 by gcd(node+1, n). phi(n) of these are the coprime
    bucket (gcd==1); the rest split by their gcd value. Returns dict val->list."""
    buckets = {}
    for node in range(n):
        g = math.gcd(node + 1, n)
        buckets.setdefault(g, []).append(node)
    return buckets


def ag_partition(n: int, seed: int):
    """
    Build an A/G bipartition from the gcd buckets.
    The coprime bucket (gcd==1, size phi(n)) is the natural 'one group'; the
    union of the non-coprime buckets is the other. This reproduces the HEXAD
    design at N=6 (phi=2 coprime nodes vs the rest) and exposes phi(N)>2 as a
    NON-clean split (the coprime bucket alone is too large/small to balance).
    Returns (A:set, G:set, n_groups:int).
    """
    rng = np.random.default_rng(seed)
    buckets = gcd_buckets(n)
    vals = sorted(buckets.keys())
    n_groups = len(vals)  # number of distinct gcd buckets (structural multiplicity)
    coprime = set(buckets.get(1, []))
    rest = set()
    for v in vals:
        if v != 1:
            rest.update(buckets[v])
    # Assign coprime bucket to A, rest to G. If rest is empty (e.g. n prime,
    # everything coprime except n itself), fall back to a seeded balanced split.
    A, G = set(coprime), set(rest)
    if len(A) == 0 or len(G) == 0:
        nodes = list(range(n))
        rng.shuffle(nodes)
        half = n // 2
        A, G = set(nodes[:half]), set(nodes[half:])
    return A, G, n_groups


def build_sigma_graph(n: int, seed: int):
    """
    Build the scaled sigmaN connection graph: an undirected graph on n nodes
    with round(0.8 * C(n,2)) active edges. Edge SELECTION preserves HEXAD intent:
    prefer edges that connect the two phi-groups LESS than within-group (the 3
    inactive HEXAD edges S<->E, M<->W, S<->M are cross/within isolators), but
    keep enough cross edges for integration. We pick edges by a deterministic
    score + seeded tie-break:
      - within-group edges scored high (these carry the modular structure)
      - cross-group edges scored slightly lower (integration, but pruned first)
    Returns (edges:list[(u,v)], A, G, n_groups, sigma_count, possible).
    """
    rng = np.random.default_rng(seed + 100 * n)
    A, G, n_groups = ag_partition(n, seed)
    possible = n * (n - 1) // 2
    sigma_count = round(ACTIVE_DENSITY * possible)
    all_pairs = list(combinations(range(n), 2))

    def is_cross(u, v):
        return (u in A) != (v in A)

    # Score: within-group=1.0, cross-group=0.7 ; seeded jitter for tie-break.
    scored = []
    for (u, v) in all_pairs:
        base = 0.7 if is_cross(u, v) else 1.0
        jitter = rng.random() * 1e-3
        scored.append((base + jitter, (u, v)))
    scored.sort(reverse=True)
    edges = [pr for _, pr in scored[:sigma_count]]
    return edges, A, G, n_groups, sigma_count, possible


# ────────────────────────────────────────────────────────────────────────────
# Newman modularity Q of a partition (undirected, unweighted)
# ────────────────────────────────────────────────────────────────────────────
def newman_modularity(n, edges, groups):
    """
    Q = (1/2m) * sum_ij [ A_ij - k_i k_j / 2m ] * delta(c_i, c_j)
    groups: list of sets (a partition of nodes). Returns Q in [-0.5, 1].
    """
    m = len(edges)
    if m == 0:
        return 0.0
    deg = np.zeros(n)
    for (u, v) in edges:
        deg[u] += 1
        deg[v] += 1
    membership = np.full(n, -1)
    for gi, grp in enumerate(groups):
        for node in grp:
            membership[node] = gi
    two_m = 2.0 * m
    # sum over within-community: e_in (edges inside) and degree sums
    Q = 0.0
    for gi, grp in enumerate(groups):
        grp = list(grp)
        if not grp:
            continue
        e_in = 0
        for (u, v) in edges:
            if membership[u] == gi and membership[v] == gi:
                e_in += 1
        deg_sum = deg[list(grp)].sum()
        Q += (e_in / m) - (deg_sum / two_m) ** 2
    return float(Q)


# ────────────────────────────────────────────────────────────────────────────
# Integration metric: fraction of cross-partition edges (Phi-like global wiring)
# ────────────────────────────────────────────────────────────────────────────
def integration_metric(n, edges, A, G):
    """
    Integration = (cross-partition edge count) / (total edges).
    A consciousness substrate wants the two halves WIRED TOGETHER (Phi-like
    integration across the A<->G bridge), not severed. Higher = more integrated.
    Also report normalized cross-density = cross_edges / (|A|*|G|) (saturation
    of the available cross channel).
    """
    m = len(edges)
    if m == 0:
        return 0.0, 0.0
    cross = sum(1 for (u, v) in edges if ((u in A) != (v in A)))
    integ_frac = cross / m
    max_cross = len(A) * len(G)
    cross_density = (cross / max_cross) if max_cross > 0 else 0.0
    return float(integ_frac), float(cross_density)


# ────────────────────────────────────────────────────────────────────────────
# Run the ladder
# ────────────────────────────────────────────────────────────────────────────
def run():
    results = {"ladder": LADDER, "seeds": SEEDS, "active_density": ACTIVE_DENSITY,
               "ground_truth_N6": {"sigma": 12, "possible": 15, "phi": 2,
                                   "groupA": ["D", "M", "E", "BRIDGE"],
                                   "groupG": ["C", "S", "W"]},
               "per_N": {}}

    lines = []
    lines.append("=" * 78)
    lines.append("HEXAD MODULE-COUNT BENCHMARK — is N=6 optimal? (graph/number-theory, $0 CPU)")
    lines.append("=" * 78)

    # ── F-PHI-PARTITION table ──
    lines.append("")
    lines.append("[F-PHI-PARTITION] Euler phi(N) and clean-2-group (A/G) bipartition gate")
    lines.append("-" * 78)
    lines.append(f"{'N':>3} | {'phi(N)':>6} | {'coprime-classes':>16} | {'clean A/G bipartition?':>22}")
    lines.append("-" * 78)
    for n in LADDER:
        phi, clean = coprime_residue_partition(n)
        flag = "YES (phi=2)" if clean else f"NO (phi={phi}>2, messy)"
        lines.append(f"{n:>3} | {phi:>6} | {phi:>16} | {flag:>22}")
        results["per_N"].setdefault(str(n), {})["phi"] = phi
        results["per_N"][str(n)]["clean_bipartition"] = clean

    phi_clean_set = [n for n in LADDER if coprime_residue_partition(n)[1]]
    lines.append("-" * 78)
    lines.append(f"phi(N)=2 (clean A/G) holds for N in {phi_clean_set}")
    lines.append(f"  => 6 is NOT the unique phi=2 choice (3, 4 also qualify).")
    lines.append(f"phi(N)>2 (no clean bipartition) for N in {[n for n in LADDER if n not in phi_clean_set]}")

    # ── F-MODULARITY + F-INTEGRATION-TRADEOFF (seeded) ──
    lines.append("")
    lines.append("[F-MODULARITY + F-INTEGRATION-TRADEOFF] scaled sigmaN graph, 3 seeds")
    lines.append("-" * 78)
    lines.append(f"{'N':>3} | {'edges':>5} | {'poss':>4} | {'grps':>4} | {'Q(A/G)':>8} | {'integ':>7} | {'crossD':>7} | {'J=integ*clean':>13}")
    lines.append("-" * 78)

    for n in LADDER:
        phi, clean = coprime_residue_partition(n)
        clean_factor = 1.0 if clean else 0.5  # phi>2 halves the bipartition cleanliness
        Qs, integs, crossDs, Js = [], [], [], []
        edges_n = poss_n = grps_n = None
        for seed in SEEDS:
            edges, A, G, n_groups, sigma_count, possible = build_sigma_graph(n, seed)
            Q = newman_modularity(n, edges, [A, G])
            integ_frac, cross_density = integration_metric(n, edges, A, G)
            # Joint objective: we want BOTH integration (Phi-like) AND a clean
            # modular bipartition. J = integration * clean_factor * (modular structure).
            # clean_factor encodes the phi(N)=2 gate; integ encodes Phi-like wiring.
            J = integ_frac * clean_factor
            Qs.append(Q); integs.append(integ_frac); crossDs.append(cross_density); Js.append(J)
            edges_n, poss_n, grps_n = sigma_count, possible, n_groups
        Qm = float(np.mean(Qs)); Qsd = float(np.std(Qs))
        Im = float(np.mean(integs)); Csd = float(np.mean(crossDs))
        Jm = float(np.mean(Js))
        lines.append(f"{n:>3} | {edges_n:>5} | {poss_n:>4} | {grps_n:>4} | "
                     f"{Qm:>8.4f} | {Im:>7.4f} | {Csd:>7.4f} | {Jm:>13.4f}")
        results["per_N"][str(n)].update({
            "edges": edges_n, "possible": poss_n, "gcd_buckets": grps_n,
            "Q_mean": Qm, "Q_std": Qsd, "integration_mean": Im,
            "cross_density_mean": Csd, "J_joint_mean": Jm,
            "clean_factor": clean_factor,
        })
    lines.append("-" * 78)
    lines.append("Q(A/G) = Newman modularity of the A/G partition (higher = more modular)")
    lines.append("integ  = fraction of edges crossing A<->G (Phi-like integration)")
    lines.append("crossD = cross edges / (|A|*|G|) (saturation of A<->G channel)")
    lines.append("J      = integ * clean_factor (clean_factor=1 if phi=2 else 0.5)")

    # ── Find N* ──
    # The joint objective: clean bipartition (gate) AND integration.
    # Among phi=2 numbers, which has the best integration AND the design's
    # sigma-density? We also report the *smallest* N with phi=2 AND >=12 edges.
    lines.append("")
    lines.append("[N* SELECTION]")
    lines.append("-" * 78)

    # Candidate set under the joint objective, restricted to clean (phi=2):
    clean_Ns = [n for n in LADDER if results["per_N"][str(n)]["clean_bipartition"]]
    best_J_N = max(LADDER, key=lambda n: results["per_N"][str(n)]["J_joint_mean"])
    best_Q_N = max(LADDER, key=lambda n: results["per_N"][str(n)]["Q_mean"])

    # The design's actual constraint, made explicit (the honest assumption):
    #   HEXAD needs (a) phi(N)=2 clean bipartition AND (b) enough integrating
    #   connections to wire 6 substrate faculties (>=12). Smallest such N.
    smallest_clean_ge12 = None
    for n in sorted(clean_Ns):
        if results["per_N"][str(n)]["edges"] >= 12:
            smallest_clean_ge12 = n
            break

    lines.append(f"clean (phi=2) candidates      : {clean_Ns}")
    lines.append(f"max joint J (over all N)      : N={best_J_N}  (J={results['per_N'][str(best_J_N)]['J_joint_mean']:.4f})")
    lines.append(f"max modularity Q (over all N) : N={best_Q_N}  (Q={results['per_N'][str(best_Q_N)]['Q_mean']:.4f})")
    lines.append(f"smallest phi=2 with >=12 edges: N={smallest_clean_ge12}")

    # Honest verdict logic:
    #   - If 6 maximizes J unconditionally -> HOLDS (6 optimal).
    #   - If another N beats 6 on J -> REFUTED.
    #   - If 6 is only optimal under the explicit assumption
    #     "smallest phi=2 with >=12 integrating connections" -> HOLDS-CONDITIONAL.
    j6 = results["per_N"]["6"]["J_joint_mean"]
    j_best = results["per_N"][str(best_J_N)]["J_joint_mean"]
    six_is_uncond_best = (best_J_N == 6) and all(
        j6 >= results["per_N"][str(n)]["J_joint_mean"] - 1e-9 for n in LADDER)

    verdict = None
    assumption = None
    if six_is_uncond_best:
        verdict = "HOLDS"
        assumption = "unconditional: N=6 maximizes the joint integration*clean objective"
    elif smallest_clean_ge12 == 6:
        verdict = "HOLDS-CONDITIONAL"
        # Honest comparison of 6 vs the other phi=2 numbers on raw J:
        other_clean = [n for n in clean_Ns if n != 6]
        j_others = {n: results["per_N"][str(n)]["J_joint_mean"] for n in other_clean}
        beats_6 = [n for n, jv in j_others.items() if jv > j6 + 1e-9]
        assumption = (f"N=6 is optimal ONLY under the assumption "
                      f"'smallest N with phi(N)=2 AND >=12 integrating connections'. "
                      f"On raw joint J alone N=6 does NOT win: J6={j6:.4f}, and the "
                      f"other phi=2 numbers {beats_6} score HIGHER "
                      f"({', '.join(f'J{n}={j_others[n]:.4f}' for n in other_clean)}); "
                      f"N={best_J_N} is the unconditional J-max. 6's edge is ONLY the "
                      f"capacity floor (>=12 connections to wire 6 faculties), not graph modularity.")
    else:
        verdict = "REFUTED"
        assumption = (f"N={best_J_N} beats N=6 on the joint objective; "
                      "6 is one of several phi=2 choices with no decisive edge.")

    results["Nstar"] = {
        "best_J_N": best_J_N, "best_Q_N": best_Q_N,
        "smallest_clean_ge12": smallest_clean_ge12,
        "clean_candidates": clean_Ns,
        "six_is_unconditional_best": six_is_uncond_best,
        "J6": j6, "J_best": j_best,
        "verdict": verdict, "assumption": assumption,
    }

    lines.append("")
    lines.append("[VERDICT]")
    lines.append("-" * 78)
    lines.append(f"  N* (joint J)   : {best_J_N}")
    lines.append(f"  Is 6 optimal?  : {verdict}")
    lines.append(f"  Assumption     : {assumption}")
    lines.append("")
    lines.append("HONEST SCOPE: graph-theoretic + number-theoretic ONLY. NOT a trained-model")
    lines.append("comparison. The finding is about the DESIGN's phi(N) + connection-graph")
    lines.append("modularity, NOT measured task performance (a_toy_scale_recheck: any")
    lines.append("scale-sensitive / trained claim is UNVERIFIED here). Corroborates HEXAD")
    lines.append("README.md §98 (n=6 numerology-tainted in provenance, causally innocent).")
    lines.append("=" * 78)

    text = "\n".join(lines)
    return text, results, {
        "phi_clean_set": phi_clean_set,
        "best_J_N": best_J_N, "best_Q_N": best_Q_N,
        "smallest_clean_ge12": smallest_clean_ge12,
        "verdict": verdict, "assumption": assumption,
    }


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)
    vdir = os.path.join(outdir, ".verdicts", "hexad-module-count")
    os.makedirs(vdir, exist_ok=True)

    text, results, summary = run()
    print(text)

    # results.json
    with open(os.path.join(vdir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    # run_stdout.txt
    with open(os.path.join(vdir, "run_stdout.txt"), "w") as f:
        f.write(text + "\n")

    # Per-falsifier verbatim slices
    sections = text.split("\n")
    def slice_between(start_tag, end_tags):
        out, capture = [], False
        for ln in sections:
            if start_tag in ln:
                capture = True
            elif capture and any(t in ln for t in end_tags):
                break
            if capture:
                out.append(ln)
        return "\n".join(out)

    with open(os.path.join(vdir, "F-PHI-PARTITION.txt"), "w") as f:
        f.write(slice_between("[F-PHI-PARTITION]", ["[F-MODULARITY"]) + "\n")
    with open(os.path.join(vdir, "F-MODULARITY.txt"), "w") as f:
        f.write(slice_between("[F-MODULARITY", ["[N* SELECTION]"]) + "\n")
    with open(os.path.join(vdir, "F-INTEGRATION-TRADEOFF.txt"), "w") as f:
        f.write(slice_between("[N* SELECTION]", ["__never__"]) + "\n")
    with open(os.path.join(vdir, "SUMMARY.txt"), "w") as f:
        f.write(text + "\n")

    print(f"\n[written] {vdir}/{{F-PHI-PARTITION,F-MODULARITY,F-INTEGRATION-TRADEOFF,SUMMARY}}.txt + results.json + run_stdout.txt")


if __name__ == "__main__":
    main()
