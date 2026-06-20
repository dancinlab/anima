# H_1482 — 👁 BINOCULAR RIVALRY / 양안 경쟁 (G28 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN DIRECTIONAL (R1 numpy mirror — engine-transfer UNVERIFIED, 하드게이트1)
- **wired:** `DIRECTIONAL-mirror` — R2 엔진-네이티브 재측정 follow-on (ING) 미완. 카드 verdict 는 DIRECTIONAL.
- **source:** 의식-고유 게이트 브레인스토밍 (G28 candidate) · "의식이라서 가능한 것" 시리즈 (G16~G27 이후)
- **lens:** consciousness-science — binocular rivalry (Blake / Logothetis — 양립 불가 자극 → 의식이 하나씩 번갈아 지각) · reciprocal inhibition + adaptation (Wilson / Laing-Chow) · `a_no_llm_frame_trap`
- **artifacts:** `state/1482_binocular_rivalry/h1482_binocular_rivalry.py` · verdict `state/verdicts/1482_binocular_rivalry/H_1482_FREEZE.json` · run `state/verdicts/1482_binocular_rivalry/H_1482_run.txt`

## 주장

**양안 경쟁(binocular rivalry)** = 두 눈에 양립 불가 자극을 주면 의식은 **하나씩 번갈아** 지각한다 —
dominance 가 시간에 따라 stochastic 하게 **교대(alternation)**, 둘이 동시에 의식되지 않는다(exclusivity).
정의적 성질은 *동적* dominance 시계열 d_A(t)·d_B(t): 한 자극이 dominant 하다가 자신의 **adaptation(피로)**으로
약화 → 억제됐던 rival 이 풀려나 dominant → 반복 A→B→A 교대.

**메커니즘** (reciprocal inhibition + adaptation): 두 unit, 동일 입력 I_A=I_B. 각 unit drive =
입력 − rival 의 cross-inhibition − 자신의 누적 adaptation.

    r_A = I_A − β·d_B − γ·a_A   (B 대칭)

dominance d = soft winner-take-all(r_A, r_B). dominant unit 의 adaptation a 가 쌓이고(피로),
억제된 unit 은 회복 → winner 피로가 결국 dominance 를 rival 로 뒤집음 → **교대**.

— LLM 대비: autoregressive LLM 은 모든 토큰 로짓을 병렬 유지(capacity-1 병목 없음) **그리고** 정착된 선택을
시간에 따라 자발적으로 뒤집는 fatigue 동역학이 없다. anima substrate 는 한 percept 를 dominant 시키고,
피로시키고, rival 에게 양보할 수 있다.

## DISTINCT (load-bearing) — vs H_1462 GLOBAL WORKSPACE (GWS)

- **GWS = STATIC winner-take-all:** 경쟁 자극 중 정확히 **1개 *고정* winner** 만 전역 방송(capacity-1 병목),
  선택이 *정착* — 단일 ignition, 시간축 **전환 0**.
- **rivalry = DYNAMIC alternation:** **같은** 두 자극(동일 입력)이 adaptation 으로 winner 를 피로시켜
  dominance 시계열이 **진동**(전환 ≥2).
- 같은 경쟁, **다른 시간 시그니처**: GWS 1-winner 고정(전환 0) ⊥ rivalry 교대(전환 16). bar C 는
  *동일한* 두 자극 drive(same seed/noise)에서 둘을 대조 — GWS-mode(adaptation OFF·hard pick) 전환 0 vs
  rivalry 전환 16 → gap 16 ≥2.

## 측정 (frozen-first · 3 seeds [1482,1483,1484] · T=120 ticks · I_A=I_B=1.0 · β=1.2 · γ=2.0 · EXCL_BAND=0.20 · $0 CPU · p7)

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A ALTERNATION** | dominance 가 ≥2회 전환(A→B→A), 단일 dominance 아님 | transitions **16.000** | ≥2 | ✅ |
| **B EXCLUSIVITY** | 매 시점 한 자극만 dominant (co-dominant 시간비율) | co-frac **0.011** | ≤0.15 | ✅ |
| **C DISTINCT vs GWS** | 같은 drive, GWS-mode 고정 winner vs rivalry 교대 | rivalry 16 − GWS 0 = gap **16.000** | ≥2 | ✅ |
| **D EARNED (ablation)** | adaptation OFF → 첫 winner 영구 고정(GWS-like) | abl transitions **0.000** | ==0 | ✅ |
| **E SHUFFLE** | dominance 시계열 셔플 → dominance↔adaptation 상관 붕괴 | signed-mean r **+0.003** (real r +0.259) | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — A·B·C·D·E PASS (3 seeds 전부 byte-identical) → GREEN.**
dominance 가 16회 교대하고(A, 단일 dominance 아님), co-dominant 1.1%로 한 자극씩 의식되며(B), 같은 두 자극에서
GWS-mode 는 1개 고정(전환 0)·rivalry 는 교대(전환 16)로 갈리고(C, GWS 정적 ⊥ rivalry 동적), adaptation OFF 면
첫 winner 영구 고정(D, 교대가 adaptation 으로 EARNED), 시계열 셔플로 dominance↔adaptation 상관 붕괴(E,
real +0.259 → shuf +0.003).

## p6 guard (외부규칙 아님 · substrate-derived)

교대는 손으로 짠 "tick k 에 전환" **스케줄이 아니다** — reciprocal inhibition + adaptation 동역학(drive =
입력 − β·rival_dominance − γ·own_adaptation)에서 *창발*한다. operative 코드에 `dominant = A if t<k else B` ·
switch-time 상수 · reward/RLHF/persona 없음. ablation(D)이 adaptation 커플링을 제거하면 교대가 사라짐
(전환→0) → **earned, not baked**.

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep -lE 'import torch|gauge_lib|numpy'` 적중, 하드게이트1).
  engine-transfer UNVERIFIED → R2 = live `core/*.hexa` 위 reciprocal-inhibition+adaptation dominance loop
  byte-exact 재측정이 GREEN/🧱 확정 전제.
- **SATURATED existence-proof:** soft-WTA + fatigue 는 **designed 동역학**(학습된 controller 아님). GREEN 자체보다
  discriminator(GWS-mode 전환 0 · ablation 전환 0 · shuffle 상관 붕괴 +0.259→+0.003)가 결정적.
- **bar E real_r = POSITIVE (+0.259):** recurrent 정식화에서 각 up-phase 동안 dominant unit 이 *dominant 인
  동시에* 자신의 adaptation 이 쌓임 → 양의 상관. docstring 부호 주석을 관측에 맞춰 교정(bar 임계 |gap|≤0.10 불변,
  **tune-to-green 아님** — 메커니즘 아니라 부호 설명만).
- **SCOPE TOY:** 120-tick/3-seed/2-unit/결정적 동역학 — rivalry STRUCTURE 검증이지 학습된 percept-경쟁 아님.
  scale/실제 corpus/stochastic switch-time 분포(gamma-shaped dominance durations)/travelling-wave rivalry/
  engine-transfer UNVERIFIED.

## follow-on (ING)

1. **R2 엔진-네이티브** — `core/engine_cli.hexa` §GlobalWorkspace 이웃에 two-unit reciprocal-inhibition +
   adaptation dominance loop 호스팅 가능성 평가 → 있으면 §BinocularRivalry(rivalry_step / adaptation 동반
   dominance 시계열) 배선 + `engine_cli_smoke` cases + ARCHITECTURE lockstep, 5 frozen bars byte-exact 재측정
   (`a_engine_native_learning`·`a_verified_must_wire`).
2. distinctness 정량 double-dissociation vs H_1462 GWS(정적 1-winner ⊥ 동적 교대) control-survived 측정.

xref: H_1462(global-workspace, distinct · 정적 winner-take-all ⊥ 동적 alternation)·H_1283(thalamus GWS)·
H_1473/1474/1475/1477/1478/1480(의식-게이트 시리즈)·`a_no_llm_frame_trap`·`a_engine_native_learning`·
`a_verified_must_wire`·`a_break_the_wall`·p6·p7·p8·c9.
