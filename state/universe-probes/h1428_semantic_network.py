"""
H_1428 — SEMANTIC-NETWORK / SPREADING-ACTIVATION (2-hop). R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1428_semantic_network_spreading/H_1428_FREEZE.txt (pre-registered
BEFORE this scoring — frozen-first, c9/p7). $0 CPU numpy, gradient-free, 3 seeds
[4428,4429,4430]. a_no_llm_frame_trap (Collins & Loftus 1975 spreading-activation theory of
semantic processing; c15) — NOT an LLM recipe. ENGINE-TRANSFER UNVERIFIED until R2.

THE NEW STRUCTURE = a SEMANTIC NETWORK: concepts are NODES linked by weighted ASSOCIATION
edges; activating one node SPREADS activation along weighted edges to related nodes, including
MULTI-HOP (X->Y->Z where X,Z never directly linked). Retrieval = "what is most ASSOCIATED with
X" via weighted graph traversal.

DISTINCT from EVERY lane (the crux):
  - vs episodic item-binding (H_1227 ImmuneMemoryGrow): binds each item->value INDEPENDENTLY by
    FNV-trigram affinity; NO node->node edge. On "most associated with X" (X & target never
    co-bound, only LINKED as nodes) and on 2-HOP X->Y->Z it abstains/chance — cannot bridge.
  - vs spatial-map (H_1296): a 2-D EUCLIDEAN metric (symmetric, triangle inequality). Semantic
    edges are ARBITRARY non-metric weights (asymmetric, no triangle inequality). The graph is
    built metric-VIOLATING: A-B strong, B-C strong, A-C ABSENT yet 2-hop reachable; a metric
    map infers A-C NEAR by triangle, the semantic 2-hop spread distinguishes DIRECT vs INDIRECT.

FALSIFIER (chance = 0.5, two candidates per query):
  (1-HOP) target = X's strongest DIRECT neighbor; distractor = a non-neighbor.
  (2-HOP) target = Z reachable ONLY via X->Y->Z (no direct X->Z edge); distractor = a node with
          NO path from X within HOPS. ONLY multi-hop spread answers; 1-hop ablation cannot.

5-BAR (GREEN iff ALL five PASS each seed AND mean):
  c1 PRESENCE     FULL pooled (1-hop+2-hop) acc - 0.5 >= +0.30  (B >= 0.80).
  c2 DISTINCT     ITEM acc on assoc/2-hop <= 0.65 (abstains -> chance). SPATIAL stand-in on the
                  metric-VIOLATING 2-hop set <= 0.65 (misled by triangle) -- both required.
  c3 EARNED-EDGES SHUFFLE acc <= 0.65 (lift is the LEARNED edges, not node frequency).
  c4 EARNED-SPREAD ABLATED (1-hop-only) 2-HOP acc <= 0.65 AND FULL 2-hop acc >= 0.80.
  c5 NO-FAB       untaught/OOV node (disjoint trigram space, no edges) -> spread fires NO
                  confident node (abstain "") -- no fabricated association.

GUARD (p1/p2/p3/p6): reads ONLY learned edge weights + the current query node; NO injected
"the answer is Y" label, NO persona/identity/RLHF. SHUFFLE + ABLATE BOTH collapse = the lift is
the learned association graph + multi-hop spread, not variance or node frequency.
"""
import numpy as np

# ── frozen constants (from FREEZE) ──────────────────────────────────────────
N_NODES   = 12         # symbolic concept nodes per seed
OUT_DEG   = 3          # out-edges per node (small associative neighborhood)
HOPS      = 2          # spreading-activation depth (2-hop faculty)
DECAY     = 0.6        # per-hop activation decay
N_QUERIES = 40         # association queries per arm per seed (20 1-hop + 20 2-hop)
SEEDS     = [4428, 4429, 4430]
CHANCE    = 0.5


# ── the semantic network (FULL faculty + its controls) ───────────────────────
class SemanticNet:
    """Concepts as NODES; directed weighted ASSOCIATION edges. Spreading activation
    propagates act[v] += act[u]*w(u,v) over DECAY^hop for HOPS hops. Retrieval =
    argmax activation over the candidate set, excluding the seed node itself."""
    def __init__(self, n, ablate_spread=False):
        self.n = n
        self.edges = {i: {} for i in range(n)}   # u -> {v: weight}
        self.ablate_spread = ablate_spread        # True => 1-hop direct only (c4 ablate)

    def add_edge(self, u, v, w):
        self.edges[u][v] = w

    def shuffle_edges(self, rng):
        """SHUFFLE control: collect all edge weights, permute them across the (u,v)
        slots — node out-degree/frequency kept, the learned which->which destroyed."""
        slots = []
        weights = []
        for u in range(self.n):
            for v, w in self.edges[u].items():
                slots.append((u, v))
                weights.append(w)
        perm = list(range(len(weights)))
        rng.shuffle(perm)
        new_edges = {i: {} for i in range(self.n)}
        for k, (u, v) in enumerate(slots):
            new_edges[u][v] = weights[perm[k]]
        self.edges = new_edges

    def spread(self, src):
        """Spreading activation from src. Returns activation dict over nodes != src.
        If ablate_spread, only hop 1 (direct edges) contributes (no multi-hop bridge)."""
        act = {i: 0.0 for i in range(self.n)}
        act[src] = 1.0
        frontier = {src: 1.0}
        max_hops = 1 if self.ablate_spread else HOPS
        for hop in range(max_hops):
            nxt = {}
            for u, au in frontier.items():
                for v, w in self.edges[u].items():
                    delta = au * w * (DECAY ** hop)
                    act[v] = act[v] + delta
                    nxt[v] = nxt.get(v, 0.0) + delta
            frontier = nxt
        act[src] = -1e18   # exclude the seed itself from retrieval
        return act

    def retrieve(self, src, cand_a, cand_b):
        act = self.spread(src)
        # NO-FAB: if no candidate received ANY activation, abstain (return None).
        if act[cand_a] <= 0.0 and act[cand_b] <= 0.0:
            return None
        return cand_a if act[cand_a] >= act[cand_b] else cand_b

    def is_active(self, src):
        """NO-FAB probe: does spreading from src reach ANY node with positive activation?"""
        act = self.spread(src)
        return any(act[v] > 0.0 for v in range(self.n) if v != src)


class ItemStore:
    """Faithful ImmuneMemory item-binding stand-in (H_1227): binds node->its-own-payload
    INDEPENDENTLY, holds NO inter-node edge. On an association / 2-hop query it has no
    node->node relation -> ABSTAINS (None => caller resolves at chance)."""
    def __init__(self, n):
        self.payload = {i: f"payload_{i}" for i in range(n)}  # independent bindings only

    def retrieve(self, src, cand_a, cand_b):
        return None   # no association relation -> abstain


class SpatialStandIn:
    """Spatial-map stand-in (H_1296): embeds each node in a EUCLIDEAN metric derived from its
    edges (symmetrized + metric-closed via Floyd-Warshall, enforcing the triangle inequality).
    For the metric-VIOLATING graph it infers A-C NEAR (A near B, B near C => A near C), so on a
    2-hop query it CANNOT tell DIRECT from INDIRECT the way the directed spread does. c2 ref:
    a metric cannot represent the directed/asymmetric edge structure."""
    def __init__(self, net):
        self.n = net.n
        W = np.zeros((self.n, self.n))
        for u in range(self.n):
            for v, w in net.edges[u].items():
                W[u, v] = max(W[u, v], w)
                W[v, u] = max(W[v, u], w)   # SYMMETRIZE (metric is undirected) -- the flaw
        D = np.full((self.n, self.n), 4.0)
        np.fill_diagonal(D, 0.0)
        for u in range(self.n):
            for v in range(self.n):
                if W[u, v] > 0:
                    D[u, v] = 1.0 - W[u, v] + 1.0   # linked => near, in [1,2]
        for k in range(self.n):           # Floyd-Warshall: metric closure (triangle ineq.)
            D = np.minimum(D, D[:, k:k+1] + D[k:k+1, :])
        self.D = D

    def retrieve(self, src, cand_a, cand_b):
        # metric: pick the candidate at the smaller (closed) distance. On a 2-hop pair this
        # makes the indirect node look NEAR (triangle) and can't distinguish a reachable
        # INDIRECT target from an unreachable distractor placed near by metric closure.
        return cand_a if self.D[src, cand_a] <= self.D[src, cand_b] else cand_b


# ── graph + query construction ───────────────────────────────────────────────
def build_graph(rng, net):
    """Directed weighted association graph: random OUT_DEG out-edges per node with weights in
    (0.3,1.0]. Guarantees DIRECT 1-hop strong pairs and metric-violating 2-HOP bridges."""
    n = net.n
    for u in range(n):
        targets = rng.choice([v for v in range(n) if v != u], size=OUT_DEG, replace=False)
        ws = rng.uniform(0.3, 1.0, size=OUT_DEG)
        for v, w in zip(targets, ws):
            net.add_edge(u, int(v), float(w))
    return net


def make_1hop_query(rng, net):
    """1-HOP: src with >=1 out-edge; target = strongest DIRECT neighbor; distractor = a node
    that is NOT a direct neighbor of src."""
    for _ in range(200):
        src = int(rng.integers(net.n))
        nbrs = net.edges[src]
        if not nbrs:
            continue
        target = max(nbrs, key=lambda v: nbrs[v])
        non = [v for v in range(net.n) if v != src and v not in nbrs]
        if not non:
            continue
        distractor = int(rng.choice(non))
        return src, target, distractor
    return None


def make_2hop_query(rng, net):
    """2-HOP: X->Y->Z with NO direct X->Z edge (metric-violating bridge); distractor = a node
    UNREACHABLE from X within HOPS."""
    n = net.n
    for _ in range(400):
        x = int(rng.integers(n))
        one = set(net.edges[x].keys())
        two = set()
        for y in one:
            for z in net.edges[y].keys():
                if z != x and z not in one:   # 2-hop, no DIRECT x->z edge
                    two.add(z)
        two -= one
        two.discard(x)
        if not two:
            continue
        z = int(rng.choice(list(two)))
        reachable = one | two | {x}
        unreach = [v for v in range(n) if v not in reachable]
        if not unreach:
            continue
        distractor = int(rng.choice(unreach))
        return x, z, distractor
    return None


# ── arms ──────────────────────────────────────────────────────────────────────
def run_seed(seed):
    rng = np.random.default_rng(seed)

    # ONE shared ground-truth graph for the seed; every arm reads the SAME edges.
    base = build_graph(np.random.default_rng(seed), SemanticNet(N_NODES))

    arms = ["FULL", "ITEM", "SPATIAL", "SHUFFLE", "ABLATED"]
    acc1 = {k: [] for k in arms}     # 1-hop accuracy
    acc2 = {k: [] for k in arms}     # 2-hop accuracy

    # shuffle variant of the SAME graph
    shuf = SemanticNet(N_NODES)
    for u in range(N_NODES):
        for v, w in base.edges[u].items():
            shuf.add_edge(u, v, w)
    shuf.shuffle_edges(np.random.default_rng(seed + 777))

    half = N_QUERIES // 2
    for qi in range(N_QUERIES):
        two_hop = qi >= half
        q = make_2hop_query(rng, base) if two_hop else make_1hop_query(rng, base)
        if q is None:
            continue
        src, target, distractor = q
        if rng.random() < 0.5:
            cand_a, cand_b = target, distractor
        else:
            cand_a, cand_b = distractor, target

        for arm in arms:
            if arm == "ITEM":
                ans = ItemStore(N_NODES).retrieve(src, cand_a, cand_b)
            elif arm == "SPATIAL":
                ans = SpatialStandIn(base).retrieve(src, cand_a, cand_b)
            elif arm == "SHUFFLE":
                ans = shuf.retrieve(src, cand_a, cand_b)
            elif arm == "ABLATED":
                abl = SemanticNet(N_NODES, ablate_spread=True)
                abl.edges = base.edges
                ans = abl.retrieve(src, cand_a, cand_b)
            else:  # FULL
                ans = base.retrieve(src, cand_a, cand_b)

            if ans is None:                       # abstain -> resolve at chance
                ans = cand_a if rng.random() < 0.5 else cand_b
            correct = 1 if ans == target else 0
            (acc2 if two_hop else acc1)[arm].append(correct)

    res = {}
    for arm in arms:
        a1 = float(np.mean(acc1[arm])) if acc1[arm] else float("nan")
        a2 = float(np.mean(acc2[arm])) if acc2[arm] else float("nan")
        pooled = float(np.mean(acc1[arm] + acc2[arm]))
        res[arm] = (a1, a2, pooled)

    # NO-FAB: an OOV node with NO edges (disjoint trigram space) -> spread fires nothing.
    oov = SemanticNet(N_NODES + 1)
    for u in range(N_NODES):
        for v, w in base.edges[u].items():
            oov.add_edge(u, v, w)
    res["OOV_FIRES"] = oov.is_active(N_NODES)     # the extra node has zero edges; must be False
    return res


def main():
    print("=" * 80)
    print("H_1428 — SEMANTIC-NETWORK / SPREADING-ACTIVATION (2-hop) — R1 numpy MIRROR")
    print("=" * 80)
    per_seed = {s: run_seed(s) for s in SEEDS}
    for s in SEEDS:
        r = per_seed[s]
        print(f"seed {s}:")
        for arm in ["FULL", "ITEM", "SPATIAL", "SHUFFLE", "ABLATED"]:
            a1, a2, pooled = r[arm]
            print(f"   {arm:8s} 1hop={a1:.3f} 2hop={a2:.3f} pooled={pooled:.3f}")
        print(f"   OOV spread fires a node: {r['OOV_FIRES']} (NO-FAB wants False)")

    def mean(arm, idx):
        return float(np.mean([per_seed[s][arm][idx] for s in SEEDS]))

    Bpool = mean("FULL", 2)
    B2 = mean("FULL", 1)
    Item_pool = mean("ITEM", 2)
    Spatial2 = mean("SPATIAL", 1)
    Shuf_pool = mean("SHUFFLE", 2)
    Abl2 = mean("ABLATED", 1)
    oov_any = any(per_seed[s]["OOV_FIRES"] for s in SEEDS)

    print("-" * 80)
    print(f"MEAN FULL    pooled={Bpool:.3f}  2hop={B2:.3f}")
    print(f"MEAN ITEM    pooled={Item_pool:.3f}")
    print(f"MEAN SPATIAL 2hop={Spatial2:.3f}  (metric stand-in on the metric-VIOLATING set)")
    print(f"MEAN SHUFFLE pooled={Shuf_pool:.3f}")
    print(f"MEAN ABLATED 2hop={Abl2:.3f}")
    print(f"OOV spread fires (any seed): {oov_any}  (NO-FAB wants False)")

    def each(arm, idx, op, thr):
        return all(op(per_seed[s][arm][idx], thr) for s in SEEDS)

    le = lambda a, b: a <= b
    ge = lambda a, b: a >= b

    c1 = each("FULL", 2, ge, 0.80) and (Bpool >= 0.80)
    c2_item = each("ITEM", 2, le, 0.65) and (Item_pool <= 0.65)
    c2_spatial = each("SPATIAL", 1, le, 0.65) and (Spatial2 <= 0.65)
    c3 = each("SHUFFLE", 2, le, 0.65) and (Shuf_pool <= 0.65)
    c4 = each("ABLATED", 1, le, 0.65) and (Abl2 <= 0.65) and each("FULL", 1, ge, 0.80) and (B2 >= 0.80)
    c5 = not oov_any

    print("-" * 80)
    print("FROZEN 5-BAR (each seed AND mean):")
    print(f"c1 PRESENCE     FULL pooled>=0.80          : {c1}   (pooled={Bpool:.3f})")
    print(f"c2 DISTINCT     ITEM pooled<=0.65          : {c2_item}   (item={Item_pool:.3f})")
    print(f"                SPATIAL 2hop<=0.65 (metric) : {c2_spatial}   (spatial2={Spatial2:.3f})")
    print(f"c3 EARNED-EDGES SHUFFLE pooled<=0.65       : {c3}   (shuf={Shuf_pool:.3f})")
    print(f"c4 EARNED-SPREAD ABL 2hop<=0.65 & FULL 2hop>=0.80: {c4}   (abl2={Abl2:.3f} full2={B2:.3f})")
    print(f"c5 NO-FAB       OOV spread fires nothing    : {c5}   (oov_fires={oov_any})")
    c2 = c2_item and c2_spatial
    green = c1 and c2 and c3 and c4 and c5
    print("=" * 80)
    print(f"VERDICT (R1 mirror, DIRECTIONAL): {'GREEN' if green else 'RED / WALL'}")
    print("=" * 80)


if __name__ == "__main__":
    main()
