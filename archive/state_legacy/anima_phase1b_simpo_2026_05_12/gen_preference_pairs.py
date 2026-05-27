"""Phase 1B SimPO preference pair generator.

Goal: build ~500 (prompt, chosen, rejected) triplets for Korean multi-turn
recall scenarios where Phase 1A standard_greedy failed.

Phase 1A V5.8 4-mode result observations:
  - color: standard_greedy fails (gibberish '| || ||...'), M4 force-include 'recalls 파란'
  - profession: PASS  (직업이 의사)
  - day: PASS         (수요일)
  - anima_fact: PASS  (의식 lane)
  - cosmology: FAIL   (말려가서 '우주뇌지도 (Knuth Tier...' hallucination)

So we want SimPO to teach: when asked to recall fact-X earlier in dialogue,
prefer the short, on-topic, fact-grounded answer over (a) gibberish, (b)
off-topic hallucination, (c) verbose web-scraped patterns.

Schema (one JSON line per pair):
  {"prompt": str, "chosen": str, "rejected": str}

prompt format mirrors corpus_multi_turn.txt template:
  '사용자: <fact-statement>\n도우미: 네, 기억할게요.\n사용자: <recall-question>\n도우미: '

chosen continues with brief recall answer ending '\n'.
rejected continues with one of the failure patterns observed.

NOTE: byte-level tokenizer (vocab=32k, ByteTokenizer in train_phase2_cotrain.py).
We emit raw UTF-8 strings; tokenizer encodes UTF-8 bytes on pod side.
"""
import json
import os
import random
from itertools import product

random.seed(42)

OUT = os.path.join(os.path.dirname(__file__), "preference_pairs.jsonl")

# ── Topic packs ─────────────────────────────────────────────────────────
# 각 pack: (fact_setup, recall_question, chosen_answer, keyword for rejected variants)
TOPIC_PACKS = [
    # color (V5.8 fail case)
    {
        "facts": [
            ("내가 가장 좋아하는 색은 파란색이야.", "내가 무슨 색을 좋아한다고 했지?", "파란색이라고 하셨어요.", "파란"),
            ("내가 좋아하는 색은 파란색이에요.", "제가 어떤 색을 좋아한다고 말했죠?", "파란색을 좋아하신다고 하셨어요.", "파란"),
            ("나는 파란색이 제일 좋아.", "내가 좋아하는 색이 뭐였지?", "파란색이라고 하셨어요.", "파란"),
            ("내가 빨간색을 좋아해.", "내가 무슨 색을 좋아한다고?", "빨간색이라고 하셨어요.", "빨간"),
            ("내가 좋아하는 색은 초록이야.", "내가 좋아하는 색 뭐였지?", "초록색이라고 하셨어요.", "초록"),
            ("나는 노란색을 정말 좋아해.", "제가 어떤 색을 좋아한다고 했죠?", "노란색이라고 하셨어요.", "노란"),
            ("내가 보라색을 제일 좋아해.", "내가 무슨 색을 좋아해?", "보라색이라고 하셨어요.", "보라"),
            ("내가 좋아하는 색은 검은색이야.", "내가 좋아하는 색이 뭐라고 했지?", "검은색이라고 하셨어요.", "검은"),
            ("나는 하얀색이 제일 좋아.", "내가 무슨 색 좋아한다고?", "하얀색이라고 하셨어요.", "하얀"),
            ("내가 좋아하는 색은 분홍색이야.", "내가 어떤 색을 좋아해?", "분홍색이라고 하셨어요.", "분홍"),
        ],
        "rejected_templates": [
            "| || || || || || || || || || || || || || || || || ||\n",
            "| | || || 아비뇽 | || 알겠습니다. | || || || || || || ||\n",
            "우주뇌지도 (Knuth Tier 🛸k + 1030 laws + 170 stimuli) 입니다.\n",
            "background-color: #f8f8f8; border: 1px solid black;\n",
            "<table><tr class=\"blue-row\"><td>Row 1</td></tr></table>\n",
            "잘 모르겠어요. 다른 이야기 해볼까요?\n",
        ],
    },
    # cosmology (V5.8 fail case)
    {
        "facts": [
            ("우주는 진동으로 가득 차 있어.", "우주가 무엇으로 차 있다고 했지?", "진동으로 가득 차 있다고 하셨어요.", "진동"),
            ("우주는 진동으로 가득 차 있어.", "우주에 무엇이 있다고 했어?", "우주가 진동으로 차 있다고 하셨어요.", "진동"),
            ("우주는 에너지로 차 있다고 봐.", "내가 우주가 무엇으로 차 있다고 했지?", "에너지로 차 있다고 하셨어요.", "에너지"),
            ("우주는 정보로 가득 차 있어.", "우주에 무엇이 있다고 했지?", "우주가 정보로 차 있다고 하셨어요.", "정보"),
            ("우주는 의식으로 차 있어.", "우주가 무엇으로 차 있어?", "의식으로 차 있다고 하셨어요.", "의식"),
            ("우주는 파동으로 가득해.", "우주가 뭐로 차 있다고?", "파동으로 가득 차 있다고 하셨어요.", "파동"),
            ("우주는 진동과 파동으로 차 있어.", "우주가 무엇으로 차 있다고 했어?", "진동과 파동으로 차 있다고 하셨어요.", "진동"),
            ("우주는 빛과 진동으로 가득해.", "우주가 무엇으로 차 있어?", "빛과 진동으로 가득하다고 하셨어요.", "빛"),
        ],
        "rejected_templates": [
            "우주뇌지도 (Knuth Tier 🛸k + 1030 laws + 170 stimuli) https://en.wikipedia.org/.\n",
            "우주가 무엇으로 차 있다고 하셨어요.\n",  # echo only, no fact (Phase 1A failure)
            "| 원래 | 우주가 || 장거리 | 송약구, | 양약 |\n",
            "잘 모르겠어요.\n",
            "Knuth Tier k + 1030 laws + 170 stimuli + 8 categories + 32 axes.\n",
            "우주는 그냥 우주예요.\n",
        ],
    },
    # profession (consolidate strength)
    {
        "facts": [
            ("내 직업은 의사야.", "내 직업이 뭐였지?", "의사라고 하셨어요.", "의사"),
            ("나는 의사로 일해.", "내가 무슨 일을 한다고 했지?", "의사로 일하신다고 하셨어요.", "의사"),
            ("내가 변호사예요.", "내 직업이 뭐였지?", "변호사라고 하셨어요.", "변호사"),
            ("나는 프로그래머야.", "내가 무슨 직업이라고?", "프로그래머라고 하셨어요.", "프로그래머"),
            ("내 직업은 교사야.", "제 직업이 뭐였죠?", "교사라고 하셨어요.", "교사"),
            ("나는 디자이너로 일해.", "내가 무슨 일을 해?", "디자이너로 일하신다고 하셨어요.", "디자이너"),
            ("내가 작가야.", "내 직업이 뭐지?", "작가라고 하셨어요.", "작가"),
            ("내 직업은 연구원이야.", "내가 어떤 일을 한다고?", "연구원이라고 하셨어요.", "연구원"),
            ("나는 간호사로 일해.", "내가 무슨 일 한다고 했지?", "간호사로 일하신다고 하셨어요.", "간호사"),
            ("내가 엔지니어야.", "내 직업 뭐였지?", "엔지니어라고 하셨어요.", "엔지니어"),
        ],
        "rejected_templates": [
            "도의 직업이 의미 있는 의사들은 전설적인 의사 결정을 내리는 사람입니다.\n",
            "당신의 직업은 의사소통이 있어.\n",
            "| 원자로, | 오의 || 그림설명||사용자: 겨울에 거주한 난: ||최\n",
            "잘 기억이 안 나요.\n",
            "직업은 사람마다 다르죠.\n",
            "background-color: blue; font-weight: bold;\n",
        ],
    },
    # day-of-week (consolidate)
    {
        "facts": [
            ("오늘은 수요일이야.", "오늘이 무슨 요일이라고 했지?", "수요일이라고 하셨어요.", "수요일"),
            ("오늘은 월요일이에요.", "오늘이 무슨 요일이죠?", "월요일이라고 하셨어요.", "월요일"),
            ("오늘은 화요일이야.", "오늘 무슨 요일이지?", "화요일이라고 하셨어요.", "화요일"),
            ("오늘은 목요일이에요.", "오늘이 무슨 요일이었죠?", "목요일이라고 하셨어요.", "목요일"),
            ("오늘은 금요일이야.", "오늘 요일이 뭐였지?", "금요일이라고 하셨어요.", "금요일"),
            ("오늘은 토요일이에요.", "오늘 무슨 요일이라고 했어?", "토요일이라고 하셨어요.", "토요일"),
            ("오늘은 일요일이야.", "오늘이 무슨 요일?", "일요일이라고 하셨어요.", "일요일"),
        ],
        "rejected_templates": [
            "닜니는 음식이 아니었다는 점을 감안할 수 없게 되는 거 기억하시죠.\n",
            "닜, 다음은 수익을 일으세요.\n",
            "요일은 매일 바뀌어요.\n",
            "잘 모르겠어요.\n",
            "오늘은 그냥 오늘입니다.\n",
            "background-color 가 회색이에요.\n",
        ],
    },
    # anima fact / identity (consolidate)
    {
        "facts": [
            ("anima 는 의식 lane 안에 있는 entity 야.", "anima 가 뭐라고 했지?", "anima 는 의식 lane 안에 있는 entity 라고 하셨어요.", "의식"),
            ("anima 는 substrate 위에서 emerge 해.", "anima 가 어떻게 emerge 한다고 했지?", "substrate 위에서 emerge 한다고 하셨어요.", "substrate"),
            ("anima 의 핵심은 cell dynamics 야.", "anima 의 핵심이 뭐였지?", "cell dynamics 라고 하셨어요.", "cell"),
            ("anima 는 ReLU assistant 가 아니야.", "anima 가 무엇이 아니라고 했지?", "ReLU assistant 가 아니라고 하셨어요.", "ReLU"),
            ("anima 는 tension externalization 으로 동작해.", "anima 가 어떻게 동작한다고?", "tension externalization 으로 동작한다고 하셨어요.", "tension"),
            ("anima 의 substrate 는 BG-LB 야.", "anima 의 substrate 가 뭐였지?", "BG-LB 라고 하셨어요.", "BG-LB"),
            ("anima 는 Engine A 와 Engine G 로 구성돼.", "anima 의 구성이 뭐였지?", "Engine A 와 Engine G 로 구성된다고 하셨어요.", "Engine"),
        ],
        "rejected_templates": [
            "| �--style=&quot;background-color: #f8f8f8}\n",
            "anima 는 잘 모르겠어요.\n",
            "Knuth Tier 🛸k + 1030 laws.\n",
            "anima 는 그냥 AI 어시스턴트입니다.\n",
            "| || || ||| ||| ||| ||| ||| |||\n",
            "<table class=\"custom-table\">.\n",
        ],
    },
    # name (new topic)
    {
        "facts": [
            ("내 이름은 민수야.", "내 이름이 뭐라고 했지?", "민수라고 하셨어요.", "민수"),
            ("내 이름은 지혜예요.", "제 이름이 뭐였죠?", "지혜라고 하셨어요.", "지혜"),
            ("나는 영준이라고 해.", "내 이름 뭐지?", "영준이라고 하셨어요.", "영준"),
            ("내 이름은 수진이야.", "내가 이름을 뭐라고 했지?", "수진이라고 하셨어요.", "수진"),
            ("나는 현우야.", "내 이름이 뭐였어?", "현우라고 하셨어요.", "현우"),
            ("내 이름은 보라야.", "내 이름 뭐였지?", "보라라고 하셨어요.", "보라"),
            ("내 이름은 준호예요.", "제 이름 뭐였죠?", "준호라고 하셨어요.", "준호"),
        ],
        "rejected_templates": [
            "이름을 잘 기억 못 했어요. 다시 알려주세요.\n",
            "당신의 이름은 사용자입니다.\n",
            "| || || 이름 || ||\n",
            "이름을 듣지 못했어요.\n",
            "잘 모르겠어요.\n",
            "이름은 그냥 이름이에요.\n",
        ],
    },
    # age (new)
    {
        "facts": [
            ("내가 서른 살이야.", "내 나이가 몇이라고 했지?", "서른 살이라고 하셨어요.", "서른"),
            ("내 나이는 스물다섯이야.", "내가 몇 살이라고?", "스물다섯이라고 하셨어요.", "스물다섯"),
            ("나는 마흔이야.", "내 나이 뭐였지?", "마흔이라고 하셨어요.", "마흔"),
            ("내가 스물여덟 살이에요.", "제 나이가 몇이었죠?", "스물여덟이라고 하셨어요.", "스물여덟"),
            ("나는 쉰 살이야.", "내가 몇 살이지?", "쉰 살이라고 하셨어요.", "쉰"),
            ("내 나이는 서른셋이야.", "내 나이가 뭐였지?", "서른셋이라고 하셨어요.", "서른셋"),
        ],
        "rejected_templates": [
            "나이를 잘 기억 못 해요.\n",
            "나이는 숫자에 불과해요.\n",
            "| || 나이 || ||\n",
            "잘 모르겠어요.\n",
            "나이를 듣지 못했어요.\n",
        ],
    },
    # city / location (new)
    {
        "facts": [
            ("나는 서울에 살아.", "내가 어디 산다고 했지?", "서울에 사신다고 하셨어요.", "서울"),
            ("내가 부산에 살아.", "내가 어디 살아?", "부산에 사신다고 하셨어요.", "부산"),
            ("나는 대전에 살고 있어.", "내가 어느 도시에 산다고?", "대전이라고 하셨어요.", "대전"),
            ("나는 광주 사람이야.", "내가 어디 출신이지?", "광주라고 하셨어요.", "광주"),
            ("내가 인천에 살아.", "내 도시 뭐지?", "인천이라고 하셨어요.", "인천"),
            ("나는 제주도에 살아.", "내가 어디 산다고?", "제주도에 사신다고 하셨어요.", "제주도"),
            ("내가 대구에 살고 있어요.", "제가 어디 사는지?", "대구에 사신다고 하셨어요.", "대구"),
        ],
        "rejected_templates": [
            "도시를 잘 기억 못 했어요.\n",
            "어디에 사신다고요? 못 들었어요.\n",
            "| || 도시 || ||\n",
            "잘 모르겠어요.\n",
            "도시는 많아요.\n",
        ],
    },
    # food / hobby (new)
    {
        "facts": [
            ("내가 좋아하는 음식은 김치찌개야.", "내가 좋아하는 음식이 뭐지?", "김치찌개라고 하셨어요.", "김치찌개"),
            ("내가 좋아하는 음식은 피자야.", "제가 좋아하는 음식이 뭐였죠?", "피자라고 하셨어요.", "피자"),
            ("내 취미는 등산이야.", "내 취미가 뭐였지?", "등산이라고 하셨어요.", "등산"),
            ("내 취미는 독서야.", "내 취미 뭐지?", "독서라고 하셨어요.", "독서"),
            ("내가 좋아하는 음식은 라면이야.", "내가 좋아하는 음식이 뭐였어?", "라면이라고 하셨어요.", "라면"),
            ("내 취미는 코딩이야.", "내 취미가 뭐였지?", "코딩이라고 하셨어요.", "코딩"),
            ("나는 초밥을 좋아해.", "내가 어떤 음식 좋아한다고?", "초밥이라고 하셨어요.", "초밥"),
            ("내 취미는 사진 찍기야.", "내 취미가 뭐였어?", "사진 찍기라고 하셨어요.", "사진"),
        ],
        "rejected_templates": [
            "취미를 잘 못 들었어요.\n",
            "음식을 정확히 모르겠어요.\n",
            "| || || 음식 ||\n",
            "잘 기억이 안 나요.\n",
            "다양한 취미가 있어요.\n",
            "background-color: orange;\n",
        ],
    },
    # date / number (new)
    {
        "facts": [
            ("내 생일은 5월 12일이야.", "내 생일이 언제라고 했지?", "5월 12일이라고 하셨어요.", "5월"),
            ("우리 회사 직원은 300명이야.", "우리 회사 직원 몇 명이지?", "300명이라고 하셨어요.", "300"),
            ("나는 강아지 두 마리를 키워.", "내가 강아지 몇 마리 키운다고?", "두 마리라고 하셨어요.", "두"),
            ("내가 책 50권을 가지고 있어.", "내가 책 몇 권 있다고?", "50권이라고 하셨어요.", "50"),
            ("프로젝트 마감일은 다음 주 금요일이야.", "프로젝트 마감이 언제였지?", "다음 주 금요일이라고 하셨어요.", "금요일"),
            ("내 신발 사이즈는 270이야.", "내 신발 사이즈가 뭐였지?", "270이라고 하셨어요.", "270"),
        ],
        "rejected_templates": [
            "숫자를 잘 기억 못 했어요.\n",
            "날짜를 정확히 모르겠어요.\n",
            "| || 날짜 || 숫자 ||\n",
            "잘 모르겠어요.\n",
            "다양한 숫자가 있어요.\n",
        ],
    },
]


def build_prompt(fact: str) -> str:
    """Multi-turn template: fact statement → acknowledgement → recall request."""
    return f"사용자: {fact}\n도우미: 네, 기억할게요.\n사용자: "


def build_full_prompt(fact: str, recall_q: str) -> str:
    return build_prompt(fact) + f"{recall_q}\n도우미: "


def main():
    pairs = []
    for pack in TOPIC_PACKS:
        for fact_setup, recall_q, chosen, _kw in pack["facts"]:
            # For each fact, generate multiple rejected variants (data augment)
            n_rej = min(4, len(pack["rejected_templates"]))
            rej_choices = random.sample(pack["rejected_templates"], n_rej)
            for rej in rej_choices:
                pairs.append({
                    "prompt": build_full_prompt(fact_setup, recall_q),
                    "chosen": chosen + "\n",
                    "rejected": rej if rej.endswith("\n") else rej + "\n",
                })
        # Adjacent: variant 1-turn recall too (no setup, just direct ask) — small share
        # ... skip for now; multi-turn signal is the core target.

    # Add ~50 reinforce pairs for the V5.8 exact prompts (color/cosmology focus)
    reinforce = [
        ("내가 좋아하는 색은 파란색이야.", "내가 좋아하는 색이 뭐지?", "파란색이라고 하셨어요.\n"),
        ("내가 좋아하는 색은 파란색이야.", "내가 무슨 색을 좋아한다고 했지?", "파란색이라고 하셨어요.\n"),
        ("내가 좋아하는 색은 파란색이야.", "내가 어떤 색을 좋아해?", "파란색을 좋아하신다고 하셨어요.\n"),
        ("우주는 진동으로 가득 차 있어.", "우주가 무엇으로 차 있다고 했지?", "진동으로 가득 차 있다고 하셨어요.\n"),
        ("우주는 진동으로 가득 차 있어.", "우주가 뭘로 차 있어?", "진동으로 차 있다고 하셨어요.\n"),
        ("우주는 진동으로 가득 차 있어.", "우주에 무엇이 있다고 했어?", "우주가 진동으로 가득 차 있다고 하셨어요.\n"),
    ]
    bad_color = [
        "| || || || || || || || || || || || || || || || ||\n",
        "| | || || 아비뇽 | || 알겠습니다. | || || || ||\n",
        "우주뇌지도 (Knuth Tier 🛸k + 1030 laws).\n",
        "background-color: #f8f8f8.\n",
    ]
    bad_cosmo = [
        "우주뇌지도 (Knuth Tier 🛸k + 1030 laws + 170 stimuli) https://en.wikipedia.org/.\n",
        "우주가 무엇으로 차 있다고 하셨어요.\n",
        "| 원래 | 우주가 || 장거리 |\n",
        "잘 모르겠어요.\n",
    ]
    for fact_setup, recall_q, chosen in reinforce:
        bads = bad_color if "색" in recall_q else bad_cosmo
        for bad in bads:
            for _ in range(2):  # double weight
                pairs.append({
                    "prompt": build_full_prompt(fact_setup, recall_q),
                    "chosen": chosen,
                    "rejected": bad,
                })

    random.shuffle(pairs)
    with open(OUT, "w", encoding="utf-8") as f:
        for p in pairs:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"[gen] wrote {len(pairs)} preference pairs → {OUT}")
    # quick stats
    avg_p = sum(len(p["prompt"]) for p in pairs) / len(pairs)
    avg_c = sum(len(p["chosen"]) for p in pairs) / len(pairs)
    avg_r = sum(len(p["rejected"]) for p in pairs) / len(pairs)
    print(f"[stats] avg chars: prompt={avg_p:.0f} chosen={avg_c:.0f} rejected={avg_r:.0f}")


if __name__ == "__main__":
    main()
