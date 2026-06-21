#!/usr/bin/env python3
"""
H_1556 — GABA × CLS: SELF-ORGANIZED CRITICALITY (adaptive E/I tracking a SHIFTING critical point)
(the ESCAPE lens after GABA's 5 mechanism-families censused — sparse 🧱 ×3 / disinhibition 🟠 /
 gamma 🟠 / divisive-norm 🧱 / E-I-setpoint 🧱(skipped). The 6th GABA family.)

WHY THIS IS A GENUINELY NEW ESCAPE, NOT A 6th RE-HIT OF THE STATIC WALL (a_break_the_wall §3):
  GABA walled because in ALL 5 families its inhibitory benefit had a GLOBAL/STATIC optimum →
  a single grid-tuned fixed setting captured it (the FUSION LAW: a NT's adaptive lever beats a
  fixed setting ONLY where the optimal operating point SHIFTS over time/regime). The census
  SKIPPED the E/I-setpoint family (R4) as "a single fixed E/I target = monotone → re-tests the
  static wall." That skip is correct FOR A FIXED TARGET. CRITICALITY is the ONE escape it misses:

    The system is maximally expressive (max dynamic range / max distinct stored patterns) ONLY at
    the edge-of-chaos CRITICAL E/I ratio, where the branching ratio σ ≈ 1 (Beggs & Plenz 2003
    neuronal avalanches; Shew & Plenz 2013 functional benefits of criticality). The KEY difference
    from a fixed E/I setpoint: the critical E/I ratio is NOT a fixed target — it SHIFTS with the
    INPUT STATISTICS (drive variance / arrival rate). The same E/I that yields σ≈1 under one input
    regime yields σ<1 (subcritical, activity dies, patterns collapse) or σ>1 (supercritical,
    activity saturates, patterns merge) under a different input regime. So NO fixed E/I can hold
    criticality as the stream's statistics drift — exactly the SHIFTING-optimum condition the
    fusion law needs, and a capability the 5 phasic GREEN NTs do NOT provide (they don't set the
    E/I operating REGIME — they schedule LR/gate/abstain WITHIN a fixed regime).

  HONEST PRIOR (c9): if a single grid-tuned best-fixed-E/I STILL captures the benefit across the
  drift (i.e. one E/I happens to stay near-critical across all input regimes, OR criticality's
  capacity benefit is shallow enough that a compromise fixed E/I wins), that IS the scientific
  answer — GABA-as-adaptive is then exhausted across 6 distinct families = honest structural-NT
  ceiling, and 5/6 all-green (ACh/DA/NE/orexin/5-HT) is the honest campaign result. We pre-
  register the bars BEFORE the scored run and report whichever side honestly. NO tune-to-green.

THE CRITICALITY PHYSICS (why a fixed E/I cannot hold σ≈1 across drifting input statistics):
  We model a recurrent associative substrate as a 1-step branching process over DIM units. When a
  stored pattern is cued, each active unit recurrently re-activates its neighbours; the EXPECTED
  number of next-step active units per current active unit is the BRANCHING RATIO σ. σ is set by
    σ ≈ (recurrent excitatory gain) − (GABA inhibitory gain)        [E/I balance]
        scaled by the current input DRIVE LEVEL (more drive → more units cross threshold → higher
        effective fan-out).
  Retention of a cued pattern (the capability) is maximised at σ ≈ 1:
    • σ < 1 (SUBCRITICAL): each step loses activity → the cued pattern DIES before read-out →
      retention collapses (the pattern is under-recalled).
    • σ > 1 (SUPERCRITICAL): activity EXPLODES → unrelated units recruit → distinct stored patterns
      MERGE / saturate → retention collapses (cross-talk, the read-out is ambiguous).
    • σ ≈ 1 (CRITICAL): activity is self-sustaining without exploding → max distinct patterns
      co-resident → retention peaks.
  Because the DRIVE LEVEL (input statistic) drifts across the stream, a FIXED E/I yields a DRIFTING
  σ: tuned critical at one drive level, it goes subcritical when drive falls and supercritical when
  drive rises. GABA-CRITICAL reads a criticality proxy (the live branching ratio σ̂ = descendants/
  ancestors measured on the substrate) and homeostatically adjusts the inhibitory gain to drive
  σ̂ → 1 under the CURRENT input statistic — holding the edge-of-chaos as the stats move.

ARMS (frozen-first):
  GABA-CRITICAL    = E/I (inhibitory gain) adapts each segment to hold the live branching-ratio
                     proxy σ̂ ≈ 1 under the current input drive level. The signal a fixed E/I
                     cannot use: the live per-segment branching ratio.
  BEST-FIXED-EI    = the strongest single grid-tuned FIXED inhibitory gain over the WHOLE drifting
                     stream (the honest strong baseline / fusion-law discriminator). Disjoint tune
                     seed.
  SUBCRITICAL-FIXED= a fixed E/I that is critical only at the LOW-drive end (σ<1 elsewhere).
  SUPERCRITICAL-FIXED= a fixed E/I that is critical only at the HIGH-drive end (σ>1 elsewhere).
  ABL (const E/I)  = adaptive frozen to a CONSTANT E/I == best-fixed → reverts (proves the LEVER
                     is the criticality-tracking, not the inhibition per se).
  SHUFFLE          = the per-segment input-statistic cue PERMUTED vs the TRUE drift order → the
                     gain tracks the WRONG drive level → drifts off-critical → collapse (proves it
                     tracks the TRUE input statistic, not a mean gain).

FROZEN bars (🟢 iff A∧B∧C∧D∧E):
  A PRESENCE+SHIFT  : GABA-critical − best-fixed-EI ≥ ½·(GABA-critical − worst arm) across the drift
                     (the earned-majority / regime-shift bar) AND best-fixed cannot win at BOTH ends
                     of the stat-drift (low-drive AND high-drive) — the "critical point shifted"
                     evidence: a single fixed E/I is off-critical at one end.
  B DISTINCT        : sub-critical-fixed AND super-critical-fixed each FAIL off their matched regime
                     (sub fails the high-drive end, super fails the low-drive end) — criticality is
                     regime-specific, not a global constant.
  C ABL→fixed       : const-E/I ablation reverts toward best-fixed (gaba − abl ≥ MARGIN AND
                     |abl − best-fixed| < MARGIN).
  D SHUFFLE         : permuted input-stat cue collapses (gaba − shuffle ≥ MARGIN) — proves it tracks
                     the TRUE input statistic.
  E NO-FAB          : best-fixed-EI itself is a real working baseline ( > worst fixed ) — the
                     criticality capacity effect is genuinely real (a working E/I beats a broken one).
  🟢 iff A∧B∧C∧D∧E  → adaptive criticality-tracking carries the majority = GABA's escape capability
                       (the critical E/I SHIFTED with input stats and only adaptive held it);
  🟠 if best-fixed-EI captures ≥half (¬A but adaptive helps over worst & E holds) → criticality
                       benefit is monotone/static like the other 5 families → GABA confirmed
                       structural across 6 families;
  🧱 if GABA-critical ties no-inhibition / worst (criticality INERT).

p7: exact ground truth (cued pattern known); NO LLM judge, NO perplexity, NO loss term — every read
is a no-grad read of substrate state. $0 CPU, 3 seeds, frozen falsifier in H_1556_FREEZE.txt.

R1 numpy DIRECTIONAL (a_engine_native_learning hard-gate-1: grep numpy ⇒ auto-DIRECTIONAL) —
engine §GabaCritical R2 deferred ING. REUSES the H_1532/H_1552 key_vec / FNV-1a / SuperStore-style
machinery; the NEW piece is the BRANCHING-PROCESS criticality substrate (σ-dependent recurrent
recall) + the input-statistic-DRIFT stream + the σ≈1-tracking adaptive inhibitory gain.

Citations:
  Beggs & Plenz 2003 J Neurosci 23:11167 (neuronal avalanches; cortical networks operate at a
    critical branching ratio σ≈1).
  Shew & Plenz 2013 The Neuroscientist 19:88 (the functional benefits of criticality: max dynamic
    range, max information capacity, max distinct patterns at the critical point).
  Turrigiano 2011 Annu Rev Neurosci (homeostatic plasticity tracking a set-point) — but here the
    set-point (critical E/I) SHIFTS with input statistics, unlike a fixed firing-rate target.
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / H_1552 / CORE engine_cli) ──
DIM = 64                   # unit dim (key/state)  — VERBATIM family value
MARGIN = 0.05              # frozen ablation/shuffle bar (same family value)

# criticality substrate constants (frozen)
N_PATTERNS = 24            # distinct stored patterns to retain
RECALL_STEPS = 4           # recurrent branching steps before read-out
E_GAIN = 1.0               # recurrent excitatory gain (fixed; GABA modulates the inhibitory side)
SIGMA_TARGET = 1.0         # criticality target (edge-of-chaos branching ratio σ≈1)
ADAPT_RATE = 0.5           # homeostatic gain-correction rate toward σ_target (frozen)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532 / H_1552) ───────────────────
def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


def key_vec(s: str) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (VERBATIM from H_1532/H_1552)."""
    bs = s.encode()
    v = np.zeros(DIM)
    for i in range(len(bs) - 2):
        tri = bs[i:i + 3]
        idx = fnv1a(tri) % DIM
        v[idx] += 1.0
    n = np.linalg.norm(v)
    if n < 1e-9:
        v = np.zeros(DIM); v[fnv1a(bs) % DIM] = 1.0; n = 1.0
    return v / n


# ── CRITICALITY substrate: a recurrent associative store whose recall is a branching process ──
class CriticalStore:
    """A recurrent associative substrate over DIM units. Patterns are stored as binary unit-sets
    (Hopfield-style support); a cued pattern is recalled by RECURRENT propagation: each active unit
    re-activates its co-stored neighbours, modulated by E (excitation) and GABA inhibition. The
    EXPECTED active-units-per-active-unit per step is the BRANCHING RATIO σ. Retention peaks at
    σ≈1 (Beggs-Plenz): σ<1 the pattern dies, σ>1 distinct patterns merge.

    σ is set by  σ ≈ drive_level * E_GAIN * conn_density / inhib_gain  —
    so the SAME inhib_gain yields a DIFFERENT σ as the input drive_level drifts. That is why a
    fixed E/I cannot hold criticality across a drifting stream."""
    def __init__(self, dim, n_patterns, seed):
        rng = np.random.default_rng(seed + 777)
        self.dim = dim
        self.n_patterns = n_patterns
        # each pattern = a sparse support of ~PAT_K units (binary), low overlap
        PAT_K = 6
        self.patterns = []
        for _ in range(n_patterns):
            sup = rng.choice(dim, size=PAT_K, replace=False)
            p = np.zeros(dim); p[sup] = 1.0
            self.patterns.append(p)
        self.patterns = np.array(self.patterns)            # (n_patterns, dim)
        # recurrent connectivity = Hebbian sum of pattern outer products (co-active → connected)
        self.W = np.zeros((dim, dim))
        for p in self.patterns:
            self.W += np.outer(p, p)
        np.fill_diagonal(self.W, 0.0)
        # normalize so the bare (E=1, inhib=baseline, drive=1) branching ratio is ~1: each unit
        # connects to ~(PAT_K-1)*occurrences neighbours; we scale columns to unit out-degree mass.
        col = self.W.sum(axis=0, keepdims=True)
        col[col < 1e-9] = 1.0
        self.Wn = self.W / col                              # column-stochastic-ish propagation

    def measure_branching(self, drive_level, inhib_gain, n_probe=8, rng=None):
        """Estimate the live branching ratio σ̂ = descendants/ancestors averaged over n_probe cued
        patterns — the CRITICALITY PROXY the adaptive arm reads (Beggs-Plenz avalanche balance).
        One propagation step: active set → next active set; σ̂ = |next_active| / |active|."""
        if rng is None:
            rng = np.random.default_rng(0)
        idxs = rng.choice(self.n_patterns, size=min(n_probe, self.n_patterns), replace=False)
        ratios = []
        for i in idxs:
            active = self.patterns[i].copy()               # ancestors
            drive = drive_level * E_GAIN * (self.Wn @ active) / max(inhib_gain, 1e-6)
            nxt = (drive > 0.5).astype(float)               # threshold crossing → descendants
            na, nn = active.sum(), nxt.sum()
            if na > 0:
                ratios.append(nn / na)
        return float(np.mean(ratios)) if ratios else 0.0

    def recall(self, cue_idx, drive_level, inhib_gain):
        """Recurrent recall of pattern cue_idx under (drive_level, inhib_gain). Propagate
        RECALL_STEPS branching steps, then read out the NEAREST stored pattern. Returns True iff the
        settled state is closest to the cued pattern (retention)."""
        state = self.patterns[cue_idx].copy()
        for _ in range(RECALL_STEPS):
            drive = drive_level * E_GAIN * (self.Wn @ state) / max(inhib_gain, 1e-6)
            state = (drive > 0.5).astype(float)
            # renormalize total activity defensively (avoid pure 0 / pure all-on degenerate read)
            if state.sum() < 1e-9:
                break
        # read-out: nearest stored pattern by overlap (cosine on binary supports)
        sn = np.linalg.norm(state)
        if sn < 1e-9:
            return False                                    # pattern died (subcritical) → miss
        overlaps = self.patterns @ state / (np.linalg.norm(self.patterns, axis=1) * sn + 1e-9)
        return int(np.argmax(overlaps)) == cue_idx


# ── INPUT-STATISTIC DRIFT stream: drive level drifts across segments ──────────
# The input drive_level (the input statistic) DRIFTS across N_SEG segments. The critical E/I that
# yields σ≈1 SHIFTS with drive_level — so no fixed inhib_gain holds criticality across the stream.
def make_drift_stream(n_seg, drive_lo, drive_hi):
    """Build the per-segment input drive-level schedule (the drifting input statistic). Alternates
    LOW-drive and HIGH-drive segments (the stats drift). Returns the per-segment drive levels."""
    drives = []
    for s in range(n_seg):
        drives.append(drive_hi if (s % 2 == 1) else drive_lo)
    return drives


def critical_inhib_for(store, drive_level, rng):
    """Solve (by homeostatic adaptation toward σ_target) the inhib_gain that makes σ̂≈1 at this
    drive_level — i.e. what an adaptive GABA homeostat converges to. Pure σ-tracking, no task
    label (p7): it only reads the branching-ratio proxy, never the recall outcome."""
    g = 1.0
    for _ in range(40):
        sig = store.measure_branching(drive_level, g, rng=rng)
        # σ ∝ 1/g (more inhibition → lower σ); correct multiplicatively toward σ_target
        if sig <= 1e-6:
            g *= 0.5                                        # σ collapsed → relax inhibition
            continue
        g *= (sig / SIGMA_TARGET) ** ADAPT_RATE
        g = float(np.clip(g, 0.05, 50.0))
    return g


def score_stream(store, drives, mode, inhib_fixed=None, adapt_gains=None,
                 ablate_const=False, shuffle_drive=False, rng=None):
    """Stream segments at their drifting drive levels; in each segment recall ALL patterns under the
    arm's inhib_gain policy; capability = mean retention (fraction of patterns correctly recalled)
    across the whole drifting stream.

    mode:
      'fixed'    : a single FIXED inhib_gain over the whole drift (best/sub/super baselines).
      'adaptive' : GABA-CRITICAL — inhib_gain = the σ≈1 gain for the CURRENT segment drive level
                   (adapt_gains[seg]); homeostatically tracks the shifting critical point.
    ablate_const=True : adaptive frozen to a CONSTANT gain (== best-fixed) → reverts.
    shuffle_drive=True: the per-segment drive cue PERMUTED vs the TRUE drift order → adaptive gain
                   matches the WRONG drive → off-critical → collapse.
    """
    drive_seq = list(drives)
    if shuffle_drive and rng is not None:
        # permute which adaptive gain is applied vs the true segment drive (cue scrambled)
        perm = list(range(len(adapt_gains)))
        rng.shuffle(perm)
        adapt_gains = [adapt_gains[perm[s]] for s in range(len(adapt_gains))]

    seg_scores = []
    for s, drive in enumerate(drive_seq):
        if mode == 'fixed':
            g = inhib_fixed
        else:  # adaptive
            g = inhib_fixed if ablate_const else adapt_gains[s]
        correct = 0
        for ci in range(store.n_patterns):
            if store.recall(ci, drive, g):
                correct += 1
        seg_scores.append(correct / store.n_patterns)
    return seg_scores                                       # per-segment retention


def end_means(seg_scores, drives, drive_lo, drive_hi):
    """Split per-segment retention into the LOW-drive end and HIGH-drive end means (for the
    can't-win-both-ends regime-shift bar A and the distinctness bar B)."""
    lo = [s for s, d in zip(seg_scores, drives) if d == drive_lo]
    hi = [s for s, d in zip(seg_scores, drives) if d == drive_hi]
    return (float(np.mean(lo)) if lo else 0.0,
            float(np.mean(hi)) if hi else 0.0)


def grid_tune_fixed_ei(n_seg, drive_lo, drive_hi, tune_seed):
    """BEST/SUB/SUPER-critical FIXED inhib_gain over a grid on a DISJOINT tune-seed drift stream.
    best = strongest single fixed gain over the WHOLE drift; sub = gain critical at LOW end (low
    gain → σ>1 at high end / σ≈1 at low... actually inhib LOW → σ high → critical at LOW drive);
    super = gain critical at HIGH end. Returns best gain, its mean, and the sub/super gains+means,
    plus the worst-arm mean (for the earned-majority gap)."""
    rng = np.random.default_rng(tune_seed)
    store = CriticalStore(DIM, N_PATTERNS, tune_seed)
    drives = make_drift_stream(n_seg, drive_lo, drive_hi)
    grid = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
    results = {}
    end = {}
    for g in grid:
        ss = score_stream(store, drives, mode='fixed', inhib_fixed=g)
        results[g] = float(np.mean(ss))
        end[g] = end_means(ss, drives, drive_lo, drive_hi)
    best_g = max(results, key=results.get)
    worst_g = min(results, key=results.get)
    # sub-critical: the fixed gain whose LOW-end retention is highest but HIGH-end lowest (critical
    # only at low drive). super-critical: highest HIGH-end but lowest LOW-end (critical only high).
    sub_g = max(grid, key=lambda g: end[g][0] - end[g][1])    # best at low, worst at high
    super_g = max(grid, key=lambda g: end[g][1] - end[g][0])  # best at high, worst at low
    return (best_g, results[best_g], worst_g, results[worst_g],
            sub_g, results[sub_g], end[sub_g],
            super_g, results[super_g], end[super_g],
            results, end)


def main():
    N_SEG = 8                   # 4 LOW-drive (even) + 4 HIGH-drive (odd) alternating segments
    DRIVE_LO = 0.7              # LOW input drive (a fixed-inhib tuned here goes SUPERcritical at hi)
    DRIVE_HI = 1.6              # HIGH input drive (a fixed-inhib tuned here goes SUBcritical at lo)
    TUNE_SEED = 7               # disjoint seed for the best/sub/super-fixed grid
    SCORE_SEEDS = [11, 22, 33]

    drives = make_drift_stream(N_SEG, DRIVE_LO, DRIVE_HI)

    # grid-tune best / sub / super FIXED E/I on a DISJOINT drift stream (anti-confound).
    (best_g, best_mean, worst_g, worst_mean,
     sub_g, sub_mean, sub_end,
     super_g, super_mean, super_end,
     g_grid, g_end) = grid_tune_fixed_ei(N_SEG, DRIVE_LO, DRIVE_HI, TUNE_SEED)

    rows = []
    crit_end_lo, crit_end_hi = [], []
    best_end_lo, best_end_hi = [], []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        store = CriticalStore(DIM, N_PATTERNS, seed)
        # adaptive: per-segment σ≈1 inhib gain at that segment's drive level (criticality tracking)
        adapt_gains = [critical_inhib_for(store, d, np.random.default_rng(seed + 100 + s))
                       for s, d in enumerate(drives)]

        crit_ss = score_stream(store, drives, mode='adaptive', adapt_gains=adapt_gains)
        best_ss = score_stream(store, drives, mode='fixed', inhib_fixed=best_g)
        worst_ss = score_stream(store, drives, mode='fixed', inhib_fixed=worst_g)
        sub_ss = score_stream(store, drives, mode='fixed', inhib_fixed=sub_g)
        super_ss = score_stream(store, drives, mode='fixed', inhib_fixed=super_g)
        abl_ss = score_stream(store, drives, mode='adaptive', adapt_gains=adapt_gains,
                              inhib_fixed=best_g, ablate_const=True)
        shf_ss = score_stream(store, drives, mode='adaptive', adapt_gains=adapt_gains,
                              shuffle_drive=True, rng=np.random.default_rng(seed + 1000))

        crit_m, best_m, worst_m = np.mean(crit_ss), np.mean(best_ss), np.mean(worst_ss)
        sub_m, super_m, abl_m, shf_m = (np.mean(sub_ss), np.mean(super_ss),
                                        np.mean(abl_ss), np.mean(shf_ss))
        cl, ch = end_means(crit_ss, drives, DRIVE_LO, DRIVE_HI)
        bl, bh = end_means(best_ss, drives, DRIVE_LO, DRIVE_HI)
        sbl, sbh = end_means(sub_ss, drives, DRIVE_LO, DRIVE_HI)
        spl, sph = end_means(super_ss, drives, DRIVE_LO, DRIVE_HI)
        crit_end_lo.append(cl); crit_end_hi.append(ch)
        best_end_lo.append(bl); best_end_hi.append(bh)

        rows.append({'seed': seed,
                     'gaba_critical': round(float(crit_m), 4),
                     'best_fixed_ei': round(float(best_m), 4),
                     'worst_fixed_ei': round(float(worst_m), 4),
                     'subcritical_fixed': round(float(sub_m), 4),
                     'supercritical_fixed': round(float(super_m), 4),
                     'abl_const': round(float(abl_m), 4),
                     'shuffle': round(float(shf_m), 4),
                     'crit_low_end': round(cl, 4), 'crit_high_end': round(ch, 4),
                     'best_fixed_low_end': round(bl, 4), 'best_fixed_high_end': round(bh, 4),
                     'sub_low_end': round(sbl, 4), 'sub_high_end': round(sbh, 4),
                     'super_low_end': round(spl, 4), 'super_high_end': round(sph, 4),
                     'crit_minus_best_fixed': round(float(crit_m - best_m), 4),
                     'adapt_gains': [round(g, 3) for g in adapt_gains]})

    def m(key):
        return float(np.mean([r[key] for r in rows]))
    cr_m = m('gaba_critical'); bf_m = m('best_fixed_ei'); wf_m = m('worst_fixed_ei')
    sub_mm = m('subcritical_fixed'); sup_mm = m('supercritical_fixed')
    abl_mm = m('abl_const'); shf_mm = m('shuffle')
    cr_lo = float(np.mean(crit_end_lo)); cr_hi = float(np.mean(crit_end_hi))
    bf_lo = float(np.mean(best_end_lo)); bf_hi = float(np.mean(best_end_hi))
    sub_lo = m('sub_low_end'); sub_hi = m('sub_high_end')
    sup_lo = m('super_low_end'); sup_hi = m('super_high_end')

    # ── FROZEN falsifier (pre-registered in H_1556_FREEZE.txt) ────────────────
    #   A PRESENCE+SHIFT  : (crit − best_fixed) ≥ 0.5·(crit − worst_arm), worst-gap>0  AND
    #                       best-fixed cannot win BOTH ends (min(best_lo,best_hi) < crit-MARGIN at
    #                       its weak end) — the "critical point shifted" evidence
    #   B DISTINCT        : sub-critical fails the HIGH end (sub_hi < crit_hi − MARGIN) AND
    #                       super-critical fails the LOW end (sup_lo < crit_lo − MARGIN)
    #   C ABL→fixed       : crit − abl ≥ MARGIN  AND  |abl − best_fixed| < MARGIN
    #   D SHUFFLE         : crit − shuffle ≥ MARGIN
    #   E NO-FAB          : best_fixed > worst_fixed (a working E/I beats a broken one — capacity real)
    worst_arm = min(wf_m, sub_mm, sup_mm)
    full_gap = cr_m - worst_arm
    earned_majority = ((cr_m - bf_m) >= 0.5 * full_gap) and (full_gap > 0)
    best_fixed_weak_end = min(bf_lo, bf_hi)
    cant_win_both = best_fixed_weak_end < (cr_m - MARGIN)
    presence = earned_majority and cant_win_both

    distinct = (sub_hi < cr_hi - MARGIN) and (sup_lo < cr_lo - MARGIN)
    abl_reverts = ((cr_m - abl_mm) >= MARGIN) and (abs(abl_mm - bf_m) < MARGIN)
    shuffle_collapses = (cr_m - shf_mm) >= MARGIN
    no_fab = bf_m > wf_m

    if presence and distinct and abl_reverts and shuffle_collapses and no_fab:
        verdict = 'GREEN'       # adaptive criticality-tracking is the lever — the critical E/I SHIFTED
    elif no_fab and (cr_m - worst_arm) > MARGIN and not presence:
        verdict = 'AMBER'       # criticality helps over broken but best-fixed captures ≥half → KNOB
    else:
        verdict = 'WALL_HOLDS'  # criticality INERT / best-fixed captures it → GABA static across 6

    frac_adaptive = (100 * (cr_m - bf_m) / full_gap) if full_gap > 0 else float('nan')
    if verdict == 'GREEN':
        law_side = ('ADAPTIVE-FACULTY (🟢, like orexin/5-HT shifting-optimum) — the CRITICAL E/I '
                    'SHIFTS with input statistics, so adaptive σ≈1-tracking beats the best single '
                    'fixed E/I by the MAJORITY and holds criticality at BOTH drift ends where any '
                    'fixed E/I goes off-critical; GABA-as-criticality is a genuine adaptive faculty '
                    '— the ESCAPE the 5-family census missed (R4 skipped the SHIFTING setpoint)')
    elif verdict == 'AMBER':
        law_side = ('RE-TUNES-KNOB (🟠, like 5-HT/disinhibition/gamma) — criticality-tracking helps '
                    'over a broken E/I but a single grid-tuned best-fixed-E/I captures ≥half; the '
                    'critical point did NOT shift enough for adaptive to earn its keep. GABA-as-'
                    'adaptive now exhausted across 6 distinct families = honest structural-NT '
                    'ceiling; 5/6 all-green (ACh/DA/NE/orexin/5-HT) is the honest campaign result')
    else:
        law_side = ('STATIC-ARCHITECTURE 🧱 / INERT — criticality-tracking ties no-inhibition or a '
                    'single fixed E/I captures everything; GABA confirmed STRUCTURAL across 6 '
                    'distinct families (sparse ×3, disinhibition, gamma, criticality), NOT an '
                    'adaptive faculty — the fusion law is satisfied by NO GABA family. 5/6 NTs '
                    'all-green is the honest campaign result')

    summary = {
        'hypothesis': 'H_1556',
        'name': 'GABA × CLS — SELF-ORGANIZED CRITICALITY (adaptive E/I tracking a SHIFTING critical point)',
        'capability': 'pattern-retention / effective capacity across a stream whose INPUT STATISTICS '
                      '(drive level) DRIFT, via GABA homeostatically tracking the branching-ratio '
                      'proxy σ≈1 (the edge-of-chaos critical point) per current input statistic — '
                      'the regime where the critical E/I SHIFTS so no single fixed E/I holds it',
        'escape_framing': 'the ABSTRACT→ESCAPE lens after GABA 5-family census (sparse 🧱×3 / '
                          'disinhibition 🟠 / gamma 🟠 / divnorm 🧱 / E-I-setpoint 🧱-skipped). The '
                          'census SKIPPED E/I-setpoint (R4) as "single FIXED target = monotone". '
                          'CRITICALITY is the distinct escape: the critical E/I is NOT a fixed '
                          'target — it SHIFTS with input statistics (Beggs-Plenz σ≈1 depends on '
                          'drive), so NO fixed E/I holds criticality as the stream drifts = the '
                          'fusion-law SHIFTING-optimum condition. 6th GABA family.',
        'distinct_from_R4': 'R4 E/I-setpoint = a SINGLE fixed E/I target (monotone, fixed captures '
                            'it). H_1556 = the critical E/I MOVES with the input statistic, so the '
                            'optimum genuinely SHIFTS — the one regime R4 could not reach. Also a '
                            'capability the 5 phasic GREEN NTs do NOT provide (they schedule LR/gate/'
                            'abstain WITHIN a fixed regime; none SET the E/I operating regime).',
        'cites': ['Beggs & Plenz 2003 J Neurosci 23:11167 (neuronal avalanches; cortex at critical '
                  'branching ratio σ≈1)',
                  'Shew & Plenz 2013 The Neuroscientist 19:88 (functional benefits of criticality: '
                  'max dynamic range / max distinct patterns at the critical point)',
                  'Turrigiano 2011 Annu Rev Neurosci (homeostatic plasticity to a set-point; here the '
                  'set-point SHIFTS with input statistics)'],
        'criticality_proxy': 'branching ratio σ̂ = descendants/ancestors per recurrent step '
                             '(Beggs-Plenz avalanche balance); adaptive arm reads σ̂ ONLY (p7, no '
                             'task label) and drives σ̂→1 by adjusting the GABA inhibitory gain',
        'N_SEG': N_SEG, 'DRIVE_LO': DRIVE_LO, 'DRIVE_HI': DRIVE_HI, 'DIM': DIM,
        'N_PATTERNS': N_PATTERNS, 'RECALL_STEPS': RECALL_STEPS, 'SIGMA_TARGET': SIGMA_TARGET,
        'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
        'best_fixed_gain': best_g, 'worst_fixed_gain': worst_g,
        'subcritical_gain': sub_g, 'supercritical_gain': super_g,
        'fixed_grid_tune': {str(g): round(v, 4) for g, v in g_grid.items()},
        'fixed_grid_end_means': {str(g): [round(e[0], 4), round(e[1], 4)] for g, e in g_end.items()},
        'per_seed': rows,
        'gaba_critical_mean': round(cr_m, 4),
        'best_fixed_ei_mean': round(bf_m, 4),
        'worst_fixed_ei_mean': round(wf_m, 4),
        'subcritical_fixed_mean': round(sub_mm, 4),
        'supercritical_fixed_mean': round(sup_mm, 4),
        'abl_const_mean': round(abl_mm, 4),
        'shuffle_mean': round(shf_mm, 4),
        'crit_low_end_mean': round(cr_lo, 4), 'crit_high_end_mean': round(cr_hi, 4),
        'best_fixed_low_end_mean': round(bf_lo, 4), 'best_fixed_high_end_mean': round(bf_hi, 4),
        'sub_low_end_mean': round(sub_lo, 4), 'sub_high_end_mean': round(sub_hi, 4),
        'super_low_end_mean': round(sup_lo, 4), 'super_high_end_mean': round(sup_hi, 4),
        'crit_minus_best_fixed_mean': round(cr_m - bf_m, 4),
        'crit_minus_worst_arm_gap': round(full_gap, 4),
        'best_fixed_weak_end': round(best_fixed_weak_end, 4),
        'crit_carries_pct_of_gap': round(frac_adaptive, 1),
        'A_presence_shift': bool(presence),
        'A_earned_majority': bool(earned_majority),
        'A_best_fixed_cant_win_both_ends': bool(cant_win_both),
        'B_distinct_sub_super_fail_off_regime': bool(distinct),
        'C_abl_reverts': bool(abl_reverts),
        'D_shuffle_collapses': bool(shuffle_collapses),
        'E_no_fab': bool(no_fab),
        'verdict': verdict,
        'law_side': law_side,
        'directional': True,
        'note': 'numpy mirror ⇒ DIRECTIONAL (a_engine_native_learning hard-gate-1); engine '
                '§GabaCritical R2 deferred ING h1556-r2-engine-native; reuses H_1532/H_1552 '
                'key_vec/FNV-1a byte-exact; NEW = branching-process criticality substrate '
                '(σ-dependent recurrent recall) + input-statistic DRIFT stream + σ≈1-tracking '
                'adaptive inhibitory gain; bars frozen-first (NO tune-to-green); A presence measures '
                'adaptive vs BEST-FIXED-E/I AND the critical-point-shifted (cant-win-both-ends) test',
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
