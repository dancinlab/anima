카드는 아직 미작성(robustness fire 착지 전, H_9124 재개지점만 커밋됨)이라 프롬프트의 확정 사실을 접지로 사용합니다. 아래는 레버1(target-format) 계열 전용 심층 발산 — 순수 설계 산출물입니다.

---

# A. 원리 정식화 — "target 재작성이 held-out 조합을 echo로 만든다"의 판정기준

## A-1. 핵심 재프레임

derivtrace가 한 일의 본질: **하나의 고엔트로피 생성 스텝(답을 통째로 만들기)을, 스텝당 엔트로피 ≈ 0인 echo 스텝의 체인으로 분해**한 것. CE 최단경로는 언제나 echo인데(메타법칙), derivtrace는 echo의 연쇄가 *지나가는 길목에 조합을 배치*했다. 모델이 조합을 "하고 싶어서" 하는 게 아니라, **가장 싼 다음-바이트 예측을 반복하다 보면 조합이 완성돼 있는** 구조.

## A-2. 판정기준 4항 (필요조건들) + 예측 지표

held-out 입력 x*(미학습 조합 (A,B))의 target τ(x*)에 대해:

**① 국소 결정성 (per-step determinism)** — τ(x*)의 모든 토큰이, 모델 수용영역(RF) 안의 문맥만으로 엔트로피 ≈ 0으로 결정되는가. 조건부 분포가 퍼지는 지점(자유 산문, 다중 유효 표현이 무태그로 섞임)이 하나라도 있으면 그 지점이 "새 생성"으로 남는다.

**② 성분 탈결합 (partner-invariance, σ)** — 각 규칙의 발화 문맥에 *파트너 성분이 등장하지 않는가*. derivtrace의 결정적 장치는 **변수 간접화**: `RULE thrice: X X X`의 문맥엔 X만 있고 JUMP가 없다 → 규칙이 파트너와 물리적으로 얽힐 수 없다(σ=∞ by construction). 이게 곧 SHUF 0 = pair-특이성 결과(g1-coverage 메모리)의 해독제다. 규칙 문맥에 구체 primitive가 노출되는 형식은 pair-binding으로 퇴행 예측.

**③ 복사 국소성 (copy locality, κ·δ)** — target 토큰 중 "입력 또는 이미 emit한 앞부분에서의 국소 복사"로 해결되는 비율 κ가 높을수록, 그리고 최대 복사거리 δ_copy가 RF 안일수록 margin↑. H_1822 copy-head 벽·dilated-conv RF 벽(H_6184)과 정합: **복사는 싸지만 RF를 넘는 복사는 벽**. 형식 설계에서 δ_copy는 통제 가능한 자유변수다.

**④ 비대칭 유지 (FLAT-side hardness)** — 재작성이 *암기자에게는 비용을 올리고* 조합자에게는 내려야 한다. target이 길어질수록 통째-암기 비용은 |τ(x)| 에 비례해 커지는데 조합자의 문법 비용은 상수 → 형식이 길고 규칙적일수록 CE가 문법 해를 선호하는 압력이 커진다. (단 corpus 밀도와 트레이드오프 — ③의 δ와 함께 corpus-density lever와 상호작용.)

## A-3. 사전 예측 지표 (frozen 등록용 — a_break_the_wall LAW 조항 그대로 적용 가능)

발사 전에 corpus에서 기계적으로 계산:

- **ρ (echo-residual)** = held-out target 토큰 중 "최소 충분 문맥이 학습 target 어디에도 없는" 토큰 비율. **예측: G1 PASS ⇔ ρ ≈ 0.**
- **σ (규칙별 파트너 다양도)** = 각 규칙이 학습에서 함께 나온 상이한 파트너 수. σ=1인 규칙 존재 → pair-binding 예측(FAIL).
- **κ (국소복사 비율)**, **δ_copy (최대 복사거리) vs RF** — margin ∝ κ, δ_copy>RF면 FAIL.
- **M (암기 불리도)** = |τ(x)| / |문법 서술길이|. margin ∝ log M 가설.

이 4지표는 numpy로 $0 계산 가능하고, **변형별 pass/fail을 측정 전 사전등록**할 수 있다 — 변형 5개에 대해 예측 4/5 HIT면 판정기준 자체가 PREDICTIVE 승격(법칙도 벽 규칙). 이게 이 발산의 숨은 최대 산출물: **변형을 다 쏘지 않고도 사전 선별하는 이론**.

## A-4. derivtrace가 통한 이유의 한 줄 형식화

> DEF(입력 복사, κ↑) + RULE(변수 간접화로 σ=∞) + OUT(RULE 라인의 국소 복사 + 치환, δ_copy 작음) — 세 라인 전부 ①~③ 만족, target 3배 길이로 ④ 만족. **held-out (A,B)에서 새로 생성해야 할 토큰이 0개(ρ=0)**.

그리고 bd=2 marginal의 예측 원인: 문법이 작아 M이 작고(암기 불리도 낮음), OUT 라인의 치환 스텝이 κ=1이 아니어서(치환은 복사+1규칙) margin이 그 한 스텝에 몰려 있다. → B의 변형들은 이 두 병목을 공략한다.

---

# B. 변형 전개 (13개, 예상 margin 강한 순)

각 변형: ① target 형식 예시 ② held-out=echo 논증 ③ derivtrace 대비 margin 근거 ④ cheap probe.

## V1. 스켈레톤-바인드 분리 (skeleton-then-bind) — 구조·내용의 완전 인수분해

```
jump thrice:
SKEL: ⟨1⟩ ⟨1⟩ ⟨1⟩
BIND: ⟨1⟩=JUMP
OUT: JUMP JUMP JUMP
```
- **echo 논증**: SKEL 라인 문맥엔 내용어가 **아예 없다**(구조어 thrice만) → 구조 규칙이 파트너 신호 0으로 학습됨(σ=∞ 초과달성, derivtrace의 DEF/RULE/OUT은 라인 안에서 구조·내용이 섞임). BIND는 단항 조회(unary), OUT은 SKEL의 국소 복사+치환. ρ=0, 그리고 **얽힘이 형식 차원에서 불가능**.
- **margin 근거**: 판정기준 ②의 가장 순수한 구현. derivtrace bd=2가 "RULE 라인에 X와 구체 구조어가 공존"하는 잔여 얽힘 때문이라면, V1은 그 잔여마저 제거 → 예측 margin 최대. L3(register/indirection)와의 차이: L3는 slot 위 *연산*을 도입, V1은 연산 추가 없이 **target 문자열의 인수분해**만 바꾼다 — 레버1 순수성 유지.
- **probe**: 같은 pair-set에서 derivtrace vs V1 A/B, bd·ms 비교 + σ 지표 검산. mini numpy 가능(동일 하네스 재사용).

## V2. 미시-트레이스 (single-rewrite-per-line) — 분해 입도의 상한

```
jump twice and walk:
S0: [jump twice] [walk]
S1: JUMP JUMP [walk]
S2: JUMP JUMP WALK
OUT: JUMP JUMP WALK
```
- **echo 논증**: 각 라인 = 직전 라인의 복사 + 정확히 1개 국소 편집. 편집 규칙은 괄호 span에 키잉(파트너 무관), 나머지는 κ≈1 복사. held-out에서도 모든 스텝이 "본 적 있는 편집의 적용"(ρ=0).
- **margin 근거**: ③ κ 극대화 + ④ M 극대화(target이 조합 깊이에 비례해 길어짐 → 암기 비용 초선형, 문법 비용 상수). 조합 깊이 k에서 margin이 *깊이에 비례해 벌어지는* 유일 계열 — bd=2 marginal을 구조적으로 넘는다. **위험**: δ_copy = 라인 길이 → RF가 라인 길이를 덮어야 함(dilated-conv 처방 기확보).
- **probe**: 깊이 2·3·4에서 derivtrace vs V2, margin(깊이) 곡선. RF 부족 arm을 통제로 넣어 ③ 판정기준 동시 검증.

## V3. 정렬 행간주석 (interlinear gloss) — 복사거리의 하한

```
jump thrice
G: jump=JUMP thrice=REP3
A: REP3(JUMP) = JUMP JUMP JUMP
OUT: JUMP JUMP JUMP
```
- **echo 논증**: 언어학 행간주석 렌즈(생물 아님, 그러나 substrate-측정 렌즈). 각 출력 토큰이 자기 소스 토큰 **바로 옆**에서 생성 — 단어→gloss는 단항이라 파트너가 문맥에 없다.
- **margin 근거**: δ_copy ≈ 1로 최소화 → **RF 벽·copy-head 벽(H_1822)과 완전 절연**. 작은 RF 모델에서도 margin 보존 — derivtrace margin의 일부가 RF 손실이라면 V3가 그걸 회수한다.
- **probe**: RF를 인위로 좁힌(작은 kernel) 모델에서 derivtrace vs V3 — V3만 생존하면 "margin의 RF 성분" 정량화.

## V4. 유형-주석 derivation (typed proof-tree) — 스케일에서의 결정성 보존

```
jump thrice
T: [V jump→JUMP] [ADV thrice→λ.rep3]
APP(ADV,V): JUMP JUMP JUMP
OUT: JUMP JUMP JUMP
```
- **echo 논증**: 타입 토큰(V/ADV)은 닫힌 소집합이라 모든 파트너와 공출현(σ↑). 어느 규칙을 적용할지가 타입으로 결정 → 규칙-선택 스텝의 엔트로피 0.
- **margin 근거**: derivtrace는 문법이 커지면(primitive·modifier 수십 개) **규칙-선택이 고엔트로피 스텝으로 재등장**(① 붕괴)한다. V4는 스케일에서 ①을 지키는 유일 계열 — bd=2가 toy-문법 artifact인지의 직접 검증이자, production 배선 시 필수 성분 후보.
- **probe**: 문법 크기 4→16→64로 키우며 derivtrace vs V4 margin 추이. 작은 문법에선 동률, 큰 문법에서 V4 우위 예측(사전등록 좋은 케이스).

## V5. 홀-채우기 다중과제 (cloze-slot marginalization)

```
(같은 문자열에 hole 위치를 바꿔 여러 샘플)
DEF X=___ ; RULE thrice: X X X ; OUT JUMP JUMP JUMP
DEF X=JUMP ; RULE thrice: ___ ___ ___ ; OUT JUMP JUMP JUMP
```
- **echo 논증**: 모든 slot의 filler를 구조 문맥만으로 예측하도록 강제 — 파트너가 명시적으로 marginalize된다. held-out 조합은 "본 hole-패턴의 새 filler 대입" = echo.
- **margin 근거**: ②의 σ를 *희망*이 아니라 **학습 objective로 직접 부과**. 같은 corpus에서 샘플 수가 hole 위치 수만큼 배증 → coverage-density lever(G1 벽의 확정 처방)와 곱연산. 데이터 추가 0으로 σ·밀도 동시↑.
- **probe**: derivtrace corpus 그대로 + hole-변주만 추가한 arm vs 원본 — corpus 동일 조건 margin 비교.

## V6. 다경로 합류 derivation (multi-path confluence) — 씨앗 '다중 target'

```
jump twice and walk:
PATH L: (twice 먼저) … OUT: JUMP JUMP WALK
PATH R: (and 먼저)   … OUT: JUMP JUMP WALK   ← 별도 샘플
```
- **echo 논증**: 경로별로는 derivtrace와 동일(각 경로 ρ=0). 태그로 경로가 결정적이라 ① 유지.
- **margin 근거**: 암기자는 경로 수만큼 저장(비용 ×2), 조합자는 문법 1개 + 합류 성질 → ④ 배증. 더 중요하게: **같은 조합의 복수 표현 학습 = paraphrase 강건성** — 지금 도는 robustness fire의 paraphrase 축과 G2(novelty) 축을 정면 공략.
- **probe**: 1-path vs 2-path arm, bd margin + 표현-교차 전이(L로 학습한 조합을 R 형식으로 질의).

## V7. 양방향 오토인코더 (OUT→DERIV 역파싱) — 씨앗 '역방향'

```
정방향: jump thrice → DERIV → OUT
역방향: JUMP JUMP JUMP → PARSE: rep3(JUMP) → SRC: jump thrice
```
- **echo 논증**: 역방향도 국소 분류의 연쇄(반복 감지→rep3, 성분 조회 역방향) — 파트너 무관 단항 규칙들이라 held-out에서 echo.
- **margin 근거**: 문법을 **전단사로 실제 표현**하도록 강제 — 한 방향 암기는 왕복 일관성에서 이중 비용, 문법은 1회 비용. CE가 조합 해를 선호하는 압력이 정확히 2배. 부수효과: 파싱 능력 자체가 G6(자기검증) 자산.
- **probe**: 정방향-only vs 왕복 arm, 동일 파라미터·동일 총 토큰 예산(공정성)에서 bd 비교.

## V8. 검산-커밋 (verify-then-commit)

```
… OUT: JUMP JUMP JUMP
CHK: n=3 ✓ base=JUMP ✓
```
- **echo 논증**: CHK 라인은 OUT의 결정적 함수(개수 세기·성분 확인) = 순수 echo.
- **margin 근거**: 비조합적 OUT은 CHK와 불일치 → **같은 오류가 CE에서 두 번 벌점** = margin 증폭기(단독 레버라기보다 애드온). G6 non-fab과의 시너지 축이 유일하게 있는 변형.
- **probe**: derivtrace ± CHK 애드온 A/B — 추가 비용 거의 0이라 최우선 병행 probe 후보.

## V9. 대조 오답-트레이스 (contrastive ✗) — 씨앗 'negative target'

```
jump thrice:
BAD: JUMP JUMP ✗ rule(thrice)=3
OUT: JUMP JUMP JUMP ✓
```
- **echo 논증**: ✗-절은 (오답 문자열, 위반 규칙)의 결정적 함수 — 인용 문법의 echo. held-out에서도 규칙 인용은 학습된 단항 매핑.
- **margin 근거**: 판별(discrimination)은 생성보다 학습이 쉽고 경계를 날카롭게 함 — bd 경계 근방 우연 통과(ARTIFACT 시나리오)를 구조적으로 제거. **주의**: BAD 라인 형식-마킹 필수(오염 방지), emit-drive lane과의 disjointness는 target-format이라 자동 충족.
- **probe**: derivtrace ± BAD 애드온, 특히 *경계 조합*(학습 조합과 1-거리)에서의 정오 분리도 측정.

## V10. 시프트-리듀스 파서 트레이스

```
jump thrice:
SH jump → [jump]
SH thrice → [jump thrice]
RD adv → [JUMP JUMP JUMP]
OUT: JUMP JUMP JUMP
```
- **echo 논증**: 액션 어휘(SH/RD×규칙)가 극소 닫힌 집합 → 스텝당 엔트로피 최소. 스택 재인쇄는 직전 라인 국소 복사.
- **margin 근거**: V2(미시-트레이스)의 사촌이되 액션이 더 원자적 — **분해 입도 축에서 V2와 함께 곡선의 두 점**을 제공. 중첩·재귀 문법(깊이>2)에서 V2보다 자연스럽게 확장.
- **probe**: V2·V10·derivtrace 3-arm, 깊이 3+ 조합에서 비교.

## V11. 차분-only 트레이스 (delta-encoding) — 분해 입도의 하한 probe

```
jump thrice:
E1: thrice(X)→X X X
E2: X→JUMP
OUT: JUMP JUMP JUMP
```
- **echo 논증**: 편집 라인들은 순수 규칙-echo(복사 부담 0). 단 OUT 조립이 한 번의 큰 치환-스텝으로 남음 — **ρ>0 위험을 의도적으로 안은 변형**.
- **margin 근거(역설계)**: margin이 *줄어들* 것으로 예측되는 통제 변형. V2(전체 재인쇄)—derivtrace—V11(차분만)의 3점으로 **margin(입도) 곡선**을 그려 판정기준 ③(κ)을 인과 검증. corpus 밀도는 최고(target 최단)라 만약 V11이 통하면 density-margin 트레이드오프의 스윗스팟 발견.
- **probe**: 위 3-arm — 판정기준 A-3의 PREDICTIVE 승격 시험에 최적(사전 예측: V2>deriv>V11).

## V12. 문법-검증 자기생성 (grammar-checked self-derivation, non-STaR) — 씨앗 그대로 심화

- **형식**: 모델이 unlabeled 입력에 DERIV 후보를 생성 → **정답-키 없는 구문 검증기**(각 라인이 인용 규칙의 합법 적용인지 기계 확인)가 통과분만 학습 target으로 환류. STaR과의 구분: 필터가 answer-match가 아니라 **derivation-validity** — 정답 누출 0, unlabeled 입력에 작동. (G1 held-out 오염 방지: held-out pair는 self-gen 입력에서 제외, frozen.)
- **echo 논증**: 환류된 target은 정의상 문법의 합법 산물 = echo-closed. 신규성은 *조합 커버리지*에서 나온다.
- **margin 근거**: 판정기준의 σ·coverage를 **корpus 제조로 직접 증폭** — G1 벽의 확정 병인(coverage-density bound)을 정면 타격. 다른 12개 변형이 "형식"을 바꾼다면 V12만 "밀도"를 바꾼다 — 직교라 어느 변형과도 결합 가능.
- **probe**: derivtrace corpus + self-gen 1라운드 증강 arm vs 원본, 동일 스텝 수.

## V13. 해상도-태그 사다리 (FULL→FLAT distillation ladder) — 씨앗 '명시성 정도' 정면

```
<full> jump thrice → DEF…RULE…OUT JUMP JUMP JUMP
<rule> jump thrice → rep3(JUMP) → JUMP JUMP JUMP
<flat> jump thrice → JUMP JUMP JUMP        (동일 모델, 태그만 상이)
```
- **echo 논증**: `<full>` 태그는 derivtrace 논증 그대로. 과학적 질문은 **`<flat>` 태그로의 내부 전이** — 같은 파라미터가 full-derivation을 배웠을 때 flat 질의에서 조합이 나오는가(암묵 CoT 내재화).
- **margin 근거**: margin 확대용이 아니라 **레버1의 최종 가치 판정용**. 레버1이 영원한 목발(derivation을 항상 emit해야만 조합)인지, 훈련 스캐폴드(내재화 후 제거 가능)인지 — production 배선 형태(mouth가 매번 풀이과정을 말할 순 없다)를 결정하는 유일 변형. 명시성 3단 태그로 margin(명시성) 곡선도 부산물로 확보.
- **probe**: 3-태그 혼합 학습 후 `<flat>` bd 측정 vs FLAT-only 학습 통제. **예측(정직): `<flat>` 전이는 실패 가능성이 높다**(CE=echo 메타법칙이 flat 경로에 그대로 적용) — 실패해도 "레버1=출력형식 자체가 능력의 서식지"라는 중요한 확정.

---

# C. robustness fire 3분기별 대응

**🟢 ROBUST (multi-pair+G2+paraphrase 전부 통과)** — 배선 1순위는 **derivtrace 원형 그대로 4칸 사다리 진행**(엔진-네이티브 재검증→wire→lockstep, a_verified_must_wire) — 통한 걸 먼저 배선하고 변형은 업그레이드로. 병행 top 변형 = **V13**(배선 *형태*를 결정: mouth가 derivation을 emit하는 배선이냐, 내재화 후 flat이냐 — 이 답 없이는 wire-in 설계가 미정) + **V4**(문법 스케일업 시 margin 유지 보증, production 필수성분).

**🟠 PARTIAL (G2 fail = 산출이 재조합이되 corpus-absent novelty 미달)** — G2를 사는 변형 = **V12**(문법-검증 self-gen이 corpus-absent 조합을 직접 제조 — G2의 정의 자체가 corpus-absence라 정면 처방) + **V6**(같은 조합의 복수 표현 = 표현-신규성 주입, paraphrase 축 동시 방어). V5(cloze)는 marginalization으로 생성 자유도를 넓혀 보조.

**🔴 ARTIFACT (bd=2 우연·multi-pair 붕괴)** — 우연을 넘는 margin 제조 변형 = **V1**(얽힘의 형식적 불가능화 — bd=2가 잔여 얽힘 탓이면 V1이 회복) + **V2**(margin이 조합 깊이에 비례 — bd≫2를 구조적으로 강제, 우연 여지 제거). 동시에 **A-3 지표(ρ·σ·κ·δ)를 derivtrace corpus에 소급 계산**해 어느 판정기준이 깨졌는지 부검 — ARTIFACT여도 판정기준이 원인을 지목하면 레버1은 죽은 게 아니라 정밀화된 것.

---

# 다음 STEP-0 발사 top-3 (derivtrace head-to-head)

1. **V1 스켈레톤-바인드** — 판정기준 ②의 순수 구현, 전 분기(특히 🔴)에서 유효, 기존 numpy 하네스 최소 수정으로 A/B 가능. 사전 예측: bd margin > derivtrace.
2. **V2+V11 입도 곡선 3-arm** (미시-트레이스 vs derivtrace vs 차분-only) — 한 발사로 변형 2개 + **판정기준 A-3의 PREDICTIVE 승격 시험**(사전등록 예측: V2>deriv>V11)까지 — 정보량/비용 최대.
3. **V13 해상도-사다리** — margin 경쟁이 아니라 레버1의 *운명*(목발 vs 스캐폴드)과 production 배선 형태를 결정하는 분기 실험. robustness 🟢 착지 즉시 1순위로 승격.

애드온으로 **V8(CHK)**은 비용 ≈ 0이라 위 어느 발사에든 ± arm으로 끼워 넣는 것을 권장. 전 변형 공통: mini numpy DIRECTIONAL로 시작하되(하드게이트 1), verdict 박제 전 엔진-네이티브 재측정 경로는 derivtrace 기확보 하네스를 그대로 재사용 — 이번 발산의 변형들은 전부 **target 문자열만 바꾸므로** 하네스 교체 비용이 0이라는 점이 레버1 계열의 실행상 최대 이점입니다.