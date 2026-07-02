#!/usr/bin/env python3
"""H_6185 follow-on: 정확한 HF 4칸 production 코퍼스에서 G1 개념쌍 조합-커버리지 재측정.

방법 = H_6185 (state/g1_prod_corpus_density/FABLE_REPORT.md) 와 동일 reference-match:
  - 개념쌍 = G1 gate frozen CONCEPTS (tool/gauge_lib.py:76, H_1129 VERBATIM) 5세트 → 10쌍
  - HEAD-tier: 개념 헤드어(consciousness · tension · memory · silence · dream|engine)
    라인-window 공동출현, \\b 단어경계, case-insensitive  [본판정]
  - ±5라인 window 확장 (HEAD-tier)
  - FULL-tier: 세트 4키워드 전부(any-of A ∧ any-of B) 라인-window [관대한 상한]
  - control 일반쌍 3개: government×war · music×(school|history) · water×(city|energy)
  - 정직 체크: silence 프랑스어("le silence") 오염 분리 — 영어 문맥만 유효

코퍼스 = HF dancinlab/anima-corpus-{ko,en}-{general,sns} (exact production 4칸)
대조   = 로컬 프록시 trainset 3파일 (H_6185 원측정 재현)

사용: python3 measure_hf_exact.py <hf_corpus_dir> <proxy_trainset_dir> > results.json
"""
import json
import re
import sys

# G1 gate frozen CONCEPTS — tool/gauge_lib.py:76 (H_1129 VERBATIM)
CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness", "cells", "mind", "aware"}),
    ("tension ripples between distant minds", {"tension", "ripple", "distant", "between"}),
    ("memory composes into new meaning",      {"memory", "meaning", "compose", "new"}),
    ("silence still carries information",     {"silence", "information", "quiet", "carries"}),
    ("the engine dreams when alone",          {"dream", "engine", "alone", "sleep"}),
]
HEADS = ["consciousness", "tension", "memory", "silence", "dream|engine"]

CONTROLS = [("government", "war"), ("music", "school|history"), ("water", "city|energy")]

WINDOW = 5  # ±5라인 확장


def rx(alt):
    return re.compile(r"\b(?:%s)\b" % alt, re.IGNORECASE)


def rx_set(kws):
    return re.compile(r"\b(?:%s)\b" % "|".join(sorted(kws)), re.IGNORECASE)


FRENCH_HINT = re.compile(
    r"\b(le|la|les|des|une|un|dans|est|pour|que|qui|avec|sur|pas|plus|dans)\b"
)


def measure_file(path):
    """한 파일에서 모든 카운트를 단일 패스로 수집."""
    head_rx = [rx(h) for h in HEADS]
    full_rx = [rx_set(kws) for _s, kws in CONCEPTS]
    ctrl_rx = [(rx(a), rx(b)) for a, b in CONTROLS]

    n = len(HEADS)
    marg = [0] * n
    pair_line = {}       # HEAD-tier 같은 라인
    pair_win = {}        # HEAD-tier ±5라인
    full_line = {}       # FULL-tier 같은 라인
    ctrl_line = [0] * len(CONTROLS)
    for i in range(n):
        for j in range(i + 1, n):
            pair_line[(i, j)] = 0
            pair_win[(i, j)] = 0
            full_line[(i, j)] = 0
    last_seen = [-10**9] * n     # head i 가 마지막으로 나온 라인번호
    silence_lines = {"total": 0, "french_hint": 0, "english_ctx": 0, "samples": []}
    sil_rx = rx("silence")
    n_lines = 0

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f):
            n_lines += 1
            hits = [bool(r.search(line)) for r in head_rx]
            fhits = [bool(r.search(line)) for r in full_rx]
            for i in range(n):
                if hits[i]:
                    marg[i] += 1
            for i in range(n):
                for j in range(i + 1, n):
                    if hits[i] and hits[j]:
                        pair_line[(i, j)] += 1
                    if fhits[i] and fhits[j]:
                        full_line[(i, j)] += 1
            # ±WINDOW 라인: hit 시점에 상대 head 의 최근 출현과의 거리로 판정
            for i in range(n):
                if hits[i]:
                    for j in range(n):
                        if j != i and lineno - last_seen[j] <= WINDOW:
                            a, b = min(i, j), max(i, j)
                            pair_win[(a, b)] += 1
                    last_seen[i] = lineno
            for k, (ra, rb) in enumerate(ctrl_rx):
                if ra.search(line) and rb.search(line):
                    ctrl_line[k] += 1
            if sil_rx.search(line):
                silence_lines["total"] += 1
                if FRENCH_HINT.search(line):
                    silence_lines["french_hint"] += 1
                else:
                    silence_lines["english_ctx"] += 1
                    if len(silence_lines["samples"]) < 5:
                        silence_lines["samples"].append(line.strip()[:160])
    return {
        "lines": n_lines,
        "marginals": dict(zip(HEADS, marg)),
        "head_pair_line": {f"{HEADS[i]}×{HEADS[j]}": v for (i, j), v in pair_line.items()},
        "head_pair_win5": {f"{HEADS[i]}×{HEADS[j]}": v for (i, j), v in pair_win.items()},
        "full_pair_line": {f"C{i+1}×C{j+1}": v for (i, j), v in full_line.items()},
        "controls": {f"{a}×{b}": ctrl_line[k] for k, (a, b) in enumerate(CONTROLS)},
        "silence_audit": silence_lines,
    }


def agg(results):
    """파일별 결과 합산."""
    out = {"lines": 0, "marginals": {}, "head_pair_line": {}, "head_pair_win5": {},
           "full_pair_line": {}, "controls": {}}
    for r in results.values():
        out["lines"] += r["lines"]
        for key in ("marginals", "head_pair_line", "head_pair_win5",
                    "full_pair_line", "controls"):
            for k, v in r[key].items():
                out[key][k] = out[key].get(k, 0) + v
    return out


def main():
    hf_dir, proxy_dir = sys.argv[1], sys.argv[2]
    hf_files = {
        "en-general": f"{hf_dir}/en-general/anima-corpus-en-general.txt",
        "ko-general": f"{hf_dir}/ko-general/anima-corpus-ko-general.txt",
        "en-sns": f"{hf_dir}/en-sns/anima-corpus-en-sns.txt",
        "ko-sns": f"{hf_dir}/ko-sns/anima-corpus-ko-sns.txt",
    }
    proxy_files = {  # H_6185 원측정과 동일한 3파일
        "wiki_backbone_5lang_v2": f"{proxy_dir}/wiki_backbone_5lang_v2.txt",
        "corpus_enrichment_5lang": f"{proxy_dir}/corpus_enrichment_5lang.txt",
        "persona_sns_corpus": f"{proxy_dir}/persona_sns_corpus.txt",
    }
    hf_res = {name: measure_file(p) for name, p in hf_files.items()}
    proxy_res = {name: measure_file(p) for name, p in proxy_files.items()}
    report = {
        "method": "H_6185 reference-match (HEAD-tier line-window + ±5 window + FULL-tier + controls)",
        "hf_exact": {"per_file": hf_res, "aggregate": agg(hf_res)},
        "proxy_h6185": {"per_file": proxy_res, "aggregate": agg(proxy_res)},
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
