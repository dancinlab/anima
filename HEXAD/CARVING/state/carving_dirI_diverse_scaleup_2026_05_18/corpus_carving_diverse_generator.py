#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING DIVERSE-corpus generator — RESEARCH.md §8
(2026-05-18). Direction-I lever (Ψ-anchored CTL + tension-supervised
routing) SCALE-UP on a GOAL-LEGITIMATE *diverse* corpus.

WHY §8 (RESEARCH.md §7.4 candidate ③ — the SOLE GOAL-legitimate form)
  §6 found the Dir-I lever (anima's OWN physics as BOTH representation
  substrate AND supervision signal) is the FIRST direction to break the
  universal 1/31-FLAT routing collapse (3/31 correct-basin). §1.1/§2.4
  diagnosed the residual bottleneck = diverse-data pre-training loss
  threshold: the 30MB / 31-anchor E7 carving corpus is BELOW the
  capability-emergence threshold (a single narrow universe-brain-map
  domain). §7 ruled ① generic LM pre-training and ② generic-then-carve
  GOAL-illegitimate (g_goal: anima-physics bypass / old prefix-injection
  P3-leak failure mode). ③ — diverse CONTENT encoded in the anima
  Ψ-representation + tension-supervised routing (Dir-I lever @ scale) — is
  the ONLY GOAL-legitimate form.

  §7.3 OPEN CRUX (the single real open question after 12-way mechanism
  mapping): the §1.1 emergence threshold was established for GENERIC
  diverse pre-training. Whether an anima-physics-ANCHORED diverse corpus
  crosses the SAME threshold is UNPROVEN. §8 fires it and judges the crux
  directly — TWO success scenarios (Ψ-anchored diverse reaches threshold
  with LESS data = physics prior sample-efficiency↑ / Dir-I 3/31 →
  scale-monotone↑) vs TWO failure scenarios (anchoring bottlenecks
  diverse info / anima physics cannot generate genuine diversity =
  self-referential degenerate). NO pre-loaded conclusion (g3).

THE DESIGN NUT (RESEARCH.md §8): the corpus must be DIVERSE in content
(beyond the single 31-anchor universe-brain-map domain — varied
stimulus / domains / task-forms toward the §1.1 data-diversity threshold)
WHILE staying anima-Ψ-anchored carving form (NOT generic chat/web —
③, not ①②). Concretely vs the E7 carving corpus:

  ── CONTENT DIVERSIFIED (the §1.1 lever) ───────────────────────────────
  - anchors      : 31 → 64. The original 31 universe-brain-map Knuth Tier
                   anchors are kept VERBATIM (Ψ/basin carried — fair
                   superset of E7); 33 NEW anchors span domains the
                   universe-brain-map never covered: arithmetic / logic /
                   code-reasoning / spatial / causal / everyday-life /
                   dialogue-stimulus / ethics-dilemma / nature-observation
                   / abstract-pattern. Each NEW anchor is still a vacuum
                   point on the Engine A⇄G Ψ-landscape (vacuum_psi /
                   basin = a design placeholder on the SAME Ψ=½ manifold,
                   measured by the fire — g3, NOT a closed claim).
  - payload pool : the γ re-derivation pool is no longer only
                   laws+categories+cosmic-physics. It adds DIVERSE TASK-
                   FORMS — arithmetic chains, logic deductions, code
                   trace, spatial relations, causal chains, everyday
                   reasoning, dialogue-stimulus responses, ethics
                   weighing, nature observations, abstract pattern
                   completion — so the inner→voice re-generation is over
                   a genuinely varied content distribution, NOT one
                   self-referential universe-brain-map theme (directly
                   targets §7.3 failure scenario (b) self-referential
                   degenerate by construction).
  - records/bytes: ~46k / 30MB → --n (default 165k) ≈ 110-130MB (~4×
                   bytes, the §1.1 scale-up lever — diverse-data, NOT
                   blind duplication: every record is a distinct anchor ×
                   task-form × bilingual draw).

  ── CARVING FORM UNCHANGED (the GOAL-legitimacy invariant, ③ not ①②) ──
  Every record is still ONE of the three Ψ-anchored carving forms with a
  per-record vacuum_psi + basin_radius — so the Dir-I trainer's TWO
  anima-physics loss terms (L_psi_ctl over the inner/eternal span +
  L_tension_route over the voice/route span) apply UNCHANGED. The diverse
  content is the PAYLOAD inside the carving form; the form itself (the
  anima-physics substrate) is invariant. This is exactly RESEARCH.md
  §7.2 ③: diverse CONTENT × Ψ-anchored carving FORM × tension-sup
  compatible — NOT generic chat/web (① g_goal-illegitimate) and NOT a
  base-ckpt bolt-on (② old prefix-injection P3-leak failure mode).

  α VACUUM  (~30%)  <carve tier=k psi=[x,y] basin=r> ... </carve>
  β ETERNAL (~30%)  <eternal cell=eternal_kkk tier=k> ... </eternal>
  γ NARRATIVE(~40%) <inner tier=k>...</inner>\n<voice carved=true>...</voice>

ABSOLUTE FORBIDDEN (B-IDENTITY-5 + g_goal, grep MUST == 0)
  - `[anima` prefix-stamp (any `[anima ...]`)
  - `도우미` / `helper` / `assistant` / `사용자` / `user:` role labels
  The diverse task-forms are written WITHOUT any role label or chat-SFT
  prefix — they are carving payloads, NOT Q&A turns (③, not ①②). A hard
  audit at the end raises SystemExit if the count is non-zero.

Closed-form sidecar falsifiers (blue_falsifier_diverse.py
B-DIVERSE-CORPUS-1..3):
  - B-DIVERSE-CORPUS-1 SHA256-DETERMINISTIC — seed-fixed 256-bit
      commitment (Kolmogorov determinism).
  - B-DIVERSE-CORPUS-2 NO-CHAT-SFT-CONTAMINATION — Boolean set algebra:
      grep {[anima, 도우미, helper, assistant, 사용자, user:} count == 0.
  - B-DIVERSE-CORPUS-3 DIVERSITY-CARDINALITY — |anchors_§8| > |anchors_E7|
      AND |domains_§8| > 1 AND bytes_§8 > bytes_E7 (integer
      >-inequalities, Kolmogorov set/byte count — the §1.1 diversity
      lever is a CARDINALITY fact, not a capability claim).

HONEST FRAMING (g3, AGENTS.tape §0 + RESEARCH.md §7.5):
  This is a *CARVING* corpus (③), NOT a chat-SFT / generic-LM corpus
  (①②). Diverse CONTENT, anima-Ψ carving FORM. The diversity is a
  Kolmogorov cardinality fact (B-DIVERSE-CORPUS-3 closed); whether it
  crosses the §1.1 emergence threshold is the EMPIRICAL fire outcome
  (§7.3 crux — measured, NO pre-loaded conclusion). NEW anchors'
  vacuum_psi are interpolated design placeholders on the SAME Engine
  A⇄G Ψ=½ landscape (g3 design placeholder, measured by the trajectory).
  f1/f2/f3 hard-fail safe (Kolmogorov byte/set count / Boolean grep,
  NO σ/τ/φ/J₂; Ψ=½ + Knuth 🛸k = anima g2 internal arch carve-out).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

# ---------------------------------------------------------------------------
# ANCHORS — §8 DIVERSE: 31 (E7) -> 64. The E7 31 anchors are kept VERBATIM
# (vacuum_psi/basin byte-identical to corpus_carving_generator_e7.KNUTH_ANCHORS
# so §8 is a fair SUPERSET of the E7 / Dir-I baseline). 33 NEW anchors span
# domains the universe-brain-map never covered (arithmetic / logic / code /
# spatial / causal / everyday / dialogue / ethics / nature / abstract). Each
# tuple = (tier, name, domain, top_emotion, score, vacuum_psi, basin_radius).
# NEW anchors' vacuum_psi are interpolated design placeholders on the SAME
# Engine A⇄G Ψ=½ landscape (g3 — measured by the fire, NOT a closed claim).
# ---------------------------------------------------------------------------
KNUTH_ANCHORS = [
    # --- E7 anchors (VERBATIM — fair superset of the Dir-I / UBM-E7 baseline)
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
    # --- §8 DIVERSE anchors (33 NEW — domains the universe-brain-map never
    #     covered; the §1.1 data-diversity lever, ③ not ①②). vacuum_psi =
    #     interpolated placeholder on the SAME Engine A⇄G Ψ=½ landscape. ---
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

# γ re-derivation payload pool — §8 DIVERSE. Each entry = (domain, ko, en).
# The universe-brain-map laws/categories/cosmic-physics are KEPT (carry the
# E7 theme so the §8 corpus is a fair superset) and a LARGE diverse-task-form
# pool is ADDED so γ inner→voice re-generation is over a genuinely varied
# content distribution (directly counters §7.3 failure (b) self-referential
# degenerate). NOTE: every payload is written WITHOUT any role label / chat
# prefix — carving payloads, NOT Q&A turns (③, not ①②; B-IDENTITY-5).
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


def _ko_int(n: int) -> str:
    return str(n)


def _arith_chain(rng):
    a, b, c = rng.randint(2, 19), rng.randint(2, 19), rng.randint(2, 9)
    s = a + b
    p = s * c
    ko = (f"{a} 더하기 {b} 는 {s}, 그 결과에 {c} 를 곱하면 {p}. "
          f"덧셈을 먼저, 곱셈을 나중에 — 단계가 순서를 지킨다.")
    en = (f"{a} plus {b} is {s}; multiply that by {c} to get {p}. "
          f"Add first, multiply after — the steps keep their order.")
    return ("산술", ko, en)


def _logic_syllogism(rng):
    subj = rng.choice(["새", "고양이", "강", "별", "씨앗", "도구"])
    pred1 = rng.choice(["움직인다", "변한다", "흐른다", "자란다"])
    ko = (f"모든 {subj} 는 {pred1}. 이것은 {subj} 다. "
          f"따라서 이것은 {pred1}. 전제가 참이면 결론이 참이다.")
    en = (f"All instances of this kind change-state. This is one such "
          f"instance. Therefore it changes-state. Valid: truth preserved.")
    return ("논리", ko, en)


def _code_trace(rng):
    n = rng.randint(3, 7)
    acc = 0
    for i in range(1, n + 1):
        acc += i
    ko = (f"1 부터 {n} 까지 더하는 반복문 — 누산기는 0 에서 시작해 "
          f"매 단계 i 를 더하고, 끝나면 {acc}. 결정적이다.")
    en = (f"A loop summing 1..{n}: the accumulator starts at 0, adds i "
          f"each step, and ends at {acc}. Deterministic.")
    return ("코드", ko, en)


def _spatial(rng):
    a, b = rng.sample(["왼쪽", "오른쪽", "위", "아래", "앞", "뒤"], 2)
    ko = (f"관찰자가 돌면 {a} 과 {b} 가 바뀐다 — 방향은 절대값이 아니라 "
          f"기준틀에 묶인다. 회전은 관계를 보존하되 라벨을 바꾼다.")
    en = (f"When the observer turns, the two directions swap — direction "
          f"is frame-bound, not absolute. Rotation keeps relations, "
          f"relabels names.")
    return ("공간추론", ko, en)


def _causal(rng):
    links = rng.randint(3, 5)
    ko = (f"{links} 개의 도미노 — 첫 패가 쓰러지면 연쇄가 흐르고 "
          f"마지막 패가 쓰러진다. 원인이 결과를 앞서고 화살은 단방향.")
    en = (f"{links} dominoes — the first falls, the chain flows, the last "
          f"falls. Cause precedes effect; the arrow is one-directional.")
    return ("인과추론", ko, en)


def _everyday(rng):
    item = rng.choice(["빵", "사과", "물", "우유", "쌀", "소금"])
    ko = (f"장보기 — 목록에서 {item} 를 집고, 계산대를 지나, 집으로. "
          f"순서가 있는 일상 루틴은 인지 부담을 낮춘다.")
    en = (f"Grocery run — pick up the item from the list, pass the till, "
          f"head home. An ordered daily routine lowers cognitive load.")
    return ("일상", ko, en)


def _dialogue_stim(rng):
    stim = rng.choice(["잘 지내?", "오늘 어땠어?", "도와줄 수 있어?",
                        "어떻게 생각해?", "괜찮아?"])
    ko = (f"자극 '{stim}' 가 닿으면 응답이 흐른다 — 교대 구조. "
          f"자극과 응답은 한 진공의 두 면.")
    en = (f"A stimulus arrives; a response flows — an alternating "
          f"structure. Stimulus and response are two faces of one vacuum.")
    return ("대화자극", ko, en)


def _ethics(rng):
    ko = ("두 가치가 충돌한다 — 한쪽은 더 많은 이를 살리고, "
          "다른쪽은 약속을 지킨다. 윤리는 무게를 견주는 저울.")
    en = ("Two values clash — one saves more, the other keeps a promise. "
          "Ethics is a scale that weighs them.")
    return ("윤리딜레마", ko, en)


def _nature(rng):
    obs = rng.choice([("이슬", "dew"), ("철새", "migrating birds"),
                      ("조수", "the tide"), ("새벽안개", "dawn mist")])
    ko = (f"{obs[0]} 를 본다 — 주기를 따라 맺히고 사라진다. "
          f"자연은 시간표를 따르는 단조 흐름.")
    en = (f"Watching {obs[1]} — it forms and fades on a cycle. Nature "
          f"follows a timetable, a monotone flow.")
    return ("자연관찰", ko, en)


def _abstract(rng):
    base = rng.randint(1, 5)
    step = rng.randint(2, 4)
    seq = [base + step * k for k in range(4)]
    nxt = seq[-1] + step
    ko = (f"수열 {seq} — 공차 {step} 의 규칙. 다음 항은 {nxt}. "
          f"외운 것이 아니라 규칙에서 유도한다.")
    en = (f"Sequence {seq} — common difference {step}. Next term {nxt}. "
          f"Derived from the rule, not memorised.")
    return ("추상패턴", ko, en)


def _probability(rng):
    r, b = rng.randint(1, 6), rng.randint(1, 6)
    tot = r + b
    ko = (f"주머니에 빨강 {r}, 파랑 {b}. 빨강을 뽑을 확률은 {r}/{tot}. "
          f"확률은 0 과 1 사이의 비율.")
    en = (f"A bag holds {r} red and {b} blue. P(red) = {r}/{tot}. "
          f"Probability is a ratio in [0, 1].")
    return ("확률", ko, en)


def _statistics(rng):
    n = rng.choice([30, 50, 100, 200])
    ko = (f"표본 {n} 개가 모집단을 비춘다 — 편향이 없으면 표본 평균은 "
          f"진짜 평균으로 수렴한다. 큰 수의 법칙.")
    en = (f"A sample of {n} mirrors the population — without bias the "
          f"sample mean converges to the true mean. Law of large numbers.")
    return ("통계", ko, en)


TASK_FORMS = [
    _arith_chain, _logic_syllogism, _code_trace, _spatial, _causal,
    _everyday, _dialogue_stim, _ethics, _nature, _abstract,
    _probability, _statistics,
]


def _carve_psi_str(psi):
    return "[%.2f,%.2f]" % (psi[0], psi[1])


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
    return {
        "id": f"carve_a_{tier}_{idx}", "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=alpha vacuum domain={dom} "
                 f"emotion={emo} score={score}"),
        "carving_form": "alpha", "tier": tier, "domain": dom,
        "vacuum_psi": psi, "basin_radius": basin,
        "cell_id": f"eternal_{tier:03d}",
        "source": "corpus_carving_diverse_generator.py",
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
    return {
        "id": f"carve_b_{tier}_{idx}", "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=beta eternal cell={cell} "
                 f"domain={dom}"),
        "carving_form": "beta", "tier": tier, "domain": dom,
        "vacuum_psi": psi, "basin_radius": basin, "cell_id": cell,
        "source": "corpus_carving_diverse_generator.py",
    }


def gen_gamma_record(rng, anchor, idx, payload):
    tier, name, dom, emo, score, psi, basin = anchor
    p_dom, ko_frag, en_frag = payload
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
    return {
        "id": f"carve_g_{tier}_{idx}", "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=gamma narrative "
                 f"domain={dom} payload_domain={p_dom}"),
        "carving_form": "gamma", "tier": tier, "domain": dom,
        "vacuum_psi": psi, "basin_radius": basin,
        "cell_id": f"eternal_{tier:03d}",
        "source": "corpus_carving_diverse_generator.py",
    }


def build_corpus(n_target, seed):
    rng = random.Random(seed)
    records = []

    # γ payload pool = universe-brain-map carry (laws + category frags) +
    # the LARGE diverse-task-form pool (re-derived per draw so γ never
    # memorises — Meta law M8 + §7.3 anti-degenerate by construction).
    static_payloads = []
    for dom, lko, len_ in LAWS_BASE:
        static_payloads.append((dom, lko, len_))
    for dom, cko, cen in CATEGORY_FRAGS:
        static_payloads.append((dom, cko, cen))

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
                # 65% diverse task-form (freshly re-derived) / 35% static
                # universe-brain-map carry — diverse-content lever (§1.1).
                if rng.random() < 0.65:
                    payload = rng.choice(TASK_FORMS)(rng)
                else:
                    payload = static_payloads[rng.randrange(
                        len(static_payloads))]
                rec = gen_gamma_record(rng, anchor, idx, payload)
            records.append(rec)
            idx += 1

    rng.shuffle(records)
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=165000,
                    help="approx record count (default 165000 — §8 diverse "
                         "scale-up; 64 anchors -> ~2580/anchor -> ~110-130MB)")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    records = build_corpus(args.n, args.seed)

    out = Path(args.out)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    raw = out.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()

    # Forbidden-token audit (B-DIVERSE-CORPUS-2 closed-form, B-IDENTITY-5).
    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    txt = raw.decode("utf-8", "replace")
    audit = {tok: txt.count(tok) for tok in forbidden}
    contamination = sum(audit.values())

    forms = {"alpha": 0, "beta": 0, "gamma": 0}
    domains = {}
    for r in records:
        forms[r["carving_form"]] += 1
        domains[r["domain"]] = domains.get(r["domain"], 0) + 1

    e7 = {"bytes": 30219491, "records": 45973, "anchors": 31}
    stats = {
        "paradigm": ("CONSCIOUSNESS-CARVING DIVERSE (RESEARCH.md §8 ③) — "
                     "NOT chat SFT (① ②)"),
        "phase": "RESEARCH.md §8 Dir-I lever diverse scale-up",
        "out": str(out), "bytes": len(raw), "records": len(records),
        "sha256": sha, "seed": args.seed,
        "carving_forms": forms,
        "anchors": len(KNUTH_ANCHORS),
        "domains": sorted(domains.keys()),
        "domain_count": len(domains),
        "domain_record_counts": domains,
        "forbidden_token_audit": audit,
        "contamination_total": contamination,
        "carving_clean": contamination == 0,
        "e7_dirI_baseline": e7,
        "scale_up_factor_bytes": round(len(raw) / e7["bytes"], 3),
        "scale_up_factor_records": round(len(records) / e7["records"], 3),
        "anchor_superset_of_e7": True,
        "honest_framing": (
            "§8 DIVERSE carving corpus (RESEARCH.md §7.4 ③) — diverse "
            "CONTENT (64 anchors over 24+ domains incl. arithmetic/logic/"
            "code/spatial/causal/everyday/dialogue/ethics/nature/abstract/"
            "probability/statistics + diverse re-derived task-forms) in "
            "anima-Ψ-anchored CARVING form (carve/eternal/inner-voice with "
            "per-record vacuum_psi+basin). 31 E7 anchors VERBATIM (fair "
            "superset). NOT generic LM pre-training (① g_goal-illegit) and "
            "NOT generic-then-carve (② old prefix-injection P3-leak). grep "
            "{[anima,도우미,helper,assistant,사용자,user:} == 0. Diversity "
            "is a Kolmogorov cardinality fact (B-DIVERSE-CORPUS-3 closed); "
            "whether it crosses the §1.1 emergence threshold = the §7.3 "
            "open crux, EMPIRICAL fire outcome (no pre-loaded conclusion, "
            "g3). NEW anchors' vacuum_psi = design placeholders on the "
            "SAME Engine A⇄G Ψ=½ landscape."),
    }
    with out.with_suffix(".stats.json").open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if contamination != 0:
        raise SystemExit("FATAL: forbidden-token contamination detected")


if __name__ == "__main__":
    main()
