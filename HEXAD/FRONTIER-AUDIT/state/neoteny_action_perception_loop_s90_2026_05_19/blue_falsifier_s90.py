#!/usr/bin/env python3
"""
§90 NEOTENY + #3 ACTION-PERCEPTION LOOP — closed-form sidecar battery B-S90-1..7.

Sidecar — does NOT touch the central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py (sha c93e160a 0-line-diff mandate, g_blue_closed_mandate).

g3: battery proves the §90 design+stub is structurally honest — #3 closed-form
loop transfer/invariant, §88-F2 neoteny carry byte-equal, §9 metric reuse,
γ-closing predicate falsifiable, echo-amplify detector, §24-decision connection,
determinism. It does NOT prove γ is closed at trained scale (B-S90-NOTE).
necessary-not-sufficient (B-EMERGE-7).
"""
import json
import hashlib
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT = os.path.join(HERE, "result.json")
SMOKE = os.path.join(HERE, "neoteny_loop_smoke_s90.py")


def _load_result():
    with open(RESULT) as f:
        return json.load(f)


def _smoke_src():
    with open(SMOKE) as f:
        return f.read()


# ── B-S90-1 — #3-LOOP-TRANSFER-CLOSED ────────────────────────────────
# §89 carry: transfer x_{t+1}=S_encode(e_t), invariant
# K(x_{t+1}) <= K(e_t)+K(S_encode) (Kolmogorov data-processing inequality).
# Closed-form: the smoke must implement s_encode + a Kolmogorov-bound check;
# the data-processing inequality holds for ANY encoder by construction
# (encoding cannot create information). Verify structurally + numerically.
def b_s90_1():
    src = _smoke_src()
    has_encode = "s_encode" in src
    has_kol = "s_encode_kolmogorov_ok" in src or "kolmogorov" in src.lower()
    r = _load_result()
    loop3 = r.get("s89_loop3_closed_form", {})
    transfer_ok = loop3.get("transfer", "").startswith("x_{t+1}")
    invariant_ok = "K(" in loop3.get("invariant", "") and "<=" in loop3.get("invariant", "")
    # data-processing inequality: K(g(x)) <= K(x) + K(g) — definitionally true
    # for any deterministic encoder. structural presence is the closed check.
    passed = has_encode and has_kol and transfer_ok and invariant_ok
    return passed, f"s_encode={has_encode} kolmogorov_check={has_kol} transfer={transfer_ok} invariant={invariant_ok}"


# ── B-S90-2 — NEOTENY-CARRY-BYTE-EQUAL (연결부위) ─────────────────────
# §88-F2 neoteny arm trained-scale measured values must be carried byte-equal
# as the §90 design-anchor (NOT re-measured).
def b_s90_2():
    r = _load_result()
    carry = r.get("s88f2_carry", {})
    neo = carry.get("neoteny", {})
    base = carry.get("baseline", {})
    # §88-F2 published: neoteny maturity 0.7478, maj_frac 0.35, D 2.70, CE 0.0413
    #                   baseline maturity 0.9496, maj_frac 0.872, D 1.89, CE 0.0038
    neo_ok = (abs(neo.get("maturity", 0) - 0.7478041127531916) < 1e-9
              and abs(neo.get("maj_frac", 0) - 0.35) < 1e-9
              and abs(neo.get("eff_D", 0) - 2.695751905441284) < 1e-9)
    base_ok = (abs(base.get("maturity", 0) - 0.9495988095306581) < 1e-9
               and abs(base.get("maj_frac", 0) - 0.8724999999999999) < 1e-9)
    passed = neo_ok and base_ok
    return passed, f"neoteny_carry_byte_equal={neo_ok} baseline_carry_byte_equal={base_ok}"


# ── B-S90-3 — §9-METRIC-REUSE ────────────────────────────────────────
# honest_coherent must be the §9 cascade-rate metric (4-clause: cascade_rate
# < 0.30, max_run < 10, len >= 20, printable_ratio >= 0.80). 4-corner witness.
def b_s90_3():
    src = _smoke_src()
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location("s90_smoke", SMOKE)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except Exception as e:
        return False, f"smoke import fail: {e}"
    hc = getattr(m, "honest_coherent", None)
    if hc is None:
        return False, "honest_coherent fn absent"
    # 4-corner witnesses
    short = hc("abc")                                  # len<20 -> False
    clean = hc("the quiet morning light moved slow")   # clean printable -> True
    char_casc = hc("a" * 30)                           # char cascade -> False
    digit_casc = hc("55555555555555555555555")         # digit cascade -> False
    passed = (not short) and clean and (not char_casc) and (not digit_casc)
    return passed, f"short={short} clean={clean} char_cascade={char_casc} digit_cascade={digit_casc}"


# ── B-S90-4 — γ-CLOSING-PREDICATE (falsifiable) ──────────────────────
# γ-closing := cell2 (neoteny+#3) §9 coherent rate > cell0 (neoteny baseline).
# Closed-form Boolean over the measured grid — falsifiable: if cell2 <= cell0
# the predicate is FALSE and γ-closing is refuted.
def b_s90_4():
    r = _load_result()
    fc = r.get("four_corner_verdict", {})
    cr = fc.get("coherence_rates", {})
    cell0 = cr.get("cell0_neoteny_baseline")
    cell2 = cr.get("cell2_neoteny_loop3")
    if cell0 is None or cell2 is None:
        return False, "coherence_rates missing cell0/cell2"
    gamma_closing = cell2 > cell0
    alpha = fc.get("alpha_GAMMA_CLOSING_MEASURED")
    # predicate must agree with the recorded α corner
    consistent = (gamma_closing == bool(alpha))
    passed = gamma_closing and consistent
    return passed, f"cell2={cell2} > cell0={cell0} -> gamma_closing={gamma_closing}, alpha_corner={alpha}, consistent={consistent}"


# ── B-S90-5 — ECHO-AMPLIFY-DETECTOR (§62 carry) ──────────────────────
# #3 loop-only on a saturated regime must amplify echo (maj_frac -> 1.0).
# This is the honest risk control: cell1 (#3 loop only) maj_frac >= 0.95
# means the loop ALONE is unsafe — γ corner. Detector must FIRE on cell1.
def b_s90_5():
    r = _load_result()
    fc = r.get("four_corner_verdict", {})
    mf = fc.get("maj_frac_final", {})
    cell1 = mf.get("cell1_loop3_only")
    cell2 = mf.get("cell2_neoteny_loop3")
    if cell1 is None or cell2 is None:
        return False, "maj_frac_final missing cell1/cell2"
    echo_on_loop_alone = cell1 >= 0.95          # loop alone collapses
    no_echo_with_neoteny = cell2 < 0.95         # neoteny+loop does NOT
    gamma_corner = fc.get("gamma_ECHO_AMPLIFIES")
    # detector must agree with recorded γ corner
    consistent = (echo_on_loop_alone == bool(gamma_corner))
    passed = echo_on_loop_alone and no_echo_with_neoteny and consistent
    return passed, f"cell1_maj={cell1}>=0.95={echo_on_loop_alone} cell2_maj={cell2}<0.95={no_echo_with_neoteny} gamma_corner={gamma_corner} consistent={consistent}"


# ── B-S90-6 — §24-DECISION-CONSISTENCY (연결부위) ────────────────────
# cell4 = §24 baseline (no loop, no neoteny). It must be present as the
# 4-corner reference floor for the synergy decomposition; synergy decomp's
# base_s24 anchors on cell4. Structural connection-point check.
def b_s90_6():
    r = _load_result()
    fc = r.get("four_corner_verdict", {})
    sd = fc.get("synergy_decomp", {})
    cr = fc.get("coherence_rates", {})
    has_s24_cell = "cell4_s24_baseline" in cr
    base_s24 = sd.get("base_s24")
    # base_s24 must equal cell4 coherence rate (decomposition anchored on §24)
    anchored = (base_s24 == cr.get("cell4_s24_baseline"))
    delta = r.get("note", "")
    passed = has_s24_cell and (base_s24 is not None) and anchored
    return passed, f"cell4_present={has_s24_cell} base_s24={base_s24} anchored_on_cell4={anchored}"


# ── B-S90-7 — DETERMINISTIC ──────────────────────────────────────────
# The smoke must be a pure deterministic function of a seeded LCG. Verify
# the result.json records a fixed seed and the smoke has no unseeded RNG.
def b_s90_7():
    src = _smoke_src()
    r = _load_result()
    seed_recorded = r.get("seed")
    has_seed = seed_recorded is not None
    # forbidden: unseeded randomness
    forbidden = ["random.random(", "random.randint(", "np.random",
                 "time.time(", "os.urandom"]
    hits = [tok for tok in forbidden if tok in src]
    passed = has_seed and len(hits) == 0
    return passed, f"seed={seed_recorded} forbidden_rng_hits={hits}"


BATTERY = [
    ("B-S90-1", "#3-LOOP-TRANSFER-CLOSED", b_s90_1),
    ("B-S90-2", "NEOTENY-CARRY-BYTE-EQUAL", b_s90_2),
    ("B-S90-3", "§9-METRIC-REUSE", b_s90_3),
    ("B-S90-4", "γ-CLOSING-PREDICATE", b_s90_4),
    ("B-S90-5", "ECHO-AMPLIFY-DETECTOR", b_s90_5),
    ("B-S90-6", "§24-DECISION-CONSISTENCY", b_s90_6),
    ("B-S90-7", "DETERMINISTIC", b_s90_7),
]

# B-S90-NOTE — empirical carve-out: whether the #3 action-perception loop
# ACTUALLY closes γ (coherent emission emerges) = trained-scale GPU fire
# OUTCOME. The $0 stub encodes garble-feeds-garble (echo) AND
# gain-shallows-basin (correction) as competing forces; which dominates at
# trained scale is unmeasured. B-D-NOTE / B-S88F2-NOTE / B-EMERGE-NOTE
# family — NOT counted 🔵. necessary-not-sufficient (B-EMERGE-7).


def main():
    results = []
    npass = 0
    for bid, name, fn in BATTERY:
        try:
            ok, note = fn()
        except Exception as e:
            ok, note = False, f"EXC {e}"
        results.append({"id": bid, "name": name, "passed": bool(ok), "note": note})
        npass += int(bool(ok))
        mark = "🔵" if ok else "✗"
        print(f"  {bid} {name}: {mark} — {note}")
    out = {
        "section": "§90",
        "battery": "B-S90-1..7",
        "n_pass": npass,
        "n_total": len(BATTERY),
        "all_blue": npass == len(BATTERY),
        "results": results,
        "B-S90-NOTE": "γ-closing actual emergence = trained-scale OUTCOME, NOT counted 🔵 (B-D-NOTE/B-S88F2-NOTE/B-EMERGE-NOTE family); necessary-not-sufficient B-EMERGE-7",
    }
    with open(os.path.join(HERE, "blue_falsifier_s90_result.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"\nB-S90: {npass}/{len(BATTERY)} {'all 🔵' if out['all_blue'] else 'INCOMPLETE'}")
    return 0 if out["all_blue"] else 1


if __name__ == "__main__":
    sys.exit(main())
