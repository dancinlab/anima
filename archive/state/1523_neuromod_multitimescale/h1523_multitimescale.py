#!/usr/bin/env python3
"""
H_1523 — MULTI-TIMESCALE NEUROMODULATION (tonic baseline + phasic transient)
against the H_1284 NEUROMODULATION wall (no-free-lunch, 5+ lenses held).

THE WALL: a SINGLE-timescale context-adaptive gain / buffer / lr never beats the
best-tuned FIXED operating point (H_1284 + R3 + H_1509/b/c). THE NEW FAMILY
(a_break_the_wall, a_no_llm_frame_trap, c15): real neuromodulators are DUAL-
timescale — a slow TONIC baseline (operating mode) PLUS a fast PHASIC transient
(reward-prediction-error burst). A single EMA must pick ONE bandwidth, which the
grid-tuned fixed point already matches. Decompose the modulator into TWO
timescales and ask whether it beats best-fixed across regimes a single-timescale
one cannot.

FROZEN-FIRST (state/verdicts/1523_neuromod_multitimescale/H_1523_FREEZE.txt):
REUSE the EXACT H_1284 task / regimes / best-fixed baseline / metric / bar /
seeds (imported from state/universe-probes/h1284_neuromodulation_gain.py — NOT
reimplemented). ONLY new code = arm D (two-timescale modulator) + two decisive
ablations (phasic to 0 pure-tonic, tonic to const pure-phasic). MARGIN=0.05 UNMOVED.

p7: exact ground truth, no LLM judge, no loss term — every knob is a no-grad
read-out of substrate state. numpy mirror of CORE/engine_cli.hexa VAdaptField
(host has no torch) -> DIRECTIONAL (a_engine_native_learning hard-gate-1). $0 CPU,
3 seeds. Honest: 5+ lenses already held the wall — it likely HOLDS; if it does,
this is the Nth independent lens CONFIRMING it (a valid result, c9). NO tune-to-green.
"""
import numpy as np
import json, sys, os

# ── REUSE the EXACT H_1284 harness (task / regimes / baseline / metric) ───────
# this file lives under state/1523_neuromod_multitimescale/ ; the H_1284 probe is
# at state/universe-probes/ ; both two levels up from here share the state/ root.
_here = os.path.dirname(os.path.abspath(__file__))
_state_root = os.path.normpath(os.path.join(_here, '..'))
_probe_dir = os.path.join(_state_root, 'universe-probes')
sys.path.insert(0, _probe_dir)
from h1284_neuromodulation_gain import (
    fnv1a, key_vec, MemStore, Neuromod, DIM,
    make_facts, gen_stream, grid_tune,
    run_arm as h1284_run_arm,
)


# ── TWO-TIMESCALE modulator: slow TONIC EMA + fast PHASIC transient ───────────
class TwoTimescaleMod:
    """gain_t = tonic_slow_baseline + phasic_fast_transient.

    Two EMAs of the surprise signal with DIFFERENT time-constants. The slow
    tonic sets the sustained operating mode (split-bar, abstain, baseline
    plasticity); the fast phasic transient (phasic - tonic) spikes plasticity on
    a genuinely novel event then decays — the decomposition a SINGLE EMA (H_1284
    arm B) cannot do. All knobs are no-grad read-outs of substrate state (p7).

    Pre-registered constants (H_1523_FREEZE.txt, written before scoring):
      a_tonic=0.02 (slow ~50-tick), a_phasic=0.50 (fast ~2-tick),
      kT_tonic=0.8, kP_phasic=1.2, kT_split=0.8, kN_tonic=0.6.
    ABLATIONS: phasic0 (kP_phasic:=0 -> pure tonic) · tonic0 (a_tonic:=0 -> tonic
    frozen at TH0, pure phasic)."""
    A_TONIC = 0.02
    A_PHASIC = 0.50
    KT_TONIC = 0.8
    KP_PHASIC = 1.2
    KT_SPLIT = 0.8
    KN_TONIC = 0.6

    def __init__(self, LR0, TH0, abstain0, phasic0=False, tonic0=False):
        self.LR0, self.TH0, self.ab0 = LR0, TH0, abstain0
        self.tonic = TH0          # slow baseline (init at the split bar)
        self.phasic = TH0         # fast transient tracker
        self.phasic0 = phasic0    # ablation: kill phasic term (pure tonic)
        self.tonic0 = tonic0      # ablation: freeze tonic (pure phasic)

    def observe(self, surprise):
        if not self.tonic0:
            self.tonic = (1 - self.A_TONIC) * self.tonic + self.A_TONIC * surprise
        # tonic0 ablation: tonic stays frozen at its init TH0
        self.phasic = (1 - self.A_PHASIC) * self.phasic + self.A_PHASIC * surprise

    def knobs(self, surprise):
        # update timescales on the CURRENT surprise first (causal read-out)
        self.observe(surprise)
        transient = (self.phasic - self.tonic)
        kP = 0.0 if self.phasic0 else self.KP_PHASIC
        # ACh plasticity: slow tonic baseline + fast phasic burst
        LR = self.LR0 * (1 + self.KT_TONIC * (self.tonic - self.TH0)
                             + kP * transient)
        LR = float(np.clip(LR, 0.05, 0.60))
        # ACh/novelty split: tracks the SLOW tonic baseline ONLY (H_1230 guard:
        # transient bursts must NOT raise the split bar)
        TH = self.TH0 * (1 + self.KT_SPLIT * (self.tonic - self.TH0))
        TH = float(np.clip(TH, 0.15, 0.60))
        # NE abstain: caution tracks the slow tonic arousal baseline
        ab = self.ab0 * (1 + self.KN_TONIC * (self.tonic - self.TH0))
        ab = float(np.clip(ab, 0.20, 1.20))
        return LR, TH, ab


def run_arm_2ts(regime, facts, events, rng, LR0, TH0, abstain0,
                phasic0=False, tonic0=False):
    """Two-timescale arm on the SAME MemStore / event-stream / metric as H_1284.
    Mirrors h1284 run_arm's adaptive path EXACTLY except the modulator is the
    TwoTimescaleMod (tonic+phasic) instead of the single-EMA Neuromod."""
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)),
                     abstain_margin=abstain0)
    nm = TwoTimescaleMod(LR0, TH0, abstain0, phasic0=phasic0, tonic0=tonic0)
    n_recall = n_correct = n_fab = 0
    for kind, key, val, sig in events:
        x = key_vec(key, rng) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)
        _, err, _ = store._nearest(x)
        err = err if err < 1e8 else nm.TH0
        LR, TH, ab = nm.knobs(err)
        store.abstain_margin = ab

        if kind == 'write':
            store.write(x, val, LR, TH)
        else:  # recall / recall_oos
            n_recall += 1
            pred, rerr, _ = store.recall(x)
            if kind == 'recall_oos':
                if pred is not None:
                    n_fab += 1
            else:
                if pred == val:
                    n_correct += 1
                elif pred is not None:
                    n_fab += 1
    acc = n_correct / max(1, n_recall)
    fab = n_fab / max(1, n_recall)
    return acc, fab, acc - fab


def run_arm_single(regime, facts, events, rng, LR0, TH0, abstain0):
    """EXACT H_1284 arm B (single-EMA Neuromod) reproduced for continuity —
    same body as h1284 run_arm(adaptive=True), inlined to keep the metric byte-
    identical and avoid the h1284 shuffle branch."""
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)),
                     abstain_margin=abstain0)
    nm = Neuromod(LR0, TH0, abstain0)
    n_recall = n_correct = n_fab = 0
    for kind, key, val, sig in events:
        x = key_vec(key, rng) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)
        _, err, _ = store._nearest(x)
        err = err if err < 1e8 else nm.TH0
        LR, TH, ab = nm.knobs(err)
        store.abstain_margin = ab
        if kind == 'write':
            store.write(x, val, LR, TH)
            nm.observe(err, 0.0)
        else:
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
            nm.observe(rerr if rerr < 1e8 else nm.TH0, reward)
    acc = n_correct / max(1, n_recall)
    fab = n_fab / max(1, n_recall)
    return acc, fab, acc - fab


def main():
    # ── identical knobs to H_1284 (frozen-first) ─────────────────────────────
    N_FACTS = 30
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    REGIMES = ('R1_STABLE', 'R2_DRIFT', 'R3_NOISE')
    MARGIN = 0.05

    # ARM A best-fixed: SAME grid / disjoint tune seed as H_1284
    tune_rng = np.random.default_rng(TUNE_SEED)
    tune_facts = make_facts(N_FACTS, tune_rng)
    LR0_star, TH0_star = grid_tune(tune_facts, TUNE_SEED)

    keys = ('A', 'B', 'D', 'D_PHASIC0', 'D_TONIC0')
    res = {r: {k: [] for k in keys} for r in REGIMES}
    fab = {r: {k: [] for k in keys} for r in REGIMES}
    for seed in SCORE_SEEDS:
        for regime in REGIMES:
            rng_facts = np.random.default_rng(seed)
            facts = make_facts(N_FACTS, rng_facts)
            ev = gen_stream(regime, facts, rng_facts, n_events=300)

            a_acc, a_fab, a_cap = h1284_run_arm(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                adaptive=False)
            b_acc, b_fab, b_cap = run_arm_single(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0)
            d_acc, d_fab, d_cap = run_arm_2ts(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0)
            dp_acc, dp_fab, dp_cap = run_arm_2ts(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                phasic0=True)
            dt_acc, dt_fab, dt_cap = run_arm_2ts(regime, facts, ev,
                np.random.default_rng(seed), LR0_star, TH0_star, ABSTAIN0,
                tonic0=True)

            res[regime]['A'].append(a_cap); fab[regime]['A'].append(a_fab)
            res[regime]['B'].append(b_cap); fab[regime]['B'].append(b_fab)
            res[regime]['D'].append(d_cap); fab[regime]['D'].append(d_fab)
            res[regime]['D_PHASIC0'].append(dp_cap)
            fab[regime]['D_PHASIC0'].append(dp_fab)
            res[regime]['D_TONIC0'].append(dt_cap)
            fab[regime]['D_TONIC0'].append(dt_fab)

    # ── aggregate + frozen falsifier (verbatim H_1523_FREEZE bar) ────────────
    summary = {'LR0_star': LR0_star, 'TH0_star': TH0_star, 'MARGIN': MARGIN,
               'seeds': SCORE_SEEDS, 'regimes': {}}
    wins = []
    fab_ok = True
    never_much_worse = True
    ablation_separated_on_wins = []   # regimes where BOTH ablations < D-MARGIN
    for regime in REGIMES:
        A = float(np.mean(res[regime]['A']))
        B = float(np.mean(res[regime]['B']))
        D = float(np.mean(res[regime]['D']))
        DP = float(np.mean(res[regime]['D_PHASIC0']))
        DT = float(np.mean(res[regime]['D_TONIC0']))
        Af = float(np.mean(fab[regime]['A']))
        Df = float(np.mean(fab[regime]['D']))
        summary['regimes'][regime] = {
            'A_cap': round(A, 4), 'B_single_cap': round(B, 4),
            'D_2ts_cap': round(D, 4),
            'D_PHASIC0_cap': round(DP, 4), 'D_TONIC0_cap': round(DT, 4),
            'A_fab': round(Af, 4), 'D_fab': round(Df, 4),
            'D_minus_A': round(D - A, 4),
            'B_single_minus_A': round(B - A, 4),
            'D_minus_DPHASIC0': round(D - DP, 4),
            'D_minus_DTONIC0': round(D - DT, 4),
        }
        beats = D >= A + MARGIN
        if beats:
            wins.append(regime)
            if Df > Af:
                fab_ok = False
            if (DP < D - MARGIN) and (DT < D - MARGIN):
                ablation_separated_on_wins.append(regime)
        else:
            if D < A - 0.02:
                never_much_worse = False

    n_wins = len(wins)
    n_ablation_ok = len(ablation_separated_on_wins)
    # GREEN iff >=2 wins AND never_much_worse AND fab_ok AND ablations separated
    #   on EVERY win (n_ablation_ok == n_wins and n_wins>=2)
    if n_wins >= 2 and fab_ok and never_much_worse and n_ablation_ok == n_wins:
        verdict = 'GREEN'
    elif n_wins == 1:
        verdict = 'PARTIAL'
    elif n_wins >= 2 and n_ablation_ok < n_wins:
        verdict = 'PARTIAL'   # lift not attributable to the timescale split
    else:
        verdict = 'RED_NO_LUNCH'   # 0 wins — wall holds, Nth confirming lens

    summary['wins_over_A+MARGIN'] = wins
    summary['ablation_separated_on_wins'] = ablation_separated_on_wins
    summary['fab_ok'] = fab_ok
    summary['never_much_worse'] = never_much_worse
    summary['verdict'] = verdict
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
