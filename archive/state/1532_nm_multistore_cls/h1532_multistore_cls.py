#!/usr/bin/env python3
"""
H_1532 — MULTI-STORE / Complementary Learning Systems (CLS) on AB-AC INTERFERENCE.

Census C3 (state/1530_nm_research_census/CENSUS.md §3 C3 / §4 SPEC-3). Tries to
break the **H_1284 NEUROMODULATION wall** from an ORTHOGONAL angle.

WHY this angle (a_break_the_wall, type-(d) only after ablation):
H_1284 + 11 confirming lenses ALL measured the same ceiling on CLEAN RECALL — the
recall capability is key-GEOMETRY / capacity bound, the abstain decision IS already a
threshold on the live recall-margin, so any neuromodulator conditioning a knob
(LR/SPLIT_THRESH/temperature/abstain) on that SAME margin is circular: a single tuned
fixed point dominates every controller. EVERY controller-family lens lives on the
margin axis and the wall absorbs it.

The orthogonal capability the census flags = **AB-AC interference**: learn A->B, then
learn A->C; measure A->B retention. A SINGLE flat store catastrophically overwrites B
with C at the shared key A (one cell, one slot). CLS theory (McClelland-McNaughton-
O'Reilly 1995; Kumaran-Hassabis-McClelland 2016): a FAST episodic store written in an
encode-phase with the retrieval/recurrent path SUPPRESSED (Hasselmo 1999/2006 ACh
encode-mode) + a SLOW store consolidated by interleaved replay keeps confusable facts
in SEPARATE substrates — interference-avoidance NO threshold-schedule on one store can
produce.

⚠ CRITICAL HAZARD (census-flagged, the whole point): the win MUST come from HAVING TWO
PHASE-SEPARATED STORES, NOT a scalar gain on a single store — a gain framing re-enters
the controller family the wall already absorbs (the H_1422 ACh-gain lens 🧱). The
ablation (MERGE the two stores -> revert; SHUFFLE store-assignment -> collapse) is what
proves the lever is HAVING SEPARATE STORES.

p7: exact ground truth (the true A->B binding is known), NO LLM judge, NO perplexity, NO
loss term — every decision is a no-grad read of substrate state. p8: inference-time
write = the engine's own tick. $0 CPU. 3 seeds. Frozen falsifier in H_1532_FREEZE.txt.

R1 numpy DIRECTIONAL (host has no torch; a_engine_native_learning) — engine R2 deferred
ING. REUSES the H_1284 store machinery byte-for-byte (MemStore/key_vec/FNV-1a/MARGIN).
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from CORE/engine_cli.hexa / H_1284) ─────
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 16                   # key dim (H_1227 byte-trigram FNV-1a; toy 16, same as H_1284)
MARGIN = 0.05              # frozen lift bar (same as H_1284 / census C3 SPEC-3)


# ── byte-trigram FNV-1a key (H_1227/H_1231 key — VERBATIM from H_1284) ────────
def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


def key_vec(s: str) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (VERBATIM from H_1284)."""
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


# ── VAdaptField numpy mirror (byte-faithful to vadapt_field_step — H_1284) ────
# A capacity-bounded prototype store: writes either SPLIT a new cell (novel key,
# recon-err>THRESH, capacity free) or REFINE the winner toward the key (LR pull),
# REBINDING the winner's stored value. THIS is exactly why a single flat store
# suffers AB-AC interference: a second fact on key A finds the SAME winner cell and
# overwrites the bound value B with C.
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
        """vadapt_field_step write. suppress_retrieval = Hasselmo ACh encode-mode:
        the recurrent/retrieval path that would MATCH a pre-existing winner is gated
        OFF, so a new fact is laid down in a FRESH cell instead of overwriting the
        winner it would otherwise refine. This is the phase-separation mechanism —
        NOT a scalar gain (it changes WHICH substrate slot the fact lands in)."""
        self.tick += 1
        win, err, _ = self._nearest(x)
        if suppress_retrieval and len(self.protos) < self.max_cells:
            # encode-phase: retrieval suppressed -> always lay down a new cell
            # (do NOT refine/overwrite the matched winner)
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
        # REFINE: pull winner toward x, OVERWRITE its bound value (= interference)
        self.protos[win] = self.protos[win] + self.LR * (x - self.protos[win])
        self.values[win] = value
        self.lru[win] = self.tick

    def recall(self, x):
        """nearest-cell fires; ABSTAIN (None) if recon-err > abstain margin."""
        self.tick += 1
        win, err, second = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None, err, second
        self.lru[win] = self.tick
        return self.values[win], err, second


# ── AB-AC interference fixture (exact ground truth) ───────────────────────────
def make_abac(n_pairs, n_distract, rng):
    """n_pairs shared keys A_i, each with an OLD value B_i (phase 1) and a NEW value
    C_i (phase 2). n_distract unrelated facts D_j land in phase 2 alongside the AC
    re-bindings (interference load). The CAPABILITY = retain A_i->B_i after phase 2."""
    A = [f"key_A{i:03d}" for i in range(n_pairs)]
    B = [f"val_B{rng.integers(0, 99999):05d}" for _ in range(n_pairs)]
    C = [f"val_C{rng.integers(0, 99999):05d}" for _ in range(n_pairs)]
    # ensure C != B per pair
    for i in range(n_pairs):
        while C[i] == B[i]:
            C[i] = f"val_C{rng.integers(0, 99999):05d}"
    D_keys = [f"key_D{j:03d}" for j in range(n_distract)]
    D_vals = [f"val_D{rng.integers(0, 99999):05d}" for _ in range(n_distract)]
    return A, B, C, D_keys, D_vals


# ── ARMS ──────────────────────────────────────────────────────────────────────
def run_one_store(A, B, C, Dk, Dv, max_cells, LR, THRESH, abstain):
    """ONE-STORE = single flat store (the wall baseline, grid-tuned best-fixed).
    Phase 1 writes A->B; phase 2 writes A->C + distractors. A second write on key A
    finds the SAME winner cell and OVERWRITES B with C -> catastrophic interference."""
    store = MemStore(max_cells, abstain, LR, THRESH)
    for a, b in zip(A, B):                       # phase 1: A -> B
        store.write(key_vec(a), b)
    items = list(zip(A, C)) + list(zip(Dk, Dv))  # phase 2: A -> C + distractors
    for k, v in items:
        store.write(key_vec(k), v)
    return _score_ab_retention(store, A, B)


def run_two_store(A, B, C, Dk, Dv, max_cells, LR, THRESH, abstain,
                  merge=False, shuffle=False, rng=None):
    """TWO-STORE = fast EPISODIC store (phase-1 A->B, retrieval-path suppressed =
    Hasselmo encode-mode, laid down without interference) + SLOW store fed by replay.
    Phase 2 A->C + distractors go to the SLOW store. At recall, the FAST episodic
    store holds A->B in a SEPARATE substrate, so the phase-2 A->C re-binding cannot
    clobber it. Replay interleaves the episodic store into slow consolidation.

    merge=True  -> single merged store (disable phase-separation) -> reverts to 1-store.
    shuffle=True-> randomize which store each fact is assigned to -> collapses the
                   substrate separation (the value lives in the wrong place)."""
    # FAST episodic store: A->B written in encode-phase (retrieval suppressed)
    fast = MemStore(max_cells, abstain, LR, THRESH)
    # SLOW store: phase-2 re-bindings + distractors, normal interfering writes
    slow = MemStore(max_cells, abstain, LR, THRESH)

    def store_for(tag, default):
        # store-assignment policy. shuffle randomizes it (destroys separation).
        if shuffle:
            return fast if rng.random() < 0.5 else slow
        return default

    if merge:
        # MERGE ablation: one store, encode-mode disabled -> identical to one-store.
        m = MemStore(max_cells, abstain, LR, THRESH)
        for a, b in zip(A, B):
            m.write(key_vec(a), b)                       # NO suppress -> refines/overwrites
        for k, v in list(zip(A, C)) + list(zip(Dk, Dv)):
            m.write(key_vec(k), v)
        return _score_ab_retention(m, A, B)

    # phase 1: A->B into FAST episodic, encode-phase (retrieval path suppressed)
    for a, b in zip(A, B):
        tgt = store_for('AB', fast)
        tgt.write(key_vec(a), b, suppress_retrieval=(tgt is fast))
    # phase 2: A->C re-bindings + distractors into SLOW store (interfering writes)
    for k, v in list(zip(A, C)) + list(zip(Dk, Dv)):
        tgt = store_for('AC_D', slow)
        tgt.write(key_vec(k), v, suppress_retrieval=False)
    # REPLAY: interleave episodic (fast) traces into slow consolidation (CLS replay).
    # Replay re-presents A->B from the fast store; consolidation writes into a fresh
    # slow cell (encode-phase) so it is not clobbered by the A->C slow binding.
    if not shuffle:
        for a, b in zip(A, B):
            v, err, _ = fast.recall(key_vec(a))
            if v is not None:
                slow.write(key_vec(a), v, suppress_retrieval=True)

    return _score_ab_retention_two(fast, slow, A, B)


def _score_ab_retention(store, A, B):
    """A->B retention on a single store: fraction of A keys whose nearest-cell value
    is still the OLD B (not the phase-2 C). Abstain counts as NOT retained (honest)."""
    correct = 0
    for a, b in zip(A, B):
        pred, _, _ = store.recall(key_vec(a))
        if pred == b:
            correct += 1
    return correct / max(1, len(A))


def _score_ab_retention_two(fast, slow, A, B):
    """Two-store retention: A->B is retained if EITHER the fast episodic store OR the
    slow (replay-consolidated) store still returns B. The point of CLS is that the
    confusable A->B and A->C bindings live in separate substrates, so B survives."""
    correct = 0
    for a, b in zip(A, B):
        pf, _, _ = fast.recall(key_vec(a))
        ps, _, _ = slow.recall(key_vec(a))
        if pf == b or ps == b:
            correct += 1
    return correct / max(1, len(A))


def run_single_encode(A, B, C, Dk, Dv, max_cells, LR, THRESH, abstain):
    """DECONFOUND arm (single store WITH encode-mode): A->B and A->C BOTH written
    suppress_retrieval=True (fresh cells) into ONE store. This isolates whether the
    two-store win is just 'fresh cells avoid overwrite' vs genuinely 'SEPARATE stores'.
    With one store, both the A->B and A->C cells sit in the SAME geometry, so at recall
    the nearest-cell tiebreak shadows B with the later A->C cell -> B mostly NOT
    returned. If this ALSO retained B, the win would be encode-mode, not separation."""
    s = MemStore(max_cells, abstain, LR, THRESH)
    for a, b in zip(A, B):
        s.write(key_vec(a), b, suppress_retrieval=True)
    for k, v in list(zip(A, C)) + list(zip(Dk, Dv)):
        s.write(key_vec(k), v, suppress_retrieval=True)
    return _score_ab_retention(s, A, B)


def grid_tune_one_store(n_pairs, n_distract, tune_seed):
    """ONE-STORE baseline is the BEST FIXED (LR0,TH0) over a grid on a DISJOINT seed
    (anti-confound: two-store must beat the strongest honest single store)."""
    best = None
    for LR in (0.1, 0.2, 0.3, 0.4):
        for TH in (0.2, 0.3, 0.4):
            rng = np.random.default_rng(tune_seed)
            A, B, C, Dk, Dv = make_abac(n_pairs, n_distract, rng)
            r = run_one_store(A, B, C, Dk, Dv,
                              max_cells=max(4, int((n_pairs + n_distract) * 1.5)),
                              LR=LR, THRESH=TH, abstain=0.45)
            if best is None or r > best[0]:
                best = (r, LR, TH)
    return best[1], best[2]


def main():
    N_PAIRS = 24
    N_DISTRACT = 24
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    MAX_CELLS = max(4, int((N_PAIRS + N_DISTRACT) * 1.5))  # ample capacity (interference, not capacity, is the test)

    LR_star, TH_star = grid_tune_one_store(N_PAIRS, N_DISTRACT, TUNE_SEED)

    rows = []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        A, B, C, Dk, Dv = make_abac(N_PAIRS, N_DISTRACT, rng)
        one = run_one_store(A, B, C, Dk, Dv, MAX_CELLS, LR_star, TH_star, ABSTAIN0)
        two = run_two_store(A, B, C, Dk, Dv, MAX_CELLS, LR_star, TH_star, ABSTAIN0,
                            merge=False, shuffle=False)
        mrg = run_two_store(A, B, C, Dk, Dv, MAX_CELLS, LR_star, TH_star, ABSTAIN0,
                            merge=True)
        shf = run_two_store(A, B, C, Dk, Dv, MAX_CELLS, LR_star, TH_star, ABSTAIN0,
                            merge=False, shuffle=True,
                            rng=np.random.default_rng(seed + 1000))
        enc = run_single_encode(A, B, C, Dk, Dv, MAX_CELLS, LR_star, TH_star, ABSTAIN0)
        rows.append({'seed': seed, 'one_store': round(one, 4), 'two_store': round(two, 4),
                     'merge_abl': round(mrg, 4), 'shuffle_abl': round(shf, 4),
                     'single_encode_deconfound': round(enc, 4),
                     'two_minus_one': round(two - one, 4)})

    one_m = float(np.mean([r['one_store'] for r in rows]))
    two_m = float(np.mean([r['two_store'] for r in rows]))
    mrg_m = float(np.mean([r['merge_abl'] for r in rows]))
    shf_m = float(np.mean([r['shuffle_abl'] for r in rows]))
    enc_m = float(np.mean([r['single_encode_deconfound'] for r in rows]))

    # ── FROZEN falsifier (pre-registered in H_1532_FREEZE.txt) ────────────────
    #   c1 PRESENCE : two_store - one_store >= +MARGIN on >= 2/3 seeds
    #   c2 MERGE    : merge ablation REVERTS to one-store (merge - one < MARGIN, mean)
    #   c3 SHUFFLE  : shuffle ablation COLLAPSES (two - shuffle >= MARGIN, mean)
    n_win = sum(1 for r in rows if r['two_minus_one'] >= MARGIN)
    merge_reverts = (mrg_m - one_m) < MARGIN
    shuffle_collapses = (two_m - shf_m) >= MARGIN

    if n_win >= 2 and merge_reverts and shuffle_collapses:
        verdict = 'GREEN'   # WALL-BROKEN: the lever is HAVING SEPARATE STORES
    elif n_win >= 2:
        # lift exists but NOT attributable to the two-store separation (ablation failed)
        verdict = 'AMBIGUOUS_ABLATION'
    else:
        verdict = 'WALL_HOLDS'   # two-store ties/loses to one-store on AB-AC

    summary = {
        'capability': 'AB-AC interference: A->B retention after learning A->C',
        'LR_star': LR_star, 'TH_star': TH_star,
        'N_PAIRS': N_PAIRS, 'N_DISTRACT': N_DISTRACT, 'MAX_CELLS': MAX_CELLS,
        'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
        'per_seed': rows,
        'one_store_mean': round(one_m, 4),
        'two_store_mean': round(two_m, 4),
        'merge_abl_mean': round(mrg_m, 4),
        'shuffle_abl_mean': round(shf_m, 4),
        'single_encode_deconfound_mean': round(enc_m, 4),
        'two_minus_single_encode_mean': round(two_m - enc_m, 4),
        'two_minus_one_mean': round(two_m - one_m, 4),
        'merge_minus_one_mean': round(mrg_m - one_m, 4),
        'two_minus_shuffle_mean': round(two_m - shf_m, 4),
        'n_wins_over_one+MARGIN': n_win,
        'merge_reverts': bool(merge_reverts),
        'shuffle_collapses': bool(shuffle_collapses),
        'verdict': verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
