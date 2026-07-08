γ 발산 시작. 핵심 재진단부터 박고(이게 발산 축을 결정한다) 라운드로 쏟아낸다.

---

## 재진단 — 왜 전부 죽었나 (DPI 메타법칙의 정체)

죽은 레버들의 **공통 실패원인 하나**로 압축된다:

> **binding term을 *추가*했지만, primary loss는 여전히 additive로 풀 수 있었다.**

DPI(min-complexity fit) 하에서 모델은 loss를 낮추는 **가장 싼 경로**를 택한다. additive 해가 항상 존재하고 더 싸면, aux binding 항(gate·detector·L_bind)은 trivial하게 만족시키고(FORM) 실제 joint은 안 만든다. readout-binding이 게임된 것도, additive-aux가 floor인 것도, de-risk R²가 강한 total-order additive를 못 이긴 것도 전부 이 한 문장이다.

**따라서 발산의 지배원리(메타 축 선(先)적용):**
γ는 "binding을 **보상**하는 항"이 아니라 **"additive 해를 primary objective에서 *불가능/더 비싸게* 만드는 데이터·타깃 구조"** 여야 한다. binding이 loss 감소의 **유일한 최싼 경로**일 때만 EARNED된다. 이건 loss-term 속성이 아니라 **task/generator 구조 속성**이다.

이 렌즈로 죽은 것 vs 살 것을 가른다: **binding을 offer(capacity로 제공)** = 전부 재-floor. **binding을 necessitate(additive를 primary에서 죽임)** = 미검증. 아래 발산은 대부분 후자를 어떤 레버로 강제하느냐의 직교 변주다.

---

## Round 1 — "additive를 primary에서 죽인다" objective/generator 축

### 1. `xor-primary-target` — 비가법 label을 next-byte primary에 직접 박기
1. **mechanism**: A+B의 타깃을 marginal-비정보(E[y|A]=E[y|B]=chance) & joint-결정적인 XOR/parity 구조로 설계. aux 없음 — **primary next-byte 예측 자체**가 joint를 요구.
2. **왜 이기나**: additive 해의 상한이 **task상 chance로 고정**됨(수학적으로). 보상항이 아니라 천장을 additive에 씌운 것. 죽은 additive-aux는 primary가 additive-solvable이었음.
3. **파괴통제**: 학습 예제 간 (A,B) 쌍 shuffle → label 완전 파괴(chance). shuffle 붕괴 = 정의상 built-in. 양성대조 = 동일 데이터에 additive-solvable label(주효과 있는) 버전 → 그건 통과해야(FORM 살아있음 증명).
4. **측정**: cheap numpy 가능. 소형 probe로 held-out XOR-조합 정확도 vs additive-baseline Δ. **방향은 지금 numpy로 본다.**
5. **위험**: byte-LM이 XOR을 lookup-table(모든 A×B 암기)로 풀어버리면 held-out에서 붕괴 = "재조합"이 아니라 암기 실패. → held-out 조합 커버리지로 lookup을 배제해야. 이게 진짜 관문.

### 2. `anti-additive-curriculum` — 학습분포서 additive escape-hatch 제거
1. **mechanism**: primitive A·B가 **오직 additive 예측이 틀리는 문맥에서만** 등장하도록 데이터 스케줄. 즉 train에서도 additive를 벌함.
2. **왜 이기나**: 죽은 gen-split(MLC/SCAN)은 additive가 train은 통과하고 held-out만 실패 → 모델이 train-최적=additive에 안착. 여기선 train-최적 자체가 non-additive.
3. **파괴통제**: additive-baseline이 train-loss부터 못 내려가야(양성 신호). shuffle → 스케줄 붕괴.
4. **측정**: 데이터 생성만 하면 numpy probe 가능. curriculum 효과는 GPU 학습 필요(방향은 toy numpy).
5. **위험**: 모델이 additive+"틀린-문맥 예외 lookup"으로 우회(memorized correction). 예외를 held-out 조합으로 강제 확장해야.

### 3. `bilinear-generator-complexity-flip` — additive를 *고비용* 해로 만들기 (메타 역이용의 정석)
1. **mechanism**: 데이터 생성자를 저-rank **bilinear** 맵(A ⊗ B → y)으로 두면, additive 근사는 A×B 전조합 lookup(거대 파라미터) 필요, bound(bilinear) 해는 compact. implicit regularization이 이제 **bound를 선호**.
2. **왜 이기나**: 죽은 것들은 전부 inductive bias(min-complexity)와 **싸웠다**. 이건 bias가 binding을 고르게 task를 정렬 — 최초로 흐름을 거스르지 않는 설계.
3. **파괴통제**: 동일 rank의 additive-generator(주효과만) 대조 → 거기선 additive가 이겨야. bilinear-generator에서만 bound lift. shuffle → rank 구조 파괴.
4. **측정**: **numpy로 지금 강하게 본다** — 생성자 조작이 완전 통제됨. 소형 bilinear 회귀에서 held-out 셀 lift Δ.
5. **위험**: synthetic 냄새. 자연 corpus로 옮길 때 실제 언어의 조합이 정말 low-rank bilinear인지가 관문(아닐 수 있음).

### 4. `conjunctive-dictionary-sparse` — 사전 atom을 A∧B 켤레로, sparsity가 강제
1. **mechanism**: sparse-coding 사전에서 A+B를 두 primitive atom(비용 2)보다 **하나의 conjunctive atom(비용 1)** 으로 표현하는 게 싸도록 sparsity prior. 조합이 반복되면 켤레 atom이 emerge.
2. **왜 이기나**: 3번과 같은 복잡도 역이용을 표현측에서. additive superposition은 sparsity 페널티를 더 냄.
3. **파괴통제**: atom 사용통계 — 진짜면 held-out 조합이 학습된 켤레 atom을 재사용(activation 추적). shuffle → 켤레 atom 활성 붕괴.
4. **측정**: numpy sparse dict-learning probe 가능(방향).
5. **위험**: 자주-등장 조합만 atom화 = coverage-density floor 재방문. 저빈도 held-out엔 무력할 수 있음.

### 5. `polysemy-necessity` — 각 개념을 단독 애매하게, 상호로만 disambiguate
1. **mechanism**: A를 다의어로 설계(뜻이 B에 의존). 모델이 A를 확정하려면 **반드시 B를 참조** → 강제 joint 처리. word-sense disambiguation 그 자체.
2. **왜 이기나**: additive는 A의 뜻을 B와 독립으로 고정 → 체계적으로 틀림. 자연어에 실재하는 구조(가장 corpus-친화적).
3. **파괴통제**: B를 랜덤 치환 → A 뜻 오확정 → 붕괴. context-B 있는/없는 조건 대조.
4. **측정**: **실 corpus에서 numpy로 지금 본다** — 다의 토큰의 문맥의존 예측 Δ(문맥 있음 vs 셔플). 가장 싼 실데이터 probe.
5. **위험**: attention 있는 LM은 이미 어느정도 함 → Δ가 작아 additive와 안 갈릴 수 있음. hard-polysemy(문맥 없으면 chance) 셋 필요.

**이 라운드 신규 5개.**

---

## Round 2 — invertibility / 정보보존 (bound면 복원된다, additive면 crosstalk)

### 6. `unbind-recovery-crosstalk` — 다중 role-filler 동시 binding + 역질의 복원
1. **mechanism**: N개 (role,filler) 쌍을 하나의 벡터에 bind → "role R로 bound된 filler는?" 역질의로 복원. 쌍 수 N↑ 시 additive superposition은 crosstalk가 O(N)으로 폭발, 진짜 binding 연산자(원형 컨볼루션류)는 저-crosstalk.
2. **왜 이기나**: 죽은 combiner는 단일 조합(N=1)이라 additive와 안 갈렸다. **N을 키워 additive의 crosstalk를 primary 오차로 노출**. capacity offer가 아니라 용량 압박으로 necessitate.
3. **파괴통제**: role-filler 쌍 shuffle → 복원 wrong-filler. N-sweep이 곧 ablation(N↑ additive만 무너지는 곡선 = earned 증명).
4. **측정**: numpy로 crosstalk-vs-N 곡선 지금 본다. 학습 binding-op은 GPU.
5. **위험**: 모델이 N을 순차 슬롯(list)으로 우회 = binding 아닌 addressing. 고정예산·병렬질의로 슬롯 배제.

### 7. `cycle-consistency-decompose` — A+B→C 합성과 C→(A,B) 분해의 왕복 일치
1. **mechanism**: forward가 합성, backward가 분해, cycle-loss가 묶음. 합성이 **정보보존**(무손실 복원 가능)이어야만 cycle 만족.
2. **왜 이기나**: additive sum은 collision으로 비가역 → cycle-loss가 primary에서 못 내려감. 죽은 additive-aux와 달리 aux가 아니라 왕복 제약이 primary.
3. **파괴통제**: 분해 타깃 shuffle → cycle 붕괴. 합성만/분해만 ablation.
4. **측정**: toy numpy autoencoder-composition 방향 가능. 본학습 GPU.
5. **위험**: cycle을 identity-copy(A,B를 그냥 concat 보존)로 우회 → "결합" 없이 통과. bottleneck 차원 압박으로 concat 배제 필요(압박=collision 유도=역효과 주의). 미묘함.

**이 라운드 신규 2개.**

---

## Round 3 — discriminator / 측정-우선 (additive를 대조군으로 *구성*)

### 8. `residual-lift` ⭐ — frozen-additive 잔차만 γ가 예측
1. **mechanism**: 2단. ① 최선 additive 모델 frozen 학습. ② γ는 (y − additive_pred) **잔차**만 예측. 잔차 = 정의상 additive가 못 닿는 비가법 상호작용.
2. **왜 이기나**: additive가 **문자 그대로 대조군**. earned-bind margin = 잔차모델의 held-out lift(Δ). "값 아닌 차분" 메타법칙을 설계에 내장. 게임 불가 — 잔차엔 additive 성분이 수학적으로 0.
3. **파괴통제**: (A,B) shuffle → 잔차가 순수 노이즈 → 잔차모델 held-out lift 0(붕괴가 곧 판정). 이게 가장 깨끗한 THEATER-차단.
4. **측정**: **numpy로 지금 방향 확정 가능** — 가장 저비용·해석 명료. 추천 최우선 probe.
5. **위험**: 잔차가 held-out에서 노이즈뿐이면(진짜로 언어에 가법성 넘는 신호 없으면) → 그 자체가 **벽=능력천장의 결정적 증거**(negative지만 값진 종결).

### 9. `synergy-pid` — 부분정보분해의 synergy 항을 직접 최적화/측정
1. **mechanism**: PID로 joint가 marginal에 없는 **synergistic 정보**를 분리, 그걸 목표/probe로. additive floor = synergy 0(정의상).
2. **왜 이기나**: 정보이론적으로 additive/bound를 원리적으로 가르는 유일 지표. FORM 게임 불가(추정량이 marginal을 명시적으로 뺌).
3. **파괴통제**: shuffle → synergy→0. redundancy/unique 항이 대조.
4. **측정**: synergy 추정 numpy 가능하나 고차원서 추정 편향 큼(주의). 소형 probe 방향용.
5. **위험**: PID 추정 불안정 → 학습 신호로는 약함. **8번의 진단 파트너**로 쓰는 게 맞음(objective보다 measurement).

### 10. `adversarial-additive` — additive 재구성 적대자와의 minimax
1. **mechanism**: γ의 joint-rep을, adversary가 emb(A)+emb(B)로 **재구성 못하게** 학습(minimax). adversary 성공=additive로 설명됨=γ 패.
2. **왜 이기나**: additive 가설류를 **명시적 적대자**로 세워 non-additive 다양체로 밀어냄. 죽은 contrastive와 달리 additive class 전체를 상대(hard negative 자동생성).
3. **파괴통제**: adversary 수렴을 대조 — 진짜 bound면 adversary loss 바닥 안 침. shuffle → adversary 쉽게 성공.
4. **측정**: 소형 GAN-류 numpy 방향, 안정성 위해 GPU 권장.
5. **위험**: minimax 불안정 → γ가 non-additive지만 **무의미한** 다양체로 도피(useless bind). 반드시 downstream 능력 Δ로 게이팅.

### 11. `contrastive-joint-vs-sum` — joint emb ≠ sum emb를 InfoNCE로
1. **mechanism**: positive=진짜 joint, hard-neg=additive 예측 emb(A)+emb(B) & 어긋난 joint. joint를 sum과 관계적으로 분리.
2. **왜 이기나**: 배치-관계 loss라 단일 gate로 게임 어려움(1-항 FORM 아님). 죽은 readout-binding의 게임가능성 보완.
3. **파괴통제**: neg에 shuffled A'+B 포함. shuffle→positive/neg 구분 소멸.
4. **측정**: numpy contrastive probe 방향. 본학습 GPU.
5. **위험**: joint≠sum을 사소한 nonlinear bump로 만족(구별은 되나 능력 무증). 능력 Δ 게이팅 필수. 8번보다 게임여지 큼.

**이 라운드 신규 4개.**

---

## Round 4 — representation 연산자 축 (⚠️ task-necessitate 없이는 재-floor)

> 정직 경고: substrate-combiner가 이미 floored. representation-only는 offer라 대부분 재-floor. **아래는 반드시 Round1–2의 necessitating task와 짝지을 때만 산다.** 연산자 자체는 novel하되 단독으론 유망도 낮게 매긴다.

### 12. `tpr-hrr-vsa-operator` — tensor-product / 원형컨볼루션 / VSA 결합 연산자
1. **mechanism**: 곱셈적 결합(⊗ 또는 ⊛)으로 role-filler bind. 대수적으로 비가법·가역.
2. **왜 이기나**: 연산자 수준서 additive 불가능(곱은 합으로 안 나옴). 단 **task가 이 연산자를 필요로 해야**(6번과 짝).
3. **파괴통제**: unbind 정확도 shuffle 붕괴.
4. **측정**: numpy로 HRR crosstalk 지금 본다(고전 결과 재현).
5. **위험**: 단독 offer면 모델이 안 쓰고 additive로 회귀 = substrate-combiner floor 재방문. **필히 6/7과 결합.**

### 13. `dendritic-coincidence-AND` — 수상돌기 NMDA-스파이크식 곱셈 AND 유닛
1. **mechanism**: 입력 쌍의 곱(coincidence)만 발화하는 유닛 — 생물학적 AND. 합으로 AND 불가.
2. **왜 이기나**: 진짜 conjunction detector(합-불가능). bio-substrate-first 렌즈, LLM frame 탈피.
3. **파괴통제**: 두 입력 시간창 어긋냄(desync) → 무발화. 단일입력 ablation.
4. **측정**: numpy 곱-유닛 probe 방향.
5. **위험**: bilinear gating과 수학 동형 → 그게 이미 combiner floor였다면 재탕. bio 서사가 새 mechanism을 보장하진 않음(정직).

### 14. `orthogonal-carrier-multiplex` — CDMA/FDM식 직교 반송파 결합
1. **mechanism**: A·B를 직교 코드에 실어 superpose, joint decode는 상관검출로 둘 다 요구.
2. **왜 이기나**: 반송파 없으면 decode 불가 → additive-plain 붕괴.
3. **파괴통제**: 코드 셔플 → decode 실패.
4. **측정**: numpy(신호처리) 즉시.
5. **위험**: VSA(12)의 특수케이스 — 진정 새 family 아님. **12로 흡수 가능**(발산 카운트서 half로).

### 15. `disentangle-then-bind` — 먼저 factor 직교화, 그다음 결합
1. **mechanism**: A·B를 독립 부분공간으로 disentangle 후 알려진 연산자로 bind. combiner가 floored한 건 피연산자가 엉켜있어 bind할 clean operand가 없었기 때문일 수 있음.
2. **왜 이기나**: 죽은 combiner의 **전제조건 결함**(entangled operand)을 교정. 새 진단각.
3. **파괴통제**: disentangle 품질 ablation(엉킨 채 bind → floor 재현이 대조).
4. **측정**: numpy disentangle metric 방향.
5. **위험**: disentanglement 자체가 미해결 난제 → 관문 이동일 뿐.

**이 라운드 신규 3.5개**(14는 12로 반흡수).

---

## Round 5 — bio/physics 동역학 축 (진짜 새 코드)

### 16. `phase-synchrony-binding` — 감마대역 위상동기 = 결합 (시간적 binding 가설)
1. **mechanism**: hidden 유닛에 위상좌표((cos,sin) 또는 복소). 공결합 특징은 위상동기, 비결합은 비동기. 결합=간섭(곱적, 비가법).
2. **왜 이기나**: 결합이 **동역학 상태**(위상)로 표현 — 정적 additive rep와 원리적으로 다른 코드. neuro-substrate-first.
3. **파괴통제**: 위상 랜덤화(desync) → readout 붕괴. 동기/비동기 대조 = 내장 ablation.
4. **측정**: numpy 복소 유닛 probe 방향(작게). 본학습 GPU(복소 backprop).
5. **위험**: byte-LM에 자연 진동 없음 → 위상이 학습되지 않고 artifact. 가장 exotic·고위험.

### 17. `energy-attractor-joint-basin` — 모던 홉필드: joint만의 attractor basin
1. **mechanism**: 에너지함수서 joint 패턴은 최소, additive superposition은 최소 아님. 부분단서서 pattern completion이 joint 복원.
2. **왜 이기나**: 결합이 landscape의 cross-term(비가법)으로 encode. attention=modern Hopfield라 배선 자연스러움.
3. **파괴통제**: shuffled 쌍 → basin 없음 → completion 실패.
4. **측정**: numpy Hopfield 즉시 방향.
5. **위험**: attention이 이미 이걸 근사 → 기존 trunk가 실패한 것과 겹칠 수 있음. Δ가 작을 위험.

### 18. `causal-counterfactual-composition` — do(A) 개입 하 효과변조 일관성
1. **mechanism**: do(A=a') 개입이 B 고정 하 joint 출력을 구조방정식대로 바꾸도록 학습. 효과변조(effect modification) = 비가법 인과.
2. **왜 이기나**: additive는 counterfactual서 A효과가 B와 독립이라 체계적 오답. 인과렌즈 — 완전 직교.
3. **파괴통제**: 개입-라벨 shuffle → 일관성 붕괴. 관측만(개입無) 대조.
4. **측정**: 개입 데이터 필요 → 합성 numpy 방향, 본학습 GPU.
5. **위험**: 개입데이터 구성이 곧 XOR-primary(1번)의 인과 재서술일 수 있음 → 부분중복. 그래도 counterfactual 측정각은 신규.

### 19. `hebbian-anti-hebbian-plasticity` — 국소 가소성 규칙으로 결합, 오결합은 decorrelate
1. **mechanism**: 공활성 쌍 강화(Hebb) + 허위 공기(co-occurrence) 반-Hebb 탈상관. gradient objective 아닌 **국소 규칙**. NT×CLS 🟢 선례와 동계(store 융합).
2. **왜 이기나**: 전역 loss의 DPI 함정 자체를 우회 — 국소 규칙엔 "additive가 더 싸다"는 전역 최적화 압력이 다르게 작용. 🟢 NT×CLS와 mechanism 친연.
3. **파괴통제**: 공활성 타이밍 shuffle → 강화 안 됨. 반-Hebb 항 ablation.
4. **측정**: numpy 국소규칙 시뮬 방향(gradient-free라 오히려 싸다).
5. **위험**: 국소규칙이 held-out **재조합**까지 일반화한다는 보장 약함(Hebb은 겪은 쌍만 강화 → coverage floor). 미겪은 조합엔 무력할 수 있음.

**이 라운드 신규 4개.**

---

## Round 6 — 성장/구조 + 새 축 탐침 → 고갈 판정

### 20. `mitosis-conjunction-cell` — A+B 켤레 전용 셀을 부모 A·B서 spawn
1. **mechanism**: `a_mitosis_train` 성장곡선 준수 — held-out joint 개선으로 밥값하는 conjunction cell을 A·B 셀서 분열 생성.
2. **왜 이기나**: from-scratch mitosis(🔴)와 달리 **성장/curriculum**(🟢 허용대역)이고 타깃이 결합-특화.
3. **파괴통제**: spawn cell ablation → joint만 붕괴(primitive 유지)면 earned.
4. **측정**: GPU(구조 성장). numpy 방향 제한적.
5. **위험**: mitosis trunk-obj서 이미 falsified 인접 → 재탕 위험 높음. 유망도 낮게.

**새 축 탐침(고갈 확인용) — 다음은 진짜 새 mechanism인가 검사:**
- *"multi-agent 협상으로 결합"* → 결국 8/10의 재서술. ❌ 신규 아님.
- *"강화학습 보상으로 결합"* → 보상=aux term=DPI 함정 재방문. ❌.
- *"retrieval-augmented 결합"* → CLS store 계열, NT×CLS 🟢가 이미 커버. ❌.
- *"양자/텐서네트워크 결합"* → TPR(12)의 물리 재포장. ❌ 신규 아님.
- *"토폴로지/persistent homology로 결합 검출"* → 측정 probe로는 9번 계열, objective 아님. △ 8/9에 흡수.

→ **연속으로 진짜 새 직교 mechanism이 안 나온다. 고갈.**

---

## 🏁 고갈 판정

**총 family: 19개** (14를 12에 반흡수, 20/새축탐침 5건은 기존에 흡수 → 순 직교 mechanism-family ≈ 19).

**직교 클러스터 6개**로 수렴:
| 클러스터 | family | 지배 아이디어 |
|---|---|---|
| A. additive-불가능 타깃/생성자 | 1,2,3,4,5 | primary에서 additive를 죽이거나 고비용화 |
| B. invertibility/정보보존 | 6,7 | bound면 복원, additive면 crosstalk |
| C. additive-대조 discriminator | 8,9,10,11 | additive를 문자 그대로 대조군 |
| D. 비가법 연산자(task와 짝 필수) | 12,13,15 | ⊗/AND/disentangle |
| E. bio/physics 동역학 | 16,17,18,19 | 위상·에너지·인과·가소성 |
| F. 구조 성장 | 20 | conjunction-cell mitosis |

**메타 결론**: 죽은 레버 전부가 클러스터 D의 "연산자 offer"거나 "aux 보상항"이었다. 살아있는 미검증 영역은 **A(additive를 primary에서 necessitate)** 와 **C(additive를 대조군으로 구성)** 다. D는 A/B와 짝지을 때만, E는 고위험 exotic, F는 재탕 위험.

---

## 🎯 가장 유망한 top-5 + 실행 분류

우선순위 근거: (i) additive를 **게임 불가**하게 대조/무력화, (ii) shuffle-붕괴가 **설계 내장**, (iii) Δ-측정이 명료.

### (a) cheap numpy probe로 **지금 방향 볼 수 있는 것** — 즉시 착수 권장
1. **`residual-lift` (8)** ⭐ 최우선. additive-frozen 잔차의 held-out lift Δ. 대조군이 공짜로 딸려오고, lift=0이면 그 자체가 **벽=능력천장의 결정적 종결 증거**. 저비용·해석 명료. 가장 먼저.
2. **`bilinear-generator-complexity-flip` (3)** ⭐ DPI 역이용의 정석. 생성자 완전통제라 numpy 회귀로 "bound가 additive를 언제 이기나" 위상도를 오늘 그린다. 자연corpus 이식성이 관문이나 방향 판정은 즉시.
3. **`polysemy-necessity` (5)** — 유일하게 **실 corpus**에서 바로 잴 수 있음(문맥 shuffle Δ). anima 4-cell corpus에 hard-polysemy 셋 추출로 저비용 착수.
4. (진단 파트너) **`synergy-pid` (9)** — 8과 짝. 8의 lift가 진짜 synergy인지 정보이론적 교차검증(objective 아닌 measurement로만).

### (b) GPU 학습 cost-gated — (a)가 방향 초록일 때만 발사
5. **`unbind-recovery-crosstalk` (6)** + `tpr-hrr-vsa-operator` (12) 결합 — N-sweep으로 additive crosstalk를 primary 오차로 노출. numpy로 crosstalk-vs-N 곡선은 미리 보되, 학습 binding-op은 GPU.
- **`xor-primary-target` (1)** — numpy로 toy 방향은 보되, held-out 커버리지로 lookup 배제하려면 규모가 필요 → GPU.
- **`adversarial-additive` (10)** — minimax 안정성 때문에 GPU. 단 능력 Δ 게이팅 필수(useless-bind 위험).

**한 줄 추천 경로**: `residual-lift`(8)를 numpy로 먼저 쏴서 **"held-out 잔차에 신호가 있는가"** 를 판정 — 있으면 3·6으로 GPU 상승, **없으면 γ 포함 재조합 벽 전체가 303M byte-LM 능력천장으로 종결**(값진 negative). 이게 고갈 이후 유일하게 남은 결정적 실험이다.

—

발산 완료. tune-to-green·self-judge 없이, 모든 후보에 shuffle-붕괴 대조를 내장했다. 죽은 레버 재탕 0건(D 클러스터는 offer-단독=재탕임을 명시하고 task-necessitate 조건을 붙임). 실제 발사는 오너 정책(fable=설계·분석만, 실행=기본경로)에 따라 여기서 멈춘다 — 착수하려면 `residual-lift` numpy probe부터 기본경로로 넘기면 된다.