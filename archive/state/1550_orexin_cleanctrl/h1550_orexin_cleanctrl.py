#!/usr/bin/env python3
"""
H_1550 — OREXIN × CLS: mode-stability with a CLEAN SHUFFLE CONTROL (honest GREEN attempt).

This is the CONTROL-FIX of H_1547 (a_break_the_wall type-(a) measurement-fix, NOT
tune-to-green). H_1547 landed 🟠 because its SHUFFLE control did not cleanly collapse
(seed33 shuffle 0.654 > orexin 0.603; mean orexin−shuffle only +0.0579) AND because the
distinction did not carry the law-majority (C2). The DIAGNOSIS (team-lead, a_break_the_wall
type-(a)): the H_1547 shuffle permuted the per-segment `arousal_dur` signal, but that field
ALSO drives the TRUE interference position (`interf_tick = 0 if ad>=2 else DWELL`) inside the
same arm — so permuting `arousal_dur` CO-PERMUTED the true interference boundary, keeping the
controller's transient/sustained call ALIGNED with where interference actually landed. The
shuffle therefore never broke the alignment between the arousal SIGNAL the controller reads
and the TRUE boundary, so a fixed-dwell hysteresis on a permuted-but-still-aligned stream kept
its gain. That is a CONTROL-DESIGN flaw, not evidence against the capability.

THE CLEAN CONTROL (pre-registered, frozen-first): hold the DWELL-WIDTH hysteresis controller
byte-identical, but DECOUPLE the two roles of `arousal_dur` into:
  • a TRUE per-segment property `interf_dur` that fixes WHERE the A->C interference lands
    (the real consolidation-demand boundary) — held at its REAL per-segment value, and
  • a SIGNAL `arousal_read` that the controller READS to decide transient-vs-sustained —
    PERMUTED across segments in CLEAN-SHUFFLE only.
In CLEAN-SHUFFLE the controller makes its transient/sustained call from `arousal_read`
(permuted) while interference still lands at the REAL `interf_dur` of each segment. So only
the controller's read is scrambled; the true boundary is untouched. Any surviving gain is
PURELY the fixed dwell-width (a knob, regardless of timing). If orexin's gain comes from
reading TRUE timing, CLEAN-SHUFFLE collapses; if it survives, the lever is genuinely the
dwell-width and the honest verdict stays 🟠 (we report it, we do NOT force green).

ALL OTHER ARMS AND BARS ARE IDENTICAL TO H_1547 (presence +0.05, distinct, ABL, NO-FAB).
Only the shuffle control is corrected. The corrected control is pre-registered in
H_1550_FREEZE.txt BEFORE the scored run.

Bars: (A PRESENCE) orexin−best_alt ≥+0.05 on ≥2/3 AND mean (UNCHANGED) · (B DISTINCT)
thrash<orexin−0.05 AND fixed<orexin−0.05 (UNCHANGED) · (C ABL→always, |abl−always|<0.05)
(UNCHANGED) · (D CLEAN-SHUFFLE COLLAPSE) orexin−clean_shuffle ≥+0.05 on ≥2/3 AND mean
(CORRECTED control) · (E NO-FAB) best_alt>0 (UNCHANGED). 🟢 iff A∧B∧C∧D∧E. Honest 🟠 if
even the clean control does not collapse.

p7: exact ground truth, NO LLM judge, NO perplexity, NO loss term. p8: write/consolidate =
the engine's own tick. $0 CPU. 3 seeds. R1 numpy DIRECTIONAL (a_engine_native_learning
hard-gate-1) — engine §OrexinMode R2 deferred ING. REUSES the H_1532 MemStore / key_vec /
FNV-1a / suppress_retrieval encode-mode / LRU eviction BYTE-FOR-BYTE.
Sakurai 2007 Nat Rev Neurosci 8:171 (orexin loss = narcolepsy = unstable wake/sleep
transitions; orexin = TRANSITION STABILITY, distinguishing transient blip from sustained drive).
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / H_1547 / CORE/engine_cli.hexa) ──
LR0_ENGINE = 0.20          # adapt_field_step LR
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH
DIM = 16                   # key dim (byte-trigram FNV-1a; toy 16, same as H_1532)
MARGIN = 0.05              # frozen lift bar (same as H_1532 / H_1547)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532 / H_1547) ───────────────────
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


# ── VAdaptField numpy mirror (byte-faithful to H_1532 / H_1547 MemStore) ──────
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
    """Identical to H_1547 make_stream. Each segment carries `arousal_dur` (0 quiet /
    1 transient / >=2 sustained). NOTE the decoupling done DOWNSTREAM (run_arm): the TRUE
    interference position is derived from this REAL arousal_dur (`interf_dur`); the controller
    READ is a separate field that only CLEAN-SHUFFLE permutes."""
    segs = []
    for s in range(n_segments):
        burst = int(rng.integers(3, 8))           # data-driven burst size (irregular)
        A = [f"key_A{s:02d}_{i:02d}" for i in range(burst)]
        B = [f"val_B{rng.integers(0, 99999):05d}" for _ in range(burst)]
        C = [f"val_C{rng.integers(0, 99999):05d}" for _ in range(burst)]
        for i in range(burst):
            while C[i] == B[i]:
                C[i] = f"val_C{rng.integers(0, 99999):05d}"
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
    """One tick of a consolidation sweep — VERBATIM from H_1547."""
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

    The DECOUPLING (the H_1550 fix): each segment has
      • interf_dur  = the segment's REAL arousal_dur  -> drives WHERE A->C interference lands
                      (interf_tick = 0 if interf_dur>=2 else DWELL). This is the TRUE boundary
                      and is NEVER permuted (so the physics of the stream is identical for
                      every arm, including clean-shuffle).
      • arousal_read = the signal the CONTROLLER reads to call transient vs sustained. For
                      every arm EXCEPT 'clean_shuffle' arousal_read == interf_dur (so orexin/
                      thrash/fixed/abl behave BYTE-IDENTICALLY to H_1547). For 'clean_shuffle'
                      arousal_read is PERMUTED across segments while interf_dur stays REAL ->
                      the controller's call is scrambled relative to the true boundary, but the
                      dwell-width hysteresis is otherwise unchanged. Surviving gain = pure
                      dwell-width knob; collapse = the gain reads TRUE timing.

    mode: 'orexin' / 'thrash' / 'fixed' / 'abl' / 'always' / 'clean_shuffle'
    """
    fast = MemStore(FAST_CELLS, abstain, LR, THRESH)
    slow = MemStore(SLOW_CELLS, abstain, LR, THRESH)
    all_A, all_B = [], []

    # build per-segment (interf_dur REAL, arousal_read = controller input)
    interf_durs = [seg['arousal_dur'] for seg in segs]
    if mode == 'clean_shuffle':
        reads = list(interf_durs)
        shuffle_rng.shuffle(reads)             # permute ONLY the controller's read
        mode_eff = 'orexin'
    else:
        reads = list(interf_durs)              # controller reads the TRUE arousal (no scramble)
        if mode in ('abl', 'always'):
            hyst_dwell = 0
            mode_eff = 'orexin'
        else:
            mode_eff = mode

    carry = []   # A-keys DEFERRED from a sustained-arousal segment (orexin re-sweeps later)
    for si, seg in enumerate(segs):
        A, B, C = seg['A'], seg['B'], seg['C']
        all_A += A; all_B += B
        interf_dur = interf_durs[si]   # TRUE boundary (never permuted)
        read = reads[si]               # controller's read (permuted only in clean_shuffle)

        # (1) ENCODE A->B into the fast episodic store (encode-mode, fresh cells).
        for a, b in zip(A, B):
            fast.write(key_vec(a), b, suppress_retrieval=True)

        # carry = deferred A-keys from a prior sustained segment; re-lay B then sweep FIRST.
        for a, b in carry:
            fast.write(key_vec(a), b, suppress_retrieval=True)
        sweep_keys = [a for a, _ in carry] + list(A)
        carry = []

        # (2) the CONSOLIDATION window + the A->C INTERFERENCE share the same ticks.
        #     interf_tick = WHERE interference lands = TRUE boundary from interf_dur.
        #     The controller decides sweep/defer from `read` (its arousal signal).
        sustained = (read >= hyst_dwell) if hyst_dwell > 0 else (read >= 2)
        interf_tick = 0 if (interf_dur >= 2) else DWELL   # TRUE: sustained => early interference

        if mode_eff == 'fixed':
            do_sweep = (fixed_period > 0 and (si % fixed_period) == 0)
            dwell = fixed_dwell if do_sweep else 0
            abort_at = None; defer = False
        elif mode_eff == 'orexin':
            dwell = DWELL
            if sustained and hyst_dwell > 0:
                do_sweep, defer, abort_at = False, True, None   # DEFER on (read-)sustained
            else:
                do_sweep, defer, abort_at = True, False, None   # complete through (read-)transient
        elif mode_eff == 'thrash':
            dwell = DWELL; defer = False
            do_sweep = True
            abort_at = 1 if read >= 1 else None     # any spike aborts after tick 0
        else:
            do_sweep, dwell, abort_at, defer = False, 0, None, False

        if defer:
            carry = [(a, b) for a, b in zip(A, B)]  # re-sweep B next (quieter) segment
        elif do_sweep and dwell > 0:
            cursor = 0
            for t in range(dwell):
                if t == interf_tick:                # A->C interference lands at TRUE tick
                    for a, c in zip(A, C):
                        fast.write(key_vec(a), c, suppress_retrieval=False)
                if abort_at is not None and t >= abort_at:
                    break
                cursor = _sweep_tick(fast, slow, sweep_keys, cursor, k=SWEEP_K)
                if cursor >= len(sweep_keys):
                    break

        # (3) if interference has not landed yet this segment, it lands now (overwrite fast B).
        if (not do_sweep) or dwell == 0 or interf_tick >= dwell:
            for a, c in zip(A, C):
                fast.write(key_vec(a), c, suppress_retrieval=False)

    # flush any final carry (deferred at the last segment) into the slow store
    for a, b in carry:
        fast.write(key_vec(a), b, suppress_retrieval=True)
        slow.write(key_vec(a), b, suppress_retrieval=True)

    return _score(fast, slow, all_A, all_B)


def _score(fast, slow, A, B):
    """A->B retention across BOTH stores (CLS OR-read) — VERBATIM from H_1547."""
    correct = 0
    for a, b in zip(A, B):
        pf, _, _ = fast.recall(key_vec(a))
        ps, _, _ = slow.recall(key_vec(a))
        if pf == b or ps == b:
            correct += 1
    return correct / max(1, len(A))


def grid_tune_fixed(n_segments, tune_seed):
    """FIXED-DUTYCYCLE baseline = BEST grid-tuned (period, dwell) on a DISJOINT seed —
    VERBATIM from H_1547."""
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
        clean_shuf = run_arm(segs, LR0_ENGINE, TH0_ENGINE, ABSTAIN0, 'clean_shuffle',
                             hyst_dwell=HYST_DWELL,
                             shuffle_rng=np.random.default_rng(seed + 1000))
        best_alt = max(thrash, fixed, always)
        rows.append({'seed': seed,
                     'orexin': round(orexin, 4), 'thrash': round(thrash, 4),
                     'fixed_dutycycle': round(fixed, 4),
                     'always_complete': round(always, 4), 'abl': round(abl, 4),
                     'clean_shuffle': round(clean_shuf, 4),
                     'best_alt': round(best_alt, 4),
                     'orexin_minus_best_alt': round(orexin - best_alt, 4),
                     'orexin_minus_clean_shuffle': round(orexin - clean_shuf, 4)})

    orx_m = float(np.mean([r['orexin'] for r in rows]))
    thr_m = float(np.mean([r['thrash'] for r in rows]))
    fix_m = float(np.mean([r['fixed_dutycycle'] for r in rows]))
    alw_m = float(np.mean([r['always_complete'] for r in rows]))
    abl_m = float(np.mean([r['abl'] for r in rows]))
    cshf_m = float(np.mean([r['clean_shuffle'] for r in rows]))
    best_alt_m = float(np.mean([r['best_alt'] for r in rows]))

    # ── FROZEN falsifier (pre-registered in H_1550_FREEZE.txt) ────────────────
    #   A PRESENCE  : orexin − best_alt ≥ +0.05 on ≥2/3 AND mean (best_alt=max(thr,fix,alw))
    #   B DISTINCT  : thrash < orexin − 0.05 (mean) AND fixed < orexin − 0.05 (mean)
    #   C ABL       : orexin − always ≥ 0.05 AND |abl − always| < 0.05 (clean ablation)
    #   D CLEAN-SHUFFLE COLLAPSE (the CORRECTED control):
    #                 orexin − clean_shuffle ≥ +0.05 on ≥2/3 seeds AND mean — permuting ONLY
    #                 the controller's read (true interference boundary untouched) collapses
    #                 the lift => the gain reads TRUE arousal timing, not just dwell-width.
    #   E NO-FAB    : best_alt > 0
    n_win = sum(1 for r in rows if r['orexin_minus_best_alt'] >= MARGIN)
    n_cshuf_collapse = sum(1 for r in rows if r['orexin_minus_clean_shuffle'] >= MARGIN)
    A_presence = (n_win >= 2) and ((orx_m - best_alt_m) >= MARGIN)
    B_distinct = (thr_m < orx_m - MARGIN) and (fix_m < orx_m - MARGIN)
    C_earned = ((orx_m - alw_m) >= MARGIN) and (abs(abl_m - alw_m) < MARGIN)
    D_clean_shuffle = (n_cshuf_collapse >= 2) and ((orx_m - cshf_m) >= MARGIN)
    E_nofab = best_alt_m > 0.0

    if A_presence and B_distinct and C_earned and D_clean_shuffle and E_nofab:
        # the gain survives every alternative AND the corrected control collapses it ->
        # orexin reads the TRUE arousal-boundary timing = a real stabilization CAPABILITY.
        verdict = 'GREEN'
    elif A_presence and B_distinct and C_earned and E_nofab and (not D_clean_shuffle):
        # presence/distinct/ablation hold, but even the CORRECTED control does not collapse
        # the lift -> the lever genuinely is the fixed dwell-width (a knob), not true-timing.
        # HONEST 🟠 — reported, NOT forced green.
        verdict = 'AMBER_KNOB'
    elif A_presence and E_nofab and not B_distinct:
        verdict = 'AMBER_TIE'
    elif A_presence:
        verdict = 'AMBIGUOUS_ABLATION'
    else:
        verdict = 'WALL_HOLDS'

    summary = {
        'capability': 'arousal-gated ENCODE<->CONSOLIDATE mode STABILITY with a CLEAN shuffle '
                      'control (permute controller READ, hold TRUE interference boundary)',
        'control_fix': 'H_1547 type-(a): decouple arousal_read (controller input, permuted in '
                       'clean_shuffle) from interf_dur (TRUE boundary, never permuted); '
                       'bars otherwise unchanged; NOT tune-to-green',
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
        'clean_shuffle_mean': round(cshf_m, 4),
        'best_alt_mean': round(best_alt_m, 4),
        'orexin_minus_best_alt_mean': round(orx_m - best_alt_m, 4),
        'orexin_minus_clean_shuffle_mean': round(orx_m - cshf_m, 4),
        'orexin_minus_thrash_mean': round(orx_m - thr_m, 4),
        'orexin_minus_fixed_mean': round(orx_m - fix_m, 4),
        'orexin_minus_always_mean': round(orx_m - alw_m, 4),
        'abl_minus_always_mean': round(abl_m - alw_m, 4),
        'n_wins_over_best_alt+MARGIN': n_win,
        'n_clean_shuffle_collapse': n_cshuf_collapse,
        'A_presence': bool(A_presence), 'B_distinct': bool(B_distinct),
        'C_earned': bool(C_earned), 'D_clean_shuffle': bool(D_clean_shuffle),
        'E_nofab': bool(E_nofab),
        'verdict': verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
