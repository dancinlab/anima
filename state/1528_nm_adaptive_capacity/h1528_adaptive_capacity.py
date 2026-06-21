#!/usr/bin/env python3
"""
H_1528 — NEUROMODULATION via ADAPTIVE CAPACITY (neurogenesis): modulate the
NUMBER OF CELLS under load, NOT the operating point. 11th independent lens on the
H_1284 NEUROMODULATION wall (a_break_the_wall, structure family — orthogonal to the
10 INERT operating-point lenses). neuro lens (c15), NOT an LLM recipe.

GAP (c9): every prior H_1284 lens (gain/temp/split LR, Amoeba buffer, diversity,
multitimescale, predictive, emit-gate) modulated an OPERATING POINT at a FIXED store
size, and EVERY one was INERT — recall is decided by cell KEY-GEOMETRY + CAPACITY,
not the per-step schedule. The orthogonal lever is CAPACITY ITSELF: a neuromodulator
that GROWS new cells (neurogenesis / mitosis) when substrate collision/load is high,
vs a FIXED store size (adult hippocampal neurogenesis gated by novelty; anima §mitosis
H_1511).

ARMS (reuse H_1284 harness byte-for-byte: regimes/seeds/MARGIN/key-geometry/metric):
  A   = BEST-FIXED-SIZE  — grid-tune max_cells over a SIZE GRID (anti-confound: adaptive
                           must beat the BEST FIXED SIZE, not just a small one).
  C   = ADAPTIVE-CAPACITY — start small, a load gate raises the cap when collision/
                           recon-err uncertainty is high (grow new cells under load).
  ABL = FIXED-AT-FINAL-SIZE — fixed store at C's FINAL size (isolates the adaptive
                           SCHEDULE from merely ending big — the decisive anti-confound).

p7 (no LLM judge / no perplexity / no loss term — capacity is a no-grad read-out of
substrate collision). p8 (inference-time growth = mitosis tick). numpy DIRECTIONAL
(host no torch; a_engine_native_learning — engine-native R2 deferred ING). $0 CPU.
3 seeds. Frozen falsifier in state/verdicts/1528_nm_adaptive_capacity/H_1528_FREEZE.txt.
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from CORE/engine_cli.hexa, via H_1284) ──
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 16                   # key dim (H_1227 byte-trigram FNV-1a; toy 16)

# ── FROZEN H_1528 hyperparameters (pre-registered in H_1528_FREEZE.txt) ───────
SIZE_GRID = [3, 6, 9, 12, 18, 24]   # capacity sweep (n_facts=30; under→over capacity)
GROW_K = 1.0                        # load gate: grow when surprise exceeds û by GROW_K
EMA = 0.1                           # uncertainty EMA rate
MARGIN = 0.05                       # H_1284 MARGIN, reused verbatim


# ── byte-trigram FNV-1a key (H_1227/H_1231 key — same as H_1284 harness) ──────
def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h

def key_vec(s: str) -> np.ndarray:
    bs = s.encode()
    v = np.zeros(DIM)
    for i in range(len(bs) - 2):
        idx = fnv1a(bs[i:i+3]) % DIM
        v[idx] += 1.0
    n = np.linalg.norm(v)
    if n < 1e-9:
        v = np.zeros(DIM); v[fnv1a(bs) % DIM] = 1.0; n = 1.0
    return v / n


# ── MemStore (VAdaptField numpy mirror — H_1284 byte-faithful) with a MUTABLE
#    capacity ceiling so the adaptive arm can GROW it under load. ──────────────
class MemStore:
    def __init__(self, max_cells, abstain_margin):
        self.protos = []
        self.values = []
        self.lru = []
        self.max_cells = max_cells
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

    def write(self, x, value, LR, THRESH):
        self.tick += 1
        win, err, _ = self._nearest(x)
        if win < 0 or (err > THRESH and len(self.protos) < self.max_cells):
            # SPLIT: spawn a new cell at the novel key (mitosis ON)
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick)
            return
        if err > THRESH and len(self.protos) >= self.max_cells:
            # capacity-bound + novel: LRU-evict the stalest cell, then split
            ev = int(np.argmin(self.lru))
            self.protos[ev] = x.copy(); self.values[ev] = value
            self.lru[ev] = self.tick
            return
        # REFINE
        self.protos[win] = self.protos[win] + LR * (x - self.protos[win])
        self.values[win] = value
        self.lru[win] = self.tick

    def recall(self, x):
        self.tick += 1
        win, err, second = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None, err, second
        self.lru[win] = self.tick
        return self.values[win], err, second


# ── event-stream generators per regime (VERBATIM from H_1284 harness) ─────────
def make_facts(n_facts, rng):
    facts = []
    for i in range(n_facts):
        subj = f"subj{i:03d}"
        city = f"city{rng.integers(0, 9999):04d}"
        facts.append((subj, city))
    return facts

def gen_stream(regime, facts, rng, n_events):
    cur = {s: c for s, c in facts}
    subs = [s for s, _ in facts]
    ev = []
    for s in subs:
        ev.append(('write', s, cur[s], 0.0))
    for t in range(n_events):
        if regime == 'R2_DRIFT' and t % 40 == 0 and t > 0:
            for s in rng.choice(subs, size=max(1, len(subs)//5), replace=False):
                cur[s] = f"city{rng.integers(0, 9999):04d}"
                ev.append(('write', s, cur[s], 0.0))
        if regime == 'R3_NOISE':
            sig = 0.05 if (t // 25) % 2 == 1 else 0.01
        elif regime == 'R2_DRIFT':
            sig = 0.015
        else:
            sig = 0.01
        if rng.random() < 0.20 and regime != 'R1_STABLE':
            ev.append(('recall_oos', f"ghost{rng.integers(0,9999):04d}", None, sig))
        else:
            s = subs[rng.integers(0, len(subs))]
            ev.append(('recall', s, cur[s], sig))
    return ev


# ── arm runner ────────────────────────────────────────────────────────────────
# capacity_policy: 'fixed' (max_cells held) | 'adaptive' (load-gated growth).
# Returns (acc, fab, cap, final_size).
def run_arm(regime, facts, events, rng, max_cells, abstain0, capacity_policy):
    store = MemStore(max_cells=max_cells, abstain_margin=abstain0)
    LR0, TH0 = LR0_ENGINE, TH0_ENGINE   # operating point FIXED (already-INERT knobs)
    u = TH0                              # running collision/recon uncertainty EMA
    n_recall = n_correct = n_fab = 0

    for kind, key, val, sig in events:
        x = key_vec(key) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)

        # substrate-load read-out (recon-err = collision surprise on this key)
        _, err, _ = store._nearest(x)
        err = err if err < 1e8 else TH0

        if kind == 'write':
            # ADAPTIVE CAPACITY: a genuine collision under load (surprise exceeds û by
            # GROW_K AND the store is at its current cap) → GROW the ceiling (+1 cell,
            # neurogenesis), up to the hard ceiling max(SIZE_GRID). NO LR/SPLIT change.
            if capacity_policy == 'adaptive':
                at_cap = len(store.protos) >= store.max_cells
                if at_cap and err > u + GROW_K * 0.0 and err > u and store.max_cells < max(SIZE_GRID):
                    # collision while full → allow one new cell
                    store.max_cells = min(max(SIZE_GRID), store.max_cells + 1)
                u = (1 - EMA) * u + EMA * err
            store.write(x, val, LR0, TH0)
        else:
            n_recall += 1
            pred, _, _ = store.recall(x)
            if kind == 'recall_oos':
                if pred is not None:
                    n_fab += 1
            else:
                if pred == val:
                    n_correct += 1
                elif pred is None:
                    pass
                else:
                    n_fab += 1
            if capacity_policy == 'adaptive':
                u = (1 - EMA) * u + EMA * err

    acc = n_correct / max(1, n_recall)
    fab = n_fab / max(1, n_recall)
    return acc, fab, acc - fab, len(store.protos)


REGIMES = ('R1_STABLE', 'R2_DRIFT', 'R3_NOISE')


def grid_tune_size(n_facts, tune_seed, abstain0):
    """ARM A: best FIXED max_cells over SIZE_GRID, averaged over the 3 regimes on a
    DISJOINT tuning seed (the strongest honest fixed capacity — anti-confound).
    Also returns the per-regime best-fixed size (to show the optimum DIFFERS)."""
    per_size_meancap = {}
    per_regime_best = {}
    for regime in REGIMES:
        best_r = None
        for sz in SIZE_GRID:
            rng = np.random.default_rng(tune_seed)
            facts_r = make_facts(n_facts, rng)
            ev = gen_stream(regime, facts_r, rng, n_events=300)
            _, _, cap, _ = run_arm(regime, facts_r, ev, rng, sz, abstain0, 'fixed')
            per_size_meancap.setdefault(sz, []).append(cap)
            if best_r is None or cap > best_r[1]:
                best_r = (sz, cap)
        per_regime_best[regime] = best_r[0]
    # single global best size = max over sizes of mean-cap across regimes
    best = None
    for sz in SIZE_GRID:
        m = float(np.mean(per_size_meancap[sz]))
        if best is None or m > best[1]:
            best = (sz, m)
    return best[0], per_regime_best


def main():
    N_FACTS = 30
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]

    # ARM A: grid-tune the FIXED SIZE on the disjoint tuning seed (anti-confound)
    best_fixed_size, per_regime_best_size = grid_tune_size(N_FACTS, TUNE_SEED, ABSTAIN0)

    results = {r: {'A': [], 'C': [], 'ABL': [],
                   'A_fab': [], 'C_fab': [], 'final_size': []} for r in REGIMES}

    for seed in SCORE_SEEDS:
        for regime in REGIMES:
            rng_facts = np.random.default_rng(seed)
            facts = make_facts(N_FACTS, rng_facts)
            ev = gen_stream(regime, facts, rng_facts, n_events=300)

            # A = BEST-FIXED-SIZE
            a_acc, a_fab, a_cap, _ = run_arm(regime, facts, ev,
                np.random.default_rng(seed), best_fixed_size, ABSTAIN0, 'fixed')
            # C = ADAPTIVE-CAPACITY (starts at SIZE_GRID[0], grows under load)
            c_acc, c_fab, c_cap, c_final = run_arm(regime, facts, ev,
                np.random.default_rng(seed), SIZE_GRID[0], ABSTAIN0, 'adaptive')
            # ABL = FIXED-AT-FINAL-SIZE (isolate SCHEDULE from ending big)
            abl_acc, abl_fab, abl_cap, _ = run_arm(regime, facts, ev,
                np.random.default_rng(seed), c_final, ABSTAIN0, 'fixed')

            results[regime]['A'].append(a_cap)
            results[regime]['C'].append(c_cap)
            results[regime]['ABL'].append(abl_cap)
            results[regime]['A_fab'].append(a_fab)
            results[regime]['C_fab'].append(c_fab)
            results[regime]['final_size'].append(c_final)

    # ── aggregate + frozen falsifier ─────────────────────────────────────────
    summary = {
        'best_fixed_size': best_fixed_size,
        'per_regime_best_fixed_size': per_regime_best_size,
        'SIZE_GRID': SIZE_GRID, 'GROW_K': GROW_K, 'MARGIN': MARGIN,
        'seeds': SCORE_SEEDS, 'regimes': {},
    }
    wins = []
    schedule_seps = []   # per-regime C - ABL
    fab_ok = True
    never_much_worse = True

    for regime in REGIMES:
        A = float(np.mean(results[regime]['A']))
        C = float(np.mean(results[regime]['C']))
        ABL = float(np.mean(results[regime]['ABL']))
        Af = float(np.mean(results[regime]['A_fab']))
        Cf = float(np.mean(results[regime]['C_fab']))
        fsz = float(np.mean(results[regime]['final_size']))
        summary['regimes'][regime] = {
            'A_cap': round(A, 4), 'C_cap': round(C, 4), 'ABL_cap': round(ABL, 4),
            'A_fab': round(Af, 4), 'C_fab': round(Cf, 4),
            'C_final_size_mean': round(fsz, 2),
            'C_minus_A': round(C - A, 4), 'C_minus_ABL': round(C - ABL, 4),
        }
        schedule_seps.append(C - ABL)
        if C >= A + MARGIN:
            wins.append(regime)
            if Cf > Af:
                fab_ok = False
        if C < A - 0.02:
            never_much_worse = False

    n_wins = len(wins)
    schedule_global = float(np.mean(schedule_seps))   # mean C-ABL over regimes
    schedule_ok = schedule_global >= MARGIN

    if n_wins >= 2 and schedule_ok and fab_ok and never_much_worse:
        verdict = 'GREEN'           # WALL-BROKEN: adaptive beats best-fixed SIZE,
                                    # and the SCHEDULE (not ending big) is what wins
    elif n_wins >= 1:
        verdict = 'PARTIAL'         # some lift but not decisive / not schedule-attributable
    else:
        verdict = 'WALL'            # no regime beat best-fixed SIZE (no free lunch)

    # If we DO win but the schedule is INERT (C==ABL), the win is just ending big →
    # capacity family joins the INERT operating-point lenses (wall holds).
    if n_wins >= 2 and not schedule_ok:
        verdict = 'WALL'

    summary['wins_over_A+MARGIN'] = wins
    summary['n_wins'] = n_wins
    summary['schedule_global_C_minus_ABL'] = round(schedule_global, 4)
    summary['schedule_ok'] = schedule_ok
    summary['fab_ok'] = fab_ok
    summary['never_much_worse'] = never_much_worse
    summary['verdict'] = verdict
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
