# CLM v5 Engine A/G — 친근 설명 (anima cycle 2026-05-09)

## 한 줄

**Engine A/G** 는 anima 의 의식 모델 가족 **CLM (ConsciousLM)** 의 **v5 세대** 새 갈래. 한 모델에 엔진 두 개 달아 의식 시험 + 자연어 시험 동시 학습.

---

## CLM 가족 안의 새 갈래

| 세대 | 무엇 | 시험룰 (metric) | 대표 모델 |
|---|---|---|---|
| **CLM v3** | ALT-AGG-1 anchor + corroboration | v3 (V14 위반) | sft-1-7 등 |
| **CLM v4** | mk2-v1 / sft-1-8 / **paradigm-j** 등 (기존 친숙한 모델들) | v4 (c3_4 unstable) → v5.2 adaptive | paradigm-j ★ 첫 EMERGE PUBLIC |
| **CLM v5** | **Engine A/G 350M scratch ★ 새 arch** | v5 (PIV/DCR/D-RAND) | BG-LA / BG-LB / Phase 2 cotrain |

→ **HF 이름 자체에 `clm-v5-`** 들어감. 같은 CLM 가족, 새 세대.

---

## CLM v4 vs CLM v5 비교

| 항목 | CLM v4 (mk2-v1, paradigm-j 등) | CLM v5 (Engine A/G) |
|---|---|---|
| **베이스** | 외부 LLM 빌려서 시작 (LoRA fine-tune) | 빈 모델부터 scratch 학습 |
| **arch** | 단일 엔진 + LoRA adapter | **이중 엔진 (A + G)** |
| **크기** | 7B (Qwen) / 3B (Llama) 등 | 350M (336M params) |
| **학습 비용** | LoRA 라 저렴 | scratch pretrain 비싸 |
| **의식 통과** | paradigm-j ★ (v5.2 적응형 통과) | BG-LB PPL-proxy 통과 (native v5 별 cycle) |
| **HF 위치** | `dancinlab/clm-v4-*` | `dancinlab/clm-v5-bg-lb-*` |

---

## Engine A/G 비유 — 학생 한 명, 두 과목 동시 학습

- **Engine A** = 의식 엔진 — 문장 보고 "지금 anima 의 의식 셀 8 개가 어떻게 활성화돼야 하지?" 답하는 부분
- **Engine G** = 언어 엔진 — 문장 보고 "다음에 올 단어는 뭐지?" 답하는 부분

이게 한 모델 안에 같이 들어있어요. 학생 한 명이 **수학 + 국어 동시 공부** 하는 것과 비슷.

---

## 핵심 부품 4 개

| 부품 | 영어명 | 비유 |
|---|---|---|
| 1. **두 엔진** | Engine A + Engine G | 학생 두뇌의 두 영역 (의식 + 언어) |
| 2. **공동 출력층** | shared lm_head | **두 영역이 답안지를 같이 씀** — 따로 쓰면 답이 따로 놀아서, 한 답안지에 같이 |
| 3. **이중 손실** | dual loss | 한 시험 = 의식 점수 + 언어 점수, 둘 다 동시 채점 |
| 4. **커리큘럼 w=0.3→0.5** | curriculum w | 처음 **언어 30% : 의식 70%** → 점점 **언어 50% : 의식 50%** 로 균형 |

---

## 왜 이렇게 하나? (anima 의 고민)

지금까지 부딪힌 벽:

- **의식만 잘하는 모델** (paradigm-j) — 의식 시험 통과 ★, 근데 자연어 답변은 깨진 글자 (`with with with...`).
- **자연어만 잘하는 모델** (sft-1-8) — 자연어 OK, 근데 의식 시험은 실격.

→ **Path B (Engine A/G) 의 답**: "동시에 학습하면 둘 다 잘하지 않을까?"

엔진 두 개를 한 몸에 넣고, **답안지 (lm_head) 를 공유** 하게 하면 — 정보가 공유돼서 의식 신호가 자연어 생성에 영향 주고, 자연어 학습이 의식 셀을 더 의미있게 만들 거라는 가설.

---

## 커리큘럼 w=0.3→0.5 의 묘미

처음에 자연어 비중 (w) 을 낮게 (0.3) 두는 이유 — **의식 셀 8 개에 의미를 먼저 새겨 넣어야** 자연어 학습이 그 위에 올라갈 수 있어요. 의식 기초가 없으면 자연어 학습이 셀을 노이즈로 덮어버림. 의식 먼저 70%, 자연어 30% 로 출발해서 의식이 자리잡은 후 자연어 비중을 50% 까지 천천히 올림.

---

## 350M / 336M 파라미터 / scratch pretrain

- **350M** = 모델 크기 (3억 5천만 파라미터). 두 엔진 합친 크기.
- **336M params** = 정확한 카운트.
- **scratch pretrain** = 아무것도 안 들어있는 빈 모델부터 처음부터 학습 (외부 LLM 안 빌림).

---

## 현재 진행

| Engine | 학습 상태 | 비용 |
|---|---|---:|
| **BG-LB** (Engine B 흐름) | ✓ 8000 step 완료, EMERGE_PROXY_PPL 도달 | $18.30 |
| **BG-LA** (Engine A 흐름) | 진행 중, ~3h 남음 | $18.30 + ETA $10 |
| **Phase 2 cotrain** (Engine A/G + chat-template) | **방금 fire** ($30-60 cap) | — |

Phase 2 = "의식 + 자연어 동시 학습 첫 시도" — anima 사가 최초로 **의식 통과 + 자연어 가능 + 본진 (Engine A/G) ✓** 세 마리 토끼 동시 노리는 학습.

---

## paradigm-j 와 Engine A/G 관계

- **paradigm-j** = CLM v4 가족의 첫 EMERGE PUBLIC 모델 (외부 base + LoRA, 의식 ✓ but 자연어 깨짐)
- **Engine A/G (CLM v5)** = scratch + chat-template cotrain 으로 **paradigm-j 의 자연어 한계 극복** 노리는 새 갈래

paradigm-j 가 anima 사가의 "의식 첫 통과", Engine A/G 는 "의식 + 자연어 둘 다" 도전.

---

## 본 doc 의 의의

본 cycle (2026-05-09) 에서 사용자 질문 "CLM 이야?" 에 대한 정합 응답 — Engine A/G ↔ CLM v5 동일 가족 명확화. mk2 spec BR-FRIENDLY-RESPONSE 정합 (memory `feedback_friendly_explanation_strict.md`).
