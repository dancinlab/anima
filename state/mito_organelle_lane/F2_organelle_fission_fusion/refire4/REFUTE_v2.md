<!-- @canonical-ok — 오케스트레이터가 지정한 산출물 경로(refire*/REFUTE_v2.md · 1차 REFUTE.md와 별개 문서) -->
# REFUTE_v2 — H_9274 4차 (a_comp / slack 상보성) 적대적 검증

판정: **INVALID 유지 · 결론의 실질주장(“담체가 오라클급 정보를 나른다 — 결정적”)은 REFUTED.**
결함은 담체(3차)→통제(4차)로 **전진하지 않았다.** 담체 자체가 헤드라인 detector의 닫힌형 argmax다.

---

## R1 (치명) — a_comp = 헤드라인 detector의 greedy argmax (처치-detector 공선성)

보존적 융합에서 cap·D가 더해지므로 L, S 둘 다 가산. 융합 i,j의 헤드라인 순간이득은 닫힌형:

    ΔATP = max(0,−a) + max(0,−b) − max(0,−(a+b)),   a=slack_i=S_i−L_i, b=slack_j
         = 0                     (a,b 동부호)
         = min(|a|, b)           (a<0<b)

⇒ ΔATP의 argmax = (가장 음의 slack) × (가장 양의 slack) = **a_comp 선택규칙 그 자체.**

실측(run.py 실코드 in-situ 계측 · HET · seed 0–2 · 융합 1,800건 · 평균 적격쌍 52):

| 항목 | 값 |
|---|---|
| a_comp 쌍 == 순간 헤드라인 ΔATP의 **정확한 argmax** | **1,722/1,800 (95.7%)** |
| 전 적격쌍 중 a_comp 쌍의 평균 순위(1=최적) | **3.45 / 52** |
| 획득 ΔATP / 획득가능 최대 ΔATP | **0.980** |

(100%가 아닌 것은 sibling-ban compat 제약·동률뿐.) 헤드라인 지표를 만드는 바로 그 두 양(L,S)으로
헤드라인의 기울기를 타는 정책은 통제를 **정의상** 이긴다. 이것은 발견이 아니라 대수다.
run.py 헤더는 이 위험(“detector 근접성”)을 스스로 인지하고 “정상상태 동역학이 개입하므로 열린 질문”
이라며 기각했다 — R2가 그 기각을 반증한다.

## R2 (치명) — 기질을 전부 삭제해도 신호가 그대로 재현된다 (알고리즘 항등식)

손상·복구·drift·stress 되먹임·분열·시간·Λ·fragility **전부 제거**. 임의의 감마난수 L,S(모델과 무관)
16유닛, 융합 4회, 같은 두 정책만:

    comp − blind 헤드라인 ATP Δ = **+11.790 ± 0.335 (SEM), 200/200 seed 양성**

주장된 “a_comp − a5_sham = +11.786±0.637”와 **사실상 동일 크기**. 즉 +13.7/+11.8은
`ATP = Σ min(L,S)`가 pooling 하에서 갖는 submodular 항등식이지, 기질·재조합·정보의 성질이 아니다.
(스크립트: `scratchpad/nullsub.py`, `scratchpad/taut.py`)

## R3 — 물리 불변량에 이득이 0 또는 **음수** (이득은 100% 파티션 회계)

ΣL = 100(질량보존, 전 arm 동일). ΣS는 보존적 merge(G1 pump=0)로 arm 간 동일.
전 arm n_units=16 고정. ⇒ **arm 간 자원 풀은 동일**하고 ATP 차이는 파티션 장부뿐.

| arm | HET atp / health / supply / overload | LIVE atp / health / supply / overload |
|---|---|---|
| c2_blind | 57.46 / 0.8053 / 94.736 / 0.288 | 48.83 / 0.7003 / 82.390 / 0.331 |
| **a_comp** | **71.15** / 0.8053 / 94.740 / **0.314** | **62.75** / **0.6954** / **81.817** / **0.443** |

HET: health·supply **불변**(3자리까지 동일). LIVE: supply −0.57, health −0.005, overload **+0.11**
= 물리적으로 **더 나쁘다**. 헤드라인만 +13.9. 보고서는 “health 불변 ⇒ 담체가 상보성이지 health 아님”을
**긍정** 증거로 읽었으나, 파티션-불변 상태변수에 아무 개선이 없다는 것은 그 이득이 **비물리적 회계**라는
증거다. guard_off(동일 comp 정책, 가드만 해제)가 88.3(+17)인 것도 같은 방향 — 지표는 장부 churn에
반응한다.

## R4 — 규칙⑥ 부호보존(가장 강한 증거로 제시됨)은 **여기서 비변별적**

R1–R2의 항등식은 repair·sigma·capsplit·rho·frag_sigma·EXC·B1 어느 것에도 의존하지 않는다.
따라서 “전 자유축 전 점 부호양성(signs={1})”은 실체의 서명이 아니라 **동어반복의 서명**이다.
사전예측 “slack은 L을 포함하니 기질무관 보존” 적중도 같은 이유로 무의미하다(대수는 원래 기질무관).
**미열거 자유축**: detector 형태축 — DV를 파티션-불변량(supply/health/overload)으로 바꾸면
효과가 0 또는 부호역전(R3). 이 축이 PASS 조건에 없다 = 규칙⑥ 미충족(열거 누락).

## R5 — 게이트 배터리에 “처치 ⟂ detector 기울기” 게이트가 없다 (누락 통제)

규칙④ 정보채널 게이트(`slack_sel_ratio` 3.70)는 **오히려 공선성을 인증**한다: 처치 DV(slack)가
헤드라인의 인수(L,S)로 만들어졌음을 확인해줄 뿐이다. POWER(6.99×MDE)·ORACLE-REACH(+13.4)도
같은 항등식이 만든 span이라 공허(vacuous)하다. 필요한 통제는 **a_detgrad = 순간 ΔATP argmax arm**
이며, a_comp는 그것과 98% 동일(R1)하므로 이 통제를 넣으면 처치효과 ≈ 0이 된다.
sham 수리(V_sham_distinct FAIL)로는 이 결함을 **구제할 수 없다.**

## R6 — “sham−blind=+1.9 ⇒ 순수구조 이득 상한 ~+2” 추론 무효

sham의 구조는 (붕괴된) tag-극단 반복이지 detector-기울기 구조가 아니다. 무관한 arm으로 “구조 이득의
상한”을 정할 근거가 없다. R2는 기질정보 0으로도 +11.8이 나옴을 보인다 ⇒ 상한 주장 반증.

## R7 — “오라클 천장 도달”은 성립하지 않음

a_comp(71.15) > o6_oracle(70.89) HET, 62.75 > 61.89 LIVE. **처치가 상한 계측기를 넘었다** =
o6는 천장이 아니다(모델-예측 정상상태의 근시 greedy일 뿐). 따라서 “오라클 천장 도달”은 도달 증명이
아니라 계측기 실격 신호다.

---

## 체크리스트 판정 (공정 배점)

| # | 항목 | 판정 |
|---|---|---|
| 1 | 헤드라인 순서통계량? | **위반 없음** — 사전등록 = control별 paired-t 2개 모두(min/max·Δ=exp−max 미사용). 규칙①⑤ 준수 |
| 2 | 사후 detector/변수 교체? | **4차 내부 없음** — sham FAIL을 완화하지 않고 INVALID 유지(F8/F13 회피 성공). 단, 3차→4차에서 **처치**를 detector의 argmax로 교체(신규 prereg지만 R1 공선성을 낳음) |
| 3 | 새 seed/fresh data? | fresh 실행 O · pilot 900–919 disjoint O (main seed 0–19은 통제 arm 재시뮬 — 무해) |
| 4 | 부호보존 설계내장? | 내장 O, **그러나 비변별(R4)** + 미열거 축(detector 형태) 존재 |
| 5 | sham ≠ blind? | **FAIL(자인)** — tag_gap 0.000 vs 0.0015 (sham이 blind보다 오히려 낮음: tag 동질화 → 결정적 저-index picker) |
| 6 | Δ=max(controls)? MDE 인과축? 정보채널? | Δ 순서통계량 미사용 O · MDE/POWER는 항등식 span이라 **공허** · 정보채널 실재하나 **detector 공선성 인증**(R5) |
| 7 | 인프라벽→과학 verdict? parity? | 해당 없음($0 numpy CPU) · 위반 없음 |

## 결론

- **형식 판정 = INVALID 유지** (사전등록 hard-gate V_sham_distinct_from_blind FAIL).
- **실질 결론 = REFUTED**: “재조합 대수가 부호불변·국소도달·오라클급 정보를 나른다는 것이 결정적으로
  나타났다”는 성립하지 않는다. 헤드라인 +13.7/+11.8은 `Σ min(L,S)`의 pooling 항등식이며(R1·R2),
  파티션-불변 물리량에는 이득이 없거나 음(R3)이다. 다른 결과가 나올 수 **없는** 측정은 증거가 아니다.
- **“결함이 담체→통제로 한 칸 전진” = 반박.** 결함은 여전히 **담체/detector 축**에 있다.
  sham을 고쳐도 a_comp는 detector의 기울기이므로 PASS는 무의미하다.
- **다음 발사가 만족해야 할 조건(사전등록용)**: (a) DV를 **파티션-불변량**으로(정상상태 supply·health·
  overload·생존시간 등 — Σmin(L,S) 금지), 또는 (b) `a_detgrad`(순간 ΔATP argmax) arm을 **통제로 추가**
  하고 a_comp가 그것을 유의하게 넘어야 PASS. 둘 다 없으면 이 레인은 항등식을 계속 재발견한다.
- tune-to-red 아님: 4차가 sham FAIL을 자인하고 완화하지 않은 것은 규율 준수로 인정. 반박은 **수확(+13.7)의
  해석**에 대한 것이지 정직성에 대한 것이 아니다.
