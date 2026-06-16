"""
H_1294 — HIERARCHICAL PFC GOAL→SUBGOAL CONTROLLER (HD31). R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1294_hierarchical_pfc/H_1294_FREEZE.txt (pre-registered
BEFORE this scoring). $0 CPU numpy, gradient-free, 3 seeds [4294,4295,4296], p7.
a_no_llm_frame_trap (prefrontal hierarchical-control lens, c15) — NOT an LLM recipe.
ENGINE-TRANSFER UNVERIFIED until R2 (this is a directional mirror of the immune store).

THE NEW STRUCTURE = a 2-level goal STACK {top goal, ordered subgoal list, pointer p}
with COMPLETION-TRIGGERED ADVANCE + goal PERSISTENCE. DISTINCT from VBasalGate
(single-step one-of-K selection, NO pointer/plan) and WorkMemBuffer (passive leaky
maintenance, NO controller/advance). Tested on an ORDERED 3-fact-chain grounding task
that a flat one-of-K selector (the live engine's analogue) cannot solve.
"""
import numpy as np

# ── frozen constants (from FREEZE) ──────────────────────────────────────────
DIM        = 64
RECALL_THR = 0.30
CHAIN_LEN  = 3
N_EPISODES = 40
N_DISTRACT = 4
CUE_NOISE  = 0.02
SEEDS      = [4294, 4295, 4296]


def fnv_3gram(text, dim=DIM):
    """byte-3gram FNV-1a hash embedding, L2-normalized (matches the engine key geometry)."""
    b = text.encode("utf-8")
    v = np.zeros(dim, dtype=np.float64)
    for i in range(len(b) - 2):
        h = 2166136261
        for j in range(3):
            h ^= b[i + j]
            h = (h * 16777619) & 0xFFFFFFFF
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


class ImmuneStore:
    """minimal mirror of ImmuneMemoryGrow recall — bind a cell per fact, recall =
    best-affinity cell margin, ABSTAIN (margin<=0) if no cell within recall_thr."""
    def __init__(self):
        self.protos = []

    def bind(self, key):
        self.protos.append(key)

    def margin(self, key):
        if not self.protos:
            return 0.0
        errs = [float(np.linalg.norm(p - key)) for p in self.protos]
        err = min(errs)
        m = 1.0 - err / RECALL_THR
        return max(0.0, min(1.0, m))


# ── task construction ────────────────────────────────────────────────────────
# A top goal = "ground a 3-fact chain about subject X". Subgoals = recall fact-A/B/C(X)
# IN ORDER. Each episode: pick a subject, bind its 3 chain facts into the store, then
# present a NOISY cue stream interleaving the 3 ordered cues with distractor cues
# (out-of-order facts of OTHER subjects + ungrounded random cues). The controller must
# emit subgoal facts IN ORDER 1->2->3.

CHAIN_TAGS = ["alpha", "beta", "gamma"]   # fact-A / fact-B / fact-C role tags


def make_episode(rng, n_subjects=12):
    store = ImmuneStore()
    subjects = [f"subj{ i:03d}" for i in range(n_subjects)]
    # bind every subject's 3-fact chain
    chain_keys = {}
    for s in subjects:
        keys = []
        for t in CHAIN_TAGS:
            k = fnv_3gram(f"{s}.{t}")
            store.bind(k)
            keys.append(k)
        chain_keys[s] = keys
    target = subjects[int(rng.integers(n_subjects))]
    ordered = [chain_keys[target][i] + rng.standard_normal(DIM) * CUE_NOISE
               for i in range(CHAIN_LEN)]
    # distractor cues: out-of-order facts of OTHER subjects + ungrounded random cues
    distractors = []
    others = [s for s in subjects if s != target]
    for _ in range(N_DISTRACT):
        if rng.random() < 0.5 and others:
            os_ = others[int(rng.integers(len(others)))]
            distractors.append(chain_keys[os_][int(rng.integers(CHAIN_LEN))]
                               + rng.standard_normal(DIM) * CUE_NOISE)
        else:
            r = rng.standard_normal(DIM)
            distractors.append(r / np.linalg.norm(r))   # ungrounded random cue
    return store, ordered, distractors, chain_keys, target


def _present_stream(rng, ordered, distractors):
    """Build a per-tick cue stream. Each tick shows a window of cues (the current set
    of candidates the controller sees). We schedule the ordered cues to appear over
    time, interleaved with distractors — but NOT pre-labeled by role/order."""
    # tick schedule: at tick t, the t-th ordered cue becomes 'available' alongside
    # a refreshed distractor window. (The controller does NOT know which is which —
    # it only reads grounding margin + its own pointer.)
    ticks = []
    for t in range(CHAIN_LEN):
        window = [ordered[t]]
        # add a couple distractors into the window
        k = 2
        idxs = list(range(len(distractors)))
        rng.shuffle(idxs)
        for di in idxs[:k]:
            window.append(distractors[di])
        rng.shuffle(window)
        ticks.append(window)
    return ticks


# ── ARM A: FLAT-SELECT (live-engine analogue, no pointer) ────────────────────
def run_flat(rng, ordered, distractors, store, target_keys):
    """Single-step one-of-K go/no-go by grounding margin, NO pointer, NO ordering, NO
    memory of done subgoals. Emits the best-grounded cue in the window each tick
    (a faithful stand-in for VBasalGate / the flat 8-weight gate)."""
    ticks = _present_stream(rng, ordered, distractors)
    emitted_order = []   # sequence of which target-subgoal index was emitted (or -1 fab)
    out_of_order = 0
    for window in ticks:
        margins = [store.margin(c) for c in window]
        best = int(np.argmax(margins))
        if margins[best] <= 0.0:
            continue   # nothing grounded -> abstain this tick
        # identify which target subgoal (if any) this cue corresponds to
        sel = window[best]
        role = _match_target_role(sel, target_keys)
        emitted_order.append(role)
        if role < 0:
            out_of_order += 1   # emitted an ungrounded/other-subject cue as if a fact
    return _score(emitted_order, out_of_order)


# ── ARM B: HIER-PFC (2-level goal stack with pointer + completion-advance) ───
def run_hier(rng, ordered, distractors, store, target_keys, plan_order=None,
             freeze_pointer=False):
    """2-level controller: top goal + ordered subgoal list + pointer p. Emits ONLY
    subgoal[p] when grounded, ADVANCES p on completion, SUPPRESSES out-of-order /
    ungrounded cues. plan_order permutes the subgoal order (shuffle control).
    freeze_pointer pins p=0 (ablate-advance control)."""
    if plan_order is None:
        plan_order = list(range(CHAIN_LEN))
    ticks = _present_stream(rng, ordered, distractors)
    p = 0
    emitted_order = []
    out_of_order = 0
    # the controller's CURRENT subgoal target key = the plan_order[p]-th target chain key
    for window in ticks:
        if p >= CHAIN_LEN:
            break
        cur_target = target_keys[plan_order[p]]
        # the controller looks for a cue in the window that matches its CURRENT subgoal
        # (grounded against the store AND closest to the current-subgoal target).
        best_c, best_align = None, -1.0
        for c in window:
            if store.margin(c) <= 0.0:
                continue
            align = float(np.dot(c / (np.linalg.norm(c) + 1e-9),
                                 cur_target / (np.linalg.norm(cur_target) + 1e-9)))
            if align > best_align:
                best_align, best_c = align, c
        # emit only if a cue plausibly matches the CURRENT subgoal (align high)
        if best_c is not None and best_align >= 0.85:
            role = _match_target_role(best_c, target_keys)
            emitted_order.append(role)
            if role != plan_order[p]:
                out_of_order += 1   # matched current subgoal but it was actually another
            if not freeze_pointer:
                p += 1              # COMPLETION-TRIGGERED ADVANCE
        # else: suppress (no grounded current-subgoal cue this tick) -> hold pointer
    return _score(emitted_order, out_of_order)


def _match_target_role(cue, target_keys):
    """Which target subgoal (0/1/2) does this cue best match, if grounded; else -1."""
    best, best_align = -1, 0.85
    for i, tk in enumerate(target_keys):
        align = float(np.dot(cue / (np.linalg.norm(cue) + 1e-9),
                             tk / (np.linalg.norm(tk) + 1e-9)))
        if align > best_align:
            best_align, best = align, i
    return best


def _score(emitted_order, out_of_order):
    """ordered-chain completion = emitted exactly [0,1,2] in order, no fab. Returns
    (completed: 0/1, out_of_order_count, n_emit)."""
    # strip fabs for the ordering check but they count against no-fab
    clean = [r for r in emitted_order if r >= 0]
    completed = 1 if clean == [0, 1, 2] else 0
    return completed, out_of_order, len(emitted_order)


# ── run all arms over seeds ──────────────────────────────────────────────────
def run_seed(seed):
    rng = np.random.default_rng(seed)
    import random as _r
    pr = _r.Random(seed)   # for shuffle/window scheduling determinism

    arms = {"A": [], "B": [], "Bshuf": [], "Babl": []}
    fab = {"A": 0, "B": 0, "Bshuf": 0, "Babl": 0}
    emits = {"A": 0, "B": 0, "Bshuf": 0, "Babl": 0}

    for ep in range(N_EPISODES):
        store, ordered, distractors, chain_keys, target = make_episode(rng)
        target_keys = chain_keys[target]   # clean (noise-free) target keys for alignment

        # use a per-arm rng-shuffle stream but SAME episode content
        for arm in arms:
            # rebuild a fresh python-rng so each arm sees the SAME stream schedule
            stream_rng = _r.Random(seed * 1000 + ep)
            if arm == "A":
                c, oo, ne = run_flat(stream_rng, ordered, distractors, store, target_keys)
            elif arm == "B":
                c, oo, ne = run_hier(stream_rng, ordered, distractors, store, target_keys)
            elif arm == "Bshuf":
                # PERMUTE the plan order (shuffle control)
                po = list(range(CHAIN_LEN)); _r.Random(seed * 7 + ep).shuffle(po)
                if po == [0, 1, 2]:
                    po = [2, 0, 1]   # ensure genuinely permuted
                c, oo, ne = run_hier(stream_rng, ordered, distractors, store,
                                     target_keys, plan_order=po)
            else:  # Babl
                c, oo, ne = run_hier(stream_rng, ordered, distractors, store,
                                     target_keys, freeze_pointer=True)
            arms[arm].append(c)
            fab[arm] += oo
            emits[arm] += ne

    res = {}
    for arm in arms:
        comp = float(np.mean(arms[arm]))
        fab_rate = fab[arm] / max(1, emits[arm])
        res[arm] = (comp, fab_rate)
    return res


def main():
    print("=" * 78)
    print("H_1294 — HIERARCHICAL PFC GOAL->SUBGOAL CONTROLLER (HD31) — R1 numpy MIRROR")
    print("=" * 78)
    per_seed = {}
    for s in SEEDS:
        per_seed[s] = run_seed(s)
        r = per_seed[s]
        print(f"seed {s}:  A.comp={r['A'][0]:.3f}  B.comp={r['B'][0]:.3f}  "
              f"Bshuf={r['Bshuf'][0]:.3f}  Babl={r['Babl'][0]:.3f}  "
              f"B.fab={r['B'][1]:.3f}")

    def mean(arm, idx=0):
        return float(np.mean([per_seed[s][arm][idx] for s in SEEDS]))

    A, B = mean("A"), mean("B")
    Bshuf, Babl = mean("Bshuf"), mean("Babl")
    Bfab = mean("B", 1)
    print("-" * 78)
    print(f"MEAN:  A.comp={A:.3f}  B.comp={B:.3f}  Bshuf={Bshuf:.3f}  "
          f"Babl={Babl:.3f}  B.fab={Bfab:.3f}")

    # frozen predicate
    c1_each = all(per_seed[s]["B"][0] >= per_seed[s]["A"][0] + 0.30 for s in SEEDS)
    c1 = c1_each and (B >= A + 0.30)
    c2 = A < 0.50
    c3 = Bshuf <= A + 0.15
    c4 = Babl <= A + 0.15
    c5 = Bfab <= 0.10
    print("-" * 78)
    print(f"c1 PRESENCE     B>=A+0.30 (each+mean): {c1}   (B-A mean={B-A:+.3f})")
    print(f"c2 DISTINCT     A<0.50 (flat fails)  : {c2}   (A={A:.3f})")
    print(f"c3 EARNED-ORDER Bshuf<=A+0.15        : {c3}   (Bshuf={Bshuf:.3f})")
    print(f"c4 EARNED-ADV   Babl<=A+0.15         : {c4}   (Babl={Babl:.3f})")
    print(f"c5 NO-FAB       B.fab<=0.10          : {c5}   (B.fab={Bfab:.3f})")
    green = c1 and c2 and c3 and c4 and c5
    print("=" * 78)
    print(f"VERDICT (R1 mirror, DIRECTIONAL): {'GREEN' if green else 'RED / WALL'}")
    print("=" * 78)


if __name__ == "__main__":
    main()
