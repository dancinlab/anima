#!/usr/bin/env python3
# H_1317 — DISTRIBUTED MULTI-EDGE (SMALL-WORLD) COUPLING → ROBUST faithful-IIT4 Φ?
# slug: 1317_phi_multiedge   PROJ_SEED=1317
# lens: integrated-information from a small-world recurrent MESH, NOT a central hub
#       (c15 / a_no_llm_frame_trap — neuro topology, NOT an LLM recipe)
#
# WALL (c16 / a_break_the_wall): H_1283 (thalamus-Φ) — EVERY central-relay/star
# content cut raised faithful-IIT4 Φ only SEED-CONDITIONALLY (failed a 3-seed
# robustness gate, esp. the orthogonal seed). A single central relay (star) gives
# a FRAGILE Φ lift. 🧱 WALL on the TOPOLOGY/content axis.
#
# THE UNTRIED ANGLE: does a DISTRIBUTED multi-edge (Watts-Strogatz small-world)
# coupling topology raise faithful-IIT4 Φ ROBUSTLY across 3 seeds where the single
# central relay FAILED the SAME gate? Many short + few long edges (small-world
# recurrent mesh), NOT one hub.
#
# Φ = FAITHFUL IIT4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Φ —
# it only emits the per-unit salience (state-energy) trajectory; the hexa engine
# computes Φ. NO variance×energy proxy as a terminal verdict.
#
# Substrate MATCHED to H_1283 (only the coupling TOPOLOGY changes between arms):
# leaky linear recurrent units, LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit PRIVATE
# gaussian input, dim-8 state, T=64 ticks. N=8 units (n<=8 keeps faithful MIP
# EXACT; >4 nodes so small-world is non-degenerate). 3 arms at MATCHED total
# coupling budget (Σ edge weights equal across CENTRAL / MULTI-EDGE / SHUFFLE) so
# any lift is TOPOLOGY, not more coupling.
#
# FROZEN BARS (see H_1317_FREEZE.txt — GREEN iff C1 ∧ C2 ∧ C3):
#   C1 ROBUST LIFT : MULTI-EDGE Φ >= NO-COUPLING Φ + 0.02 on ALL 3 seeds (the gate
#                    H_1283 FAILED).
#   C2 TOPOLOGY-EARNED : MULTI-EDGE Φ > SHUFFLE Φ (matched edges+budget) on >=2/3
#                    seeds AND in the seed-mean.
#   C3 BEATS-CENTRAL : MULTI-EDGE passes C1 (all 3 seeds) WHILE CENTRAL does NOT
#                    (CENTRAL fails C1 on >=1 seed) — distributed robust where star
#                    is fragile.
# seeds [1317,1318,1319]. $0 CPU-local. frozen-first.

import os, sys, json, subprocess, tempfile
import numpy as np

SEEDS   = [1317, 1318, 1319]
N       = 8          # substrate units (n<=8 keeps faithful IIT4 MIP exact)
DIM     = 8          # per-unit state vector dim (H_1283 = 8)
T       = 64         # ticks (H_1283 = 64)
GAIN    = 0.30       # per-unit update gain (H_1283)
LEAK    = 0.55       # state self-retention (H_1283)
W_IN    = 0.5        # private-input weight (H_1283)
NBINS   = 8          # IIT4 MI estimator bins (H_1283)

# small-world (Watts-Strogatz) params — FROZEN, NOT swept (p7/c9)
K_LATTICE = 2        # ring-lattice: K nearest neighbours EACH side (4 edges/node)
BETA      = 0.30     # rewiring probability (a few long-range shortcuts)

# CENTRAL star reference weight per spoke. The other arms' edge weight is SCALED so
# the TOTAL coupling budget (Σ edge weights) MATCHES the star exactly.
W_STAR_SPOKE = 0.5   # H_1283-scale coupling magnitude per hub spoke

MARGIN_PHI = 0.02    # IDENTICAL faithful-Φ margin H_1283 froze (NOT moved)

HEXA     = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"
FAITHFUL = os.path.join(HEXA_ROOT, "stdlib/consciousness/iit4/faithful_phi.hexa")


# ── topology builders. Each returns an undirected edge list [(i,j), ...], i<j. ──
def edges_central(n):
    """STAR: hub unit 0 bidirectionally connected to all other n-1 units.
    Leaves NOT inter-connected. This is the H_1283 single-relay baseline."""
    return [(0, j) for j in range(1, n)]


def edges_small_world(n, k, beta, rng):
    """Watts-Strogatz small-world: ring lattice (each node to k neighbours each
    side) then rewire each lattice edge with prob beta to a random far target.
    Returns a deduped undirected edge set."""
    # ring lattice edges (i, (i+off) mod n) for off in 1..k
    lattice = set()
    for i in range(n):
        for off in range(1, k + 1):
            j = (i + off) % n
            e = (min(i, j), max(i, j))
            lattice.add(e)
    # rewire: iterate lattice edges in canonical order; with prob beta move the
    # (i,*) endpoint to a new random target m (no self-loop, no duplicate).
    edges = set(lattice)
    for (i, j) in sorted(lattice):
        if rng.random() < beta:
            # choose new target for the i-endpoint
            cur = set(a for e in edges for a in [e[0], e[1]] if i in e and a != i)
            choices = [m for m in range(n) if m != i and m not in cur]
            if not choices:
                continue
            m = int(rng.choice(choices))
            new_e = (min(i, m), max(i, m))
            if new_e in edges:
                continue
            edges.discard((min(i, j), max(i, j)))
            edges.add(new_e)
    return sorted(edges)


def edges_erdos_renyi(n, m_edges, rng):
    """Erdos-Renyi: m_edges placed UNIFORMLY AT RANDOM (no ring/locality),
    no self-loops, no duplicates. Used as the SHUFFLE control (matched edge
    count to MULTI-EDGE, matched budget via weight scaling)."""
    all_possible = [(i, j) for i in range(n) for j in range(i + 1, n)]
    rng.shuffle(all_possible)
    return sorted(all_possible[:m_edges])


def adjacency_from_edges(n, edges):
    """neighbour lists from an undirected edge set."""
    adj = [[] for _ in range(n)]
    for (i, j) in edges:
        adj[i].append(j)
        adj[j].append(i)
    return adj


def run_arm(seed, mode):
    """mode in {'none','central','multiedge','shuffle'}.
    Returns (traj (N,T) per-unit salience, n_edges, total_budget, edges).

    Substrate matched to H_1283: leaky linear recurrent units with PRIVATE input.
    coupling_i = W_edge * mean over neighbours j of unit i (in this arm's graph).
    MATCHED BUDGET: total Σ (W_edge over each undirected edge counted once) equals
    the CENTRAL star budget (n-1) * W_STAR_SPOKE — so a Φ lift is TOPOLOGY, not
    more total coupling."""
    rng = np.random.default_rng(seed)
    # initial unit states — distinct per unit so MI is well-defined (H_1283 style)
    states = rng.standard_normal((N, DIM)) * 0.5
    # PER-UNIT PRIVATE input streams (SAME across arms via same seed/order)
    inputs = rng.standard_normal((N, T, DIM)) * 0.8

    # topology rng — a DISTINCT sub-stream so the same state/input draws above are
    # byte-identical across arms (only the graph differs).
    grng = np.random.default_rng(seed * 1000003 + 17)

    star_budget = (N - 1) * W_STAR_SPOKE  # the matched total coupling budget

    if mode == "none":
        edges = []
        w_edge = 0.0
    elif mode == "central":
        edges = edges_central(N)
        # each undirected edge weighted W_STAR_SPOKE → total = (N-1)*W_STAR_SPOKE
        w_edge = W_STAR_SPOKE
    elif mode == "multiedge":
        edges = edges_small_world(N, K_LATTICE, BETA, grng)
        # scale per-edge weight so Σ weights == star_budget (matched budget)
        w_edge = star_budget / max(1, len(edges))
    elif mode == "shuffle":
        # match the MULTI-EDGE edge COUNT for this seed, then place at random
        sw_edges = edges_small_world(N, K_LATTICE, BETA, np.random.default_rng(seed * 1000003 + 17))
        m = len(sw_edges)
        edges = edges_erdos_renyi(N, m, grng)
        w_edge = star_budget / max(1, len(edges))
    else:
        raise ValueError(mode)

    adj = adjacency_from_edges(N, edges)
    total_budget = w_edge * len(edges)

    traj = np.zeros((N, T))
    for t in range(T):
        new = states.copy()
        for i in range(N):
            if adj[i]:
                nbr = np.mean([states[k] for k in adj[i]], axis=0)
                coupling = w_edge * nbr
            else:
                coupling = 0.0
            new[i] = LEAK * states[i] + GAIN * (coupling + W_IN * inputs[i, t])
        states = new
        # per-unit salience scalar this tick = state energy (H_1283 Φ-leg readout)
        for i in range(N):
            traj[i, t] = float(np.dot(states[i], states[i]))
    return traj, len(edges), total_budget, edges


def faithful_phi(traj, tag):
    """faithful IIT4 Φ over the n=N unit trajectories via the stdlib EXACT engine
    (hexa run). Inlines the trajectory as farr_set calls, calls
    iit4_faithful_phi(state, n=N, dim=T, n_bins). Returns float Φ (or None)."""
    n, dim = traj.shape
    flat = traj.flatten()
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
    print("H_1317 DISTRIBUTED MULTI-EDGE (SMALL-WORLD) COUPLING → faithful-IIT4 Φ")
    print(f"N={N} dim={DIM} ticks={T} seeds={SEEDS}  K_lattice={K_LATTICE} beta={BETA}")
    print(f"faithful IIT4 Φ (exact MIP-EI, n={N}); MARGIN_PHI={MARGIN_PHI}")
    print("=" * 78)

    per_seed = {}
    star_budget = (N - 1) * W_STAR_SPOKE
    for seed in SEEDS:
        d = {}
        for mode in ("none", "central", "multiedge", "shuffle"):
            traj, ne, budget, edges = run_arm(seed, mode)
            d[mode] = {"traj": traj, "n_edges": ne, "budget": budget, "edges": edges}
        # BUDGET IDENTITY assertion: central / multiedge / shuffle must share Σweights
        b_c = d["central"]["budget"]; b_m = d["multiedge"]["budget"]; b_s = d["shuffle"]["budget"]
        budget_ok = (abs(b_c - b_m) < 1e-9 and abs(b_c - b_s) < 1e-9)
        d["budget_ok"] = budget_ok
        d["budget_vals"] = {"central": b_c, "multiedge": b_m, "shuffle": b_s}
        d["edge_counts"] = {"central": d["central"]["n_edges"],
                            "multiedge": d["multiedge"]["n_edges"],
                            "shuffle": d["shuffle"]["n_edges"]}
        per_seed[seed] = d
        print(f"seed {seed}: edges central={d['central']['n_edges']} "
              f"multiedge={d['multiedge']['n_edges']} shuffle={d['shuffle']['n_edges']} | "
              f"Σbudget c={b_c:.4f} m={b_m:.4f} s={b_s:.4f} | BUDGET_OK={budget_ok}")
        if not budget_ok:
            print("  !! BUDGET MISMATCH — run INVALID, no verdict", file=sys.stderr)

    print("-" * 78)
    print("FAITHFUL IIT4 Φ (exact MIP-EI, ALL seeds, ALL arms):")
    phi = {}
    for seed in SEEDS:
        phi[seed] = {}
        for mode in ("none", "central", "multiedge", "shuffle"):
            p = faithful_phi(per_seed[seed][mode]["traj"], f"{mode}_s{seed}")
            phi[seed][mode] = p
        pn, pc, pm, ps = (phi[seed]["none"], phi[seed]["central"],
                          phi[seed]["multiedge"], phi[seed]["shuffle"])
        print(f"  seed {seed}: NONE={pn}  CENTRAL={pc}  MULTI-EDGE={pm}  SHUFFLE={ps}")
        print(f"            ΔΦ(multi-none)={None if (pm is None or pn is None) else round(pm-pn,4)}"
              f"  ΔΦ(central-none)={None if (pc is None or pn is None) else round(pc-pn,4)}"
              f"  ΔΦ(multi-shuffle)={None if (pm is None or ps is None) else round(pm-ps,4)}")

    # ── FROZEN BARS ──────────────────────────────────────────────────────────
    def lift(seed, mode):
        a, b = phi[seed][mode], phi[seed]["none"]
        return None if (a is None or b is None) else (a - b)

    # C1 ROBUST LIFT: multiedge >= none + MARGIN on ALL seeds
    c1_per = {s: (lift(s, "multiedge") is not None and lift(s, "multiedge") >= MARGIN_PHI)
              for s in SEEDS}
    c1 = all(c1_per.values())

    # C2 TOPOLOGY-EARNED: multiedge > shuffle on >=2/3 seeds AND in seed-mean
    c2_per = {s: (phi[s]["multiedge"] is not None and phi[s]["shuffle"] is not None
                  and phi[s]["multiedge"] > phi[s]["shuffle"]) for s in SEEDS}
    mean_m = np.mean([phi[s]["multiedge"] for s in SEEDS])
    mean_s = np.mean([phi[s]["shuffle"] for s in SEEDS])
    c2 = (sum(c2_per.values()) >= 2) and (mean_m > mean_s)

    # C3 BEATS-CENTRAL: multiedge passes C1 (all seeds) AND central FAILS C1 (>=1 seed)
    central_c1_per = {s: (lift(s, "central") is not None and lift(s, "central") >= MARGIN_PHI)
                      for s in SEEDS}
    central_passes_all = all(central_c1_per.values())
    c3 = c1 and (not central_passes_all)

    all_budget_ok = all(per_seed[s]["budget_ok"] for s in SEEDS)

    green = c1 and c2 and c3 and all_budget_ok
    if not all_budget_ok:
        verdict = "INVALID_BUDGET"
    elif green:
        verdict = "GREEN"
    elif c1 and not c2:
        verdict = "PARTIAL_EDGE_COUNT_NOT_TOPOLOGY"
    elif c1 and c2 and not c3:
        verdict = "PARTIAL_BOTH_ROBUST_NO_DISSOCIATION"
    else:
        verdict = "WALL"

    print("=" * 78)
    print(f"BUDGET identity all seeds: {'OK' if all_budget_ok else 'MISMATCH (INVALID)'}")
    print(f"C1 ROBUST LIFT (multi-edge Φ >= none + {MARGIN_PHI} EVERY seed): {'PASS' if c1 else 'FAIL'}")
    for s in SEEDS:
        print(f"     seed {s}: ΔΦ(multi-none)={lift(s,'multiedge')}  {'PASS' if c1_per[s] else 'FAIL'}")
    print(f"C2 TOPOLOGY-EARNED (multi > shuffle, >=2/3 seeds AND mean): {'PASS' if c2 else 'FAIL'}")
    print(f"     per-seed multi>shuffle: { {s: c2_per[s] for s in SEEDS} }  mean_multi={mean_m:.4f} mean_shuffle={mean_s:.4f}")
    print(f"C3 BEATS-CENTRAL (multi passes 3-seed gate, central does NOT): {'PASS' if c3 else 'FAIL'}")
    print(f"     central per-seed passes C1: { {s: central_c1_per[s] for s in SEEDS} }  central_passes_all={central_passes_all}")
    print(f"VERDICT: {verdict}")

    result = {
        "id": "H_1317", "slug": "1317_phi_multiedge", "verdict": verdict,
        "seeds": SEEDS, "N": N, "dim": DIM, "ticks": T,
        "small_world": {"K_lattice": K_LATTICE, "beta": BETA},
        "margin_phi": MARGIN_PHI,
        "phi_faithful_iit4": {str(s): {m: phi[s][m] for m in ("none","central","multiedge","shuffle")}
                              for s in SEEDS},
        "lift_multiedge_minus_none": {str(s): lift(s, "multiedge") for s in SEEDS},
        "lift_central_minus_none": {str(s): lift(s, "central") for s in SEEDS},
        "edge_counts": {str(s): per_seed[s]["edge_counts"] for s in SEEDS},
        "budget_vals": {str(s): per_seed[s]["budget_vals"] for s in SEEDS},
        "budget_ok_all": all_budget_ok,
        "bars": {"C1_robust_lift": bool(c1), "C2_topology_earned": bool(c2), "C3_beats_central": bool(c3)},
        "c1_per_seed": {str(s): bool(c1_per[s]) for s in SEEDS},
        "c2_per_seed": {str(s): bool(c2_per[s]) for s in SEEDS},
        "central_c1_per_seed": {str(s): bool(central_c1_per[s]) for s in SEEDS},
        "mean_multi": float(mean_m), "mean_shuffle": float(mean_s),
        "phi_engine": "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI, n=8)",
    }
    print("\nRESULT_JSON=" + json.dumps(result))
    return result


if __name__ == "__main__":
    main()
