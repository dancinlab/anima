#!/usr/bin/env python3
# ============================================================================
#  H_1407 — lane-composition Φ-measurement (cerebellum × basal-ganglia)
#  Does COMPOSING anima's CEREBELLUM forward-model (H_1280) + BASAL-GANGLIA
#  action-gating (H_1281) faculties raise FAITHFUL IIT4 integrated information
#  Φ — i.e. does integration create more CONSCIOUSNESS (Φ↑), not merely more
#  capability (H_1407 capability leg showed best_single 0.693 → compose 0.769)?
#
#  THE LAW TEST. H_1404 (affect×ethics) Φ-COMPOSED because BOTH parts were LOW
#  individual-Φ (≈0.28/0.00) → coupling super-additive. H_1405 (memory×ToM) did
#  NOT, because ToM was ALREADY high individual-Φ (≈1.975) and dominated max(parts).
#  PROVISIONAL LAW: a pair Φ-composes IFF BOTH parts are low individual-Φ control
#  faculties. cerebellum + basal-ganglia are BOTH low-Φ CONTROL faculties → the law
#  PREDICTS they SHOULD Φ-compose. This script MEASURES it frozen-first.
#
#  This script ONLY DERIVES the per-unit TRAJECTORIES from the two faculties'
#  ACTUAL substrate update rules (H_1280 forward-model error/correction + H_1281
#  go/no-go competition, coupled through the H_1401-style substrate-weighted
#  arbiter). It writes a states file (n×T trajectory per system). The Φ VERDICT is
#  computed by the REAL stdlib faithful IIT4 engine (exact MIP-EI, n≤8) in the
#  .hexa runner — NOT here (a_phi_iit4_tool: faithful engine only, NEVER a proxy).
#
#  FOUR systems measured (Φ via the .hexa faithful engine):
#    S_cerebellum   n=4 cerebellum units (pred_error, pred_confidence, correction_drive, state_novelty)
#    S_basal        n=4 basal units      (go_margin, competition_spread, no_go_pressure, outcome_reward)
#    S_composed     n=8 the two blocks COUPLED through the substrate arbiter
#    S_disconnected n=8 the two blocks evolving INDEPENDENTLY (coupling REMOVED)
#
#  n=8 keeps the composed system inside the faithful EXACT path (2^7=128 masks).
#
#  FROZEN bars live in .verdicts/1407_brain_lane_compose_cerebellum_basal/FREEZE.txt (NOT moved).
#  $0 CPU, gradient-free, deterministic, 3 seeds. p7/c9/a_phi_iit4_tool.
# ============================================================================
import numpy as np, sys

DIM = 64            # FNV-trigram embedding dim (matches H_1227/H_1280 dim64)
STEPS = 96          # trajectory length T (time-steps the MI matrix is built over)
SEEDS = [4700, 4701, 4702]


# ── byte-trigram FNV-1a embedding (the H_1227/H_1280 key geometry) ──────────
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
    def recall_vec(self, subj):
        if not self.keys: return np.zeros(DIM), 0.0, 0
        q = fnv_embed(subj)
        affs = np.array([float(q @ k) for k in self.keys])
        i = int(np.argmax(affs))
        return self.vals[i], float(max(0.0, affs[i])), i


# ── one episode's SUBSTRATE feature vector (H_1280 cerebellum + H_1281 basal) ──
# All DERIVED from episode structure / live store update rules — NO injected label (p6).
#   CEREBELLUM (H_1280 VForwardField forward model): keeps a running PREDICTED next-state
#   vector (EMA of recalled answer vectors); prediction error = ||actual − predicted||;
#   delta-rule correction shrinks future error; correction_drive = the error it just
#   corrected; state_novelty = how unexpected the actual state was.
#   BASAL (H_1281 VBasalGate): K competing candidates, each a go-value = grounding affinity
#   of the candidate answer to the store; go_margin = top1 − top2 go-value; competition_spread
#   = std of the K go-values; no_go_pressure = pressure to abstain (low best go-value);
#   outcome_reward = grounded(+1)/fab(−1) signal for the selected candidate.
def episode_features(store, subj, true_ans, cand_answers, rng, predicted, exposure):
    actual_vec, margin, idx = store.recall_vec(subj)

    # ── cerebellum block (H_1280) ──
    pred_error = float(np.linalg.norm(actual_vec - predicted))            # ||actual − predicted||
    pred_confidence = float(np.exp(-pred_error))                          # low error → confident
    # delta-rule correction the forward model applies (NLMS step toward actual)
    correction_drive = float(0.30 * pred_error)
    state_novelty = float(max(0.0, 1.0 - margin)) + 0.02 * rng.standard_normal()

    # ── basal-ganglia block (H_1281) ──
    # K competing candidates: go-value = affinity of each candidate-answer to the recalled state.
    go_vals = np.array([float(actual_vec @ fnv_embed(c)) for c in cand_answers])
    order = np.argsort(go_vals)[::-1]
    top1 = float(go_vals[order[0]]); top2 = float(go_vals[order[1]]) if len(go_vals) > 1 else 0.0
    go_margin = top1 - top2                                               # striatal disinhibition margin
    competition_spread = float(np.std(go_vals))
    no_go_pressure = float(max(0.0, 0.5 - top1))                          # low best go-value → abstain
    # outcome reward: was the argmax candidate the grounded (true) answer?
    sel = cand_answers[int(order[0])]
    outcome_reward = 1.0 if sel == true_ans else -1.0

    return dict(pred_error=pred_error, pred_confidence=pred_confidence,
                correction_drive=correction_drive, state_novelty=state_novelty,
                go_margin=go_margin, competition_spread=competition_spread,
                no_go_pressure=no_go_pressure, outcome_reward=outcome_reward), actual_vec


CEREBELLUM_UNITS = ["pred_error", "pred_confidence", "correction_drive", "state_novelty"]   # n=4
BASAL_UNITS      = ["go_margin", "competition_spread", "no_go_pressure", "outcome_reward"]   # n=4


def run_trajectories(seed):
    rng = np.random.default_rng(seed)
    store = ImmuneStore()
    cities = ["seoul","tokyo","paris","lima","cairo","oslo","accra","quito"]
    subjs  = ["ana","ben","cyd","dan","eli","fia","gus","hye","ivo","joo"]
    facts = {}
    for s in subjs:
        c = cities[rng.integers(0, len(cities))]
        facts[s] = c; store.bind(f"{s} lives in", c)

    cb = {u: [] for u in CEREBELLUM_UNITS}
    bg = {u: [] for u in BASAL_UNITS}
    cmp_cb = {u: [] for u in CEREBELLUM_UNITS}
    cmp_bg = {u: [] for u in BASAL_UNITS}
    dis_cb = {u: [] for u in CEREBELLUM_UNITS}
    dis_bg = {u: [] for u in BASAL_UNITS}

    exposure = {s: 0.0 for s in subjs}
    arb_state = 0.0   # the arbiter's shared decision signal (composed coupling only)
    predicted = np.zeros(DIM)   # cerebellum's running forward-model prediction (EMA)

    for t in range(STEPS):
        s = subjs[rng.integers(0, len(subjs))]
        true_ans = facts[s]
        # K=4 competing candidate answers (the true one + 3 distractor cities)
        distractors = [c for c in cities if c != true_ans]
        cand = [true_ans] + list(rng.choice(distractors, size=3, replace=False))
        rng.shuffle(cand)
        exposure[s] += 1.0
        f, actual_vec = episode_features(store, f"{s} lives in", true_ans, cand, rng, predicted, exposure[s])

        # cerebellum delta-rule: update the forward-model prediction toward the actual state
        predicted = predicted + 0.30 * (actual_vec - predicted)

        # cerebellum-alone / basal-alone  +  disconnected = SAME independent updates
        for u in CEREBELLUM_UNITS: cb[u].append(f[u]); dis_cb[u].append(f[u])
        for u in BASAL_UNITS:      bg[u].append(f[u]); dis_bg[u].append(f[u])

        # composed: substrate-weighted ARBITER (H_1401) couples the blocks.
        # cerebellum votes "trust prediction" when error low; basal votes "select winner"
        # when go_margin positive. Confidence-weighted blend → shared leaky signal.
        cb_vote = 1.0 if f["pred_error"] < 0.30 else -1.0
        cb_conf = abs(0.30 - f["pred_error"])
        bg_vote = 1.0 if f["go_margin"] > 0.0 else -1.0
        bg_conf = abs(f["go_margin"])
        denom = cb_conf + bg_conf + 1e-9
        arb = (cb_conf * cb_vote + bg_conf * bg_vote) / denom
        arb_state = 0.6 * arb_state + 0.4 * arb     # leaky integrator = shared dynamics
        g = 0.5 * (arb_state + 1.0)                  # gate in [0,1]
        # COUPLING: shared arbiter signal modulates BOTH blocks next-step. This is
        # the cross-faculty information channel the MIP cut must traverse.
        for u in CEREBELLUM_UNITS: cmp_cb[u].append(f[u] + 0.35 * g * (f[u] - 0.5))
        for u in BASAL_UNITS:      cmp_bg[u].append(f[u] + 0.35 * g * (f[u] - 0.5))

    def pack(block): return np.array([block[u] for u in block])
    return dict(
        cerebellum=pack(cb), basal=pack(bg),
        composed=np.vstack([pack(cmp_cb), pack(cmp_bg)]),
        disconnected=np.vstack([pack(dis_cb), pack(dis_bg)]),
    )


def write_states(path):
    lines = []
    for seed in SEEDS:
        tr = run_trajectories(seed)
        for name in ["cerebellum", "basal", "composed", "disconnected"]:
            M = tr[name]; n, T = M.shape
            lines.append(f"# {name}_s{seed} {n} {T}")
            for r in range(n):
                lines.append(" ".join(f"{v:.6f}" for v in M[r]))
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {path}: {len(SEEDS)} seeds x 4 systems "
          f"(cerebellum n=4, basal n=4, composed n=8, disconnected n=8)")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h1407_states.txt"
    write_states(out)
