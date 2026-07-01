"""H_1016 — robustness (n=5) + dose-response onset of the H_1014 split predictor.

MISSION
-------
H_1014 (terminal, QUALIFIED): at n=4, across the intervention SET {planning[split],
imagination, guided, chaos[no-split]}, a single MAGNITUDE threshold on the candidate
predictor Δ(cross-MIP coupling) (boundary +1.4933, read off the SAME binary discretization
that feeds BOTH stdlib IIT-4.0 engines) separates the one split-inducing intervention
(planning, +2.2983) from the three non-split ones (≤+0.6883). The pre-registered DIRECTION
(split ⟺ DECREASED coupling) was FALSIFIED — every intervention RAISES coupling; only
magnitude separates. H_1012 showed the SPLIT itself is robust across n={4,5}.

Two open robustness questions, both extending H_1014:
  PART 1 (robustness in n): re-score the SAME SET at n=5 — does the magnitude threshold still
    separate planning(split) from the non-split set, planning the sole split?
  PART 2 (dose-response onset): sweep planning depth d ∈ {1,2,3,4,6,8} (d=1=greedy baseline)
    vs greedy; locate the depth where the faithful-up/big-Φ-down SPLIT first ONSETS and whether
    the predictor Δ(cross-MIP coupling) crosses the H_1014 boundary +1.4933 at the same depth
    (monotone in depth?).

WHAT IS REUSED VERBATIM
-----------------------
- The H_1014 module: its `substrate_reads` (ONE matched binary discretization → big_phi +
  faithful_phi + the predictor reads mi_total/mi_mincut/bigphi_*), its intervention SET
  generators (gen_planning/gen_imagination/gen_guided/gen_chaos), `score_intervention`,
  `_mi_min_cut_weight`, sgn/signword. IMPORTED, not reinvented.
- H_1012 `prove_mirrors_at_n` — the per-n equivalence proof (BOTH CPU mirrors ≡ stdlib
  iit4_bigphi.hexa / iit4/faithful_phi.hexa) is run at n=4 AND n=5 BEFORE scoring.
- The ONLY new code: an n-parametric `substrate_reads_n` (H_1014's substrate_reads with
  N_UNITS a free parameter via latent_to_binary_seq(H, n)), an n-parametric scorer, and the
  depth-sweep dose-response loop. No engine logic is reinvented; the predictor is the SAME
  pure function of the SAME bits, only the unit-count n and the planning depth vary.

EQUIVALENCE PROOF (g5, BEFORE scoring; a_phi_iit4_tool, p7)
----------------------------------------------------------
H_1012 prove_mirrors_at_n(4) AND prove_mirrors_at_n(5) are run first — BOTH CPU mirrors
re-proven ≡ their stdlib IIT-4.0 engines on LIVE stdlib reference values at n=4 AND n=5
BEFORE any condition is scored, and the predictor cut-weight determinism is re-asserted.

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n={4,5} — both engines exact;
big-Phi super-exponential so n=5 is slow-but-tractable and n=6 is the honest cap (skipped, as
in H_1012). Scale-transfer UNVERIFIED. NOT a forge binary; $0 CPU-local, no GPU.
"""
import sys, os, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))
from cwm_probe_lib import cohens_d, welch_t, spearman  # noqa: E402

# ── Import the H_1014 module VERBATIM (defs only; do not run its main). ──
import importlib.util as _ilu
_h1014_path = os.path.join(HERE, "h1014_intervention_split_predictor.py")
_spec = _ilu.spec_from_file_location("h1014", _h1014_path)
_h1014 = _ilu.module_from_spec(_spec)
_src = open(_h1014_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1014_path, "exec"), _h1014.__dict__)

# Engines + harness, all from H_1014 (which imported them from H_1004 verbatim).
big_phi = _h1014.big_phi
build_mi_matrix = _h1014.build_mi_matrix
faithful_phi_from_mi = _h1014.faithful_phi_from_mi
_mi_min_cut_weight = _h1014._mi_min_cut_weight
binary_seq_to_tpm = _h1014.binary_seq_to_tpm
modal_state = _h1014.modal_state
binary_seq_to_faithful_state = _h1014.binary_seq_to_faithful_state
latent_to_binary_seq = _h1014.latent_to_binary_seq   # signature (H, n_units=N_UNITS)
planning_trajectories = _h1014.planning_trajectories
gen_planning = _h1014.gen_planning
gen_imagination = _h1014.gen_imagination
gen_guided = _h1014.gen_guided
gen_chaos = _h1014.gen_chaos
score_intervention = _h1014.score_intervention
prove_mirrors_at_n = _h1014.prove_mirrors_at_n
sgn = _h1014.sgn
signword = _h1014.signword
N_SEEDS = _h1014.N_SEEDS

H1014_BOUNDARY = 1.4933   # the n=4 separating boundary on Δ(cross-MIP coupling) from H_1014

# ═══════════════════════════════════════════════════════════════════════════
# n-PARAMETRIC substrate read — H_1014.substrate_reads with N_UNITS a free
# parameter. SAME engines, SAME predictor; only the unit-count n varies. This is
# the H_1014 read with latent_to_binary_seq(H, n) (its n_units argument, == the
# H_1012 latent_to_binary_seq_n path). No engine logic is reinvented.
# ═══════════════════════════════════════════════════════════════════════════
def substrate_reads_n(H, n_units):
    bits, n = latent_to_binary_seq(H, n_units)
    tpm, sc = binary_seq_to_tpm(bits, n)
    s = modal_state(sc)
    bres = big_phi(tpm, n, s)            # [min_loss, total, sum_d, sum_r, nd]
    bphi = bres[0]; btotal = bres[1]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    mi = build_mi_matrix(fstate, fn, fdim, 2)
    fphi = faithful_phi_from_mi(mi, fn)
    mi_total = float(np.triu(mi, 1).sum())
    mi_mincut = _mi_min_cut_weight(mi, fn)
    return dict(big=bphi, faith=fphi, mi_total=mi_total, mi_mincut=mi_mincut,
                bigphi_miploss=bphi, bigphi_total=btotal)

def _agg(rows):
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}

def score_intervention_n(name, gen, n_units, t0):
    """gen(seed) -> (H_baseline, H_intervention). Contrasts for big/faith + predictor at n_units."""
    base_rows, intv_rows = [], []
    for s in range(N_SEEDS):
        Hb, Hi = gen(s)
        base_rows.append(substrate_reads_n(Hb, n_units))
        intv_rows.append(substrate_reads_n(Hi, n_units))
        print(f"    [{name} n={n_units} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    B = _agg(base_rows); I = _agg(intv_rows)
    out = {}
    for k in ("big", "faith", "mi_mincut", "mi_total", "bigphi_miploss", "bigphi_total"):
        c = I[k].mean() - B[k].mean()
        try:
            d = cohens_d(I[k], B[k])
        except Exception:
            d = float("nan")
        try:
            _, p = welch_t(I[k], B[k])
        except Exception:
            p = float("nan")
        out[k] = dict(contrast=c, d=d, p=p, base=B[k].mean(), intv=I[k].mean())
    return out

# ═══════════════════════════════════════════════════════════════════════════
# PART 1 — re-score the H_1014 SET at a given n; run the SAME separation test.
# ═══════════════════════════════════════════════════════════════════════════
SET = [
    ("planning", gen_planning, "known SPLIT (H_1004/H_1012)"),
    ("imagination", gen_imagination, "known no-split (H_1004)"),
    ("guided", gen_guided, "known no-split (H_1004)"),
    ("chaos", gen_chaos, "NEW intervention (gain=1.4)"),
]

def score_set_at_n(n_units):
    t0 = time.time()
    results = {}
    for name, gen, note in SET:
        print(f"################ [n={n_units}] SCORE intervention = {name}  [{note}] ################", flush=True)
        results[name] = score_intervention_n(name, gen, n_units, t0)
        r = results[name]
        bs = signword(r["big"]["contrast"]); fs = signword(r["faith"]["contrast"])
        split = sgn(r["faith"]["contrast"]) != sgn(r["big"]["contrast"])
        print(f"  --- {name} @ n={n_units}: intervention vs baseline ---")
        print(f"     big-Phi      contrast={r['big']['contrast']:+.4f} d={r['big']['d']:+.3f} p={r['big']['p']:.3e} -> {bs}")
        print(f"     faithful_phi contrast={r['faith']['contrast']:+.4f} d={r['faith']['d']:+.3f} p={r['faith']['p']:.3e} -> {fs}")
        print(f"     SPLIT label (sign(faith)!=sign(big)): {split}")
        print(f"     PREDICTOR mi_mincut(cross-MIP coupling) contrast={r['mi_mincut']['contrast']:+.4f} "
              f"d={r['mi_mincut']['d']:+.3f} p={r['mi_mincut']['p']:.3e} -> {signword(r['mi_mincut']['contrast'])}")
        print(f"       (context) mi_total contrast={r['mi_total']['contrast']:+.4f} | "
              f"bigphi_total contrast={r['bigphi_total']['contrast']:+.4f}")
        print(flush=True)
    return results

def separation_test(results, n_units):
    print(f"--- [n={n_units}] CLASSIFIER MATRIX (split label vs predictor) ---")
    print(f"  {'intervention':12s} | {'big d':>8s} | {'faith d':>8s} | {'SPLIT?':>6s} | "
          f"{'pred mincut Δ':>13s} | {'pred sign':>9s}")
    table = []
    for name, gen, note in SET:
        r = results[name]
        split = sgn(r["faith"]["contrast"]) != sgn(r["big"]["contrast"])
        pred = r["mi_mincut"]["contrast"]; psign = sgn(pred)
        table.append((name, split, pred, psign))
        print(f"  {name:12s} | {r['big']['d']:+8.3f} | {r['faith']['d']:+8.3f} | "
              f"{str(split):>6s} | {pred:+13.4f} | {psign:+9d}")
    split_preds = [pred for (nm, sp, pred, ps) in table if sp]
    nosplit_preds = [pred for (nm, sp, pred, ps) in table if not sp]
    print(f"  split interventions' predictor:   {[f'{p:+.4f}' for p in split_preds]}")
    print(f"  no-split interventions' predictor: {[f'{p:+.4f}' for p in nosplit_preds]}")
    separates = False; boundary = None
    only_planning_split = [nm for (nm, sp, pr, ps) in table if sp] == ["planning"]
    if split_preds and nosplit_preds:
        max_split = max(split_preds); min_nosplit = min(nosplit_preds)
        min_split = min(split_preds); max_nosplit = max(nosplit_preds)
        if max_split < min_nosplit:
            separates = True; boundary = 0.5 * (max_split + min_nosplit)
            kind = "split predictors all BELOW no-split"
        elif min_split > max_nosplit:
            separates = True; boundary = 0.5 * (min_split + max_nosplit)
            kind = "split predictors all ABOVE no-split"
        else:
            kind = "ranges OVERLAP — no separating threshold"
        print(f"  separation: {kind}")
        if boundary is not None:
            print(f"  separating boundary (Δ cross-MIP coupling): {boundary:+.4f}  "
                  f"(H_1014 n=4 boundary was {H1014_BOUNDARY:+.4f})")
    else:
        kind = "degenerate set"
        print(f"  separation: {kind}")
    print(f"  only-planning-is-split: {only_planning_split}")
    print(flush=True)
    return dict(separates=separates, boundary=boundary, only_planning_split=only_planning_split,
                split_preds=split_preds, nosplit_preds=nosplit_preds)

# ═══════════════════════════════════════════════════════════════════════════
# PART 2 — dose-response: sweep planning depth vs greedy(depth-1) at the binding n.
# ═══════════════════════════════════════════════════════════════════════════
SWEEP_DEPTHS = [1, 2, 3, 4, 6, 8]   # depth-1 == greedy baseline

def dose_response(n_units):
    """At each depth d, contrast planning(depth-d) vs greedy(depth-1) on the SAME WM/seed.
    planning_trajectories(seed, depth) returns (H_greedy, H_plan). The greedy arm is the
    SAME across depths (depth-1 == greedy); we score it once. Returns per-depth rows."""
    t0 = time.time()
    # greedy baseline (planning_trajectories returns greedy as the first element regardless of d;
    # use depth=1 call to obtain the matched greedy arm) — score once.
    big_g, faith_g, pred_g = [], [], []
    plan_reads = {d: dict(big=[], faith=[], pred=[]) for d in SWEEP_DEPTHS if d > 1}
    for s in range(N_SEEDS):
        Hg, _ = planning_trajectories(s, 1)
        rg = substrate_reads_n(Hg, n_units)
        big_g.append(rg["big"]); faith_g.append(rg["faith"]); pred_g.append(rg["mi_mincut"])
        for d in SWEEP_DEPTHS:
            if d == 1:
                continue
            _, Hp = planning_trajectories(s, d)
            rp = substrate_reads_n(Hp, n_units)
            plan_reads[d]["big"].append(rp["big"])
            plan_reads[d]["faith"].append(rp["faith"])
            plan_reads[d]["pred"].append(rp["mi_mincut"])
        print(f"    [dose n={n_units} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    big_g = np.array(big_g); faith_g = np.array(faith_g); pred_g = np.array(pred_g)
    rows = []
    for d in SWEEP_DEPTHS:
        if d == 1:
            rows.append(dict(depth=1, dbig=0.0, dfaith=0.0, pred=0.0, split=False, note="greedy baseline"))
            continue
        bp = np.array(plan_reads[d]["big"]); fp = np.array(plan_reads[d]["faith"])
        pp = np.array(plan_reads[d]["pred"])
        dbig = bp.mean() - big_g.mean()
        dfaith = fp.mean() - faith_g.mean()
        dpred = pp.mean() - pred_g.mean()
        split = sgn(dfaith) != sgn(dbig)
        rows.append(dict(depth=d, dbig=dbig, dfaith=dfaith, pred=dpred, split=split, note=""))
    return rows

def analyze_dose(rows):
    print(f"--- DOSE-RESPONSE: planning depth sweep (depth-d vs greedy depth-1) ---")
    print(f"  {'depth':>5s} | {'Δbig-Φ':>9s} | {'Δfaith':>9s} | {'SPLIT?':>6s} | "
          f"{'pred Δcoupling':>14s} | {'> H_1014 bdry?':>14s}")
    onset_depth = None
    cross_depth = None
    depths_gt1 = []
    preds_gt1 = []
    for r in rows:
        crosses = r["pred"] > H1014_BOUNDARY
        print(f"  {r['depth']:>5d} | {r['dbig']:+9.4f} | {r['dfaith']:+9.4f} | "
              f"{str(r['split']):>6s} | {r['pred']:+14.4f} | {str(crosses):>14s}")
        if r["depth"] > 1:
            depths_gt1.append(r["depth"]); preds_gt1.append(r["pred"])
            if r["split"] and onset_depth is None:
                onset_depth = r["depth"]
            if crosses and cross_depth is None:
                cross_depth = r["depth"]
    # monotonicity of the predictor in depth (over the swept depths, incl. greedy=0).
    all_depths = [r["depth"] for r in rows]
    all_preds = [r["pred"] for r in rows]
    rho, prho = spearman(np.array(all_depths, float), np.array(all_preds, float))
    monotone = (rho > 0.0)
    onset_matches_cross = (onset_depth is not None and cross_depth is not None and
                           onset_depth == cross_depth)
    onset_at_or_after_cross = (onset_depth is not None and cross_depth is not None and
                               onset_depth >= cross_depth)
    print(f"  predictor-vs-depth Spearman rho={rho:+.3f} p={prho:.3e}  monotone(rho>0): {monotone}")
    print(f"  split ONSET depth: {onset_depth}   predictor crosses H_1014 boundary at depth: {cross_depth}")
    print(f"  onset == boundary-cross depth: {onset_matches_cross}   "
          f"onset >= boundary-cross depth: {onset_at_or_after_cross}")
    print(flush=True)
    # "monotone dose-response onset" = predictor monotone in depth AND a split onsets AND the
    # onset coincides with / immediately follows the predictor crossing the boundary.
    dose_onset_ok = bool(monotone and (onset_depth is not None) and (cross_depth is not None)
                         and onset_at_or_after_cross)
    return dict(onset_depth=onset_depth, cross_depth=cross_depth, rho=rho, monotone=monotone,
                onset_matches_cross=onset_matches_cross, dose_onset_ok=dose_onset_ok)

# ═══════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 80)
    print("H_1016 — robustness (n=5) + dose-response onset of the H_1014 split predictor")
    print("substrate=CPU-mirror (numpy) — H_1014 module (H_1004 engines + H_1012 proof) VERBATIM")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("predictor = MAGNITUDE of Delta(cross-MIP coupling) vs baseline (H_1014 boundary +1.4933)")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print("PART 1: re-score H_1014 SET at n=5. PART 2: planning depth dose-response onset.")
    print("PASS=GREEN iff n=5 separation HOLDS *and* a monotone dose-response onset exists.")
    print("=" * 80); print()

    # STEP 0 — equivalence proof at n=4 AND n=5 (H_1012 discipline) BEFORE scoring.
    print("EQUIVALENCE PROOF (H_1012 prove_mirrors_at_n — re-prove BOTH mirrors vs stdlib at n=4 AND n=5):")
    ok4 = prove_mirrors_at_n(4); print()
    ok5 = prove_mirrors_at_n(5); print()
    ok = ok4 and ok5
    print(f"  EQUIVALENCE PROOF: n=4 {'PROVEN' if ok4 else 'FAILED'} | n=5 {'PROVEN' if ok5 else 'FAILED'}")
    if not ok:
        raise SystemExit("equivalence proof failed — aborting")
    print()

    # ── PART 1 — robustness in n: re-score the SET at n=5 ──
    print("#" * 80)
    print("PART 1 — ROBUSTNESS IN n: re-score the H_1014 intervention SET at n=5")
    print("#" * 80)
    res5 = score_set_at_n(5)
    sep5 = separation_test(res5, 5)

    # ── PART 2 — dose-response onset (binding n=4; full depth sweep tractable) ──
    print("#" * 80)
    print("PART 2 — DOSE-RESPONSE: planning depth sweep {1,2,3,4,6,8} vs greedy, n=4 (binding rung)")
    print("#" * 80)
    rows4 = dose_response(4)
    dose4 = analyze_dose(rows4)

    # ═══════════════════════════════════════════════════════════════════════
    # VERDICT
    # ═══════════════════════════════════════════════════════════════════════
    n5_separates = bool(sep5["separates"] and sep5["only_planning_split"] == ["planning"])
    dose_ok = bool(dose4["dose_onset_ok"])
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    print(f"  PART 1 (n=5): separating threshold exists = {sep5['separates']}  "
          f"only-planning-is-split = {sep5['only_planning_split']}  => n=5 separation HOLDS: {n5_separates}")
    if sep5["boundary"] is not None:
        print(f"           n=5 separating boundary = {sep5['boundary']:+.4f}  (n=4 was {H1014_BOUNDARY:+.4f})")
    print(f"  PART 2 (dose): monotone predictor(rho={dose4['rho']:+.3f}) = {dose4['monotone']}  "
          f"onset depth = {dose4['onset_depth']}  predictor-cross depth = {dose4['cross_depth']}  "
          f"=> monotone dose-onset: {dose_ok}")
    print()
    if n5_separates and dose_ok:
        token = "ROBUST-AND-DOSE-GRADED"
        print("OVERALL: PASS (GREEN) — ROBUST-AND-DOSE-GRADED. The H_1014 magnitude-threshold")
        print("  predictor SEPARATES split(planning) from the no-split set at n=5 (robust in n,")
        print("  matching the H_1012 split robustness), AND the planning depth sweep shows a")
        print("  MONOTONE dose-response: the predictor Δ(cross-MIP coupling) rises with depth and")
        print("  the faithful-up/big-Φ-down split ONSETS at/after the predictor crosses +1.4933.")
        print("  The magnitude-threshold is a genuine dose-graded, n-robust classifier (PASS).")
    elif n5_separates or dose_ok:
        token = "PARTIAL"
        print("OVERALL: PARTIAL (AMBER) — exactly one of {n=5 separation, monotone dose-onset} holds.")
        print(f"  n=5 separation: {n5_separates} | monotone dose-onset: {dose_ok}. The predictor's")
        print("  robustness is QUALIFIED — it does not clear BOTH pre-registered robustness bars.")
    else:
        token = "NOT-ROBUST"
        print("OVERALL: CLOSED-NEGATIVE (RED) — NOT-ROBUST. Neither the n=5 magnitude separation")
        print("  NOR a monotone dose-response onset holds: the H_1014 n=4/depth-8 predictor")
        print("  separation does NOT generalize. The magnitude-threshold predictor's robustness")
        print("  is RULED OUT (a_paper_negative_ok — a closed-negative is publishable).")
    print(f"  VERDICT-TOKEN: {token}")
    print("=" * 80)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n={4,5}. big-Phi")
    print("super-exponential — n=5 is slow-but-tractable for the SET + the n=4 depth sweep;")
    print("n=6 is the honest cap (skipped, as in H_1012). Both CPU mirrors RE-PROVEN == stdlib")
    print("at n=4 AND n=5 (H_1012 prove_mirrors_at_n) BEFORE scoring; the predictor is a")
    print("deterministic pure function of the SAME bits. Scale-transfer beyond n=5 UNVERIFIED.")
    print("g5 CODE-measured (no LLM self-judge, p7), a_phi_iit4_tool. NOT a forge binary; $0 CPU.")

if __name__ == "__main__":
    main()
