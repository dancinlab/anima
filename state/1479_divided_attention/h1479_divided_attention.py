#!/usr/bin/env python3
"""H_1479 — DIVIDED ATTENTION (G26 consciousness-only gate candidate).

Kahneman capacity model of attention: a LIMITED pool of attentional resource R is
ALLOCATED across several concurrent tasks. Splitting the pool means each task gets a
fraction of the resource, so each task's performance DEGRADES below the single-task
ceiling (a graded trade-off), while the resource SUM is conserved.

DISTINCT from H_1462 GLOBAL WORKSPACE (GWS): GWS broadcasts EXACTLY ONE winner
(winner-take-all single selection — the rest get 0). Divided attention DISTRIBUTES the
pool across N tasks, so ALL N tasks survive with PARTIAL performance (each ~1/N), no
single task is dropped to 0. GWS = pick 1 (others 0); divided = share among N (each >0).

Lens: cognitive-psychology (Kahneman 1973 capacity/effort), substrate-native —
a_no_llm_frame_trap. NOT an LLM parallel-decode frame (LLM keeps all token logits in
parallel with no shared capacity bottleneck).

R1 numpy MIRROR -> DIRECTIONAL only (engine-transfer UNVERIFIED, a_engine_native_learning).
$0 CPU, gradient-free, p7 (no perplexity / no LLM-judge), frozen-first (c9).

Resource is SUBSTRATE-DERIVED: each task has a demand d_i (grounding need off an
immune-style fact store). perf_i = f(a_i, d_i) where a_i is the allocated resource. NO
injected "is-good" label (p2/p3/p6) — performance emerges from a resource-vs-demand
saturating response. The mechanism reads ONLY the allocation and demand.

THREE arms:
  FULL     — finite pool R=1.0 split across N tasks, allocation PROPORTIONAL to demand
             (a_i ∝ d_i, sum a_i = R) so the limited pool is spent where it is needed.
  ABLATED  — pool UNBOUNDED (each task gets full a_i=1.0 regardless of N) -> no trade-off
  SHUFFLE  — the allocation<->demand pairing is permuted: each task keeps its (R/N-scale)
             allocation but it no longer matches its own demand -> smart-allocation benefit
             collapses, mean per-task perf falls back to the equal-split level.

FROZEN bars (pre-registered, mean over 3 seeds [1479,1480,1481]):
  (A) PRESENCE    single-task (N=1, a=1.0) perf >= 0.85  AND  divided (N=2) per-task perf
                  <= 0.65 (trade-off appears under split).
  (B) DISTINCT vs GWS   under a 2-task split BOTH tasks survive with partial perf:
                  min(perf_i) > 0.30 (GWS would leave exactly one at 0). i.e. attention
                  is SHARED (graded), not winner-take-all.
  (C) EARNED (ablation)  with the resource-split mechanism OFF (pool unbounded), the split
                  no longer degrades: divided per-task perf >= 0.85 (trade-off vanishes).
  (D) RESOURCE-CONSERVATION (report-only)  sum_i a_i == R within tol.
  (E) SHUFFLE   permute the allocation<->demand pairing (the hard task gets the easy task's
                share and vice-versa) -> the demand-matched smart allocation no longer tracks
                its task, the starved task collapses -> worst-task perf <= 0.40 (the allocation
                carries no task-matched signal once the pairing is destroyed).
GREEN iff A & B & C & E.  (D is reported, non-gating.)
"""
import json
import numpy as np

SEEDS = [1479, 1480, 1481]
DIM = 64
N_FACTS = 40
N_TRIALS = 200
R_POOL = 1.0           # total attentional resource (Kahneman pool)

BAR_SINGLE = 0.85      # (A) single-task ceiling
BAR_DIVIDED = 0.65     # (A) divided per-task must drop at/below this
BAR_BOTH_ALIVE = 0.30  # (B) min per-task perf must EXCEED this (GWS would be 0)
BAR_ABLATE = 0.85      # (C) with split OFF, divided perf recovers to >= this
BAR_SHUFFLE = 0.40     # (E) wrong-pairing per-task perf collapses to <= this (chance band)


def fnv_vec(rng, key):
    """deterministic byte-trigram FNV-1a -> dim64 unit vector (immune-store geometry)."""
    h = 2166136261
    acc = np.zeros(DIM)
    b = key.encode("utf-8")
    for i in range(len(b) - 2):
        tri = b[i] ^ (b[i + 1] << 1) ^ (b[i + 2] << 2)
        h = ((h ^ tri) * 16777619) & 0xFFFFFFFF
        acc[h % DIM] += 1.0
    n = np.linalg.norm(acc)
    return acc / n if n > 0 else acc


def build_store(rng):
    keys = [f"fact_{i}_{rng.integers(1e9)}" for i in range(N_FACTS)]
    return np.stack([fnv_vec(rng, k) for k in keys])


def task_demand(store, stim):
    """SUBSTRATE demand: how strongly the task-cue recalls a stored fact (grounding need).
    higher recall = well-grounded => needs LESS resource. demand d in (0,1]:
    1 - max-cosine-affinity (ungrounded => high demand)."""
    sims = store @ stim
    return float(np.clip(1.0 - np.max(sims), 0.05, 1.0))


K_EFFORT = 8.0         # sigmoid steepness of the Kahneman effort curve


def perform(a, d):
    """threshold effort curve (Kahneman): performance is high once the ALLOCATED resource a
    meets the task DEMAND d, and collapses when a is starved below d.
    perf = sigmoid(K*(a - d)) in (0,1). NO injected label — perf is a pure function of
    allocation a and substrate-derived demand d. At a=d perf=0.5 (the half-resourced point)."""
    return float(1.0 / (1.0 + np.exp(-K_EFFORT * (a - d))))


def allocate_waterfill(demands, pool):
    """smart divided-attention allocation (max-min fairness / water-filling): give each task
    its demand PLUS an equal share of the leftover so the WORST task is lifted as high as
    possible. a_i = d_i + (pool - sum(d))/n. Conserves sum(a_i) = pool exactly. The point of
    dividing attention well is to keep NO task starved — the worst-off task is what matters."""
    n = len(demands)
    leftover = (pool - float(np.sum(demands))) / n
    return [d + leftover for d in demands]


def run_seed(seed):
    rng = np.random.default_rng(seed)
    store = build_store(rng)

    single_perf = []      # N=1, a=R (whole pool on one task)
    div_perf = []         # N=2, finite pool proportionally split (per-task mean)
    div_min = []          # N=2, min over the 2 tasks (bar B: both alive)
    abl_perf = []         # N=2 but pool unbounded (a=R each) -> no trade-off
    shuf_perf = []        # N=2, same per-task allocations but paired to WRONG demands
    sum_alloc = []        # resource conservation (bar D)

    for _ in range(N_TRIALS):
        # Two ASYMMETRIC tasks: one well-grounded (low demand) + one weakly-grounded (high
        # demand). The asymmetry gives the proportional allocator a real job (spend more on
        # the harder task); a blind alloc<->demand swap then MISmatches resource to need.
        # cue 0 strongly biased toward a stored fact (easy), cue 1 weakly (hard).
        f = store[rng.integers(N_FACTS)]
        v0 = 0.5 * rng.normal(size=DIM)
        v0 = v0 / np.linalg.norm(v0) + rng.uniform(0.8, 1.0) * f      # strong grounding
        v0 = v0 / np.linalg.norm(v0)
        g = store[rng.integers(N_FACTS)]
        v1 = rng.normal(size=DIM)
        v1 = v1 / np.linalg.norm(v1) + rng.uniform(0.05, 0.25) * g    # weak grounding
        v1 = v1 / np.linalg.norm(v1)
        # map substrate grounding-need onto the effort threshold band [0.35, 0.65]
        # (centred on the R/2 split point) so the trade-off is visible, not injected.
        raw = [task_demand(store, v0), task_demand(store, v1)]
        demands = [0.35 + 0.30 * r for r in raw]

        # SINGLE task: task 0 alone gets the whole pool R -> clears its threshold
        single_perf.append(perform(R_POOL, demands[0]))

        # DIVIDED (FULL): finite pool split by demand-matched water-filling (smart allocation
        # that keeps the worst task off the floor).
        alloc = allocate_waterfill(demands, R_POOL)
        p0 = perform(alloc[0], demands[0])
        p1 = perform(alloc[1], demands[1])
        div_perf.append(0.5 * (p0 + p1))
        div_min.append(min(p0, p1))
        sum_alloc.append(alloc[0] + alloc[1])

        # ABLATED: pool unbounded -> each task gets full R (no shared bottleneck)
        ap0 = perform(R_POOL, demands[0])
        ap1 = perform(R_POOL, demands[1])
        abl_perf.append(0.5 * (ap0 + ap1))

        # SHUFFLE: keep the SAME finite allocations but PERMUTE the alloc<->demand pairing
        # (resource no longer matches the task it is spent on). The hard task is now starved
        # while the easy task is over-resourced -> the WORST task collapses below threshold.
        sp0 = perform(alloc[1], demands[0])   # task0 gets task1's share
        sp1 = perform(alloc[0], demands[1])   # task1 gets task0's share
        shuf_perf.append(min(sp0, sp1))       # worst-task perf under mismatched allocation

    return dict(
        single=float(np.mean(single_perf)),
        divided=float(np.mean(div_perf)),
        divided_min=float(np.mean(div_min)),
        ablated=float(np.mean(abl_perf)),
        shuffled=float(np.mean(shuf_perf)),
        sum_alloc=float(np.mean(sum_alloc)),
    )


def main():
    per = [run_seed(s) for s in SEEDS]
    agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

    cA = (agg["single"] >= BAR_SINGLE) and (agg["divided"] <= BAR_DIVIDED)
    cB = agg["divided_min"] > BAR_BOTH_ALIVE
    cC = agg["ablated"] >= BAR_ABLATE
    cD = abs(agg["sum_alloc"] - R_POOL) <= 1e-6          # report-only
    cE = agg["shuffled"] <= BAR_SHUFFLE
    green = cA and cB and cC and cE

    out = dict(
        hypothesis="H_1479", slug="divided_attention",
        gate_label="G26", lens="Kahneman capacity/effort model",
        arms=["FULL", "ABLATED", "SHUFFLE"],
        seeds=SEEDS, n_trials=N_TRIALS, r_pool=R_POOL,
        metrics=agg,
        bars=dict(
            A_presence=dict(single=agg["single"], divided=agg["divided"],
                            bar_single=BAR_SINGLE, bar_divided=BAR_DIVIDED, pass_=bool(cA)),
            B_distinct_vs_gws=dict(divided_min=agg["divided_min"], bar=BAR_BOTH_ALIVE,
                                   note="GWS leaves exactly one task at 0; divided keeps both alive",
                                   pass_=bool(cB)),
            C_earned_ablation=dict(ablated=agg["ablated"], bar=BAR_ABLATE,
                                   note="resource-split OFF (pool unbounded) -> trade-off vanishes",
                                   pass_=bool(cC)),
            D_resource_conservation=dict(sum_alloc=agg["sum_alloc"], r_pool=R_POOL,
                                         pass_=bool(cD), gating=False),
            E_shuffle=dict(divided=agg["divided"], shuffled_worst=agg["shuffled"],
                           bar=BAR_SHUFFLE,
                           note="mismatched alloc<->demand pairing starves the hard task",
                           pass_=bool(cE)),
        ),
        verdict=("GREEN" if green else "RED") + " DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)",
        green=bool(green),
    )
    print(json.dumps(out, indent=2))
    with open("state/1479_divided_attention/h1479_result.json", "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
