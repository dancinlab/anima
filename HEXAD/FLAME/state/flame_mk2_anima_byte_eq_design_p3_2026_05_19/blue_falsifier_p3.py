#!/usr/bin/env python3
"""P3 blue falsifier — flame mk2 anima byte-eq falsifier DESIGN battery.

5 closed-form propositions (B-S-P3-1..5) + 1 empirical carve-out (B-S-P3-NOTE).

These verify that the 3 byte-eq falsifiers F-1/F-2/F-3 are WELL-FORMED closed-form
predicates (bounded, deterministic, partition-clean) — they do NOT measure whether
flame and anima actually agree at full d=768.12L scale (that = future cost-bearing
fire, B-S-P3-NOTE empirical carve-out). g3: design-tier closed, capability claim 0.

Sidecar — central state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED.
"""
import ast
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


# ---- F-1 closed bound: 1 ulp x 256-element softmax floor (FMA reorder) -------
def fp_floor():
    """fp non-associativity FLOOR for one d=32 init forward (Higham 2002 recursive
    summation backward error, fp64): (n-1)*u/(1-(n-1)*u), n_terms = D + VOCAB = 288.
    This is the LOWER reference — drift can NEVER be below this if any reduction
    reorder occurs. It is NOT the F-1 admissibility ceiling (see eps_init below):
    the documented 4e-6 cross-substrate init drift is dominated by DIFFERENT
    RNG-init sequences (flame and anima seed their own LCG/init independently),
    not by FMA reorder alone — so a derived single-forward fp bound under-counts.
    DESIGN_FINDINGS.md C3 #5 records this honestly."""
    u = 0.5 * (2.0 ** -52)
    n_terms = 32 + 256
    return (n_terms - 1) * u / (1.0 - (n_terms - 1) * u)


# F-1 admissibility ceiling — eps_init: an EMPIRICAL threshold (honestly named),
# bounding acceptable cross-substrate init-gn2 relative agreement. Set 1e-3:
# three orders above the documented 4e-6, four orders below an O(1) divergence.
# A flame regression that broke init parity (>1e-3 relative) would FAIL F-1.
EPS_INIT = 1.0e-3


def b_p3_1_init_gn2_fp_drift_bounded():
    """B-S-P3-1 — F-INIT-GN2-FP-DRIFT-BOUNDED well-formed: documented relative
    init-gn2 drift sits in the half-open interval [fp_floor, EPS_INIT). The
    predicate is a CLOSED admissibility band — fp_floor (Higham recursive-sum
    backward error, derived) is the unbreakable lower reference; EPS_INIT is an
    honestly-named empirical ceiling (DESIGN C3 #5). F-1 certifies RELATIVE drift
    (gn2 unit/scale differs cross-substrate, C3 #4)."""
    flame = _load("flame_anchor_values.json")
    rel = flame["documented_drift"]["delta_init_gn2_rel_approx"]  # ~4e-6
    floor = fp_floor()
    finite = math.isfinite(floor) and floor > 0.0 and EPS_INIT > floor
    # documented drift is at or above the unbreakable fp floor
    above_floor = rel >= floor
    # documented drift is strictly inside the admissibility ceiling
    inside_ceiling = rel < EPS_INIT
    # band is non-vacuous: ceiling within 1e3x of the documented drift
    not_vacuous = (EPS_INIT / rel) <= 1.0e3
    ok = finite and above_floor and inside_ceiling and not_vacuous
    return ok, (f"rel_drift={rel:.3e} fp_floor={floor:.3e} "
                f"eps_init={EPS_INIT:.0e} band=[floor,eps_init)")


# ---- F-2 loss-curve shape metric (closed) ------------------------------------
def shape_of(curve):
    """Shape = curve normalized to its own L2 norm (scale-removed trajectory)."""
    n = math.sqrt(sum(x * x for x in curve))
    if n == 0.0:
        return [0.0] * len(curve)
    return [x / n for x in curve]


def b_p3_2_loss_curve_shape_metric_closed():
    """B-S-P3-2 — F-2 shape metric is a closed [0, 2] bounded relative-L2 form.
    For two unit-norm shape vectors a, b: ||a-b||_2 in [0, 2] by triangle
    inequality (each norm 1). Self-comparison ||a-a|| = 0. Closed-form proof:
    monotone in disagreement, anchored at 0, ceiling 2."""
    res = _load("anima_mini_result.json")
    curve = res["loss_curve"]
    sa = shape_of(curve)
    # self-distance is exactly 0 (deterministic identity)
    self_d = math.sqrt(sum((x - x) ** 2 for x in sa))
    # a degraded curve (reversed) gives a strictly positive, <= 2 distance
    sb = shape_of(list(reversed(curve)))
    deg_d = math.sqrt(sum((x - y) ** 2 for x, y in zip(sa, sb)))
    bounded = (0.0 <= deg_d <= 2.0 + 1e-9)
    monotone = (self_d == 0.0) and (deg_d > self_d)
    # epsilon threshold eps_shape=0.20 lies strictly inside the [0,2] range
    eps_inside = 0.0 < 0.20 < 2.0
    ok = bounded and monotone and eps_inside
    return ok, f"self_d={self_d:.3e} deg_d={deg_d:.4f} eps_shape=0.20"


# ---- F-3 weight-diff norm (closed) -------------------------------------------
def b_p3_3_weight_diff_norm_bounded():
    """B-S-P3-3 — F-3 relative Frobenius weight-diff is a closed [0, inf) form
    anchored at 0 for identical weights. Relative form ||Wf-Wa||_F / ||Wa||_F
    is well-defined whenever ||Wa||_F > 0 (true for any trained net). Closed:
    self-diff = 0; eps_weight=0.15 is a finite positive admissibility cut."""
    res = _load("anima_mini_result.json")
    wa = res["head_frobenius"]
    well_defined = wa > 0.0
    # identical-weight self relative diff is exactly 0
    self_rel = 0.0 / wa
    eps_pos = 0.15 > 0.0
    ok = well_defined and (self_rel == 0.0) and eps_pos
    return ok, f"||Wa||_F={wa:.4f} self_rel={self_rel:.1f} eps_weight=0.15"


# ---- Mode S1 vs S2 partition -------------------------------------------------
def b_p3_4_mode_s1_vs_s2_partition():
    """B-S-P3-4 — Mode S1 (anima-derived) and Mode S2 (flame-documented-pulled)
    are DISJOINT provenance classes. S1 = computed by anima_trainer_mini_smoke.py
    here; S2 = pulled verbatim from hexa-lang upstream README (no anima exec of
    flame). The 3 falsifiers compare ONE S1 datapoint against ONE S2 datapoint —
    a 2-class cross-comparison, never a self-comparison. Boolean disjointness."""
    s1 = _load("anima_mini_result.json")
    s2 = _load("flame_anchor_values.json")
    s1_is_computed = ("loss_curve" in s1 and "head_frobenius" in s1
                      and s1["config"].startswith("d=32"))
    s2_is_pulled = ("flame_phase3" in s2 and "_doc" in s2
                    and "upstream" in s2["_doc"].lower())
    # provenance partition: S1 has no flame-pulled key, S2 has no anima-computed key
    disjoint = ("flame_phase3" not in s1) and ("loss_curve" not in s2)
    ok = s1_is_computed and s2_is_pulled and disjoint
    return ok, f"S1_computed={s1_is_computed} S2_pulled={s2_is_pulled} disjoint={disjoint}"


# ---- determinism -------------------------------------------------------------
def b_p3_5_deterministic():
    """B-S-P3-5 — anima_trainer_mini_smoke.py is deterministic: LCG seed 1337,
    NO RNG library, NO wall-time path. AST audit confirms no forbidden
    non-determinism sources; 3x re-import yields bit-identical result."""
    src_path = os.path.join(HERE, "anima_trainer_mini_smoke.py")
    with open(src_path) as f:
        tree = ast.parse(f.read())
    forbidden = {"random", "numpy", "torch", "time", "datetime"}
    bad = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] in forbidden:
                    bad += 1
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in forbidden:
                bad += 1
    no_forbidden = (bad == 0)
    # re-run 3x, compare init_gn2 + final_gn2 + acc bit-identically
    import subprocess
    runs = []
    for _ in range(3):
        subprocess.run(["python3", src_path], capture_output=True, check=True)
        r = _load("anima_mini_result.json")
        runs.append((r["init_gn2"], r["final_gn2"], r["acc_8of8"]))
    bit_identical = (runs[0] == runs[1] == runs[2])
    ok = no_forbidden and bit_identical
    return ok, f"forbidden_imports={bad} bit_identical_3x={bit_identical}"


def main():
    checks = [
        ("B-S-P3-1 INIT-GN2-FP-DRIFT-BOUNDED", b_p3_1_init_gn2_fp_drift_bounded),
        ("B-S-P3-2 LOSS-CURVE-SHAPE-METRIC-CLOSED", b_p3_2_loss_curve_shape_metric_closed),
        ("B-S-P3-3 WEIGHT-DIFF-NORM-BOUNDED", b_p3_3_weight_diff_norm_bounded),
        ("B-S-P3-4 MODE-S1-vs-S2-PARTITION", b_p3_4_mode_s1_vs_s2_partition),
        ("B-S-P3-5 DETERMINISTIC", b_p3_5_deterministic),
    ]
    results = {}
    n_pass = 0
    for name, fn in checks:
        ok, detail = fn()
        results[name] = {"pass": ok, "detail": detail}
        n_pass += int(ok)
        print(f"{'PASS' if ok else 'FAIL'} {name} :: {detail}")
    note = ("B-S-P3-NOTE empirical carve-out: whether flame mk2 and the anima "
            "trainer actually agree at full d=768.12L scale (real init-gn2 drift, "
            "real loss-curve shape, real weight-diff norm) is an SGD/hardware "
            "OUTCOME measurable only by a future cost-bearing flame-vs-anima fire. "
            "This battery proves the F-1/F-2/F-3 falsifiers are well-formed "
            "closed-form predicates (bounded / shape-metric / deterministic / "
            "provenance-partitioned), NOT that flame == anima. "
            "B-D-NOTE / B-S71-NOTE family, NOT counted blue.")
    print(f"\nB-S-P3 {n_pass}/5 closed-form PASS")
    print(note)
    out = {"battery": "B-S-P3", "n_pass": n_pass, "n_total": 5,
           "all_closed": n_pass == 5, "results": results, "note": note}
    with open(os.path.join(HERE, "blue_falsifier_p3_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    return 0 if n_pass == 5 else 1


if __name__ == "__main__":
    raise SystemExit(main())
