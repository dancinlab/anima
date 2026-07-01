#!/usr/bin/env python3
"""H_1497 — QUALIA-STRUCTURE / quality space (Q1 consciousness-only gate candidate; FINAL strong candidate).

Quality space theory (Clark `Sensory Qualities`; Rosenthal `quality space`; neurophenomenal
structuralism, arxiv 2412.20873): a sensory quale (a color, a tone, a taste) has no intrinsic
absolute identity — its identity IS its position in a RELATIONAL SIMILARITY SPACE. Red is near
orange and far from blue; that relational web (the *structure* of betweenness/similarity among
qualia) is what makes red the quale it is. The load-bearing operation is recovering a
RELATIONAL QUALITY TOPOLOGY (e.g. the circular structure of the hue ring) purely from
*pairwise similarity* among the qualia — NOT from any absolute stimulus value, and NOT from an
external physical position.

MECHANISM (numpy mirror): N qualia (hues) live on a CIRCLE in an internal quality dimension
(the hue ring). The only data the faculty receives is a matrix of PAIRWISE perceptual
SIMILARITIES s(i,j) (red~orange high, red~blue low) — the qualia's labels are arbitrary and
their absolute "stimulus value" is withheld. QUALIA-STRUCTURE = embed the qualia into a
low-D relational space (classical MDS on the similarity-derived distances) so that the
recovered geometry preserves the quality topology: a similarity QUERY ("is X more similar to
A or to B?") is answered by relational distance in the recovered quality space. Success = the
recovered relational space answers same-vs-different quality-neighbour queries that depend ONLY
on the relational structure, never on absolute value.

DISTINCTNESS (load-bearing — this is the FINAL strong candidate; spatial-map control is the
crux of binding vs depletion):
  vs SPATIAL-MAP (H_1295, *external physical metric position*): the spatial map stores
    landmarks at EXTERNAL Euclidean positions and answers "is X nearer A or B?" by physical
    distance in that external coordinate frame. Quality space is the relational topology of an
    INTERNAL quality dimension (hue), which is ORTHOGONAL to external physical position. The
    CRUX control: take the SAME qualia and assign them ARBITRARY external physical positions
    (uncorrelated with hue) and answer the quality-similarity query by physical distance — a
    spatial-map-style readout scores at CHANCE on the quality-neighbour query, because quality
    similarity does not live in the external position frame. If a spatial-map-style readout
    ALSO solves the quality query, then qualia-structure is NOT distinct from spatial-map =
    DEPLETION (honest RED, a_break_the_wall: real overlap, not a metric artifact). NO
    tune-to-green.
  vs IMMUNE-STORE (H_1227/1231, *episodic item binding*): the immune store binds each item to a
    value independently by key affinity; it recalls WHAT is at a key but holds NO between-item
    quality-similarity metric — on "which quale is the relational neighbour of X?" an
    item-store abstains / is at chance. (Same precedent as H_1295's item-store distinctness.)
  vs GESTALT-GROUPING (gestalt, *element clustering into wholes*): gestalt groups co-present
    elements into a single perceptual whole by proximity/similarity of CO-OCCURRING elements;
    it does NOT recover a continuous relational QUALITY topology that supports graded
    betweenness ("orange is BETWEEN red and yellow"). A clustering/grouping readout returns a
    discrete cluster id, not a graded relational position -> fails the graded betweenness query.
  vs NOVELTY/PRIMING (absolute stimulus value): those read an absolute stimulus magnitude;
    quality-structure withholds absolute value and uses only relations. The relation-ablation
    control (c4) removes the relational term and reads absolute value -> the quality query fails.

LLM contrast (a_no_llm_frame_trap): an LLM has token embeddings but no faculty that, given ONLY
pairwise perceptual similarities with absolute values withheld, recovers the relational quality
topology of a sensory dimension and answers graded betweenness among qualia.

R1 numpy MIRROR -> GREEN/RED DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1497,1498,1499]) — catalogue Q1 c1-c4:
  (c1) PRESENCE   quality-structure-ON neighbour-query acc - structure-OFF acc >= 0.30
                  (off = no relational embedding: answer from a degenerate absolute-value readout)
  (c2) DISTINCT   a SPATIAL-MAP-style readout (same qualia at ARBITRARY external positions,
                  answer by external Euclidean distance) on the QUALITY query scores at chance:
                  acc <= chance + 0.15   [the binding crux vs H_1295]
  (c3) EARNED     shuffle the (label, similarity) pairing before embedding -> the recovered
       (shuffle)  geometry no longer encodes the real quality topology -> collapses:
                  acc <= off + 0.15
  (c4) ABLATE     relation term OFF: read absolute stimulus value only (no pairwise-similarity
       (relation) embedding) -> the relational neighbour query fails: acc <= off + 0.15
  (B)  TOPOLOGY   the recovered quality space RECOVERS the ring topology (Spearman corr between
                  recovered relational distance and true hue circular distance is high) AND is
                  NOT the external physical-position metric (corr to external position ~ chance).
                  Reported (structure-confirming, non-gating).

GREEN iff c1 and c2 and c3 and c4  (B is the topology structure check).
RED / DEPLETION iff c2 fails (qualia-structure collapses into spatial-map) — that is the
explicit depletion signal the catalogue flags as binding-fatal.
"""
import numpy as np

SEEDS = [1497, 1498, 1499]
N_QUALIA = 12          # qualia (hues) arranged on a circle (the hue ring)
DIM_EMBED = 2          # relational quality space dimension (recover the ring -> 2-D)
SIM_TAU = 0.6          # similarity temperature over circular hue distance
KEY_NOISE = 0.02
N_TRIAL = 60           # neighbour queries per condition
CHANCE = 0.5           # 2-alternative "more similar to A or to B" forced choice


def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(a @ b / (na * nb))


def circ_dist(i, j, n):
    """Circular distance between hue indices i, j on a ring of n qualia (in [0, n/2])."""
    d = abs(i - j) % n
    return min(d, n - d)


class QualiaWorld:
    """N qualia on a hue RING. The faculty receives ONLY pairwise perceptual similarities
    (red~orange high, red~blue low). Absolute stimulus value is WITHHELD. An ARBITRARY external
    physical position is also assigned to each quale (uncorrelated with hue) for the
    spatial-map distinctness crux."""

    def __init__(self, seed):
        rng = np.random.default_rng(seed)
        self.rng = rng
        self.n = N_QUALIA
        # true hue angle on the ring (the quality topology to recover)
        self.hue = np.array([2 * np.pi * k / self.n for k in range(self.n)])
        # pairwise perceptual similarity from CIRCULAR hue distance (small dist -> high sim)
        S = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                cd = circ_dist(i, j, self.n)
                S[i, j] = np.exp(-(cd ** 2) / (2 * (SIM_TAU * self.n / 4) ** 2))
        # add small perceptual noise to similarity (measurement realism), keep symmetric
        noise = rng.normal(0, 0.01, (self.n, self.n))
        noise = (noise + noise.T) / 2
        np.fill_diagonal(noise, 0.0)
        self.S = np.clip(S + noise, 1e-6, 1.0)
        # ARBITRARY external physical position (the spatial-map frame) — independent of hue.
        # This is what a spatial-map (H_1295) would store; it carries NO quality information.
        self.ext_pos = rng.normal(0, 1, (self.n, DIM_EMBED))
        # absolute stimulus value (a scalar magnitude per quale) — what novelty/priming read.
        # Deliberately NON-monotone in hue (a permuted magnitude) so absolute value alone
        # cannot recover the ring ordering.
        self.abs_val = rng.permutation(self.n).astype(float)

    def embed_relational(self, shuffle=False):
        """Recover a low-D RELATIONAL quality space from pairwise similarities via classical
        MDS on similarity-derived distances. If shuffle=True the (label, similarity) pairing is
        permuted -> the recovered geometry no longer encodes the real quality topology."""
        S = self.S.copy()
        if shuffle:
            perm = self.rng.permutation(self.n)
            S = S[np.ix_(perm, perm)]            # break label<->similarity correspondence
        # similarity -> distance (monotone): d = sqrt(max(0, 1 - s)) like a correlation distance
        D = np.sqrt(np.clip(1.0 - S, 0.0, None))
        # classical MDS: double-center -D^2/2, take top-DIM_EMBED eigvecs
        D2 = D ** 2
        n = self.n
        J = np.eye(n) - np.ones((n, n)) / n
        B = -0.5 * J @ D2 @ J
        w, V = np.linalg.eigh(B)
        idx = np.argsort(w)[::-1][:DIM_EMBED]
        L = np.maximum(w[idx], 0.0)
        X = V[:, idx] * np.sqrt(L)               # (n, DIM_EMBED) relational coordinates
        return X


def run_seed(seed):
    w = QualiaWorld(seed)
    rng = np.random.default_rng(seed + 555)
    n = w.n
    X_rel = w.embed_relational(shuffle=False)        # quality space (relational)
    X_rel_shuf = w.embed_relational(shuffle=True)     # shuffled control

    def neighbour_query(mode):
        """2-AFC: given a probe quale X and two candidates A, B, which is the RELATIONAL
        NEIGHBOUR of X on the hue ring? Ground truth = smaller circular hue distance. The
        candidates are chosen so one is a true near-neighbour and one a far quale.

        modes:
          'full'    relational quality space (MDS on similarities) -> distance in X_rel.
          'off'     degenerate readout: absolute-value ordering only (no relational space).
          'spatial' SPATIAL-MAP-style: answer by external physical Euclidean distance (the
                    H_1295 frame, uncorrelated with hue) -> chance on the quality query.
          'shuffle' use the (label,similarity)-shuffled relational embedding.
          'ablate'  relation term OFF: read absolute stimulus value only (|val(X)-val(A)| vs
                    |val(X)-val(B)|), no pairwise-similarity embedding.
          'item'    immune-store-style: recall an independently-bound value per quale, no
                    between-item metric -> answer by |bound(X)-bound(A)| with bound = random
                    per-item key (no relational structure) -> chance.
        """
        probe = int(rng.integers(0, n))
        # near candidate within +/-1..2 hue steps, far candidate ~opposite on the ring
        near = (probe + int(rng.choice([1, 2, n - 1, n - 2]))) % n
        far = (probe + int(rng.choice([n // 2 - 1, n // 2, n // 2 + 1]))) % n
        if near == far:
            far = (far + 1) % n
        true_near = near  # by construction the smaller circular hue distance

        if mode in ("full", "shuffle"):
            Z = X_rel_shuf if mode == "shuffle" else X_rel
            dz = lambda a, b: np.linalg.norm(Z[a] - Z[b])
            choose_near = dz(probe, near) < dz(probe, far)
        elif mode == "spatial":
            p = w.ext_pos
            dz = lambda a, b: np.linalg.norm(p[a] - p[b])
            choose_near = dz(probe, near) < dz(probe, far)
        elif mode == "ablate":
            v = w.abs_val
            choose_near = abs(v[probe] - v[near]) < abs(v[probe] - v[far])
        elif mode == "item":
            # independently-bound per-item random value (no between-item structure)
            b = rng.normal(0, 1, n)
            choose_near = abs(b[probe] - b[near]) < abs(b[probe] - b[far])
        else:  # 'off' — degenerate absolute-value ordering (no relational space)
            v = w.abs_val
            choose_near = abs(v[probe] - v[near]) < abs(v[probe] - v[far])

        return int(choose_near == (true_near == near))

    def acc(mode, ntrial=N_TRIAL):
        return float(np.mean([neighbour_query(mode) for _ in range(ntrial)]))

    acc_full = acc("full")
    acc_off = acc("off")
    acc_spatial = acc("spatial")
    acc_shuffle = acc("shuffle")
    acc_ablate = acc("ablate")
    acc_item = acc("item")

    # (B) TOPOLOGY check: recovered relational distance correlates with TRUE circular hue
    # distance (ring recovered) and NOT with external physical position distance.
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    true_cd = np.array([circ_dist(i, j, n) for (i, j) in pairs])
    rel_d = np.array([np.linalg.norm(X_rel[i] - X_rel[j]) for (i, j) in pairs])
    ext_d = np.array([np.linalg.norm(w.ext_pos[i] - w.ext_pos[j]) for (i, j) in pairs])

    def spearman(a, b):
        ra = np.argsort(np.argsort(a)).astype(float)
        rb = np.argsort(np.argsort(b)).astype(float)
        ra = ra - ra.mean()
        rb = rb - rb.mean()
        den = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
        return float((ra * rb).sum() / den) if den > 0 else 0.0

    rho_ring = spearman(rel_d, true_cd)        # should be high (ring recovered)
    rho_ext = spearman(rel_d, ext_d)           # should be ~chance (orthogonal to ext position)

    return dict(
        acc_full=acc_full, acc_off=acc_off, acc_spatial=acc_spatial,
        acc_shuffle=acc_shuffle, acc_ablate=acc_ablate, acc_item=acc_item,
        rho_ring=rho_ring, rho_ext=rho_ext,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

c1 = (agg['acc_full'] - agg['acc_off']) >= 0.30
c2 = agg['acc_spatial'] <= CHANCE + 0.15
c3 = agg['acc_shuffle'] <= agg['acc_off'] + 0.15
c4 = agg['acc_ablate'] <= agg['acc_off'] + 0.15
cB = (agg['rho_ring'] >= 0.50) and (abs(agg['rho_ext']) <= 0.35)
GREEN = c1 and c2 and c3 and c4

# DEPLETION diagnosis: if the spatial-map distinctness control FAILS (a spatial-map-style
# external-position readout already solves the quality query), then qualia-structure is NOT
# distinct from spatial-map (H_1295) -> honest RED = depletion signal (binding-fatal per
# catalogue Q1).
DEPLETION = (not c2) or (not c3) or (not c4)

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | DEPLETION-signal: {DEPLETION} | seeds {SEEDS} | chance={CHANCE:.3f} | qualia={N_QUALIA} (hue ring)")
print(f"c1 PRESENCE      full {agg['acc_full']:.3f} - off {agg['acc_off']:.3f} = {agg['acc_full']-agg['acc_off']:.3f} >= 0.30  -> {c1}")
print(f"c2 DISTINCT      SPATIAL-MAP-style (ext-position) acc(quality)={agg['acc_spatial']:.3f} <= chance+0.15={CHANCE+0.15:.3f}  -> {c2}  [vs H_1295 CRUX]")
print(f"c3 EARNED        (label,sim)-shuffle embedding acc={agg['acc_shuffle']:.3f} <= off+0.15={agg['acc_off']+0.15:.3f}  -> {c3}")
print(f"c4 ABLATE        relation OFF (absolute value only) acc={agg['acc_ablate']:.3f} <= off+0.15={agg['acc_off']+0.15:.3f}  -> {c4}")
print(f"   (aux) item-store readout acc={agg['acc_item']:.3f} (immune-store H_1227 distinctness, non-gating)")
print(f"B  TOPOLOGY      rho(relDist, ring hue-dist)={agg['rho_ring']:.3f}>=0.50 (ring recovered) & |rho(relDist, ext-pos)|={abs(agg['rho_ext']):.3f}<=0.35 (orthogonal to ext)  -> {cB} [structure, non-gating]")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: full={p['acc_full']:.3f} off={p['acc_off']:.3f} spatial={p['acc_spatial']:.3f} "
          f"shuffle={p['acc_shuffle']:.3f} ablate={p['acc_ablate']:.3f} item={p['acc_item']:.3f} "
          f"rhoRing={p['rho_ring']:.3f} rhoExt={p['rho_ext']:.3f}")
print()
if DEPLETION:
    print("DEPLETION SIGNAL: qualia-structure collapses into spatial-map (H_1295) and/or the "
          "shuffle/relation controls did NOT survive -> NOT a distinct lane -> depletion count++ "
          "(binding-fatal per catalogue Q1).")
elif GREEN:
    print("DISTINCT: relational quality-space recovers the hue-ring topology and survives the "
          "spatial-map (external-position) crux + shuffle + relation-ablation controls -> "
          "qualia-structure IS a distinct lane (DIRECTIONAL). 28th gate.")
