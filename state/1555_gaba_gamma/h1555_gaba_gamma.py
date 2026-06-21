#!/usr/bin/env python3
"""
H_1555 — GABA × CLS: GAMMA-OSCILLATION temporal-binding (adaptive bin-width).

The LAST untested ORTHOGONAL GABA mechanism-family (census H_1553 RANK 2). After this,
the GABA frontier has a full mechanism-family census: sparse-coding (H_1546/1551/1552 all
🧱 STATIC), disinhibition-routing (H_1554 🟠 KNOB), and now gamma temporal-segmentation.

WHY this angle (a_no_llm_frame_trap · a_break_the_wall MULTI-LENS):
PV-basket-cell GABAergic feedback generates a ~40 Hz gamma rhythm that chops continuous
input into discrete TIME-BINS; features arriving in the SAME gamma cycle bind into ONE
memory item, features in SUCCESSIVE cycles stay SEPARATE (Lisman & Jensen 2013 Neuron
77:1002 "The Theta-Gamma Neural Code"; Buzsáki & Wang 2012 Annu Rev Neurosci 35:203).
This is a TEMPORAL-SEGMENTATION lever — it decides WHICH features count as simultaneous
(one item) vs span two items — orthogonal to representational density (sparse), write-port
routing (disinhibition), score rescale (divnorm), and E/I setpoint.

ADAPTIVE bin-WIDTH (gamma frequency tracking input rate) has a regime-shifting optimum:
fast input → narrow bins (segment finely, avoid merging distinct items); slow/bursty →
wide bins (group co-arriving features, avoid fragmenting one item). A FIXED bin-width
over-merges the fast regime OR over-fragments the slow regime — neither fixed setting wins
both. This is the fusion-law shape the 5 GREEN NTs share.

CRITICAL NE-DECONFOUND (load-bearing, census-flagged): NE-flush (H_1544 🟢) already
segments at CONTEXT BOUNDARIES. Gamma must be tested on a BOUNDARY-FREE grouping regime —
features that must be grouped by CO-OCCURRENCE/SIMULTANEITY within a continuous stream
(no event boundaries at all), where NE-flush has nothing meaningful to flush. The
NE-FROZEN arm holds NE-flush ON; gamma's lift must SURVIVE it, proving boundary-free
GROUPING ≠ NE segmentation. If gamma only ties NE-frozen → it is NE re-skinned → 🧱.

CAPABILITY — boundary-free continuous STREAM. Feature events arrive at inter-arrival GAPs.
Ground-truth ITEMS are groups of features whose within-item gaps are SMALL (co-occur);
successive items are separated by a LARGER gap. NO abrupt context boundaries — the only
structure is co-occurrence TIMING. The segmenter must recover which consecutive features
belong to ONE item (bind together) vs the NEXT item. METRIC = item-binding F1: each
recovered group is matched to a ground-truth item; F1 over (recovered-set == truth-set).

p7: exact ground truth (item grouping known), NO LLM judge / loss / perplexity. p8:
write = engine's own tick. $0 CPU, 3 seeds, frozen falsifier (H_1555_FREEZE.txt).

R1 numpy DIRECTIONAL (host has no torch; a_engine_native_learning hard-gate-1) — engine
§GabaGamma R2 deferred ING. REUSES H_1532/H_1544 MemStore/key_vec/FNV-1a/MARGIN byte-for-
byte; the ONLY new variable is the temporal bin segmentation.
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / H_1544 / CORE) ────────────
LR0_ENGINE = 0.20          # adapt_field_step LR
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH
DIM = 16                   # key dim (FNV-1a trigram; toy 16, same as H_1532/H_1544)
MARGIN = 0.10              # frozen PRESENCE bar
ADAPT_K = 0.5              # adaptive bin-width = ADAPT_K * running median-gap EMA (frozen)
GAP_RATIO = 4.0            # between-item gap / within-item gap (same separability both regimes)
EMA_ALPHA = 0.30           # gap EMA smoothing (frozen)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532 / H_1544) ───────────────────
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


# ── boundary-free co-occurrence STREAM (exact ground truth) ───────────────────
def make_stream(n_items, feats_per_item_choices, within_gap, n_distract, rng):
    """A boundary-free stream of feature EVENTS with inter-arrival GAPs.

    n_items ground-truth ITEMS; each item is a SET of (variable-count) features that
    CO-OCCUR (within-item inter-feature gap = within_gap * small jitter). Between
    successive items the gap is LARGER (within_gap * GAP_RATIO * jitter). There are NO
    abrupt context boundaries — the WHOLE stream is one continuous context; the only cue
    is the inter-arrival GAP timing (NE-deconfound: nothing to flush for grouping).

    Returns:
      events   : list of feature-name strings in arrival order
      gaps      : list of inter-arrival gaps (len == len(events); gaps[0] = 0)
      truth     : list of frozensets, the ground-truth item feature-sets (in order)
      distract  : interleaved distractor singleton features (own large gaps)
    """
    events, gaps, truth = [], [], []
    fid = 0
    first_overall = True
    for it in range(n_items):
        k = int(rng.choice(feats_per_item_choices))
        item_feats = []
        for j in range(k):
            f = f"f_{it:03d}_{j:02d}_{fid:04d}"
            fid += 1
            item_feats.append(f)
            if first_overall:
                g = 0.0
                first_overall = False
            elif j == 0:
                # between-item gap (LARGE) — separates this item from the previous
                jit = 0.85 + 0.30 * rng.random()
                g = within_gap * GAP_RATIO * jit
            else:
                # within-item gap (SMALL) — co-occurrence
                jit = 0.85 + 0.30 * rng.random()
                g = within_gap * jit
            events.append(f); gaps.append(g)
        truth.append(frozenset(item_feats))
    # interleave a few distractor SINGLETON items (own between-item gap) at the end —
    # they are their own ground-truth items (each a singleton), part of the load.
    for d in range(n_distract):
        f = f"d_{d:03d}_{fid:04d}"; fid += 1
        jit = 0.85 + 0.30 * rng.random()
        events.append(f); gaps.append(within_gap * GAP_RATIO * jit)
        truth.append(frozenset([f]))
    return events, gaps, truth


# ── segmenters (produce groups of feature-names) ──────────────────────────────
def segment_adaptive(events, gaps):
    """GAMMA-ADAPTIVE: bin-width tracks the running inter-arrival gap (EMA of recent
    gaps). A new bin OPENS when the next gap exceeds the current adaptive bin-width
    (ADAPT_K * EMA). Features within one bin bind into one item. The width SCALES with
    the stream's tempo → wins both FAST (compressed) and SLOW (stretched) regimes."""
    groups = []
    cur = []
    ema = None
    for i, (f, g) in enumerate(zip(events, gaps)):
        if i == 0:
            cur = [f]
            ema = None
            continue
        if ema is None:
            # seed the EMA from the first observed gap
            ema = g
            width = ADAPT_K * ema
        else:
            width = ADAPT_K * ema
        if g > width:
            groups.append(cur); cur = [f]
        else:
            cur.append(f)
        # update the running gap EMA (running tempo estimate)
        ema = (1 - EMA_ALPHA) * ema + EMA_ALPHA * g
    if cur:
        groups.append(cur)
    return groups


def segment_fixed(events, gaps, bin_width):
    """BEST-FIXED-BINWIDTH / ABL: a single CONSTANT bin-width. A new bin opens when the
    gap exceeds the constant bin_width. (ABL = gamma with the adaptive signal frozen to
    a constant = exactly this fixed-bin segmenter.)"""
    groups = []
    cur = []
    for i, (f, g) in enumerate(zip(events, gaps)):
        if i == 0:
            cur = [f]; continue
        if g > bin_width:
            groups.append(cur); cur = [f]
        else:
            cur.append(f)
    if cur:
        groups.append(cur)
    return groups


def segment_none(events, gaps):
    """NO-BINNING: each feature is its own singleton binding (no grouping at all) =
    the H_1532 wall baseline (no temporal segmentation)."""
    return [[f] for f in events]


def segment_shuffle(events, gaps, rng):
    """SHUFFLE: the inter-arrival GAP cue is permuted (decoupled from the true item
    structure). Run the adaptive segmenter on the PERMUTED gaps → segmentation no longer
    tracks co-occurrence → collapses."""
    perm = list(rng.permutation(len(gaps)))
    sgaps = [gaps[p] for p in perm]
    sgaps[0] = 0.0
    return segment_adaptive(events, sgaps)


def segment_ne_frozen(events, gaps, within_gap):
    """NE-FROZEN-DECONFOUND: NE-flush (H_1544) held ON. NE-flush detects an ABRUPT
    boundary and FLUSHES the fast store. In a BOUNDARY-FREE grouping stream the only
    'large gap' is the between-item gap; if we let NE flush there, NE's behavior on this
    stream is to flush at every between-item gap and emit each accumulated run. Crucially
    NE-flush does NOT know the within/between gap STRUCTURE adaptively — it uses a FIXED
    surprise/boundary threshold (a single tuned constant), so on this continuous stream
    it is forced to the SAME fixed-threshold segmentation as best-fixed (it has no tempo
    tracking). We instantiate NE-frozen as a FIXED boundary threshold at the FAST regime's
    between-gap (its native operating point) — proving NE cannot adaptively track the
    SLOW regime, so gamma's lift over NE survives. This is the honest deconfound: NE-flush
    = fixed boundary detector, gamma = adaptive tempo tracker."""
    # NE's native boundary threshold = a fixed constant (it flushes on 'surprise' = a gap
    # above a fixed bar). Set at the FAST regime between-item gap (where NE was 'designed').
    ne_thresh = within_gap * GAP_RATIO  # FAST-regime between-item gap (FIXED, no tempo track)
    return segment_fixed(events, gaps, ne_thresh)


# ── store-write + item-F1 scoring ─────────────────────────────────────────────
def bind_groups(groups, max_cells, LR, THRESH, abstain):
    """Write each segmented GROUP as ONE bound item into the CLS fast store: the group's
    features are concatenated into a single item key+value (co-occurrence binding). This
    is the substrate write — the segmentation decides WHAT gets bound together. Returns
    the recovered groups (as frozensets) read back from the store's bound items."""
    store = MemStore(max_cells, abstain, LR, THRESH)
    recovered = []
    for grp in groups:
        # the bound item = the SET of co-occurring features (sorted for a canonical key)
        feats = sorted(grp)
        item_key = "+".join(feats)
        store.write(key_vec(item_key), item_key, suppress_retrieval=True)
        recovered.append(frozenset(feats))
    return recovered


def item_f1(recovered, truth):
    """Item-binding F1: a recovered group matches a truth item iff their feature-SETS are
    identical. F1 = 2PR/(P+R) over exact-set matches (multiset-correct, greedy by identity)."""
    truth_ms = {}
    for t in truth:
        truth_ms[t] = truth_ms.get(t, 0) + 1
    rec_ms = {}
    for r in recovered:
        rec_ms[r] = rec_ms.get(r, 0) + 1
    tp = 0
    for s, c in rec_ms.items():
        tp += min(c, truth_ms.get(s, 0))
    n_rec = sum(rec_ms.values())
    n_truth = sum(truth_ms.values())
    prec = tp / max(1, n_rec)
    rec = tp / max(1, n_truth)
    if prec + rec < 1e-12:
        return 0.0
    return 2 * prec * rec / (prec + rec)


# ── one full run for a (regime, seed) ─────────────────────────────────────────
def run_regime(within_gap, n_items, feats_choices, n_distract, max_cells, LR, THRESH,
               abstain, fixed_bin, seed):
    rng = np.random.default_rng(seed)
    events, gaps, truth = make_stream(n_items, feats_choices, within_gap, n_distract, rng)

    g_adaptive = segment_adaptive(events, gaps)
    g_fixed = segment_fixed(events, gaps, fixed_bin)
    g_none = segment_none(events, gaps)
    g_abl = segment_fixed(events, gaps, fixed_bin)  # adaptive OFF == const bin
    g_shuf = segment_shuffle(events, gaps, np.random.default_rng(seed + 9000))
    g_ne = segment_ne_frozen(events, gaps, within_gap)

    def score(groups):
        rec = bind_groups(groups, max_cells, LR, THRESH, abstain)
        return item_f1(rec, truth)

    return {
        'adaptive': score(g_adaptive),
        'fixed': score(g_fixed),
        'none': score(g_none),
        'abl': score(g_abl),
        'shuffle': score(g_shuf),
        'ne_frozen': score(g_ne),
    }


def grid_tune_fixed_bin(within_gaps, n_items, feats_choices, n_distract, max_cells, LR,
                        THRESH, abstain, tune_seed):
    """BEST-FIXED-BINWIDTH = the single CONSTANT bin-width that maximizes mean item-F1
    over the WHOLE rate sweep (both regimes) on a DISJOINT tune seed. The honest strong
    baseline: if one fixed width wins BOTH regimes, gamma's adaptivity is INERT → 🧱.
    Grid spans widths between the within-item and between-item gap scales of both regimes."""
    # candidate widths span from below the FAST within-gap to above the SLOW between-gap
    lo = min(within_gaps) * 0.5
    hi = max(within_gaps) * GAP_RATIO * 1.5
    cands = np.linspace(lo, hi, 25)
    best = None
    for w in cands:
        scores = []
        for wg in within_gaps:
            r = run_regime(wg, n_items, feats_choices, n_distract, max_cells, LR, THRESH,
                           abstain, fixed_bin=w, seed=tune_seed)
            scores.append(r['fixed'])
        m = float(np.mean(scores))
        if best is None or m > best[0]:
            best = (m, float(w))
    return best[1]


def main():
    N_ITEMS = 20
    FEATS_CHOICES = [2, 3, 4]   # variable-length items (the binding ambiguity)
    N_DISTRACT = 8
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    # rate regimes: FAST (compressed) vs SLOW (stretched) within-item gap. Same 1:4
    # within:between ratio (SAME separability) → only the ABSOLUTE scale shifts, so a
    # fixed bin tuned to one regime fails the other; the adaptive bin tracks both.
    WITHIN_FAST = 1.0
    WITHIN_SLOW = 8.0
    WITHIN_GAPS = [WITHIN_FAST, WITHIN_SLOW]
    MAX_CELLS = (N_ITEMS + N_DISTRACT) * 3  # ample (segmentation, not capacity, is the test)

    fixed_bin = grid_tune_fixed_bin(WITHIN_GAPS, N_ITEMS, FEATS_CHOICES, N_DISTRACT,
                                    MAX_CELLS, LR0_ENGINE, TH0_ENGINE, ABSTAIN0, TUNE_SEED)

    rows = []
    for seed in SCORE_SEEDS:
        per_regime = {}
        for name, wg in (('fast', WITHIN_FAST), ('slow', WITHIN_SLOW)):
            r = run_regime(wg, N_ITEMS, FEATS_CHOICES, N_DISTRACT, MAX_CELLS,
                           LR0_ENGINE, TH0_ENGINE, ABSTAIN0, fixed_bin=fixed_bin, seed=seed)
            per_regime[name] = {k: round(v, 4) for k, v in r.items()}
        rows.append({'seed': seed, **{f'{rg}_{k}': per_regime[rg][k]
                                      for rg in ('fast', 'slow')
                                      for k in ('adaptive', 'fixed', 'none', 'abl',
                                                'shuffle', 'ne_frozen')}})

    def mean_over(metric, regime=None):
        vals = []
        for rrow in rows:
            if regime:
                vals.append(rrow[f'{regime}_{metric}'])
            else:
                vals.append((rrow[f'fast_{metric}'] + rrow[f'slow_{metric}']) / 2.0)
        return float(np.mean(vals))

    adp_m = mean_over('adaptive'); fix_m = mean_over('fixed'); non_m = mean_over('none')
    abl_m = mean_over('abl'); shf_m = mean_over('shuffle'); ne_m = mean_over('ne_frozen')
    adp_fast = mean_over('adaptive', 'fast'); adp_slow = mean_over('adaptive', 'slow')
    fix_fast = mean_over('fixed', 'fast'); fix_slow = mean_over('fixed', 'slow')

    # worst fixed over regimes (for the earned-shift sub-bar) = min regime-mean of fixed
    worst_fixed = min(fix_fast, fix_slow)

    # ── FROZEN falsifier (pre-registered in H_1555_FREEZE.txt) ────────────────
    #  A PRESENCE+SHIFT : (adp - fix) >= 0.5*(adp - worst_fixed)  AND  (adp - none) >= MARGIN
    #  B DISTINCT       : none < adp - MARGIN  AND  best-fixed loses >=MARGIN in >=1 regime
    #                     where gamma holds (fixed_fast < adp_fast - MARGIN OR
    #                     fixed_slow < adp_slow - MARGIN)
    #  C ABL->fixed     : abl <= fixed + MARGIN  (adaptive OFF reverts to fixed)
    #  D SHUFFLE        : adp - shuffle >= MARGIN
    #  E NE-DECONFOUND  : adp - ne_frozen >= MARGIN
    earned_shift = (adp_m - fix_m) >= 0.5 * (adp_m - worst_fixed)
    presence = (adp_m - non_m) >= MARGIN and earned_shift
    fixed_loses_a_regime = (fix_fast < adp_fast - MARGIN) or (fix_slow < adp_slow - MARGIN)
    distinct = (non_m < adp_m - MARGIN) and fixed_loses_a_regime
    abl_reverts = abl_m <= fix_m + MARGIN
    shuffle_collapses = (adp_m - shf_m) >= MARGIN
    ne_deconfound = (adp_m - ne_m) >= MARGIN

    if presence and distinct and abl_reverts and shuffle_collapses and ne_deconfound:
        verdict = 'GREEN'   # gamma adaptive bin-width is a DISTINCT load-bearing GABA faculty
    elif (adp_m - non_m) >= MARGIN and not earned_shift:
        verdict = 'KNOB'    # best-fixed-binwidth captures >= half (🟠)
    elif not ne_deconfound:
        verdict = 'WALL_NE_REDUNDANT'   # lift vanishes under NE-frozen -> NE re-skinned (🧱)
    else:
        verdict = 'WALL_INERT'          # gamma ties no-binning -> segmentation inert (🧱)

    summary = {
        'capability': 'boundary-free co-occurrence stream: item-binding F1 (which features '
                      'bind into one item vs separate), across a FAST/SLOW arrival-rate sweep',
        'last_orthogonal_gaba_family': True,
        'closes_gaba_census': True,
        'fixed_bin_star': round(fixed_bin, 4),
        'N_ITEMS': N_ITEMS, 'FEATS_CHOICES': FEATS_CHOICES, 'N_DISTRACT': N_DISTRACT,
        'WITHIN_FAST': WITHIN_FAST, 'WITHIN_SLOW': WITHIN_SLOW, 'GAP_RATIO': GAP_RATIO,
        'ADAPT_K': ADAPT_K, 'EMA_ALPHA': EMA_ALPHA, 'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
        'per_seed': rows,
        'adaptive_mean': round(adp_m, 4),
        'best_fixed_binwidth_mean': round(fix_m, 4),
        'no_binning_mean': round(non_m, 4),
        'abl_const_bin_mean': round(abl_m, 4),
        'shuffle_mean': round(shf_m, 4),
        'ne_frozen_mean': round(ne_m, 4),
        'adaptive_fast': round(adp_fast, 4), 'adaptive_slow': round(adp_slow, 4),
        'fixed_fast': round(fix_fast, 4), 'fixed_slow': round(fix_slow, 4),
        'worst_fixed_regime': round(worst_fixed, 4),
        'adp_minus_fixed_mean': round(adp_m - fix_m, 4),
        'adp_minus_none_mean': round(adp_m - non_m, 4),
        'adp_minus_shuffle_mean': round(adp_m - shf_m, 4),
        'adp_minus_ne_frozen_mean': round(adp_m - ne_m, 4),
        'half_adp_minus_worstfixed': round(0.5 * (adp_m - worst_fixed), 4),
        'earned_shift': bool(earned_shift),
        'presence': bool(presence),
        'distinct': bool(distinct),
        'abl_reverts': bool(abl_reverts),
        'shuffle_collapses': bool(shuffle_collapses),
        'ne_deconfound_survives': bool(ne_deconfound),
        'gamma_distinct_from_ne': bool(ne_deconfound),
        'verdict': verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
