#!/usr/bin/env python3
"""h1061_fair_phi_vs_t_contest.py — H_1061: FAIR Phi-vs-T contest.

QUESTION (closes the H_1060 QUALIFIED / DEGENERATE residual)
============================================================
H_1060 (RULER-NEEDS-T) was QUALIFIED: its +0.60 margin was partly BUILT-IN because the
DELIBERATE-ACTIVE vs DELIBERATE-PASSIVE classes were Phi-IDENTICAL pair-for-pair (24/24) —
agency-mode moved ONLY T, never Phi — so a Phi-scalar was *structurally* unable to separate
them. H_1060 flagged the open follow-up VERBATIM: "a fair head-to-head Phi-vs-T contest (agency
also moving Phi-relevant behavior) is UNVERIFIED."

THIS hypothesis closes it. Build a FAIR battery where agency-mode ALSO co-varies Phi-relevant
behavioral structure (NOT Phi-identical pairs) — so NEITHER axis is structurally privileged —
and re-run the head-to-head: does T STILL add discriminative power over the best single
Phi-scalar when Phi is genuinely allowed to move with agency?

THE FIX (anti-degeneracy)
-------------------------
In rich_rollout(seed, depth, explore, mix) the realized n=4 state distribution (hence faithful
phi_EI and big-Phi) is a deterministic function of (depth, explore, mix). H_1060 held (e, m)
FIXED across agency, so Phi was agency-blind by construction. Here agency SETS the Phi-driving
(explore, mix) to OPPOSITE absolute corners (NON-saturating, so it ALWAYS moves Phi):
  ACTIVE  = committed plan -> (ACT_E, ACT_M) = (0.00, 0.0),  active=True  (deep prov + real veto)
  PASSIVE = drifting  plan -> (PAS_E, PAS_M) = (0.20, 0.5),  active=False (shallow prov + sat veto)
=> the SAME deliberate base policy under ACTIVE vs PASSIVE has a DIFFERENT Phi AND a DIFFERENT T.
The deliberate battery is swept by DEPTH only ({1,2,4,8}), so EVERY deliberate pair is guaranteed
a genuine Phi-contrast (the additive+cap coupling of the first cut saturated 4/24 pairs at the
(e=0.20,mix=0.5) corner -> variance-0 tautology cells, the H_1051 idealized-binary lesson; the
opposite-corner coupling removes that defect BEFORE any terminal scoring). REACTIVE = depth-0
greedy, one cell per agency (agency cannot move a depth-0 reactive Phi -> still REACTIVE).

THE KEY NEW PIECE = the anti-tautology NON-DEGENERACY guard (converse of H_1060's fairness
guard): explicitly MEASURE + ASSERT the agency classes are NOT Phi-identical (per-pair
|dphi| > FLOOR=1e-3) and report the full distribution. This is what makes H_1061 a genuine new
measurement, not a re-run.

REUSE (verbatim, no reinvention — a_phi_iit4_tool)
--------------------------------------------------
- H_1047 module exec'd with __main__ stripped -> H_1035 policy battery, substrate_reads (BOTH
  stdlib IIT-4.0 engines, n=4, NO proxy), the H_1012 prove_mirrors_at_n proof (n=4 AND n=5),
  reproduce_h1029_check, rich_rollout, AND loo_nearest_centroid_accuracy — byte-for-byte.
- H_1051 module by path -> _provenance_depth (H_932) + _veto_capacity (H_935) UNMODIFIED + PureField.

FROZEN design (UNIVERSE/H_1061_fair_phi_vs_t_contest.md, BEFORE measuring):
  classes: REACTIVE / DELIBERATE-ACTIVE / DELIBERATE-PASSIVE (structural, measure-INDEPENDENT).
  features: PAIR (best-Phi-scalar-norm, T-norm) 2-D; scalars s_faith, s_big, s_T (1-D each).
  classifier: H_1047 loo_nearest_centroid_accuracy. MARGIN = 0.15 (SAME bar; FROZEN).
  non-degeneracy FLOOR = 1e-3 (FROZEN). s_T-saturation eps = 1e-9.
  H1-PASS = RULER-GENUINELY-NEEDS-BOTH : non-deg PASS AND margin >= 0.15 AND acc_pair > acc_sT+eps.
  FAIL (a) PHI-ABSORBS-AGENCY  : non-deg PASS AND margin < 0.15  (a_paper_negative_ok).
  FAIL (b) NON-DEGENERATE-T-DOMINANT : non-deg PASS AND margin >= 0.15 AND acc_sT >= acc_pair-eps.

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

prove_mirrors_at_n = _h1047.prove_mirrors_at_n          # H_1012: BOTH engines, any n
substrate_reads = _h1047.substrate_reads                # H -> {big, faith, ...} (n=4)
rich_rollout = _h1047.rich_rollout                      # parameterized H_1035 rollout
reproduce_h1029_check = _h1047.reproduce_h1029_check
policies = _h1047.policies                              # H_1035 richer policy space
pol_name = _h1047.pol_name
loo_nearest_centroid_accuracy = _h1047.loo_nearest_centroid_accuracy  # H_1047 LOO protocol
N_SEEDS = _h1047.N_SEEDS                                 # H_1035 seed count (30); Phi = seed-mean


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
_provenance_depth = _h1051._provenance_depth            # H_932 verified-link DEPTH, UNMODIFIED
_veto_capacity = _h1051._veto_capacity                  # H_935 active-veto fraction, UNMODIFIED
H1051_GATE_TICKS = _h1051.GATE_TICKS


# ── FROZEN H_1061 design (H_1061_fair_phi_vs_t_contest.md). ──
CLASSES = ["REACTIVE", "DELIBERATE-ACTIVE", "DELIBERATE-PASSIVE"]  # frozen order = tie-break
MARGIN = 0.15
NONDEG_FLOOR = 1e-3       # per-pair |dphi| floor: classes must NOT be Phi-identical (FROZEN)
SAT_EPS = 1e-9           # s_T-saturation sub-clause epsilon (deterministic LOO)
N_AGENCY_SEEDS = 12       # agency-mode seeds per (policy, agency) cell; T-machinery is the cost

# deliberate base policies swept by DEPTH only (agency sets explore/mix), so every deliberate
# pair is guaranteed a Phi-contrast (no cap-saturation tautology cell). FROZEN.
DELIB_DEPTHS = [1, 2, 4, 8]   # H_1035 depths > 0 (depth 0 == greedy == REACTIVE)
# agency -> Phi-relevant coupling (FROZEN): OPPOSITE absolute corners (NON-saturating).
ACT_E, ACT_M = 0.00, 0.0   # ACTIVE  = committed plan (low explore / no greedy-mix)
PAS_E, PAS_M = 0.20, 0.5   # PASSIVE = drifting / forced plan (high explore / greedy-mix)


def behavioral_class(depth, agency):
    """Structural behavioral class spanning BOTH axes. measure-INDEPENDENT.
    agency in {True=ACTIVE, False=PASSIVE}."""
    if depth == 0:
        return "REACTIVE"
    return "DELIBERATE-ACTIVE" if agency else "DELIBERATE-PASSIVE"


def agency_rollout_params(agency):
    """FAIR coupling: agency SETS the Phi-driving rollout params to opposite absolute corners.
    ACTIVE  = committed plan (ACT_E, ACT_M).
    PASSIVE = drifting/forced plan (PAS_E, PAS_M).  NON-saturating -> always a Phi-contrast."""
    return (ACT_E, ACT_M) if agency else (PAS_E, PAS_M)


def _zscore(v):
    v = np.asarray(v, float)
    s = v.std()
    return (v - v.mean()) / s if s > 1e-12 else np.zeros_like(v)


def main():
    print("=" * 90)
    print("H_1061 — FAIR Phi-vs-T contest: closes the H_1060 QUALIFIED/DEGENERATE residual")
    print("agency co-varies Phi-relevant behavior (NOT Phi-identical pairs); re-run head-to-head.")
    print("substrate=CPU-mirror (numpy) — H_1047/H_1035/H_1014/H_1004 engines + H_1012 proof")
    print("                              + H_1051 T-machinery (H_932 prov-depth + H_935 veto), all verbatim")
    print(f"FROZEN: classes={CLASSES}  MARGIN={MARGIN}  NONDEG_FLOOR={NONDEG_FLOOR}  agency_seeds={N_AGENCY_SEEDS}")
    print("=" * 90)
    print()

    out_lines = []

    def emit(s=""):
        print(s, flush=True)
        out_lines.append(s)

    emit("=" * 90)
    emit("H_1061 — FAIR Phi-vs-T contest (closes H_1060 QUALIFIED residual; agency co-varies Phi)")
    emit("verdict-gate g73 — raw measurement, verbatim (committed BEFORE the .md emoji tier)")
    emit("substrate: CPU-local numpy mirror of stdlib IIT-4.0 (a_phi_iit4_tool, NO proxy); $0; serial.")
    emit("big-Phi:      hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    emit("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    emit("T:            z(provenance-depth, H_932) + z(veto-capacity, H_935)  [H_1051 machinery, UNMODIFIED]")
    emit(f"FAIR coupling: ACTIVE = committed plan (e={ACT_E},mix={ACT_M}); PASSIVE = drifting plan "
         f"(e={PAS_E},mix={PAS_M}).")
    emit(f"               deliberate base = DEPTH sweep {DELIB_DEPTHS} (agency sets e/mix). "
         "=> agency moves BOTH Phi AND T, NON-degenerately.")
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
    def _phi_seedmean(depth, explore, mix):
        fs, bs = [], []
        for s in range(N_SEEDS):
            r = substrate_reads(rich_rollout(s, depth, explore, mix))
            fs.append(float(r["faith"])); bs.append(float(r["big"]))
        return float(np.mean(fs)), float(np.mean(bs))

    emit("== STEP 0b: REPRODUCE-H_1047 anchor — greedy policy (0,0.0,0.0) SEED-MEAN faith/big ==")
    g_faith, g_big = _phi_seedmean(0, 0.0, 0.0)
    rep1047_faith = abs(g_faith - 0.5069) < 1e-3
    rep1047_big = abs(g_big - 9.5283) < 1e-3
    rep1047 = rep1047_faith and rep1047_big
    emit(f"  greedy faith={g_faith:.5f} (H_1047 ref 0.50693, |d|={abs(g_faith-0.50693):.2e}, OK={rep1047_faith})")
    emit(f"  greedy big  ={g_big:.5f} (H_1047 ref 9.52829, |d|={abs(g_big-9.52829):.2e}, OK={rep1047_big})")
    emit(f"  REPRODUCE-H_1047 (greedy seed-mean faith/big anchor matches published): {rep1047}")
    if not rep1047:
        raise SystemExit("REPRODUCE-H_1047 anchor mismatch — aborting (harness drift)")
    emit("")

    # ── STEP 1 — build the FAIR MIXED battery. ──
    # cells = REACTIVE (depth-0 greedy, one per agency) + DELIBERATE (DEPTH sweep x agency).
    # agency SETS the Phi-driving (explore, mix) to opposite corners, so each deliberate pair
    # has a DIFFERENT Phi AND a DIFFERENT T (NON-degenerate by construction; no cap-saturation).
    cells = [(0, ag) for ag in (True, False)]                    # REACTIVE: depth-0 x agency
    cells += [(d, ag) for d in DELIB_DEPTHS for ag in (True, False)]  # DELIBERATE: depth x agency
    emit(f"== STEP 1: FAIR MIXED battery — REACTIVE(depth0 x{{ACT,PAS}}) + "
         f"DELIBERATE(depths {DELIB_DEPTHS} x{{ACT,PAS}}); agency seeds={N_AGENCY_SEEDS} ==")
    emit("   (Phi read PER (depth, agency); agency sets explore/mix to opposite corners.)")
    t0 = time.time()

    # each cell emits N_AGENCY_SEEDS members: Phi SHARED within the cell (one seed-mean read,
    # the H_1047/H_1035 path VERBATIM), T computed PER agency-seed (H_1051 machinery UNMODIFIED)
    # — exactly the H_1060 member structure, with the Phi/agency coupling added.
    members = []
    for ci, (d, agency) in enumerate(cells):
        e_eff, m_eff = agency_rollout_params(agency)
        # Phi for this (depth, agency) — seed-mean over the H_1047/H_1035 path, VERBATIM.
        # depth-0 (REACTIVE) ignores explore/mix in rich_rollout, so both agency cells share Phi
        # (a depth-0 reaction has no plan to be active/passive ABOUT — declared in the .md).
        faith, big = _phi_seedmean(d, e_eff, m_eff)
        for s in range(N_AGENCY_SEEDS):
            rng = np.random.default_rng((ci * 9173 + s * 31 + (1 if agency else 0)) & 0x7fffffff)
            ph0 = tuple(float(rng.uniform(-0.5, 0.5)) for _ in range(3))
            am0 = tuple(float(0.1 + rng.uniform(-0.02, 0.02)) for _ in range(3))
            pf = PureField(phase0=ph0, amp0=am0)
            veto = _veto_capacity(pf, H1051_GATE_TICKS, active=agency, rng=rng)
            depth_prov = _provenance_depth(active=agency, seed_tag=(ci * 1000 + s), rng=rng)
            members.append(dict(
                policy=(d, e_eff, m_eff), depth=d, agency=agency, e_eff=e_eff, m_eff=m_eff,
                faith=faith, big=big,
                prov_depth=float(depth_prov), veto_cap=float(veto),
                cls=behavioral_class(d, agency),
            ))
        emit(f"  [{ci+1:2d}/{len(cells)}] depth={d} agency={'ACT' if agency else 'PAS'} "
             f"(e={e_eff:.2f},mix={m_eff:.1f})  faith={faith:7.4f} big={big:8.4f}  "
             f"x{N_AGENCY_SEEDS} members  elapsed={time.time()-t0:6.1f}s")
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

    # ── NON-DEGENERACY GUARD (THE KEY NEW PIECE — converse of H_1060's fairness guard). ──
    # Assert the deliberate ACTIVE vs PASSIVE classes are NOT Phi-identical pair-for-pair, so
    # the contest is FAIR (Phi had a genuine chance on the agency split). Report distribution.
    emit("== NON-DEGENERACY GUARD (THE KEY NEW PIECE — are agency classes NOT Phi-identical?) ==")
    by_depth = {}        # pair the deliberate ACTIVE/PASSIVE cells of the SAME depth
    for mm in members:
        by_depth.setdefault(mm["depth"], {})[mm["agency"]] = mm
    dphi_faith_list, dphi_big_list = [], []
    n_delib_pairs = 0
    n_nondeg_pairs = 0
    for d, dct in by_depth.items():
        if d == 0:        # REACTIVE — no active/passive deliberate split (depth-0 reaction)
            continue
        a, q = dct.get(True), dct.get(False)
        if a is None or q is None:
            continue
        n_delib_pairs += 1
        df = abs(a["faith"] - q["faith"]); dbg = abs(a["big"] - q["big"])
        dphi_faith_list.append(df); dphi_big_list.append(dbg)
        if df > NONDEG_FLOOR or dbg > NONDEG_FLOOR:
            n_nondeg_pairs += 1
    non_degenerate = (n_delib_pairs > 0 and n_nondeg_pairs == n_delib_pairs)
    df_arr = np.array(dphi_faith_list, float); dbg_arr = np.array(dphi_big_list, float)
    emit(f"  deliberate ACTIVE/PASSIVE pairs: {n_delib_pairs};  "
         f"NON-Phi-identical pairs (|dphi|>{NONDEG_FLOOR}): {n_nondeg_pairs}")
    emit(f"  |dphi_faith| distribution: min={df_arr.min():.4f} median={np.median(df_arr):.4f} "
         f"max={df_arr.max():.4f}")
    emit(f"  |dphi_big|   distribution: min={dbg_arr.min():.4f} median={np.median(dbg_arr):.4f} "
         f"max={dbg_arr.max():.4f}")
    emit(f"  => agency classes are NON-Phi-identical (FAIR contest, Phi can move): {non_degenerate}")
    emit("  (this is the anti-tautology guard — the EXACT failure H_1060 self-flagged. The")
    emit("   head-to-head below is only honest when this is True: Phi had a genuine chance.)")
    if not non_degenerate:
        emit("  !! NON-DEGENERACY FAILED — battery still Phi-identical; contest NOT fair. !!")
    emit("")

    # majority-class baseline (the honest floor a 1-feature classifier must beat).
    counts = {c: labels.count(c) for c in CLASSES}
    majority_baseline = max(counts.values()) / len(members)
    emit(f"== BASELINES == majority-class baseline = {majority_baseline:.4f} "
         f"(largest class {max(counts,key=counts.get)}={max(counts.values())}/{len(members)})")
    emit("")

    # orthogonality diagnostics
    def _spearman(x, yv):
        x, yv = np.asarray(x, float), np.asarray(yv, float)
        rx = np.argsort(np.argsort(x)).astype(float)
        ry = np.argsort(np.argsort(yv)).astype(float)
        rx -= rx.mean(); ry -= ry.mean()
        den = math.sqrt((rx * rx).sum() * (ry * ry).sum())
        return float((rx * ry).sum() / den) if den > 1e-12 else 0.0

    rho_f_T = _spearman(faiths, Ts)
    rho_b_T = _spearman(bigs, Ts)
    emit("== ORTHOGONALITY (Phi vs T over the battery) ==")
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

    phi_scalar_accs = {k: v for k, v in scalar_accs.items() if k in ("s_faith", "s_big")}
    best_phi_scalar = max(phi_scalar_accs, key=lambda k: phi_scalar_accs[k])
    best_phi_acc = phi_scalar_accs[best_phi_scalar]
    emit(f"  BEST single Phi-scalar = {best_phi_scalar} (acc={best_phi_acc:.4f})")
    emit("")

    # (Phi, T) 2-vector: Phi-component = the BEST single Phi-scalar.
    X_pair = np.column_stack([scalars[best_phi_scalar], T_norm])
    acc_pair, _ = loo_nearest_centroid_accuracy(X_pair, y)
    emit(f"  (Phi, T) 2-vector [Phi={best_phi_scalar}, T]   acc = {acc_pair:.4f}")
    margin = acc_pair - best_phi_acc
    emit(f"  observed margin (acc_pair - best_Phi_scalar) = {margin:+.4f}  (required >= {MARGIN})")
    margin_pass = acc_pair >= best_phi_acc + MARGIN
    emit(f"  MARGIN test (2-vector beats best Phi-scalar by >= {MARGIN}): {margin_pass}")
    # does Phi ALSO contribute (s_T-alone does NOT already saturate the 2-vector)?
    sT_acc = scalar_accs["s_T"]
    phi_contributes = acc_pair > sT_acc + SAT_EPS
    emit(f"  s_T-alone acc = {sT_acc:.4f}; (Phi,T) acc = {acc_pair:.4f}; "
         f"Phi ALSO contributes (acc_pair > s_T + {SAT_EPS}): {phi_contributes}")
    emit("")

    # ── VERDICT — FROZEN falsifier with the NON-DEGENERACY guard applied honestly. ──
    emit("=" * 90)
    if not non_degenerate:
        token = "🟠"
        vtok = "CONTEST-NOT-FAIR-VOID"
        emit("OVERALL: CONTEST-NOT-FAIR (VOID) — the non-degeneracy guard FAILED: agency classes are")
        emit("  still Phi-identical, so the head-to-head is NOT fair (same trap H_1060 fell into).")
        emit("  No honest verdict on the Phi-vs-T contest. (Should not happen given the FAIR coupling.)")
        emit("  VERDICT-TOKEN: CONTEST-NOT-FAIR-VOID")
    elif margin_pass and phi_contributes:
        token = "🟢"
        vtok = "RULER-GENUINELY-NEEDS-BOTH"
        emit("OVERALL: RULER-GENUINELY-NEEDS-BOTH (H1-PASS, NON-DEGENERATE) — on a Phi-FAIR battery")
        emit(f"  (agency co-varies Phi; classes NON-Phi-identical, {n_nondeg_pairs}/{n_delib_pairs}")
        emit(f"  deliberate pairs differ in Phi, |dphi_faith| up to {df_arr.max():.3f} / |dphi_big| up to")
        emit(f"  {dbg_arr.max():.3f}), the (Phi, T) 2-vector predicts the behavioral class at "
             f"acc={acc_pair:.4f},")
        emit(f"  beating the BEST single Phi-scalar ({best_phi_scalar}, acc={best_phi_acc:.4f}) by "
             f"{margin:+.4f} >= {MARGIN}")
        emit(f"  AND s_T-alone ({sT_acc:.4f}) does NOT saturate the 2-vector (Phi ALSO contributes).")
        emit("  Even when Phi is genuinely allowed to move with agency, the ruler NEEDS BOTH axes —")
        emit("  the H_1060 result survives the fair head-to-head, NON-degenerately. VERDICT-TOKEN: "
             "RULER-GENUINELY-NEEDS-BOTH")
    elif margin_pass and not phi_contributes:
        token = "🟢"
        vtok = "NON-DEGENERATE-T-DOMINANT"
        emit("OVERALL: NON-DEGENERATE-T-DOMINANT (H1-PASS but T-dominant; a_paper_negative_ok framing)")
        emit(f"  On a Phi-FAIR battery (NON-Phi-identical classes, {n_nondeg_pairs}/{n_delib_pairs} pairs")
        emit(f"  differ in Phi), the (Phi, T) 2-vector (acc={acc_pair:.4f}) beats the best Phi-scalar "
             f"({best_phi_scalar},")
        emit(f"  acc={best_phi_acc:.4f}) by {margin:+.4f} >= {MARGIN} — BUT s_T-alone already reaches "
             f"{sT_acc:.4f}")
        emit("  == the 2-vector (Phi adds ~0). So even when Phi CAN move with agency, the class signal")
        emit("  is carried by T; Phi does not add separating power on top. This is a NON-DEGENERATE")
        emit("  T-dominant result (the H_1060 degeneracy is removed — Phi had a genuine chance and")
        emit("  still does not help) — distinct from H_1060's built-in margin. VERDICT-TOKEN: "
             "NON-DEGENERATE-T-DOMINANT")
    else:
        token = "🔴"
        vtok = "PHI-ABSORBS-AGENCY"
        emit("OVERALL: PHI-ABSORBS-AGENCY (CLOSED-NEGATIVE, a_paper_negative_ok) — on a Phi-FAIR battery")
        emit(f"  (agency co-varies Phi; NON-Phi-identical classes, {n_nondeg_pairs}/{n_delib_pairs} pairs")
        emit(f"  differ in Phi), the best single Phi-scalar ({best_phi_scalar}, acc={best_phi_acc:.4f})")
        emit(f"  predicts the behavioral class about as well as the (Phi, T) 2-vector (acc={acc_pair:.4f},")
        emit(f"  margin {margin:+.4f} < MARGIN {MARGIN}). Once Phi is allowed to MOVE with agency, a")
        emit("  Phi-scalar ABSORBS the agency signal and the orthogonal T axis is REDUNDANT — the")
        emit("  H_1060 'needs-T' result was an artifact of the Phi-blind-by-construction battery, and")
        emit("  on a fair contest one Phi-scalar suffices (strengthens H_1045). A sub-threshold")
        emit("  directional win is an HONEST negative (the H_1047 lesson: the bar has teeth).")
        emit("  VERDICT-TOKEN: PHI-ABSORBS-AGENCY")
    emit("=" * 90)
    emit(f"NON-DEGENERACY: non_degenerate={non_degenerate}  delib_pairs={n_delib_pairs}  "
         f"non_phi_identical={n_nondeg_pairs}  FLOOR={NONDEG_FLOOR}")
    emit(f"  |dphi_faith| min/med/max = {df_arr.min():.4f}/{np.median(df_arr):.4f}/{df_arr.max():.4f}")
    emit(f"  |dphi_big|   min/med/max = {dbg_arr.min():.4f}/{np.median(dbg_arr):.4f}/{dbg_arr.max():.4f}")
    emit(f"SUMMARY: acc_(Phi,T)_2vec={acc_pair:.4f}  best_single_Phi_scalar={best_phi_acc:.4f} "
         f"({best_phi_scalar})  s_T_alone={sT_acc:.4f}  margin={margin:+.4f}  FROZEN_bar={MARGIN}  "
         f"margin_pass={margin_pass}  phi_contributes={phi_contributes}")
    emit(f"  majority_baseline={majority_baseline:.4f}  rho(faith,T)={rho_f_T:+.4f}  rho(big,T)={rho_b_T:+.4f}")
    emit(f"REPRODUCE: mirror n4,5 PROVEN={mirror_ok}  REPRODUCE-H_1029=EXACT  "
         f"REPRODUCE-H_1047 greedy(faith={g_faith:.5f},big={g_big:.5f})=anchored")
    emit("HONEST scope (a_scale_honest_scope): TOY n=4 system for the per-member Phi reads (big-Phi")
    emit("super-exponential); n=5 used ONLY for the mirror re-proof. BOTH CPU mirrors RE-PROVEN ==")
    emit("stdlib at n=4 AND n=5 (H_1012) + REPRODUCE-H_1029 EXACT + REPRODUCE-H_1047 greedy anchor")
    emit("BEFORE scoring; REAL engines are the measures (a_phi_iit4_tool, NO proxy). T = H_1051")
    emit("machinery UNMODIFIED (H_932 prov-depth + H_935 veto). p3/p6/p7. g5 CODE-measured (no LLM")
    emit("self-judge). Scale-transfer UNVERIFIED. NOT a forge binary; $0 CPU-local, SERIAL, no GPU/pod.")

    out = dict(
        h_id="H_1061",
        title="FAIR Phi-vs-T contest — does T still beat the best single Phi-scalar when agency "
              "ALSO moves Phi-relevant behavior (closes the H_1060 QUALIFIED residual)?",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        substrate="SW-only CPU numpy mirror of stdlib IIT-4.0 (a_phi_iit4_tool, NO proxy); "
                  "no AKIDA Lane A, no GPU/forge Lane G; $0; serial.",
        classes=CLASSES, margin_bar=MARGIN, nondeg_floor=NONDEG_FLOOR,
        n_agency_seeds=N_AGENCY_SEEDS, n_members=len(members),
        delib_depths=DELIB_DEPTHS, active_e=ACT_E, active_m=ACT_M,
        passive_e=PAS_E, passive_m=PAS_M,
        class_counts={c: labels.count(c) for c in CLASSES},
        mirror_n4_proven=bool(ok4), mirror_n5_proven=bool(ok5),
        reproduce_h1029=bool(rep), reproduce_h1047_greedy_faith=g_faith,
        reproduce_h1047_greedy_big=g_big,
        non_degenerate=bool(non_degenerate),
        n_deliberate_pairs=int(n_delib_pairs), n_non_phi_identical_pairs=int(n_nondeg_pairs),
        dphi_faith_min=float(df_arr.min()), dphi_faith_median=float(np.median(df_arr)),
        dphi_faith_max=float(df_arr.max()),
        dphi_big_min=float(dbg_arr.min()), dphi_big_median=float(np.median(dbg_arr)),
        dphi_big_max=float(dbg_arr.max()),
        scalar_accs={k: float(v) for k, v in scalar_accs.items()},
        best_phi_scalar=best_phi_scalar, best_phi_acc=float(best_phi_acc),
        acc_pair_phi_T=float(acc_pair), s_T_alone_acc=float(sT_acc),
        margin=float(margin), margin_pass=bool(margin_pass),
        phi_contributes=bool(phi_contributes),
        rho_faith_T=float(rho_f_T), rho_big_T=float(rho_b_T),
        majority_baseline=float(majority_baseline),
        verdict_token=token, verdict_id=vtok,
        scope="TOY n=4 per-member Phi; n=5 only for mirror re-proof; scale-transfer UNVERIFIED; "
              "p3/p6/p7; g5 CODE-measured.",
    )
    emit("")
    emit("── full machine record (JSON) ──────────────────────────────────────")
    emit(json.dumps(out, indent=2, ensure_ascii=False))

    vdir = os.path.join(_REPO, ".verdicts", "1061_fair_phi_vs_t_contest")
    os.makedirs(vdir, exist_ok=True)
    vpath = os.path.join(vdir, "H_1061.txt")
    with open(vpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out_lines) + "\n")
    print(f"\n[written] {vpath}")
    return out


if __name__ == "__main__":
    main()
