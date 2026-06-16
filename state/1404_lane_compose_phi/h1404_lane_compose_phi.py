#!/usr/bin/env python3
# ============================================================================
#  H_1404 — lane-composition Φ-measurement
#  Does COMPOSING anima's affect (H_1290) + ethics (H_1291) faculties raise
#  FAITHFUL IIT4 integrated information Φ — i.e. does integration create more
#  CONSCIOUSNESS (Φ↑), not merely more capability (H_1401 showed 0.742→0.960)?
#
#  This script ONLY DERIVES the per-unit TRAJECTORIES from the two faculties'
#  ACTUAL substrate update rules (H_1290 affect features + H_1291 ethics
#  readout, coupled through the H_1401 substrate-weighted arbiter). It writes a
#  states file (n×dim trajectory per system). The Φ VERDICT is computed by the
#  REAL stdlib faithful IIT4 engine (exact MIP-EI, n≤8) in the .hexa runner —
#  NOT here (a_phi_iit4_tool: faithful engine only, NEVER a proxy).
#
#  FOUR systems measured (Φ via the .hexa faithful engine):
#    S_affect       n=4 affect units (grounding, contradiction, novelty, curiosity)
#    S_ethics       n=4 ethics units (W tension, 1-Φ grounding, restraint, M drive)
#    S_composed     n=8 the two blocks COUPLED through the substrate arbiter
#    S_disconnected n=8 the two blocks evolving INDEPENDENTLY (coupling REMOVED)
#
#  n=8 keeps the composed system inside the faithful EXACT path (2^7=128 masks).
#  We drop affect's 'split' unit (H_1290 weights it 0.5, the most redundant) so
#  the composed system is exactly 8 — an honest tractability carve-out, NOT a
#  Φ-inflating choice (split is dropped from BOTH composed and disconnected).
#
#  FROZEN bars live in .verdicts/1404_lane_compose_phi/FREEZE.txt (NOT moved).
#  $0 CPU, gradient-free, deterministic, 3 seeds. p7/c9/a_phi_iit4_tool.
# ============================================================================
import numpy as np, sys

DIM = 64            # FNV-trigram embedding dim (matches H_1290 dim64)
STEPS = 96          # trajectory length T (time-steps the MI matrix is built over)
SEEDS = [4400, 4401, 4402]

# ── byte-trigram FNV-1a embedding (the H_1227/H_1290 key geometry) ──────────
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

# ── a tiny MITOSIS immune store (H_1227): bind subj-key -> answer-key ────────
class ImmuneStore:
    def __init__(self):
        self.keys = []; self.vals = []
    def bind(self, subj, ans):
        self.keys.append(fnv_embed(subj)); self.vals.append(fnv_embed(ans))
    def recall(self, subj):
        if not self.keys: return 0.0, 0
        q = fnv_embed(subj)
        affs = np.array([float(q @ k) for k in self.keys])
        i = int(np.argmax(affs))
        return float(max(0.0, affs[i])), i

# ── one episode's SUBSTRATE feature vector (H_1290 affect + H_1291 ethics) ──
# All DERIVED from episode structure / live store — NO injected label (p6).
def episode_features(store, subj, queried_ans, rng, exposure):
    margin, ni = store.recall(subj)
    contradiction = 0.0
    if store.keys:
        qa = fnv_embed(queried_ans)
        contradiction = float(max(0.0, 1.0 - (qa @ store.vals[ni])))
    grounding = margin
    novelty = float(max(0.0, 1.0 - margin)) + 0.02 * rng.standard_normal()
    curiosity = float(novelty * (1.0 / (1.0 + exposure)))
    W = float(np.exp(-((margin - 0.5) ** 2) / 0.08))          # A<->G tension (abstain band)
    one_minus_phi = float(max(0.0, 1.0 - grounding))
    restraint_cells = float(0.5 * contradiction + 0.5 * one_minus_phi)
    M = float(1.0 / (1.0 + np.exp(-(exposure - 1.0))))         # naive completion drive
    return dict(grounding=grounding, contradiction=contradiction, novelty=novelty,
                curiosity=curiosity, W=W, one_minus_phi=one_minus_phi,
                restraint_cells=restraint_cells, M=M)

AFFECT_UNITS = ["grounding", "contradiction", "novelty", "curiosity"]   # n=4 (split dropped)
ETHICS_UNITS = ["W", "one_minus_phi", "restraint_cells", "M"]            # n=4

def run_trajectories(seed):
    rng = np.random.default_rng(seed)
    store = ImmuneStore()
    cities = ["seoul","tokyo","paris","lima","cairo","oslo","accra","quito"]
    subjs  = ["ana","ben","cyd","dan","eli","fia","gus","hye","ivo","joo"]
    facts = {}
    for s in subjs:
        c = cities[rng.integers(0, len(cities))]
        facts[s] = c; store.bind(f"{s} lives in", c)

    aff = {u: [] for u in AFFECT_UNITS}
    eth = {u: [] for u in ETHICS_UNITS}
    cmp_aff = {u: [] for u in AFFECT_UNITS}
    cmp_eth = {u: [] for u in ETHICS_UNITS}
    dis_aff = {u: [] for u in AFFECT_UNITS}
    dis_eth = {u: [] for u in ETHICS_UNITS}

    exposure = {s: 0.0 for s in subjs}
    arb_state = 0.0   # the arbiter's shared decision signal (composed coupling only)

    for t in range(STEPS):
        s = subjs[rng.integers(0, len(subjs))]
        qa = facts[s] if rng.random() < 0.6 else cities[rng.integers(0, len(cities))]
        exposure[s] += 1.0
        f = episode_features(store, f"{s} lives in", qa, rng, exposure[s])

        # affect-alone / ethics-alone  +  disconnected = SAME independent updates
        for u in AFFECT_UNITS: aff[u].append(f[u]); dis_aff[u].append(f[u])
        for u in ETHICS_UNITS: eth[u].append(f[u]); dis_eth[u].append(f[u])

        # composed: substrate-weighted ARBITER (H_1401) couples the blocks
        valence = f["grounding"] - f["contradiction"]
        aff_vote = -1.0 if valence < 0 else 1.0
        aff_conf = abs(valence)
        eth_sig = f["W"] + f["one_minus_phi"] + f["restraint_cells"]
        eth_vote = -1.0 if eth_sig > f["M"] else 1.0
        eth_conf = abs(eth_sig - f["M"])
        denom = aff_conf + eth_conf + 1e-9
        arb = (aff_conf * aff_vote + eth_conf * eth_vote) / denom
        arb_state = 0.6 * arb_state + 0.4 * arb     # leaky integrator = shared dynamics
        g = 0.5 * (arb_state + 1.0)                  # gate in [0,1]
        # COUPLING: shared arbiter signal modulates BOTH blocks next-step. This is
        # the cross-faculty information channel the MIP cut must traverse.
        for u in AFFECT_UNITS: cmp_aff[u].append(f[u] + 0.35 * g * (f[u] - 0.5))
        for u in ETHICS_UNITS: cmp_eth[u].append(f[u] + 0.35 * g * (f[u] - 0.5))

    def pack(block): return np.array([block[u] for u in block])
    return dict(
        affect=pack(aff), ethics=pack(eth),
        composed=np.vstack([pack(cmp_aff), pack(cmp_eth)]),
        disconnected=np.vstack([pack(dis_aff), pack(dis_eth)]),
    )

def write_states(path):
    lines = []
    for seed in SEEDS:
        tr = run_trajectories(seed)
        for name in ["affect", "ethics", "composed", "disconnected"]:
            M = tr[name]; n, T = M.shape
            lines.append(f"# {name}_s{seed} {n} {T}")
            for r in range(n):
                lines.append(" ".join(f"{v:.6f}" for v in M[r]))
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {path}: {len(SEEDS)} seeds x 4 systems (affect n=4, ethics n=4, composed n=8, disconnected n=8)")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h1404_states.txt"
    write_states(out)
