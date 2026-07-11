# REFUTE — H_9273 / F1 ATP 대사경제 · 적대적 재검증

**판정: 🚫 INVALID (원 결론 THEATER 반박)** — 음성 자체는 아마 참일 것이나 **이 프로브로는 벌 수 없는 음성**이다.
프로브는 (a) 구조적으로 **검출력 0**이고 (b) 처치 arm이 **데이터-맹목 결정론 시계**라 Δ≈0이 설계상 강제되며
(c) 두 V-gate가 **주장하는 것을 인증하지 못하고** (d) c1/c2가 **동일 arm 중복**이며 (e) p5 constructive test가 **dead-code 항진명제**다.
ρ-AXON 도그마 "confound → INVALID, never a false PASS/FAIL" 적용 → THEATER가 아니라 INVALID.

---

## R1. 검출력 0 — 음성이 실행 전부터 확정 (치명)

| 축 | 값 |
|---|---|
| ATP 경제가 도달하는 캡 대역 | mean_k **1.66 ~ 4.72** (eval k=2/3/5) |
| 그 대역 + c1(k=8)의 acc 전체 스팬 | 0.7505 ~ 0.7618 = **1.12 pp** |
| 유의 문턱 (vs c1, `max(DELTA_EPS, 2·sem)`) | **1.71 pp** |
| DELTA_EPS (THEATER 선언선) | 1.00 pp |

**캡 축이 움직일 수 있는 전 범위(1.12pp) < 검출 문턱(1.71pp).** ATP 경제가 대역 내 *최적* 캡을 골랐어도
"sig=True"는 수학적으로 불가능하다. 즉 `sig=False ⇒ ΔEff≈0 ⇒ THEATER`라는 추론 사슬은 **데이터가 아니라
설계에서** 나왔다. 사전등록 반증조건("어느 캡에서도 ΔEff≈0")을 **아무 캡도 무언가를 할 수 없는 대역**에서
평가한 것 = 무의미한 통과.

**VR gate는 거짓 안심.** VR(k=1 −12.3pp)은 **처치가 결코 머무르지 않는 점**에서 민감도를 인증한다
(EXP_tight도 eval k=2). 처치가 실제로 사는 k∈[2,8]에서는 acc가 0.7505/0.7567/0.7580/0.7533 = **완전 평지**.
"계측기 정상"이 아니라 **계측기는 처치 대역 밖에서만 정상**이다.

## R2. 처치 arm = 데이터-맹목 결정론 시계 ⇒ Δ≈0은 해석적 귀결 (치명)

`policy_atp(t)`는 batch·loss·model·demand를 **인자로도 클로저로도 받지 않는다**. `k=f(atp)`이고 `atp`는 오직
`k`로만 진화하는 **자율 폐루프**. 재현 결과(run.py 상수 그대로 시뮬):

```
tight  seed0/2  tail = [2,1,2,2,1,2,2,1,...]  주기-3 클럭 · 시드 무관 동일
mid    seed0/2  tail = [3,3,3,3,3,3,3,3,4,...] ≈ static k=3 (92.5%가 k=3)
loose  seed0/2  tail = [5,4,5,5,4,5,5,5,4,...] 주기-3 클럭
```

⇒ ATP 장(場)이 모델로 들어가는 **유일한 채널은 정수 k**이고, 그 k는 **c3 static cap ± 결정론적 dither**다.
정보를 나를 채널이 애초에 0이므로 "동일-캡 static 대비 lift 없음"은 **측정된 발견이 아니라 항진명제**다.
카드가 세운 기제(수요 ≥ 생산 → 예산이 묶임)는 **인스턴스화된 적이 없다**: 수요는 독립량이 아니라
`afford = floor((atp−EQ)/COST)` → `consumed = k·COST+EQ ≤ atp`, 즉 **수요는 공급의 함수로 정의**되어 있어
구조적으로 수요 > 생산이 불가능하다.

**"binding=99.9%"도 발견이 아니다.** `bind := (k < K_MAX)`. 평형 k(1.66/3.08/4.72)가 8 미만인 것은
`resp` 상수 선택이 강제한 값 = **파라미터의 재진술**. 헤드라인 "예산은 99.9% binding 된다"는 동어반복.

## R3. 용량 레인이 애초에 inert — route_acc가 **우연 이하** (치명)

E=16 → 우연 route_acc = **0.0625**. 전 arm 실측:

```
c1 0.0380 · c2 0.0380 · EXP_tight 0.0328 · c3k2 0.0398 · EXP_mid 0.0442 · EXP_loose 0.0410 · vr_k1 0.0340
```

**모든 arm이 우연 이하**, usage_entropy 0.88~1.00 (거의 균일). 즉 라우터는 잠재 토픽을 **전혀** 잡지 못하고
expert 특화가 존재하지 않는다. 따라서 k는 "동시 활성 *특화* expert 수"가 아니라 **평균화(smoothing) 노브**다
— 측정 메타법칙의 **FORM tunable** 그 자체. k∈[2,8] 평지도, k=1에서만의 −12pp도 전부 **앙상블 평균 상실**로
설명되며 "용량"과 무관하다. ATP→용량→표현이라는 인과 사슬의 중간 고리가 이 기질엔 **없다**.

**V1 gate도 confound.** `shuffle_select=True`는 3가지를 동시에 바꾼다: ① 무작위 선택 ② soft gate
`G=P·Mask/ΣP` → **균일 `G=Mask/k`** ③ 라우터 학습 자체를 끔(`if not shuffle_select`). route_acc가 우연 이하인
이상 15pp 붕괴의 주범은 **soft mixture weight(②)**이지 top-k 선택 채널이 아닐 개연성이 높다. V1은 "선택 채널이
살아있다"를 인증하지 못한다.

## R4. c1 ≡ c2 — 통제 2개가 아니라 1개 (통제 인플레)

per-seed acc **byte-identical**: c1 `[0.77625, 0.7675, 0.71, 0.7625, 0.75]` = c2 (route/H/emit/tension 전부 동일).
c2(resp=25)는 항상 k=8 → **c1과 완전히 같은 학습 궤적**. 보고된 "vs c1 +0.0085 · vs c2 +0.0085"는 같은 숫자
2번 인쇄. 카드의 "Δ vs ≥2 controls"는 실질 **c1(=c2) + c3 = 2개**로 간신히 유지되나, 저자가 자기 통제의
중복을 인지하지 못했다는 신호.

## R5. p5 constructive test = dead-code 항진명제 (증거 무효)

```python
_zero = np.zeros_like(atp_trace)                                  # ← 사용 안 됨
_rand = ...standard_normal(...)*100.0                             # ← 사용 안 됨
h1 = sha256(emit_decide(logits, thr)[0]...)   # "ATP=0 문맥"      ← h0과 완전히 동일한 호출
h2 = sha256(emit_decide(logits, thr)[0]...)   # "ATP=random 문맥" ← h0과 완전히 동일한 호출
```

`_zero`/`_rand`는 **어디에도 주입되지 않는다**. h0=h1=h2는 순수함수 동일 인자 3회 호출이므로 `identical=True`가
**구성상 보장**된다. 만약 emit_decide가 전역 ATP를 읽는 진짜 p5 위반이 있었어도 이 테스트는 그대로
`p5_clean=True`를 뱉는다 — **막으라는 실패 모드를 못 막는 죽은 가드**.
(다행히 `emit_decide(logits, thr)`는 실제로 순수함수이고 심볼 검사 `'atp' not in body`는 유효 → **실 p5 위반은
없음**. 그러나 보고서가 내세운 "구성적 p5 증명"은 **증거로서 무효**이며, 이 상태로 카드/RESULT에
`p5_clean=true`를 인용하면 안 된다.)

부수: emit 문턱 `THR[seed] = median(c1 tension)` → **c1의 emit_rate=0.500은 구성상 강제**. EXP arm의
`Δemit=−0.040`은 c1-보정 상수를 다른 logit 스케일에 전이시킨 **FORM/scale 아티팩트**이지 "창발"이 아니다
(verdict에서 배제한 건 옳으나, "합법 ATP→…→emit 창발경로"라는 서술도 근거 없음).

---

## 체크리스트 대조

| # | 항목 | 판정 |
|---|---|---|
| 1 | control 동일 예산 (params 2560 · step 1500 · batch · data · init) | ✅ 공정 (c1/c2는 FLOPs가 오히려 **더 많음**, c3 동일) — **여기선 INVALID 안 나옴** |
| 2 | 양성이 tunable FORM인가 | 양성 자체가 없음. 단 **k 축 전체가 FORM(평균화 노브)** — route_acc 우연 이하 (R3) |
| 3 | held-out | ✅ 진짜 held-out (test rng 3000+seed, 표본 disjoint, 동일 topic_emb/W_topic) |
| 4 | Δ가 seed 분산 안인가 | ✅ 전부 안. **단 축의 전 범위(1.12pp)가 문턱(1.71pp)보다 작아** 무의미 (R1) |
| 5 | p5 위반 (`if budget<k: silence`) | 실 위반 **없음** (emit_decide 순수). 단 **증명은 dead-code 항진명제** (R5) |
| 6 | tune-to-green 흔적 | 없음. 상수 사전등록 · c3/V-gate 사후추가는 **통제 강화**(음성을 강화하는 방향)라 합법 |

## 결론

원 결론의 두 문장 모두 **licensed 되지 않는다**:

1. **"ATP 대사경제 = bookkeeping overhead"** — 정보를 나를 채널이 0인 데이터-맹목 시계(R2)를,
   검출력 0인 대역(R1)에서, 특화가 존재하지 않는 용량 레인(R3)으로 측정했다. 음성은 **설계가 강제한 것**이다.
   카드 §3 반증조건은 **충족된 게 아니라 무의미하게 통과**했다.
2. **"살아있는 레버는 '캡'이지 '회계장부'가 아니다"** — 자기 데이터가 **정면 반박**한다. c3 스윕상 캡은
   k=2/3/5/8에서 전부 평지(0.7505~0.7580, 노이즈 내)이고 **k=1에서만 −12pp 해악**. 이 토이엔 **캡 레버도 없다**.
   실증된 유일한 사실은 "이 단일-토픽 토이는 k≥2면 용량 수요가 0"이다.

⇒ **INVALID**. F1 레인을 THEATER로 닫으면 안 된다(잘못된 closure). 재실행 조건(전부 필요):
(i) 수요를 **외생화** — demand를 입력 난이도/loss/모델 상태에서 뽑아 supply와 독립시킬 것 (현재는 supply의 함수),
(ii) 라우터가 **우연 이상**(route_acc ≫ 1/E)이고 expert 특화가 성립하는 기질에서 — 그래야 k가 FORM 아닌 용량,
(iii) acc가 k에 **가파른** 대역(다중-토픽/재조합 데이터: y가 ≥2 expert의 결합을 요구)으로 arm을 이동,
(iv) MDE < 축의 동적 범위가 되도록 seed↑ 또는 효과크기↑ — **사전 검출력 계산 필수**,
(v) V1을 1-변수 분리(선택만 셔플, soft gate·라우터 학습은 유지), p5 테스트의 `_zero`/`_rand` **실제 주입**.
