#!/usr/bin/env python3
"""
H_1545 — SEROTONIN × CLS: adaptive consolidation TIMING (when to replay fast→slow).

FUSION of two prior lanes (a_no_llm_frame_trap — biological structure first):
  • H_1532 🟢 (PR #2522) MULTI-STORE / Complementary Learning Systems broke the H_1284
    neuromodulation wall on AB-AC interference: TWO phase-separated stores (a FAST
    episodic store written in Hasselmo encode-mode + a SLOW store fed by interleaved
    REPLAY) keep confusable A->B / A->C bindings in separate substrates. The win is
    HAVING SEPARATE STORES — but in H_1532 the consolidation sweep (fast→slow replay)
    fired ONCE, unconditionally, at the end of the stream.
  • H_1538 🟠 (#2519) / H_1540 🟠 (#2523) SEROTONIN-AS-PATIENCE: a substrate-adaptive
    5-HT discount/horizon read was PRESENT + EARNED as an emit-timing faculty, but a
    FIXED γ already captured the MAJORITY of the value (H_1538 ~49%, H_1540 ~94% under
    a regime-shifting horizon). 5-HT-adaptive stayed a MINORITY lever because a SINGLE
    store with ONE value-arrival timescale gave a fixed schedule almost no room.

THE STRUCTURE-REOPEN (this hypothesis): put 5-HT where it has a real EVENT TO TIME.
In CLS, 5-HT controls WHEN to trigger a consolidation sweep (fast→slow replay), not how
patiently to emit. The fast episodic store has FINITE capacity; it accumulates new
bindings and EVICTS the least-recently-used when full (the H_1532 MemStore LRU eviction,
byte-reused). So:
  • consolidate TOO EARLY  → the fast store hasn't accumulated enough to have laid the
    confusable A->B in a fresh cell yet; replaying a half-formed store wastes the sweep.
  • consolidate TOO LATE   → the fast store OVERFLOWS; LRU eviction drops the old A->B
    cell before it is ever replayed into the slow store → the binding is lost forever.
The RIGHT consolidation timing is CONTEXT-DEPENDENT: a stream segment with DENSE AB-AC
collisions floods the fast store fast and needs an EARLY sweep (before eviction eats the
old binding); a SPARSE segment can wait. A single FIXED replay period cannot serve both —
it is too eager in sparse regions (wastes sweeps) and too lazy in dense regions (loses
bindings to eviction). The 5-HT signal = the fast-store INTERFERENCE PRESSURE (how close
to overflow / how many colliding keys are queued); a substrate-gated threshold on that
pressure triggers the sweep adaptively. Doya 2002 (5-HT sets the reward-integration
TIME-SCALE — here the consolidation time-scale); Lisman 2017 (consolidation TIMING gates
what survives systems consolidation). This is the condition H_1538/H_1540 lacked: a
genuine timing event whose optimum SHIFTS with context, so the adaptive 5-HT slope should
now be the MAJORITY lever.

p7: exact ground truth (the true A->B binding is known); NO LLM judge, NO perplexity, NO
loss term — every read is a no-grad read of substrate state. p8: inference-time write =
the engine's own tick. $0 CPU, 3 seeds, frozen falsifier in H_1545_FREEZE.txt.

R1 numpy DIRECTIONAL (host has no torch; a_engine_native_learning: grep numpy ⇒ auto-
DIRECTIONAL) — engine §Ht5Timing R2 deferred ING. REUSES the H_1532 store machinery
(MemStore / key_vec / FNV-1a / suppress_retrieval encode-mode / LRU eviction) byte-exact.
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / CORE/engine_cli.hexa) ─────
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 16                   # key dim (H_1227 byte-trigram FNV-1a; toy 16, same as H_1532)
MARGIN = 0.05              # frozen lift bar (same as H_1532 / H_1284)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532) ────────────────────────────
def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


def key_vec(s: str) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (VERBATIM from H_1532)."""
    bs = s.encode()
    v = np.zeros(DIM)
    for i in range(len(bs) - 2):
        tri = bs[i:i+3]
        idx = fnv1a(tri) % DIM
        v[idx] += 1.0
    n = np.linalg.norm(v)
    if n < 1e-9:
        v = np.zeros(DIM); v[fnv1a(bs) % DIM] = 1.0; n = 1.0
    return v / n


# ── MemStore (VERBATIM from H_1532 — finite-capacity LRU prototype store) ─────
# A capacity-bounded prototype store: a write SPLITs a new cell (novel key, recon-err>
# THRESH, capacity free), REFINEs the winner toward the key (LR pull, REBINDING its
# value = interference), or — when full — EVICTS the least-recently-used cell. The LRU
# eviction is THE timing hazard this hypothesis exploits: a binding the fast store has
# not yet replayed into the slow store can be EVICTED if consolidation comes too late.
class MemStore:
    def __init__(self, max_cells, abstain_margin, LR, THRESH):
        self.protos = []
        self.values = []
        self.lru = []
        self.max_cells = max_cells
        self.abstain_margin = abstain_margin
        self.LR = LR
        self.THRESH = THRESH
        self.tick = 0

    def _nearest(self, x):
        if not self.protos:
            return -1, 1e9, 1e9
        d = [np.linalg.norm(p - x) for p in self.protos]
        order = np.argsort(d)
        win = int(order[0]); bestd = d[win]
        second = d[int(order[1])] if len(d) > 1 else 1e9
        return win, bestd, second

    def write(self, x, value, suppress_retrieval=False):
        """vadapt_field_step write (VERBATIM H_1532). suppress_retrieval = Hasselmo ACh
        encode-mode: lay a fact in a FRESH cell instead of refining/overwriting the
        winner it would otherwise match (the phase-separation mechanism)."""
        self.tick += 1
        win, err, _ = self._nearest(x)
        if suppress_retrieval and len(self.protos) < self.max_cells:
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick)
            return
        if win < 0 or (err > self.THRESH and len(self.protos) < self.max_cells):
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick)
            return
        if err > self.THRESH and len(self.protos) >= self.max_cells:
            ev = int(np.argmin(self.lru))               # LRU EVICTION (the timing hazard)
            self.protos[ev] = x.copy(); self.values[ev] = value
            self.lru[ev] = self.tick
            return
        # REFINE: pull winner toward x, OVERWRITE its bound value (= interference)
        self.protos[win] = self.protos[win] + self.LR * (x - self.protos[win])
        self.values[win] = value
        self.lru[win] = self.tick

    def write_encode_evictable(self, x, value):
        """Fast-store encode write that STILL respects capacity: lay a fresh cell when
        room, else EVICT the LRU cell (this is what makes 'too-late consolidation' lose
        the old A->B binding — the fast store cannot grow without bound)."""
        self.tick += 1
        if len(self.protos) < self.max_cells:
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick)
            return
        ev = int(np.argmin(self.lru))                   # full → evict oldest unreplayed cell
        self.protos[ev] = x.copy(); self.values[ev] = value
        self.lru[ev] = self.tick

    def recall(self, x):
        self.tick += 1
        win, err, second = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None, err, second
        self.lru[win] = self.tick
        return self.values[win], err, second

    def pressure(self):
        """Fast-store INTERFERENCE PRESSURE = fill fraction (the 5-HT substrate read).
        Near 1.0 the next encode write will EVICT an unreplayed binding → sweep NOW."""
        return len(self.protos) / max(1, self.max_cells)


# ── varying-interference-density stream ───────────────────────────────────────
def make_stream(n_segments, rng):
    """A stream of SEGMENTS, each an AB-AC interference burst, with VARYING density.
    DENSE segments pack many colliding A->B / A->C pairs (flood the fast store fast →
    need an EARLY sweep); SPARSE segments have few (can wait). Each segment yields an
    ordered event list; the ground-truth A->B bindings (to retain) are accumulated.

    An event = ('AB', key, B) writes the OLD binding into the fast episodic store;
    ('AC', key, C) is the later interfering re-binding routed to the slow store;
    ('D', key, D) is an unrelated distractor (also slow-store)."""
    events = []
    truth = []          # list of (key, B) we must still retain at the end
    seg_meta = []
    for _ in range(n_segments):
        dense = (rng.uniform() < 0.5)
        n_pairs = int(rng.integers(8, 12)) if dense else int(rng.integers(1, 3))
        n_dist = int(rng.integers(0, 2)) if dense else int(rng.integers(2, 5))
        seg_meta.append(('DENSE' if dense else 'SPARSE', n_pairs, n_dist))
        seg_events = []
        for i in range(n_pairs):
            k = f"key_{len(truth):04d}"
            B = f"val_B{rng.integers(0, 99999):05d}"
            C = f"val_C{rng.integers(0, 99999):05d}"
            while C == B:
                C = f"val_C{rng.integers(0, 99999):05d}"
            seg_events.append(('AB', k, B))             # phase-1 binding (to retain)
            seg_events.append(('AC', k, C))             # phase-2 interfering re-binding
            truth.append((k, B))
        for _ in range(n_dist):
            dk = f"keyD_{rng.integers(0, 99999):05d}"
            dv = f"val_D{rng.integers(0, 99999):05d}"
            seg_events.append(('D', dk, dv))
        events.append(seg_event_order(seg_events, rng))
    return events, truth, seg_meta


def seg_event_order(seg_events, rng):
    """Within a segment, emit all AB writes first (encode), then the AC/D interference —
    the AB-AC ordering H_1532 uses (A->B before A->C). Distractors interleave with AC."""
    ab = [e for e in seg_events if e[0] == 'AB']
    rest = [e for e in seg_events if e[0] != 'AB']
    rng.shuffle(rest)
    return ab + rest


# ── CLS engine with consolidation-timing control ──────────────────────────────
def run_cls(events, truth, max_cells_fast, max_cells_slow, LR, THRESH, abstain,
            sweep_policy, sweep_arg, rng=None, ablate_const=False, shuffle_pressure=False):
    """One pass over the event stream with a CONSOLIDATION-TIMING policy.

    fast  = FAST episodic store (finite, LRU-evicting): AB bindings encode here.
    slow  = SLOW store: AC re-bindings + distractors (interfering writes) land here.
    A consolidation SWEEP replays every fast-store binding into the slow store (encode-
    mode, fresh cells) and then CLEARS the swept cells from fast (they are consolidated),
    freeing capacity. If a sweep does not fire before the fast store overflows, the LRU
    cell (an un-replayed A->B) is EVICTED and lost.

    sweep_policy:
      'adaptive' : 5-HT — sweep when fast pressure() crosses a substrate-gated threshold
                   sweep_arg (∈[0,1]); dense bursts hit it early, sparse never → adaptive.
      'fixed'    : sweep every sweep_arg events (a single fixed consolidation period).
      'early'    : fixed, very short period (aggressive).
      'late'     : fixed, very long period (lazy).
    ablate_const=True : force the adaptive threshold to a CONSTANT (==best fixed period
                  behaviour) → reverts to a fixed schedule (the bar-C ablation).
    shuffle_pressure=True : permute the pressure SIGNAL the gate reads → the trigger
                  fires at meaningless times (the bar-D control)."""
    fast = MemStore(max_cells_fast, abstain, LR, THRESH)
    slow = MemStore(max_cells_slow, abstain, LR, THRESH)
    n_since_sweep = 0
    ev_count = 0
    fake_pressure_seq = None
    if shuffle_pressure and rng is not None:
        # a fixed permuted pressure trace the gate reads instead of the real fill
        flat = [e for seg in events for e in seg]
        fake_pressure_seq = rng.uniform(0.0, 1.0, size=len(flat)).tolist()

    def do_sweep():
        # CLS replay: re-present every fast-store binding into the slow store (encode-
        # mode, fresh cell), then clear fast (consolidated → capacity freed).
        for proto, val in zip(fast.protos, fast.values):
            slow.write(proto, val, suppress_retrieval=True)
        fast.protos.clear(); fast.values.clear(); fast.lru.clear()

    for seg in events:
        for ev in seg:
            tag, k, val = ev
            kv = key_vec(k)
            if tag == 'AB':
                fast.write_encode_evictable(kv, val)    # episodic encode (evictable!)
            else:                                       # 'AC' / 'D' → slow interfering write
                slow.write(kv, val, suppress_retrieval=False)
            n_since_sweep += 1

            # ── consolidation-timing decision ──
            trigger = False
            if sweep_policy == 'adaptive':
                if ablate_const:
                    # ablation: ignore pressure, sweep on a FIXED count (== best fixed)
                    trigger = (n_since_sweep >= sweep_arg)
                else:
                    p = fast.pressure()
                    if shuffle_pressure:
                        p = fake_pressure_seq[ev_count]
                    trigger = (p >= sweep_arg)          # 5-HT substrate-gated threshold
            else:  # 'fixed' / 'early' / 'late' — a single fixed period
                trigger = (n_since_sweep >= sweep_arg)

            if trigger and fast.protos:
                do_sweep()
                n_since_sweep = 0
            ev_count += 1

    # final flush of whatever remains in fast (end-of-stream consolidation, all arms)
    if fast.protos:
        do_sweep()
    return _score(fast, slow, truth)


def _score(fast, slow, truth):
    """A->B retained if EITHER store still returns B (CLS: confusable bindings live in
    separate substrates). Eviction / overwrite / abstain all count as NOT retained."""
    correct = 0
    for k, B in truth:
        kv = key_vec(k)
        pf, _, _ = fast.recall(kv)
        ps, _, _ = slow.recall(kv)
        if pf == B or ps == B:
            correct += 1
    return correct / max(1, len(truth))


def grid_tune_fixed(n_segments, tune_seed, mcf, mcs, LR, THRESH, abstain):
    """BEST-FIXED-SCHEDULE: the strongest single fixed consolidation period over a grid
    (anti-confound — adaptive must beat the best honest fixed schedule, NOT a strawman).
    Also returns the WORST fixed for the earned-majority gap (bar B)."""
    rng = np.random.default_rng(tune_seed)
    events, truth, _ = make_stream(n_segments, rng)
    results = {}
    for period in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32):
        r = run_cls(events, truth, mcf, mcs, LR, THRESH, abstain,
                    sweep_policy='fixed', sweep_arg=period)
        results[period] = r
    best_period = max(results, key=results.get)
    worst_period = min(results, key=results.get)
    return best_period, results[best_period], worst_period, results[worst_period], results


def grid_tune_threshold(n_segments, tune_seed, mcf, mcs, LR, THRESH, abstain):
    """Tune the 5-HT pressure threshold on the DISJOINT tune seed (the adaptive arm gets
    the SAME honest grid-tune budget as the fixed baseline — no asymmetry)."""
    rng = np.random.default_rng(tune_seed)
    events, truth, _ = make_stream(n_segments, rng)
    best = None
    for thr in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
        r = run_cls(events, truth, mcf, mcs, LR, THRESH, abstain,
                    sweep_policy='adaptive', sweep_arg=thr)
        if best is None or r > best[1]:
            best = (thr, r)
    return best[0]


def main():
    N_SEGMENTS = 16
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    LR_star, TH_star = LR0_ENGINE, TH0_ENGINE
    # FAST store deliberately SMALL (the capacity that makes timing matter — a dense
    # burst overflows it, forcing eviction unless a sweep frees capacity in time).
    MAX_CELLS_FAST = 8
    MAX_CELLS_SLOW = 256          # ample slow capacity (interference, not slow capacity, is the test)

    # grid-tune the fixed baseline AND the adaptive threshold on a DISJOINT seed
    best_period, best_fixed_tune, worst_period, worst_fixed_tune, fixed_grid = \
        grid_tune_fixed(N_SEGMENTS, TUNE_SEED, MAX_CELLS_FAST, MAX_CELLS_SLOW,
                        LR_star, TH_star, ABSTAIN0)
    thr_star = grid_tune_threshold(N_SEGMENTS, TUNE_SEED, MAX_CELLS_FAST, MAX_CELLS_SLOW,
                                   LR_star, TH_star, ABSTAIN0)

    rows = []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        events, truth, seg_meta = make_stream(N_SEGMENTS, rng)
        adaptive = run_cls(events, truth, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                           ABSTAIN0, sweep_policy='adaptive', sweep_arg=thr_star)
        fixed_best = run_cls(events, truth, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                             ABSTAIN0, sweep_policy='fixed', sweep_arg=best_period)
        fixed_early = run_cls(events, truth, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                              ABSTAIN0, sweep_policy='fixed', sweep_arg=1)
        fixed_late = run_cls(events, truth, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                             ABSTAIN0, sweep_policy='fixed', sweep_arg=32)
        # bar-C ablation: adaptive threshold frozen to a CONSTANT count (best fixed period)
        abl = run_cls(events, truth, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                      ABSTAIN0, sweep_policy='adaptive', sweep_arg=best_period,
                      ablate_const=True)
        # bar-D shuffle: pressure SIGNAL permuted → trigger fires at meaningless times
        shf = run_cls(events, truth, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                      ABSTAIN0, sweep_policy='adaptive', sweep_arg=thr_star,
                      shuffle_pressure=True, rng=np.random.default_rng(seed + 1000))
        worst_fixed = run_cls(events, truth, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                              ABSTAIN0, sweep_policy='fixed', sweep_arg=worst_period)
        rows.append({'seed': seed,
                     'adaptive': round(adaptive, 4),
                     'fixed_best': round(fixed_best, 4),
                     'fixed_early': round(fixed_early, 4),
                     'fixed_late': round(fixed_late, 4),
                     'worst_fixed': round(worst_fixed, 4),
                     'abl_const': round(abl, 4),
                     'shuffle': round(shf, 4),
                     'adaptive_minus_best': round(adaptive - fixed_best, 4),
                     'n_dense': sum(1 for m in seg_meta if m[0] == 'DENSE')})

    def m(key):
        return float(np.mean([r[key] for r in rows]))
    ad_m = m('adaptive'); bf_m = m('fixed_best'); fe_m = m('fixed_early')
    fl_m = m('fixed_late'); wf_m = m('worst_fixed'); abl_m = m('abl_const'); shf_m = m('shuffle')

    # ── FROZEN falsifier (pre-registered in H_1545_FREEZE.txt) ────────────────
    #   A PRESENCE       : adaptive − best-fixed ≥ +MARGIN on ≥2/3 seeds AND in mean
    #   B EARNED-MAJORITY: adaptive − best-fixed ≥ 0.5×(adaptive − worst-fixed)   (the bar
    #                      H_1538/H_1540 MISSED — adaptive must now carry the MAJORITY of
    #                      the timing value, not a minority a fixed schedule already has)
    #   C ABL→fixed      : const-threshold ablation reverts toward best-fixed
    #                      (adaptive − abl ≥ MARGIN  AND  |abl − best_fixed| < MARGIN)
    #   D SHUFFLE        : permuted-pressure trigger collapses (adaptive − shuffle ≥ MARGIN)
    #   E NO-FAB         : best-fixed itself is a real working baseline (> 0), so the lift
    #                      is timing, not a broken control (sanity, not pass-rigging)
    seed_wins = sum(1 for r in rows if r['adaptive_minus_best'] >= MARGIN)
    presence = (seed_wins >= 2) and ((ad_m - bf_m) >= MARGIN)
    full_gap = ad_m - wf_m
    earned_majority = (ad_m - bf_m) >= 0.5 * full_gap and full_gap > 0
    abl_reverts = ((ad_m - abl_m) >= MARGIN) and (abs(abl_m - bf_m) < MARGIN)
    shuffle_collapses = (ad_m - shf_m) >= MARGIN
    no_fab = bf_m > 0.0

    if presence and earned_majority and abl_reverts and shuffle_collapses and no_fab:
        verdict = 'GREEN'      # 5-HT timing is load-bearing AND the majority lever
    elif presence and abl_reverts and shuffle_collapses and no_fab and not earned_majority:
        verdict = 'AMBER'      # adaptive present+earned but fixed still ≥half (honest)
    elif presence:
        verdict = 'AMBIGUOUS_ABLATION'
    else:
        verdict = 'WALL_HOLDS'

    frac_adaptive = (100 * (ad_m - bf_m) / full_gap) if full_gap > 0 else float('nan')

    summary = {
        'hypothesis': 'H_1545',
        'name': 'serotonin × CLS — adaptive consolidation timing (when to replay fast→slow)',
        'capability': 'AB-AC retention on a VARYING-interference-density stream via 5-HT-gated sweep timing',
        'LR_star': LR_star, 'TH_star': TH_star,
        'N_SEGMENTS': N_SEGMENTS, 'MAX_CELLS_FAST': MAX_CELLS_FAST, 'MAX_CELLS_SLOW': MAX_CELLS_SLOW,
        'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
        'best_fixed_period': best_period, 'worst_fixed_period': worst_period,
        'adaptive_threshold_star': thr_star,
        'fixed_grid_tune': {str(k): round(v, 4) for k, v in fixed_grid.items()},
        'per_seed': rows,
        'adaptive_mean': round(ad_m, 4),
        'fixed_best_mean': round(bf_m, 4),
        'fixed_early_mean': round(fe_m, 4),
        'fixed_late_mean': round(fl_m, 4),
        'worst_fixed_mean': round(wf_m, 4),
        'abl_const_mean': round(abl_m, 4),
        'shuffle_mean': round(shf_m, 4),
        'adaptive_minus_best_mean': round(ad_m - bf_m, 4),
        'adaptive_minus_worst_mean': round(full_gap, 4),
        'adaptive_carries_pct_of_gap': round(frac_adaptive, 1),
        'seed_wins_over_best+MARGIN': seed_wins,
        'A_presence': bool(presence),
        'B_earned_majority': bool(earned_majority),
        'C_abl_reverts': bool(abl_reverts),
        'D_shuffle_collapses': bool(shuffle_collapses),
        'E_no_fab': bool(no_fab),
        'verdict': verdict,
        'directional': True,
        'note': 'numpy mirror ⇒ DIRECTIONAL (a_engine_native_learning); engine §Ht5Timing R2 deferred ING; '
                'reuses H_1532 MemStore/key_vec/encode-mode byte-exact; bars frozen-first (NO tune-to-green)',
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
