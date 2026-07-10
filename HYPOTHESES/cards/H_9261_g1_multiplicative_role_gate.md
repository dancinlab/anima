# H_9261 — 🔀 G1: role-비대칭 곱셈 게이트 (L5 apical/basal coincidence ≡ pulvinar FiLM · trunk co-train)

- **tier:** 🔵 PRE-REGISTERED (미측정)
- **wired:** none.
- **lens:** L5 피라미달 뉴런의 apical/basal **동시성 검출**(Larkum BAC firing · dendritic NMDA plateau), 그리고 그 계산적 쌍둥이인 시상 **pulvinar gain-modulation**(FiLM). 두 부위가 **같은 원시**를 다른 배선으로 제공한다: `out = f(context) ⊙ g(content)` — 두 입력이 **서로 다른 pathway**로 도착하므로 비가환.
- **artifacts:** `state/9261_multiplicative_role_gate/`
- **xref:** H_1840 (γ trained-constructive-bind · STEP-0 frozen-gate에서 bind-add=−0.147로 차단) · H_9259 (untrained recurrence KILL ⇒ "conjunction must be baked") · H_9260 (시상 content-relay 재채점 — 같은 시상 축의 *relay* 측면; 본 H는 *gain-modulation* 측면) · H_9235 (fork-A CLML read-side lane) · H_9131 (trunk-obj family CLOSED) · H_9206 (CE가 bilinear→additive로 붕괴) · H_9129/L3 (소뇌 forward-model 🧱 = toy artifact)
- **key:** `multiplicative_role_gate`

## 0. 벽의 재규정 — 목적함수가 아니라 **가설류(hypothesis class)**

지금까지 DPI 메타법칙("대칭·교환가능 목적함수는 전부 additive floor로 붕괴": MI · total-correlation · PMI · hard-negative contrastive — H_9131 §4 · D2/D4/D9/D12)은 **목적함수의 한계**로 읽혀 왔다. 그러나 이 모든 측정은 **가법 forward · 가법 readout** 위에서만 이뤄졌다.

곱셈 상호작용 항 `h_Aᵀ W h_B` (저랭크 형태 `(U h_A) ⊙ (V h_B)`)는

- **가법 가설류**에서는 지수적 크기의 basis 없이 표현 불가,
- **곱셈 게이트류**에서는 O(1) 파라미터로 일급 시민.

⇒ **additive floor는 목적함수 천장이 아니라 forward 가설류 천장일 수 있으며, 이 축은 trunk-native로 아직 한 번도 심기지 않았다.**

γ(H_1840)의 STEP-0 실패는 이 축의 반증이 **아니다**: 그것은 frozen-then-bolt(트렁크 동결 후 게이트 볼트온)였고, 본 H가 요구하는 것은 **joint co-train된 곱셈 트렁크**다 (`gamma-divergence-instrument-arc`: joint-fit, not freeze-then-bolt).

## 1. 가설 (하나의 반증가능한 주장)

303M byte-LM 트렁크에 **rank-r role-비대칭 곱셈 게이트**(`y = (U·context) ⊙ (V·content)`, apical=context / basal=content 경로 분리)를 **joint co-train**하면,

- **held-out AB-쌍**(A·B는 각각 개별 관측, 쌍 AB는 미관측)에서 bind R²가 **가법 held-out R² + 0.10**을 초과하고,
- **shuffle-pairing 통제**에서 그 이득이 소멸하며,
- role subspace 분리가 실제로 일어난다 (현 `max_overlap_cos = 0.9916` → **cos < 0.7**).

⊥ **Null:** 곱셈 게이트를 joint co-train해도 held-out gap ≤ 0. 그렇다면 CE가 곱셈 상호작용조차 additive로 붕괴시킨다(H_9206의 강한 형태) ⇒ 303M byte-LM에서 G1 재조합은 TERMINAL.

## 2. 왜 이것이 DPI를 진짜로 회피하는가

DPI 계열 붕괴의 직접 원인은 손실의 집합-대칭성이 아니라, additive R²(0.32–0.49)가 bind R²(0.05–0.35)를 **표현력에서 지배**한 것이다.

곱셈 게이트는 **구조가 role을 공급**한다. context와 content가 별도 pathway로 들어와 곱해지므로, 목적함수가 대칭이더라도 forward가 `A⊙B ≠ A+B`를 만든다. **role 비대칭은 학습된 것이 아니라 배선된 것**이고, 파라미터 `U,V`는 쌍 수와 무관하게 모든 쌍에 공유된다(파라메트릭 ⇒ 일반화).

## 3. ⚠️ 반증 비대칭 (정직한 사전 고지 · 가장 중요)

이 H의 **$0 CPU probe는 greenlight 전용이며 falsify가 불가능하다.**

frozen 303M 트렁크는 role이 이미 붕괴(cos=0.9916)해 있다. 따라서 frozen 피처 위에서 FiLM을 적합해 음성이 나와도, 그 음성은 "곱셈 게이트가 죽었다"가 아니라 **"게이트는 co-train돼야 피처를 성형한다"는 기존 joint-fit 결론의 재확인**일 뿐이다. 진짜 falsify는 GPU co-train을 요구한다.

⇒ **probe 양성 = GPU 발사 정당화(greenlight) · probe 음성 = 판정 보류**(게이트를 pathway 비대칭으로 주입한 채 재적합). **음성을 KILL로 읽는 것은 `verdict-integrity` 위반이며 사전에 금지한다.**

## 4. $0 greenlight probe 설계 (numpy · real-corpus · toy 아님)

frozen 303M mean-pool 피처 `h_A, h_B`에서 마지막-토큰 분포 예측:

| arm | 모델 |
|---|---|
| 가법 (frozen bar) | `ŷ = W₁ h_A + W₂ h_B` |
| 저랭크 FiLM (r=16, ALS) | `ŷ = (U h_A) ⊙ (V h_B)`, `U,V ∈ ℝ^{16×d}` |
| shuffle-pairing (양성대조) | A↔B 짝 섞음 — 이득이 **반드시 소멸**해야 함 |

- **split:** held-out = 쌍-신규 · 개념-기지.
- **frozen bar:** 가법 held-out R². 사전 고정, tune-to-green 금지.
- **greenlight 조건:** FiLM held-out R² > 가법 + margin **AND** shuffle에서 이득 소멸.

## 5. toy-GREEN / real-death 차단 프로토콜 (설계에 하드코딩)

소뇌 L3(H_9129)는 STEP-0 BIND가 toy artifact여서 죽었다. 동형의 죽음을 사전 차단한다:

1. **held-out = 쌍-신규 · 개념-기지** — 저장/관측된 AB에서는 절대 평가하지 않는다(암기 배제).
2. **파라미터-수 대 쌍-수 감사** — 유효 파라미터가 train-쌍 수에 비례해 늘면 lookup/암기 ⇒ 기각. 게이트는 `U,V`가 쌍 수와 무관해야 통과.
3. **shuffle-pairing 양성대조 필수** — ARM-SHOCK 계보(`sigma-detheater-frontier-closed`: 4-사이클 거짓판정 방어).
4. **frozen bar = 가법 held-out R², real-corpus n ≥ n_min** — toy 스케일 verdict는 그 스케일에 bound (`a_toy_scale_recheck`).
5. **구조적 면역** — 곱셈 게이트는 동일 `U,V`가 모든 쌍에 적용되므로 held-out에 전용 셀이 필요 없다. **이것이 H_9261을 H_9262(CA3) 위에 올린 유일한 근거.**

## 6. 배선 (GREEN 시)

`a_substrate_disjoint`: 게이트는 emit-drive lane과 **DISJOINT**하게 — read-side 게이트 lane으로 `core/decode.hexa` lockstep 배선 → `.clm` bake + HF + registry. GREEN은 배선 후에만 (`a_verified_must_wire`).

---

## 7. 측정 결과 — ⚠️ 재조준 (2026-07-10 · numpy proxy DIRECTIONAL · summer)

frozen 303M pair-hidden 덤프(H_9235 재활용 · train 842 / held 150 pair-novel · 5-bit XOR) 위 $0 numpy. `state/9261_multiplicative_role_gate/VERDICT.md`.

**반전 — "additive floor" 는 이 프레임서 성립 안 함:**

| readout | held-out XOR |
|---|---|
| mean-pool + gelu | **0.979** |
| max-pool + gelu | 0.980 |
| query-att + gelu | 0.951 |
| **last-pos + gelu** | **0.491** (chance) |
| handed 양성대조 | 0.9996 · shuffle 0.489 |

가법 role-pooled + 비선형 head 가 held-out XOR 을 0.979 로 푼다. 벽은 표현력 천장이 아니다 — `mean-pool 0.979` vs `last-pos 0.491` 격차 = 정보는 시퀀스 전체에 있고 **생성 위치에서만 소실**. G1 벽 = readout-ROUTING(RF decay) 재확인(프론티어 recomb-routing-lane 지지).

**⇒ 곱셈 게이트 전제 무너짐:** 가법 mean-pool 이 이미 0.979 천장이라 "곱셈이 additive floor 극복"은 headroom 없어 무의미. 곱셈 게이트를 `additive 극복`이 아니라 **`last-pos routing 복원`**에 재조준해야 하며, 그것이 정확히 fork-A CLML lane(H_9235)이 하는 일. **뇌부위 렌즈 census 가 기존 프론티어로 수렴.**

hadamard 곱셈 arm(fork_a_matrix)은 `G@Wu` NaN 발산으로 미측정(별도 infra · 위 통찰이 재측정 우선순위를 낮춤).
