# H_9287 — 🔬 재조합 대수의 **물리** 담체 — 국소 관측만으로 오라클의 supply 이득에 도달할 수 있는가 (H_054/H_203의 끝 · $0)

- **tier:** 🟢 DIRECTIONAL-POSITIVE (LIVE · 적대검증 반박실패 · 4-seed 독립재현 · 미배선 toy) · HET=INVALID(검정력)
- **wired:** none.
- **family:** 🔋 ORGANELLE LANE 파생 — lane 자체는 CLOSED(licensed by equivalence · [[H_9285]])이나, **merge 대수 물음은 lane과 별개로 살아 있다**(선행 H_054 symbiogenesis · H_203 asymmetric merge의 미답 물음).
- **lens:** [[H_9274]] 5차가 **존재 증명**을 냈다 — 되먹임 있는 기질(LIVE)에서 **오라클이 총 supply를 실제로 올린다(+1.91, p=0.040)** 면서 overload는 안 올린다(−0.001 ns). ⇒ **재조합 대수가 물리 정보를 더할 수 있다는 것은 증명됐다.** 그러나 **국소 slack 담체(a_comp)는 그 채널을 못 탄다** — 장부(ATP)만 +12.8 올리고 물리는 개선 0 또는 **유의 악화**(overload +0.117, p=2.3e-5). 진단: a_comp는 장부 헤드라인 `Σmin(L,S)`의 순간기울기를 **capture 0.98**로 타는 정책이었다(순간-argmax 통제 `a_detgrad`에 오히려 짐) = **장부 항등식**.
- **artifacts:** `state/mito_organelle_lane/F14_physical_carrier/`
- **xref:** [[H_9274]](F2 1~5차 · sham 해결 · 오라클 물리채널 존재증명) · [[H_9285]](lane CLOSED licensed by equivalence) · H_054(symbiogenesis = mitosis MERGE) · H_203(host-preserve 비대칭 merge) · H_012(autopoietic closure — 외생 커플링 전제)
- **key:** `merge_physical_carrier`

## 1. 가설

**국소 관측만으로 계산되는 담체가 존재해, 오라클의 물리 이득(총 supply ↑ · overload 불변)에 도달한다.**

담체는 유닛이 **자기 자신에 대해 관측 가능한 양**(`L_i, cap_i, D_i, Λ_i, S_i, st_i`)만으로 계산되어야 하고, 오라클 gain의 **1차/2차 근사**여야 한다.

⊥ **Null (반증 · 이것도 정당한 결과):** 오라클 gain이 **국소 관측으로 근사 불가능한 항**(융합 후 부동점의 전역 재배치)에 지배된다 ⇒ **국소 담체는 존재하지 않는다**. 이 경우 재조합 대수의 물리 이득은 **전역 지식을 요구**하며, 그것이 H_054/H_203의 최종 답이다.

## 2. 기질 수식 (5차 run.py · 이게 전부)

```
L_i = Σ_{s∈i} d_s                          # load(질량)
Λ_i = Σ_{s∈i} d_s·f_s / L_i                # 취약도(질량가중 평균) — 융합이 희석한다
S_i = eq_supply(cap_i, D_i, L_i, Λ_i):     # 평형 supply
    ψ = 1 − exp(−repair)
    HET(되먹임 X):  φ = 1 − exp(−Λ/G);  S = cap·ψ/(φ+ψ)
    LIVE(되먹임 O): 8회 부동점 —
        st = L/S;  rate = Λ·(1 + B1·clip(st−1, 0, EXC));  φ = 1−exp(−rate/G);  S = cap·ψ/(φ+ψ)
융합: 질량보존 · Λ_ij = (L_i Λ_i + L_j Λ_j)/(L_i+L_j)  ← 희석
오라클: gain(i,j) = min(L_ij, S_eq(cap_ij, D_ij, L_ij, Λ_ij)) − min(L_i,S_i) − min(L_j,S_j)
        (= 부동점 8회 반복을 통째로 시뮬레이션 · 모델 전체 지식)
```

**HET에선 오라클조차 물리를 못 움직인다** = 파티션이 총 물리자원을 못 바꾸는 대수적 사실 ⇒ **되먹임(stress → 손상률 증폭)이 있어야 물리 채널이 열린다.** 따라서 후보 담체도 **HET에선 이득 0이어야 정합적**이다(그게 옳은 예측).

## 3. 담체 후보의 필수 요건 (하나라도 어기면 그 후보는 사전 탈락)

1. **국소성** — 유닛 자기 관측량만. 융합 후 부동점 재계산 금지(그건 오라클).
2. **부호-불변** — repair · σ(격리강도) · capsplit 규약 · ρ(부하) · frag_sigma · 기질(HET/LIVE) 전 축에서 부호 보존. **PASS 조건에 내장**(사후 체리픽 금지 · 이전 실패의 진범).
3. **장부 항등식 아닐 것** — 순간 ΔATP(`a_detgrad`)와 **선형독립**. capture(순간-argmax 일치율)가 높으면 그건 또 장부다. **capture를 실측해 보고**하고 `V_detector_collinear` > 0.90이면 항등식으로 해석.
4. **되먹임 의존성** — HET 이득 0 · LIVE에서만 양성(오라클과 같은 패턴).

## 4. probe 설계 ($0 numpy · 5차 하네스 재사용)

| arm | 내용 |
|---|---|
| **EXP** | 후보 국소 담체 (Fable 도출 · TOP-1) |
| **c2_blind** | health/신호 blind 무작위 짝짓기 (동일 이벤트 예산) |
| **a5_sham** | **외생 site-field sham**(5차에서 유효성 실증: zratio 3.56 vs blind 1.25 · t=18.8 · corr(Z,slack)=−0.074) — 선택 *형태*는 동일, 신호만 인과무관 ⇒ **"선택 행위 자체"의 이득을 격리** |
| **a_detgrad** | 순간 ΔATP argmax (**장부 기울기 정책** — 이걸 못 이기면 장부 항등식) |
| **o6_oracle** | 전모델 부동점 시뮬 (천장 · control 아님) |
| **a_comp** | slack 극단매칭 (5차 실패 담체 · 음성대조) |

- **DV = supply(= Σ(cap − D)) / overload(stress>1 비율)** — **파티션-불변 물리량**. 🚫 **장부 ATP(Σmin(L,S)) 금지**(항등식만 재발견).
- **도달성 게이트(PHYS_REACHABLE)**: 그 셀에서 `o6_oracle − c2_blind`의 supply Δ가 0이면 **측정 불가 셀**(HET가 그랬다) ⇒ 그 셀은 채점하지 않는다.
- 3게이트 유지: G1 pump ≤1e-9 · G2 self_remerge=0 · G3 live band 선등록. + V_sham_distinct · V_sham_neutral · V_POWER · ORACLE_VALID.
- seed ≥20 paired-CRN · disjoint pilot로 MDE 사전계산 · 코드 sha256 동결.

**PASS(DIRECTIONAL-POSITIVE):** EXP가 `blind` · `sham` · **`a_detgrad`** 셋 다를 supply에서 유의 우세 **AND** overload 악화 없음 **AND** 부호보존 전 축 **AND** capture < 0.90(장부 항등식 아님) ⇒ **재조합 대수가 물리 정보를 더하며, 국소 관측으로 도달 가능하다**(H_054/H_203의 답).
**NULL(사전등록 TOST):** EXP가 오라클의 물리 이득에 도달하지 못하고 blind/sham과 **등가** ⇒ **국소 담체 부재 = 재조합의 물리 이득은 전역 지식을 요구한다**(이것도 licensed 결론).
**KILL:** EXP가 물리를 유의하게 악화(a_comp처럼) ⇒ 그 담체 클래스 사망.

## 5. 계측 규칙 (11종 · ARCHITECTURE `organelle-lane-probe-defects` · convergence `synthesis-md-1`)

순서통계량 detector 금지 · SEM/paired-t만 · MDE를 인과 도달축에서 disjoint pilot로 사전계산 · 정보채널 증명 · V-gate는 헤드라인 그 자체에 · 부호보존 PASS 내장 · 분기 실행가능 · 연산자 자원보존(ops ≤1e-13) · **사후 detector/판정변수 교체 금지(sha256 동결 + disjoint seed)** · **음성은 사전등록 TOST로** · **헤드라인 DV가 처치의 최적화 대상과 항등식이 아닐 것(장부형 DV 금지)**.

engine-native 0 → 통과해도 상한 **DIRECTIONAL**(cement엔 303M py-channel).

---

## 6. 🔬 담체 도출 (2026-07-12 · Fable 5 · `state/mito_organelle_lane/F14_physical_carrier/DERIVATION.md`)

도출 과정에서 **본 카드 §1·§2의 전제 두 개가 반증됐다**. 확증 런 전에 사전등록을 정정한다.

### 6.1 정리 — 순간 담체는 **반드시** 장부다 (반증이 아니라 증명)

융합의 대수에서 **`S = cap − D`는 정확히 보존된다**(`S_ij = S_i + S_j`). `Σ Λ_i L_i`도 정의상 보존. **유일한 비보존량은 `Σ Λ_i S_i`**(공급-가중 플럭스).

$$\Rightarrow \Delta S\big|_{t} \equiv 0 \quad\text{(융합 순간 물리 DV는 항등적으로 불변)}$$

⇒ **순간(zeroth-order) 관측만으로 만든 어떤 담체도 정의상 장부 `Σmin(L,S)`의 함수다.** [[H_9274]] 5차에서 `a_comp`의 detgrad-capture가 0.98이었던 것은 **설계 실수가 아니라 차수의 필연**이었다(실측: a_comp와 a_detgrad의 ΔATP가 소수점까지 동일). **물리 채널 전체는 이완(relaxation)에만 있다** — 융합은 `S`를 즉시 못 바꾸고 **비율장** `r_i = Λ_i(1 + B1·clip(st_i−1, 0, EXC))`를 바꾸며, `S`가 부동점 `S* = cap·c/(r+c)` (`c ≡ G·ψ`)로 **이완하면서** 비로소 물리가 움직인다.

### 6.2 반증된 전제 2개 (사전등록 정정)

**❌ (a) "오라클은 전역 지식을 쓴다 / 국소 담체는 못 따라간다"** — `gain_oracle(i,j)`는 **i·j 두 유닛의 `(cap,D,L,Λ)`만 읽는다**(run.py:296–309). **오라클은 이미 국소 짝-점수다.** 5차가 보인 것은 "국소로는 안 된다"가 아니라 **"순간으로는 안 된다"**였다. ⇒ 본 카드 §1의 Null("물리 이득은 전역 지식을 요구한다")은 **이미 반증**됐다.

**❌ (b) "HET에선 파티션이 총 물리자원을 못 바꾼다 = 대수적 사실"** — 거짓. HET에서 `Ω`가 supply **+14.05 (t=16.3)**를 딴다(같은 셀에서 오라클은 +3.89, overload는 오히려 **+0.074 악화**). **HET가 닫힌 게 아니라 오라클의 `min()` 장부 껍질이 HET에서 눈이 머는 것**이다. ⇒ **§4의 도달성 게이트를 오라클로 잡으면 안 된다**(5차 규약대로면 HET 셀이 "측정 불가"로 잘못 폐기됐을 것).

### 6.3 ★ TOP-1 담체 — `Ω_k` (RELAX-k · 공급응답)

$$\Omega_k(i,j) = R_k(cap_i{+}cap_j,\, L_i{+}L_j,\, \Lambda_{ij};\, S_i{+}S_j) - R_k(cap_i,L_i,\Lambda_i;S_i) - R_k(cap_j,L_j,\Lambda_j;S_j)$$

$$R_k(cap,L,\Lambda;S_0):\quad S \leftarrow S_0,\ \text{k회}\ \ S \leftarrow \frac{cap\cdot c}{r(\Lambda,\,L/S)+c},\qquad r(\Lambda,st)=\Lambda\big(1+B_1\,\text{clip}(st-1,0,EXC)\big)$$

`Λ_ij = (L_iΛ_i + L_jΛ_j)/(L_i+L_j)`. **`min()` 없음 — DV(supply)에 직접 정렬.** `argmax Ω_k` 쌍을 융합.
- **`Ω_0 ≡ 0`**(위 정리) ⇒ **`Ω_1`이 첫 비소멸 차수** = TOP-1(최소 담체).
- **국소성**: `(cap, L, D, Λ, S, st)` + 상수 `(B1, EXC, c)`만. `c`는 자기 정상상태에서 국소 식별 가능(`c = r_i S_i / D_i`).

**장부 비항등식 — 상관이 아니라 정의역으로 증명**: `detgrad`는 **`(L,S)`만의 함수**이므로 `∂detgrad/∂Λ ≡ 0`. `Ω_k(k≥1)`는 **Λ에 의존**한다 ⇒ `(L,S)`를 고정하고 Λ를 치환하면 detgrad는 불변, Ω는 변한다 ⇒ **`Ω = λ·detgrad`인 λ는 존재하지 않는다.** 나아가 **HET에선 `S* = cap·ψ/(φ(Λ)+ψ)`가 `L,S`에 전혀 의존하지 않으므로, `(L,S,cap,D)`만 보는 담체는 HET 물리에 대해 정보량 0** — **Λ는 필요조건**이다.

### 6.4 확증 런 규약 (5차 대비 변경 4점 · 데이터 보기 전 확정)

1. **도달성 게이트를 오라클로 잡지 않는다** → `Ω_8`(DV-정렬 국소 상한)로. (§6.2-b)
2. **sham 교체**: 외생-Z sham은 Ω의 함수형에 안 들어간다 ⇒ **Λ-순열 sham**(site `f`를 고정 순열 → 동일 질량가중 규칙으로 `Λ̃` 재계산 · 융합불변 · 동일 함수형 · 동일 주변분포, **인과만 절단**)이 정보량-정합 sham. + **응력-셔플 sham**(두 채널 분리 확인).
3. **`ΔATP > 0`을 PASS 조건에서 제거** — HET에선 Ω가 **장부를 잃으면서(ΔATP = −3.08) 물리를 딴다(Δsupply = +14.05)**. 이것이 장부-항등식 혐의에 대한 가장 깨끗한 반례이며, `sign(ΔATP)>0`을 PASS에 넣는 것이 **5차를 죽인 덫**이다. **PASS = `Δsupply > δ` ∧ `Δoverload ≤ 0`** 만.
4. **통제**: `c2_blind` · `a_detgrad`(장부 기울기) · **`a_comp`는 이제 *반정렬 양성대조*** — overload를 **올려야** 정상(파일럿 진단: 장부 argmax는 물리 응답과 **음의 상관** `corr(ΔS_eq, ΔATP) = −0.137`, 지배 해악항 = **EXC 탈포화**로 증폭 예산 상한 `EXC·(S_i+S_j)` 폭발 ⇒ 5차 overload +0.117은 잡음이 아니라 **예측된 부호**).

### 6.5 파일럿 (Fable · seed 950–985 · **확증 seed 200–219과 서로소** ⇒ 오염 0)

| | Δsupply | Δoverload |
|---|---|---|
| **`Ω_3`** | **+25.3 (t=20.1)** | **−0.149 (t=−7.6)** |
| `o6_oracle` (같은 seed) | +11.9 | −0.050 |

**부호보존 8축 20셀 · 반전 0/20**(repair·σ·capsplit·ρ·frag_sigma·EXC·B1·feedback). **오설정 강건성**: `B1×3, EXC×0.5, c×4`를 전부 틀리게 줘도 **+18.55 (t=17.5)** — 여전히 오라클(+11.57)을 이김 ⇒ 담체는 상수가 아니라 **형태**(쌍곡선 + 하중가중 Λ + 응력 중항)를 탄다 = 국소성 주장이 선다. **Λ-순열 sham 확증**: HET에서 sham이 **정확히 blind로 붕괴**(−0.13, t=−0.1) ⇒ **Λ 채널은 인과적**. detgrad-capture = **0.016**.

> ⚠️ 위 수치는 **Fable 파일럿(DIRECTIONAL)**이다. 확증 런 = 사전등록 코드 **sha256 동결** + **확증 seed 200–219** + 적대검증. 그 전에는 어떤 tier도 cement하지 않는다.

### 6.6 남은 반증가능한 음성 (정직)

- **"국소 담체 부재"는 이미 반증됐다**(오라클 자신이 국소 짝-점수이고 Ω가 그것을 2배 이긴다). **증명된 불가능성은 더 좁고 날카롭다**: `Ω_0 ≡ 0`(순간 담체 불가) · HET에서 Λ-맹인 담체는 정보량 0. **이 둘이 5차가 실제로 부딪힌 벽이고, 둘 다 정리다.**
- **남은 음성**: `Ω_1`이 확증 seed에서 blind와 TOST-등가(δ=1.0)인데 `Ω_8`은 아니라면 ⇒ "이득은 환원 불가능하게 반복적 = 담체가 모델을 **시뮬레이션**해야만 한다". (파일럿은 `Ω_1 ≈ Ω_3 ≈ Ω_8`이라 이 음성은 예측되지 않는다.)
- **오라클은 상한이 아니다** — `min(L, S_eq)`는 평형 **장부**다. 물리 DV의 진짜 천장은 `ΔS_eq`의 argmax이고 오라클은 그 **68%**밖에 못 딴다.

---

## 7. 확증 런 결과 — 🟢 DIRECTIONAL-POSITIVE (2026-07-12)

**확증 런(2026-07-12 · $0 numpy · mini · 사전등록 sha256 동결 · 적대검증 REFUTED=false)** — **6번의 발사 끝에 H_054/H_203이 답을 얻었다.**

**🎯 답: 재조합(merge) 대수는 물리 정보를 더하며, 국소 관측 `(cap, L, S, Λ)`만으로 도달 가능하다.** `Ω_1`(RELAX-1 · 이완 1스텝 supply 응답)이 **물리 DV(supply)에서 3 control 전부를 유의 우세**: vs `c2_blind` **+10.87±0.74 (t=+14.6, p=8.9e-12, 20/20)** · vs `Λ-순열 sham` **+3.29±0.45 (t=+7.2, p=7.3e-07, 19/20)** · vs `a_detgrad`(장부 기울기) **+9.75±1.04 (t=+9.4, p=1.5e-08, 20/20)** · **overload도 개선**(−0.073, p=1.0e-09) · **부호보존 44/44 셀(LIVE)·32/32(HET) 반전 0**(PASS 조건에 내장) · **detgrad-capture 0.231**(<0.90 ⇒ 장부 항등식 아님). `o6_oracle`(+2.14)을 **5배 초과** — 오라클은 상한이 아니다(`min()`은 평형 *장부*다).

**🔑 왜 5발이 실패했는지가 *정리*로 밝혀졌다**: 융합은 `S = cap−D`를 **정확히 보존**한다(`S_ij = S_i+S_j`) ⇒ **`ΔS|_t ≡ 0`**(수치확인 `Ω_0` max|·| = 4.4e-16) ⇒ **순간(zeroth-order) 관측 담체는 정의상 장부의 함수다**. [[H_9274]] 5차 `a_comp`의 capture 0.98은 설계 실수가 아니라 **차수의 필연**이었다. **물리 채널은 이완(relaxation)에만 있고, `Ω_1`이 첫 비소멸 차수**다.

**장부-항등식 배제 = 3중**: ① capture 0.231 (vs a_comp 0.976 · a_detgrad 1.000) ② 장부 기울기 arm(`a_detgrad`)을 supply에서 **+9.75로 압도**(그 arm의 supply는 ns) ③ **정의역 논증**: `detgrad`는 `(L,S)`만의 함수라 `∂/∂Λ ≡ 0`인데 `Ω`는 Λ 의존 ⇒ `Ω = λ·detgrad`인 λ **부재**(검증자가 `(cap,L,S)` 고정 후 Λ만 치환해 max|ΔΩ|=1.914·argmax 짝 변경을 코드로 확인). **반정렬 양성대조 `a_comp`가 예측대로 overload를 올렸다**(+0.095, p=1.2e-04) ⇒ 5차의 덫이 실물이었음이 확증 seed에서 재현.

**동어반복 아님(가장 위험했던 지점)**: Ω는 supply 응답을 argmax하지만 그건 *예보*이고 DV는 *실현*이다. **`s_stressshuf`(동일 함수형·동일 argmax·신호만 절단)가 blind로 완전 붕괴**(+0.26, ns) ⇒ 함수형이 이기는 게 아니다. 더 정확한 예보 `Ω_8`이 오히려 더 나쁘고(+10.09 < Ω_1 +10.87) 평형 오라클은 +2.14뿐 ⇒ **예보는 틀릴 수 있다 = 진짜 측정**.

**두 채널 인과성 분리**: `s_stressshuf`(상태 절단) → blind로 붕괴 ⇒ **응력-중항 채널 인과적**. `s_lamperm`(Λ 절단) → **HET에서 정확히 blind로 붕괴**(−0.25, ns) ⇒ **'Λ-맹인 담체는 HET에서 정보량 0'** 불가능성 정리 재현.

⚠️ **정직한 정정 3항(적대검증이 남긴 것 · 반드시 함께 인용)**:
1. **효과 분해 — 재조합 대수(Λ)의 기여는 ~30%다.** Ω_1 − lamperm = +3.29 / Ω_1 − blind = +10.87 ⇒ **Λ 수송(= 진짜 merge 대수) 30% · 응력-중항 채널(= 파티션 기하) 70%**. 헤드라인을 '재조합 대수가 물리를 지배한다'로 읽으면 안 된다 — **더하긴 하되 30%**다.
2. **개정 `V_info` 게이트는 실패불가(재사용 금지)**. 원 런(seed 200–219)은 헤드라인 PASS 조건을 전부 충족했으나 자초한 `V_info`(om_sel_z>1.0) 임계 오설정(실측 0.93)에 걸려 **사전등록대로 INVALID로 기록에 남겼다**(사후 완화 금지 · 규칙⑨). 개정 런은 `V_info` **사양 하나만** 척도-불변형으로 교체하고 **결과를 이미 본 200–219가 아니라 THIRD-disjoint 미관측 seed 300–319**에서 재확증(헤드라인 DV·control·마진·TOST·부호축·판정분기·arm·기질상수는 **바이트 동일** — 검증자가 diff로 확인). 향후 정보채널 게이트는 **sham-대비 우세**로 대체할 것.
3. **파일럿 미재현 2건**: 효과크기 파일럿 +25.3 → 확증 +10.9~13.3(**절반** · 파일럿이 seed-낙관적) · **'HET에서 장부를 잃으며 물리를 딴다(ΔATP=−3.08)'는 재현 실패**(ΔATP=+0.94 ns) ⇒ **그 서사는 버린다**(장부 배제는 위 3중 증거로만 주장).

**HET = INVALID**(검정력): `V_POWER` 2.58× < 3×MDE로 **사전등록 abort 발화**(게이트가 살아있다는 증거 — LIVE는 5.61× PASS). 방향은 유의(+2.67, t=+7.2)하나 채점 불가. 다음 저비용 = HET만 seed 40으로 재발사(검정력만 보강 · 나머지 불변 · 새 disjoint seed).

**독립 재현 4-seed**: 200–219 (+13.3) · 300–319 (+10.9) · **400–419 (+12.0 · 검증자가 직접 고른 미관측 seed)** ⇒ **seed 잡음 아님**(이 lane에서 원 KILL이 seed 잡음이었던 전례를 정면으로 통과). **오설정 강건성**: `B1×3, EXC×0.5, c×4` 전부 틀리게 줘도 효과 **90% 유지**(+9.80, t=+15.4) ⇒ 담체는 상수가 아니라 **형태**(쌍곡선 + 하중가중 Λ + 응력 중항)를 탄다 = **국소성 주장이 선다**(모델-전지 아님).

**scope**: toy organelle 기질(numpy · 300 step · 20 seed) · engine-native `core/` 배선 0 ⇒ **DIRECTIONAL 상한**(`a_toy_scale_recheck` · GREEN 아님). state/mito_organelle_lane/F14_physical_carrier/ (DERIVATION.md · PREREG.md · run.py · run_regate.py · RESULT.md · REFUTE.md).
