"""H_1044 — Does the REDUNDANCY-MARGIN predictor (H_1020 GREEN @ n=5) survive at n=6 EXACT?

Combines the H_1037 n=6 EXACT rung with the H_1020 PID redundancy-margin predictor.
Substrate + PID + engines IMPORTED VERBATIM from the h1014->h1020 chain; the ONLY thing
that changes is n_units = 6 (was 5). a_phi_iit4_tool: big-Phi/faithful CPU mirrors RE-PROVEN
== stdlib at n=4,5 BEFORE scoring; the PID (Williams-Beer I_min) is the EXPLANATORY variable
(exact, n-agnostic), NOT a Phi proxy. Frozen bar: state/h104x_phi/H_1044_FREEZE.txt.

Run:  python3 -u h1044_redundancy_margin_n6.py [--n 6] [--pid-only]
  --pid-only : skip the (potentially super-exp) n=6 big-Phi split-LABEL column; the redundancy-
               margin PREDICTOR verdict is unaffected (it is a pure PID function of the bits).
"""
import sys, os, time, json, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.abspath(os.path.join(HERE, "..", "..", "archive", "state", "universe-probes"))
CWM = os.path.abspath(os.path.join(HERE, "..", "..", "archive", "CWM", "probes"))
for p in (CWM, PROBES):
    if p not in sys.path:
        sys.path.insert(0, p)

import importlib.util as _ilu
from cwm_probe_lib import cohens_d


def _load(modname, fname):
    path = os.path.join(PROBES, fname)
    spec = _ilu.spec_from_file_location(modname, path)
    mod = _ilu.module_from_spec(spec)
    src = open(path).read().replace('if __name__ == "__main__":\n    main()', "")
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod


_h1017 = _load("h1017", "h1017_split_redundancy_mechanism.py")
_h1016 = _load("h1016", "h1016_split_predictor_robustness.py")

pid_system = _h1017.pid_system
_pid_two_source = _h1017._pid_two_source
substrate_reads_n = _h1016.substrate_reads_n
latent_to_binary_seq = _h1016.latent_to_binary_seq
prove_mirrors_at_n = _h1016.prove_mirrors_at_n
gen_planning = _h1016.gen_planning
gen_imagination = _h1016.gen_imagination
gen_guided = _h1016.gen_guided
gen_chaos = _h1016.gen_chaos
sgn = _h1016.sgn
N_SEEDS = _h1016.N_SEEDS
LATENT = _h1017.LATENT

H1014_BOUNDARY = 1.4933  # H_1014 n=4 coupling-magnitude separating boundary (frozen)
PRESET_GAP = 1.0         # H_1044 frozen redundancy-margin separation gap

SET = [
    ("planning", gen_planning, "known SPLIT / TRUE split-inducer"),
    ("imagination", gen_imagination, "no-split control"),
    ("guided", gen_guided, "no-split control"),
    ("chaos", gen_chaos, "no-split control"),
]


def _faithful_mi_only(H, n_units):
    """Cheap EXACT faithful_phi + MI-coupling path (NO super-exp big_phi)."""
    bits, n = latent_to_binary_seq(H, n_units)
    fstate, fn, fdim = _h1016.binary_seq_to_faithful_state(bits, n)
    mi = _h1016.build_mi_matrix(fstate, fn, fdim, 2)
    fphi = _h1016.faithful_phi_from_mi(mi, fn)
    mi_total = float(np.triu(mi, 1).sum())
    mi_mincut = _h1016._mi_min_cut_weight(mi, fn)
    return fphi, mi_total, mi_mincut


def reads_n_with_pid(H, n_units, mode="full"):
    """mode: 'pid' (PID only) | 'nobig' (PID+faithful+MI, no big_phi) | 'full' (+big_phi)."""
    bits, n = latent_to_binary_seq(H, n_units)
    p = pid_system(bits)
    out = dict(red_total=p["red_total"], syn_total=p["syn_total"])
    if mode == "pid":
        return out
    if mode == "nobig":
        f, mt, mc = _faithful_mi_only(H, n_units)
        out.update(faith=f, mi_total=mt, mi_mincut=mc)
        return out
    base = substrate_reads_n(H, n_units)
    out.update(big=base["big"], faith=base["faith"],
               mi_total=base["mi_total"], mi_mincut=base["mi_mincut"])
    return out


def _contrast(I, B, k):
    c = I[k].mean() - B[k].mean()
    try:
        d = cohens_d(I[k], B[k])
    except Exception:
        d = float("nan")
    return dict(contrast=c, d=d, base=B[k].mean(), intv=I[k].mean())


def score(name, gen, n_units, keys, t0, mode):
    base_rows, intv_rows = [], []
    for s in range(N_SEEDS):
        Hb, Hi = gen(s)
        base_rows.append(reads_n_with_pid(Hb, n_units, mode))
        intv_rows.append(reads_n_with_pid(Hi, n_units, mode))
        print(f"    [{name} n={n_units} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    B = {k: np.array([r[k] for r in base_rows]) for k in base_rows[0]}
    I = {k: np.array([r[k] for r in intv_rows]) for k in intv_rows[0]}
    return {k: _contrast(I, B, k) for k in keys if k in B}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--mode", choices=["pid", "nobig", "full"], default="nobig",
                    help="pid=PID only | nobig=PID+faithful+MI (no super-exp big_phi) | full=+big_phi split-label")
    ap.add_argument("--pid-only", action="store_true", help="alias for --mode pid")
    ap.add_argument("--out", default=os.path.join(HERE, "h1044_redundancy_margin_n6_result.json"))
    args = ap.parse_args()
    mode = "pid" if args.pid_only else args.mode
    pid_only = mode == "pid"
    n = args.n

    print("=" * 92)
    print(f"H_1044 — REDUNDANCY-MARGIN predictor at n={n} EXACT (H_1020 robustness ladder; follow-up of n=5)")
    print("substrate=CPU-mirror (numpy) — h1014->h1016 VERBATIM; PID = Williams-Beer I_min (H_1017 verbatim)")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa | faithful_phi: .../iit4/faithful_phi.hexa")
    print("a_phi_iit4_tool: mirrors RE-PROVEN == stdlib at n=4,5 BEFORE scoring. PID != Phi proxy (explanatory).")
    print(f"FROZEN BAR: PASS = planning red-dominated AND planning margin > max(control margin) + GAP({PRESET_GAP}).")
    print(f"pid_only={pid_only}  N_SEEDS={N_SEEDS}")
    print("=" * 92, flush=True)

    print("\nSTEP 0 — RE-PROVE CPU mirror == stdlib at n=4 AND n=5 (a_phi_iit4_tool):")
    proven = {}
    for k in (4, 5):
        proven[k] = bool(prove_mirrors_at_n(k))
    print(f"  mirror-equivalence: {proven}")
    if not all(proven.values()):
        raise SystemExit("mirror proof FAILED — abort")

    rng = np.random.default_rng(20260710)
    H = rng.standard_normal((40, LATENT))
    b1, _ = latent_to_binary_seq(H, n)
    p1 = pid_system(b1); p2 = pid_system(b1)
    pid_det = abs(p1["red_total"] - p2["red_total"]) < 1e-12
    Tc = np.array([0, 1, 0, 1, 1, 0, 1, 0]); rc, _, _, sc_ = _pid_two_source(Tc, Tc, Tc)
    Xa = np.array([0, 0, 1, 1, 0, 0, 1, 1]); Xb = np.array([0, 1, 0, 1, 0, 1, 0, 1]); Xt = Xa ^ Xb
    rx, _, _, sx = _pid_two_source(Xt, Xa, Xb)
    copy_ok = rc > 0.5 and abs(sc_) < 1e-6
    xor_ok = rx < 1e-6 and sx > 0.5
    print(f"  PID det@n={n}: {pid_det} | WB COPY red={rc:.3f} syn={sc_:.3f} ({copy_ok}) | "
          f"XOR red={rx:.3f} syn={sx:.3f} ({xor_ok})")
    if not (pid_det and copy_ok and xor_ok):
        raise SystemExit("PID validity FAILED — abort")

    if mode == "pid":
        keys = ["red_total", "syn_total"]
    elif mode == "nobig":
        keys = ["red_total", "syn_total", "faith", "mi_total", "mi_mincut"]
    else:
        keys = ["red_total", "syn_total", "big", "faith", "mi_total", "mi_mincut"]
    t0 = time.time()
    results = {}
    for name, gen, note in SET:
        print(f"\n######## SCORE n={n} intervention={name} [{note}] mode={mode} ########", flush=True)
        results[name] = score(name, gen, n, keys, t0, mode)

    print("\n" + "=" * 92)
    print(f"REDUNDANCY-MARGIN MATRIX @ n={n} EXACT")
    print("=" * 92)
    rows = {}
    for name, gen, note in SET:
        r = results[name]
        dred = r["red_total"]["contrast"]; dsyn = r["syn_total"]["contrast"]
        margin = dred - dsyn
        reddom = dred > dsyn and dred > 0.0
        split = None
        if "big" in r and "faith" in r:
            split = sgn(r["faith"]["contrast"]) != sgn(r["big"]["contrast"])
        rows[name] = dict(dred=dred, dsyn=dsyn, margin=margin, reddom=reddom, split=split)
        print(f"  {name:12s} | dred={dred:+8.4f} | dsyn={dsyn:+8.4f} | margin={margin:+9.4f} | "
              f"reddom={str(reddom):>5s} | split={split}")

    pl = rows["planning"]
    controls = {k: v for k, v in rows.items() if k != "planning"}
    max_ctrl = max(v["margin"] for v in controls.values())
    plan_reddom = pl["reddom"]
    gap_ok = pl["margin"] > max_ctrl + PRESET_GAP
    separates = plan_reddom and gap_ok
    print(f"\nplanning margin={pl['margin']:+.4f} reddom={plan_reddom} | max(control margin)={max_ctrl:+.4f} "
          f"| GAP={PRESET_GAP} | planning > max+gap: {gap_ok}")
    for k, v in controls.items():
        print(f"  control {k:12s}: margin={v['margin']:+.4f}  planning exceeds by {pl['margin']-v['margin']:+.4f} "
              f"(>= gap {PRESET_GAP}: {pl['margin']-v['margin'] >= PRESET_GAP})")

    coupling_note = "SKIPPED (pid mode)"
    if mode != "pid":
        print(f"\nCOUPLING-MAGNITUDE cross-check @ n={n} (H_1014 d(mi_total-mi_mincut) vs boundary {H1014_BOUNDARY}):")
        coup = {}
        for name, gen, note in SET:
            r = results[name]
            dcoup = r["mi_total"]["contrast"] - r["mi_mincut"]["contrast"]
            coup[name] = dcoup
            print(f"  {name:12s}: dcoupling={dcoup:+.4f}  above-boundary({H1014_BOUNDARY}): {dcoup > H1014_BOUNDARY}")
        plan_above = coup["planning"] > H1014_BOUNDARY
        ctrl_above = [k for k in controls if coup[k] > H1014_BOUNDARY]
        coupling_clean = plan_above and not ctrl_above
        coupling_note = (f"planning above={plan_above}, controls above={ctrl_above} -> "
                         f"coupling {'SEPARATES (alive)' if coupling_clean else 'STAYS DEAD (no clean planning-only separation)'}")
        print(f"  => {coupling_note}")

    print("\n" + "=" * 92)
    if separates:
        verdict = "MECHANISM-PREDICTOR-ROBUST-N6"
        print(f"OVERALL: PASS — {verdict}. At n={n} EXACT the redundancy-margin predictor STILL separates")
        print("  planning from ALL controls by the frozen gap: planning is redundancy-dominated AND its")
        print("  margin exceeds every control's by >= GAP. H_1020 (n=5) strengthened to a >=3-rung ladder.")
    else:
        verdict = "MECHANISM-PREDICTOR-N5-BOUND"
        print(f"OVERALL: FAIL (closed-negative) — {verdict}. At n={n} EXACT the redundancy-margin no longer")
        print("  separates planning from ALL controls by the frozen gap. Like the coupling magnitude at")
        print("  n<=4, redundancy bounds to n<=5 (a_paper_negative_ok).")
    print(f"  VERDICT-TOKEN: {verdict}")
    print("=" * 92)
    print(f"HONEST SCOPE: n={n} EXACT rung; n=7 infeasible-cap. PID exact+deterministic (n-agnostic).")
    print(f"  mirror==stdlib re-proven n=4,5. TOY n-ladder; production-scale UNVERIFIED. pid_only={pid_only}.")

    out = dict(n=int(n), pid_only=bool(pid_only), mirror_proven=proven,
               preset_gap=PRESET_GAP, planning_margin=float(pl["margin"]),
               max_control_margin=float(max_ctrl), planning_reddom=bool(plan_reddom),
               gap_ok=bool(gap_ok), separates=bool(separates), verdict_token=verdict,
               coupling_note=coupling_note,
               rows={k: {kk: (float(vv) if isinstance(vv, (int, float, np.floating)) else vv)
                         for kk, vv in v.items()} for k, v in rows.items()},
               total_wall_sec=time.time() - t0)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nRESULT JSON -> {args.out}")


if __name__ == "__main__":
    main()
