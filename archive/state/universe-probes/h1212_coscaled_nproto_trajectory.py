"""
H_1212 — CO-SCALED N_PROTO TRAJECTORY GATE (MITOSIS-ENGINE).

H_1211 found the GATE-B trajectory-coupling separation COLLAPSES along AXIS-T as the
stream length T grows, at a FIXED prototype-book size N_PROTO=24:
    WALK/WALK_SHUF = 10.916 (T=2400) -> 2.629 (T=24000) -> 1.136 (T=240000, FAIL).
Root cause (H_1211 ruling): finite-alphabet SATURATION of the predictability count
table — with only 24 symbols, as T grows EACH (prev,*) row fills enough that even a
SHUFFLED proto-id stream crosses CONF_FLOOR=0.34 by chance. H_1211 AXIS-P confirmed:
ENLARGING the alphabet at fixed toy T restores the separation.

This probe tests a PRINCIPLED CO-SCALING RULE N_PROTO = f(T) that keeps the per-row
observation budget obs_per_row = T/N_PROTO at the clean-toy value (~100), so the book
is never starved of symbols at long T. If GATE-B's ordered >> shuffle separation then
stays >= 1.5 across the SAME AXIS-T ladder where fixed-24 collapsed, the H_1211
collapse was a FIXED-BOOK artifact (fixable by co-scaling), not an intrinsic limit.

  PRIMARY (linear) rule:   N_PROTO(T) = round(T/100)        [obs_per_row ~ 100 const]
  SUB-LINEAR probe:        N_PROTO(T) = round(24*sqrt(T/2400))  [obs_per_row grows]
  CONTROL:                 N_PROTO = 24 fixed               [reproduce H_1211 collapse]

GATE-B + build_fixed_book + proto_ids (H_1208) and WALK/RANDGAUSS builders (H_1207/
H_1208) imported VERBATIM; the driver ONLY monkeypatches the pre-declared scale knobs
(T, WARMUP, MAX_CELLS) and sets N_PROTO via the rule (the SAME N_PROTO knob H_1211 set
to a fixed 24). Mechanism CODE byte-unchanged.

p7 (cell/transition count, NOT perplexity). p8 (split tick == growth). gradient-free.
$0 local CPU. 3 seeds. numpy mirror (H_1199/H_1208/H_1211 precedent). Frozen bar 1.5
NOT moved (inherited from H_1203/1208/1209/1211).
Pre-registered: .verdicts/1212_coscaled_nproto_trajectory/H_1212_FREEZE.txt
"""
import os, sys, time, math
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1163_tick_decode_metric as H          # _byte_feature / DIM / WIN_BYTES / STRIDE / WARMUP / T / CORPUS
import h1203_mitosis_novelty_coupling as H3   # constants + _load_corpus
import h1207_recurrent_split_key as H7        # make_walk_stream / make_walk_shuffled VERBATIM
import h1208_predictability_split_gate as H8  # GATE-B + build_fixed_book + proto_ids + randgauss VERBATIM

BAR = 1.5
SEEDS = [900, 901, 902]
TOY_CORPUS = H.CORPUS

# AXIS-T ladder — IDENTICAL to H_1211 (the rungs where fixed-24 collapsed)
LADDER = [("T-toy:2400", 2400, 250), ("T-10x:24000", 24000, 2500), ("T-100x:240000", 240000, 25000)]
BIG_CAP = 10**9   # never clip growth at long T (a cap would be a scale artifact)


# ── co-scaling rules (pre-registered in FREEZE) ─────────────────────────────────
def n_proto_linear(T):     return max(2, int(round(T / 100.0)))            # obs_per_row ~ 100 const
def n_proto_sqrt(T):       return max(2, int(round(24.0 * math.sqrt(T / 2400.0))))
def n_proto_fixed(T):      return 24                                       # H_1211 control


def _set_scale(T, warmup):
    """Monkeypatch the pre-declared scale knobs on EVERY module that captured a copy at
    import. Builder/gate CODE byte-unchanged; only these scalars move (FREEZE-declared)."""
    for m in (H, H3, H7, H8):
        if hasattr(m, "T"):       m.T = T
        if hasattr(m, "WARMUP"):  m.WARMUP = warmup
    for m in (H3, H7, H8):
        if hasattr(m, "MAX_CELLS"): m.MAX_CELLS = BIG_CAP
    H.CORPUS = TOY_CORPUS
    H3.CORPUS = TOY_CORPUS
    if hasattr(H7, "CORPUS"): H7.CORPUS = TOY_CORPUS


def measure_trajectory(n_proto, max_cells):
    """H_1208 GATE-B on the ORDERED WALK stream + RANDGAUSS sanity, at a given N_PROTO.
    Returns 3-seed means + the clamp note (book can't exceed scored span)."""
    H8.N_PROTO = n_proto                         # the SAME knob H_1211 set to fixed 24
    arms = {"WALK": H7.make_walk_stream, "WALK_SHUF": H7.make_walk_shuffled,
            "RANDGAUSS": H8.make_randgauss_stream, "RANDGAUSS_SHUF": H8.make_randgauss_shuffled}
    b = {a: [] for a in arms}
    book_sizes = []
    for s in SEEDS:
        for a, mk in arms.items():
            X = mk(s)
            book = H8.build_fixed_book(X, s)     # VERBATIM (clamps to span internally)
            if a == "WALK":
                book_sizes.append(len(book))
            ids = H8.proto_ids(X, book)
            b[a].append(H8.gate_B_transition_predictability(ids, max_cells))
    m = {a: float(np.mean(b[a])) for a in arms}
    f2 = m["WALK"] / max(m["WALK_SHUF"], 1e-9)
    san = m["RANDGAUSS"] / max(m["RANDGAUSS_SHUF"], 1e-9)
    actual_book = int(round(float(np.mean(book_sizes))))   # realized (post-clamp) WALK book
    return m, b, f2, san, actual_book


def run_rule(rule_name, n_proto_fn):
    print(f"\n########## RULE: {rule_name} ##########", flush=True)
    rows = []
    for lab, T, wu in LADDER:
        t0 = time.time()
        _set_scale(T, wu)
        npp = n_proto_fn(T)
        m, b, f2, san, actual = measure_trajectory(npp, BIG_CAP)
        obs_per_row = T / max(npp, 1)
        clamp = "" if actual >= npp else f"  [CLAMPED to span: requested {npp} -> book {actual}]"
        print(f"=== RUNG [{lab}]  T={T} N_PROTO(req)={npp} obs/row={obs_per_row:.1f}{clamp} ===", flush=True)
        print(f"  WALK={m['WALK']:.1f}(seed {b['WALK']})  WALK_SHUF={m['WALK_SHUF']:.1f}(seed {b['WALK_SHUF']})  "
              f"RANDG={m['RANDGAUSS']:.1f}(seed {b['RANDGAUSS']})  RANDG_SHUF={m['RANDGAUSS_SHUF']:.1f}(seed {b['RANDGAUSS_SHUF']})", flush=True)
        print(f"  F2 WALK/WALK_SHUF = {f2:7.3f}  (bar>={BAR})  -> {'PASS' if f2>=BAR else 'FAIL'}", flush=True)
        print(f"  sanity RANDG/SHUF = {san:7.3f}  (honest if << F2; flag if >={BAR})", flush=True)
        print(f"  [rung wall {time.time()-t0:.1f}s]", flush=True)
        rows.append({"lab": lab, "T": T, "n_req": npp, "n_act": actual,
                     "obs_per_row": obs_per_row, "f2": f2, "san": san})
    return rows


def main():
    print("================================================================================", flush=True)
    print("H_1212 CO-SCALED N_PROTO TRAJECTORY GATE — numpy mirror, $0 CPU, p7/p8, 3 seeds", flush=True)
    print(f"SEEDS={SEEDS}  BAR={BAR}  DIM={H.DIM} (structural, NOT scaled)", flush=True)
    print("GATE-B + build_fixed_book + proto_ids (H_1208) + WALK/RANDGAUSS (H_1207/1208) VERBATIM;", flush=True)
    print("driver sets ONLY pre-declared scale knobs (T,WARMUP,MAX_CELLS) + N_PROTO via the rule.", flush=True)
    print("AXIS-T ladder IDENTICAL to H_1211 (where fixed-24 collapsed 10.9->2.63->1.136).", flush=True)
    print("================================================================================", flush=True)

    linear = run_rule("PRIMARY linear  N_PROTO=round(T/100)  [obs/row~100 const]", n_proto_linear)
    sublin = run_rule("SUB-LINEAR probe  N_PROTO=round(24*sqrt(T/2400))  [obs/row grows]", n_proto_sqrt)
    fixed  = run_rule("CONTROL fixed  N_PROTO=24  [reproduce H_1211 collapse]", n_proto_fixed)

    # ── LADDER SUMMARY ────────────────────────────────────────────────────────────
    print("\n================================================================================", flush=True)
    print("LADDER CURVES (3-seed means; a_scale_honest_scope)", flush=True)
    print("================================================================================", flush=True)
    hdr = f"{'rule':18s} {'rung':16s} {'T':>8s} {'N_req':>6s} {'N_act':>6s} {'obs/row':>9s} {'F2 WALK/SHUF':>13s} {'sanity':>8s}"
    print(hdr, flush=True)
    for name, rows in (("linear", linear), ("sqrt-sublin", sublin), ("fixed-24", fixed)):
        for r in rows:
            flag = " FAIL" if r["f2"] < BAR else ""
            print(f"{name:18s} {r['lab']:16s} {r['T']:8d} {r['n_req']:6d} {r['n_act']:6d} "
                  f"{r['obs_per_row']:9.1f} {r['f2']:13.3f}{flag} {r['san']:8.3f}", flush=True)

    # ── FROZEN FALSIFIERS ─────────────────────────────────────────────────────────
    lin_min = min(r["f2"] for r in linear)
    lin_pass = all(r["f2"] >= BAR for r in linear)
    sqrt_min = min(r["f2"] for r in sublin)
    sqrt_pass = all(r["f2"] >= BAR for r in sublin)
    # control: fixed-24 must reproduce the H_1211 collapse (drop below bar at T=240000)
    fixed_100x = [r for r in fixed if r["T"] == 240000]
    fixed_collapses = bool(fixed_100x) and fixed_100x[0]["f2"] < BAR
    # sanity honesty under the PRIMARY (linear) rule
    lin_san_flags = [r for r in linear if r["san"] >= BAR and not (r["f2"] >= 3 * r["san"])]

    print("\n=== FROZEN FALSIFIERS (bar = 1.5, inherited from H_1203/1208/1209/1211, NOT moved) ===", flush=True)
    print(f"  F1 SCALE-ROBUST RESTORATION (PRIMARY linear, WALK/WALK_SHUF >= {BAR} at EVERY rung):", flush=True)
    print(f"     min F2 = {lin_min:.3f}  -> {'PASS' if lin_pass else 'FAIL'}", flush=True)
    print(f"  F2 CONTROL (fixed-24 still collapses on the SAME ladder, attribution):", flush=True)
    print(f"     fixed-24 @T=240000 F2 = {fixed_100x[0]['f2']:.3f} (H_1211 ref ~1.136) -> "
          f"{'COLLAPSE CONFIRMED' if fixed_collapses else 'MISMATCH (invalidates comparison!)'}", flush=True)
    print(f"  F3 NO FREE LUNCH (cost of the rule):", flush=True)
    print(f"     PRIMARY linear N_PROTO grows ~linearly with T (round(T/100)): "
          f"{[r['n_req'] for r in linear]} -> {'LINEAR cost (honest)' if lin_pass else 'n/a'}", flush=True)
    print(f"     SUB-LINEAR sqrt N_PROTO = {[r['n_req'] for r in sublin]}  min F2 = {sqrt_min:.3f}  -> "
          f"{'HOLDS (STRONG RESULT: sub-linear cost)' if sqrt_pass else 'FAILS (linear cost needed)'}", flush=True)
    if lin_san_flags:
        print(f"  SANITY note (PRIMARY): {len(lin_san_flags)} rung(s) flagged (sanity rivals F2):", flush=True)
        for r in lin_san_flags:
            print(f"     {r['lab']}: sanity={r['san']:.3f} vs F2={r['f2']:.3f}  INSPECT", flush=True)
    else:
        print(f"  SANITY (PRIMARY): all RANDGAUSS sanity ratios honest (<< F2 or < {BAR}).", flush=True)

    # ── TIER ──────────────────────────────────────────────────────────────────────
    if lin_pass and fixed_collapses:
        cost = ("SUB-LINEAR (sqrt rule ALSO holds — the alphabet need only grow as sqrt(T); "
                "trajectory substrate is scale-robust at sub-linear book cost = the STRONG result)"
                if sqrt_pass else
                "LINEAR (only round(T/100) holds; the alphabet must grow ~linearly with T to keep "
                "separation — a real, honestly-stated cost, NOT free)")
        tier = ("GREEN (🟢 scale-robust UNDER co-scaling) — with the principled co-scaling rule "
                "N_PROTO=round(T/100) (obs_per_row held at the clean-toy ~100), GATE-B WALK/WALK_SHUF "
                f">= {BAR} at EVERY rung of the SAME AXIS-T ladder where fixed-24 collapsed (incl "
                "T=240000), while the fixed-24 CONTROL still collapses (attribution clean). This "
                "REFINES H_1211's 'toy artifact' to a 'fixed-book artifact, fixable by a principled "
                "N_PROTO co-scaling rule': the predictability/trajectory substrate (H_1209/1210) "
                f"PROMOTES from toy to SCALE-QUALIFIED-GREEN. COST: {cost}. PAPER-SUPERSEDE FLAGGED "
                "for PAPER/mitosis-substrate-lane (a follow-on supersede handles it; the merged "
                "paper is NOT silently edited).")
    elif lin_pass and not fixed_collapses:
        tier = ("INCONCLUSIVE — the PRIMARY rule holds F1 but the fixed-24 CONTROL did NOT reproduce "
                "the H_1211 collapse on this ladder, so the restoration is NOT cleanly attributable "
                "to co-scaling (a stream/seed/code difference vs H_1211 must be found before any "
                "promotion). Report + investigate.")
    else:
        tier = ("RED (🔴 honest closed-neg, a_scale_honest_scope · a_paper_negative_ok) — even the "
                "principled co-scaling rule does NOT restore GATE-B separation across the ladder "
                f"(min F2 = {lin_min:.3f} < {BAR}). The saturation is INTRINSIC to the predictability "
                "gate, not merely a book-resourcing artifact; co-scaling does not save it. The "
                "trajectory substrate stays toy-scoped (H_1211's scale-break stands). A valid "
                "closed-negative; report WHERE the co-scaled rule still breaks.")
    print(f"\nTIER: {tier}", flush=True)

    print("\nHONESTY (a_scale_honest_scope): numpy mirror (H_1199/1208/1211 precedent), gradient-free, "
          "$0 CPU, 3 seeds. GATE-B + build_fixed_book + proto_ids (H_1208) + WALK/RANDGAUSS builders "
          "(H_1207/1208) imported VERBATIM; the driver monkeypatches ONLY the pre-declared scale knobs "
          "(T, WARMUP, MAX_CELLS) and sets N_PROTO via the co-scaling rule (the SAME N_PROTO knob "
          "H_1211 set to fixed 24) — mechanism CODE byte-unchanged. AXIS-T ladder IDENTICAL to H_1211. "
          "DIM=8 structural, NOT scaled. p7 (cell/transition count, NOT perplexity), p8 (split == "
          "growth). Frozen bar (1.5) inherited, NOT moved. Ladder reported as the full CURVE.", flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
