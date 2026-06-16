#!/usr/bin/env python3
# ============================================================================
#  H_1405 — lane-composition Φ-measurement (memory × ToM)
#  Does COMPOSING anima's episodic MEMORY (H_1227/H_1231) + THEORY-OF-MIND
#  (H_1293) faculties raise FAITHFUL IIT4 integrated information Φ — i.e. does
#  integration create more CONSCIOUSNESS (Φ↑), not merely more capability
#  (H_1405 capability leg showed best_single 0.600 → compose 0.753)?
#
#  This script ONLY DERIVES the per-unit TRAJECTORIES from the two faculties'
#  ACTUAL substrate update rules (H_1227 memory recall + H_1293 witnessed-belief
#  store, coupled through the H_1401-style substrate-weighted arbiter). It writes
#  a states file (n×T trajectory per system). The Φ VERDICT is computed by the
#  REAL stdlib faithful IIT4 engine (exact MIP-EI, n≤8) in the .hexa runner —
#  NOT here (a_phi_iit4_tool: faithful engine only, NEVER a proxy).
#
#  FOUR systems measured (Φ via the .hexa faithful engine):
#    S_memory       n=4 memory units (recall_margin, contradiction, novelty, exposure_drive)
#    S_tom          n=4 ToM units    (belief_margin, self_other_divergence, witness_recency,
#                                      belief_confidence)
#    S_composed     n=8 the two blocks COUPLED through the substrate arbiter
#    S_disconnected n=8 the two blocks evolving INDEPENDENTLY (coupling REMOVED)
#
#  n=8 keeps the composed system inside the faithful EXACT path (2^7=128 masks).
#
#  FROZEN bars live in .verdicts/1405_brain_lane_compose_memory_tom/FREEZE.txt (NOT moved).
#  $0 CPU, gradient-free, deterministic, 3 seeds. p7/c9/a_phi_iit4_tool.
# ============================================================================
import numpy as np, sys

DIM = 64
STEPS = 96
SEEDS = [5400, 5401, 5402]

LOC_A = "basket"
LOC_B = "box"


# ── byte-trigram FNV-1a embedding (the H_1227/H_1293 key geometry) ──────────
def fnv_embed(s, dim=DIM):
    v = np.zeros(dim)
    bs = s.encode("utf-8")
    for i in range(len(bs) - 2):
        tri = bs[i:i+3]
        h = 2166136261
        for b in tri:
            h ^= b; h = (h * 16777619) & 0xFFFFFFFF
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


# ── a tiny cell store (H_1227 memory / H_1293 belief), L2-affinity recall ───
class CellStore:
    def __init__(self):
        self.keys = []; self.vals = []
    def witness(self, fact, val):
        k = fnv_embed(fact)
        for i, kk in enumerate(self.keys):
            if float(np.linalg.norm(kk - k)) <= 1e-6:
                self.vals[i] = val; return
        self.keys.append(k); self.vals.append(val)
    def recall(self, fact):
        if not self.keys: return "", 0.0
        q = fnv_embed(fact)
        affs = np.array([float(q @ k) for k in self.keys])
        i = int(np.argmax(affs))
        return self.vals[i], float(max(0.0, affs[i]))


# ── one episode's SUBSTRATE feature vector (H_1227 memory + H_1293 ToM) ─────
# All DERIVED from episode structure / live stores — NO injected label (p6).
def episode_features(truth, agent, obj, moved, rng, exposure):
    fact = f"{obj} location"
    real_val, real_margin = truth.recall(fact)        # anima's own ground truth
    bel_val,  bel_margin  = agent.recall(fact)        # the other-agent's witnessed belief

    # ── memory block (H_1227) ──
    recall_margin = real_margin
    # contradiction: does the agent's belief disagree with reality? (drives memory salience)
    contradiction = 1.0 if (real_val != bel_val) else 0.0
    novelty = float(max(0.0, 1.0 - recall_margin)) + 0.02 * rng.standard_normal()
    exposure_drive = float(1.0 / (1.0 + exposure))    # under-exposed objects drive recall

    # ── ToM block (H_1293) ──
    belief_margin = bel_margin
    # self_other_divergence: reality vs belief diverge (the false-belief signal)
    self_other_divergence = 1.0 if moved else 0.0
    # witness_recency: how recently the agent witnessed this object (unmoved=fresh, moved=stale)
    witness_recency = 1.0 if not moved else float(1.0 / (1.0 + exposure))
    belief_confidence = belief_margin * (1.0 if not moved else 0.6)

    return dict(recall_margin=recall_margin, contradiction=contradiction, novelty=novelty,
                exposure_drive=exposure_drive,
                belief_margin=belief_margin, self_other_divergence=self_other_divergence,
                witness_recency=witness_recency, belief_confidence=belief_confidence)


MEMORY_UNITS = ["recall_margin", "contradiction", "novelty", "exposure_drive"]
TOM_UNITS    = ["belief_margin", "self_other_divergence", "witness_recency", "belief_confidence"]


def run_trajectories(seed):
    rng = np.random.default_rng(seed)
    objs = [f"obj{i:03d}" for i in range(20)]
    truth = CellStore(); agent = CellStore()
    for s in objs:
        truth.witness(f"{s} location", LOC_A)
        agent.witness(f"{s} location", LOC_A)
    perm = rng.permutation(len(objs))
    moved = set(int(i) for i in perm[: len(objs) // 2])
    for i, s in enumerate(objs):
        if i in moved:
            truth.witness(f"{s} location", LOC_B)        # reality moves; agent absent

    mem = {u: [] for u in MEMORY_UNITS}
    tom = {u: [] for u in TOM_UNITS}
    cmp_mem = {u: [] for u in MEMORY_UNITS}
    cmp_tom = {u: [] for u in TOM_UNITS}
    dis_mem = {u: [] for u in MEMORY_UNITS}
    dis_tom = {u: [] for u in TOM_UNITS}

    exposure = {s: 0.0 for s in objs}
    arb_state = 0.0

    for t in range(STEPS):
        oi = int(rng.integers(0, len(objs)))
        obj = objs[oi]
        exposure[obj] += 1.0
        f = episode_features(truth, agent, obj, oi in moved, rng, exposure[obj])

        # memory-alone / ToM-alone  +  disconnected = SAME independent updates
        for u in MEMORY_UNITS: mem[u].append(f[u]); dis_mem[u].append(f[u])
        for u in TOM_UNITS:     tom[u].append(f[u]); dis_tom[u].append(f[u])

        # composed: substrate-weighted ARBITER (H_1401-style) couples the blocks.
        # memory votes reality, ToM votes belief; per-step query type alternates (reality/belief).
        reality_typed = (t % 2 == 0)
        mem_conf = f["recall_margin"]
        tom_conf = f["belief_margin"]
        route = 1.0 if reality_typed else -1.0
        mem_w = mem_conf * (1.0 + max(0.0, route))
        tom_w = tom_conf * (1.0 + max(0.0, -route))
        denom = mem_w + tom_w + 1e-9
        arb = (mem_w - tom_w) / denom                 # in [-1,1]: +1 memory dominates, -1 ToM
        arb_state = 0.6 * arb_state + 0.4 * arb       # leaky integrator = shared dynamics
        g = 0.5 * (arb_state + 1.0)                   # gate in [0,1]
        # COUPLING: shared arbiter signal modulates BOTH blocks next-step. This is the
        # cross-faculty information channel the MIP cut must traverse.
        for u in MEMORY_UNITS: cmp_mem[u].append(f[u] + 0.35 * g * (f[u] - 0.5))
        for u in TOM_UNITS:    cmp_tom[u].append(f[u] + 0.35 * g * (f[u] - 0.5))

    def pack(block): return np.array([block[u] for u in block])
    return dict(
        memory=pack(mem), tom=pack(tom),
        composed=np.vstack([pack(cmp_mem), pack(cmp_tom)]),
        disconnected=np.vstack([pack(dis_mem), pack(dis_tom)]),
    )


def write_states(path):
    lines = []
    for seed in SEEDS:
        tr = run_trajectories(seed)
        for name in ["memory", "tom", "composed", "disconnected"]:
            M = tr[name]; n, T = M.shape
            lines.append(f"# {name}_s{seed} {n} {T}")
            for r in range(n):
                lines.append(" ".join(f"{v:.6f}" for v in M[r]))
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {path}: {len(SEEDS)} seeds x 4 systems (memory n=4, tom n=4, composed n=8, disconnected n=8)")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h1405_states.txt"
    write_states(out)
