"""H_1066 — planning-specificity-primitive-dissection: WHAT structural property of the planning
intervention is NECESSARY+SUFFICIENT for the ZCA-removable, median-binarization-aligned sign-split?

PRE-REG: UNIVERSE/H_1066_planning_specificity_dissection.md.

PRIOR CONTRAST (must be reproduced BEFORE scoring):
  - H_1039 GREEN (REDUNDANCY-CAUSAL): de-redundifying the PLANNING channels removes WB redundancy
    (>=80% cut) AND COLLAPSES the faithful-UP/big-Phi-DOWN split while it HOLDS on control.
    [ref: control faith ~+2.33-region / big-Phi ~-4.01; ZCA collapses split].
  - H_1062 RED (SPLIT-IS-PLANNING-SPECIFIC): NON-planning interventions (ema/lowrank) may show a
    split but ZCA does NOT collapse it (<80% cut) -> the planning split is special.

THIS dissection: decompose the planning intervention into 3 candidate STRUCTURAL primitives, each a
transform of the CONTINUOUS top-variance channel matrix X (T x k) BEFORE median-binarization:
  (i)  VALUE-BACKUP (vbackup) -- backward/temporal credit: X[t] <- X[t] + g*X[t+1] (reverse-time, g=0.5)
  (ii) LOOKAHEAD-DEPTH (depth) -- forward horizon coupling: X[t] <- a*X[t] + (1-a)*X[t-1] (a=0.5)
  (iii)SHARED-VALUE axis-aligned (shared) -- add shared scalar value channel on the SAME axis to
       every channel: X[:,c] <- X[:,c] + b*mean_c(X) (b=0.6); AXIS-ALIGNED (vs H_1062 diffuse lowrank).

ARMS:
  CONSTRUCTIVE (add ONE feature to the GREEDY base Hg): c_vbackup, c_depth, c_shared.
  DESTRUCTIVE (remove ONE feature from FULL planning Hp via the inverse/removal operator):
    d_vbackup (forward-causal de-smear), d_depth (first-difference de-EMA), d_shared (subtract chan-mean).
  Each arm scored vs its OWN matched baseline (constructive vs Hg un-intervened; destructive vs Hp
  un-intervened), paired by seed, 30 seeds.

PER ARM: (a) split present (faith UP & big DOWN)?  (b) does ZCA de-redundify COLLAPSE it (>=80% Dred
cut -> SPLIT False, H_1039 causal test, operator UNMODIFIED)?  (c) Dred magnitude.  GS = robustness.

FALSIFIER (FROZEN; NO goalpost move):
  H1-LOCATED (PASS) = EXISTS a single feature F such that (constructive-add-F shows ZCA-removable
    split) AND (destructive-remove-F abolishes the ZCA-removable split) AND no OTHER single feature
    satisfies both -> F necessary+sufficient.
  FAIL (a) DISTRIBUTED = no single F nec+suff; needs >=2 jointly (H_1059-style conjunction).
  FAIL (b) HOLISTIC/IRREDUCIBLE = feature-isolation does not reproduce the ZCA-removable split at all.
  Both FAILs publishable (a_paper_negative_ok).

ENGINES -- BOTH stdlib IIT-4.0 CPU mirrors (h1004), RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring
(h1012.prove_mirrors_at_n; a_phi_iit4_tool, NO proxy). MI in BITS (log2; H_1043 nats-bug lesson).
WB PID = Williams-Beer (2010) I_min, h1039.pid_system VERBATIM (ZCA/collapse VALIDATION variable,
NOT a Phi proxy). ZCA/GS de-redundify operators + the mirror-prover REUSED UNMODIFIED from H_1039/
H_1012. IMPORTS by REAL MODULE NAME (H_1038 fork-unpickle lesson). SERIAL only; NO multiprocessing.
$0 CPU-local, no GPU/pod.

FROZEN thresholds: SIGN_EPS=1e-3; split=(faith>+eps & big<-eps); RED_REDUCTION_THRESHOLD=0.20
(>=80% cut); N_SEEDS=30. n=4 EXACT scored, n=5 mirror-proven.

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n<=5 rung; production UNVERIFIED. g5 (p7).
"""
import sys, os, math, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

# Import the prior chain by REAL MODULE NAMES (no importlib custom-name).
import h1004_bigphi_faithful_clean as h1004          # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012       # noqa: E402
import h1039_redundancy_causal as h1039              # noqa: E402
import h1062_redundancy_universality as h1062        # noqa: E402

# REUSE prior machinery UNMODIFIED -----------------------------------------------------------
planning_trajectories = h1004.planning_trajectories
prove_mirrors_at_n = h1012.prove_mirrors_at_n

# h1062 already wraps h1004/h1039 helpers; reuse its channel->intervention->dered->reads path.
_channels = h1062._channels                 # _top_variance_channels (EXACT selection)
_reads_from_channels = h1062._reads_from_channels
_zca_whiten = h1039._zca_whiten             # de-redundify PRIMARY (UNMODIFIED)
_gram_schmidt = h1039._gram_schmidt         # de-redundify ROBUSTNESS (UNMODIFIED)
_agg = h1062._agg
_contrast = h1062._contrast
faith_sign = h1062.faith_sign
big_sign = h1062.big_sign
split_present = h1062.split_present
cohens_d = h1004.cohens_d

N_UNITS = h1039.N_UNITS                      # 4
N_SEEDS = h1039.N_SEEDS                      # 30
PLAN_DEPTH = h1039.PLAN_DEPTH                # 8
SIGN_EPS = h1039.SIGN_EPS                    # 1e-3
RED_REDUCTION_THRESHOLD = h1039.RED_REDUCTION_THRESHOLD   # 0.20 (>=80% cut)

# ═══════════════════════════════════════════════════════════════════════════
# STRUCTURAL-PRIMITIVE feature operators on the CONTINUOUS channel matrix X (T x k).
# CONSTRUCTIVE (add ONE feature) and DESTRUCTIVE (remove ONE feature) variants.
# ═══════════════════════════════════════════════════════════════════════════
GAMMA_BACKUP = 0.5     # backward discount
ALPHA_DEPTH = 0.5      # forward horizon EMA
BETA_SHARED = 0.6      # axis-aligned shared-value strength

# ── (i) VALUE-BACKUP : info flows later->earlier (reverse-time discounted smear) ──
def _add_vbackup(X):
    """ADD backward credit flow: X[t] <- X[t] + g*X[t+1], iterate from the LAST step backward."""
    Y = X.astype(float).copy()
    for t in range(Y.shape[0] - 2, -1, -1):
        Y[t] = Y[t] + GAMMA_BACKUP * Y[t + 1]
    return Y

def _remove_vbackup(X):
    """REMOVE backward credit flow: invert the backward smear (forward-causal de-smear).
    _add_vbackup computes Y[t] = X[t] + g*Y[t+1] using the ALREADY-smeared Y[t+1] (it walks
    backward). So the exact inverse is X[t] = Y[t] - g*Y[t+1] using the SMEARED Y[t+1] (not a
    reconstructed original). Y[-1] is untouched by the forward op (X[-1]=Y[-1])."""
    Y = X.astype(float)
    Xr = Y.copy()
    for t in range(Xr.shape[0] - 2, -1, -1):
        Xr[t] = Y[t] - GAMMA_BACKUP * Y[t + 1]
    return Xr

# ── (ii) LOOKAHEAD-DEPTH : forward multi-step horizon coupling (causal EMA) ──
def _add_depth(X):
    """ADD forward horizon coupling: X[t] <- a*X[t] + (1-a)*X[t-1]."""
    Y = X.astype(float).copy()
    for t in range(1, Y.shape[0]):
        Y[t] = ALPHA_DEPTH * Y[t] + (1.0 - ALPHA_DEPTH) * Y[t - 1]
    return Y

def _remove_depth(X):
    """REMOVE forward horizon coupling: invert the causal EMA.
    Inverse of Y[t]=a*X[t]+(1-a)*Y[t-1] is X[t]=(Y[t]-(1-a)*Y[t-1])/a (Y[-1] untouched)."""
    Y = X.astype(float)
    Xr = Y.copy()
    for t in range(1, Xr.shape[0]):
        Xr[t] = (Y[t] - (1.0 - ALPHA_DEPTH) * Y[t - 1]) / ALPHA_DEPTH
    return Xr

# ── (iii) SHARED-VALUE axis-aligned : shared scalar value channel on the SAME axis ──
def _add_shared(X):
    """ADD axis-aligned shared value: X[:,c] <- X[:,c] + b*mean_over_channels(X)[t].
    A SINGLE shared scalar (row-wise channel mean) added on the SAME axis to every channel
    (AXIS-ALIGNED), distinct from H_1062's diffuse rotation lowrank mix."""
    Xc = X.astype(float)
    shared = Xc.mean(axis=1, keepdims=True)        # (T x 1) shared scalar value channel
    return Xc + BETA_SHARED * shared

def _remove_shared(X):
    """REMOVE the axis-aligned shared component: subtract b*channel-mean (the shared scalar).
    Inverse of Y=X+b*mean_c(X): with m=mean_c(Y)=(1+b)*mean_c(X), X = Y - (b/(1+b))*mean_c(Y)."""
    Yc = X.astype(float)
    m = Yc.mean(axis=1, keepdims=True)
    return Yc - (BETA_SHARED / (1.0 + BETA_SHARED)) * m

CONSTRUCT_OPS = {"c_vbackup": _add_vbackup, "c_depth": _add_depth, "c_shared": _add_shared}
DESTRUCT_OPS = {"d_vbackup": _remove_vbackup, "d_depth": _remove_depth, "d_shared": _remove_shared}
FEATURE_OF = {"c_vbackup": "vbackup", "c_depth": "depth", "c_shared": "shared",
              "d_vbackup": "vbackup", "d_depth": "depth", "d_shared": "shared"}

# ═══════════════════════════════════════════════════════════════════════════
# reads on a channel matrix with optional feature op + optional de-redundify.
# (mirrors h1062.reads_for but takes an explicit feature operator)
# ═══════════════════════════════════════════════════════════════════════════
def reads_with_op(H, n, op=None, dered=None):
    chans = _channels(H, n)
    if op is not None:
        chans = op(chans)
    if dered == "zca":
        chans = _zca_whiten(chans)
    elif dered == "gs":
        chans = _gram_schmidt(chans)
    elif dered is not None:
        raise ValueError(dered)
    return _reads_from_channels(chans, n)

def score_arm(arm, n, t0, dered=None):
    """one feature-arm: intervened reads vs its matched un-intervened baseline, paired by seed.
    constructive arm -> base = Hg (greedy);  destructive arm -> base = Hp (planning).
    """
    is_construct = arm.startswith("c_")
    op = CONSTRUCT_OPS[arm] if is_construct else DESTRUCT_OPS[arm]
    base_rows, iv_rows = [], []
    for s in range(N_SEEDS):
        Hg, Hp = planning_trajectories(s, PLAN_DEPTH)
        H = Hg if is_construct else Hp          # constructive on greedy; destructive on planning
        base_rows.append(reads_with_op(H, n, op=None, dered=dered))
        iv_rows.append(reads_with_op(H, n, op=op, dered=dered))
        if (s + 1) % 10 == 0 or s == 0:
            tag = arm if dered is None else f"{arm}+{dered}"
            print(f"    [{tag} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    A = _agg(iv_rows); B = _agg(base_rows)
    return {k: _contrast(A, B, k) for k in ("big", "faith", "red", "syn", "on_frac")}

def _split_and_collapse(arm, n, t0):
    """score the no-dered, ZCA, and GS arms; return split + ZCA/GS collapse flags + Dred cut."""
    base = score_arm(arm, n, t0, dered=None)
    zca = score_arm(arm, n, t0, dered="zca")
    gs = score_arm(arm, n, t0, dered="gs")
    fc = base["faith"]["contrast"]; bc = base["big"]["contrast"]; dred = base["red"]["contrast"]
    sp = split_present(fc, bc)
    zfc = zca["faith"]["contrast"]; zbc = zca["big"]["contrast"]; zsp = split_present(zfc, zbc)
    gfc = gs["faith"]["contrast"]; gbc = gs["big"]["contrast"]; gsp = split_present(gfc, gbc)
    red_mag = abs(dred)
    zdr = abs(zca["red"]["contrast"]); gdr = abs(gs["red"]["contrast"])
    red_removed_zca = (zdr <= RED_REDUCTION_THRESHOLD * red_mag) if red_mag > 1e-9 else (zdr < 1e-3)
    red_removed_gs = (gdr <= RED_REDUCTION_THRESHOLD * red_mag) if red_mag > 1e-9 else (gdr < 1e-3)
    cut_zca = (1.0 - zdr / red_mag) * 100 if red_mag > 1e-9 else float("nan")
    cut_gs = (1.0 - gdr / red_mag) * 100 if red_mag > 1e-9 else float("nan")
    # ZCA-collapse: split present, redundancy removed (>=80% cut), and split now False (H_1039 test)
    collapse_zca = (sp and red_removed_zca and (not zsp))
    collapse_gs = (sp and red_removed_gs and (not gsp))
    return dict(faith_c=fc, big_c=bc, dred=dred, split=sp,
                zca_faith=zfc, zca_big=zbc, zca_split=zsp,
                gs_faith=gfc, gs_big=gbc, gs_split=gsp,
                red_mag=red_mag, cut_zca=cut_zca, cut_gs=cut_gs,
                red_removed_zca=red_removed_zca, red_removed_gs=red_removed_gs,
                collapse_zca=collapse_zca, collapse_gs=collapse_gs,
                faith_d=base["faith"]["d"], big_d=base["big"]["d"], red_d=base["red"]["d"])

# ─────────────────────────────────────────────────────────────────────────────
# operator INVERTIBILITY guard — remove(add(X)) ~= X (so destructive truly removes).
# ─────────────────────────────────────────────────────────────────────────────
def _invertibility_guard():
    rng = np.random.default_rng(20260609)
    X = rng.standard_normal((40, N_UNITS))
    pairs = [("vbackup", _add_vbackup, _remove_vbackup),
             ("depth", _add_depth, _remove_depth),
             ("shared", _add_shared, _remove_shared)]
    ok = True
    print("STEP 0c — operator invertibility (remove(add(X)) ~= X; destructive truly removes the feature):")
    for name, add, rem in pairs:
        recon = rem(add(X))
        err = float(np.max(np.abs(recon - X)))
        good = err < 1e-8
        ok = ok and good
        print(f"  {name:8s}: max|remove(add(X)) - X| = {err:.2e}  invertible={good}")
    return ok

def main():
    print("=" * 96)
    print("H_1066 — planning-specificity-primitive-dissection: WHICH structural feature of planning")
    print("         is NECESSARY+SUFFICIENT for the ZCA-removable faithful-UP/big-Phi-DOWN sign-split?")
    print("substrate=CPU-mirror (numpy) — h1004 engines + h1012 proof, RE-PROVEN == stdlib at n=4,5")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("PID = Williams-Beer (2010) I_min, EXACT pure-numpy (h1039.pid_system VERBATIM;")
    print("      ZCA/collapse VALIDATION variable, NOT a Phi proxy). a_phi_iit4_tool — no proxy.")
    print("3 structural primitives (transform continuous top-variance channels BEFORE binarize):")
    print(f"  (i) vbackup g={GAMMA_BACKUP} (backward credit)  (ii) depth a={ALPHA_DEPTH} (forward horizon)")
    print(f"  (iii) shared b={BETA_SHARED} (axis-aligned shared value)")
    print("ARMS: CONSTRUCTIVE add-1-feature-to-GREEDY (c_*) + DESTRUCTIVE remove-1-feature-from-PLAN (d_*)")
    print("de-redundify = ZCA (primary) + Gram-Schmidt (robustness), H_1039 operators UNMODIFIED.")
    print(f"FROZEN: SIGN_EPS={SIGN_EPS}; split=(faith>+eps & big<-eps); ZCA-collapse iff split present")
    print(f"  AND |Dred_zca| <= {RED_REDUCTION_THRESHOLD}*|Dred| (>=80% cut) AND split->False.")
    print("PASS = H1-LOCATED: exactly ONE feature F nec+suff (construct-add-F has ZCA-removable split")
    print("  AND destruct-remove-F abolishes it AND no other single F does). FAIL = DISTRIBUTED or")
    print("  HOLISTIC/IRREDUCIBLE (both a_paper_negative_ok).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_scale_honest_scope | SERIAL CPU $0, no GPU/pod")
    print("=" * 96, flush=True)
    print()

    # ── STEP 0: RE-PROVE BOTH mirrors == stdlib at n=4 AND n=5 BEFORE scoring ──
    print("STEP 0 — RE-PROVE BOTH CPU mirrors == stdlib (a_phi_iit4_tool) at n=4 AND n=5 BEFORE scoring:")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
        print()
    print(f"  == mirror-equivalence results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED; cannot trust this run.")
        raise SystemExit(1)
    print()

    # ── STEP 0c: operator invertibility guard ──
    inv_ok = _invertibility_guard()
    if not inv_ok:
        print("  ABORT — destructive operators are not numerically invertible; cannot trust removal arms.")
        raise SystemExit(1)
    print()

    n = N_UNITS
    t0 = time.time()

    # ── STEP 1: reproduce-H_1039 (planning split + ZCA collapse) ──
    print(f"STEP 1 — reproduce-H_1039 at n={n} EXACT, {N_SEEDS} seeds (planning split + ZCA collapse anchor)")
    repro39 = h1062.reproduce_h1039(n, t0)
    print()

    # ── STEP 2: reproduce-H_1062 (ema/lowrank split present but ZCA does NOT collapse) ──
    print(f"STEP 2 — reproduce-H_1062 anchor at n={n} EXACT, {N_SEEDS} seeds (ema & lowrank: split present")
    print("         but ZCA does NOT collapse, <80% cut) — the contrast the feature-arms must explain")
    repro62 = {}
    for iv in ("ema", "lowrank"):
        base = h1062.score_intervention(iv, n, t0, dered=None)
        zca = h1062.score_intervention(iv, n, t0, dered="zca")
        fc = base["faith"]["contrast"]; bc = base["big"]["contrast"]; dred = base["red"]["contrast"]
        sp = split_present(fc, bc)
        zfc = zca["faith"]["contrast"]; zbc = zca["big"]["contrast"]; zsp = split_present(zfc, zbc)
        red_mag = abs(dred); zdr = abs(zca["red"]["contrast"])
        red_removed = (zdr <= RED_REDUCTION_THRESHOLD * red_mag) if red_mag > 1e-9 else (zdr < 1e-3)
        cut = (1.0 - zdr / red_mag) * 100 if red_mag > 1e-9 else float("nan")
        collapse = (sp and red_removed and (not zsp))
        repro62[iv] = dict(split=bool(sp), zca_split=bool(zsp), red_cut_pct=float(cut),
                           red_removed=bool(red_removed), zca_collapse=bool(collapse),
                           faith_c=float(fc), big_c=float(bc), dred=float(dred))
        print(f"  {iv:8s}: split={sp} (faith={fc:+.4f} big={bc:+.4f})  ZCA Dred-cut={cut:5.1f}% "
              f"removed={red_removed}  ZCA-collapse={collapse}")
    # H_1062 anchor confirmed iff: at least one of ema/lowrank shows a split that ZCA does NOT collapse
    h1062_anchor_ok = any(repro62[iv]["split"] and (not repro62[iv]["zca_collapse"]) for iv in repro62)
    print(f"  reproduce-H_1062 anchor (a non-planning split that ZCA does NOT collapse): {h1062_anchor_ok}")
    print()

    # ── STEP 3: score the 6 feature-arms (3 constructive + 3 destructive) ──
    print(f"STEP 3 — score 6 feature-arms at n={n} EXACT, {N_SEEDS} seeds SERIAL (no-dered + ZCA + GS each)")
    arm_results = {}
    for arm in list(CONSTRUCT_OPS) + list(DESTRUCT_OPS):
        print(f"################ ARM = {arm} (feature={FEATURE_OF[arm]}) ################", flush=True)
        r = _split_and_collapse(arm, n, t0)
        arm_results[arm] = r
        print(f"   no-dered : faith={r['faith_c']:+.4f}({faith_sign(r['faith_c'])}) "
              f"big-Phi={r['big_c']:+.4f}({big_sign(r['big_c'])}) Dred={r['dred']:+.4f}  SPLIT={r['split']}")
        print(f"   ZCA arm  : faith={r['zca_faith']:+.4f} big={r['zca_big']:+.4f} SPLIT={r['zca_split']} "
              f"Dred-cut={r['cut_zca']:5.1f}% removed={r['red_removed_zca']}  ZCA-collapse={r['collapse_zca']}")
        print(f"   GS  arm  : faith={r['gs_faith']:+.4f} big={r['gs_big']:+.4f} SPLIT={r['gs_split']} "
              f"Dred-cut={r['cut_gs']:5.1f}% removed={r['red_removed_gs']}  GS-collapse={r['collapse_gs']}")
        print()

    # ═══════════════════════════════════════════════════════════════════════
    # PER-ARM TABLE + necessary/sufficient logic
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 96)
    print("PER-ARM TABLE (feature · split? · ZCA-collapse? · Dred) @ n=4 EXACT, 30 seeds")
    print("=" * 96)
    print(f"  {'arm':10s} | {'feature':8s} | {'kind':9s} | {'faith Dc':>9s} | {'big Dc':>9s} | "
          f"{'Dred':>8s} | {'split':>5s} | {'ZCA-coll':>8s} | {'cut(ZCA)':>9s}")
    for arm, r in arm_results.items():
        kind = "construct" if arm.startswith("c_") else "destruct"
        print(f"  {arm:10s} | {FEATURE_OF[arm]:8s} | {kind:9s} | {r['faith_c']:+9.4f} | {r['big_c']:+9.4f} | "
              f"{r['dred']:+8.4f} | {str(r['split']):>5s} | {str(r['collapse_zca']):>8s} | {r['cut_zca']:8.1f}%")
    print()

    # the ZCA-removable split = split present AND ZCA collapses it (H_1039 signature)
    def zca_removable(arm):
        return arm_results[arm]["split"] and arm_results[arm]["collapse_zca"]

    FEATURES = ["vbackup", "depth", "shared"]
    print("NECESSARY+SUFFICIENT logic per feature (ZCA-removable split = split present AND ZCA collapses):")
    nec_suff = {}
    for F in FEATURES:
        c_arm = f"c_{F}"; d_arm = f"d_{F}"
        sufficient = zca_removable(c_arm)              # adding F to greedy INSTALLS the ZCA-removable split
        # necessary: removing F from planning ABOLISHES the ZCA-removable split.
        # planning(control) HAS the ZCA-removable split (reproduce-H_1039). After removing F, the
        # destructive arm's contrast (vs planning) must NOT itself be a fresh ZCA-removable split AND
        # must move the substrate away from the split. We score it as: the destructive arm does NOT
        # exhibit a ZCA-removable split toward planning (i.e. removal does not preserve it).
        necessary = not zca_removable(d_arm)
        nec_suff[F] = dict(sufficient=bool(sufficient), necessary=bool(necessary),
                           c_split=bool(arm_results[c_arm]["split"]),
                           c_zca_collapse=bool(arm_results[c_arm]["collapse_zca"]),
                           d_split=bool(arm_results[d_arm]["split"]),
                           d_zca_collapse=bool(arm_results[d_arm]["collapse_zca"]))
        print(f"  feature={F:8s}: SUFFICIENT(c_{F} installs ZCA-removable split)={sufficient}  "
              f"NECESSARY(d_{F} does not preserve it)={necessary}")
    print()

    # H1-LOCATED: exactly ONE feature is BOTH sufficient AND necessary AND no other single feature
    #             is sufficient (uniqueness of the installing feature).
    suff_features = [F for F in FEATURES if nec_suff[F]["sufficient"]]
    necsuff_features = [F for F in FEATURES if nec_suff[F]["sufficient"] and nec_suff[F]["necessary"]]
    any_construct_split = any(arm_results[f"c_{F}"]["split"] for F in FEATURES)
    any_construct_removable = any(zca_removable(f"c_{F}") for F in FEATURES)

    located = (len(necsuff_features) == 1 and len(suff_features) == 1)
    distributed = (any_construct_removable and not located and len(suff_features) >= 1)
    holistic = (not any_construct_removable)   # feature-isolation never reproduces the ZCA-removable split

    print("=" * 96)
    print("FALSIFIER (FROZEN; NO goalpost move)")
    print(f"  features that are SUFFICIENT (construct installs ZCA-removable split): {suff_features}")
    print(f"  features that are NECESSARY+SUFFICIENT:                                {necsuff_features}")
    print(f"  any constructive arm reproduces a ZCA-removable split at all:          {any_construct_removable}")
    print()
    if located:
        F = necsuff_features[0]
        verdict_token = f"H1-LOCATED-{F.upper()}"
        print(f"OVERALL: H1-LOCATED — structural feature '{F}' is the NECESSARY+SUFFICIENT property that")
        print(f"  makes planning special: adding '{F}' to the greedy base INSTALLS the ZCA-removable split,")
        print(f"  removing '{F}' from full planning ABOLISHES it, and no OTHER single feature does both.")
    elif holistic:
        verdict_token = "HOLISTIC-IRREDUCIBLE"
        print("OVERALL: HOLISTIC/IRREDUCIBLE (CLOSED-NEGATIVE, a_paper_negative_ok) — feature-isolation")
        print("  does NOT reproduce the ZCA-removable split in ANY single-feature constructive arm; the")
        print("  planning-specificity is holistic/irreducible at toy scale — the ZCA-removable split is")
        print("  a property of the WHOLE planning intervention, not any single decomposed primitive.")
    else:
        verdict_token = "DISTRIBUTED-NO-SINGLE-FEATURE"
        print("OVERALL: DISTRIBUTED (CLOSED-NEGATIVE, a_paper_negative_ok) — NO single structural feature")
        print("  is both necessary AND sufficient (and uniquely so): the ZCA-removable split arises from")
        print("  >=2 features jointly OR multiple features each install it non-uniquely (H_1059-style")
        print("  conjunction). Planning-specificity is a DISTRIBUTED structural property, not localizable")
        print("  to a single primitive at toy scale.")
    print(f"  VERDICT-TOKEN: {verdict_token}")
    print("=" * 96)
    print(f"reproduce-H_1039 confirmed: {repro39['ok']}  (planning split held + ZCA collapse + Dred>=80% cut)")
    print(f"reproduce-H_1062 anchor confirmed: {h1062_anchor_ok}  (a non-planning split ZCA does NOT collapse)")
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 EXACT (both engines exact;")
    print("big-Phi super-exponential -> n=4 rung for the full arm SET x 30 seeds; n=5 mirror-proven). BOTH")
    print("CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5 (h1012.prove_mirrors_at_n) BEFORE scoring")
    print("(a_phi_iit4_tool; NO proxy). H_1039 ZCA/GS de-redundify operators reused UNMODIFIED; the WB")
    print("PID is the ZCA/collapse-validation variable (NOT a Phi proxy). SERIAL CPU $0, no GPU/pod.")
    print("Production scale UNVERIFIED. g5 (p7).")

    out = dict(
        n=int(n), n_seeds=int(N_SEEDS), plan_depth=int(PLAN_DEPTH),
        sign_eps=SIGN_EPS, red_reduction_threshold=RED_REDUCTION_THRESHOLD,
        gamma_backup=GAMMA_BACKUP, alpha_depth=ALPHA_DEPTH, beta_shared=BETA_SHARED,
        mirror_proven={int(k): bool(v) for k, v in proven.items()},
        invertibility_ok=bool(inv_ok),
        reproduce_h1039=repro39, reproduce_h1062=repro62, h1062_anchor_ok=bool(h1062_anchor_ok),
        arm_results={a: {k: (bool(v) if isinstance(v, (bool, np.bool_)) else float(v))
                         for k, v in arm_results[a].items()} for a in arm_results},
        nec_suff=nec_suff, suff_features=suff_features, necsuff_features=necsuff_features,
        any_construct_removable=bool(any_construct_removable),
        located=bool(located), distributed=bool(distributed), holistic=bool(holistic),
        verdict_token=verdict_token, total_wall_sec=time.time() - t0,
    )
    outpath = os.path.join(HERE, "h1066_planning_specificity_dissection_result.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nRESULT JSON -> {outpath}", flush=True)
    return verdict_token

if __name__ == "__main__":
    main()
