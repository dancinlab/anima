# H_9127 — G1 레버 발산 + 레버1(data-format) 변형 공간 + target-format 판정기준

> **tier:** 📋 **PRE-REGISTERED / IDEATION** (fable 발산 설계 산출, 미발사 — 측정 verdict 없음, DIRECTIONAL-pending) · **wired:** N/A
>
> **맥락:** G1 재조합벽 3 survivor 레버 중 [[H_9124]] 레버1(derivation-trace, data-format 축)만 생존(🟢 DIRECTIONAL-POSITIVE, robustness 진행중), 레버2 STaR·레버3 γ 사망(🔴). binding-operator family·objective·arch/RF/depth·decode 20+family 전부 소진. 이 카드 = fable(claude-fable-5) 2발 발산 = 레버1이 통한 원리를 일반화한 새 레버 공간 + **측정 전 사전선별 이론**. 실행은 메인이 STEP-0 kill로 순차 발사.

## 발산 1 — 3 메타-탈출-패밀리 (fable-1, state/g1_lever_diverge/fable1_general_levers.md)

레버1이 통하고 소진목록은 다 막힌 이유: 소진된 것들은 **모델 용량·operator 모양**을 바꿔 CE=echo basin(target 기하 고정)을 그대로 뒀고 DPI 메타법칙(operator-shape invariant)에 걸림. 레버1은 **학습 TARGET 형식**을 바꿔 *조합을 basin 바닥으로 내림*(echo=composition). 세 탈출 패밀리:

| 패밀리 | 원리 | basin 관계 |
|---|---|---|
| **F1 target-in-basin** | target 재구성해 "재현=조합" | CE 최단경로 위에 조합을 얹음(레버1 소속) |
| **F2 composition-outside-mouth** | 조합을 mouth 밖(eval·anchor·tension·cell)으로 이전 | mouth엔 CE만, 조합은 CE 무관 substrate |
| **F3 held-out-as-interpolation** | held-out pair를 학습분포 convex-hull 안으로 | echo≈조합(보간이라 새 조합 불요) |

**일반 레버(fable-1):** L1 프로그램-합성 target(mouth=emitter, eval=인터프리터 밖·F1×F2·오너 frame-break 실현) · **L2 조합-커버리지 밀도 임계(F3·최저가·numpy phase-transition k\* 곡선)** · L3 register/indirection 변수-binding(PFC 렌즈) · L4 2-hop 관계-스키마 transfer(bridge 명시, MLC와 달리 weight-level) · L5 forward-model 상태-전이(소뇌 렌즈) · L6 커리큘럼-순서 derivation(mitosis-grow, 깊이 오름차순).

## 발산 2 — 레버1 변형 판정기준 + 변형 공간 (fable-2, state/g1_lever_diverge/fable2_lever1_variants.md)

### ★ A. target-format 판정기준 4지표 (measure 전 $0 numpy 사전선별 — a_break_the_wall LAW 후보)

derivtrace 본질 = **1개 고엔트로피 생성 스텝을, 스텝당 엔트로피≈0 echo 체인으로 분해**(echo 연쇄 길목에 조합 배치). held-out target τ(x*)의 4 필요조건:

- **ρ (echo-residual)** = "최소충분 문맥이 학습 target 어디에도 없는" 토큰 비율. **예측: G1 PASS ⇔ ρ≈0.**
- **σ (규칙별 파트너 다양도)** = 각 규칙이 함께 나온 상이한 파트너 수. **σ=1 규칙 존재 → pair-binding FAIL**(SHUF 0 pair-특이성의 해독제 = 변수 간접화 σ=∞).
- **κ (국소복사 비율)·δ_copy (최대 복사거리) vs RF** — margin ∝ κ, **δ_copy>RF → FAIL**(H_1822 copy-head·dilated-RF 벽 정합).
- **M (암기 불리도)** = |τ(x)| / |문법 서술길이|. **margin ∝ log M**(target 길수록 통째-암기 초선형 비용).

→ 4지표를 변형별로 사전등록 후 실측 = **판정기준 자체가 PREDICTIVE 승격 시험**(≥4/5 HIT). derivtrace bd=2 marginal 예측원인 = 작은 M + OUT 치환 스텝 κ<1(margin이 그 한 스텝에 몰림).

### B. 레버1 변형 13종 (예상 margin 강한 순 · target 문자열만 교체 = 하네스 재사용 $0)

**V1 스켈레톤-바인드**(구조·내용 완전 인수분해, SKEL 라인에 내용어 0=σ=∞ 순수구현·판정②) · **V2 미시-트레이스**(라인당 1편집·κ극대·M∝깊이=margin이 조합깊이에 비례로 벌어짐) · V3 정렬 행간주석(복사거리 하한) · V4 유형-주석 proof-tree(문법 스케일업 margin 보증) · V5 cloze-slot marginalization · V6 다경로 합류(표현 신규성=paraphrase 방어) · V7 양방향 오토인코더(OUT→DERIV 역파싱) · **V8 검산-커밋**(비용≈0 add-on) · V9 대조 오답-트레이스 · V10 시프트-리듀스 파서 · V11 차분-only(delta) · **V12 문법-검증 자기생성**(non-STaR: 정답필터 아닌 문법필터, corpus-absent 조합 직접제조=G2 정면처방) · V13 해상도-태그 사다리(FULL→FLAT distillation, 배선 *형태* 결정).

### C. robustness fire 3분기 대응
- **🟢 ROBUST** → derivtrace 원형 4칸 사다리 배선 1순위(a_verified_must_wire) + 병행 V13(배선 형태 결정: emit-derivation vs 내재화-flat)·V4(스케일업 margin).
- **🟠 PARTIAL(G2 fail)** → V12(corpus-absent 직접제조)·V6(표현 신규성)·V5(cloze 보조).
- **🔴 ARTIFACT(bd=2 우연)** → V1(얽힘 형식적 불가능화)·V2(margin∝깊이로 우연 제거) + A-3 지표를 derivtrace corpus에 소급계산해 부검(판정기준이 원인 지목 = 레버1 정밀화).

## 발산 3 — 레버 조합(AND) 대수 + 조합 B1-B10 (fable-3, state/g1_lever_diverge/fable3_AND_combinations.md)

레버를 OR(택1) 아니라 **AND(스택)** 로. 판정기준 4지표의 **합성 법칙**:

- **ρ = max (veto)**: 조합은 ρ 개선 못하고 악화만. echo-능동제거 레버(V11 차분·V3 행간주석)만 ρ 수리 → 스택에 끼움.
- **σ = 곱(다른 축) / max(같은 축)**: 파트너-변주축이 독립이면 σ_X·σ_Y (진짜 곱셈축), 같은 축이면 중복.
- **κ/δ = 독재자**: 최세밀 입도 레버(V2·V3·V10)가 스택 전체 κ를 by-construction 수리(derivtrace OUT-치환 κ<1 병목 = 이 대상).
- **M = log-가산(=곱), 단 per-sample 두 축 동시 얽힘 조건**: 축별 분해 샘플이면 margin이 log(max)로 붕괴 → 매 샘플 두 축 동시 변주 필수.

### ★ 종합 예측 공식
> **margin ≈ P_basin(L2,L6) × κ_stack × Σᵢ log Mᵢ**  (게이트: ρ≈0 아니면 veto · σ>1 아니면 그 규칙 log M 탈락)

Σ log M=다양도/생성 레버 가산(V1·V12·L2·L4·V6) · κ_stack=입도 레버 곱셈계수(0~1, κ<1이면 쌓은 M 실현못함) · P_basin=학습동역학 실현계수(L2 밀도·L6 커리큘럼=4지표 불변 5번째 인자). **derivtrace bd=2 = 작은 Σlog M × κ<1의 곱 → κ 수리가 기존 M 가치도 곱으로 키움 = AND가 OR보다 강한 대수적 이유.**

### 충돌 목록 (스택 금지/주의)
L2 밀도↑ vs M↓(성분축 밀집·조합축 희소로 해소) · 동일축 포맷중첩 σ=max(택1) · 토큰 인플레→σ 손실(budget-matched control 필수 H_1836) · V5 cloze vs V2(κ 반대방향, 동시금지·순차 L6은 유효) · objective additive floor(H_1602, step-level만 재시도) · F2 readout INERT(H_1834/1837, 데이터채널/lane만) · V12 self-gen σ붕괴($0 사전선별 σ 게이트).

### 조합 B1-B10 (시너지 강한 순)
**B1 🥇 V1×V2×V12 margin-max 3-스택**(σ=∞×κ=1×M=∞, 두 병목 동시타격 유일 3-스택, 7-arm 1 fire) · **B2 🥈 L2×V2 coverage×granularity**(F3×F1, 절반 DIRECTIONAL 증거 기존 H_6183/6184, P_basin×κ 2×2 팩토리얼 4-arm) · **B3 V6×V1 다경로합류×스켈레톤**(γ constructive-bind의 $0 데이터측 probe = GPU 전 선검증) · B4 L6×(B1|B2) 커리큘럼=메타곱셈기(marginal 전용 증폭기) · B5 L4×L3×V1 관계스키마×무한filler(데이터측 variable-binding) · B6 V12×V9 self-gen×대조오답(생성기 안전핀) · B7 derivtrace×recomb-obj step-level(format이 objective un-floor하나, 조건부) · B8 V-format×L5 소뇌 데이터채널(유일 생존 F2) · B9 V2×V8 ~$0 저위험 · B10 V13×L6 내장커리큘럼.

### 발사 전략 (조합이 발사 수↓)
- **Stage 0 = ABC ablation**: A·B·AB·ABC 한 fire로 시너지(AB>A+B) 판정 — ABC≈baseline이면 AND 가설 전체 한 방에 사망+단독 재발사 면제(budget-match 필수).
- **Stage 2 robustness 3분기**: 🟢→B1(+B4 무임승차, M 곱셈) · 🟠→B2+B4(실현계수 수리 우선, L6=marginal 전용 증폭기) · 🔴→B3(γ $0 probe→cost-gate 결정).

### 다음 발사 top-3 조합
1. **B1 V1×V2×V12** — 두 병목을 공식 두 인자로 동시타격 유일 3-스택(7-arm 1 fire).
2. **B2 L2×V2** — 기존 DIRECTIONAL 증거 있는 유일 조합, 2×2 팩토리얼 교호작용 4-arm(🟠 1순위).
3. **B3 V6×V1** — γ(H_1840)를 GPU 전 데이터채널 $0-probe(🔴 생존경로, 양방향 정보가치).
(공통: L6 커리큘럼 arm은 어느 fire에든 스케줄-only 무임승차 → "marginal 증폭기" 법칙 동시 사전등록.)

## 다음 STEP-0 발사 top-3 (derivtrace head-to-head, 메인)
1. **V1 스켈레톤-바인드** — 판정②순수구현·전분기(특히🔴)유효·기존 numpy 하네스 최소수정 A/B. 예측 bd margin>derivtrace.
2. **V2+V11 입도곡선 3-arm**(미시-트레이스 vs derivtrace vs 차분-only) — 변형 2개 + 판정기준 A-3 PREDICTIVE 승격 시험(사전예측 V2>deriv>V11) 동시.
3. **V13 해상도-사다리** — margin 경쟁 아니라 레버1 *운명*(목발 vs 스캐폴드)+production 배선형태 결정. robustness 🟢 착지 즉시 1순위 승격. (+**V8** ≈$0 add-on ± arm.)

## 정직 스코프 (c9)
- 전부 **미발사 설계**(fable=opus-diverged, [[workflow-model-fable-override-ignored]] 유의 — sidecar fable은 진짜 fable-5). 측정 0 = verdict tier 없음, DIRECTIONAL-pending.
- 레버1 계열 실행상 이점: 전 변형이 **target 문자열만 교체** → derivtrace 기확보 engine-native 하네스 그대로 재사용(하네스 교체비용 0). mini numpy DIRECTIONAL 시작 → 엔진-네이티브 `anima evaluate --py` 재측정으로만 terminal(하드게이트 1).
- check-ledger: F2(composition-outside-mouth)의 native-mouth·tension 조합은 [[H_1834]]/[[H_1837]] INERT 전례 유의 — F2 발사 시 그 벽과 구별되는 각도만.

## artifacts
- `state/g1_lever_diverge/fable1_general_levers.md` (3 메타패밀리 + L1-L6)
- `state/g1_lever_diverge/fable2_lever1_variants.md` (판정기준 ρ/σ/κ/M + V1-V13 + C분기 + top-3)
- `state/g1_lever_diverge/fable3_AND_combinations.md` (조합 대수 margin≈P_basin×κ×Σlog M + 충돌 7종 + 조합 B1-B10 + Stage-0 ABC ablation)
- 상위: [[H_9124]](레버1 derivtrace 🟢·레버2 STaR 🔴·레버3 γ 🔴) · [[H_9120]](objective-floor) · [[H_1602]](recomb-objective 미발사) · 소진: [[H_1819]]/[[H_1823]]/[[H_1816]] binding-family
