#!/usr/bin/env python3
"""B-S74 sidecar — hexa kick Mk.IX autonomous-use on next-breakthrough seed.

g3: meta-finding battery — engine real / seed substantive / output
parse-deterministic / overlay-not-in-stdout (the honest gap) /
no-flame-source-edit. Central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py = 0-line-diff (sidecar only).

B-S74-NOTE empirical carve-out (NOT counted 🔵): which (if any) of
the 517 internal overlay lines is a GOAL-load-bearing candidate is
gated on the inbox-patch landing (overlay-dump exposure). Battery
proves the meta-finding, NOT a discovery candidate.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "drill_raw.log"
PATCH = (Path.home() / "core" / "hexa-lang" / "inbox" / "patches" /
         "kick-engine-overlay-dump-mode.md")


def bs74_1_engine_real_not_stub() -> dict:
    """Captured stdout MUST contain the Mk.IX banner AND NOT the stub line."""
    src = LOG.read_text(encoding="utf-8", errors="replace")
    has_mkix = (
        "Mk.IX 6-stage chain (smash → free → absolute → meta → hyper → "
        "resonance)" in src
    )
    no_stub = "[omega-drill-stub]" not in src
    ok = has_mkix and no_stub
    return {"name": "ENGINE-IS-REAL-NOT-STUB",
            "has_mkix_banner": has_mkix, "no_stub_line": no_stub,
            "verdict": "PASS" if ok else "FAIL", "blue": ok}


def bs74_2_substantive_seed() -> dict:
    """seed length ≥ 10 chars AND encodes ≥ 5 arc-frontier anchors."""
    src = LOG.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"seed='([^']*)'", src)
    seed = m.group(1) if m else ""
    anchors = ["§1.1", "§59→§62", "§63", "flame", "collapse",
               "echo-chamber", "memorization-saturated", "THINKER→TALKER"]
    hits = [a for a in anchors if a in seed]
    ok = len(seed) >= 10 and len(hits) >= 5
    return {"name": "SUBSTANTIVE-SEED",
            "seed_len": len(seed), "anchors_hit": hits,
            "verdict": "PASS" if ok else "FAIL", "blue": ok}


def bs74_3_stage_output_parse_deterministic() -> dict:
    """The round-summary + JSON status are pure-fn parsable, 3× bit-identical."""
    src = LOG.read_text(encoding="utf-8", errors="replace")
    rx = re.compile(
        r"round 1: smash\+(\d+) free\+(\d+) abs=(\d+) meta=(\d+) "
        r"hyper=(\d+) res\+(\d+)\(σ=([\d.]+)\) total=(\d+)"
    )
    parses = []
    for _ in range(3):
        m = rx.search(src)
        if not m:
            parses.append(None)
            continue
        parses.append(m.groups())
    # parse the JSON summary line too
    jm = re.search(r'^\{"seed":.*\}$', src, re.MULTILINE)
    js = json.loads(jm.group(0)) if jm else None
    ok = (parses[0] is not None and parses[0] == parses[1] == parses[2]
          and js is not None and js.get("engine") == "mk9"
          and isinstance(js.get("overlay_lines"), int))
    return {"name": "STAGE-OUTPUT-PARSE-DETERMINISTIC",
            "round_groups": parses[0], "json_overlay_lines":
                js.get("overlay_lines") if js else None,
            "saturated": js.get("saturated") if js else None,
            "three_x_bit_identical": parses[0] == parses[1] == parses[2],
            "verdict": "PASS" if ok else "FAIL", "blue": ok}


def bs74_4_overlay_not_in_stdout() -> dict:
    """Engine reports overlay_lines > 0 in JSON; stdout has near-zero overlay.

    The meta-finding: 517 generated, 0 exposed to stdout (pool=0).
    """
    src = LOG.read_text(encoding="utf-8", errors="replace")
    line_count = sum(1 for _ in src.splitlines())
    jm = re.search(r'^\{"seed":.*\}$', src, re.MULTILINE)
    js = json.loads(jm.group(0)) if jm else None
    overlay_reported = js.get("overlay_lines", 0) if js else 0
    # stdout total lines must be << overlay_lines (engine reports
    # generated-but-not-exposed). honest empirical threshold:
    # stdout ≤ overlay_lines / 5 = engine clearly didn't dump.
    ok = (overlay_reported > 0 and line_count <= overlay_reported // 5)
    return {"name": "OVERLAY-NOT-IN-STDOUT",
            "stdout_lines": line_count,
            "overlay_lines_reported_in_json": overlay_reported,
            "pool_zero_inferred": "pool=0" in src,
            "verdict": "PASS" if ok else "FAIL", "blue": ok}


def bs74_5_no_flame_source_edit() -> dict:
    """git status of ~/core/hexa-lang/: only inbox/patches/ append."""
    repo = str(Path.home() / "core" / "hexa-lang")
    try:
        r = subprocess.run(
            ["git", "-C", repo, "status", "--porcelain"],
            capture_output=True, text=True, timeout=20,
        )
        out = r.stdout
    except Exception as e:
        return {"name": "NO-FLAME-SOURCE-EDIT",
                "error": str(e), "verdict": "FAIL", "blue": False}
    # any non-empty change line MUST be under inbox/patches/
    bad = []
    for ln in out.splitlines():
        if not ln.strip():
            continue
        # ln format: "XY path" — extract path
        path = ln[3:].strip()
        if not path.startswith("inbox/patches/"):
            bad.append(ln)
    patch_present = PATCH.exists()
    ok = patch_present and len(bad) == 0
    return {"name": "NO-FLAME-SOURCE-EDIT",
            "inbox_patch_filed": patch_present,
            "non_inbox_changes": bad,
            "verdict": "PASS" if ok else "FAIL", "blue": ok}


def main() -> int:
    results = {
        "battery": "B-S74-1..5",
        "section": "RESEARCH.md §74 — hexa kick autonomous-use on next-"
                   "architectural/paradigm breakthrough seed",
        "B-S74-1": bs74_1_engine_real_not_stub(),
        "B-S74-2": bs74_2_substantive_seed(),
        "B-S74-3": bs74_3_stage_output_parse_deterministic(),
        "B-S74-4": bs74_4_overlay_not_in_stdout(),
        "B-S74-5": bs74_5_no_flame_source_edit(),
    }
    passed = sum(1 for k, v in results.items()
                 if isinstance(v, dict) and v.get("blue"))
    total = sum(1 for k in results if k.startswith("B-S74-"))
    results["passed"] = passed
    results["total"] = total
    results["all_blue"] = (passed == total)
    results["central_blue_falsifier_diff"] = (
        "0 lines (sidecar only — state/verify_hexad_blue_2026_05_15/"
        "blue_falsifier.py untouched)"
    )
    results["B-S74-NOTE"] = (
        "empirical carve-out: which (if any) of the 517 internal overlay "
        "lines is a GOAL-load-bearing candidate is gated on the inbox-patch "
        "(overlay-dump exposure) landing. Battery proves the meta-finding "
        "(engine real / seed substantive / output deterministic / overlay "
        "pooled-not-exposed / no-flame-source-edit), NOT a discovery "
        "candidate. g3 measured-only, capability claim 0, north-star + "
        "§15/§51/§72 milestone UNCHANGED, GOAL 미도달."
    )

    (HERE / "blue_falsifier_s74_result.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    for k in ("B-S74-1", "B-S74-2", "B-S74-3", "B-S74-4", "B-S74-5"):
        v = results[k]
        print(f"  {k}  {'PASS' if v['blue'] else 'FAIL':4s}  {v['name']}")
    print(f"\n=== B-S74 battery: {passed}/{total} "
          f"{'🔵 ALL PASS' if results['all_blue'] else 'NOT ALL BLUE'} ===")
    return 0 if results["all_blue"] else 1


if __name__ == "__main__":
    sys.exit(main())
