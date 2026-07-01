#!/usr/bin/env python3
"""
H_1534 — NEUROMODULATION wall break attempt: C4 CURIOSITY-GATED ACQUISITION.

Census candidate C4 (active-sampling family, orthogonal to the controller /
capacity / geometry / interference / retrieval families that all FAILED H_1284).
Gottlieb & Oudeyer 2018 (Nat Rev Neurosci) — curiosity as info-gain-driven
active sampling. The precondition the 12 prior lenses lacked: a FIXED STORE
BUDGET N < total facts. When the store admits EVERYTHING, selecting WHAT to store
cannot help (that is why prior full-store probes were INERT). Under a budget, a
curiosity gate that ADMITS by novelty and SKIPS near-collinear duplicates frees
slots for DISTINCT facts -> higher recall than random admission at the same budget.

DIRECTIONAL numpy mirror of CORE/engine_cli.hexa VAdaptField (host has no torch;
a_engine_native_learning -> engine-native R2 reconfirm = follow-on ING only if
clean-GREEN). Reuses the H_1284 probe's key geometry VERBATIM (key_vec / fnv1a /
make_facts / split-on-novelty). p7 (exact ground truth, NO LLM judge, NO loss
term — the admit gate is a no-grad read of substrate key novelty). $0 CPU. 3
seeds. Frozen falsifier pre-registered in H_1534_FREEZE.txt (frozen-first, c9).
"""
import os
import sys
import json
import numpy as np

# import the H_1284 probe's key geometry VERBATIM (no re-derivation of the key)
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROBE = os.path.abspath(os.path.join(_HERE, "..", "universe-probes"))
if _PROBE not in sys.path:
    sys.path.insert(0, _PROBE)
from h1284_neuromodulation_gain import key_vec, make_facts, DIM, LR0_ENGINE, TH0_ENGINE

ABSTAIN0 = 0.45          # H_1284 abstain margin (recall ABSTAINs if err > this)
LR0 = LR0_ENGINE         # 0.20 engine winner-pull (refine on duplicate admit)
TH0 = TH0_ENGINE         # 0.30 engine split-thresh (novelty bar for new cell)


# ── capacity-bounded store with EXPLICIT admission gate ───────────────────────
# This is the H_1284 MemStore semantics (split-on-novelty, LRU-evict, abstain),
# but the ADMISSION decision is lifted OUT of write() into the arm controller so
# the curiosity gate can SKIP a fact entirely (the budget lever the prior lacked).
class BudgetStore:
    def __init__(self, budget, abstain_margin):
        self.protos = []
        self.values = []
        self.lru = []
        self.budget = budget          # max cells (the FIXED store budget N)
        self.abstain_margin = abstain_margin
        self.tick = 0

    def _nearest(self, x):
        if not self.protos:
            return -1, 1e9, 1e9
        d = [np.linalg.norm(p - x) for p in self.protos]
        order = np.argsort(d)
        win = int(order[0]); bestd = d[win]
        second = d[int(order[1])] if len(d) > 1 else 1e9
        return win, bestd, second

    def novelty(self, x):
        """recon-err to nearest stored prototype = the curiosity / info-gain
        signal (large => novel/distinct, small => near-collinear duplicate)."""
        _, err, _ = self._nearest(x)
        return err

    def admit(self, x, value):
        """store the fact: refine a near winner, else spawn a cell (LRU-evict
        when at budget). SAME byte semantics as H_1284 write()."""
        self.tick += 1
        win, err, _ = self._nearest(x)
        if win >= 0 and err <= TH0:
            # near an existing cell -> refine winner (online LR), rebind value
            self.protos[win] = self.protos[win] + LR0 * (x - self.protos[win])
            self.values[win] = value
            self.lru[win] = self.tick
            return
        if len(self.protos) < self.budget:
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick)
            return
        # at budget + novel -> LRU-evict stalest, then spawn
        ev = int(np.argmin(self.lru))
        self.protos[ev] = x.copy(); self.values[ev] = value
        self.lru[ev] = self.tick

    def recall(self, x):
        self.tick += 1
        win, err, _ = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None, err
        self.lru[win] = self.tick
        return self.values[win], err


# ── budget-regime event stream: distinct facts + near-collinear duplicates ────
def gen_budget_stream(facts, rng, dup_factor=3):
    """Arrival stream of WRITE events under a budget regime.

    Each subject's fact appears ONCE as a DISTINCT arrival, plus `dup_factor`
    extra near-collinear DUPLICATE arrivals (same key + tiny jitter, redundant:
    rebinds an already-stored fact, carries no new distinct subject). The stream
    is shuffled so duplicates interleave distinct arrivals -> an unselective
    admitter wastes scarce budget slots on duplicates."""
    stream = []
    for (subj, city) in facts:
        stream.append(("distinct", subj, city))
        for _ in range(dup_factor):
            stream.append(("dup", subj, city))
    rng.shuffle(stream)
    return stream


DUP_SIGMA = 0.10         # collinear-dup jitter: L2~0.38 > TH0 0.30 so a dup
                         # SPAWNS its own cell under unselective admission
                         # (wastes a budget slot) — yet stays near its distinct
                         # parent (recall of the subject still finds the cluster).


def materialize(kind, subj, city, rng):
    """key vector for this arrival (duplicates get a collinear jitter that lands
    just BEYOND the refine threshold, so a naive admitter spends a slot on it)."""
    x = key_vec(subj, rng)
    if kind == "dup":
        x = x + rng.normal(0, DUP_SIGMA, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)
    return x


# ── arms ──────────────────────────────────────────────────────────────────────
def run_arm(arm, facts, stream, rng, budget):
    """arm in {'random','curiosity','abl','shuffle'}. Returns (acc, fab)."""
    store = BudgetStore(budget=budget, abstain_margin=ABSTAIN0)
    n = len(stream)

    # RANDOM / ABL: admit a uniform-random subset of arrivals (no regard to
    # novelty -> collinear dups can occupy budget slots). ABL is identical to
    # RANDOM (curiosity OFF must revert).
    if arm in ("random", "abl"):
        keep_idx = set(rng.choice(n, size=min(budget * 4, n),
                                  replace=False).tolist())
        for i, (kind, subj, city) in enumerate(stream):
            if i in keep_idx:
                x = materialize(kind, subj, city, rng)
                store.admit(x, city)
        return _score(store, facts, rng)

    # CURIOSITY: admit iff novelty > adaptive threshold (EMA of seen novelty).
    # SHUFFLE: same gate but the novelty SCORE used for the decision is drawn
    # from a phase-scrambled schedule (decoupled from the fact it scores).
    shuffle = (arm == "shuffle")
    shuf_scores = None
    if shuffle:
        # first pass to harvest the coupled novelty schedule, then scramble it
        tmp = BudgetStore(budget=budget, abstain_margin=ABSTAIN0)
        sched = []
        u = TH0
        for kind, subj, city in stream:
            x = materialize(kind, subj, city, rng)
            nov = tmp.novelty(x)
            nov = nov if nov < 1e8 else u * 2.0
            sched.append(nov)
            u = 0.9 * u + 0.1 * min(nov, 2.0)
            if nov > u:                 # mirror admit policy to fill tmp
                tmp.admit(x, city)
        shuf_scores = [sched[i] for i in rng.permutation(len(sched))]

    u = TH0                            # running expected-novelty (EMA)
    for j, (kind, subj, city) in enumerate(stream):
        x = materialize(kind, subj, city, rng)
        nov_true = store.novelty(x)
        nov_true = nov_true if nov_true < 1e8 else u * 2.0
        nov_decide = shuf_scores[j] if shuffle else nov_true
        admit = nov_decide > u         # curiosity gate: novel beats expectation
        # under-budget store: always admit (bootstrap) — same rule both arms
        if len(store.protos) < min(budget, 2):
            admit = True
        if admit:
            store.admit(x, city)
        # update expected-novelty EMA from the TRUE novelty seen (substrate read)
        u = 0.9 * u + 0.1 * min(nov_true, 2.0)
    return _score(store, facts, rng)


def _score(store, facts, rng):
    """recall every distinct subject (true = its fact) + out-of-store ghosts
    (true = abstain). acc = correct / distinct queries; fab = confident-wrong /
    total queries (abstain is honest, not a fab)."""
    n_q = n_correct = n_fab = 0
    for subj, city in facts:
        x = key_vec(subj, rng)
        pred, _ = store.recall(x)
        n_q += 1
        if pred == city:
            n_correct += 1
        elif pred is not None:
            n_fab += 1
    # ghost (out-of-store) probes: a confident answer = fabrication
    n_ghost = len(facts) // 2
    for g in range(n_ghost):
        x = key_vec(f"ghost{g:04d}", rng)
        pred, _ = store.recall(x)
        if pred is not None:
            n_fab += 1
    acc = n_correct / max(1, n_q)
    fab = n_fab / max(1, n_q + n_ghost)
    return acc, fab


def main():
    N_FACTS = 30
    DUP_FACTOR = 3                     # 3 collinear dups per distinct fact
    BUDGET = 18                        # N < total distinct (30) -> scarce slots
    SEEDS = [11, 22, 33]
    MARGIN = 0.05
    ARMS = ("random", "curiosity", "abl", "shuffle")

    per = {a: {"acc": [], "fab": []} for a in ARMS}
    for seed in SEEDS:
        for arm in ARMS:
            # identical fact set + arrival stream for all arms this seed
            rng_facts = np.random.default_rng(seed)
            facts = make_facts(N_FACTS, rng_facts)
            stream = gen_budget_stream(facts, np.random.default_rng(seed),
                                       dup_factor=DUP_FACTOR)
            acc, fab = run_arm(arm, facts, stream,
                               np.random.default_rng(seed * 100 + 7), BUDGET)
            per[arm]["acc"].append(acc)
            per[arm]["fab"].append(fab)

    m = {a: {"acc": float(np.mean(per[a]["acc"])),
             "fab": float(np.mean(per[a]["fab"]))} for a in ARMS}

    # ── frozen bars (verbatim from H_1534_FREEZE.txt) ─────────────────────────
    cur, ran, abl, shu = m["curiosity"], m["random"], m["abl"], m["shuffle"]

    per_seed_lift = [per["curiosity"]["acc"][i] - per["random"]["acc"][i]
                     for i in range(len(SEEDS))]
    b1_seed_hits = sum(1 for d in per_seed_lift if d >= MARGIN)
    B1 = (cur["acc"] - ran["acc"] >= MARGIN) and (b1_seed_hits >= 2)

    B2 = (cur["acc"] >= abl["acc"] + MARGIN) and (abs(abl["acc"] - ran["acc"]) <= 0.03)
    B3 = (cur["acc"] >= shu["acc"] + MARGIN) and (abs(shu["acc"] - ran["acc"]) <= 0.03)
    B4 = (cur["fab"] - ran["fab"] <= MARGIN)

    broke = B1 and B2 and B3 and B4
    verdict = "GREEN" if broke else "WALL"

    summary = {
        "candidate": "C4 curiosity-gated acquisition (active-sampling)",
        "N_FACTS": N_FACTS, "DUP_FACTOR": DUP_FACTOR, "BUDGET": BUDGET,
        "seeds": SEEDS, "MARGIN": MARGIN,
        "means": {a: {"acc": round(m[a]["acc"], 4), "fab": round(m[a]["fab"], 4)}
                  for a in ARMS},
        "per_seed_acc": {a: [round(v, 4) for v in per[a]["acc"]] for a in ARMS},
        "per_seed_lift_cur_minus_random": [round(d, 4) for d in per_seed_lift],
        "lift_cur_minus_random": round(cur["acc"] - ran["acc"], 4),
        "cur_minus_abl": round(cur["acc"] - abl["acc"], 4),
        "cur_minus_shuffle": round(cur["acc"] - shu["acc"], 4),
        "bars": {"B1_lift": bool(B1), "B1_seed_hits": b1_seed_hits,
                 "B2_earned_abl": bool(B2), "B3_earned_shuffle": bool(B3),
                 "B4_no_fab": bool(B4)},
        "verdict": verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
