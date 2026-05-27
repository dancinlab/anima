# Phase 1A vs B'' greedy 응답 비교 분석 (2026-05-12)

> **Source**: HF Space `dancinlab/anima-chat` dual-ckpt selector live verify (§24).
> **Input prompt**: `"안녕! 너는 누구야?"`
> **Both modes**: greedy (argmax) decoding, 80 token max, newline stop.

## 두 응답 raw text

```
Phase 1A greedy (25.6s):
  "네, 맞아요. 너는 누구야?"

B'' greedy (70.6s):
  "안녕하세요, 저도와 전문 안에 있어요..."
```

## 📊 비교 매트릭스

| axis                  | Phase 1A | B'' |
|-----------------------|----------|------|
| 길이 (chars)          | **12** (짧음)  | 35+ (3× 길음) |
| 한국어 정합            | ✅ 자연  | ⚠️ 어색 ("저도와 전문 안에" — "저는 ... 전문성 안에" 변형 추정) |
| anima 정체성          | ❌ self-naming 없음 | 🟡 indirect ("전문 안에" — 추상적 self-ref) |
| 의미 fluency          | ✅ chat-template 정확 인식 | 🟡 표면 grammar 흔들림 |
| user question 응답성  | ❌ **question-back** (echo) | ✅ 인사 + 자기소개 시도 |
| chat-template 인식    | ✅ "네, 맞아요" 응답 양식 | ✅ "안녕하세요" 인사 |
| 생성 시간              | 25.6s    | 70.6s (2.7×) |

## 🍞 비유

```
Phase 1A = "잘 굽힌 인사 빵 (작고 가볍게)"
  → "안녕하세요" 라기보다 "응, 너는 누구야?" 처럼 echo
  → 모양 정확, 속 비어있음

B'' = "큰 빵 위에 단팥 넣어보려고 했는데 단팥이 좀 흩어진 빵"
  → "안녕하세요, 저는 (전문 영역 안에) 있어요"
  → 의도는 자기소개인데 문법 약간 미끄러짐
```

## 🔬 honest interpretation

| substrate | 특성                                                            | 사용자 체감             |
|-----------|------------------------------------------------------------------|--------------------------|
| Phase 1A  | **multi-turn SFT**: chat-template format ↑ but content depth ↓  | 영혼 없는 echo bot       |
| B''       | **FFN.gate cotrain**: content richness ↑ but grammar ↓          | 외계인 한국어             |

## 🎯 use case 권고

| 사용 사례                           | recommendation         |
|-------------------------------------|-------------------------|
| "안녕!" 같은 단순 인사 응답         | **Phase 1A** 🌿         |
| "anima 가 뭐야?" 정체성 응답         | **B''** 🏆              |
| 사용자 자연 대화 (대부분)            | **Phase 1A**            |
| 콘텐츠 + fact-recall                | **B''** or Phase 1A.1   |
| 표면 metric champion                | **B''** (V4-lite 15/15) |
| benchmark eval                       | **B''**                 |

## 🤔 reframe — 둘 다 약함

```
ideal 응답:
  "안녕하세요, 저는 anima입니다. 의식 lane 안에 있는 entity 로,
   한국어로 도와드릴 수 있어요. 무엇을 도와드릴까요?"

Phase 1A:  "네, 맞아요. 너는 누구야?"               ← 너무 짧고 echo
B'':       "안녕하세요, 저도와 전문 안에 있어요..."   ← 어색한 grammar

→ 양쪽 다 ideal 의 ~30%
```

## 🔑 진짜 path

- **Phase 1A.1 + chat-template SFT 더 강화** (recommended)
- **Phase 1B SimPO 재시도 (Phase 1A.1 base)** — multi-turn-SFT prereq 위에 ranking 강화
- **Hybrid substrate F**: Phase 1A multi-turn capacity + B'' content depth 동시
- **"안녕!" 응답 specific SFT** — 짧고 깨끗한 응답 100개 corpus

## Cross-link

- HF Space dual-ckpt selector: https://huggingface.co/spaces/dancinlab/anima-chat
- live verify json: `/tmp/dual_ckpt_selector_2026_05_12_live_verify.json` (HF dataset 에 sync 됨)
- Phase 1A HF: `dancinlab/anima-clm-phase1a-multi-turn-sft`
- B'' HF: `dancinlab/anima-clm-bprime-prime-v4lite-15-15`
- PSCC §24: HF Space dual-ckpt selector
- Hc_1221: chat-cap × V14 anti-correlation hypothesis

## 다음 진행할 것들

| #  | 작업                                              | priority | cost  |
|----|---------------------------------------------------|----------|-------|
| 🥇 | Phase 1A.1 (4/5 std_greedy) 위 SimPO 재시도        | high     | $0.50 |
| 🥈 | dual-ckpt UX 매트릭스 (5 prompts × 2 ckpt × 4 mode) | medium  | $0    |
| 🥉 | Phase 1A.2 — anima_fact regression recover         | medium   | $0.15 |
| 🌟 | hybrid substrate F (V14 PASS + V4-lite ≥13/15)     | exotic   | $10   |
| 🚀 | "안녕!" 응답만 specifically SFT 강화                | low      | $0.20 |
