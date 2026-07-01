#!/usr/bin/env python3
"""
H_1547 — OREXIN/HISTAMINE × CLS: arousal-gated ENCODE↔CONSOLIDATE mode STABILITY.

The 6th (final core) neurotransmitter fused into the H_1532 two-store CLS module
(completes "신경전달물질 모두 융합"; census H_1542 Rank-7 candidate, framed below as the
WAKE/SLEEP MODE selector ABOVE the ACh encode/retrieve MICRO-switch, NOT the encode-RATE
the census flagged as redundant).

WHY this angle (a_no_llm_frame_trap — biological structure first):
Orexin/hypocretin stabilizes the WAKE state and gates whether the system is in ENCODE
(awake → write to fast store) vs CONSOLIDATE (sleep → replay fast→slow) macro-mode
(Sakurai 2007 Nat Rev Neurosci 8:171; orexin LOSS = narcolepsy = UNSTABLE wake/sleep
transitions, intrusion of one state into the other). This is the WAKE/SLEEP MODE selector
ABOVE the ACh (H_1541) encode/retrieve MICRO-switch and ABOVE the 5-HT (H_1545) sweep
TIMING. The biological signature of orexin is not setting a rate — it is providing
TRANSITION STABILITY (hysteresis) so a transient arousal blip does NOT thrash the system
out of an in-progress consolidation.

THE LAW under test (the family running through H_1541🟢/H_1543🟢/H_1544🟢/H_1545🟠):
  NT adds a NEW CAPABILITY a fixed schedule cannot → 🟢 ; NT only RE-TUNES an existing
  duty-cycle a fixed schedule already sets → 🟠.
HONEST PREDICTION via the law (census prior = "honest null / redundant with dr_stage_at"):
  if orexin's hysteresis adds a real STABILIZATION capability (correctly protecting an
  in-progress consolidation that a non-stabilized controller corrupts, AND a FIXED wake/
  sleep duty-cycle CANNOT capture because the demand for consolidation is DATA-DRIVEN, not
  periodic) → 🟢 ; if a grid-tuned fixed dutycycle matches it → 🟠 (it is a knob, the
  census prior wins).

THE CAPABILITY (what makes this distinct from a tunable period):
A stream of ENCODE-events (lay A→B / A→C interfering facts into the small fast store) is
punctuated by CONSOLIDATION-DEMAND windows that arrive at DATA-DRIVEN (irregular) times —
the fast store fills and MUST be swept to the slow store before it LRU-evicts the un-
consolidated bindings. A consolidation sweep takes DWELL ticks to complete. The stream
ALSO carries spurious AROUSAL SPIKES (intrusions) that — for a controller that flips mode
on every spike (THRASH) — kick the system BACK into ENCODE mid-sweep, ABORTING the
consolidation so the un-swept bindings are lost. Orexin hysteresis: arousal must stay
above threshold for a dwell before flipping, so transient spikes are IGNORED and the in-
progress consolidation COMPLETES. A FIXED-DUTYCYCLE controller (sweep every P ticks for D
ticks, grid-tuned) cannot align its windows to the DATA-DRIVEN demand and cannot protect a
sweep an arousal spike lands on top of.

p7: exact ground truth (the true A→B binding is known), NO LLM judge, NO perplexity, NO
loss term — every decision is a no-grad read of substrate state. p8: write/consolidate =
the engine's own tick. $0 CPU. 3 seeds. Frozen falsifier in H_1547_FREEZE.txt.

R1 numpy DIRECTIONAL (a_engine_native_learning hard-gate-1) — engine §OrexinMode R2
deferred ING. REUSES the H_1532 MemStore / key_vec / FNV-1a / suppress_retrieval encode-
mode / LRU eviction BYTE-FOR-BYTE.
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / CORE/engine_cli.hexa) ─────
LR0_ENGINE = 0.20          # adapt_field_step LR
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH
DIM = 16                   # key dim (byte-trigram FNV-1a; toy 16, same as H_1532)
MARGIN = 0.05              # frozen lift bar (same as H_1532 / H_1545)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532) ────────────────────────────
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
        tri = bs[i:i+3]
        idx = fnv1a(tri) % DIM
        v[idx] += 1.0
    n = np.linalg.norm(v)
    if n < 1e-9:
        v = np.zeros(DIM); v[fnv1a(bs) % DIM] = 1.0; n = 1.0
    return v / n


# ── VAdaptField numpy mirror (byte-faithful to H_1532 MemStore) ───────────────
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
            ev = int(np.argmin(self.lru))
            self.protos[ev] = x.copy(); self.values[ev] = value
            self.lru[ev] = self.tick
            return
        self.protos[win] = self.protos[win] + self.LR * (x - self.protos[win])
        self.values[win] = value
        self.lru[win] = self.tick

    def recall(self, x):
        self.tick += 1
        win, err, second = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None, err, second
        self.lru[win] = self.tick
        return self.values[win], err, second


# ── stream: ENCODE events + DATA-DRIVEN consolidation demand + arousal spikes ──
def make_stream(n_segments, rng):
    """A stream of SEGMENTS. Each segment = a burst of ENCODE events (A->B then the
    interfering A->C re-binding over shared keys) that FILLS the small fast store, after
    which a CONSOLIDATION sweep MUST run (DWELL ticks) before the fast store LRU-evicts the
    un-swept A->B. Burst SIZE varies (data-driven demand: big bursts need a sweep SOON,
    small bursts can wait) so a FIXED period cannot align. AROUSAL SPIKES (intrusions) are
    injected at random ticks: a THRASH controller flips mode on each spike (aborting any
    in-progress sweep); an orexin-stabilized controller ignores transient spikes."""
    segs = []
    for s in range(n_segments):
        burst = int(rng.integers(3, 8))           # data-driven burst size (irregular)
        A = [f"key_A{s:02d}_{i:02d}" for i in range(burst)]
        B = [f"val_B{rng.integers(0, 99999):05d}" for _ in range(burst)]
        C = [f"val_C{rng.integers(0, 99999):05d}" for _ in range(burst)]
        for i in range(burst):
            while C[i] == B[i]:
                C[i] = f"val_C{rng.integers(0, 99999):05d}"
        # Arousal during this segment's consolidation window. `arousal_dur` = how many ticks
        # the arousal stays high (0 = none). TRANSIENT (1 tick) = spurious intrusion that
        # should be IGNORED (the in-progress sweep should COMPLETE). SUSTAINED (>=HYST_DWELL
        # ticks) = a genuine arousal/wake demand that should ABORT the sweep (defer
        # consolidation — encoding is the priority). Sakurai 2007: orexin distinguishes a
        # transient blip from a sustained wake-drive; orexin-loss (thrash) cannot.
        roll = rng.random()
        if roll < 0.45:
            arousal_dur = 1                       # TRANSIENT intrusion (ignore)
        elif roll < 0.75:
            arousal_dur = int(rng.integers(2, 5))  # SUSTAINED wake-demand (abort/defer)
        else:
            arousal_dur = 0                        # quiet
        segs.append({'A': A, 'B': B, 'C': C, 'burst': burst,
                     'arousal_dur': arousal_dur})
    return segs


FAST_CELLS = 64     # ample fast store (interference, not capacity, is the test)
SLOW_CELLS = 512
DWELL = 4           # a consolidation sweep takes DWELL ticks to complete (interruptible)
SWEEP_K = 1         # bindings transferred per sweep tick (so DWELL ticks needed to finish)


def _sweep_tick(fast, slow, keys, cursor, k):
    """One tick of a consolidation sweep: transfer up to k bindings by READING THE FAST
    STORE (recall) at `keys[cursor:]` and writing whatever value is CURRENTLY there into the
    slow store. Reading the fast store (not a saved copy) is load-bearing: a sweep that runs
    AFTER the A->C interference has overwritten the fast copy will transfer C, not B -> the
    binding is NOT durably saved. A sweep that COMPLETES before interference transfers B."""
    n = 0
    while cursor < len(keys) and n < k:
        a = keys[cursor]
        v, _, _ = fast.recall(key_vec(a))
        if v is not None:
            slow.write(key_vec(a), v, suppress_retrieval=True)
        cursor += 1; n += 1
    return cursor


def run_arm(segs, LR, THRESH, abstain, mode, fixed_period=0, fixed_dwell=0,
            hyst_dwell=2, shuffle_rng=None):
    """ENCODE<->CONSOLIDATE mode controller over the stream.

    mode:
      'orexin'  — arousal-stabilized: completes a sweep through a TRANSIENT blip (hysteresis
                  absorbs it) and DEFERS on a SUSTAINED wake-demand. (Sakurai 2007.)
      'thrash'  — flips on EVERY arousal spike: aborts sweeps mid-flight, no clean defer.
      'fixed'   — FIXED-DUTYCYCLE: grid-tuned (period,dwell), ignores arousal+demand.
      'abl'     — orexin with the transient/sustained DISTINCTION collapsed (hyst_dwell=0):
                  it ALWAYS completes the sweep and NEVER defers (a fixed always-complete
                  policy that ignores the arousal *kind*). Isolates the distinction's value.
      'always'  — explicit ALWAYS-COMPLETE fixed policy (== abl): a no-arousal-reading
                  controller that just runs the full sweep every segment. The law's refuter.
      'shuffle' — orexin but the arousal_dur signal is PERMUTED across segments -> the
                  stabilizer makes the transient/sustained call on the WRONG segments.
    """
    fast = MemStore(FAST_CELLS, abstain, LR, THRESH)
    slow = MemStore(SLOW_CELLS, abstain, LR, THRESH)
    all_A, all_B = [], []

    if mode in ('abl', 'always'):
        hyst_dwell = 0
        mode_eff = 'orexin'
    elif mode == 'shuffle':
        durs = [seg['arousal_dur'] for seg in segs]
        shuffle_rng.shuffle(durs)
        segs = [dict(s, arousal_dur=d) for s, d in zip(segs, durs)]
        mode_eff = 'orexin'
    else:
        mode_eff = mode

    carry = []   # A-keys DEFERRED from a sustained-arousal segment (orexin re-sweeps later)
    for si, seg in enumerate(segs):
        A, B, C = seg['A'], seg['B'], seg['C']
        all_A += A; all_B += B
        ad = seg['arousal_dur']

        # (1) ENCODE A->B into the fast episodic store (encode-mode, fresh cells).
        for a, b in zip(A, B):
            fast.write(key_vec(a), b, suppress_retrieval=True)

        # carry = deferred A-keys from a prior sustained segment; sweep them FIRST this
        # (quieter) segment. They still hold B in the fast store (their A->C already fired in
        # their own segment overwrote the fast copy) -> actually re-encode B so the deferred
        # sweep can transfer it. (orexin defers the *consolidation*, re-laying B fresh.)
        for a, b in carry:
            fast.write(key_vec(a), b, suppress_retrieval=True)
        sweep_keys = [a for a, _ in carry] + list(A)
        carry = []

        # (2) the CONSOLIDATION-DEMAND window + the A->C INTERFERENCE share the same ticks.
        #     timeline: at tick INTERF_TICK the A->C re-binding lands (overwrites the fast
        #     A->B copy). A sweep tick BEFORE INTERF_TICK reads B; a sweep tick AFTER reads C.
        #     SUSTAINED arousal => interference lands EARLY (tick 0) so sweeping now is futile
        #     (transfers mostly C) => the right move is to DEFER. TRANSIENT/quiet =>
        #     interference lands LATE (after DWELL) so a completed sweep captures all B.
        sustained = (ad >= hyst_dwell) if hyst_dwell > 0 else (ad >= 2)
        interf_tick = 0 if (ad >= 2) else DWELL   # sustained arousal = early interference

        if mode_eff == 'fixed':
            do_sweep = (fixed_period > 0 and (si % fixed_period) == 0)
            dwell = fixed_dwell if do_sweep else 0
            abort_at = None; defer = False
        elif mode_eff == 'orexin':
            dwell = DWELL
            if sustained and hyst_dwell > 0:
                do_sweep, defer, abort_at = False, True, None   # DEFER on sustained
            else:
                do_sweep, defer, abort_at = True, False, None   # complete through transient
        elif mode_eff == 'thrash':
            dwell = DWELL; defer = False
            do_sweep = True
            abort_at = 1 if ad >= 1 else None       # any spike aborts after tick 0
        else:
            do_sweep, dwell, abort_at, defer = False, 0, None, False

        if defer:
            carry = [(a, b) for a, b in zip(A, B)]  # re-sweep B next (quieter) segment
        elif do_sweep and dwell > 0:
            cursor = 0
            for t in range(dwell):
                if t == interf_tick:                # A->C interference lands at this tick
                    for a, c in zip(A, C):
                        fast.write(key_vec(a), c, suppress_retrieval=False)
                if abort_at is not None and t >= abort_at:
                    break
                cursor = _sweep_tick(fast, slow, sweep_keys, cursor, k=SWEEP_K)
                if cursor >= len(sweep_keys):
                    break

        # (3) if interference has not landed yet this segment (late/never reached in the
        #     sweep loop, or no sweep ran), it lands now -> overwrite the fast A->B copy.
        if (not do_sweep) or dwell == 0 or interf_tick >= dwell:
            for a, c in zip(A, C):
                fast.write(key_vec(a), c, suppress_retrieval=False)

    # flush any final carry (deferred at the last segment) into the slow store
    for a, b in carry:
        fast.write(key_vec(a), b, suppress_retrieval=True)
        slow.write(key_vec(a), b, suppress_retrieval=True)

    return _score(fast, slow, all_A, all_B)


def _score(fast, slow, A, B):
    """A->B retention scored across BOTH stores (CLS OR-read): retained if the fast OR the
    slow store still returns the OLD B. Un-consolidated bindings that were LRU-evicted from
    the small fast store before reaching the slow store count as NOT retained (honest)."""
    correct = 0
    for a, b in zip(A, B):
        pf, _, _ = fast.recall(key_vec(a))
        ps, _, _ = slow.recall(key_vec(a))
        if pf == b or ps == b:
            correct += 1
    return correct / max(1, len(A))


def grid_tune_fixed(n_segments, tune_seed):
    """FIXED-DUTYCYCLE baseline = the BEST grid-tuned (period, dwell) on a DISJOINT seed
    (anti-confound: orexin must beat the strongest honest fixed schedule)."""
    best = None
    rng = np.random.default_rng(tune_seed)
    segs = make_stream(n_segments, rng)
    for period in (1, 2, 3, 4):
        for dwell in (1, 2, 3):
            r = run_arm(segs, LR0_ENGINE, TH0_ENGINE, 0.45, 'fixed',
                        fixed_period=period, fixed_dwell=dwell)
            if best is None or r > best[0]:
                best = (r, period, dwell)
    return best[1], best[2]


def main():
    N_SEG = 14
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    HYST_DWELL = 2     # orexin hysteresis dwell (transient spikes < this are absorbed)

    P_star, D_star = grid_tune_fixed(N_SEG, TUNE_SEED)

    rows = []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        segs = make_stream(N_SEG, rng)
        orexin = run_arm(segs, LR0_ENGINE, TH0_ENGINE, ABSTAIN0, 'orexin',
                         hyst_dwell=HYST_DWELL)
        thrash = run_arm(segs, LR0_ENGINE, TH0_ENGINE, ABSTAIN0, 'thrash')
        fixed = run_arm(segs, LR0_ENGINE, TH0_ENGINE, ABSTAIN0, 'fixed',
                        fixed_period=P_star, fixed_dwell=D_star)
        always = run_arm(segs, LR0_ENGINE, TH0_ENGINE, ABSTAIN0, 'always')
        abl = run_arm(segs, LR0_ENGINE, TH0_ENGINE, ABSTAIN0, 'abl')
        shuf = run_arm(segs, LR0_ENGINE, TH0_ENGINE, ABSTAIN0, 'shuffle',
                       hyst_dwell=HYST_DWELL,
                       shuffle_rng=np.random.default_rng(seed + 1000))
        # best ALTERNATIVE = strongest non-orexin controller (the honest bar to beat) =
        # max over thrash / fixed-dutycycle / always-complete fixed policy.
        best_alt = max(thrash, fixed, always)
        rows.append({'seed': seed,
                     'orexin': round(orexin, 4), 'thrash': round(thrash, 4),
                     'fixed_dutycycle': round(fixed, 4),
                     'always_complete': round(always, 4), 'abl': round(abl, 4),
                     'shuffle': round(shuf, 4), 'best_alt': round(best_alt, 4),
                     'orexin_minus_best_alt': round(orexin - best_alt, 4)})

    orx_m = float(np.mean([r['orexin'] for r in rows]))
    thr_m = float(np.mean([r['thrash'] for r in rows]))
    fix_m = float(np.mean([r['fixed_dutycycle'] for r in rows]))
    alw_m = float(np.mean([r['always_complete'] for r in rows]))
    abl_m = float(np.mean([r['abl'] for r in rows]))
    shf_m = float(np.mean([r['shuffle'] for r in rows]))
    best_alt_m = float(np.mean([r['best_alt'] for r in rows]))

    # ── FROZEN falsifier (pre-registered in H_1547_FREEZE.txt) ────────────────
    #   A PRESENCE      : orexin - best_alt >= +MARGIN on >= 2/3 seeds AND in mean
    #                     (best_alt = max(thrash, fixed-dutycycle, always-complete))
    #   B DISTINCT      : thrash corrupts (thrash < orexin - MARGIN) AND fixed-dutycycle
    #                     misses demand (fixed < orexin - MARGIN), both in mean
    #   C EARNED-DISTINCTION : orexin - always-complete >= MARGIN (the arousal-reading
    #                     transient/sustained DISTINCTION adds value beyond a fixed never-
    #                     abort policy) AND abl == always-complete (sanity: ablating the
    #                     distinction reduces EXACTLY to always-complete, |abl-always|<MARGIN)
    #   C2 LAW-MAJORITY : orexin - always-complete >= 0.5*(orexin - thrash)
    #                     — does the arousal-reading DISTINCTION carry the MAJORITY of the
    #                       value over the worst controller? if a FIXED always-complete
    #                       policy already captures the majority -> it's a knob (law -> 🟠).
    #   D SHUFFLE       : permute arousal signal -> collapse (orexin - shuffle >= MARGIN)
    #   E NO-FAB        : best_alt > 0 (a real working baseline; lift is the distinction)
    n_win = sum(1 for r in rows if r['orexin_minus_best_alt'] >= MARGIN)
    A_presence = (n_win >= 2) and ((orx_m - best_alt_m) >= MARGIN)
    B_distinct = (thr_m < orx_m - MARGIN) and (fix_m < orx_m - MARGIN)
    C_earned = ((orx_m - alw_m) >= MARGIN) and (abs(abl_m - alw_m) < MARGIN)
    C2_majority = (orx_m - alw_m) >= 0.5 * (orx_m - thr_m)
    D_shuffle = (orx_m - shf_m) >= MARGIN
    E_nofab = best_alt_m > 0.0

    if A_presence and B_distinct and C_earned and C2_majority and D_shuffle and E_nofab:
        verdict = 'GREEN'        # arousal-reading DISTINCTION = a new CAPABILITY (law: 🟢)
    elif A_presence and C_earned and D_shuffle and E_nofab and (not C2_majority):
        # the distinction is PRESENT + EARNED but a fixed always-complete policy captures
        # the MAJORITY -> orexin re-tunes a knob (law: 🟠; census 'honest null' prior wins).
        verdict = 'AMBER'
    elif A_presence and E_nofab and not B_distinct:
        verdict = 'AMBER'
    elif A_presence:
        verdict = 'AMBIGUOUS_ABLATION'
    else:
        verdict = 'WALL_HOLDS'   # orexin ties/loses -> census 'honest null' prior wins

    gap = orx_m - thr_m
    summary = {
        'capability': 'arousal-gated ENCODE<->CONSOLIDATE mode STABILITY: A->B retention '
                      'when transient arousal would abort an in-progress consolidation',
        'P_star': P_star, 'D_star': D_star,
        'N_SEG': N_SEG, 'FAST_CELLS': FAST_CELLS, 'SLOW_CELLS': SLOW_CELLS,
        'DWELL': DWELL, 'HYST_DWELL': HYST_DWELL,
        'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
        'per_seed': rows,
        'orexin_mean': round(orx_m, 4),
        'thrash_mean': round(thr_m, 4),
        'fixed_dutycycle_mean': round(fix_m, 4),
        'always_complete_mean': round(alw_m, 4),
        'abl_mean': round(abl_m, 4),
        'shuffle_mean': round(shf_m, 4),
        'best_alt_mean': round(best_alt_m, 4),
        'orexin_minus_best_alt_mean': round(orx_m - best_alt_m, 4),
        'orexin_minus_thrash_mean': round(orx_m - thr_m, 4),
        'orexin_minus_fixed_mean': round(orx_m - fix_m, 4),
        'orexin_minus_always_mean': round(orx_m - alw_m, 4),
        'distinction_majority_fraction': round((orx_m - alw_m) / gap, 4) if gap > 1e-9 else None,
        'majority_bar': round(0.5 * gap, 4),
        'abl_minus_always_mean': round(abl_m - alw_m, 4),
        'orexin_minus_shuffle_mean': round(orx_m - shf_m, 4),
        'n_wins_over_best_alt+MARGIN': n_win,
        'A_presence': bool(A_presence), 'B_distinct': bool(B_distinct),
        'C_earned': bool(C_earned), 'C2_majority': bool(C2_majority),
        'D_shuffle': bool(D_shuffle), 'E_nofab': bool(E_nofab),
        'verdict': verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
