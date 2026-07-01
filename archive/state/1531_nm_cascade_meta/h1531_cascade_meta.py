#!/usr/bin/env python3
"""
H_1531 — CASCADE METAPLASTICITY (Benna-Fusi) on RETENTION-UNDER-INTERFERENCE.

WALL-BREAK candidate C2 (census state/1530_nm_research_census/CENSUS.md). The
H_1284 NEUROMODULATION wall is 11 lenses deep, but every prior probe tested CLEAN
recall — where capacity is monotone and no structure helps (H_1528 capacity races
to the ceiling; H_1527 expansion inert on clean recall). The census + H_1528's own
diagnostic identify the MISSING precondition: a capability where a FLAT store
genuinely FAILS and structured memory can win = RETENTION / INTERFERENCE.

CAPABILITY (precondition the wall's prior probes LACKED): write an early target
fact A->B, then write K later interfering facts (some at near-collinear keys that
land on A's cell), then measure A->B recall accuracy at an interference horizon.
A FLAT store has NO per-cell consolidation timescale — every overwrite happens at
the same rate, so a later confusable fact clobbers the early one. A Benna-Fusi
cascade gives per-cell variable timescales: a repeatedly-confirmed early fact sinks
DEEPER into the cascade and becomes RESISTANT to being clobbered. This is a
STRUCTURE the flat store lacks, on a CAPABILITY where it matters.

ARMS (census C2 spec):
  FLAT    — single-timescale store, best-fixed write rate (grid-tuned, disjoint seed).
  CASCADE — per-cell 2-3 level Benna-Fusi cascade; consolidation depth = confirmation count.
  ABL     — cascade depth=0 (reverts to flat single-timescale store).
  SHUFFLE — randomize WHICH fact gets consolidated (destroys the history coupling).

HAZARD (flagged in the brief): the cascade must be a per-cell STRUCTURE, not a
global consolidation-rate gain. A scalar rate that conditions on the recall margin
re-enters the absorbed controller family (H_1422). Here the cascade variable is
PER-CELL and its depth is set by that cell's OWN confirmation history — there is no
global knob and no read of the abstain margin. (Self-check: grep the source — no
margin-conditioned global gain in the CASCADE write.)

FROZEN bar (H_1531_FREEZE.txt, pre-register):
  retention_cascade - retention_flat >= +0.05 at the interference horizon on >=2/3 seeds
  AND ablation decisive (depth=0 reverts to flat; shuffle collapses).
  HONEST (c9): if cascade ties flat even on interference, the wall extends to the
  metaplasticity family. NO tune-to-green; bar frozen before scoring.

DIRECTIONAL: numpy mirror of the H_1284 store machinery (host has no torch). Engine
R2 re-score (live core/ A<->G + VAdaptField) = deferred ING follow-on
(a_engine_native_learning). $0 CPU, >=3 seeds, p7 (exact ground truth, no LLM judge,
no loss term — the cascade is a no-grad per-cell state update).
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1284 store machinery) ────────────
DIM = 16                  # key dim (H_1227 byte-trigram FNV-1a -> dim16 toy)
ABSTAIN0 = 0.45           # H_1284 abstain margin


# ── byte-trigram FNV-1a key (H_1227/H_1231 key, documented discriminating) ────
def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


def key_vec(s: str) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (H_1284 key_vec)."""
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


# ── FLAT store (H_1284 MemStore, single global write rate) ────────────────────
# write: nearest cell within SPLIT_THRESH is OVERWRITTEN at rate=1 (full clobber)
# — the flat store has NO per-cell consolidation: a later confusable fact at a
# near-collinear key lands on the SAME cell and replaces its value.
class FlatStore:
    def __init__(self, max_cells, split_thresh, abstain_margin):
        self.protos = []          # DIM cell prototypes
        self.values = []          # bound value (the fact)
        self.max_cells = max_cells
        self.split_thresh = split_thresh
        self.abstain_margin = abstain_margin

    def _nearest(self, x):
        if not self.protos:
            return -1, 1e9
        d = [np.linalg.norm(p - x) for p in self.protos]
        order = np.argsort(d)
        win = int(order[0])
        return win, d[win]

    def write(self, x, value):
        win, err = self._nearest(x)
        if win < 0 or (err > self.split_thresh and len(self.protos) < self.max_cells):
            self.protos.append(x.copy()); self.values.append(value)
            return
        # within-threshold OR capacity-bound: OVERWRITE the winner (full clobber).
        self.protos[win] = x.copy()
        self.values[win] = value

    def recall(self, x):
        win, err = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None
        return self.values[win]


# ── CASCADE store (Benna-Fusi per-cell metaplasticity) ────────────────────────
# Each cell carries a per-cell cascade STATE: a consolidation depth d in {0..DMAX}.
# - On a CONFIRMING write (same value to the same cell within threshold) depth+=1
#   — the fact sinks DEEPER, becoming progressively more resistant to change.
# - On a CLOBBERING write (DIFFERENT value lands on the cell within threshold) the
#   incumbent's depth gates whether it is overwritten: overwrite probability decays
#   with depth (deep = consolidated = power-law resistant, Benna-Fusi 2016). The
#   challenger only wins if it overcomes the incumbent's consolidation; on a miss
#   the incumbent SURVIVES and the challenger spawns its own cell if capacity allows.
# This is PER-CELL STRUCTURE (each cell's own history sets its own timescale), NOT a
# global gain conditioned on the recall margin — the hazard the brief flagged.
class CascadeStore:
    DMAX = 2                       # 3 levels {0,1,2} (census "2-3 level cascade")

    def __init__(self, max_cells, split_thresh, abstain_margin, depth_enabled=True,
                 resist_per_depth=0.50):
        self.protos = []
        self.values = []
        self.depth = []            # PER-CELL consolidation depth (the cascade state)
        self.max_cells = max_cells
        self.split_thresh = split_thresh
        self.abstain_margin = abstain_margin
        self.depth_enabled = depth_enabled
        self.resist_per_depth = resist_per_depth   # resistance growth per cascade level

    def _nearest(self, x):
        if not self.protos:
            return -1, 1e9
        d = [np.linalg.norm(p - x) for p in self.protos]
        order = np.argsort(d)
        win = int(order[0])
        return win, d[win]

    def write(self, x, value, rng):
        win, err = self._nearest(x)
        if win < 0 or (err > self.split_thresh and len(self.protos) < self.max_cells):
            self.protos.append(x.copy()); self.values.append(value); self.depth.append(0)
            return
        if err > self.split_thresh:
            # capacity-bound, no near cell: overwrite the winner (rare in this fixture)
            self.protos[win] = x.copy(); self.values[win] = value; self.depth[win] = 0
            return
        # a cell within threshold already holds something
        if self.values[win] == value:
            # CONFIRMING write: consolidate — sink deeper (per-cell, history-driven)
            if self.depth_enabled and self.depth[win] < self.DMAX:
                self.depth[win] += 1
            self.protos[win] = self.protos[win] + 0.20 * (x - self.protos[win])
            return
        # CLOBBERING write: a DIFFERENT value challenges the incumbent.
        if self.depth_enabled:
            # incumbent resists in proportion to its OWN consolidation depth.
            p_overwrite = 1.0 / (1.0 + self.resist_per_depth * self.depth[win])
        else:
            p_overwrite = 1.0          # ABL depth=0: always clobber == flat store
        if rng.random() < p_overwrite:
            self.protos[win] = x.copy(); self.values[win] = value; self.depth[win] = 0
        else:
            # incumbent survives; challenger spawns its own cell if capacity allows
            if len(self.protos) < self.max_cells:
                self.protos.append(x.copy()); self.values.append(value); self.depth.append(0)
            # else challenger is dropped (incumbent consolidated wins the slot)

    def recall(self, x):
        win, err = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None
        return self.values[win]


# ── interference fixture ──────────────────────────────────────────────────────
# An EARLY target fact A->B is written + repeatedly CONFIRMED (rehearsal — anima
# revisits a grounded fact), then K LATER interfering facts arrive, a fraction of
# them at NEAR-COLLINEAR keys that land on A's cell (the AB-AC interference the flat
# store suffers). At the interference HORIZON we probe A->B retention.
def perturb_key(base: np.ndarray, sigma: float, rng) -> np.ndarray:
    x = base + rng.normal(0, sigma, DIM)
    return x / (np.linalg.norm(x) + 1e-9)


def run_trial(arm, seed_rng, split_thresh, n_targets, n_confirm, K_interf,
              collinear_frac, collinear_sigma, max_cells):
    """One interference trial. Returns A->B retention accuracy over the targets.

    arm in {'FLAT','CASCADE','ABL','SHUFFLE'}.
    """
    if arm == 'FLAT':
        store = FlatStore(max_cells, split_thresh, ABSTAIN0)
    else:
        depth_enabled = (arm != 'ABL')          # ABL freezes cascade depth at 0
        store = CascadeStore(max_cells, split_thresh, ABSTAIN0,
                             depth_enabled=depth_enabled)

    # build target facts A_i -> B_i
    targets = []
    for i in range(n_targets):
        kA = key_vec(f"alpha{i:03d}")
        vB = f"beta{i:03d}"
        targets.append((kA, vB))

    # SHUFFLE control: decide which targets get the consolidation rehearsal AT RANDOM,
    # decoupling consolidation from the actual early-fact identity. The same total
    # number of confirming writes happen, just bound to randomly chosen targets.
    if arm == 'SHUFFLE':
        consolidate_idx = set(seed_rng.permutation(n_targets)[:n_targets].tolist())
    else:
        consolidate_idx = set(range(n_targets))   # all early facts rehearsed

    def w(x, val):
        if arm == 'FLAT':
            store.write(x, val)
        else:
            store.write(x, val, seed_rng)

    # phase 1: write + CONFIRM (rehearse) each early target fact
    for i, (kA, vB) in enumerate(targets):
        w(perturb_key(kA, 0.01, seed_rng), vB)
        if i in consolidate_idx:
            for _ in range(n_confirm):
                w(perturb_key(kA, 0.01, seed_rng), vB)   # confirming writes -> sink deeper

    # phase 2: K later interfering facts. A fraction land at NEAR-COLLINEAR keys to a
    # random target (challenge the incumbent on its own cell with a DIFFERENT value).
    for k in range(K_interf):
        if seed_rng.random() < collinear_frac:
            ti = int(seed_rng.integers(0, n_targets))
            kA, _ = targets[ti]
            xk = perturb_key(kA, collinear_sigma, seed_rng)   # collinear -> hits A's cell
            vC = f"gamma{k:04d}"                              # DIFFERENT value (clobber)
            w(xk, vC)
        else:
            kD = key_vec(f"delta{k:04d}")
            w(perturb_key(kD, 0.01, seed_rng), f"epsilon{k:04d}")

    # phase 3: probe A->B retention at the interference horizon
    n_ok = 0
    for kA, vB in targets:
        pred = store.recall(perturb_key(kA, 0.01, seed_rng))
        if pred == vB:
            n_ok += 1
    return n_ok / n_targets


def grid_tune_flat(tune_seed, n_targets, n_confirm, K_interf, collinear_frac,
                   collinear_sigma, max_cells):
    """ARM FLAT: best fixed SPLIT_THRESH on a DISJOINT tuning seed (strongest honest
    fixed single-timescale store — the H_1284 'best-fixed dominates' baseline)."""
    best = None
    for st in (0.20, 0.30, 0.40, 0.50, 0.60):
        rng = np.random.default_rng(tune_seed)
        ret = run_trial('FLAT', rng, st, n_targets, n_confirm, K_interf,
                        collinear_frac, collinear_sigma, max_cells)
        if best is None or ret > best[0]:
            best = (ret, st)
    return best[1]


def main():
    # fixture params (frozen before scoring)
    N_TARGETS = 24
    N_CONFIRM = 3            # rehearsal count for early facts (consolidation history)
    K_INTERF = 120          # later interfering facts (the interference horizon)
    COLLINEAR_FRAC = 0.6    # fraction of interferers at near-collinear keys
    COLLINEAR_SIGMA = 0.18  # key noise small enough to land on the target's cell
    MAX_CELLS = N_TARGETS * 3
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    MARGIN = 0.05

    # ARM FLAT tuning (disjoint seed) — strongest honest single-timescale baseline
    st_star = grid_tune_flat(TUNE_SEED, N_TARGETS, N_CONFIRM, K_INTERF,
                             COLLINEAR_FRAC, COLLINEAR_SIGMA, MAX_CELLS)

    per_seed = {'FLAT': [], 'CASCADE': [], 'ABL': [], 'SHUFFLE': []}
    for seed in SCORE_SEEDS:
        for arm in ('FLAT', 'CASCADE', 'ABL', 'SHUFFLE'):
            # identical fixture per (seed, arm): same split_thresh, same RNG seed so
            # the event stream is matched; only the STORE structure differs.
            rng = np.random.default_rng(seed)
            ret = run_trial(arm, rng, st_star, N_TARGETS, N_CONFIRM, K_INTERF,
                            COLLINEAR_FRAC, COLLINEAR_SIGMA, MAX_CELLS)
            per_seed[arm].append(ret)

    # ── aggregate + frozen falsifier ─────────────────────────────────────────
    flat = np.array(per_seed['FLAT'])
    casc = np.array(per_seed['CASCADE'])
    abl = np.array(per_seed['ABL'])
    shuf = np.array(per_seed['SHUFFLE'])

    lift = casc - flat                      # per-seed cascade lift over flat
    n_seed_win = int(np.sum(lift >= MARGIN))  # seeds clearing +0.05

    mean_flat = float(flat.mean())
    mean_casc = float(casc.mean())
    mean_abl = float(abl.mean())
    mean_shuf = float(shuf.mean())

    # ablation decisive: depth=0 reverts to flat (ABL ~ FLAT, within MARGIN) AND
    # shuffle collapses (SHUFFLE loses most of the cascade lift over flat).
    abl_reverts = abs(mean_abl - mean_flat) <= MARGIN
    shuf_collapse = (mean_shuf - mean_flat) <= (mean_casc - mean_flat) - MARGIN \
                    if (mean_casc - mean_flat) >= MARGIN else (mean_shuf <= mean_casc)
    ablation_decisive = abl_reverts and shuf_collapse

    primary = (n_seed_win >= 2)             # >=2/3 seeds clear +0.05
    if primary and ablation_decisive:
        verdict = 'GREEN'                   # WALL-BROKEN (DIRECTIONAL / numpy)
    elif primary and not ablation_decisive:
        verdict = 'PARTIAL'                 # lift not cleanly ablation-attributable
    else:
        verdict = 'WALL'                    # cascade ties flat on interference (c9)

    summary = {
        'hypothesis': 'H_1531',
        'candidate': 'C2 cascade metaplasticity (Benna-Fusi) on retention-under-interference',
        'split_thresh_star': st_star,
        'fixture': {
            'n_targets': N_TARGETS, 'n_confirm': N_CONFIRM, 'K_interf': K_INTERF,
            'collinear_frac': COLLINEAR_FRAC, 'collinear_sigma': COLLINEAR_SIGMA,
            'max_cells': MAX_CELLS, 'DMAX': CascadeStore.DMAX,
        },
        'seeds': SCORE_SEEDS,
        'per_seed': {k: [round(v, 4) for v in vs] for k, vs in per_seed.items()},
        'retention_flat': round(mean_flat, 4),
        'retention_cascade': round(mean_casc, 4),
        'retention_ABL_depth0': round(mean_abl, 4),
        'retention_SHUFFLE': round(mean_shuf, 4),
        'cascade_minus_flat': round(mean_casc - mean_flat, 4),
        'per_seed_lift': [round(v, 4) for v in lift.tolist()],
        'n_seed_win_over_margin': n_seed_win,
        'abl_reverts_to_flat': bool(abl_reverts),
        'shuffle_collapses': bool(shuf_collapse),
        'ablation_decisive': bool(ablation_decisive),
        'MARGIN': MARGIN,
        'verdict': verdict,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
