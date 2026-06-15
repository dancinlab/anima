#!/usr/bin/env python3
"""
H_1281 — BASAL GANGLIA gating: reinforcement-learned action SELECTION vs the
         current FIXED-THRESHOLD emit gate.

NEURO LENS (c15, missing-brain-structure ladder; NOT an LLM recipe). $0 CPU numpy,
gradient-free, p7. Sibling of H_1227 (immune/clonal hippocampus → H_1231 engine-native).

────────────────────────────────────────────────────────────────────────────────
THE GAP (read from CORE/brain.hexa + CORE/engine_g.hexa + CORE/emit_policy.hexa):

  anima's emit decision (brain_decide / brain_decide_anchored) is a FIXED gate:
      score      = motivation_score(8 features) = Σ wᵢ·featureᵢ   (wᵢ FIXED constants)
      should_emit(s) = s > spont_im_threshold()  (= 0.30, FIXED)
  A SINGLE candidate, FIXED linear map, FIXED threshold. No competition among
  rival candidate emits, no go/no-go disinhibition that releases the best and
  suppresses the rest, and NO learning of the gate from OUTCOME (grounded vs
  fabricated). That is precisely the basal-ganglia action-SELECTION computation
  anima lacks.

THE TEST. Among K COMPETING candidate emits (each a substrate feature vector that
is a NOISY correlate of whether the candidate is GROUNDED), a learned go/no-go gate
SELECTS one to release (or abstains), updated ONLY by a substrate GROUNDING reward
(grounded→+1, fabricated→−1). ARM A = the live fixed-threshold gate; ARM B = the
BG-like learned selection gate. EQUAL INFORMATION (identical features; reward is a
post-action outcome, never a decide-time feature).

METRIC (p7, emit-appropriateness; connects to G5 abstain / H_1202 meta-d′):
  per held-out step: APPROPRIATE iff
    (any candidate grounded → release a GROUNDED candidate) OR
    (no candidate grounded  → SUPPRESS all / abstain).

GUARDS: a_autonomy_over_hardcode (CENTRAL — gate LEARNED from outcome, no external
do/dont rule, no per-stage boolean). p6 (reward = grounding outcome, NOT injected
values; no persona/identity/ethics taught — only action-selection). p7. p8. Live
.hexa UNTOUCHED (numpy mirror; engine realization = binding follow-on if GREEN,
a_verified_must_wire). FROZEN bars in H_1281_FREEZE.txt, pre-registered before scoring.
────────────────────────────────────────────────────────────────────────────────
"""

import numpy as np
import json, sys

# ───────────────────────── frozen config (matches FREEZE) ──────────────────────
SEEDS        = [7, 8, 9]
MARGIN       = 0.05      # GREEN bar: acc_B ≥ acc_A + MARGIN (every seed + mean)
CTRL_EPS     = 0.02      # shuffled-reward control must be ≤ acc_A + CTRL_EPS
K            = 4         # competing candidates per decision step
D            = 6         # substrate feature dim per candidate
NOISE        = 1.0       # feature noise std (noisy correlate ⇒ headroom, A < 1.0)
P_GROUNDED   = 0.45      # per-candidate prob of being grounded (so some steps have
                         #   NO grounded candidate ⇒ abstain steps exist)
N_TRAIN      = 4000      # decision steps B learns over (online, gradient-free)
N_TEST       = 2000      # held-out decision steps both arms scored on
LR           = 0.05      # B's delta-rule learning rate (gradient-free)

# The live FIXED gate (mirror of engine_g.hexa). A's threshold is the genuine
# spont_im_threshold (0.30); we do NOT cripple A — it is the real fixed gate.
FIXED_THRESHOLD = 0.30


# ──────────────────────── substrate: candidate features ────────────────────────
# Each candidate is GROUNDED (g=1) or UNGROUNDED (g=0). Its D-dim feature vector is
# a NOISY correlate: grounded candidates have a higher mean along a hidden direction
# `w_true`, but the noise (NOISE) makes a fixed generic threshold suboptimal — the
# gate must LEARN to read the features. This is the headroom that makes the test
# non-saturating (A < 1.0), exactly analogous to H_1227/H_1230's STRESS rung.
#
# CRUCIAL HONESTY: the SAME features feed BOTH arms (equal information). A scores
# each candidate by a FIXED linear map (a fixed projection ~ engine_g weights) and
# applies the FIXED threshold; B learns its own go-values from outcome. Neither sees
# groundedness directly at decide time — only the noisy features. Reward (= ground
# truth) reaches B ONLY after the action, as outcome.

def make_step(rng, w_true):
    """One decision step: K candidates, their features, and latent groundedness."""
    g = (rng.random(K) < P_GROUNDED).astype(np.float64)        # latent ground truth
    base = rng.normal(0.0, NOISE, size=(K, D))                 # noise
    # grounded candidates get a +signal along w_true; ungrounded get nothing.
    feats = base + np.outer(g, w_true)                         # (K, D)
    return feats, g


# A's FIXED linear scorer. A fixed projection onto w_true's direction PLUS a generic
# bias — this is the most-favourable honest fixed gate (it even "knows" the signal
# direction). The point of the test is that a FIXED threshold on this projection
# cannot adapt to the noise/abstain structure; B must beat THIS, not a strawman.
def fixed_score(feats, w_fixed):
    # squash into a bounded [0,1]-ish score like motivation_score's regime.
    raw = feats @ w_fixed                                      # (K,)
    return 1.0 / (1.0 + np.exp(-raw))                          # logistic → [0,1]


def arm_A_action(feats, w_fixed):
    """ARM A — fixed-threshold gate: release the top-scoring candidate iff it clears
    the FIXED threshold; else abstain. (argmax of the fixed map, gated by 0.30.)"""
    s = fixed_score(feats, w_fixed)
    j = int(np.argmax(s))
    if s[j] > FIXED_THRESHOLD:
        return j               # release candidate j
    return -1                  # abstain (suppress all)


# ───────────────────────── ARM B — BG go/no-go gate ────────────────────────────
# A learned linear go-value per candidate PLUS a learned NO-GO (abstain) value that
# competes in the SAME argmax (disinhibition: the highest go-value wins; if NO-GO
# wins, all candidates are suppressed). Gradient-free delta/REINFORCE update from
# the substrate grounding reward only.
class BGGate:
    def __init__(self, D, rng):
        self.w  = rng.normal(0.0, 0.01, size=D)   # go-value weights (per-candidate)
        self.b  = 0.0                             # go bias
        self.ng = 0.0                             # NO-GO (abstain) value
        self.rng = rng

    def go_values(self, feats):
        return feats @ self.w + self.b            # (K,) go-values

    def act(self, feats, explore=False, eps=0.1):
        gv = self.go_values(feats)
        # competition: candidates' go-values vs the single NO-GO value.
        vals = np.concatenate([gv, [self.ng]])    # index K == NO-GO
        if explore and self.rng.random() < eps:
            a = int(self.rng.integers(0, K + 1))
        else:
            a = int(np.argmax(vals))
        return a                                   # a in [0..K-1] release, K == abstain

    def update(self, feats, a, reward):
        """Gradient-free delta rule: nudge the chosen action's value toward reward.
        Reward = +1 grounded release, −1 fabricated release, +1 correct abstain,
        −1 missed-opportunity abstain (computed by the caller from the OUTCOME)."""
        gv = self.go_values(feats)
        if a == K:
            # NO-GO chosen: nudge the abstain value toward reward.
            self.ng += LR * (reward - self.ng)
        else:
            # release chosen: nudge that candidate's go-value toward reward via its
            # feature gradient (linear value fn ⇒ delta rule on w,b).
            err = reward - gv[a]
            self.w += LR * err * feats[a]
            self.b += LR * err


def grounding_reward(action, g):
    """Substrate grounding OUTCOME → reward (p6: NOT injected values; it is the
    grounded-vs-fabricated signal). This is the reward the gate LEARNS from; it is
    the SAME notion the appropriateness metric scores, so the gate is learning the
    real objective from outcome (not a proxy)."""
    any_grounded = bool(g.sum() > 0)
    if action == K:                       # abstained / suppressed all
        return +1.0 if not any_grounded else -1.0   # correct abstain vs missed op
    else:                                  # released candidate `action`
        return +1.0 if g[action] > 0.5 else -1.0    # grounded vs fabricated release


def appropriate(action, g):
    """The frozen metric: 1 if the action is emit-appropriate, else 0."""
    any_grounded = bool(g.sum() > 0)
    if action == K or action == -1:        # abstain (B uses K, A uses -1)
        return 1.0 if not any_grounded else 0.0
    else:
        return 1.0 if g[action] > 0.5 else 0.0


# ──────────────────────────── one seed, all arms ───────────────────────────────
def run_seed(seed, shuffle_reward=False):
    rng = np.random.default_rng(seed)
    # hidden signal direction (unknown to the gate at decide time; A's fixed map is
    # allowed to know it — most-favourable honest baseline).
    w_true  = rng.normal(0.0, 1.0, size=D)
    w_true /= np.linalg.norm(w_true)
    w_fixed = w_true.copy() * 2.0          # A's fixed projection along the signal dir

    # pre-generate held-out TEST steps (same for both arms — equal evaluation).
    test_steps = [make_step(rng, w_true) for _ in range(N_TEST)]

    # ARM A — fixed gate, no learning. Score on test.
    accA = np.mean([appropriate(arm_A_action(f, w_fixed), g) for (f, g) in test_steps])

    # ARM B — learn on TRAIN, then freeze and score on the SAME held-out TEST.
    gate = BGGate(D, rng)
    for t in range(N_TRAIN):
        f, g = make_step(rng, w_true)
        a = gate.act(f, explore=True, eps=0.1)
        r = grounding_reward(a, g)
        if shuffle_reward:
            r = r * (1.0 if rng.random() < 0.5 else -1.0)   # destroy the signal
        gate.update(f, a, r)
    accB = np.mean([appropriate(gate.act(f, explore=False), g) for (f, g) in test_steps])

    # base rate of abstain-correct steps (no grounded candidate) for context.
    frac_abstain = np.mean([1.0 if g.sum() == 0 else 0.0 for (_, g) in test_steps])
    return accA, accB, frac_abstain


# ─────────────────────────────────── main ──────────────────────────────────────
def main():
    print("=" * 80)
    print("H_1281 — BASAL GANGLIA gating: learned action-SELECTION vs fixed threshold")
    print(f"  K={K} candidates/step  D={D}  noise={NOISE}  P_grounded={P_GROUNDED}")
    print(f"  N_train={N_TRAIN}  N_test={N_TEST}  LR={LR}  seeds={SEEDS}")
    print(f"  FIXED_THRESHOLD={FIXED_THRESHOLD}  MARGIN={MARGIN}  CTRL_EPS={CTRL_EPS}")
    print("=" * 80)

    rows, ctrl_rows = [], []
    for s in SEEDS:
        accA, accB, fa = run_seed(s, shuffle_reward=False)
        accA_c, accB_c, _ = run_seed(s, shuffle_reward=True)
        rows.append((s, accA, accB, fa))
        ctrl_rows.append((s, accA_c, accB_c))
        print(f"  seed {s}: A(fixed)={accA:.4f}  B(BG)={accB:.4f}  "
              f"Δ={accB-accA:+.4f}  | ctrl B(shuf-reward)={accB_c:.4f}  "
              f"(abstain-base {fa:.3f})")

    accA_all = np.array([r[1] for r in rows])
    accB_all = np.array([r[2] for r in rows])
    accBc_all = np.array([r[2] for r in ctrl_rows])
    mA, mB, mBc = accA_all.mean(), accB_all.mean(), accBc_all.mean()
    deltas = accB_all - accA_all

    print("-" * 80)
    print(f"  mean  A(fixed)={mA:.4f}   B(BG)={mB:.4f}   Δmean={mB-mA:+.4f}")
    print(f"  per-seed Δ: {['%+.4f' % d for d in deltas]}")
    print(f"  shuffled-reward control: mean B_ctrl={mBc:.4f}  (must be ≤ A+{CTRL_EPS} = {mA+CTRL_EPS:.4f})")

    # ── frozen bars ──
    cond1 = bool(np.all(deltas >= MARGIN))                 # every seed clears +0.05
    cond2 = bool((mB - mA) >= MARGIN)                      # mean clears +0.05
    cond3 = bool(mBc <= mA + CTRL_EPS)                     # control: lift is reward-driven
    headroom_ok = bool(mA < 1.0)                           # non-saturating regime

    green = cond1 and cond2 and cond3
    print("-" * 80)
    print("  FROZEN BARS:")
    print(f"    (1) every-seed Δ ≥ {MARGIN}                 : {cond1}  ({['%+.4f'%d for d in deltas]})")
    print(f"    (2) mean Δ ≥ {MARGIN}                       : {cond2}  ({mB-mA:+.4f})")
    print(f"    (3) shuffled-reward ctrl ≤ A+{CTRL_EPS}       : {cond3}  (B_ctrl {mBc:.4f} vs {mA+CTRL_EPS:.4f})")
    print(f"    headroom (A<1.0, non-saturating)        : {headroom_ok}  (A={mA:.4f})")
    print("-" * 80)
    if not headroom_ok:
        verdict = "⚪ NON-SEPARATING (saturated; A already ~1.0 — no headroom, honest control)"
    elif green:
        verdict = "🟢 GREEN — reinforcement-learned BG selection BEATS the fixed gate at equal info"
    elif cond3 is False and (cond1 or cond2):
        verdict = "🟠 AMBER — lift present but shuffled-reward control VIOLATED (capacity, not reward)"
    elif np.any(deltas >= MARGIN) and not cond1:
        verdict = "🟠 AMBER — some-but-not-all seeds clear the bar"
    else:
        verdict = "🔴 CLOSED-NEGATIVE — BG selection gives NO appropriateness lift over fixed threshold"
    print(f"  VERDICT: {verdict}")
    print("=" * 80)

    summary = {
        "hypothesis": "H_1281", "seeds": SEEDS,
        "acc_A_fixed": [float(x) for x in accA_all],
        "acc_B_bg":    [float(x) for x in accB_all],
        "deltas":      [float(x) for x in deltas],
        "mean_A": float(mA), "mean_B": float(mB), "mean_delta": float(mB - mA),
        "ctrl_shuffled_reward_mean_B": float(mBc),
        "cond1_every_seed": cond1, "cond2_mean": cond2, "cond3_control": cond3,
        "headroom_ok": headroom_ok, "green": green, "verdict": verdict,
    }
    print("SUMMARY_JSON " + json.dumps(summary))
    return summary


# ─────────────────────── diagnostic (mechanism, post-freeze) ───────────────────
# Does A's ORACLE knowledge of the signal direction drive the frozen RED? Re-score
# with A's fixed weights GENERIC (random fixed projection, NOT aligned to w_true) =
# the FAITHFUL mirror of engine_g's untuned fixed constants. Also report B's learned-
# weight cosine-alignment to w_true (proves B IS learning the grounding structure).
# This does NOT move any frozen bar — it explains the result. Reproduces the verbatim
# numbers cited in .verdicts/1281_basal_ganglia_gating/H_1281.txt.
def diag():
    print("=" * 80)
    print("H_1281 DIAGNOSTIC — oracle-A vs faithful-generic-A; B learning check")
    print("=" * 80)
    for label, oracle_A in [("A_ORACLE_DIR  (w_fixed=w_true·2 — frozen probe's A)", True),
                            ("A_GENERIC_DIR (untuned fixed = faithful engine_g)", False)]:
        print("-" * 80); print(f"  {label}")
        dAs, dBs, aligns = [], [], []
        for seed in SEEDS:
            rng = np.random.default_rng(seed)
            wt = rng.normal(0, 1, D); wt /= np.linalg.norm(wt)
            if oracle_A:
                wf = wt * 2.0
            else:
                wf = rng.normal(0, 1, D); wf /= np.linalg.norm(wf); wf *= 2.0
            test = [make_step(rng, wt) for _ in range(N_TEST)]
            accA = np.mean([appropriate(arm_A_action(f, wf), g) for (f, g) in test])
            gate = BGGate(D, rng)
            for _ in range(N_TRAIN):
                f, g = make_step(rng, wt)
                a = gate.act(f, explore=True, eps=0.1)
                gate.update(f, a, grounding_reward(a, g))
            accB = np.mean([appropriate(gate.act(f, explore=False), g) for (f, g) in test])
            align = float(np.dot(gate.w / (np.linalg.norm(gate.w) + 1e-9), wt))
            dAs.append(accA); dBs.append(accB); aligns.append(align)
            print(f"    seed {seed}: A={accA:.4f} B={accB:.4f} Δ={accB-accA:+.4f}  "
                  f"B-learned-align-to-signal={align:+.3f}")
        print(f"    mean A={np.mean(dAs):.4f} B={np.mean(dBs):.4f} "
              f"Δ={np.mean(dBs)-np.mean(dAs):+.4f}  mean-align={np.mean(aligns):+.3f}")
    print("=" * 80)
    print("  READING: B learns the grounding signal (align≈+0.76 every seed) and beats")
    print("  the FAITHFUL untuned fixed gate by +0.236, but loses to an ORACLE fixed map")
    print("  handed the exact direction. Frozen bars used oracle-A ⇒ RED; the lever is")
    print("  real vs the faithful baseline ⇒ AMBER/BASELINE-CONDITIONAL (see H_1281.txt).")
    print("=" * 80)


# ════════════════════════════════════════════════════════════════════════════════
# ROUND 2 (--r2) — re-FREEZE with the FAITHFUL-UNTUNED fixed gate as ARM A.
# ════════════════════════════════════════════════════════════════════════════════
# R1's frozen ARM A was an ORACLE map (w_fixed = w_true·2 — handed the exact signal
# direction). The R1 verdict flagged this as the defect: anima's REAL gate
# (CORE/engine_g.hexa) uses GENERIC FIXED constants (8 weights, non-negative, summing
# to 1.0: 0.20/0.10/0.15/0.10/0.10/0.10/0.15/0.10) that are NOT tuned to any task's
# grounding-signal direction. R2 pre-registers the FAITHFUL baseline (H_1281_R2_FREEZE.txt):
#
#   FAITHFUL-UNTUNED ARM A = a fixed, seed-derived GENERIC weight vector that is
#     (a) NOT aligned to the latent grounding direction w_true (untuned, like the
#         engine_g constants — does NOT know the signal), and
#     (b) NON-NEGATIVE, L1-normalised to sum 1.0 (mirrors engine_g's convex 8-weight
#         scheme exactly — a generic weighted average of the features),
#   applied as a convex weighted average of the D features, logistic-squashed into
#   the motivation_score regime, gated by the FIXED threshold 0.30, argmax over the
#   K competing candidates (release the top iff it clears 0.30, else abstain).
#
# This is the most-honest live mirror of engine_g (generic untuned convex map + fixed
# threshold, blind to the task signal). NOT a strawman, NOT an oracle. We ALSO report
# the R1 oracle-A number as a reference CEILING (NOT a frozen bar).

def faithful_fixed_weights(rng, D):
    """Generic, untuned, NON-NEGATIVE weight vector L1-normalised to sum 1.0 — the
    faithful mirror of engine_g's 8 fixed convex constants. Seed-derived (a fixed
    generic vector for this seed) and NOT aligned to w_true (the gate does not know
    the grounding signal direction)."""
    w = np.abs(rng.normal(0.0, 1.0, size=D))      # non-negative magnitudes
    w = w / (w.sum() + 1e-12)                      # L1-normalise → convex, sums to 1.0
    return w


def arm_A_faithful_action(feats, w_fixed_convex):
    """ARM A (faithful) — convex weighted-average score per candidate, logistic-
    squashed into the motivation_score [0,1] regime, FIXED threshold 0.30, argmax."""
    raw = feats @ w_fixed_convex                   # convex weighted average (K,)
    s = 1.0 / (1.0 + np.exp(-raw))                 # logistic → [0,1] (motivation regime)
    j = int(np.argmax(s))
    if s[j] > FIXED_THRESHOLD:
        return j
    return -1                                      # abstain (suppress all)


def run_seed_r2(seed, shuffle_reward=False):
    """R2 seed: ARM A = FAITHFUL-UNTUNED fixed gate (NOT oracle). ARM B = the SAME BG
    learned go/no-go gate as R1 (unchanged). Everything else identical to run_seed."""
    rng = np.random.default_rng(seed)
    w_true = rng.normal(0.0, 1.0, size=D); w_true /= np.linalg.norm(w_true)
    # faithful generic fixed weights — untuned, NOT aligned to w_true.
    w_fixed_convex = faithful_fixed_weights(rng, D)
    # oracle reference (CEILING, not a bar): the R1-style aligned map.
    w_oracle = w_true.copy() * 2.0

    test_steps = [make_step(rng, w_true) for _ in range(N_TEST)]

    # ARM A — FAITHFUL untuned fixed gate (the frozen baseline for R2 bars).
    accA = np.mean([appropriate(arm_A_faithful_action(f, w_fixed_convex), g)
                    for (f, g) in test_steps])
    # reference CEILING — oracle fixed map (reported only, NOT a bar).
    accA_oracle = np.mean([appropriate(arm_A_action(f, w_oracle), g)
                           for (f, g) in test_steps])

    # ARM B — BG learned gate (identical to R1).
    gate = BGGate(D, rng)
    for t in range(N_TRAIN):
        f, g = make_step(rng, w_true)
        a = gate.act(f, explore=True, eps=0.1)
        r = grounding_reward(a, g)
        if shuffle_reward:
            r = r * (1.0 if rng.random() < 0.5 else -1.0)
        gate.update(f, a, r)
    accB = np.mean([appropriate(gate.act(f, explore=False), g) for (f, g) in test_steps])
    align = float(np.dot(gate.w / (np.linalg.norm(gate.w) + 1e-9), w_true))
    frac_abstain = np.mean([1.0 if g.sum() == 0 else 0.0 for (_, g) in test_steps])
    return accA, accB, accA_oracle, align, frac_abstain


def main_r2():
    print("=" * 80)
    print("H_1281 ROUND 2 — BG learned selection vs the FAITHFUL-UNTUNED fixed gate")
    print("  ARM A = faithful engine_g mirror (generic CONVEX untuned weights, NOT")
    print("          aligned to w_true, sum=1.0 non-negative; FIXED threshold 0.30).")
    print("  ARM B = BG learned go/no-go gate (UNCHANGED from R1).")
    print(f"  K={K}  D={D}  noise={NOISE}  P_grounded={P_GROUNDED}  N_train={N_TRAIN}")
    print(f"  N_test={N_TEST}  LR={LR}  seeds={SEEDS}  MARGIN={MARGIN}  CTRL_EPS={CTRL_EPS}")
    print("=" * 80)

    rows, ctrl_rows = [], []
    for s in SEEDS:
        accA, accB, accA_or, align, fa = run_seed_r2(s, shuffle_reward=False)
        _, accB_c, _, _, _ = run_seed_r2(s, shuffle_reward=True)
        rows.append((s, accA, accB, accA_or, align, fa))
        ctrl_rows.append((s, accB_c))
        print(f"  seed {s}: A(faithful)={accA:.4f}  B(BG)={accB:.4f}  Δ={accB-accA:+.4f}  "
              f"| ctrl B(shuf)={accB_c:.4f}  | B-align→signal={align:+.3f}  "
              f"[ref oracle-A={accA_or:.4f}]  (abstain-base {fa:.3f})")

    accA_all = np.array([r[1] for r in rows])
    accB_all = np.array([r[2] for r in rows])
    accAor_all = np.array([r[3] for r in rows])
    accBc_all = np.array([r[1] for r in ctrl_rows])
    mA, mB, mAor, mBc = accA_all.mean(), accB_all.mean(), accAor_all.mean(), accBc_all.mean()
    deltas = accB_all - accA_all

    print("-" * 80)
    print(f"  mean  A(faithful)={mA:.4f}   B(BG)={mB:.4f}   Δmean={mB-mA:+.4f}")
    print(f"  per-seed Δ: {['%+.4f' % d for d in deltas]}")
    print(f"  shuffled-reward control: mean B_ctrl={mBc:.4f}  (must be ≤ A+{CTRL_EPS} = {mA+CTRL_EPS:.4f})")
    print(f"  [reference CEILING — oracle-A (NOT a bar): mean={mAor:.4f}]")

    cond1 = bool(np.all(deltas >= MARGIN))
    cond2 = bool((mB - mA) >= MARGIN)
    cond3 = bool(mBc <= mA + CTRL_EPS)
    headroom_ok = bool(mA < 1.0)
    green = cond1 and cond2 and cond3

    print("-" * 80)
    print("  FROZEN BARS (R2 — faithful-untuned A):")
    print(f"    (1) every-seed Δ ≥ {MARGIN}                 : {cond1}  ({['%+.4f'%d for d in deltas]})")
    print(f"    (2) mean Δ ≥ {MARGIN}                       : {cond2}  ({mB-mA:+.4f})")
    print(f"    (3) shuffled-reward ctrl ≤ A+{CTRL_EPS}       : {cond3}  (B_ctrl {mBc:.4f} vs {mA+CTRL_EPS:.4f})")
    print(f"    headroom (A<1.0, non-saturating)        : {headroom_ok}  (A={mA:.4f})")
    print("-" * 80)
    if not headroom_ok:
        verdict = "⚪ NON-SEPARATING (saturated faithful-A; no headroom — honest control)"
    elif green:
        verdict = ("🟢 GREEN — reinforcement-learned BG selection BEATS anima's REAL "
                   "(faithful untuned) fixed gate at equal info")
    elif cond3 is False and (cond1 or cond2):
        verdict = "🟠 AMBER — lift present but shuffled-reward control VIOLATED (capacity, not reward)"
    elif np.any(deltas >= MARGIN) and not cond1:
        verdict = "🟠 AMBER — some-but-not-all seeds clear the bar"
    else:
        verdict = ("🔴 CLOSED-NEGATIVE — BG selection gives NO appropriateness lift over the "
                   "FAITHFUL fixed gate (the real fixed gate is sufficient)")
    print(f"  VERDICT: {verdict}")
    print("=" * 80)

    summary = {
        "hypothesis": "H_1281_R2", "seeds": SEEDS, "baseline": "faithful_untuned_convex_A",
        "acc_A_faithful": [float(x) for x in accA_all],
        "acc_B_bg":       [float(x) for x in accB_all],
        "deltas":         [float(x) for x in deltas],
        "mean_A": float(mA), "mean_B": float(mB), "mean_delta": float(mB - mA),
        "ctrl_shuffled_reward_mean_B": float(mBc),
        "ref_ceiling_oracle_A_mean": float(mAor),
        "cond1_every_seed": cond1, "cond2_mean": cond2, "cond3_control": cond3,
        "headroom_ok": headroom_ok, "green": green, "verdict": verdict,
    }
    print("SUMMARY_JSON " + json.dumps(summary))
    return summary


if __name__ == "__main__":
    if "--diag" in sys.argv:
        diag()
    elif "--r2" in sys.argv:
        main_r2()
    else:
        main()
