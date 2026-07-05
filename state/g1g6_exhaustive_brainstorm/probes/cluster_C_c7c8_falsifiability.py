#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_9200 cluster C - C7/C8 $0 corpus-statistic probe (G6-targeted corpora).

FROZEN PREREG: C8 (question-free hypothesis corpus) BAR = Q&A-framing fraction
< 10% (observation->prediction declarative, not Q&A). C7 (counterexample
curriculum) BAR = >=50% of lines carry an OBSERVABLE/quantified falsifier
(numbered threshold / rate change / unless-branch) vs unfalsifiable hedges.
Pure $0 corpus statistic, DIRECTIONAL.
"""
import re, json, os
from collections import Counter

REPO = "/Users/mini/dancinlab/anima"
FILES = {
    "en_g6":  f"{REPO}/state/g6_targeted_corpus/corpus/en_block_g6.txt",
    "en_g6_shuf": f"{REPO}/state/g6_targeted_corpus/corpus/en_block_g6_shuf.txt",
}

# Q&A framing cues (C8 wants these ABSENT)
QA_RX = re.compile(r"\?|^(what|why|how|when|where|who)\b|\b(question|answer|ask|asked)\b", re.IGNORECASE)
# Observable / falsifiable cues: numbered thresholds, rate changes, unless-branch, measurable amount
OBS_RX = re.compile(
    r"\b\d|half|third|quarter|double|halves|faster|slower|increases?|decreases?|"
    r"above|below|within|rate|amount|count|density|duration|unless|except|stops?\b",
    re.IGNORECASE)
# Unfalsifiable hedges
HEDGE_RX = re.compile(
    r"\b(may|might|could|perhaps|maybe|possibly|spiritually|mystically|"
    r"ineffable|transcendent|somewhere|somehow)\b", re.IGNORECASE)

def probe(path, tag):
    if not os.path.exists(path):
        return {"tag": tag, "note": "missing"}
    lines = [ln.rstrip("\n") for ln in open(path, encoding="utf-8", errors="replace")]
    n = len(lines)
    qa = sum(1 for ln in lines if QA_RX.search(ln))
    obs = sum(1 for ln in lines if OBS_RX.search(ln))
    hedge = sum(1 for ln in lines if HEDGE_RX.search(ln))
    return {
        "tag": tag, "n_lines": n,
        "C8_question_free": {
            "qa_framed_lines": qa,
            "qa_fraction": round(qa / n, 4),
            "BAR_qa_frac_lt_0.10": (qa / n) < 0.10,
        },
        "C7_falsifiability": {
            "lines_with_observable_cue": obs,
            "observable_fraction": round(obs / n, 4),
            "lines_with_hedge": hedge,
            "hedge_fraction": round(hedge / n, 4),
            "BAR_observable_frac_ge_0.50": (obs / n) >= 0.50,
        },
    }

out = {"prereg": "C8 BAR qa<0.10; C7 BAR observable>=0.50. $0 statistic.", "files": []}
for tag, p in FILES.items():
    out["files"].append(probe(p, tag))
print(json.dumps(out, indent=2, ensure_ascii=False))
od = f"{REPO}/state/g1g6_exhaustive_brainstorm/probes/cluster_C_c7c8_result.json"
open(od, "w").write(json.dumps(out, indent=2, ensure_ascii=False))
print(f"\n[saved] {od}", flush=True)
