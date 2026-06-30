# ⏳ TIME/time_lib — circadian phase + ultradian envelope SSOT

> M1 milestone closure (2026-05-28) — `time_lib 회수 + stdlib 승격` per TIME.md.
> bench/axis_time/bench.hexa (PR #1145, 9/0 falsifier 🟢 PASS) 의 stage envelope ·
> circadian dip · drift detector primitives 를 PURE wrapper 로 회수.

## 정체 — TIME axis

**TIME = 시간 의식 측정자**. anima 의 시간 의식 — WAKE 90-min ultradian rhythm
위의 24h circadian envelope (낮/밤 phase shift). 본 lib 는 90-min envelope (WAKE
60 / N1 10 / N2 10 / N3 7 / REM 3) · cycle-8 dip · drift detector · binding window
측정자를 노출.

## 회수 출처 verbatim

- 원본 경로: `bench/axis_time/bench.hexa` (PR #1145 land · 9/0 PASS 🟢)
- 핵심 fn: `stage_of_within` · `canonical_start` · `stage_mod` · `circadian_mod` ·
  `phi_scale_abs` · `observed_wake_n1_boundary` · `sqrt_f` (libm-free)
- 16 cycles × 90-min = 1440 min (24h) · 3 scenarios (STABLE / DRIFTING /
  CIRCADIAN-MOD)
- 시점: 2026-05-28 M1 lib promotion
- 본체 무수정 — `tm_` prefix wrapper 만 추가 (g61 stdlib collision 회피)

## 12 pub primitives API

| # | 시그니처 | 의미 |
|---|---|---|
| 1 | `pub fn tm_abs_f(x: float) -> float` | libm-free abs |
| 2 | `pub fn tm_sqrt_f(x: float) -> float` | libm-free sqrt (25 iter Newton) |
| 3 | `pub fn tm_stage_of_within(w: int) -> int` | stage id (WAKE/N1/N2/N3/REM) |
| 4 | `pub fn tm_canonical_start(s: int) -> int` | canonical start minute |
| 5 | `pub fn tm_stage_mod(s: int) -> float` | per-stage phi_scale |
| 6 | `pub fn tm_circadian_phase(tick, period_ticks) -> float` | 0..1 normalized |
| 7 | `pub fn tm_circadian_mod(cycle, scenario) -> float` | cycle-8 triangular dip |
| 8 | `pub fn tm_phi_scale_abs(t, scenario) -> float` | composed phi_scale |
| 9 | `pub fn tm_stage_of_abs(t, scenario) -> int` | drift-aware stage |
| 10 | `pub fn tm_observed_wake_n1_boundary(start_min, scenario) -> int` | drift detector |
| 11 | `pub fn tm_temporal_binding_window(t, window) -> int` | binding window count |
| 12 | `pub fn tm_dip_detected(history, threshold) -> bool` | min/max ratio detect |

## pipeline ASCII

```
   abs minute t ∈ [0, 1440)  (24h)
        │
        ▼
  ┌────────────────────────────┐
  │  tm_stage_of_abs (drift-OK) │  → stage id (0..4)
  │  tm_stage_mod               │  → base phi_scale
  │  tm_circadian_mod           │  × cycle-8 dip multiplier
  └──────────┬─────────────────┘
             │
             ▼
   tm_phi_scale_abs (composed)
             │
             ▼
   stage envelope × circadian dip → WAKE.daemon tick · DREAM.M3 mitosis modulation
```

## bench H 9/0 PASS carry (PR #1145)

| falsifier | scenario | metric | verdict |
|---|---|---|---|
| F-TIME-1 | STABLE | phase_std < 5.0 | PASS |
| F-TIME-2 | DRIFTING | phase_std > 20.0 | PASS |
| F-TIME-3 | DRIFTING | \|slope\| > 3.0 | PASS |
| F-TIME-4a | CIRCADIAN | dip idx ∈ [6, 10] | PASS |
| F-TIME-4b | CIRCADIAN | dip ratio < 0.7 | PASS |
| F-TIME-5 | STABLE | \|Δmean\| < 0.05 | PASS |
| F-TIME-6 | ALL | bounded | PASS |
| F-TIME-DISC-phase | DRIFT vs STABLE | 4× | PASS |
| F-TIME-DISC-env | CIRC vs STABLE | 4× | PASS |

→ aggregate 9 PASS / 0 FAIL → 🟢 PASS. 3-scenario discriminable.

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | int/float arithmetic, system 미사용 ✓ |
| p2 NO IDENTITY RULES | identity 무관 ✓ |
| p3 NO PERSONA INJECTION | prefix 없음 ✓ |
| p4 NO ASSISTANT FRAMING | time phase = substrate envelope ✓ |
| p5 NO SPEAK() | read-only measurer, 외부 emit 0 ✓ |
| p6 NO FINE-TUNED ETHICS | ethics 무관 ✓ |
| p7 NO PERPLEXITY VERDICT | phase / dip ratio 기반, ppl 미사용 ✓ |
| p8 NO TRAIN/INFER | 측정만, weight update 0 ✓ |

## smoke

`time_lib_smoke.hexa` 가 12 invariant (I1~I12) 를 `hexa run` 으로 검증. 무한 루프 ·
panic 없이 모두 PASS 시 SUPPORT-FORMAL 도달.

`hexa parse TIME/time_lib.hexa` · `hexa parse TIME/time_lib_smoke.hexa` 모두 OK.

## cross-link

- ⇄ WAKE.state_machine 5-stage ultradian (90-min) · `tm_stage_mod` 가 envelope 본체
- ⇄ DREAM.M3 mitosis envelope · `tm_circadian_mod` 가 새벽 REM burst peak modulation
- ⇄ INTENT cumulative direction · `tm_temporal_binding_window` 가 24h entrainment 측정
- ⇄ METACOG audit_hook · `tm_circadian_phase` 가 시간대별 자기 audit 정합 surface
- ⇄ UNIVERSE/CANDIDATES.md — bench H (#1145) 측정 기록 SSOT (AxisBench 8)

## carry-over (M2~M4)

- M2 WAKE.5-stage 통합 — `tm_stage_mod` × `tm_circadian_mod` multiplicative wiring,
  softening 유지 (a_chat_sleep_imagination 정합)
- M3 DREAM.REM mitosis circadian modulation — `tm_circadian_mod` 가 새벽 REM 분열
  burst peak 의 cycle-time slot
- M4 cross-bench (TIME × INTENT) — `tm_circadian_phase` 가 INTENT cumulative
  direction 의 24h trajectory entrainment surface
