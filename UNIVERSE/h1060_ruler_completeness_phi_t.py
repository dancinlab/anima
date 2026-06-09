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

FROZEN design (declared in UNIVERSE/H_1060_ruler_completeness_phi_t.md BEFORE measuring):
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

    # ── STEP 0b — REPRODUCE-H_1047 numeric anchor (greedy policy faith/big read). ──
    emit("== STEP 0b: REPRODUCE-H_1047 anchor — greedy policy (depth0,e0.05,mix0.0) faith/big read ==")
    H_greedy = rich_rollout(0, 0, 0.05, 0.0)
    r_greedy = substrate_reads(H_greedy)
    g_faith, g_big = float(r_greedy["faith"]), float(r_greedy["big"])
    # H_1047/H_1035 published: policy-1 greedy faith=0.5069 big=9.5283
    rep1047_faith = abs(g_faith - 0.5069) < 1e-3
    rep1047_big = abs(g_big - 9.5283) < 1e-3
    rep1047 = rep1047_faith and rep1047_big
    emit(f"  greedy faith={g_faith:.4f} (H_1047 ref 0.5069, |Δ|={abs(g_faith-0.5069):.2e}, OK={rep1047_faith})")
    emit(f"  greedy big  ={g_big:.4f} (H_1047 ref 9.5283, |Δ|={abs(g_big-9.5283):.2e}, OK={rep1047_big})")
    emit(f"  REPRODUCE-H_1047 (greedy faith/big anchor matches published): {rep1047}")
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

    # Phi reads are per-policy (deterministic, computed once).
    pol_faith, pol_big = {}, {}
    for p in POLS:
        d, e, m = p
        H = rich_rollout(0, d, e, m)            # seed 0 for the Phi snapshot (deterministic)
        r = substrate_reads(H)
        pol_faith[p] = float(r["faith"])
        pol_big[p] = float(r["big"])

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

    # ── VERDICT — FROZEN falsifier. ──
    emit("=" * 90)
    if margin_pass:
        token = "🟢"
        vtok = "RULER-NEEDS-T"
        emit("OVERALL: RULER-NEEDS-T (H1-PASS) — once the battery varies in BOTH planning-structure")
        emit(f"  AND agency, the (Phi, T) 2-vector predicts the behavioral class at acc={acc_pair:.4f},")
        emit(f"  beating the BEST single Phi-scalar ({best_phi_scalar}, acc={best_phi_acc:.4f}) by")
        emit(f"  {margin:+.4f} >= MARGIN {MARGIN}. The orthogonal T axis carries class-information the")
        emit("  Phi-scalar is BLIND to (the DELIBERATE-ACTIVE vs DELIBERATE-PASSIVE split has the SAME")
        emit("  Phi but different T). The consciousness ruler genuinely NEEDS two axes.")
        emit("  VERDICT-TOKEN: RULER-NEEDS-T")
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
