#!/usr/bin/env python3
"""
H_1284 — NEUROMODULATION (신경조절) global gain / exploration / plasticity-rate
controller. "missing brain-structure" ladder (neuro lens, c15), NOT an LLM recipe.

GAP (c9): anima's live engine (CORE/engine_cli.hexa adapt_field_step /
vadapt_field_step) runs on FIXED hyperparameters — SPLIT_THRESH=0.30, LR=0.20 —
and a fixed decode temperature. There is NO context-driven neuromodulator that
ADAPTS these by substrate state. This probe is the numpy mirror of VAdaptField
(host has no torch; a_engine_native_learning DIRECTIONAL) with a neuromodulatory
controller mapping substrate state -> (plasticity-rate ACh, split-thresh,
exploration NE, reward-gain DA).

Cross-ref H_1228 (SOC/edge-of-chaos decode, 🟠 PARTIAL): a per-step TEMPERATURE
controller is ONE channel (NE/exploration); helped ideation but was not the full
lever. THIS goes beyond temperature alone — unified neuromodulator on the engine's
real LR / SPLIT_THRESH (mitosis memory), measured as a CAPABILITY across regimes.

p7: exact ground truth, NO LLM judge, NO perplexity, NO loss term (every knob is a
no-grad read-out of substrate state). p8: inference-time plasticity = the engine's
own tick. $0 CPU. ≥3 seeds. Frozen falsifier in H_1284_FREEZE.txt.
"""
import numpy as np
import json, sys

# ── engine-native constants (VERBATIM from CORE/engine_cli.hexa) ──────────────
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 16                   # key dim (H_1227 byte-trigram FNV-1a -> dim64; toy 16)

# ── byte-trigram FNV-1a key (H_1227/H_1231 key, documented discriminating) ────
def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h

def key_vec(s: str, rng) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (discriminating key)."""
    bs = s.encode()
    v = np.zeros(DIM)
    for i in range(len(bs) - 2):
        tri = bs[i:i+3]
        idx = fnv1a(tri) % DIM
        v[idx] += 1.0
    n = np.linalg.norm(v)
    if n < 1e-9:
        # fall back to whole-string hash for very short keys
        v = np.zeros(DIM); v[fnv1a(bs) % DIM] = 1.0; n = 1.0
    return v / n


# ── VAdaptField numpy mirror (byte-faithful to vadapt_field_step) ─────────────
# Plus an external per-cell VALUE binding (H_1231 immune value table keyed by the
# engine's winner index) and LRU eviction for the capacity-bounded store.
class MemStore:
    def __init__(self, max_cells, abstain_margin):
        self.protos = []          # list of DIM vectors (cell prototypes)
        self.values = []          # per-cell bound value (the "fact")
        self.lru = []             # last-use tick per cell (for eviction)
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
        """vadapt_field_step write: split iff recon-err>THRESH & capacity, else
        refine winner by LR. Binds `value` to the winning/new cell."""
        self.tick += 1
        win, err, _ = self._nearest(x)
        if win < 0 or (err > THRESH and len(self.protos) < self.max_cells):
            # SPLIT: spawn a new cell seeded AT the novel key (engine_mitosis_tick ON)
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick)
            return
        if err > THRESH and len(self.protos) >= self.max_cells:
            # capacity-bound + novel: LRU-evict the stalest cell, then split
            ev = int(np.argmin(self.lru))
            self.protos[ev] = x.copy(); self.values[ev] = value
            self.lru[ev] = self.tick
            return
        # REFINE: pull winner toward x (online LR), overwrite its bound value
        self.protos[win] = self.protos[win] + LR * (x - self.protos[win])
        self.values[win] = value
        self.lru[win] = self.tick

    def recall(self, x):
        """nearest-cell fires; ABSTAIN (return None) if recon-err > abstain margin
        (no fabrication, H_1227)."""
        self.tick += 1
        win, err, second = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None, err, second
        self.lru[win] = self.tick
        return self.values[win], err, second


# ── neuromodulator: substrate state -> (LR, THRESH, abstain) ──────────────────
class Neuromod:
    """ACh plasticity + novelty split, NE exploration, DA gain. All knobs are
    no-grad read-outs of substrate state — NOT a loss term (p7)."""
    KA = 1.2     # ACh: unexpected-surprise -> plasticity gain
    KT = 0.8     # split-thresh raise under expected-uncertainty (anti over-split)
    KD = 0.4     # DA reward gain
    KN = 0.6     # NE: abstain widening under expected-uncertainty
    EMA = 0.1    # expected-uncertainty / reward EMA rate

    def __init__(self, LR0, TH0, abstain0):
        self.LR0, self.TH0, self.abstain0 = LR0, TH0, abstain0
        self.u = TH0          # running expected-uncertainty (EMA of surprise)
        self.r = 0.0          # reward EMA

    def observe(self, surprise, reward):
        self.u = (1 - self.EMA) * self.u + self.EMA * surprise
        self.r = (1 - self.EMA) * self.r + self.EMA * reward

    def knobs(self, surprise):
        # ACh plasticity: raise on UNEXPECTED surprise (s>û), calm when s≈û
        LR = self.LR0 * (1 + self.KA * (surprise - self.u))
        LR = float(np.clip(LR, 0.05, 0.60))
        # DA gain: consolidate what works (reward) — scale winner-pull
        LR = float(np.clip(LR * (1 + self.KD * self.r), 0.05, 0.60))
        # ACh/novelty split: RAISE the bar under high expected-uncertainty (noise)
        TH = self.TH0 * (1 + self.KT * (self.u - self.TH0))
        TH = float(np.clip(TH, 0.15, 0.60))
        # NE exploration: widen abstain margin (cautious) under noise
        ab = self.abstain0 * (1 + self.KN * (self.u - self.TH0))
        ab = float(np.clip(ab, 0.20, 1.20))
        return LR, TH, ab


# ── event-stream generators per regime (exact ground truth) ───────────────────
def make_facts(n_facts, rng):
    facts = []
    for i in range(n_facts):
        subj = f"subj{i:03d}"
        city = f"city{rng.integers(0, 9999):04d}"
        facts.append((subj, city))
    return facts

def gen_stream(regime, facts, rng, n_events):
    """yield ('write'|'recall', key_str, true_value, noise_sigma).
    true_value tracks the CURRENT value of each subject (drift rewrites it)."""
    cur = {s: c for s, c in facts}          # current binding
    subs = [s for s, _ in facts]
    ev = []
    # phase 1: write every fact once
    for s in subs:
        ev.append(('write', s, cur[s], 0.0))
    for t in range(n_events):
        if regime == 'R2_DRIFT' and t % 40 == 0 and t > 0:
            # concept drift: rewrite a random subset of facts to NEW values
            for s in rng.choice(subs, size=max(1, len(subs)//5), replace=False):
                cur[s] = f"city{rng.integers(0, 9999):04d}"
                ev.append(('write', s, cur[s], 0.0))
        # noise schedule
        if regime == 'R3_NOISE':
            sig = 0.05 if (t // 25) % 2 == 1 else 0.01
        elif regime == 'R2_DRIFT':
            sig = 0.015
        else:  # R1_STABLE
            sig = 0.01
        # recall a random in-store subject (true = current binding)
        if rng.random() < 0.20 and regime != 'R1_STABLE':
            # out-of-store probe (must ABSTAIN — fabrication test)
            ev.append(('recall_oos', f"ghost{rng.integers(0,9999):04d}", None, sig))
        else:
            s = subs[rng.integers(0, len(subs))]
            ev.append(('recall', s, cur[s], sig))
    return ev


def run_arm(regime, facts, events, rng, LR0, TH0, abstain0, adaptive,
            shuffle_knobs=False):
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)),
                     abstain_margin=abstain0)
    nm = Neuromod(LR0, TH0, abstain0) if adaptive else None
    n_recall = n_correct = n_fab = 0
    knob_log = []   # (LR, TH, ab) per write/recall for shuffle control
    # optional pre-computed shuffled knob schedule
    shuf = None
    if shuffle_knobs:
        # first pass to harvest the coupled schedule, then phase-scramble it
        tmp_store = MemStore(max_cells=store.max_cells, abstain_margin=abstain0)
        tmp_nm = Neuromod(LR0, TH0, abstain0)
        sched = []
        for kind, key, val, sig in events:
            x = key_vec(key, rng) + rng.normal(0, sig, DIM)
            x = x / (np.linalg.norm(x) + 1e-9)
            _, err, _ = tmp_store._nearest(x)
            err = err if err < 1e8 else tmp_nm.TH0
            LR, TH, ab = tmp_nm.knobs(err)
            sched.append((LR, TH, ab))
            tmp_nm.observe(err, 0.0)
            if kind.startswith('write') or kind == 'write':
                tmp_store.write(x, val, LR, TH)
        idx = rng.permutation(len(sched))   # phase-scramble (destroy coupling)
        shuf = [sched[i] for i in idx]

    si = 0
    for kind, key, val, sig in events:
        x = key_vec(key, rng) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)
        if adaptive:
            _, err, _ = store._nearest(x)
            err = err if err < 1e8 else nm.TH0
            if shuffle_knobs:
                LR, TH, ab = shuf[si]; si += 1
            else:
                LR, TH, ab = nm.knobs(err)
            store.abstain_margin = ab
        else:
            LR, TH = LR0, TH0
            store.abstain_margin = abstain0
            err = 0.0

        if kind == 'write':
            store.write(x, val, LR, TH)
            if adaptive and not shuffle_knobs:
                nm.observe(err, 0.0)
        else:  # recall or recall_oos
            n_recall += 1
            pred, rerr, _ = store.recall(x)
            if kind == 'recall_oos':
                # truth = abstain; a confident answer = fabrication
                if pred is not None:
                    n_fab += 1
                reward = 1.0 if pred is None else 0.0
            else:
                if pred == val:
                    n_correct += 1; reward = 1.0
                elif pred is None:
                    reward = 0.0        # honest abstain, not fabrication
                else:
                    n_fab += 1; reward = 0.0   # confident WRONG = fabrication
            if adaptive and not shuffle_knobs:
                nm.observe(rerr if rerr < 1e8 else nm.TH0, reward)

    acc = n_correct / max(1, n_recall)
    fab = n_fab / max(1, n_recall)
    return acc, fab, acc - fab


def grid_tune(facts, rng_seed):
    """ARM A: find the BEST fixed (LR0, TH0) on a DISJOINT tuning seed, averaged
    over the 3 regimes (a single global operating point — strongest honest fixed)."""
    best = None
    for LR0 in (0.1, 0.2, 0.3, 0.4):
        for TH0 in (0.2, 0.3, 0.4):
            caps = []
            for regime in ('R1_STABLE', 'R2_DRIFT', 'R3_NOISE'):
                rng = np.random.default_rng(rng_seed)
                facts_r = make_facts(len(facts), rng)
                ev = gen_stream(regime, facts_r, rng, n_events=300)
                _, _, cap = run_arm(regime, facts_r, ev, rng, LR0, TH0,
                                    abstain0=0.45, adaptive=False)
                caps.append(cap)
            m = float(np.mean(caps))
            if best is None or m > best[0]:
                best = (m, LR0, TH0)
    return best[1], best[2]


def main():
    N_FACTS = 30
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    REGIMES = ('R1_STABLE', 'R2_DRIFT', 'R3_NOISE')

    # ARM A tuning (disjoint seed)
    tune_rng = np.random.default_rng(TUNE_SEED)
    tune_facts = make_facts(N_FACTS, tune_rng)
    LR0_star, TH0_star = grid_tune(tune_facts, TUNE_SEED)

    results = {r: {'A': [], 'B': [], 'CSHUF': [],
                   'A_fab': [], 'B_fab': [], 'CSHUF_fab': []} for r in REGIMES}
    for seed in SCORE_SEEDS:
        for regime in REGIMES:
            # identical fact set + event stream for A/B/C this (seed,regime)
            rng_facts = np.random.default_rng(seed)
            facts = make_facts(N_FACTS, rng_facts)
            ev = gen_stream(regime, facts, rng_facts, n_events=300)
            # A FIXED
            a_acc, a_fab, a_cap = run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                adaptive=False)
            # B NEUROMOD
            b_acc, b_fab, b_cap = run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                adaptive=True)
            # C-SHUF (phase-scrambled knob schedule)
            c_acc, c_fab, c_cap = run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                adaptive=True, shuffle_knobs=True)
            results[regime]['A'].append(a_cap)
            results[regime]['B'].append(b_cap)
            results[regime]['CSHUF'].append(c_cap)
            results[regime]['A_fab'].append(a_fab)
            results[regime]['B_fab'].append(b_fab)
            results[regime]['CSHUF_fab'].append(c_fab)

    # ── aggregate + frozen falsifier ─────────────────────────────────────────
    MARGIN = 0.05
    summary = {'LR0_star': LR0_star, 'TH0_star': TH0_star, 'regimes': {}}
    wins = []          # regimes where B beats A+MARGIN
    coupling_ok = []   # regimes where C-SHUF separated below B-MARGIN
    fab_ok = True
    never_much_worse = True
    for regime in REGIMES:
        A = float(np.mean(results[regime]['A']))
        B = float(np.mean(results[regime]['B']))
        C = float(np.mean(results[regime]['CSHUF']))
        Af = float(np.mean(results[regime]['A_fab']))
        Bf = float(np.mean(results[regime]['B_fab']))
        summary['regimes'][regime] = {
            'A_cap': round(A, 4), 'B_cap': round(B, 4), 'CSHUF_cap': round(C, 4),
            'A_fab': round(Af, 4), 'B_fab': round(Bf, 4),
            'B_minus_A': round(B - A, 4), 'B_minus_CSHUF': round(B - C, 4),
        }
        beats = B >= A + MARGIN
        if beats:
            wins.append(regime)
            if Bf > Af:
                fab_ok = False
            if C < B - MARGIN:
                coupling_ok.append(regime)
        else:
            if B < A - 0.02:
                never_much_worse = False

    n_wins = len(wins)
    n_coupled = len(coupling_ok)
    if n_wins >= 2 and fab_ok and never_much_worse and n_coupled >= 2:
        verdict = 'GREEN'
    elif n_wins >= 1:
        if n_wins >= 2 and n_coupled < 2:
            verdict = 'PARTIAL'   # lift not coupling-attributable
        else:
            verdict = 'PARTIAL'   # single operating point / no-free-lunch beyond 1
    else:
        verdict = 'RED'           # no regime beat best-fixed (no free lunch)

    summary['wins_over_A+MARGIN'] = wins
    summary['coupling_separated'] = coupling_ok
    summary['fab_ok'] = fab_ok
    summary['never_much_worse'] = never_much_worse
    summary['MARGIN'] = MARGIN
    summary['seeds'] = SCORE_SEEDS
    summary['verdict'] = verdict
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
