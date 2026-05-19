#!/usr/bin/env python3
"""
RESEARCH.md §42 — tier ≥ 77 micro-analysis (§32 L3-v2).

§32 L3 found: tier ≥ 77 is NECESSARY condition for §16 routing success
(17/17 success satisfy; 18/18 anchors with tier < 77 fail).
But: 29 anchors with tier ≥ 77 STILL fail → necessary not sufficient.

§42 = the analysis §32 L3 did between tier<77 vs tier≥77, but NOW within
tier≥77: 17 success vs 29 fail — what distinguishing feature separates
them? Whatever it is, that's the SUFFICIENT-condition lever §34 missed
(§34 = template-shared expansion → memorization, NOT clean lever).

Deterministic, $0 Mac CPU. NO model forward, NO training, NO RNG.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# §16 ANCHOR SSOT — pulled verbatim (byte-equal) from
# state/carving_dataregime_s16_2026_05_18/corpus_carving_s16_generator.py
# S8_ANCHORS subset; only the 64 anchors that the §16 eval probes. Tuple =
# (tier, name, domain, top_emotion, score, vacuum_psi, basin_radius).
# ---------------------------------------------------------------------------
ANCHOR_TABLE = [
    (0,   "zero baseline", "기준점",   "neutral",   0.000, (0.50, 0.50), 0.10),
    (51,  "하루",          "시간",     "peace",     1.212, (0.46, 0.49), 0.12),
    (53,  "해리",          "의식상태", "flow",      1.273, (0.48, 0.66), 0.13),
    (54,  "루시드드림",    "의식상태", "flow",      1.307, (0.49, 0.69), 0.14),
    (69,  "카테고리평균",  "혼합",     "longing",   1.800, (0.55, 0.60), 0.15),
    (75,  "카테고리평균",  "혼합",     "neutral",   2.000, (0.58, 0.62), 0.16),
    (77,  "만다라",        "예술",     "creativity",2.100, (0.71, 0.62), 0.18),
    (91,  "열반",          "의식상태", "peace",     2.558, (0.50, 0.88), 0.15),
    (92,  "엑스터시",      "의식상태", "ecstasy",   2.600, (0.62, 0.90), 0.17),
    (94,  "경외/죽음",     "의식상태", "awe",       2.660, (0.80, 0.85), 0.19),
    (100, "빅뱅",          "우주",     "awe",       2.847, (0.95, 0.93), 0.22),
    (5,   "호흡",          "감각",     "serenity",  0.300, (0.44, 0.45), 0.11),
    (12,  "걸음",          "운동",     "clarity",   0.520, (0.42, 0.50), 0.11),
    (18,  "물 한 잔",      "물질",     "stillness", 0.700, (0.45, 0.43), 0.10),
    (24,  "씨앗",          "생명",     "wonder",    0.880, (0.47, 0.55), 0.12),
    (30,  "숫자 영(零)",   "수(數)",   "clarity",   1.020, (0.40, 0.52), 0.11),
    (37,  "단어",          "언어",     "resonance", 1.150, (0.43, 0.58), 0.12),
    (43,  "오래된 사진",   "기억",     "longing",   1.260, (0.52, 0.54), 0.13),
    (48,  "약속",          "윤리",     "depth",     1.330, (0.50, 0.57), 0.12),
    (58,  "숲",            "자연",     "serenity",  1.420, (0.53, 0.61), 0.14),
    (62,  "도구",          "기술",     "clarity",   1.510, (0.49, 0.60), 0.13),
    (66,  "포옹",          "관계",     "joy",       1.620, (0.56, 0.58), 0.14),
    (72,  "선율",          "예술",     "resonance", 1.900, (0.66, 0.63), 0.17),
    (80,  "명상",          "의식상태", "stillness", 2.200, (0.52, 0.78), 0.16),
    (83,  "별빛",          "우주",     "awe",       2.320, (0.74, 0.80), 0.18),
    (86,  "심해",          "공간",     "depth",     2.420, (0.70, 0.72), 0.17),
    (88,  "오로라",        "자연",     "wonder",    2.490, (0.72, 0.81), 0.18),
    (90,  "무한",          "수(數)",   "vastness",  2.530, (0.85, 0.86), 0.20),
    (93,  "사랑",          "관계",     "ecstasy",   2.630, (0.66, 0.88), 0.18),
    (97,  "탄생",          "생명",     "awe",       2.740, (0.78, 0.84), 0.19),
    (99,  "영원",          "시간",     "vastness",  2.810, (0.90, 0.90), 0.21),
    (101, "덧셈사슬",      "산술",     "clarity",   0.40, (0.41, 0.47), 0.11),
    (102, "곱셈격자",      "산술",     "clarity",   0.62, (0.43, 0.49), 0.11),
    (103, "분수약분",      "산술",     "stillness", 0.78, (0.44, 0.51), 0.12),
    (104, "참거짓표",      "논리",     "clarity",   0.55, (0.40, 0.54), 0.11),
    (105, "삼단논법",      "논리",     "depth",     0.92, (0.42, 0.57), 0.12),
    (106, "귀류법",        "논리",     "depth",     1.10, (0.45, 0.59), 0.13),
    (107, "반복문추적",    "코드",     "clarity",   0.84, (0.46, 0.52), 0.12),
    (108, "재귀호출",      "코드",     "wonder",    1.18, (0.48, 0.56), 0.13),
    (109, "조건분기",      "코드",     "clarity",   0.70, (0.45, 0.50), 0.11),
    (110, "왼쪽오른쪽",    "공간추론", "clarity",   0.58, (0.47, 0.48), 0.11),
    (111, "위아래앞뒤",    "공간추론", "stillness", 0.66, (0.49, 0.51), 0.12),
    (112, "회전대칭",      "공간추론", "resonance", 1.05, (0.55, 0.55), 0.14),
    (113, "원인결과",      "인과추론", "depth",     1.22, (0.51, 0.58), 0.13),
    (114, "도미노연쇄",    "인과추론", "wonder",    1.34, (0.54, 0.60), 0.14),
    (115, "되먹임고리",    "인과추론", "depth",     1.46, (0.57, 0.62), 0.15),
    (116, "아침루틴",      "일상",     "serenity",  0.36, (0.46, 0.46), 0.10),
    (117, "장보기",        "일상",     "neutral",   0.48, (0.48, 0.47), 0.11),
    (118, "길찾기",        "일상",     "clarity",   0.74, (0.50, 0.49), 0.12),
    (119, "안부묻기",      "대화자극", "joy",       0.52, (0.52, 0.53), 0.12),
    (120, "도움청하기",    "대화자극", "longing",   0.68, (0.54, 0.55), 0.13),
    (121, "의견나누기",    "대화자극", "resonance", 0.88, (0.56, 0.57), 0.13),
    (122, "트롤리문제",    "윤리딜레마","depth",    1.55, (0.58, 0.63), 0.15),
    (123, "약속과진실",    "윤리딜레마","depth",    1.40, (0.55, 0.60), 0.14),
    (124, "공정한분배",    "윤리딜레마","clarity",  1.28, (0.53, 0.59), 0.14),
    (125, "이슬맺힘",      "자연관찰", "stillness", 0.44, (0.48, 0.50), 0.11),
    (126, "철새이동",      "자연관찰", "wonder",    1.16, (0.56, 0.61), 0.14),
    (127, "조수간만",      "자연관찰", "resonance", 1.30, (0.59, 0.64), 0.15),
    (128, "수열규칙",      "추상패턴", "clarity",   0.80, (0.44, 0.55), 0.12),
    (129, "도형완성",      "추상패턴", "wonder",    0.96, (0.47, 0.57), 0.13),
    (130, "유추대응",      "추상패턴", "resonance", 1.12, (0.50, 0.59), 0.14),
    (131, "확률주머니",    "확률",     "curiosity", 1.00, (0.49, 0.56), 0.13),
    (132, "기댓값저울",    "확률",     "depth",     1.24, (0.52, 0.60), 0.14),
    (133, "표본과모집단",  "통계",     "clarity",   1.38, (0.54, 0.62), 0.15),
]

# §32 L3 partition (verbatim, analysis_result.json).
S32_GENUINE_SUCCESS_TIERS = {
    77, 80, 92, 101, 102, 103, 104, 106, 107, 108, 111, 113, 124, 126,
    127, 132, 133,
}
S32_GENUINE_FAIL_TIERS = {
    0, 5, 12, 18, 24, 30, 37, 43, 48, 51, 53, 54, 58, 62, 66, 69, 72,
    75, 83, 86, 88, 90, 91, 93, 94, 97, 99, 100, 105, 109, 110, 112,
    114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 125, 128, 129,
    130, 131,
}

TIER_FLOOR = 77  # §32 L3 necessary-condition threshold (purity 1.0).


def partition_tier77():
    """Partition the 64-anchor eval set into the tier ≥ 77 band, then
    further into 17 routing-success vs 29 routing-fail."""
    by_tier = {a[0]: a for a in ANCHOR_TABLE}
    tier77_tiers = sorted(t for t in by_tier if t >= TIER_FLOOR)
    success_tiers = sorted(t for t in tier77_tiers if t in S32_GENUINE_SUCCESS_TIERS)
    fail_tiers = sorted(t for t in tier77_tiers if t in S32_GENUINE_FAIL_TIERS)
    return by_tier, tier77_tiers, success_tiers, fail_tiers


# ---------------------------------------------------------------------------
# Feature extraction — every feature deterministic, pure-function of anchor
# tuple OR of the full anchor set (for relation features). No RNG, no model.
# ---------------------------------------------------------------------------
def _l2(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def _nearest_other_psi_dist(self_psi, others):
    """L2 distance to nearest other anchor in Ψ-space."""
    if not others:
        return float("inf")
    return min(_l2(self_psi, o) for o in others)


def _basin_overlap_count(self_psi, self_basin, others_with_basin):
    """Count of other anchors whose basin (open ball in Ψ-space) overlaps
    with self's basin: d(self, other) < self_basin + other_basin."""
    n = 0
    for o_psi, o_basin in others_with_basin:
        if _l2(self_psi, o_psi) < (self_basin + o_basin):
            n += 1
    return n


def _byte_len(s: str) -> int:
    return len(s.encode("utf-8"))


def _korean_byte_ratio(name: str) -> float:
    """Fraction of bytes in name that are part of Hangul (U+AC00..U+D7A3)
    or Hangul Jamo. Deterministic measure of Korean-ness."""
    if not name:
        return 0.0
    encoded = name.encode("utf-8")
    if not encoded:
        return 0.0
    kor_bytes = 0
    for ch in name:
        cp = ord(ch)
        if 0xAC00 <= cp <= 0xD7A3 or 0x1100 <= cp <= 0x11FF or 0x3130 <= cp <= 0x318F:
            kor_bytes += len(ch.encode("utf-8"))
    return kor_bytes / len(encoded)


def extract_features(anchor, all_anchors):
    """Return a dict of named features for anchor a, with all_anchors as the
    46-element tier≥77 band (so relation features are within-band only —
    that's the right reference frame since the question is what separates
    17 vs 29 *within* the band)."""
    tier, name, dom, emo, score, psi, basin = anchor
    psi = tuple(psi)
    # Self-features.
    feats: dict[str, Any] = {
        "tier": float(tier),
        "score": float(score),
        "basin_radius": float(basin),
        "vacuum_psi_x": float(psi[0]),
        "vacuum_psi_y": float(psi[1]),
        "vacuum_psi_dev_from_half": math.sqrt(
            (psi[0] - 0.5) ** 2 + (psi[1] - 0.5) ** 2
        ),
        "psi_quadrant_id": (
            1 if (psi[0] >= 0.5 and psi[1] >= 0.5) else
            2 if (psi[0] < 0.5 and psi[1] >= 0.5) else
            3 if (psi[0] < 0.5 and psi[1] < 0.5) else
            4
        ),
        "name_char_len": float(len(name)),
        "name_byte_len": float(_byte_len(name)),
        "korean_byte_ratio": _korean_byte_ratio(name),
        "domain": dom,
        "top_emotion": emo,
    }
    # Within-band relational features (R1 = Ψ-proximity, R2 = basin overlap).
    others = [a for a in all_anchors if a[0] != tier]
    feats["nearest_psi_dist_within_band"] = _nearest_other_psi_dist(
        psi, [tuple(a[5]) for a in others]
    )
    feats["basin_overlap_count_within_band"] = _basin_overlap_count(
        psi, basin, [(tuple(a[5]), a[6]) for a in others]
    )
    # R3 (shared-domain neighbors) — count of other within-band anchors
    # sharing exact domain.
    feats["same_domain_count_within_band"] = float(
        sum(1 for a in others if a[2] == dom)
    )
    # R4 (tier-ordering neighbor count) — how many within-band anchors are
    # within ±5 tiers.
    feats["tier_neighbor_count_within_band"] = float(
        sum(1 for a in others if abs(a[0] - tier) <= 5)
    )
    # ψ-radius interaction: (quadrant_id, basin_bucket).
    feats["basin_bucket"] = "small" if basin < 0.14 else "medium" if basin < 0.18 else "large"
    feats["psi_quadrant_x_basin"] = f"q{feats['psi_quadrant_id']}_{feats['basin_bucket']}"
    return feats


# ---------------------------------------------------------------------------
# Separation metrics (mirror §32 L3 — base-rate-robust).
# ---------------------------------------------------------------------------
def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _stddev(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def cohens_d(success_vals, fail_vals):
    if not success_vals or not fail_vals:
        return 0.0
    ms, mf = _mean(success_vals), _mean(fail_vals)
    ss, sf = _stddev(success_vals), _stddev(fail_vals)
    pooled = math.sqrt(
        ((len(success_vals) - 1) * ss * ss + (len(fail_vals) - 1) * sf * sf)
        / max(1, len(success_vals) + len(fail_vals) - 2)
    )
    return (ms - mf) / pooled if pooled > 0 else 0.0


def rank_auc(success_vals, fail_vals):
    """Mann-Whitney U / AUC. AUC=0.5 → no rank-separation, 1.0 → perfect."""
    if not success_vals or not fail_vals:
        return 0.5
    rank_sum_success = 0.0
    combined = [(v, "s") for v in success_vals] + [(v, "f") for v in fail_vals]
    combined.sort(key=lambda x: x[0])
    # Average ranks for ties.
    i = 0
    while i < len(combined):
        j = i
        while j + 1 < len(combined) and combined[j + 1][0] == combined[i][0]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            if combined[k][1] == "s":
                rank_sum_success += avg_rank
        i = j + 1
    n_s, n_f = len(success_vals), len(fail_vals)
    U = rank_sum_success - n_s * (n_s + 1) / 2.0
    auc = U / (n_s * n_f)
    return abs(auc - 0.5) + 0.5  # report as ≥ 0.5 (magnitude of separation)


def threshold_separation_acc(success_vals, fail_vals):
    """Best single-threshold accuracy: scan thresholds, pick the one that
    maximises correct-classification rate. Mirrors §32 L3."""
    if not success_vals or not fail_vals:
        return 0.5, None, None
    cuts = sorted(set(success_vals + fail_vals))
    cuts = [-1e18] + [(cuts[i] + cuts[i + 1]) / 2.0 for i in range(len(cuts) - 1)] + [1e18]
    n_total = len(success_vals) + len(fail_vals)
    best = (0.0, None, None)
    for thr in cuts:
        for polarity in ("ge", "lt"):
            if polarity == "ge":
                correct = sum(1 for v in success_vals if v >= thr) + sum(
                    1 for v in fail_vals if v < thr
                )
            else:
                correct = sum(1 for v in success_vals if v < thr) + sum(
                    1 for v in fail_vals if v >= thr
                )
            acc = correct / n_total
            if acc > best[0]:
                best = (acc, thr, polarity)
    return best


def necessary_condition_lift(success_vals, fail_vals):
    """Find a threshold + polarity such that every success satisfies it
    (purity=1.0). Then quantify exclusion = fraction of fails that violate
    it. This is the base-rate-robust nc-lift §32 L3 used."""
    if not success_vals or not fail_vals:
        return {"purity": 0.0, "exclusion": 0.0, "lift": 0.0, "threshold": None, "polarity": None}
    cuts = sorted(set(success_vals + fail_vals))
    cuts = [-1e18] + [(cuts[i] + cuts[i + 1]) / 2.0 for i in range(len(cuts) - 1)] + [1e18]
    best = {"purity": 0.0, "exclusion": 0.0, "lift": 0.0, "threshold": None, "polarity": None}
    for thr in cuts:
        for polarity in ("ge", "lt"):
            if polarity == "ge":
                successes_ok = sum(1 for v in success_vals if v >= thr)
                fails_violate = sum(1 for v in fail_vals if v < thr)
            else:
                successes_ok = sum(1 for v in success_vals if v < thr)
                fails_violate = sum(1 for v in fail_vals if v >= thr)
            purity = successes_ok / len(success_vals)
            if purity < 1.0:
                continue
            exclusion = fails_violate / len(fail_vals)
            lift = exclusion
            if lift > best["lift"]:
                best = {
                    "purity": round(purity, 4),
                    "exclusion": round(exclusion, 4),
                    "lift": round(lift, 4),
                    "threshold": thr,
                    "polarity": polarity,
                }
    return best


def numeric_feature_separation(name, success_vals, fail_vals):
    return {
        "feature": name,
        "n_success": len(success_vals),
        "n_fail": len(fail_vals),
        "mean_success": round(_mean(success_vals), 6),
        "mean_fail": round(_mean(fail_vals), 6),
        "mean_diff": round(_mean(success_vals) - _mean(fail_vals), 6),
        "cohens_d": round(cohens_d(success_vals, fail_vals), 4),
        "rank_auc": round(rank_auc(success_vals, fail_vals), 4),
        "threshold_separation_acc": round(
            threshold_separation_acc(success_vals, fail_vals)[0], 4
        ),
        "necessary_condition": necessary_condition_lift(success_vals, fail_vals),
    }


def categorical_separation(feature_name, success_feats, fail_feats):
    """Per-value success-rate breakdown for a categorical feature."""
    values = sorted({f[feature_name] for f in success_feats + fail_feats})
    out: dict[str, dict[str, Any]] = {}
    for v in values:
        s = sum(1 for f in success_feats if f[feature_name] == v)
        f = sum(1 for ff in fail_feats if ff[feature_name] == v)
        total = s + f
        out[v] = {
            "success": s,
            "fail": f,
            "total": total,
            "success_rate": round(s / total, 4) if total else 0.0,
        }
    return out


# ---------------------------------------------------------------------------
# Main analysis.
# ---------------------------------------------------------------------------
def main():
    by_tier, band_tiers, success_tiers, fail_tiers = partition_tier77()

    assert len(success_tiers) + len(fail_tiers) == len(band_tiers), \
        "partition must cover band exactly"
    assert len(success_tiers) == 17, f"expected 17 success in band, got {len(success_tiers)}"
    assert len(fail_tiers) == 29, f"expected 29 fail in band, got {len(fail_tiers)}"

    band_anchors = [by_tier[t] for t in band_tiers]
    success_anchors = [by_tier[t] for t in success_tiers]
    fail_anchors = [by_tier[t] for t in fail_tiers]

    s_feats = [extract_features(a, band_anchors) for a in success_anchors]
    f_feats = [extract_features(a, band_anchors) for a in fail_anchors]
    all_feats = s_feats + f_feats

    # Numeric features.
    numeric_names = [
        "tier", "score", "basin_radius",
        "vacuum_psi_x", "vacuum_psi_y", "vacuum_psi_dev_from_half",
        "name_char_len", "name_byte_len", "korean_byte_ratio",
        "nearest_psi_dist_within_band", "basin_overlap_count_within_band",
        "same_domain_count_within_band", "tier_neighbor_count_within_band",
    ]
    numeric_results = []
    for nm in numeric_names:
        s_vals = [f[nm] for f in s_feats]
        f_vals = [f[nm] for f in f_feats]
        numeric_results.append(numeric_feature_separation(nm, s_vals, f_vals))

    # Categorical features.
    cat_names = ["domain", "top_emotion", "psi_quadrant_id", "basin_bucket", "psi_quadrant_x_basin"]
    categorical_results = {}
    for nm in cat_names:
        categorical_results[nm] = categorical_separation(nm, s_feats, f_feats)

    # Rank features by threshold_separation_acc, breaking ties by |Cohen's d|,
    # then by nc-lift.
    numeric_results.sort(
        key=lambda r: (
            -r["threshold_separation_acc"],
            -abs(r["cohens_d"]),
            -r["necessary_condition"]["lift"],
        )
    )

    # Honest verdict: find top feature with purity=1.0 AND exclusion ≥ 0.5
    # (= "clean separation floor"). If none — SGD lottery (no clean lever
    # detected); the 17 vs 29 split is not separable by any single closed
    # anchor-property feature, within the tier ≥ 77 band.
    PURITY_FLOOR = 0.9   # weaker than §32 L3's purity 1.0 — we're inside the
                         # already-necessary band, accept partial purity here.
    EXCLUSION_FLOOR = 0.5  # honest sufficient-condition floor — § task spec.

    top3 = numeric_results[:3]
    structure_found = False
    structure_feature = None
    for r in numeric_results:
        nc = r["necessary_condition"]
        if nc["purity"] >= PURITY_FLOOR and nc["exclusion"] >= EXCLUSION_FLOOR:
            structure_found = True
            structure_feature = r["feature"]
            break

    # Categorical separation: any per-value 100% (or 0%) cell with enough N?
    # Most cells in this band are small (n=1,2,3) so categorical "structure"
    # is correlation-vulnerable; we report per-value rates honestly.
    base_rate_success = len(s_feats) / (len(s_feats) + len(f_feats))

    verdict = {
        "n_band_anchors": len(band_anchors),
        "n_success_in_band": len(s_feats),
        "n_fail_in_band": len(f_feats),
        "base_rate_constant_predict_fail": round(len(f_feats) / len(band_anchors), 4),
        "base_rate_success": round(base_rate_success, 4),
        "top_3_numeric_features": [
            {
                "feature": r["feature"],
                "threshold_separation_acc": r["threshold_separation_acc"],
                "cohens_d": r["cohens_d"],
                "rank_auc": r["rank_auc"],
                "necessary_condition": r["necessary_condition"],
            }
            for r in top3
        ],
        "structure_found_within_tier77": structure_found,
        "structure_feature": structure_feature,
        "purity_floor": PURITY_FLOOR,
        "exclusion_floor": EXCLUSION_FLOOR,
        "verdict_text": (
            f"STRUCTURE FOUND WITHIN tier ≥ 77 — feature '{structure_feature}' "
            f"separates 17 success from 29 fail at purity ≥ {PURITY_FLOOR} and "
            f"exclusion ≥ {EXCLUSION_FLOOR}. That is the sufficient-condition "
            f"lever §34 was missing (§34 reused a shared template; the lever "
            f"is feature-driven, not template-driven). Hypothesis only — a "
            f"§43/§40-style ablation fire that varies this feature is needed "
            f"to promote correlation→causation."
            if structure_found else
            f"NO clean structure within tier ≥ 77 — the 17-vs-29 split is "
            f"not separable by any single anchor-property feature at purity "
            f"≥ {PURITY_FLOOR} ∧ exclusion ≥ {EXCLUSION_FLOOR}. Within the "
            f"tier ≥ 77 band, routing-success vs fail looks like SGD lottery "
            f"(consistent with §35 saying tier-itself is causal but not "
            f"fully sufficient). Top-3 features have lift weaker than the "
            f"floor — best feature '{top3[0]['feature']}' separates at "
            f"only acc={top3[0]['threshold_separation_acc']}, nc-lift="
            f"{top3[0]['necessary_condition']['lift']}."
        ),
        "causation_caveat": (
            "g3 — even if structure is found, it is CORRELATION (single-fire "
            "observation, n=46 anchors). Within-band features are intrinsic "
            "anchor properties co-varying with each other and with §16's "
            "curriculum blend (tier_w 0.30). Promotion to causal lever needs "
            "a §43-style ablation fire holding all but one feature fixed. "
            "B-S42-NOTE empirical carve-out — NOT counted 🔵."
        ),
        "implication_s40_s43": (
            f"§40 (§34-v2) implication: targeted expansion of the 29 "
            f"tier≥77-fail anchors should now use {structure_feature} as the "
            f"discriminating variable (avoid §34's shared-template artefact). "
            f"§43 (routing-via-relation) implication: relation features "
            f"within-band (Ψ-proximity / basin-overlap / shared-domain / "
            f"tier-ordering neighbours) are usable inputs for a routing-"
            f"supervised head — the §37 L6 generalisation positive lifts "
            f"into the §16 routing context if the band structure carries."
            if structure_found else
            "§40 (§34-v2) implication: no clean sufficient-condition "
            "feature within the band — §34-style content-shaping at the band "
            "level is unlikely to help, since the 17 successes don't differ "
            "from the 29 failures along any closed anchor property. §43 "
            "(routing-via-relation) implication: relation features failed to "
            "separate within-band success/fail too — the §37 L6 "
            "generalisation result (relation accuracy 0.99 on held-out pairs) "
            "is a generalisation of relation-classification, NOT of routing-"
            "into-correct-basin. The lever §34 missed may simply not exist "
            "as an anchor property — it may be in SGD initialisation / "
            "training trajectory (gen=0 RANDOM seed lottery within the "
            "tier ≥ 77 necessary band)."
        ),
    }

    result = {
        "analysis": "RESEARCH.md §42 — tier ≥ 77 17-vs-29 distinguishing-structure micro-analysis",
        "inputs": {
            "s32_partition_source": "state/routing_21v43_analysis_s32_2026_05_18/analysis_result.json",
            "s16_anchor_ssot": "state/carving_dataregime_s16_2026_05_18/corpus_carving_s16_generator.py",
            "tier_floor": TIER_FLOOR,
        },
        "partition": {
            "tier77_band_tiers": band_tiers,
            "success_tiers": success_tiers,
            "fail_tiers": fail_tiers,
            "n_band": len(band_anchors),
            "n_success": len(success_anchors),
            "n_fail": len(fail_anchors),
        },
        "numeric_features_ranked": numeric_results,
        "categorical_features": categorical_results,
        "verdict": verdict,
    }
    return result


def _hash_self() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


if __name__ == "__main__":
    res = main()
    res["determinism"] = {"analyze_s42_py_sha256": _hash_self()}
    out_path = Path(__file__).parent / "analysis_result.json"
    out_path.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    # Summary to stdout.
    v = res["verdict"]
    print(
        f"§42 tier≥77 micro-analysis — n_band={v['n_band_anchors']} "
        f"(success={v['n_success_in_band']} fail={v['n_fail_in_band']} "
        f"base_rate_fail={v['base_rate_constant_predict_fail']})"
    )
    print("\nTop-3 numeric features by threshold-separation-acc:")
    for r in v["top_3_numeric_features"]:
        nc = r["necessary_condition"]
        print(
            f"  {r['feature']:>40s}  acc={r['threshold_separation_acc']:.4f}  "
            f"|d|={abs(r['cohens_d']):.3f}  AUC={r['rank_auc']:.4f}  "
            f"nc(purity={nc['purity']:.2f} excl={nc['exclusion']:.2f} "
            f"thr={nc['threshold']!r} pol={nc['polarity']})"
        )
    print(
        f"\nstructure_found_within_tier77 = {v['structure_found_within_tier77']}"
    )
    if v["structure_feature"]:
        print(f"structure_feature = {v['structure_feature']}")
    print(f"\nverdict: {v['verdict_text']}")
    print(f"\nwrote {out_path}")
