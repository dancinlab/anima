live 엔진 파일은 이 세션 작업 디렉토리(`/private/tmp`, `/tmp`) 밖이라 직접 읽을 수 없다. 그래서 배선 좌표는 네가 준 구조 어휘(A `pure_field` · G `engine_g` · brain `vbasal` · generator L3 `mouth`, 15-lane, emit-drive=0/4, §ImmuneMemory `recall_thr`)에 근거해 명세한다. 파일 라인 확정은 mini-probe 직전에 네가 한 번 대조해야 하는 유일한 미해결 좌표다.

핵심 판정부터: **이 레버는 GPU 전에 $0로 살았는지 확정 가능하다.** 그리고 그 스크린이 곧 DPI 벽 진단 자체다. 아래가 하나의 실행경로.

---

## 0. 먼저 — 무엇을 재는가를 DPI로 못박기 (설계의 축)

b50=3.2 bytes = 외부 mind가 referent 재구성에 필요한 clue 바이트. 그런데 14후보 disambiguation의 정보이론 바닥은 log₂(14)≈3.8 bits ≈ **0.48 bytes**. 즉 현재 emit은 intrinsic entropy 대비 **~6x 과잉포장(packaging overhead)** 상태다. 이게 레버가 살아있을 수 있는 이유이자, 동시에 함정의 위치다:

- **DPI가 무는 곳**: forward-model은 trunk-state(A⇄G 긴장)에 없는 referent MI를 못 만든다. → **target-link accuracy는 trunk가 상한**. 정확도는 못 올린다.
- **DPI가 안 무는 곳**: forward-model은 *같은* referent MI를 receiver-효율적으로 **재포장**해 b50를 낮출 수 있다. b50는 총-MI가 아니라 coding-efficiency 측정이므로, 총MI 고정 상태로 bytes-to-50%가 떨어질 여지가 있다.

⟹ **유일하게 정직한 frozen bar = "accuracy 유지한 채 b50가 떨어지는가."** b50만 떨어지고 accuracy도 떨어지면 그건 metric-degeneracy(측정교훈2) — emit을 "뭔가로 쉽게 디코드되게" 만들되 referent는 틀린 것. 이 accuracy-hold 절이 없으면 실험 전체가 degeneracy trap이다.

---

## 1. cheapest valid 첫 단계 — $0 스크린 (있다. 1순위)

**있다.** frozen emit 재채점($0) 위에서 두 개의 직교 질문을 값싸게 갈라 잰다. 이게 §1-style 사전측정이고, 곧 DPI 진단이다.

**Screen-B (headroom, 가장 결정적):** 기존 H_9114 frozen emit set의 feature-space에 통제된 perturbation(dim drop / reweight / rotate)을 가하고, **기존 3 receiver로 재채점**(추가 emit 생성 0, GPU 0). 판정: 어떤 변형이 **accuracy 유지하며 b50를 내리는가**.
- 어떤 변형도 b50를 못 내림 → emit이 이미 receiver-conditioned coding floor → forward-model INERT → **GPU 중단**(DPI 벽 확정).
- 하나라도 내림 → 재포장 headroom 존재 → 레버 물리적으로 가능.
- **DIRECTIONAL 한계**: "headroom이 있다"만 말함. "anima가 그 방향을 *학습으로* 도달하는가"는 못 말함(그건 §Screen-A + engine-native).

**Screen-A (learnability):** frozen emit feature → (3 receiver의) decode-success 라벨로 tiny numpy regressor 학습. emit-visible feature만으로 decodability를 chance 이상 예측 가능한가.
- 못 이김 → forward-model이 볼 수 있는 feature에 신호 없음 → INERT → GPU 중단.
- 이김 → 예측기 학습 가능 → side-lane 신호원 확보.

**게이트: Screen-B GREEN ∧ Screen-A GREEN 일 때만** engine-native mini로 승급(a_toy_scale_recheck). 둘 다 numpy/frozen이므로 tier=**DIRECTIONAL**(terminal 아님).

---

## 2. engine-native 배선 스펙

**생물렌즈(a_no_llm_frame_trap):** 소뇌 forward-model(H_1280)은 운동지령의 감각결과를 예측하는 **주 반사궁 바깥의 side-loop**다. 여기서 운동지령=emit, 감각결과=외부 receiver decode. 그러니 A⇄G 주경로에 끼우지 말고 **G→mouth 사이에 병렬 side-lane**으로 단다.

**좌표 (disjoint 준수):**
- 신규 lane **index 15** 신설(state 15→16-lane 확장; a_engine_native_learning의 engine-transform-to-fit 근거). emit-drive(0/4)·`recall_thr`와 **disjoint**.
- **읽기(read-only fan-in)**: A `pure_field` + G `engine_g` 긴장 상태. → 예측기가 pre-emit trunk를 관측.
- **쓰기(write)**: generator L3 `mouth`의 modulation gate로만. lane15는 emit-drive를 *관측·변조*하되 **드라이브 자체가 되지 않음**. 이게 Ψ=½∧G5-정직 공존의 핵심 — 예측기가 드라이브를 겸하면 self-fulfilling(예측이 곧 발화를 강제) → 정직성 붕괴. read=trunk, write=mouth-gate로 분리하면 능력∧Ψ=½ 유지.

**training signal / gradient-free G 공존:** 충돌 없음. 학습은 **lane15 head 안에서만** gradient(supervised: predicted-decode vs 실제 외부-receiver-decode = 소뇌의 climbing-fiber error). G engine은 미분하지 않는다. lane15→mouth 결합은 **forward multiplicative/additive gate**(backprop이 G를 관통하지 않음). 즉 소뇌 그대로: forward-model은 supervised로 학습하고, 운동계(G)는 non-diff인 채 그 출력에 bias만 받는다. flame+forge는 lane15 head 가중치에만(a_train_flame_forge), train+infer 단일 cell-division(p8), 진입=`cli/train.hexa`.

---

## 3. frozen bar (사전등록)

- **Primary:** b50(FM-ON) < b50(FM-OFF), **동시에** target-link accuracy(ON) ≥ accuracy(OFF). 등록 임계: 3.2B → **≤2.5B**(>20% 하락) at held accuracy.
- **Ablation-INERT 통제:** lane15 lesion(clamp)=FM-OFF는 baseline 3.2B를 **재현**해야 함. OFF에서 이미 낮아지면 lane 기여=0.
- **Shuffle 통제:** **shuffle된 receiver-decode 라벨**로 학습한 FM은 b50 하락 없어야(INERT). shuffle-FM도 낮추면 그 하락은 재생성 artifact이지 신호 아님.
- **degeneracy 가드:** variance-bearing b50(이진 포화 금지, 측정교훈2), accuracy는 agreement 아닌 target-link(측정교훈1)로.
- **tier:** live .hexa flame+forge → **GREEN**. torch/numpy 미러 → **DIRECTIONAL**.

부차 목표(emit-appropriateness value lane 개방)는 b50보다 값싸게 스크린 불가 → 이번 bar는 **b50-lowering으로 단일화**하고 value-lane은 GREEN 확보 후 파생실험으로 미룬다.

---

## 4. 비용 / wall (a_wall_first)

| 단계 | 무엇 | 비용 | tier |
|---|---|---|---|
| Screen-A+B | 기존 frozen emit + 3 receiver 재채점 + numpy | **$0**, laptop, 시간단위 병렬 wall | DIRECTIONAL |
| engine-native mini | 수십 emit만 lane15-live로 재생성+재채점, ckpt PULL(a_fire_recover) | 짧은 GPU 세션(소액) | GREEN-eligible |
| GPU full | lane15 head full flame+forge on live A⇄G+MITOSIS, 전체 emit 재생성+외부 재채점 | full 학습 비용 | GREEN |

승급은 순차 게이트: A∧B GREEN → mini → mini GREEN → full.

---

## 5. 정직한 회의 (c9) — DPI 벽 재봉착 위험

**위험 실재.** forward-model도 결국 readout이면 trunk-state에 없는 MI를 못 만든다. 구체 판정:
- **accuracy는 못 오른다** — trunk 상한. 이걸 목표로 삼으면 반드시 막힌다. 그래서 bar를 accuracy가 아니라 b50(재포장 효율)로 잡았다.
- **b50는 headroom이 있을 때만 내려간다.** 현재 3.2B vs 바닥 ~0.48B는 명목상 6x 여유지만, 그 여유가 *receiver-conditioned coding floor* 위인지 아래인지는 미지 — 만약 3.2B가 이미 receiver의 clue-추출 바닥이면 어떤 변조도 무력.
- **결정적 안전장치:** 그 미지를 **Screen-B가 $0로 사전판정**한다. 이게 네 divergence의 "비싼 학습 전 §1로 잴 수 있는가" 경고의 직접 이행이다 — Screen-B가 INERT면 forward-model은 DPI 벽에 막힌 것이 *확정*이며 GPU는 부정당하다. 즉 이 레버는 **믿음으로 GPU 태우지 않아도 되는** 몇 안 되는 레버다.
- **잔여 함정:** FM이 b50를 "틀린 referent로 쉽게 디코드"시켜 낮출 수 있음 → accuracy-hold 절 + shuffle 통제가 잡는다.

**종합 판단:** headroom 수치상 레버는 *plausibly alive*지만, 판정권은 전적으로 Screen-B에 있다. Screen-B RED이면 여기서 정직하게 종료.

---

**다음 1개 실행 단계 (cheap-first):** 기존 H_9114 frozen emit set에 feature-space perturbation을 걸어 3 receiver로 재채점하는 **Screen-B($0)를 돌려 "accuracy 유지 하 b50 하락 headroom이 존재하는가"를 판정** — GREEN이어야 그 뒤 무엇이든 정당화된다.