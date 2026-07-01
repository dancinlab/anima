"""
H_1429 — TRANSITIVE INFERENCE / serial-order premise-integration (HD34). R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1429_transitive_inference/H_1429_FREEZE.txt (pre-registered
BEFORE this scoring). $0 CPU numpy, gradient-free, 3 seeds [4429,4430,4431], p7.
a_no_llm_frame_trap (transitive-inference paradigm — Bryant & Trabasso 1971; hippocampal
relational integration, Dusek & Eichenbaum 1997; symbolic-distance effect; c15) — NOT an
LLM recipe. ENGINE-TRANSFER UNVERIFIED until R2.

THE NEW STRUCTURE = a TRANSITIVE-INFERENCE faculty: from ADJACENT-only ordered premises
(A>B, B>C, C>D, ...) it INTEGRATES a latent 1-D rank and answers the order of NEVER-
OBSERVED non-adjacent pairs (A>C, A>D, B>D, ...). DISTINCT from ImmuneMemory item-binding
(memorizes the observed pairs, abstains on an unobserved pair), HierGoalStack (an order is
HANDED to it, it does not INFER one), and SpatialMap (stores GIVEN metric coordinates, not
a rank inferred from ordinal comparisons). The decisive bar = unobserved-pair generalization.
"""
import numpy as np

# ── frozen constants (from FREEZE) ──────────────────────────────────────────
DIM        = 64
RECALL_THR = 0.30
N_ITEMS    = 7
N_EP       = 30
CHANCE     = 0.50
SEEDS      = [4429, 4430, 4431]


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


# ── ARM A: ITEM-STORE (faithful ImmuneMemory item-binding stand-in) ──────────
class ItemStore:
    """Binds each PRESENTED ordered premise pair (higher,lower) by its FNV-trigram
    key. A query {X,Y} is answered ONLY if the exact ordered pair was bound (i.e. the
    pair was an observed premise); otherwise it ABSTAINS. No premise integration —
    this is item/episodic memory of the GIVEN pairs (the live-engine ImmuneMemory analogue)."""
    def __init__(self):
        self.keys = []      # bound premise-pair keys
        self.dirs = []      # (higher, lower) for the bound pair

    def bind(self, higher, lower):
        self.keys.append(fnv_3gram(f"{higher}>{lower}"))
        self.dirs.append((higher, lower))

    def _match(self, higher, lower):
        """is the ordered pair (higher>lower) within recall_thr of a bound key?"""
        if not self.keys:
            return False
        q = fnv_3gram(f"{higher}>{lower}")
        errs = [float(np.linalg.norm(k - q)) for k in self.keys]
        return min(errs) <= 1e-9   # exact-key recall (deterministic keys)

    def answer(self, x, y):
        """return the higher of {x,y}, or None if it must ABSTAIN (unobserved pair)."""
        if self._match(x, y):
            return x
        if self._match(y, x):
            return y
        return None   # ABSTAIN: this exact pair was never presented


# ── ARM B: TRANSITIVE-INFERENCE LANE (integrate premises -> latent rank) ─────
class TransitiveLane:
    """Integrates adjacent ordinal premises into a latent 1-D rank by iterative
    relaxation: each premise higher>lower asserts rank[higher] < rank[lower]; we relax
    until a consistent ordering emerges, then answer ANY pair by comparing ranks.
    ablate=True DISABLES integration -> per-pair lookup (falls back to ItemStore behavior)."""
    def __init__(self, ablate=False):
        self.ablate = ablate
        self.premises = []          # (higher, lower)
        self.items = set()
        self.rank = {}              # item -> latent rank (lower = higher status)
        self._store = ItemStore()   # for the ablated / observed-pair lookup path

    def bind(self, higher, lower):
        self.premises.append((higher, lower))
        self.items.add(higher); self.items.add(lower)
        self._store.bind(higher, lower)

    def integrate(self):
        """relax latent ranks so that for every premise higher>lower: rank[higher] < rank[lower].
        Trabasso-style: initialize all at 0, repeatedly push violating pairs apart until stable."""
        if self.ablate:
            return   # NO integration in the ablate control
        items = list(self.items)
        self.rank = {it: 0.0 for it in items}
        # iterative relaxation (bounded iters; converges for a consistent partial order)
        for _ in range(200):
            moved = False
            for (hi, lo) in self.premises:
                # we want rank[hi] strictly below rank[lo]; if not, push them apart
                if self.rank[hi] >= self.rank[lo]:
                    mid = (self.rank[hi] + self.rank[lo]) / 2.0
                    self.rank[hi] = mid - 0.5
                    self.rank[lo] = mid + 0.5
                    moved = True
            if not moved:
                break

    def answer(self, x, y):
        """which of {x,y} is HIGHER. Abstain if either token is unknown to this episode."""
        if x not in self.items or y not in self.items:
            return None   # NO-FAB: unknown token -> abstain
        if self.ablate:
            # ABLATED: per-pair lookup only (no rank) -> abstain on unobserved pairs
            return self._store.answer(x, y)
        # higher status = LOWER latent rank value
        if self.rank[x] < self.rank[y]:
            return x
        if self.rank[y] < self.rank[x]:
            return y
        return None   # tie (should not happen for a consistent total order)


# ── episode construction ──────────────────────────────────────────────────────
def build_episode(rng):
    """7 opaque tokens with a HIDDEN linear order. Present ONLY the 6 adjacent pairs."""
    tokens = [f"itm{int(rng.integers(100000, 999999))}_{i}" for i in range(N_ITEMS)]
    order = list(tokens)
    rng.shuffle(order)        # hidden ground-truth order: order[0] = highest ... order[-1] = lowest
    adjacent = [(order[i], order[i + 1]) for i in range(N_ITEMS - 1)]  # higher>lower premises
    # queries: all unordered pairs split into observed-adjacent vs unobserved
    observed_set = set()
    for hi, lo in adjacent:
        observed_set.add(frozenset((hi, lo)))
    unobserved = []
    observed = []
    rankpos = {tok: i for i, tok in enumerate(order)}   # 0 = highest
    for i in range(N_ITEMS):
        for j in range(i + 1, N_ITEMS):
            a, b = order[i], order[j]   # a is higher (lower index)
            pair = frozenset((a, b))
            # randomize presentation order of the query pair so neither arm can cheat on position
            qx, qy = (a, b) if rng.random() < 0.5 else (b, a)
            higher_truth = a            # a (lower rankpos) is higher status
            dist = abs(rankpos[a] - rankpos[b])
            rec = (qx, qy, higher_truth, dist)
            if pair in observed_set:
                observed.append(rec)
            else:
                unobserved.append(rec)
    far_token = f"FOIL{int(rng.integers(100000, 999999))}"   # token NOT in the item set
    far_partner = order[int(rng.integers(N_ITEMS))]
    far = (far_token, far_partner) if rng.random() < 0.5 else (far_partner, far_token)
    return order, adjacent, observed, unobserved, far


def build_arm(arm, adjacent, rng):
    if arm == "A":
        fac = ItemStore()
        for hi, lo in adjacent:
            fac.bind(hi, lo)
        return fac
    ablate = (arm == "Babl")
    fac = TransitiveLane(ablate=ablate)
    prem = adjacent
    if arm == "Bshuf":
        # SHUFFLE control: randomly FLIP the direction of each premise before integration
        prem = [(lo, hi) if rng.random() < 0.5 else (hi, lo) for (hi, lo) in adjacent]
    for hi, lo in prem:
        fac.bind(hi, lo)
    fac.integrate()
    return fac


def acc_unobserved(fac, unobserved):
    """unobserved-pair accuracy; ABSTAIN counts as INCORRECT (frozen rule)."""
    if not unobserved:
        return 0.0
    ok = 0
    for qx, qy, higher_truth, _dist in unobserved:
        ans = fac.answer(qx, qy)
        if ans == higher_truth:
            ok += 1
    return ok / len(unobserved)


def acc_observed(fac, observed):
    if not observed:
        return 0.0
    ok = 0
    for qx, qy, higher_truth, _dist in observed:
        ans = fac.answer(qx, qy)
        if ans == higher_truth:
            ok += 1
    return ok / len(observed)


def dist_curve(fac, unobserved):
    """symbolic-distance diagnostic: accuracy bucketed by rank distance (NON-GATING)."""
    buckets = {}
    for qx, qy, higher_truth, dist in unobserved:
        ans = fac.answer(qx, qy)
        buckets.setdefault(dist, [0, 0])
        buckets[dist][1] += 1
        if ans == higher_truth:
            buckets[dist][0] += 1
    return {d: (c[0] / c[1] if c[1] else 0.0) for d, c in sorted(buckets.items())}


ARM_SALT = {"A": 11, "B": 23, "Bshuf": 37, "Babl": 53}   # fixed (deterministic, no PYTHONHASHSEED)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    arms = ["A", "B", "Bshuf", "Babl"]
    unobs = {a: [] for a in arms}
    obs = {a: [] for a in arms}
    abst = {a: [0, 0] for a in arms}     # [abstain_count, total] on far foil
    dist_acc = {}                         # B distance curve accumulator
    for ep in range(N_EP):
        order, adjacent, observed, unobserved, far = build_episode(rng)
        for a in arms:
            arm_rng = np.random.default_rng(seed * 1000 + ep * 7 + ARM_SALT[a])
            fac = build_arm(a, adjacent, arm_rng)
            unobs[a].append(acc_unobserved(fac, unobserved))
            obs[a].append(acc_observed(fac, observed))
            # far-foil abstain
            fx, fy = far
            abst[a][1] += 1
            if fac.answer(fx, fy) is None:
                abst[a][0] += 1
            if a == "B":
                dc = dist_curve(fac, unobserved)
                for d, acc in dc.items():
                    dist_acc.setdefault(d, []).append(acc)
    res = {}
    for a in arms:
        res[a] = dict(
            unobs=float(np.mean(unobs[a])),
            obs=float(np.mean(obs[a])),
            abst=abst[a][0] / max(1, abst[a][1]),
        )
    res["_dist"] = {d: float(np.mean(v)) for d, v in sorted(dist_acc.items())}
    return res


def main():
    print("=" * 78)
    print("H_1429 — TRANSITIVE INFERENCE / serial-order premise-integration (HD34) — R1 numpy MIRROR")
    print("=" * 78)
    per = {}
    for s in SEEDS:
        per[s] = run_seed(s)
        r = per[s]
        print(f"seed {s}: UNOBS A={r['A']['unobs']:.3f} B={r['B']['unobs']:.3f} "
              f"Bshuf={r['Bshuf']['unobs']:.3f} Babl={r['Babl']['unobs']:.3f} | "
              f"OBS A={r['A']['obs']:.3f} B={r['B']['obs']:.3f} | "
              f"B.far-abstain={r['B']['abst']:.3f}")

    def m(arm, key):
        return float(np.mean([per[s][arm][key] for s in SEEDS]))

    Au, Bu, Bsu, Bau = m("A", "unobs"), m("B", "unobs"), m("Bshuf", "unobs"), m("Babl", "unobs")
    Ao, Bo = m("A", "obs"), m("B", "obs")
    Bfar = m("B", "abst")

    print("-" * 78)
    print(f"MEAN UNOBS: A={Au:.3f} B={Bu:.3f} Bshuf={Bsu:.3f} Babl={Bau:.3f}  (chance={CHANCE:.3f})")
    print(f"MEAN OBS  : A={Ao:.3f} B={Bo:.3f}   (both arms recall the trained premises)")
    print(f"B far-foil abstain rate: {Bfar:.3f}")
    # symbolic-distance diagnostic (NON-GATING)
    dist_all = {}
    for s in SEEDS:
        for d, acc in per[s]["_dist"].items():
            dist_all.setdefault(d, []).append(acc)
    dc = {d: float(np.mean(v)) for d, v in sorted(dist_all.items())}
    print(f"B symbolic-distance curve (acc by rank-distance, NON-GATING): "
          + "  ".join(f"d{d}={a:.3f}" for d, a in dc.items()))

    # ── frozen predicate (bars fixed in FREEZE BEFORE this run) ──
    c1_each = all(per[s]["B"]["unobs"] >= CHANCE + 0.30 for s in SEEDS)
    c1 = c1_each and (Bu >= CHANCE + 0.30)
    c2 = (Bu - Au >= 0.30) and (Au <= CHANCE + 0.10)
    c3 = (Bsu - CHANCE) <= 0.10
    c4 = Bau <= Au + 0.10
    c5 = Bfar >= 0.90

    print("-" * 78)
    print("BINDING predicate — transitive inference (lift = the integrated latent rank):")
    print(f"c1 PRESENCE   B-chance>=0.30 (each+mean)  : {c1}   (B={Bu:.3f} chance={CHANCE:.3f}, B-chance={Bu-CHANCE:+.3f})")
    print(f"c2 DISTINCT   B-A>=0.30 & A<=chance+0.10  : {c2}   (B-A={Bu-Au:+.3f}; A={Au:.3f}<=0.60? {Au <= CHANCE + 0.10})")
    print(f"c3 SHUFFLE    Bshuf-chance<=0.10          : {c3}   (Bshuf={Bsu:.3f}, Bshuf-chance={Bsu-CHANCE:+.3f})")
    print(f"c4 ABLATE     Babl<=A+0.10                : {c4}   (Babl={Bau:.3f} <= A+0.10={Au+0.10:.3f})")
    print(f"c5 NO-FAB     B far-abstain>=0.90         : {c5}   (abstain={Bfar:.3f})")
    green = c1 and c2 and c3 and c4 and c5
    print("=" * 78)
    print(f"VERDICT (R1 mirror, DIRECTIONAL): {'GREEN' if green else 'RED / WALL'}")
    print("=" * 78)


if __name__ == "__main__":
    main()
