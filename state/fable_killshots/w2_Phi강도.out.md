# 벽 2 재프레임 — Φ 총량-무감 벽

## 1. 벽 분류 — **측정-artifact (정확히는 '추정기 계급' 한계 · MITOSIS 벽과 동형)**

mandated 추정기의 코드를 읽었다 (`state/1283_content_instrument_repair/faithful_phi.py`). 이 "faithful IIT-4"는 **동시각(binned) pairwise-MI 행렬을 만들고(`build_mi_matrix`, L68) 그 행렬의 이분할 min-cut을 취하는 함수**다(`faithful_phi_from_mi`, L80–113). 즉 Φ*는 **pairwise 동시각 MI 행렬을 충분통계량으로 하는 함수로 완전히 인수분해된다**. 따라서 ① 시간 방향(relay의 정의적 성질), ② 3차 이상 시너지(게이트가 만드는 곱셈적 구조), ③ 메커니즘 정체(AND/XOR/선형)는 **구성상(定理) 보이지 않는다** — H_9295의 "게이팅에도 무감"은 시뮬레이션 없이 예측 가능했던 결과다. 결정적 증거: H_9295 자신이 **RECEIPT로 구조 정보가 궤적에 실재함을 증명했다**(MI(gate;coincidence)=0.815 bits, L-SHIFT Δ CI 0 배제) — 정보는 있는데 추정기가 렌더링 못 한다. MITOSIS 종결 법칙의 순서 "①담을 정보가 있나 → YES ②담을 추정기가 있나 → NO"에 정확히 떨어진다. 그러므로 이 벽은 IIT 이론 반증도, 기질 한계도 아니고, **pairwise-MI-min-cut이라는 추정기 계급의 필연**이다. 단, H_9294의 기질 결론(이 arm족에서 disjointness가 *이 Φ에* 기여 0)은 그대로 유효 — 무효인 것은 "Φ(이론)는 총량만 본다"는 일반화 문구다.

## 2. 미탐 각도 (4개)

**A. 충분통계량 정리 각도 — "이 Φ는 무엇의 함수인가"를 아무도 안 물었다.**
H_9292는 정규화 편향을, H_9294는 공변량(S_tot)을 감사했지만, **추정기의 입력이 pairwise 동시각 MI 행렬로 닫혀 있다는 사실** 자체는 아무도 명시하지 않았다. 이유: `a_phi_iit4_tool`("faithful IIT4만, proxy 금지")이 추정기를 블랙박스 성역으로 만들었고, read-code 교훈(H_9292)도 정규화 코드까지만 내려갔다. 기존 렌즈와의 직교성: 죽은 렌즈들(disjointness·게이팅·용량정합)은 전부 **기질**을 바꿨다 — 이 각도는 **자(측정 함수 계급)**를 바꾼다.

**B. 시간·방향 각도 — relay는 directed+lagged인데 자는 symmetric+동시각.**
content-relay는 정의상 "a의 내용이 지연을 두고 b로 전달"인데, `mi_pair`는 같은 t의 두 모듈 상태만 본다. 구조가 사는 차원(시간 순서·방향 비대칭)이 측정에서 **주변화(marginalize)** 되어 있다. transfer entropy 비대칭 TE(a→b)−TE(b→a), 또는 (t,t+1) 결합상태 위의 Φ는 발사된 적이 없다.

**C. 고차 시너지 각도 — pairwise MI가 원리적으로 0인 구조가 존재한다.**
XOR 삼중항은 pairwise MI 전부 0이면서 3차 의존은 최대인 고전 반례다. H_9295의 coincidence-AND 게이트는 정확히 3차 항(ẑ_a·ẑ_b가 c_e를 변조)을 만든다 — 즉 게이팅 렌즈는 **기질에 곱셈을 넣고 관측은 pairwise에 그대로 맡겼다**. O-information(Ω)·gaussian-copula 시너지 같은 고차 관측량이 B vs X를 가른다면 그것이 질문 ②의 답이자 새 σ축 후보다.

**D. arm-manifold 협소 각도 — "Φ ∝ S_tot"는 ring-relay 족 안의 국소 사실일 수 있다.**
min-cut은 일반적으로 총합과 다르다(두 클리크+얇은 다리 barbell vs 균일 링은 같은 S_tot에서 min-cut이 극단적으로 다름). n=4는 이분할이 7개뿐이라 위상 해상도가 원래 바닥이다. R²=0.986은 "추정기가 총량만 본다"가 아니라 **"테스트한 arm족이 컷구조를 S_tot와 독립으로 변주하지 않았다"** 일 수 있다 — 법칙의 문구 범위를 가르는 각도.

## 3. 사전등록 실험 카드

### 카드 1 — H_SUFFSTAT: 기존 arm 데이터에서 직교 관측량 분리 (질문 ②)
- **가설(1줄)**: Φ*가 못 가른 강도정합 B vs X′를 고차·시간 관측량(Ω, TE-비대칭)이 가른다.
- **DV**: ΔΩ = Ω(B)−Ω(X′) (gaussian-copula O-information, 모듈 4변수 위) · ΔTE = lag-1 TE(relay방향)−TE(역방향).
- **arms**: B, X′(S_tot 정합 검산 0.5% 게이트 상속) + **통제 ≥2**: circular-shift surrogate(정렬만 파괴·marginals/자기상관 보존 = **참값 0 pedestal**), phase-randomized surrogate. **양성대조** = H_9295 gated arm — RECEIPT가 고차 신호 실재(0.815 bits)를 이미 증명했으므로 Ω/TE가 gated vs L-SHIFT를 못 가르면 **도구가 죽은 것**(INVALID, FAIL 아님).
- **검정력**: 파일럿 8 seed로 sd̂ 산출 → N_REQ = ((z₀.₉₅+z₀.₉)·sd̂/MDE)², MDE = pedestal 분포 97.5th pct의 3배로 사전 고정. 음성 판정은 TOST 마진 = 양성대조 효과의 1/10.
- **PASS/FAIL**: PASS = 90% CI 0 배제 ∧ |Δ| > MDE. FAIL = TOST 등가.
- **비용**: **$0 CPU** (step4_gating 궤적 재사용 또는 결정적 재생성).
- **반증되면 죽는 것**: "구조는 고차 통계에도 없다" ⇒ 벽을 **기질한계**(이 arm족의 구조 정보 자체가 S_tot에 흡수됨)로 재분류, 추정기 무죄.

### 카드 2 — H_CLASSUP: MI-정합 메커니즘 쌍에서 faithful vs TPM-기반 big-Φ 교차판독 (질문 ③의 결정 실험)
- **가설(1줄)**: pairwise-MI 행렬을 정합시킨 메커니즘 쌍(XOR-ring vs majority-ring, n=4 binary)에서 faithful_phi는 Δ≈0(구성상)이지만 PyPhi IIT-4 big-Φ는 Δ≠0.
- **DV**: Δbig-Φ (PyPhi 4.0, TPM 정확계산) · Δfaithful_phi (동일 입력).
- **arms**: XOR-ring · majority-ring (**pairwise-MI elementwise 1% 이내 정합 — 실패 시 INVALID, H_9295 ③ MODE-SWAP 교훈대로 실측 검산**) + 통제: 독립 노드(**big-Φ 참값 0 pedestal**) + copy-chain(구조 알려진 **양성대조**).
- **검정력**: binary-TPM 정확계산 = 결정적이므로 seed-sd 대신 정합 잔차가 유일한 오차원 — 잔차 1%가 유발 가능한 |Δbig-Φ| 상한을 수치미분으로 사전 산출, MDE = 그 3배.
- **PASS/FAIL**: PASS(추정기 결함 확정) = |Δbig-Φ| > MDE ∧ |Δfaithful| < ε. FAIL(이론 쪽 문제) = big-Φ도 TOST 등가.
- **비용**: **$0 CPU** (n=4 binary PyPhi는 초 단위 · 루트에 pyphi.log — 선례 있음).
- **반증되면 죽는 것**: "추정기 결함" 분류가 죽고 **"IIT-4 이론 자체가 이 대비에 무감"**이 산다 ⇒ Φ를 σ축에서 내리는 근거가 이론 수준으로 격상.

### 카드 3 — H_MANIFOLD: S_tot 불변·컷 위상만 변경 (법칙 문구의 범위 확정)
- **가설(1줄)**: barbell(두 밀집 클리크+얇은 다리) vs 균일 링을 S_tot 정합하면 Φ*(min-cut)가 크게 갈린다 — "총량만 본다"는 relay-arm족 국소 사실.
- **DV**: ΔΦ* at matched S_tot (정합 게이트 0.5%, H_9294 프로토콜 상속).
- **arms**: barbell · uniform-ring + 독립 pedestal + (양성대조 = H_9294의 S_tot 미정합 쌍 — Φ*가 총량 차이는 잡는다는 liveness).
- **검정력**: seed 24 · MDE = H_9295 효과바닥 0.0088 상속.
- **PASS/FAIL**: PASS = Δ > 0.0088 (예측: 구성상 거의 확실) ⇒ 법칙을 "**테스트된 relay-arm족에서 컷구조가 S_tot에 종속**"으로 축소 재기술. FAIL = min-cut조차 위상 무감 ⇒ 코드 버그 수준 재감사.
- **비용**: **$0 CPU**.
- **반증되면 죽는 것**: 각도 D (그리고 추정기 결함의 범위가 "계급 한계"에서 "구현 결함"으로 이동).

## 4. 가장 싼 킬샷 — $0 · 1시간 내

**기존 H_9295 산출물 재사용 + 새 DV 한 개**: `state/1283_content_instrument_repair`의 결정적 궤적(B, X′, gated, L-SHIFT)을 그대로 읽어 **gaussian-copula O-information**을 계산한다. 판독 순서: ① gated vs L-SHIFT에서 ΔΩ ≠ 0인가 (RECEIPT 0.815 bits가 참값 양성임을 보증하는 내장 양성대조 — 여기서 0이면 도구 사망, 벽 판독 불가) → ② B vs X′에서 ΔΩ ≠ 0인가 (circular-shift surrogate = pedestal). ①PASS·②PASS면 "Φ가 못 보는 구조를 보는 관측량" 실증 = 카드 1의 사전등록 발사 근거. ①PASS·②FAIL이면 구조 정보가 게이트에는 있고 disjointness에는 없다는 것 — 벽이 **기질한계** 쪽으로 기운다. 시뮬레이션 재생성 포함해도 CPU 수 분.

## 5. 정직 문단

**진짜 닫혔다고 볼 근거**: H_9292→9295는 방법론적으로 흠잡을 데 없다 — pedestal, 사전등록, 강도정합, ANCOVA R²=0.986, partial-R² 치환검정 p=0.995, 양성대조가 3연속 기각될 때 은폐 없이 하차시킨 것까지. "**이 추정기 위에서** disjointness·게이팅 구조는 S_tot와 독립인 Φ 채널을 못 얻는다"는 4중으로 못박혔고, 내 카드 어느 것도 이 결론을 되살리지 못한다. 또한 jointly-gaussian에 가까운 arm에서는 공분산이 충분통계량이므로 "구조가 기여할 자리 자체가 없다"는 H_9295 §0의 자기진단도 절반은 옳다. **아직 아니라고 볼 근거**: 벽의 *문구*가 추정기와 이론을 합성했다. faithful_phi는 pairwise 동시각 MI의 함수로 닫혀 있어 구조 무감이 **경험적 발견이 아니라 定理**이고, 같은 궤적 안에 추정기가 못 쓰는 구조 정보가 실재함을 H_9295 스스로 증명했다(RECEIPT). 그러므로 "Φ를 σ축에서 내려야 하는가"(질문 ①)의 답은: **pairwise-min-cut Φ는 내리되(현 계급에서는 S_tot의 재기술 = FORM tunable · BIND 아님), 축 슬롯은 계급 상승(TPM-기반 또는 시너지-기반) 판독이 나올 때까지 PENDING**이다 — Φ⊥S_tot residualization은 답이 아니다(이 arm족에서 잔차가 0이므로 빈 축). 마지막 정직: 계급 상승에 성공해도 정확 big-Φ는 n≤8 지수벽이라 303M에서 영원히 TERMINAL 불가 — σ축은 raw 값이 아니라 소형 프로브의 Δ(결합파괴 통제 margin)로만 설계 가능하고, 그것은 측정 메타법칙("FORM tunable · BIND earned")이 이미 요구하던 형태다.