#!/usr/bin/env python3
"""§141 LEGO GPU spiking primitive design battery — 5 closed-form props + 1 NOTE."""

import ast
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent.parent.parent
CENTRAL_BLUE = ANIMA / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
DESIGN_MD = HERE / "DESIGN.md"
GPU_PATCH = Path.home() / "core" / "hexa-lang" / "inbox" / "patches" / "flame-stdp-pair-gpu-kernel.md"
CPU_PATCH = Path.home() / "core" / "hexa-lang" / "inbox" / "patches" / "flame-spiking-substrate-primitives.md"


def sha16(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def b_s141_1_gpu_primitive_is_device_kernel():
    """DESIGN.md asserts the GPU primitives are runtime_cuda.c device kernels,
    NOT pure-hexa stdlib like §138's CPU ones."""
    d = DESIGN_MD.read_text()
    device_kernel = "runtime_cuda.c" in d and "device" in d.lower()
    distinguishes_138 = "§138" in d and ("pure-hexa" in d or "stdlib" in d)
    return {"name": "B-S141-1 GPU-PRIMITIVE-IS-DEVICE-KERNEL-NOT-STDLIB",
            "passed": bool(device_kernel and distinguishes_138),
            "evidence": {"runtime_cuda_kernel_asserted": device_kernel,
                          "distinguishes_from_s138_stdlib": distinguishes_138}}


def b_s141_2_stdp_pair_is_on2():
    """DESIGN.md identifies flame_stdp_pair as the O(N²) primitive — the one
    that genuinely needs GPU; event/refractory are O(N)."""
    d = DESIGN_MD.read_text()
    on2 = "O(N²)" in d or "O(N^2)" in d or "N×N" in d
    on_named = "stdp_pair" in d.lower()
    on_others_cheap = "O(N)" in d
    return {"name": "B-S141-2 STDP-PAIR-IS-THE-O-N2-PRIMITIVE",
            "passed": bool(on2 and on_named and on_others_cheap),
            "evidence": {"o_n2_identified": on2, "stdp_pair_named": on_named,
                          "o_n_ops_noted_cheap": on_others_cheap}}


def b_s141_3_lego_gpu_fire_2_steps_away():
    """DESIGN.md honestly states a LEGO GPU fire is 2 upstream steps away,
    NOT fire-ready now."""
    d = DESIGN_MD.read_text()
    two_steps = "2 upstream steps" in d or "2-upstream-steps" in d or "2 upstream-steps" in d
    not_fire_ready = "NOT fire-ready" in d or "not fire-ready" in d.lower()
    fire_gate = "fire-gate" in d
    return {"name": "B-S141-3 LEGO-GPU-FIRE-IS-2-UPSTREAM-STEPS-AWAY",
            "passed": bool(two_steps and not_fire_ready and fire_gate),
            "evidence": {"two_upstream_steps_stated": two_steps,
                          "not_fire_ready_honest": not_fire_ready,
                          "fire_gate_discipline_cited": fire_gate}}


def b_s141_4_inbox_patch_filed():
    """The GPU inbox patch flame-stdp-pair-gpu-kernel.md exists, requests
    exactly flame_stdp_pair_gpu, flags runtime-kernel tier, has F-STDP-GPU
    falsifiers."""
    if not GPU_PATCH.exists():
        return {"name": "B-S141-4 INBOX-PATCH-PATH-HEXA-FIRST-COMPLIANT",
                "passed": False, "evidence": {"error": "GPU patch missing"}}
    src = GPU_PATCH.read_text()
    requests_gpu = "flame_stdp_pair_gpu" in src
    runtime_kernel_flagged = "runtime-kernel" in src or "runtime_cuda.c" in src
    falsifiers = all(f in src for f in ["F-STDP-GPU-1", "F-STDP-GPU-2",
                                          "F-STDP-GPU-3", "F-STDP-GPU-4"])
    cpu_companion = "flame-spiking-substrate-primitives" in src
    return {"name": "B-S141-4 INBOX-PATCH-PATH-HEXA-FIRST-COMPLIANT",
            "passed": bool(requests_gpu and runtime_kernel_flagged
                            and falsifiers and cpu_companion),
            "evidence": {"requests_flame_stdp_pair_gpu": requests_gpu,
                          "runtime_kernel_tier_flagged": runtime_kernel_flagged,
                          "all_4_falsifiers_present": falsifiers,
                          "cpu_companion_cited": cpu_companion}}


def b_s141_5_central_and_ast():
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
    return {"name": "B-S141-5 CENTRAL-0-DIFF-AND-NO-FORBIDDEN-IMPORT",
            "passed": bool(central_ok and len(ih) == 0),
            "evidence": {"central_sha16": prefix, "central_match": central_ok,
                          "forbidden_imports": sorted(ih)}}


def b_s141_note():
    return {"name": "B-S141-NOTE EMPIRICAL-CARVE-OUT (NOT counted 🔵)",
            "carve_out_kind": "design-names-gpu-gap-kernel-impl-is-upstream",
            "family": "B-EMERGE-7 / §138-§139-§140 / §71-flame-inbox-precedent",
            "honest_scope": ("§141 names the LEGO GPU fire prerequisite: a "
                             "flame_stdp_pair_gpu device CUDA kernel (runtime_cuda.c "
                             "+ codegen wire) — a heavier upstream change than §138's "
                             "pure-hexa CPU stdlib. The O(N) event/refractory ops can "
                             "stay CPU; only the O(N²) STDP outer-product genuinely "
                             "needs GPU. inbox patch flame-stdp-pair-gpu-kernel.md "
                             "filed. §141 does NOT implement the kernel (hexa-lang "
                             "upstream CUDA work) and does NOT fire a GPU LIF (the "
                             "prerequisite is unmet — fire-gate discipline forbids "
                             "firing on an unmet prerequisite). A LEGO GPU fire is "
                             "honestly 2 upstream steps away. GOAL-orthogonal engine "
                             "tooling; necessary-not-sufficient (B-EMERGE-7); GOAL 미도달.")}


def main():
    results = {
        "preconditions": [b_s141_5_central_and_ast()],
        "closed_propositions": [
            b_s141_1_gpu_primitive_is_device_kernel(),
            b_s141_2_stdp_pair_is_on2(),
            b_s141_3_lego_gpu_fire_2_steps_away(),
            b_s141_4_inbox_patch_filed(),
            b_s141_5_central_and_ast(),
        ],
        "empirical_carve_out": b_s141_note(),
    }
    all_pre = all(p["passed"] for p in results["preconditions"])
    all_props = all(p["passed"] for p in results["closed_propositions"])
    cc = sum(1 for p in results["closed_propositions"] if p["passed"])
    total = len(results["closed_propositions"])
    summary = {
        "preconditions_passed": all_pre,
        "closed_propositions_passed": f"{cc}/{total}",
        "all_closed_pass": all_props,
        "battery_verdict": (f"GPU-SPIKING-DESIGN-CLOSE-DEVICE-KERNEL-GAP-NAMED-{cc}-{total}-🔵"
                            if (all_pre and all_props) else "BATTERY-INCOMPLETE"),
        "empirical_carve_out_NOT_counted_🔵": True,
        "north_star_unchanged": True, "goal_unreached": True,
    }
    results["summary"] = summary
    (HERE / "blue_falsifier_s141_result.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if (all_pre and all_props) else 1)


if __name__ == "__main__":
    main()
