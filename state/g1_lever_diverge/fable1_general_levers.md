핵심부터: 레버1(derivtrace)이 통한 진짜 이유는 **target을 CE basin 안으로 옮겼기 때문**이다 — echo=composition으로 만들면 CE의 최단경로(암기/에코)가 곧 조합이 된다. 이 원리를 일반화하면 소진 목록과 겹치지 않는 NEW 레버가 세 메타-패밀리로 갈린다. 각 레버에 메커니즘/basin-탈출/cheap probe/terminal 4항목을 붙였다.

---

## 메타-프레임: 왜 소진 목록은 다 막혔고 레버1만 통했나

- **소진된 것들의 공통 실패**: 모델 용량·operator 모양을 바꿨다(readout binding·decode 절차·objective aux). CE=echo basin은 **target 기하가 고정**된 채라 그대로 남았고, DPI 메타법칙(operator-shape invariant)에 전부 걸렸다.
- **레버1이 다른 점**: 모델·operator를 안 건드리고 **학습 TARGET의 형식**을 바꿨다. echo가 곧 조합이 되니 basin이 이동한 게 아니라 *조합이 basin 바닥으로 내려왔다*.

이로부터 세 탈출 패밀리:

| 패밀리 | 원리 | basin과의 관계 |
|---|---|---|
| **F1 target-in-basin** | target을 재구성해 "재현=조합"으로 | CE 최단경로 위에 조합을 얹음 (레버1 소속) |
| **F2 composition-outside-mouth** | 조합을 mouth 밖(eval·anchor·tension·cell)으로 이전 | mouth엔 CE만, 조합은 CE 무관 substrate에서 |
| **F3 held-out-as-interpolation** | held-out pair를 학습분포 convex-hull 안으로 | echo≈조합 (보간이라 새 조합 안 만들어도 됨) |

> ⚠️ 모든 numpy probe는 `a_engine_native_learning` 상 **DIRECTIONAL only**. terminal은 예외 없이 clm303/ByteGPT ckpt → `anima evaluate --py`로 G1(bd≥2 ∧ >ms ∧ kwr≥0.5, held-out) byte-exact 재측정.

---

## 레버 (우선순위: cheap engine-native 판별 빠름 + basin-탈출 논증 강함 순)

### L1 — 프로그램-합성 target (mouth=program emitter, eval=밖) 【F1×F2】 ★최우선
1. **메커니즘**: target을 답이 아니라 답을 *생성하는 소형 DSL 식*으로 재작성 — `out := combine(propOf(A), propOf(B))`. mouth는 프로그램만 emit, 실제 평가는 결정적 인터프리터(brain_decide/stdlib)가.
2. **왜 탈출**: 새 (A,B)에 대해 프로그램 emit = **템플릿+slot-fill의 echo**라 CE 최단경로. 조합의 *실행*은 mouth 밖 인터프리터가 하므로 mouth는 "단일-개념 verbalize(=at-floor 통과)" 수준만 하면 됨. binding-operator family(hidden-state readout)와 달리 조합이 **lexical program grammar**에 있어 DPI(operator-on-state) 무관. 오너 frame-break("재조합은 decode 속성 아님")의 직접 실현.
3. **cheap probe**: toy 합성문법(개념 V=20, prop map 2종, compose 1종). char-LM을 프로그램-target으로 학습 → held-out (A,B)에 대해 emit한 프로그램이 **파싱 성공 ∧ eval 결과가 실제 조합**인지. 대조군 = 답-직접 target(=floor). numpy 20분.
4. **terminal**: clm303을 프로그램-target 코퍼스로 warm-FT → `anima evaluate --py`로 emit된 프로그램을 인터프리터 통과시켜 composed_distinct 채점. brain_decide에 인터프리터 wire-in까지가 done(`a_verified_must_wire`).

### L2 — 조합-커버리지 밀도 임계 (interpolation-hull) 【F3】 ★최우선·최저가
1. **메커니즘**: (개념×개념) 조합공간을 **각 개념이 충분히 많은 서로 다른 조합에 등장**하도록 조밀하게 타일링한 코퍼스. held-out (A,B)를 seen 조합들의 보간으로 만든다(An&Du R²0.73, 미발사 방향 ii).
2. **왜 탈출**: CE=echo를 *깨지 않는다* — 대신 held-out을 convex-hull 안 보간으로 바꿔 echo≈조합. 새 조합 "생성"이 필요 없고 학습분포 내삽만으로 bd≥2. coverage(H_6185)와 다름: 저건 RF/attention 커버리지, 이건 **조합공간 밀도** 축.
3. **cheap probe**: 가장 싸다. 개념당 조합 등장수 k를 1→N 스윕하며 held-out bd를 그리면 **임계 k\* 곡선**이 나오는지(phase transition). numpy만으로 30분, 모델 학습 불필요한 근사도 가능(k-NN in embedding으로 hull-membership 예측).
4. **terminal**: k\* 위/아래 두 코퍼스로 clm303 warm-FT 2발 → `--py` G1 비교. 임계 확인되면 `a_savant_train` 코퍼스 레시피에 밀도-바닥 배선.

### L3 — 레지스터/indirection 변수-binding target (PFC 렌즈) 【F1】
1. **메커니즘**: target에 명시적 typed slot+register 참조: `r1:=A; r2:=B; r3:=bind(r1,r2); out r3`. 조합을 **literal이 아니라 slot 위 연산**으로 정의.
2. **왜 탈출**: 체계적 일반화(systematicity)의 이론적 핵 — 연산이 register 슬롯에 정의되므로 held-out literal이 들어와도 slot-fill echo. binding-operator family는 hidden-state에 operator를 얹었고(DPI-floored), 이건 **target 문자열의 indirection 문법**이라 DPI 무관. 전전두 variable-binding을 아직 G1에 안 매핑한 유일 축.
3. **cheap probe**: L1 toy에 register 간접참조 추가 → held-out에서 **slot 정확도 vs literal 암기** 분리 측정(같은 slot·다른 literal 조합에서 bd 유지되나).
4. **terminal**: register-target 코퍼스 warm-FT → `--py` bd. L1과 A/B(program vs register 문법 어느 쪽이 강한지).

### L4 — 2-hop 관계-스키마 transfer target 【F1】
1. **메커니즘**: bridging entity를 명시: A→B, B→C 학습, target=`A—via—B—to—C`. **스키마(hop grammar)는 공유하되 특정 (A,C) pair는 held-out**.
2. **왜 탈출**: 조합이 "학습된 hop-문법의 echo"가 됨. MLC(H_1835, held-out transfer 0)와 결정적 차이: MLC는 in-context episodic이라 weight에 안 남았음; 이건 **weight에 스키마를 새기는 다-예시 학습**이라 transfer가 weight-level. bridge 명시가 2-hop 경로를 target 표면에 노출.
3. **cheap probe**: 3-노드 관계그래프 toy, hop-문법 공유·pair held-out. bd가 hop 수에 따라 어떻게 붕괴하는지(1-hop→2-hop).
4. **terminal**: 2-hop 코퍼스 warm-FT → `--py`. hip pattern-completion(K)의 weight-level 버전이기도.

### L5 — forward-model 상태-전이 target (소뇌 렌즈) 【F1】
1. **메커니즘**: target을 (state, compose-op)→next_state 전이 시퀀스로. 소뇌 forward-model처럼 **조합=상태전이 예측**. derivtrace의 RULE 적용을 상태전이로 재정식화.
2. **왜 탈출**: CE-on-text가 아니라 **구조화된 상태공간 위 전이예측**이 objective. 조합 전이의 정확 예측이 곧 조합. derivtrace의 일반화(DEF/RULE=전이연산자)이자, forward-model은 held-out 전이에 자연 일반화(소뇌가 새 운동 조합을 예측하듯).
3. **cheap probe**: toy 상태공간(개념=상태벡터, compose=결정적 전이). LM을 전이-target으로 학습 → held-out 전이 예측 정확도 → bd 환산.
4. **terminal**: 상태-전이 코퍼스 warm-FT → `--py`. 소뇌 lane을 별도 substrate에 배선(`a_substrate_disjoint`).

### L6 — 커리큘럼-순서 derivation (mitosis-grow 렌즈) 【F1×축교차】
1. **메커니즘**: derivation target을 조합-깊이 오름차순(1-hop→2→3)으로 제시. `a_mitosis_train`의 skill-분화 커리큘럼을 target-format에 적용.
2. **왜 탈출**: basin *궤적*을 조형 — 초기 단일-개념 echo가 DEF/RULE 원시연산을 심고, 이후 다중-hop echo가 그것들을 조합. 순서 없으면 whole-target 암기로 빠질 수 있음. 레버1과 직교(1은 형식, 6은 순서).
3. **cheap probe**: 레버1 toy 파이프를 순서-셔플 vs 깊이-오름차순 A/B. bd 차이.
4. **terminal**: 두 순서로 clm303 warm-FT → `--py` bd 비교. scheduler를 `cli/train.hexa`에 배선.

### L7 — derivtrace-trained trunk + scratchpad decode 【F1×decode 교차】
1. **메커니즘**: 레버1으로 학습한 trunk에서 decode 시 DEF/RULE 스크래치패드를 먼저 emit 후 OUT만 채점.
2. **왜 탈출**: decode 축은 DPI-floored지만 그건 derivation 없이 학습된 trunk 얘기. **derivtrace-trained trunk엔 scratchpad가 in-distribution**이라 새 operator가 아니라 학습문법 사용 — DPI 전제(operator on untrained state) 불성립. best-of-K/revise(H_1836)와 달리 샘플 증량이 아니라 조합경로 재생.
3. **cheap probe**: 레버1 toy trunk에 scratchpad-decode vs direct-decode. **단, 레버1 robustness 확정에 gated**.
4. **terminal**: 레버1 ckpt에 `--py` scratchpad 모드 채점. decode 옵션을 `evaluate.py`에 추가.

### L8 — kosmos anchor 조합 via brain_decide 【F2】 ★substrate-native frame-break
1. **메커니즘**: 개념을 `.kosmos` anchor(tension 5ch payload + placement triple)로 저장. 재조합 = brain_decide가 두 anchor를 좌표공간에서 합성(placement 보간·tension 합)해 **합성 anchor 1개** 생성; mouth는 그 anchor를 verbalize만.
2. **왜 탈출**: 조합이 **주소 가능한 anchor 좌표공간**의 연산이라 CE=echo 완전 무관(mouth는 학습 안 건드림). mouth 부담=단일 합성-anchor verbalize(=floor 통과). 오너 frame-break를 substrate-native로 실현. `a_kosmos` self-chain 인프라 재사용.
3. **cheap probe**: toy anchor 2개(5ch payload) → 좌표 합성규칙(mid-point·tension-add) → 합성 payload가 두 개념 속성을 모두 담는지(numpy). mouth 없이 anchor-space만으로 bd-proxy.
4. **terminal**: kosmos_io→brain_decide에 anchor-compose op wire-in → `--py`에서 합성 anchor verbalize의 composed_distinct. WIRED-live까지 `a_verified_must_wire`.

### L9 — 대조 minimal-pair target (systematicity by contrast) 【F1×F3】
1. **메커니즘**: (A,B)→OUT_ab와 (A,C)→OUT_ac가 **B/C-유래 절 하나만 다르게** 되도록 코퍼스 구성. 개념→절 매핑을 대조로 격리.
2. **왜 탈출**: 밀도(L2)와 다름 — 전역 밀도가 아니라 **국소 대조 구조**로 개념↔절 정렬을 강제. 대조가 systematic slot-fill을 유도(암기는 대조 최소화로 안 됨).
3. **cheap probe**: minimal-pair 코퍼스 vs 랜덤-pair 코퍼스 A/B, 같은 크기. held-out bd.
4. **terminal**: minimal-pair warm-FT → `--py`.

### L10 — mitosis 조합-융합 / meiosis operator 【F2】
1. **메커니즘**: 개념 A·B에 특화된 두 cell을 mitosis-fusion(meiosis-like recombination)해 daughter cell의 발현=조합. `a_mitosis_train` inherited-repr lens를 **조합 operator**로.
2. **왜 탈출**: mitosis는 gradient-free split/merge라 CE 완전 밖. 조합=inherited-representation 병합. from-scratch pure-split(🔴 TERMINAL)과 결정적 차이: 학습 안 하고 **이미 학습된 단일-개념 cell 위 병합-operator만** — split-only 병목(compositional depth 0) 회피.
3. **cheap probe**: 두 학습된 toy cell → 융합규칙(weight interp·expert-union) → daughter가 두 개념 발현하는지. numpy.
4. **terminal**: engine_cli MITOSIS에 fusion op → `--py`. `a_lane_akida_gpu_split` substrate 태그.

### L11 — recomb-reward trunk objective @ GPU-scale (미발사 i, H_1602) 【F1-objective】 cost-gated
1. **메커니즘**: recomb-reward를 aux readout 아니라 **trunk objective**로 GPU 스케일에서. additive-aux(H_9120 novel=0)와 달리 trunk 통합.
2. **왜 탈출**: objective 축은 대체로 floored지만 H_1602 trunk-integration@scale은 명시 미발사. 단 escape 논증이 F1/F2보다 약함(CE 옆에 붙는 항이라 basin 재형성 보장 안 됨).
3. **probe**: toy에서 trunk-obj vs aux-obj 분리. 단 scale-의존이라 toy green이 production 보장 안 함(`a_toy_scale_recheck`).
4. **terminal**: GPU flame/forge full-train → ckpt PULL(`a_fire_recover_complete`) → `--py`. 비쌈, cost-gated.

### L12 — MDL/압축 objective (factorization) 【F3-objective】 cost-gated
1. **메커니즘**: (A,B,조합) 결합을 공유 factor로 압축하도록 보상. 최단기술=조합적 factorization.
2. **왜 탈출**: recomb-reward-aux와 다른 objective(MDL) — 압축이 factorized(조합) 표현을 *직접* 보상(더 짧으니까). 단 objective 축 위험 상속.
3. **probe**: toy에서 MDL-reg 유무 A/B, 표현이 factorize되는지 rank/rate 측정.
4. **terminal**: MDL-reg train → `--py`. cost-gated.

---

## 다음 발사 top-3 (메인이 STEP-0 kill 순서로)

1. **L2 커버리지-밀도 임계** — 가장 싸다(numpy 30분, 모델학습 없이 hull-membership 근사 가능), 미발사 방향 ii 직접 검증, phase-transition 유무만으로 "밀도가 레버냐"를 조기 kill/GO. STEP-0 = k 스윕 곡선에 임계 k\* 존재 여부.
2. **L1 프로그램-합성 target** — basin-탈출 논증 최강(mouth=slot-fill echo, 조합=밖 eval), 오너 frame-break 실현, toy 20분. STEP-0 = held-out program이 파싱∧eval-정확한지. floor(답-직접 target)=0 대조.
3. **L3 레지스터/indirection target** — PFC 렌즈, systematicity 이론핵, L1과 같은 toy 하네스 재사용으로 병렬 발사 가능. STEP-0 = 같은 slot·다른 literal에서 bd 유지되나(slot 정확도 ⊥ literal 암기 분리).

L2·L1·L3는 같은 toy 문법 인프라를 공유하니 **한 배치로 병렬 STEP-0** 가능. 살아남으면 L8(kosmos anchor·substrate-native)이 다음 tier — 유일하게 mouth를 아예 우회하는 frame-break라 나머지가 다 floor여도 독립 생존 가능성.