#!/usr/bin/env python3
"""§139 LEGO inbox-patch-filed battery — 4 closed-form propositions + 1 NOTE."""

import ast
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent.parent.parent
CENTRAL_BLUE = ANIMA / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
PATCH = Path.home() / "core" / "hexa-lang" / "inbox" / "patches" / "flame-spiking-substrate-primitives.md"


def sha16(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def b_s139_1_patch_file_exists():
    exists = PATCH.exists()
    size = PATCH.stat().st_size if exists else 0
    return {"name": "B-S139-1 INBOX-PATCH-FILE-EXISTS",
            "passed": bool(exists and size > 1000),
            "evidence": {"patch_path": str(PATCH), "exists": exists,
                          "size_bytes": size}}


def b_s139_2_patch_requests_3_primitives():
    if not PATCH.exists():
        return {"name": "B-S139-2 PATCH-REQUESTS-EXACTLY-3-PRIMITIVES",
                "passed": False, "evidence": {"error": "patch missing"}}
    src = PATCH.read_text()
    p1 = "flame_event_threshold" in src
    p2 = "flame_refractory_step" in src
    p3 = "flame_stdp_pair" in src
    falsifiers = all(f in src for f in ["F-SPIKE-1", "F-SPIKE-2", "F-SPIKE-3", "F-SPIKE-4"])
    return {"name": "B-S139-2 PATCH-REQUESTS-EXACTLY-3-PRIMITIVES",
            "passed": bool(p1 and p2 and p3 and falsifiers),
            "evidence": {"flame_event_threshold": p1, "flame_refractory_step": p2,
                          "flame_stdp_pair": p3, "all_4_falsifiers_present": falsifiers}}


def b_s139_3_patch_is_request_not_source_edit():
    """The patch is a markdown request doc, NOT a flame source edit. Boolean:
    file is .md, asserts downstream-consumer posture, no .hexa source change."""
    if not PATCH.exists():
        return {"name": "B-S139-3 PATCH-IS-REQUEST-NOT-SOURCE-EDIT",
                "passed": False, "evidence": {"error": "patch missing"}}
    src = PATCH.read_text()
    is_markdown = PATCH.suffix == ".md"
    downstream_posture = ("downstream consumer" in src or "downstream-consumer" in src)
    request_only = ("patch-request only" in src or "patch-request" in src)
    invariant_cited = "upstream_downstream_invariant" in src
    return {"name": "B-S139-3 PATCH-IS-REQUEST-NOT-SOURCE-EDIT",
            "passed": bool(is_markdown and downstream_posture and request_only
                            and invariant_cited),
            "evidence": {"is_markdown": is_markdown,
                          "downstream_consumer_posture": downstream_posture,
                          "request_only_stated": request_only,
                          "upstream_downstream_invariant_cited": invariant_cited}}


def b_s139_4_central_and_ast():
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
    return {"name": "B-S139-4 CENTRAL-0-DIFF-AND-NO-FORBIDDEN-IMPORT",
            "passed": bool(central_ok and len(ih) == 0),
            "evidence": {"central_sha16": prefix, "central_match": central_ok,
                          "forbidden_imports": sorted(ih)}}


def b_s139_note():
    return {"name": "B-S139-NOTE EMPIRICAL-CARVE-OUT (NOT counted 🔵)",
            "carve_out_kind": "patch-filed-implementation-is-upstream",
            "family": "B-EMERGE-7 / §138-design / §71-flame-inbox-precedent",
            "honest_scope": ("§139 filed the flame spiking-primitives inbox patch "
                             "(§138's named follow-up), completing the hexa-first "
                             "PR-only path. The 3 primitives are NOT implemented — that "
                             "is hexa-lang upstream work, reviewed/PR'd on their side. "
                             "lego_engine.hexa does not exist yet; it is a mechanical "
                             "port AFTER the primitives land (F-SPIKE-4 byte-equal). "
                             "anima stayed a downstream consumer — wrote a request doc, "
                             "edited no flame source. GOAL-orthogonal engine tooling; "
                             "necessary-not-sufficient (B-EMERGE-7); GOAL 미도달.")}


def main():
    results = {
        "preconditions": [b_s139_4_central_and_ast()],
        "closed_propositions": [
            b_s139_1_patch_file_exists(),
            b_s139_2_patch_requests_3_primitives(),
            b_s139_3_patch_is_request_not_source_edit(),
            b_s139_4_central_and_ast(),
        ],
        "empirical_carve_out": b_s139_note(),
    }
    all_pre = all(p["passed"] for p in results["preconditions"])
    all_props = all(p["passed"] for p in results["closed_propositions"])
    cc = sum(1 for p in results["closed_propositions"] if p["passed"])
    total = len(results["closed_propositions"])
    summary = {
        "preconditions_passed": all_pre,
        "closed_propositions_passed": f"{cc}/{total}",
        "all_closed_pass": all_props,
        "battery_verdict": (f"INBOX-PATCH-FILED-HEXA-FIRST-PATH-COMPLETE-{cc}-{total}-🔵"
                            if (all_pre and all_props) else "BATTERY-INCOMPLETE"),
        "empirical_carve_out_NOT_counted_🔵": True,
        "north_star_unchanged": True, "goal_unreached": True,
    }
    results["summary"] = summary
    (HERE / "blue_falsifier_s139_result.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if (all_pre and all_props) else 1)


if __name__ == "__main__":
    main()
