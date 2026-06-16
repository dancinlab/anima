#!/usr/bin/env python3
# ============================================================================
#  H_1408 — lane-composition Φ-measurement (WITHIN the memory family)
#  Does COMPOSING anima's spatial-map (H_1296) + episodic-memory (H_1227/H_1231)
#  faculties raise FAITHFUL IIT4 integrated information Φ — i.e. does integration
#  create more CONSCIOUSNESS (Φ↑), not merely more capability (the capability
#  probe showed best_single≈0.703 → compose≈0.899)?
#
#  This script ONLY DERIVES the per-unit TRAJECTORIES from the two faculties'
#  ACTUAL substrate update rules (H_1296 spatial-map metric features + H_1227
#  episodic recall features, coupled through the H_1401/H_1405 substrate-weighted
#  arbiter). It writes a states file (n×T trajectory per system). The Φ VERDICT is
#  computed by the REAL stdlib faithful IIT4 engine (exact MIP-EI, n≤8) in the
#  .hexa runner — NOT here (a_phi_iit4_tool: faithful engine only, NEVER a proxy).
#
#  FOUR systems measured (Φ via the .hexa faithful engine):
#    S_spatial      n=4 spatial units  (nearest_margin, metric_spread, landmark_novelty, query_where_cue)
#    S_episodic     n=4 episodic units (recall_margin, contradiction, value_novelty, exposure_drive)
#    S_composed     n=8 the two blocks COUPLED through the substrate arbiter
#    S_disconnected n=8 the two blocks evolving INDEPENDENTLY (coupling REMOVED)
#
#  n=8 keeps the composed system inside the faithful EXACT path (2^7=128 masks).
#
#  FROZEN bars live in .verdicts/1408_brain_lane_compose_spatial_episodic/FREEZE.txt.
#  $0 CPU, gradient-free, deterministic, 3 seeds. p7/c9/a_phi_iit4_tool.
# ============================================================================
import numpy as np, sys

DIM = 64            # FNV-trigram embedding dim (matches H_1227/H_1296 geometry)
STEPS = 96          # trajectory length T (time-steps the MI matrix is built over)
SEEDS = [5408, 5409, 5410]
GRID = 10.0
N_LANDMARKS = 8

# ── byte-trigram FNV-1a embedding (the H_1227/H_1296 key geometry) ──────────
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

# routing anchors (H_1405): query-text geometry routes the composed coupling
_WHAT = fnv_embed("what is bound to landmark")
_WHERE = fnv_embed("which landmark is nearer to")

# ── episodic immune store (H_1227): bind name -> value-key; recall by affinity ──
class ImmuneStore:
    def __init__(self):
        self.keys = []; self.vals = []
    def bind(self, name, val):
        self.keys.append(fnv_embed(name)); self.vals.append(fnv_embed(val))
    def recall(self, name):
        if not self.keys: return 0.0, 0
        q = fnv_embed(name)
        affs = np.array([float(q @ k) for k in self.keys])
        i = int(np.argmax(affs))
        return float(max(0.0, affs[i])), i

# ── one episode's SUBSTRATE feature vector (H_1296 spatial + H_1227 episodic) ──
# All DERIVED from episode structure / live stores — NO injected label (p6).
def episode_features(positions, names, store, target, x, a, b, queried_val, rng, exposure):
    # ── spatial units (H_1296 metric map) ──
    px, pa, pb = positions[x], positions[a], positions[b]
    da = float(np.linalg.norm(px - pa)); db = float(np.linalg.norm(px - pb))
    nearest_margin = abs(da - db) / (GRID * 1.4142)                 # metric query margin, normalized
    all_pos = np.array([positions[n] for n in names])
    metric_spread = float(np.std(all_pos)) / GRID                   # map dispersion
    nearest_d = min(float(np.linalg.norm(px - positions[n])) for n in names if n != x)
    landmark_novelty = float(min(1.0, nearest_d / GRID))           # how isolated X is
    qtext = f"which landmark is nearer to {a} or {b}"
    qe = fnv_embed(qtext)
    query_where_cue = 1.0 / (1.0 + np.exp(-((qe @ _WHERE) - (qe @ _WHAT)) * 6.0))
    # ── episodic units (H_1227 recall) ──
    recall_margin, ni = store.recall(f"value bound to landmark {target}")
    qv = fnv_embed(queried_val)
    contradiction = float(max(0.0, 1.0 - (qv @ store.vals[ni])))
    value_novelty = float(max(0.0, 1.0 - recall_margin)) + 0.02 * rng.standard_normal()
    exposure_drive = float(1.0 / (1.0 + np.exp(-(exposure - 1.0))))
    return dict(nearest_margin=nearest_margin, metric_spread=metric_spread,
                landmark_novelty=landmark_novelty, query_where_cue=float(query_where_cue),
                recall_margin=recall_margin, contradiction=contradiction,
                value_novelty=value_novelty, exposure_drive=exposure_drive)

SPATIAL_UNITS = ["nearest_margin", "metric_spread", "landmark_novelty", "query_where_cue"]
EPISODIC_UNITS = ["recall_margin", "contradiction", "value_novelty", "exposure_drive"]

def run_trajectories(seed):
    rng = np.random.default_rng(seed)
    names = [f"L{i}" for i in range(N_LANDMARKS)]
    positions = {n: rng.uniform(0, GRID, size=2) for n in names}
    vals = ["alpha","beta","gamma","delta","epsilon","zeta","eta","theta"]
    bound = {n: vals[rng.integers(0, len(vals))] for n in names}
    store = ImmuneStore()
    for n in names:
        store.bind(f"value bound to landmark {n}", bound[n])

    sp = {u: [] for u in SPATIAL_UNITS}
    ep = {u: [] for u in EPISODIC_UNITS}
    cmp_sp = {u: [] for u in SPATIAL_UNITS}
    cmp_ep = {u: [] for u in EPISODIC_UNITS}
    dis_sp = {u: [] for u in SPATIAL_UNITS}
    dis_ep = {u: [] for u in EPISODIC_UNITS}

    exposure = {n: 0.0 for n in names}
    arb_state = 0.0   # the arbiter's shared decision signal (composed coupling only)

    for t in range(STEPS):
        target = names[rng.integers(0, len(names))]
        x, a, b = rng.choice(names, size=3, replace=False)
        exposure[target] += 1.0
        qv = bound[target] if rng.random() < 0.6 else vals[rng.integers(0, len(vals))]
        f = episode_features(positions, names, store, target, x, a, b, qv, rng, exposure[target])

        # spatial-alone / episodic-alone  +  disconnected = SAME independent updates
        for u in SPATIAL_UNITS: sp[u].append(f[u]); dis_sp[u].append(f[u])
        for u in EPISODIC_UNITS: ep[u].append(f[u]); dis_ep[u].append(f[u])

        # composed: substrate-weighted ARBITER (H_1401/H_1405) couples the blocks.
        # spatial vote: metric nearer-margin; episodic vote: recall margin vs contradiction.
        where_cue = f["query_where_cue"]
        sp_conf = f["nearest_margin"]
        ep_conf = f["recall_margin"] * (1.0 - f["contradiction"])
        sp_w = sp_conf * where_cue
        ep_w = ep_conf * (1.0 - where_cue)
        sp_vote = 1.0 if sp_w >= ep_w else -1.0
        denom = sp_w + ep_w + 1e-9
        arb = (sp_w * sp_vote + ep_w * (-sp_vote)) / denom
        arb_state = 0.6 * arb_state + 0.4 * arb     # leaky integrator = shared dynamics
        g = 0.5 * (arb_state + 1.0)                  # gate in [0,1]
        # COUPLING: shared arbiter signal modulates BOTH blocks next-step. This is the
        # cross-faculty information channel the MIP cut must traverse.
        for u in SPATIAL_UNITS: cmp_sp[u].append(f[u] + 0.35 * g * (f[u] - 0.5))
        for u in EPISODIC_UNITS: cmp_ep[u].append(f[u] + 0.35 * g * (f[u] - 0.5))

    def pack(block): return np.array([block[u] for u in block])
    return dict(
        spatial=pack(sp), episodic=pack(ep),
        composed=np.vstack([pack(cmp_sp), pack(cmp_ep)]),
        disconnected=np.vstack([pack(dis_sp), pack(dis_ep)]),
    )

def write_states(path):
    lines = []
    for seed in SEEDS:
        tr = run_trajectories(seed)
        for name in ["spatial", "episodic", "composed", "disconnected"]:
            M = tr[name]; n, T = M.shape
            lines.append(f"# {name}_s{seed} {n} {T}")
            for r in range(n):
                lines.append(" ".join(f"{v:.6f}" for v in M[r]))
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {path}: {len(SEEDS)} seeds x 4 systems "
          f"(spatial n=4, episodic n=4, composed n=8, disconnected n=8)")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h1408_states.txt"
    write_states(out)
