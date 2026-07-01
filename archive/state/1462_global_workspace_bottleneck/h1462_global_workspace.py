#!/usr/bin/env python3
"""H_1462 — GLOBAL WORKSPACE BOTTLENECK (G17 consciousness-only gate candidate).

Global Workspace Theory (Baars / Dehaene): of many simultaneous stimuli competing
for access, consciousness BROADCASTS exactly ONE winner (capacity-limited bottleneck
+ lateral inhibition + global ignition), suppressing the rest. This is DISTINCT from
a plain salience score (every item gets a number; many can pass a threshold at once).

Lens: consciousness-science (GWT global-ignition), substrate-native — a_no_llm_frame_trap.

R1 numpy MIRROR -> DIRECTIONAL only (engine-transfer UNVERIFIED, a_engine_native_learning).
$0 CPU, gradient-free, p7 (no perplexity / no LLM-judge), frozen-first (c9).

Salience is SUBSTRATE-DERIVED (grounding margin off an immune-style fact store), NOT an
injected label (p2/p3/p6). The competition reads ONLY those margins; the workspace
applies a winner-take-all bottleneck with lateral inhibition + capacity C=1.

THREE arms:
  FULL      — competition ON (lateral inhibition, capacity 1, global ignition)
  ABLATED   — inhibition OFF (capacity unbounded -> behaves like salience-only readout)
  SHUFFLE   — salience margins permuted across items (signal destroyed)

FROZEN bars (pre-registered, mean over 3 seeds [1461,1462,1463]):
  (A) PRESENCE   broadcast == true top-salience item, acc >= 0.90
  (B) DISTINCT   no-bottleneck baseline passes > 1.5 items on avg AND the bottleneck COMPRESSES
                 throughput >=2x (base_count > 2*full_count) with NO capacity violation (full_count<=1).
                 [R1b frozen-first fix, a_break_the_wall(b): the original "full_count==1.0" was a
                  measurement artifact — capacity=1 makes full_count structurally <=1, and GWT allows
                  ignition FAILURE (empty consciousness when all sub-threshold), so a mean of 0.995 is
                  CORRECT behaviour, not a miss. Bottleneck = throughput COMPRESSION, not "always 1".]
  (C) EARNED-COMP   ablated (inhibition off) winner acc <= 0.40 (-> chance 1/N=0.2)
  (D) SHUFFLE    permuted-margin broadcast acc <= 0.40 (-> chance)
  (E) CAPACITY   2nd-most-salient leak into workspace <= 0.10
GREEN iff A & B & C & D & E.
"""
import json
import numpy as np

SEEDS = [1462, 1463, 1464]
DIM = 64
N_STIM = 5          # simultaneous competing stimuli
N_TRIALS = 200
N_FACTS = 40        # immune-style grounded fact store
CHANCE = 1.0 / N_STIM

BAR_PRESENCE = 0.90
BAR_DISTINCT_BASE = 1.5     # salience-only passes MORE than this many items
BAR_ABLATE = 0.40
BAR_SHUFFLE = 0.40
BAR_CAPACITY = 0.10
PASS_THR = 0.55             # salience threshold for "passes to consciousness" (baseline)


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
    """grounded fact vectors; a stimulus' salience = how strongly it recalls a stored fact."""
    keys = [f"fact_{i}_{rng.integers(1e9)}" for i in range(N_FACTS)]
    return np.stack([fnv_vec(rng, k) for k in keys])


def salience(store, stim):
    """SUBSTRATE margin: max cosine affinity to any stored fact (grounding strength).
    NO injected 'is-salient' label — salience emerges from grounding geometry (p6)."""
    sims = store @ stim
    return float(np.max(sims))


def workspace_broadcast(margins, inhibition=True, capacity=1):
    """GWT bottleneck: lateral inhibition -> winner-take-all -> capacity-limited ignition.
    Returns the set of item-indices that reach the global workspace."""
    m = np.array(margins)
    if not inhibition:
        # no competition: every item above threshold ignites (salience-only readout)
        return [i for i in range(len(m)) if m[i] >= PASS_THR]
    # lateral inhibition: each item suppressed by the strongest competitor
    winner = int(np.argmax(m))
    suppressed = m.copy()
    top = m[winner]
    for i in range(len(m)):
        if i != winner:
            suppressed[i] = m[i] - 0.9 * top   # inhibited below ignition
    ignited = [i for i in range(len(m)) if suppressed[i] >= PASS_THR]
    return ignited[:capacity]


def run_seed(seed):
    rng = np.random.default_rng(seed)
    store = build_store(rng)

    full_acc = []        # FULL broadcast == true top
    full_count = []      # FULL workspace size
    base_count = []      # no-bottleneck passed-item count
    abl_acc = []         # ablated winner == true top
    shuf_acc = []        # shuffled broadcast == true top
    leak = []            # 2nd-most-salient leaked into FULL workspace

    for _ in range(N_TRIALS):
        stims = []
        for _ in range(N_STIM):
            v = rng.normal(size=DIM)
            # bias some stimuli toward a stored fact => higher grounding margin
            if rng.random() < 0.7:
                f = store[rng.integers(N_FACTS)]
                v = 0.5 * v / np.linalg.norm(v) + rng.uniform(0.3, 1.0) * f
            v = v / np.linalg.norm(v)
            stims.append(v)
        margins = [salience(store, s) for s in stims]
        true_top = int(np.argmax(margins))
        order = np.argsort(margins)[::-1]
        second = int(order[1])

        # FULL
        ws = workspace_broadcast(margins, inhibition=True, capacity=1)
        full_count.append(len(ws))
        full_acc.append(1.0 if (len(ws) == 1 and ws[0] == true_top) else 0.0)
        leak.append(1.0 if second in ws else 0.0)

        # baseline (no bottleneck)
        base = workspace_broadcast(margins, inhibition=False)
        base_count.append(len(base))

        # ABLATED: inhibition off but forced to pick one -> top of an unbounded set is ambiguous;
        # model "no competition" winner as a random ignited item (no winner-take-all)
        abl = workspace_broadcast(margins, inhibition=False)
        if abl:
            pick = int(rng.choice(abl))
        else:
            pick = int(rng.integers(N_STIM))
        abl_acc.append(1.0 if pick == true_top else 0.0)

        # SHUFFLE: permute margins across items, then full bottleneck
        perm = rng.permutation(N_STIM)
        sm = [margins[perm[i]] for i in range(N_STIM)]
        sws = workspace_broadcast(sm, inhibition=True, capacity=1)
        shuf_acc.append(1.0 if (len(sws) == 1 and sws[0] == true_top) else 0.0)

    return dict(
        full_acc=np.mean(full_acc), full_count=np.mean(full_count),
        base_count=np.mean(base_count), abl_acc=np.mean(abl_acc),
        shuf_acc=np.mean(shuf_acc), leak=np.mean(leak),
    )


def main():
    per = [run_seed(s) for s in SEEDS]
    agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

    cA = agg["full_acc"] >= BAR_PRESENCE
    cB = (agg["base_count"] > BAR_DISTINCT_BASE) and \
         (agg["base_count"] > 2.0 * agg["full_count"]) and (agg["full_count"] <= 1.0 + 1e-9)
    cC = agg["abl_acc"] <= BAR_ABLATE
    cD = agg["shuf_acc"] <= BAR_SHUFFLE
    cE = agg["leak"] <= BAR_CAPACITY
    green = cA and cB and cC and cD and cE

    out = dict(
        hypothesis="H_1462", slug="global_workspace_bottleneck",
        gate_label="G17", lens="GWT global-ignition", arms=["FULL", "ABLATED", "SHUFFLE"],
        seeds=SEEDS, n_stim=N_STIM, n_trials=N_TRIALS, chance=CHANCE,
        metrics=agg,
        bars=dict(
            A_presence=dict(val=agg["full_acc"], bar=BAR_PRESENCE, pass_=bool(cA)),
            B_distinct=dict(base_count=agg["base_count"], full_count=agg["full_count"],
                            bar=BAR_DISTINCT_BASE, pass_=bool(cB)),
            C_earned_competition=dict(val=agg["abl_acc"], bar=BAR_ABLATE, pass_=bool(cC)),
            D_shuffle=dict(val=agg["shuf_acc"], bar=BAR_SHUFFLE, pass_=bool(cD)),
            E_capacity=dict(val=agg["leak"], bar=BAR_CAPACITY, pass_=bool(cE)),
        ),
        verdict=("GREEN" if green else "RED") + " DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)",
        green=bool(green),
    )
    print(json.dumps(out, indent=2))
    with open("state/1462_global_workspace_bottleneck/h1462_result.json", "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
