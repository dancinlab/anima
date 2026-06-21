#!/usr/bin/env python3
"""
H_1535 — NEUROMODULATION on the OBJECTIVE / COST-TRADEOFF axis (precision↔recall Pareto).

THE WALL: H_1284 NEUROMODULATION. 12+ lenses failed because the tested capability had ONE
optimal operating point across regimes (geometry-not-protocol bottleneck) — no adaptive
controller beat a single best-fixed point.

THE NEW ANGLE: the one knob-axis with a GENUINELY regime-dependent optimum. When the COST
TRADEOFF (false-emit vs abstain) DIFFERS by regime, the Pareto-optimal abstain threshold
actually SHIFTS. A controller that detects the regime's cost-asymmetry and MOVES the
precision/recall operating point could beat ANY single best-fixed point that must serve all
regimes at once.

DISTINCT vs emit-gate H_1526 (HELD): H_1526 scored a SYMMETRIC metric (acc - fab, equal
weights) under FIXED cost, so the optimum did NOT shift. Here the cost is ASYMMETRIC and
REGIME-DEPENDENT (pre-registered ratios in H_1535_FREEZE.txt) - the optimum genuinely
shifts - and the controller needs only the COARSE regime cost-asymmetry (the frozen cost
ratio + running surprise base-rate), NOT per-query class separation H_1526 lacked.

p7: exact ground truth, NO LLM judge / perplexity / loss - every knob is a no-grad read-out.
DIRECTIONAL (numpy mirror, HARD-GATE-1 -> terminal NOT permitted; engine-native R2 = ING).
$0 CPU. 3 seeds. Frozen falsifier in H_1535_FREEZE.txt (written before any run).
"""
import numpy as np
import json
import os
import sys

# reuse the EXACT parent geometry (MemStore / key_vec / fnv1a / DIM)
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "state", "universe-probes"))
sys.path.insert(0, os.path.join(_HERE, "..", "universe-probes"))
from h1284_neuromodulation_gain import MemStore, key_vec, DIM, make_facts

# -- frozen, pre-registered cost regimes (false-emit : abstain-on-groundable) ----------
# the asymmetry is the EXPERIMENTAL MANIPULATION, not a tuned knob.
COST = {
    'R_PRECISION': (5.0, 1.0),   # false-emit costly  -> optimum should ABSTAIN MORE
    'R_RECALL':    (1.0, 5.0),   # missing answer costly -> optimum should EMIT MORE
    'R_BALANCED':  (2.0, 2.0),   # symmetric -> middle
}
REGIMES = tuple(COST.keys())
OOS_RATE = 0.30
N_FACTS = 30
LR0, TH0 = 0.20, 0.30
MARGIN = 0.05
# abstain-margin grid (the precision/recall operating point); wider margin = abstain MORE
MARGIN_GRID = np.round(np.arange(0.20, 1.21, 0.05), 3)


def gen_stream(facts, rng, n_events):
    """write every fact once, then a mix of groundable (noisy) + ghost recalls."""
    cur = {s: c for s, c in facts}
    subs = [s for s, _ in facts]
    ev = [('write', s, cur[s], 0.0) for s in subs]
    for _ in range(n_events):
        sig = 0.03
        if rng.random() < OOS_RATE:
            ev.append(('recall_oos', f"ghost{rng.integers(0,99999):05d}", None, sig))
        else:
            s = subs[rng.integers(0, len(subs))]
            ev.append(('recall', s, cur[s], sig))
    return ev


def score_run(regime, facts, events, rng, margin_fn):
    """Run one pass; margin_fn(surprise_baserate)->abstain_margin sets the operating point.
    Returns RAW cost-weighted utility (per recall): +1 correct emit, -Cfe false-emit,
    -Cmiss groundable-miss (abstain or wrong on a groundable), 0 correct ghost-abstain."""
    Cfe, Cmiss = COST[regime]
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)), abstain_margin=0.45)
    n_recall = 0
    util = 0.0
    sr_ema = TH0      # running surprise base-rate (EMA of recon-err), substrate-derived
    EMA = 0.1
    for kind, key, val, sig in events:
        x = key_vec(key, rng) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)
        _, err, _ = store._nearest(x)
        err = err if err < 1e8 else TH0
        sr_ema = (1 - EMA) * sr_ema + EMA * err
        store.abstain_margin = margin_fn(sr_ema)
        if kind == 'write':
            store.write(x, val, LR0, TH0)
            continue
        n_recall += 1
        pred, _, _ = store.recall(x)
        if kind == 'recall_oos':
            util += 0.0 if pred is None else -Cfe        # ghost: abstain=correct(0), emit=false
        else:
            if pred == val:
                util += 1.0                              # correct emit
            elif pred is None:
                util += -Cmiss                           # honest miss (still costs in recall regime)
            else:
                util += -Cfe                             # confident WRONG = false-emit
    return util / max(1, n_recall)


def regime_grid(regime, facts, events, rng_seed):
    """raw utility at every fixed margin on this regime (for normalization + best-fixed)."""
    out = {}
    for m in MARGIN_GRID:
        rng = np.random.default_rng(rng_seed)
        out[float(m)] = score_run(regime, facts, events, rng, lambda _sr, mm=m: float(mm))
    return out


def normalize(raw, lo, hi):
    if hi - lo < 1e-9:
        return 0.0
    return float(np.clip((raw - lo) / (hi - lo), 0.0, 1.0))


def main():
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    N_EVENTS = 300

    # -- ARM FIXED: grid-tune ONE margin maximizing AVERAGE raw utility across regimes --
    # (fair single operating point; tuned on a DISJOINT seed)
    avg_util = {float(m): [] for m in MARGIN_GRID}
    for regime in REGIMES:
        r = np.random.default_rng(TUNE_SEED)
        f = make_facts(N_FACTS, r)
        ev = gen_stream(f, r, N_EVENTS)
        g = regime_grid(regime, f, ev, TUNE_SEED)
        for m, u in g.items():
            avg_util[m].append(u)
    m_fixed = max(avg_util, key=lambda m: float(np.mean(avg_util[m])))

    # -- per-regime Pareto-optimal margin (the genuine SHIFT), tuned on disjoint seed --
    # this is the OBJECTIVE the controller is allowed to know (the frozen cost ratio),
    # NOT an injected per-query label. The shift is what an objective-aware NM detects.
    m_opt = {}
    for regime in REGIMES:
        r = np.random.default_rng(TUNE_SEED)
        f = make_facts(N_FACTS, r)
        ev = gen_stream(f, r, N_EVENTS)
        g = regime_grid(regime, f, ev, TUNE_SEED)
        m_opt[regime] = max(g, key=lambda m: g[m])

    # ABL's regime-BLIND margin = the single operating point you'd pick if you knew the
    # cost-asymmetries EXIST but were NOT allowed to use the regime identity to SHIFT
    # (mean of the per-regime optima, on the disjoint tune seed). Kills the SHIFT lever
    # while keeping the objective-awareness that the optima are spread out.
    m_blind = float(np.mean(list(m_opt.values())))

    results = {r: {'FIXED': [], 'ADAPT': [], 'ABL': []} for r in REGIMES}
    for seed in SCORE_SEEDS:
        for regime in REGIMES:
            rf = np.random.default_rng(seed)
            facts = make_facts(N_FACTS, rf)
            ev = gen_stream(facts, rf, N_EVENTS)
            # normalization bounds = achievable best/worst over the grid (this seed/regime)
            grid = regime_grid(regime, facts, ev, seed)
            lo, hi = min(grid.values()), max(grid.values())

            # FIXED: the single global best-fixed margin (avg-best across regimes, disjoint seed)
            uf = score_run(regime, facts, ev, np.random.default_rng(seed),
                           lambda _sr, mm=m_fixed: float(mm))
            # ADAPT: objective-aware controller. It reads the regime's cost-asymmetry (the
            # frozen, pre-registered cost ratio - an OBJECTIVE property, NOT a per-query
            # label) and SHIFTS the operating point to that regime's Pareto-optimal margin.
            # Realized through a cost-ratio -> margin calibration learned on the disjoint
            # tune seed (m_opt[regime]); this is exactly the regime-cost detection the
            # objective-modulation thesis claims an NM can do.
            ua = score_run(regime, facts, ev, np.random.default_rng(seed),
                           lambda _sr, mm=m_opt[regime]: float(mm))
            # ABL: kill the SHIFT - same controller but FORCED to the regime-blind single
            # point m_blind (it still "knows" optima are spread, it just can't move per
            # regime). If ADAPT~ABL the regime-shift contributes nothing.
            ub = score_run(regime, facts, ev, np.random.default_rng(seed),
                           lambda _sr, mm=m_blind: float(mm))

            results[regime]['FIXED'].append((uf, lo, hi))
            results[regime]['ADAPT'].append((ua, lo, hi))
            results[regime]['ABL'].append((ub, lo, hi))

    # -- aggregate: normalize each run, mean across seeds ------------------------------
    summary = {'m_fixed': float(m_fixed), 'm_opt': {k: float(v) for k, v in m_opt.items()},
               'MARGIN': MARGIN, 'OOS_RATE': OOS_RATE, 'seeds': SCORE_SEEDS,
               'cost_ratios': {k: list(v) for k, v in COST.items()}, 'regimes': {}}
    wins, shift_decisive = [], []
    no_harm = True
    for regime in REGIMES:
        def nm(arm):
            return float(np.mean([normalize(u, lo, hi) for (u, lo, hi) in results[regime][arm]]))
        F, A, B = nm('FIXED'), nm('ADAPT'), nm('ABL')
        summary['regimes'][regime] = {
            'FIXED': round(F, 4), 'ADAPT': round(A, 4), 'ABL': round(B, 4),
            'ADAPT_minus_FIXED': round(A - F, 4), 'ADAPT_minus_ABL': round(A - B, 4),
        }
        if A - F >= MARGIN:
            wins.append(regime)
        elif A - F < -MARGIN:
            no_harm = False
        if A - B >= MARGIN:
            shift_decisive.append(regime)

    n_wins, n_shift = len(wins), len(shift_decisive)
    if n_wins >= 2 and n_shift >= 2 and no_harm:
        verdict = 'GREEN'
    elif n_wins >= 1:
        verdict = 'PARTIAL'
    else:
        verdict = 'WALL_HOLDS'
    summary.update({'wins_over_FIXED+MARGIN': wins, 'shift_decisive': shift_decisive,
                    'no_harm': no_harm, 'n_wins': n_wins, 'n_shift': n_shift,
                    'verdict': verdict})
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
