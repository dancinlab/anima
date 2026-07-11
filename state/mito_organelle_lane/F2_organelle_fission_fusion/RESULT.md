# H_9274 / F2 — organelle 분열·융합 probe 결과 · 🔴 KILL (등록된 정책은 blind control보다 **나쁘다**)

- **일시:** 2026-07-12 · mini CPU-local · numpy only · wall **5.1s** · $0
- **산출:** `run.py` · `result.json` (raw) · 본 문서
- **seeds:** 5 (0–4) · 결정적 · demand 스트림은 arm 간 **동일**(paired Δ)
- **p5:** emit gate 무접촉 — 구조(호흡) 레인 전용. 코드에 emit/silence 경로 자체가 없음.

---

## 1. 한 줄 결론

**카드 §3에 등록된 health-aware fission-fusion(실험 arm)은 동일 예산의 health-blind random rewiring(c2)보다 throughput이 −0.359 (5/5 seed 전부 음수, sweep 5개 ρ 전부 음수) 낮다 ⇒ 등록 가설 KILL.**
단, 같은 예산의 분해 ablation이 **정보 채널의 위치**를 특정했다: **fusion 선택은 정보를 나르지만(+0.157), aware fission이 그 정보를 파괴한다.**

---

## 2. 기질 (요약 · 상세는 run.py 헤더)

64 site의 **드리프트하는 수요장**(총수요 일정, 공간분포만 random-walk → frozen 배치는 반드시 낡는다) · 16 organelle = (territory, capacity c, mtDNA 병변마스크 L∈{0,1}^32).
- health h = 1 − |L|/G · supply = c·h · load = territory 수요합 · **output = min(load, supply)** (ATP는 유닛 간 이송 불가 = pooling 이득의 원천)
- **damage(ROS)** = Poisson(b0 + b1·초과stress) → 임의 유전자 KO · **repair** = 병변당 1%/step (전 arm 동일)
- **FUSION** = territory 합집합 · capacity 합 · **L_i AND L_j (mtDNA 상보성 = 손상 희석)**
- **FISSION** = territory 2분할 · capacity 절반씩 · **mtDNA 양쪽에 복사**
- 두 연산 모두 **총 capacity 보존**(검증됨) · 이벤트 예산 = 전 dynamic arm 공통 k=2 fission + 2 fusion / step (N=16 고정, 검증됨)

**유효성 게이트(V1):** 손상 실재 ✅ (c1 health 0.383 < 0.99) · capacity 실제 구속 ✅ (c1 throughput 0.188 < 0.999) · capacity 보존 ✅ · N 보존 ✅ ⇒ **no-op 아님, INVALID 아님.**

---

## 3. 수치 (primary ρ=0.85 · 사전등록 · mean±std over 5 seeds)

| arm | 선택 정책 | 예산 | throughput | health | overload | fusion쌍 hamming | **clone쌍 비율** |
|---|---|---|---|---|---|---|---|
| **실험** `exp_aware_ff` | 고stress split + 저health 쌍 fuse | 2+2 ev/step | **0.290 ± 0.038** | 0.533 | 0.417 | 2.30 | **0.54** |
| c1 `frozen` | 동역학 없음 | 0 ev | 0.188 ± 0.034 | 0.383 | 0.592 | — | — |
| c2 `random_rw` | **health-blind 랜덤** | 2+2 ev/step | **0.650 ± 0.053** | 0.934 | 0.272 | 6.46 | 0.01 |
| a3 `awarefuse` | 랜덤 split + **저health 쌍 fuse** | 2+2 ev/step | **0.807 ± 0.032** | 0.999 | 0.135 | 1.75 | 0.07 |
| a4 `awarefiss` | **고stress split** + 랜덤 fuse | 2+2 ev/step | 0.675 ± 0.059 | 0.947 | 0.321 | 5.71 | 0.01 |

**Δ (paired, 동일 seed·동일 수요 스트림):**

| 비교 | Δ throughput | seed별 |
|---|---|---|
| **실험 − max(c1,c2) = 실험 − c2** | **−0.359 ± 0.089** | −0.30 / −0.26 / −0.49 / −0.34 / −0.41 (5/5 음수) |
| 실험 − c1 (frozen) | +0.102 | (dynamics 자체는 frozen보다 낫다 — 단 이건 blind도 하는 일) |
| a3 − c2 | **+0.157 ± 0.024** | +0.17/+0.19/+0.12/+0.15/+0.16 (5/5 양수, ≈6.5σ) |
| a4 − c2 | +0.025 ± 0.032 | +0.04/+0.05/+0.05/−0.02/+0.01 (1σ 미만 = 무의미) |

**ρ sweep (throughput, 전 구간 동일 순서 — primary가 체리픽이 아님):**

| ρ | exp | c1 | c2 | a3 | a4 |
|---|---|---|---|---|---|
| 0.50 | 0.646 | 0.424 | 0.831 | **0.947** | 0.809 |
| 0.70 | 0.503 | 0.284 | 0.709 | **0.886** | 0.719 |
| **0.85** | 0.290 | 0.188 | 0.650 | **0.807** | 0.675 |
| 1.00 | 0.159 | 0.131 | 0.585 | **0.723** | 0.625 |
| 1.20 | 0.099 | 0.070 | 0.505 | **0.584** | 0.575 |

실험 arm은 **모든 ρ에서 c2보다 나쁘다.** a3은 **모든 ρ에서 최고.**

---

## 4. 왜 — 메커니즘 (clone-pair 퇴화 루프)

진단 계측(추가 RNG 소비 0 → 수치 bit-identical)이 원인을 지목한다:

- **aware fission**은 최고 stress 유닛을 쪼갠다. stress = load/(c·h)이므로 최고 stress ≈ **가장 병든 유닛**. 분열 시 **mtDNA는 복사**된다 ⇒ 병변마스크가 **동일한 쌍둥이 2개** 생성.
- **aware fusion**은 최저 health 2개를 고른다 ⇒ 방금 만들어진 **그 쌍둥이**를 정확히 집는다.
- 융합 상보성은 `L & L = L` ⇒ **손상 희석 0**. 계측: 실험 arm의 융합 이벤트 **54%가 clone 쌍**(c2는 1%), 쌍의 damage heterogeneity(hamming) 2.30 vs c2 6.46.

⇒ **두 aware 정책이 반(反)시너지다.** 융합의 상보성은 **손상의 이질성**을 먹고 사는데, aware fission이 바로 그 이질성을 (게놈 복사로) 파괴하고 aware fusion에게 되먹인다. 닫힌 퇴화 루프 = 두 번 aware한 것이 blind보다 나쁜 이유.

**따라서 카드의 "분열 = 부하분산 + 손상격리" 렌즈는 이 기질에서 반증된다:** 분열은 손상을 격리하지 않고 **복제**한다. 격리가 되려면 F3(미토파지 = 복제된 쌍 중 하나 제거)가 반드시 붙어야 하며, F3 없는 F2 aware-fission은 순수 손해다.

---

## 5. 반증조건 충족 여부 (카드 §3 대비)

| 카드 조건 | 결과 |
|---|---|
| **PASS**: Δthroughput(dynamic) − max(c1,c2) > margin(1%) | ❌ **−35.9%** (margin의 반대 방향) |
| **FAIL**: dynamic ≈ random ⇒ theater | ❌ 이것도 아님 — dynamic **≪** random. ΔEff≈0(무정보)이 아니라 **음의 정보**(적극적 해악) |
| V1 유효성(손상 실재·capacity 구속·예산 공정) | ✅ 전부 통과 ⇒ INVALID 아님, no-op 아님 |

⇒ **THEATER가 아니라 KILL.** (ΔEff≈0이면 theater였겠으나, Δ가 크고 일관되게 음수다.)

---

## 6. 판정

- **H_9274 (등록된 composite health-aware fission-fusion) = 🔴 KILL.** 동일 예산 health-blind rewiring이 압도한다.
- **살아남은 조각 = a3 (aware **fusion** only + blind fission) = 🟡 DIRECTIONAL-POSITIVE.** 동일 예산에서 c2 대비 +0.157 (5/5 seed, ~6.5σ), health 0.934 → 0.999. **저-health 표적 융합 선택은 실제로 health 정보를 나른다.** 정보 채널은 **융합 쪽에만** 있다.
- **부수 확인:** 동역학 자체(blind 포함) ≫ frozen (0.650 vs 0.188). 하지만 이건 health 정보 주장이 아니다 — blind도 하는 일이므로 카드 가설의 증거가 **아니다**.

## 7. 정직한 scope 한계 (과대해석 금지)

1. **이건 손으로 만든 toy 시뮬레이터다.** anima 엔진(CLM/decode/emit)에 배선된 것이 0이다 ⇒ a3의 양성조차 **toy DIRECTIONAL**이며 engine-native verdict가 아니다 (`a_engine_native_learning`·`a_toy_scale_recheck`).
2. a3의 이득 크기는 내가 고른 **상보성 규칙(L_i AND L_j)** 에 의존한다. 규칙 자체는 전 arm 동일하므로 **Δ = 표적선택의 정보**라는 결론은 유효하지만, **절대 크기는 모델 산물**이다.
3. 수치 blow-up 가드 1개(ROS 손상 포화 EXC_CAP=2.0 — 죽은 유닛의 stress→∞로 Poisson 무한 draw를 막음)는 **전 arm 동일 적용**이라 어느 arm도 편들지 않는다.
4. 하이퍼파라미터 재조정 없음: primary ρ=0.85·margin·seed는 실행 **전** 고정, sweep 전 구간 공개(체리픽 아님). tune-to-green 0회.

## 8. Follow-on (제안 · 미실행)

- **F2′ (신규 카드감):** "**융합 표적선택만** 정보를 나른다 + **aware fission은 F3(미토파지) 없이는 해롭다**" — 즉 F2는 **F3에 물려 있다**(Fable이 예측한 THEATER 랭킹 6위의 근거 "F4/손상신호가 없으면 QC는 no-op"의 변주가 실측된 셈). F3를 붙여 clone 쌍 중 하나를 제거하면 aware fission이 흑자로 돌아서는지가 다음 $0 실험.
- 상보성 규칙을 anima 실물(예: expert-mask/route 중복도)로 치환했을 때도 aware-fusion Δ가 살아남는지 = engine 접점 첫 관문.
