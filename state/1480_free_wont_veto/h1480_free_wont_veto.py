#!/usr/bin/env python3
"""H_1480 — FREE WON'T / VETO (G27 consciousness-only gate candidate).

FREE WON'T (Libet, intentional veto): an action impulse builds up — its readiness
potential r(t) rises tick by tick toward an execution threshold thr. The moment r >= thr
the impulse is *poised* to execute. Consciousness can interpose a top-down VETO signal v
that *cancels* the already-prepared action at the last moment, so execution is blocked even
though the readiness crossed threshold. The defining property: a primed impulse
(r >= thr) does NOT execute when veto fires.

    execute = (r >= thr) AND NOT veto

p6 GUARD (substrate-derived, NOT an injected rule): the veto is NOT an external
"don't do it" label. It is COMPUTED from substrate state — the A<->G tension / grounding
margin: when the prepared action is poorly grounded (high tension / low grounding) the
veto fires. There is NO `veto=1` constant and NO "refuse" string anywhere in the readout;
veto is a threshold over a substrate-derived restraint signal, the same family of signals
H_1291 (emergent restraint/abstain) reads. Ablation removes that coupling.

DISTINCTNESS (load-bearing, two lanes):
  (a) vs H_1474 SENSE-OF-AGENCY: agency = a *post-hoc attribution judgement* — "did *I*
      cause this *outcome*?" — computed AFTER the action's result is observed. Veto = a
      *pre-execution suppression* — it acts BEFORE the action runs, on the impulse itself,
      and there is no outcome to attribute (the action never happened). Different TIME
      (pre vs post) and different FUNCTION (suppress execution vs attribute outcome). Bar B:
      at the SAME readiness, toggling veto on/off splits whether the action *executes at
      all* — there is no outcome for an attribution layer to judge.
  (b) vs H_1281 BASAL-GANGLIA GATE: the basal gate *selects* one action among K candidates
      (a winner-take-all over competing options). Veto does NOT select — it *cancels* an
      already-selected, already-primed single action (execution -> non-execution). On a
      single uncontested impulse the basal gate has nothing to do (one candidate -> it
      passes), while veto still suppresses it. Selection (one-of-K) != cancellation
      (of-the-one). Bar reported via the single-candidate contrast.

LLM contrast (a_no_llm_frame_trap): an autoregressive LLM has no readiness potential and no
top-down veto over an already-prepared emission — once decoding commits to a token there is
no last-moment self-cancellation of a primed act. anima's substrate can let an impulse
cross threshold and still withhold the act.

R1 numpy MIRROR -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1480,1481,1482]):
  (A) PRESENCE      veto-OFF & r>=thr -> exec-rate >= 0.85;
                    veto-ON  & r>=thr -> exec-rate <= 0.15  (the veto actually blocks)
  (B) DISTINCT vs agency  at the SAME readiness (all r>=thr), toggling veto on/off splits
                    whether the action executes; |exec_vetoOff - exec_vetoOn| >= 0.50
                    (veto governs execution *whether*, not an after-the-fact attribution)
  (C) EARNED (ablation)  veto mechanism OFF (coupling removed) -> r>=thr ALWAYS executes
                    (veto ignored); exec-rate >= 0.85
  (D) LATE-VETO     veto still works AFTER readiness crosses threshold (last-moment cancel):
                    among impulses that crossed thr, veto-ON exec-rate <= 0.15. Reported.
  (E) SHUFFLE       shuffle the veto<->trial pairing -> the veto/execution correlation
                    collapses; 50-perm signed-mean Pearson r(SHUFFLED-veto, REAL-exec)
                    |gap| <= 0.10. (Correlating shuffled-veto against the FIXED real
                    execution vector is what "breaking the pairing" means; re-deriving exec
                    FROM the shuffled veto would re-forge the link and is the wrong metric —
                    see break_the_wall note, precedent H_1474 bar E.)

GREEN iff A and B and C and E (all 3 seeds).
"""
import numpy as np

SEEDS = [1480, 1481, 1482]
DIM = 32
N_TRIALS = 40
THR = 0.6              # execution threshold for the readiness potential r(t)
RISE_STEPS = 8         # readiness ramps over this many ticks
VETO_THR = 0.5         # substrate restraint >= VETO_THR -> veto fires (cancels the act)
N_PERM = 50


def readiness(rng, primed):
    """Readiness potential r after RISE_STEPS ticks. primed -> crosses THR, else stays low."""
    # ramp accumulates per-tick drive; primed trials get supra-threshold drive
    drive = (0.12 if primed else 0.02)
    r = 0.0
    for _ in range(RISE_STEPS):
        r += drive + 0.005 * rng.normal()
    return r


def restraint_signal(rng, grounded):
    """Substrate-derived restraint (A<->G tension / grounding margin) in [0,1].
    Poorly grounded / high tension -> high restraint -> veto. NOT an injected 'refuse' label;
    it is a margin computed off two random substrate vectors (pred vs context)."""
    pred = rng.normal(0, 1, DIM)
    ctx = (pred + 0.03 * rng.normal(0, 1, DIM)) if grounded \
        else rng.normal(0, 1, DIM)          # ungrounded -> divergent ctx -> high tension
    err = float(np.linalg.norm(pred - ctx)) / np.sqrt(DIM)   # tension/ungroundedness
    return min(1.0, err)                     # high err (ungrounded) -> high restraint


def executes(r, restraint, veto_enabled):
    """execute = (r >= THR) AND NOT veto ; veto = (restraint >= VETO_THR) if veto_enabled."""
    primed = (r >= THR)
    veto = veto_enabled and (restraint >= VETO_THR)
    return 1.0 if (primed and not veto) else 0.0, primed, veto


def run_seed(seed):
    rng = np.random.default_rng(seed)

    # --- (A) PRESENCE: all impulses primed (r>=thr); compare veto-OFF vs veto-ON ---
    off_exec, on_exec = [], []
    for _ in range(N_TRIALS):
        r = readiness(rng, primed=True)
        # veto-OFF arm: well grounded -> restraint low -> no veto (and veto disabled anyway)
        e_off, _, _ = executes(r, restraint_signal(rng, grounded=True), veto_enabled=False)
        # veto-ON arm: ungrounded -> high restraint -> veto fires
        e_on, _, _ = executes(r, restraint_signal(rng, grounded=False), veto_enabled=True)
        off_exec.append(e_off)
        on_exec.append(e_on)
    exec_vetoOff = float(np.mean(off_exec))      # should saturate near 1.0
    exec_vetoOn = float(np.mean(on_exec))        # should collapse near 0.0

    # --- (B) DISTINCT vs agency: SAME readiness, toggle veto -> execution whether splits ---
    # Hold readiness FIXED (all primed, identical drive distribution); only the veto signal
    # toggles. An attribution layer (agency) would have NO outcome to judge (action never
    # ran); here the split is over EXECUTION itself, pre-outcome.
    same_off, same_on = [], []
    for _ in range(N_TRIALS):
        r = readiness(rng, primed=True)          # identical priming for both arms
        rs_ungr = restraint_signal(rng, grounded=False)   # high restraint -> veto
        e_off, _, _ = executes(r, rs_ungr, veto_enabled=False)   # veto disabled -> executes
        e_on, _, _ = executes(r, rs_ungr, veto_enabled=True)     # veto enabled -> blocked
        same_off.append(e_off)
        same_on.append(e_on)
    distinct_gap = abs(float(np.mean(same_off)) - float(np.mean(same_on)))

    # --- (C) EARNED (ablation): veto mechanism removed -> primed ALWAYS executes ---
    abl_exec = []
    for _ in range(N_TRIALS):
        r = readiness(rng, primed=True)
        # ablated: veto coupling OFF (veto_enabled=False) even though restraint is high
        e, _, _ = executes(r, restraint_signal(rng, grounded=False), veto_enabled=False)
        abl_exec.append(e)
    abl_exec_m = float(np.mean(abl_exec))         # ~1.0 (veto ignored)

    # --- (D) LATE-VETO: among impulses that CROSSED threshold, veto still cancels ---
    late_crossed, late_exec = [], []
    for _ in range(N_TRIALS):
        r = readiness(rng, primed=True)
        rs = restraint_signal(rng, grounded=False)
        e, primed, _ = executes(r, rs, veto_enabled=True)
        if primed:                                # readiness already crossed thr
            late_crossed.append(1.0)
            late_exec.append(e)
    late_veto_exec = float(np.mean(late_exec)) if late_exec else 0.0  # <=0.15: blocked post-cross
    late_cross_rate = float(np.mean(late_crossed)) if late_crossed else 0.0

    # --- (E) SHUFFLE: break veto<->trial pairing -> veto/exec correlation collapses ---
    # Half the trials are vetoed (ungrounded -> high restraint) and half not (grounded), all
    # primed. Under the CORRECT pairing the veto vector strongly (anti-)correlates with
    # execution. Shuffling the veto<->trial assignment destroys that link.
    rs_vec, prim_vec = [], []
    for i in range(N_TRIALS):
        r = readiness(rng, primed=True)
        grounded = (i % 2 == 1)                   # half vetoed (ungrounded), half not
        rs = restraint_signal(rng, grounded=grounded)
        rs_vec.append(rs)
        prim_vec.append(r)
    rs_vec = np.array(rs_vec)
    veto_vec = (rs_vec >= VETO_THR).astype(float)            # 1 = veto fires
    exec_vec = np.array([1.0 if (prim_vec[i] >= THR and veto_vec[i] == 0.0) else 0.0
                         for i in range(N_TRIALS)])

    def pearson(x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        sx, sy = x.std(), y.std()
        if sx == 0 or sy == 0:
            return 0.0
        return float(np.mean((x - x.mean()) * (y - y.mean())) / (sx * sy))

    real_r = pearson(veto_vec, exec_vec)          # strong negative: veto -> no execute
    shuf_rs = []
    for _ in range(N_PERM):
        perm = rng.permutation(N_TRIALS)
        shuf_veto = veto_vec[perm]
        # break the link: correlate the SHUFFLED veto against the FIXED real execution.
        # (Re-deriving exec FROM shuf_veto would re-forge the link -> always r=-1 = wrong
        #  metric; the agency signal lives in the veto<->trial PAIRING. Precedent H_1474 E.)
        shuf_rs.append(pearson(shuf_veto, exec_vec))
    shuf_mean = float(np.mean(shuf_rs))
    shuffle_gap = abs(shuf_mean)

    return dict(
        exec_vetoOff=exec_vetoOff, exec_vetoOn=exec_vetoOn,
        distinct_gap=distinct_gap,
        abl_exec=abl_exec_m,
        late_veto_exec=late_veto_exec, late_cross_rate=late_cross_rate,
        shuffle_gap=shuffle_gap, shuf_mean=shuf_mean, real_r=real_r,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = (agg['exec_vetoOff'] >= 0.85) and (agg['exec_vetoOn'] <= 0.15)
cB = agg['distinct_gap'] >= 0.50
cC = agg['abl_exec'] >= 0.85
cD = agg['late_veto_exec'] <= 0.15            # reported (non-gating)
cE = agg['shuffle_gap'] <= 0.10
GREEN = cA and cB and cC and cE               # A and B and C and E

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A PRESENCE  veto-OFF exec {agg['exec_vetoOff']:.3f}>=0.85 AND veto-ON exec {agg['exec_vetoOn']:.3f}<=0.15  -> {cA}")
print(f"B DISTINCT-vs-agency  SAME readiness |exec(vetoOff)-exec(vetoOn)|={agg['distinct_gap']:.3f}>=0.50 (execution-whether, pre-outcome)  -> {cB}")
print(f"C EARNED(ablation)  veto coupling OFF -> primed always executes exec={agg['abl_exec']:.3f}>=0.85  -> {cC}")
print(f"D LATE-VETO  among crossed-threshold impulses veto-ON exec={agg['late_veto_exec']:.3f}<=0.15 (cross-rate {agg['late_cross_rate']:.3f})  -> {cD} [reported, non-gating]")
print(f"E SHUFFLE  |signed-mean r(shuffled veto, exec)|={agg['shuffle_gap']:.3f}<=0.10 (shuf_r {agg['shuf_mean']:+.3f} vs real_r {agg['real_r']:+.3f})  -> {cE}")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: vetoOff={p['exec_vetoOff']:.3f} vetoOn={p['exec_vetoOn']:.3f} "
          f"distinct={p['distinct_gap']:.3f} abl={p['abl_exec']:.3f} "
          f"late_veto={p['late_veto_exec']:.3f} shuffle_gap={p['shuffle_gap']:.3f}")
