# REFUTE — F4 / H_9276 적대적 재검증

**판정: 원 결론(THEATER) 반박됨 → DIRECTIONAL-POSITIVE**

원 보고서의 수치는 **전부 정확히 재현**된다(result.json 대조 완료). 조작·체리피킹 없음.
그러나 결론 문장 — "역행신호는 구조 레인에서도 아무 일도 하지 않아(Δ≤0) ... 아무 데서도
일하지 않는 신호의 disjointness는 공허하며 카드 FAIL('구조 Δ≈0')이 발동했다" — 은
**두 개의 독립적 오류** 위에 서 있다. 둘 다 $0으로 반증된다.

---

## 오류 1 — 통계: `mean ≪ 1 std = 무의미`는 유효한 검정이 아니다

보고서는 SECONDARY(절대 setpoint) 렌즈를 이렇게 기각했다:

> Δ(EXPabs−c0) = +0.380 ± 1.585 (3/5 양) → mean ≪ 1std = **무의미**
> Δ(EXPabs−c1) = +0.656 ± 1.406 (4/5 양) → mean < 1std = **무의미**

**1.585는 per-seed std이지 평균의 표준오차가 아니다.** paired-CRN 설계에서 유의성은
SEM = std/√n 로 판단한다. n=5에서 SEM=0.709 → t=+0.54. 올바른 n=5 판독은
"무의미(=효과 없음)"가 아니라 **INCONCLUSIVE(검정력 부족)** 이다. 효과 없음을
입증한 게 아니라, 있는지 없는지 말할 수 없는 상태였다.

seed를 5→30으로 올리면(하이퍼·배선·fitness·컨트롤 전부 원본 그대로, **오직 n만 증가**):

| Δ (30 seed, paired) | mean ± std | SEM | t | 양seed |
|---|---|---|---|---|
| **PRIMARY** EXP−c0 (z-tonic) | −1.006 ± 1.768 | 0.323 | **−3.12** | 9/30 |
| **PRIMARY** EXP−c1 | −1.194 ± 1.796 | 0.328 | **−3.64** | 9/30 |
| **SECONDARY** EXPabs−c0 | **+1.472** ± 1.465 | 0.268 | **+5.50** | 23/30 |
| **SECONDARY** EXPabs−c1 (동일 multiset) | **+0.877** ± 1.277 | 0.233 | **+3.76** | 24/30 |
| ORACLE−EXPabs (잔여 헤드룸) | +1.307 ± 0.914 | 0.167 | +7.83 | 28/30 |

**나는 green이 나올 때까지 seed를 늘린 게 아니다.** 두 렌즈를 동시에 한 번 올렸고,
PRIMARY는 오히려 **유의하게 더 음수**가 됐다(t=−3.12). 방향 무관하게 검정력만 올린 것 →
tune-to-green 아님. 결론: **PRIMARY 사망은 더 강해지고, SECONDARY는 살아난다.**

## 오류 2 — 인과: 깨진 컨트롤러의 실패를 "신호의 무정보"로 일반화

보고서는 PRIMARY 실패의 진짜 원인을 **스스로 정확히 진단해놓고**("causal z-score는 평균 0 →
미분만 나르고 절대 레벨을 못 나름") 그 진단을 **신호 전체의 사형선고로 확대**했다.

`z = (R − EMA(R))/σ` 는 **setpoint가 없는 자기추적 항등식**이다. R이 4.2든 0.5든 EMA가 따라붙어
z→0 → g→0.5 → 무편향 랜덤워크. 즉 **표류해서 도달한 아사 수준을 그대로 고착**시킨다:

```
seed0  z-tonic: R=4.17  mean_n=16.5  shortfall=0.542   <- 용량의 4배 과부하를 "정상"으로 고정
seed0  abs    : R=1.13  mean_n=32.3  shortfall=0.067   <- load==capacity로 실제 조절
```

R≈4.2 = 만성 4배 과부하. PRIMARY는 "ROS가 정보를 나르는가"를 검정한 게 **아니라**,
setpoint 없는 항상성 루프가 작동 불가함을 검정했다. 이건 **컨트롤러 사실이지 신호 사실이 아니다.**
카드 FAIL 조건("구조 Δ≈0 = 역행 무정보")의 괄호 안 인과귀속이 틀렸다.

---

## 검증: SECONDARY 양성은 FORM(레벨 효과)인가? — 아니다. 두 관문 통과

원 c0(`g=mean(g_EXP)`)는 **최적 상수가 아니다** → 약한 null. 그래서 더 센 컨트롤 2개를 붙였다.

### 관문 A — setpoint가 튜닝된 knob인가? (θ 스윕)

| θ | EXPabs fit | Δ(c0) t | Δ(c1) t |
|---|---|---|---|
| 0.6 | +1.62 | +0.90 | +2.17 |
| 0.8 | +2.02 | +2.60 | +3.19 |
| 0.9 | +2.04 | +3.02 | +3.63 |
| **1.0 (사전등록)** | +2.21 | **+5.50** | **+3.76** |
| 1.2 | +2.51 | +6.25 | +5.18 |
| 1.5 | +2.36 | +6.15 | +5.92 |
| 2.0 | +2.21 | +5.18 | +4.09 |

θ=0.6~2.0 **전 구간에서 c1을 이긴다**(t=+2.2~+5.9). knife-edge 아님 = tunable FORM 아님.
게다가 사전등록 θ=1.0은 **최적점도 아니다**(1.2~1.5가 더 좋음) → 튜닝 흔적 없음(정직성 확인).

### 관문 B — "그냥 풀을 더 키운 것" 아닌가? (최선의 open-loop 상수 null)

상수 g 그리드 전수(30 seed). 상수는 어떤 값을 골라도 **rent-shortfall 트레이드오프를 못 벗어난다**:

| const g | fit | mean_n | shortfall |
|---|---|---|---|
| 0.50 | +0.05 | 15.8 | 0.551 |
| **0.55 (최선)** | **+0.95** | 27.1 | 0.238 |
| 0.60 | +0.13 | 37.2 | 0.067 | ← shortfall은 EXPabs급인데 rent가 이득을 먹음 |
| 0.70 | −1.79 | 44.9 | 0.008 |

> **EXPabs +2.208 vs BEST-const +0.945 → Δ = +1.263 ± 1.423, SEM 0.260, t = +4.86, 25/30 양**

EXPabs는 mean_n=31.6에서 shortfall=0.071을 달성한다 — **어떤 상수도 도달 못 하는 좌표.**
상수는 shortfall 0.067을 사려면 n=37.2까지 키워 rent로 다 토해낸다. 즉 이득의 원천은
"더 키움"(레벨/FORM)이 **아니라** 동적 배분(과부하 시 성장·여유 시 가지치기)이다 = earned BIND.

### 예산 공정성 (INVALID 배제)
구조 이벤트 EXPabs 297.1 / c0 296.2 / c1 296.6 / ORACLE 299.0 — 매칭. CRN u-stream 공유.
컨트롤러 형태·파라미터 수 동일(상수 1개 vs setpoint 1개). c1은 g multiset 완전 동일.
**컨트롤 불공정 없음 → INVALID 아님.**

---

## 원 보고서에서 **살아남는** 것 (정직하게)

1. **PRIMARY(z-tonic) 배선은 진짜 죽었다** — 보고서보다 더 심하게. 30 seed에서 t=−3.12로
   **유의하게 유해**. 이 부분은 오히려 과소보고됐다.
2. **emit disjointness는 유지된다** — 30 seed dAUC(c2−E0): emit_on_exp **−0.0005 (t=−0.12)**,
   emit_on_c0 +0.0083. Δprec 음수. ROS-only AUC 0.52~0.53. **PASS-2(ΔEff≈0) 충족.** p5 위반 없음
   (emit은 학습된 로지스틱 스코어, 하드코딩 게이트 0 · held-out 1/2 분할 정상).
3. **corr(n,d) = FORM 함정이라는 지적은 옳다** — 그리고 내 재분석이 이를 **더 강하게** 입증한다:
   abs-setpoint 배선은 corr(n,d)가 **고작 +0.088**인데 fitness는 강한 양수(+2.21)다. 반대로
   z-tonic은 corr=+0.375(오라클급!)인데 fitness는 음수. **corr과 earned fitness가 배선 간
   역상관** → "corr을 리포트했으면 거짓 GREEN"이라는 교훈은 그대로 성립. 메타법칙 무사.

## 무너지는 것

- ❌ "유의한 구조 fitness Δ = 없음" → **거짓.** +1.47/+0.88/+1.26 vs 3개 컨트롤, t=3.8~5.5.
- ❌ "아무 데서도 일하지 않는 신호(vacuous disjointness)" → **거짓.** 구조 레인에서 일한다.
  disjointness는 공허하지 않다 — **일하는 채널이 emit을 안 건드리는 것** = a_substrate_disjoint 실증.
- ❌ 카드 FAIL "구조 Δ≈0" 발동 → **오발.** 사전등록 PASS 3조건(구조 Δ>0 · emit ΔEff≈0 ·
  c1로 이득 소멸) **전부 충족**(abs-setpoint 배선).
- ❌ verdict THEATER → **THEATER 아님.** THEATER는 "FORM은 빛나는데 earned는 0"인데, 여기선
  FORM(corr)은 죽어있고 earned(fitness)가 살아있다. 정확히 THEATER의 **반대**.

## 남는 한계 (그래서 GREEN이 아니라 DIRECTIONAL)

- **toy numpy** — engine-native `core/` decode 아님(`a_engine_native_learning` · toy=DIRECTIONAL).
- **미배선** — `core/` + ARCHITECTURE.json lockstep 없음(`a_verified_must_wire`).
- **ORACLE 헤드룸 잔존** — ORACLE−EXPabs = +1.31 (t=7.8). ROS는 손실 있는 프록시지 천장 아님.
- **toy 내재 관대함** — `ROS_i = load/cap_i`는 사실상 수요/공급 충분통계에 가까워, 이 서브스트레이트는
  가설에 유리하게 기울어 있다. "온도조절기가 open-loop를 이긴다"는 결과가 anima 실체(303M)로
  전이된다는 보장은 없다(`a_toy_scale_recheck`).

## 권고

1. F4를 THEATER/KILL로 매장하지 말 것. **DIRECTIONAL-POSITIVE**로 재등록.
2. 카드 H_9276 정정: PRIMARY 배선(z-tonic)을 **🧱 KILL(컨트롤러 결함 · setpoint 부재)** 로 분리하고,
   SECONDARY(absolute setpoint)를 **본선**으로 승격. 진짜 교훈 =
   **"역행신호는 정보를 나른다. 나르지 못한 건 z-score 항상성 루프였다"** (신호≠컨트롤러).
3. `mean vs 1·std` 기각 휴리스틱을 랩 전역에서 폐기 — SEM/paired-t 사용. n=5는 |Δ|≈0.4급
   효과에 대해 구조적으로 검정력 부족. **F2/F3/F5/F10이 이 H에 물려 있으므로**(카드 §5),
   같은 5-seed·std-기각 패턴으로 내려진 형제 verdict들을 재감사할 것.

---
_재현: `python3 run.py` (원본 5-seed) · 검증 스크립트는 seed만 30으로 올리고 `run.py`의
`one_seed`/`one_seed_abs`/`run_sim`/`fitness`를 그대로 import — 상수·배선·fitness 무수정._
