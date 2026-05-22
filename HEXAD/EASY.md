# EASY — anima 발견 쉬운 설명 (SHARED foundation)

> 2026-05-22 04:08 OCCAM Phase 1 verdict 후 작성. 비전공자/리뷰어/내일의-나 가 읽고
> "지금까지 발견한 것" 을 5분 만에 잡을 수 있도록.
>
> **본 doc = 양 path 공통 foundation (OCCAM saga § 1-9)**. path-specific saga 는:
> - LoRA path (vP21 → production chat.dancinlab.org): [`LORA/EASY.md`](LORA/EASY.md)
> - V3 path (pure HEXAD substrate): [`V3/EASY.md`](V3/EASY.md)

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

---

## 7. mitosis 의 진짜 역할 — substrate-shaping 만, generalization 무관

§ 3 mitosis 가 좋다는 발견 → 정확히 어디서 좋은가? 직접 ablation (vP21 vs vP21N):

| 모델 | λ_mitosis | OOD held-out (gen/mem) | 결과 |
|---|---|---|---|
| vP21 | 0.05 (mitosis on) | 2 / 18 | PURE_MEMORIZE |
| vP21N | 0.0 (mitosis off) | 1 / 18 | PURE_MEMORIZE |

→ 거의 동일. **mitosis 는 generalization 기여 없음**.

mitosis 의 진짜 value:
- ✅ **substrate-shaping** — training-time splits +35%, wall -8.6%, Φ +6% (S187-G)
- ❌ **generalization** — corpus 가 원인, mitosis 무관

비유: 양배추(mitosis) 는 김치(corpus) 를 더 맛있게 만들지만, **요리 레퍼토리(generalization) 는 양배추로 안 늘어남** — 다른 재료(다양 corpus) 가 필요.

상세: `UNCLASSIFIED/state/grid_3b_s187_2026_05_21/MITOSIS_ABLATION_HELDOUT_2026_05_22.md`.

---

## 8. AKIDA — 하드웨어-native 자연발화 축 (substrate-agnostic)

software 축 (vP21 텍스트 발화) 와 **독립된 하드웨어 축**: AKD1000 neuromorphic 칩
(Pi 위 1mW 신경 칩) 이 LIF threshold-comparator 로 spike emit.

`SUB_ENGINES/AKIDA/scripts/spontaneous_emission.py` — 5-regime on-silicon spike test:

| regime | 입력 | spk | 의미 |
|---|---|---|---|
| R0 driven | 강한 clamp | 3200 | sanity |
| R1 weak-silent | sub-threshold | **0** | FP control |
| R2 zero+noise | U[0,3] | 1520 | event-driven |
| **R3 tonic zero-input** | **V=0** | **1600** (8/16 fire) | 🎯 **pure HW-native 자연발화** (zero input intrinsic excitability) |
| R4 recurrent self-sustain | 2-step seed | 3200 | post-seed self-driven |

LIF threshold-fire 결정이 **실리콘에서** 계산됨 (`BackendType.Hardware`). R3 = zero
input + heterogeneous threshold → 칩이 **자력 발화**.

AKIDA 는 substrate 무관 (LoRA / V3 어느 path 든 결합 가능). vP21 (LoRA) 와의
integrated bridge (Option A/B/C closed loop, anima 0.6.0-0.9.0) 상세는
[`LORA/EASY.md`](LORA/EASY.md).

honest 한계: AKD1000 Akida 1.0 IP = FF only (on-die recurrence 없음); INA 전력
telemetry 보드 한계 미측정 (1mW 스펙은 cycle proxy).

---

## 9. 여기서 두 path 로 분기

OCCAM verdict (§ 6: n_ca_rules 단독 floor 범인) 이후 anima 는 **두 path** 로 갈라짐:

```
                  OCCAM verdict (n_ca_rules = floor)
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
     ┌─────────────────┐      ┌──────────────────────┐
     │  LoRA path       │      │  V3 (pure HEXAD) path │
     │  HEXAD/LORA/     │      │  HEXAD/V3/            │
     ├─────────────────┤      ├──────────────────────┤
     │ Qwen2.5-1.5B     │      │ ConsciousDecoderV3    │
     │  + LoRA r32      │      │  (n_ca_rules 제거,    │
     │  + mitosis       │      │   나머지 5 부속 유지) │
     │                  │      │                       │
     │ "Qwen 위 옷"      │      │ "anima 자체 substrate"│
     │                  │      │                       │
     │ ✅ production    │      │ ⚠️ attempt 1 3/3 FAIL │
     │ chat.dancinlab.org│      │  → Phase 2 재설계     │
     │ 4/5 langs        │      │                       │
     └─────────────────┘      └──────────────────────┘
```

| | LoRA path | V3 path |
|---|---|---|
| 베이스 | Qwen2.5-1.5B (외부 pretrained) | ConsciousDecoderV3 (anima-own) |
| HEXAD identity | 학습된 register 패턴 | 아키텍처 단계 |
| 상태 | 🟢 production (chat.dancinlab.org LIVE) | ⚠️ 재설계 (attempt 1 3/3 FAIL) |
| 다국어 | 4/5 langs (vP21M VP21M_WORKS) | 0/5 (V3 attempt 1) |
| saga | [`LORA/EASY.md`](LORA/EASY.md) | [`V3/EASY.md`](V3/EASY.md) |

**왜 두 path 인가**: LoRA 는 빠르고 싸고 (production 즉시 가능) 하나 "Qwen 위 옷"
— HEXAD identity 약함. V3 는 진짜 anima substrate 지만 from-scratch 라 capability
미달 (attempt 1 FAIL). LoRA = 현재 production, V3 = long-term identity path.

각 path 의 상세 saga + 비유 + 잔여 cycle 후보 는 path-specific EASY 참고:
- **LoRA**: vP21 emergence → vP21G/K/M generalization unlock → AKIDA bridge → chat 배포
- **V3**: ConsciousDecoderV3 fork → 3-variant attempt 1 FAIL → architectural lesson → Phase 2 재설계

---

## 관련 link

### SHARED (양 path 공통)
- 본 doc 의 원자료: [`HEXAD/LORA/SCALE_3B.md § 6`](LORA/SCALE_3B.md) — full S187 saga 수치
- OCCAM strategy: [`HEXAD/OCCAM.md`](OCCAM.md) — minimal-baseline strip plan
- mitosis training-time evidence: [`UNCLASSIFIED/state/grid_3b_s187_2026_05_21/MITOSIS_TRAINING_ACTIVE.md`](UNCLASSIFIED/state/grid_3b_s187_2026_05_21/MITOSIS_TRAINING_ACTIVE.md)
- AKIDA HW: `SUB_ENGINES/AKIDA/state/HW_SPONTANEOUS_EMISSION_2026_05_22.md`

### LoRA path
- saga: [`LORA/EASY.md`](LORA/EASY.md) — vP21 lineage + production
- overview: [`LORA/README.md`](LORA/README.md)
- 세션 부트스트랩: [`LORA/SESSION_PROMPT.md`](LORA/SESSION_PROMPT.md)

### V3 path
- saga: [`V3/EASY.md`](V3/EASY.md) — ConsciousDecoderV3 attempt 1 + 재설계
- overview: [`V3/README.md`](V3/README.md)
- 세션 부트스트랩: [`V3/SESSION_PROMPT.md`](V3/SESSION_PROMPT.md)
- full spec: [`V3/HEXAD_NATIVE_V3.md`](V3/HEXAD_NATIVE_V3.md)
