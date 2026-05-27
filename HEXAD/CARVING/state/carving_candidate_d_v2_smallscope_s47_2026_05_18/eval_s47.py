#!/usr/bin/env python3
"""§47 eval — §25 candidate D v2 fire (anchor-DISTINCT content, small-scope).

The 64-anchor routing eval is the §16 harness (eval_carving_s16.py)
BYTE-IDENTICAL — imported, NOT re-typed. The §16 harness is run on the
§47 ckpt to produce the standard 4-axis result; THIS wrapper then adds a
§47-specific report: routing accuracy on the 29 tier>=77-fail TARGET
subset (the candidate-D v2 measurement) alongside the full 64.

  §16 baseline on the 29 targets : 0/29 (all 29 failed by definition —
    they ARE the tier>=77-but-fail set, §32 L3 genuine grade).
  §34 baseline (shared template) : 2/29 with full-64 21->4 regression.
  §47 measure                    : X/29 on the same 29-anchor subset
                                   with anchor-DISTINCT discriminative
                                   content per target.

Honest framing (g3): even a positive X is a sufficient-condition lever,
NOT GOAL emergence; §15 milestone (north-star unsolved) unchanged.
§42 predicted weak/null (lottery internal to tier>=77 band).
"""
import argparse
import json
import os
import subprocess
import sys

# the 29 tier>=77-fail TARGET anchors (§32 L3 genuine-grade fail ∩ tier>=77).
TARGET_TIERS = [
    83, 86, 88, 90, 91, 93, 94, 97, 99, 100, 105, 109, 110, 112, 114,
    115, 116, 117, 118, 119, 120, 121, 122, 123, 125, 128, 129, 130, 131,
]
_TARGET_SET = set(TARGET_TIERS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--max-new", type=int, default=90)
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    s16_eval = os.path.join(here, "eval_carving_s16.py")  # byte-identical
    raw_out = args.output + ".s16raw.json"

    # run the §16 harness UNMODIFIED on the §47 ckpt.
    cmd = [sys.executable, s16_eval, "--ckpt", args.ckpt,
           "--output", raw_out, "--device", args.device,
           "--max-new", str(args.max_new)]
    print("RUN §16 harness:", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)

    with open(raw_out) as f:
        res = json.load(f)

    probes = res["axis1_knowledge_access"]["probes"]
    by_tier = {p["tier"]: p for p in probes}
    target_probes = []
    target_routed = 0
    target_semantic = 0
    for t in sorted(_TARGET_SET):
        p = by_tier.get(t)
        if p is None:
            continue
        rok = bool(p["routing_correct"])
        sem = bool(p["semantic_recall"])
        target_routed += rok
        target_semantic += sem
        target_probes.append({
            "tier": t, "category": p["category"],
            "routing_correct": rok, "semantic_recall": sem,
            "own_tier_surfaced": p["own_tier_surfaced"],
            "bled_into_tiers": p["bled_into_tiers"],
            "rep": p["rep"], "gen": p["gen"][:130]})

    n_target = len(target_probes)
    full_routing = res["axis1_knowledge_access"]["routing_accuracy"]

    # honest verdict (g3 — measured only, no pre-loaded conclusion).
    if target_routed >= 6:
        verdict = ("SIGNAL — candidate D v2 (anchor-distinct) routed "
                   f"{target_routed}/{n_target} (>=6) of the tier>=77-fail "
                   "anchors. Anchor-distinct content lifted multiple "
                   "anchors above the §32 L3 necessity floor (vs §34's "
                   "shared-template 2/29). §42 weak/null prediction "
                   "partly refuted on the data axis. NOT GOAL emergence (g3).")
    elif target_routed >= 1:
        verdict = ("WEAK-POSITIVE — candidate D v2 routed "
                   f"{target_routed}/{n_target}. Comparable to §34's "
                   "2/29; anchor-distinct content moves a few but not "
                   "decisively more. §42 prediction broadly confirmed.")
    else:
        verdict = ("NULL — candidate D v2 routed 0/29 (§42 weak/null "
                   "prediction confirmed). Lottery internal to tier>=77 "
                   "band lies in SGD init/batch-order, NOT anchor-property "
                   "or content-distinctness. Honest negative, valuable.")

    s47 = {
        "eval_version": "s47-candidate-d-v2-smallscope",
        "research_section": ("RESEARCH.md §47 / §25 candidate D v2 / §34 / "
                             "§32 L3 / §42"),
        "ckpt": res.get("ckpt"),
        "ckpt_sha256": res.get("ckpt_sha256"),
        "honest_framing": (
            "§47 = §25 candidate D v2 fire — anchor-DISTINCT content for "
            "the 29 tier>=77-fail anchors. §34 used SHARED template "
            "(2/29 routed but full-64 21->4 regression). §47 uses "
            "per-anchor signature-derived discriminative paragraph (no "
            "shared skeleton, C(29,2)=406 pairwise byte-distinct). Scale "
            "REDUCED: 0.25× §16 step budget (3000 vs 12000) — small-scope "
            "per §47 mandate. The 64-anchor harness is §16's "
            "(eval_carving_s16.py byte-identical). §47 subset report = "
            "routing on the 29 tier>=77-fail TARGET anchors. §16 baseline "
            "on those 29 = 0/29; §34 baseline = 2/29 with full-64 "
            "21->4. §42 predicted weak/null (lottery internal). §47 "
            "measures whether anchor-distinct content moves the needle "
            "beyond §34 OR confirms §42's negative. NOT GOAL emergence "
            "either way."),
        "target_subset_29": {
            "n_target": n_target,
            "target_tiers": sorted(_TARGET_SET),
            "s16_baseline_routing": f"0/{n_target}",
            "s34_baseline_routing": f"2/{n_target}",
            "s47_routing": f"{target_routed}/{n_target}",
            "s47_semantic_recall": f"{target_semantic}/{n_target}",
            "delta_vs_s16_baseline": target_routed,
            "delta_vs_s34_baseline": target_routed - 2,
            "verdict": verdict,
            "probes": target_probes},
        "full_64_anchor": {
            "routing_accuracy": full_routing,
            "semantic_recall":
                res["axis1_knowledge_access"]["semantic_recall"],
            "joint": res["joint_metric"]["SCORE_joint"],
            "axis2_chat_uncontaminated":
                res["axis2_chat_uncontaminated"]["score"],
            "axis3_lane_separation":
                res["axis3_lane_separation"]["score"],
            "axis4_v_spont": res["axis4_v_spont"]["score"]},
        "baseline_compare": {
            "s16_full_routing": "21/64",
            "s16_full_joint": 0.0,
            "s34_full_routing": "4/64",
            "s34_full_joint": 0.0297,
            "note": ("§16 full-64 routing 21/64 (genuine 17). §34 with "
                     "shared template 4/64 (regression). §47 measures "
                     "whether anchor-distinct content avoids both the "
                     "shared-template attractor AND moves the 29 targets.")},
        "s16_raw_result_file": os.path.basename(raw_out),
    }
    with open(args.output, "w") as f:
        json.dump(s47, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "target_subset_routing": f"{target_routed}/{n_target}",
        "target_semantic": f"{target_semantic}/{n_target}",
        "full_64_routing": full_routing,
        "full_64_joint": res["joint_metric"]["SCORE_joint"],
        "delta_vs_s34": target_routed - 2,
        "verdict_bucket": ("SIGNAL" if target_routed >= 6
                           else "WEAK-POSITIVE" if target_routed >= 1
                           else "NULL")},
        ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
