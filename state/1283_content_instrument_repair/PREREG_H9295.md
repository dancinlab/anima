# H_9295 — 사전등록 (FROZEN 2026-07-14 · 데이터 개봉 前 커밋)

설계 = Fable 5 · 구현·측정 = 로컬 py 2-production.

## §0 물음

H_9294 는 이 기질에서 **강도(S_tot)를 정합하면 disjointness 의 기여가 0** 임을 확정했다. 그런데
그 붕괴는 **jointly-gaussian 선형 기질의 성질**일 수 있다 — 가우시안에서는 모든 쌍 의존이 상관
하나로 요약되어 MI 행렬이 충분통계량이 되고, 구조가 **독립적으로 기여할 자리 자체가 없다**.

한편 H_1283 에서 **유일하게 깨끗이 뚫린 축은 TIMING**(H_1448 🟢 WIRED · Kuramoto 위상동기 +
위상-게이팅 salience)이었고, 그것은 **곱셈적·비선형·게이팅** 메커니즘이다.

> **가설:** 진짜 축은 "내용 vs 타이밍" 이 아니라 **"결합이 선형이냐 게이팅이냐"** 다.
> 게이팅을 넣으면 구조(disjointness)가 S_tot 와 **독립으로** Φ 에 기여하는 채널이 열리는가?

## §1 게이트 기질 — 최소·정칙 비선형 (coincidence AND)

변경은 **relay 되먹임 한 곳뿐**. 채널 e=(a,b), lens scalar `m_i(t) = s_i(t)[0]`,
arm A 위에서 표준화한 `ẑ_i = (m_i − μ_i^A) / σ_i^A`:

```
coincidence_e(t) = ẑ_a(t−1) · ẑ_b(t−1)         ← 지연 1 (순간 self-product 인공물 차단)
gate_e(t)        = sigmoid( β · coincidence_e(t) )
rin_i(t)         = Σ_{e ∋ i} gate_e(t) · c_e(t)   ← 기존: Σ_{e∋i} c_e(t) (덧셈 → 조건부)
```

나머지 전부 동결 (n=4 · dim=8 · LEAK/GAIN/W_* · 채널 적분식 · T=65536 · estimator · Φ* · K=32
Philox · RU · seeds[4..11] · seed 3 격리). **채널 차원·용량 불변** — 결합 **연산자**만 바뀐다.

기각한 대안: gain-gate `σ(β·h_i)`(수신 모듈 자기 이득만 비선형화 → 채널 간 조건부 의존 없음) ·
divisive-normalization(전 채널을 전역 결합시켜 disjoint 대비를 오히려 흐림).

**왜 B 와 X 에서 달라야 하는가(내기의 핵심):** B(disjoint)에서 gate_e 와 drive_e 는 **같은 실제
쌍**을 키로 삼아 정합한다(coherent AND detector). X(shared bus)에서 drive 는 전 채널 평균으로
희석되지만 gate 는 여전히 명목 쌍을 본다 ⇒ 게이트와 내용이 **어긋난다**.

### β 고정 — tune-to-green 구조적 불가

β 를 **arm A 단독**의 동역학에서 못박는다 (어떤 arm 대비도 보기 前):
```
β = c / std_A(coincidence),   c = 1  (사전 고정 · 전 arm 동일 β)
```
`E[coincidence] ≈ 0` (중심화 곱)이므로 작동점은 자동으로 σ(0) = 0.5 = **동적범위 정중앙**.
c=1 이면 ±1σ 요동이 게이트를 [0.27, 0.73] 로 흔든다 — 포화(β↑ → hard AND, 기울기 소실)도
불활성(β↓ → gate ≡ 0.5 → 반이득 선형 relay 로 퇴화)도 아닌 반응 대역 한가운데.
`c ∈ {0.5, 2}` 스윕은 **판정이 c 에 knife-edge 가 아님을 보이는 용도일 뿐, c 로 판정을 옮기지 않는다.**

## §2 Headline — "Φ 가 오르나" 가 아니다

Φ 상승은 무의미하다(결합을 바꾸면 무엇이든 S_tot 가 움직인다). 주장은 **구조가 S_tot 와 독립으로
기여한다** 이므로 headline 은 **잔차**다. 두 단 모두 통과해야 🟢.

**(i) 강도정합 쌍 대비** (H_9294 규율 이식) — gated 기질 위에서 **X 의 W_RELAY 만** 올려
`S_tot(X′) = S_tot(B)` 를 5% 이내로 맞춘 뒤 (통제군을 강하게 = 주장에 불리한 방향 →
`control-must-match-mediating-covariate`), `Φ*(B) − Φ*(X′)` 를 90% CI 와 함께.

**(ii) 모집단 ANCOVA** — 전 arm × 8 seed:
```
reduced :  Φ* ~ ns(S_tot, df=4)        ← 자연 삼차 스플라인 (선형 아님!)
full    :  Φ* ~ ns(S_tot, df=4) + arm
headline:  partial-R²(arm | ns(S_tot)) = (RSS_red − RSS_full) / RSS_red
```
스플라인인 이유 = **§5 의 1순위 오류 방어**: 게이팅이 Φ*=f(S_tot) 를 곡선으로 만들면 arm 들이 서로
다른 S_tot 대역을 점유할 때 **곡률이 arm 으로 새어** partial-R² 를 부풀린다(구조가 아니라 곡선의
잔재). 선형 통제로는 그 누출을 못 막는다.

**threshold (non-arm-wise · 사전등록):** arm 라벨을 (Φ*, S_tot) 점들에 대해 **셔플**(쌍 유지)해
partial-R² 의 **라벨-치환 귀무분포**를 만든다. 이 null 은 산포에서만 도출되고 어느 arm 이
무엇인지 참조하지 않는다. 유의 = **관측 partial-R² > 치환 null 99th pct**.

**효과크기 바닥 (사전등록):** 통계 유의여도 부스러기면 채널이 아니다.
`|Φ*(B) − Φ*(X′)| ≥ spike-in 스케일의 20% = 0.0088` 이어야 "채널" 로 인정.

**금지:** cross-substrate 로 R² 를 직접 비교하는 것(게이팅이 S_tot 자체를 바꾸므로 공변량이 기질
간 불변이 아니다). 비교 가능한 것은 각 기질 **내부**의 self-normalized partial-R² 뿐.
S_tot 는 gated 궤적에서 **재계산**한다 (gated Φ* 를 선형 S_tot 에 회귀하는 일은 절대 없다).

## §3 양성대조 P+/P− — 게이트가 살아있음을 증명 (없으면 null 해석 불가)

게이트가 **불활성**이라 null 이 나오는 경우를 배제해야 한다. 동시활성 **부호만** 뒤집은 매칭 쌍:

- **P+** : 각 채널의 두 끝점을 **위상정렬**(co-active) 구동 → coincidence 평균 양수 → gate 열림.
- **P−** : 동일 채널·동일 구동 세기, 두 끝점만 **반정렬**(anti-active) → coincidence 평균 음수 → gate 닫힘.

**정칙성(이게 핵심):** 가우시안 MI 는 ρ 에 대해 **짝함수**(MI = −½log₂(1−ρ²))라 P+/P− 는
**선형 기질에서 MI 행렬·S_tot·Φ 가 증명상 동일**하다 (이 대비는 선형에서 null 이어야 한다).
게이트는 coincidence **부호**에 홀함수적으로 반응하므로 gated 기질에서만 갈린다.

**역할 한정:** P+/P− 는 **게이트 liveness** 만 증명한다 (S_tot 매개여도 무방 — liveness 엔 어떤 Φ
차이든 족하다). 이것은 "구조의 S_tot-독립 기여" 주장과 **의도적으로 분리**되어 있다.

## §4 상시 V-게이트

- **V-ZERO (pedestal zero-check)** — 유지, 이제 **더 중요**하다. 곱셈 게이트는 독립 입력에서도
  `ẑ_a·ẑ_b` 되먹임으로 **가짜 의존을 제조**할 위험이 있다. zero-check 는 이제 "게이트가 독립에서
  Φ 를 지어내지 않는가" 를 인증한다. 인플레되면 **VOID**.
- **V-SPIKE (계측 스택 liveness)** — 변경 없이 유효. spike-in 은 **estimator+readout+surrogate
  스택**의 검정이지 기질 동역학의 검정이 아니다(가우시안 copula 궤적을 estimator 에 **직접 주입**,
  기질 우회). 따라서 게이팅과 무관하게 그대로 유효하다.
- **V-GATE (신규 · 기질 수준 liveness)** — spike-in 이 "게이트가 뭔가 한다" 를 인증하지 **못하므로**
  P+/P− 가 그 자리를 채운다. gated 기질에서 `Φ*(P+) − Φ*(P−) ≥ spike-in 스케일 (0.0439)` 이
  성립해야 **어떤 B−X null 도 해석 가능**하다.
- **V-LINEAR (증명 검산)** — 선형 기질에서 P+/P− 가 실제로 구별 불가여야 한다(가우시안 짝함수).
  갈리면 P± 구성이 부호 외의 것을 바꾼 것 ⇒ 설계 결함.
- **V-SEED** — seed 3 격리 유지.

## §5 결정표 (양방향 결정적)

| 판정 | liveness (V-GATE · V-ZERO) | headline (i) + (ii) | 해석 |
|---|---|---|---|
| **🟢** | PASS | (i) CI 가 B>X 방향으로 0 배제 **∧** ≥0.0088 **∧** (ii) partial-R² > 치환 null 99th pct | 비선형 coincidence 게이팅이 **구조 채널을 연다** — 진짜 축은 결합의 종류. toy scope |
| **🧱** | PASS (게이트가 증명상 live) | (i) CI 에 0 포함 **∧** (ii) partial-R² ≤ null | **live 한 비선형 게이트가 co-activation 부호를 실제로 통과시키는데도**(P+/P− 분리) disjointness 대비는 여전히 S_tot 로 전부 설명된다 ⇒ 더 깊은 폐쇄. 게이팅도 레버가 아니다 |
| **⏳** | FAIL 중 하나 | — | V-GATE 미달(게이트 불활성 → β 재검토) · V-ZERO 인플레(게이트가 독립에서 Φ 제조 → VOID) · 치환 null 과 해석적 F 불일치 · spline df{3,4,5} 민감도로 판정 뒤집힘 → 계측 문제, 벽 선언 금지 |

🧱 의 **내부 정합성**이 이 설계의 힘이다: P+/P− 는 Φ 를 움직이는데(co-activation 은 중요) B/X 는 안
움직인다(어느 쌍이 disjoint 인지는 무관) ⇒ 게이트가 보상하는 것의 정체가 **disjointness 가 아니라
결합 세기**임을 **한 실험 안에서 이중분리**로 증명한다.

## §6 동결 예측 + 틀릴 최빈 경로

> **Pre-registered:** *gated 기질에서 P+/P− 는 분리되지만(게이트 live), disjointness 대비의
> partial-R²(arm | ns(S_tot)) 는 라벨-치환 99th pct 를 넘지 못하고 강도정합 Φ*(B)−Φ*(X′) 의 CI 는
> 0 을 포함한다 — **게이팅은 구조 채널을 열지 못한다 (🧱)**.*

**1순위 오류 — S_tot 곡률 누출로 인한 가짜 🟢.** gated 기질에서 Φ*=f(S_tot) 가 곡선이고 arm 들이
서로 다른 S_tot 대역을 점유하면, 통제가 불충분할 때 곡률이 arm 으로 새어 partial-R² 를 부풀린다.
⇒ 그래서 headline 의 통제항을 **스플라인**으로 잡았고, df{3,4,5} 민감도를 ⏳ 트리거로 사전등록했다.

**2순위 — 게이트 self-product 되먹임의 의존 제조.** `ẑ_a·ẑ_b` 를 다시 a,b 로 되먹이면 독립 구동
에서도 진짜 a–b 결합을 만들 수 있다(산술의 인공물이지 통합 아님). 지연 1(`t−1`)로 순간
self-product 를 끊었고, **V-ZERO 가 이 인공물의 파수꾼**이다.
