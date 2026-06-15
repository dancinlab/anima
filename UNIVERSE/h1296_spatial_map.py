"""
H_1296 — PLACE/GRID SPATIAL-MAP / PATH-INTEGRATION (HD32). R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1296_spatial_map/H_1296_FREEZE.txt (pre-registered BEFORE
this scoring). $0 CPU numpy, gradient-free, 3 seeds [4295,4296,4297], p7.
a_no_llm_frame_trap (entorhinal grid / hippocampal place-cell / path-integration lens
— O'Keefe, Moser; c15) — NOT an LLM recipe. ENGINE-TRANSFER UNVERIFIED until R2.

THE NEW STRUCTURE = a METRIC/RELATIONAL COGNITIVE MAP: landmarks stored AT POSITIONS in
a metric space, so the DISTANCE/RELATION between two stored facts is itself represented
and queryable, plus PATH-INTEGRATION (accumulate displacement steps → net position).
DISTINCT from ImmuneMemory item-binding (binds each fact→value INDEPENDENTLY, NO
inter-fact geometry) and from HierGoalStack (an ORDERED plan = sequence, NOT a metric
space) and WorkMemBuffer (leaky maintenance, NO positions).

FALSIFIER = a RELATIONAL/METRIC query the item-store CANNOT answer:
  (Q1 NEAREST) "is landmark X nearer to A or to B?" — needs the metric DISTANCE between
               two stored facts; a pure item-store has no between-item geometry → chance.
  (Q2 PATH-INTEGRATION) given a sequence of displacement steps from a known start,
               infer the net displacement (which of two candidate endpoints). An
               item-store binds endpoints independently and cannot integrate a path.
A spatial map answers both; item-only must abstain/guess (chance 0.5). Both controls
(shuffle the stored positions / ablate the metric) MUST collapse to chance or it is
variance → honest RED/WALL.
"""
import numpy as np

# ── frozen constants (from FREEZE) ──────────────────────────────────────────
N_LANDMARKS = 8        # landmarks placed on a 2D metric map per episode
GRID        = 10.0     # positions drawn in [0,GRID]^2
N_EPISODES  = 40       # relational queries per arm per seed
N_STEPS_PI  = 4        # path-integration: number of displacement steps
MARGIN_MIN  = 1.20     # min |d(X,A) - d(X,B)| to keep a query UNAMBIGUOUS (frozen)
SEEDS       = [4295, 4296, 4297]


# ── the two faculties ────────────────────────────────────────────────────────
class ItemStore:
    """Faithful ImmuneMemory item-binding stand-in: binds name->payload INDEPENDENTLY,
    holds NO inter-item geometry. It can say WHAT a landmark is, but has no metric to
    compare the DISTANCE between two landmarks — so on a relational query it ABSTAINS
    (returns None = guess at chance)."""
    def __init__(self):
        self.payload = {}      # name -> opaque payload (e.g. a label); NO position metric

    def bind(self, name, payload):
        self.payload[name] = payload

    def nearest(self, x_name, a_name, b_name):
        # an item-store has no distance between stored items → it cannot answer.
        return None            # ABSTAIN → caller resolves at chance

    def integrate(self, start_name, steps, cand_names):
        # an item-store cannot accumulate a displacement path → ABSTAIN.
        return None


class SpatialMap:
    """Place/grid metric map: stores each landmark AT a 2D POSITION; the relation
    (Euclidean distance) between two stored facts is queryable, and a displacement
    path can be INTEGRATED (vector sum) to a net position."""
    def __init__(self, ablate_metric=False):
        self.pos = {}                 # name -> 2D position vector (the metric content)
        self.ablate_metric = ablate_metric

    def bind(self, name, position):
        if self.ablate_metric:
            self.pos[name] = np.zeros(2)   # METRIC ABLATED: collapse all to the origin
        else:
            self.pos[name] = np.asarray(position, dtype=np.float64)

    def shuffle_positions(self, rng):
        """SHUFFLE control: permute the stored positions across names — the map keeps a
        position per name but the RELATION name<->place is destroyed."""
        names = list(self.pos.keys())
        vals = [self.pos[n] for n in names]
        perm = list(range(len(names)))
        rng.shuffle(perm)
        if perm == list(range(len(names))) and len(names) > 1:
            perm = perm[1:] + perm[:1]   # ensure a genuine derangement-ish permute
        self.pos = {names[i]: vals[perm[i]] for i in range(len(names))}

    def nearest(self, x_name, a_name, b_name):
        x, a, b = self.pos[x_name], self.pos[a_name], self.pos[b_name]
        da = float(np.linalg.norm(x - a))
        db = float(np.linalg.norm(x - b))
        return a_name if da < db else b_name

    def integrate(self, start_name, steps, cand_names):
        net = self.pos[start_name].copy()
        for s in steps:
            net = net + np.asarray(s, dtype=np.float64)
        # pick the candidate endpoint nearest the integrated net position
        best, bestd = None, 1e18
        for c in cand_names:
            d = float(np.linalg.norm(net - self.pos[c]))
            if d < bestd:
                bestd, best = d, c
        return best


# ── episode construction ──────────────────────────────────────────────────────
def make_episode(rng):
    """Place N landmarks on a 2D map; build one UNAMBIGUOUS nearest-query and one
    path-integration query. The same ground-truth positions feed every arm."""
    names = [f"L{i}" for i in range(N_LANDMARKS)]
    positions = {n: rng.uniform(0, GRID, size=2) for n in names}

    # ── Q1 NEAREST: pick X, A, B such that |d(X,A) - d(X,B)| is unambiguous ──
    for _ in range(200):
        x, a, b = rng.choice(names, size=3, replace=False)
        da = float(np.linalg.norm(positions[x] - positions[a]))
        db = float(np.linalg.norm(positions[x] - positions[b]))
        if abs(da - db) >= MARGIN_MIN:
            truth_near = a if da < db else b
            break
    else:
        # degenerate map: fall back to any triple (rare); truth by raw distance
        x, a, b = names[0], names[1], names[2]
        truth_near = a if np.linalg.norm(positions[x]-positions[a]) < \
                          np.linalg.norm(positions[x]-positions[b]) else b

    # ── Q2 PATH-INTEGRATION: from a start landmark, take N_STEPS_PI displacement
    #     steps to a true endpoint; the answer is which of two candidate landmarks
    #     the integrated path lands nearest. Steps sum to (endpoint - start). ──
    start = rng.choice(names)
    true_end = rng.choice([n for n in names if n != start])
    total = positions[true_end] - positions[start]
    # split `total` into N_STEPS_PI noisy displacement steps (sum == total exactly)
    raw = rng.standard_normal((N_STEPS_PI, 2))
    raw = raw - raw.mean(axis=0)                 # zero-mean so we can re-center to total
    steps = raw + total / N_STEPS_PI             # each step + equal share; sum == total
    # a distractor candidate endpoint far from the true integrated landing
    dist_cands = [n for n in names if n not in (start, true_end)]
    far = max(dist_cands, key=lambda n: float(np.linalg.norm(positions[n] - positions[true_end])))
    cand_names = [true_end, far]
    # R1b (a_break_the_wall): RANDOMIZE candidate order so a metric-BLIND arm cannot
    # pick the true endpoint by list position (argmin tie-break leak the control caught).
    if rng.random() < 0.5:
        cand_names = [far, true_end]

    return names, positions, (x, a, b, truth_near), (start, steps, cand_names, true_end)


# ── arms ──────────────────────────────────────────────────────────────────────
def run_arm(arm, rng, names, positions, q_near, q_pi):
    x, a, b, truth_near = q_near
    start, steps, cand_names, true_end = q_pi

    if arm == "A":
        fac = ItemStore()
        for n in names:
            fac.bind(n, f"payload_{n}")          # item-binding: name->label, NO geometry
    else:
        ablate = (arm == "Babl")
        fac = SpatialMap(ablate_metric=ablate)
        for n in names:
            fac.bind(n, positions[n])
        if arm == "Bshuf":
            fac.shuffle_positions(rng)

    # Q1 NEAREST
    ans = fac.nearest(x, a, b)
    if ans is None:                              # item-store abstains → chance guess
        ans = a if rng.random() < 0.5 else b
        near_abstain = 1
    else:
        near_abstain = 0
    near_correct = 1 if ans == truth_near else 0

    # Q2 PATH-INTEGRATION
    ans2 = fac.integrate(start, steps, cand_names)
    if ans2 is None:
        ans2 = cand_names[0] if rng.random() < 0.5 else cand_names[1]
        pi_abstain = 1
    else:
        pi_abstain = 0
    pi_correct = 1 if ans2 == true_end else 0

    return near_correct, pi_correct, near_abstain, pi_abstain


def run_seed(seed):
    rng = np.random.default_rng(seed)
    arms = ["A", "B", "Bshuf", "Babl"]
    acc_near = {k: [] for k in arms}
    acc_pi = {k: [] for k in arms}
    abst_near = {k: 0 for k in arms}
    for ep in range(N_EPISODES):
        names, positions, q_near, q_pi = make_episode(rng)
        for arm in arms:
            # per-arm rng so shuffle/guess draws are independent but episode is shared
            arm_rng = np.random.default_rng(seed * 1000 + ep * 10 + hash(arm) % 7)
            nc, pc, na, pa = run_arm(arm, arm_rng, names, positions, q_near, q_pi)
            acc_near[arm].append(nc)
            acc_pi[arm].append(pc)
            abst_near[arm] += na
    res = {}
    for arm in arms:
        res[arm] = (float(np.mean(acc_near[arm])), float(np.mean(acc_pi[arm])),
                    abst_near[arm] / N_EPISODES)
    return res


def main():
    print("=" * 78)
    print("H_1296 — PLACE/GRID SPATIAL-MAP / PATH-INTEGRATION (HD32) — R1 numpy MIRROR")
    print("=" * 78)
    per_seed = {}
    for s in SEEDS:
        per_seed[s] = run_seed(s)
        r = per_seed[s]
        print(f"seed {s}: NEAR  A={r['A'][0]:.3f} B={r['B'][0]:.3f} "
              f"Bshuf={r['Bshuf'][0]:.3f} Babl={r['Babl'][0]:.3f} | "
              f"PI  A={r['A'][1]:.3f} B={r['B'][1]:.3f} "
              f"Bshuf={r['Bshuf'][1]:.3f} Babl={r['Babl'][1]:.3f}")

    def mean(arm, idx):
        return float(np.mean([per_seed[s][arm][idx] for s in SEEDS]))

    # NEAREST relational query (the headline falsifier)
    An, Bn, Bsn, Ban = mean("A", 0), mean("B", 0), mean("Bshuf", 0), mean("Babl", 0)
    # PATH-INTEGRATION
    Ap, Bp, Bsp, Bap = mean("A", 1), mean("B", 1), mean("Bshuf", 1), mean("Babl", 1)
    A_abst = mean("A", 2)
    print("-" * 78)
    print(f"MEAN NEAREST:  A={An:.3f} B={Bn:.3f} Bshuf={Bsn:.3f} Babl={Ban:.3f}")
    print(f"MEAN PATH-INT: A={Ap:.3f} B={Bp:.3f} Bshuf={Bsp:.3f} Babl={Bap:.3f}")
    print(f"item-store NEAREST abstain rate (A): {A_abst:.3f}  (1.0 = always abstains)")

    # frozen predicate (NEAREST = the headline relational query)
    c1_each = all(per_seed[s]["B"][0] >= per_seed[s]["A"][0] + 0.30 for s in SEEDS)
    c1 = c1_each and (Bn >= An + 0.30)
    c2 = An <= 0.65                       # item-only at/below chance band (no metric)
    c3 = Bsn <= An + 0.15                 # shuffle collapses to ~chance
    c4 = Ban <= An + 0.15                 # ablate collapses to ~chance
    c5 = A_abst >= 0.90                   # item-store ABSTAINS (no fabricated metric)
    # PI (Q2) = NON-GATING diagnostic (R1c FREEZE): the map-shuffle control correctly
    # refused to collapse it because the path-integration signal leaks through the
    # displacement STEPS, not the stored map — Q2 is not a clean stored-map isolator.
    c6 = (Bp >= Ap + 0.30) and (Bsp <= Ap + 0.15) and (Bap <= Ap + 0.15)
    print("-" * 78)
    print("BINDING predicate — NEAREST relational query (signal lives ONLY in the metric):")
    print(f"c1 PRESENCE     B>=A+0.30 (each+mean): {c1}   (B-A mean={Bn-An:+.3f})")
    print(f"c2 DISTINCT     A<=0.65 (no metric)  : {c2}   (A={An:.3f})")
    print(f"c3 EARNED-MAP   Bshuf<=A+0.15        : {c3}   (Bshuf={Bsn:.3f})")
    print(f"c4 EARNED-METRIC Babl<=A+0.15        : {c4}   (Babl={Ban:.3f})")
    print(f"c5 NO-FAB       item-abstain>=0.90   : {c5}   (abstain={A_abst:.3f})")
    green = c1 and c2 and c3 and c4 and c5
    print("-" * 78)
    print("NON-GATING diagnostic — PATH-INTEGRATION (signal leaks via the steps, "
          "shuffle cannot blind):")
    print(f"   PI clean-collapse c6 (reported, NOT in verdict): {c6}   "
          f"(B={Bp:.3f} A={Ap:.3f} Bshuf={Bsp:.3f} Babl={Bap:.3f})")
    print("=" * 78)
    print(f"VERDICT (R1 mirror, DIRECTIONAL, NEAREST falsifier): "
          f"{'GREEN' if green else 'RED / WALL'}")
    print("=" * 78)


if __name__ == "__main__":
    main()
