#!/usr/bin/env python3
# §87-F2 B-S87F2-1..6 sidecar closed-form falsifier battery.
# central state/verify_hexad_blue_2026_05_15/blue_falsifier.py = 0-line-diff
# (sidecar only; B-S77/B-S81/B-S82/B-S83/B-S83-NOTE selrege).
#
# Proves the neoteny anti-saturation MECHANISM is honest:
#   maturity/neoteny metric well-formed, NK partition distinct, anti-
#   saturation monotone, §16.6-C + §11-B connection points closed,
#   deterministic.
#
# B-S87F2-NOTE empirical carve-out: whether neoteny anti-saturation
# actually breaks the §16.6-C ceiling = trained-scale GPU fire OUTCOME,
# NOT counted 🔵 (B-D-NOTE/B-SCALE-NOTE/B-EMERGE-NOTE family).
# axolotl neoteny biology = honest direction-anchor, NOT transfer claim.

import ast, json, hashlib
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

import sympy as sp

HERE = Path(__file__).parent
SMOKE = HERE / "axolotl_neoteny_smoke_s87f2.py"


def _load():
    spec = spec_from_file_location("smoke87f2", SMOKE)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- B-S87F2-1 MATURITY-PROXY-BOUNDED ---------------------------------
# maturity = W_CE*m1 + W_MAJ*m2 + W_D*m3 with each m_i in [0,1] and
# weights non-negative summing to 1 => maturity in [0,1] (convex
# combination, sympy). neoteny N = 1 - maturity => N in [0,1].
def b1_maturity_proxy_bounded():
    mod = _load()
    w_ce, w_maj, w_d = mod.W_CE, mod.W_MAJ, mod.W_D
    weights_nonneg = w_ce >= 0 and w_maj >= 0 and w_d >= 0
    weights_sum1 = abs((w_ce + w_maj + w_d) - 1.0) < 1e-9
    # sympy: convex combination of [0,1] variables is bounded to [0,1]
    m1, m2, m3 = sp.symbols("m1 m2 m3", nonnegative=True)
    maturity = sp.Rational(int(round(w_ce * 1e6)), 1000000) * m1 \
        + sp.Rational(int(round(w_maj * 1e6)), 1000000) * m2 \
        + sp.Rational(int(round(w_d * 1e6)), 1000000) * m3
    # at corner (1,1,1) maturity == sum of weights == 1; at (0,0,0) == 0
    mat_max = maturity.subs({m1: 1, m2: 1, m3: 1})
    mat_min = maturity.subs({m1: 0, m2: 0, m3: 0})
    sym_bounded = (abs(float(mat_max) - 1.0) < 1e-9) and (float(mat_min) == 0.0)
    # numeric: every cell's neoteny in [0,1] and == 1 - maturity
    grid = mod.run_grid(seed=1337)
    numeric_ok = all(
        0.0 <= c["final_neoteny"] <= 1.0
        and 0.0 <= c["final_maturity"] <= 1.0
        and abs(c["final_neoteny"] - (1.0 - c["final_maturity"])) < 1e-9
        for c in grid)
    passed = weights_nonneg and weights_sum1 and sym_bounded and numeric_ok
    return {"passed": bool(passed), "weights_nonneg": weights_nonneg,
            "weights_sum1": weights_sum1, "sym_bounded": sym_bounded,
            "numeric_ok": numeric_ok,
            "detail": "maturity = convex combo of 3 proxies in [0,1] => [0,1]; "
                      "neoteny N = 1 - maturity in [0,1] (sympy corners + numeric)"}


# ---- B-S87F2-2 NK-MECHANISM-PARTITION ---------------------------------
# NK-1..4 each target a distinct maturity axis: NK-1 -> CE (M-1),
# NK-2 -> attractor depth maj (M-2), NK-3 -> D (M-3), NK-4 -> global
# maturation rate. The 3 single-NK cells produce pairwise-distinct final
# state signatures (no two NK collapse to the same effect).
def b2_nk_mechanism_partition():
    mod = _load()
    grid = {c["cell"]: c for c in mod.run_grid(seed=1337)}
    c1 = grid["cell1_floor_clamps"]   # NK-1 + NK-3
    c2 = grid["cell2_reinjection"]    # NK-2
    c3 = grid["cell3_metamorph_block"]  # NK-4
    c0 = grid["cell0_baseline"]
    # signature per single-NK axis
    sig1 = (round(c1["final_ce"], 4), round(c1["final_D"], 4))         # CE+D axis
    sig2 = (round(c2["final_maj_frac"], 4), round(c2["final_D"], 4))   # maj axis
    sig3 = (c3["saturation_delay_step"], round(c3["final_maturity"], 4))
    pairwise_distinct = len({str(sig1), str(sig2), str(sig3)}) == 3
    # each NK cell must differ from baseline (NK actually does something)
    differ_from_base = all(
        abs(c["final_maturity"] - c0["final_maturity"]) > 1e-6
        for c in (c1, c2, c3))
    # AST: 4 NK branches structurally present in step_trajectory
    src = SMOKE.read_text()
    tree = ast.parse(src)
    step_fn = next((n for n in ast.walk(tree)
                    if isinstance(n, ast.FunctionDef)
                    and n.name == "step_trajectory"), None)
    step_src = ast.unparse(step_fn) if step_fn else ""
    nk_branches = all(t in step_src for t in ("nk1", "nk2", "nk3", "nk4"))
    passed = pairwise_distinct and differ_from_base and nk_branches
    return {"passed": bool(passed), "pairwise_distinct": pairwise_distinct,
            "differ_from_base": differ_from_base, "nk_branches_present": nk_branches,
            "sig1": str(sig1), "sig2": str(sig2), "sig3": str(sig3),
            "detail": "NK-1..4 target distinct maturity axes; 3 single-NK cells "
                      "pairwise-distinct signatures; all differ from baseline"}


# ---- B-S87F2-3 ANTI-SATURATION-MONOTONE -------------------------------
# Turning a neoteny mechanism ON delays/reduces maturation: full-neoteny
# cell keeps maturity <= baseline (monotone non-increasing in neoteny-set),
# and saturation_delay_step non-decreasing. sympy: with NK-1 clamp
# CE >= THETA_FLOOR > CE_NATURAL_FLOOR => m1 strictly < 1 => maturity
# strictly below the unclamped maximum.
def b3_anti_saturation_monotone():
    mod = _load()
    grid = {c["cell"]: c for c in mod.run_grid(seed=1337)}
    c0 = grid["cell0_baseline"]
    c4 = grid["cell4_full_neoteny"]
    # numeric monotone: full neoteny lowers maturity, raises delay
    maturity_monotone = c4["final_maturity"] <= c0["final_maturity"]
    delay_monotone = c4["saturation_delay_step"] >= c0["saturation_delay_step"]
    neoteny_higher = c4["final_neoteny"] >= c0["final_neoteny"]
    # sympy: NK-1 clamp forces ce >= THETA_FLOOR; m1 = 1 - (ce-floor)/(init-floor)
    ce, floor, init, theta = sp.symbols("ce floor init theta", positive=True)
    m1 = 1 - (ce - floor) / (init - floor)
    # dm1/dce < 0 (maturity proxy strictly decreasing in ce) => clamping ce
    # UP strictly lowers m1 vs the unclamped (ce->floor) maximum
    dm1 = sp.diff(m1, ce)
    # dm1 simplifies to -1/(init-floor) < 0 for init > floor
    dm1_negative = sp.simplify(dm1 - (-1 / (init - floor))) == 0
    # m1 at ce=THETA_FLOOR strictly less than m1 at ce=floor (=1)
    m1_floor = m1.subs(ce, floor)               # = 1
    m1_theta = m1.subs({ce: mod.THETA_FLOOR, floor: mod.CE_NATURAL_FLOOR,
                        init: mod.CE_INIT})
    clamp_lowers = float(m1_theta) < float(m1_floor.subs({floor: 0, init: 1}))
    passed = (maturity_monotone and delay_monotone and neoteny_higher
              and dm1_negative and clamp_lowers)
    return {"passed": bool(passed), "maturity_monotone": maturity_monotone,
            "delay_monotone": delay_monotone, "neoteny_higher": neoteny_higher,
            "dm1_negative": bool(dm1_negative), "clamp_lowers_m1": bool(clamp_lowers),
            "baseline_maturity": c0["final_maturity"],
            "full_neoteny_maturity": c4["final_maturity"],
            "detail": "neoteny ON => maturity non-increasing + delay non-decreasing "
                      "(numeric); NK-1 CE-clamp strictly lowers m1 (sympy dm1/dce<0)"}


# ---- B-S87F2-4 S16-6C-CONNECTION (연결부위) ----------------------------
# neoteny is the DIRECT anti-mechanism of §16.6-C memorization-saturation.
# Connection point: the baseline cell DOES saturate (maturity over the
# SAT_TRIGGER, byte-cascade attractor maj_frac near 1.0, D collapsed near
# the §84 anchor) — i.e. it reproduces the §16.6-C diagnosis — and the
# neoteny mechanism reduces exactly those quantities. Structural.
def b4_s16_6c_connection():
    mod = _load()
    grid = {c["cell"]: c for c in mod.run_grid(seed=1337)}
    c0 = grid["cell0_baseline"]
    c4 = grid["cell4_full_neoteny"]
    # baseline reproduces §16.6-C saturation: high maturity, deep basin, low D
    baseline_saturates = (c0["final_maturity"] > mod.SAT_TRIGGER
                          and c0["final_maj_frac"] > 0.90
                          and c0["final_D"] < mod.D_NATURAL_FLOOR + 0.5)
    # CE floor stub anchored to the §16 trained-saturated value
    ce_floor_anchored = abs(mod.CE_NATURAL_FLOOR - 0.0045) < 1e-9
    # neoteny reduces every §16.6-C saturation quantity
    neoteny_reduces = (c4["final_maturity"] < c0["final_maturity"]
                       and c4["final_maj_frac"] < c0["final_maj_frac"]
                       and c4["final_D"] > c0["final_D"])
    # structural: maturity_score reads ce + maj + D (the 3 §16.6-C proxies)
    src = SMOKE.read_text()
    tree = ast.parse(src)
    mat_fn = next((n for n in ast.walk(tree)
                   if isinstance(n, ast.FunctionDef)
                   and n.name == "maturity_score"), None)
    mat_src = ast.unparse(mat_fn) if mat_fn else ""
    reads_three_proxies = all(t in mat_src for t in ("ce", "maj", "D"))
    passed = (baseline_saturates and ce_floor_anchored
              and neoteny_reduces and reads_three_proxies)
    return {"passed": bool(passed), "baseline_saturates": baseline_saturates,
            "ce_floor_anchored_to_s16": ce_floor_anchored,
            "neoteny_reduces_saturation": neoteny_reduces,
            "reads_three_s16_6c_proxies": reads_three_proxies,
            "detail": "connection point: baseline reproduces §16.6-C saturation "
                      "(maturity>trigger, maj~1, D collapsed); neoteny reduces "
                      "all three; maturity_score reads the §16.6-C proxy triple"}


# ---- B-S87F2-5 S11-B-CE-BASE-PRESERVED (연결부위) ----------------------
# §11-B measured: anima physics alone (no-CE) is degenerate => the NK
# mechanisms are CE-BASE OVERLAYS, not physics-only replacements. The
# saturation trajectory is built on a CE-descent curve; NK-1 clamps the CE
# floor (it does not remove CE); NK-2/3/4 modulate around the CE curve.
# AST/structural: CE is a first-class trajectory variable and is never
# zeroed/removed.
def b5_s11b_ce_base_preserved():
    src = SMOKE.read_text()
    tree = ast.parse(src)
    step_fn = next((n for n in ast.walk(tree)
                    if isinstance(n, ast.FunctionDef)
                    and n.name == "step_trajectory"), None)
    step_src = ast.unparse(step_fn) if step_fn else ""
    # CE descent toward a floor is present (CE_NATURAL_FLOOR + descent term)
    ce_descent_present = "CE_NATURAL_FLOOR" in step_src and "prev_ce" in step_src
    # NK-1 clamps CE to THETA_FLOOR (overlay) — does NOT delete CE
    nk1_clamps_not_removes = "ce = THETA_FLOOR" in step_src
    # forbidden: no path that sets CE to 0 / removes CE term entirely
    forbidden = ["ce = 0.0", "ce = 0\n", "del ce", "ce = None"]
    no_ce_removal = not any(f in step_src for f in forbidden)
    # maturity_score's m1 proxy is the CE-floor-proximity term (CE load-bearing)
    mod = _load()
    grid = mod.run_grid(seed=1337)
    # cell0 baseline final CE is a small-but-positive descended value (CE active)
    ce_active = all(c["final_ce"] > 0.0 for c in grid)
    passed = (ce_descent_present and nk1_clamps_not_removes
              and no_ce_removal and ce_active)
    return {"passed": bool(passed), "ce_descent_present": ce_descent_present,
            "nk1_clamps_not_removes": nk1_clamps_not_removes,
            "no_ce_removal_path": no_ce_removal, "ce_active_all_cells": ce_active,
            "detail": "§11-B precedence: NK are CE-BASE overlays (clamp/modulate "
                      "the CE curve), NOT no-CE physics-only — CE is a load-bearing "
                      "trajectory variable, never zeroed/removed (AST)"}


# ---- B-S87F2-6 DETERMINISTIC ------------------------------------------
# run_grid(seed=1337) bit-identical across 3 invocations (LCG, no RNG
# library, no wall-time-dependent path).
def b6_deterministic():
    mod = _load()
    hashes = []
    for _ in range(3):
        g = mod.run_grid(seed=1337)
        hashes.append(hashlib.sha256(
            json.dumps(g, sort_keys=True).encode()).hexdigest())
    # AST: no forbidden non-determinism source
    src = SMOKE.read_text()
    forbidden = ["import random", "random.", "time.time", "np.random",
                 "datetime.now", "os.urandom"]
    no_forbidden = not any(f in src for f in forbidden)
    all_equal = len(set(hashes)) == 1
    passed = all_equal and no_forbidden
    return {"passed": bool(passed), "all_equal": all_equal,
            "no_forbidden_rng": no_forbidden, "hashes": hashes,
            "detail": "3x run_grid(seed=1337) bit-identical canonical JSON; "
                      "LCG only, no random/time/urandom (AST)"}


if __name__ == "__main__":
    battery = {
        "B-S87F2-1_MATURITY-PROXY-BOUNDED": b1_maturity_proxy_bounded(),
        "B-S87F2-2_NK-MECHANISM-PARTITION": b2_nk_mechanism_partition(),
        "B-S87F2-3_ANTI-SATURATION-MONOTONE": b3_anti_saturation_monotone(),
        "B-S87F2-4_S16-6C-CONNECTION": b4_s16_6c_connection(),
        "B-S87F2-5_S11-B-CE-BASE-PRESERVED": b5_s11b_ce_base_preserved(),
        "B-S87F2-6_DETERMINISTIC": b6_deterministic(),
    }
    total = len(battery)
    passed = sum(1 for v in battery.values() if v["passed"])
    out = {
        "battery": battery,
        "pass_count": passed,
        "total": total,
        "all_blue": passed == total,
        "note": ("B-S87F2-NOTE: whether neoteny anti-saturation actually "
                 "breaks the §16.6-C ceiling = trained-scale GPU fire OUTCOME, "
                 "NOT counted 🔵 (B-D-NOTE/B-SCALE-NOTE/B-EMERGE-NOTE family). "
                 "$0 stub saturation trajectory != trained ckpt. axolotl "
                 "neoteny = honest direction-anchor, NOT capability proof. g3 "
                 "necessary-not-sufficient (B-EMERGE-7); amphibian-biology USE "
                 "!= GOAL emergence. central blue_falsifier.py 0-line-diff "
                 "(sidecar only)."),
    }
    (HERE / "blue_falsifier_s87f2_result.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k: {"passed": v["passed"]} for k, v in battery.items()},
                     indent=2))
    print(f"\nPASS {passed}/{total}  all_blue={out['all_blue']}")
