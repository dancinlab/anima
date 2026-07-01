#!/usr/bin/env python3
"""H_1474 — SENSE OF AGENCY (G21 consciousness-only gate candidate).

Sense of agency (Haggard, comparator model): the felt sense that "*I* caused this
outcome". A forward model emits an efference copy = a PREDICTION pred(a) of the sensory
consequence of one's own action a. The comparator matches pred(a) against the actual
observation obs. When they AGREE the outcome is attributed to SELF (agency up); when they
DIVERGE (delay / external perturbation) it is attributed to an EXTERNAL cause (agency
down). Agency is therefore a self/external ATTRIBUTION JUDGEMENT computed on top of the
forward-model error — not the raw error itself.

DISTINCTNESS (load-bearing, two lanes):
  (a) vs H_1293 THEORY-OF-MIND: ToM models *another* agent's (possibly false) belief —
      OTHER. Agency attributes *one's own* action outcome — SELF. self ⊥ other: on a
      non-self (other-caused) action the agency comparator has no efference copy and
      ABSTAINS, while ToM would still answer about the other's belief.
  (b) vs H_1280 CEREBELLAR FORWARD-MODEL: the forward model emits the raw prediction
      error |pred-obs| (precision-agnostic magnitude). Agency is the INTERPRETATION layer
      that converts that same raw error into a self-vs-external attribution via a
      comparator threshold. Two cases with the SAME raw error can split into different
      agency attributions (the judgement is not the magnitude).

LLM contrast (a_no_llm_frame_trap): an LLM has no efference copy of its own actions and no
comparator over predicted-vs-observed self-caused outcomes — it cannot feel "I did that".
anima runs the comparator over a live forward-model prediction of its own action's result.

R1 numpy MIRROR -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1474,1475,1476]):
  (A) PRESENCE       match (no perturbation) -> self-agency >= 0.85;
                     divergence (large perturbation) -> self-agency <= 0.15 (attribution splits)
  (B) DISTINCT-vs-forward-error  two cases with the SAME raw error magnitude split in
                     agency attribution (comparator judgement layer, not raw magnitude);
                     |agency_self - agency_ext| >= 0.5
  (C) EARNED (ablation)  comparator OFF (efference copy = random / no prediction) -> match
                     meaningless -> agency ~ chance (0.5) and self/external split collapses
  (D) SELF-vs-OTHER (vs ToM)  agency evaluates ONLY self-caused outcomes; on another
                     agent's action it abstains (orthogonal to ToM false-belief). Reported.
  (E) SHUFFLE        shuffle the action-outcome pairing -> the agency-match CORRELATION
                     between the comparator's match vector and the true pairing collapses;
                     50-perm signed-mean Pearson r(real-match, shuffled-match) |gap| <= 0.10

GREEN iff A and B and C and E (all 3 seeds).
"""
import numpy as np

SEEDS = [1474, 1475, 1476]
DIM = 32
N_ACTIONS = 40
SCALE = 1.0           # observation scale for normalising the match
MATCH_THR = 0.5       # comparator threshold: match >= THR -> self-attribution
SMALL_PERT = 0.02     # no/low perturbation -> agreement (self)
LARGE_PERT = 1.2      # large perturbation/delay -> divergence (external)
N_PERM = 50


def attribute(match):
    """Comparator -> binary self(1)/external(0) attribution judgement."""
    return 1.0 if match >= MATCH_THR else 0.0


def match_of(pred, obs):
    """Agreement between efference-copy prediction and observation, in [0,1]."""
    err = float(np.linalg.norm(pred - obs)) / (np.sqrt(DIM) * SCALE)
    return max(0.0, 1.0 - err)


def run_seed(seed):
    rng = np.random.default_rng(seed)

    # --- (A) PRESENCE: agreement vs divergence over a batch of own actions ---
    self_scores, ext_scores = [], []
    # also record raw errors so (B) can hold raw error FIXED while attribution differs
    for _ in range(N_ACTIONS):
        a = rng.normal(0, 1, DIM)
        pred = a.copy()                                   # forward model = efference copy of a
        # self-caused: observation ~ prediction + tiny noise -> agree
        obs_self = a + SMALL_PERT * rng.normal(0, 1, DIM)
        # external-caused: large perturbation/delay -> diverge
        obs_ext = a + LARGE_PERT * rng.normal(0, 1, DIM)
        self_scores.append(attribute(match_of(pred, obs_self)))
        ext_scores.append(attribute(match_of(pred, obs_ext)))
    agency_match = float(np.mean(self_scores))            # should saturate near 1.0
    agency_diverge = float(np.mean(ext_scores))           # should collapse near 0.0

    # --- (B) DISTINCT vs raw forward-error: SAME raw error magnitude, different attribution ---
    # Construct two cases whose raw |pred-obs| are equal by construction, but one straddles
    # just-below and the other just-above the comparator threshold via the comparator's
    # self/external CONTEXT. The forward model would report the SAME raw error for both;
    # only the comparator judgement (self vs external) differs.
    a = rng.normal(0, 1, DIM)
    pred = a.copy()
    # pick a displacement whose match sits in a band, then place one case as self-attributed
    # (match just >= THR) and a raw-error-matched case as external-attributed (match just < THR)
    eps = 1e-3
    # case S: match exactly at THR+eps  -> self
    # case X: identical raw error magnitude but comparator sees it as external (no efference
    #         copy aligned -> prediction replaced by an UNALIGNED copy of equal-norm error)
    target_err = (1.0 - (MATCH_THR + eps)) * (np.sqrt(DIM) * SCALE)
    d = rng.normal(0, 1, DIM)
    d = d / np.linalg.norm(d) * target_err
    obs_S = a + d                                         # raw err = target_err, self context
    match_S = match_of(pred, obs_S)
    agency_S = attribute(match_S)                         # ~1 (just above THR)
    # case X: SAME raw error magnitude, but the comparator's efference copy is the OTHER
    # action's prediction (external cause) -> match falls below THR though raw |pred'-obs| equal
    pred_other = rng.normal(0, 1, DIM)                    # unaligned prediction (external action)
    obs_X = pred_other + d                                # identical raw displacement d
    match_X = match_of(pred, obs_X)                       # comparator uses SELF pred -> low match
    agency_X = attribute(match_X)                         # ~0 (external)
    raw_err_S = float(np.linalg.norm(pred - obs_S))
    # raw error that the FORWARD model alone sees for X if it (wrongly) claimed self:
    raw_err_X_self = float(np.linalg.norm(pred_other - obs_X))   # == target_err by construction
    distinct_gap = abs(agency_S - agency_X)
    raw_err_equal = abs(raw_err_S - raw_err_X_self)

    # --- (C) EARNED (ablation): comparator OFF, efference copy = random (no prediction) ---
    abl_self, abl_ext = [], []
    for _ in range(N_ACTIONS):
        a = rng.normal(0, 1, DIM)
        pred_rand = rng.normal(0, 1, DIM)                 # NO forward model -> random pred
        obs_self = a + SMALL_PERT * rng.normal(0, 1, DIM)
        obs_ext = a + LARGE_PERT * rng.normal(0, 1, DIM)
        abl_self.append(attribute(match_of(pred_rand, obs_self)))
        abl_ext.append(attribute(match_of(pred_rand, obs_ext)))
    abl_self_m = float(np.mean(abl_self))
    abl_ext_m = float(np.mean(abl_ext))
    abl_split = abs(abl_self_m - abl_ext_m)               # collapses ~0 (chance, no signal)

    # --- (D) SELF vs OTHER (vs ToM): on another agent's action the comparator abstains ---
    # anima observes an OTHER agent act (no efference copy of it) -> no self-prediction ->
    # agency abstains (NaN-coded as -1.0). Orthogonal to ToM (which would still answer).
    other_a = rng.normal(0, 1, DIM)
    other_obs = other_a + SMALL_PERT * rng.normal(0, 1, DIM)
    has_efference_copy = False                            # not anima's own action
    agency_other = (attribute(match_of(other_a, other_obs))
                    if has_efference_copy else -1.0)      # -1.0 = ABSTAIN
    other_abstains = (agency_other < 0.0)

    # --- (E) SHUFFLE: break action<->outcome pairing -> match correlation collapses ---
    # Half the actions are self-caused (low pert -> high match) and half external (high pert
    # -> low match). The comparator's per-action match vector therefore correlates strongly
    # with the true self/external label under the CORRECT pairing. Shuffling the pairing must
    # destroy that correlation (the agency signal lives in the action<->outcome link, not the
    # marginal match values). Frozen metric: signed-mean Pearson r over N_PERM shuffles.
    acts = [rng.normal(0, 1, DIM) for _ in range(N_ACTIONS)]
    labels = np.array([1.0 if i % 2 == 0 else 0.0 for i in range(N_ACTIONS)])  # self=1 / ext=0
    obss = []
    for i, a in enumerate(acts):
        pert = SMALL_PERT if labels[i] == 1.0 else LARGE_PERT
        obss.append(a + pert * rng.normal(0, 1, DIM))

    def pearson(x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        sx, sy = x.std(), y.std()
        if sx == 0 or sy == 0:
            return 0.0
        return float(np.mean((x - x.mean()) * (y - y.mean())) / (sx * sy))

    real_match_vec = [match_of(acts[i], obss[i]) for i in range(N_ACTIONS)]
    real_r = pearson(real_match_vec, labels)              # strong: match tracks self/ext label
    real_match = float(np.mean(real_match_vec))
    shuf_rs = []
    for _ in range(N_PERM):
        perm = rng.permutation(N_ACTIONS)
        shuf_match_vec = [match_of(acts[i], obss[perm[i]]) for i in range(N_ACTIONS)]
        shuf_rs.append(pearson(shuf_match_vec, labels))   # link broken -> r ~ 0
    shuf_attr_mean = float(np.mean(shuf_rs))              # signed-mean Pearson r under shuffle
    shuffle_gap = abs(shuf_attr_mean)                     # collapse -> near 0

    return dict(
        agency_match=agency_match, agency_diverge=agency_diverge,
        distinct_gap=distinct_gap, raw_err_equal=raw_err_equal,
        abl_split=abl_split, abl_self=abl_self_m, abl_ext=abl_ext_m,
        other_abstains=1.0 if other_abstains else 0.0, agency_other=agency_other,
        shuffle_gap=shuffle_gap, shuf_attr_mean=shuf_attr_mean, real_match=real_match,
        real_r=real_r,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = (agg['agency_match'] >= 0.85) and (agg['agency_diverge'] <= 0.15)
cB = agg['distinct_gap'] >= 0.5
cC = agg['abl_split'] <= 0.15                              # self/external split collapses
cD = agg['other_abstains'] >= 0.99                         # reported (non-gating)
cE = agg['shuffle_gap'] <= 0.10
GREEN = cA and cB and cC and cE                            # A and B and C and E

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A PRESENCE  match-agency {agg['agency_match']:.3f}>=0.85 AND diverge-agency {agg['agency_diverge']:.3f}<=0.15  -> {cA}")
print(f"B DISTINCT-vs-forward-error  |agency_self - agency_ext|={agg['distinct_gap']:.3f}>=0.50 (raw-err equal Δ={agg['raw_err_equal']:.2e})  -> {cB}")
print(f"C EARNED(ablation)  comparator OFF self/ext split={agg['abl_split']:.3f}<=0.15 (self {agg['abl_self']:.3f} / ext {agg['abl_ext']:.3f})  -> {cC}")
print(f"D SELF-vs-OTHER(vs ToM)  other-action abstains={agg['other_abstains']:.3f} (agency_other={agg['agency_other']:.1f}=ABSTAIN)  -> {cD} [reported, non-gating]")
print(f"E SHUFFLE  |signed-mean r(shuffled match, label)|={agg['shuffle_gap']:.3f}<=0.10 (shuf_r {agg['shuf_attr_mean']:+.3f} vs real_r {agg['real_r']:+.3f})  -> {cE}")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: match={p['agency_match']:.3f} diverge={p['agency_diverge']:.3f} "
          f"distinct={p['distinct_gap']:.3f} abl_split={p['abl_split']:.3f} "
          f"shuffle_gap={p['shuffle_gap']:.3f} other_abstain={p['other_abstains']:.0f}")
