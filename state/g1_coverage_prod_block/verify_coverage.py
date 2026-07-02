#!/usr/bin/env python3
"""H_6185 처방 (2) — 생성 코퍼스의 조합-커버리지 verify (독립 재측정).

design.json 을 '설계 의도'로만 읽되, 커버리지 수치는 corpus/en_block.txt·ko_block.txt 를
전수 스캔해 *실측*한다 (design.json 을 신뢰하지 않고 실제 라인 co-occurrence 로 재확인).

측정:
  - 각 라인에서 등장하는 개념 토큰 집합을 찾아 그 안의 모든 쌍 co-occurrence 를 센다.
    (ko/en 은 별도, 그다음 합산. 개념 vocab 은 상호 substring-free 라 plain 매칭 안전.)
  - COVERED 쌍 = corpus 에 ≥1 회 등장한 쌍. HELD-OUT 쌍 = design 이 영구 미노출로 지정한 40쌍.
  - 판정:
      (1) 커버리지 = |actually-covered ∩ POOL| / |POOL|  ≥ 임계 ~20% 인가
      (2) HELD-OUT 40쌍 실측 co-occurrence == 0 인가 (gate-내부 10쌍 포함)
      (3) 커버된 쌍당 reps ≥ 30 (bar) 인가 (min/median)
      (4) control 일반쌍(개념 vocab 밖 단어) co-occurrence == 0 인가 (설계 오염 없음)
  - 밀도 = pair-lines / MB (toy HIGH arm 17,143 pair-lines/MB 급 목표).

torch 미사용. 결정적. 산출: verify_results.json (stdout 요약 + 파일).
"""
import json
import os
import re
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
design = json.load(open(os.path.join(HERE, "design.json"), encoding="utf-8"))

C_EN = design["concepts_en"]
C_KO = design["concepts_ko"]
N = design["N_concepts"]
HELD = {tuple(p) for p in design["held_out"]}
GATE_INTERNAL = {tuple(p) for p in design["held_out_gate_internal"]}
POOL_designed = {tuple(p) for p in design["covered_pairs"]}  # 설계상 커버 대상
allpairs = set(combinations(range(N), 2))
POOL = allpairs - HELD  # 커버 후보 (740)


def scan(path, concepts):
    """파일 전수 스캔 → 쌍별 라인-co-occurrence 카운트 (실측)."""
    # 개념 토큰 매칭: 영어는 단어경계 \b, 한국어는 plain substring (substring-free 보장됨).
    is_ko = any(ord(c[0]) > 0x3000 for c in concepts)
    if is_ko:
        pats = [(idx, tok) for idx, tok in enumerate(concepts)]
    else:
        pats = [(idx, re.compile(r"\b%s\b" % re.escape(tok))) for idx, tok in enumerate(concepts)]
    pair_cnt = {}
    nlines = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            nlines += 1
            if is_ko:
                present = [idx for idx, tok in pats if tok in line]
            else:
                present = [idx for idx, rx in pats if rx.search(line)]
            for a, b in combinations(sorted(present), 2):
                pair_cnt[(a, b)] = pair_cnt.get((a, b), 0) + 1
    return pair_cnt, nlines


en_cnt, en_lines = scan(os.path.join(HERE, "corpus/en_block.txt"), C_EN)
ko_cnt, ko_lines = scan(os.path.join(HERE, "corpus/ko_block.txt"), C_KO)

# 합산 (같은 개념 인덱스 = 같은 개념, en+ko 언어횡단 합산)
total = {}
for d in (en_cnt, ko_cnt):
    for p, c in d.items():
        total[p] = total.get(p, 0) + c

covered_actual = {p for p, c in total.items() if c > 0}
covered_in_pool = covered_actual & POOL
coverage_frac = len(covered_in_pool) / len(POOL)

# HELD-OUT 유출 검사
held_leak = {f"{p}": total[p] for p in HELD if total.get(p, 0) > 0}
gate_leak = {f"{p}": total[p] for p in GATE_INTERNAL if total.get(p, 0) > 0}

# reps 분포 (커버된 쌍당)
reps = sorted(total[p] for p in covered_in_pool)
reps_min = reps[0] if reps else 0
reps_med = reps[len(reps) // 2] if reps else 0
reps_max = reps[-1] if reps else 0

# 설계 vs 실측 일치 (실측 covered_in_pool 이 설계 POOL_designed 와 같아야)
matches_design = covered_in_pool == POOL_designed

# control 일반쌍: 개념 vocab 밖 단어쌍이 코퍼스에 있으면 오염. 대표 control 3쌍 grep.
CONTROLS = [("government", "war"), ("music", "school"), ("water", "city")]
ctrl_hits = {}
with open(os.path.join(HERE, "corpus/en_block.txt"), encoding="utf-8") as f:
    txt = f.read()
for a, b in CONTROLS:
    ra = re.compile(r"\b%s\b" % a)
    rb = re.compile(r"\b%s\b" % b)
    ctrl_hits[f"{a}×{b}"] = sum(1 for ln in txt.splitlines() if ra.search(ln) and rb.search(ln))

# 밀도: pair-lines / MB
total_bytes = os.path.getsize(os.path.join(HERE, "corpus/en_block.txt")) + \
    os.path.getsize(os.path.join(HERE, "corpus/ko_block.txt"))
total_mb = total_bytes / 1e6
pair_lines = en_lines + ko_lines  # 각 라인이 정확히 1 pair 표현 (설계)
density = pair_lines / total_mb

THRESH = 0.20
verdict = {
    "N_concepts": N,
    "pairs_total": len(allpairs),
    "held_out_n": len(HELD),
    "pool_n": len(POOL),
    "coverage": {
        "covered_pairs_in_pool": len(covered_in_pool),
        "coverage_frac_of_pool": round(coverage_frac, 4),
        "threshold": THRESH,
        "CROSSES_THRESHOLD": coverage_frac >= THRESH,
        "matches_design_covered_set": matches_design,
    },
    "held_out_isolation": {
        "held_leak_pairs": held_leak,
        "held_leak_count": len(held_leak),
        "HELD_OUT_ZERO": len(held_leak) == 0,
        "gate_internal_leak": gate_leak,
        "GATE_INTERNAL_ZERO": len(gate_leak) == 0,
    },
    "reps_per_covered_pair": {
        "min": reps_min, "median": reps_med, "max": reps_max,
        "bar": 30, "ABOVE_BAR": reps_min >= 30,
    },
    "control_general_pairs": {
        "hits": ctrl_hits,
        "CONTROL_ZERO": all(v == 0 for v in ctrl_hits.values()),
    },
    "density": {
        "total_MB": round(total_mb, 3),
        "en_MB": round(os.path.getsize(os.path.join(HERE, "corpus/en_block.txt")) / 1e6, 3),
        "ko_MB": round(os.path.getsize(os.path.join(HERE, "corpus/ko_block.txt")) / 1e6, 3),
        "pair_lines": pair_lines,
        "pair_lines_per_MB": round(density, 0),
        "toy_HIGH_ref_per_MB": 17143,
    },
    "PASS": bool(
        coverage_frac >= THRESH
        and len(held_leak) == 0
        and reps_min >= 30
        and all(v == 0 for v in ctrl_hits.values())
    ),
}

json.dump(verdict, open(os.path.join(HERE, "verify_results.json"), "w"),
          ensure_ascii=False, indent=1)
print(json.dumps(verdict, ensure_ascii=False, indent=1))
