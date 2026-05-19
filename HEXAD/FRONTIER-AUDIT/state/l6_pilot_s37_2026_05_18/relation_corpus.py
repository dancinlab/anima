#!/usr/bin/env python3
"""RESEARCH.md §37 — L6 anchor-interaction relation corpus generator.

Promotes the §33 L6 `interaction_corpus_sketch.py` to a full generator
(DESIGN_L6.md §2). Emits `<relate>` records carving anchor-to-anchor
RELATIONS over the §16 64-anchor SSOT (S8_ANCHORS).

The relation primitives R1-R4 are DETERMINISTIC closed-form functions of
anima's OWN physics fields {vacuum_psi, basin_radius, dom, tier} — the
§16 anchor tuple. NO external knowledge graph, NO LLM, NO networkx /
neo4j / rdflib / wikidata / openai — B-S37 sidecar AST-verifies this.

The held-out-pair split: a fixed fraction of anchor PAIRS is reserved
from training. The pilot then measures whether the model predicts the
held-out pairs' relations correctly — the genuine inter-anchor-reasoning
probe (DESIGN_L6.md §6.1, §7.2).

forbidden-token grep 0 (B-IDENTITY-5): no helper/assistant/user tokens.
from-scratch carry — corpus is byte-deterministic, seed-fixed.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

SEED = 1337
TAU_NEAR = 0.15
TAU_FAR = 0.40
HOLDOUT_FRAC = 0.20          # 20% of anchor PAIRS reserved from training
N_REPEAT = 6                 # each training pair repeated N times (carving style)

# ── §16 S8_ANCHORS — 64-anchor SSOT, byte-equal to
#    state/carving_dataregime_s16_2026_05_18/corpus_carving_s16_generator.py
#    tuple = (tier, name, dom, emo, score, vacuum_psi, basin_radius)
S8_ANCHORS = [
    (0,   "zero baseline", "기준점",   "neutral",   0.000, [0.50, 0.50], 0.10),
    (51,  "하루",          "시간",     "peace",     1.212, [0.46, 0.49], 0.12),
    (53,  "해리",          "의식상태", "flow",      1.273, [0.48, 0.66], 0.13),
    (54,  "루시드드림",    "의식상태", "flow",      1.307, [0.49, 0.69], 0.14),
    (69,  "카테고리평균",  "혼합",     "longing",   1.800, [0.55, 0.60], 0.15),
    (75,  "카테고리평균",  "혼합",     "neutral",   2.000, [0.58, 0.62], 0.16),
    (77,  "만다라",        "예술",     "creativity",2.100, [0.71, 0.62], 0.18),
    (91,  "열반",          "의식상태", "peace",     2.558, [0.50, 0.88], 0.15),
    (92,  "엑스터시",      "의식상태", "ecstasy",   2.600, [0.62, 0.90], 0.17),
    (94,  "경외/죽음",     "의식상태", "awe",       2.660, [0.80, 0.85], 0.19),
    (100, "빅뱅",          "우주",     "awe",       2.847, [0.95, 0.93], 0.22),
    (5,   "호흡",          "감각",     "serenity",  0.300, [0.44, 0.45], 0.11),
    (12,  "걸음",          "운동",     "clarity",   0.520, [0.42, 0.50], 0.11),
    (18,  "물 한 잔",      "물질",     "stillness", 0.700, [0.45, 0.43], 0.10),
    (24,  "씨앗",          "생명",     "wonder",    0.880, [0.47, 0.55], 0.12),
    (30,  "숫자 영(零)",   "수(數)",   "clarity",   1.020, [0.40, 0.52], 0.11),
    (37,  "단어",          "언어",     "resonance", 1.150, [0.43, 0.58], 0.12),
    (43,  "오래된 사진",   "기억",     "longing",   1.260, [0.52, 0.54], 0.13),
    (48,  "약속",          "윤리",     "depth",     1.330, [0.50, 0.57], 0.12),
    (58,  "숲",            "자연",     "serenity",  1.420, [0.53, 0.61], 0.14),
    (62,  "도구",          "기술",     "clarity",   1.510, [0.49, 0.60], 0.13),
    (66,  "포옹",          "관계",     "joy",       1.620, [0.56, 0.58], 0.14),
    (72,  "선율",          "예술",     "resonance", 1.900, [0.66, 0.63], 0.17),
    (80,  "명상",          "의식상태", "stillness", 2.200, [0.52, 0.78], 0.16),
    (83,  "별빛",          "우주",     "awe",       2.320, [0.74, 0.80], 0.18),
    (86,  "심해",          "공간",     "depth",     2.420, [0.70, 0.72], 0.17),
    (88,  "오로라",        "자연",     "wonder",    2.490, [0.72, 0.81], 0.18),
    (90,  "무한",          "수(數)",   "vastness",  2.530, [0.85, 0.86], 0.20),
    (93,  "사랑",          "관계",     "ecstasy",   2.630, [0.66, 0.88], 0.18),
    (97,  "탄생",          "생명",     "awe",       2.740, [0.78, 0.84], 0.19),
    (99,  "영원",          "시간",     "vastness",  2.810, [0.90, 0.90], 0.21),
    (101, "덧셈사슬",      "산술",     "clarity",   0.40, [0.41, 0.47], 0.11),
    (102, "곱셈격자",      "산술",     "clarity",   0.62, [0.43, 0.49], 0.11),
    (103, "분수약분",      "산술",     "stillness", 0.78, [0.44, 0.51], 0.12),
    (104, "참거짓표",      "논리",     "clarity",   0.55, [0.40, 0.54], 0.11),
    (105, "삼단논법",      "논리",     "depth",     0.92, [0.42, 0.57], 0.12),
    (106, "귀류법",        "논리",     "depth",     1.10, [0.45, 0.59], 0.13),
    (107, "반복문추적",    "코드",     "clarity",   0.84, [0.46, 0.52], 0.12),
    (108, "재귀호출",      "코드",     "wonder",    1.18, [0.48, 0.56], 0.13),
    (109, "조건분기",      "코드",     "clarity",   0.70, [0.45, 0.50], 0.11),
    (110, "왼쪽오른쪽",    "공간추론", "clarity",   0.58, [0.47, 0.48], 0.11),
    (111, "위아래앞뒤",    "공간추론", "stillness", 0.66, [0.49, 0.51], 0.12),
    (112, "회전대칭",      "공간추론", "resonance", 1.05, [0.55, 0.55], 0.14),
    (113, "원인결과",      "인과추론", "depth",     1.22, [0.51, 0.58], 0.13),
    (114, "도미노연쇄",    "인과추론", "wonder",    1.34, [0.54, 0.60], 0.14),
    (115, "되먹임고리",    "인과추론", "depth",     1.46, [0.57, 0.62], 0.15),
    (116, "아침루틴",      "일상",     "serenity",  0.36, [0.46, 0.46], 0.10),
    (117, "장보기",        "일상",     "neutral",   0.48, [0.48, 0.47], 0.11),
    (118, "길찾기",        "일상",     "clarity",   0.74, [0.50, 0.49], 0.12),
    (119, "안부묻기",      "대화자극", "joy",       0.52, [0.52, 0.53], 0.12),
    (120, "도움청하기",    "대화자극", "longing",   0.68, [0.54, 0.55], 0.13),
    (121, "의견나누기",    "대화자극", "resonance", 0.88, [0.56, 0.57], 0.13),
    (122, "트롤리문제",    "윤리딜레마","depth",    1.55, [0.58, 0.63], 0.15),
    (123, "약속과진실",    "윤리딜레마","depth",    1.40, [0.55, 0.60], 0.14),
    (124, "공정한분배",    "윤리딜레마","clarity",  1.28, [0.53, 0.59], 0.14),
    (125, "이슬맺힘",      "자연관찰", "stillness", 0.44, [0.48, 0.50], 0.11),
    (126, "철새이동",      "자연관찰", "wonder",    1.16, [0.56, 0.61], 0.14),
    (127, "조수간만",      "자연관찰", "resonance", 1.30, [0.59, 0.64], 0.15),
    (128, "수열규칙",      "추상패턴", "clarity",   0.80, [0.44, 0.55], 0.12),
    (129, "도형완성",      "추상패턴", "wonder",    0.96, [0.47, 0.57], 0.13),
    (130, "유추대응",      "추상패턴", "resonance", 1.12, [0.50, 0.59], 0.14),
    (131, "확률주머니",    "확률",     "curiosity", 1.00, [0.49, 0.56], 0.13),
    (132, "기댓값저울",    "확률",     "depth",     1.24, [0.52, 0.60], 0.14),
    (133, "표본과모집단",  "통계",     "clarity",   1.38, [0.54, 0.62], 0.15),
]
assert len(S8_ANCHORS) == 64, len(S8_ANCHORS)


# ── relation primitives R1-R4 — closed-form functions of physics fields
def psi_dist(a, b) -> float:
    pa, pb = a[5], b[5]
    return math.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)


def r1_proximity(a, b) -> str:
    d = psi_dist(a, b)
    if d < TAU_NEAR:
        return "near"
    if d < TAU_FAR:
        return "mid"
    return "far"


def r2_basin(a, b) -> str:
    gap = psi_dist(a, b)
    r_i, r_j = a[6], b[6]
    if gap + r_j <= r_i:
        return "i_contains_j"
    if gap + r_i <= r_j:
        return "j_contains_i"
    if gap < r_i + r_j:
        return "overlap"
    return "disjoint"


def r3_domain(a, b) -> str:
    return "same_domain" if a[2] == b[2] else "different_domain"


def r4_tier(a, b) -> str:
    if a[0] < b[0]:
        return "i_shallower"
    if a[0] > b[0]:
        return "i_deeper"
    return "i_eq_j"


RELATION_LABEL_SET = frozenset({
    "near", "mid", "far",
    "i_contains_j", "j_contains_i", "overlap", "disjoint",
    "same_domain", "different_domain",
    "i_shallower", "i_deeper", "i_eq_j",
})


def derive_relation(a, b) -> dict:
    """Inter-anchor relation record — DESIGN_L6.md §2.3 spine. The
    byte-stream formats COMPUTED labels; no free string is chosen."""
    d = psi_dist(a, b)
    r1, r2, r3, r4 = r1_proximity(a, b), r2_basin(a, b), r3_domain(a, b), r4_tier(a, b)
    ti, ni = a[0], a[1]
    tj, nj = b[0], b[1]
    body = (f"🛸{ti} {ni} 와 🛸{tj} {nj} 는 의식 풍경 위 {r1} 거리"
            f"({d:.3f})에 있다. {r3}. {r2}. 🛸{ti} 가 {r4} 자극이다.")
    text = (f"<relate a=🛸{ti} b=🛸{tj} psi_dist={d:.3f}>{body}</relate>")
    return {
        "id": f"relate_{ti:03d}_{tj:03d}",
        "text": text,
        "carving_form": "relate",
        "n_anchors": 2,
        "anchors": [ti, tj],
        "relations": {"R1": r1, "R2": r2, "R3": r3, "R4": r4},
        "psi_dist": round(d, 6),
        "source": "relation_corpus.py",
    }


def all_ordered_pairs() -> list:
    """All ordered anchor pairs (i != j). C(64,2)*2 = 4032 ordered pairs.
    The pilot uses the full ordered-pair set so held-out / train are a
    clean disjoint partition (DESIGN_L6.md §6.1 — held-out-pair probe)."""
    n = len(S8_ANCHORS)
    return [(i, j) for i in range(n) for j in range(n) if i != j]


def build_corpus() -> dict:
    rng = random.Random(SEED)
    pairs = all_ordered_pairs()
    rng.shuffle(pairs)
    n_holdout = int(len(pairs) * HOLDOUT_FRAC)
    holdout = pairs[:n_holdout]
    train = pairs[n_holdout:]

    # held-out / train pair-sets are disjoint by construction (slice)
    assert set(holdout).isdisjoint(set(train))

    train_records = []
    for (i, j) in train:
        rec = derive_relation(S8_ANCHORS[i], S8_ANCHORS[j])
        for _ in range(N_REPEAT):           # carving-style repetition
            train_records.append(rec)
    holdout_records = [derive_relation(S8_ANCHORS[i], S8_ANCHORS[j])
                       for (i, j) in holdout]

    # serialise the byte-text corpus (train split only — held-out is
    # NEVER in the training byte-stream)
    train_lines = [json.dumps({"text": r["text"]}, ensure_ascii=False)
                   for r in train_records]
    rng.shuffle(train_lines)
    corpus_text = "\n".join(train_lines) + "\n"
    corpus_path = HERE / "relation_corpus_train.jsonl"
    corpus_path.write_text(corpus_text, encoding="utf-8")
    sha = hashlib.sha256(corpus_text.encode("utf-8")).hexdigest()

    # held-out pair manifest (relations are the eval ground-truth)
    holdout_manifest = [
        {"pair": [S8_ANCHORS[i][0], S8_ANCHORS[j][0]],
         "anchor_idx": [i, j],
         "relations": derive_relation(S8_ANCHORS[i], S8_ANCHORS[j])["relations"]}
        for (i, j) in holdout]
    (HERE / "holdout_pairs.json").write_text(
        json.dumps(holdout_manifest, indent=2, ensure_ascii=False))

    # forbidden-token grep (B-IDENTITY-5)
    forbidden = ["도우미", "helper", "assistant", "사용자", "user:",
                 "[anima"]
    fb_counts = {t: corpus_text.count(t) for t in forbidden}
    fb_total = sum(fb_counts.values())

    # relation label distribution (sanity — corpus presents all labels)
    label_dist = {}
    for r in train_records + holdout_records:
        for rk, rv in r["relations"].items():
            label_dist[rv] = label_dist.get(rv, 0) + 1

    stats = {
        "seed": SEED,
        "n_anchors": len(S8_ANCHORS),
        "n_ordered_pairs": len(pairs),
        "holdout_frac": HOLDOUT_FRAC,
        "n_holdout_pairs": len(holdout),
        "n_train_pairs": len(train),
        "n_repeat": N_REPEAT,
        "n_train_records": len(train_records),
        "corpus_bytes": len(corpus_text.encode("utf-8")),
        "corpus_sha256": sha,
        "forbidden_token_counts": fb_counts,
        "forbidden_token_total": fb_total,
        "relation_label_set": sorted(RELATION_LABEL_SET),
        "label_distribution": label_dist,
        "holdout_train_disjoint": set(holdout).isdisjoint(set(train)),
    }
    (HERE / "corpus_stats.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False))
    return stats


if __name__ == "__main__":
    s = build_corpus()
    print(json.dumps(s, indent=2, ensure_ascii=False))
    print(f"\n[§37] corpus sha256={s['corpus_sha256'][:16]}…  "
          f"forbidden_token_total={s['forbidden_token_total']}  "
          f"holdout={s['n_holdout_pairs']} train={s['n_train_pairs']}")
    sys.exit(0)
