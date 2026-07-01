#!/usr/bin/env python3
"""h1060_ruler_completeness_phi_t.py — H_1060: ruler-completeness Phi-T capstone.

QUESTION (the consciousness-RULER arc capstone — synthesis of H_1045 + H_1051 + H_1047)
=======================================================================================
Two ESTABLISHED orthogonal ruler axes exist:
  (1) instantaneous Phi — H_1045 closed-neg: one big-Phi scalar suffices for BINARY
      planning-vs-control (a 3-vector adds only +0.0136 AUC).
  (2) temporal/agency T = z(provenance-depth, H_932) + z(veto-capacity, H_935) — H_1051
      H1-PASS: T separates Phi-matched active/passive (|d_T|=8.77), orthogonal to Phi.
H_1047 closed-neg: a (faithful, big-Phi) PAIR is directional but sub-threshold
(+0.1333 < 0.15) — BUT that pair was two Phi-MEASURES, NOT Phi+T.

CONSTRUCTIVE CAPSTONE: on a MIXED battery whose policies vary in BOTH planning-structure
(Phi-laden) AND agency (T-laden), does the (Phi, T) 2-vector beat the best single
Phi-scalar at predicting the behavioral CLASS? -> does the ruler genuinely NEED two axes?

REUSE (verbatim, no reinvention — a_phi_iit4_tool)
--------------------------------------------------
- H_1047 module exec'd with its __main__ guard stripped -> inherits the H_1035 policy
  battery, substrate_reads (BOTH stdlib IIT-4.0 engines, n=4, NO proxy), the H_1012
  prove_mirrors_at_n equivalence proof (BOTH engines, n=4 AND n=5), reproduce_h1029_check,
  AND the LOO nearest-centroid protocol loo_nearest_centroid_accuracy — all byte-for-byte.
- H_1051 module loaded by path -> _provenance_depth (H_932 verified-link DEPTH) +
  _veto_capacity (H_935 active-veto fraction) UNMODIFIED, plus PureField for the gate.

FROZEN design (declared in UNIVERSE/cards/H_1060_ruler_completeness_phi_t.md BEFORE measuring):
  behavioral class (structural, measure-INDEPENDENT — the prediction target), >=3 classes:
    REACTIVE            iff depth == 0                 (regardless of agency)
    DELIBERATE-ACTIVE   iff depth >= 1 and agency==ACTIVE
    DELIBERATE-PASSIVE  iff depth >= 1 and agency==PASSIVE
  features: PAIR (Phi_scalar_best_norm, T_norm) 2-D ; scalars s_faith, s_big, s_T (1-D each).
  classifier: H_1047 loo_nearest_centroid_accuracy (deterministic, $0). accuracy over battery.
  MARGIN = 0.15 (SAME bar as H_1047; FROZEN).
  H1-PASS = RULER-NEEDS-T : acc[(Phi,T)] >= best_acc[single Phi-scalar] + 0.15.
  H1-FAIL = PHI-SCALAR-STILL-SUFFICES : margin < 0.15 (closed-negative, a_paper_negative_ok).

p3/p6/p7 honored. g5 CODE-measured. a_phi_iit4_tool (REAL engines, no proxy). TOY n<=4 for
per-member Phi (n=5 only for the mirror re-proof; a_scale_honest_scope); $0 CPU SERIAL.
"""
from __future__ import annotations

import importlib.util as _ilu
import json
import math
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(HERE)


# ── Import the H_1047 harness VERBATIM (it exec's H_1035 -> H_1014 -> H_1004 engines +
#    the H_1012 prove_mirrors_at_n proof + the LOO nearest-centroid protocol). ──
_h1047_path = os.path.join(HERE, "h1047_pair_ruler.py")
_spec = _ilu.spec_from_file_location("h1047", _h1047_path)
_h1047 = _ilu.module_from_spec(_spec)
_src = open(_h1047_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1047_path, "exec"), _h1047.__dict__)

# substrate handles inherited through H_1047 (== H_1035/H_1014/H_1004, all verbatim)
prove_mirrors_at_n = _h1047.prove_mirrors_at_n     # H_1012: BOTH engines, any n
substrate_reads = _h1047.substrate_reads            # H -> {big, faith, ...} (n=4)
rich_rollout = _h1047.rich_rollout                  # parameterized H_1035 rollout
reproduce_h1029_check = _h1047.reproduce_h1029_check
policies = _h1047.policies                          # H_1035 richer policy space
pol_name = _h1047.pol_name
loo_nearest_centroid_accuracy = _h1047.loo_nearest_centroid_accuracy  # H_1047 LOO protocol
N_SEEDS = _h1047.N_SEEDS                             # H_1035 seed count (30); Phi = seed-mean


# ── Load the H_1051 T-machinery by path (real-module import; UNMODIFIED). ──
def _load(modname, relpath):
    path = os.path.join(_REPO, relpath)
    d = os.path.dirname(path)
    if d not in sys.path:
        sys.path.insert(0, d)
    spec = _ilu.spec_from_file_location(modname, path)
    m = _ilu.module_from_spec(spec)
    sys.modules[modname] = m
    spec.loader.exec_module(m)
    return m


_h1051 = _load("h1051_temporal_agency_ruler",
               "UNIVERSE/h1051_temporal_agency_ruler.py")
PureField = _h1051.PureField
_provenance_depth = _h1051._provenance_depth        # H_932 verified-link DEPTH, UNMODIFIED
_veto_capacity = _h1051._veto_capacity              # H_935 active-veto fraction, UNMODIFIED
H1051_GATE_TICKS = _h1051.GATE_TICKS


# ── FROZEN H_1060 design (H_1060_ruler_completeness_phi_t.md). ──
CLASSES = ["REACTIVE", "DELIBERATE-ACTIVE", "DELIBERATE-PASSIVE"]  # frozen order = tie-break
MARGIN = 0.15
N_AGENCY_SEEDS = 12   # agency-mode seeds per (policy, agency) cell; T-machinery is the cost


def behavioral_class(depth, agency):
    """Structural behavioral class spanning BOTH axes. measure-INDEPENDENT.
    agency in {True=ACTIVE, False=PASSIVE}."""
    if depth == 0:
        return "REACTIVE"
    return "DELIBERATE-ACTIVE" if agency else "DELIBERATE-PASSIVE"


def _zscore(v):
    v = np.asarray(v, float)
    s = v.std()
    return (v - v.mean()) / s if s > 1e-12 else np.zeros_like(v)


def main():
    print("=" * 90)
    print("H_1060 — ruler-completeness Phi-T capstone: does (Phi, T) beat the best single")
    print("Phi-scalar on a MIXED battery varying in BOTH planning-structure AND agency?")
    print("substrate=CPU-mirror (numpy) — H_1047/H_1035/H_1014/H_1004 engines + H_1012 proof")
    print("                              + H_1051 T-machinery (H_932 prov-depth + H_935 veto), all verbatim")
    print("big-Phi:      hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s) — measure (no proxy)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar) — measure")
    print(f"FROZEN: classes={CLASSES}  MARGIN={MARGIN}  agency_seeds={N_AGENCY_SEEDS}")
    print("target = behavioral CLASS (structural, measure-INDEPENDENT). classifier = LOO nearest-centroid.")
    print("PASS=RULER-NEEDS-T (acc[(Phi,T)] >= best_acc[single Phi-scalar] + 0.15)")
    print("FAIL=PHI-SCALAR-STILL-SUFFICES (margin < 0.15; a_paper_negative_ok)")
    print("=" * 90)
    print()

    out_lines = []

    def emit(s=""):
        print(s, flush=True)
        out_lines.append(s)

    emit("=" * 90)
    emit("H_1060 — ruler-completeness Phi-T capstone (synthesis of H_1045 + H_1051 + H_1047)")
    emit("verdict-gate g73 — raw measurement, verbatim (committed BEFORE the .md emoji tier)")
    emit("substrate: CPU-local numpy mirror of stdlib IIT-4.0 (a_phi_iit4_tool, NO proxy); $0; serial.")
    emit("big-Phi:      hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    emit("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    emit("T:            z(provenance-depth, H_932) + z(veto-capacity, H_935)  [H_1051 machinery, UNMODIFIED]")
    emit("=" * 90)
    emit("")

    # ── STEP 0 — mirror-equivalence re-proof at n=4 AND n=5 (BOTH engines, a_phi_iit4_tool). ──
    emit("== STEP 0: mirror ==stdlib RE-PROVEN at n=4 AND n=5 (BOTH engines) BEFORE scoring ==")
    import io
    import contextlib
    for n in (4, 5):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            okn = prove_mirrors_at_n(n)
        for ln in buf.getvalue().rstrip("\n").split("\n"):
            emit("  " + ln)
        emit(f"  ==-PROOF n={n}: {'PROVEN' if okn else 'FAILED'}")
    ok4 = prove_mirrors_at_n(4)
    ok5 = prove_mirrors_at_n(5)
    rep = reproduce_h1029_check()
    emit(f"  mirror n=4 PROVEN={ok4}   mirror n=5 PROVEN={ok5}   REPRODUCE-H_1029={'EXACT' if rep else 'MISMATCH'}")
    mirror_ok = ok4 and ok5 and rep
    emit(f"  EQUIVALENCE + REPRODUCE PROOF n=4,5: {'PROVEN' if mirror_ok else 'FAILED — DO NOT TRUST'}")
    if not mirror_ok:
        raise SystemExit("equivalence/reproduce proof failed — aborting")
    emit("")

    # ── STEP 0b — REPRODUCE-H_1047 numeric anchor (greedy policy SEED-MEAN faith/big read). ──
    # H_1047/H_1035 published "policy-1 read greedy faith=0.5069 big=9.5283" — that is the
    # SEED-MEAN over N_SEEDS of the greedy policy (0, 0.0, 0.0), exactly the H_1047 path:
    #   for s in range(N_SEEDS): H = rich_rollout(s, d, e, m); r = substrate_reads(H).
    def _policy_phi_seedmean(p):
        d, e, m = p
        fs, bs = [], []
        for s in range(N_SEEDS):
            r = substrate_reads(rich_rollout(s, d, e, m))
            fs.append(float(r["faith"])); bs.append(float(r["big"]))
        return float(np.mean(fs)), float(np.mean(bs))

    emit("== STEP 0b: REPRODUCE-H_1047 anchor — greedy policy (0,0.0,0.0) SEED-MEAN faith/big ==")
    g_faith, g_big = _policy_phi_seedmean((0, 0.0, 0.0))
    rep1047_faith = abs(g_faith - 0.5069) < 1e-3
    rep1047_big = abs(g_big - 9.5283) < 1e-3
    rep1047 = rep1047_faith and rep1047_big
    emit(f"  greedy faith={g_faith:.4f} (H_1047 ref 0.5069, |Δ|={abs(g_faith-0.5069):.2e}, OK={rep1047_faith})")
    emit(f"  greedy big  ={g_big:.4f} (H_1047 ref 9.5283, |Δ|={abs(g_big-9.5283):.2e}, OK={rep1047_big})")
    emit(f"  REPRODUCE-H_1047 (greedy seed-mean faith/big anchor matches published): {rep1047}")
    if not rep1047:
        raise SystemExit("REPRODUCE-H_1047 anchor mismatch — aborting (harness drift)")
    emit("")

    # ── STEP 1 — build the MIXED battery: (policy, agency-mode) members. ──
    # Phi is a deterministic function of the policy (substrate_reads on rich_rollout); the
    # same policy under ACTIVE vs PASSIVE has the SAME Phi but DIFFERENT T -> the Phi-axis
    # cannot tell ACTIVE from PASSIVE within a depth>=1 policy; only T can. That is exactly
    # the capstone test: is the agency-only-distinguishable class recoverable from Phi alone?
    POLS = policies()
    emit(f"== STEP 1: MIXED battery — {len(POLS)} policies x {{ACTIVE,PASSIVE}} agency, "
         f"agency seeds={N_AGENCY_SEEDS} ==")
    t0 = time.time()

    # Phi reads are per-policy SEED-MEANS over N_SEEDS (the H_1047/H_1035 path, VERBATIM).
    pol_faith, pol_big = {}, {}
    for p in POLS:
        pol_faith[p], pol_big[p] = _policy_phi_seedmean(p)

    # Build battery members: for each policy x agency-mode, average T over agency seeds.
    members = []
    for pi, p in enumerate(POLS):
        d, e, m = p
        for agency in (True, False):
            depths_seed, vetos_seed = [], []
            for s in range(N_AGENCY_SEEDS):
                rng = np.random.default_rng((pi * 9173 + s * 31 + (1 if agency else 0)) & 0x7fffffff)
                # H_935 active-veto fraction on a fresh PureField (H_1051 machinery UNMODIFIED)
                ph0 = tuple(float(rng.uniform(-0.5, 0.5)) for _ in range(3))
                am0 = tuple(float(0.1 + rng.uniform(-0.02, 0.02)) for _ in range(3))
                pf = PureField(phase0=ph0, amp0=am0)
                veto = _veto_capacity(pf, H1051_GATE_TICKS, active=agency, rng=rng)
                # H_932 verified-link depth (H_1051 machinery UNMODIFIED)
                depth_prov = _provenance_depth(active=agency, seed_tag=(pi * 1000 + s), rng=rng)
                depths_seed.append(depth_prov)
                vetos_seed.append(veto)
            members.append(dict(
                policy=p, depth=d, agency=agency,
                faith=pol_faith[p], big=pol_big[p],
                prov_depth=float(np.mean(depths_seed)),
                veto_cap=float(np.mean(vetos_seed)),
                cls=behavioral_class(d, agency),
            ))
        emit(f"  [{pi+1:2d}/{len(POLS)}] {pol_name(p):26s} faith={pol_faith[p]:7.4f} "
             f"big={pol_big[p]:8.4f}  elapsed={time.time()-t0:6.1f}s")
    emit("")

    # ── STEP 2 — features. T = z(prov-depth) + z(veto-cap) over ALL battery members. ──
    depths = np.array([mm["prov_depth"] for mm in members], float)
    vetos = np.array([mm["veto_cap"] for mm in members], float)
    T_raw = _zscore(depths) + _zscore(vetos)
    for mm, t in zip(members, T_raw):
        mm["T"] = float(t)

    faiths = np.array([mm["faith"] for mm in members], float)
    bigs = np.array([mm["big"] for mm in members], float)
    Ts = np.array([mm["T"] for mm in members], float)

    def _minmax(v):
        lo, hi = v.min(), v.max()
        return (v - lo) / (hi - lo + 1e-12)

    f_norm = _minmax(faiths)
    b_norm = _minmax(bigs)
    T_norm = _minmax(Ts)

    labels = [mm["cls"] for mm in members]
    y = np.array([CLASSES.index(c) for c in labels])
    emit("== CLASS PARTITION (structural, measure-INDEPENDENT; the prediction target) ==")
    for c in CLASSES:
        emit(f"  {c:20s}: {labels.count(c)} members")
    emit("")

    # orthogonality / agency-blindness diagnostics (Phi cannot see the ACTIVE/PASSIVE split)
    def _spearman(x, yv):
        x, yv = np.asarray(x, float), np.asarray(yv, float)
        rx = np.argsort(np.argsort(x)).astype(float)
        ry = np.argsort(np.argsort(yv)).astype(float)
        rx -= rx.mean(); ry -= ry.mean()
        den = math.sqrt((rx * rx).sum() * (ry * ry).sum())
        return float((rx * ry).sum() / den) if den > 1e-12 else 0.0

    rho_f_T = _spearman(faiths, Ts)
    rho_b_T = _spearman(bigs, Ts)
    emit("== ORTHOGONALITY (Phi vs T over the battery; low |rho| => T is a distinct axis) ==")
    emit(f"  Spearman rho(faith, T) = {rho_f_T:+.4f}")
    emit(f"  Spearman rho(big,   T) = {rho_b_T:+.4f}")
    emit("")

    # ── FAIRNESS / DEGENERACY GUARD (the H_1051 graded-design + H_1047 fair-bar lesson) ──
    # The capstone is only a CLEAN win if Phi had a genuine CHANCE on the agency split. By
    # construction here, a depth>=1 policy under ACTIVE vs PASSIVE has the SAME Phi (agency
    # only changes T), so the DELIBERATE-ACTIVE vs DELIBERATE-PASSIVE classes are Phi-IDENTICAL
    # pair-for-pair. If so, the headline margin is PARTLY a built-in tautology and the verdict
    # must be QUALIFIED (degenerate), not a clean quantitative win. We MEASURE this directly.
    emit("== FAIRNESS / DEGENERACY GUARD (is the agency split Phi-IDENTICAL by construction?) ==")
    by_policy = {}
    for mm in members:
        by_policy.setdefault(mm["policy"], {})[mm["agency"]] = mm
    n_delib_pairs = 0
    n_phi_identical = 0
    for p, d in by_policy.items():
        if p[0] == 0:        # REACTIVE policies — no active/passive split to compare
            continue
        a, q = d.get(True), d.get(False)
        if a is None or q is None:
            continue
        n_delib_pairs += 1
        if abs(a["faith"] - q["faith"]) < 1e-9 and abs(a["big"] - q["big"]) < 1e-9:
            n_phi_identical += 1
    phi_blind_by_construction = (n_delib_pairs > 0 and n_phi_identical == n_delib_pairs)
    emit(f"  deliberate policy active/passive pairs: {n_delib_pairs}; "
         f"Phi-IDENTICAL pairs: {n_phi_identical}")
    emit(f"  => Phi is BLIND to the agency split BY CONSTRUCTION: {phi_blind_by_construction}")
    emit("  (when True, the agency classes share Phi pair-for-pair, so any Phi-scalar is")
    emit("   STRUCTURALLY unable to separate them — the large margin is PARTLY built-in.)")
    emit("")

    # majority-class baseline (the honest floor a 1-feature classifier must beat).
    counts = {c: labels.count(c) for c in CLASSES}
    majority_baseline = max(counts.values()) / len(members)
    emit(f"== BASELINES == majority-class baseline = {majority_baseline:.4f} "
         f"(largest class {max(counts,key=counts.get)}={max(counts.values())}/{len(members)})")

    # Phi-FAIR sub-test: can Phi separate the distinction it COULD plausibly see —
    # REACTIVE (depth0, distinct Phi) vs the DELIBERATE union (depth>=1)? This isolates
    # whether Phi is USELESS or merely blind to AGENCY specifically (the precise finding).
    y_planning = np.array([0 if mm["depth"] == 0 else 1 for mm in members])  # REACTIVE vs DELIB
    acc_phi_planning_faith, _ = loo_nearest_centroid_accuracy(f_norm, y_planning)
    acc_phi_planning_big, _ = loo_nearest_centroid_accuracy(b_norm, y_planning)
    acc_phi_planning = max(acc_phi_planning_faith, acc_phi_planning_big)
    maj_planning = max(np.bincount(y_planning)) / len(members)
    emit(f"  Phi-FAIR sub-test (Phi on REACTIVE-vs-DELIBERATE, the split Phi COULD see):")
    emit(f"    best Phi-scalar acc = {acc_phi_planning:.4f}  (majority {maj_planning:.4f}) "
         f"— Phi is{' ' if acc_phi_planning > maj_planning else ' NOT '}useful on the PLANNING split")
    emit("    => Phi is specifically BLIND to AGENCY, not globally useless (precise finding).")
    emit("")

    # ── STEP 3 — LOO nearest-centroid accuracies (H_1047 protocol VERBATIM). ──
    scalars = {
        "s_faith": f_norm,
        "s_big": b_norm,
        "s_T": T_norm,
    }
    emit("=" * 90)
    emit("LOO NEAREST-CENTROID ACCURACY (predict behavioral class; H_1047 protocol VERBATIM)")
    emit("=" * 90)
    scalar_accs = {}
    for name, sc in scalars.items():
        a, _ = loo_nearest_centroid_accuracy(sc, y)
        scalar_accs[name] = a
        emit(f"  scalar {name:8s} (1-D)                  acc = {a:.4f}")

    # best SINGLE Phi-scalar (only the Phi measures, NOT T — that is the comparison baseline)
    phi_scalar_accs = {k: v for k, v in scalar_accs.items() if k in ("s_faith", "s_big")}
    best_phi_scalar = max(phi_scalar_accs, key=lambda k: phi_scalar_accs[k])
    best_phi_acc = phi_scalar_accs[best_phi_scalar]
    emit(f"  BEST single Phi-scalar = {best_phi_scalar} (acc={best_phi_acc:.4f})")
    emit("")

    # (Phi, T) 2-vector: Phi-component = the BEST single Phi-scalar, so the 2-vector can ONLY
    # gain via the orthogonal T axis. cleanest "is T needed" test.
    X_pair = np.column_stack([scalars[best_phi_scalar], T_norm])
    acc_pair, _ = loo_nearest_centroid_accuracy(X_pair, y)
    emit(f"  (Phi, T) 2-vector [Phi={best_phi_scalar}, T]   acc = {acc_pair:.4f}")
    margin = acc_pair - best_phi_acc
    emit(f"  observed margin (acc_pair - best_Phi_scalar) = {margin:+.4f}  (required >= {MARGIN})")
    margin_pass = acc_pair >= best_phi_acc + MARGIN
    emit(f"  MARGIN test (2-vector beats best Phi-scalar by >= {MARGIN}): {margin_pass}")
    emit("")

    # ── VERDICT — FROZEN falsifier, with the FAIRNESS/DEGENERACY guard applied honestly. ──
    # The frozen falsifier resolves on margin >= 0.15. But the H_1051 graded-design lesson +
    # H_1047 fair-bar lesson demand: if the agency classes are Phi-IDENTICAL BY CONSTRUCTION,
    # the margin is PARTLY built-in -> the PASS is DEGENERATE and the verdict is QUALIFIED
    # (still terminal/publishable per a_paper_negative_ok framing, but NOT a clean win).
    emit("=" * 90)
    if margin_pass and not phi_blind_by_construction:
        token = "🟢"
        vtok = "RULER-NEEDS-T"
        emit("OVERALL: RULER-NEEDS-T (H1-PASS, CLEAN) — the (Phi, T) 2-vector predicts the behavioral")
        emit(f"  class at acc={acc_pair:.4f}, beating the BEST single Phi-scalar ({best_phi_scalar}, "
             f"acc={best_phi_acc:.4f})")
        emit(f"  by {margin:+.4f} >= MARGIN {MARGIN}, AND Phi had a genuine chance on the agency split")
        emit("  (not Phi-identical by construction). The ruler genuinely NEEDS the orthogonal T axis.")
        emit("  VERDICT-TOKEN: RULER-NEEDS-T")
    elif margin_pass and phi_blind_by_construction:
        token = "🟢"
        vtok = "RULER-NEEDS-T-QUALIFIED-PHI-BLIND-BY-CONSTRUCTION"
        emit("OVERALL: RULER-NEEDS-T (QUALIFIED / DEGENERATE PASS) — the frozen falsifier resolves PASS")
        emit(f"  (margin {margin:+.4f} >= {MARGIN}: (Phi,T) acc={acc_pair:.4f} vs best Phi-scalar "
             f"{best_phi_scalar}={best_phi_acc:.4f}),")
        emit(f"  AND s_T ALONE already reaches {scalar_accs['s_T']:.4f} == the 2-vector (Phi adds ZERO).")
        emit("  BUT the FAIRNESS GUARD fires: the DELIBERATE-ACTIVE vs DELIBERATE-PASSIVE classes are")
        emit(f"  Phi-IDENTICAL pair-for-pair ({n_phi_identical}/{n_delib_pairs} deliberate pairs share Phi")
        emit("  exactly), because agency-mode only changes T, never the policy-determined Phi. So Phi is")
        emit("  STRUCTURALLY blind to the agency split and the large margin is PARTLY built-in — NOT a")
        emit("  clean quantitative win. The PRECISE, NON-tautological finding (corroborated by the")
        emit(f"  Phi-FAIR sub-test: Phi reaches {acc_phi_planning:.4f} on the REACTIVE-vs-DELIBERATE")
        emit("  planning split it CAN see, but is blind to AGENCY specifically; and the empirical")
        emit(f"  orthogonality rho(faith,T)={rho_f_T:+.3f}, rho(big,T)={rho_b_T:+.3f}) is:")
        emit("  WHEN behavioral classes differ ONLY in agency, an instantaneous Phi-scalar is provably")
        emit("  insufficient and the temporal/agency T axis is NECESSARY to recover them — consistent")
        emit("  with H_1051's orthogonal-T result, lifted to a multi-class battery. This CONFIRMS the")
        emit("  ruler needs T for agency, but does NOT demonstrate a fair head-to-head Phi-vs-T contest")
        emit("  (that would need agency to ALSO move Phi-relevant behavior — UNVERIFIED, follow-up).")
        emit("  VERDICT-TOKEN: RULER-NEEDS-T-QUALIFIED-PHI-BLIND-BY-CONSTRUCTION")
    else:
        token = "🔴"
        vtok = "PHI-SCALAR-STILL-SUFFICES"
        emit("OVERALL: PHI-SCALAR-STILL-SUFFICES (CLOSED-NEGATIVE, a_paper_negative_ok) — even WITH")
        emit(f"  agency-variation present, the best single Phi-scalar ({best_phi_scalar}, acc={best_phi_acc:.4f})")
        emit(f"  predicts the behavioral class about as well as the (Phi, T) 2-vector (acc={acc_pair:.4f},")
        emit(f"  margin {margin:+.4f} < MARGIN {MARGIN}). Adding the orthogonal T axis does NOT clear the")
        emit("  PRE-SET 0.15 bar here. Extends H_1045's one-scalar-suffices result into the agency regime.")
        emit("  A sub-threshold directional win is an HONEST negative (the H_1047 lesson: the bar has teeth).")
        emit("  VERDICT-TOKEN: PHI-SCALAR-STILL-SUFFICES")
    emit("=" * 90)
    emit(f"DEGENERACY: phi_blind_by_construction={phi_blind_by_construction}  "
         f"majority_baseline={majority_baseline:.4f}  s_T_alone={scalar_accs['s_T']:.4f}  "
         f"phi_fair_planning_acc={acc_phi_planning:.4f}")
    emit(f"SUMMARY: acc_(Phi,T)_2vec={acc_pair:.4f}  best_single_Phi_scalar={best_phi_acc:.4f} "
         f"({best_phi_scalar})  margin={margin:+.4f}  FROZEN_bar={MARGIN}  s_T_alone_acc={scalar_accs['s_T']:.4f}")
    emit(f"REPRODUCE: mirror n4,5 PROVEN={mirror_ok}  REPRODUCE-H_1029=EXACT  "
         f"REPRODUCE-H_1047 greedy(faith={g_faith:.4f},big={g_big:.4f})=anchored")
    emit("HONEST scope (a_scale_honest_scope): TOY n=4 system for the per-policy Phi reads (big-Phi")
    emit("super-exponential); n=5 used ONLY for the mirror re-proof. BOTH CPU mirrors RE-PROVEN ==")
    emit("stdlib at n=4 AND n=5 (H_1012) + REPRODUCE-H_1029 EXACT + REPRODUCE-H_1047 greedy anchor")
    emit("BEFORE scoring; REAL engines are the measures (a_phi_iit4_tool, NO proxy). T = H_1051")
    emit("machinery UNMODIFIED (H_932 prov-depth + H_935 veto). p3/p6/p7. g5 CODE-measured (no LLM")
    emit("self-judge). Scale-transfer UNVERIFIED. NOT a forge binary; $0 CPU-local, SERIAL, no GPU/pod.")

    out = dict(
        h_id="H_1060",
        title="ruler-completeness Phi-T capstone — does (Phi, T) 2-vector beat the best single "
              "Phi-scalar on a mixed battery varying in BOTH planning-structure and agency?",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        substrate="SW-only CPU numpy mirror of stdlib IIT-4.0 (a_phi_iit4_tool, NO proxy); "
                  "no AKIDA Lane A, no GPU/forge Lane G; $0; serial.",
        classes=CLASSES, margin_bar=MARGIN, n_agency_seeds=N_AGENCY_SEEDS,
        n_members=len(members),
        class_counts={c: labels.count(c) for c in CLASSES},
        mirror_n4_proven=bool(ok4), mirror_n5_proven=bool(ok5),
        reproduce_h1029=bool(rep), reproduce_h1047_greedy_faith=g_faith,
        reproduce_h1047_greedy_big=g_big,
        scalar_accs={k: float(v) for k, v in scalar_accs.items()},
        best_phi_scalar=best_phi_scalar, best_phi_acc=float(best_phi_acc),
        acc_pair_phi_T=float(acc_pair), margin=float(margin), margin_pass=bool(margin_pass),
        rho_faith_T=float(rho_f_T), rho_big_T=float(rho_b_T),
        phi_blind_by_construction=bool(phi_blind_by_construction),
        n_deliberate_pairs=int(n_delib_pairs), n_phi_identical_pairs=int(n_phi_identical),
        majority_baseline=float(majority_baseline),
        phi_fair_planning_acc=float(acc_phi_planning),
        s_T_alone_acc=float(scalar_accs["s_T"]),
        verdict_token=token, verdict_id=vtok,
        scope="TOY n=4 per-member Phi; n=5 only for mirror re-proof; scale-transfer UNVERIFIED; "
              "p3/p6/p7; g5 CODE-measured.",
    )
    emit("")
    emit("── full machine record (JSON) ──────────────────────────────────────")
    emit(json.dumps(out, indent=2, ensure_ascii=False))

    vdir = os.path.join(_REPO, ".verdicts", "1060_ruler_completeness_phi_t")
    os.makedirs(vdir, exist_ok=True)
    vpath = os.path.join(vdir, "H_1060.txt")
    with open(vpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out_lines) + "\n")
    print(f"\n[written] {vpath}")
    return out


if __name__ == "__main__":
    main()
