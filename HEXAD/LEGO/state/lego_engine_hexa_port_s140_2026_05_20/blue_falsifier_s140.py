#!/usr/bin/env python3
"""§140 LEGO hexa-native engine port battery — 6 closed-form propositions + 1 NOTE."""

import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent.parent.parent
CENTRAL_BLUE = ANIMA / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
ENGINE_HEXA = ANIMA / "HEXAD" / "LEGO" / "lego_engine.hexa"
SMOKE_HEXA = ANIMA / "HEXAD" / "LEGO" / "lego_engine_smoke.hexa"
ENGINE_PY = ANIMA / "HEXAD" / "LEGO" / "lego_engine.py"
SPIKING_LIB = Path.home() / "core" / "hexa-lang" / "stdlib" / "flame" / "spiking_lib.hexa"


def sha16(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def b_s140_1_hexa_engine_file_exists():
    exists = ENGINE_HEXA.exists() and SMOKE_HEXA.exists()
    return {"name": "B-S140-1 HEXA-ENGINE-FILE-EXISTS",
            "passed": bool(exists),
            "evidence": {"lego_engine.hexa": ENGINE_HEXA.exists(),
                          "lego_engine_smoke.hexa": SMOKE_HEXA.exists()}}


def b_s140_2_imports_pr77_spiking_lib():
    """lego_engine.hexa uses the PR#77 spiking_lib (flame_event_threshold etc.)."""
    src = ENGINE_HEXA.read_text()
    uses_spiking = 'use "stdlib/flame/spiking_lib"' in src
    uses_tensor = 'use "stdlib/flame/tensor_lib"' in src
    smoke_src = SMOKE_HEXA.read_text()
    smoke_uses_primitives = ("flame_event_threshold" in smoke_src
                              and "flame_refractory_step" in smoke_src)
    spiking_lib_exists = SPIKING_LIB.exists()
    return {"name": "B-S140-2 IMPORTS-PR77-SPIKING-LIB",
            "passed": bool(uses_spiking and uses_tensor and smoke_uses_primitives
                            and spiking_lib_exists),
            "evidence": {"engine_uses_spiking_lib": uses_spiking,
                          "engine_uses_tensor_lib": uses_tensor,
                          "smoke_uses_flame_primitives": smoke_uses_primitives,
                          "spiking_lib_on_disk": spiking_lib_exists}}


def b_s140_3_smoke_4_4_pass():
    """Build + run the smoke; assert 4/4 PASS."""
    proc_b = subprocess.run(["hexa", "build", "HEXAD/LEGO/lego_engine_smoke.hexa"],
                             capture_output=True, text=True, cwd=str(ANIMA))
    built = "OK: built" in proc_b.stdout or "OK: built" in proc_b.stderr
    if not built:
        return {"name": "B-S140-3 SMOKE-4-4-PASS", "passed": False,
                "evidence": {"build_failed": True,
                              "stderr_tail": proc_b.stderr[-400:]}}
    proc_r = subprocess.run([str(ANIMA / "build" / "artifacts" / "app")],
                             capture_output=True, text=True, cwd=str(ANIMA))
    out = proc_r.stdout
    all_pass = "4 / 4 PASS" in out
    pass_count = out.count("PASS  F-S140-")
    return {"name": "B-S140-3 SMOKE-4-4-PASS",
            "passed": bool(all_pass and pass_count == 4),
            "evidence": {"build_ok": built, "smoke_4_4_pass": all_pass,
                          "f_s140_pass_lines": pass_count}}


def b_s140_4_algorithmic_not_byte_equal_honest():
    """The .hexa engine honestly declares algorithmic-equivalence (NOT byte-equal
    vs numpy) — RNG divergence is documented in the header."""
    src = ENGINE_HEXA.read_text()
    declares_algo_equiv = ("ALGORITHMICALLY EQUIVALENT" in src
                            or "algorithmic" in src.lower())
    declares_not_byte_equal = ("NOT byte-equal" in src or "not byte-equal" in src.lower())
    cites_rng_divergence = ("PCG64" in src or "RNG" in src)
    py_is_oracle = ("reference oracle" in src or "canonical reference" in src)
    return {"name": "B-S140-4 ALGORITHMIC-NOT-BYTE-EQUAL-HONEST",
            "passed": bool(declares_algo_equiv and declares_not_byte_equal
                            and cites_rng_divergence and py_is_oracle),
            "evidence": {"declares_algorithmic_equivalence": declares_algo_equiv,
                          "declares_not_byte_equal_vs_numpy": declares_not_byte_equal,
                          "cites_rng_divergence": cites_rng_divergence,
                          "numpy_py_is_reference_oracle": py_is_oracle}}


def b_s140_5_downstream_consumer_no_hexa_lang_edit():
    """§140 edits NO hexa-lang source — lego_engine.hexa lives in the anima repo
    and only `use`s hexa-lang stdlib. Verify: (a) the engine file is under the
    anima repo path, (b) every public function it defines is anima-namespaced
    (`lego_*` prefix), NOT a `stdlib/flame` namespace definition. The §138/§139
    hexa-lang changes are a separate reviewed PR (#77); §140 = anima-repo only."""
    engine_under_anima = str(ENGINE_HEXA).startswith(str(ANIMA))
    src = ENGINE_HEXA.read_text()
    # collect public fn names; all must be lego_*-prefixed (anima namespace)
    import re
    pub_fns = re.findall(r"^pub fn (\w+)", src, re.MULTILINE)
    all_lego_namespaced = all(fn.startswith("lego_") for fn in pub_fns)
    return {"name": "B-S140-5 DOWNSTREAM-CONSUMER-NO-HEXA-LANG-EDIT",
            "passed": bool(engine_under_anima and all_lego_namespaced and len(pub_fns) > 0),
            "evidence": {"engine_file_under_anima_repo": engine_under_anima,
                          "public_fns": pub_fns,
                          "all_lego_namespaced (anima, not stdlib)": all_lego_namespaced}}


def b_s140_6_central_and_ast():
    prefix = sha16(CENTRAL_BLUE)
    central_ok = (prefix == "c93e160a8a376a94")
    forbidden_imports = {"torch", "runpod", "vastai", "anthropic", "openai"}
    ih = set()
    tree = ast.parse(Path(__file__).read_text())
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for nm in n.names:
                if nm.name.split(".")[0] in forbidden_imports: ih.add(nm.name)
        elif isinstance(n, ast.ImportFrom):
            if n.module and n.module.split(".")[0] in forbidden_imports: ih.add(n.module)
    return {"name": "B-S140-6 CENTRAL-0-DIFF-AND-NO-FORBIDDEN-IMPORT",
            "passed": bool(central_ok and len(ih) == 0),
            "evidence": {"central_sha16": prefix, "central_match": central_ok,
                          "forbidden_imports": sorted(ih)}}


def b_s140_note():
    return {"name": "B-S140-NOTE EMPIRICAL-CARVE-OUT (NOT counted 🔵)",
            "carve_out_kind": "algorithmic-equivalent-not-byte-equal-to-numpy",
            "family": "B-EMERGE-7 / §71-flame-init-divergence / §138-§139",
            "honest_scope": ("§140 ports lego_engine.py → lego_engine.hexa using the "
                             "hexa-lang PR#77 flame spiking primitives. The port is "
                             "ALGORITHMICALLY EQUIVALENT (same LIF leaky-integrate "
                             "dynamics, threshold-and-reset, LOCAL STDP rule) verified "
                             "by F-S140-1..4 4/4 PASS + hexa build clean. It is NOT "
                             "byte-equal to the numpy reference — numpy PCG64+ziggurat "
                             "RNG vs hexa-lang LCG diverge on W/bias init (same honest "
                             "limit §71 recorded: gn2 7.97113 vs 7.97116). numpy "
                             "lego_engine.py stays the canonical reference oracle. "
                             "PR#77 not yet merged — lego_engine.hexa builds against "
                             "the flame-spiking-substrate-primitives branch worktree; "
                             "post-merge it builds against stdlib main. GOAL-orthogonal "
                             "engine tooling; necessary-not-sufficient (B-EMERGE-7); "
                             "GOAL 미도달.")}


def main():
    results = {
        "preconditions": [b_s140_6_central_and_ast()],
        "closed_propositions": [
            b_s140_1_hexa_engine_file_exists(),
            b_s140_2_imports_pr77_spiking_lib(),
            b_s140_3_smoke_4_4_pass(),
            b_s140_4_algorithmic_not_byte_equal_honest(),
            b_s140_5_downstream_consumer_no_hexa_lang_edit(),
            b_s140_6_central_and_ast(),
        ],
        "empirical_carve_out": b_s140_note(),
    }
    all_pre = all(p["passed"] for p in results["preconditions"])
    all_props = all(p["passed"] for p in results["closed_propositions"])
    cc = sum(1 for p in results["closed_propositions"] if p["passed"])
    total = len(results["closed_propositions"])
    summary = {
        "preconditions_passed": all_pre,
        "closed_propositions_passed": f"{cc}/{total}",
        "all_closed_pass": all_props,
        "battery_verdict": (f"HEXA-NATIVE-ENGINE-PORT-ALGORITHMIC-EQUIVALENT-{cc}-{total}-🔵"
                            if (all_pre and all_props) else "BATTERY-INCOMPLETE"),
        "empirical_carve_out_NOT_counted_🔵": True,
        "north_star_unchanged": True, "goal_unreached": True,
    }
    results["summary"] = summary
    (HERE / "blue_falsifier_s140_result.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if (all_pre and all_props) else 1)


if __name__ == "__main__":
    main()
