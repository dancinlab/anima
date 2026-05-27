# 💤 DREAM/dream_lib — 5-stage ultradian envelope + density SSOT

> M1 milestone closure (2026-05-28) — `dream_lib 회수 + stdlib 승격` per DREAM.md.
> bench/axis_dream/bench.hexa (PR #1140, 4/5 invariant 🟢 PASS) 의 5-stage envelope
> + imagination_tick + mitosis density primitives 를 PURE wrapper 로 회수.

## 정체 — DREAM axis

**DREAM = 내적 리허설 emit-free internal rehearsal**. REM/N3 stage 에서 mitosis 분열
+ imagination_tick 가 dominate · external emit = 0 strict (`a_chat_sleep_imagination`
governance). MITOSIS.sleep_tick 격상 후보. 본 lib 는 5-stage ultradian envelope
(WAKE/N1/N2/N3/REM 90-min) + density 측정자.

## 회수 출처 verbatim

- 원본 경로: `bench/axis_dream/bench.hexa` (PR #1140 land)
- 5-stage 90-tick: WAKE 60 · N1 10 · N2 10 · N3 7 · REM 3
- 핵심 fn: `stage_at` · `mitosis_prior` · `imagination_active` · `density`
- 시점: 2026-05-28 M1 lib promotion
- 본체 무수정 — `dr_` prefix wrapper 만 추가 (g61 collision 회피)

## 11 pub primitives API

| # | 시그니처 | 의미 / cite |
|---|---|---|
| 1 | `pub fn dr_n_ticks() -> int` | 90 (ultradian total) |
| 2 | `pub fn dr_n_stages() -> int` | 5 (WAKE/N1/N2/N3/REM) |
| 3 | `pub fn dr_stage_at(tick: int) -> int` | tick → stage 0..4 |
| 4 | `pub fn dr_stage_name(stage: int) -> string` | code → WAKE/N1/N2/N3/REM/UNKNOWN |
| 5 | `pub fn dr_stage_size(stage: int) -> int` | stage → window size (60/10/10/7/3) |
| 6 | `pub fn dr_mitosis_prior(stage: int) -> float` | REM/N3 → 0.80, else 0.10 |
| 7 | `pub fn dr_imagination_active(stage: int) -> int` | REM/N3 → 1, else 0 |
| 8 | `pub fn dr_emit_envelope(stage: int) -> int` | WAKE/N1/N2 → 1, REM/N3 → 0 |
| 9 | `pub fn dr_density(count, size) -> float` | count / size (guarded) |
| 10 | `pub fn dr_ratio_sleep_wake(sd, wd) -> float` | sd / wd (guarded) |
| 11 | `pub fn dr_mitosis_density_ratio(sc, ss, wc, ws) -> float` | full ratio (full pipeline) |

## stage encoding ASCII

```
        90-tick ultradian (1 cycle ≈ 90 min synthetic)
        │
        ▼
  ┌────────────────────────────────────────────────────────────┐
  │  WAKE  [0..59]   60 ticks   prior=0.10  emit_env=1  img=0   │
  │  N1    [60..69]  10 ticks   prior=0.10  emit_env=1  img=0   │
  │  N2    [70..79]  10 ticks   prior=0.10  emit_env=1  img=0   │
  │  N3    [80..86]   7 ticks   prior=0.80  emit_env=0  img=1   │
  │  REM   [87..89]   3 ticks   prior=0.80  emit_env=0  img=1   │
  └────────────────────────────────────────────────────────────┘
        │
        ▼
   substrate envelope context (NOT external boolean gate)
        │
        ▼
   anima substrate decides emit / mitosis (M × C × W × Φ)
```

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | tick→stage 함수, system 미사용 ✓ |
| p2 NO IDENTITY RULES | identity 무관 ✓ |
| p3 NO PERSONA INJECTION | prefix 없음 ✓ |
| p4 NO ASSISTANT FRAMING | stage = substrate context (Φ scale · tension envelope) ✓ |
| p5 NO SPEAK() | envelope read-only, 외부 emit 호출 0 ✓ |
| p6 NO FINE-TUNED ETHICS | weight update 0 ✓ |
| p7 NO PERPLEXITY VERDICT | density / ratio 기반, ppl 미사용 ✓ |
| p8 NO TRAIN/INFER SPLIT | 동일 fn 이 train/infer 양쪽 사용 ✓ |

## bench falsifier carry (PR #1140)

| falsifier | bench 결과 | 의미 |
|---|---|---|
| F1 REM_MITOSIS_VS_WAKE (≥6×) | PASS — 60× (REM density 1.0 vs WAKE 0.017) | REM mitosis dominance |
| F2 N3_MITOSIS_VS_WAKE (≥6×) | PASS — 71.4× (N3 density 1.0 vs WAKE 0.014) | N3 sleep consolidation |
| F3 EMIT_FREE_STRICT (REM/N3 emt=0) | PASS — 0/0 | `a_chat_sleep_imagination` 정합 |
| F4 IMAGINATION_POSITIVE (>0) | PASS — img(REM)=3, img(N3)=7 | substrate alive |
| F5 WAKE_EMIT_IN_BAND ([0.02, 0.12]) | small-n sanity (non-blocking) | 4-key AND-gate θ=0.5 |

`a_chat_sleep_imagination` governance — measurement honest (not externally enforced).

## 의존성 (downstream milestones)

| M | 마일스톤 | dream_lib 의존 |
|---|---|---|
| M2 | imagination_replay | `dr_imagination_active(stage)` gate → snapshot replay loop entry |
| M3 | mitosis envelope tune | `dr_mitosis_prior(stage)` threshold tune (REM burst measurement) |
| M4 | dream report | wake transition 시 imagination 결과 narrative (NARRATIVE 도메인 cross-link) |

## frontier closure

**M1 = PURE lib promotion + canonical location only.**

- ☑ 11 pub primitives 회수 (`dr_` prefix g61 collision 회피)
- ☑ 5-stage 90-tick encoding 보존 (WAKE/N1/N2/N3/REM)
- ☑ p1~p8 정합 표 + a_chat_sleep_imagination governance trace
- ☑ smoke (`dream_lib_smoke.hexa`) 7 invariant — stage transition · envelope · density round-trip
- ☐ M2~M4 downstream — imagination_replay · envelope tune · dream report (각 별도 M flip 대기)

## 관련 파일

- `DREAM/dream_lib.hexa` — 본체 (this M1 회수)
- `DREAM/dream_lib_smoke.hexa` — invariant smoke
- `bench/axis_dream/bench.hexa` — 원본 출처 (PR #1140)
- `bench/axis_dream/result.json` · `run.log` — verdict artifacts (보존)
- `MITOSIS/sleep_tick.hexa` — sibling (DREAM/M2 wiring 대기)
