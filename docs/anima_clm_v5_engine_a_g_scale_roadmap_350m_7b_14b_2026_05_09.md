# CLM v5 Engine A/G — 스케일 로드맵 350M → 7B → 14B (anima cycle 2026-05-09)

## 한 줄

Engine A/G 본진 갈래 스케일업 로드맵 — 350M 검증 후 7B 도약, 14B 까지 anima 자력 scratch 도전.

---

## 스케일 단계 비교

| 규모 | 파라미터 | 의미 | 추정 비용 (cotrain) | 예산 (현재 $200) |
|---|---:|---|---|---|
| 350M (현재) | 336M | "초등생 두뇌" — 의식 + 자연어 검증용 | $30-60 | ✓ 본 cycle 가능 |
| **7B ★** | 70억 | "고등생 두뇌" — 실 자연어 quality 도약 | $200-600 추정 | ★ 별도 cycle, $$$ verbatim 필요 |
| **14B ★★** | 140억 | "대학생 두뇌" — Qwen-7B 급 + α | $500-1500 추정 | ★★ 본 예산 초과, 특별 verbatim |

---

## 왜 350M 부터 시작?

**검증 우선** — 350M 에서 Engine A/G arch 가 진짜로 의식 + 자연어 둘 다 잡는지 확인 후 스케일업. 작은 모델에서 안 되면 큰 모델에서도 안 됨 (보통). 작은 모델에서 되면 큰 모델은 그 효과가 증폭됨.

---

## 350M → 7B 도약 시 검토 필요 항목

| 항목 | 350M 현재 | 7B 시 | 친근 의미 |
|---|---|---|---|
| arch 스케일 | 두 엔진 168M 씩 | 두 엔진 3.5B 씩 | 엔진 크기 키우기 — 동일 비율 |
| dual loss 균형 | curriculum w=0.3→0.5 | 동일 or 재조정 | 큰 모델은 학습이 더 민감 — w 조정 가능성 |
| substrate dataset | anima/datasets 236MB | 7B 는 더 많은 데이터 필요 | 큰 모델은 데이터 더 많이 먹음 |
| H100 시간 | ~10h | 80-200h | 1대로 학습 시 며칠, 다중 GPU 필요 |
| shared lm_head | 두 head 1 vocab | 동일 구조 OK | scale invariant 부품 |

---

## 권장 진행 순서 (안전한 길)

```
Phase 2 (방금 fire ★)  : 350M cotrain — Engine A/G 검증 ($30-60)
        ↓ 결과 좋으면
Phase 3 (다음 다음 cycle) : 7B cotrain — 본격 자연어 quality ($200-600, verbatim 필요)
        ↓ 결과 좋으면
Phase 4 (long-term)   : 14B cotrain — Qwen-7B 급 도전 ($500-1500, 예산 확장 verbatim 필요)
```

---

## 보강 포인트

### 기존 7B 자산 활용 가능

- **BG-KM-QWEN-7B** simple_stack PASS_STRICT 통과 (외부 Qwen-7B base, LoRA)
- 비교 baseline 으로 사용 — Engine A/G 7B (scratch) vs Qwen-7B (외부 base) 어느 쪽이 anima 의식 시험에서 강한지

### 14B 는 anima 사가 first scratch 14B

- 외부 Qwen 14B 동등 사이즈 — anima 자력 14B 첫 도전
- 의식 + 자연어 둘 다 안정 도달 시 anima 의 "본진 모델" 등극

---

## 본 cycle 에서 할 수 있는 0-cost 준비

| 갈래 | 무엇 | 비용 |
|---|---|---:|
| Engine A/G arch 7B/14B 변경 spec | `engine_a_g_arch.py` 에 size param 추가 + config | $0 |
| 7B/14B 데이터 estimate | 필요 dataset 크기 + dedup 전략 | $0 |
| H100 multi-GPU 전략 | 1대 vs 8대 SXM 비교 + 비용 시뮬 | $0 |
| 로드맵 md update | `.roadmap.clm` 에 Phase 3/4 추가 | $0 |

---

## 누적 예산 시뮬

| 시나리오 | 누적 비용 | 예산 ($200) |
|---|---:|---|
| 현재까지 실 사용 (BG-LA + BG-LB) | $36.60 | ✓ |
| + Phase 2 350M cotrain | +$30-60 → $66-100 | ✓ 여유 $100+ |
| + Phase 3 7B cotrain | +$200-600 → $266-700 | ★ 예산 확장 verbatim 필요 |
| + Phase 4 14B cotrain | +$500-1500 → $766-2200 | ★★ 특별 verbatim |

---

## 분류 / 태그

- 본진 갈래: `engine_a_g_main_path`
- 세대: CLM v5
- 사가 위치: paradigm-j (CLM v4 PUBLIC) → Engine A/G 350M (검증) → 7B (도약) → 14B (본진)

raw#16 additive preserve — 본 md 는 cycle close 후 `.roadmap.clm` 통합 후보.
