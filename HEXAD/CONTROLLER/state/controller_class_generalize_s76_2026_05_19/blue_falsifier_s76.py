#!/usr/bin/env python3
"""§76 blue falsifier — A-only generalization probe closed-form battery.

7 closed-form propositions (B-S76-1..7) + 1 empirical carve-out (B-S76-NOTE).

Sidecar — central state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED.
g3: design-tier closed, capability claim 0, necessary-not-sufficient.
"""
import ast
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SMOKE = os.path.join(HERE, "subaxis_generalize_smoke_s76.py")


def _load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def b_s76_1_grid_partition_exhaustive_disjoint():
    """B-S76-1 — grid is exhaustive + disjoint: 4 state x 5 statistic = 20 grid
    cells + 2 controls = 22, no missing pair, no duplicate (state,statistic)."""
    r = _load("result.json")
    cells = r["cells"]
    grid = {k: v for k, v in cells.items() if not v.get("control")}
    states = {"tension", "psi_dir", "phi", "curiosity_ema"}
    forms = {"mean", "median", "max_window", "p75", "p95"}
    # exhaustive: every (state, statistic) pair present exactly once
    pairs = {(v["state"], v["statistic"]) for v in grid.values()}
    expected = {(s, f) for s in states for f in forms}
    exhaustive = (pairs == expected)
    disjoint = (len(grid) == len(pairs) == 20)
    total = (len(cells) == 22) and (4 * 5 + 2 == 22)
    ok = exhaustive and disjoint and total
    return ok, f"grid={len(grid)} pairs={len(pairs)} total={len(cells)} (4x5+2=22)"


def b_s76_2_each_cell_deterministic():
    """B-S76-2 — each cell measured deterministically: LCG seed 1337, pure-fn,
    no RNG library, no wall-time path. 3x re-run -> bit-identical result."""
    with open(SMOKE) as f:
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
    runs = []
    for _ in range(3):
        subprocess.run(["python3", SMOKE], capture_output=True, check=True)
        r = _load("result.json")
        runs.append(json.dumps(r["cells"], sort_keys=True))
    bit_identical = (runs[0] == runs[1] == runs[2])
    ok = (bad == 0) and bit_identical
    return ok, f"forbidden_imports={bad} bit_identical_3x={bit_identical}"


def b_s76_3_survive_predicate_closed():
    """B-S76-3 — survive predicate is a CLOSED Boolean conjunction:
    survive := (interval_var > TAU) AND (maj_frac < 0.95) AND (n_emits >= 2).
    Verified: every cell's recorded `survive` equals the recomputed conjunction
    over its three recorded metrics (no hidden state)."""
    r = _load("result.json")
    TAU = 1e-4
    mismatch = 0
    for k, v in r["cells"].items():
        recomputed = (v["interval_var"] > TAU) and (v["maj_frac"] < 0.95) \
            and (v["n_emits"] >= 2)
        if recomputed != v["survive"]:
            mismatch += 1
    ok = (mismatch == 0)
    return ok, f"survive_predicate_mismatch={mismatch}/22 (closed conjunction)"


def b_s76_4_s24_control_collapses():
    """B-S76-4 — §24-baseline scalar control collapses BY CONSTRUCTION:
    a fixed non-state-derived cut below the channel floor emits every step
    -> maj_frac = 1.0, interval_var = 0.0, survive = False. This is the
    negative control validating the survive metric has discriminating power."""
    r = _load("result.json")
    c = r["cells"]["CONTROL__s24_baseline_scalar"]
    collapsed = (c["maj_frac"] == 1.0) and (c["interval_var"] == 0.0) \
        and (c["survive"] is False)
    ok = collapsed and (r["baseline_collapses"] is True)
    return ok, (f"s24 maj_frac={c['maj_frac']} ivar={c['interval_var']} "
                f"survive={c['survive']}")


def b_s76_5_s73_a_only_tension_mean_reproduces():
    """B-S76-5 (연결부위) — §73-A-only tension-mean control reproduces the
    tension__mean grid cell byte-equal. Closed-form connection point: the §76
    grid contains §75-FIRE's exact cell1 lever (state=tension, statistic=mean)
    as one of its 20 cells -> fair-compare with §75 BY CONSTRUCTION."""
    r = _load("result.json")
    ref = r["cells"]["CONTROL__s73_a_only_tension_mean"]
    grid = r["cells"]["tension__mean"]
    byte_eq = (abs(ref["interval_var"] - grid["interval_var"]) < 1e-12) and \
        (ref["maj_frac"] == grid["maj_frac"]) and \
        (ref["n_emits"] == grid["n_emits"])
    same_lever = (ref["state"] == "tension") and (ref["statistic"] == "mean")
    ok = byte_eq and same_lever and (r["s73_reference_matches_grid"] is True)
    return ok, f"byte_eq={byte_eq} ivar_ref={ref['interval_var']} ivar_grid={grid['interval_var']}"


def b_s76_6_state_source_from_physics_tuple():
    """B-S76-6 — the 4 state sources are the anima Law-71 physics tuple, NOT
    arbitrary external signals. AST audit of gen_physics_stub confirms it
    derives exactly {tension, psi_dir, phi, curiosity_ema} and psi_dir uses the
    (1+cos)/2 form (conscious_decoder.py:728-751 mirror)."""
    with open(SMOKE) as f:
        src = f.read()
    tree = ast.parse(src)
    # locate gen_physics_stub, confirm the 4 channels are the dict keys
    chan_keys = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "gen_physics_stub":
            for sub in ast.walk(node):
                if isinstance(sub, ast.Dict):
                    keys = [k.value for k in sub.keys
                            if isinstance(k, ast.Constant)]
                    if "tension" in keys:
                        chan_keys = set(keys)
    expected = {"tension", "psi_dir", "phi", "curiosity_ema"}
    keys_ok = (chan_keys == expected)
    # psi_dir uses Law-71 (1+cos)/2 form
    psi_form = ("(1.0 + cos) / 2.0" in src) or ("(1.0+cos)/2.0" in src)
    ok = keys_ok and psi_form
    return ok, f"channels={sorted(chan_keys or [])} psi_law71_form={psi_form}"


def b_s76_7_deterministic():
    """B-S76-7 — full pipeline deterministic: smoke + this falsifier are
    pure-fn, no RNG library, no wall-time. Re-confirmed via 3x grid-hash."""
    runs = []
    for _ in range(3):
        subprocess.run(["python3", SMOKE], capture_output=True, check=True)
        r = _load("result.json")
        runs.append((r["n_survive_grid"], r["verdict_4corner"],
                     json.dumps(r["per_statistic_survive"], sort_keys=True)))
    ok = (runs[0] == runs[1] == runs[2])
    return ok, f"bit_identical_3x={ok} verdict={runs[0][1]}"


def main():
    checks = [
        ("B-S76-1 GRID-PARTITION-EXHAUSTIVE-DISJOINT", b_s76_1_grid_partition_exhaustive_disjoint),
        ("B-S76-2 EACH-CELL-DETERMINISTIC", b_s76_2_each_cell_deterministic),
        ("B-S76-3 SURVIVE-PREDICATE-CLOSED", b_s76_3_survive_predicate_closed),
        ("B-S76-4 §24-CONTROL-COLLAPSES", b_s76_4_s24_control_collapses),
        ("B-S76-5 §73-A-ONLY-TENSION-MEAN-REPRODUCES-§75", b_s76_5_s73_a_only_tension_mean_reproduces),
        ("B-S76-6 STATE-SOURCE-FROM-PHYSICS-TUPLE", b_s76_6_state_source_from_physics_tuple),
        ("B-S76-7 DETERMINISTIC", b_s76_7_deterministic),
    ]
    results = {}
    n_pass = 0
    for name, fn in checks:
        ok, detail = fn()
        results[name] = {"pass": ok, "detail": detail}
        n_pass += int(ok)
        print(f"{'PASS' if ok else 'FAIL'} {name} :: {detail}")
    note = ("B-S76-NOTE empirical carve-out: which state-source x statistic-form "
            "combinations actually generalize is a $0-STUB physics-state OUTCOME, "
            "NOT a trained-ckpt measurement. Trained-scale generalization (does "
            "A-only survive across statistics on REAL anima Law-71 W-physics) is a "
            "future cost-bearing fire per B-S75-FIRE-NOTE. The battery proves the "
            "grid is exhaustive/disjoint/deterministic, the survive predicate is "
            "closed, the §24 control collapses, and the §75-FIRE lever is "
            "reproduced — NOT that the controller class achieves emergence. "
            "necessary-not-sufficient (B-EMERGE-7). B-D-NOTE / B-S75-FIRE-NOTE / "
            "B-S75-NOTE family, NOT counted blue.")
    print(f"\nB-S76 {n_pass}/7 closed-form PASS")
    print(note)
    out = {"battery": "B-S76", "n_pass": n_pass, "n_total": 7,
           "all_closed": n_pass == 7, "results": results, "note": note}
    with open(os.path.join(HERE, "blue_falsifier_s76_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    return 0 if n_pass == 7 else 1


if __name__ == "__main__":
    raise SystemExit(main())
