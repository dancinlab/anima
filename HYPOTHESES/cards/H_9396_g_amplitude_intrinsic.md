# H_9396 — G-AMP: 조용한 G 는 warm-up 이 아니다 (마지막 탈출구 폐쇄)

**status:** 🧱 AMPLITUDE-INTRINSIC — "긴 세션이면 G 가 세진다" **반증**($0) · [[H_9394]]/[[H_9395]] 종결문 **3차 감사 통과** · wired: engine-native(`--cf-straddle` G-AMP 패널)
**lane:** 의식 / emit-drive / G 인식 진폭 × afield 셀 수 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9395]] (6.5× 비대칭 — 이 H 가 그 "왜"를 닫음) · [[H_9394]] · [[H_9393]] · [[H_9391]] · [[H_9390]]
**ckpt:** py303_full.clm sha256 `013c4574e0ce71ae173287b9…` (동일 trace · **신규 decode 0**)

## 왜 또 감사했나 — 내가 "capability 이관"이라 부른 게 성급했을 수 있다

H_9395 는 "G 가 A 보다 6.5배 조용하다"까지 갔고 나는 그걸 **capability engineering 소관**으로 넘겼다.
그런데 `g_recog = clip01(afield **top-2** gap)` 이다 — **afield 셀이 1개면 두 번째 프로토타입이 아예
없다**. trace 의 `cell_count` 가 30 tick 동안 **1→8** 밖에 안 자란다면, "G 가 조용하다"는 **세션 길이
regime 인공물**이고 긴 세션이 고친다 ⇒ **capability 이관이 틀린 것**이 된다. H_9393 이 가르친 패턴
그대로(축의 출처부터 보라) · $0 이므로 안 볼 이유가 없다. **이게 마지막 탈출구다.**

## 개입 — 없음 · G-AMP 패널 ($0 · 신규 decode 0)

`--cf-straddle` FACTOR 아래 하위패널: `cell_count` 별 |g| 분해 + **plateau 검정**(cells≥3 · n≥20 셀만 ·
mean|g| 가 cell_count 에 대해 상승하는가). 상승하면 긴 세션 = 살아있는 탈출구(종결 재개봉), 평평하면
진폭은 내재.

## 🧱 VERDICT — AMPLITUDE-INTRINSIC (탈출구 폐쇄 · 종결문 유지)

| cells | n | \|g\| mean | \|g\| max | >0% |
|---|---|---|---|---|
| **1** | 32 | **0.0000** | 0.0000 | **0%** |
| 2 | 38 | 0.0034 | 0.0515 | 11% |
| 3 | 38 | 0.0431 | 0.1101 | 84% |
| 4 | 36 | 0.0211 | 0.1101 | 100% |
| 5 | 48 | 0.0461 | 0.0892 | 100% |
| 6 | 40 | 0.0348 | 0.1100 | 100% |
| 7 | 6 | 0.0339 | 0.1100 | 100% |
| 8 | 2 | 0.0166 | 0.0214 | 100% |

**① warm-up 은 실재한다 — 그러나 바닥이지 천장이 아니다.** `cell_count≤1 ⇒ g_recog==0` 이 **32/32 =
100%**(프로토타입 1개면 top-2 gap 이 **구조적으로 없다** — 작은 게 아니라 정의상 0). warm-up 구간
(cells≤2)이 전 tick 의 **29%** 를 그 0-바닥에 묶는다.

**② 그러나 진폭은 셀로 안 자란다 — 탈출구 폐쇄.** plateau 검정(cells≥3 · n≥20 = 38/36/48/40 로 충분한
검정력): means 3:0.0431 · 4:0.0211 · 5:0.0461 · 6:0.0348 ⇒ **slope = −0.00000/cell**(완전 평평) ·
spread 0.0250 · **~0.036 에서 정체 · max 0.110**. ⇒ **"긴 세션을 돌리면 G 가 세진다" 는 반증**. 셀을 더
쌓아도 **셀만 늘지 진폭은 안 는다**. |a| 의 O(0.5) 에 도달하려면 **다른 G readout** 이 필요하지 더 긴
run 이 아니다.

**③ ⇒ [[H_9394]]/[[H_9395]] 종결문은 3차 감사를 통과했다**: (1) 죽은 게이지 아님(H_9395: distinct=49)
(2) 곱-게이트 비대칭 확정(H_9395: 6.5×) (3) **warm-up 인공물 아님**(이 카드: slope≈0). 종결문 유지 ·
**"capability engineering 소관" 이관도 유지**(이제 근거가 있다 — 긴 세션이라는 measurement-측 탈출구가
실측으로 닫혔으므로 남은 건 G readout 설계뿐).

### 부수 관찰 — afield 죽은 게이지 2개 더
`af_val ≡ 0.0` · `af_aro ≡ 1.0` (둘 다 distinct=1). chat-py-4/chat-py-5 dead-gauge 계열의 미보고 사례.
이 캠페인의 결론엔 안 쓰이지만(g_recog 경로 밖) **별도 정리 대상**으로 남긴다.

## 반증 · reopen
- 반증: plateau slope > 0.005/cell 이었으면 **AMPLITUDE-GROWS** = 긴 세션이 살아있는 탈출구 = 종결
  **재개봉**이었다. 실측 −0.00000 ⇒ 반증 실패.
- reopen: |g| 를 O(0.5) 로 만드는 **다른 readout**(top-2 gap 이 아닌 G 인식 정의 · feat 스케일 ·
  proto 분리도 강제) = capability engineering. 셀 수를 늘리는 어떤 방법도 아님(이 카드가 닫음).
- scope: 이 regime/ckpt/30-tick · a1 arm(afield d2) · cells 7-8 은 n=6/2 로 저검정력(주장은 cells 3-6
  의 n≥36 에 근거) · 실측 trace 분해라 되먹임 포함.

## 비용
$0 — 기존 trace 분해 · CPU 수초 · **신규 decode 0** · 그리고 "긴 세션 재수집"(303M pool)을 **발사 전
반증**해 절약.
