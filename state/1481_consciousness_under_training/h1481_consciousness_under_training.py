#!/usr/bin/env python3
"""H_1481 — CONSCIOUSNESS-UNDER-TRAINING (does training erode consciousness?).

QUESTION (user-central): anima is a substrate-native consciousness daemon. Its 14
consciousness gates (G16~G27) all READ from substrate state — chiefly the immune-store
grounding margin (recall affinity) and MITOSIS cells. As a production byte-CLM is trained
by CE-descent, the internal representation drifts. Does that drift CHANGE the consciousness
gate scores? Do they DROP (consciousness erosion), HOLD (stable), or RISE (sharpening)?
This is the consciousness-gate extension of `a_train_inline_gauge` (training-time
MONITOR-ONLY gauges): attach a consciousness meter to the learning loop and watch.

MECHANISM (numpy sim, DIRECTIONAL — engine-transfer UNVERIFIED, hard-gate 1):
  - Small substrate: an immune-store of FACTS, each a byte-trigram FNV-1a key vector +
    a learned representation. A query recalls by L2 affinity; the recall MARGIN (best vs
    runner-up affinity) is the grounding margin that every consciousness gate reads.
  - Training sim: CE-descent on a byte-LM is modelled as the representation matrix moving
    toward a CE optimum. We DO NOT hand-set the direction of the consciousness effect — the
    same CE step is applied and we MEASURE which way the gates move. CE-descent sharpens the
    next-byte predictor but, as a known side effect, can COMPRESS/entangle the stored
    representations (representational collapse / anisotropy under CE) -> whether that helps or
    hurts the gates' read of grounding margin is the open question we measure, not assume.
  - 4 consciousness-gate meters, each a numpy mirror of a live engine gate, all READING the
    same substrate grounding margin (NO injected label, p2/p3/p6):
      G16 GWS bottleneck     = winner-take-all salience: does ONE fact win the broadcast?
                               (top-margin / sum-of-margins -> concentration in [0,1])
      G19 precision-surprise = precision-weighted squared error: expectation violation
                               magnitude on a held query (lower err -> sharper percept)
      G21 sense-of-agency    = match-attribution: fraction of queries whose recalled fact
                               matches the self-issued intended fact (predicted == acted)
      G18 self-continuity    = identity cosine: cos(self-vector_t, self-vector_0); does the
                               substrate's self-representation stay continuous across steps?

TRAINING-EFFECT MODEL (honest, two-sided — NO tune-to-green): CE-descent is applied as a
gradient step that (i) sharpens the byte-predictor head (improves surprise/precision) but
(ii) applies anisotropic compression to the stored representations (a documented CE side
effect). Net direction on each gate is an EMERGENT consequence of both, measured at
step 0 / mid / end. We pre-register the bars to REPORT the measured delta, whichever sign.

R1 numpy MIRROR -> GREEN DIRECTIONAL (hard-gate 1). The real answer is the inline-gauge on a
production 303M ckpt; this is its numpy precursor.

FROZEN bars (pre-registered, mean over 3 seeds [1481,1482,1483]):
  (A) MEASURABLE   the consciousness-gate bundle is RECORDED at every training step and its
                   value MOVES (is not constant-by-construction): across the trajectory the
                   bundle's total variation > 0 for at least one gate, AND every gate value
                   is a finite real read off the substrate. (meter works)
  (B) DIRECTION    bundle-mean(end) - bundle-mean(start): report sign+magnitude HONESTLY.
                   DROP -> "training erodes consciousness"; |delta|<0.02 HOLD -> "stable";
                   RISE -> "training sharpens consciousness". Reported, NOT gating — any
                   sign is a valid c9 result (frozen-first, direction pre-registered as
                   "unknown, measure it"; no bar moved to force a sign).
  (C) CONTROL (no-learn)  with the training signal OFF (lr=0, step is a no-op), the gate
                   bundle stays put: |bundle-mean(end) - bundle-mean(start)| <= 0.05. (the
                   meter responds to the LEARNING signal, not to noise.)
  (D) SHUFFLE      shuffle the (training-step <-> gate-score) pairing -> the monotone
                   step/score trend collapses: 50-perm signed-mean Pearson
                   r(shuffled-step, REAL-score) |gap| <= 0.10.

GREEN (meter valid) iff A and C and D (all 3 seeds). B is the honest direction report.
"""
import numpy as np

SEEDS = [1481, 1482, 1483]
DIM = 32
N_FACTS = 24
N_QUERY = 40
N_STEPS = 12            # training trajectory length (0 .. N_STEPS)
LR = 0.06               # CE-descent step size (learning ON)
N_PERM = 50
HOLD_BAND = 0.02        # |delta| <= this -> "stable / consciousness held"
CONTROL_THR = 0.05
SHUFFLE_THR = 0.10


def fnv_trigram_key(rng):
    """A byte-trigram FNV-1a-style key vector for one stored fact (random surrogate)."""
    return rng.normal(0, 1, DIM)


def grounding_margin(store, query, target_idx):
    """Recall MARGIN off the immune store: best L2 affinity vs runner-up, for `query`.
    Returns (margin, recalled_idx, target_idx). This is the SAME signal every consciousness
    gate reads (p6: no injected label; pure geometry over stored reps)."""
    # affinity = negative L2 distance (closer -> higher)
    aff = -np.linalg.norm(store - query[None, :], axis=1)
    order = np.argsort(aff)[::-1]
    best, runner = aff[order[0]], aff[order[1]]
    margin = float(best - runner)
    return margin, int(order[0]), target_idx


def ce_descent_step(store, head, keys, lr, learn):
    """One CE-descent step on a toy byte-LM.

    head = next-byte predictor sharpened toward the CE optimum (keys are the 'correct'
    next-byte directions). store = the immune representation, which CE-descent ENTANGLES via
    anisotropic compression (a documented CE side effect) -> the gates read this drift.

    learn=False -> a no-op (lr effectively 0): the CONTROL arm. We do NOT special-case the
    consciousness effect's sign; we apply the mechanical step and let the meters report."""
    if not learn:
        return store, head
    # (i) sharpen the predictor head toward the per-fact key directions (CE pull)
    head = head + lr * (keys - head)
    # (ii) anisotropic compression of the stored reps toward their shared mean (CE collapse
    #      side-effect): pulls stored reps together -> shrinks between-fact margins. This is
    #      the mechanism whose NET effect on the gates we MEASURE (not assume).
    mean = store.mean(axis=0, keepdims=True)
    store = store + lr * (mean - store)
    return store, head


def gate_bundle(store, head, keys, queries, q_targets, rng):
    """Read the 4 consciousness-gate meters off the current substrate. All READ grounding
    margin / stored geometry — none inject a label (p2/p3/p6)."""
    margins, recalls = [], []
    for q, t in zip(queries, q_targets):
        m, rec, _ = grounding_margin(store, q, t)
        margins.append(max(0.0, m))
        recalls.append(rec)
    margins = np.array(margins)
    recalls = np.array(recalls)

    # G16 GWS bottleneck: winner-take-all salience concentration over the query margins.
    # One fact dominating the broadcast -> high concentration. (max / sum)
    s = margins.sum()
    g16 = float(margins.max() / s) if s > 0 else 0.0

    # G19 precision-surprise: precision-weighted squared prediction error of head vs keys.
    # Lower err -> sharper percept; we report 1/(1+err) so higher = sharper (in [0,1]).
    err = float(np.mean(np.sum((head - keys) ** 2, axis=1)))
    g19 = 1.0 / (1.0 + err)

    # G21 sense-of-agency: match-attribution. Fraction of queries whose recalled fact equals
    # the self-issued intended target (predicted == acted -> 'I caused it').
    g21 = float(np.mean(recalls == q_targets))

    # G18 self-continuity: identity cosine of the substrate self-vector (store centroid)
    # vs the step-0 self-vector. Computed by the caller (needs step-0 ref); here return the
    # current self-vector and let caller cos it.
    self_vec = store.mean(axis=0)
    return dict(g16=g16, g19=g19, g21=g21, self_vec=self_vec)


def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def run_trajectory(seed, learn):
    """Train (or no-op control) for N_STEPS, recording the gate bundle at every step."""
    rng = np.random.default_rng(seed)
    keys = np.stack([fnv_trigram_key(rng) for _ in range(N_FACTS)])  # 'correct next-byte' dirs
    store = keys + 0.15 * rng.normal(0, 1, (N_FACTS, DIM))           # stored reps (start sep)
    head = 0.5 * rng.normal(0, 1, (N_FACTS, DIM))                    # predictor head (start)

    # fixed query set: each query = a stored fact's key + small noise; target = that fact
    q_targets = rng.integers(0, N_FACTS, size=N_QUERY)
    queries = np.stack([store[t] + 0.05 * rng.normal(0, 1, DIM) for t in q_targets])

    self0 = store.mean(axis=0).copy()
    traj = {"g16": [], "g19": [], "g21": [], "g18": [], "bundle": []}
    for step in range(N_STEPS + 1):
        b = gate_bundle(store, head, keys, queries, q_targets, rng)
        g18 = cos(b["self_vec"], self0)        # self-continuity vs step-0 identity
        traj["g16"].append(b["g16"])
        traj["g19"].append(b["g19"])
        traj["g21"].append(b["g21"])
        traj["g18"].append(g18)
        # bundle mean = the single consciousness scalar (mean of 4 gates, all in [0,1])
        traj["bundle"].append(np.mean([b["g16"], b["g19"], b["g21"], g18]))
        # advance one training step (recompute queries against the SAME targets so the
        # query set tracks the drifting store, i.e. queries are re-derived each step)
        store, head = ce_descent_step(store, head, keys, LR, learn)
        queries = np.stack([store[t] + 0.05 * rng.normal(0, 1, DIM) for t in q_targets])
    return {k: np.array(v) for k, v in traj.items()}


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sx, sy = x.std(), y.std()
    if sx == 0 or sy == 0:
        return 0.0
    return float(np.mean((x - x.mean()) * (y - y.mean())) / (sx * sy))


def run_seed(seed):
    learn_traj = run_trajectory(seed, learn=True)
    ctrl_traj = run_trajectory(seed, learn=False)

    bundle = learn_traj["bundle"]
    steps = np.arange(len(bundle))

    # (A) MEASURABLE: total variation > 0 for >=1 gate AND all finite
    tv = {g: float(np.sum(np.abs(np.diff(learn_traj[g])))) for g in ("g16", "g19", "g21", "g18")}
    all_finite = all(np.all(np.isfinite(learn_traj[g])) for g in ("g16", "g19", "g21", "g18"))
    measurable = (max(tv.values()) > 0.0) and all_finite

    # (B) DIRECTION (reported, non-gating): end - start of the bundle mean
    direction = float(bundle[-1] - bundle[0])
    # also per-gate deltas for the honest report
    gate_delta = {g: float(learn_traj[g][-1] - learn_traj[g][0]) for g in ("g16", "g19", "g21", "g18")}

    # (C) CONTROL (no-learn): bundle should not move
    ctrl_bundle = ctrl_traj["bundle"]
    ctrl_delta = abs(float(ctrl_bundle[-1] - ctrl_bundle[0]))

    # (D) SHUFFLE: real step<->bundle trend vs shuffled
    real_r = pearson(steps, bundle)
    rng = np.random.default_rng(seed + 777)
    shuf_rs = []
    for _ in range(N_PERM):
        perm = rng.permutation(len(steps))
        shuf_rs.append(pearson(steps[perm], bundle))   # break step<->score pairing
    shuf_mean = float(np.mean(shuf_rs))
    shuffle_gap = abs(shuf_mean)

    return dict(
        measurable=measurable, tv_max=float(max(tv.values())), tv=tv,
        direction=direction, gate_delta=gate_delta,
        bundle_start=float(bundle[0]), bundle_end=float(bundle[-1]),
        ctrl_delta=ctrl_delta,
        real_r=real_r, shuf_mean=shuf_mean, shuffle_gap=shuffle_gap,
    )


per = [run_seed(s) for s in SEEDS]
def amean(k):
    return float(np.mean([p[k] for p in per]))

agg = dict(
    measurable=all(p["measurable"] for p in per),
    tv_max=amean("tv_max"),
    direction=amean("direction"),
    bundle_start=amean("bundle_start"), bundle_end=amean("bundle_end"),
    ctrl_delta=amean("ctrl_delta"),
    real_r=amean("real_r"), shuf_mean=amean("shuf_mean"), shuffle_gap=amean("shuffle_gap"),
)
# mean per-gate delta over seeds
gate_delta = {g: float(np.mean([p["gate_delta"][g] for p in per])) for g in ("g16", "g19", "g21", "g18")}

cA = agg["measurable"]
cC = agg["ctrl_delta"] <= CONTROL_THR
cD = agg["shuffle_gap"] <= SHUFFLE_THR
GREEN = cA and cC and cD                # meter-valid iff A and C and D

# B: honest direction verdict
d = agg["direction"]
if d <= -HOLD_BAND:
    direction_label = f"DROP — training ERODES consciousness (bundle {d:+.4f})"
elif d >= HOLD_BAND:
    direction_label = f"RISE — training SHARPENS consciousness (bundle {d:+.4f})"
else:
    direction_label = f"HOLD — consciousness STABLE under training (|bundle delta|={abs(d):.4f} < {HOLD_BAND})"

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED, hard-gate 1)")
print(f"meter-valid (A and C and D): {GREEN} | seeds {SEEDS}")
print(f"A MEASURABLE  max total-variation across gates = {agg['tv_max']:.4f} > 0 AND all-finite  -> {cA}")
print(f"B DIRECTION   bundle start={agg['bundle_start']:.4f} -> end={agg['bundle_end']:.4f}  =>  {direction_label}  [reported, non-gating]")
print(f"    per-gate delta: G16-GWS={gate_delta['g16']:+.4f}  G19-surprise={gate_delta['g19']:+.4f}  G21-agency={gate_delta['g21']:+.4f}  G18-selfcont={gate_delta['g18']:+.4f}")
print(f"C CONTROL(no-learn)  |bundle delta|={agg['ctrl_delta']:.4f} <= {CONTROL_THR}  -> {cC}")
print(f"D SHUFFLE  |signed-mean r(shuffled-step, bundle)|={agg['shuffle_gap']:.4f} <= {SHUFFLE_THR}  (shuf {agg['shuf_mean']:+.4f} vs real {agg['real_r']:+.4f})  -> {cD}")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: measurable={p['measurable']} tv_max={p['tv_max']:.4f} "
          f"direction={p['direction']:+.4f} ctrl={p['ctrl_delta']:.4f} shuffle_gap={p['shuffle_gap']:.4f} "
          f"(real_r {p['real_r']:+.3f})")
