"""H_1020 — does the REDUNDANCY-MARGIN mechanism predictor beat the H_1014 MAGNITUDE
predictor in robustness to n? Does redundancy-dominance still separate the split
intervention (planning) from the no-split controls at n=5, where the cruder
magnitude predictor was shown to be an n=4 artifact (H_1016)?

MISSION
-------
H_1014 (terminal, QUALIFIED): at n=4 a MAGNITUDE threshold on Δ(cross-MIP coupling)
separated the split-inducing planning intervention from the three no-split ones.
H_1016 (PARTIAL): that magnitude separation is an n=4 ARTIFACT — it does NOT survive
to n=5 (the weak no-split interventions imagination & guided pick up SPURIOUS split
labels from non-significant big-Φ sign-flips, so "only-planning-is-split" breaks and
the predictor ranges OVERLAP). The PLANNING split ITSELF survives n=5 (d_big −2.28 /
d_faith +4.65). H_1017 (🟢): the MECHANISM — planning's MI rise is REDUNDANCY-dominated
(Δredundancy ≫ Δsynergy), measured by a Williams-Beer I_min PID at n=4, and planning's
redundancy-margin (Δred−Δsyn = +10.44) DWARFS every no-split control (≤+2.95).

HYPOTHESIS (the WHY behind the WHY — predictor-class comparison)
---------------------------------------------------------------
The H_1014 coupling-MAGNITUDE predictor broke at n=5 (H_1016). Test whether the H_1017
REDUNDANCY-MARGIN predictor (Δred−Δsyn / redundancy-dominance) is MORE robust: does
redundancy-margin STILL separate planning (the true split-inducer) from ALL no-split
controls {imagination, guided, chaos} at n=5, where the cruder magnitude predictor failed?

METHOD — REUSE H_1017 PID + H_1016 n=5 path VERBATIM
---------------------------------------------------
- The Williams-Beer I_min PID estimator (pid_system / _pid_two_source / _specific_info /
  _mi_discrete) is IMPORTED from h1017 VERBATIM — it is already n-agnostic (loops over n
  units), so it applies unchanged at n=5.
- The n-parametric substrate read substrate_reads_n is IMPORTED from h1016 VERBATIM (the
  ONE matched n-binary discretization → big_phi + faithful_phi via the H_1004 engines),
  and EXTENDED here with the H_1017 PID red_total/syn_total on the SAME bits.
- The SPLIT label is computed exactly as H_1016 (sign(Δfaith) != sign(Δbig)); we reuse
  H_1016's n=5 split labels (planning True; imagination True[spurious]; guided
  True[spurious]; chaos False) and report whether redundancy-margin separation tracks
  the TRUE planning-only split or the spurious-sign-flip labels.
- H_1012 prove_mirrors_at_n(5) is run BEFORE scoring (mirror ≡ stdlib at n=5; H_1012/
  H_1016 discipline). The PID is independently re-validated on the canonical COPY (pure
  redundancy) and XOR (pure synergy) cases BEFORE scoring (H_1017 discipline).

The PID redundancy/synergy is an INFORMATION-DECOMPOSITION of the same bits — the
EXPLANATORY variable, NOT a Φ proxy. Any Φ/big-Φ number reuses the stdlib mirrors
(iit4/faithful_phi.hexa + iit4_bigphi.hexa) re-proven ≡ stdlib at n=5 (a_phi_iit4_tool).

PRE-REGISTERED FALSIFIER (frozen 2026-06-07)
--------------------------------------------
Score the SET {planning, imagination, guided, chaos}, 30 seeds, matched n=5 binary
discretization, both stdlib engines (mirror RE-PROVEN ≡ stdlib at n=5 BEFORE scoring),
python3 -u, serial, $0 CPU. NO emoji token before
.verdicts/1020_redundancy_predictor_robustness/H_1020.txt exists.

- PASS = MECHANISM-PREDICTOR-ROBUST IF redundancy-margin (Δred−Δsyn) cleanly SEPARATES
  planning (the true split-inducer) from ALL no-split controls {imagination, guided,
  chaos} at n=5 — operationally planning is redundancy-dominated (Δred>Δsyn & Δred>0)
  AND planning's redundancy-margin EXCEEDS every other intervention's redundancy-margin
  at n=5. THEN the mechanism (redundancy) predictor is MORE robust than the magnitude
  predictor (which failed at n=5, H_1016): a Δ-vs-H_1016 result.
- FAIL / CLOSED-NEGATIVE = MECHANISM-PREDICTOR-N4-BOUND IF redundancy-margin ALSO fails
  to separate at n=5 (planning's margin does NOT exceed every control's, OR planning is
  not redundancy-dominated). THEN the redundancy explanation, like the coupling
  magnitude, is an n=4 property; it bounds the mechanism to n=4 (a_paper_negative_ok).

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=5 — both engines exact;
big-Φ super-exponential so n=5 is slow-but-tractable and n=6 is the honest cap (skipped,
as in H_1012/H_1016). The PID is exact + deterministic on the SAME bits. Scale-transfer
beyond n=5 UNVERIFIED. NOT a forge binary; $0 CPU-local, no GPU.
"""
import sys, os, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))
from cwm_probe_lib import cohens_d, welch_t  # noqa: E402

# ── Import H_1017 (PID estimator) and H_1016 (n-parametric substrate) VERBATIM. ──
import importlib.util as _ilu


def _load(modname, fname):
    path = os.path.join(HERE, fname)
    spec = _ilu.spec_from_file_location(modname, path)
    mod = _ilu.module_from_spec(spec)
    src = open(path).read().replace('if __name__ == "__main__":\n    main()', "")
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod


_h1017 = _load("h1017", "h1017_split_redundancy_mechanism.py")
_h1016 = _load("h1016", "h1016_split_predictor_robustness.py")

# PID estimator — IMPORTED VERBATIM from H_1017 (already n-agnostic).
pid_system = _h1017.pid_system
_pid_two_source = _h1017._pid_two_source

# n-parametric substrate read — IMPORTED VERBATIM from H_1016 (H_1014 engines + H_1012 proof).
substrate_reads_n = _h1016.substrate_reads_n   # dict(big, faith, mi_total, mi_mincut, ...)
latent_to_binary_seq = _h1016.latent_to_binary_seq
prove_mirrors_at_n = _h1016.prove_mirrors_at_n
gen_planning = _h1016.gen_planning
gen_imagination = _h1016.gen_imagination
gen_guided = _h1016.gen_guided
gen_chaos = _h1016.gen_chaos
sgn = _h1016.sgn
N_SEEDS = _h1016.N_SEEDS
LATENT = _h1017.LATENT

# ═══════════════════════════════════════════════════════════════════════════
# substrate read at n_units: H_1016 substrate_reads_n (split label engines) EXTENDED
# with the H_1017 PID red_total/syn_total on the SAME bits. No engine logic reinvented.
# ═══════════════════════════════════════════════════════════════════════════
def reads_n_with_pid(H, n_units):
    base = substrate_reads_n(H, n_units)          # H_1016 verbatim: big, faith, mi_total, ...
    bits, n = latent_to_binary_seq(H, n_units)    # SAME matched n-binary bits
    p = pid_system(bits)                          # H_1017 PID verbatim, on the SAME bits
    base = dict(base)
    base["red_total"] = p["red_total"]
    base["syn_total"] = p["syn_total"]
    base["syn_raw"] = p["syn_total_raw"]
    return base


def _agg(rows):
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}


def _contrast(I, B, k):
    c = I[k].mean() - B[k].mean()
    try:
        d = cohens_d(I[k], B[k])
    except Exception:
        d = float("nan")
    try:
        _, p = welch_t(I[k], B[k])
    except Exception:
        p = float("nan")
    return dict(contrast=c, d=d, p=p, base=B[k].mean(), intv=I[k].mean())


def score(name, gen, n_units, t0):
    base_rows, intv_rows = [], []
    for s in range(N_SEEDS):
        Hb, Hi = gen(s)
        base_rows.append(reads_n_with_pid(Hb, n_units))
        intv_rows.append(reads_n_with_pid(Hi, n_units))
        print(f"    [{name} n={n_units} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    B = _agg(base_rows); I = _agg(intv_rows)
    return {k: _contrast(I, B, k) for k in
            ("big", "faith", "mi_total", "red_total", "syn_total")}


SET = [
    ("planning", gen_planning, "known SPLIT (H_1004/H_1012), TRUE split-inducer"),
    ("imagination", gen_imagination, "no-split @ n=4; SPURIOUS split label @ n=5 (H_1016)"),
    ("guided", gen_guided, "no-split @ n=4; SPURIOUS split label @ n=5 (H_1016)"),
    ("chaos", gen_chaos, "no-split (H_1016 n=5 SPLIT=False)"),
]


def main():
    print("=" * 80)
    print("H_1020 — REDUNDANCY-MARGIN mechanism predictor vs the MAGNITUDE predictor: robustness in n")
    print("substrate=CPU-mirror (numpy) — H_1016 substrate_reads_n (H_1014 engines + H_1012 proof) VERBATIM")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("PID = Williams-Beer (2010) I_min redundancy lattice — IMPORTED VERBATIM from H_1017")
    print("  (the EXPLANATORY variable — NOT a Phi proxy/replacement; Phi from stdlib mirrors only)")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print("SET: planning[TRUE split] + imagination[spurious n=5 split] + guided[spurious] + chaos[no-split]")
    print("PASS = redundancy-margin (Δred−Δsyn) SEPARATES planning from ALL no-split controls AT n=5")
    print("       (planning red-dominated AND planning margin > every other intervention's), where the")
    print("       H_1014 MAGNITUDE predictor FAILED at n=5 (H_1016). FAIL = redundancy is also n=4-bound.")
    print("=" * 80)
    print()

    # STEP 0 — equivalence proof at n=5 (H_1012/H_1016 discipline) BEFORE scoring.
    print("EQUIVALENCE PROOF at n=5 (H_1012 prove_mirrors_at_n — re-prove BOTH mirrors vs stdlib):")
    ok5 = prove_mirrors_at_n(5)
    print()

    # PID re-validation (H_1017 discipline): determinism + canonical COPY/XOR cases.
    rng = np.random.default_rng(20260607)
    H = rng.standard_normal((40, LATENT))
    r1 = reads_n_with_pid(H, 5); r2 = reads_n_with_pid(H, 5)
    pid_det = (abs(r1["red_total"] - r2["red_total"]) < 1e-12 and
               abs(r1["syn_total"] - r2["syn_total"]) < 1e-12)
    pid_nonneg = (r1["red_total"] >= -1e-9 and r1["syn_total"] >= -1e-9)
    print(f"  PID deterministic re-run @ n=5: {pid_det}   red_total={r1['red_total']:.6f} "
          f"syn_total={r1['syn_total']:.6f} (raw_syn={r1['syn_raw']:+.6f}) nonneg={pid_nonneg}")
    Tc = np.array([0, 1, 0, 1, 1, 0, 1, 0]); rc, _, _, sc_ = _pid_two_source(Tc, Tc, Tc)
    Xa = np.array([0, 0, 1, 1, 0, 0, 1, 1]); Xb = np.array([0, 1, 0, 1, 0, 1, 0, 1]); Xt = Xa ^ Xb
    rx, _, _, sx = _pid_two_source(Xt, Xa, Xb)
    print(f"  WB sanity: COPY(T;T,T) red={rc:.4f} syn={sc_:.4f} (expect red>0,syn~0) | "
          f"XOR(T;A,B) red={rx:.4f} syn={sx:.4f} (expect red~0,syn>0)")
    copy_ok = (rc > 0.5 and abs(sc_) < 1e-6)
    xor_ok = (rx < 1e-6 and sx > 0.5)
    print(f"  WB canonical-case check: COPY={copy_ok} XOR={xor_ok}")
    ok = ok5 and pid_det and pid_nonneg and copy_ok and xor_ok
    print(f"  EQUIVALENCE + PID-VALIDITY PROOF n=5: {'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
    if not ok:
        raise SystemExit("equivalence/PID proof failed — aborting")
    print()

    # ── SCORE the SET at n=5 ──
    t0 = time.time()
    results = {}
    for name, gen, note in SET:
        print(f"################ [n=5] SCORE intervention = {name}  [{note}] ################", flush=True)
        r = score(name, gen, 5, t0)
        results[name] = r
        split = sgn(r["faith"]["contrast"]) != sgn(r["big"]["contrast"])
        dred = r["red_total"]["contrast"]; dsyn = r["syn_total"]["contrast"]
        print(f"  --- {name} @ n=5: intervention vs baseline (matched n=5 binary discretization) ---")
        print(f"     big-Phi      contrast={r['big']['contrast']:+.4f} d={r['big']['d']:+.3f} p={r['big']['p']:.3e}")
        print(f"     faithful_phi contrast={r['faith']['contrast']:+.4f} d={r['faith']['d']:+.3f} p={r['faith']['p']:.3e}")
        print(f"     SPLIT label (sign(faith)!=sign(big)): {split}")
        print(f"     Δredundancy  contrast={dred:+.4f} d={r['red_total']['d']:+.3f} p={r['red_total']['p']:.3e}")
        print(f"     Δsynergy     contrast={dsyn:+.4f} d={r['syn_total']['d']:+.3f} p={r['syn_total']['p']:.3e}")
        print(f"     redundancy-margin (Δred−Δsyn)={dred - dsyn:+.4f}  "
              f"redundancy-dominated (Δred>Δsyn & Δred>0): {dred > dsyn and dred > 0.0}")
        print(f"     (cross-check) Δmi_total={r['mi_total']['contrast']:+.4f}", flush=True)
        print()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER — redundancy-margin separation at n=5
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("REDUNDANCY-MARGIN MATRIX @ n=5 — Δred, Δsyn, margin, split label, predictor verdict")
    print("=" * 80)
    print(f"  {'intervention':12s} | {'SPLIT?':>6s} | {'Δredund':>9s} | {'Δsynergy':>9s} | "
          f"{'red-margin':>10s} | {'red-dom':>7s}")
    rows = {}
    for name, gen, note in SET:
        r = results[name]
        split = sgn(r["faith"]["contrast"]) != sgn(r["big"]["contrast"])
        dred = r["red_total"]["contrast"]; dsyn = r["syn_total"]["contrast"]
        margin = dred - dsyn
        reddom = (dred > dsyn and dred > 0.0)
        rows[name] = dict(split=split, dred=dred, dsyn=dsyn, margin=margin, reddom=reddom)
        print(f"  {name:12s} | {str(split):>6s} | {dred:+9.4f} | {dsyn:+9.4f} | "
              f"{margin:+10.4f} | {str(reddom):>7s}")
    print()

    pl = rows["planning"]
    controls = {k: v for k, v in rows.items() if k != "planning"}
    plan_reddom = pl["reddom"]
    plan_margin = pl["margin"]
    print(f"Planning @ n=5: Δred={pl['dred']:+.4f} Δsyn={pl['dsyn']:+.4f} "
          f"redundancy-dominated: {plan_reddom}  margin(Δred−Δsyn)={plan_margin:+.4f}")
    print("Controls (redundancy-margin Δred−Δsyn) — ALL controls, not just no-split-labelled:")
    separates = plan_reddom
    for k, v in controls.items():
        exceeds = plan_margin > v["margin"]
        tag = "split=True[spurious per H_1016]" if v["split"] else "split=False"
        print(f"  {k:12s}: margin={v['margin']:+.4f} reddom={v['reddom']}  ({tag})  "
              f"planning margin {plan_margin:+.4f} > this: {exceeds}")
        if not exceeds:
            separates = False

    # Track the TRUE planning-only split vs the spurious-sign-flip labels:
    nosplit_labelled = [k for k, v in rows.items() if not v["split"]]   # chaos at n=5
    spurious_split = [k for k, v in controls.items() if v["split"]]     # imagination, guided at n=5
    print()
    print(f"  H_1016 n=5 split labels: planning={rows['planning']['split']} "
          f"imagination={rows['imagination']['split']} guided={rows['guided']['split']} "
          f"chaos={rows['chaos']['split']}")
    print(f"  no-split-LABELLED at n=5: {nosplit_labelled}  (the magnitude predictor's clean class shrank)")
    print(f"  SPURIOUS-split controls (sign-flip artifact, H_1016): {spurious_split}")
    # Does redundancy-margin track the TRUE planning-only split (separates planning from ALL
    # controls) rather than the spurious split labels?
    tracks_true_split = separates
    print(f"  redundancy-margin separates planning from ALL controls (incl. spurious-labelled): {separates}")
    print(f"   => tracks the TRUE planning-only split (NOT the spurious-sign-flip labels): {tracks_true_split}")

    print()
    print("=" * 80)
    if separates:
        token = "MECHANISM-PREDICTOR-ROBUST"
        print("OVERALL: PASS (GREEN) — MECHANISM-PREDICTOR-ROBUST. The H_1017 REDUNDANCY-MARGIN")
        print("  predictor cleanly SEPARATES planning (the true split-inducer) from ALL no-split")
        print("  controls {imagination, guided, chaos} at n=5: planning is redundancy-dominated AND")
        print("  planning's redundancy-margin EXCEEDS every control's. Crucially it separates planning")
        print("  even from imagination & guided — which the cruder MAGNITUDE predictor mislabelled as")
        print("  'split' at n=5 via non-significant big-Φ sign-flips (H_1016). The MECHANISM predictor")
        print("  tracks the TRUE planning-only split where the magnitude predictor became an n=4")
        print("  artifact: redundancy-margin is MORE robust in n (Δ-vs-H_1016).")
        print("  VERDICT-TOKEN: MECHANISM-PREDICTOR-ROBUST")
    else:
        token = "MECHANISM-PREDICTOR-N4-BOUND"
        print("OVERALL: CLOSED-NEGATIVE (RED) — MECHANISM-PREDICTOR-N4-BOUND. The redundancy-margin")
        print("  predictor ALSO fails to separate planning from all controls at n=5 (planning's margin")
        print("  does NOT exceed every control's, or planning is not redundancy-dominated at n=5). Like")
        print("  the coupling MAGNITUDE (H_1016), the redundancy explanation is an n=4 property; it does")
        print("  NOT generalize to n=5. The mechanism predictor's robustness is RULED OUT — the result")
        print("  BOUNDS the redundancy mechanism to n=4 (a_paper_negative_ok — publishable).")
        print("  VERDICT-TOKEN: MECHANISM-PREDICTOR-N4-BOUND")
    print("=" * 80)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=5 — both engines EXACT;")
    print("big-Phi super-exponential so n=5 is slow-but-tractable, n=6 is the honest cap (skipped, as")
    print("in H_1012/H_1016). The CPU mirror RE-PROVEN == stdlib at n=5 (H_1012 prove_mirrors_at_n)")
    print("BEFORE scoring; the PID is exact + deterministic on the SAME bits, validated on canonical")
    print("COPY(redundant)/XOR(synergy) cases. The PID is NOT a proxy for Phi — it is an info-")
    print("decomposition of the SAME bits (the explanatory variable). Scale-transfer beyond n=5")
    print("UNVERIFIED. g5 CODE-measured (no LLM self-judge, p7), a_phi_iit4_tool. NOT a forge binary; $0 CPU.")


if __name__ == "__main__":
    main()
