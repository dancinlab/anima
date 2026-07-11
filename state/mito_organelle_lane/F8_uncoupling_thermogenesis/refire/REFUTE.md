# REFUTE (재발사) — H_9280 / F8 언커플링·열발생 · 적대적 재검증

**판정: 재발사 결론(🎭 THEATER) REFUTED · 최종 = ⛔ INVALID (still_invalid = true)**

원 INVALID의 3대 결함(D1 분위수 항등식 · D2 no-op 개입 · D3 KILL 변수 사후교체)은 **코드상 실제로 수리됐다** —
말로만 고친 게 아니다(§0). 그러나 재발사는 **새로운 설계 결함 2개** 위에 서 있고, 그 결함이 곧 헤드라인 결론
(THEATER)과 핵심 부수주장(earned p5-clean) 둘 다를 무효화한다. 반박 근거는 전부 **재발사 자신의 `run.py` ·
자신의 사전등록 `verdict()` 함수 · 자신의 control 코드**를 무수정으로 호출해 얻었다 (probe1/2/3/4, seed 동일,
paired-CRN 동일).

---

## §0. 수리 확인 (칭찬할 것은 칭찬한다 — 여기까진 진짜다)

| 원 결함 | 코드 확인 | 판정 |
|---|---|---|
| D1 병 부재(분위수 항등식) | `calibrate()`가 `make_stream(..., p_event=0.0)`에서 θ 추출(run.py:242) · P_EVENT는 독립 상수(run.py:58) | ✅ 진짜 수리. c1 filler = 41.0±6.6, t=30.2 (실측 선증명) |
| D2 약 미투여(no-op) | θ·C 둘 다 `simulate_operating()`(emit 방전 켜짐) fixed-point(run.py:250-262) · GATE-1 사전검사 | ✅ 진짜 수리. mass 5.076 = 31.8 θ-eq, fire_rate_min 0.104>0 |
| D3 KILL 변수 사후교체 | `verdict(...)` 시그니처(run.py:466)에 `n_true` 인자 **없음** — 코드상 접근 불가 | ✅ 진짜 수리 |
| Δ = exp − max(controls) | 미사용. control별 paired-t + pooled-mean (run.py:645-672) | ✅ |
| 정보채널 (a) 코드 | exp 결정변수 `carry`(run.py:291) = 입력 u₀..ₜ의 누적함수 · c2는 `plan`(rng) | ✅ 채널 실재 |
| 정보채널 (b) 분산 | Var(carry)=0.00102>0 · fire_rate 0.150∈(0,1) · carry@fire exp 0.133 vs rand 0.067 | ✅ 항진 arm 아님 |

⟹ **채점 불가의 원 사유는 해소됐다.** 그래서 이 REFUTE는 "또 INVALID"가 아니라 **다른 축의 INVALID**다.

---

## R1 (치명) — 헤드라인 THEATER는 **Q_CEIL 한 점에서만 성립**한다. 부호가 뒤집히고, 원 사전등록값(80)에서는 재발사 자신의 `verdict()`가 **DIRECTIONAL-POSITIVE**를 뱉는다

재발사는 `Q_CEIL`을 **90**으로 새로 등록했다(run.py:60 · "상위 decile = 병리적 과압"). 원 실험의 사전등록값은
**80**이었다. 이 knob 하나가 **결정적 비교(exp vs 동량 blind)의 부호를 뒤집는다.**

재발사의 `run_arm`·`match_rand`·`match_uleak`·`score`·`verdict`를 **한 줄도 고치지 않고**, 동일 24 analysis
seed + 20 pilot seed(MDE 재계산 포함)로 Q_CEIL만 바꿔 호출한 결과 (probe3):

| Q_CEIL | mass(θ-eq) | Δfiller vs c1 | **Δfiller vs 동량 random** | Δfiller vs 동량 uleak | Δrecall | **재발사 자신의 사전등록 verdict() call** |
|---|---|---|---|---|---|---|
| 95 | 23.1 | −2.38 | **+5.71** (t=+8.33) | +4.08 | −0.0012 | THEATER |
| **90 (재발사 등록값)** | 31.8 | −8.38 | **+2.50** (t=+3.57) | +0.54 | −0.0012 | **THEATER** ← 보고된 결론 |
| **80 (원 사전등록값)** | 47.6 | −19.29 | **−1.58 (t=−2.27)** | −5.88 (t=−5.79) | −0.0008 | **DIRECTIONAL-POSITIVE** |
| 60 | 71.7 | −30.04 | **−4.54 (t=−7.91)** | −10.83 (t=−12.52) | −0.0025 | **DIRECTIONAL-POSITIVE** |
| 40 | 92.1 | −36.46 | **−5.79 (t=−11.50)** | −11.42 (t=−15.65) | −0.0054 | **DIRECTIONAL-POSITIVE** |
| 20 | 110.6 | −38.71 | **−4.58 (t=−10.28)** | −8.00 (t=−15.56) | −0.0092 | **DIRECTIONAL-POSITIVE** |
| 5 | 133.8 | −40.21 | −2.00 (t=−6.07) | −3.25 | −0.0140 | PARTIAL |

(Q_CEIL=90 행은 result.json과 소수점까지 일치 — Δ vs c1 = −8.375, Δ vs c2 = +2.500. 하네스 재현성 검증됨.)

**7개 ceiling 중 4개(80·60·40·20)에서 재발사 자신의 사전등록 판정함수가 DIRECTIONAL-POSITIVE를 반환한다.**
THEATER는 오직 **가장 보수적인·가장 저용량인 두 corner(95·90)**에서만 나온다. 그리고 재발사는 하필 그 corner를
새 등록값으로 골랐다.

### 왜 이것이 "내가 tune-to-green 한 것"이 아닌가

1. **부활시킨 게 아니라, 선언된 종결범위를 반증했다.** RESULT.md §7은 narrow 결론이 아니라
   **"스칼라 magnitude ceiling *계열*은 이 재발사로 licensed 종결(THEATER)"**이라는 **family-level 폐쇄**를
   선언했고, §5는 메커니즘 법칙("과압 조건은 filler에 대해 무정보다 · 질량 효율이 blind보다 나쁘다")을 주장했다.
   그 메커니즘 주장이 참이면 **모든 용량에서** blind가 이겨야 한다. 실제로는 4/7에서 exp가 blind를 유의하게 이긴다.
   ⟹ 선언된 family 폐쇄와 메커니즘 법칙은 **재발사 자신의 코드로 반증된다.**
2. **Q_CEIL=80은 내가 고른 값이 아니라 원 사전등록값**이다. 재발사가 결과를 본 뒤 80→90으로 옮겼고, 그 이동이
   정확히 THEATER를 만든다. 이건 tune-to-green의 거울상 = **tune-to-red**다.
3. **degeneracy 방어 실패.** "낮은 ceiling은 그냥 전역 누설이라 saturation-gate가 아니다"는 반론은 Q_CEIL=80에서
   성립하지 않는다 (probe4): fire_rate = **0.194** (19.4% step만 발화 · 여전히 희소 과압게이트) ·
   diss_on_event_frac = 0.334. 상위 quintile을 "과압"으로 부르는 것은 상위 decile만큼이나 정당하다.
   즉 Q90만이 유일하게 정당한 "saturation" 정의라는 근거가 없다.
4. **강제규칙 6 위반이 바로 여기다.** "규약이 부호를 뒤집을 수 있는 곳은 카드 등록값을 쓰고 ≥2 규약에서 부호
   보존을 확인하라." 재발사의 R6 스윕(W∈{1,2,4}×{asym,sym})은 **부호를 뒤집을 수 없는 규약**만 흔들었다 —
   W는 `score()`의 라벨링만 바꿀 뿐 dynamics(어떤 emit이 일어나는가)를 바꾸지 못한다. 그래서 "6/6 부호 보존"은
   거의 항진적이다. **부호를 실제로 뒤집는 유일한 규약(=가설의 대상인 saturation 임계 그 자체)은 한 점에
   고정됐고, 그 스윕은 "tune-to-green이므로 금지"라고 사전 봉인됐다.** 부호 민감 축을 봉인하고 부호 무감 축에서
   robustness를 선언한 것.

⟹ **헤드라인 THEATER는 licensed 음성이 아니라 operating-point-selected 음성이다.**

---

## R2 (치명) — "earned p5-clean"은 여전히 **dead-code 가드**다. KILL 분기는 *어떤 용량에서도* 도달 불가

RESULT.md §4: "원 실험의 p5_clean은 개입질량 0.33이라 공짜였고 dead-code 가드였지만, **이번 것은 약을 세게 준
상태에서 얻은 earned p5-clean**". 이 주장은 **거짓**이다.

강제규칙 3은 "**처치가 도달 가능한 축의 동적범위 > 유의 문턱**"을 요구한다. GATE-2는 **잡음바닥 MDE**
(MDE_recall=0.0031 ≤ KILL임계 0.0996)만 확인했지, **이 레인의 채널로 recall을 10% 떨어뜨리는 것이 애초에
가능한가**를 확인하지 않았다.

probe1 (재발사 코드 그대로 · 12 seed) — **최대개입 arm**(매 step carry→0 전량 방출 · budget 무제한 · mass 28.48
= exp_A의 **5.6배**):

```
true_recall :  c1 = 0.9951   exp_A = 0.9939   MAX-DRAIN(carry→0 매 step) = 0.9538
n_filler    :  c1 = 40.3                       MAX-DRAIN = 0.1
⟹ p5 축의 *도달 가능한* 동적범위 = 0.0413 (상대 4.1%)   vs   KILL 임계 0.0996 (10%)
```

**KILL 임계는 무한질량 개입으로도 못 넘는다.** 이유는 구조적이다:
- event drive 자체가 θ를 압도한다 — u_event median **0.357**, min 0.104, **P(u_event ≥ θ) = 0.948** (θ=0.160).
- lane은 drive 이전의 carry만 감산한다(run.py:291-323) ⟹ event emit의 94.8%는 carry와 **무관하게** 발생.
- (반면 ordinary drive는 u_max = 0.136 < θ ⟹ filler는 100% carry 의존. 그래서 filler 축엔 동적범위가 있고
  recall 축엔 없다. 이 비대칭이 곧 "p5 안전"의 정체다.)

⟹ `verdict()`의 `kill` 분기(run.py:486)는 **실행 불가능한 코드**다. "약을 세게 줬는데도 p5 위반이 없었다"가
아니라 **"이 lane으로는 p5를 위반할 방법이 애초에 없다"**가 맞다. 안전성은 *측정된* 것이 아니라 *설계된* 것이다.
(비열등 검정(마진 −0.02)은 도달범위 0.041 > 0.02 이므로 살아남는다 — 인용 가능한 것은 **비열등**뿐이고
"earned KILL-clean"은 인용 불가.)

---

## R3 (부수) — 동량 매칭 ≠ 연산자 매칭. c2/c3는 exp와 *다른 연산자*다

- exp: `amt = carry − C` = **천장 clamp** (P를 절대 C 아래로 못 내린다 · C=0.108 = θ=0.160의 67% 받침대 유지).
- c2(rand): `amt = min(mag, P)` (run.py:302) — 낮은 carry step에서 발화하면 P를 **0 쪽으로 완전 배수**.
- c3(uleak): `amt = uleak·P` — 전역 비례 누설.

세 arm은 "동일 질량, 다른 타이밍"이 아니라 **동일 질량, 다른 연산자**다. 조건(언제 쏘나)의 정보량을 격리하려면
**연산자를 고정한 채 조건만 blind화**해야 한다(예: 다른 seed의 carry surrogate로 clamp). 재발사에 그런 arm은 없다.
그래서 Q_CEIL=90의 "+2.50 열등"은 *조건이 무정보*라는 증거가 아니라 *얕은 clamp가 저용량에서 비효율*이라는
증거일 수 있다 — 그리고 R1이 정확히 그것을 보여준다(용량이 커지면 같은 조건·같은 연산자가 blind를 이긴다).

## R4 (부수) — 결정적 null 비교(c3·c4)에는 MDE가 없다

판정은 c2(유의)로 갈렸지만, RESULT의 "3종 blind 전부에게 지거나 동등"이라는 문구는 c3(Δ=+0.54, t=0.67) ·
c4(Δ=+1.04, t=1.31)의 **null**에 기댄다. 이 두 null의 MDE는 계산되지 않았다(사후 SEM 기준 ≈ ±2.3 filler ≈
baseline의 6%). "동등"은 **±6% 이내에서만** 주장 가능하다.

## R5 (부수) — engine-native 0

순수 numpy toy · `core/` 접촉 0 · `.hexa` 0 · CLM 0. `a_engine_native_learning`상 tier 상한 DIRECTIONAL.
(RESULT도 인정 — 이 항목은 등급 상한이지 반박은 아니다.)

---

## 정리 — 왜 THEATER가 아니라 다시 INVALID인가

- **THEATER 아님**: THEATER = "개입했는데 정보가 없다". 그런데 동일 코드·동일 seed·동일 control에서 ceiling을
  원 사전등록값(80)으로만 되돌려도 exp가 동량 random(−1.58, t=−2.27)·동량 uleak(−5.88, t=−5.79)을 **유의하게
  이기고**, 재발사 자신의 판정함수가 **DIRECTIONAL-POSITIVE**를 찍는다. 조건은 정보를 담고 있다 — 다만 그 정보의
  가치가 **용량(=ceiling)에 강하게 의존**한다.
- **DIRECTIONAL-POSITIVE로 승격도 금지**: 그 양성은 내가 knob을 돌려 얻은 것이고, 어느 Q_CEIL이 "진짜 saturation"
  인지 결정할 **외생적 원리가 설계에 없다**. 여기서 양성을 채택하면 그게 tune-to-green이다. 나는 하지 않는다.
- ⟹ **INVALID**: (i) 헤드라인 판정의 **부호가 기제 자신의 자유 knob(Q_CEIL)의 함수**이고 그 knob이 결과를 본 뒤
  80→90으로 이동했다(tune-to-red) · (ii) 부호를 뒤집는 축의 스윕이 "tune-to-green"이라는 이름으로 사전 봉인되고,
  대신 부호를 뒤집을 수 없는 축(W)에서 robustness가 선언됐다(강제규칙 6 실패) · (iii) p5 KILL 축은 **도달 가능
  동적범위 4.1% < 임계 10%** = 검출력 0 = dead-code 가드(강제규칙 3 실패).
  ⟹ 이 설계로는 양성도 음성도 **채점할 수 없다**.

## 재설계 요구조건 (이것 없이는 어떤 tier도 부여 불가)

1. **Q_CEIL을 결과와 무관한 외생 원리로 pin** 하라 (예: "saturation = 자연 emit 확률이 X를 넘는 carry" 처럼
   기질 물리에서 유도) — 아니면 **전 ceiling 격자에서 결론을 진술**하라("조건은 용량 D 이상에서만 blind를 이긴다").
   한 점을 골라 family closure를 선언하는 것은 양방향 모두 금지.
2. **연산자-고정 조건-blind control** 추가: 동일 clamp 연산자 · surrogate carry(다른 seed/위상섞은 u)로 발화.
   현재의 c2/c3는 연산자가 달라 조건의 정보량을 격리하지 못한다.
3. **p5 축의 도달 가능 동적범위를 사전 계산**하라(max-drain probe). 4.1% < 10% 이면 KILL 규칙을 그 축에 걸지 말고,
   비열등(마진 ≤ 도달범위)만 주장하라. 현 문구 "earned p5-clean"은 철회 대상.
4. c3·c4 null에도 MDE를 붙여라 ("동등"의 폭을 수치로).
5. 최종 tier는 engine-native(`core/` decode)에서만.

---

### 검증 산출물 (재현)
- probe1 (p5 도달범위): `/private/tmp/claude-501/-Users-mini-dancinlab-anima/a20dbd82-2d30-4f9f-9365-996d415ad96a/scratchpad/probe1.py`
- probe2 (Q_CEIL × 동량 random 부호): `.../scratchpad/probe2.py`
- probe3 (재발사 사전등록 `verdict()` × Q_CEIL): `.../scratchpad/probe3.py`
- probe4 (ceiling degeneracy · fire_rate): `.../scratchpad/probe4.py`
- 전부 refire `run.py`를 **import 후 무수정 호출** · 동일 SEEDS/PILOT_SEEDS · paired-CRN · $0 numpy.
