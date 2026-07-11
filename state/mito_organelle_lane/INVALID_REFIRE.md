# INVALID 3건 재발사 — 종합

범위: F1/H_9273 (ATP 에너지 경제) · F2/H_9274 (분열-융합 대수) · F8/H_9280 (언커플링 열발생).
셋 다 원판정이 INVALID(채점 불가)여서, 지목된 결함을 코드로 수리해 재발사한 결과의 종합이다.
전 3건 toy numpy · $0 · engine-native 0 (⇒ 통과했더라도 tier 상한은 DIRECTIONAL).

---

## 1. 한 문장 결론

**해소되지 않았다 — 3/3 여전히 INVALID(채점 불가).** 지목된 원 결함은 세 건 모두 코드로 진짜 수리됐고
(tune-to-green 흔적 0) 그 과정에서 **원 판정 3건이 모두 아티팩트로 반증**됐지만, 세 재발사의 헤드라인은
**부호를 뒤집는 미등록 자유 상수의 한 점**(F1=짝짓기 축·조건별 지출매칭 / F2=repair sink 상수 / F8=Q_CEIL)에
걸려 있어 licensed 결과를 얻지 못했다 — 결함이 사라진 게 아니라 **한 칸 옆으로 이동**했다(동형 재발).

---

## 2. 전수 표

| 패밀리 | 원판정 | 고친 결함 (코드로 확인) | 재발사 verdict | 핵심 Δ + paired-t | 한 줄 근거 |
|---|---|---|---|---|---|
| **F1 / H_9273**<br>ATP 에너지 경제 | INVALID<br>(원 PASS조건 구조적 불가 · 검출력 0 · 항진적 처치 · c1≡c2 byte-identical · p5 dead-code) | R1 pilot-MDE 사전게이트(seed 100–105, main과 disjoint) · R2 demand를 supply에서 외생화(라우터 원점수 함수, ATP 미수취) → binding_rate 0.528 · R3 비가산 기질(topic×polarity, 선형 지름길 = 최빈 baseline 0.5173 vs 0.5174) · R4 c1(static cap) ≠ c2(permuted-k) 실측 4.3pp · R5 emit_decide에 atp 실주입 → illegal_channel_closed 20/20 · R6 원 PASS조건 구조적 달성불가 자진 공시 | run=THEATER<br>**verify=REFUTED → STILL INVALID** | 헤드라인 EXP−c5_nobank = **−0.0007±0.0014, t=−0.53, p=0.60, 9/20 (ns)**<br>EXP−c2_perm_k = +0.0242, t=+11.37, 20/20<br>EXP−c1_static = −0.0190, t=−8.36<br>bursty EXP−c5 = −0.0288, t=−13.24 | 헤드라인을 만드는 **유일한 대비(EXP vs c5)가 두 다리 다 무효**: iid는 분포적 항등식(인과 저수지 aff_t=g(dem_<t) ⇒ iid에서 aff_t ⊥ dem_t 강제 ⇒ Δ=0은 측정이 아니라 정리), bursty는 지출 미매칭(EXP 3.6416 vs c5 3.8674 = +6.2% ATP, paired t=−34.9; static-k 기울기 12pp/k × Δk 0.226 ≈ 2.7pp가 관측 −2.88pp의 거의 전부) |
| **F2 / H_9274**<br>분열-융합 | KILL<br>(부분양성 a3 +0.157) → INVALID | 미등록 연산자 대수 제거: 병변 bool→연속장 L∈[0,1]^32, FUSION = capacity-weighted **average**(희석), FISSION = σ-비대칭 **격리**(질량보존) · **대수 중립성** ops_supply_created ≤3e-14 전 arm (원 대수 D1로 돌리면 펌프 +507.4(c2) ~ +608.9(a3)/run) · self_remerge 42.8%→0.000 (sibling-ban + COOL=2) · a3 PRIMARY 사전등록 · pilot-MDE(seed 900–904) · max(controls) 0회 | run=THEATER<br>**verify=REFUTED → STILL INVALID** | 헤드라인 a3−a5_sham = **−0.03±0.18, t=−0.19, p=0.855, 9/20 (ns)** @repair=0.01(등록)<br>a3−c1_frozen = −9.65, t=−11.47<br>독립 probe(저자 코드 import): a3−sham = **+1.12(p=1.5e-4)@0.005 · −0.03@0.01 · −11.37@0.05 · +9.30(20/20)@0.20** | **등록 상수 repair=0.01이 정확히 부호 영점**. 정보량은 0이 아니라 −10×MDE ~ +8×MDE로 거대하며 비단조(+,0,−,−,−,+) ⇒ THEATER 요건("처치가 축을 못 움직임") 불성립. 게다가 등록 레짐은 사망구역(c2 health 0.085, 아무것도 안 하는 c1_frozen이 최고 arm) · 사전등록 검정력 게이트 FAIL(1.39×<3×)을 사후 span 6.26으로 갈아끼움 |
| **F8 / H_9280**<br>언커플링 열발생 | KILL<br>(true_recall 붕괴) → INVALID<br>(filler=0 분위수 항등식 · 개입 no-op · KILL 변수 사후교체) | D1 θ를 **event 0개인 ordinary-only calib stream**에서 추출 → baseline filler 41.0±6.6 (t=30.2, 24/24) 선증명 · D2 operating-trajectory damped fixed-point 캘리브 → 방출질량 **31.8 θ-eq**(원 0.52 = no-op) · D3 verdict()가 **n_true를 인자로 아예 안 받음** (원 KILL = 중복-emit 착시임을 재현 확인) | run=THEATER<br>**verify=REFUTED → STILL INVALID** | @Q_CEIL=90(보고): exp_A−c2A_rand Δfiller = **+2.50, t=+3.57 (exp 열등)** → THEATER<br>@**사전등록 Q_CEIL=80**: vs random **−1.58, t=−2.27** · vs uleak **−5.88, t=−5.79** ⇒ **재발사 자신의 판정함수가 DIRECTIONAL-POSITIVE 반환**<br>(60/40/20에서도 t=−7.9/−11.5/−10.3; 7 ceiling 중 4개 POSITIVE) | 헤드라인 THEATER가 **기제의 자유 knob Q_CEIL 한 점(90)에서만** 성립. 원 사전등록값 80에서 뒤집힘 = **tune-to-red**(결과를 본 뒤 80→90 이동). R6 규약 스윕(W×asym/sym)은 score() 라벨링만 바꿔 dynamics를 못 건드리는 부호-무감 규약이라 "6/6 부호보존"은 항진적 |

---

## 3. 여전히 INVALID인 것 — 무엇이 남았고 왜 안 고쳐졌나

**3건 전부.** 원 결함 목록은 성실히 수리됐으나 **결함의 생성 규칙**(= 헤드라인이 검증되지 않은 자유 상수/축에
의존한다)은 수리되지 않았다. 그래서 같은 실패가 한 칸 옆에서 재발했다.

### (a) 부호를 뒤집는 미등록 자유 축이 남아 있다
- **F1** — 짝짓기(pairing) 축. c5는 EXP가 실제로 만든 afford 벡터의 순열이라 demand 벡터·afford 주변분포가 동일하고 차이는 짝짓기뿐인데, iid 수요에서 인과 저수지는 그 축에 **도달할 수 없다**(도달에 corr(aff,dem)=+0.787 투시가 필요; 실측 EXP −0.0049 vs c5 −0.0054). bursty로 도달범위를 만들었지만 그 조건은 지출 매칭을 안 했다(V4 예산공정성이 코드상 iid에서만 계산됨, run.py:521).
- **F2** — repair(sink) 상수 + capsplit 규약. 등록점 0.01이 부호 영점이고, 카드충실 R3/R4(capsplit=load)에서는 a3−sham = **+1.75(p=0.0024) / +2.76(p=1.6e-4)**로 MARGIN 초과 유의 양성. 헤드라인은 R1 한 칸 체리픽.
- **F8** — Q_CEIL(포화 임계) 자체. 부호를 실제로 뒤집는 유일한 규약축인데 한 점 고정 + 스윕이 사전 봉인됐다.

### (b) 검출력이 "처치가 인과적으로 도달하는 축"에서 측정되지 않았다 (강제규칙 3 위반)
- **F1**: 보고된 52배 여유는 **static-k 축**(이 처치가 정의상 고정하는 축)에서 계산됨. 짝짓기 축의 동적범위는 4.21pp(align 0.7724 − anti 0.7303, t=+9.53) 존재하나 **인과 도달범위 0** ⇒ MDE/band = ∞ = 검출력 0. 원 R1 실패모드의 이전(移轉).
- **F2**: result.json이 스스로 `V6_POWERED_info_axis=false`, `PASS=false`를 기록. 사전등록 게이트(pilot span > 3×MDE)가 1.56/1.125 = **1.39× FAIL**인데 요약은 사후 analysis-seed span 6.26(5.6×MDE)으로 교체. 그 6.26조차 단일 arm o8_hi_health(Δ=+4.81±2.08, 9/20 pos = 헤비테일)가 떠받치고, 제외하면 1.29× 재-FAIL. headroom 계측기 o6_ORACLE이 blind에 진다(−0.58, p=0.0063) ⇒ 도달 동적범위가 한 번도 유효 측정된 적 없음.
- **F8**: GATE-2는 **잡음바닥 MDE만** 확인했고 처치의 p5-축 도달범위는 확인 안 함. 최대개입 arm(매 step carry→0, mass = exp의 5.6배)조차 recall 상대하락 4.1% < KILL 임계 10% ⇒ KILL 분기(run.py:486)는 **실행 불가능한 코드**.

### (c) 통제가 실효 중복이거나 자원 비대칭
- **F1**: EXP를 이기는 arm은 전부 자원 우위(c1 +9% ATP · bursty-c5 +6.2%). 정확 등지출 통제(c2·c4)에서는 iid·bursty 둘 다 EXP가 이긴다(+2.42/+2.45pp, +1.91/+1.61pp, 전부 20/20). **저자 자신의 R6 결함이 decomposition 안에서 부활**.
- **F2**: a5_sham의 argsort(rng.permutation(h)) = 균등 랜덤 순열 = c2_blind와 분포 동일(a5−c2 = −0.20±0.19 ns) ⇒ 3 control이 **실효 2개**.
- **F8**: c2(clamp)/c3(비례누설)는 동량이나 연산자가 달라 "조건"의 정보량을 격리하지 못함. c3/c4 null에 MDE 없음(동등은 ±6% 폭 내에서만 주장 가능).

### (d) F1의 결정적 공백 — 등지출 무-기제 통제 부재
검증자가 추가한 **ATP-free 1줄 클램프** k = min(demand, 2) = **0.7616 vs EXP 0.7403 (Δ=+2.13pp, t=+8.23, 20/20;
지출보정 후 잔차 +0.7pp)**. 즉 "ATP 경제"의 방향성 결론(licensed bookkeeping)은 오히려 이 통제가 더 잘 지지하지만,
**설계에 그 통제가 없어서 THEATER를 주장할 수는 있어도 벌 수는 없다.**

### 재발사 조건 (패밀리별)
- **F1** — 등지출·동일정보·무-ATP 정책 통제(clamp 계열)를 primary에 편입 · 조건별(특히 bursty) 지출 매칭을 V4 게이트에 포함 · 검출력은 처치가 인과적으로 도달하는 축(짝짓기)에서 계산.
- **F2** — control만 보고 **살아있는 repair 구간**(c2 health>0.5)을 선등록 · V1_liveness를 양쪽(포화+붕괴)으로 · 사후 span 채택 금지(pilot 게이트 못 넘으면 프로브 재설계) · headroom 오라클이 blind를 이기는지 먼저 검증 · nuisance 상수(repair) 축의 부호보존을 PASS 조건에 포함 · sham을 blind와 분포적으로 구별.
- **F8** — Q_CEIL을 정하는 **외생 원리**를 설계에 넣거나 Q_CEIL 축 전체에서 부호보존을 PASS 조건화 · p5 축 도달범위 > KILL 임계를 먼저 확보(lane이 drive-후 신호에 도달하게 하거나 event drive를 θ 근방으로) · c2/c3를 연산자까지 매칭.

---

## 4. 판정이 뒤집힌 것

**원 판정 3/3이 무효화됐다.** 다만 어느 것도 대체 판정이 서지 않았다 — "원 판정이 틀렸다"까지가 licensed고,
"그러므로 반대가 맞다"는 아직 아니다.

### F2 — 예상된 +0.179 PASS는 **재현되지 않았다**
카드 등록 규약(평균 융합 + 격리 분열)으로 되돌리자 a3(aware-fusion)−sham = **−0.03 ± 0.18 (p=0.855, 9/20)**.
PASS가 아니라 정확히 0이다. 하지만 이것이 원 KILL의 정당화는 **아니다**:

- **원 부분양성 +0.157의 정체가 코드로 노출됐다.** 원 run.py의 AND-융합/copy-분열은 무에서 supply를 창조한다:
  펌프 per run = c1_frozen 0.0 · c2_blind **+507.4** · a3 **+608.9** · sham +508.8 · exp +434.9.
  등록 규약에서는 전 arm ≤3e-14 = 0. 즉 **원 실험의 "신호"는 aware arm이 그 펌프를 20% 더 수확한 회계 착시**였다.
  ⇒ 원 KILL도 원 부분양성도 물리적으로 존재하지 않는 자원 위에 서 있었다 = **완전한 오판**(양방향으로).
- **그러나 재발사의 THEATER("aware-fusion 정보량 0")도 반증된다.** 등록 상수 repair=0.01은 부호 영점이고,
  정보량은 +1.12(p=1.5e-4)@0.005 ~ −11.37@0.05 ~ +9.30(20/20)@0.20으로 거대하다. 카드충실 R3/R4에서는
  a3−sham = +1.75/+2.76 유의 양성. 게다가 등록 레짐은 사망구역이다(전 dynamic arm health 0.066~0.152,
  ATP 6.6~8.1/100, c1_frozen 17.48이 최고 arm; result.json에 `"c2_alive_health_gt_0.5": false` 기록).
- **결론**: "카드 규약으로 돌리면 +0.179 PASS"라는 예측은 **규약 축에서만 성립하고 sink 축에서 무너진다**.
  F2는 PASS로도 KILL로도 뒤집히지 않았다 — **미채점 상태로 되돌아갔다**. 재조합 대수가 정보를 더하는지를
  이 레인은 아직 한 번도 유효하게 물은 적이 없다.

### F8 — 원 KILL은 오판으로 확정, 재발사 THEATER는 자기 코드로 반증
- 원 KILL(true_recall 붕괴)은 **중복-emit 착시**였다: exp_A는 n_true를 113.0→80.8로 32개 줄이지만 실제로 잃은
  event는 **0.08/72.8개**(24 seed 중 22개가 손실 0). verdict()가 n_true를 안 받게 계약을 고정하자 KILL이 사라졌다.
- 그러나 재발사의 THEATER는 Q_CEIL=90에서만 성립하고, **원 사전등록값 80에서 exp가 동량 blind를 유의하게 이긴다**
  (vs random −1.58 t=−2.27 · vs uleak −5.88 t=−5.79) ⇒ 재발사 자신의 판정함수가 DIRECTIONAL-POSITIVE를 낸다.
  Q80은 degenerate 전역누설이 아니라 fire_rate 0.194의 희소 과압게이트다. **양성으로의 승격도 금지** — 어느
  Q_CEIL이 진짜 saturation인지 정하는 외생 원리가 없어, 양성 채택은 tune-to-green의 거울상이다.

### F1 — 원 카드의 PASS 조건 자체가 구조적 달성불가였다 (저자 자진 공시, R6)
원 control(c1=무한 ATP, c2=never-binds)은 둘 다 EXP보다 자원이 많다. acc가 k에 단조증가인 이상 "제약 arm이
무제약 arm을 이겨라"는 **구조적으로 달성 불가**. 질문을 "동일 비용에서 ATP 경제가 수요맹목 지출보다 잘 배분하는가"로
교정한 것은 옳다. 다만 교정된 질문의 답도 채점되지 않았다(3(d) 참조).

---

## 5. F8 p5 판정 — 숨은 speak-억제기인가?

**답: p5 위반의 증거는 없다. 그러나 "earned p5-clean"으로 승격할 수도 없다 — 그 축의 검출력이 0이다.
그리고 "병리적 과압에서만 발화한다"는 서술은 사실이 아니다.**

**관측 (p5 무해)**
- exp_A − c1_none, true_recall Δ = **−0.0012**, SEM 0.0008, t=−1.45, **95%CI [−0.0029, +0.0005]** — 상대 하락 0.12%.
- 잃은 event = **0.08 ± 0.06 / 전체 72.8개**, 24 seed 중 22개가 손실 0. 비열등 마진 −0.02 통과. KILL=NO.

**그러나 이건 earned가 아니라 구조적으로 강제된 결과 = dead-code 가드**
- event drive의 **94.8%가 단독으로 θ를 넘는다**(u_event median 0.357 vs θ=0.160). lane은 drive **이전** carry만 건드린다.
- 따라서 **최대개입 arm**(매 step carry→0, 방출질량 28.5 = exp의 5.6배)조차 true_recall 0.9951→0.9538 =
  **상대 4.1% 하락**으로 KILL 임계 10%에 **도달 불가**. KILL 분기는 실행될 수 없는 코드다.
- ⇒ 인용 가능한 것은 **비열등(마진 0.02 < 도달범위 0.041)**뿐. "약을 세게 준 상태에서 얻은 earned p5-clean"이라는
  RESULT.md의 문구는 과대 주장이다.

**"병리적 과압에서만 발화"는 반증됨 (선택성이 blind보다 나쁘다)**
- 개입 발화의 **40.4%가 event 근방**(우연확률 14.4% 대비 2.8배).
- 질량 효율: exp_A는 **emit 40.7개를 죽여 filler 8.4개**를 얻는다. 동량 blind random은 **emit 15.7개만 죽이고
  filler 10.9개**를 얻는다. ⇒ lane은 무차별 방전에 가깝고, **true emit이 살아남는 이유는 lane의 선택성이 아니라
  event drive가 단독-초임계이기 때문**이다.
- 즉 F8 lane은 "숨은 speak-억제기"는 아니지만 "병리 특이적 감압기"도 아니다. 지금 설계로는 둘을 구별할 수 없다.

**p5 축을 진짜로 시험하려면**: lane을 drive-후 신호에 도달시키거나 event drive를 θ 근방까지 낮춰
**도달범위 > KILL 임계**를 먼저 확보한 뒤에만 p5 축의 PASS/KILL을 채점한다.

---

## 6. 선행(H_054 / H_203 / H_012) 발사 전제조건 갱신

### H_054 · H_203 (merge 대수) — 전제조건이 **바뀐다**. 아래 3게이트 선등록 없이는 발사 금지.

1. **ALGEBRAIC-NEUTRALITY 게이트 (F2가 코드로 확립 · 신규 필수)**
   연산자는 총 capacity와 총 supply(Σ cᵢhᵢ)를 **EXACT 보존**해야 한다. arm별 `ops_supply_created`를 실측해
   **≤1e-13**을 사전 게이트로 박는다. 원 AND-융합은 per-run **+507(c2) ~ +609(a3)**의 무-창조 펌프였고,
   원 "부분양성 +0.157"은 그 펌프의 20% 수확차였다.
   ⇒ **이 게이트를 통과하지 못한 merge 양성은 전부 회계 착시로 간주.** merge 대수 계열의 기존 양성 주장은
   이 렌즈로 재검토 대상.

2. **DEGENERACY 게이트 (신규 필수)**
   fission 자손 영구 sibling-ban + fusion 쿨다운(COOL=2). 없으면 self-remerge가 42.8% 발생해
   **명목예산 ≠ 실효예산**(churn ratio 0.32 → 3.56)이고, "연산 횟수"가 처치 강도의 대리변수 역할을 못 한다.

3. **LIVE-REGIME 선등록 + nuisance 축 부호보존 (신규 필수)**
   sink/repair 상수가 **부호를 뒤집는다**(a3−sham −11.4 ~ +9.3 ATP). 따라서
   (a) control만 보고 **살아있는 구간**(c2 health>0.5)을 실험 전에 선등록,
   (b) `V1_liveness`를 **양쪽**(상단 포화 + 하단 붕괴)으로,
   (c) **PASS 조건에 규약 축뿐 아니라 nuisance 상수 축의 부호보존**을 포함,
   (d) sham은 blind와 분포적으로 구별되게(균등 순열 sham = blind는 통제 중복).

   ⇒ **H_054/H_203은 "재조합 대수가 정보를 더하는가"를 아직 한 번도 유효하게 물은 적이 없다.**
   레인은 살아 있고 발사 자체는 유효하나, 위 3게이트를 통과하지 못한 결과는 PASS도 KILL도 채점 불가다.

### H_012 (외생 커플링) — 전제조건이 **바뀐다**. F1의 수정본이 그대로 템플릿.

1. **수요 외생성 증명 = 필수 전제** (F1 R2 fix)
   수요 센서는 supply/ATP를 **인자·클로저·전역 어디로도 받지 않고** 입력×모델상태의 함수여야 한다
   (F1: `demand_i = #{e : S_e > 0.5·max S}`, S = 라우터 원점수). 그리고 **binding_rate > 0**(수요>공급이
   구조적으로 가능)을 실측 보고한다(F1 = 0.528; 원 설계에선 정의상 0 = 항진적 처치 = 결과가 정의상 참).
   정보채널 증명도 동반: demand 셔플 시 EXP의 k가 43.6% 바뀌고 통제는 0% 변함.

2. **등지출·동일정보·무-기제 통제가 필수** (F1의 결정적 공백)
   ATP를 전혀 안 쓰는 1줄 클램프 `k = min(demand, 2)`가 EXP를 **+2.13pp (t=+8.23, 20/20; 지출보정 후 잔차 +0.7pp)**로
   이긴다. 외생 커플링의 효과 주장은 반드시 **이 계열(동일 지출 · 동일 정보 · 기제 없음)** 대비로 채점해야 한다.
   그렇지 않으면 "licensed bookkeeping"(장부는 맞지만 기제는 무기여)과 구별할 수 없다.

3. **조건별 지출 매칭 + 자기상관 수요** (F1의 두 다리 붕괴 원인)
   iid 수요에서 인과 저수지/커플링 대비는 **분포적 항등식**이다(aff_t = g(dem_<t) ⇒ iid에서 aff_t ⊥ dem_t 강제
   ⇒ Δ=0은 측정이 아니라 정리). 따라서 저장/커플링 축을 시험하려면 **자기상관 수요(bursty)가 필수**인데,
   **그 조건에서도 지출을 매칭**해야 한다. F1의 bursty 다리는 EXP 3.6416 vs c5 3.8674(+6.2% ATP, t=−34.9)로
   미매칭이었고, 설계 자신의 기울기(12pp/k) × Δk 0.226 ≈ 2.7pp가 관측된 "저장이 해롭다" −2.88pp의 거의 전부를
   설명한다 ⇒ **자원격차 아티팩트**.
   (참고 기제: corr(afford, demand) = −0.005(iid) → −0.560(bursty). 탐욕적 저수지는 지속수요와 역상관.)

4. **검출력은 처치가 인과적으로 도달하는 축에서**
   F1의 "52배 여유"는 처치가 **정의상 고정하는** static-k 축에서 계산된 값이다. 도달범위 0인 축(짝짓기)에서는
   MDE/band = ∞. 사전 MDE는 반드시 **처치가 실제로 움직이는 축**에서, **분석 seed와 disjoint한 pilot seed**로 계산하고,
   미달 시 abort를 코드에 박는다. **사후 span 채택 금지**(F2가 이걸로 게이트를 우회했다).

### 전 계열 공통
- **engine-native 0** (3건 모두 toy numpy) ⇒ 통과했더라도 tier 상한 **DIRECTIONAL**. cement하려면 303M py-channel
  (`anima-py evaluate`) 경로가 필요하다(`a_engine_native_learning` · `a_eval_py_canonical`).
- **max(controls) 금지의 교과서적 실례** (F1): max를 썼다면 c1이 삼켜 KILL, min을 썼다면 c2만 보고 PASS.
  둘 다 거짓 — control마다 서로 다른 질문에 답하며 각각 유의하다. control별 paired-t 전부 + pooled-mean이 규약이다.
- **메타 진단**: 세 재발사가 지목된 결함을 정직하게(자기 PASS=false를 자진 공시할 정도로) 수리하고도 전부 실패한
  공통 원인은 하나다 — **헤드라인이 사전에 검증되지 않은 자유 상수의 한 점 위에 있었고, 그 축에서 부호가 뒤집힌다.**
  다음 사전등록부터는 **"부호를 뒤집을 수 있는 축을 전부 열거하고, 각 축의 부호보존을 PASS 조건에 포함한다"**를
  강제규칙으로 올린다. ρ-AXON 도그마(confound → INVALID, never a false PASS/FAIL)를 적용하면,
  **F1·F2·F8 어느 레인도 THEATER로 닫아서는 안 된다.**

---

## 부록 — 원본 위치
- F1: `.../state/mito_organelle_lane/F1_atp_energy_economy/refire/` (RESULT.md · REFUTE.md · result.json · run.py)
- F2: `.../state/mito_organelle_lane/F2_organelle_fission_fusion/refire/`
- F8: `.../state/mito_organelle_lane/F8_uncoupling_thermogenesis/refire/`
- 원 종합: `.../state/mito_organelle_lane/SYNTHESIS.md`
