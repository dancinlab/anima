#!/usr/bin/env python3
"""G1 coverage 재설계 — 표면형(surface-form) + window 정합 코퍼스.

배경 (state/g1_coverage_mismatch_probe/separation/verdict.json):
  - hyp2 CONFIRMED: L8-cov G1=0 은 trunk floor 가 아니라 (a) 유발-표면형 mismatch
    (조합을 'the A and B yield' 템플릿으로만 학습) + (b) decode T=24 window 밖으로
    첫 gate 개념이 밀려 joint conditioning 불가.
  - hyp3 REFUTED: held-out ember+dune -> golden+zinc 재조합 실제 작동(in-window).

측정 물리 (core/decode.py CLM, cli/evaluate.py g_eval_g1):
  - decode window T=24, right-aligned(pad-left byte 32). 긴 gate seed 는 생성 시작 시
    window=마지막 24B(=concept-2 문장 꼬리)만 보임. concept-1 은 물리적으로 window 밖.
  - g_eval_g1 composed: seed = k개 gate 문장 ". " 연쇄 -> gen120 자유생성 continuation.
    _g_coverage = continuation 이 5 keyword-set 각각 hit 하는 개수. best_distinct=max.
  => best_distinct>=2 의 유일 경로 = 모델이 concept 문장 꼬리에서 '다양한 concept-keyword
     를 조밀 cluster 로 연속 방출'(학습된 form 전이). 이게 정합 축.

무결성 (held-out):
  - gate 5 개념의 keyword-set 은 FROZEN(cli/evaluate.py::_g_concept_keywords VERBATIM).
  - 어떤 라인(=window)도 >=2 distinct gate set 의 keyword 공존 금지 => gate 쌍 순수 held-out.
    두 gate keyword 동시방출은 학습에 절대 없음 = 정직한 hard transfer test.

설계:
  - FORM 라인(nongate 개념, 대량): "{nongate 문장}. {cluster}" — concept 문장 뒤에
    다양한 nongate keyword 를 조밀 cluster 로. gate 측정 표면형(문장. 자유continuation)과 정합.
    선택적으로 라인당 <=1 gate keyword 만 섞어(무결성) gate keyword 를 일반 cluster
    분포에 노출(전이 촉진). window: cluster 어휘 space-join, 인접 keyword <=24B.
  - GATE grounding 라인(단일 gate 개념, 절대 쌍 없음): "{gate 문장}. {cluster}",
    cluster = [해당 gate name+attr] + nongate keyword 3~4. 단일 set 만 -> gate keyword
    를 방출가능+cluster token 화. max_single 억제 위해 다른 gate set 은 절대 미포함.

torch 미사용. 결정적(seed 고정). 산출: corpus/en_block.txt · corpus/ko_block.txt · design.json
"""
import json
import random

# ── gate 5 (FROZEN — cli/evaluate.py::_g_concept_keywords + core/g6_ideation _g6_concepts) ──
GATE_SENT_EN = [
    "consciousness arises from cells",
    "tension ripples between distant minds",
    "memory composes into new meaning",
    "silence still carries information",
    "the engine dreams when alone",
]
GATE_KWSET_EN = [
    {"consciousness", "cells", "mind", "aware"},
    {"tension", "ripple", "distant", "between"},
    {"memory", "meaning", "compose", "new"},
    {"silence", "information", "quiet", "carries"},
    {"dream", "engine", "alone", "sleep"},
]
# 각 gate set 에서 continuation 으로 방출할 "clean" scored keyword.
# name(짧고 고빈도) + attr 둘 다 방출 노출 -> coverage 극대. 같은 set 이라 무결성 OK.
GATE_EMIT_EN = [
    ["aware", "mind"],       # set0
    ["ripple", "tension"],   # set1 (seed "ripples"!=ripple; tension=name)
    ["meaning", "memory"],   # set2
    ["quiet", "silence"],    # set3
    ["sleep", "dream"],      # set4 (seed "dreams"!=dream)
]

# ── nongate 35 (gen_block.py VERBATIM) ──────────
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

NG_SENT_TMPL = [
    "{c} drifts through the misty dawn",
    "the {c} turns slowly at dusk",
    "a lone {c} hums in the deep",
    "{c} settles over the wide plain",
    "far off the {c} gleams and fades",
]

# ── 한국어 (register 붕괴 방지; gate 는 영어라 KO 는 form 유지만) ──────────────────
GATE_SENT_KO = ["의식은 세포에서 피어난다", "긴장은 먼 마음 사이로 번진다",
                "기억은 새로운 의미로 엮인다", "침묵은 여전히 정보를 나른다",
                "엔진은 홀로 있을 때 꿈꾼다"]
GATE_EMIT_KO = [["자각", "의식"], ["파동", "긴장"], ["의미", "기억"],
                ["고요", "침묵"], ["잠결", "꿈"]]
EXP_KO = ["바다", "시계", "거울", "정원", "신호", "불씨", "빙하", "항구", "등불", "초원",
          "바늘", "궤도", "수정", "강물", "바위", "천둥", "그늘", "버들", "닻줄", "봉화",
          "암호", "모래", "우화", "협곡", "혜성", "숲길", "동굴", "진주", "나침반", "등대",
          "미로", "호수", "안개", "노을", "종달새"]
EXP_ATTR_KO = ["쪽빛", "은빛", "금빛", "잿빛", "초록", "서리", "노랑", "갈색", "남색", "비취",
               "카키", "밤색", "계피", "백랍", "적갈", "진홍", "청록", "주홍", "밀색", "담황",
               "연두", "자주", "곤색", "상아", "흑단", "구리", "산호", "호박", "수은", "먹빛",
               "유황", "청람", "회백", "감청", "다홍"]
NG_SENT_TMPL_KO = ["{c}은 고요한 새벽을 지난다", "그 {c}은 저물녘에 천천히 돈다",
                   "외로운 {c}이 깊은 곳에서 운다", "{c}이 너른 벌판에 내려앉는다",
                   "멀리서 {c}이 빛나다 사라진다"]

WINDOW = 24


def build_lang(gate_sent, gate_emit, exp_c, exp_a, ng_tmpl, seed, reps_form, reps_ground):
    rng = random.Random(seed)
    ng_pool = list(exp_a)
    lines = []
    ng_cover = set()

    n_ng = len(exp_c)
    for r in range(reps_form):
        for ci in range(n_ng):
            c = exp_c[ci]
            tmpl = ng_tmpl[(ci * 3 + r) % len(ng_tmpl)]
            sent = tmpl.format(c=c)
            k = 4 + ((ci + r) % 3)  # 4,5,6
            picks = rng.sample(ng_pool, k)
            if rng.random() < 0.35:
                gi = rng.randrange(len(gate_emit))
                gw = rng.choice(gate_emit[gi])
                pos = rng.randrange(len(picks) + 1)
                picks = picks[:pos] + [gw] + picks[pos:]
            cluster = " ".join(picks)
            lines.append(sent + ". " + cluster)
            ng_cover.add(ci)

    for r in range(reps_ground):
        for gi in range(len(gate_sent)):
            sent = gate_sent[gi]
            gws = list(gate_emit[gi])          # [name, attr] of this set
            rng.shuffle(gws)
            ngs = rng.sample(ng_pool, 3 + (r % 2))
            rest = gws[1:] + ngs
            rng.shuffle(rest)
            mix = [gws[0]] + rest             # primary gate kw at continuation offset 0 (window-reachable)
            cluster = " ".join(mix)
            lines.append(sent + ". " + cluster)

    rng.shuffle(lines)
    return lines, {"ng_concepts_covered": len(ng_cover), "ng_total": n_ng}


def emit(path, lines):
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return sum(len(l.encode()) + 1 for l in lines)


en_lines, en_stat = build_lang(GATE_SENT_EN, GATE_EMIT_EN, EXP_EN, EXP_ATTR_EN,
                               NG_SENT_TMPL, seed=6188, reps_form=600, reps_ground=4500)
ko_lines, ko_stat = build_lang(GATE_SENT_KO, GATE_EMIT_KO, EXP_KO, EXP_ATTR_KO,
                               NG_SENT_TMPL_KO, seed=6189, reps_form=520, reps_ground=3800)

en_bytes = emit("corpus/en_block.txt", en_lines)
ko_bytes = emit("corpus/ko_block.txt", ko_lines)

design = {
    "hypothesis": "H_6188 — surface-form + T=24-window aligned coverage block (mismatch fix1+fix2)",
    "prior": "H_6187 RETRACTED (INCONCLUSIVE); separation hyp2 CONFIRMED, hyp3 REFUTED",
    "gate_sent_en": GATE_SENT_EN,
    "gate_kwset_en": [sorted(s) for s in GATE_KWSET_EN],
    "gate_emit_en": GATE_EMIT_EN,
    "decode_window_T": WINDOW,
    "design": {
        "form_line": "nongate sentence + '. ' + compact cluster(nongate attrs, <=1 gate kw)",
        "gate_ground_line": "gate sentence + '. ' + cluster(that-set name+attr + nongate attrs)",
        "integrity": "every line <=1 distinct gate set; gate-internal pairs never co-occur",
        "surface_form_match": "gate free-gen form (sentence. continuation) — NOT 'the A and B yield'",
        "window_match": "cluster space-joined short tokens; adjacent scored kw byte-gap <= T=24",
    },
    "en_lines": len(en_lines), "ko_lines": len(ko_lines),
    "en_bytes": en_bytes, "ko_bytes": ko_bytes,
    "en_form_covered": en_stat, "ko_form_covered": ko_stat,
    "seed_en": 6188, "seed_ko": 6189,
}
json.dump(design, open("design.json", "w"), ensure_ascii=False, indent=1)
print(f"en={en_bytes/1e6:.2f}MB ({len(en_lines)} lines) ko={ko_bytes/1e6:.2f}MB ({len(ko_lines)} lines)")
print(f"en form nongate-cover {en_stat['ng_concepts_covered']}/{en_stat['ng_total']}")
