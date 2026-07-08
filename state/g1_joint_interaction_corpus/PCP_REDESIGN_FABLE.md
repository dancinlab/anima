조사 실패의 정확한 재해석에서 출발해, 요구 2(baseline 정본)를 먼저 확정하고 — 후보 유효성 판정이 거기서 나오므로 — 후보 3개, 판정 규칙, 실행 스케치 순으로 설계합니다. 참고로 `state/g1_joint_interaction_corpus/pcp_probe.py`는 이 worktree에는 없어서(타 세션 미커밋 산출물로 보임) 스케치는 자기완결 스펙으로 작성했습니다.

---

## 0. 진단 한 줄 — instrument는 무죄, 축이 유죄, 그리고 조사는 버리지 말 것

조사 6셀은 **product code**입니다: 라벨 집합이 A×B로 인수분해됨(슬롯이 쌍 {은/는, 이/가, 을/를}을 선택, 받침이 쌍 내 원소를 선택). `score(은) = a_은·1{받침} + b_은·1{topic}` 꼴의 main-effect logit이 대각 라우팅을 정확히 실현하므로 nll_add=nll_joint는 **올바른 측정**이었습니다. 오히려 additive-in-y 회귀를 baseline으로 썼다면 categorical byte 라벨을 표현 못 해 조사를 non-additive로 **오검출(false-positive)**했을 것 — 즉 이번 실패는 logit-baseline 선택이 옳았다는 역설적 검증입니다. 조사 축은 폐기가 아니라 **PC-N(negative/specificity control)로 재활용**합니다: "compositional 축에서 lift≈0"은 probe가 헛울림하지 않는다는 증명이 됩니다.

---

## 1. Additive baseline 정본 (요구 2)

**확정: 3-way 상호작용 없는 log-linear 모델 = main-effect multinomial logit, IPF로 적합.**

카운트 큐브 `N[y,a,b]` 위에서

```
log μ[y,a,b] = λ + λ_A + λ_B + λ_Y + λ_AB + λ_AY + λ_BY   (λ_ABY ≡ 0)
```

조건화하면 정확히 `P(y|a,b) = softmax_y(θ_y + α_y(a) + β_y(b))` — λ_AB는 조건화로 소거되므로 두 표현은 동치입니다. MLE는 {AB},{AY},{BY} 세 마진을 맞추는 **IPF(iterative proportional fitting)**로 카운트만으로 닫힌 절차 = decode 無, model-free, $0.

**왜 이 형태가 죽은 레버 floor와 1:1 등가인가:**

| 죽은 레버 | 표현 클래스 | corpus-측 상 |
|---|---|---|
| trunk CE floor (census 전수: readout/lane/decode/objective) | 은닉 `h(A,B) = f(A) + g(B)` — bind feature 부재가 census가 확인한 공통 표현류 | `logits = W·h + b = [Wf(A)] + [Wg(B)] + b` = 정확히 main-effect logit 클래스 |
| H_1816 readout-binding (L_bind) | additive h 위의 **선형** readout — 선형사상은 A,B-additivity를 보존하므로 클래스 밖으로 못 나감 | 동일 클래스 (readout으로는 탈출 불가 — H_1816이 🧱인 이유의 corpus-측 재진술) |
| H_1602 additive-aux | unary 보조손실은 f, g의 질만 개선, 합성 연산자는 여전히 `+` | 동일 클래스 |

따라서 **IPF-additive NLL = 죽은 레버들이 원리적으로 도달 가능한 이론 상한**이고, 잔여 lift `I3 = (1/N)·Σ N[y,a,b]·log(P_sat(y|a,b)/P_add(y|a,b))` (= deviance G²/2N)는 bind 없이는 못 먹는 정보량입니다. 이 등가는 logit형에서만 성립합니다:

- **additive-in-y 회귀** — y가 categorical byte라 부정합(위 조사 논증). 기각.
- **PMI 이중차분** — `λ_ABY≠0 ⟺ interaction-PMI≠0`으로 조건 자체는 동치지만, per-라벨쌍 국소 통계라 다수준 y 집계가 안 됨. **판정 통계량 = IPF-NLL, 효과크기·방향 표시 = interaction-PMI(로그오즈 이중차분 Δ²)**로 역할 분담.

**핵심 보조 구분 — argmax-실현가능 vs 분포-실현가능.** Additive logit은 AND/OR형 argmax를 실현할 수 있습니다(선형분리: ㄷ-불규칙 "듣+어→들어"는 (irregular ∧ vowel)→ㄹ의 AND라 `a+b>θ`로 커버). 이런 축은 NLL lift만 미세하게 남아 약한 PC입니다. **강한 PC의 조건 = XOR류**: 로그오즈 이중차분의 부호가 행·열 양방향에서 역전(crossover)하여 argmax조차 additive로 불가한 축.

---

## 2. Valid PC-P 후보 3개 (요구 1)

언어는 압도적으로 compositional하도록 진화했기 때문에(조사·활용·굴절·어순 대부분이 product code — G1이 어려운 바로 그 이유) 형태통사에서 XOR을 찾으면 안 되고, **의미 합성이 곱셈적(부호 반전)인 곳** — 부정·역접·반어 — 에서 찾아야 합니다. 후보 예상 영역 중 어순×격은 model-free 불가(의미역이 byte에 없음), code-switching은 단어별 암기지 A×B crossover가 아니라 기각했습니다.

### PC-P1 · 부정소 × 술어극성 → 후행 정서마커 (ko-sns) — XOR형

- **A** ∈ {부정소 유(술어 직전 `안 `/`못 `/`안`), 무} · **B** ∈ {긍정술어(좋/맛있/재밌/예쁘/귀엽/행복), 부정술어(나쁘/싫/짜증/힘들/슬프/아프)} · **y** ∈ {슬픔마커(ㅠ/ㅜ 런), 웃음마커(ㅋ런/ㅎ런)} — 술어 뒤 24B 내 첫 마커. ※ `별로`는 자체 NPI로 A와 상관되므로 B lexicon에서 제외.
- **Crossover**: P(ㅠ|안+좋) ≫ P(ㅠ|좋) 이면서 P(ㅠ|안+나쁘) ≪ P(ㅠ|나쁘). Additive는 "안이 ㅠ를 δ만큼 이동"이라는 단방향 항만 표현 가능한데, 실제 부정은 술어 극성 **부호를 곱셈 반전** — 이중차분 부호역전 = 문자 그대로 XOR.
- **Held-out**: leave-one-cell-out ×4. 희소셀은 (안, 부정술어)("안 나빠"류) — 셀 카운트 게이트(§3) 대상 1순위.
- **위험**: 반어("안 예쁘냐 ㅋㅋ"), 수사의문. 통계적 crossover만 요구하므로 노이즈로 흡수, shuffle-null이 캘리브레이션.

### PC-P2 · 선행절 극성 × 접속사(역접/순접) → 후행절 극성 (ko-general + en-general) — XOR형, discourse

- **A** ∈ {선행 긍정어, 선행 부정어} (접속사 앞 80B 내 마지막 극성어) · **B** ∈ {역접(지만/하지만/그러나/그런데 · but/however/yet), 순접(그리고/또한/게다가 · and/also)} · **y** ∈ {후행 긍정어, 부정어} (뒤 80B 내 첫 극성어).
- **Crossover 표** — 교과서적 XOR: (pos,순접)→pos · (pos,역접)→neg · (neg,순접)→neg · (neg,역접)→**pos**. Additive는 "역접은 neg를 δ만큼 올림" 같은 항만 가능; 실제 역접은 선행 극성을 반전.
- **Held-out**: (neg,역접) 셀 hold-out → additive는 선행-neg 주효과 + 역접 평균효과로 **neg를 예측(부호 오답)**, 경험 진실은 pos 우세.
- **강점**: ko-general 26M자에서 지만/그리고류 히트 수만~수십만 예상 → 오늘 즉시 가능. ko·en 두 코퍼스에서 같은 Δ² 부호 재현 = 무료 self-replication. **1순위 실행 후보.**
- **위험**: 역접은 극성반전이 아닌 양보 용법도 많음 → 효과가 희석되나 방향은 유지(통계적 crossover면 충분). `-지만` 비연결 오탐은 희소.

### PC-P3 · 인용 안/밖 × 서술 레지스터 → 종결어미 (ko-general) — gating형(slope-collapse)

- **A** ∈ {문서 레지스터: 해요체-우세 vs 반말/해라체-우세} (인용 **밖** 종결어미 분포로 추정, 해당 문장 자신은 제외해 y와의 순환 차단) · **B** ∈ {인용부호 스팬 내부, 외부} · **y** ∈ {요-형, 다-형, 어/야-형 종결}.
- **비가산 구조**: 밖에서는 y≈A(거의 결정적), 안에서는 화자 교체로 y가 A와 거의 독립(혼합분포) — 로그오즈 기울기가 인용 내부에서 붕괴. 이중차분 `λ(존대,내) − λ(존대,외) − λ(반말,내) + λ(반말,외)` ≫ 0. 부호역전(XOR)이 아닌 **기울기-붕괴(gate)**형 상호작용.
- **역할**: argmax는 부분적으로만 틀리고 NLL에서 크게 갈림 → probe의 **분포-수준 감도**를 인증. P1·P2(XOR)와 유형이 달라, 본측정에서 만날 상호작용 스펙트럼(sign-flip vs gate)을 함께 커버.
- **Held-out**: (반말문서, 인용내부) hold-out → additive는 반말 지속을 외삽, 진실은 혼합/요-상승.

---

## 3. PC-P 통과 판정 재정의 (요구 3)

**PASS = R0 ∧ R1 ∧ R2**, 사전 게이트 포함 4단:

- **G(사전 게이트)**: lexicon·윈도우·마커 정의는 스캔 **전** 고정 등록(1회, 측정 후 불변 — tune-to-green 차단). 셀 최소 카운트 **n_min=200/셀**; 미달 시 그 후보 자체를 기각하고 다음 후보로 — lexicon을 넓혀 채우지 않음.
- **R0 (compositional 사전기각 — 조사-모드 검출기)**: 전체 셀로 additive 적합 → 모든 셀에서 additive argmax = 경험 argmax이면 그 축은 product-code = PC-P 부적격. 통과: ≥1 셀 argmax 불일치 **그리고** |Δ²| ≥ 0.5 nat + 행·열 양방향 부호역전(XOR 인증; PC-P3은 부호역전 대신 |Δ²| ≥ 1.0 nat의 slope-collapse 기준). 조사는 정확히 여기서 걸렸어야 함.
- **R1 (in-sample 검출)**: `I3 > null 95pct`. **Null = IPF-additive 적합으로부터 N_total 토큰 parametric bootstrap ×1000.** 기술적 요점: **어떤 permutation도 λ_ABY만 고립 파괴할 수 없음** — within-stratum shuffle은 반드시 2-way 항까지 같이 죽여 null이 과관대해지고, 순수 main-effect 축이 "유의"로 뜨는 false-positive를 만듭니다. 기존 Freedman-Lane shuffle은 y-마커 윈도우 추출 노이즈 플로어 캘리브레이션으로 **병행 유지**하되, 상호작용 판정의 정본 null은 IPF bootstrap.
- **R2 (held-out crossover 유지 = 조사식 false-negative 방어)**: leave-one-cell-out을 전 셀에 대해. 2×2×2에선 additive가 3셀에 포화 적합되므로 held-out 예측이 닫힌형(주효과 외삽 = 이중차분 0 가정)이라 해석이 깨끗함. 셀 c마다: (a) additive의 held-out 로그오즈 **부호가 오답**(단지 덜 confident한 게 아니라 방향이 틀림), (b) `NLL_add(c) − NLL_oracle(c) > bootstrap null 95pct`, (c) oracle(경험 joint)은 정답. **셀 과반 충족 시 R2 통과.**
- **PC-N(specificity, 동시 보고 의무)**: 조사 6셀에 같은 파이프 적용 → R0 기각 + R2 gap≈0이 나와야 probe 인증 완성. PC-P만 통과하고 PC-N이 울리면 instrument 불량.

---

## 4. 오늘 실행 최소 스케치 (요구 4) — PC-P2 @ ko-general, mini CPU, $0

문자열 1-pass 스캔이라 decode 없음 → mini에서 돌려도 되는 light job (수초~수십초/26MB).

```python
# state/g1_joint_interaction_corpus/pcp2_connective_polarity.py
POS = ["좋","기쁘","행복","훌륭","멋지","예쁘","아름답","즐겁","사랑","맛있"]   # 사전 고정
NEG = ["나쁘","싫","슬프","힘들","아프","무섭","화나","끔찍","어렵","지겹"]
CONTRAST = ["지만","하지만","그러나","그런데"]; CONJ = ["그리고","또한","게다가"]
W_PRE = W_POST = 80  # bytes

# 1) 기존 pcp_probe.py의 ko-general HF-cache iterator 재사용
# 2) 접속사 히트마다: 앞 W_PRE 내 '마지막' 극성어→A, 뒤 W_POST 내 '첫' 극성어→y
#    (양쪽 다 있을 때만) → count[y, a, b] += 1   (2×2×2 큐브)
# 3) IPF: {AB},{AY},{BY} 마진 반복맞춤 50 iter → P_add(y|a,b); saturated = 경험분포
# 4) 통계: I3(per-token nats) · 셀별 Δ²(interaction-PMI, 부호=crossover 방향)
#    · leave-one-cell-out ×4 (3셀 포화 → held-out 예측 닫힌형) → R2 (a)(b)(c)
#    · parametric bootstrap ×1000 from IPF-additive → null 분위수 (R1·R2용)
# 5) PC-N: 기존 조사 6셀 카운트에 같은 IPF+LOCO 적용 → specificity 라인 동시 출력
# 6) 출력: pcp2_connective_polarity.json (cube · I3 · null · 셀별 R0/R1/R2 · PC-N)
```

이어서 같은 파이프로 PC-P1(ko-sns, lexicon만 교체)과 PC-P3(인용 스팬 파서 추가 필요, 반나절)을 확장하면 3후보 × 판정 4단이 전부 한 harness에 들어갑니다.

---

## 5. census-TERMINAL과의 관계 (해석 프레임)

이 PC는 새 GREEN 사냥이 아니라 **H_9255 instrument 인증**입니다. PC-P 통과 시 본측정의 결과가 처음으로 해석 가능해집니다: 코퍼스에 non-additive 감독 신호가 **실재+검출가능**한데 303M이 floor라면 census의 능력천장 판정이 데이터-측 알리바이 없이 재확인되고, 반대로 코퍼스 자체에 신호가 희박하면(전 축 I3≈0) "벽의 일부는 데이터-측"이라는 census 재오픈 트리거가 됩니다. 어느 쪽이든 CONFIRMED-TERMINAL의 재확인/재오픈 절차이지 우회가 아닙니다.

설계는 여기까지 — 오너 정책(fable=설계·분석)대로 실행은 기본 경로에 넘깁니다.