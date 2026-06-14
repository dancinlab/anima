"""
H_1233 — DOMINANCE-FREE TARGET axis-combination climb (the open frontier)
H_1232 collapsed to singleton {G-LZ} because the target (complex-vs-simple) was
near-definitional for LZ. This probe uses a DOMINANCE-FREE target: the FULL 4-way
Wolfram class {I,II,III,IV}. LZ separates {I,II} from {III,IV} but NOT I-from-II
(both simple) nor III-from-IV (both complex) — so distinguishing all four REQUIRES
multiple research axes. If a genuine RICH multi-axis FINAL COMBINATION exists anywhere,
it must appear here. Framework MATRIX.md §0. $0 LOCAL numpy.

SHARED SUBSTRATE + AXES: identical to H_1232 (ECA panel; B-PHI·E-SI·F-SYNC·G-LZ·density·col-ent).
TARGET = 4-way class label. METRIC = macro one-vs-rest AUROC (mean over the 4 classes).
METHOD = greedy forward climb by held-out macro-AUROC.

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 RICH-COMBINATION — climb saturates at k* >= 3 (a genuinely multi-axis final
                        combination is needed) AND macro-AUROC >= 0.75.
  H_1233 SUPPORTED iff F1 — the dominance-free target reveals a RICH (k*>=3) final
  combination (the matrix is NOT low-rank for a non-definitional target).
  CLOSED-NEGATIVE (a_paper_negative_ok) iff k* <= 2 — even a 4-way target collapses to
  <=2 axes ⇒ these axis systems are intrinsically LOW-RANK (the climb's terminal finding).

scope: small ECA, proxy-Φ pre-screen (a_phi_iit4_tool · a_scale_honest_scope). seed-fixed.
"""
import os, math, json
import numpy as np
import importlib.util

# reuse H_1232 substrate + axis functions
_spec = importlib.util.spec_from_file_location("h1232", os.path.join(os.path.dirname(__file__), "h1232_research_axis_climb.py"))
h1232 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(h1232)

SEED = 7
np.random.seed(SEED)
CLASS = h1232.CLASS; AXES = h1232.AXES
CIDX = {"I":0, "II":1, "III":2, "IV":3}
EPS = 0.01
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1233_dominancefree_axis_climb")


def macro_auroc(feats_sel_tr, ytr_multi, feats_sel_te, yte_multi):
    # mean one-vs-rest held-out AUROC over the 4 classes
    aus = []
    for c in range(4):
        ytr = (ytr_multi == c).astype(float); yte = (yte_multi == c).astype(float)
        if ytr.sum() < 2 or (1-ytr).sum() < 2 or yte.sum() < 1 or (1-yte).sum() < 1:
            continue
        aus.append(h1232.logreg_auroc(feats_sel_tr, ytr, feats_sel_te, yte))
    return float(np.mean(aus)) if aus else float("nan")


def main():
    print("=== H_1233 dominance-free (4-way class) axis climb ===", flush=True)
    rows = []
    for rule in CLASS:
        for d in h1232.DENS:
            for sd in h1232.SEEDS:
                sp = h1232.eca_run(rule, h1232.W, h1232.T, d, sd)
                feats = {"B-PHI":h1232.phi_proxy(sp),"E-SI":h1232.savant_index(sp),
                         "F-SYNC":h1232.sync_param(sp),"G-LZ":h1232.lz76_simple(sp.flatten()),
                         "density":float(sp.mean()),"col-ent":h1232.col_entropy(sp)}
                rows.append((CIDX[CLASS[rule]], feats))
    rng = np.random.RandomState(SEED); order = rng.permutation(len(rows)); rows = [rows[i] for i in order]
    ym = np.array([r[0] for r in rows])
    feats = {a: np.array([r[1][a] for r in rows]) for a in AXES}
    half = len(ym)//2; ytr, yte = ym[:half], ym[half:]
    counts = {k:int((ym==v).sum()) for k,v in CIDX.items()}
    print(f"[data] {len(rows)} runs · class counts {counts}", flush=True)
    def Xof(sel, sl): return np.stack([feats[a][sl] for a in sel], axis=1)

    chosen, ladder, rem, prev = [], [], list(AXES), 0.5
    while rem:
        ba, bau = None, -1
        for a in rem:
            au = macro_auroc(Xof(chosen+[a], slice(0,half)), ytr, Xof(chosen+[a], slice(half,None)), yte)
            if not math.isnan(au) and au > bau: bau, ba = au, a
        if ba is None: break
        ladder.append({"k":len(chosen)+1,"added":ba,"macro_auroc":bau,"gain":bau-prev})
        print(f"  k={len(chosen)+1} +{ba:9s} macroAUROC={bau:.4f} gain={bau-prev:+.4f}", flush=True)
        chosen.append(ba); rem.remove(ba); prev = bau
    kstar = len(AXES); final = list(chosen); sat = ladder[-1]["macro_auroc"]
    for i in range(1, len(ladder)):
        if ladder[i]["gain"] < EPS: kstar=i; final=[ladder[j]["added"] for j in range(i)]; sat=ladder[i-1]["macro_auroc"]; break

    f1 = (kstar >= 3) and (sat >= 0.75)
    supported = bool(f1)
    if supported:
        ruling = f"SUPPORTED: dominance-free 4-way target reveals a RICH multi-axis FINAL COMBINATION — k*={kstar} {final} (macro-AUROC {sat:.3f}); the axis matrix is NOT low-rank for a non-definitional target"
    else:
        ruling = f"CLOSED-NEGATIVE: even the 4-way dominance-free target collapses to k*={kstar} {final} (macro-AUROC {sat:.3f}) — these axis systems are intrinsically LOW-RANK; the combination fixed point is small at every target. Climb DEPLETED."

    verdict = {
        "H":"H_1233","title":"dominance-free 4-way class axis climb","axes":AXES,
        "class_counts":counts,"ladder":ladder,"k_star":kstar,"final_combination":final,
        "saturation_macro_auroc":sat,
        "F1_rich_combination":{"k_star":kstar,"sat":sat,"bars":"k*>=3 AND macroAUROC>=0.75","pass":bool(f1)},
        "supported":supported,"ruling":ruling,
        "framework":"MATRIX.md §0 — dominance-free target (open frontier)",
        "caveat":"variance-partition Φ-proxy pre-screen (a_phi_iit4_tool); small ECA (a_scale_honest_scope)","seed":SEED,
    }
    print("=== VERDICT ===", flush=True); print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(verdict, open(os.path.join(OUTDIR,"result.json"),"w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
