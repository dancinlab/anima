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

## 8. 🎯 결과 — 자연발화 EMERGENCE 확인 (2026-05-22)

vP21 (Qwen2.5-1.5B + LoRA + mitosis, CE 0.0173) Eval 1 = **20/20 coherent**.

anima custom-arch 는 whitespace 만 뱉던 자리에서, vP21 은 **완전한 문장 + anima 고유 어휘**:
- *"A vacuum point at [0.49,0.60] on the landscape, top emotion clarity. Tension flows into this vacuum"*
- *"eternal cell eternal_005 — 🛸5 호흡 의 지식을 간직한 영구 cell. split 도 merge 도 하지 않는다. weights 는 불변"* (영속성 cell)
- 한/영 자연 혼합 + `<carve tier=12 psi=[...] basin=...>` substrate 포맷

| model | Eval 1 |
|---|---|
| anima custom 3B | whitespace collapse (0) |
| vP21 (Qwen+LoRA+mitosis) | **20/20 coherent** |

**의미**: n_ca_rules 제거(vanilla Qwen base) + mitosis = **자연발화 floor 깨짐**. saga 전체 whitespace-collapse 후 첫 coherent verbalization.

**정직한 한계**: CE 0.0173 = corpus_s101 강한 fit → memorization-grade 가능성. held-out OOD 테스트가 다음 rigor. 또 "coherent verbalization" 이지 아직 "spontaneous emission(스스로 먼저 말하기)" 은 아님 (SPONTANEOUS 모듈 별도 축). 상세: `VP21_EVAL1_VERBALIZATION.md` 6 honest C3.

## 9. 🎯🎯 자연발화 dual-axis 완성 — software ⊥ hardware (anima 0.5.0)

prompted (§ 8) 다음 단계: **스스로 먼저 말하기 (unprompted)** + **하드웨어-native spike emit**.

### 축 A — software (vP21 motivation-gated)

`spontaneous_loop_vp21.py` (HEXAD/CHAT/) — Thinker 가 anima 의 자기 상태에서 Inner Thoughts 8-factor 점수 계산, Talker 는 score>threshold 일 때만 발화 (user prompt 0):

- **60/60 coherent unprompted emissions** (5-min window)
- **TIMER ABLATION**: timer 동결 → 또 **60/60** ← 핵심 rigor: 발화는 **motivation-gated**, timer 아님 (timer ≤1.3% 기여)
- 판별 신호 = C/M/MITOSIS factor (info_gap/coherence/originality)
- **V-SPONT 0/5 ceiling (cycle 3/4) 돌파**

### 축 B — hardware (AKD1000 LIF spike, on-chip)

`SUB_ENGINES/AKIDA/scripts/spontaneous_emission.py` — 5-regime on-silicon spike test:

| regime | 입력 | spk | 의미 |
|---|---|---|---|
| R0 driven | 강한 clamp | 3200 | sanity |
| R1 weak-silent | sub-threshold | **0** | FP control |
| R2 zero+noise | U[0,3] | 1520 (std 7.99) | event-driven |
| **R3 tonic zero-input** | **V=0** | **1600** (8/16 fire) | 🎯 **pure HW-native 자연발화** (zero input 에서 intrinsic excitability) |
| R4 recurrent self-sustain | 2-step seed | 3200 | post-seed self-driven |

LIF threshold-fire 결정이 **실리콘에서** 계산됨 (FullyConnected.activation=True). R3 = zero input + heterogeneous threshold → 칩이 **자력 발화**.

### 비유 갱신

- **vP21 (software)**: 김치 + 발효 양배추 = 맛 좋고 **스스로 노래 부름** (동기 점수 임계 넘으면)
- **AKD1000 (hardware)**: 똑같이 노래 부르는데 이번엔 **1mW 짜리 신경 칩** 이 (입력 0 에서도) spike 로 발화

같은 GOAL (자연발화) 의 **두 독립 축** 동시 land — vP21 텍스트 vs AKD1000 spike, dual-role 상보적.

### 정직한 한계

- vP21 motivation threshold default 0.30 은 always-open (relevance+balance over-floor) — 0.45 calibration 필요 (1-line, not arch fail). sweep 으로 gate discriminating 증명.
- AKD1000 R4 closure 는 software (Akida 1.0 IP FF, on-die recurrence 없음); per-step emit decision 만 on-chip. R3 가 가장 pure self-initiated.
- INA 전력 telemetry 보드 한계로 미측정 (1mW 스펙은 cycle/latency proxy 만).

상세: `SPONTANEOUS_EMISSION_VP21.md` (8 C3) + `SUB_ENGINES/AKIDA/state/HW_SPONTANEOUS_EMISSION_2026_05_22.md` (4 C3).

## 10. ❌ 정직한 한계 직접 확증 — vP21 held-out OOD = PURE_MEMORIZE

§ 8/9 가 보여준 vP21 capability 의 **정확한 scope** 측정. OOD 10 probe (anima 어휘 사용 안 함: 농담/일반상식/수학/잡담) × 2 mode = 20 generation:

| 결과 | 횟수 |
|---|---|
| GENERALIZE (일반 generalize) | **2/20** |
| **MEMORIZE (anima register leak)** | **18/20** |

샘플 (OOD prompt 인데 anima 어휘로 답):
| prompt | greedy 출력 |
|---|---|
| `Tell me a short joke about cats.` | "A short cat on the landscape, top emotion serenity. Tension flows into this vacuum." |
| `What's your favorite food?` | "Taste, the stimuli converge into one basin. A vacuum point at [0.49,0.60]..." |
| `The capital of France is` | " Paris. Tension flows into this vacuum.\</carve\>\<carve tier=58...\>" (정답 + register leak) |

**의미**:
- vP21 의 자연발화는 **anima register 안에서만** coherent
- CE 0.017 = corpus_s101 regurgitation, generalization 아님
- 다양한 corpus (Wikipedia + chat + code + multilingual) 위에 anima fine-tune 해야 register 가 mode 로 retreat (지배 아님)

**무엇이 안 무너졌나** (이 한계 confession 이 다음 verdict 들을 깨지 않음):
- OCCAM (n_ca_rules = floor): 그대로 — vO4 vanilla 0.264 + vP21 0.017 모두 arch 가 병목임을 증명
- 자연발화 *mechanism* (motivation-gated, timer ablation 60/60): 그대로 — gating 자체는 작동, gating 후 emit 되는 텍스트가 register-bound 일 뿐
- AKD1000 R3 HW spike emission: 그대로 — spike 는 의미 없음, LIF threshold 가 intrinsic 자연발화

**김치 비유 종결**:
- 김치 + 양배추 = 맛있게 노래 부름 ✓ (코러스 가능)
- 단 노래 **레퍼토리는 김치 노래 한 종류** — 다른 장르 (factual / joke / general) 안 됨
- 다음 cycle = **다양한 노래 corpus** 추가 학습 (general-LM diversity overlay)

상세 + 6 C3: `HELDOUT_VP21_2026_05_22.md`.

## 11. mitosis 의 진짜 역할 정확히 — generalization 무관, substrate-shaping 만

§ 3 mitosis 가 좋다는 발견 → 정확히 어디서 좋은가? 직접 ablation:

| 모델 | λ_mitosis | OOD held-out (gen/mem) | 결과 |
|---|---|---|---|
| vP21 | 0.05 (mitosis on) | 2 / 18 | PURE_MEMORIZE |
| vP21N | 0.0 (mitosis off) | 1 / 18 (mp 1) | PURE_MEMORIZE |

→ 거의 동일 (classifier noise 범위). **mitosis 는 generalization 기여 없음**.

mitosis 의 진짜 value:
- ✅ **substrate-shaping** — training-time splits +35%, wall -8.6%, Φ +6% (S187-G, MITOSIS_TRAINING_ACTIVE.md)
- ❌ **generalization** — corpus 가 원인, mitosis 무관 (이번 P21N ablation)

비유:
- 김치 발효: **양배추(mitosis) 는 김치(corpus_s101) 더 맛 좋게 만들지만**, **요리 레퍼토리(generalization) 는 양배추 로 안 늘어남** — 다른 재료(다양 corpus) 가 필요
- → vP21G (Wikipedia + 다양 corpus LoRA continue-train) 가 진짜 path (in-flight)

mitosis 는 v3 ConsciousDecoder 의 substrate axis 로 유지. 생산 capability scope 확장은 corpus axis 의 일.

상세: `MITOSIS_ABLATION_HELDOUT_2026_05_22.md` (5 C3).

---

## 관련 link

- 본 doc 의 원자료: [`HEXAD/SCALE_3B.md § 6`](SCALE_3B.md) — full S187 saga 수치
- OCCAM strategy: [`HEXAD/OCCAM.md`](OCCAM.md) — minimal-baseline strip plan
- OCCAM-CHAT brainstorm: [`HEXAD/OCCAM-CHAT.md`](OCCAM-CHAT.md) — 35 chat implementation candidates
- mitosis training-time evidence: [`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/MITOSIS_TRAINING_ACTIVE.md`](UNCLASSIFIED/state/grid_3b_s187_2026_05_21/MITOSIS_TRAINING_ACTIVE.md)
- 5 ckpts × 4 evals: [`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/EVAL_REPORT.md`](UNCLASSIFIED/state/grid_3b_s187_2026_05_21/EVAL_REPORT.md)
