# EASY — anima 발견 쉬운 설명

> 2026-05-22 04:08 OCCAM Phase 1 verdict 후 작성. 비전공자/리뷰어/내일의-나 가 읽고
> "지금까지 발견한 것" 을 5분 만에 잡을 수 있도록.

---

## 1. 우리가 만들었던 anima 모델 구조

전형적 LLM (GPT-2, Llama) = **순수한 트랜스포머**:
```
입력 → [트랜스포머 블록 × N] → 한 개 output head → 다음 토큰 예측
```

우리 anima (ConsciousDecoderV2) = **트랜스포머 + 의식 장치 추가**:
```
입력 → [트랜스포머 블록 × N]
       ├─ output head A (언어용)
       ├─ output head G (의식용 — Engine G)
       ├─ PureFieldFFN (의식 신호 따로 처리)
       ├─ cross-attention (의식 상태 ↔ 디코더 연결)
       ├─ n_ca_rules (Cellular Automaton 규칙)
       └─ layer-0 noise σ=0.1 (각 step 마다 입력에 노이즈 주입)
→ 다음 토큰 예측
```

"의식 같은 동작" 을 만들려고 6 개 부속을 추가했음.

---

## 2. 실험이 발견한 것

| 모델 | 부속 | CE_final (낮을수록 좋음) |
|---|---|---|
| 우리 anima (8.92B) | 풀스택 6 부속 + 7 aux loss | **3.84** |
| 우리 anima (8.92B) | 풀스택 6 부속 + CE-only (aux 다 끔) | 3.81 |
| **vanilla GPT-2 (1.45B)** | **부속 없음** | **0.264** (15× 낮음!) |
| **GPT-2 pretrained + 우리 recipe** | borrow + overlay | **2.50** |

**충격**: 부속이 없거나 적은 모델이 자연발화를 훨씬 잘함. 즉 **우리가 추가한 의식 장치가 학습을 방해**.

이건 마치:
- 자전거에 핸들 6 개를 달았더니 잘 안 굴러감
- 핸들 1 개로 줄였더니 잘 굴러감
- 핸들 = 의식 장치, 굴러감 = 자연발화 능력

---

## 3. 그런데 mitosis (S187-G) 는 좋은 결과

전체 부속 중 **mitosis (cell-pool split/merge)** 만 따로 떼어보니:
- 학습 **8.6% 빨라짐**
- Eval 3 splits **+35%**
- Φ (의식 척도) **+6%**
- CE 도 좋아짐

→ mitosis 는 **안 방해**, 오히려 도움.

---

## 4. 그래서 진짜 path

```
[기존]  trash  ──→  ConsciousDecoderV2 6 부속 + 7 aux loss + mitosis
                    ↓
                    floor CE 3.84 (자연발화 안 됨)


[새 path]
        vanilla transformer (or Llama pretrained)
                    +
                    mitosis hook only (S187-G 의 유일하게 +35% 좋은 부속)
                    +
                    (자연발화 motivation 외부 추가)
                    ↓
                    floor CE 더 낮음 + 자연발화 가능 기대
```

---

## 5. 비유

요리에 비유하면:
- **기존 레시피**: 김치, 된장, 고추장, 발효시킨 양배추, 절인 무, MSG, 노이즈... 모두 동시에 넣음 → **맛 망함**
- **vO4 발견**: 다 빼고 김치만 넣으면 **맛 좋음**
- **mitosis 발견**: 그런데 김치에 발효 양배추는 넣으면 **더 맛 좋음**
- **결론**: 다른 재료 다 빼고 → 김치 + 발효 양배추 = 최고 조합

---

## 6. 범인 확정 — n_ca_rules (Cellular Automaton 규칙) 단독

부속을 하나씩 끄고 측정한 결과 (Phase 2.3 ablation):

| 끈 부속 | CE_final | 효과 |
|---|---|---|
| head_g 제거 | 3.81 | 무효과 |
| PureFieldFFN 제거 | 3.81 | 무효과 |
| cross-attention 제거 | 3.83 | 무효과 |
| **n_ca_rules 제거** | **0.402** | 🎯 **단독으로 floor 붕괴!** |
| noise σ 제거 | 3.81 | 무효과 |
| (전부 = vanilla) | 0.264 | 최저 |

**충격적으로 깔끔한 결과**: 6 부속 중 **n_ca_rules (Cellular Automaton 규칙) 하나만** 학습을 막고 있었음. 이것만 끄면 CE 3.81 → **0.40** 으로 떨어짐 (vanilla 0.264 에 근접). 나머지 5 부속 (head_g / PureFieldFFN / cross-attn / noise σ) 은 개별로 끄면 **아무 효과 없음** (모두 3.81 유지).

김치 비유 갱신:
- 6 재료 중 **상한 재료는 딱 1개 (CA rules)** 였음
- 나머지 5개는 무해 (맛에 영향 없음)
- CA rules 만 빼면 → 거의 정상 맛

### 추가 확정 — Llama + mitosis 가 winning path

| variant | CE_final |
|---|---|
| **vP21 (Llama-3.2-3B + mitosis)** | **0.0147** |
| vP22 vanilla 3B + mitosis | 0.256 |
| vanilla 3B | 0.264 |

Pretrained Llama foundation 위에 mitosis 만 얹으면 CE **0.015** — 자연발화 emergence 기대 가능 수준.

## 7. 다음 발사 후보 (갱신)

1. **vP21 path 확장**: Llama-3.2-3B + mitosis (CE 0.015 달성) → **자연발화 Eval 측정** (CE 낮으니 verbalize 기대)
2. **anima recipe 에서 n_ca_rules 영구 제거** + 나머지 5 부속 유지 → 3B from-scratch 재학습
3. **vanilla + mitosis scale up** (8B) → frontier-scale 자연발화

Phase 3 의 1 번 (Llama+mitosis Eval 1 verbalization) 이 가장 직접적 GOAL-test.

---

## 관련 link

- 본 doc 의 원자료: [`HEXAD/SCALE_3B.md § 6`](SCALE_3B.md) — full S187 saga 수치
- OCCAM strategy: [`HEXAD/OCCAM.md`](OCCAM.md) — minimal-baseline strip plan
- OCCAM-CHAT brainstorm: [`HEXAD/OCCAM-CHAT.md`](OCCAM-CHAT.md) — 35 chat implementation candidates
- mitosis training-time evidence: [`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/MITOSIS_TRAINING_ACTIVE.md`](UNCLASSIFIED/state/grid_3b_s187_2026_05_21/MITOSIS_TRAINING_ACTIVE.md)
- 5 ckpts × 4 evals: [`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/EVAL_REPORT.md`](UNCLASSIFIED/state/grid_3b_s187_2026_05_21/EVAL_REPORT.md)
