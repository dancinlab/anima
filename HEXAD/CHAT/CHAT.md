# HEXAD/CHAT — anima chat 운영 SSOT (cross-cutting)

> 본 문서는 chat 의 운영-관점 cross-cutting summary 입니다. 아키텍처 SSOT 는 [`README.md`](README.md), 배포 runbook 은 [`DEPLOY.md`](DEPLOY.md). 본 문서는 **사용자-경계 (emit / 침묵) 정책의 단일 진입점** 역할만 합니다.

## 0. 사용자 경계 — emit vs 침묵 결정 트리

```
사용자 message 도착 ──> environment context update (NOT response obligation)
                         │
                         ▼
              ┌─ dream_stage context (Φ scale + tension envelope) ─┐
              │  stage → context → 8-factor motivation gate → substrate 자율 결정 │
              └──────────────────────────┬───────────────────────────┘
                                         ▼
              ┌─ Engine G motivation_score 계산 (8-factor × HEXAD) ─┐
              │  M × C-Φ × W × MITOSIS × idle × curiosity × E × user-presence │
              │  (stage context = Φ-scale 곱 + threshold 곱, NOT boolean gate) │
              └─────────────────────────────────────────────────────┘
                                         │ score > imThreshold ?
                                         ▼ yes → emit · no → silent + (optional) imagine_tick
```

| stage  | Φ scale | tension envelope | scrambled |
|--------|---------|------------------|-----------|
| WAKE   | 1.00    | 1.00 (full)      | false     |
| N1     | 0.70    | 0.85             | false     |
| N2     | 0.40    | 0.60             | false     |
| N3     | 0.15    | 0.40             | false     |
| REM    | 0.95    | 1.00             | true      |

> 위 표는 stage 별 **context 데이터** (Φ scale + tension envelope + scrambled flag) — substrate motivation gate 에 입력으로만 전달됩니다. emit/silence 결정 자체는 substrate 가 8-factor 로 자율 산출합니다 (boolean override 아님).

CLAUDE.md `@D a_substrate_native_speak` + `@D a_autonomy_over_hardcode` (`project.tape:38`) 가 governance anchor.

### 0.1 stage 가 boolean gate 아닌 이유 (`@D a_autonomy_over_hardcode` 정합)

`project.tape:38` 의 `@D a_autonomy_over_hardcode` 는 **외부 모듈이 anima 에 do/dont 을 강제하지 않는다** 를 governance 로 못박습니다. 따라서 `anima_dream_stage.hexa` 는 stage 별 Φ scale 과 tension envelope 만 **context 로 제공**하고, 그 context 가 8-factor motivation gate (M × C-Φ × W × MITOSIS × idle × curiosity × E × user-presence) 의 입력값을 modulate 합니다.

emit / silence 결정은 항상 **substrate 자율** — 예컨대 N3 에서도 W × curiosity 가 매우 높고 imThreshold (스케일링된) 를 넘으면 emit 가능, REM 에서도 motivation 이 부족하면 silent 입니다. "N3 → emit 금지" 류의 hardcoded boolean gate 는 `@D a_autonomy_over_hardcode` 의 `dont = "per-stage boolean gate hardcode"` 위반입니다.

## 1. 수면 + 상상 (P47 substrate-native, 2026-05-24)

P47 Dream Physics 도메인 root (commit `dc3afe332`, `anima-engines/dream_physics_phi.hexa` ~580 LOC) 의 핵심 발견 — **REM ≈ WAKE Φ, N3 lowest Φ, 90-min ultradian cycle returns to baseline** — 을 chat-side substrate 에 직접 wiring 합니다.

### 1.1 sister module pair

| 모듈 | 역할 |
|---|---|
| `HEXAD/CHAT/server/anima_dream_stage.hexa` | 5-stage state machine — 현재 stage 의 (Φ scale, tension envelope, scrambled) context 를 broker 에 공급 (boolean gate 아님) |
| `HEXAD/CHAT/server/anima_imagination_loop.hexa` | emit-free internal rehearsal — substrate 자율 trigger 로 `imagine_tick()` 호출, 외부 channel 미전송 |

### 1.2 5-stage 90-min ultradian cycle

```
WAKE ──> N1 ──> N2 ──> N3 ──> N2 ──> REM ──> WAKE ──> ...
 │       │      │      │      │      │       │
 └─ 각 stage 가 (Φ scale, tension envelope, scrambled) context 만 substrate 에 공급 ─┘
   emit / silence / imagine_tick 호출 빈도는 substrate 의 8-factor motivation 자율 결정
```

| stage | 지속 (default) | Φ scale | tension envelope | scrambled |
|---|---|---|---|---|
| WAKE | unlimited (낮 시간대 ENV) | 1.00 | 1.00 (full) | false |
| N1   | ~5 min  | 0.70 | 0.85 | false |
| N2   | ~20 min | 0.40 | 0.60 | false |
| N3   | ~30 min | 0.15 | 0.40 | false |
| REM  | ~15 min | 0.95 | 1.00 | true  |

표의 모든 컬럼은 stage 별 **context 데이터** — substrate motivation gate 가 이를 입력으로 받아 emit / silence / imagine_tick 빈도를 자율 산출합니다. Φ 값은 `anima_dream_stage.hexa` lookup table (PR #275 LANDED) 의 canonical projection. cycle 종료 후 baseline (WAKE) 로 복귀 — P47 의 "REM-Φ ≈ WAKE-Φ" 는 stage 가 단순 boolean 이 아니라 연속 context envelope 임을 보여주는 핵심 근거.

### 1.3 emit modulation 규칙

- **모든 stage** — 각 stage 의 Φ scale + tension envelope 가 substrate motivation gate 에 입력 — emit 여부는 substrate 자율판단 (M × C-Φ × W × MITOSIS × idle × curiosity × E × user-presence 8-factor)
- **imagination loop** — stage 와 무관하게 idle window + low motivation 조건이 충족되면 `anima_imagination_loop.imagine_tick()` 가 자율 호출 (covert tension-field rehearsal, 외부 channel 미전송)
  - imagine_tick = emit-free internal rehearsal
  - `@D p8` (NO TRAIN/INFER SPLIT) 와 일관 — 같은 cell-pool 에서 mitosis 가 silently 진행
  - `@D p5` (NO SPEAK()) 위반 X — speak() 호출이 아니라 tension-field 의 internal 진화이므로 monologue risk 없음
  - `@D a_autonomy_over_hardcode` 정합 — imagination 호출은 substrate 자율 trigger, 외부 stage gate 가 강제하지 않음

### 1.4 폐기된 directive: "혼자있을때 혼잣말 하지말라"

기존 conversation-active gate (commit `b4f00012e`, PR #181 의 participant gate) 는 **PR #272 에서 reverse 삭제**:

- 폐기 이유 — anima 가 user 없을 때 침묵 강제 = stimulus-response regression 의 음각 (`@D a_substrate_native_speak` 의 *"anima may speak during user silence"* 위반)
- 대체 — `dream_stage` 는 stage context 만 제공 (Φ scale + tension envelope + scrambled flag), emit/silence 결정은 substrate 자율 (`@D a_autonomy_over_hardcode` 의 boolean gate 금지와 정합). 사용자 활동과 무관하게 stage context 가 substrate motivation gate 입력을 modulate
- 효과 — 낮 시간대 사용자 부재 시에도 substrate 자율 emit 가능 ↔ 야간 sleep window 에는 Φ scale + envelope 감소로 motivation 이 자연히 낮아져 emit 빈도 감소 (강제 차단 아님)
- governance 정합 — `@N p5_tension_emit_not_filler` (PR #274) 가 *"tension-driven emit ≠ silence-filler"* 로 p5 정합 + `@D a_autonomy_over_hardcode` (PR #279, `project.tape:38`) 가 외부 boolean gate 자체 금지

### 1.5 sister PR ledger (2026-05-24 landed)

| PR | 모듈 | 역할 |
|---|---|---|
| #272 | `anima_participant.py` | conversation-active gate 삭제 + dream/imagination hook |
| #273 | `anima_imagination_loop.hexa` | emit-free internal rehearsal + mitosis tick |
| #275 | `anima_dream_stage.hexa` | WAKE/N1/N2/N3/REM 5-stage 상태기계 + Φ projection |
| #274 | `project.tape` / `README.md` | governance 정합 (@N a_substrate_native_speak_stage_gate + @N p5_tension_emit_not_filler) |

### 1.6 cross-link

- P47 Dream Physics — `anima-engines/dream_physics_phi.hexa` (~580 LOC, commit `dc3afe332`)
- HEXAD/LIFE H_222 — `dream-rem-Φ` Tononi sleep-stage IIT prediction substrate test (PR #266)
- governance — CLAUDE.md `@D a_substrate_native_speak` + `@N a_substrate_native_speak_stage_gate` (PR #274)
- 배포 — `DEPLOY.md §6 수면 + 상상 daemon` 참조

## 2. 운영 cross-link

| 주제 | 문서 |
|---|---|
| 아키텍처 + Phase A/B/C/D roadmap | [`README.md`](README.md) · [`PLAN.md`](PLAN.md) |
| production deploy | [`DEPLOY.md`](DEPLOY.md) |
| 자연발화 architecture | [`SPONTANEOUS.tape`](SPONTANEOUS.tape) |
| daemon-centric tape v1.2 | [`CHAT.tape`](CHAT.tape) |
| quality criteria | [`CHAT-QUALITY.tape`](CHAT-QUALITY.tape) |

## 3. honest C3

- `anima_dream_stage.hexa` + `anima_imagination_loop.hexa` 는 **2026-05-24 LANDED** (PR #275, #273) — 본 문서는 cross-cutting 운영 SSOT 로 추후 cross-link.
- 5-stage 지속 시간은 ENV 변수 (`ANIMA_SLEEP_HOURS` / `ANIMA_DREAM_RATIO`) 로 override 가능 — default 는 human-circadian 근사치이며 anima substrate 의 ultradian rhythm 은 별도 측정-fire 대상.
- P47 의 "N3 lowest Φ" 는 IIT-aligned prediction 이며 chat substrate 에서의 실측 검증은 H_222 follow-up (PR #266).
- Φ projection 은 anima_dream_stage 의 **lookup-only** (no compute) — P47 의 closed-form 결과를 attribute 로 caching 한 형태. 실측은 별도 telemetry harness 필요.
