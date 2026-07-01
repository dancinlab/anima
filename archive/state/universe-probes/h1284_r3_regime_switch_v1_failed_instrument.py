#!/usr/bin/env python3
"""
H_1284_R3 — NEUROMODULATION as REGIME / MODE SWITCHING (break the HD27 wall).

THE WALL (H_1284, kept 🧱): a context-adaptive GAIN controller never beats a
single well-tuned FIXED operating point — no free lunch, on memory AND ideation.

THE NEW ANGLE (a_break_the_wall, a_no_llm_frame_trap, c15): neuromodulation's
biological role is REGIME / MODE switching, not gain-scaling. ACh gates
ENCODE-vs-RECALL (Hasselmo): high-ACh = plasticity-on/encode & suppress readout;
low-ACh = consolidate/recall, read-only. A fixed operating point cannot serve an
environment that interleaves two regimes demanding OPPOSITE policies on the
write-on-cue axis. Test: a substrate-derived regime-SWITCHER (read write-pressure
surprise → gate writes_enabled) vs the BEST single FIXED policy.

Byte-faithful numpy mirror of CORE/engine_cli.hexa VAdaptField (host has no torch;
a_engine_native_learning DIRECTIONAL). p7 exact metric, no loss, no LLM judge.
Frozen falsifier in .verdicts/1284_r3_regime_switch/FREEZE.txt. $0 CPU, 3 seeds.

ARMS: A = best FIXED single policy (grid-search, incl. the discrete write-enable
knob). B = regime-SWITCHER (substrate write-pressure EMA → writes_enabled, A's
gains held fixed in both sub-modes). C = the H_1284 gain-tuner (continuity check).
"""
import numpy as np
import json, sys, os

# import the EXACT H_1284 substrate + gain-tuner (continuity: arm C is the wall's
# own controller, unchanged). Same directory.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h1284_neuromodulation_gain import (
    fnv1a, key_vec, MemStore, Neuromod, DIM, LR0_ENGINE, TH0_ENGINE,
)

# ── environment: interleaved ENCODE / RECALL stream (opposite-policy regimes) ──
def gen_regime_stream(facts, rng, n_blocks, block_len):
    """Alternating ENCODE / RECALL blocks in ONE stream.

    yields (kind, key_str, true_value, noise_sigma, regime)
      kind ∈ {'write', 'recall', 'recall_oos'}
      regime ∈ {'ENCODE', 'RECALL'}  (ground-truth label — METRIC/SHUFFLE only,
                                       NEVER fed to arm B's switch)

    ENCODE block: presents NEW or REWRITTEN facts as WRITE events (high surprise:
      brand-new or drifted keys). The correct policy is plasticity-ON.
    RECALL block: presents in-store subjects as RECALL queries (low surprise:
      noisy copies of stored keys) + a fraction of out-of-store GHOST probes
      (must ABSTAIN). The correct policy is read-only (no store mutation).
    """
    cur = {s: c for s, c in facts}     # current binding (drift rewrites it)
    subs = [s for s, _ in facts]
    ev = []
    # seed the store with an initial ENCODE block (write every fact once)
    for s in subs:
        ev.append(('write', s, cur[s], 0.0, 'ENCODE'))
    for blk in range(n_blocks):
        if blk % 2 == 0:
            # ── RECALL block: query stored facts (low surprise), no new content
            for _ in range(block_len):
                if rng.random() < 0.20:
                    ev.append(('recall_oos', f"ghost{rng.integers(0,99999):05d}",
                               None, 0.04, 'RECALL'))
                else:
                    s = subs[rng.integers(0, len(subs))]
                    ev.append(('recall', s, cur[s], 0.04, 'RECALL'))
        else:
            # ── ENCODE block: rewrite a subset of facts (concept drift) = new
            # high-surprise content that MUST be written, plus brand-new facts.
            for _ in range(block_len):
                if rng.random() < 0.5:
                    # rewrite an existing subject to a NEW value (drift)
                    s = subs[rng.integers(0, len(subs))]
                    cur[s] = f"city{rng.integers(0, 99999):05d}"
                    ev.append(('write', s, cur[s], 0.0, 'ENCODE'))
                else:
                    # interleave a recall of an already-stored fact so the ENCODE
                    # block is not write-only (realistic; the policy must still be
                    # plasticity-on so the drift gets stored for later recall)
                    s = subs[rng.integers(0, len(subs))]
                    ev.append(('recall', s, cur[s], 0.04, 'ENCODE'))
    return ev


# ── run one arm over the interleaved stream ───────────────────────────────────
# policy = how writes_enabled is decided per tick:
#   'fixed'   : writes_enabled = const FIXED_WRITES (arm A grid knob)
#   'switch'  : writes_enabled = substrate write-pressure EMA > running median
#   'switch_shuffle' : same as switch but EMA signal phase-scrambled (control)
#   'gain'    : H_1284 Neuromod continuous knobs, writes always enabled (arm C)
def run_arm(facts, events, rng, LR0, TH0, abstain0, policy,
            fixed_writes=True):
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)),
                     abstain_margin=abstain0)
    nm = Neuromod(LR0, TH0, abstain0) if policy == 'gain' else None
    n_recall = n_correct = n_fab = 0

    # ----- precompute the switch schedule (substrate write-pressure EMA) -------
    # For 'switch'/'switch_shuffle' we run a faithful first pass that mirrors the
    # store dynamics WITH writes enabled (the substrate must actually evolve to
    # produce surprise) and records the per-tick surprise EMA. Then writes_enabled
    # = (EMA_t > median(EMA up to t)). For shuffle, the EMA *series* is permuted in
    # time before thresholding (decorrelated from the true regime, same values).
    sched = None
    if policy in ('switch', 'switch_shuffle'):
        tmp = MemStore(max_cells=store.max_cells, abstain_margin=abstain0)
        EMA = TH0
        BETA = 0.15
        ema_series = []
        for kind, key, val, sig, regime in events:
            x = key_vec(key, rng) + rng.normal(0, sig, DIM)
            x = x / (np.linalg.norm(x) + 1e-9)
            _, err, _ = tmp._nearest(x)
            err = err if err < 1e8 else TH0
            EMA = (1 - BETA) * EMA + BETA * err
            ema_series.append(EMA)
            # the probe store always writes (so it tracks content) — only the
            # MAIN store's writes are gated; this probe just senses surprise.
            if kind == 'write':
                tmp.write(x, val, LR0, TH0)
        ema_series = np.array(ema_series)
        if policy == 'switch_shuffle':
            ema_series = ema_series[rng.permutation(len(ema_series))]
        # writes_enabled when surprise EMA above its self-running median
        # (self-calibrating threshold — no constant fed the true regime).
        sched = np.zeros(len(ema_series), dtype=bool)
        for t in range(len(ema_series)):
            med = np.median(ema_series[:t+1])
            sched[t] = ema_series[t] >= med

    # ----- main scored pass ----------------------------------------------------
    si = 0
    for kind, key, val, sig, regime in events:
        x = key_vec(key, rng) + rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)

        if policy == 'gain':
            _, err, _ = store._nearest(x)
            err = err if err < 1e8 else nm.TH0
            LR, TH, ab = nm.knobs(err)
            store.abstain_margin = ab
            writes_enabled = True            # gain-tuner always writes (H_1284)
        else:
            LR, TH = LR0, TH0
            store.abstain_margin = abstain0
            if policy == 'fixed':
                writes_enabled = fixed_writes
            else:                            # switch / switch_shuffle
                writes_enabled = bool(sched[si]); si += 1
            err = 0.0

        if kind == 'write':
            if writes_enabled:
                store.write(x, val, LR, TH)
            if policy == 'gain':
                nm.observe(err, 0.0)
            # if writes disabled on a write event, the new content is simply not
            # encoded — that is the COST of read-only mode if mis-applied to encode
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
            # CRITICAL regime axis: in plasticity-ON, a recall cue ALSO refines
            # the winner toward the (noisy) cue — this is the corruption channel.
            if writes_enabled and pred is not None:
                # write-on-recall: refine winner toward noisy cue (corrupts clean
                # binding under capacity pressure — the read-only mode avoids this)
                store.write(x, val if kind != 'recall_oos' else val, LR, TH)
            if policy == 'gain':
                nm.observe(rerr if rerr < 1e8 else nm.TH0, reward)

    acc = n_correct / max(1, n_recall)
    fab = n_fab / max(1, n_recall)
    return acc, fab, acc - fab


def make_facts(n_facts, rng):
    facts = []
    for i in range(n_facts):
        facts.append((f"subj{i:03d}", f"city{rng.integers(0, 99999):05d}"))
    return facts


def grid_tune(n_facts, tune_seed, n_blocks, block_len, abstain0):
    """ARM A: best FIXED (writes_enabled, LR0, TH0) on a DISJOINT tuning seed.
    The discrete write-enable knob is INCLUDED so the fixed baseline gets to pick
    its single best mode (strongest honest fixed point)."""
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

    per_seed = {'A': [], 'B': [], 'B_shuf': [], 'C': [],
                'A_fab': [], 'B_fab': [], 'C_fab': []}
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

        per_seed['A'].append(a_cap); per_seed['A_fab'].append(a_fab)
        per_seed['B'].append(b_cap); per_seed['B_fab'].append(b_fab)
        per_seed['B_shuf'].append(s_cap)
        per_seed['C'].append(c_cap); per_seed['C_fab'].append(c_fab)

    A = float(np.mean(per_seed['A']))
    B = float(np.mean(per_seed['B']))
    Bs = float(np.mean(per_seed['B_shuf']))
    C = float(np.mean(per_seed['C']))

    # per-seed B−A margins (c1 = EVERY seed ≥ MARGIN)
    margins_BA = [round(b - a, 4) for a, b in zip(per_seed['A'], per_seed['B'])]
    c1 = all(m >= MARGIN for m in margins_BA)
    # c2 shuffle collapses: B_shuffle ≤ A + MARGIN (mean)
    c2 = Bs <= A + MARGIN
    # c3 continuity: gain-tuner C does NOT clear bar (mean)
    c3 = C < A + MARGIN

    if c1 and c2 and c3:
        verdict = 'GREEN'      # wall BROKEN: value of neuromod = regime-switching
    elif c1 and not c2:
        verdict = 'RED_CONFOUND'   # lift not regime-tracking (shuffle survived)
    elif not c1:
        verdict = 'RED_NO_LUNCH'   # switcher sub-bar: no-free-lunch generalizes
    else:
        verdict = 'PARTIAL'

    summary = {
        'best_fixed': {'writes_enabled': bool(fw_star), 'LR0': LR0_star,
                       'TH0': TH0_star, 'tune_cap': round(tune_cap, 4)},
        'seeds': SCORE_SEEDS, 'MARGIN': MARGIN,
        'A_cap_mean': round(A, 4), 'B_cap_mean': round(B, 4),
        'B_shuffle_cap_mean': round(Bs, 4), 'C_gain_cap_mean': round(C, 4),
        'per_seed_A': [round(v, 4) for v in per_seed['A']],
        'per_seed_B': [round(v, 4) for v in per_seed['B']],
        'per_seed_B_shuffle': [round(v, 4) for v in per_seed['B_shuf']],
        'per_seed_C_gain': [round(v, 4) for v in per_seed['C']],
        'per_seed_B_minus_A': margins_BA,
        'B_minus_A_mean': round(B - A, 4),
        'B_minus_Bshuffle_mean': round(B - Bs, 4),
        'C_minus_A_mean': round(C - A, 4),
        'A_fab_mean': round(float(np.mean(per_seed['A_fab'])), 4),
        'B_fab_mean': round(float(np.mean(per_seed['B_fab'])), 4),
        'c1_B_beats_A_every_seed': bool(c1),
        'c2_shuffle_collapses': bool(c2),
        'c3_gain_tuner_loses': bool(c3),
        'verdict': verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
