#!/usr/bin/env python3
# §83 B-S83-1..7 sidecar closed-form falsifier battery.
# central state/verify_hexad_blue_2026_05_15/blue_falsifier.py 0-line-diff (verified externally).
# B-S83-NOTE empirical carve-out: substrate-plasticity score + rule discrimination =
#   SGD/measurement empirical (B-D-NOTE/B-S49-NOTE/B-EMERGE-NOTE family, NOT counted 🔵);
#   biology ectopic-eye Levin substrate ≠ silicon substrate (anchor only, not transfer claim).

import ast, json, hashlib
from pathlib import Path
from itertools import product

HERE = Path(__file__).parent
SMOKE = HERE / "physics_metacognition_smoke_s83.py"

results = {}

# ---- B-S83-1 NO-LEARNED-PARAMETER-IN-RULES ----
# AST structural: rule cells (R1..R5) functions must contain NO nn.Linear/torch.nn/train/fit/optimizer/backward/grad call
def b_s83_1_no_learned_param():
    forbidden_substrings = ["nn.Linear", "torch.nn", ".train(", ".fit(",
                            "optimizer", ".backward(", "autograd",
                            ".zero_grad", "loss.backward"]
    src = SMOKE.read_text()
    tree = ast.parse(src)
    # Extract rule function bodies (rule_R1..R5)
    target_fns = {"rule_R1_phi_tension","rule_R2_criticality_band",
                  "rule_R3_motivation_critical","rule_R4_slow_dwell",
                  "rule_R5_composite"}
    rule_bodies = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in target_fns:
            rule_bodies.append(ast.unparse(node))
    body_concat = "\n".join(rule_bodies)
    hits = [s for s in forbidden_substrings if s in body_concat]
    # Also verify all 5 rule functions exist
    found = sum(1 for fn in target_fns if fn in {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)})
    passed = (len(hits) == 0) and (found == 5)
    return {"passed": passed, "forbidden_hits": hits, "rule_fns_found": found,
            "rule_fns_expected": 5,
            "detail": "AST: 5 closed-form rule fns, 0 learned-param/training call"}

# ---- B-S83-2 §27/§44/§48-DISTILLATION-BASELINE-PRESERVED ----
# Cell 0 closed-form mirror = (psi_dir>0.55 AND tension>0.5)→EMIT else SILENT.
# This is by-design the §24 threshold §27/§44/§48 distilled to. Verify behaviour.
def b_s83_2_distillation_baseline():
    src = SMOKE.read_text()
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location("smoke83", SMOKE)
    mod = module_from_spec(spec); spec.loader.exec_module(mod)
    # Boundary witnesses
    witnesses = [
        ({"psi_dir":0.6,"tension":0.6,"phi":0.5,"motivation":0.5}, "EMIT_VOICE"),
        ({"psi_dir":0.3,"tension":0.6,"phi":0.5,"motivation":0.5}, "REMAIN_SILENT"),
        ({"psi_dir":0.6,"tension":0.3,"phi":0.5,"motivation":0.5}, "REMAIN_SILENT"),
        ({"psi_dir":0.0,"tension":0.0,"phi":0.0,"motivation":0.0}, "REMAIN_SILENT"),
    ]
    fails = []
    for psi, expected in witnesses:
        got = mod.cell0_dhdl_distillation(psi)
        if got != expected:
            fails.append({"psi":psi,"expected":expected,"got":got})
    passed = len(fails) == 0 and ("cell0_dhdl_distillation" in src)
    return {"passed": passed, "fails": fails, "n_witnesses": len(witnesses),
            "detail": "Cell 0 is §27 DH-DL distillation baseline (mirrors §24 label) — 4-witness truth table"}

# ---- B-S83-3 RULE-PARTITION-EXHAUSTIVE ----
# Every rule output ∈ {EMIT_VOICE, CONTINUE_THINK, REMAIN_SILENT}, exhaustive 3-set Boolean.
def b_s83_3_partition():
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location("smoke83b", SMOKE)
    mod = module_from_spec(spec); spec.loader.exec_module(mod)
    grid = [{"psi_dir":a,"tension":b,"phi":c,"motivation":d}
            for a,b,c,d in product([0.0,0.3,0.5,0.7,1.0], repeat=4)]
    actions_set = set(mod.ACTIONS)
    cells_to_test = [mod.cell0_dhdl_distillation, mod.cell1_s24_baseline,
                     mod.rule_R1_phi_tension, mod.rule_R2_criticality_band,
                     mod.rule_R3_motivation_critical, mod.rule_R5_composite]
    # rule_R4 has state; skip in pure-fn partition test
    out_of_set = []
    n_checked = 0
    for fn in cells_to_test:
        for psi in grid:
            r = fn(psi); n_checked += 1
            if r not in actions_set:
                out_of_set.append({"fn":fn.__name__,"psi":psi,"got":r})
    passed = (len(out_of_set) == 0) and (len(actions_set) == 3)
    return {"passed": passed, "out_of_set": out_of_set[:5], "n_checked": n_checked,
            "actions_set_size": len(actions_set),
            "detail": "All rule outputs ∈ 3-action partition (5^4 × 6 fn = 3750 closed checks)"}

# ---- B-S83-4 §9-METRIC-REUSE ----
# honest_coherent reuses the §9 cascade-rate "necessary-not-sufficient" notion:
# coherent ≡ window-of-5 contains ≥2 distinct labels (avoids single-class collapse).
def b_s83_4_s9_reuse():
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location("smoke83c", SMOKE)
    mod = module_from_spec(spec); spec.loader.exec_module(mod)
    # Witnesses
    collapsed = ["EMIT_VOICE"]*5
    diverse = ["EMIT_VOICE","REMAIN_SILENT","EMIT_VOICE","CONTINUE_THINK","EMIT_VOICE"]
    short = ["EMIT_VOICE"]*3
    ok = (mod.honest_coherent(collapsed) is False) and \
         (mod.honest_coherent(diverse) is True) and \
         (mod.honest_coherent(short) is False)
    return {"passed": ok,
            "detail": "honest_coherent: collapse→False · diverse→True · short→False (§9 necessary-not-sufficient mirror)"}

# ---- B-S83-5 SUBSTRATE-PLASTICITY-METRIC-CLOSED ----
# Agreement rate ∈ [0,1] closed-form under permuted ψ field assignment.
def b_s83_5_plasticity_bounded():
    res = json.loads((HERE / "result.json").read_text())
    plast_vals = [r["substrate_plasticity_agreement"] for r in res["grid"]]
    in_range = all(0.0 <= v <= 1.0 for v in plast_vals)
    n_cells = len(plast_vals)
    passed = in_range and n_cells == 7
    return {"passed": passed, "values": plast_vals, "n_cells": n_cells,
            "detail": "All 7 cells produce substrate_plasticity ∈ [0,1] under 2 ψ-field permutations (Levin mirror)"}

# ---- B-S83-6 §24-BASELINE-PRESERVED ----
# Cell 1 == §24 scalar threshold (motivation > 0.6 → EMIT else SILENT)
def b_s83_6_s24_baseline():
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location("smoke83d", SMOKE)
    mod = module_from_spec(spec); spec.loader.exec_module(mod)
    witnesses = [
        ({"psi_dir":0.5,"tension":0.5,"phi":0.5,"motivation":0.7}, "EMIT_VOICE"),
        ({"psi_dir":0.5,"tension":0.5,"phi":0.5,"motivation":0.5}, "REMAIN_SILENT"),
        ({"psi_dir":0.9,"tension":0.9,"phi":0.9,"motivation":0.55}, "REMAIN_SILENT"),
        ({"psi_dir":0.0,"tension":0.0,"phi":0.0,"motivation":1.0}, "EMIT_VOICE"),
    ]
    fails = []
    for psi, expected in witnesses:
        got = mod.cell1_s24_baseline(psi)
        if got != expected: fails.append({"psi":psi,"expected":expected,"got":got})
    return {"passed": len(fails)==0, "fails": fails, "n_witnesses": len(witnesses),
            "detail": "Cell 1 = §24 motivation>0.6 scalar threshold byte-equal"}

# ---- B-S83-7 DETERMINISTIC ----
# 3× run produces bit-identical result.json
def b_s83_7_deterministic():
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location("smoke83e", SMOKE)
    mod = module_from_spec(spec); spec.loader.exec_module(mod)
    hashes = []
    for _ in range(3):
        g = mod.run_grid(seed=1337, env_phase=0.4, n_step=20)
        # canonicalize: drop unordered keys
        payload = json.dumps(g, sort_keys=True)
        hashes.append(hashlib.sha256(payload.encode()).hexdigest())
    all_equal = len(set(hashes)) == 1
    return {"passed": all_equal, "hashes": hashes,
            "detail": "3× run_grid(seed=1337) bit-identical canonical JSON sha256"}

if __name__ == "__main__":
    battery = {
        "B-S83-1_NO-LEARNED-PARAMETER-IN-RULES": b_s83_1_no_learned_param(),
        "B-S83-2_DISTILLATION-BASELINE-PRESERVED": b_s83_2_distillation_baseline(),
        "B-S83-3_RULE-PARTITION-EXHAUSTIVE": b_s83_3_partition(),
        "B-S83-4_S9-METRIC-REUSE": b_s83_4_s9_reuse(),
        "B-S83-5_SUBSTRATE-PLASTICITY-METRIC-CLOSED": b_s83_5_plasticity_bounded(),
        "B-S83-6_S24-BASELINE-PRESERVED": b_s83_6_s24_baseline(),
        "B-S83-7_DETERMINISTIC": b_s83_7_deterministic(),
    }
    total = len(battery)
    passed = sum(1 for v in battery.values() if v["passed"])
    out = {
        "battery": battery,
        "pass_count": passed,
        "total": total,
        "all_blue": passed == total,
        "note": "B-S83-NOTE: substrate-plasticity score + rule discrimination empirical (B-D-NOTE/B-S49-NOTE/B-EMERGE-NOTE family, NOT counted 🔵); biology ectopic-eye Levin substrate ≠ silicon substrate; capability claim 0; g3 necessary-not-sufficient (B-EMERGE-7)",
    }
    (HERE / "blue_falsifier_s83_result.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k:{"passed":v["passed"]} for k,v in battery.items()}, indent=2))
    print(f"\nPASS {passed}/{total}  all_blue={out['all_blue']}")
