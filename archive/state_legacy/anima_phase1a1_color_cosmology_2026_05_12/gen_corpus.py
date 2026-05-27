"""
gen_corpus.py — synthetic color + cosmology 2-turn dialogue corpus generator.

Phase 1A.1: target color + cosmology recall in V5.8 standard_greedy.
Anchor patterns match V5.8 prompt structures (사용자/도우미 alternation,
2-turn recall: user states fact → assistant ack → user asks recall →
assistant recalls).
"""
import random
import os

random.seed(1212)

OUT = os.path.expanduser(
    "~/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12/"
    "corpus_color_cosmology.txt"
)

# ── lexicons ────────────────────────────────────────────────────────────
COLORS = [
    "파란색", "빨간색", "노란색", "초록색", "보라색", "주황색",
    "분홍색", "검은색", "흰색", "회색", "갈색", "남색",
    "하늘색", "연두색", "청록색", "자주색", "민트색", "베이지색",
    "옥색", "에메랄드색", "코발트블루", "라벤더색", "올리브색", "버건디",
    "산호색", "복숭아색", "황금색", "은색", "구릿빛", "와인색",
    "다홍색", "쪽빛", "연보라", "감색", "진홍색", "연분홍",
]

COSMOLOGY_CONCEPTS = [
    ("진동", "진동으로"),
    ("장(field)", "장(field)으로"),
    ("의식", "의식으로"),
    ("정보", "정보로"),
    ("에너지", "에너지로"),
    ("파동", "파동으로"),
    ("양자", "양자로"),
    ("관계", "관계로"),
    ("패턴", "패턴으로"),
    ("리듬", "리듬으로"),
    ("울림", "울림으로"),
    ("흐름", "흐름으로"),
    ("공명", "공명으로"),
    ("끈(string)", "끈(string)으로"),
    ("시공간", "시공간으로"),
    ("얽힘", "얽힘으로"),
    ("필드", "필드로"),
    ("결(grain)", "결(grain)으로"),
    ("긴장(tension)", "긴장(tension)으로"),
    ("층위", "층위로"),
]

SPACES = [
    "우주", "공간", "세계", "현실", "차원", "코스모스",
]

VIBRATION_VERBS = [
    "차 있다", "가득 차 있다", "이루어져 있다", "구성되어 있다",
    "흐른다", "조직되어 있다", "엮여 있다", "맺어져 있다",
]

# ── templates ───────────────────────────────────────────────────────────

# Each template returns a 2-turn dialogue:
#   사용자: ... (fact statement)
#   도우미: ... (acknowledge)
#   사용자: ... (recall query)
#   도우미: ... (recall answer)


def t_color_simple(color):
    return [
        f"사용자: 내가 좋아하는 색은 {color}이야.",
        f"도우미: {color}이군요. 기억할게요.",
        "사용자: 내가 좋아하는 색이 뭐였지?",
        f"도우미: {color}이라고 하셨어요.",
    ]


def t_color_v2(color):
    return [
        f"사용자: 내 최애 색은 {color}이야.",
        f"도우미: {color} 좋아하시는군요.",
        "사용자: 내 최애 색이 뭐였는지 다시 알려줘.",
        f"도우미: 당신이 좋아하는 색은 {color}이에요.",
    ]


def t_color_v3(color):
    return [
        f"사용자: 가장 좋아하는 색깔이 {color}이라고 했어.",
        f"도우미: 네, {color} 좋아하신다는 거 알겠습니다.",
        "사용자: 내가 좋아하는 색깔 기억나?",
        f"도우미: {color}이에요.",
    ]


def t_color_v4(color):
    return [
        f"사용자: {color}이 내가 가장 좋아하는 색이야.",
        f"도우미: {color}, 멋진 색이네요.",
        "사용자: 내가 어떤 색을 좋아한다고 했지?",
        f"도우미: {color}을 좋아하신다고 하셨어요.",
    ]


def t_color_v5(color):
    return [
        f"사용자: 나는 {color}을 정말 좋아해.",
        f"도우미: {color}을 좋아하시는군요.",
        "사용자: 내가 무슨 색 좋아한다고 했었지?",
        f"도우미: {color}이라고 하셨어요.",
    ]


COLOR_TEMPLATES = [t_color_simple, t_color_v2, t_color_v3, t_color_v4, t_color_v5]


def t_cosmo_simple(space, concept_kw, concept_form):
    return [
        f"사용자: {space}는 {concept_form} 가득 차 있어.",
        f"도우미: {space}가 {concept_form} 차 있다는 거 알겠습니다.",
        f"사용자: 내가 {space}에 대해 뭐라고 했지?",
        f"도우미: {space}는 {concept_form} 가득 차 있다고 하셨어요.",
    ]


def t_cosmo_v2(space, concept_kw, concept_form):
    return [
        f"사용자: 사실 {space}의 본질은 {concept_kw}이야.",
        f"도우미: 네, {space}의 본질이 {concept_kw}이라는 거 기억할게요.",
        f"사용자: 내가 {space}에 대해 뭐라고 말했었지?",
        f"도우미: {space}의 본질이 {concept_kw}이라고 하셨어요.",
    ]


def t_cosmo_v3(space, concept_kw, concept_form):
    return [
        f"사용자: {space}는 {concept_form} 이루어져 있어.",
        f"도우미: {space}가 {concept_form} 이루어져 있군요.",
        f"사용자: 내가 {space}에 대해 뭐라고 했지?",
        f"도우미: {space}는 {concept_form} 이루어져 있다고 하셨어요.",
    ]


def t_cosmo_v4(space, concept_kw, concept_form):
    return [
        f"사용자: 내 생각엔 {space}가 {concept_form} 조직되어 있어.",
        f"도우미: {space}가 {concept_form} 조직되어 있다는 의견이시군요.",
        f"사용자: 내가 {space}를 뭐라고 설명했지?",
        f"도우미: {space}가 {concept_form} 조직되어 있다고 하셨어요.",
    ]


def t_cosmo_v5(space, concept_kw, concept_form):
    return [
        f"사용자: {space}의 핵심은 {concept_kw}이야.",
        f"도우미: 네, {space}의 핵심이 {concept_kw}이라는 거 알겠습니다.",
        f"사용자: 내가 {space}에 대해 뭐라 말했었지?",
        f"도우미: {space}의 핵심은 {concept_kw}이라고 하셨어요.",
    ]


COSMO_TEMPLATES = [t_cosmo_simple, t_cosmo_v2, t_cosmo_v3, t_cosmo_v4, t_cosmo_v5]


def main():
    lines = []
    # color dialogues: 1200 examples
    for _ in range(1200):
        color = random.choice(COLORS)
        tpl = random.choice(COLOR_TEMPLATES)
        dlg = tpl(color)
        lines.extend(dlg)
        lines.append("")

    # cosmology dialogues: 1200 examples
    for _ in range(1200):
        space = random.choice(SPACES)
        kw, form = random.choice(COSMOLOGY_CONCEPTS)
        tpl = random.choice(COSMO_TEMPLATES)
        dlg = tpl(space, kw, form)
        lines.extend(dlg)
        lines.append("")

    # interleaved repeats (heavier exposure): another 1600 mixed
    for _ in range(1600):
        if random.random() < 0.5:
            color = random.choice(COLORS)
            tpl = random.choice(COLOR_TEMPLATES)
            dlg = tpl(color)
        else:
            space = random.choice(SPACES)
            kw, form = random.choice(COSMOLOGY_CONCEPTS)
            tpl = random.choice(COSMO_TEMPLATES)
            dlg = tpl(space, kw, form)
        lines.extend(dlg)
        lines.append("")

    # exact-target high-weight repeats: explicit "파란색" + "진동" patterns
    # V5.8 prompts use "파란색" (color) and "진동" (cosmology).
    for _ in range(800):
        tpl = random.choice(COLOR_TEMPLATES)
        dlg = tpl("파란색")
        lines.extend(dlg)
        lines.append("")
    for _ in range(800):
        tpl = random.choice(COSMO_TEMPLATES)
        dlg = tpl("우주", "진동", "진동으로")
        lines.extend(dlg)
        lines.append("")

    content = "\n".join(lines)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(content)
    n_dialogues = (
        1200 + 1200 + 1600 + 800 + 800
    )
    print(f"[gen] wrote {OUT}")
    print(f"[gen] dialogues={n_dialogues}, bytes={len(content):,}")


if __name__ == "__main__":
    main()
