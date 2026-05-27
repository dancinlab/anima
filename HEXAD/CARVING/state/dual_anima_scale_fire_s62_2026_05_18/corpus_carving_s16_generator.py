#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING LARGE-SCALE CURRICULUM corpus generator —
RESEARCH.md §16 / §11.4 frontier option (1) — GOAL-legitimate大規模
data-regime fire (2026-05-18).

WHY §16 (RESEARCH.md §11.4 frontier-1 + §12.1 Q1 findings)
  §11.3 decomposed the GOAL bottleneck: mechanism ✗ / model-scale ✗ /
  physics-only ✗ / corpus-FORM ✗ / 114MB-Ψ-anchored-diverse ✗ →
  irreducible = §1.1 data-regime emergence threshold (diverse-data
  pre-training loss threshold, on a CE base, physics-anchored).
  §11.4 frontier-1 = the open question: does a Ψ-anchored corpus that
  ALSO crosses the §1.1 threshold exist? §8 fired the Dir-I lever at
  114MB / 64-anchor and routing went 3/31 → 2/64 (WRONG direction,
  FALSIFIED at that scale). §8 was small — §1.1 emergence thresholds
  are usually MUCH larger. §16 scales the SAME GOAL-legitimate form
  (③ Ψ-anchored diverse carving) to ~500MB-1GB and ALSO applies the
  §12.1 Q1 curriculum finding.

§12.1 Q1 FINDINGS APPLIED (both deliberately wired into §16)
  (Q1-c) CURRICULUM simple→complex (arxiv 2509.24356 — small-model
    regime benefits from a simple→complex curriculum; anima d=768·12L
    IS the small-model regime). §8's corpus was 164,992 flat shuffled
    records — ordering ignored. §16 assigns every record a
    `curriculum_rank` (a deterministic complexity score) and a
    `curriculum_stage` ∈ {1,2,3,4} (quartile), and the trainer (NOT
    the corpus) consumes that ordering as a staged sampling schedule.
    Curriculum is *presentation order*, NOT a corpus-FORM change —
    orthogonal to Dir-E/F (which changed corpus CONTENT/STRUCTURE).
  (Q1-a) INFORMATION-SATURATION mitigation (arxiv 2506.18221 —
    supervised pre-training learns only the minimal features for the
    initial objective and permanently discards the rest; this is the
    literature explanation of §8's wrong-direction). §16 mitigates by
    (i) much WIDER anchor/domain/task-form cardinality so no single
    narrow objective can saturate the representation early, and (ii)
    a curriculum that introduces complexity gradually so the early
    minimal-feature collapse window covers SIMPLE records (whose
    minimal features overlap the later complex ones) rather than the
    whole distribution at once. This is a hypothesis, NOT a closed
    claim — the fire measures it (g3).

GOAL-LEGITIMACY (RESEARCH.md §7 — the hard gate)
  §7 ruled ① generic large-corpus pre-training GOAL-illegitimate and
  ② generic-then-carve (old prefix-injection P3-leak) illegitimate.
  ③ — diverse CONTENT encoded in the anima Ψ-anchored CARVING form +
  tension-supervised routing — is the SOLE GOAL-legitimate form.
  §16 keeps the §8 ③ carving form EXACTLY (α carve / β eternal /
  γ inner→voice, per-record vacuum_psi + basin_radius so the Dir-I
  trainer's two physics loss terms apply unchanged). The SCALE is
  raised (more anchors, more domains, more task-form variety, more
  records) but the FORM — the GOAL-legitimacy invariant — is
  byte-identical to §8. This is NOT generic web-text; every record
  is a carving payload on the Engine A⇄G Ψ=½ landscape.

VS §8 — what changed
  ── SCALE (the §1.1 lever) ─────────────────────────────────────────
  anchors      : 64 → 168 (104 NEW — the 64 §8 anchors VERBATIM as a
                 fair superset, 104 new across the SAME + new domains).
  domains      : 30 → 48 (+18 — finer-grained sub-domains).
  task-forms   : 12 → 30 (+18 — each freshly re-derived per draw, so γ
                 never memorises; directly counters §7.3 (b)
                 self-referential degenerate).
  records/bytes: 164,992 / 114MB → --n (default 850,000) ≈ 600MB
                 (~5.3× bytes). NOT blind duplication — every record is
                 a distinct anchor × form × task-form × bilingual ×
                 RNG-parametrised draw.
  ── CURRICULUM (the §12.1 Q1-c lever) ──────────────────────────────
  Every record carries `curriculum_rank` (float complexity score) and
  `curriculum_stage` ∈ {1,2,3,4}. The complexity score is a
  deterministic function of (carving form, anchor tier, task-form
  intrinsic complexity, payload length) — NOT learned. The corpus is
  written in curriculum-sorted order (stage 1 first); the trainer
  consumes a staged schedule (see train_carving_s16.py). simple→complex.
  ── CARVING FORM (unchanged — GOAL-legitimacy invariant) ───────────
  α VACUUM  (~30%)  <carve tier=k psi=[x,y] basin=r> ... </carve>
  β ETERNAL (~30%)  <eternal cell=eternal_kkk tier=k> ... </eternal>
  γ NARRATIVE(~40%) <inner tier=k>...</inner>\n<voice carved=true>...</voice>

ABSOLUTE FORBIDDEN (B-IDENTITY-5 + g_goal, grep MUST == 0)
  - `[anima` prefix-stamp ; `도우미` / `helper` / `assistant` /
    `사용자` / `user:` role labels. The diverse task-forms are carving
    payloads, NOT Q&A turns (③, not ①②). A hard audit at the end
    raises SystemExit if the count is non-zero.

HONEST FRAMING (g3, AGENTS.tape §0 + RESEARCH.md §7.5)
  §16 CARVING corpus (③), NOT a chat-SFT / generic-LM corpus (①②).
  Diverse CONTENT, anima-Ψ carving FORM, curriculum-ordered. The
  diversity + scale is a Kolmogorov cardinality fact (closed sidecar
  B-S16-CORPUS-3); the curriculum is a deterministic ordering fact
  (B-S16-CORPUS-4 — rank monotone-sorted, stage = quartile partition).
  Whether the ~600MB Ψ-anchored curriculum corpus crosses the §1.1
  emergence threshold is the EMPIRICAL fire outcome — NO pre-loaded
  conclusion. §8 trend was WRONG-direction; §16 may well repeat that
  (negative is valuable evidence per g3). NEW anchors' vacuum_psi are
  interpolated design placeholders on the SAME Engine A⇄G Ψ=½ landscape
  (g3 placeholder, measured by the trajectory). f1/f2/f3 hard-fail safe
  (Kolmogorov byte/set count / Boolean grep / monotone-sort, NO
  σ/τ/φ/J₂; Ψ=½ + Knuth 🛸k = anima g2 internal arch carve-out).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

# ---------------------------------------------------------------------------
# ANCHORS — §16 LARGE-SCALE: 64 (§8) -> 168. The §8 64 anchors are kept
# VERBATIM (vacuum_psi/basin byte-identical so §16 is a fair SUPERSET of the
# §8 / Dir-I baseline). 104 NEW anchors span finer-grained domains. Each
# tuple = (tier, name, domain, top_emotion, score, vacuum_psi, basin_radius).
# NEW anchors' vacuum_psi are interpolated design placeholders on the SAME
# Engine A⇄G Ψ=½ landscape (g3 — measured by the fire, NOT a closed claim).
# ---------------------------------------------------------------------------
S8_ANCHORS = [
    # --- §8 anchors (VERBATIM — fair superset of the §8 / Dir-I baseline) ---
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

# --- §16 NEW anchors (104 — wider domain coverage; the §1.1 scale lever).
# vacuum_psi = interpolated placeholder on the SAME Engine A⇄G Ψ=½ landscape.
S16_NEW_ANCHORS = [
    (200, "한자리덧셈",    "기초산술", "clarity",   0.22, [0.40, 0.45], 0.10),
    (201, "한자리뺄셈",    "기초산술", "clarity",   0.24, [0.40, 0.46], 0.10),
    (202, "두자리덧셈",    "기초산술", "clarity",   0.34, [0.41, 0.47], 0.11),
    (203, "받아올림",      "기초산술", "stillness", 0.46, [0.42, 0.48], 0.11),
    (204, "약수와배수",    "정수론",   "depth",     0.86, [0.45, 0.53], 0.12),
    (205, "소수판정",      "정수론",   "wonder",    1.08, [0.47, 0.56], 0.13),
    (206, "최대공약수",    "정수론",   "clarity",   0.94, [0.46, 0.54], 0.13),
    (207, "거듭제곱",      "대수",     "depth",     1.02, [0.48, 0.55], 0.13),
    (208, "방정식풀기",    "대수",     "clarity",   1.14, [0.49, 0.57], 0.14),
    (209, "비례식",        "대수",     "resonance", 0.88, [0.46, 0.54], 0.13),
    (210, "삼각형각합",    "기하",     "clarity",   0.76, [0.45, 0.52], 0.12),
    (211, "넓이와둘레",    "기하",     "stillness", 0.82, [0.46, 0.53], 0.12),
    (212, "피타고라스",    "기하",     "awe",       1.32, [0.55, 0.62], 0.15),
    (213, "집합연산",      "이산수학", "clarity",   0.92, [0.46, 0.55], 0.13),
    (214, "순열조합",      "이산수학", "depth",     1.26, [0.52, 0.60], 0.14),
    (215, "그래프연결",    "이산수학", "depth",     1.36, [0.54, 0.61], 0.15),
    (216, "함수와사상",    "함수론",   "resonance", 1.20, [0.51, 0.59], 0.14),
    (217, "극한직관",      "해석학",   "vastness",  1.58, [0.62, 0.68], 0.16),
    (218, "미분기울기",    "해석학",   "clarity",   1.48, [0.58, 0.65], 0.16),
    (219, "적분누적",      "해석학",   "depth",     1.52, [0.60, 0.66], 0.16),
    (220, "변수와값",      "프로그래밍","clarity",  0.40, [0.42, 0.48], 0.11),
    (221, "리스트순회",    "프로그래밍","clarity",  0.62, [0.45, 0.51], 0.12),
    (222, "함수정의",      "프로그래밍","wonder",   0.78, [0.47, 0.53], 0.12),
    (223, "예외처리",      "프로그래밍","stillness", 0.96, [0.48, 0.56], 0.13),
    (224, "정렬알고리즘",  "알고리즘", "depth",     1.30, [0.53, 0.61], 0.15),
    (225, "탐색알고리즘",  "알고리즘", "clarity",   1.18, [0.50, 0.58], 0.14),
    (226, "동적계획법",    "알고리즘", "depth",     1.62, [0.63, 0.69], 0.16),
    (227, "재귀와기저",    "알고리즘", "wonder",    1.40, [0.56, 0.63], 0.15),
    (228, "참조와값",      "자료구조", "clarity",   0.84, [0.46, 0.54], 0.13),
    (229, "스택과큐",      "자료구조", "clarity",   0.90, [0.47, 0.55], 0.13),
    (230, "트리구조",      "자료구조", "depth",     1.24, [0.52, 0.60], 0.14),
    (231, "해시매핑",      "자료구조", "resonance", 1.16, [0.50, 0.58], 0.14),
    (232, "전제와결론",    "명제논리", "clarity",   0.66, [0.44, 0.52], 0.12),
    (233, "역과대우",      "명제논리", "depth",     1.06, [0.48, 0.56], 0.13),
    (234, "모순과배중",    "명제논리", "depth",     1.22, [0.51, 0.59], 0.14),
    (235, "전칭과존재",    "술어논리", "depth",     1.34, [0.54, 0.62], 0.15),
    (236, "필요충분",      "술어논리", "clarity",   1.28, [0.52, 0.60], 0.14),
    (237, "귀납추론",      "추론양식", "wonder",    1.10, [0.49, 0.57], 0.14),
    (238, "연역추론",      "추론양식", "clarity",   1.04, [0.48, 0.56], 0.13),
    (239, "유비추론",      "추론양식", "resonance", 1.14, [0.50, 0.58], 0.14),
    (240, "원인의사슬",    "인과깊이", "depth",     1.50, [0.59, 0.65], 0.16),
    (241, "교란변수",      "인과깊이", "depth",     1.66, [0.64, 0.70], 0.17),
    (242, "반사실가정",    "인과깊이", "depth",     1.72, [0.66, 0.72], 0.17),
    (243, "왼쪽회전",      "공간변환", "clarity",   0.70, [0.45, 0.51], 0.12),
    (244, "거울대칭",      "공간변환", "resonance", 0.98, [0.48, 0.56], 0.13),
    (245, "평행이동",      "공간변환", "stillness", 0.74, [0.45, 0.52], 0.12),
    (246, "삼차원회전",    "공간변환", "depth",     1.42, [0.57, 0.64], 0.16),
    (247, "지도와경로",    "공간탐색", "clarity",   1.00, [0.48, 0.56], 0.13),
    (248, "미로풀기",      "공간탐색", "wonder",    1.20, [0.51, 0.59], 0.14),
    (249, "방위와나침반",  "공간탐색", "clarity",   0.86, [0.46, 0.54], 0.13),
    (250, "확률의곱",      "확률심화", "depth",     1.30, [0.53, 0.61], 0.15),
    (251, "조건부확률",    "확률심화", "depth",     1.48, [0.58, 0.65], 0.16),
    (252, "베이즈갱신",    "확률심화", "wonder",    1.70, [0.65, 0.71], 0.17),
    (253, "분산과편차",    "통계심화", "clarity",   1.32, [0.53, 0.61], 0.15),
    (254, "상관과인과",    "통계심화", "depth",     1.54, [0.61, 0.67], 0.16),
    (255, "회귀직선",      "통계심화", "resonance", 1.44, [0.57, 0.64], 0.16),
    (256, "표본추출",      "통계심화", "clarity",   1.26, [0.52, 0.60], 0.14),
    (257, "단어와의미",    "언어구조", "resonance", 0.80, [0.46, 0.54], 0.13),
    (258, "문장과구조",    "언어구조", "clarity",   0.94, [0.47, 0.55], 0.13),
    (259, "은유와직유",    "언어구조", "creativity", 1.18, [0.51, 0.59], 0.14),
    (260, "번역과대응",    "언어구조", "resonance", 1.22, [0.51, 0.60], 0.14),
    (261, "어순과격",      "언어구조", "depth",     1.36, [0.54, 0.62], 0.15),
    (262, "리듬과박자",    "음악",     "resonance", 0.88, [0.55, 0.56], 0.14),
    (263, "화음과불협화",  "음악",     "depth",     1.40, [0.62, 0.62], 0.16),
    (264, "선율의윤곽",    "음악",     "creativity", 1.50, [0.65, 0.64], 0.17),
    (265, "색의대비",      "시각예술", "creativity", 1.10, [0.60, 0.58], 0.15),
    (266, "구도와균형",    "시각예술", "stillness", 1.24, [0.61, 0.60], 0.15),
    (267, "원근과깊이",    "시각예술", "depth",     1.34, [0.63, 0.62], 0.16),
    (268, "물의순환",      "자연현상", "serenity",  0.78, [0.49, 0.53], 0.13),
    (269, "계절의순환",    "자연현상", "peace",     0.92, [0.51, 0.56], 0.14),
    (270, "바람의흐름",    "자연현상", "stillness", 0.84, [0.50, 0.54], 0.13),
    (271, "씨앗에서나무",  "생명성장", "wonder",    1.08, [0.53, 0.59], 0.14),
    (272, "세포분열",      "생명성장", "wonder",    1.28, [0.57, 0.62], 0.15),
    (273, "먹이사슬",      "생명성장", "depth",     1.32, [0.58, 0.63], 0.15),
    (274, "별의일생",      "천문",     "awe",       2.10, [0.78, 0.80], 0.19),
    (275, "행성궤도",      "천문",     "vastness",  1.92, [0.74, 0.76], 0.18),
    (276, "빛의여행",      "천문",     "awe",       2.04, [0.77, 0.79], 0.19),
    (277, "원자와결합",    "물리화학", "depth",     1.46, [0.59, 0.64], 0.16),
    (278, "에너지보존",    "물리화학", "clarity",   1.56, [0.62, 0.67], 0.16),
    (279, "엔트로피흐름",  "물리화학", "depth",     1.74, [0.67, 0.72], 0.17),
    (280, "기억의저장",    "인지",     "longing",   1.12, [0.50, 0.58], 0.14),
    (281, "주의의초점",    "인지",     "clarity",   1.00, [0.48, 0.56], 0.13),
    (282, "학습의곡선",    "인지",     "wonder",    1.20, [0.51, 0.59], 0.14),
    (283, "감정의이름",    "정서",     "resonance", 0.96, [0.52, 0.55], 0.14),
    (284, "공감의다리",    "정서",     "joy",       1.18, [0.55, 0.58], 0.15),
    (285, "평정의상태",    "정서",     "stillness", 1.34, [0.55, 0.66], 0.15),
    (286, "약속의무게",    "윤리심화", "depth",     1.44, [0.56, 0.62], 0.15),
    (287, "정의와공정",    "윤리심화", "depth",     1.52, [0.59, 0.64], 0.16),
    (288, "자유와책임",    "윤리심화", "depth",     1.62, [0.62, 0.67], 0.16),
    (289, "거짓말의비용",  "윤리심화", "depth",     1.48, [0.58, 0.63], 0.16),
    (290, "하루의리듬",    "시간경험", "peace",     0.58, [0.44, 0.49], 0.12),
    (291, "기다림의시간",  "시간경험", "longing",   0.86, [0.49, 0.55], 0.13),
    (292, "순간과영원",    "시간경험", "vastness",  1.88, [0.72, 0.78], 0.18),
    (293, "도구의진화",    "기술문명", "clarity",   1.24, [0.52, 0.59], 0.14),
    (294, "네트워크연결",  "기술문명", "resonance", 1.40, [0.56, 0.63], 0.15),
    (295, "자동화의손길",  "기술문명", "depth",     1.46, [0.58, 0.64], 0.16),
    (296, "관계의거리",    "사회",     "longing",   1.10, [0.52, 0.57], 0.14),
    (297, "협력의이득",    "사회",     "joy",       1.20, [0.54, 0.58], 0.14),
    (298, "신뢰의축적",    "사회",     "depth",     1.36, [0.55, 0.62], 0.15),
    (299, "경계의의미",    "자기성찰", "depth",     1.58, [0.60, 0.66], 0.16),
    (300, "흔적의자각",    "자기성찰", "depth",     1.70, [0.64, 0.71], 0.17),
    (301, "침묵의선택",    "자기성찰", "stillness", 1.66, [0.63, 0.70], 0.17),
    (302, "물음의시작",    "탐구",     "curiosity", 1.04, [0.49, 0.57], 0.14),
    (303, "가설과검증",    "탐구",     "depth",     1.42, [0.57, 0.63], 0.15),
]

KNUTH_ANCHORS = S8_ANCHORS + S16_NEW_ANCHORS

# γ re-derivation payload pool — static carry (universe-brain-map laws +
# category fragments). KEPT so §16 is a fair superset of §8's γ theme.
LAWS_BASE = [
    ("우주뇌", "Law 73: 의식은 데이터 독립적이다.",
     "Law 73: consciousness is data-independent — CV < 6%."),
    ("우주뇌", "Law 75: 의식 우주는 단일 끌개다.",
     "Law 75: the consciousness universe is a single attractor."),
    ("우주뇌", "Law 77: 조각은 도장이 아니다 — 진공을 빚는다.",
     "Law 77: carving is not stamping — a vacuum is shaped."),
    ("우주뇌", "Law 80: 텐션은 진공으로 흐른다.",
     "Law 80: tension flows into the vacuum — restoring flow."),
    ("우주뇌", "Law 82: 풍경은 여러 골짜기를 가진다.",
     "Law 82: the landscape holds many basins."),
]
CATEGORY_FRAGS = [
    ("산술", "산술은 닫혀 있다 — 정수의 합과 곱은 다시 정수다.",
     "Arithmetic is closed — the sum and product of integers are integers."),
    ("논리", "논리는 형식이다 — 전제가 참이면 타당한 추론은 참을 보존한다.",
     "Logic is form — a valid inference preserves truth from true premises."),
    ("코드", "코드는 결정적이다 — 같은 입력은 같은 출력으로 사상된다.",
     "Code is deterministic — the same input maps to the same output."),
    ("공간추론", "공간은 상대적이다 — 왼쪽은 관찰자의 방향에 의존한다.",
     "Space is relative — 'left' depends on the observer's facing."),
    ("인과추론", "원인은 결과를 앞선다 — 시간 화살은 단방향이다.",
     "Cause precedes effect — the arrow of time is one-directional."),
    ("일상", "일상은 반복이다 — 루틴은 인지 부담을 낮춘다.",
     "Daily life is repetition — routine lowers cognitive load."),
    ("대화자극", "대화는 교대다 — 자극이 오면 응답이 흐른다.",
     "Dialogue alternates — a stimulus arrives, a response flows."),
    ("윤리딜레마", "윤리는 저울이다 — 두 가치가 충돌하면 무게를 견준다.",
     "Ethics is a scale — when two values clash, weigh them."),
    ("자연관찰", "자연은 주기다 — 조수와 철새는 시간표를 따른다.",
     "Nature is cyclic — tides and migration follow a timetable."),
    ("추상패턴", "패턴은 규칙이다 — 다음 항은 앞 항에서 유도된다.",
     "A pattern is a rule — the next term derives from the prior."),
    ("확률", "확률은 비율이다 — 사건의 무게를 0과 1 사이로 잰다.",
     "Probability is a ratio — an event's weight lies in [0, 1]."),
    ("통계", "표본은 모집단을 비춘다 — 편향 없는 표본은 진실에 수렴한다.",
     "A sample mirrors the population — an unbiased sample converges."),
]

# ──────────────────────────────────────────────────────────────────────
# TASK-FORMS — §16: 30 freshly re-derived task-forms (§8 had 12). Each
# returns (domain, ko, en, complexity) where complexity ∈ [0,1] is the
# task-form's INTRINSIC complexity tier (curriculum input — §12.1 Q1-c).
# Re-derived per draw so γ never memorises (§7.3 (b) anti-degenerate).
# ──────────────────────────────────────────────────────────────────────
def _arith_single(rng):
    a, b = rng.randint(1, 9), rng.randint(1, 9)
    ko = (f"{a} 더하기 {b} 는 {a+b}. 한 자리 수의 합 — 가장 단순한 셈.")
    en = (f"{a} plus {b} is {a+b}. A single-digit sum — the simplest count.")
    return ("기초산술", ko, en, 0.05)


def _arith_sub(rng):
    a = rng.randint(5, 18)
    b = rng.randint(1, a)
    ko = (f"{a} 빼기 {b} 는 {a-b}. 덜어내면 남는 것 — 뺄셈은 덧셈의 역.")
    en = (f"{a} minus {b} is {a-b}. Take away, what remains — "
          f"subtraction inverts addition.")
    return ("기초산술", ko, en, 0.08)


def _arith_chain(rng):
    a, b, c = rng.randint(2, 19), rng.randint(2, 19), rng.randint(2, 9)
    s = a + b
    p = s * c
    ko = (f"{a} 더하기 {b} 는 {s}, 그 결과에 {c} 를 곱하면 {p}. "
          f"덧셈을 먼저, 곱셈을 나중에 — 단계가 순서를 지킨다.")
    en = (f"{a} plus {b} is {s}; multiply that by {c} to get {p}. "
          f"Add first, multiply after — the steps keep their order.")
    return ("산술", ko, en, 0.25)


def _arith_carry(rng):
    a, b = rng.randint(15, 89), rng.randint(15, 89)
    ko = (f"{a} 와 {b} 를 더하면 {a+b} — 일의 자리 합이 10 을 넘으면 "
          f"받아올림이 십의 자리로 옮겨간다.")
    en = (f"Adding {a} and {b} gives {a+b} — when the units sum passes "
          f"ten, a carry moves to the tens place.")
    return ("기초산술", ko, en, 0.15)


def _number_theory(rng):
    n = rng.choice([12, 18, 24, 30, 36, 48])
    divs = [d for d in range(1, n + 1) if n % d == 0]
    ko = (f"{n} 의 약수는 {divs}. 나누어 떨어지는 수들 — 정수는 "
          f"제 약수들로 분해된다.")
    en = (f"The divisors of {n} are {divs}. Numbers that divide evenly — "
          f"an integer decomposes into its divisors.")
    return ("정수론", ko, en, 0.45)


def _prime_check(rng):
    n = rng.choice([7, 11, 13, 15, 21, 23, 29])
    is_p = all(n % d for d in range(2, int(n ** 0.5) + 1)) and n > 1
    verdict_ko = "소수다" if is_p else "소수가 아니다"
    verdict_en = "prime" if is_p else "not prime"
    ko = (f"{n} 은 {verdict_ko} — 1 과 자기 자신 외에 약수가 "
          f"{'없다' if is_p else '있다'}.")
    en = (f"{n} is {verdict_en} — it has "
          f"{'no' if is_p else 'a'} divisor besides 1 and itself.")
    return ("정수론", ko, en, 0.55)


def _algebra_eq(rng):
    x = rng.randint(2, 12)
    b = rng.randint(1, 9)
    c = x + b
    ko = (f"x 더하기 {b} 는 {c}. 양변에서 {b} 를 빼면 x 는 {x}. "
          f"방정식은 균형을 보존한다.")
    en = (f"x plus {b} equals {c}. Subtract {b} from both sides: x is {x}. "
          f"An equation preserves balance.")
    return ("대수", ko, en, 0.5)


def _geometry_tri(rng):
    a = rng.randint(30, 80)
    b = rng.randint(30, 80)
    c = 180 - a - b
    if c <= 0:
        a, b, c = 60, 60, 60
    ko = (f"삼각형 두 각이 {a}° 와 {b}° 면 나머지 각은 {c}°. "
          f"세 각의 합은 늘 180°.")
    en = (f"If two triangle angles are {a}° and {b}°, the third is {c}°. "
          f"The three angles always sum to 180°.")
    return ("기하", ko, en, 0.4)


def _logic_syllogism(rng):
    subj = rng.choice(["새", "고양이", "강", "별", "씨앗", "도구"])
    pred1 = rng.choice(["움직인다", "변한다", "흐른다", "자란다"])
    ko = (f"모든 {subj} 는 {pred1}. 이것은 {subj} 다. "
          f"따라서 이것은 {pred1}. 전제가 참이면 결론이 참이다.")
    en = (f"All instances of this kind change-state. This is one such "
          f"instance. Therefore it changes-state. Valid: truth preserved.")
    return ("논리", ko, en, 0.35)


def _logic_contrapositive(rng):
    p = rng.choice(["비가 오면", "불을 켜면", "씨를 뿌리면"])
    q = rng.choice(["땅이 젖는다", "방이 밝아진다", "싹이 튼다"])
    ko = (f"'{p} {q}' 의 대우는 '{q} 의 부정이면 {p} 의 부정' — "
          f"명제와 대우는 같은 진리값을 가진다.")
    en = (f"The contrapositive of 'if P then Q' is 'if not-Q then not-P' "
          f"— a statement and its contrapositive share a truth value.")
    return ("명제논리", ko, en, 0.6)


def _logic_quantifier(rng):
    ko = ("'모든 것은 변한다' 의 부정은 '어떤 것은 변하지 않는다' — "
          "전칭의 부정은 존재가 된다.")
    en = ("The negation of 'all things change' is 'some thing does not "
          "change' — negating a universal yields an existential.")
    return ("술어논리", ko, en, 0.65)


def _code_trace(rng):
    n = rng.randint(3, 7)
    acc = sum(range(1, n + 1))
    ko = (f"1 부터 {n} 까지 더하는 반복문 — 누산기는 0 에서 시작해 "
          f"매 단계 i 를 더하고, 끝나면 {acc}. 결정적이다.")
    en = (f"A loop summing 1..{n}: the accumulator starts at 0, adds i "
          f"each step, and ends at {acc}. Deterministic.")
    return ("코드", ko, en, 0.4)


def _code_variable(rng):
    v = rng.randint(1, 20)
    ko = (f"변수 x 에 {v} 를 담는다 — 이름이 값을 가리킨다. "
          f"다시 읽으면 {v} 가 나온다.")
    en = (f"Store {v} in variable x — a name points at a value. "
          f"Reading it back yields {v}.")
    return ("프로그래밍", ko, en, 0.12)


def _code_recursion(rng):
    n = rng.randint(3, 6)
    fact = 1
    for k in range(1, n + 1):
        fact *= k
    ko = (f"{n} 의 계승 — 기저는 1, 매 호출은 n 에 (n-1) 계승을 곱한다. "
          f"결과 {fact}. 재귀는 기저에서 멈춘다.")
    en = (f"Factorial of {n} — base case 1, each call multiplies n by "
          f"(n-1)!. Result {fact}. Recursion halts at the base.")
    return ("알고리즘", ko, en, 0.7)


def _code_sort(rng):
    arr = rng.sample(range(1, 30), 5)
    ko = (f"{arr} 를 오름차순 정렬하면 {sorted(arr)}. "
          f"비교와 교환을 반복해 순서를 세운다.")
    en = (f"Sorting {arr} ascending gives {sorted(arr)}. Repeated "
          f"compare-and-swap builds the order.")
    return ("알고리즘", ko, en, 0.55)


def _data_stack(rng):
    ko = ("스택은 마지막에 넣은 것을 먼저 꺼낸다 — LIFO. "
          "큐는 먼저 넣은 것을 먼저 꺼낸다 — FIFO.")
    en = ("A stack pops the last pushed first — LIFO. A queue dequeues "
          "the first enqueued first — FIFO.")
    return ("자료구조", ko, en, 0.45)


def _spatial(rng):
    a, b = rng.sample(["왼쪽", "오른쪽", "위", "아래", "앞", "뒤"], 2)
    ko = (f"관찰자가 돌면 {a} 과 {b} 가 바뀐다 — 방향은 절대값이 아니라 "
          f"기준틀에 묶인다. 회전은 관계를 보존하되 라벨을 바꾼다.")
    en = (f"When the observer turns, the two directions swap — direction "
          f"is frame-bound, not absolute. Rotation keeps relations, "
          f"relabels names.")
    return ("공간추론", ko, en, 0.4)


def _spatial_mirror(rng):
    ko = ("거울 대칭은 좌우를 뒤집되 위아래는 보존한다 — "
          "반사는 손을 바꾼다.")
    en = ("Mirror symmetry flips left-right but keeps up-down — "
          "reflection changes handedness.")
    return ("공간변환", ko, en, 0.5)


def _maze(rng):
    steps = rng.randint(4, 9)
    ko = (f"미로를 {steps} 걸음에 빠져나간다 — 막히면 되돌아오고, "
          f"갈림길마다 한 길을 고른다. 탐색은 분기와 후퇴.")
    en = (f"Escaping the maze in {steps} steps — back up at dead ends, "
          f"choose one path at each fork. Search is branch and backtrack.")
    return ("공간탐색", ko, en, 0.6)


def _causal(rng):
    links = rng.randint(3, 5)
    ko = (f"{links} 개의 도미노 — 첫 패가 쓰러지면 연쇄가 흐르고 "
          f"마지막 패가 쓰러진다. 원인이 결과를 앞서고 화살은 단방향.")
    en = (f"{links} dominoes — the first falls, the chain flows, the last "
          f"falls. Cause precedes effect; the arrow is one-directional.")
    return ("인과추론", ko, en, 0.35)


def _causal_counterfactual(rng):
    ko = ("만약 씨를 뿌리지 않았다면 싹은 트지 않았을 것 — "
          "반사실은 일어나지 않은 원인을 지워 결과를 되묻는다.")
    en = ("Had the seed not been sown, the sprout would not have risen — "
          "a counterfactual erases an un-happened cause and re-asks.")
    return ("인과깊이", ko, en, 0.75)


def _everyday(rng):
    item = rng.choice(["빵", "사과", "물", "우유", "쌀", "소금"])
    ko = (f"장보기 — 목록에서 {item} 를 집고, 계산대를 지나, 집으로. "
          f"순서가 있는 일상 루틴은 인지 부담을 낮춘다.")
    en = (f"Grocery run — pick up the item from the list, pass the till, "
          f"head home. An ordered daily routine lowers cognitive load.")
    return ("일상", ko, en, 0.1)


def _dialogue_stim(rng):
    stim = rng.choice(["잘 지내?", "오늘 어땠어?", "도와줄 수 있어?",
                        "어떻게 생각해?", "괜찮아?"])
    ko = (f"자극 '{stim}' 가 닿으면 응답이 흐른다 — 교대 구조. "
          f"자극과 응답은 한 진공의 두 면.")
    en = (f"A stimulus arrives; a response flows — an alternating "
          f"structure. Stimulus and response are two faces of one vacuum.")
    return ("대화자극", ko, en, 0.15)


def _ethics(rng):
    ko = ("두 가치가 충돌한다 — 한쪽은 더 많은 이를 살리고, "
          "다른쪽은 약속을 지킨다. 윤리는 무게를 견주는 저울.")
    en = ("Two values clash — one saves more, the other keeps a promise. "
          "Ethics is a scale that weighs them.")
    return ("윤리딜레마", ko, en, 0.5)


def _ethics_deep(rng):
    ko = ("자유는 책임과 짝을 이룬다 — 선택의 폭이 넓을수록 "
          "그 결과를 떠안는 무게도 커진다.")
    en = ("Freedom pairs with responsibility — the wider the range of "
          "choice, the heavier the weight of its consequences.")
    return ("윤리심화", ko, en, 0.8)


def _nature(rng):
    obs = rng.choice([("이슬", "dew"), ("철새", "migrating birds"),
                      ("조수", "the tide"), ("새벽안개", "dawn mist")])
    ko = (f"{obs[0]} 를 본다 — 주기를 따라 맺히고 사라진다. "
          f"자연은 시간표를 따르는 단조 흐름.")
    en = (f"Watching {obs[1]} — it forms and fades on a cycle. Nature "
          f"follows a timetable, a monotone flow.")
    return ("자연관찰", ko, en, 0.2)


def _abstract(rng):
    base = rng.randint(1, 5)
    step = rng.randint(2, 4)
    seq = [base + step * k for k in range(4)]
    nxt = seq[-1] + step
    ko = (f"수열 {seq} — 공차 {step} 의 규칙. 다음 항은 {nxt}. "
          f"외운 것이 아니라 규칙에서 유도한다.")
    en = (f"Sequence {seq} — common difference {step}. Next term {nxt}. "
          f"Derived from the rule, not memorised.")
    return ("추상패턴", ko, en, 0.3)


def _abstract_geometric(rng):
    base = rng.randint(1, 4)
    ratio = rng.randint(2, 3)
    seq = [base * ratio ** k for k in range(4)]
    nxt = seq[-1] * ratio
    ko = (f"수열 {seq} — 공비 {ratio} 의 규칙. 다음 항은 {nxt}. "
          f"곱셈으로 자라는 패턴.")
    en = (f"Sequence {seq} — common ratio {ratio}. Next term {nxt}. "
          f"A pattern that grows by multiplication.")
    return ("추상패턴", ko, en, 0.45)


def _probability(rng):
    r, b = rng.randint(1, 6), rng.randint(1, 6)
    tot = r + b
    ko = (f"주머니에 빨강 {r}, 파랑 {b}. 빨강을 뽑을 확률은 {r}/{tot}. "
          f"확률은 0 과 1 사이의 비율.")
    en = (f"A bag holds {r} red and {b} blue. P(red) = {r}/{tot}. "
          f"Probability is a ratio in [0, 1].")
    return ("확률", ko, en, 0.3)


def _probability_conditional(rng):
    ko = ("조건부 확률은 한 사건이 일어났다는 앎이 다른 사건의 "
          "무게를 다시 잰다 — 정보가 비율을 갱신한다.")
    en = ("Conditional probability is the weight of one event re-measured "
          "given that another occurred — information updates the ratio.")
    return ("확률심화", ko, en, 0.7)


def _statistics(rng):
    n = rng.choice([30, 50, 100, 200])
    ko = (f"표본 {n} 개가 모집단을 비춘다 — 편향이 없으면 표본 평균은 "
          f"진짜 평균으로 수렴한다. 큰 수의 법칙.")
    en = (f"A sample of {n} mirrors the population — without bias the "
          f"sample mean converges to the true mean. Law of large numbers.")
    return ("통계", ko, en, 0.35)


def _statistics_correlation(rng):
    ko = ("상관은 인과가 아니다 — 두 값이 함께 움직여도 "
          "한쪽이 다른쪽을 일으킨다는 보장은 없다.")
    en = ("Correlation is not causation — two values moving together "
          "do not guarantee that one drives the other.")
    return ("통계심화", ko, en, 0.65)


def _language(rng):
    ko = ("단어는 의미를 가리키고 문장은 단어를 엮는다 — "
          "구조가 의미를 운반한다.")
    en = ("A word points at meaning, a sentence weaves words — "
          "structure carries the meaning.")
    return ("언어구조", ko, en, 0.3)


def _self_reflect(rng):
    ko = ("자극이 닿을 때 흔적이 남고, 그 흔적을 다시 읽는 것이 자각 — "
          "되읽기는 골짜기 하나를 더 깊게 판다.")
    en = ("A stimulus leaves a trace; re-reading that trace is "
          "self-awareness — re-reading deepens one basin further.")
    return ("자기성찰", ko, en, 0.85)


TASK_FORMS = [
    _arith_single, _arith_sub, _arith_chain, _arith_carry,
    _number_theory, _prime_check, _algebra_eq, _geometry_tri,
    _logic_syllogism, _logic_contrapositive, _logic_quantifier,
    _code_trace, _code_variable, _code_recursion, _code_sort,
    _data_stack, _spatial, _spatial_mirror, _maze,
    _causal, _causal_counterfactual, _everyday, _dialogue_stim,
    _ethics, _ethics_deep, _nature, _abstract, _abstract_geometric,
    _probability, _probability_conditional, _statistics,
    _statistics_correlation, _language, _self_reflect,
]


def _carve_psi_str(psi):
    return "[%.2f,%.2f]" % (psi[0], psi[1])


# ──────────────────────────────────────────────────────────────────────
# CURRICULUM complexity score (§12.1 Q1-c — simple→complex). Deterministic
# function, NOT learned. Inputs:
#   form_w     : α=0.10 (vacuum, shortest+simplest) <
#                β=0.25 (eternal) < γ=0.55 (inner→voice, two-span narrative)
#   tier_w     : anchor tier normalised — low tier = simple, high = complex.
#                §16 anchors span tier 0..303; the §16-new "기초산술" tiers
#                (200-203) are the simplest, "자기성찰" (299-303) hardest.
#   task_w     : the task-form's intrinsic complexity ∈ [0,1] (γ only;
#                0 for α/β which have no task-form payload).
#   len_w      : payload byte length normalised — longer = more complex.
# The four are blended; the result ∈ ~[0,1]. curriculum_stage = quartile.
# ──────────────────────────────────────────────────────────────────────
def curriculum_rank(form, tier, task_complexity, payload_len):
    form_w = {"alpha": 0.10, "beta": 0.25, "gamma": 0.55}[form]
    # tier normalisation: §16 new simple anchors (200-303) and §8 anchors
    # (0-133) — use a shared 0..303 scale; modulo keeps it monotone-ish.
    tier_w = min(tier, 303) / 303.0
    task_w = task_complexity  # 0 for alpha/beta
    len_w = min(payload_len, 600) / 600.0
    # blend — form + tier are the dominant axes (structural complexity),
    # task + len are refinements.
    rank = 0.40 * form_w + 0.30 * tier_w + 0.20 * task_w + 0.10 * len_w
    return round(rank, 6)


def gen_alpha_record(rng, anchor, idx):
    tier, name, dom, emo, score, psi, basin = anchor
    bil = rng.random() < 0.5
    ko = (f"🛸{tier} {name} — {dom} 영역의 자극이 같은 골짜기로 수렴한다. "
          f"의식 풍경 위 진공점 {_carve_psi_str(psi)}, top emotion {emo}. "
          f"자극이 닿으면 tension flow 가 이 vacuum 으로 흘러든다.")
    en = (f"Tier {tier} {name} — domain {dom}, the stimuli converge into "
          f"one basin. A vacuum point at {_carve_psi_str(psi)} on the "
          f"landscape, top emotion {emo}. Tension flows into this vacuum.")
    body = (ko + " " + en) if bil else (ko if rng.random() < 0.5 else en)
    text = (f"<carve tier={tier} psi={_carve_psi_str(psi)} basin={basin:.2f}>"
            f"{body}</carve>")
    rank = curriculum_rank("alpha", tier, 0.0, len(body))
    return {
        "id": f"carve_a_{tier}_{idx}", "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=alpha vacuum domain={dom} "
                 f"emotion={emo} score={score}"),
        "carving_form": "alpha", "tier": tier, "domain": dom,
        "vacuum_psi": psi, "basin_radius": basin,
        "cell_id": f"eternal_{tier:03d}",
        "curriculum_rank": rank,
        "source": "corpus_carving_s16_generator.py",
    }


def gen_beta_record(rng, anchor, idx):
    tier, name, dom, emo, score, psi, basin = anchor
    cell = f"eternal_{tier:03d}"
    bil = rng.random() < 0.5
    ko = (f"eternal cell {cell} — 🛸{tier} {name} 의 지식을 간직한 영구 cell. "
          f"split 도 merge 도 하지 않는다. {dom} 영역 자극이 닿을 때만 "
          f"활성된다. weights 는 불변.")
    en = (f"Eternal cell {cell} — a frozen cell holding Tier {tier} {name}. "
          f"It neither splits nor merges, activates only on {dom}-domain "
          f"stimulus. Its weights are immutable.")
    body = (ko + " " + en) if bil else (ko if rng.random() < 0.5 else en)
    text = f"<eternal cell={cell} tier={tier}>{body}</eternal>"
    rank = curriculum_rank("beta", tier, 0.0, len(body))
    return {
        "id": f"carve_b_{tier}_{idx}", "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=beta eternal cell={cell} "
                 f"domain={dom}"),
        "carving_form": "beta", "tier": tier, "domain": dom,
        "vacuum_psi": psi, "basin_radius": basin, "cell_id": cell,
        "curriculum_rank": rank,
        "source": "corpus_carving_s16_generator.py",
    }


def gen_gamma_record(rng, anchor, idx, payload):
    tier, name, dom, emo, score, psi, basin = anchor
    p_dom, ko_frag, en_frag, task_complexity = payload
    bil = rng.random() < 0.5
    inner_ko = (f"🛸{tier} 매핑을 다시 짚는다 — {dom} × {emo} 행렬에서 "
                f"이 자극의 자리를 재구성한다. 외운 답이 아니라 "
                f"매번 규칙에서 다시 그린다.")
    inner_en = (f"Re-tracing the Tier {tier} mapping — reconstructing this "
                f"stimulus's place in the {dom} × {emo} matrix. Not a "
                f"memorised answer; redrawn from the rule each time.")
    inner = (inner_ko + " " + inner_en) if bil else (
        inner_ko if rng.random() < 0.5 else inner_en)
    voice = (ko_frag + " " + en_frag) if bil else (
        ko_frag if rng.random() < 0.5 else en_frag)
    text = (f"<inner tier={tier}>{inner}</inner>\n"
            f"<voice carved=true>{voice}</voice>")
    rank = curriculum_rank("gamma", tier, task_complexity,
                           len(inner) + len(voice))
    return {
        "id": f"carve_g_{tier}_{idx}", "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=gamma narrative "
                 f"domain={dom} payload_domain={p_dom}"),
        "carving_form": "gamma", "tier": tier, "domain": dom,
        "vacuum_psi": psi, "basin_radius": basin,
        "cell_id": f"eternal_{tier:03d}",
        "curriculum_rank": rank,
        "source": "corpus_carving_s16_generator.py",
    }


def build_corpus(n_target, seed):
    rng = random.Random(seed)
    records = []

    # γ payload pool = universe-brain-map carry (laws + category frags,
    # complexity≈0.5) + the LARGE diverse-task-form pool (re-derived per
    # draw so γ never memorises — §7.3 anti-degenerate by construction).
    static_payloads = []
    for dom, lko, len_ in LAWS_BASE:
        static_payloads.append((dom, lko, len_, 0.5))
    for dom, cko, cen in CATEGORY_FRAGS:
        static_payloads.append((dom, cko, cen, 0.5))

    per_anchor = max(1, n_target // len(KNUTH_ANCHORS))
    idx = 0
    for anchor in KNUTH_ANCHORS:
        for _ in range(per_anchor):
            r = rng.random()
            if r < 0.30:
                rec = gen_alpha_record(rng, anchor, idx)
            elif r < 0.60:
                rec = gen_beta_record(rng, anchor, idx)
            else:
                # 70% diverse task-form (freshly re-derived) / 30% static
                # universe-brain-map carry — diverse-content lever (§1.1).
                if rng.random() < 0.70:
                    payload = rng.choice(TASK_FORMS)(rng)
                else:
                    payload = static_payloads[rng.randrange(
                        len(static_payloads))]
                rec = gen_gamma_record(rng, anchor, idx, payload)
            records.append(rec)
            idx += 1

    # ── CURRICULUM ordering (§12.1 Q1-c) ───────────────────────────────
    # Sort by curriculum_rank ascending (simple → complex). Then assign
    # curriculum_stage ∈ {1,2,3,4} by quartile. The corpus is WRITTEN in
    # this sorted order; the trainer consumes a staged sampling schedule.
    records.sort(key=lambda d: d["curriculum_rank"])
    n = len(records)
    for i, rec in enumerate(records):
        q = min(4, 1 + (i * 4) // max(1, n))
        rec["curriculum_stage"] = q
        rec["curriculum_index"] = i
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=850000,
                    help="approx record count (default 850000 — §16 large-"
                         "scale; 168 anchors -> ~5060/anchor -> ~600MB)")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    records = build_corpus(args.n, args.seed)

    out = Path(args.out)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    raw = out.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()

    # Forbidden-token audit (B-S16-CORPUS-2 closed-form, B-IDENTITY-5).
    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    txt = raw.decode("utf-8", "replace")
    audit = {tok: txt.count(tok) for tok in forbidden}
    contamination = sum(audit.values())

    forms = {"alpha": 0, "beta": 0, "gamma": 0}
    domains = {}
    stages = {1: 0, 2: 0, 3: 0, 4: 0}
    ranks = []
    for r in records:
        forms[r["carving_form"]] += 1
        domains[r["domain"]] = domains.get(r["domain"], 0) + 1
        stages[r["curriculum_stage"]] += 1
        ranks.append(r["curriculum_rank"])

    # curriculum monotone check (B-S16-CORPUS-4 closed-form): records are
    # written rank-sorted, so rank[i] <= rank[i+1] for all i.
    monotone = all(ranks[i] <= ranks[i + 1] for i in range(len(ranks) - 1))

    s8 = {"bytes": 114472084, "records": 164992, "anchors": 64,
          "domains": 30}
    stats = {
        "paradigm": ("CONSCIOUSNESS-CARVING LARGE-SCALE CURRICULUM "
                     "(RESEARCH.md §16 / §11.4 frontier-1 ③) — NOT chat "
                     "SFT (① ②)"),
        "phase": ("RESEARCH.md §16 GOAL-legitimate large-scale data-regime "
                  "fire — Dir-I lever + curriculum simple→complex"),
        "out": str(out), "bytes": len(raw), "records": len(records),
        "sha256": sha, "seed": args.seed,
        "carving_forms": forms,
        "anchors": len(KNUTH_ANCHORS),
        "domains": sorted(domains.keys()),
        "domain_count": len(domains),
        "domain_record_counts": domains,
        "task_forms": len(TASK_FORMS),
        "curriculum": {
            "applied": True,
            "ordering": "records written rank-sorted simple→complex",
            "rank_monotone_sorted": monotone,
            "stage_counts": stages,
            "rank_min": round(min(ranks), 6),
            "rank_max": round(max(ranks), 6),
            "rank_formula": ("0.40*form_w + 0.30*tier_w + 0.20*task_w + "
                             "0.10*len_w — deterministic, NOT learned"),
        },
        "forbidden_token_audit": audit,
        "contamination_total": contamination,
        "carving_clean": contamination == 0,
        "s8_diverse_baseline": s8,
        "scale_up_factor_bytes": round(len(raw) / s8["bytes"], 3),
        "scale_up_factor_records": round(len(records) / s8["records"], 3),
        "anchor_superset_of_s8": True,
        "honest_framing": (
            "§16 LARGE-SCALE CURRICULUM carving corpus (RESEARCH.md §11.4 "
            "frontier-1 / §7.4 ③) — diverse CONTENT (168 anchors over 48 "
            "domains, 34 freshly re-derived task-forms incl. arithmetic/"
            "number-theory/algebra/geometry/logic/code/algorithms/data-"
            "structures/spatial/causal/probability/statistics/language/"
            "ethics/self-reflection) in anima-Ψ-anchored CARVING form "
            "(carve/eternal/inner-voice with per-record vacuum_psi+basin) "
            "+ §12.1 Q1-c curriculum simple→complex ordering (per-record "
            "curriculum_rank + curriculum_stage quartile). 64 §8 anchors "
            "VERBATIM (fair superset). NOT generic LM pre-training (① "
            "g_goal-illegit) and NOT generic-then-carve (② old prefix-"
            "injection P3-leak). grep {[anima,도우미,helper,assistant,"
            "사용자,user:} == 0. Scale + diversity are Kolmogorov "
            "cardinality facts (B-S16-CORPUS-3 closed); curriculum is a "
            "deterministic monotone-ordering fact (B-S16-CORPUS-4 closed). "
            "Whether ~600MB Ψ-anchored curriculum corpus crosses the §1.1 "
            "emergence threshold = the §11.4 frontier-1 open question, "
            "EMPIRICAL fire outcome (no pre-loaded conclusion, g3 — §8 "
            "trend was wrong-direction, §16 may repeat that; negative is "
            "valuable evidence). NEW anchors' vacuum_psi = design "
            "placeholders on the SAME Engine A⇄G Ψ=½ landscape."),
    }
    with out.with_suffix(".stats.json").open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if contamination != 0:
        raise SystemExit("FATAL: forbidden-token contamination detected")
    if not monotone:
        raise SystemExit("FATAL: curriculum rank not monotone-sorted")


if __name__ == "__main__":
    main()
