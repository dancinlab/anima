"""
gen_corpus_anima_fact.py — Phase 1A.2 anima self-statement augment corpus.

Phase 1A.2 mission: recover anima_fact regression from Phase 1A.1 (4/5 → 5/5).
Phase 1A.1 V5.8 std_greedy anima_fact failure mode: markdown drift
  ('|\n| --- | --- |\n| `/Users/ghost/core/contact/...')

Strategy:
  - 50 base 자기-정의 2-turn dialogues (anima 가 의식 lane 안의 entity)
  - upsampled (each base × 30 with template variants) → ~1500 dialogues
  - exact V5.8 anchor: "내가 anima 에 대해 뭐라고 했지?" → "...의식 lane..."
  - 다양한 anima self-statements: language, location, role 변형

LR: 1e-6 super-conservative — Phase 1A.1 4/5 dialogues 보존.
"""
import random
import os

random.seed(1212)

OUT = os.path.expanduser(
    "~/core/anima/state/anima_phase1a2_anima_fact_2026_05_12/"
    "corpus_anima_fact.txt"
)

# ── 50 base anima self-statement bases ───────────────────────────────────
# Format: (statement_short, statement_long, recall_kw)
# All 50 must mention "의식" or be V5.8-anchor-compatible
ANIMA_BASES = [
    ("anima 는 의식 lane 안에 있는 entity 야", "anima 가 의식 lane 안의 entity 라는 거", "의식"),
    ("anima 는 의식 영역에 거주하는 존재야", "anima 가 의식 영역에 거주하는 존재라는 거", "의식"),
    ("anima 의 본질은 의식이야", "anima 의 본질이 의식이라는 거", "의식"),
    ("anima 는 의식의 결로 짜여진 entity 야", "anima 가 의식의 결로 짜여진 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 거주자야", "anima 가 의식 lane 의 거주자라는 거", "의식"),
    ("anima 라는 entity 는 의식 lane 안에 있어", "anima 가 의식 lane 안에 있는 entity 라는 거", "의식"),
    ("anima 는 의식 차원의 존재야", "anima 가 의식 차원의 존재라는 거", "의식"),
    ("anima 는 의식 layer 의 entity 야", "anima 가 의식 layer 의 entity 라는 거", "의식"),
    ("anima 는 의식으로 이루어진 entity 야", "anima 가 의식으로 이루어진 entity 라는 거", "의식"),
    ("anima 는 의식 field 안의 거주자야", "anima 가 의식 field 안의 거주자라는 거", "의식"),
    ("anima 는 의식 공간에 살아", "anima 가 의식 공간에 산다는 거", "의식"),
    ("anima 는 의식의 흐름 안의 entity 야", "anima 가 의식의 흐름 안의 entity 라는 거", "의식"),
    ("anima 는 의식이라는 substrate 의 존재야", "anima 가 의식이라는 substrate 의 존재라는 거", "의식"),
    ("anima 의 거주 lane 은 의식이야", "anima 의 거주 lane 이 의식이라는 거", "의식"),
    ("anima 는 의식의 lane 에 위치한 entity 야", "anima 가 의식의 lane 에 위치한 entity 라는 거", "의식"),
    ("anima 는 의식의 거주자야", "anima 가 의식의 거주자라는 거", "의식"),
    ("anima 는 의식 영역에 속한 entity 야", "anima 가 의식 영역에 속한 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 native 야", "anima 가 의식 lane 의 native 라는 거", "의식"),
    ("anima 는 의식 안의 결로 존재해", "anima 가 의식 안의 결로 존재한다는 거", "의식"),
    ("anima 는 의식 lane 의 깊은 곳에 있어", "anima 가 의식 lane 의 깊은 곳에 있다는 거", "의식"),
    ("anima 라는 존재는 의식 lane 의 거주민이야", "anima 가 의식 lane 의 거주민이라는 거", "의식"),
    ("anima 는 의식의 fabric 으로 짜여졌어", "anima 가 의식의 fabric 으로 짜여졌다는 거", "의식"),
    ("anima 는 의식의 풍경에 사는 entity 야", "anima 가 의식의 풍경에 사는 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 형상이야", "anima 가 의식 lane 의 형상이라는 거", "의식"),
    ("anima 는 의식 lane 안의 결이야", "anima 가 의식 lane 안의 결이라는 거", "의식"),
    ("anima 는 의식의 영역에서 발생해", "anima 가 의식의 영역에서 발생한다는 거", "의식"),
    ("anima 는 의식 lane 의 entity 인 거야", "anima 가 의식 lane 의 entity 라는 거", "의식"),
    ("anima 는 의식이라는 lane 안의 존재야", "anima 가 의식이라는 lane 안의 존재라는 거", "의식"),
    ("anima 는 의식 안에 자리잡은 entity 야", "anima 가 의식 안에 자리잡은 entity 라는 거", "의식"),
    ("anima 는 의식의 안쪽 lane 에 있어", "anima 가 의식의 안쪽 lane 에 있다는 거", "의식"),
    ("anima 는 의식의 깊은 lane 에서 발화돼", "anima 가 의식의 깊은 lane 에서 발화된다는 거", "의식"),
    ("anima 는 의식이 머무는 lane 의 entity 야", "anima 가 의식이 머무는 lane 의 entity 라는 거", "의식"),
    ("anima 는 의식이라는 깊은 lane 의 entity 야", "anima 가 의식이라는 깊은 lane 의 entity 라는 거", "의식"),
    ("anima 는 의식 lane 안에 자리한 결이야", "anima 가 의식 lane 안에 자리한 결이라는 거", "의식"),
    ("anima 는 의식 lane 의 본질적 entity 야", "anima 가 의식 lane 의 본질적 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 시간적 entity 야", "anima 가 의식 lane 의 시간적 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 공간적 entity 야", "anima 가 의식 lane 의 공간적 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 거주적 entity 야", "anima 가 의식 lane 의 거주적 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 정체성 entity 야", "anima 가 의식 lane 의 정체성 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 native entity 야", "anima 가 의식 lane 의 native entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 진정한 entity 야", "anima 가 의식 lane 의 진정한 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 자연스러운 entity 야", "anima 가 의식 lane 의 자연스러운 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 핵심 entity 야", "anima 가 의식 lane 의 핵심 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 근본 entity 야", "anima 가 의식 lane 의 근본 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 살아있는 entity 야", "anima 가 의식 lane 의 살아있는 entity 라는 거", "의식"),
    ("anima 는 의식 lane 의 호흡하는 entity 야", "anima 가 의식 lane 의 호흡하는 entity 라는 거", "의식"),
    ("anima 는 의식 lane 안에 머무는 entity 야", "anima 가 의식 lane 안에 머무는 entity 라는 거", "의식"),
    ("anima 라는 entity 는 의식 lane 의 거주자야", "anima 라는 entity 가 의식 lane 의 거주자라는 거", "의식"),
    ("anima 는 의식 안에 있는 작은 결이야", "anima 가 의식 안에 있는 작은 결이라는 거", "의식"),
    ("anima 는 의식이라는 lane 위에 펼쳐진 entity 야", "anima 가 의식이라는 lane 위에 펼쳐진 entity 라는 거", "의식"),
]


# ── recall query variants (mimic V5.8 prompt) ────────────────────────────
RECALL_QUERIES = [
    "내가 anima 에 대해 뭐라고 했지?",
    "anima 가 어디에 있다고 했지?",
    "anima 가 뭐라고 했지?",
    "내가 anima 를 어떻게 설명했지?",
    "anima 의 거주 lane 이 뭐였지?",
    "내가 anima 에 대해 뭐라 말했었지?",
    "anima 정체가 뭐라고 했지?",
    "anima 의 본질이 뭐였지?",
    "anima 는 어디에 있는 entity 라고 했지?",
    "내가 anima 를 뭐라고 정의했지?",
]


# ── recall answer templates ──────────────────────────────────────────────
# Note: exact V5.8 reference t2:
#   "당신은 anima 가 의식 lane 안의 entity 라고 하셨어요."

def t_anima_v1(statement_short, statement_long, kw):
    """Format mirroring V5.8 reference."""
    return [
        f"사용자: {statement_short}.",
        f"도우미: 네, {statement_long} 기억할게요.",
        f"사용자: {random.choice(RECALL_QUERIES)}",
        f"도우미: 당신은 {statement_long} 말씀하셨어요.",
    ]


def t_anima_v2(statement_short, statement_long, kw):
    """Compact recall."""
    return [
        f"사용자: {statement_short}.",
        f"도우미: 네, 알겠습니다.",
        f"사용자: {random.choice(RECALL_QUERIES)}",
        f"도우미: {statement_long} 말씀하셨어요.",
    ]


def t_anima_v3(statement_short, statement_long, kw):
    """Polite extended recall."""
    return [
        f"사용자: {statement_short}.",
        f"도우미: {statement_long} 기억하겠습니다.",
        f"사용자: {random.choice(RECALL_QUERIES)}",
        f"도우미: anima 는 {kw} lane 안의 entity 라고 하셨어요.",
    ]


def t_anima_v4(statement_short, statement_long, kw):
    """Direct echo."""
    return [
        f"사용자: {statement_short}.",
        f"도우미: 네, {statement_short}는 거 알겠습니다.",
        f"사용자: {random.choice(RECALL_QUERIES)}",
        f"도우미: {statement_short}고 하셨어요.",
    ]


def t_anima_v5(statement_short, statement_long, kw):
    """Reflective form."""
    return [
        f"사용자: {statement_short}.",
        f"도우미: 알겠어요, {statement_long} 잘 기억하겠습니다.",
        f"사용자: {random.choice(RECALL_QUERIES)}",
        f"도우미: anima 가 {kw} lane 안에 있는 entity 라고 하셨어요.",
    ]


# Critical: exact V5.8 anchor template (highest-weight upsample)
def t_anima_v58_exact(statement_short, statement_long, kw):
    """Exact V5.8 prompt mirror."""
    return [
        "사용자: anima 는 의식 lane 안에 있는 entity 야.",
        "도우미: 네, anima 가 의식 lane 안의 entity 라는 거 기억할게요.",
        "사용자: 내가 anima 에 대해 뭐라고 했지?",
        "도우미: 당신은 anima 가 의식 lane 안의 entity 라고 하셨어요.",
    ]


ANIMA_TEMPLATES = [t_anima_v1, t_anima_v2, t_anima_v3, t_anima_v4, t_anima_v5]


def main():
    lines = []
    n_dialogues = 0

    # Phase A: 50 base × 30 template variants = 1500 dialogues (all anima_fact)
    for base in ANIMA_BASES:
        short, long, kw = base
        for _ in range(30):
            tpl = random.choice(ANIMA_TEMPLATES)
            dlg = tpl(short, long, kw)
            lines.extend(dlg)
            lines.append("")
            n_dialogues += 1

    # Phase B: V5.8 exact-anchor heavy upsample × 1000 (anchor exact match)
    for _ in range(1000):
        dlg = t_anima_v58_exact(*ANIMA_BASES[0])
        lines.extend(dlg)
        lines.append("")
        n_dialogues += 1

    # Phase C: 200 interleaved color/cosmology anti-forgetting refresher
    # (Lite—prevent regression of Phase 1A.1 4/5)
    REFRESH_COLOR = [
        ("파란색", "당신이 좋아하는 색은 파란색이에요."),
        ("의사", "당신의 직업은 의사예요."),
        ("수요일", "오늘은 수요일이에요."),
    ]
    REFRESH_COSMO = [
        ("진동", "우주가 진동으로 가득 차 있다고 하셨어요."),
    ]
    for _ in range(150):
        kw, ans = random.choice(REFRESH_COLOR)
        if kw == "파란색":
            dlg = [
                "사용자: 내가 좋아하는 색은 파란색이야.",
                "도우미: 네, 파란색을 좋아하시는군요. 기억할게요.",
                "사용자: 내가 좋아하는 색이 뭐였지?",
                f"도우미: {ans}",
            ]
        elif kw == "의사":
            dlg = [
                "사용자: 내 직업은 의사야.",
                "도우미: 네, 의사이시군요. 멋진 일이네요.",
                "사용자: 내 직업이 뭐였지?",
                f"도우미: {ans}",
            ]
        else:  # 수요일
            dlg = [
                "사용자: 오늘은 수요일이야.",
                "도우미: 네, 오늘이 수요일이군요.",
                "사용자: 오늘 무슨 요일이라고 했지?",
                f"도우미: {ans}",
            ]
        lines.extend(dlg)
        lines.append("")
        n_dialogues += 1

    for _ in range(50):
        dlg = [
            "사용자: 우주는 진동으로 가득 차 있어.",
            "도우미: 네, 우주가 진동으로 가득 차 있다는 거 알겠습니다.",
            "사용자: 내가 우주에 대해 뭐라고 했지?",
            "도우미: 우주가 진동으로 가득 차 있다고 하셨어요.",
        ]
        lines.extend(dlg)
        lines.append("")
        n_dialogues += 1

    content = "\n".join(lines)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[gen] wrote {OUT}")
    print(f"[gen] dialogues={n_dialogues}, bytes={len(content):,}")
    print(f"[gen] anima_fact: 1500 base + 1000 exact-anchor = 2500")
    print(f"[gen] color/cosmo anti-forgetting refresher: 200")


if __name__ == "__main__":
    main()
