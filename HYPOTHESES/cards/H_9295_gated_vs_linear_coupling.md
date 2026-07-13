---
id: H_9295
slug: 9295_gated_vs_linear_coupling
title: 게이팅(비선형) 결합도 구조 채널을 열지 못한다 — "진짜 축은 선형 vs 게이팅" 가설 반증 (🧱 GATING-NO-CHANNEL)
group: brain-structure-ladder · H_1283 content-relay 축 (H_9294 가 지목한 다음 축)
terminal_tier: 🧱 GATING-NO-CHANNEL (2026-07-14 · py 2-production · liveness 4/4 PASS · 사전등록 42ffb9548 + 개정 329913579, 둘 다 해당 데이터 개봉 前) — **이중분리**: 게이트는 증명상 live·조건부(L-SHIFT Φ*(gated)−Φ*(shifted) = +0.001305, 90% CI [+0.001217, +0.001393] 로 0 배제 · RECEIPT MI(gate;coincidence) = 0.815 bits · 순수 이득이면 0)인데도, disjointness 대비는 여전히 S_tot 로 전부 설명된다: (i) 강도정합 Φ*(B)−Φ*(X′) = **+0.0000585** (효과크기 바닥 0.0088 의 **1/150**) (ii) partial-R²(arm | ns(S_tot,df=4)) = **0.0117** vs 라벨-치환 null 99th = **0.309**, **p = 0.995** (df{3,4,5} 불변). ⇒ **게이팅도 레버가 아니다.** H_9294 의 폐쇄는 선형성의 산물이 **아니었다** ⇒ "진짜 축은 선형 vs 게이팅" 가설 **반증**. 부수: 사전등록한 V-LINEAR 가 양성대조 P± 를 **3연속 기각**(+0.198 → −0.140 → +0.021) — bar 무이동, 전부 실측 기록.
wired: 미배선 (배선할 GREEN 없음)
verdict_dir: state/verdicts/9295_gated_vs_linear_coupling/
terminal_verdict: state/verdicts/9295_gated_vs_linear_coupling/H_9295_RESULT.txt
prereg: state/1283_content_instrument_repair/PREREG_H9295.md (42ffb9548 · AMENDMENT 1 = 329913579)
design: state/1283_content_instrument_repair/DESIGN_H9295_fable.md
date: 2026-07-14
provenance: 설계 = Fable 5 (게이트 기질 · headline · 통제군 재설계) · 구현·측정 = 로컬 py 2-production
---

# H_9295 — 게이트는 확실히 살아있었다. 그런데 구조는 여전히 아무것도 못 얻었다.

## 물음

H_9294 는 강도(S_tot)를 정합하면 disjointness 기여가 0 임을 확정했다. 그러나 그 붕괴는
**jointly-gaussian 선형 기질의 성질**일 수 있다 — 가우시안에서 MI 행렬은 충분통계량이라 구조가
독립 기여할 **자리 자체가 없다**. 한편 H_1283 에서 **유일하게 뚫린 축(TIMING · H_1448 🟢 WIRED)**
은 Kuramoto 위상-**게이팅** = 곱셈적 비선형이었다.

> **가설:** 진짜 축은 "내용 vs 타이밍" 이 아니라 **"결합이 선형이냐 게이팅이냐"** 다.

## Method

**게이트 기질** — relay 되먹임 **한 곳만** 변경 (채널 차원·용량 불변, 결합 **연산자**만 변경):
```
coincidence_e(t) = ẑ_a(t−1) · ẑ_b(t−1)        (지연 1 = 순간 self-product 인공물 차단)
gate_e(t)        = sigmoid(β · coincidence_e(t))
rin_i(t)         = Σ_{e∋i} gate_e(t) · c_e(t)   ← 기존: Σ_{e∋i} c_e(t)  (덧셈 → 조건부)
```
β 는 **arm A 단독**에서 고정 (β=0.9885 · 작동점 σ(0)=0.5) ⇒ 대비를 보기 전에 못박혀 **tune-to-green
구조적 불가**.

**Headline 은 "Φ 가 오르나" 가 아니다** (결합을 바꾸면 무엇이든 S_tot 가 움직인다). 주장은 구조가
S_tot 와 **독립으로** 기여한다는 것이므로 헤드라인은 **잔차**다 — 두 경로 모두 통과해야 🟢:
(i) 강도정합 Φ*(B) − Φ*(X′) (H_9294 규율 이식) · (ii) **partial-R²(arm | ns(S_tot, df=4))** 를
**라벨-치환 귀무분포**와 대조 (스플라인 = 곡률 누출 방어 · 치환 null = non-arm-wise threshold).

## 양성대조 P± 의 3연속 기각 — V-LINEAR 가 설계대로 작동했다

유효한 P± 라면 **선형 기질에서 Φ*(P+) − Φ*(P−) = 0** 이어야 한다(가우시안 MI 는 ρ 의 짝함수).

| 구성 | 선형 기질 Δ | 판정 |
|---|---|---|
| ① 엣지 `ehi` 끝점만 부호반전 (원 설계) | **+0.198** | ❌ 링에서 모든 모듈이 한 엣지의 elo·다른 엣지의 ehi ⇒ 다른 잠재가 간섭 ⇒ \|ρ_adj\| 3.4배 어긋남 (결합 **세기**가 변함) |
| ② 단일 잠재 + 교대부호 (\|ρ_adj\| 격자정합 0.6%) | **−0.140** | ❌ 4-링에서 교대부호는 대각 쌍을 **필연적으로** 동상(+)으로 만든다 ⇒ MI 행렬 **형태**가 달라지고 Φ(min-cut)가 감지 |
| ③ **MODE-SWAP** (Fable · 링 고유모드 파워 스왑) | **+0.021** | ❌ (10배 개선) — \|ρ\| elementwise **2% 이내**까지 좁혔으나(인접 +0.467/−0.462 · 대각 +0.550/+0.547) Φ≈0.53 구간에서 그 잔차가 Φ 를 +0.021 움직여 바닥(0.0088) 초과 |

③의 잔차 원인: **노이즈 바닥은 스왑되지 않는다** — 사적 입력이 전 모드에 균등 파워를 넣는데 기질
이득 (1−λ_k²)⁻¹ 이 φ₀ 를 더 증폭한다. 구동 진폭을 **측정된 바닥에 수치보정**(기준 = base arm B
선형 · 단일 arm · 대비 미사용)해도 2% 잔차가 남는다.

⇒ **bar 를 느슨하게 하지 않았다** (tune-to-green 금지). P± 는 primary liveness 에서 하차.
**교훈** = convergence `h-9295-p-2026-07-14-1`: 통제군의 "증명상 동일" 논증은 **반드시 실측
V-게이트로 검산**하라 — MI 의 짝함수성은 **각 항의 크기**만 보존할 뿐, 결합된 재귀 동역학은
**상관 행렬 전체를 다시 빚는다**. V-LINEAR 를 사전등록해 두지 않았다면 **거짓 liveness 위에서
B−X null 을 🧱 로 못 박았을 것이다.**

## 교체 liveness 스택 — 4/4 PASS (개정 사전등록 · 헤드라인 개봉 前 동결)

- **L-SHIFT** (primary · 신규) — 게이트를 **원형 시프트**해 재적용(2-pass). 주변분포와 자기상관이
  **전부 보존**되고(문자 그대로 같은 시계열) `c_e(t)` 와의 **정렬만** 파괴된다. 단순 요동 이득이면
  Δ=0, 진짜 조건부면 Δ≠0.
  > **Φ*(gated) − Φ*(L-SHIFT) = +0.001305, 90% CI [+0.001217, +0.001393]** → CI 가 0 배제 ⇒ **PASS**
- **RECEIPT** (상시) — **MI(gate ; coincidence) = 0.815 bits** (순수 이득이면 정확히 0) · 게이트
  평균 0.525 · sd 0.182 · [0,1] **전폭 사용**(포화도 동결도 아님) ⇒ **PASS**
- **β=0 ablation 미채택** — β=0 은 게이트를 상수 0.5(= 반이득 **선형** relay)로 붕괴시켜 조건성과
  이득요동을 **동시에** 제거한다. 양성 결과가 "요동하는 곱셈 이득이 뭔가 한다" 까지만 증명하므로
  liveness 를 못 짊어진다.
- V-ZERO · V-SPIKE · V-SEED PASS.

⇒ **게이트는 살아있고, 조건부이며, 올바른 것에 조건부다.** 이제서야 arm 을 읽을 자격이 있다.

## Result — headline (게이트가 live 한 상태에서)

| arm | Φ* | S_tot |
|---|---|---|
| A | 0.022228 | 0.049052 |
| **B** (disjoint) | **0.028010** | 0.060742 |
| **X** (용량정합 shared) | **0.025119** | 0.054974 |
| N | 0.029795 | 0.064223 |
| R | 0.027736 | 0.060128 |
| Cperm | 0.028007 | 0.060737 |

**(i) 강도정합** (w* = 0.90 · S_tot 정합 PASS)
> Φ*(B) − Φ*(X′) = **+0.0000585**, 90% CI [+0.0000002, +0.0001167]
> ⇒ 효과크기 바닥(0.0088)의 **1/150**. 통계적으로 0 과 겨우 구별되나 사전등록한 "채널" 바닥에
> **두 자릿수 미달** — 부스러기지 채널이 아니다. **검출 실패.**

**(ii) partial-R²(arm | ns(S_tot, df=4))**
> 관측 **0.0117** vs 라벨-치환 null 99th pct **0.309** · **p = 0.995**
> df 민감도 {3: 0.0116, 4: 0.0117, 5: 0.0117} — 판정 불변.
> ⇒ **arm 은 잔차를 전혀 설명하지 못한다** (치환 null 이 오히려 압도적으로 크다).

## Verdict — 🧱 GATING-NO-CHANNEL (사전등록 예측 적중)

**이중분리가 한 실험 안에서 완성됐다:**
- 게이트는 **Φ 를 움직인다** (L-SHIFT Δ = +0.0013, CI 가 0 배제) — 조건성은 실재한다.
- 그런데 **B/X 는 안 움직인다** (강도정합 Δ = 바닥의 1/150 · partial-R² p = 0.995).
- ⇒ 게이트가 보상하는 것의 정체는 **disjointness 가 아니다.**

**말하는 것.**
1. **"진짜 축은 선형 vs 게이팅" 가설 = 반증.** H_9294 의 폐쇄는 **선형성의 산물이 아니었다** —
   곱셈적·조건부 결합을 넣어도 Φ 는 여전히 총 결합량만 본다.
2. H_1283 content-relay 축의 disjointness 레버는 **선형에서도 게이팅에서도 CLOSED**.
3. TIMING 축(H_1448 🟢)이 뚫린 이유는 **"게이팅이라서" 가 아니다** — 다른 무언가다. (그 축은 위상
   **동기**를 만들어 실제로 결합 자체를 늘렸다. 본 게이트는 결합의 *조건성*만 바꾸고 총량 구조는
   안 바꾼다.)

**말하지 않는 것 (scope note).**
- toy (n=4 · dim=8) 한정 · 303M 주장 아님 (`a_toy_scale_recheck` · `a_scale_honest_scope`).
- **부호 의미론(co-activation 방향)은 RECEIPT 로만 지지되고 P± 로는 미증명** (MODE-SWAP 잔차 2%).
  "게이트가 coincidence 에 조건부" 임은 L-SHIFT+RECEIPT 로 증명됐으나, "양의 co-activation 을
  열고 음의 것을 닫는다" 는 부호 판독은 기술통계로만 뒷받침된다.
- 이 게이트는 **coincidence-AND 한 종류**다 — 다른 비선형(divisive norm · hard AND · 학습된
  게이트)까지 일반화하지 않는다.

## Cross-links

H_9294 (본 H 가 검정한 가설의 출처 · 🧱 STRENGTH-ONLY) · H_9293 · H_9292 (계측기 감사) ·
H_1283 (축의 출처) · H_1448 (TIMING 🟢 WIRED — "게이팅이라서 뚫린 게 아니다" 가 본 H 의 결론) ·
convergence `h-9295-p-2026-07-14-1` (통제군의 증명상-동일 논증은 실측 검산하라) ·
`a_phi_iit4_tool` · `a_break_the_wall` · `a_toy_scale_recheck` · `negative-claims-need-tost-not-ns` ·
`control-must-match-mediating-covariate` · c9 · c16 · p7
