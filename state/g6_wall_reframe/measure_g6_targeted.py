#!/usr/bin/env python3
"""G6 TARGETED coverage: falsifiable FORM (comp×meas) INTERSECTED with ideation-seed TOPICS.

이것이 진짜 G1-analog. G1(H_6185)은 generic 개념이 아니라 gate 의 TARGET 개념쌍을 쟀다.
1차 측정(measure_g6_coverage.py)은 generic comparator×measurable 을 재서 "form 은 풍부"를 확인.
그러나 G6 gate 는 IDEATION_SEEDS(consciousness/mind/substrate/memory ...) 주제에 대해
반증가능 주장을 생성하라 요구한다. 따라서 결정적 질문:
  "반증가능 FORM 이 ideation-seed 주제어와 한 발화에서 공동출현하는가?"
  → ~0 이면 TARGETED-coverage 갭(G1식 데이터 레버) · 풍부하면 attention-capacity 천장 확정.

TOPIC set = gauge_lib IDEATION_SEEDS + CONCEPTS 주제어 (VERBATIM 어휘).
검출 = 1차 스크립트 _is_falsifiable(comp&meas&content) AND 라인에 topic 단어 >=1.
"""
import json
import re
import sys

COMPARATOR = {"if", "when", "whenever", "than", "more", "less", "greater",
              "fewer", "higher", "lower", "increases", "decreases", "correlates",
              "predicts", "causes", "depends", "unless", "whereas", "versus",
              "compared", "proportional", "faster", "slower", "stronger", "weaker"}
MEASURABLE = {"measure", "measured", "rate", "number", "count", "amount", "level",
              "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
              "score", "value", "quantity", "percent", "times", "fraction", "distance",
              "duration", "speed", "size", "strength", "density"}
STOP = {"a", "i", "the", "of", "and", "to", "in", "is", "it", "that", "we", "you",
        "they", "s", "t", "as", "on", "at", "by", "or", "be", "an", "for", "with",
        "this", "from", "are", "was"}
STANCE = {"that", "s", "a", "profound", "question", "i", "think", "interesting",
          "good", "nice", "great", "wonderful", "beautiful", "amazing"}

# TOPIC = IDEATION_SEEDS content words + CONCEPTS keyword sets (gauge_lib.py VERBATIM)
TOPIC = {
    # IDEATION_SEEDS content words
    "idea", "consciousness", "minds", "mind", "connect", "substrate", "memory",
    "hypothesis", "testing", "imagine",
    # CONCEPTS keyword sets
    "cells", "aware", "tension", "ripple", "distant", "between",
    "meaning", "compose", "silence", "information", "quiet", "carries",
    "dream", "engine", "alone", "sleep",
}

def _build_known():
    known = set(STOP) | COMPARATOR | MEASURABLE | STANCE | TOPIC
    for p in ("/usr/share/dict/words",):
        try:
            with open(p, errors="ignore") as f:
                for w in f:
                    w = w.strip().lower()
                    if w.isalpha():
                        known.add(w)
            break
        except OSError:
            continue
    return known
_KNOWN = _build_known()
_TOK = re.compile(r"[0-9A-Za-z]+")

def is_falsifiable(toks):
    if not toks: return False
    if not any(w in COMPARATOR for w in toks): return False
    if not any(w in MEASURABLE for w in toks): return False
    if sum(1 for w in toks if len(w) >= 3 and w in _KNOWN and w not in STOP) < 2: return False
    nf = min(3, len(toks))
    if nf > 0 and all(toks[f] in STANCE for f in range(nf)): return False
    return True

def measure(path, cap=40):
    n_lines = fals = topic_lines = fals_topic = 0
    samples = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            n_lines += 1
            toks = [m.group(0).lower() for m in _TOK.finditer(line)]
            if not toks: continue
            has_topic = any(w in TOPIC for w in toks)
            if has_topic: topic_lines += 1
            tr = line.strip()
            if not tr.endswith("?") and is_falsifiable(toks):
                fals += 1
                if has_topic:
                    fals_topic += 1
                    if len(samples) < cap:
                        hit = sorted({w for w in toks if w in TOPIC})
                        samples.append({"topic": hit, "text": tr[:220]})
    import os
    mb = max(1, os.path.getsize(path)) / 1e6
    return {"lines": n_lines, "mb": round(mb, 3), "topic_lines": topic_lines,
            "fals_lines": fals, "fals_AND_topic": fals_topic,
            "fals_topic_per_mb": round(fals_topic / mb, 3),
            "fals_topic_pct_of_fals": round(100 * fals_topic / max(1, fals), 3),
            "samples": samples}

def main():
    hf = sys.argv[1]
    files = {"en-general": f"{hf}/en-general/anima-corpus-en-general.txt",
             "en-sns": f"{hf}/en-sns/anima-corpus-en-sns.txt"}
    per = {n: measure(p) for n, p in files.items()}
    tot_fals = sum(v["fals_lines"] for v in per.values())
    tot_ft = sum(v["fals_AND_topic"] for v in per.values())
    tot_mb = sum(v["mb"] for v in per.values())
    report = {
        "method": "G6 TARGETED coverage = _is_falsifiable(comp&meas) AND >=1 ideation-seed topic word (gauge_lib IDEATION_SEEDS+CONCEPTS VERBATIM)",
        "topic_words_n": len(TOPIC),
        "per_file": per,
        "aggregate_en": {"fals_lines": tot_fals, "fals_AND_topic": tot_ft,
                         "fals_topic_per_mb": round(tot_ft / max(1e-9, tot_mb), 4),
                         "fals_topic_pct_of_all_fals": round(100 * tot_ft / max(1, tot_fals), 3),
                         "mb": round(tot_mb, 2)},
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
