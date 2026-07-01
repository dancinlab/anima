#!/usr/bin/env python3
"""
H_1543 — DOPAMINE × CLS : salience-weighted REPLAY PRIORITY (FUSION).

Census H_1542 Rank 2 — interface DOF **I2 (fast→slow transfer priority)**. FUSES the
DA-RPE faculty (H_1536 🟢 #2520) INTO the H_1532 two-store CLS module (#2514 / R2 #2522).

WHY this fusion (a_no_llm_frame_trap · a_break_the_wall type-(d) only after ablation):
H_1532 broke the H_1284 NEUROMODULATION wall with TWO phase-separated stores — a FAST
episodic store (Hasselmo encode-mode → fresh cell) + a SLOW store consolidated by REPLAY
of the fast-store episodes. In H_1532 that replay is UNIFORM (every fast episode replayed
equally). Biology says replay is NOT uniform: dopamine-RPE prioritizes WHICH memories
reactivate first — high reward-prediction-error / high-value experiences are preferentially
replayed (Lisman-Grace 2005 hippocampal-VTA loop; McNamara et al. 2014 dopaminergic
modulation of place-cell replay; Mattar & Daw 2018 prioritized memory access; Ambrose-
Pfeiffer-Foster 2016 reward-biased replay). H_1536 already proved DA-RPE is a real
standalone faculty (credit-assignment DA=1.000 vs recency 0.291). This lane FUSES it: the
DA-RPE per-identity value V(s) becomes the REPLAY-PRIORITY ranking inside CLS.

⚠ THE STRUCTURAL PRECONDITION (census-flagged, the whole point): the lever is meaningful
ONLY under a CONSOLIDATION BUDGET — the slow store can absorb only K < N fast episodes per
sweep before the fast buffer decays. With scarcity, WHICH K you replay matters: DA-priority
keeps the high-value bindings; uniform/recency replay loses them. If K = N (no scarcity)
DA-priority MUST be INERT (everything consolidates regardless of order) — that is the
cheapest refuter and we report it explicitly (precondition check, honest scoping).

⚠ CRITICAL HAZARD (inherited from H_1532): the win must come from VALUE-RANKED transfer
over the fast→slow channel, NOT a scalar gain on one store. The ablations prove it:
  ABL    : DA value forced CONSTANT (V≡const) ⇒ ranking degenerates → reverts to UNIFORM.
  SHUFFLE: the DA value↔episode pairing permuted ⇒ priority dissociated from value
           ⇒ collapse (the ranking carries no real signal).
  merge-precondition: K=N removes scarcity ⇒ DA must be INERT (no transfer to order).

p7: exact ground truth (each binding's true value tag is known; metric = retained
high-value bindings), NO LLM judge, NO perplexity, NO loss term — every decision is a
no-grad read of substrate state. p8: replay = the engine's own consolidation tick. $0 CPU.
3 seeds. Frozen falsifier in H_1543_FREEZE.txt.

R1 numpy DIRECTIONAL (host has no torch; a_engine_native_learning hard-gate-1: grep numpy
⇒ auto-DIRECTIONAL, terminal NOT permitted) — engine R2 §DaReplay deferred ING.

REUSES H_1532 MemStore/key_vec/FNV-1a/MARGIN byte-for-byte + H_1536 TD(λ) value head
byte-for-byte (the DA-RPE faculty that supplies the priority).
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / CORE/engine_cli.hexa §MultiStore) ──
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 16                   # key dim (H_1227 byte-trigram FNV-1a; toy 16, same as H_1532/H_1284)
MARGIN = 0.10              # frozen lift bar for the FUSION presence test (≥+0.10, the H_1536 bar)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532 / H_1284) ───────────────────
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


# ── VAdaptField numpy mirror (byte-faithful to vadapt_field_step — VERBATIM H_1532) ──
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
        retrieval path gated OFF ⇒ a new fact is laid down in a FRESH cell instead of
        overwriting the winner it would otherwise refine. Phase-separation mechanism."""
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
        """nearest-cell fires; ABSTAIN (None) if recon-err > abstain margin."""
        self.tick += 1
        win, err, second = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None, err, second
        self.lru[win] = self.tick
        return self.values[win], err, second


# ── DA-RPE value head (TD(λ), VERBATIM mechanism from H_1536) ──────────────────
# The dopamine faculty: a per-identity value learned by TD(λ). High |value| episodes are
# the high-reward-prediction-error experiences biology replays first. We learn a scalar
# value PER BINDING-IDENTITY (which A_i carries reward) and use it as the replay PRIORITY.
GAMMA = 0.95
LAMBDA = 0.8
ALPHA = 0.05
N_EPOCHS = 30


def da_rpe_values(value_tags, n_pairs, zero_delta=False, shuffle_rng=None):
    """DA-RPE per-pair value via TD(λ) over single-step reward episodes.

    Each pair A_i carries a true scalar reward tag value_tags[i] (HIGH=1.0 or LOW=0.0). The
    DA faculty learns V(A_i) = expected reward of that identity by TD over (A_i → terminal,
    r=value_tags[i]) episodes — exactly the H_1536 RPE computation, here one step per pair.
    zero_delta: ABL — δ forced 0 ⇒ V stays flat ⇒ all-equal priority (reverts to uniform).
    shuffle_rng: SHUFFLE — permute which reward tag trains which identity ⇒ value dissociated
    from the true high-value bindings ⇒ priority carries no real signal.
    Returns a value per pair index (the replay-priority signal)."""
    tags = list(value_tags)
    if shuffle_rng is not None:
        perm = shuffle_rng.permutation(n_pairs)
        tags = [value_tags[perm[i]] for i in range(n_pairs)]
    # value head keyed on a per-identity one-hot (collision-free per-pair slot, H_1536 ident key)
    w = np.zeros(n_pairs, dtype=np.float64)
    for _ in range(N_EPOCHS):
        for i in range(n_pairs):
            phi = np.zeros(n_pairs); phi[i] = 1.0
            v_t = float(w @ phi)
            # one-step absorbing terminal: V(terminal):=0, reward = tag delivered on arrival
            delta = tags[i] + GAMMA * 0.0 - v_t
            if zero_delta:
                delta = 0.0
            e = phi  # single-step eligibility
            w = w + ALPHA * delta * e
    return np.array([float(w[i]) for i in range(n_pairs)], dtype=np.float64)


# ── AB-AC interference fixture WITH reward tags (extends H_1532 make_abac) ─────
def make_abac(n_pairs, n_distract, rng, frac_high=0.5):
    """n_pairs shared keys A_i, each A_i->B_i (phase 1, the binding to RETAIN) then A_i->C_i
    (phase 2, the interfering re-bind) + distractors. EXTENSION vs H_1532: each pair carries
    a REWARD TAG (HIGH-value or LOW-value). Under a consolidation budget the slow store can
    only replay K<N fast episodes; the capability = retain the HIGH-value A_i->B_i bindings.
    Which A_i are high-value is INDEPENDENT of position/recency (recency-uninformative)."""
    A = [f"key_A{i:03d}" for i in range(n_pairs)]
    B = [f"val_B{rng.integers(0, 99999):05d}" for _ in range(n_pairs)]
    C = [f"val_C{rng.integers(0, 99999):05d}" for _ in range(n_pairs)]
    for i in range(n_pairs):
        while C[i] == B[i]:
            C[i] = f"val_C{rng.integers(0, 99999):05d}"
    # reward tags: a random subset is HIGH-value (the bindings that MUST survive consolidation)
    n_high = int(round(n_pairs * frac_high))
    high_idx = set(rng.choice(n_pairs, size=n_high, replace=False).tolist())
    value_tags = np.array([1.0 if i in high_idx else 0.0 for i in range(n_pairs)], dtype=np.float64)
    D_keys = [f"key_D{j:03d}" for j in range(n_distract)]
    D_vals = [f"val_D{rng.integers(0, 99999):05d}" for _ in range(n_distract)]
    return A, B, C, D_keys, D_vals, value_tags, high_idx


# ── two-store CLS with BUDGETED, PRIORITIZED replay (the fusion) ───────────────
def run_cls_budget(A, B, C, Dk, Dv, value_tags, high_idx,
                   max_cells, LR, THRESH, abstain, K,
                   priority='da', merge=False, da_zero=False, shuffle_da=False, rng=None):
    """Two-store CLS (H_1532) + a consolidation BUDGET K and a replay PRIORITY policy.

    FAST episodic store: phase-1 A->B (encode-mode, fresh cells). SLOW store: phase-2 A->C +
    distractors (interfering). REPLAY consolidates only K of the N fast A->B episodes into the
    slow store (budget) — chosen by `priority`:
       'da'      : rank by DA-RPE learned value (high |V| first)  — the fusion arm.
       'uniform' : random K of N (H_1532's uniform replay, the baseline).
       'recency' : the LAST K written to the fast store.
    Un-replayed fast episodes DECAY (evicted from the fast buffer before recall — the budget
    bites). Retention is scored on the HIGH-value pairs only (the bindings that mattered).

    merge=True : K=N degenerate path is handled by the caller; merge collapses to one store
                 (no transfer to order) — used as the structural precondition ablation."""
    fast = MemStore(max_cells, abstain, LR, THRESH)
    slow = MemStore(max_cells, abstain, LR, THRESH)
    n_pairs = len(A)

    if merge:
        # MERGE: one store, no phase-separation, no transfer — priority undefined → one-store.
        m = MemStore(max_cells, abstain, LR, THRESH)
        for a, b in zip(A, B):
            m.write(key_vec(a), b)
        for k, v in list(zip(A, C)) + list(zip(Dk, Dv)):
            m.write(key_vec(k), v)
        return _score_high_retention(m, None, A, B, high_idx)

    # phase 1: A->B into FAST episodic, encode-mode (retrieval suppressed → fresh cells)
    for a, b in zip(A, B):
        fast.write(key_vec(a), b, suppress_retrieval=True)
    # phase 2: A->C re-bindings + distractors into SLOW store (interfering writes)
    for k, v in list(zip(A, C)) + list(zip(Dk, Dv)):
        slow.write(key_vec(k), v, suppress_retrieval=False)

    # ── compute replay PRIORITY ranking over the N fast A->B episodes ──
    if priority == 'da':
        vals = da_rpe_values(value_tags, n_pairs, zero_delta=da_zero,
                             shuffle_rng=(rng if shuffle_da else None))
        order = list(np.argsort(-vals))          # high DA-value first
    elif priority == 'recency':
        order = list(range(n_pairs))[::-1]       # last-written first
    else:  # uniform
        order = list(rng.permutation(n_pairs))   # random K of N

    replay_idx = set(order[:K])                  # only K episodes survive consolidation

    # REPLAY: interleave the selected K episodic A->B traces into slow consolidation (CLS replay,
    # encode-mode → fresh slow cell so the A->C slow binding does not clobber it). The fast buffer
    # then DECAYS: only consolidated (replayed) bindings persist into the recall phase.
    for i in replay_idx:
        v, err, _ = fast.recall(key_vec(A[i]))
        if v is not None:
            slow.write(key_vec(A[i]), v, suppress_retrieval=True)

    # fast buffer decays: un-replayed episodes are gone (budget bites). Recall from slow only
    # (plus any replayed trace the slow store now holds).
    return _score_high_retention(None, slow, A, B, high_idx)


def _score_high_retention(single, slow, A, B, high_idx):
    """Retention of the HIGH-value A->B bindings: fraction of high-value A keys whose surviving
    store still returns OLD B. Abstain = NOT retained (honest). For merge (single store) recall
    from `single`; for two-store recall from the consolidated `slow` store."""
    store = single if single is not None else slow
    hi = sorted(high_idx)
    if not hi:
        return 0.0
    correct = 0
    for i in hi:
        pred, _, _ = store.recall(key_vec(A[i]))
        if pred == B[i]:
            correct += 1
    return correct / len(hi)


def grid_note():
    # LR/TH reuse H_1532's grid-tuned best-fixed (LR*=0.1, TH*=0.2 on disjoint seed 7). The
    # baseline here is UNIFORM replay under the SAME budget (the strongest honest no-DA arm) —
    # not a re-tune; DA must beat uniform replay, not a weaker store.
    return 0.1, 0.2


def main():
    N_PAIRS = 24
    N_DISTRACT = 24
    ABSTAIN0 = 0.45
    SCORE_SEEDS = [11, 22, 33]
    MAX_CELLS = max(4, int((N_PAIRS + N_DISTRACT) * 1.5))
    LR_star, TH_star = grid_note()
    K = N_PAIRS // 2                 # consolidation BUDGET: only half the fast episodes survive
    FRAC_HIGH = 0.5                  # half the pairs are high-value (the bindings that must survive)

    rows = []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        A, B, C, Dk, Dv, vtags, high_idx = make_abac(N_PAIRS, N_DISTRACT, rng, FRAC_HIGH)

        common = dict(max_cells=MAX_CELLS, LR=LR_star, THRESH=TH_star, abstain=ABSTAIN0, K=K)

        da = run_cls_budget(A, B, C, Dk, Dv, vtags, high_idx, priority='da',
                            rng=np.random.default_rng(seed + 1), **common)
        uni = run_cls_budget(A, B, C, Dk, Dv, vtags, high_idx, priority='uniform',
                            rng=np.random.default_rng(seed + 2), **common)
        rec = run_cls_budget(A, B, C, Dk, Dv, vtags, high_idx, priority='recency',
                            rng=np.random.default_rng(seed + 3), **common)
        abl = run_cls_budget(A, B, C, Dk, Dv, vtags, high_idx, priority='da', da_zero=True,
                            rng=np.random.default_rng(seed + 4), **common)
        shf = run_cls_budget(A, B, C, Dk, Dv, vtags, high_idx, priority='da', shuffle_da=True,
                            rng=np.random.default_rng(seed + 5), **common)
        # precondition (cheapest refuter): K=N (no scarcity) ⇒ DA must be INERT vs uniform
        full = dict(common); full['K'] = N_PAIRS
        da_full = run_cls_budget(A, B, C, Dk, Dv, vtags, high_idx, priority='da',
                                rng=np.random.default_rng(seed + 6), **full)
        uni_full = run_cls_budget(A, B, C, Dk, Dv, vtags, high_idx, priority='uniform',
                                 rng=np.random.default_rng(seed + 7), **full)

        rows.append({'seed': seed,
                     'da_priority': round(da, 4), 'uniform': round(uni, 4),
                     'recency': round(rec, 4), 'abl_da0': round(abl, 4),
                     'shuffle_da': round(shf, 4),
                     'da_full_K=N': round(da_full, 4), 'uniform_full_K=N': round(uni_full, 4),
                     'da_minus_uniform': round(da - uni, 4),
                     'da_minus_recency': round(da - rec, 4),
                     'da_minus_uniform_K=N': round(da_full - uni_full, 4)})

    da_m = float(np.mean([r['da_priority'] for r in rows]))
    uni_m = float(np.mean([r['uniform'] for r in rows]))
    rec_m = float(np.mean([r['recency'] for r in rows]))
    abl_m = float(np.mean([r['abl_da0'] for r in rows]))
    shf_m = float(np.mean([r['shuffle_da'] for r in rows]))
    da_full_m = float(np.mean([r['da_full_K=N'] for r in rows]))
    uni_full_m = float(np.mean([r['uniform_full_K=N'] for r in rows]))

    # ── FROZEN falsifier (pre-registered in H_1543_FREEZE.txt) ────────────────
    #   A PRESENCE : da_priority - uniform >= +MARGIN on >= 2/3 seeds (high-value retention)
    #   B DISTINCT : uniform AND recency lose high-value under budget (da - uniform >= +MARGIN
    #                AND da - recency >= +MARGIN, mean)
    #   C EARNED   : ABL (DA->const) reverts to uniform (|abl - uniform| < MARGIN, mean)
    #   D SHUFFLE  : permuted DA value collapses (da - shuffle >= +MARGIN, mean)
    #   E NO-FAB   : abstain counts as not-retained (built into scoring — no fabrication credit)
    #   PRECONDITION (reported, not a GREEN gate): K=N ⇒ DA inert (|da - uniform| < MARGIN)
    n_win = sum(1 for r in rows if r['da_minus_uniform'] >= MARGIN)
    a_pass = n_win >= 2
    b_pass = (da_m - uni_m) >= MARGIN and (da_m - rec_m) >= MARGIN
    c_pass = abs(abl_m - uni_m) < MARGIN
    d_pass = (da_m - shf_m) >= MARGIN
    precondition_inert = abs(da_full_m - uni_full_m) < MARGIN

    if a_pass and b_pass and c_pass and d_pass:
        verdict = 'GREEN'   # FUSION WORKS: DA-RPE value as replay priority retains high-value bindings
    elif a_pass:
        verdict = 'AMBIGUOUS_ABLATION'  # lift exists but not cleanly attributable (ablation failed)
    else:
        verdict = 'WALL_HOLDS'          # DA-priority ties/loses to uniform replay under budget

    summary = {
        'capability': 'budgeted CLS consolidation: high-value A->B retention when only K<N replay',
        'fusion': 'H_1536 DA-RPE value  ->  H_1532 two-store CLS replay priority (interface I2)',
        'LR_star': LR_star, 'TH_star': TH_star,
        'N_PAIRS': N_PAIRS, 'N_DISTRACT': N_DISTRACT, 'MAX_CELLS': MAX_CELLS,
        'K_budget': K, 'FRAC_HIGH': FRAC_HIGH, 'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
        'per_seed': rows,
        'da_priority_mean': round(da_m, 4),
        'uniform_mean': round(uni_m, 4),
        'recency_mean': round(rec_m, 4),
        'abl_da0_mean': round(abl_m, 4),
        'shuffle_da_mean': round(shf_m, 4),
        'da_full_K=N_mean': round(da_full_m, 4),
        'uniform_full_K=N_mean': round(uni_full_m, 4),
        'da_minus_uniform_mean': round(da_m - uni_m, 4),
        'da_minus_recency_mean': round(da_m - rec_m, 4),
        'da_minus_shuffle_mean': round(da_m - shf_m, 4),
        'abl_minus_uniform_mean': round(abl_m - uni_m, 4),
        'da_minus_uniform_K=N_mean': round(da_full_m - uni_full_m, 4),
        'n_wins_over_uniform+MARGIN': n_win,
        'A_presence': bool(a_pass),
        'B_distinct': bool(b_pass),
        'C_earned_ablate': bool(c_pass),
        'D_shuffle': bool(d_pass),
        'precondition_K=N_inert': bool(precondition_inert),
        'verdict': verdict,
        'wired': 'DIRECTIONAL-mirror (numpy) -> R2 engine-native §DaReplay follow-on (ING)',
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    import sys
    s = main()
    if '--freeze' in sys.argv:
        with open('state/verdicts/1543_cls_da_replay/H_1543_R1.json', 'w') as f:
            json.dump(s, f, ensure_ascii=False, indent=2)
    sys.exit(0 if s['verdict'] == 'GREEN' else 1)
