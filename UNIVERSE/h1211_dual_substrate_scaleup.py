"""
H_1211 — DUAL-SUBSTRATE SCALE-UP (MITOSIS-ENGINE).

Re-tests the H_1202-1210 arc's ONE honest gap: TOY SCALE. The central finding is a
DENSITY-vs-TRAJECTORY dual-substrate split (H_1203 density gate = novelty-density-
sensitive but trajectory-blind; H_1208/H_1209 GATE-B trajectory gate = separates only
on ORDERED streams). All measured at toy scale (DIM=8, T=2400, one 402 KB corpus).

Per a_toy_scale_recheck this driver re-runs the SAME builders + gates, imported
VERBATIM, across a pre-registered >=3-rung scale ladder on THREE orthogonal axes:
  AXIS-T  stream length T  {2400, 24000, 240000}   (warmup scaled to keep fraction)
  AXIS-C  corpus  {clm_mid_5lang_c4 402KB, flores5 1.65MB, data/corpus.txt 5.24MB}
  AXIS-P  trajectory-gate alphabet N_PROTO  {24, 64, 128}

The mechanism CODE is byte-unchanged; the ladder ONLY monkeypatches the pre-declared
scale constants on the imported modules (apples-to-apples). DIM stays 8 (structural —
_byte_feature emits exactly 8 features; declared in the FREEZE).

p7 (cell-count / ratio, NOT perplexity). p8 (split == growth). gradient-free. $0 CPU.
3 seeds. numpy mirror (H_1199 precedent). Frozen bars (1.5) NOT moved.
Pre-registered: .verdicts/1211_dual_substrate_scaleup/H_1211_FREEZE.txt
"""
import os, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1163_tick_decode_metric as H          # _byte_feature / DIM / WIN_BYTES / STRIDE / WARMUP / T / CORPUS
import h1203_mitosis_novelty_coupling as H3   # DENSITY gate (run_vadapt) + make_novel/repeat/shuffled VERBATIM
import h1207_recurrent_split_key as H7        # make_walk_stream / make_walk_shuffled VERBATIM
import h1208_predictability_split_gate as H8  # TRAJECTORY GATE-B + build_fixed_book + proto_ids + randgauss VERBATIM

BAR = 1.5
SEEDS = [900, 901, 902]
TOY_CORPUS = H.CORPUS
CORPORA = {
    "clm_mid_5lang_c4(402KB)": os.path.join(os.path.dirname(__file__), "..", "CORE", "testdata", "clm_mid_5lang_c4.txt"),
    "flores5_devtest(1.65MB)": os.path.join(os.path.dirname(__file__), "..", "CORE", "testdata", "flores5_dev_devtest.txt"),
    "data_corpus(5.24MB)":     os.path.join(os.path.dirname(__file__), "..", "data", "corpus.txt"),
}


def _set_scale(T, warmup, corpus, n_proto, max_cells):
    """Monkeypatch the pre-declared scale constants on EVERY module that captured a
    copy at import time. The builder/gate CODE is byte-unchanged (verbatim reuse);
    only these scalar knobs move (declared in H_1211_FREEZE.txt)."""
    # stream length + warmup — H3 globals are what make_novel/repeat/shuffled read;
    # H7 (walk) reads WARMUP/T from its own globals (= copies of H3's at import).
    for m in (H, H3, H7, H8):
        if hasattr(m, "T"):       m.T = T
        if hasattr(m, "WARMUP"):  m.WARMUP = warmup
    # cell cap (raise so long-T growth is never prematurely clipped)
    for m in (H3, H7, H8):
        if hasattr(m, "MAX_CELLS"): m.MAX_CELLS = max_cells
    # corpus path (H3._load_corpus reads H3.CORPUS; H7/H8 call H3._load_corpus / H3.make_*)
    H.CORPUS = corpus
    H3.CORPUS = corpus
    if hasattr(H7, "CORPUS"): H7.CORPUS = corpus
    # trajectory-gate alphabet
    H8.N_PROTO = n_proto


def measure_density(max_cells):
    """H_1203 DENSITY gate on PRIMARY i.i.d. streams (run_vadapt VERBATIM).
    Returns 3-seed means: NOVEL/REPEAT (F1) and NOVEL/SHUFFLED (dual-split blindness)."""
    arms = {"NOVEL": H3.make_novel_stream, "REPEAT": H3.make_repeat_stream,
            "SHUFFLED": H3.make_shuffled_stream}
    g = {a: [] for a in arms}
    for s in SEEDS:
        for a, mk in arms.items():
            X = mk(s)
            _, final, _ = H3.run_vadapt(X, True, max_cells)
            g[a].append(final - 1)
    m = {a: float(np.mean(g[a])) for a in arms}
    f1 = m["NOVEL"] / max(m["REPEAT"], 1e-9)       # density coupling
    f_blind = m["NOVEL"] / max(m["SHUFFLED"], 1e-9)  # must stay ~1 (trajectory-blind)
    return m, g, f1, f_blind


def measure_trajectory(max_cells):
    """H_1208 GATE-B (transition-predictability) on the ORDERED WALK stream + sanity.
    Returns 3-seed means: WALK/WALK_SHUF (F2) and RANDGAUSS/RANDGAUSS_SHUF (sanity)."""
    arms = {"WALK": H7.make_walk_stream, "WALK_SHUF": H7.make_walk_shuffled,
            "RANDGAUSS": H8.make_randgauss_stream, "RANDGAUSS_SHUF": H8.make_randgauss_shuffled}
    b = {a: [] for a in arms}
    for s in SEEDS:
        for a, mk in arms.items():
            X = mk(s)
            book = H8.build_fixed_book(X, s)
            ids = H8.proto_ids(X, book)
            b[a].append(H8.gate_B_transition_predictability(ids, max_cells))
    m = {a: float(np.mean(b[a])) for a in arms}
    f2 = m["WALK"] / max(m["WALK_SHUF"], 1e-9)          # trajectory separation (ordered)
    san = m["RANDGAUSS"] / max(m["RANDGAUSS_SHUF"], 1e-9)  # noise-floor sanity
    return m, b, f2, san


def run_rung(label, T, warmup, corpus, n_proto, max_cells, do_density=True, do_traj=True):
    t0 = time.time()
    _set_scale(T, warmup, corpus, n_proto, max_cells)
    cn = os.path.basename(corpus)
    print(f"\n=== RUNG [{label}]  T={T} WARMUP={warmup} N_PROTO={n_proto} corpus={cn} ===", flush=True)
    rec = {"label": label, "T": T, "n_proto": n_proto, "corpus": cn}
    if do_density:
        md, gd, f1, fblind = measure_density(max_cells)
        print(f"  DENSITY  NOVEL={md['NOVEL']:.1f}(seed {gd['NOVEL']})  REPEAT={md['REPEAT']:.1f}(seed {gd['REPEAT']})  "
              f"SHUFFLED={md['SHUFFLED']:.1f}(seed {gd['SHUFFLED']})", flush=True)
        print(f"           F1 NOVEL/REPEAT   = {f1:7.3f}  (bar>={BAR})  -> {'PASS' if f1>=BAR else 'FAIL'}", flush=True)
        print(f"           blind NOVEL/SHUF  = {fblind:7.3f}  (dual-split needs <{BAR}: trajectory-BLIND)  "
              f"-> {'BLIND-ok' if fblind<BAR else 'COUPLED-break'}", flush=True)
        rec.update(f1=f1, f_blind=fblind, dens=md)
    if do_traj:
        mt, bt, f2, san = measure_trajectory(max_cells)
        print(f"  TRAJ-B   WALK={mt['WALK']:.1f}(seed {bt['WALK']})  WALK_SHUF={mt['WALK_SHUF']:.1f}(seed {bt['WALK_SHUF']})  "
              f"RANDG={mt['RANDGAUSS']:.1f}(seed {bt['RANDGAUSS']})  RANDG_SHUF={mt['RANDGAUSS_SHUF']:.1f}(seed {bt['RANDGAUSS_SHUF']})", flush=True)
        print(f"           F2 WALK/WALK_SHUF = {f2:7.3f}  (bar>={BAR})  -> {'PASS' if f2>=BAR else 'FAIL'}", flush=True)
        print(f"           sanity RANDG/SHUF = {san:7.3f}  (honest if << F2; flag if >={BAR})", flush=True)
        rec.update(f2=f2, sanity=san, traj=mt)
    print(f"  [rung wall {time.time()-t0:.1f}s]", flush=True)
    return rec


def main():
    print("================================================================================", flush=True)
    print("H_1211 DUAL-SUBSTRATE SCALE-UP — numpy mirror (H_1199), $0 CPU, p7/p8, 3 seeds", flush=True)
    print(f"SEEDS={SEEDS}  BAR={BAR}  DIM={H.DIM} (structural, NOT scaled — see FREEZE)", flush=True)
    print("builders+gates imported VERBATIM (H_1203 density · H_1207 walk · H_1208 GATE-B);", flush=True)
    print("the ladder ONLY monkeypatches pre-declared scale constants. Frozen bars NOT moved.", flush=True)
    print("================================================================================", flush=True)

    BIG_CAP = 10**9   # never clip growth at long T (a cap would be a scale artifact)
    rungs = []

    # ── AXIS-T : STREAM LENGTH (warmup scaled to keep the ~9.4% warmup fraction) ──
    print("\n########## AXIS-T : STREAM LENGTH (toy / 10x / 100x) ##########", flush=True)
    axisT = [("T-toy:2400", 2400, 250), ("T-10x:24000", 24000, 2500), ("T-100x:240000", 240000, 25000)]
    for lab, T, wu in axisT:
        rungs.append(("AXIS-T", run_rung(lab, T, wu, TOY_CORPUS, 24, BIG_CAP)))

    # ── AXIS-C : CORPUS (toy / 4x / 13x) at fixed toy T=2400 ──────────────────────
    print("\n########## AXIS-C : CORPUS (402KB / 1.65MB / 5.24MB) @ T=2400 ##########", flush=True)
    for cname, cpath in CORPORA.items():
        rungs.append(("AXIS-C", run_rung(f"C:{cname}", 2400, 250, cpath, 24, 2048)))

    # ── AXIS-P : TRAJECTORY ALPHABET N_PROTO (24 / 64 / 128) @ toy T, toy corpus ──
    print("\n########## AXIS-P : TRAJECTORY ALPHABET N_PROTO (24 / 64 / 128) @ T=2400 ##########", flush=True)
    # density is N_PROTO-independent; measure it ONCE (toy) and carry it for the dual-split.
    _set_scale(2400, 250, TOY_CORPUS, 24, 2048)
    md0, gd0, f1_0, fblind_0 = measure_density(2048)
    print(f"  [density is book-independent; toy density carried: F1={f1_0:.3f} blind={fblind_0:.3f}]", flush=True)
    for npp in (24, 64, 128):
        rec = run_rung(f"P:N_PROTO={npp}", 2400, 250, TOY_CORPUS, npp, 2048, do_density=False, do_traj=True)
        rec.update(f1=f1_0, f_blind=fblind_0)   # carry toy density for the dual-split check
        rungs.append(("AXIS-P", rec))

    # ── LADDER SUMMARY + FROZEN FALSIFIERS ────────────────────────────────────────
    print("\n================================================================================", flush=True)
    print("LADDER CURVES (3-seed means; a_scale_honest_scope)", flush=True)
    print("================================================================================", flush=True)
    print(f"{'axis':8s} {'rung':24s} {'F1 dens NOVEL/REP':>18s} {'blind NOVEL/SHUF':>17s} {'F2 WALK/SHUF':>14s} {'sanity':>9s}", flush=True)
    for axis, r in rungs:
        f1 = r.get("f1"); fb = r.get("f_blind"); f2 = r.get("f2"); sn = r.get("sanity")
        s1 = f"{f1:7.3f}" if f1 is not None else "    -  "
        sb = f"{fb:7.3f}" if fb is not None else "    -  "
        s2 = f"{f2:7.3f}" if f2 is not None else "    -  "
        ss = f"{sn:6.3f}" if sn is not None else "   -  "
        print(f"{axis:8s} {r['label']:24s} {s1:>18s} {sb:>17s} {s2:>14s} {ss:>9s}", flush=True)

    # F1: density coupling >= bar at EVERY rung that measured it
    f1_vals = [(axis, r["label"], r["f1"]) for axis, r in rungs if r.get("f1") is not None]
    f1_pass = all(v >= BAR for _, _, v in f1_vals)
    # F2: trajectory separation >= bar at EVERY rung that measured it
    f2_vals = [(axis, r["label"], r["f2"]) for axis, r in rungs if r.get("f2") is not None]
    f2_pass = all(v >= BAR for _, _, v in f2_vals)
    # F3: dual-split — density BLIND (<bar) AND trajectory SEPARATES (>=bar) at every rung
    blind_vals = [(axis, r["label"], r["f_blind"]) for axis, r in rungs if r.get("f_blind") is not None]
    dens_blind_ok = all(v < BAR for _, _, v in blind_vals)
    traj_sep_ok = f2_pass
    f3_pass = dens_blind_ok and traj_sep_ok
    # sanity honesty (report; flag if a sanity ratio rivals its rung F2)
    san_flags = [(axis, r["label"], r["sanity"], r["f2"]) for axis, r in rungs
                 if r.get("sanity") is not None and r["sanity"] >= BAR]

    print("\n=== FROZEN FALSIFIERS (bar = 1.5, pre-registered, NOT moved) ===", flush=True)
    print(f"  F1 DENSITY scale-stability (NOVEL/REPEAT >= {BAR} at all rungs): "
          f"min={min(v for _,_,v in f1_vals):.3f}  -> {'PASS' if f1_pass else 'FAIL'}", flush=True)
    print(f"  F2 TRAJECTORY scale-stability (WALK/WALK_SHUF >= {BAR} at all rungs): "
          f"min={min(v for _,_,v in f2_vals):.3f}  -> {'PASS' if f2_pass else 'FAIL'}", flush=True)
    print(f"  F3 DUAL-SPLIT persists (density BLIND <{BAR} AND trajectory SEPARATES >={BAR}, all rungs): "
          f"-> {'PASS' if f3_pass else 'FAIL'}", flush=True)
    print(f"     - density trajectory-BLIND on i.i.d. (max NOVEL/SHUF = "
          f"{max(v for _,_,v in blind_vals):.3f} < {BAR}): {'OK' if dens_blind_ok else 'BROKEN'}", flush=True)
    print(f"     - trajectory SEPARATES on ordered (all WALK/WALK_SHUF >= {BAR}): "
          f"{'OK' if traj_sep_ok else 'BROKEN'}", flush=True)
    if san_flags:
        print(f"  SANITY note: {len(san_flags)} rung(s) have RANDGAUSS sanity >= {BAR} (inspect vs F2):", flush=True)
        for axis, lab, sn, f2 in san_flags:
            print(f"     {axis} {lab}: sanity={sn:.3f} vs F2={f2:.3f}  "
                  f"({'noise-floor small-int (honest, F2>>sanity)' if f2 >= 3*sn else 'INSPECT'})", flush=True)
    else:
        print(f"  SANITY: all RANDGAUSS sanity ratios < {BAR} (clean noise floor).", flush=True)

    if f1_pass and f2_pass and f3_pass:
        tier = ("GREEN (🟢 scale-robust) — the DENSITY-vs-TRAJECTORY dual-substrate split HOLDS "
                "at EVERY rung of all three axes (stream length 100x, corpus 13x, alphabet 5.3x). "
                "The toy H_1202-1210 verdict PROMOTES to a scale-robust finding: the density gate "
                "stays novelty-coupled + trajectory-blind on i.i.d., the trajectory gate keeps "
                "separating on ordered streams. 'The determinant is the stream, not the gate' "
                "survives scale-up (a_toy_scale_recheck satisfied; paper claim stands).")
    elif f1_pass and f2_pass:
        tier = ("PARTIAL (🟠) — F1+F2 hold but the qualitative dual-split shows a wrinkle at a "
                "rung (see curve). Toy verdict QUALIFIED, not fully promoted.")
    else:
        tier = ("RED (🔴 honest scale-break, a_paper_negative_ok) — the dual-split BREAKS at an "
                "identified rung (see curve + per-falsifier lines for WHERE/WHY). The toy finding "
                "was a scale artifact on that axis; a paper-supersede FLAG is required (do NOT "
                "silently edit the merged PAPER/mitosis-substrate-lane).")
    print(f"\nTIER: {tier}", flush=True)
    print("\nHONESTY (a_scale_honest_scope): numpy mirror (H_1199 precedent), gradient-free, $0 CPU, "
          "3 seeds. Builders + gates (H_1203 density · H_1207 walk · H_1208 GATE-B) imported VERBATIM; "
          "the ladder monkeypatches ONLY the pre-declared scale constants (T, WARMUP, MAX_CELLS, "
          "CORPUS, N_PROTO) — mechanism CODE byte-unchanged. DIM=8 is structural and NOT scaled "
          "(declared in FREEZE: _byte_feature emits exactly 8 features). p7 (cell-count/ratio, NOT "
          "perplexity), p8 (split == growth). Frozen bar (1.5) NOT moved. Ladder reported as the "
          "full CURVE per a_scale_honest_scope.", flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
