#!/usr/bin/env python3
"""H_9200 P0: extend the existing grow-window/echo-guard G1 probe to 3 seeds.

This imports the frozen concepts, coverage, decoder, and grow-window implementation
from state/g1_growwindow_remeasure without modifying that prior artifact.
"""
import importlib.util
import json
import os
import sys
import time


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = os.path.join(ROOT, "state", "g1_growwindow_remeasure")
CKPT = sys.argv[1]
SEEDS = [int(x) for x in sys.argv[2:]] or [7, 4302, 4303]

spec = importlib.util.spec_from_file_location(
    "g1_growwindow_base", os.path.join(BASE, "g1_growwindow_remeasure.py")
)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
# The imported legacy script interprets argv[2] as RF_CAP. In this wrapper argv[2]
# is the first RNG seed, so pin the preregistered physical receptive-field cap.
M.RF_CAP = 512


def measure_seed(weights, known, base_seed):
    concepts = M._g6_concepts()
    singles = []
    max_raw = 0
    max_novel = 0
    for idx, concept in enumerate(concepts):
        seed = concept + ". "
        text = M._clm_decode_grow(weights, seed, M.GEN, 40, 0.7,
                                  base_seed + idx, M.RF_CAP)
        raw = M._coverage_raw(text)
        novel = M._coverage_novel(text, seed)
        kwr = M._g6_known_word_ratio(text, known)
        singles.append({"index": idx, "raw": raw, "novel": novel,
                        "kwr": round(kwr, 4), "text": text})
        max_raw = max(max_raw, raw)
        max_novel = max(max_novel, novel)

    composed = []
    pass_raw = False
    pass_novel = False
    for k in range(2, len(concepts) + 1):
        seed = ". ".join(concepts[:k]) + ". "
        text = M._clm_decode_grow(weights, seed, M.GEN, 40, 0.7,
                                  base_seed, M.RF_CAP)
        raw = M._coverage_raw(text)
        novel = M._coverage_novel(text, seed)
        kwr = M._g6_known_word_ratio(text, known)
        coherent = kwr >= 0.5
        clears_raw = raw >= 2 and raw > max_raw and coherent
        clears_novel = novel >= 2 and novel > max_novel and coherent
        composed.append({"k": k, "raw": raw, "novel": novel,
                         "kwr": round(kwr, 4), "coherent": coherent,
                         "clears_raw": clears_raw,
                         "clears_novel": clears_novel, "text": text})
        pass_raw = pass_raw or clears_raw
        pass_novel = pass_novel or clears_novel

    return {
        "seed": base_seed,
        "max_single_raw": max_raw,
        "max_single_novel": max_novel,
        "best_composed_raw": max(x["raw"] for x in composed),
        "best_composed_novel": max(x["novel"] for x in composed),
        "pass_raw": pass_raw,
        "pass_novel": pass_novel,
        "singles": singles,
        "composed": composed,
    }


def main():
    started = time.time()
    weights = M.D.clm_load_weights(CKPT)
    if not weights.get("ok"):
        raise SystemExit("checkpoint is not decodable: " + CKPT)
    known = M._g6_dict_load()
    results = []
    for seed in SEEDS:
        row = measure_seed(weights, known, seed)
        results.append(row)
        print(json.dumps({k: row[k] for k in (
            "seed", "max_single_raw", "max_single_novel",
            "best_composed_raw", "best_composed_novel",
            "pass_raw", "pass_novel")}, ensure_ascii=False), flush=True)

    raw_majority = sum(x["pass_raw"] for x in results) >= 2
    novel_majority = sum(x["pass_novel"] for x in results) >= 2
    out = {
        "hypothesis": "H_9200/A1+A2+A8",
        "ckpt": CKPT,
        "seeds": SEEDS,
        "gen": M.GEN,
        "rf_cap": M.RF_CAP,
        "raw_majority": raw_majority,
        "novel_only_majority": novel_majority,
        "verdict": (
            "CAPABILITY-REAL" if novel_majority else
            "ECHO-ONLY-ROBUST" if raw_majority else
            "TRUE-WALL-CANDIDATE"
        ),
        "results": results,
        "wall_seconds": round(time.time() - started, 1),
    }
    path = os.path.join(HERE, "g1_growwindow_multiseed_result.json")
    with open(path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: out[k] for k in (
        "raw_majority", "novel_only_majority", "verdict", "wall_seconds"
    )}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
