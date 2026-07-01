#!/usr/bin/env python3
"""
H_1525 — PREDICTIVE / ANTICIPATORY NEUROMODULATION (forward-model-gated gain).

Break the H_1284 NEUROMODULATION wall with a genuinely different mechanism-
family: gate the gain on the PREDICTED next-step surprise from a forward model,
BEFORE the step, instead of REACTING to the current surprise.

WHY (a_break_the_wall): every REACTIVE adaptive gain (H_1284 + Amoeba buffer
H_1509/b/c) is structurally one step behind a regime change — by the time
surprise has risen, the damaging writes have landed, so a good FIXED constant
beats a lagging adjustment. An ANTICIPATORY controller that pre-adjusts gain
AHEAD of the shift, using a cerebellar forward model's next-step prediction
(substrate lens: VForwardField H_1280), can in principle win where reactive
cannot. This is the strongest a-priori candidate to break the wall.

REUSE THE FROZEN H_1284 HARNESS verbatim (same MemStore / Neuromod knob
formulas / gen_stream regimes / capacity / grid-tune baseline / MARGIN). The
ONLY new arm is the gain INPUT: reactive=current s_t, predictive=forward-model
shat_{t+1}. Ablations: ABL-NOLOOKAHEAD (shat:=s_t, = reactive by construction)
and ABL-SHUFFLE (phase-scramble shat, destroy predictor accuracy).

numpy mirror of CORE/engine_cli.hexa VAdaptField — DIRECTIONAL (host no torch,
a_engine_native_learning HARD-GATE-1). $0 CPU, 3 seeds. Frozen falsifier in
state/verdicts/1525_neuromod_predictive/H_1525_FREEZE.txt. p7 exact metric, no
loss, no LLM judge. live CORE/*.hexa UNTOUCHED.
"""
import numpy as np
import json, sys, os

# import the FROZEN H_1284 harness from its canonical location (single source —
# do NOT copy/re-tune; we reuse its MemStore, Neuromod knob constants, regimes,
# generators, capacity, grid-tune baseline verbatim).
# file = <state>/1525_neuromod_predictive/h1525_predictive.py → two dirnames up
# reaches <state>/, then the canonical harness dir state/universe-probes/.
_HARNESS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'universe-probes')
sys.path.insert(0, _HARNESS_DIR)
from h1284_neuromodulation_gain import (
    fnv1a, key_vec, MemStore, Neuromod, DIM,
    make_facts, gen_stream, grid_tune,
)


# ── forward model: online AR(2)+EMA predictor of the surprise series ──────────
# Cheap numpy stand-in for the live VForwardField (H_1280) cerebellar tick:
# predicts the NEXT-step surprise shat_{t+1} from past surprise only, via online
# least-mean-squares (p7: trained on the surprise series, NOT on the capability
# objective — no loss leak into the gate). Sees no regime label, no future.
class SurpriseForward:
    ETA = 0.05          # online LMS rate (cerebellar eta; vforward_update analog)
    EMA = 0.1           # surprise EMA (matches Neuromod.EMA)

    def __init__(self, s0):
        # regressor = [bias, s_t, s_{t-1}, ema]; init toward identity (predict
        # "next ≈ current") so an UNTRAINED model degrades gracefully to reactive,
        # then LEARNS the lead/lag structure online.
        self.w = np.array([0.0, 1.0, 0.0, 0.0])
        self.s_prev = s0
        self.s_prev2 = s0
        self.ema = s0
        self.last_pred = s0

    def _feat(self):
        return np.array([1.0, self.s_prev, self.s_prev2, self.ema])

    def predict(self):
        """shat_{t+1} from past surprise (formed BEFORE the current event knobs)."""
        self.last_pred = float(self.w @ self._feat())
        return self.last_pred

    def update(self, s_now):
        """online LMS: correct the prediction the PREVIOUS tick made of s_now,
        then roll the lag buffers. (vforward_update online tick analog.)"""
        feat = self._feat()
        pred = float(self.w @ feat)
        err = s_now - pred
        self.w = self.w + self.ETA * err * feat
        # roll lags + ema with the realized surprise
        self.s_prev2 = self.s_prev
        self.s_prev = s_now
        self.ema = (1 - self.EMA) * self.ema + self.EMA * s_now


# ── one arm: A=fixed, R=reactive(current s), P=predictive(forward shat), with the
#    two ablations of P. The MemStore + Neuromod knob formulas are the FROZEN
#    H_1284 harness; only the LR input swaps. ───────────────────────────────────
def run_arm(regime, facts, events, rng, LR0, TH0, abstain0, mode,
            pred_shuffle_seq=None):
    """mode in {'fixed','reactive','predictive','abl_nolook','abl_shuffle'}.
    For 'abl_shuffle', pred_shuffle_seq supplies a pre-scrambled shat schedule."""
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)),
                     abstain_margin=abstain0)
    adaptive = mode != 'fixed'
    nm = Neuromod(LR0, TH0, abstain0) if adaptive else None
    fwd = None
    if mode in ('predictive', 'abl_shuffle'):
        # seed the forward model with the first key recon-error vs empty store
        fwd = SurpriseForward(s0=TH0)
    n_recall = n_correct = n_fab = 0
    pred_log = []     # (pred, actual) for forward-model accuracy diagnostic
    si = 0

    for kind, key, val, sig in events:
        x = key_vec(key, rng) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)

        if adaptive:
            _, err, _ = store._nearest(x)
            err = err if err < 1e8 else nm.TH0     # current surprise s_t
            if mode == 'reactive':
                gate_s = err
            elif mode == 'abl_nolook':
                gate_s = err                       # shat_{t+1} := s_t (no lookahead)
            elif mode == 'predictive':
                gate_s = fwd.predict()             # shat_{t+1} forward-model (BEFORE step)
                pred_log.append((gate_s, err))
            elif mode == 'abl_shuffle':
                gate_s = pred_shuffle_seq[si]       # accuracy destroyed (scrambled shat)
                si += 1
            # SAME Neuromod knob formulas as the wall — only the LR input swaps to
            # gate_s (the surprise the knobs see).
            LR, TH, ab = nm.knobs(gate_s)
            store.abstain_margin = ab
        else:
            LR, TH = LR0, TH0
            store.abstain_margin = abstain0
            err = 0.0

        if kind == 'write':
            store.write(x, val, LR, TH)
            if adaptive:
                nm.observe(err, 0.0)
                if fwd is not None:
                    fwd.update(err)
        else:  # recall / recall_oos
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
            if adaptive:
                rr = rerr if rerr < 1e8 else nm.TH0
                nm.observe(rr, reward)
                if fwd is not None:
                    fwd.update(rr)

    acc = n_correct / max(1, n_recall)
    fab = n_fab / max(1, n_recall)
    # forward-model accuracy (Pearson rho of shat_{t+1} vs realized next surprise)
    rho = None
    if pred_log and len(pred_log) > 3:
        ps = np.array([p for p, _ in pred_log[:-1]])
        ac = np.array([a for _, a in pred_log[1:]])   # realized surprise one tick later
        if ps.std() > 1e-9 and ac.std() > 1e-9:
            rho = float(np.corrcoef(ps, ac)[0, 1])
    return acc, fab, acc - fab, rho


def harvest_pred_schedule(regime, facts, events, rng, LR0, TH0, abstain0):
    """Run the predictive forward model ONCE to harvest its shat schedule, then
    phase-scramble it for the ABL-SHUFFLE arm (same marginal shat values, future
    decorrelated)."""
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)), abstain_margin=abstain0)
    nm = Neuromod(LR0, TH0, abstain0)
    fwd = SurpriseForward(s0=TH0)
    sched = []
    for kind, key, val, sig in events:
        x = key_vec(key, rng) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)
        _, err, _ = store._nearest(x)
        err = err if err < 1e8 else nm.TH0
        sched.append(fwd.predict())
        LR, TH, _ = nm.knobs(sched[-1])
        if kind == 'write':
            store.write(x, val, LR, TH); nm.observe(err, 0.0); fwd.update(err)
        else:
            pred, rerr, _ = store.recall(x)
            rr = rerr if rerr < 1e8 else nm.TH0
            reward = 1.0 if (pred == val or (key.startswith('ghost') and pred is None)) else 0.0
            nm.observe(rr, reward); fwd.update(rr)
    sched = np.array(sched)
    return sched[rng.permutation(len(sched))]


def main():
    N_FACTS = 30
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    REGIMES = ('R1_STABLE', 'R2_DRIFT', 'R3_NOISE')
    MARGIN = 0.05

    # ARM A baseline = the wall grid-tuned best fixed (DISJOINT tune seed)
    tune_rng = np.random.default_rng(TUNE_SEED)
    tune_facts = make_facts(N_FACTS, tune_rng)
    LR0_star, TH0_star = grid_tune(tune_facts, TUNE_SEED)

    acc = {r: {k: [] for k in
               ('A', 'R', 'P', 'ABLN', 'ABLS',
                'A_fab', 'R_fab', 'P_fab', 'ABLN_fab', 'ABLS_fab', 'rho')}
           for r in REGIMES}

    for seed in SCORE_SEEDS:
        for regime in REGIMES:
            rng_facts = np.random.default_rng(seed)
            facts = make_facts(N_FACTS, rng_facts)
            ev = gen_stream(regime, facts, rng_facts, n_events=300)

            a_acc, a_fab, a_cap, _ = run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0, 'fixed')
            r_acc, r_fab, r_cap, _ = run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0, 'reactive')
            p_acc, p_fab, p_cap, rho = run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0, 'predictive')
            n_acc, n_fab, n_cap, _ = run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0, 'abl_nolook')
            shuf = harvest_pred_schedule(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0)
            s_acc, s_fab, s_cap, _ = run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                'abl_shuffle', pred_shuffle_seq=shuf)

            acc[regime]['A'].append(a_cap);  acc[regime]['A_fab'].append(a_fab)
            acc[regime]['R'].append(r_cap);  acc[regime]['R_fab'].append(r_fab)
            acc[regime]['P'].append(p_cap);  acc[regime]['P_fab'].append(p_fab)
            acc[regime]['ABLN'].append(n_cap); acc[regime]['ABLN_fab'].append(n_fab)
            acc[regime]['ABLS'].append(s_cap); acc[regime]['ABLS_fab'].append(s_fab)
            if rho is not None:
                acc[regime]['rho'].append(rho)

    summary = {'LR0_star': LR0_star, 'TH0_star': TH0_star, 'MARGIN': MARGIN,
               'seeds': SCORE_SEEDS, 'regimes': {}}
    wins = []            # regimes where P beats A+MARGIN
    p_never_much_worse = True
    fab_ok = True
    dissoc_ok = []       # regimes where P beats R+MARGIN  (c4)
    abl_ok = []          # regimes where BOTH ablations <= P-MARGIN  (c5)

    for regime in REGIMES:
        A = float(np.mean(acc[regime]['A']))
        R = float(np.mean(acc[regime]['R']))
        P = float(np.mean(acc[regime]['P']))
        N = float(np.mean(acc[regime]['ABLN']))
        S = float(np.mean(acc[regime]['ABLS']))
        Af = float(np.mean(acc[regime]['A_fab']))
        Pf = float(np.mean(acc[regime]['P_fab']))
        rho = float(np.mean(acc[regime]['rho'])) if acc[regime]['rho'] else None
        summary['regimes'][regime] = {
            'A_cap': round(A, 4), 'R_cap': round(R, 4), 'P_cap': round(P, 4),
            'ABL_nolook_cap': round(N, 4), 'ABL_shuffle_cap': round(S, 4),
            'A_fab': round(Af, 4), 'P_fab': round(Pf, 4),
            'P_minus_A': round(P - A, 4), 'P_minus_R': round(P - R, 4),
            'P_minus_ABLnolook': round(P - N, 4), 'P_minus_ABLshuffle': round(P - S, 4),
            'fwd_rho': round(rho, 4) if rho is not None else None,
        }
        if P >= A + MARGIN:
            wins.append(regime)
            if Pf > Af:
                fab_ok = False
            if P >= R + MARGIN:
                dissoc_ok.append(regime)
            if N <= P - MARGIN and S <= P - MARGIN:
                abl_ok.append(regime)
        else:
            if P < A - 0.02:
                p_never_much_worse = False

    n_wins = len(wins)
    # GREEN iff c1 (>=2 wins) & c2 (never much worse) & c3 (fab ok) &
    #          c4 (dissociation on ALL wins) & c5 (ablation decisive on ALL wins)
    c1 = n_wins >= 2
    c2 = p_never_much_worse
    c3 = fab_ok
    c4 = len(dissoc_ok) >= 2 and all(w in dissoc_ok for w in wins)
    c5 = len(abl_ok) >= 2 and all(w in abl_ok for w in wins)
    if c1 and c2 and c3 and c4 and c5:
        verdict = 'GREEN'           # WALL BROKEN
    elif n_wins == 1 or (n_wins >= 2 and not (c4 and c5)):
        verdict = 'PARTIAL'
    else:
        verdict = 'WALL_HOLDS'      # 🔴/🧱 no free lunch, anticipation lens too

    summary['wins_P_over_A'] = wins
    summary['dissociation_P_over_R'] = dissoc_ok
    summary['ablation_decisive'] = abl_ok
    summary['c1_two_wins'] = c1
    summary['c2_never_much_worse'] = c2
    summary['c3_fab_ok'] = c3
    summary['c4_dissociation'] = c4
    summary['c5_ablation_decisive'] = c5
    summary['verdict'] = verdict
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
