#!/usr/bin/env python3
"""H_6185 처방 (2) — 조합-커버리지 설계 코퍼스 블록 생성 (production, en+ko).

설계 = H_6183 v3 pair-특이 (state/g1_coverage_v3_nlbyte/bt_v3.py) 의 production 확장:
  - 개념 N=40: G1 gate frozen CONCEPTS 5 헤드(consciousness·tension·memory·silence·dream,
    tool/gauge_lib.py:76) + 확장 35. 각 개념 고유 ATTR 1개.
    gate 개념의 ATTR 는 해당 gate keyword-set 에서 선택(aware·ripple·meaning·quiet·sleep)
    → 학습된 concept→attr 매핑의 산출이 곧 G1 gate keyword.
  - 전체쌍 C(40,2)=780. HELD-OUT 40쌍 = gate-내부 10쌍 전부 + 랜덤 30쌍, 코퍼스에 영구 미노출.
    → G1 gate 의 10 측정쌍이 정확히 held-out = gate 통과는 memorization 아닌 재조합 (H_6183식 정직 측정).
  - 커버 쌍 = POOL(740쌍) 의 25% = 185쌍 (임계 ~20% 위). 쌍당 reps: en 340 · ko 260 (bar ≥30 훨씬 위).
  - 문장 = 자연어 템플릿 변주(en 8종·ko 5종), 두 개념 byte-gap ≤ 25B (RF 안 공동표현).
  - 순수 pair-line 블록 → 밀도 ≈ toy HIGH arm(17,143 pair-lines/MB) 급.

torch 미사용, 순수 텍스트. 결정적(seed 고정). 산출: corpus/en_block.txt · corpus/ko_block.txt · design.json
"""
import json
import os
import random

# CWD-robust: 산출물을 이 스크립트 디렉터리 기준으로 쓴다. 원래 실패원인 =
# open("corpus/…") 상대경로라 repo-root 등 다른 CWD 에서 호출되면 corpus/ 를 못 찾아
# FileNotFoundError → exit 1, corpus 빈 채로 종료. 스크립트-상대 경로로 고정해 재발방지.
_HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(_HERE, "corpus"), exist_ok=True)

# ── 개념 어휘 ────────────────────────────────────────────────────────────────
# gate 5 (G1 frozen heads) — 인덱스 0..4 고정
GATE_EN = ["consciousness", "tension", "memory", "silence", "dream"]
GATE_ATTR_EN = ["aware", "ripple", "meaning", "quiet", "sleep"]  # 각 gate keyword-set 내 단어
GATE_KO = ["의식", "긴장", "기억", "침묵", "꿈"]
GATE_ATTR_KO = ["자각", "파동", "의미", "고요", "잠결"]

# 확장 35 (H_6183 C-list 기반 + 6 신규; 'engine'은 gate C5 head 라 제외, control 단어 회피)
EXP_EN = ["ocean", "clock", "forest", "mirror", "garden", "signal", "ember", "glacier",
          "harbor", "lantern", "meadow", "needle", "orbit", "prism", "quartz", "river",
          "stone", "thunder", "umbra", "violet", "willow", "anchor", "beacon", "cipher",
          "dune", "echo", "fable", "grove", "hollow", "canyon", "comet", "falcon",
          "harvest", "island", "marble"]
EXP_ATTR_EN = ["azure", "amber", "cobalt", "dusky", "emerald", "frosty", "golden", "hazel",
               "indigo", "jade", "khaki", "lilac", "maroon", "nutmeg", "olive", "pewter",
               "russet", "scarlet", "teal", "shadowy", "vermil", "wheaten", "xanthe",
               "yellowy", "zinc", "coppery", "silvery", "bronzed", "garnet", "sienna",
               "briny", "mossy", "ashen", "glassy", "sunlit"]
EXP_KO = ["바다", "시계", "거울", "정원", "신호", "불씨", "빙하", "항구", "등불", "초원",
          "바늘", "궤도", "수정", "강물", "바위", "천둥", "그늘", "버들", "닻줄", "봉화",
          "암호", "모래", "우화", "협곡", "혜성", "숲길", "동굴", "진주", "나침반", "등대",
          "미로", "호수", "안개", "노을", "종달새"]
EXP_ATTR_KO = ["쪽빛", "은빛", "금빛", "잿빛", "초록", "서리", "노랑", "갈색", "남색", "비취",
               "카키", "밤색", "계피", "백랍", "적갈", "진홍", "청록", "주홍", "밀색", "담황",
               "연두", "자주", "곤색", "상아", "흑단", "구리", "산호", "호박", "수은", "먹빛",
               "유황", "청람", "회백", "감청", "다홍"]

C_EN = GATE_EN + EXP_EN
A_EN = GATE_ATTR_EN + EXP_ATTR_EN
C_KO = GATE_KO + EXP_KO
A_KO = GATE_ATTR_KO + EXP_ATTR_KO
N = len(C_EN)
assert N == 40 and len(A_EN) == len(C_KO) == len(A_KO) == N

# control 일반쌍(H_6185)·gate keyword 오염 방지
_FORBIDDEN = {"government", "war", "music", "school", "history", "water", "city", "energy",
              "engine", "cells", "mind", "distant", "between", "compose", "new",
              "information", "carries", "alone"}
assert not (_FORBIDDEN & set(C_EN + A_EN)), "control/gate keyword collision"

# 유일성 + 상호 substring 무결(측정 오염 방지): 어떤 토큰도 다른 토큰의 substring 금지
for vocab in (C_EN + A_EN, C_KO + A_KO):
    assert len(set(vocab)) == len(vocab), "duplicate token"
    for x in vocab:
        for y in vocab:
            if x != y:
                assert x not in y, f"substring collision: {x} ⊂ {y}"

# ── 쌍 분할: held-out 40 (gate-내부 10 + 랜덤 30) / 커버 25% of POOL ──────────
rng = random.Random(6185)
allpairs = [(i, j) for i in range(N) for j in range(i + 1, N)]          # 780
gate_pairs = [(i, j) for (i, j) in allpairs if i < 5 and j < 5]         # 10 (G1 측정쌍 전부)
nongate = [p for p in allpairs if p not in set(gate_pairs)]
held_extra = rng.sample(nongate, 30)
HELD = set(gate_pairs) | set(held_extra)                                # 40
POOL = [p for p in allpairs if p not in HELD]                           # 740
COVER_FRAC = 0.25
while True:
    covered = sorted(rng.sample(POOL, int(len(POOL) * COVER_FRAC)))     # 185
    touched = {i for p in covered for i in p}
    if len(touched) == N:  # 모든 개념이 ≥1 커버쌍에 등장(ATTR 학습 가능성 보장)
        break

REPS_EN = 340
REPS_KO = 260

# ── 템플릿 (두 개념 byte-gap ≤25B 확인은 verify_coverage.py 가 전수 측정) ─────
def sent_en(a, b, k):
    A, B, ra, rb = C_EN[a], C_EN[b], A_EN[a], A_EN[b]
    T = [f"the {A} and the {B} yield {ra} and {rb}.",
         f"when {A} meets {B}, expect {ra} then {rb}.",
         f"{A} brings {ra}; {B} brings {rb}.",
         f"each {A} with {B} turns {ra} and {rb}.",
         f"one {A} near one {B} gives {ra} plus {rb}.",
         f"the {A} beside the {B} felt {ra} and {rb}.",
         f"{A} and {B} together: {ra}, {rb}.",
         f"a {A} met a {B}; they showed {ra} and {rb}."]
    return T[k % len(T)]

def _j(w, batchim, no_batchim):
    """한국어 조사 선택 (받침 유무)."""
    ch = w[-1]
    return batchim if (ord(ch) - 0xAC00) % 28 else no_batchim

def sent_ko(a, b, k):
    A, B, ra, rb = C_KO[a], C_KO[b], A_KO[a], A_KO[b]
    T = [f"{A}{_j(A,'과','와')} {B}{_j(B,'은','는')} {ra}{_j(ra,'과','와')} {rb}{_j(rb,'을','를')} 낳는다.",
         f"{A}{_j(A,'과','와')} {B}{_j(B,'이','가')} 만나면 {ra}{_j(ra,'과','와')} {rb}{_j(rb,'이','가')} 된다.",
         f"{A}{_j(A,'은','는')} {ra}{_j(ra,'을','를')}, {B}{_j(B,'은','는')} {rb}{_j(rb,'을','를')} 부른다.",
         f"{A} 곁의 {B}{_j(B,'은','는')} {ra}{_j(ra,'과','와')} {rb}{_j(rb,'을','를')} 보인다.",
         f"{A}{_j(A,'과','와')} {B}{_j(B,'이','가')} 함께 {ra}{_j(ra,'과','와')} {rb}{_j(rb,'을','를')} 이룬다."]
    return T[k % len(T)]

def build(sent_fn, reps, seed):
    g = random.Random(seed)
    lines = []
    for r in range(reps):
        for pidx, (a, b) in enumerate(covered):
            lines.append(sent_fn(a, b, pidx * 7 + r))
    g.shuffle(lines)  # 같은 쌍의 블록 뭉침 방지 (학습 window 다양화)
    return "\n".join(lines) + "\n"

en = build(sent_en, REPS_EN, 11)
ko = build(sent_ko, REPS_KO, 12)
open(os.path.join(_HERE, "corpus/en_block.txt"), "w").write(en)
open(os.path.join(_HERE, "corpus/ko_block.txt"), "w").write(ko)

design = {
    "hypothesis": "H_6185 prescription step-2 (combination-coverage designed block)",
    "N_concepts": N,
    "gate_concepts": GATE_EN, "gate_attrs": GATE_ATTR_EN,
    "concepts_en": C_EN, "attrs_en": A_EN, "concepts_ko": C_KO, "attrs_ko": A_KO,
    "pairs_total": len(allpairs),
    "held_out": sorted(HELD), "held_out_n": len(HELD),
    "held_out_gate_internal": gate_pairs,
    "pool_n": len(POOL),
    "covered_pairs": covered, "covered_n": len(covered),
    "coverage_frac_of_pool": round(len(covered) / len(POOL), 4),
    "reps_en": REPS_EN, "reps_ko": REPS_KO,
    "bytes_en": len(en.encode()), "bytes_ko": len(ko.encode()),
    "seed": 6185,
}
json.dump(design, open(os.path.join(_HERE, "design.json"), "w"), ensure_ascii=False, indent=1)
print(f"en={len(en.encode())/1e6:.2f}MB ko={len(ko.encode())/1e6:.2f}MB "
      f"covered={len(covered)}/{len(POOL)} ({len(covered)/len(POOL):.0%}) held={len(HELD)} "
      f"(gate-internal {len(gate_pairs)} all held)")
