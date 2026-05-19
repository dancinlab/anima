#!/usr/bin/env python3
"""
§92 #3 ACTION-PERCEPTION AS TRAINING-TIME OBJECTIVE — closed-form sidecar
battery B-S92-1..7.

Sidecar — does NOT touch the central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py (0-line-diff mandate,
g_blue_closed_mandate).

g3: the battery proves the §92 design+stub is structurally honest — L_ap
closed-form ‖ψ−ψ_target‖² + §90 #3 Kolmogorov transfer carry, §11-B CE-base
preserved (L = L_CE + λ_ap·L_ap, NOT no-CE), training-time vs decode-time
mechanically distinct, §9 metric reuse, §88-F2 neoteny carry byte-equal, §91
echo-control reproduces, determinism.  It does NOT prove the training-time
L_ap objective closes γ at trained scale (B-S92-NOTE). necessary-not-sufficient
(B-EMERGE-7).
"""
import json
import sys
import os
import ast

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT = os.path.join(HERE, "result.json")
SMOKE = os.path.join(HERE, "ap_training_objective_smoke_s92.py")


def _load_result():
    with open(RESULT) as f:
        return json.load(f)


def _smoke_src():
    with open(SMOKE) as f:
        return f.read()


# ── B-S92-1 — L-AP-CLOSED-FORM ───────────────────────────────────────
# L_ap = ‖ψ(forward(S_encode(e_t))) − ψ_target‖² must be a closed-form
# squared deviation to the Ψ=½ vacuum (Law-71 fixed point), with the §89/§90
# #3 transfer x_{t+1}=S_encode(e_t) + Kolmogorov data-processing invariant.
# Verified structurally (formula + s_encode pure fn) + numerically (L_ap ≥ 0,
# L_ap = 0 iff ψ_heard == ψ_target).
def b_s92_1():
    src = _smoke_src()
    r = _load_result()
    cf = r.get("l_ap_closed_form", {})
    has_formula = "psi(forward(S_encode" in cf.get("formula", "")
    has_target = "1/2" in cf.get("psi_target", "") or "Psi=1/2" in cf.get("psi_target", "")
    transfer_ok = cf.get("transfer", "").startswith("x_{t+1}")
    invariant_ok = "K(" in cf.get("invariant", "") and "<=" in cf.get("invariant", "")
    has_fn = "def ap_consistency_loss" in src and "def s_encode" in src
    # numeric: L_ap >= 0 ∀ (squared deviation); L_ap = 0 only at the vacuum.
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location("s92_smoke_b1", SMOKE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    # a fully-clean coherent body -> emit_dev small -> ψ near vacuum -> L_ap small
    clean = "the quiet morning light moved across the floor "
    cascade = "a" * 56
    l_clean = m.ap_consistency_loss(clean)
    l_casc = m.ap_consistency_loss(cascade)
    nonneg = l_clean >= 0.0 and l_casc >= 0.0
    monotone = l_casc > l_clean   # more garble -> larger physics deviation
    passed = (has_formula and has_target and transfer_ok and invariant_ok
              and has_fn and nonneg and monotone)
    return passed, (f"formula={has_formula} target={has_target} transfer={transfer_ok} "
                    f"invariant={invariant_ok} fn={has_fn} L_ap>=0={nonneg} "
                    f"monotone(casc {l_casc:.5f}>clean {l_clean:.5f})={monotone}")


# ── B-S92-2 — §11-B-CE-BASE-PRESERVED (연결부위) ─────────────────────
# Total loss L = L_CE + λ_ap·L_ap — L_ap is an OVERLAY on the CE base, NOT
# a no-CE objective (§11-B PURE-PHYSICS measured DEGENERATE).  AST: the smoke
# must compute both ce_loss_proxy AND ap_consistency_loss and combine them;
# λ_ap must be a finite positive scalar.
def b_s92_2():
    src = _smoke_src()
    tree = ast.parse(src)
    has_ce = any(isinstance(n, ast.FunctionDef) and n.name == "ce_loss_proxy"
                 for n in ast.walk(tree))
    has_ap = any(isinstance(n, ast.FunctionDef) and n.name == "ap_consistency_loss"
                 for n in ast.walk(tree))
    # l_total = l_ce + LAMBDA_AP * l_ap  — additive CE-base composition
    has_total = "l_ce + LAMBDA_AP * l_ap" in src or "l_ce + LAMBDA_AP*l_ap" in src
    r = _load_result()
    lam = r.get("lambda_ap")
    lam_ok = isinstance(lam, (int, float)) and 0.0 < lam < 100.0
    # forbidden: a no-CE path (CE removed entirely)
    no_ce_removed = "ce_loss_proxy" in src  # CE proxy IS present -> CE-base
    passed = has_ce and has_ap and has_total and lam_ok and no_ce_removed
    return passed, (f"ce_fn={has_ce} ap_fn={has_ap} additive_total={has_total} "
                    f"lambda_ap={lam} in(0,100)={lam_ok} ce_base_present={no_ce_removed}")


# ── B-S92-3 — TRAINING-TIME-vs-DECODE-TIME-DISTINCT ──────────────────
# The §91→§92 core distinction: cell2 (training-time L_ap) and cell4
# (§91 decode-time mirror) must be MECHANICALLY distinct configs — cell2
# has l_ap=True decode_loop=False; cell4 has l_ap=False decode_loop=True.
# Boolean: their config tuples are disjoint on (l_ap, decode_loop).
def b_s92_3():
    r = _load_result()
    grid = {c["cell"]: c for c in r.get("grid_full", [])}
    c2 = grid.get("cell2_neoteny_l_ap", {}).get("config", {})
    c4 = grid.get("cell4_s91_decode_mirror", {}).get("config", {})
    if not c2 or not c4:
        return False, "cell2/cell4 config missing"
    # cell2 = training-time objective: l_ap ON, decode_loop OFF
    c2_training = (c2.get("l_ap") is True and c2.get("decode_loop") is False)
    # cell4 = §91 decode-time overlay: l_ap OFF, decode_loop ON
    c4_decode = (c4.get("l_ap") is False and c4.get("decode_loop") is True)
    # mechanically distinct: the (l_ap, decode_loop) tuples differ on BOTH axes
    distinct = (c2.get("l_ap") != c4.get("l_ap")
                and c2.get("decode_loop") != c4.get("decode_loop"))
    # the smoke must document that decode_corr does NOT enter produce_body
    src = _smoke_src()
    decode_not_in_body = "self_coherence_skill=skill" in src
    passed = c2_training and c4_decode and distinct and decode_not_in_body
    return passed, (f"cell2_training(l_ap,~decode)={c2_training} "
                    f"cell4_decode(~l_ap,decode)={c4_decode} tuples_distinct={distinct} "
                    f"decode_corr_excluded_from_body={decode_not_in_body}")


# ── B-S92-4 — §9-METRIC-REUSE ────────────────────────────────────────
# honest_coherent must be the §9 cascade-rate metric (4-clause: cascade_rate
# < 0.30, max_run < 10, len >= 20, printable >= 0.80). 4-corner witness.
def b_s92_4():
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location("s92_smoke_b4", SMOKE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    hc = getattr(m, "honest_coherent", None)
    if hc is None:
        return False, "honest_coherent fn absent"
    short = hc("abc")
    clean = hc("the quiet morning light moved slow")
    char_casc = hc("a" * 30)
    digit_casc = hc("55555555555555555555555")
    passed = (not short) and clean and (not char_casc) and (not digit_casc)
    return passed, (f"short={short} clean={clean} char_cascade={char_casc} "
                    f"digit_cascade={digit_casc}")


# ── B-S92-5 — NEOTENY-CARRY-BYTE-EQUAL (연결부위) ────────────────────
# §88-F2 trained-scale neoteny + baseline values must be carried byte-equal
# as the §92 design-anchor (NOT re-measured). Also psi_update must be the
# §90 smoke byte-equal Law-71 stub.
def b_s92_5():
    r = _load_result()
    carry = r.get("s88f2_carry", {})
    neo = carry.get("neoteny", {})
    base = carry.get("baseline", {})
    neo_ok = (abs(neo.get("maturity", 0) - 0.7478041127531916) < 1e-9
              and abs(neo.get("maj_frac", 0) - 0.35) < 1e-9
              and abs(neo.get("eff_D", 0) - 2.695751905441284) < 1e-9)
    base_ok = (abs(base.get("maturity", 0) - 0.9495988095306581) < 1e-9
               and abs(base.get("maj_frac", 0) - 0.8724999999999999) < 1e-9)
    # psi_update byte-equal to §90 smoke (connection-point): 0.30 stim coef,
    # 0.20 restoring coef toward PSI_VACUUM.
    src = _smoke_src()
    psi_eq = ("0.30 * stimulus_deviation" in src
              and "0.20 * (PSI_VACUUM - psi)" in src
              and "PSI_VACUUM = 0.5" in src)
    passed = neo_ok and base_ok and psi_eq
    return passed, (f"neoteny_carry_byte_equal={neo_ok} baseline_carry={base_ok} "
                    f"psi_update_byte_equal_s90={psi_eq}")


# ── B-S92-6 — §91-ECHO-CONTROL-REPRODUCES ────────────────────────────
# cell4 (§91 decode-time mirror) must reproduce §91 (β) ECHO-DOMINATES:
# the decode-time loop on a neoteny ckpt deepens the byte-cascade attractor
# (maj_frac rises strictly above its §88-F2 neoteny carry start of 0.35),
# AND it gets §9-WORSE than cell2 (training-time objective). Sanity control.
def b_s92_6():
    r = _load_result()
    fc = r.get("four_corner_verdict", {})
    mf = fc.get("maj_frac_final", {})
    cr = fc.get("coherence_rates", {})
    c4_maj = mf.get("cell4_s91_decode_mirror")
    c2_maj = mf.get("cell2_neoteny_l_ap")
    c4_coh = cr.get("cell4_s91_decode_mirror")
    c2_coh = cr.get("cell2_neoteny_l_ap")
    if None in (c4_maj, c2_maj, c4_coh, c2_coh):
        return False, "cell2/cell4 maj_frac or coherence missing"
    # §91 echo: cell4 decode-loop maj rises above the 0.35 neoteny start
    echo_reproduced = c4_maj > 0.35 + 1e-6
    # training-time objective (cell2) keeps the neoteny regime — maj at 0.35
    cell2_holds = abs(c2_maj - 0.35) < 1e-6
    # cell4 (decode) §9-WORSE-or-equal than cell2 (training-time)
    decode_not_better = c4_coh <= c2_coh
    passed = echo_reproduced and cell2_holds and decode_not_better
    return passed, (f"cell4_maj={c4_maj:.4f}>0.35(echo)={echo_reproduced} "
                    f"cell2_maj={c2_maj:.4f}~0.35(holds)={cell2_holds} "
                    f"cell4_coh={c4_coh}<=cell2_coh={c2_coh}={decode_not_better}")


# ── B-S92-7 — DETERMINISTIC ──────────────────────────────────────────
# The smoke must be a pure deterministic function of a seeded LCG. No
# unseeded RNG, no wall-time path. result.json records a fixed seed.
def b_s92_7():
    src = _smoke_src()
    r = _load_result()
    seed_recorded = r.get("seed")
    has_seed = seed_recorded is not None
    forbidden = ["random.random(", "random.randint(", "np.random",
                 "time.time(", "os.urandom", "datetime.now("]
    hits = [tok for tok in forbidden if tok in src]
    # re-run grid twice -> bit-identical (pure determinism)
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location("s92_smoke_b7", SMOKE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    import hashlib
    g1 = hashlib.sha256(json.dumps(m.run_grid(1337), sort_keys=True).encode()).hexdigest()
    g2 = hashlib.sha256(json.dumps(m.run_grid(1337), sort_keys=True).encode()).hexdigest()
    bit_identical = g1 == g2
    passed = has_seed and len(hits) == 0 and bit_identical
    return passed, (f"seed={seed_recorded} forbidden_rng_hits={hits} "
                    f"bit_identical={bit_identical}")


BATTERY = [
    ("B-S92-1", "L-AP-CLOSED-FORM", b_s92_1),
    ("B-S92-2", "§11-B-CE-BASE-PRESERVED", b_s92_2),
    ("B-S92-3", "TRAINING-TIME-vs-DECODE-TIME-DISTINCT", b_s92_3),
    ("B-S92-4", "§9-METRIC-REUSE", b_s92_4),
    ("B-S92-5", "NEOTENY-CARRY-BYTE-EQUAL", b_s92_5),
    ("B-S92-6", "§91-ECHO-CONTROL-REPRODUCES", b_s92_6),
    ("B-S92-7", "DETERMINISTIC", b_s92_7),
]

# B-S92-NOTE — empirical carve-out: whether the training-time L_ap objective
# ACTUALLY closes γ (coherent emission emerges) at trained scale = GPU fire
# OUTCOME, NOT counted 🔵. The $0 stub encodes L_ap-gradient-shapes-skill as
# a DESIGN hypothesis; the §1.1 data-regime / §88-trio collapse pattern means
# a training-time objective CAN still degenerate at trained scale (β corner
# risk carries). B-D-NOTE / B-S88F2-NOTE / B-S90-NOTE / B-S91-NOTE /
# B-EMERGE-NOTE family. necessary-not-sufficient (B-EMERGE-7).


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
        "section": "§92",
        "battery": "B-S92-1..7",
        "n_pass": npass,
        "n_total": len(BATTERY),
        "all_blue": npass == len(BATTERY),
        "results": results,
        "B-S92-NOTE": ("training-time L_ap actually closing γ = trained-scale "
                       "OUTCOME, NOT counted 🔵 (B-D-NOTE/B-S88F2-NOTE/"
                       "B-S90-NOTE/B-S91-NOTE/B-EMERGE-NOTE family); "
                       "necessary-not-sufficient B-EMERGE-7"),
    }
    with open(os.path.join(HERE, "blue_falsifier_s92_result.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"\nB-S92: {npass}/{len(BATTERY)} {'all 🔵' if out['all_blue'] else 'INCOMPLETE'}")
    return 0 if out["all_blue"] else 1


if __name__ == "__main__":
    sys.exit(main())
