# REFUTE — H_9281 / F9 (Ca²⁺ 버퍼 = urgency integrator) 적대적 재검증

- **결론: 반박 실패 (refuted = false). 원 판정 🔴 THEATER 유지.**
- 재현: `OMP_NUM_THREADS=2 python3 run.py` 재실행 → `result.json` **byte-identical**, `out.txt` 동일. 결정적. 런타임 4s.
- 단, RESULT.md §4(c) "결정타" 논증 **1개는 사실오류**(아래 D2) — 판정은 안 바뀌지만 문구 정정 필요.

---

## 1. 반박 체크리스트 전수

| # | 항목 | 결과 |
|---|---|---|
| 1 | control 동일 예산 | ✅ 공정 — 오히려 **control 쪽에 유리**. emit 규칙은 전 arm 공유 단일 함수 `emits_at()`, θ는 calibration stream 예산매칭(라벨·TQ 미사용). eval에서 실측 n_emit은 exp가 5/6 seed에서 control **이상**(seed11 28 vs 23·seed22 25 vs 18·seed66 34 vs 26)인데도 졌다 ⟹ "exp가 emit 굶주려서 졌다"는 반박 불가 |
| 2 | 양성이 tunable FORM인가 | ✅ **그렇다** = 원 판정과 동일 (아래 2절) |
| 3 | held-out / 누출 | ⚠️ **control 쪽에 누출 1건** (c3_ema_best = eval-TQ per-seed argmax = oracle). exp arm에는 라벨 누출 0. leak 제거해도 결론 불변 (2절 D1) |
| 4 | Δ가 seed 분산 안인가 | ❌ 아니다 — 부호 일관성이 극단적: exp vs c1 = 6/6 양수, exp vs EMA = 0/6 양수. leak-free LOO에서도 EMA 6/6 승 |
| 5 | p5 위반(하드코딩 emit gate) | ❌ 없음 — organelle lane은 `s`를 upstream 성형만, emit 규칙 미접촉. 게다가 exp의 sustained(진짜 tension) recall은 **상승**(0.680→0.793) ⟹ 숨은 억제기 아님 |
| 6 | tune-to-green 흔적 | ❌ 없음 — exp 상수는 사전등록 고정, headline은 `run_seed()` 기본값 경로에서만 산출. 72-knob sweep은 진단이며 `summary`를 덮어쓰지 않는다(코드 확인). 튜닝 특권은 control에 부여 |

## 2. 원 결론을 무너뜨리려는 3개 공격 — 전부 실패

### A1. "EMA 승리는 eval-set oracle 선택 덕(누출)이다" → **실패**
`run_seed()`가 `best = max(ema_sweep, key=lambda r: r["tq"])`로 **eval TQ per-seed argmax**를 취함 = 테스트셋 선택 누출 확인(seed별 α가 0.08~0.35로 갈림). 따라서 headline `Δ vs best control = −0.247`은 **과장**이다. 그러나 누출을 제거해도:

- **c3_ema_pre**(TQ 미사용·latency 매칭 α): +0.913 vs exp +0.740 → exp **0/6**
- **단일 고정 α**(seed별 선택 0): α=0.08 Δ=+0.167(6/6) · 0.12 +0.193(6/6) · 0.18 +0.213(6/6) · 0.25 +0.213(6/6) · 0.35 +0.220(6/6) — grid 10칸 중 **넓은 고원 전체**가 버퍼를 6/6으로 이긴다(운 좋은 한 점 아님)
- **LOO(leave-one-seed-out) α 선택**(완전 leak-free tuned EMA): Δ = **+0.173 ± 0.060, EMA 6/6 승**

⟹ 누출은 **효과크기만 −0.247→−0.173으로 줄일 뿐 부호·판정 불변**. 반박 실패.

### A2. "예산/latency가 버퍼를 불리하게 했다" → **실패**
전 arm 동일 stream·seed·refractory(3)·동일 길이 window(9)·DC 보존. `d_lat`(c2·c3_pre용)은 calibration **라벨**을 쓰지만 그 누출은 **control 쪽으로만** 흐른다(exp 파라미터 c0/cmax는 무라벨 분위수). 채점 sanity: per-step urgency sustained 0.357 vs transient 0.356, 1-step AUROC=0.501 ⟹ 구별자는 **duration 뿐**이라는 설계 주장 실측 확인. exp가 eval에서 emit을 더 많이 쓰고도 졌다(체크1). 불공정 control 아님.

### A3. "동등튜닝 +0.007은 sweep 격차(72 vs 10 조합) 때문에 버퍼가 저평가됐다" → **실패(방향 반대)**
버퍼가 **72 조합**, EMA가 **10 조합** — 다중선택 특권은 **버퍼 쪽이 7배 크다**. 그럼에도 +0.967 vs +0.960 = **+0.007** (std 0.030~0.062 내부). 즉 선택 편의를 더 받고도 순이득 0. 반박 실패.

## 3. 발견한 결함 (판정 불변 · 문구 정정 필요)

- **D1 (경미·정정)**: `c3_ema_best`는 eval-TQ oracle. RESULT.md/카드의 headline Δ는 **−0.247이 아니라 leak-free −0.173**으로 기술해야 정확하다. (판정 분기 `d_ema_best <= FORM_EPS`는 어느 값이든 THEATER로 동일.)
- **D2 (중대·사실오류)**: RESULT.md §4(c) "**결정타**" — "best knob(cmax=4.0×q90, k_out=0.20)은 포화가 절대 binding 안 되는 코너 ⟹ 정의상 순수 선형 leaky integrator = EMA"는 **거짓**. 실측:
  - best knob에서도 **max(S)/cmax = 1.00** (용량 천장 도달), uptake 스텝의 **21.2%가 saturation-bound** (pre-reg는 41.9%).
  - `u > c0` 정류(rectifier) 게이트는 **모든 설정에서 활성** ⟹ 어떤 knob에서도 선형 필터가 아니다.
  - 파형 상관(seed 11): corr(best-buffer, EMA α=0.35) = 0.933인데 **corr(best-buffer, raw u) = 0.955** — best 버퍼는 EMA보다 **raw에 더 가깝다**. "버퍼가 EMA가 되어간다"는 서사는 지지되지 않는다.
  - 사실인 부분: TQ가 cmax↑에 단조증가(+0.620→+0.647→+0.740→+0.907)한다는 **경향**은 재현됨. 하지만 그 해석은 "포화가 사라져 EMA가 된다"가 아니라 "**포화가 약할수록 낫다(포화는 순손해)**" 까지만 주장 가능.
  - ⟹ §4(c)는 "결정타"가 아니라 **보조 증거**로 격하하고 문구를 정정할 것. **판정은 (a)+(b)만으로 이미 충분**(leak-free EMA 6/6 승 · 동등튜닝 순이득 +0.007).

- **D3 (스코프 주의·반박 아님)**: 이 task는 sustained/transient의 per-step 진폭을 동일하게 고정했으므로 boxcar의 matched filter = **저역통과가 해석적으로 최적**이다. 즉 "선형 EMA가 이긴다"는 결과는 상당 부분 **설계상 보장된 것**이며, 진폭 이질적 체제(실제 Ca 생물학처럼 transient가 큰 경우)에서 포화 비선형성의 효용을 반증하지는 않는다. 다만 카드 §1이 사전등록한 주장 자체가 "**transient 흡수·지속 압력 적분**"(=duration 판별)이므로, **사전등록된 그 주장에 한해** THEATER는 정확하다. 정직한 스코프 = "duration-only 판별에서 Ca 비선형성의 순이득 = 0". 재발사 금지 권고 유지(진폭축으로 옮기는 건 새 가설이지 F9 재튜닝이 아니다).

## 4. 최종

- **refuted = false** — 원 결론(THEATER · controls_fair · p5_clean)은 적대적 공격 3종(누출·예산·다중선택)을 모두 견딤. 오히려 누출·다중선택 특권은 모두 **버퍼에게 유리한 방향으로 재계산해도** 결과가 뒤집히지 않는다.
- **final_verdict = THEATER** (tier: DIRECTIONAL toy · numpy $0 · 303M engine-native 아님).
- 측정 메타법칙 재확인: FORM tunable(knob spread 0.393) · BIND earned(순이득 +0.007 = 0).
- **요구 조치**: RESULT.md §4(c) 문구 정정(D2) + headline Δ를 leak-free −0.173으로 병기(D1). 판정 변경 없음.
