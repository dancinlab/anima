#!/usr/bin/env python3
"""
H_1524 — MODULATOR DIVERSITY (신경조절 다양성): N INDEPENDENT, axis-targeted
neuromodulators (specificity) vs ONE global adaptive gain (H_1284's controller).
NEW orthogonal mechanism-family attempting the H_1284 NEUROMODULATION wall.

The wall (H_1284, 🔴/🧱): a SINGLE global context-adaptive gain never beats a
single well-tuned FIXED operating point (no-free-lunch, general). 5+ lenses
(incl. Amoeba homeostatic-buffer H_1509/b/c) confirmed it. THIS family is
DIFFERENT: instead of ONE global gain feeding a coupled knob bundle through one
EMA, use N=3 INDEPENDENT modulators — each driven by a DIFFERENT substrate
signal, targeting a DIFFERENT knob, with NO shared EMA (DA→abstain/consolidate,
NE/ACh→split-rate from a recall-noise floor, ACh→LR from fast-vs-slow surprise).
Real neuromodulation = separate nuclei, separate signals, separate targets
(the H_1284 FREEZE cites exactly DA/NE/ACh); anima's §Neuropharm already
realizes this per-axis structure. Hypothesis: SPECIFICITY beats both a single
global gain AND best-fixed across regimes.

HARD-GATE-1: numpy mirror of CORE/engine_cli.hexa VAdaptField → DIRECTIONAL only
(a_engine_native_learning). Engine-native R2 (.hexa via CORE) = binding ING.
p7 exact metric (NO LLM judge / perplexity / loss); every knob = no-grad
read-out of substrate state. $0 CPU. Frozen falsifier in H_1524_FREEZE.txt.

The environment (MemStore / gen_stream / make_facts / grid_tune / Neuromod=
GLOBAL) is BYTE-REUSED from state/universe-probes/h1284_neuromodulation_gain.py
— SAME task / regimes / best-fixed baseline / frozen MARGIN the wall used.
"""
import numpy as np
import json, os, sys

# ── import the byte-identical H_1284 environment (frozen-first, no env change) ─
_H1284 = os.path.join(os.path.dirname(__file__), '..', 'universe-probes',
                      'h1284_neuromodulation_gain.py')
import importlib.util
_spec = importlib.util.spec_from_file_location('h1284', _H1284)
h1284 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h1284)

DIM = h1284.DIM
MemStore = h1284.MemStore
key_vec = h1284.key_vec
make_facts = h1284.make_facts
gen_stream = h1284.gen_stream
grid_tune = h1284.grid_tune
Neuromod = h1284.Neuromod          # the H_1284 GLOBAL single-EMA controller (arm S)


# ── DIVERSITY controller: N=3 INDEPENDENT axis-targeted modulators ────────────
class DiversityMod:
    """3 SEPARATE modulators, each with its OWN signal stream and OWN EMA state,
    each targeting a DIFFERENT knob — NO shared expected-uncertainty (the exact
    separation that defines the diversity family vs H_1284's monolithic û).

    ACh  (LR)      : s_fast (λ=0.5) vs s_slow (λ=0.05) — genuine-novelty axis.
    NE/ACh (TH)    : n_floor = LONG-EMA of RECALL-cue surprise ONLY — noise-floor
                     axis (writes excluded), the H_1230 anti-over-split guard.
    DA   (abstain) : r_ema = correct-recall rate — exploit/explore + consolidate.
    `collapse=True` removes specificity: all 3 read the SAME single global EMA
    (the recon-err EMA, like S) — the decisive ablation (c2). If collapse≈full,
    specificity is INERT and the wall holds.
    """
    KA = 1.2     # ACh: fast-vs-slow surprise -> plasticity (LR) gain
    KT = 0.8     # NE/ACh: recall-noise-floor -> split-thresh raise
    KD = 0.4     # DA: reward -> abstain narrowing (exploit) + consolidate gain
    KG = 0.4     # DA consolidation: reward-EMA -> winner-pull gain
    L_FAST = 0.5
    L_SLOW = 0.05
    L_FLOOR = 0.05
    L_REWARD = 0.1

    def __init__(self, LR0, TH0, abstain0, collapse=False):
        self.LR0, self.TH0, self.abstain0 = LR0, TH0, abstain0
        self.collapse = collapse
        # INDEPENDENT per-channel state (no sharing) — the diversity claim
        self.s_fast = TH0      # ACh fast surprise EMA
        self.s_slow = TH0      # ACh slow surprise EMA
        self.n_floor = TH0     # NE/ACh recall-noise floor EMA
        self.r_ema = 0.5       # DA reward EMA (start at chance)
        # collapsed: ONE global EMA shared by all channels (like S's û)
        self.u_global = TH0

    def observe(self, surprise, reward, is_recall):
        if self.collapse:
            # all channels collapse to ONE global signal (specificity removed)
            self.u_global = (1 - 0.1) * self.u_global + 0.1 * surprise
            self.r_ema = (1 - self.L_REWARD) * self.r_ema + self.L_REWARD * reward
            return
        # INDEPENDENT streams ↓
        self.s_fast = (1 - self.L_FAST) * self.s_fast + self.L_FAST * surprise
        self.s_slow = (1 - self.L_SLOW) * self.s_slow + self.L_SLOW * surprise
        if is_recall:   # noise-floor channel reads RECALL-cue surprise ONLY
            self.n_floor = (1 - self.L_FLOOR) * self.n_floor + self.L_FLOOR * surprise
        self.r_ema = (1 - self.L_REWARD) * self.r_ema + self.L_REWARD * reward

    def knobs(self, surprise, channels=('ACh', 'split', 'DA')):
        """Return (LR, TH, ab). `channels` = active set; a channel NOT in the set
        is held at its FIXED A-value (per-channel marginal ablation)."""
        if self.collapse:
            u = self.u_global
            # all knobs driven by the SAME global signal (no per-axis specificity)
            LR = self.LR0 * (1 + self.KA * (surprise - u)) if 'ACh' in channels else self.LR0
            LR = float(np.clip(LR, 0.05, 0.60))
            LR = float(np.clip(LR * (1 + self.KG * self.r_ema), 0.05, 0.60)) if 'DA' in channels else LR
            TH = self.TH0 * (1 + self.KT * (u - self.TH0)) if 'split' in channels else self.TH0
            TH = float(np.clip(TH, 0.15, 0.60))
            ab = self.abstain0 * (1 - self.KD * (self.r_ema - 0.5)) if 'DA' in channels else self.abstain0
            ab = float(np.clip(ab, 0.20, 1.20))
            return LR, TH, ab

        # ── INDEPENDENT axis-targeted knobs ──
        # ACh (LR): genuine-novelty = THIS event's surprise above its OWN slow baseline
        if 'ACh' in channels:
            LR = self.LR0 * (1 + self.KA * (self.s_fast - self.s_slow))
        else:
            LR = self.LR0
        LR = float(np.clip(LR, 0.05, 0.60))
        # DA consolidation: scale winner-pull on a working store (reward EMA)
        if 'DA' in channels:
            LR = float(np.clip(LR * (1 + self.KG * self.r_ema), 0.05, 0.60))
        # NE/ACh (TH): raise split bar when the RECALL-noise floor is high
        if 'split' in channels:
            TH = self.TH0 * (1 + self.KT * (self.n_floor - self.TH0))
        else:
            TH = self.TH0
        TH = float(np.clip(TH, 0.15, 0.60))
        # DA (abstain): exploit when reward high (narrow), explore when low (widen)
        if 'DA' in channels:
            ab = self.abstain0 * (1 - self.KD * (self.r_ema - 0.5))
        else:
            ab = self.abstain0
        ab = float(np.clip(ab, 0.20, 1.20))
        return LR, TH, ab


def run_diversity(regime, facts, events, rng, LR0, TH0, abstain0,
                  collapse=False, channels=('ACh', 'split', 'DA')):
    """Run the DIVERSITY arm (or D-COLLAPSE / per-channel ablation). Mirrors
    h1284.run_arm's event loop exactly; only the controller differs."""
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)),
                     abstain_margin=abstain0)
    dm = DiversityMod(LR0, TH0, abstain0, collapse=collapse)
    n_recall = n_correct = n_fab = 0
    for kind, key, val, sig in events:
        x = key_vec(key, rng) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)
        _, err, _ = store._nearest(x)
        err = err if err < 1e8 else dm.TH0
        is_recall = not (kind == 'write')
        LR, TH, ab = dm.knobs(err, channels=channels)
        store.abstain_margin = ab

        if kind == 'write':
            store.write(x, val, LR, TH)
            dm.observe(err, 0.0, is_recall=False)
        else:  # recall or recall_oos
            n_recall += 1
            pred, rerr, _ = store.recall(x)
            if kind == 'recall_oos':
                if pred is not None:
                    n_fab += 1
                reward = 1.0 if pred is None else 0.0
            else:
                if pred == val:
                    n_correct += 1; reward = 1.0
                elif pred is None:
                    reward = 0.0
                else:
                    n_fab += 1; reward = 0.0
            dm.observe(rerr if rerr < 1e8 else dm.TH0, reward, is_recall=True)

    acc = n_correct / max(1, n_recall)
    fab = n_fab / max(1, n_recall)
    return acc, fab, acc - fab


def main():
    N_FACTS = 30
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    REGIMES = ('R1_STABLE', 'R2_DRIFT', 'R3_NOISE')
    MARGIN = 0.05

    # ── ARM A tuning (DISJOINT seed) — byte-reused grid_tune (same best-fixed) ─
    tune_rng = np.random.default_rng(TUNE_SEED)
    tune_facts = make_facts(N_FACTS, tune_rng)
    LR0_star, TH0_star = grid_tune(tune_facts, TUNE_SEED)

    acc = {r: {k: [] for k in
               ('A', 'S', 'D', 'DCOL', 'A_fab', 'D_fab',
                'D_noACh', 'D_nosplit', 'D_noDA')} for r in REGIMES}

    for seed in SCORE_SEEDS:
        for regime in REGIMES:
            rng_facts = np.random.default_rng(seed)
            facts = make_facts(N_FACTS, rng_facts)
            ev = gen_stream(regime, facts, rng_facts, n_events=300)

            # A FIXED (byte-reused H_1284 run_arm, adaptive=False)
            a_acc, a_fab, a_cap = h1284.run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                adaptive=False)
            # S GLOBAL (byte-reused H_1284 run_arm, adaptive=True = the wall)
            s_acc, s_fab, s_cap = h1284.run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                adaptive=True)
            # D DIVERSITY (N=3 independent axis-targeted modulators)
            d_acc, d_fab, d_cap = run_diversity(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                collapse=False)
            # D-COLLAPSE (specificity ablation — all channels share ONE signal)
            dc_acc, dc_fab, dc_cap = run_diversity(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                collapse=True)
            # per-channel marginal ablations
            _, _, dnoa = run_diversity(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                collapse=False, channels=('split', 'DA'))
            _, _, dnos = run_diversity(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                collapse=False, channels=('ACh', 'DA'))
            _, _, dnod = run_diversity(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                collapse=False, channels=('ACh', 'split'))

            acc[regime]['A'].append(a_cap)
            acc[regime]['S'].append(s_cap)
            acc[regime]['D'].append(d_cap)
            acc[regime]['DCOL'].append(dc_cap)
            acc[regime]['A_fab'].append(a_fab)
            acc[regime]['D_fab'].append(d_fab)
            acc[regime]['D_noACh'].append(dnoa)
            acc[regime]['D_nosplit'].append(dnos)
            acc[regime]['D_noDA'].append(dnod)

    # ── aggregate + frozen falsifier ─────────────────────────────────────────
    summary = {'LR0_star': LR0_star, 'TH0_star': TH0_star, 'MARGIN': MARGIN,
               'seeds': SCORE_SEEDS, 'regimes': {}}
    wins = []          # D beats A+MARGIN
    spec_ok = []       # specificity separated (D - D-COLLAPSE >= MARGIN)
    s_clear = []       # S (global) clears the bar (continuity check c3)
    fab_ok = True
    never_much_worse = True
    for regime in REGIMES:
        A = float(np.mean(acc[regime]['A']))
        S = float(np.mean(acc[regime]['S']))
        D = float(np.mean(acc[regime]['D']))
        DC = float(np.mean(acc[regime]['DCOL']))
        Af = float(np.mean(acc[regime]['A_fab']))
        Df = float(np.mean(acc[regime]['D_fab']))
        summary['regimes'][regime] = {
            'A_cap': round(A, 4), 'S_global_cap': round(S, 4),
            'D_diversity_cap': round(D, 4), 'D_collapse_cap': round(DC, 4),
            'A_fab': round(Af, 4), 'D_fab': round(Df, 4),
            'D_minus_A': round(D - A, 4),
            'D_minus_collapse': round(D - DC, 4),
            'S_minus_A': round(S - A, 4),
            'marginal_drop_ACh': round(D - float(np.mean(acc[regime]['D_noACh'])), 4),
            'marginal_drop_split': round(D - float(np.mean(acc[regime]['D_nosplit'])), 4),
            'marginal_drop_DA': round(D - float(np.mean(acc[regime]['D_noDA'])), 4),
        }
        beats = D >= A + MARGIN
        if beats:
            wins.append(regime)
            if Df > Af:
                fab_ok = False
            if D - DC >= MARGIN:
                spec_ok.append(regime)
            if S >= A + MARGIN:
                s_clear.append(regime)
        else:
            if D < A - 0.02:
                never_much_worse = False

    n_wins = len(wins)
    n_spec = len(spec_ok)
    # GREEN: >=2 wins, fab ok, never much worse, specificity separated on wins,
    #        and S (global) did NOT clear (diversity-specific, c3)
    s_did_not_clear = (len(s_clear) == 0)
    if n_wins >= 2 and fab_ok and never_much_worse and n_spec >= 2 and s_did_not_clear:
        verdict = 'GREEN'
    elif n_wins >= 1:
        verdict = 'PARTIAL'   # single operating point OR specificity not separated
    else:
        verdict = 'RED'       # no regime beat best-fixed (wall holds — no free lunch)

    summary['wins_over_A+MARGIN'] = wins
    summary['specificity_separated'] = spec_ok
    summary['S_global_cleared_bar'] = s_clear
    summary['fab_ok'] = fab_ok
    summary['never_much_worse'] = never_much_worse
    summary['verdict'] = verdict
    summary['note'] = ('DIRECTIONAL (numpy mirror, HARD-GATE-1); '
                       'engine-native R2 is the binding follow-on if GREEN')
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
