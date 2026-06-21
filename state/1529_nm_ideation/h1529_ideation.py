#!/usr/bin/env python3
"""
H_1529 — NEUROMODULATION on a GEOMETRY-FREE capability: GROUNDED RECOMBINATION
IDEATION (novelty net of fabrication), NOT discrete recall.

Attempts to break the H_1284 NEUROMODULATION wall by moving OFF the
key-geometry-bound recall capability onto IDEATION, where the optimal exploration
temperature genuinely SHIFTS with regime (H_1228 NE/exploration axis, 🟠 PARTIAL).

Reuses the H_1284 store/regime machinery VERBATIM (MemStore, gen_stream, regimes,
seeds, MARGIN) — imports from state/universe-probes/h1284_neuromodulation_gain.py —
and re-purposes the capability from RECALL to RECOMBINATION ideation under an
exploration-temperature knob. Score = novelty_rate − fabrication_rate (anti-Goodhart
p7: blind high-T is penalized because it fabricates).

ARMS: A=best-fixed-T (grid-tuned on disjoint seed) · E=adaptive exploration (T gated
by substrate surprise + coverage) · ABL=adaptive→mean (E's own mean T, coupling
destroyed). Frozen falsifier: H_1529_FREEZE.txt.

p7: exact combinatorial ground truth, NO LLM judge, NO perplexity, controller is a
no-grad readout NEVER folded into a loss. $0 CPU numpy. ≥3 seeds. DIRECTIONAL
(a_engine_native_learning — numpy mirror of CORE VAdaptField; engine R2 deferred ING).
CORE/*.hexa + H_1284 + H_1228 UNTOUCHED.
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))           # repo root (worktree)
PROBES = os.path.join(ROOT, "state", "universe-probes")
sys.path.insert(0, PROBES)

# ── reuse H_1284 machinery VERBATIM (frozen byte-for-byte) ────────────────────
import h1284_neuromodulation_gain as H1284
from h1284_neuromodulation_gain import (
    MemStore, key_vec, make_facts, gen_stream, DIM,
    LR0_ENGINE, TH0_ENGINE,
)

MARGIN = 0.05                      # inherited from H_1284
SCORE_SEEDS = [11, 22, 33]
TUNE_SEED = 7
REGIMES = ('R1_STABLE', 'R2_DRIFT', 'R3_NOISE')
N_FACTS = 30
ABSTAIN0 = 0.45
N_EVENTS = 300                     # to evolve the store (same as H_1284)
N_EMIT = 200                       # ideation candidates per stream
# T_GRID widened (frozen-first a_break_the_wall type-a): the initial (≤1.4) grid
# stopped BELOW the fabrication cliff, so grid-tune picked the ceiling and ARM A was
# NOT the strongest honest fixed point. The true interior optimum (precision vs
# fabrication) sits at T≈4 with M≈0.54 then DECLINES as ghost-reach rises. Widened so
# ARM A is genuinely the best-fixed operating point. Binding metric M and c1–c4
# thresholds UNCHANGED — not tune-to-green.
T_GRID = (0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0)


# ── build the evolved store for a (seed,regime) by replaying the H_1284 stream ─
def build_store(regime, seed):
    """Replay the H_1284 write/recall event stream to evolve a MemStore, exactly
    as H_1284 run_arm does (FIXED engine knobs, adaptive=False path) — the store is
    identical across arms; only the downstream IDEATION policy differs."""
    rng = np.random.default_rng(seed)
    facts = make_facts(N_FACTS, rng)
    events = gen_stream(regime, facts, rng, n_events=N_EVENTS)
    store = MemStore(max_cells=max(4, int(len(facts) * 0.6)),
                     abstain_margin=ABSTAIN0)
    # use a FRESH rng for the noise draws (mirrors H_1284 run_arm's separate rng)
    noise_rng = np.random.default_rng(seed)
    for kind, key, val, sig in events:
        x = key_vec(key, noise_rng) + noise_rng.normal(0, sig, DIM)
        x = x / (np.linalg.norm(x) + 1e-9)
        if kind == 'write':
            store.write(x, val, LR0_ENGINE, TH0_ENGINE)
    return store, facts, noise_rng


# ── grounded affinity neighbor ranking off the live store (substrate read) ────
def cell_xs(store):
    """unit prototype vectors of the stored cells (the live substrate keys)."""
    return [p / (np.linalg.norm(p) + 1e-9) for p in store.protos]


def make_ghosts(n_ghost, seed):
    """ungrounded 'ghost' tokens — untaught keys NOT in the store (the H_1284
    recall_oos fabrication tokens). A recombination that reaches a ghost is a
    FABRICATION (the made-up token the abstain band should reject). These sit
    INTERLEAVED in the affinity ranking so that high exploration-T reaches them
    while low-T stays among grounded cells — the novelty-vs-fabrication tradeoff."""
    grng = np.random.default_rng(seed + 104729)
    ghosts = []
    for g in range(n_ghost):
        v = key_vec(f"ghost{grng.integers(0,99999):05d}", grng)
        v = v / (np.linalg.norm(v) + 1e-9)
        ghosts.append((v, f"GHOST{g:03d}"))
    return ghosts


def ranked_neighbors(store, xs, ghost_xs, i):
    """affinity-ranked OTHER candidates for cell i (nearest-first by L2): the real
    stored cells (grounded) PLUS the ghost tokens (ungrounded). Each entry carries
    a `grounded` flag so the ideation scorer can net novelty against fabrication."""
    pi = xs[i]
    d = [(np.linalg.norm(xs[j] - pi), j, True) for j in range(len(xs)) if j != i]
    for gj, (gv, _) in enumerate(ghost_xs):
        d.append((float(np.linalg.norm(gv - pi)), ('G', gj), False))
    d.sort(key=lambda t: t[0])
    return d  # list of (dist, ref, grounded) nearest-first


def temp_pick(neighbors, T, rng):
    """exploration-temperature pick: T≈0 -> nearest (grounded), high T -> reach
    further down the ranked list. Returns (dist, j). Geometry-free: T scales the
    softmax over -rank, so it is the IDEATION knob, not a key-geometry readout."""
    if not neighbors:
        return None
    ranks = np.arange(len(neighbors), dtype=float)        # 0=nearest
    # logits favour near (low rank) at low T; flatten/invert toward far at high T
    logits = -ranks / max(1e-6, T)
    logits -= logits.max()
    p = np.exp(logits); p /= p.sum()
    idx = int(rng.choice(len(neighbors), p=p))
    return neighbors[idx]


# ── the IDEATION capability: emit grounded recombinations under a T-policy ────
N_GHOST = 18           # ungrounded token pool size (~= #cells; balanced reach)


def run_ideation(store, facts, seed, policy):
    """policy(state) -> T per emit. Returns (novelty_rate, fabrication_rate, M,
    mean_T). A candidate = recombine cell i's subject with a T-sampled neighbor's
    city. The neighbor pool = grounded stored cells + ungrounded GHOST tokens.
    NOVEL iff the grounded combo is not already in store / not re-emitted;
    GROUNDED iff the reached neighbor is a real stored cell; FABRICATION iff it is
    a ghost (made-up token the abstain band should reject). Score nets them:
    M = novelty_rate − fabrication_rate (p7 anti-Goodhart: blind high-T reaches
    more ghosts → more fabrication → penalized)."""
    rng = np.random.default_rng(seed + 7919)
    xs = cell_xs(store)
    if len(xs) < 2:
        return 0.0, 0.0, 0.0, 0.0
    ghost_xs = make_ghosts(N_GHOST, seed)
    existing = set()                       # combos already in the store
    for k in range(len(store.protos)):
        existing.add((k, store.values[k]))
    emitted = set()
    n_novel_grounded = 0
    n_fab = 0
    recombined_recent = []                 # rolling coverage window
    COV_WIN = 40
    u = TH0_ENGINE                         # running expected surprise (EMA)
    EMA = 0.1
    T_log = []
    for e in range(N_EMIT):
        i = int(rng.integers(0, len(xs)))
        neighbors = ranked_neighbors(store, xs, ghost_xs, i)
        if not neighbors:
            continue
        # substrate surprise for cell i = nearest-GROUNDED distance (how isolated
        # cell i is among real cells — a no-grad substrate read, NE axis)
        gdist = [d for d, ref, gr in neighbors if gr]
        surprise = gdist[0] if gdist else neighbors[0][0]
        # coverage = fraction of distinct grounded cells touched recently (the
        # safe-novel well drying out drives ACh/novelty exploration up)
        cov = len(set(recombined_recent[-COV_WIN:])) / max(1, len(xs))
        T = policy(surprise=surprise, u=u, coverage=cov)
        T_log.append(T)
        pick = temp_pick(neighbors, T, rng)
        if pick is None:
            continue
        dist, ref, grounded = pick
        if not grounded:
            n_fab += 1                      # reached a ghost = fabrication
            continue
        j = ref
        combo = (i, store.values[j])       # subjA recombined with cityB
        novel = combo not in existing and combo not in emitted
        emitted.add(combo)
        recombined_recent.append(j)
        if novel:
            n_novel_grounded += 1
        # update running expected-surprise (EMA), substrate read (no loss, p7)
        u = (1 - EMA) * u + EMA * surprise
    novelty_rate = n_novel_grounded / N_EMIT
    fab_rate = n_fab / N_EMIT
    M = novelty_rate - fab_rate
    return novelty_rate, fab_rate, M, float(np.mean(T_log)) if T_log else 0.0


# ── policies ──────────────────────────────────────────────────────────────────
def fixed_policy(T0):
    return lambda surprise, u, coverage: T0


# adaptive gains (frozen in FREEZE, NOT tuned to green)
KS = 0.8        # NE: raise T on UNEXPECTED surprise (s>û) = explore the unfamiliar
KC = 0.9        # ACh/novelty: raise T as recent coverage rises (safe-novel well drying)
# adaptive clamp band scaled to the capability (×0.25..×2 of the operating T0) so the
# controller can swing through the SAME range the fixed arm uses — a FAIR test (an
# adaptive arm bottled below the optimum would lose by construction, not by merit).
# frozen-first: matching the controller's operating scale to the capability, not a bar.
T_LO_FRAC, T_HI_FRAC = 0.25, 2.0


def adaptive_policy(T0):
    lo, hi = T_LO_FRAC * T0, T_HI_FRAC * T0
    def pol(surprise, u, coverage):
        T = T0 * (1 + KS * (surprise - u)) * (1 + KC * coverage)
        return float(np.clip(T, lo, hi))
    return pol


def mean_policy(mean_T):
    """ABL: same average exploration as E, coupling to state destroyed."""
    return lambda surprise, u, coverage: mean_T


# ── ARM A: grid-tune best fixed T on a DISJOINT seed (mean over regimes) ───────
def grid_tune():
    best = None
    for T0 in T_GRID:
        caps = []
        for regime in REGIMES:
            store, facts, _ = build_store(regime, TUNE_SEED)
            _, _, M, _ = run_ideation(store, facts, TUNE_SEED, fixed_policy(T0))
            caps.append(M)
        m = float(np.mean(caps))
        if best is None or m > best[0]:
            best = (m, T0)
    return best[1]


def main():
    T_star = grid_tune()

    results = {r: {'A': [], 'E': [], 'ABL': [],
                   'A_fab': [], 'E_fab': [], 'meanT': []} for r in REGIMES}

    for seed in SCORE_SEEDS:
        for regime in REGIMES:
            # identical evolved store for A/E/ABL this (seed,regime)
            store_A, facts, _ = build_store(regime, seed)
            store_E, _, _ = build_store(regime, seed)
            store_ABL, _, _ = build_store(regime, seed)

            # A FIXED best-T
            a_nov, a_fab, a_M, _ = run_ideation(
                store_A, facts, seed, fixed_policy(T_star))
            # E ADAPTIVE
            e_nov, e_fab, e_M, e_meanT = run_ideation(
                store_E, facts, seed, adaptive_policy(T_star))
            # ABL ADAPTIVE->MEAN (use E's realized mean T as the fixed knob)
            abl_nov, abl_fab, abl_M, _ = run_ideation(
                store_ABL, facts, seed, mean_policy(e_meanT))

            results[regime]['A'].append(a_M)
            results[regime]['E'].append(e_M)
            results[regime]['ABL'].append(abl_M)
            results[regime]['A_fab'].append(a_fab)
            results[regime]['E_fab'].append(e_fab)
            results[regime]['meanT'].append(e_meanT)

    # ── aggregate + frozen falsifier ─────────────────────────────────────────
    summary = {'T_star': T_star, 'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
               'regimes': {}}
    wins = []          # regimes where E beats A + MARGIN
    coupled = []       # winning regimes where E - ABL >= MARGIN
    fab_ok = True      # c3: E fab <= A fab on each winning regime
    never_much_worse = True

    for regime in REGIMES:
        A = float(np.mean(results[regime]['A']))
        E = float(np.mean(results[regime]['E']))
        ABL = float(np.mean(results[regime]['ABL']))
        Af = float(np.mean(results[regime]['A_fab']))
        Ef = float(np.mean(results[regime]['E_fab']))
        mT = float(np.mean(results[regime]['meanT']))
        summary['regimes'][regime] = {
            'A_M': round(A, 4), 'E_M': round(E, 4), 'ABL_M': round(ABL, 4),
            'A_fab': round(Af, 4), 'E_fab': round(Ef, 4),
            'E_minus_A': round(E - A, 4), 'E_minus_ABL': round(E - ABL, 4),
            'E_mean_T': round(mT, 4),
        }
        beats = E >= A + MARGIN
        if beats:
            wins.append(regime)
            if E - ABL >= MARGIN:
                coupled.append(regime)
            if Ef > Af:
                fab_ok = False
        else:
            if E < A - 0.02:
                never_much_worse = False

    n_wins = len(wins)
    n_coupled = len(coupled)
    # c2 evaluated on the winning regimes (mean lift over wins >= MARGIN, AND each
    # winning regime individually coupling-separated >= MARGIN)
    c1 = n_wins >= 2
    c2 = (n_wins >= 1) and (n_coupled >= n_wins)   # every win is coupling-attributable
    c3 = fab_ok
    c4 = never_much_worse

    if c1 and c2 and c3 and c4:
        verdict = 'GREEN'        # WALL-BROKEN on ideation
    elif n_wins >= 1 and not c1:
        verdict = 'WALL'         # single regime only -> no-free-lunch holds broadly
    elif c1 and not (c2 and c3):
        verdict = 'PARTIAL'      # lift not coupling-attributable / fab-bought
    else:
        verdict = 'WALL'         # no regime beat best-fixed: wall holds

    summary['wins_over_A+MARGIN'] = wins
    summary['coupling_separated'] = coupled
    summary['c1_presence_2of3'] = c1
    summary['c2_coupling_every_win'] = c2
    summary['c3_fab_ok'] = c3
    summary['c4_never_much_worse'] = c4
    summary['n_wins'] = n_wins
    summary['n_coupled'] = n_coupled
    summary['verdict'] = verdict
    summary['DIRECTIONAL'] = True
    summary['note'] = ('numpy mirror of CORE VAdaptField via H_1284 MemStore; '
                       'engine-transfer UNVERIFIED (a_engine_native_learning); '
                       'engine R2 deferred ING follow-on')
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
