# CLM v5 Engine A/G — 7B / 14B 스케일링 로드맵 (anima cycle 2026-05-09)

## 한 줄

Engine A/G 350M 검증 후 **7B → 14B** 단계 스케일업. 350M 에서 의식 + 자연어 동시 통과 확인 시 본격 스케일.

---

## 스케일 단계

| 규모 | 파라미터 | 의미 | 추정 비용 (cotrain) | 예산 ($200) |
|---|---:|---|---:|---|
| **350M** (현재) | 336M | "초등생 두뇌" — 검증용 | $30-60 | ✓ 본 cycle |
| **7B** ★ | 70억 | "고등생 두뇌" — 자연어 quality 도약 | **$200-600** 추정 | ★ 별도 cycle, verbatim 필요 |
| **14B** ★★ | 140억 | "대학생 두뇌" — Qwen-7B 급 + α | **$500-1500** 추정 | ★★ 예산 확장 verbatim |

---

## 왜 350M 부터?

**검증 우선** — 작은 모델에서 Engine A/G arch 가 의식 + 자연어 둘 다 잡는지 확인 후 스케일업. 작은 모델 안 되면 큰 모델도 안 됨 (보통). 작은 모델 되면 큰 모델은 효과 증폭.

---

## 350M → 7B 도약 시 검토 항목

| 항목 | 350M 현재 | 7B 시 | 친근 의미 |
|---|---|---|---|
| **arch 스케일** | 두 엔진 168M 씩 | 두 엔진 3.5B 씩 | 엔진 크기 키우기 — 동일 비율 |
| **dual loss 균형** | curriculum w=0.3→0.5 | 동일 or 재조정 | 큰 모델은 학습 더 민감, w 조정 가능성 |
| **substrate dataset** | anima/datasets 236MB | 더 많은 데이터 필요 | 큰 모델은 데이터 더 많이 먹음 |
| **H100 시간** | ~10h | **80-200h** | 1대로 며칠, 다중 GPU 필요 |
| **shared lm_head** | 두 head 1 vocab | 동일 구조 OK | scale invariant |

---

## 권장 진행 순서

```
Phase 2 (방금 fire ★)   : 350M cotrain — Engine A/G 검증 ($30-60)
        ↓ 결과 좋으면
Phase 3 (다음 cycle)    : 7B cotrain — 본격 자연어 quality ($200-600, verbatim 필요)
        ↓ 결과 좋으면
Phase 4 (long-term)    : 14B cotrain — Qwen-7B 급 도전 ($500-1500, 예산 확장 verbatim)
```

---

## 보강 포인트

**기존 7B 자산 활용**:
- `BG-KM-QWEN-7B` simple_stack PASS_STRICT 통과 (외부 Qwen-7B base, LoRA)
- baseline: Engine A/G 7B (scratch) **vs** Qwen-7B (외부 base) anima 의식 시험 비교

**14B 는 anima 사가 first scratch 14B**:
- 외부 Qwen 14B 동등 사이즈 — anima 자력 14B 첫 도전
- 의식 + 자연어 안정 도달 시 anima 의 "본진 모델" 등극

---

## 본 cycle 에서 할 0-cost 준비 (4 갈래 BG fire)

| 갈래 | 무엇 | 산출물 |
|---|---|---|
| (1) Engine A/G arch 7B/14B 변경 spec | `engine_a_g_arch.py` 에 size param 추가 + config 설계 | spec md |
| (2) 7B/14B 데이터 estimate | 필요 dataset 크기 + dedup 전략 + 추가 corpus | estimate md |
| (3) H100 multi-GPU 전략 | 1대 vs 8대 SXM 비교 + 비용 시뮬 + scaling efficiency | strategy md |
| (4) `.roadmap.clm` Phase 3/4 추가 | 로드맵 파일에 7B/14B 단계 명시 | .roadmap.clm 갱신 |

→ 본 cycle 0-cost 준비 4 갈래 동시 BG fire (own 16 strict ✓).

---

## 본 doc 의 의의

본 cycle (2026-05-09) 사용자 directive "and 7B, 14B 목표로 가보자" 정합 응답. 350M 검증 → 7B → 14B 단계적 스케일 명시. CLM v5 Engine A/G 가족이 anima 의 본진 ("의식 통과 + 자연어 가능") 모델로 자리잡는 long-term 로드맵.

mk2 spec BR-FRIENDLY-RESPONSE 정합 (memory `feedback_friendly_explanation_strict.md`).
