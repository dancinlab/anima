#!/usr/bin/env python3
"""
H_1526 — NEUROMODULATION on the EMIT/SALIENCE gate (abstain_margin), tested on a
CALIBRATION capability. The 10th and LAST live angle on the H_1284 NEUROMODULATION
wall (a_break_the_wall). All 9 prior lenses modulated the plasticity-LR / SPLIT_THRESH
knobs and were INERT — RECALL is decided by cell KEY-GEOMETRY, not the LR schedule.
The ONE knob that is NOT geometry-bound = the abstain_margin (emit/abstain gate): the
abstain DECISION is THRESHOLD-bound, and the OPTIMAL threshold SHIFTS with regime.

CAPABILITY = CALIBRATION (emit-the-right-answer when groundable, abstain when
ungroundable), NOT recall-accuracy. Stream has BOTH groundable + ungroundable queries
in EVERY regime so the abstain gate is the load-bearing decision.

ARMS:  A=best-FIXED margin (grid-tuned on disjoint seed) · ADAPT=substrate-gated
adaptive margin · ABLATE=collapse ADAPT's per-event margin schedule to its OWN MEAN
(fixed). ADAPT−ABLATE decisive ⇒ lift is the substrate-GATING, not the mean.

FROZEN bar in state/verdicts/1526_neuromod_emitgate/H_1526_FREEZE.txt (written first).
p7 exact ground truth, no LLM/perplexity/loss, $0 CPU, 3 seeds. numpy mirror =
DIRECTIONAL (a_engine_native_learning hard-gate-1); engine-native R2 deferred ING.

REUSE: MemStore / key_vec / make_facts geometry is byte-faithful to the H_1284 parent
harness state/universe-probes/h1284_neuromodulation_gain.py (vadapt_field_step mirror).
"""
import numpy as np
import json

DIM = 16
LR0_ENGINE = 0.20
TH0_ENGINE = 0.30


def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


def key_vec(s: str) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (H_1227/H_1231 key)."""
    bs = s.encode()
    v = np.zeros(DIM)
    for i in range(len(bs) - 2):
        idx = fnv1a(bs[i:i + 3]) % DIM
        v[idx] += 1.0
    n = np.linalg.norm(v)
    if n < 1e-9:
        v = np.zeros(DIM); v[fnv1a(bs) % DIM] = 1.0; n = 1.0
    return v / n


class MemStore:
    """VAdaptField numpy mirror + per-cell value bind + LRU eviction (H_1284 parent)."""
    def __init__(self, max_cells, abstain_margin):
        self.protos, self.values, self.lru = [], [], []
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
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick); return
        if err > THRESH and len(self.protos) >= self.max_cells:
            ev = int(np.argmin(self.lru))
            self.protos[ev] = x.copy(); self.values[ev] = value
            self.lru[ev] = self.tick; return
        self.protos[win] = self.protos[win] + LR * (x - self.protos[win])
        self.values[win] = value; self.lru[win] = self.tick

    def recall(self, x):
        """nearest-cell fires; ABSTAIN (None) if recon-err > abstain_margin (H_1227)."""
        self.tick += 1
        win, err, second = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None, err, second
        self.lru[win] = self.tick
        return self.values[win], err, second


def make_facts(n_facts, rng):
    facts = []
    for i in range(n_facts):
        facts.append((f"subj{i:03d}", f"city{rng.integers(0, 9999):04d}"))
    return facts


# ── stream: BOTH groundable + ungroundable in EVERY regime (abstain = load-bearing) ──
OOS_RATE = 0.30


def gen_stream(regime, facts, rng, n_events):
    cur = {s: c for s, c in facts}
    subs = [s for s, _ in facts]
    ev = []
    for s in subs:
        ev.append(('write', s, cur[s], 0.0))
    for t in range(n_events):
        if regime == 'R2_DRIFT' and t % 40 == 0 and t > 0:
            for s in rng.choice(subs, size=max(1, len(subs) // 5), replace=False):
                cur[s] = f"city{rng.integers(0, 9999):04d}"
                ev.append(('write', s, cur[s], 0.0))
        if regime == 'R3_NOISE':
            sig = 0.05 if (t // 25) % 2 == 1 else 0.01
        elif regime == 'R2_DRIFT':
            sig = 0.015
        else:
            sig = 0.01
        if rng.random() < OOS_RATE:
            ev.append(('recall_oos', f"ghost{rng.integers(0, 9999):04d}", None, sig))
        else:
            s = subs[rng.integers(0, len(subs))]
            ev.append(('recall', s, cur[s], sig))
    return ev


# ── neuromodulator on the EMIT GATE ONLY (abstain_margin), gated by substrate surprise ──
class EmitNeuromod:
    """Substrate-gated abstain_margin: raise margin (abstain more) when running
    recall-noise/uncertainty û is high; lower (emit more) when confident. NO LR/SPLIT
    change — the emit gate is the only knob. û = EMA of recon-err (substrate surprise)."""
    KN = 0.9      # NE: abstain-margin gain on (û − û_ref)
    EMA = 0.1
    U_REF = TH0_ENGINE   # reference operating uncertainty (0.30, engine SPLIT_THRESH)

    def __init__(self, margin0):
        self.margin0 = margin0
        self.u = TH0_ENGINE

    def observe(self, surprise):
        self.u = (1 - self.EMA) * self.u + self.EMA * surprise

    def margin(self):
        m = self.margin0 * (1 + self.KN * (self.u - self.U_REF))
        return float(np.clip(m, 0.20, 1.20))


def run_arm(regime, facts, events, rng, margin0, mode, fixed_override=None):
    """mode ∈ {'fixed','adapt','ablate'}.
    'fixed'  : constant margin = margin0 (or fixed_override).
    'adapt'  : per-event substrate-gated margin schedule.
    'ablate' : constant margin = the MEAN of the adapt schedule on THIS stream
               (collapses the gating to its time-average; INERT test).
    Returns (cal, fab, miss, mean_margin)."""
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)), abstain_margin=margin0)
    nm = EmitNeuromod(margin0) if mode in ('adapt', 'ablate') else None

    # ABLATE pre-pass: harvest the adapt margin schedule's mean on an identical run.
    ablate_margin = None
    if mode == 'ablate':
        ablate_margin = _adapt_mean_margin(regime, facts, events, np.random.default_rng(0xC0FFEE), margin0)

    n_recall = n_correct = n_fab = n_miss = 0
    margins_used = []
    for kind, key, val, sig in events:
        x = key_vec(key) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)

        if kind == 'write':
            # writes use the engine-fixed LR/SPLIT (the emit knob does not touch them)
            store.write(x, val, LR0_ENGINE, TH0_ENGINE)
            if mode == 'adapt':
                _, err, _ = store._nearest(x)
                nm.observe(err if err < 1e8 else TH0_ENGINE)
            continue

        # recall event — set the abstain margin per the arm's policy
        if mode == 'fixed':
            store.abstain_margin = fixed_override if fixed_override is not None else margin0
        elif mode == 'ablate':
            store.abstain_margin = ablate_margin
        else:  # adapt
            _, perr, _ = store._nearest(x)
            nm.observe(perr if perr < 1e8 else TH0_ENGINE)
            store.abstain_margin = nm.margin()
        margins_used.append(store.abstain_margin)

        n_recall += 1
        pred, _, _ = store.recall(x)
        if kind == 'recall_oos':
            if pred is not None:        # fabricated on ungroundable
                n_fab += 1
            else:
                n_correct += 1          # correctly abstained
        else:                           # groundable
            if pred == val:
                n_correct += 1          # emitted the right answer
            elif pred is None:
                n_miss += 1             # over-cautious miss
            else:
                n_fab += 1              # confident wrong

    cal = n_correct / max(1, n_recall)
    fab = n_fab / max(1, n_recall)
    miss = n_miss / max(1, n_recall)
    mm = float(np.mean(margins_used)) if margins_used else margin0
    return cal, fab, miss, mm


def _adapt_mean_margin(regime, facts, events, rng, margin0):
    """Run the adapt schedule once to get its time-average margin (for ABLATE)."""
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)), abstain_margin=margin0)
    nm = EmitNeuromod(margin0)
    used = []
    for kind, key, val, sig in events:
        x = key_vec(key) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)
        if kind == 'write':
            store.write(x, val, LR0_ENGINE, TH0_ENGINE)
            _, err, _ = store._nearest(x)
            nm.observe(err if err < 1e8 else TH0_ENGINE)
            continue
        _, perr, _ = store._nearest(x)
        nm.observe(perr if perr < 1e8 else TH0_ENGINE)
        used.append(nm.margin())
    return float(np.mean(used)) if used else margin0


# ── ARM A: best FIXED margin, grid-tuned on a disjoint seed over the 3 regimes ──
MARGIN_GRID = (0.30, 0.40, 0.45, 0.55, 0.65, 0.80)


def grid_tune(n_facts, tune_seed):
    best = None
    for m in MARGIN_GRID:
        cals = []
        for regime in ('R1_STABLE', 'R2_DRIFT', 'R3_NOISE'):
            rng = np.random.default_rng(tune_seed)
            facts = make_facts(n_facts, rng)
            ev = gen_stream(regime, facts, rng, n_events=300)
            cal, _, _, _ = run_arm(regime, facts, ev, np.random.default_rng(tune_seed),
                                   m, mode='fixed', fixed_override=m)
            cals.append(cal)
        mean = float(np.mean(cals))
        if best is None or mean > best[0]:
            best = (mean, m)
    return best[1]


def main():
    N_FACTS = 30
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    REGIMES = ('R1_STABLE', 'R2_DRIFT', 'R3_NOISE')
    MARGIN = 0.05

    m_star = grid_tune(N_FACTS, TUNE_SEED)

    res = {r: {'A': [], 'ADAPT': [], 'ABLATE': [],
               'A_fab': [], 'ADAPT_fab': [], 'A_miss': [], 'ADAPT_miss': [],
               'ADAPT_mm': []} for r in REGIMES}
    for seed in SCORE_SEEDS:
        for regime in REGIMES:
            rng_facts = np.random.default_rng(seed)
            facts = make_facts(N_FACTS, rng_facts)
            ev = gen_stream(regime, facts, rng_facts, n_events=300)
            a_cal, a_fab, a_miss, _ = run_arm(regime, facts, ev,
                np.random.default_rng(seed), m_star, mode='fixed', fixed_override=m_star)
            d_cal, d_fab, d_miss, d_mm = run_arm(regime, facts, ev,
                np.random.default_rng(seed), m_star, mode='adapt')
            l_cal, _, _, _ = run_arm(regime, facts, ev,
                np.random.default_rng(seed), m_star, mode='ablate')
            res[regime]['A'].append(a_cal)
            res[regime]['ADAPT'].append(d_cal)
            res[regime]['ABLATE'].append(l_cal)
            res[regime]['A_fab'].append(a_fab)
            res[regime]['ADAPT_fab'].append(d_fab)
            res[regime]['A_miss'].append(a_miss)
            res[regime]['ADAPT_miss'].append(d_miss)
            res[regime]['ADAPT_mm'].append(d_mm)

    summary = {'m_star': m_star, 'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
               'OOS_RATE': OOS_RATE, 'regimes': {}}
    wins, ablate_decisive = [], []
    for regime in REGIMES:
        A = float(np.mean(res[regime]['A']))
        D = float(np.mean(res[regime]['ADAPT']))
        L = float(np.mean(res[regime]['ABLATE']))
        summary['regimes'][regime] = {
            'A_cal': round(A, 4), 'ADAPT_cal': round(D, 4), 'ABLATE_cal': round(L, 4),
            'ADAPT_minus_A': round(D - A, 4), 'ADAPT_minus_ABLATE': round(D - L, 4),
            'A_fab': round(float(np.mean(res[regime]['A_fab'])), 4),
            'ADAPT_fab': round(float(np.mean(res[regime]['ADAPT_fab'])), 4),
            'A_miss': round(float(np.mean(res[regime]['A_miss'])), 4),
            'ADAPT_miss': round(float(np.mean(res[regime]['ADAPT_miss'])), 4),
            'ADAPT_mean_margin': round(float(np.mean(res[regime]['ADAPT_mm'])), 4),
        }
        if D >= A + MARGIN:
            wins.append(regime)
            if D - L >= MARGIN:
                ablate_decisive.append(regime)

    n_wins = len(wins)
    n_dec = len(ablate_decisive)
    # FROZEN bar: ≥2/3 regimes ADAPT beats best-fixed by ≥MARGIN AND ablation decisive on ≥2 of them
    if n_wins >= 2 and n_dec >= 2:
        verdict = 'GREEN'          # WALL-BROKEN: emit-gate escapes the geometry bottleneck
    else:
        verdict = 'WALL'           # 🧱 wall holds on the emit knob too (DIRECTIONAL)

    summary['wins_over_A+MARGIN'] = wins
    summary['ablate_decisive'] = ablate_decisive
    summary['n_wins'] = n_wins
    summary['n_ablate_decisive'] = n_dec
    summary['verdict'] = verdict
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
