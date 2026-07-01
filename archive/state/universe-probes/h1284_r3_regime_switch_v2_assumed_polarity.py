#!/usr/bin/env python3
"""
H_1284_R3 — NEUROMODULATION as REGIME / MODE SWITCHING (break the HD27 wall).

THE WALL (H_1284, kept 🧱): a context-adaptive GAIN controller never beats a
single well-tuned FIXED operating point — no free lunch, on memory AND ideation.

THE NEW ANGLE (a_break_the_wall, a_no_llm_frame_trap, c15): neuromodulation's
biological role is REGIME / MODE switching, not gain-scaling. ACh gates
ENCODE-vs-RECALL (Hasselmo): high-ACh = plasticity-on/encode & suppress readout;
low-ACh = consolidate/recall, read-only. Build an environment that interleaves
two regimes demanding OPPOSITE policies on the write-on-cue axis, so NO single
fixed policy can win, and test whether a substrate-derived regime-SWITCHER beats
the BEST single FIXED policy.

VALIDATED opposite-policy crossover (the v1 instrument failed to deliver this;
see .verdicts/1284_r3_regime_switch/result_v1_failed_instrument.txt):
  ENCODE (drift rewrites): plasticity-ON beats OFF (must write to learn new value)
  RECALL (noisy cues, tight capacity): plasticity-OFF beats ON — writing on a
    noisy recall cue SPLITS a spurious cell that LRU-evicts a real fact (the
    H_1230 self-inflicted-forgetting mode). Recall-noise 0.10 + max_cells make
    the corruption channel actually bite.

Byte-faithful numpy mirror of CORE/engine_cli.hexa VAdaptField (host has no torch;
a_engine_native_learning DIRECTIONAL). p7 exact metric, no loss, no LLM judge.
Frozen falsifier in .verdicts/1284_r3_regime_switch/FREEZE.txt. $0 CPU, 3 seeds.

ARMS: A = best FIXED single policy (grid-search, incl. the discrete write-enable
knob). B = regime-SWITCHER (substrate write-pressure EMA → writes_enabled, A's
gains held fixed in both sub-modes). C = the H_1284 gain-tuner (continuity check).
"""
import numpy as np
import json, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h1284_neuromodulation_gain import (
    fnv1a, key_vec, MemStore, Neuromod, DIM, LR0_ENGINE, TH0_ENGINE,
)

# ── tuned-to-realize-the-regimes environment constants (NOT falsifier bars) ───
RECALL_NOISE = 0.10        # noisy recall cues — high enough that write-on-recall
                           # corrupts (validated crossover; see result_v1 note)
ENCODE_NOISE = 0.0         # clean writes during encode
MAX_CELLS_FRAC = 0.6       # capacity-bounded store (max_cells < #facts)


def make_facts(n_facts, rng):
    return [(f"subj{i:03d}", f"city{rng.integers(0, 99999):05d}")
            for i in range(n_facts)]


def gen_regime_stream(facts, rng, n_blocks, block_len):
    """Alternating ENCODE / RECALL blocks in ONE interleaved stream.

    yields (kind, key_str, true_value, noise_sigma, regime)
      regime ∈ {'ENCODE','RECALL'} is GROUND TRUTH — METRIC/SHUFFLE only, NEVER
      fed to arm B's switch.

    RECALL block: query in-store subjects with NOISY cues (σ=RECALL_NOISE) +
      out-of-store GHOST probes (must ABSTAIN). Correct policy = read-only:
      a noisy recall cue, if written, splits a spurious cell that LRU-evicts a
      real fact (corruption). Low substrate surprise (cues are near stored cells).
    ENCODE block: rewrite a subset of facts to NEW values (concept drift) =
      high-surprise content that MUST be written (plasticity-on) to be recalled
      later. Brand-new high recon-error keys.
    """
    cur = {s: c for s, c in facts}
    subs = [s for s, _ in facts]
    ev = []
    # initial ENCODE: write every fact once (seed the store)
    for s in subs:
        ev.append(('write', s, cur[s], ENCODE_NOISE, 'ENCODE'))
    for blk in range(n_blocks):
        if blk % 2 == 0:
            # RECALL block (read-only is correct)
            for _ in range(block_len):
                if rng.random() < 0.20:
                    ev.append(('recall_oos', f"ghost{rng.integers(0,99999):05d}",
                               None, RECALL_NOISE, 'RECALL'))
                else:
                    s = subs[rng.integers(0, len(subs))]
                    ev.append(('recall', s, cur[s], RECALL_NOISE, 'RECALL'))
        else:
            # ENCODE block (plasticity-on is correct): rewrite facts to new values
            for _ in range(block_len):
                s = subs[rng.integers(0, len(subs))]
                cur[s] = f"city{rng.integers(0, 99999):05d}"
                ev.append(('write', s, cur[s], ENCODE_NOISE, 'ENCODE'))
    return ev


def run_arm(facts, events, rng, LR0, TH0, abstain0, policy, fixed_writes=True):
    """policy ∈ {'fixed','switch','switch_shuffle','gain'}.
    write-on-cue corruption: when writes_enabled, a RECALL event ALSO writes the
    noisy cue back (Hasselmo: plasticity-on does not gate out recall-driven
    encoding) — this is the channel that corrupts the store in RECALL regime."""
    store = MemStore(max_cells=max(4, int(len(facts) * MAX_CELLS_FRAC)),
                     abstain_margin=abstain0)
    nm = Neuromod(LR0, TH0, abstain0) if policy == 'gain' else None
    n_recall = n_correct = n_fab = 0

    # ----- switch schedule: substrate write-pressure EMA (no regime label) -----
    sched = None
    if policy in ('switch', 'switch_shuffle'):
        tmp = MemStore(max_cells=store.max_cells, abstain_margin=abstain0)
        EMA = TH0; BETA = 0.15; ema_series = []
        for kind, key, val, sig, regime in events:
            x = key_vec(key, rng) + rng.normal(0, sig, DIM)
            x = x / (np.linalg.norm(x) + 1e-9)
            _, err, _ = tmp._nearest(x)
            err = err if err < 1e8 else TH0
            EMA = (1 - BETA) * EMA + BETA * err
            ema_series.append(EMA)
            if kind == 'write':
                tmp.write(x, val, LR0, TH0)
        ema_series = np.array(ema_series)
        if policy == 'switch_shuffle':
            ema_series = ema_series[rng.permutation(len(ema_series))]
        sched = np.zeros(len(ema_series), dtype=bool)
        for t in range(len(ema_series)):
            sched[t] = ema_series[t] >= np.median(ema_series[:t+1])

    si = 0
    for kind, key, val, sig, regime in events:
        x = key_vec(key, rng) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)

        if policy == 'gain':
            _, err, _ = store._nearest(x)
            err = err if err < 1e8 else nm.TH0
            LR, TH, ab = nm.knobs(err)
            store.abstain_margin = ab
            writes_enabled = True
        else:
            LR, TH = LR0, TH0
            store.abstain_margin = abstain0
            if policy == 'fixed':
                writes_enabled = fixed_writes
            else:
                writes_enabled = bool(sched[si]); si += 1
            err = 0.0

        if kind == 'write':
            if writes_enabled:
                store.write(x, val, LR, TH)
            if policy == 'gain':
                nm.observe(err, 0.0)
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
            # CORRUPTION CHANNEL: plasticity-on writes the noisy recall cue back.
            # On an in-store recall the noisy cue can exceed TH and SPLIT a
            # spurious duplicate → LRU-evicts a real fact (RECALL-regime damage).
            if writes_enabled and kind == 'recall':
                store.write(x, val, LR, TH)
            if policy == 'gain':
                nm.observe(rerr if rerr < 1e8 else nm.TH0, reward)

    acc = n_correct / max(1, n_recall)
    fab = n_fab / max(1, n_recall)
    return acc, fab, acc - fab


def grid_tune(n_facts, tune_seed, n_blocks, block_len, abstain0):
    """ARM A: best FIXED (writes_enabled, LR0, TH0) on a DISJOINT tuning seed.
    The discrete write-enable knob is INCLUDED so the fixed baseline picks its
    single best mode (strongest honest fixed point)."""
    best = None
    for fixed_writes in (True, False):
        for LR0 in (0.1, 0.2, 0.3, 0.4):
            for TH0 in (0.2, 0.3, 0.4):
                rng = np.random.default_rng(tune_seed)
                facts = make_facts(n_facts, rng)
                ev = gen_regime_stream(facts, rng, n_blocks, block_len)
                _, _, cap = run_arm(facts, ev, np.random.default_rng(tune_seed),
                                    LR0, TH0, abstain0, policy='fixed',
                                    fixed_writes=fixed_writes)
                if best is None or cap > best[0]:
                    best = (cap, fixed_writes, LR0, TH0)
    return best[1], best[2], best[3], best[0]


def main():
    N_FACTS = 30
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    N_BLOCKS = 12
    BLOCK_LEN = 25
    MARGIN = 0.05

    fw_star, LR0_star, TH0_star, tune_cap = grid_tune(
        N_FACTS, TUNE_SEED, N_BLOCKS, BLOCK_LEN, ABSTAIN0)

    per = {k: [] for k in ('A', 'B', 'B_shuf', 'C', 'A_fab', 'B_fab', 'C_fab')}
    for seed in SCORE_SEEDS:
        rng_facts = np.random.default_rng(seed)
        facts = make_facts(N_FACTS, rng_facts)
        ev = gen_regime_stream(facts, rng_facts, N_BLOCKS, BLOCK_LEN)

        a_acc, a_fab, a_cap = run_arm(facts, ev, np.random.default_rng(seed),
            LR0_star, TH0_star, ABSTAIN0, policy='fixed', fixed_writes=fw_star)
        b_acc, b_fab, b_cap = run_arm(facts, ev, np.random.default_rng(seed),
            LR0_star, TH0_star, ABSTAIN0, policy='switch')
        s_acc, s_fab, s_cap = run_arm(facts, ev, np.random.default_rng(seed),
            LR0_star, TH0_star, ABSTAIN0, policy='switch_shuffle')
        c_acc, c_fab, c_cap = run_arm(facts, ev, np.random.default_rng(seed),
            LR0_star, TH0_star, ABSTAIN0, policy='gain')

        per['A'].append(a_cap); per['A_fab'].append(a_fab)
        per['B'].append(b_cap); per['B_fab'].append(b_fab)
        per['B_shuf'].append(s_cap)
        per['C'].append(c_cap); per['C_fab'].append(c_fab)

    A = float(np.mean(per['A'])); B = float(np.mean(per['B']))
    Bs = float(np.mean(per['B_shuf'])); C = float(np.mean(per['C']))

    margins_BA = [round(b - a, 4) for a, b in zip(per['A'], per['B'])]
    c1 = all(m >= MARGIN for m in margins_BA)
    c2 = Bs <= A + MARGIN
    c3 = C < A + MARGIN

    if c1 and c2 and c3:
        verdict = 'GREEN'
    elif c1 and not c2:
        verdict = 'RED_CONFOUND'
    elif not c1:
        verdict = 'RED_NO_LUNCH'
    else:
        verdict = 'PARTIAL'

    summary = {
        'best_fixed': {'writes_enabled': bool(fw_star), 'LR0': LR0_star,
                       'TH0': TH0_star, 'tune_cap': round(tune_cap, 4)},
        'env': {'recall_noise': RECALL_NOISE, 'max_cells_frac': MAX_CELLS_FRAC,
                'n_blocks': N_BLOCKS, 'block_len': BLOCK_LEN},
        'seeds': SCORE_SEEDS, 'MARGIN': MARGIN,
        'A_cap_mean': round(A, 4), 'B_cap_mean': round(B, 4),
        'B_shuffle_cap_mean': round(Bs, 4), 'C_gain_cap_mean': round(C, 4),
        'per_seed_A': [round(v, 4) for v in per['A']],
        'per_seed_B': [round(v, 4) for v in per['B']],
        'per_seed_B_shuffle': [round(v, 4) for v in per['B_shuf']],
        'per_seed_C_gain': [round(v, 4) for v in per['C']],
        'per_seed_B_minus_A': margins_BA,
        'B_minus_A_mean': round(B - A, 4),
        'B_minus_Bshuffle_mean': round(B - Bs, 4),
        'C_minus_A_mean': round(C - A, 4),
        'A_fab_mean': round(float(np.mean(per['A_fab'])), 4),
        'B_fab_mean': round(float(np.mean(per['B_fab'])), 4),
        'c1_B_beats_A_every_seed': bool(c1),
        'c2_shuffle_collapses': bool(c2),
        'c3_gain_tuner_loses': bool(c3),
        'verdict': verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
