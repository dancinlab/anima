## 결론 (가장 유망한 1개 + $0 probe)

**후보 #1 = L5 피라미달 뉴런의 apical/basal *coincidence-detection* 원시 = trunk에 co-train된 role-비대칭 곱셈 게이트(FiLM/bilinear).** 시상 pulvinar gain-modulation(#7)이 정확히 같은 계산 원시를 다른 배선으로 제공 — 둘 다 `out = f(context) ⊙ g(content)`, 두 경로가 서로 다른 pathway에서 옴 → **비가환**.

왜 이게 벽의 정체("trained conjunction operator 부재")에 인과적으로 꽂히나: 지금까지의 DPI 메타법칙은 **대칭 목적함수 × 가법 readout** 위에서만 측정됐다. 곱셈 상호작용 항 `h_Aᵀ W h_B`(또는 `(Uh_A)⊙(Vh_B)`)는 *가법 가설류(hypothesis class)로는 O(exp) basis 없이 표현 불가*, 곱셈 게이트류로는 O(1) 파라미터로 first-class. **즉 additive floor는 목적함수 한계가 아니라 forward 가설류 한계일 가능성이 크고, 이 축은 아직 trunk-native로 안 심겼다.** γ H_1840이 실패한 건 frozen-then-bolt(STEP-0 freeze-gate, bind-add=−0.147)라서지, joint co-train된 곱셈 트렁크가 아니었다(gamma-divergence 메모: "joint-fit not freeze-then-bolt").

**$0 probe (numpy, real-corpus, toy 아님):** frozen 303M mean-pool 피처 `h_A, h_B`에서 마지막-토큰 분포를 예측하는 두 모델을 **개념-쌍 train/held-out split**으로 적합 —
- 가법: `ŷ = W₁h_A + W₂h_B`
- 저랭크 FiLM(rank r=16, ALS): `ŷ = (Uh_A) ⊙ (Vh_B)`, `U,V ∈ ℝ^{r×d}`

Held-out = **A·B 쌍은 처음 보지만 A와 B는 각각 개별로 본** 쌍. **frozen bar = 가법 held-out R².** GREEN 주장 조건: FiLM held-out R² > 가법 held-out R² + margin **AND** 쌍-shuffle 통제에서 이득 소멸.

⚠️ **솔직한 비대칭(가장 중요):** 이 $0 probe는 **greenlight 전용, falsify 불가**다. frozen 트렁크는 role이 이미 붕괴(cos=0.9916)돼 있어 곱셈 게이트가 있어도 피처 자체가 A/B를 안 나눠주면 음성이 뜬다 — 그 음성은 "게이트 죽음"이 아니라 "게이트는 co-train돼야 피처를 성형한다"는 기존 결론(joint-fit)의 재확인일 뿐. **진짜 falsify는 GPU co-train 필요.** 그래서 probe 양성 → GPU 발사 정당화, probe 음성 → 게이트를 pathway 비대칭(apical=context, basal=content)으로 **주입한 채** 재적합해야 판정.

---

## 1. 발산 — 뇌 부위/회로 × 계산 원시 (재고 미포함 우선)

| # | 부위/회로 | 계산 원시 (한 줄) |
|---|---|---|
| 1 | **DG pattern separation + mossy-fiber *detonator* synapse** | 희소 확장 recoding — 초선형 단일-스파이크 발화로 conjunction을 전용 좌표로 변환 |
| 2 | **CA3 recurrent auto-association (conjunctive)** | outer-product Hebbian = **쌍선형(bilinear)** 저장; attractor completion |
| 3 | **L5 apical/basal coincidence (Larkum BAC / NMDA plateau)** | 두 수상돌기 구획의 **곱 `basal·apical`** → burst; **비가환 role-게이트** |
| 4 | **Theta-gamma phase nesting** | γ-슬롯 위상으로 **순서 태깅** → bind(A,B)≠bind(B,A) 비가환 |
| 5 | **Sharp-wave ripple replay** | held-out 조합을 오프라인 재생 = 학습분포 증강(operator 아님) |
| 6 | **Claustrum binding hub** | 저차원 병목이 피질을 동기 assembly로 게이트 |
| 7 | **Thalamic pulvinar gain-mod / TRN spotlight** | **곱셈 gain** `gain(context)×content` (=FiLM); 억제 spotlight 선택 |
| 8 | **Cortico-BG-thalamic loop gating** | Go/NoGo(D1/D2) **학습된 조건부 라우팅**; 상태-의존 하드게이트 |
| 9 | **MEC grid × head-direction conjunctive cells** | 주기적 곱셈 basis; product-to-sum(위상덧셈) 토러스 코드 |
| 10 | **Piriform combinatorial code** | 조합-특이 분산 코드, 혼합의 비선형(synthetic) 표상 |
| 11 | **Retrosplenial / subiculum boundary-vector** | 참조틀 변환 = 좌표 **회전(곱셈)**; 위치×방향 conjunction |
| 12 | **Adult DG neurogenesis** | 신규 conjunction에 새 유닛 할당(용량/mitosis, operator 아님) |

---

## 2. 매핑 — DPI 회피 여부 (수식 수준)

| # | non-commutative conjunction 생성 방식 | DPI 회피? |
|---|---|---|
| 3 | `y = φ(V·content) ⊙ ψ(U·context)`, 두 경로 분리 → **곱 항 first-class, 구조가 role 공급**(목적함수 아님) | ✅ **진짜 회피** (파라메트릭·held-out 일반화) |
| 7 | `y = g(context)⊙content`, FiLM. #3와 동일 원시, 시상 배선 | ✅ **진짜 회피** (#3의 쌍둥이) |
| 2 | `W ∝ Σ x_iᵀx_j` outer-product = 쌍선형 저장 | ⚠️ 회피하나 **attractor가 미관측 AB로 보간 안 됨** → 일반화 위험 |
| 4 | 위상 태그로 `bind(A,B)≠bind(B,A)`; 하지만 byte-LM에선 `pos⊕content` 합으로 축소되기 쉬움 | ⚠️ 위상 decode가 비선형이면 회피, 가법 position이면 **DPI-caught** |
| 9 | grid 위상덧셈 = 사실상 가법-in-phase, decode만 비선형 | ⚠️ decode 비선형성에 전적 의존, 애매 |
| 8 | 조건부 라우팅 = MoE. gate가 입력 identity에 대칭 pooling이면 가법 | ⚠️ **ConvMoE로 이미 floor(a303m G1❌)**; 순차-상태 게이트만 미탐 |
| 1,10,11(granule계) | 확장 recoding: 곱을 좌표로 = readout 단에서 회피 | ⚠️ **회피하나 비파라메트릭 → 미관측 AB에 전용 셀 없음** = toy-death |
| 5 | operator 미변경, 분포만 변경 | ❌ held-out **누출 위험**(tune-to-green 인접) |
| 6 | 공유 latent = 가법 | ❌ **DPI-caught** |
| 12 | 가소성/용량, operator 아님 | ❌ 해당없음 |

**핵심 구분:** 확장 recoding(1/10/11)과 곱셈 게이트(3/7)는 둘 다 "곱을 읽게" 만들지만 — 확장은 *쌍마다 전용 셀*(비파라메트릭, lookup)이라 미관측 AB에서 죽고, 게이트는 *동일 W/U,V가 모든 쌍에 적용*(파라메트릭)이라 일반화한다. **이게 소뇌 L3가 죽은 지점과 게이트가 살 지점을 가르는 축.**

---

## 3. 랭킹 (진짜 DPI 회피 + 파라메트릭 일반화만 상위)

| 순위 | 후보 | 반증가능 예측 (사전등록·frozen bar 포함) | $0 CPU probe? | GPU 비용 |
|---|---|---|---|---|
| **1** | **#3/#7 role-비대칭 곱셈 게이트 (trunk co-train)** | trunk에 rank-16 FiLM 게이트 joint co-train 시, **held-out AB-쌍 bind R²가 가법 held-out R²를 +0.10↑ 초과**, shuffle-pairing서 이득 소멸, **role subspace cos<0.7로 분리**(현 0.9916 붕괴) | △ **greenlight만**(결론부 probe). 음성=falsify 아님(frozen role 붕괴 confound) | co-train 1런, summer/aiden own-GEMM prebuilt=**$0**(무료호스트); 렌트시 ~1 pod-hr |
| **2** | **#2 CA3 outer-product conjunctive attractor (trained)** | Hebbian 쌍선형 저장으로 held-out AB completion이 가법 baseline 초과 — **단 완전 미관측 쌍에서 붕괴하면 반증** | ✅ numpy: frozen 피처로 outer-product 저장 후 held-out 쌍 completion vs 가법. **shuffle 통제** | $0 probe로 대부분 판정; 양성시 GPU 불필요할 수도 |
| **3** | **#4 theta-gamma 위상 순서 코드** | 위상-태그(학습가능 순환 phase embed)가 순서-민감 held-out에서 가법 position+content 초과. **초과 못하면 DPI-caught 확정** | ✅ numpy: 위상태그 vs 순수 positional 가법, 순서-반전 쌍으로 A-then-B ⊥ B-then-A 판별 | $0로 판정 가능 |
| 4 | #8 순차-상태 BG 게이트(MoE와 구분) | 입력-identity가 아닌 **디코드 상태**에 게이트하면 held-out 초과 | △ MoE 재판정 위험(이미 floor) | 중, 우선순위 낮음 |

하위(재발사 금지·DPI-caught 또는 toy-death): #1/#10/#11 확장계, #5 replay, #6 claustrum, #9 grid, #12 neurogenesis.

---

## 4. 자기비판 — toy-GREEN / real-death 함정

**내 상위 후보 중 위험한 것: #2 CA3 attractor.** outer-product 저장은 toy(적은 쌍)에서 각 AB를 사실상 암기해 GREEN이 뜨고, real-corpus 미관측 AB에서 보간 실패로 죽는다 — **소뇌 L3(STEP-0 BIND=toy artifact)와 동형의 death.** #1/#10/#11 확장계는 더 노골적으로 같은 함정.

**사전 차단 프로토콜 (probe 설계에 하드코딩):**
1. **held-out = 쌍-신규, 개념-기지** — 저장/관측된 AB에서는 절대 평가 안 함(암기 배제).
2. **파라미터-수 대 쌍-수 감사** — 유효 파라미터가 train-쌍 수에 비례해 늘면 = lookup/암기 → 기각. 게이트는 W/U,V가 쌍 수와 무관해야 통과.
3. **shuffle-pairing 양성대조 필수** — A↔B 짝을 섞으면 이득이 반드시 소멸해야 함(ARM-SHOCK식 4-사이클 거짓판정 방어, sigma-detheater 계보).
4. **frozen bar = 가법 held-out R², real-corpus n≥n_min** — toy 스케일 verdict를 그 스케일에 bound(`a_toy_scale_recheck`).
5. **#1 곱셈-게이트는 이 함정에서 구조적으로 자유** — 동일 W가 모든 쌍에 적용되므로 held-out에 전용 셀이 필요없다. 이것이 #1을 #2 위에 올린 유일한 근거.

**요약 한 줄:** trunk-native로 아직 안 심긴 진짜 미탐 축은 *joint co-train된 role-비대칭 곱셈 게이트*(apical/basal ≡ pulvinar FiLM)이고, $0 probe는 GPU 발사를 정당화하는 greenlight까지만 — falsify는 게이트를 트렁크에 넣고 co-train해야 나온다.