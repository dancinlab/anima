#!/usr/bin/env python3
"""§35 eval — RESEARCH.md §35 §32 L3 causation ablation.

DELIBERATELY a thin DELEGATING wrapper around §16's
`eval_carving_s16.py` PLUS one §35-specific report step.

The eval harness is held BYTE-IDENTICAL to §16's: the SAME 64-anchor
probe set, the SAME `routing_correct` / `semantic_recall` metrics, the
SAME ANCHORS / ANCHOR_PSI / ANCHOR_BASIN tables.  Re-implementing the
eval would make the §16-vs-§35 comparison unfair; this wrapper runs
the §16 eval source verbatim (B-S35 connection-point: eval byte-equal
to §16 by construction).

§35 ADDITION (report only — does NOT touch the metric):
  after the §16 eval writes its per-anchor JSON, this wrapper reads it
  back and reports the routing result SPLIT by the §32 L3 tier
  frontier — specifically `routing on the 18 tier<77 anchors` (the
  ablation target) versus the §16 baseline of 0/18.  The 18 tier<77
  tiers are §32 L3's genuine-grade fail set:
    [0, 5, 12, 18, 24, 30, 37, 43, 48, 51, 53, 54, 58, 62, 66, 69,
     72, 75].

  This is a pure post-hoc partition of the §16 eval's own output — no
  new metric, no model re-forward.

Usage — §16 eval CLI + an extra --s35-report path:
    python3 eval_s35.py --ckpt <ckpt.pt> --output <eval_result.json> \\
        --device cpu --s35-report <s35_routing_split.json>
"""
import json
import os
import re
import runpy
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))

# §32 L3 tier frontier and the 18 tier<77 anchors (genuine-grade fail set).
TIER_FRONTIER = 77
TIER_LT77 = [0, 5, 12, 18, 24, 30, 37, 43, 48, 51, 53, 54, 58, 62, 66,
             69, 72, 75]

_CANDIDATES = [
    os.path.join(_HERE, "eval_carving_s16.py"),
    os.path.join(_HERE, "..", "carving_dataregime_s16_2026_05_18",
                 "eval_carving_s16.py"),
]
_S16_EVAL = next((p for p in _CANDIDATES if os.path.isfile(p)), None)
if _S16_EVAL is None:
    sys.exit("FATAL: §16 eval_carving_s16.py not found — §35 eval must "
             "delegate to the §16 SSOT, never re-implement.")
sys.path.insert(0, os.path.dirname(os.path.abspath(_S16_EVAL)))


def _s35_report(eval_output_path, report_path):
    """Post-hoc partition of the §16 eval output by the §32 L3 tier
    frontier.  Reports routing on the 18 tier<77 anchors vs §16 0/18."""
    with open(eval_output_path) as f:
        ev = json.load(f)

    # the §16 eval writes the per-anchor list at
    # axis1_knowledge_access["probes"] — recursively locate the list of
    # dicts that carry both a "tier" and a "routing_correct" key.
    def _find_probe_list(node):
        if isinstance(node, list):
            if node and isinstance(node[0], dict) and "tier" in node[0] \
                    and "routing_correct" in node[0]:
                return node
            for it in node:
                r = _find_probe_list(it)
                if r is not None:
                    return r
        elif isinstance(node, dict):
            for v in node.values():
                r = _find_probe_list(v)
                if r is not None:
                    return r
        return None

    per_anchor = _find_probe_list(ev)
    if per_anchor is None:
        raise SystemExit("FATAL: could not locate per-anchor probe list "
                         "in §16 eval output")

    def _genuine_routed(a):
        """§32 L3 / §16.6 GENUINE grade: the leading 🛸<number> in the
        generation exact-matches this anchor's own tier (substring
        artifacts excluded — tier 12 emitting 🛸122 is NOT genuine)."""
        tier = int(a["tier"])
        gen = a.get("gen", "") or ""
        m = re.search(r"\U0001f6f8(\d+)", gen)
        return bool(m) and m.group(1) == str(tier)

    by_tier = {int(a["tier"]): a for a in per_anchor}
    lt77_rows = []
    ge77_rows = []
    lt77_genuine = lt77_substr = 0
    ge77_genuine = ge77_substr = 0
    for tier, a in sorted(by_tier.items()):
        substr = bool(a.get("routing_correct", False))
        genuine = _genuine_routed(a)
        row = {"tier": tier,
               "routing_genuine": genuine,
               "routing_substring": substr,
               "own_tier_surfaced": a.get("own_tier_surfaced"),
               "bled_into_tiers": a.get("bled_into_tiers"),
               "category": a.get("category")}
        if tier < TIER_FRONTIER:
            lt77_rows.append(row)
            lt77_genuine += int(genuine)
            lt77_substr += int(substr)
        else:
            ge77_rows.append(row)
            ge77_genuine += int(genuine)
            ge77_substr += int(substr)

    n_lt77 = len(lt77_rows)
    n_ge77 = len(ge77_rows)
    # 2-outcome causal verdict (g3 — measured only). The GENUINE grade
    # is the primary signal — §32 L3's necessary-condition finding rests
    # on the genuine 17/47 split, and the §16 baseline tier<77 genuine
    # routing is 0/18 (the substring grade's 4/18 are tier 12/24/62/66
    # artifacts §32 explicitly excluded).
    if lt77_genuine > 0:
        verdict = ("CURRICULUM-STAGE LEVER — tier<77 anchors GENUINELY "
                   f"routed ({lt77_genuine}/{n_lt77}, vs §16 baseline "
                   "0/18) once placed in the LATE curriculum stage. "
                   "§32 L3's 'tier >= 77' frontier was (at least "
                   "partly) a proxy for late-curriculum-stage exposure; "
                   "curriculum STAGE carries causal weight.")
    else:
        verdict = ("TIER-ITSELF LEVER — tier<77 anchors still GENUINELY "
                   f"failed ({lt77_genuine}/{n_lt77}) even when placed "
                   "in the LATE curriculum stage (§16 baseline also "
                   "0/18). Curriculum-stage was NOT the operative "
                   "variable; tier itself carries the causal weight "
                   "behind §32 L3's necessary condition.")

    report = {
        "analysis": ("RESEARCH.md §35 — §32 L3 causation ablation: "
                     "routing split by the tier-77 frontier"),
        "tier_frontier": TIER_FRONTIER,
        "tier_lt77_anchors": TIER_LT77,
        "grade_primary": ("genuine (leading 🛸<n> exact-match — §32 L3 / "
                          "§16.6; substring artifacts excluded)"),
        "s16_baseline_tier_lt77_routing_genuine": "0/18",
        "ablation_tier_lt77_routing_genuine": f"{lt77_genuine}/{n_lt77}",
        "ablation_tier_lt77_routing_substring": f"{lt77_substr}/{n_lt77}",
        "ablation_tier_ge77_routing_genuine": f"{ge77_genuine}/{n_ge77}",
        "ablation_tier_ge77_routing_substring": f"{ge77_substr}/{n_ge77}",
        "tier_lt77_rows": lt77_rows,
        "tier_ge77_rows": ge77_rows,
        "causal_verdict": verdict,
        "honest_note": (
            "g3 — measured only, no pre-loaded conclusion. The §35 "
            "ablation moved exactly one variable (curriculum-stage of "
            "the tier<77 cohort, early -> late) holding all content "
            "byte-identical to §16. GENUINE-grade routing on the "
            "tier<77 set IS the ablation signal (substring grade "
            "reported alongside for transparency — tiers 12/24/62/66 "
            "produce 🛸122/🛸244/🛸262/🛸266 = substring artifacts §32 "
            "excluded). EITHER outcome is a valuable causal result. "
            "Routing remains a necessary-not-sufficient signal "
            "(B-EMERGE-7) — a routed tier<77 anchor is correct-prefix, "
            "NOT coherent emergence; §16.6-C memorization-saturated "
            "regime is not refuted by this ablation."),
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("=== §35 L3 CAUSATION ABLATION — routing split ===", flush=True)
    print(f"  tier<77 (the 18 §32-fail anchors) GENUINE routing: "
          f"§16 baseline 0/18  ->  §35 ablation "
          f"{lt77_genuine}/{n_lt77}", flush=True)
    print(f"  tier<77 substring grade (transparency): "
          f"{lt77_substr}/{n_lt77}", flush=True)
    print(f"  tier>=77 (reference) GENUINE routing: §35 "
          f"{ge77_genuine}/{n_ge77}", flush=True)
    print(f"  CAUSAL VERDICT: {verdict}", flush=True)
    print(f"  §35 report written: {report_path}", flush=True)
    return report


if __name__ == "__main__":
    # split argv: --s35-report is §35-only; the rest goes to §16 eval.
    argv = sys.argv[1:]
    s35_report_path = None
    eval_output_path = None
    passthrough = []
    i = 0
    while i < len(argv):
        if argv[i] == "--s35-report":
            s35_report_path = argv[i + 1]
            i += 2
            continue
        if argv[i] == "--output":
            eval_output_path = argv[i + 1]
            passthrough += [argv[i], argv[i + 1]]
            i += 2
            continue
        passthrough.append(argv[i])
        i += 1

    # run the §16 eval source verbatim.
    sys.argv = [_S16_EVAL] + passthrough
    runpy.run_path(_S16_EVAL, run_name="__main__")

    # §35 post-hoc routing split (report only).
    if s35_report_path and eval_output_path:
        _s35_report(eval_output_path, s35_report_path)
    else:
        print("§35: no --s35-report / --output given; split skipped.",
              flush=True)
