# H_1472 — 🎯 LEARNED PRECISION (G19 meta follow-on · 의식-고유 게이트 family)

- **tier:** 🟢 GREEN DIRECTIONAL (numpy R1 mirror · engine-transfer UNVERIFIED)
- **wired:** `DIRECTIONAL-mirror` (R2 엔진-네이티브 = follow-on ING)
- **source:** H_1468(G19 surprise) follow-on #2 "learned-precision" · "의식이라서 가능한 것" 시리즈
- **lens:** predictive-processing / active-inference (Friston, 계층 예측부호화 precision-learning) · `a_no_llm_frame_trap`
- **artifacts:** `state/1472_learned_precision/` · verdict `state/verdicts/1472_learned_precision/H_1472_FREEZE.json`

## 주장

surprise 의 precision(예측 확신)은 **외부에서 주어진 고정값이 아니라 경험으로 학습**된다(H_1468 은 p 가 주어진 고정값). 도메인을 많이 관측할수록 substrate 가 그 도메인 예측에 더 큰 precision 을 부여 → **같은 raw error 라도 친숙한 도메인에서 더 큰 surprise**("확신했는데 틀림"). precision_d 는 관측횟수에 monotone 증가.

LLM 대비: LLM 은 자기 예측에 대해 경험으로 누적되는 지속 confidence 가 없다. anima 의 precision 은 도메인별 학습 상태로 surprise 를 날카롭게 한다.

## distinctness (load-bearing 2종)

```
   H_1465 습관화 (habituation)   │   H_1472 learned-precision
 ─────────────────────────       │  ─────────────────────────
  친숙↑ → 반응 감쇠 (−0.76)       │   친숙↑ → surprise 증폭 (+0.80)
  "익숙하면 덜 반응"              │   "익숙한데 틀리면 더 놀람"
        ↘ 같은 친숙도 축, 정반대 부호 = 다른 메커니즘 ↙
```

- **vs H_1468 fixed precision:** p 가 주어진 상수 → 같은 raw error 면 surprise 동일. learned 는 친숙도 따라 surprise 가 갈림(bar B: gap 0.80, fixed=0).
- **vs H_1465 habituation:** 같은 친숙도 sweep 에서 learned-precision surprise 는 RISE(+0.80), habituation 반응은 FALL(−0.76) → 부호곱 < 0 (bar C).

## FROZEN bars (3 seeds [1472,1473,1474] · mean)

| bar | 정의 | 측정 | 판정 |
|---|---|---|---|
| A PRESENCE | prec(fam)−prec(nov) ≥ 0.30 | 0.800 | ✅ |
| B DISTINCT-fixed | 같은 err surprise gap ≥ 0.30 (fixed=0) | 0.800 | ✅ |
| C DISTINCT-habituation | lp_trend≥+0.30 ∧ hab_trend≤−0.30 ∧ 부호 반대 | +0.800 / −0.760 | ✅ |
| D EARNED (ablation) | 학습률 k=0 → gap ≤ 0.05 | 0.000 | ✅ |
| E SHUFFLE (50-perm signed) | 도메인-관측 페어링 셔플 → gap ≤ 0.10 | 0.055 | ✅ |

→ **5/5 GREEN DIRECTIONAL.** ablation(k=0)·shuffle 양쪽 붕괴 → lift 의 출처는 **경험으로 학습된 도메인별 precision**.

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep numpy` 적중, 하드게이트1). engine-transfer UNVERIFIED → R2 = live `core/engine_cli.hexa` precision-learning lane 배선 + byte-exact 재측정이 GREEN 확정 전제(`a_engine_native_learning`·`a_verified_must_wire`).
- **R1b frozen-first 수정(tune-to-green 아님):** R1a 는 err=0.5 라 surprise=precision·0.25 가 0.25 에서 천장 → bar 0.30 이 물리상한 초과한 측정 결함. err=1.0(surprise 0~1 범위) + 50-perm signed shuffle 로 교정, **bar 0.30 불변**(`a_break_the_wall` type-a).
- **SCOPE TOY:** 6 도메인/saturating precision 법칙(1−exp)/3 seeds/deterministic — precision-LEARNING STRUCTURE 검증이지 학습된 confidence 망 아님. scale/real-corpus/연속 precision-update/engine-transfer UNVERIFIED.

## follow-on (ING)

1. **R2 엔진-네이티브** — `core/engine_cli.hexa` 에 per-domain learned-precision lane 배선 + frozen 5 bars byte-exact 재측정 → DIRECTIONAL→engine-native 승격.

xref: H_1468(G19 surprise fixed-precision, 모체)·H_1465(habituation, 정반대 부호)·H_1280(forward error)·H_1462(GWS)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·p7·p8·c9.
