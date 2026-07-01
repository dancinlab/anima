"""
H_1430 — CONCEPT / CATEGORY PROTOTYPE-ABSTRACTION (HD33). R1/R1b numpy MIRROR (DIRECTIONAL).

Frozen designs:
  R1  : .verdicts/1430_concept_prototype_abstraction/H_1430_FREEZE.txt
  R1b : .verdicts/1430_concept_prototype_abstraction/H_1430_R1b_FREEZE.txt
        (a_break_the_wall type-(a): R1 lived in a DEGENERATE high-separation/low-noise
        slice where EVERY arm saturated to 1.000 so the prototype-vs-exemplar
        dissociation was unobservable. R1b re-scales the EPISODE GEOMETRY ONLY into the
        Posner-Keele high-distortion band — the 5 bars are byte-identical, NO bar moved,
        NOT tune-to-green; the regime simply now permits the effect to exist.)

Pass --regime r1 or --regime r1b (default r1b). $0 CPU numpy, gradient-free, 3 seeds
[4430,4431,4432], p7. a_no_llm_frame_trap (Rosch; Posner-Keele dot-pattern; c15) — NOT an
LLM recipe. ENGINE-TRANSFER UNVERIFIED until R2.

THE NEW STRUCTURE = a CONCEPT / CATEGORY PROTOTYPE: from noisy training INSTANCES the
faculty abstracts a per-category CENTROID and classifies NOVEL never-seen instances,
including the never-shown prototype itself (often classified BETTER than trained exemplars
— the Posner-Keele enhancement effect). DISTINCT from ImmuneMemory item-binding (memorizes
specific instances, abstains/misses on a novel instance, CANNOT show prototype-enhancement)
and from SpatialMap (metric positions of specific landmarks, not a learned class boundary
over a feature distribution).

FALSIFIER (identical both regimes):
  (c1)  novel-instance classification B - chance >= 0.30 (each seed + mean).
  (c2)  exemplar/item-store on novel B - A >= 0.10 AND A shows NO prototype-enhancement.
  (c2b) the never-shown prototype is classified by B >= B's trained-instance accuracy.
  (c3)  shuffle instance->category -> Bshuf collapses to chance.
  (c4)  ablate centroid (nearest-exemplar mode) -> enhancement disappears + novel-acc drops.
  (c5)  far foil -> B abstains (>= 0.90).
GREEN iff c1 ∧ c2 ∧ c2b ∧ c3 ∧ c4 ∧ c5; any fail w/ clean control collapse = honest 🧱.
"""
import sys
import numpy as np

# ── frozen constants ─────────────────────────────────────────────────────────
K_CAT   = 4
DIM     = 24
N_TRAIN = 8
N_TEST  = 8
CHANCE  = 1.0 / K_CAT
SEEDS   = [4430, 4431, 4432]

REGIMES = {
    # R1 (original frozen): high separation (floor), low noise -> degenerate (all arms saturate)
    "r1":  dict(NOISE_TRAIN=1.0, NOISE_TEST=1.0, PROTO_SEP=6.0, FOIL_MIN=12.0, ABSTAIN_D=9.0,
                CONTROLLED_SEP=False, GEOM="axis"),
    # R1b (1st re-freeze): axis-controlled separation, over-tight abstain band -> all abstain
    "r1b": dict(NOISE_TRAIN=3.0, NOISE_TEST=4.0, PROTO_SEP=6.0, FOIL_MIN=14.0, ABSTAIN_D=10.0,
                CONTROLLED_SEP=True, GEOM="axis"),
    # R1c (FINAL frozen): multi-dim sphere prototypes + principled high-distortion band
    "r1c": dict(NOISE_TRAIN=2.5, NOISE_TEST=2.5, PROTO_SEP=6.0, FOIL_MIN=13.0, ABSTAIN_D=13.0,
                CONTROLLED_SEP=True, GEOM="sphere"),
}


# ── faculties ────────────────────────────────────────────────────────────────
class ExemplarStore:
    """Faithful ImmuneMemory item-binding stand-in: MEMORIZES each trained instance
    -> category INDEPENDENTLY; classifies a test vector by its NEAREST TRAINED
    instance (1-NN exemplar). Abstracts NO category centroid."""
    def __init__(self, abstain_d):
        self.items = []
        self.abstain_d = abstain_d

    def observe(self, vec, cat):
        self.items.append((np.asarray(vec, dtype=np.float64), int(cat)))

    def classify(self, vec):
        v = np.asarray(vec, dtype=np.float64)
        best, bestd = -1, 1e18
        for iv, ic in self.items:
            d = float(np.linalg.norm(v - iv))
            if d < bestd:
                bestd, best = d, ic
        if bestd > self.abstain_d:
            return -1
        return best


class PrototypeLane:
    """Running per-category CENTROID (mean of observed instances); classifies by nearest
    centroid. The abstraction. `ablate` -> nearest-exemplar mode (collapses to exemplar
    store, the c4 control)."""
    def __init__(self, k, dim, abstain_d, ablate=False):
        self.k = k
        self.dim = dim
        self.abstain_d = abstain_d
        self.ablate = ablate
        self.sum = np.zeros((k, dim))
        self.cnt = np.zeros(k)
        self.items = []

    def observe(self, vec, cat):
        v = np.asarray(vec, dtype=np.float64)
        c = int(cat)
        self.sum[c] += v
        self.cnt[c] += 1
        self.items.append((v, c))

    def _centroid(self, c):
        if self.cnt[c] == 0:
            return None
        return self.sum[c] / self.cnt[c]

    def classify(self, vec):
        v = np.asarray(vec, dtype=np.float64)
        if self.ablate:
            best, bestd = -1, 1e18
            for iv, ic in self.items:
                d = float(np.linalg.norm(v - iv))
                if d < bestd:
                    bestd, best = d, ic
            if bestd > self.abstain_d:
                return -1
            return best
        best, bestd = -1, 1e18
        for c in range(self.k):
            cen = self._centroid(c)
            if cen is None:
                continue
            d = float(np.linalg.norm(v - cen))
            if d < bestd:
                bestd, best = d, c
        if bestd > self.abstain_d:
            return -1
        return best


# ── episode construction ──────────────────────────────────────────────────────
def make_prototypes(rng, cfg):
    """K prototype vectors. R1b: EXACT pairwise PROTO_SEP via an orthogonal-axis frame
    (each proto on its own axis at PROTO_SEP/sqrt(2) so pairwise L2 == PROTO_SEP exactly).
    R1: legacy uniform-draw with a >= PROTO_SEP floor (the degenerate slice)."""
    sep = cfg["PROTO_SEP"]
    geom = cfg.get("GEOM", "axis")
    if geom == "sphere":
        # R1c: random MULTI-DIM direction scaled to radius=sep (Posner-Keele dot-pattern:
        # a pattern that varies across ALL features). pairwise L2 ~ sep*sqrt(2).
        protos = []
        for c in range(K_CAT):
            g = rng.standard_normal(DIM)
            protos.append(g / np.linalg.norm(g) * sep)
        return [np.asarray(p, dtype=np.float64) for p in protos]
    if cfg["CONTROLLED_SEP"]:
        # place on distinct axes: proto c = e_c * a, pairwise L2 = a*sqrt(2) = sep
        a = sep / np.sqrt(2.0)
        protos = []
        for c in range(K_CAT):
            v = np.zeros(DIM)
            v[c] = a
            protos.append(v)
        # random rigid offset/rotation-free shift so it is not axis-trivial across seeds
        shift = rng.uniform(-2.0, 2.0, size=DIM)
        return [np.asarray(p + shift, dtype=np.float64) for p in protos]
    # R1 legacy
    protos, tries = [], 0
    while len(protos) < K_CAT and tries < 10000:
        tries += 1
        cand = rng.uniform(-5.0, 5.0, size=DIM)
        if all(float(np.linalg.norm(cand - p)) >= sep for p in protos):
            protos.append(cand)
    if len(protos) < K_CAT:
        protos = []
        for c in range(K_CAT):
            v = np.zeros(DIM)
            v[c % DIM] = sep * 1.5 * (1 + c)
            protos.append(v)
    return [np.asarray(p, dtype=np.float64) for p in protos]


def make_far_foil(rng, protos, cfg):
    fmin = cfg["FOIL_MIN"]
    for _ in range(20000):
        cand = rng.uniform(-30.0, 30.0, size=DIM)
        if all(float(np.linalg.norm(cand - p)) >= fmin for p in protos):
            return cand
    return protos[0] + fmin * 2.0 * np.ones(DIM) / np.sqrt(DIM)


def build_episode(rng, cfg):
    protos = make_prototypes(rng, cfg)
    train = []
    for c in range(K_CAT):
        for _ in range(N_TRAIN):
            v = protos[c] + rng.standard_normal(DIM) * cfg["NOISE_TRAIN"]
            train.append((v, c))
    test_novel = []
    for c in range(K_CAT):
        for _ in range(N_TEST):
            v = protos[c] + rng.standard_normal(DIM) * cfg["NOISE_TEST"]
            test_novel.append((v, c))
    far = make_far_foil(rng, protos, cfg)
    return protos, train, test_novel, far


# ── arms ──────────────────────────────────────────────────────────────────────
def build_faculty(arm, train, rng, cfg):
    if arm == "A":
        fac = ExemplarStore(cfg["ABSTAIN_D"])
        for v, c in train:
            fac.observe(v, c)
    else:
        ablate = (arm == "Babl")
        fac = PrototypeLane(K_CAT, DIM, cfg["ABSTAIN_D"], ablate=ablate)
        order = train
        if arm == "Bshuf":
            cats = [c for _, c in train]
            perm = list(range(len(cats)))
            rng.shuffle(perm)
            order = [(train[i][0], cats[perm[i]]) for i in range(len(train))]
        for v, c in order:
            fac.observe(v, c)
    return fac


def acc_over(fac, items):
    ok = 0
    for v, c in items:
        if fac.classify(v) == c:
            ok += 1
    return ok / len(items)


def run_seed(seed, cfg):
    rng = np.random.default_rng(seed)
    protos, train, test_novel, far = build_episode(rng, cfg)
    proto_items = [(protos[c], c) for c in range(K_CAT)]
    out = {}
    for arm in ["A", "B", "Bshuf", "Babl"]:
        arm_rng = np.random.default_rng(seed * 1000 + (hash(arm) % 97))
        fac = build_faculty(arm, train, arm_rng, cfg)
        out[arm] = dict(
            novel=acc_over(fac, test_novel),
            proto=acc_over(fac, proto_items),
            train=acc_over(fac, train),
            abst=(1 if fac.classify(far) == -1 else 0),
        )
    return out


def main():
    regime = "r1c"
    if "--regime" in sys.argv:
        regime = sys.argv[sys.argv.index("--regime") + 1].lower()
    cfg = REGIMES[regime]

    print("=" * 78)
    print(f"H_1430 — CONCEPT / CATEGORY PROTOTYPE-ABSTRACTION (HD33) — R1 numpy MIRROR [{regime}]")
    print("=" * 78)
    per = {}
    for s in SEEDS:
        per[s] = run_seed(s, cfg)
        r = per[s]
        print(f"seed {s}: NOVEL A={r['A']['novel']:.3f} B={r['B']['novel']:.3f} "
              f"Bshuf={r['Bshuf']['novel']:.3f} Babl={r['Babl']['novel']:.3f} | "
              f"PROTO A={r['A']['proto']:.3f} B={r['B']['proto']:.3f} "
              f"Babl={r['Babl']['proto']:.3f} | "
              f"TRAIN A={r['A']['train']:.3f} B={r['B']['train']:.3f} "
              f"Babl={r['Babl']['train']:.3f}")

    def m(arm, key):
        return float(np.mean([per[s][arm][key] for s in SEEDS]))

    An, Bn, Bsn, Ban = m("A", "novel"), m("B", "novel"), m("Bshuf", "novel"), m("Babl", "novel")
    Ap, Bp, Bap = m("A", "proto"), m("B", "proto"), m("Babl", "proto")
    At, Bt, Bat = m("A", "train"), m("B", "train"), m("Babl", "train")
    B_abst = m("B", "abst")

    print("-" * 78)
    print(f"MEAN NOVEL: A={An:.3f} B={Bn:.3f} Bshuf={Bsn:.3f} Babl={Ban:.3f}  (chance={CHANCE:.3f})")
    print(f"MEAN PROTO: A={Ap:.3f} B={Bp:.3f} Babl={Bap:.3f}")
    print(f"MEAN TRAIN: A={At:.3f} B={Bt:.3f} Babl={Bat:.3f}")
    print(f"B far-foil abstain rate: {B_abst:.3f}")

    c1_each = all(per[s]["B"]["novel"] >= CHANCE + 0.30 for s in SEEDS)
    c1 = c1_each and (Bn >= CHANCE + 0.30)
    A_no_enh = Ap < At
    c2 = (Bn - An >= 0.10) and A_no_enh
    c2b = Bp >= Bt
    c3 = Bsn - CHANCE <= 0.10
    Babl_no_enh = Bap < Bat
    c4 = Babl_no_enh and (Ban <= Bn - 0.05)
    c5 = B_abst >= 0.90

    print("-" * 78)
    print("BINDING predicate — prototype abstraction (lift = the abstracted centroid):")
    print(f"c1 PRESENCE      B-chance>=0.30 (each+mean): {c1}   (B={Bn:.3f} chance={CHANCE:.3f})")
    print(f"c2 DISTINCT      B-A>=0.10 & A no-enhance  : {c2}   "
          f"(B-A={Bn-An:+.3f}; A_proto={Ap:.3f}<A_train={At:.3f}? {A_no_enh})")
    print(f"c2b PROTO-EFFECT B_proto>=B_train          : {c2b}  "
          f"(B_proto={Bp:.3f} >= B_train={Bt:.3f})")
    print(f"c3 EARNED-CAT    Bshuf-chance<=0.10        : {c3}   (Bshuf={Bsn:.3f})")
    print(f"c4 EARNED-ABSTR  ablate no-enhance & drop  : {c4}   "
          f"(Babl_proto={Bap:.3f}<Babl_train={Bat:.3f}? {Babl_no_enh}; "
          f"Babl_novel={Ban:.3f}<=B-0.05={Bn-0.05:.3f}? {Ban <= Bn-0.05})")
    print(f"c5 NO-FAB        far-abstain>=0.90         : {c5}   (abstain={B_abst:.3f})")
    green = c1 and c2 and c2b and c3 and c4 and c5
    print("=" * 78)
    print(f"VERDICT (R1 mirror, DIRECTIONAL): {'GREEN' if green else 'RED / WALL'}")
    print("=" * 78)


if __name__ == "__main__":
    main()
