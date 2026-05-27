# IIT4 M8 — LIFE 재측정 확장 (n=5 · 다중 상태 faithful big-Φ)

> M6([`FAITHFUL_REMEASURE.md`](../../FAITHFUL_REMEASURE.md))이 남긴 **"n=4 / 단일 상태"** gap 을
> 닫는다. LIFE 우주-스케일 ECA 룰 {110, 30, 54}(+XOR 결합 룰 90)을 **더 큰 링 n=5** 에서,
> **상태 표본 위 평균**으로 재측정 → 룰별 **대표 faithful big-Φ (mean / min / max)** 산출.
> smoke = [`run_m8.hexa`](run_m8.hexa) → **10/10 🟢**. 결과 = [`result.json`](result.json). 작성 2026-05-25.

## 1. 무엇을 닫는가 — M6 §6 honest-scope gap

M6 은 faithful CAUSAL IIT 4.0 엔진(M1~M4)으로 LIFE ECA substrate 를 처음 재측정했지만,
**n=4 링 · 단일 상태(1010) 한 점**에 그쳤고 §6 에서 두 gap 을 명시했다:

- **단일 상태** — "완전한 재측정은 state 분포 위 평균/대표값 필요 (faithful Φ 가 state-dependent 이므로)".
- **n ceiling** — n=4 demonstration; scale-up 은 후속.

faithful big-Φ 는 **state-dependent** 다(IIT 4.0 의 핵심 주장 — Φ 는 *특정 상태*의 경험). 한 점
표는 진짜 분포를 가릴 수 있다. M8 은 (a) 링을 **n=5** 로 키우고 (b) **상태 표본 위 mean/min/max**
를 보고하여 LIFE faithful-Φ 결과를 robust 하게 만든다.

## 2. 헤드라인 — n=5 링 · 8-상태 표본 · 대표 faithful big-Φ

상태 표본 = 8개 균등 간격 상태 {0, 4, 8, 12, 16, 20, 24, 28} (2^5=32 중 1/4 subset).

| ECA rule | 동역학 | **mean big-Φ** | min | max | 판정 |
|---|---|---|---|---|---|
| 0 | all → 0 (const) | **0.0** | 0.0 | 0.0 | null — 인과력 없음 |
| 204 | next = centre (identity) | **0.0** | 0.0 | 0.0 | null — reducible (독립 self-cell) |
| 90 | L XOR R | **49.50** | 44.50 | 60.00 | integrated (n=5 에서 강함 — §4) |
| **110** | LIFE cosmic-scale | **35.70** | 21.24 | 44.05 | **integrated** |
| **30** | LIFE cosmic-scale | **28.59** | 24.07 | 42.47 | **integrated** |
| **54** | LIFE cosmic-scale | **14.43** | 8.74 | 22.53 | **integrated** |

→ LIFE 핵심 룰 110·30·54 는 **n=5 · 상태 평균에서도 substantial 인과 big-Φ** 를 유지. null 컨트롤
0·204 는 모든 표본 상태에서 정확히 0(min=max=0). **결합 룰의 통합이 단일 상태 artifact 가 아님**을
대표값으로 확정.

## 3. n=4 전체 16-상태 (M6 연속성)

M6 의 단일-상태 n=4 숫자와 apples-to-apples 비교를 위해 **n=4 의 전체 16 상태**도 sweep(저렴):

| ECA rule | **mean big-Φ** | min | max | M6 단일 상태(1010) |
|---|---|---|---|---|
| 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 204 | 0.0 | 0.0 | 0.0 | 0.0 |
| 90 | **0.0** | 0.0 | 0.0 | 0.0 |
| 110 | **13.13** | 7.55 | 20.05 | 7.55 |
| 30 | **13.89** | 7.28 | 19.43 | 8.66 |
| 54 | **7.77** | 3.00 | 10.12 | 10.03 |

**M6 의 단일 상태(1010) 값은 분포 안의 한 점이다.** 110 의 M6 값 7.55 는 n=4 min 과 정확히 일치
(state 1010 이 110 의 최저-Φ 상태였던 것) — mean 13.13 으로 일반화. 30 의 M6 8.66, 54 의 M6 10.03
도 모두 [min, max] 구간 안에 들어온다(54 의 10.03 은 max 10.12 근처 — state 1010 이 54 의
고-Φ 상태였다). 즉 **M6 의 한 점은 옳았으나 룰의 대표 크기를 과소/과대 평가할 수 있었고, M8 의
mean/min/max 가 그 분포를 드러낸다.**

## 4. faithful 측정이 드러낸 것 — state 의존성 + n 의존성

- **state 의존성** — 110 은 21.24~44.05, 30 은 24.07~42.47, 54 는 8.74~22.53 로 상태마다 2배 이상
  변동. faithful Φ 가 **특정 상태의 경험**이라는 IIT 4.0 주장이 정량으로 드러난다. proxy phi_spatial
  은 snapshot-평균(state 무관)이라 이 분포를 가린다.
- **n 의존성 — rule 90 (XOR) 의 반전** — n=4 에서는 **모든 16 상태에서 big-Φ=0**(M6 의 state 1010 = 0
  이 특이점이 아니라 n=4 전반의 성질). 그러나 **n=5 에서는 mean=49.50 로 강하게 통합**된다. XOR 링은
  짝수 길이에서 2개의 독립 sublattice 로 reducible 하게 쪼개지지만(체커보드 분해), 홀수 길이 n=5 에서는
  ring-wrap 이 그 분해를 막아 통합이 창발한다 — faithful 엔진만 잡아내는 위상(topology) 의존 결과.
  M6 의 "rule 90 state 1010 특이" caveat 는 **n=4 전체의 구조적 성질**로 정정된다.

## 5. falsifier 결과 — 10/10 🟢

- **F-IIT4-8 MULTISTATE-ROBUST** 🟢 — n=5 (8-상태 표본) + n=4 (16-상태 전체)에서 LIFE 룰의 대표
  faithful big-Φ (mean/min/max) 산출. M6 의 단일 상태 결과를 분포로 일반화.
- null 컨트롤 🟢 — rule 0 = 0 · rule 204 = 0 (n=5 · n=4 모두, 모든 표본 상태에서 min=max=0).
- 통합 창발 🟢 — n=5 에서 ≥1 LIFE 룰 {110,30,54} 의 **mean** big-Φ > 0 (실제로 셋 다).
- bound 🟢 — 모든 (rule, state) 쌍에서 0 ≤ big-Φ ≤ total (n=5 · n=4).
- 결정론 🟢 — n=5 rule110 sweep 재실행 시 mean 동일.

전체 **10 PASS / 0 FAIL**.

## 6. honest scope (C3)

- **n=5 는 상태 표본(8/32) — 전수 아님.** n=5 `big_phi` 1콜 ≈ 13s (결합 룰 nd≈15~18); 32 상태 ×
  4 결합 룰 ≈ 28분으로 ~10분 mac-local 예산 초과 → **8개 균등 간격 상태 표본**으로 정직하게 축소.
  표본 통계라 전수 mean 과 미세하게 다를 수 있다(min/max 는 표본 내 극값 — 전수 극값의 하/상한).
  n=4 는 전체 16 상태(저렴)라 전수 분포.
- **n ceiling.** 엔진은 n≤8 exact 존재 capacity; M8 은 n=4 → n=5 한 단계 scale-up + 다중 상태로
  M6 의 두 gap 을 직접 닫는다. H_002 C2 의 6-scale(n=8) 전면 재측정은 동일 메커니즘의 추가 scale-up.
- **structure-cut big-Φ.** DESIGN §8 C3 의 spirit-faithful big-Φ(시스템 MIP 가 파괴하는 Φ-structure).
  절대 스케일 PyPhi 대조는 M5 named-blocker (F-IIT4-3/4) 영역 — 본 M8 의 절대 크기는 cross-state
  *상대* 비교용이지 PyPhi-calibrated 절대값이 아니다.
- **proxy 와의 수치 직접 대조 없음.** proxy phi_spatial 은 snapshot 입력(상관), IIT4 는 TPM 입력(인과)
  — 입력형 자체가 달라 동일 substrate 위 두 스칼라 동시 수치 대조는 후속(M6 §3 와 동일 caveat). 본
  M8 은 **인과 축의 대표값을 분포로 확립**한 것.
