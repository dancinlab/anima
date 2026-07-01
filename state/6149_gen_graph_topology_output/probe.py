# H_6149 graph-topology output (non-AR, combination=edges) — numpy DIRECTIONAL screen
# ============================================================================
# G1 recombination wall = trunk COMBINATION OPERATOR floor. Prior census:
#   readout ops (H_1816 predcoding / H_1823 circconv), tension (H_1834),
#   constraint-intersection (H_6104) ALL floor == additive by construction.
#   meiosis-crossover (H_6112) numpy REACHABLE 1.0 BUT real CLMConvMoE trunk
#   FALSIFIED (0->0.022) -> numpy abstract toys OVERSTATE.
# H_6149 angle: abandon the 1D AR sequence entirely; output is a GRAPH whose
#   EDGES encode the composition of two independent concepts.
# Question of this screen: does a graph-structured (edge-as-combination) output
#   recover BOTH independent legs where an additive-superposition 1D readout
#   collapses to a single nearest basin?
#
# FROZEN BAR (set BEFORE the run):
#   composed_distinct(graph) - composed_distinct(additive) >= +0.30
#   AND composed_distinct(additive) <= 0.20   on >= 2/3 seeds.
# GREEN-DIRECTIONAL iff bar met. numpy == DIRECTIONAL, never terminal.
# ============================================================================
import numpy as np

K = 8          # number of independent concept prototypes
D = 6          # feature dims per concept slot (concepts INDEPENDENT / orthogonal)
def run(seed):
    rng = np.random.default_rng(seed)
    # K independent concepts, each a random orthonormal-ish vector in R^D
    C = rng.standard_normal((K, D))
    C /= np.linalg.norm(C, axis=1, keepdims=True)
    # a "valid composition" of concept i and j = we can READ OUT both i and j
    # from the combined object (both legs recoverable) -> a genuinely new pair.
    pairs = [(i, j) for i in range(K) for j in range(K) if i != j]  # off-diagonal
    add_hits = 0
    graph_hits = 0
    for (i, j) in pairs:
        # ---- ADDITIVE readout baseline (the anima mouth failure mode) ----
        # superpose the two concept vectors in ONE 1D slot, then nearest-basin
        # (argmax over concept dictionary) readout -> collapses to dominant leg.
        s = C[i] + C[j]
        sims = C @ s
        top2 = set(np.argsort(sims)[-2:].tolist())
        add_ok = ({i, j} == top2)          # BOTH legs recovered from the sum?
        add_hits += add_ok
        # ---- H_6149 GRAPH output (edges = combination) ----
        # output is a 2-node graph: node slot A holds concept i, node slot B
        # holds concept j, and an EDGE records the relation. Each leg lives in
        # its OWN coordinate (no superposition) -> read out per-node.
        nodeA = C[i]; nodeB = C[j]
        recA = int(np.argmax(C @ nodeA))
        recB = int(np.argmax(C @ nodeB))
        edge_present = True                 # non-AR: relation is emitted, not chained
        graph_ok = (recA == i and recB == j and edge_present and recA != recB)
        graph_hits += graph_ok
    n = len(pairs)
    return add_hits / n, graph_hits / n

seeds = [6149, 6150, 6151]
print("H_6149 GRAPH-TOPOLOGY OUTPUT (non-AR, edges=combination) vs ADDITIVE readout")
print(f"K={K} concept-dim={D}  off-diagonal pairs/seed={K*(K-1)}")
print("FROZEN BAR: (graph-additive)>=+0.30 AND additive<=0.20 on >=2/3 seeds")
print("-"*72)
wins = 0
for s in seeds:
    a, g = run(s)
    win = (g - a >= 0.30) and (a <= 0.20)
    wins += win
    print(f"seed {s}: additive={a:.3f}  graph={g:.3f}  lift={g-a:+.3f}  {'WIN' if win else 'floor'}")
print("-"*72)
verdict = "GREEN-DIRECTIONAL" if wins >= 2 else "FLOOR/FALSIFIED"
print(f"wins={wins}/3  VERDICT: {verdict}  (numpy = DIRECTIONAL, never terminal)")
print("NOTE: graph 'combination-by-construction' reaches by placing each leg in its")
print("own node coord (no superposition) -> tautological reach, SAME overstatement")
print("class as H_6112 meiosis (numpy 1.0 -> real trunk 0.022). transfer-UNVERIFIED.")
