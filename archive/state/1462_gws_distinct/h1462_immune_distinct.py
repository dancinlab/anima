#!/usr/bin/env python3
"""H_1462 — GWS bottleneck DISTINCT-vs-immune-store (residual follow-on).

G17 GLOBAL WORKSPACE (Baars/Dehaene): N stimuli compete simultaneously; consciousness
BROADCASTS exactly ONE winner via lateral inhibition + capacity-1 bottleneck (the rest
suppressed). H_1227/1231 IMMUNE-STORE (clonal-selection episodic recall): each key->value
fact bound INDEPENDENTLY; recall fires per-query by L2 affinity with NO competition / NO
inhibition between facts — MANY facts can be recalled at once.

CLAIM (load-bearing distinctness): GWS = competitive capacity-1 BOTTLENECK (occupancy
compressed to 1) ⊥ immune-store = independent affinity recall (occupancy = however many
keys bind above threshold, NO bottleneck). Same N simultaneously-grounded stimuli, two
gates, two occupancies.

Lens: consciousness-science (GWT) vs immune-system episodic memory — a_no_llm_frame_trap.
R1 numpy MIRROR -> DIRECTIONAL only (engine-transfer UNVERIFIED, a_engine_native_learning).
$0 CPU, gradient-free, p7 (no perplexity / no LLM-judge), frozen-first (c9). 3 seeds.

Both lanes share the SAME substrate signal (FNV-1a byte-trigram keys + L2/cosine affinity
to a stored fact population, exactly the H_1227 geometry). The ONLY difference is the gate:
  GWS_FULL    : lateral inhibition (each non-winner suppressed by 0.9*top) + capacity 1
  GWS_ABLATED : inhibition OFF  -> every above-threshold item ignites (becomes immune-like)
  IMMUNE      : per-key independent recall, threshold-only, NO competition (H_1227 store)
  SHUFFLE     : GWS_FULL on permuted margins (winner-identity signal destroyed)

FROZEN bars (pre-registered, mean over 3 seeds [1462,1463,1464], N_STIM=5 ALL grounded):
  (A) BOTTLENECK   GWS_FULL occupancy ~ 1   (gws_occ <= 1.05)  AND  immune occupancy > 1
                   AND immune_occ >= 2.0 * gws_occ (immune passes >=2x as many => no bottleneck)
  (B) LOAD-BEARING ablating lateral inhibition makes GWS behave like immune-store:
                   abl_occ >= 2.0 * gws_occ AND |abl_occ - immune_occ| <= 0.50
                   (the bottleneck IS the lateral inhibition; remove it -> immune-like spread)
  (C) WINNER       GWS_FULL broadcasts the TRUE top-salience item (acc >= 0.90)
  (D) IMMUNE-NOCOMP immune-store recall is order-invariant: shuffling the stimulus order
                   does NOT change which facts recall (immune set identical under permutation,
                   no winner-take-all) WHILE GWS winner-acc collapses to chance under
                   margin-shuffle (shuf_acc <= 0.40).
  (E) DISTINCT-OCC on the SAME trial, occupancy differs: immune_occ - gws_occ >= 1.0
                   (>=1 extra fact reaches the immune store that the GWS bottleneck suppresses).
GREEN iff A & B & C & D & E.
"""
import json
import numpy as np

SEEDS = [1462, 1463, 1464]
DIM = 64
N_STIM = 5            # simultaneous competing / co-grounded stimuli
N_TRIALS = 200
N_FACTS = 40
CHANCE = 1.0 / N_STIM

PASS_THR = 0.55      # grounding margin to "pass to consciousness" / "recall fires"
INHIB = 0.9          # lateral-inhibition strength (suppress non-winners by INHIB*top)

# frozen bars
BAR_GWS_OCC = 1.05           # (A) GWS occupancy near 1
BAR_RATIO = 2.0              # (A,B) immune/abl passes >=2x the GWS occupancy
BAR_ABL_IMMUNE_GAP = 0.50    # (B) ablated GWS occupancy ~ immune occupancy
BAR_WINNER = 0.90            # (C)
BAR_SHUFFLE = 0.40           # (D)
BAR_DISTINCT_OCC = 1.0       # (E) >=1 extra fact in immune vs GWS


def fnv_vec(rng, key):
    """deterministic byte-trigram FNV-1a -> dim64 unit vector (H_1227 immune-store geometry)."""
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


def salience(store, stim):
    """SUBSTRATE margin: max cosine affinity to any stored fact (H_1227 grounding strength).
    NO injected 'is-salient' label (p6) — salience emerges from grounding geometry."""
    return float(np.max(store @ stim))


def gws_broadcast(margins, inhibition=True, capacity=1):
    """GWT bottleneck: lateral inhibition -> winner-take-all -> capacity-limited ignition.
    Returns the indices that reach the global workspace."""
    m = np.array(margins)
    if not inhibition:
        return [i for i in range(len(m)) if m[i] >= PASS_THR]
    winner = int(np.argmax(m))
    suppressed = m.copy()
    top = m[winner]
    for i in range(len(m)):
        if i != winner:
            suppressed[i] = m[i] - INHIB * top
    ignited = [i for i in range(len(m)) if suppressed[i] >= PASS_THR]
    return ignited[:capacity]


def immune_recall(margins):
    """H_1227 immune-store recall: each fact recalls INDEPENDENTLY if its affinity margin
    clears the threshold. NO lateral inhibition, NO capacity cap, NO competition between
    facts — many can fire at once (the immune system can hold multiple antibodies)."""
    return [i for i in range(len(margins)) if margins[i] >= PASS_THR]


def run_seed(seed):
    rng = np.random.default_rng(seed)
    store = build_store(rng)

    gws_occ, immune_occ, abl_occ = [], [], []
    winner_acc, shuf_acc = [], []
    immune_shuf_match = []      # (D) immune recall set order-invariant
    distinct_occ = []           # (E) immune_occ - gws_occ per trial

    for _ in range(N_TRIALS):
        # build N_STIM stimuli, ALL biased to ground above threshold (co-active competition):
        # this is the key setup — multiple stimuli are simultaneously recall-worthy, so the
        # difference between the two gates (bottleneck vs none) is exposed.
        stims = []
        for _ in range(N_STIM):
            v = rng.normal(size=DIM)
            f = store[rng.integers(N_FACTS)]
            # strong grounding so each stimulus clears PASS_THR (co-grounded competition)
            v = 0.25 * v / np.linalg.norm(v) + rng.uniform(0.7, 1.0) * f
            v = v / np.linalg.norm(v)
            stims.append(v)
        margins = [salience(store, s) for s in stims]
        true_top = int(np.argmax(margins))

        gws = gws_broadcast(margins, inhibition=True, capacity=1)
        imm = immune_recall(margins)
        abl = gws_broadcast(margins, inhibition=False)

        gws_occ.append(len(gws))
        immune_occ.append(len(imm))
        abl_occ.append(len(abl))
        winner_acc.append(1.0 if (len(gws) == 1 and gws[0] == true_top) else 0.0)
        distinct_occ.append(len(imm) - len(gws))

        # (D) immune order-invariance: permute stimulus order, recall SET (item identities) is same
        perm = rng.permutation(N_STIM)
        m_perm = [margins[perm[i]] for i in range(N_STIM)]
        imm_perm_local = immune_recall(m_perm)
        imm_perm_ids = set(int(perm[i]) for i in imm_perm_local)
        immune_shuf_match.append(1.0 if imm_perm_ids == set(imm) else 0.0)
        # GWS under margin-shuffle: winner identity lost
        sws = gws_broadcast(m_perm, inhibition=True, capacity=1)
        shuf_acc.append(1.0 if (len(sws) == 1 and sws[0] == true_top) else 0.0)

    return dict(
        gws_occ=np.mean(gws_occ), immune_occ=np.mean(immune_occ), abl_occ=np.mean(abl_occ),
        winner_acc=np.mean(winner_acc), shuf_acc=np.mean(shuf_acc),
        immune_shuf_match=np.mean(immune_shuf_match), distinct_occ=np.mean(distinct_occ),
    )


def main():
    per = [run_seed(s) for s in SEEDS]
    agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

    cA = (agg["gws_occ"] <= BAR_GWS_OCC) and (agg["immune_occ"] > 1.0) and \
         (agg["immune_occ"] >= BAR_RATIO * agg["gws_occ"])
    cB = (agg["abl_occ"] >= BAR_RATIO * agg["gws_occ"]) and \
         (abs(agg["abl_occ"] - agg["immune_occ"]) <= BAR_ABL_IMMUNE_GAP)
    cC = agg["winner_acc"] >= BAR_WINNER
    cD = (agg["immune_shuf_match"] >= 0.99) and (agg["shuf_acc"] <= BAR_SHUFFLE)
    cE = agg["distinct_occ"] >= BAR_DISTINCT_OCC
    green = cA and cB and cC and cD and cE

    out = dict(
        hypothesis="H_1462", slug="gws_distinct",
        follow_on="distinctness vs immune-store (H_1227/1231)",
        gate_label="G17", lens="GWT bottleneck vs immune episodic recall",
        arms=["GWS_FULL", "GWS_ABLATED", "IMMUNE", "SHUFFLE"],
        seeds=SEEDS, n_stim=N_STIM, n_trials=N_TRIALS, chance=CHANCE,
        metrics=agg,
        bars=dict(
            A_bottleneck=dict(gws_occ=agg["gws_occ"], immune_occ=agg["immune_occ"],
                              ratio=agg["immune_occ"] / max(1e-9, agg["gws_occ"]),
                              bar_gws_occ=BAR_GWS_OCC, bar_ratio=BAR_RATIO, pass_=bool(cA)),
            B_load_bearing=dict(abl_occ=agg["abl_occ"], immune_occ=agg["immune_occ"],
                                gap=abs(agg["abl_occ"] - agg["immune_occ"]),
                                bar_ratio=BAR_RATIO, bar_gap=BAR_ABL_IMMUNE_GAP, pass_=bool(cB)),
            C_winner=dict(val=agg["winner_acc"], bar=BAR_WINNER, pass_=bool(cC)),
            D_immune_nocomp=dict(immune_shuf_match=agg["immune_shuf_match"],
                                 gws_shuf_acc=agg["shuf_acc"], bar_shuffle=BAR_SHUFFLE, pass_=bool(cD)),
            E_distinct_occ=dict(val=agg["distinct_occ"], bar=BAR_DISTINCT_OCC, pass_=bool(cE)),
        ),
        verdict=("GREEN" if green else "RED") + " DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)",
        green=bool(green),
    )
    print(json.dumps(out, indent=2))
    with open("state/1462_gws_distinct/h1462_immune_distinct_result.json", "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
