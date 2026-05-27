#!/usr/bin/env python3
"""RESEARCH.md §46 — SGD-trajectory variance multi-seed comparison.

Given N seed runs (§16 trainer byte-identical, §16 corpus byte-identical,
ONLY trainer --seed varies) compute the routing-correct anchor set for
each fire, then the run-to-run set-comparison metrics:

  * intersection ⋂ᵢ Sᵢ — anchors that route correct under EVERY seed
  * union        ⋃ᵢ Sᵢ — anchors that routed correct under ANY seed
  * Jaccard       J(A,B) = |A ∩ B| / |A ∪ B|  ∈ [0,1]
  * per-anchor stability — for each of the 64 anchors, fraction of seeds
    in which that anchor routed correct (∈ {0, 1/N, 2/N, …, 1})

Verdict bands (§46 task contract, no fudging):
  * SEED-STABLE   : |⋂| close to |individual run| (e.g. ≥ 80% — set up to
                    catch "intersection ≈ 17 (close to §16's 17)")
  * SEED-VARIABLE : |⋂| ≪ |individual run| (e.g. ≤ 50% of run mean — §42
                    SGD-lottery hypothesis SUPPORTED)
  * MIXED         : middle band (band-level reproducibility but per-anchor
                    lottery within band)

The band thresholds are STATED in this header but the script also reports
the raw numbers — verdict is honest given the measured values.

§16 lives at `state/carving_dataregime_s16_2026_05_18/eval_result_s16.json`
(its routing-correct set = 21 anchors, the third datapoint already on file).

The eval result format follows §16's eval_carving_s16.py — each result has
  d["axis1_knowledge_access"]["probes"] = list of {tier, routing_correct, …}

Honest framing (g3):
  Set-comparison metrics are deterministic (3× bit-identical, no RNG, no
  forward). The VERDICT (seed-stable vs seed-variable) interprets the
  numbers under the §46 task's verdict bands — interpretation is empirical
  (B-S46-NOTE). Battery (B-S46-1..4) closes the set-comparison structural
  side (cardinality bounds, Jaccard bounds, seed disjointness, corpus
  byte-identity) — NOT the interpretation.
"""

import argparse
import hashlib
import json
import os
import sys
from collections import defaultdict


def routing_set_from_eval(path):
    """Read an §16-style eval_result_*.json and return (sorted-tier-list,
    routing-correct-tier-set, n_anchors_probed)."""
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    probes = d["axis1_knowledge_access"]["probes"]
    all_tiers = sorted({p["tier"] for p in probes})
    correct = {p["tier"] for p in probes if p.get("routing_correct")}
    return all_tiers, correct, len(probes)


def jaccard(a, b):
    if not a and not b:
        return 1.0  # both empty = trivially identical
    return len(a & b) / max(1, len(a | b))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--eval", action="append", required=True,
        help="seed-tagged eval result, format SEED:PATH (repeatable, ≥2 required)")
    ap.add_argument(
        "--s16-eval", required=True,
        help="path to §16 baseline eval_result_s16.json (the third on-file datapoint)")
    ap.add_argument(
        "--out", required=True, help="output result.json")
    ap.add_argument(
        "--ckpt", action="append", default=[],
        help="optional seed-tagged ckpt for sha256 record, format SEED:PATH")
    args = ap.parse_args()

    # Parse SEED:PATH pairs.
    new_fires = {}
    for s in args.eval:
        seed_str, path = s.split(":", 1)
        new_fires[int(seed_str)] = path
    ckpt_paths = {}
    for s in args.ckpt:
        seed_str, path = s.split(":", 1)
        ckpt_paths[int(seed_str)] = path

    # Load each fire's routing set + §16 baseline.
    fires = {}  # seed -> (all_tiers, correct_set, n_probed)
    s16 = routing_set_from_eval(args.s16_eval)
    fires[1337] = s16  # §16 was seed 1337
    for seed, path in new_fires.items():
        fires[seed] = routing_set_from_eval(path)

    if len(fires) < 2:
        raise SystemExit("§46: need ≥2 seeds (incl §16 baseline) for comparison")

    # Sanity: all fires should have probed the same 64-anchor superset.
    anchor_supersets = {seed: tuple(t) for seed, (t, _, _) in fires.items()}
    if len(set(anchor_supersets.values())) != 1:
        sys.stderr.write(
            "WARNING: anchor supersets differ across fires — "
            f"sets: {anchor_supersets}\n")

    n_seeds = len(fires)
    seeds_sorted = sorted(fires.keys())

    # Compute intersection / union / per-pair Jaccard / per-anchor stability.
    correct_sets = {seed: c for seed, (_, c, _) in fires.items()}
    intersection = set.intersection(*correct_sets.values())
    union = set.union(*correct_sets.values())

    # Pairwise Jaccard (sorted pairs, deterministic).
    pairwise = []
    for i in range(len(seeds_sorted)):
        for j in range(i + 1, len(seeds_sorted)):
            a_seed, b_seed = seeds_sorted[i], seeds_sorted[j]
            a, b = correct_sets[a_seed], correct_sets[b_seed]
            pairwise.append({
                "seed_a": a_seed, "seed_b": b_seed,
                "intersection_size": len(a & b),
                "union_size": len(a | b),
                "jaccard": round(jaccard(a, b), 6),
                "a_only": sorted(a - b),
                "b_only": sorted(b - a),
            })

    # Per-anchor stability: for each anchor in union, fraction of seeds in
    # which it routed correct. Also report on the FULL 64-anchor superset.
    all_anchors_sorted = sorted(set.union(*[set(t) for t, _, _ in fires.values()]))
    stability = []
    for tier in all_anchors_sorted:
        n_correct = sum(1 for seed in seeds_sorted if tier in correct_sets[seed])
        stability.append({
            "tier": tier,
            "n_seeds_correct": n_correct,
            "n_seeds_total": n_seeds,
            "stability_fraction": round(n_correct / n_seeds, 6),
            "correct_in_seeds": sorted(
                [seed for seed in seeds_sorted if tier in correct_sets[seed]]),
        })

    # Verdict bands.
    mean_run_size = sum(len(s) for s in correct_sets.values()) / n_seeds
    inter_size = len(intersection)
    union_size = len(union)
    inter_over_mean = (inter_size / mean_run_size) if mean_run_size > 0 else 0.0

    if inter_over_mean >= 0.80:
        verdict = "SEED-STABLE"
        verdict_note = (
            f"|⋂| {inter_size} ≥ 80% of mean-run-size {mean_run_size:.2f} — "
            f"data-order/curriculum structure carries the routing-success set "
            f"across seeds; §42 SGD-lottery hypothesis NOT supported on this "
            f"axis (the 17-vs-29 split IS reproducible).")
    elif inter_over_mean <= 0.50:
        verdict = "SEED-VARIABLE"
        verdict_note = (
            f"|⋂| {inter_size} ≤ 50% of mean-run-size {mean_run_size:.2f} — "
            f"run-to-run lottery within the necessary band; §42 SGD-trajectory "
            f"hypothesis SUPPORTED (the lever for 17-vs-29 lives in SGD-init/"
            f"batch-order, not in anchor property; consistent with §1.1 "
            f"data-regime threshold's deeper face).")
    else:
        verdict = "MIXED"
        verdict_note = (
            f"|⋂| {inter_size} is between 50% and 80% of mean-run-size "
            f"{mean_run_size:.2f} — band-level reproducibility (a stable "
            f"sub-core routes regardless of seed) but per-anchor lottery "
            f"within that band; §42 hypothesis partially supported.")

    # Optional ckpt shas.
    ckpt_meta = {}
    for seed, path in ckpt_paths.items():
        if os.path.exists(path):
            ckpt_meta[str(seed)] = {
                "path": path,
                "sha256": sha256_file(path),
                "size_bytes": os.path.getsize(path),
            }
        else:
            ckpt_meta[str(seed)] = {"path": path, "missing": True}

    result = {
        "research_section": "RESEARCH.md §46 — SGD-trajectory variance multi-seed",
        "trigger": (
            "§42 prediction (TIER77 FINDINGS §7-#10): within-band routing-"
            "success is SGD-trajectory lottery. §46 measures whether re-firing "
            "§16 with different seeds re-shuffles the 17-vs-29 split."),
        "design": (
            "Corpus byte-identical to §16 SSOT (sha256 422c64a0…). Trainer + "
            "model + steps + curriculum byte-identical to §16. ONLY trainer "
            "--seed varies. §16 (seed 1337) is the third datapoint already on "
            "file (eval_result_s16.json, 21 routing-correct anchors)."),
        "n_seeds": n_seeds,
        "seeds": seeds_sorted,
        "per_seed": {
            str(seed): {
                "routing_correct_set": sorted(correct_sets[seed]),
                "routing_correct_count": len(correct_sets[seed]),
                "n_anchors_probed": fires[seed][2],
            }
            for seed in seeds_sorted
        },
        "intersection_all": sorted(intersection),
        "intersection_size": inter_size,
        "union_all": sorted(union),
        "union_size": union_size,
        "mean_run_size": round(mean_run_size, 4),
        "intersection_over_mean_run": round(inter_over_mean, 4),
        "pairwise_jaccard": pairwise,
        "per_anchor_stability": stability,
        "anchors_unanimously_correct": sorted(
            [s["tier"] for s in stability if s["n_seeds_correct"] == n_seeds]),
        "anchors_unanimously_failed": sorted(
            [s["tier"] for s in stability if s["n_seeds_correct"] == 0]),
        "anchors_seed_split": sorted(
            [s["tier"] for s in stability
             if 0 < s["n_seeds_correct"] < n_seeds]),
        "verdict": verdict,
        "verdict_note": verdict_note,
        "verdict_bands": {
            "SEED-STABLE": "|⋂| / mean-run-size ≥ 0.80",
            "MIXED": "0.50 < |⋂| / mean-run-size < 0.80",
            "SEED-VARIABLE": "|⋂| / mean-run-size ≤ 0.50",
        },
        "ckpt_meta": ckpt_meta,
        "honest_framing": (
            "Set-comparison metrics (intersection, union, Jaccard, per-anchor "
            "stability) are DETERMINISTIC pure functions of the eval JSONs — "
            "no RNG, no forward. The VERDICT is an interpretation under the "
            "fixed bands above and is therefore EMPIRICAL (B-S46-NOTE — "
            "B-D-NOTE / B-L3-NOTE / B-S35-NOTE family). Battery B-S46-1..4 "
            "closes corpus byte-identity, seed disjointness, intersection-"
            "cardinality bound and Jaccard ∈ [0,1] — closed-form structural, "
            "not capability."),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "verdict": verdict,
        "n_seeds": n_seeds,
        "intersection_size": inter_size,
        "union_size": union_size,
        "mean_run_size": round(mean_run_size, 4),
        "intersection_over_mean": round(inter_over_mean, 4),
        "pairwise_jaccards": [round(p["jaccard"], 4) for p in pairwise],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
