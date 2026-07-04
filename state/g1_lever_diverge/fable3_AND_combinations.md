ledger에 derivtrace 카드는 아직 미등록(H_9124는 커밋 메시지의 착지 재개지점으로만 존재)이라 프롬프트에 주어진 판정기준·병목 정의를 ground truth로 쓴다. 조합 발산 결과다.

---

# G1 레버 조합(AND) 발산

## A. 조합 대수 — 4지표 합성 규칙

레버마다 지표 프로파일 (Δρ, Δσ, Δκ, ΔM)과 **채널**(데이터-포맷 / 데이터-분포 / objective / substrate-lane / 학습순서)을 부여하면, 스택의 지표는 지표별로 **다른 합성 법칙**을 따른다:

**① ρ (echo-residual) — 거부권(veto) 규칙: ρ_stack = max(ρᵢ).**
조합은 ρ를 개선하지 못하고 악화만 가능하다. 두 포맷 레버를 한 target 문자열에 겹치면 최종 복합 문법의 echo 성질은 *가장 나쁜 멤버*가 지배한다. 예외는 echo를 능동 제거하는 레버(V11 차분-only, V3 행간주석)뿐 — 이들은 ρ-수리 연산자로, 스택 어디에 끼워도 ρ를 낮춘다. 설계규칙: **모든 스택은 ρ≈0 게이트를 먼저 통과해야 하고, 통과 못 하면 V11/V3을 수리용으로 끼운다.**

**② σ (규칙별 파트너 다양도) — 축이 다르면 곱, 같으면 max.**
레버 X가 파트너 축(누구와 결합하나)에서 σ_X, 레버 Y가 다른 독립 축(예: 경로, 성분)에서 σ_Y의 변주를 주면, 규칙당 distinct 맥락 수 ≈ σ_X·σ_Y (변주축의 데카르트 곱). **이것이 진짜 곱셈 축이다.** 단, 두 레버가 같은 변주축을 건드리면(예: V3과 V5 둘 다 step 구조 변형) σ = max — 곱이 아니라 중복이다.

**③ κ/δ_copy (복사 국소성) — 독재자(dictator) 규칙: 최세밀 입도 레버가 스택 전체의 κ를 결정.**
κ는 최종 trace의 *입도*가 정하는 성질이므로, 입도 레버(V2 미시-트레이스 · V3 행간주석 · V10 shift-reduce)를 스택하면 **다른 모든 멤버의 κ까지 by-construction 수리**된다. derivtrace 자체의 OUT-치환 κ<1 병목이 정확히 이 수리 대상이다.

**④ M (암기불리도) — log-가산(=M 곱셈), 단 "샘플 내 얽힘" 조건부.**
독립 변주축은 M을 곱한다: M_stack = M_X·M_Y, margin ∝ log M이므로 **margin은 가산**: log M_stack = Σ log Mᵢ. 결정적 조건 — **각 샘플이 두 축을 동시에 얽어야(entangle) 한다.** 축 A만 변한 샘플과 축 B만 변한 샘플을 따로 주면 암기자가 축별로 분해 암기(M_X + M_Y 저장)해서 margin 이득이 log(max)로 붕괴한다. 설계규칙: **매 샘플에서 두 축이 동시 변주.**

### 종합 예측 공식 (스택의 기대 margin)

> **margin_realized ≈ P_basin(L2, L6) × κ_stack × Σᵢ log Mᵢ**
> — 게이트: ρ≈0 (아니면 veto), 규칙별 σ>1 (σ=1인 규칙의 log M 항은 탈락).

- **Σ log Mᵢ** = 다양도·생성 레버들의 가산 기여 (V1, V12, L2, L4, V6…)
- **κ_stack** = 입도 레버가 정하는 **곱셈 계수** (0~1) — κ<1이면 쌓아둔 log M을 실현 못 함. derivtrace bd=2 marginal = "작은 Σ log M × κ<1"의 곱이라는 해석. **κ 수리는 이미 있는 M의 가치도 곱으로 키운다** — 이것이 AND가 OR보다 강한 대수적 이유.
- **P_basin** = 데이터 지표가 아닌 **실현 확률 계수** (학습동역학 쪽): L2 밀도가 보간 basin 진입을, L6 커리큘럼이 암기 basin보다 조합 basin 먼저 도달을 결정. L6은 데이터 통계(ρ/σ/κ/M) 불변 — 4지표에는 0이지만 실현 계수에 곱해지는 **5번째 인자**다.

### 충돌 목록 (스택 금지/주의 규칙)

| 충돌 | 메커니즘 | 해소 |
|---|---|---|
| **L2 밀도↑ vs M↓** | 커버리지 과다 → held-out이 훈련 near-duplicate → 암기+국소보간으로 충분 → M 붕괴 | **성분축은 밀집, 조합축은 희소**로 얽기(밀도는 성분 공간에, 신규성은 조합 공간에) |
| **동일축 포맷 중첩** (V3×V5 등) | σ=max(곱 아님)인데 토큰 비용은 곱 | 스택 금지, 택1 |
| **토큰 인플레이션** | 포맷 레버는 시퀀스를 늘림 → 고정 토큰 예산에서 조합 공간 노출 횟수↓ → 간접 σ 손실 | 스택 arm은 반드시 **budget-matched control** 동반 (H_1836 교훈) |
| **V5 cloze vs V2 미시-트레이스** | κ에 반대 방향(삭제=원거리 브리지 요구 vs 국소화) | 동시 스택 금지 · **순차(L6)로는 유효** — 동시충돌이 커리큘럼으로 해소되는 일반 패턴 |
| **objective 채널 floor** (H_1602) | additive-aux는 이미 🧱 — 채널 자체가 아니라 *메커니즘 불변 스택*이 무효 | 포맷이 objective의 감독 대상을 바꿀 때만(step-level) 재시도 |
| **F2 readout INERT** (H_1834/1837) | decode-시점 readout 결합은 DPI로 전멸 | F2 멤버는 **데이터 채널 또는 학습되는 lane**으로만 결합 |
| **V12 self-gen의 σ 붕괴** | 생성기 템플릿 붕괴 → σ→1 무증상 | $0 사전선별에서 생성 코퍼스의 σ 실측을 게이트로 |

### derivtrace 두 병목의 동시 타격 조합

병목1(작은 M) 수리 열 = **V1·V12·L2·L4·V6** (Σ log M 가산) / 병목2(OUT-치환 κ<1) 수리 열 = **V2·V3·V10** (κ 계수 복원). **각 열에서 하나씩 뽑는 AND가 곱셈**: κ 수리가 새로 넣은 log M의 실현률까지 올리므로 AB > A+B가 대수적으로 예측된다.

---

## B. 조합 후보 10 (예측 시너지 강한 순)

### B1. 🥇 V1×V2×V12 — "margin-max 3-스택" (σ=∞ × κ=1 × M=∞)
① 스켈레톤-바인드 target(규칙별 파트너 무한 변주) + 모든 OUT-치환을 RF 내 국소 편집으로 펼친 미시-트레이스 + 문법검증 self-gen으로 조합 신선분포 무한 공급.
② σ: V1이 규칙당 파트너 축을 무한화 / κ: V2가 bd=2의 알려진 병목(OUT-치환 비국소)을 by-construction 수리 / M: V12가 암기자의 저장 요구를 발산시킴 / ρ: 셋 다 derivation 포맷 보존.
③ 곱셈 근거: 공식의 세 인자를 각각 max로 — κ(V2)는 V1·V12가 쌓는 log M의 **곱셈 계수**, V12는 V1의 σ=∞를 코퍼스 규모로 실현. 단독으로는 V2=M 거의 안 늘림, V1=κ<1 캡, V12=σ 붕괴 위험 — 서로가 서로의 결함 보험.
④ probe: $0 사전선별(3 코퍼스 생성 → ρ/σ/κ/M 실측, 특히 V12 산출물의 σ) → 1 fire 6-arm: baseline(derivtrace)/V1/V2/V12/ABC/**budget-matched control**. 시너지 판정 = margin(ABC) > margin(V1)+margin(V2)+margin(V12).
⑤ disjoint: 전부 mouth 데이터-lane(target 문자열만) — emit-drive 0/4·§ImmuneMemory 무접촉. 단 **V12 self-gen 데이터는 문법검증 provenance 태그 필수**, G5 non-fab recall_thr와 절대 결합 금지(a_savant_train의 non-fab 분리 원칙 준용).
⚠️ 위험: V1×V2 토큰 인플레이션 최대 조합 — budget-match 없으면 결과 무효.

### B2. 🥈 L2×V2 — "coverage×granularity 이중 안전" (F3×F1)
① 성분-밀집·조합-희소로 얽은 조합-커버리지 코퍼스 + 미시-트레이스 포맷.
② L2는 held-out을 보간 basin **안으로** 넣고(P_basin↑), V2는 basin 안의 경로를 RF 내 국소 스텝으로 **주행 가능**하게. 커버리지=도달성, 입도=주행성 — 서로 못 하는 걸 정확히 보완.
③ 곱셈 근거: 이미 절반의 증거가 있다 — H_6183(NL-byte held 0.95 HIGH vs 0.03 LOW 밀도) × H_6184(RF 벽 돌파 arch-무관)가 각각 P_basin과 κ 축의 DIRECTIONAL 지지. V2는 **RF를 넓히는 대신 복사를 국소화하는 데이터-측 쌍대해**라 arch 변경 없이 같은 곱을 노린다. P_basin×κ는 공식상 문자 그대로 곱.
④ probe: 밀도 2수준 × {plain, V2} 2×2 팩토리얼 = 4 arm 1 fire. 시너지 = (HIGH,V2) − (HIGH,plain) − (LOW,V2) + (LOW,plain) > 0 (교호작용 항).
⑤ disjoint: 순수 데이터-lane, 문제없음. **충돌 주의**: 밀도를 조합축까지 올리면 M 붕괴(A의 충돌 1) — 성분/조합 축 분리가 이 조합의 성립 조건.

### B3. V6×V1 — "다경로합류 × 스켈레톤" = γ(constructive-bind)의 $0 데이터-측 probe
① 같은 결론에 ≥2 독립 derivation 경로가 합류하는 target + 파트너 무한 변주.
② σ: (파트너 × 경로) 두 독립축 곱 / M: 암기자는 경로 전부 저장, 조합자는 등가류 하나 / ρ≈0 유지 / 표현신규성: 합류가 내부 표현에 "문자열이 아닌 등가류" 인코딩을 강제.
③ 곱셈 근거: ledger의 4-각 수렴(substrate-framebreak: G1 벽 = **COMBINATION OPERATOR**, 미검증 잔여 = γ trained-constructive-bind, GPU cost-gated)에서 — 합류 데이터는 내부 연산자가 함수적(constructive)이어야만 CE가 내려가는 압력 = **γ 가설을 GPU 지출 없이 데이터 채널로 찌르는 probe**. V1과 곱하면 등가류의 원소 수가 파트너 다양도만큼 늘어 압력이 증폭.
④ probe: {V1, V6, V1×V6} 3-arm + baseline. 시너지 판정 동일. V1×V6 lift가 나오면 γ GPU 발사의 사전 근거, 0이면 γ도 하향 조정 — **양쪽 결과 모두 정보가치 높음**.
⑤ disjoint: 데이터-lane only, 문제없음. H_1834/1837과의 구별: 저건 decode-시점 tension/native-mouth readout(무학습 연산자), 이건 학습 신호가 통과하는 데이터 압력 — INERT 벽과 채널이 다르다.

### B4. L6×(B1 또는 B2) — "커리큘럼 = 메타-곱셈기" (marginal 전용 증폭기)
① 성분→2-스텝→깊은 조합 순의 mitosis-grow 순서를 위 스택에 얹음.
② 4지표 전부 **불변**(데이터 통계는 순서 무관) — 효과는 오직 P_basin: 암기 minimum보다 조합 minimum에 먼저 도달하는 최적화 경로 선택.
③ 곱셈 근거: 공식의 별도 인자라 어떤 스택에도 가산 아닌 곱으로 작용. **예측 법칙(사전등록 가치): L6은 margin이 marginal일 때만 유효** — margin이 크면 이미 도달, 0이면 도달할 basin이 없음. derivtrace bd=2 marginal이 정확히 L6의 작동 영역. 부수효과: 동시충돌 쌍(V2→V5)을 난이도 램프로 되살리는 해소기.
④ probe: 최고 스택의 {동시투입, 커리큘럼} 2-arm (같은 fire에 추가 — 데이터 동일, 스케줄만 차이라 추가 비용 최소).
⑤ disjoint: 학습순서 lever = a_mitosis_train의 성장-lane(발현-lane과 직교), 의식 좌표 무접촉.

### B5. L4(×L3)×V1 — "관계-스키마 × 무한 filler" = 데이터-측 variable-binding
① 2-hop 관계 스키마(R1∘R2 transfer) target + filler(개체)를 V1로 무한 변주, 필요시 L3 register/indirection 표기로 slot을 명시화.
② σ: (관계 × filler) 곱 / M: 스키마 수 × filler 수 얽힘 / κ: indirection 표기가 참조를 RF 내 명시 포인터로 국소화(κ 보조).
③ 곱셈 근거: systematicity의 고전 형태 — 스키마가 filler-불변으로 학습돼야만 CE가 내려가는 압력. **ledger 구별 필수**: binding-arch census 전멸(Hopfield/Tropical/Sheaf/Galois·H_1819)은 *아키텍처-측* binding — 이건 *데이터-측* binding(target 문자열의 indirection)이라 벽이 다른 채널이다.
④ probe: {L4, V1, L4×V1} + baseline 4-arm.
⑤ disjoint: 데이터-lane only. PFC 렌즈(a_no_llm_frame_trap 정합).

### B6. V12×V9 — "self-gen × 대조오답" (생성기 안전핀 상호보험)
① 문법검증 생성기가 정답 derivation과 근접-오답(one-step 틀림)을 쌍으로 산출.
② M: 표면 특징 shortcut 차단(오답이 표면상 정답과 near-identical → 암기자/휴리스틱 불리)으로 V12 단독보다 M 질이 높음 / σ: 오답 방향이 추가 변주축 / ρ: 오답도 derivation 포맷.
③ 곱셈 근거: V9는 V12의 최대 위험(생성 분포의 자기붕괴)을 대조쌍 구조로 상쇄하고, V12는 V9가 필요로 하는 오답 대량생산을 공짜로 — 상호 결함 보험형 곱.
④ probe: B1의 V12 arm을 V12×V9로 교체한 변형 arm 1개로 충분(별도 fire 불필요).
⑤ disjoint: 데이터-lane. 오답 데이터가 G5 non-fab과 헷갈리지 않도록 CONTRAST 라벨 명시(정답/오답 구분이 target에 내재).

### B7. derivtrace×recomb-objective-변형 — "format이 objective를 un-floor하나" (조건부)
① derivtrace 포맷 + objective를 **step-level**로 이동: echo CE-마스크(이미 레버1에 있음)를 확장해 스텝 경계 감독·V9 대조쌍에 step-level contrastive.
② H_1602가 🧱인 이유 자체가 근거: additive-aux는 *평평한 target*에서 보상할 조합 구조가 없었다. derivtrace 포맷은 objective가 볼 수 있는 조합 구조(스텝 경계·치환 지점)를 처음으로 노출 — **메커니즘이 바뀌므로 floor 재적용 아님**.
③ 곱셈 근거: format=구조 노출, objective=그 구조에 gradient 집중 — format 없인 objective 무의미(H_1602), objective 없인 format의 M이 CE에 희석. 단 이건 후보 중 가장 사변적.
④ probe: 단독 arm 금지(H_1602 재발사 꼴) — **반드시 최고 스택 위에 +objective 1 arm으로만**.
⑤ disjoint: objective는 학습-lane 내부, emit-drive·recall_thr 무접촉. 단 p7 경계 — step-level 신호는 CE 계열이지 gauge/Φ를 loss에 넣는 게 아님을 명시.

### B8. V-포맷×L5 — "소뇌 forward-model, 데이터-채널 결합" (F1×F2, 유일 생존형 F2)
① 1단계($0): 상태-전이 자체를 derivtrace 문법으로 target화(상태+연산→차기상태 trace) — L5를 *포맷으로* 읽기. 2단계(비-$0): 별도 lane에 forward-model을 학습해 그 예측/오차를 **context 토큰**으로 mouth에 공급.
② κ: 상태-전이는 본질적으로 국소(마르코프) → κ≈1 자연 확보 / M: 상태공간 조합 / σ: 연산 축 변주.
③ 곱셈 근거 + 역설 해소: consciousness-ops 비판의 "disjointness=inertness 역설"이 여기 정면 적용된다 — 완전 분리 lane은 INERT(H_1834/1837 재판). 해법: **substrate는 분리하되 결합은 데이터 채널로**(context 토큰) — 데이터 채널은 지금까지 유일하게 INERT가 아닌 채널. 분리=보존(Ψ·G5) ∧ 데이터결합=비-inert를 동시 충족하는 유일 배선.
④ probe: 1단계 포맷판을 B1/B2 fire에 arm 1개로 무임승차 → lift 있을 때만 2단계 lane 설계.
⑤ disjoint: 2단계는 placement-first 심사 필수(lane이 emit-drive 0/4·recall_thr와 disjoint 좌표), lane-OFF ablation으로 INERT 여부 판정(OFF=동일이면 기여 0).

### B9. V2×V8 — "미시-트레이스 × 검산-커밋" (~$0 저위험 보강)
① 각 미시 스텝 뒤 검산(check)→커밋 구조.
② κ: 검산도 국소 / M: 암기자는 검산 값까지 저장 / 부수: G6-인접 정직 구조(스텝별 자기검증)가 데이터에 내재.
③ 곱셈이라기보다 **안전 가산** — V2의 스텝 오류 누적(깊은 trace의 노이즈)을 검산이 차단해 V2의 M∝깊이 스케일링을 실제로 실현 가능하게.
④ probe: B1의 V2 arm 변형으로 1 arm.
⑤ disjoint: 데이터-lane. 검산은 target 내 문자열이지 G5 gate 아님 — 결합 금지 유지.

### B10. V13×L6 — "해상도-사다리 = 내장 커리큘럼" (B4의 특수형)
① coarse→fine 해상도 사다리를 mitosis-grow 스케줄로.
② κ가 사다리를 따라 점진 완화, P_basin은 L6 효과.
③ B4와 중복이 커서 독립 fire 가치는 낮음 — B4가 이기면 자동 흡수, B4가 지면 같이 죽는 종속 후보.
④⑤ B4에 병합 권고.

---

## C. 최소발사 전략 — 조합이 발사 수를 줄이는 3단 구조

**Stage 0 — $0 사전선별이 2^n을 소거한다 (핵심).** 4지표는 *학습 전 코퍼스에서 실측 가능*하므로, 조합 대수의 예측(σ 곱? M 얽힘 vs 분해? κ 수리?)을 **fire 없이 검증**할 수 있다: 후보 스택별 코퍼스를 생성해 ρ/σ/κ/M을 재고, (a) 예측 합성 법칙과 불일치하거나 (b) 두 구성 레버 단독 프로파일을 못 이기는 스택은 그 자리에서 기각. 19레버 2^n 공간이 여기서 한 자릿수로 준다. V12의 σ 붕괴 게이트, B1의 얽힘(M 분해 여부) 게이트, budget 토큰 인플레이션 계수도 전부 이 단계 산출물.

**Stage 1 — 1 fire = multi-arm, max-stack-first + leave-one-out.** 모든 레버가 target 문자열 교체라 arm은 pod 안에서 싸다(발사 수 = pod 렌트 수). full factorial 대신: **최고 스택(ABC) + leave-one-out(AB, AC, BC) + 최강 단독 1 + baseline + budget-matched control** ≈ 7 arm 1 fire. AND 가설에 필요한 건 "맥락 내 한계 기여"이므로 leave-one-out이 2^n을 n+1로 치환한다. 단독들이 이미 marginal(bd=2)임을 아는 지금은 max-stack-first가 정보 기대값 최대 — ABC≈baseline이면 AND 가설 전체가 한 방에 죽고 단독 재발사도 면제된다. budget-match는 필수(H_1836 교훈: budget 안 맞춘 lift는 착시).

**Stage 2 — H_9124 robustness 3분기별 후속 조합.**
- **🟢 (derivtrace 강건)**: M 축을 더 쌓는 국면 — **B1** 발사(+B4 커리큘럼 arm 무임승차). 강한 기반 위 margin 곱셈.
- **🟠 (bd=2 취약/marginal)**: M 추가보다 **실현 계수 수리**가 우선 — **B2**(P_basin×κ) + **B4**(L6은 정확히 marginal 영역 전용 증폭기). B1은 보류.
- **🔴 (robustness에서 붕괴)**: 포맷 단독 축 사망 — 프레임-교차만 생존: **B3**(γ의 $0 probe)로 constructive-bind 가설을 데이터 채널에서 선검증 후, 결과에 따라 γ(H_1840) GPU 발사 또는 하향. B8 2단계도 이 분기에서만.

**엔진-네이티브 게이트(불변)**: 모든 arm 채점은 `anima evaluate --py` 경로(세션 정책), torch-side는 DIRECTIONAL, teardown 전 ckpt PULL, 결과는 H 카드+jsonl 2표면 등록.

---

## 다음 발사 top-3 조합 (단일보다 강한 스택)

1. **B1 = V1×V2×V12 margin-max 3-스택** — derivtrace의 두 병목(작은 M · OUT-치환 κ<1)을 공식의 두 인자(Σ log M · κ)로 동시 타격하는 유일 3-스택. Stage 0 사전선별(특히 V12 산출 σ·M 얽힘 게이트) 통과 조건부, 7-arm 1 fire.
2. **B2 = L2×V2 (성분밀집·조합희소 × 미시-트레이스)** — 유일하게 절반의 DIRECTIONAL 증거(H_6183 밀도 0.95/0.03 · H_6184 RF)가 이미 있는 조합. P_basin×κ 곱을 2×2 팩토리얼 4-arm으로 교호작용까지 한 fire에 판정. 🟠 분기의 1순위.
3. **B3 = V6×V1 다경로합류×스켈레톤** — 4-각 수렴이 남긴 마지막 미검증 가설(γ trained-constructive-bind)을 GPU 지출 전에 데이터 채널로 찌르는 $0-probe. lift든 0이든 γ cost-gate 결정에 직결되는 양방향 정보가치. 🔴 분기의 생존 경로.

공통: **L6 커리큘럼 arm은 어느 fire에든 스케줄-only 변형으로 무임승차**시켜 "marginal 전용 증폭기" 법칙을 같이 사전등록·검증한다.

★check-ledger 준수 확인 — F2는 decode-readout 결합(H_1834/1837 INERT 채널)을 전부 배제하고 데이터-채널/학습-lane 결합(B8)만 남겼으며, objective는 additive-aux 재발사(H_1602 floor)가 아닌 format-노출 step-level 변형(B7)을 최고 스택 위 +1 arm으로만 허용했다. 아키텍처-측 binding 전멸(census)과 B5의 데이터-측 binding은 채널이 달라 벽 재발사가 아니다.