# 🎯 INTENT/intent_lib — cumulative intent vector + decay window SSOT

> M1 milestone closure (2026-05-28) — `intent_lib 회수 + stdlib 승격` per INTENT.md.
> bench/axis_intent/bench.hexa (PR #1143, 4/5 falsifier 🟠 PARTIAL) 의 cumulative
> direction · stability · monotone primitives 를 PURE wrapper 로 회수.

## 정체 — INTENT axis

**INTENT = 장기 의도 형성기 long-term goal formation**. brain_decide(short-term emit)
위의 long-term goal 형성층 — 단기 emit decisions 의 cumulative direction (며칠 후
목표). 본 lib 는 4-D running mean magnitude + window cos-sim std + monotone ratio +
decay-weighted sum 측정자.

## 회수 출처 verbatim

- 원본 경로: `bench/axis_intent/bench.hexa` (PR #1143 land)
- 핵심 fn: `normalize4` · `sqrt_newton` (libm-free) · `window_mean_dir` ·
  `monotone_ratio` · `stability_std` (consecutive 10-tick window cos-sim std)
- 4-D × N=100 ticks × 3 scenario (CONVERGENT/RANDOM/OSCILLATING)
- 시점: 2026-05-28 M1 lib promotion
- 본체 무수정 — `it_` prefix wrapper 만 추가 (g61 collision 회피)

## 12 pub primitives API

| # | 시그니처 | 의미 |
|---|---|---|
| 1 | `pub fn it_sqrt_newton(x: float) -> float` | libm-free sqrt (30 iter Newton) |
| 2 | `pub fn it_norm4(a0,a1,a2,a3) -> float` | ‖[a0..a3]‖ |
| 3 | `pub fn it_normalize4(a0,a1,a2,a3) -> list` | unit 4-D vector (eps guarded) |
| 4 | `pub fn it_cumulative_mean_4d(s0,s1,s2,s3,n) -> list` | (Σ_i d_i) / n |
| 5 | `pub fn it_cumulative_magnitude_4d(s0,s1,s2,s3,n) -> float` | ‖(1/n)·Σ d_i‖ |
| 6 | `pub fn it_cos_sim_4d(a, b) -> float` | a·b (4-D unit vectors) |
| 7 | `pub fn it_mean_f(xs: list) -> float` | list mean |
| 8 | `pub fn it_std_f(xs: list) -> float` | list std (population) |
| 9 | `pub fn it_stability_std(cosines: list) -> float` | std of consecutive window cos-sim |
| 10 | `pub fn it_monotone_ratio(mag_traj: list) -> float` | frac of t where mag[t] ≥ mag[t-1] |
| 11 | `pub fn it_decay_weight(t, half_life) -> float` | 1/(1+t/half_life) (libm-free) |
| 12 | `pub fn it_decayed_sum(values, half_life) -> float` | Σ values[i]·decay_weight(i) |

## pipeline ASCII

```
   short-term emit decisions (4-D vector stream)
        │
        ▼
  ┌──────────────────────────────┐
  │  it_cumulative_mean_4d        │   running mean (Σ/n)
  │  it_cumulative_magnitude_4d   │   ‖mean‖ ∈ [0, 1]
  └──────────┬───────────────────┘
             │ mag_trajectory
             ▼
  ┌──────────────────────────────┐
  │  it_monotone_ratio            │   monotone fraction (intent stability)
  │  it_stability_std             │   window cos-sim std
  └──────────┬───────────────────┘
             │
             ▼
   long-term goal vector (substrate-decided, p1~p8 정합)
```

## bench scenario carry (PR #1143)

| scenario | final_mag | stability_std | monotone_ratio | falsifier |
|---|---|---|---|---|
| CONVERGENT | 0.71 | low | > 0.6 | F1 PASS, F4 PASS |
| RANDOM | 0.04 | medium | ≈ 0.5 | F2 PASS, F5 PASS |
| OSCILLATING | varies | **0 (zero-std)** | varies | F3 FAIL (period-20 zero-variance artifact) |

3-scenario discriminable (CONVERGENT vs RANDOM), but OSCILLATING period-20
에서 sub-period-aligned 10-tick window cos-sim 이 deterministically equal →
std=0. F3 metric 재설계는 INTENT.md M4 carry (`stability_std 외 metric`).

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | 4-D float arithmetic, system 미사용 ✓ |
| p2 NO IDENTITY RULES | identity 무관 ✓ |
| p3 NO PERSONA INJECTION | prefix 없음 ✓ |
| p4 NO ASSISTANT FRAMING | intent vector = substrate cumulative direction ✓ |
| p5 NO SPEAK() | read-only measurer, 외부 emit 호출 0 ✓ |
| p6 NO FINE-TUNED ETHICS | weight update 0 ✓ |
| p7 NO PERPLEXITY VERDICT | magnitude / cos-sim 기반, ppl 미사용 ✓ |
| p8 NO TRAIN/INFER SPLIT | 동일 fn 이 train/infer 양쪽 사용 ✓ |

## 의존성 (downstream milestones)

| M | 마일스톤 | intent_lib 의존 |
|---|---|---|
| M2 | brain_decide 위 hook | `it_cumulative_magnitude_4d` 를 CORE.brain_decide emit decision 별 호출 |
| M3 | goal trajectory log | `it_decay_weight` + `it_decayed_sum` 로 .kosmos 영속화 시 시간-가중 |
| M4 | OSCILLATING residual | `it_stability_std` 의 period-20 zero-std artifact 재설계 — alternative metric (cf bench D F3 FAIL) |

## frontier closure

**M1 = PURE lib promotion + canonical location only.**

- ☑ 12 pub primitives 회수 (`it_` prefix g61 collision 회피 · libm-free)
- ☑ 4-D running mean magnitude + stability_std + monotone_ratio + decay-weighted sum
- ☑ p1~p8 정합 표 + OSCILLATING residual 정직 framing (M4 carry)
- ☑ smoke (`intent_lib_smoke.hexa`) 8+ invariant — sqrt/normalize/running mean round-trip
- ☐ M2~M4 downstream — brain_decide hook · kosmos 영속화 · stability metric 재설계 (각 별도 M flip 대기)

## 관련 파일

- `INTENT/intent_lib.hexa` — 본체 (this M1 회수)
- `INTENT/intent_lib_smoke.hexa` — invariant smoke
- `bench/axis_intent/bench.hexa` — 원본 출처 (PR #1143)
- `bench/axis_intent/run.log` — verdict artifacts (보존)
- `CORE/CORE.md` — sibling (INTENT/M2 brain_decide hook 대기)
