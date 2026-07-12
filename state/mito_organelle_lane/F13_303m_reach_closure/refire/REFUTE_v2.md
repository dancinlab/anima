<!-- @canonical-ok — 2차 적대검증 노트. 1차 REFUTE.md(원 run 대상)와 별개 문서이며 대체가 아님(둘 다 보존 필요: 1차가 사후 KILL을 주장했고 이 문서가 그것을 감사한다). 파일명은 상위 태스크가 명시 지정. -->

# H_9285 REFIRE — 적대적 재검증 v2 (REFUTE_v2)

**결론: 반박 실패 (refuted = false). 제시된 결론 `verdict = INVALID` + "KILL은 cement되지 않았고
오히려 반증됐다"는 **유지된다**. 7종 계측 강제규칙 전부 통과. still_invalid = true.**

적대적 목표는 결론을 깨는 것이었다. 깨지지 않았다 — 오히려 독립 재계산이 결론을 **강화**했다.

---

## 1. 체크리스트 전수 판정

| # | 반박 축 | 판정 | 근거(독립 검증) |
|---|---|---|---|
| 1 | 헤드라인이 순서통계량? | ✅ 아님 | `run_refire.py:76` `HEAD = "m_B_conj"` — 단일 변수. `min()`/`max()` 없음. 원 F13의 `m_conj=min(mA,mB)`(`run.py:469`)와 대조 |
| 2 | 사후 detector 교체? | ✅ 없음 | 실행 파일 sha256 = `7b1d3760…9c7d` = PREREG.md 동결 sha **일치**(내가 직접 `shasum` 재계산). 헤드라인이 코드에 하드코딩 |
| 3 | 새 disjoint seed? | ✅ 진짜 새 데이터 | **자체보고 불신하고 직접 검증**: 5-tuple overlap **0** · (A,B)쌍 overlap **0** · cue 단어 vocab overlap **0** (old 142 ⊥ new 167). seeds 20260713/2000/13 ≠ 20260712/1000/7 |
| 4 | 부호보존 설계 내장? | ✅ 내장 | `sign_flip_axes` 3축(setpoint·constant-k·schedule) 사전열거 + `PASS = beats(c0) and beats(c1) and beats(c2)` — 사후 체리픽 아님 |
| 5 | sham(SHOCK) 구별? | ✅ 구별됨(단 무의미하게) | SHOCK routerL1=0.425로 개입은 실재하나 마진에 signed −0.086(t=−1.49) — **이것이 바로 V2 FAIL의 내용** |
| 6 | Δ=max(controls)? MDE? 정보채널? | ✅ 전부 준수 | control별 paired-t 3개 + pooled 전부 보고(max 미사용) · MDE는 disjoint pilot(6 blocks)에서 · Var(k_t)=0.200>0, var0 seq 비율 0.000 |
| 7 | 인프라 벽을 과학 verdict로? | ✅ 아님 | PARITY max\|Δ\| = **0.0** (run.log:4, byte-exact) · wall 154s · 인프라 실패 0. INVALID는 **측정타당성** 판정(V2)이지 인프라 핑계 아님 |

## 2. 원 KILL 근거의 독립 재계산 — 요약의 원 수치가 정확함

원 `result.json` items에서 내가 직접 block-mean paired-t 재계산:

| 량 | 요약 주장 | 내 재계산 | 일치 |
|---|---|---|---|
| ORIG c0 level | +1.083 (t=4.69) | **+1.0833** | ✅ |
| ORIG EXP−c0 | −0.209 (t=−2.30, p=.033) | **−0.2088 SEM=0.0907 t=−2.302** | ✅ |
| ORIG SHOCK−c0 | +0.100 (t=+2.48) | **+0.1000 SEM=0.0404 t=2.476** | ✅ |

원 KILL이 **사후 detector 교체**(headline `m_conj`→live branch `m_B_conj`)로 얻어졌다는 진단도 사실 —
`run.py:469`가 `HEAD="m_conj"`임을 확인. 즉 그 KILL은 F8/F13과 동일한 죄로 licensed가 아니었다.

## 3. 결정타 — "저검출력 미재현"이 아니라 **통계적 불일치**다 (내가 추가한 검정)

요약은 "부호반전 + ns"로 논증한다. 적대적으로 보면 **ns 자체는 약한 증거**다: 새 run의 SEM=0.122라서
원 효과 −0.209가 **진짜여도** |t|=1.71 < 2.093 ⇒ 유의하게 못 잡는다. "ns"만으론 저검출력 미재현과
구별 불가.

그래서 두 seed 추정치의 **이질성 검정**을 직접 돌렸다:

```
old EXP−c0 = −0.2088 ± 0.0907   |   new EXP−c0 = +0.1286 ± 0.1219
difference = 0.3374   SE = 0.1520   z = 2.220   two-sided p = 0.026
```

⇒ 두 추정치는 **서로 유의하게 다르다(p=.026)**. 단순한 검출력 부족 미재현이 아니라 **seed 간 통계적
불일치** = "seed 특이적 잡음 draw" 진단과 정확히 부합. **요약의 결론은 요약이 제시한 것보다 더 강하게
성립한다.**

구조적 보강: EXP는 정보를 **버리는** 연산(k∈{1,2}, k=3은 0회)인데 dense c0(k=E=3)보다 nominal 우위
(+0.129)다. 정보 파괴가 성능을 올리는 건 구조적으로 불가능 ⇒ 이 축은 잡음이 지배한다는 독립 증거.

## 4. 발견한 실 약점 (verdict를 바꾸지 않음 · 정직 기록)

1. **MDE는 낙관적이었다.** pilot block-delta sd = 0.2596 → MDE 0.121. 그러나 **verdict set의 실제
   EXP−c0 block-delta sd = 0.5453** (SEM 0.122) — pilot이 분산을 **2.1배 과소추정**했다(6-block sd
   추정의 표집오차 범위 안이긴 함). 따라서 사전등록 `mde_ok=True`("검출력 0 아님")는 참이나,
   verdict set의 실효 MDE는 ~0.255로 사전 MDE의 2배다. **규칙③ 위반은 아니다**(pilot이 분석과
   disjoint하다는 요구는 지킴) — 그러나 "검출력 충분"으로 읽으면 안 된다.
   → 이 약점은 **KILL을 구제하지 않는다**. 오히려 양 seed 모두 잡음이 크다는 뜻이며, 원 run의
   p=.033은 딱 재현 실패하는 종류의 경계 결과다. cement 금지 방향으로만 작용.
2. **V2가 아니었으면 KILL이 cement될 뻔했다.** `all_deg_or_ns = True`(3 control 전부 t ≤ 2.093)
   이므로 V2만 통과했다면 사전등록 분기는 `FAIL_CLOSED`(= KILL cement)를 반환했을 것이다. KILL을
   막은 유일한 요소가 V2 게이트다. **요약은 이걸 숨기지 않고 "EXP는 0/3 control 유의 우세 ⇒ PASS
   미실현"으로 정직히 명시**했다. tune-to-red도 tune-to-green도 아님 — 사전등록 분기 순서(V-gate가
   substance를 지배)를 그대로 따랐다.
   ⟹ **"반증"의 사정거리**: 반증된 것은 **KILL의 증거기반(유의 음성)**이지, "organelle lane이 레버다"가
   아니다. 레버 주장은 여전히 미실현(PASS 아님). 요약도 레버를 주장하지 않는다 — scope 정확.
3. **경미**: content/foil 슬롯(a/b/f) vocab은 old와 147단어 공유. 단 주장은 "**cue** 단어 완전
   disjoint"이며 그것은 사실(0 overlap). 재조합쌍·5-tuple 모두 0 overlap이라 데이터 재사용 아님.
4. **경미**: c1 best-constant를 pilot 평균 `max()`로 고름 = 순서통계량. 그러나 (a) **disjoint pilot**에서
   고르고 (b) control을 **더 강하게** 만드는 방향(= PASS에 보수적, KILL에 유리)이라 규칙① 금지의
   취지(하향편향이 KILL을 기계적 생성)에 역행하지 않는다. 게다가 3 control 전부 개별 보고됨.

## 5. 최종

- **refuted = false** — 결론을 깨려 했으나 깨지지 않았다. 사전등록 무결성(sha 일치)·데이터
  disjoint성(직접 검증)·V-gate 위치·분기 실행가능성·parity 0.0 전부 확인.
- **still_invalid = true** — `verdict = INVALID`는 사전등록 코드가 반환한 값 그대로이며 정당하다.
  V2 채널가시성 FAIL ⇒ 이 헤드라인은 이 seed에서 처치 채널을 신뢰성 있게 보지 못한다 ⇒
  **PASS도 KILL도 cement 불가**.
- **원 KILL(#F13 사후 recompute)은 licensed가 아니었고, 새 disjoint seed에서 그 근거가 부호반전 +
  seed-이질성 p=.026으로 재현 실패** ⇒ KILL cement 금지는 옳다.
- 다음 행동이 필요하다면: 이 축은 항목당 |Δ|=0.37~0.80 / signed mean≈0 인 **잡음 지배** 축이다.
  n(blocks)을 실측 sd=0.545 기준으로 재설계(원 효과 −0.209를 80% power로 잡으려면 block 수
  ≈ (2.8×0.545/0.209)² ≈ 53 blocks)하지 않는 한, 어떤 verdict도 seed draw다. **현재 데이터로
  KILL을 재차 시도하는 것은 tune-to-red.**
