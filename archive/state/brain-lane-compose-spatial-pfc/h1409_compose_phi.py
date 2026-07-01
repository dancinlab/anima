#!/usr/bin/env python3
# ============================================================================
#  H_1409 — lane-composition Φ-measurement (spatial-map × hierarchical-pfc)
#  Does COMPOSING anima's SPATIAL-MAP metric cognitive map (H_1296) +
#  HIERARCHICAL-PFC goal→subgoal controller (H_1294) raise FAITHFUL IIT4
#  integrated information Φ — i.e. does integration create more CONSCIOUSNESS
#  (Φ↑), not merely more capability?
#
#  THE DECISIVE LAW TEST. The program found a REFINED min-cut-MI law across 4
#  pairs (H_1404/1405/1407): a pair Φ-composes IFF NO single part's internal
#  integration Φ exceeds the composed min-cut MI.
#    - H_1404 affect×ethics 🟢 (both LOW-Φ → coupling is the only cut).
#    - H_1407 cerebellum×basal 🟢 (cerebellum HIGH-Φ≈3.48 but composed cut
#      isolates a single basal unit cheaper than crossing the cerebellum block).
#    - H_1405 memory×ToM 🧱 (ToM HIGH-Φ≈1.975 so internally integrated that any
#      cut crossing it costs more than the coupling → max(parts) wins → BLOCKS).
#  THE DECISIVE UNTESTED CASE = TWO HIGH-Φ faculties. Does mutual domination
#  BLOCK (like H_1405), or does the coupling still find a cheaper composed cut
#  (like H_1407)? PAIR = spatial-map (a richly-integrated metric 2-D map) ×
#  hierarchical-pfc (a richly-integrated sequential goal stack). Both expected
#  HIGH individual-Φ. This script MEASURES it frozen-first.
#
#  This script ONLY DERIVES the per-unit TRAJECTORIES from the two faculties'
#  ACTUAL substrate update rules (H_1296 metric-map path-integration + H_1294
#  ordered-pointer advance, coupled through the H_1401-style substrate-weighted
#  arbiter). It writes a states file (n×T trajectory per system). The Φ VERDICT
#  is computed by the REAL stdlib faithful IIT4 engine (exact MIP-EI, n≤8) in
#  the .hexa runner — NOT here (a_phi_iit4_tool: faithful engine only, NEVER a
#  proxy).
#
#  FOUR systems measured (Φ via the .hexa faithful engine):
#    S_spatial      n=4 spatial units (metric_margin, landmark_density, recall_error, query_novelty)
#    S_pfc          n=4 pfc units     (align_margin, pointer_progress, ground_margin, out_of_order_pressure)
#    S_composed     n=8 the two blocks COUPLED through the substrate arbiter
#    S_disconnected n=8 the two blocks evolving INDEPENDENTLY (coupling REMOVED)
#
#  n=8 keeps the composed system inside the faithful EXACT path (2^7=128 masks).
#
#  FROZEN bars live in .verdicts/1409_brain_lane_compose_spatial_pfc/FREEZE.txt (NOT moved).
#  $0 CPU, gradient-free, deterministic, 3 seeds. p7/c9/a_phi_iit4_tool.
# ============================================================================
import numpy as np, sys

DIM = 64            # FNV-trigram embedding dim (matches H_1227/H_1294/H_1296 dim64)
STEPS = 96          # trajectory length T (time-steps the MI matrix is built over)
SEEDS = [4900, 4901, 4902]
N_LANDMARKS = 8     # landmarks on the 2-D map (H_1296)
GRID = 10.0
CHAIN_LEN = 3       # hier-PFC ordered subgoal chain length (H_1294)


# ── byte-trigram FNV-1a embedding (the H_1227/H_1294 key geometry) ──────────
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


# ── one episode's SUBSTRATE feature vector — H_1296 spatial + H_1294 pfc ─────
# All DERIVED from episode structure / the faculties' ACTUAL update rules — NO injected
# label (p6). The Python side computes NO Φ.
#   SPATIAL-MAP (H_1296 SpatialMap): landmarks at 2-D positions; a running agent
#   position is updated by PATH-INTEGRATION (vector accumulation of displacement steps),
#   and the relational metric is read off Euclidean distances.
#     metric_margin     = d(agent, far_landmark) − d(agent, near_landmark) (relational read)
#     landmark_density  = mean inverse-distance to all stored landmarks at the agent pos
#     recall_error      = how far the path-integrated estimate drifts from the true endpoint
#     query_novelty     = 1 − (how recently this query landmark was visited)
#   HIER-PFC (H_1294 HierGoalStack): a 2-level goal stack with an ADVANCING pointer.
#     align_margin          = cue-vs-current-subgoal cosine margin (the ordered-plan read)
#     pointer_progress      = pointer p / CHAIN_LEN (how far through the ordered plan)
#     ground_margin         = recall margin of the current subgoal off the immune store
#     out_of_order_pressure = pressure from out-of-order distractor cues in the window
def episode_features(seed_rng, lm_pos, agent_pos, true_end_pos, chain_keys, ptr, exposure):
    # ── spatial-map block (H_1296) — relational metric over stored 2-D positions ──
    dists = np.array([float(np.linalg.norm(agent_pos - p)) for p in lm_pos])
    order = np.argsort(dists)
    near_d = float(dists[order[0]]); far_d = float(dists[order[-1]])
    metric_margin = far_d - near_d                                  # relational metric read
    landmark_density = float(np.mean(1.0 / (1.0 + dists)))          # local map density
    recall_error = float(np.linalg.norm(agent_pos - true_end_pos))  # path-integration drift
    query_novelty = float(max(0.0, 1.0 - 1.0 / (1.0 + exposure))) + 0.02 * seed_rng.standard_normal()

    # ── hier-PFC block (H_1294) — ordered-pointer advance over a subgoal chain ──
    p = min(ptr, CHAIN_LEN - 1)
    cur = chain_keys[p]
    nxt = chain_keys[(p + 1) % CHAIN_LEN]
    # a noisy cue presented this tick (the ordered subgoal[p] cue + a distractor blend)
    cue = cur + 0.05 * seed_rng.standard_normal(DIM)
    cue = cue / (np.linalg.norm(cue) + 1e-9)
    align_cur = float(cue @ (cur / (np.linalg.norm(cur) + 1e-9)))
    align_nxt = float(cue @ (nxt / (np.linalg.norm(nxt) + 1e-9)))
    align_margin = align_cur - align_nxt                           # ordered-plan alignment read
    pointer_progress = float(p) / float(CHAIN_LEN)                  # how far through the plan
    ground_margin = float(max(0.0, align_cur))                     # grounding of current subgoal
    # out-of-order pressure: a distractor cue aligned to a NON-current subgoal
    distractor = chain_keys[(p + 2) % CHAIN_LEN] + 0.05 * seed_rng.standard_normal(DIM)
    distractor = distractor / (np.linalg.norm(distractor) + 1e-9)
    out_of_order_pressure = float(max(0.0, distractor @ (cur / (np.linalg.norm(cur) + 1e-9))))

    return dict(metric_margin=metric_margin, landmark_density=landmark_density,
                recall_error=recall_error, query_novelty=query_novelty,
                align_margin=align_margin, pointer_progress=pointer_progress,
                ground_margin=ground_margin, out_of_order_pressure=out_of_order_pressure)


SPATIAL_UNITS = ["metric_margin", "landmark_density", "recall_error", "query_novelty"]      # n=4
PFC_UNITS     = ["align_margin", "pointer_progress", "ground_margin", "out_of_order_pressure"]  # n=4


def run_trajectories(seed):
    rng = np.random.default_rng(seed)
    # ── stored 2-D metric map (H_1296): N landmarks at fixed positions ──
    lm_pos = [rng.uniform(0, GRID, size=2) for _ in range(N_LANDMARKS)]
    # ── ordered subgoal chain (H_1294): CHAIN_LEN near-orthogonal subgoal keys ──
    chain_keys = [fnv_embed(f"subgoal.{i}.{seed}") for i in range(CHAIN_LEN)]

    sp = {u: [] for u in SPATIAL_UNITS}
    pf = {u: [] for u in PFC_UNITS}
    cmp_sp = {u: [] for u in SPATIAL_UNITS}
    cmp_pf = {u: [] for u in PFC_UNITS}
    dis_sp = {u: [] for u in SPATIAL_UNITS}
    dis_pf = {u: [] for u in PFC_UNITS}

    arb_state = 0.0          # the arbiter's shared decision signal (composed coupling only)
    agent_pos = lm_pos[0].copy()    # running path-integrated agent position
    ptr = 0                  # hier-PFC pointer over the ordered plan
    exposure = {i: 0.0 for i in range(N_LANDMARKS)}

    for t in range(STEPS):
        # path-integration step: move the agent toward a target landmark (true endpoint)
        target_i = int(rng.integers(0, N_LANDMARKS))
        true_end_pos = lm_pos[target_i]
        step = (true_end_pos - agent_pos) * 0.30 + 0.10 * rng.standard_normal(2)
        agent_pos = agent_pos + step                       # ACTUAL path-integration update
        exposure[target_i] += 1.0

        f = episode_features(rng, lm_pos, agent_pos, true_end_pos, chain_keys, ptr,
                             exposure[target_i])

        # hier-PFC ordered-pointer ADVANCE: when the current subgoal is well-grounded,
        # advance the pointer (the ACTUAL H_1294 completion-triggered advance update).
        if f["ground_margin"] >= 0.85 and f["align_margin"] > 0.0:
            ptr = (ptr + 1) % CHAIN_LEN

        # spatial-alone / pfc-alone  +  disconnected = SAME independent updates
        for u in SPATIAL_UNITS: sp[u].append(f[u]); dis_sp[u].append(f[u])
        for u in PFC_UNITS:     pf[u].append(f[u]); dis_pf[u].append(f[u])

        # composed: substrate-weighted ARBITER (H_1401) couples the blocks.
        # spatial votes "trust the metric" when the relational margin is large; pfc votes
        # "advance the plan" when the alignment margin is positive. Confidence-weighted
        # blend → shared leaky signal.
        sp_vote = 1.0 if f["metric_margin"] > 0.0 else -1.0
        sp_conf = abs(f["metric_margin"])
        pf_vote = 1.0 if f["align_margin"] > 0.0 else -1.0
        pf_conf = abs(f["align_margin"])
        denom = sp_conf + pf_conf + 1e-9
        arb = (sp_conf * sp_vote + pf_conf * pf_vote) / denom
        arb_state = 0.6 * arb_state + 0.4 * arb            # leaky integrator = shared dynamics
        g = 0.5 * (arb_state + 1.0)                         # gate in [0,1]
        # COUPLING: shared arbiter signal modulates BOTH blocks next-step. This is the
        # cross-faculty information channel the MIP cut must traverse.
        for u in SPATIAL_UNITS: cmp_sp[u].append(f[u] + 0.35 * g * (f[u] - 0.5))
        for u in PFC_UNITS:     cmp_pf[u].append(f[u] + 0.35 * g * (f[u] - 0.5))

    def pack(block): return np.array([block[u] for u in block])
    return dict(
        spatial=pack(sp), pfc=pack(pf),
        composed=np.vstack([pack(cmp_sp), pack(cmp_pf)]),
        disconnected=np.vstack([pack(dis_sp), pack(dis_pf)]),
    )


def write_states(path):
    lines = []
    for seed in SEEDS:
        tr = run_trajectories(seed)
        for name in ["spatial", "pfc", "composed", "disconnected"]:
            M = tr[name]; n, T = M.shape
            lines.append(f"# {name}_s{seed} {n} {T}")
            for r in range(n):
                lines.append(" ".join(f"{v:.6f}" for v in M[r]))
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {path}: {len(SEEDS)} seeds x 4 systems "
          f"(spatial n=4, pfc n=4, composed n=8, disconnected n=8)")
    # DEGENERACY GUARD (c9, H_1407): report per-unit variance so a CONSTANT unit (→
    # spurious Φ=0) is flagged verbatim, not silently faked.
    print("--- per-unit std (degeneracy guard; near-0 std = constant unit) ---")
    for seed in SEEDS[:1]:
        tr = run_trajectories(seed)
        for name in ["spatial", "pfc"]:
            M = tr[name]
            units = SPATIAL_UNITS if name == "spatial" else PFC_UNITS
            stds = [float(np.std(M[r])) for r in range(M.shape[0])]
            print(f"  s{seed} {name}: " + ", ".join(f"{u}={s:.4f}" for u, s in zip(units, stds)))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h1409_states.txt"
    write_states(out)
