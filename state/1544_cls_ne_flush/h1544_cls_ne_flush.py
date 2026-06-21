#!/usr/bin/env python3
"""
H_1544 — NOREPINEPHRINE × CLS: context-boundary fast-store FLUSH.

The REOPEN of the TWICE-WALLED NE-as-RESET faculty (H_1537 🧱 #2518 +0.006;
H_1539 🧱 #2521 −0.0049) INSIDE the H_1532 two-store CLS module.

WHY this angle (a_no_llm_frame_trap · a_break_the_wall TYPE-(b)/(c)):
NE-as-reset walled TWICE as a STANDALONE SINGLE-STORE faculty. The honest
mechanistic reason both lanes walled (H_1537's own diagnostic; H_1532-R2 verdict):
**a single store gives a reset-knob NOTHING STRUCTURAL to act on** — a high fixed
gain (H_1537 α*=0.6) already performs a slow overwrite, masking the explicit flush.
On ONE store, "reset" = scale down a scalar — it re-enters the controller family the
H_1284 wall absorbs.

The reopen (the structural lever single-store LACKED): once a FAST EPISODIC store
exists (H_1532 CLS), NE's real Bouret-Sara 2005 computation — a phasic burst at a
detected CONTEXT BOUNDARY firing a GLOBAL NETWORK RESET — has a concrete substrate
target: **FLUSH (commit-then-clear) the fast episodic store at the segment boundary**
so the next context's bindings are laid down on a CLEAN fast store, not on top of the
previous segment's stale fast traces. (Event-segmentation theory, Zacks et al. 2007:
the brain parses experience into segments at event boundaries; the boundary is where
working/episodic buffers are flushed and the next event is encoded fresh.)

This is NOT a scalar gain (H_1422 ACh-gain 🧱) — it changes the STATE of a store
(which traces persist into the next segment), exactly the structural DOF the
single-store NE lanes had none of.

CAPABILITY — MULTI-CONTEXT INTERFERENCE STREAM. The stream is a sequence of SEGMENTS
separated by boundaries. WITHIN a segment, keys A_i bind to that segment's values
(AB). ACROSS segments the SAME keys A_i reappear with DIFFERENT values (AC, AD, …):
each new segment re-binds the shared keys. The fast episodic store accumulates a
segment's bindings; if it is NOT flushed at the boundary, the previous segment's
stale fast traces collide with the next segment's re-bindings on the shared keys.
METRIC = CURRENT-segment retention: after the whole stream, for each shared key, does
the store still return the value it was bound to IN THE FINAL (current) segment?
(p7: exact ground truth — the current-segment binding is known; NO LLM judge / loss /
perplexity. p8: write = the engine's own tick. $0 CPU, 3 seeds, frozen falsifier.)

ARMS (identical fixture / fact-set / event-stream per seed; LR/TH = H_1532 best-fixed):
  NE-FLUSH    : CLS two-store; at each DETECTED boundary, COMMIT the fast episodic
                store into slow (replay-consolidate) then CLEAR fast → next segment
                encodes on a clean fast store (the Bouret-Sara network reset).
  NO-FLUSH    : CLS two-store, fast persists across boundaries (the H_1532 CLS, no NE).
  ALWAYS-FLUSH: flush EVERY step (no boundary detection) → loses within-segment
                bindings (can't accumulate the current segment) = over-reset control.
  ABL         : boundary signal held CONSTANT (never crosses) → never flushes →
                MUST REVERT to NO-FLUSH (proves the lever is the boundary-triggered
                flush, not the two-store machinery alone).
  SHUFFLE     : same NUMBER of flushes at PERMUTED random tick positions (decoupled
                from the TRUE boundaries) → MUST COLLAPSE (proves it is TRUE
                boundaries, not flush-rate / periodic clearing).

R1 numpy DIRECTIONAL (host has no torch; a_engine_native_learning hard-gate-1) —
engine §NeFlush R2 deferred ING. REUSES the H_1532 / H_1284 store machinery
byte-for-byte (MemStore/key_vec/FNV-1a/MARGIN), so the ONLY new variable is the
boundary flush.
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / H_1284 / CORE) ────────────
LR0_ENGINE = 0.20          # adapt_field_step LR
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH
DIM = 16                   # key dim (FNV-1a trigram; toy 16, same as H_1532/H_1284)
MARGIN = 0.10              # frozen PRESENCE bar (the H_1537/H_1539 NE-reset bar, +0.10)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532 / H_1284) ───────────────────
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


# ── MemStore (byte-faithful to vadapt_field_step — VERBATIM from H_1532) ──────
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

    def clear(self):
        """NE network-reset: empty the fast episodic store (Bouret-Sara 2005)."""
        self.protos = []
        self.values = []
        self.lru = []
        # keep self.tick monotone (no peek at boundary labels)


# ── MULTI-CONTEXT interference stream (exact ground truth) ────────────────────
def make_multicontext(n_keys, n_segments, n_distract_per_seg, rng):
    """A sequence of n_segments SEGMENTS over n_keys SHARED keys A_i. In each segment
    every shared key A_i is re-bound to a fresh value V[seg][i] (AB within seg-0, AC in
    seg-1, AD in seg-2, …). Each segment also writes n_distract_per_seg unrelated
    distractor facts (interference load). The CAPABILITY = retain each key's CURRENT
    (final-segment) binding after the whole stream, despite the stale prior-segment
    bindings on the SAME keys."""
    A = [f"key_A{i:03d}" for i in range(n_keys)]
    # per-segment values for each shared key (all distinct across segments per key)
    V = []
    for s in range(n_segments):
        seg_vals = []
        for i in range(n_keys):
            v = f"val_S{s}_{rng.integers(0, 99999):05d}"
            seg_vals.append(v)
        V.append(seg_vals)
    # ensure within a key the per-segment values are mutually distinct
    for i in range(n_keys):
        seen = set()
        for s in range(n_segments):
            while V[s][i] in seen:
                V[s][i] = f"val_S{s}_{rng.integers(0, 99999):05d}"
            seen.add(V[s][i])
    # per-segment distractors
    D = []
    for s in range(n_segments):
        dk = [f"key_D{s}_{j:03d}" for j in range(n_distract_per_seg)]
        dv = [f"val_DD{rng.integers(0, 99999):05d}" for _ in range(n_distract_per_seg)]
        D.append((dk, dv))
    return A, V, D


def _build_stream(A, V, D):
    """Flatten the segments into a single tick-stream of (key, value, is_boundary).
    is_boundary marks the FIRST tick of each segment after segment 0 (a TRUE event
    boundary — the model 'enters a new context')."""
    n_segments = len(V)
    stream = []
    for s in range(n_segments):
        first = True
        # shared-key re-bindings for this segment
        for i in range(len(A)):
            stream.append((A[i], V[s][i], (s > 0 and first)))
            first = False
        # distractors for this segment
        dk, dv = D[s]
        for k, v in zip(dk, dv):
            stream.append((k, v, False))
    return stream


# ── ARMS ──────────────────────────────────────────────────────────────────────
def _new_store(max_cells, abstain, LR, THRESH):
    return MemStore(max_cells, abstain, LR, THRESH)


def run_cls(A, V, D, fast_cap, slow_cap, LR, THRESH, abstain,
            flush_mode='none', shuffle=False, seed=0):
    """CLS two-store over the multi-context stream.

    Every write lands in fast in encode-mode (Hasselmo; H_1532 phase-separation =
    a FRESH cell, never an overwrite). Capacity is AMPLE (interference, NOT capacity,
    is the test — exactly H_1532's framing): so WITHOUT a boundary flush, ALL three
    segments' same-key cells COEXIST in fast. At recall the exact-key query ties at
    distance ~0 across those same-key cells and the H_1532 _nearest (argsort, stable)
    returns the FIRST-written = the STALE seg-0 binding — the current binding is
    SHADOWED (this is the AB-AC interference, now ACROSS the whole stream). The SLOW
    store is the consolidated history (large), written by commit-on-flush.

    flush_mode:
      'none'    : NO-FLUSH — fast persists across boundaries (H_1532 CLS, no NE).
      'boundary': NE-FLUSH — at each TRUE boundary, COMMIT fast→slow (replay
                  consolidation) then CLEAR fast (Bouret-Sara network reset) → the
                  next segment encodes on a clean, uncongested fast store.
      'always'  : ALWAYS-FLUSH — commit+clear EVERY tick → fast can never hold even
                  the current segment (over-reset; loses within-segment bindings).
    shuffle=True: flush at PERMUTED random tick positions (same flush COUNT, decoupled
                  from the TRUE boundaries).
    ABL is expressed as flush_mode='none' (boundary signal const → never flush)."""
    fast = _new_store(fast_cap, abstain, LR, THRESH)
    slow = _new_store(slow_cap, abstain, LR, THRESH)
    stream = _build_stream(A, V, D)

    true_boundary_idx = [t for t, (_, _, b) in enumerate(stream) if b]
    if flush_mode == 'boundary':
        flush_ticks = set(true_boundary_idx)
    elif flush_mode == 'always':
        flush_ticks = set(range(len(stream)))
    else:  # 'none'
        flush_ticks = set()
    if shuffle and flush_mode == 'boundary':
        rng = np.random.default_rng(seed + 7000)
        k = len(true_boundary_idx)
        perm = rng.permutation(list(range(len(stream))))[:k]
        flush_ticks = set(int(x) for x in perm)

    def do_flush():
        # COMMIT-then-CLEAR: consolidate fast episodic traces into slow, empty fast.
        for p, val in zip(fast.protos, fast.values):
            slow.write(p.copy(), val, suppress_retrieval=True)
        fast.clear()

    for t, (k, v, _b) in enumerate(stream):
        if t in flush_ticks:
            do_flush()
        fast.write(key_vec(k), v, suppress_retrieval=True)

    # CURRENT-context read = fast episodic (the segment you are in); the slow store is
    # NOT consulted for the current binding (it holds consolidated OLD contexts and on
    # the shared keys returns whichever stale binding it consolidated). Score fast.
    return _score_current(fast, A, V)


def _score_current(store, A, V):
    """CURRENT-segment retention: for each shared key, does the FAST episodic store
    still return the value it was bound to in the FINAL (current) segment? Abstain /
    wrong = NOT retained (honest)."""
    final = V[len(V) - 1]
    correct = 0
    for i, a in enumerate(A):
        pred, _, _ = store.recall(key_vec(a))
        if pred == final[i]:
            correct += 1
    return correct / max(1, len(A))


def grid_tune_no_flush(n_keys, n_segments, n_distract, tune_seed, fast_cap, slow_cap):
    """NO-FLUSH CLS baseline is the BEST FIXED (LR,TH) over a grid on a DISJOINT seed
    (anti-confound: NE-flush must beat the strongest honest no-flush CLS)."""
    best = None
    for LR in (0.1, 0.2, 0.3, 0.4):
        for TH in (0.2, 0.3, 0.4):
            rng = np.random.default_rng(tune_seed)
            A, V, D = make_multicontext(n_keys, n_segments, n_distract, rng)
            r = run_cls(A, V, D, fast_cap, slow_cap, LR, TH, 0.45, flush_mode='none')
            if best is None or r > best[0]:
                best = (r, LR, TH)
    return best[1], best[2]


def main():
    N_KEYS = 24
    N_SEGMENTS = 3            # AB / AC / AD on the shared keys
    N_DISTRACT = 12           # per segment
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    # AMPLE capacity (interference, NOT capacity, is the test — H_1532 framing): no
    # eviction, so all 3 segments' same-key cells coexist in fast when un-flushed →
    # the stale seg-0 binding shadows the current one at the exact-key tie. SLOW large.
    FAST_CAP = (N_KEYS + N_DISTRACT) * N_SEGMENTS * 3  # 324 (ample, no eviction)
    SLOW_CAP = (N_KEYS + N_DISTRACT) * N_SEGMENTS * 3  # 324 (ample)

    LR_star, TH_star = grid_tune_no_flush(N_KEYS, N_SEGMENTS, N_DISTRACT, TUNE_SEED,
                                          FAST_CAP, SLOW_CAP)

    rows = []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        A, V, D = make_multicontext(N_KEYS, N_SEGMENTS, N_DISTRACT, rng)
        ne   = run_cls(A, V, D, FAST_CAP, SLOW_CAP, LR_star, TH_star, ABSTAIN0,
                       flush_mode='boundary')
        nof  = run_cls(A, V, D, FAST_CAP, SLOW_CAP, LR_star, TH_star, ABSTAIN0,
                       flush_mode='none')
        alw  = run_cls(A, V, D, FAST_CAP, SLOW_CAP, LR_star, TH_star, ABSTAIN0,
                       flush_mode='always')
        abl  = run_cls(A, V, D, FAST_CAP, SLOW_CAP, LR_star, TH_star, ABSTAIN0,
                       flush_mode='none')   # boundary signal const -> never flush
        shf  = run_cls(A, V, D, FAST_CAP, SLOW_CAP, LR_star, TH_star, ABSTAIN0,
                       flush_mode='boundary', shuffle=True, seed=seed)
        rows.append({'seed': seed,
                     'ne_flush': round(ne, 4), 'no_flush': round(nof, 4),
                     'always_flush': round(alw, 4), 'abl': round(abl, 4),
                     'shuffle': round(shf, 4),
                     'ne_minus_noflush': round(ne - nof, 4)})

    ne_m  = float(np.mean([r['ne_flush'] for r in rows]))
    nof_m = float(np.mean([r['no_flush'] for r in rows]))
    alw_m = float(np.mean([r['always_flush'] for r in rows]))
    abl_m = float(np.mean([r['abl'] for r in rows]))
    shf_m = float(np.mean([r['shuffle'] for r in rows]))

    # ── FROZEN falsifier (pre-registered in H_1544_FREEZE.txt) ────────────────
    #   A PRESENCE : ne_flush - no_flush >= +MARGIN on >= 2/3 seeds
    #   B DISTINCT : no_flush suffers cross-segment interference (no_flush < ne_flush
    #                - MARGIN, mean) AND always_flush loses within-segment
    #                (always_flush < ne_flush - MARGIN, mean)
    #   C EARNED   : ABL (boundary const -> never flush) reverts to no_flush
    #                (|abl - no_flush| < MARGIN, mean)
    #   D SHUFFLE  : permuted-boundary flush COLLAPSES (ne_flush - shuffle >= MARGIN, mean)
    #   E NO-FAB   : the win is current-segment binding retention, exact ground truth
    n_win = sum(1 for r in rows if r['ne_minus_noflush'] >= MARGIN)
    presence = n_win >= 2
    distinct = (nof_m < ne_m - MARGIN) and (alw_m < ne_m - MARGIN)
    earned   = abs(abl_m - nof_m) < MARGIN
    shuffle_collapses = (ne_m - shf_m) >= MARGIN

    if presence and distinct and earned and shuffle_collapses:
        verdict = 'GREEN'   # NE-reset is LOAD-BEARING once a fast store exists to flush
    elif presence:
        verdict = 'AMBIGUOUS_ABLATION'
    else:
        verdict = 'WALL_HOLDS'   # NE-flush ties/loses even inside the CLS structure

    summary = {
        'capability': 'multi-context interference: current-segment binding retention '
                      'after AB/AC/AD re-binding on shared keys',
        'reopen_of': 'H_1537 (NE-reset standalone 🧱 +0.006) / H_1539 '
                     '(NE-reset retry standalone 🧱 -0.0049) INSIDE H_1532 CLS',
        'LR_star': LR_star, 'TH_star': TH_star,
        'N_KEYS': N_KEYS, 'N_SEGMENTS': N_SEGMENTS, 'N_DISTRACT': N_DISTRACT,
        'FAST_CAP': FAST_CAP, 'SLOW_CAP': SLOW_CAP,
        'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
        'per_seed': rows,
        'ne_flush_mean': round(ne_m, 4),
        'no_flush_mean': round(nof_m, 4),
        'always_flush_mean': round(alw_m, 4),
        'abl_mean': round(abl_m, 4),
        'shuffle_mean': round(shf_m, 4),
        'ne_minus_noflush_mean': round(ne_m - nof_m, 4),
        'ne_minus_alwaysflush_mean': round(ne_m - alw_m, 4),
        'abl_minus_noflush_mean': round(abl_m - nof_m, 4),
        'ne_minus_shuffle_mean': round(ne_m - shf_m, 4),
        'n_wins_over_noflush+MARGIN': n_win,
        'presence': bool(presence),
        'distinct': bool(distinct),
        'earned_abl_reverts': bool(earned),
        'shuffle_collapses': bool(shuffle_collapses),
        'verdict': verdict,
        'reopened_standalone_wall': bool(verdict == 'GREEN'),
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
